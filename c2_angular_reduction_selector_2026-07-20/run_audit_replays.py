#!/usr/bin/env python3
"""Run and preserve the exact CPU-only census, derivation, verification, and tests."""

from __future__ import annotations

import csv
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


def run(identity: str, command: list[str], output: str, expected: int,
        env: dict[str, str] | None = None) -> dict[str, object]:
    done = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)
    (HERE / output).write_bytes(done.stdout)
    if done.returncode != expected:
        raise AssertionError(f"{identity}: exit {done.returncode}, expected {expected}")
    return {"id": identity, "command": " ".join(command), "exit_code": done.returncode,
            "output_artifact": output, "stdout_stderr_sha256": digest(done.stdout)}


def main() -> None:
    prefix = "c2_angular_reduction_selector_2026-07-20/"
    records = [
        run("E01", [sys.executable, prefix+"build_source_census.py"], "CENSUS_TRANSCRIPT.txt", 0),
        run("E02", [sys.executable, prefix+"build_source_adjudication.py"], "ADJUDICATION_TRANSCRIPT.txt", 0),
        run("E03", [sys.executable, prefix+"derive_c2_angular_reduction.py"], "DERIVATION_TRANSCRIPT.txt", 0),
        run("E04", [sys.executable, prefix+"verify_c2_angular_reduction.py"], "VERIFICATION_TRANSCRIPT.txt", 0),
    ]
    env = dict(os.environ); env["CUDA_VISIBLE_DEVICES"] = ""; env["PYTHONDONTWRITEBYTECODE"] = "1"
    tests = run("E05", [sys.executable, "-m", "pytest", "tests/"], "TEST_TRANSCRIPT.txt", 1, env)
    text = (HERE/"TEST_TRANSCRIPT.txt").read_text(encoding="utf-8")
    match = re.search(r"(\d+) failed, (\d+) passed, (\d+) xfailed", text)
    if match is None or tuple(map(int, match.groups())) != (1, 69, 1):
        raise AssertionError("test baseline drift")
    if "tests/test_hygiene_header.py::test_covered_results_have_hygiene_header" not in text:
        raise AssertionError("known hygiene failure missing")
    records.append(tests)
    site_packages = str(Path(sympy.__file__).resolve().parent.parent)
    isolated_code = (
        "import sys,runpy; "
        f"sys.path.insert(0,{site_packages!r}); "
        "import sympy; assert sympy.__version__=='1.13.1'; "
        "print('isolated_sympy='+sympy.__version__); "
        f"runpy.run_path({prefix+'verify_c2_angular_reduction.py'!r},run_name='__main__')"
    )
    records.append(run("E06", [sys.executable, "-I", "-c", isolated_code],
                       "ISOLATED_VERIFICATION_TRANSCRIPT.txt", 0, env))
    result = {
        "schema": "udt-conditional-c2-angular-reduction-execution-1.0", "result": "PASS",
        "records": records,
        "environment": {"python": sys.version.split()[0], "sympy": sympy.__version__,
                        "cpu_only": True, "gpu_used": False},
        "test_baseline": {"passed": 69, "failed_known_hygiene": 1, "xfailed": 1},
    }
    (HERE/"EXECUTION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    fields = ["id", "command", "compute", "exit_code", "output_artifact", "output_sha256"]
    with (HERE/"EXECUTION_LEDGER.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for record in records:
            writer.writerow({"id": record["id"], "command": record["command"], "compute": "CPU_ONLY",
                             "exit_code": "1_EXPECTED_BASELINE" if record["exit_code"] == 1 else "0",
                             "output_artifact": record["output_artifact"],
                             "output_sha256": record["stdout_stderr_sha256"]})
        writer.writerow({"id": "E07", "command": "fresh external-model review",
                         "compute": "EXTERNAL_REVIEW_NOT_PERFORMED", "exit_code": "AUTHORIZATION_NOT_GIVEN",
                         "output_artifact": "EXTERNAL_REVIEW_STATUS.txt",
                         "output_sha256": digest((HERE/"EXTERNAL_REVIEW_STATUS.txt").read_bytes())})
    (HERE/"ENVIRONMENT.txt").write_text(
        f"python={sys.version.split()[0]}\nsympy={sympy.__version__}\ncompute=CPU_ONLY\n"
        "gpu_used=false\nexternal_review=NOT_AUTHORIZED\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "records": len(records),
                      "tests": "69_passed_1_known_failed_1_xfailed"}, sort_keys=True))


if __name__ == "__main__":
    main()
