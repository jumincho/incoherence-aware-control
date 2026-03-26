#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[cleanup] root: $ROOT_DIR"

# 1) Remove throwaway run directories from debugging/smoke attempts.
for d in runs/dryrun_* runs/smoke_v1; do
  if [[ -d "$d" ]]; then
    echo "[cleanup] remove run dir: $d"
    rm -rf "$d"
  fi
done

# 2) Remove throwaway logs.
for f in logs/dryrun_* logs/smoke_v1_*; do
  if [[ -e "$f" ]]; then
    echo "[cleanup] remove log: $f"
    rm -f "$f"
  fi
done

# Optional: remove empty smoke_v2 logs.
for f in logs/smoke_v2_*; do
  if [[ -f "$f" ]] && [[ ! -s "$f" ]]; then
    echo "[cleanup] remove empty log: $f"
    rm -f "$f"
  fi
done

# 3) Remove local pycache artifacts under project source/tests.
for c in src/__pycache__ tests/__pycache__; do
  if [[ -d "$c" ]]; then
    echo "[cleanup] remove cache dir: $c"
    rm -rf "$c"
  fi
done

# 4) Stop stale tmux sessions created for previous rounds.
for s in $(tmux ls 2>/dev/null | cut -d: -f1 | grep -E '^(incoh_full_s[0-9]+|incoh_monitor|round2_s[0-9]+|round2_smoke_s[0-9]+|round2c_s[0-9]+|round3_s[0-9]+)$' || true); do
  echo "[cleanup] kill tmux session: $s"
  tmux kill-session -t "$s" || true
done

echo "[cleanup] done."
