#!/usr/bin/env python3
"""Dependency-free exact full-metric G260 production derivation.

The script reconstructs the registered formulas from raw metric two-jets with
exact rational arithmetic.  It uses no third-party package and does not import
the independent verifier or read any prior result artifact.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


OUT = Path(__file__).with_name("DERIVATION_RESULT.json")


def zeros(*shape: int):
    if len(shape) == 1:
        return [F(0) for _ in range(shape[0])]
    return [zeros(*shape[1:]) for _ in range(shape[0])]


def diagonal_inverse(metric):
    inverse = zeros(len(metric), len(metric))
    for i in range(len(metric)):
        assert metric[i][i] != 0
        assert all(metric[i][j] == 0 for j in range(len(metric)) if i != j)
        inverse[i][i] = 1 / metric[i][i]
    return inverse


def curvature_from_metric_jets(metric, first_metric, second_metric):
    """Return exact Ricci, mixed Einstein, and scalar curvature at one event."""
    n = len(metric)
    inverse = diagonal_inverse(metric)
    first_inverse = zeros(n, n, n)
    for a in range(n):
        for b in range(n):
            for e in range(n):
                first_inverse[a][b][e] = -sum(
                    inverse[a][m]
                    * first_metric[m][q][e]
                    * inverse[q][b]
                    for m in range(n)
                    for q in range(n)
                )

    christoffel = zeros(n, n, n)
    first_christoffel = zeros(n, n, n, n)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                first_terms = [
                    first_metric[d][c][b]
                    + first_metric[d][b][c]
                    - first_metric[b][c][d]
                    for d in range(n)
                ]
                christoffel[a][b][c] = sum(
                    inverse[a][d] * first_terms[d] for d in range(n)
                ) / 2
                for e in range(n):
                    second_terms = [
                        second_metric[d][c][b][e]
                        + second_metric[d][b][c][e]
                        - second_metric[b][c][d][e]
                        for d in range(n)
                    ]
                    first_christoffel[a][b][c][e] = (
                        sum(first_inverse[a][d][e] * first_terms[d] for d in range(n))
                        + sum(inverse[a][d] * second_terms[d] for d in range(n))
                    ) / 2

    ricci = zeros(n, n)
    for a in range(n):
        for b in range(n):
            ricci[a][b] = sum(
                first_christoffel[c][a][b][c]
                - first_christoffel[c][a][c][b]
                + sum(
                    christoffel[c][c][d] * christoffel[d][a][b]
                    - christoffel[c][b][d] * christoffel[d][a][c]
                    for d in range(n)
                )
                for c in range(n)
            )
    scalar = sum(
        inverse[a][b] * ricci[a][b] for a in range(n) for b in range(n)
    )
    einstein_covariant = zeros(n, n)
    einstein_mixed = zeros(n, n)
    for a in range(n):
        for b in range(n):
            einstein_covariant[a][b] = ricci[a][b] - metric[a][b] * scalar / 2
            einstein_mixed[a][b] = sum(
                inverse[a][c] * einstein_covariant[c][b] for c in range(n)
            )
    return ricci, einstein_mixed, scalar


def four_metric_jets(r: F, f: F, fp: F, fpp: F, sphere_curvature: bool):
    """Metric two-jets at an equatorial event, with c_E fixed to its unit calibration."""
    metric = zeros(4, 4)
    first = zeros(4, 4, 4)
    second = zeros(4, 4, 4, 4)
    metric[0][0] = -f
    metric[1][1] = 1 / f
    metric[2][2] = r**2
    metric[3][3] = r**2
    first[0][0][1] = -fp
    first[1][1][1] = -fp / f**2
    first[2][2][1] = 2 * r
    first[3][3][1] = 2 * r
    second[0][0][1][1] = -fpp
    second[1][1][1][1] = 2 * fp**2 / f**3 - fpp / f**2
    second[2][2][1][1] = 2
    second[3][3][1][1] = 2
    if sphere_curvature:
        second[3][3][2][2] = -2 * r**2
    return metric, first, second


def two_metric_jets(f: F, fp: F, fpp: F):
    metric = zeros(2, 2)
    first = zeros(2, 2, 2)
    second = zeros(2, 2, 2, 2)
    metric[0][0] = -f
    metric[1][1] = 1 / f
    first[0][0][1] = -fp
    first[1][1][1] = -fp / f**2
    second[0][0][1][1] = -fpp
    second[1][1][1][1] = 2 * fp**2 / f**3 - fpp / f**2
    return metric, first, second


def solve_exact(rows, values):
    """Solve an overdetermined exact linear system and prove consistency and uniqueness."""
    width = len(rows[0])
    matrix = [list(row) + [value] for row, value in zip(rows, values)]
    pivot_row = 0
    pivots = []
    for column in range(width):
        selected = next(
            (index for index in range(pivot_row, len(matrix)) if matrix[index][column]),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        pivot = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot for entry in matrix[pivot_row]]
        for index in range(len(matrix)):
            if index == pivot_row or not matrix[index][column]:
                continue
            factor = matrix[index][column]
            matrix[index] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(matrix[index], matrix[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
    assert len(pivots) == width
    assert all(any(row[:width]) or row[-1] == 0 for row in matrix)
    solution = [F(0) for _ in range(width)]
    for row_index, column in enumerate(pivots):
        solution[column] = matrix[row_index][-1]
    assert all(
        sum(coefficient * value for coefficient, value in zip(row, solution)) == target
        for row, target in zip(rows, values)
    )
    return tuple(solution)


def main() -> None:
    probes = (
        (F(2), F(3, 2), F(1, 3), F(-2, 5)),
        (F(3), F(5, 4), F(-2, 7), F(3, 8)),
        (F(5, 2), F(7, 3), F(4, 9), F(5, 11)),
        (F(7, 3), F(9, 5), F(-5, 8), F(-1, 6)),
        (F(4), F(11, 6), F(7, 10), F(2, 9)),
        (F(9, 2), F(13, 7), F(-3, 11), F(4, 13)),
    )

    sphere_data = []
    flat_data = []
    for r, f, fp, fpp in probes:
        ricci, einstein, scalar = curvature_from_metric_jets(
            *four_metric_jets(r, f, fp, fpp, True)
        )
        _, flat_einstein, _ = curvature_from_metric_jets(
            *four_metric_jets(r, f, fp, fpp, False)
        )
        _, base_einstein, _ = curvature_from_metric_jets(*two_metric_jets(f, fp, fpp))
        assert all(base_einstein[i][j] == 0 for i in range(2) for j in range(2))
        assert all(einstein[i][j] == 0 for i in range(4) for j in range(4) if i != j)
        assert all(ricci[i][j] == 0 for i in range(4) for j in range(4) if i != j)
        sphere_data.append((r, f, fp, fpp, einstein, scalar))
        flat_data.append((r, f, fp, fpp, flat_einstein))

    e0_coefficients = solve_exact(
        [(r * fp, f, F(1)) for r, f, fp, _, _, _ in sphere_data],
        [r**2 * tensor[0][0] for r, _, _, _, tensor, _ in sphere_data],
    )
    e1_coefficients = solve_exact(
        [(r * fp, r**2 * fpp) for r, _, fp, fpp, _, _ in sphere_data],
        [r**2 * tensor[2][2] for r, _, _, _, tensor, _ in sphere_data],
    )
    scalar_coefficients = solve_exact(
        [(r**2 * fpp, r * fp, f, F(1)) for r, f, fp, fpp, _, _ in sphere_data],
        [r**2 * scalar for r, _, _, _, _, scalar in sphere_data],
    )
    flat_e0_coefficients = solve_exact(
        [(r * fp, f, F(1)) for r, f, fp, _, _ in flat_data],
        [r**2 * tensor[0][0] for r, _, _, _, tensor in flat_data],
    )
    assert e0_coefficients == (F(1), F(1), F(-1))
    assert e1_coefficients == (F(1), F(1, 2))
    assert scalar_coefficients == (F(-1), F(-4), F(-2), F(2))
    assert flat_e0_coefficients == (F(1), F(1), F(0))

    angular_parallel_values = []
    angular_perp_values = []
    for r, f, fp, fpp, _, _ in sphere_data:
        p = -r * fp / (2 * f)
        q = -r**2 * (fpp / f - fp**2 / f**2) / 2
        angular_parallel_values.append(f * (2 * p**2 + p - q))
        angular_perp_values.append(1 - f * (1 + p))
    parallel_coefficients = solve_exact(
        [(r**2 * fpp, r * fp) for r, _, fp, fpp, _, _ in sphere_data],
        angular_parallel_values,
    )
    perp_coefficients = solve_exact(
        [(F(1), f, r * fp) for r, f, fp, _, _, _ in sphere_data],
        angular_perp_values,
    )
    sum_coefficients = solve_exact(
        [(r**2 * fpp, f, F(1)) for r, f, _, fpp, _, _ in sphere_data],
        [left + right for left, right in zip(angular_parallel_values, angular_perp_values)],
    )
    assert parallel_coefficients == (F(1, 2), F(-1, 2))
    assert perp_coefficients == (F(1), F(-1), F(1, 2))
    assert sum_coefficients == (F(1, 2), F(-1), F(1))

    for r, c in ((F(2), F(1, 3)), (F(5), F(-2, 3)), (F(7, 2), F(4, 5))):
        f = 1 + c / r
        assert f > 0 and c != 0
        fp = -c / r**2
        fpp = 2 * c / r**3
        ricci, einstein, _ = curvature_from_metric_jets(
            *four_metric_jets(r, f, fp, fpp, True)
        )
        assert all(ricci[i][j] == 0 for i in range(4) for j in range(4))
        assert all(einstein[i][j] == 0 for i in range(4) for j in range(4))
        a_parallel = (r**2 * fpp - r * fp) / 2
        a_perp = 1 - f + r * fp / 2
        assert a_parallel == 3 * c / (2 * r)
        assert a_perp == -3 * c / (2 * r)
        _, flat_einstein, _ = curvature_from_metric_jets(
            *four_metric_jets(r, f, fp, fpp, False)
        )
        assert r**2 * flat_einstein[0][0] == 1

    # The trace equation has indicial polynomial k(k-1)-2=(k-2)(k+1).
    roots = tuple(k for k in range(-4, 5) if k * (k - 1) - 2 == 0)
    assert roots == (-1, 2)
    for r, a, b in (
        (F(2), F(1, 5), F(-1, 7)),
        (F(3), F(-2, 9), F(4, 11)),
        (F(5, 2), F(3, 8), F(2, 13)),
    ):
        f = 1 + a * r**2 + b / r
        fp = 2 * a * r - b / r**2
        fpp = 2 * a + 2 * b / r**3
        a_sum = (r**2 * fpp - r * fp) / 2 + 1 - f + r * fp / 2
        e0 = r * fp + f - 1
        e1 = r * fp + r**2 * fpp / 2
        assert a_sum == 0
        assert e0 == e1 == 3 * a * r**2

    mass_probes = (
        (F(2), F(1, 3), F(-2, 5), F(3, 7)),
        (F(3), F(-1, 4), F(5, 9), F(-2, 11)),
        (F(5, 2), F(7, 8), F(1, 6), F(4, 13)),
        (F(7, 3), F(-3, 10), F(-4, 15), F(2, 9)),
        (F(4), F(5, 12), F(7, 16), F(-3, 14)),
    )
    mass_values = []
    for r, mu, mup, mupp in mass_probes:
        f = 1 - 2 * mu / r
        fp = -2 * mup / r + 2 * mu / r**2
        fpp = -2 * mupp / r + 4 * mup / r**2 - 4 * mu / r**3
        mass_values.append(
            (
                r,
                mu,
                mup,
                mupp,
                r * fp + f - 1,
                r * fp + r**2 * fpp / 2,
                (r**2 * fpp - r * fp) / 2,
                1 - f + r * fp / 2,
            )
        )
    assert solve_exact([(mup,) for _, _, mup, _, _, _, _, _ in mass_values],
                       [e0 for _, _, _, _, e0, _, _, _ in mass_values]) == (F(-2),)
    assert solve_exact([(r * mupp,) for r, _, _, mupp, _, _, _, _ in mass_values],
                       [e1 for _, _, _, _, _, e1, _, _ in mass_values]) == (F(-1),)
    assert solve_exact(
        [(r * mupp, mup, mu / r) for r, mu, mup, mupp, _, _, _, _ in mass_values],
        [ap for _, _, _, _, _, _, ap, _ in mass_values],
    ) == (F(-1), F(3), F(-3))
    assert solve_exact(
        [(mup, mu / r) for r, mu, mup, _, _, _, _, _ in mass_values],
        [at for _, _, _, _, _, _, _, at in mass_values],
    ) == (F(-1), F(3))

    pair_f = F(1, 2)
    pair_r = F(2)
    alpha = F(1, 10)
    beta = F(1, 5)
    pair_h00 = -pair_f + pair_r**2 * alpha**2
    pair_h11 = 1 / pair_f + pair_r**2 * beta**2
    pair_angular_00 = pair_r**2 * alpha**2
    pair_angular_11 = pair_r**2 * beta**2
    assert pair_h00 < 0 < pair_h11 and pair_h00 * pair_h11 < 0
    assert pair_angular_00 > 0 and pair_angular_11 > 0

    result = {
        "status": "PASS",
        "landing": "FULL_METRIC_CANCELLATION_WITH_ACTIVE_ANGULAR_SECTOR",
        "scope": "primary_static_spherical_positive_f_GR_quiet_comparison_only",
        "full_sphere": {
            "Einstein_mixed_diagonal": [
                "(r*Derivative(f(r), r) + f(r) - 1)/r**2",
                "(r*Derivative(f(r), r) + f(r) - 1)/r**2",
                "(r*Derivative(f(r), (r, 2)) + 2*Derivative(f(r), r))/(2*r)",
                "(r*Derivative(f(r), (r, 2)) + 2*Derivative(f(r), r))/(2*r)",
            ],
            "Ricci_scalar": "-(r**2*Derivative(f(r), (r, 2)) + 4*r*Derivative(f(r), r) + 2*f(r) - 2)/r**2",
            "E0": "r*Derivative(f(r), r) + f(r) - 1",
            "E1": "r*(r*Derivative(f(r), (r, 2)) + 2*Derivative(f(r), r))/2",
        },
        "angular_interlock": {
            "A_parallel": "r*(r*Derivative(f(r), (r, 2)) - Derivative(f(r), r))/2",
            "A_perp": "(r*Derivative(f(r), r) - 2*f(r) + 2)/2",
            "A_sum": "(r**2*Derivative(f(r), (r, 2)) - 2*f(r) + 2)/2",
            "identity": "A_parallel+A_perp=E1-E0",
        },
        "vacuum_family": {
            "f": "1+C/r",
            "full_Ricci": "0",
            "full_Einstein": "0",
            "A_parallel": "3*C/(2*r)",
            "A_perp": "-3*C/(2*r)",
            "A_sum": "0",
        },
        "balanced_angular_trace_family": {
            "general_local_f": "1+a*r^2+b/r",
            "E0": "3*a*r^2",
            "E1": "3*a*r^2",
            "vacuum_requires": "a=0",
        },
        "mass_aspect": {
            "E0": "-2*Derivative(mu(r), r)",
            "E1": "-r*Derivative(mu(r), (r, 2))",
            "A_parallel": "-(r**2*Derivative(mu(r), (r, 2)) - 3*r*Derivative(mu(r), r) + 3*mu(r))/r",
            "A_perp": "-(r*Derivative(mu(r), r) - 3*mu(r))/r",
            "A_sum": "-r*Derivative(mu(r), (r, 2)) + 2*Derivative(mu(r), r)",
        },
        "corruption_controls": {
            "isolated_2d_Einstein_identically_zero": True,
            "flat_k0_E0": "r*Derivative(f(r), r) + f(r)",
            "flat_k0_on_spherical_vacuum_family": "1",
        },
        "nonradial_pair_witness": {
            "h00": str(pair_h00),
            "h11": str(pair_h11),
            "angular_gram_00": str(pair_angular_00),
            "angular_gram_11": str(pair_angular_11),
            "regular_lorentzian": True,
        },
        "checks": {
            "direct_full_4d_tensor": True,
            "angular_identity": True,
            "vacuum_full_tensor_zero": True,
            "vacuum_angular_modes_individually_nonzero": True,
            "two_dimensional_base_vacuous": True,
            "flat_screen_corrupts_vacuum_family": True,
            "balanced_trace_family_classified_without_filter": True,
            "nonradial_pair_angular_gram_retained": True,
        },
        "maximum_conclusion": "Bounded quiet-regime non-discard theorem only; no UDT parent equation, source/history, or loud-regime extension selected.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
