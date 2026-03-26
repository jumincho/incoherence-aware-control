# Round2 Summary

- Run dir: `/data2/chojm/incoh-pilot/runs/round8c_mmlu_repro_r3_v1`
- Baseline: `hard_cap`
- Budgets: `[400, 900, 1500]`

## Budget 400

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.4050 | 0.6000 | 0.1233 | 0.1705 | 183.3 | 0.458 | 0.000 |
| hard_cap_matched | 0.4050 | 0.6000 | 0.1233 | 0.1705 | 183.3 | 0.458 | 0.000 |
| ours_controller_v2_nofallback | 0.6967 | 0.3000 | 0.0117 | 0.0374 | 237.6 | 0.594 | 0.000 |
| probe_only_fixedk_k4 | 0.7017 | 0.2950 | 0.0067 | 0.0221 | 256.9 | 0.642 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | 0.0000 | 0.000 | -0.000 | 0.0000 | [0.0000, 0.0000] | FAIL |
| ours_controller_v2_nofallback | 0.1331 | 0.780 | 0.727 | 0.2917 | [0.2300, 0.3600] | FAIL |
| probe_only_fixedk_k4 | 0.1484 | 0.870 | 0.771 | 0.2967 | [0.2350, 0.3667] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 600 | 0.0% | 88.0% | 97.2% | 0.0% | 231.0 | 0.0 | 0.5 | `{'stop_after_probe': 528, 'continue_solve': 72}` |

## Budget 900

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.4200 | 0.5750 | 0.1133 | 0.1646 | 227.8 | 0.253 | 0.000 |
| hard_cap_matched | 0.4383 | 0.5650 | 0.1200 | 0.1752 | 241.1 | 0.268 | 0.000 |
| ours_controller_v2_nofallback | 0.7333 | 0.2650 | 0.0067 | 0.0245 | 379.6 | 0.422 | 0.000 |
| probe_only_fixedk_k4 | 0.7367 | 0.2650 | 0.0033 | 0.0124 | 631.6 | 0.702 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0105 | -0.064 | -0.076 | 0.0183 | [-0.0000, 0.0383] | FAIL |
| ours_controller_v2_nofallback | 0.1401 | 0.851 | 0.831 | 0.3133 | [0.2466, 0.3850] | FAIL |
| probe_only_fixedk_k4 | 0.1522 | 0.925 | 0.891 | 0.3167 | [0.2483, 0.3883] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 600 | 0.0% | 99.0% | 99.9% | 0.0% | 379.1 | 0.0 | 0.0 | `{'stop_after_probe': 594, 'continue_solve': 6}` |

## Budget 1500

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.4400 | 0.5650 | 0.1117 | 0.1650 | 228.0 | 0.152 | 0.000 |
| hard_cap_matched | 0.4650 | 0.5450 | 0.1250 | 0.1866 | 242.0 | 0.161 | 0.000 |
| ours_controller_v2_nofallback | 0.7450 | 0.2550 | 0.0050 | 0.0192 | 404.2 | 0.269 | 0.000 |
| probe_only_fixedk_k4 | 0.7350 | 0.2650 | 0.0100 | 0.0364 | 758.3 | 0.506 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0215 | -0.131 | -0.095 | 0.0250 | [0.0067, 0.0450] | FAIL |
| ours_controller_v2_nofallback | 0.1458 | 0.883 | 0.844 | 0.3050 | [0.2316, 0.3767] | FAIL |
| probe_only_fixedk_k4 | 0.1287 | 0.780 | 0.821 | 0.2950 | [0.2217, 0.3667] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 600 | 0.0% | 99.0% | 99.5% | 0.4% | 402.4 | 1.8 | 0.0 | `{'stop_after_probe': 594, 'continue_solve': 6}` |

