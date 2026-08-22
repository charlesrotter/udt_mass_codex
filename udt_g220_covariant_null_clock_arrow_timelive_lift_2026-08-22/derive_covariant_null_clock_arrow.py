#!/usr/bin/env python3
"""Exact symbolic derivation for the bounded G220 null clock-arrow lift."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


if not __debug__:
    raise RuntimeError("G220 evidence must run with Python assertions enabled; -O is forbidden")


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def check_manifest() -> int:
    rows = HERE.joinpath("SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
    for row in rows:
        expected, relative = row.split("\t")
        actual = hashlib.sha256(ROOT.joinpath(relative).read_bytes()).hexdigest()
        assert actual == expected, relative
    return len(rows)


def derive() -> dict[str, object]:
    checks: dict[str, bool] = {}

    # Abstract implicit-incidence and affine-frequency derivation.
    sigma_a_u, sigma_b_u = sp.symbols("sigma_a_u sigma_b_u", nonzero=True, real=True)
    k_a_u, k_b_u, affine_span, affine_scale = sp.symbols(
        "k_a_u k_b_u affine_span affine_scale", nonzero=True, real=True
    )
    r_implicit = -sigma_a_u / sigma_b_u
    r_from_k = sp.simplify(
        r_implicit.subs({sigma_a_u: -affine_span * k_a_u, sigma_b_u: affine_span * k_b_u})
    )
    omega_a, omega_b = -k_a_u, -k_b_u
    checks["implicit_null_incidence"] = sp.simplify(sigma_a_u + sigma_b_u * r_implicit) == 0
    checks["world_function_to_affine_tangent"] = sp.simplify(r_from_k - k_a_u / k_b_u) == 0
    checks["affine_frequency_ratio"] = sp.simplify(r_from_k - omega_a / omega_b) == 0
    checks["affine_rescaling_cancels"] = (
        sp.simplify((affine_scale * k_a_u) / (affine_scale * k_b_u) - r_from_k) == 0
    )

    # General time-dependent upper-triangular 1+1 pair metric at one point.
    N, A, beta = sp.symbols("N A beta", positive=True, real=True)
    c_plus, c_minus = A - N * beta, A + N * beta
    metric = sp.Matrix([[-N**2, -N**2 * beta], [-N**2 * beta, A**2 - N**2 * beta**2]])
    right_dx_dt = N / c_plus
    left_dx_dt = -N / c_minus
    right = sp.Matrix([1, right_dx_dt])
    left = sp.Matrix([1, left_dx_dt])
    checks["pair_metric_determinant"] = sp.factor(metric.det()) == -N**2 * A**2
    checks["right_tangent_is_null"] = sp.factor((right.T * metric * right)[0]) == 0
    checks["left_tangent_is_null"] = sp.factor((left.T * metric * left)[0]) == 0

    # Endpoint differentiation of integral N/Cplus dt = L.
    n_a, n_b, cp_a, cp_b = sp.symbols("N_A N_B Cp_A Cp_B", positive=True, real=True)
    dt_b_dt_a = n_a * cp_b / (cp_a * n_b)
    r_pair = sp.simplify(n_b * dt_b_dt_a / n_a)
    checks["incidence_integral_first_jet"] = sp.simplify(
        -n_a / cp_a + n_b * dt_b_dt_a / cp_b
    ) == 0
    checks["proper_clock_slope"] = sp.simplify(r_pair - cp_b / cp_a) == 0
    checks["lapse_cancels_after_proper_clock"] = not r_pair.has(n_a, n_b)

    # Same event relation pulled back with y=tau_A.
    dt_a_dy = 1 / n_a
    dt_b_dy = sp.simplify(dt_b_dt_a * dt_a_dy)
    target_clock_norm = sp.simplify(-n_b**2 * dt_b_dy**2)
    completed_t = sp.sqrt(-target_clock_norm)
    checks["source_clock_is_unit"] = sp.simplify(-n_a**2 * dt_a_dy**2 + 1) == 0
    checks["target_pullback_norm"] = sp.simplify(target_clock_norm + r_pair**2) == 0
    checks["completed_clock_equals_incidence_slope"] = sp.simplify(completed_t - r_pair) == 0
    checks["completed_depth_matches"] = sp.simplify(-sp.log(completed_t) + sp.log(r_pair)) == 0

    # Founded scalar factorization remains exact.
    ruler = 1 / r_pair
    q = sp.simplify(r_pair / ruler)
    chi = sp.simplify((ruler - r_pair) / (ruler + r_pair))
    checks["completed_reciprocal_product"] = sp.simplify(r_pair * ruler - 1) == 0
    checks["completed_q"] = sp.simplify(q - r_pair**2) == 0
    checks["completed_chi"] = sp.simplify(chi - (1 - r_pair**2) / (1 + r_pair**2)) == 0

    # Mandatory controls.
    eta = sp.symbols("eta", real=True)
    C, S = sp.cosh(eta), sp.sinh(eta)
    k_flat = sp.Matrix([1, 1])
    minkowski = sp.diag(-1, 1)
    u_a_flat = sp.Matrix([1, 0])
    u_b_flat = sp.Matrix([C, S])
    flat_ratio = sp.simplify(
        (k_flat.T * minkowski * u_a_flat)[0] / (k_flat.T * minkowski * u_b_flat)[0]
    )
    checks["G219_moving_flat_recovery"] = sp.simplify(flat_ratio - sp.exp(eta)) == 0

    phi_a, phi_b = sp.symbols("phi_A phi_B", real=True)
    lapse_a, lapse_b = sp.exp(-phi_a), sp.exp(-phi_b)
    static_ratio = sp.simplify(lapse_b / lapse_a)
    checks["primary_static_ratio"] = sp.simplify(static_ratio - sp.exp(phi_a - phi_b)) == 0
    checks["primary_static_depth"] = sp.simplify(
        sp.expand_log(-sp.log(static_ratio), force=True) - (phi_b - phi_a)
    ) == 0

    omega_a_value, omega_b_value = sp.symbols("Omega_A Omega_B", real=True)
    conformal_ratio = sp.exp(omega_b_value) / sp.exp(omega_a_value)
    checks["conformal_timelive_ratio"] = sp.simplify(
        conformal_ratio - sp.exp(omega_b_value - omega_a_value)
    ) == 0

    # Exact time-live affine ruler/shift witness.
    a0, slope_a, slope_beta, t_a, length = sp.symbols(
        "a0 a1 s t_A L", positive=True, real=True
    )
    d_expr = slope_a - slope_beta
    t_b = ((a0 + d_expr * t_a) * sp.exp(d_expr * length) - a0) / d_expr
    cp_at_a = a0 + d_expr * t_a
    cp_at_b = sp.simplify(a0 + d_expr * t_b)
    checks["affine_witness_Cplus"] = sp.simplify(
        (a0 + slope_a * t_a) - slope_beta * t_a - (a0 + (slope_a - slope_beta) * t_a)
    ) == 0
    checks["affine_witness_endpoint_ratio"] = sp.simplify(
        cp_at_b / cp_at_a - sp.exp(d_expr * length)
    ) == 0
    checks["affine_witness_map_slope"] = sp.simplify(
        sp.diff(t_b, t_a) - sp.exp(d_expr * length)
    ) == 0
    checks["affine_witness_incidence"] = sp.simplify(
        sp.expand_log(sp.log(cp_at_b / cp_at_a), force=True) / d_expr - length
    ) == 0
    checks["affine_witness_static_limit"] = sp.simplify(
        sp.limit(t_b, slope_a, slope_beta) - (t_a + a0 * length)
    ) == 0

    # Return uses the opposite null chord at later events, not outgoing inversion.
    cm_source, cm_target = sp.symbols("Cm_source Cm_target", positive=True, real=True)
    return_slope = cm_target / cm_source
    inverse_outgoing = cp_a / cp_b
    checks["return_chord_is_Cminus"] = sp.simplify(
        -n_b / cm_source + n_a * (n_b * cm_target / (cm_source * n_a)) / cm_target
    ) == 0
    checks["return_not_symbolic_inverse"] = sp.simplify(return_slope - inverse_outgoing) != 0

    assert all(checks.values()), {key: value for key, value in checks.items() if not value}
    return {
        "manifest_files": check_manifest(),
        "checks": checks,
        "check_count": len(checks),
        "formulas": {
            "covariant_clock_slope": "-(sigma_a*U_A^a)/(sigma_a_prime*U_B^a_prime)",
            "affine_frequency_slope": "(k_A.U_A)/(k_B.U_B)=omega_A/omega_B",
            "timelive_Cplus": "A-N*beta",
            "timelive_incidence": "L=integral(N/Cplus, t_A, t_B)",
            "timelive_clock_slope": "Cplus_B/Cplus_A",
            "completed_target_clock": "T_B=r_AB",
            "completed_depth": "-log(r_AB)",
            "future_return_chord": "Cminus=A+N*beta",
        },
        "landing": "COVARIANT_NULL_CLOCK_ARROW_DERIVED__COMPLETED_CLOCK_LEG_COMPATIBLE__NULL_REMAINS_QUERY_TYPED",
    }


if __name__ == "__main__":
    print(json.dumps(derive(), indent=2, sort_keys=True))
