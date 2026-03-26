# Round4 Budget Run Result Report

## Run 정보
- Run ID: `round4_budget_core5_r7_v1`
- Run dir: `/data2/chojm/incoh-pilot/runs/round4_budget_core5_r7_v1`
- Dataset: `Wanfq/gpqa:gpqa_main`, `train`
- Scale: `N=400`, `R=7`
- Methods: 5 (`baseline_longcot`, `hard_cap`, `budgeted_self_consistency`, `ours_controller_v2`, `ours_controller_v2_nofallback`)
- Budgets: `[512, 768, 1024, 1536, 2048, 2560]`
- Total records: `84,000` (완료)

## 실행/품질 요약
- 전체 parse-fail: `0.28%` (235/84000)
- parse repair 시도: `1,345`건
- parse repair 성공: `1,264`건
- repair 성공률: `93.98%`
- hard fail: `0`
- identity check: 실패 없음

## 핵심 결과
### 1) feedback 핵심 검증: fallback 분리
- `ours_controller_v2`는 저예산(512/768/1024)에서 `fallback_hard_cap=100%`.
- 같은 구간에서 `ours_controller_v2_nofallback`은 fallback 없이 동작했고, incoherence가 v2/hard_cap 대비 더 낮음.

### 2) nofallback vs hard_cap
- 모든 budget에서 `ours_controller_v2_nofallback`의 incoherence가 `hard_cap`보다 낮음.
- 정확도도 전 budget에서 `hard_cap`보다 높거나 동일 수준.

### 3) nofallback vs budgeted_self_consistency
- incoherence 기준:
  - nofallback 우세: `512, 1024, 2048, 2560`
  - self-consistency 우세: `768, 1536`
- accuracy 기준:
  - self-consistency가 전반적으로 소폭 우세(특히 768 이상).
- 해석: nofallback은 안정성(incoherence) 축에서 강하고, self-consistency는 정확도 축에서 강함.

### 4) regime 관찰
- 1536+에서 `ours_controller_v2`와 `nofallback`이 사실상 동일(둘 다 fallback 미사용, stop-after-probe 중심).
- 즉, 고예산 구간은 controller 본체 효과 구간으로 볼 수 있음.

## budget별 핵심 수치 (요약)
- B=512: baseline incoh `0.0849`, nofallback `0.0556`
- B=768: baseline incoh `0.0790`, nofallback `0.0546`
- B=1024: baseline incoh `0.0844`, nofallback `0.0454`
- B=1536: baseline incoh `0.0999`, nofallback `0.0588`
- B=2048: baseline incoh `0.0921`, nofallback `0.0493`
- B=2560: baseline incoh `0.0838`, nofallback `0.0434`

## 결론
- Round3 피드백 중 가장 중요한 지적(“저예산은 fallback 성능 아니냐?”)에 대해, Round4는 `nofallback`을 포함해 controller 본체 기여를 분리 검증함.
- controller 본체는 hard_cap 대비 일관된 incoherence 개선을 보임.
- 다만 accuracy 축은 self-consistency가 여전히 경쟁력이 있어, 최종 claim은 Pareto 관점(정확도-비용-incoherence)으로 정리하는 것이 타당.

## 산출물
- 분석 요약: `/data2/chojm/incoh-pilot/runs/round4_budget_core5_r7_v1/round2_summary.md`
- 분석 JSON: `/data2/chojm/incoh-pilot/runs/round4_budget_core5_r7_v1/analysis_summary_round2.json`
- 본 보고서: `/data2/chojm/incoh-pilot/reports/round4_budget_result_report.md`
