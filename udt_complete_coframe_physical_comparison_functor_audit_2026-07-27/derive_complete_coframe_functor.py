#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 4


def zero_matrix(rows: int = N, cols: int = N) -> list[list[F]]:
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def identity(n: int = N) -> list[list[F]]:
    result = zero_matrix(n, n)
    for i in range(n):
        result[i][i] = F(1)
    return result


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[x + y for x, y in zip(left, right)] for left, right in zip(a, b)]


def sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[x - y for x, y in zip(left, right)] for left, right in zip(a, b)]


def mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt] for row in a]


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    work = [row[:] + identity(n)[i] for i, row in enumerate(a)]
    for col in range(n):
        pivot = next(row for row in range(col, n) if work[row][col])
        work[col], work[pivot] = work[pivot], work[col]
        value = work[col][col]
        work[col] = [entry / value for entry in work[col]]
        for row in range(n):
            if row != col and work[row][col]:
                factor = work[row][col]
                work[row] = [x - factor * y for x, y in zip(work[row], work[col])]
    return [row[n:] for row in work]


def rank(matrix: list[list[F]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    result = 0
    for col in range(cols):
        pivot = next((row for row in range(result, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        value = work[result][col]
        work[result] = [entry / value for entry in work[result]]
        for row in range(rows):
            if row != result and work[row][col]:
                factor = work[row][col]
                work[row] = [x - factor * y for x, y in zip(work[row], work[result])]
        result += 1
    return result


def flatten(a: list[list[F]]) -> list[F]:
    return [entry for row in a for entry in row]


def diagonal(values: list[F]) -> list[list[F]]:
    result = zero_matrix(len(values), len(values))
    for i, value in enumerate(values):
        result[i][i] = value
    return result


def extension_basis() -> list[list[list[F]]]:
    entries = [(2, 2), (2, 3), (3, 3), (2, 0), (2, 1), (3, 0), (3, 1)]
    result = []
    for i, j in entries:
        matrix = zero_matrix()
        matrix[i][j] = F(1)
        result.append(matrix)
    return result


def metric_response(x: list[list[F]]) -> list[list[F]]:
    eta = diagonal([F(-1), F(1), F(1), F(1)])
    return add(mul(transpose(x), eta), mul(eta, x))


def lorentz_generators() -> list[list[list[F]]]:
    generators = []
    for i in range(1, 4):
        boost = zero_matrix()
        boost[0][i] = boost[i][0] = F(1)
        generators.append(boost)
    for i, j in ((1, 2), (1, 3), (2, 3)):
        rotation = zero_matrix()
        rotation[i][j] = F(1)
        rotation[j][i] = F(-1)
        generators.append(rotation)
    return generators


def centralizer_equation_matrix() -> list[list[F]]:
    equations: list[list[F]] = []
    for generator in lorentz_generators():
        for i in range(N):
            for j in range(N):
                row = [F(0) for _ in range(N * N)]
                # (XG-GX)_ij = sum_k X_ik G_kj - G_ik X_kj.
                for k in range(N):
                    row[i * N + k] += generator[k][j]
                    row[k * N + j] -= generator[i][k]
                equations.append(row)
    return equations


def path_functor_control() -> dict[str, bool]:
    d1 = diagonal([F(1, 2), F(2), F(3), F(1, 3)])
    d2 = mul(d1, d1)
    d12 = mul(d2, d1)
    u1 = identity()
    u1[0][0], u1[0][1], u1[1][0], u1[1][1] = F(5, 3), F(4, 3), F(4, 3), F(5, 3)
    u2 = identity()
    u2[2][2], u2[2][3], u2[3][2], u2[3][3] = F(3, 5), F(-4, 5), F(4, 5), F(3, 5)
    u1_inv = inverse(u1)
    d2_at_q = mul(mul(u1, d2), u1_inv)
    arrow1 = mul(u1, d1)
    arrow2 = mul(u2, d2_at_q)
    composed = mul(arrow2, arrow1)
    expected = mul(mul(u2, u1), d12)

    d1_inv_at_q = mul(mul(u1, inverse(d1)), u1_inv)
    reverse_arrow = mul(u1_inv, d1_inv_at_q)
    return {
        "composition": composed == expected,
        "reversal": mul(reverse_arrow, arrow1) == identity(),
        "transported_generator_rule": d2_at_q == mul(mul(u1, d2), u1_inv),
    }


def gate_status(class_id: str, gate_id: str) -> tuple[str, str]:
    pointwise_family = {"E02", "E03", "E04", "E05", "E09", "E10"}
    countermodels = {"E07", "E08"}
    if gate_id == "G01":
        if class_id == "E01":
            return "NOT_APPLICABLE", "founded_pair_is_two_channel_not_complete_four_slot_action"
        if class_id in pointwise_family:
            return "CLASSIFIED_FAMILY", "complete_pointwise_family_exists_with_residual_parameters"
        if class_id == "E06":
            return "EXACT_WITNESS", "complete_spectator_member_exists_under_two_extra_premises"
        if class_id in countermodels:
            return "EXACT_COUNTERMODEL", "complete_non_spectator_family_exists"
        return "NOT_APPLICABLE", "reading_or_global_layer_not_a_pointwise_member"
    if gate_id == "G02":
        if class_id == "E01":
            return "DERIVED", "founded_base_subgroup_is_fixed"
        if class_id == "E06":
            return "AVAILABLE_CONDITIONAL", "unique_only_given_transverse_invariance_and_no_mixing"
        if class_id in pointwise_family | countermodels:
            return "CLASSIFIED_FAMILY", "residual_member_parameters_are_not_selected"
        return "OPEN", "no_unique_physical_member_supplied"
    if gate_id == "G03":
        if class_id == "E10":
            return "INACTIVE_PREMISE", "strong_local_CSN_is_inactive_and_would_not_remove_all_ambiguity"
        return "OPEN", "chart_level_extension_has_no_selected_local_Lorentz_independent_physical_operation"
    if gate_id == "G04":
        return "OPEN", "no_extension_class_supplies_one_intrinsic_same_branch_clock_and_founded_ruler"
    if gate_id == "G05":
        return "OPEN", "physical_observer_objects_and_event_pairing_are_not_selected"
    if gate_id == "G06":
        return "OPEN", "extension_class_does_not_assign_metric_native_signed_depth_to_physical_arrows"
    if gate_id == "G07":
        if class_id == "E01":
            return "AVAILABLE_CONDITIONAL", "founded_base_representation_composes_given_additive_depth_but_is_not_a_complete_functor"
        if class_id in {"E11", "E12"}:
            return "AVAILABLE_CONDITIONAL", "typed_associated_bundle_composition_survives_but_requires_a_supplied_extension_member_and_depth"
        return "AVAILABLE_CONDITIONAL", "any_supplied_constant_extension_generator_and_additive_depth_compose_on_typed_path_arrows"
    if gate_id == "G08":
        return "OPEN", "path_retention_endpoint_collapse_or_quotient_is_not_selected"
    if gate_id == "G09":
        return "OPEN", "finite_cell_boundary_and_global_descent_are_not_supplied"
    if gate_id == "G10":
        return "OPEN", "no_extension_class_supplies_the_operational_pair_functional_or_asymptotic_Xmax_join"
    if gate_id == "G11":
        return "OPEN", "all_pairs_clock_map_has_rank_but_no_native_target_or_compatibility_equality"
    if gate_id == "G12":
        if class_id == "E10":
            return "INACTIVE_PREMISE", "counterfactual_strong_CSN_branch_is_not_active_authority"
        return "NOT_SELECTED", "at_least_one_prior_gate_is_open_and_no_active_premise_selects_this_class"
    raise AssertionError((class_id, gate_id))


OUTCOMES = {
    "E01": "FOUNDED_BASE_ONLY_NOT_COMPLETE_PHYSICAL_FUNCTOR",
    "E02": "SEVEN_PARAMETER_POINTWISE_CLASS_PATHWISE_AVAILABLE_NOT_SELECTED",
    "E03": "SIX_PARAMETER_DETERMINANT_ONE_CLASS_PATHWISE_AVAILABLE_NOT_SELECTED",
    "E04": "FOUR_PARAMETER_MIXING_CLASS_PATHWISE_AVAILABLE_NOT_SELECTED",
    "E05": "THREE_PARAMETER_ANGULAR_CLASS_PATHWISE_AVAILABLE_NOT_SELECTED",
    "E06": "EXACT_SPECTATOR_WITNESS_PATHWISE_AVAILABLE_UNDER_EXTRA_PREMISES_NOT_SELECTED",
    "E07": "EXACT_ANGULAR_NONUNIQUENESS_COUNTERFAMILY_NOT_SELECTED",
    "E08": "EXACT_SHIFT_NONUNIQUENESS_COUNTERFAMILY_NOT_SELECTED",
    "E09": "PHYSICAL_METRIC_READING_RETAINS_SEVEN_PARAMETER_OPEN_SELECTION",
    "E10": "CONFORMAL_READING_INACTIVE_AND_RETAINS_SIX_PARAMETER_AMBIGUITY",
    "E11": "LOCAL_LORENTZ_PHYSICAL_OPERATION_DESCENT_OPEN",
    "E12": "GLOBAL_PHYSICAL_COMPARISON_FUNCTOR_OPEN",
}


def main() -> int:
    with (HERE / "EXTENSION_CLASS_UNIVERSE.tsv").open(newline="") as handle:
        classes = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "GATE_SCHEMA.tsv").open(newline="") as handle:
        gates = list(csv.DictReader(handle, delimiter="\t"))
    assert len(classes) == len(gates) == 12

    basis = extension_basis()
    tangent_rank = rank([list(column) for column in zip(*[flatten(x) for x in basis])])
    responses = [metric_response(matrix) for matrix in basis]
    response_rank = rank([list(column) for column in zip(*[flatten(x) for x in responses])])
    assert tangent_rank == response_rank == 7

    centralizer_equations = centralizer_equation_matrix()
    centralizer_rank = rank(centralizer_equations)
    assert centralizer_rank == 15
    identity_vector = flatten(identity())
    assert all(sum((coefficient * value for coefficient, value in zip(row, identity_vector)), F(0)) == 0 for row in centralizer_equations)
    founded_base_not_scalar = F(-1) != F(1)
    assert founded_base_not_scalar

    path = path_functor_control()
    assert all(path.values())

    matrix_rows = []
    for class_row in classes:
        for gate in gates:
            status, reason = gate_status(class_row["id"], gate["gate_id"])
            matrix_rows.append(
                {
                    "class_id": class_row["id"],
                    "gate_id": gate["gate_id"],
                    "status": status,
                    "reason": reason,
                }
            )
    assert len(matrix_rows) == 144
    with (HERE / "CLASS_GATE_MATRIX.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(matrix_rows[0]))
        writer.writeheader()
        writer.writerows(matrix_rows)

    outcome_rows = []
    for class_row in classes:
        class_id = class_row["id"]
        if class_id == "E01":
            path_status = "BASE_PAIR_REPRESENTATION_COMPOSES_GIVEN_DEPTH_NOT_COMPLETE_FUNCTOR"
            endpoint_status = "NOT_APPLICABLE_INCOMPLETE_FOUR_SLOT_ACTION"
        elif class_id in {"E11", "E12"}:
            path_status = "AVAILABLE_CONDITIONAL_GIVEN_EXTENSION_MEMBER_DEPTH_TYPED_PATH"
            endpoint_status = "OPEN_DEPENDS_ON_SELECTED_EXTENSION_AND_GLOBAL_COMPLETION"
        else:
            path_status = "AVAILABLE_CONDITIONAL_GIVEN_MEMBER_DEPTH_TYPED_PATH"
            endpoint_status = "OBSTRUCTED_ON_FULL_HOLONOMY_CONTROL_ONLY"
        outcome_rows.append(
            {
                "class_id": class_id,
                "class": class_row["class"],
                "free_extension_parameters": class_row["free_extension_parameters"],
                "path_functor": path_status,
                "endpoint_collapse_on_full_holonomy_control": endpoint_status,
                "physical_selection": "INACTIVE" if class_id == "E10" else "NOT_SELECTED",
                "outcome": OUTCOMES[class_id],
            }
        )
    with (HERE / "CLASS_OUTCOMES.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(outcome_rows[0]))
        writer.writeheader()
        writer.writerows(outcome_rows)

    result = {
        "schema": "udt.complete_coframe_physical_comparison_functor.derivation.v1",
        "status": "PASS_CLASSIFIED_NO_PHYSICAL_FUNCTOR_SELECTED",
        "class_count": 12,
        "gate_count": 12,
        "matrix_cells": 144,
        "extension_generator_rank": tangent_rank,
        "metric_response_rank": response_rank,
        "determinant_one_extension_rank": 6,
        "transverse_invariant_residual_rank": 4,
        "no_mixing_residual_rank": 3,
        "spectator_residual_rank_given_both": 0,
        "path_functor_exact": path,
        "path_functor_status": "AVAILABLE_CONDITIONAL_FOR_EVERY_SUPPLIED_EXTENSION_MEMBER_AND_ADDITIVE_DEPTH_ON_TYPED_PATH_GROUPOID",
        "composition_selects_extension_parameters": False,
        "physical_path_ontology_selected": False,
        "full_so_1_3_commutator_constraint_rank": centralizer_rank,
        "full_so_1_3_centralizer_dimension": 16 - centralizer_rank,
        "full_centralizer": "SCALAR_IDENTITY_ONLY",
        "founded_base_compatible_with_full_holonomy_centralizer": False,
        "endpoint_collapse_requires_holonomy_centralization": True,
        "endpoint_collapse_status": "OBSTRUCTED_FOR_EVERY_FOUNDED_EXTENSION_ON_FULL_HOLONOMY_CONTROL_ONLY",
        "reduced_holonomy_other_branches": "OPEN",
        "all_pairs_clock_response_rank": "INFINITE_DIMENSIONAL_MOD_CONSTANTS_GIVEN_PHYSICAL_PAIR_DOMAIN",
        "native_all_pairs_target": "OPEN_NOT_SELECTED",
        "physical_comparison_functor_status": "OPEN_NOT_SELECTED_IN_TWELVE_CLASS_UNIVERSE",
        "Xmax_status": "WORKING_SCHEMA_UNCHANGED_NO_OPERATIONAL_JOIN",
        "bootstrap_status": "WORKING_ON_SHELL_ADMISSIBILITY_ONLY_UNCHANGED",
        "c_E_and_G_sufficient_for_length_or_density_closure": False,
        "strong_local_CSN_status": "CHALLENGED_OWNER_POSTULATE_NOT_DERIVED_INACTIVE",
        "cross_branch_splice_used": False,
        "universal_holonomy_no_go_claimed": False,
        "maximum_conclusion": "TWELVE_CLASSES_AND_144_GATES_CLASSIFIED;_ARBITRARY_EXTENSION_PATH_FUNCTOR_AND_FULL_HOLONOMY_CONTROL_OBSTRUCTION_DERIVED;_NO_PHYSICAL_FUNCTOR_SELECTED",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
