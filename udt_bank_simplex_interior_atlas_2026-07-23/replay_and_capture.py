#!/usr/bin/env python3
"""Replay production and both verifiers, requiring byte-identical outputs."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUTS = (
    "GROUP_REGISTRY.tsv",
    "LATTICE_SHEET_CENSUS.tsv",
    "COARSE_INTERVAL_CENSUS.tsv.gz",
    "LATTICE_COORDINATES.json",
    "RESULT.json",
    "RAW_SIGNS_L1_J1.npy.gz",
    "RAW_SIGNS_L1_J2.npy.gz",
    "RAW_SIGNS_L2_J1.npy.gz",
    "RAW_SIGNS_L2_J2.npy.gz",
    "HIGH_PRECISION_FULL_MATRIX_ANCHORS.tsv",
    "INDEPENDENT_NODE_REPLAY.tsv",
    "CATCH_PROOFS.tsv",
    "INDEPENDENT_VERIFICATION.json",
    "PACKAGE_ASSERTION_CHECKS.tsv",
    "PACKAGE_VERIFICATION.json",
)
COMMANDS = (
    (
        "production",
        [sys.executable, str(HERE / "build_bank_simplex_atlas.py"), "--replay"],
    ),
    (
        "independent",
        [sys.executable, str(HERE / "verify_bank_simplex_independent.py")],
    ),
    ("package", [sys.executable, str(HERE / "verify_package.py")]),
)


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def main():
    missing = [name for name in OUTPUTS if not (HERE / name).exists()]
    if missing:
        raise AssertionError(f"missing replay inputs: {missing}")
    before = {name: digest(HERE / name) for name in OUTPUTS}
    exits = {}
    for label, command in COMMANDS:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        exits[label] = completed.returncode
        (HERE / f"REPLAY_{label.upper()}_STDOUT.txt").write_text(
            completed.stdout, encoding="utf-8"
        )
        (HERE / f"REPLAY_{label.upper()}_STDERR.txt").write_text(
            completed.stderr, encoding="utf-8"
        )
        if completed.returncode:
            raise AssertionError(f"{label} replay exit {completed.returncode}")
    after = {name: digest(HERE / name) for name in OUTPUTS}
    result = {
        "schema": "udt-bank-simplex-deterministic-replay-1.0",
        "all_exit_zero": all(value == 0 for value in exits.values()),
        "all_outputs_byte_identical": before == after,
        "exit_codes": exits,
        "outputs": len(OUTPUTS),
        "output_sha256": after,
    }
    if not result["all_outputs_byte_identical"]:
        result["changed"] = [
            name for name in OUTPUTS if before[name] != after[name]
        ]
    (HERE / "REPLAY_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_exit_zero"] or not result["all_outputs_byte_identical"]:
        raise AssertionError("deterministic replay")


if __name__ == "__main__":
    main()
