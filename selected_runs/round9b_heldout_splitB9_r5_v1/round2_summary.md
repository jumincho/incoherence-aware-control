# Round2 Summary

- Run dir: `/data2/chojm/incoh-pilot/runs/round9b_heldout_splitB9_r5_v1`
- Baseline: `hard_cap`
- Budgets: `[300, 350, 400, 450, 500, 600, 900, 1500]`

## Budget 300

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.3351 | 0.6622 | 0.0392 | 0.0559 | 140.1 | 0.467 | 0.000 |
| hard_cap | 0.2797 | 0.7162 | 0.0784 | 0.0986 | 142.7 | 0.476 | 0.000 |
| hard_cap_matched | 0.2838 | 0.7162 | 0.0824 | 0.1032 | 143.5 | 0.478 | 0.000 |
| ours_controller_v3_nofallback | 0.2568 | 0.7432 | 0.0000 | 0.0000 | 151.3 | 0.504 | 0.000 |
| probe_adaptive_k_selected | 0.3297 | 0.6689 | 0.0243 | 0.0351 | 150.1 | 0.500 | 0.000 |
| probe_only_fixedk_k2 | 0.3284 | 0.6689 | 0.0257 | 0.0370 | 150.1 | 0.500 | 0.000 |
| probe_only_fixedk_k4 | 0.3284 | 0.6689 | 0.0257 | 0.0370 | 150.1 | 0.500 | 0.000 |
| probe_only_fixedk_k8 | 0.3284 | 0.6689 | 0.0257 | 0.0370 | 150.1 | 0.500 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0428 | 0.434 | 0.765 | 0.0554 | [-0.0027, 0.1149] | PASS |
| hard_cap_matched | -0.0046 | -0.046 | -0.031 | 0.0041 | [0.0000, 0.0108] | FAIL |
| ours_controller_v3_nofallback | 0.0986 | 1.000 | 1.291 | -0.0230 | [-0.0703, 0.0243] | PASS |
| probe_adaptive_k_selected | 0.0636 | 0.644 | 0.829 | 0.0500 | [-0.0189, 0.1190] | PASS |
| probe_only_fixedk_k2 | 0.0617 | 0.625 | 0.807 | 0.0486 | [-0.0203, 0.1189] | PASS |
| probe_only_fixedk_k4 | 0.0617 | 0.625 | 0.807 | 0.0486 | [-0.0203, 0.1189] | PASS |
| probe_only_fixedk_k8 | 0.0617 | 0.625 | 0.807 | 0.0486 | [-0.0203, 0.1189] | PASS |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 740 | 0.0% | 0.0% | 65.3% | 0.0% | 98.9 | 0.0 | 0.0 | `{'continue_solve': 740}` |

## Budget 350

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.3419 | 0.6486 | 0.0743 | 0.1028 | 204.1 | 0.583 | 0.000 |
| hard_cap | 0.2824 | 0.7095 | 0.1365 | 0.1613 | 205.1 | 0.586 | 0.000 |
| hard_cap_matched | 0.2865 | 0.7027 | 0.1284 | 0.1545 | 207.6 | 0.593 | 0.000 |
| ours_controller_v3_nofallback | 0.2568 | 0.7432 | 0.0000 | 0.0000 | 225.4 | 0.644 | 0.000 |
| probe_adaptive_k_selected | 0.3743 | 0.6351 | 0.0419 | 0.0619 | 203.7 | 0.582 | 0.000 |
| probe_only_fixedk_k2 | 0.3743 | 0.6351 | 0.0405 | 0.0600 | 203.7 | 0.582 | 0.000 |
| probe_only_fixedk_k4 | 0.3743 | 0.6351 | 0.0405 | 0.0600 | 203.7 | 0.582 | 0.000 |
| probe_only_fixedk_k8 | 0.3743 | 0.6351 | 0.0405 | 0.0600 | 203.7 | 0.582 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0585 | 0.363 | 0.416 | 0.0595 | [0.0000, 0.1162] | FAIL |
| hard_cap_matched | 0.0069 | 0.043 | -0.005 | 0.0041 | [-0.0014, 0.0108] | FAIL |
| ours_controller_v3_nofallback | 0.1613 | 1.000 | 1.275 | -0.0257 | [-0.0743, 0.0230] | PASS |
| probe_adaptive_k_selected | 0.0995 | 0.616 | 0.914 | 0.0919 | [0.0108, 0.1770] | FAIL |
| probe_only_fixedk_k2 | 0.1013 | 0.628 | 0.921 | 0.0919 | [0.0108, 0.1770] | FAIL |
| probe_only_fixedk_k4 | 0.1013 | 0.628 | 0.921 | 0.0919 | [0.0108, 0.1770] | FAIL |
| probe_only_fixedk_k8 | 0.1013 | 0.628 | 0.921 | 0.0919 | [0.0108, 0.1770] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 740 | 0.0% | 0.0% | 76.8% | 0.0% | 173.1 | 0.0 | 0.0 | `{'continue_solve': 740}` |

## Budget 400

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.3500 | 0.6689 | 0.0946 | 0.1239 | 253.7 | 0.634 | 0.000 |
| hard_cap | 0.2892 | 0.7162 | 0.1554 | 0.1783 | 254.6 | 0.636 | 0.000 |
| hard_cap_matched | 0.2905 | 0.7095 | 0.1608 | 0.1848 | 261.7 | 0.654 | 0.000 |
| ours_controller_v3_nofallback | 0.2568 | 0.7432 | 0.0000 | 0.0000 | 283.0 | 0.708 | 0.000 |
| probe_adaptive_k_selected | 0.4027 | 0.6014 | 0.0432 | 0.0671 | 250.5 | 0.626 | 0.000 |
| probe_only_fixedk_k2 | 0.4027 | 0.6014 | 0.0432 | 0.0671 | 250.5 | 0.626 | 0.000 |
| probe_only_fixedk_k4 | 0.4027 | 0.6014 | 0.0432 | 0.0671 | 251.2 | 0.628 | 0.000 |
| probe_only_fixedk_k8 | 0.4027 | 0.6014 | 0.0432 | 0.0671 | 251.2 | 0.628 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0544 | 0.305 | 0.501 | 0.0608 | [0.0000, 0.1217] | FAIL |
| hard_cap_matched | -0.0065 | -0.036 | -0.046 | 0.0014 | [-0.0149, 0.0176] | FAIL |
| ours_controller_v3_nofallback | 0.1783 | 1.000 | 1.155 | -0.0324 | [-0.0784, 0.0135] | PASS |
| probe_adaptive_k_selected | 0.1112 | 0.624 | 0.792 | 0.1135 | [0.0216, 0.2027] | FAIL |
| probe_only_fixedk_k2 | 0.1112 | 0.624 | 0.792 | 0.1135 | [0.0216, 0.2027] | FAIL |
| probe_only_fixedk_k4 | 0.1112 | 0.624 | 0.792 | 0.1135 | [0.0216, 0.2027] | FAIL |
| probe_only_fixedk_k8 | 0.1112 | 0.624 | 0.792 | 0.1135 | [0.0216, 0.2027] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 740 | 0.0% | 0.0% | 81.3% | 0.3% | 230.0 | 0.7 | 0.0 | `{'continue_solve': 740}` |

## Budget 450

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.3432 | 0.6892 | 0.0838 | 0.1084 | 294.6 | 0.655 | 0.000 |
| hard_cap | 0.3054 | 0.7027 | 0.1608 | 0.1862 | 281.0 | 0.624 | 0.000 |
| hard_cap_matched | 0.3054 | 0.6689 | 0.1905 | 0.2217 | 300.6 | 0.668 | 0.000 |
| ours_controller_v3_nofallback | 0.2568 | 0.7432 | 0.0000 | 0.0000 | 324.8 | 0.722 | 0.000 |
| probe_adaptive_k_selected | 0.3959 | 0.6216 | 0.0581 | 0.0855 | 289.2 | 0.643 | 0.000 |
| probe_only_fixedk_k2 | 0.3959 | 0.6216 | 0.0581 | 0.0855 | 289.2 | 0.643 | 0.000 |
| probe_only_fixedk_k4 | 0.3959 | 0.6216 | 0.0581 | 0.0855 | 290.6 | 0.646 | 0.000 |
| probe_only_fixedk_k8 | 0.3959 | 0.6216 | 0.0581 | 0.0855 | 290.6 | 0.646 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0778 | 0.418 | 0.722 | 0.0378 | [-0.0203, 0.1014] | PASS |
| hard_cap_matched | -0.0355 | -0.190 | -0.254 | 0.0000 | [-0.0338, 0.0351] | FAIL |
| ours_controller_v3_nofallback | 0.1862 | 1.000 | 1.293 | -0.0486 | [-0.0986, 0.0027] | PASS |
| probe_adaptive_k_selected | 0.1007 | 0.541 | 0.922 | 0.0905 | [0.0027, 0.1797] | FAIL |
| probe_only_fixedk_k2 | 0.1007 | 0.541 | 0.922 | 0.0905 | [0.0027, 0.1797] | FAIL |
| probe_only_fixedk_k4 | 0.1007 | 0.541 | 0.922 | 0.0905 | [0.0027, 0.1797] | FAIL |
| probe_only_fixedk_k8 | 0.1007 | 0.541 | 0.922 | 0.0905 | [0.0027, 0.1797] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 740 | 0.0% | 0.0% | 83.3% | 0.5% | 270.7 | 1.6 | 0.0 | `{'continue_solve': 740}` |

## Budget 500

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.3149 | 0.6959 | 0.0919 | 0.1166 | 327.2 | 0.654 | 0.000 |
| hard_cap | 0.3203 | 0.6689 | 0.1770 | 0.2093 | 294.1 | 0.588 | 0.000 |
| hard_cap_matched | 0.3216 | 0.6486 | 0.1986 | 0.2344 | 326.6 | 0.653 | 0.000 |
| ours_controller_v3_nofallback | 0.2595 | 0.7432 | 0.0095 | 0.0126 | 364.0 | 0.728 | 0.000 |
| probe_adaptive_k_selected | 0.4081 | 0.5878 | 0.0432 | 0.0685 | 326.8 | 0.654 | 0.000 |
| probe_only_fixedk_k2 | 0.4068 | 0.5878 | 0.0446 | 0.0705 | 326.4 | 0.653 | 0.000 |
| probe_only_fixedk_k4 | 0.4068 | 0.5878 | 0.0419 | 0.0665 | 329.5 | 0.659 | 0.000 |
| probe_only_fixedk_k8 | 0.4068 | 0.5878 | 0.0419 | 0.0665 | 329.5 | 0.659 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0926 | 0.443 | 0.622 | -0.0054 | [-0.0622, 0.0568] | PASS |
| hard_cap_matched | -0.0252 | -0.120 | -0.237 | 0.0014 | [-0.0378, 0.0405] | FAIL |
| ours_controller_v3_nofallback | 0.1967 | 0.940 | 1.194 | -0.0608 | [-0.1163, -0.0040] | FAIL |
| probe_adaptive_k_selected | 0.1407 | 0.673 | 0.870 | 0.0878 | [-0.0014, 0.1851] | PASS |
| probe_only_fixedk_k2 | 0.1388 | 0.663 | 0.866 | 0.0865 | [-0.0027, 0.1825] | PASS |
| probe_only_fixedk_k4 | 0.1427 | 0.682 | 0.876 | 0.0865 | [-0.0027, 0.1825] | PASS |
| probe_only_fixedk_k8 | 0.1427 | 0.682 | 0.876 | 0.0865 | [-0.0027, 0.1825] | PASS |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 740 | 0.0% | 0.0% | 84.0% | 1.8% | 305.6 | 6.5 | 0.9 | `{'continue_solve': 740}` |

## Budget 600

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.3338 | 0.6757 | 0.1068 | 0.1364 | 417.0 | 0.695 | 0.000 |
| hard_cap | 0.2973 | 0.6959 | 0.1595 | 0.1864 | 305.0 | 0.508 | 0.000 |
| hard_cap_matched | 0.3351 | 0.6689 | 0.1905 | 0.2217 | 351.0 | 0.585 | 0.000 |
| ours_controller_v3_nofallback | 0.2500 | 0.7568 | 0.0135 | 0.0175 | 461.5 | 0.769 | 0.000 |
| probe_adaptive_k_selected | 0.3986 | 0.5878 | 0.0432 | 0.0685 | 398.7 | 0.664 | 0.000 |
| probe_only_fixedk_k2 | 0.3986 | 0.5878 | 0.0446 | 0.0705 | 398.1 | 0.663 | 0.000 |
| probe_only_fixedk_k4 | 0.3986 | 0.5878 | 0.0432 | 0.0685 | 413.8 | 0.690 | 0.000 |
| probe_only_fixedk_k8 | 0.3986 | 0.5878 | 0.0432 | 0.0685 | 413.8 | 0.690 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0500 | 0.268 | 0.426 | 0.0365 | [-0.0257, 0.0986] | PASS |
| hard_cap_matched | -0.0353 | -0.189 | -0.153 | 0.0378 | [-0.0095, 0.0865] | FAIL |
| ours_controller_v3_nofallback | 0.1689 | 0.906 | 1.100 | -0.0473 | [-0.0986, 0.0054] | PASS |
| probe_adaptive_k_selected | 0.1179 | 0.632 | 0.741 | 0.1014 | [0.0135, 0.1946] | FAIL |
| probe_only_fixedk_k2 | 0.1159 | 0.622 | 0.737 | 0.1014 | [0.0135, 0.1946] | FAIL |
| probe_only_fixedk_k4 | 0.1179 | 0.632 | 0.741 | 0.1014 | [0.0135, 0.1946] | FAIL |
| probe_only_fixedk_k8 | 0.1179 | 0.632 | 0.741 | 0.1014 | [0.0135, 0.1946] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 740 | 0.0% | 0.0% | 84.5% | 5.5% | 389.8 | 25.3 | 0.0 | `{'continue_solve': 740}` |

## Budget 900

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.3432 | 0.6689 | 0.0892 | 0.1176 | 714.3 | 0.794 | 0.000 |
| hard_cap | 0.2905 | 0.6959 | 0.1649 | 0.1915 | 313.3 | 0.348 | 0.000 |
| hard_cap_matched | 0.3189 | 0.6892 | 0.2216 | 0.2433 | 368.3 | 0.409 | 0.000 |
| ours_controller_v3_nofallback | 0.3892 | 0.6081 | 0.0324 | 0.0506 | 527.8 | 0.586 | 0.000 |
| probe_adaptive_k_selected | 0.4014 | 0.6081 | 0.0297 | 0.0466 | 558.5 | 0.621 | 0.000 |
| probe_only_fixedk_k2 | 0.4108 | 0.5811 | 0.0378 | 0.0611 | 539.2 | 0.599 | 0.000 |
| probe_only_fixedk_k4 | 0.4014 | 0.6081 | 0.0297 | 0.0466 | 707.0 | 0.786 | 0.000 |
| probe_only_fixedk_k8 | 0.4014 | 0.6081 | 0.0297 | 0.0466 | 717.7 | 0.797 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0739 | 0.386 | 0.764 | 0.0527 | [-0.0108, 0.1176] | PASS |
| hard_cap_matched | -0.0518 | -0.270 | -0.256 | 0.0284 | [-0.0176, 0.0757] | FAIL |
| ours_controller_v3_nofallback | 0.1409 | 0.736 | 1.099 | 0.0986 | [0.0095, 0.1919] | FAIL |
| probe_adaptive_k_selected | 0.1449 | 0.757 | 1.058 | 0.1108 | [0.0216, 0.2054] | FAIL |
| probe_only_fixedk_k2 | 0.1304 | 0.681 | 0.861 | 0.1203 | [0.0311, 0.2122] | FAIL |
| probe_only_fixedk_k4 | 0.1449 | 0.757 | 1.058 | 0.1108 | [0.0216, 0.2054] | FAIL |
| probe_only_fixedk_k8 | 0.1449 | 0.757 | 1.058 | 0.1108 | [0.0216, 0.2054] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 740 | 0.0% | 95.0% | 99.5% | 0.0% | 525.1 | 0.0 | 0.0 | `{'stop_after_probe': 703, 'continue_solve': 37}` |

## Budget 1500

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.3459 | 0.6689 | 0.0932 | 0.1223 | 1140.7 | 0.760 | 0.000 |
| hard_cap | 0.2946 | 0.6892 | 0.1703 | 0.1981 | 320.1 | 0.213 | 0.000 |
| hard_cap_matched | 0.3027 | 0.7027 | 0.2297 | 0.2464 | 374.4 | 0.250 | 0.000 |
| ours_controller_v3_nofallback | 0.4027 | 0.6014 | 0.0270 | 0.0430 | 588.2 | 0.392 | 0.000 |
| probe_adaptive_k_selected | 0.4054 | 0.5946 | 0.0324 | 0.0517 | 626.3 | 0.418 | 0.000 |
| probe_only_fixedk_k2 | 0.4135 | 0.5946 | 0.0432 | 0.0678 | 576.7 | 0.384 | 0.000 |
| probe_only_fixedk_k4 | 0.4095 | 0.5946 | 0.0351 | 0.0558 | 1072.1 | 0.715 | 0.000 |
| probe_only_fixedk_k8 | 0.4081 | 0.5878 | 0.0324 | 0.0523 | 1312.9 | 0.875 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| budgeted_self_consistency | 0.0758 | 0.382 | 0.501 | 0.0514 | [-0.0095, 0.1162] | PASS |
| hard_cap_matched | -0.0483 | -0.244 | -0.369 | 0.0081 | [-0.0379, 0.0554] | FAIL |
| ours_controller_v3_nofallback | 0.1551 | 0.783 | 1.000 | 0.1081 | [0.0216, 0.1946] | FAIL |
| probe_adaptive_k_selected | 0.1464 | 0.739 | 0.932 | 0.1108 | [0.0230, 0.2014] | FAIL |
| probe_only_fixedk_k2 | 0.1303 | 0.658 | 0.885 | 0.1189 | [0.0324, 0.2068] | FAIL |
| probe_only_fixedk_k4 | 0.1423 | 0.718 | 0.920 | 0.1149 | [0.0270, 0.2054] | FAIL |
| probe_only_fixedk_k8 | 0.1458 | 0.736 | 0.906 | 0.1135 | [0.0270, 0.2054] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v3_nofallback | 740 | 0.0% | 96.8% | 99.3% | 0.5% | 584.1 | 2.7 | 0.0 | `{'stop_after_probe': 716, 'continue_solve': 24}` |

