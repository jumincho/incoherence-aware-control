# Round4 Spend Sweep Follow-up Report

## 1) 실험 개요
- Run ID: `round4_spend_core6_r5_v1`
- Run dir: `/data2/chojm/incoh-pilot/runs/round4_spend_core6_r5_v1`
- 목적: 동일 total-token 조건에서 `nofallback controller`의 위치를 hard_cap / budgeted_self_consistency / probe-only 대비 비교하고, 임계 구간(phase transition)을 확인.
- 데이터: `Wanfq/gpqa:gpqa_main/train`, 고정 샘플 `N=400`
- 반복: `R=5` (`seed=[11,22,33,44,55]`)
- 방법: 6개
  - `baseline_longcot`
  - `hard_cap`
  - `budgeted_self_consistency`
  - `ours_controller_v2`
  - `ours_controller_v2_nofallback`
  - `probe_only_fixedk`
- spend targets: `T={200,300,450,600,750,900,1200,1500}`
- 총 레코드: `96,000` (완주)

## 2) 피드백 반영 사항 (실행 전 조치)
- fallback 동치성 수정
  - v2 fallback 경로의 seed offset 제거
  - hard_cap과 동일 seed/경로 보장
- stop-after-probe formatter 강제
  - 최종 응답을 코드에서 `Final Answer: X` 형식으로 고정
- parse repair 단답형 강화
  - repair prompt를 `A/B/C/D 한 글자` 전용으로 변경
  - parser single-letter 파싱 지원 추가
- 정적 비교 baseline 추가
  - `probe_only_fixedk` 추가로 동적 제어 기여 분리

## 3) 실행 신뢰성
- 완주: `96,000 / 96,000`
- hard fail: `0`
- 최종 parse fail: `1,091` (`1.1365%`)
- repair 시도/성공: `13,036 / 12,953` (성공률 `99.36%`)
- bias-variance identity: failure 없음
- 총 소요: `666.8분`

## 4) 핵심 결과
### 4.1 Low-spend 구간(T=200,300)
- `ours_controller_v2_nofallback`은 실패 구간
  - T=200: acc `0.2880`, incoh `0.0221`
  - T=300: acc `0.3175`, incoh `0.0489`
- hard_cap / v2(fallback)는 이 구간에서 더 안정적
- 해석: 저예산에서는 controller 본체의 overhead/분기 비용이 손해를 유발

### 4.2 전환 시작 구간(T=450)
- nofallback가 hard_cap 대비 개선 시작
  - Δincoh(nf-hc) `-0.0018`, Δacc(nf-hc) `+0.0070`
- nofallback가 budgeted_sc 대비도 incoh 우세
  - Δincoh(nf-sc) `-0.0163`, Δacc(nf-sc) `-0.0050`
- phase threshold(실무 판정): `T≈450`

### 4.3 Mid/High-spend 구간(T>=600)
- nofallback vs hard_cap: 대부분 구간에서 일관 우세
  - incoh 개선 + acc 개선 동시 달성(600/900/1200/1500)
- nofallback vs budgeted_sc:
  - 정확도는 보통 소폭 열세
  - incoh는 구간별 혼재 (우세: 600/1200, 열세: 750/900/1500)
- budgeted_sc는 정확도 상위권이지만 cost가 큼
  - 예: T=1500에서 avg total tok `1392.5`

### 4.4 probe_only_fixedk 비교
- `probe_only_fixedk`가 일부 구간에서 매우 낮은 incoh를 보여 동적 정책과 경쟁
  - 예: T=1200 incoh `0.0419` (nofallback `0.0450`)
  - 예: T=1500 incoh `0.0428` (nofallback `0.0516`)
- 해석: 현재 controller는 stop-after-probe 비중이 높아 “동적 제어 이득”이 충분히 분리되지 않음

## 5) controller 동작 분석
- `ours_controller_v2`
  - T<=900: fallback 100%
  - T>=1200: fallback 0%, stop-after-probe 약 96.9%
- `ours_controller_v2_nofallback`
  - T<=300: continue-solve 100%
  - T>=450: stop-after-probe 91.5~96.9%
- 결론: 이번 spend 실험에서도 controller 본체는 사실상 “probe-driven gate”로 동작

## 6) 예측 신호 분석 (probe disagreement)
- AUC(probe_disagree -> baseline_error): `~0.50~0.52` (약함)
- AUC(probe_disagree -> baseline_disagreement>0):
  - T=450: `0.593`
  - T=600: `0.660`
  - T=1200: `0.706`
  - T=1500: `0.696`
- 해석: 정답/오답 직접 예측보다는 “불안정성(disagreement) 탐지” 신호로 유의미

## 7) 이번 라운드 결론
- 피드백 핵심(동치성/포맷/repair/정적 baseline 추가)은 기술적으로 수용 완료.
- 실험적으로는 명확한 regime map이 확인됨:
  - Low spend(200/300): nofallback 열세
  - Transition(~450): nofallback 개선 시작
  - Mid/High spend: nofallback는 hard_cap 대비 우세, budgeted_sc와는 정확도-일관성 트레이드오프
- 즉, 주장은 “항상 우월”이 아니라 “compute 구간별 Pareto 위치가 다르다”로 정리하는 것이 타당.

## 8) 후속 실험 제안 (즉시 실행 가능)
1. pseudo held-out 검증
- 현재 400문항을 A/B로 분할
- A에서 threshold/파라미터 선택, B에서 최종 평가

2. controller 동적성 강화 ablation
- stop-after-probe 상한 도입(예: max 80%)
- continue-solve를 강제하는 조건부 policy 비교
- probe_only_fixedk 대비 동적 정책의 순이득 분리

3. calibration 분석 추가
- probe disagreement를 decile binning 후
- bin별 실제 baseline disagreement/error 곡선 작성
- threshold 선택 근거를 데이터로 고정

## 9) 산출물 경로
- 분석 요약: `/data2/chojm/incoh-pilot/runs/round4_spend_core6_r5_v1/round2_summary.md`
- 분석 JSON: `/data2/chojm/incoh-pilot/runs/round4_spend_core6_r5_v1/analysis_summary_round2.json`
- 자동 상세 리포트: `/data2/chojm/incoh-pilot/reports/round4_spend_core6_r5_v1_detailed_report.md`
- 본 리포트: `/data2/chojm/incoh-pilot/reports/round4_spend_followup_experiment_report.md`
