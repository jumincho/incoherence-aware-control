#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
. .venv/bin/activate

RUN9A="round9a_tuning_splitA9_r3_v1"
RUN9B="round9b_heldout_splitB9_r5_v1"
RUN9C="round9c_mmlu_repro_r3_v1"
RUN9D="round9d_confirm_core_r7_v1"

CFG9A="configs/round9a_tuning_splitA9.yaml"
CFG9B="configs/round9b_heldout_splitB9.yaml"
CFG9C="configs/round9c_mmlu_repro.yaml"
CFG9D="configs/round9d_confirm_core_r7.yaml"

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
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] ${run_id} all shards done"
}

analyze_and_report() {
  local run_id="$1"
  python -m src.analyze_hotmess_style --run-dir "runs/${run_id}"
  python -m src.report_spend_sweep --run-dir "runs/${run_id}" --out "reports/${run_id}_detailed_report.md"
}

# 1) A9 tuning
launch_shards_wait "$CFG9A" "$RUN9A"
analyze_and_report "$RUN9A"

# 2) adaptive selection + hard_cap_matched map patch for B/C/D
python - <<'PY'
import json, yaml
from pathlib import Path

run='round9a_tuning_splitA9_r3_v1'
summary=json.loads(Path(f'runs/{run}/analysis_summary_round2.json').read_text())['summary_by_budget']
focus=['350','400','450','500','600']
cands=[m for m in summary[focus[0]].keys() if m.startswith('probe_adaptive_k_')]
rows=[]
for m in cands:
    acc=sum(float(summary[b][m]['accuracy']) for b in focus)/len(focus)
    incoh=sum(float(summary[b][m]['incoherence']) for b in focus)/len(focus)
    tok=sum(float(summary[b][m]['avg_total_tokens']) for b in focus)/len(focus)
    rows.append((m,acc,incoh,tok))
rows.sort(key=lambda x:(-x[1],x[2],x[3],x[0]))
selected=rows[0][0]

# matched hard-cap token map from v3_nofallback vs hard_cap
base_cap=80
reserve=64
budgets=[300,350,400,450,500,600,900,1500]
cap_map={}
for b in budgets:
    sb=summary[str(b)]
    nf=float(sb['ours_controller_v3_nofallback']['avg_total_tokens'])
    hc=float(sb['hard_cap']['avg_total_tokens'])
    cap=round(base_cap + max(0.0, nf-hc))
    cap=max(24, min(int(cap), int(b)-reserve))
    cap_map[str(b)] = int(cap)

cfgA=yaml.safe_load(Path('configs/round9a_tuning_splitA9.yaml').read_text())
sel_params=dict(cfgA['method_params'][selected])

# patch B
cfgB_path=Path('configs/round9b_heldout_splitB9.yaml')
cfgB=yaml.safe_load(cfgB_path.read_text())
cfgB['method_params']['probe_adaptive_k_selected']=sel_params
cfgB['method_params']['hard_cap_matched']['max_new_tokens_by_budget']=cap_map
cfgB_path.write_text(yaml.safe_dump(cfgB, sort_keys=False, allow_unicode=True))

# patch C
cfgC_path=Path('configs/round9c_mmlu_repro.yaml')
cfgC=yaml.safe_load(cfgC_path.read_text())
cap_map_c={k:v for k,v in cap_map.items() if k in {'400','900','1500'}}
cfgC['method_params']['hard_cap_matched']['max_new_tokens_by_budget']=cap_map_c
cfgC_path.write_text(yaml.safe_dump(cfgC, sort_keys=False, allow_unicode=True))

# patch D
cfgD_path=Path('configs/round9d_confirm_core_r7.yaml')
cfgD=yaml.safe_load(cfgD_path.read_text())
cap_map_d={k:v for k,v in cap_map.items() if k in {'400','500','600'}}
cfgD['method_params']['hard_cap_matched']['max_new_tokens_by_budget']=cap_map_d
cfgD_path.write_text(yaml.safe_dump(cfgD, sort_keys=False, allow_unicode=True))

Path('reports/round9_adaptive_and_matched_config.json').write_text(json.dumps({
  'selected_adaptive': selected,
  'adaptive_candidates': [{'method':m,'mean_acc':a,'mean_incoh':i,'mean_tok':t} for m,a,i,t in rows],
  'hard_cap_matched_map_gpqa': cap_map,
  'hard_cap_matched_map_mmlu': cap_map_c,
  'hard_cap_matched_map_confirm': cap_map_d,
}, indent=2))
print(json.dumps({'selected':selected,'cap_map':cap_map}, indent=2))
PY

# 3) code lock before held-out / repro
sha256sum $(find src configs tests scripts -type f | sort) > reports/round9_code_lock_manifest.sha256

# 4) B9 held-out
launch_shards_wait "$CFG9B" "$RUN9B"
analyze_and_report "$RUN9B"

# 5) D confirm (core budgets R=7)
launch_shards_wait "$CFG9D" "$RUN9D"
analyze_and_report "$RUN9D"

# 6) C second benchmark repro
launch_shards_wait "$CFG9C" "$RUN9C"
analyze_and_report "$RUN9C"

# 7) integrated round9 report
python - <<'PY'
import json
from pathlib import Path

ra='round9a_tuning_splitA9_r3_v1'
rb='round9b_heldout_splitB9_r5_v1'
rc='round9c_mmlu_repro_r3_v1'
rd='round9d_confirm_core_r7_v1'

A=json.loads(Path(f'runs/{ra}/analysis_summary_round2.json').read_text())
B=json.loads(Path(f'runs/{rb}/analysis_summary_round2.json').read_text())
C=json.loads(Path(f'runs/{rc}/analysis_summary_round2.json').read_text())
D=json.loads(Path(f'runs/{rd}/analysis_summary_round2.json').read_text())
sel=json.loads(Path('reports/round9_adaptive_and_matched_config.json').read_text())

bud_b=[300,350,400,450,500,600,900,1500]
bud_core=[400,450,500,600]
bud_c=[400,900,1500]
bud_d=[400,500,600]

sumB=B['summary_by_budget']
sumC=C['summary_by_budget']
sumD=D['summary_by_budget']

# threshold parse-included/excluded
sumB_ex=B.get('summary_by_budget_parse_excluded', {})
def threshold(summary, base='hard_cap', method='ours_controller_v3_nofallback'):
    for b in sorted(int(x) for x in summary.keys()):
        sb=summary[str(b)]
        if base in sb and method in sb:
            da=float(sb[method]['accuracy'])-float(sb[base]['accuracy'])
            di=float(sb[method]['incoherence'])-float(sb[base]['incoherence'])
            if da>=0 and di<0:
                return b
    return None

th_in=threshold(sumB)
th_ex=threshold(sumB_ex) if sumB_ex else None

# Probe-only hull dominance check (simple dominance test)
probe_family=['probe_only_fixedk_k2','probe_only_fixedk_k4','probe_only_fixedk_k8','probe_adaptive_k_selected']

def dominated_by_probe(sb):
    v=sb['ours_controller_v3_nofallback']
    v_acc=float(v['accuracy']); v_inc=float(v['incoherence']); v_tok=float(v['avg_total_tokens'])
    for m in probe_family:
        if m not in sb: continue
        p=sb[m]
        p_acc=float(p['accuracy']); p_inc=float(p['incoherence']); p_tok=float(p['avg_total_tokens'])
        cond=(p_tok<=v_tok and p_acc>=v_acc and p_inc<=v_inc and ((p_acc>v_acc) or (p_inc<v_inc) or (p_tok<v_tok)))
        if cond:
            return True,m
    return False,None

# parse gating core
methods_b=['hard_cap','hard_cap_matched','budgeted_self_consistency','ours_controller_v3_nofallback'] + probe_family
gating=[]
for b in bud_core:
    vals=[float(sumB[str(b)][m]['parse_fail_rate']) for m in methods_b if m in sumB[str(b)]]
    mx=max(vals); mn=min(vals); sp=mx-mn
    gating.append((b,mx,mn,sp,int(mx<=0.01),int(sp<=0.01)))

lines=[]
lines.append('# Round9 Final Experiment Report')
lines.append('')
lines.append(f"- Runs: A9=`{ra}`, B9=`{rb}`, D9-confirm=`{rd}`, C9=`{rc}`")
lines.append(f"- Selected adaptive: `{sel['selected_adaptive']}`")
lines.append(f"- hard_cap_matched map: `{sel['hard_cap_matched_map_gpqa']}`")
lines.append('')
lines.append('## 1) Main Held-out (B9)')
lines.append(f"- Threshold parse-included: `T*={th_in}`")
lines.append(f"- Threshold parse-excluded: `T*={th_ex}`")
lines.append('')
lines.append('| Budget | Δacc(v3-hc) | Δincoh(v3-hc) | Δacc(v3-hcm) | Δincoh(v3-hcm) | v3_tok | hc_tok | hcm_tok | dominated_by_probe_family |')
lines.append('|---|---:|---:|---:|---:|---:|---:|---:|---|')
for b in bud_b:
    sb=sumB[str(b)]
    v=sb['ours_controller_v3_nofallback']; hc=sb['hard_cap']; hm=sb['hard_cap_matched']
    dom,who=dominated_by_probe(sb)
    lines.append(f"| {b} | {float(v['accuracy'])-float(hc['accuracy']):+.4f} | {float(v['incoherence'])-float(hc['incoherence']):+.4f} | {float(v['accuracy'])-float(hm['accuracy']):+.4f} | {float(v['incoherence'])-float(hm['incoherence']):+.4f} | {float(v['avg_total_tokens']):.1f} | {float(hc['avg_total_tokens']):.1f} | {float(hm['avg_total_tokens']):.1f} | {who if dom else 'NO'} |")
lines.append('')

lines.append('## 2) Parse Gating (B9 core budgets)')
lines.append('| Budget | max_parse_fail | min_parse_fail | spread | gate(max<=1%) | gate(spread<=1%p) |')
lines.append('|---|---:|---:|---:|---:|---:|')
for b,mx,mn,sp,g1,g2 in gating:
    lines.append(f'| {b} | {mx:.4f} | {mn:.4f} | {sp:.4f} | {g1} | {g2} |')
lines.append('')

lines.append('## 3) Dynamic Token Allocation (B9)')
lines.append('| Budget | Stop@Probe | ContinueSolve | ProbeShare | SolveShare | AvgProbeTok | AvgSolveTok |')
lines.append('|---|---:|---:|---:|---:|---:|---:|')
for b in bud_b:
    cd=(B.get('controller_diagnostics_by_budget',{}).get(str(b),{}) or {}).get('ours_controller_v3_nofallback',{})
    dec=cd.get('decision_counts',{})
    n=float(cd.get('n',0) or 0)
    stop=float(dec.get('stop_after_probe',0))/n if n>0 else 0.0
    cont=float(dec.get('continue_solve',0))/n if n>0 else 0.0
    lines.append(f"| {b} | {stop:.3f} | {cont:.3f} | {float(cd.get('probe_token_share',0.0)):.3f} | {float(cd.get('solve_token_share',0.0)):.3f} | {float(cd.get('avg_probe_tokens',0.0)):.1f} | {float(cd.get('avg_solve_tokens',0.0)):.1f} |")
lines.append('')

lines.append('## 4) R7 Confirm (D9 core budgets)')
lines.append('| Budget | Δacc(v3-hc) | Δincoh(v3-hc) | Δacc(v3-hcm) | Δincoh(v3-hcm) |')
lines.append('|---|---:|---:|---:|---:|')
for b in bud_d:
    sb=sumD[str(b)]
    v=sb['ours_controller_v3_nofallback']; hc=sb['hard_cap']; hm=sb['hard_cap_matched']
    lines.append(f"| {b} | {float(v['accuracy'])-float(hc['accuracy']):+.4f} | {float(v['incoherence'])-float(hc['incoherence']):+.4f} | {float(v['accuracy'])-float(hm['accuracy']):+.4f} | {float(v['incoherence'])-float(hm['incoherence']):+.4f} |")
lines.append('')

lines.append('## 5) 2nd Benchmark (C9 MMLU)')
lines.append('| Budget | Δacc(v3-hc) | Δincoh(v3-hc) | Δacc(v3-hcm) | Δincoh(v3-hcm) | v3_tok | hc_tok | hcm_tok |')
lines.append('|---|---:|---:|---:|---:|---:|---:|---:|')
for b in bud_c:
    sb=sumC[str(b)]
    v=sb['ours_controller_v3_nofallback']; hc=sb['hard_cap']; hm=sb['hard_cap_matched']
    lines.append(f"| {b} | {float(v['accuracy'])-float(hc['accuracy']):+.4f} | {float(v['incoherence'])-float(hc['incoherence']):+.4f} | {float(v['accuracy'])-float(hm['accuracy']):+.4f} | {float(v['incoherence'])-float(hm['incoherence']):+.4f} | {float(v['avg_total_tokens']):.1f} | {float(hc['avg_total_tokens']):.1f} | {float(hm['avg_total_tokens']):.1f} |")
lines.append('')

lines.append('## 6) Artifacts')
for name in [
    f'reports/{ra}_detailed_report.md',
    f'reports/{rb}_detailed_report.md',
    f'reports/{rd}_detailed_report.md',
    f'reports/{rc}_detailed_report.md',
    'reports/round9_adaptive_and_matched_config.json',
    'reports/round9_code_lock_manifest.sha256',
    'reports/round9_preregistration.md',
]:
    lines.append(f'- `{name}`')

Path('reports/round9_final_experiment_report.md').write_text('\n'.join(lines)+'\n')
Path('reports/round9_integrated_followup_report.md').write_text('\n'.join(lines)+'\n')
print('reports/round9_final_experiment_report.md')
PY

echo "ROUND9_PIPELINE_DONE"
