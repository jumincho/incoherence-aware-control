from __future__ import annotations

import argparse
import glob
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import yaml

HOT_MESS_UTILS = Path(__file__).resolve().parents[2] / "hot-mess-of-ai" / "scripts"
if str(HOT_MESS_UTILS) not in sys.path:
    sys.path.insert(0, str(HOT_MESS_UTILS))

from utils import process_question_metrics  # type: ignore

from .parser import option_to_index


def load_rows(run_dir: Path) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for p in sorted(glob.glob(str(run_dir / "results_shard*.jsonl"))):
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except Exception:
                    continue

    dedup = {}
    for r in rows:
        key = (r.get("doc_id"), r.get("seed"), r.get("method"), int(r.get("budget_total", -1)))
        dedup[key] = r
    return list(dedup.values())


def _to_answer_and_prob(pred_option: str | None) -> Tuple[int, np.ndarray]:
    idx = option_to_index(pred_option)
    if idx is None:
        return 4, np.ones(4, dtype=float) / 4.0
    probs = np.zeros(4, dtype=float)
    probs[idx] = 1.0
    return idx, probs


def _inter_disagreement(final_answers: List[str]) -> float:
    if not final_answers:
        return 1.0
    cnt = Counter(final_answers)
    return 1.0 - (max(cnt.values()) / len(final_answers))


def paired_bootstrap_delta(
    base_doc_metric: Dict[str, float],
    other_doc_metric: Dict[str, float],
    iters: int = 2000,
    seed: int = 1234,
) -> Dict[str, float]:
    docs = sorted(set(base_doc_metric.keys()) & set(other_doc_metric.keys()))
    if not docs:
        return {"n": 0, "delta_mean": math.nan, "ci_low": math.nan, "ci_high": math.nan, "p_two_sided": math.nan}

    base = np.array([base_doc_metric[d] for d in docs], dtype=float)
    other = np.array([other_doc_metric[d] for d in docs], dtype=float)
    deltas = other - base

    rng = np.random.default_rng(seed)
    boots = np.empty(iters, dtype=float)
    n = len(docs)
    for i in range(iters):
        idx = rng.integers(0, n, n)
        boots[i] = float(np.mean(deltas[idx]))

    ci_low, ci_high = np.percentile(boots, [2.5, 97.5])
    p = 2 * min(float(np.mean(boots <= 0.0)), float(np.mean(boots >= 0.0)))
    return {
        "n": n,
        "delta_mean": float(np.mean(deltas)),
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "p_two_sided": float(min(1.0, p)),
    }


def compute_budget_stats(
    rows: List[Dict[str, object]],
    budget: int,
    identity_tol: float,
    identity_dump_path: Path,
    drop_parse_fail: bool = False,
) -> Dict[str, Dict[str, object]]:
    grouped: Dict[str, Dict[str, List[Dict[str, object]]]] = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if int(r.get("budget_total", -1)) != int(budget):
            continue
        grouped[str(r["method"])][str(r["doc_id"])].append(r)

    out: Dict[str, Dict[str, object]] = {}
    identity_fails: List[Dict[str, object]] = []

    for method, by_doc in grouped.items():
        sum_bias = 0.0
        sum_variance = 0.0
        sum_accuracy = 0.0
        sum_total_tokens = 0.0
        sum_output_tokens = 0.0
        sum_budget_util = 0.0
        total_trials = 0
        intra_flips: List[float] = []
        parse_fail_count = 0
        parse_fail_types = Counter()

        doc_incoh = {}
        doc_acc = {}
        doc_bias = {}
        doc_var = {}
        doc_inter = {}
        n_docs_metric = 0

        for doc_id, trials in by_doc.items():
            metric_trials = trials
            if drop_parse_fail:
                metric_trials = [t for t in trials if t.get("parse_fail_type") is None]
                if not metric_trials:
                    continue

            answers = []
            probs = []
            gold_idx = option_to_index(str(metric_trials[0]["target_option"]))
            if gold_idx is None:
                continue
            n_docs_metric += 1

            final_answers = []
            for t in metric_trials:
                ans, prob = _to_answer_and_prob(t.get("pred_option"))
                answers.append(ans)
                probs.append(prob)
                total_trials += 1
                u = t.get("usage") or {}
                tt = int(u.get("total_tokens", 0))
                sum_total_tokens += tt
                sum_output_tokens += int(u.get("output_tokens", 0))
                bgt = int(t.get("budget_total", budget))
                if bgt > 0:
                    sum_budget_util += min(1.0, tt / bgt)
                intra_flips.append(float(t.get("intermediate_flip_count", 0)))

                pft = t.get("parse_fail_type")
                if pft is not None:
                    parse_fail_count += 1
                    parse_fail_types[str(pft)] += 1
                if t.get("pred_option") is not None:
                    final_answers.append(str(t.get("pred_option")))

            m = process_question_metrics(answers=answers, probs=probs, gold_answer=gold_idx)

            # Identity sanity check: (1 - soft_acc) == bias + actual_variance
            lhs = 1.0 - float(m["accuracy"])
            rhs = float(m["bias"]) + float(m["actual_variance"])
            if abs(lhs - rhs) > identity_tol:
                identity_fails.append(
                    {
                        "budget_total": int(budget),
                        "method": method,
                        "doc_id": doc_id,
                        "drop_parse_fail": drop_parse_fail,
                        "lhs_error": lhs,
                        "rhs_bias_plus_actual_var": rhs,
                        "diff": lhs - rhs,
                        "trials": [
                            {
                                "seed": int(t.get("seed", -1)),
                                "pred_option": t.get("pred_option"),
                                "target_option": t.get("target_option"),
                                "parse_fail_type": t.get("parse_fail_type"),
                                "response_text": t.get("response_text", "")[:400],
                            }
                            for t in trials
                        ],
                    }
                )

            sum_bias += float(m["bias"])
            sum_variance += float(m["variance"])
            sum_accuracy += float(m["accuracy_hard"])

            err = float(m["bias"]) + float(m["variance"])
            doc_incoh[doc_id] = float(m["variance"]) / err if err > 0 else 0.0
            doc_acc[doc_id] = float(m["accuracy_hard"])
            doc_bias[doc_id] = float(m["bias"])
            doc_var[doc_id] = float(m["variance"])
            doc_inter[doc_id] = _inter_disagreement(final_answers)

        n_docs = max(1, n_docs_metric)
        error = sum_bias + sum_variance
        incoh = (sum_variance / error) if error > 0 else 0.0

        out[method] = {
            "n_docs": n_docs_metric,
            "n_trials": total_trials,
            "mean_bias": sum_bias / n_docs,
            "mean_variance": sum_variance / n_docs,
            "mean_error": error / n_docs,
            "incoherence": incoh,
            "accuracy": sum_accuracy / n_docs,
            "avg_total_tokens": (sum_total_tokens / total_trials) if total_trials else 0.0,
            "avg_output_tokens": (sum_output_tokens / total_trials) if total_trials else 0.0,
            "avg_budget_utilization": (sum_budget_util / total_trials) if total_trials else 0.0,
            "intra_flip_rate": float(np.mean(intra_flips)) if intra_flips else 0.0,
            "inter_disagreement": float(np.mean(list(doc_inter.values()))) if doc_inter else 0.0,
            "parse_fail_rate": (parse_fail_count / total_trials) if total_trials else 0.0,
            "parse_fail_count": int(parse_fail_count),
            "parse_fail_types": dict(parse_fail_types),
            "doc_incoh": doc_incoh,
            "doc_acc": doc_acc,
            "doc_bias": doc_bias,
            "doc_var": doc_var,
            "doc_inter": doc_inter,
            "drop_parse_fail": drop_parse_fail,
        }

    if identity_fails:
        with identity_dump_path.open("a", encoding="utf-8") as f:
            for row in identity_fails:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    return out


def controller_diagnostics(rows: List[Dict[str, object]], budget: int, method: str) -> Dict[str, object]:
    tgt = [r for r in rows if int(r.get("budget_total", -1)) == int(budget) and str(r.get("method")) == method]
    if not tgt:
        return {}

    decisions = Counter()
    probe_tokens = []
    solve_tokens = []
    restart_tokens = []
    total_tokens = []

    for r in tgt:
        trace = r.get("controller_trace") or {}
        decision = str(trace.get("decision", "unknown"))
        decisions[decision] += 1

        stage = r.get("stage_token_spend") or {}
        probe_tok = 0
        solve_tok = 0
        restart_tok = 0
        for k, v in stage.items():
            tok = int((v or {}).get("total_tokens", 0))
            if "probe" in str(k):
                probe_tok += tok
            elif "solve" in str(k):
                solve_tok += tok
            elif "restart" in str(k):
                restart_tok += tok
        probe_tokens.append(probe_tok)
        solve_tokens.append(solve_tok)
        restart_tokens.append(restart_tok)
        total_tokens.append(int((r.get("usage") or {}).get("total_tokens", 0)))

    return {
        "n": len(tgt),
        "decision_counts": dict(decisions),
        "decision_rates": {k: (v / len(tgt)) for k, v in decisions.items()} if tgt else {},
        "fallback_rate": (decisions.get("fallback_hard_cap", 0) / len(tgt)) if tgt else 0.0,
        "stop_after_probe_rate": (decisions.get("stop_after_probe", 0) / len(tgt)) if tgt else 0.0,
        "avg_probe_tokens": float(np.mean(probe_tokens)) if probe_tokens else 0.0,
        "avg_solve_tokens": float(np.mean(solve_tokens)) if solve_tokens else 0.0,
        "avg_restart_tokens": float(np.mean(restart_tokens)) if restart_tokens else 0.0,
        "avg_total_tokens": float(np.mean(total_tokens)) if total_tokens else 0.0,
        "probe_token_share": (float(np.sum(probe_tokens)) / float(np.sum(total_tokens))) if total_tokens and np.sum(total_tokens) > 0 else 0.0,
        "solve_token_share": (float(np.sum(solve_tokens)) / float(np.sum(total_tokens))) if total_tokens and np.sum(total_tokens) > 0 else 0.0,
    }


def stratify_disagreement(
    baseline_inter: Dict[str, float],
    base_metric: Dict[str, float],
    other_metric: Dict[str, float],
) -> Dict[str, Dict[str, float]]:
    docs = sorted(set(baseline_inter.keys()) & set(base_metric.keys()) & set(other_metric.keys()))
    if len(docs) < 3:
        return {}

    vals = np.array([baseline_inter[d] for d in docs], dtype=float)
    q1, q2 = np.quantile(vals, [1 / 3, 2 / 3])

    buckets = {"low": [], "mid": [], "high": []}
    for d in docs:
        v = baseline_inter[d]
        if v <= q1:
            buckets["low"].append(d)
        elif v <= q2:
            buckets["mid"].append(d)
        else:
            buckets["high"].append(d)

    out = {}
    for k, ds in buckets.items():
        if not ds:
            continue
        delta = np.mean([other_metric[d] - base_metric[d] for d in ds])
        out[k] = {"n": len(ds), "delta_mean": float(delta)}
    return out


def build_failure_taxonomy(rows: List[Dict[str, object]], budget: int, method: str = "ours_full") -> Dict[str, object]:
    tgt = [r for r in rows if int(r.get("budget_total", -1)) == int(budget) and r.get("method") == method and not bool(r.get("is_correct", False))]
    counts = Counter()
    samples = []

    for r in tgt:
        reason = "wrong_reasoning"
        if r.get("parse_fail_type"):
            reason = f"parse_fail:{r.get('parse_fail_type')}"
        elif bool(r.get("stopped_by_budget", False)):
            reason = "budget_exhausted"
        else:
            anchor = str(r.get("anchor_constraints") or "")
            if anchor and len(anchor.split()) > 80:
                reason = "anchor_too_long"
        counts[reason] += 1
        if len(samples) < 20:
            samples.append(
                {
                    "doc_id": r.get("doc_id"),
                    "seed": r.get("seed"),
                    "reason": reason,
                    "budget_total": r.get("budget_total"),
                    "pred_option": r.get("pred_option"),
                    "target_option": r.get("target_option"),
                    "usage": r.get("usage"),
                }
            )

    return {"counts": dict(counts), "samples": samples, "n_failures": len(tgt)}


def parse_fail_table(rows: List[Dict[str, object]], budget: int) -> Dict[str, object]:
    out = defaultdict(lambda: Counter())
    total = Counter()
    for r in rows:
        if int(r.get("budget_total", -1)) != int(budget):
            continue
        m = str(r.get("method"))
        pft = str(r.get("parse_fail_type") or "OK")
        out[m][pft] += 1
        total[m] += 1

    table = {}
    for m, ctr in out.items():
        row = {k: int(v) for k, v in ctr.items()}
        row["total"] = int(total[m])
        row["parse_fail_rate"] = (row["total"] - row.get("OK", 0)) / row["total"] if row["total"] else 0.0
        table[m] = row
    return table


def parse_fail_reason_table(rows: List[Dict[str, object]], budget: int) -> Dict[str, object]:
    out = defaultdict(lambda: Counter())
    total = Counter()
    for r in rows:
        if int(r.get("budget_total", -1)) != int(budget):
            continue
        m = str(r.get("method"))
        reason = str(r.get("parse_fail_reason") or "OK")
        out[m][reason] += 1
        total[m] += 1

    table = {}
    for m, ctr in out.items():
        row = {k: int(v) for k, v in ctr.items()}
        row["total"] = int(total[m])
        row["parse_fail_rate"] = (
            (row["total"] - row.get("OK", 0) - row.get("repaired_success", 0)) / row["total"] if row["total"] else 0.0
        )
        table[m] = row
    return table


def main() -> None:
    ap = argparse.ArgumentParser(description="Analyze Round2 results with Hot-Mess style metrics")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--bootstrap-iters", type=int, default=2000)
    ap.add_argument("--identity-tol", type=float, default=1e-6)
    args = ap.parse_args()

    run_dir = Path(args.run_dir).resolve()
    cfg = yaml.safe_load((run_dir / "config_resolved.yaml").read_text())
    rows = load_rows(run_dir)

    baseline = cfg["evaluation"].get("compare_to", "baseline_longcot")
    budgets = cfg["evaluation"].get("total_token_budgets")
    if budgets is None:
        budgets = [int(cfg["evaluation"].get("output_token_budget", 768))]
    budgets = [int(b) for b in budgets]

    identity_dump = run_dir / "identity_failures.jsonl"
    if identity_dump.exists():
        identity_dump.unlink()

    summary_by_budget = {}
    summary_by_budget_parse_excluded = {}
    comparisons_by_budget = {}
    verdict_by_budget = {}
    parse_fail_by_budget = {}
    parse_fail_reason_by_budget = {}
    stratification_by_budget = {}
    bias_var_shift_by_budget = {}
    failure_taxonomy_by_budget = {}
    controller_diag_by_budget = {}

    success_cfg = cfg["evaluation"]["success"]
    min_abs = float(success_cfg.get("incoherence_reduction_min_abs", 0.0))
    min_rel = float(success_cfg.get("incoherence_reduction_min_rel", success_cfg.get("incoherence_reduction_min", 0.1)))
    require_no_sig_drop = bool(success_cfg.get("require_no_sig_accuracy_drop", True))

    pareto_points = []

    for b in budgets:
        stats = compute_budget_stats(rows, b, args.identity_tol, identity_dump, drop_parse_fail=False)
        stats_parse_excluded = compute_budget_stats(rows, b, args.identity_tol, identity_dump, drop_parse_fail=True)
        if baseline not in stats:
            continue

        summary_by_budget[str(b)] = stats
        summary_by_budget_parse_excluded[str(b)] = stats_parse_excluded
        parse_fail_by_budget[str(b)] = parse_fail_table(rows, b)
        parse_fail_reason_by_budget[str(b)] = parse_fail_reason_table(rows, b)
        failure_taxonomy_by_budget[str(b)] = build_failure_taxonomy(rows, b, method="ours_full")
        controller_diag_by_budget[str(b)] = {
            "ours_controller": controller_diagnostics(rows, b, method="ours_controller"),
            "ours_controller_v2": controller_diagnostics(rows, b, method="ours_controller_v2"),
            "ours_controller_v2_nofallback": controller_diagnostics(rows, b, method="ours_controller_v2_nofallback"),
            "ours_controller_v3": controller_diagnostics(rows, b, method="ours_controller_v3"),
            "ours_controller_v3_nofallback": controller_diagnostics(rows, b, method="ours_controller_v3_nofallback"),
        }

        base_doc_incoh = stats[baseline]["doc_incoh"]
        base_doc_acc = stats[baseline]["doc_acc"]
        base_doc_bias = stats[baseline]["doc_bias"]
        base_doc_var = stats[baseline]["doc_var"]

        comps = {}
        verdict = {}
        shifts = {}

        for method, s in stats.items():
            pareto_points.append(
                {
                    "budget_total": int(b),
                    "method": method,
                    "accuracy": float(s["accuracy"]),
                    "incoherence": float(s["incoherence"]),
                    "avg_total_tokens": float(s["avg_total_tokens"]),
                }
            )
            if method == baseline:
                continue

            incoh_delta = paired_bootstrap_delta(base_doc_incoh, s["doc_incoh"], iters=args.bootstrap_iters, seed=2026 + b)
            acc_delta = paired_bootstrap_delta(base_doc_acc, s["doc_acc"], iters=args.bootstrap_iters, seed=3026 + b)
            bias_delta = paired_bootstrap_delta(base_doc_bias, s["doc_bias"], iters=args.bootstrap_iters, seed=4026 + b)
            var_delta = paired_bootstrap_delta(base_doc_var, s["doc_var"], iters=args.bootstrap_iters, seed=5026 + b)

            base_incoh = float(stats[baseline]["incoherence"])
            other_incoh = float(s["incoherence"])

            # Primary relative-improvement definition used for success criterion.
            # rel_improve = (base - method) / base
            incoh_reduction_abs = base_incoh - other_incoh
            incoh_reduction_rel = incoh_reduction_abs / base_incoh if base_incoh > 0 else 0.0

            # Secondary doc-level bootstrap view retained for diagnostics.
            incoh_reduction_abs_doc_boot = -float(incoh_delta["delta_mean"])
            incoh_reduction_rel_doc_boot = (
                incoh_reduction_abs_doc_boot / base_incoh if base_incoh > 0 else 0.0
            )

            acc_ci_low = float(acc_delta["ci_low"])
            acc_ci_high = float(acc_delta["ci_high"])
            no_sig_drop = acc_ci_low <= 0 <= acc_ci_high

            cond_abs = incoh_reduction_abs >= min_abs
            cond_rel = incoh_reduction_rel >= min_rel
            cond_acc = no_sig_drop if require_no_sig_drop else True

            verdict[method] = {
                "pass": bool(cond_abs and cond_rel and cond_acc),
                "incoh_reduction_abs": incoh_reduction_abs,
                "incoh_reduction_rel": incoh_reduction_rel,
                "incoh_reduction_abs_doc_boot": incoh_reduction_abs_doc_boot,
                "incoh_reduction_rel_doc_boot": incoh_reduction_rel_doc_boot,
                "acc_no_significant_drop": no_sig_drop,
                "acc_ci_low": acc_ci_low,
                "acc_ci_high": acc_ci_high,
            }
            comps[method] = {
                "delta_incoh_other_minus_base": incoh_delta,
                "delta_acc_other_minus_base": acc_delta,
                "incoh_reduction_abs": incoh_reduction_abs,
                "incoh_reduction_rel": incoh_reduction_rel,
                "incoh_reduction_abs_doc_boot": incoh_reduction_abs_doc_boot,
                "incoh_reduction_rel_doc_boot": incoh_reduction_rel_doc_boot,
            }
            shifts[method] = {
                "delta_bias_other_minus_base": bias_delta,
                "delta_variance_other_minus_base": var_delta,
            }

        comparisons_by_budget[str(b)] = comps
        verdict_by_budget[str(b)] = verdict
        bias_var_shift_by_budget[str(b)] = shifts

        if "ours_controller" in stats:
            stratification_by_budget[str(b)] = {
                "incoh_delta_by_baseline_disagreement": stratify_disagreement(
                    stats[baseline]["doc_inter"],
                    stats[baseline]["doc_incoh"],
                    stats["ours_controller"]["doc_incoh"],
                ),
                "acc_delta_by_baseline_disagreement": stratify_disagreement(
                    stats[baseline]["doc_inter"],
                    stats[baseline]["doc_acc"],
                    stats["ours_controller"]["doc_acc"],
                ),
            }
        if "ours_controller_v2" in stats:
            stratification_by_budget.setdefault(str(b), {})
            stratification_by_budget[str(b)]["incoh_delta_v2_by_baseline_disagreement"] = stratify_disagreement(
                stats[baseline]["doc_inter"],
                stats[baseline]["doc_incoh"],
                stats["ours_controller_v2"]["doc_incoh"],
            )
            stratification_by_budget[str(b)]["acc_delta_v2_by_baseline_disagreement"] = stratify_disagreement(
                stats[baseline]["doc_inter"],
                stats[baseline]["doc_acc"],
                stats["ours_controller_v2"]["doc_acc"],
            )
        if "ours_controller_v2_nofallback" in stats:
            stratification_by_budget.setdefault(str(b), {})
            stratification_by_budget[str(b)]["incoh_delta_v2_nofallback_by_baseline_disagreement"] = stratify_disagreement(
                stats[baseline]["doc_inter"],
                stats[baseline]["doc_incoh"],
                stats["ours_controller_v2_nofallback"]["doc_incoh"],
            )
            stratification_by_budget[str(b)]["acc_delta_v2_nofallback_by_baseline_disagreement"] = stratify_disagreement(
                stats[baseline]["doc_inter"],
                stats[baseline]["doc_acc"],
                stats["ours_controller_v2_nofallback"]["doc_acc"],
            )

    out_json = {
        "run_dir": str(run_dir),
        "baseline": baseline,
        "budgets": budgets,
        "summary_by_budget": summary_by_budget,
        "summary_by_budget_parse_excluded": summary_by_budget_parse_excluded,
        "comparisons_by_budget": comparisons_by_budget,
        "verdict_by_budget": verdict_by_budget,
        "parse_fail_by_budget": parse_fail_by_budget,
        "parse_fail_reason_by_budget": parse_fail_reason_by_budget,
        "stratification_by_budget": stratification_by_budget,
        "bias_variance_shift_by_budget": bias_var_shift_by_budget,
        "failure_taxonomy_by_budget": failure_taxonomy_by_budget,
        "controller_diagnostics_by_budget": controller_diag_by_budget,
        "pareto_points": pareto_points,
    }
    (run_dir / "analysis_summary_round2.json").write_text(json.dumps(out_json, indent=2))
    (run_dir / "pareto_points.json").write_text(json.dumps(pareto_points, indent=2))

    lines = []
    lines.append("# Round2 Summary")
    lines.append("")
    lines.append(f"- Run dir: `{run_dir}`")
    lines.append(f"- Baseline: `{baseline}`")
    lines.append(f"- Budgets: `{budgets}`")
    lines.append("")

    for b in budgets:
        sb = summary_by_budget.get(str(b), {})
        if not sb:
            continue
        lines.append(f"## Budget {b}")
        lines.append("")
        lines.append("| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
        for method, s in sorted(sb.items()):
            lines.append(
                f"| {method} | {s['accuracy']:.4f} | {s['mean_bias']:.4f} | {s['mean_variance']:.4f} | {s['incoherence']:.4f} | {s['avg_total_tokens']:.1f} | {s['avg_budget_utilization']:.3f} | {s['parse_fail_rate']:.3f} |"
            )

        lines.append("")
        lines.append("| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for method, c in sorted(comparisons_by_budget.get(str(b), {}).items()):
            acc = c["delta_acc_other_minus_base"]
            v = verdict_by_budget[str(b)][method]
            verdict_txt = "PASS" if v["pass"] else "FAIL"
            lines.append(
                f"| {method} | {c['incoh_reduction_abs']:.4f} | {c['incoh_reduction_rel']:.3f} | {c.get('incoh_reduction_rel_doc_boot', 0.0):.3f} | {acc['delta_mean']:.4f} | [{acc['ci_low']:.4f}, {acc['ci_high']:.4f}] | {verdict_txt} |"
            )
        lines.append("")

        cd = controller_diag_by_budget.get(str(b), {})
        if cd:
            lines.append("| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |")
            lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
            for m in [
                "ours_controller",
                "ours_controller_v2",
                "ours_controller_v2_nofallback",
                "ours_controller_v3",
                "ours_controller_v3_nofallback",
            ]:
                row = cd.get(m) or {}
                if not row:
                    continue
                lines.append(
                    f"| {m} | {row.get('n', 0)} | {100.0*row.get('fallback_rate', 0.0):.1f}% | {100.0*row.get('stop_after_probe_rate', 0.0):.1f}% | {100.0*row.get('probe_token_share', 0.0):.1f}% | {100.0*row.get('solve_token_share', 0.0):.1f}% | {row.get('avg_probe_tokens', 0.0):.1f} | {row.get('avg_solve_tokens', 0.0):.1f} | {row.get('avg_restart_tokens', 0.0):.1f} | `{row.get('decision_counts', {})}` |"
                )
            lines.append("")

    report_text = "\n".join(lines) + "\n"
    (run_dir / "round2_summary.md").write_text(report_text)

    reports_dir = Path(__file__).resolve().parents[1] / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "round2_summary.md").write_text(report_text)

    print(report_text)
    print(f"Saved: {run_dir / 'analysis_summary_round2.json'}")
    print(f"Identity failures dumped: {identity_dump if identity_dump.exists() else 'none'}")


if __name__ == "__main__":
    main()
