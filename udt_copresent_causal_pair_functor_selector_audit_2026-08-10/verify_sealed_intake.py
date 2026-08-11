#!/usr/bin/env python3
"""Read-only verification of the exact 14-source repository or sealed-intake layout."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
PROHIBITED = (
    "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02",
    "udt_native_onshell_timelive_reset_owner_audit_2026-08-10",
)
PREREG_COMMIT = "86380447"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))

    assert len(rows) == 14
    assert len({row["path"] for row in rows}) == 14
    assert all(not any(token in row["path"] for token in PROHIBITED) for row in rows)

    sealed_root = PARENT / "sources"
    if all((sealed_root / row["path"]).is_file() for row in rows):
        for row in rows:
            assert digest(sealed_root / row["path"]) == row["sha256"], row["path"]
        layout = "sealed_sources"
    else:
        # The live premise registry legitimately changes when this result is banked. Replay the
        # exact preregistered Git objects rather than pretending current mutable bytes are frozen.
        for row in rows:
            frozen = subprocess.run(
                ["git", "show", f"{PREREG_COMMIT}:{row['path']}"], cwd=PARENT,
                capture_output=True, check=False,
            )
            assert frozen.returncode == 0, row["path"]
            assert hashlib.sha256(frozen.stdout).hexdigest() == row["sha256"], row["path"]
        layout = "preregistered_git_objects"
    print(f"PASS: {len(rows)} exact sources; layout={layout}; prohibited trees absent")


if __name__ == "__main__":
    main()
