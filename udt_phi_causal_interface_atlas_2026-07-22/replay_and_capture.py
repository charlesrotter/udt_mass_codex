#!/usr/bin/env python3
"""Replay both scientific routes and require byte-identical generated evidence."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTPUTS = (
    "IDENTITY_CAUSAL_CERTIFICATES.tsv",
    "INTERVAL_SIGN_CERTIFICATES.tsv.gz",
    "INTERFACE_ATLAS.tsv",
    "REGISTERED_BANK_CAUSAL_PARTITION.tsv",
    "PATH_PRESENTATION_CAUSAL_ATLAS.tsv.gz",
    "MOTIF_CAUSAL_JOIN_CENSUS.tsv",
    "COMPLETION_CAUSAL_COMPATIBILITY.tsv",
    "EXACT_IDENTITY_LEDGER.tsv",
    "SOURCE_LEDGER.tsv",
    "RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
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
        "production": run("PRODUCTION", "build_phi_causal_interface_atlas.py"),
        "independent": run("INDEPENDENT", "verify_phi_causal_interface_independent.py"),
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
    (HERE / "REPLAY_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
