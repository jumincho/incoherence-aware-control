# Pilot Summary

- Run dir: `/data2/chojm/incoh-pilot/runs/pilot_full_v1`
- Baseline: `baseline_longcot`

## Method Metrics

| Method | Accuracy | Bias | Variance | Incoherence | Avg Out Tok | Intra Flip | Inter Disagreement |
|---|---:|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.3937 | 0.5833 | 0.1484 | 0.2028 | 159.8 | 0.000 | 0.146 |
| confidence_select | 0.3521 | 0.6562 | 0.0641 | 0.0889 | 152.0 | 0.308 | 0.062 |
| hard_cap | 0.3854 | 0.6146 | 0.0458 | 0.0694 | 20.9 | 0.000 | 0.046 |
| ours_controller | 0.4042 | 0.5938 | 0.0437 | 0.0686 | 53.5 | 0.029 | 0.045 |
| ours_full | 0.3458 | 0.6250 | 0.1281 | 0.1701 | 197.7 | 0.006 | 0.145 |
| self_consistency | 0.4000 | 0.5938 | 0.0271 | 0.0436 | 272.7 | 0.244 | 0.027 |

## Baseline Comparisons

| Method | Incoh Reduction vs Base | Acc Δ (other-base) | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|
| confidence_select | 0.1553 | -0.0417 | [-0.1042, 0.0188] | PASS |
| hard_cap | 0.1705 | -0.0083 | [-0.0792, 0.0667] | PASS |
| ours_controller | 0.1620 | 0.0104 | [-0.0646, 0.0896] | PASS |
| ours_full | 0.0074 | -0.0479 | [-0.1271, 0.0334] | FAIL |
| self_consistency | 0.1837 | 0.0063 | [-0.0708, 0.0855] | PASS |
