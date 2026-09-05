#!/usr/bin/env python3
"""Build an exact sealed G352 R2 repair-only follow-up intake under /tmp."""

import hashlib
import json
from pathlib import Path
import shutil
import tempfile


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent.relative_to(ROOT)

PACKAGE_FILES = (
    "ADOPTION_RECORD.md",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "AUDIT_REPORT.md",
    "build_review_intake.py",
    "build_repair_followup_intake.py",
    "CATCH_PROOF_RESULT.json",
    "COMMANDS.md",
    "COMPLETENESS_MAP.md",
    "DERIVATION_RESULT.json",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
    "FROZEN_PREREGISTRATION_HASHES.tsv",
    "FROZEN_SOURCE_HASHES.tsv",
    "GIT_PREREGISTRATION_PROOF.txt",
    "INDEPENDENT_VERIFICATION.json",
    "LAY_REPORT.md",
    "MAP.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "PREREGISTRATION_EXECUTION_NOTE.md",
    "R1_PREREGISTRATION_SIGN_REPAIR.md",
    "R2_PREREGISTRATION_EXTERNAL_REVIEW_REPAIRS.md",
    "R2_REPAIRED_PREMISE_LEDGER.tsv",
    "REPAIR_FOLLOWUP_REVIEW_REQUEST.md",
    "RUN_RECORD.md",
    "SOURCE_SCOPE.tsv",
    "STATUS_LEDGER.tsv",
    "VERIFICATION_RESULT.json",
    "derive_clock_rate_readout.py",
    "run_catch_proofs.py",
    "verify_clock_rate_readout_independent.py",
    "verify_package.py",
)

ROOT_FILES = (
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_g347_arbitrary_endpoint_observer_angular_area_covariance_2026-09-04/EXACT_DERIVATION.md",
    "udt_g348_generic_lorentzian_null_screen_area_theorem_2026-09-04/EXACT_DERIVATION.md",
    "udt_g349_finite_null_wavefront_patch_area_2026-09-04/EXACT_DERIVATION.md",
    "udt_g350_frequency_area_carried_content_ownership_2026-09-05/EXACT_DERIVATION.md",
    "udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/EXACT_DERIVATION.md",
    "udt_g351_source_free_labelwise_carried_measure_conservation_2026-09-05/EXTERNAL_REVIEW_RESPONSE.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g352_repair_followup_", dir="/tmp"))
    paths = [PACKAGE / name for name in PACKAGE_FILES] + [Path(name) for name in ROOT_FILES]
    scope_path = Path("REVIEW_SCOPE.json")
    declared = sorted(path.as_posix() for path in paths) + [scope_path.as_posix()]
    scope = {
        "date": "2026-09-05",
        "files": declared,
        "maximum_conclusion": (
            "verify only preregistered G352 R2 repairs to the continuous-versus-atomic distinction, "
            "nonnegative product measure, explicit supplied factorization, tightened domains, "
            "evidence grading, and unchanged conditional T_clock=R A^-1 landing"
        ),
        "payload_count": len(declared),
        "prohibitions": [
            "edit evidence",
            "continue research or change the scientific question",
            "browse internet download or install packages",
            "access repository or protected packages outside intake",
            "promote owner premise or chosen realization to derived or canon",
            "select p=1 universally or suppress p=0 atomic or other readout types",
            "select phase source population cross-label physics light energy detector or distance",
            "select metric history matter mass scale X_max observations or canon",
        ],
        "review": "read-only G352 R2 repair-only follow-up review",
    }
    (intake / scope_path).write_text(
        json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
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
