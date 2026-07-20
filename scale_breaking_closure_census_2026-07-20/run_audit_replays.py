#!/usr/bin/env python3
"""Run and preserve the exact CPU-only census, algebra, verifier, and test outputs."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import sympy


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(identity: str, command: list[str], output: str, expected: int, env: dict[str, str] | None = None) -> dict[str, object]:
    completed = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (HERE / output).write_bytes(completed.stdout)
    if completed.returncode != expected:
        raise AssertionError(f"{identity}: exit {completed.returncode}, expected {expected}")
    return {
        "id": identity,
        "command": " ".join(command),
        "exit_code": completed.returncode,
        "output_artifact": output,
        "stdout_stderr_sha256": digest(completed.stdout),
    }


def main() -> None:
    prefix = "scale_breaking_closure_census_2026-07-20/"
    records = [
        run("E01", [sys.executable, prefix + "build_source_census.py"], "CENSUS_TRANSCRIPT.txt", 0),
        run("E02", [sys.executable, prefix + "derive_scale_breaking_closure.py"], "DERIVATION_TRANSCRIPT.txt", 0),
        run("E03", [sys.executable, prefix + "verify_scale_breaking_closure.py"], "VERIFICATION_TRANSCRIPT.txt", 0),
    ]
    env = dict(os.environ)
    env["CUDA_VISIBLE_DEVICES"] = ""
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    tests = run("E04", [sys.executable, "-m", "pytest", "tests/"], "TEST_TRANSCRIPT.txt", 1, env)
    text = (HERE / "TEST_TRANSCRIPT.txt").read_text(encoding="utf-8")
    match = re.search(r"(\d+) failed, (\d+) passed, (\d+) xfailed", text)
    if match is None or tuple(map(int, match.groups())) != (1, 69, 1):
        raise AssertionError("test baseline drift")
    if "tests/test_hygiene_header.py::test_covered_results_have_hygiene_header" not in text:
        raise AssertionError("known hygiene failure missing")
    records.append(tests)
    result = {
        "schema": "udt-scale-breaking-execution-1.0",
        "result": "PASS",
        "records": records,
        "environment": {
            "python": sys.version.split()[0],
            "sympy": sympy.__version__,
            "cpu_only": True,
            "gpu_used": False,
        },
        "test_baseline": {"passed": 69, "failed_known_hygiene": 1, "xfailed": 1},
    }
    (HERE / "EXECUTION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "records": len(records), "tests": "69_passed_1_known_failed_1_xfailed"}, sort_keys=True))


if __name__ == "__main__":
    main()
