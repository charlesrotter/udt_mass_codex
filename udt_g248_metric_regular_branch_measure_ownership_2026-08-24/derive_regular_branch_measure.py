#!/usr/bin/env python3
"""Exact production checks for the G248 regular branch-measure classification."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import sympy as sp


LANDING = (
    "METRIC_OWNS_ORDERED_REGULAR_INCIDENCE_COAREA_DENSITY_R_OVER_A"
    "__SKY_PHASE_COUNTING_AND_INCIDENCE_MEASURES_ARE_DISTINCT_TYPED_OBJECTS"
    "__CSP4_COMPOSITION_LEAVES_REAL_CHARACTER_FAMILY_R_TO_ALPHA"
    "__UNIVERSAL_PHYSICAL_BRANCH_MEASURE_SOURCE_POPULATION_AND_CRITICAL_COMPLETION_REMAIN_OPEN"
)


def block2(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix, d: sp.Matrix) -> sp.Matrix:
    return a.row_join(b).col_join(c.row_join(d))


def random_symmetric(rng: random.Random) -> sp.Matrix:
    while True:
        x = sp.Rational(rng.randint(1, 9), rng.randint(1, 7))
        y = sp.Rational(rng.randint(-5, 5), rng.randint(1, 7))
        z = sp.Rational(rng.randint(1, 9), rng.randint(1, 7))
        matrix = sp.Matrix([[x, y], [y, z]])
        if matrix.det() != 0:
            return matrix


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=4096)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    assertions = 0

    def check(value: bool) -> None:
        nonlocal assertions
        assertions += 1
        if not bool(value):
            raise AssertionError(f"exact check {assertions} failed")

    # Symbolic transverse determinant, including arbitrary null-gauge additions to the Jacobi fields.
    d11, d12, d21, d22, omega, gamma1, gamma2 = sp.symbols(
        "d11 d12 d21 d22 omega gamma1 gamma2", nonzero=True
    )
    u = sp.Matrix([1, 0, 0, 0])
    k = sp.Matrix([omega, 0, 0, omega])
    e1 = sp.Matrix([0, 1, 0, 0])
    e2 = sp.Matrix([0, 0, 1, 0])
    j1 = d11 * e1 + d21 * e2 + gamma1 * k
    j2 = d12 * e1 + d22 * e2 + gamma2 * k
    transverse_det = sp.Matrix.hstack(j1, j2, k, u).det()
    det_d = d11 * d22 - d12 * d21
    check(sp.simplify(transverse_det**2 - omega**2 * det_d**2) == 0)

    eye = sp.eye(2)
    zero = sp.zeros(2)
    omega4 = block2(zero, eye, -eye, zero)
    identity4 = sp.eye(4)
    rng = random.Random(248024)
    unequal_counting_coarea = 0
    three_measure_separations = 0
    reverse_query_density_differences = 0
    noncommuting_phase_cases = 0

    for _ in range(args.cases):
        p = random_symmetric(rng)
        qmat = random_symmetric(rng)
        upper = block2(eye, p, zero, eye)
        lower = block2(eye, zero, qmat, eye)
        symplectic = lower * upper

        scale = sp.Rational(rng.randint(1, 9), rng.randint(1, 7))
        multiplier = scale**2
        phase = scale * symplectic

        symplectic_residual = symplectic.T * omega4 * symplectic - omega4
        conformal_residual = phase.T * omega4 * phase - multiplier * omega4
        for entry in symplectic_residual:
            check(entry == 0)
        for entry in conformal_residual:
            check(entry == 0)
        check(sp.factor(phase.det() - multiplier**2) == 0)

        inverse_formula = sp.Rational(1, 1) / multiplier * block2(
            phase[2:4, 2:4].T,
            -phase[0:2, 2:4].T,
            -phase[2:4, 0:2].T,
            phase[0:2, 0:2].T,
        )
        for entry in phase * inverse_formula - identity4:
            check(entry == 0)

        # G226 block B, denoted the Jacobi screen map mathcal-D in G244.
        jacobi_position = phase[0:2, 2:4]
        inverse_position = inverse_formula[0:2, 2:4]
        for entry in inverse_position + jacobi_position.T / multiplier:
            check(entry == 0)
        area = abs(jacobi_position.det())
        inverse_area = abs(inverse_position.det())
        check(area > 0)
        check(sp.factor(inverse_area - area / multiplier**2) == 0)

        coarea_weight = multiplier / area
        inverse_coarea_coefficient = (1 / multiplier) / inverse_area
        check(sp.factor(inverse_coarea_coefficient - coarea_weight) == 0)

        # Direct Lorentz-volume evaluation of J=omega_B*A=A/r, with source frequency one.
        target_frequency = 1 / multiplier
        gauge1 = sp.Rational(rng.randint(-5, 5), rng.randint(1, 7))
        gauge2 = sp.Rational(rng.randint(-5, 5), rng.randint(1, 7))
        k_num = sp.Matrix([target_frequency, 0, 0, target_frequency])
        j1_num = jacobi_position[0, 0] * e1 + jacobi_position[1, 0] * e2 + gauge1 * k_num
        j2_num = jacobi_position[0, 1] * e1 + jacobi_position[1, 1] * e2 + gauge2 * k_num
        lorentz_det = sp.Matrix.hstack(j1_num, j2_num, k_num, u).det()
        transverse_jacobian = area / multiplier
        check(sp.factor(lorentz_det**2 - transverse_jacobian**2) == 0)
        check(sp.factor(1 / abs(lorentz_det) - coarea_weight) == 0)

        # Phase volume is a different typed density: pullback r^2, pushforward r^-2.
        check(phase.det() == multiplier**2)
        check((1 / phase.det()) == multiplier**-2)

        scale2 = sp.Rational(rng.randint(1, 9), rng.randint(1, 7))
        multiplier2 = scale2**2
        for alpha in range(-3, 4):
            check((multiplier2 * multiplier) ** alpha == multiplier2**alpha * multiplier**alpha)
            check((1 / multiplier) ** alpha == 1 / (multiplier**alpha))

        # Three metric-natural but differently typed branch weights need not agree.
        counting_weight = sp.Integer(1)
        symmetric_clock_weight = scale  # sqrt(r), exact because r=scale^2 in this census.
        if coarea_weight != counting_weight:
            unequal_counting_coarea += 1
        if len({counting_weight, symmetric_clock_weight, coarea_weight}) == 3:
            three_measure_separations += 1
        # Rebuilding the inverse ordered query gives the same coefficient but a different base clock density.
        if multiplier != 1:
            reverse_query_density_differences += 1

        second_phase = scale2 * upper * lower
        if phase * second_phase != second_phase * phase:
            noncommuting_phase_cases += 1

        # Matched-chain density multiplies on the fiber product; it is not identified with a direct edge.
        area2 = abs((second_phase[0:2, 2:4]).det())
        if area2 != 0:
            weight2 = multiplier2 / area2
            check(coarea_weight * weight2 == (multiplier * multiplier2) / (area * area2))

    check(unequal_counting_coarea > 0)
    check(three_measure_separations > 0)
    check(reverse_query_density_differences > 0)
    check(noncommuting_phase_cases > 0)

    result = {
        "assertions": assertions,
        "cases": args.cases,
        "caustic_boundary": "A=0__REGULAR_COAREA_DENSITY_LEAVES_SCOPE__FULL_PHASE_REMAINS_INVERTIBLE",
        "character_family": "chi_alpha(M)=r(M)^alpha__alpha_in_R__NOT_SELECTED",
        "coarea_density": "dmu_AB=(r_AB/A_AB)*d_tau_A",
        "formal_inverse": "B_inverse=-r^-1*B^T__A_inverse=A/r^2__coarea_coefficient_inverse=r/A",
        "landing": LANDING,
        "measure_types": [
            "observer_solid_angle",
            "phase_symplectic_volume",
            "finite_branch_counting",
            "ordered_incidence_coarea_density",
            "csp_character_half_density_candidate",
        ],
        "noncommuting_phase_cases": noncommuting_phase_cases,
        "observational_outcomes": "CLOSED_AND_UNREAD",
        "phase_volume": "M_pullback_nu_target=r^2*nu_source__M_pushforward_nu_source=r^-2*nu_target",
        "reverse_query_density_differences": reverse_query_density_differences,
        "selected_alternative": "B_TYPED_CANONICAL_GEOMETRIC_MEASURES_EXIST__PHYSICAL_BRANCH_MEASURE_UNSELECTED",
        "status": "PASS",
        "three_measure_separations": three_measure_separations,
        "transverse_jacobian": "J=omega_B*A=A/r",
        "unequal_counting_coarea_cases": unequal_counting_coarea,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
