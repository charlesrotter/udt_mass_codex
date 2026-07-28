#!/usr/bin/env python3
"""Replay both implementations, retain raw streams, and hash the package."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def replay(script: str, stem: str) -> None:
    result = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    (HERE / f"{stem}_STDOUT.txt").write_bytes(result.stdout)
    (HERE / f"{stem}_STDERR.txt").write_bytes(result.stderr)
    if result.returncode:
        raise SystemExit(f"{script} failed with exit code {result.returncode}")


def main() -> None:
    replay("derive_nogo.py", "DERIVATION")
    replay("verify_nogo.py", "VERIFICATION")
    environment = {
        "schema": "udt-metric-natural-joint-selector-nogo-environment-1.0",
        "python": platform.python_version(),
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "backend": "CPU_EXACT_SYMBOLIC_PLUS_INDEPENDENT_RATIONAL_LINEAR_ALGEBRA",
        "commands": [
            "python3 udt_metric_natural_joint_selector_nogo_2026-07-28/derive_nogo.py",
            "python3 udt_metric_natural_joint_selector_nogo_2026-07-28/verify_nogo.py",
        ],
        "gpu_processes_launched": 0,
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    excluded = {"SHA256SUMS.txt", "REPOSITORY_GATES.json", "FINAL_REPOSITORY_GATES.json"}
    entries = [
        f"{digest(path)}  {path.name}"
        for path in sorted(HERE.iterdir(), key=lambda item: item.name)
        if path.is_file() and path.name not in excluded
    ]
    (HERE / "SHA256SUMS.txt").write_text("\n".join(entries) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "hashed_files": len(entries)}, sort_keys=True))


if __name__ == "__main__":
    main()
