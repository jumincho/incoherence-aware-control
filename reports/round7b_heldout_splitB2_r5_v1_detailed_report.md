# round7b_heldout_splitB2_r5_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round7b_heldout_splitB2_r5_v1`
- Dataset: `Wanfq/gpqa:200 sampled from run manifest`
- Methods: `['hard_cap', 'ours_controller_v2_nofallback', 'probe_only_fixedk_k4', 'probe_only_fixedk_k8', 'probe_adaptive_k_selected']`
- Budgets: `[300, 400, 500, 600, 750, 900, 1200, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `40000` completed
- Hard fail: `0`
- Parse fail: `208` (`0.5200%`)
- Repair success: `2213/2213` (`100.0000%`)
- Duration: `259.83` minutes

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
| 300 | +0.0051 | -0.0010 | +nan | +nan |
| 400 | -0.0822 | +0.0510 | +nan | +nan |
| 500 | -0.1070 | +0.0150 | +nan | +nan |
| 600 | -0.1188 | +0.0500 | +nan | +nan |
| 750 | -0.1417 | +0.0370 | +nan | +nan |
| 900 | -0.1186 | +0.0620 | +nan | +nan |
| 1200 | -0.1356 | +0.0590 | +nan | +nan |
| 1500 | -0.1286 | +0.0560 | +nan | +nan |

## Adaptive Probe vs Probe-Only
| Budget | Adaptive | Probe | Δacc(adapt-probe) | Δincoh(adapt-probe) | Adapt Tok | Probe Tok |
|---|---|---|---:|---:|---:|---:|
| 300 | probe_adaptive_k_selected | probe_only_fixedk_k4 | -0.0020 | -0.0007 | 207.1 | 207.1 |
| 400 | probe_adaptive_k_selected | probe_only_fixedk_k4 | +0.0000 | +0.0000 | 289.2 | 290.4 |
| 500 | probe_adaptive_k_selected | probe_only_fixedk_k4 | +0.0000 | +0.0000 | 372.4 | 382.0 |
| 600 | probe_adaptive_k_selected | probe_only_fixedk_k4 | +0.0000 | +0.0000 | 443.8 | 473.1 |
| 750 | probe_adaptive_k_selected | probe_only_fixedk_k4 | +0.0000 | +0.0000 | 523.9 | 617.4 |
| 900 | probe_adaptive_k_selected | probe_only_fixedk_k4 | +0.0000 | -0.0013 | 575.2 | 748.0 |
| 1200 | probe_adaptive_k_selected | probe_only_fixedk_k4 | -0.0020 | +0.0014 | 626.1 | 964.2 |
| 1500 | probe_adaptive_k_selected | probe_only_fixedk_k4 | -0.0020 | +0.0105 | 650.0 | 1072.8 |

## Parse-Fail Sensitivity (Included vs Excluded)
| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |
|---|---|---:|---:|---:|---:|---:|
| 300 | hard_cap | 0.3270 | 0.3303 | 0.1584 | 0.1604 | 198 |
| 300 | ours_controller_v2_nofallback | 0.3260 | 0.3276 | 0.1635 | 0.1645 | 199 |
| 300 | probe_only_fixedk_k4 | 0.3470 | 0.3541 | 0.0679 | 0.0699 | 196 |
| 300 | probe_only_fixedk_k8 | 0.3470 | 0.3541 | 0.0679 | 0.0699 | 196 |
| 300 | probe_adaptive_k_selected | 0.3450 | 0.3520 | 0.0672 | 0.0672 | 196 |
| 400 | hard_cap | 0.2910 | 0.2925 | 0.1647 | 0.1657 | 199 |
| 400 | ours_controller_v2_nofallback | 0.3420 | 0.3480 | 0.0825 | 0.0817 | 197 |
| 400 | probe_only_fixedk_k4 | 0.3330 | 0.3364 | 0.0759 | 0.0769 | 198 |
| 400 | probe_only_fixedk_k8 | 0.3330 | 0.3364 | 0.0759 | 0.0769 | 198 |
| 400 | probe_adaptive_k_selected | 0.3330 | 0.3364 | 0.0759 | 0.0769 | 198 |
| 500 | hard_cap | 0.3220 | 0.3236 | 0.1897 | 0.1908 | 199 |
| 500 | ours_controller_v2_nofallback | 0.3370 | 0.3402 | 0.0826 | 0.0787 | 199 |
| 500 | probe_only_fixedk_k4 | 0.3470 | 0.3470 | 0.0661 | 0.0661 | 200 |
| 500 | probe_only_fixedk_k8 | 0.3470 | 0.3470 | 0.0661 | 0.0661 | 200 |
| 500 | probe_adaptive_k_selected | 0.3470 | 0.3470 | 0.0661 | 0.0661 | 200 |
| 600 | hard_cap | 0.3030 | 0.3030 | 0.1921 | 0.1921 | 200 |
| 600 | ours_controller_v2_nofallback | 0.3530 | 0.3555 | 0.0733 | 0.0713 | 200 |
| 600 | probe_only_fixedk_k4 | 0.3450 | 0.3450 | 0.0688 | 0.0688 | 200 |
| 600 | probe_only_fixedk_k8 | 0.3450 | 0.3450 | 0.0688 | 0.0688 | 200 |
| 600 | probe_adaptive_k_selected | 0.3450 | 0.3450 | 0.0688 | 0.0688 | 200 |
| 750 | hard_cap | 0.3150 | 0.3150 | 0.2099 | 0.2099 | 200 |
| 750 | ours_controller_v2_nofallback | 0.3520 | 0.3560 | 0.0683 | 0.0680 | 200 |
| 750 | probe_only_fixedk_k4 | 0.3600 | 0.3600 | 0.0689 | 0.0689 | 200 |
| 750 | probe_only_fixedk_k8 | 0.3600 | 0.3600 | 0.0689 | 0.0689 | 200 |
| 750 | probe_adaptive_k_selected | 0.3600 | 0.3600 | 0.0689 | 0.0689 | 200 |
| 900 | hard_cap | 0.3060 | 0.3060 | 0.1960 | 0.1960 | 200 |
| 900 | ours_controller_v2_nofallback | 0.3680 | 0.3680 | 0.0774 | 0.0732 | 200 |
| 900 | probe_only_fixedk_k4 | 0.3520 | 0.3520 | 0.0706 | 0.0706 | 200 |
| 900 | probe_only_fixedk_k8 | 0.3520 | 0.3520 | 0.0693 | 0.0693 | 200 |
| 900 | probe_adaptive_k_selected | 0.3520 | 0.3520 | 0.0693 | 0.0693 | 200 |
| 1200 | hard_cap | 0.3030 | 0.3030 | 0.2027 | 0.2027 | 200 |
| 1200 | ours_controller_v2_nofallback | 0.3620 | 0.3620 | 0.0671 | 0.0704 | 200 |
| 1200 | probe_only_fixedk_k4 | 0.3560 | 0.3560 | 0.0625 | 0.0625 | 200 |
| 1200 | probe_only_fixedk_k8 | 0.3570 | 0.3570 | 0.0570 | 0.0570 | 200 |
| 1200 | probe_adaptive_k_selected | 0.3540 | 0.3540 | 0.0639 | 0.0639 | 200 |
| 1500 | hard_cap | 0.3000 | 0.3000 | 0.1932 | 0.1932 | 200 |
| 1500 | ours_controller_v2_nofallback | 0.3560 | 0.3560 | 0.0645 | 0.0625 | 200 |
| 1500 | probe_only_fixedk_k4 | 0.3620 | 0.3620 | 0.0556 | 0.0556 | 200 |
| 1500 | probe_only_fixedk_k8 | 0.3650 | 0.3650 | 0.0643 | 0.0643 | 200 |
| 1500 | probe_adaptive_k_selected | 0.3600 | 0.3600 | 0.0661 | 0.0661 | 200 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 300 | hard_cap | 0.010 | 0.250 | 1.000 |
| 300 | ours_controller_v2_nofallback | 0.005 | 0.225 | 1.000 |
| 300 | probe_only_fixedk_k4 | 0.020 | 0.245 | 1.000 |
| 300 | probe_only_fixedk_k8 | 0.020 | 0.245 | 1.000 |
| 300 | probe_adaptive_k_selected | 0.022 | 0.245 | 1.000 |
| 400 | hard_cap | 0.005 | 0.075 | 1.000 |
| 400 | ours_controller_v2_nofallback | 0.018 | 0.084 | 1.000 |
| 400 | probe_only_fixedk_k4 | 0.010 | 0.070 | 1.000 |
| 400 | probe_only_fixedk_k8 | 0.010 | 0.070 | 1.000 |
| 400 | probe_adaptive_k_selected | 0.010 | 0.070 | 1.000 |
| 500 | hard_cap | 0.005 | 0.035 | 1.000 |
| 500 | ours_controller_v2_nofallback | 0.023 | 0.048 | 1.000 |
| 500 | probe_only_fixedk_k4 | 0.000 | 0.025 | 1.000 |
| 500 | probe_only_fixedk_k8 | 0.000 | 0.025 | 1.000 |
| 500 | probe_adaptive_k_selected | 0.000 | 0.025 | 1.000 |
| 600 | hard_cap | 0.000 | 0.015 | 1.000 |
| 600 | ours_controller_v2_nofallback | 0.013 | 0.092 | 1.000 |
| 600 | probe_only_fixedk_k4 | 0.000 | 0.020 | 1.000 |
| 600 | probe_only_fixedk_k8 | 0.000 | 0.020 | 1.000 |
| 600 | probe_adaptive_k_selected | 0.000 | 0.020 | 1.000 |
| 750 | hard_cap | 0.000 | 0.010 | 1.000 |
| 750 | ours_controller_v2_nofallback | 0.020 | 0.061 | 1.000 |
| 750 | probe_only_fixedk_k4 | 0.000 | 0.010 | 1.000 |
| 750 | probe_only_fixedk_k8 | 0.000 | 0.010 | 1.000 |
| 750 | probe_adaptive_k_selected | 0.000 | 0.010 | 1.000 |
| 900 | hard_cap | 0.000 | 0.010 | 1.000 |
| 900 | ours_controller_v2_nofallback | 0.008 | 0.071 | 1.000 |
| 900 | probe_only_fixedk_k4 | 0.000 | 0.010 | 1.000 |
| 900 | probe_only_fixedk_k8 | 0.000 | 0.010 | 1.000 |
| 900 | probe_adaptive_k_selected | 0.000 | 0.010 | 1.000 |
| 1200 | hard_cap | 0.000 | 0.005 | 1.000 |
| 1200 | ours_controller_v2_nofallback | 0.003 | 0.046 | 1.000 |
| 1200 | probe_only_fixedk_k4 | 0.000 | 0.005 | 1.000 |
| 1200 | probe_only_fixedk_k8 | 0.000 | 0.005 | 1.000 |
| 1200 | probe_adaptive_k_selected | 0.000 | 0.005 | 1.000 |
| 1500 | hard_cap | 0.000 | 0.005 | 1.000 |
| 1500 | ours_controller_v2_nofallback | 0.006 | 0.011 | 1.000 |
| 1500 | probe_only_fixedk_k4 | 0.000 | 0.005 | 1.000 |
| 1500 | probe_only_fixedk_k8 | 0.000 | 0.005 | 1.000 |
| 1500 | probe_adaptive_k_selected | 0.000 | 0.005 | 1.000 |

## Parse-Fail Gating Check
| Budget | Max ParseFail | Min ParseFail | Spread | Gate(max<=1%) | Gate(spread<=1%p) |
|---|---:|---:|---:|---:|---:|
| 300 | 0.022 | 0.005 | 0.017 | 0 | 0 |
| 400 | 0.018 | 0.005 | 0.013 | 0 | 0 |
| 500 | 0.023 | 0.000 | 0.023 | 0 | 0 |
| 600 | 0.013 | 0.000 | 0.013 | 0 | 0 |
| 750 | 0.020 | 0.000 | 0.020 | 0 | 0 |
| 900 | 0.008 | 0.000 | 0.008 | 1 | 1 |
| 1200 | 0.003 | 0.000 | 0.003 | 1 | 1 |
| 1500 | 0.006 | 0.000 | 0.006 | 1 | 1 |

## Cost Reality (Actual Total Tokens)
| Budget | Method | AvgTotalTok | Accuracy | Incoherence | ParseFail |
|---|---|---:|---:|---:|---:|
| 300 | hard_cap | 203.0 | 0.3270 | 0.1584 | 0.0100 |
| 300 | probe_only_fixedk_k4 | 207.1 | 0.3470 | 0.0679 | 0.0200 |
| 300 | probe_only_fixedk_k8 | 207.1 | 0.3470 | 0.0679 | 0.0200 |
| 300 | probe_adaptive_k_selected | 207.1 | 0.3450 | 0.0672 | 0.0220 |
| 300 | ours_controller_v2_nofallback | 209.5 | 0.3260 | 0.1635 | 0.0050 |
| 400 | hard_cap | 282.8 | 0.2910 | 0.1647 | 0.0050 |
| 400 | ours_controller_v2_nofallback | 283.9 | 0.3420 | 0.0825 | 0.0180 |
| 400 | probe_adaptive_k_selected | 289.2 | 0.3330 | 0.0759 | 0.0100 |
| 400 | probe_only_fixedk_k4 | 290.4 | 0.3330 | 0.0759 | 0.0100 |
| 400 | probe_only_fixedk_k8 | 290.4 | 0.3330 | 0.0759 | 0.0100 |
| 500 | hard_cap | 311.0 | 0.3220 | 0.1897 | 0.0050 |
| 500 | ours_controller_v2_nofallback | 364.0 | 0.3370 | 0.0826 | 0.0230 |
| 500 | probe_adaptive_k_selected | 372.4 | 0.3470 | 0.0661 | 0.0000 |
| 500 | probe_only_fixedk_k4 | 382.0 | 0.3470 | 0.0661 | 0.0000 |
| 500 | probe_only_fixedk_k8 | 382.0 | 0.3470 | 0.0661 | 0.0000 |
| 600 | hard_cap | 317.5 | 0.3030 | 0.1921 | 0.0000 |
| 600 | ours_controller_v2_nofallback | 438.6 | 0.3530 | 0.0733 | 0.0130 |
| 600 | probe_adaptive_k_selected | 443.8 | 0.3450 | 0.0688 | 0.0000 |
| 600 | probe_only_fixedk_k4 | 473.1 | 0.3450 | 0.0688 | 0.0000 |
| 600 | probe_only_fixedk_k8 | 473.5 | 0.3450 | 0.0688 | 0.0000 |
| 750 | hard_cap | 321.6 | 0.3150 | 0.2099 | 0.0000 |
| 750 | ours_controller_v2_nofallback | 514.9 | 0.3520 | 0.0683 | 0.0200 |
| 750 | probe_adaptive_k_selected | 523.9 | 0.3600 | 0.0689 | 0.0000 |
| 750 | probe_only_fixedk_k4 | 617.4 | 0.3600 | 0.0689 | 0.0000 |
| 750 | probe_only_fixedk_k8 | 622.2 | 0.3600 | 0.0689 | 0.0000 |
| 900 | hard_cap | 321.9 | 0.3060 | 0.1960 | 0.0000 |
| 900 | ours_controller_v2_nofallback | 548.7 | 0.3680 | 0.0774 | 0.0080 |
| 900 | probe_adaptive_k_selected | 575.2 | 0.3520 | 0.0693 | 0.0000 |
| 900 | probe_only_fixedk_k4 | 748.0 | 0.3520 | 0.0706 | 0.0000 |
| 900 | probe_only_fixedk_k8 | 768.9 | 0.3520 | 0.0693 | 0.0000 |
| 1200 | hard_cap | 327.1 | 0.3030 | 0.2027 | 0.0000 |
| 1200 | ours_controller_v2_nofallback | 600.2 | 0.3620 | 0.0671 | 0.0030 |
| 1200 | probe_adaptive_k_selected | 626.1 | 0.3540 | 0.0639 | 0.0000 |
| 1200 | probe_only_fixedk_k4 | 964.2 | 0.3560 | 0.0625 | 0.0000 |
| 1200 | probe_only_fixedk_k8 | 1071.1 | 0.3570 | 0.0570 | 0.0000 |
| 1500 | hard_cap | 327.0 | 0.3000 | 0.1932 | 0.0000 |
| 1500 | ours_controller_v2_nofallback | 615.2 | 0.3560 | 0.0645 | 0.0060 |
| 1500 | probe_adaptive_k_selected | 650.0 | 0.3600 | 0.0661 | 0.0000 |
| 1500 | probe_only_fixedk_k4 | 1072.8 | 0.3620 | 0.0556 | 0.0000 |
| 1500 | probe_only_fixedk_k8 | 1352.3 | 0.3650 | 0.0643 | 0.0000 |

## Probe Predictive Signal (nofallback)
- Baseline method for labels: `hard_cap`
| Budget | n trial-pairs | AUC(disagree->base_error) | ECE(disagree->base_error) | n docs | AUC(disagree->base_disagree>0) |
|---|---:|---:|---:|---:|---:|
| 300 | 1000 | 0.500 | 0.327 | 200 | 0.500 |
| 400 | 1000 | 0.538 | 0.624 | 200 | 0.437 |
| 500 | 1000 | 0.497 | 0.639 | 200 | 0.493 |
| 600 | 1000 | 0.471 | 0.654 | 200 | 0.461 |
| 750 | 1000 | 0.475 | 0.647 | 200 | 0.473 |
| 900 | 1000 | 0.470 | 0.660 | 200 | 0.464 |
| 1200 | 1000 | 0.473 | 0.667 | 200 | 0.499 |
| 1500 | 1000 | 0.471 | 0.670 | 200 | 0.484 |

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round7b_heldout_splitB2_r5_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round7b_heldout_splitB2_r5_v1/analysis_summary_round2.json`
