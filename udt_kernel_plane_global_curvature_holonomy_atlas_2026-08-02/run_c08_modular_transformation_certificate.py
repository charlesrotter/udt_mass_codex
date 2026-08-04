#!/usr/bin/env python3
"""Prepare and supervise the exact C08 modular transformation certificate."""

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
LABELS = ("12", "13", "23")
EXPECTED_INPUT_SHA256 = "8079b60cbe573ffefe0557a92b0c35f35b2e6a6a413bc26c5f99a85fc7c96ec0"
EXPECTED_BASIS_STDOUT_SHA256 = "a785441f0bb6fc5bb8f631861a84336660f8508e729780a6e40459868070479b"
WALL_LIMIT_SECONDS = 7_200
RSS_LIMIT_KIB = 64 * 1024 * 1024
AVAILABLE_FLOOR_KIB = 32 * 1024 * 1024
SWAP_LIMIT_KIB = 8 * 1024 * 1024
POLL_SECONDS = 5
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


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def source_gate() -> tuple[int, str]:
    manifest_path = HERE / "SOURCE_MANIFEST.tsv"
    rows = read_tsv(manifest_path)
    assert len(rows) == len({row["path"] for row in rows})
    required = {
        str((HERE / name).relative_to(ROOT))
        for name in (
            "C08_REVERSE_CONTAINMENT_CERTIFICATE_PREREGISTRATION.md",
            "C08_MODULAR_TRANSFORMATION_CERTIFICATE_PREREGISTRATION.md",
            "C08_MODULAR_ALL_ZERO_INPUT.sing",
            "C08_MODULAR_ALL_ZERO_STDOUT.txt",
            "C08_MODULAR_PROCESS_RESULT.json",
            "C08_MODULAR_RETURN_STATUS.md",
            "run_c08_modular_transformation_certificate.py",
            "verify_c08_transformation_certificate_independent.py",
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
    manifest_hash = digest(manifest_path)
    assert manifest_hash == (HERE / "SOURCE_MANIFEST.sha256").read_text().strip()
    return len(rows), manifest_hash


def input_expressions() -> list[str]:
    construction = json.loads((HERE / "C08_LINEAR_ELIMINATION_CONSTRUCTION.json").read_text())
    expressions: list[str] = []
    for label, component in zip(LABELS, construction["components"]):
        assert component["component"] == label
        for key in ("A", "B"):
            path = ROOT / component[key]["path"]
            committed_clean(path)
            assert digest(path) == component[key]["sha256"]
            expressions.append(
                path.read_text().strip().replace("**", "^")
                .replace("z_ratio", "z").replace("y_ratio", "y")
            )
    return expressions


def basis_expressions() -> list[str]:
    stdout_path = HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt"
    committed_clean(stdout_path)
    assert digest(stdout_path) == EXPECTED_BASIS_STDOUT_SHA256
    text = stdout_path.read_text()
    body = text.split("UDT_BASIS_BEGIN", 1)[1].split("UDT_BASIS_END", 1)[0]
    rows = re.findall(r"^G\[(\d+)\]=(.*)$", body, re.MULTILINE)
    assert [int(index) for index, _ in rows] == list(range(1, 10))
    return [expression for _, expression in rows]


PROCEDURES = r'''
proc stdWithTransform(ideal J, ideal Target)
{
  matrix T;
  ideal H=liftstd(J,T);
  int nr=nrows(T)+1;
  int nc=ncols(T);
  matrix W[nr][nc];
  int i,j;
  for (j=1;j<=nc;j++) { W[1,j]=H[j]; }
  for (i=1;i<=nrows(T);i++) { for (j=1;j<=nc;j++) { W[i+1,j]=T[i,j]; } }
  return(W);
}

proc certPrimeTest(int p, alias list args)
{
  ideal J=args[1],args[2];
  int n=ncols(J);
  ideal C;
  intvec sizes;
  number cnt;
  int i;
  for (i=n;i>0;i--)
  {
    C[i]=cleardenom(J[i]);
    cnt=leadcoef(C[i])/leadcoef(J[i]);
    C[i]=numerator(cnt)*var(1)+denominator(cnt);
  }
  sizes=size(J[1..n]);
  def br=basering;
  list lr=ringlist(br);
  lr[1]=p;
  def rp=ring(lr);
  setring rp;
  def Jp=fetch(br,J);
  def Cp=fetch(br,C);
  int ok=(intvec(size(Jp[1..n]))==sizes) && (intvec(size(Cp[1..n]))==2:n);
  setring br;
  return(ok);
}

proc projectedLead(def W)
{
  ideal H;
  int j;
  for (j=1;j<=ncols(W);j++) { H[j]=W[1,j]; }
  ideal L=lead(H);
  attrib(L,"isSB",1);
  return(L);
}

proc certDeleteUnlucky(alias list results)
{
  int count=size(results);
  list categories;
  int cats;
  int i,j;
  ideal L;
  for (i=1;i<=count;i++)
  {
    L=projectedLead(results[i]);
    for (j=1;j<=cats;j++)
    {
      if (nrows(results[i])==categories[j][4] && ncols(results[i])==categories[j][5]
          && size(L)==size(categories[j][1])
          && size(reduce(L,categories[j][1],5))==0
          && size(reduce(categories[j][1],L,5))==0)
      {
        categories[j][2]=categories[j][2]+1;
        categories[j][3][categories[j][2]]=i;
        break;
      }
    }
    if (j>cats)
    {
      cats++;
      categories[cats]=list(L,1,list(i),nrows(results[i]),ncols(results[i]));
    }
  }
  int winner=1;
  for (i=2;i<=cats;i++) { if (categories[i][2]>categories[winner][2]) { winner=i; } }
  list unlucky;
  for (i=1;i<=cats;i++) { if (i!=winner) { unlucky=unlucky+categories[i][3]; } }
  return(unlucky);
}

proc unpackCheck(alias list args, def W)
{
  ideal I=args[1];
  ideal Target=args[2];
  int nc=ncols(W);
  int nr=nrows(W);
  if (nr!=size(I)+1 || nc!=size(Target)) { return(0); }
  ideal H;
  matrix T[nr-1][nc];
  int i,j;
  for (j=1;j<=nc;j++) { H[j]=W[1,j]; }
  for (i=2;i<=nr;i++) { for (j=1;j<=nc;j++) { T[i-1,j]=W[i,j]; } }
  if (size(ideal(matrix(I)*T-matrix(H)))!=0) { return(0); }
  for (j=1;j<=nc;j++) { if (H[j]-Target[j]!=0) { return(0); } }
  if (system("verifyGB",H)!=1) { return(0); }
  attrib(H,"isSB",1);
  for (i=1;i<=size(I);i++) { if (reduce(I[i],H,1)!=0) { return(0); } }
  return(1);
}

proc certPTest(string command, alias list args, alias def result, int p)
{
  def br=basering;
  list lr=ringlist(br);
  lr[1]=p;
  def rp=ring(lr);
  setring rp;
  def Ip=fetch(br,args)[1];
  def Gp=fetch(br,args)[2];
  def Wp=fetch(br,result);
  int ok=unpackCheck(list(Ip,Gp),Wp);
  setring br;
  return(ok);
}

proc certFinal(string command, alias list args, def result)
{
  return(unpackCheck(args,result));
}
'''


def toy_source() -> str:
    return (
        'LIB "modular.lib";\noption(redSB);\n' + PROCEDURES +
        '\nring r=0,(x,y),dp;\n'
        'ideal I=x2+y,xy+1;\n'
        'ideal G=y2-x,xy+1,x2+y;\n'
        'matrix W=modular("stdWithTransform",list(I,G),certPrimeTest,certDeleteUnlucky,certPTest,certFinal);\n'
        'print("UDT_TOY_FINAL_BEGIN"); unpackCheck(list(I,G),W); print("UDT_TOY_FINAL_END");\n'
        'matrix WM=W; WM[2,1]=WM[2,1]+1;\n'
        'print("UDT_TOY_MUTATION_BEGIN"); 1-unpackCheck(list(I,G),WM); print("UDT_TOY_MUTATION_END");\n'
        'print("UDT_TOY_MATRIX_BEGIN"); W; print("UDT_TOY_MATRIX_END");\nquit;\n'
    )


def marker(text: str, name: str) -> str | None:
    start = f"UDT_{name}_BEGIN"
    end = f"UDT_{name}_END"
    if start not in text or end not in text:
        return None
    values = [line.strip() for line in text.split(start, 1)[1].split(end, 1)[0].splitlines() if line.strip()]
    return values[-1] if values else None


def smoke_test() -> dict[str, object]:
    completed = subprocess.run(
        [str(SINGULAR), "-q", "--no-rc", "--allow-net", "--cpus=4", "--threads=1", "--flint-threads=1"],
        input=toy_source(), text=True, capture_output=True, env=environment(), timeout=60, check=False,
    )
    stdout_path = HERE / "C08_TRANSFORMATION_TOY_STDOUT.txt"
    stderr_path = HERE / "C08_TRANSFORMATION_TOY_STDERR.txt"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")
    combined = completed.stdout + completed.stderr
    passed = (
        completed.returncode == 0 and marker(completed.stdout, "TOY_FINAL") == "1"
        and marker(completed.stdout, "TOY_MUTATION") == "1"
        and "? ERROR" not in combined and "error occurred" not in combined
        and "Could not find dynamic library" not in combined
    )
    assert passed
    return {
        "status": "PASS_NONTRIVIAL_EXACT_TRANSFORMATION_TOY",
        "returncode": completed.returncode,
        "stdout_sha256": digest(stdout_path),
        "stderr_sha256": digest(stderr_path),
        "optimized_kernel_sha256": {path.name: digest(path) for path in POLY_KERNELS},
    }


def production_source(inputs: list[str], basis: list[str]) -> str:
    lines = ['LIB "modular.lib";', "option(redSB);", PROCEDURES, "ring r=0,(z,y),dp;"]
    lines.extend(f"poly i{index}={expression};" for index, expression in enumerate(inputs, 1))
    lines.extend(f"poly g{index}={expression};" for index, expression in enumerate(basis, 1))
    lines.extend((
        "ideal I=i1,i2,i3,i4,i5,i6;",
        "ideal G=g1,g2,g3,g4,g5,g6,g7,g8,g9;",
        'print("UDT_TRANSFORMATION_BEGIN");',
        "int t0=timer;",
        'matrix W=modular("stdWithTransform",list(I,G),certPrimeTest,certDeleteUnlucky,certPTest,certFinal);',
        "int elapsed_ticks=timer-t0;",
        'print("UDT_TRANSFORMATION_END");',
        'print("UDT_CERTIFICATE_FINAL_BEGIN");', "unpackCheck(list(I,G),W);", 'print("UDT_CERTIFICATE_FINAL_END");',
        "matrix WM=W; WM[2,1]=WM[2,1]+1;",
        'print("UDT_CERTIFICATE_MUTATION_BEGIN");', "1-unpackCheck(list(I,G),WM);", 'print("UDT_CERTIFICATE_MUTATION_END");',
        'print("UDT_CERTIFICATE_ELAPSED_BEGIN");', "elapsed_ticks;", 'print("UDT_CERTIFICATE_ELAPSED_END");',
        'print("UDT_CERTIFICATE_ROWS_BEGIN");', "nrows(W);", 'print("UDT_CERTIFICATE_ROWS_END");',
        'print("UDT_CERTIFICATE_COLS_BEGIN");', "ncols(W);", 'print("UDT_CERTIFICATE_COLS_END");',
        'print("UDT_CERTIFICATE_MATRIX_BEGIN");', "W;", 'print("UDT_CERTIFICATE_MATRIX_END");',
        "quit;",
    ))
    return "\n".join(lines) + "\n"


def prepare() -> dict[str, object]:
    assert SINGULAR.is_file() and all(path.is_file() for path in POLY_KERNELS)
    source_count, source_hash = source_gate()
    smoke = smoke_test()
    inputs = input_expressions()
    basis = basis_expressions()
    original_input = HERE / "C08_MODULAR_ALL_ZERO_INPUT.sing"
    committed_clean(original_input)
    assert digest(original_input) == EXPECTED_INPUT_SHA256
    target = HERE / "C08_TRANSFORMATION_CERTIFICATE_INPUT.sing"
    target.write_text(production_source(inputs, basis), encoding="utf-8")
    record = {
        "schema": "udt-c08-transformation-preparation-1.0",
        "status": "PASS_PREPARED_NOT_LAUNCHED",
        "prepared_at": iso_now(),
        "source_count": source_count,
        "source_manifest_sha256": source_hash,
        "input_sha256": digest(target),
        "frozen_original_input_sha256": digest(original_input),
        "frozen_basis_stdout_sha256": digest(HERE / "C08_MODULAR_ALL_ZERO_STDOUT.txt"),
        "toy": smoke,
    }
    (HERE / "C08_TRANSFORMATION_PREPARATION.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
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
    values: dict[str, int] = {}
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
    preparation_path = HERE / "C08_TRANSFORMATION_PREPARATION.json"
    input_path = HERE / "C08_TRANSFORMATION_CERTIFICATE_INPUT.sing"
    committed_clean(preparation_path)
    committed_clean(input_path)
    preparation = json.loads(preparation_path.read_text())
    assert preparation["status"] == "PASS_PREPARED_NOT_LAUNCHED"
    assert preparation["input_sha256"] == digest(input_path)
    source_count, source_hash = source_gate()
    assert source_count == preparation["source_count"]
    assert source_hash == preparation["source_manifest_sha256"]
    smoke = smoke_test()
    assert smoke["status"] == "PASS_NONTRIVIAL_EXACT_TRANSFORMATION_TOY"

    stdout_path = HERE / "C08_TRANSFORMATION_CERTIFICATE_STDOUT.txt"
    stderr_path = HERE / "C08_TRANSFORMATION_CERTIFICATE_STDERR.txt"
    monitor_path = HERE / "C08_TRANSFORMATION_CERTIFICATE_MONITOR.tsv"
    result_path = HERE / "C08_TRANSFORMATION_CERTIFICATE_PROCESS.json"
    command = [
        str(SINGULAR), "-q", "--no-rc", "--allow-net", "--cpus=4", "--threads=1", "--flint-threads=1",
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
            env=environment(), start_new_session=True,
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
                if stop_reason:
                    terminate_group(process); break
                time.sleep(POLL_SECONDS)
        returncode = process.wait()

    stdout_text = stdout_path.read_text(encoding="utf-8", errors="replace")
    final = marker(stdout_text, "CERTIFICATE_FINAL")
    mutation = marker(stdout_text, "CERTIFICATE_MUTATION")
    rows = marker(stdout_text, "CERTIFICATE_ROWS")
    cols = marker(stdout_text, "CERTIFICATE_COLS")
    combined = stdout_text + stderr_path.read_text(encoding="utf-8", errors="replace")
    passed = (
        returncode == 0 and not stop_reason and final == "1" and mutation == "1"
        and rows == "7" and cols == "9" and "? ERROR" not in combined
        and "error occurred" not in combined and "Could not find dynamic library" not in combined
    )
    status = "RETURNED_EXACT_TRANSFORMATION_PENDING_INDEPENDENT_REVIEW" if passed else (
        "OPEN_RESOURCE_BOUNDED_TRANSFORMATION_ATTEMPT" if stop_reason else "OPEN_PROCESS_OR_CERTIFICATE_FAILURE"
    )
    result = {
        "schema": "udt-c08-transformation-process-1.0",
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
        "certificate_final": final,
        "mutation_caught": mutation,
        "matrix_rows": rows,
        "matrix_columns": cols,
        "source_count": source_count,
        "source_manifest_sha256": source_hash,
        "toy": smoke,
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
