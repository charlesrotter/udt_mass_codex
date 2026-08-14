#!/usr/bin/env bash
set -euo pipefail

ROOT=/home/udt-admin/udt_mass_codex/udt_observed_angular_pattern_raw_restart_2026-08-12
PROGRAM="$ROOT/run_r3_covariance_atlas.py"

if [[ "${1:-}" == "--self-test-exit" ]]; then
  python3 -c 'raise SystemExit(7)' 2>&1 | tee /tmp/udt_r3_service_exit_self_test.log
  exit 0
fi

if [[ "$#" -ne 1 ]]; then
  echo "usage: $0 CHECKPOINT_DIR" >&2
  exit 64
fi

checkpoint_dir=$1
mkdir -p "$checkpoint_dir"

export MPLCONFIGDIR=/tmp/udt_mpl
export PYTHONPATH="/tmp/udt_corrfunc_r2:/tmp/udt_treecorr_r2:$ROOT"

python3 "$PROGRAM" \
  --phase components \
  --checkpoint-dir "$checkpoint_dir" \
  2>&1 | tee -a "$checkpoint_dir/R3_SERVICE.log"
