# Round6 A/B Integrated Report (A′ Tuning + B′ Held-out)

## 1) Scope and Goal
- Goal: Apply Round5 feedback with stronger fairness controls, then verify on new held-out split whether regime transition and dynamic-control gains hold.
- Round6-A: tuning on A′ (200 questions, R=3) to select adaptive probe variant.
- Round6-B: held-out on B′ (200 questions, R=5) with fixed policy.

## 2) Fairness Controls Implemented
- New sample pool and split protocol: A′/B′ from a new 400-question pool (`sample_seed=20260328`).
- Pre-registration and code-lock maintained for Round6 runs.
- Unified accounting: total tokens include prompt/output/repair/discard/restart.
- Unified parse policy across methods: `P1R`.
- Common formatter path in code (`Final Answer: X`) + repair reserve (`repair_min_remaining_tokens=32`).
- Method family for fairness test:
  - `hard_cap`
  - `probe_only_fixedk`
  - `probe_adaptive_k_*` (A′), then `probe_adaptive_k_selected` (B′)
  - `ours_controller_v2_nofallback`

## 3) Round6-A (A′ Tuning) Summary
Run: `/data2/chojm/incoh-pilot/runs/round6a_tuning_splitAprime_r3_v3`
Report: `/data2/chojm/incoh-pilot/reports/round6a_tuning_splitAprime_r3_v3_detailed_report.md`

Reliability:
- Records: 32,400
- Hard fail: 0
- Parse fail: 1.5617% (506)
- Repair success: 5475/5981 (91.54%)

Key findings:
- nofallback vs hard_cap threshold bootstrap:
  - finite_rate = 0.950
  - median T* = 600
  - 95% CI = [400, 1500]
- nofallback beat hard_cap with both `Δincoh<0` and `Δacc>0` at T=1200, 1500.
- Low spend remained vulnerable (notably T=300).
- `probe_adaptive_k_t67/t75/t80` were near-identical on A′; selected `t67` by tie-break rule (higher-T incoh stability preference).

## 4) Round6-B (B′ Held-out) Summary
Run: `/data2/chojm/incoh-pilot/runs/round6b_heldout_splitBprime_r5_v1`
Report: `/data2/chojm/incoh-pilot/reports/round6b_heldout_splitBprime_r5_v1_detailed_report.md`

Reliability:
- Records: 36,000
- Hard fail: 0
- Parse fail: 1.1750% (423)
- Repair success: 5964/6387 (93.38%)
- Duration: 152.87 min

### 4.1 Regime/Threshold (held-out)
- nofallback beats hard_cap on incoherence with no accuracy loss first at T=400.
- Threshold bootstrap (hard_cap vs nofallback):
  - finite_rate = 1.000
  - median T* = 400
  - 95% CI = [200, 900]

Interpretation:
- Transition region is held-out reproducible.
- Compared to Round5 narrative, threshold moved but remains in low-mid spend regime.

### 4.2 nofallback vs hard_cap (held-out deltas)
- T=200: Δacc +0.001, Δincoh +0.0038 (fail)
- T=300: Δacc -0.094, Δincoh +0.0207 (clear fail)
- T=400: Δacc +0.004, Δincoh -0.0459
- T=500: Δacc +0.003, Δincoh -0.0258
- T=600: Δacc -0.002, Δincoh -0.0224
- T=750: Δacc +0.015, Δincoh -0.0143
- T=900: Δacc +0.022, Δincoh -0.0385
- T=1200: Δacc +0.029, Δincoh -0.0303
- T=1500: Δacc +0.027, Δincoh -0.0442

Takeaway:
- From T>=400, nofallback consistently reduces incoherence vs hard_cap.
- Accuracy is mostly better vs hard_cap except a tiny drop at T=600.

### 4.3 Dynamic gain check: probe_adaptive_k_selected vs probe_only_fixedk
Held-out deltas (PA - PO):
- T=200: Δacc -0.005, Δincoh +0.0013
- T=300: Δacc +0.008, Δincoh -0.0079
- T=400: Δacc +0.003, Δincoh +0.0098
- T=500: Δacc -0.014, Δincoh -0.0062
- T=600: Δacc +0.006, Δincoh +0.0056
- T=750: Δacc -0.008, Δincoh -0.0064
- T=900: Δacc -0.010, Δincoh +0.0051
- T=1200: Δacc -0.014, Δincoh -0.0177
- T=1500: Δacc -0.001, Δincoh -0.0028

Takeaway:
- Adaptive probing does not show a clean, consistent Pareto gain over probe_only.
- Gains are budget-dependent and mixed; dynamic control benefit is not yet definitively established.

### 4.4 Parse fairness and method×T skew (held-out)
Key method×T parse-fail rates:
- nofallback: 2.5% (T=200), 13.0% (T=300), ~0.8-1.9% for T>=400
- hard_cap: <=1.5% at low T, 0% for most T>=500
- probe_only: 3.0% at T=300, mostly 0% for T>=500
- probe_adaptive: 4.5% at T=300, mostly <=0.8% for T>=500

Interpretation:
- The major remaining fairness risk is controller-side parse skew at T=300 (and mildly T=200).
- For T>=500, parse skew is much smaller but still not perfectly equalized.

### 4.5 Cost reality (held-out)
Representative average total tokens by method:
- T=900: hard_cap 270.9, nofallback 533.5, probe_only 722.3, adaptive 588.3
- T=1500: hard_cap 276.1, nofallback 578.9, probe_only 1035.1, adaptive 647.0

Interpretation:
- nofallback sits between hard_cap and probe-only in spend.
- At higher T, nofallback achieves much lower incoherence than hard_cap while using substantially fewer tokens than probe-only.

## 5) Consolidated Conclusion
What is confirmed:
- Held-out regime transition is real.
- nofallback provides robust incoherence reduction vs hard_cap from T>=400, with mostly non-negative (often positive) accuracy deltas.

What is not confirmed yet:
- Dynamic control does not yet show a stable, dominant gain over probe-only/adaptive-probe baselines across budgets.

Main unresolved risk:
- Parse-fail skew at low T (especially nofallback at T=300) can still confound conclusions.

## 6) Actions for Next Round (execution-oriented)
1. Fix low-T parse skew first:
- Increase guaranteed repair reserve (e.g., 48) for all methods.
- Add final-output post-formatter uniformly on all terminal paths (including continue-solve branches).
- Add method×T parse-fail gating criterion before claiming policy gains.

2. Isolate dynamic policy gain with stricter ablation:
- `probe_only_fixedk`
- `probe_adaptive_k`
- `nofallback` with forced minimum continue ratio (small, controlled)
- Evaluate only on T in {400, 500, 600, 750, 900} where regime is active.

3. Keep held-out hygiene:
- Since B′ is now observed, any further policy change requires a fresh held-out split (C or B′′).

## 7) Artifact Paths
- Round6-A run: `/data2/chojm/incoh-pilot/runs/round6a_tuning_splitAprime_r3_v3`
- Round6-A report: `/data2/chojm/incoh-pilot/reports/round6a_tuning_splitAprime_r3_v3_detailed_report.md`
- Round6-B run: `/data2/chojm/incoh-pilot/runs/round6b_heldout_splitBprime_r5_v1`
- Round6-B report: `/data2/chojm/incoh-pilot/reports/round6b_heldout_splitBprime_r5_v1_detailed_report.md`
- Integrated report (this file): `/data2/chojm/incoh-pilot/reports/round6_ab_integrated_report.md`
