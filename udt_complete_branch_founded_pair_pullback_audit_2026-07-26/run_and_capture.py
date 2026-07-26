#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script, stdout_name, stderr_name):
    proc = subprocess.run([sys.executable, str(HERE / script)], cwd=HERE.parent, capture_output=True)
    (HERE / stdout_name).write_bytes(proc.stdout)
    (HERE / stderr_name).write_bytes(proc.stderr)
    if proc.returncode:
        raise SystemExit(f"{script} failed with {proc.returncode}")


run("derive_complete_branch_pullback.py", "DERIVATION_STDOUT.txt", "DERIVATION_STDERR.txt")
run("verify_complete_branch_independent.py", "INDEPENDENT_STDOUT.txt", "INDEPENDENT_STDERR.txt")
run("verify_audit.py", "VERIFICATION_STDOUT.txt", "VERIFICATION_STDERR.txt")
print("PASS captured production independent and verification runs")
