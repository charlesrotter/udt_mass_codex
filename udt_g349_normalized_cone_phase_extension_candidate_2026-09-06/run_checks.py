"""Capture this package's bounded checks, including intentional code mutants.

Prints actual command/stdout/stderr/exit records; writes no files. Must run from
the repository root. No verdict on the analytic proof or scientific acceptance.
"""
import json
from pathlib import Path
import subprocess
import sys
import time

package = Path(__file__).parent
runs = []
for mutation in [None, 'acceleration_zero', 'pullback_only', 'omit_frequency', 'area_radius']:
    command = [sys.executable, str(package/'check_exact.py')]
    if mutation:
        command += ['--mutation', mutation]
    start = time.monotonic()
    proc = subprocess.run(command, text=True, capture_output=True, timeout=60)
    runs.append({'command': command, 'mutation': mutation, 'returncode': proc.returncode,
                 'stdout': proc.stdout, 'stderr': proc.stderr,
                 'elapsed_seconds': time.monotonic()-start})
print(json.dumps({'runs': runs}, indent=2))
