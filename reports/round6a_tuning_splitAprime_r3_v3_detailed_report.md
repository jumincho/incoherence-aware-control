# round6a_tuning_splitAprime_r3_v3 Detailed Report

## Run Meta
- Run dir: `/data2/chojm/incoh-pilot/runs/round6a_tuning_splitAprime_r3_v3`
- Dataset: `Wanfq/gpqa:200 sampled from run manifest`
- Methods: `['hard_cap', 'probe_only_fixedk', 'probe_adaptive_k_t67', 'probe_adaptive_k_t75', 'probe_adaptive_k_t80', 'ours_controller_v2_nofallback']`
- Budgets: `[200, 300, 400, 500, 600, 750, 900, 1200, 1500]`
- Parse policy: `P1R`

## Reliability
- Records: `32400` completed
- Hard fail: `0`
- Parse fail: `506` (`1.5617%`)
- Repair success: `5475/5981` (`91.5399%`)
- Duration: `182.58` minutes

## Phase Threshold
- nofallback beats hard_cap on incoh with no acc loss first at: `1200`
- nofallback beats budgeted_sc on incoh with <=1% acc drop first at: `None`
- nofallback beats budgeted_sc on incoh with <=2% acc drop first at: `None`
- Threshold bootstrap (hard_cap vs nofallback): finite_rate=`0.950`, median=`600.0`, 95% CI=`[400.0, 1500.0]`

## nofallback Delta Table
| Budget | Δincoh(nf-hc) | Δacc(nf-hc) | Δincoh(nf-sc) | Δacc(nf-sc) |
|---|---:|---:|---:|---:|
| 200 | +0.0111 | -0.0183 | +nan | +nan |
| 300 | +0.0179 | -0.0617 | +nan | +nan |
| 400 | -0.0194 | -0.0150 | +nan | +nan |
| 500 | -0.0308 | -0.0100 | +nan | +nan |
| 600 | -0.0555 | -0.0200 | +nan | +nan |
| 750 | -0.0222 | -0.0050 | +nan | +nan |
| 900 | -0.0389 | -0.0233 | +nan | +nan |
| 1200 | -0.0284 | +0.0033 | +nan | +nan |
| 1500 | -0.0404 | +0.0050 | +nan | +nan |

## Parse-Fail Sensitivity (Included vs Excluded)
| Budget | Method | Acc(incl) | Acc(excl) | Incoh(incl) | Incoh(excl) | n_docs_excl |
|---|---|---:|---:|---:|---:|---:|
| 200 | hard_cap | 0.2933 | 0.3024 | 0.0047 | 0.0049 | 194 |
| 200 | probe_only_fixedk | 0.2800 | 0.2995 | 0.0069 | 0.0076 | 187 |
| 200 | probe_adaptive_k_t67 | 0.2783 | 0.2977 | 0.0114 | 0.0125 | 187 |
| 200 | probe_adaptive_k_t75 | 0.2783 | 0.2977 | 0.0114 | 0.0125 | 187 |
| 200 | probe_adaptive_k_t80 | 0.2783 | 0.2977 | 0.0114 | 0.0125 | 187 |
| 200 | ours_controller_v2_nofallback | 0.2750 | 0.2910 | 0.0158 | 0.0207 | 189 |
| 300 | hard_cap | 0.3400 | 0.3417 | 0.0625 | 0.0630 | 199 |
| 300 | probe_only_fixedk | 0.3500 | 0.3627 | 0.0299 | 0.0315 | 193 |
| 300 | probe_adaptive_k_t67 | 0.3467 | 0.3556 | 0.0528 | 0.0530 | 195 |
| 300 | probe_adaptive_k_t75 | 0.3467 | 0.3556 | 0.0528 | 0.0530 | 195 |
| 300 | probe_adaptive_k_t80 | 0.3467 | 0.3556 | 0.0528 | 0.0530 | 195 |
| 300 | ours_controller_v2_nofallback | 0.2783 | 0.3200 | 0.0804 | 0.0808 | 187 |
| 400 | hard_cap | 0.3667 | 0.3667 | 0.0758 | 0.0758 | 200 |
| 400 | probe_only_fixedk | 0.3633 | 0.3652 | 0.0406 | 0.0409 | 199 |
| 400 | probe_adaptive_k_t67 | 0.3500 | 0.3570 | 0.0618 | 0.0597 | 197 |
| 400 | probe_adaptive_k_t75 | 0.3500 | 0.3570 | 0.0618 | 0.0597 | 197 |
| 400 | probe_adaptive_k_t80 | 0.3500 | 0.3570 | 0.0618 | 0.0597 | 197 |
| 400 | ours_controller_v2_nofallback | 0.3517 | 0.3561 | 0.0564 | 0.0549 | 198 |
| 500 | hard_cap | 0.3733 | 0.3752 | 0.0797 | 0.0803 | 199 |
| 500 | probe_only_fixedk | 0.3550 | 0.3568 | 0.0538 | 0.0542 | 199 |
| 500 | probe_adaptive_k_t67 | 0.3750 | 0.3802 | 0.0746 | 0.0700 | 199 |
| 500 | probe_adaptive_k_t75 | 0.3750 | 0.3802 | 0.0746 | 0.0700 | 199 |
| 500 | probe_adaptive_k_t80 | 0.3750 | 0.3802 | 0.0746 | 0.0700 | 199 |
| 500 | ours_controller_v2_nofallback | 0.3633 | 0.3652 | 0.0489 | 0.0475 | 199 |
| 600 | hard_cap | 0.3967 | 0.3967 | 0.1053 | 0.1053 | 200 |
| 600 | probe_only_fixedk | 0.3717 | 0.3717 | 0.0479 | 0.0479 | 200 |
| 600 | probe_adaptive_k_t67 | 0.3783 | 0.3783 | 0.0582 | 0.0582 | 200 |
| 600 | probe_adaptive_k_t75 | 0.3783 | 0.3783 | 0.0582 | 0.0582 | 200 |
| 600 | probe_adaptive_k_t80 | 0.3783 | 0.3783 | 0.0582 | 0.0582 | 200 |
| 600 | ours_controller_v2_nofallback | 0.3767 | 0.3827 | 0.0498 | 0.0481 | 199 |
| 750 | hard_cap | 0.3867 | 0.3867 | 0.0870 | 0.0870 | 200 |
| 750 | probe_only_fixedk | 0.3583 | 0.3601 | 0.0519 | 0.0522 | 199 |
| 750 | probe_adaptive_k_t67 | 0.3683 | 0.3702 | 0.0455 | 0.0458 | 199 |
| 750 | probe_adaptive_k_t75 | 0.3683 | 0.3702 | 0.0455 | 0.0458 | 199 |
| 750 | probe_adaptive_k_t80 | 0.3683 | 0.3702 | 0.0455 | 0.0458 | 199 |
| 750 | ours_controller_v2_nofallback | 0.3817 | 0.3864 | 0.0647 | 0.0651 | 198 |
| 900 | hard_cap | 0.3950 | 0.3950 | 0.0740 | 0.0740 | 200 |
| 900 | probe_only_fixedk | 0.3617 | 0.3617 | 0.0397 | 0.0397 | 200 |
| 900 | probe_adaptive_k_t67 | 0.3767 | 0.3767 | 0.0437 | 0.0437 | 200 |
| 900 | probe_adaptive_k_t75 | 0.3767 | 0.3767 | 0.0437 | 0.0437 | 200 |
| 900 | probe_adaptive_k_t80 | 0.3767 | 0.3767 | 0.0437 | 0.0437 | 200 |
| 900 | ours_controller_v2_nofallback | 0.3717 | 0.3783 | 0.0351 | 0.0338 | 200 |
| 1200 | hard_cap | 0.3817 | 0.3817 | 0.0810 | 0.0810 | 200 |
| 1200 | probe_only_fixedk | 0.3600 | 0.3600 | 0.0327 | 0.0327 | 200 |
| 1200 | probe_adaptive_k_t67 | 0.3767 | 0.3800 | 0.0484 | 0.0469 | 200 |
| 1200 | probe_adaptive_k_t75 | 0.3767 | 0.3800 | 0.0484 | 0.0469 | 200 |
| 1200 | probe_adaptive_k_t80 | 0.3767 | 0.3800 | 0.0484 | 0.0469 | 200 |
| 1200 | ours_controller_v2_nofallback | 0.3850 | 0.3917 | 0.0526 | 0.0497 | 200 |
| 1500 | hard_cap | 0.3800 | 0.3800 | 0.0889 | 0.0889 | 200 |
| 1500 | probe_only_fixedk | 0.3700 | 0.3700 | 0.0409 | 0.0409 | 200 |
| 1500 | probe_adaptive_k_t67 | 0.3783 | 0.3783 | 0.0406 | 0.0388 | 200 |
| 1500 | probe_adaptive_k_t75 | 0.3783 | 0.3783 | 0.0406 | 0.0388 | 200 |
| 1500 | probe_adaptive_k_t80 | 0.3783 | 0.3783 | 0.0431 | 0.0412 | 200 |
| 1500 | ours_controller_v2_nofallback | 0.3850 | 0.3917 | 0.0485 | 0.0451 | 200 |

## Method x Budget Repair
| Budget | Method | ParseFail | RepairAttempt | RepairSuccess|
|---|---|---:|---:|---:|
| 200 | hard_cap | 0.030 | 0.930 | 0.968 |
| 200 | probe_only_fixedk | 0.065 | 0.915 | 0.929 |
| 200 | probe_adaptive_k_t67 | 0.065 | 0.915 | 0.929 |
| 200 | probe_adaptive_k_t75 | 0.065 | 0.915 | 0.929 |
| 200 | probe_adaptive_k_t80 | 0.065 | 0.915 | 0.929 |
| 200 | ours_controller_v2_nofallback | 0.057 | 0.932 | 0.939 |
| 300 | hard_cap | 0.005 | 0.335 | 0.985 |
| 300 | probe_only_fixedk | 0.035 | 0.340 | 0.897 |
| 300 | probe_adaptive_k_t67 | 0.030 | 0.338 | 0.911 |
| 300 | probe_adaptive_k_t75 | 0.030 | 0.338 | 0.911 |
| 300 | probe_adaptive_k_t80 | 0.030 | 0.338 | 0.911 |
| 300 | ours_controller_v2_nofallback | 0.122 | 0.437 | 0.721 |
| 400 | hard_cap | 0.000 | 0.155 | 1.000 |
| 400 | probe_only_fixedk | 0.005 | 0.150 | 0.967 |
| 400 | probe_adaptive_k_t67 | 0.018 | 0.173 | 0.894 |
| 400 | probe_adaptive_k_t75 | 0.018 | 0.173 | 0.894 |
| 400 | probe_adaptive_k_t80 | 0.018 | 0.173 | 0.894 |
| 400 | ours_controller_v2_nofallback | 0.013 | 0.172 | 0.922 |
| 500 | hard_cap | 0.005 | 0.075 | 0.933 |
| 500 | probe_only_fixedk | 0.005 | 0.070 | 0.929 |
| 500 | probe_adaptive_k_t67 | 0.010 | 0.093 | 0.893 |
| 500 | probe_adaptive_k_t75 | 0.010 | 0.093 | 0.893 |
| 500 | probe_adaptive_k_t80 | 0.010 | 0.093 | 0.893 |
| 500 | ours_controller_v2_nofallback | 0.017 | 0.113 | 0.853 |
| 600 | hard_cap | 0.000 | 0.030 | 1.000 |
| 600 | probe_only_fixedk | 0.000 | 0.030 | 1.000 |
| 600 | probe_adaptive_k_t67 | 0.000 | 0.052 | 1.000 |
| 600 | probe_adaptive_k_t75 | 0.000 | 0.052 | 1.000 |
| 600 | probe_adaptive_k_t80 | 0.000 | 0.052 | 1.000 |
| 600 | ours_controller_v2_nofallback | 0.015 | 0.088 | 0.830 |
| 750 | hard_cap | 0.000 | 0.015 | 1.000 |
| 750 | probe_only_fixedk | 0.005 | 0.015 | 0.667 |
| 750 | probe_adaptive_k_t67 | 0.008 | 0.032 | 0.737 |
| 750 | probe_adaptive_k_t75 | 0.008 | 0.032 | 0.737 |
| 750 | probe_adaptive_k_t80 | 0.008 | 0.032 | 0.737 |
| 750 | ours_controller_v2_nofallback | 0.015 | 0.080 | 0.812 |
| 900 | hard_cap | 0.000 | 0.010 | 1.000 |
| 900 | probe_only_fixedk | 0.000 | 0.010 | 1.000 |
| 900 | probe_adaptive_k_t67 | 0.000 | 0.023 | 1.000 |
| 900 | probe_adaptive_k_t75 | 0.000 | 0.023 | 1.000 |
| 900 | probe_adaptive_k_t80 | 0.000 | 0.023 | 1.000 |
| 900 | ours_controller_v2_nofallback | 0.015 | 0.058 | 0.743 |
| 1200 | hard_cap | 0.000 | 0.000 | 0.000 |
| 1200 | probe_only_fixedk | 0.000 | 0.000 | 0.000 |
| 1200 | probe_adaptive_k_t67 | 0.005 | 0.012 | 0.571 |
| 1200 | probe_adaptive_k_t75 | 0.005 | 0.012 | 0.571 |
| 1200 | probe_adaptive_k_t80 | 0.005 | 0.012 | 0.571 |
| 1200 | ours_controller_v2_nofallback | 0.013 | 0.042 | 0.680 |
| 1500 | hard_cap | 0.000 | 0.000 | 0.000 |
| 1500 | probe_only_fixedk | 0.000 | 0.000 | 0.000 |
| 1500 | probe_adaptive_k_t67 | 0.002 | 0.008 | 0.800 |
| 1500 | probe_adaptive_k_t75 | 0.002 | 0.008 | 0.800 |
| 1500 | probe_adaptive_k_t80 | 0.002 | 0.008 | 0.800 |
| 1500 | ours_controller_v2_nofallback | 0.007 | 0.027 | 0.750 |

## Probe Predictive Signal (nofallback)
| Budget | n trial-pairs | AUC(probe_disagree -> baseline_error) | n docs | AUC(probe_disagree -> baseline_disagreement>0) |
|---|---:|---:|---:|---:|

## Source Files
- Summary: `/data2/chojm/incoh-pilot/runs/round6a_tuning_splitAprime_r3_v3/round2_summary.md`
- Analysis JSON: `/data2/chojm/incoh-pilot/runs/round6a_tuning_splitAprime_r3_v3/analysis_summary_round2.json`
