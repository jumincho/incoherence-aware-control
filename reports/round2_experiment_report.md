# Round2 Experiment Report (End-to-End)

## 1) Objective
- Core claim to test: **incoherence-aware test-time control** can reduce `incoherence = variance / error` while keeping accuracy from dropping significantly.
- Primary benchmark: `Wanfq/gpqa` (`gpqa_diamond`, `train` subset).
- Main metrics: Accuracy, Bias, Variance, Incoherence, Avg total tokens, parse-fail rate.

## 2) Feedback Integration Checklist
This round explicitly incorporated key feedback items.

- Total-token accounting (prompt + output + discarded + restarts): implemented.
- Parse-fail taxonomy + per-method reporting: implemented (`NO_ANSWER`, `MULTI_ANSWER`, `INVALID`).
- Bias/variance identity sanity check (`error = bias + actual_variance`): implemented and passed (no identity failures).
- Budget sweep (>=4 levels): implemented (`1024, 1536, 2048, 2560`).
- Ablations for decomposition/anchor: implemented (`ours_decompose_only`, `ours_anchor_only`).
- Failure taxonomy for `ours_full`: implemented.
- Stratification by baseline disagreement: implemented in analyzer output.

## 3) Code/Infra Changes
Key files updated for Round2 stability and reliability.

- `src/run_pilot.py`
  - Injects per-question budget into method params (`_budget_total`) so adaptive logic actually activates.
  - Logs detailed token events and stage spends.
- `src/token_meter.py`
  - Total-token budgeting and per-call accounting.
- `src/parser.py`
  - Improved parsing to prioritize explicit final-answer lines.
  - Parse-fail taxonomy.
- `src/methods.py`
  - 8 methods with budget-aware structured behavior.
  - Fallback in `confidence_select`.
- `src/analyze_hotmess_style.py`
  - Budget-wise summary, bootstrap comparisons, parse-fail tables, stratification, failure taxonomy.
- `configs/round2_gpqa.yaml`
  - Budget sweep and method settings tuned for total-token regime.
- Added scripts:
  - `scripts/launch_round2_compact.sh`

## 4) Executed Runs
## 4.1 Main Round2 Run (completed)
- Run ID: `round2_compact_v1`
- Command basis: `scripts/launch_round2_compact.sh`
- Config: `configs/round2_gpqa.yaml`
- Effective scope: `N=48`, `R=2`, 8 methods, 4 budgets, 8 GPUs.
- Expected records: `48 * 2 * 8 * 4 = 3072`.
- Status: **completed** (`3072/3072`, 8/8 shards done).

## 4.2 Cost-matched Add-on Run (completed)
- Run ID: `round2_costmatch_v1`
- Config: `configs/round2_costmatch.yaml`
- Methods: `baseline_longcot`, `hard_cap`, `ours_controller`
- Budget: `1024` only
- Scope: `N=48`, `R=2`, expected `288` records.
- Status: **completed** (`288/288`, 8/8 shards done).

## 5) Main Results (round2_compact_v1)
### 5.1 Ours Controller vs Baseline by Budget

- Budget `1024`
  - baseline: acc `0.3958`, incoh `0.0169`, avg_total_tokens `442.1`
  - ours_controller: acc `0.4062`, incoh `0.0667`, avg_total_tokens `542.7`
  - verdict: **FAIL** (incoherence worsened)

- Budget `1536`
  - baseline: acc `0.3854`, incoh `0.0508`, avg_total_tokens `435.6`
  - ours_controller: acc `0.3854`, incoh `0.0169`, avg_total_tokens `1030.2`
  - incoh reduction abs `+0.0417` (rel `+81.9%`), acc delta `0.0000` (CI includes 0)
  - verdict: **PASS**

- Budget `2048`
  - baseline: acc `0.4271`, incoh `0.0526`, avg_total_tokens `437.5`
  - ours_controller: acc `0.3854`, incoh `0.0333`, avg_total_tokens `1133.6`
  - incoh reduction abs `+0.0069` (rel `+13.2%`), acc delta `-0.0417` (CI touches 0)
  - verdict: **PASS** (configured criterion)

- Budget `2560`
  - baseline: acc `0.4271`, incoh `0.0877`, avg_total_tokens `436.0`
  - ours_controller: acc `0.4062`, incoh `0.0175`, avg_total_tokens `1188.8`
  - incoh reduction abs `+0.0556` (rel `+63.3%`), acc delta `-0.0208` (CI includes 0)
  - verdict: **PASS**

### 5.2 Ablation Signals
- `ours_full` consistently underperformed on incoherence and did not pass at any budget.
- Failure taxonomy for `ours_full` is dominated by `wrong_reasoning` (not parse failures).
- `ours_decompose_only` showed selective benefit only at highest budget (`2560`).
- `ours_anchor_only` did not pass at any budget.

### 5.3 Parse/Robustness
- Overall parse failures were very low in final main run (`~0.13%` overall during completion phase).
- Method x budget parse-fail tables are present and mostly 0 except small `ours_controller` NO_ANSWER at `1536/2048`.
- Identity sanity check failures: none.

## 6) Cost-matched Add-on Result (round2_costmatch_v1)
At `budget=1024` with controller constrained for low token use:
- baseline: acc `0.3646`, incoh `0.0323`, avg_total_tokens `431.2`
- hard_cap: acc `0.3646`, incoh `0.0164`, avg_total_tokens `266.0` -> **PASS**
- ours_controller (cost-matched style): acc `0.3958`, incoh `0.0769`, avg_total_tokens `261.2` -> **FAIL**

Interpretation:
- Under strict low-cost constraints, controller did not suppress incoherence.
- Controller benefit appears in medium/high compute regime (1536+), not in aggressive cost-matched low-compute regime.

## 7) Success Criteria Assessment
Configured success criterion:
- Incoherence reduction >= 10% relative
- No significant accuracy drop

Assessment:
- `ours_controller` **meets criterion at budgets 1536/2048/2560** in main run.
- `ours_controller` **fails at budget 1024** and in strict cost-matched add-on.
- Therefore the claim is **conditional**: effective in medium/high budget regime, not universally across low-budget cost-matched settings.

## 8) Mapping Back to 3 Ideas
- Idea 1 (adaptive controller): **partially validated**
  - Works in medium/high budget, but not low-cost matched regime.
- Idea 2 (decomposition + constraints): **currently weak/conditional**
  - `decompose_only` helps only at highest budget.
- Idea 3 (small-anchor): **not validated in current form**
  - `anchor_only/full` did not produce consistent gains.

## 9) Artifacts
- Main run dir: `runs/round2_compact_v1`
- Main summary: `runs/round2_compact_v1/round2_summary.md`
- Main analysis JSON: `runs/round2_compact_v1/analysis_summary_round2.json`
- Cost-match run dir: `runs/round2_costmatch_v1`
- Cost-match summary: `runs/round2_costmatch_v1/round2_summary.md`
- Report copies:
  - `reports/round2_compact_summary.md`
  - `reports/round2_costmatch_summary.md`

## 10) Cleanup Performed
Removed obsolete/intermediate artifacts from failed/aborted Round2 attempts:
- old smoke runs, partial full runs (`round2_full_v2/v3/v4`), micro/preflight scratch runs.
- corresponding obsolete logs in `logs/`.

Current retained run set:
- `runs/pilot_full_v1` (Round1 reference)
- `runs/round2_compact_v1` (main Round2)
- `runs/round2_costmatch_v1` (cost-matched add-on)
