#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    completed = subprocess.run(
        [sys.executable, str(HERE / "verify_repository_gates.py")], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if completed.returncode:
        raise AssertionError(completed.stderr or completed.stdout)
    result = json.loads(completed.stdout)
    assert result["result"] == "PASS"
    (HERE / "REPOSITORY_GATES.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("PASS repository gate capture")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
