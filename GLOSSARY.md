# Glossary

The closure reports and the code carry some internal vocabulary that isn't
self-explanatory if you're coming in cold. This is the decoder ring.

## The headline signal

| Term | What it means |
|---|---|
| **Incoherence** | Per-cell metric defined in `src/analyze_hotmess_style.py::compute_budget_stats` as `sum_variance / (sum_bias + sum_variance)` over all questions in a `(method, budget)` cell. The variance term is computed per question by `hot-mess-of-ai`'s `process_question_metrics` across that question's multiple trial seeds — i.e., it captures *how much the model's answer wavers across reseeded attempts on the same question*. Lower is better. This is the signal the controller is meant to steer compute by. |
| **inter_disagreement** | A simpler per-doc proxy: `1 − (max-final-answer-count / number-of-final-answers)` across the question's trials. Used for stratification (`stratify_disagreement`), not as the headline metric. |
| **intra_flip_rate** | Average count of within-attempt answer flips inside a single response, recorded by `parser.count_flips` / `summarize_answer_trace`. A different axis of instability: not "different attempts disagree," but "a single attempt's text mentions different letters." |
| **bias / variance / accuracy_hard** | The bias / variance / hard-accuracy decomposition coming out of `process_question_metrics`. The project enforces the identity `1 − soft_acc ≈ bias + actual_variance` per question (`--identity-tol`) so a violation is flagged into `identity_failures.jsonl`. |

## Spend, budget, and the spend sweep

| Term | What it means |
|---|---|
| **Spend** / **budget** | The total-token budget per question, in tokens (prompt + output + parse-repair + restart, all counted together by `src.token_meter.TokenBudget`). Configured per round as `evaluation.total_token_budgets` in `configs/round*.yaml`. The runner sweeps each question × method through every budget in that list. |
| **Spend sweep** | The experiment design: at fixed dataset + seeds + methods, vary the per-question token budget across e.g. `{300, 500, 700, 900, 1200, 1500}` and measure accuracy / incoherence at each point. Implemented end-to-end as `src.run_pilot` → `src.analyze_hotmess_style` → `src.report_spend_sweep`. |
| **Total tokens vs. attempts** | The project's primary budget axis is **total tokens** (`budget_total`), not attempts. Repeat-and-aggregate methods consume more tokens by issuing more attempts; controller methods consume more by issuing longer solves. The accounting is unified so they're directly comparable. |
| **T\*** ("threshold") | The lowest budget at which `ours_controller_v3_nofallback` beats `hard_cap` on both accuracy and incoherence in a held-out evaluation. `report_spend_sweep._phase_thresholds*` is the estimator. **T\* is protocol-dependent** — Round 8 reports ≈ 400, Round 9 reports ≈ 900. See `docs/HANDOVER_MASTER.md` §3. |
| **budget_utilization** | Per-row average of `min(1, total_tokens / budget_total)` — how much of the budget the method actually spent. |
| **stage_token_spend** | Per-row breakdown of total tokens by `step.role` (`probe`, `solve`, `restart`, `repair`, `anchor`, `verify`, ...) as emitted by `TokenBudget`. `controller_diagnostics` uses this to compute the probe / solve / restart **token shares** per method. |

## Methods (the controllers and the baselines)

The full dispatch table is `methods.run_method`. By family:

### Static, uniform-allocation baselines

| Name | What it does |
|---|---|
| `baseline_longcot` | Long chain-of-thought solve, one attempt. |
| `hard_cap` | Short strict-format solve under a per-budget `max_new_tokens` cap (the project's primary `uniform` baseline). |
| `hard_cap_matched` | Same logic as `hard_cap`, run with a budget chosen to *token-match* what the controller actually spends. Forces an apples-to-apples comparison. |

### Repeat-and-aggregate ("ask N times and vote")

This is the family the closure report flags as "surprisingly strong; not cleanly beaten." All members issue multiple short attempts and aggregate by majority vote / highest confidence.

| Name | What it does |
|---|---|
| `self_consistency` | `N` independent attempts; majority vote; tie-break by confidence. |
| `confidence_select` | `N` attempts; pick the single attempt with the highest stated `Confidence:`. |
| `budgeted_self_consistency` | As `self_consistency`, with optional early stop once agreement crosses a threshold. |
| `probe_only_fixedk` / `probe_only_fixedk_kN` | `K` short "Tentative Answer" probes only — no separate solve stage. Majority vote of the probes. |
| `probe_adaptive_k` | Grow `K` from `initial_k` toward `k_max` until majority agreement crosses `agreement_threshold` (or `k_max` is reached). |

### Project's controllers (the "ours" family)

The incoherence signal is read off the probe-stage disagreement; that decides whether to stop or to spend more compute on a solve.

| Name | What it does |
|---|---|
| `ours_controller` | v1. Run `n_probe` probes → if `agreement >= stop_conf_threshold`, stop and vote; else spend a long solve; restart on parse failure. |
| `ours_controller_v2` | v2. Adds a budget-aware probe reserve (`probe_budget_ratio`, `probe_budget_cap`) and a hard `solve_min_target` floor so the solve stage always has room. Optional low-budget hard-cap fallback. |
| `ours_controller_v3` | v3 (Round 9 / latest). Stricter low-budget fallback (`low_budget_stop_forbid_threshold`), tighter probe cap, reserved solve floor, "Solve carefully after probe disagreement" prompt. |
| `*_nofallback` | Same controller, but `enable_low_budget_fallback = False` — the controller is forced to run its own logic even at low budget. Used to isolate the controller's behaviour from the fallback's. |
| `*_nofallback_forcecontinue` / `*_nofallback_stopcap` | v2 variants that toggle `force_continue_disagreement_threshold` / `stop_after_probe_cap_rate` — i.e., they pin down *when* the controller is allowed to stop after probes. Used as ablations. |

### Structured deliberation (older line)

| Name | What it does |
|---|---|
| `forced_deliberation` | Initial solve, then `max_rounds` of "reconsider alternatives" follow-ups; final answer is the last successful one. |
| `ours_full` / `ours_anchor_only` / `ours_decompose_only` | Anchor (checklist) and/or decompose (subtasks) stages before the solve, then a verify pass. `hard_anchor=True` lets a passing verify overwrite the solve answer. The auxiliary anchor model lives at `cfg.models.anchor`. |

## Code modules

| File | Plain English |
|---|---|
| `src/run_pilot.py` | Main runner. Builds the question pool from a HF dataset, shards over GPUs, loops `(question × seed × method × budget)`, calls `methods.run_method`, parses the result, writes one row per cell to `results_shard*.jsonl`. Also enforces the parse-repair reserve. |
| `src/methods.py` | Every method implementation + the `run_method` dispatch. See "Methods" above. |
| `src/parser.py` | Turns raw model text into a single `(A)`/`(B)`/`(C)`/`(D)` answer (or a typed parse-failure). Also counts within-response answer flips. |
| `src/token_meter.py` | `TokenBudget` — counts prompt + output + repair + restart + discarded tokens on the same total basis. Single source of truth for "compute spent." |
| `src/analyze_hotmess_style.py` | Bias / variance / **incoherence** metrics, paired-bootstrap deltas, controller decision diagnostics, parse-fail tables. Writes the analysis JSON the reports consume. |
| `src/report_spend_sweep.py` | Turns the analysis JSON into the per-round detailed markdown report — per-budget tables, threshold estimation, CIs, parse-repair diagnostics. |
| `src/monitor.py` | Live read-only progress watcher for an active run (progress %, parse-fail rate, ETA). |

## Benchmarks

| Name | What it means |
|---|---|
| **GPQA** | Graduate-Level Google-Proof Q&A. The project's primary benchmark — hard multiple-choice scientific reasoning. Loaded via HF `datasets`; `data_format: gpqa` triggers the GPQA-specific row schema (`Question`, `Correct Answer`, `Incorrect Answer 1..3`, `Writer's Difficulty Estimate`, `High-level domain`). |
| **MMLU** | Massive Multitask Language Understanding. Used as the **secondary reproduction benchmark** in Rounds 8 and 9 (`round*c_mmlu_repro_*`) — does the qualitative direction of the GPQA finding reproduce on a different dataset under the same protocol? |
| **splitA / splitB / splitA' / splitB' / splitA2..A9 / splitB2..B9** | Disjoint subsets of the question pool used as the **tuning** split (A) vs the **held-out** confirmation split (B). The numeric suffix bumps every time a methodological change forces a fresh split (`docs/REPRODUCTION_GUIDE.md` §4). |

## Per-round and per-run artifacts

| Term | What it refers to |
|---|---|
| **Round** | One protocol-frozen experimental iteration. Rounds 1–9; Round 9 is the final state of the world. Each round has a tuning sub-round (`a`), a held-out sub-round (`b`), optionally an MMLU reproduction (`c`), and sometimes a confirm-the-prior-finding sub-round (`d`). |
| `selected_runs/round{N}{a,b,c,d}_*` | Per-round summary-only artifacts: `run_meta.json`, `config_resolved.yaml`, analysis JSON, detailed markdown report. The raw `runs/` tree (the per-shard JSONLs) is not included in this closure bundle — it was too large and mostly redundant once the analysis JSONs were frozen. |
| `closure_reports/project_closure_report_*_20260327.md` | The final project-wide closure summary. `_ko_` is Korean, the other is English. Same content. |
| `reports/round{N}_*` | Per-round detailed reports and governance artifacts: experiment reports, integrated follow-ups, prereg docs, code-lock manifests. Survives by date order. |
| `reports/round{N}_preregistration.md` | Pre-registration document — the planned methods, splits, budgets, success criteria — written **before** the held-out run. |
| `reports/round{N}_code_lock_manifest.sha256` | SHA-256 of every source file at the moment of held-out launch. Frozen so the held-out can't silently use an updated method. |
| `reports/round{N}_adaptive_and_matched_config.json` | The specific config parameters used for the `adaptive` controller and its `hard_cap_matched` partner. |
| `runs/` | The full raw output tree from `run_pilot` (per-shard JSONLs, hot-mess logs, status files). Not included in this closure bundle — see `selected_runs/` for the small per-round summary that is preserved. |

## Handover docs

| File | What it's for |
|---|---|
| [`docs/HANDOVER_MASTER.md`](docs/HANDOVER_MASTER.md) | Whole-project handover. Goal, what was done across Rounds 1–9, current status, most-important files, open questions. The single-page brief if you have time for only one document. |
| [`docs/EXPERIMENT_TIMELINE.md`](docs/EXPERIMENT_TIMELINE.md) | One-line-per-round timeline (PoC → metric hardening → held-out formalization → fairness controls → v3 + fresh held-out). |
| [`docs/ARTIFACT_INDEX.md`](docs/ARTIFACT_INDEX.md) | Map from "what kind of artifact" → "where it lives" (code, configs, latest reports, governance). |
| [`docs/REPRODUCTION_GUIDE.md`](docs/REPRODUCTION_GUIDE.md) | How to re-run a round: env setup, Round 9 pipeline script, manual shard sequence, reproducibility rules. |
| [`docs/NEXT_STEPS_CHECKLIST.md`](docs/NEXT_STEPS_CHECKLIST.md) | Candidate next moves if the project is revived — split by "continuing the dynamic-novelty track" vs "solidifying the regime-aware claim." Plus the mandatory hygiene checklist before any new held-out. |
| [`docs/FILELIST.txt`](docs/FILELIST.txt) | Inventory of files in the transfer bundle. |
