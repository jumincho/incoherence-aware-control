# Round7 Progress Report

## Status
- Round7-A (A") completed: `yes`
- Round7-B (B") completed shards: `0/8`
- Round7-B records processed: `11889/40000`
- Round7-B current parse-fail count: `75`

## Round7-A Selection Result
- Selected adaptive method: `probe_adaptive_k_t67`
| Candidate | MeanAcc (400-900) | MeanIncoh (400-900) | MeanParseFail |
|---|---:|---:|---:|
| probe_adaptive_k_t67 | 0.3763 | 0.0507 | 0.0010 |
| probe_adaptive_k_t75 | 0.3763 | 0.0507 | 0.0010 |

## Round7-A Core Snapshot (hard_cap vs nofallback)
| Budget | HC Acc | NF Acc | ΔAcc | HC Incoh | NF Incoh | ΔIncoh | HC Tok | NF Tok | HC Parse | NF Parse |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 300 | 0.2717 | 0.2533 | -0.0183 | 0.1030 | 0.0982 | -0.0048 | 202.4 | 207.3 | 0.0050 | 0.0100 |
| 400 | 0.2683 | 0.3383 | +0.0700 | 0.1245 | 0.0478 | -0.0766 | 263.9 | 274.9 | 0.0100 | 0.0317 |
| 500 | 0.2767 | 0.3950 | +0.1183 | 0.1495 | 0.0442 | -0.1053 | 295.2 | 358.5 | 0.0050 | 0.0117 |
| 600 | 0.2717 | 0.3983 | +0.1267 | 0.1462 | 0.0501 | -0.0961 | 314.1 | 437.8 | 0.0000 | 0.0167 |
| 750 | 0.2800 | 0.3767 | +0.0967 | 0.1768 | 0.0557 | -0.1211 | 322.1 | 498.7 | 0.0000 | 0.0200 |
| 900 | 0.2483 | 0.3833 | +0.1350 | 0.1648 | 0.0597 | -0.1051 | 327.0 | 545.4 | 0.0000 | 0.0083 |
| 1200 | 0.2650 | 0.3767 | +0.1117 | 0.1654 | 0.0484 | -0.1171 | 337.3 | 593.1 | 0.0000 | 0.0017 |
| 1500 | 0.2450 | 0.3850 | +0.1400 | 0.1630 | 0.0538 | -0.1092 | 337.4 | 619.6 | 0.0000 | 0.0000 |

## Artifacts
- A detailed report: `/data2/chojm/incoh-pilot/reports/round7a_tuning_splitA2_r3_v1_detailed_report.md`
- B detailed report (auto after completion): `/data2/chojm/incoh-pilot/reports/round7b_heldout_splitB2_r5_v1_detailed_report.md`
- Final integrated report (auto after completion): `/data2/chojm/incoh-pilot/reports/round7_integrated_report.md`
- Code lock manifest: `/data2/chojm/incoh-pilot/reports/round7_code_lock_manifest.sha256`
