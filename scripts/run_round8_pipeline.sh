#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
. .venv/bin/activate

RUN_SMOKE="round8smoke_format_splitA3_r1_v1"
RUN_A3="round8a_tuning_splitA3_r3_v1"
RUN_B3="round8b_heldout_splitB3_r5_v1"
RUN_C="round8c_mmlu_repro_r3_v1"

CFG_SMOKE="configs/round8a_format_smoke_splitA3.yaml"
CFG_A3="configs/round8a_tuning_splitA3.yaml"
CFG_B3="configs/round8b_heldout_splitB3.yaml"
CFG_C="configs/round8c_mmlu_repro.yaml"

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "HF_TOKEN is not set" >&2
  exit 1
fi

launch_shards_wait() {
  local cfg="$1"
  local run_id="$2"
  local extra_args="${3:-}"
  mkdir -p "runs/${run_id}/logs"
  local pids=()
  for i in 0 1 2 3 4 5 6 7; do
    python -m src.run_pilot --config "$cfg" --gpu-shard "${i}/8" --run-id "$run_id" ${extra_args} > "runs/${run_id}/logs/shard${i}.log" 2>&1 &
    pids+=("$!")
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] launched ${run_id} shard=${i} pid=${pids[-1]}"
    sleep 1
  done
  for p in "${pids[@]}"; do
    wait "$p"
  done
}

analyze_and_report() {
  local run_id="$1"
  python -m src.analyze_hotmess_style --run-dir "runs/${run_id}"
  python -m src.report_spend_sweep --run-dir "runs/${run_id}" --out "reports/${run_id}_detailed_report.md"
}

# 0) smoke: parse-gating readiness with small workload
launch_shards_wait "$CFG_SMOKE" "$RUN_SMOKE" "--max-questions 50 --max-trials 1"
analyze_and_report "$RUN_SMOKE"

# 1) A3 tuning
launch_shards_wait "$CFG_A3" "$RUN_A3"
analyze_and_report "$RUN_A3"

# 2) select adaptive + derive hard_cap_matched cap map from A3
python - <<'PY'
import json, yaml
from pathlib import Path
run='round8a_tuning_splitA3_r3_v1'
summary=json.loads(Path(f'runs/{run}/analysis_summary_round2.json').read_text())['summary_by_budget']
budgets=[300,400,500,600,750,900,1200,1500]
# Adaptive selection on transition-focused budgets
focus=['400','500','600','750','900']
methods=[m for m in summary[focus[0]].keys() if m.startswith('probe_adaptive_k_')]
rows=[]
for m in methods:
    mean_acc=sum(float(summary[b][m]['accuracy']) for b in focus)/len(focus)
    mean_incoh=sum(float(summary[b][m]['incoherence']) for b in focus)/len(focus)
    mean_parse=sum(float(summary[b][m]['parse_fail_rate']) for b in focus)/len(focus)
    rows.append((m,mean_acc,mean_incoh,mean_parse))
rows.sort(key=lambda x:(-x[1],x[2],x[3],x[0]))
selected=rows[0][0]
Path(f'runs/{run}/adaptive_selection_round8.json').write_text(json.dumps({'selected':selected,'rows':[{'method':m,'mean_acc':a,'mean_incoh':i,'mean_parse':p} for m,a,i,p in rows]},indent=2))

# compute-matched hard_cap map: cap = base_cap + (nf_avg_total - hc_avg_total), clipped by budget-reserve
base_cap=80
reserve=64
cap_map={}
for b in budgets:
    sb=summary[str(b)]
    nf=float(sb['ours_controller_v2_nofallback']['avg_total_tokens'])
    hc=float(sb['hard_cap']['avg_total_tokens'])
    cap=round(base_cap + max(0.0,nf-hc))
    cap=max(24,min(int(cap),int(b)-reserve))
    cap_map[str(b)]=int(cap)

cfg_b=Path('configs/round8b_heldout_splitB3.yaml')
yb=yaml.safe_load(cfg_b.read_text())
yb['method_params']['probe_adaptive_k_selected']=dict(yb['method_params'][selected])
yb['method_params']['hard_cap_matched']['max_new_tokens_by_budget']=cap_map
cfg_b.write_text(yaml.safe_dump(yb, sort_keys=False, allow_unicode=True))

cfg_c=Path('configs/round8c_mmlu_repro.yaml')
yc=yaml.safe_load(cfg_c.read_text())
cap_map_c={k:v for k,v in cap_map.items() if k in {'400','900','1500'}}
yc['method_params']['hard_cap_matched']['max_new_tokens_by_budget']=cap_map_c
cfg_c.write_text(yaml.safe_dump(yc, sort_keys=False, allow_unicode=True))

print(json.dumps({'selected_adaptive':selected,'hard_cap_matched_map_gpqa':cap_map,'hard_cap_matched_map_mmlu':cap_map_c},indent=2))
PY

# 3) code lock before held-out B3 and C
sha256sum $(find src configs tests scripts -type f | sort) > reports/round8_code_lock_manifest.sha256

# 4) B3 held-out
launch_shards_wait "$CFG_B3" "$RUN_B3"
analyze_and_report "$RUN_B3"

# 5) C benchmark (MMLU)
launch_shards_wait "$CFG_C" "$RUN_C"
analyze_and_report "$RUN_C"

# 6) integrated report
python - <<'PY'
import json
from pathlib import Path
run_smoke='round8smoke_format_splitA3_r1_v1'
run_a='round8a_tuning_splitA3_r3_v1'
run_b='round8b_heldout_splitB3_r5_v1'
run_c='round8c_mmlu_repro_r3_v1'
sa=json.loads(Path(f'runs/{run_a}/analysis_summary_round2.json').read_text())
sb=json.loads(Path(f'runs/{run_b}/analysis_summary_round2.json').read_text())
sc=json.loads(Path(f'runs/{run_c}/analysis_summary_round2.json').read_text())
sel=json.loads(Path(f'runs/{run_a}/adaptive_selection_round8.json').read_text())

bud_b=[300,400,500,600,750,900,1200,1500]
bud_c=[400,900,1500]

lines=[]
lines.append('# Round8 Integrated Follow-up Report')
lines.append('')
lines.append('## Runs')
lines.append(f'- smoke: `{run_smoke}`')
lines.append(f'- tuning A3: `{run_a}`')
lines.append(f'- held-out B3: `{run_b}`')
lines.append(f'- 2nd bench C (MMLU): `{run_c}`')
lines.append(f"- selected adaptive: `{sel['selected']}`")
lines.append('')
lines.append('## B3 Core (nofallback vs hard_cap / hard_cap_matched)')
lines.append('| Budget | Δacc(nf-hc) | Δincoh(nf-hc) | Δacc(nf-hcm) | Δincoh(nf-hcm) | tok_nf | tok_hc | tok_hcm |')
lines.append('|---|---:|---:|---:|---:|---:|---:|---:|')
for b in bud_b:
    sbm=sb['summary_by_budget'][str(b)]
    nf=sbm['ours_controller_v2_nofallback']; hc=sbm['hard_cap']; hm=sbm['hard_cap_matched']
    lines.append(f"| {b} | {nf['accuracy']-hc['accuracy']:+.4f} | {nf['incoherence']-hc['incoherence']:+.4f} | {nf['accuracy']-hm['accuracy']:+.4f} | {nf['incoherence']-hm['incoherence']:+.4f} | {nf['avg_total_tokens']:.1f} | {hc['avg_total_tokens']:.1f} | {hm['avg_total_tokens']:.1f} |")
lines.append('')

lines.append('## B3 Parse-Fail Gating (max<=1%, spread<=1%p)')
lines.append('| Budget | max_parse_fail | min_parse_fail | spread | gate_max | gate_spread |')
lines.append('|---|---:|---:|---:|---:|---:|')
rep_b=json.loads(Path(f'runs/{run_b}/analysis_summary_round2.json').read_text())['summary_by_budget']
for b in bud_b:
    vals=[float(v['parse_fail_rate']) for v in rep_b[str(b)].values()]
    mx=max(vals); mn=min(vals); sp=mx-mn
    lines.append(f"| {b} | {mx:.4f} | {mn:.4f} | {sp:.4f} | {int(mx<=0.01)} | {int(sp<=0.01)} |")
lines.append('')

lines.append('## C Benchmark (MMLU) Core')
lines.append('| Budget | Δacc(nf-hc) | Δincoh(nf-hc) | nf_acc | hc_acc | nf_incoh | hc_incoh |')
lines.append('|---|---:|---:|---:|---:|---:|---:|')
for b in bud_c:
    scm=sc['summary_by_budget'][str(b)]
    nf=scm['ours_controller_v2_nofallback']; hc=scm['hard_cap']
    lines.append(f"| {b} | {nf['accuracy']-hc['accuracy']:+.4f} | {nf['incoherence']-hc['incoherence']:+.4f} | {nf['accuracy']:.4f} | {hc['accuracy']:.4f} | {nf['incoherence']:.4f} | {hc['incoherence']:.4f} |")
lines.append('')

lines.append('## Artifacts')
lines.append(f'- `reports/{run_smoke}_detailed_report.md`')
lines.append(f'- `reports/{run_a}_detailed_report.md`')
lines.append(f'- `reports/{run_b}_detailed_report.md`')
lines.append(f'- `reports/{run_c}_detailed_report.md`')
lines.append('- `reports/round8_code_lock_manifest.sha256`')
Path('reports/round8_integrated_followup_report.md').write_text('\n'.join(lines)+'\n')
print('reports/round8_integrated_followup_report.md')
PY

echo "ROUND8_PIPELINE_DONE"
