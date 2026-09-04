#!/usr/bin/env python3
"""Build a sealed exact-file G340 adversarial-review intake under /tmp."""

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
    "derive_finite_pair_relations.py",
    "verify_finite_pair_independent.py",
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
    "udt_g323_g320_unmarked_taub_quotient_classification_2026-09-01/EXACT_DERIVATION.md",
    "udt_g338_explicit_taub_pair_finite_time_readout_2026-09-03/EXACT_DERIVATION.md",
    "udt_g339_finite_time_pair_carry_type_classification_2026-09-03/EXACT_DERIVATION.md",
    "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/EXACT_DERIVATION.md",
    "udt_g275_projective_position_scale_attachment_xmax_separation_2026-08-26/EXACT_DERIVATION.md",
    "udt_g276_proper_clock_ce_scale_anchor_reconciliation_2026-08-26/EXACT_DERIVATION.md",
    "udt_g297_complete_pair_causal_dilation_equivalence_2026-08-29/EXACT_DERIVATION.md",
    "udt_g298_causal_diamond_to_pair_germ_transfer_2026-08-29/EXACT_DERIVATION.md",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_g340_review_", dir="/tmp"))
    payload: list[Path] = []

    for name in PACKAGE_FILES:
        source = PACKAGE / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = destination / "g340" / name
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
        "task": "fresh read-only adversarial review of bounded G340 finite-separated pair relation classification",
        "intake_only": True,
        "may_run": "registered checks in a writable ephemeral copy",
        "must_not": [
            "edit evidence files",
            "continue the research",
            "access the repository or protected packages",
            "use internet or unsealed observations",
            "import a light field, transfer law, source, action, matter model, fit, or observation",
            "select or canonize a physical protocol, route or observer population, occupancy, scale, or X_max",
        ],
        "preregistration_commit": "d2b68663",
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
