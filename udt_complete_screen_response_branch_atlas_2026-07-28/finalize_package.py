#!/usr/bin/env python3
"""Capture exact/independent streams, environment, and package SHA-256 manifest."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def capture(script: str, stem: str) -> None:
    environment = dict(os.environ)
    environment.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1"})
    process = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT, env=environment,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    (HERE / f"{stem}_STDOUT.txt").write_bytes(process.stdout)
    (HERE / f"{stem}_STDERR.txt").write_bytes(process.stderr)
    if process.returncode:
        raise SystemExit(f"{script} failed: {process.returncode}")


def main() -> None:
    capture("extract_branch_universe.py", "EXTRACTION")
    capture("derive_screen_response_atlas.py", "DERIVATION")
    capture("verify_screen_response_independent.py", "INDEPENDENT")
    capture("verify_audit.py", "VERIFICATION")
    environment = {
        "schema": "udt-complete-screen-response-environment-1.0",
        "python": platform.python_version(),
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "backend": "CPU_SYMBOLIC_ONLY",
        "CUDA_VISIBLE_DEVICES": "empty",
        "commands": [
            f"python3 {HERE.name}/extract_branch_universe.py",
            f"python3 {HERE.name}/derive_screen_response_atlas.py",
            f"python3 {HERE.name}/verify_screen_response_independent.py",
            f"python3 {HERE.name}/verify_audit.py",
        ],
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n")
    excluded = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    entries = [
        f"{sha(path)}  {path.name}"
        for path in sorted(HERE.iterdir(), key=lambda p: p.name)
        if path.is_file() and path.name not in excluded
    ]
    (HERE / "SHA256SUMS.txt").write_text("\n".join(entries) + "\n")
    print(json.dumps({"status": "PASS", "hashed_files": len(entries)}, sort_keys=True))


if __name__ == "__main__":
    main()
