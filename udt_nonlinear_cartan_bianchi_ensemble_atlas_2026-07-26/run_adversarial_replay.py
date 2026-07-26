#!/usr/bin/env python3
"""Run both portable adversarial implementations and preserve raw streams."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent


def run(script: str, prefix: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(HERE / script)],
        cwd=HERE.parent,
        text=True,
        capture_output=True,
    )
    stdout = completed.stdout
    stderr = completed.stderr
    (HERE / f"{prefix}_STDOUT.txt").write_text(stdout, encoding="utf-8")
    (HERE / f"{prefix}_STDERR.txt").write_text(stderr, encoding="utf-8")
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return {
        "script": script,
        "script_sha256": hashlib.sha256((HERE / script).read_bytes()).hexdigest(),
        "stdout_sha256": hashlib.sha256(stdout.encode("utf-8")).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr.encode("utf-8")).hexdigest(),
        "exit_code": completed.returncode,
    }


def main() -> None:
    import sympy
    if sympy.__version__ != "1.13.1":
        raise SystemExit(f"wrong SymPy version: {sympy.__version__}")
    result = {
        "status": "PASS",
        "sympy": sympy.__version__,
        "koszul_frame": run("verify_adversarial_koszul.py", "ADVERSARIAL_KOSZUL"),
        "coordinate_metric": run("verify_adversarial_coordinate_metric.py", "ADVERSARIAL_COORDINATE"),
        "original_fresh_context_hashes": {
            "expectation": "6e197767abf3e4efc8da01fe9eba6d237effd036c246c6c1c9118405008b6569",
            "koszul_script": "3b5377d3a6e0d62802bc2d4b837d70390f4e90be4279b426cb1359a456dbef48",
            "coordinate_script": "104c2f65b55d0211bce049921fb588b989cf34f1528fbc9e28892fca4340c123",
        },
    }
    (HERE / "ADVERSARIAL_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
