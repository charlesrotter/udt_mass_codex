#!/usr/bin/env python3
"""Replay both implementations, preserve raw streams, and hash the package."""

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
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(script: str, stem: str) -> None:
    process = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    (HERE / f"{stem}_STDOUT.txt").write_bytes(process.stdout)
    (HERE / f"{stem}_STDERR.txt").write_bytes(process.stderr)
    if process.returncode:
        raise SystemExit(f"{script} failed with exit code {process.returncode}")


def main() -> None:
    run("derive_method_salvage.py", "DERIVATION")
    run("verify_method_salvage.py", "VERIFICATION")
    environment = {
        "schema": "udt-historical-angular-method-salvage-environment-1.0",
        "python": platform.python_version(),
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "backend": "CPU_SYMBOLIC",
        "commands": [
            "python3 udt_historical_angular_method_salvage_audit_2026-07-28/derive_method_salvage.py",
            "python3 udt_historical_angular_method_salvage_audit_2026-07-28/verify_method_salvage.py",
        ],
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    excluded = {"SHA256SUMS.txt", "REPOSITORY_GATES.json"}
    entries = [
        f"{sha256(path)}  {path.name}"
        for path in sorted(HERE.iterdir(), key=lambda item: item.name)
        if path.is_file() and path.name not in excluded
    ]
    (HERE / "SHA256SUMS.txt").write_text("\n".join(entries) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "hashed_files": len(entries)}, sort_keys=True))


if __name__ == "__main__":
    main()
