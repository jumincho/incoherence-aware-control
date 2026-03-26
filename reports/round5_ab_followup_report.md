# Round5 A/B Follow-up Experiment Report

Date: 2026-02-28 (UTC)  
Project: Incoherence-aware test-time control (GPQA spend regime)

## 1) Executive Summary
- Round5-A (Split A tuning) and Round5-B (Split B held-out) were both completed end-to-end.
- Core fairness controls from feedback were applied:
  - pseudo held-out split (A/B),
  - pre-registration,
  - code-lock checksum manifest,
  - identical parse policy and total-token accounting across methods,
  - identity check (`error = bias + variance`) passed (no dump).
- Main held-out result:
  - `ours_controller_v2_nofallback` starts beating `hard_cap` on incoherence from `T=600` onward while accuracy is higher.
  - `forcecontinue` did not show consistent incremental gain over `nofallback`.
- Remaining risk:
  - parse-fail remains method-skewed toward controller variants in low-T regimes (`T=200/300`).

## 2) Runs and Artifacts

### Round5-A (tuning split)
- Run ID: `round5a_tuning_splitA_r5_v2`
- Config: `configs/round5a_tuning_splitA.yaml`
- Data: manifest index `[0, 199]` from fixed 400-sample pool
- Methods:
  - `hard_cap`
  - `probe_only_fixedk`
  - `ours_controller_v2_nofallback`
  - `ours_controller_v2_nofallback_forcecontinue`
  - `ours_controller_v2_nofallback_stopcap`
- Budgets: `{300, 450, 600, 900, 1200}`, `R=5`
- Records: `25,000/25,000`, hard fail `0`
- Duration: `106.42` min
- Outputs:
  - `runs/round5a_tuning_splitA_r5_v2/analysis_summary_round2.json`
  - `reports/round5a_tuning_splitA_r5_v2_detailed_report.md`
  - `reports/round5a_dynamic_selection_note.md`

### Round5-B (held-out report split)
- Run ID: `round5b_heldout_splitB_r5_v1`
- Config: `configs/round5b_heldout_splitB.yaml`
- Data: manifest index `[200, 399]` (no retuning on B)
- Methods:
  - `hard_cap`
  - `budgeted_self_consistency`
  - `probe_only_fixedk`
  - `ours_controller_v2_nofallback`
  - `ours_controller_v2_nofallback_forcecontinue`
- Budgets: `{200, 300, 450, 600, 900, 1200, 1500}`, `R=5`
- Records: `35,000/35,000`, hard fail `0`
- Duration: `196.33` min
- Outputs:
  - `runs/round5b_heldout_splitB_r5_v1/analysis_summary_round2.json`
  - `reports/round5b_heldout_splitB_r5_v1_detailed_report.md`

## 3) Feedback-to-Implementation Mapping
- Pseudo held-out:
  - Implemented via `subset_start/subset_end` in `src/run_pilot.py`.
  - A/B split configs fixed.
- Pre-registration:
  - `reports/round5_preregistration.md`.
- Code lock:
  - `reports/round5_code_lock_manifest.sha256` (post-A/pre-B refresh).
- Same-policy parsing/repair:
  - All methods used `P1R` with shared repair setting (`repair_min_remaining_tokens=16`).
- Runtime stability fix:
  - `src/run_pilot.py` updated to load anchor model only when anchor-dependent methods are requested.
  - This removed unnecessary model load overhead for Round5 A/B method sets and stabilized 8-GPU shard execution.
- Equivalence/stability:
  - Existing unit tests retained and passing.
  - Runtime identity checks passed (`Identity failures dumped: none` in both runs).

## 4) Round5-A Key Findings (Split A Tuning)
- `stopcap` was consistently unstable and rejected.
- `forcecontinue` tracked `nofallback` closely and did not provide robust extra gain.
- Selection for Round5-B:
  - Kept pre-registered dynamic variant `ours_controller_v2_nofallback_forcecontinue` with fixed threshold `0.25`.
  - No Split-B retuning.

## 5) Round5-B Key Findings (Held-out)

### 5.1 Regime behavior vs `hard_cap`
- `T=200`: `nofallback` is worse (acc `-0.006`, incoh `+0.0003`).
- `T=300`: `nofallback` is worse (acc `-0.012`, incoh `+0.0073`).
- `T=450`: acc improves (`+0.013`) but incoh still worse (`+0.0049`).
- `T>=600`: `nofallback` improves both:
  - `T=600`: acc `+0.023`, incoh `-0.0080`
  - `T=900`: acc `+0.026`, incoh `-0.0163`
  - `T=1200`: acc `+0.021`, incoh `-0.0069`
  - `T=1500`: acc `+0.025`, incoh `-0.0188`
- Reported phase threshold:
  - first `nofallback` point beating `hard_cap` on both axes at `T=600`.

### 5.2 Dynamic gain vs `probe_only_fixedk`
- `nofallback` beats `probe_only` on incoherence at `T=450/600` but trails at `T=900/1200/1500`.
- `forcecontinue` did not dominate `nofallback`; usually equal or slightly worse incoherence.
- Conclusion:
  - “dynamic continue” incremental gain over strong static probe baseline remains unproven in this run.

### 5.3 Compute-scaling baseline
- `budgeted_self_consistency` generally highest accuracy but highest spend.
- `nofallback` provides lower spend with competitive/strong incoherence in mid/high regime.
- This supports a regime-dependent Pareto narrative (efficiency-consistency point vs accuracy-max point).

## 6) Parse-Fail and Fairness Risk Check
- Round5-B overall parse-fail: `607/35000 = 1.7343%`.
- Method-level parse-fail:
  - `hard_cap`: `0.43%`
  - `budgeted_self_consistency`: `0.84%`
  - `probe_only_fixedk`: `1.00%`
  - `ours_controller_v2_nofallback`: `3.17%`
  - `ours_controller_v2_nofallback_forcecontinue`: `3.23%`
- Budget-level controller parse-fail is highly concentrated at low-T:
  - `T=200`: `5.2%`
  - `T=300`: `12.9%`
  - `T>=450`: sharp drop (`0.4%`, `1.7%`, `1.3%`, `0.5%`, `0.2%`)
- Interpretation:
  - low-budget controller overhead + format robustness is still a confound risk.
  - results are reported with this limitation explicitly, not hidden.

## 7) Cleanup and File Hygiene
- Failed/partial attempt directories were not deleted destructively; they were archived:
  - `.cleanup_archive/round5a_tuning_splitA_r5_v1_anchorload_partial_*`
  - `.cleanup_archive/round5a_tuning_splitA_r5_v2_partial_*`
  - corresponding archived logs.
- Active results/reports kept in canonical `runs/` and `reports/`.

## 8) What This Round Validates
- Validation success:
  - held-out regime threshold exists (`~600`) for `nofallback` vs `hard_cap`.
  - same-cost framing with total-token accounting is operationally reliable.
- Not yet validated:
  - dynamic branch (`forcecontinue`) strictly improving over strong static probe baseline.
  - parse-fail neutrality across methods in low-budget regime.

## 9) Recommended Next Round (Actionable)
- Keep held-out protocol unchanged; only method internals change.
- For controller low-T robustness:
  - enforce stronger deterministic final formatter in continue-solve path,
  - reserve parse-repair budget more aggressively for controller branches,
  - add two-stage repair for controller only **or** apply the same stronger formatter to all methods for symmetry.
- For dynamic-gain proof:
  - sweep force-continue threshold on Split A only, then lock one value for held-out.
  - include direct `nofallback` vs `forcecontinue` paired bootstrap table for `Δacc`, `Δincoh`.
