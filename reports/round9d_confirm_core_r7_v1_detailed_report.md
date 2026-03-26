# round9d_confirm_core_r7_v1 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round9d_confirm_core_r7_v1`
- Dataset: `Wanfq/gpqa:gpqa_main:train`, `n_questions=600`, `sample_seed=20260430`
- Methods: `['hard_cap', 'hard_cap_matched', 'probe_only_fixedk_k4', 'ours_controller_v3_nofallback']`
- Budgets: `[400, 500, 600]`
- Parse policy: `P1R`

## Reliability
- Records: `12432` completed
- Hard fail: `0`
- Parse fail: `0` (`0.0000%`)
- Repair success: `3594/3594` (`100.0000%`)
- Duration: `84.98` minutes

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
| 400 | hard_cap | 0.2905 | 0.2905 | 0.1878 | 0.1878 | 148 |
| 400 | hard_cap_matched | 0.2934 | 0.2934 | 0.1985 | 0.1985 | 148 |
| 400 | probe_only_fixedk_k4 | 0.4035 | 0.4035 | 0.0776 | 0.0776 | 148 |
| 400 | ours_controller_v3_nofallback | 0.2568 | 0.2568 | 0.0000 | 0.0000 | 148 |
| 500 | hard_cap | 0.3098 | 0.3098 | 0.2136 | 0.2136 | 148 |
| 500 | hard_cap_matched | 0.3108 | 0.3108 | 0.2495 | 0.2495 | 148 |
| 500 | probe_only_fixedk_k4 | 0.4073 | 0.4073 | 0.0745 | 0.0745 | 148 |
| 500 | ours_controller_v3_nofallback | 0.2597 | 0.2597 | 0.0116 | 0.0116 | 148 |
| 600 | hard_cap | 0.3069 | 0.3069 | 0.2004 | 0.2004 | 148 |
| 600 | hard_cap_matched | 0.3330 | 0.3330 | 0.2359 | 0.2359 | 148 |
| 600 | probe_only_fixedk_k4 | 0.3996 | 0.3996 | 0.0722 | 0.0722 | 148 |
| 600 | ours_controller_v3_nofallback | 0.2510 | 0.2510 | 0.0202 | 0.0202 | 148 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 400 | hard_cap | 0.000 | 0.142 | 1.000 |
| 400 | hard_cap_matched | 0.000 | 0.142 | 1.000 |
| 400 | probe_only_fixedk_k4 | 0.000 | 0.135 | 1.000 |
| 400 | ours_controller_v3_nofallback | 0.000 | 0.993 | 1.000 |
| 500 | hard_cap | 0.000 | 0.047 | 1.000 |
| 500 | hard_cap_matched | 0.000 | 0.047 | 1.000 |
| 500 | probe_only_fixedk_k4 | 0.000 | 0.041 | 1.000 |
| 500 | ours_controller_v3_nofallback | 0.000 | 0.959 | 1.000 |
| 600 | hard_cap | 0.000 | 0.027 | 1.000 |
| 600 | hard_cap_matched | 0.000 | 0.027 | 1.000 |
| 600 | probe_only_fixedk_k4 | 0.000 | 0.027 | 1.000 |
| 600 | ours_controller_v3_nofallback | 0.000 | 0.881 | 1.000 |

## Method x Budget Parse-Fail Reasons
| Budget | Method | no_budget_for_repair | repair_called_but_failed | invalid_format_unresolved | multi_answer_unresolved | no_answer_token |
|---|---|---:|---:|---:|---:|---:|
| 400 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 400 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 400 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 400 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 500 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 500 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 500 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 500 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |
| 600 | hard_cap | 0 | 0 | 0 | 0 | 0 |
| 600 | hard_cap_matched | 0 | 0 | 0 | 0 | 0 |
| 600 | probe_only_fixedk_k4 | 0 | 0 | 0 | 0 | 0 |
| 600 | ours_controller_v3_nofallback | 0 | 0 | 0 | 0 | 0 |

## Parse-Fail Gating Check
| Budget | Max ParseFail | Min ParseFail | Spread | Gate(max<=1%) | Gate(spread<=1%p) |
|---|---:|---:|---:|---:|---:|
| 400 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 500 | 0.000 | 0.000 | 0.000 | 1 | 1 |
| 600 | 0.000 | 0.000 | 0.000 | 1 | 1 |

## Cost Reality (Actual Total Tokens)
| Budget | Method | AvgTotalTok | Accuracy | Incoherence | ParseFail |
|---|---|---:|---:|---:|---:|
| 400 | probe_only_fixedk_k4 | 251.4 | 0.4035 | 0.0776 | 0.0000 |
| 400 | hard_cap | 254.7 | 0.2905 | 0.1878 | 0.0000 |
| 400 | hard_cap_matched | 261.8 | 0.2934 | 0.1985 | 0.0000 |
| 400 | ours_controller_v3_nofallback | 283.1 | 0.2568 | 0.0000 | 0.0000 |
| 500 | hard_cap | 293.9 | 0.3098 | 0.2136 | 0.0000 |
| 500 | hard_cap_matched | 326.4 | 0.3108 | 0.2495 | 0.0000 |
| 500 | probe_only_fixedk_k4 | 329.2 | 0.4073 | 0.0745 | 0.0000 |
| 500 | ours_controller_v3_nofallback | 364.1 | 0.2597 | 0.0116 | 0.0000 |
| 600 | hard_cap | 305.1 | 0.3069 | 0.2004 | 0.0000 |
| 600 | hard_cap_matched | 351.3 | 0.3330 | 0.2359 | 0.0000 |
| 600 | probe_only_fixedk_k4 | 413.7 | 0.3996 | 0.0722 | 0.0000 |
| 600 | ours_controller_v3_nofallback | 461.8 | 0.2510 | 0.0202 | 0.0000 |

## nofallback Decision Breakdown
| Budget | Stop@Probe | ContinueSolve | FallbackHardCap | ProbeShare | SolveShare | AvgProbeTok | AvgSolveTok |
|---|---:|---:|---:|---:|---:|---:|---:|
| 400 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |
| 500 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |
| 600 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.0 | 0.0 |

## Probe Predictive Signal (nofallback)
- Baseline method for labels: `hard_cap`
| Budget | n trial-pairs | AUC(disagree->base_error) | ECE(disagree->base_error) | n docs | AUC(disagree->base_disagree>0) |
|---|---:|---:|---:|---:|---:|

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round9d_confirm_core_r7_v1/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round9d_confirm_core_r7_v1/analysis_summary_round2.json`
