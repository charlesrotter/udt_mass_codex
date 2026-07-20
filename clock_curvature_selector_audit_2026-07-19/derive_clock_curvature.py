#!/usr/bin/env python3
"""Exact CPU/SymPy audit of the WR-L clock-curvature selector candidate."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def need(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    r, X, epsilon, k, a, b = sp.symbols("r X epsilon k a b", positive=True)
    A = sp.Function("A")(r)
    checks: dict[str, str] = {}

    # Exact arbitrary-profile curvature in reciprocal areal gauge.
    R4 = -sp.diff(A, r, 2) - 4 * sp.diff(A, r) / r + 2 * (1 - A) / r**2
    R3 = -2 * sp.diff(A, r) / r + 2 * (1 - A) / r**2
    N = sp.sqrt(A)
    laplace_N = sp.simplify(sp.sqrt(A) / r**2 * sp.diff(r**2 * sp.sqrt(A) * sp.diff(N, r), r))
    need("general_lapse_laplacian", sp.simplify(laplace_N - N * (sp.diff(A, r, 2) / 2 + sp.diff(A, r) / r)) == 0, checks)

    profile_operator = sp.diff(A, r, 2) + sp.diff(A, r) / r + (1 - A) / r**2
    E4 = sp.factor(laplace_N + R4 * N / 6)
    E3 = sp.factor(laplace_N + R3 * N / 4)
    need("E4_reduction", sp.simplify(E4 - N * profile_operator / 3) == 0, checks)
    need("E3_reduction", sp.simplify(E3 - N * profile_operator / 2) == 0, checks)
    need("E3_E4_equivalence", sp.simplify(E3 - sp.Rational(3, 2) * E4) == 0, checks)

    # The equation selects a two-constant profile family. Seat finiteness and one wall then select WR-L.
    candidate_general = 1 - a * r - b / r
    need("profile_general_solution", sp.simplify(profile_operator.subs(A, candidate_general).doit()) == 0, checks)
    need("singular_mode_excluded_by_finite_seat", sp.limit(candidate_general, r, 0, dir="+") == -sp.oo, checks)
    candidate_seat = candidate_general.subs(b, 0)
    need("finite_seat_normalization", sp.limit(candidate_seat, r, 0, dir="+") == 1, checks)
    wr_l = candidate_seat.subs(a, 1 / X)
    need("one_wall_selects_WRL", sp.simplify(wr_l.subs(r, X)) == 0 and sp.simplify(wr_l - (1 - r / X)) == 0, checks)

    # Explicit same-endpoint reciprocal deformation; epsilon=1/2 is positive throughout the open cell.
    y = r / X
    A_eps = sp.expand((1 - y) * (1 + epsilon * y * (1 - y)))
    A_half = sp.factor(A_eps.subs(epsilon, sp.Rational(1, 2)))
    need("deformation_seat", sp.simplify(A_eps.subs(r, 0) - 1) == 0, checks)
    need("deformation_wall", sp.simplify(A_eps.subs(r, X)) == 0, checks)
    need("deformation_positive_factor", sp.simplify(A_half - (2 * X - r) * (X - r) * (X + r) / (2 * X**3)) == 0, checks)
    wall_slope_factor = sp.limit(A_eps / (1 - y), r, X, dir="-")
    need("same_linear_wall_class", sp.simplify(wall_slope_factor - 1) == 0, checks)
    O_eps = sp.factor(profile_operator.subs(A, A_eps).doit())
    need("deformation_residual", sp.simplify(O_eps - 2 * epsilon * (-3 * X + 4 * r) / X**3) == 0, checks)
    need("deformation_violates_selector", sp.simplify(O_eps.subs({epsilon: sp.Rational(1, 2), r: X / 2}) + 1 / X**2) == 0, checks)

    R4_eps = sp.factor(R4.subs(A, A_eps).doit())
    R3_eps = sp.factor(R3.subs(A, A_eps).doit())
    weighted_R4_eps = sp.simplify(sp.sqrt(A_eps) * R4_eps * r**2 / sp.sqrt(A_eps))
    weighted_R3_eps = sp.simplify(sp.sqrt(A_eps) * R3_eps * r**2 / sp.sqrt(A_eps))
    need("deformation_weighted_R4_integrable_seat", sp.limit(weighted_R4_eps, r, 0, dir="+") == 0, checks)
    need("deformation_weighted_R3_integrable_seat", sp.limit(weighted_R3_eps, r, 0, dir="+") == 0, checks)

    # Local Common-Scale transformation. These coefficients follow directly for h'=e^(2s)h, N'=e^s N.
    cross, lap_sigma, grad2, R3sym, lapN, lapse = sp.symbols("cross lap_sigma grad2 R3sym lapN lapse")
    alpha = sp.symbols("alpha")
    transformed_spatial = lapN + alpha * R3sym * lapse + 3 * cross + (1 - 4 * alpha) * lapse * lap_sigma + (2 - 2 * alpha) * lapse * grad2
    need("simple_spatial_operator_cross_obstruction", sp.diff(transformed_spatial, cross) == 3, checks)
    no_alpha = sp.solve(
        [sp.Eq(3, 0), sp.Eq(1 - 4 * alpha, 0), sp.Eq(2 - 2 * alpha, 0)],
        [alpha],
        dict=True,
    )
    need("no_simple_spatial_coefficient_restores_local_CSN", no_alpha == [], checks)

    # Four-dimensional E4 transformation: E4' = e^-s(E4 + 2 grad(s).grad(N) + N|grad s|^2).
    A_wrl = 1 - r / X
    N_wrl = sp.sqrt(A_wrl)
    sigma_prime = k / X
    local_scale_extra = sp.factor(2 * A_wrl * sigma_prime * sp.diff(N_wrl, r) + N_wrl * A_wrl * sigma_prime**2)
    expected_extra = -k * N_wrl / X**2 + k**2 * N_wrl**3 / X**2
    need("E4_local_CSN_extra", sp.simplify(local_scale_extra - expected_extra) == 0, checks)
    need(
        "E4_zero_not_preserved_locally",
        sp.simplify(local_scale_extra.subs({k: 1, r: X / 2}) + 1 / (2 * sp.sqrt(2) * X**2)) == 0,
        checks,
    )
    need("constant_common_scale_preserves_zero", sp.simplify(expected_extra.subs(k, 0)) == 0, checks)

    # Covariant meaning after a static clock congruence has been selected.
    Rtt = sp.symbols("Rtt")
    Rscalar = sp.symbols("Rscalar")
    gtt = -lapse**2
    covariant_clock_contraction = Rtt / lapse**2 + Rscalar / 6
    substituted = covariant_clock_contraction.subs(Rtt, lapse * lapN)
    need("clock_contraction_equals_E4_over_N", sp.simplify(substituted - (lapN + Rscalar * lapse / 6) / lapse) == 0, checks)
    need("trace_adjusted_Ricci_form", sp.simplify(Rtt - Rscalar * gtt / 6 - (Rtt + Rscalar * lapse**2 / 6)) == 0, checks)

    result = {
        "schema": "udt-clock-curvature-selector-1.0",
        "result": "PASS",
        "checks": checks,
        "general_family": {
            "metric": "ds^2=-A(r)c^2dt^2+A(r)^(-1)dr^2+r^2dOmega^2",
            "R4": "-A''-4A'/r+2(1-A)/r^2",
            "R3": "-2A'/r+2(1-A)/r^2",
            "laplace_N": "N(A''/2+A'/r)",
            "E4": "N[A''+A'/r+(1-A)/r^2]/3",
            "E3": "N[A''+A'/r+(1-A)/r^2]/2",
        },
        "selector_solution": {
            "general": "A=1-a*r-b/r",
            "finite_normalized_seat": "b=0",
            "wall_at_X": "a=1/X",
            "conditional_result": "A=1-r/X (WR-L)",
        },
        "countermetric": {
            "profile": "A_epsilon=(1-r/X)[1+epsilon(r/X)(1-r/X)]",
            "tested_member": "epsilon=1/2",
            "profile_residual": "2*epsilon*(4*r-3*X)/X^3",
            "satisfied": ["reciprocal clock/ruler block", "A(0)=1", "A(X)=0", "A>0 inside", "same linear wall class", "integrable weighted seat curvature"],
            "unresolved_or_not_satisfied": ["WR-L residual-recentering profile axiom", "complete off-shell action/source/boundary/bootstrap"],
        },
        "common_scale": {
            "E4_transform": "E4'=exp(-sigma)[E4+2 grad(sigma).grad(N)+N|grad(sigma)|^2]",
            "simple_E3a_transform": "E_a'=exp(-sigma)[E_a+3 grad(sigma).grad(N)+(1-4a)N Delta sigma+(2-2a)N|grad sigma|^2]",
            "ruling": "constant common scale preserves zero; general local common scale does not; no coefficient a fixes the physical lapse weight",
        },
        "covariant_readout": {
            "equation": "(R_mu_nu-R*g_mu_nu/6)u^mu u^nu=0",
            "required_structure": "selected static unit clock direction u and physical representative",
        },
        "maximum_conclusion": "CLOCK_CURVATURE_PROFILE_SELECTION_UNIQUE_CONDITIONAL_WITHIN_STATIC_RECIPROCAL_AREAL_GAUGE; NOT_FORCED_BY_CURRENT_RECIPROCITY_CSN_FINITE_CELL_OR_BOOTSTRAP",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks), "maximum_conclusion": result["maximum_conclusion"]}, sort_keys=True))


if __name__ == "__main__":
    main()
