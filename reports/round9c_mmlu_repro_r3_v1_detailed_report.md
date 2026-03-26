# round9c_mmlu_repro_r3_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round9c_mmlu_repro_r3_v1`
- Dataset: `cais/mmlu:all:test`, `n_questions=200`, `sample_seed=20260501`
- Methods: `['hard_cap', 'hard_cap_matched', 'probe_only_fixedk_k4', 'budgeted_self_consistency', 'ours_controller_v3_nofallback']`
- Budgets: `[400, 900, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `9000` completed
- Hard fail: `0`
- Parse fail: `0` (`0.0000%`)
- Repair success: `723/723` (`100.0000%`)
- Duration: `74.25` minutes

## Phase Threshold
- nofallback beats hard_cap on incoh with no acc loss first at: `None`
- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `None`
- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `None`
- (parse-excluded) nofallback beats hard_cap on incoh with no acc loss first at: `None`

## nofallback Delta Table
| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |
|---|---:|---:|---:|---:|

## Parse-Fail Sensitivity (Included vs Excluded)
| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |
|---|---|---:|---:|---:|---:|---:|
| 400 | hard_cap | 0.4267 | 0.4267 | 0.1342 | 0.1342 | 200 |
| 400 | hard_cap_matched | 0.4333 | 0.4333 | 0.1342 | 0.1342 | 200 |
| 400 | probe_only_fixedk_k4 | 0.7217 | 0.7217 | 0.0059 | 0.0059 | 200 |
| 400 | budgeted_self_consistency | 0.5167 | 0.5167 | 0.0812 | 0.0812 | 200 |
| 400 | ours_controller_v3_nofallback | 0.3133 | 0.3133 | 0.0072 | 0.0072 | 200 |
| 900 | hard_cap | 0.4583 | 0.4583 | 0.1769 | 0.1769 | 200 |
| 900 | hard_cap_matched | 0.4800 | 0.4800 | 0.1853 | 0.1853 | 200 |
| 900 | probe_only_fixedk_k4 | 0.7633 | 0.7633 | 0.0204 | 0.0204 | 200 |
| 900 | budgeted_self_consistency | 0.5400 | 0.5400 | 0.0900 | 0.0900 | 200 |
| 900 | ours_controller_v3_nofallback | 0.7883 | 0.7883 | 0.0373 | 0.0373 | 200 |
| 1500 | hard_cap | 0.4283 | 0.4283 | 0.1546 | 0.1546 | 200 |
| 1500 | hard_cap_matched | 0.4567 | 0.4567 | 0.1697 | 0.1697 | 200 |
| 1500 | probe_only_fixedk_k4 | 0.7650 | 0.7650 | 0.0270 | 0.0270 | 200 |
| 1500 | budgeted_self_consistency | 0.5350 | 0.5350 | 0.0792 | 0.0792 | 200 |
| 1500 | ours_controller_v3_nofallback | 0.7867 | 0.7867 | 0.0153 | 0.0153 | 200 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 400 | hard_cap | 0.000 | 0.080 | 1.000 |
| 400 | hard_cap_matched | 0.000 | 0.080 | 1.000 |
| 400 | probe_only_fixedk_k4 | 0.000 | 0.085 | 1.000 |
| 400 | budgeted_self_consistency | 0.000 | 0.080 | 1.000 |
| 400 | ours_controller_v3_nofallback | 0.000 | 0.877 | 1.000 |
| 900 | hard_cap | 0.000 | 0.000 | 0.000 |
| 900 | hard_cap_matched | 0.000 | 0.000 | 0.000 |
| 900 | probe_only_fixedk_k4 | 0.000 | 0.000 | 0.000 |
| 900 | budgeted_self_consistency | 0.000 | 0.000 | 0.000 |
| 900 | ours_controller_v3_nofallback | 0.000 | 0.003 | 1.000 |
| 1500 | hard_cap | 0.000 | 0.000 | 0.000 |
| 1500 | hard_cap_matched | 0.000 | 0.000 | 0.000 |
| 1500 | probe_only_fixedk_k4 | 0.000 | 0.000 | 0.000 |
| 1500 | budgeted_self_consistency | 0.000 | 0.000 | 0.000 |
| 1500 | ours_controller_v3_nofallback | 0.000 | 0.000 | 0.000 |

## Method x Budget Parse-Fail Reasons
| Budget | Method | no_budget_for_repair | repair_called_but_failed | invalid_format_unresolved | multi_answer_unresolved | no_answer_token |
|---|---|---:|---:|---:|---:|---:|
| 400 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 400 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 400 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 400 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 900 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 900 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 900 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 900 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 900 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 1500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 1500 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 1500 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 1500 | budgeted_self_consistency | 0 | 0 | 0 | 0 | 0 |
| 1500 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |

## Parse-Fail Gating Check
| Budget | Max ParseFail | Min ParseFail | Spread | Gate(max<=1%) | Gate(spread<=1%p) |
|---|---:|---:|---:|---:|---:|
| 400 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 900 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 1500 | 0.000 | 0.000 | 0.000 | 1 | 1 |

## Cost Reality (Actual Total Tokens)
| Budget | Method | AvgTotalTok | Accuracy | Incoherence | ParseFail |
|---|---|---:|---:|---:|---:|
| 400 | hard_cap | 173.6 | 0.4267 | 0.1342 | 0.0000 |
| 400 | hard_cap_matched | 176.3 | 0.4333 | 0.1342 | 0.0000 |
| 400 | probe_only_fixedk_k4 | 259.8 | 0.7217 | 0.0059 | 0.0000 |
| 400 | budgeted_self_consistency | 272.0 | 0.5167 | 0.0812 | 0.0000 |
| 400 | ours_controller_v3_nofallback | 299.5 | 0.3133 | 0.0072 | 0.0000 |
| 900 | hard_cap | 211.3 | 0.4583 | 0.1769 | 0.0000 |
| 900 | hard_cap_matched | 219.2 | 0.4800 | 0.1853 | 0.0000 |
| 900 | ours_controller_v3_nofallback | 347.8 | 0.7883 | 0.0373 | 0.0000 |
| 900 | probe_only_fixedk_k4 | 617.7 | 0.7633 | 0.0204 | 0.0000 |
| 900 | budgeted_self_consistency | 684.9 | 0.5400 | 0.0900 | 0.0000 |
| 1500 | hard_cap | 213.0 | 0.4283 | 0.1546 | 0.0000 |
| 1500 | hard_cap_matched | 222.9 | 0.4567 | 0.1697 | 0.0000 |
| 1500 | ours_controller_v3_nofallback | 373.0 | 0.7867 | 0.0153 | 0.0000 |
| 1500 | probe_only_fixedk_k4 | 704.3 | 0.7650 | 0.0270 | 0.0000 |
| 1500 | budgeted_self_consistency | 800.1 | 0.5350 | 0.0792 | 0.0000 |

## nofallback Decision Breakdown
| Budget | Stop@Probe | ContinueSolve | FallbackHardCap | ProbeShare | SolveShare | AvgProbeTok | AvgSolveTok |
|---|---:|---:|---:|---:|---:|---:|---:|
| 400 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |
| 900 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |
| 1500 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |

## Probe Predictive Signal (nofallback)
- Baseline method for labels: `hard_cap`
| Budget | n trial-pairs | AUC(disagree->base_error) | ECE(disagree->base_error) | n docs | AUC(disagree->base_disagree>0) |
|---|---:|---:|---:|---:|---:|

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round9c_mmlu_repro_r3_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round9c_mmlu_repro_r3_v1/analysis_summary_round2.json`
