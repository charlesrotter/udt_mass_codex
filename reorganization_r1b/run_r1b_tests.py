#!/usr/bin/env python3
"""Run and record the complete R1B repository test baseline."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def count(pattern: str, text: str) -> int:
    matches = re.findall(pattern, text, flags=re.MULTILINE)
    return int(matches[-1]) if matches else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--scope", required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/"],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    transcript = completed.stdout
    (output / "TEST_BASELINE.txt").write_text(transcript, encoding="utf-8")
    passed = count(r"(\d+) passed", transcript)
    failed = count(r"(\d+) failed", transcript)
    xfailed = count(r"(\d+) xfailed", transcript)
    known = "tests/test_hygiene_header.py::test_covered_results_have_hygiene_header"
    result = {
        "command": "python3 -m pytest tests/",
        "scope": args.scope,
        "python": sys.version.split()[0],
        "returncode": completed.returncode,
        "passed": passed,
        "failed": failed,
        "xfailed": xfailed,
        "expected_failure": known,
        "baseline_match": passed == 69 and failed == 1 and xfailed == 1 and known in transcript,
    }
    (output / "TEST_BASELINE.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["baseline_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
