from __future__ import annotations

import hashlib
from collections import Counter
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

from .parser import extract_confidence, extract_final_option


@dataclass
class Attempt:
    step: str
    text: str
    option: Optional[str]
    confidence: Optional[float]


GenerateFn = Callable[[str, str, int, float, float, int, bool], str]


def _mcq_block(sample: Dict[str, object]) -> str:
    return (
        f"Question:\n{sample['question']}\n\n"
        f"Choices:\n"
        f"(A) {sample['choices']['A']}\n"
        f"(B) {sample['choices']['B']}\n"
        f"(C) {sample['choices']['C']}\n"
        f"(D) {sample['choices']['D']}\n"
    )


def _option_letter(option: Optional[str]) -> Optional[str]:
    if option is None:
        return None
    raw = str(option).strip()
    if raw.startswith("(") and raw.endswith(")") and len(raw) >= 3:
        return raw[1].upper()
    if raw and raw[0].upper() in {"A", "B", "C", "D"}:
        return raw[0].upper()
    return None


def _format_final_answer(option: Optional[str], confidence: Optional[float] = None) -> str:
    letter = _option_letter(option) or "A"
    if confidence is None:
        confidence = 0.5
    confidence = max(0.0, min(1.0, float(confidence)))
    return f"Final Answer: {letter}\nConfidence: {confidence:.2f}\n"


def _attempt(
    call_main: GenerateFn,
    step: str,
    prompt: str,
    max_new_tokens: int,
    temperature: float,
    top_p: float,
    seed: int,
    discarded: bool = False,
) -> Attempt:
    text = call_main(step, prompt, max_new_tokens, temperature, top_p, seed, discarded)
    return Attempt(
        step=step,
        text=text,
        option=extract_final_option(text),
        confidence=extract_confidence(text),
    )


def _majority_vote(options: List[Optional[str]]) -> Tuple[Optional[str], float]:
    valid = [o for o in options if o is not None]
    if not valid:
        return None, 0.0
    counts = Counter(valid)
    voted, voted_count = sorted(counts.items(), key=lambda x: (-x[1], x[0]))[0]
    return voted, voted_count / len(valid)


def _pick_by_option_and_conf(attempts: List[Attempt], option: Optional[str]) -> Optional[Attempt]:
    if not attempts:
        return None
    if option is None:
        return attempts[0]
    candidates = [a for a in attempts if a.option == option]
    if not candidates:
        return attempts[0]

    def score(a: Attempt) -> float:
        return a.confidence if a.confidence is not None else -1.0

    return sorted(candidates, key=score, reverse=True)[0]


def _base_return(
    final_attempt: Optional[Attempt],
    attempts: List[Attempt],
    restart_count: int,
    anchor_constraints: Optional[str],
    controller_trace: Optional[Dict[str, object]] = None,
) -> Dict[str, object]:
    final_attempt = final_attempt or (attempts[-1] if attempts else None)
    final_text = final_attempt.text if final_attempt else ""
    final_option = final_attempt.option if final_attempt else None
    return {
        "response_text": final_text,
        "pred_option": final_option,
        "intermediate_answers": [a.option for a in attempts if a.option],
        "restart_count": restart_count,
        "anchor_constraints": anchor_constraints,
        "controller_trace": controller_trace,
    }


def run_baseline_longcot(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    prompt = (
        "Solve the multiple-choice question and keep the answer format strict.\n"
        "Output format (exact):\n"
        "Final Answer: A|B|C|D\n"
        "Confidence: <0 to 1>\n\n"
        "Reasoning: <brief>\n\n"
        + _mcq_block(sample)
    )
    a = _attempt(
        call_main,
        "solve.baseline",
        prompt,
        int(params["max_new_tokens"]),
        float(params["temperature"]),
        float(params["top_p"]),
        trial_seed,
    )
    return _base_return(a, [a], restart_count=0, anchor_constraints=None)


def run_hard_cap(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    max_new_tokens = int(params.get("max_new_tokens", 96))
    budget_total = params.get("_budget_total")
    by_budget = params.get("max_new_tokens_by_budget")
    if isinstance(by_budget, dict) and budget_total is not None:
        bt = str(int(budget_total))
        if bt in by_budget:
            max_new_tokens = int(by_budget[bt])
        elif int(budget_total) in by_budget:  # defensive: int-keyed YAML maps
            max_new_tokens = int(by_budget[int(budget_total)])
    prompt = (
        "Line 1 must be exactly: Final Answer: A|B|C|D\n"
        "Line 2: optional short rationale.\n"
        + _mcq_block(sample)
    )
    a = _attempt(
        call_main,
        "solve.hardcap",
        prompt,
        max_new_tokens,
        float(params["temperature"]),
        float(params["top_p"]),
        trial_seed,
    )
    return _base_return(a, [a], restart_count=0, anchor_constraints=None)


def run_self_consistency(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    n_samples = int(params["n_samples"])
    attempts: List[Attempt] = []
    for i in range(n_samples):
        prompt = (
            "Independent MCQ attempt in at most 3 lines.\n"
            "Output format:\n"
            "Final Answer: A|B|C|D\n"
            "Confidence: <0 to 1>\n"
            "Rationale: <one sentence>\n\n"
            + _mcq_block(sample)
        )
        a = _attempt(
            call_main,
            f"sample.self_consistency.{i}",
            prompt,
            int(params["per_sample_max_new_tokens"]),
            float(params["temperature"]),
            float(params["top_p"]),
            trial_seed + i * 101,
            discarded=True,
        )
        attempts.append(a)

    voted, agreement = _majority_vote([a.option for a in attempts])
    chosen = _pick_by_option_and_conf(attempts, voted)
    out = _base_return(chosen, attempts, restart_count=0, anchor_constraints=None)
    out["controller_trace"] = {
        "n_probe": n_samples,
        "agreement": agreement,
        "decision": "majority_select",
    }
    return out


def run_confidence_select(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    n_samples = int(params["n_samples"])
    attempts: List[Attempt] = []
    for i in range(n_samples):
        prompt = (
            "Solve the MCQ in at most 3 lines.\n"
            "Output format:\n"
            "Final Answer: A|B|C|D\n"
            "Confidence: <0 to 1>\n\n"
            + _mcq_block(sample)
        )
        a = _attempt(
            call_main,
            f"sample.confidence.{i}",
            prompt,
            int(params["per_sample_max_new_tokens"]),
            float(params["temperature"]),
            float(params["top_p"]),
            trial_seed + i * 131,
            discarded=True,
        )
        attempts.append(a)

    scored = [a for a in attempts if a.option is not None]
    if scored:
        chosen = sorted(scored, key=lambda x: x.confidence if x.confidence is not None else -1.0, reverse=True)[0]
    else:
        fallback_prompt = (
            "Give only a final answer in strict format.\n"
            "Output format:\n"
            "Final Answer: A|B|C|D\n"
            "Confidence: <0 to 1>\n\n"
            + _mcq_block(sample)
        )
        fallback = _attempt(
            call_main,
            "fallback.confidence",
            fallback_prompt,
            int(params.get("fallback_max_new_tokens", 96)),
            float(params["temperature"]),
            float(params["top_p"]),
            trial_seed + 1901,
        )
        attempts.append(fallback)
        chosen = fallback

    out = _base_return(chosen, attempts, restart_count=0, anchor_constraints=None)
    out["controller_trace"] = {
        "n_probe": n_samples,
        "agreement": _majority_vote([a.option for a in attempts])[1],
        "decision": "confidence_select",
    }
    return out


def run_ours_controller(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    budget_total = int(params.get("_budget_total", 10**9))
    n_probe = int(params.get("n_probe", 4))
    if budget_total < int(params.get("min_budget_for_four_probe", 512)):
        n_probe = min(n_probe, 2)
    threshold = float(params["stop_conf_threshold"])
    max_restart = int(params.get("max_restart", 1))
    solve_cap = min(int(params["solve_max_new_tokens"]), max(32, int(0.60 * budget_total)))
    restart_cap = min(int(params["restart_max_new_tokens"]), max(24, int(0.30 * budget_total)))

    attempts: List[Attempt] = []
    for i in range(n_probe):
        probe_prompt = (
            "Quick probe only.\n"
            "Output format:\n"
            "Tentative Answer: A|B|C|D\n"
            "Confidence: <0 to 1>\n\n"
            + _mcq_block(sample)
        )
        a = _attempt(
            call_main,
            f"probe.controller.{i}",
            probe_prompt,
            int(params["probe_max_new_tokens"]),
            float(params["temperature"]),
            float(params["top_p"]),
            trial_seed + i * 17,
            discarded=True,
        )
        attempts.append(a)

    voted, agreement = _majority_vote([a.option for a in attempts])
    decision = "stop" if (voted is not None and agreement >= threshold) else "continue"

    restart_count = 0
    if decision == "stop":
        chosen = _pick_by_option_and_conf(attempts, voted)
        return _base_return(
            chosen,
            attempts,
            restart_count,
            anchor_constraints=None,
            controller_trace={
                "probe_used": True,
                "n_probe": n_probe,
                "agreement": agreement,
                "decision": decision,
                "restarts": restart_count,
                "voted_option": voted,
            },
        )

    solve_prompt = (
        "Solve carefully with one-pass verification in concise format.\n"
        "Output format:\n"
        "Final Answer: A|B|C|D\n"
        "Confidence: <0 to 1>\n\n"
        "Reasoning: <brief>\n\n"
        + _mcq_block(sample)
    )
    solve = _attempt(
        call_main,
        "solve.controller",
        solve_prompt,
        solve_cap,
        float(params["temperature"]),
        float(params["top_p"]),
        trial_seed + 701,
    )
    attempts.append(solve)
    final = solve

    while final.option is None and restart_count < max_restart:
        restart_prompt = (
            "Independent restart. Ignore prior chain.\n"
            "Output format:\n"
            "Final Answer: A|B|C|D\n"
            "Confidence: <0 to 1>\n\n"
            + _mcq_block(sample)
        )
        rs = _attempt(
            call_main,
            f"restart.controller.{restart_count}",
            restart_prompt,
            restart_cap,
            float(params["temperature"]),
            float(params["top_p"]),
            trial_seed + 1701 + restart_count * 31,
        )
        attempts.append(rs)
        restart_count += 1
        final = rs

    return _base_return(
        final,
        attempts,
        restart_count,
        anchor_constraints=None,
        controller_trace={
            "probe_used": True,
            "n_probe": n_probe,
            "agreement": agreement,
            "decision": decision,
            "restarts": restart_count,
            "voted_option": voted,
        },
    )


def run_budgeted_self_consistency(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    attempts: List[Attempt] = []
    max_rounds = int(params.get("max_rounds", 12))
    early_stop = bool(params.get("early_majority_stop", False))
    early_min_votes = int(params.get("early_min_votes", 4))
    early_agree = float(params.get("early_agree_threshold", 0.8))

    for i in range(max_rounds):
        prompt = (
            "Independent attempt under fixed compute budget.\n"
            "Output format:\n"
            "Final Answer: A|B|C|D\n"
            "Confidence: <0 to 1>\n"
            "Rationale: <one sentence>\n\n"
            + _mcq_block(sample)
        )
        a = _attempt(
            call_main,
            f"sample.budgeted_sc.{i}",
            prompt,
            int(params["per_sample_max_new_tokens"]),
            float(params["temperature"]),
            float(params["top_p"]),
            trial_seed + i * 97,
            discarded=True,
        )
        if not a.text.strip():
            break
        attempts.append(a)

        if early_stop:
            voted, agreement = _majority_vote([x.option for x in attempts])
            valid_votes = len([x for x in attempts if x.option is not None])
            if voted is not None and valid_votes >= early_min_votes and agreement >= early_agree:
                break

    if not attempts:
        fallback_prompt = (
            "Give one direct answer in strict format.\n"
            "Final Answer: A|B|C|D\n"
            "Confidence: <0 to 1>\n\n"
            + _mcq_block(sample)
        )
        fb = _attempt(
            call_main,
            "fallback.budgeted_sc",
            fallback_prompt,
            int(params.get("fallback_max_new_tokens", 96)),
            float(params["temperature"]),
            float(params["top_p"]),
            trial_seed + 19001,
        )
        attempts.append(fb)

    voted, agreement = _majority_vote([a.option for a in attempts])
    chosen = _pick_by_option_and_conf(attempts, voted)
    out = _base_return(chosen, attempts, restart_count=0, anchor_constraints=None)
    out["controller_trace"] = {
        "decision": "budgeted_self_consistency",
        "n_generated": len(attempts),
        "agreement": agreement,
        "voted_option": voted,
    }
    return out


def run_probe_only_fixedk(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    attempts: List[Attempt] = []
    n_probe = int(params.get("n_probe", 4))
    per_probe_cap = int(params.get("per_probe_max_new_tokens", 64))
    temperature = float(params["temperature"])
    top_p = float(params["top_p"])

    for i in range(n_probe):
        prompt = (
            "Line 1 must be exactly: Tentative Answer: A|B|C|D\n"
            "Line 2: optional confidence in [0,1].\n"
            + _mcq_block(sample)
        )
        a = _attempt(
            call_main,
            f"probe_only.fixedk.{i}",
            prompt,
            per_probe_cap,
            temperature,
            top_p,
            trial_seed + i * 97,
            discarded=True,
        )
        if not a.text.strip():
            break
        attempts.append(a)

    voted, agreement = _majority_vote([a.option for a in attempts])
    chosen = _pick_by_option_and_conf(attempts, voted)

    if voted is None:
        fallback_prompt = (
            "Line 1 must be exactly: Final Answer: A|B|C|D\n"
            + _mcq_block(sample)
        )
        fb = _attempt(
            call_main,
            "fallback.probe_only",
            fallback_prompt,
            int(params.get("fallback_max_new_tokens", 64)),
            temperature,
            top_p,
            trial_seed + 19001,
        )
        attempts.append(fb)
        return _base_return(
            fb,
            attempts,
            restart_count=0,
            anchor_constraints=None,
            controller_trace={
                "decision": "probe_only_fallback",
                "n_probe": len([a for a in attempts if a.step.startswith("probe_only")]),
                "agreement": 0.0,
                "voted_option": None,
            },
        )

    final_attempt = Attempt(
        step="final.probe_only",
        text=_format_final_answer(voted, chosen.confidence if chosen else None),
        option=voted,
        confidence=chosen.confidence if chosen else None,
    )
    out = _base_return(final_attempt, attempts, restart_count=0, anchor_constraints=None)
    out["controller_trace"] = {
        "decision": "probe_only_stop",
        "n_probe": len(attempts),
        "agreement": agreement,
        "voted_option": voted,
    }
    return out


def run_probe_adaptive_k(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    attempts: List[Attempt] = []
    temperature = float(params["temperature"])
    top_p = float(params["top_p"])
    initial_k = int(params.get("initial_k", 2))
    step_k = int(params.get("step_k", 2))
    k_max = int(params.get("k_max", 10))
    per_probe_cap = int(params.get("per_probe_max_new_tokens", 48))
    agree_thresh = float(params.get("agreement_threshold", 0.75))

    generated = 0
    batch = max(1, initial_k)
    voted = None
    agreement = 0.0

    while generated < k_max:
        generated_before = generated
        n_to_add = min(batch, k_max - generated)
        for j in range(n_to_add):
            i = generated + j
            prompt = (
                "Line 1 must be exactly: Tentative Answer: A|B|C|D\n"
                "Line 2: optional confidence in [0,1].\n"
                + _mcq_block(sample)
            )
            a = _attempt(
                call_main,
                f"probe_adaptive.{i}",
                prompt,
                per_probe_cap,
                temperature,
                top_p,
                trial_seed + i * 97,
                discarded=True,
            )
            if not a.text.strip():
                break
            attempts.append(a)
        generated = len(attempts)
        # If no probe text was produced in this round, stop to avoid infinite loop.
        if generated == generated_before:
            break

        voted, agreement = _majority_vote([a.option for a in attempts])
        if voted is not None and agreement >= agree_thresh:
            break
        batch = max(1, step_k)

    if voted is None:
        fallback_prompt = (
            "Line 1 must be exactly: Final Answer: A|B|C|D\n"
            + _mcq_block(sample)
        )
        fb = _attempt(
            call_main,
            "fallback.probe_adaptive",
            fallback_prompt,
            int(params.get("fallback_max_new_tokens", 64)),
            temperature,
            top_p,
            trial_seed + 20001,
        )
        attempts.append(fb)
        return _base_return(
            fb,
            attempts,
            restart_count=0,
            anchor_constraints=None,
            controller_trace={
                "decision": "probe_adaptive_fallback",
                "n_probe": len([a for a in attempts if a.step.startswith("probe_adaptive.")]),
                "agreement": 0.0,
                "voted_option": None,
            },
        )

    # Optional single solve only for very low agreement cases.
    low_agree_thr = params.get("low_agreement_solve_threshold")
    if low_agree_thr is not None and agreement <= float(low_agree_thr):
        solve = _attempt(
            call_main,
            "solve.probe_adaptive_lowagree",
            (
                "Line 1 must be exactly: Final Answer: A|B|C|D\n"
                "Then one short rationale line.\n"
                + _mcq_block(sample)
            ),
            int(params.get("low_agreement_solve_max_new_tokens", 96)),
            temperature,
            top_p,
            trial_seed + 20041,
        )
        attempts.append(solve)
        if solve.option is not None:
            final_attempt = Attempt(
                step="final.probe_adaptive_lowagree",
                text=_format_final_answer(solve.option, solve.confidence),
                option=solve.option,
                confidence=solve.confidence,
            )
            out = _base_return(final_attempt, attempts, restart_count=0, anchor_constraints=None)
            out["controller_trace"] = {
                "decision": "probe_adaptive_lowagree_solve",
                "n_probe": len([a for a in attempts if a.step.startswith("probe_adaptive.")]),
                "agreement": agreement,
                "voted_option": voted,
            }
            return out

    chosen = _pick_by_option_and_conf(attempts, voted)
    final_attempt = Attempt(
        step="final.probe_adaptive",
        text=_format_final_answer(voted, chosen.confidence if chosen else None),
        option=voted,
        confidence=chosen.confidence if chosen else None,
    )
    out = _base_return(final_attempt, attempts, restart_count=0, anchor_constraints=None)
    out["controller_trace"] = {
        "decision": "probe_adaptive_stop",
        "n_probe": len([a for a in attempts if a.step.startswith("probe_adaptive.")]),
        "agreement": agreement,
        "voted_option": voted,
        "k_max": k_max,
        "agreement_threshold": agree_thresh,
    }
    return out


def run_forced_deliberation(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    attempts: List[Attempt] = []

    init_prompt = (
        "Solve the MCQ and return strict output.\n"
        "Output format:\n"
        "Final Answer: A|B|C|D\n"
        "Confidence: <0 to 1>\n"
        "Reasoning: <brief>\n\n"
        + _mcq_block(sample)
    )
    cur = _attempt(
        call_main,
        "force.solve.0",
        init_prompt,
        int(params.get("initial_max_new_tokens", params.get("per_cycle_max_new_tokens", 128))),
        float(params["temperature"]),
        float(params["top_p"]),
        trial_seed + 2101,
    )
    attempts.append(cur)
    final = cur

    max_rounds = int(params.get("max_rounds", 4))
    for r in range(1, max_rounds + 1):
        prev = final.text[: int(params.get("carry_prev_chars", 400))]
        round_prompt = (
            f"Deliberation round {r}. Re-check the prior answer and explicitly reconsider alternatives.\n"
            "If unchanged, repeat the same final answer; if changed, provide revised final answer.\n"
            "Output format:\n"
            "Final Answer: A|B|C|D\n"
            "Confidence: <0 to 1>\n"
            "Reasoning: <brief>\n\n"
            f"Previous candidate:\n{prev}\n\n"
            + _mcq_block(sample)
        )
        nxt = _attempt(
            call_main,
            f"force.round.{r}",
            round_prompt,
            int(params.get("per_cycle_max_new_tokens", 128)),
            float(params["temperature"]),
            float(params["top_p"]),
            trial_seed + 2101 + r * 29,
            discarded=True,
        )
        if not nxt.text.strip():
            break
        attempts.append(nxt)
        if nxt.option is not None:
            final = nxt

    out = _base_return(final, attempts, restart_count=0, anchor_constraints=None)
    out["controller_trace"] = {
        "decision": "forced_deliberation",
        "rounds_executed": len(attempts),
    }
    return out


def run_ours_controller_v2(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    budget_total = int(params.get("_budget_total", 10**9))
    temperature = float(params["temperature"])
    top_p = float(params["top_p"])

    # Low-budget fallback to avoid controller overhead dominating solve tokens.
    low_budget_threshold = int(params.get("low_budget_threshold", 1024))
    if bool(params.get("enable_low_budget_fallback", True)) and budget_total <= low_budget_threshold:
        fallback_params = {
            "max_new_tokens": int(params.get("fallback_hard_cap_tokens", 96)),
            "temperature": temperature,
            "top_p": top_p,
        }
        # Keep exact equivalence with hard_cap path when fallback triggers.
        out = run_hard_cap(sample, fallback_params, trial_seed, call_main)
        out["controller_trace"] = {
            "decision": "fallback_hard_cap",
            "budget_total": budget_total,
            "low_budget_threshold": low_budget_threshold,
        }
        return out

    solve_min_target = max(int(params.get("solve_min_floor", 256)), int(float(params.get("solve_min_ratio", 0.6)) * budget_total))
    probe_budget_cap = int(params.get("probe_budget_cap", 128))
    probe_budget_ratio = float(params.get("probe_budget_ratio", 0.15))
    probe_budget_target = min(max(0, budget_total - solve_min_target), min(probe_budget_cap, int(probe_budget_ratio * budget_total)))

    n_probe_first = int(params.get("n_probe_first", 2))
    n_probe_second = int(params.get("n_probe_second", 2))
    max_probe_n = int(params.get("n_probe", 4))
    min_probe_budget_tokens = int(params.get("min_probe_budget_tokens", 48))

    n_probe_plan = min(max_probe_n, n_probe_first + n_probe_second)
    if probe_budget_target < min_probe_budget_tokens:
        n_probe_plan = 0
    per_probe_cap = int(params.get("probe_max_new_tokens", 64))
    if n_probe_plan > 0:
        per_probe_cap = max(16, min(per_probe_cap, max(16, probe_budget_target // n_probe_plan)))

    attempts: List[Attempt] = []
    for i in range(n_probe_first if n_probe_plan > 0 else 0):
        probe_prompt = (
            "Line 1 must be exactly: Tentative Answer: A|B|C|D\n"
            "Line 2: optional confidence in [0,1].\n"
            + _mcq_block(sample)
        )
        a = _attempt(
            call_main,
            f"probe_v2.first.{i}",
            probe_prompt,
            per_probe_cap,
            temperature,
            top_p,
            trial_seed + 50001 + i * 11,
            discarded=True,
        )
        if not a.text.strip():
            break
        attempts.append(a)

    voted, agreement = _majority_vote([a.option for a in attempts])
    agree_thresh = float(params.get("stop_conf_threshold", 0.67))

    # Progressive probing: add more probes only when disagreement persists.
    if len(attempts) > 0 and agreement < agree_thresh and n_probe_plan > n_probe_first:
        for j in range(n_probe_second):
            idx = n_probe_first + j
            probe_prompt = (
                "Line 1 must be exactly: Tentative Answer: A|B|C|D\n"
                "Line 2: optional confidence in [0,1].\n"
                + _mcq_block(sample)
            )
            a = _attempt(
                call_main,
                f"probe_v2.second.{j}",
                probe_prompt,
                per_probe_cap,
                temperature,
                top_p,
                trial_seed + 51001 + idx * 13,
                discarded=True,
            )
            if not a.text.strip():
                break
            attempts.append(a)
        voted, agreement = _majority_vote([a.option for a in attempts])

    disagreement = 1.0 - agreement
    force_continue = False
    force_reason = None

    force_continue_thr = params.get("force_continue_disagreement_threshold")
    if force_continue_thr is not None and disagreement >= float(force_continue_thr):
        force_continue = True
        force_reason = "force_continue_disagreement_threshold"

    stop_cap_rate = params.get("stop_after_probe_cap_rate")
    stop_cap_disagree_thr = float(params.get("stop_cap_disagreement_threshold", 1.0))
    if stop_cap_rate is not None and voted is not None and agreement >= agree_thresh:
        if disagreement >= stop_cap_disagree_thr:
            force_continue = True
            force_reason = "stop_cap_disagreement_threshold"
        else:
            key = f"{sample.get('doc_id', sample.get('question', ''))}|{trial_seed}|{budget_total}"
            h = hashlib.sha256(key.encode("utf-8")).hexdigest()
            u = int(h[:8], 16) / float(0xFFFFFFFF)
            if u > float(stop_cap_rate):
                force_continue = True
                force_reason = "stop_after_probe_cap_rate"

    if voted is not None and agreement >= agree_thresh and not force_continue:
        chosen = _pick_by_option_and_conf(attempts, voted)
        final_attempt = Attempt(
            step="final.controller_v2",
            text=_format_final_answer(voted, chosen.confidence if chosen else None),
            option=voted,
            confidence=chosen.confidence if chosen else None,
        )
        return _base_return(
            final_attempt,
            attempts,
            restart_count=0,
            anchor_constraints=None,
            controller_trace={
                "decision": "stop_after_probe",
                "decision_trace": "probe->stop",
                "budget_total": budget_total,
                "solve_min_target": solve_min_target,
                "probe_budget_target": probe_budget_target,
                "n_probe": len(attempts),
                "agreement": agreement,
                "disagreement": disagreement,
                "voted_option": voted,
                "forced_continue": False,
            },
        )

    solve_cap = min(int(params.get("solve_max_new_tokens", 256)), max(int(params.get("solve_min_floor", 256)), int(0.7 * budget_total)))
    solve_prompt = (
        "Line 1 must be exactly: Final Answer: A|B|C|D\n"
        "Line 2: optional one-sentence rationale.\n"
        + _mcq_block(sample)
    )
    solve = _attempt(
        call_main,
        "solve.controller_v2",
        solve_prompt,
        solve_cap,
        temperature,
        top_p,
        trial_seed + 52001,
    )
    attempts.append(solve)
    final = solve

    restart_count = 0
    max_restart = int(params.get("max_restart", 1))
    restart_cap = min(int(params.get("restart_max_new_tokens", 160)), max(32, int(0.25 * budget_total)))
    while final.option is None and restart_count < max_restart:
        rp = (
            "Line 1 must be exactly: Final Answer: A|B|C|D\n"
            + _mcq_block(sample)
        )
        rs = _attempt(
            call_main,
            f"restart.controller_v2.{restart_count}",
            rp,
            restart_cap,
            temperature,
            top_p,
            trial_seed + 53001 + restart_count * 31,
        )
        attempts.append(rs)
        final = rs
        restart_count += 1

    return _base_return(
        final,
        attempts,
        restart_count=restart_count,
        anchor_constraints=None,
        controller_trace={
            "decision": "continue_solve",
            "budget_total": budget_total,
            "solve_min_target": solve_min_target,
            "probe_budget_target": probe_budget_target,
            "n_probe": len([a for a in attempts if a.step.startswith("probe_v2")]),
            "agreement": agreement,
            "disagreement": disagreement,
            "voted_option": voted,
            "restarts": restart_count,
            "forced_continue": force_continue,
            "force_reason": force_reason,
        },
    )


def run_ours_controller_v3(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    # Budget-aware controller tuned for low-budget robustness.
    budget_total = int(params.get("_budget_total", 10**9))
    temperature = float(params["temperature"])
    top_p = float(params["top_p"])

    low_budget_threshold = int(params.get("low_budget_threshold", 900))
    if bool(params.get("enable_low_budget_fallback", True)) and budget_total <= low_budget_threshold:
        fallback_params = {
            "max_new_tokens": int(params.get("fallback_hard_cap_tokens", 80)),
            "temperature": temperature,
            "top_p": top_p,
        }
        # Keep exact equivalence with hard_cap path when fallback triggers.
        out = run_hard_cap(sample, fallback_params, trial_seed, call_main)
        out["controller_trace"] = {
            "decision": "fallback_hard_cap",
            "budget_total": budget_total,
            "low_budget_threshold": low_budget_threshold,
            "decision_trace": "fallback_hard_cap",
            "fallback_used": True,
        }
        return out

    # Hard reservation for solve budget.
    solve_min_target = max(int(params.get("solve_min_floor", 256)), int(float(params.get("solve_min_ratio", 0.70)) * budget_total))
    probe_budget_cap = int(params.get("probe_budget_cap", 96))
    probe_budget_ratio = float(params.get("probe_budget_ratio", 0.10))
    probe_budget_target = min(max(0, budget_total - solve_min_target), min(probe_budget_cap, int(probe_budget_ratio * budget_total)))
    min_probe_budget_tokens = int(params.get("min_probe_budget_tokens", 48))
    if probe_budget_target < min_probe_budget_tokens:
        probe_budget_target = 0

    n_probe_first = int(params.get("n_probe_first", 2))
    n_probe_second = int(params.get("n_probe_second", 2))
    max_probe_n = int(params.get("n_probe", 4))

    n_probe_plan = min(max_probe_n, n_probe_first + n_probe_second) if probe_budget_target > 0 else 0
    per_probe_cap = int(params.get("probe_max_new_tokens", 64))
    if n_probe_plan > 0:
        per_probe_cap = max(16, min(per_probe_cap, max(16, probe_budget_target // n_probe_plan)))

    attempts: List[Attempt] = []
    for i in range(n_probe_first if n_probe_plan > 0 else 0):
        probe_prompt = (
            "Fast probe only.\n"
            "Output format:\n"
            "Tentative Answer: A|B|C|D\n"
            "Confidence: <0 to 1>\n\n"
            + _mcq_block(sample)
        )
        a = _attempt(
            call_main,
            f"probe_v3.first.{i}",
            probe_prompt,
            per_probe_cap,
            temperature,
            top_p,
            trial_seed + 60001 + i * 11,
            discarded=True,
        )
        if not a.text.strip():
            break
        attempts.append(a)

    voted, agreement = _majority_vote([a.option for a in attempts])
    agree_thresh = float(params.get("stop_conf_threshold", 0.67))

    if len(attempts) > 0 and agreement < agree_thresh and n_probe_plan > n_probe_first:
        for j in range(n_probe_second):
            idx = n_probe_first + j
            probe_prompt = (
                "Additional probe due uncertainty.\n"
                "Output format:\n"
                "Tentative Answer: A|B|C|D\n"
                "Confidence: <0 to 1>\n\n"
                + _mcq_block(sample)
            )
            a = _attempt(
                call_main,
                f"probe_v3.second.{j}",
                probe_prompt,
                per_probe_cap,
                temperature,
                top_p,
                trial_seed + 61001 + idx * 13,
                discarded=True,
            )
            if not a.text.strip():
                break
            attempts.append(a)
        voted, agreement = _majority_vote([a.option for a in attempts])

    low_budget_stop_forbid_threshold = int(params.get("low_budget_stop_forbid_threshold", 1200))
    can_stop_after_probe = bool(params.get("enable_stop_after_probe", True)) and budget_total > low_budget_stop_forbid_threshold
    if voted is not None and agreement >= agree_thresh and can_stop_after_probe:
        chosen = _pick_by_option_and_conf(attempts, voted)
        final_attempt = Attempt(
            step="final.controller_v3",
            text=_format_final_answer(voted, chosen.confidence if chosen else None),
            option=voted,
            confidence=chosen.confidence if chosen else None,
        )
        return _base_return(
            final_attempt,
            attempts,
            restart_count=0,
            anchor_constraints=None,
            controller_trace={
                "decision": "stop_after_probe",
                "decision_trace": "probe->stop",
                "budget_total": budget_total,
                "solve_min_target": solve_min_target,
                "probe_budget_target": probe_budget_target,
                "n_probe": len(attempts),
                "agreement": agreement,
                "disagreement": (1.0 - agreement),
                "voted_option": voted,
                "fallback_used": False,
                "stop_after_probe": True,
            },
        )

    solve_cap = min(
        int(params.get("solve_max_new_tokens", 320)),
        max(int(params.get("solve_min_floor", 256)), int(0.8 * budget_total)),
    )
    solve_prompt = (
        "Solve carefully after probe disagreement.\n"
        "Output format:\n"
        "Final Answer: A|B|C|D\n"
        "Confidence: <0 to 1>\n"
        "Reasoning: <brief>\n\n"
        + _mcq_block(sample)
    )
    solve = _attempt(
        call_main,
        "solve.controller_v3",
        solve_prompt,
        solve_cap,
        temperature,
        top_p,
        trial_seed + 62001,
    )
    attempts.append(solve)
    final = solve

    restart_count = 0
    max_restart = int(params.get("max_restart", 1))
    restart_cap = min(int(params.get("restart_max_new_tokens", 160)), max(32, int(0.2 * budget_total)))
    while final.option is None and restart_count < max_restart:
        rp = (
            "Independent restart after parse/format failure.\n"
            "Output format:\n"
            "Final Answer: A|B|C|D\n"
            "Confidence: <0 to 1>\n\n"
            + _mcq_block(sample)
        )
        rs = _attempt(
            call_main,
            f"restart.controller_v3.{restart_count}",
            rp,
            restart_cap,
            temperature,
            top_p,
            trial_seed + 63001 + restart_count * 31,
        )
        attempts.append(rs)
        final = rs
        restart_count += 1

    return _base_return(
        final,
        attempts,
        restart_count=restart_count,
        anchor_constraints=None,
        controller_trace={
            "decision": "continue_solve",
            "decision_trace": "probe->solve" + ("->restart" if restart_count > 0 else ""),
            "budget_total": budget_total,
            "solve_min_target": solve_min_target,
            "probe_budget_target": probe_budget_target,
            "n_probe": len([a for a in attempts if a.step.startswith("probe_v3")]),
            "agreement": agreement,
            "disagreement": (1.0 - agreement),
            "voted_option": voted,
            "restarts": restart_count,
            "fallback_used": False,
            "stop_after_probe": False,
        },
    )


def _anchor_prompt(sample: Dict[str, object]) -> str:
    return (
        "Generate exactly 3 to 5 checklist constraints only.\n"
        "Rules:\n"
        "- Do NOT pick an answer.\n"
        "- Each bullet <= 12 tokens.\n"
        "- Focus on must-have / must-not violations.\n\n"
        + _mcq_block(sample)
    )


def _decompose_prompt(sample: Dict[str, object]) -> str:
    return (
        "Decompose into at most 3 short subtasks.\n"
        "Each subtask must be <= 1 sentence.\n"
        "No final answer.\n\n"
        + _mcq_block(sample)
    )


def _solve_prompt(sample: Dict[str, object], anchor: Optional[str], decomp: Optional[str], hard_anchor: bool) -> str:
    chunks: List[str] = [
        "Solve the MCQ concisely with explicit final answer.",
        "Output format:",
        "Final Answer: A|B|C|D",
        "Confidence: <0 to 1>",
        "Reasoning: <brief>",
    ]
    if anchor:
        chunks.append("Checklist constraints:")
        chunks.append(anchor)
    if decomp:
        chunks.append("Subtasks:")
        chunks.append(decomp)
    if hard_anchor:
        chunks.append("Before final answer, ensure checklist is satisfied.")
    chunks.append("")
    chunks.append(_mcq_block(sample))
    return "\n".join(chunks)


def _verify_prompt(sample: Dict[str, object], candidate: str, anchor: Optional[str]) -> str:
    checklist = anchor if anchor else "(none)"
    return (
        "Verify candidate answer against constraints.\n"
        "Output format:\n"
        "Check: PASS or FAIL\n"
        "Final Answer: A|B|C|D\n"
        "Confidence: <0 to 1>\n\n"
        f"Checklist:\n{checklist}\n\n"
        f"Candidate response:\n{candidate}\n\n"
        + _mcq_block(sample)
    )


def _run_structured(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
    call_anchor: GenerateFn,
    use_anchor: bool,
    use_decompose: bool,
    hard_anchor: bool,
) -> Dict[str, object]:
    attempts: List[Attempt] = []
    restart_count = 0
    budget_total = int(params.get("_budget_total", 10**9))

    def _cap(name: str, default: int, frac: float) -> int:
        cfg_cap = int(params.get(name, default))
        dyn_cap = max(16, int(frac * budget_total))
        return min(cfg_cap, dyn_cap)

    anchor_text: Optional[str] = None
    if use_anchor and budget_total >= int(params.get("min_budget_for_anchor", 320)):
        anchor_text = call_anchor(
            "anchor.structured",
            _anchor_prompt(sample),
            _cap("anchor_stage_cap", int(params.get("anchor_max_new_tokens", 64)), 0.12),
            0.2,
            0.9,
            trial_seed + 3001,
            True,
        )

    decomp_text: Optional[str] = None
    if use_decompose and budget_total >= int(params.get("min_budget_for_decompose", 512)):
        decomp_attempt = _attempt(
            call_main,
            "decompose.structured",
            _decompose_prompt(sample),
            _cap("decompose_stage_cap", 96, 0.16),
            float(params["temperature"]),
            float(params["top_p"]),
            trial_seed + 3501,
            discarded=True,
        )
        attempts.append(decomp_attempt)
        decomp_text = decomp_attempt.text

    solve = _attempt(
        call_main,
        "solve.structured",
        _solve_prompt(sample, anchor_text, decomp_text, hard_anchor),
        _cap("solve_stage_cap", int(params.get("solve_max_new_tokens", 300)), 0.58),
        float(params["temperature"]),
        float(params["top_p"]),
        trial_seed + 5001,
    )
    attempts.append(solve)

    verify = _attempt(
        call_main,
        "verify.structured",
        _verify_prompt(sample, solve.text, anchor_text),
        _cap("verify_stage_cap", 96, 0.10),
        float(params["temperature"]),
        float(params["top_p"]),
        trial_seed + 5501,
        discarded=True,
    )
    attempts.append(verify)

    final = solve
    if hard_anchor and verify.option is not None:
        final = verify

    max_restart = int(params.get("max_restart", 1))
    while final.option is None and restart_count < max_restart:
        rs = _attempt(
            call_main,
            f"restart.structured.{restart_count}",
            _solve_prompt(sample, anchor_text, decomp_text, hard_anchor),
            _cap("restart_stage_cap", int(params.get("restart_max_new_tokens", 220)), 0.28),
            float(params["temperature"]),
            float(params["top_p"]),
            trial_seed + 6001 + restart_count * 37,
        )
        attempts.append(rs)
        final = rs
        restart_count += 1

    return _base_return(
        final,
        attempts,
        restart_count,
        anchor_constraints=anchor_text,
        controller_trace={
            "use_anchor": use_anchor,
            "use_decompose": use_decompose,
            "hard_anchor": hard_anchor,
            "restarts": restart_count,
        },
    )


def run_ours_full(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
    call_anchor: GenerateFn,
) -> Dict[str, object]:
    return _run_structured(
        sample=sample,
        params=params,
        trial_seed=trial_seed,
        call_main=call_main,
        call_anchor=call_anchor,
        use_anchor=True,
        use_decompose=True,
        hard_anchor=bool(params.get("hard_anchor", True)),
    )


def run_ours_decompose_only(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
    call_anchor: GenerateFn,
) -> Dict[str, object]:
    return _run_structured(
        sample=sample,
        params=params,
        trial_seed=trial_seed,
        call_main=call_main,
        call_anchor=call_anchor,
        use_anchor=False,
        use_decompose=True,
        hard_anchor=False,
    )


def run_ours_anchor_only(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
    call_anchor: GenerateFn,
) -> Dict[str, object]:
    return _run_structured(
        sample=sample,
        params=params,
        trial_seed=trial_seed,
        call_main=call_main,
        call_anchor=call_anchor,
        use_anchor=True,
        use_decompose=False,
        hard_anchor=bool(params.get("hard_anchor", True)),
    )


def run_ours_controller_v2_nofallback_forcecontinue(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    p = dict(params)
    p["enable_low_budget_fallback"] = False
    return run_ours_controller_v2(sample, p, trial_seed, call_main)


def run_ours_controller_v2_nofallback_stopcap(
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
) -> Dict[str, object]:
    p = dict(params)
    p["enable_low_budget_fallback"] = False
    return run_ours_controller_v2(sample, p, trial_seed, call_main)


def run_method(
    method_name: str,
    sample: Dict[str, object],
    params: Dict[str, object],
    trial_seed: int,
    call_main: GenerateFn,
    call_anchor: GenerateFn,
) -> Dict[str, object]:
    if method_name == "baseline_longcot":
        return run_baseline_longcot(sample, params, trial_seed, call_main)
    if method_name == "hard_cap":
        return run_hard_cap(sample, params, trial_seed, call_main)
    if method_name == "hard_cap_matched":
        return run_hard_cap(sample, params, trial_seed, call_main)
    if method_name == "self_consistency":
        return run_self_consistency(sample, params, trial_seed, call_main)
    if method_name == "confidence_select":
        return run_confidence_select(sample, params, trial_seed, call_main)
    if method_name == "budgeted_self_consistency":
        return run_budgeted_self_consistency(sample, params, trial_seed, call_main)
    if method_name == "probe_only_fixedk" or method_name.startswith("probe_only_fixedk_"):
        return run_probe_only_fixedk(sample, params, trial_seed, call_main)
    if method_name == "probe_adaptive_k" or method_name.startswith("probe_adaptive_k_"):
        return run_probe_adaptive_k(sample, params, trial_seed, call_main)
    if method_name == "forced_deliberation":
        return run_forced_deliberation(sample, params, trial_seed, call_main)
    if method_name == "ours_controller":
        return run_ours_controller(sample, params, trial_seed, call_main)
    if method_name == "ours_controller_v2":
        return run_ours_controller_v2(sample, params, trial_seed, call_main)
    if method_name == "ours_controller_v2_nofallback":
        return run_ours_controller_v2(sample, params, trial_seed, call_main)
    if method_name == "ours_controller_v2_nofallback_forcecontinue":
        return run_ours_controller_v2_nofallback_forcecontinue(sample, params, trial_seed, call_main)
    if method_name == "ours_controller_v2_nofallback_stopcap":
        return run_ours_controller_v2_nofallback_stopcap(sample, params, trial_seed, call_main)
    if method_name == "ours_controller_v3":
        return run_ours_controller_v3(sample, params, trial_seed, call_main)
    if method_name == "ours_controller_v3_nofallback":
        return run_ours_controller_v3(sample, params, trial_seed, call_main)
    if method_name == "ours_full":
        return run_ours_full(sample, params, trial_seed, call_main, call_anchor)
    if method_name == "ours_decompose_only":
        return run_ours_decompose_only(sample, params, trial_seed, call_main, call_anchor)
    if method_name == "ours_anchor_only":
        return run_ours_anchor_only(sample, params, trial_seed, call_main, call_anchor)

    raise ValueError(f"Unknown method: {method_name}")


__all__ = ["run_method"]
