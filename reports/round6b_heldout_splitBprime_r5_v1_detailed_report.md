# round6b_heldout_splitBprime_r5_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round6b_heldout_splitBprime_r5_v1`
- Dataset: `Wanfq/gpqa:200 sampled from run manifest`
- Methods: `['hard_cap', 'probe_only_fixedk', 'probe_adaptive_k_selected', 'ours_controller_v2_nofallback']`
- Budgets: `[200, 300, 400, 500, 600, 750, 900, 1200, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `36000` completed
- Hard fail: `0`
- Parse fail: `423` (`1.1750%`)
- Repair success: `5964/6387` (`93.3772%`)
- Duration: `152.87` minutes

## Phase Threshold
- nofallback beats hard_cap on incoh with no acc loss first at: `400`
- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `None`
- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `None`
- Threshold bootstrap (hard_cap vs nofallback): finite_rate=`1.000`, median=`400.0`, 95% CI=`[200.0, 900.0]`

## nofallback Delta Table
| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |
|---|---:|---:|---:|---:|
| 200 | +0.0038 | +0.0010 | +nan | +nan |
| 300 | +0.0207 | -0.0940 | +nan | +nan |
| 400 | -0.0459 | +0.0040 | +nan | +nan |
| 500 | -0.0258 | +0.0030 | +nan | +nan |
| 600 | -0.0224 | -0.0020 | +nan | +nan |
| 750 | -0.0143 | +0.0150 | +nan | +nan |
| 900 | -0.0385 | +0.0220 | +nan | +nan |
| 1200 | -0.0303 | +0.0290 | +nan | +nan |
| 1500 | -0.0442 | +0.0270 | +nan | +nan |

## Parse-Fail Sensitivity (Included vs Excluded)
| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |
|---|---|---:|---:|---:|---:|---:|
| 200 | hard_cap | 0.2320 | 0.2332 | 0.0077 | 0.0078 | 199 |
| 200 | probe_only_fixedk | 0.2330 | 0.2365 | 0.0102 | 0.0104 | 197 |
| 200 | probe_adaptive_k_selected | 0.2280 | 0.2315 | 0.0115 | 0.0117 | 197 |
| 200 | ours_controller_v2_nofallback | 0.2330 | 0.2390 | 0.0116 | 0.0119 | 195 |
| 300 | hard_cap | 0.3270 | 0.3320 | 0.0556 | 0.0567 | 197 |
| 300 | probe_only_fixedk | 0.3510 | 0.3619 | 0.0433 | 0.0454 | 194 |
| 300 | probe_adaptive_k_selected | 0.3590 | 0.3755 | 0.0354 | 0.0392 | 192 |
| 300 | ours_controller_v2_nofallback | 0.2330 | 0.2637 | 0.0763 | 0.0872 | 182 |
| 400 | hard_cap | 0.3570 | 0.3588 | 0.0980 | 0.0987 | 199 |
| 400 | probe_only_fixedk | 0.3600 | 0.3673 | 0.0487 | 0.0502 | 196 |
| 400 | probe_adaptive_k_selected | 0.3630 | 0.3685 | 0.0585 | 0.0594 | 197 |
| 400 | ours_controller_v2_nofallback | 0.3610 | 0.3689 | 0.0521 | 0.0526 | 198 |
| 500 | hard_cap | 0.3760 | 0.3760 | 0.0863 | 0.0863 | 200 |
| 500 | probe_only_fixedk | 0.4090 | 0.4090 | 0.0752 | 0.0752 | 200 |
| 500 | probe_adaptive_k_selected | 0.3950 | 0.3970 | 0.0691 | 0.0673 | 199 |
| 500 | ours_controller_v2_nofallback | 0.3790 | 0.3812 | 0.0605 | 0.0538 | 199 |
| 600 | hard_cap | 0.3790 | 0.3790 | 0.0869 | 0.0869 | 200 |
| 600 | probe_only_fixedk | 0.3880 | 0.3880 | 0.0524 | 0.0524 | 200 |
| 600 | probe_adaptive_k_selected | 0.3940 | 0.3990 | 0.0580 | 0.0551 | 200 |
| 600 | ours_controller_v2_nofallback | 0.3770 | 0.3793 | 0.0645 | 0.0556 | 200 |
| 750 | hard_cap | 0.3700 | 0.3700 | 0.0929 | 0.0929 | 200 |
| 750 | probe_only_fixedk | 0.4070 | 0.4070 | 0.0630 | 0.0630 | 200 |
| 750 | probe_adaptive_k_selected | 0.3990 | 0.3990 | 0.0566 | 0.0566 | 200 |
| 750 | ours_controller_v2_nofallback | 0.3850 | 0.3862 | 0.0785 | 0.0761 | 200 |
| 900 | hard_cap | 0.3720 | 0.3720 | 0.1026 | 0.1026 | 200 |
| 900 | probe_only_fixedk | 0.4040 | 0.4040 | 0.0521 | 0.0521 | 200 |
| 900 | probe_adaptive_k_selected | 0.3940 | 0.3950 | 0.0573 | 0.0562 | 200 |
| 900 | ours_controller_v2_nofallback | 0.3940 | 0.3963 | 0.0641 | 0.0640 | 200 |
| 1200 | hard_cap | 0.3710 | 0.3710 | 0.0973 | 0.0973 | 200 |
| 1200 | probe_only_fixedk | 0.4100 | 0.4100 | 0.0650 | 0.0650 | 200 |
| 1200 | probe_adaptive_k_selected | 0.3960 | 0.3960 | 0.0472 | 0.0472 | 200 |
| 1200 | ours_controller_v2_nofallback | 0.4000 | 0.4015 | 0.0670 | 0.0700 | 200 |
| 1500 | hard_cap | 0.3740 | 0.3740 | 0.0876 | 0.0876 | 200 |
| 1500 | probe_only_fixedk | 0.4030 | 0.4030 | 0.0419 | 0.0419 | 200 |
| 1500 | probe_adaptive_k_selected | 0.4020 | 0.4020 | 0.0391 | 0.0391 | 200 |
| 1500 | ours_controller_v2_nofallback | 0.4010 | 0.4010 | 0.0434 | 0.0388 | 200 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 200 | hard_cap | 0.005 | 0.870 | 0.994 |
| 200 | probe_only_fixedk | 0.015 | 0.865 | 0.983 |
| 200 | probe_adaptive_k_selected | 0.015 | 0.865 | 0.983 |
| 200 | ours_controller_v2_nofallback | 0.025 | 0.880 | 0.972 |
| 300 | hard_cap | 0.015 | 0.430 | 0.965 |
| 300 | probe_only_fixedk | 0.030 | 0.410 | 0.927 |
| 300 | probe_adaptive_k_selected | 0.045 | 0.431 | 0.896 |
| 300 | ours_controller_v2_nofallback | 0.130 | 0.510 | 0.745 |
| 400 | hard_cap | 0.005 | 0.125 | 0.960 |
| 400 | probe_only_fixedk | 0.020 | 0.125 | 0.840 |
| 400 | probe_adaptive_k_selected | 0.016 | 0.137 | 0.883 |
| 400 | ours_controller_v2_nofallback | 0.019 | 0.141 | 0.865 |
| 500 | hard_cap | 0.000 | 0.030 | 1.000 |
| 500 | probe_only_fixedk | 0.000 | 0.025 | 1.000 |
| 500 | probe_adaptive_k_selected | 0.008 | 0.047 | 0.830 |
| 500 | ours_controller_v2_nofallback | 0.019 | 0.070 | 0.729 |
| 600 | hard_cap | 0.000 | 0.015 | 1.000 |
| 600 | probe_only_fixedk | 0.000 | 0.015 | 1.000 |
| 600 | probe_adaptive_k_selected | 0.006 | 0.034 | 0.824 |
| 600 | ours_controller_v2_nofallback | 0.013 | 0.057 | 0.772 |
| 750 | hard_cap | 0.000 | 0.010 | 1.000 |
| 750 | probe_only_fixedk | 0.000 | 0.010 | 1.000 |
| 750 | probe_adaptive_k_selected | 0.000 | 0.022 | 1.000 |
| 750 | ours_controller_v2_nofallback | 0.009 | 0.066 | 0.864 |
| 900 | hard_cap | 0.000 | 0.010 | 1.000 |
| 900 | probe_only_fixedk | 0.000 | 0.010 | 1.000 |
| 900 | probe_adaptive_k_selected | 0.001 | 0.016 | 0.938 |
| 900 | ours_controller_v2_nofallback | 0.009 | 0.061 | 0.852 |
| 1200 | hard_cap | 0.000 | 0.005 | 1.000 |
| 1200 | probe_only_fixedk | 0.000 | 0.005 | 1.000 |
| 1200 | probe_adaptive_k_selected | 0.000 | 0.008 | 1.000 |
| 1200 | ours_controller_v2_nofallback | 0.010 | 0.039 | 0.744 |
| 1500 | hard_cap | 0.000 | 0.005 | 1.000 |
| 1500 | probe_only_fixedk | 0.000 | 0.005 | 1.000 |
| 1500 | probe_adaptive_k_selected | 0.000 | 0.008 | 1.000 |
| 1500 | ours_controller_v2_nofallback | 0.008 | 0.025 | 0.680 |

## Probe Predictive Signal (nofallback)
| Budget | n trial-pairs | AUC(probe_disagree -> baseline_error) | n docs | AUC(probe_disagree -> baseline_disagreement>0) |
|---|---:|---:|---:|---:|

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round6b_heldout_splitBprime_r5_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round6b_heldout_splitBprime_r5_v1/analysis_summary_round2.json`
