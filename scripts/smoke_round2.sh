#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "HF_TOKEN is not set" >&2
  exit 1
fi

RUN_ID="${1:-round2_smoke_$(date -u +%Y%m%d_%H%M%S)}"
CONFIG="${2:-configs/round2_gpqa.yaml}"
SHARDS=2

mkdir -p logs
for i in $(seq 0 $((SHARDS - 1))); do
  tmux kill-session -t "round2_smoke_s${i}" 2>/dev/null || true
  tmux new-session -d -s "round2_smoke_s${i}" \
    "cd $ROOT_DIR && source .venv/bin/activate && export HF_TOKEN='${HF_TOKEN}' && CUDA_VISIBLE_DEVICES=${i} python -m src.run_pilot --config ${CONFIG} --run-id ${RUN_ID} --gpu-shard ${i}/${SHARDS} --max-questions 8 --max-trials 2 --budgets 1024,1536 > ${ROOT_DIR}/logs/${RUN_ID}_shard${i}.log 2>&1"
  echo "launched smoke shard ${i}/${SHARDS}"
done

echo "Smoke run dir: ${ROOT_DIR}/runs/${RUN_ID}"
