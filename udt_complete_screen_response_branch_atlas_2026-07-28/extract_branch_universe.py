#!/usr/bin/env python3
"""Freeze the registered completion/representative universe at the preregistered base.

This is a provenance router, not a semantic classifier.  It copies exact registered rows from
the fixed tree, identifies the direct load-bearing sources, and gives every row in the broad
discovery census exactly one source role.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
BASE = "bd8649ae31aab31435fbe986427d7f4e84d58e6d"

DIRECT = {
    "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv": "completion_class_registry",
    "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/CONCRETE_REPRESENTATIVE_ATLAS.tsv": "complete_control_registry",
    "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/EXACT_DERIVATION.md": "complete_control_geometry",
    "udt_directional_observer_pair_distance_audit_2026-07-24/CORRECTED_CONFIGURATION_REGISTRY.tsv": "configuration_identity_registry",
    "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/WITNESS_UNIVERSE.tsv": "nonultrastatic_witness_registry",
    "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/WITNESS_OUTCOMES.tsv": "nonultrastatic_witness_outcomes",
    "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/EXACT_DERIVATION.md": "nonultrastatic_geometry",
    "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/EXACT_DERIVATION.md": "intrinsic_pair_geometry",
    "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/CANDIDATE_UNIVERSE.tsv": "screen_parameter_registry",
    "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/CONNECTION_MIXING_ATLAS.tsv": "screen_response_results",
    "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/EXACT_DERIVATION.md": "screen_response_geometry",
    "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/HOMOGENEOUS_HOLONOMY_ATLAS.tsv": "homogeneous_holonomy",
    "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/CONCRETE_CONTROL_ASSEMBLY.tsv": "homogeneous_global_assembly",
    "udt_reciprocal_transport_holonomy_atlas_2026-07-26/AUDIT_REPORT.md": "transport_holonomy_scope",
    "udt_intrinsic_pair_deformation_neighborhood_audit_2026-07-27/AUDIT_REPORT.md": "deformation_neighborhood_scope",
    "udt_angular_bulk_jacobi_selector_audit_2026-07-23/AUDIT_REPORT.md": "screen_jacobi_scope",
}

FAMILY_PREFIXES = (
    "udt_finite_cell_completion_atlas_2026-07-21/",
    "udt_global_metric_assembly_atlas_2026-07-22/",
    "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/",
    "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/",
    "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/",
    "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/",
    "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/",
    "udt_intrinsic_pair_lambda_component_atlas_2026-07-27/",
    "udt_intrinsic_pair_deformation_neighborhood_audit_2026-07-27/",
    "udt_reciprocal_transport_holonomy_atlas_2026-07-26/",
    "udt_angular_bulk_jacobi_selector_audit_2026-07-23/",
    "udt_historical_angular_method_salvage_audit_2026-07-28/",
)


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def show(path: str) -> bytes:
    return git("show", f"{BASE}:{path}")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_tsv_at_base(path: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(show(path).decode()), delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def blob(path: str) -> str:
    return git("rev-parse", f"{BASE}:{path}").decode().strip()


def source_roles() -> dict[str, int]:
    discovered_path = OUT / "DISCOVERED_SOURCE_CENSUS.tsv"
    rows = list(csv.DictReader(discovered_path.open(encoding="utf-8"), delimiter="\t"))
    out_rows: list[dict[str, str]] = []
    counts: dict[str, int] = {}
    for row in rows:
        path = row["path"]
        if path in DIRECT:
            role = "LOAD_BEARING_DIRECT"
            rationale = DIRECT[path]
        elif path.startswith(FAMILY_PREFIXES):
            role = "BRANCH_OR_SCREEN_FAMILY_SUPPORT"
            rationale = "inside a registered completion, branch, holonomy, or screen-response package"
        elif "TRANSITIVE" in row["discovery_reason"]:
            role = "TRANSITIVE_FORENSIC_SUPPORT"
            rationale = "reached by the frozen transitive-reference rule; not a direct branch row here"
        else:
            role = "BROAD_SEED_NO_DIRECT_BRANCH_ROLE"
            rationale = "retained by the broad frozen seed rule; no direct atlas ownership assigned"
        counts[role] = counts.get(role, 0) + 1
        out_rows.append({**row, "source_role": role, "role_rationale": rationale})
    write_tsv(
        OUT / "SOURCE_ROLE_CENSUS.tsv",
        list(rows[0]) + ["source_role", "role_rationale"],
        out_rows,
    )
    return counts


def main() -> None:
    if git("rev-parse", f"{BASE}^{{tree}}").decode().strip() != "b0ec58d2f956eb942592c965858876f7d932149a":
        raise SystemExit("fixed base tree mismatch")

    direct_rows = []
    discovered = {
        r["path"]
        for r in csv.DictReader((OUT / "DISCOVERED_SOURCE_CENSUS.tsv").open(encoding="utf-8"), delimiter="\t")
    }
    for path, role in sorted(DIRECT.items()):
        data = show(path)
        if path not in discovered:
            raise SystemExit(f"direct source omitted by discovery: {path}")
        direct_rows.append(
            {
                "path": path,
                "git_blob": blob(path),
                "sha256": sha(data),
                "bytes": str(len(data)),
                "direct_role": role,
            }
        )
    write_tsv(
        OUT / "LOAD_BEARING_SOURCE_MANIFEST.tsv",
        ["path", "git_blob", "sha256", "bytes", "direct_role"],
        direct_rows,
    )

    completion_path = "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv"
    completion_rows = read_tsv_at_base(completion_path)
    for row in completion_rows:
        row["record_scope"] = "REGISTERED_COMPLETION_TAXONOMY_NOT_AN_ACTUAL_METRIC"
        row["source_path"] = completion_path
    write_tsv(
        OUT / "COMPLETION_CLASS_UNIVERSE.tsv",
        list(completion_rows[0]),
        completion_rows,
    )

    rep_path = "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/CONCRETE_REPRESENTATIVE_ATLAS.tsv"
    rep_rows = read_tsv_at_base(rep_path)
    rep_out = []
    for row in rep_rows:
        rid = row["representative_id"]
        if rid.startswith("Q01"):
            kind = "ACTUAL_COMPLETE_CONDITIONAL_ON_SHELL_CONTROL"
        elif rid.startswith("Q02"):
            kind = "ACTUAL_COMPLETE_OFF_SHELL_CONTROL"
        elif rid.startswith("Q03"):
            kind = "INCOMPLETE_LOCAL_PROFILE"
        else:
            kind = "ABSENT_JOIN"
        rep_out.append({**row, "representative_kind": kind, "source_path": rep_path})
    write_tsv(
        OUT / "CONCRETE_REPRESENTATIVE_UNIVERSE.tsv",
        list(rep_out[0]),
        rep_out,
    )

    witness_path = "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/WITNESS_UNIVERSE.tsv"
    outcome_path = "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/WITNESS_OUTCOMES.tsv"
    witnesses = read_tsv_at_base(witness_path)
    outcomes = read_tsv_at_base(outcome_path)
    outcome_by_id = {r["witness_id"]: r for r in outcomes}
    witness_out = []
    for row in witnesses:
        extra = outcome_by_id[row["witness_id"]]
        witness_out.append({**row, **{f"outcome_{k}": v for k, v in extra.items() if k != "witness_id"}, "source_path": witness_path})
    write_tsv(OUT / "NONULTRASTATIC_WITNESS_UNIVERSE.tsv", list(witness_out[0]), witness_out)

    candidate_path = "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/CANDIDATE_UNIVERSE.tsv"
    candidate_rows = read_tsv_at_base(candidate_path)
    for row in candidate_rows:
        row["parent_witness"] = "W01_TWISTED_RECIPROCAL_S3"
        row["source_path"] = candidate_path
    write_tsv(OUT / "TWISTED_PARAMETER_STRATA.tsv", list(candidate_rows[0]), candidate_rows)

    relationships = [
        {"alias_or_child": "B19_ROUND_S3", "canonical_record": "Q01_ROUND_S3_B19", "relation": "SAME_REGISTERED_ROUND_CONTROL", "merge_policy": "ALIASED_BUT_SOURCE_ROWS_RETAINED"},
        {"alias_or_child": "Q01_ROUND_S3", "canonical_record": "Q01_ROUND_S3_B19", "relation": "SHORT_CONFIGURATION_ID", "merge_policy": "ALIASED_BUT_SOURCE_ROWS_RETAINED"},
        {"alias_or_child": "Q02_SQUASHED_S3", "canonical_record": "Q02_SQUASHED_S3_OFF_SHELL", "relation": "SHORT_CONFIGURATION_ID", "merge_policy": "ALIASED_BUT_SOURCE_ROWS_RETAINED"},
        {"alias_or_child": "C01-C06", "canonical_record": "W01_TWISTED_RECIPROCAL_S3", "relation": "PARAMETER_SAMPLES_IN_COMPLETE_TWISTED_FAMILY", "merge_policy": "CHILD_STRATA_RETAINED"},
        {"alias_or_child": "C07", "canonical_record": "W06_TWIST_FREE_NONCONSTANT_CLOCK", "relation": "TWIST_OFF_PARAMETER_CONTROL", "merge_policy": "RELATED_NOT_IDENTIFIED"},
        {"alias_or_child": "C08", "canonical_record": "W03_ULTRASTATIC_S3", "relation": "DEPTH_OFF_PARAMETER_CONTROL_WITH_TWIST_PARAMETER_RETAINED", "merge_policy": "RELATED_NOT_IDENTIFIED"},
        {"alias_or_child": "W01", "canonical_record": "FC04_TWO_CAP_P1", "relation": "COMPLETE_S3_REALIZATION", "merge_policy": "INSTANCE_NOT_CLASS"},
        {"alias_or_child": "W02-W06", "canonical_record": "FC04_TWO_CAP_P1", "relation": "S3_CONTROLS_OR_BOUNDARY_STRATA", "merge_policy": "INSTANCE_OR_STRATUM_NOT_CLASS"},
        {"alias_or_child": "Q03_WRL_LOCAL", "canonical_record": "NONE", "relation": "INCOMPLETE_LOCAL_PROFILE", "merge_policy": "DO_NOT_SPLICE_WITH_COMPLETE_BRANCH"},
        {"alias_or_child": "Q04_PHYSICAL_XMAX_JOIN", "canonical_record": "NONE", "relation": "ABSENT_CONFIGURATION", "merge_policy": "DO_NOT_INVENT"},
    ]
    write_tsv(OUT / "BRANCH_IDENTITY_ALIAS_LEDGER.tsv", list(relationships[0]), relationships)

    counts = source_roles()
    result = {
        "base_commit": BASE,
        "base_tree": git("rev-parse", f"{BASE}^{{tree}}").decode().strip(),
        "discovered_source_rows": len(discovered),
        "direct_source_rows": len(direct_rows),
        "completion_classes": len(completion_rows),
        "configuration_rows": len(rep_out),
        "nonultrastatic_witness_rows": len(witness_out),
        "twisted_parameter_rows": len(candidate_rows),
        "source_role_counts": counts,
    }
    (OUT / "SOURCE_EXTRACTION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
