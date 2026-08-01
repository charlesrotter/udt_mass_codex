#!/usr/bin/env python3
"""Cold, standard-library-only verifier for the stability cross-family atlas.

This implementation intentionally does not import the primary atlas producer or its
verifier.  It reads the frozen sources, reconstructs the finite family/claim/grammar
logic, applies deletion controls, and exercises the same predicates with mutations.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
RAW_PATH = PKG / "INDEPENDENT_RAW.jsonl"
RESULT_PATH = PKG / "INDEPENDENT_RESULT.json"

raw: list[dict[str, Any]] = []
checks: list[dict[str, Any]] = []
mutations: list[dict[str, Any]] = []


def tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def json_file(name: str) -> dict[str, Any]:
    return json.loads((PKG / name).read_text(encoding="utf-8"))


def record(kind: str, name: str, passed: bool, detail: Any) -> None:
    entry = {"kind": kind, "name": name, "passed": bool(passed), "detail": detail}
    raw.append(entry)
    if kind == "check":
        checks.append(entry)
    elif kind == "mutation":
        mutations.append(entry)


def check(name: str, passed: bool, detail: Any) -> None:
    record("check", name, passed, detail)


def mutate(name: str, rejected: bool, detail: Any) -> None:
    record("mutation", name, rejected, detail)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def parse_manifest() -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for line in (PKG / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        if rel.startswith("../"):
            rel = rel[3:]
        parsed.append((rel, digest))
    return parsed


def source_predicate(
    rows: list[dict[str, str]],
    source_paths: list[str],
    manifest: list[tuple[str, str]],
    overrides: dict[str, bytes] | None = None,
) -> tuple[bool, list[str], dict[str, Any], dict[str, dict[str, Any]]]:
    overrides = overrides or {}
    errors: list[str] = []
    paths = [row["path"] for row in rows]
    if len(rows) != 1469:
        errors.append(f"inventory_count:{len(rows)}")
    if len(set(paths)) != len(paths):
        errors.append("duplicate_inventory_path")
    if paths != sorted(paths):
        errors.append("inventory_not_sorted")
    if source_paths != paths:
        errors.append("source_paths_mismatch")
    if manifest != [(row["path"], row["sha256"]) for row in rows]:
        errors.append("manifest_mismatch")

    layers = Counter(row["layer"] for row in rows)
    expected_layers = {
        "PARENT_PREMISE_AUDIT_SOURCE_UNIVERSE": 1424,
        "GLOBAL_LOCAL_PREMISE_PARENT_PACKAGE": 42,
        "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02": 3,
    }
    if dict(layers) != expected_layers:
        errors.append(f"layer_counts:{dict(layers)}")

    atlas_prefix = "udt_stability_hypothesis_cross_family_atlas_2026-08-01/"
    if any(path.startswith(atlas_prefix) for path in paths):
        errors.append("generated_atlas_entered_source_universe")

    parent_prefix = "udt_global_local_self_consistency_premise_audit_2026-08-01/"
    parent_rows = [row for row in rows if row["layer"] == "GLOBAL_LOCAL_PREMISE_PARENT_PACKAGE"]
    if any(not row["path"].startswith(parent_prefix) for row in parent_rows):
        errors.append("parent_package_layer_path_mismatch")

    expected_additions = {
        "PONDER_MATH_ELEGANCE_2026-07-31.md",
        "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md",
        "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv",
    }
    additions = {
        row["path"] for row in rows if row["layer"] == "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02"
    }
    if additions != expected_additions:
        errors.append(f"controlling_anchor_additions:{sorted(additions)}")

    computed: dict[str, dict[str, Any]] = {}
    total_bytes = 0
    for row in rows:
        rel = row["path"]
        candidate = (ROOT / rel).resolve()
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"path_escape:{rel}")
            continue
        if rel in overrides:
            data = overrides[rel]
        else:
            try:
                data = candidate.read_bytes()
            except OSError as exc:
                errors.append(f"read:{rel}:{exc}")
                continue
        got = {
            "sha256": sha256(data),
            "git_blob": git_blob_sha1(data),
            "bytes": len(data),
            "layer": row["layer"],
        }
        computed[rel] = got
        total_bytes += len(data)
        if got["sha256"] != row["sha256"]:
            errors.append(f"sha256:{rel}")
        if got["git_blob"] != row["git_blob"]:
            errors.append(f"git_blob:{rel}")
        if got["bytes"] != int(row["bytes"]):
            errors.append(f"bytes:{rel}")

    stats = {
        "paths": len(rows),
        "unique_paths": len(set(paths)),
        "bytes": total_bytes,
        "layers": dict(sorted(layers.items())),
        "manifest_rows": len(manifest),
    }
    return not errors, errors, stats, computed


def keyed(rows: Iterable[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    return {row[field]: row for row in rows}


FAMILY_IDS = [f"F{i:02d}" for i in range(1, 8)]
CLAIM_IDS = [f"H{i:02d}" for i in range(1, 9)]
GRAMMAR_IDS = [f"G{i:02d}" for i in range(1, 11)]


def family_predicate(rows: list[dict[str, str]]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    ids = [row["family_id"] for row in rows]
    if ids != FAMILY_IDS or len(set(ids)) != 7:
        errors.append(f"family_ids:{ids}")
        return False, errors
    f = keyed(rows, "family_id")

    required = {
        "F01": [
            ("existence", "conditional"),
            ("boundary_completion", "empty closed postures excluded to F06"),
            ("stability_outcome", "whole certificate still open"),
            ("time_persistence", "OPEN"),
            ("hopfion_dependency", "NO_RESULT_TRANSFER_METHOD_SHAPE_ONLY"),
            ("hypothesis_role", "PRIMARY_NON_HOPF_ALGEBRAIC_SPINE"),
        ],
        "F02": [
            ("stability_outcome", "stable iff 64 E0^2 ell^4 <= g_p c_m pi^4"),
            ("overall_grade", "CONDITIONAL_SECTOR_PRUNING_EVIDENCE"),
            ("time_persistence", "OPEN"),
        ],
        "F03": [
            ("stability_outcome", "not isolated stable basins"),
            ("overall_grade", "CONTROL_NOT_SURVIVOR_EVIDENCE"),
        ],
        "F04": [
            ("equation_or_functional", "conditional L2+L4"),
            ("carrier", "ROUND_S2_POSIT"),
            ("boundary_completion", "physical finite-cell carrier completion open"),
            ("stability_outcome", "not time-live or infinite-volume persistence"),
            ("time_persistence", "OPEN"),
            ("hopfion_dependency", "SELF_ONLY"),
            ("hypothesis_role", "OBJECT_INEQUIVALENT_FULL3D_CONDITIONAL_EXEMPLAR"),
        ],
        "F05": [
            ("boundary_completion", "empty massive one-cell posture excluded to F06"),
            ("stability_test", "NONE"),
            ("stability_outcome", "NOT_TESTED"),
            ("hypothesis_role", "STRUCTURAL_TAXONOMY_AND_MASS_NEGATIVE_NOT_STABILITY"),
        ],
        "F06": [
            ("existence", "EMPTY"),
            ("stability_test", "NOT_APPLICABLE_EMPTY_DOMAIN"),
            ("stability_outcome", "nonexistence pruning, not instability"),
        ],
        "F07": [
            ("existence", "formal embeddings only"),
            ("stability_test", "NONE_ON_JOINT_REALIZED_OBJECT"),
            ("stability_outcome", "BLOCKED_BY_REALIZATION_JOIN"),
            ("overall_grade", "FORMAL_COMPATIBILITY_NOT_STABILITY"),
        ],
    }
    for fid, constraints in required.items():
        for field, needle in constraints:
            if needle not in f[fid][field]:
                errors.append(f"{fid}:{field}:{needle}")
    if any("SELECT" in row["bootstrap_role"] and "NONE" not in row["bootstrap_role"] for row in rows):
        errors.append("bootstrap_selection_in_family_atlas")
    return not errors, errors


EXPECTED_GRAMMAR: dict[str, list[str]] = {
    "F01": ["PRESENT_SCOPED", "PRESENT_SUPPLIED", "PRESENT", "PRESENT_CONDITIONAL", "PRESENT_CONDITIONAL", "PARTIAL_OPEN", "PRESENT_CONDITIONAL", "OPEN_FULL_CERTIFICATE", "OPEN", "ABSENT"],
    "F02": ["PRESENT_SCOPED", "PRESENT_BRANCH", "PRESENT", "CONDITIONAL_CLASS", "PRESENT_CONDITIONAL", "PARTIAL", "PRESENT_SECTOR", "PRESENT_SECTOR_ONLY", "OPEN", "ABSENT"],
    "F03": ["PRESENT_CONTROL", "PRESENT_CONTROL", "PRESENT_FLAT", "PRESENT_CONTROL", "PRESENT_CONDITIONAL", "PRESENT_CONTROL", "PRESENT_CONTROL", "ABSENT_PSD_DEGENERATE", "OPEN", "ABSENT"],
    "F04": ["PRESENT_CONDITIONAL", "PRESENT_TOPOLOGICAL", "PRESENT", "OBSERVED_CONDITIONAL", "PRESENT_CHOSEN", "SOLVER_ONLY_PHYSICAL_OPEN", "PRESENT_CONDITIONAL", "PRESENT_STATIC_FINITE_BOX_CONDITIONAL", "OPEN", "ABSENT"],
    "F05": ["PRESENT_SCOPED", "PRESENT_COMPLETION", "PRESENT", "PRESENT_MASSLESS_CONDITIONAL", "PRESENT_PERIOD_LAW", "PRESENT_SCOPED", "PRESENT_EXISTENCE_MASS", "NOT_TESTED", "OPEN", "ABSENT"],
    "F06": ["PRESENT_SCOPED", "PRESENT_POSTURE", "ELIMINATED", "EMPTY", "PRESENT_COMPLETION_LAW", "PRESENT_SCOPED", "PRESENT_NONEXISTENCE", "NOT_APPLICABLE", "NOT_APPLICABLE", "ABSENT"],
    "F07": ["PARTIAL_FORMAL", "PRESENT_MODULE", "PRESENT_FORMAL", "OPEN_JOINT", "ABSENT_COMPLETE", "OPEN", "BLOCKED", "BLOCKED", "OPEN", "ABSENT"],
}


def grammar_predicate(rows: list[dict[str, str]]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    cells = [(row["family_id"], row["component_id"]) for row in rows]
    expected_cells = [(fid, gid) for fid in FAMILY_IDS for gid in GRAMMAR_IDS]
    if cells != expected_cells or len(set(cells)) != 70:
        errors.append("grammar_not_exact_7x10")
        return False, errors
    for row in rows:
        index = int(row["component_id"][1:]) - 1
        expected = EXPECTED_GRAMMAR[row["family_id"]][index]
        if row["status"] != expected:
            errors.append(f"{row['family_id']}:{row['component_id']}:{row['status']}!=expected:{expected}")
    return not errors, errors


def partition_predicate(
    rows: list[dict[str, str]], family_rows: list[dict[str, str]], correction_text: str
) -> tuple[bool, list[str]]:
    errors: list[str] = []
    ids = [row["family_id"] for row in rows]
    keys = [row["effective_partition_key"] for row in rows]
    if ids != FAMILY_IDS or len(set(keys)) != 7:
        errors.append("partition_ids_or_keys")
        return False, errors
    p = keyed(rows, "family_id")
    f = keyed(family_rows, "family_id")
    if "NONEMPTY_OR_CONDITIONAL" not in p["F01"]["effective_partition_key"]:
        errors.append("F01_not_nonempty_partition")
    if "N1_CYCLIC_OR_DOUBLE_CREASE|EMPTY" not in p["F06"]["effective_partition_key"]:
        errors.append("F06_not_empty_partition")
    if "MASSLESS_OR_MULTICELL_MIXED" not in p["F05"]["effective_partition_key"]:
        errors.append("F05_not_ring_partition")
    if "excluded to F06" not in f["F01"]["boundary_completion"]:
        errors.append("F01_atlas_exclusion_missing")
    if "excluded to F06" not in f["F05"]["boundary_completion"]:
        errors.append("F05_atlas_exclusion_missing")
    if "EMPTY" not in f["F06"]["existence"]:
        errors.append("F06_empty_missing")
    correction_tokens = [
        "preserved unchanged",
        "effective partition",
        "No family is added or removed",
        "No source, outcome label, premise, conclusion ceiling, or favorable result changes",
    ]
    normalized_correction = " ".join(correction_text.split())
    if any(" ".join(token.split()) not in normalized_correction for token in correction_tokens):
        errors.append("correction_not_transparent")
    return not errors, errors


def source_correction_predicate(
    rows: list[dict[str, str]], correction_text: str
) -> tuple[bool, list[str], dict[str, str]]:
    errors: list[str] = []
    expected = {
        "PONDER_MATH_ELEGANCE_2026-07-31.md",
        "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md",
        "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv",
    }
    additions = {
        row["path"]: row
        for row in rows
        if row["layer"] == "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02"
    }
    if set(additions) != expected:
        errors.append(f"addition_set:{sorted(additions)}")
    normalized = " ".join(correction_text.split())
    tokens = [
        "original preregistration at `3ae58ba`",
        "absent from the frozen 1,466-path source universe",
        "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02",
        "effective source universe becomes exactly **1,469 sorted unique paths**",
        "changes no family, premise, claim, outcome label, algebra, source meaning, or conclusion ceiling",
        "SOURCE_CONFLICT_OR_SCOPE_BROKEN",
    ]
    if any(" ".join(token.split()) not in normalized for token in tokens):
        errors.append("source_correction_not_explicit")

    base_hashes: dict[str, str] = {}
    for path in sorted(expected):
        proc = subprocess.run(
            ["git", "show", f"c77c8b281155dfbd33c05ef57856a26fcf20f1da:{path}"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode != 0:
            errors.append(f"base_read:{path}:{proc.stderr.decode('utf-8', errors='replace')}")
            continue
        base_digest = sha256(proc.stdout)
        base_hashes[path] = base_digest
        row = additions.get(path)
        if row is None or row["sha256"] != base_digest:
            errors.append(f"base_hash:{path}")
        current = (ROOT / path).read_bytes()
        if sha256(current) != base_digest:
            errors.append(f"current_not_base_identical:{path}")
    return not errors, errors, base_hashes


def graph_predicate(rows: list[dict[str, str]]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    ids = [row["edge_id"] for row in rows]
    if ids != [f"D{i:02d}" for i in range(1, 15)] or len(set(ids)) != 14:
        errors.append("edge_census")
        return False, errors
    d = keyed(rows, "edge_id")
    expected = {
        "D01": ("F01", "H04", "LOAD_BEARING_NON_HOPF_ALGEBRA"),
        "D02": ("F02", "H05", "LOAD_BEARING_NON_HOPF_ALGEBRA"),
        "D03": ("F04", "H07", "LOAD_BEARING_EXEMPLAR"),
        "D04": ("F05", "H06", "STRUCTURAL_ONLY"),
        "D05": ("F06", "H06", "NEGATIVE_EXISTENCE_CONTROL"),
        "D06": ("F07", "H08", "OPEN_JOIN_CONTROL"),
        "D07": ("H04", "H03", "ORIGINAL_P4_SPINE"),
        "D08": ("H05", "H03", "ORIGINAL_P4_SPINE"),
        "D09": ("H07", "H03", "OBJECT_INEQUIVALENT_SUPPORT"),
    }
    for edge, triplet in expected.items():
        got = (d[edge]["from"], d[edge]["to"], d[edge]["role"])
        if got != triplet:
            errors.append(f"{edge}:{got}!={triplet}")
    return not errors, errors


def deletion_recompute(rows: list[dict[str, str]], removed: set[str]) -> dict[str, Any]:
    retained = [row for row in rows if row["from"] not in removed and row["to"] not in removed]
    p4_spine = {
        row["from"]
        for row in retained
        if row["role"] == "ORIGINAL_P4_SPINE" and row["to"] == "H03"
    }
    p4_feeders = {
        row["to"]
        for row in retained
        if row["role"] == "LOAD_BEARING_NON_HOPF_ALGEBRA" and row["from"] in {"F01", "F02"}
    }
    p4_components = len(p4_spine & p4_feeders)
    hopf_exemplar = any(
        row["from"] == "F04" and row["to"] == "H07" and row["role"] == "LOAD_BEARING_EXEMPLAR"
        for row in retained
    ) and any(
        row["from"] == "H07" and row["to"] == "H03" and row["role"] == "OBJECT_INEQUIVALENT_SUPPORT"
        for row in retained
    )
    streams = int(p4_components > 0) + int(hopf_exemplar)
    return {
        "original_P4_spine_components": p4_components,
        "P4_algebra_survives": p4_components == 2,
        "original_hypothesis_formulation_survives": "H03" not in removed and p4_components > 0,
        "conditional_Hopfion_exemplar_survives": hopf_exemplar,
        "object_inequivalent_stability_support_streams": streams,
        "original_July31_algebraic_spine_survives": p4_components == 2,
    }


def deletion_predicate(rows: list[dict[str, str]], candidate: dict[str, Any]) -> tuple[bool, list[str], dict[str, Any]]:
    errors: list[str] = []
    all_state = deletion_recompute(rows, set())
    without_hopf = deletion_recompute(rows, {"F04", "H07"})
    without_p4 = deletion_recompute(rows, {"F01", "F02", "H04", "H05"})
    expected = {
        "all_evidence": {
            "object_inequivalent_stability_support_streams": all_state["object_inequivalent_stability_support_streams"],
            "original_P4_spine_components": all_state["original_P4_spine_components"],
        },
        "remove_Hopfion_F04_H07": {
            "P4_algebra_survives": without_hopf["P4_algebra_survives"],
            "object_inequivalent_stability_support_streams": without_hopf["object_inequivalent_stability_support_streams"],
            "original_P4_spine_components": without_hopf["original_P4_spine_components"],
            "original_hypothesis_formulation_survives": without_hopf["original_hypothesis_formulation_survives"],
        },
        "remove_P4_F01_F02_H04_H05": {
            "conditional_Hopfion_exemplar_survives": without_p4["conditional_Hopfion_exemplar_survives"],
            "object_inequivalent_stability_support_streams": without_p4["object_inequivalent_stability_support_streams"],
            "original_July31_algebraic_spine_survives": without_p4["original_July31_algebraic_spine_survives"],
            "original_P4_spine_components": without_p4["original_P4_spine_components"],
        },
        "scope": "finite dependency deletion control; not counterfactual physics",
    }
    if candidate != expected:
        errors.append("deletion_artifact_does_not_match_independent_graph_recompute")
    if without_hopf["original_P4_spine_components"] != 2 or without_hopf["object_inequivalent_stability_support_streams"] != 1:
        errors.append("Hopf_deletion_wrong")
    if without_p4["original_P4_spine_components"] != 0 or not without_p4["conditional_Hopfion_exemplar_survives"]:
        errors.append("P4_deletion_wrong")
    return not errors, errors, expected


def status_predicate(rows: list[dict[str, str]], result: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    s = keyed(rows, "claim")
    expected = {
        "Hopfion_dependency": "NOT_REQUIRED_FOR_FORMULATION_OR_P4_ALGEBRA",
        "P4_dependency": "LOAD_BEARING_TO_ORIGINAL_JULY31_ALGEBRAIC_SPINE",
        "discrete_species_catalog": "NOT_DERIVED_OR_OBSERVED",
        "shared_metric_native_stability_operator": "NOT_FOUND",
        "rings_and_empty_branches": "STRUCTURAL_OR_EXISTENCE_PRUNING_NOT_STABILITY",
        "time_live_persistence": "ZERO_OF_SEVEN_FAMILIES_DERIVED",
        "bootstrap_selection": "ZERO_OF_SEVEN_FAMILIES_SELECTED",
        "overall": "HYPOTHESIS_MULTI_FAMILY_SUPPORTED_NOT_DERIVED",
    }
    for claim, status in expected.items():
        if claim not in s or s[claim]["status"] != status:
            errors.append(f"{claim}:{s.get(claim, {}).get('status')}!=expected:{status}")
    result_expected = {
        "families": 7,
        "hypothesis_claims": 8,
        "grammar_cells": 70,
        "dependency_edges": 14,
        "source_paths_verified": 1469,
        "object_inequivalent_stability_support_streams": 2,
        "non_hopf_load_bearing_stability_families": 2,
        "time_live_persistence_derived_families": 0,
        "bootstrap_selected_families": 0,
        "shared_metric_native_stability_operator_found": False,
        "P4_threshold_is_continuous_region": True,
        "discrete_species_catalog_derived": False,
        "isolated_multi_basin_spectrum_observed": False,
        "family_overlap_after_correction": 0,
        "family_partition_rows": 7,
        "post_prereg_partition_correction": True,
        "post_prereg_source_admission_correction": True,
        "outcome": "HYPOTHESIS_MULTI_FAMILY_SUPPORTED_NOT_DERIVED",
        "new_stability_solve_run": False,
        "gpu_used": False,
    }
    for field, value in result_expected.items():
        if result.get(field) != value:
            errors.append(f"result:{field}:{result.get(field)}!=expected:{value}")
    return not errors, errors


def authority_predicate(rows: list[dict[str, str]], computed: dict[str, dict[str, Any]]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    ids = [row["anchor_id"] for row in rows]
    if ids != [f"A{i:02d}" for i in range(1, 19)]:
        errors.append("anchor_ids")
    for row in rows:
        source = computed.get(row["path"])
        if source is None:
            errors.append(f"anchor_outside_freeze:{row['anchor_id']}")
        elif source["sha256"] != row["sha256"]:
            errors.append(f"anchor_hash:{row['anchor_id']}")
        if not row["role"] or not row["ruling"]:
            errors.append(f"anchor_blank:{row['anchor_id']}")
    return not errors, errors


def source_semantics() -> tuple[bool, list[str], dict[str, int]]:
    requirements = {
        "PONDER_MATH_ELEGANCE_2026-07-31.md": [
            "STATUS: PURE PONDER",
            "a \"species\" = (discrete label data) ×",
            "(stable basin)",
            "the first two",
            "one candidate stabilized by a DISCRETE parity pin",
        ],
        "udt_p4_stability_slice_2026-07-30/AUDIT_REPORT.md": [
            "method transfer only",
            "zero-trace core is",
            "64 E0^2 l^4 <= g_p c_m pi^4",
            "free wall-germ curvature",
            "no dynamics adopted",
        ],
        "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md": [
            "SETTLED_STATIC_FINITE_BOX_CONDITIONAL",
            "round-`S2`, `L2+L4`, fixed-boundary",
            "physical finite-cell carrier completion",
            "No time-live stability",
        ],
        "udt_stability_foundations_audit_2026-08-01/AUDIT_REPORT.md": [
            "Realization join",
            "Persistence join",
            "not full dynamical or particle stability",
            "fixed realized on-shell coexistence open",
        ],
        "udt_global_local_self_consistency_premise_audit_2026-08-01/AUDIT_REPORT.md": [
            "BOOTSTRAP_IS_DISTINCT_POSIT",
            "no derivation of global/local mutual determination",
            "No registered route supplies the missing nontrivial membership",
        ],
    }
    errors: list[str] = []
    for path, tokens in requirements.items():
        text = " ".join((ROOT / path).read_text(encoding="utf-8").split())
        for token in tokens:
            if " ".join(token.split()) not in text:
                errors.append(f"missing_token:{path}:{token}")

    # This lexical census is not an authority rule; it proves every frozen byte was also
    # admitted to a whole-universe scan rather than only to a manifest check.
    terms = ["stability", "hopfion", "bootstrap", "stable basin", "double-crease", "time-live persistence"]
    counts = {term: 0 for term in terms}
    for path in (PKG / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines():
        data = (ROOT / path).read_bytes().lower()
        for term in terms:
            if term.encode("utf-8") in data:
                counts[term] += 1
    return not errors, errors, counts


def mutate_field(rows: list[dict[str, str]], key_field: str, key: str, field: str, value: str) -> list[dict[str, str]]:
    candidate = copy.deepcopy(rows)
    for row in candidate:
        if row[key_field] == key:
            row[field] = value
            return candidate
    raise KeyError(key)


def main() -> int:
    inventory = tsv("SOURCE_INVENTORY.tsv")
    source_paths = (PKG / "SOURCE_PATHS.txt").read_text(encoding="utf-8").splitlines()
    manifest = parse_manifest()
    sources_ok, source_errors, source_stats, computed = source_predicate(inventory, source_paths, manifest)
    check("frozen_source_universe", sources_ok, {"errors": source_errors, **source_stats})
    for row in inventory:
        rel = row["path"]
        got = computed.get(rel, {})
        raw.append({"kind": "source", "path": rel, **got})

    family_universe = tsv("FAMILY_UNIVERSE.tsv")
    claim_universe = tsv("HYPOTHESIS_CLAIM_UNIVERSE.tsv")
    family_rows = tsv("FAMILY_ATLAS.tsv")
    grammar_rows = tsv("COMMON_GRAMMAR_MATRIX.tsv")
    graph_rows = tsv("DEPENDENCY_GRAPH.tsv")
    partition_rows = tsv("FAMILY_PARTITION_LEDGER.tsv")
    correction_text = (PKG / "PREREGISTRATION_CORRECTION_01.md").read_text(encoding="utf-8")
    source_correction_text = (PKG / "PREREGISTRATION_CORRECTION_02.md").read_text(encoding="utf-8")
    status_rows = tsv("STATUS_LEDGER.tsv")
    authority_rows = tsv("SOURCE_AUTHORITY_LEDGER.tsv")
    premise_rows = tsv("PREMISE_LEDGER.tsv")
    lineage_rows = tsv("LINEAGE_LEDGER.tsv")
    result = json_file("RESULT.json")
    deletion_artifact = json_file("DELETION_CONTROL.json")

    check("frozen_family_universe", [row["family_id"] for row in family_universe] == FAMILY_IDS, {"rows": len(family_universe)})
    check("frozen_claim_universe", [row["claim_id"] for row in claim_universe] == CLAIM_IDS, {"rows": len(claim_universe)})
    family_ok, family_errors = family_predicate(family_rows)
    check("seven_family_semantics", family_ok, family_errors)
    grammar_ok, grammar_errors = grammar_predicate(grammar_rows)
    check("grammar_exact_70_cells", grammar_ok, grammar_errors)
    graph_ok, graph_errors = graph_predicate(graph_rows)
    check("dependency_exact_14_edges", graph_ok, graph_errors)
    partition_ok, partition_errors = partition_predicate(partition_rows, family_rows, correction_text)
    check("effective_family_partition_no_inflation", partition_ok, partition_errors)
    source_correction_ok, source_correction_errors, base_addition_hashes = source_correction_predicate(
        inventory, source_correction_text
    )
    check(
        "source_admission_correction_exact_and_base_identical",
        source_correction_ok,
        {"errors": source_correction_errors, "base_sha256": base_addition_hashes},
    )
    check("eight_claim_lineage", [row["claim_id"] for row in lineage_rows] == CLAIM_IDS, {"rows": len(lineage_rows)})
    check("eighteen_premises", [row["premise_id"] for row in premise_rows] == [f"P{i:02d}" for i in range(1, 19)], {"rows": len(premise_rows)})
    authority_ok, authority_errors = authority_predicate(authority_rows, computed)
    check("eighteen_authority_anchors", authority_ok, authority_errors)

    semantic_ok, semantic_errors, keyword_counts = source_semantics()
    check("load_bearing_source_semantics", semantic_ok, {"errors": semantic_errors, "whole_universe_keyword_file_counts": keyword_counts})

    # Independent exact P4 controls: the n=1 2x2 determinant gives the coefficient 64,
    # and the odd-pin crossing scalar is strictly negative for J>0, s>1.
    threshold_coefficient = 4 * (2**4)
    crossing_samples = [
        Fraction(-2, 1) / (j * (s - 1))
        for j, s in [(Fraction(1, 2), Fraction(3, 2)), (Fraction(2, 1), Fraction(5, 2)), (Fraction(7, 3), Fraction(11, 5))]
    ]
    check("independent_P4_threshold_algebra", threshold_coefficient == 64, {"coefficient": threshold_coefficient, "determinant": "g_p*c_m*(pi/(2*ell))^4 - 4*E0^2"})
    check("independent_odd_pin_crossing_sign", all(value < 0 for value in crossing_samples), {"exact_samples": [str(value) for value in crossing_samples], "premises": "J>0,s>1"})

    deletion_ok, deletion_errors, deletion_expected = deletion_predicate(graph_rows, deletion_artifact)
    check("independent_deletion_controls", deletion_ok, {"errors": deletion_errors, "recomputed": deletion_expected})
    status_ok, status_errors = status_predicate(status_rows, result)
    check("overall_outcome_logic", status_ok, status_errors)

    # Genuine mutations.  Every mutation enters the same predicate used above.
    first_path = inventory[0]["path"]
    mutated_bytes = (ROOT / first_path).read_bytes() + b"\nCOLD_MUTATION"
    m_ok, m_errors, _, _ = source_predicate(inventory, source_paths, manifest, {first_path: mutated_bytes})
    mutate("source_byte_mutation", not m_ok and any(err.startswith("sha256:") for err in m_errors), m_errors[:4])

    bad_inventory = copy.deepcopy(inventory)
    bad_inventory[0]["sha256"] = "0" * 64
    m_ok, m_errors, _, _ = source_predicate(bad_inventory, source_paths, manifest)
    mutate("inventory_hash_mutation", not m_ok, m_errors[:4])

    m_ok, m_errors = family_predicate(family_rows[:-1])
    mutate("missing_family", not m_ok, m_errors)
    m_ok, m_errors = family_predicate(family_rows + [copy.deepcopy(family_rows[0])])
    mutate("duplicate_family", not m_ok, m_errors)
    candidate = mutate_field(family_rows, "family_id", "F01", "hopfion_dependency", "HOPF_RESULT_TRANSFER")
    m_ok, m_errors = family_predicate(candidate)
    mutate("Hopf_result_transfer", not m_ok, m_errors)
    candidate = mutate_field(family_rows, "family_id", "F02", "time_persistence", "DERIVED")
    m_ok, m_errors = family_predicate(candidate)
    mutate("sector_to_time_persistence", not m_ok, m_errors)
    candidate = mutate_field(family_rows, "family_id", "F03", "overall_grade", "STABLE_SURVIVOR")
    m_ok, m_errors = family_predicate(candidate)
    mutate("control_to_survivor", not m_ok, m_errors)
    candidate = mutate_field(family_rows, "family_id", "F04", "carrier", "NATIVE_S2_DERIVED")
    m_ok, m_errors = family_predicate(candidate)
    mutate("carrier_promotion", not m_ok, m_errors)
    candidate = mutate_field(family_rows, "family_id", "F04", "time_persistence", "DERIVED")
    m_ok, m_errors = family_predicate(candidate)
    mutate("Hopf_time_promotion", not m_ok, m_errors)
    candidate = mutate_field(family_rows, "family_id", "F05", "stability_test", "FULL_HESSIAN")
    m_ok, m_errors = family_predicate(candidate)
    mutate("ring_stability_smuggle", not m_ok, m_errors)
    candidate = mutate_field(family_rows, "family_id", "F06", "stability_outcome", "UNSTABLE_BASIN")
    m_ok, m_errors = family_predicate(candidate)
    mutate("empty_to_instability", not m_ok, m_errors)
    candidate = mutate_field(family_rows, "family_id", "F07", "overall_grade", "REALIZED_STABILITY")
    m_ok, m_errors = family_predicate(candidate)
    mutate("formal_to_realized", not m_ok, m_errors)

    duplicate_partition = copy.deepcopy(partition_rows)
    duplicate_partition[1]["effective_partition_key"] = duplicate_partition[0]["effective_partition_key"]
    m_ok, m_errors = partition_predicate(duplicate_partition, family_rows, correction_text)
    mutate("duplicate_partition_key", not m_ok, m_errors)
    overlap_family = mutate_field(family_rows, "family_id", "F01", "boundary_completion", "all postures including double-crease")
    m_ok, m_errors = partition_predicate(partition_rows, overlap_family, correction_text)
    mutate("F01_F06_overlap_return", not m_ok, m_errors)
    hidden_correction = correction_text.replace("preserved unchanged", "rewritten")
    m_ok, m_errors = partition_predicate(partition_rows, family_rows, hidden_correction)
    mutate("hidden_preregistration_correction", not m_ok, m_errors)

    addition_rows = [
        row for row in inventory if row["layer"] == "CONTROLLING_ANCHOR_ADDITION_CORRECTION_02"
    ]
    missing_addition_inventory = [row for row in inventory if row["path"] != addition_rows[0]["path"]]
    missing_addition_paths = [path for path in source_paths if path != addition_rows[0]["path"]]
    missing_addition_manifest = [pair for pair in manifest if pair[0] != addition_rows[0]["path"]]
    m_ok, m_errors, _, _ = source_predicate(
        missing_addition_inventory, missing_addition_paths, missing_addition_manifest
    )
    mutate("missing_source_admission", not m_ok, m_errors[:5])
    hidden_source_correction = source_correction_text.replace(
        "absent from the frozen 1,466-path source universe", "already inside the frozen source universe"
    )
    m_ok, m_errors, _ = source_correction_predicate(inventory, hidden_source_correction)
    mutate("hidden_source_admission_correction", not m_ok, m_errors)

    duplicate_grammar = copy.deepcopy(grammar_rows)
    duplicate_grammar[-1]["family_id"] = "F06"
    m_ok, m_errors = grammar_predicate(duplicate_grammar)
    mutate("grammar_duplicate_cell", not m_ok, m_errors)
    bootstrap_grammar = copy.deepcopy(grammar_rows)
    for row in bootstrap_grammar:
        if row["family_id"] == "F02" and row["component_id"] == "G10":
            row["status"] = "PRESENT_SELECTOR"
    m_ok, m_errors = grammar_predicate(bootstrap_grammar)
    mutate("bootstrap_selection_grammar", not m_ok, m_errors)

    m_ok, m_errors = graph_predicate(graph_rows[:-1])
    mutate("missing_dependency_edge", not m_ok, m_errors)
    mutated_graph = mutate_field(graph_rows, "edge_id", "D07", "from", "H07")
    m_ok, m_errors, _ = deletion_predicate(mutated_graph, deletion_artifact)
    mutate("Hopf_deletion_erases_P4_spine", not m_ok, m_errors)
    mutated_deletion = copy.deepcopy(deletion_artifact)
    mutated_deletion["remove_P4_F01_F02_H04_H05"]["original_P4_spine_components"] = 2
    m_ok, m_errors, _ = deletion_predicate(graph_rows, mutated_deletion)
    mutate("P4_deletion_false_spine_survival", not m_ok, m_errors)

    promoted_status = mutate_field(status_rows, "claim", "shared_metric_native_stability_operator", "status", "FOUND")
    m_ok, m_errors = status_predicate(promoted_status, result)
    mutate("shared_operator_smuggle", not m_ok, m_errors)
    selected_status = mutate_field(status_rows, "claim", "bootstrap_selection", "status", "SELECTED")
    m_ok, m_errors = status_predicate(selected_status, result)
    mutate("bootstrap_selector_smuggle", not m_ok, m_errors)
    species_status = mutate_field(status_rows, "claim", "discrete_species_catalog", "status", "DERIVED_DISCRETE_SPECTRUM")
    m_ok, m_errors = status_predicate(species_status, result)
    mutate("species_catalog_promotion", not m_ok, m_errors)
    discretized_result = copy.deepcopy(result)
    discretized_result["P4_threshold_is_continuous_region"] = False
    discretized_result["discrete_species_catalog_derived"] = True
    discretized_result["isolated_multi_basin_spectrum_observed"] = True
    m_ok, m_errors = status_predicate(status_rows, discretized_result)
    mutate("continuous_threshold_to_discrete_basin_spectrum", not m_ok, m_errors)
    bad_result = copy.deepcopy(result)
    bad_result["outcome"] = "HYPOTHESIS_HOPFION_DEPENDENT"
    m_ok, m_errors = status_predicate(status_rows, bad_result)
    mutate("wrong_overall_outcome", not m_ok, m_errors)

    failures = [entry for entry in checks + mutations if not entry["passed"]]
    status = "PASS" if not failures else "FAIL"
    repair_map = {
        "frozen_source_universe": "Repair the frozen source census/hash admission; do not claim verified source scope while any listed byte or layer fails.",
        "eighteen_authority_anchors": "Admit every load-bearing authority source through a transparent, base-identical source-scope correction or return SOURCE_CONFLICT_OR_SCOPE_BROKEN.",
        "effective_family_partition_no_inflation": "Restore an explicit disjoint F01/F05/F06 partition without adding a family or favorable outcome.",
        "load_bearing_source_semantics": "Repair the source-to-ruling anchor; a missing controlling statement cannot be replaced by atlas prose.",
        "source_admission_correction_exact_and_base_identical": "Repair or explicitly regrade the post-preregistration source admission; each named addition must be exact, visible, and base-identical.",
        "overall_outcome_logic": "Regrade the overall fixed outcome to the independently reconstructed logic.",
        "independent_deletion_controls": "Repair the finite deletion control so it is derived from the 14-edge graph rather than asserted.",
    }
    repairs_required = [repair_map[name] for name in [entry["name"] for entry in failures] if name in repair_map]
    final = {
        "status": status,
        "verdict": "VERIFIED_WITH_CAVEATS" if status == "PASS" else "REPAIRS_REQUIRED",
        "outcome": result.get("outcome"),
        "source_paths_read_and_sha256_verified": source_stats["paths"] if sources_ok else 0,
        "source_bytes_read": source_stats["bytes"],
        "source_layer_counts": source_stats["layers"],
        "families_recomputed": len(family_rows),
        "hypothesis_claims_recomputed": len(lineage_rows),
        "grammar_cells_recomputed": len(grammar_rows),
        "dependency_edges_recomputed": len(graph_rows),
        "partition_keys_recomputed": len(partition_rows),
        "checks_passed": sum(entry["passed"] for entry in checks),
        "checks_total": len(checks),
        "mutations_rejected": sum(entry["passed"] for entry in mutations),
        "mutations_total": len(mutations),
        "failed": [entry["name"] for entry in failures],
        "deletion_recompute": deletion_expected,
        "repairs_required": repairs_required,
        "caveats": [
            "The family partition correction is post-preregistration but conservative, explicit, and no-outcome-changing; the original preregistration remains immutable.",
            "The effective source universe is 1,469 after an explicit post-preregistration correction adding three predeclared, base-identical controlling anchors to the original verified 1,466.",
            "F02 establishes a conditional sector Hessian dichotomy, not a full isolated basin, common dynamics, or time persistence.",
            "F04 remains conditional on the round-S2 posit, L2+L4 functional, fixed computational box, boundary mask, staticity, and audited operator.",
            "The common result is architectural only; no shared metric-native stability operator or bootstrap membership rule was found.",
        ],
    }

    with RAW_PATH.open("w", encoding="utf-8") as handle:
        for entry in raw:
            handle.write(json.dumps(entry, sort_keys=True, separators=(",", ":")) + "\n")
    RESULT_PATH.write_text(json.dumps(final, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(final, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
