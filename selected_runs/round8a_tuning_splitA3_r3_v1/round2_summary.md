# Round2 Summary

- Run dir: `/data2/chojm/incoh-pilot/runs/round8a_tuning_splitA3_r3_v1`
- Baseline: `hard_cap`
- Budgets: `[300, 400, 500, 600, 750, 900, 1200, 1500]`

## Budget 300

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2717 | 0.7300 | 0.0667 | 0.0837 | 149.0 | 0.497 | 0.000 |
| ours_controller_v2_nofallback | 0.2867 | 0.7150 | 0.0733 | 0.0930 | 155.1 | 0.517 | 0.000 |
| probe_adaptive_k_t67 | 0.3250 | 0.6700 | 0.0267 | 0.0383 | 146.5 | 0.488 | 0.000 |
| probe_adaptive_k_t75 | 0.3250 | 0.6700 | 0.0267 | 0.0383 | 146.5 | 0.488 | 0.000 |
| probe_adaptive_k_t80 | 0.3250 | 0.6700 | 0.0267 | 0.0383 | 146.5 | 0.488 | 0.000 |
| probe_only_fixedk_k2 | 0.3217 | 0.6750 | 0.0267 | 0.0380 | 146.5 | 0.488 | 0.000 |
| probe_only_fixedk_k4 | 0.3217 | 0.6750 | 0.0267 | 0.0380 | 146.5 | 0.488 | 0.000 |
| probe_only_fixedk_k8 | 0.3217 | 0.6750 | 0.0267 | 0.0380 | 146.5 | 0.488 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| ours_controller_v2_nofallback | -0.0093 | -0.112 | -0.233 | 0.0150 | [-0.0133, 0.0433] | FAIL |
| probe_adaptive_k_t67 | 0.0454 | 0.543 | 0.577 | 0.0533 | [-0.0050, 0.1133] | PASS |
| probe_adaptive_k_t75 | 0.0454 | 0.543 | 0.577 | 0.0533 | [-0.0050, 0.1133] | PASS |
| probe_adaptive_k_t80 | 0.0454 | 0.543 | 0.577 | 0.0533 | [-0.0050, 0.1133] | PASS |
| probe_only_fixedk_k2 | 0.0457 | 0.546 | 0.621 | 0.0500 | [-0.0100, 0.1100] | PASS |
| probe_only_fixedk_k4 | 0.0457 | 0.546 | 0.621 | 0.0500 | [-0.0100, 0.1100] | PASS |
| probe_only_fixedk_k8 | 0.0457 | 0.546 | 0.621 | 0.0500 | [-0.0100, 0.1100] | PASS |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 600 | 0.0% | 0.0% | 0.0% | 77.8% | 0.0 | 120.7 | 9.4 | `{'continue_solve': 600}` |

## Budget 400

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2983 | 0.7000 | 0.1200 | 0.1463 | 243.2 | 0.608 | 0.000 |
| ours_controller_v2_nofallback | 0.3400 | 0.6500 | 0.0350 | 0.0511 | 218.4 | 0.546 | 0.000 |
| probe_adaptive_k_t67 | 0.3467 | 0.6550 | 0.0383 | 0.0553 | 227.9 | 0.570 | 0.000 |
| probe_adaptive_k_t75 | 0.3467 | 0.6550 | 0.0383 | 0.0553 | 227.9 | 0.570 | 0.000 |
| probe_adaptive_k_t80 | 0.3467 | 0.6550 | 0.0383 | 0.0553 | 227.9 | 0.570 | 0.000 |
| probe_only_fixedk_k2 | 0.3483 | 0.6550 | 0.0417 | 0.0598 | 227.9 | 0.570 | 0.000 |
| probe_only_fixedk_k4 | 0.3483 | 0.6550 | 0.0417 | 0.0598 | 227.9 | 0.570 | 0.000 |
| probe_only_fixedk_k8 | 0.3483 | 0.6550 | 0.0417 | 0.0598 | 227.9 | 0.570 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| ours_controller_v2_nofallback | 0.0952 | 0.651 | 0.752 | 0.0417 | [-0.0333, 0.1167] | PASS |
| probe_adaptive_k_t67 | 0.0911 | 0.622 | 0.806 | 0.0483 | [-0.0250, 0.1233] | PASS |
| probe_adaptive_k_t75 | 0.0911 | 0.622 | 0.806 | 0.0483 | [-0.0250, 0.1233] | PASS |
| probe_adaptive_k_t80 | 0.0911 | 0.622 | 0.806 | 0.0483 | [-0.0250, 0.1233] | PASS |
| probe_only_fixedk_k2 | 0.0865 | 0.591 | 0.789 | 0.0500 | [-0.0233, 0.1250] | PASS |
| probe_only_fixedk_k4 | 0.0865 | 0.591 | 0.789 | 0.0500 | [-0.0233, 0.1250] | PASS |
| probe_only_fixedk_k8 | 0.0865 | 0.591 | 0.789 | 0.0500 | [-0.0233, 0.1250] | PASS |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 600 | 0.0% | 81.0% | 93.3% | 0.8% | 203.7 | 1.7 | 3.4 | `{'stop_after_probe': 486, 'continue_solve': 114}` |

## Budget 500

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.3083 | 0.6850 | 0.1217 | 0.1508 | 279.1 | 0.558 | 0.000 |
| ours_controller_v2_nofallback | 0.3650 | 0.6400 | 0.0500 | 0.0725 | 316.3 | 0.633 | 0.000 |
| probe_adaptive_k_t67 | 0.3667 | 0.6350 | 0.0433 | 0.0639 | 322.1 | 0.644 | 0.000 |
| probe_adaptive_k_t75 | 0.3667 | 0.6350 | 0.0433 | 0.0639 | 322.1 | 0.644 | 0.000 |
| probe_adaptive_k_t80 | 0.3667 | 0.6350 | 0.0433 | 0.0639 | 322.1 | 0.644 | 0.000 |
| probe_only_fixedk_k2 | 0.3700 | 0.6300 | 0.0400 | 0.0597 | 321.4 | 0.643 | 0.000 |
| probe_only_fixedk_k4 | 0.3700 | 0.6300 | 0.0400 | 0.0597 | 325.1 | 0.650 | 0.000 |
| probe_only_fixedk_k8 | 0.3700 | 0.6300 | 0.0400 | 0.0597 | 325.1 | 0.650 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| ours_controller_v2_nofallback | 0.0784 | 0.520 | 0.612 | 0.0567 | [-0.0217, 0.1317] | PASS |
| probe_adaptive_k_t67 | 0.0869 | 0.576 | 0.703 | 0.0583 | [-0.0217, 0.1350] | PASS |
| probe_adaptive_k_t75 | 0.0869 | 0.576 | 0.703 | 0.0583 | [-0.0217, 0.1350] | PASS |
| probe_adaptive_k_t80 | 0.0869 | 0.576 | 0.703 | 0.0583 | [-0.0217, 0.1350] | PASS |
| probe_only_fixedk_k2 | 0.0911 | 0.604 | 0.719 | 0.0617 | [-0.0183, 0.1367] | PASS |
| probe_only_fixedk_k4 | 0.0911 | 0.604 | 0.719 | 0.0617 | [-0.0183, 0.1367] | PASS |
| probe_only_fixedk_k8 | 0.0911 | 0.604 | 0.719 | 0.0617 | [-0.0183, 0.1367] | PASS |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 600 | 0.0% | 87.2% | 96.0% | 0.7% | 303.6 | 2.2 | 4.3 | `{'stop_after_probe': 523, 'continue_solve': 77}` |

## Budget 600

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.3017 | 0.6950 | 0.1300 | 0.1576 | 300.0 | 0.500 | 0.000 |
| ours_controller_v2_nofallback | 0.3650 | 0.6400 | 0.0433 | 0.0634 | 393.2 | 0.655 | 0.000 |
| probe_adaptive_k_t67 | 0.3667 | 0.6300 | 0.0283 | 0.0430 | 402.8 | 0.671 | 0.000 |
| probe_adaptive_k_t75 | 0.3667 | 0.6300 | 0.0283 | 0.0430 | 402.8 | 0.671 | 0.000 |
| probe_adaptive_k_t80 | 0.3667 | 0.6300 | 0.0283 | 0.0430 | 402.8 | 0.671 | 0.000 |
| probe_only_fixedk_k2 | 0.3633 | 0.6350 | 0.0317 | 0.0475 | 400.9 | 0.668 | 0.000 |
| probe_only_fixedk_k4 | 0.3667 | 0.6300 | 0.0283 | 0.0430 | 413.9 | 0.690 | 0.000 |
| probe_only_fixedk_k8 | 0.3667 | 0.6300 | 0.0283 | 0.0430 | 413.9 | 0.690 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| ours_controller_v2_nofallback | 0.0942 | 0.598 | 0.823 | 0.0633 | [-0.0100, 0.1417] | PASS |
| probe_adaptive_k_t67 | 0.1145 | 0.727 | 0.936 | 0.0650 | [-0.0100, 0.1433] | PASS |
| probe_adaptive_k_t75 | 0.1145 | 0.727 | 0.936 | 0.0650 | [-0.0100, 0.1433] | PASS |
| probe_adaptive_k_t80 | 0.1145 | 0.727 | 0.936 | 0.0650 | [-0.0100, 0.1433] | PASS |
| probe_only_fixedk_k2 | 0.1101 | 0.699 | 0.920 | 0.0617 | [-0.0133, 0.1400] | PASS |
| probe_only_fixedk_k4 | 0.1145 | 0.727 | 0.936 | 0.0650 | [-0.0100, 0.1433] | PASS |
| probe_only_fixedk_k8 | 0.1145 | 0.727 | 0.936 | 0.0650 | [-0.0100, 0.1433] | PASS |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 600 | 0.0% | 89.2% | 98.5% | 0.0% | 387.3 | 0.0 | 0.3 | `{'stop_after_probe': 535, 'continue_solve': 65}` |

## Budget 750

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.3200 | 0.6900 | 0.1433 | 0.1720 | 316.0 | 0.421 | 0.000 |
| ours_controller_v2_nofallback | 0.3917 | 0.6050 | 0.0433 | 0.0668 | 478.3 | 0.638 | 0.000 |
| probe_adaptive_k_t67 | 0.3683 | 0.6350 | 0.0267 | 0.0403 | 494.4 | 0.659 | 0.000 |
| probe_adaptive_k_t75 | 0.3683 | 0.6350 | 0.0267 | 0.0403 | 494.4 | 0.659 | 0.000 |
| probe_adaptive_k_t80 | 0.3683 | 0.6350 | 0.0267 | 0.0403 | 494.7 | 0.660 | 0.000 |
| probe_only_fixedk_k2 | 0.3683 | 0.6400 | 0.0233 | 0.0352 | 484.0 | 0.645 | 0.000 |
| probe_only_fixedk_k4 | 0.3683 | 0.6350 | 0.0267 | 0.0403 | 570.6 | 0.761 | 0.000 |
| probe_only_fixedk_k8 | 0.3683 | 0.6350 | 0.0267 | 0.0403 | 572.1 | 0.763 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| ours_controller_v2_nofallback | 0.1052 | 0.611 | 0.702 | 0.0717 | [-0.0083, 0.1500] | PASS |
| probe_adaptive_k_t67 | 0.1317 | 0.766 | 0.856 | 0.0483 | [-0.0300, 0.1217] | PASS |
| probe_adaptive_k_t75 | 0.1317 | 0.766 | 0.856 | 0.0483 | [-0.0300, 0.1217] | PASS |
| probe_adaptive_k_t80 | 0.1317 | 0.766 | 0.856 | 0.0483 | [-0.0300, 0.1217] | PASS |
| probe_only_fixedk_k2 | 0.1368 | 0.795 | 0.890 | 0.0483 | [-0.0300, 0.1234] | PASS |
| probe_only_fixedk_k4 | 0.1317 | 0.766 | 0.856 | 0.0483 | [-0.0300, 0.1217] | PASS |
| probe_only_fixedk_k8 | 0.1317 | 0.766 | 0.856 | 0.0483 | [-0.0300, 0.1217] | PASS |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 600 | 0.0% | 90.0% | 98.8% | 0.0% | 472.6 | 0.0 | 0.5 | `{'stop_after_probe': 540, 'continue_solve': 60}` |

## Budget 900

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.3000 | 0.6950 | 0.1433 | 0.1710 | 323.3 | 0.359 | 0.000 |
| ours_controller_v2_nofallback | 0.3750 | 0.6350 | 0.0450 | 0.0662 | 528.2 | 0.587 | 0.000 |
| probe_adaptive_k_t67 | 0.3800 | 0.6200 | 0.0383 | 0.0582 | 547.9 | 0.609 | 0.000 |
| probe_adaptive_k_t75 | 0.3800 | 0.6200 | 0.0383 | 0.0582 | 547.9 | 0.609 | 0.000 |
| probe_adaptive_k_t80 | 0.3800 | 0.6200 | 0.0383 | 0.0582 | 548.7 | 0.610 | 0.000 |
| probe_only_fixedk_k2 | 0.3717 | 0.6250 | 0.0317 | 0.0482 | 521.1 | 0.579 | 0.000 |
| probe_only_fixedk_k4 | 0.3783 | 0.6200 | 0.0383 | 0.0582 | 701.3 | 0.779 | 0.000 |
| probe_only_fixedk_k8 | 0.3800 | 0.6200 | 0.0383 | 0.0582 | 710.7 | 0.790 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| ours_controller_v2_nofallback | 0.1048 | 0.613 | 0.848 | 0.0750 | [0.0017, 0.1483] | FAIL |
| probe_adaptive_k_t67 | 0.1127 | 0.659 | 0.869 | 0.0800 | [0.0033, 0.1567] | FAIL |
| probe_adaptive_k_t75 | 0.1127 | 0.659 | 0.869 | 0.0800 | [0.0033, 0.1567] | FAIL |
| probe_adaptive_k_t80 | 0.1127 | 0.659 | 0.869 | 0.0800 | [0.0033, 0.1567] | FAIL |
| probe_only_fixedk_k2 | 0.1228 | 0.718 | 0.854 | 0.0717 | [-0.0033, 0.1450] | PASS |
| probe_only_fixedk_k4 | 0.1127 | 0.659 | 0.847 | 0.0783 | [0.0016, 0.1550] | FAIL |
| probe_only_fixedk_k8 | 0.1127 | 0.659 | 0.869 | 0.0800 | [0.0033, 0.1567] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 600 | 0.0% | 92.0% | 99.0% | 0.2% | 523.1 | 0.9 | 0.0 | `{'stop_after_probe': 552, 'continue_solve': 48}` |

## Budget 1200

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.2917 | 0.7050 | 0.1350 | 0.1607 | 333.3 | 0.278 | 0.000 |
| ours_controller_v2_nofallback | 0.3850 | 0.6200 | 0.0400 | 0.0606 | 595.8 | 0.496 | 0.000 |
| probe_adaptive_k_t67 | 0.3800 | 0.6150 | 0.0233 | 0.0366 | 608.6 | 0.507 | 0.000 |
| probe_adaptive_k_t75 | 0.3800 | 0.6150 | 0.0233 | 0.0366 | 608.6 | 0.507 | 0.000 |
| probe_adaptive_k_t80 | 0.3800 | 0.6150 | 0.0233 | 0.0366 | 612.4 | 0.510 | 0.000 |
| probe_only_fixedk_k2 | 0.3750 | 0.6200 | 0.0367 | 0.0558 | 565.5 | 0.471 | 0.000 |
| probe_only_fixedk_k4 | 0.3767 | 0.6150 | 0.0283 | 0.0440 | 921.9 | 0.768 | 0.000 |
| probe_only_fixedk_k8 | 0.3783 | 0.6150 | 0.0233 | 0.0366 | 1014.0 | 0.845 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| ours_controller_v2_nofallback | 0.1001 | 0.623 | 0.773 | 0.0933 | [0.0200, 0.1683] | FAIL |
| probe_adaptive_k_t67 | 0.1242 | 0.773 | 0.842 | 0.0883 | [0.0150, 0.1633] | FAIL |
| probe_adaptive_k_t75 | 0.1242 | 0.773 | 0.842 | 0.0883 | [0.0150, 0.1633] | FAIL |
| probe_adaptive_k_t80 | 0.1242 | 0.773 | 0.842 | 0.0883 | [0.0150, 0.1633] | FAIL |
| probe_only_fixedk_k2 | 0.1049 | 0.653 | 0.756 | 0.0833 | [0.0117, 0.1567] | FAIL |
| probe_only_fixedk_k4 | 0.1167 | 0.726 | 0.795 | 0.0850 | [0.0133, 0.1600] | FAIL |
| probe_only_fixedk_k8 | 0.1242 | 0.773 | 0.818 | 0.0867 | [0.0133, 0.1600] | FAIL |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 600 | 0.0% | 94.3% | 98.6% | 1.0% | 587.3 | 6.0 | 0.8 | `{'stop_after_probe': 566, 'continue_solve': 34}` |

## Budget 1500

| Method | Accuracy | Bias | Variance | Incoherence | Avg Total Tok | Budget Util | ParseFail |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.3017 | 0.6950 | 0.1417 | 0.1693 | 333.6 | 0.222 | 0.000 |
| ours_controller_v2_nofallback | 0.3717 | 0.6300 | 0.0417 | 0.0620 | 609.9 | 0.407 | 0.000 |
| probe_adaptive_k_t67 | 0.3750 | 0.6350 | 0.0333 | 0.0499 | 635.1 | 0.423 | 0.000 |
| probe_adaptive_k_t75 | 0.3750 | 0.6350 | 0.0333 | 0.0499 | 635.1 | 0.423 | 0.000 |
| probe_adaptive_k_t80 | 0.3750 | 0.6350 | 0.0333 | 0.0499 | 649.0 | 0.433 | 0.000 |
| probe_only_fixedk_k2 | 0.3733 | 0.6300 | 0.0383 | 0.0574 | 578.3 | 0.386 | 0.000 |
| probe_only_fixedk_k4 | 0.3717 | 0.6350 | 0.0283 | 0.0427 | 1038.9 | 0.693 | 0.000 |
| probe_only_fixedk_k8 | 0.3733 | 0.6350 | 0.0283 | 0.0427 | 1313.0 | 0.875 | 0.000 |

| Method | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| ours_controller_v2_nofallback | 0.1073 | 0.634 | 0.839 | 0.0700 | [-0.0100, 0.1467] | PASS |
| probe_adaptive_k_t67 | 0.1194 | 0.705 | 0.936 | 0.0733 | [-0.0083, 0.1483] | PASS |
| probe_adaptive_k_t75 | 0.1194 | 0.705 | 0.936 | 0.0733 | [-0.0083, 0.1483] | PASS |
| probe_adaptive_k_t80 | 0.1194 | 0.705 | 0.936 | 0.0733 | [-0.0067, 0.1483] | PASS |
| probe_only_fixedk_k2 | 0.1120 | 0.661 | 0.847 | 0.0717 | [-0.0067, 0.1483] | PASS |
| probe_only_fixedk_k4 | 0.1266 | 0.748 | 0.936 | 0.0700 | [-0.0100, 0.1467] | PASS |
| probe_only_fixedk_k8 | 0.1266 | 0.748 | 0.958 | 0.0717 | [-0.0100, 0.1483] | PASS |

| Controller | N | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg Probe Tok | Avg Solve Tok | Avg Restart Tok | Decision Counts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2_nofallback | 600 | 0.0% | 95.7% | 97.9% | 2.0% | 597.3 | 12.4 | 0.0 | `{'stop_after_probe': 574, 'continue_solve': 26}` |

