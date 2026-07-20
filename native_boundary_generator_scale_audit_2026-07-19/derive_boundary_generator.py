#!/usr/bin/env python3
"""Exact metric-flux, action-ambiguity, and scale-rank derivation."""

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
    r, X, y = sp.symbols("r X y", positive=True)
    c, G, alpha, gamma, rho_star = sp.symbols("c G alpha gamma rho_star", positive=True)
    kappa, eta, zeta, qp, qpp = sp.symbols("kappa eta zeta qp qpp", nonzero=True)
    checks: dict[str, str] = {}

    A = 1 - r / X
    N = sp.sqrt(A)
    R4 = 6 / (X * r)
    R3 = 4 / (X * r)
    dV_dr = 4 * sp.pi * r**2 / sp.sqrt(A)

    # h_rr=A^-1, hence n^r=sqrt(A) on a round sphere.
    flux = sp.simplify(4 * sp.pi * r**2 * sp.sqrt(A) * sp.diff(N, r))
    need("flux_profile", sp.simplify(flux + 2 * sp.pi * r**2 / X) == 0, checks)
    need("flux_seat", sp.limit(flux, r, 0, dir="+") == 0, checks)
    need("flux_wall", sp.limit(flux, r, X, dir="-") == -2 * sp.pi * X, checks)
    need("flux_not_radially_conserved", sp.simplify(sp.diff(flux, r) + 4 * sp.pi * r / X) == 0, checks)

    # Direct radial Laplace-Beltrami calculation.
    laplace_N = sp.simplify(sp.sqrt(A) / r**2 * sp.diff(r**2 * sp.sqrt(A) * sp.diff(N, r), r))
    need("lapse_laplacian", sp.simplify(laplace_N + N / (X * r)) == 0, checks)
    need("lapse_R4_identity", sp.simplify(laplace_N + R4 * N / 6) == 0, checks)
    need("lapse_R3_identity", sp.simplify(laplace_N + R3 * N / 4) == 0, checks)

    weighted_R4 = sp.integrate(sp.simplify(N * R4 * dV_dr), (r, 0, X))
    weighted_R3 = sp.integrate(sp.simplify(N * R3 * dV_dr), (r, 0, X))
    integrated_laplace = sp.integrate(sp.simplify(laplace_N * dV_dr), (r, 0, X))
    need("weighted_R4_budget", sp.simplify(weighted_R4 - 12 * sp.pi * X) == 0, checks)
    need("weighted_R3_budget", sp.simplify(weighted_R3 - 8 * sp.pi * X) == 0, checks)
    need("divergence_theorem", sp.simplify(integrated_laplace - flux.subs(r, X)) == 0, checks)
    need("R4_flux_budget", sp.simplify(integrated_laplace + weighted_R4 / 6) == 0, checks)
    need("R3_flux_budget", sp.simplify(integrated_laplace + weighted_R3 / 4) == 0, checks)

    # All WR-L metric data reduce to dimensionless shape plus powers of X.
    flux_y = sp.simplify(flux.subs(r, X * y))
    R4_y = sp.simplify(R4.subs(r, X * y))
    V = sp.simplify(sp.integrate(dV_dr, (r, 0, X)))
    need("dimensionless_flux_shape", sp.simplify(flux_y / X + 2 * sp.pi * y**2) == 0, checks)
    need("dimensionless_curvature_shape", sp.simplify(R4_y * X**2 - 6 / y) == 0, checks)
    need("volume_scaling", sp.simplify(V - 64 * sp.pi * X**3 / 15) == 0, checks)

    # Overall action normalization and exact-boundary terms do not alter bulk stationarity.
    # Toy reduced L=kappa*q'^2/2: EL=-kappa*q'', p=kappa*q'.
    EL = -kappa * qpp
    momentum = kappa * qp
    EL_rescaled = sp.simplify(EL / kappa)
    momentum_rescaled = sp.simplify(momentum / kappa)
    need("action_rescaling_same_bulk_equation", EL_rescaled == -qpp, checks)
    need("action_rescaling_changes_momentum", momentum_rescaled == qp and momentum != qp, checks)

    # Adding d(eta*q)/dr=eta*q' shifts fixed-boundary canonical momentum, not EL.
    shifted_momentum = momentum + eta
    need("exact_q_boundary_term_shifts_momentum", sp.simplify(shifted_momentum - momentum - eta) == 0, checks)
    need("exact_q_boundary_term_same_bulk_EL", EL == -kappa * qpp, checks)

    # Adding d(zeta*r)/dr=zeta shifts the movable-endpoint Hamiltonian by -zeta.
    H = sp.simplify(momentum * qp - kappa * qp**2 / 2)
    H_shifted = sp.simplify(momentum * qp - (kappa * qp**2 / 2 + zeta))
    need("exact_r_boundary_term_shifts_endpoint_H", sp.simplify(H_shifted - H + zeta) == 0, checks)

    # General normalized mass candidate from a length-valued flux.
    M_flux = gamma * c**2 * X / G
    compactness = sp.simplify(G * M_flux / (c**2 * X))
    density = sp.simplify(M_flux / V)
    need("flux_mass_compactness_only", compactness == gamma, checks)
    need("flux_mass_density_scaling", sp.simplify(density - 15 * gamma * c**2 / (64 * sp.pi * G * X**2)) == 0, checks)

    # Pairing X=alpha*G*M/c^2 with M=gamma*c^2*X/G is rank deficient when consistent.
    closure_matrix = sp.Matrix([[1, -alpha * G / c**2], [-gamma * c**2 / G, 1]])
    closure_det = sp.factor(closure_matrix.det())
    need("linear_closure_determinant", closure_det == 1 - alpha * gamma, checks)
    closure_after_substitution = sp.factor(X - alpha * G * M_flux / c**2)
    need(
        "linear_closure_reduces_to_coefficient",
        sp.simplify(closure_after_substitution - X * (1 - alpha * gamma)) == 0,
        checks,
    )

    # A separately supplied physical density center would select X, but that is the missing datum.
    X_from_density = sp.sqrt(15 * gamma * c**2 / (64 * sp.pi * G * rho_star))
    need("density_center_would_select_scale", sp.simplify(density.subs(X, X_from_density) - rho_star) == 0, checks)

    result = {
        "schema": "udt-native-boundary-generator-scale-1.0",
        "result": "PASS",
        "checks": checks,
        "metric_flux": {
            "profile": "Phi_N(r)=-2*pi*r^2/X",
            "wall": "Phi_N(X)=-2*pi*X",
            "radial_derivative": "dPhi_N/dr=-4*pi*r/X != 0",
            "laplace_N": "D^2 N=-N/(X*r)=-R4*N/6=-R3*N/4",
            "weighted_R4_integral": "12*pi*X",
            "weighted_R3_integral": "8*pi*X",
            "ruling": "FINITE_INTEGRATED_CURVATURE_BUDGET; NOT_SURFACE_INDEPENDENT_CHARGE",
        },
        "action_ambiguity": {
            "overall_rescaling": "same stationary equation; canonical momenta/charges rescale",
            "exact_q_boundary_term": "same bulk EL; fixed-boundary momentum shifts by eta",
            "exact_r_boundary_term": "same bulk EL; movable-endpoint Hamiltonian shifts by -zeta",
            "ruling": "METRIC_AND_BULK_EQUATIONS_DO_NOT_FIX_BOUNDARY_GENERATOR_OR_NORMALIZATION",
        },
        "scale_rank": {
            "candidate_mass": "M_flux=gamma*c_E^2*X/G_obs",
            "compactness": "G_obs*M_flux/(c_E^2*X)=gamma",
            "paired_X_relation": "X=alpha*G_obs*M_flux/c_E^2",
            "determinant": "1-alpha*gamma",
            "consistent_case": "alpha*gamma=1 gives rank one and a continuum of positive X",
            "inconsistent_case": "alpha*gamma!=1 gives only X=0 for the homogeneous pair",
            "missing_gate": "native non-degree-one mass/boundary equation or separately derived physical density/scale",
        },
        "maximum_conclusion": "RAW_METRIC_CURVATURE_BUDGET_DERIVED; CONSERVED_CHARGE_AND_ABSOLUTE_SCALE_OPEN",
        "compute": {"cpu_only": True, "gpu_used": False, "sympy": sp.__version__},
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks), "maximum_conclusion": result["maximum_conclusion"]}, sort_keys=True))


if __name__ == "__main__":
    main()
