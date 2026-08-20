#!/usr/bin/env python3
"""Exact symbolic checks for the preregistered G190 joint evaluator.

This implementation is intentionally bounded.  It checks the completed pair null frame, a fully
time-live conformal mathematical control, the general frequency-contraction identity on that
control, the finite Jacobi equation, and the static/local regression limits.  It does not select a
metric history, fit observations, or implement radiative transfer.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


def simp(value):
    return sp.simplify(sp.trigsimp(value))


def christoffel(metric: sp.Matrix, coords: tuple[sp.Symbol, ...]):
    dim = len(coords)
    inverse = simp(metric.inv())
    gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                gamma[a][b][c] = simp(
                    sp.Rational(1, 2)
                    * sum(
                        inverse[a, d]
                        * (
                            sp.diff(metric[d, c], coords[b])
                            + sp.diff(metric[d, b], coords[c])
                            - sp.diff(metric[b, c], coords[d])
                        )
                        for d in range(dim)
                    )
                )
    return gamma


def riemann(gamma, coords: tuple[sp.Symbol, ...]):
    """R^a_{b c d} for R(X,Y)Z with slots Z=b, X=c, Y=d."""
    dim = len(coords)
    tensor = [[[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                for d in range(dim):
                    tensor[a][b][c][d] = simp(
                        sp.diff(gamma[a][d][b], coords[c])
                        - sp.diff(gamma[a][c][b], coords[d])
                        + sum(
                            gamma[a][c][e] * gamma[e][d][b]
                            - gamma[a][d][e] * gamma[e][c][b]
                            for e in range(dim)
                        )
                    )
    return tensor


def inner(metric: sp.Matrix, left: sp.Matrix, right: sp.Matrix):
    return simp((left.T * metric * right)[0])


def completed_pair_frame_checks():
    T, L, beta = sp.symbols("T L beta", positive=True, real=True)
    h = sp.Matrix(
        [
            [-T**2, -T**2 * beta],
            [-T**2 * beta, L**2 - T**2 * beta**2],
        ]
    )
    U = sp.Matrix([1 / T, 0])
    N = sp.Matrix([-beta / L, 1 / L])
    ell_plus = U + N
    ell_minus = U - N
    m = simp(sp.sqrt(-h.det()))

    residuals = {
        "det_plus_T2L2": simp(h.det() + T**2 * L**2),
        "m_minus_TL": simp(m - T * L),
        "UU_plus_1": simp(inner(h, U, U) + 1),
        "NN_minus_1": simp(inner(h, N, N) - 1),
        "UN": inner(h, U, N),
        "ell_plus_null": inner(h, ell_plus, ell_plus),
        "ell_minus_null": inner(h, ell_minus, ell_minus),
        "ell_plus_normalization": simp(-inner(h, U, ell_plus) - 1),
        "ell_minus_normalization": simp(-inner(h, U, ell_minus) - 1),
    }
    assert all(value == 0 for value in residuals.values())
    return residuals


def conformal_timelive_control():
    eta, r, x, y, H, lam = sp.symbols("eta r x y H lambda", real=True)
    coords = (eta, r, x, y)
    a = sp.exp(H * eta)
    metric = sp.diag(-a**2, a**2, a**2, a**2)
    gamma = christoffel(metric, coords)
    curvature = riemann(gamma, coords)

    # Observer vertex is eta=0, where a=1.  The normalized affine outgoing ray is
    # k=a^-2(partial_eta+partial_r).
    k = sp.Matrix([a**-2, a**-2, 0, 0])
    U = sp.Matrix([a**-1, 0, 0, 0])
    screen = (
        sp.Matrix([0, 0, a**-1, 0]),
        sp.Matrix([0, 0, 0, a**-1]),
    )

    null_residual = inner(metric, k, k)
    unit_residual = simp(inner(metric, U, U) + 1)
    geodesic = []
    for mu in range(4):
        directional = sum(k[nu] * sp.diff(k[mu], coords[nu]) for nu in range(4))
        connection = sum(gamma[mu][aa][bb] * k[aa] * k[bb] for aa in range(4) for bb in range(4))
        geodesic.append(simp(directional + connection))

    screen_parallel = []
    for vector in screen:
        residual = []
        for mu in range(4):
            directional = sum(k[nu] * sp.diff(vector[mu], coords[nu]) for nu in range(4))
            connection = sum(gamma[mu][aa][bb] * k[aa] * vector[bb] for aa in range(4) for bb in range(4))
            residual.append(simp(directional + connection))
        screen_parallel.append(residual)

    omega = simp(-inner(metric, U, k))
    domega = simp(sum(k[nu] * sp.diff(omega, coords[nu]) for nu in range(4)))

    # -k^a k^b nabla_a U_b, reconstructed in coordinates without invoking a pre-existing
    # frequency formula.
    U_cov = metric * U
    contraction = sp.S.Zero
    for aa in range(4):
        for bb in range(4):
            nabla_u = sp.diff(U_cov[bb], coords[aa]) - sum(
                gamma[cc][aa][bb] * U_cov[cc] for cc in range(4)
            )
            contraction += k[aa] * k[bb] * nabla_u
    frequency_rhs = simp(-contraction)
    frequency_residual = simp(domega - frequency_rhs)

    tidal = sp.zeros(2, 2)
    for A, s_left in enumerate(screen):
        for B, s_right in enumerate(screen):
            Rvec = sp.zeros(4, 1)
            for mu in range(4):
                Rvec[mu] = simp(
                    sum(
                        curvature[mu][z][xx][yy]
                        * k[z]
                        * s_right[xx]
                        * k[yy]
                        for z in range(4)
                        for xx in range(4)
                        for yy in range(4)
                    )
                )
            tidal[A, B] = inner(metric, s_left, Rvec)
    tidal = tidal.applyfunc(simp)

    # lambda=(a^2-1)/(2H), so q=1+2H lambda=a^2 along the ray.
    q = 1 + 2 * H * lam
    D_lam = sp.sqrt(q) * sp.log(q) / (2 * H)
    tidal_lam = H**2 / q**2
    jacobi_residual = simp(sp.diff(D_lam, lam, 2) + tidal_lam * D_lam)
    vertex_D = simp(sp.limit(D_lam, lam, 0))
    vertex_Dprime = simp(sp.limit(sp.diff(D_lam, lam), lam, 0))

    Z = sp.exp(-H * eta)
    Phi = -sp.log(a)
    dA = a * eta
    Zsym = sp.symbols("Z", positive=True, real=True)
    dA_of_Z = -sp.log(Zsym) / (H * Zsym)

    assert null_residual == 0
    assert unit_residual == 0
    assert all(value == 0 for value in geodesic)
    assert all(value == 0 for row in screen_parallel for value in row)
    assert frequency_residual == 0
    assert tidal == sp.eye(2) * H**2 * sp.exp(-4 * H * eta)
    assert jacobi_residual == 0
    assert vertex_D == 0
    assert vertex_Dprime == 1
    assert simp(sp.log(Z) - Phi) == 0

    return {
        "metric_determinant": str(simp(metric.det())),
        "null_residual": str(null_residual),
        "unit_clock_residual": str(unit_residual),
        "geodesic_residual": [str(v) for v in geodesic],
        "screen_parallel_residual": [[str(v) for v in row] for row in screen_parallel],
        "omega": str(omega),
        "domega_dlambda": str(domega),
        "frequency_identity_residual": str(frequency_residual),
        "tidal_matrix": [[str(tidal[i, j]) for j in range(2)] for i in range(2)],
        "D_of_lambda": str(D_lam),
        "jacobi_residual": str(jacobi_residual),
        "vertex_D": str(vertex_D),
        "vertex_Dprime": str(vertex_Dprime),
        "Z_of_eta": str(Z),
        "Phi": str(Phi),
        "logZ_minus_Phi": str(simp(sp.log(Z) - Phi)),
        "dA_of_eta": str(dA),
        "dA_of_Z": str(dA_of_Z),
    }


def static_and_local_regressions():
    phi_s, phi_o, E, c_E = sp.symbols("phi_s phi_o E c_E", real=True, positive=True)
    omega_s = E * sp.exp(phi_s) / c_E
    omega_o = E * sp.exp(phi_o) / c_E
    static_ratio = simp(omega_s / omega_o)
    static_residual = simp(static_ratio - sp.exp(phi_s - phi_o))

    # Post-result G116 algebraic regression only.  These symbols are not used by the general
    # derivation or the time-live control above.
    R, b, qsrc, ell, n, bdot, qdot = sp.symbols("R b q ell n bdot qdot", real=True)
    p2 = sp.Rational(1, 2) * (ell - n + b**2 - bdot / 2)
    Aopt = 2 * ell + 2 * n + bdot
    vrel = b - qsrc
    vrel_dot = bdot - qdot
    zeta_direct = vrel * R + (b**2 / 2 - n + bdot / 2 - qdot) * R**2
    zeta_join = p2 * R**2 + vrel * R + (vrel_dot - Aopt / 4) * R**2
    local_residual = simp(zeta_direct - zeta_join)

    assert static_residual == 0
    assert local_residual == 0
    return {
        "static_frequency_ratio": str(static_ratio),
        "static_recovery_residual": str(static_residual),
        "g116_post_result_regression_residual": str(local_residual),
    }


def full_matrix_screen_regression():
    """Post-result G188 regression: the joined screen must remain a full matrix."""
    lam = sp.symbols("lambda", real=True)
    tide = sp.Matrix([[-2, -2], [-2, -2]])
    diagonal = lam / 2 + sp.sinh(2 * lam) / 4
    cross = -lam / 2 + sp.sinh(2 * lam) / 4
    D = sp.Matrix([[diagonal, cross], [cross, diagonal]])
    residual = (sp.diff(D, lam, 2) + tide * D).applyfunc(simp)
    vertex = D.subs(lam, 0)
    vertex_prime = sp.diff(D, lam).subs(lam, 0)
    assert residual == sp.zeros(2)
    assert vertex == sp.zeros(2)
    assert vertex_prime == sp.eye(2)
    assert simp(cross - lam**3 / 3).series(lam, 0, 5).removeO() == 0
    return {
        "tidal": [[str(tide[i, j]) for j in range(2)] for i in range(2)],
        "D": [[str(D[i, j]) for j in range(2)] for i in range(2)],
        "residual": [[str(residual[i, j]) for j in range(2)] for i in range(2)],
        "offdiagonal_series": str(sp.series(cross, lam, 0, 5)),
    }


def main():
    result = {
        "landing": "COMPLETED_PAIR_TIMELIVE_FREQUENCY_SCREEN_JOINT_EVALUATOR_DERIVED_CONDITIONALLY",
        "pair_frame_residuals": {key: str(value) for key, value in completed_pair_frame_checks().items()},
        "time_live_control": conformal_timelive_control(),
        "full_matrix_screen_regression": full_matrix_screen_regression(),
        "regressions": static_and_local_regressions(),
        "scope": {
            "p1_used": False,
            "phi_of_R_used": False,
            "xmax_used": False,
            "radiative_transfer_derived": False,
            "physical_history_selected": False,
        },
    }
    if os.environ.get("G190_NO_WRITE") != "1":
        output = Path(__file__).with_name("PRODUCTION_RESULT.json")
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
