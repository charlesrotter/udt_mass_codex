#!/usr/bin/env python3
"""Dependency-free G239 premise-scope audit for a sealed intake."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INTAKE_ROOT = ROOT.parent
REGISTRY = INTAKE_ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv"

EXPECTED_COLUMNS = (
    "premise_id",
    "term",
    "current_status",
    "epistemic_label",
    "active_use",
    "open_scope",
    "forbidden_regression",
    "controlling_source",
    "precedence_rule",
)

EXPECTED_DEPENDENCIES = {
    "G126": {
        "source": "udt_g126_angular_lane_same_query_bridge_2026-08-16/AUDIT_REPORT.md",
        "tokens": (
            "NO_CURRENT_R5_TO_K_OR_PHASE_BRIDGE",
            "IDEAL_REFERENCE_REMOVES_PURE_RADIAL_MODULATION",
        ),
    },
    "G127": {
        "source": "udt_g127_same_history_radial_displaced_screen_emergence_2026-08-16/AUDIT_REPORT.md",
        "tokens": (
            "LOCAL_SAME_HISTORY_RADIAL_TILTED_SCREEN_EMERGENCE_DERIVED",
            "PHYSICAL_HISTORY_GLOBAL_QUERY_AND_OBSERVATIONS_OPEN",
        ),
    },
    "G188": {
        "source": "udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/AUDIT_REPORT.md",
        "tokens": (
            "COMPLETE_COFRAME_AND_REGULAR_AFFINE_NULL_QUERY",
            "UNIQUE_FINITE_VERTEX_NORMALIZED_MATRIX_JACOBI_MAP",
        ),
    },
    "G221": {
        "source": "udt_g221_complete_coframe_null_clock_chord_2026-08-22/AUDIT_REPORT.md",
        "tokens": (
            "SUPPLIED_SMOOTH_COMPLETE_COFRAME",
            "Q_SX_AND_ST_ENTER_UPSTREAM_BEFORE_SCALAR_READOUT",
            "NO_PHYSICAL_PROTOCOL_BRANCH_POPULATION",
        ),
    },
    "G226": {
        "source": "udt_g226_null_chain_conformal_symplectic_assembly_2026-08-22/AUDIT_REPORT.md",
        "tokens": (
            "ONE_SUPPLIED_COMPOSABLE_NONANTIPODAL_NULL_CHAIN",
            "NO_G225_TRANSPORT_PROMOTION",
            "OBSERVER_OR_BRANCH_POPULATION_PHYSICAL_HISTORY",
        ),
    },
    "G238": {
        "source": "udt_g238_bao_heldout_query_typing_2026-08-23/AUDIT_REPORT.md",
        "tokens": (
            "QUERY_TYPING_INCOMPLETE__NO_OUTCOME_OPENING",
            "G237_K12_STATE_DOES_NOT_DETERMINE_CONTINUOUS_METRIC_OR_SCREEN_HISTORY",
            "TWO_SOURCE_POPULATION_AND_REFERENCE_FORWARD_MAP_OPEN",
        ),
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compute() -> dict[str, object]:
    if not REGISTRY.is_file():
        raise AssertionError(f"sealed registry absent: {REGISTRY}")
    with REGISTRY.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != EXPECTED_COLUMNS:
            raise AssertionError("premise registry columns changed")
        rows = list(reader)
    if len(rows) != 221:
        raise AssertionError(f"expected 221 premise rows, found {len(rows)}")
    ids = [row["premise_id"] for row in rows]
    if len(set(ids)) != len(ids):
        raise AssertionError("duplicate premise_id in sealed registry")
    by_id = {row["premise_id"]: row for row in rows}

    checked: dict[str, object] = {}
    for premise_id, expected in EXPECTED_DEPENDENCIES.items():
        row = by_id.get(premise_id)
        if row is None:
            raise AssertionError(f"missing premise dependency: {premise_id}")
        if row["controlling_source"] != expected["source"]:
            raise AssertionError(f"controlling source changed: {premise_id}")
        absent = [token for token in expected["tokens"] if token not in row["current_status"]]
        if absent:
            raise AssertionError(f"status tokens absent for {premise_id}: {absent}")
        checked[premise_id] = {
            "controlling_source": row["controlling_source"],
            "status_tokens_checked": list(expected["tokens"]),
        }

    # G239 is still under repair review.  It must not enter the exact premise registry before
    # external repair acceptance.
    if "G239" in by_id:
        raise AssertionError("G239 prematurely entered the current premise registry")

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        manifest = list(csv.DictReader(handle, delimiter="\t"))
    registry_rows = [row for row in manifest if row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv"]
    if len(registry_rows) != 1:
        raise AssertionError("sealed source manifest does not identify one premise registry")
    registered_hash = registry_rows[0]["sha256"]
    actual_hash = sha256(REGISTRY)
    if registered_hash != actual_hash:
        raise AssertionError("sealed premise registry hash differs from source manifest")

    return {
        "audit": "G239_SEALED_PREMISE_SCOPE",
        "status": "PASS",
        "registry_rows": len(rows),
        "registry_sha256": actual_hash,
        "dependencies_checked": checked,
        "g239_registry_row_absent_until_external_repair_acceptance": True,
        "scope": "BOUNDED_SEALED_DEPENDENCY_AUDIT__NOT_REPOSITORY_WIDE_VERIFIER",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = compute()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not args.no_write:
        (ROOT / "SEALED_PREMISE_SCOPE_RESULT.json").write_text(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
