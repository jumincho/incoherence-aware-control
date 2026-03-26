# Round9 Pre-registration

- Date: 2026-03-02 UTC
- Primary objective:
  - Demonstrate dynamic controller v3 contribution beyond probe-only baselines around transition budgets.

## Fixed Claims
- Primary claim: On held-out GPQA(B9), `ours_controller_v3_nofallback` improves or matches probe-only Pareto region on selected budgets while keeping incoherence below hard_cap/hard_cap_matched in transition/high regimes.
- Secondary claim: `ours_controller_v3_nofallback` improves over `hard_cap_matched` on incoherence and/or accuracy in multiple budgets.
- Repro claim: One additional benchmark (MMLU C) reproduces incoherence reduction trend vs hard-cap family.

## Data Protocol
- GPQA new pool: `Wanfq/gpqa:gpqa_main/train`, `n_questions=600`, `sample_seed=20260430`
  - A9(tuning): `subset[0:300]`, `R=3`
  - B9(held-out): `subset[300:600]`, `R=5`
- Confirm run (core budgets): B9 subset, `R=7`, budgets `{400,500,600}`.
- MMLU repro: `cais/mmlu:all/test`, `n_questions=200`, `sample_seed=20260501`, `R=3`.

## Budgets
- Main grid: `{300,350,400,450,500,600,900,1500}`
- Confirm grid: `{400,500,600}`

## Methods
- Baselines:
  - `hard_cap`, `hard_cap_matched`
  - `probe_only_fixedk_{k2,k4,k8}`
  - `probe_adaptive_k_selected` (selected on A9 only)
  - `budgeted_self_consistency`
- Ours:
  - `ours_controller_v3_nofallback`

## Controller v3 constraints (fixed)
- Probe budget cap behavior via config:
  - `probe_budget_ratio=0.35`
  - `solve_min_ratio=0.40`, `solve_min_floor=128`
- Low budget fallback disabled.
- Unified parse policy `P1R`, common formatter, strict repair reserve `64`.

## Fairness controls
- Unified token accounting (prompt+output+repair+discard+restart).
- Shared parser/repair policy across methods.
- Code-lock applied before B9/C/D execution.
- Reports include both target budgets and actual-token reality tables.
