#!/usr/bin/env python3
"""Build a self-contained sealed G277 read-only review intake under /tmp."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from sealed_source_paths import source_path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g277_review_", dir="/tmp"))
    destination = intake / PACKAGE.name
    for source in sorted(PACKAGE.rglob("*")):
        if not source.is_file() or "__pycache__" in source.parts:
            continue
        target = destination / source.relative_to(PACKAGE)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    frozen_rows: list[dict[str, str]] = []
    frozen_root = intake / "frozen_sources"
    frozen_root.mkdir()
    for index, row in enumerate(source_rows, start=1):
        source = source_path(row["path"], REPO)
        assert digest(source) == row["sha256"]
        target = frozen_root / f"{index:02d}_{source.name}"
        shutil.copy2(source, target)
        assert digest(target) == row["sha256"]
        frozen_rows.append(
            {
                "logical_path": row["path"],
                "sealed_path": str(target.relative_to(intake)),
                "sha256": row["sha256"],
            }
        )

    source_map = intake / "SEALED_SOURCE_MAP.tsv"
    with source_map.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            delimiter="\t",
            fieldnames=("logical_path", "sealed_path", "sha256"),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(frozen_rows)

    package_files = [path for path in destination.rglob("*") if path.is_file()]
    total_files = len(package_files) + len(frozen_rows) + 3
    manifest_entries = total_files - 1
    scope = {
        "status": "SEALED_READ_ONLY_REPAIR_ONLY_FOLLOWUP_INTAKE",
        "package": PACKAGE.name,
        "scientific_landing_commit": "f64d673e",
        "external_repair_preregistration_commit": "15728f76",
        "file_count_including_scope_and_manifest": total_files,
        "manifest_entry_count_excluding_manifest": manifest_entries,
        "review_question": (
            "Verify only external repairs R1 and R2: sealed-versus-repository evidence separation, "
            "distinct source-derived same-object and bridge facts for all eight candidates, exact "
            "agreement with the frozen production census, and the unchanged bounded G277 landing."
        ),
        "allowed": [
            "inspect only this sealed intake",
            "verify only preregistered external repairs R1 and R2 and the retained landing",
            "run registered no-write replays inside the intake",
            "run bounded checks in a writable ephemeral copy",
        ],
        "forbidden": [
            "edit evidence files",
            "continue the research",
            "change the scientific question",
            "access the repository or protected packages outside this intake",
            "inspect unsealed observational outcomes",
            "fit or select a numerical scale, history, metric, kernel, operational distance, or Xmax",
            "reopen any finding outside external repairs R1 and R2",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    payloads = sorted(path for path in intake.rglob("*") if path.is_file())
    assert len(payloads) == manifest_entries
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    with manifest_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        for path in payloads:
            writer.writerow(
                (str(path.relative_to(intake)), digest(path), path.stat().st_size)
            )
    assert len([path for path in intake.rglob("*") if path.is_file()]) == total_files
    print(
        json.dumps(
            {
                "intake": str(intake),
                "file_count": total_files,
                "scope_sha256": digest(scope_path),
                "manifest_sha256": digest(manifest_path),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
