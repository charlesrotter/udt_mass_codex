#!/usr/bin/env python3
"""Run the 34 preregistered exact invariant point jobs in a bounded CPU pool."""

from __future__ import annotations

import concurrent.futures
import json
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCRIPT = HERE / "derive_invariant_certificate.py"
JOBS = [(f"C{i:02d}", point) for i in range(1, 18) for point in ("p1", "p2")]
MAX_WORKERS = 4
TIMEOUT_SECONDS = 600


def run_one(job: tuple[str, str]) -> dict[str, object]:
    candidate, point = job
    command = [sys.executable, str(SCRIPT), "--candidate", candidate, "--point", point]
    started = time.monotonic()
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=TIMEOUT_SECONDS,
        check=False,
    )
    return {
        "candidate_id": candidate,
        "point_id": point,
        "command": command,
        "exit_code": result.returncode,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main() -> int:
    assert len(JOBS) == len(set(JOBS)) == 34
    records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(run_one, job): job for job in JOBS}
        for future in concurrent.futures.as_completed(futures):
            record = future.result()
            records.append(record)
            print(json.dumps({
                "candidate_id": record["candidate_id"],
                "point_id": record["point_id"],
                "exit_code": record["exit_code"],
                "elapsed_seconds": record["elapsed_seconds"],
            }, sort_keys=True), flush=True)
    records.sort(key=lambda row: (row["candidate_id"], row["point_id"]))
    (HERE / "INVARIANT_RUN_LOG.json").write_text(
        json.dumps({
            "schema": "udt-general-screen-invariant-run-log-1.0",
            "max_workers": MAX_WORKERS,
            "per_job_timeout_seconds": TIMEOUT_SECONDS,
            "job_count": len(records),
            "records": records,
        }, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    failures = [record for record in records if record["exit_code"] != 0]
    if failures:
        print(json.dumps({"status": "FAIL", "failed_jobs": len(failures)}, sort_keys=True))
        return 1
    assemble = subprocess.run(
        [sys.executable, str(SCRIPT), "--assemble"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    (HERE / "INVARIANT_ASSEMBLE_STDOUT.txt").write_text(assemble.stdout, encoding="utf-8")
    (HERE / "INVARIANT_ASSEMBLE_STDERR.txt").write_text(assemble.stderr, encoding="utf-8")
    if assemble.returncode != 0:
        print(assemble.stderr, file=sys.stderr)
        return assemble.returncode
    print(assemble.stdout, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
