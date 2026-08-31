#!/usr/bin/env python3
"""Build the sealed G307 repair-only follow-up intake."""

from __future__ import annotations

import csv
import json
import shutil
import tempfile
from pathlib import Path

import build_review_intake as base


HERE = Path(__file__).resolve().parent
FOLLOWUP_FILES = base.PACKAGE_FILES + [
    "REPAIR_FOLLOWUP_REQUEST.md",
    "build_repair_followup_intake.py",
]


def main() -> None:
    target = Path(tempfile.mkdtemp(prefix="udt_g307_repair_followup_", dir="/tmp"))
    package_target = target / HERE.name
    package_target.mkdir()
    for name in FOLLOWUP_FILES:
        source = HERE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, package_target / name)

    frozen = target / "frozen_sources"
    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in source_rows:
        source = base.resolve_source(Path(row["path"]))
        if base.digest(source) != row["sha256"]:
            raise AssertionError(f"source hash drift: {row['path']}")
        destination = frozen / row["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    frozen_current = target / "frozen_current"
    frozen_current.mkdir()
    for name in base.CURRENT_FILES:
        shutil.copy2(base.resolve_current(name), frozen_current / name)

    premise_audit = json.loads((HERE / "PREMISE_AUDIT_RESULT.json").read_text(encoding="utf-8"))
    if base.digest(frozen_current / "CURRENT_SCIENTIFIC_PREMISES.tsv") != premise_audit["registry_sha256"]:
        raise AssertionError("current premise registry drift since G307 audit")

    scope = {
        "schema": "UDT_G307_REPAIR_FOLLOWUP_SCOPE_V1",
        "question": "verify only preregistered G307 repairs R1 through R4 and unchanged landing",
        "package": HERE.name,
        "package_file_count": len(FOLLOWUP_FILES),
        "frozen_source_count": len(source_rows),
        "frozen_current_count": len(base.CURRENT_FILES),
        "allowed": [
            "read intake",
            "verify only R1 through R4 and unchanged bounded landing",
            "run registered checks in a writable ephemeral copy",
            "write response outside intake",
        ],
        "forbidden": [
            "edit evidence files",
            "continue research",
            "change scientific question or landing",
            "access repository or protected packages",
            "use internet or unsealed observations",
            "import field equation action source matter model population mass law fit scale or X_max",
        ],
    }
    scope_path = target / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    payloads = sorted(path for path in target.rglob("*") if path.is_file())
    manifest = target / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["sha256", "bytes", "path"])
        for path in payloads:
            writer.writerow([
                base.digest(path), path.stat().st_size, path.relative_to(target).as_posix()
            ])
    seal = target / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{base.digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(target),
        "manifest_payloads": len(payloads),
        "total_files": len(payloads) + 2,
        "scope_sha256": base.digest(scope_path),
        "manifest_sha256": base.digest(manifest),
        "detached_seal_sha256": base.digest(seal),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
