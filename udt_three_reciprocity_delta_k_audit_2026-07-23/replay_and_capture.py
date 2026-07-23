#!/usr/bin/env python3
"""Replay production and independent implementations and preserve streams."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def sha(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def run(script: str, prefix: str) -> dict[str, object]:
    environment = dict(os.environ)
    environment["CUDA_VISIBLE_DEVICES"] = ""
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
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
        "stdout_bytes": len(completed.stdout.encode("utf-8")),
        "stderr_bytes": len(completed.stderr.encode("utf-8")),
        "stdout_sha256": sha(completed.stdout),
        "stderr_sha256": sha(completed.stderr),
    }


def main() -> None:
    result = {
        "schema": "udt-three-reciprocity-replay-1.0",
        "result": "PASS",
        "python": sys.version.split()[0],
        "runs": [
            run("derive_three_reciprocity_delta_k.py", "DERIVATION"),
            run(
                "verify_three_reciprocity_delta_k_independent.py",
                "INDEPENDENT",
            ),
        ],
    }
    (HERE / "REPLAY_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
