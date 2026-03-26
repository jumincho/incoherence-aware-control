# Round4 Budget Core5 Detailed Report

## 1) 실험 목적
- Round3 피드백 반영 검증:
  - `fallback` 성능과 controller 본체 성능 분리
  - `relative incoherence 개선율` 정의 고정
  - parse-fail 보정(`P1R`)이 실제로 안정화에 기여하는지 확인
  - compute-scaling baseline(`budgeted_self_consistency`) 대비 위치 확인

## 2) 피드백 반영 구현 변경
- 분석 정의 고정: `rel_improve = (incoh_base - incoh_method) / incoh_base` (primary).
- doc-bootstrap 기반 상대개선율은 보조지표로 별도 병기 (`Incoh Red Rel (DocBoot)`).
- 실행기 parse repair 추가: parse 실패 시 budget 여유가 있으면 1회 repair 호출.
- controller diagnostics 확장: fallback율, stop-after-probe율, probe/solve token share 포함.
- 핵심 비교군 확장: `ours_controller_v2_nofallback` 포함.

## 3) 실험 설정
| 항목 | 값 |
|---|---|
| Run ID | `round4_budget_core5_r7_v1` |
| Dataset | `400 sampled` from `Wanfq/gpqa:gpqa_main/train` |
| N | `400` |
| R (trial seeds) | `7` ([11, 22, 33, 44, 55, 66, 77]) |
| Budgets (total tokens) | `[512, 768, 1024, 1536, 2048, 2560]` |
| Methods | `['baseline_longcot', 'hard_cap', 'budgeted_self_consistency', 'ours_controller_v2', 'ours_controller_v2_nofallback']` |
| Parse policy | `P1R` (P1 + repair) |
| Expected records | `84000` |
| Shards | `8` GPUs |

## 4) 실행 품질/신뢰성
| 지표 | 값 |
|---|---:|
| Start (UTC) | 2026-02-26 08:32:49 |
| End (UTC) | 2026-02-27 01:20:26 |
| Duration (min) | 1007.62 |
| Completed records | 84000 / 84000 |
| Hard fail | 0 |
| Parse fail | 235 (0.2798%) |
| Parse repair attempted | 1345 |
| Parse repair success | 1264 (93.9777%) |
| Bias-Variance identity check | pass (failure dump none) |

## 5) Budget별 성능 요약
### Budget 512
| Method | Acc | Incoh | Bias | Var | Avg total tok | ParseFail |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.3804 | 0.0849 | 0.6275 | 0.0582 | 388.7 | 0.003 |
| hard_cap | 0.3707 | 0.0689 | 0.6275 | 0.0464 | 259.2 | 0.000 |
| budgeted_self_consistency | 0.3839 | 0.0783 | 0.6225 | 0.0529 | 409.8 | 0.003 |
| ours_controller_v2 | 0.3711 | 0.0652 | 0.6300 | 0.0439 | 259.1 | 0.000 |
| ours_controller_v2_nofallback | 0.3775 | 0.0556 | 0.6175 | 0.0363 | 370.0 | 0.021 |

| Method(vs baseline) | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ mean | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.0160 | 0.189 | 0.239 | -0.0096 | [-0.0254, 0.0054] | PASS |
| budgeted_self_consistency | 0.0066 | 0.078 | 0.115 | 0.0036 | [-0.0129, 0.0204] | FAIL |
| ours_controller_v2 | 0.0197 | 0.232 | 0.316 | -0.0093 | [-0.0250, 0.0064] | PASS |
| ours_controller_v2_nofallback | 0.0293 | 0.345 | 0.252 | -0.0029 | [-0.0189, 0.0146] | PASS |

| Controller | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg probe tok | Avg solve tok | Decision counts |
|---|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2 | 100.0% | 0.0% | 0.0% | 99.2% | 0.0 | 257.0 | `{'fallback_hard_cap': 2800}` |
| ours_controller_v2_nofallback | 0.0% | 92.7% | 99.1% | 0.0% | 366.8 | 0.0 | `{'stop_after_probe': 2595, 'continue_solve': 205}` |

### Budget 768
| Method | Acc | Incoh | Bias | Var | Avg total tok | ParseFail |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.3889 | 0.0790 | 0.6075 | 0.0521 | 424.0 | 0.000 |
| hard_cap | 0.3761 | 0.0556 | 0.6250 | 0.0368 | 271.1 | 0.000 |
| budgeted_self_consistency | 0.3989 | 0.0550 | 0.5950 | 0.0346 | 661.1 | 0.001 |
| ours_controller_v2 | 0.3779 | 0.0636 | 0.6150 | 0.0418 | 271.2 | 0.000 |
| ours_controller_v2_nofallback | 0.3793 | 0.0546 | 0.6250 | 0.0361 | 502.7 | 0.019 |

| Method(vs baseline) | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ mean | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.0235 | 0.297 | 0.412 | -0.0129 | [-0.0279, 0.0011] | PASS |
| budgeted_self_consistency | 0.0240 | 0.304 | 0.235 | 0.0100 | [-0.0061, 0.0272] | PASS |
| ours_controller_v2 | 0.0154 | 0.195 | 0.226 | -0.0111 | [-0.0275, 0.0054] | PASS |
| ours_controller_v2_nofallback | 0.0245 | 0.310 | 0.539 | -0.0096 | [-0.0268, 0.0071] | PASS |

| Controller | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg probe tok | Avg solve tok | Decision counts |
|---|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2 | 100.0% | 0.0% | 0.0% | 99.7% | 0.0 | 270.4 | `{'fallback_hard_cap': 2800}` |
| ours_controller_v2_nofallback | 0.0% | 92.8% | 99.3% | 0.0% | 499.4 | 0.1 | `{'stop_after_probe': 2599, 'continue_solve': 201}` |

### Budget 1024
| Method | Acc | Incoh | Bias | Var | Avg total tok | ParseFail |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.3896 | 0.0844 | 0.6125 | 0.0564 | 432.3 | 0.000 |
| hard_cap | 0.3771 | 0.0654 | 0.6275 | 0.0439 | 275.2 | 0.000 |
| budgeted_self_consistency | 0.3954 | 0.0567 | 0.6125 | 0.0368 | 915.8 | 0.001 |
| ours_controller_v2 | 0.3775 | 0.0699 | 0.6225 | 0.0468 | 275.4 | 0.000 |
| ours_controller_v2_nofallback | 0.3832 | 0.0454 | 0.6175 | 0.0294 | 553.3 | 0.007 |

| Method(vs baseline) | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ mean | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.0189 | 0.224 | 0.158 | -0.0125 | [-0.0272, 0.0021] | PASS |
| budgeted_self_consistency | 0.0277 | 0.328 | 0.241 | 0.0057 | [-0.0107, 0.0214] | PASS |
| ours_controller_v2 | 0.0145 | 0.171 | 0.069 | -0.0121 | [-0.0279, 0.0029] | PASS |
| ours_controller_v2_nofallback | 0.0389 | 0.462 | 0.413 | -0.0064 | [-0.0225, 0.0097] | PASS |

| Controller | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg probe tok | Avg solve tok | Decision counts |
|---|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2 | 100.0% | 0.0% | 0.0% | 99.8% | 0.0 | 274.9 | `{'fallback_hard_cap': 2800}` |
| ours_controller_v2_nofallback | 0.0% | 94.5% | 99.2% | 0.3% | 548.9 | 1.9 | `{'stop_after_probe': 2646, 'continue_solve': 154}` |

### Budget 1536
| Method | Acc | Incoh | Bias | Var | Avg total tok | ParseFail |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.3904 | 0.0999 | 0.6050 | 0.0671 | 438.8 | 0.000 |
| hard_cap | 0.3807 | 0.0717 | 0.6150 | 0.0475 | 280.5 | 0.000 |
| budgeted_self_consistency | 0.3932 | 0.0488 | 0.6050 | 0.0311 | 1422.9 | 0.000 |
| ours_controller_v2 | 0.3907 | 0.0588 | 0.6050 | 0.0378 | 597.6 | 0.006 |
| ours_controller_v2_nofallback | 0.3907 | 0.0588 | 0.6050 | 0.0378 | 597.6 | 0.006 |

| Method(vs baseline) | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ mean | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.0282 | 0.282 | 0.369 | -0.0096 | [-0.0236, 0.0043] | PASS |
| budgeted_self_consistency | 0.0510 | 0.511 | 0.579 | 0.0029 | [-0.0139, 0.0193] | PASS |
| ours_controller_v2 | 0.0411 | 0.412 | 0.453 | 0.0004 | [-0.0161, 0.0179] | PASS |
| ours_controller_v2_nofallback | 0.0411 | 0.412 | 0.453 | 0.0004 | [-0.0161, 0.0179] | PASS |

| Controller | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg probe tok | Avg solve tok | Decision counts |
|---|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2 | 0.0% | 96.6% | 98.3% | 1.6% | 587.4 | 9.6 | `{'stop_after_probe': 2704, 'continue_solve': 96}` |
| ours_controller_v2_nofallback | 0.0% | 96.6% | 98.3% | 1.6% | 587.4 | 9.6 | `{'stop_after_probe': 2704, 'continue_solve': 96}` |

### Budget 2048
| Method | Acc | Incoh | Bias | Var | Avg total tok | ParseFail |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.3893 | 0.0921 | 0.6200 | 0.0629 | 439.3 | 0.000 |
| hard_cap | 0.3818 | 0.0662 | 0.6200 | 0.0439 | 280.3 | 0.000 |
| budgeted_self_consistency | 0.3989 | 0.0514 | 0.6000 | 0.0325 | 1934.6 | 0.000 |
| ours_controller_v2 | 0.3882 | 0.0493 | 0.6075 | 0.0315 | 606.5 | 0.005 |
| ours_controller_v2_nofallback | 0.3882 | 0.0493 | 0.6075 | 0.0315 | 606.5 | 0.005 |

| Method(vs baseline) | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ mean | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.0259 | 0.281 | 0.203 | -0.0075 | [-0.0236, 0.0075] | PASS |
| budgeted_self_consistency | 0.0407 | 0.442 | 0.307 | 0.0096 | [-0.0071, 0.0286] | PASS |
| ours_controller_v2 | 0.0427 | 0.464 | 0.388 | -0.0011 | [-0.0182, 0.0161] | PASS |
| ours_controller_v2_nofallback | 0.0427 | 0.464 | 0.388 | -0.0011 | [-0.0182, 0.0161] | PASS |

| Controller | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg probe tok | Avg solve tok | Decision counts |
|---|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2 | 0.0% | 96.9% | 97.6% | 2.1% | 591.7 | 12.5 | `{'stop_after_probe': 2714, 'continue_solve': 86}` |
| ours_controller_v2_nofallback | 0.0% | 96.9% | 97.6% | 2.1% | 591.7 | 12.5 | `{'stop_after_probe': 2714, 'continue_solve': 86}` |

### Budget 2560
| Method | Acc | Incoh | Bias | Var | Avg total tok | ParseFail |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.3907 | 0.0838 | 0.6050 | 0.0554 | 440.5 | 0.000 |
| hard_cap | 0.3811 | 0.0687 | 0.6150 | 0.0454 | 280.4 | 0.000 |
| budgeted_self_consistency | 0.3989 | 0.0467 | 0.5975 | 0.0293 | 2449.2 | 0.000 |
| ours_controller_v2 | 0.3871 | 0.0434 | 0.6100 | 0.0277 | 613.2 | 0.004 |
| ours_controller_v2_nofallback | 0.3871 | 0.0434 | 0.6100 | 0.0277 | 613.2 | 0.004 |

| Method(vs baseline) | Incoh Red Abs | Incoh Red Rel | Incoh Red Rel (DocBoot) | Acc Δ mean | Acc 95% CI | Verdict |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap | 0.0151 | 0.181 | 0.209 | -0.0096 | [-0.0236, 0.0043] | PASS |
| budgeted_self_consistency | 0.0371 | 0.443 | 0.532 | 0.0082 | [-0.0082, 0.0250] | PASS |
| ours_controller_v2 | 0.0404 | 0.482 | 0.594 | -0.0036 | [-0.0200, 0.0125] | PASS |
| ours_controller_v2_nofallback | 0.0404 | 0.482 | 0.594 | -0.0036 | [-0.0200, 0.0125] | PASS |

| Controller | Fallback% | Stop@Probe% | ProbeShare% | SolveShare% | Avg probe tok | Avg solve tok | Decision counts |
|---|---:|---:|---:|---:|---:|---:|---|
| ours_controller_v2 | 0.0% | 96.9% | 97.0% | 2.1% | 595.0 | 12.9 | `{'stop_after_probe': 2713, 'continue_solve': 87}` |
| ours_controller_v2_nofallback | 0.0% | 96.9% | 97.0% | 2.1% | 595.0 | 12.9 | `{'stop_after_probe': 2713, 'continue_solve': 87}` |

## 6) nofallback 기준 추가 비교 (feedback 핵심)
| Budget | nofallback vs hard_cap (Δincoh) | nofallback vs hard_cap (Δacc) | nofallback vs budgeted_sc (Δincoh) | nofallback vs budgeted_sc (Δacc) |
|---|---:|---:|---:|---:|
| 512 | -0.0133 | +0.0068 | -0.0227 | -0.0064 |
| 768 | -0.0010 | +0.0032 | -0.0005 | -0.0196 |
| 1024 | -0.0200 | +0.0061 | -0.0112 | -0.0121 |
| 1536 | -0.0129 | +0.0100 | +0.0099 | -0.0025 |
| 2048 | -0.0168 | +0.0064 | -0.0021 | -0.0107 |
| 2560 | -0.0253 | +0.0061 | -0.0033 | -0.0118 |

## 7) 핵심 관찰
1. `ours_controller_v2` 저예산(512/768/1024)은 fallback 100%로 동작해, 해당 구간은 사실상 hard-cap 계열 정책 성능입니다.
2. `ours_controller_v2_nofallback`은 전 budget에서 hard_cap 대비 incoherence가 낮고 정확도도 동일/우세입니다.
3. `budgeted_self_consistency`는 정확도 축에서 강하지만 token 사용량이 매우 큽니다 (고예산에서 거의 budget 소진).
4. 1536+ 구간에서는 `v2 == nofallback` (fallback 미사용)으로 controller 본체 성능 구간으로 해석 가능합니다.
5. parse repair가 높은 성공률(93.98%)로 parse-fail 리스크를 실질 완화했습니다.

## 8) 리스크/한계
- 현재 budget run은 `gpqa_main/train` 기반이며 held-out 검증은 별도 라운드에서 필요합니다.
- `stop_after_probe` 비율이 매우 높아, probe signal의 예측력/캘리브레이션 분석을 Spend run과 함께 추가 제시해야 합니다.
- nofallback은 저예산에서 parse-fail이 상대적으로 높아(P1R 포함) 포맷 강제 프롬프트 추가 개선 여지가 있습니다.

## 9) 다음 라운드 즉시 실행 권고
- 동일 방법군으로 spend sweep (`T={200,300,450,600,750,900,1200,1500}`) 실행.
- 동일 report 템플릿으로 임계점(phase transition) 지도 작성.
- budget+spend 통합 Pareto(Acc-Incoh-Token) 그림과 nofallback 중심 메시지 정리.

## 10) 산출물 경로
- Run dir: `/data2/chojm/incoh-pilot/runs/round4_budget_core5_r7_v1`
- Summary md: `/data2/chojm/incoh-pilot/runs/round4_budget_core5_r7_v1/round2_summary.md`
- Analysis json: `/data2/chojm/incoh-pilot/runs/round4_budget_core5_r7_v1/analysis_summary_round2.json`
- This report: `/data2/chojm/incoh-pilot/reports/round4_budget_detailed_report.md`
