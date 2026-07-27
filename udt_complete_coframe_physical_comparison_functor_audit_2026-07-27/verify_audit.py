#!/usr/bin/env python3
"""Fail-closed verifier for the complete-coframe comparison-functor audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CLASS_IDS = {f"E{i:02d}" for i in range(1, 13)}
GATE_IDS = {f"G{i:02d}" for i in range(1, 13)}
CATCH_IDS = {f"F{i:02d}" for i in range(1, 25)}
STATUS_ALPHABET = {
    "DERIVED", "AVAILABLE_CONDITIONAL", "CLASSIFIED_FAMILY", "EXACT_WITNESS",
    "EXACT_COUNTERMODEL", "OPEN", "INACTIVE_PREMISE", "NOT_APPLICABLE",
    "OBSTRUCTED_ON_CONTROL_ONLY", "NOT_SELECTED",
}


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def run(script: str) -> tuple[int, str, str]:
    result = subprocess.run(
        [sys.executable, str(HERE / script)], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return result.returncode, result.stdout, result.stderr


def review_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    in_block = False
    for line in text.splitlines():
        if line == "```text REVIEW_FIELDS":
            in_block = True
            continue
        if in_block and line == "```":
            break
        if in_block and "=" in line:
            key, value = line.split("=", 1)
            fields[key.strip()] = value.strip()
    return fields


def load_state() -> dict[str, object]:
    return {
        "classes": table("EXTENSION_CLASS_UNIVERSE.tsv"),
        "gates": table("GATE_SCHEMA.tsv"),
        "matrix": table("CLASS_GATE_MATRIX.tsv"),
        "outcomes": table("CLASS_OUTCOMES.tsv"),
        "independent_matrix": table("INDEPENDENT_CLASS_GATE_STATUS.tsv"),
        "independent_outcomes": table("INDEPENDENT_CLASS_OUTCOMES.tsv"),
        "derived": json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "independent": json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8")),
        "review": review_fields((HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text(encoding="utf-8")),
    }


def unique(rows: list[dict[str, str]], key: str, expected: set[str]) -> None:
    values = [row[key] for row in rows]
    assert len(values) == len(set(values))
    assert set(values) == expected


def validate(state: dict[str, object]) -> None:
    classes = state["classes"]
    gates = state["gates"]
    matrix = state["matrix"]
    outcomes = state["outcomes"]
    independent_matrix = state["independent_matrix"]
    independent_outcomes = state["independent_outcomes"]
    derived = state["derived"]
    independent = state["independent"]
    review = state["review"]
    assert isinstance(classes, list) and isinstance(gates, list)
    assert isinstance(matrix, list) and isinstance(outcomes, list)
    assert isinstance(independent_matrix, list) and isinstance(independent_outcomes, list)
    assert isinstance(derived, dict) and isinstance(independent, dict) and isinstance(review, dict)

    unique(classes, "id", CLASS_IDS)
    unique(gates, "gate_id", GATE_IDS)
    assert len(matrix) == 144
    keys = [(row["class_id"], row["gate_id"]) for row in matrix]
    assert len(keys) == len(set(keys)) and set(keys) == {(c, g) for c in CLASS_IDS for g in GATE_IDS}
    assert {row["status"] for row in matrix} <= STATUS_ALPHABET
    independent_by_key = {(row["class_id"], row["gate_id"]): row["status"] for row in independent_matrix}
    assert len(independent_by_key) == 144
    assert all(independent_by_key[key] == row["status"] for key, row in zip(keys, matrix))

    unique(outcomes, "class_id", CLASS_IDS)
    independent_outcome_map = {row["class_id"]: row["outcome"] for row in independent_outcomes}
    assert len(independent_outcome_map) == 12
    assert all(independent_outcome_map[row["class_id"]] == row["outcome"] for row in outcomes)
    by_cell = {(row["class_id"], row["gate_id"]): row["status"] for row in matrix}
    assert by_cell[("E01", "G01")] == "NOT_APPLICABLE"
    assert by_cell[("E02", "G02")] == "CLASSIFIED_FAMILY"
    assert by_cell[("E03", "G02")] == "CLASSIFIED_FAMILY"
    assert by_cell[("E04", "G02")] == "CLASSIFIED_FAMILY"
    assert by_cell[("E05", "G02")] == "CLASSIFIED_FAMILY"
    assert by_cell[("E06", "G02")] == "AVAILABLE_CONDITIONAL"
    assert by_cell[("E06", "G12")] == "NOT_SELECTED"
    assert by_cell[("E07", "G01")] == "EXACT_COUNTERMODEL"
    assert by_cell[("E08", "G01")] == "EXACT_COUNTERMODEL"
    assert by_cell[("E10", "G12")] == "INACTIVE_PREMISE"
    assert all(by_cell[(class_id, "G03")] != "DERIVED" for class_id in CLASS_IDS)
    assert all(by_cell[(class_id, "G09")] != "DERIVED" for class_id in CLASS_IDS)

    expected_ranks = {
        "general": 7, "determinant_one": 6, "transverse_invariant": 4,
        "no_mixing": 3, "spectator_given_both": 0,
    }
    assert derived["extension_generator_rank"] == derived["metric_response_rank"] == 7
    assert derived["determinant_one_extension_rank"] == 6
    assert derived["transverse_invariant_residual_rank"] == 4
    assert derived["no_mixing_residual_rank"] == 3
    assert derived["spectator_residual_rank_given_both"] == 0
    assert independent["registered_residual_ranks"] == expected_ranks
    assert independent["registered_residual_metric_response_ranks"] == expected_ranks
    assert derived["path_functor_exact"] == {
        "composition": True, "reversal": True, "transported_generator_rule": True,
    }
    assert independent["independent_path_functor_holdout"] is True
    assert derived["composition_selects_extension_parameters"] is False
    assert independent["composition_selects_extension_parameters"] is False
    assert derived["physical_path_ontology_selected"] is False
    assert independent["physical_path_ontology_selected"] is False
    assert derived["endpoint_collapse_requires_holonomy_centralization"] is True
    assert independent["endpoint_collapse_requires_holonomy_centralization"] is True
    assert derived["full_so_1_3_commutator_constraint_rank"] == 15
    assert independent["full_Lorentz_commutator_constraint_rank"] == 15
    assert derived["full_so_1_3_centralizer_dimension"] == 1
    assert independent["full_Lorentz_centralizer_dimension"] == 1
    assert derived["founded_base_compatible_with_full_holonomy_centralizer"] is False
    assert independent["founded_base_in_full_centralizer"] is False
    assert derived["universal_holonomy_no_go_claimed"] is False
    assert derived["cross_branch_splice_used"] is False
    assert derived["strong_local_CSN_status"] == "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED_INACTIVE"
    assert derived["native_all_pairs_target"] == "OPEN_NOT_SELECTED"
    assert derived["Xmax_status"] == "WORKING_SCHEMA_UNCHANGED_NO_OPERATIONAL_JOIN"
    assert derived["bootstrap_status"] == "WORKING_ON_SHELL_ADMISSIBILITY_ONLY_UNCHANGED"
    assert derived["c_E_and_G_sufficient_for_length_or_density_closure"] is False
    assert independent["production_outputs_read"] is False
    assert independent["control_obstruction_scope"] == "FULL_HOLONOMY_TWISTED_CONTROL_ONLY"
    assert derived["physical_comparison_functor_status"] == "OPEN_NOT_SELECTED_IN_TWELVE_CLASS_UNIVERSE"
    assert review == {
        "verdict": "VERIFIED_WITH_CAVEATS",
        "source_first": "TRUE",
        "production_outputs_read_before_independent_verdict": "FALSE",
        "control_only_holonomy_scope_preserved": "TRUE",
        "physical_functor_promoted": "FALSE",
        "required_corrections_applied": "TRUE",
    }


def mutate_cell(state: dict[str, object], class_id: str, gate_id: str, status: str) -> None:
    for row in state["matrix"]:
        if row["class_id"] == class_id and row["gate_id"] == gate_id:
            row["status"] = status
            return
    raise AssertionError("cell not found")


def rejected(mutator) -> str:
    state = load_state()
    mutator(state)
    try:
        validate(state)
    except (AssertionError, KeyError, TypeError):
        return "PASS"
    raise AssertionError("mutation accepted")


def catch_proofs() -> list[dict[str, str]]:
    mutations = {
        "F01": lambda s: s["classes"].pop(),
        "F02": lambda s: s["matrix"].pop(),
        "F03": lambda s: mutate_cell(s, "E01", "G01", "EXACT_WITNESS"),
        "F04": lambda s: mutate_cell(s, "E02", "G02", "EXACT_WITNESS"),
        "F05": lambda s: mutate_cell(s, "E03", "G02", "EXACT_WITNESS"),
        "F06": lambda s: mutate_cell(s, "E04", "G02", "EXACT_WITNESS"),
        "F07": lambda s: mutate_cell(s, "E05", "G02", "EXACT_WITNESS"),
        "F08": lambda s: mutate_cell(s, "E06", "G12", "DERIVED"),
        "F09": lambda s: s["classes"].__setitem__(6, copy.deepcopy(s["classes"][5])),
        "F10": lambda s: s["classes"].__setitem__(7, copy.deepcopy(s["classes"][5])),
        "F11": lambda s: s["derived"].__setitem__("strong_local_CSN_status", "ACTIVE"),
        "F12": lambda s: mutate_cell(s, "E02", "G03", "DERIVED"),
        "F13": lambda s: mutate_cell(s, "E02", "G09", "DERIVED"),
        "F14": lambda s: s["derived"].__setitem__("composition_selects_extension_parameters", True),
        "F15": lambda s: s["derived"].__setitem__("physical_path_ontology_selected", True),
        "F16": lambda s: s["derived"].__setitem__("endpoint_collapse_requires_holonomy_centralization", False),
        "F17": lambda s: s["derived"].__setitem__("founded_base_compatible_with_full_holonomy_centralizer", True),
        "F18": lambda s: s["derived"].__setitem__("universal_holonomy_no_go_claimed", True),
        "F19": lambda s: s["derived"].__setitem__("cross_branch_splice_used", True),
        "F20": lambda s: s["derived"].__setitem__("native_all_pairs_target", "SELECTED"),
        "F21": lambda s: s["derived"].__setitem__("Xmax_status", "DERIVED"),
        "F22": lambda s: s["derived"].__setitem__("bootstrap_status", "DERIVED_LOCAL_EQUATION"),
        "F23": lambda s: s["derived"].__setitem__("c_E_and_G_sufficient_for_length_or_density_closure", True),
        "F24": lambda s: s["independent"].__setitem__("production_outputs_read", True),
    }
    contract = {row["catch_id"]: row["false_promotion_or_corruption"] for row in table("FALSIFICATION_CONTRACT.tsv")}
    assert set(contract) == CATCH_IDS and set(mutations) == CATCH_IDS
    return [
        {"catch_id": catch_id, "mutation": contract[catch_id], "status": rejected(mutations[catch_id])}
        for catch_id in sorted(CATCH_IDS)
    ]


def main() -> int:
    validate(load_state())
    code, source_stdout, source_stderr = run("verify_source_manifest.py")
    assert code == 0 and source_stderr == ""
    assert json.loads(source_stdout) == {"result": "PASS", "sources": 20}

    code, derivation_stdout, derivation_stderr = run("derive_complete_coframe_functor.py")
    assert code == 0 and derivation_stderr == ""
    assert json.loads(derivation_stdout) == json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert derivation_stdout == (HERE / "DERIVATION_STDOUT.txt").read_text(encoding="utf-8")
    assert derivation_stderr == (HERE / "DERIVATION_STDERR.txt").read_text(encoding="utf-8")

    code, independent_stdout, independent_stderr = run("verify_complete_coframe_functor_independent.py")
    assert code == 0 and independent_stderr == ""
    assert json.loads(independent_stdout) == json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8"))
    assert independent_stdout == (HERE / "INDEPENDENT_STDOUT.txt").read_text(encoding="utf-8")
    assert independent_stderr == (HERE / "INDEPENDENT_STDERR.txt").read_text(encoding="utf-8")
    independent_code = (HERE / "verify_complete_coframe_functor_independent.py").read_text(encoding="utf-8")
    for forbidden in ("derive_complete_coframe_functor", "DERIVATION_RESULT.json", "CLASS_GATE_MATRIX.tsv", '"CLASS_OUTCOMES.tsv"'):
        assert forbidden not in independent_code

    catches = catch_proofs()
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=("catch_id", "mutation", "status"))
        writer.writeheader()
        writer.writerows(catches)
    assert len(catches) == 24 and all(row["status"] == "PASS" for row in catches)

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    exact = (HERE / "EXACT_DERIVATION.md").read_text(encoding="utf-8")
    ledger = (HERE / "STATUS_LEDGER.tsv").read_text(encoding="utf-8")
    for token in (
        "TWELVE_REGISTERED_EXTENSION_CLASSES_CLASSIFIED",
        "CONTROL_SCOPED_HOLONOMY_OBSTRUCTION",
        "BRANCH_SPECIFIC_STATIONARY_DEPTH_EXISTS",
        "PHYSICAL_COMPARISON_FUNCTOR_REMAINS_OPEN",
        "No cross-branch splice",
    ):
        assert token in report
    for token in ("Pointwise extension space", "Arbitrary-generator typed path functor", "Endpoint collapse and holonomy", "Smallest residual"):
        assert token in exact
    assert "physical_comparison_functor\tOPEN_NOT_SELECTED_IN_TWELVE_CLASS_UNIVERSE" in ledger

    result = {
        "schema": "udt.complete_coframe_physical_comparison_functor.verification.v1",
        "status": "PASS_VERIFIED_WITH_CAVEATS",
        "sources": 20,
        "classes": 12,
        "gates": 12,
        "cells": 144,
        "catch_proofs": 24,
        "production_replay": "PASS",
        "independent_no_production_read_replay": "PASS",
        "fresh_adversarial_review": "VERIFIED_WITH_CAVEATS",
        "physical_functor": "OPEN_NOT_SELECTED",
        "audit_report_sha256": hashlib.sha256((HERE / "AUDIT_REPORT.md").read_bytes()).hexdigest(),
        "status_ledger_sha256": hashlib.sha256((HERE / "STATUS_LEDGER.tsv").read_bytes()).hexdigest(),
        "class_gate_matrix_sha256": hashlib.sha256((HERE / "CLASS_GATE_MATRIX.tsv").read_bytes()).hexdigest(),
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
