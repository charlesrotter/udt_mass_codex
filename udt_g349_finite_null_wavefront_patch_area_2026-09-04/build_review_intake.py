#!/usr/bin/env python3
"""Build an exact sealed G349 R1--R4 repair-follow-up intake under /tmp."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent.relative_to(ROOT)

PACKAGE_FILES = (
    "ADVERSARIAL_REVIEW_REQUEST.md", "AUDIT_REPORT.md", "CATCH_PROOF_RESULT.json", "COMMANDS.md",
    "COMPLETENESS_MAP.md", "DERIVATION_RESULT.json", "EVIDENCE_GATES.md", "EXACT_DERIVATION.md",
    "EXTERNAL_REVIEW_ADJUDICATION.md", "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
    "GIT_PREREGISTRATION_PROOF.txt", "INDEPENDENT_VERIFICATION.json", "LAY_REPORT.md", "MAP.md",
    "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "PREREGISTRATION_EXECUTION_NOTE.md",
    "REPAIR_EXECUTION_RECORD.md", "REPAIR_FOLLOWUP_REQUEST.md", "REPAIR_PREREGISTRATION.md",
    "RUN_RECORD.md", "SOURCE_SCOPE.tsv", "STATUS_LEDGER.tsv", "VERIFICATION_RESULT.json",
    "derive_finite_null_patch_area.py", "run_catch_proofs.py",
    "verify_finite_null_patch_area_independent.py", "verify_package.py",
)

ROOT_FILES = (
    "LIVE.md", "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/EXACT_DERIVATION.md",
    "udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/AUDIT_REPORT.md",
    "udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/EXTERNAL_REVIEW_RESPONSE.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g349_repair_followup_", dir="/tmp"))
    paths = [PACKAGE / name for name in PACKAGE_FILES] + [Path(name) for name in ROOT_FILES]
    scope_path = Path("REVIEW_SCOPE.json")
    declared = sorted(path.as_posix() for path in paths) + [scope_path.as_posix()]
    scope = {
        "date": "2026-09-04",
        "files": declared,
        "maximum_conclusion": "verify only preregistered G349 repairs R1-R4 and unchanged bounded scientific landing",
        "payload_count": len(declared),
        "prohibitions": [
            "edit evidence", "continue research", "change scientific question",
            "use internet", "access repository outside intake", "import optics transfer or a field equation",
            "select metric history ray population distance scale X_max or canon",
        ],
        "review": "read-only repair-only G349 R1-R4 follow-up review",
    }
    (intake / scope_path).write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    for relative in paths:
        source = ROOT / relative
        target = intake / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    rows = []
    for relative_name in declared:
        path = intake / relative_name
        rows.append((relative_name, path.stat().st_size, digest(path)))
    manifest = "path\tbytes\tsha256\n" + "".join(
        f"{name}\t{size}\t{sha}\n" for name, size, sha in rows
    )
    manifest_path = intake / "REVIEW_MANIFEST.tsv"
    manifest_path.write_text(manifest, encoding="utf-8")
    seal = digest(manifest_path)
    (intake / "REVIEW_MANIFEST.sha256").write_text(
        f"{seal}  REVIEW_MANIFEST.tsv\n", encoding="utf-8"
    )
    result = {
        "intake": str(intake),
        "manifest_payloads": len(rows),
        "scope_sha256": digest(intake / scope_path),
        "manifest_sha256": seal,
        "detached_seal_sha256": digest(intake / "REVIEW_MANIFEST.sha256"),
        "total_files": sum(1 for path in intake.rglob("*") if path.is_file()),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
