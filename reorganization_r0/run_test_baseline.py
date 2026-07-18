#!/usr/bin/env python3
"""Run and record the existing Phase-R0 test baseline without changing tests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


EXPECTED_FAILURE = "tests/test_hygiene_header.py::test_covered_results_have_hygiene_header"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    output_dir = args.output_dir.resolve()
    command = [sys.executable, "-m", "pytest", "tests/"]
    completed = subprocess.run(
        command,
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        text=True,
    )
    output = completed.stdout
    (output_dir / "TEST_BASELINE.txt").write_text(output, encoding="utf-8")
    summary_match = re.search(
        r"(?P<failed>\d+) failed, (?P<passed>\d+) passed, (?P<xfailed>\d+) xfailed",
        output,
    )
    if not summary_match:
        raise SystemExit("could not parse pytest summary")
    failed = int(summary_match.group("failed"))
    passed = int(summary_match.group("passed"))
    xfailed = int(summary_match.group("xfailed"))
    baseline_match = (
        completed.returncode == 1
        and failed == 1
        and passed == 69
        and xfailed == 1
        and EXPECTED_FAILURE in output
    )
    record = {
        "date": "2026-07-18",
        "command": "python3 -m pytest tests/",
        "python": sys.version.split()[0],
        "returncode": completed.returncode,
        "passed": passed,
        "failed": failed,
        "xfailed": xfailed,
        "expected_failure": EXPECTED_FAILURE,
        "baseline_match": baseline_match,
        "scope": "existing tests at the bfa0b9a R0 base; no test or physics file edited",
    }
    (output_dir / "TEST_BASELINE.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if baseline_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
