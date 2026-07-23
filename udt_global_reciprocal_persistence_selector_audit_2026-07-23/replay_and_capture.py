#!/usr/bin/env python3
"""Replay both audit implementations and preserve raw stdout/stderr."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def run(script: str, prefix: str) -> dict[str, object]:
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    completed = subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    (HERE / f"{prefix}_STDOUT.txt").write_text(
        completed.stdout, encoding="utf-8"
    )
    (HERE / f"{prefix}_STDERR.txt").write_text(
        completed.stderr, encoding="utf-8"
    )
    if completed.returncode != 0:
        raise AssertionError(f"{script} failed: {completed.returncode}")
    return {
        "script": script,
        "returncode": completed.returncode,
        "stdout_bytes": len(completed.stdout.encode()),
        "stderr_bytes": len(completed.stderr.encode()),
    }


def main() -> None:
    result = {
        "schema": "udt-global-reciprocal-persistence-replay-1.0",
        "result": "PASS",
        "python": sys.version.split()[0],
        "runs": [
            run("derive_global_persistence_selector.py", "DERIVATION"),
            run(
                "verify_global_persistence_selector_independent.py",
                "INDEPENDENT",
            ),
        ],
    }
    (HERE / "REPLAY_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
