# round5b_heldout_splitB_r5_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round5b_heldout_splitB_r5_v1`
- Dataset: `Wanfq/gpqa:200 sampled from run manifest`
- Methods: `['hard_cap', 'budgeted_self_consistency', 'probe_only_fixedk', 'ours_controller_v2_nofallback', 'ours_controller_v2_nofallback_forcecontinue']`
- Budgets: `[200, 300, 450, 600, 900, 1200, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `35000` completed
- Hard fail: `0`
- Parse fail: `607` (`1.7343%`)
- Repair success: `6293/6900` (`91.2029%`)
- Duration: `196.33` minutes

## Phase Threshold
- nofallback beats hard_cap on incoh with no acc loss first at: `600`
- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `None`
- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `450`

## nofallback Delta Table
| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |
|---|---:|---:|---:|---:|
| 200 | +0.0003 | -0.0060 | +0.0000 | -0.0240 |
| 300 | +0.0073 | -0.0120 | -0.0014 | -0.0560 |
| 450 | +0.0049 | +0.0130 | -0.0104 | -0.0180 |
| 600 | -0.0080 | +0.0230 | -0.0198 | -0.0200 |
| 900 | -0.0163 | +0.0260 | -0.0148 | -0.0170 |
| 1200 | -0.0069 | +0.0210 | -0.0054 | -0.0160 |
| 1500 | -0.0188 | +0.0250 | -0.0039 | -0.0160 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 200 | hard_cap | 0.015 | 0.830 | 0.982 |
| 200 | budgeted_self_consistency | 0.020 | 0.805 | 0.975 |
| 200 | probe_only_fixedk | 0.040 | 0.825 | 0.952 |
| 200 | ours_controller_v2_nofallback | 0.052 | 0.842 | 0.938 |
| 200 | ours_controller_v2_nofallback_forcecontinue | 0.052 | 0.842 | 0.938 |
| 300 | hard_cap | 0.015 | 0.375 | 0.960 |
| 300 | budgeted_self_consistency | 0.030 | 0.350 | 0.914 |
| 300 | probe_only_fixedk | 0.030 | 0.350 | 0.914 |
| 300 | ours_controller_v2_nofallback | 0.129 | 0.464 | 0.722 |
| 300 | ours_controller_v2_nofallback_forcecontinue | 0.129 | 0.464 | 0.722 |
| 450 | hard_cap | 0.000 | 0.060 | 1.000 |
| 450 | budgeted_self_consistency | 0.000 | 0.063 | 1.000 |
| 450 | probe_only_fixedk | 0.000 | 0.060 | 1.000 |
| 450 | ours_controller_v2_nofallback | 0.004 | 0.085 | 0.953 |
| 450 | ours_controller_v2_nofallback_forcecontinue | 0.004 | 0.085 | 0.953 |
| 600 | hard_cap | 0.000 | 0.015 | 1.000 |
| 600 | budgeted_self_consistency | 0.002 | 0.017 | 0.882 |
| 600 | probe_only_fixedk | 0.000 | 0.015 | 1.000 |
| 600 | ours_controller_v2_nofallback | 0.017 | 0.052 | 0.673 |
| 600 | ours_controller_v2_nofallback_forcecontinue | 0.017 | 0.052 | 0.673 |
| 900 | hard_cap | 0.000 | 0.010 | 1.000 |
| 900 | budgeted_self_consistency | 0.003 | 0.013 | 0.769 |
| 900 | probe_only_fixedk | 0.000 | 0.010 | 1.000 |
| 900 | ours_controller_v2_nofallback | 0.013 | 0.039 | 0.667 |
| 900 | ours_controller_v2_nofallback_forcecontinue | 0.016 | 0.049 | 0.673 |
| 1200 | hard_cap | 0.000 | 0.005 | 1.000 |
| 1200 | budgeted_self_consistency | 0.002 | 0.007 | 0.714 |
| 1200 | probe_only_fixedk | 0.000 | 0.005 | 1.000 |
| 1200 | ours_controller_v2_nofallback | 0.005 | 0.020 | 0.750 |
| 1200 | ours_controller_v2_nofallback_forcecontinue | 0.005 | 0.031 | 0.839 |
| 1500 | hard_cap | 0.000 | 0.005 | 1.000 |
| 1500 | budgeted_self_consistency | 0.002 | 0.007 | 0.714 |
| 1500 | probe_only_fixedk | 0.000 | 0.005 | 1.000 |
| 1500 | ours_controller_v2_nofallback | 0.002 | 0.017 | 0.882 |
| 1500 | ours_controller_v2_nofallback_forcecontinue | 0.003 | 0.026 | 0.885 |

## Probe Predictive Signal (nofallback)
| Budget | n trial-pairs | AUC(probe_disagree -> baseline_error) | n docs | AUC(probe_disagree -> baseline_disagreement>0) |
|---|---:|---:|---:|---:|

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round5b_heldout_splitB_r5_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round5b_heldout_splitB_r5_v1/analysis_summary_round2.json`
