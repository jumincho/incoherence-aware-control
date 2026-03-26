# Round2 Summary

- Run dir: `/data2/chojm/incoh-pilot/runs/round9d_confirm_core_r7_v1`
- Baseline: `hard_cap`
- Budgets: `[400, 500, 600]`

## Budget 400

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2905 | 0.7095 | 0.1641 | 0.1878 | 254.7 | 0.637 | 0.000 |
| hard_cap_matched | 0.2934 | 0.7095 | 0.1757 | 0.1985 | 261.8 | 0.655 | 0.000 |
| ours_controller_v3_nofallback | 0.2568 | 0.7432 | 0.0000 | 0.0000 | 283.1 | 0.708 | 0.000 |
| probe_only_fixedk_k4 | 0.4035 | 0.6081 | 0.0512 | 0.0776 | 251.4 | 0.629 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0106 | -0.057 | -0.070 | 0.0029 | [-0.0125, 0.0184] | FAIL |
| ours_controller_v3_nofallback | 0.1878 | 1.000 | 1.183 | -0.0338 | [-0.0801, 0.0116] | PASS |
| probe_only_fixedk_k4 | 0.1102 | 0.587 | 0.737 | 0.1129 | [0.0241, 0.2008] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 1036 | 0.0% | 0.0% | 81.3% | 0.3% | 230.0 | 0.7 | 0.0 | `{'continue_solve': 1036}` |

## Budget 500

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.3098 | 0.6824 | 0.1853 | 0.2136 | 293.9 | 0.588 | 0.000 |
| hard_cap_matched | 0.3108 | 0.6622 | 0.2201 | 0.2495 | 326.4 | 0.653 | 0.000 |
| ours_controller_v3_nofallback | 0.2597 | 0.7432 | 0.0087 | 0.0116 | 364.1 | 0.728 | 0.000 |
| probe_only_fixedk_k4 | 0.4073 | 0.5878 | 0.0473 | 0.0745 | 329.2 | 0.658 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0359 | -0.168 | -0.254 | 0.0010 | [-0.0347, 0.0396] | FAIL |
| ours_controller_v3_nofallback | 0.2020 | 0.946 | 1.236 | -0.0502 | [-0.1062, 0.0039] | PASS |
| probe_only_fixedk_k4 | 0.1391 | 0.651 | 0.914 | 0.0975 | [0.0106, 0.1921] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 1036 | 0.0% | 0.0% | 84.0% | 1.8% | 305.7 | 6.5 | 0.9 | `{'continue_solve': 1036}` |

## Budget 600

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.3069 | 0.6892 | 0.1728 | 0.2004 | 305.1 | 0.508 | 0.000 |
| hard_cap_matched | 0.3330 | 0.6689 | 0.2066 | 0.2359 | 351.3 | 0.586 | 0.000 |
| ours_controller_v3_nofallback | 0.2510 | 0.7500 | 0.0154 | 0.0202 | 461.8 | 0.770 | 0.000 |
| probe_only_fixedk_k4 | 0.3996 | 0.6081 | 0.0473 | 0.0722 | 413.7 | 0.689 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0355 | -0.177 | -0.315 | 0.0261 | [-0.0193, 0.0734] | FAIL |
| ours_controller_v3_nofallback | 0.1803 | 0.899 | 1.172 | -0.0560 | [-0.1091, 0.0019] | PASS |
| probe_only_fixedk_k4 | 0.1283 | 0.640 | 0.884 | 0.0927 | [0.0077, 0.1824] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 1036 | 0.0% | 0.0% | 84.4% | 5.5% | 389.9 | 25.3 | 0.0 | `{'continue_solve': 1036}` |

