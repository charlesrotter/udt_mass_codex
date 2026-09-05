#!/usr/bin/env python3
"""Build an exact sealed fresh G351 review intake under /tmp."""

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent.relative_to(ROOT)

PACKAGE_FILES = (
    "ADVERSARIAL_REVIEW_REQUEST.md", "AUDIT_REPORT.md", "BLIND_ADVERSARIAL_REVIEW_RESPONSE.md",
    "CATCH_PROOF_RESULT.json", "COMMANDS.md",
    "COMPLETENESS_MAP.md", "DERIVATION_RESULT.json", "EVIDENCE_GATES.md", "EXACT_DERIVATION.md",
    "FROZEN_PREREGISTRATION_HASHES.tsv", "FROZEN_SOURCE_HASHES.tsv",
    "GIT_PREREGISTRATION_PROOF.txt", "INDEPENDENT_VERIFICATION.json",
    "INTERNAL_VERIFIER_REPAIR_PREREGISTRATION.md", "INTERNAL_VERIFIER_REPAIR_RECORD.md",
    "LAY_REPORT.md", "MAP.md", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md",
    "R2_REPAIR_PREREGISTRATION.md", "R3_REPAIR_PREREGISTRATION.md",
    "R4_COMPLETION_REVIEW_RESPONSE.md", "R4_REPAIR_PREREGISTRATION.md",
    "REPAIR_EXECUTION_RECORD.md",
    "REPAIR_PREMISE_LEDGER.tsv",
    "REPAIR_PREREGISTRATION.md",
    "RUN_RECORD.md", "SOURCE_SCOPE.tsv",
    "STATUS_LEDGER.tsv", "VERIFICATION_RESULT.json", "derive_carried_measure_conservation.py",
    "run_catch_proofs.py", "verify_carried_measure_independent.py", "verify_package.py",
)

ROOT_FILES = (
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/AUDIT_REPORT.md",
    "udt_g349_finite_null_wavefront_patch_area_2026-09-04/AUDIT_REPORT.md",
    "udt_g350_frequency_area_carried_content_ownership_2026-09-05/EXACT_DERIVATION.md",
    "udt_g350_frequency_area_carried_content_ownership_2026-09-05/AUDIT_REPORT.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g351_review_", dir="/tmp"))
    paths = [PACKAGE / name for name in PACKAGE_FILES] + [Path(name) for name in ROOT_FILES]
    scope_path = Path("REVIEW_SCOPE.json")
    declared = sorted(path.as_posix() for path in paths) + [scope_path.as_posix()]
    scope = {
        "date": "2026-09-05",
        "files": declared,
        "maximum_conclusion": (
            "audit only the premise-conditioned source-free label-measure theorem: nonzero "
            "absolutely continuous regular-density area weight q=-1, arbitrary observer weight p, "
            "singular component without ordinary q, and the stated caustic/multiplicity boundary"
        ),
        "payload_count": len(declared),
        "prohibitions": [
            "edit evidence", "continue research", "change the scientific question",
            "browse internet or download", "access repository outside intake",
            "promote the owner-adopted premise to derived or canon",
            "select p source population cross-label physics light transfer or distance",
            "select metric history scale X_max matter model or canon",
        ],
        "review": "fresh read-only adversarial G351 review",
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
