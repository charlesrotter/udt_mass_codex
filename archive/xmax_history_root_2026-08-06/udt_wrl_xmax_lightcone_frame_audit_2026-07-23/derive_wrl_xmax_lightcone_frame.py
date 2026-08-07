#!/usr/bin/env python3
"""Exact WR-L null-cone, local-frame, and global-recentering audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PREREG_COMMIT = "44ebe4c"
MAXIMUM = (
    "THE_WRL_METRIC_DERIVES_A_FRAME_INVARIANT_NULL_SURFACE_AND_LOCAL_"
    "LORENTZIAN_OBSERVER_RECIPROCITY;STATIC_CLOCK_AND_OPTICAL_"
    "UNATTAINABILITY_ARE_EXACT;THE_REGULAR_INGOING_CHART_ADMITS_CROSSING_"
    "CURVES;THE_CONSTANT_DEPTH_RECENTERING_OF_THE_OLDER_PROJECTIVE_FRAME_"
    "FAILS_AS_A_FULL_WRL_METRIC_HOMOTHETY_IN_THE_AREAL_ANGULAR_SECTOR;"
    "UNIVERSAL_UNCROSSABILITY_AND_GLOBAL_OBSERVER_RECIPROCITY_REQUIRE_"
    "ADDITIONAL_COMPLETE_METRIC_OR_BOUNDARY_CONTENT"
)

SOURCE_HASHES = {
    "SIMPLE_METRIC_MACRO.md":
        "f0c045abf9810dc327d249d0df385cd7e8d6914eedfaf5b31c78d186eaa13d44",
    "CANON.md":
        "5d99c0ba09fcee0429a34ac6b3dda4faff489b7d214b622fcbd286deb3785314",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md":
        "af6bcc49535fd9cf4c8a60e997935d10619f2d52d146482ee40ad9d968f76810",
    "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md":
        "bf10dc2d525e26723ee2eb2eaacf368ad8546e76b0a8d3ba0d3baa0b9639d11d",
    "udt_xmax_dilation_asymptote_correction_2026-07-23/AUDIT_REPORT.md":
        "fd3d99c357d158021151e12013158da13b0a4c30940bcec4c60f3cc7b7277164",
    "udt_xmax_dilation_asymptote_correction_2026-07-23/STATUS_LEDGER.tsv":
        "97d51fcc3db1e2521332f1c8476f65111865903991cc1a109c02a3d15c8984cd",
    "xmax_full_frame_realization_2026-07-19/AUDIT_REPORT.md":
        "01b4e7e4c1c2fabd983a98e227073d7b57e9df46816938ed2440ad714f2275d4",
    "xmax_dynamic_observer_frame_2026-07-19/AUDIT_REPORT.md":
        "3c23d222c94fc2bd219d188803bfd2174d38cb88809a273d0a303351267d0d2c",
    "xmax_accelerating_finite_cell_cartan_2026-07-19/AUDIT_REPORT.md":
        "bfcaaa7bfa0b9455c32f39ebbed38f8f166c097fd375e4c265f956e5df6799e8",
    "copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md":
        "5f3d9472388e9012af2b63d548bfbf91808a800b016d6c8e31be85dea6c2e2f0",
    "udt_two_frame_regime_metric_limit_audit_2026-07-22/AUDIT_REPORT.md":
        "cadc315cbb88fd3b418accada7b075f42883ec1c8ad3f4ac3ab98c7419ae1f8f",
    "udt_temporal_soldering_atlas_2026-07-22/AUDIT_REPORT.md":
        "85a568a215161e2f827ae5014dcf5a7d40f98c2697ea00a93ecff25171a16f3e",
    "udt_phi_causal_interface_atlas_2026-07-22/AUDIT_REPORT.md":
        "fbfced171bcb77377a850fc4562c3aff06df9f732c9ccc176faf37753325e2ec",
    "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md":
        "ce76d6236b78a2c70fb47c17740ea07949d5845b2065683905dc3218a3a0fbbc",
}


class ContractError(AssertionError):
    """Fail-closed science contract error."""


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, label: str, checks: dict[str, str]) -> None:
    if not condition:
        raise ContractError(label)
    checks[label] = "PASS"


def require_zero(name: str, value, checks: dict[str, str]) -> None:
    reduced = (
        value.applyfunc(lambda item: sp.simplify(sp.trigsimp(item)))
        if isinstance(value, sp.MatrixBase)
        else sp.simplify(sp.trigsimp(value))
    )
    entries = list(reduced) if isinstance(reduced, sp.MatrixBase) else [reduced]
    if any(entry != 0 for entry in entries):
        raise ContractError(f"{name}: {reduced}")
    checks[name] = "PASS"


def source_checks(checks: dict[str, str]) -> None:
    for relative, expected in SOURCE_HASHES.items():
        path = ROOT / relative
        require(path.is_file(), "source_exists:" + relative, checks)
        require(digest(path) == expected, "source_hash:" + relative, checks)


def status_contract(overrides: dict[str, object] | None = None) -> None:
    state: dict[str, object] = {
        "local_null_cone": "DERIVED_CONDITIONAL_WRL",
        "local_frame_group": "DERIVED_SO_PLUS_1_1",
        "local_light_speed": "c_E",
        "coordinate_light_speed": "c_E_A",
        "surface": "INVARIANT_NULL_SURFACE",
        "static_reach": "INFINITE_OPTICAL_TIME",
        "crossing": "REGULAR_CHART_WITNESS_EXISTS",
        "universal_uncrossability": "NOT_DERIVED",
        "global_recentering": "OBSTRUCTED_IN_FIXED_ANGULAR_WRL_SLICE",
        "variable_rapidity": "FREE_PURE_FRAME_CONNECTION",
        "observer_dynamics": "OPEN",
        "angular_hopf": "NOT_TESTED",
    }
    if overrides:
        state.update(overrides)
    expected = {
        "local_null_cone": "DERIVED_CONDITIONAL_WRL",
        "local_frame_group": "DERIVED_SO_PLUS_1_1",
        "local_light_speed": "c_E",
        "coordinate_light_speed": "c_E_A",
        "surface": "INVARIANT_NULL_SURFACE",
        "static_reach": "INFINITE_OPTICAL_TIME",
        "crossing": "REGULAR_CHART_WITNESS_EXISTS",
        "universal_uncrossability": "NOT_DERIVED",
        "global_recentering": "OBSTRUCTED_IN_FIXED_ANGULAR_WRL_SLICE",
        "variable_rapidity": "FREE_PURE_FRAME_CONNECTION",
        "observer_dynamics": "OPEN",
        "angular_hopf": "NOT_TESTED",
    }
    for key, value in expected.items():
        if state[key] != value:
            raise ContractError(f"{key}:{state[key]}")


def catch_proofs() -> list[dict[str, str]]:
    mutations = [
        ("C01", {"local_null_cone": "IMPORTED_FROM_GR"}),
        ("C02", {"local_frame_group": "ASSUMED_LORENTZ_TRANSFORM"}),
        ("C03", {"local_light_speed": "c_E_A"}),
        ("C04", {"coordinate_light_speed": "c_E"}),
        ("C05", {"surface": "CURVATURE_SINGULARITY"}),
        ("C06", {"static_reach": "FINITE_OPTICAL_TIME"}),
        ("C07", {"crossing": "NO_CROSSING"}),
        ("C08", {"universal_uncrossability": "DERIVED"}),
        ("C09", {"global_recentering": "FULL_WRL_HOMOTHETY"}),
        ("C10", {"variable_rapidity": "DYNAMIC_FORCE_FIELD"}),
        ("C11", {"observer_dynamics": "DERIVED_GEODESIC"}),
        ("C12", {"angular_hopf": "S2_CARRIER_DERIVED"}),
    ]
    output = []
    for catch_id, mutation in mutations:
        try:
            status_contract(mutation)
        except ContractError as error:
            output.append(
                {
                    "catch_id": catch_id,
                    "result": "PASS_REJECTED",
                    "reason": str(error),
                }
            )
        else:
            raise ContractError("mutation survived:" + catch_id)
    return output


def build_result() -> dict[str, object]:
    checks: dict[str, str] = {}
    source_checks(checks)

    r, X, c0 = sp.symbols("r X c_E", positive=True)
    t, v, u = sp.symbols("t v u", real=True)
    phi, beta, eta = sp.symbols("phi beta eta", real=True)
    kappa = sp.symbols("kappa", positive=True)
    A = 1 - r / X
    Aprime = sp.diff(A, r)
    Asecond = sp.diff(A, r, 2)

    # Exact radial metric and null slopes.
    g2 = sp.diag(-A * c0**2, 1 / A)
    g2_inverse = sp.simplify(g2.inv())
    require_zero("radial_metric_inverse", g2 * g2_inverse - sp.eye(2), checks)
    require_zero("radial_metric_determinant", g2.det() + c0**2, checks)
    null_plus = c0 * A
    null_minus = -c0 * A
    for name, slope in (("plus", null_plus), ("minus", null_minus)):
        require_zero(
            "coordinate_null_slope_" + name,
            -A * c0**2 + slope**2 / A,
            checks,
        )

    # Static orthonormal clock/ruler measurement.
    local_plus = sp.simplify((null_plus / sp.sqrt(A)) / sp.sqrt(A))
    local_minus = sp.simplify((null_minus / sp.sqrt(A)) / sp.sqrt(A))
    require_zero("static_local_light_speed_plus", local_plus - c0, checks)
    require_zero("static_local_light_speed_minus", local_minus + c0, checks)
    require_zero(
        "coordinate_light_speed_limit",
        sp.limit(null_plus, r, X, dir="-"),
        checks,
    )

    # Optical coordinate and conformal radial block.
    rstar = -X * sp.log(A)
    require_zero("tortoise_derivative", sp.diff(rstar, r) - 1 / A, checks)
    require(
        sp.limit(rstar, r, X, dir="-") == sp.oo,
        "tortoise_infinite_at_X",
        checks,
    )
    conformal = A * sp.diag(-1, 1)
    jac_t_rstar = sp.diag(1 / c0, A)
    require_zero(
        "optical_conformal_form",
        jac_t_rstar.T * g2 * jac_t_rstar - conformal,
        checks,
    )

    # Ingoing/outgoing charts use v=ct+rstar and u=ct-rstar.
    jac_ingoing = sp.Matrix([[1 / c0, -1 / (c0 * A)], [0, 1]])
    g_ingoing = sp.simplify(jac_ingoing.T * g2 * jac_ingoing)
    require_zero(
        "ingoing_metric",
        g_ingoing - sp.Matrix([[-A, 1], [1, 0]]),
        checks,
    )
    require_zero("ingoing_determinant", g_ingoing.det() + 1, checks)
    jac_outgoing = sp.Matrix([[1 / c0, 1 / (c0 * A)], [0, 1]])
    g_outgoing = sp.simplify(jac_outgoing.T * g2 * jac_outgoing)
    require_zero(
        "outgoing_metric",
        g_outgoing - sp.Matrix([[-A, -1], [-1, 0]]),
        checks,
    )
    require_zero("outgoing_determinant", g_outgoing.det() + 1, checks)

    # Surface and curvature character.
    normal_norm = g2_inverse[1, 1]
    killing_norm = g2[0, 0]
    require_zero(
        "X_surface_normal_null",
        sp.limit(normal_norm, r, X, dir="-"),
        checks,
    )
    require_zero(
        "static_Killing_field_null",
        sp.limit(killing_norm, r, X, dir="-"),
        checks,
    )
    ricci_scalar = sp.simplify(
        -Asecond - 4 * Aprime / r + 2 * (1 - A) / r**2
    )
    kretschmann = sp.simplify(
        Asecond**2
        + 4 * (Aprime / r) ** 2
        + 4 * ((1 - A) / r**2) ** 2
    )
    require_zero("ricci_scalar", ricci_scalar - 6 / (X * r), checks)
    require_zero(
        "kretschmann_scalar",
        kretschmann - 8 / (X**2 * r**2),
        checks,
    )
    require_zero(
        "finite_wall_ricci",
        sp.limit(ricci_scalar, r, X, dir="-") - 6 / X**2,
        checks,
    )
    require_zero(
        "finite_wall_kretschmann",
        sp.limit(kretschmann, r, X, dir="-") - 8 / X**4,
        checks,
    )

    # Static clocks require divergent proper acceleration near the surface.
    static_acceleration = c0**2 * sp.Abs(Aprime) / (2 * sp.sqrt(A))
    require_zero(
        "inverse_static_acceleration_tends_zero",
        sp.limit(1 / static_acceleration, r, X, dir="-"),
        checks,
    )
    require(
        sp.simplify(static_acceleration.subs(r, X / 2)) > 0,
        "static_acceleration_positive_inside",
        checks,
    )

    # Local connected Lorentz-frame family derived from metric preservation.
    minkowski = sp.diag(-1, 1)
    boost = sp.Matrix(
        [[sp.cosh(eta), sp.sinh(eta)], [sp.sinh(eta), sp.cosh(eta)]]
    )
    require_zero(
        "local_boost_preserves_metric",
        boost.T * minkowski * boost - minkowski,
        checks,
    )
    require_zero("local_boost_unit_determinant", boost.det() - 1, checks)
    null_plus_vector = sp.Matrix([1, 1])
    null_minus_vector = sp.Matrix([1, -1])
    require_zero(
        "null_plus_line_preserved",
        boost * null_plus_vector - sp.exp(eta) * null_plus_vector,
        checks,
    )
    require_zero(
        "null_minus_line_preserved",
        boost * null_minus_vector - sp.exp(-eta) * null_minus_vector,
        checks,
    )

    # Arbitrary smooth local rapidity adds only the metric-compatible gauge
    # term d eta in the radial SO+(1,1) connection.
    tt, rr = sp.symbols("tt rr", real=True)
    eta_field = sp.Function("eta")(tt, rr)
    mixed_residual = sp.diff(eta_field, tt, rr) - sp.diff(
        eta_field, rr, tt
    )
    require_zero("d_squared_eta_zero", mixed_residual, checks)
    base_connection_dt = sp.simplify(c0 * Aprime / 2)
    require_zero(
        "base_radial_spin_connection",
        base_connection_dt + c0 / (2 * X),
        checks,
    )
    require_zero(
        "radial_connection_curvature",
        sp.diff(base_connection_dt, r),
        checks,
    )

    # Exact regular crossing witnesses in the ingoing chart.
    timelike_crossing_norm = sp.simplify(-A - 2 * kappa)
    require_zero(
        "timelike_crossing_wall_norm",
        sp.limit(timelike_crossing_norm, r, X) + 2 * kappa,
        checks,
    )
    require(
        sp.limit(timelike_crossing_norm, r, X) < 0,
        "timelike_crossing_exists",
        checks,
    )
    null_crossing_norm = sp.Matrix([0, 1]).T * g_ingoing * sp.Matrix([0, 1])
    require_zero("ingoing_constant_v_null_crossing", null_crossing_norm[0], checks)

    # The corrected WR-L depth form and the angular obstruction to the older
    # constant-depth-shift frame homothety.
    Aphi = sp.exp(-2 * phi)
    rphi = X * (1 - Aphi)
    require_zero("WRL_depth_derivative", sp.diff(rphi, phi) - 2 * X * Aphi, checks)
    require_zero(
        "WRL_depth_radial_coframe_squared",
        (sp.diff(rphi, phi) ** 2 / Aphi) - 4 * X**2 * Aphi,
        checks,
    )
    block_common_ratio = sp.exp(2 * beta)
    angular_ratio = sp.simplify(
        (
            (1 - sp.exp(-2 * (phi - beta)))
            / (1 - sp.exp(-2 * phi))
        )
        ** 2
    )
    mismatch = sp.simplify(angular_ratio - block_common_ratio)
    require(
        mismatch != 0,
        "angular_ratio_not_common_homothety",
        checks,
    )
    witness = sp.simplify(
        angular_ratio.subs(
            {phi: sp.log(2), beta: sp.log(2) / 2}
        )
    )
    witness_block = sp.simplify(
        block_common_ratio.subs(beta, sp.log(2) / 2)
    )
    require_zero("angular_mismatch_witness", witness - sp.Rational(4, 9), checks)
    require_zero("block_ratio_witness", witness_block - 2, checks)
    require(
        witness != witness_block,
        "full_WRL_depth_shift_homothety_rejected",
        checks,
    )

    status_contract()
    catches = catch_proofs()
    require(len(catches) == 12, "catch_count_12", checks)

    return {
        "schema": "udt-wrl-xmax-lightcone-frame-1.0",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "result": "PASS",
        "grade": "VERIFIED-WITH-CAVEATS",
        "preregistration_commit": PREREG_COMMIT,
        "checks": checks,
        "check_count": len(checks),
        "source_hash_checks": len(SOURCE_HASHES),
        "catch_count": len(catches),
        "catch_pass_count": len(catches),
        "radial_lightcone": {
            "metric": "ds2_rad=-A c_E^2 dt^2+A^-1 dr^2",
            "A": "1-r/X",
            "coordinate_null_slopes": "dr/dt=+-c_E A",
            "local_static_speed": "+-c_E",
            "tortoise": "r_star=-X log(1-r/X)=2X phi",
            "null_coordinates": "u=c_E t-r_star; v=c_E t+r_star",
        },
        "surface": {
            "normal_norm": "g_inverse(dr,dr)=A -> 0",
            "Killing_norm": "g(partial_t,partial_t)=-A c_E^2 -> 0",
            "character": "INVARIANT_NULL_SURFACE_IN_RECORDED_WRL_GEOMETRY",
            "wall_Ricci": "6/X^2",
            "wall_Kretschmann": "8/X^4",
            "static_proper_acceleration": "c_E^2/(2X sqrt(A)) -> infinity",
        },
        "regular_extension": {
            "ingoing_metric": "ds2_rad=-A dv^2+2 dv dr",
            "ingoing_determinant": "-1",
            "null_crossing": "v=constant with varying r",
            "timelike_crossing": "dv=dlam; dr=-kappa dlam gives ds2=-(A+2kappa)dlam2",
            "ruling": "METRIC_ADMITS_CROSSING;GLOBAL_EXTENSION_OR_BOUNDARY_SELECTION_OPEN",
        },
        "observer_frames": {
            "local_group": "SO_PLUS(1,1) from orthonormal metric preservation",
            "null_action": "theta_plus->exp(eta)theta_plus; theta_minus->exp(-eta)theta_minus",
            "eta": "arbitrary smooth local rapidity field",
            "connection": "omega_prime=omega-deta in the registered coframe convention",
            "curvature_added_by_eta": "ZERO because d_squared_eta=0",
            "observer_dynamics": "NOT_SELECTED",
        },
        "global_recentering": {
            "WRL_depth_metric":
                "ds2=e^-2phi(-c_E^2dt^2+4X^2dphi^2)+X^2(1-e^-2phi)^2dOmega2",
            "constant_shift_radial_time_ratio": "exp(2beta)",
            "angular_ratio":
                "[(1-exp(-2(phi-beta)))/(1-exp(-2phi))]^2",
            "exact_witness": {
                "phi": "log(2)",
                "beta": "log(2)/2",
                "radial_time_ratio": "2",
                "angular_ratio": "4/9",
            },
            "ruling":
                "OLDER_CONSTANT_DEPTH_SHIFT_IS_NOT_A_FULL_WRL_HOMOTHETY_WITH_FIXED_ANGLES",
            "scope":
                "does not exclude a different complete angular transformation or nonspherical metric",
        },
        "maximum_conclusion": MAXIMUM,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build_result()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        (HERE / "DERIVATION_RESULT.json").write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
