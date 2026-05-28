"""Live progress watcher for an active `run_pilot` run.

A run produced by `src.run_pilot --gpu-shard i/N` writes per-shard JSONL
result files (`results_shard*.jsonl`) and per-shard status snapshots
(`status_shard*.json`) into `run_dir`. This module reads those files and
prints a one-line summary of:

- `completed / expected` across all shards, with a rolling ETA,
- `parse_fail_rate` and the breakdown by `PARSE_FAIL_*` type,
- average output / total tokens per row,
- coverage by `method` and by `budget_total`,
- per-shard `done` flag plus what (doc_id, seed, method, budget) it is
  currently working on.

Invoked two ways:

- One-shot: `python -m src.monitor --run-dir <run_dir>`.
- Watcher : add `--watch` and `--interval <seconds>` to keep printing
            updates until the run finishes (the per-shard `done=True` flag
            written by `run_pilot` is the source of truth for completion).

Read-only: this script never writes into `run_dir` and never decides what to
re-run; it just summarises what's already on disk.
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import time
from collections import Counter
from pathlib import Path
from typing import Dict, List


def _load_jsonl_records(paths: List[Path]) -> List[Dict[str, object]]:
    recs: List[Dict[str, object]] = []
    for path in paths:
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    recs.append(json.loads(line))
                except Exception:
                    continue
    return recs


def _parse_iso(ts: str) -> float:
    return dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()


def summarize(run_dir: Path) -> Dict[str, object]:
    meta_path = run_dir / "run_meta.json"
    meta = json.loads(meta_path.read_text()) if meta_path.exists() else {}

    result_paths = sorted(Path(p) for p in glob.glob(str(run_dir / "results_shard*.jsonl")))
    recs = _load_jsonl_records(result_paths)

    dedup = {}
    for r in recs:
        key = (r.get("doc_id"), r.get("seed"), r.get("method"), r.get("budget_total"))
        dedup[key] = r
    rows = list(dedup.values())

    completed = len(rows)
    expected = int(meta.get("expected_total_global", 0))

    by_method = Counter(r.get("method") for r in rows)
    by_budget = Counter(int(r.get("budget_total", -1)) for r in rows)

    parse_fail = sum(1 for r in rows if r.get("pred_option") is None)
    parse_fail_types = Counter((r.get("parse_fail_type") or "OK") for r in rows)

    avg_output_tokens = (
        sum(int((r.get("usage") or {}).get("output_tokens", 0)) for r in rows) / completed if completed else 0.0
    )
    avg_total_tokens = (
        sum(int((r.get("usage") or {}).get("total_tokens", 0)) for r in rows) / completed if completed else 0.0
    )

    start_ts = _parse_iso(meta.get("created_at", dt.datetime.utcnow().isoformat() + "Z")) if meta else time.time()
    elapsed = max(time.time() - start_ts, 1e-6)
    rate = completed / elapsed
    eta = ((expected - completed) / rate) if rate > 0 and expected > 0 and completed < expected else 0.0

    status_files = sorted(Path(p) for p in glob.glob(str(run_dir / "status_shard*.json")))
    shard_status = []
    for p in status_files:
        try:
            shard_status.append(json.loads(p.read_text()))
        except Exception:
            pass

    return {
        "completed": completed,
        "expected": expected,
        "progress": (completed / expected) if expected else 0.0,
        "parse_fail": parse_fail,
        "parse_fail_rate": (parse_fail / completed) if completed else 0.0,
        "parse_fail_types": dict(parse_fail_types),
        "avg_output_tokens": avg_output_tokens,
        "avg_total_tokens": avg_total_tokens,
        "rate_items_per_sec": rate,
        "eta_seconds": eta,
        "by_method": dict(sorted(by_method.items())),
        "by_budget": dict(sorted(by_budget.items())),
        "shard_status": shard_status,
    }


def print_summary(s: Dict[str, object]) -> None:
    eta_s = int(s["eta_seconds"]) if s["eta_seconds"] else 0
    print(
        f"progress={s['completed']}/{s['expected']} ({s['progress']*100:.1f}%) "
        f"parse_fail={s['parse_fail_rate']*100:.2f}% avg_out_tok={s['avg_output_tokens']:.1f} "
        f"avg_total_tok={s['avg_total_tokens']:.1f} rate={s['rate_items_per_sec']:.3f}/s eta={eta_s}s"
    )
    print("parse_fail_types:")
    for k, v in sorted(s["parse_fail_types"].items()):
        print(f"  {k}: {v}")
    print("by_budget:")
    for k, v in s["by_budget"].items():
        print(f"  {k}: {v}")
    print("by_method:")
    for k, v in s["by_method"].items():
        print(f"  {k}: {v}")
    if s["shard_status"]:
        print("shards:")
        for st in s["shard_status"]:
            shard = st.get("shard", "?")
            done = st.get("done", False)
            cur = st.get("current", {})
            cur_txt = (
                f"{cur.get('method', '-')}/{cur.get('doc_id', '-')}/"
                f"seed{cur.get('seed', '-')}/B{cur.get('budget_total', '-')}"
            )
            print(
                f"  {shard} done={done} completed={st.get('completed', 0)} "
                f"parse_fail={st.get('parse_fail', 0)} current={cur_txt}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor incoh pilot run")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval", type=int, default=1200, help="seconds")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.exists():
        raise FileNotFoundError(run_dir)

    if not args.watch:
        print_summary(summarize(run_dir))
        return

    while True:
        print(f"\n[{dt.datetime.utcnow().isoformat()}Z] monitor tick")
        print_summary(summarize(run_dir))
        time.sleep(max(1, args.interval))


if __name__ == "__main__":
    main()
