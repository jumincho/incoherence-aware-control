# Round7 Final Experiment Report

## 1. Objective and Protocol
- Objective: verify regime-aware incoherence control under strengthened fairness constraints, then test dynamic probing gain on held-out.
- Data protocol: new pool with `sample_seed=20260407`, split into A"(tuning 200) and B"(held-out 200).
- Parse policy: `P1R`, common formatter/repair path, repair reserve `48` tokens, unified total-token accounting.
- Pre-registration/code-lock artifacts are preserved for Round7.

## 2. Run Reliability
- A" run `round7a_tuning_splitA2_r3_v1`: completed `38400` records, hard fail `0`, parse fail `126` (0.3281%), repair success `2465/2465` (100.00%).
- B" run `round7b_heldout_splitB2_r5_v1`: completed `40000` records, hard fail `0`, parse fail `208` (0.5200%), repair success `2213/2213` (100.00%).

## 3. A" Tuning Outcome
- Selected adaptive method: `probe_adaptive_k_t67`
| Candidate | MeanAcc(400-900) | MeanIncoh(400-900) | MeanParseFail |
|---|---:|---:|---:|
| probe_adaptive_k_t67 | 0.3763 | 0.0507 | 0.0010 |
| probe_adaptive_k_t75 | 0.3763 | 0.0507 | 0.0010 |

## 4. B" Main Result: nofallback vs hard_cap
- Threshold (parse-included) T*: `400`
- Threshold (parse-excluded) T*: `400`
- Threshold bootstrap (hard_cap vs nofallback, parse-included): finite_rate=`1.000`, median=`400.0`, 95% CI=`[300.0, 500.0]`
- Threshold bootstrap (hard_cap vs nofallback, parse-excluded): finite_rate=`1.000`, median=`400.0`, 95% CI=`[300.0, 500.0]`

| Budget | HC Acc | NF Acc | ΔAcc | HC Incoh | NF Incoh | ΔIncoh | HC Tok | NF Tok | HC Parse | NF Parse |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 300 | 0.3270 | 0.3260 | -0.0010 | 0.1584 | 0.1635 | +0.0051 | 203.0 | 209.5 | 0.0100 | 0.0050 |
| 400 | 0.2910 | 0.3420 | +0.0510 | 0.1647 | 0.0825 | -0.0822 | 282.8 | 283.9 | 0.0050 | 0.0180 |
| 500 | 0.3220 | 0.3370 | +0.0150 | 0.1897 | 0.0826 | -0.1070 | 311.0 | 364.0 | 0.0050 | 0.0230 |
| 600 | 0.3030 | 0.3530 | +0.0500 | 0.1921 | 0.0733 | -0.1188 | 317.5 | 438.6 | 0.0000 | 0.0130 |
| 750 | 0.3150 | 0.3520 | +0.0370 | 0.2099 | 0.0683 | -0.1417 | 321.6 | 514.9 | 0.0000 | 0.0200 |
| 900 | 0.3060 | 0.3680 | +0.0620 | 0.1960 | 0.0774 | -0.1186 | 321.9 | 548.7 | 0.0000 | 0.0080 |
| 1200 | 0.3030 | 0.3620 | +0.0590 | 0.2027 | 0.0671 | -0.1356 | 327.1 | 600.2 | 0.0000 | 0.0030 |
| 1500 | 0.3000 | 0.3560 | +0.0560 | 0.1932 | 0.0645 | -0.1286 | 327.0 | 615.2 | 0.0000 | 0.0060 |

Interpretation:
- T=300: nofallback is not better (Δincoh +0.0051, Δacc -0.0010).
- T>=400: nofallback consistently shows lower incoherence than hard_cap with non-negative accuracy deltas in this held-out run.

## 5. Dynamic Gain Check: Adaptive vs Probe-Only Frontier
| Budget | Adapt Acc | Probe(k4) Acc | ΔAcc | Adapt Incoh | Probe(k4) Incoh | ΔIncoh | Adapt Tok | Probe(k4) Tok |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 300 | 0.3450 | 0.3470 | -0.0020 | 0.0672 | 0.0679 | -0.0007 | 207.1 | 207.1 |
| 400 | 0.3330 | 0.3330 | +0.0000 | 0.0759 | 0.0759 | +0.0000 | 289.2 | 290.4 |
| 500 | 0.3470 | 0.3470 | +0.0000 | 0.0661 | 0.0661 | +0.0000 | 372.4 | 382.0 |
| 600 | 0.3450 | 0.3450 | +0.0000 | 0.0688 | 0.0688 | +0.0000 | 443.8 | 473.1 |
| 750 | 0.3600 | 0.3600 | +0.0000 | 0.0689 | 0.0689 | +0.0000 | 523.9 | 617.4 |
| 900 | 0.3520 | 0.3520 | +0.0000 | 0.0693 | 0.0706 | -0.0013 | 575.2 | 748.0 |
| 1200 | 0.3540 | 0.3560 | -0.0020 | 0.0639 | 0.0625 | +0.0014 | 626.1 | 964.2 |
| 1500 | 0.3600 | 0.3620 | -0.0020 | 0.0661 | 0.0556 | +0.0105 | 650.0 | 1072.8 |

Interpretation:
- Adaptive is token-efficient versus fixed k4 at all budgets (always lower avg tokens).
- Accuracy/Incoherence gains are mixed; no universal Pareto dominance over probe-only-k4 is established.

## 6. Parse-Fail Gating (B")
Rule: `max(parse_fail)<=1%` and `spread<=1%p` for budget-level claim safety.
| Budget | Max ParseFail | Min ParseFail | Spread | Gate(max<=1%) | Gate(spread<=1%p) |
|---|---:|---:|---:|---:|---:|
| 300 | 0.0220 | 0.0050 | 0.0170 | 0 | 0 |
| 400 | 0.0180 | 0.0050 | 0.0130 | 0 | 0 |
| 500 | 0.0230 | 0.0000 | 0.0230 | 0 | 0 |
| 600 | 0.0130 | 0.0000 | 0.0130 | 0 | 0 |
| 750 | 0.0200 | 0.0000 | 0.0200 | 0 | 0 |
| 900 | 0.0080 | 0.0000 | 0.0080 | 1 | 1 |
| 1200 | 0.0030 | 0.0000 | 0.0030 | 1 | 1 |
| 1500 | 0.0060 | 0.0000 | 0.0060 | 1 | 1 |

- Parse-gating safe budgets: `[900, 1200, 1500]`
- Therefore, strongest fairness-safe claims should prioritize high budgets (>=900) in this run.

## 7. Final Conclusion
- Confirmed on held-out: regime-aware nofallback reduces incoherence versus hard_cap from mid budgets onward (T>=400), with positive or neutral accuracy deltas in this run.
- Not confirmed as universal: adaptive probing does not strictly dominate probe-only frontier on both accuracy and incoherence, though it is more token-efficient.
- Remaining caution: parse-fail skew still exists at lower budgets; gating marks low/mid budgets as less claim-safe.

## 8. Artifacts
- A" detailed: `/data2/chojm/incoh-pilot/reports/round7a_tuning_splitA2_r3_v1_detailed_report.md`
- B" detailed: `/data2/chojm/incoh-pilot/reports/round7b_heldout_splitB2_r5_v1_detailed_report.md`
- This final report: `/data2/chojm/incoh-pilot/reports/round7_final_experiment_report.md`
- Pre-registration: `/data2/chojm/incoh-pilot/reports/round7_preregistration.md`
- Code lock: `/data2/chojm/incoh-pilot/reports/round7_code_lock_manifest.sha256`
