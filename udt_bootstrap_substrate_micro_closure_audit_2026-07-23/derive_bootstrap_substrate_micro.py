#!/usr/bin/env python3
"""Exact bounded substrate-to-micro channel audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


CHANNEL_OUTCOMES = {
    "C01_PULLBACK_METRIC": (
        "METRIC_NATIVE_KINEMATIC_CHANNEL_WITH_EMBEDDING_SCOPE",
        "For a fixed embedding h=E^T g E and delta_h=E^T delta_g E; a preferred physical embedding is not selected.",
    ),
    "C02_PULLBACK_VOLUME": (
        "GEOMETRIC_AFTER_COMPLETION_AND_REPRESENTATIVE",
        "Proper measure follows from the induced metric but total volume needs a selected slice completion and physical representative.",
    ),
    "C03_ANGULAR_DEPTH": (
        "REGISTERED_COFRAME_SHAPE_CHANNEL_PHYSICAL_OWNERSHIP_OPEN",
        "The determinant-normalized angular block depends on reciprocal depth without selecting its carrier interpretation.",
    ),
    "C04_ANGULAR_SHEAR": (
        "LOCAL_CHART_PHASE_CANDIDATE_NOT_DESCENDED",
        "Shear changes the spin-two axis away from isotropy but does not define a global physical phase.",
    ),
    "C05_SHIFT_CONNECTION": (
        "PHASE_CONNECTION_DERIVED_IN_CHART",
        "The shift difference b combines with ddelta to form an invariant phase differential; delta itself is not selected.",
    ),
    "C06_SHIFT_CURVATURE": (
        "GAUGE_INVARIANT_CURVATURE_CHANNEL",
        "db is unchanged by b to b-dlambda and can carry global substrate information.",
    ),
    "C07_SHIFT_HOLONOMY": (
        "GLOBAL_HOLONOMY_COMPATIBILITY_CHANNEL",
        "Periods of b constrain global descent when the base is not contractible.",
    ),
    "C08_COMPLETION_CAPS": (
        "COMPLETION_DEPENDENT_SECTION_CONSTRAINT",
        "Caps and physical boundaries constrain regularity and framing but select no matter branch.",
    ),
    "C09_COMPLETION_MONODROMY": (
        "MONODROMY_DEPENDENT_DESCENT_CONSTRAINT",
        "GL2Z and orientation data constrain phase descent but are not selected.",
    ),
    "C10_COMMON_CONSTANT_SCALE": (
        "PURE_HOMOTHETY_DOES_NOT_REMOVE_COEFFICIENT_RULER",
        "For the scaled shape q changes coordinate size inversely; physical size and optimum energy retain the xi-kappa ruler.",
    ),
    "C11_NONCONSTANT_SCALE_PROFILE": (
        "CONDITIONAL_POSTSCALE_BACKGROUND_RESPONSE",
        "For the supplied action the pointwise E2 and E4 weights are q and q^-1; physical use requires a selected representative.",
    ),
    "C12_SCALE_GRADIENT_OPERATOR": (
        "CONDITIONAL_OPERATOR_GRADIENT_RESPONSE",
        "A nonconstant q enters the local Euler operator through grad(log q); this is an exact response witness, not a native matter law.",
    ),
    "C13_ANISOTROPIC_METRIC_RESPONSE": (
        "CONDITIONAL_ANISOTROPIC_E2_RESPONSE",
        "The E2 metric variation is generically nonzero and depends on the full induced metric.",
    ),
    "C14_FOUR_DERIVATIVE_METRIC_RESPONSE": (
        "CONDITIONAL_ANISOTROPIC_E4_RESPONSE",
        "The E4 metric variation is generically nonzero and has the opposite conformal trace weight in three dimensions.",
    ),
    "C15_BOUNDARY_TO_STABILITY": (
        "FIXED_BACKGROUND_SCOPE_DEPENDENCE",
        "The existing Hessian and basin evidence holds for its supplied flat finite box and does not test substrate-varying stability.",
    ),
    "C16_GLOBAL_CURVATURE_TO_MICRO": (
        "OPEN_NO_NATIVE_CURVATURE_TO_MATTER_LAW",
        "Curvature is metric-native but no current native matter operator states how it controls carrier existence.",
    ),
    "C17_PHI_PROFILE_TO_MICRO": (
        "METRIC_NATIVE_PHI_TO_LOCAL_GEOMETRY_CHANNEL",
        "The complete coframe makes the phi profile part of local angular geometry; its matter interpretation remains open.",
    ),
    "C18_AFTER_SOLUTION_WINDOW": (
        "WORKING_PRIMARY_GLOBAL_ADMISSIBILITY",
        "This is the presently explicit primary owner reading and current implemented role.",
    ),
    "C19_STRONG_LOCAL_WINDOW": (
        "WORKING_HYPOTHESIS_CHANNEL_ARCHITECTURE_EXISTS_DEPENDENCE_OPEN",
        "Global geometry can reach micro geometry and a conditional operator, but no derived rho-to-geometry or native stability law closes the fork.",
    ),
    "C20_SIMULTANEOUS_FIXED_POINT": (
        "OPEN_NATIVE_SIMULTANEOUS_CLOSURE",
        "The noncircular architecture is type-correct but native matter, mass, boundary and feedback arrows are absent.",
    ),
    "C21_VARIED_GLOBAL_CONSTRAINT": (
        "OPEN_CONDITIONAL_FORM_NOT_PRESENT",
        "No bootstrap functional B and variation domain are currently supplied.",
    ),
    "C22_SELECTION_MAP": (
        "OPEN_CONDITIONAL_FORM_NOT_PRESENT",
        "No Sigma map selecting representative or section is currently supplied.",
    ),
    "C23_DIRECT_DENSITY_COUPLING": (
        "REJECTED_DIRECT_INSERTION",
        "The owner rule forbids inserting global average density as a fitted local coupling or cutoff.",
    ),
    "C24_GR_DENSITY_CURVATURE": (
        "REJECTED_AS_UDT_DERIVATION",
        "A GR density-curvature equation may be a comparison but cannot provide affirmative UDT physics.",
    ),
}


REGRADE_OUTCOMES = {
    "R01_RECIPROCAL_KINEMATICS": (
        "UNCHANGED",
        "The audit uses but does not alter the exact kinematic derivation.",
    ),
    "R02_COMPLETE_COFRAME_GEOMETRY": (
        "UNCHANGED_AND_USED_AS_CHANNEL",
        "The complete coframe supplies the substrate-to-local geometric interface.",
    ),
    "R03_HOPF_TOPOLOGICAL_CORE": (
        "UNCHANGED_CONDITIONAL",
        "The topological definition remains conditional on supplied carrier and domain data.",
    ),
    "R04_CARRIER_STATUS": (
        "UNCHANGED_POSIT",
        "No global substrate channel by itself derives the round S2 carrier.",
    ),
    "R05_STATIC_STABILITY": (
        "UNCHANGED_FIXED_BACKGROUND_SCOPE",
        "The result remains valid but does not cover substrate-varying backgrounds.",
    ),
    "R06_TIME_LIVE_STABILITY": (
        "UNCHANGED_OPEN",
        "No physical time evolution is solved.",
    ),
    "R07_ACTION_STATUS": (
        "UNCHANGED",
        "No action is selected by the channel audit.",
    ),
    "R08_MASS_STATUS": (
        "UNCHANGED_OPEN_OR_CONDITIONAL",
        "No native source or unconditional mass is derived.",
    ),
    "R09_BOOTSTRAP_AFTER_SOLUTION": (
        "QUALIFIED_CURRENT_ROLE_NOT_EXHAUSTIVE_OWNER_HYPOTHESIS",
        "Outer admissibility is the current explicit role; the owner source separately retains the stronger local fork.",
    ),
    "R10_NO_DENSITY_SCAN": (
        "UNCHANGED_DENSITY_GATE_PRE_DENSITY_GEOMETRIC_BRACKETING_ALLOWED",
        "Metric backgrounds may be bracketed before native density exists, but must not be labeled density values.",
    ),
    "R11_SELECTOR_NEGATIVES": (
        "RETAIN_SCOPED_NEGATIVES_JOINT_BOOTSTRAP_UNTESTED",
        "Fixed-background or local candidate failures do not test a complete simultaneous universe-plus-matter solve.",
    ),
    "R12_DIMENSIONAL_RULER": (
        "RETAINED_UNIFORM_SCALE_INSUFFICIENT",
        "Constant homothety does not remove sqrt(kappa/xi) or derive its value.",
    ),
    "R13_COMPLETION_CENSUS": (
        "UNCHANGED_TAXONOMY",
        "No completion class is selected.",
    ),
    "R14_HOPF_DEFORMATION": (
        "LOCAL_RESULT_RETAINED_GLOBAL_COMPATIBILITY_CHANNEL_ADDED",
        "Shear and shift conclusions remain; completion and holonomy can constrain but do not select a section.",
    ),
    "R15_XMAX_STATUS": (
        "BOOTSTRAP_EXPLICITLY_BROADER_THAN_XMAX_SELECTION",
        "The owner principle concerns matter-bearing self-consistency and may constrain micro existence as well as global scale.",
    ),
}


COMPLETION_CHANNELS = {
    "FC01_BOUNDARY_BOUNDARY": (
        "BOUNDARY_DATA_REQUIRED",
        "PHYSICAL_PHASE_FRAMING_OPEN",
    ),
    "FC02_ONE_CAP_BOUNDARY": (
        "ONE_CAP_ONE_BOUNDARY_VOLUME_CONDITIONAL",
        "CAP_REGULARITY_PLUS_BOUNDARY_FRAMING",
    ),
    "FC03_TWO_CAP_P0": (
        "CLOSED_VOLUME_AFTER_REPRESENTATIVE",
        "DEPENDENT_CAP_CYCLES_BLOCK_UNIT_HOPF_CONTROL",
    ),
    "FC04_TWO_CAP_P1": (
        "CLOSED_VOLUME_AFTER_REPRESENTATIVE",
        "EXACT_CONDITIONAL_SEED_WITH_SUPPLIED_GLOBAL_DATA",
    ),
    "FC05_TWO_CAP_P_GT1": (
        "LENS_VOLUME_AFTER_REPRESENTATIVE",
        "CAP_LATTICE_AND_QUOTIENT_DEPENDENT",
    ),
    "FC06_NONPRIMITIVE_CAP": (
        "SINGULAR_OR_ORBIFOLD_MEASURE_DEPENDENT",
        "EXCEPTIONAL_STABILIZER_DATA_REQUIRED",
    ),
    "FC07_PERIODIC_TORUS_BUNDLE": (
        "PERIODIC_VOLUME_AFTER_MONODROMY_AND_REPRESENTATIVE",
        "HOLONOMY_AND_GL2Z_DESCENT_DEPENDENT",
    ),
    "FC08_MIRROR_DOUBLE": (
        "DOUBLE_VOLUME_AFTER_LIFT_AND_REPRESENTATIVE",
        "MIRROR_LIFT_DEPENDENT",
    ),
    "FC09_NONORIENTABLE_GLUE": (
        "VOLUME_POSSIBLE_ORIENTATION_DATA_DEPENDENT",
        "ORIENTATION_TWISTED",
    ),
    "FC10_STRATIFIED_PROJECTOR": (
        "STRATUM_MEASURE_DEPENDENT",
        "RANK_CHANGE_BLOCKS_UNIVERSAL_SECTION",
    ),
    "FC11_NONINTEGRABLE_DISTRIBUTION": (
        "ANHOLONOMIC_VOLUME_GEOMETRICALLY_POSSIBLE",
        "NO_GLOBAL_TORIC_PHASE",
    ),
    "FC12_RECIPROCAL_TORIC_DIAGONAL": (
        "ENDPOINT_SUBCASE_DEPENDENT",
        "ONLY_FC04_LIKE_SUBCASE_HAS_EXACT_SEED",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def exact_algebra() -> dict[str, object]:
    checks: list[dict[str, object]] = []

    def check(name: str, expression: sp.Expr | sp.MatrixBase, expected: object = 0) -> None:
        if isinstance(expression, sp.MatrixBase):
            passed = expression == sp.zeros(*expression.shape)
            rendered = str(expression)
        else:
            reduced = sp.simplify(expression)
            passed = reduced == expected
            rendered = str(reduced)
        checks.append({"name": name, "passed": bool(passed), "value": rendered})

    # Fixed-embedding pullback variation.
    epsilon = sp.symbols("epsilon")
    e = sp.Matrix(4, 3, lambda a, i: sp.symbols(f"e{a}{i}"))
    g_symbols = sp.symbols("g00:04 g10:14 g20:24 g30:34")
    dg_symbols = sp.symbols("d00:04 d10:14 d20:24 d30:34")
    g = sp.Matrix(4, 4, g_symbols)
    dg = sp.Matrix(4, 4, dg_symbols)
    pullback_difference = sp.expand(
        e.T * (g + epsilon * dg) * e - e.T * g * e - epsilon * e.T * dg * e
    )
    check("fixed_embedding_pullback_variation", pullback_difference)

    # Exact conformal weights in d=3.
    q = sp.symbols("q", positive=True)
    volume_weight = q**3
    e2_weight = sp.simplify(volume_weight * q**-2)
    e4_weight = sp.simplify(volume_weight * q**-4)
    check("e2_conformal_weight", e2_weight - q)
    check("e4_conformal_weight", e4_weight - q**-1)

    # Nonconstant conformal profile enters a local scalar Euler operator.
    x = sp.symbols("x")
    qf = sp.Function("q")(x)
    uf = sp.Function("u")(x)
    divergence = sp.diff(qf * sp.diff(uf, x), x)
    expanded = qf * sp.diff(uf, x, 2) + sp.diff(qf, x) * sp.diff(uf, x)
    check("weighted_scalar_euler_identity", divergence - expanded)
    laplace_h = qf**-3 * divergence
    laplace_expected = qf**-2 * (
        sp.diff(uf, x, 2)
        + sp.diff(sp.log(qf), x) * sp.diff(uf, x)
    )
    check("conformal_laplacian_d3_identity", laplace_h - laplace_expected)

    # Constant homothety and scaled-shape control.
    xi, kappa, a, b, radius = sp.symbols(
        "xi kappa A B R", positive=True
    )
    energy = xi * q * a * radius + kappa * q**-1 * b / radius
    radius_star = sp.sqrt(kappa * b / (xi * a)) / q
    check(
        "constant_q_stationarity",
        sp.diff(energy, radius).subs(radius, radius_star),
    )
    physical_radius = sp.simplify(q * radius_star)
    check(
        "constant_q_physical_radius_independent",
        sp.diff(physical_radius, q),
    )
    energy_star = sp.simplify(energy.subs(radius, radius_star))
    check("constant_q_optimum_energy", energy_star - 2 * sp.sqrt(xi * kappa * a * b))

    # Metric-variation conformal trace controls in d=3.
    dimension, sigma = sp.symbols("d sigma")
    e2_trace_factor = (dimension - 2) * sigma
    e4_trace_factor = (dimension - 4) * sigma
    check("e2_metric_variation_trace_d3", e2_trace_factor.subs(dimension, 3) - sigma)
    check("e4_metric_variation_trace_d3", e4_trace_factor.subs(dimension, 3) + sigma)

    # Relative phase plus shift connection.
    delta, lam = sp.Function("delta")(x), sp.Function("lambda")(x)
    bfield = sp.Function("b")(x)
    transformed = sp.diff(delta + lam, x) + bfield - sp.diff(lam, x)
    check("phase_covariant_derivative_invariant", transformed - (sp.diff(delta, x) + bfield))

    xx, yy = sp.symbols("x y")
    bx = sp.Function("bx")(xx, yy)
    by = sp.Function("by")(xx, yy)
    lam2 = sp.Function("lambda")(xx, yy)
    curvature = sp.diff(by, xx) - sp.diff(bx, yy)
    transformed_curvature = sp.diff(by - sp.diff(lam2, yy), xx) - sp.diff(
        bx - sp.diff(lam2, xx), yy
    )
    check("shift_curvature_invariant", transformed_curvature - curvature)

    return {
        "checks": checks,
        "passed": sum(1 for row in checks if row["passed"]),
        "total": len(checks),
        "all_pass": all(row["passed"] for row in checks),
        "expressions": {
            "e2_metric_variation": (
                "(xi/2) int sqrt(h) ["
                "(1/2)h^(ab)h^(ij)G_ij-h^(ia)h^(jb)G_ij] delta h_ab"
            ),
            "e4_metric_variation": (
                "kappa int sqrt(h) ["
                "(1/8)h^(ab)F^2-(1/2)F^a_c F^(bc)] delta h_ab"
            ),
            "scaled_energy": str(energy),
            "coordinate_radius_star": str(radius_star),
            "physical_radius_star": str(physical_radius),
            "optimum_energy": str(energy_star),
        },
    }


def validate_sources() -> list[dict[str, object]]:
    manifest = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    rows: list[dict[str, object]] = []
    for row in manifest:
        path = ROOT / row["source_path"]
        observed = sha256(path)
        rows.append(
            {
                "source_path": row["source_path"],
                "expected": row["sha256"],
                "observed": observed,
                "passed": observed == row["sha256"],
            }
        )

    owner = (ROOT / "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md").read_text(
        encoding="utf-8"
    )
    phrase_checks = {
        "owner_primary_global_reading": "**Primary global reading:**" in owner,
        "owner_stronger_local_reading": "**Stronger local reading:**" in owner,
        "owner_no_nonlocal_insertion": "**No nonlocal insertion:**" in owner,
        "coframe_complete_angular_form": "theta_ang = D(dxi + S dx)"
        in (ROOT / "udt_hopf_realization_deformation_audit_2026-07-23/AUDIT_REPORT.md").read_text(
            encoding="utf-8"
        ),
        "conditional_continuum_functional": "E = int [ (xi/2)"
        in (ROOT / "noNull_energy.py").read_text(encoding="utf-8"),
    }
    rows.extend(
        {
            "source_path": name,
            "expected": "present",
            "observed": "present" if passed else "missing",
            "passed": passed,
        }
        for name, passed in phrase_checks.items()
    )
    return rows


def classify_channels(output: Path) -> list[dict[str, str]]:
    candidates = read_tsv(HERE / "CHANNEL_CANDIDATES.tsv")
    if {row["id"] for row in candidates} != set(CHANNEL_OUTCOMES):
        raise AssertionError("candidate universe mismatch")
    rows = []
    for row in candidates:
        outcome, reason = CHANNEL_OUTCOMES[row["id"]]
        rows.append(
            {
                "id": row["id"],
                "channel": row["channel"],
                "origin": row["origin"],
                "outcome": outcome,
                "reason": reason,
                "matter_closure": "NOT_CLOSED",
            }
        )
    write_tsv(
        output,
        ["id", "channel", "origin", "outcome", "reason", "matter_closure"],
        rows,
    )
    return rows


def classify_regrades(output: Path) -> list[dict[str, str]]:
    contract = read_tsv(HERE / "PRIOR_RESULT_REGRADE_CONTRACT.tsv")
    if {row["id"] for row in contract} != set(REGRADE_OUTCOMES):
        raise AssertionError("regrade universe mismatch")
    rows = []
    for row in contract:
        disposition, reason = REGRADE_OUTCOMES[row["id"]]
        rows.append(
            {
                "id": row["id"],
                "prior_scope": row["current_scope"],
                "disposition": disposition,
                "reason": reason,
            }
        )
    write_tsv(output, ["id", "prior_scope", "disposition", "reason"], rows)
    return rows


def classify_fixed_point(output: Path) -> list[dict[str, str]]:
    rows = read_tsv(HERE / "FIXED_POINT_ARROW_CENSUS.tsv")
    outcomes = []
    for row in rows:
        defined = row["current_status"] in {
            "EXACT_KINEMATIC",
            "EXACT_IN_CHART",
            "EXACT_CONDITIONAL",
            "TYPED_DEFINITION",
            "OBSERVATIONAL_ANCHORS",
        }
        if row["arrow_id"] == "F14":
            disposition = "REJECTED_DIRECT_INSERTION"
        elif defined:
            disposition = "DEFINED_WITH_RECORDED_SCOPE"
        elif row["current_status"].startswith("OPEN"):
            disposition = "OPEN_ARROW"
        else:
            disposition = "CONDITIONAL_OR_WORKING_ARROW"
        outcomes.append({**row, "disposition": disposition})
    write_tsv(
        output,
        list(rows[0].keys()) + ["disposition"],
        outcomes,
    )
    return outcomes


def classify_completions(output: Path) -> list[dict[str, str]]:
    source_rows = read_tsv(
        ROOT
        / "udt_hopf_realization_deformation_audit_2026-07-23"
        / "GLOBAL_COMPLETION_OUTCOMES.tsv"
    )
    if {row["completion_id"] for row in source_rows} != set(COMPLETION_CHANNELS):
        raise AssertionError("completion universe mismatch")
    rows = []
    for row in source_rows:
        volume_channel, phase_channel = COMPLETION_CHANNELS[row["completion_id"]]
        rows.append(
            {
                "completion_id": row["completion_id"],
                "topology_or_role": row["topology_or_role"],
                "volume_channel": volume_channel,
                "phase_channel": phase_channel,
                "micro_geometry_channel": "PRESENT_AFTER_BRANCH_DATA",
                "density_status": "UNDEFINED_BEFORE_NATIVE_MASS_AND_PHYSICAL_VOLUME",
                "matter_closure": "NOT_SUPPLIED",
            }
        )
    write_tsv(
        output,
        [
            "completion_id",
            "topology_or_role",
            "volume_channel",
            "phase_channel",
            "micro_geometry_channel",
            "density_status",
            "matter_closure",
        ],
        rows,
    )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--channels", type=Path, required=True)
    parser.add_argument("--regrades", type=Path, required=True)
    parser.add_argument("--fixed-point", type=Path, required=True)
    parser.add_argument("--completions", type=Path, required=True)
    args = parser.parse_args()

    algebra = exact_algebra()
    sources = validate_sources()
    channels = classify_channels(args.channels)
    regrades = classify_regrades(args.regrades)
    fixed_point = classify_fixed_point(args.fixed_point)
    completions = classify_completions(args.completions)

    all_sources = all(bool(row["passed"]) for row in sources)
    exact_channel_count = sum(
        "METRIC_NATIVE" in row["outcome"]
        or "CONNECTION_DERIVED" in row["outcome"]
        or "CURVATURE_CHANNEL" in row["outcome"]
        or "HOLONOMY_COMPATIBILITY" in row["outcome"]
        for row in channels
    )
    conditional_response_count = sum(
        row["outcome"].startswith("CONDITIONAL") for row in channels
    )
    open_count = sum(
        "OPEN" in row["outcome"] or "WORKING_HYPOTHESIS" in row["outcome"]
        for row in channels
    )
    rejected_count = sum(row["outcome"].startswith("REJECTED") for row in channels)
    fixed_open = sum(row["disposition"] == "OPEN_ARROW" for row in fixed_point)

    result = {
        "schema": "udt-bootstrap-substrate-micro-closure-v1",
        "date": "2026-07-23",
        "base": "3e3237b",
        "mode": "CPU_ONLY_EXACT_AND_TYPED_AUDIT",
        "algebra": algebra,
        "source_checks": sources,
        "counts": {
            "channel_candidates": len(channels),
            "exact_or_geometric_channel_rows": exact_channel_count,
            "conditional_response_rows": conditional_response_count,
            "open_or_working_rows": open_count,
            "rejected_rows": rejected_count,
            "regrade_rows": len(regrades),
            "fixed_point_arrows": len(fixed_point),
            "open_fixed_point_arrows": fixed_open,
            "completion_rows": len(completions),
        },
        "rulings": {
            "owner_bootstrap": (
                "PRIMARY_GLOBAL_ADMISSIBILITY_PLUS_SEPARATE_STRONGER_LOCAL_FORK"
            ),
            "global_to_micro_geometry": (
                "DERIVED_KINEMATIC_CHANNELS_WITH_EMBEDDING_REPRESENTATIVE_SCOPE"
            ),
            "conditional_hopf_action": (
                "BACKGROUND_SENSITIVE_AFTER_CARRIER_ACTION_AND_REPRESENTATIVE"
            ),
            "constant_homothety": (
                "DOES_NOT_REMOVE_CONDITIONAL_COEFFICIENT_RULER"
            ),
            "strong_local_bootstrap": (
                "WORKING_HYPOTHESIS_CHANNEL_ARCHITECTURE_EXISTS_DEPENDENCE_OPEN"
            ),
            "simultaneous_density_matter_closure": "OPEN_MISSING_NATIVE_ARROWS",
            "density_scan": "NOT_PERFORMED",
        },
        "maximum_conclusion": (
            "GLOBAL_SUBSTRATE_TO_MICRO_GEOMETRY_CHANNELS_DERIVED__"
            "CONDITIONAL_HOPF_OPERATOR_BACKGROUND_SENSITIVE__"
            "SIMULTANEOUS_DENSITY_MATTER_CLOSURE_REMAINS_OPEN"
        ),
        "all_checks_pass": bool(algebra["all_pass"] and all_sources),
        "authority_boundary": {
            "carrier_derived": False,
            "action_derived": False,
            "density_curvature_law_derived": False,
            "native_mass_or_source_derived": False,
            "physical_representative_selected": False,
            "completion_selected": False,
            "density_window_computed": False,
            "gpu_used": False,
        },
    }
    args.result.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if not result["all_checks_pass"]:
        raise SystemExit("production checks failed")
    print(
        "production=PASS "
        f"algebra={algebra['passed']}/{algebra['total']} "
        f"sources={sum(bool(row['passed']) for row in sources)}/{len(sources)} "
        f"channels={len(channels)} regrades={len(regrades)} "
        f"fixed_point={len(fixed_point)} completions={len(completions)}"
    )


if __name__ == "__main__":
    main()
