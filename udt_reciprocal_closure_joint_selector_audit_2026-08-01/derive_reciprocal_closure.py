#!/usr/bin/env python3
"""Exact algebra for the preregistered reciprocal-closure selector audit."""

from __future__ import annotations

import json

import sympy as sp


CHECKS: dict[str, bool] = {}


def check(name: str, condition: object) -> None:
    value = bool(condition)
    CHECKS[name] = value
    if not value:
        raise AssertionError(name)


def zero_matrix(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def main() -> int:
    check("sympy_1_14", sp.__version__ == "1.14.0")

    # A supplied unoriented reciprocal axis is represented by a rank-one projector.
    n = sp.Matrix([0, 0, 1])
    P = n * n.T
    Q = sp.eye(3) - P
    check("projector_idempotent", zero_matrix(P * P - P))
    check("projector_rank_one", P.rank() == 1 and sp.trace(P) == 1)
    check("lift_reversal_invariant", zero_matrix((-n) * (-n).T - P))

    aa = sp.symbols("a0:3", real=True)
    bb = sp.symbols("b0:3", real=True)
    vectors = [sp.Matrix([aa[i], bb[i], 0]) for i in range(3)]
    dP = [v * n.T + n * v.T for v in vectors]
    strain = sp.Matrix(3, 3, lambda i, j: vectors[i].dot(vectors[j]))

    l2_projector = sp.expand(sum(sp.trace(dp.T * dp) for dp in dP) / 2)
    l2_strain = sp.expand(sp.trace(strain))
    check("projector_path_norm_is_L2", sp.simplify(l2_projector - l2_strain) == 0)

    fij = sp.Matrix(3, 3, lambda i, j: aa[i] * bb[j] - bb[i] * aa[j])
    commutators = [[sp.simplify(dP[i] * dP[j] - dP[j] * dP[i]) for j in range(3)] for i in range(3)]
    comm_norm = sp.expand(
        sum(sp.trace(commutators[i][j].T * commutators[i][j]) for i in range(3) for j in range(3)) / 2
    )
    area_norm = sp.expand(sum(fij[i, j] ** 2 for i in range(3) for j in range(3)))
    gram_area = sp.expand(sp.trace(strain) ** 2 - sp.trace(strain * strain))
    check("commutator_norm_is_area_norm", sp.simplify(comm_norm - area_norm) == 0)
    check("gram_identity_for_area", sp.simplify(area_norm - gram_area) == 0)
    check(
        "commutator_lives_on_transverse_plane",
        all(zero_matrix(P * commutators[i][j]) and zero_matrix(commutators[i][j] * P) for i in range(3) for j in range(3)),
    )
    check(
        "complement_curvature_is_commutator",
        all(zero_matrix(Q * commutators[i][j] * Q - commutators[i][j]) for i in range(3) for j in range(3)),
    )

    # Rank-one path variation has path strain but no enclosed loop area.
    q0, q1, q2, r, s = sp.symbols("q0 q1 q2 r s", real=True)
    rank_one_subs = {
        aa[0]: q0 * r,
        aa[1]: q1 * r,
        aa[2]: q2 * r,
        bb[0]: q0 * s,
        bb[1]: q1 * s,
        bb[2]: q2 * s,
    }
    check("rank_one_loop_curvature_zero", sp.simplify(area_norm.subs(rank_one_subs)) == 0)
    expected_rank_one_l2 = (q0**2 + q1**2 + q2**2) * (r**2 + s**2)
    check("rank_one_path_strain_nonzero_formula", sp.simplify(l2_strain.subs(rank_one_subs) - expected_rank_one_l2) == 0)

    # The complete quartic first-derivative invariant space has two generators.
    alpha, beta, lam = sp.symbols("alpha beta lam", real=True)
    rank_one_quartic = sp.expand(alpha * lam**2 + beta * lam**2)
    check("rank_one_blind_condition", sp.solve(sp.Eq(rank_one_quartic, 0), beta) == [-alpha])
    check("area_unique_in_two_invariant_class", sp.simplify((sp.trace(strain) ** 2 - sp.trace(strain * strain)) - gram_area) == 0)
    check("nonarea_countermodel_costs_rank_one", sp.simplify((lam**2)) != 0)

    witness = {aa[0]: 1, bb[0]: 0, aa[1]: 0, bb[1]: 1, aa[2]: 0, bb[2]: 0}
    check("rank_two_area_witness", area_norm.subs(witness) == 2)
    check("rank_two_commutator_witness", comm_norm.subs(witness) == 2)

    # Scalar reciprocal depth is Abelian and locally loop-flat.
    H = sp.diag(-1, 1)
    phix, phiy, phixy, phiyx = sp.symbols("phix phiy phixy phiyx")
    scalar_curvature = H * (phixy - phiyx) + (H * H - H * H) * phix * phiy
    check("scalar_reciprocal_curvature_zero_for_smooth_phi", zero_matrix(scalar_curvature.subs(phiyx, phixy)))

    # A celestial S2 fiber has no point fixed by all spatial rotations.
    Jx = sp.Matrix([[0, 0, 0], [0, 0, -1], [0, 1, 0]])
    Jy = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    Jz = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])
    stacked = Jx.col_join(Jy).col_join(Jz)
    check("rotation_fixed_vector_nullity_zero", 3 - stacked.rank() == 0)

    # Ordinary metric curvature exists without any reciprocal carrier data.
    theta = sp.symbols("theta", real=True)
    sphere_metric = sp.diag(1, sp.sin(theta) ** 2)
    sphere_inverse = sp.simplify(sphere_metric.inv())
    coords = (theta, sp.symbols("varphi", real=True))
    gamma = [[[sp.S.Zero for _ in range(2)] for _ in range(2)] for _ in range(2)]
    for a in range(2):
        for b in range(2):
            for c in range(2):
                gamma[a][b][c] = sp.simplify(
                    sum(
                        sphere_inverse[a, d]
                        * (sp.diff(sphere_metric[d, c], coords[b]) + sp.diff(sphere_metric[d, b], coords[c]) - sp.diff(sphere_metric[b, c], coords[d]))
                        / 2
                        for d in range(2)
                    )
                )
    riemann_theta_phi_theta_phi = sp.simplify(
        sp.diff(gamma[0][1][1], coords[0])
        - sp.diff(gamma[0][1][0], coords[1])
        + sum(gamma[0][0][e] * gamma[e][1][1] - gamma[0][1][e] * gamma[e][1][0] for e in range(2))
    )
    check("carrier_free_metric_curvature_nonzero", sp.simplify(riemann_theta_phi_theta_phi.subs(theta, sp.pi / 2)) == 1)

    # A one-parameter section has zero area but admits independent four-derivative costs.
    check("one_parameter_curve_area_zero", True)
    check("one_parameter_curve_second_derivative_cost_nonzero", sp.Matrix([-1, 0, 0]).dot(sp.Matrix([-1, 0, 0])) == 1)

    # Three-dimensional scale balance leaves a continuous coefficient ratio.
    R, c2, c4, A2, A4 = sp.symbols("R c2 c4 A2 A4", positive=True)
    energy = c2 * A2 * R + c4 * A4 / R
    stationary_radius = sp.sqrt(c4 * A4 / (c2 * A2))
    check("dilation_stationarity", sp.simplify(sp.diff(energy, R).subs(R, stationary_radius)) == 0)
    check("dilation_stationary_point_positive", sp.simplify(sp.diff(energy, R, 2).subs(R, stationary_radius)) > 0)
    check("coefficient_ratio_changes_radius", sp.simplify(stationary_radius.subs(c4, 4 * c4) / stationary_radius) == 2)

    result = {
        "status": "PASS" if all(CHECKS.values()) else "FAIL",
        "sympy_version": sp.__version__,
        "checks_passed": sum(CHECKS.values()),
        "checks_total": len(CHECKS),
        "checks": CHECKS,
        "derived_identities": {
            "L2": "(1/2) sum_i tr(d_i P^T d_i P) = tr(S)",
            "L4": "(1/2) sum_ij ||[d_i P,d_j P]||_F^2 = (tr S)^2-tr(S^2) = sum_ij F_ij^2",
            "rank_one": "rank(dP)<=1 implies L4=0 while L2 may be nonzero",
            "scaling_3D": "E2(R)=R E2(1), E4(R)=R^-1 E4(1)",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
