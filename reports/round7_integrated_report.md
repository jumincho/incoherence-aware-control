# Round7 Integrated Report

## Runs
- A": `round7a_tuning_splitA2_r3_v1`
- B": `round7b_heldout_splitB2_r5_v1`
- Adaptive selected on A": `probe_adaptive_k_t67`

## B" nofallback vs hard_cap
| Budget | Δacc | Δincoh | hc_acc | nf_acc | hc_incoh | nf_incoh | hc_tok | nf_tok | hc_parse | nf_parse |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 300 | -0.0010 | +0.0051 | 0.3270 | 0.3260 | 0.1584 | 0.1635 | 203.0 | 209.5 | 0.0100 | 0.0050 |
| 400 | +0.0510 | -0.0822 | 0.2910 | 0.3420 | 0.1647 | 0.0825 | 282.8 | 283.9 | 0.0050 | 0.0180 |
| 500 | +0.0150 | -0.1070 | 0.3220 | 0.3370 | 0.1897 | 0.0826 | 311.0 | 364.0 | 0.0050 | 0.0230 |
| 600 | +0.0500 | -0.1188 | 0.3030 | 0.3530 | 0.1921 | 0.0733 | 317.5 | 438.6 | 0.0000 | 0.0130 |
| 750 | +0.0370 | -0.1417 | 0.3150 | 0.3520 | 0.2099 | 0.0683 | 321.6 | 514.9 | 0.0000 | 0.0200 |
| 900 | +0.0620 | -0.1186 | 0.3060 | 0.3680 | 0.1960 | 0.0774 | 321.9 | 548.7 | 0.0000 | 0.0080 |
| 1200 | +0.0590 | -0.1356 | 0.3030 | 0.3620 | 0.2027 | 0.0671 | 327.1 | 600.2 | 0.0000 | 0.0030 |
| 1500 | +0.0560 | -0.1286 | 0.3000 | 0.3560 | 0.1932 | 0.0645 | 327.0 | 615.2 | 0.0000 | 0.0060 |

## B" Probe Frontier (actual spend)
| Budget | Method | Accuracy | Incoherence | AvgTotalTok | ParseFail |
|---|---|---:|---:|---:|---:|
| 300 | probe_only_fixedk_k4 | 0.3470 | 0.0679 | 207.1 | 0.0200 |
| 300 | probe_only_fixedk_k8 | 0.3470 | 0.0679 | 207.1 | 0.0200 |
| 300 | probe_adaptive_k_selected | 0.3450 | 0.0672 | 207.1 | 0.0220 |
| 400 | probe_adaptive_k_selected | 0.3330 | 0.0759 | 289.2 | 0.0100 |
| 400 | probe_only_fixedk_k4 | 0.3330 | 0.0759 | 290.4 | 0.0100 |
| 400 | probe_only_fixedk_k8 | 0.3330 | 0.0759 | 290.4 | 0.0100 |
| 500 | probe_adaptive_k_selected | 0.3470 | 0.0661 | 372.4 | 0.0000 |
| 500 | probe_only_fixedk_k4 | 0.3470 | 0.0661 | 382.0 | 0.0000 |
| 500 | probe_only_fixedk_k8 | 0.3470 | 0.0661 | 382.0 | 0.0000 |
| 600 | probe_adaptive_k_selected | 0.3450 | 0.0688 | 443.8 | 0.0000 |
| 600 | probe_only_fixedk_k4 | 0.3450 | 0.0688 | 473.1 | 0.0000 |
| 600 | probe_only_fixedk_k8 | 0.3450 | 0.0688 | 473.5 | 0.0000 |
| 750 | probe_adaptive_k_selected | 0.3600 | 0.0689 | 523.9 | 0.0000 |
| 750 | probe_only_fixedk_k4 | 0.3600 | 0.0689 | 617.4 | 0.0000 |
| 750 | probe_only_fixedk_k8 | 0.3600 | 0.0689 | 622.2 | 0.0000 |
| 900 | probe_adaptive_k_selected | 0.3520 | 0.0693 | 575.2 | 0.0000 |
| 900 | probe_only_fixedk_k4 | 0.3520 | 0.0706 | 748.0 | 0.0000 |
| 900 | probe_only_fixedk_k8 | 0.3520 | 0.0693 | 768.9 | 0.0000 |
| 1200 | probe_adaptive_k_selected | 0.3540 | 0.0639 | 626.1 | 0.0000 |
| 1200 | probe_only_fixedk_k4 | 0.3560 | 0.0625 | 964.2 | 0.0000 |
| 1200 | probe_only_fixedk_k8 | 0.3570 | 0.0570 | 1071.1 | 0.0000 |
| 1500 | probe_adaptive_k_selected | 0.3600 | 0.0661 | 650.0 | 0.0000 |
| 1500 | probe_only_fixedk_k4 | 0.3620 | 0.0556 | 1072.8 | 0.0000 |
| 1500 | probe_only_fixedk_k8 | 0.3650 | 0.0643 | 1352.3 | 0.0000 |

## Artifacts
- A report: `/data2/chojm/incoh-pilot/reports/round7a_tuning_splitA2_r3_v1_detailed_report.md`
- B report: `/data2/chojm/incoh-pilot/reports/round7b_heldout_splitB2_r5_v1_detailed_report.md`
- Code lock: `/data2/chojm/incoh-pilot/reports/round7_code_lock_manifest.sha256`
