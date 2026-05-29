<div align="center">

# incoherence-aware-control

**불안정성을 보고 test-time compute를 더 똑똑하게 배분할 수 있는가**
**Can we steer test-time compute using answer-incoherence as a signal?**

![Status](https://img.shields.io/badge/status-dormant-lightgrey)
![Language](https://img.shields.io/badge/language-Python-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)
![Closure](https://img.shields.io/badge/closure-2026--03-blue)

**한국어** · [English](#english) · [中文](./README.zh-CN.md)

</div>

> 🧊 **휴면(dormant) 중인 연구 파일럿입니다.**

## ⭐ 핵심 결과 (TL;DR)

- **불안정성(incoherence) 신호로 test-time compute를 배분하면 효과가 있었습니다** — 충분히 큰 예산에서 균등 배분 baseline보다 정확도·안정성이 모두 개선.
- 단 **효과는 예산에 의존**했습니다 — 작은 예산에선 안정성은 올라도 정확도는 떨어질 수 있었습니다("항상"이 아니라 "조건부").
- **가장 강한 단순 baseline(여러 번 풀어 다수결)을 깔끔히 이기진 못했습니다** — 컨트롤러 고유의 이득을 분리하지 못했습니다.

## 무엇을 보려던 연구였나

객관식 추론 문제(예: GPQA, MMLU)에서 모델에게 같은 양의 "생각할 시간(test-time compute)" 을 줄 때, 좀 더 똑똑하게 그 시간을 배분하는 컨트롤러를 만들 수 있을까 — 라는 질문에서 출발한 연구입니다.

핵심 아이디어는 단순했습니다.

- 모델이 한 문제를 여러 번 풀어 보게 합니다.
- 답이 흔들리는 정도를 **"불안정성(incoherence)"** 이라는 양으로 측정합니다.
- 그 불안정성을 보면서, 더 위태로워 보이는 문제에 시간을 더 쓰게 합니다.

이렇게 하면 같은 예산 안에서 정확도와 안정성을 동시에 챙길 수 있지 않을까 — 가 출발 가설이었습니다.

## 무엇을 알아냈나

여러 라운드를 거치면서 결론은 점점 좁아졌습니다. 마지막까지 가장 정직하게 말할 수 있는 건 이 정도입니다.

- **컨트롤러 효과 자체는 있었습니다.** 충분히 큰 예산을 줄 때는, 단순히 시간을 균등하게 쓰는 baseline 보다 정확도와 안정성 모두 더 좋았습니다.
- **다만 그 효과는 예산에 따라 달라졌습니다.** 예산이 작을 때는 안정성은 좋아져도 정확도는 오히려 떨어지는 경우가 있었습니다. 즉 "항상 이긴다" 가 아니라 "조건이 맞으면 이긴다" 였습니다.
- **가장 강한 단순 baseline 까지 이긴다는 주장은 끝까지 마무리하지 못했습니다.** 단순히 여러 번 풀어 보고 답을 합치는 방식이 의외로 강했고, 컨트롤러만의 고유 이득이 얼마인지 깔끔하게 분리하지 못했습니다.

자세한 숫자가 궁금하시면:

- 🇰🇷 [`closure_reports/project_closure_report_ko_20260327.md`](closure_reports/project_closure_report_ko_20260327.md)
- 🇬🇧 [`closure_reports/project_closure_report_20260327.md`](closure_reports/project_closure_report_20260327.md)

## 왜 잠시 멈춰 두는가

처음에는 "이런 컨트롤러가 항상 더 좋다" 라는 더 야심찬 주장을 노렸지만, 라운드를 거듭할수록 결론이 "조건이 맞으면 더 좋다" 쪽으로 좁아졌습니다. 그 좁아진 결론도 그 자체로는 의미가 있지만, 지금 시점에서 더 밀어붙이는 것보다는 잠시 묶어 두고, 새로운 자극(다른 데이터셋, 새로운 컨트롤러 계열, 더 강한 baseline 분해)이 생겼을 때 다시 깨우는 편이 자연스럽다고 판단했습니다.

## 다시 들여다볼 때는 어디부터

- 📖 [`GLOSSARY.md`](GLOSSARY.md) — 본문과 종료 보고서에 등장하는 내부 용어(`incoherence`, `spend sweep`, `hard_cap`, `ours_controller_v3_nofallback`, `T*`, splitA/B 등)를 일반어로 정리한 사전
- [`docs/HANDOVER_MASTER.md`](docs/HANDOVER_MASTER.md) — 전체 흐름 한 번에
- [`docs/EXPERIMENT_TIMELINE.md`](docs/EXPERIMENT_TIMELINE.md) — 라운드별 어떤 변화가 있었는지
- [`docs/ARTIFACT_INDEX.md`](docs/ARTIFACT_INDEX.md) — 어떤 산출물이 어디에 있는지
- [`docs/REPRODUCTION_GUIDE.md`](docs/REPRODUCTION_GUIDE.md) — 다시 실행하는 절차
- [`docs/NEXT_STEPS_CHECKLIST.md`](docs/NEXT_STEPS_CHECKLIST.md) — 다음에 해 볼 만한 후보들

## 코드 어디에 뭐가 있나

| 파일 | 하는 일 |
|---|---|
| [`src/run_pilot.py`](src/run_pilot.py) | 실험을 실제로 돌리는 메인 러너 |
| [`src/methods.py`](src/methods.py) | 비교에 쓰는 baseline 들과 우리 쪽 컨트롤러 구현 |
| [`src/parser.py`](src/parser.py) | 모델 답안을 정답 형식으로 뽑아내는 파서 |
| [`src/token_meter.py`](src/token_meter.py) | 한 문제당 쓴 토큰을 일관된 기준으로 세는 회계 |
| [`src/analyze_hotmess_style.py`](src/analyze_hotmess_style.py) | 불안정성(incoherence) 같은 진단 지표 계산 |
| [`src/report_spend_sweep.py`](src/report_spend_sweep.py) | 예산을 바꿔 가며 비교한 결과를 표/리포트로 정리 |

## 폴더 지도

```
.
├── src/                실험 코드
├── configs/            라운드별 실험 설정
├── scripts/            파이프라인 실행 스크립트
├── tests/              회귀 / smoke 테스트
├── reports/            라운드별 보고서와 사전 등록(prereg) 자료
├── docs/               전체 핸드오버 문서들
├── selected_runs/      라운드별 핵심 run 의 요약본
├── closure_reports/    종료 보고서 (한국어 / 영문)
└── GLOSSARY.md         내부 용어 사전
```

## 환경

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install -U -r requirements.txt
export HF_TOKEN=...   # 필요한 경우에만
```

## 상태

🧊 **휴면 중** — 능동 개발은 멈췄지만 살리려면 살릴 수 있는 상태입니다.

---

<a name="english"></a>

## English

> 🧊 **Dormant research pilot.**

### ⭐ Key result (TL;DR)

- Steering test-time compute by **incoherence works** — at large enough budgets it beat uniform allocation on both accuracy and stability.
- But the **win is budget-dependent** — at small budgets stability rose while accuracy could fall ("conditional," not "always").
- It **did not cleanly beat the strongest simple baseline** (repeat-and-vote); the controller's unique gain wasn't isolated.

### What this set out to test

On multiple-choice reasoning benchmarks (e.g., GPQA, MMLU), at a fixed test-time compute budget, can a controller allocate that budget more cleverly than uniform allocation?

The core idea was simple:

- Have the model solve each question several times.
- Measure how much the answer wavers across attempts — call this **incoherence**.
- Use that incoherence signal to spend more compute on the more uncertain-looking questions.

The starting hypothesis: doing so could improve accuracy **and** answer stability under the same total budget.

### What it found

Conclusions narrowed across rounds. The most honest summary that stayed standing:

- **The controller does have an effect.** At sufficiently large budgets, both accuracy and stability improved over uniform-allocation baselines.
- **But the effect depends on the budget.** At smaller budgets, stability improved while accuracy could drop. So: "wins under the right conditions," not "always wins."
- **The strongest simple baseline was not cleanly beaten.** Plain repeat-and-aggregate ("ask N times, vote") was surprisingly strong; isolating the controller's unique contribution didn't fully resolve.

Full numbers:

- 🇰🇷 [`closure_reports/project_closure_report_ko_20260327.md`](closure_reports/project_closure_report_ko_20260327.md)
- 🇬🇧 [`closure_reports/project_closure_report_20260327.md`](closure_reports/project_closure_report_20260327.md)

### Why it's on hold

The original ambition ("this controller is always better") narrowed to "better under the right conditions." That narrower result has standalone value, but pushing further now is less natural than parking it and waiting for a fresh angle (different dataset, different controller family, sharper baseline decomposition).

### Where to look first when revisiting

- 📖 [`GLOSSARY.md`](GLOSSARY.md) — Decoder ring for the internal vocabulary that survived into source and closure reports (`incoherence`, `spend sweep`, `hard_cap`, `ours_controller_v3_nofallback`, `T*`, splitA/B, etc.).
- [`docs/HANDOVER_MASTER.md`](docs/HANDOVER_MASTER.md) — whole-project handover.
- [`docs/EXPERIMENT_TIMELINE.md`](docs/EXPERIMENT_TIMELINE.md) — per-round changes.
- [`docs/ARTIFACT_INDEX.md`](docs/ARTIFACT_INDEX.md) — what artifact lives where.
- [`docs/REPRODUCTION_GUIDE.md`](docs/REPRODUCTION_GUIDE.md) — how to re-run.
- [`docs/NEXT_STEPS_CHECKLIST.md`](docs/NEXT_STEPS_CHECKLIST.md) — candidate next moves.

### Code map

| File | What it does |
|---|---|
| [`src/run_pilot.py`](src/run_pilot.py) | Main experiment runner |
| [`src/methods.py`](src/methods.py) | Baselines and the project's controller implementation |
| [`src/parser.py`](src/parser.py) | Extracts the answer choice from raw model output |
| [`src/token_meter.py`](src/token_meter.py) | Per-question token accounting on a consistent basis |
| [`src/analyze_hotmess_style.py`](src/analyze_hotmess_style.py) | Diagnostic metrics including incoherence |
| [`src/report_spend_sweep.py`](src/report_spend_sweep.py) | Cross-budget comparison tables and reports |

### Folder map

```
.
├── src/                experiment code
├── configs/            per-round experiment configs
├── scripts/            pipeline runners
├── tests/              regression / smoke tests
├── reports/            per-round reports and pre-registration documents
├── docs/               handover documents
├── selected_runs/      summaries of the key runs per round
├── closure_reports/    closure reports (KO / EN)
└── GLOSSARY.md         internal-vocabulary decoder ring
```

### Environment

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install -U -r requirements.txt
export HF_TOKEN=...   # only if needed
```

### Status

🧊 **Dormant** — active development stopped; revivable if the next angle calls for it.

### License

Released under [CC BY-NC 4.0](./LICENSE).
