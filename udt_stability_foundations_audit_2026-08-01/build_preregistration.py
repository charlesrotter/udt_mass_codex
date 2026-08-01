#!/usr/bin/env python3
"""Freeze the preregistered stability-foundations source paths and bytes."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "5adeb59dde063770c0619d37b76b03f735d82038"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    paths = [line.strip() for line in (HERE / "SOURCE_PATHS.txt").read_text().splitlines() if line.strip()]
    assert len(paths) == len(set(paths))
    tracked = set(subprocess.run(["git", "ls-tree", "-r", "--name-only", BASE], cwd=ROOT,
                                 check=True, text=True, capture_output=True).stdout.splitlines())
    assert all(path in tracked for path in paths), sorted(set(paths) - tracked)
    rows = []
    manifest = []
    for path in paths:
        data = subprocess.run(["git", "show", f"{BASE}:{path}"], cwd=ROOT, check=True,
                              capture_output=True).stdout
        current = (ROOT / path).read_bytes()
        assert current == data
        digest = sha(data)
        rows.append({"path": path, "sha256": digest, "bytes": len(data), "base": BASE})
        manifest.append(f"{digest}  ../{path}")
    with (HERE / "SOURCE_INVENTORY.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=("path", "sha256", "bytes", "base"), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (HERE / "SOURCE_MANIFEST.sha256").write_text("\n".join(manifest) + "\n")
    snapshot = {
        "base": BASE,
        "source_paths": len(paths),
        "source_paths_sha256": sha((HERE / "SOURCE_PATHS.txt").read_bytes()),
        "source_inventory_sha256": sha((HERE / "SOURCE_INVENTORY.tsv").read_bytes()),
        "source_manifest_sha256": sha((HERE / "SOURCE_MANIFEST.sha256").read_bytes()),
        "premise_rows": sum(1 for _ in (HERE / "PREMISE_LEDGER.tsv").open()) - 1,
        "maximum_conclusion": "premise-scoped stability-foundations architecture only",
    }
    (HERE / "PREREG_SNAPSHOT.json").write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n")
    print(json.dumps(snapshot, sort_keys=True))


if __name__ == "__main__":
    main()
