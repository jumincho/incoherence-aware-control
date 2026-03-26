# Round2 Summary

- Run dir: `/data2/chojm/incoh-pilot/runs/round2_costmatch_v1`
- Baseline: `baseline_longcot`
- Budgets: `[1024]`

## Budget 1024

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | ParseFail |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.3646 | 0.6250 | 0.0208 | 0.0323 | 431.2 | 0.000 |
| hard_cap | 0.3646 | 0.6250 | 0.0104 | 0.0164 | 266.0 | 0.000 |
| ours_controller | 0.3958 | 0.6250 | 0.0521 | 0.0769 | 261.2 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|
| hard_cap | 0.0069 | 0.215 | 0.0000 | [-0.0312, 0.0312] | PASS |
| ours_controller | -0.0069 | -0.215 | 0.0312 | [-0.0107, 0.0938] | FAIL |

