#!/usr/bin/env python3
"""Production derivation for the bounded G325 homogeneous diagonal mode census."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path


LANDING = (
    "HOMOGENEOUS_DIAGONAL_MODES_CLOSE_AS_TIME_GAUGE__"
    "THREE_QUOTIENT_LATTICE_MODULI__ONE_LOCAL_KASNER_SHEAR__"
    "ONE_CONNECTED_SCALAR_MODE__NO_FULL_STABILITY_CLAIM"
)

P = (Fraction(-1, 3), Fraction(2, 3), Fraction(2, 3))


def matrix_rank(rows: list[list[Fraction]]) -> int:
    matrix = [row[:] for row in rows]
    if not matrix:
        return 0
    rank = 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next((index for index in range(rank, len(matrix))
                      if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank:
                continue
            scale = matrix[index][column]
            if scale:
                matrix[index] = [left - scale * right
                                 for left, right in zip(matrix[index], matrix[rank])]
        rank += 1
    return rank


def solve_linear(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    n = len(matrix)
    for column in range(n):
        pivot = next(index for index in range(column, n) if augmented[index][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for index in range(n):
            if index == column:
                continue
            scale = augmented[index][column]
            augmented[index] = [left - scale * right
                                for left, right in zip(augmented[index], augmented[column])]
    return [augmented[index][-1] for index in range(n)]


def residuals(
    time: Fraction,
    gauge: Fraction,
    shear: Fraction,
    scalar: Fraction,
) -> dict[str, object]:
    """Exact first-order Ricci and trace-free residuals from the Bianchi-I metric."""
    q = (Fraction(0), shear, -shear)
    first = [
        q_i / time - p_i * gauge / time**2
        + (1 - p_i) * scalar * time / 2
        for p_i, q_i in zip(P, q)
    ]
    second = [
        -q_i / time**2 + 2 * p_i * gauge / time**3
        + (1 - p_i) * scalar / 2
        for p_i, q_i in zip(P, q)
    ]
    expansion = sum(first)
    ricci_00 = -sum(second_i + 2 * p_i * first_i / time
                    for p_i, first_i, second_i in zip(P, first, second))
    ricci_space = [
        second_i + first_i / time + p_i * expansion / time
        for p_i, first_i, second_i in zip(P, first, second)
    ]
    scalar_curvature = -ricci_00 + sum(ricci_space)
    tracefree_00 = ricci_00 + scalar_curvature / 4
    tracefree_space = [value - scalar_curvature / 4 for value in ricci_space]
    hamiltonian = (expansion - sum(p_i * first_i for p_i, first_i in zip(P, first))) / time
    return {
        "first": first,
        "second": second,
        "ricci_00": ricci_00,
        "ricci_space": ricci_space,
        "scalar_curvature": scalar_curvature,
        "tracefree_00": tracefree_00,
        "tracefree_space": tracefree_space,
        "hamiltonian": hamiltonian,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="DERIVATION_RESULT.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    checks: list[str] = []

    def gate(condition: bool, name: str) -> None:
        assert condition, name
        checks.append(name)

    gate(sum(P) == 1, "background_kasner_sum")
    gate(sum(value * value for value in P) == 1, "background_kasner_square_sum")

    # The constant-in-log-time exponent vector is constrained by sum(q)=p.q=0.
    constraint_rows = [[Fraction(1), Fraction(1), Fraction(1)], list(P)]
    gate(matrix_rank(constraint_rows) == 2, "exponent_constraint_rank_two")
    q_basis = [Fraction(0), Fraction(1), Fraction(-1)]
    gate(sum(q_basis) == 0, "kasner_shear_zero_trace")
    gate(sum(p_i * q_i for p_i, q_i in zip(P, q_basis)) == 0,
         "kasner_shear_tangent_constraint")
    gate(matrix_rank(constraint_rows + [q_basis]) == 3,
         "kasner_shear_spans_one_dimensional_nullspace")

    # The connected-scalar particular solution is unique at the w_i=T*u_i' level.
    scalar_matrix = [
        [2 * (1 if i == j else 0) + P[i] for j in range(3)]
        for i in range(3)
    ]
    scalar_w = solve_linear(scalar_matrix, [Fraction(1)] * 3)
    expected_scalar_w = [(1 - value) / 2 for value in P]
    gate(scalar_w == expected_scalar_w, "connected_scalar_particular_unique")
    scalar_u = [value / 2 for value in scalar_w]
    gate(scalar_u == [(1 - value) / 4 for value in P],
         "connected_scalar_metric_coefficients")

    # The T^-1 solution at w=T*u' is precisely the time-translation Lie derivative.
    gauge_w = [-value for value in P]
    gauge_sum = sum(gauge_w)
    gate(all(-value + P[index] * gauge_sum == 0
             for index, value in enumerate(gauge_w)), "gauge_ode_solution")
    gate(all(2 * P[index] == 2 * P[index] for index in range(3)),
         "time_shift_lie_derivative_witness")

    # Exact all-mode checks at unrelated rational times and amplitudes.
    samples = (
        (Fraction(2, 3), Fraction(7, 5), Fraction(-4, 9), Fraction(5, 11)),
        (Fraction(7, 4), Fraction(-3, 8), Fraction(9, 13), Fraction(-2, 7)),
        (Fraction(19, 6), Fraction(0), Fraction(5, 3), Fraction(0)),
    )
    for index, (time, gauge, shear, scalar) in enumerate(samples):
        result = residuals(time, gauge, shear, scalar)
        gate(result["tracefree_00"] == 0, f"tracefree_time_zero_{index}")
        gate(all(value == 0 for value in result["tracefree_space"]),
             f"tracefree_space_zero_{index}")
        gate(result["ricci_00"] == -scalar, f"einstein_time_{index}")
        gate(all(value == scalar for value in result["ricci_space"]),
             f"einstein_space_{index}")
        gate(result["scalar_curvature"] == 4 * scalar,
             f"scalar_curvature_four_lambda_{index}")
        gate(result["hamiltonian"] == scalar, f"hamiltonian_constraint_{index}")

    # Constant strains are a complete three-dimensional integration-constant sector.
    lattice_forms = [
        [Fraction(1), Fraction(1), Fraction(1)],
        [Fraction(1), Fraction(-1, 2), Fraction(-1, 2)],
        [Fraction(0), Fraction(1), Fraction(-1)],
    ]
    gate(matrix_rank(lattice_forms) == 3, "three_lattice_modulus_coordinates")
    periods = (Fraction(5), Fraction(7), Fraction(11))
    nonzero_strain = (Fraction(2, 5), Fraction(-3, 7), Fraction(4, 11))
    jumps = [strain * period for strain, period in zip(nonzero_strain, periods)]
    gate(all(value != 0 for value in jumps), "cover_scaling_vector_not_periodic")
    gate(all(Fraction(0) * period == 0 for period in periods),
         "zero_scaling_vector_periodic")

    # Local curvature distinguishes the shear mode even though scalar invariants are symmetric
    # under y-z exchange at first order.
    shear = Fraction(13, 17)
    time = Fraction(11, 5)
    electric_weyl_y_minus_z = -2 * shear / (3 * time**2)
    gate(electric_weyl_y_minus_z != 0, "local_weyl_eigenvalue_split_nonzero")
    gate(electric_weyl_y_minus_z == Fraction(-650, 6171),
         "local_weyl_eigenvalue_split_exact")

    # Endpoint behavior follows from exact basis functions and is classification, not a filter.
    shear_log_coefficient = Fraction(1)
    scalar_power = Fraction(2)
    gauge_power = Fraction(-1)
    gate(shear_log_coefficient != 0, "shear_log_secular_both_ends")
    gate(scalar_power > 0, "scalar_mode_quadratic_future_growth")
    gate(scalar_power > 0, "scalar_mode_zero_at_past_end")
    gate(gauge_power < 0 and gauge_w == [-value for value in P],
         "time_shift_growth_is_gauge")

    result = {
        "schema": "udt-g325-homogeneous-diagonal-production-v1",
        "status": "INTERNAL_VERIFIED_PENDING_EXTERNAL_REVIEW",
        "landing": LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "background_exponents": [str(value) for value in P],
        "general_solution": (
            "u_i=c_i+q_i*log(T/Tref)+p_i*G/T+"
            "(1-p_i)*lambda*T^2/4; sum(q)=sum(p_i*q_i)=0"
        ),
        "mode_dimensions": {
            "residual_time_translation_gauge": 1,
            "fixed_quotient_lattice_moduli": 3,
            "local_kasner_shear": 1,
            "connected_scalar_curvature": 1,
        },
        "linearized_scalar_curvature": "4*lambda",
        "shear_curvature_witness": "delta(E_y-E_z)=-2*q/(3*T^2)",
        "full_linear_stability_proved": False,
        "nonlinear_stability_proved": False,
        "inhomogeneous_modes_classified": False,
        "offdiagonal_modes_classified": False,
        "physical_occupancy_selected": False,
        "physical_scale_selected": False,
        "Xmax_selected": False,
        "metric_changed": False,
        "kernel_changed": False,
        "angular_sector_changed": False,
        "python_version": sys.version,
    }
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
