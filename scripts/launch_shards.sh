#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "HF_TOKEN is not set" >&2
  exit 1
fi

RUN_ID="${1:-pilot_$(date -u +%Y%m%d_%H%M%S)}"
SHARDS="${2:-8}"
CONFIG="${3:-configs/pilot_gpqa.yaml}"

mkdir -p logs

for ((i=0;i<SHARDS;i++)); do
  CUDA_VISIBLE_DEVICES="$i" nohup python -m src.run_pilot \
    --config "$CONFIG" \
    --run-id "$RUN_ID" \
    --gpu-shard "$i/$SHARDS" \
    > "logs/${RUN_ID}_shard${i}.log" 2>&1 &
  echo "launched shard $i/$SHARDS (run_id=$RUN_ID)"
done

echo "Run dir: runs/$RUN_ID"
