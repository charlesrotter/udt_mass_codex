#!/usr/bin/env python3
"""Replay the audit, retain raw streams, record environment, and hash files."""

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


def run(script: str, stem: str) -> None:
    result = subprocess.run([sys.executable, str(HERE / script)], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    (HERE / f"{stem}_STDOUT.txt").write_bytes(result.stdout)
    (HERE / f"{stem}_STDERR.txt").write_bytes(result.stderr)
    if result.returncode:
        raise SystemExit(f"{script} failed with exit code {result.returncode}")


def main() -> None:
    run("build_audit.py", "BUILD")
    run("run_algebra.py", "ALGEBRA")
    run("verify_audit.py", "VERIFICATION")
    environment = {
        "schema": "udt-joint-selector-run-environment-1.0",
        "python": platform.python_version(),
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "backend": "CPU_SYMBOLIC_AND_FIXED_GIT_BLOB_CENSUS",
        "commands": [
            "python3 udt_joint_selector_provenance_audit_2026-07-28/build_audit.py",
            "python3 udt_joint_selector_provenance_audit_2026-07-28/run_algebra.py",
            "python3 udt_joint_selector_provenance_audit_2026-07-28/verify_audit.py",
        ],
        "gpu_processes_launched": 0,
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n")

    entries = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if path.is_file() and path.name not in {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}:
            entries.append(f"{digest(path)}  {path.name}")
    (HERE / "SHA256SUMS.txt").write_text("\n".join(entries) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "hashed_files": len(entries)}, sort_keys=True))


if __name__ == "__main__":
    main()
