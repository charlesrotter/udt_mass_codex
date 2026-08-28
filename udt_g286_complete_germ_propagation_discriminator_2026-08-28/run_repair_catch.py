#!/usr/bin/env python3
"""Confirm the repaired aggregate verifier rejects a failed fresh production replay."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="udt_g286_catch_") as temporary:
        copy = Path(temporary) / ROOT.name
        shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns("__pycache__"))
        target = copy / "derive_propagation_discriminator.py"
        text = target.read_text(encoding="utf-8")
        needle = '"sampled_future_tidal_nonzero": max(abs(v) for row in future_t for v in row) > 0.0,'
        replacement = '"sampled_future_tidal_nonzero": False,'
        if text.count(needle) != 1:
            raise AssertionError("hostile mutation target not unique")
        target.write_text(text.replace(needle, replacement), encoding="utf-8")
        replay = subprocess.run(
            [sys.executable, "-S", str(copy / "verify_package.py")],
            cwd=copy, capture_output=True, text=True, check=False,
        )
    result = {
        "mutation": "force fresh production sampled_future_tidal_nonzero false",
        "aggregate_verifier_exit": replay.returncode,
        "rejected": replay.returncode != 0,
    }
    result["pass"] = result["rejected"]
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
