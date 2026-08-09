#!/usr/bin/env python3
"""Run and preserve the final N03 local and repository gates."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import sympy


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    jobs = [
        ("derivation", [sys.executable, str(HERE / "derive_n03_profile_map.py")]),
        ("verification", [sys.executable, str(HERE / "verify_n03_profile_map.py")]),
        ("premise_gate", [sys.executable, str(ROOT / "verify_current_scientific_premises.py")]),
        ("pytest", [sys.executable, "-m", "pytest", "tests/", "-q"]),
    ]
    records = []
    for name, command in jobs:
        completed = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
        (HERE / f"{name.upper()}_STDOUT.txt").write_bytes(completed.stdout)
        (HERE / f"{name.upper()}_STDERR.txt").write_bytes(completed.stderr)
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
    (HERE / "RUN_LOG.json").write_text(
        json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    environment = {
        "cpu_only": True,
        "git_preregistration_commit": "c64acaa1",
        "platform": platform.platform(),
        "python": platform.python_version(),
        "sympy": sympy.__version__,
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS: captured {len(records)} N03 local/repository gates")


if __name__ == "__main__":
    main()
