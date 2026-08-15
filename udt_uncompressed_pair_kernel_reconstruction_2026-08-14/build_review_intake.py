#!/usr/bin/env python3
"""Build a sealed read-only review intake from the package and exact source manifest."""

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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = args.output or Path(tempfile.mkdtemp(prefix="udt_uncompressed_pair_review_", dir="/tmp"))
    if args.output:
        output.mkdir(parents=True, exist_ok=False)

    package_files = sorted(
        path for path in HERE.iterdir()
        if path.is_file() and path.name != "EXTERNAL_ADVERSARIAL_REVIEW.md"
    )
    with (HERE / "SOURCE_MANIFEST.tsv").open() as handle:
        source_paths = [ROOT / row["path"] for row in csv.DictReader(handle, delimiter="\t")]

    payload: dict[str, Path] = {}
    for path in package_files + source_paths:
        relative = str(path.relative_to(ROOT))
        if relative in payload and payload[relative] != path:
            raise SystemExit(f"intake path collision: {relative}")
        if path.is_symlink() or not path.is_file():
            raise SystemExit(f"non-regular intake source: {relative}")
        payload[relative] = path

    records = []
    for relative, source in sorted(payload.items()):
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        destination.chmod(0o444)
        records.append({"path": relative, "bytes": destination.stat().st_size, "sha256": sha256(destination)})

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
        },
        "explicit_exclusions": [
            "protected curvature/holonomy atlas",
            "stopped native-on-shell draft",
            "G88 SNe/Xmax AM control except no file from it is listed",
            "all repository files not copied into this intake",
        ],
    }
    scope_path = output / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
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
