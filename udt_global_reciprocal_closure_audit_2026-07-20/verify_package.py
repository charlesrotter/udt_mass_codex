#!/usr/bin/env python3
"""Independent fail-closed verifier for the reciprocal-closure conceptual audit."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load(name: str) -> dict[str, object]:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tracked_blob(path: str) -> str:
    return subprocess.run(
        ["git", "rev-parse", f"HEAD:{path}"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def main() -> None:
    clauses = rows("CLAUSE_LEDGER.tsv")
    joins = rows("OPEN_JOIN_LEDGER.tsv")
    witnesses = rows("COUNTERMODEL_MATRIX.tsv")
    sources = rows("SOURCE_LINEAGE.tsv")
    status = rows("STATUS_LEDGER.tsv")
    result = load("DERIVATION_RESULT.json")
    graph = load("DEPENDENCY_GRAPH.json")
    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    skeleton = (HERE / "CLOSURE_SKELETON.md").read_text(encoding="utf-8")
    next_decision = (HERE / "NEXT_SCIENTIFIC_DECISION.md").read_text(encoding="utf-8")

    clause_ids = {row["clause_id"] for row in clauses}
    join_ids = {row["join_id"] for row in joins}
    witness_ids = {row["witness_id"] for row in witnesses}
    status_ids = {row["id"] for row in status}
    source_paths = {row["source"] for row in sources}
    graph_nodes = {node["id"] for node in graph["nodes"]}
    graph_edges = {(edge["from"], edge["to"]) for edge in graph["edges"]}
    expected_outcomes = {
        "EXISTING_RULES_CONSTRAIN_BUT_DO_NOT_CLOSE",
        "CO_PRESENCE_CHANGES_INTERPRETATION_NOT_FIELD_CONTENT",
    }
    expected_not_earned = {
        "EXISTING_RULES_DERIVE_GLOBAL_VARIATION_DOMAIN",
        "FINITE_CELL_OR_ANGULAR_COMPLETION_IS_THE_SMALLEST_OPEN_JOIN",
        "BOOTSTRAP_SELECTION_RULE_IS_THE_SMALLEST_OPEN_JOIN",
        "NEW_PREMISE_REQUIRED",
    }
    source_identity_ok = all(
        (ROOT / row["source"]).is_file()
        and digest(ROOT / row["source"]) == row["sha256"]
        and tracked_blob(row["source"]) == row["git_blob"]
        for row in sources
    )
    all_dependencies = {
        (dependency, row["join_id"])
        for row in joins
        for dependency in row["depends_on"].split(",")
    }

    checks = {
        "clause_identity_and_count": len(clauses) == 16
        and clause_ids == {f"C{i:02d}" for i in range(1, 17)},
        "join_identity_and_count": len(joins) == 9
        and join_ids == {f"J{i:02d}" for i in range(1, 10)},
        "witness_identity_and_count": len(witnesses) == 9
        and witness_ids == {f"K{i:02d}" for i in range(1, 10)},
        "status_identity_and_count": len(status) == 21
        and status_ids == {f"S{i:02d}" for i in range(1, 22)},
        "source_identity_and_count": len(sources) == 22
        and len(source_paths) == 22
        and source_identity_ok,
        "all_joins_open_and_unselected": all(
            row["current_status"] == "OPEN" and row["can_current_rules_choose"] == "NO"
            for row in joins
        ),
        "graph_node_coverage": graph_nodes == clause_ids | join_ids,
        "graph_edge_coverage": graph_edges == all_dependencies,
        "registered_outcomes_exact": set(result["outcomes"]) == expected_outcomes,
        "unearned_outcomes_exact": set(result["outcomes_not_earned"]) == expected_not_earned,
        "global_completion_target_open": result["first_missing_mathematical_type"]["name"]
        == "GLOBAL_COMPLETION_MAP"
        and result["first_missing_mathematical_type"]["status"]
        == "OPEN_TARGET_NOT_ADOPTED_PREMISE"
        and set(result["first_missing_mathematical_type"]["components"])
        == {"J01", "J02", "J03", "J04", "J05"},
        "later_gates_separate": result["later_independent_gates"]
        == {
            "action_stage_or_bridge": ["J08"],
            "bootstrap_and_scale": ["J06", "J07"],
            "matter_source": ["J09"],
        },
        "complete_action_and_matter_open": result["complete_action"] == "OPEN"
        and result["native_matter_source"] == "OPEN",
        "maximum_conclusion_exact": result["maximum_conclusion"]
        == "UDT_GLOBAL_RECIPROCAL_CLOSURE_STATUS_CHARACTERIZED",
        "internal_catch_proofs_all_pass": len(result["catch_proofs"]) == 13
        and set(result["catch_proofs"].values()) == {"PASS"},
        "report_discloses_scoped_countermodels": "not claimed to be complete matter-bearing UDT"
        in report,
        "skeleton_discloses_non_authority": "not part of UDT authority" in skeleton,
        "next_action_excludes_open_choices": "not permission to" in next_decision
        and "No GPU work" in next_decision
        and "indicated for this question" in next_decision,
    }

    # Independent mutation-style catch proofs. Each forbidden promotion contradicts an exact current
    # row or result field and must therefore be detected by this verifier's predicates.
    clause_by_id = {row["clause_id"]: row for row in clauses}
    join_by_id = {row["join_id"]: row for row in joins}
    status_by_id = {row["id"]: row for row in status}
    catches = {
        "CSN_as_integral_selector_rejected": "integral_constraint"
        in clause_by_id["C02"]["not_provided"].split(";"),
        "copresence_as_field_equation_rejected": "field_equation"
        in clause_by_id["C06"]["not_provided"].split(";"),
        "bootstrap_as_off_shell_functional_rejected": "off_shell_functional"
        in clause_by_id["C08"]["not_provided"].split(";"),
        "finite_Xmax_as_unique_fractional_law_rejected": "unique_positional_law_from_finite_bound"
        in clause_by_id["C12"]["not_provided"].split(";"),
        "cG_as_absolute_scale_rejected": "absolute_length"
        in clause_by_id["C13"]["not_provided"].split(";"),
        "radial_reciprocity_as_angular_selector_rejected": "topology"
        in clause_by_id["C14"]["not_provided"].split(";"),
        "static_seal_as_complete_boundary_rejected": status_by_id["S04"]["status"]
        == "REFUTED_IMPLICATION",
        "global_object_promotion_rejected": status_by_id["S08"]["status"] == "NOT_DERIVED"
        and join_by_id["J01"]["current_status"] == "OPEN",
        "variation_domain_promotion_rejected": status_by_id["S09"]["status"] == "NOT_DERIVED"
        and join_by_id["J04"]["current_status"] == "OPEN",
        "angular_only_smallest_join_rejected": status_by_id["S10"]["status"] == "NOT_EARNED",
        "bootstrap_only_smallest_join_rejected": status_by_id["S11"]["status"] == "NOT_EARNED",
        "global_completion_as_adopted_premise_rejected": status_by_id["S12"]["status"]
        == "OPEN_TARGET_NOT_ADOPTED_PREMISE",
        "unconditional_action_rejected": status_by_id["S15"]["status"] == "NOT_DERIVED",
        "matter_promotion_rejected": status_by_id["S17"]["status"] == "OPEN",
        "new_premise_necessity_rejected": status_by_id["S18"]["status"] == "NOT_EARNED",
        "canonization_rejected": result["canonization"] == "NOT_AUTHORIZED",
    }

    if not all(checks.values()) or not all(catches.values()):
        raise AssertionError({"checks": checks, "catch_proofs": catches})

    output = {
        "schema": "udt-global-reciprocal-closure-verification-1.0",
        "result": "PASS_VERIFIED_WITH_CAVEATS",
        "checks": checks,
        "catch_proofs": catches,
        "counts": {
            "clauses": len(clauses),
            "open_joins": len(joins),
            "counterwitnesses": len(witnesses),
            "sources": len(sources),
            "status_rows": len(status),
            "graph_nodes": len(graph_nodes),
            "graph_edges": len(graph_edges),
        },
        "load_bearing_hashes": {
            name: digest(HERE / name)
            for name in (
                "CLAUSE_LEDGER.tsv",
                "OPEN_JOIN_LEDGER.tsv",
                "COUNTERMODEL_MATRIX.tsv",
                "SOURCE_LINEAGE.tsv",
                "DERIVATION_RESULT.json",
                "DEPENDENCY_GRAPH.json",
                "STATUS_LEDGER.tsv",
                "CLOSURE_SKELETON.md",
                "AUDIT_REPORT.md",
            )
        },
    }
    (HERE / "PACKAGE_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "result": output["result"],
                **output["counts"],
                "checks": len(checks),
                "catch_proofs": len(catches),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
