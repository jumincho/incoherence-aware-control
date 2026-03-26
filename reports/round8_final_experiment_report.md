# Round8 Final Experiment Report

- Generated at: `2026-03-02 11:51:34 UTC`
- Runs: A3=`round8a_tuning_splitA3_r3_v1`, B3=`round8b_heldout_splitB3_r5_v1`, C=`round8c_mmlu_repro_r3_v1`
- Selected adaptive from A3: `probe_adaptive_k_t67`
- hard_cap_matched map: `{'300': 86, '400': 80, '500': 117, '600': 173, '750': 242, '900': 285, '1200': 343, '1500': 356}`

## 1) Protocol & Fairness Controls
- New pool + split: `sample_seed=20260421`, A3(0:200) tuning, B3(200:400) held-out.
- Pre-registration + code-lock manifest applied before B3/C.
- Unified token accounting (prompt+output+repair+discard+restart).
- Unified parse policy `P1R`, common formatter, repair reserve `64`, strict reserve enforcement.

## 2) B3 Main Result (held-out GPQA)
- Phase threshold (parse-included): `T*=400`
- Phase threshold (parse-excluded): `T*=400`
- Threshold bootstrap incl: finite_rate=1.000, median=400.0, 95% CI=[300.0, 400.0]
- Threshold bootstrap excl: finite_rate=1.000, median=400.0, 95% CI=[300.0, 400.0]

| Budget | Δacc(nf-hc) | Δincoh(nf-hc) | Δacc(nf-hcm) | Δincoh(nf-hcm) | nf_tok | hc_tok | hcm_tok |
|---|---:|---:|---:|---:|---:|---:|---:|
| 300 | -0.0240 | -0.0102 | -0.0240 | -0.0113 | 148.4 | 137.4 | 137.9 |
| 400 | +0.0940 | -0.1033 | +0.0940 | -0.1033 | 230.6 | 243.1 | 243.1 |
| 500 | +0.0790 | -0.1265 | +0.0700 | -0.1501 | 316.1 | 298.7 | 317.2 |
| 600 | +0.0930 | -0.1120 | +0.0730 | -0.1487 | 389.5 | 316.1 | 354.1 |
| 750 | +0.1080 | -0.1383 | +0.0780 | -0.1803 | 482.2 | 325.5 | 374.2 |
| 900 | +0.0740 | -0.1010 | +0.0400 | -0.1542 | 548.8 | 325.7 | 379.7 |
| 1200 | +0.0820 | -0.1412 | +0.0320 | -0.1947 | 584.4 | 325.0 | 383.0 |
| 1500 | +0.0960 | -0.1287 | +0.0560 | -0.1770 | 611.5 | 325.4 | 382.6 |

## 3) Parse Gating Check (B3, core budgets)
| Budget | max_parse_fail | min_parse_fail | spread | gate(max<=1%) | gate(spread<=1%p) |
|---|---:|---:|---:|---:|---:|
| 400 | 0.0000 | 0.0000 | 0.0000 | 1 | 1 |
| 500 | 0.0000 | 0.0000 | 0.0000 | 1 | 1 |
| 600 | 0.0000 | 0.0000 | 0.0000 | 1 | 1 |
| 750 | 0.0000 | 0.0000 | 0.0000 | 1 | 1 |
| 900 | 0.0000 | 0.0000 | 0.0000 | 1 | 1 |

### nofallback Parse-Fail Reasons (B3)
| Budget | OK | repaired_success | no_budget_for_repair | repair_called_but_failed | unresolved_total |
|---|---:|---:|---:|---:|---:|
| 300 | 477 | 523 | 0 | 0 | 0 |
| 400 | 804 | 196 | 0 | 0 | 0 |
| 500 | 927 | 73 | 0 | 0 | 0 |
| 600 | 926 | 74 | 0 | 0 | 0 |
| 750 | 941 | 59 | 0 | 0 | 0 |
| 900 | 923 | 77 | 0 | 0 | 0 |
| 1200 | 953 | 47 | 0 | 0 | 0 |
| 1500 | 972 | 28 | 0 | 0 | 0 |

## 4) Dynamic vs Probe-Only (B3)
| Budget | probe_adaptive_selected acc/incoh/tok | probe_k4 acc/incoh/tok | probe_k8 acc/incoh/tok |
|---|---|---|---|
| 300 | 0.3320/0.0523/139.1 | 0.3300/0.0523/139.1 | 0.3300/0.0523/139.1 |
| 400 | 0.3610/0.0576/238.1 | 0.3610/0.0616/238.9 | 0.3610/0.0616/238.9 |
| 500 | 0.3550/0.0616/322.2 | 0.3550/0.0616/325.7 | 0.3550/0.0616/325.7 |
| 600 | 0.3490/0.0566/395.1 | 0.3490/0.0566/414.5 | 0.3490/0.0566/414.5 |
| 750 | 0.3530/0.0455/495.8 | 0.3550/0.0469/565.9 | 0.3550/0.0469/568.2 |
| 900 | 0.3510/0.0552/557.9 | 0.3520/0.0543/701.1 | 0.3520/0.0525/715.8 |
| 1200 | 0.3640/0.0630/606.5 | 0.3620/0.0616/917.4 | 0.3620/0.0602/1009.3 |
| 1500 | 0.3520/0.0459/624.2 | 0.3510/0.0465/1051.4 | 0.3490/0.0416/1298.2 |

## 5) 2nd Benchmark Reproduction (MMLU, C)
| Budget | Δacc(nf-hc) | Δincoh(nf-hc) | Δacc(nf-hcm) | Δincoh(nf-hcm) | nf_tok | hc_tok | hcm_tok |
|---|---:|---:|---:|---:|---:|---:|---:|
| 400 | +0.2917 | -0.1331 | +0.2917 | -0.1331 | 237.6 | 183.3 | 183.3 |
| 900 | +0.3133 | -0.1401 | +0.2950 | -0.1506 | 379.6 | 227.8 | 241.1 |
| 1500 | +0.3050 | -0.1458 | +0.2800 | -0.1673 | 404.2 | 228.0 | 242.0 |

## 6) Final Assessment
- `nofallback vs hard_cap` on B3: T>=400에서 accuracy/incoherence 동시 개선이 재현됨.
- `nofallback vs hard_cap_matched` on B3: 중/고 budget에서 incoherence 우세가 유지되며, 일부 구간 정확도도 우세.
- Parse skew: Round7 대비 크게 완화(전 budget parse_fail=0 수준).
- Dynamic>probe-only: acc/incoh 절대우세는 여전히 혼재. 다만 budget별 token-efficiency 포인트는 확인됨.
- 2nd benchmark(MMLU): hard_cap 대비 nofallback의 incoherence 감소 + accuracy 상승이 3 budget 모두 재현됨.

## Artifacts
- [A3 detail](/data2/chojm/incoh-pilot/reports/round8a_tuning_splitA3_r3_v1_detailed_report.md)
- [B3 detail](/data2/chojm/incoh-pilot/reports/round8b_heldout_splitB3_r5_v1_detailed_report.md)
- [C detail](/data2/chojm/incoh-pilot/reports/round8c_mmlu_repro_r3_v1_detailed_report.md)
- [Round8 config patch](/data2/chojm/incoh-pilot/reports/round8_adaptive_and_matched_config.json)
- [Round8 code lock](/data2/chojm/incoh-pilot/reports/round8_code_lock_manifest.sha256)
