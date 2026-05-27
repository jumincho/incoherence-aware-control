#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
. .venv/bin/activate

RUN7A="round7a_tuning_splitA2_r3_v1"
RUN7B="round7b_heldout_splitB2_r5_v1"
CFG7A="configs/round7a_tuning_splitA2.yaml"
CFG7B="configs/round7b_heldout_splitB2.yaml"

wait_done_shards() {
  local run_id="$1"
  while true; do
    done_ct=$(python - <<PY
import glob,json
p=glob.glob('runs/${run_id}/status_shard*.json')
print(sum(1 for x in p if json.load(open(x)).get('done')) if p else 0)
PY
)
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ${run_id} done_shards=${done_ct}"
    if [[ "$done_ct" == "8" ]]; then
      break
    fi
    sleep 120
  done
}

# 1) Wait Round7-A complete and analyze
wait_done_shards "$RUN7A"
python -m src.analyze_hotmess_style --run-dir "runs/${RUN7A}"
python -m src.report_spend_sweep --run-dir "runs/${RUN7A}" --out "reports/${RUN7A}_detailed_report.md"

# 2) Adaptive selection from A'' and patch B'' config
python - <<'PY'
import json, yaml
from pathlib import Path
run='round7a_tuning_splitA2_r3_v1'
analysis=json.loads(Path(f'runs/{run}/analysis_summary_round2.json').read_text())
summary=analysis['summary_by_budget']
budgets=['400','500','600','750','900']
# Rule: max mean acc, tie min mean incoh, tie min mean parse_fail
cands=[m for m in summary[budgets[0]].keys() if m.startswith('probe_adaptive_k_')]
rows=[]
for m in cands:
    acc=[]; incoh=[]; pf=[]
    for b in budgets:
        s=summary[b][m]
        acc.append(float(s['accuracy']))
        incoh.append(float(s['incoherence']))
        pf.append(float(s['parse_fail_rate']))
    rows.append((m,sum(acc)/len(acc),sum(incoh)/len(incoh),sum(pf)/len(pf)))
rows.sort(key=lambda x:(-x[1],x[2],x[3],x[0]))
best=rows[0][0]
out={'selected_method':best,'candidates':[{'method':m,'mean_acc':a,'mean_incoh':i,'mean_parse_fail':p} for m,a,i,p in rows]}
Path(f'runs/{run}/adaptive_selection.json').write_text(json.dumps(out,indent=2))

cfg_path=Path('configs/round7b_heldout_splitB2.yaml')
cfg=yaml.safe_load(cfg_path.read_text())
src=cfg['method_params'][best]
cfg['method_params']['probe_adaptive_k_selected']=dict(src)
cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True))
print(json.dumps({'selected':best,'patched_config':str(cfg_path)},indent=2))
PY

# 3) Code lock manifest before B''
sha256sum $(find src configs tests -type f | sort) > reports/round7_code_lock_manifest.sha256

# 4) Launch Round7-B shards
mkdir -p "runs/${RUN7B}/logs"
pids=()
for i in 0 1 2 3 4 5 6 7; do
  python -m src.run_pilot --config "$CFG7B" --gpu-shard "${i}/8" --run-id "$RUN7B" > "runs/${RUN7B}/logs/shard${i}.log" 2>&1 &
  pids+=("$!")
  echo "launched shard ${i} pid=${pids[-1]}"
done
for p in "${pids[@]}"; do
  wait "$p"
done

# 5) Analyze Round7-B
python -m src.analyze_hotmess_style --run-dir "runs/${RUN7B}"
python -m src.report_spend_sweep --run-dir "runs/${RUN7B}" --out "reports/${RUN7B}_detailed_report.md"

# 6) Integrated report
python - <<'PY'
import json
from pathlib import Path
ra='round7a_tuning_splitA2_r3_v1'
rb='round7b_heldout_splitB2_r5_v1'
a=json.loads(Path(f'runs/{ra}/analysis_summary_round2.json').read_text())
b=json.loads(Path(f'runs/{rb}/analysis_summary_round2.json').read_text())
sel=json.loads(Path(f'runs/{ra}/adaptive_selection.json').read_text())

def line(summary,b,m):
    s=summary[str(b)][m]
    return s['accuracy'],s['incoherence'],s['avg_total_tokens'],s['parse_fail_rate']

budgets=[300,400,500,600,750,900,1200,1500]
lines=[]
lines.append('# Round7 Integrated Report')
lines.append('')
lines.append(f"- Round7-A run: `{ra}`")
lines.append(f"- Round7-B run: `{rb}`")
lines.append(f"- Selected adaptive: `{sel['selected_method']}`")
lines.append('')
lines.append('## Held-out Core (B\" nofallback vs hard_cap)')
lines.append('| Budget | Δacc(nf-hc) | Δincoh(nf-hc) | nf_tok | hc_tok | nf_parse | hc_parse |')
lines.append('|---|---:|---:|---:|---:|---:|---:|')
for bd in budgets:
    sb=b['summary_by_budget'][str(bd)]
    hc=sb['hard_cap']; nf=sb['ours_controller_v2_nofallback']
    lines.append(f"| {bd} | {nf['accuracy']-hc['accuracy']:+.4f} | {nf['incoherence']-hc['incoherence']:+.4f} | {nf['avg_total_tokens']:.1f} | {hc['avg_total_tokens']:.1f} | {nf['parse_fail_rate']:.4f} | {hc['parse_fail_rate']:.4f} |")
lines.append('')
lines.append('## Held-out Probe Frontier (B\")')
lines.append('| Budget | Method | Accuracy | Incoherence | AvgTotalTok | ParseFail |')
lines.append('|---|---|---:|---:|---:|---:|')
for bd in budgets:
    sb=b['summary_by_budget'][str(bd)]
    for m in sorted([k for k in sb.keys() if k.startswith('probe_only_fixedk_') or k.startswith('probe_adaptive_k')], key=lambda x: sb[x]['avg_total_tokens']):
        s=sb[m]
        lines.append(f"| {bd} | {m} | {s['accuracy']:.4f} | {s['incoherence']:.4f} | {s['avg_total_tokens']:.1f} | {s['parse_fail_rate']:.4f} |")
lines.append('')
lines.append('## Artifacts')
lines.append(f"- A detailed: `reports/{ra}_detailed_report.md`")
lines.append(f"- B detailed: `reports/{rb}_detailed_report.md`")
lines.append(f"- Selection: `runs/{ra}/adaptive_selection.json`")
lines.append(f"- Code lock: `reports/round7_code_lock_manifest.sha256`")
Path('reports/round7_integrated_report.md').write_text('\n'.join(lines)+'\n')
print('reports/round7_integrated_report.md')
PY

echo "ROUND7_PIPELINE_DONE"
