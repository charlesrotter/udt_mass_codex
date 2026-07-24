#!/usr/bin/env python3
"""Freeze the second additions-only source correction."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PATHS = PACKAGE / "SOURCE_PATHS_CORRECTION_02.txt"
OUTPUT = PACKAGE / "SOURCE_MANIFEST_CORRECTION_02.tsv"


def lines(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def git_blob(path: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> None:
    original = set(lines(PACKAGE / "SOURCE_PATHS.txt"))
    correction_01 = set(lines(PACKAGE / "SOURCE_PATHS_CORRECTION_01.txt"))
    correction_02 = lines(PATHS)
    prior = original | correction_01
    if len(original) != 97 or len(correction_01) != 4 or len(prior) != 101:
        raise SystemExit("prior source-universe count mismatch")
    if len(correction_02) != 35 or len(set(correction_02)) != 35:
        raise SystemExit(f"correction-02 count mismatch: {len(correction_02)}")
    if prior & set(correction_02):
        raise SystemExit("correction 02 overlaps prior source universe")
    if len(prior | set(correction_02)) != 136:
        raise SystemExit("effective source-universe count mismatch")
    output = ["path\tgit_blob\tbytes\tsha256"]
    for path in correction_02:
        artifact = ROOT / path
        if not artifact.is_file():
            raise SystemExit(f"missing correction source: {path}")
        data = artifact.read_bytes()
        output.append(
            f"{path}\t{git_blob(path)}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}"
        )
    OUTPUT.write_text("\n".join(output) + "\n", encoding="utf-8")
    print("froze 35 correction sources; effective universe 136")


if __name__ == "__main__":
    main()
