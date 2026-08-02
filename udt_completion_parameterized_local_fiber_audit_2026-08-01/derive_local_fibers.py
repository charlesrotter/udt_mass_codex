#!/usr/bin/env python3
"""Derive completion-parameterized local compatibility fibers and curvature obstructions."""

from __future__ import annotations

import ast
import csv
import json
from itertools import combinations
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    monodromy_source = ROOT / "udt_global_metric_assembly_atlas_2026-07-22/TORUS_MONODROMY_REGISTRY.tsv"
    monodromies = read_tsv(monodromy_source)
    graph_rows: list[dict[str, object]] = []
    graph_rrefs: dict[str, tuple[tuple[sp.Expr, ...], ...]] = {}
    for row in monodromies:
        matrix = sp.Matrix(ast.literal_eval(row["matrix"]))
        assert matrix.shape == (2, 2) and abs(int(matrix.det())) == 1
        # Columns span {(v,Mv)} in R^2 x R^2.
        graph_basis = sp.Matrix.vstack(sp.eye(2), matrix)
        graph_rank = int(graph_basis.rank())
        fixed_dim = 2 - int((matrix - sp.eye(2)).rank())
        constraint = sp.Matrix.hstack(-matrix, sp.eye(2))
        graph_rrefs[row["monodromy_id"]] = tuple(tuple(value for value in r) for r in constraint.rref()[0].tolist())
        graph_rows.append(
            {
                "monodromy_id": row["monodromy_id"],
                "matrix": row["matrix"],
                "monodromy_class": row["monodromy_class"],
                "descent_equation": "v_plus=M*v_minus",
                "graph_dimension_in_R4": graph_rank,
                "constraint_rank": int(constraint.rank()),
                "conditional_fixed_parallel_dimension": fixed_dim,
                "primary_ruling": "DISTINCT_ENDPOINT_MATCHING_FIBER_NOT_FIXED_SUBSPACE",
            }
        )
    assert len(graph_rows) == 8 and all(row["graph_dimension_in_R4"] == 2 for row in graph_rows)
    distinct_pairs = sum(graph_rrefs[left] != graph_rrefs[right] for left, right in combinations(graph_rrefs, 2))
    assert distinct_pairs == 28
    write_tsv("MONODROMY_LOCAL_FIBERS.tsv", graph_rows)

    # Identity-transition scalar jet control. Each endpoint has a value and first two derivatives.
    # Ck matching imposes k+1 independent equalities and defines a changing nested fiber.
    jet_rows = []
    for join, order in (("NO_JOIN", -1), ("C0_JOIN", 0), ("C1_JOIN", 1), ("C2_JOIN", 2)):
        constraints = max(0, order + 1)
        jet_rows.append(
            {
                "join_class": join,
                "matched_jet_order": order,
                "ambient_endpoint_jet_dimension": 6,
                "constraint_rank": constraints,
                "compatibility_fiber_dimension": 6 - constraints,
                "exact_control": "j_plus_through_k=j_minus_through_k" if order >= 0 else "none",
                "scope": "SCALAR_IDENTITY_TRANSITION_CONTROL_FULL_TRANSITION_ACTS_ON_JETS",
            }
        )
    assert [row["compatibility_fiber_dimension"] for row in jet_rows] == [6, 5, 4, 3]
    write_tsv("JET_MATCHING_FIBERS.tsv", jet_rows)

    # Cap control from the registered toric family: w=xV+yY closes, y!=0.
    cap_rows = []
    for cap_id, x, y in (("CAP_PLUS", sp.Rational(-1, 2), sp.Rational(1, 2)), ("CAP_MINUS", sp.Rational(1, 2), sp.Rational(1, 2))):
        f_cap = sp.simplify(-x / y)
        cap_rows.append(
            {
                "cap_id": cap_id,
                "x": str(x),
                "y": str(y),
                "f_cap": str(f_cap),
                "b_cap": "0",
                "df_cap": "0",
                "db_cap": "0",
                "chi_cap": "0",
                "exceptional_stratum_c": str(sp.simplify(f_cap**2)),
                "local_jet_fiber": f"f0={f_cap};b0=0;f1=0;b1=0;u1=0;u0>0",
            }
        )
    assert {row["f_cap"] for row in cap_rows} == {"-1", "1"}
    assert {row["exceptional_stratum_c"] for row in cap_rows} == {"1"}
    write_tsv("CAP_LOCAL_JET_FIBERS.tsv", cap_rows)

    candidates = [
        {"candidate_id": "G01", "global_data_class": "POINTWISE_CURVATURE_DATA", "registered_datum": "YES_LOCAL_TENSOR_READOUT", "independent_global_argument": "NO", "natural_local_fiber": "NO", "distinct_fibers": "NO", "same_configuration_reidentification": "YES_AS_READOUT", "premise_firewall": "PASS", "ruling": "FORWARD_LOCAL_READOUT_NOT_RETURN"},
        {"candidate_id": "G02", "global_data_class": "PRESCRIBED_CURVATURE_LEVEL", "registered_datum": "NO_SELECTED_LEVEL", "independent_global_argument": "ONLY_IF_ADDED", "natural_local_fiber": "NO", "distinct_fibers": "FORMAL_LEVEL_SETS_ONLY", "same_configuration_reidentification": "CONDITIONAL", "premise_firewall": "FAIL_IF_LEVEL_ADOPTED", "ruling": "BLOCKED_ARBITRARY_LEVEL_SET"},
        {"candidate_id": "G03", "global_data_class": "CURVATURE_SPECTRUM_OR_DISTRIBUTION", "registered_datum": "NO_CHOICE_FREE_GLOBAL_OBJECT", "independent_global_argument": "NO", "natural_local_fiber": "NO", "distinct_fibers": "NO", "same_configuration_reidentification": "NO", "premise_firewall": "PASS", "ruling": "BLOCKED_OPERATOR_DOMAIN_MEASURE_CHOICE"},
        {"candidate_id": "G04", "global_data_class": "CURVATURE_INTEGRAL_OR_NORMALIZED_AVERAGE", "registered_datum": "UNSELECTED_FUNCTIONAL_FAMILY", "independent_global_argument": "ONLY_IF_ADDED", "natural_local_fiber": "NO", "distinct_fibers": "FORMAL_ONLY", "same_configuration_reidentification": "CONDITIONAL_ON_DOMAIN_WEIGHT", "premise_firewall": "FAIL_IF_PROMOTED", "ruling": "BLOCKED_INTEGRAL_WEIGHT_NORMALIZATION_CHOICE"},
        {"candidate_id": "G05", "global_data_class": "PATH_LOOP_HOLONOMY", "registered_datum": "CONDITIONAL_PATH_OR_LOOP_OUTPUT", "independent_global_argument": "PATH_QUERY_SUPPLIED", "natural_local_fiber": "ENDPOINT_TRANSPORT_GRAPH_FOR_SPECIFIED_PATH", "distinct_fibers": "YES_CONDITIONAL_ON_PATH_AND_METRIC", "same_configuration_reidentification": "YES_CONDITIONAL", "premise_firewall": "PASS", "ruling": "CONDITIONAL_TRANSPORT_FIBER_NOT_CONFIGURATION_ADMISSIBILITY"},
        {"candidate_id": "G06", "global_data_class": "DISCRETE_TOPOLOGY_COMPLETION_LABEL", "registered_datum": "YES_LABEL", "independent_global_argument": "YES", "natural_local_fiber": "NO_FROM_LABEL_ALONE", "distinct_fibers": "NO_UNLESS_ACTION_DATA_SUPPLIED", "same_configuration_reidentification": "YES_CLASSIFICATION", "premise_firewall": "PASS", "ruling": "SUPPLIED_LABEL_WITHOUT_LOCAL_ACTION"},
        {"candidate_id": "G07", "global_data_class": "TRANSITION_MONODROMY_REPRESENTATION", "registered_datum": "YES_GL2Z_PARAMETRIC_FAMILY_AND_WITNESSES", "independent_global_argument": "YES", "natural_local_fiber": "GRAPH_M_ENDPOINT_DESCENT", "distinct_fibers": "YES_28_OF_28_WITNESS_PAIRS", "same_configuration_reidentification": "SCHEMA_ONLY_NO_COMPLETE_METRIC_WITNESS", "premise_firewall": "PASS", "ruling": "NATURAL_PARAMETRIC_LOCAL_JOIN_FIBER_SCHEMA"},
        {"candidate_id": "G08", "global_data_class": "SMOOTH_CAP_DEGENERATION_DATA", "registered_datum": "YES_CONDITIONAL_REGISTERED_TORIC_FAMILY", "independent_global_argument": "YES_CAP_CYCLE", "natural_local_fiber": "CAP_REGULARITY_JET_CONDITIONS", "distinct_fibers": "YES_FCAP_PLUS_MINUS_ONE", "same_configuration_reidentification": "YES_FROM_CLOSING_CYCLE_AND_CAP_LIMIT", "premise_firewall": "PASS", "ruling": "NATURAL_PARTIAL_CAP_JET_FIBER_CONDITIONAL_FAMILY"},
        {"candidate_id": "G09", "global_data_class": "SEAM_GLUE_MATCHING_DATA", "registered_datum": "YES_REGULARITY_CLASS_SCHEMA", "independent_global_argument": "YES_TRANSITION_AND_K", "natural_local_fiber": "TRANSFORMED_JET_MATCHING", "distinct_fibers": "YES_C0_C1_C2_NESTED_CONTROLS", "same_configuration_reidentification": "SCHEMA_IF_FULL_TRANSITION_SUPPLIED", "premise_firewall": "PASS", "ruling": "NATURAL_PARAMETRIC_JET_MATCHING_SCHEMA_PHYSICAL_SEAM_OPEN"},
        {"candidate_id": "G10", "global_data_class": "COMPLETION_SCOPED_R_GEOM", "registered_datum": "YES_PARTIAL_12_BY_17_SCHEMA", "independent_global_argument": "COMPLETION_SUPPLIED", "natural_local_fiber": "COMPATIBILITY_ROWS_ONLY", "distinct_fibers": "YES_SCHEMA_DIFFERENCES", "same_configuration_reidentification": "NO_COMPLETE_WITNESS", "premise_firewall": "PASS", "ruling": "PARTIAL_READOUT_AND_COMPATIBILITY_NOT_COMPLETE_RETURN"},
        {"candidate_id": "G11", "global_data_class": "COMPLETION_CONDITIONED_PROJECTOR_NEIGHBORHOOD", "registered_datum": "YES_ONLY_FC04_S3_CONSTRUCTIVE_WITNESS", "independent_global_argument": "COMPLETION_SUPPLIED", "natural_local_fiber": "INTERSECTION_DEFINED_FOR_S3_ONLY", "distinct_fibers": "NO_CROSS_COMPLETION_PROJECTOR_FAMILY", "same_configuration_reidentification": "YES_BOUNDED_S3", "premise_firewall": "PASS", "ruling": "SINGLE_COMPLETION_COMPATIBILITY_NOT_CHANGING_FAMILY"},
        {"candidate_id": "G12", "global_data_class": "COMBINED_CURVATURE_COMPLETION_SELECTOR", "registered_datum": "NO_SELECTOR", "independent_global_argument": "UNDEFINED", "natural_local_fiber": "NO", "distinct_fibers": "NO_SELECTED_FAMILY", "same_configuration_reidentification": "NO", "premise_firewall": "PASS", "ruling": "NO_CURRENT_SELECTOR_OR_BOOTSTRAP_RETURN"},
    ]
    write_tsv("GLOBAL_DATA_FIBER_GATE_MATRIX.tsv", candidates)

    hierarchy = [
        {"object": "topology_label", "status": "CLASSIFICATION_ONLY", "local_effect": "none_without_transition_cap_or_action_data", "selection": "OPEN"},
        {"object": "transition_monodromy", "status": "DERIVED_PARAMETRIC_COMPLETION_DATA", "local_effect": "endpoint_pair_must_lie_in_Graph_M", "selection": "OPEN"},
        {"object": "join_regularity_class", "status": "REGISTERED_SCHEMA", "local_effect": "transformed_jets_through_k_must_match", "selection": "OPEN"},
        {"object": "smooth_cap_cycle", "status": "DERIVED_CONDITIONAL_ON_REGISTERED_TORIC_FAMILY", "local_effect": "closing_cycle_sets_cap_value_and_even_jet_conditions", "selection": "OPEN"},
        {"object": "curvature_holonomy", "status": "METRIC_READOUT_OR_CONDITIONAL_TRANSPORT", "local_effect": "parallel_fixed_subspace_only_if_parallelism_independently_required", "selection": "OPEN"},
        {"object": "complete_physical_bootstrap_fiber", "status": "OPEN", "local_effect": "no_native_on_shell_mass_energy_stability_membership", "selection": "OPEN"},
    ]
    write_tsv("FIBER_OWNERSHIP_LEDGER.tsv", hierarchy)

    result = {
        "schema": "udt.completion_parameterized_local_fiber.result.v1",
        "status": "PASS",
        "outcome": "COMPLETION_DATA_SUPPLY_PARAMETRIC_LOCAL_FIBER_SCHEMAS_AND_ONE_CONDITIONAL_CAP_REALIZATION__CURVATURE_RETURN_AND_PHYSICAL_SELECTION_OPEN",
        "candidate_count": len(candidates),
        "parametric_fiber_schema_routes": ["G07", "G09"],
        "conditional_completed_family_fiber_route": "G08",
        "conditional_transport_route": "G05",
        "curvature_native_return_routes": 0,
        "physical_completion_selectors": 0,
        "monodromy_witnesses": len(graph_rows),
        "distinct_monodromy_graph_pairs": distinct_pairs,
        "jet_fiber_dimensions": [row["compatibility_fiber_dimension"] for row in jet_rows],
        "cap_f_values": sorted(row["f_cap"] for row in cap_rows),
        "maximum_conclusion": "PARTIAL_KINEMATIC_GLOBAL_TO_LOCAL_FIBER_FAMILY_ONLY_NO_BOOTSTRAP_DYNAMICS_STABILITY_OR_SELECTION",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
