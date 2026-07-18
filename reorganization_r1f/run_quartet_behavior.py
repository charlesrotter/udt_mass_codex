#!/usr/bin/env python3
"""Run the preregistered quartet in bounded CPU-only processes and retain raw streams."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

import sympy


REPO = Path(__file__).resolve().parents[1]
BATCH = REPO / "reorganization_r1f/PREREGISTERED_BATCH.tsv"


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("pre_move", "post_move"), required=True)
    args = parser.parse_args()
    with BATCH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    output = REPO / "reorganization_r1f" / args.phase
    output.mkdir(parents=True, exist_ok=True)
    records = []
    for row in rows:
        executed = row["current_path"] if args.phase == "pre_move" else row["destination"]
        script = REPO / executed
        if not script.is_file():
            raise AssertionError(f"missing execution path: {executed}")
        command = ["timeout", "30s", "python3", executed]
        env = dict(os.environ)
        env["CUDA_VISIBLE_DEVICES"] = ""
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        started = time.monotonic()
        completed = subprocess.run(command, cwd=REPO, env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, check=False)
        elapsed = time.monotonic() - started
        stem = Path(row["current_path"]).stem
        stdout_path = output / f"{stem}.stdout.txt"
        stderr_path = output / f"{stem}.stderr.txt"
        stdout_path.write_bytes(completed.stdout)
        stderr_path.write_bytes(completed.stderr)
        records.append({
            "phase": args.phase,
            "original_path": row["current_path"],
            "executed_path": executed,
            "exact_command": "env CUDA_VISIBLE_DEVICES= PYTHONDONTWRITEBYTECODE=1 " + shlex.join(command),
            "python_version": sys.version.replace("\n", " "),
            "python_executable": sys.executable,
            "sympy_version": sympy.__version__,
            "timeout_seconds": 30,
            "exit_code": completed.returncode,
            "elapsed_seconds": f"{elapsed:.6f}",
            "stdout_path": str(stdout_path.relative_to(REPO)),
            "stdout_size": len(completed.stdout),
            "stdout_sha256": sha(completed.stdout),
            "stderr_path": str(stderr_path.relative_to(REPO)),
            "stderr_size": len(completed.stderr),
            "stderr_sha256": sha(completed.stderr),
        })
        if completed.returncode != 0:
            raise AssertionError(f"verifier failed: {executed}: {completed.returncode}")
    fields = list(records[0])
    with (output / "BEHAVIOR_RUNS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(records)
    result = {
        "result": "PASS", "phase": args.phase, "runs": len(records),
        "python_version": sys.version.replace("\n", " "),
        "python_executable": sys.executable, "sympy_version": sympy.__version__,
        "all_exit_zero": all(row["exit_code"] == 0 for row in records),
    }
    (output / "BEHAVIOR_SUMMARY.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
