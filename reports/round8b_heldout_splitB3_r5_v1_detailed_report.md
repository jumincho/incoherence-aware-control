# round8b_heldout_splitB3_r5_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round8b_heldout_splitB3_r5_v1`
- Dataset: `Wanfq/gpqa:200 sampled from run manifest`
- Methods: `['hard_cap', 'hard_cap_matched', 'ours_controller_v2_nofallback', 'probe_only_fixedk_k2', 'probe_only_fixedk_k4', 'probe_only_fixedk_k8', 'probe_adaptive_k_selected']`
- Budgets: `[300, 400, 500, 600, 750, 900, 1200, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `56000` completed
- Hard fail: `0`
- Parse fail: `0` (`0.0000%`)
- Repair success: `5843/5843` (`100.0000%`)
- Duration: `371.00` minutes

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
| 300 | -0.0102 | -0.0240 | +nan | +nan |
| 400 | -0.1033 | +0.0940 | +nan | +nan |
| 500 | -0.1265 | +0.0790 | +nan | +nan |
| 600 | -0.1120 | +0.0930 | +nan | +nan |
| 750 | -0.1383 | +0.1080 | +nan | +nan |
| 900 | -0.1010 | +0.0740 | +nan | +nan |
| 1200 | -0.1412 | +0.0820 | +nan | +nan |
| 1500 | -0.1287 | +0.0960 | +nan | +nan |

## Adaptive Probe vs Probe-Only
| Budget | Adaptive | Probe | Δacc(adapt-probe) | Δincoh(adapt-probe) | Adapt Tok | Probe Tok |
|---|---|---|---:|---:|---:|---:|
| 300 | probe_adaptive_k_selected | probe_only_fixedk_k2 | +0.0020 | +0.0000 | 139.1 | 139.1 |
| 400 | probe_adaptive_k_selected | probe_only_fixedk_k2 | +0.0000 | -0.0041 | 238.1 | 238.1 |
| 500 | probe_adaptive_k_selected | probe_only_fixedk_k2 | -0.0010 | -0.0014 | 322.2 | 321.9 |
| 600 | probe_adaptive_k_selected | probe_only_fixedk_k2 | +0.0020 | -0.0023 | 395.1 | 393.1 |
| 750 | probe_adaptive_k_selected | probe_only_fixedk_k2 | +0.0010 | -0.0101 | 495.8 | 489.8 |
| 900 | probe_adaptive_k_selected | probe_only_fixedk_k2 | -0.0040 | -0.0045 | 557.9 | 542.4 |
| 1200 | probe_adaptive_k_selected | probe_only_fixedk_k2 | +0.0040 | -0.0051 | 606.5 | 569.8 |
| 1500 | probe_adaptive_k_selected | probe_only_fixedk_k2 | -0.0040 | -0.0224 | 624.2 | 575.0 |

## Parse-Fail Sensitivity (Included vs Excluded)
| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |
|---|---|---:|---:|---:|---:|---:|
| 300 | hard_cap | 0.2680 | 0.2680 | 0.1038 | 0.1038 | 200 |
| 300 | hard_cap_matched | 0.2680 | 0.2680 | 0.1049 | 0.1049 | 200 |
| 300 | ours_controller_v2_nofallback | 0.2440 | 0.2440 | 0.0936 | 0.0936 | 200 |
| 300 | probe_only_fixedk_k2 | 0.3300 | 0.3300 | 0.0523 | 0.0523 | 200 |
| 300 | probe_only_fixedk_k4 | 0.3300 | 0.3300 | 0.0523 | 0.0523 | 200 |
| 300 | probe_only_fixedk_k8 | 0.3300 | 0.3300 | 0.0523 | 0.0523 | 200 |
| 300 | probe_adaptive_k_selected | 0.3320 | 0.3320 | 0.0523 | 0.0523 | 200 |
| 400 | hard_cap | 0.2650 | 0.2650 | 0.1694 | 0.1694 | 200 |
| 400 | hard_cap_matched | 0.2650 | 0.2650 | 0.1694 | 0.1694 | 200 |
| 400 | ours_controller_v2_nofallback | 0.3590 | 0.3590 | 0.0661 | 0.0661 | 200 |
| 400 | probe_only_fixedk_k2 | 0.3610 | 0.3610 | 0.0616 | 0.0616 | 200 |
| 400 | probe_only_fixedk_k4 | 0.3610 | 0.3610 | 0.0616 | 0.0616 | 200 |
| 400 | probe_only_fixedk_k8 | 0.3610 | 0.3610 | 0.0616 | 0.0616 | 200 |
| 400 | probe_adaptive_k_selected | 0.3610 | 0.3610 | 0.0576 | 0.0576 | 200 |
| 500 | hard_cap | 0.2780 | 0.2780 | 0.2050 | 0.2050 | 200 |
| 500 | hard_cap_matched | 0.2870 | 0.2870 | 0.2287 | 0.2287 | 200 |
| 500 | ours_controller_v2_nofallback | 0.3570 | 0.3570 | 0.0786 | 0.0786 | 200 |
| 500 | probe_only_fixedk_k2 | 0.3560 | 0.3560 | 0.0630 | 0.0630 | 200 |
| 500 | probe_only_fixedk_k4 | 0.3550 | 0.3550 | 0.0616 | 0.0616 | 200 |
| 500 | probe_only_fixedk_k8 | 0.3550 | 0.3550 | 0.0616 | 0.0616 | 200 |
| 500 | probe_adaptive_k_selected | 0.3550 | 0.3550 | 0.0616 | 0.0616 | 200 |
| 600 | hard_cap | 0.2530 | 0.2530 | 0.1941 | 0.1941 | 200 |
| 600 | hard_cap_matched | 0.2730 | 0.2730 | 0.2308 | 0.2308 | 200 |
| 600 | ours_controller_v2_nofallback | 0.3460 | 0.3460 | 0.0821 | 0.0821 | 200 |
| 600 | probe_only_fixedk_k2 | 0.3470 | 0.3470 | 0.0589 | 0.0589 | 200 |
| 600 | probe_only_fixedk_k4 | 0.3490 | 0.3490 | 0.0566 | 0.0566 | 200 |
| 600 | probe_only_fixedk_k8 | 0.3490 | 0.3490 | 0.0566 | 0.0566 | 200 |
| 600 | probe_adaptive_k_selected | 0.3490 | 0.3490 | 0.0566 | 0.0566 | 200 |
| 750 | hard_cap | 0.2440 | 0.2440 | 0.2057 | 0.2057 | 200 |
| 750 | hard_cap_matched | 0.2740 | 0.2740 | 0.2477 | 0.2477 | 200 |
| 750 | ours_controller_v2_nofallback | 0.3520 | 0.3520 | 0.0674 | 0.0674 | 200 |
| 750 | probe_only_fixedk_k2 | 0.3520 | 0.3520 | 0.0556 | 0.0556 | 200 |
| 750 | probe_only_fixedk_k4 | 0.3550 | 0.3550 | 0.0469 | 0.0469 | 200 |
| 750 | probe_only_fixedk_k8 | 0.3550 | 0.3550 | 0.0469 | 0.0469 | 200 |
| 750 | probe_adaptive_k_selected | 0.3530 | 0.3530 | 0.0455 | 0.0455 | 200 |
| 900 | hard_cap | 0.2640 | 0.2640 | 0.1876 | 0.1876 | 200 |
| 900 | hard_cap_matched | 0.2980 | 0.2980 | 0.2408 | 0.2408 | 200 |
| 900 | ours_controller_v2_nofallback | 0.3380 | 0.3380 | 0.0865 | 0.0865 | 200 |
| 900 | probe_only_fixedk_k2 | 0.3550 | 0.3550 | 0.0598 | 0.0598 | 200 |
| 900 | probe_only_fixedk_k4 | 0.3520 | 0.3520 | 0.0543 | 0.0543 | 200 |
| 900 | probe_only_fixedk_k8 | 0.3520 | 0.3520 | 0.0525 | 0.0525 | 200 |
| 900 | probe_adaptive_k_selected | 0.3510 | 0.3510 | 0.0552 | 0.0552 | 200 |
| 1200 | hard_cap | 0.2580 | 0.2580 | 0.2024 | 0.2024 | 200 |
| 1200 | hard_cap_matched | 0.3080 | 0.3080 | 0.2559 | 0.2559 | 200 |
| 1200 | ours_controller_v2_nofallback | 0.3400 | 0.3400 | 0.0612 | 0.0612 | 200 |
| 1200 | probe_only_fixedk_k2 | 0.3600 | 0.3600 | 0.0680 | 0.0680 | 200 |
| 1200 | probe_only_fixedk_k4 | 0.3620 | 0.3620 | 0.0616 | 0.0616 | 200 |
| 1200 | probe_only_fixedk_k8 | 0.3620 | 0.3620 | 0.0602 | 0.0602 | 200 |
| 1200 | probe_adaptive_k_selected | 0.3640 | 0.3640 | 0.0630 | 0.0630 | 200 |
| 1500 | hard_cap | 0.2580 | 0.2580 | 0.1908 | 0.1908 | 200 |
| 1500 | hard_cap_matched | 0.2980 | 0.2980 | 0.2390 | 0.2390 | 200 |
| 1500 | ours_controller_v2_nofallback | 0.3540 | 0.3540 | 0.0620 | 0.0620 | 200 |
| 1500 | probe_only_fixedk_k2 | 0.3560 | 0.3560 | 0.0683 | 0.0683 | 200 |
| 1500 | probe_only_fixedk_k4 | 0.3510 | 0.3510 | 0.0465 | 0.0465 | 200 |
| 1500 | probe_only_fixedk_k8 | 0.3490 | 0.3490 | 0.0416 | 0.0416 | 200 |
| 1500 | probe_adaptive_k_selected | 0.3520 | 0.3520 | 0.0459 | 0.0459 | 200 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 300 | hard_cap | 0.000 | 0.540 | 1.000 |
| 300 | hard_cap_matched | 0.000 | 0.540 | 1.000 |
| 300 | ours_controller_v2_nofallback | 0.000 | 0.523 | 1.000 |
| 300 | probe_only_fixedk_k2 | 0.000 | 0.509 | 1.000 |
| 300 | probe_only_fixedk_k4 | 0.000 | 0.509 | 1.000 |
| 300 | probe_only_fixedk_k8 | 0.000 | 0.509 | 1.000 |
| 300 | probe_adaptive_k_selected | 0.000 | 0.509 | 1.000 |
| 400 | hard_cap | 0.000 | 0.190 | 1.000 |
| 400 | hard_cap_matched | 0.000 | 0.190 | 1.000 |
| 400 | ours_controller_v2_nofallback | 0.000 | 0.196 | 1.000 |
| 400 | probe_only_fixedk_k2 | 0.000 | 0.180 | 1.000 |
| 400 | probe_only_fixedk_k4 | 0.000 | 0.180 | 1.000 |
| 400 | probe_only_fixedk_k8 | 0.000 | 0.180 | 1.000 |
| 400 | probe_adaptive_k_selected | 0.000 | 0.180 | 1.000 |
| 500 | hard_cap | 0.000 | 0.055 | 1.000 |
| 500 | hard_cap_matched | 0.000 | 0.055 | 1.000 |
| 500 | ours_controller_v2_nofallback | 0.000 | 0.073 | 1.000 |
| 500 | probe_only_fixedk_k2 | 0.000 | 0.050 | 1.000 |
| 500 | probe_only_fixedk_k4 | 0.000 | 0.050 | 1.000 |
| 500 | probe_only_fixedk_k8 | 0.000 | 0.050 | 1.000 |
| 500 | probe_adaptive_k_selected | 0.000 | 0.050 | 1.000 |
| 600 | hard_cap | 0.000 | 0.020 | 1.000 |
| 600 | hard_cap_matched | 0.000 | 0.020 | 1.000 |
| 600 | ours_controller_v2_nofallback | 0.000 | 0.074 | 1.000 |
| 600 | probe_only_fixedk_k2 | 0.000 | 0.020 | 1.000 |
| 600 | probe_only_fixedk_k4 | 0.000 | 0.020 | 1.000 |
| 600 | probe_only_fixedk_k8 | 0.000 | 0.020 | 1.000 |
| 600 | probe_adaptive_k_selected | 0.000 | 0.020 | 1.000 |
| 750 | hard_cap | 0.000 | 0.005 | 1.000 |
| 750 | hard_cap_matched | 0.000 | 0.005 | 1.000 |
| 750 | ours_controller_v2_nofallback | 0.000 | 0.059 | 1.000 |
| 750 | probe_only_fixedk_k2 | 0.000 | 0.005 | 1.000 |
| 750 | probe_only_fixedk_k4 | 0.000 | 0.005 | 1.000 |
| 750 | probe_only_fixedk_k8 | 0.000 | 0.005 | 1.000 |
| 750 | probe_adaptive_k_selected | 0.000 | 0.005 | 1.000 |
| 900 | hard_cap | 0.000 | 0.005 | 1.000 |
| 900 | hard_cap_matched | 0.000 | 0.005 | 1.000 |
| 900 | ours_controller_v2_nofallback | 0.000 | 0.077 | 1.000 |
| 900 | probe_only_fixedk_k2 | 0.000 | 0.005 | 1.000 |
| 900 | probe_only_fixedk_k4 | 0.000 | 0.005 | 1.000 |
| 900 | probe_only_fixedk_k8 | 0.000 | 0.005 | 1.000 |
| 900 | probe_adaptive_k_selected | 0.000 | 0.005 | 1.000 |
| 1200 | hard_cap | 0.000 | 0.005 | 1.000 |
| 1200 | hard_cap_matched | 0.000 | 0.005 | 1.000 |
| 1200 | ours_controller_v2_nofallback | 0.000 | 0.047 | 1.000 |
| 1200 | probe_only_fixedk_k2 | 0.000 | 0.005 | 1.000 |
| 1200 | probe_only_fixedk_k4 | 0.000 | 0.005 | 1.000 |
| 1200 | probe_only_fixedk_k8 | 0.000 | 0.005 | 1.000 |
| 1200 | probe_adaptive_k_selected | 0.000 | 0.005 | 1.000 |
| 1500 | hard_cap | 0.000 | 0.005 | 1.000 |
| 1500 | hard_cap_matched | 0.000 | 0.005 | 1.000 |
| 1500 | ours_controller_v2_nofallback | 0.000 | 0.028 | 1.000 |
| 1500 | probe_only_fixedk_k2 | 0.000 | 0.005 | 1.000 |
| 1500 | probe_only_fixedk_k4 | 0.000 | 0.005 | 1.000 |
| 1500 | probe_only_fixedk_k8 | 0.000 | 0.005 | 1.000 |
| 1500 | probe_adaptive_k_selected | 0.000 | 0.005 | 1.000 |

## Method x Budget Parse-Fail Reasons
| Budget | Method | no_budget_for_repair | repair_called_but_failed | invalid_format_unresolved | multi_answer_unresolved | no_answer_token |
|---|---|---:|---:|---:|---:|---:|
| 300 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 300 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 300 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 400 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 400 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 400 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 500 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 500 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 600 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 600 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 600 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 750 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 750 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 750 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 750 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 750 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 750 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 750 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 900 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 900 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 900 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 1200 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 1200 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 1200 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 1200 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 1200 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 1200 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 1200 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 1500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 1500 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 1500 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |

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
| 300 | hard_cap | 137.4 | 0.2680 | 0.1038 | 0.0000 |
| 300 | hard_cap_matched | 137.9 | 0.2680 | 0.1049 | 0.0000 |
| 300 | probe_only_fixedk_k2 | 139.1 | 0.3300 | 0.0523 | 0.0000 |
| 300 | probe_only_fixedk_k4 | 139.1 | 0.3300 | 0.0523 | 0.0000 |
| 300 | probe_only_fixedk_k8 | 139.1 | 0.3300 | 0.0523 | 0.0000 |
| 300 | probe_adaptive_k_selected | 139.1 | 0.3320 | 0.0523 | 0.0000 |
| 300 | ours_controller_v2_nofallback | 148.4 | 0.2440 | 0.0936 | 0.0000 |
| 400 | ours_controller_v2_nofallback | 230.6 | 0.3590 | 0.0661 | 0.0000 |
| 400 | probe_adaptive_k_selected | 238.1 | 0.3610 | 0.0576 | 0.0000 |
| 400 | probe_only_fixedk_k2 | 238.1 | 0.3610 | 0.0616 | 0.0000 |
| 400 | probe_only_fixedk_k4 | 238.9 | 0.3610 | 0.0616 | 0.0000 |
| 400 | probe_only_fixedk_k8 | 238.9 | 0.3610 | 0.0616 | 0.0000 |
| 400 | hard_cap | 243.1 | 0.2650 | 0.1694 | 0.0000 |
| 400 | hard_cap_matched | 243.1 | 0.2650 | 0.1694 | 0.0000 |
| 500 | hard_cap | 298.7 | 0.2780 | 0.2050 | 0.0000 |
| 500 | ours_controller_v2_nofallback | 316.1 | 0.3570 | 0.0786 | 0.0000 |
| 500 | hard_cap_matched | 317.2 | 0.2870 | 0.2287 | 0.0000 |
| 500 | probe_only_fixedk_k2 | 321.9 | 0.3560 | 0.0630 | 0.0000 |
| 500 | probe_adaptive_k_selected | 322.2 | 0.3550 | 0.0616 | 0.0000 |
| 500 | probe_only_fixedk_k4 | 325.7 | 0.3550 | 0.0616 | 0.0000 |
| 500 | probe_only_fixedk_k8 | 325.7 | 0.3550 | 0.0616 | 0.0000 |
| 600 | hard_cap | 316.1 | 0.2530 | 0.1941 | 0.0000 |
| 600 | hard_cap_matched | 354.1 | 0.2730 | 0.2308 | 0.0000 |
| 600 | ours_controller_v2_nofallback | 389.5 | 0.3460 | 0.0821 | 0.0000 |
| 600 | probe_only_fixedk_k2 | 393.1 | 0.3470 | 0.0589 | 0.0000 |
| 600 | probe_adaptive_k_selected | 395.1 | 0.3490 | 0.0566 | 0.0000 |
| 600 | probe_only_fixedk_k4 | 414.5 | 0.3490 | 0.0566 | 0.0000 |
| 600 | probe_only_fixedk_k8 | 414.5 | 0.3490 | 0.0566 | 0.0000 |
| 750 | hard_cap | 325.5 | 0.2440 | 0.2057 | 0.0000 |
| 750 | hard_cap_matched | 374.2 | 0.2740 | 0.2477 | 0.0000 |
| 750 | ours_controller_v2_nofallback | 482.2 | 0.3520 | 0.0674 | 0.0000 |
| 750 | probe_only_fixedk_k2 | 489.8 | 0.3520 | 0.0556 | 0.0000 |
| 750 | probe_adaptive_k_selected | 495.8 | 0.3530 | 0.0455 | 0.0000 |
| 750 | probe_only_fixedk_k4 | 565.9 | 0.3550 | 0.0469 | 0.0000 |
| 750 | probe_only_fixedk_k8 | 568.2 | 0.3550 | 0.0469 | 0.0000 |
| 900 | hard_cap | 325.7 | 0.2640 | 0.1876 | 0.0000 |
| 900 | hard_cap_matched | 379.7 | 0.2980 | 0.2408 | 0.0000 |
| 900 | probe_only_fixedk_k2 | 542.4 | 0.3550 | 0.0598 | 0.0000 |
| 900 | ours_controller_v2_nofallback | 548.8 | 0.3380 | 0.0865 | 0.0000 |
| 900 | probe_adaptive_k_selected | 557.9 | 0.3510 | 0.0552 | 0.0000 |
| 900 | probe_only_fixedk_k4 | 701.1 | 0.3520 | 0.0543 | 0.0000 |
| 900 | probe_only_fixedk_k8 | 715.8 | 0.3520 | 0.0525 | 0.0000 |
| 1200 | hard_cap | 325.0 | 0.2580 | 0.2024 | 0.0000 |
| 1200 | hard_cap_matched | 383.0 | 0.3080 | 0.2559 | 0.0000 |
| 1200 | probe_only_fixedk_k2 | 569.8 | 0.3600 | 0.0680 | 0.0000 |
| 1200 | ours_controller_v2_nofallback | 584.4 | 0.3400 | 0.0612 | 0.0000 |
| 1200 | probe_adaptive_k_selected | 606.5 | 0.3640 | 0.0630 | 0.0000 |
| 1200 | probe_only_fixedk_k4 | 917.4 | 0.3620 | 0.0616 | 0.0000 |
| 1200 | probe_only_fixedk_k8 | 1009.3 | 0.3620 | 0.0602 | 0.0000 |
| 1500 | hard_cap | 325.4 | 0.2580 | 0.1908 | 0.0000 |
| 1500 | hard_cap_matched | 382.6 | 0.2980 | 0.2390 | 0.0000 |
| 1500 | probe_only_fixedk_k2 | 575.0 | 0.3560 | 0.0683 | 0.0000 |
| 1500 | ours_controller_v2_nofallback | 611.5 | 0.3540 | 0.0620 | 0.0000 |
| 1500 | probe_adaptive_k_selected | 624.2 | 0.3520 | 0.0459 | 0.0000 |
| 1500 | probe_only_fixedk_k4 | 1051.4 | 0.3510 | 0.0465 | 0.0000 |
| 1500 | probe_only_fixedk_k8 | 1298.2 | 0.3490 | 0.0416 | 0.0000 |

## nofallback Decision Breakdown
| Budget | Stop@Probe | ContinueSolve | FallbackHardCap | ProbeShare | SolveShare | AvgProbeTok | AvgSolveTok |
|---|---:|---:|---:|---:|---:|---:|---:|
| 300 | 0.000 | 1.000 | 0.000 | 0.000 | 0.724 | 0.0 | 107.4 |
| 400 | 0.789 | 0.211 | 0.000 | 0.918 | 0.007 | 211.8 | 1.7 |
| 500 | 0.922 | 0.078 | 0.000 | 0.974 | 0.000 | 307.9 | 0.0 |
| 600 | 0.925 | 0.075 | 0.000 | 0.989 | 0.000 | 385.1 | 0.0 |
| 750 | 0.938 | 0.062 | 0.000 | 0.992 | 0.000 | 478.4 | 0.0 |
| 900 | 0.917 | 0.083 | 0.000 | 0.990 | 0.002 | 543.5 | 1.3 |
| 1200 | 0.943 | 0.057 | 0.000 | 0.991 | 0.004 | 579.4 | 2.3 |
| 1500 | 0.949 | 0.051 | 0.000 | 0.987 | 0.010 | 603.3 | 6.4 |

## Probe Predictive Signal (nofallback)
- Baseline method for labels: `hard_cap`
| Budget | n trial-pairs | AUC(disagree->base_error) | ECE(disagree->base_error) | n docs | AUC(disagree->base_disagree>0) |
|---|---:|---:|---:|---:|---:|
| 300 | 1000 | 0.500 | 0.268 | 200 | 0.500 |
| 400 | 1000 | 0.499 | 0.640 | 200 | 0.328 |
| 500 | 1000 | 0.502 | 0.686 | 200 | 0.463 |
| 600 | 1000 | 0.524 | 0.701 | 200 | 0.509 |
| 750 | 1000 | 0.513 | 0.725 | 200 | 0.528 |
| 900 | 1000 | 0.498 | 0.694 | 200 | 0.542 |
| 1200 | 1000 | 0.491 | 0.710 | 200 | 0.529 |
| 1500 | 1000 | 0.496 | 0.703 | 200 | 0.558 |

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round8b_heldout_splitB3_r5_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round8b_heldout_splitB3_r5_v1/analysis_summary_round2.json`
