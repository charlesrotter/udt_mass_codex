#!/usr/bin/env python3
"""Run the registered gates and preserve exact stdout/stderr plus hashes."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    jobs = [
        ("derivation", [sys.executable, str(HERE / "derive_mode_ownership.py")]),
        ("verification", [sys.executable, str(HERE / "verify_mode_ownership.py")]),
        ("premise_gate", [sys.executable, str(ROOT / "verify_current_scientific_premises.py")]),
        ("pytest", [sys.executable, "-m", "pytest", "tests/", "-q"]),
    ]
    records = []
    for name, command in jobs:
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
        stdout_path = HERE / f"{name.upper()}_STDOUT.txt"
        stderr_path = HERE / f"{name.upper()}_STDERR.txt"
        stdout_path.write_bytes(completed.stdout)
        stderr_path.write_bytes(completed.stderr)
        records.append(
            {
                "name": name,
                "command": command,
                "exit_code": completed.returncode,
                "stdout_sha256": digest(completed.stdout),
                "stderr_sha256": digest(completed.stderr),
            }
        )
        if completed.returncode:
            raise SystemExit(f"gate failed: {name}")
    (HERE / "RUN_LOG.json").write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: captured {len(records)} registered gates")


if __name__ == "__main__":
    main()
