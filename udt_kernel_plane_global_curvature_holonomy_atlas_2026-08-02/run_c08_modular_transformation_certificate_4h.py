#!/usr/bin/env python3
"""Supervise the separately preregistered four-hour C08 continuation."""

from __future__ import annotations

import csv
import json
import os
import signal
import subprocess
import time
from pathlib import Path

import run_c08_modular_transformation_certificate as base


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WALL_LIMIT_SECONDS = 14_400
RSS_LIMIT_KIB = 64 * 1024 * 1024
AVAILABLE_FLOOR_KIB = 32 * 1024 * 1024
SWAP_LIMIT_KIB = 8 * 1024 * 1024
POLL_SECONDS = 5
LOG_SECONDS = 30
EXPECTED_INPUT_SHA256 = "bf6e00b8f98b7313844139a284b76faff4364579b342356eec60104c5f4db044"
EXPECTED_TWO_HOUR_PROCESS_SHA256 = "4b26737e631d66d8803ffddb00269007c8045b8627dff69029cf0ea2053b34bc"
EXPECTED_TWO_HOUR_MONITOR_SHA256 = "77df5226885e532c7f7c96169cae4f58fe86a76964df6774041dcb40b69e1d1a"


def committed_blob(path: Path) -> str:
    return base.committed_clean(path)


def historical_gate() -> dict[str, object]:
    process_path = HERE / "C08_TRANSFORMATION_CERTIFICATE_PROCESS.json"
    monitor_path = HERE / "C08_TRANSFORMATION_CERTIFICATE_MONITOR.tsv"
    committed_blob(process_path)
    committed_blob(monitor_path)
    assert base.digest(process_path) == EXPECTED_TWO_HOUR_PROCESS_SHA256
    assert base.digest(monitor_path) == EXPECTED_TWO_HOUR_MONITOR_SHA256
    process = json.loads(process_path.read_text())
    assert process["status"] == "OPEN_RESOURCE_BOUNDED_TRANSFORMATION_ATTEMPT"
    assert process["stop_reason"] == "WALL_LIMIT"
    assert process["input_sha256"] == EXPECTED_INPUT_SHA256
    return process


def toy_gate(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command, input=base.toy_source(), text=True, capture_output=True,
        env=base.environment(), timeout=60, check=False,
    )
    stdout_path = HERE / "C08_TRANSFORMATION_4H_TOY_STDOUT.txt"
    stderr_path = HERE / "C08_TRANSFORMATION_4H_TOY_STDERR.txt"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    combined = completed.stdout + completed.stderr
    passed = (
        completed.returncode == 0
        and base.marker(completed.stdout, "TOY_FINAL") == "1"
        and base.marker(completed.stdout, "TOY_MUTATION") == "1"
        and "? ERROR" not in combined
        and "error occurred" not in combined
        and "Could not find dynamic library" not in combined
    )
    assert passed
    return {
        "status": "PASS_NONTRIVIAL_EXACT_TRANSFORMATION_TOY",
        "returncode": completed.returncode,
        "stdout_sha256": base.digest(stdout_path),
        "stderr_sha256": base.digest(stderr_path),
        "optimized_kernel_sha256": {path.name: base.digest(path) for path in base.POLY_KERNELS},
    }


def main() -> int:
    assert base.SINGULAR.is_file() and all(path.is_file() for path in base.POLY_KERNELS)
    driver_blob = committed_blob(Path(__file__))
    prereg_blob = committed_blob(HERE / "C08_MODULAR_TRANSFORMATION_4H_PREREGISTRATION.md")
    old_process = historical_gate()
    source_count, source_hash = base.source_gate()
    input_path = HERE / "C08_TRANSFORMATION_CERTIFICATE_INPUT.sing"
    committed_blob(input_path)
    assert base.digest(input_path) == EXPECTED_INPUT_SHA256

    stdout_path = HERE / "C08_TRANSFORMATION_4H_STDOUT.txt"
    stderr_path = HERE / "C08_TRANSFORMATION_4H_STDERR.txt"
    monitor_path = HERE / "C08_TRANSFORMATION_4H_MONITOR.tsv"
    result_path = HERE / "C08_TRANSFORMATION_4H_PROCESS.json"
    for path in (stdout_path, stderr_path, monitor_path, result_path):
        assert not path.exists(), f"refusing to overwrite {path.name}"

    command = [
        str(base.SINGULAR), "-q", "--no-rc", "--allow-net", "--cpus=4",
        "--threads=1", "--flint-threads=1",
    ]
    toy = toy_gate(command)
    start_wall = time.monotonic()
    start_iso = base.iso_now()
    stop_reason: str | None = None
    peak_rss = 0
    min_available = 2**63 - 1
    max_swap = 0
    external_signal: list[int] = []

    def signal_handler(signum: int, _frame: object) -> None:
        external_signal.append(signum)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    with input_path.open("rb") as stdin, stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        process = subprocess.Popen(
            command, stdin=stdin, stdout=stdout, stderr=stderr,
            env=base.environment(), start_new_session=True,
        )
        with monitor_path.open("w", newline="", encoding="utf-8") as monitor:
            writer = csv.writer(monitor, delimiter="\t", lineterminator="\n")
            writer.writerow((
                "timestamp", "elapsed_seconds", "processes", "aggregate_rss_kib",
                "mem_available_kib", "swap_used_kib",
            ))
            next_log = 0.0
            while process.poll() is None:
                elapsed = time.monotonic() - start_wall
                processes, aggregate_rss = base.proc_snapshot(process.pid)
                available, swap_used = base.memory_snapshot()
                peak_rss = max(peak_rss, aggregate_rss)
                min_available = min(min_available, available)
                max_swap = max(max_swap, swap_used)
                if elapsed >= next_log:
                    writer.writerow((base.iso_now(), f"{elapsed:.3f}", processes, aggregate_rss, available, swap_used))
                    monitor.flush()
                    next_log += LOG_SECONDS
                if external_signal:
                    stop_reason = f"EXTERNAL_SIGNAL_{external_signal[-1]}"
                elif elapsed >= WALL_LIMIT_SECONDS:
                    stop_reason = "WALL_LIMIT"
                elif aggregate_rss >= RSS_LIMIT_KIB:
                    stop_reason = "AGGREGATE_RSS_LIMIT"
                elif available <= AVAILABLE_FLOOR_KIB:
                    stop_reason = "AVAILABLE_MEMORY_FLOOR"
                elif swap_used >= SWAP_LIMIT_KIB:
                    stop_reason = "SWAP_LIMIT"
                if stop_reason:
                    base.terminate_group(process)
                    break
                time.sleep(POLL_SECONDS)
        returncode = process.wait()

    stdout_text = stdout_path.read_text(encoding="utf-8", errors="replace")
    final = base.marker(stdout_text, "CERTIFICATE_FINAL")
    mutation = base.marker(stdout_text, "CERTIFICATE_MUTATION")
    rows = base.marker(stdout_text, "CERTIFICATE_ROWS")
    cols = base.marker(stdout_text, "CERTIFICATE_COLS")
    combined = stdout_text + stderr_path.read_text(encoding="utf-8", errors="replace")
    passed = (
        returncode == 0 and not stop_reason and final == "1" and mutation == "1"
        and rows == "7" and cols == "9" and "? ERROR" not in combined
        and "error occurred" not in combined and "Could not find dynamic library" not in combined
    )
    status = "RETURNED_EXACT_TRANSFORMATION_PENDING_INDEPENDENT_REVIEW" if passed else (
        "OPEN_RESOURCE_BOUNDED_TRANSFORMATION_ATTEMPT" if stop_reason
        else "OPEN_PROCESS_OR_CERTIFICATE_FAILURE"
    )
    result = {
        "schema": "udt-c08-transformation-process-4h-1.0",
        "status": status,
        "command": command,
        "start_timestamp": start_iso,
        "stop_timestamp": base.iso_now(),
        "wall_seconds": time.monotonic() - start_wall,
        "returncode": returncode,
        "stop_reason": stop_reason,
        "input_sha256": base.digest(input_path),
        "stdout_sha256": base.digest(stdout_path),
        "stderr_sha256": base.digest(stderr_path),
        "monitor_sha256": base.digest(monitor_path),
        "peak_aggregate_rss_kib": peak_rss,
        "minimum_mem_available_kib": min_available,
        "maximum_swap_used_kib": max_swap,
        "certificate_final": final,
        "mutation_caught": mutation,
        "matrix_rows": rows,
        "matrix_columns": cols,
        "source_count": source_count,
        "source_manifest_sha256": source_hash,
        "driver_blob": driver_blob,
        "preregistration_blob": prereg_blob,
        "prior_process_sha256": base.digest(HERE / "C08_TRANSFORMATION_CERTIFICATE_PROCESS.json"),
        "prior_status": old_process["status"],
        "toy": toy,
    }
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
