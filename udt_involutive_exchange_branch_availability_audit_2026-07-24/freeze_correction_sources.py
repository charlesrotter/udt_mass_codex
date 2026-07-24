#!/usr/bin/env python3
"""Freeze the additions-only source correction without rewriting prereg evidence."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PATHS = PACKAGE / "SOURCE_PATHS_CORRECTION_01.txt"
OUTPUT = PACKAGE / "SOURCE_MANIFEST_CORRECTION_01.tsv"
ORIGINAL = PACKAGE / "SOURCE_PATHS.txt"


def git_blob(path: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> None:
    original = {line.strip() for line in ORIGINAL.read_text().splitlines() if line.strip()}
    corrected: list[str] = []
    for raw in PATHS.read_text(encoding="utf-8").splitlines():
        path = raw.strip()
        if not path:
            continue
        if path in original or path in corrected:
            raise SystemExit(f"non-disjoint or duplicate correction path: {path}")
        corrected.append(path)
    if len(corrected) != 4 or len(original | set(corrected)) != 101:
        raise SystemExit("effective source-universe count mismatch")
    lines = ["path\tgit_blob\tbytes\tsha256"]
    for path in corrected:
        artifact = ROOT / path
        if not artifact.is_file():
            raise SystemExit(f"missing correction source: {path}")
        data = artifact.read_bytes()
        lines.append(
            f"{path}\t{git_blob(path)}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}"
        )
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("froze 4 correction sources; effective universe 101")


if __name__ == "__main__":
    main()
