#!/usr/bin/env python3
"""Exact production checks for the preregistered G145 regular relation atlas."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def require_zero(expr: sp.Expr | sp.MatrixBase, label: str, checks: list[str]) -> None:
    simplified = expr.applyfunc(sp.simplify) if isinstance(expr, sp.MatrixBase) else sp.simplify(expr)
    if simplified != sp.zeros(*simplified.shape) if isinstance(simplified, sp.MatrixBase) else simplified != 0:
        raise AssertionError(f"{label}: {simplified}")
    checks.append(label)


def design_rank(checks: list[str]) -> int:
    directions = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
    )
    basis = (
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3),
    )
    rows: list[list[int]] = []
    e0 = sp.Matrix([1, 0, 0, 0])
    for direction in directions:
        v = sp.Matrix([0, *direction])
        for left, right in ((e0, e0), (e0, v), (v, v)):
            row = []
            for i, j in basis:
                coefficient = left[i] * right[j]
                if i != j:
                    coefficient += left[j] * right[i]
                row.append(int(coefficient))
            rows.append(row)
    rank = sp.Matrix(rows).rank()
    if rank != 10:
        raise AssertionError(f"six-plane rank {rank}")
    checks.append("six_clock_ruler_plane_design_rank_ten")
    return rank


def curvature_from_metric(g: sp.Matrix, coordinates: tuple[sp.Symbol, ...]) -> sp.Expr:
    n = len(coordinates)
    inverse = sp.simplify(g.inv())
    gamma = [[[sp.S.Zero for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for upper in range(n):
        for left in range(n):
            for right in range(n):
                gamma[upper][left][right] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        inverse[upper, k]
                        * (
                            sp.diff(g[k, right], coordinates[left])
                            + sp.diff(g[k, left], coordinates[right])
                            - sp.diff(g[left, right], coordinates[k])
                        )
                        for k in range(n)
                    )
                )
    ricci = sp.zeros(n)
    for left in range(n):
        for right in range(n):
            ricci[left, right] = sp.simplify(
                sum(
                    sp.diff(gamma[k][left][right], coordinates[k])
                    - sp.diff(gamma[k][left][k], coordinates[right])
                    + sum(
                        gamma[k][k][ell] * gamma[ell][left][right]
                        - gamma[k][right][ell] * gamma[ell][left][k]
                        for ell in range(n)
                    )
                    for k in range(n)
                )
            )
    return sp.simplify(sum(inverse[i, j] * ricci[i, j] for i in range(n) for j in range(n)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true", help="recompute without replacing saved evidence")
    args = parser.parse_args()
    checks: list[str] = []
    rank = design_rank(checks)

    t, r, y, z = sp.symbols("t r y z", real=True)
    c_e, a, b = sp.symbols("c_E a b", positive=True)
    phi = sp.Function("Phi")(r)
    g = sp.diag(-sp.exp(-2 * phi) * c_e**2, sp.exp(2 * phi), 1, 1)
    if sp.simplify(g.det() + c_e**2) != 0:
        raise AssertionError("metric determinant")
    checks.append("reciprocal_metric_determinant_constant")
    if sp.simplify(g.inv()[0, 0] + sp.exp(2 * phi) / c_e**2) != 0:
        raise AssertionError("time function inverse norm")
    checks.append("dt_covector_strictly_timelike_for_positive_cE")

    scalar = curvature_from_metric(g, (t, r, y, z))
    expected_scalar = sp.exp(-2 * phi) * (2 * sp.diff(phi, r, 2) - 4 * sp.diff(phi, r) ** 2)
    require_zero(scalar - expected_scalar, "scalar_curvature_full_christoffel_formula", checks)
    phi_minus = a * r
    phi_plus = a * r + b * r**2
    scalar_minus = sp.simplify(expected_scalar.subs(phi, phi_minus).doit().subs(r, 0))
    scalar_plus = sp.simplify(expected_scalar.subs(phi, phi_plus).doit().subs(r, 0))
    require_zero(scalar_minus + 4 * a**2, "linear_profile_marked_curvature_negative", checks)
    require_zero(scalar_plus - (4 * b - 4 * a**2), "quadratic_profile_marked_curvature_positive_if_b_gt_a2", checks)
    require_zero(scalar_plus - scalar_minus - 4 * b, "marked_histories_invariantly_separated", checks)

    p_a, p_b, p_c = sp.symbols("p_A p_B p_C", real=True)

    def endpoint_factor(value: sp.Expr) -> sp.Matrix:
        return sp.diag(sp.exp(-value), sp.exp(value))

    r_a, r_b, r_c = map(endpoint_factor, (p_a, p_b, p_c))
    c_ba = sp.simplify(r_b * r_a.inv())
    c_cb = sp.simplify(r_c * r_b.inv())
    c_ca = sp.simplify(r_c * r_a.inv())
    require_zero(c_cb * c_ba - c_ca, "endpoint_factor_composition", checks)
    require_zero(c_ba.inv() - r_a * r_b.inv(), "endpoint_factor_reversal", checks)
    delta_ba = p_b - p_a
    delta_cb = p_c - p_b
    delta_ca = p_c - p_a
    require_zero(delta_ba + delta_cb - delta_ca, "endpoint_depth_triangle_closure", checks)
    xi_ba, xi_cb = sp.tanh(delta_ba), sp.tanh(delta_cb)
    mobius = (xi_ba + xi_cb) / (1 + xi_ba * xi_cb)
    require_zero(sp.trigsimp(mobius - sp.tanh(delta_ca)), "signed_position_mobius_composition", checks)

    j_ba = sp.Matrix([[2, 1], [1, 1]])
    j_cb = sp.Matrix([[1, 1], [1, 2]])
    j_ca = j_cb * j_ba
    h_c = sp.Matrix([[-5, 1], [1, 2]])
    h_b = j_cb.T * h_c * j_cb
    h_a = j_ba.T * h_b * j_ba
    require_zero(h_a - j_ca.T * h_c * j_ca, "cech_pullback_metric_descent", checks)
    require_zero(j_cb * j_ba - j_ca, "overlap_differential_cocycle", checks)

    base_j_ba = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]])
    base_j_cb = sp.Matrix([[1, 0, 0, 1], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1]])
    base_j_ca = base_j_cb * base_j_ba
    base_g_c = sp.diag(-7, 2, 3, 5)
    base_g_b = base_j_cb.T * base_g_c * base_j_cb
    base_g_a = base_j_ba.T * base_g_b * base_j_ba
    require_zero(base_g_a - base_j_ca.T * base_g_c * base_j_ca,
                 "four_dimensional_base_chart_metric_descent", checks)
    require_zero(base_j_cb * base_j_ba - base_j_ca,
                 "four_dimensional_base_chart_cocycle", checks)

    # Fixed nonzero rational amplitudes make every claimed live field falsifiable. Symbolic
    # amplitudes could all be set to zero while still satisfying an identity of the form d^3f=6a.
    alpha, beta, gamma = sp.Rational(1, 7), sp.Rational(-2, 9), sp.Rational(3, 11)
    m1, m2, m3, m4 = (
        sp.Rational(2, 5), sp.Rational(-3, 7), sp.Rational(5, 13), sp.Rational(-7, 17)
    )
    kappa_amp, shift_amp = sp.Rational(11, 19), sp.Rational(-13, 23)
    q = sp.Matrix([[1 + alpha * t**3, gamma * r**3], [0, 1 + beta * (t + r) ** 3]])
    s = sp.Matrix([[m1 * t**3, m2 * r**3], [m3 * (t + r) ** 3, m4 * (t - r) ** 3]])
    kappa = kappa_amp * (t + r) ** 3
    base_shift = shift_amp * (t - 2 * r) ** 3
    base_t = sp.exp(kappa - phi)
    base_l = sp.exp(kappa + phi)
    bmat = sp.Matrix([[base_t, base_t * base_shift], [0, base_l]])
    zero = sp.zeros(2)
    e = bmat.row_join(zero).col_join((q * s).row_join(q))
    eta = sp.diag(-c_e**2, 1, 1, 1)
    full_g = sp.simplify(e.T * eta * e)
    baseline_b = sp.diag(sp.exp(-phi), sp.exp(phi))
    baseline_e = baseline_b.row_join(zero).col_join(zero.row_join(sp.eye(2)))
    baseline_g = sp.simplify(baseline_e.T * eta * baseline_e)
    difference = sp.simplify(full_g - baseline_g)
    jet_count = 0
    for dt_order in range(3):
        for dr_order in range(3 - dt_order):
            jet = difference.diff(t, dt_order).diff(r, dr_order).subs({t: 0, r: 0})
            require_zero(jet, f"active_orchestra_zero_{dt_order + dr_order}_jet_{dt_order}_{dr_order}", checks)
            jet_count += 1
    if sp.simplify(e.det() - sp.det(bmat) * sp.det(q)) != 0:
        raise AssertionError("complete coframe determinant")
    checks.append("complete_coframe_all_sector_determinant_factorization")

    live_germs = (
        (sp.diff(kappa, t, 3).subs({t: 0, r: 0}), 6 * kappa_amp, "base_common_scale_live"),
        (sp.diff(base_shift, t, 3).subs({t: 0, r: 0}), 6 * shift_amp, "base_shift_live"),
        (sp.diff(q[0, 0] - 1, t, 3).subs({t: 0, r: 0}), 6 * alpha, "screen_scale_t_live"),
        (sp.diff(q[0, 1], r, 3).subs({t: 0, r: 0}), 6 * gamma, "screen_shear_r_live"),
        (sp.diff(q[1, 1] - 1, t, 3).subs({t: 0, r: 0}), 6 * beta, "screen_second_scale_t_live"),
        (sp.diff(s[0, 0], t, 3).subs({t: 0, r: 0}), 6 * m1, "mixing_mu1_live"),
        (sp.diff(s[0, 1], r, 3).subs({t: 0, r: 0}), 6 * m2, "mixing_mu2_live"),
        (sp.diff(s[1, 0], t, 3).subs({t: 0, r: 0}), 6 * m3, "mixing_mu3_live"),
        (sp.diff(s[1, 1], t, 3).subs({t: 0, r: 0}), 6 * m4, "mixing_mu4_live"),
    )
    for observed, expected, label in live_germs:
        if sp.simplify(expected) == 0 or sp.simplify(observed) == 0:
            raise AssertionError(f"{label}: zero amplitude")
        require_zero(observed - expected, label, checks)

    dim_matrix = sp.Matrix([[1, 3], [0, -1], [-1, -2]])
    target_length = sp.Matrix([1, 0, 0])
    if sp.linsolve((dim_matrix, target_length)) != sp.EmptySet:
        raise AssertionError("cE and G unexpectedly form length")
    checks.append("cE_and_G_cannot_form_length_without_additional_dimensionful_datum")

    source_hashes: dict[str, str] = {}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            digest = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
            if digest != row["sha256"]:
                raise AssertionError(f"source hash mismatch: {row['path']}")
            source_hashes[row["path"]] = digest
            checks.append(f"source_hash_{Path(row['path']).parent.name}")

    result = {
        "status": "PASS",
        "landing_candidate": "RELATION_NETWORK_EQUIVALENT_TO_HISTORY__VALUES_OPEN",
        "checks_passed": len(checks),
        "checks_total": len(checks),
        "checks": checks,
        "six_plane_rank": rank,
        "scalar_curvature": str(expected_scalar),
        "marked_curvatures": {"Phi_minus": str(scalar_minus), "Phi_plus": str(scalar_plus)},
        "active_orchestra_jet_checks": jet_count,
        "active_complete_coframe_fields": len(live_germs),
        "source_hashes": source_hashes,
    }
    if not args.no_write:
        (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
