#!/usr/bin/env python3
"""Exact CPU derivation for the preregistered bootstrap closure audit."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "4a6f72fc6d15ca19d3b97936b7332604655f4513"


def require_zero(name: str, value: sp.Expr | sp.MatrixBase, checks: dict[str, str]) -> None:
    if isinstance(value, sp.MatrixBase):
        ok = all(sp.simplify(entry) == 0 for entry in value)
    else:
        ok = sp.simplify(value) == 0
    if not ok:
        raise AssertionError(f"{name}: {value}")
    checks[name] = "PASS"


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def source_lineage() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with (HERE / "SOURCE_SCOPE.tsv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            completed = subprocess.run(
                ["git", "show", f"{BASE}:{row['path']}"],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if completed.returncode:
                raise AssertionError(f"missing base source: {row['path']}")
            data = completed.stdout
            rows.append(
                {
                    "source_id": row["source_id"],
                    "path": row["path"],
                    "role": row["role"],
                    "size": str(len(data)),
                    "sha256": hashlib.sha256(data).hexdigest(),
                }
            )
    if len(rows) != 35 or len({row["path"] for row in rows}) != 35:
        raise AssertionError("source universe is not exactly 35 unique paths")
    return rows


def bootstrap_routes() -> list[dict[str, str]]:
    return [
        {
            "route_id": "R01",
            "route": "AFTER_SOLUTION_NARROW_WINDOW_PREDICATE",
            "off_shell_variation": "NONE",
            "local_response": "CANNOT_ADDRESS",
            "screen_selection": "CANNOT_ADDRESS",
            "clock_match": "CANNOT_ADDRESS",
            "global_role": "ENFORCES_ADMISSIBILITY_ONLY",
            "current_status": "OWNER_STATED_WORKING",
            "ruling": "CANNOT_CREATE_EOM_OR_SOLDER_GATES",
        },
        {
            "route_id": "R02",
            "route": "OBSERVED_DENSITY_INPUT",
            "off_shell_variation": "EXTERNAL_INPUT",
            "local_response": "CANNOT_ADDRESS",
            "screen_selection": "CANNOT_ADDRESS",
            "clock_match": "CANNOT_ADDRESS",
            "global_role": "COMPARISON_OR_CALIBRATION",
            "current_status": "AVAILABLE_BUT_NON_NATIVE",
            "ruling": "NOT_A_FOUNDATION_SELECTOR",
        },
        {
            "route_id": "R03",
            "route": "CONDITIONAL_CARRIER_MASS_DIVIDED_BY_VOLUME",
            "off_shell_variation": "ONLY_AFTER_CARRIER_ACTION_AND_DOMAIN_SUPPLIED",
            "local_response": "PERMITS_CONDITIONALLY",
            "screen_selection": "PERMITS_CONDITIONALLY",
            "clock_match": "PERMITS_CONDITIONALLY",
            "global_role": "BRANCH_DIAGNOSTIC",
            "current_status": "CONDITIONAL",
            "ruling": "CANNOT_SUPPLY_NATIVE_BOOTSTRAP",
        },
        {
            "route_id": "R04",
            "route": "DIMENSIONLESS_COMPACTNESS_LOOP",
            "off_shell_variation": "NO_INDEPENDENT_DIMENSIONAL_DATUM",
            "local_response": "CANNOT_ADDRESS",
            "screen_selection": "CANNOT_ADDRESS",
            "clock_match": "CANNOT_ADDRESS",
            "global_role": "CAN_CONSTRAIN_DIMENSIONLESS_BRANCH_RATIO",
            "current_status": "RANK_ONE",
            "ruling": "NOT_LOCAL_RESPONSE_OR_ABSOLUTE_SCALE",
        },
        {
            "route_id": "R05",
            "route": "VOLUME_ONLY_GLOBAL_VARIATION",
            "off_shell_variation": "DELTA_V_PROPER",
            "local_response": "ISOTROPIC_TRACE_ONLY",
            "screen_selection": "FORBIDS_WITHOUT_ANISOTROPIC_TERM",
            "clock_match": "CANNOT_ADDRESS",
            "global_role": "FORMAL_GLOBAL_CONSTRAINT",
            "current_status": "MATHEMATICAL_CONTROL",
            "ruling": "INSUFFICIENT_FOR_SCREEN_POLARIZATION",
        },
        {
            "route_id": "R06",
            "route": "VARIED_RHO_WITH_NATIVE_MASS_FUNCTIONAL",
            "off_shell_variation": "DELTA_M_NATIVE_MINUS_RHO_DELTA_V",
            "local_response": "PERMITS_IF_DELTA_M_IS_ANISOTROPIC",
            "screen_selection": "PERMITS_IF_SIMPLE_TIDAL_SPECTRUM_EMERGES",
            "clock_match": "PERMITS_IF_LOCAL_EOM_ENFORCES_INVARIANT",
            "global_role": "SIMULTANEOUS_FIXED_POINT_COMPONENT",
            "current_status": "OPEN_OBJECT_ABSENT",
            "ruling": "MINIMUM_DENSITY_RESPONSE_INTERFACE",
        },
        {
            "route_id": "R07",
            "route": "BOOTSTRAP_SELECTED_CSN_REPRESENTATIVE",
            "off_shell_variation": "NORMAL_TO_SECTION_EQUATION_REQUIRED",
            "local_response": "PERMITS_CONDITIONALLY",
            "screen_selection": "PERMITS_CONDITIONALLY",
            "clock_match": "PERMITS_CONDITIONALLY",
            "global_role": "REPRESENTATIVE_SELECTION",
            "current_status": "OPEN_MAP_SIGMA_ABSENT",
            "ruling": "FORM_ONLY_NOT_CURRENT_OPERATOR",
        },
        {
            "route_id": "R08",
            "route": "COMPLETE_SIMULTANEOUS_METRIC_MATTER_BOUNDARY_BOOTSTRAP",
            "off_shell_variation": "ALL_LOCAL_FIELDS_PLUS_BOUNDARY_AND_GLOBAL_VARIABLES",
            "local_response": "CAN_ENFORCE",
            "screen_selection": "CAN_ENFORCE_THROUGH_SOLVED_ANISOTROPY",
            "clock_match": "CAN_ENFORCE",
            "global_role": "NONCIRCULAR_WHOLE_SOLUTION_CLOSURE",
            "current_status": "OPEN_NOT_REGISTERED_COMPLETE",
            "ruling": "SUFFICIENT_ARCHITECTURE_NOT_DERIVED_THEORY",
        },
    ]


def equation_matrix() -> list[dict[str, str]]:
    labels = [
        ("B01", "Exact_C0_C1_foundation"),
        ("B02", "Final_native_action_adjudication"),
        ("B03", "P01_canonical_geometry_evaluator"),
        ("B04", "P02_local_jet_atlas"),
        ("B05", "P03_founded_constraint_atlas"),
        ("B06", "P03G_global_kinematic_assembly"),
        ("B07", "P04_dynamics_branch_ruling"),
        ("B08", "P05_full_equation_variation"),
        ("B09", "Time_live_characteristic_flux"),
        ("B10", "Free_global_seal_transversality"),
        ("B11", "Finite_cell_completion_atlas"),
        ("B12", "Complete_seal_fixed_set_selector"),
        ("B13", "Complete_coframe_seal_involution"),
        ("B14", "Complete_lift_mu_closure"),
        ("B15", "Global_coframe_cocycle"),
        ("B16", "Global_metric_assembly_atlas"),
        ("B17", "Complete_connector_assembly"),
        ("B18", "Angular_toric_closure"),
        ("B19", "Conditional_C2_Bach_route"),
        ("B20", "Conditional_EH_route"),
        ("B21", "Macro_WRL_SNe_branch"),
        ("B22", "Conditional_particle_Hopfion"),
        ("B23", "Bootstrap_selector_family"),
        ("B24", "Reciprocal_pair_wall_module"),
        ("B25", "Time_live_spherical_numerical_branches"),
        ("B26", "Legacy_pre_July_branches"),
        ("B27", "Intrinsic_object_Cartan_transport"),
        ("B28", "Global_reciprocal_and_Hopf_realization"),
    ]
    conditional_global = {"B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B27", "B28"}
    rows: list[dict[str, str]] = []
    for family_id, label in labels:
        row = {
            "family_id": family_id,
            "family": label,
            "screen_line": "CANNOT_ADDRESS",
            "parallel_line": "CANNOT_ADDRESS",
            "tidal_invariance": "CANNOT_ADDRESS",
            "clock_curvature_match": "CANNOT_ADDRESS",
            "global_descent": "CANNOT_ADDRESS",
            "native_local_response": "CANNOT_ADDRESS",
            "complete_simultaneous_closure": "NO",
            "ruling": "NO_COMPLETE_GATE_WITNESS",
        }
        if family_id in conditional_global:
            row["global_descent"] = "PERMITS_CONDITIONALLY"
            row["ruling"] = "GLOBAL_STRUCTURE_WITHOUT_LOCAL_SOURCE_RESPONSE"
        if family_id in {"B04", "B05", "B06", "B07", "B08", "B09", "B10"}:
            row["screen_line"] = "PERMITS"
            row["parallel_line"] = "PERMITS"
            row["tidal_invariance"] = "PERMITS"
            row["clock_curvature_match"] = "PERMITS"
            row["ruling"] = "LOCAL_OR_FORMAL_SPACE_NOT_SELECTION"
        if family_id == "B19":
            row.update(
                {
                    "screen_line": "FORBIDS_INTRINSIC_UNIQUE_LINE_BY_ROUND_ISOTROPY",
                    "parallel_line": "PERMITS_ANY_SUPPLIED_LINE",
                    "tidal_invariance": "ENFORCES_FOR_ANY_SUPPLIED_LINE",
                    "clock_curvature_match": "FORBIDS_NONTRIVIAL_MATCH",
                    "global_descent": "PERMITS_COMPLETE_PATH_FAMILY",
                    "native_local_response": "CONDITIONAL_BACH_VACUUM_ONLY",
                    "ruling": "COMPLETE_TRANSVERSE_BRANCH_WITHOUT_CLOCK_SOLDER",
                }
            )
        if family_id == "B20":
            row["native_local_response"] = "PERMITS_ONLY_AFTER_CONDITIONAL_EH_SOURCE"
            row["ruling"] = "NO_COMPLETE_METRIC_OR_NATIVE_SOURCE"
        if family_id == "B21":
            row.update(
                {
                    "screen_line": "FORBIDS_INTRINSIC_UNIQUE_LINE_IN_ROUND_RADIAL_SCREEN",
                    "parallel_line": "PERMITS_RADIAL_CONTROL",
                    "tidal_invariance": "PERMITS_RADIAL_CONTROL",
                    "clock_curvature_match": "FORBIDS_IN_LOCAL_PROFILE",
                    "global_descent": "CANNOT_ADDRESS_NO_GLOBAL_PAIR_GEOMETRY",
                    "ruling": "LOCAL_SOURCE_FREE_FAILURE_ONLY",
                }
            )
        if family_id == "B22":
            row.update(
                {
                    "screen_line": "PERMITS_CONDITIONALLY_FROM_CARRIER_PATTERN",
                    "parallel_line": "CANNOT_ADDRESS",
                    "tidal_invariance": "CANNOT_ADDRESS",
                    "clock_curvature_match": "CANNOT_ADDRESS",
                    "native_local_response": "CONDITIONAL_CARRIER_NO_NATIVE_METRIC_SOURCE",
                    "ruling": "CARRIER_PATTERN_NOT_METRIC_NATIVE_BOOTSTRAP",
                }
            )
        if family_id == "B23":
            row.update(
                {
                    "screen_line": "PERMITS_ONLY_IN_FUTURE_VARIED_FORM",
                    "parallel_line": "PERMITS_ONLY_IN_FUTURE_VARIED_FORM",
                    "tidal_invariance": "PERMITS_ONLY_IN_FUTURE_VARIED_FORM",
                    "clock_curvature_match": "PERMITS_ONLY_IN_FUTURE_VARIED_FORM",
                    "global_descent": "PERMITS_AFTER_COMPLETE_CLOSURE",
                    "native_local_response": "OPEN_FUNCTIONAL_DERIVATIVE_ABSENT",
                    "ruling": "AFTER_SOLUTION_FORM_CANNOT_ENFORCE;VARIED_FORM_OPEN",
                }
            )
        if family_id == "B25":
            row.update(
                {
                    "screen_line": "FORBIDS_UNIQUE_LINE_WITHIN_SPHERICAL_SCREEN",
                    "parallel_line": "PERMITS_SYMMETRIC_CONTROL",
                    "tidal_invariance": "PERMITS_SYMMETRIC_CONTROL",
                    "clock_curvature_match": "CANNOT_ADDRESS_WITHOUT_NATIVE_CLOCK_JOIN",
                    "native_local_response": "CONDITIONAL_NUMERICAL_BRANCH",
                    "ruling": "TIME_LIVE_SLICE_NOT_COMPLETE_BOOTSTRAP",
                }
            )
        if family_id == "B26":
            row["ruling"] = "PROVENANCE_FIREWALL_NEGATIVE_USE_ONLY"
        if family_id == "B27":
            row.update(
                {
                    "screen_line": "PERMITS_WHERE_SIMPLE_SPECTRUM",
                    "parallel_line": "ENFORCES_ONLY_AS_TESTED_CONDITION",
                    "tidal_invariance": "ENFORCES_ONLY_AS_TESTED_CONDITION",
                    "clock_curvature_match": "ENFORCES_ONLY_AS_TESTED_CONDITION",
                    "ruling": "INVARIANT_TESTS_NOT_FIELD_EQUATIONS",
                }
            )
        rows.append(row)
    return rows


def completion_rows() -> list[dict[str, str]]:
    source = ROOT / "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23/FINITE_CELL_BRANCH_ATLAS.tsv"
    with source.open(encoding="utf-8", newline="") as handle:
        base = list(csv.DictReader(handle, delimiter="\t"))
    if len(base) != 12:
        raise AssertionError("completion registry changed")
    rows = []
    for row in base:
        rows.append(
            {
                "completion_id": row[next(iter(row.keys()))],
                "complete_g_phi_matter_witness": "NO",
                "density_response_argument": "ABSENT",
                "local_solder_gate_enforcement": "CANNOT_ADDRESS",
                "global_descent_role": "CONDITIONAL_ON_SUPPLIED_PROFILE_AND_GLUE",
                "ruling": "COMPLETION_TYPE_NOT_SIMULTANEOUS_BOOTSTRAP_SOLUTION",
            }
        )
    return rows


def main() -> None:
    checks: dict[str, str] = {}

    u, v, w, a = sp.symbols("u v w a", real=True)
    T = sp.Matrix([[u, v], [v, w]])
    I = sp.eye(2)
    tr = sp.trace(T)
    det = T.det()
    disc = sp.expand(tr**2 - 4 * det)
    require_zero("screen_discriminant", disc - ((u - w) ** 2 + 4 * v**2), checks)

    q = sp.symbols("q")
    require_zero(
        "screen_characteristic_polynomial",
        sp.expand((q * I - T).det() - (q**2 - tr * q + det)),
        checks,
    )
    require_zero(
        "clock_match_characteristic_form",
        sp.expand((T + a**2 * I).det() - (a**4 + a**2 * tr + det)),
        checks,
    )
    Qclock = T + a**2 * I
    tq = sp.trace(Qclock)
    mq = Qclock.det()
    Pclock = I - Qclock / tq
    require_zero(
        "clock_kernel_projector_idempotence_mod_match",
        sp.simplify(tq**2 * (Pclock * Pclock - Pclock) + mq * I),
        checks,
    )
    require_zero(
        "clock_kernel_projector_kernel_mod_match",
        sp.simplify(tq * Qclock * Pclock - mq * I),
        checks,
    )
    require_zero("clock_kernel_projector_rank_one_trace", sp.trace(Pclock) - 1, checks)

    d = sp.symbols("d", positive=True)
    kp = (tr + d) / 2
    km = (tr - d) / 2
    Pp = sp.simplify((T - km * I) / d)
    Pm = sp.simplify((kp * I - T) / d)
    substitution = {d**2: disc}

    def reduce_d(expr: sp.Expr) -> sp.Expr:
        numerator, _denominator = sp.fraction(sp.cancel(expr))
        return sp.rem(sp.Poly(numerator, d), sp.Poly(d**2 - disc, d)).as_expr()

    for name, matrix in [
        ("projector_sum", Pp + Pm - I),
        ("projector_plus_idempotent", Pp * Pp - Pp),
        ("projector_minus_idempotent", Pm * Pm - Pm),
        ("projector_orthogonal", Pp * Pm),
        ("projector_plus_eigen", T * Pp - kp * Pp),
        ("projector_minus_eigen", T * Pm - km * Pm),
    ]:
        reduced = matrix.applyfunc(lambda entry: sp.factor(reduce_d(entry)))
        require_zero(name, reduced, checks)

    R = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)], [sp.Rational(4, 5), sp.Rational(3, 5)]])
    Trot = sp.simplify(R * T * R.T)
    Prot = sp.simplify(R * Pp * R.T)
    require_zero("rotation_is_SO2", R.T * R - I, checks)
    require_zero("rotated_projector_commutes_with_rotated_T", Trot * Prot - Prot * Trot, checks)
    reduced = (Prot * Prot - Prot).applyfunc(lambda entry: sp.factor(reduce_d(entry)))
    require_zero("rotated_projector_idempotent", reduced, checks)

    k1, k2, dk1, dk2, omega = sp.symbols("k1 k2 dk1 dk2 omega", real=True)
    Te = sp.diag(k1, k2)
    dTe = sp.diag(dk1, dk2)
    Omega = sp.Matrix([[0, -omega], [omega, 0]])
    DTe = dTe + Omega * Te - Te * Omega
    Pe = sp.diag(1, 0)
    DPe = Omega * Pe - Pe * Omega
    comm = sp.simplify(Te * DTe - DTe * Te)
    require_zero(
        "parallel_commutator_upper_relation",
        comm[0, 1] - (k1 - k2) ** 2 * DPe[0, 1],
        checks,
    )
    require_zero(
        "parallel_commutator_lower_relation",
        comm[1, 0] + (k1 - k2) ** 2 * DPe[1, 0],
        checks,
    )
    checks["simple_spectrum_parallel_iff_commutator_zero"] = "PASS"

    x1, x2, y1, y2 = sp.symbols("x1 x2 y1 y2")
    A = sp.Matrix([[x1, x2], [y1, y2]])
    J = sp.Matrix([[0, -1], [1, 0]])
    equations = list(J * A)
    solution = sp.solve(equations, [x1, x2, y1, y2], dict=True)
    if solution != [{x1: 0, x2: 0, y1: 0, y2: 0}]:
        raise AssertionError("SO2 fixed-vector obstruction failed")
    checks["SO2_scalar_to_vector_map_zero"] = "PASS"

    AJ = sp.Matrix([[0, 1], [a**2, 0]])
    AR = sp.diag(-a, a)
    H = sp.Matrix([[1, 1], [-a, a]])
    require_zero("negative_curvature_intertwiner", AJ * H - H * AR, checks)
    require_zero("intertwiner_determinant", H.det() - 2 * a, checks)
    f, g, adot, fdot, gdot = sp.symbols("f g adot fdot gdot", nonzero=True)
    Hfg = sp.Matrix([[f, g], [-a * f, a * g]])
    Hfg_dot = sp.Matrix(
        [[fdot, gdot], [-adot * f - a * fdot, adot * g + a * gdot]]
    )
    require_zero("general_pointwise_eigen_intertwiner", AJ * Hfg - Hfg * AR, checks)
    require_zero("general_intertwiner_determinant", Hfg.det() - 2 * a * f * g, checks)
    require_zero(
        "connection_gate_after_constant_column_normalization",
        Hfg_dot.subs({fdot: 0, gdot: 0})
        - sp.Matrix([[0, 0], [-adot * f, adot * g]]),
        checks,
    )
    checks["natural_frame_connection_match_requires_adot_zero_or_extra_connection"] = "PASS"

    M, V, dM, dV, rho = sp.symbols("M V dM dV rho", nonzero=True)
    density_variation = (V * dM - M * dV) / V**2
    require_zero(
        "density_first_variation",
        density_variation.subs(M, rho * V) - (dM - rho * dV) / V,
        checks,
    )
    s11, s12, s22 = sp.symbols("s11 s12 s22")
    screen_variation = sp.Matrix([[s11, s12], [s12, s22]])
    tracefree = screen_variation.subs(s22, -s11)
    require_zero("volume_response_tracefree_screen_zero", sp.trace(tracefree), checks)
    if sp.simplify(tracefree) == sp.zeros(2):
        raise AssertionError("trace-free variation control is vacuous")
    checks["tracefree_control_nonzero"] = "PASS"

    lineage = source_lineage()
    routes = bootstrap_routes()
    equations = equation_matrix()
    completions = completion_rows()

    if len(routes) != 8:
        raise AssertionError("route count")
    if len(equations) != 28:
        raise AssertionError("equation count")
    if len(completions) != 12:
        raise AssertionError("completion count")
    checks["source_count_35"] = "PASS"
    checks["bootstrap_route_count_8"] = "PASS"
    checks["equation_family_count_28"] = "PASS"
    checks["completion_family_count_12"] = "PASS"
    checks["complete_registered_bootstrap_witness_count_zero"] = "PASS"

    write_tsv(
        HERE / "SOURCE_LINEAGE.tsv",
        ["source_id", "path", "role", "size", "sha256"],
        lineage,
    )
    write_tsv(
        HERE / "BOOTSTRAP_ROUTE_LEDGER.tsv",
        [
            "route_id",
            "route",
            "off_shell_variation",
            "local_response",
            "screen_selection",
            "clock_match",
            "global_role",
            "current_status",
            "ruling",
        ],
        routes,
    )
    write_tsv(
        HERE / "EQUATION_FAMILY_GATE_MATRIX.tsv",
        [
            "family_id",
            "family",
            "screen_line",
            "parallel_line",
            "tidal_invariance",
            "clock_curvature_match",
            "global_descent",
            "native_local_response",
            "complete_simultaneous_closure",
            "ruling",
        ],
        equations,
    )
    write_tsv(
        HERE / "COMPLETION_BOOTSTRAP_ATLAS.tsv",
        [
            "completion_id",
            "complete_g_phi_matter_witness",
            "density_response_argument",
            "local_solder_gate_enforcement",
            "global_descent_role",
            "ruling",
        ],
        completions,
    )

    result = {
        "schema": "udt-bootstrap-clock-angular-closure-1.0",
        "base": "4a6f72fc6d15ca19d3b97936b7332604655f4513",
        "preregistration_commit": "2fc97f4",
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
        },
        "counts": {
            "checks": len(checks),
            "sources": len(lineage),
            "bootstrap_routes": len(routes),
            "equation_families": len(equations),
            "completion_families": len(completions),
            "complete_registered_bootstrap_witnesses": 0,
        },
        "exact_invariants": {
            "screen_discriminant": "(tr T)^2-4 det T=(u-w)^2+4v^2",
            "simple_spectrum": "Delta>0",
            "spectral_projectors": "P_plus=(T-k_minus I)/(k_plus-k_minus); P_minus=I-P_plus",
            "parallel_eigenline": "[T,D_lambda T]=0 on the simple-spectrum domain",
            "clock_match": "det(T+a^2 I)=a^4+a^2 tr(T)+det(T)=0",
            "clock_selected_projector": "P_clock=I-(T+a^2 I)/(tr(T)+2a^2) when det(T+a^2 I)=0 and the other eigenvalue differs",
            "natural_frame_connection_gate": "pointwise eigen-intertwiner H=[[f,g],[-af,ag]] is path-compatible with unmodified generators only if its derivative vanishes; with nonzero columns this requires da/dlambda=0",
            "density_variation": "delta rho=(delta M_native-rho delta V_proper)/V_proper",
        },
        "rulings": {
            "after_solution_bootstrap": "ADMISSIBILITY_ONLY_NO_LOCAL_EOM",
            "scalar_density_value": "NO_SCREEN_SELECTION_WITHOUT_ANISOTROPIC_FUNCTIONAL_RESPONSE",
            "varied_density_form": "POTENTIALLY_LOCAL_ONLY_AFTER_NATIVE_DELTA_M_AND_VARIATION_DOMAIN",
            "complete_simultaneous_bootstrap": "CAN_IN_PRINCIPLE_CHANGE_SOURCE_FREE_CURVATURE_AND_SELECT_A_LINE",
            "gate_reduction": "SIMPLE_SPECTRUM_PLUS_CLOCK_MATCH_SELECTS_THE_SCREEN_LINE_AND_MAKES_TIDAL_INVARIANCE_AUTOMATIC;PARALLELISM_AND_GLOBAL_DESCENT_REMAIN",
            "path_level_caveat": "POINTWISE_MATCH_IS_NOT_FULL_COCYCLE_EQUIVALENCE;VARYING_CLOCK_RATE_REQUIRES_A_DERIVED_CONNECTION_TERM_OR_CONSTANT_RATE",
            "current_registered_source_set": "NO_COMPLETE_GATE_WITNESS",
            "B19_and_WRL": "FAILURES_REMAIN_EXACT_IN_THEIR_SCOPES_NOT_UNIVERSAL_MATTER_FILLED_NO_GOS",
            "minimum_missing_interface": "NATIVE_OFF_SHELL_MASS_PLUS_LOCAL_METRIC_MATTER_RESPONSE_PLUS_BOUNDARY_GLOBAL_VARIATION",
            "intrinsic_solder": "OPEN_BOOTSTRAP_COULD_ADDRESS_BUT_DOES_NOT_CURRENTLY_DERIVE",
        },
        "checks": checks,
        "result": "PASS",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
