# Incoherence-Aware Test-Time Control 종료 보고서

작성일: 2026-03-27  
아카이브 대상 저장소: `/workspace/incoh-pilot-transfer-repo`

## 1. 한눈에 보는 결론

이 프로젝트는 **multiple-choice reasoning에서 test-time budget을 더 잘 쓰는 controller를 만들 수 있는가**를 연구한 실험 시리즈입니다.

핵심 아이디어는 다음과 같았습니다.

- 추론 과정에서 여러 probe 또는 controller 단계를 수행하고
- 그 결과의 불안정성을 `incoherence`라는 양으로 측정하며
- 예산을 더 지능적으로 배분해 incoherence를 줄이면서 정확도도 유지하거나 높이고자 한다

최종적으로 가장 정직한 해석은 이렇습니다.

- **controller 효과 자체는 있다**
- 다만 그 효과는 **budget 구간에 따라 달라지는 regime-dependent 현상**이다
- 후반 라운드의 더 엄격한 프로토콜에서는 incoherence 감소가 안정적으로 보였다
- 하지만 정확도까지 함께 좋아지는 것은 모든 budget이 아니라 **충분히 큰 budget 구간**에서만 확인되었다
- 또, probe-only 강한 baseline까지 controller가 깔끔하게 압도했다고 보기는 어렵다

즉 이 프로젝트의 결론은 “controller가 항상 이긴다”가 아니라 다음에 가깝습니다.

> incoherence-aware test-time control은 도움이 될 수 있지만, 그 이득은 budget regime에 강하게 의존하며 보편적인 dominance 결과는 아니다.

## 2. 이 프로젝트는 무엇을 하려던 것이었나

이 저장소는 대략 **Round 1부터 Round 9까지** 이어진 실험의 transfer package입니다.

연구 질문은 간단히 말해 다음과 같습니다.

- 같은 test-time compute budget에서
- 단순한 baseline보다 더 안정적인 추론 제어를 할 수 있는가
- 그 결과 incoherence를 줄이면서 정확도까지 유지하거나 높일 수 있는가

주요 baseline은 다음과 같았습니다.

- `hard_cap`
- `hard_cap_matched`
- `probe_only_fixedk_k{2,4,8}`
- `probe_adaptive_k_selected`
- `budgeted_self_consistency`

우리 쪽 method는 점진적으로 바뀌었습니다.

- `ours_controller`
- `ours_controller_v2_nofallback`
- `ours_controller_v3_nofallback`

후반 라운드의 주요 벤치마크는:

- `GPQA`
- 보조 재현 벤치마크로 `MMLU`

또한 이 프로젝트는 후반으로 갈수록 실험 위생과 공정성 통제를 매우 중요하게 다루었습니다.

- unified token accounting
- 공통 parser / repair policy
- parse-fail 공개
- held-out split
- preregistration
- code-lock manifest

## 3. 저장소에서 중요한 코드

핵심 구현은 다음 파일에 모여 있습니다.

- `src/run_pilot.py`: 메인 실험 러너와 sharded 실행
- `src/methods.py`: baseline과 controller 구현
- `src/parser.py`: 정답 추출과 parse-policy
- `src/token_meter.py`: token accounting
- `src/analyze_hotmess_style.py`: incoherence / variance 계열 분석
- `src/report_spend_sweep.py`: budget sweep 결과 보고서 생성

운영상 중요한 디렉터리는 다음과 같습니다.

- `configs/`: 라운드별 설정
- `scripts/`: 파이프라인 실행 스크립트
- `reports/`: 라운드 보고서, prereg, code-lock 등
- `docs/`: handover와 재현 가이드

## 4. 프로젝트가 어떻게 전개되었는가

### Round 1 ~ 4

초기 라운드들은 feasibility와 측정 체계 정리에 가까웠습니다.

이 단계에서 알게 된 점:

- controller 비슷한 접근이 불안정성을 줄일 가능성은 있었다
- 하지만 token accounting, parser 동작, parse-fail 처리 방식이 결과를 크게 흔들 수 있었다
- 즉, 프로토콜을 엄격히 고정하지 않으면 좋아 보이는 결과가 착시일 수 있었다

그래서 초기에는 “가능성은 있다” 정도였고, 아직 강한 결론을 내릴 단계는 아니었습니다.

### Round 5 ~ 7

이 구간에서는 실험을 더 publication-grade에 가깝게 만들기 위한 작업이 들어갔습니다.

- preregistration
- code lock
- held-out split
- 보다 엄격한 claim discipline

이 과정에서 서사는 더 좁고 더 정직해졌습니다.

- controller는 여전히 유망해 보였지만
- 정확히 어느 budget에서 좋아지는지, 얼마나 robust한지는 프로토콜에 따라 달라졌다
- 강한 baseline과 cleaner control을 넣을수록 원래 주장도 더 보수적으로 바뀌었다

### Round 8

Round 8은 이 저장소에서 매우 중요한 분기점입니다.

여기서 다음이 들어갔습니다.

- 새로운 pool과 split
- stricter fairness control
- strict formatter / repair reserve
- unified token accounting
- matched hard-cap baseline
- second benchmark reproduction

가장 중요한 Round 8 결과:

- held-out `GPQA` B3에서 `ours_controller_v2_nofallback`이 `hard_cap` 대비 대략 `T*=400`부터 정확도와 incoherence를 함께 개선했다
- core held-out budget들에서 parse fail은 사실상 0으로 통제되었다
- `MMLU` 재현에서도 hard-cap 계열 대비 같은 방향의 결과가 나왔다

하지만 중요한 제한도 남았습니다.

- probe-only 강한 baseline을 상대로 controller가 완전히 결정적 우위를 보였다고 하기는 어려웠다

### Round 9

Round 9는 이 프로젝트의 최신이자 사실상 최종 상태입니다.

여기서 새로 들어간 것:

- fresh split
- `ours_controller_v3_nofallback`
- 새 preregistration
- 새 code lock
- held-out GPQA
- confirm run
- MMLU 재현

Round 9의 핵심은 Round 8보다 더 nuanced했습니다.

- `hard_cap` 대비 전환 임계점이 대략 `T*=900`으로 올라갔다
- 그보다 낮은 budget에서는 incoherence는 줄지만 정확도를 희생하는 경우가 많았다
- `900`, `1500` 같은 높은 budget에서는 정확도와 incoherence를 함께 개선했다

대표적인 held-out GPQA B9 결과:

- Budget `900`: `Δacc = +0.0986`, `Δincoh = -0.1409`
- Budget `1500`: `Δacc = +0.1081`, `Δincoh = -0.1551`

동시에 중요한 사실:

- parse fail은 `0`
- repair success는 사실상 완전 통제
- confirm run은 낮은 budget 위주여서 그 구간의 accuracy drop을 다시 보여 주었다
- probe-only 대비 controller novelty는 여전히 완전히 정리되지 않았다

그래서 최종 결론은 이렇게 정리됩니다.

- controller 효과는 **있다**
- 하지만 **regime-dependent**이다
- threshold는 **보편적 상수**가 아니다
- probe-only 대비 novelty는 **혼합적(mixed)** 이다

## 5. 그래서 무엇을 알아냈는가

### 가장 강하게 말할 수 있는 주장

이 프로젝트가 가장 자신 있게 남기는 결론은 다음입니다.

> 엄격한 accounting / parse control 아래에서 incoherence-aware controller는 충분히 큰 budget 구간에서 hard-cap baseline보다 더 좋을 수 있다.

이 주장을 믿을 수 있는 이유:

- 후반 라운드에서 프로토콜이 계속 더 엄격해졌는데도 효과가 완전히 사라지지 않았다
- Round 8과 Round 9 모두 threshold-style 현상을 보였다
- second benchmark에서도 같은 방향이 재현되었다
- 후반에는 parse confound가 사실상 제거되었다

### 중요한 단서

threshold는 안정적인 상수가 아니었습니다.

저장소 내부 기록만 봐도:

- Round 8에서는 대략 `T≈400`
- Round 9에서는 대략 `T≈900`

따라서 threshold는 이렇게 해석해야 합니다.

- **설정과 프로토콜에 의존하는 regime boundary**

이렇게 해석하면 안 됩니다.

- **항상 같은 값을 갖는 보편 법칙**

### 약하거나 미해결인 주장

끝내 강하게 말하지 못한 것은 다음 주장입니다.

> dynamic controller가 strong probe-only baseline까지 깔끔하게 지배한다.

이 주장이 약한 이유:

- probe-only 계열이 매우 강했다
- controller novelty가 실제로 probe-only 선택보다 얼마나 더 본질적인지는 끝까지 혼합적이었다
- 일부 budget에서는 incoherence 개선이 커도 accuracy drop이 함께 남았다

즉 이 저장소는 sweeping dominance claim보다는, 더 조심스러운 systems-style claim을 지지합니다.

## 6. 왜 이 프로젝트를 아카이브하는가

이 작업은 분명 의미 있는 지식을 남겼지만, 시간이 갈수록 결론이 더 좁고 더 조건부가 되었습니다.

아카이브하는 이유:

1. 최종 주장이 초기의 가장 야심찬 framing보다 좁아졌습니다.
2. 가장 좋은 결과는 universal한 것이 아니라 regime-aware한 것입니다.
3. probe-only를 넘는 strongest novelty claim은 끝내 완전히 정리되지 않았습니다.
4. 이 저장소는 이미 active development repo라기보다 handoff / transfer package에 가깝습니다.

즉, 실패한 프로젝트라기보다는 “배운 것은 많지만, 최종적으로 남는 기여가 더 정밀하고 제한적이 된 프로젝트”에 가깝습니다.

## 7. 종료 시점의 정직한 상태

종료 시점에서 가장 정확한 상태 요약은 다음과 같습니다.

- 이것은 성숙한 실험 아카이브다
- 최신 기준점은 Round 9다
- 최신 serious method는 `ours_controller_v3_nofallback`이다
- high-budget에서 hard-cap 계열 대비 개선은 가장 믿을 만한 결과다
- probe-only 대비 novelty는 아직 mixed다

누군가 “그래서 이 저장소를 읽고 무엇을 믿어야 하나?”라고 묻는다면 가장 좋은 답은 다음입니다.

- **깨끗한 프로토콜과 충분한 budget에서는 incoherence-aware control이 실제로 도움될 수 있다**는 점은 믿어도 된다
- 하지만 **모든 budget에서 모든 강한 baseline을 이긴다고 믿으면 안 된다**

## 8. 이번 보관본에는 무엇을 남겼는가

이번 closure bundle은 원본 전체를 복사하지 않고, 보관과 이해에 필요한 핵심만 남겼습니다.

포함한 것:

- `src/` 전체 코드
- `configs/`, `scripts/`, `tests/`, `docs/`
- 라운드 보고서와 governance artifact 전체
- Round 8과 Round 9의 핵심 run들에서 summary-level 메타만 선별한 `selected_runs/`
- 이 종료 보고서 영문/한글판

제외한 것:

- 전체 raw `runs/` 트리

원본 `runs/`는 훨씬 크고, newcomer가 프로젝트의 최종 상태를 이해하는 데는 summary-level artifact만으로도 충분하다고 판단했습니다.

## 9. 최종 한 줄 정리

이 프로젝트는 “reasoning instability를 측정 가능한 것으로 만들고, test-time compute budget 안에서 제어할 수 있는가”를 진지하게 탐구한 연구였습니다.

최종적으로 남은 가장 좋은 결론은:

- **엄격한 프로토콜 아래에서 controller 이득은 실제로 존재한다**
- **그 이득은 regime-dependent이다**
- **high-budget에서 hard-cap 대비 개선이 가장 강한 최종 결과다**
- **probe-only 대비 완전한 novelty는 아직 미해결이다**

이것이 이 저장소를 처음 읽는 사람에게 가장 정확하고 이해하기 쉬운 종료 시점 요약입니다.
