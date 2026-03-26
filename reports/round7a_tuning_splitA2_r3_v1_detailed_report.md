# round7a_tuning_splitA2_r3_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round7a_tuning_splitA2_r3_v1`
- Dataset: `Wanfq/gpqa:200 sampled from run manifest`
- Methods: `['hard_cap', 'ours_controller_v2_nofallback', 'probe_only_fixedk_k2', 'probe_only_fixedk_k4', 'probe_only_fixedk_k6', 'probe_only_fixedk_k8', 'probe_adaptive_k_t67', 'probe_adaptive_k_t75']`
- Budgets: `[300, 400, 500, 600, 750, 900, 1200, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `38400` completed
- Hard fail: `0`
- Parse fail: `126` (`0.3281%`)
- Repair success: `2465/2465` (`100.0000%`)
- Duration: `240.77` minutes

## Phase Threshold
- nofallback beats hard_cap on incoh with no acc loss first at: `400`
- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `None`
- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `None`
- (parse-excluded) nofallback beats hard_cap on incoh with no acc loss first at: `400`
- Threshold bootstrap (hard_cap vs nofallback, parse-included): finite_rate=`1.000`, median=`400.0`, 95% CI=`[300.0, 400.0]`
- Threshold bootstrap (hard_cap vs nofallback, parse-excluded): finite_rate=`1.000`, median=`400.0`, 95% CI=`[300.0, 400.0]`

## nofallback Delta Table
| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |
|---|---:|---:|---:|---:|
| 300 | -0.0048 | -0.0183 | +nan | +nan |
| 400 | -0.0766 | +0.0700 | +nan | +nan |
| 500 | -0.1053 | +0.1183 | +nan | +nan |
| 600 | -0.0961 | +0.1267 | +nan | +nan |
| 750 | -0.1211 | +0.0967 | +nan | +nan |
| 900 | -0.1051 | +0.1350 | +nan | +nan |
| 1200 | -0.1171 | +0.1117 | +nan | +nan |
| 1500 | -0.1092 | +0.1400 | +nan | +nan |

## Adaptive Probe vs Probe-Only
| Budget | Adaptive | Probe | Δacc(adapt-probe) | Δincoh(adapt-probe) | Adapt Tok | Probe Tok |
|---|---|---|---:|---:|---:|---:|
| 300 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0000 | +0.0000 | 196.4 | 196.4 |
| 400 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0000 | +0.0000 | 274.3 | 274.3 |
| 500 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | -0.0017 | -0.0024 | 372.0 | 371.8 |
| 600 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0000 | -0.0028 | 446.8 | 444.4 |
| 750 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0000 | -0.0100 | 506.2 | 497.0 |
| 900 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0067 | -0.0036 | 550.9 | 531.4 |
| 1200 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0017 | +0.0011 | 621.7 | 580.9 |
| 1500 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0083 | +0.0029 | 644.9 | 591.5 |

## Parse-Fail Sensitivity (Included vs Excluded)
| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |
|---|---|---:|---:|---:|---:|---:|
| 300 | hard_cap | 0.2717 | 0.2730 | 0.1030 | 0.1037 | 199 |
| 300 | ours_controller_v2_nofallback | 0.2533 | 0.2559 | 0.0982 | 0.0994 | 198 |
| 300 | probe_only_fixedk_k2 | 0.3483 | 0.3519 | 0.0557 | 0.0565 | 198 |
| 300 | probe_only_fixedk_k4 | 0.3483 | 0.3519 | 0.0557 | 0.0565 | 198 |
| 300 | probe_only_fixedk_k6 | 0.3483 | 0.3519 | 0.0557 | 0.0565 | 198 |
| 300 | probe_only_fixedk_k8 | 0.3483 | 0.3519 | 0.0557 | 0.0565 | 198 |
| 300 | probe_adaptive_k_t67 | 0.3483 | 0.3519 | 0.0557 | 0.0565 | 198 |
| 300 | probe_adaptive_k_t75 | 0.3483 | 0.3519 | 0.0557 | 0.0565 | 198 |
| 400 | hard_cap | 0.2683 | 0.2710 | 0.1245 | 0.1260 | 198 |
| 400 | ours_controller_v2_nofallback | 0.3383 | 0.3495 | 0.0478 | 0.0491 | 196 |
| 400 | probe_only_fixedk_k2 | 0.3500 | 0.3500 | 0.0526 | 0.0526 | 200 |
| 400 | probe_only_fixedk_k4 | 0.3500 | 0.3500 | 0.0526 | 0.0526 | 200 |
| 400 | probe_only_fixedk_k6 | 0.3500 | 0.3500 | 0.0526 | 0.0526 | 200 |
| 400 | probe_only_fixedk_k8 | 0.3500 | 0.3500 | 0.0526 | 0.0526 | 200 |
| 400 | probe_adaptive_k_t67 | 0.3500 | 0.3500 | 0.0526 | 0.0526 | 200 |
| 400 | probe_adaptive_k_t75 | 0.3500 | 0.3500 | 0.0526 | 0.0526 | 200 |
| 500 | hard_cap | 0.2767 | 0.2781 | 0.1495 | 0.1504 | 199 |
| 500 | ours_controller_v2_nofallback | 0.3950 | 0.3970 | 0.0442 | 0.0407 | 199 |
| 500 | probe_only_fixedk_k2 | 0.3667 | 0.3685 | 0.0546 | 0.0550 | 199 |
| 500 | probe_only_fixedk_k4 | 0.3650 | 0.3668 | 0.0522 | 0.0526 | 199 |
| 500 | probe_only_fixedk_k6 | 0.3650 | 0.3668 | 0.0522 | 0.0526 | 199 |
| 500 | probe_only_fixedk_k8 | 0.3650 | 0.3668 | 0.0522 | 0.0526 | 199 |
| 500 | probe_adaptive_k_t67 | 0.3650 | 0.3668 | 0.0522 | 0.0526 | 199 |
| 500 | probe_adaptive_k_t75 | 0.3650 | 0.3668 | 0.0522 | 0.0526 | 199 |
| 600 | hard_cap | 0.2717 | 0.2717 | 0.1462 | 0.1462 | 200 |
| 600 | ours_controller_v2_nofallback | 0.3983 | 0.4033 | 0.0501 | 0.0429 | 200 |
| 600 | probe_only_fixedk_k2 | 0.3833 | 0.3833 | 0.0514 | 0.0514 | 200 |
| 600 | probe_only_fixedk_k4 | 0.3833 | 0.3833 | 0.0486 | 0.0486 | 200 |
| 600 | probe_only_fixedk_k6 | 0.3833 | 0.3833 | 0.0486 | 0.0486 | 200 |
| 600 | probe_only_fixedk_k8 | 0.3833 | 0.3833 | 0.0486 | 0.0486 | 200 |
| 600 | probe_adaptive_k_t67 | 0.3833 | 0.3833 | 0.0486 | 0.0486 | 200 |
| 600 | probe_adaptive_k_t75 | 0.3833 | 0.3833 | 0.0486 | 0.0486 | 200 |
| 750 | hard_cap | 0.2800 | 0.2800 | 0.1768 | 0.1768 | 200 |
| 750 | ours_controller_v2_nofallback | 0.3767 | 0.3861 | 0.0557 | 0.0485 | 199 |
| 750 | probe_only_fixedk_k2 | 0.3933 | 0.3933 | 0.0576 | 0.0576 | 200 |
| 750 | probe_only_fixedk_k4 | 0.3933 | 0.3933 | 0.0476 | 0.0476 | 200 |
| 750 | probe_only_fixedk_k6 | 0.3933 | 0.3933 | 0.0476 | 0.0476 | 200 |
| 750 | probe_only_fixedk_k8 | 0.3933 | 0.3933 | 0.0476 | 0.0476 | 200 |
| 750 | probe_adaptive_k_t67 | 0.3933 | 0.3933 | 0.0476 | 0.0476 | 200 |
| 750 | probe_adaptive_k_t75 | 0.3933 | 0.3933 | 0.0476 | 0.0476 | 200 |
| 900 | hard_cap | 0.2483 | 0.2483 | 0.1648 | 0.1648 | 200 |
| 900 | ours_controller_v2_nofallback | 0.3833 | 0.3850 | 0.0597 | 0.0590 | 200 |
| 900 | probe_only_fixedk_k2 | 0.3833 | 0.3833 | 0.0558 | 0.0558 | 200 |
| 900 | probe_only_fixedk_k4 | 0.3900 | 0.3900 | 0.0447 | 0.0447 | 200 |
| 900 | probe_only_fixedk_k6 | 0.3917 | 0.3917 | 0.0472 | 0.0472 | 200 |
| 900 | probe_only_fixedk_k8 | 0.3917 | 0.3917 | 0.0472 | 0.0472 | 200 |
| 900 | probe_adaptive_k_t67 | 0.3900 | 0.3900 | 0.0522 | 0.0522 | 200 |
| 900 | probe_adaptive_k_t75 | 0.3900 | 0.3900 | 0.0522 | 0.0522 | 200 |
| 1200 | hard_cap | 0.2650 | 0.2650 | 0.1654 | 0.1654 | 200 |
| 1200 | ours_controller_v2_nofallback | 0.3767 | 0.3767 | 0.0484 | 0.0465 | 200 |
| 1200 | probe_only_fixedk_k2 | 0.3883 | 0.3883 | 0.0465 | 0.0465 | 200 |
| 1200 | probe_only_fixedk_k4 | 0.3900 | 0.3900 | 0.0580 | 0.0580 | 200 |
| 1200 | probe_only_fixedk_k6 | 0.3900 | 0.3900 | 0.0472 | 0.0472 | 200 |
| 1200 | probe_only_fixedk_k8 | 0.3900 | 0.3900 | 0.0472 | 0.0472 | 200 |
| 1200 | probe_adaptive_k_t67 | 0.3900 | 0.3900 | 0.0476 | 0.0476 | 200 |
| 1200 | probe_adaptive_k_t75 | 0.3900 | 0.3900 | 0.0476 | 0.0476 | 200 |
| 1500 | hard_cap | 0.2450 | 0.2450 | 0.1630 | 0.1630 | 200 |
| 1500 | ours_controller_v2_nofallback | 0.3850 | 0.3850 | 0.0538 | 0.0538 | 200 |
| 1500 | probe_only_fixedk_k2 | 0.3833 | 0.3833 | 0.0543 | 0.0543 | 200 |
| 1500 | probe_only_fixedk_k4 | 0.3900 | 0.3900 | 0.0497 | 0.0497 | 200 |
| 1500 | probe_only_fixedk_k6 | 0.3883 | 0.3883 | 0.0538 | 0.0538 | 200 |
| 1500 | probe_only_fixedk_k8 | 0.3850 | 0.3850 | 0.0490 | 0.0490 | 200 |
| 1500 | probe_adaptive_k_t67 | 0.3917 | 0.3917 | 0.0571 | 0.0571 | 200 |
| 1500 | probe_adaptive_k_t75 | 0.3917 | 0.3917 | 0.0571 | 0.0571 | 200 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 300 | hard_cap | 0.005 | 0.260 | 1.000 |
| 300 | ours_controller_v2_nofallback | 0.010 | 0.245 | 1.000 |
| 300 | probe_only_fixedk_k2 | 0.010 | 0.255 | 1.000 |
| 300 | probe_only_fixedk_k4 | 0.010 | 0.255 | 1.000 |
| 300 | probe_only_fixedk_k6 | 0.010 | 0.255 | 1.000 |
| 300 | probe_only_fixedk_k8 | 0.010 | 0.255 | 1.000 |
| 300 | probe_adaptive_k_t67 | 0.010 | 0.255 | 1.000 |
| 300 | probe_adaptive_k_t75 | 0.010 | 0.255 | 1.000 |
| 400 | hard_cap | 0.010 | 0.125 | 1.000 |
| 400 | ours_controller_v2_nofallback | 0.032 | 0.125 | 1.000 |
| 400 | probe_only_fixedk_k2 | 0.000 | 0.115 | 1.000 |
| 400 | probe_only_fixedk_k4 | 0.000 | 0.115 | 1.000 |
| 400 | probe_only_fixedk_k6 | 0.000 | 0.115 | 1.000 |
| 400 | probe_only_fixedk_k8 | 0.000 | 0.115 | 1.000 |
| 400 | probe_adaptive_k_t67 | 0.000 | 0.115 | 1.000 |
| 400 | probe_adaptive_k_t75 | 0.000 | 0.115 | 1.000 |
| 500 | hard_cap | 0.005 | 0.055 | 1.000 |
| 500 | ours_controller_v2_nofallback | 0.012 | 0.107 | 1.000 |
| 500 | probe_only_fixedk_k2 | 0.005 | 0.055 | 1.000 |
| 500 | probe_only_fixedk_k4 | 0.005 | 0.055 | 1.000 |
| 500 | probe_only_fixedk_k6 | 0.005 | 0.055 | 1.000 |
| 500 | probe_only_fixedk_k8 | 0.005 | 0.055 | 1.000 |
| 500 | probe_adaptive_k_t67 | 0.005 | 0.055 | 1.000 |
| 500 | probe_adaptive_k_t75 | 0.005 | 0.055 | 1.000 |
| 600 | hard_cap | 0.000 | 0.030 | 1.000 |
| 600 | ours_controller_v2_nofallback | 0.017 | 0.082 | 1.000 |
| 600 | probe_only_fixedk_k2 | 0.000 | 0.030 | 1.000 |
| 600 | probe_only_fixedk_k4 | 0.000 | 0.030 | 1.000 |
| 600 | probe_only_fixedk_k6 | 0.000 | 0.030 | 1.000 |
| 600 | probe_only_fixedk_k8 | 0.000 | 0.030 | 1.000 |
| 600 | probe_adaptive_k_t67 | 0.000 | 0.030 | 1.000 |
| 600 | probe_adaptive_k_t75 | 0.000 | 0.030 | 1.000 |
| 750 | hard_cap | 0.000 | 0.015 | 1.000 |
| 750 | ours_controller_v2_nofallback | 0.020 | 0.068 | 1.000 |
| 750 | probe_only_fixedk_k2 | 0.000 | 0.015 | 1.000 |
| 750 | probe_only_fixedk_k4 | 0.000 | 0.015 | 1.000 |
| 750 | probe_only_fixedk_k6 | 0.000 | 0.015 | 1.000 |
| 750 | probe_only_fixedk_k8 | 0.000 | 0.015 | 1.000 |
| 750 | probe_adaptive_k_t67 | 0.000 | 0.015 | 1.000 |
| 750 | probe_adaptive_k_t75 | 0.000 | 0.015 | 1.000 |
| 900 | hard_cap | 0.000 | 0.010 | 1.000 |
| 900 | ours_controller_v2_nofallback | 0.008 | 0.062 | 1.000 |
| 900 | probe_only_fixedk_k2 | 0.000 | 0.010 | 1.000 |
| 900 | probe_only_fixedk_k4 | 0.000 | 0.010 | 1.000 |
| 900 | probe_only_fixedk_k6 | 0.000 | 0.010 | 1.000 |
| 900 | probe_only_fixedk_k8 | 0.000 | 0.010 | 1.000 |
| 900 | probe_adaptive_k_t67 | 0.000 | 0.010 | 1.000 |
| 900 | probe_adaptive_k_t75 | 0.000 | 0.010 | 1.000 |
| 1200 | hard_cap | 0.000 | 0.000 | 0.000 |
| 1200 | ours_controller_v2_nofallback | 0.002 | 0.025 | 1.000 |
| 1200 | probe_only_fixedk_k2 | 0.000 | 0.000 | 0.000 |
| 1200 | probe_only_fixedk_k4 | 0.000 | 0.000 | 0.000 |
| 1200 | probe_only_fixedk_k6 | 0.000 | 0.000 | 0.000 |
| 1200 | probe_only_fixedk_k8 | 0.000 | 0.000 | 0.000 |
| 1200 | probe_adaptive_k_t67 | 0.000 | 0.000 | 0.000 |
| 1200 | probe_adaptive_k_t75 | 0.000 | 0.000 | 0.000 |
| 1500 | hard_cap | 0.000 | 0.000 | 0.000 |
| 1500 | ours_controller_v2_nofallback | 0.000 | 0.020 | 1.000 |
| 1500 | probe_only_fixedk_k2 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_only_fixedk_k4 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_only_fixedk_k6 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_only_fixedk_k8 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_adaptive_k_t67 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_adaptive_k_t75 | 0.000 | 0.000 | 0.000 |

## Parse-Fail Gating Check
| Budget | Max ParseFail | Min ParseFail | Spread | Gate(max<=1%) | Gate(spread<=1%p) |
|---|---:|---:|---:|---:|---:|
| 300 | 0.010 | 0.005 | 0.005 | 1 | 1 |
| 400 | 0.032 | 0.000 | 0.032 | 0 | 0 |
| 500 | 0.012 | 0.005 | 0.007 | 0 | 1 |
| 600 | 0.017 | 0.000 | 0.017 | 0 | 0 |
| 750 | 0.020 | 0.000 | 0.020 | 0 | 0 |
| 900 | 0.008 | 0.000 | 0.008 | 1 | 1 |
| 1200 | 0.002 | 0.000 | 0.002 | 1 | 1 |
| 1500 | 0.000 | 0.000 | 0.000 | 1 | 1 |

## Cost Reality (Actual Total Tokens)
| Budget | Method | AvgTotalTok | Accuracy | Incoherence | ParseFail |
|---|---|---:|---:|---:|---:|
| 300 | probe_only_fixedk_k2 | 196.4 | 0.3483 | 0.0557 | 0.0100 |
| 300 | probe_only_fixedk_k4 | 196.4 | 0.3483 | 0.0557 | 0.0100 |
| 300 | probe_only_fixedk_k6 | 196.4 | 0.3483 | 0.0557 | 0.0100 |
| 300 | probe_only_fixedk_k8 | 196.4 | 0.3483 | 0.0557 | 0.0100 |
| 300 | probe_adaptive_k_t67 | 196.4 | 0.3483 | 0.0557 | 0.0100 |
| 300 | probe_adaptive_k_t75 | 196.4 | 0.3483 | 0.0557 | 0.0100 |
| 300 | hard_cap | 202.4 | 0.2717 | 0.1030 | 0.0050 |
| 300 | ours_controller_v2_nofallback | 207.3 | 0.2533 | 0.0982 | 0.0100 |
| 400 | hard_cap | 263.9 | 0.2683 | 0.1245 | 0.0100 |
| 400 | probe_only_fixedk_k2 | 274.3 | 0.3500 | 0.0526 | 0.0000 |
| 400 | probe_adaptive_k_t67 | 274.3 | 0.3500 | 0.0526 | 0.0000 |
| 400 | probe_adaptive_k_t75 | 274.3 | 0.3500 | 0.0526 | 0.0000 |
| 400 | ours_controller_v2_nofallback | 274.9 | 0.3383 | 0.0478 | 0.0317 |
| 400 | probe_only_fixedk_k4 | 275.3 | 0.3500 | 0.0526 | 0.0000 |
| 400 | probe_only_fixedk_k6 | 275.3 | 0.3500 | 0.0526 | 0.0000 |
| 400 | probe_only_fixedk_k8 | 275.3 | 0.3500 | 0.0526 | 0.0000 |
| 500 | hard_cap | 295.2 | 0.2767 | 0.1495 | 0.0050 |
| 500 | ours_controller_v2_nofallback | 358.5 | 0.3950 | 0.0442 | 0.0117 |
| 500 | probe_only_fixedk_k2 | 371.8 | 0.3667 | 0.0546 | 0.0050 |
| 500 | probe_adaptive_k_t67 | 372.0 | 0.3650 | 0.0522 | 0.0050 |
| 500 | probe_adaptive_k_t75 | 372.0 | 0.3650 | 0.0522 | 0.0050 |
| 500 | probe_only_fixedk_k4 | 380.5 | 0.3650 | 0.0522 | 0.0050 |
| 500 | probe_only_fixedk_k6 | 380.5 | 0.3650 | 0.0522 | 0.0050 |
| 500 | probe_only_fixedk_k8 | 380.5 | 0.3650 | 0.0522 | 0.0050 |
| 600 | hard_cap | 314.1 | 0.2717 | 0.1462 | 0.0000 |
| 600 | ours_controller_v2_nofallback | 437.8 | 0.3983 | 0.0501 | 0.0167 |
| 600 | probe_only_fixedk_k2 | 444.4 | 0.3833 | 0.0514 | 0.0000 |
| 600 | probe_adaptive_k_t67 | 446.8 | 0.3833 | 0.0486 | 0.0000 |
| 600 | probe_adaptive_k_t75 | 446.8 | 0.3833 | 0.0486 | 0.0000 |
| 600 | probe_only_fixedk_k4 | 478.0 | 0.3833 | 0.0486 | 0.0000 |
| 600 | probe_only_fixedk_k6 | 478.0 | 0.3833 | 0.0486 | 0.0000 |
| 600 | probe_only_fixedk_k8 | 478.0 | 0.3833 | 0.0486 | 0.0000 |
| 750 | hard_cap | 322.1 | 0.2800 | 0.1768 | 0.0000 |
| 750 | probe_only_fixedk_k2 | 497.0 | 0.3933 | 0.0576 | 0.0000 |
| 750 | ours_controller_v2_nofallback | 498.7 | 0.3767 | 0.0557 | 0.0200 |
| 750 | probe_adaptive_k_t67 | 506.2 | 0.3933 | 0.0476 | 0.0000 |
| 750 | probe_adaptive_k_t75 | 506.2 | 0.3933 | 0.0476 | 0.0000 |
| 750 | probe_only_fixedk_k4 | 620.6 | 0.3933 | 0.0476 | 0.0000 |
| 750 | probe_only_fixedk_k6 | 621.9 | 0.3933 | 0.0476 | 0.0000 |
| 750 | probe_only_fixedk_k8 | 621.9 | 0.3933 | 0.0476 | 0.0000 |
| 900 | hard_cap | 327.0 | 0.2483 | 0.1648 | 0.0000 |
| 900 | probe_only_fixedk_k2 | 531.4 | 0.3833 | 0.0558 | 0.0000 |
| 900 | ours_controller_v2_nofallback | 545.4 | 0.3833 | 0.0597 | 0.0083 |
| 900 | probe_adaptive_k_t67 | 550.9 | 0.3900 | 0.0522 | 0.0000 |
| 900 | probe_adaptive_k_t75 | 550.9 | 0.3900 | 0.0522 | 0.0000 |
| 900 | probe_only_fixedk_k4 | 755.9 | 0.3900 | 0.0447 | 0.0000 |
| 900 | probe_only_fixedk_k6 | 773.0 | 0.3917 | 0.0472 | 0.0000 |
| 900 | probe_only_fixedk_k8 | 773.0 | 0.3917 | 0.0472 | 0.0000 |
| 1200 | hard_cap | 337.3 | 0.2650 | 0.1654 | 0.0000 |
| 1200 | probe_only_fixedk_k2 | 580.9 | 0.3883 | 0.0465 | 0.0000 |
| 1200 | ours_controller_v2_nofallback | 593.1 | 0.3767 | 0.0484 | 0.0017 |
| 1200 | probe_adaptive_k_t67 | 621.7 | 0.3900 | 0.0476 | 0.0000 |
| 1200 | probe_adaptive_k_t75 | 621.7 | 0.3900 | 0.0476 | 0.0000 |
| 1200 | probe_only_fixedk_k4 | 954.0 | 0.3900 | 0.0580 | 0.0000 |
| 1200 | probe_only_fixedk_k6 | 1071.1 | 0.3900 | 0.0472 | 0.0000 |
| 1200 | probe_only_fixedk_k8 | 1081.4 | 0.3900 | 0.0472 | 0.0000 |
| 1500 | hard_cap | 337.4 | 0.2450 | 0.1630 | 0.0000 |
| 1500 | probe_only_fixedk_k2 | 591.5 | 0.3833 | 0.0543 | 0.0000 |
| 1500 | ours_controller_v2_nofallback | 619.6 | 0.3850 | 0.0538 | 0.0000 |
| 1500 | probe_adaptive_k_t67 | 644.9 | 0.3917 | 0.0571 | 0.0000 |
| 1500 | probe_adaptive_k_t75 | 644.9 | 0.3917 | 0.0571 | 0.0000 |
| 1500 | probe_only_fixedk_k4 | 1050.3 | 0.3900 | 0.0497 | 0.0000 |
| 1500 | probe_only_fixedk_k6 | 1300.6 | 0.3883 | 0.0538 | 0.0000 |
| 1500 | probe_only_fixedk_k8 | 1364.5 | 0.3850 | 0.0490 | 0.0000 |

## Probe Predictive Signal (nofallback)
- Baseline method for labels: `hard_cap`
| Budget | n trial-pairs | AUC(disagree->base_error) | ECE(disagree->base_error) | n docs | AUC(disagree->base_disagree>0) |
|---|---:|---:|---:|---:|---:|
| 300 | 600 | 0.500 | 0.272 | 200 | 0.500 |
| 400 | 600 | 0.516 | 0.638 | 200 | 0.429 |
| 500 | 600 | 0.512 | 0.649 | 200 | 0.486 |
| 600 | 600 | 0.498 | 0.682 | 200 | 0.516 |
| 750 | 600 | 0.487 | 0.678 | 200 | 0.494 |
| 900 | 600 | 0.437 | 0.715 | 200 | 0.451 |
| 1200 | 600 | 0.505 | 0.708 | 200 | 0.526 |
| 1500 | 600 | 0.467 | 0.721 | 200 | 0.539 |

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round7a_tuning_splitA2_r3_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round7a_tuning_splitA2_r3_v1/analysis_summary_round2.json`
