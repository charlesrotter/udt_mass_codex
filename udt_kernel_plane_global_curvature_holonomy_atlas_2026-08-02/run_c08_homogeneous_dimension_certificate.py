#!/usr/bin/env python3
"""Prepare and supervise the corrected homogeneous C08 certificate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import signal
import subprocess
import time
from pathlib import Path

import run_c08_finite_field_dimension_certificate as affine


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIME = 32_003
WALL_LIMIT_SECONDS = 3_600
RSS_LIMIT_KIB = 32 * 1024 * 1024
AVAILABLE_FLOOR_KIB = 64 * 1024 * 1024
SWAP_LIMIT_KIB = 4 * 1024 * 1024
OUTPUT_LIMIT_BYTES = 2 * 1024 * 1024 * 1024
POLL_SECONDS = 2
LOG_SECONDS = 30


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def committed_clean(path: Path) -> str:
    return affine.committed_clean(path)


def source_gate() -> tuple[int, str]:
    manifest = HERE / "C08_HOMOGENEOUS_SOURCE_MANIFEST.tsv"
    rows = list(csv.DictReader(manifest.open(newline="", encoding="utf-8"), delimiter="\t"))
    assert rows and len(rows) == len({row["path"] for row in rows})
    required = {
        str((HERE / name).relative_to(ROOT))
        for name in (
            "C08_HOMOGENEOUS_DIMENSION_CERTIFICATE_PREREGISTRATION.md",
            "C08_FINITE_FIELD_DIMENSION_ARGUMENT_CORRECTION.md",
            "C08_FINITE_FIELD_INPUT.sing",
            "C08_FINITE_FIELD_STDOUT.txt",
            "C08_FINITE_FIELD_PROCESS.json",
            "C08_MODULAR_ALL_ZERO_STDOUT.txt",
            "run_c08_homogeneous_dimension_certificate.py",
            "verify_c08_homogeneous_dimension_certificate_independent.py",
        )
    }
    assert required <= {row["path"] for row in rows}
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
            capture_output=True, check=True,
        ).stdout
        assert len(content) == int(row["bytes"])
        assert hashlib.sha256(content).hexdigest() == row["sha256"]
    manifest_hash = digest(manifest)
    assert manifest_hash == (HERE / "C08_HOMOGENEOUS_SOURCE_MANIFEST.sha256").read_text().strip()
    return len(rows), manifest_hash


def homogeneous_program(polynomials: list[tuple[str, str]], toy: bool = False) -> str:
    variables = "(x,y,t)" if toy else "(z,y,t)"
    lines = ["option(redSB);", f"ring r={PRIME},{variables},dp;"]
    homogeneous_names = []
    for index, (name, expression) in enumerate(polynomials, 1):
        hname = f"F{index}"
        lines.extend((f"poly {name}={expression};", f"poly {hname}=homog({name},t);"))
        homogeneous_names.append(hname)
    lines.extend((
        f"ideal L={','.join(homogeneous_names)};",
        "int i,j; int dehom_failures=0; int homogeneity_failures=0;",
    ))
    for index, (name, _) in enumerate(polynomials, 1):
        lines.extend((
            f"if (subst(F{index},t,1)-{name}!=0) {{ dehom_failures++; }}",
            f"if (homog(F{index},t)-F{index}!=0) {{ homogeneity_failures++; }}",
        ))
    lines.extend((
        'print("UDT_HOMOGENEOUS_BEGIN");',
        "int t0=timer;", "matrix U;", "ideal K=liftstd(L,U);", "int elapsed=timer-t0;",
        'print("UDT_HOMOGENEOUS_END");',
        'print("UDT_PRIME_BEGIN");', str(PRIME) + ";", 'print("UDT_PRIME_END");',
        'print("UDT_DEHOM_FAILURES_BEGIN");', "dehom_failures;", 'print("UDT_DEHOM_FAILURES_END");',
        'print("UDT_INPUT_HOMOGENEITY_FAILURES_BEGIN");', "homogeneity_failures;", 'print("UDT_INPUT_HOMOGENEITY_FAILURES_END");',
        'print("UDT_VERIFYGB_BEGIN");', 'int verified=system("verifyGB",K);', "verified;", 'print("UDT_VERIFYGB_END");',
        "if (verified==1) { attrib(K,\"isSB\",1); }",
        "int reduction_failures=0; int basis_homogeneity_failures=0;",
        "for (i=1;i<=size(L);i++) { if (reduce(L[i],K,1)!=0) { reduction_failures++; } }",
        "for (i=1;i<=size(K);i++) { if (homog(K[i],t)-K[i]!=0) { basis_homogeneity_failures++; } }",
        "matrix R=matrix(L)*U-matrix(K);", "int residual_nonzero=size(ideal(R));",
        "int mi=0; int mj=0;",
        "for (i=1;i<=nrows(U);i++) { for (j=1;j<=ncols(U);j++) { if (mi==0 && U[i,j]!=0) { mi=i; mj=j; } } }",
        "matrix UM=U; if (mi>0) { UM[mi,mj]=UM[mi,mj]+1; }",
        "int mutation_caught=(mi>0 && size(ideal(matrix(L)*UM-matrix(K)))>0);",
        'print("UDT_REDUCTION_FAILURES_BEGIN");', "reduction_failures;", 'print("UDT_REDUCTION_FAILURES_END");',
        'print("UDT_BASIS_HOMOGENEITY_FAILURES_BEGIN");', "basis_homogeneity_failures;", 'print("UDT_BASIS_HOMOGENEITY_FAILURES_END");',
        'print("UDT_TRANSFORM_RESIDUAL_BEGIN");', "residual_nonzero;", 'print("UDT_TRANSFORM_RESIDUAL_END");',
        'print("UDT_MUTATION_CAUGHT_BEGIN");', "mutation_caught;", 'print("UDT_MUTATION_CAUGHT_END");',
        'print("UDT_DIM_BEGIN");', "dim(K);", 'print("UDT_DIM_END");',
        'print("UDT_MULT_BEGIN");', "mult(K);", 'print("UDT_MULT_END");',
        'print("UDT_BASIS_SIZE_BEGIN");', "size(K);", 'print("UDT_BASIS_SIZE_END");',
        'print("UDT_MATRIX_ROWS_BEGIN");', "nrows(U);", 'print("UDT_MATRIX_ROWS_END");',
        'print("UDT_MATRIX_COLS_BEGIN");', "ncols(U);", 'print("UDT_MATRIX_COLS_END");',
        'print("UDT_ELAPSED_BEGIN");', "elapsed;", 'print("UDT_ELAPSED_END");',
        'print("UDT_HOMOGENIZED_INPUT_BEGIN");', "L;", 'print("UDT_HOMOGENIZED_INPUT_END");',
        'print("UDT_BASIS_BEGIN");', "K;", 'print("UDT_BASIS_END");',
        'print("UDT_MATRIX_BEGIN");', "U;", 'print("UDT_MATRIX_END");',
        "quit;",
    ))
    return "\n".join(lines) + "\n"


def toy_gate() -> dict[str, object]:
    source = homogeneous_program([("f1", "x2+y"), ("f2", "xy+1")], toy=True)
    completed = subprocess.run(
        [str(affine.SINGULAR), "-q", "--no-rc", "--cpus=1", "--threads=1", "--flint-threads=1"],
        input=source, text=True, capture_output=True,
        env=affine.environment(), timeout=60, check=False,
    )
    stdout_path = HERE / "C08_HOMOGENEOUS_TOY_STDOUT.txt"
    stderr_path = HERE / "C08_HOMOGENEOUS_TOY_STDERR.txt"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    combined = completed.stdout + completed.stderr
    passed = (
        completed.returncode == 0 and affine.marker(completed.stdout, "PRIME") == str(PRIME)
        and affine.marker(completed.stdout, "DEHOM_FAILURES") == "0"
        and affine.marker(completed.stdout, "INPUT_HOMOGENEITY_FAILURES") == "0"
        and affine.marker(completed.stdout, "VERIFYGB") == "1"
        and affine.marker(completed.stdout, "REDUCTION_FAILURES") == "0"
        and affine.marker(completed.stdout, "BASIS_HOMOGENEITY_FAILURES") == "0"
        and affine.marker(completed.stdout, "TRANSFORM_RESIDUAL") == "0"
        and affine.marker(completed.stdout, "MUTATION_CAUGHT") == "1"
        and "? ERROR" not in combined and "error occurred" not in combined
    )
    assert passed
    return {
        "status": "PASS_NONTRIVIAL_HOMOGENEOUS_TRANSFORMATION_TOY",
        "returncode": completed.returncode,
        "stdout_sha256": digest(stdout_path),
        "stderr_sha256": digest(stderr_path),
    }


def prepare() -> dict[str, object]:
    assert affine.prime_gate(PRIME)
    source_count, source_hash = source_gate()
    toy = toy_gate()
    target = HERE / "C08_HOMOGENEOUS_INPUT.sing"
    target.write_text(homogeneous_program(affine.extract_inputs()), encoding="utf-8")
    result = {
        "schema": "udt-c08-homogeneous-preparation-1.0",
        "status": "PASS_PREPARED_NOT_LAUNCHED",
        "prepared_at": affine.iso_now(),
        "prime": PRIME,
        "input_sha256": digest(target),
        "source_count": source_count,
        "source_manifest_sha256": source_hash,
        "toy": toy,
    }
    (HERE / "C08_HOMOGENEOUS_PREPARATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result


def supervise() -> int:
    preparation_path = HERE / "C08_HOMOGENEOUS_PREPARATION.json"
    input_path = HERE / "C08_HOMOGENEOUS_INPUT.sing"
    committed_clean(preparation_path); committed_clean(input_path)
    preparation = json.loads(preparation_path.read_text())
    assert preparation["status"] == "PASS_PREPARED_NOT_LAUNCHED"
    assert preparation["prime"] == PRIME and preparation["input_sha256"] == digest(input_path)
    source_count, source_hash = source_gate()
    assert (source_count, source_hash) == (
        preparation["source_count"], preparation["source_manifest_sha256"]
    )
    for name, expected in (
        ("C08_HOMOGENEOUS_TOY_STDOUT.txt", preparation["toy"]["stdout_sha256"]),
        ("C08_HOMOGENEOUS_TOY_STDERR.txt", preparation["toy"]["stderr_sha256"]),
    ):
        path = HERE / name; committed_clean(path); assert digest(path) == expected

    stdout_path = HERE / "C08_HOMOGENEOUS_STDOUT.txt"
    stderr_path = HERE / "C08_HOMOGENEOUS_STDERR.txt"
    monitor_path = HERE / "C08_HOMOGENEOUS_MONITOR.tsv"
    result_path = HERE / "C08_HOMOGENEOUS_PROCESS.json"
    for path in (stdout_path, stderr_path, monitor_path, result_path):
        assert not path.exists(), f"refusing to overwrite {path.name}"
    command = [
        str(affine.SINGULAR), "-q", "--no-rc", "--cpus=1", "--threads=1", "--flint-threads=1",
    ]
    start_wall, start_iso = time.monotonic(), affine.iso_now()
    stop_reason: str | None = None
    peak_rss, min_available, max_swap = 0, 2**63 - 1, 0
    external_signal: list[int] = []

    def signal_handler(signum: int, _frame: object) -> None:
        external_signal.append(signum)

    signal.signal(signal.SIGTERM, signal_handler); signal.signal(signal.SIGINT, signal_handler)
    with input_path.open("rb") as stdin, stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        process = subprocess.Popen(
            command, stdin=stdin, stdout=stdout, stderr=stderr,
            env=affine.environment(), start_new_session=True,
        )
        with monitor_path.open("w", newline="", encoding="utf-8") as monitor:
            writer = csv.writer(monitor, delimiter="\t", lineterminator="\n")
            writer.writerow((
                "timestamp", "elapsed_seconds", "processes", "aggregate_rss_kib",
                "mem_available_kib", "swap_used_kib", "output_bytes",
            ))
            next_log = 0.0
            while process.poll() is None:
                elapsed = time.monotonic() - start_wall
                processes, aggregate_rss = affine.proc_snapshot(process.pid)
                available, swap_used = affine.memory_snapshot()
                output_bytes = stdout_path.stat().st_size + stderr_path.stat().st_size
                peak_rss = max(peak_rss, aggregate_rss)
                min_available = min(min_available, available)
                max_swap = max(max_swap, swap_used)
                if elapsed >= next_log:
                    writer.writerow((
                        affine.iso_now(), f"{elapsed:.3f}", processes, aggregate_rss,
                        available, swap_used, output_bytes,
                    ))
                    monitor.flush(); next_log += LOG_SECONDS
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
                elif output_bytes >= OUTPUT_LIMIT_BYTES:
                    stop_reason = "OUTPUT_LIMIT"
                if stop_reason:
                    affine.terminate_group(process); break
                time.sleep(POLL_SECONDS)
        returncode = process.wait()

    stdout_text = stdout_path.read_text(encoding="utf-8", errors="replace")
    combined = stdout_text + stderr_path.read_text(encoding="utf-8", errors="replace")
    names = (
        "PRIME", "DEHOM_FAILURES", "INPUT_HOMOGENEITY_FAILURES", "VERIFYGB",
        "REDUCTION_FAILURES", "BASIS_HOMOGENEITY_FAILURES", "TRANSFORM_RESIDUAL",
        "MUTATION_CAUGHT", "DIM", "MULT", "BASIS_SIZE", "MATRIX_ROWS", "MATRIX_COLS",
    )
    fields = {name.lower(): affine.marker(stdout_text, name) for name in names}
    passed = (
        returncode == 0 and not stop_reason and fields["prime"] == str(PRIME)
        and fields["dehom_failures"] == "0" and fields["input_homogeneity_failures"] == "0"
        and fields["verifygb"] == "1" and fields["reduction_failures"] == "0"
        and fields["basis_homogeneity_failures"] == "0" and fields["transform_residual"] == "0"
        and fields["mutation_caught"] == "1" and fields["dim"] == "1" and fields["mult"] == "124"
        and fields["matrix_rows"] == "6" and fields["matrix_cols"] == fields["basis_size"]
        and "? ERROR" not in combined and "error occurred" not in combined
    )
    status = "RETURNED_CERTIFIED_HOMOGENEOUS_FIBER_PENDING_INDEPENDENT_REVIEW" if passed else (
        "OPEN_RESOURCE_BOUNDED_HOMOGENEOUS_ATTEMPT" if stop_reason
        else "OPEN_PROCESS_OR_HOMOGENEOUS_CERTIFICATE_FAILURE"
    )
    result = {
        "schema": "udt-c08-homogeneous-process-1.0", "status": status,
        "command": command, "start_timestamp": start_iso, "stop_timestamp": affine.iso_now(),
        "wall_seconds": time.monotonic() - start_wall, "returncode": returncode,
        "stop_reason": stop_reason, "input_sha256": digest(input_path),
        "stdout_sha256": digest(stdout_path), "stderr_sha256": digest(stderr_path),
        "monitor_sha256": digest(monitor_path), "peak_aggregate_rss_kib": peak_rss,
        "minimum_mem_available_kib": min_available, "maximum_swap_used_kib": max_swap,
        "output_bytes": stdout_path.stat().st_size + stderr_path.stat().st_size,
        "source_count": source_count, "source_manifest_sha256": source_hash, **fields,
    }
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0 if passed else 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true"); parser.add_argument("--run", action="store_true")
    args = parser.parse_args(); assert args.prepare_only != args.run, "choose exactly one mode"
    if args.prepare_only:
        print(json.dumps(prepare(), sort_keys=True)); return 0
    return supervise()


if __name__ == "__main__":
    raise SystemExit(main())
