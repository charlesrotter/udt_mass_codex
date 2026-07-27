#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script, out, err):
    proc = subprocess.run([sys.executable, str(HERE / script)], cwd=HERE.parent, capture_output=True)
    (HERE / out).write_bytes(proc.stdout)
    (HERE / err).write_bytes(proc.stderr)
    if proc.returncode:
        raise SystemExit(f"{script} failed with {proc.returncode}")


run("derive_relational_fixed_point.py", "DERIVATION_STDOUT.txt", "DERIVATION_STDERR.txt")
run("verify_relational_fixed_point_independent.py", "INDEPENDENT_STDOUT.txt", "INDEPENDENT_STDERR.txt")
run("verify_audit.py", "VERIFICATION_STDOUT.txt", "VERIFICATION_STDERR.txt")
print("PASS captured production independent and verification runs")
