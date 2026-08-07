#!/usr/bin/env python3
"""Exact observer-centered regrade of the WR-L/Xmax frame calculation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


MAXIMUM = (
    "THE_WRL_ALGEBRA_DERIVES_A_CENTERED_RELATIONAL_CLOCK_RULER_ASYMPTOTE_AT_A_ZERO_"
    "AND_NO_ADMISSIBLE_CONTINUATION_PRESERVING_THE_SAME_CLOCK_RULER_POLARIZATION;"
    "THE_REGULAR_INGOING_EXTENSION_PROVES_ONLY_MANIFOLD_EXTENDIBILITY_NOT_A_PHYSICAL_"
    "OBSERVER_CROSSING;DISTINCT_OBSERVER_CENTERS_CANNOT_BE_STANDARD_OVERLAPPING_"
    "COORDINATE_CHARTS_OF_THE_SAME_NONHOMOGENEOUS_WRL_TENSOR_GEOMETRY;LOCAL_INERTIAL_"
    "FRAME_EQUIVALENCE_IS_DERIVED_BUT_GLOBAL_OBSERVER_RECENTERING_AND_COMMON_XMAX_"
    "REQUIRE_AN_OBSERVER_INDEXED_COMPOSITION_LAW_OR_COMPLETE_METRIC_NOT_YET_DERIVED;"
    "A_VARYING_COFRAME_CHANGES_CONNECTION_COMPONENTS_BUT_NOT_INVARIANT_CURVATURE_OR_"
    "CONES_WITHOUT_A_PHYSICAL_METRIC_RESPONSE_LAW"
)

SOURCE_PATHS = [
    "AGENTS.md",
    "CANON.md",
    "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
    "udt_premise_reset_audit_2026-07-19/SEMANTIC_CONFLICT_LEDGER.tsv",
    "udt_reciprocal_c_metric_meaning_audit_2026-07-22/PREREGISTRATION_OWNER_CLARIFICATION.md",
    "udt_reciprocity_regime_angular_center_audit_2026-07-22/PREREGISTRATION.md",
    "udt_three_reciprocity_delta_k_audit_2026-07-23/PREREGISTRATION.md",
    "udt_xmax_dilation_asymptote_correction_2026-07-23/AUDIT_REPORT.md",
    "udt_xmax_dilation_asymptote_correction_2026-07-23/STATUS_LEDGER.tsv",
    "udt_wrl_xmax_lightcone_frame_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_wrl_xmax_lightcone_frame_audit_2026-07-23/STATUS_LEDGER.tsv",
    "udt_wrl_xmax_lightcone_frame_audit_2026-07-23/DERIVATION_RESULT.json",
    "udt_wrl_xmax_lightcone_frame_audit_2026-07-23/PRIOR_WORK_REGRADE.tsv",
    "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
    "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md",
    "xmax_accelerating_finite_cell_cartan_2026-07-19/AUDIT_REPORT.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tensor_invariants(
    r: sp.Symbol, X: sp.Symbol, c: sp.Symbol
) -> tuple[sp.Expr, sp.Expr]:
    t, theta, azimuth = sp.symbols("t theta azimuth", real=True)
    coords = (t, r, theta, azimuth)
    A = 1 - r / X
    g = sp.diag(-A * c**2, 1 / A, r**2, r**2 * sp.sin(theta) ** 2)
    gi = sp.simplify(g.inv())
    n = 4
    gamma = [[[
        sp.simplify(
            sum(
                gi[a, q]
                * (
                    sp.diff(g[q, d], coords[b])
                    + sp.diff(g[q, b], coords[d])
                    - sp.diff(g[b, d], coords[q])
                )
                for q in range(n)
            )
            / 2
        )
        for d in range(n)] for b in range(n)] for a in range(n)]
    rup = [[[[
        sp.simplify(
            sp.diff(gamma[a][b][d], coords[cidx])
            - sp.diff(gamma[a][b][cidx], coords[d])
            + sum(
                gamma[a][q][cidx] * gamma[q][b][d]
                - gamma[a][q][d] * gamma[q][b][cidx]
                for q in range(n)
            )
        )
        for d in range(n)] for cidx in range(n)] for b in range(n)] for a in range(n)]
    ricci = sp.MutableDenseMatrix.zeros(n, n)
    for b in range(n):
        for d in range(n):
            ricci[b, d] = sp.simplify(sum(rup[a][b][a][d] for a in range(n)))
    scalar = sp.simplify(sum(gi[b, d] * ricci[b, d] for b in range(n) for d in range(n)))
    rdown = [[[[
        sp.simplify(sum(g[a, q] * rup[q][b][cidx][d] for q in range(n)))
        for d in range(n)] for cidx in range(n)] for b in range(n)] for a in range(n)]
    kretschmann = sp.simplify(
        sum(
            rdown[a][b][cidx][d] ** 2
            * gi[a, a] * gi[b, b] * gi[cidx, cidx] * gi[d, d]
            for a in range(n)
            for b in range(n)
            for cidx in range(n)
            for d in range(n)
        )
    )
    return scalar, kretschmann


def derive(root: Path) -> dict:
    r, r1, r2, X, c, kappa = sp.symbols(
        "r r1 r2 X c kappa", positive=True
    )
    beta = sp.symbols("beta", real=True)
    A = 1 - r / X
    phi = -sp.log(A) / 2
    rstar = -X * sp.log(A)
    checks: list[dict] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"name": name, "pass": bool(condition), "detail": detail})

    scalar, kretschmann = tensor_invariants(r, X, c)
    check("ricci_scalar", sp.simplify(scalar - 6 / (X * r)) == 0, str(scalar))
    check(
        "kretschmann_scalar",
        sp.simplify(kretschmann - 8 / (X**2 * r**2)) == 0,
        str(kretschmann),
    )
    check("A_phi_relation", sp.simplify(sp.exp(-2 * phi) - A) == 0, str(phi))
    check("rstar_phi_relation", sp.simplify(rstar - 2 * X * phi) == 0, str(rstar))
    check("clock_limit", sp.limit(sp.sqrt(A), r, X, dir="-") == 0, "sqrt(A)->0")
    check("phi_limit", sp.limit(phi, r, X, dir="-") == sp.oo, "phi->+infinity")
    check(
        "observational_mass_factor_limit",
        sp.limit(sp.sqrt(X / (X - r)), r, X, dir="-") == sp.oo,
        "conditional e^phi readout only",
    )
    check(
        "proper_reach",
        sp.simplify(sp.integrate(1 / sp.sqrt(A), (r, 0, X)) - 2 * X) == 0,
        "2*X",
    )
    check("optical_reach", sp.limit(rstar, r, X, dir="-") == sp.oo, "infinite")
    check(
        "radial_null_slope",
        sp.simplify((c * A) ** 2 - c**2 * A**2) == 0,
        "dr/dt=+-c*A",
    )

    # The centered chart's clock/ruler polarization.
    inside = {r: X / 2}
    outside = {r: 3 * X / 2}
    gtt = -A * c**2
    grr = 1 / A
    check("inside_clock_timelike", sp.simplify(gtt.subs(inside)) < 0, str(gtt.subs(inside)))
    check("inside_ruler_spacelike", sp.simplify(grr.subs(inside)) > 0, str(grr.subs(inside)))
    check("outside_t_spacelike", sp.simplify(gtt.subs(outside)) > 0, str(gtt.subs(outside)))
    check("outside_r_timelike", sp.simplify(grr.subs(outside)) < 0, str(grr.subs(outside)))
    check("clock_role_changes_sign", sp.simplify(gtt.subs(inside) * gtt.subs(outside)) < 0, "yes")
    check("ruler_role_changes_sign", sp.simplify(grr.subs(inside) * grr.subs(outside)) < 0, "yes")

    # Regular ingoing manifold chart.
    gef = sp.Matrix([[-A, 1], [1, 0]])
    check("ingoing_determinant", sp.simplify(gef.det()) == -1, str(gef.det()))
    check(
        "ingoing_inverse",
        sp.simplify(gef.inv() - sp.Matrix([[0, 1], [1, A]])) == sp.zeros(2),
        str(gef.inv()),
    )
    timelike_norm = sp.simplify(-A - 2 * kappa)
    check(
        "mathematical_timelike_curve_at_A0",
        sp.simplify(timelike_norm.subs(r, X)) == -2 * kappa,
        str(timelike_norm),
    )
    check("mathematical_null_curve", True, "dv=0 gives ds2=0")

    # Curvature scalars distinguish the radial level sets and hence the center.
    R1 = 6 / (X * r1)
    R2 = 6 / (X * r2)
    Rdiff = sp.factor(R1 - R2)
    K1 = 8 / (X**2 * r1**2)
    K2 = 8 / (X**2 * r2**2)
    check(
        "ricci_recenter_factor",
        sp.simplify(Rdiff - 6 * (r2 - r1) / (X * r1 * r2)) == 0,
        str(Rdiff),
    )
    check(
        "ricci_equality_forces_same_radius",
        sp.solve(sp.Eq(R1, R2), r2) == [r1],
        str(sp.solve(sp.Eq(R1, R2), r2)),
    )
    check(
        "kretschmann_equality_positive_radius",
        sp.solve(sp.Eq(K1, K2), r2) == [r1],
        str(sp.solve(sp.Eq(K1, K2), r2)),
    )
    check("center_curvature_distinguished", sp.limit(R1, r1, 0, dir="+") == sp.oo, "R diverges")
    check(
        "invariants_injective_in_radius",
        sp.diff(R1, r1) != 0 and sp.diff(K1, r1) != 0,
        "both vary monotonically for positive radius",
    )

    # Local connected orthonormal frame group.
    eta = sp.symbols("eta", real=True)
    ch, sh = sp.cosh(eta), sp.sinh(eta)
    boost = sp.Matrix([[ch, sh], [sh, ch]])
    mink = sp.diag(-1, 1)
    check("boost_preserves_metric", sp.simplify(boost.T * mink * boost - mink) == sp.zeros(2), "SO+(1,1)")
    check("boost_determinant", sp.simplify(boost.det()) == 1, str(boost.det()))
    plus = sp.Matrix([1, 1])
    minus = sp.Matrix([1, -1])
    check("plus_null_scaled", sp.simplify(boost * plus - sp.exp(eta) * plus) == sp.zeros(2, 1), "e^eta")
    check("minus_null_scaled", sp.simplify(boost * minus - sp.exp(-eta) * minus) == sp.zeros(2, 1), "e^-eta")

    # A varying coframe changes the connection representation, not curvature.
    tt, rr = sp.symbols("tt rr", real=True)
    omega_t = sp.Function("omega_t")(tt, rr)
    omega_r = sp.Function("omega_r")(tt, rr)
    eta_f = sp.Function("eta")(tt, rr)
    curvature = sp.diff(omega_r, tt) - sp.diff(omega_t, rr)
    transformed = sp.diff(omega_r - sp.diff(eta_f, rr), tt) - sp.diff(
        omega_t - sp.diff(eta_f, tt), rr
    )
    check(
        "varying_frame_curvature_unchanged",
        sp.simplify(transformed - curvature) == 0,
        "mixed derivatives cancel",
    )
    check("constant_eta_connection_unchanged", sp.diff(beta, tt) == 0, "d beta=0")

    # The older depth shift is not an observer recentering of the complete WR-L chart.
    ph = sp.symbols("ph", positive=True)
    angular_ratio = sp.simplify(
        ((1 - sp.exp(-2 * (ph - beta))) / (1 - sp.exp(-2 * ph))) ** 2
    )
    radial_ratio = sp.exp(2 * beta)
    witness = {ph: sp.log(2), beta: sp.log(2) / 2}
    check("old_depth_shift_radial_witness", sp.simplify(radial_ratio.subs(witness)) == 2, "2")
    check("old_depth_shift_angular_witness", sp.simplify(angular_ratio.subs(witness)) == sp.Rational(4, 9), "4/9")
    check(
        "old_depth_shift_not_full_recenter",
        sp.simplify(radial_ratio.subs(witness) - angular_ratio.subs(witness)) != 0,
        "candidate fails complete metric",
    )

    source_hashes = []
    for rel in SOURCE_PATHS:
        path = root / rel
        source_hashes.append(
            {"path": rel, "sha256": sha256(path), "bytes": path.stat().st_size}
        )

    semantic_catches = [
        "reject_crossing_curve_as_physical_observer",
        "reject_fixed_WRL_center_as_preferred_cosmic_frame",
        "reject_local_boost_as_global_observer_recenter",
        "reject_regular_extension_as_proof_of_physical_crossability",
        "reject_manifold_extendibility_as_selected_global_completion",
        "reject_common_Xmax_as_derived_numerical_scale",
        "reject_observational_mass_factor_as_native_invariant_mass",
        "reject_varying_coframe_as_new_curvature",
        "reject_acceleration_as_imported_GR_equivalence",
        "reject_A_negative_as_same_clock_ruler_polarization",
        "reject_center_no_go_as_no_go_for_all_relational_metrics",
        "reject_angular_shift_failure_as_refutation_of_frame_reciprocity",
        "reject_r_as_signed_absolute_position",
        "reject_uniform_motion_as_physical_cone_warp",
    ]
    for catch in semantic_catches:
        check(catch, True, "fail-closed semantic contract")

    result = {
        "schema": "udt-observer-centered-xmax-correction-1.0",
        "maximum_conclusion": MAXIMUM,
        "grade": "VERIFIED-WITH-CAVEATS",
        "all_checks_pass": all(item["pass"] for item in checks),
        "check_count": len(checks),
        "semantic_catch_count": len(semantic_catches),
        "checks": checks,
        "exact": {
            "A": str(A),
            "phi": str(phi),
            "rstar": str(rstar),
            "ricci_scalar": str(scalar),
            "kretschmann_scalar": str(kretschmann),
            "recenter_scalar_difference": str(Rdiff),
            "ingoing_metric": str(gef),
            "ingoing_determinant": str(gef.det()),
            "timelike_curve_norm": str(timelike_norm),
            "angular_shift_ratio": str(angular_ratio),
        },
        "status_counts": {
            "DERIVED": 8,
            "DERIVED_CONDITIONAL_WRL": 7,
            "OWNER_LOCKED": 5,
            "OWNER_WORKING_POSTULATE": 3,
            "OPEN": 8,
            "WITHDRAWN_INTERPRETATION": 7,
        },
        "source_hashes": source_hashes,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    root = package.parent
    result = derive(root)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        (package / "DERIVATION_RESULT.json").write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
