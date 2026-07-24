#!/usr/bin/env python3
"""Freeze preregistered source identity without interpreting source contents."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PATHS = PACKAGE / "SOURCE_PATHS.txt"
OUTPUT = PACKAGE / "SOURCE_MANIFEST.tsv"


def git_blob(path: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> None:
    rows: list[tuple[str, str, int, str]] = []
    seen: set[str] = set()
    for raw in PATHS.read_text(encoding="utf-8").splitlines():
        path = raw.strip()
        if not path:
            continue
        if path in seen:
            raise SystemExit(f"duplicate source path: {path}")
        seen.add(path)
        artifact = ROOT / path
        if not artifact.is_file():
            raise SystemExit(f"missing source path: {path}")
        data = artifact.read_bytes()
        rows.append((path, git_blob(path), len(data), hashlib.sha256(data).hexdigest()))
    if len(rows) < 80:
        raise SystemExit(f"source census unexpectedly small: {len(rows)}")
    lines = ["path\tgit_blob\tbytes\tsha256"]
    lines.extend("\t".join(map(str, row)) for row in rows)
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"froze {len(rows)} source paths")


if __name__ == "__main__":
    main()
