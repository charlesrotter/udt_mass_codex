#!/usr/bin/env python3
"""Build a sealed G187 fresh adversarial-review intake."""

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
    intake = Path(tempfile.mkdtemp(prefix="udt_g187_review_"))
    package_target = intake / HERE.name
    package_target.mkdir()
    for source in sorted(HERE.iterdir()):
        if source.is_file():
            shutil.copy2(source, package_target / source.name)

    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 6:
        raise RuntimeError("expected exactly 6 registered sources")

    sealed_rows = []
    for index, row in enumerate(rows, start=1):
        source = (
            HERE / "FROZEN_CURRENT_SCIENTIFIC_PREMISES.tsv"
            if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv"
            else ROOT / row["path"]
        )
        if not source.is_file() or sha256(source) != row["sha256"]:
            raise RuntimeError(f"source integrity failure: {row['path']}")
        target = intake / "sources" / f"{index:02d}_{source.name}"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        sealed_rows.append({
            "path": str(target.relative_to(intake)),
            "sha256": row["sha256"],
            "role": row["role"],
        })

    with (package_target / "SOURCE_MANIFEST.tsv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "sha256", "role"],
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(sealed_rows)

    files = []
    for path in sorted(item for item in intake.rglob("*") if item.is_file()):
        files.append({
            "path": str(path.relative_to(intake)),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        })
    scope = {
        "audit": "G187",
        "mode": "fresh zero-context read-only adversarial review",
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
    scope_path.write_text(
        json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "intake": str(intake),
        "payload_files": len(files),
        "review_scope_sha256": sha256(scope_path),
        "total_files": len(files) + 1,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
