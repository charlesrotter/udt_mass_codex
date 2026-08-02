#!/usr/bin/env python3
"""Run a bounded command and preserve exact stdout/stderr metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdout", required=True)
    parser.add_argument("--stderr", required=True)
    parser.add_argument("--meta", required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command and args.command[0] == "--" else args.command
    if not command:
        raise SystemExit("missing command")
    completed = subprocess.run(command, capture_output=True, timeout=args.timeout, check=False)
    Path(args.stdout).write_bytes(completed.stdout)
    Path(args.stderr).write_bytes(completed.stderr)
    result = {
        "command": command,
        "exit_code": completed.returncode,
        "stdout_bytes": len(completed.stdout),
        "stdout_sha256": sha(completed.stdout),
        "stderr_bytes": len(completed.stderr),
        "stderr_sha256": sha(completed.stderr),
    }
    Path(args.meta).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
