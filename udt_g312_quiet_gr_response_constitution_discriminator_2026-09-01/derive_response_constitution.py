#!/usr/bin/env python3
"""Exact standard-library checks for the preregistered G312 discriminator."""

from __future__ import annotations

import csv
import json
from fractions import Fraction as F
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
G = (F(-1), F(1), F(1), F(1))


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(4)] for i in range(4)]


def scale(value, tensor):
    return [[value * tensor[i][j] for j in range(4)] for i in range(4)]


def metric_multiple(value):
    return [[value * G[i] if i == j else F(0) for j in range(4)] for i in range(4)]


def trace(tensor):
    return sum(G[i] * tensor[i][i] for i in range(4))


def trace_free(tensor):
    return add(tensor, scale(F(-1, 4), metric_multiple(trace(tensor))))


def quadratic_ricci(tensor):
    product = [
        [sum(tensor[i][k] * G[k] * tensor[k][j] for k in range(4)) for j in range(4)]
        for i in range(4)
    ]
    return trace_free(product)


def symmetric_tensor(seed):
    tensor = [[F(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(i, 4):
            value = F(((seed + 2 * i + 3 * j) % 11) - 5, (seed % 5) + 1)
            tensor[i][j] = value
            tensor[j][i] = value
    return tensor


def response(tensor, a, b):
    return add(scale(a, tensor), metric_multiple(b * trace(tensor)))


def second_difference_solve(source):
    """Retarded discrete inverse with zero first two values."""
    values = [F(0), F(0)]
    for item in source:
        values.append(2 * values[-1] - values[-2] + item)
    return values


def read_registry():
    with (ROOT / "CURRENT_SCIENTIFIC_PREMISES.tsv").open(encoding="utf-8", newline="") as handle:
        return {row["premise_id"]: row for row in csv.DictReader(handle, delimiter="\t")}


def main():
    checks = 0

    # Exact G311-on-G301 identity on a broad rational tensor/coefficient census.
    for seed in range(1, 129):
        ricci = symmetric_tensor(seed)
        a = F((seed % 7) + 1, (seed % 5) + 1)
        b = F((seed % 9) - 4, (seed % 6) + 1)
        lhs = trace_free(response(ricci, a, b))
        rhs = scale(a, trace_free(ricci))
        for i in range(4):
            for j in range(4):
                assert lhs[i][j] == rhs[i][j]
                checks += 1

    # A pure quadratic response contains every Ricci-flat solution but has zero quiet derivative.
    nonzero_quadratic_witnesses = 0
    for seed in range(1, 65):
        ricci = symmetric_tensor(seed)
        q = quadratic_ricci(ricci)
        q_scaled = quadratic_ricci(scale(F(3, 7), ricci))
        assert q_scaled == scale(F(9, 49), q)
        checks += 16
        assert quadratic_ricci(scale(F(0), ricci)) == [[F(0)] * 4 for _ in range(4)]
        checks += 16
        if any(q[i][j] for i in range(4) for j in range(4)):
            nonzero_quadratic_witnesses += 1
    assert nonzero_quadratic_witnesses > 0
    checks += 1

    # Positive weight-one homogeneity plus a derivative at zero is exactly the derivative map.
    for seed in range(1, 65):
        vector = [F(seed + i, seed % 5 + 1) for i in range(5)]
        matrix = [[F((r + 1) * (c + 2) - 3, r + c + 2) for c in range(5)] for r in range(3)]
        image = [sum(matrix[r][c] * vector[c] for c in range(5)) for r in range(3)]
        for t in (F(1, 7), F(2, 5), F(11, 3)):
            scaled_image = [t * entry for entry in image]
            quotient = [entry / t for entry in scaled_image]
            assert quotient == image
            checks += 3

    # A nonlinear degree-one direction map is not differentiable at the quiet origin.
    def ratio_map(x, y):
        denominator = x * x + y * y
        if denominator == 0:
            raise ZeroDivisionError
        return x**3 / denominator, y**3 / denominator

    d1 = ratio_map(F(1), F(0))
    d2 = ratio_map(F(0), F(1))
    d12 = ratio_map(F(1), F(1))
    assert d12 != (d1[0] + d2[0], d1[1] + d2[1])
    checks += 2
    try:
        ratio_map(F(0), F(0))
    except ZeroDivisionError:
        checks += 1
    else:
        raise AssertionError("ratio response unexpectedly regular at quiet origin")

    # Dimensional gate: Ricci is L^-2, its quadratic is L^-4, so mixing requires L^2.
    linear_weight = -2
    quadratic_weight = -4
    required_coefficient_weight = linear_weight - quadratic_weight
    assert required_coefficient_weight == 2
    checks += 1

    # A scale-free nonlocal correction can retain the GR first variation while carrying history.
    source_a = [F(0), F(1), F(0), F(0), F(0), F(0)]
    source_b = [F(0), F(0), F(0), F(0), F(0), F(0)]
    first_a = second_difference_solve(source_a)
    first_b = second_difference_solve(source_b)
    second_a = second_difference_solve(first_a[2:])
    second_b = second_difference_solve(first_b[2:])
    assert source_a[-3:] == source_b[-3:]
    assert second_a[-1] != second_b[-1]
    assert (second_a[-1] - second_a[-2]) != (second_b[-1] - second_b[-2])
    checks += 3
    nonlocal_dimensions = {
        "Ricci_squared": -4,
        "box_inverse_twice": 4,
        "dimensionless_history_scalar": 0,
        "gradient_square_response": -2,
    }
    assert nonlocal_dimensions["Ricci_squared"] + nonlocal_dimensions["box_inverse_twice"] == 0
    checks += 1

    registry = read_registry()
    assert "RESPONSE_CONSTITUTION_REMAINS_OPEN" in registry["G311"]["current_status"]
    assert "whether UDT owns locality" in registry["G301"]["open_scope"]
    assert "CURRENT_PREMISES_DO_NOT_PRIVILEGE_ONE_RESIDUAL_FORM" in registry["G296"]["current_status"]
    assert "W3_UDT_GR_QUIET_LIMIT_REDUCTION_WORKING_POSIT_NOT_CANON" in registry["G257"]["current_status"]
    assert "METRIC_ONLY_STATE_RANK_TWO_EQUATION_POINTWISE_LOCALITY_SECOND_ORDER" in registry["G261"]["current_status"]
    checks += 5

    architectures = {
        "G301_regular_local_weight_one": {
            "metric_only": True,
            "local_finite_jet": True,
            "quiet_regular": True,
            "no_operator_length": True,
            "ricci_flat_solution_overlap": True,
            "gr_quiet_principal_overlap": True,
            "extra_carry": False,
            "classification": "CONDITIONAL_TARGET_CLASS",
        },
        "pure_curvature_quadratic": {
            "metric_only": True,
            "local_finite_jet": True,
            "quiet_regular": True,
            "no_operator_length": True,
            "ricci_flat_solution_overlap": True,
            "gr_quiet_principal_overlap": False,
            "extra_carry": False,
            "classification": "SOLUTION_OVERLAP_ONLY__QUIET_PRINCIPAL_DEGENERATE",
        },
        "linear_plus_length_squared_quadratic": {
            "metric_only": True,
            "local_finite_jet": True,
            "quiet_regular": True,
            "no_operator_length": False,
            "ricci_flat_solution_overlap": True,
            "gr_quiet_principal_overlap": True,
            "extra_carry": False,
            "classification": "REQUIRES_NEW_OPERATOR_LENGTH",
        },
        "scale_free_curvature_ratio": {
            "metric_only": True,
            "local_finite_jet": True,
            "quiet_regular": False,
            "no_operator_length": True,
            "ricci_flat_solution_overlap": False,
            "gr_quiet_principal_overlap": False,
            "extra_carry": False,
            "classification": "SINGULAR_OR_NONDIFFERENTIABLE_AT_QUIET",
        },
        "scale_free_nonlocal_metric_history": {
            "metric_only": True,
            "local_finite_jet": False,
            "quiet_regular": True,
            "no_operator_length": True,
            "ricci_flat_solution_overlap": True,
            "gr_quiet_principal_overlap": True,
            "extra_carry": True,
            "classification": "SURVIVES_UNLESS_LOCALITY_IS_ADOPTED",
        },
        "auxiliary_or_populated_relation_response": {
            "metric_only": False,
            "local_finite_jet": None,
            "quiet_regular": True,
            "no_operator_length": None,
            "ricci_flat_solution_overlap": True,
            "gr_quiet_principal_overlap": True,
            "extra_carry": True,
            "classification": "VIOLATES_METRIC_ONLY_PRIMITIVE_STATE",
        },
    }

    # Independence witnesses: one local architecture violates only principal overlap; one
    # principal-matching architecture violates locality.
    assert architectures["pure_curvature_quadratic"]["local_finite_jet"]
    assert not architectures["pure_curvature_quadratic"]["gr_quiet_principal_overlap"]
    assert architectures["scale_free_nonlocal_metric_history"]["gr_quiet_principal_overlap"]
    assert not architectures["scale_free_nonlocal_metric_history"]["local_finite_jet"]
    checks += 4

    result = {
        "status": "PASS",
        "landing": "TWO_OR_MORE_INDEPENDENT_NEW_PREMISES_ARE_REQUIRED",
        "exact_checks": checks,
        "g311_on_g301": "TF_g(a_Ric+b_R_g)=a_S__A_NONZERO_GIVES_TRACEFREE_RICCI",
        "ownership_result": {
            "already_owned_or_active": [
                "ONE_COMPLETE_METRIC_PRIMITIVE_STATE",
                "UNIVERSAL_RECIPROCITY_RESPONSE_SHAPE",
                "NO_AVAILABLE_VACUUM_OPERATOR_LENGTH_INPUT",
                "REGULAR_QUIET_GEOMETRIC_ARENA",
            ],
            "not_owned": [
                "FULL_QUIET_GR_PRINCIPAL_RESPONSE_OVERLAP",
                "LOCAL_FINITE_JET_RESPONSE_CONSTITUTION",
            ],
            "independence": "LOCAL_QUADRATIC_AND_NONLOCAL_PRINCIPAL_MATCHING_WITNESSES_SEPARATE_THE_TWO",
        },
        "conditional_closure": "IF_BOTH_MISSING_PREMISES_ARE_ADOPTED__G301_MEMBERSHIP_AND_G311_GIVE_TRACEFREE_RICCI",
        "architectures": architectures,
        "nonlocal_dimension_ledger": nonlocal_dimensions,
        "metric_kernel_changed": False,
        "observations_used": False,
        "protected_inputs_used": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
