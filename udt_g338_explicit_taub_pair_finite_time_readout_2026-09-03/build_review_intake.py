#!/usr/bin/env python3
"""Build a sealed, exact-file G338 adversarial-review intake under /tmp."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent

PACKAGE_FILES = (
    "MAP.md",
    "EXPLORATORY_MAP_NOTE.md",
    "PREREGISTRATION.md",
    "PREREGISTRATION_EXECUTION_NOTE.md",
    "PREMISE_LEDGER.tsv",
    "COMPLETENESS_MAP.md",
    "EXACT_DERIVATION.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "AUDIT_REPORT.md",
    "RUN_RECORD.md",
    "COMMANDS.md",
    "SOURCE_SCOPE.tsv",
    "derive_explicit_taub_pair_readout.py",
    "verify_explicit_taub_pair_readout_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "VERIFICATION_RESULT.json",
    "ADVERSARIAL_REVIEW_REQUEST.md",
)

SOURCE_FILES = (
    "LIVE.md",
    "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/EXACT_DERIVATION.md",
    "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/derive_completed_pair_reciprocity.py",
    "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/DERIVATION_RESULT.json",
    "udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01/EXACT_DERIVATION.md",
    "udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01/derive_unmarked_quotients.py",
    "udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01/DERIVATION_RESULT.json",
    "udt_g324_g323_taub_quotient_mghd_identification_2026-09-02/EXACT_DERIVATION.md",
    "udt_g324_g323_taub_quotient_mghd_identification_2026-09-02/derive_taub_mghd.py",
    "udt_g324_g323_taub_quotient_mghd_identification_2026-09-02/DERIVATION_RESULT.json",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g338_review_", dir="/tmp"))
    payload: list[Path] = []

    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = destination / "g338" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payload.append(target)

    for relative in SOURCE_FILES:
        source = ROOT / relative
        if not source.is_file():
            raise FileNotFoundError(source)
        target = destination / "sources" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payload.append(target)

    scope = {
        "task": "fresh read-only adversarial review of bounded G338 finite-time pair readout",
        "intake_only": True,
        "may_run": "registered checks in a writable ephemeral copy",
        "must_not": [
            "edit evidence files",
            "continue the research",
            "access the repository or protected packages",
            "use internet or unsealed observations",
            "select or canonize a physical history, carry, population, scale, topology, or X_max",
        ],
        "preregistration_commit": "01e2110a",
        "payload_count_excluding_manifest_and_detached_seal": len(payload) + 1,
    }
    scope_path = destination / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payload.append(scope_path)

    manifest_path = destination / "REVIEW_MANIFEST.tsv"
    lines = ["sha256\tbytes\tpath"]
    for path in sorted(payload, key=lambda item: item.relative_to(destination).as_posix()):
        relative = path.relative_to(destination).as_posix()
        lines.append(f"{sha256(path)}\t{path.stat().st_size}\t{relative}")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    seal_path = destination / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{sha256(manifest_path)}  REVIEW_MANIFEST.tsv\n", encoding="utf-8")

    result = {
        "intake": str(destination),
        "total_files": len(payload) + 2,
        "manifest_payloads": len(payload),
        "review_scope_sha256": sha256(scope_path),
        "review_manifest_sha256": sha256(manifest_path),
        "detached_seal_sha256": sha256(seal_path),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
