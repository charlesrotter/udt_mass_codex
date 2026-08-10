#!/usr/bin/env python3
"""Build a sealed read-only G56 intake containing exactly the 20 pinned sources."""

from __future__ import annotations

import csv
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXCLUDE = {
    "EXTERNAL_REVIEW.md", "EXTERNAL_REVIEW_RAW.md", "EXTERNAL_REVIEW_TRANSCRIPT.log",
    "PACKAGE_MANIFEST.sha256", "REPOSITORY_GATES.json",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    destination = Path(tempfile.mkdtemp(prefix="udt_g56_global_descent_review_20260810_", dir="/tmp"))
    package_target = destination / HERE.name
    package_target.mkdir()
    copied: list[Path] = []
    for source in sorted(HERE.iterdir(), key=lambda path: path.name):
        if source.is_file() and source.name not in EXCLUDE:
            target = package_target / source.name
            target.write_bytes(source.read_bytes())
            copied.append(target)

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        sources = list(csv.DictReader(stream, delimiter="\t"))
    assert len(sources) == 20
    for row in sources:
        raw = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        assert len(raw) == int(row["size"])
        assert hashlib.sha256(raw).hexdigest() == row["sha256"]
        target = destination / "sources" / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        copied.append(target)

    lines = [
        f"{digest(path)}  {path.relative_to(destination).as_posix()}"
        for path in sorted(copied, key=lambda item: item.relative_to(destination).as_posix())
    ]
    manifest = destination / "INTAKE_MANIFEST.sha256"
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    for path in copied + [manifest]:
        os.chmod(path, 0o444)
    for directory, subdirectories, _ in os.walk(destination, topdown=False):
        for subdirectory in subdirectories:
            os.chmod(Path(directory) / subdirectory, 0o555)
    os.chmod(destination, 0o555)
    print(destination)
    print(f"files={len(copied) + 1}")
    print(f"sources={len(sources)}")
    print(f"manifest_sha256={digest(manifest)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
