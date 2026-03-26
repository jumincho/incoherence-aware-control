#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "HF_TOKEN is not set" >&2
  exit 1
fi

RUN_ID="${1:-round4_$(date -u +%Y%m%d_%H%M%S)}"
SHARDS="${2:-8}"
CONFIG="${3:-configs/round4_budget_core5.yaml}"
MAX_QUESTIONS="${4:-0}"
MAX_TRIALS="${5:-0}"

mkdir -p logs

for i in $(seq 0 $((SHARDS - 1))); do
  tmux kill-session -t "round4_s${i}" 2>/dev/null || true

  EXTRA_ARGS=""
  if [[ "$MAX_QUESTIONS" != "0" ]]; then
    EXTRA_ARGS+=" --max-questions ${MAX_QUESTIONS}"
  fi
  if [[ "$MAX_TRIALS" != "0" ]]; then
    EXTRA_ARGS+=" --max-trials ${MAX_TRIALS}"
  fi

  tmux new-session -d -s "round4_s${i}" \
    "cd $ROOT_DIR && source .venv/bin/activate && export HF_TOKEN='${HF_TOKEN}' && CUDA_VISIBLE_DEVICES=${i} python -m src.run_pilot --config ${CONFIG} --run-id ${RUN_ID} --gpu-shard ${i}/${SHARDS}${EXTRA_ARGS} > ${ROOT_DIR}/logs/${RUN_ID}_shard${i}.log 2>&1"
  echo "launched round4 shard ${i}/${SHARDS}"
done

echo "Run dir: ${ROOT_DIR}/runs/${RUN_ID}"
echo "Config: ${CONFIG}"
