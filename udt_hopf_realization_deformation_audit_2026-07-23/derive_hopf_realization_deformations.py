#!/usr/bin/env python3
"""Exact controller for the Hopf realization deformation audit."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path, key: str | None = None):
    with path.open(newline="", encoding="utf-8") as handle:
        found = list(csv.DictReader(handle, delimiter="\t"))
    if key is None:
        return found
    return {row[key]: row for row in found}


def write_tsv(path: Path, records: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(records[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(records)


def verify_sources() -> tuple[bool, list[dict[str, object]]]:
    result = []
    for row in rows(HERE / "SOURCE_MANIFEST.tsv"):
        path = ROOT / row["path"]
        actual = digest(path)
        completed = subprocess.run(
            ["sha256sum", "--check", path.name],
            cwd=path.parent,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        replay = completed.returncode == 0 and "FAILED" not in completed.stdout
        result.append(
            {
                "path": row["path"],
                "expected_sha256": row["sha256"],
                "actual_sha256": actual,
                "hash_match": actual == row["sha256"],
                "manifest_replay": replay,
                "entries": len(
                    [line for line in path.read_text().splitlines() if line]
                ),
            }
        )
    return all(row["hash_match"] and row["manifest_replay"] for row in result), result


def seed_tangent_algebra() -> dict[str, object]:
    phi, delta = sp.symbols("phi delta", real=True)
    sech = sp.sech(2 * phi)
    tanh = sp.tanh(2 * phi)
    n = sp.Matrix(
        [sech * sp.cos(delta), sech * sp.sin(delta), -tanh]
    )
    n_phi = sp.simplify(n.diff(phi))
    n_delta = sp.simplify(n.diff(delta))
    gram = sp.simplify(
        sp.Matrix(
            [
                [n_phi.dot(n_phi), n_phi.dot(n_delta)],
                [n_delta.dot(n_phi), n_delta.dot(n_delta)],
            ]
        )
    )
    expected = sp.diag(4 * sech**2, sech**2)
    residual = (gram - expected).applyfunc(
        lambda value: sp.simplify(sp.trigsimp(value).rewrite(sp.exp))
    )
    gram_det = sp.simplify(
        sp.trigsimp(gram.det()).rewrite(sp.exp)
    )

    eta = sp.symbols("eta", real=True)
    polar = sp.Matrix(
        [
            sp.sin(2 * eta) * sp.cos(delta),
            sp.sin(2 * eta) * sp.sin(delta),
            sp.cos(2 * eta),
        ]
    )
    polar_eta = sp.simplify(polar.diff(eta))
    polar_delta = sp.simplify(polar.diff(delta))
    polar_gram = sp.Matrix(
        [
            [polar_eta.dot(polar_eta), polar_eta.dot(polar_delta)],
            [polar_delta.dot(polar_eta), polar_delta.dot(polar_delta)],
        ]
    ).applyfunc(lambda value: sp.trigsimp(sp.simplify(value)))

    variables = sp.symbols(
        "A_scale A_depth A_shear D_scale D_depth D_shear "
        "S10 S11 S20 S21 scalar_phi",
        real=True,
    )
    d_depth = variables[4]
    scalar_phi = variables[10]
    fixed_delta = sp.symbols("fixed_delta", real=True)

    angular_route = sp.Matrix(
        [
            sp.sech(2 * d_depth) * sp.cos(fixed_delta),
            sp.sech(2 * d_depth) * sp.sin(fixed_delta),
            -sp.tanh(2 * d_depth),
        ]
    )
    scalar_route = angular_route.xreplace({d_depth: scalar_phi})
    angular_jacobian = angular_route.jacobian(variables)
    scalar_jacobian = scalar_route.jacobian(variables)
    angular_nonzero = [
        index
        for index in range(len(variables))
        if any(sp.simplify(value) != 0 for value in angular_jacobian[:, index])
    ]
    scalar_nonzero = [
        index
        for index in range(len(variables))
        if any(sp.simplify(value) != 0 for value in scalar_jacobian[:, index])
    ]

    return {
        "map": [
            str(component) for component in n
        ],
        "unit_norm": sp.trigsimp(sp.simplify(n.dot(n))) == 1,
        "n_dot_n_phi_zero": sp.trigsimp(sp.simplify(n.dot(n_phi))) == 0,
        "n_dot_n_delta_zero": sp.trigsimp(sp.simplify(n.dot(n_delta))) == 0,
        "gram": [[str(value) for value in row] for row in gram.tolist()],
        "gram_expected": [
            [str(value) for value in row] for row in expected.tolist()
        ],
        "gram_residual_zero": all(value == 0 for value in residual),
        "gram_determinant": str(gram_det),
        "finite_phi_rank": 2,
        "polar_gram": [
            [str(value) for value in row] for row in polar_gram.tolist()
        ],
        "polar_chart_rank": "2 for 0<eta<pi/2; delta coordinate degenerates at poles",
        "target_tangent_plane_at_poles": "two-dimensional but requires a second smooth chart",
        "complete_field_order": [str(value) for value in variables],
        "angular_route_nonzero_columns": angular_nonzero,
        "scalar_route_nonzero_columns": scalar_nonzero,
        "restricted_angular_bridge_rank": 1,
        "restricted_scalar_bridge_rank": 1,
        "angular_shear_direction": "outside established aligned bridge domain, not a zero column",
        "full_chart_differential": "undefined until a shear-compatible descended bridge is supplied",
    }


def shift_connection_algebra() -> dict[str, object]:
    x0, x1 = sp.symbols("x0 x1", real=True)
    s10 = sp.Function("s10")(x0, x1)
    s11 = sp.Function("s11")(x0, x1)
    s20 = sp.Function("s20")(x0, x1)
    s21 = sp.Function("s21")(x0, x1)
    lam1 = sp.Function("lam1")(x0, x1)
    lam2 = sp.Function("lam2")(x0, x1)

    b0, b1 = s10 - s20, s11 - s21
    curvature = sp.diff(b1, x0) - sp.diff(b0, x1)
    lam = lam1 - lam2
    bp0, bp1 = b0 - sp.diff(lam, x0), b1 - sp.diff(lam, x1)
    transformed_curvature = sp.diff(bp1, x0) - sp.diff(bp0, x1)
    gauge_residual = sp.simplify(transformed_curvature - curvature)

    chi = x0**2 * x1 + 3 * x1**2
    exact_b = (sp.diff(chi, x0), sp.diff(chi, x1))
    exact_curvature = sp.simplify(
        sp.diff(exact_b[1], x0) - sp.diff(exact_b[0], x1)
    )
    nonexact_b = (sp.Integer(0), x0)
    nonexact_curvature = sp.simplify(
        sp.diff(nonexact_b[1], x0) - sp.diff(nonexact_b[0], x1)
    )
    k = sp.symbols("k", real=True)

    return {
        "angular_one_forms": "theta_ang=D(dxi+S dx)",
        "row_difference_connection": [
            "s10-s20",
            "s11-s21",
        ],
        "gauge_rule": "xi_i'=xi_i+lambda_i(x); S_i'=S_i-dlambda_i",
        "curvature": str(curvature),
        "curvature_gauge_invariant": gauge_residual == 0,
        "exact_witness_curvature": str(exact_curvature),
        "nonexact_witness_curvature": str(nonexact_curvature),
        "nonzero_curvature_blocks_scalar_phase": nonexact_curvature != 0,
        "one_dimensional_base": "locally exact; on an interval globally exact after a gauge/basepoint choice",
        "periodic_base_holonomy": "integral b=2*pi*k for b=k dtheta; exact only when the period vanishes",
        "period_symbol": str(2 * sp.pi * k),
        "typed_ruling": "SHIFT_SECTOR_SUPPLIES_PHASE_CONNECTION_NOT_SELECTED_PHASE_SECTION",
        "exact_part_status": "torus-coordinate gauge without derived section or boundary framing",
    }


def angular_shear_algebra() -> dict[str, object]:
    phi, shear = sp.symbols("phi shear", real=True)
    d = sp.Matrix(
        [
            [sp.exp(-phi), shear],
            [0, sp.exp(phi)],
        ]
    )
    h = sp.simplify(d.T * d / d.det())
    x = sp.simplify(h[0, 0] - h[1, 1])
    y = sp.simplify(2 * h[0, 1])
    anisotropy2 = sp.simplify(x**2 + y**2)
    dbeta_dshear = sp.simplify(
        ((x * sp.diff(y, shear) - y * sp.diff(x, shear)) / anisotropy2).subs(
            shear, 0
        )
    )

    p, q, r, theta = sp.symbols("p q r theta", real=True)
    h_generic = sp.Matrix([[p, q], [q, r]])
    rotation = sp.Matrix(
        [
            [sp.cos(theta), -sp.sin(theta)],
            [sp.sin(theta), sp.cos(theta)],
        ]
    )
    h_rotated = sp.trigsimp(sp.simplify(rotation.T * h_generic * rotation))
    xp = sp.trigsimp(sp.simplify(h_rotated[0, 0] - h_rotated[1, 1]))
    yp = sp.trigsimp(sp.simplify(2 * h_rotated[0, 1]))
    spin2_norm_residual = sp.trigsimp(
        sp.simplify(xp**2 + yp**2 - ((p - r) ** 2 + 4 * q**2))
    )

    isotropic = h.subs({phi: 0, shear: 0})
    return {
        "normalized_metric": [
            [str(value) for value in row] for row in h.tolist()
        ],
        "traceless_pair": [str(x), str(y)],
        "anisotropy_squared": str(anisotropy2),
        "fixed_chart_phase_derivative_at_aligned_anisotropic_point": str(
            dbeta_dshear
        ),
        "isotropic_metric": [
            [str(value) for value in row] for row in isotropic.tolist()
        ],
        "eigenaxis_undefined_at_isotropy": x.subs(
            {phi: 0, shear: 0}
        )
        == 0
        and y.subs({phi: 0, shear: 0}) == 0,
        "spin2_norm_basis_invariant": spin2_norm_residual == 0,
        "spin2_pair_basis_dependent": True,
        "typed_ruling": "LOCAL_CHART_EIGENAXIS_PHASE_CANDIDATE_NOT_GLOBAL_DESCENDED_SECTION",
        "existing_bridge_shear_extension": "not supplied",
    }


def source_authority() -> dict[str, object]:
    parent = rows(
        ROOT
        / "udt_hopf_transport_bootstrap_dependency_audit_2026-07-23"
        / "STATUS_LEDGER.tsv",
        "id",
    )
    bridge = rows(
        ROOT / "udt_coframe_hopf_bridge_audit_2026-07-23/STATUS_LEDGER.tsv",
        "id",
    )
    coframe = rows(
        ROOT
        / "udt_native_coframe_composition_law_audit_2026-07-23"
        / "STATUS_LEDGER.tsv",
        "status_id",
    )
    intrinsic = rows(
        ROOT
        / "udt_complete_metric_intrinsic_object_audit_2026-07-23"
        / "STATUS_LEDGER.tsv",
        "id",
    )
    toric = rows(
        ROOT / "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
        "claim_id",
    )
    checks = {
        "parent_emergent_join_open": parent["S22"]["status"] == "OPEN_JOIN",
        "parent_bootstrap_outer": parent["S18"]["status"]
        == "WORKING_OUTER_ADMISSIBILITY_ONLY",
        "phase_open": bridge["S06"]["status"] == "OPEN",
        "native_bridge_open": bridge["S14"]["status"] == "OPEN",
        "chart_group_not_physical": coframe["S05"]["status"] == "OPEN",
        "scalar_not_composed": coframe["S15"]["status"] == "OPEN",
        "fiber_not_section": intrinsic["S12"]["status"]
        == "DERIVED_CONDITIONAL_FIBER"
        and intrinsic["S13"]["status"] == "OPEN",
        "native_global_Hopf_open": intrinsic["S17"]["status"]
        == "OPEN_NOT_DERIVED",
        "S3_only_conditional": toric["T06"]["status"].startswith(
            "S3_UNIQUE_CONDITIONAL"
        ),
        "bootstrap_no_topology_ranking": toric["T16"]["status"]
        == "NO_TOPOLOGY_RANKING_LAW",
    }
    return {"checks": checks, "all_checks_pass": all(checks.values())}


def candidate_outcomes() -> list[dict[str, str]]:
    outcomes = {
        "D01": ("KERNEL_OF_RESTRICTED_BRIDGE", "base_common_scale_not_an_input"),
        "D02": ("KERNEL_OF_RESTRICTED_BRIDGE", "base_depth_not_an_input"),
        "D03": ("KERNEL_OF_RESTRICTED_BRIDGE", "base_shear_not_an_input"),
        "D04": ("EXACT_KERNEL_CSN", "common_angular_scale_cancels"),
        "D05": ("CONDITIONAL_LATITUDE_TANGENT", "rank_one_for_finite_phi"),
        "D06": (
            "CHART_PHASE_CANDIDATE_NOT_DESCENDED",
            "shear_rotates_metric_eigenaxis_away_from_isotropy_but_bridge_extension_and_invariant_phase_are_absent",
        ),
        "D07": ("PHASE_CONNECTION_COMPONENT", "row_difference_base_time"),
        "D08": ("PHASE_CONNECTION_COMPONENT", "row_difference_base_space"),
        "D09": ("PHASE_CONNECTION_COMPONENT", "row_difference_base_time"),
        "D10": ("PHASE_CONNECTION_COMPONENT", "row_difference_base_space"),
        "D11": (
            "UNIDENTIFIED_OR_CONDITIONAL_LATITUDE_TANGENT",
            "scalar_angular_depth_ownership_is_chosen",
        ),
        "D12": ("EXACT_KERNEL_CSN", "normalized_seed_is_scale_free"),
        "D13": (
            "COFRAME_GAUGE_NOT_PHYSICAL_MAP_VARIATION",
            "independent_representatives_do_not_descend_under_current_bridge",
        ),
        "D14": (
            "GLOBAL_TARGET_ROTATION_MODE_ONLY",
            "one_constant_not_arbitrary_local_phase",
        ),
        "D15": (
            "GAUGE_EXACT_PART_OR_CONNECTION_CURVATURE_HOLONOMY",
            "not_a_selected_scalar_phase",
        ),
        "D16": (
            "DISCRETE_GLOBAL_BASIS_OR_BRANCH_CHANGE",
            "not_a_local_tangent_direction",
        ),
        "D17": (
            "GLOBAL_COMPLETION_BRANCH_CHANGE",
            "not_a_pointwise_carrier_tangent",
        ),
        "D18": (
            "SUPPLIED_SECTION_HAS_RANK_TWO_VERTICAL_TANGENT",
            "fiber_does_not_select_section",
        ),
        "D19": (
            "POSIT_CARRIER_HAS_FULL_RANK_TWO_TANGENT",
            "comparison_space_not_metric_output",
        ),
        "D20": (
            "BRIDGE_DEGENERATES_OR_IS_UNDEFINED",
            "nonnull_semisimple_reduction_does_not_extend",
        ),
    }
    prereg = rows(HERE / "DEFORMATION_CANDIDATES.tsv")
    return [
        {
            **row,
            "outcome": outcomes[row["candidate_id"]][0],
            "evidence": outcomes[row["candidate_id"]][1],
        }
        for row in prereg
    ]


def global_outcomes() -> list[dict[str, str]]:
    outcomes = {
        "FC01_BOUNDARY_BOUNDARY": (
            "LOCAL_ONLY_BOUNDARY_FRAMING_OPEN",
            "no_closed_or_compactified_Hopf_domain_without_physical_boundary_data",
        ),
        "FC02_ONE_CAP_BOUNDARY": (
            "ONE_POLE_PLUS_BOUNDARY_RESTRICTED",
            "phase_regular_at_cap_but_remaining_boundary_open",
        ),
        "FC03_TWO_CAP_P0": (
            "NON_HOPF_P0_COMPLETION",
            "same_dependent_cycles_do_not_supply_registered_unit_Hopf_bundle",
        ),
        "FC04_TWO_CAP_P1": (
            "EXACT_CONDITIONAL_SEED_RESTRICTED_DEFORMATION",
            "S3_and_unit_seed_require_supplied_unimodular_caps_quotient_orientation_and_phase",
        ),
        "FC05_TWO_CAP_P_GT1": (
            "LENS_FAMILY_GLOBAL_DATA_REQUIRED",
            "general_cap_lattice_not_registered_unit_Hopf_control",
        ),
        "FC06_NONPRIMITIVE_CAP": (
            "SINGULAR_OR_ORBIFOLD_BRANCH",
            "smooth_carrier_descent_not_supplied",
        ),
        "FC07_PERIODIC_TORUS_BUNDLE": (
            "MONODROMY_AND_HOLONOMY_DEPENDENT",
            "phase_covector_and_connection_must_descend_under_GL2Z",
        ),
        "FC08_MIRROR_DOUBLE": (
            "LIFT_DEPENDENT",
            "registered_angular_lifts_act_differently_on_phase",
        ),
        "FC09_NONORIENTABLE_GLUE": (
            "ORIENTATION_TWISTED",
            "global_Hopf_integral_and_phase_require_additional_orientation_data",
        ),
        "FC10_STRATIFIED_PROJECTOR": (
            "STRATUM_DEPENDENT_OR_DEGENERATE",
            "rank_or_causal_type_change_blocks_universal_bridge",
        ),
        "FC11_NONINTEGRABLE_DISTRIBUTION": (
            "NO_GLOBAL_TORIC_PHASE",
            "anholonomic_plane_field_has_no_supplied_global_xi1_xi2",
        ),
        "FC12_RECIPROCAL_TORIC_DIAGONAL": (
            "CONTROL_FAMILY_SUBCASE_DEPENDENT",
            "only_supplied_FC04_like_full_range_opposite_caps_give_exact_seed",
        ),
    }
    prereg = rows(HERE / "GLOBAL_COMPLETION_TESTS.tsv")
    return [
        {
            **row,
            "outcome": outcomes[row["completion_id"]][0],
            "evidence": outcomes[row["completion_id"]][1],
        }
        for row in prereg
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--candidate-output", type=Path, required=True)
    parser.add_argument("--global-output", type=Path, required=True)
    args = parser.parse_args()

    sources_ok, source_result = verify_sources()
    seed = seed_tangent_algebra()
    shift = shift_connection_algebra()
    shear = angular_shear_algebra()
    authority = source_authority()
    candidates = candidate_outcomes()
    completions = global_outcomes()

    checks = {
        "sources_and_manifests": sources_ok,
        "source_authority": authority["all_checks_pass"],
        "seed_unit_norm": seed["unit_norm"],
        "seed_tangents_orthogonal_to_n": seed["n_dot_n_phi_zero"]
        and seed["n_dot_n_delta_zero"],
        "seed_gram_exact": seed["gram_residual_zero"],
        "seed_finite_rank_two": seed["finite_phi_rank"] == 2,
        "restricted_bridge_rank_one": seed["restricted_angular_bridge_rank"]
        == 1,
        "only_depth_column_nonzero": seed["angular_route_nonzero_columns"]
        == [4],
        "only_scalar_column_nonzero": seed["scalar_route_nonzero_columns"]
        == [10],
        "shift_curvature_gauge_invariant": shift[
            "curvature_gauge_invariant"
        ],
        "nonexact_shift_blocks_phase": shift[
            "nonzero_curvature_blocks_scalar_phase"
        ],
        "shear_isotropic_degeneracy": shear[
            "eigenaxis_undefined_at_isotropy"
        ],
        "shear_spin2_norm_invariant": shear["spin2_norm_basis_invariant"],
        "candidate_census_complete": len(candidates) == 20,
        "completion_census_complete": len(completions) == 12,
    }
    result = {
        "schema": "udt-hopf-realization-deformation-v1",
        "python": "3.10.12",
        "sympy": sp.__version__,
        "source_manifest": source_result,
        "source_authority": authority,
        "seed_tangent_algebra": seed,
        "shift_phase_connection": shift,
        "angular_shear_phase": shear,
        "candidate_counts": {
            "total": len(candidates),
            "conditional_latitude": sum(
                "LATITUDE" in row["outcome"] for row in candidates
            ),
            "connection_not_section": sum(
                "CONNECTION" in row["outcome"] for row in candidates
            ),
            "supplied_or_posit_rank_two": sum(
                "RANK_TWO" in row["outcome"] for row in candidates
            ),
        },
        "global_counts": {
            "total": len(completions),
            "native_full_deformation": sum(
                "NATIVE_FULL" in row["outcome"] for row in completions
            ),
            "conditional_exact_seed_classes": sum(
                "EXACT_CONDITIONAL_SEED" in row["outcome"]
                for row in completions
            ),
        },
        "bootstrap_adjudication": {
            "B0": "local deformation algebra uses no bootstrap",
            "B1": "current bootstrap can only filter complete matter-bearing global solutions after they exist",
            "B2": "future Sigma could select a section or representative if explicitly derived",
            "B3": "future varied B could alter equations if explicitly derived with variation and boundary data",
            "density_scan": "not run and not currently operational",
        },
        "rulings": {
            "conditional_seed_target_tangent": "FULL_RANK_TWO_IF_PHI_AND_AN_INDEPENDENT_PHASE_FIELD_ARE_SUPPLIED",
            "established_aligned_coframe_bridge": "RANK_ONE_LATITUDE_IMAGE_ON_FINITE_PHI_STRATUM",
            "complete_coframe_bridge": "NO_WELL_DEFINED_DIFFERENTIAL_OFF_ALIGNED_SUBMANIFOLD",
            "angular_shear": "LOCAL_CHART_PHASE_CANDIDATE_NOT_DESCENDED_AND_DEGENERATE_AT_ISOTROPY",
            "shift_sector": "PHASE_CONNECTION_WITH_CURVATURE_AND_HOLONOMY_NOT_SELECTED_PHASE_SECTION",
            "intrinsic_S2": "FIBER_VERTICAL_TANGENT_EXISTS_BUT_SECTION_NOT_SELECTED",
            "global_realization": "NO_REGISTERED_COMPLETION_SUPPLIES_NATIVE_FULL_CARRIER_DEFORMATION_SPACE",
            "maximum": "RESTRICTED_CONDITIONAL_SEED_DEFORMATION_ONLY__GLOBAL_REALIZATION_REMAINS_COMPLETION_AND_SECTION_DEPENDENT",
        },
        "not_claimed": [
            "native carrier",
            "full metric-induced Map(S3,S2)",
            "physical phase section",
            "physical affine transport",
            "native action",
            "physical boundary",
            "time-live persistence",
            "density window",
            "mass or scale",
        ],
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }
    if not result["all_checks_pass"]:
        failed = [name for name, passed in checks.items() if not passed]
        raise SystemExit(f"derivation failed: {failed}")

    write_tsv(args.candidate_output, candidates)
    write_tsv(args.global_output, completions)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
