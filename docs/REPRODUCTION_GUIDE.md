# Reproduction Guide (New Server)

## 0) Sibling-Repo Prerequisite

`src/analyze_hotmess_style.py` imports metric utilities from a sibling repository: clone
`hot-mess-of-ai` into the **same parent directory** as `incoherence-aware-control` before
running any analysis step (i.e. `../hot-mess-of-ai` must exist relative to this repo root).

## 1) Environment
```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install -U -r requirements.txt
export HF_TOKEN=...   # runtime only, never commit
```

## 2) Round9 Pipeline (reference)
```bash
bash scripts/run_round9_pipeline.sh
```

## 3) Manual Round9 Sequence
```bash
# tuning
python -m src.run_pilot --config configs/round9a_tuning_splitA9.yaml --gpu-shard 0/8
# ... launch all 8 shards
python -m src.monitor --run-dir runs/round9a_tuning_splitA9_r3_v1
python -m src.analyze_hotmess_style --run-dir runs/round9a_tuning_splitA9_r3_v1

# held-out
python -m src.run_pilot --config configs/round9b_heldout_splitB9.yaml --gpu-shard 0/8
# ... launch all 8 shards
python -m src.monitor --run-dir runs/round9b_heldout_splitB9_r5_v1
python -m src.analyze_hotmess_style --run-dir runs/round9b_heldout_splitB9_r5_v1
python -m src.report_spend_sweep --run-dir runs/round9b_heldout_splitB9_r5_v1
```

## 4) Reproducibility Rules
- If method/prompt/parser/policy changes: create a fresh held-out split
- Keep parse policy and token accounting identical across compared methods
- Freeze code hash before held-out final run
