#!/usr/bin/env python3
"""Deterministically derive the conceptual closure status from the frozen ledgers."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def split_semicolon(value: str) -> list[str]:
    return [item for item in value.split(";") if item]


def split_comma(value: str) -> list[str]:
    return [item for item in value.split(",") if item]


def unique(rows: list[dict[str, str]], field: str) -> bool:
    values = [row[field] for row in rows]
    return len(values) == len(set(values))


def source_identity(path: str) -> tuple[str, str]:
    payload = (ROOT / path).read_bytes()
    sha = hashlib.sha256(payload).hexdigest()
    blob = subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    return sha, blob


def validate(
    clauses: list[dict[str, str]],
    joins: list[dict[str, str]],
    witnesses: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    expected_counts = {"clauses": 16, "joins": 9, "witnesses": 9, "sources": 22}
    actual_counts = {
        "clauses": len(clauses),
        "joins": len(joins),
        "witnesses": len(witnesses),
        "sources": len(sources),
    }
    if actual_counts != expected_counts:
        errors.append(f"count mismatch: {actual_counts!r}")
    for rows, field in (
        (clauses, "clause_id"),
        (joins, "join_id"),
        (witnesses, "witness_id"),
        (sources, "source"),
    ):
        if not unique(rows, field):
            errors.append(f"duplicate {field}")

    clause_ids = {row["clause_id"] for row in clauses}
    join_ids = {row["join_id"] for row in joins}
    source_paths = {row["source"] for row in sources}
    if clause_ids != {f"C{i:02d}" for i in range(1, 17)}:
        errors.append("clause identity set mismatch")
    if join_ids != {f"J{i:02d}" for i in range(1, 10)}:
        errors.append("join identity set mismatch")

    for row in clauses:
        for path in split_semicolon(row["source"]):
            if path not in source_paths:
                errors.append(f"unregistered source {path} in {row['clause_id']}")
    for row in witnesses:
        if row["source"] not in source_paths:
            errors.append(f"unregistered witness source {row['source']}")
    for row in joins:
        if row["current_status"] != "OPEN":
            errors.append(f"non-open join {row['join_id']}")
        if row["can_current_rules_choose"] != "NO":
            errors.append(f"unsupported promotion {row['join_id']}")
        for dependency in split_comma(row["depends_on"]):
            if dependency not in clause_ids | join_ids:
                errors.append(f"unknown dependency {dependency} in {row['join_id']}")

    clause_by_id = {row["clause_id"]: row for row in clauses}
    required_absences = {
        "C02": {"physical_section", "integral_constraint", "absolute_scale"},
        "C06": {"field_equation", "causal_comparability"},
        "C08": {"off_shell_functional", "variation_domain", "selection_map"},
        "C12": {"unique_positional_law_from_finite_bound", "physical_value"},
        "C13": {"absolute_length", "absolute_mass", "Xmax"},
        "C14": {"shape", "topology", "caps", "periods"},
        "C16": {"native_carrier_emergence", "source", "unconditional_mass"},
    }
    for clause_id, required in required_absences.items():
        if clause_id not in clause_by_id:
            errors.append(f"missing required clause {clause_id}")
            continue
        actual = set(split_semicolon(clause_by_id[clause_id]["not_provided"]))
        if not required <= actual:
            errors.append(f"missing fail-closed absence in {clause_id}: {sorted(required - actual)}")

    unifiers: dict[str, set[str]] = {}
    for row in joins:
        unifiers.setdefault(row["candidate_unifier"], set()).add(row["join_id"])
    expected_unifiers = {
        "GLOBAL_COMPLETION_MAP": {"J01", "J02", "J03", "J04", "J05"},
        "BOOTSTRAP_COMPLETION": {"J06", "J07"},
        "ACTION_BRIDGE": {"J08"},
        "MATTER_COMPLETION": {"J09"},
    }
    if unifiers != expected_unifiers:
        errors.append(f"unifier partition mismatch: {unifiers!r}")

    implications = {row["proposed_implication_defeated"] for row in witnesses}
    required_witness_topics = (
        "physical_representative",
        "complete_coframe_involution",
        "boundary_variation_domain",
        "off_shell_dynamics",
        "causal_comparability",
        "fractional_linear_position",
        "fix_Mtot_and_Xmax",
        "angular_geometry",
        "global_selector",
    )
    for topic in required_witness_topics:
        if not any(topic in implication for implication in implications):
            errors.append(f"missing counterwitness topic {topic}")

    for row in sources:
        path = row["source"]
        if not (ROOT / path).is_file():
            errors.append(f"missing source path {path}")
            continue
        try:
            sha, blob = source_identity(path)
        except subprocess.CalledProcessError:
            errors.append(f"source not tracked at HEAD {path}")
            continue
        if sha != row["sha256"]:
            errors.append(f"source SHA-256 mismatch {path}")
        if blob != row["git_blob"]:
            errors.append(f"source blob mismatch {path}")
    return errors


def make_graph(
    clauses: list[dict[str, str]], joins: list[dict[str, str]]
) -> dict[str, object]:
    nodes: list[dict[str, str]] = []
    edges: list[dict[str, str]] = []
    for row in clauses:
        nodes.append(
            {
                "id": row["clause_id"],
                "kind": "ESTABLISHED_OR_SCOPED_CLAUSE",
                "label": row["object"],
                "status": row["status"],
            }
        )
    for row in joins:
        nodes.append(
            {
                "id": row["join_id"],
                "kind": "OPEN_JOIN",
                "label": row["missing_object"],
                "status": row["current_status"],
            }
        )
        for dependency in split_comma(row["depends_on"]):
            edges.append(
                {"from": dependency, "to": row["join_id"], "relation": "REQUIRED_BY"}
            )
    return {"nodes": nodes, "edges": edges}


def exercise_catch_proofs(
    clauses: list[dict[str, str]],
    joins: list[dict[str, str]],
    witnesses: list[dict[str, str]],
    sources: list[dict[str, str]],
) -> dict[str, str]:
    proofs: dict[str, str] = {}

    def must_fail(name: str, c=None, j=None, w=None, s=None) -> None:
        result = validate(c or clauses, j or joins, w or witnesses, s or sources)
        proofs[name] = "PASS" if result else "FAIL"

    must_fail("missing_clause", c=clauses[:-1])
    must_fail("duplicate_clause", c=clauses + [deepcopy(clauses[0])])
    promoted = deepcopy(joins)
    promoted[0]["current_status"] = "DERIVED"
    promoted[0]["can_current_rules_choose"] = "YES"
    must_fail("unsupported_join_promotion", j=promoted)
    missing_join = [row for row in joins if row["join_id"] != "J03"]
    must_fail("missing_angular_join", j=missing_join)
    lost_csn = deepcopy(clauses)
    lost_csn[1]["not_provided"] = "action"
    must_fail("CSN_invented_integral_or_section", c=lost_csn)
    promoted_copresence = deepcopy(clauses)
    promoted_copresence[5]["not_provided"] = "boundary_rule"
    must_fail("copresence_invented_field_content", c=promoted_copresence)
    promoted_bootstrap = deepcopy(clauses)
    promoted_bootstrap[7]["not_provided"] = "density_center"
    must_fail("bootstrap_invented_off_shell_role", c=promoted_bootstrap)
    promoted_xmax = deepcopy(clauses)
    promoted_xmax[11]["not_provided"] = "action"
    must_fail("Xmax_invented_value_or_uniqueness", c=promoted_xmax)
    promoted_anchors = deepcopy(clauses)
    promoted_anchors[12]["not_provided"] = "native_charge"
    must_fail("cG_invented_absolute_scale", c=promoted_anchors)
    lost_angular = deepcopy(clauses)
    lost_angular[13]["not_provided"] = "twist"
    must_fail("angular_completion_silently_closed", c=lost_angular)
    lost_matter = deepcopy(clauses)
    lost_matter[15]["not_provided"] = "global_join"
    must_fail("matter_emergence_silently_closed", c=lost_matter)
    must_fail("missing_countermodel", w=witnesses[:-1])
    bad_source = deepcopy(sources)
    bad_source[0]["sha256"] = "0" * 64
    must_fail("source_identity_mutation", s=bad_source)
    return proofs


def main() -> None:
    clauses = read_tsv("CLAUSE_LEDGER.tsv")
    joins = read_tsv("OPEN_JOIN_LEDGER.tsv")
    witnesses = read_tsv("COUNTERMODEL_MATRIX.tsv")
    sources = read_tsv("SOURCE_LINEAGE.tsv")
    errors = validate(clauses, joins, witnesses, sources)
    if errors:
        raise SystemExit("\n".join(errors))

    outcomes = [
        "EXISTING_RULES_CONSTRAIN_BUT_DO_NOT_CLOSE",
        "CO_PRESENCE_CHANGES_INTERPRETATION_NOT_FIELD_CONTENT",
    ]
    result = {
        "audit_date": "2026-07-20",
        "base": "f104d74e3bdf4b2c94ff99557b156254d6a1a8a6",
        "maximum_conclusion": "UDT_GLOBAL_RECIPROCAL_CLOSURE_STATUS_CHARACTERIZED",
        "outcomes": outcomes,
        "outcomes_not_earned": [
            "EXISTING_RULES_DERIVE_GLOBAL_VARIATION_DOMAIN",
            "FINITE_CELL_OR_ANGULAR_COMPLETION_IS_THE_SMALLEST_OPEN_JOIN",
            "BOOTSTRAP_SELECTION_RULE_IS_THE_SMALLEST_OPEN_JOIN",
            "NEW_PREMISE_REQUIRED",
        ],
        "counts": {
            "established_or_scoped_clauses": len(clauses),
            "open_joins": len(joins),
            "counterwitnesses": len(witnesses),
            "pinned_sources": len(sources),
        },
        "first_missing_mathematical_type": {
            "name": "GLOBAL_COMPLETION_MAP",
            "status": "OPEN_TARGET_NOT_ADOPTED_PREMISE",
            "components": ["J01", "J02", "J03", "J04", "J05"],
            "interpretation": (
                "A source-authorized map from the local reciprocal CSN coframe and finite-cell "
                "sector data to one global metric object, its complete seal, and its allowed "
                "boundary tangent space."
            ),
        },
        "later_independent_gates": {
            "bootstrap_and_scale": ["J06", "J07"],
            "action_stage_or_bridge": ["J08"],
            "matter_source": ["J09"],
        },
        "strongest_supported_synthesis": "WORKING_GLOBAL_RECIPROCAL_FINITE_METRIC_SKELETON",
        "complete_action": "OPEN",
        "native_matter_source": "OPEN",
        "canonization": "NOT_AUTHORIZED",
        "catch_proofs": exercise_catch_proofs(clauses, joins, witnesses, sources),
    }
    if set(result["catch_proofs"].values()) != {"PASS"}:
        raise SystemExit("one or more catch-proofs failed")

    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (HERE / "DEPENDENCY_GRAPH.json").write_text(
        json.dumps(make_graph(clauses, joins), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
