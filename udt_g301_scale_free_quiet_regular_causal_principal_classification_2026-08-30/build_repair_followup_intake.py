#!/usr/bin/env python3
"""Build a sealed G301 repair-only follow-up intake without transmitting it."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PACKAGE_FILES = (
    "MAP.md",
    "PREREGISTRATION.md",
    "REPAIR_PREREGISTRATION.md",
    "PREMISE_LEDGER.tsv",
    "SOURCE_MANIFEST.tsv",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "ARCHITECTURE_CLASSIFICATION.tsv",
    "STATUS_LEDGER.tsv",
    "COMMANDS.md",
    "RUN_RECORD.md",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "INVARIANT_BASIS_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "PACKAGE_VERIFICATION_RESULT.json",
    "derive_principal_classification.py",
    "verify_principal_class_independent.py",
    "verify_invariant_basis_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "EXTERNAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
    "EXTERNAL_REVIEW_GPT54.md",
    "EXTERNAL_REPAIR_FOLLOWUP_REQUEST.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_payload(intake, source, relative, payloads):
    target = intake / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    payloads.append(target.relative_to(intake))


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g301_repair_followup_", dir="/tmp"))
    payloads = []
    for name in PACKAGE_FILES:
        copy_payload(intake, PACKAGE / name, Path(PACKAGE.name) / name, payloads)

    lines = (PACKAGE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    for line in lines[1:]:
        expected, relative, _role = line.split("\t", 2)
        source = ROOT / relative
        if digest(source) != expected:
            raise RuntimeError(f"source drift: {relative}")
        target = intake / relative
        if not target.exists():
            copy_payload(intake, source, Path(relative), payloads)

    scope = {
        "review": "G301 read-only repair-only follow-up R1-R5",
        "mode": "read-only repair-only",
        "allowed": "verify only preregistered R1-R5 and unchanged bounded scientific landing; run checks in writable ephemeral copy",
        "forbidden": (
            "edit evidence; continue research; change scientific question; access repository or "
            "protected packages; use internet or unsealed observations; select law field equation "
            "source action matter scale history or X_max"
        ),
        "package": PACKAGE.name,
        "payload_count": len(payloads),
        "preregistration_commit": "accfc6b9",
        "repair_preregistration_commit": "d964e004",
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payloads.append(scope_path.relative_to(intake))

    manifest = intake / "REVIEW_MANIFEST.tsv"
    rows = ["sha256\tbytes\tpath"]
    for relative in sorted(payloads, key=lambda p: str(p)):
        path = intake / relative
        rows.append(f"{digest(path)}\t{path.stat().st_size}\t{relative}")
    manifest.write_text("\n".join(rows) + "\n", encoding="utf-8")
    seal = intake / "REVIEW_MANIFEST.sha256"
    seal.write_text(f"{digest(manifest)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "intake": str(intake),
                "files": len(payloads) + 2,
                "manifest_payloads": len(payloads),
                "scope_sha256": digest(scope_path),
                "manifest_sha256": digest(manifest),
                "seal_sha256": digest(seal),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
