#!/usr/bin/env python3
"""Build a sealed, source-bounded G304 external-review intake."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent


PACKAGE_FILES = [
    "MAP.md",
    "PREREGISTRATION.md",
    "PREREGISTRATION_ANCESTRY.md",
    "PREMISE_LEDGER.tsv",
    "STATUS_LEDGER.tsv",
    "SOURCE_MANIFEST.tsv",
    "GLOBAL_PREMISE_AUDIT.tsv",
    "derive_global_cell_discriminator.py",
    "verify_global_cell_discriminator_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "DERIVATION_RESULT.json",
    "DOMAIN_CLASSIFICATION.tsv",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "PACKAGE_VERIFICATION_RESULT.json",
    "EXACT_DERIVATION.md",
    "LAY_REPORT.md",
    "AUDIT_REPORT.md",
    "EVIDENCE_GATES.md",
    "COMMANDS.md",
    "RUN_RECORD.md",
    "EXTERNAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
    "REPAIR_PREREGISTRATION.md",
    "REPAIR_FOLLOWUP_REQUEST.md",
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--repair-followup", action="store_true")
    args = parser.parse_args()
    if args.output:
        target = Path(args.output).resolve()
        target.mkdir(parents=True, exist_ok=False)
    else:
        target = Path(tempfile.mkdtemp(prefix="udt_g304_review_", dir="/tmp"))

    package_target = target / HERE.name
    package_target.mkdir()
    for name in PACKAGE_FILES:
        source = HERE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, package_target / name)

    sources_target = target / "frozen_sources"
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in source_rows:
        source = REPO / row["path"]
        if digest(source) != row["sha256"]:
            raise AssertionError(f"source hash drift: {row['path']}")
        destination = sources_target / row["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    scope = {
        "schema": "UDT_G304_REPAIR_FOLLOWUP_SCOPE_V1" if args.repair_followup else "UDT_G304_EXTERNAL_REVIEW_SCOPE_V1",
        "question": "G304 registered repairs R1 and R2 only" if args.repair_followup else "bounded global constant-sector discriminator",
        "package": HERE.name,
        "frozen_source_count": len(source_rows),
        "package_file_count": len(PACKAGE_FILES),
        "allowed": ["read intake", "run registered checks in writable ephemeral copy", "write review response outside evidence copy"],
        "forbidden": [
            "edit evidence files",
            "continue research",
            "access repository or protected packages",
            "use internet or unsealed observational outcomes",
            "select field equation, history, source, action, matter, mass, scale, X_max, or canon",
            "change the scientific question or continue beyond registered repairs R1 and R2" if args.repair_followup else "change the registered scientific question",
        ],
    }
    scope_path = target / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

    payloads = sorted(path for path in target.rglob("*") if path.is_file())
    manifest_path = target / "REVIEW_MANIFEST.tsv"
    with manifest_path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["sha256", "bytes", "path"])
        for path in payloads:
            writer.writerow([digest(path), path.stat().st_size, path.relative_to(target).as_posix()])
    seal_path = target / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{digest(manifest_path)}  REVIEW_MANIFEST.tsv\n")

    result = {
        "intake": str(target),
        "manifest_payloads": len(payloads),
        "total_files": len(payloads) + 2,
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest_path),
        "detached_seal_sha256": digest(seal_path),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
