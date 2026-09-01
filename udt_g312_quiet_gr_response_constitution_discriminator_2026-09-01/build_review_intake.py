#!/usr/bin/env python3
"""Build a sealed, self-contained G312 external-review intake under /tmp."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent

PACKAGE_FILES = (
    "MAP.md",
    "PONDER.md",
    "PREREGISTRATION.md",
    "PREREGISTRATION_ANCESTRY.md",
    "PREMISE_LEDGER.tsv",
    "SOURCE_SCOPE.tsv",
    "EXACT_DERIVATION.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "RUN_RECORD.md",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "PACKAGE_VERIFICATION_RESULT.json",
    "derive_response_constitution.py",
    "verify_response_constitution_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "EXTERNAL_REVIEW_REQUEST.md",
    "build_review_intake.py",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g312_review_", dir="/tmp"))
    package_target = intake / "package"
    package_target.mkdir()
    for name in PACKAGE_FILES:
        shutil.copy2(PACKAGE / name, package_target / name)

    sources_target = intake / "sources"
    for row in csv.DictReader((PACKAGE / "SOURCE_SCOPE.tsv").open(encoding="utf-8", newline=""), delimiter="\t"):
        source = ROOT / row["path"]
        target = sources_target / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            shutil.copy2(source, intake / "CURRENT_SCIENTIFIC_PREMISES.tsv")

    scope = {
        "question": "G312 quiet-GR response-constitution ownership discriminator",
        "mode": "fresh read-only adversarial review",
        "allowed": ["inspect intake", "run checks in writable ephemeral copy"],
        "forbidden": [
            "edit evidence",
            "continue research",
            "access repository or protected packages",
            "use unsealed observations",
            "adopt a postulate or select a history scale source action matter model or X_max",
        ],
        "required_verdicts": [
            "G312_ACCEPTED_WITH_TWO_PREMISE_BOUNDARY",
            "G312_REPAIRABLE_DEFECTS__LANDING_RETAINED",
            "G312_SCIENTIFIC_LANDING_REFUTED",
            "G312_REVIEW_INCOMPLETE",
        ],
    }
    (intake / "REVIEW_SCOPE.json").write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    payloads = sorted(path for path in intake.rglob("*") if path.is_file())
    manifest = intake / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "bytes", "sha256"))
        for path in payloads:
            writer.writerow((path.relative_to(intake).as_posix(), path.stat().st_size, digest(path)))
    seal = intake / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(intake),
        "payloads": len(payloads),
        "total_files": len(payloads) + 2,
        "scope_sha256": digest(intake / "REVIEW_SCOPE.json"),
        "manifest_sha256": digest(manifest),
        "detached_seal_sha256": digest(seal),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
