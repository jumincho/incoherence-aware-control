# Round5 Pre-Registration (A/B Split, Spend Sweep)

Date: 2026-02-28 (UTC)

## Scope
- Objective 1: verify whether dynamic control yields net gain over `probe_only_fixedk` in spend regimes.
- Objective 2: verify held-out reproducibility of phase threshold behavior (`T≈450`) and Pareto position.

## Data Protocol (Pseudo Held-Out)
- Fixed question pool: `Wanfq/gpqa:gpqa_main`, `n_questions=400`, `sample_seed=20260227`.
- Split A (tuning only): `manifest_index in [0, 199]`.
- Split B (report only): `manifest_index in [200, 399]`.
- No Round5-B threshold or method-variant tuning on Split B.

## Round5-A (Tuning)
- Config: `configs/round5a_tuning_splitA.yaml`
- Methods:
  - `hard_cap`
  - `probe_only_fixedk`
  - `ours_controller_v2_nofallback`
  - `ours_controller_v2_nofallback_forcecontinue`
  - `ours_controller_v2_nofallback_stopcap`
- Spend targets (`total_tokens` cap): `{300, 450, 600, 900, 1200}`
- Repeats: `R=5` (`trial_seeds=[11,22,33,44,55]`)
- Selection rule for Round5-B dynamic variant:
  - Prioritize method with lower incoherence than `probe_only_fixedk` at `T in {450,600,900}` while keeping accuracy drop <= 1.0%p.
  - If tie, choose higher accuracy at `T=900`.

## Round5-B (Held-Out Report)
- Config: `configs/round5b_heldout_splitB.yaml`
- Methods:
  - `hard_cap`
  - `budgeted_self_consistency`
  - `probe_only_fixedk`
  - `ours_controller_v2_nofallback`
  - (fixed from Round5-A) `ours_controller_v2_nofallback_forcecontinue`
- Spend targets: `{200, 300, 450, 600, 900, 1200, 1500}`
- Repeats: `R=5` (`trial_seeds=[11,22,33,44,55]`)

## Fairness Guards
- Cost metric: `total_tokens` only (prompt + output + discarded + repair).
- Stop rule: generation halts when `total_tokens` cap reached.
- Same parse policy for all methods: `P1R`.
- Repair reserve: `repair_min_remaining_tokens=16`.
- Same seed list across methods and targets.
- Same parser and same repair prompt template across methods.

## Primary Metrics
- Accuracy
- Bias, Variance, Error, Incoherence (`variance / error`)
- Parse fail rate (+ fail type table per method × target)
- Actual spend (`avg_total_tokens`) in addition to target cap

## Primary Claims to Test
- C1: There exists a transition regime around `T≈450` where `ours_controller_v2_nofallback` starts to beat `hard_cap` on incoherence.
- C2: A dynamic variant beats `probe_only_fixedk` on at least one Pareto point (accuracy vs incoherence).
- C3: Held-out Split B reproduces low-T weakness (`T=200/300`) and mid/high-T gains.

## Analysis Lock
- Analysis entrypoint: `src/analyze_hotmess_style.py`
- Spend report entrypoint: `src/report_spend_sweep.py`
- Relative incoherence improvement definition:
  - `rel_improve = (incoh_base - incoh_method) / incoh_base`

