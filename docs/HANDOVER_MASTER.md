# Handover Master (New Chat / New Server)

## 1. Project Goal
Build and validate **incoherence-aware test-time control** for MCQ reasoning, with the core claim:
- Under matched or budgeted test-time compute, reduce `incoherence = variance / error`
- Maintain or improve accuracy
- Report fairness/reproducibility controls explicitly (token accounting, parse policy, held-out split, code lock)

## 2. What Has Been Done (Round1 -> Round9)
- Round1: feasibility signal found for controller-style stabilization.
- Round2: accounting/identity/parse taxonomy hardened; conditional behavior surfaced.
- Round3: regime-dependent behavior became clear; low-budget failure vs mid/high-budget improvement.
- Round4: stronger baselines + parse repair + nofallback analysis; significant hygiene upgrades.
- Round5: pseudo held-out + prereg + code lock; threshold narrative strengthened.
- Round6: new split (A'/B'), parse confound reduced but not eliminated.
- Round7: stronger fairness controls; threshold tightened in held-out.
- Round8: strict formatter/repair reserve + matched baseline + secondary benchmark reproduction.
- Round9: controller v3 introduced (probe cap + solve reserve intent), with fresh split and full rerun.

## 3. Current Status Snapshot (as of Round9)
Primary status (latest):
- `ours_controller_v3_nofallback` vs `hard_cap` on held-out B9 shows **regime-dependent improvement**:
  - Low/mid budgets: incoherence improved but accuracy may drop
  - High budgets (`>=900` in Round9 report): accuracy and incoherence both improved
- Parse-fail confound is currently controlled in Round9 runs (parse fail reported as 0 in B9/C9/D9)
- Dynamic novelty over strong probe-only family remains mixed and not fully settled

Important nuance:
- Earlier rounds (e.g., Round8) showed threshold near `T≈400`
- Round9 (v3 settings/protocol) reports threshold around `T*=900`
- Treat threshold as **configuration/protocol dependent regime boundary**, not a universal constant

## 4. Most Important Files to Read First
1. `reports/round9_final_experiment_report.md`
2. `reports/round9b_heldout_splitB9_r5_v1_detailed_report.md`
3. `reports/round8_final_experiment_report.md`
4. `reports/round8b_heldout_splitB3_r5_v1_detailed_report.md`
5. `reports/round9_preregistration.md`
6. `reports/round9_code_lock_manifest.sha256`

## 5. Ground Rules Already Adopted
- Pre-registration before held-out run
- Code-lock manifest prior to final held-out
- Unified token accounting: prompt + output + repair + discard + restart
- Unified parse policy: P1R + formatter + repair reserve
- Explicit method x budget parse-fail matrix and sensitivity view

## 6. Known Open Questions
1. Can dynamic controller strictly dominate strong static probe-only frontiers in Pareto terms?
2. Is the threshold stable across datasets/models, or policy/hyperparameter dependent?
3. Which risk signal best predicts instability regime (disagreement/entropy/etc.)?

## 7. If Starting New Chat
Give this exact context first:
- Read `docs/EXPERIMENT_TIMELINE.md` and `docs/ARTIFACT_INDEX.md`
- Use Round9 as latest baseline
- Do not reuse old held-out split after changing policy; create fresh split for any methodological change
