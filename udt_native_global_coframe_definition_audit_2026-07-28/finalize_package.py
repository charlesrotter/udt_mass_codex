#!/usr/bin/env python3
"""Replay the audit, preserve raw process streams, and hash the package."""

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


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run(script: str, stem: str) -> None:
    command = [sys.executable, str(HERE / script)]
    result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (HERE / f"{stem}_STDOUT.txt").write_bytes(result.stdout)
    (HERE / f"{stem}_STDERR.txt").write_bytes(result.stderr)
    if result.returncode != 0:
        raise SystemExit(f"{script} failed with exit code {result.returncode}")


def main() -> None:
    run("derive_global_definition.py", "DERIVATION")
    run("verify_global_definition.py", "VERIFICATION")
    environment = {
        "schema": "udt-native-global-coframe-definition-environment-1.0",
        "python": platform.python_version(),
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "backend": "CPU_SYMBOLIC",
        "commands": [
            "python3 udt_native_global_coframe_definition_audit_2026-07-28/derive_global_definition.py",
            "python3 udt_native_global_coframe_definition_audit_2026-07-28/verify_global_definition.py",
        ],
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n")

    entries = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if path.is_file() and path.name != "SHA256SUMS.txt":
            entries.append(f"{sha256(path)}  {path.name}")
    (HERE / "SHA256SUMS.txt").write_text("\n".join(entries) + "\n")
    print(json.dumps({"status": "PASS", "hashed_files": len(entries)}, sort_keys=True))


if __name__ == "__main__":
    main()
