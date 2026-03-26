# round5a_tuning_splitA_r5_v2 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round5a_tuning_splitA_r5_v2`
- Dataset: `Wanfq/gpqa:200 sampled from run manifest`
- Methods: `['hard_cap', 'probe_only_fixedk', 'ours_controller_v2_nofallback', 'ours_controller_v2_nofallback_forcecontinue', 'ours_controller_v2_nofallback_stopcap']`
- Budgets: `[300, 450, 600, 900, 1200]`
- Parse policy: `P1R`

## Reliability
- Records: `25000` completed
- Hard fail: `0`
- Parse fail: `720` (`2.8800%`)
- Repair success: `2639/3359` (`78.5650%`)
- Duration: `106.42` minutes

## Phase Threshold
- nofallback beats hard_cap on incoh with no acc loss first at: `450`
- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `None`
- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `None`

## nofallback Delta Table
| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |
|---|---:|---:|---:|---:|
| 300 | +0.0033 | -0.0460 | +nan | +nan |
| 450 | -0.0103 | +0.0020 | +nan | +nan |
| 600 | +0.0028 | +0.0070 | +nan | +nan |
| 900 | +0.0064 | -0.0040 | +nan | +nan |
| 1200 | -0.0278 | +0.0100 | +nan | +nan |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 300 | hard_cap | 0.005 | 0.280 | 0.982 |
| 300 | probe_only_fixedk | 0.015 | 0.265 | 0.943 |
| 300 | ours_controller_v2_nofallback | 0.136 | 0.391 | 0.652 |
| 300 | ours_controller_v2_nofallback_forcecontinue | 0.136 | 0.391 | 0.652 |
| 300 | ours_controller_v2_nofallback_stopcap | 0.136 | 0.391 | 0.652 |
| 450 | hard_cap | 0.000 | 0.080 | 1.000 |
| 450 | probe_only_fixedk | 0.005 | 0.080 | 0.938 |
| 450 | ours_controller_v2_nofallback | 0.009 | 0.106 | 0.915 |
| 450 | ours_controller_v2_nofallback_forcecontinue | 0.009 | 0.106 | 0.915 |
| 450 | ours_controller_v2_nofallback_stopcap | 0.061 | 0.286 | 0.787 |
| 600 | hard_cap | 0.000 | 0.025 | 1.000 |
| 600 | probe_only_fixedk | 0.005 | 0.025 | 0.800 |
| 600 | ours_controller_v2_nofallback | 0.024 | 0.081 | 0.704 |
| 600 | ours_controller_v2_nofallback_forcecontinue | 0.024 | 0.081 | 0.704 |
| 600 | ours_controller_v2_nofallback_stopcap | 0.050 | 0.222 | 0.775 |
| 900 | hard_cap | 0.000 | 0.010 | 1.000 |
| 900 | probe_only_fixedk | 0.000 | 0.010 | 1.000 |
| 900 | ours_controller_v2_nofallback | 0.016 | 0.091 | 0.824 |
| 900 | ours_controller_v2_nofallback_forcecontinue | 0.018 | 0.100 | 0.820 |
| 900 | ours_controller_v2_nofallback_stopcap | 0.032 | 0.166 | 0.807 |
| 1200 | hard_cap | 0.000 | 0.000 | 0.000 |
| 1200 | probe_only_fixedk | 0.000 | 0.000 | 0.000 |
| 1200 | ours_controller_v2_nofallback | 0.006 | 0.029 | 0.793 |
| 1200 | ours_controller_v2_nofallback_forcecontinue | 0.010 | 0.052 | 0.808 |
| 1200 | ours_controller_v2_nofallback_stopcap | 0.023 | 0.091 | 0.747 |

## Probe Predictive Signal (nofallback)
| Budget | n trial-pairs | AUC(probe_disagree -> baseline_error) | n docs | AUC(probe_disagree -> baseline_disagreement>0) |
|---|---:|---:|---:|---:|

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round5a_tuning_splitA_r5_v2/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round5a_tuning_splitA_r5_v2/analysis_summary_round2.json`
