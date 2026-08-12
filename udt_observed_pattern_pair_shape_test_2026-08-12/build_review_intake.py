#!/usr/bin/env python3
"""Build a sealed read-only intake for the pattern-shape adversarial review."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def copy_file(source: Path, target: Path, role: str, records: list[dict[str, object]]) -> None:
    if not source.is_file():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    records.append(
        {
            "role": role,
            "source": str(source),
            "intake_path": str(target.relative_to(target.parents[1])),
            "bytes": target.stat().st_size,
            "sha256": sha256(target),
        }
    )


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_pair_shape_review_", dir="/tmp"))
    records: list[dict[str, object]] = []

    for source in sorted(HERE.iterdir()):
        if not source.is_file() or source.name == "build_review_intake.py":
            continue
        copy_file(source, intake / "package" / source.name, "audit_package", records)

    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    for index, row in enumerate(source_rows, start=1):
        raw = Path(row["path"])
        source = raw if raw.is_absolute() else REPO / raw
        if raw.is_absolute():
            target = intake / "external_sources" / f"{index:02d}_{source.name}"
        else:
            target = intake / "repository_sources" / raw
        copy_file(source, target, row["scope"], records)

    scope = {
        "status": "SEALED_READ_ONLY_REVIEW_INTAKE",
        "schema": "udt-complete-pair-pattern-shape-review-v1",
        "package": HERE.name,
        "n_payload_files": len(records),
        "files": records,
        "restrictions": [
            "read-only",
            "no research continuation",
            "no fitting or history selection",
            "no access outside intake",
            "no protected curvature-atlas access",
            "no stopped native-on-shell draft access",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    for path in intake.rglob("*"):
        if path.is_file():
            os.chmod(path, 0o444)
        elif path.is_dir():
            os.chmod(path, 0o555)
    os.chmod(intake, 0o555)

    print(
        json.dumps(
            {
                "intake": str(intake),
                "request": "package/ADVERSARIAL_REVIEW_REQUEST.md",
                "payload_files": len(records),
                "scope_sha256": sha256(scope_path),
            }
        )
    )


if __name__ == "__main__":
    main()
