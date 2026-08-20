#!/usr/bin/env python3
"""Build a sealed, read-only G185 adversarial-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g185_review_"))
    package_target = intake / HERE.name
    package_target.mkdir()
    excluded = {
        "EXTERNAL_ADVERSARIAL_REVIEW_RAW.md",
        "EXTERNAL_ADVERSARIAL_REVIEW_TRANSCRIPT.txt.gz",
        "TRANSMISSION_RECORD.md",
    }
    for source in sorted(HERE.iterdir()):
        if source.is_file() and source.name not in excluded:
            shutil.copy2(source, package_target / source.name)

    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 14:
        raise RuntimeError("expected 14 registered sources")
    for index, row in enumerate(rows, start=1):
        source = Path(row["path"])
        if not source.is_absolute():
            source = ROOT / source
        if not source.is_file() or sha256(source) != row["sha256"]:
            raise RuntimeError(f"source integrity failure: {row['path']}")
        # Flatten external absolute paths into numbered immutable source records.
        safe_name = f"{index:02d}_{source.name}"
        target = intake / "sources" / safe_name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    files = []
    for path in sorted(item for item in intake.rglob("*") if item.is_file()):
        files.append({
            "path": str(path.relative_to(intake)),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        })
    scope = {
        "audit": "G185",
        "mode": "read-only adversarial review",
        "allowed_root": str(intake),
        "payload_file_count": len(files),
        "files": files,
        "restrictions": [
            "inspect only this sealed intake",
            "do not edit files",
            "do not continue the research",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(intake),
        "payload_files": len(files),
        "total_files": len(files) + 1,
        "review_scope_sha256": sha256(scope_path),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
