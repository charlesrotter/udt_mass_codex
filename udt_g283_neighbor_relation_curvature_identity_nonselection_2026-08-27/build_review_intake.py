#!/usr/bin/env python3
"""Build a sealed, source-bounded G283 external-review intake."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    output = arguments.output or Path(tempfile.mkdtemp(prefix="udt_g283_review_", dir="/tmp"))
    output.mkdir(parents=True, exist_ok=True)

    package_files = sorted(
        path for path in PACKAGE.iterdir()
        if path.is_file() and path.name not in {"build_review_intake.py"}
    )
    with (PACKAGE / "SOURCE_SCOPE.tsv").open(newline="", encoding="utf-8") as stream:
        sources = [ROOT / row["path"] for row in csv.DictReader(stream, delimiter="\t")]

    payload_paths: list[Path] = []
    package_target = output / PACKAGE.name
    package_target.mkdir()
    for source in package_files:
        target = package_target / source.name
        shutil.copy2(source, target)
        payload_paths.append(target)
    for source in sources:
        target = output / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payload_paths.append(target)

    scope = {
        "audit": "G283_FRESH_EXTERNAL_ADVERSARIAL_REVIEW",
        "mode": "read_only_source_bounded",
        "package": PACKAGE.name,
        "scientific_landing_must_not_be_strengthened": True,
        "allowed_actions": [
            "inspect_manifest_payloads",
            "run_registered_checks_in_writable_ephemeral_copy",
            "perform_bounded_read_only_independent_checks",
        ],
        "forbidden_actions": [
            "edit_evidence_files",
            "continue_research",
            "access_repository_outside_intake",
            "access_protected_packages",
            "import_observational_outcomes_or_new_physical_laws",
        ],
    }
    scope_path = output / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payload_paths.append(scope_path)

    manifest_path = output / "REVIEW_MANIFEST.tsv"
    with manifest_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=("path", "sha256", "bytes"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        for path in sorted(payload_paths, key=lambda item: str(item.relative_to(output))):
            writer.writerow(
                {
                    "path": str(path.relative_to(output)),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
    seal_path = output / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{sha256(manifest_path)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "intake": str(output),
                "physical_files": sum(1 for path in output.rglob("*") if path.is_file()),
                "manifest_payloads": len(payload_paths),
                "scope_sha256": sha256(scope_path),
                "manifest_sha256": sha256(manifest_path),
                "seal_sha256": sha256(seal_path),
                "symlinks": sum(1 for path in output.rglob("*") if path.is_symlink()),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
