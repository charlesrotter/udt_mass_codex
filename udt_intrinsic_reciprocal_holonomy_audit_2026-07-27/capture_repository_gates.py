#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    result = subprocess.run(
        [sys.executable, str(HERE / "verify_repository_gates.py")], cwd=ROOT,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    payload = json.loads(result.stdout)
    assert payload["result"] == "PASS"
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS repository gate capture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
