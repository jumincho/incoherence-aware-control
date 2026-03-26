# Round2 Summary

- Run dir: `/data2/chojm/incoh-pilot/runs/round9c_mmlu_repro_r3_v1`
- Baseline: `hard_cap`
- Budgets: `[400, 900, 1500]`

## Budget 400

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.5167 | 0.4900 | 0.0433 | 0.0812 | 272.0 | 0.680 | 0.000 |
| hard_cap | 0.4267 | 0.5700 | 0.0883 | 0.1342 | 173.6 | 0.434 | 0.000 |
| hard_cap_matched | 0.4333 | 0.5700 | 0.0883 | 0.1342 | 176.3 | 0.441 | 0.000 |
| ours_controller_v3_nofallback | 0.3133 | 0.6850 | 0.0050 | 0.0072 | 299.5 | 0.749 | 0.000 |
| probe_only_fixedk_k4 | 0.7217 | 0.2800 | 0.0017 | 0.0059 | 259.8 | 0.650 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0529 | 0.394 | 0.438 | 0.0900 | [0.0367, 0.1450] | FAIL |
| hard_cap_matched | 0.0000 | 0.000 | 0.011 | 0.0067 | [0.0017, 0.0133] | FAIL |
| ours_controller_v3_nofallback | 0.1269 | 0.946 | 0.885 | -0.1133 | [-0.1867, -0.0450] | FAIL |
| probe_only_fixedk_k4 | 0.1283 | 0.956 | 0.922 | 0.2950 | [0.2250, 0.3667] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 600 | 0.0% | 0.0% | 78.0% | 5.1% | 233.5 | 15.2 | 4.5 | `{'continue_solve': 600}` |

## Budget 900

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.5400 | 0.4550 | 0.0450 | 0.0900 | 684.9 | 0.761 | 0.000 |
| hard_cap | 0.4583 | 0.5350 | 0.1150 | 0.1769 | 211.3 | 0.235 | 0.000 |
| hard_cap_matched | 0.4800 | 0.5350 | 0.1217 | 0.1853 | 219.2 | 0.244 | 0.000 |
| ours_controller_v3_nofallback | 0.7883 | 0.2150 | 0.0083 | 0.0373 | 347.8 | 0.386 | 0.000 |
| probe_only_fixedk_k4 | 0.7633 | 0.2400 | 0.0050 | 0.0204 | 617.7 | 0.686 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0869 | 0.491 | 0.519 | 0.0817 | [0.0233, 0.1400] | FAIL |
| hard_cap_matched | -0.0084 | -0.047 | 0.021 | 0.0217 | [0.0033, 0.0417] | FAIL |
| ours_controller_v3_nofallback | 0.1396 | 0.789 | 0.904 | 0.3300 | [0.2600, 0.3983] | FAIL |
| probe_only_fixedk_k4 | 0.1565 | 0.885 | 0.940 | 0.3050 | [0.2350, 0.3733] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 600 | 0.0% | 99.7% | 99.9% | 0.0% | 347.6 | 0.0 | 0.0 | `{'stop_after_probe': 598, 'continue_solve': 2}` |

## Budget 1500

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.5350 | 0.4650 | 0.0400 | 0.0792 | 800.1 | 0.533 | 0.000 |
| hard_cap | 0.4283 | 0.5650 | 0.1033 | 0.1546 | 213.0 | 0.142 | 0.000 |
| hard_cap_matched | 0.4567 | 0.5300 | 0.1083 | 0.1697 | 222.9 | 0.149 | 0.000 |
| ours_controller_v3_nofallback | 0.7867 | 0.2150 | 0.0033 | 0.0153 | 373.0 | 0.249 | 0.000 |
| probe_only_fixedk_k4 | 0.7650 | 0.2400 | 0.0067 | 0.0270 | 704.3 | 0.470 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0754 | 0.488 | 0.550 | 0.1067 | [0.0500, 0.1650] | FAIL |
| hard_cap_matched | -0.0151 | -0.098 | -0.089 | 0.0283 | [0.0083, 0.0517] | FAIL |
| ours_controller_v3_nofallback | 0.1393 | 0.901 | 0.946 | 0.3583 | [0.2883, 0.4317] | FAIL |
| probe_only_fixedk_k4 | 0.1276 | 0.825 | 0.930 | 0.3367 | [0.2667, 0.4117] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 600 | 0.0% | 100.0% | 100.0% | 0.0% | 373.0 | 0.0 | 0.0 | `{'stop_after_probe': 600}` |

