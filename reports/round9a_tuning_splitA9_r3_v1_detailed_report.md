# round9a_tuning_splitA9_r3_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round9a_tuning_splitA9_r3_v1`
- Dataset: `Wanfq/gpqa:gpqa_main:train`, `n_questions=600`, `sample_seed=20260430`
- Methods: `['hard_cap', 'probe_only_fixedk_k2', 'probe_only_fixedk_k4', 'probe_only_fixedk_k8', 'probe_adaptive_k_t67', 'probe_adaptive_k_t75', 'probe_adaptive_k_t80', 'budgeted_self_consistency', 'ours_controller_v3_nofallback']`
- Budgets: `[300, 350, 400, 450, 500, 600, 900, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `64800` completed
- Hard fail: `0`
- Parse fail: `0` (`0.0000%`)
- Repair success: `13932/13932` (`100.0000%`)
- Duration: `395.08` minutes

## Phase Threshold
- nofallback beats hard_cap on incoh with no acc loss first at: `None`
- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `None`
- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `None`
- (parse-excluded) nofallback beats hard_cap on incoh with no acc loss first at: `None`

## nofallback Delta Table
| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |
|---|---:|---:|---:|---:|

## Adaptive Probe vs Probe-Only
| Budget | Adaptive | Probe | Δacc(adapt-probe) | Δincoh(adapt-probe) | Adapt Tok | Probe Tok |
|---|---|---|---:|---:|---:|---:|
| 300 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | -0.0022 | +0.0013 | 143.0 | 143.1 |
| 350 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0011 | +0.0000 | 201.4 | 201.5 |
| 400 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0000 | +0.0000 | 230.8 | 230.8 |
| 450 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0000 | +0.0000 | 274.7 | 274.4 |
| 500 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | -0.0011 | -0.0019 | 326.3 | 326.0 |
| 600 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | -0.0044 | +0.0014 | 406.1 | 404.8 |
| 900 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0022 | -0.0028 | 560.0 | 540.1 |
| 1500 | probe_adaptive_k_t67 | probe_only_fixedk_k2 | +0.0089 | -0.0095 | 649.1 | 597.3 |

## Parse-Fail Sensitivity (Included vs Excluded)
| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |
|---|---|---:|---:|---:|---:|---:|
| 300 | hard_cap | 0.2289 | 0.2289 | 0.0827 | 0.0827 | 300 |
| 300 | probe_only_fixedk_k2 | 0.3100 | 0.3100 | 0.0387 | 0.0387 | 300 |
| 300 | probe_only_fixedk_k4 | 0.3100 | 0.3100 | 0.0387 | 0.0387 | 300 |
| 300 | probe_only_fixedk_k8 | 0.3100 | 0.3100 | 0.0387 | 0.0387 | 300 |
| 300 | probe_adaptive_k_t67 | 0.3078 | 0.3078 | 0.0400 | 0.0400 | 300 |
| 300 | probe_adaptive_k_t75 | 0.3078 | 0.3078 | 0.0400 | 0.0400 | 300 |
| 300 | probe_adaptive_k_t80 | 0.3078 | 0.3078 | 0.0400 | 0.0400 | 300 |
| 300 | budgeted_self_consistency | 0.2644 | 0.2644 | 0.0390 | 0.0390 | 300 |
| 300 | ours_controller_v3_nofallback | 0.2367 | 0.2367 | 0.0000 | 0.0000 | 300 |
| 350 | hard_cap | 0.2433 | 0.2433 | 0.1044 | 0.1044 | 300 |
| 350 | probe_only_fixedk_k2 | 0.3367 | 0.3367 | 0.0551 | 0.0551 | 300 |
| 350 | probe_only_fixedk_k4 | 0.3367 | 0.3367 | 0.0551 | 0.0551 | 300 |
| 350 | probe_only_fixedk_k8 | 0.3367 | 0.3367 | 0.0551 | 0.0551 | 300 |
| 350 | probe_adaptive_k_t67 | 0.3378 | 0.3378 | 0.0551 | 0.0551 | 300 |
| 350 | probe_adaptive_k_t75 | 0.3378 | 0.3378 | 0.0551 | 0.0551 | 300 |
| 350 | probe_adaptive_k_t80 | 0.3378 | 0.3378 | 0.0551 | 0.0551 | 300 |
| 350 | budgeted_self_consistency | 0.2667 | 0.2667 | 0.0711 | 0.0711 | 300 |
| 350 | ours_controller_v3_nofallback | 0.2367 | 0.2367 | 0.0000 | 0.0000 | 300 |
| 400 | hard_cap | 0.2489 | 0.2489 | 0.1261 | 0.1261 | 300 |
| 400 | probe_only_fixedk_k2 | 0.3578 | 0.3578 | 0.0549 | 0.0549 | 300 |
| 400 | probe_only_fixedk_k4 | 0.3578 | 0.3578 | 0.0549 | 0.0549 | 300 |
| 400 | probe_only_fixedk_k8 | 0.3578 | 0.3578 | 0.0549 | 0.0549 | 300 |
| 400 | probe_adaptive_k_t67 | 0.3578 | 0.3578 | 0.0549 | 0.0549 | 300 |
| 400 | probe_adaptive_k_t75 | 0.3578 | 0.3578 | 0.0549 | 0.0549 | 300 |
| 400 | probe_adaptive_k_t80 | 0.3578 | 0.3578 | 0.0549 | 0.0549 | 300 |
| 400 | budgeted_self_consistency | 0.2722 | 0.2722 | 0.0750 | 0.0750 | 300 |
| 400 | ours_controller_v3_nofallback | 0.2367 | 0.2367 | 0.0000 | 0.0000 | 300 |
| 450 | hard_cap | 0.2711 | 0.2711 | 0.1412 | 0.1412 | 300 |
| 450 | probe_only_fixedk_k2 | 0.3800 | 0.3800 | 0.0574 | 0.0574 | 300 |
| 450 | probe_only_fixedk_k4 | 0.3800 | 0.3800 | 0.0574 | 0.0574 | 300 |
| 450 | probe_only_fixedk_k8 | 0.3800 | 0.3800 | 0.0574 | 0.0574 | 300 |
| 450 | probe_adaptive_k_t67 | 0.3800 | 0.3800 | 0.0574 | 0.0574 | 300 |
| 450 | probe_adaptive_k_t75 | 0.3800 | 0.3800 | 0.0574 | 0.0574 | 300 |
| 450 | probe_adaptive_k_t80 | 0.3800 | 0.3800 | 0.0574 | 0.0574 | 300 |
| 450 | budgeted_self_consistency | 0.2878 | 0.2878 | 0.0918 | 0.0918 | 300 |
| 450 | ours_controller_v3_nofallback | 0.2367 | 0.2367 | 0.0000 | 0.0000 | 300 |
| 500 | hard_cap | 0.2644 | 0.2644 | 0.1608 | 0.1608 | 300 |
| 500 | probe_only_fixedk_k2 | 0.3844 | 0.3844 | 0.0529 | 0.0529 | 300 |
| 500 | probe_only_fixedk_k4 | 0.3856 | 0.3856 | 0.0529 | 0.0529 | 300 |
| 500 | probe_only_fixedk_k8 | 0.3856 | 0.3856 | 0.0529 | 0.0529 | 300 |
| 500 | probe_adaptive_k_t67 | 0.3833 | 0.3833 | 0.0510 | 0.0510 | 300 |
| 500 | probe_adaptive_k_t75 | 0.3833 | 0.3833 | 0.0510 | 0.0510 | 300 |
| 500 | probe_adaptive_k_t80 | 0.3833 | 0.3833 | 0.0510 | 0.0510 | 300 |
| 500 | budgeted_self_consistency | 0.2911 | 0.2911 | 0.1050 | 0.1050 | 300 |
| 500 | ours_controller_v3_nofallback | 0.2356 | 0.2356 | 0.0029 | 0.0029 | 300 |
| 600 | hard_cap | 0.2667 | 0.2667 | 0.1490 | 0.1490 | 300 |
| 600 | probe_only_fixedk_k2 | 0.3856 | 0.3856 | 0.0537 | 0.0537 | 300 |
| 600 | probe_only_fixedk_k4 | 0.3811 | 0.3811 | 0.0551 | 0.0551 | 300 |
| 600 | probe_only_fixedk_k8 | 0.3811 | 0.3811 | 0.0551 | 0.0551 | 300 |
| 600 | probe_adaptive_k_t67 | 0.3811 | 0.3811 | 0.0551 | 0.0551 | 300 |
| 600 | probe_adaptive_k_t75 | 0.3811 | 0.3811 | 0.0551 | 0.0551 | 300 |
| 600 | probe_adaptive_k_t80 | 0.3811 | 0.3811 | 0.0551 | 0.0551 | 300 |
| 600 | budgeted_self_consistency | 0.2833 | 0.2833 | 0.1053 | 0.1053 | 300 |
| 600 | ours_controller_v3_nofallback | 0.2422 | 0.2422 | 0.0145 | 0.0145 | 300 |
| 900 | hard_cap | 0.2578 | 0.2578 | 0.1734 | 0.1734 | 300 |
| 900 | probe_only_fixedk_k2 | 0.3822 | 0.3822 | 0.0480 | 0.0480 | 300 |
| 900 | probe_only_fixedk_k4 | 0.3822 | 0.3822 | 0.0466 | 0.0466 | 300 |
| 900 | probe_only_fixedk_k8 | 0.3844 | 0.3844 | 0.0452 | 0.0452 | 300 |
| 900 | probe_adaptive_k_t67 | 0.3844 | 0.3844 | 0.0452 | 0.0452 | 300 |
| 900 | probe_adaptive_k_t75 | 0.3844 | 0.3844 | 0.0452 | 0.0452 | 300 |
| 900 | probe_adaptive_k_t80 | 0.3844 | 0.3844 | 0.0452 | 0.0452 | 300 |
| 900 | budgeted_self_consistency | 0.2778 | 0.2778 | 0.1004 | 0.1004 | 300 |
| 900 | ours_controller_v3_nofallback | 0.3800 | 0.3800 | 0.0653 | 0.0653 | 300 |
| 1500 | hard_cap | 0.2678 | 0.2678 | 0.1731 | 0.1731 | 300 |
| 1500 | probe_only_fixedk_k2 | 0.3900 | 0.3900 | 0.0537 | 0.0537 | 300 |
| 1500 | probe_only_fixedk_k4 | 0.3944 | 0.3944 | 0.0457 | 0.0457 | 300 |
| 1500 | probe_only_fixedk_k8 | 0.3956 | 0.3956 | 0.0426 | 0.0426 | 300 |
| 1500 | probe_adaptive_k_t67 | 0.3989 | 0.3989 | 0.0442 | 0.0442 | 300 |
| 1500 | probe_adaptive_k_t75 | 0.3989 | 0.3989 | 0.0442 | 0.0442 | 300 |
| 1500 | probe_adaptive_k_t80 | 0.3989 | 0.3989 | 0.0442 | 0.0442 | 300 |
| 1500 | budgeted_self_consistency | 0.2733 | 0.2733 | 0.0917 | 0.0917 | 300 |
| 1500 | ours_controller_v3_nofallback | 0.3900 | 0.3900 | 0.0586 | 0.0586 | 300 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 300 | hard_cap | 0.000 | 0.490 | 1.000 |
| 300 | probe_only_fixedk_k2 | 0.000 | 0.489 | 1.000 |
| 300 | probe_only_fixedk_k4 | 0.000 | 0.489 | 1.000 |
| 300 | probe_only_fixedk_k8 | 0.000 | 0.489 | 1.000 |
| 300 | probe_adaptive_k_t67 | 0.000 | 0.488 | 1.000 |
| 300 | probe_adaptive_k_t75 | 0.000 | 0.488 | 1.000 |
| 300 | probe_adaptive_k_t80 | 0.000 | 0.488 | 1.000 |
| 300 | budgeted_self_consistency | 0.000 | 0.513 | 1.000 |
| 300 | ours_controller_v3_nofallback | 0.000 | 1.000 | 1.000 |
| 350 | hard_cap | 0.000 | 0.293 | 1.000 |
| 350 | probe_only_fixedk_k2 | 0.000 | 0.272 | 1.000 |
| 350 | probe_only_fixedk_k4 | 0.000 | 0.272 | 1.000 |
| 350 | probe_only_fixedk_k8 | 0.000 | 0.272 | 1.000 |
| 350 | probe_adaptive_k_t67 | 0.000 | 0.271 | 1.000 |
| 350 | probe_adaptive_k_t75 | 0.000 | 0.271 | 1.000 |
| 350 | probe_adaptive_k_t80 | 0.000 | 0.271 | 1.000 |
| 350 | budgeted_self_consistency | 0.000 | 0.303 | 1.000 |
| 350 | ours_controller_v3_nofallback | 0.000 | 1.000 | 1.000 |
| 400 | hard_cap | 0.000 | 0.193 | 1.000 |
| 400 | probe_only_fixedk_k2 | 0.000 | 0.183 | 1.000 |
| 400 | probe_only_fixedk_k4 | 0.000 | 0.183 | 1.000 |
| 400 | probe_only_fixedk_k8 | 0.000 | 0.183 | 1.000 |
| 400 | probe_adaptive_k_t67 | 0.000 | 0.183 | 1.000 |
| 400 | probe_adaptive_k_t75 | 0.000 | 0.183 | 1.000 |
| 400 | probe_adaptive_k_t80 | 0.000 | 0.183 | 1.000 |
| 400 | budgeted_self_consistency | 0.000 | 0.200 | 1.000 |
| 400 | ours_controller_v3_nofallback | 0.000 | 1.000 | 1.000 |
| 450 | hard_cap | 0.000 | 0.113 | 1.000 |
| 450 | probe_only_fixedk_k2 | 0.000 | 0.113 | 1.000 |
| 450 | probe_only_fixedk_k4 | 0.000 | 0.113 | 1.000 |
| 450 | probe_only_fixedk_k8 | 0.000 | 0.113 | 1.000 |
| 450 | probe_adaptive_k_t67 | 0.000 | 0.113 | 1.000 |
| 450 | probe_adaptive_k_t75 | 0.000 | 0.113 | 1.000 |
| 450 | probe_adaptive_k_t80 | 0.000 | 0.113 | 1.000 |
| 450 | budgeted_self_consistency | 0.000 | 0.127 | 1.000 |
| 450 | ours_controller_v3_nofallback | 0.000 | 0.993 | 1.000 |
| 500 | hard_cap | 0.000 | 0.080 | 1.000 |
| 500 | probe_only_fixedk_k2 | 0.000 | 0.073 | 1.000 |
| 500 | probe_only_fixedk_k4 | 0.000 | 0.073 | 1.000 |
| 500 | probe_only_fixedk_k8 | 0.000 | 0.073 | 1.000 |
| 500 | probe_adaptive_k_t67 | 0.000 | 0.073 | 1.000 |
| 500 | probe_adaptive_k_t75 | 0.000 | 0.073 | 1.000 |
| 500 | probe_adaptive_k_t80 | 0.000 | 0.073 | 1.000 |
| 500 | budgeted_self_consistency | 0.000 | 0.083 | 1.000 |
| 500 | ours_controller_v3_nofallback | 0.000 | 0.980 | 1.000 |
| 600 | hard_cap | 0.000 | 0.033 | 1.000 |
| 600 | probe_only_fixedk_k2 | 0.000 | 0.033 | 1.000 |
| 600 | probe_only_fixedk_k4 | 0.000 | 0.033 | 1.000 |
| 600 | probe_only_fixedk_k8 | 0.000 | 0.033 | 1.000 |
| 600 | probe_adaptive_k_t67 | 0.000 | 0.033 | 1.000 |
| 600 | probe_adaptive_k_t75 | 0.000 | 0.033 | 1.000 |
| 600 | probe_adaptive_k_t80 | 0.000 | 0.033 | 1.000 |
| 600 | budgeted_self_consistency | 0.000 | 0.033 | 1.000 |
| 600 | ours_controller_v3_nofallback | 0.000 | 0.917 | 1.000 |
| 900 | hard_cap | 0.000 | 0.007 | 1.000 |
| 900 | probe_only_fixedk_k2 | 0.000 | 0.007 | 1.000 |
| 900 | probe_only_fixedk_k4 | 0.000 | 0.007 | 1.000 |
| 900 | probe_only_fixedk_k8 | 0.000 | 0.007 | 1.000 |
| 900 | probe_adaptive_k_t67 | 0.000 | 0.007 | 1.000 |
| 900 | probe_adaptive_k_t75 | 0.000 | 0.007 | 1.000 |
| 900 | probe_adaptive_k_t80 | 0.000 | 0.007 | 1.000 |
| 900 | budgeted_self_consistency | 0.000 | 0.007 | 1.000 |
| 900 | ours_controller_v3_nofallback | 0.000 | 0.074 | 1.000 |
| 1500 | hard_cap | 0.000 | 0.000 | 0.000 |
| 1500 | probe_only_fixedk_k2 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_only_fixedk_k4 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_only_fixedk_k8 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_adaptive_k_t67 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_adaptive_k_t75 | 0.000 | 0.000 | 0.000 |
| 1500 | probe_adaptive_k_t80 | 0.000 | 0.000 | 0.000 |
| 1500 | budgeted_self_consistency | 0.000 | 0.000 | 0.000 |
| 1500 | ours_controller_v3_nofallback | 0.000 | 0.019 | 1.000 |

## Method x Budget Parse-Fail Reasons
| Budget | Method | no_budget_for_repair | repair_called_but_failed | invalid_format_unresolved | multi_answer_unresolved | no_answer_token |
|---|---|---:|---:|---:|---:|---:|
| 300 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 300 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 300 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 350 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 350 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 350 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 350 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 350 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 350 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 350 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 350 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 350 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 400 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 400 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 400 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 450 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 450 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 450 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 450 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 450 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 450 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 450 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 450 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 450 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 500 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 500 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 600 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 600 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 600 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 900 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 900 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 900 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 1500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_adaptive_k_t67 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_adaptive_k_t75 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_adaptive_k_t80 | 0 | 0 | 0 | 0 | 0 |
| 1500 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 1500 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |

## Parse-Fail Gating Check
| Budget | Max ParseFail | Min ParseFail | Spread | Gate(max<=1%) | Gate(spread<=1%p) |
|---|---:|---:|---:|---:|---:|
| 300 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 350 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 400 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 450 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 500 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 600 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 900 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 1500 | 0.000 | 0.000 | 0.000 | 1 | 1 |

## Cost Reality (Actual Total Tokens)
| Budget | Method | AvgTotalTok | Accuracy | Incoherence | ParseFail |
|---|---|---:|---:|---:|---:|
| 300 | budgeted_self_consistency | 142.4 | 0.2644 | 0.0390 | 0.0000 |
| 300 | probe_adaptive_k_t67 | 143.0 | 0.3078 | 0.0400 | 0.0000 |
| 300 | probe_adaptive_k_t75 | 143.0 | 0.3078 | 0.0400 | 0.0000 |
| 300 | probe_adaptive_k_t80 | 143.0 | 0.3078 | 0.0400 | 0.0000 |
| 300 | probe_only_fixedk_k2 | 143.1 | 0.3100 | 0.0387 | 0.0000 |
| 300 | probe_only_fixedk_k4 | 143.1 | 0.3100 | 0.0387 | 0.0000 |
| 300 | probe_only_fixedk_k8 | 143.1 | 0.3100 | 0.0387 | 0.0000 |
| 300 | hard_cap | 144.7 | 0.2289 | 0.0827 | 0.0000 |
| 300 | ours_controller_v3_nofallback | 156.1 | 0.2367 | 0.0000 | 0.0000 |
| 350 | budgeted_self_consistency | 195.8 | 0.2667 | 0.0711 | 0.0000 |
| 350 | probe_adaptive_k_t67 | 201.4 | 0.3378 | 0.0551 | 0.0000 |
| 350 | probe_adaptive_k_t75 | 201.4 | 0.3378 | 0.0551 | 0.0000 |
| 350 | probe_adaptive_k_t80 | 201.4 | 0.3378 | 0.0551 | 0.0000 |
| 350 | probe_only_fixedk_k2 | 201.5 | 0.3367 | 0.0551 | 0.0000 |
| 350 | probe_only_fixedk_k4 | 201.5 | 0.3367 | 0.0551 | 0.0000 |
| 350 | probe_only_fixedk_k8 | 201.5 | 0.3367 | 0.0551 | 0.0000 |
| 350 | hard_cap | 202.6 | 0.2433 | 0.1044 | 0.0000 |
| 350 | ours_controller_v3_nofallback | 215.2 | 0.2367 | 0.0000 | 0.0000 |
| 400 | probe_only_fixedk_k2 | 230.8 | 0.3578 | 0.0549 | 0.0000 |
| 400 | probe_only_fixedk_k4 | 230.8 | 0.3578 | 0.0549 | 0.0000 |
| 400 | probe_only_fixedk_k8 | 230.8 | 0.3578 | 0.0549 | 0.0000 |
| 400 | probe_adaptive_k_t67 | 230.8 | 0.3578 | 0.0549 | 0.0000 |
| 400 | probe_adaptive_k_t75 | 230.8 | 0.3578 | 0.0549 | 0.0000 |
| 400 | probe_adaptive_k_t80 | 230.8 | 0.3578 | 0.0549 | 0.0000 |
| 400 | budgeted_self_consistency | 234.8 | 0.2722 | 0.0750 | 0.0000 |
| 400 | hard_cap | 237.4 | 0.2489 | 0.1261 | 0.0000 |
| 400 | ours_controller_v3_nofallback | 258.1 | 0.2367 | 0.0000 | 0.0000 |
| 450 | hard_cap | 266.9 | 0.2711 | 0.1412 | 0.0000 |
| 450 | probe_only_fixedk_k2 | 274.4 | 0.3800 | 0.0574 | 0.0000 |
| 450 | probe_adaptive_k_t67 | 274.7 | 0.3800 | 0.0574 | 0.0000 |
| 450 | probe_adaptive_k_t75 | 274.7 | 0.3800 | 0.0574 | 0.0000 |
| 450 | probe_adaptive_k_t80 | 274.7 | 0.3800 | 0.0574 | 0.0000 |
| 450 | budgeted_self_consistency | 275.5 | 0.2878 | 0.0918 | 0.0000 |
| 450 | probe_only_fixedk_k4 | 275.8 | 0.3800 | 0.0574 | 0.0000 |
| 450 | probe_only_fixedk_k8 | 275.8 | 0.3800 | 0.0574 | 0.0000 |
| 450 | ours_controller_v3_nofallback | 318.0 | 0.2367 | 0.0000 | 0.0000 |
| 500 | hard_cap | 283.2 | 0.2644 | 0.1608 | 0.0000 |
| 500 | probe_only_fixedk_k2 | 326.0 | 0.3844 | 0.0529 | 0.0000 |
| 500 | budgeted_self_consistency | 326.2 | 0.2911 | 0.1050 | 0.0000 |
| 500 | probe_adaptive_k_t67 | 326.3 | 0.3833 | 0.0510 | 0.0000 |
| 500 | probe_adaptive_k_t75 | 326.3 | 0.3833 | 0.0510 | 0.0000 |
| 500 | probe_adaptive_k_t80 | 326.3 | 0.3833 | 0.0510 | 0.0000 |
| 500 | probe_only_fixedk_k4 | 329.4 | 0.3856 | 0.0529 | 0.0000 |
| 500 | probe_only_fixedk_k8 | 329.4 | 0.3856 | 0.0529 | 0.0000 |
| 500 | ours_controller_v3_nofallback | 367.1 | 0.2356 | 0.0029 | 0.0000 |
| 600 | hard_cap | 306.8 | 0.2667 | 0.1490 | 0.0000 |
| 600 | probe_only_fixedk_k2 | 404.8 | 0.3856 | 0.0537 | 0.0000 |
| 600 | probe_adaptive_k_t67 | 406.1 | 0.3811 | 0.0551 | 0.0000 |
| 600 | probe_adaptive_k_t75 | 406.1 | 0.3811 | 0.0551 | 0.0000 |
| 600 | probe_adaptive_k_t80 | 406.1 | 0.3811 | 0.0551 | 0.0000 |
| 600 | probe_only_fixedk_k4 | 420.0 | 0.3811 | 0.0551 | 0.0000 |
| 600 | probe_only_fixedk_k8 | 420.0 | 0.3811 | 0.0551 | 0.0000 |
| 600 | budgeted_self_consistency | 420.9 | 0.2833 | 0.1053 | 0.0000 |
| 600 | ours_controller_v3_nofallback | 464.3 | 0.2422 | 0.0145 | 0.0000 |
| 900 | hard_cap | 325.0 | 0.2578 | 0.1734 | 0.0000 |
| 900 | probe_only_fixedk_k2 | 540.1 | 0.3822 | 0.0480 | 0.0000 |
| 900 | ours_controller_v3_nofallback | 546.3 | 0.3800 | 0.0653 | 0.0000 |
| 900 | probe_adaptive_k_t67 | 560.0 | 0.3844 | 0.0452 | 0.0000 |
| 900 | probe_adaptive_k_t75 | 560.0 | 0.3844 | 0.0452 | 0.0000 |
| 900 | probe_adaptive_k_t80 | 560.4 | 0.3844 | 0.0452 | 0.0000 |
| 900 | probe_only_fixedk_k4 | 705.3 | 0.3822 | 0.0466 | 0.0000 |
| 900 | budgeted_self_consistency | 710.2 | 0.2778 | 0.1004 | 0.0000 |
| 900 | probe_only_fixedk_k8 | 715.6 | 0.3844 | 0.0452 | 0.0000 |
| 1500 | hard_cap | 331.2 | 0.2678 | 0.1731 | 0.0000 |
| 1500 | probe_only_fixedk_k2 | 597.3 | 0.3900 | 0.0537 | 0.0000 |
| 1500 | ours_controller_v3_nofallback | 627.8 | 0.3900 | 0.0586 | 0.0000 |
| 1500 | probe_adaptive_k_t67 | 649.1 | 0.3989 | 0.0442 | 0.0000 |
| 1500 | probe_adaptive_k_t75 | 649.1 | 0.3989 | 0.0442 | 0.0000 |
| 1500 | probe_adaptive_k_t80 | 664.3 | 0.3989 | 0.0442 | 0.0000 |
| 1500 | probe_only_fixedk_k4 | 1058.9 | 0.3944 | 0.0457 | 0.0000 |
| 1500 | budgeted_self_consistency | 1134.3 | 0.2733 | 0.0917 | 0.0000 |
| 1500 | probe_only_fixedk_k8 | 1308.6 | 0.3956 | 0.0426 | 0.0000 |

## nofallback Decision Breakdown
| Budget | Stop@Probe | ContinueSolve | FallbackHardCap | ProbeShare | SolveShare | AvgProbeTok | AvgSolveTok |
|---|---:|---:|---:|---:|---:|---:|---:|
| 300 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |
| 350 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |
| 400 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |
| 450 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |
| 500 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |
| 600 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |
| 900 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |
| 1500 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |

## Probe Predictive Signal (nofallback)
- Baseline method for labels: `hard_cap`
| Budget | n trial-pairs | AUC(disagree->base_error) | ECE(disagree->base_error) | n docs | AUC(disagree->base_disagree>0) |
|---|---:|---:|---:|---:|---:|

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round9a_tuning_splitA9_r3_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round9a_tuning_splitA9_r3_v1/analysis_summary_round2.json`
