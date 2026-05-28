"""Incoherence-aware test-time compute control for multiple-choice reasoning.

This package is the experiment code for a dormant research pilot that asked:

> Given a fixed test-time compute budget on multiple-choice reasoning benchmarks
> (GPQA, MMLU), can a controller allocate compute more cleverly than uniform
> allocation by using *answer incoherence* — how much the model's answer wavers
> across multiple attempts on the same question — as the steering signal?

Main entry points:

- `src.run_pilot`            : runs the experiment (sharded across GPUs).
- `src.methods`              : the baselines and the controller variants.
- `src.parser`               : extracts the answer letter from raw generations.
- `src.token_meter`          : per-question token accounting on a consistent basis.
- `src.analyze_hotmess_style`: bias/variance/incoherence metrics + significance.
- `src.report_spend_sweep`   : cross-budget comparison tables and reports.
- `src.monitor`              : live progress watcher for an active run.

Closure summary lives in `closure_reports/`; see `GLOSSARY.md` at the repo
root for the project's internal vocabulary (`incoherence`, `spend sweep`,
`hard_cap`, `controller_v3_nofallback`, etc.).
"""
