#!/usr/bin/env python3
"""Freeze the exact committed source boundary before global production."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_intrinsic_defect_transport_atlas_2026-08-02"

PARENT_OUTPUTS = (
    "PACKAGE_MANIFEST.sha256",
    "PACKAGE_VERIFICATION.json",
    "AUDIT_REPORT.md",
    "EXACT_DERIVATION.md",
    "TOPOLOGY_ATLAS.tsv",
    "EDGE_ATLAS.tsv",
    "CONNECTION_POINTS.tsv",
    "CANDIDATE_TRANSPORT_ATLAS.tsv",
    "OBJECT_STATUS.tsv",
    "STATUS_LEDGER.tsv",
    "COLD_REVIEW_RETURN.md",
    "ADJUDICATION_RESULT.json",
    "TRANSPORT_RESULT.json",
    "derive_defect_transport.py",
    "verify_independent.py",
    "NEXT_STEP.md",
)
CURRENT_PREREG = (
    "PREREGISTRATION.md",
    "CANDIDATE_UNIVERSE.tsv",
    "LOOP_FAMILY_UNIVERSE.tsv",
    "ZERO_SET_CERTIFICATION_CONTRACT.tsv",
    "OBJECT_UNIVERSE.tsv",
    "PREMISE_LEDGER.tsv",
    "FALSIFICATION_CONTRACT.tsv",
    "COMPLETENESS_MAP.md",
    "PREREGISTRATION_METHOD_REFINEMENT.md",
    "PREREGISTRATION_NUMERIC_CERTIFICATION.md",
    "ZERO_SET_METHOD_REFINEMENT_2.md",
    "ZERO_SET_PROJECTIVE_COMPLETION_METHOD.md",
    "C08_EXACT_LINEAR_ELIMINATION_PREREGISTRATION.md",
    "C08_EXACT_MODULAR_GROEBNER_PREREGISTRATION.md",
)
CURRENT_EVIDENCE = (
    "C08_GENERIC_GROEBNER_RESOURCE_RETURN.json",
    "C08_ALL_ZERO_SLIMGB_RESOURCE_RETURN.json",
)
CURRENT_METHOD_INPUTS = (
    "run_c08_exact_linear_elimination.py",
    "C08_LINEAR_ELIMINATION_CONSTRUCTION.json",
    "C08_LINEAR_A_12.txt",
    "C08_LINEAR_B_12.txt",
    "C08_LINEAR_A_13.txt",
    "C08_LINEAR_B_13.txt",
    "C08_LINEAR_A_23.txt",
    "C08_LINEAR_B_23.txt",
)
CURRENT_RESOURCE_ARTIFACTS = (
    "C08_LINEAR_ALL_ZERO_INPUT.sing",
    "C08_LINEAR_ALL_ZERO_STDOUT.txt",
    "C08_LINEAR_ALL_ZERO_STDERR.txt",
    "C08_LINEAR_ALL_ZERO_PROCESS_RESULT.json",
)


def git_blob(path):
    relative = str(path.relative_to(ROOT))
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{relative}"], cwd=ROOT,
        text=True, capture_output=True, check=True,
    ).stdout.strip()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    sources = {}
    with (PARENT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            sources[row["path"]] = "inherited_parent_source_boundary"
    for name in PARENT_OUTPUTS:
        sources[str((PARENT / name).relative_to(ROOT))] = "immediate_parent_load_bearing_evidence"
    for name in CURRENT_PREREG:
        sources[str((HERE / name).relative_to(ROOT))] = "current_preregistration_boundary"
    for name in CURRENT_EVIDENCE:
        sources[str((HERE / name).relative_to(ROOT))] = "pre_refactor_resource_evidence"
    for name in CURRENT_METHOD_INPUTS:
        sources[str((HERE / name).relative_to(ROOT))] = "frozen_exact_modular_method_input"
    for name in CURRENT_RESOURCE_ARTIFACTS:
        sources[str((HERE / name).relative_to(ROOT))] = "pre_refactor_raw_resource_artifact"

    scope_rows = []
    manifest_rows = []
    for relative in sorted(sources):
        path = ROOT / relative
        blob = git_blob(path)
        content = subprocess.run(
            ["git", "cat-file", "blob", blob], cwd=ROOT,
            capture_output=True, check=True,
        ).stdout
        scope_rows.append({"path": relative, "role": sources[relative]})
        manifest_rows.append({
            "path": relative, "role": sources[relative], "git_blob": blob,
            "bytes": str(len(content)), "sha256": digest(content),
        })

    with (HERE / "SOURCE_SCOPE.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["path", "role"], lineterminator="\n")
        writer.writeheader(); writer.writerows(scope_rows)
    with (HERE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["path", "role", "git_blob", "bytes", "sha256"], lineterminator="\n")
        writer.writeheader(); writer.writerows(manifest_rows)
    manifest_hash = digest((HERE / "SOURCE_MANIFEST.tsv").read_bytes())
    (HERE / "SOURCE_MANIFEST.sha256").write_text(manifest_hash+"\n", encoding="utf-8")
    print(f"PASS frozen_sources={len(manifest_rows)} manifest_sha256={manifest_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
