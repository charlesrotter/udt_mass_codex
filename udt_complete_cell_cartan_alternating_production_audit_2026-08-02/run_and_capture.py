#!/usr/bin/env python3
"""Run package commands and preserve exact stdout/stderr and exit status."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
COMMANDS = (
    ("DERIVATION", ["python3", str(PACKAGE / "derive_cartan_alternating.py")], 120),
    ("INDEPENDENT", ["python3", str(PACKAGE / "verify_cartan_alternating_independent.py")], 120),
    ("ENVIRONMENT", ["python3", str(PACKAGE / "capture_environment.py")], 60),
    ("REPOSITORY_GATES", ["python3", str(PACKAGE / "verify_repository_gates.py")], 420),
)


def main() -> int:
    ledger = []
    for label, command, timeout in COMMANDS:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
        (PACKAGE / f"{label}_STDOUT.txt").write_text(completed.stdout, encoding="utf-8")
        (PACKAGE / f"{label}_STDERR.txt").write_text(completed.stderr, encoding="utf-8")
        ledger.append({"label": label, "command": command, "exit_code": completed.returncode})
        if completed.returncode != 0:
            raise SystemExit(f"{label} failed with {completed.returncode}")
    (PACKAGE / "RUN_LOG.json").write_text(
        json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(ledger, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

