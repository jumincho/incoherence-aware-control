# Round7 Pre-registration (A" tune + B" held-out)

## Objective
1. Main claim (Track A): verify nofallback vs hard_cap regime claim on new held-out B".
2. Secondary claim (Track B): test whether adaptive probing yields net gain over probe_only frontier under spend constraints.

## Data protocol
- New pool sampled from `Wanfq/gpqa:gpqa_main/train` with `sample_seed=20260407`.
- A": manifest indices `[0, 200)` for tuning only.
- B": manifest indices `[200, 400)` for held-out final reporting.

## Methods
- A": `hard_cap`, `ours_controller_v2_nofallback`, `probe_only_fixedk_k{2,4,6,8}`, `probe_adaptive_k_t67`, `probe_adaptive_k_t75`.
- B": `hard_cap`, `ours_controller_v2_nofallback`, `probe_only_fixedk_k4`, `probe_only_fixedk_k8`, `probe_adaptive_k_selected`.

## Budgets / Seeds
- Budgets: `{300, 400, 500, 600, 750, 900, 1200, 1500}`
- A": `R=3` seeds `{11,22,33}`
- B": `R=5` seeds `{11,22,33,44,55}`

## Common evaluation policy
- Parse policy: `P1R`
- Repair reserve: `48` tokens (all methods)
- Global accounting: total tokens include prompt/output/repair/discard/restart
- Primary metrics: Accuracy, Bias, Variance, Incoherence, ParseFail
- Secondary metrics: threshold bootstrap CI, probe predictive AUC/ECE, parse included/excluded sensitivity

## Parse-fairness gating
For any budget-level claim:
- `max(parse_fail_rate across methods) <= 1%`
- `(max - min parse_fail_rate) <= 1%p`
If either fails, mark that budget result as `interpretation_deferred_due_to_parse_skew`.

## Selection rule (A" -> B")
- Select `probe_adaptive_k_selected` from A" by:
  1) maximize mean accuracy over `{400,500,600,750,900}`,
  2) tie-break by lower mean incoherence,
  3) tie-break by lower mean parse_fail.

## Reporting commitments
- Report both threshold variants:
  - parse-included T*
  - parse-excluded T*
- Report both x-axes:
  - budget target
  - actual avg total tokens
- Keep B" frozen for reporting; any post-hoc policy edit requires new held-out split.
