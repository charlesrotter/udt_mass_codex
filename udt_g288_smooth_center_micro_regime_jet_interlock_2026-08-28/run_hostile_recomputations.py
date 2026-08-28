#!/usr/bin/env python3
"""Reject geometric mutations by rerunning the dependency-free tensor verifier."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "verify_independent.py"
OUT = HERE / "HOSTILE_RECOMPUTATION_RESULT.json"
MUTATIONS = (
    "add_quadratic_parallel",
    "change_quartic_ratio",
    "quadratic_weyl_nonzero",
    "local_speed_coordinate_factor",
)


def run(*extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VERIFIER), "--no-write", *extra],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> None:
    baseline = run()
    if baseline.returncode != 0:
        raise AssertionError(f"baseline tensor recomputation failed: {baseline.stderr}")

    rows = []
    for mutation in MUTATIONS:
        trial = run("--hostile", mutation)
        caught = trial.returncode != 0 and "AssertionError" in trial.stderr
        rows.append({"name": mutation, "caught": caught, "returncode": trial.returncode})
    if not all(row["caught"] for row in rows):
        raise AssertionError(f"geometric mutation escaped: {rows}")

    result = {
        "status": "PASS",
        "baseline_recomputed": True,
        "implementation": "subprocess reruns of the standard-library exact tensor reconstruction",
        "caught": sum(row["caught"] for row in rows),
        "total": len(rows),
        "mutations": rows,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
