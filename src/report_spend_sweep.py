from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import yaml


def _load_rows(run_dir: Path) -> List[Dict[str, object]]:
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


def _auc_binary(scores: List[float], labels: List[int]) -> float:
    s = np.array(scores, dtype=float)
    y = np.array(labels, dtype=int)
    pos = np.where(y == 1)[0]
    neg = np.where(y == 0)[0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")

    order = np.argsort(s)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(s) + 1)

    vals, inv, counts = np.unique(s, return_inverse=True, return_counts=True)
    for i, c in enumerate(counts):
        if c > 1:
            idx = np.where(inv == i)[0]
            ranks[idx] = np.mean(ranks[idx])

    r_pos = np.sum(ranks[pos])
    u = r_pos - len(pos) * (len(pos) + 1) / 2
    return float(u / (len(pos) * len(neg)))


def _ece_binary(scores: List[float], labels: List[int], n_bins: int = 10) -> float:
    if not scores:
        return float("nan")
    s = np.array(scores, dtype=float)
    y = np.array(labels, dtype=float)
    s = np.clip(s, 0.0, 1.0)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    n = len(s)
    for i in range(n_bins):
        lo, hi = edges[i], edges[i + 1]
        if i == n_bins - 1:
            mask = (s >= lo) & (s <= hi)
        else:
            mask = (s >= lo) & (s < hi)
        if not np.any(mask):
            continue
        conf = float(np.mean(s[mask]))
        acc = float(np.mean(y[mask]))
        ece += (np.sum(mask) / n) * abs(acc - conf)
    return float(ece)


def _parse_repair_stats(rows: List[Dict[str, object]], methods: List[str], budgets: List[int]) -> Dict[str, Dict[str, Dict[str, float]]]:
    out: Dict[str, Dict[str, Dict[str, float]]] = {}
    for b in budgets:
        out[str(b)] = {}
        for m in methods:
            tgt = [r for r in rows if int(r.get("budget_total", -1)) == int(b) and str(r.get("method")) == m]
            n = len(tgt)
            if n == 0:
                out[str(b)][m] = {
                    "n": 0,
                    "parse_fail_rate": 0.0,
                    "repair_attempt_rate": 0.0,
                    "repair_success_rate_given_attempt": 0.0,
                    "repair_success_rate_overall": 0.0,
                }
                continue
            parse_fail = sum(1 for r in tgt if r.get("parse_fail_type") is not None)
            rep_attempt = sum(1 for r in tgt if bool(r.get("parse_repair_used")))
            rep_success = sum(
                1
                for r in tgt
                if bool(r.get("parse_repair_used"))
                and r.get("parse_fail_type_initial") is not None
                and r.get("parse_fail_type") is None
            )
            out[str(b)][m] = {
                "n": n,
                "parse_fail_rate": parse_fail / n,
                "repair_attempt_rate": rep_attempt / n,
                "repair_success_rate_given_attempt": (rep_success / rep_attempt) if rep_attempt else 0.0,
                "repair_success_rate_overall": rep_success / n,
            }
    return out


def _parse_fail_reason_stats(
    rows: List[Dict[str, object]], methods: List[str], budgets: List[int]
) -> Dict[str, Dict[str, Dict[str, float]]]:
    out: Dict[str, Dict[str, Dict[str, float]]] = {}
    for b in budgets:
        out[str(b)] = {}
        for m in methods:
            tgt = [r for r in rows if int(r.get("budget_total", -1)) == int(b) and str(r.get("method")) == m]
            ctr = Counter([str(r.get("parse_fail_reason") or "OK") for r in tgt])
            row: Dict[str, float] = {"n": float(len(tgt))}
            for k, v in ctr.items():
                row[f"reason::{k}"] = float(v)
            out[str(b)][m] = row
    return out


def _phase_thresholds_from_summary(summary: Dict[str, object], budgets: List[int]) -> Dict[str, object]:

    nf_vs_hc: List[Tuple[int, float, float]] = []
    nf_vs_sc: List[Tuple[int, float, float]] = []
    for b in budgets:
        sb = summary.get(str(b), {})
        if not sb:
            continue
        nf = sb.get("ours_controller_v2_nofallback")
        hc = sb.get("hard_cap")
        sc = sb.get("budgeted_self_consistency")
        if nf and hc:
            nf_vs_hc.append((b, float(nf["incoherence"]) - float(hc["incoherence"]), float(nf["accuracy"]) - float(hc["accuracy"])))
        if nf and sc:
            nf_vs_sc.append((b, float(nf["incoherence"]) - float(sc["incoherence"]), float(nf["accuracy"]) - float(sc["accuracy"])))

    def first_budget(rows: List[Tuple[int, float, float]], incoh_lt: float, acc_ge: float) -> int | None:
        for b, dincoh, dacc in sorted(rows, key=lambda x: x[0]):
            if dincoh < incoh_lt and dacc >= acc_ge:
                return b
        return None

    return {
        "nf_vs_hc": [
            {"budget": b, "delta_incoh": dincoh, "delta_acc": dacc}
            for b, dincoh, dacc in sorted(nf_vs_hc, key=lambda x: x[0])
        ],
        "nf_vs_sc": [
            {"budget": b, "delta_incoh": dincoh, "delta_acc": dacc}
            for b, dincoh, dacc in sorted(nf_vs_sc, key=lambda x: x[0])
        ],
        "threshold_nf_beats_hc_incoh_and_acc": first_budget(nf_vs_hc, 0.0, 0.0),
        "threshold_nf_beats_sc_incoh_with_acc_tol_1p": first_budget(nf_vs_sc, 0.0, -0.01),
        "threshold_nf_beats_sc_incoh_with_acc_tol_2p": first_budget(nf_vs_sc, 0.0, -0.02),
    }


def _phase_thresholds(analysis: Dict[str, object], summary_key: str = "summary_by_budget") -> Dict[str, object]:
    budgets = [int(b) for b in analysis.get("budgets", [])]
    summary = analysis.get(summary_key, {})
    return _phase_thresholds_from_summary(summary, budgets)


def _threshold_ci_bootstrap(
    analysis: Dict[str, object],
    base_method: str = "hard_cap",
    method: str = "ours_controller_v2_nofallback",
    summary_key: str = "summary_by_budget",
    iters: int = 1000,
    seed: int = 2026,
) -> Dict[str, object]:
    budgets = sorted([int(b) for b in analysis.get("budgets", [])])
    summary = analysis.get(summary_key, {})
    rng = np.random.default_rng(seed)

    per_budget = []
    for b in budgets:
        sb = summary.get(str(b), {})
        if base_method not in sb or method not in sb:
            continue
        base_acc = sb[base_method].get("doc_acc", {})
        base_incoh = sb[base_method].get("doc_incoh", {})
        meth_acc = sb[method].get("doc_acc", {})
        meth_incoh = sb[method].get("doc_incoh", {})
        docs = sorted(set(base_acc.keys()) & set(base_incoh.keys()) & set(meth_acc.keys()) & set(meth_incoh.keys()))
        if not docs:
            continue
        per_budget.append((b, docs, base_acc, base_incoh, meth_acc, meth_incoh))

    if not per_budget:
        return {"method": method, "base_method": base_method, "n_boot": 0}

    thresholds = []
    for _ in range(iters):
        hit = None
        for b, docs, base_acc, base_incoh, meth_acc, meth_incoh in per_budget:
            n = len(docs)
            idx = rng.integers(0, n, n)
            sample_docs = [docs[i] for i in idx]
            dacc = float(np.mean([meth_acc[d] - base_acc[d] for d in sample_docs]))
            dincoh = float(np.mean([meth_incoh[d] - base_incoh[d] for d in sample_docs]))
            if dacc > 0 and dincoh < 0:
                hit = b
                break
        thresholds.append(hit if hit is not None else np.nan)

    arr = np.array(thresholds, dtype=float)
    finite = arr[np.isfinite(arr)]
    out = {
        "method": method,
        "base_method": base_method,
        "summary_key": summary_key,
        "n_boot": int(iters),
        "n_finite": int(finite.size),
        "finite_rate": float(finite.size / max(1, arr.size)),
    }
    if finite.size > 0:
        out.update(
            {
                "median": float(np.median(finite)),
                "q25": float(np.quantile(finite, 0.25)),
                "q75": float(np.quantile(finite, 0.75)),
                "ci95_low": float(np.quantile(finite, 0.025)),
                "ci95_high": float(np.quantile(finite, 0.975)),
            }
        )
    return out


def _probe_predictive(
    rows: List[Dict[str, object]],
    budgets: List[int],
    controller_method: str = "ours_controller_v2_nofallback",
    baseline_method: str = "hard_cap",
) -> Dict[str, Dict[str, float]]:
    out: Dict[str, Dict[str, float]] = {}
    for b in budgets:
        ctrl = [r for r in rows if int(r.get("budget_total", -1)) == int(b) and str(r.get("method")) == controller_method]
        base = [r for r in rows if int(r.get("budget_total", -1)) == int(b) and str(r.get("method")) == baseline_method]
        if not ctrl or not base:
            continue

        feat = {}
        for r in ctrl:
            tr = r.get("controller_trace") or {}
            if "agreement" in tr and tr.get("agreement") is not None:
                feat[(str(r.get("doc_id")), int(r.get("seed", -1)))] = 1.0 - float(tr.get("agreement"))

        if not feat:
            continue

        # Trial-level baseline error predictability
        scores = []
        labels = []
        for r in base:
            k = (str(r.get("doc_id")), int(r.get("seed", -1)))
            if k in feat:
                scores.append(feat[k])
                labels.append(0 if bool(r.get("is_correct", False)) else 1)
        auc_err = _auc_binary(scores, labels) if scores else float("nan")
        ece_err = _ece_binary(scores, labels, n_bins=10) if scores else float("nan")

        # Doc-level baseline disagreement > 0 predictability
        by_doc = defaultdict(list)
        for r in base:
            by_doc[str(r.get("doc_id"))].append(r.get("pred_option"))
        doc_inter = {}
        for d, ans in by_doc.items():
            vals = [a for a in ans if a is not None]
            if not vals:
                doc_inter[d] = 1.0
            else:
                cnt = Counter(vals)
                doc_inter[d] = 1.0 - (max(cnt.values()) / len(vals))

        x_doc = []
        y_doc = []
        feat_doc = defaultdict(list)
        for (d, _s), v in feat.items():
            feat_doc[d].append(v)
        for d, vals in feat_doc.items():
            if d in doc_inter:
                x_doc.append(float(np.mean(vals)))
                y_doc.append(1 if doc_inter[d] > 0 else 0)
        auc_disagree = _auc_binary(x_doc, y_doc) if x_doc else float("nan")

        out[str(b)] = {
            "controller_method": controller_method,
            "baseline_method": baseline_method,
            "n_trial_pairs": len(scores),
            "auc_probe_disagree_to_baseline_error": auc_err,
            "ece_probe_disagree_to_baseline_error": ece_err,
            "n_docs": len(x_doc),
            "auc_probe_disagree_to_baseline_disagreement_gt0": auc_disagree,
        }
    return out


def _probe_risk_calibration(
    rows: List[Dict[str, object]],
    budgets: List[int],
    controller_method: str = "ours_controller_v2_nofallback",
    baseline_method: str = "hard_cap",
    n_bins: int = 10,
) -> Dict[str, List[Dict[str, float]]]:
    out: Dict[str, List[Dict[str, float]]] = {}
    for b in budgets:
        ctrl = [r for r in rows if int(r.get("budget_total", -1)) == int(b) and str(r.get("method")) == controller_method]
        base = [r for r in rows if int(r.get("budget_total", -1)) == int(b) and str(r.get("method")) == baseline_method]
        if not ctrl or not base:
            continue

        feat = {}
        for r in ctrl:
            tr = r.get("controller_trace") or {}
            if tr.get("agreement") is not None:
                feat[(str(r.get("doc_id")), int(r.get("seed", -1)))] = 1.0 - float(tr.get("agreement"))
        if not feat:
            continue

        # trial-level risk: baseline error
        trial_pairs: List[Tuple[float, int]] = []
        for r in base:
            k = (str(r.get("doc_id")), int(r.get("seed", -1)))
            if k in feat:
                trial_pairs.append((feat[k], 0 if bool(r.get("is_correct", False)) else 1))
        if not trial_pairs:
            continue
        trial_pairs.sort(key=lambda x: x[0])

        # doc-level instability label: baseline disagreement > 0
        by_doc = defaultdict(list)
        for r in base:
            by_doc[str(r.get("doc_id"))].append(r.get("pred_option"))
        doc_inter = {}
        for d, ans in by_doc.items():
            vals = [a for a in ans if a is not None]
            if not vals:
                doc_inter[d] = 1.0
            else:
                cnt = Counter(vals)
                doc_inter[d] = 1.0 - (max(cnt.values()) / len(vals))
        doc_feat = defaultdict(list)
        for (d, _s), v in feat.items():
            doc_feat[d].append(v)
        doc_pairs: List[Tuple[float, int]] = []
        for d, vals in doc_feat.items():
            if d in doc_inter:
                doc_pairs.append((float(np.mean(vals)), 1 if doc_inter[d] > 0 else 0))

        bins: List[Dict[str, float]] = []
        n = len(trial_pairs)
        for i in range(n_bins):
            lo = int(i * n / n_bins)
            hi = int((i + 1) * n / n_bins)
            part = trial_pairs[lo:hi]
            if not part:
                continue
            s_mean = float(np.mean([x[0] for x in part]))
            err_mean = float(np.mean([x[1] for x in part]))

            # match doc-pairs by score band for instability rate
            if doc_pairs:
                s_lo = min(x[0] for x in part)
                s_hi = max(x[0] for x in part)
                dp = [x for x in doc_pairs if (x[0] >= s_lo and x[0] <= s_hi)]
                inst_mean = float(np.mean([x[1] for x in dp])) if dp else float("nan")
            else:
                inst_mean = float("nan")

            bins.append(
                {
                    "bin": i + 1,
                    "n_trials": len(part),
                    "mean_disagreement": s_mean,
                    "baseline_error_rate": err_mean,
                    "baseline_instability_rate": inst_mean,
                }
            )
        out[str(b)] = bins
    return out


def _adaptive_vs_probeonly(analysis: Dict[str, object]) -> List[Dict[str, float]]:
    budgets = sorted([int(b) for b in analysis.get("budgets", [])])
    summary = analysis.get("summary_by_budget", {})
    def pick_method(keys: List[str], prefix: str) -> str | None:
        if prefix in keys:
            return prefix
        cands = sorted([k for k in keys if k.startswith(prefix)])
        return cands[0] if cands else None

    out = []
    for b in budgets:
        sb = summary.get(str(b), {})
        keys = list(sb.keys())
        a_name = pick_method(keys, "probe_adaptive_k")
        p_name = pick_method(keys, "probe_only_fixedk")
        if a_name is None or p_name is None:
            continue
        a = sb[a_name]
        p = sb[p_name]
        out.append(
            {
                "budget": b,
                "adaptive_method": a_name,
                "probe_method": p_name,
                "delta_acc_adaptive_minus_probe": float(a["accuracy"]) - float(p["accuracy"]),
                "delta_incoh_adaptive_minus_probe": float(a["incoherence"]) - float(p["incoherence"]),
                "acc_adaptive": float(a["accuracy"]),
                "acc_probe": float(p["accuracy"]),
                "incoh_adaptive": float(a["incoherence"]),
                "incoh_probe": float(p["incoherence"]),
                "tok_adaptive": float(a["avg_total_tokens"]),
                "tok_probe": float(p["avg_total_tokens"]),
            }
        )
    return out


def _parse_fail_gating(rep_stats: Dict[str, Dict[str, Dict[str, float]]], methods: List[str], budgets: List[int]) -> List[Dict[str, float]]:
    out: List[Dict[str, float]] = []
    for b in budgets:
        vals = [float(rep_stats.get(str(b), {}).get(m, {}).get("parse_fail_rate", 0.0)) for m in methods]
        if not vals:
            continue
        out.append(
            {
                "budget": int(b),
                "max_parse_fail_rate": float(max(vals)),
                "min_parse_fail_rate": float(min(vals)),
                "spread_parse_fail_rate": float(max(vals) - min(vals)),
                "gate_ok_max_le_1pct": 1.0 if max(vals) <= 0.01 else 0.0,
                "gate_ok_spread_le_1pp": 1.0 if (max(vals) - min(vals)) <= 0.01 else 0.0,
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate detailed spend-sweep report")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    run_dir = Path(args.run_dir).resolve()
    out_path = Path(args.out).resolve() if args.out else (run_dir.parents[0] / "reports" / f"{run_dir.name}_detailed_report.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    meta = json.loads((run_dir / "run_meta.json").read_text())
    cfg = yaml.safe_load((run_dir / "config_resolved.yaml").read_text())
    analysis = json.loads((run_dir / "analysis_summary_round2.json").read_text())
    rows = _load_rows(run_dir)

    statuses = []
    for p in sorted(glob.glob(str(run_dir / "status_shard*.json"))):
        try:
            statuses.append(json.loads(Path(p).read_text()))
        except Exception:
            continue

    created = dt.datetime.strptime(meta["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    end = max(dt.datetime.strptime(s["ts"], "%Y-%m-%dT%H:%M:%SZ") for s in statuses) if statuses else created
    duration_min = (end - created).total_seconds() / 60.0

    parse_fail_total = sum(int(s.get("parse_fail", 0)) for s in statuses)
    rep_attempt_total = sum(int(s.get("parse_repair_attempted", 0)) for s in statuses)
    rep_success_total = sum(int(s.get("parse_repair_success", 0)) for s in statuses)
    hard_fail_total = sum(int(s.get("hard_fail", 0)) for s in statuses)

    methods = list(meta.get("methods", []))
    budgets = [int(b) for b in meta.get("budgets", [])]
    rep_stats = _parse_repair_stats(rows, methods, budgets)
    reason_stats = _parse_fail_reason_stats(rows, methods, budgets)
    phase = _phase_thresholds(analysis, summary_key="summary_by_budget")
    phase_excl = _phase_thresholds(analysis, summary_key="summary_by_budget_parse_excluded")
    baseline_for_probe = "hard_cap" if "hard_cap" in methods else (methods[0] if methods else "hard_cap")
    probe_pred = _probe_predictive(
        rows,
        budgets,
        controller_method="ours_controller_v2_nofallback",
        baseline_method=baseline_for_probe,
    )
    probe_cal = _probe_risk_calibration(
        rows,
        budgets,
        controller_method="ours_controller_v2_nofallback",
        baseline_method=baseline_for_probe,
        n_bins=10,
    )
    threshold_ci = _threshold_ci_bootstrap(
        analysis,
        base_method="hard_cap",
        method="ours_controller_v2_nofallback",
        summary_key="summary_by_budget",
        iters=1000,
        seed=2026,
    )
    threshold_ci_excl = _threshold_ci_bootstrap(
        analysis,
        base_method="hard_cap",
        method="ours_controller_v2_nofallback",
        summary_key="summary_by_budget_parse_excluded",
        iters=1000,
        seed=2026,
    )
    adaptive_vs_probe = _adaptive_vs_probeonly(analysis)
    summary_parse_excl = analysis.get("summary_by_budget_parse_excluded", {})
    parse_gating = _parse_fail_gating(rep_stats, methods, budgets)

    lines: List[str] = []
    lines.append(f"# {run_dir.name} Detailed Report")
    lines.append("")
    lines.append("## Run Meta")
    lines.append(f"- Run dir: `{run_dir}`")
    ds = cfg.get("dataset", {})
    lines.append(
        f"- Dataset: `{ds.get('name')}:{ds.get('config')}:{ds.get('split')}`, "
        f"`n_questions={ds.get('n_questions')}`, `sample_seed={ds.get('sample_seed')}`"
    )
    lines.append(f"- Methods: `{methods}`")
    lines.append(f"- Budgets: `{budgets}`")
    lines.append(f"- Parse policy: `{meta.get('parse_policy')}`")
    lines.append("")
    lines.append("## Reliability")
    lines.append(f"- Records: `{meta.get('expected_total_global')}` completed")
    lines.append(f"- Hard fail: `{hard_fail_total}`")
    lines.append(f"- Parse fail: `{parse_fail_total}` (`{(parse_fail_total / max(1, int(meta.get('expected_total_global', 1)))):.4%}`)")
    lines.append(
        f"- Repair success: `{rep_success_total}/{rep_attempt_total}` (`{(rep_success_total / rep_attempt_total if rep_attempt_total else 0.0):.4%}`)"
    )
    lines.append(f"- Duration: `{duration_min:.2f}` minutes")
    lines.append("")
    lines.append("## Phase Threshold")
    lines.append(f"- nofallback beats hard_cap on incoh with no acc loss first at: `{phase['threshold_nf_beats_hc_incoh_and_acc']}`")
    lines.append(f"- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `{phase['threshold_nf_beats_sc_incoh_with_acc_tol_1p']}`")
    lines.append(f"- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `{phase['threshold_nf_beats_sc_incoh_with_acc_tol_2p']}`")
    lines.append(
        f"- (parse-excluded) nofallback beats hard_cap on incoh with no acc loss first at: "
        f"`{phase_excl['threshold_nf_beats_hc_incoh_and_acc']}`"
    )
    if threshold_ci.get("n_boot", 0) > 0:
        lines.append(
            "- Threshold bootstrap (hard_cap vs nofallback, parse-included): "
            f"finite_rate=`{threshold_ci.get('finite_rate', 0.0):.3f}`, "
            f"median=`{threshold_ci.get('median', float('nan'))}`, "
            f"95% CI=`[{threshold_ci.get('ci95_low', float('nan'))}, {threshold_ci.get('ci95_high', float('nan'))}]`"
        )
    if threshold_ci_excl.get("n_boot", 0) > 0:
        lines.append(
            "- Threshold bootstrap (hard_cap vs nofallback, parse-excluded): "
            f"finite_rate=`{threshold_ci_excl.get('finite_rate', 0.0):.3f}`, "
            f"median=`{threshold_ci_excl.get('median', float('nan'))}`, "
            f"95% CI=`[{threshold_ci_excl.get('ci95_low', float('nan'))}, {threshold_ci_excl.get('ci95_high', float('nan'))}]`"
        )
    lines.append("")
    lines.append("## nofallback Delta Table")
    lines.append("| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |")
    lines.append("|---|---:|---:|---:|---:|")
    for row in phase["nf_vs_hc"]:
        b = row["budget"]
        sc_row = next((x for x in phase["nf_vs_sc"] if int(x["budget"]) == int(b)), None)
        din_sc = float(sc_row["delta_incoh"]) if sc_row else float("nan")
        dac_sc = float(sc_row["delta_acc"]) if sc_row else float("nan")
        lines.append(
            f"| {b} | {float(row['delta_incoh']):+.4f} | {float(row['delta_acc']):+.4f} | {din_sc:+.4f} | {dac_sc:+.4f} |"
        )
    lines.append("")
    if adaptive_vs_probe:
        lines.append("## Adaptive Probe vs Probe-Only")
        lines.append("| Budget | Adaptive | Probe | Δacc(adapt-probe) | Δincoh(adapt-probe) | Adapt Tok | Probe Tok |")
        lines.append("|---|---|---|---:|---:|---:|---:|")
        for r in adaptive_vs_probe:
            lines.append(
                f"| {int(r['budget'])} | {r['adaptive_method']} | {r['probe_method']} | "
                f"{r['delta_acc_adaptive_minus_probe']:+.4f} | {r['delta_incoh_adaptive_minus_probe']:+.4f} | "
                f"{r['tok_adaptive']:.1f} | {r['tok_probe']:.1f} |"
            )
        lines.append("")

    if summary_parse_excl:
        lines.append("## Parse-Fail Sensitivity (Included vs Excluded)")
        lines.append("| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |")
        lines.append("|---|---|---:|---:|---:|---:|---:|")
        for b in budgets:
            incl = analysis.get("summary_by_budget", {}).get(str(b), {})
            excl = summary_parse_excl.get(str(b), {})
            for m in methods:
                if m not in incl or m not in excl:
                    continue
                mi = incl[m]
                me = excl[m]
                lines.append(
                    f"| {b} | {m} | {float(mi.get('accuracy', 0.0)):.4f} | {float(me.get('accuracy', 0.0)):.4f} | "
                    f"{float(mi.get('incoherence', 0.0)):.4f} | {float(me.get('incoherence', 0.0)):.4f} | {int(me.get('n_docs', 0))} |"
                )
        lines.append("")

    lines.append("## Method x Budget Repair")
    lines.append("| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|")
    lines.append("|---|---|---:|---:|---:|")
    for b in budgets:
        rb = rep_stats.get(str(b), {})
        for m in methods:
            v = rb.get(m, {})
            lines.append(
                f"| {b} | {m} | {float(v.get('parse_fail_rate', 0.0)):.3f} | {float(v.get('repair_attempt_rate', 0.0)):.3f} | {float(v.get('repair_success_rate_given_attempt', 0.0)):.3f} |"
            )
    lines.append("")
    lines.append("## Method x Budget Parse-Fail Reasons")
    lines.append("| Budget | Method | no_budget_for_repair | repair_called_but_failed | invalid_format_unresolved | multi_answer_unresolved | no_answer_token |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for b in budgets:
        rb = reason_stats.get(str(b), {})
        for m in methods:
            v = rb.get(m, {})
            lines.append(
                f"| {b} | {m} | {int(v.get('reason::no_budget_for_repair', 0.0))} | "
                f"{int(v.get('reason::repair_called_but_failed', 0.0))} | "
                f"{int(v.get('reason::invalid_format_unresolved', 0.0))} | "
                f"{int(v.get('reason::multi_answer_unresolved', 0.0))} | "
                f"{int(v.get('reason::no_answer_token', 0.0))} |"
            )
    lines.append("")
    if parse_gating:
        lines.append("## Parse-Fail Gating Check")
        lines.append("| Budget | Max ParseFail | Min ParseFail | Spread | Gate(max<=1%) | Gate(spread<=1%p) |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for g in parse_gating:
            lines.append(
                f"| {int(g['budget'])} | {g['max_parse_fail_rate']:.3f} | {g['min_parse_fail_rate']:.3f} | "
                f"{g['spread_parse_fail_rate']:.3f} | {int(g['gate_ok_max_le_1pct'])} | {int(g['gate_ok_spread_le_1pp'])} |"
            )
        lines.append("")

    lines.append("## Cost Reality (Actual Total Tokens)")
    lines.append("| Budget | Method | AvgTotalTok | Accuracy | Incoherence | ParseFail |")
    lines.append("|---|---|---:|---:|---:|---:|")
    summary = analysis.get("summary_by_budget", {})
    for b in budgets:
        sb = summary.get(str(b), {})
        for m in sorted(sb.keys(), key=lambda x: float(sb[x].get("avg_total_tokens", 0.0))):
            v = sb[m]
            lines.append(
                f"| {b} | {m} | {float(v.get('avg_total_tokens', 0.0)):.1f} | {float(v.get('accuracy', 0.0)):.4f} | "
                f"{float(v.get('incoherence', 0.0)):.4f} | {float(v.get('parse_fail_rate', 0.0)):.4f} |"
            )
    lines.append("")
    lines.append("## nofallback Decision Breakdown")
    lines.append("| Budget | Stop@Probe | ContinueSolve | FallbackHardCap | ProbeShare | SolveShare | AvgProbeTok | AvgSolveTok |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    cd_all = analysis.get("controller_diagnostics_by_budget", {})
    for b in budgets:
        cd = (cd_all.get(str(b), {}) or {}).get("ours_controller_v2_nofallback", {})
        dec = cd.get("decision_counts", {})
        n = float(cd.get("n", 0) or 0)
        stop = float(dec.get("stop_after_probe", 0)) / n if n > 0 else 0.0
        cont = float(dec.get("continue_solve", 0)) / n if n > 0 else 0.0
        fb = float(dec.get("fallback_hard_cap", 0)) / n if n > 0 else 0.0
        lines.append(
            f"| {b} | {stop:.3f} | {cont:.3f} | {fb:.3f} | "
            f"{float(cd.get('probe_token_share', 0.0)):.3f} | {float(cd.get('solve_token_share', 0.0)):.3f} | "
            f"{float(cd.get('avg_probe_tokens', 0.0)):.1f} | {float(cd.get('avg_solve_tokens', 0.0)):.1f} |"
        )
    lines.append("")

    lines.append("## Probe Predictive Signal (nofallback)")
    lines.append(f"- Baseline method for labels: `{baseline_for_probe}`")
    lines.append("| Budget | n trial-pairs | AUC(disagree->base_error) | ECE(disagree->base_error) | n docs | AUC(disagree->base_disagree>0) |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for b in budgets:
        v = probe_pred.get(str(b))
        if not v:
            continue
        lines.append(
            f"| {b} | {int(v['n_trial_pairs'])} | {float(v['auc_probe_disagree_to_baseline_error']):.3f} | "
            f"{float(v.get('ece_probe_disagree_to_baseline_error', float('nan'))):.3f} | "
            f"{int(v['n_docs'])} | {float(v['auc_probe_disagree_to_baseline_disagreement_gt0']):.3f} |"
        )
    lines.append("")
    if probe_cal:
        lines.append("## Probe Risk Calibration (Deciles)")
        lines.append("| Budget | Bin | Mean Disagree | Baseline Error Rate | Baseline Instability Rate | n_trials |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for b in budgets:
            bins = probe_cal.get(str(b), [])
            for row in bins:
                lines.append(
                    f"| {b} | {int(row['bin'])} | {float(row['mean_disagreement']):.3f} | "
                    f"{float(row['baseline_error_rate']):.3f} | {float(row['baseline_instability_rate']):.3f} | "
                    f"{int(row['n_trials'])} |"
                )
        lines.append("")
    lines.append("## Source Files")
    lines.append(f"- Summary: `{run_dir / 'round2_summary.md'}`")
    lines.append(f"- Analysis JSON: `{run_dir / 'analysis_summary_round2.json'}`")

    out_path.write_text("\n".join(lines) + "\n")
    print(out_path)


if __name__ == "__main__":
    main()
