# Round6 Pre-Registration (A′/B′, Spend Sweep)

Date: 2026-02-28 (UTC)

## Objective
- Remove remaining fairness confounds (especially low-T parse-fail skew).
- Test whether adaptive probing shows net dynamic gain over fixed-k probing.
- Re-establish held-out validity with a new sample pool and new split.

## Data Protocol
- New fixed question pool:
  - `Wanfq/gpqa:gpqa_main`
  - `n_questions=400`
  - `sample_seed=20260328` (new from Round5)
- Split A′ (tuning): `manifest_index in [0,199]`
- Split B′ (held-out): `manifest_index in [200,399]`
- No retuning on B′ after A′ selection.

## Cost / Parsing Policy (all methods)
- Budget metric: `total_tokens` (prompt + output + discard + repair).
- Parse policy: `P1R`.
- Repair reserve: `repair_min_remaining_tokens=32`.
- Common formatter enforced in runtime pipeline:
  - final stored answer string normalized as `Final Answer: X` when option can be extracted.

## Round6-A (tuning)
- Config: `configs/round6a_tuning_splitAprime.yaml`
- Methods:
  - `hard_cap`
  - `probe_only_fixedk`
  - `probe_adaptive_k_t67`
  - `probe_adaptive_k_t75`
  - `probe_adaptive_k_t80`
  - `ours_controller_v2_nofallback`
- Targets: `T={200,300,400,500,600,750,900,1200,1500}`
- Repeats: `R=3`
- Selection rule for adaptive probe:
  - prioritize lower incoherence than `probe_only_fixedk` with non-inferior accuracy in `T={500,600,750,900}`;
  - tie-break by higher accuracy at `T=900`.

## Round6-B (held-out)
- Config: `configs/round6b_heldout_splitBprime.yaml`
- Methods:
  - `hard_cap`
  - `probe_only_fixedk`
  - `probe_adaptive_k_selected` (fixed from A′)
  - `ours_controller_v2_nofallback`
- Targets: `T={200,300,400,500,600,750,900,1200,1500}`
- Repeats: `R=5`

## Required Reports
- Accuracy / Bias / Variance / Incoherence.
- Method×T parse-fail matrix.
- Parse-fail sensitivity:
  - metric with parse-fail included (primary),
  - metric with parse-fail excluded (secondary).
- Threshold analysis:
  - bootstrap distribution/CI of first budget where (`Δacc>0` and `Δincoh<0`) vs `hard_cap`.
- Dynamic gain analysis:
  - `probe_adaptive_k_selected` vs `probe_only_fixedk` Pareto table.

