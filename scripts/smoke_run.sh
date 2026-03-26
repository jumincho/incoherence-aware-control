#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${HF_TOKEN:-}" ]]; then
  echo "HF_TOKEN is not set" >&2
  exit 1
fi

RUN_ID="${1:-smoke_$(date -u +%Y%m%d_%H%M%S)}"
CONFIG="${2:-configs/pilot_gpqa.yaml}"
SHARDS=2

mkdir -p logs
for ((i=0;i<SHARDS;i++)); do
  CUDA_VISIBLE_DEVICES="$i" nohup python -m src.run_pilot \
    --config "$CONFIG" \
    --run-id "$RUN_ID" \
    --gpu-shard "$i/$SHARDS" \
    --max-questions 8 \
    --max-trials 2 \
    > "logs/${RUN_ID}_shard${i}.log" 2>&1 &
  echo "launched smoke shard $i/$SHARDS"
done

echo "smoke run: runs/$RUN_ID"
