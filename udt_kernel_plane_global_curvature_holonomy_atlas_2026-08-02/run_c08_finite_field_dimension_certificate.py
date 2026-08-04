#!/usr/bin/env python3
"""Prepare and supervise the preregistered C08 finite-field dimension certificate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import signal
import subprocess
import time
from datetime import datetime
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SINGULAR_ROOT = Path("/tmp/udt_singular_local")
SINGULAR = SINGULAR_ROOT / "usr/bin/Singular"
SINGULAR_LIB = SINGULAR_ROOT / "usr/lib/x86_64-linux-gnu"
POLY_KERNELS = tuple(
    SINGULAR_ROOT / "usr/libexec/x86_64-linux-gnu/singular/MOD" / name
    for name in (
        "p_Procs_FieldGeneral.so", "p_Procs_FieldIndep.so",
        "p_Procs_FieldQ.so", "p_Procs_FieldZp.so",
    )
)
PRIME = 32_003
EXPECTED_RATIONAL_INPUT_SHA256 = "8079b60cbe573ffefe0557a92b0c35f35b2e6a6a413bc26c5f99a85fc7c96ec0"
EXPECTED_RATIONAL_BASIS_SHA256 = "a785441f0bb6fc5bb8f631861a84336660f8508e729780a6e40459868070479b"
WALL_LIMIT_SECONDS = 3_600
RSS_LIMIT_KIB = 32 * 1024 * 1024
AVAILABLE_FLOOR_KIB = 64 * 1024 * 1024
SWAP_LIMIT_KIB = 4 * 1024 * 1024
OUTPUT_LIMIT_BYTES = 2 * 1024 * 1024 * 1024
POLL_SECONDS = 2
LOG_SECONDS = 30


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def environment() -> dict[str, str]:
    result = dict(os.environ)
    result["LD_LIBRARY_PATH"] = str(SINGULAR_LIB)
    result["LD_PRELOAD"] = ":".join(map(str, POLY_KERNELS))
    return result


def committed_clean(path: Path) -> str:
    relative = str(path.relative_to(ROOT))
    blob = subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"], cwd=ROOT,
        text=True, capture_output=True, check=True,
    ).stdout.strip()
    content = subprocess.run(
        ["git", "cat-file", "blob", blob], cwd=ROOT,
        capture_output=True, check=True,
    ).stdout
    assert content == path.read_bytes(), f"not committed clean: {relative}"
    return blob


def source_gate() -> tuple[int, str]:
    manifest = HERE / "C08_FINITE_FIELD_SOURCE_MANIFEST.tsv"
    rows = list(csv.DictReader(manifest.open(newline="", encoding="utf-8"), delimiter="\t"))
    assert rows and len(rows) == len({row["path"] for row in rows})
    required = {
        str((HERE / name).relative_to(ROOT))
        for name in (
            "C08_FINITE_FIELD_DIMENSION_CERTIFICATE_PREREGISTRATION.md",
            "C08_MODULAR_ALL_ZERO_INPUT.sing",
            "C08_MODULAR_ALL_ZERO_STDOUT.txt",
            "C08_MODULAR_INDEPENDENT_VERIFICATION.json",
            "C08_MODULAR_RETURN_STATUS.md",
            "C08_MODULAR_TRANSFORMATION_4H_RETURN_STATUS.md",
            "run_c08_finite_field_dimension_certificate.py",
            "verify_c08_finite_field_dimension_certificate_independent.py",
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
    assert manifest_hash == (HERE / "C08_FINITE_FIELD_SOURCE_MANIFEST.sha256").read_text().strip()
    return len(rows), manifest_hash


def prime_gate(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def marker(text: str, name: str) -> str | None:
    begin, end = f"UDT_{name}_BEGIN", f"UDT_{name}_END"
    if begin not in text or end not in text:
        return None
    values = [line.strip() for line in text.split(begin, 1)[1].split(end, 1)[0].splitlines() if line.strip()]
    return values[-1] if values else None


def certificate_program(polynomials: list[tuple[str, str]], toy: bool = False) -> str:
    variables = "(x,y)" if toy else "(z,y)"
    names = [name for name, _ in polynomials]
    lines = ["option(redSB);", f"ring r={PRIME},{variables},dp;"]
    lines.extend(f"poly {name}={expression};" for name, expression in polynomials)
    lines.extend((
        f"ideal I={','.join(names)};",
        'print("UDT_FINITE_FIELD_BEGIN");',
        "int t0=timer;", "matrix T;", "ideal H=liftstd(I,T);", "int elapsed=timer-t0;",
        'print("UDT_FINITE_FIELD_END");',
        'print("UDT_PRIME_BEGIN");', str(PRIME) + ";", 'print("UDT_PRIME_END");',
        'print("UDT_VERIFYGB_BEGIN");', 'int verified=system("verifyGB",H);', "verified;", 'print("UDT_VERIFYGB_END");',
        "if (verified==1) { attrib(H,\"isSB\",1); }",
        "int i,j; int reduction_failures=0;",
        "for (i=1;i<=size(I);i++) { if (reduce(I[i],H,1)!=0) { reduction_failures++; } }",
        "matrix R=matrix(I)*T-matrix(H);",
        "int residual_nonzero=size(ideal(R));",
        "int mi=0; int mj=0;",
        "for (i=1;i<=nrows(T);i++) { for (j=1;j<=ncols(T);j++) { if (mi==0 && T[i,j]!=0) { mi=i; mj=j; } } }",
        "matrix TM=T; if (mi>0) { TM[mi,mj]=TM[mi,mj]+1; }",
        "int mutation_caught=(mi>0 && size(ideal(matrix(I)*TM-matrix(H)))>0);",
        'print("UDT_REDUCTION_FAILURES_BEGIN");', "reduction_failures;", 'print("UDT_REDUCTION_FAILURES_END");',
        'print("UDT_TRANSFORM_RESIDUAL_BEGIN");', "residual_nonzero;", 'print("UDT_TRANSFORM_RESIDUAL_END");',
        'print("UDT_MUTATION_CAUGHT_BEGIN");', "mutation_caught;", 'print("UDT_MUTATION_CAUGHT_END");',
        'print("UDT_DIM_BEGIN");', "dim(H);", 'print("UDT_DIM_END");',
        'print("UDT_VDIM_BEGIN");', "vdim(H);", 'print("UDT_VDIM_END");',
        'print("UDT_BASIS_SIZE_BEGIN");', "size(H);", 'print("UDT_BASIS_SIZE_END");',
        'print("UDT_MATRIX_ROWS_BEGIN");', "nrows(T);", 'print("UDT_MATRIX_ROWS_END");',
        'print("UDT_MATRIX_COLS_BEGIN");', "ncols(T);", 'print("UDT_MATRIX_COLS_END");',
        'print("UDT_ELAPSED_BEGIN");', "elapsed;", 'print("UDT_ELAPSED_END");',
        'print("UDT_BASIS_BEGIN");', "H;", 'print("UDT_BASIS_END");',
        'print("UDT_MATRIX_BEGIN");', "T;", 'print("UDT_MATRIX_END");',
        "quit;",
    ))
    return "\n".join(lines) + "\n"


def extract_inputs() -> list[tuple[str, str]]:
    path = HERE / "C08_MODULAR_ALL_ZERO_INPUT.sing"
    committed_clean(path)
    assert digest(path) == EXPECTED_RATIONAL_INPUT_SHA256
    rows = re.findall(r"^poly ([ab][123])=(.*);$", path.read_text(), re.MULTILINE)
    assert [name for name, _ in rows] == ["a1", "b1", "a2", "b2", "a3", "b3"]
    return rows


def toy_gate() -> dict[str, object]:
    source = certificate_program([("f1", "x2+y"), ("f2", "xy+1")], toy=True)
    completed = subprocess.run(
        [str(SINGULAR), "-q", "--no-rc", "--cpus=1", "--threads=1", "--flint-threads=1"],
        input=source, text=True, capture_output=True, env=environment(), timeout=60, check=False,
    )
    stdout_path = HERE / "C08_FINITE_FIELD_TOY_STDOUT.txt"
    stderr_path = HERE / "C08_FINITE_FIELD_TOY_STDERR.txt"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    combined = completed.stdout + completed.stderr
    passed = (
        completed.returncode == 0 and marker(completed.stdout, "PRIME") == str(PRIME)
        and marker(completed.stdout, "VERIFYGB") == "1"
        and marker(completed.stdout, "REDUCTION_FAILURES") == "0"
        and marker(completed.stdout, "TRANSFORM_RESIDUAL") == "0"
        and marker(completed.stdout, "MUTATION_CAUGHT") == "1"
        and "? ERROR" not in combined and "error occurred" not in combined
    )
    assert passed
    return {
        "status": "PASS_NONTRIVIAL_FINITE_FIELD_TRANSFORMATION_TOY",
        "returncode": completed.returncode,
        "stdout_sha256": digest(stdout_path),
        "stderr_sha256": digest(stderr_path),
    }


def prepare() -> dict[str, object]:
    assert prime_gate(PRIME)
    assert SINGULAR.is_file() and all(path.is_file() for path in POLY_KERNELS)
    source_count, source_hash = source_gate()
    rational_basis = HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt"
    committed_clean(rational_basis)
    assert digest(rational_basis) == EXPECTED_RATIONAL_BASIS_SHA256
    toy = toy_gate()
    target = HERE / "C08_FINITE_FIELD_INPUT.sing"
    target.write_text(certificate_program(extract_inputs()), encoding="utf-8")
    result = {
        "schema": "udt-c08-finite-field-preparation-1.0",
        "status": "PASS_PREPARED_NOT_LAUNCHED",
        "prepared_at": iso_now(),
        "prime": PRIME,
        "prime_trial_division_pass": True,
        "input_sha256": digest(target),
        "source_count": source_count,
        "source_manifest_sha256": source_hash,
        "rational_input_sha256": EXPECTED_RATIONAL_INPUT_SHA256,
        "rational_basis_sha256": EXPECTED_RATIONAL_BASIS_SHA256,
        "toy": toy,
    }
    (HERE / "C08_FINITE_FIELD_PREPARATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result


def proc_snapshot(root_pid: int) -> tuple[int, int]:
    parents: dict[int, list[int]] = {}
    rss: dict[int, int] = {}
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            stat = (entry / "stat").read_text().split(") ", 1)[1].split()
            pid = int(entry.name)
            parents.setdefault(int(stat[1]), []).append(pid)
            for line in (entry / "status").read_text().splitlines():
                if line.startswith("VmRSS:"):
                    rss[pid] = int(line.split()[1]); break
        except (FileNotFoundError, PermissionError, ProcessLookupError, ValueError):
            continue
    descendants: set[int] = set()
    pending = [root_pid]
    while pending:
        pid = pending.pop()
        if pid in descendants:
            continue
        descendants.add(pid)
        pending.extend(parents.get(pid, ()))
    return len(descendants), sum(rss.get(pid, 0) for pid in descendants)


def memory_snapshot() -> tuple[int, int]:
    values = {}
    for line in Path("/proc/meminfo").read_text().splitlines():
        key, rest = line.split(":", 1)
        values[key] = int(rest.split()[0])
    return values["MemAvailable"], values["SwapTotal"] - values["SwapFree"]


def terminate_group(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return
    os.killpg(process.pid, signal.SIGTERM)
    try:
        process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=10)


def supervise() -> int:
    preparation_path = HERE / "C08_FINITE_FIELD_PREPARATION.json"
    input_path = HERE / "C08_FINITE_FIELD_INPUT.sing"
    committed_clean(preparation_path)
    committed_clean(input_path)
    preparation = json.loads(preparation_path.read_text())
    assert preparation["status"] == "PASS_PREPARED_NOT_LAUNCHED"
    assert preparation["prime"] == PRIME and prime_gate(PRIME)
    assert preparation["input_sha256"] == digest(input_path)
    source_count, source_hash = source_gate()
    assert (source_count, source_hash) == (
        preparation["source_count"], preparation["source_manifest_sha256"]
    )
    for name, expected in (
        ("C08_FINITE_FIELD_TOY_STDOUT.txt", preparation["toy"]["stdout_sha256"]),
        ("C08_FINITE_FIELD_TOY_STDERR.txt", preparation["toy"]["stderr_sha256"]),
    ):
        path = HERE / name
        committed_clean(path)
        assert digest(path) == expected

    stdout_path = HERE / "C08_FINITE_FIELD_STDOUT.txt"
    stderr_path = HERE / "C08_FINITE_FIELD_STDERR.txt"
    monitor_path = HERE / "C08_FINITE_FIELD_MONITOR.tsv"
    result_path = HERE / "C08_FINITE_FIELD_PROCESS.json"
    for path in (stdout_path, stderr_path, monitor_path, result_path):
        assert not path.exists(), f"refusing to overwrite {path.name}"
    command = [
        str(SINGULAR), "-q", "--no-rc", "--cpus=1", "--threads=1", "--flint-threads=1",
    ]
    start_wall, start_iso = time.monotonic(), iso_now()
    stop_reason: str | None = None
    peak_rss, min_available, max_swap = 0, 2**63 - 1, 0
    external_signal: list[int] = []

    def signal_handler(signum: int, _frame: object) -> None:
        external_signal.append(signum)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    with input_path.open("rb") as stdin, stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        process = subprocess.Popen(
            command, stdin=stdin, stdout=stdout, stderr=stderr,
            env=environment(), start_new_session=True,
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
                processes, aggregate_rss = proc_snapshot(process.pid)
                available, swap_used = memory_snapshot()
                output_bytes = stdout_path.stat().st_size + stderr_path.stat().st_size
                peak_rss = max(peak_rss, aggregate_rss)
                min_available = min(min_available, available)
                max_swap = max(max_swap, swap_used)
                if elapsed >= next_log:
                    writer.writerow((
                        iso_now(), f"{elapsed:.3f}", processes, aggregate_rss,
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
                    terminate_group(process); break
                time.sleep(POLL_SECONDS)
        returncode = process.wait()

    stdout_text = stdout_path.read_text(encoding="utf-8", errors="replace")
    combined = stdout_text + stderr_path.read_text(encoding="utf-8", errors="replace")
    fields = {
        name.lower(): marker(stdout_text, name)
        for name in (
            "PRIME", "VERIFYGB", "REDUCTION_FAILURES", "TRANSFORM_RESIDUAL",
            "MUTATION_CAUGHT", "DIM", "VDIM", "BASIS_SIZE", "MATRIX_ROWS", "MATRIX_COLS",
        )
    }
    passed = (
        returncode == 0 and not stop_reason and fields["prime"] == str(PRIME)
        and fields["verifygb"] == "1" and fields["reduction_failures"] == "0"
        and fields["transform_residual"] == "0" and fields["mutation_caught"] == "1"
        and fields["dim"] == "0" and fields["vdim"] == "124"
        and fields["matrix_rows"] == "6" and fields["matrix_cols"] == fields["basis_size"]
        and "? ERROR" not in combined and "error occurred" not in combined
    )
    status = "RETURNED_CERTIFIED_FINITE_FIELD_FIBER_PENDING_INDEPENDENT_REVIEW" if passed else (
        "OPEN_RESOURCE_BOUNDED_FINITE_FIELD_ATTEMPT" if stop_reason
        else "OPEN_PROCESS_OR_CERTIFICATE_FAILURE"
    )
    result = {
        "schema": "udt-c08-finite-field-process-1.0",
        "status": status,
        "command": command,
        "start_timestamp": start_iso,
        "stop_timestamp": iso_now(),
        "wall_seconds": time.monotonic() - start_wall,
        "returncode": returncode,
        "stop_reason": stop_reason,
        "input_sha256": digest(input_path),
        "stdout_sha256": digest(stdout_path),
        "stderr_sha256": digest(stderr_path),
        "monitor_sha256": digest(monitor_path),
        "peak_aggregate_rss_kib": peak_rss,
        "minimum_mem_available_kib": min_available,
        "maximum_swap_used_kib": max_swap,
        "output_bytes": stdout_path.stat().st_size + stderr_path.stat().st_size,
        "source_count": source_count,
        "source_manifest_sha256": source_hash,
        **fields,
    }
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0 if passed else 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    assert args.prepare_only != args.run, "choose exactly one mode"
    if args.prepare_only:
        print(json.dumps(prepare(), sort_keys=True))
        return 0
    return supervise()


if __name__ == "__main__":
    raise SystemExit(main())
