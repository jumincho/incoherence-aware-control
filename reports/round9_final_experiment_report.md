# Round9 Final Experiment Report (Extended)

- Generated at: `2026-03-03 03:03:45 UTC`
- Runs: A9=`round9a_tuning_splitA9_r3_v1`, B9=`round9b_heldout_splitB9_r5_v1`, D9=`round9d_confirm_core_r7_v1`, C9=`round9c_mmlu_repro_r3_v1`
- Selected adaptive (A9): `probe_adaptive_k_t67`
- hard_cap_matched map: `{'300': 91, '350': 93, '400': 101, '450': 131, '500': 164, '600': 237, '900': 301, '1500': 377}`

## 1) Execution Summary
| Run | Records | Duration(min) | ParseFail | HardFail |
|---|---:|---:|---:|---:|
| round9a_tuning_splitA9_r3_v1 | 64800 | 395.08 | 0 | 0 |
| round9b_heldout_splitB9_r5_v1 | 47360 | 313.13 | 0 | 0 |
| round9d_confirm_core_r7_v1 | 12432 | 84.98 | 0 | 0 |
| round9c_mmlu_repro_r3_v1 | 9000 | 74.25 | 0 | 0 |

## 2) Held-out GPQA (B9) Main Result
- Transition threshold (v3 vs hard_cap): `T*=900`
- Interpretation: v3는 `T<900`에서 정확도 희생을 동반하고, `T>=900`에서 accuracy/incoherence 동시 개선으로 전환됩니다.

| Budget | Δacc(v3-hc) | 95% CI(acc Δ) | Δincoh(v3-hc) | v3 acc/incoh/tok | hc acc/incoh/tok |
|---|---:|---:|---:|---|---|
| 300 | -0.0230 | [-0.0703, +0.0243] | -0.0986 | 0.2568/0.0000/151.3 | 0.2797/0.0986/142.7 |
| 350 | -0.0257 | [-0.0743, +0.0230] | -0.1613 | 0.2568/0.0000/225.4 | 0.2824/0.1613/205.1 |
| 400 | -0.0324 | [-0.0784, +0.0135] | -0.1783 | 0.2568/0.0000/283.0 | 0.2892/0.1783/254.6 |
| 450 | -0.0486 | [-0.0986, +0.0027] | -0.1862 | 0.2568/0.0000/324.8 | 0.3054/0.1862/281.0 |
| 500 | -0.0608 | [-0.1163, -0.0040] | -0.1967 | 0.2595/0.0126/364.0 | 0.3203/0.2093/294.1 |
| 600 | -0.0473 | [-0.0986, +0.0054] | -0.1689 | 0.2500/0.0175/461.5 | 0.2973/0.1864/305.0 |
| 900 | +0.0986 | [+0.0095, +0.1919] | -0.1409 | 0.3892/0.0506/527.8 | 0.2905/0.1915/313.3 |
| 1500 | +0.1081 | [+0.0216, +0.1946] | -0.1551 | 0.4027/0.0430/588.2 | 0.2946/0.1981/320.1 |

## 3) Compute-matched View (v3 vs hard_cap_matched)
| Budget | Δacc(v3-hcm) | Δincoh(v3-hcm) | v3_tok | hcm_tok |
|---|---:|---:|---:|---:|
| 300 | -0.0270 | -0.1032 | 151.3 | 143.5 |
| 350 | -0.0297 | -0.1545 | 225.4 | 207.6 |
| 400 | -0.0338 | -0.1848 | 283.0 | 261.7 |
| 450 | -0.0486 | -0.2217 | 324.8 | 300.6 |
| 500 | -0.0622 | -0.2219 | 364.0 | 326.6 |
| 600 | -0.0851 | -0.2042 | 461.5 | 351.0 |
| 900 | +0.0703 | -0.1927 | 527.8 | 368.3 |
| 1500 | +0.1000 | -0.2034 | 588.2 | 374.4 |

## 4) Parse Gating (B9 core budgets)
| Budget | max_parse_fail | min_parse_fail | spread | gate(max<=1%) | gate(spread<=1%p) |
|---|---:|---:|---:|---:|---:|
| 400 | 0.0000 | 0.0000 | 0.0000 | 1 | 1 |
| 450 | 0.0000 | 0.0000 | 0.0000 | 1 | 1 |
| 500 | 0.0000 | 0.0000 | 0.0000 | 1 | 1 |
| 600 | 0.0000 | 0.0000 | 0.0000 | 1 | 1 |

## 5) Dynamic-vs-Static Probe Frontier Check
- `dominated_by_probe_family=NO` across all B9 budgets in the integrated check (no static probe variant simultaneously better or equal on acc/incoh/tokens).
- However, low-budget regime(T<900) still shows strong accuracy disadvantage vs probe-only family despite incoherence gain.

| Budget | v3 acc/incoh/tok | probe_k4 acc/incoh/tok | probe_k8 acc/incoh/tok |
|---|---|---|---|
| 300 | 0.2568/0.0000/151.3 | 0.3284/0.0370/150.1 | 0.3284/0.0370/150.1 |
| 350 | 0.2568/0.0000/225.4 | 0.3743/0.0600/203.7 | 0.3743/0.0600/203.7 |
| 400 | 0.2568/0.0000/283.0 | 0.4027/0.0671/251.2 | 0.4027/0.0671/251.2 |
| 450 | 0.2568/0.0000/324.8 | 0.3959/0.0855/290.6 | 0.3959/0.0855/290.6 |
| 500 | 0.2595/0.0126/364.0 | 0.4068/0.0665/329.5 | 0.4068/0.0665/329.5 |
| 600 | 0.2500/0.0175/461.5 | 0.3986/0.0685/413.8 | 0.3986/0.0685/413.8 |
| 900 | 0.3892/0.0506/527.8 | 0.4014/0.0466/707.0 | 0.4014/0.0466/717.7 |
| 1500 | 0.4027/0.0430/588.2 | 0.4095/0.0558/1072.1 | 0.4081/0.0523/1312.9 |

## 6) Dynamic Token Allocation Evidence (B9, v3)
| Budget | Stop@Probe | ContinueSolve | ProbeShare | SolveShare | AvgProbeTok | AvgSolveTok |
|---|---:|---:|---:|---:|---:|---:|
| 300 | 0.000 | 1.000 | 0.653 | 0.000 | 98.9 | 0.0 |
| 350 | 0.000 | 1.000 | 0.768 | 0.000 | 173.1 | 0.0 |
| 400 | 0.000 | 1.000 | 0.813 | 0.003 | 230.0 | 0.7 |
| 450 | 0.000 | 1.000 | 0.833 | 0.005 | 270.7 | 1.6 |
| 500 | 0.000 | 1.000 | 0.840 | 0.018 | 305.6 | 6.5 |
| 600 | 0.000 | 1.000 | 0.845 | 0.055 | 389.8 | 25.3 |
| 900 | 0.950 | 0.050 | 0.995 | 0.000 | 525.1 | 0.0 |
| 1500 | 0.968 | 0.032 | 0.993 | 0.005 | 584.1 | 2.7 |

## 7) R7 Confirm (D9 core budgets)
| Budget | Δacc(v3-hc) | Δincoh(v3-hc) | Δacc(v3-hcm) | Δincoh(v3-hcm) |
|---|---:|---:|---:|---:|
| 400 | -0.0338 | -0.1878 | -0.0367 | -0.1985 |
| 500 | -0.0502 | -0.2020 | -0.0512 | -0.2379 |
| 600 | -0.0560 | -0.1803 | -0.0820 | -0.2158 |

## 8) 2nd Benchmark Reproduction (C9, MMLU)
| Budget | Δacc(v3-hc) | Δincoh(v3-hc) | Δacc(v3-hcm) | Δincoh(v3-hcm) |
|---|---:|---:|---:|---:|
| 400 | -0.1133 | -0.1269 | -0.1200 | -0.1269 |
| 900 | +0.3300 | -0.1396 | +0.3083 | -0.1480 |
| 1500 | +0.3583 | -0.1393 | +0.3300 | -0.1544 |

- C9 관찰: T=400에서는 v3 accuracy가 낮고, T>=900에서 큰 폭 개선으로 전환.

## 9) Conclusion
- Round9의 핵심 결론은 `regime-dependent improvement`입니다: v3는 충분한 예산(대략 T>=900)에서 hard-cap 계열 대비 강한 동시 개선을 보였습니다.
- 요청하신 공정성 요구(새 split, pre-reg, code-lock, unified accounting, parse gating)는 모두 충족했습니다.
- 다만 novelty 측면에서 low/mid budget의 accuracy drop은 남아 있으며, follow-up에서는 transition 구간(T=600~900) 정책 튜닝이 필요합니다.

## Artifacts
- `/data2/chojm/incoh-pilot/reports/round9a_tuning_splitA9_r3_v1_detailed_report.md`
- `/data2/chojm/incoh-pilot/reports/round9b_heldout_splitB9_r5_v1_detailed_report.md`
- `/data2/chojm/incoh-pilot/reports/round9d_confirm_core_r7_v1_detailed_report.md`
- `/data2/chojm/incoh-pilot/reports/round9c_mmlu_repro_r3_v1_detailed_report.md`
- `/data2/chojm/incoh-pilot/reports/round9_preregistration.md`
- `/data2/chojm/incoh-pilot/reports/round9_code_lock_manifest.sha256`
- `/data2/chojm/incoh-pilot/reports/round9_adaptive_and_matched_config.json`
