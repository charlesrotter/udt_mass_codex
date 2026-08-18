#!/usr/bin/env python3
"""Exact symbolic derivation for G153."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def main() -> None:
    T, L, X, Omega = sp.symbols("T L X_max Omega", positive=True)
    beta, phi = sp.symbols("beta phi", real=True)
    phi_t, phi_s = sp.symbols("partial_tau_phi partial_sigma_phi", real=True)
    X_t, X_s = sp.symbols("partial_tau_Xmax partial_sigma_Xmax", real=True)

    sech2 = sp.cosh(phi) ** -2
    rho = X * sp.tanh(phi)
    rho_t = sp.simplify(X_t * sp.tanh(phi) + X * sech2 * phi_t)
    rho_s = sp.simplify(X_s * sp.tanh(phi) + X * sech2 * phi_s)
    u_rho = sp.simplify(rho_t / T)
    n_rho = sp.simplify((rho_s - beta * rho_t) / L)

    # Coframe rows in coordinate components (d tau, d sigma).
    theta0 = sp.Matrix([T, T * beta])
    theta1 = sp.Matrix([0, L])
    coordinate_from_frame = sp.simplify(u_rho * theta0 + n_rho * theta1)
    coordinate_direct = sp.Matrix([rho_t, rho_s])

    # Common scale changes the metric ruler normalization but not reciprocal position.
    u_rho_scaled = sp.simplify(rho_t / (Omega * T))
    n_rho_scaled = sp.simplify((rho_s - beta * rho_t) / (Omega * L))
    scaled_reconstruction = sp.simplify(
        u_rho_scaled * (Omega * theta0) + n_rho_scaled * (Omega * theta1)
    )

    # Rational expression directly in terminal T,L and their first derivatives.
    Tt, Lt, Ts, Ls = sp.symbols("T_tau L_tau T_sigma L_sigma", real=True)
    chi = sp.simplify((L - T) / (L + T))
    dchi_t = sp.simplify(sp.diff(chi, T) * Tt + sp.diff(chi, L) * Lt)
    dchi_s = sp.simplify(sp.diff(chi, T) * Ts + sp.diff(chi, L) * Ls)
    dphi_t = sp.simplify((Lt / L - Tt / T) / 2)
    dphi_s = sp.simplify((Ls / L - Ts / T) / 2)
    sech2_TL = sp.simplify(4 * T * L / (T + L) ** 2)

    # Same relational position, different ruler density: equality is not common-scale invariant.
    finite_equal_base = {
        "T": sp.Rational(1, 3), "L": sp.Rational(1), "X": sp.Rational(2)
    }
    rho_base = sp.simplify(
        X * (L - T) / (L + T)
    ).subs({T: finite_equal_base["T"], L: finite_equal_base["L"], X: finite_equal_base["X"]})
    rho_scaled = sp.simplify(
        X * (L - T) / (L + T)
    ).subs({T: 2 * finite_equal_base["T"], L: 2 * finite_equal_base["L"], X: finite_equal_base["X"]})

    source_checks = {}
    sources = {
        "G135": ROOT / "udt_g135_projective_pair_separation_constitution_audit_2026-08-17/AUDIT_REPORT.md",
        "G137": ROOT / "udt_g137_copresent_relational_position_join_2026-08-17/AUDIT_REPORT.md",
        "G147": ROOT / "udt_g147_pair_directional_metric_screen_solder_2026-08-17/EXACT_DERIVATION.md",
        "G152": ROOT / "udt_g152_pair_immersion_variational_chord_ownership_2026-08-17/AUDIT_REPORT.md",
    }
    source_checks["G135_common_scale_blind"] = (
        "same `chi` can have" in sources["G135"].read_text()
        or "same `chi` can have different" in sources["G135"].read_text()
    )
    g137_text = sources["G137"].read_text()
    source_checks["G137_proper_length_open"] = "proper length" in g137_text and "What remains open" in g137_text
    g147_text = sources["G147"].read_text()
    source_checks["G147_lift_conditional"] = "DEFINED / SUPPLIED_CONDITIONAL_QUERY_RELATIVE_LIFT" in g147_text
    source_checks["G147_not_displacement_or_length"] = (
        "not a spacetime displacement" in g147_text and "proper length" in g147_text
    )
    source_checks["G152_no_automatic_identity"] = "does not\nautomatically identify" in sources["G152"].read_text()

    gates = {
        "coordinate_frame_decomposition_exact": all(
            sp.simplify(q) == 0 for q in coordinate_from_frame - coordinate_direct
        ),
        "common_scale_reconstruction_invariant": all(
            sp.simplify(q) == 0 for q in scaled_reconstruction - coordinate_direct
        ),
        "chi_tau_derivative_exact": sp.simplify(
            dchi_t - sech2_TL * dphi_t
        ) == 0,
        "chi_sigma_derivative_exact": sp.simplify(
            dchi_s - sech2_TL * dphi_s
        ) == 0,
        "finite_equality_base": sp.simplify(rho_base - finite_equal_base["L"]) == 0,
        "finite_equality_destroyed_by_common_scale": sp.simplify(
            rho_scaled - 2 * finite_equal_base["L"]
        ) != 0,
        "position_unchanged_by_common_scale": sp.simplify(rho_scaled - rho_base) == 0,
        **source_checks,
    }
    gates = {name: bool(value) for name, value in gates.items()}

    result = {
        "schema": "udt.g153.differential_join.v1",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "formulas": {
            "rho": str(rho),
            "theta0_coordinate": [str(q) for q in theta0],
            "theta1_coordinate": [str(q) for q in theta1],
            "u_rho": str(u_rho),
            "n_rho": str(n_rho),
            "fixed_Xmax_u_rho": str(sp.simplify(u_rho.subs({X_t: 0}))),
            "fixed_Xmax_n_rho": str(sp.simplify(n_rho.subs({X_t: 0, X_s: 0}))),
            "d_rho_coordinate": [str(q) for q in coordinate_direct],
            "metric_norm_d_rho": str(sp.simplify(-u_rho**2 + n_rho**2)),
            "chi": str(chi),
            "dchi_tau": str(dchi_t),
            "dchi_sigma": str(dchi_s),
            "optional_spatial_unit_ruler_condition": "n(rho)=epsilon",
            "optional_full_one_form_condition": "u(rho)=0 and n(rho)=epsilon",
        },
        "common_scale": {
            "rho_base": str(rho_base),
            "L_base": str(finite_equal_base["L"]),
            "rho_after_scale_2": str(rho_scaled),
            "L_after_scale_2": str(2 * finite_equal_base["L"]),
            "response_coefficients_scale": "u(rho),n(rho) -> Omega^-1 times themselves",
            "coframes_scale": "theta0,theta1 -> Omega times themselves",
            "d_rho": "unchanged when Xmax and phi are common-scale invariant",
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sources.values()
        },
        "gates": gates,
        "premise_stamps": {
            "finite_relational_position": "CHOSE_WORKING_FOUNDATIONAL_CLARIFICATION_AND_DERIVED_DOWNSTREAM",
            "rest_space_vector_lift": "DEFINED_SUPPLIED_CONDITIONAL",
            "metric_ruler_coframe": "DERIVED_FROM_SUPPLIED_PAIR_METRIC",
            "differential_response": "DERIVED_ON_SUPPLIED_SMOOTH_PAIR_FAMILY_INCLUDING_D_XMAX",
            "fixed_Xmax_response": "CONDITIONAL_SUBCASE",
            "unit_ruler_identification": "OPTIONAL_ADDITIONAL_CALIBRATION_NOT_ADOPTED",
            "proper_length_history_Xmax_value_completion": "OPEN",
        },
        "maximum_conclusion": (
            "G137_OWNS_FINITE_RELATIONAL_POSITION_NOT_METRIC_PROPER_RULER_LENGTH__"
            "G147_REST_SPACE_VECTOR_LIFT_REMAINS_CONDITIONAL__"
            "FINITE_CHORD_EQUALS_LOCAL_RULER_IS_NOT_THE_NATIVE_JOIN__"
            "D_RHO_HAS_EXACT_METRIC_FRAME_DECOMPOSITION_ON_SUPPLIED_SMOOTH_PAIR_FAMILY__"
            "UNIT_RULER_IDENTIFICATION_PROPER_LENGTH_HISTORY_XMAX_VALUE_AND_COMPLETION_OPEN"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
