#!/usr/bin/env python3
"""Freeze exact inputs for the intrinsic defect/transport atlas."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_intrinsic_two_form_distribution_audit_2026-08-02"
EXPECTED_SOURCE_COUNT = 86

ADDITIONS = (
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/SOURCE_MANIFEST.tsv", "parent_source_boundary"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/PACKAGE_MANIFEST.sha256", "parent_corrected_package_identity"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/PACKAGE_VERIFICATION.json", "parent_corrected_package_verification"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/CORRECTION_LAYER.md", "parent_kernel_wording_correction"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/AUDIT_REPORT.md", "parent_report"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/EXACT_DERIVATION.md", "parent_exact_derivation"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/CANDIDATE_ATLAS.tsv", "parent_candidate_atlas"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/LOCUS_ATLAS.tsv", "parent_locus_atlas"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/DISTRIBUTION_RESULT.json", "parent_machine_result"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/STATUS_LEDGER.tsv", "parent_status_ledger"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/COLD_REVIEW_RETURN.md", "parent_fresh_review"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/COLD_REVIEW_RESULT.json", "parent_fresh_review_result"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/derive_distribution_atlas.py", "parent_production_code"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/ADJUDICATION_RESULT.json", "parent_adjudication"),
    ("udt_intrinsic_two_form_distribution_audit_2026-08-02/NEXT_STEP.md", "parent_authorized_next_boundary"),
    ("udt_intrinsic_defect_transport_atlas_2026-08-02/PREREGISTRATION.md", "current_preregistration"),
    ("udt_intrinsic_defect_transport_atlas_2026-08-02/CANDIDATE_BINDING.tsv", "current_candidate_binding"),
    ("udt_intrinsic_defect_transport_atlas_2026-08-02/LOOP_UNIVERSE.tsv", "current_loop_universe"),
    ("udt_intrinsic_defect_transport_atlas_2026-08-02/OBJECT_UNIVERSE.tsv", "current_object_universe"),
    ("udt_intrinsic_defect_transport_atlas_2026-08-02/PREMISE_LEDGER.tsv", "current_premise_ledger"),
    ("udt_intrinsic_defect_transport_atlas_2026-08-02/FALSIFICATION_CONTRACT.tsv", "current_falsification_contract"),
    ("udt_intrinsic_defect_transport_atlas_2026-08-02/COMPLETENESS_MAP.md", "current_completeness_map"),
)


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


with (PARENT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
    inherited = list(csv.DictReader(handle, delimiter="\t"))
assert len(inherited) == 64

scope = [
    {"path": row["path"], "role": f"inherited_parent_source:{row['role']}"}
    for row in inherited
]
scope.extend({"path": path, "role": role} for path, role in ADDITIONS)
assert len(scope) == len({row["path"] for row in scope}) == EXPECTED_SOURCE_COUNT

with (HERE / "SOURCE_SCOPE.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["path", "role"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(scope)

rows = []
for item in scope:
    path = ROOT / item["path"]
    assert path.is_file(), item["path"]
    blob = subprocess.run(
        ["git", "rev-parse", f"HEAD:{item['path']}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    content = subprocess.run(
        ["git", "cat-file", "blob", blob],
        cwd=ROOT,
        capture_output=True,
        check=True,
    ).stdout
    assert content == path.read_bytes(), item["path"]
    rows.append({
        "path": item["path"],
        "role": item["role"],
        "git_blob": blob,
        "bytes": str(len(content)),
        "sha256": digest(content),
    })

with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(
        handle,
        delimiter="\t",
        fieldnames=["path", "role", "git_blob", "bytes", "sha256"],
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)

manifest_hash = digest((HERE / "SOURCE_MANIFEST.tsv").read_bytes())
(HERE / "SOURCE_MANIFEST.sha256").write_text(manifest_hash + "\n", encoding="utf-8")
print(f"PASS frozen_sources={len(rows)} manifest_sha256={manifest_hash}")
