# Round2 Summary

- Run dir: `/data2/chojm/incoh-pilot/runs/round9a_tuning_splitA9_r3_v1`
- Baseline: `hard_cap`
- Budgets: `[300, 350, 400, 450, 500, 600, 900, 1500]`

## Budget 300

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.2644 | 0.7400 | 0.0300 | 0.0390 | 142.4 | 0.475 | 0.000 |
| hard_cap | 0.2289 | 0.7767 | 0.0700 | 0.0827 | 144.7 | 0.482 | 0.000 |
| ours_controller_v3_nofallback | 0.2367 | 0.7633 | 0.0000 | 0.0000 | 156.1 | 0.520 | 0.000 |
| probe_adaptive_k_t67 | 0.3078 | 0.6933 | 0.0289 | 0.0400 | 143.0 | 0.477 | 0.000 |
| probe_adaptive_k_t75 | 0.3078 | 0.6933 | 0.0289 | 0.0400 | 143.0 | 0.477 | 0.000 |
| probe_adaptive_k_t80 | 0.3078 | 0.6933 | 0.0289 | 0.0400 | 143.0 | 0.477 | 0.000 |
| probe_only_fixedk_k2 | 0.3100 | 0.6900 | 0.0278 | 0.0387 | 143.1 | 0.477 | 0.000 |
| probe_only_fixedk_k4 | 0.3100 | 0.6900 | 0.0278 | 0.0387 | 143.1 | 0.477 | 0.000 |
| probe_only_fixedk_k8 | 0.3100 | 0.6900 | 0.0278 | 0.0387 | 143.1 | 0.477 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0437 | 0.529 | 0.522 | 0.0356 | [-0.0034, 0.0756] | PASS |
| ours_controller_v3_nofallback | 0.0827 | 1.000 | 0.937 | 0.0078 | [-0.0300, 0.0467] | PASS |
| probe_adaptive_k_t67 | 0.0427 | 0.516 | 0.506 | 0.0789 | [0.0344, 0.1234] | FAIL |
| probe_adaptive_k_t75 | 0.0427 | 0.516 | 0.506 | 0.0789 | [0.0344, 0.1234] | FAIL |
| probe_adaptive_k_t80 | 0.0427 | 0.516 | 0.506 | 0.0789 | [0.0344, 0.1234] | FAIL |
| probe_only_fixedk_k2 | 0.0440 | 0.532 | 0.486 | 0.0811 | [0.0367, 0.1278] | FAIL |
| probe_only_fixedk_k4 | 0.0440 | 0.532 | 0.486 | 0.0811 | [0.0367, 0.1278] | FAIL |
| probe_only_fixedk_k8 | 0.0440 | 0.532 | 0.486 | 0.0811 | [0.0367, 0.1278] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 900 | 0.0% | 0.0% | 66.4% | 0.0% | 103.7 | 0.0 | 0.0 | `{'continue_solve': 900}` |

## Budget 350

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.2667 | 0.7400 | 0.0567 | 0.0711 | 195.8 | 0.560 | 0.000 |
| hard_cap | 0.2433 | 0.7533 | 0.0878 | 0.1044 | 202.6 | 0.579 | 0.000 |
| ours_controller_v3_nofallback | 0.2367 | 0.7633 | 0.0000 | 0.0000 | 215.2 | 0.615 | 0.000 |
| probe_adaptive_k_t67 | 0.3378 | 0.6667 | 0.0389 | 0.0551 | 201.4 | 0.576 | 0.000 |
| probe_adaptive_k_t75 | 0.3378 | 0.6667 | 0.0389 | 0.0551 | 201.4 | 0.576 | 0.000 |
| probe_adaptive_k_t80 | 0.3378 | 0.6667 | 0.0389 | 0.0551 | 201.4 | 0.576 | 0.000 |
| probe_only_fixedk_k2 | 0.3367 | 0.6667 | 0.0389 | 0.0551 | 201.5 | 0.576 | 0.000 |
| probe_only_fixedk_k4 | 0.3367 | 0.6667 | 0.0389 | 0.0551 | 201.5 | 0.576 | 0.000 |
| probe_only_fixedk_k8 | 0.3367 | 0.6667 | 0.0389 | 0.0551 | 201.5 | 0.576 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0332 | 0.318 | 0.361 | 0.0233 | [-0.0211, 0.0656] | PASS |
| ours_controller_v3_nofallback | 0.1044 | 1.000 | 1.148 | -0.0067 | [-0.0533, 0.0356] | PASS |
| probe_adaptive_k_t67 | 0.0492 | 0.472 | 0.660 | 0.0944 | [0.0367, 0.1500] | FAIL |
| probe_adaptive_k_t75 | 0.0492 | 0.472 | 0.660 | 0.0944 | [0.0367, 0.1500] | FAIL |
| probe_adaptive_k_t80 | 0.0492 | 0.472 | 0.660 | 0.0944 | [0.0367, 0.1500] | FAIL |
| probe_only_fixedk_k2 | 0.0492 | 0.472 | 0.632 | 0.0933 | [0.0356, 0.1489] | FAIL |
| probe_only_fixedk_k4 | 0.0492 | 0.472 | 0.632 | 0.0933 | [0.0356, 0.1489] | FAIL |
| probe_only_fixedk_k8 | 0.0492 | 0.472 | 0.632 | 0.0933 | [0.0356, 0.1489] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 900 | 0.0% | 0.0% | 75.6% | 0.0% | 162.7 | 0.0 | 0.0 | `{'continue_solve': 900}` |

## Budget 400

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.2722 | 0.7267 | 0.0589 | 0.0750 | 234.8 | 0.587 | 0.000 |
| hard_cap | 0.2489 | 0.7467 | 0.1078 | 0.1261 | 237.4 | 0.594 | 0.000 |
| ours_controller_v3_nofallback | 0.2367 | 0.7633 | 0.0000 | 0.0000 | 258.1 | 0.645 | 0.000 |
| probe_adaptive_k_t67 | 0.3578 | 0.6500 | 0.0378 | 0.0549 | 230.8 | 0.577 | 0.000 |
| probe_adaptive_k_t75 | 0.3578 | 0.6500 | 0.0378 | 0.0549 | 230.8 | 0.577 | 0.000 |
| probe_adaptive_k_t80 | 0.3578 | 0.6500 | 0.0378 | 0.0549 | 230.8 | 0.577 | 0.000 |
| probe_only_fixedk_k2 | 0.3578 | 0.6500 | 0.0378 | 0.0549 | 230.8 | 0.577 | 0.000 |
| probe_only_fixedk_k4 | 0.3578 | 0.6500 | 0.0378 | 0.0549 | 230.8 | 0.577 | 0.000 |
| probe_only_fixedk_k8 | 0.3578 | 0.6500 | 0.0378 | 0.0549 | 230.8 | 0.577 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0512 | 0.406 | 0.348 | 0.0233 | [-0.0189, 0.0711] | PASS |
| ours_controller_v3_nofallback | 0.1261 | 1.000 | 1.091 | -0.0122 | [-0.0544, 0.0311] | PASS |
| probe_adaptive_k_t67 | 0.0712 | 0.565 | 0.770 | 0.1089 | [0.0533, 0.1644] | FAIL |
| probe_adaptive_k_t75 | 0.0712 | 0.565 | 0.770 | 0.1089 | [0.0533, 0.1644] | FAIL |
| probe_adaptive_k_t80 | 0.0712 | 0.565 | 0.770 | 0.1089 | [0.0533, 0.1644] | FAIL |
| probe_only_fixedk_k2 | 0.0712 | 0.565 | 0.770 | 0.1089 | [0.0533, 0.1644] | FAIL |
| probe_only_fixedk_k4 | 0.0712 | 0.565 | 0.770 | 0.1089 | [0.0533, 0.1644] | FAIL |
| probe_only_fixedk_k8 | 0.0712 | 0.565 | 0.770 | 0.1089 | [0.0533, 0.1644] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 900 | 0.0% | 0.0% | 79.4% | 0.0% | 205.0 | 0.0 | 0.0 | `{'continue_solve': 900}` |

## Budget 450

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.2878 | 0.7367 | 0.0744 | 0.0918 | 275.5 | 0.612 | 0.000 |
| hard_cap | 0.2711 | 0.7433 | 0.1222 | 0.1412 | 266.9 | 0.593 | 0.000 |
| ours_controller_v3_nofallback | 0.2367 | 0.7633 | 0.0000 | 0.0000 | 318.0 | 0.707 | 0.000 |
| probe_adaptive_k_t67 | 0.3800 | 0.6200 | 0.0378 | 0.0574 | 274.7 | 0.610 | 0.000 |
| probe_adaptive_k_t75 | 0.3800 | 0.6200 | 0.0378 | 0.0574 | 274.7 | 0.610 | 0.000 |
| probe_adaptive_k_t80 | 0.3800 | 0.6200 | 0.0378 | 0.0574 | 274.7 | 0.610 | 0.000 |
| probe_only_fixedk_k2 | 0.3800 | 0.6200 | 0.0378 | 0.0574 | 274.4 | 0.610 | 0.000 |
| probe_only_fixedk_k4 | 0.3800 | 0.6200 | 0.0378 | 0.0574 | 275.8 | 0.613 | 0.000 |
| probe_only_fixedk_k8 | 0.3800 | 0.6200 | 0.0378 | 0.0574 | 275.8 | 0.613 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0494 | 0.350 | 0.479 | 0.0167 | [-0.0278, 0.0589] | PASS |
| ours_controller_v3_nofallback | 0.1412 | 1.000 | 1.065 | -0.0344 | [-0.0800, 0.0100] | PASS |
| probe_adaptive_k_t67 | 0.0838 | 0.593 | 0.687 | 0.1089 | [0.0511, 0.1656] | FAIL |
| probe_adaptive_k_t75 | 0.0838 | 0.593 | 0.687 | 0.1089 | [0.0511, 0.1656] | FAIL |
| probe_adaptive_k_t80 | 0.0838 | 0.593 | 0.687 | 0.1089 | [0.0511, 0.1656] | FAIL |
| probe_only_fixedk_k2 | 0.0838 | 0.593 | 0.687 | 0.1089 | [0.0511, 0.1656] | FAIL |
| probe_only_fixedk_k4 | 0.0838 | 0.593 | 0.687 | 0.1089 | [0.0511, 0.1656] | FAIL |
| probe_only_fixedk_k8 | 0.0838 | 0.593 | 0.687 | 0.1089 | [0.0511, 0.1656] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 900 | 0.0% | 0.0% | 83.0% | 0.6% | 263.8 | 1.9 | 0.0 | `{'continue_solve': 900}` |

## Budget 500

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.2911 | 0.7200 | 0.0844 | 0.1050 | 326.2 | 0.652 | 0.000 |
| hard_cap | 0.2644 | 0.7367 | 0.1411 | 0.1608 | 283.2 | 0.566 | 0.000 |
| ours_controller_v3_nofallback | 0.2356 | 0.7633 | 0.0022 | 0.0029 | 367.1 | 0.734 | 0.000 |
| probe_adaptive_k_t67 | 0.3833 | 0.6200 | 0.0333 | 0.0510 | 326.3 | 0.653 | 0.000 |
| probe_adaptive_k_t75 | 0.3833 | 0.6200 | 0.0333 | 0.0510 | 326.3 | 0.653 | 0.000 |
| probe_adaptive_k_t80 | 0.3833 | 0.6200 | 0.0333 | 0.0510 | 326.3 | 0.653 | 0.000 |
| probe_only_fixedk_k2 | 0.3844 | 0.6167 | 0.0344 | 0.0529 | 326.0 | 0.652 | 0.000 |
| probe_only_fixedk_k4 | 0.3856 | 0.6167 | 0.0344 | 0.0529 | 329.4 | 0.659 | 0.000 |
| probe_only_fixedk_k8 | 0.3856 | 0.6167 | 0.0344 | 0.0529 | 329.4 | 0.659 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0558 | 0.347 | 0.431 | 0.0267 | [-0.0144, 0.0678] | PASS |
| ours_controller_v3_nofallback | 0.1579 | 0.982 | 1.047 | -0.0289 | [-0.0767, 0.0189] | PASS |
| probe_adaptive_k_t67 | 0.1097 | 0.683 | 0.828 | 0.1189 | [0.0611, 0.1767] | FAIL |
| probe_adaptive_k_t75 | 0.1097 | 0.683 | 0.828 | 0.1189 | [0.0611, 0.1767] | FAIL |
| probe_adaptive_k_t80 | 0.1097 | 0.683 | 0.828 | 0.1189 | [0.0611, 0.1767] | FAIL |
| probe_only_fixedk_k2 | 0.1079 | 0.671 | 0.792 | 0.1200 | [0.0633, 0.1778] | FAIL |
| probe_only_fixedk_k4 | 0.1079 | 0.671 | 0.808 | 0.1211 | [0.0644, 0.1789] | FAIL |
| probe_only_fixedk_k8 | 0.1079 | 0.671 | 0.808 | 0.1211 | [0.0644, 0.1789] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 900 | 0.0% | 0.0% | 84.9% | 1.0% | 311.8 | 3.7 | 0.0 | `{'continue_solve': 900}` |

## Budget 600

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.2833 | 0.7267 | 0.0856 | 0.1053 | 420.9 | 0.701 | 0.000 |
| hard_cap | 0.2667 | 0.7300 | 0.1278 | 0.1490 | 306.8 | 0.511 | 0.000 |
| ours_controller_v3_nofallback | 0.2422 | 0.7567 | 0.0111 | 0.0145 | 464.3 | 0.774 | 0.000 |
| probe_adaptive_k_t67 | 0.3811 | 0.6100 | 0.0356 | 0.0551 | 406.1 | 0.677 | 0.000 |
| probe_adaptive_k_t75 | 0.3811 | 0.6100 | 0.0356 | 0.0551 | 406.1 | 0.677 | 0.000 |
| probe_adaptive_k_t80 | 0.3811 | 0.6100 | 0.0356 | 0.0551 | 406.1 | 0.677 | 0.000 |
| probe_only_fixedk_k2 | 0.3856 | 0.6067 | 0.0344 | 0.0537 | 404.8 | 0.675 | 0.000 |
| probe_only_fixedk_k4 | 0.3811 | 0.6100 | 0.0356 | 0.0551 | 420.0 | 0.700 | 0.000 |
| probe_only_fixedk_k8 | 0.3811 | 0.6100 | 0.0356 | 0.0551 | 420.0 | 0.700 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0436 | 0.293 | 0.311 | 0.0167 | [-0.0278, 0.0633] | PASS |
| ours_controller_v3_nofallback | 0.1345 | 0.903 | 0.986 | -0.0244 | [-0.0756, 0.0289] | PASS |
| probe_adaptive_k_t67 | 0.0939 | 0.630 | 0.697 | 0.1144 | [0.0544, 0.1745] | FAIL |
| probe_adaptive_k_t75 | 0.0939 | 0.630 | 0.697 | 0.1144 | [0.0544, 0.1745] | FAIL |
| probe_adaptive_k_t80 | 0.0939 | 0.630 | 0.697 | 0.1144 | [0.0544, 0.1745] | FAIL |
| probe_only_fixedk_k2 | 0.0952 | 0.639 | 0.719 | 0.1189 | [0.0578, 0.1789] | FAIL |
| probe_only_fixedk_k4 | 0.0939 | 0.630 | 0.697 | 0.1144 | [0.0544, 0.1745] | FAIL |
| probe_only_fixedk_k8 | 0.0939 | 0.630 | 0.697 | 0.1144 | [0.0544, 0.1745] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 900 | 0.0% | 0.0% | 85.4% | 3.9% | 396.4 | 17.9 | 1.5 | `{'continue_solve': 900}` |

## Budget 900

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.2778 | 0.7167 | 0.0800 | 0.1004 | 710.2 | 0.789 | 0.000 |
| hard_cap | 0.2578 | 0.7467 | 0.1567 | 0.1734 | 325.0 | 0.361 | 0.000 |
| ours_controller_v3_nofallback | 0.3800 | 0.6200 | 0.0433 | 0.0653 | 546.3 | 0.607 | 0.000 |
| probe_adaptive_k_t67 | 0.3844 | 0.6100 | 0.0289 | 0.0452 | 560.0 | 0.622 | 0.000 |
| probe_adaptive_k_t75 | 0.3844 | 0.6100 | 0.0289 | 0.0452 | 560.0 | 0.622 | 0.000 |
| probe_adaptive_k_t80 | 0.3844 | 0.6100 | 0.0289 | 0.0452 | 560.4 | 0.623 | 0.000 |
| probe_only_fixedk_k2 | 0.3822 | 0.6167 | 0.0311 | 0.0480 | 540.1 | 0.600 | 0.000 |
| probe_only_fixedk_k4 | 0.3822 | 0.6133 | 0.0300 | 0.0466 | 705.3 | 0.784 | 0.000 |
| probe_only_fixedk_k8 | 0.3844 | 0.6100 | 0.0289 | 0.0452 | 715.6 | 0.795 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0730 | 0.421 | 0.479 | 0.0200 | [-0.0267, 0.0711] | PASS |
| ours_controller_v3_nofallback | 0.1081 | 0.623 | 0.791 | 0.1222 | [0.0644, 0.1845] | FAIL |
| probe_adaptive_k_t67 | 0.1282 | 0.739 | 0.862 | 0.1267 | [0.0666, 0.1900] | FAIL |
| probe_adaptive_k_t75 | 0.1282 | 0.739 | 0.862 | 0.1267 | [0.0666, 0.1900] | FAIL |
| probe_adaptive_k_t80 | 0.1282 | 0.739 | 0.862 | 0.1267 | [0.0666, 0.1900] | FAIL |
| probe_only_fixedk_k2 | 0.1254 | 0.723 | 0.867 | 0.1244 | [0.0656, 0.1878] | FAIL |
| probe_only_fixedk_k4 | 0.1268 | 0.731 | 0.857 | 0.1244 | [0.0644, 0.1889] | FAIL |
| probe_only_fixedk_k8 | 0.1282 | 0.739 | 0.862 | 0.1267 | [0.0666, 0.1900] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 900 | 0.0% | 92.6% | 99.3% | 0.0% | 542.4 | 0.0 | 0.0 | `{'stop_after_probe': 833, 'continue_solve': 67}` |

## Budget 1500

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.2733 | 0.7267 | 0.0733 | 0.0917 | 1134.3 | 0.756 | 0.000 |
| hard_cap | 0.2678 | 0.7433 | 0.1556 | 0.1731 | 331.2 | 0.221 | 0.000 |
| ours_controller_v3_nofallback | 0.3900 | 0.6067 | 0.0378 | 0.0586 | 627.8 | 0.419 | 0.000 |
| probe_adaptive_k_t67 | 0.3989 | 0.6000 | 0.0278 | 0.0442 | 649.1 | 0.433 | 0.000 |
| probe_adaptive_k_t75 | 0.3989 | 0.6000 | 0.0278 | 0.0442 | 649.1 | 0.433 | 0.000 |
| probe_adaptive_k_t80 | 0.3989 | 0.6000 | 0.0278 | 0.0442 | 664.3 | 0.443 | 0.000 |
| probe_only_fixedk_k2 | 0.3900 | 0.6067 | 0.0344 | 0.0537 | 597.3 | 0.398 | 0.000 |
| probe_only_fixedk_k4 | 0.3944 | 0.6033 | 0.0289 | 0.0457 | 1058.9 | 0.706 | 0.000 |
| probe_only_fixedk_k8 | 0.3956 | 0.6000 | 0.0267 | 0.0426 | 1308.6 | 0.872 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0814 | 0.470 | 0.457 | 0.0056 | [-0.0389, 0.0522] | PASS |
| ours_controller_v3_nofallback | 0.1144 | 0.661 | 0.776 | 0.1222 | [0.0589, 0.1811] | FAIL |
| probe_adaptive_k_t67 | 0.1288 | 0.744 | 0.832 | 0.1311 | [0.0667, 0.1900] | FAIL |
| probe_adaptive_k_t75 | 0.1288 | 0.744 | 0.832 | 0.1311 | [0.0667, 0.1900] | FAIL |
| probe_adaptive_k_t80 | 0.1288 | 0.744 | 0.832 | 0.1311 | [0.0667, 0.1900] | FAIL |
| probe_only_fixedk_k2 | 0.1193 | 0.690 | 0.758 | 0.1222 | [0.0589, 0.1800] | FAIL |
| probe_only_fixedk_k4 | 0.1274 | 0.736 | 0.798 | 0.1267 | [0.0633, 0.1844] | FAIL |
| probe_only_fixedk_k8 | 0.1305 | 0.754 | 0.808 | 0.1278 | [0.0622, 0.1867] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 900 | 0.0% | 96.3% | 98.5% | 1.3% | 618.3 | 8.3 | 0.3 | `{'stop_after_probe': 867, 'continue_solve': 33}` |

