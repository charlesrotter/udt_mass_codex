#!/usr/bin/env python3
"""Prove the literal default G183 package-verifier entrypoint is read-only."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hashes():
    return {path.name: digest(path) for path in ROOT.iterdir() if path.is_file()}


def run():
    before = hashes()
    env = dict(os.environ)
    env.pop("UDT_WRITE_VERIFICATION_RESULT", None)
    completed = subprocess.run(
        [sys.executable, "-I", "-S", "verify_package.py"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    after = hashes()
    result = {
        "audit": "G183",
        "status": "PASS" if completed.returncode == 0 and before == after else "FAIL",
        "returncode": completed.returncode,
        "hashes_unchanged": before == after,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }
    if os.environ.get("UDT_WRITE_DEFAULT_ENTRYPOINT_RESULT") == "1":
        (ROOT / "DEFAULT_ENTRYPOINT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    run()
