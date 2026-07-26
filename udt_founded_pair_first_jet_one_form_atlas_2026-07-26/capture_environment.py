#!/usr/bin/env python3
"""Capture CPU-only audit environment."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys

import sympy


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def main():
    print(json.dumps({
        "schema": "udt-founded-pair-first-jet-environment-1.0",
        "python": sys.version.split()[0],
        "sympy": sympy.__version__,
        "platform": platform.platform(),
        "head_at_capture": git("rev-parse", "HEAD"),
        "branch": git("branch", "--show-current"),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "compute": "CPU_ONLY_EXACT_SYMBOLIC_AND_FRACTION",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
