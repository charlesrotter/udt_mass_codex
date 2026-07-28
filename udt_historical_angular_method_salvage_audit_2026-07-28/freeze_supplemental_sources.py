#!/usr/bin/env python3
"""Freeze the explicitly post-discovery current comparison sources."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "fa77ce28c8b5b83e7a6d5a92df2e684b62bb60e6"


def git(*args: str, binary: bool = False):
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if result.returncode:
        message = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise SystemExit(message)
    return result.stdout


def main() -> None:
    rows = ["path\tblob\tsha256\tsize_bytes"]
    paths = [line for line in (HERE / "SUPPLEMENTAL_SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines() if line]
    for path in paths:
        blob = str(git("rev-parse", f"{BASE}:{path}")).strip()
        payload = git("show", f"{BASE}:{path}", binary=True)
        rows.append(f"{path}\t{blob}\t{hashlib.sha256(payload).hexdigest()}\t{len(payload)}")
    (HERE / "SUPPLEMENTAL_SOURCE_MANIFEST.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"supplemental_sources_frozen={len(paths)} base={BASE}")


if __name__ == "__main__":
    main()
