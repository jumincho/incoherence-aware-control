# Round 1 실험 보고서

## 1) 실험 목적
본 실험의 핵심 목적은 아래 질문에 답하는 것입니다.

- **동일 token cost 조건**에서, 제안한 확장 방법(`ours_controller`, `ours_full`)이 기존 방법보다 **incoherence(variance/error)**를 더 낮출 수 있는가?
- incoherence를 낮추는 과정에서 정확도(accuracy)가 유의미하게 악화되지 않는가?

Hot-Mess 문제의식(추론/행동 길이 증가 시 변동성 누적)을 직접 겨냥해, 단순 정확도 개선이 아닌 **오류 성질(bias vs variance)** 개선 여부를 검증했습니다.

---

## 2) 실험 설계

### 2.1 실험 환경
- 코드 루트: `/data2/chojm/incoh-pilot`
- GPU: NVIDIA RTX A6000 x 8
- Python: 3.11, venv 사용
- 모델:
  - Main: `Qwen/Qwen3-14B`
  - Anchor: `Qwen/Qwen3-1.7B`
- 데이터:
  - `Wanfq/gpqa`, config `gpqa_main`, split `train`
  - 문제 수 `N=96` (고정 seed 샘플링)
- 반복 실행:
  - trial seeds = `[11,22,33,44,55]` (문항당 5회)
- 총 평가 샘플 수:
  - `96 x 5 x 6 methods = 2880`

### 2.2 방법군(6조건)
1. `baseline_longcot`
2. `hard_cap`
3. `self_consistency`
4. `confidence_select`
5. `ours_controller`
6. `ours_full`

### 2.3 비용 공정성(핵심)
- 문항당 output token 예산: `B=768`
- 버려진 샘플(discard), 재시작(restart), anchor 생성 토큰까지 누적 회계
- 즉, 방법별 토큰 사용 방식이 달라도 **총 예산은 동일 규칙으로 제한**

### 2.4 평가 지표
- Accuracy
- Bias, Variance
- Incoherence = Variance / (Bias + Variance)
- Intra flip / Inter disagreement
- 평균 output token
- Baseline 대비 paired bootstrap (95% CI, p-value)

---

## 3) 구현 및 디버깅 이력

### 3.1 초기 구현 파일
- 오케스트레이터: `src/run_pilot.py`
- 방법 정책: `src/methods.py`
- 파서: `src/parser.py`
- 토큰 회계: `src/token_meter.py`
- 모니터: `src/monitor.py`
- 분석: `src/analyze_hotmess_style.py`
- 설정: `configs/pilot_gpqa.yaml`

### 3.2 실행 중 확인된 이슈와 조치
1. **라이브러리 호환 이슈**
- 문제: `transformers 5.x`가 현재 torch(2.3.0)와 충돌
- 조치: `transformers<5`, `datasets<3`, `huggingface_hub<1`로 고정

2. **Qwen3 추론 형식 이슈(`<think>` 장문 루프)**
- 문제: 최종 답안 미출력/파싱 실패
- 조치: chat template에 `enable_thinking=False` 적용

3. **generate 인자 이슈**
- 문제: `generator` 인자 미사용 에러로 샘플 실패
- 조치: `generator` 제거, `torch.manual_seed`로 시드 고정

4. **self_consistency 파싱 실패율 상승(중간 라운드)**
- 문제: 장문 응답으로 최종 포맷 미준수
- 조치: 프롬프트를 3줄 요약 형식으로 강화, per-sample max tokens 축소(192/176 -> 112)

---

## 4) 라운드별 진행 요약

### 4.1 드라이런
- `dryrun_qwen3*`에서 모델 로딩/생성/로그 포맷 검증
- 주요 버그(의존성, generate 인자, thinking mode) 확인 및 수정

### 4.2 스모크 라운드
- `smoke_v1`: 파싱 실패율이 높아 중단(규칙 준수)
- `smoke_v2`: 수정 반영 후 재실행, 파싱 실패율 0%로 안정화

### 4.3 본실험 라운드 (`pilot_full_v1`)
- 8개 shard 병렬 실행 완료
- shard별 완료: 360건씩 총 2880건
- shard 파싱 실패 합계: 43건 (1.49%)
- hard_fail: 0
- 시작: `2026-02-25T08:24:44Z` (`run_meta`)
- 마지막 shard 완료: `2026-02-25T09:11:39Z` (`status_shard2`)

---

## 5) 최종 결과 (Round 1)

## 5.1 방법별 절대 지표

| Method | Accuracy | Bias | Variance | Incoherence | Avg Out Tokens | Inter Disagreement |
|---|---:|---:|---:|---:|---:|---:|
| baseline_longcot | 0.3937 | 0.5833 | 0.1484 | 0.2028 | 159.79 | 0.1458 |
| hard_cap | 0.3854 | 0.6146 | 0.0458 | 0.0694 | 20.86 | 0.0458 |
| self_consistency | 0.4000 | 0.5938 | 0.0271 | 0.0436 | 272.70 | 0.0271 |
| confidence_select | 0.3521 | 0.6562 | 0.0641 | 0.0889 | 152.04 | 0.0625 |
| **ours_controller** | **0.4042** | 0.5938 | 0.0437 | **0.0686** | 53.53 | 0.0446 |
| ours_full | 0.3458 | 0.6250 | 0.1281 | 0.1701 | 197.71 | 0.1450 |

## 5.2 Baseline 대비 통계 비교

| Method | Incoh Reduction vs Baseline | Incoh Δ 95% CI (other-base) | Acc Δ (other-base) | Acc Δ 95% CI | p(incoh) | p(acc) |
|---|---:|---:|---:|---:|---:|---:|
| hard_cap | +0.1705 | [-0.2492, -0.0967] | -0.0083 | [-0.0792, 0.0667] | 0.000 | 0.821 |
| self_consistency | +0.1837 | [-0.2626, -0.1119] | +0.0063 | [-0.0708, 0.0855] | 0.000 | 0.895 |
| confidence_select | +0.1553 | [-0.2330, -0.0833] | -0.0417 | [-0.1042, 0.0188] | 0.000 | 0.179 |
| **ours_controller** | **+0.1620** | **[-0.2410, -0.0876]** | **+0.0104** | **[-0.0646, 0.0896]** | **0.000** | **0.777** |
| ours_full | +0.0074 | [-0.1069, 0.0915] | -0.0479 | [-0.1271, 0.0334] | 0.856 | 0.253 |

---

## 6) 성공 판정

### 6.1 사전 성공 기준
- baseline 대비 incoherence 감소
- accuracy 유의미한 하락 없음

### 6.2 판정 결과
- **성공:** `ours_controller`
  - incoherence 유의하게 감소
  - accuracy 유의한 하락 없음(오히려 평균 +0.0104)
- **실패:** `ours_full`
  - incoherence 개선 거의 없음(+0.0074 수준)
  - accuracy도 baseline 대비 낮은 평균

---

## 7) 아이디어 3종 관점 해석

1. 아이디어1(적응형 예산/중단·재시작):
- `ours_controller`가 실질 성과를 보여 **유효성 확인**

2. 아이디어2(분해 + 제약 누적):
- `ours_full` 내부 구조로 반영했으나, 현재 프롬프트/예산 배분에서는 기대만큼 효율적이지 않음

3. 아이디어3(작은 모델 앵커):
- `ours_full`에서 1.7B 체크리스트 앵커를 사용했으나 본 라운드에서는 비용 대비 성능 이득 미확인

---

## 8) 한계 및 리스크
- `ours_full`의 토큰 사용량이 높은 편(197.71)으로 비용 효율 열위
- parse_fail 1.49%는 허용 범위였지만, 특정 shard/method 편향 분석 필요
- 현재 성공 기준은 절대 감소량 기준에 가까워, 다음 라운드에서는 상대 감소율 기준도 병행 명시 권장

---

## 9) 다음 라운드 제안
1. `ours_controller` 중심 확장
- threshold, probe 길이, restart 정책 grid 탐색
- 동일 cost 하에서 accuracy-incoherence Pareto 전면 비교

2. `ours_full` 축소/재설계
- anchor 길이 제한 강화
- checklist 강제 방식을 soft constraint -> hard constraint로 나눠 ablation
- 분해 단계 수 최소화

3. 평가 강화
- relative incoherence reduction 지표 병기
- parse_fail 원인 분해(문항/방법/seed)

---

## 10) 산출물 경로
- 최종 런: `/data2/chojm/incoh-pilot/runs/pilot_full_v1`
- 최종 분석 JSON: `/data2/chojm/incoh-pilot/runs/pilot_full_v1/analysis_summary.json`
- 최종 요약 MD: `/data2/chojm/incoh-pilot/runs/pilot_full_v1/pilot_summary.md`
- 스모크 참조 런: `/data2/chojm/incoh-pilot/runs/smoke_v2`

---

## 11) 라운드 전환 정리(파일 cleanup)
본 보고서 작성 시점에 아래 정리를 수행했습니다.

- 삭제(run): `runs/dryrun_qwen3`, `runs/dryrun_qwen3_v2`, `runs/dryrun_qwen3_v3`, `runs/smoke_v1`
- 삭제(log): `logs/smoke_v1_*`, `logs/smoke_v2_shard0.log`, `logs/smoke_v2_shard1.log`(빈 파일)
- 삭제(cache): `src/__pycache__`, `tests/__pycache__`
- 종료(session): `incoh_monitor` (stale tmux)

자동 정리 스크립트:
- `/data2/chojm/incoh-pilot/scripts/cleanup_round.sh`

다음 라운드 시작 전 동일 스크립트를 실행해 불필요 산출물을 정리하는 운영 방식을 권장합니다.
