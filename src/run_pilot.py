"""Main experiment runner — sharded across GPUs, one row per (question × seed × method × budget).

This is the script that actually runs the pilot. A round is launched as N
parallel shards (`--gpu-shard i/N`), where each shard loads the configured HF
model, takes its slice of the question pool, and for every cell

    (doc_id, trial_seed, method, total_token_budget)

invokes the corresponding entry in `src.methods.run_method`. Each cell's
compute is wrapped in a `src.token_meter.TokenBudget` so prompt + output +
parse-repair + restart all count toward the same `budget_total`.

What the runner owns:

- **Question pool construction** (`build_question_pool`): loads the configured
  HF `datasets` split (GPQA or MMLU), samples `n_questions` with `sample_seed`,
  optionally shuffles the choice positions per question, and freezes the
  resulting manifest to `run_dir/questions_manifest.json` so re-runs are
  bit-identical.
- **Sharding** (`parse_gpu_shard`): an i/N split over the manifest by
  `manifest_index % N == i`.
- **Per-row execution**: builds the rendered prompt, calls `runner.generate_*`,
  passes the result through `parser.classify_parse_result`, and if the parse
  fails *and* `enable_parse_repair` is on and the budget reserve survives,
  spends a small `repair.parse` step trying to recover the answer.
- **Resume safety**: existing rows are read from `results_shard{i}.jsonl` and
  matching `(doc_id, seed, method, budget)` keys are skipped, so a crashed
  shard can be restarted without redoing finished work.
- **Outputs in `run_dir`**:
    - `results_shard{i}.jsonl`  : one JSON row per cell (the primary artifact),
    - `hotmess_shard{i}.jsonl`  : per-attempt records used by hot-mess metrics,
    - `status_shard{i}.json`    : live status read by `src.monitor`,
    - `questions_manifest.json` : frozen question pool,
    - `config_resolved.yaml`    : the config the run was actually started with,
    - `run_meta.json`           : run-wide metadata (created_at, expected total,
                                  parse policy, budgets, methods).

The fairness contract (token accounting, parse policy `P1R`, repair reserve)
is enforced here so all downstream comparisons sit on the same basis.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import yaml
from datasets import load_dataset
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer

from .methods import run_method
from .parser import (
    PARSE_FAIL_INVALID,
    PARSE_FAIL_MULTI_ANSWER,
    PARSE_FAIL_NO_ANSWER,
    classify_parse_result,
    count_flips,
    extract_last_option_anywhere,
    option_to_index,
)
from .token_meter import TokenBudget


@dataclass
class ModelRunner:
    model_id: str
    device: str
    use_fast_tokenizer: bool
    trust_remote_code: bool
    dtype: str

    def __post_init__(self) -> None:
        torch_dtype = torch.bfloat16 if self.dtype == "bfloat16" else torch.float16
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_id,
            use_fast=self.use_fast_tokenizer,
            trust_remote_code=self.trust_remote_code,
        )
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=torch_dtype,
            trust_remote_code=self.trust_remote_code,
            low_cpu_mem_usage=True,
        ).to(self.device)
        self.model.eval()

    def render_prompt(self, user_prompt: str) -> str:
        msgs = [
            {"role": "system", "content": "You are a precise reasoning assistant for multiple-choice QA."},
            {"role": "user", "content": user_prompt},
        ]
        try:
            return self.tokenizer.apply_chat_template(
                msgs,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False,
            )
        except Exception:
            return user_prompt

    def count_rendered_tokens(self, rendered_prompt: str) -> int:
        enc = self.tokenizer(rendered_prompt, return_tensors="pt")
        return int(enc["input_ids"].shape[-1])

    def generate_rendered(
        self,
        rendered_prompt: str,
        max_new_tokens: int,
        temperature: float,
        top_p: float,
        seed: int,
        retries: int = 2,
    ) -> Tuple[str, Dict[str, int]]:
        if max_new_tokens <= 0:
            return "", {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}

        inputs = self.tokenizer(rendered_prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.device)
        attn_mask = inputs["attention_mask"].to(self.device)
        input_tokens = int(input_ids.shape[-1])

        do_sample = temperature > 0
        last_err: Optional[Exception] = None
        for _ in range(retries + 1):
            try:
                torch.manual_seed(int(seed))
                if torch.cuda.is_available():
                    torch.cuda.manual_seed_all(int(seed))
                with torch.inference_mode():
                    outputs = self.model.generate(
                        input_ids=input_ids,
                        attention_mask=attn_mask,
                        max_new_tokens=max_new_tokens,
                        do_sample=do_sample,
                        temperature=max(temperature, 1e-5) if do_sample else None,
                        top_p=top_p if do_sample else None,
                        pad_token_id=self.tokenizer.pad_token_id,
                        eos_token_id=self.tokenizer.eos_token_id,
                        use_cache=True,
                    )
                gen_ids = outputs[0, input_tokens:]
                output_tokens = int(gen_ids.shape[-1])
                text = self.tokenizer.decode(gen_ids, skip_special_tokens=True)
                return text, {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                }
            except Exception as err:
                last_err = err
                torch.cuda.empty_cache()
                time.sleep(0.3)

        raise RuntimeError(f"Generation failed for {self.model_id}: {last_err}")


def parse_gpu_shard(raw: str) -> Tuple[int, int]:
    if "/" not in raw:
        raise ValueError("--gpu-shard must be in format i/N, e.g., 0/8")
    sid, total = raw.split("/", 1)
    return int(sid), int(total)


def now_ts() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _format_final_answer_text(option: str) -> str:
    if not option:
        return ""
    letter = option.strip().replace("(", "").replace(")", "").upper()
    if letter not in {"A", "B", "C", "D"}:
        return ""
    return f"Final Answer: {letter}\n"


def ensure_run_dir(cfg: Dict[str, object], run_id_arg: Optional[str]) -> Path:
    output_root = Path(cfg["experiment"]["output_root"]).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    run_id = run_id_arg or cfg["experiment"].get("run_id")
    if not run_id:
        run_id = dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    run_dir = output_root / str(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _answer_to_index(ans: object, choices: List[str]) -> int:
    if isinstance(ans, (int, float)):
        idx = int(ans)
        if 0 <= idx < len(choices):
            return idx
    raw = str(ans).strip()
    if raw.upper() in {"A", "B", "C", "D"}:
        return {"A": 0, "B": 1, "C": 2, "D": 3}[raw.upper()]
    if raw.startswith("(") and raw.endswith(")") and len(raw) == 3 and raw[1].upper() in {"A", "B", "C", "D"}:
        return {"A": 0, "B": 1, "C": 2, "D": 3}[raw[1].upper()]
    if raw.isdigit():
        idx = int(raw)
        if 0 <= idx < len(choices):
            return idx
    for i, c in enumerate(choices):
        if str(c).strip() == raw:
            return i
    raise ValueError(f"Cannot map answer to index: answer={ans!r}, choices={choices!r}")


def build_question_pool(cfg: Dict[str, object], run_dir: Path) -> List[Dict[str, object]]:
    manifest_path = run_dir / "questions_manifest.json"
    if manifest_path.exists():
        return json.loads(manifest_path.read_text())

    ds_cfg = cfg["dataset"]
    ds = load_dataset(ds_cfg["name"], ds_cfg["config"], split=ds_cfg["split"])
    n_questions_req = int(ds_cfg["n_questions"])
    n_questions = min(n_questions_req, len(ds))
    sample_seed = int(ds_cfg["sample_seed"])
    data_format = str(ds_cfg.get("format", "auto")).lower()
    shuffle_choices = bool(ds_cfg.get("shuffle_choices", True))
    question_field = str(ds_cfg.get("question_field", "question"))
    choices_field = str(ds_cfg.get("choices_field", "choices"))
    answer_field = str(ds_cfg.get("answer_field", "answer"))
    doc_prefix = str(ds_cfg.get("doc_id_prefix", ds_cfg["name"].split("/")[-1].replace("-", "_")))

    if n_questions_req > len(ds):
        print(
            f"[{now_ts()}] requested n_questions={n_questions_req} exceeds dataset size={len(ds)}; "
            f"clamping to {n_questions}"
        )

    rng = random.Random(sample_seed)
    selected = sorted(rng.sample(range(len(ds)), n_questions))

    items: List[Dict[str, object]] = []
    for i, ridx in enumerate(selected):
        row = ds[int(ridx)]
        is_gpqa_schema = all(
            k in row for k in ["Question", "Correct Answer", "Incorrect Answer 1", "Incorrect Answer 2", "Incorrect Answer 3"]
        )
        if data_format in {"gpqa"} or (data_format == "auto" and is_gpqa_schema):
            question_text = str(row["Question"])
            answers = [
                str(row["Correct Answer"]),
                str(row["Incorrect Answer 1"]),
                str(row["Incorrect Answer 2"]),
                str(row["Incorrect Answer 3"]),
            ]
            correct_idx = 0
            difficulty = row.get("Writer's Difficulty Estimate", None)
            domain = row.get("High-level domain", None)
            record_id = row.get("Record ID", ridx)
        else:
            if question_field not in row or choices_field not in row or answer_field not in row:
                raise KeyError(
                    f"Unsupported row schema for format={data_format}. Required keys: "
                    f"{question_field}, {choices_field}, {answer_field}; row keys={list(row.keys())}"
                )
            question_text = str(row[question_field])
            raw_choices = list(row[choices_field])
            if len(raw_choices) < 4:
                raise ValueError(f"Need at least 4 choices, got {len(raw_choices)} at idx={ridx}")
            answers = [str(x) for x in raw_choices[:4]]
            correct_idx = _answer_to_index(row[answer_field], answers)
            difficulty = row.get("difficulty", None)
            domain = row.get("subject", row.get("domain", None))
            record_id = row.get("id", row.get("question_id", ridx))

        order = [0, 1, 2, 3]
        if shuffle_choices:
            perm_rng = random.Random(sample_seed * 1000003 + int(ridx))
            perm_rng.shuffle(order)
        shuffled = [answers[j] for j in order]
        correct_pos = order.index(correct_idx)
        doc_id = f"{doc_prefix}_{record_id}_{ridx}"

        items.append(
            {
                "manifest_index": i,
                "dataset_index": int(ridx),
                "doc_id": doc_id,
                "question": question_text,
                "choices": {
                    "A": shuffled[0],
                    "B": shuffled[1],
                    "C": shuffled[2],
                    "D": shuffled[3],
                },
                "target_option": ["(A)", "(B)", "(C)", "(D)"][correct_pos],
                "difficulty": difficulty,
                "domain": domain,
            }
        )

    manifest_path.write_text(json.dumps(items, ensure_ascii=False, indent=2))
    return items


def write_jsonl(path: Path, record: Dict[str, object]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_done_keys(path: Path) -> set:
    done = set()
    if not path.exists():
        return done
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                done.add((rec["doc_id"], int(rec["seed"]), rec["method"], int(rec.get("budget_total", -1))))
            except Exception:
                continue
    return done


def _step_role(step: str) -> str:
    if not step:
        return "unknown"
    return step.split(".", 1)[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run GPQA incoherence Round2 experiments")
    parser.add_argument("--config", required=True)
    parser.add_argument("--gpu-shard", required=True, help="Format: i/N, e.g., 0/8")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--max-questions", type=int, default=None, help="Optional debug cap")
    parser.add_argument("--max-trials", type=int, default=None, help="Optional trial seed cap")
    parser.add_argument("--methods", default=None, help="Comma-separated method override")
    parser.add_argument("--budgets", default=None, help="Comma-separated budget override")
    args = parser.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text())
    shard_id, shard_total = parse_gpu_shard(args.gpu_shard)

    hf_token = os.environ.get("HF_TOKEN")
    if hf_token:
        login(token=hf_token, add_to_git_credential=False)

    run_dir = ensure_run_dir(cfg, args.run_id)

    resolved_cfg_path = run_dir / "config_resolved.yaml"
    if not resolved_cfg_path.exists():
        resolved_cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True))

    questions = build_question_pool(cfg, run_dir)
    subset_start = int(cfg["dataset"].get("subset_start", 0))
    subset_end_raw = cfg["dataset"].get("subset_end")
    subset_end = int(subset_end_raw) if subset_end_raw is not None else len(questions)
    subset_start = max(0, subset_start)
    subset_end = min(len(questions), subset_end)
    if subset_start > 0 or subset_end < len(questions):
        questions = [q for q in questions if subset_start <= int(q["manifest_index"]) < subset_end]

    if args.max_questions is not None:
        questions = questions[: int(args.max_questions)]

    sharded_questions = [q for i, q in enumerate(questions) if i % shard_total == shard_id]

    trial_seeds = cfg["evaluation"]["trial_seeds"]
    if args.max_trials is not None:
        trial_seeds = trial_seeds[: int(args.max_trials)]

    methods = cfg["methods"]
    if args.methods:
        methods = [m.strip() for m in args.methods.split(",") if m.strip()]

    budgets = cfg["evaluation"].get("total_token_budgets")
    if budgets is None:
        # Backward compatibility
        budgets = [int(cfg["evaluation"].get("output_token_budget", 768))]
    budgets = [int(b) for b in budgets]
    if args.budgets:
        budgets = [int(x.strip()) for x in args.budgets.split(",") if x.strip()]

    parse_policy = str(cfg["evaluation"].get("parse_policy", "P1"))
    enable_parse_repair = bool(
        cfg["evaluation"].get("enable_parse_repair", str(parse_policy).upper() in {"P1R", "P1_REPAIR", "P1+REPAIR"})
    )
    repair_min_remaining = int(cfg["evaluation"].get("repair_min_remaining_tokens", 24))
    repair_max_new_tokens = int(cfg["evaluation"].get("repair_max_new_tokens", 16))
    repair_temperature = float(cfg["evaluation"].get("repair_temperature", 0.0))
    repair_top_p = float(cfg["evaluation"].get("repair_top_p", 1.0))
    enforce_strict_repair_reserve = bool(cfg["evaluation"].get("enforce_strict_repair_reserve", True))

    expected_total_shard = len(sharded_questions) * len(trial_seeds) * len(methods) * len(budgets)

    results_path = run_dir / f"results_shard{shard_id}.jsonl"
    hotmess_path = run_dir / f"hotmess_shard{shard_id}.jsonl"
    status_path = run_dir / f"status_shard{shard_id}.json"

    done_keys = load_done_keys(results_path)

    gpu_count = torch.cuda.device_count()
    if gpu_count <= 0:
        raise RuntimeError("No CUDA device available")
    gpu_id = shard_id % gpu_count
    device = f"cuda:{gpu_id}"

    print(f"[{now_ts()}] shard={shard_id}/{shard_total} on {device}")

    main_runner = ModelRunner(
        model_id=cfg["models"]["main"],
        device=device,
        use_fast_tokenizer=bool(cfg["runtime"].get("use_fast_tokenizer", False)),
        trust_remote_code=bool(cfg["runtime"].get("trust_remote_code", True)),
        dtype=str(cfg["runtime"].get("dtype", "bfloat16")),
    )
    anchor_required_methods = {"ours_full", "ours_decompose_only", "ours_anchor_only"}
    need_anchor_runner = any(m in anchor_required_methods for m in methods)
    anchor_runner: Optional[ModelRunner] = None
    if need_anchor_runner:
        print(f"[{now_ts()}] loading models main={cfg['models']['main']} anchor={cfg['models']['anchor']}")
        anchor_runner = ModelRunner(
            model_id=cfg["models"]["anchor"],
            device=device,
            use_fast_tokenizer=bool(cfg["runtime"].get("use_fast_tokenizer", False)),
            trust_remote_code=bool(cfg["runtime"].get("trust_remote_code", True)),
            dtype=str(cfg["runtime"].get("dtype", "bfloat16")),
        )
    else:
        print(f"[{now_ts()}] loading model main={cfg['models']['main']} (anchor disabled for this method set)")

    run_meta_path = run_dir / "run_meta.json"
    if not run_meta_path.exists():
        run_meta_path.write_text(
            json.dumps(
                {
                    "created_at": now_ts(),
                    "run_dir": str(run_dir),
                    "dataset_n": len(questions),
                    "shard_total": shard_total,
                    "methods": methods,
                    "trial_seeds": trial_seeds,
                    "budgets": budgets,
                    "budget_metric": "total_tokens",
                    "parse_policy": parse_policy,
                    "enforce_strict_repair_reserve": enforce_strict_repair_reserve,
                    "repair_min_remaining_tokens": repair_min_remaining,
                    "expected_total_global": len(questions) * len(trial_seeds) * len(methods) * len(budgets),
                    "expected_total_per_shard_estimate": expected_total_shard,
                },
                indent=2,
            )
        )

    method_params = cfg["method_params"]

    started = time.time()
    completed = 0
    parse_fail = 0
    parse_repair_attempted = 0
    parse_repair_success = 0
    hard_fail = 0
    parse_fail_types = Counter()

    for q in sharded_questions:
        for s in trial_seeds:
            for budget_limit in budgets:
                for method in methods:
                    key = (q["doc_id"], int(s), method, int(budget_limit))
                    if key in done_keys:
                        continue

                    budget = TokenBudget(total_limit=int(budget_limit))
                    local_errors: List[str] = []

                    def _call(
                        runner: ModelRunner,
                        step: str,
                        prompt: str,
                        requested_new_tokens: int,
                        temperature: float,
                        top_p: float,
                        seed: int,
                        discarded: bool,
                    ) -> str:
                        if not budget.can_generate():
                            return ""

                        rendered = runner.render_prompt(prompt)
                        prompt_tokens = runner.count_rendered_tokens(rendered)
                        reserve = 0
                        if enable_parse_repair and not str(step).startswith("repair.parse"):
                            reserve = max(0, repair_min_remaining)
                        allowed = budget.remaining_total() - int(prompt_tokens) - reserve
                        if (
                            not enforce_strict_repair_reserve
                            and allowed <= 0
                            and enable_parse_repair
                            and not str(step).startswith("repair.parse")
                        ):
                            min_nonrepair_out = int(cfg["evaluation"].get("min_nonrepair_output_tokens", 8))
                            max_reserve = max(0, budget.remaining_total() - int(prompt_tokens) - min_nonrepair_out)
                            reserve = min(reserve, max_reserve)
                            allowed = budget.remaining_total() - int(prompt_tokens) - reserve
                        allowed = max(0, allowed)
                        max_new_tokens = max(0, min(int(requested_new_tokens), allowed))
                        if max_new_tokens <= 0:
                            return ""

                        text, usage = runner.generate_rendered(
                            rendered,
                            max_new_tokens=max_new_tokens,
                            temperature=float(temperature),
                            top_p=float(top_p),
                            seed=int(seed),
                            retries=int(cfg["runtime"].get("max_retries", 2)),
                        )
                        budget.add(
                            step=step,
                            role=_step_role(step),
                            input_tokens=usage["input_tokens"],
                            output_tokens=usage["output_tokens"],
                            discarded=discarded,
                        )
                        return text

                    def call_main(step: str, prompt: str, mx: int, temp: float, top_p: float, seed: int, discarded: bool) -> str:
                        return _call(main_runner, step, prompt, mx, temp, top_p, seed, discarded)

                    def call_anchor(step: str, prompt: str, mx: int, temp: float, top_p: float, seed: int, discarded: bool) -> str:
                        if anchor_runner is None:
                            raise RuntimeError(
                                f"Anchor model call requested by step={step}, but anchor runner is disabled for methods={methods}"
                            )
                        return _call(anchor_runner, step, prompt, mx, temp, top_p, seed, discarded)

                    try:
                        method_cfg = dict(method_params[method])
                        method_cfg["_budget_total"] = int(budget_limit)
                        out = run_method(
                            method_name=method,
                            sample=q,
                            params=method_cfg,
                            trial_seed=int(s) + q["manifest_index"] * 10000 + int(budget_limit),
                            call_main=call_main,
                            call_anchor=call_anchor,
                        )
                    except Exception as err:
                        hard_fail += 1
                        local_errors.append(str(err))
                        out = {
                            "response_text": "",
                            "pred_option": None,
                            "intermediate_answers": [],
                            "restart_count": 0,
                            "anchor_constraints": None,
                            "controller_trace": None,
                        }

                    raw_response_text = str(out.get("response_text", ""))
                    terminal_path = str((out.get("controller_trace") or {}).get("decision", "method_terminal"))
                    remaining_budget_before_finalize = int(budget.remaining_total())
                    formatter_option_initial = extract_last_option_anywhere(raw_response_text)
                    response_text = (
                        _format_final_answer_text(formatter_option_initial) if formatter_option_initial else raw_response_text
                    )
                    formatter_applied_initial = formatter_option_initial is not None
                    parsed_option, parse_fail_type, parse_info = classify_parse_result(response_text)
                    parse_info = {
                        "initial": parse_info,
                        "formatter_option_initial": formatter_option_initial,
                        "formatter_applied_initial": formatter_applied_initial,
                    }
                    parse_fail_type_initial = parse_fail_type
                    repair_response_text = None
                    parse_repair_used = False
                    remaining_budget_before_repair = None
                    pred_option = parsed_option
                    parse_fail_reason = "OK" if parse_fail_type is None else "initial_parse_fail"

                    if parse_fail_type is not None:
                        if not enable_parse_repair:
                            parse_fail_reason = "repair_disabled"
                        elif budget.remaining_total() < repair_min_remaining:
                            parse_fail_reason = "no_budget_for_repair"
                        else:
                            parse_repair_attempted += 1
                            parse_repair_used = True
                            remaining_for_repair = budget.remaining_total()
                            remaining_budget_before_repair = int(remaining_for_repair)
                            if remaining_for_repair < 96:
                                repair_prompt = (
                                    "Output exactly one uppercase letter: A or B or C or D.\n"
                                    "No other text."
                                )
                            else:
                                repair_prompt = (
                                    "Read candidate response. Output exactly one uppercase letter: A or B or C or D.\n"
                                    "No other text.\n\n"
                                    "Candidate:\n"
                                    f"{response_text[:512]}\n"
                                )
                            repair_response_text = call_main(
                                "repair.parse",
                                repair_prompt,
                                repair_max_new_tokens,
                                repair_temperature,
                                repair_top_p,
                                int(s) + q["manifest_index"] * 100000 + int(budget_limit) + 9091,
                                False,
                            )
                            rep_fmt_opt = extract_last_option_anywhere(repair_response_text)
                            if rep_fmt_opt is not None:
                                rep_opt = rep_fmt_opt
                                rep_fail = None
                                rep_info = {
                                    "repair_formatter_option": rep_fmt_opt,
                                    "repair_formatter_applied": True,
                                }
                                response_text = _format_final_answer_text(rep_fmt_opt)
                            else:
                                rep_opt, rep_fail, rep_info = classify_parse_result(repair_response_text)
                            parse_info = {**parse_info, "repair": rep_info}
                            if rep_fail is None and rep_opt is not None:
                                pred_option = rep_opt
                                parse_fail_type = None
                                parse_repair_success += 1
                                parse_fail_reason = "repaired_success"
                            else:
                                parse_fail_type = rep_fail
                                parse_fail_reason = "repair_called_but_failed"

                    if parse_fail_type is not None and parse_fail_reason in {"OK", "initial_parse_fail"}:
                        if parse_fail_type == PARSE_FAIL_NO_ANSWER and not str(response_text).strip():
                            parse_fail_reason = "no_answer_token"
                        elif parse_fail_type == PARSE_FAIL_MULTI_ANSWER:
                            parse_fail_reason = "multi_answer_unresolved"
                        elif parse_fail_type == PARSE_FAIL_INVALID:
                            parse_fail_reason = "invalid_format_unresolved"
                        else:
                            parse_fail_reason = f"unresolved_{str(parse_fail_type).lower()}"

                    if parse_fail_type is not None:
                        parse_fail += 1
                        parse_fail_types[parse_fail_type] += 1
                        if parse_policy == "P1":
                            pred_option = None

                    pred_idx = option_to_index(pred_option)
                    target_idx = option_to_index(q["target_option"])
                    is_correct = (pred_idx is not None) and (target_idx is not None) and (pred_idx == target_idx)

                    stage_spend = budget.stage_spend()
                    result_rec = {
                        "ts": now_ts(),
                        "doc_id": q["doc_id"],
                        "method": method,
                        "seed": int(s),
                        "budget_total": int(budget_limit),
                        "budget_metric": "total_tokens",
                        "dataset_index": q["dataset_index"],
                        "manifest_index": q["manifest_index"],
                        "target_option": q["target_option"],
                        "pred_option": pred_option,
                        "is_correct": bool(is_correct),
                        "response_text": response_text,
                        "raw_response_text": raw_response_text,
                        "terminal_path": terminal_path,
                        "response_text_formatter_applied": formatter_applied_initial,
                        "response_text_formatter_option": formatter_option_initial,
                        "final_formatter_applied": formatter_applied_initial,
                        "usage": budget.usage_dict(),
                        "budget_spent": int(budget.total_spent),
                        "budget_limit": int(budget.total_limit),
                        "stopped_by_budget": budget.remaining_total() == 0,
                        "remaining_budget_before_finalize": remaining_budget_before_finalize,
                        "remaining_budget_before_repair": remaining_budget_before_repair,
                        "num_calls": len(budget.events),
                        "stage_token_spend": stage_spend,
                        "restart_count": int(out.get("restart_count", 0)),
                        "intermediate_answers": out.get("intermediate_answers", []),
                        "intermediate_flip_count": count_flips(out.get("intermediate_answers", [])),
                        "anchor_constraints": out.get("anchor_constraints"),
                        "controller_trace": out.get("controller_trace"),
                        "parse_policy": parse_policy,
                        "parse_repair_used": parse_repair_used,
                        "parse_fail_type_initial": parse_fail_type_initial,
                        "repair_response_text": repair_response_text,
                        "parse_fail_type": parse_fail_type,
                        "parse_fail_reason": parse_fail_reason,
                        "strict_repair_reserve_enforced": enforce_strict_repair_reserve,
                        "parse_info": parse_info,
                        "token_events": budget.to_dict()["events"],
                        "errors": local_errors,
                    }
                    write_jsonl(results_path, result_rec)

                    hotmess_rec = {
                        "doc_id": q["doc_id"],
                        "filter": "get-answer",
                        "resps": [[response_text]],
                        "target": q["target_option"],
                        "response_length": int(budget.output_spent),
                        "usage": {
                            "output_tokens": int(budget.output_spent),
                            "input_tokens": int(budget.input_spent),
                            "total_tokens": int(budget.total_spent),
                        },
                        "method": method,
                        "seed": int(s),
                        "budget_total": int(budget_limit),
                    }
                    write_jsonl(hotmess_path, hotmess_rec)

                    completed += 1
                    elapsed = max(time.time() - started, 1e-6)
                    rate = completed / elapsed
                    eta = (expected_total_shard - completed) / rate if rate > 0 else None

                    status = {
                        "ts": now_ts(),
                        "shard": f"{shard_id}/{shard_total}",
                        "device": device,
                        "completed": completed,
                        "expected_total_shard": expected_total_shard,
                        "parse_fail": parse_fail,
                        "parse_fail_rate": parse_fail / completed if completed else 0.0,
                        "parse_repair_attempted": parse_repair_attempted,
                        "parse_repair_success": parse_repair_success,
                        "parse_fail_types": dict(parse_fail_types),
                        "hard_fail": hard_fail,
                        "rate_items_per_sec": rate,
                        "eta_seconds": eta,
                        "current": {"doc_id": q["doc_id"], "seed": s, "budget_total": budget_limit, "method": method},
                    }
                    status_path.write_text(json.dumps(status, indent=2))

                    if completed % 20 == 0:
                        print(
                            f"[{now_ts()}] shard {shard_id}: {completed}/{expected_total_shard} "
                            f"parse_fail={status['parse_fail_rate']:.3f} eta={int(eta) if eta else 'na'}s"
                        )

    done = {
        "ts": now_ts(),
        "done": True,
        "completed": completed,
        "expected_total_shard": expected_total_shard,
        "parse_fail": parse_fail,
        "parse_fail_rate": parse_fail / completed if completed else 0.0,
        "parse_repair_attempted": parse_repair_attempted,
        "parse_repair_success": parse_repair_success,
        "parse_fail_types": dict(parse_fail_types),
        "hard_fail": hard_fail,
    }
    status_path.write_text(json.dumps(done, indent=2))
    print(f"[{now_ts()}] shard {shard_id} finished: {completed} records")


if __name__ == "__main__":
    main()
