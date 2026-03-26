#!/usr/bin/env bash
set -euo pipefail
cd /data2/chojm/incoh-pilot
. .venv/bin/activate
RUN7A='round7a_tuning_splitA2_r3_v1'
RUN7B='round7b_heldout_splitB2_r5_v1'
while true; do
  done_ct=$(python - <<'PY'
import glob,json
p=glob.glob('runs/round7b_heldout_splitB2_r5_v1/status_shard*.json')
print(sum(1 for x in p if json.load(open(x)).get('done')) if p else 0)
PY
)
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] finalize-round7 wait done_shards=${done_ct}"
  if [[ "$done_ct" == "8" ]]; then break; fi
  sleep 180
 done
python -m src.analyze_hotmess_style --run-dir runs/${RUN7B}
python -m src.report_spend_sweep --run-dir runs/${RUN7B} --out reports/${RUN7B}_detailed_report.md
python - <<'PY'
import json
from pathlib import Path
ra='round7a_tuning_splitA2_r3_v1'
rb='round7b_heldout_splitB2_r5_v1'
a=json.loads(Path(f'runs/{ra}/analysis_summary_round2.json').read_text())
b=json.loads(Path(f'runs/{rb}/analysis_summary_round2.json').read_text())
sel=json.loads(Path(f'runs/{ra}/adaptive_selection.json').read_text())
budgets=[300,400,500,600,750,900,1200,1500]
lines=[]
lines.append('# Round7 Integrated Report')
lines.append('')
lines.append('## Runs')
lines.append(f"- A\": `{ra}`")
lines.append(f"- B\": `{rb}`")
lines.append(f"- Adaptive selected on A\": `{sel['selected_method']}`")
lines.append('')
lines.append('## B\" nofallback vs hard_cap')
lines.append('| Budget | Δacc | Δincoh | hc_acc | nf_acc | hc_incoh | nf_incoh | hc_tok | nf_tok | hc_parse | nf_parse |')
lines.append('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for bd in budgets:
  sb=b['summary_by_budget'][str(bd)]
  hc=sb['hard_cap']; nf=sb['ours_controller_v2_nofallback']
  lines.append(f"| {bd} | {nf['accuracy']-hc['accuracy']:+.4f} | {nf['incoherence']-hc['incoherence']:+.4f} | {hc['accuracy']:.4f} | {nf['accuracy']:.4f} | {hc['incoherence']:.4f} | {nf['incoherence']:.4f} | {hc['avg_total_tokens']:.1f} | {nf['avg_total_tokens']:.1f} | {hc['parse_fail_rate']:.4f} | {nf['parse_fail_rate']:.4f} |")
lines.append('')
lines.append('## B\" Probe Frontier (actual spend)')
lines.append('| Budget | Method | Accuracy | Incoherence | AvgTotalTok | ParseFail |')
lines.append('|---|---|---:|---:|---:|---:|')
for bd in budgets:
  sb=b['summary_by_budget'][str(bd)]
  methods=[m for m in sb.keys() if m.startswith('probe_only_fixedk') or m.startswith('probe_adaptive_k')]
  for m in sorted(methods,key=lambda x: sb[x]['avg_total_tokens']):
    s=sb[m]
    lines.append(f"| {bd} | {m} | {s['accuracy']:.4f} | {s['incoherence']:.4f} | {s['avg_total_tokens']:.1f} | {s['parse_fail_rate']:.4f} |")
lines.append('')
lines.append('## Artifacts')
lines.append(f"- A report: `/data2/chojm/incoh-pilot/reports/{ra}_detailed_report.md`")
lines.append(f"- B report: `/data2/chojm/incoh-pilot/reports/{rb}_detailed_report.md`")
lines.append('- Code lock: `/data2/chojm/incoh-pilot/reports/round7_code_lock_manifest.sha256`')
Path('reports/round7_integrated_report.md').write_text('\n'.join(lines)+'\n')
print('/data2/chojm/incoh-pilot/reports/round7_integrated_report.md')
PY

echo 'ROUND7_FINALIZED'
