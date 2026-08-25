#!/usr/bin/env python3
"""Build a sealed, self-contained G258 external-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PACKAGE_FILES = tuple(
    sorted(
        path.name
        for path in ROOT.iterdir()
        if path.is_file() and path.name not in {"EXTERNAL_REVIEW_GPT54.md"}
    )
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g258_review_", dir="/tmp"))
    package_target = intake / ROOT.name
    package_target.mkdir()
    for name in PACKAGE_FILES:
        shutil.copy2(ROOT / name, package_target / name)

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    for source in sources:
        source_path = REPO / source["path"]
        target = intake / source["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if source["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            retained = [
                line
                for line in source_path.read_text().splitlines(keepends=True)
                if not line.startswith("G258\t")
            ]
            target.write_text("".join(retained))
        else:
            shutil.copy2(source_path, target)
        assert digest(target) == source["sha256"], source["path"]

    scope = {
        "package": ROOT.name,
        "purpose": "fresh read-only adversarial review of the bounded G258 landing",
        "restrictions": [
            "intake only",
            "no repository or protected package access",
            "no internet",
            "no evidence edits",
            "no research continuation",
            "replays only in writable ephemeral copy",
            "observational outcomes may not alter the preregistered question or ceiling",
        ],
        "registered_commands_from_package_directory": [
            "python3 verify_package.py",
            "python3 derive_inverse_metric_reconstruction.py",
            "python3 verify_independent.py",
            "python3 run_catch_proofs.py",
        ],
        "package_file_count": len(PACKAGE_FILES),
        "source_file_count": len(sources),
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    payloads = sorted(path for path in intake.rglob("*") if path.is_file() and path != manifest_path)
    with manifest_path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        for path in payloads:
            writer.writerow((path.relative_to(intake), digest(path), path.stat().st_size))

    all_files = sorted(path for path in intake.rglob("*") if path.is_file())
    for path in all_files:
        path.chmod(0o444)
    for directory in sorted((path for path in intake.rglob("*") if path.is_dir()), reverse=True):
        directory.chmod(0o555)
    intake.chmod(0o555)

    print(f"INTAKE={intake}")
    print(f"TOTAL_FILES={len(all_files)}")
    print(f"MANIFEST_ENTRIES={len(payloads)}")
    print(f"REVIEW_SCOPE_SHA256={digest(scope_path)}")
    print(f"REVIEW_MANIFEST_SHA256={digest(manifest_path)}")


if __name__ == "__main__":
    main()
