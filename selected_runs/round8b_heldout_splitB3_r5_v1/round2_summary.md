# Round2 Summary

- Run dir: `/data2/chojm/incoh-pilot/runs/round8b_heldout_splitB3_r5_v1`
- Baseline: `hard_cap`
- Budgets: `[300, 400, 500, 600, 750, 900, 1200, 1500]`

## Budget 300

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2680 | 0.7250 | 0.0840 | 0.1038 | 137.4 | 0.458 | 0.000 |
| hard_cap_matched | 0.2680 | 0.7250 | 0.0850 | 0.1049 | 137.9 | 0.460 | 0.000 |
| ours_controller_v2_nofallback | 0.2440 | 0.7650 | 0.0790 | 0.0936 | 148.4 | 0.495 | 0.000 |
| probe_adaptive_k_selected | 0.3320 | 0.6700 | 0.0370 | 0.0523 | 139.1 | 0.464 | 0.000 |
| probe_only_fixedk_k2 | 0.3300 | 0.6700 | 0.0370 | 0.0523 | 139.1 | 0.464 | 0.000 |
| probe_only_fixedk_k4 | 0.3300 | 0.6700 | 0.0370 | 0.0523 | 139.1 | 0.464 | 0.000 |
| probe_only_fixedk_k8 | 0.3300 | 0.6700 | 0.0370 | 0.0523 | 139.1 | 0.464 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0011 | -0.011 | -0.008 | 0.0000 | [0.0000, 0.0000] | FAIL |
| ours_controller_v2_nofallback | 0.0102 | 0.099 | 0.135 | -0.0240 | [-0.0550, 0.0060] | PASS |
| probe_adaptive_k_selected | 0.0515 | 0.496 | 0.555 | 0.0640 | [0.0060, 0.1210] | FAIL |
| probe_only_fixedk_k2 | 0.0515 | 0.496 | 0.555 | 0.0620 | [0.0030, 0.1190] | FAIL |
| probe_only_fixedk_k4 | 0.0515 | 0.496 | 0.555 | 0.0620 | [0.0030, 0.1190] | FAIL |
| probe_only_fixedk_k8 | 0.0515 | 0.496 | 0.555 | 0.0620 | [0.0030, 0.1190] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 1000 | 0.0% | 0.0% | 0.0% | 72.4% | 0.0 | 107.4 | 13.0 | `{'continue_solve': 1000}` |

## Budget 400

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2650 | 0.7600 | 0.1550 | 0.1694 | 243.1 | 0.608 | 0.000 |
| hard_cap_matched | 0.2650 | 0.7600 | 0.1550 | 0.1694 | 243.1 | 0.608 | 0.000 |
| ours_controller_v2_nofallback | 0.3590 | 0.6500 | 0.0460 | 0.0661 | 230.6 | 0.577 | 0.000 |
| probe_adaptive_k_selected | 0.3610 | 0.6550 | 0.0400 | 0.0576 | 238.1 | 0.595 | 0.000 |
| probe_only_fixedk_k2 | 0.3610 | 0.6550 | 0.0430 | 0.0616 | 238.1 | 0.595 | 0.000 |
| probe_only_fixedk_k4 | 0.3610 | 0.6550 | 0.0430 | 0.0616 | 238.9 | 0.597 | 0.000 |
| probe_only_fixedk_k8 | 0.3610 | 0.6550 | 0.0430 | 0.0616 | 238.9 | 0.597 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | 0.0000 | 0.000 | -0.000 | 0.0000 | [0.0000, 0.0000] | FAIL |
| ours_controller_v2_nofallback | 0.1033 | 0.610 | 0.714 | 0.0940 | [0.0270, 0.1610] | FAIL |
| probe_adaptive_k_selected | 0.1118 | 0.660 | 0.781 | 0.0960 | [0.0290, 0.1640] | FAIL |
| probe_only_fixedk_k2 | 0.1078 | 0.636 | 0.768 | 0.0960 | [0.0290, 0.1640] | FAIL |
| probe_only_fixedk_k4 | 0.1078 | 0.636 | 0.768 | 0.0960 | [0.0290, 0.1640] | FAIL |
| probe_only_fixedk_k8 | 0.1078 | 0.636 | 0.768 | 0.0960 | [0.0290, 0.1640] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 1000 | 0.0% | 78.9% | 91.8% | 0.7% | 211.8 | 1.7 | 6.7 | `{'continue_solve': 211, 'stop_after_probe': 789}` |

## Budget 500

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2780 | 0.7250 | 0.1870 | 0.2050 | 298.7 | 0.597 | 0.000 |
| hard_cap_matched | 0.2870 | 0.7150 | 0.2120 | 0.2287 | 317.2 | 0.634 | 0.000 |
| ours_controller_v2_nofallback | 0.3570 | 0.6450 | 0.0550 | 0.0786 | 316.1 | 0.632 | 0.000 |
| probe_adaptive_k_selected | 0.3550 | 0.6400 | 0.0420 | 0.0616 | 322.2 | 0.644 | 0.000 |
| probe_only_fixedk_k2 | 0.3560 | 0.6400 | 0.0430 | 0.0630 | 321.9 | 0.644 | 0.000 |
| probe_only_fixedk_k4 | 0.3550 | 0.6400 | 0.0420 | 0.0616 | 325.7 | 0.651 | 0.000 |
| probe_only_fixedk_k8 | 0.3550 | 0.6400 | 0.0420 | 0.0616 | 325.7 | 0.651 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0237 | -0.115 | -0.102 | 0.0090 | [-0.0140, 0.0310] | FAIL |
| ours_controller_v2_nofallback | 0.1265 | 0.617 | 0.886 | 0.0790 | [0.0110, 0.1480] | FAIL |
| probe_adaptive_k_selected | 0.1435 | 0.700 | 0.912 | 0.0770 | [0.0100, 0.1460] | FAIL |
| probe_only_fixedk_k2 | 0.1421 | 0.693 | 0.909 | 0.0780 | [0.0110, 0.1470] | FAIL |
| probe_only_fixedk_k4 | 0.1435 | 0.700 | 0.912 | 0.0770 | [0.0100, 0.1460] | FAIL |
| probe_only_fixedk_k8 | 0.1435 | 0.700 | 0.912 | 0.0770 | [0.0100, 0.1460] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 1000 | 0.0% | 92.2% | 97.4% | 0.0% | 307.9 | 0.0 | 4.4 | `{'stop_after_probe': 922, 'continue_solve': 78}` |

## Budget 600

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2530 | 0.7600 | 0.1830 | 0.1941 | 316.1 | 0.527 | 0.000 |
| hard_cap_matched | 0.2730 | 0.7200 | 0.2160 | 0.2308 | 354.1 | 0.590 | 0.000 |
| ours_controller_v2_nofallback | 0.3460 | 0.6600 | 0.0590 | 0.0821 | 389.5 | 0.649 | 0.000 |
| probe_adaptive_k_selected | 0.3490 | 0.6500 | 0.0390 | 0.0566 | 395.1 | 0.658 | 0.000 |
| probe_only_fixedk_k2 | 0.3470 | 0.6550 | 0.0410 | 0.0589 | 393.1 | 0.655 | 0.000 |
| probe_only_fixedk_k4 | 0.3490 | 0.6500 | 0.0390 | 0.0566 | 414.5 | 0.691 | 0.000 |
| probe_only_fixedk_k8 | 0.3490 | 0.6500 | 0.0390 | 0.0566 | 414.5 | 0.691 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0367 | -0.189 | -0.282 | 0.0200 | [-0.0120, 0.0500] | FAIL |
| ours_controller_v2_nofallback | 0.1120 | 0.577 | 0.811 | 0.0930 | [0.0240, 0.1650] | FAIL |
| probe_adaptive_k_selected | 0.1375 | 0.708 | 0.857 | 0.0960 | [0.0250, 0.1710] | FAIL |
| probe_only_fixedk_k2 | 0.1352 | 0.696 | 0.868 | 0.0940 | [0.0240, 0.1670] | FAIL |
| probe_only_fixedk_k4 | 0.1375 | 0.708 | 0.857 | 0.0960 | [0.0250, 0.1710] | FAIL |
| probe_only_fixedk_k8 | 0.1375 | 0.708 | 0.857 | 0.0960 | [0.0250, 0.1710] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 1000 | 0.0% | 92.5% | 98.9% | 0.0% | 385.1 | 0.0 | 0.5 | `{'stop_after_probe': 925, 'continue_solve': 75}` |

## Budget 750

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2440 | 0.7800 | 0.2020 | 0.2057 | 325.5 | 0.434 | 0.000 |
| hard_cap_matched | 0.2740 | 0.7350 | 0.2420 | 0.2477 | 374.2 | 0.499 | 0.000 |
| ours_controller_v2_nofallback | 0.3520 | 0.6500 | 0.0470 | 0.0674 | 482.2 | 0.643 | 0.000 |
| probe_adaptive_k_selected | 0.3530 | 0.6500 | 0.0310 | 0.0455 | 495.8 | 0.661 | 0.000 |
| probe_only_fixedk_k2 | 0.3520 | 0.6450 | 0.0380 | 0.0556 | 489.8 | 0.653 | 0.000 |
| probe_only_fixedk_k4 | 0.3550 | 0.6500 | 0.0320 | 0.0469 | 565.9 | 0.754 | 0.000 |
| probe_only_fixedk_k8 | 0.3550 | 0.6500 | 0.0320 | 0.0469 | 568.2 | 0.758 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0420 | -0.204 | -0.289 | 0.0300 | [-0.0050, 0.0650] | FAIL |
| ours_controller_v2_nofallback | 0.1383 | 0.672 | 0.901 | 0.1080 | [0.0400, 0.1780] | FAIL |
| probe_adaptive_k_selected | 0.1602 | 0.779 | 0.944 | 0.1090 | [0.0410, 0.1800] | FAIL |
| probe_only_fixedk_k2 | 0.1501 | 0.730 | 0.888 | 0.1080 | [0.0380, 0.1800] | FAIL |
| probe_only_fixedk_k4 | 0.1588 | 0.772 | 0.940 | 0.1110 | [0.0420, 0.1830] | FAIL |
| probe_only_fixedk_k8 | 0.1588 | 0.772 | 0.940 | 0.1110 | [0.0420, 0.1830] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 1000 | 0.0% | 93.8% | 99.2% | 0.0% | 478.4 | 0.0 | 0.7 | `{'stop_after_probe': 938, 'continue_solve': 62}` |

## Budget 900

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2640 | 0.7450 | 0.1720 | 0.1876 | 325.7 | 0.362 | 0.000 |
| hard_cap_matched | 0.2980 | 0.7000 | 0.2220 | 0.2408 | 379.7 | 0.422 | 0.000 |
| ours_controller_v2_nofallback | 0.3380 | 0.6650 | 0.0630 | 0.0865 | 548.8 | 0.610 | 0.000 |
| probe_adaptive_k_selected | 0.3510 | 0.6500 | 0.0380 | 0.0552 | 557.9 | 0.620 | 0.000 |
| probe_only_fixedk_k2 | 0.3550 | 0.6450 | 0.0410 | 0.0598 | 542.4 | 0.603 | 0.000 |
| probe_only_fixedk_k4 | 0.3520 | 0.6450 | 0.0370 | 0.0543 | 701.1 | 0.779 | 0.000 |
| probe_only_fixedk_k8 | 0.3520 | 0.6500 | 0.0360 | 0.0525 | 715.8 | 0.795 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0532 | -0.284 | -0.390 | 0.0340 | [-0.0030, 0.0680] | FAIL |
| ours_controller_v2_nofallback | 0.1010 | 0.539 | 0.871 | 0.0740 | [0.0080, 0.1410] | FAIL |
| probe_adaptive_k_selected | 0.1323 | 0.706 | 0.923 | 0.0870 | [0.0200, 0.1560] | FAIL |
| probe_only_fixedk_k2 | 0.1278 | 0.681 | 0.859 | 0.0910 | [0.0250, 0.1590] | FAIL |
| probe_only_fixedk_k4 | 0.1333 | 0.711 | 0.933 | 0.0880 | [0.0210, 0.1580] | FAIL |
| probe_only_fixedk_k8 | 0.1351 | 0.720 | 0.952 | 0.0880 | [0.0210, 0.1580] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 1000 | 0.0% | 91.7% | 99.0% | 0.2% | 543.5 | 1.3 | 0.0 | `{'stop_after_probe': 917, 'continue_solve': 83}` |

## Budget 1200

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2580 | 0.7450 | 0.1890 | 0.2024 | 325.0 | 0.271 | 0.000 |
| hard_cap_matched | 0.3080 | 0.6950 | 0.2390 | 0.2559 | 383.0 | 0.319 | 0.000 |
| ours_controller_v2_nofallback | 0.3400 | 0.6600 | 0.0430 | 0.0612 | 584.4 | 0.487 | 0.000 |
| probe_adaptive_k_selected | 0.3640 | 0.6250 | 0.0420 | 0.0630 | 606.5 | 0.505 | 0.000 |
| probe_only_fixedk_k2 | 0.3600 | 0.6300 | 0.0460 | 0.0680 | 569.8 | 0.475 | 0.000 |
| probe_only_fixedk_k4 | 0.3620 | 0.6250 | 0.0410 | 0.0616 | 917.4 | 0.764 | 0.000 |
| probe_only_fixedk_k8 | 0.3620 | 0.6250 | 0.0400 | 0.0602 | 1009.3 | 0.841 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0535 | -0.265 | -0.254 | 0.0500 | [0.0150, 0.0900] | FAIL |
| ours_controller_v2_nofallback | 0.1412 | 0.698 | 1.014 | 0.0820 | [0.0190, 0.1540] | FAIL |
| probe_adaptive_k_selected | 0.1394 | 0.689 | 0.918 | 0.1060 | [0.0410, 0.1800] | FAIL |
| probe_only_fixedk_k2 | 0.1343 | 0.664 | 0.882 | 0.1020 | [0.0370, 0.1750] | FAIL |
| probe_only_fixedk_k4 | 0.1408 | 0.696 | 0.921 | 0.1040 | [0.0380, 0.1780] | FAIL |
| probe_only_fixedk_k8 | 0.1422 | 0.703 | 0.925 | 0.1040 | [0.0380, 0.1780] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 1000 | 0.0% | 94.3% | 99.1% | 0.4% | 579.4 | 2.3 | 0.2 | `{'stop_after_probe': 943, 'continue_solve': 57}` |

## Budget 1500

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2580 | 0.7550 | 0.1780 | 0.1908 | 325.4 | 0.217 | 0.000 |
| hard_cap_matched | 0.2980 | 0.7100 | 0.2230 | 0.2390 | 382.6 | 0.255 | 0.000 |
| ours_controller_v2_nofallback | 0.3540 | 0.6500 | 0.0430 | 0.0620 | 611.5 | 0.408 | 0.000 |
| probe_adaptive_k_selected | 0.3520 | 0.6450 | 0.0310 | 0.0459 | 624.2 | 0.416 | 0.000 |
| probe_only_fixedk_k2 | 0.3560 | 0.6550 | 0.0480 | 0.0683 | 575.0 | 0.383 | 0.000 |
| probe_only_fixedk_k4 | 0.3510 | 0.6350 | 0.0310 | 0.0465 | 1051.4 | 0.701 | 0.000 |
| probe_only_fixedk_k8 | 0.3490 | 0.6450 | 0.0280 | 0.0416 | 1298.2 | 0.865 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap_matched | -0.0482 | -0.253 | -0.501 | 0.0400 | [0.0080, 0.0730] | FAIL |
| ours_controller_v2_nofallback | 0.1287 | 0.675 | 0.843 | 0.0960 | [0.0300, 0.1660] | FAIL |
| probe_adaptive_k_selected | 0.1449 | 0.760 | 0.800 | 0.0940 | [0.0260, 0.1640] | FAIL |
| probe_only_fixedk_k2 | 0.1225 | 0.642 | 0.755 | 0.0980 | [0.0310, 0.1650] | FAIL |
| probe_only_fixedk_k4 | 0.1442 | 0.756 | 0.742 | 0.0930 | [0.0250, 0.1620] | FAIL |
| probe_only_fixedk_k8 | 0.1492 | 0.782 | 0.812 | 0.0910 | [0.0230, 0.1610] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 1000 | 0.0% | 94.9% | 98.7% | 1.0% | 603.3 | 6.4 | 0.3 | `{'stop_after_probe': 949, 'continue_solve': 51}` |

