#!/usr/bin/env python3
"""Production algebra and source checks for the CSN provenance audit."""

from __future__ import annotations

import hashlib
import json
import pathlib
import platform

import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = pathlib.Path(__file__).resolve().parent


def source(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def exact_checks() -> dict:
    A, phi, Omega, c, k, x = sp.symbols(
        "A phi Omega c k x", positive=True, finite=True
    )
    K = sp.Matrix([[0, 1], [1, 0]])
    eta = sp.diag(-1, 1)
    D = sp.diag(sp.exp(-phi), sp.exp(phi))
    P = A * D

    pairing_exact = sp.simplify(D.T * K * D)
    pairing_general = sp.simplify(P.T * K * P)
    metric_general = sp.simplify(P.T * eta * P)
    determinant = sp.simplify(P.det())

    # Four-dimensional constant and nonconstant conformal controls.
    volume_weight = Omega**4
    scalar_curvature_constant_weight = Omega**-2
    eh_density_constant_weight = sp.simplify(
        volume_weight * scalar_curvature_constant_weight
    )
    c2_scalar_weight = Omega**-4
    c2_density_constant_weight = sp.simplify(volume_weight * c2_scalar_weight)
    omega_x = sp.exp(k * x)
    flat_conformal_scalar = sp.simplify(-6 * omega_x**-2 * k**2)

    # No monomial in c and G alone can have length dimension.
    a, b = sp.symbols("a b")
    dimensional_solution = sp.linsolve(
        [
            sp.Eq(a + 3 * b, 1),  # length
            sp.Eq(-a - 2 * b, 0),  # time
            sp.Eq(-b, 0),  # mass
        ],
        (a, b),
    )

    # A common coframe rescaling preserves the local time/length ratio.
    dtau, dell = sp.symbols("dtau dell", positive=True)
    ratio_before = sp.simplify(dtau / dell)
    ratio_after = sp.simplify((Omega * dtau) / (Omega * dell))

    postulate = source("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md")
    reciprocal = source("UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md")
    cold = source("UDT_NATIVE_ACTION_COLD_PACKET.md")
    representative = source(
        "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md"
    )

    checks = {
        "R01_reciprocal_D_preserves_fixed_K": pairing_exact == K,
        "R02_general_common_factor_scales_K": pairing_general == A**2 * K,
        "R03_fixed_K_positive_solution_is_A1": sp.solve(
            sp.Eq(A**2, 1), A
        )
        == [1],
        "R04_common_factor_changes_metric": metric_general
        == sp.diag(-A**2 * sp.exp(-2 * phi), A**2 * sp.exp(2 * phi)),
        "R05_common_factor_changes_determinant": determinant == A**2,
        "R06_common_rescaling_preserves_clock_length_ratio": ratio_after
        == ratio_before,
        "R07_volume_weight_is_Omega4": volume_weight == Omega**4,
        "R08_scalar_curvature_constant_weight_is_Omega_minus2": (
            scalar_curvature_constant_weight == Omega**-2
        ),
        "R09_EH_density_has_constant_weight_two": (
            eh_density_constant_weight == Omega**2
        ),
        "R10_C2_density_has_constant_weight_zero": (
            c2_density_constant_weight == 1
        ),
        "R11_nonconstant_Omega_changes_flat_scalar_curvature": (
            flat_conformal_scalar != 0
        ),
        "R12_c_and_G_alone_supply_no_length_monomial": (
            dimensional_solution == sp.EmptySet
        ),
        "S01_CSN_is_explicitly_a_postulate": (
            "FOUNDATIONAL POSTULATE" in postulate
        ),
        "S02_CSN_declares_factor_calibrational": (
            "declares the first factor calibrational" in postulate
        ),
        "S03_CSN_scope_is_local_Omega_x": (
            r"\Omega(x)^2g_{\mu\nu}" in postulate
        ),
        "S04_reciprocity_derives_uv1": (
            r"\boxed{u(\Delta)v(\Delta)=1.}" in reciprocal
        ),
        "S05_reciprocity_does_not_derive_scale_X": (
            "does not yet derive a unique action, the profile" in reciprocal
            and "or the scale $X$" in reciprocal
        ),
        "S06_cold_packet_keeps_CSN_founding": (
            "**FOUNDING**—provenance: owner-locked" in cold
        ),
        "S07_cold_packet_uses_declaration_not_derivation": (
            "Common-Scale Neutrality declares the first factor calibrational"
            in cold
        ),
        "S08_no_current_representative_selector": (
            "SELECTOR_NOT_FOUND_IN_CURRENT_FOUNDATION" in representative
        ),
    }
    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise AssertionError(f"failed production checks: {failed}")

    return {
        "status": "PASS",
        "production_check_count": len(checks),
        "production_checks": checks,
        "algebra": {
            "P": "A*diag(exp(-phi),exp(phi))",
            "P_transpose_K_P": "A^2*K",
            "fixed_K_positive_A": "1",
            "metric_block": "A^2*diag(-exp(-2phi),exp(2phi))",
            "det_P": "A^2",
            "clock_length_ratio_under_common_rescaling": "unchanged",
            "constant_Omega_EH_density_weight": "Omega^2",
            "constant_Omega_C2_density_weight": "1",
            "nonconstant_flat_control_R_tilde": "-6*k^2*exp(-2*k*x)",
            "length_from_c_and_G_alone": "NO_MONOMIAL_SOLUTION",
        },
        "rulings": {
            "reciprocity": "FOUNDING_WITH_DETERMINANT_ONE_COMPARISON_DERIVED",
            "observed_c": "OBSERVED_TIME_LENGTH_CONVERSION_ANCHOR",
            "weak_unit_freedom": "CALIBRATIONAL",
            "common_factor_from_reciprocity": "FIXED_IN_EXACT_K_PRESERVING_COMPARISON_NOT_GAUGE_DERIVED",
            "strong_local_CSN": "OWNER_POSTULATE_NOT_DERIVED_FROM_RECIPROCITY_CURRENTLY_CHALLENGED",
            "physical_representative": "OPEN_SELECTOR",
            "c_absolute_length_selection": "NOT_DERIVED",
            "C2_Bach": "UNIQUE_CONDITIONAL_IF_STRONG_LOCAL_CSN_IS_RETAINED",
            "EH": "CONDITIONAL_NOT_SELECTED",
            "scale_free_UDT_core": "CONDITIONAL_ON_STRONG_LOCAL_CSN",
        },
        "maximum_conclusion": (
            "STRONG_LOCAL_CSN_IS_AN_EXPLICIT_OWNER_POSTULATE_NOT_A_RECIPROCITY_THEOREM;"
            "OBSERVED_C_PRESERVES_THE_RATIO_BUT_DOES_NOT_ALONE_SELECT_THE_COMMON_FACTOR;"
            "CSN_DEPENDENT_RESULTS_REQUIRE_REGRADING_IF_THE_POSTULATE_IS_WITHDRAWN_OR_WEAKENED"
        ),
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
        },
    }


def main() -> None:
    result = exact_checks()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (OUT / "RESULTS.json").write_text(payload, encoding="utf-8")
    print(payload, end="")
    print("results_sha256=" + hashlib.sha256(payload.encode()).hexdigest())


if __name__ == "__main__":
    main()
