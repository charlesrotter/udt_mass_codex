#!/usr/bin/env python3
"""Production symbolic derivation for the bounded G188 complete-coframe witness."""

from __future__ import annotations

import json
import sympy as sp


DIM = 4
u_coord, v_coord, x_coord, y_coord = sp.symbols("u v x y", real=True)
COORDS = (u_coord, v_coord, x_coord, y_coord)
ZERO_POINT = {x_coord: 0, y_coord: 0}


def connection_and_curvature(metric: sp.Matrix):
    inverse = sp.simplify(metric.inv())
    gamma = [[[
        sp.simplify(sp.Rational(1, 2) * sum(
            inverse[a, e] * (
                sp.diff(metric[e, c], COORDS[b])
                + sp.diff(metric[e, b], COORDS[c])
                - sp.diff(metric[b, c], COORDS[e])
            )
            for e in range(DIM)
        ))
        for c in range(DIM)] for b in range(DIM)] for a in range(DIM)]
    riemann = [[[[] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    riemann[a][b][c].append(sp.simplify(
                        sp.diff(gamma[a][d][b], COORDS[c])
                        - sp.diff(gamma[a][c][b], COORDS[d])
                        + sum(
                            gamma[a][c][e] * gamma[e][d][b]
                            - gamma[a][d][e] * gamma[e][c][b]
                            for e in range(DIM)
                        )
                    ))
    return inverse, gamma, riemann


def inner(metric: sp.Matrix, left: sp.Matrix, right: sp.Matrix):
    return sp.simplify((left.T * metric * right)[0])


def tidal_entry(metric, riemann, left, ray, right):
    return sp.simplify(sum(
        metric[mu, a] * left[mu] * riemann[a][b][c][d]
        * ray[b] * right[c] * ray[d]
        for mu in range(DIM)
        for a in range(DIM)
        for b in range(DIM)
        for c in range(DIM)
        for d in range(DIM)
    ).subs(ZERO_POINT))


def central_covariant_derivative(gamma, ray, vector):
    return sp.Matrix([
        sp.simplify(sum(
            gamma[a][b][c].subs(ZERO_POINT) * ray[b] * vector[c]
            for b in range(DIM) for c in range(DIM)
        ))
        for a in range(DIM)
    ])


def witness_coframe(mixing: bool = True):
    zeta = x_coord + y_coord if mixing else sp.Integer(0)
    return sp.Matrix([
        [sp.Rational(1, 2), 1, 0, 0],
        [-sp.Rational(1, 2), 1, 0, 0],
        [zeta, 0, 1, 0],
        [zeta, 0, 0, 1],
    ])


def main():
    eta = sp.diag(-1, 1, 1, 1)
    coframe = witness_coframe(mixing=True)
    metric = sp.simplify(coframe.T * eta * coframe)
    inverse, gamma, riemann = connection_and_curvature(metric)
    metric0 = metric.subs(ZERO_POINT)

    ray = sp.Matrix([1, 0, 0, 0])
    observer = sp.Matrix([sp.Rational(1, 2), 1, 0, 0])
    ruler = ray - observer
    screen = (sp.Matrix([0, 0, 1, 0]), sp.Matrix([0, 0, 0, 1]))

    tidal = sp.Matrix([
        [tidal_entry(metric, riemann, left, ray, right) for right in screen]
        for left in screen
    ])
    expected_tidal = sp.Matrix([[-2, -2], [-2, -2]])

    pair = sp.Matrix.hstack(observer, ruler)
    pair_metric = sp.simplify(pair.T * metric0 * pair)
    projector = sp.simplify(
        sp.eye(DIM) - pair * pair_metric.inv() * pair.T * metric0
    )

    lam = sp.symbols("lambda", real=True)
    d_plus = sp.sinh(2 * lam) / 2
    p_plus = sp.Matrix([[1, 1], [1, 1]]) / 2
    p_minus = sp.eye(2) - p_plus
    finite_map = sp.simplify(d_plus * p_plus + lam * p_minus)

    flat_coframe = witness_coframe(mixing=False)
    flat_metric = sp.simplify(flat_coframe.T * eta * flat_coframe)
    _, _, flat_riemann = connection_and_curvature(flat_metric)
    flat_tidal = sp.Matrix([
        [tidal_entry(flat_metric, flat_riemann, left, ray, right) for right in screen]
        for left in screen
    ])
    flat_finite_map = lam * sp.eye(2)

    boost = sp.Matrix([
        [sp.Rational(5, 3), 0, sp.Rational(4, 3), 0],
        [0, 1, 0, 0],
        [sp.Rational(4, 3), 0, sp.Rational(5, 3), 0],
        [0, 0, 0, 1],
    ])
    boosted_metric = sp.simplify((boost * coframe).T * eta * (boost * coframe))

    alpha, beta = sp.symbols("alpha beta", real=True)
    gauged_screen = (screen[0] + alpha * ray, screen[1] + beta * ray)
    gauged_tidal = sp.Matrix([
        [tidal_entry(metric, riemann, left, ray, right) for right in gauged_screen]
        for left in gauged_screen
    ])

    q_source = sp.Matrix([
        [sp.Rational(3, 5), -sp.Rational(4, 5)],
        [sp.Rational(4, 5), sp.Rational(3, 5)],
    ])
    q_sink = sp.Matrix([
        [sp.Rational(5, 13), -sp.Rational(12, 13)],
        [sp.Rational(12, 13), sp.Rational(5, 13)],
    ])
    transformed_map = sp.simplify(q_sink.T * finite_map * q_source)

    tp, tq = sp.symbols("T_parallel T_perpendicular", real=True)
    dp = sp.Function("D_parallel")(lam)
    dq = sp.Function("D_perpendicular")(lam)
    diagonal_tidal = sp.diag(tp, tq)
    diagonal_map = sp.diag(dp, dq)
    diagonal_residual = sp.simplify(
        diagonal_map.diff(lam, 2) + diagonal_tidal * diagonal_map
    )
    expected_diagonal_residual = sp.diag(
        sp.diff(dp, lam, 2) + tp * dp,
        sp.diff(dq, lam, 2) + tq * dq,
    )

    checks = {
        "affine_central_null_geodesic": all(
            sp.simplify(gamma[a][0][0].subs(ZERO_POINT)) == 0 for a in range(DIM)
        ),
        "coframe_invertible": sp.simplify(coframe.det()) != 0,
        "coframe_metric_readout": sp.simplify(metric - coframe.T * eta * coframe) == sp.zeros(DIM),
        "complete_metric_determinant_minus_one": sp.simplify(metric.det()) == -1,
        "finite_cross_response_nonzero": sp.simplify(finite_map[0, 1]) != 0,
        "finite_jacobi_equation": sp.simplify(
            finite_map.diff(lam, 2) + tidal * finite_map
        ) == sp.zeros(2),
        "flat_deletion_finite_equation": sp.simplify(
            flat_finite_map.diff(lam, 2) + flat_tidal * flat_finite_map
        ) == sp.zeros(2),
        "flat_deletion_vertex_data": flat_finite_map.subs(lam, 0) == sp.zeros(2)
        and flat_finite_map.diff(lam).subs(lam, 0) == sp.eye(2),
        "flat_deletion_tidal_zero": flat_tidal == sp.zeros(2),
        "g187_diagonal_specialization": diagonal_residual == expected_diagonal_residual
        and diagonal_residual[0, 1] == 0
        and diagonal_residual[1, 0] == 0,
        "initial_screen_matches_pair_projector": all(
            sp.simplify(projector * vector - vector) == sp.zeros(DIM, 1)
            for vector in screen
        ),
        "lorentz_coframe_gauge_invariant": sp.simplify(boost.T * eta * boost - eta) == sp.zeros(DIM)
        and sp.simplify(boosted_metric - metric) == sp.zeros(DIM),
        "null_gauge_tidal_invariant": sp.simplify(gauged_tidal - tidal) == sp.zeros(2),
        "observer_normalizes_ray": inner(metric0, observer, ray) == -1,
        "observer_unit_timelike": inner(metric0, observer, observer) == -1,
        "pair_projector_annihilates_pair": sp.simplify(projector * pair) == sp.zeros(DIM, 2),
        "pair_projector_rank_two": sp.simplify(sp.trace(projector)) == 2,
        "ray_is_null": inner(metric0, ray, ray) == 0,
        "ruler_unit_spacelike": inner(metric0, ruler, ruler) == 1,
        "screen_is_orthonormal": sp.Matrix([
            [inner(metric0, left, right) for right in screen] for left in screen
        ]) == sp.eye(2),
        "screen_is_parallel": all(
            central_covariant_derivative(gamma, ray, vector) == sp.zeros(DIM, 1)
            for vector in screen
        ),
        "screen_is_ray_orthogonal": all(inner(metric0, vector, ray) == 0 for vector in screen),
        "tidal_cross_is_live": tidal[0, 1] == tidal[1, 0] == -2,
        "tidal_is_expected": tidal == expected_tidal,
        "tidal_is_self_adjoint": tidal == tidal.T,
        "vertex_position_zero": finite_map.subs(lam, 0) == sp.zeros(2),
        "vertex_slope_identity": finite_map.diff(lam).subs(lam, 0) == sp.eye(2),
        "endpoint_o2_abs_det_covariant": sp.simplify(
            transformed_map.det() ** 2 - finite_map.det() ** 2
        ) == 0,
    }
    failed = [name for name, passed in checks.items() if not passed]
    output = {
        "audit": "G188_PRODUCTION",
        "checks": checks,
        "coframe": str(coframe),
        "finite_map": str(finite_map),
        "landing": (
            "GENERAL_COMPLETE_COFRAME_NULL_JACOBI_FUNCTOR_DERIVED_CONDITIONALLY"
            "__G187_IS_THE_REFLECTION_DIAGONAL_SPECIALIZATION"
            "__GENUINE_COFRAME_MIXING_GENERATES_OFFDIAGONAL_FINITE_RESPONSE"
        ),
        "metric": str(metric),
        "status": "PASS" if not failed else "FAIL",
        "tidal": str(tidal),
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    if failed:
        raise SystemExit("failed checks: " + ", ".join(failed))


if __name__ == "__main__":
    main()
