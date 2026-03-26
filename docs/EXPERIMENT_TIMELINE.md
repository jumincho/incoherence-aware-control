# Experiment Timeline (Concise)

## Round Family Overview
- R1-R2: PoC + metric/accounting hardening
- R3-R4: regime map + stronger baselines + parse confound containment
- R5-R7: held-out protocol formalization + repeated confirmation
- R8: strict fairness controls + matched baseline + second benchmark reproduction
- R9: v3 controller and fresh held-out rerun

## Key Runs (latest-critical)
- Round8 tuning: `runs/round8a_tuning_splitA3_r3_v1`
- Round8 held-out: `runs/round8b_heldout_splitB3_r5_v1`
- Round8 repro: `runs/round8c_mmlu_repro_r3_v1`
- Round9 tuning: `runs/round9a_tuning_splitA9_r3_v1`
- Round9 held-out: `runs/round9b_heldout_splitB9_r5_v1`
- Round9 repro: `runs/round9c_mmlu_repro_r3_v1`
- Round9 confirm (R7): `runs/round9d_confirm_core_r7_v1`

## Method Evolution
- `ours_controller` -> `ours_controller_v2(_nofallback)` -> `ours_controller_v3_nofallback`
- Static baselines strengthened across rounds:
  - `hard_cap`
  - `hard_cap_matched`
  - `probe_only_fixedk_k{2,4,8}`
  - `budgeted_self_consistency`
  - `probe_adaptive_k_selected`

## Current Best Interpretation
- Hard-cap comparison claim: strong and reproducible in high-budget regime
- Dynamic-over-static-probe claim: still mixed, needs more targeted proof
