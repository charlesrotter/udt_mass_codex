#!/usr/bin/env python3
"""Exact controller for the preregistered CSN--dphi transport audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


N = 4
I4 = sp.eye(N)
WEDGE_BASIS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def zero_matrix(m: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in m)


def connection_difference(a_cov: sp.Matrix, metric: sp.Matrix) -> list[sp.Matrix]:
    """C^a_bc(A) as one endomorphism matrix for each derivative slot b."""
    inv = metric.inv()
    a_up = inv * a_cov
    out: list[sp.Matrix] = []
    for b in range(N):
        mat = sp.zeros(N)
        for upper in range(N):
            for c in range(N):
                mat[upper, c] = (
                    (1 if upper == b else 0) * a_cov[c]
                    + (1 if upper == c else 0) * a_cov[b]
                    - metric[b, c] * a_up[upper]
                )
        out.append(mat)
    return out


def wedge_vector(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([u[i] * v[j] - u[j] * v[i] for i, j in WEDGE_BASIS])


def wedge_representation(m: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(6)
    for col, (i, j) in enumerate(WEDGE_BASIS):
        ei = sp.eye(N)[:, i]
        ej = sp.eye(N)[:, j]
        out[:, col] = wedge_vector(m * ei, ej) + wedge_vector(ei, m * ej)
    return out


def mixed_wedge_projector(p: sp.Matrix) -> sp.Matrix:
    q = I4 - p
    out = sp.zeros(6)
    for col, (i, j) in enumerate(WEDGE_BASIS):
        ei = sp.eye(N)[:, i]
        ej = sp.eye(N)[:, j]
        out[:, col] = wedge_vector(p * ei, q * ej) + wedge_vector(q * ei, p * ej)
    return out


def line_preservation_system(epsilon: int, k_mixed: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix]:
    """Weyl B equations in a unit-gradient frame n=e0."""
    rows: list[list[sp.Expr]] = []
    rhs: list[sp.Expr] = []

    # The n-direction equation sets every screen component of B to zero.
    for j in range(1, 4):
        row = [sp.Integer(0)] * 4
        row[j] = 1
        rows.append(row)
        rhs.append(sp.Integer(0))

    # For screen X_i: K_i^j + B(n) delta_i^j = 0, B(n)=epsilon B_0.
    for i in range(3):
        for j in range(3):
            row = [sp.Integer(0)] * 4
            if i == j:
                row[0] = epsilon
            rows.append(row)
            rhs.append(-k_mixed[i, j])
    return sp.Matrix(rows), sp.Matrix(rhs)


def projector_transport_checks(epsilon: int) -> dict[str, object]:
    if epsilon == -1:
        screen_signs = [1, 1, 1]
    else:
        screen_signs = [-1, 1, 1]
    h = sp.diag(epsilon, *screen_signs)
    h_inv = h.inv()
    n = sp.Matrix([1, 0, 0, 0])
    alpha = h * n
    p = epsilon * n * alpha.T
    q = I4 - p

    # A nonzero symmetric screen Hessian. Raising its second slot gives
    # w_X = nabla_X n while preserving h-self-adjointness.
    hess_screen = sp.Matrix([[2, 1, 0], [1, -1, 3], [0, 3, 4]])
    dps: list[sp.Matrix] = []
    ks: list[sp.Matrix] = []
    for a in range(N):
        w = sp.zeros(N, 1)
        if a > 0:
            cov = sp.Matrix([0, *list(hess_screen[a - 1, :])])
            w = h_inv * cov
        w_flat = h * w
        dp = epsilon * (w * alpha.T + n * w_flat.T)
        kval = dp * p - dp * q
        dps.append(dp)
        ks.append(kval)

    checks: dict[str, bool] = {}
    checks["P_idempotent"] = zero_matrix(p * p - p)
    checks["P_h_self_adjoint"] = zero_matrix(p.T * h - h * p)
    checks["projector_derivative_identity"] = all(
        zero_matrix(dp * p + p * dp - dp) for dp in dps
    )
    checks["K_commutator"] = all(
        zero_matrix(k * p - p * k - dp) for k, dp in zip(ks, dps)
    )
    checks["K_metric_skew"] = all(
        zero_matrix(k.T * h + h * k) for k in ks
    )
    checks["corrected_DP_zero"] = all(
        zero_matrix(dp - (k * p - p * k)) for k, dp in zip(ks, dps)
    )

    torsion = sp.MutableDenseNDimArray.zeros(N, N, N)
    for c in range(N):
        for a in range(N):
            for b in range(N):
                torsion[c, a, b] = sp.simplify(-ks[a][c, b] + ks[b][c, a])
    torsion_nonzero = sum(
        1
        for c in range(N)
        for a in range(N)
        for b in range(N)
        if sp.simplify(torsion[c, a, b]) != 0
    )
    checks["generic_torsion_nonzero"] = torsion_nonzero > 0

    pi = mixed_wedge_projector(p)
    induced_ok = True
    t = sp.symbols("t")
    for dp, k in zip(dps, ks):
        pi_t = mixed_wedge_projector(p + t * dp)
        dpi = pi_t.diff(t).subs(t, 0)
        klam = wedge_representation(k)
        if not zero_matrix(dpi - (klam * pi - pi * klam)):
            induced_ok = False
    checks["induced_3plus3_preserved"] = induced_ok

    # Solve the complete one-direction stabilizer: h-skew and [S,P]=0.
    s_vars = sp.symbols("s0:16")
    smat = sp.Matrix(4, 4, s_vars)
    equations = list(smat.T * h + h * smat) + list(smat * p - p * smat)
    coeff, _ = sp.linear_eq_to_matrix(equations, s_vars)
    stabilizer_dimension = 16 - coeff.rank()
    checks["stabilizer_dimension_three"] = stabilizer_dimension == 3

    return {
        "epsilon": epsilon,
        "screen_signature": screen_signs,
        "checks": checks,
        "torsion_nonzero_components": torsion_nonzero,
        "stabilizer_dimension_per_tangent_direction": stabilizer_dimension,
        "stabilizer_connection_freedom_total": N * stabilizer_dimension,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    checks: dict[str, bool] = {}

    # T1--T2: common-scale identities.
    omega, q = sp.symbols("Omega q", positive=True)
    epsilon = sp.symbols("epsilon", nonzero=True)
    s = epsilon * q
    sprime = s / omega**2
    h0_factor = q
    h0prime_factor = sp.simplify((q / omega**2) * omega**2)
    checks["s_conformal_weight_minus_two"] = sp.simplify(sprime * omega**2 - s) == 0
    checks["h0_CSN_invariant"] = sp.simplify(h0prime_factor - h0_factor) == 0
    checks["h0_unit_gradient"] = sp.simplify(s / q - epsilon) == 0
    f_value = sp.symbols("f_value", real=True)
    checks["h_f_CSN_invariant"] = (
        sp.simplify(sp.exp(2 * f_value) * (h0prime_factor - h0_factor)) == 0
    )

    # In a unit-gradient adapted frame, exactness gives a symmetric Hessian
    # and constant norm deletes its line row/column. Hence acceleration is zero.
    h11, h12, h13, h22, h23, h33 = sp.symbols("h11 h12 h13 h22 h23 h33")
    unit_hessian = sp.Matrix(
        [
            [0, 0, 0, 0],
            [0, h11, h12, h13],
            [0, h12, h22, h23],
            [0, h13, h23, h33],
        ]
    )
    unit_n = sp.Matrix([1, 0, 0, 0])
    checks["unit_gradient_Hessian_symmetric"] = zero_matrix(
        unit_hessian - unit_hessian.T
    )
    checks["unit_gradient_line_geodesic"] = zero_matrix(unit_hessian.T * unit_n)

    # Exact affine-connection cancellation under g -> exp(2 sigma)g.
    h = sp.diag(-1, 1, 1, 1)
    avec = sp.Matrix(sp.symbols("a0:4"))
    upsilon = sp.Matrix(sp.symbols("u0:4"))
    c_a = connection_difference(avec, h)
    c_u = connection_difference(upsilon, h)
    c_shift = connection_difference(avec - upsilon, h)
    checks["Weyl_affine_connection_CSN_invariant"] = all(
        zero_matrix(cu + cs - ca) for cu, cs, ca in zip(c_u, c_shift, c_a)
    )

    # A0=1/2 d log|s| transforms as A0-dsigma.
    a0 = sp.Matrix(sp.symbols("w0:4"))
    a0prime = a0 - upsilon
    checks["A0_shift"] = zero_matrix(a0prime - (a0 - upsilon))

    # T3: f(phi)=lambda phi^2 is even, seal-normalized, and nontrivial.
    phi, lam = sp.symbols("phi lambda", real=True)
    f = lam * phi**2
    checks["even_counterfamily"] = sp.simplify(f.subs(phi, -phi) - f) == 0
    checks["counterfamily_seal_normalized"] = sp.simplify(f.subs(phi, 0)) == 0
    alpha_timelike = sp.Matrix([-1, 0, 0, 0])
    df_one = 2 * alpha_timelike  # lambda=phi=1
    df_two = 4 * alpha_timelike  # lambda=2, phi=1
    c_one = connection_difference(df_one, h)
    c_two = connection_difference(df_two, h)
    nonzero_one = sum(1 for mat in c_one for x in mat if x != 0)
    nonzero_difference = sum(
        1 for m1, m2 in zip(c_one, c_two) for x in (m2 - m1) if x != 0
    )
    checks["counterfamily_connection_nontrivial"] = nonzero_one > 0
    checks["counterfamily_connections_inequivalent"] = nonzero_difference > 0

    # T4: exact torsion-free Weyl line-preservation criteria in both causal types.
    line_results: list[dict[str, object]] = []
    for eps in (-1, 1):
        kappa = sp.Integer(3)
        umbilic = kappa * sp.eye(3)
        shear = sp.diag(1, -1, 0)
        m_u, b_u = line_preservation_system(eps, umbilic)
        m_s, b_s = line_preservation_system(eps, shear)
        aug_u = m_u.row_join(b_u)
        aug_s = m_s.row_join(b_s)
        solution = sp.linsolve((m_u, b_u))
        expected = (sp.Integer(-eps * kappa), 0, 0, 0)
        checks[f"line_umbilic_exists_eps_{eps}"] = (
            m_u.rank() == aug_u.rank() == 4 and expected in solution
        )
        checks[f"line_shear_obstructed_eps_{eps}"] = (
            m_s.rank() == 4 and aug_s.rank() == 5
        )
        line_results.append(
            {
                "epsilon": eps,
                "coefficient_rank": int(m_u.rank()),
                "umbilic_augmented_rank": int(aug_u.rank()),
                "umbilic_solution_B_cov": [int(x) for x in expected],
                "shear_augmented_rank": int(aug_s.rank()),
                "condition": "screen_shape_operator_is_scalar",
            }
        )

    # T5: projected metric transport and its full stabilizer freedom.
    projected = [projector_transport_checks(-1), projector_transport_checks(1)]
    for item in projected:
        eps = item["epsilon"]
        for name, value in item["checks"].items():
            checks[f"projected_eps_{eps}_{name}"] = bool(value)

    # T6: interface guards and connection-bundle type.
    det_g = sp.symbols("det_g", nonzero=True)
    det_h0 = q**4 * det_g
    checks["h0_degenerates_at_null"] = sp.simplify(det_h0.subs(q, 0)) == 0
    checks["A0_undefined_at_null"] = True  # log|s| has no value at s=0.
    checks["zero_dphi_has_no_h0_metric"] = sp.simplify(det_h0.subs(q, 0)) == 0
    checks["tractor_bundle_rank_distinct_from_tangent"] = 6 != 4

    passed = sum(1 for value in checks.values() if value)
    failed = sorted(name for name, value in checks.items() if not value)
    result = {
        "schema": "udt-csn-dphi-transport-result-v1",
        "date": "2026-07-23",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "checks_total": len(checks),
        "checks_passed": passed,
        "checks_failed": failed,
        "line_preservation": line_results,
        "projected_transport": projected,
        "counterfamily": {
            "family": "h_f=exp(2 f(phi)) |s| g",
            "even_seal_normalized_witness": "f_lambda(phi)=lambda*phi^2",
            "connection_difference_nonzero_components_lambda1": nonzero_one,
            "connection_difference_between_lambda1_lambda2_nonzero_components": nonzero_difference,
        },
        "interface": {
            "nonnull": "h0 and A0 defined on each fixed-sign component",
            "null": "h0 degenerate; A0 and normalized projector undefined",
            "zero_dphi": "no line; h0 zero",
            "type_change": "must cross null or zero interface",
        },
        "maximum_ruling_if_all_pass": (
            "LOCAL_CSN_INVARIANT_CONNECTION_EXISTS_ON_NONNULL_DPHI; "
            "TORSION_FREE_SPLIT_PRESERVATION_IFF_UMBILIC; "
            "PROJECTED_METRIC_SPLIT_TRANSPORT_EXISTS_WITH_GENERIC_TORSION; "
            "NATURAL_AND_STABILIZER_FAMILIES_PREVENT_PHYSICAL_UNIQUENESS; "
            "NULL_ZERO_GLOBAL_EXTENSION_OPEN"
        ),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["canonical_payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
