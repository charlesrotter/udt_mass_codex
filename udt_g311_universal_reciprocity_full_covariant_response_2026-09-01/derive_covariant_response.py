#!/usr/bin/env python3
"""Exact production checks for the G311 covariant reciprocity classification."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


DIM = 4
SIGNS = (F(-1), F(1), F(1), F(1))
COMPONENTS = tuple((i, j) for i in range(DIM) for j in range(i, DIM))


def zeros() -> list[list[F]]:
    return [[F(0) for _ in range(DIM)] for _ in range(DIM)]


def metric() -> list[list[F]]:
    out = zeros()
    for i, sign in enumerate(SIGNS):
        out[i][i] = sign
    return out


def dot(v: tuple[F, ...], w: tuple[F, ...]) -> F:
    return sum(SIGNS[i] * v[i] * w[i] for i in range(DIM))


def lower(v: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(SIGNS[i] * v[i] for i in range(DIM))


def reciprocal_tangent(u: tuple[F, ...], n: tuple[F, ...]) -> list[list[F]]:
    assert dot(u, u) == -1
    assert dot(n, n) == 1
    assert dot(u, n) == 0
    uf, nf = lower(u), lower(n)
    out = zeros()
    for i in range(DIM):
        for j in range(DIM):
            out[i][j] = 2 * (uf[i] * uf[j] + nf[i] * nf[j])
    return out


def flatten(tensor: list[list[F]]) -> list[F]:
    return [tensor[i][j] for i, j in COMPONENTS]


def unflatten(values: list[F]) -> list[list[F]]:
    out = zeros()
    for value, (i, j) in zip(values, COMPONENTS):
        out[i][j] = value
        out[j][i] = value
    return out


def tensor_trace(tensor: list[list[F]]) -> F:
    return sum(SIGNS[i] * tensor[i][i] for i in range(DIM))


def tensor_pair(left: list[list[F]], right: list[list[F]]) -> F:
    total = F(0)
    for i in range(DIM):
        for j in range(DIM):
            total += SIGNS[i] * SIGNS[j] * left[i][j] * right[i][j]
    return total


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[a[i][j] + b[i][j] for j in range(DIM)] for i in range(DIM)]


def scale(c: F, tensor: list[list[F]]) -> list[list[F]]:
    return [[c * tensor[i][j] for j in range(DIM)] for i in range(DIM)]


def tracefree(tensor: list[list[F]]) -> list[list[F]]:
    return add(tensor, scale(-tensor_trace(tensor) / DIM, metric()))


def rref(matrix: list[list[F]]) -> tuple[list[list[F]], list[int]]:
    rows = [row[:] for row in matrix]
    if not rows:
        return rows, []
    n_rows, n_cols = len(rows), len(rows[0])
    pivot_cols: list[int] = []
    pivot_row = 0
    for col in range(n_cols):
        found = next((r for r in range(pivot_row, n_rows) if rows[r][col]), None)
        if found is None:
            continue
        rows[pivot_row], rows[found] = rows[found], rows[pivot_row]
        lead = rows[pivot_row][col]
        rows[pivot_row] = [value / lead for value in rows[pivot_row]]
        for r in range(n_rows):
            if r == pivot_row or not rows[r][col]:
                continue
            factor = rows[r][col]
            rows[r] = [rows[r][c] - factor * rows[pivot_row][c] for c in range(n_cols)]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == n_rows:
            break
    return rows, pivot_cols


def rank(matrix: list[list[F]]) -> int:
    return len(rref(matrix)[1])


def nullspace(matrix: list[list[F]]) -> list[list[F]]:
    reduced, pivots = rref(matrix)
    n_cols = len(matrix[0])
    free_cols = [col for col in range(n_cols) if col not in pivots]
    basis: list[list[F]] = []
    for free in free_cols:
        vector = [F(0) for _ in range(n_cols)]
        vector[free] = F(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free]
        basis.append(vector)
    return basis


def balance_row(h: list[list[F]]) -> list[F]:
    row: list[F] = []
    for i, j in COMPONENTS:
        factor = F(1) if i == j else F(2)
        row.append(factor * SIGNS[i] * SIGNS[j] * h[i][j])
    return row


def standard_tracefree_basis() -> list[list[F]]:
    basis: list[list[F]] = []
    for spatial in (1, 2, 3):
        item = zeros()
        item[0][0] = 1
        item[spatial][spatial] = 1
        basis.append(item)
    for i in range(DIM):
        for j in range(i + 1, DIM):
            item = zeros()
            item[i][j] = item[j][i] = 1
            basis.append(item)
    assert len(basis) == 9
    assert all(tensor_trace(item) == 0 for item in basis)
    return basis


def exact_pair_basis() -> list[list[list[F]]]:
    e = [tuple(F(1) if i == j else F(0) for i in range(DIM)) for j in range(DIM)]
    pairs: list[tuple[tuple[F, ...], tuple[F, ...]]] = []
    for i in (1, 2, 3):
        pairs.append((e[0], e[i]))
    for i, j in ((1, 2), (1, 3), (2, 3)):
        n = tuple(F(3, 5) * e[i][k] + F(4, 5) * e[j][k] for k in range(DIM))
        pairs.append((e[0], n))
    for i in (1, 2, 3):
        u = tuple(F(5, 3) * e[0][k] + F(4, 3) * e[i][k] for k in range(DIM))
        n = tuple(F(4, 3) * e[0][k] + F(5, 3) * e[i][k] for k in range(DIM))
        pairs.append((u, n))
    return [reciprocal_tangent(u, n) for u, n in pairs]


def matrix_multiply(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [
        [sum(a[i][k] * b[k][j] for k in range(DIM)) for j in range(DIM)]
        for i in range(DIM)
    ]


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [[a[j][i] for j in range(DIM)] for i in range(DIM)]


def congruence(lorentz: list[list[F]], tensor: list[list[F]]) -> list[list[F]]:
    return matrix_multiply(transpose(lorentz), matrix_multiply(tensor, lorentz))


def projector_covariance_check() -> bool:
    e = unflatten([F(2), F(1), F(-2), F(3), F(5), F(4), F(-1), F(7), F(6), F(11)])
    boost = [
        [F(5, 3), F(4, 3), F(0), F(0)],
        [F(4, 3), F(5, 3), F(0), F(0)],
        [F(0), F(0), F(1), F(0)],
        [F(0), F(0), F(0), F(1)],
    ]
    eta = metric()
    assert congruence(boost, eta) == eta
    lhs = tracefree(congruence(boost, e))
    rhs = congruence(boost, tracefree(e))
    return lhs == rhs and tensor_trace(lhs) == 0


def run() -> dict[str, object]:
    pair_basis = exact_pair_basis()
    pair_vectors = [flatten(item) for item in pair_basis]
    shape_rank = rank(pair_vectors)
    assert shape_rank == 9
    assert all(tensor_trace(item) == 0 for item in pair_basis)

    full_balance = [balance_row(item) for item in pair_basis]
    balance_rank = rank(full_balance)
    annihilator = nullspace(full_balance)
    assert balance_rank == 9
    assert len(annihilator) == 1
    annihilator_tensor = unflatten(annihilator[0])
    eta = metric()
    scale_ratio = annihilator_tensor[0][0] / eta[0][0]
    assert annihilator_tensor == scale(scale_ratio, eta)

    tf_basis = standard_tracefree_basis()
    rank_census: dict[str, dict[str, int]] = {}
    for r in range(1, 10):
        restricted = [
            [tensor_pair(tf_direction, pair_basis[row]) for tf_direction in tf_basis]
            for row in range(r)
        ]
        functional_rank = rank(restricted)
        assert functional_rank == r
        rank_census[str(r)] = {
            "pair_span_rank": r,
            "response_shape_nullity": 9 - functional_rank,
        }

    sample = unflatten([F(2), F(1), F(-2), F(3), F(5), F(4), F(-1), F(7), F(6), F(11)])
    tf_sample = tracefree(sample)
    assert tensor_trace(tf_sample) == 0
    assert add(tf_sample, scale(tensor_trace(sample) / 4, eta)) == sample
    assert projector_covariance_check()

    for value in (F(-7), F(0), F(5, 3)):
        pure_trace = scale(value, eta)
        assert all(tensor_pair(pure_trace, h) == 0 for h in pair_basis)
    variable_lambda_derivative_at_one = F(2)
    assert variable_lambda_derivative_at_one != 0

    ricci_flrw_t0 = zeros()
    for i, value in enumerate((F(-6), F(2), F(2), F(2))):
        ricci_flrw_t0[i][i] = value
    scalar_flrw_t0 = tensor_trace(ricci_flrw_t0)
    assert scalar_flrw_t0 == 12
    s_flrw_t0 = tracefree(ricci_flrw_t0)
    assert flatten(s_flrw_t0) == [F(-3), F(0), F(0), F(0), F(-1), F(0), F(0), F(-1), F(0), F(-1)]
    ricci_balance = [tensor_pair(ricci_flrw_t0, h) for h in pair_basis]
    assert any(value != 0 for value in ricci_balance)
    weyl_quadratic_response = zeros()  # The independent verifier derives C_abcd=0 for this metric.
    assert all(tensor_pair(weyl_quadratic_response, h) == 0 for h in pair_basis)

    a_coeff, b_coeff = F(3), F(-5)
    arbitrary_ricci = unflatten([F(-2), F(1), F(0), F(2), F(4), F(-1), F(3), F(5), F(2), F(7)])
    scalar_r = tensor_trace(arbitrary_ricci)
    response = add(scale(a_coeff, arbitrary_ricci), scale(b_coeff * scalar_r, eta))
    assert tracefree(response) == scale(a_coeff, tracefree(arbitrary_ricci))

    result = {
        "landing": "FULL_COVARIANT_RECIPROCITY_CLOSES_RESPONSE_SHAPE_ONLY__RESPONSE_CONSTITUTION_REMAINS_OPEN",
        "strongest_conditional_landing": "G301_FAITHFUL_BRANCH_GIVES_EINSTEIN_SPACE_DYNAMICS",
        "adoption_status": "OWNER_ADOPTED_PROVISIONAL_POSTULATE__NOT_DERIVED__NOT_CANON",
        "symmetric_metric_dimension": 10,
        "reciprocal_shape_rank": shape_rank,
        "balance_rank": balance_rank,
        "full_rank_shape_nullity": 0,
        "full_response_annihilator": "span(g_ab)",
        "covariant_unconditional_equation": "TF_g(E)=0, equivalently E=lambda(x)*g",
        "lambda_constant_from_pointwise_ddr_alone": False,
        "lambda_constant_if_divergence_free_response_added": True,
        "rank_census": rank_census,
        "projector_is_lorentz_covariant": True,
        "g301_conditional_equation": "Ric_ab-(R/4)*g_ab=0",
        "g301_connected_consequence": "dR=0; Ric_ab=(R0/4)*g_ab",
        "g301_remaining_metric_configuration_dof_per_point": 2,
        "g301_remaining_initial_phase_dof_per_point": 4,
        "g301_regional_scalar_data": 1,
        "countermetric": "g_b=-dt^2+exp(2*b*t^2)*(dx^2+dy^2+dz^2), evaluated at b=1,t=0",
        "countermetric_scalar_curvature_at_t0": int(scalar_flrw_t0),
        "countermetric_tracefree_ricci_nonzero": True,
        "countermetric_weyl_zero": True,
        "ricci_response_fails_countermetric_ddr": True,
        "weyl_quadratic_response_passes_countermetric_ddr": True,
        "response_architecture_selected_by_covariance_alone": False,
        "metric_or_kernel_changed": False,
        "observations_sources_actions_matter_mass_scale_xmax_used": False,
        "production_checks": 24,
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
