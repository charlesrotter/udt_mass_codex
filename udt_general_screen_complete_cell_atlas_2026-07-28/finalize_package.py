#!/usr/bin/env python3
"""Capture deterministic runs and freeze the package manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def capture(script: str, label: str) -> None:
    run = subprocess.run([sys.executable, str(HERE / script)], cwd=ROOT, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (HERE / f"{label}_STDOUT.txt").write_text(run.stdout)
    (HERE / f"{label}_STDERR.txt").write_text(run.stderr)
    if run.returncode:
        raise SystemExit(f"{script} failed with {run.returncode}")


def write_manifest() -> None:
    excluded = {"SHA256SUMS.txt"}
    rows = []
    for path in sorted(HERE.iterdir(), key=lambda p: p.name):
        if path.is_file() and path.name not in excluded and "__pycache__" not in path.parts:
            rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n")
    (HERE / "SHA256SUMS.txt").write_text("".join(rows))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pre-external", action="store_true")
    args = parser.parse_args()
    capture("freeze_sources.py", "SOURCE_FREEZE")
    capture("derive_general_screen.py", "DERIVATION")
    capture("verify_general_screen_independent.py", "INDEPENDENT")
    if not args.pre_external:
        capture("verify_audit.py", "VERIFICATION")

    environment = {
        "schema": "udt-general-screen-run-environment-1.0",
        "python": platform.python_version(),
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "cpu_only": True,
        "base": "73833fa4e75152e51d24f8056b6856dd835785f7",
        "commands": [
            f"python3 {HERE.name}/freeze_sources.py",
            f"python3 {HERE.name}/derive_general_screen.py",
            f"python3 {HERE.name}/verify_general_screen_independent.py",
            f"python3 {HERE.name}/verify_audit.py",
        ],
        "fresh_external_complete": not args.pre_external,
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(environment, indent=2, sort_keys=True)+"\n")
    (HERE / "COMMANDS.txt").write_text("\n".join(environment["commands"])+"\n")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, check=True,
                          stdout=subprocess.PIPE).stdout.strip()
    phase = "PRE_EXTERNAL_EVIDENCE_CAPTURE" if args.pre_external else "FINAL_VERIFIED_CAPTURE"
    (HERE / "RUN_LOG.md").write_text(
        "# Run log\n\n"
        f"- phase: `{phase}`\n"
        f"- execution HEAD: `{head}`\n"
        f"- Python: `{platform.python_version()}`\n"
        f"- SymPy: `{sympy.__version__}`\n"
        "- device: `CPU_ONLY`\n"
        "- production and independent scripts exited zero\n"
        f"- fresh zero-context review: `{'COMPLETE' if not args.pre_external else 'PENDING'}`\n"
    )
    write_manifest()
    print(json.dumps({"status": "PASS", "phase": phase, "files_hashed": len((HERE / "SHA256SUMS.txt").read_text().splitlines())}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
