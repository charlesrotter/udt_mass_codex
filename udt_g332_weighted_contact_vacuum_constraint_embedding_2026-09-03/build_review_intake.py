#!/usr/bin/env python3
"""Build a sealed, dependency-free G332 external-review intake under /tmp."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parent
PACKAGE_FILES = (
    "MAP.md", "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "COMPLETENESS_MAP.md",
    "EXECUTION_NOTE.md", "derive_weighted_constraint_embedding.py",
    "verify_weighted_constraint_embedding_independent.py", "run_catch_proofs.py",
    "verify_package.py", "DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json", "PACKAGE_VERIFICATION_RESULT.json", "EXACT_DERIVATION.md",
    "LAY_REPORT.md", "STATUS_LEDGER.tsv", "AUDIT_REPORT.md", "EVIDENCE_GATES.md",
    "COMMANDS.md", "REPLAY_COMMANDS.txt", "RUN_RECORD.md", "SOURCE_SCOPE.tsv",
    "SOURCE_MANIFEST.tsv", "build_source_manifest.py", "build_review_intake.py",
    "verify_review_intake.py", "EXTERNAL_REVIEW_REQUEST.md", "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_TRANSMISSION.md", "REPAIR_PREREGISTRATION.md",
    "REPAIR_FOLLOWUP_REQUEST.md", "EXTERNAL_REPAIR_FOLLOWUP.md",
    "REPAIR_FOLLOWUP_TRANSMISSION.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    rows = list(csv.DictReader((PACKAGE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8"), delimiter="\t"))
    intake = Path(tempfile.mkdtemp(prefix="udt_g332_review_", dir="/tmp"))
    package_out = intake / "package"
    source_out = intake / "sources"
    package_out.mkdir()
    source_out.mkdir()
    copied = []
    for filename in PACKAGE_FILES:
        source = PACKAGE / filename
        if not source.is_file():
            raise SystemExit(f"missing package file: {filename}")
        target = package_out / filename
        shutil.copy2(source, target)
        copied.append(target)
    for row in rows:
        source = REPO / row["path"]
        if (not source.is_file() or source.stat().st_size != int(row["bytes"])
                or digest(source) != row["sha256"]):
            raise SystemExit(f"source manifest drift: {row['path']}")
        target = source_out / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        copied.append(target)

    scope = {
        "review": "read-only G332 repair-only follow-up review",
        "allowed": [
            "inspect only this sealed intake",
            "verify only preregistered repairs R1 and R2 and the unchanged bounded landing",
            "run registered checks in a writable ephemeral copy",
        ],
        "forbidden": [
            "edit evidence files", "continue the research", "access repository or protected packages",
            "use internet or unsealed observations", "import carrier action source matter mass fit scale Xmax",
            "change the scientific question", "promote provisional equations or results into canon",
            "select physical occupancy history topology or branch",
        ],
        "allowed_verdicts": [
            "REPAIRS_ACCEPTED__G332_BOUNDED_SCIENTIFIC_LANDING_RETAINED",
            "REPAIRS_INCOMPLETE__G332_BOUNDED_SCIENTIFIC_LANDING_RETAINED",
            "REFUTE__G332_WEIGHTED_CONSTRAINT_EMBEDDING",
        ],
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    copied.append(scope_path)

    manifest_lines = ["sha256\tbytes\tpath"]
    for path in sorted(copied, key=lambda item: item.relative_to(intake).as_posix()):
        manifest_lines.append(
            f"{digest(path)}\t{path.stat().st_size}\t{path.relative_to(intake).as_posix()}"
        )
    manifest = intake / "REVIEW_MANIFEST.tsv"
    manifest.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    seal = intake / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")
    print(json.dumps({
        "intake": str(intake),
        "file_count": len(copied) + 2,
        "payload_count": len(copied),
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest),
        "seal_sha256": digest(seal),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
