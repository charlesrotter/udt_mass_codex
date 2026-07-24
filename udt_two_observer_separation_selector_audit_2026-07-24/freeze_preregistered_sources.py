#!/usr/bin/env python3
"""Freeze exact base identities for the preregistered source set."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "566686f0d05b149792b4e266e78d112830a77579"


def git(*args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr.decode("utf-8", "replace"))
    return completed.stdout


def main() -> None:
    paths = [
        line.strip()
        for line in (HERE / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(paths) != 50 or len(set(paths)) != 50:
        raise AssertionError("expected 50 unique preregistered source paths")
    rows = []
    for index, path in enumerate(paths, 1):
        payload = git("show", f"{BASE}:{path}")
        rows.append(
            {
                "source_id": f"SRC{index:03d}",
                "path": path,
                "git_blob": git("rev-parse", f"{BASE}:{path}").decode().strip(),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "size_bytes": len(payload),
            }
        )
    with (HERE / "SOURCE_MANIFEST.tsv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["source_id", "path", "git_blob", "sha256", "size_bytes"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)
    identity = hashlib.sha256("\n".join(paths).encode()).hexdigest()
    print(f"source_count={len(paths)}")
    print(f"path_identity_sha256={identity}")


if __name__ == "__main__":
    main()
