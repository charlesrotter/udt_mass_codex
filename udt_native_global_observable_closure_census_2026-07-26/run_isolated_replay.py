#!/usr/bin/env python3
"""Run the package verifier with only the explicitly pinned dependency tree."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    pinned = os.environ.get("UDT_PINNED_SITE")
    if not pinned:
        raise SystemExit("set UDT_PINNED_SITE to a directory containing SymPy 1.14.0")
    bootstrap = ("import runpy,sys;"
                 f"sys.path.insert(0,{pinned!r});"
                 f"runpy.run_path({str(HERE / 'verify_package.py')!r},run_name='__main__')")
    command = ["/usr/bin/python3", "-I", "-S", "-c", bootstrap]
    env = dict(os.environ)
    env.update({"CUDA_VISIBLE_DEVICES": "", "PYTHONDONTWRITEBYTECODE": "1", "UDT_PINNED_SITE": pinned})
    run = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
    (HERE / "ISOLATED_STDOUT.txt").write_text(run.stdout, encoding="utf-8")
    (HERE / "ISOLATED_STDERR.txt").write_text(run.stderr, encoding="utf-8")
    normalized_command = ["/usr/bin/python3", "-I", "-S", "-c", "<BOOTSTRAP_WITH_PINNED_SITE>"]
    record = {
        "schema": "udt-native-global-observable-run-environment-1.0",
        "result": "PASS" if run.returncode == 0 else "FAIL",
        "exit_code": run.returncode,
        "command": normalized_command,
        "pinned_dependency": "sympy==1.14.0",
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "cpu_only": True,
        "stdout_sha256": hashlib.sha256(run.stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(run.stderr.encode()).hexdigest(),
    }
    (HERE / "RUN_ENVIRONMENT.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2, sort_keys=True))
    if run.returncode:
        raise SystemExit(run.returncode)


if __name__ == "__main__":
    main()
