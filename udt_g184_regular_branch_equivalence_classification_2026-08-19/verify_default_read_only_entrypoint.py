#!/usr/bin/env python3
"""Verify that the default G184 verifier invocation is read-only."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def hashes():
    return {path.name: sha256(path) for path in ROOT.iterdir() if path.is_file()}


def run():
    before = hashes()
    env = dict(os.environ)
    env.pop("UDT_WRITE_VERIFICATION_RESULT", None)
    env["G184_SKIP_DEFAULT_CHECK"] = "1"
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
        "audit": "G184",
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
    if result["status"] != "PASS":
        raise SystemExit(json.dumps(result, sort_keys=True))
    print("PASS: G184 default verify_package.py entrypoint is read-only")


if __name__ == "__main__":
    run()
