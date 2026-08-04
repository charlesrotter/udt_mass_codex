#!/usr/bin/env python3
"""Prepare and supervise the preregistered exact modular C08 all-zero case."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
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
        "p_Procs_FieldGeneral.so",
        "p_Procs_FieldIndep.so",
        "p_Procs_FieldQ.so",
        "p_Procs_FieldZp.so",
    )
)
LABELS = ("12", "13", "23")
EXPECTED_SOURCE_COUNT = 131
WALL_LIMIT_SECONDS = 86_400
RSS_LIMIT_KIB = 96 * 1024 * 1024
AVAILABLE_FLOOR_KIB = 24 * 1024 * 1024
SWAP_LIMIT_KIB = 8 * 1024 * 1024
POLL_SECONDS = 10
LOG_SECONDS = 60


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def iso_now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def singular_environment() -> dict[str, str]:
    environment = dict(os.environ)
    environment["LD_LIBRARY_PATH"] = str(SINGULAR_LIB)
    environment["LD_PRELOAD"] = ":".join(map(str, POLY_KERNELS))
    return environment


def source_gate() -> str:
    manifest = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest})
    assert len(manifest) == EXPECTED_SOURCE_COUNT
    for row in manifest:
        blob = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
            capture_output=True, check=True,
        ).stdout
        assert len(blob) == int(row["bytes"])
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]
    manifest_hash = digest(HERE / "SOURCE_MANIFEST.tsv")
    assert manifest_hash == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip()
    return manifest_hash


def committed_clean(path: Path) -> str:
    relative = str(path.relative_to(ROOT))
    blob = subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"], cwd=ROOT,
        text=True, capture_output=True, check=True,
    ).stdout.strip()
    committed = subprocess.run(
        ["git", "cat-file", "blob", blob], cwd=ROOT,
        capture_output=True, check=True,
    ).stdout
    assert committed == path.read_bytes(), f"not committed clean: {relative}"
    return blob


def smoke_test() -> dict[str, object]:
    assert SINGULAR.is_file() and all(path.is_file() for path in POLY_KERNELS)
    source = (
        'LIB "modstd.lib";\n'
        "ring r=0,(x,y),dp;\n"
        "ideal I=x2+y,y2+x;\n"
        "ideal G=modStd(I,1);\n"
        'int verified=system("verifyGB",G);\n'
        "int reduction_failures=0;\n"
        "for (int i=1; i<=size(I); i++) { if (reduce(I[i],G,1)!=0) { reduction_failures++; } }\n"
        'print("UDT_TOY_VERIFYGB_BEGIN"); verified; print("UDT_TOY_VERIFYGB_END");\n'
        'print("UDT_TOY_REDUCTIONS_BEGIN"); reduction_failures; print("UDT_TOY_REDUCTIONS_END");\n'
        'print("UDT_EXACT_MODULAR_OPTIMIZED_KERNEL_SMOKE_PASS");\n'
        "quit;\n"
    )
    completed = subprocess.run(
        [str(SINGULAR), "-q", "--no-rc", "--allow-net", "--cpus=4", "--threads=1", "--flint-threads=1"],
        input=source, text=True, capture_output=True,
        env=singular_environment(), check=False,
    )
    stdout_path = HERE / "C08_MODULAR_SMOKE_STDOUT.txt"
    stderr_path = HERE / "C08_MODULAR_SMOKE_STDERR.txt"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    combined = completed.stdout + completed.stderr
    assert completed.returncode == 0
    assert "UDT_EXACT_MODULAR_OPTIMIZED_KERNEL_SMOKE_PASS" in completed.stdout
    assert "Could not find dynamic library" not in combined
    assert "? ERROR" not in combined and "error occurred" not in combined
    assert marker_value(completed.stdout, "TOY_VERIFYGB") == "1"
    assert marker_value(completed.stdout, "TOY_REDUCTIONS") == "0"
    return {
        "returncode": completed.returncode,
        "stdout_sha256": digest(stdout_path),
        "stderr_sha256": digest(stderr_path),
        "optimized_kernel_sha256": {path.name: digest(path) for path in POLY_KERNELS},
        "status": "PASS_WARNING_FREE_EXACT_MODULAR_OPTIMIZED_KERNEL",
    }


def singular_expression(text: str) -> str:
    return text.strip().replace("**", "^").replace("y_ratio", "y").replace("z_ratio", "z")


def construct_input() -> tuple[Path, dict[str, object]]:
    construction = json.loads((HERE / "C08_LINEAR_ELIMINATION_CONSTRUCTION.json").read_text())
    records: list[dict[str, str]] = []
    lines = ['LIB "modstd.lib";', "option(redSB);", "ring r=0,(z,y),dp;"]
    generators: list[str] = []
    for index, (label, component) in enumerate(zip(LABELS, construction["components"]), 1):
        assert component["component"] == label
        for key, prefix in (("A", "a"), ("B", "b")):
            path = ROOT / component[key]["path"]
            assert committed_clean(path)
            assert digest(path) == component[key]["sha256"]
            name = f"{prefix}{index}"
            lines.append(f"poly {name}={singular_expression(path.read_text())};")
            generators.append(name)
            records.append({"name": name, "path": component[key]["path"], "sha256": digest(path)})
    lines.extend((
        f"ideal I={','.join(generators)};",
        'print("UDT_MODSTD_BEGIN");',
        "int t0=timer;",
        "ideal G=modStd(I,1);",
        "int elapsed_ticks=timer-t0;",
        'print("UDT_MODSTD_END");',
        'print("UDT_ELAPSED_TICKS_BEGIN");',
        "elapsed_ticks;",
        'print("UDT_ELAPSED_TICKS_END");',
        'print("UDT_VERIFYGB_BEGIN");',
        'int verified=system("verifyGB",G);',
        "verified;",
        'print("UDT_VERIFYGB_END");',
        "int reduction_failures=0;",
        "for (int i=1; i<=size(I); i++) { if (reduce(I[i],G,1)!=0) { reduction_failures++; } }",
        'print("UDT_REDUCTION_FAILURES_BEGIN");',
        "reduction_failures;",
        'print("UDT_REDUCTION_FAILURES_END");',
        'print("UDT_DIM_BEGIN");',
        "dim(G);",
        'print("UDT_DIM_END");',
        'print("UDT_VDIM_BEGIN");',
        "vdim(G);",
        'print("UDT_VDIM_END");',
        'print("UDT_BASIS_SIZE_BEGIN");',
        "size(G);",
        'print("UDT_BASIS_SIZE_END");',
        'print("UDT_BASIS_BEGIN");',
        "G;",
        'print("UDT_BASIS_END");',
        "quit;",
    ))
    input_path = HERE / "C08_MODULAR_ALL_ZERO_INPUT.sing"
    input_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return input_path, {"generators": records, "input_sha256": digest(input_path)}


def singular_version() -> str:
    completed = subprocess.run(
        [str(SINGULAR), "--version"], text=True, capture_output=True,
        env=singular_environment(), check=True,
    )
    return completed.stdout.splitlines()[0]


def prepare() -> dict[str, object]:
    smoke = smoke_test()
    manifest_hash = source_gate()
    input_path, input_record = construct_input()
    record = {
        "schema": "udt-c08-exact-modular-preparation-1.0",
        "status": "PASS_PREPARED_NOT_LAUNCHED",
        "prepared_at": iso_now(),
        "source_manifest_sha256": manifest_hash,
        "singular_version": singular_version(),
        "smoke": smoke,
        **input_record,
    }
    target = HERE / "C08_MODULAR_PREPARATION.json"
    target.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


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
                    rss[pid] = int(line.split()[1])
                    break
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
    values: dict[str, int] = {}
    for line in Path("/proc/meminfo").read_text().splitlines():
        key, rest = line.split(":", 1)
        values[key] = int(rest.split()[0])
    return values["MemAvailable"], values["SwapTotal"] - values["SwapFree"]


def marker_value(text: str, name: str) -> str | None:
    begin = f"UDT_{name}_BEGIN"
    end = f"UDT_{name}_END"
    if begin not in text or end not in text:
        return None
    middle = text.split(begin, 1)[1].split(end, 1)[0]
    values = [line.strip() for line in middle.splitlines() if line.strip()]
    return values[-1] if values else None


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
    preparation_path = HERE / "C08_MODULAR_PREPARATION.json"
    input_path = HERE / "C08_MODULAR_ALL_ZERO_INPUT.sing"
    committed_clean(preparation_path)
    committed_clean(input_path)
    preparation = json.loads(preparation_path.read_text())
    assert preparation["status"] == "PASS_PREPARED_NOT_LAUNCHED"
    assert preparation["input_sha256"] == digest(input_path)
    assert source_gate() == preparation["source_manifest_sha256"]
    smoke = smoke_test()
    assert smoke["status"] == "PASS_WARNING_FREE_EXACT_MODULAR_OPTIMIZED_KERNEL"

    stdout_path = HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt"
    stderr_path = HERE / "C08_MODULAR_ALL_ZERO_STDERR.txt"
    monitor_path = HERE / "C08_MODULAR_RESOURCE_MONITOR.tsv"
    result_path = HERE / "C08_MODULAR_PROCESS_RESULT.json"
    command = [
        str(SINGULAR), "-q", "--no-rc", "--allow-net", "--cpus=4", "--threads=1",
        "--flint-threads=1",
    ]
    start_wall = time.monotonic()
    start_iso = iso_now()
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
            env=singular_environment(), start_new_session=True,
        )
        with monitor_path.open("w", newline="", encoding="utf-8") as monitor:
            writer = csv.writer(monitor, delimiter="\t", lineterminator="\n")
            writer.writerow(("timestamp", "elapsed_seconds", "processes", "aggregate_rss_kib", "mem_available_kib", "swap_used_kib"))
            next_log = 0.0
            while process.poll() is None:
                elapsed = time.monotonic() - start_wall
                processes, aggregate_rss = proc_snapshot(process.pid)
                available, swap_used = memory_snapshot()
                peak_rss = max(peak_rss, aggregate_rss)
                min_available = min(min_available, available)
                max_swap = max(max_swap, swap_used)
                if elapsed >= next_log:
                    writer.writerow((iso_now(), f"{elapsed:.3f}", processes, aggregate_rss, available, swap_used))
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
                    terminate_group(process)
                    break
                time.sleep(POLL_SECONDS)
        returncode = process.wait()

    stdout_text = stdout_path.read_text(encoding="utf-8", errors="replace")
    verify = marker_value(stdout_text, "VERIFYGB")
    reductions = marker_value(stdout_text, "REDUCTION_FAILURES")
    verified_return = returncode == 0 and verify == "1" and reductions == "0"
    if stop_reason:
        status = "OPEN_RESOURCE_BOUNDED_EXACT_ATTEMPT"
    elif verified_return:
        status = "RETURNED_EXACT_VERIFICATION_PASS_PENDING_INDEPENDENT_REVIEW"
    else:
        status = "OPEN_PROCESS_OR_VERIFICATION_FAILURE"
    result = {
        "schema": "udt-c08-exact-modular-process-1.0",
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
        "verifygb": verify,
        "input_reduction_failures": reductions,
        "source_manifest_sha256": preparation["source_manifest_sha256"],
        "smoke": smoke,
    }
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True), flush=True)
    return 0 if verified_return else 2


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
