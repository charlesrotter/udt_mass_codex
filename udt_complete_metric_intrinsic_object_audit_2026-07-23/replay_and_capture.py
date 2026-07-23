#!/usr/bin/env python3
"""Replay production and independent derivations and freeze raw streams."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run(script: str, prefix: str) -> dict[str, object]:
    command = [sys.executable, str(HERE / script)]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True)
    (HERE / f"{prefix}_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / f"{prefix}_STDERR.txt").write_bytes(completed.stderr)
    return {
        "command": " ".join(command),
        "exit_code": completed.returncode,
        "stdout_sha256": digest_bytes(completed.stdout),
        "stderr_sha256": digest_bytes(completed.stderr),
    }


def main() -> None:
    production = run("derive_intrinsic_objects.py", "DERIVATION")
    independent = run("verify_intrinsic_objects_independent.py", "INDEPENDENT")
    output = {
        "schema": "udt-complete-metric-intrinsic-object-replay-1.0",
        "production": production,
        "independent": independent,
        "all_exit_zero": production["exit_code"] == independent["exit_code"] == 0,
    }
    (HERE / "REPLAY_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    if not output["all_exit_zero"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
