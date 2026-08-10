#!/usr/bin/env python3
"""Build a sealed review intake containing this package and its exact pinned sources."""

from __future__ import annotations

import csv
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: build_external_intake.py /tmp/new-empty-directory")
    target = Path(sys.argv[1]).resolve()
    if target.parent != Path("/tmp") or (target.exists() and any(target.iterdir())):
        raise SystemExit("target must be a nonexistent or empty direct child of /tmp")
    package_target = target / HERE.name
    package_target.mkdir(parents=True)
    for source in sorted(HERE.iterdir()):
        if source.is_file():
            shutil.copy2(source, package_target / source.name)

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == 18
    for row in rows:
        raw = subprocess.check_output(("git", "show", row["source_ref"]), cwd=ROOT)
        assert len(raw) == int(row["size"]), row["path"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"], row["path"]
        destination = target / "sources" / row["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)

    manifest_rows = []
    for path in sorted(item for item in target.rglob("*") if item.is_file()):
        relative = path.relative_to(target)
        manifest_rows.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {relative}")
    (target / "INTAKE_MANIFEST.sha256").write_text("\n".join(manifest_rows) + "\n", encoding="utf-8")
    for path in sorted(target.rglob("*"), reverse=True):
        os.chmod(path, 0o555 if path.is_dir() else 0o444)
    os.chmod(target, 0o555)
    print(f"{target}\t{len(manifest_rows) + 1}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
