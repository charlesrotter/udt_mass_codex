#!/usr/bin/env python3
"""Replay and capture all deterministic audit and repository gates."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
COMMANDS = (
    ("SOURCE_FREEZE", ["python3", str(PACKAGE / "freeze_sources.py")], 60),
    ("DERIVATION", ["python3", str(PACKAGE / "derive_compatibility.py")], 60),
    ("INDEPENDENT", ["python3", str(PACKAGE / "verify_compatibility_independent.py")], 60),
    ("VERIFICATION", ["python3", str(PACKAGE / "verify_audit.py")], 60),
    ("REPOSITORY_GATES", ["python3", str(PACKAGE / "verify_repository_gates.py")], 360),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    command_records = []
    for label, command, timeout in COMMANDS:
        result = subprocess.run(
            command, cwd=ROOT, capture_output=True, timeout=timeout, check=False
        )
        (PACKAGE / f"{label}_STDOUT.txt").write_bytes(result.stdout)
        (PACKAGE / f"{label}_STDERR.txt").write_bytes(result.stderr)
        command_records.append(
            {
                "label": label,
                "command": command,
                "exit_code": result.returncode,
                "stdout_sha256": sha256(result.stdout),
                "stderr_sha256": sha256(result.stderr),
            }
        )
        if result.returncode:
            raise RuntimeError(f"{label} failed with exit code {result.returncode}")
    environment = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "commands": command_records,
    }
    (PACKAGE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS captured source, derivation, independent, semantic, and repository gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
