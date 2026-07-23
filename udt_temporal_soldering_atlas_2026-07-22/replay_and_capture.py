#!/usr/bin/env python3
"""Replay the complete deterministic temporal-atlas pipeline and capture raw streams."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ENV = {**os.environ, "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
STEPS = [
    {
        "id": "production",
        "command": [sys.executable, str(HERE / "build_temporal_soldering_atlas.py"), "--jobs", "12"],
        "outputs": [
            "PATH_TEMPORAL_CLASSIFICATION.tsv.gz", "ORTHOGONAL_COMPLEMENT_ATLAS.tsv.gz",
            "LINE_COMPLETION_ATLAS.tsv", "TEMPORAL_CLASS_CENSUS.tsv",
            "CHART_COFRAME_TEMPORAL_INVARIANCE.tsv", "COMPLETION_LADDER.tsv",
            "SELECTOR_STATUS.tsv", "INVARIANT_RECONSTRUCTION_LEDGER.tsv",
            "FROZEN_SOURCE_LEDGER.tsv", "VERIFICATION_RESULT.json",
        ],
    },
    {
        "id": "threshold_refinement",
        "command": [sys.executable, str(HERE / "refine_threshold_conflicts.py")],
        "outputs": ["THRESHOLD_CONFLICT_REFINEMENT.tsv", "THRESHOLD_CONFLICT_REFINEMENT_RESULT.json"],
    },
    {
        "id": "consolidation",
        "command": [sys.executable, str(HERE / "consolidate_temporal_results.py")],
        "outputs": [
            "CROSS_IMPLEMENTATION_COMPLEMENT_CLASSIFICATION.tsv.gz",
            "CROSS_IMPLEMENTATION_LINE_COMPLETION.tsv", "CONSOLIDATED_COMPLETION_LADDER.tsv",
            "CONSOLIDATED_INVARIANT_RECONSTRUCTION_LEDGER.tsv", "CONSOLIDATED_RESULT.json",
        ],
    },
    {
        "id": "independent",
        "command": [sys.executable, str(HERE / "verify_temporal_soldering_independent.py"), "--jobs", "12"],
        "outputs": ["INDEPENDENT_CATCH_PROOFS.tsv", "INDEPENDENT_VERIFICATION_RESULT.json"],
    },
    {
        "id": "timelike_phi_join",
        "command": [sys.executable, str(HERE / "verify_phi_gradient_soldering.py")],
        "outputs": ["PHI_GRADIENT_SOLDERING_RESULT.json"],
    },
    {
        "id": "spacelike_phi_join",
        "command": [sys.executable, str(HERE / "verify_phi_gradient_spacelike_branch.py")],
        "outputs": ["PHI_GRADIENT_SPACELIKE_BRANCH_RESULT.json"],
    },
    {
        "id": "package_verification",
        "command": [sys.executable, str(HERE / "verify_package.py")],
        "outputs": ["PACKAGE_CATCH_PROOFS.tsv", "PACKAGE_VERIFICATION_RESULT.json"],
    },
]


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""): h.update(block)
    return h.hexdigest()


def main():
    records = []
    for step in STEPS:
        paths = [HERE / name for name in step["outputs"]]
        if not all(path.exists() for path in paths):
            raise AssertionError(f"missing pre-replay output {step['id']}")
        before = {path.name: digest(path) for path in paths}
        completed = subprocess.run(step["command"], cwd=ROOT, env=ENV, text=True, capture_output=True, check=False)
        stdout_path = HERE / f"REPLAY_{step['id'].upper()}_STDOUT.txt"
        stderr_path = HERE / f"REPLAY_{step['id'].upper()}_STDERR.txt"
        stdout_path.write_text(completed.stdout, encoding="utf-8")
        stderr_path.write_text(completed.stderr, encoding="utf-8")
        after = {path.name: digest(path) for path in paths}
        deterministic = before == after
        if completed.returncode != 0 or not deterministic:
            raise AssertionError(f"replay failure {step['id']}: exit={completed.returncode} deterministic={deterministic}")
        records.append({
            "step_id": step["id"], "command": step["command"], "exit_code": completed.returncode,
            "stdout_path": stdout_path.name, "stdout_sha256": digest(stdout_path),
            "stderr_path": stderr_path.name, "stderr_sha256": digest(stderr_path),
            "output_hashes_before": before, "output_hashes_after": after,
            "byte_identical_replay": deterministic,
        })
    result = {
        "status": "PASS",
        "environment": {
            "python": sys.version.replace("\n", " "), "numpy": np.__version__,
            "platform": platform.platform(),
            "OMP_NUM_THREADS": ENV["OMP_NUM_THREADS"],
            "OPENBLAS_NUM_THREADS": ENV["OPENBLAS_NUM_THREADS"],
            "MKL_NUM_THREADS": ENV["MKL_NUM_THREADS"],
        },
        "steps": records,
        "all_exit_zero": all(row["exit_code"] == 0 for row in records),
        "all_outputs_byte_identical": all(row["byte_identical_replay"] for row in records),
        "cpu_only": True,
        "gpu_runs": 0,
    }
    (HERE / "REPLAY_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__": main()
