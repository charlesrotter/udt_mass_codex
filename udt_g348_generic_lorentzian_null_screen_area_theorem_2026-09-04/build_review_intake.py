#!/usr/bin/env python3
"""Build an exact sealed G348 review intake under /tmp."""

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
    "GIT_PREREGISTRATION_PROOF.txt", "INDEPENDENT_VERIFICATION.json", "LAY_REPORT.md", "MAP.md",
    "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "PREREGISTRATION_EXECUTION_NOTE.md",
    "RUN_RECORD.md", "SOURCE_SCOPE.tsv", "STATUS_LEDGER.tsv", "VERIFICATION_RESULT.json",
    "derive_generic_null_screen_area.py", "run_catch_proofs.py",
    "verify_generic_null_screen_area_independent.py", "verify_package.py",
)

ROOT_FILES = (
    "LIVE.md", "CURRENT_RESEARCH_PROGRAM.md", "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_g343_bilocal_screen_phase_space_propagator_2026-09-04/EXACT_DERIVATION.md",
    "udt_g344_endpoint_generating_function_determinant_density_2026-09-04/EXACT_DERIVATION.md",
    "udt_g345_observer_calibrated_screen_scalar_2026-09-04/EXACT_DERIVATION.md",
    "udt_g346_directional_angular_area_reciprocity_2026-09-04/EXACT_DERIVATION.md",
    "udt_g347_arbitrary_endpoint_observer_angular_area_covariance_2026-09-04/EXACT_DERIVATION.md",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    intake = Path(tempfile.mkdtemp(prefix="udt_g348_review_", dir="/tmp"))
    paths = [PACKAGE / name for name in PACKAGE_FILES] + [Path(name) for name in ROOT_FILES]
    scope_path = Path("REVIEW_SCOPE.json")
    declared = sorted(path.as_posix() for path in paths) + [scope_path.as_posix()]
    scope = {
        "date": "2026-09-04",
        "files": declared,
        "maximum_conclusion": "bounded generic infinitesimal Lorentzian null-screen area theorem or scoped refutation",
        "payload_count": len(declared),
        "prohibitions": [
            "edit evidence", "continue research", "use internet", "access repository outside intake",
            "import optics or a field equation", "select history population distance scale X_max or canon",
        ],
        "review": "fresh read-only adversarial G348 review",
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
