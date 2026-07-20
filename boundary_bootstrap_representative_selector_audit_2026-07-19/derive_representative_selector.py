#!/usr/bin/env python3
"""Exact CSN-orbit, boundary, bootstrap, and Xmax-reciprocity selector audit."""

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
    y, r, X, epsilon, lam = sp.symbols("y r X epsilon lam", positive=True)
    checks: dict[str, str] = {}
    y_expr = r / X
    A = 1 - y_expr
    N = sp.sqrt(A)
    f_y = y**2 * (1 - y) ** 2
    f = f_y.subs(y, y_expr)
    sigma = epsilon * f
    Omega = sp.exp(sigma)

    # Endpoint-flat local CSN orbit.
    need("bump_seat_value", f_y.subs(y, 0) == 0, checks)
    need("bump_wall_value", f_y.subs(y, 1) == 0, checks)
    need("bump_seat_derivative", sp.diff(f_y, y).subs(y, 0) == 0, checks)
    need("bump_wall_derivative", sp.diff(f_y, y).subs(y, 1) == 0, checks)
    need("bump_nontrivial_interior", f_y.subs(y, sp.Rational(1, 2)) == sp.Rational(1, 16), checks)

    # Reciprocal ratio/depth is invariant while the common product changes.
    temporal = Omega**2 * A
    radial = Omega**2 / A
    need("reciprocal_ratio_preserved", sp.simplify(radial / temporal - 1 / A**2) == 0, checks)
    need("common_product_changes", sp.simplify(temporal * radial - Omega**4) == 0, checks)
    depth_before = sp.log((1 / A) / A) / 4
    depth_after = sp.log(radial / temporal) / 4
    need("reciprocal_depth_preserved", sp.simplify(depth_after - depth_before) == 0, checks)

    # The optical spatial metric h/N^2 is exactly invariant under h'=Omega^2 h, N'=Omega N.
    optical_rr_before = sp.simplify((1 / A) / N**2)
    optical_rr_after = sp.simplify((Omega**2 / A) / (Omega * N) ** 2)
    optical_ang_before = sp.simplify(r**2 / N**2)
    optical_ang_after = sp.simplify(Omega**2 * r**2 / (Omega * N) ** 2)
    need("optical_radial_metric_invariant", sp.simplify(optical_rr_after - optical_rr_before) == 0, checks)
    need("optical_angular_metric_invariant", sp.simplify(optical_ang_after - optical_ang_before) == 0, checks)

    # Endpoint metric/first-order wall data and wall area are preserved by the bump.
    need("Omega_seat", sp.simplify(Omega.subs(r, 0) - 1) == 0, checks)
    need("Omega_wall", sp.simplify(Omega.subs(r, X) - 1) == 0, checks)
    need("Omega_prime_seat", sp.simplify(sp.diff(Omega, r).subs(r, 0)) == 0, checks)
    need("Omega_prime_wall", sp.simplify(sp.diff(Omega, r).subs(r, X)) == 0, checks)
    wall_area_before = 4 * sp.pi * X**2
    wall_area_after = sp.simplify(4 * sp.pi * (Omega.subs(r, X) * X) ** 2)
    need("wall_area_preserved", sp.simplify(wall_area_after - wall_area_before) == 0, checks)

    # Static surface-gravity magnitude squared |D N|^2 is unchanged at the wall.
    N_prime = Omega * N
    kappa_sq_prime = sp.simplify(Omega**-2 * A * sp.diff(N_prime, r) ** 2)
    need("surface_gravity_preserved", sp.simplify(sp.limit(kappa_sq_prime, r, X, dir="-") - 1 / (4 * X**2)) == 0, checks)

    # Proper radial length and volume do change: boundary data have not fixed the interior representative.
    length_linear_response = sp.integrate(f_y / sp.sqrt(1 - y), (y, 0, 1)) * X
    volume_linear_response = 12 * sp.pi * X**3 * sp.integrate(y**2 * f_y / sp.sqrt(1 - y), (y, 0, 1))
    need("proper_length_changes", sp.simplify(length_linear_response - 16 * X / 315) == 0, checks)
    need("proper_volume_changes", sp.simplify(volume_linear_response - 1024 * sp.pi * X**3 / 5005) == 0, checks)
    angular_area_mid_ratio = sp.simplify(Omega.subs(r, X / 2) ** 2)
    need("interior_angular_area_changes", angular_area_mid_ratio == sp.exp(epsilon / 8), checks)

    # The bump preserves finite wall curvature and its value, but changes the interior curvature.
    R4 = 6 / (X * r)
    sigma_prime = sp.diff(sigma, r)
    box_sigma = sp.simplify(sp.diff(r**2 * A * sigma_prime, r) / r**2)
    grad_sigma_sq = sp.simplify(A * sigma_prime**2)
    R4_prime = sp.simplify(Omega**-2 * (R4 - 6 * box_sigma - 6 * grad_sigma_sq))
    need("wall_scalar_curvature_preserved", sp.simplify(sp.limit(R4_prime, r, X, dir="-") - 6 / X**2) == 0, checks)
    need("interior_scalar_curvature_changes", sp.simplify(sp.diff(R4_prime, epsilon).subs({epsilon: 0, r: X / 2})) != 0, checks)

    # Clock-curvature zero is not preserved, reproducing the prior selector obstruction independently.
    f_prime = sp.diff(f, r)
    E4_extra = sp.simplify(2 * A * f_prime * epsilon * sp.diff(N, r) + N * A * (f_prime * epsilon) ** 2)
    expected_extra = sp.simplify(-N * epsilon * sp.diff(f_y, y).subs(y, y_expr) / X**2 + N**3 * epsilon**2 * sp.diff(f_y, y).subs(y, y_expr) ** 2 / X**2)
    need("clock_curvature_bump_extra", sp.simplify(E4_extra - expected_extra) == 0, checks)
    point_extra = sp.simplify(E4_extra.subs({epsilon: 1, r: X / 4}))
    need("clock_curvature_not_preserved", sp.simplify(point_extra + 165 * sp.sqrt(3) / (2048 * X**2)) == 0, checks)

    # Constant scale and Xmax reciprocity: dimensionless position and compactness remain invariant.
    x, Xmax, M, c, G, mu, nu, delta = sp.symbols("x Xmax M c G mu nu delta", positive=True)
    xi = x / Xmax
    need("xmax_ratio_homothety_invariant", sp.simplify((lam * x) / (lam * Xmax) - xi) == 0, checks)
    compactness = G * M / (c**2 * Xmax)
    need("compactness_homothety_invariant", sp.simplify(compactness.subs({M: lam * M, Xmax: lam * Xmax}) - compactness) == 0, checks)
    density = M / Xmax**3
    dimensionless_density = G * density * Xmax**2 / c**2
    need("dimensionless_density_homothety_invariant", sp.simplify(dimensionless_density.subs({M: lam * M, Xmax: lam * Xmax}) - dimensionless_density) == 0, checks)
    boot = mu - nu * delta
    need("bootstrap_root_scale_blind", not boot.has(Xmax) and not boot.has(lam), checks)

    # Fractional-linear Xmax law acts only on xi and cannot see the common scale.
    eta = sp.symbols("eta", real=True)
    compose = (xi + eta) / (1 + xi * eta)
    compose_scaled = sp.simplify(compose.subs({x: lam * x, Xmax: lam * Xmax}))
    need("xmax_composition_homothety_invariant", sp.simplify(compose_scaled - compose) == 0, checks)

    result = {
        "schema": "udt-boundary-bootstrap-representative-selector-1.0",
        "result": "PASS",
        "checks": checks,
        "endpoint_flat_CSN_family": {
            "Omega": "exp(epsilon*y^2*(1-y)^2)",
            "preserves": [
                "CSN class and reciprocal ratio/depth",
                "null/causal structure",
                "seat and wall endpoint values and first derivatives",
                "wall area and static surface-gravity magnitude",
                "complete optical spatial metric and optical reach",
                "finite/infinite character of recorded reaches",
            ],
            "changes": [
                "interior angular areas",
                "proper radial length and proper volume",
                "interior scalar curvature representative",
                "clock-curvature residual",
            ],
            "length_first_variation": "16*X/315",
            "volume_first_variation": "1024*pi*X^3/5005",
            "clock_curvature_witness": "E4_extra(epsilon=1,y=1/4)=-165*sqrt(3)/(2048*X^2)",
        },
        "xmax_reciprocity": {
            "dimensionless_position": "xi=x/Xmax",
            "homothety": "x->lambda*x, Xmax->lambda*Xmax leaves xi and XR1 composition unchanged",
            "global_fixed_value": "would fix one global scale only if independently derived; current value/origin remain open",
            "local_representative": "even fixed endpoint Xmax does not remove endpoint-flat interior Omega(y)",
            "ruling": "VALUABLE_DIMENSIONLESS_POSITIONAL_HYPOTHESIS; NOT_A_CURRENT_CSN_REPRESENTATIVE_SELECTOR",
        },
        "bootstrap": {
            "dimensionless_root": "mu(delta)-nu(delta)*delta=0",
            "homothety": "M,Xmax -> lambda*M,lambda*Xmax leaves compactness and dimensionless density unchanged",
            "ruling": "CURRENT_ON_SHELL_BOOTSTRAP_CAN_FILTER_COMPLETE_SOLUTIONS_BUT_DOES_NOT_SUPPLY_SIGMA_OR_REMOVE_LOCAL_CSN_ORBIT",
        },
        "maximum_conclusion": "NO_EXISTING_NONCIRCULAR_BOUNDARY_BOOTSTRAP_OR_XMAX_RECIPROCITY_RULE_SELECTS_THE_PHYSICAL_CSN_REPRESENTATIVE; WRL_RATIO_PROFILE_AND_CONDITIONAL_CLOCK_CURVATURE_SELECTOR_REMAIN_DISTINCT",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks), "maximum_conclusion": result["maximum_conclusion"]}, sort_keys=True))


if __name__ == "__main__":
    main()
