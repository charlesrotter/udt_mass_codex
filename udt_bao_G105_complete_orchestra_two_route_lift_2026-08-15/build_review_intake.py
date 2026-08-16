#!/usr/bin/env python3
"""Build a sealed, read-only G105 review intake."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXCLUDED = {
    "EXTERNAL_REVIEW.md",
    "EXTERNAL_REVIEW_RAW.md",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
    "REVIEW_DISPATCH.md",
}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or Path(tempfile.mkdtemp(prefix="udt_g105_two_route_review_", dir="/tmp"))
    if args.output:
        output.mkdir(parents=True, exist_ok=False)

    package_files = sorted(
        path for path in HERE.iterdir() if path.is_file() and path.name not in EXCLUDED
    )
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(source_rows) != 7:
        raise SystemExit(f"expected 7 source rows, got {len(source_rows)}")

    source_files = []
    for row in source_rows:
        path = ROOT / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            raise SystemExit(f"source mismatch: {row['path']}")
        source_files.append(path)

    payload: dict[str, Path] = {}
    for path in package_files + source_files:
        relative = str(path.relative_to(ROOT))
        if path.is_symlink() or not path.is_file():
            raise SystemExit(f"nonregular payload: {relative}")
        if relative in payload and payload[relative] != path:
            raise SystemExit(f"collision: {relative}")
        payload[relative] = path

    records = []
    for relative, source in sorted(payload.items()):
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        destination.chmod(0o444)
        records.append({
            "path": relative,
            "bytes": destination.stat().st_size,
            "sha256": sha256(destination),
        })

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    scope = {
        "schema": "udt.external_readonly_review_scope.v1",
        "package": HERE.name,
        "git_head": head,
        "payload_count": len(records),
        "payload": records,
        "permissions": {
            "read_only": True,
            "may_edit": False,
            "may_continue_research": False,
            "may_access_outside_intake": False,
            "may_use_internet": False,
        },
        "explicit_exclusions": [
            "all BOSS R2--R5 curves covariances descriptors singular vectors features and outcomes",
            "all CMB outcomes",
            "protected curvature/holonomy atlas",
            "stopped native-on-shell draft",
            "protected G88 package",
            "protected pair-regime-flow package",
            "all repository files not copied into this intake",
        ],
    }
    scope_path = output / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    scope_path.chmod(0o444)
    output.chmod(0o555)
    print(json.dumps({
        "intake": str(output),
        "payload_count": len(records),
        "review_scope_sha256": sha256(scope_path),
        "git_head": head,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
