#!/usr/bin/env python3
"""Freeze the final report-level source correction."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PATHS = PACKAGE / "SOURCE_PATHS_CORRECTION_03.txt"
OUTPUT = PACKAGE / "SOURCE_MANIFEST_CORRECTION_03.tsv"


def load(path: Path) -> list[str]:
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
    prior_files = (
        "SOURCE_PATHS.txt",
        "SOURCE_PATHS_CORRECTION_01.txt",
        "SOURCE_PATHS_CORRECTION_02.txt",
    )
    prior: set[str] = set()
    for name in prior_files:
        values = load(PACKAGE / name)
        if prior & set(values):
            raise SystemExit(f"prior overlap in {name}")
        prior.update(values)
    current = load(PATHS)
    if len(prior) != 136 or len(current) != 14 or len(set(current)) != 14:
        raise SystemExit("source count mismatch")
    if prior & set(current) or len(prior | set(current)) != 150:
        raise SystemExit("correction overlap or effective count mismatch")
    output = ["path\tgit_blob\tbytes\tsha256"]
    for path in current:
        artifact = ROOT / path
        if not artifact.is_file():
            raise SystemExit(f"missing correction source: {path}")
        data = artifact.read_bytes()
        output.append(
            f"{path}\t{git_blob(path)}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}"
        )
    OUTPUT.write_text("\n".join(output) + "\n", encoding="utf-8")
    print("froze 14 correction sources; effective universe 150")


if __name__ == "__main__":
    main()
