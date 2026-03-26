# Round4 Feedback Acceptance Note

## 요약
Round4 budget 결과에 대한 피드백 항목을 검토했고, 실험 안정성과 다음 Spend sweep 준비를 위해 아래를 수용/반영했다.

## 수용/반영 항목

### 1) fallback 동치성 점검 및 수정
- 문제: `ours_controller_v2`가 fallback 100%인데 `hard_cap`과 수치 차이가 날 수 있다는 지적.
- 원인: fallback 경로에서 seed offset(`+49001`)이 적용되어 hard_cap과 샘플링 조건이 달랐음.
- 조치:
  - `run_ours_controller_v2` fallback seed를 `trial_seed` 그대로 사용하도록 수정.
  - `run_ours_controller_v3` fallback도 동일하게 수정.
- 코드:
  - `/data2/chojm/incoh-pilot/src/methods.py`
- 검증:
  - 단위테스트 추가: fallback 동치성 test (`hard_cap` vs `v2 fallback`) 통과.
  - 실제 스모크(10문항, R=1, B=768) 결과:
    - pair 10개 중 `same_pred=10`, `same_text=10`, `same_tokens=10`.
  - 런 경로: `/data2/chojm/incoh-pilot/runs/round4_fallback_equiv_smoke_v2`

### 2) stop_after_probe formatter 강제
- 문제: 저예산 nofallback의 parse-fail(1~2%) 완화 필요.
- 조치:
  - controller의 `stop_after_probe` 경로에서 모델 출력을 그대로 쓰지 않고,
    코드에서 `Final Answer: X` 형식으로 최종 문자열을 강제 생성.
- 코드:
  - `/data2/chojm/incoh-pilot/src/methods.py`

### 3) parse repair 단답형 강화
- 문제: repair를 더 강하게 단답형으로 고정하라는 피드백.
- 조치:
  - repair prompt를 `A/B/C/D 한 글자만` 반환하도록 변경.
  - parser가 single-letter 응답(`A`, `d`)을 정답으로 인식하도록 확장.
- 코드:
  - `/data2/chojm/incoh-pilot/src/run_pilot.py`
  - `/data2/chojm/incoh-pilot/src/parser.py`
- 테스트:
  - parser 테스트에 single-letter 케이스 추가.
  - `/data2/chojm/incoh-pilot/tests/test_parser.py`

### 4) probe-only 정적 baseline 추가
- 목적: 동적 의사결정 기여 분리를 위해 `probe_only_fixedk` 도입.
- 조치:
  - `probe_only_fixedk` method 추가 (fixed-k probe 후 majority + formatter).
  - dispatcher 등록.
- 코드:
  - `/data2/chojm/incoh-pilot/src/methods.py`

### 5) Spend sweep 신규 설정 준비
- 피드백 권장 target 그대로 반영:
  - `T_target = {200,300,450,600,750,900,1200,1500}`
- method 구성:
  - `baseline_longcot`, `hard_cap`, `budgeted_self_consistency`,
    `ours_controller_v2`, `ours_controller_v2_nofallback`, `probe_only_fixedk`
- config:
  - `/data2/chojm/incoh-pilot/configs/round4_spend_core6.yaml`

## 품질 상태
- `py_compile` 통과
- unit tests 통과 (8/8)

## 다음 실행 권장
- Spend sweep 실행:
  - `HF_TOKEN=... ./scripts/launch_round4.sh round4_spend_core6_r5_v1 8 configs/round4_spend_core6.yaml`
