#!/usr/bin/env python3
"""Run the preregistered algebra commands in a clean exported HEAD tree."""

from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COMMANDS = [
    ["python3", "verify_udt_reciprocal_c_postulate.py"],
    ["python3", "udt_observer_pair_clock_operator_audit_2026-07-24/derive_observer_pair_clock_operator.py"],
    ["python3", "udt_observer_pair_clock_operator_audit_2026-07-24/verify_observer_pair_clock_operator_independent.py"],
    ["python3", "udt_relational_pair_depth_realization_audit_2026-07-24/derive_relational_pair_depth.py"],
    ["python3", "udt_relational_pair_depth_realization_audit_2026-07-24/verify_relational_pair_depth_independent.py"],
    ["python3", "udt_complete_physical_comparison_map_audit_2026-07-27/derive_comparison_map.py"],
    ["python3", "udt_complete_physical_comparison_map_audit_2026-07-27/verify_comparison_map_independent.py"],
    ["python3", "udt_global_phi_ownership_overlap_audit_2026-08-05/derive_global_ownership.py"],
    ["python3", "udt_global_phi_ownership_overlap_audit_2026-08-05/independent_global_ownership.py"],
    ["python3", "udt_founding_phi_ownership_morphism_audit_2026-08-05/derive_founding_ownership.py"],
    ["python3", "udt_founding_phi_ownership_morphism_audit_2026-08-05/independent_founding_ownership.py"],
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    archive = subprocess.check_output(["git", "archive", "--format=tar", "HEAD"], cwd=ROOT)
    records: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="udt_phi_regrade_") as temp_name:
        temp = Path(temp_name)
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as handle:
            handle.extractall(temp, filter="data")
        version = subprocess.run(
            ["python3", "-c", "import platform,sympy;print(platform.python_version());print(sympy.__version__)"],
            cwd=temp, capture_output=True, check=True,
        ).stdout.decode().splitlines()
        for index, command in enumerate(COMMANDS, 1):
            started = time.monotonic()
            run = subprocess.run(command, cwd=temp, capture_output=True, timeout=180)
            elapsed = time.monotonic() - started
            stem = f"{index:02d}_" + Path(command[1]).stem
            stdout_name = f"RERUN_{stem}.stdout"
            stderr_name = f"RERUN_{stem}.stderr"
            (HERE / stdout_name).write_bytes(run.stdout)
            (HERE / stderr_name).write_bytes(run.stderr)
            records.append({
                "index": index,
                "command": command,
                "exit_code": run.returncode,
                "elapsed_seconds": round(elapsed, 6),
                "stdout_file": stdout_name,
                "stdout_bytes": len(run.stdout),
                "stdout_sha256": digest(run.stdout),
                "stderr_file": stderr_name,
                "stderr_bytes": len(run.stderr),
                "stderr_sha256": digest(run.stderr),
            })
            if run.returncode != 0:
                break
    result = {
        "schema": "udt.relational_phi_regrade.rerun.v1",
        "head": head,
        "python_version": version[0],
        "sympy_version": version[1],
        "commands_expected": len(COMMANDS),
        "commands_completed": len(records),
        "all_exit_zero": len(records) == len(COMMANDS) and all(row["exit_code"] == 0 for row in records),
        "records": records,
    }
    (HERE / "RERUN_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "records"}, sort_keys=True))
    if not result["all_exit_zero"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
