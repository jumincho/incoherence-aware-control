# round8smoke_format_splitA3_r1_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round8smoke_format_splitA3_r1_v1`
- Dataset: `Wanfq/gpqa:50 sampled from run manifest`
- Methods: `['hard_cap', 'ours_controller_v2_nofallback']`
- Budgets: `[400, 500, 600, 750]`
- Parse policy: `P1R`

## Reliability
- Records: `400` completed
- Hard fail: `0`
- Parse fail: `0` (`0.0000%`)
- Repair success: `48/48` (`100.0000%`)
- Duration: `2.37` minutes

## Phase Threshold
- nofallback beats hard_cap on incoh with no acc loss first at: `None`
- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `None`
- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `None`
- (parse-excluded) nofallback beats hard_cap on incoh with no acc loss first at: `None`
- Threshold bootstrap (hard_cap vs nofallback, parse-included): finite_rate=`0.000`, median=`nan`, 95% CI=`[nan, nan]`
- Threshold bootstrap (hard_cap vs nofallback, parse-excluded): finite_rate=`0.000`, median=`nan`, 95% CI=`[nan, nan]`

## nofallback Delta Table
| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |
|---|---:|---:|---:|---:|
| 400 | +0.0000 | +0.1000 | +nan | +nan |
| 500 | +0.0000 | +0.0400 | +nan | +nan |
| 600 | +0.0000 | +0.2000 | +nan | +nan |
| 750 | +0.0000 | +0.2000 | +nan | +nan |

## Parse-Fail Sensitivity (Included vs Excluded)
| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |
|---|---|---:|---:|---:|---:|---:|
| 400 | hard_cap | 0.2600 | 0.2600 | 0.0000 | 0.0000 | 50 |
| 400 | ours_controller_v2_nofallback | 0.3600 | 0.3600 | 0.0000 | 0.0000 | 50 |
| 500 | hard_cap | 0.3200 | 0.3200 | 0.0000 | 0.0000 | 50 |
| 500 | ours_controller_v2_nofallback | 0.3600 | 0.3600 | 0.0000 | 0.0000 | 50 |
| 600 | hard_cap | 0.2000 | 0.2000 | 0.0000 | 0.0000 | 50 |
| 600 | ours_controller_v2_nofallback | 0.4000 | 0.4000 | 0.0000 | 0.0000 | 50 |
| 750 | hard_cap | 0.2200 | 0.2200 | 0.0000 | 0.0000 | 50 |
| 750 | ours_controller_v2_nofallback | 0.4200 | 0.4200 | 0.0000 | 0.0000 | 50 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 400 | hard_cap | 0.000 | 0.180 | 1.000 |
| 400 | ours_controller_v2_nofallback | 0.000 | 0.180 | 1.000 |
| 500 | hard_cap | 0.000 | 0.080 | 1.000 |
| 500 | ours_controller_v2_nofallback | 0.000 | 0.120 | 1.000 |
| 600 | hard_cap | 0.000 | 0.060 | 1.000 |
| 600 | ours_controller_v2_nofallback | 0.000 | 0.140 | 1.000 |
| 750 | hard_cap | 0.000 | 0.040 | 1.000 |
| 750 | ours_controller_v2_nofallback | 0.000 | 0.160 | 1.000 |

## Method x Budget Parse-Fail Reasons
| Budget | Method | no_budget_for_repair | repair_called_but_failed | invalid_format_unresolved | multi_answer_unresolved | no_answer_token |
|---|---|---:|---:|---:|---:|---:|
| 400 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 400 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 500 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 600 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 600 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |
| 750 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 750 | ours_controller_v2_nofallback | 0 | 0 | 0 | 0 | 0 |

## Parse-Fail Gating Check
| Budget | Max ParseFail | Min ParseFail | Spread | Gate(max<=1%) | Gate(spread<=1%p) |
|---|---:|---:|---:|---:|---:|
| 400 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 500 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 600 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 750 | 0.000 | 0.000 | 0.000 | 1 | 1 |

## Cost Reality (Actual Total Tokens)
| Budget | Method | AvgTotalTok | Accuracy | Incoherence | ParseFail |
|---|---|---:|---:|---:|---:|
| 400 | ours_controller_v2_nofallback | 210.4 | 0.3600 | 0.0000 | 0.0000 |
| 400 | hard_cap | 241.8 | 0.2600 | 0.0000 | 0.0000 |
| 500 | hard_cap | 281.9 | 0.3200 | 0.0000 | 0.0000 |
| 500 | ours_controller_v2_nofallback | 314.5 | 0.3600 | 0.0000 | 0.0000 |
| 600 | hard_cap | 293.6 | 0.2000 | 0.0000 | 0.0000 |
| 600 | ours_controller_v2_nofallback | 385.0 | 0.4000 | 0.0000 | 0.0000 |
| 750 | hard_cap | 305.3 | 0.2200 | 0.0000 | 0.0000 |
| 750 | ours_controller_v2_nofallback | 481.0 | 0.4200 | 0.0000 | 0.0000 |

## nofallback Decision Breakdown
| Budget | Stop@Probe | ContinueSolve | FallbackHardCap | ProbeShare | SolveShare | AvgProbeTok | AvgSolveTok |
|---|---:|---:|---:|---:|---:|---:|---:|
| 400 | 0.820 | 0.180 | 0.000 | 0.954 | 0.000 | 200.7 | 0.0 |
| 500 | 0.880 | 0.120 | 0.000 | 0.980 | 0.000 | 308.1 | 0.0 |
| 600 | 0.860 | 0.140 | 0.000 | 0.973 | 0.000 | 374.5 | 0.0 |
| 750 | 0.820 | 0.180 | 0.000 | 0.976 | 0.000 | 469.4 | 0.0 |

## Probe Predictive Signal (nofallback)
- Baseline method for labels: `hard_cap`
| Budget | n trial-pairs | AUC(disagree->base_error) | ECE(disagree->base_error) | n docs | AUC(disagree->base_disagree>0) |
|---|---:|---:|---:|---:|---:|
| 400 | 50 | 0.518 | 0.640 | 50 | nan |
| 500 | 50 | 0.588 | 0.580 | 50 | nan |
| 600 | 50 | 0.588 | 0.700 | 50 | nan |
| 750 | 50 | 0.615 | 0.680 | 50 | nan |

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round8smoke_format_splitA3_r1_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round8smoke_format_splitA3_r1_v1/analysis_summary_round2.json`
