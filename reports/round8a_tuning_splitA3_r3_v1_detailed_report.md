# round8a_tuning_splitA3_r3_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round8a_tuning_splitA3_r3_v1`
- Dataset: `Wanfq/gpqa:200 sampled from run manifest`
- Methods: `['hard_cap', 'ours_controller_v2_nofallback', 'probe_only_fixedk_k2', 'probe_only_fixedk_k4', 'probe_only_fixedk_k8', 'probe_adaptive_k_t67', 'probe_adaptive_k_t75', 'probe_adaptive_k_t80']`
- Budgets: `[300, 400, 500, 600, 750, 900, 1200, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `38400` completed
- Hard fail: `0`
- Parse fail: `0` (`0.0000%`)
- Repair success: `3961/3961` (`100.0000%`)
- Duration: `237.60` minutes

## Phase Threshold
- nofallback beats hard_cap on incoh with no acc loss first at: `400`
- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `None`
- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `None`
- (parse-excluded) nofallback beats hard_cap on incoh with no acc loss first at: `400`
- Threshold bootstrap (hard_cap vs nofallback, parse-included): finite_rate=`1.000`, median=`400.0`, 95% CI=`[300.0, 500.0]`
- Threshold bootstrap (hard_cap vs nofallback, parse-excluded): finite_rate=`1.000`, median=`400.0`, 95% CI=`[300.0, 500.0]`

## nofallback Delta Table
| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |
|---|---:|---:|---:|---:|
| 300 | +0.0093 | +0.0150 | +nan | +nan |
| 400 | -0.0952 | +0.0417 | +nan | +nan |
| 500 | -0.0784 | +0.0567 | +nan | +nan |
| 600 | -0.0942 | +0.0633 | +nan | +nan |
| 750 | -0.1052 | +0.0717 | +nan | +nan |
| 900 | -0.1048 | +0.0750 | +nan | +nan |
| 1200 | -0.1001 | +0.0933 | +nan | +nan |
| 1500 | -0.1073 | +0.0700 | +nan | +nan |

## Adaptive Probe vs Probe-Only
| Budget | Adaptive | Probe | Δacc(adapt-probe) | Δincoh(adapt-probe) | Adapt Tok | Probe Tok |
|---|---|---|---:|---:|---:|---:|
| 300 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0033 | +0.0003 | 146.5 | 146.5 |
| 400 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | -0.0017 | -0.0045 | 227.9 | 227.9 |
| 500 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | -0.0033 | +0.0042 | 322.1 | 321.4 |
| 600 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0033 | -0.0045 | 402.8 | 400.9 |
| 750 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | -0.0000 | +0.0051 | 494.4 | 484.0 |
| 900 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0083 | +0.0100 | 547.9 | 521.1 |
| 1200 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0050 | -0.0193 | 608.6 | 565.5 |
| 1500 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0017 | -0.0075 | 635.1 | 578.3 |

## Parse-Fail Sensitivity (Included vs Excluded)
| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |
|---|---|---:|---:|---:|---:|---:|
| 300 | hard_cap | 0.2717 | 0.2717 | 0.0837 | 0.0837 | 200 |
| 300 | ours_controller_v2_nofallback | 0.2867 | 0.2867 | 0.0930 | 0.0930 | 200 |
| 300 | probe_only_fixedk_k2 | 0.3217 | 0.3217 | 0.0380 | 0.0380 | 200 |
| 300 | probe_only_fixedk_k4 | 0.3217 | 0.3217 | 0.0380 | 0.0380 | 200 |
| 300 | probe_only_fixedk_k8 | 0.3217 | 0.3217 | 0.0380 | 0.0380 | 200 |
| 300 | probe_adaptive_k_t67 | 0.3250 | 0.3250 | 0.0383 | 0.0383 | 200 |
| 300 | probe_adaptive_k_t75 | 0.3250 | 0.3250 | 0.0383 | 0.0383 | 200 |
| 300 | probe_adaptive_k_t80 | 0.3250 | 0.3250 | 0.0383 | 0.0383 | 200 |
| 400 | hard_cap | 0.2983 | 0.2983 | 0.1463 | 0.1463 | 200 |
| 400 | ours_controller_v2_nofallback | 0.3400 | 0.3400 | 0.0511 | 0.0511 | 200 |
| 400 | probe_only_fixedk_k2 | 0.3483 | 0.3483 | 0.0598 | 0.0598 | 200 |
| 400 | probe_only_fixedk_k4 | 0.3483 | 0.3483 | 0.0598 | 0.0598 | 200 |
| 400 | probe_only_fixedk_k8 | 0.3483 | 0.3483 | 0.0598 | 0.0598 | 200 |
| 400 | probe_adaptive_k_t67 | 0.3467 | 0.3467 | 0.0553 | 0.0553 | 200 |
| 400 | probe_adaptive_k_t75 | 0.3467 | 0.3467 | 0.0553 | 0.0553 | 200 |
| 400 | probe_adaptive_k_t80 | 0.3467 | 0.3467 | 0.0553 | 0.0553 | 200 |
| 500 | hard_cap | 0.3083 | 0.3083 | 0.1508 | 0.1508 | 200 |
| 500 | ours_controller_v2_nofallback | 0.3650 | 0.3650 | 0.0725 | 0.0725 | 200 |
| 500 | probe_only_fixedk_k2 | 0.3700 | 0.3700 | 0.0597 | 0.0597 | 200 |
| 500 | probe_only_fixedk_k4 | 0.3700 | 0.3700 | 0.0597 | 0.0597 | 200 |
| 500 | probe_only_fixedk_k8 | 0.3700 | 0.3700 | 0.0597 | 0.0597 | 200 |
| 500 | probe_adaptive_k_t67 | 0.3667 | 0.3667 | 0.0639 | 0.0639 | 200 |
| 500 | probe_adaptive_k_t75 | 0.3667 | 0.3667 | 0.0639 | 0.0639 | 200 |
| 500 | probe_adaptive_k_t80 | 0.3667 | 0.3667 | 0.0639 | 0.0639 | 200 |
| 600 | hard_cap | 0.3017 | 0.3017 | 0.1576 | 0.1576 | 200 |
| 600 | ours_controller_v2_nofallback | 0.3650 | 0.3650 | 0.0634 | 0.0634 | 200 |
| 600 | probe_only_fixedk_k2 | 0.3633 | 0.3633 | 0.0475 | 0.0475 | 200 |
| 600 | probe_only_fixedk_k4 | 0.3667 | 0.3667 | 0.0430 | 0.0430 | 200 |
| 600 | probe_only_fixedk_k8 | 0.3667 | 0.3667 | 0.0430 | 0.0430 | 200 |
| 600 | probe_adaptive_k_t67 | 0.3667 | 0.3667 | 0.0430 | 0.0430 | 200 |
| 600 | probe_adaptive_k_t75 | 0.3667 | 0.3667 | 0.0430 | 0.0430 | 200 |
| 600 | probe_adaptive_k_t80 | 0.3667 | 0.3667 | 0.0430 | 0.0430 | 200 |
| 750 | hard_cap | 0.3200 | 0.3200 | 0.1720 | 0.1720 | 200 |
| 750 | ours_controller_v2_nofallback | 0.3917 | 0.3917 | 0.0668 | 0.0668 | 200 |
| 750 | probe_only_fixedk_k2 | 0.3683 | 0.3683 | 0.0352 | 0.0352 | 200 |
| 750 | probe_only_fixedk_k4 | 0.3683 | 0.3683 | 0.0403 | 0.0403 | 200 |
| 750 | probe_only_fixedk_k8 | 0.3683 | 0.3683 | 0.0403 | 0.0403 | 200 |
| 750 | probe_adaptive_k_t67 | 0.3683 | 0.3683 | 0.0403 | 0.0403 | 200 |
| 750 | probe_adaptive_k_t75 | 0.3683 | 0.3683 | 0.0403 | 0.0403 | 200 |
| 750 | probe_adaptive_k_t80 | 0.3683 | 0.3683 | 0.0403 | 0.0403 | 200 |
| 900 | hard_cap | 0.3000 | 0.3000 | 0.1710 | 0.1710 | 200 |
| 900 | ours_controller_v2_nofallback | 0.3750 | 0.3750 | 0.0662 | 0.0662 | 200 |
| 900 | probe_only_fixedk_k2 | 0.3717 | 0.3717 | 0.0482 | 0.0482 | 200 |
| 900 | probe_only_fixedk_k4 | 0.3783 | 0.3783 | 0.0582 | 0.0582 | 200 |
| 900 | probe_only_fixedk_k8 | 0.3800 | 0.3800 | 0.0582 | 0.0582 | 200 |
| 900 | probe_adaptive_k_t67 | 0.3800 | 0.3800 | 0.0582 | 0.0582 | 200 |
| 900 | probe_adaptive_k_t75 | 0.3800 | 0.3800 | 0.0582 | 0.0582 | 200 |
| 900 | probe_adaptive_k_t80 | 0.3800 | 0.3800 | 0.0582 | 0.0582 | 200 |
| 1200 | hard_cap | 0.2917 | 0.2917 | 0.1607 | 0.1607 | 200 |
| 1200 | ours_controller_v2_nofallback | 0.3850 | 0.3850 | 0.0606 | 0.0606 | 200 |
| 1200 | probe_only_fixedk_k2 | 0.3750 | 0.3750 | 0.0558 | 0.0558 | 200 |
| 1200 | probe_only_fixedk_k4 | 0.3767 | 0.3767 | 0.0440 | 0.0440 | 200 |
| 1200 | probe_only_fixedk_k8 | 0.3783 | 0.3783 | 0.0366 | 0.0366 | 200 |
| 1200 | probe_adaptive_k_t67 | 0.3800 | 0.3800 | 0.0366 | 0.0366 | 200 |
| 1200 | probe_adaptive_k_t75 | 0.3800 | 0.3800 | 0.0366 | 0.0366 | 200 |
| 1200 | probe_adaptive_k_t80 | 0.3800 | 0.3800 | 0.0366 | 0.0366 | 200 |
| 1500 | hard_cap | 0.3017 | 0.3017 | 0.1693 | 0.1693 | 200 |
| 1500 | ours_controller_v2_nofallback | 0.3717 | 0.3717 | 0.0620 | 0.0620 | 200 |
| 1500 | probe_only_fixedk_k2 | 0.3733 | 0.3733 | 0.0574 | 0.0574 | 200 |
| 1500 | probe_only_fixedk_k4 | 0.3717 | 0.3717 | 0.0427 | 0.0427 | 200 |
| 1500 | probe_only_fixedk_k8 | 0.3733 | 0.3733 | 0.0427 | 0.0427 | 200 |
| 1500 | probe_adaptive_k_t67 | 0.3750 | 0.3750 | 0.0499 | 0.0499 | 200 |
| 1500 | probe_adaptive_k_t75 | 0.3750 | 0.3750 | 0.0499 | 0.0499 | 200 |
| 1500 | probe_adaptive_k_t80 | 0.3750 | 0.3750 | 0.0499 | 0.0499 | 200 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 300 | hard_cap | 0.000 | 0.475 | 1.000 |
| 300 | ours_controller_v2_nofallback | 0.000 | 0.465 | 1.000 |
| 300 | probe_only_fixedk_k2 | 0.000 | 0.470 | 1.000 |
| 300 | probe_only_fixedk_k4 | 0.000 | 0.470 | 1.000 |
| 300 | probe_only_fixedk_k8 | 0.000 | 0.470 | 1.000 |
| 300 | probe_adaptive_k_t67 | 0.000 | 0.470 | 1.000 |
| 300 | probe_adaptive_k_t75 | 0.000 | 0.470 | 1.000 |
| 300 | probe_adaptive_k_t80 | 0.000 | 0.470 | 1.000 |
| 400 | hard_cap | 0.000 | 0.175 | 1.000 |
| 400 | ours_controller_v2_nofallback | 0.000 | 0.180 | 1.000 |
| 400 | probe_only_fixedk_k2 | 0.000 | 0.165 | 1.000 |
| 400 | probe_only_fixedk_k4 | 0.000 | 0.165 | 1.000 |
| 400 | probe_only_fixedk_k8 | 0.000 | 0.165 | 1.000 |
| 400 | probe_adaptive_k_t67 | 0.000 | 0.165 | 1.000 |
| 400 | probe_adaptive_k_t75 | 0.000 | 0.165 | 1.000 |
| 400 | probe_adaptive_k_t80 | 0.000 | 0.165 | 1.000 |
| 500 | hard_cap | 0.000 | 0.085 | 1.000 |
| 500 | ours_controller_v2_nofallback | 0.000 | 0.118 | 1.000 |
| 500 | probe_only_fixedk_k2 | 0.000 | 0.075 | 1.000 |
| 500 | probe_only_fixedk_k4 | 0.000 | 0.075 | 1.000 |
| 500 | probe_only_fixedk_k8 | 0.000 | 0.075 | 1.000 |
| 500 | probe_adaptive_k_t67 | 0.000 | 0.075 | 1.000 |
| 500 | probe_adaptive_k_t75 | 0.000 | 0.075 | 1.000 |
| 500 | probe_adaptive_k_t80 | 0.000 | 0.075 | 1.000 |
| 600 | hard_cap | 0.000 | 0.045 | 1.000 |
| 600 | ours_controller_v2_nofallback | 0.000 | 0.108 | 1.000 |
| 600 | probe_only_fixedk_k2 | 0.000 | 0.045 | 1.000 |
| 600 | probe_only_fixedk_k4 | 0.000 | 0.045 | 1.000 |
| 600 | probe_only_fixedk_k8 | 0.000 | 0.045 | 1.000 |
| 600 | probe_adaptive_k_t67 | 0.000 | 0.045 | 1.000 |
| 600 | probe_adaptive_k_t75 | 0.000 | 0.045 | 1.000 |
| 600 | probe_adaptive_k_t80 | 0.000 | 0.045 | 1.000 |
| 750 | hard_cap | 0.000 | 0.020 | 1.000 |
| 750 | ours_controller_v2_nofallback | 0.000 | 0.097 | 1.000 |
| 750 | probe_only_fixedk_k2 | 0.000 | 0.020 | 1.000 |
| 750 | probe_only_fixedk_k4 | 0.000 | 0.020 | 1.000 |
| 750 | probe_only_fixedk_k8 | 0.000 | 0.020 | 1.000 |
| 750 | probe_adaptive_k_t67 | 0.000 | 0.020 | 1.000 |
| 750 | probe_adaptive_k_t75 | 0.000 | 0.020 | 1.000 |
| 750 | probe_adaptive_k_t80 | 0.000 | 0.020 | 1.000 |
| 900 | hard_cap | 0.000 | 0.010 | 1.000 |
| 900 | ours_controller_v2_nofallback | 0.000 | 0.078 | 1.000 |
| 900 | probe_only_fixedk_k2 | 0.000 | 0.010 | 1.000 |
| 900 | probe_only_fixedk_k4 | 0.000 | 0.010 | 1.000 |
| 900 | probe_only_fixedk_k8 | 0.000 | 0.010 | 1.000 |
| 900 | probe_adaptive_k_t67 | 0.000 | 0.010 | 1.000 |
| 900 | probe_adaptive_k_t75 | 0.000 | 0.010 | 1.000 |
| 900 | probe_adaptive_k_t80 | 0.000 | 0.010 | 1.000 |
| 1200 | hard_cap | 0.000 | 0.000 | 0.000 |
| 1200 | ours_controller_v2_nofallback | 0.000 | 0.032 | 1.000 |
| 1200 | probe_only_fixedk_k2 | 0.000 | 0.000 | 0.000 |
| 1200 | probe_only_fixedk_k4 | 0.000 | 0.000 | 0.000 |
| 1200 | probe_only_fixedk_k8 | 0.000 | 0.000 | 0.000 |
| 1200 | probe_adaptive_k_t67 | 0.000 | 0.000 | 0.000 |
| 1200 | probe_adaptive_k_t75 | 0.000 | 0.000 | 0.000 |
| 1200 | probe_adaptive_k_t80 | 0.000 | 0.000 | 0.000 |
| 1500 | hard_cap | 0.000 | 0.000 | 0.000 |
| 1500 | ours_controller_v2_nofallback | 0.000 | 0.003 | 1.000 |
| 1500 | probe_only_fixedk_k2 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_only_fixedk_k4 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_only_fixedk_k8 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_adaptive_k_t67 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_adaptive_k_t75 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_adaptive_k_t80 | 0.000 | 0.000 | 0.000 |

## Method x Budget Parse-Fail Reasons
| Budget | Method | no_budget_for_repair | repair_called_but_failed | invalid_format_unresolved | multi_answer_unresolved | no_answer_token |
|---|---|---:|---:|---:|---:|---:|
| 300 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 300 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 400 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 400 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 500 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 600 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 600 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 750 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 750 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 750 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 750 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 750 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 750 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 750 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 750 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 900 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 900 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 1200 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 1200 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 1200 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 1200 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 1200 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 1200 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 1200 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 1200 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 1500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 1500 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |

## Parse-Fail Gating Check
| Budget | Max ParseFail | Min ParseFail | Spread | Gate(max<=1%) | Gate(spread<=1%p) |
|---|---:|---:|---:|---:|---:|
| 300 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 400 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 500 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 600 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 750 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 900 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 1200 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 1500 | 0.000 | 0.000 | 0.000 | 1 | 1 |

## Cost Reality (Actual Total Tokens)
| Budget | Method | AvgTotalTok | Accuracy | Incoherence | ParseFail |
|---|---|---:|---:|---:|---:|
| 300 | probe_adaptive_k_t67 | 146.5 | 0.3250 | 0.0383 | 0.0000 |
| 300 | probe_adaptive_k_t75 | 146.5 | 0.3250 | 0.0383 | 0.0000 |
| 300 | probe_adaptive_k_t80 | 146.5 | 0.3250 | 0.0383 | 0.0000 |
| 300 | probe_only_fixedk_k2 | 146.5 | 0.3217 | 0.0380 | 0.0000 |
| 300 | probe_only_fixedk_k4 | 146.5 | 0.3217 | 0.0380 | 0.0000 |
| 300 | probe_only_fixedk_k8 | 146.5 | 0.3217 | 0.0380 | 0.0000 |
| 300 | hard_cap | 149.0 | 0.2717 | 0.0837 | 0.0000 |
| 300 | ours_controller_v2_nofallback | 155.1 | 0.2867 | 0.0930 | 0.0000 |
| 400 | ours_controller_v2_nofallback | 218.4 | 0.3400 | 0.0511 | 0.0000 |
| 400 | probe_only_fixedk_k2 | 227.9 | 0.3483 | 0.0598 | 0.0000 |
| 400 | probe_only_fixedk_k4 | 227.9 | 0.3483 | 0.0598 | 0.0000 |
| 400 | probe_only_fixedk_k8 | 227.9 | 0.3483 | 0.0598 | 0.0000 |
| 400 | probe_adaptive_k_t67 | 227.9 | 0.3467 | 0.0553 | 0.0000 |
| 400 | probe_adaptive_k_t75 | 227.9 | 0.3467 | 0.0553 | 0.0000 |
| 400 | probe_adaptive_k_t80 | 227.9 | 0.3467 | 0.0553 | 0.0000 |
| 400 | hard_cap | 243.2 | 0.2983 | 0.1463 | 0.0000 |
| 500 | hard_cap | 279.1 | 0.3083 | 0.1508 | 0.0000 |
| 500 | ours_controller_v2_nofallback | 316.3 | 0.3650 | 0.0725 | 0.0000 |
| 500 | probe_only_fixedk_k2 | 321.4 | 0.3700 | 0.0597 | 0.0000 |
| 500 | probe_adaptive_k_t67 | 322.1 | 0.3667 | 0.0639 | 0.0000 |
| 500 | probe_adaptive_k_t75 | 322.1 | 0.3667 | 0.0639 | 0.0000 |
| 500 | probe_adaptive_k_t80 | 322.1 | 0.3667 | 0.0639 | 0.0000 |
| 500 | probe_only_fixedk_k4 | 325.1 | 0.3700 | 0.0597 | 0.0000 |
| 500 | probe_only_fixedk_k8 | 325.1 | 0.3700 | 0.0597 | 0.0000 |
| 600 | hard_cap | 300.0 | 0.3017 | 0.1576 | 0.0000 |
| 600 | ours_controller_v2_nofallback | 393.2 | 0.3650 | 0.0634 | 0.0000 |
| 600 | probe_only_fixedk_k2 | 400.9 | 0.3633 | 0.0475 | 0.0000 |
| 600 | probe_adaptive_k_t67 | 402.8 | 0.3667 | 0.0430 | 0.0000 |
| 600 | probe_adaptive_k_t75 | 402.8 | 0.3667 | 0.0430 | 0.0000 |
| 600 | probe_adaptive_k_t80 | 402.8 | 0.3667 | 0.0430 | 0.0000 |
| 600 | probe_only_fixedk_k4 | 413.9 | 0.3667 | 0.0430 | 0.0000 |
| 600 | probe_only_fixedk_k8 | 413.9 | 0.3667 | 0.0430 | 0.0000 |
| 750 | hard_cap | 316.0 | 0.3200 | 0.1720 | 0.0000 |
| 750 | ours_controller_v2_nofallback | 478.3 | 0.3917 | 0.0668 | 0.0000 |
| 750 | probe_only_fixedk_k2 | 484.0 | 0.3683 | 0.0352 | 0.0000 |
| 750 | probe_adaptive_k_t67 | 494.4 | 0.3683 | 0.0403 | 0.0000 |
| 750 | probe_adaptive_k_t75 | 494.4 | 0.3683 | 0.0403 | 0.0000 |
| 750 | probe_adaptive_k_t80 | 494.7 | 0.3683 | 0.0403 | 0.0000 |
| 750 | probe_only_fixedk_k4 | 570.6 | 0.3683 | 0.0403 | 0.0000 |
| 750 | probe_only_fixedk_k8 | 572.1 | 0.3683 | 0.0403 | 0.0000 |
| 900 | hard_cap | 323.3 | 0.3000 | 0.1710 | 0.0000 |
| 900 | probe_only_fixedk_k2 | 521.1 | 0.3717 | 0.0482 | 0.0000 |
| 900 | ours_controller_v2_nofallback | 528.2 | 0.3750 | 0.0662 | 0.0000 |
| 900 | probe_adaptive_k_t67 | 547.9 | 0.3800 | 0.0582 | 0.0000 |
| 900 | probe_adaptive_k_t75 | 547.9 | 0.3800 | 0.0582 | 0.0000 |
| 900 | probe_adaptive_k_t80 | 548.7 | 0.3800 | 0.0582 | 0.0000 |
| 900 | probe_only_fixedk_k4 | 701.3 | 0.3783 | 0.0582 | 0.0000 |
| 900 | probe_only_fixedk_k8 | 710.7 | 0.3800 | 0.0582 | 0.0000 |
| 1200 | hard_cap | 333.3 | 0.2917 | 0.1607 | 0.0000 |
| 1200 | probe_only_fixedk_k2 | 565.5 | 0.3750 | 0.0558 | 0.0000 |
| 1200 | ours_controller_v2_nofallback | 595.8 | 0.3850 | 0.0606 | 0.0000 |
| 1200 | probe_adaptive_k_t67 | 608.6 | 0.3800 | 0.0366 | 0.0000 |
| 1200 | probe_adaptive_k_t75 | 608.6 | 0.3800 | 0.0366 | 0.0000 |
| 1200 | probe_adaptive_k_t80 | 612.4 | 0.3800 | 0.0366 | 0.0000 |
| 1200 | probe_only_fixedk_k4 | 921.9 | 0.3767 | 0.0440 | 0.0000 |
| 1200 | probe_only_fixedk_k8 | 1014.0 | 0.3783 | 0.0366 | 0.0000 |
| 1500 | hard_cap | 333.6 | 0.3017 | 0.1693 | 0.0000 |
| 1500 | probe_only_fixedk_k2 | 578.3 | 0.3733 | 0.0574 | 0.0000 |
| 1500 | ours_controller_v2_nofallback | 609.9 | 0.3717 | 0.0620 | 0.0000 |
| 1500 | probe_adaptive_k_t67 | 635.1 | 0.3750 | 0.0499 | 0.0000 |
| 1500 | probe_adaptive_k_t75 | 635.1 | 0.3750 | 0.0499 | 0.0000 |
| 1500 | probe_adaptive_k_t80 | 649.0 | 0.3750 | 0.0499 | 0.0000 |
| 1500 | probe_only_fixedk_k4 | 1038.9 | 0.3717 | 0.0427 | 0.0000 |
| 1500 | probe_only_fixedk_k8 | 1313.0 | 0.3733 | 0.0427 | 0.0000 |

## nofallback Decision Breakdown
| Budget | Stop@Probe | ContinueSolve | FallbackHardCap | ProbeShare | SolveShare | AvgProbeTok | AvgSolveTok |
|---|---:|---:|---:|---:|---:|---:|---:|
| 300 | 0.000 | 1.000 | 0.000 | 0.000 | 0.778 | 0.0 | 120.7 |
| 400 | 0.810 | 0.190 | 0.000 | 0.933 | 0.008 | 203.7 | 1.7 |
| 500 | 0.872 | 0.128 | 0.000 | 0.960 | 0.007 | 303.6 | 2.2 |
| 600 | 0.892 | 0.108 | 0.000 | 0.985 | 0.000 | 387.3 | 0.0 |
| 750 | 0.900 | 0.100 | 0.000 | 0.988 | 0.000 | 472.6 | 0.0 |
| 900 | 0.920 | 0.080 | 0.000 | 0.990 | 0.002 | 523.1 | 0.9 |
| 1200 | 0.943 | 0.057 | 0.000 | 0.986 | 0.010 | 587.3 | 6.0 |
| 1500 | 0.957 | 0.043 | 0.000 | 0.979 | 0.020 | 597.3 | 12.4 |

## Probe Predictive Signal (nofallback)
- Baseline method for labels: `hard_cap`
| Budget | n trial-pairs | AUC(disagree->base_error) | ECE(disagree->base_error) | n docs | AUC(disagree->base_disagree>0) |
|---|---:|---:|---:|---:|---:|
| 300 | 600 | 0.500 | 0.272 | 200 | 0.500 |
| 400 | 600 | 0.515 | 0.617 | 200 | 0.358 |
| 500 | 600 | 0.546 | 0.613 | 200 | 0.466 |
| 600 | 600 | 0.527 | 0.642 | 200 | 0.441 |
| 750 | 600 | 0.527 | 0.633 | 200 | 0.497 |
| 900 | 600 | 0.536 | 0.659 | 200 | 0.474 |
| 1200 | 600 | 0.520 | 0.671 | 200 | 0.521 |
| 1500 | 600 | 0.540 | 0.664 | 200 | 0.484 |

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round8a_tuning_splitA3_r3_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round8a_tuning_splitA3_r3_v1/analysis_summary_round2.json`
