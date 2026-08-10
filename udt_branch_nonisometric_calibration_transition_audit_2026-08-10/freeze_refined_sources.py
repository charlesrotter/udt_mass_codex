#!/usr/bin/env python3
"""Freeze preregistered refinement sources and build the transparent union manifest."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIELDS = ("source_id", "path", "source_ref", "git_blob", "sha256", "size", "role")


def read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    initial = read(HERE / "SOURCE_MANIFEST.tsv")
    scope = read(HERE / "SOURCE_SCOPE_REFINEMENT.tsv")
    assert len(initial) == len({row["path"] for row in initial}) == 44
    assert len(scope) == len({row["path"] for row in scope}) == 28
    assert not ({row["path"] for row in initial} & {row["path"] for row in scope})
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()

    refinement = []
    for row in scope:
        path = row["path"]
        data = subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)
        refinement.append(
            {
                "source_id": row["source_id"],
                "path": path,
                "source_ref": f"{commit}:{path}",
                "git_blob": subprocess.check_output(
                    ["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT, text=True
                ).strip(),
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": str(len(data)),
                "role": row["role"],
            }
        )

    write(HERE / "SOURCE_MANIFEST_REFINEMENT.tsv", refinement)
    combined = [dict(row, source_id=f"I{index:02d}") for index, row in enumerate(initial, 1)]
    combined.extend(dict(row, source_id=f"R{index:02d}") for index, row in enumerate(refinement, 1))
    assert len(combined) == len({row["path"] for row in combined}) == 72
    write(HERE / "SOURCE_MANIFEST_CONSOLIDATED.tsv", combined)
    print(f"PASS: froze 28 refinement sources at {commit}; consolidated 72 sources")


if __name__ == "__main__":
    main()
