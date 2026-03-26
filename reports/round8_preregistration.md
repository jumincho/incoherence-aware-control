# Round8 Pre-registration

- Date: 2026-03-02 (UTC)
- Objective:
  - Goal A: T=400~750 구간에서 parse-fail gating (`max<=1%`, `spread<=1%p`) 통과.
  - Goal B: `ours_controller_v2_nofallback` vs `hard_cap_matched` 비교로 compute-only 설명을 방어.
  - Goal C: GPQA 외 1개 벤치(MMLU)에서 핵심 현상 재현 확인.

## Data Protocol
- GPQA new pool:
  - dataset: `Wanfq/gpqa:gpqa_main/train`
  - `n_questions=400`, `sample_seed=20260421`
  - A3(tuning)=`subset[0:200]`, B3(held-out)=`subset[200:400]`
- 2nd benchmark:
  - dataset: `cais/mmlu:all/test`
  - `n_questions=200`, `sample_seed=20260422`

## Fixed Evaluation Rules
- Total-token accounting: prompt + output + repair + discarded + restart.
- Parse policy: `P1R`.
- Common formatter: `Final Answer: X` output normalization.
- Repair reserve: `repair_min_remaining_tokens=64`.
- Strict reserve enforcement enabled (`enforce_strict_repair_reserve=true`).

## Methods
- GPQA A3:
  - `hard_cap`, `ours_controller_v2_nofallback`
  - `probe_only_fixedk_{k2,k4,k8}`
  - `probe_adaptive_k_{t67,t75,t80}`
- GPQA B3:
  - `hard_cap`, `hard_cap_matched`, `ours_controller_v2_nofallback`
  - `probe_only_fixedk_{k2,k4,k8}`
  - `probe_adaptive_k_selected` (chosen from A3 only)
- MMLU C:
  - `hard_cap`, `hard_cap_matched`, `ours_controller_v2_nofallback`, `probe_only_fixedk_k4`

## Budgets
- GPQA A3/B3: `{300, 400, 500, 600, 750, 900, 1200, 1500}`
- GPQA smoke: `{400, 500, 600, 750}`
- MMLU C: `{400, 900, 1500}`

## Primary Outputs
- `analysis_summary_round2.json`
- detailed report (`report_spend_sweep`)
- integrated report:
  - `/data2/chojm/incoh-pilot/reports/round8_integrated_followup_report.md`
