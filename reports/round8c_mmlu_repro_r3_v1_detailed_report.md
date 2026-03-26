# round8c_mmlu_repro_r3_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round8c_mmlu_repro_r3_v1`
- Dataset: `Wanfq/gpqa:200 sampled from run manifest`
- Methods: `['hard_cap', 'hard_cap_matched', 'ours_controller_v2_nofallback', 'probe_only_fixedk_k4']`
- Budgets: `[400, 900, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `7200` completed
- Hard fail: `0`
- Parse fail: `0` (`0.0000%`)
- Repair success: `259/259` (`100.0000%`)
- Duration: `46.47` minutes

## Phase Threshold
- nofallback beats hard_cap on incoh with no acc loss first at: `400`
- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `None`
- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `None`
- (parse-excluded) nofallback beats hard_cap on incoh with no acc loss first at: `400`
- Threshold bootstrap (hard_cap vs nofallback, parse-included): finite_rate=`1.000`, median=`400.0`, 95% CI=`[400.0, 400.0]`
- Threshold bootstrap (hard_cap vs nofallback, parse-excluded): finite_rate=`1.000`, median=`400.0`, 95% CI=`[400.0, 400.0]`

## nofallback Delta Table
| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |
|---|---:|---:|---:|---:|
| 400 | -0.1331 | +0.2917 | +nan | +nan |
| 900 | -0.1401 | +0.3133 | +nan | +nan |
| 1500 | -0.1458 | +0.3050 | +nan | +nan |

## Parse-Fail Sensitivity (Included vs Excluded)
| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |
|---|---|---:|---:|---:|---:|---:|
| 400 | hard_cap | 0.4050 | 0.4050 | 0.1705 | 0.1705 | 200 |
| 400 | hard_cap_matched | 0.4050 | 0.4050 | 0.1705 | 0.1705 | 200 |
| 400 | ours_controller_v2_nofallback | 0.6967 | 0.6967 | 0.0374 | 0.0374 | 200 |
| 400 | probe_only_fixedk_k4 | 0.7017 | 0.7017 | 0.0221 | 0.0221 | 200 |
| 900 | hard_cap | 0.4200 | 0.4200 | 0.1646 | 0.1646 | 200 |
| 900 | hard_cap_matched | 0.4383 | 0.4383 | 0.1752 | 0.1752 | 200 |
| 900 | ours_controller_v2_nofallback | 0.7333 | 0.7333 | 0.0245 | 0.0245 | 200 |
| 900 | probe_only_fixedk_k4 | 0.7367 | 0.7367 | 0.0124 | 0.0124 | 200 |
| 1500 | hard_cap | 0.4400 | 0.4400 | 0.1650 | 0.1650 | 200 |
| 1500 | hard_cap_matched | 0.4650 | 0.4650 | 0.1866 | 0.1866 | 200 |
| 1500 | ours_controller_v2_nofallback | 0.7450 | 0.7450 | 0.0192 | 0.0192 | 200 |
| 1500 | probe_only_fixedk_k4 | 0.7350 | 0.7350 | 0.0364 | 0.0364 | 200 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 400 | hard_cap | 0.000 | 0.100 | 1.000 |
| 400 | hard_cap_matched | 0.000 | 0.100 | 1.000 |
| 400 | ours_controller_v2_nofallback | 0.000 | 0.115 | 1.000 |
| 400 | probe_only_fixedk_k4 | 0.000 | 0.105 | 1.000 |
| 900 | hard_cap | 0.000 | 0.000 | 0.000 |
| 900 | hard_cap_matched | 0.000 | 0.000 | 0.000 |
| 900 | ours_controller_v2_nofallback | 0.000 | 0.010 | 1.000 |
| 900 | probe_only_fixedk_k4 | 0.000 | 0.000 | 0.000 |
| 1500 | hard_cap | 0.000 | 0.000 | 0.000 |
| 1500 | hard_cap_matched | 0.000 | 0.000 | 0.000 |
| 1500 | ours_controller_v2_nofallback | 0.000 | 0.002 | 1.000 |
| 1500 | probe_only_fixedk_k4 | 0.000 | 0.000 | 0.000 |

## Method x Budget Parse-Fail Reasons
| Budget | Method | no_budget_for_repair | repair_called_but_failed | invalid_format_unresolved | multi_answer_unresolved | no_answer_token |
|---|---|---:|---:|---:|---:|---:|
| 400 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 400 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 400 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 900 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 900 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 900 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 1500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 1500 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 1500 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |

## Parse-Fail Gating Check
| Budget | Max ParseFail | Min ParseFail | Spread | Gate(max<=1%) | Gate(spread<=1%p) |
|---|---:|---:|---:|---:|---:|
| 400 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 900 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 1500 | 0.000 | 0.000 | 0.000 | 1 | 1 |

## Cost Reality (Actual Total Tokens)
| Budget | Method | AvgTotalTok | Accuracy | Incoherence | ParseFail |
|---|---|---:|---:|---:|---:|
| 400 | hard_cap | 183.3 | 0.4050 | 0.1705 | 0.0000 |
| 400 | hard_cap_matched | 183.3 | 0.4050 | 0.1705 | 0.0000 |
| 400 | ours_controller_v2_nofallback | 237.6 | 0.6967 | 0.0374 | 0.0000 |
| 400 | probe_only_fixedk_k4 | 256.9 | 0.7017 | 0.0221 | 0.0000 |
| 900 | hard_cap | 227.8 | 0.4200 | 0.1646 | 0.0000 |
| 900 | hard_cap_matched | 241.1 | 0.4383 | 0.1752 | 0.0000 |
| 900 | ours_controller_v2_nofallback | 379.6 | 0.7333 | 0.0245 | 0.0000 |
| 900 | probe_only_fixedk_k4 | 631.6 | 0.7367 | 0.0124 | 0.0000 |
| 1500 | hard_cap | 228.0 | 0.4400 | 0.1650 | 0.0000 |
| 1500 | hard_cap_matched | 242.0 | 0.4650 | 0.1866 | 0.0000 |
| 1500 | ours_controller_v2_nofallback | 404.2 | 0.7450 | 0.0192 | 0.0000 |
| 1500 | probe_only_fixedk_k4 | 758.3 | 0.7350 | 0.0364 | 0.0000 |

## nofallback Decision Breakdown
| Budget | Stop@Probe | ContinueSolve | FallbackHardCap | ProbeShare | SolveShare | AvgProbeTok | AvgSolveTok |
|---|---:|---:|---:|---:|---:|---:|---:|
| 400 | 0.880 | 0.120 | 0.000 | 0.972 | 0.000 | 231.0 | 0.0 |
| 900 | 0.990 | 0.010 | 0.000 | 0.999 | 0.000 | 379.1 | 0.0 |
| 1500 | 0.990 | 0.010 | 0.000 | 0.995 | 0.004 | 402.4 | 1.8 |

## Probe Predictive Signal (nofallback)
- Baseline method for labels: `hard_cap`
| Budget | n trial-pairs | AUC(disagree->base_error) | ECE(disagree->base_error) | n docs | AUC(disagree->base_disagree>0) |
|---|---:|---:|---:|---:|---:|
| 400 | 600 | 0.521 | 0.556 | 200 | 0.428 |
| 900 | 600 | 0.509 | 0.574 | 200 | 0.507 |
| 1500 | 600 | 0.503 | 0.553 | 200 | 0.499 |

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round8c_mmlu_repro_r3_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round8c_mmlu_repro_r3_v1/analysis_summary_round2.json`
