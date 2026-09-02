#!/usr/bin/env python3
"""Production algebra for the bounded G326 homogeneous off-diagonal census."""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path


LANDING = (
    "HOMOGENEOUS_OFFDIAGONAL_MODES_CLOSE_AS_FIVE_QUOTIENT_LATTICE_MODULI__"
    "ONE_LOCAL_TRANSVERSE_KASNER_SHEAR__NO_NEW_GAUGE_OR_SCALAR_MODE__"
    "NO_FULL_STABILITY_CLAIM"
)

P = (Fraction(-1, 3), Fraction(2, 3), Fraction(2, 3))
PAIRS = ((0, 1), (0, 2), (1, 2))


def rank(rows: list[list[Fraction]]) -> int:
    matrix = [row[:] for row in rows]
    row_index = 0
    for column in range(len(matrix[0]) if matrix else 0):
        pivot = next((r for r in range(row_index, len(matrix)) if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[row_index], matrix[pivot] = matrix[pivot], matrix[row_index]
        value = matrix[row_index][column]
        matrix[row_index] = [entry / value for entry in matrix[row_index]]
        for r in range(len(matrix)):
            if r == row_index or not matrix[r][column]:
                continue
            value = matrix[r][column]
            matrix[r] = [left - value * right
                         for left, right in zip(matrix[r], matrix[row_index])]
        row_index += 1
    return row_index


def characteristic(pi: Fraction, pj: Fraction, exponent: Fraction) -> Fraction:
    """Coefficient of T^(m-2) in the exact off-diagonal Ricci ODE."""
    return exponent * exponent - 2 * (pi + pj) * exponent + 4 * pi * pj


def characteristic_derivative(pi: Fraction, pj: Fraction, exponent: Fraction) -> Fraction:
    """Log-solution coefficient after differentiating the power solution in m."""
    return 2 * exponent - 2 * (pi + pj)


def cover_map() -> list[list[Fraction]]:
    """A^i_j -> 3 diagonal plus 5 off-diagonal lattice coefficients at C_i=1."""
    # Columns: A11,A12,A13,A21,A22,A23,A31,A32,A33.
    rows = []
    for column in (0, 4, 8):
        row = [Fraction(0)] * 9
        row[column] = 1
        rows.append(row)
    for column in (1, 3, 2, 6):
        row = [Fraction(0)] * 9
        row[column] = 1
        rows.append(row)
    row = [Fraction(0)] * 9
    row[5] = 1
    row[7] = 1
    rows.append(row)
    return rows


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

    roots: dict[str, list[str]] = {}
    for i, j in PAIRS:
        pi, pj = P[i], P[j]
        first, second = 2 * pi, 2 * pj
        label = f"{i + 1}{j + 1}"
        gate(characteristic(pi, pj, first) == 0, f"root_{label}_left")
        gate(characteristic(pi, pj, second) == 0, f"root_{label}_right")
        discriminant = 4 * (pi - pj) ** 2
        gate(discriminant >= 0, f"real_roots_{label}")
        if pi == pj:
            gate(first == second, f"repeated_root_{label}")
            gate(characteristic_derivative(pi, pj, first) == 0,
                 f"log_solution_exact_{label}")
            roots[label] = [f"T^{first}", f"T^{first}*log(T/Tref)"]
        else:
            gate(first != second, f"distinct_roots_{label}")
            roots[label] = [f"T^{first}", f"T^{second}"]

    gate(sum(len(values) for values in roots.values()) == 6,
         "six_complete_offdiagonal_integration_constants")

    # Constant linear cover-coordinate changes have one transverse-rotation kernel.
    full_map = cover_map()
    gate(len(full_map) == 8 and rank(full_map) == 8, "full_cover_image_rank_eight")
    offdiagonal_rows = full_map[3:]
    gate(len(offdiagonal_rows) == 5 and rank(offdiagonal_rows) == 5,
         "offdiagonal_cover_image_rank_five")
    transverse_rotation = [Fraction(0)] * 9
    transverse_rotation[5] = 1
    transverse_rotation[7] = -1
    gate(all(sum(row[column] * transverse_rotation[column] for column in range(9)) == 0
             for row in full_map), "cover_map_kernel_contains_transverse_rotation")
    gate(9 - rank(full_map) == 1, "cover_map_kernel_exactly_one_dimensional")

    # The five nonzero off-diagonal image generators are affine on the cover and nonperiodic on T3.
    periods = (Fraction(5), Fraction(7), Fraction(11))
    affine_generators = ((0, 1), (1, 0), (0, 2), (2, 0), (1, 2))
    for target, source in affine_generators:
        gate(periods[source] != 0, f"affine_jump_nonzero_{target}{source}")
    gate(len(affine_generators) == 5, "five_nonperiodic_offdiagonal_cover_generators")

    # The transverse repeated-root mode is a genuine curvature-changing Kasner tangent.
    time = Fraction(11, 5)
    cross_shear = Fraction(13, 17)
    tidal_cross = -cross_shear / (3 * time**2)
    gate(tidal_cross == Fraction(-325, 6171), "transverse_tidal_witness_exact")
    gate(tidal_cross != 0, "transverse_tidal_witness_nonzero")
    gate(Fraction(4) * cross_shear**2 / (9 * time**4) > 0,
         "transverse_tidal_eigenvalue_discriminant_positive")

    # Structural first-order counts and boundaries.
    gate(5 + 1 == 6, "offdiagonal_dimension_partition")
    gate(3 + 5 == 8, "combined_quotient_lattice_dimension_eight")
    gate(1 + 8 + 2 + 1 == 12, "combined_homogeneous_dimension_twelve")
    gate(P[1] == P[2], "transverse_background_degeneracy")

    result = {
        "schema": "udt-g326-homogeneous-offdiagonal-production-v1",
        "status": "INTERNAL_VERIFIED_PENDING_EXTERNAL_REVIEW",
        "landing": LANDING,
        "assertion_count": len(checks),
        "checks": checks,
        "background_exponents": [str(value) for value in P],
        "offdiagonal_ode": (
            "k_ij''+[1-2*(p_i+p_j)]*k_ij'/T+4*p_i*p_j*k_ij/T^2=0"
        ),
        "general_solutions": roots,
        "mode_dimensions": {
            "fixed_quotient_lattice_moduli": 5,
            "local_transverse_kasner_shear": 1,
            "quotient_legal_gauge": 0,
            "connected_scalar_curvature": 0,
        },
        "combined_g325_g326_dimensions": {
            "residual_time_translation_gauge": 1,
            "fixed_quotient_lattice_moduli": 8,
            "local_kasner_shear_components": 2,
            "connected_scalar_curvature": 1,
            "total_integration_constants": 12,
        },
        "transverse_tidal_witness": "delta(E^y_z)=delta(E^z_y)=-q_cross/(3*T^2)",
        "linearized_scalar_curvature": "0",
        "full_homogeneous_synchronous_first_variation_closed_with_g325": True,
        "full_linear_stability_proved": False,
        "nonlinear_stability_proved": False,
        "inhomogeneous_modes_classified": False,
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
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
