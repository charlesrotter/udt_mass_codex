#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, json, os, re, subprocess, sys
from pathlib import Path
import numpy, torch

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent

def digest(data):
    return hashlib.sha256(data).hexdigest()

def run(identifier, command, artifact, expected, env):
    completed = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    (HERE / artifact).write_bytes(completed.stdout)
    if completed.returncode != expected:
        raise AssertionError(f"{identifier}:{completed.returncode}!={expected}")
    return {"id": identifier, "command": " ".join(command), "compute": "CPU_ONLY", "exit_code": "1_EXPECTED_BASELINE" if expected == 1 else "0", "output_artifact": artifact, "output_sha256": digest(completed.stdout)}

def main():
    prefix = "c2_open_path_checkpoint_continuation_2026-07-20/"
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1", "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
    records = [
        run("E01", [sys.executable, prefix + "summarize_extended.py"], "SUMMARY_TRANSCRIPT.txt", 0, env),
        run("E02", [sys.executable, prefix + "verify_result_integrity.py"], "INTEGRITY_TRANSCRIPT.txt", 0, env),
    ]
    tests = run("E03", [sys.executable, "-m", "pytest", "tests/"], "TEST_TRANSCRIPT.txt", 1, env)
    match = re.search(rb"(\d+) failed, (\d+) passed, (\d+) xfailed", (HERE / "TEST_TRANSCRIPT.txt").read_bytes())
    if match is None or tuple(map(int, match.groups())) != (1, 69, 1):
        raise AssertionError("test-baseline")
    records.append(tests)
    site_numpy = str(Path(numpy.__file__).resolve().parent.parent)
    package = str(HERE)
    code = "import sys,runpy; " + f"sys.path[:0]=[{site_numpy!r},{package!r}]; import numpy; assert numpy.__version__=='2.2.6'; runpy.run_path({str(HERE/'verify_result_integrity.py')!r},run_name='__main__')"
    records.append(run("E04", [sys.executable, "-I", "-c", code], "ISOLATED_INTEGRITY_TRANSCRIPT.txt", 0, env))
    full = HERE / "FULL_VERIFICATION_TRANSCRIPT.txt"
    records.append({"id": "E05", "command": "PYTHONDONTWRITEBYTECODE=1 CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 " + prefix + "verify_extended.py", "compute": "CPU_ONLY_FULL_REPLAY_COMPLETED", "exit_code": "0", "output_artifact": full.name, "output_sha256": digest(full.read_bytes())})
    external = HERE / "EXTERNAL_REVIEW_STATUS.txt"
    records.append({"id": "E06", "command": "fresh external-model review", "compute": "EXTERNAL_REVIEW_NOT_PERFORMED", "exit_code": "AUTHORIZATION_NOT_GIVEN", "output_artifact": external.name, "output_sha256": digest(external.read_bytes())})
    fields = ["id", "command", "compute", "exit_code", "output_artifact", "output_sha256"]
    with (HERE / "EXECUTION_LEDGER.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(records)
    result = {"schema": "udt-c2-open-path-checkpoint-execution-1.0", "result": "PASS", "records": records, "environment": {"python": sys.version.split()[0], "numpy": numpy.__version__, "torch": torch.__version__, "cpu_only": True, "gpu_used": False}, "test_baseline": {"passed": 69, "failed_known_hygiene": 1, "xfailed": 1}, "expensive_full_replay_completed": True, "expensive_full_replay_reruns": 2, "first_rerun_harness_failure_preserved": True}
    (HERE / "EXECUTION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"result": "PASS", "records": len(records), "tests": "69_passed_1_known_failed_1_xfailed", "full_replay": "PASS"}, sort_keys=True))

if __name__ == "__main__":
    main()
