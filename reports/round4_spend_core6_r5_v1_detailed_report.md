# round4_spend_core6_r5_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round4_spend_core6_r5_v1`
- Dataset: `Wanfq/gpqa:400 sampled from run manifest`
- Methods: `['baseline_longcot', 'hard_cap', 'budgeted_self_consistency', 'ours_controller_v2', 'ours_controller_v2_nofallback', 'probe_only_fixedk']`
- Budgets: `[200, 300, 450, 600, 750, 900, 1200, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `96000` completed
- Hard fail: `0`
- Parse fail: `1091` (`1.1365%`)
- Repair success: `12953/13036` (`99.3633%`)
- Duration: `666.80` minutes

## Phase Threshold
- nofallback beats hard_cap on incoh with no acc loss first at: `450`
- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `450`
- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `450`

## nofallback Delta Table
| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |
|---|---:|---:|---:|---:|
| 200 | +0.0080 | -0.0170 | +0.0038 | -0.0180 |
| 300 | +0.0069 | -0.0275 | +0.0013 | -0.0370 |
| 450 | -0.0018 | +0.0070 | -0.0163 | -0.0050 |
| 600 | -0.0043 | +0.0135 | -0.0070 | -0.0080 |
| 750 | +0.0024 | +0.0125 | +0.0001 | -0.0035 |
| 900 | -0.0040 | +0.0110 | +0.0028 | -0.0110 |
| 1200 | -0.0168 | +0.0155 | -0.0098 | -0.0020 |
| 1500 | -0.0149 | +0.0145 | +0.0036 | -0.0030 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 200 | baseline_longcot | 0.013 | 0.760 | 1.000 |
| 200 | hard_cap | 0.018 | 0.713 | 1.000 |
| 200 | budgeted_self_consistency | 0.033 | 0.667 | 1.000 |
| 200 | ours_controller_v2 | 0.018 | 0.713 | 1.000 |
| 200 | ours_controller_v2_nofallback | 0.082 | 0.680 | 1.000 |
| 200 | probe_only_fixedk | 0.048 | 0.667 | 1.000 |
| 300 | baseline_longcot | 0.013 | 0.285 | 1.000 |
| 300 | hard_cap | 0.015 | 0.245 | 1.000 |
| 300 | budgeted_self_consistency | 0.027 | 0.235 | 1.000 |
| 300 | ours_controller_v2 | 0.015 | 0.245 | 1.000 |
| 300 | ours_controller_v2_nofallback | 0.133 | 0.237 | 1.000 |
| 300 | probe_only_fixedk | 0.030 | 0.235 | 1.000 |
| 450 | baseline_longcot | 0.003 | 0.068 | 1.000 |
| 450 | hard_cap | 0.005 | 0.060 | 1.000 |
| 450 | budgeted_self_consistency | 0.006 | 0.059 | 0.975 |
| 450 | ours_controller_v2 | 0.005 | 0.060 | 1.000 |
| 450 | ours_controller_v2_nofallback | 0.008 | 0.081 | 0.950 |
| 450 | probe_only_fixedk | 0.010 | 0.058 | 1.000 |
| 600 | baseline_longcot | 0.003 | 0.018 | 1.000 |
| 600 | hard_cap | 0.000 | 0.018 | 1.000 |
| 600 | budgeted_self_consistency | 0.001 | 0.018 | 1.000 |
| 600 | ours_controller_v2 | 0.000 | 0.018 | 1.000 |
| 600 | ours_controller_v2_nofallback | 0.022 | 0.059 | 0.718 |
| 600 | probe_only_fixedk | 0.000 | 0.018 | 1.000 |
| 750 | baseline_longcot | 0.000 | 0.013 | 1.000 |
| 750 | hard_cap | 0.000 | 0.013 | 1.000 |
| 750 | budgeted_self_consistency | 0.002 | 0.014 | 0.893 |
| 750 | ours_controller_v2 | 0.000 | 0.013 | 1.000 |
| 750 | ours_controller_v2_nofallback | 0.007 | 0.054 | 0.898 |
| 750 | probe_only_fixedk | 0.000 | 0.013 | 1.000 |
| 900 | baseline_longcot | 0.000 | 0.010 | 1.000 |
| 900 | hard_cap | 0.000 | 0.010 | 1.000 |
| 900 | budgeted_self_consistency | 0.001 | 0.010 | 1.000 |
| 900 | ours_controller_v2 | 0.000 | 0.010 | 1.000 |
| 900 | ours_controller_v2_nofallback | 0.015 | 0.058 | 0.871 |
| 900 | probe_only_fixedk | 0.000 | 0.010 | 1.000 |
| 1200 | baseline_longcot | 0.000 | 0.003 | 1.000 |
| 1200 | hard_cap | 0.000 | 0.003 | 1.000 |
| 1200 | budgeted_self_consistency | 0.001 | 0.003 | 1.000 |
| 1200 | ours_controller_v2 | 0.004 | 0.020 | 0.875 |
| 1200 | ours_controller_v2_nofallback | 0.004 | 0.020 | 0.875 |
| 1200 | probe_only_fixedk | 0.000 | 0.003 | 1.000 |
| 1500 | baseline_longcot | 0.000 | 0.003 | 1.000 |
| 1500 | hard_cap | 0.000 | 0.003 | 1.000 |
| 1500 | budgeted_self_consistency | 0.001 | 0.003 | 1.000 |
| 1500 | ours_controller_v2 | 0.004 | 0.009 | 1.000 |
| 1500 | ours_controller_v2_nofallback | 0.004 | 0.009 | 1.000 |
| 1500 | probe_only_fixedk | 0.000 | 0.003 | 1.000 |

## Probe Predictive Signal (nofallback)
| Budget | n trial-pairs | AUC(probe_disagree -> baseline_error) | n docs | AUC(probe_disagree -> baseline_disagreement>0) |
|---|---:|---:|---:|---:|
| 200 | 2000 | 0.500 | 400 | 0.500 |
| 300 | 2000 | 0.500 | 400 | 0.500 |
| 450 | 2000 | 0.520 | 400 | 0.593 |
| 600 | 2000 | 0.516 | 400 | 0.660 |
| 750 | 2000 | 0.518 | 400 | 0.686 |
| 900 | 2000 | 0.517 | 400 | 0.675 |
| 1200 | 2000 | 0.509 | 400 | 0.706 |
| 1500 | 2000 | 0.513 | 400 | 0.696 |

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round4_spend_core6_r5_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round4_spend_core6_r5_v1/analysis_summary_round2.json`
