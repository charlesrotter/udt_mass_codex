#!/usr/bin/env python3
"""Replay all three atlas routes and require byte-identical generated evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUTS = (
    "ENDPOINT_PAIR_REGISTRY.tsv",
    "SHEET_CLASSIFICATION.tsv",
    "NULL_GRAPH_CERTIFICATES.tsv.gz",
    "SAME_SIGN_BOX_CERTIFICATES.tsv.gz",
    "UNRESOLVED_BOXES.tsv",
    "HIGH_PRECISION_ANCHORS.tsv",
    "CHART_COMPARISON.tsv",
    "ADJACENCY_COMPONENT_GRAPH.tsv",
    "EXACT_TOPOLOGY_LEDGER.tsv",
    "SOURCE_LEDGER.tsv",
    "RESULT.json",
    "INDEPENDENT_FULL_MATRIX_INTERVAL_CERTIFICATES.tsv",
    "INDEPENDENT_MATRIX_PROBES.tsv",
    "INDEPENDENT_VERIFICATION.json",
    "PACKAGE_CATCH_PROOFS.tsv",
    "PACKAGE_VERIFICATION.json",
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(label, script):
    completed = subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    (HERE / f"REPLAY_{label}_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / f"REPLAY_{label}_STDERR.txt").write_bytes(completed.stderr)
    if completed.returncode:
        raise AssertionError(f"{label} replay exit {completed.returncode}")
    return completed.returncode


def main():
    before = {name: digest(HERE / name) for name in OUTPUTS}
    exits = {
        "production": run("PRODUCTION", "build_configuration_adjacency_atlas.py"),
        "independent": run("INDEPENDENT", "verify_adjacency_independent.py"),
        "package": run("PACKAGE", "verify_package.py"),
    }
    after = {name: digest(HERE / name) for name in OUTPUTS}
    if before != after:
        changed = sorted(name for name in OUTPUTS if before[name] != after[name])
        raise AssertionError(f"non-deterministic outputs {changed}")
    result = {
        "status": "PASS",
        "all_exit_zero": all(value == 0 for value in exits.values()),
        "all_outputs_byte_identical": before == after,
        "outputs": len(OUTPUTS),
        "output_sha256": after,
        "exit_codes": exits,
    }
    (HERE / "REPLAY_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
