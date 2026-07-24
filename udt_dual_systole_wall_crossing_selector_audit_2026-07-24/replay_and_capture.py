#!/usr/bin/env python3
"""Replay production and independent checks and preserve exact streams."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def run(script: str, stem: str) -> dict[str, object]:
    command = [sys.executable, str(HERE / script)]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    (HERE / f"{stem}_STDOUT.txt").write_bytes(completed.stdout)
    (HERE / f"{stem}_STDERR.txt").write_bytes(completed.stderr)
    if completed.returncode:
        raise SystemExit(completed.returncode)
    return {
        "command": " ".join(command),
        "returncode": completed.returncode,
        "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr).hexdigest(),
    }


def main() -> None:
    result = {
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "production": run("derive_wall_crossing_selector.py", "DERIVATION"),
        "independent": run("verify_wall_crossing_independent.py", "INDEPENDENT"),
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

