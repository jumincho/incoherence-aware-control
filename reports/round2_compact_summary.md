# Round2 Summary

- Run dir: `/data2/chojm/incoh-pilot/runs/round2_compact_v1`
- Baseline: `baseline_longcot`
- Budgets: `[1024, 1536, 2048, 2560]`

## Budget 1024

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | ParseFail |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.3958 | 0.6042 | 0.0104 | 0.0169 | 442.1 | 0.000 |
| confidence_select | 0.4062 | 0.6250 | 0.0312 | 0.0476 | 717.5 | 0.010 |
| hard_cap | 0.4062 | 0.5833 | 0.0208 | 0.0345 | 283.4 | 0.000 |
| ours_anchor_only | 0.4062 | 0.6042 | 0.0417 | 0.0645 | 755.9 | 0.000 |
| ours_controller | 0.4062 | 0.5833 | 0.0417 | 0.0667 | 542.7 | 0.000 |
| ours_decompose_only | 0.4271 | 0.6042 | 0.0312 | 0.0492 | 723.7 | 0.000 |
| ours_full | 0.4062 | 0.6042 | 0.0417 | 0.0645 | 755.5 | 0.000 |
| self_consistency | 0.4271 | 0.5833 | 0.0208 | 0.0345 | 796.9 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|
| confidence_select | -0.0139 | -0.819 | 0.0104 | [-0.0417, 0.0729] | FAIL |
| hard_cap | -0.0208 | -1.229 | 0.0104 | [-0.0312, 0.0625] | FAIL |
| ours_anchor_only | -0.0347 | -2.049 | 0.0104 | [-0.0521, 0.0833] | FAIL |
| ours_controller | -0.0486 | -2.868 | 0.0104 | [-0.0417, 0.0729] | FAIL |
| ours_decompose_only | -0.0139 | -0.819 | 0.0312 | [-0.0312, 0.1042] | FAIL |
| ours_full | -0.0347 | -2.049 | 0.0104 | [-0.0521, 0.0833] | FAIL |
| self_consistency | -0.0069 | -0.410 | 0.0312 | [0.0000, 0.0833] | FAIL |

## Budget 1536

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | ParseFail |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.3854 | 0.5833 | 0.0312 | 0.0508 | 435.6 | 0.000 |
| confidence_select | 0.4062 | 0.5833 | 0.0417 | 0.0667 | 836.5 | 0.000 |
| hard_cap | 0.4271 | 0.5625 | 0.0104 | 0.0182 | 283.4 | 0.000 |
| ours_anchor_only | 0.3958 | 0.5625 | 0.0521 | 0.0847 | 914.0 | 0.000 |
| ours_controller | 0.3854 | 0.6042 | 0.0104 | 0.0169 | 1030.2 | 0.010 |
| ours_decompose_only | 0.4167 | 0.5625 | 0.0521 | 0.0847 | 851.7 | 0.000 |
| ours_full | 0.3854 | 0.5833 | 0.0417 | 0.0667 | 911.7 | 0.000 |
| self_consistency | 0.4167 | 0.5833 | 0.0000 | 0.0000 | 946.8 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|
| confidence_select | 0.0069 | 0.137 | 0.0208 | [-0.0417, 0.0833] | PASS |
| hard_cap | 0.0417 | 0.819 | 0.0417 | [0.0000, 0.0938] | PASS |
| ours_anchor_only | -0.0278 | -0.546 | 0.0104 | [-0.0625, 0.0729] | FAIL |
| ours_controller | 0.0417 | 0.819 | 0.0000 | [-0.0625, 0.0625] | PASS |
| ours_decompose_only | -0.0139 | -0.273 | 0.0312 | [-0.0208, 0.0938] | FAIL |
| ours_full | -0.0069 | -0.137 | 0.0000 | [-0.0729, 0.0625] | FAIL |
| self_consistency | 0.0625 | 1.229 | 0.0312 | [-0.0104, 0.0938] | PASS |

## Budget 2048

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | ParseFail |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.4271 | 0.5625 | 0.0312 | 0.0526 | 437.5 | 0.000 |
| confidence_select | 0.4167 | 0.5625 | 0.0625 | 0.1000 | 875.7 | 0.000 |
| hard_cap | 0.4167 | 0.5833 | 0.0417 | 0.0667 | 282.9 | 0.000 |
| ours_anchor_only | 0.3958 | 0.6042 | 0.0625 | 0.0938 | 1413.9 | 0.000 |
| ours_controller | 0.3854 | 0.6042 | 0.0208 | 0.0333 | 1133.6 | 0.021 |
| ours_decompose_only | 0.4479 | 0.5208 | 0.0938 | 0.1525 | 1190.2 | 0.000 |
| ours_full | 0.3958 | 0.6042 | 0.0625 | 0.0938 | 1409.4 | 0.000 |
| self_consistency | 0.4375 | 0.5833 | 0.0208 | 0.0345 | 1006.2 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|
| confidence_select | -0.0486 | -0.924 | -0.0104 | [-0.0521, 0.0208] | FAIL |
| hard_cap | -0.0208 | -0.396 | -0.0104 | [-0.0521, 0.0208] | FAIL |
| ours_anchor_only | -0.0208 | -0.396 | -0.0312 | [-0.1562, 0.0938] | FAIL |
| ours_controller | 0.0069 | 0.132 | -0.0417 | [-0.1042, 0.0000] | PASS |
| ours_decompose_only | -0.0972 | -1.847 | 0.0208 | [-0.0417, 0.0938] | FAIL |
| ours_full | -0.0208 | -0.396 | -0.0312 | [-0.1562, 0.0938] | FAIL |
| self_consistency | 0.0208 | 0.396 | 0.0104 | [0.0000, 0.0312] | PASS |

## Budget 2560

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | ParseFail |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.4271 | 0.5417 | 0.0521 | 0.0877 | 436.0 | 0.000 |
| confidence_select | 0.4271 | 0.5625 | 0.0104 | 0.0182 | 868.0 | 0.000 |
| hard_cap | 0.4062 | 0.5833 | 0.0208 | 0.0345 | 282.9 | 0.000 |
| ours_anchor_only | 0.3646 | 0.6458 | 0.0625 | 0.0882 | 1507.8 | 0.000 |
| ours_controller | 0.4062 | 0.5833 | 0.0104 | 0.0175 | 1188.8 | 0.000 |
| ours_decompose_only | 0.4167 | 0.6042 | 0.0625 | 0.0938 | 1261.6 | 0.000 |
| ours_full | 0.4271 | 0.5417 | 0.0521 | 0.0877 | 1807.6 | 0.000 |
| self_consistency | 0.4375 | 0.5625 | 0.0312 | 0.0526 | 1009.8 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|
| confidence_select | 0.0556 | 0.633 | 0.0000 | [-0.0417, 0.0521] | PASS |
| hard_cap | 0.0486 | 0.554 | -0.0208 | [-0.0521, 0.0000] | PASS |
| ours_anchor_only | 0.0069 | 0.079 | -0.0625 | [-0.1875, 0.0521] | FAIL |
| ours_controller | 0.0556 | 0.633 | -0.0208 | [-0.0625, 0.0104] | PASS |
| ours_decompose_only | 0.0208 | 0.237 | -0.0104 | [-0.0833, 0.0521] | PASS |
| ours_full | -0.0139 | -0.158 | 0.0000 | [-0.1458, 0.1458] | FAIL |
| self_consistency | 0.0417 | 0.475 | 0.0104 | [-0.0208, 0.0521] | PASS |

