# Round3 Feedback Integration Note

## Summary
Round2 feedback was accepted and translated into executable Round3 settings/code.
Primary direction is now explicit: **regime-dependent evaluation** with stronger compute-scaling baselines and a budget-aware controller v2.

## Accepted feedback items and implementation
1. Increase methodological rigor for compute-scaling comparison
- Added `budgeted_self_consistency` baseline (compute scales with budget).
- Added `forced_deliberation` baseline (sequential budget-forcing style).
- File: `src/methods.py`.

2. Controller redesign for low-budget robustness
- Added `ours_controller_v2` with:
  - low-budget fallback (`hard_cap`),
  - progressive probing (`n_probe_first` then `n_probe_second`),
  - probe budget cap by ratio/cap,
  - solve-min target controls.
- Alias for ablation without fallback: `ours_controller_v2_nofallback`.
- File: `src/methods.py`.

3. Round3 experiment configurations
- `configs/round3_core.yaml`
  - methods: baseline/hard_cap/self_consistency/budgeted_self_consistency/forced_deliberation/ours_controller_v2
  - budgets: 768, 1024, 1536, 2048, 2560
  - trials: 5 seeds
- `configs/round3_spend_target.yaml`
  - methods: baseline/hard_cap/budgeted_self_consistency/forced_deliberation/ours_controller_v2
  - target spends: 300, 600, 900, 1200
  - trials: 5 seeds
- `configs/round3_ablation.yaml`
  - controller v2 vs no-fallback + decomposition/anchor/full ablations.

4. Analyzer extensions for Round3 narratives
- Added average budget utilization in summary table.
- Added controller diagnostics per budget:
  - decision counts,
  - avg probe/solve/restart tokens.
- File: `src/analyze_hotmess_style.py`.

5. Robustness fix
- Dataset size clamp added when `n_questions` exceeds split size.
- File: `src/run_pilot.py`.

6. Ops/launch
- Added Round3 launcher: `scripts/launch_round3.sh`.
- Cleanup script extended to cover round3 sessions: `scripts/cleanup_round.sh`.
- README updated with Round2/Round3 commands.

## Validation status
- `py_compile` passed for all `src/*.py`.
- Unit tests passed (`7/7`).
- Round3 smoke run started and validated for early progress and method execution.

## Recommended Round3 run order
1. Core regime map
```bash
HF_TOKEN=... ./scripts/launch_round3.sh round3_core_v1 8 configs/round3_core.yaml
python -m src.monitor --run-dir runs/round3_core_v1
python -m src.analyze_hotmess_style --run-dir runs/round3_core_v1 --bootstrap-iters 2000
```

2. Spend-target sweep
```bash
HF_TOKEN=... ./scripts/launch_round3.sh round3_spend_v1 8 configs/round3_spend_target.yaml
python -m src.monitor --run-dir runs/round3_spend_v1
python -m src.analyze_hotmess_style --run-dir runs/round3_spend_v1 --bootstrap-iters 2000
```

3. Controller/ablation diagnostics
```bash
HF_TOKEN=... ./scripts/launch_round3.sh round3_ablation_v1 8 configs/round3_ablation.yaml
python -m src.monitor --run-dir runs/round3_ablation_v1
python -m src.analyze_hotmess_style --run-dir runs/round3_ablation_v1 --bootstrap-iters 2000
```

## Notes
- For `gpqa_diamond/train`, requested `n_questions` larger than split size is now automatically clamped.
- Given variance-centric metrics, keep `R>=5` for core comparisons.
