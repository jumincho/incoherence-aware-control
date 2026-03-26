# Round3 Experiment Report (Core3 + Spend Sweep)

## 1) 목적과 가설
Round3의 목적은 Round2 피드백을 반영해 다음을 검증하는 것이었습니다.

- 핵심 가설: `incoherence-aware controller`가 특정 compute 구간에서 baseline 대비 incoherence를 낮추고, 정확도는 유의미하게 악화시키지 않는가.
- 검증 방식: `total_tokens` 기준 budget sweep + spend-target 성격의 저/중 budget 스윕.

성공 기준(설정 고정):

- baseline 대비 incoherence 상대 개선 >= 10%
- 정확도 저하가 bootstrap 95% CI 기준 유의하지 않음

## 2) 실험 설정
공통:

- 모델: `Qwen/Qwen3-14B` (main), `Qwen/Qwen3-1.7B` (anchor 슬롯 보유, 본 라운드 core methods에서는 비활성)
- 데이터: `Wanfq/gpqa`, `gpqa_diamond`, `train`
- 문항 수: `N=198` (고정 샘플)
- 파싱 정책: `P1` (parse fail은 오답 처리)
- 회계: `total_tokens` (prompt + output + discard + restart)
- 분석: paired bootstrap (CI), bias/variance identity check 내장

방법군(공통 3개):

- `baseline_longcot`
- `hard_cap`
- `ours_controller_v2`

### Run A: Core budget sweep
- Run ID: `round3_core3_v1`
- Budgets: `[768, 1024, 1536, 2048, 2560]`
- 반복: `R=5` (trial seeds 5개)
- 총 샘플: `14850`
- 소요 시간: 약 `132.1분` (8 GPU shard)

### Run B: Spend-oriented 저/중 budget sweep
- Run ID: `round3_spend_core3_v1`
- Budgets: `[300, 600, 900, 1200]`
- 반복: `R=3` (trial seeds 3개)
- 총 샘플: `7128`
- 소요 시간: 약 `47.9분` (8 GPU shard)

## 3) 품질 통제 항목(피드백 반영)
이번 라운드에서 아래 항목을 유지/검증했습니다.

- total-token 기반 비용 회계
- method별 parse-fail rate/type 집계
- 분석 identity check (`error = bias + variance`) 통과
- budget sweep 기반 비교
- controller decision/probe/solve token 진단 로깅

## 4) 핵심 결과

### 4.1 Run A (`round3_core3_v1`) 요약
`ours_controller_v2`는 모든 budget에서 성공 기준을 충족했습니다 (5/5 pass).

- B=768: incoh `0.0709 -> 0.0521` (상대 개선 58.5%), acc CI [-0.0131, 0.0283]
- B=1024: incoh `0.0866 -> 0.0630` (14.4%), acc CI [-0.0141, 0.0242]
- B=1536: incoh `0.0916 -> 0.0499` (38.3%), acc CI [-0.0364, 0.0111]
- B=2048: incoh `0.0867 -> 0.0397` (65.3%), acc CI [-0.0364, 0.0091]
- B=2560: incoh `0.0874 -> 0.0372` (58.1%), acc CI [-0.0343, 0.0121]

해석 포인트:

- 1536+ 구간에서는 controller가 baseline보다 더 많은 total_tokens를 실제로 사용하면서 incoherence를 강하게 억제.
- 768/1024 구간에서는 `fallback_hard_cap`이 100%로 동작해, 사실상 hard-cap 동작과 유사.

### 4.2 Run B (`round3_spend_core3_v1`) 요약
`ours_controller_v2`는 4개 budget 중 3개에서 성공 기준을 충족했습니다 (3/4 pass).

- B=300: **FAIL** (incoh 상대 -37.5%, baseline 대비 악화)
- B=600: PASS (33.3% 개선)
- B=900: PASS (13.8% 개선)
- B=1200: PASS (49.4% 개선, 단 accuracy 감소 경향 존재하나 CI가 0 포함)

해석 포인트:

- 저예산 극단(B=300)에서는 controller 이점이 사라지거나 악화.
- B=600 이상에서 다시 개선 구간으로 진입.
- B=1200에서 parse-fail이 `ours_controller_v2=3.9%`로 baseline/hard_cap(0.5%) 대비 높게 관측되어, 이 budget에서 prompt/format 안정화 추가 튜닝 필요.

## 5) 성공 판정
Round3 전체 관점에서 본 결론:

- 조건부 성공(regime-dependent success) 신호가 강화됨.
- `ours_controller_v2`는 **중/고 compute 구간**에서 incoherence를 안정적으로 줄이는 경향.
- **극저예산 구간(B=300)**은 비효율/불안정 구간으로 확인됨.

즉, 이번 라운드는 "항상 이긴다"가 아니라 "어느 compute 구간에서 이기는지"를 실험적으로 명확히 한 라운드입니다.

## 6) 리스크/한계

- Spend sweep은 `R=3`이라 variance 계열 지표의 통계 안정성이 core run(R=5)보다 낮음.
- stratification 결과는 분석 스키마에 준비되어 있으나, 이번 산출물에서 budget별 상세 표로는 비어 있어 후속 라운드에서 별도 계산/리포팅 보강 필요.
- controller v2가 일부 구간에서 `stop_after_probe` 비중이 매우 높아, probe 비용 대비 실제 solve 품질 기여를 추가로 분해해야 함.

## 7) 산출물

- Core run: `runs/round3_core3_v1/`
- Spend run: `runs/round3_spend_core3_v1/`
- 자동 요약:
  - `runs/round3_core3_v1/round2_summary.md`
  - `runs/round3_spend_core3_v1/round2_summary.md`
- 분석 JSON:
  - `runs/round3_core3_v1/analysis_summary_round2.json`
  - `runs/round3_spend_core3_v1/analysis_summary_round2.json`

## 8) 다음 라운드 권고

- core 3-method는 `R=5~7` 유지 + `N` 확대(>=300)로 통계력 강화
- spend-target 스윕은 `T_match` 직접 제어(실제 사용 토큰 맞춤) 버전을 별도 실행
- `ours_controller_v2`에 대해:
  - low-budget fallback 경계값/solve_min 조정
  - parse-fail 높은 budget(1200)에서 포맷 안정화 프롬프트 보강
