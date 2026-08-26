#!/usr/bin/env python3
"""Build a sealed G270 fresh-review intake under /tmp."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g270_review_", dir="/tmp"))
    package_copy = destination / PACKAGE.name
    shutil.copytree(PACKAGE, package_copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    for row in sources:
        source = REPO / row["path"]
        assert source.is_file() and sha256(source) == row["sha256"]
        target = destination / "private_sources" / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    payloads = sorted(
        path for path in destination.rglob("*")
        if path.is_file() and path.name not in {"REVIEW_SCOPE.json", "REVIEW_MANIFEST.tsv"}
    )
    manifest = destination / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        for path in payloads:
            writer.writerow((path.relative_to(destination), sha256(path), path.stat().st_size))

    scope = {
        "package": PACKAGE.name,
        "review": "fresh_read_only_adversarial",
        "payload_count": len(payloads),
        "manifest_sha256": sha256(manifest),
        "allowed": [
            "inspect sealed intake",
            "run registered no-write replays",
            "run bounded checks in an ephemeral copy",
        ],
        "forbidden": [
            "edit evidence files",
            "continue research",
            "inspect repository outside intake",
            "inspect observational outcomes or protected packages",
            "import distance history Xmax source matter transfer signalling or canon",
        ],
    }
    scope_path = destination / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(destination),
        "payload_count": len(payloads),
        "total_file_count": len(payloads) + 2,
        "scope_sha256": sha256(scope_path),
        "manifest_sha256": sha256(manifest),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
