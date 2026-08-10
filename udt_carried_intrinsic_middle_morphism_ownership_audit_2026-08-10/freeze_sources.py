#!/usr/bin/env python3
"""Freeze the preregistered source scope at the current git commit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SCOPE = HERE / "SOURCE_SCOPE.tsv"
OUT = HERE / "SOURCE_MANIFEST.tsv"
PROTECTED = "udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> None:
    head = git("rev-parse", "HEAD")
    rows = list(csv.DictReader(SCOPE.open(), delimiter="\t"))
    assert rows and len({row["source_id"] for row in rows}) == len(rows)
    assert len({row["path"] for row in rows}) == len(rows)

    manifest = []
    for row in rows:
        path = row["path"]
        assert not path.startswith(PROTECTED), path
        full = ROOT / path
        assert full.is_file(), path
        data = full.read_bytes()
        tracked = git("ls-files", "--error-unmatch", "--", path)
        assert tracked == path
        manifest.append(
            {
                **row,
                "source_ref": f"{head}:{path}",
                "git_blob": git("hash-object", "--", path),
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": str(len(data)),
            }
        )

    fields = [
        "source_id",
        "path",
        "source_ref",
        "git_blob",
        "sha256",
        "size",
        "role",
    ]
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(manifest)
    print(f"head={head}")
    print(f"sources={len(manifest)}")
    print(f"manifest_sha256={hashlib.sha256(OUT.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
