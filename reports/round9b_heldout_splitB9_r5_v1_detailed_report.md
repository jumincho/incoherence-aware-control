# round9b_heldout_splitB9_r5_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round9b_heldout_splitB9_r5_v1`
- Dataset: `Wanfq/gpqa:gpqa_main:train`, `n_questions=600`, `sample_seed=20260430`
- Methods: `['hard_cap', 'hard_cap_matched', 'probe_only_fixedk_k2', 'probe_only_fixedk_k4', 'probe_only_fixedk_k8', 'probe_adaptive_k_selected', 'budgeted_self_consistency', 'ours_controller_v3_nofallback']`
- Budgets: `[300, 350, 400, 450, 500, 600, 900, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `47360` completed
- Hard fail: `0`
- Parse fail: `0` (`0.0000%`)
- Repair success: `9965/9965` (`100.0000%`)
- Duration: `313.13` minutes

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
| 300 | probe_adaptive_k_selected | probe_only_fixedk_k2 | +0.0014 | -0.0019 | 150.1 | 150.1 |
| 350 | probe_adaptive_k_selected | probe_only_fixedk_k2 | +0.0000 | +0.0019 | 203.7 | 203.7 |
| 400 | probe_adaptive_k_selected | probe_only_fixedk_k2 | +0.0000 | +0.0000 | 250.5 | 250.5 |
| 450 | probe_adaptive_k_selected | probe_only_fixedk_k2 | +0.0000 | +0.0000 | 289.2 | 289.2 |
| 500 | probe_adaptive_k_selected | probe_only_fixedk_k2 | +0.0014 | -0.0020 | 326.8 | 326.4 |
| 600 | probe_adaptive_k_selected | probe_only_fixedk_k2 | +0.0000 | -0.0020 | 398.7 | 398.1 |
| 900 | probe_adaptive_k_selected | probe_only_fixedk_k2 | -0.0095 | -0.0145 | 558.5 | 539.2 |
| 1500 | probe_adaptive_k_selected | probe_only_fixedk_k2 | -0.0081 | -0.0161 | 626.3 | 576.7 |

## Parse-Fail Sensitivity (Included vs Excluded)
| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |
|---|---|---:|---:|---:|---:|---:|
| 300 | hard_cap | 0.2797 | 0.2797 | 0.0986 | 0.0986 | 148 |
| 300 | hard_cap_matched | 0.2838 | 0.2838 | 0.1032 | 0.1032 | 148 |
| 300 | probe_only_fixedk_k2 | 0.3284 | 0.3284 | 0.0370 | 0.0370 | 148 |
| 300 | probe_only_fixedk_k4 | 0.3284 | 0.3284 | 0.0370 | 0.0370 | 148 |
| 300 | probe_only_fixedk_k8 | 0.3284 | 0.3284 | 0.0370 | 0.0370 | 148 |
| 300 | probe_adaptive_k_selected | 0.3297 | 0.3297 | 0.0351 | 0.0351 | 148 |
| 300 | budgeted_self_consistency | 0.3351 | 0.3351 | 0.0559 | 0.0559 | 148 |
| 300 | ours_controller_v3_nofallback | 0.2568 | 0.2568 | 0.0000 | 0.0000 | 148 |
| 350 | hard_cap | 0.2824 | 0.2824 | 0.1613 | 0.1613 | 148 |
| 350 | hard_cap_matched | 0.2865 | 0.2865 | 0.1545 | 0.1545 | 148 |
| 350 | probe_only_fixedk_k2 | 0.3743 | 0.3743 | 0.0600 | 0.0600 | 148 |
| 350 | probe_only_fixedk_k4 | 0.3743 | 0.3743 | 0.0600 | 0.0600 | 148 |
| 350 | probe_only_fixedk_k8 | 0.3743 | 0.3743 | 0.0600 | 0.0600 | 148 |
| 350 | probe_adaptive_k_selected | 0.3743 | 0.3743 | 0.0619 | 0.0619 | 148 |
| 350 | budgeted_self_consistency | 0.3419 | 0.3419 | 0.1028 | 0.1028 | 148 |
| 350 | ours_controller_v3_nofallback | 0.2568 | 0.2568 | 0.0000 | 0.0000 | 148 |
| 400 | hard_cap | 0.2892 | 0.2892 | 0.1783 | 0.1783 | 148 |
| 400 | hard_cap_matched | 0.2905 | 0.2905 | 0.1848 | 0.1848 | 148 |
| 400 | probe_only_fixedk_k2 | 0.4027 | 0.4027 | 0.0671 | 0.0671 | 148 |
| 400 | probe_only_fixedk_k4 | 0.4027 | 0.4027 | 0.0671 | 0.0671 | 148 |
| 400 | probe_only_fixedk_k8 | 0.4027 | 0.4027 | 0.0671 | 0.0671 | 148 |
| 400 | probe_adaptive_k_selected | 0.4027 | 0.4027 | 0.0671 | 0.0671 | 148 |
| 400 | budgeted_self_consistency | 0.3500 | 0.3500 | 0.1239 | 0.1239 | 148 |
| 400 | ours_controller_v3_nofallback | 0.2568 | 0.2568 | 0.0000 | 0.0000 | 148 |
| 450 | hard_cap | 0.3054 | 0.3054 | 0.1862 | 0.1862 | 148 |
| 450 | hard_cap_matched | 0.3054 | 0.3054 | 0.2217 | 0.2217 | 148 |
| 450 | probe_only_fixedk_k2 | 0.3959 | 0.3959 | 0.0855 | 0.0855 | 148 |
| 450 | probe_only_fixedk_k4 | 0.3959 | 0.3959 | 0.0855 | 0.0855 | 148 |
| 450 | probe_only_fixedk_k8 | 0.3959 | 0.3959 | 0.0855 | 0.0855 | 148 |
| 450 | probe_adaptive_k_selected | 0.3959 | 0.3959 | 0.0855 | 0.0855 | 148 |
| 450 | budgeted_self_consistency | 0.3432 | 0.3432 | 0.1084 | 0.1084 | 148 |
| 450 | ours_controller_v3_nofallback | 0.2568 | 0.2568 | 0.0000 | 0.0000 | 148 |
| 500 | hard_cap | 0.3203 | 0.3203 | 0.2093 | 0.2093 | 148 |
| 500 | hard_cap_matched | 0.3216 | 0.3216 | 0.2344 | 0.2344 | 148 |
| 500 | probe_only_fixedk_k2 | 0.4068 | 0.4068 | 0.0705 | 0.0705 | 148 |
| 500 | probe_only_fixedk_k4 | 0.4068 | 0.4068 | 0.0665 | 0.0665 | 148 |
| 500 | probe_only_fixedk_k8 | 0.4068 | 0.4068 | 0.0665 | 0.0665 | 148 |
| 500 | probe_adaptive_k_selected | 0.4081 | 0.4081 | 0.0685 | 0.0685 | 148 |
| 500 | budgeted_self_consistency | 0.3149 | 0.3149 | 0.1166 | 0.1166 | 148 |
| 500 | ours_controller_v3_nofallback | 0.2595 | 0.2595 | 0.0126 | 0.0126 | 148 |
| 600 | hard_cap | 0.2973 | 0.2973 | 0.1864 | 0.1864 | 148 |
| 600 | hard_cap_matched | 0.3351 | 0.3351 | 0.2217 | 0.2217 | 148 |
| 600 | probe_only_fixedk_k2 | 0.3986 | 0.3986 | 0.0705 | 0.0705 | 148 |
| 600 | probe_only_fixedk_k4 | 0.3986 | 0.3986 | 0.0685 | 0.0685 | 148 |
| 600 | probe_only_fixedk_k8 | 0.3986 | 0.3986 | 0.0685 | 0.0685 | 148 |
| 600 | probe_adaptive_k_selected | 0.3986 | 0.3986 | 0.0685 | 0.0685 | 148 |
| 600 | budgeted_self_consistency | 0.3338 | 0.3338 | 0.1364 | 0.1364 | 148 |
| 600 | ours_controller_v3_nofallback | 0.2500 | 0.2500 | 0.0175 | 0.0175 | 148 |
| 900 | hard_cap | 0.2905 | 0.2905 | 0.1915 | 0.1915 | 148 |
| 900 | hard_cap_matched | 0.3189 | 0.3189 | 0.2433 | 0.2433 | 148 |
| 900 | probe_only_fixedk_k2 | 0.4108 | 0.4108 | 0.0611 | 0.0611 | 148 |
| 900 | probe_only_fixedk_k4 | 0.4014 | 0.4014 | 0.0466 | 0.0466 | 148 |
| 900 | probe_only_fixedk_k8 | 0.4014 | 0.4014 | 0.0466 | 0.0466 | 148 |
| 900 | probe_adaptive_k_selected | 0.4014 | 0.4014 | 0.0466 | 0.0466 | 148 |
| 900 | budgeted_self_consistency | 0.3432 | 0.3432 | 0.1176 | 0.1176 | 148 |
| 900 | ours_controller_v3_nofallback | 0.3892 | 0.3892 | 0.0506 | 0.0506 | 148 |
| 1500 | hard_cap | 0.2946 | 0.2946 | 0.1981 | 0.1981 | 148 |
| 1500 | hard_cap_matched | 0.3027 | 0.3027 | 0.2464 | 0.2464 | 148 |
| 1500 | probe_only_fixedk_k2 | 0.4135 | 0.4135 | 0.0678 | 0.0678 | 148 |
| 1500 | probe_only_fixedk_k4 | 0.4095 | 0.4095 | 0.0558 | 0.0558 | 148 |
| 1500 | probe_only_fixedk_k8 | 0.4081 | 0.4081 | 0.0523 | 0.0523 | 148 |
| 1500 | probe_adaptive_k_selected | 0.4054 | 0.4054 | 0.0517 | 0.0517 | 148 |
| 1500 | budgeted_self_consistency | 0.3459 | 0.3459 | 0.1223 | 0.1223 | 148 |
| 1500 | ours_controller_v3_nofallback | 0.4027 | 0.4027 | 0.0430 | 0.0430 | 148 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 300 | hard_cap | 0.000 | 0.514 | 1.000 |
| 300 | hard_cap_matched | 0.000 | 0.514 | 1.000 |
| 300 | probe_only_fixedk_k2 | 0.000 | 0.484 | 1.000 |
| 300 | probe_only_fixedk_k4 | 0.000 | 0.484 | 1.000 |
| 300 | probe_only_fixedk_k8 | 0.000 | 0.484 | 1.000 |
| 300 | probe_adaptive_k_selected | 0.000 | 0.484 | 1.000 |
| 300 | budgeted_self_consistency | 0.000 | 0.534 | 1.000 |
| 300 | ours_controller_v3_nofallback | 0.000 | 1.000 | 1.000 |
| 350 | hard_cap | 0.000 | 0.270 | 1.000 |
| 350 | hard_cap_matched | 0.000 | 0.270 | 1.000 |
| 350 | probe_only_fixedk_k2 | 0.000 | 0.284 | 1.000 |
| 350 | probe_only_fixedk_k4 | 0.000 | 0.284 | 1.000 |
| 350 | probe_only_fixedk_k8 | 0.000 | 0.284 | 1.000 |
| 350 | probe_adaptive_k_selected | 0.000 | 0.284 | 1.000 |
| 350 | budgeted_self_consistency | 0.000 | 0.304 | 1.000 |
| 350 | ours_controller_v3_nofallback | 0.000 | 1.000 | 1.000 |
| 400 | hard_cap | 0.000 | 0.142 | 1.000 |
| 400 | hard_cap_matched | 0.000 | 0.142 | 1.000 |
| 400 | probe_only_fixedk_k2 | 0.000 | 0.135 | 1.000 |
| 400 | probe_only_fixedk_k4 | 0.000 | 0.135 | 1.000 |
| 400 | probe_only_fixedk_k8 | 0.000 | 0.135 | 1.000 |
| 400 | probe_adaptive_k_selected | 0.000 | 0.135 | 1.000 |
| 400 | budgeted_self_consistency | 0.000 | 0.142 | 1.000 |
| 400 | ours_controller_v3_nofallback | 0.000 | 0.993 | 1.000 |
| 450 | hard_cap | 0.000 | 0.074 | 1.000 |
| 450 | hard_cap_matched | 0.000 | 0.074 | 1.000 |
| 450 | probe_only_fixedk_k2 | 0.000 | 0.068 | 1.000 |
| 450 | probe_only_fixedk_k4 | 0.000 | 0.068 | 1.000 |
| 450 | probe_only_fixedk_k8 | 0.000 | 0.068 | 1.000 |
| 450 | probe_adaptive_k_selected | 0.000 | 0.068 | 1.000 |
| 450 | budgeted_self_consistency | 0.000 | 0.074 | 1.000 |
| 450 | ours_controller_v3_nofallback | 0.000 | 0.989 | 1.000 |
| 500 | hard_cap | 0.000 | 0.047 | 1.000 |
| 500 | hard_cap_matched | 0.000 | 0.047 | 1.000 |
| 500 | probe_only_fixedk_k2 | 0.000 | 0.041 | 1.000 |
| 500 | probe_only_fixedk_k4 | 0.000 | 0.041 | 1.000 |
| 500 | probe_only_fixedk_k8 | 0.000 | 0.041 | 1.000 |
| 500 | probe_adaptive_k_selected | 0.000 | 0.041 | 1.000 |
| 500 | budgeted_self_consistency | 0.000 | 0.047 | 1.000 |
| 500 | ours_controller_v3_nofallback | 0.000 | 0.959 | 1.000 |
| 600 | hard_cap | 0.000 | 0.027 | 1.000 |
| 600 | hard_cap_matched | 0.000 | 0.027 | 1.000 |
| 600 | probe_only_fixedk_k2 | 0.000 | 0.027 | 1.000 |
| 600 | probe_only_fixedk_k4 | 0.000 | 0.027 | 1.000 |
| 600 | probe_only_fixedk_k8 | 0.000 | 0.027 | 1.000 |
| 600 | probe_adaptive_k_selected | 0.000 | 0.027 | 1.000 |
| 600 | budgeted_self_consistency | 0.000 | 0.027 | 1.000 |
| 600 | ours_controller_v3_nofallback | 0.000 | 0.878 | 1.000 |
| 900 | hard_cap | 0.000 | 0.014 | 1.000 |
| 900 | hard_cap_matched | 0.000 | 0.014 | 1.000 |
| 900 | probe_only_fixedk_k2 | 0.000 | 0.014 | 1.000 |
| 900 | probe_only_fixedk_k4 | 0.000 | 0.014 | 1.000 |
| 900 | probe_only_fixedk_k8 | 0.000 | 0.014 | 1.000 |
| 900 | probe_adaptive_k_selected | 0.000 | 0.014 | 1.000 |
| 900 | budgeted_self_consistency | 0.000 | 0.014 | 1.000 |
| 900 | ours_controller_v3_nofallback | 0.000 | 0.050 | 1.000 |
| 1500 | hard_cap | 0.000 | 0.007 | 1.000 |
| 1500 | hard_cap_matched | 0.000 | 0.007 | 1.000 |
| 1500 | probe_only_fixedk_k2 | 0.000 | 0.007 | 1.000 |
| 1500 | probe_only_fixedk_k4 | 0.000 | 0.007 | 1.000 |
| 1500 | probe_only_fixedk_k8 | 0.000 | 0.007 | 1.000 |
| 1500 | probe_adaptive_k_selected | 0.000 | 0.007 | 1.000 |
| 1500 | budgeted_self_consistency | 0.000 | 0.007 | 1.000 |
| 1500 | ours_controller_v3_nofallback | 0.000 | 0.026 | 1.000 |

## Method x Budget Parse-Fail Reasons
| Budget | Method | no_budget_for_repair | repair_called_but_failed | invalid_format_unresolved | multi_answer_unresolved | no_answer_token |
|---|---|---:|---:|---:|---:|---:|
| 300 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 300 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 300 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 300 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 300 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 350 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 350 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 350 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 350 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 350 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 350 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 350 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 350 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 400 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 400 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 400 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 400 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 450 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 450 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 450 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 450 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 450 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 450 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 450 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 450 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 500 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 500 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 500 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 600 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 600 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 600 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 600 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 900 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 900 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
| 900 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 900 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 1500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 1500 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k2 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k8 | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_adaptive_k_selected | 0 | 0 | 0 | 0 | 0 |
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
| 300 | budgeted_self_consistency | 140.1 | 0.3351 | 0.0559 | 0.0000 |
| 300 | hard_cap | 142.7 | 0.2797 | 0.0986 | 0.0000 |
| 300 | hard_cap_matched | 143.5 | 0.2838 | 0.1032 | 0.0000 |
| 300 | probe_adaptive_k_selected | 150.1 | 0.3297 | 0.0351 | 0.0000 |
| 300 | probe_only_fixedk_k2 | 150.1 | 0.3284 | 0.0370 | 0.0000 |
| 300 | probe_only_fixedk_k4 | 150.1 | 0.3284 | 0.0370 | 0.0000 |
| 300 | probe_only_fixedk_k8 | 150.1 | 0.3284 | 0.0370 | 0.0000 |
| 300 | ours_controller_v3_nofallback | 151.3 | 0.2568 | 0.0000 | 0.0000 |
| 350 | probe_only_fixedk_k2 | 203.7 | 0.3743 | 0.0600 | 0.0000 |
| 350 | probe_only_fixedk_k4 | 203.7 | 0.3743 | 0.0600 | 0.0000 |
| 350 | probe_only_fixedk_k8 | 203.7 | 0.3743 | 0.0600 | 0.0000 |
| 350 | probe_adaptive_k_selected | 203.7 | 0.3743 | 0.0619 | 0.0000 |
| 350 | budgeted_self_consistency | 204.1 | 0.3419 | 0.1028 | 0.0000 |
| 350 | hard_cap | 205.1 | 0.2824 | 0.1613 | 0.0000 |
| 350 | hard_cap_matched | 207.6 | 0.2865 | 0.1545 | 0.0000 |
| 350 | ours_controller_v3_nofallback | 225.4 | 0.2568 | 0.0000 | 0.0000 |
| 400 | probe_only_fixedk_k2 | 250.5 | 0.4027 | 0.0671 | 0.0000 |
| 400 | probe_adaptive_k_selected | 250.5 | 0.4027 | 0.0671 | 0.0000 |
| 400 | probe_only_fixedk_k4 | 251.2 | 0.4027 | 0.0671 | 0.0000 |
| 400 | probe_only_fixedk_k8 | 251.2 | 0.4027 | 0.0671 | 0.0000 |
| 400 | budgeted_self_consistency | 253.7 | 0.3500 | 0.1239 | 0.0000 |
| 400 | hard_cap | 254.6 | 0.2892 | 0.1783 | 0.0000 |
| 400 | hard_cap_matched | 261.7 | 0.2905 | 0.1848 | 0.0000 |
| 400 | ours_controller_v3_nofallback | 283.0 | 0.2568 | 0.0000 | 0.0000 |
| 450 | hard_cap | 281.0 | 0.3054 | 0.1862 | 0.0000 |
| 450 | probe_only_fixedk_k2 | 289.2 | 0.3959 | 0.0855 | 0.0000 |
| 450 | probe_adaptive_k_selected | 289.2 | 0.3959 | 0.0855 | 0.0000 |
| 450 | probe_only_fixedk_k4 | 290.6 | 0.3959 | 0.0855 | 0.0000 |
| 450 | probe_only_fixedk_k8 | 290.6 | 0.3959 | 0.0855 | 0.0000 |
| 450 | budgeted_self_consistency | 294.6 | 0.3432 | 0.1084 | 0.0000 |
| 450 | hard_cap_matched | 300.6 | 0.3054 | 0.2217 | 0.0000 |
| 450 | ours_controller_v3_nofallback | 324.8 | 0.2568 | 0.0000 | 0.0000 |
| 500 | hard_cap | 294.1 | 0.3203 | 0.2093 | 0.0000 |
| 500 | probe_only_fixedk_k2 | 326.4 | 0.4068 | 0.0705 | 0.0000 |
| 500 | hard_cap_matched | 326.6 | 0.3216 | 0.2344 | 0.0000 |
| 500 | probe_adaptive_k_selected | 326.8 | 0.4081 | 0.0685 | 0.0000 |
| 500 | budgeted_self_consistency | 327.2 | 0.3149 | 0.1166 | 0.0000 |
| 500 | probe_only_fixedk_k4 | 329.5 | 0.4068 | 0.0665 | 0.0000 |
| 500 | probe_only_fixedk_k8 | 329.5 | 0.4068 | 0.0665 | 0.0000 |
| 500 | ours_controller_v3_nofallback | 364.0 | 0.2595 | 0.0126 | 0.0000 |
| 600 | hard_cap | 305.0 | 0.2973 | 0.1864 | 0.0000 |
| 600 | hard_cap_matched | 351.0 | 0.3351 | 0.2217 | 0.0000 |
| 600 | probe_only_fixedk_k2 | 398.1 | 0.3986 | 0.0705 | 0.0000 |
| 600 | probe_adaptive_k_selected | 398.7 | 0.3986 | 0.0685 | 0.0000 |
| 600 | probe_only_fixedk_k4 | 413.8 | 0.3986 | 0.0685 | 0.0000 |
| 600 | probe_only_fixedk_k8 | 413.8 | 0.3986 | 0.0685 | 0.0000 |
| 600 | budgeted_self_consistency | 417.0 | 0.3338 | 0.1364 | 0.0000 |
| 600 | ours_controller_v3_nofallback | 461.5 | 0.2500 | 0.0175 | 0.0000 |
| 900 | hard_cap | 313.3 | 0.2905 | 0.1915 | 0.0000 |
| 900 | hard_cap_matched | 368.3 | 0.3189 | 0.2433 | 0.0000 |
| 900 | ours_controller_v3_nofallback | 527.8 | 0.3892 | 0.0506 | 0.0000 |
| 900 | probe_only_fixedk_k2 | 539.2 | 0.4108 | 0.0611 | 0.0000 |
| 900 | probe_adaptive_k_selected | 558.5 | 0.4014 | 0.0466 | 0.0000 |
| 900 | probe_only_fixedk_k4 | 707.0 | 0.4014 | 0.0466 | 0.0000 |
| 900 | budgeted_self_consistency | 714.3 | 0.3432 | 0.1176 | 0.0000 |
| 900 | probe_only_fixedk_k8 | 717.7 | 0.4014 | 0.0466 | 0.0000 |
| 1500 | hard_cap | 320.1 | 0.2946 | 0.1981 | 0.0000 |
| 1500 | hard_cap_matched | 374.4 | 0.3027 | 0.2464 | 0.0000 |
| 1500 | probe_only_fixedk_k2 | 576.7 | 0.4135 | 0.0678 | 0.0000 |
| 1500 | ours_controller_v3_nofallback | 588.2 | 0.4027 | 0.0430 | 0.0000 |
| 1500 | probe_adaptive_k_selected | 626.3 | 0.4054 | 0.0517 | 0.0000 |
| 1500 | probe_only_fixedk_k4 | 1072.1 | 0.4095 | 0.0558 | 0.0000 |
| 1500 | budgeted_self_consistency | 1140.7 | 0.3459 | 0.1223 | 0.0000 |
| 1500 | probe_only_fixedk_k8 | 1312.9 | 0.4081 | 0.0523 | 0.0000 |

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
- Summary: `/data2/chojm/incoh-pilot/runs/round9b_heldout_splitB9_r5_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round9b_heldout_splitB9_r5_v1/analysis_summary_round2.json`
