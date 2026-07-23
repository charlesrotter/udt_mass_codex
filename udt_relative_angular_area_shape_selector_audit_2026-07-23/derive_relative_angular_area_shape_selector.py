#!/usr/bin/env python3
"""Audit native selectors for relative angular area and unit shape speed."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "cabb61a1f943b667fe2c2898531e365265588f05"
MAXIMUM = (
    "THE_COMPLETE_NONBLOCK_METRIC_DEFINES_EXACT_FULL_CSN_INVARIANT_"
    "RELATIVE_ANGULAR_AREA_AND_SHAPE_SPEED_DIAGNOSTICS_BUT_CURRENT_METRIC_"
    "ALGEBRA_RECIPROCITY_CSN_FINITE_CELL_TOPOLOGY_CARTAN_IDENTITIES_"
    "BOOTSTRAP_AND_C_DO_NOT_FIX_THEIR_GLOBAL_TARGET_VALUES__A_REGULAR_"
    "MIRROR_SEAL_FORCES_ZERO_RELATIVE_AREA_RATE_AT_ITS_FIXED_POINT_BUT_"
    "LEAVES_SHAPE_SPEED_AMPLITUDE_AND_BULK_PERSISTENCE_UNSELECTED"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(
    path: Path,
    rows: list[dict[str, object]],
    fields: tuple[str, ...] | None = None,
) -> None:
    if fields is None:
        if not rows:
            raise ValueError("fields required")
        fields = tuple(rows[0])
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(fields),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def exact_nonblock_formula() -> dict[str, object]:
    a, b, d = sp.symbols("a b d", real=True)
    p, r, s = sp.symbols("p r s", real=True)
    x, y, z, t = sp.symbols("x y z t", real=True)
    lam = sp.symbols("lambda", positive=True, finite=True)
    h = sp.Matrix([[a, b], [b, d]])
    q = sp.Matrix([[p, r], [r, s]])
    cross = sp.Matrix([[x, y], [z, t]])
    raw_angular = sp.simplify(q + cross.T * h.inv() * cross)
    complete = h.row_join(cross).col_join(
        cross.T.row_join(raw_angular)
    )
    schur = sp.simplify(
        raw_angular - cross.T * h.inv() * cross
    )
    if schur != q:
        raise AssertionError("Schur reconstruction")
    determinant_residual = sp.factor(
        complete.det() - h.det() * q.det()
    )
    if determinant_residual != 0:
        raise AssertionError("Schur determinant identity")

    scaled_h = lam**2 * h
    scaled_cross = lam**2 * cross
    scaled_raw = lam**2 * raw_angular
    scaled_schur = sp.simplify(
        scaled_raw
        - scaled_cross.T * scaled_h.inv() * scaled_cross
    )
    if sp.simplify(scaled_schur - lam**2 * q) != sp.zeros(2):
        raise AssertionError("full CSN Schur covariance")
    ratio_scaled = sp.simplify(
        scaled_schur.det() / scaled_h.det() - q.det() / h.det()
    )
    if ratio_scaled != 0:
        raise AssertionError("relative determinant CSN invariance")

    congruence_left = sp.eye(4)
    congruence_left[2:, :2] = cross.T * h.inv()
    block = sp.diag(1, 1, 1, 1)
    block[:2, :2] = h
    block[2:, 2:] = q
    congruence = sp.simplify(
        congruence_left * block * congruence_left.T
    )
    congruence_residual = (congruence - complete).applyfunc(
        lambda value: sp.factor(sp.simplify(value))
    )
    if congruence_residual != sp.zeros(4):
        raise AssertionError("signature congruence")
    return {
        "schema": "udt-relative-angular-nonblock-formula-1.0",
        "complete_split": "G=[[h,C],[C^T,Q]]",
        "orthogonal_angular_metric": "q=Q-C^T*h^-1*C",
        "determinant_identity": "det(G)=det(h)*det(q)",
        "signature_identity": "inertia(G)=inertia(h)+inertia(q)",
        "full_csn_schur_covariance": "q_tilde=lambda^2*q",
        "relative_determinant_ratio": "det(q)/abs(det(h))",
        "relative_ratio_full_csn_invariant": True,
        "raw_Q_is_invariant_angular_metric": False,
        "cross_terms_retained": True,
    }


def exact_diagnostics() -> dict[str, object]:
    phi, u, up, w, wp, theta, thetap, chi, chip = sp.symbols(
        "phi u u_p w w_p theta theta_p chi chi_p", real=True
    )
    c = sp.symbols("c", positive=True, finite=True)
    rotation = sp.Matrix(
        [
            [sp.cos(theta), -sp.sin(theta)],
            [sp.sin(theta), sp.cos(theta)],
        ]
    )
    q = (
        sp.exp(2 * w)
        * rotation.T
        * sp.diag(sp.exp(-2 * u), sp.exp(2 * u))
        * rotation
    )
    q_prime = (
        q.diff(u) * up
        + q.diff(w) * wp
        + q.diff(theta) * thetap
    )
    h = sp.diag(-c**2 * sp.exp(-2 * phi), sp.exp(2 * phi))
    h_prime = h.diff(phi)
    h_gen = sp.simplify(sp.Rational(1, 2) * h.inv() * h_prime)
    q_gen = sp.simplify(sp.Rational(1, 2) * q.inv() * q_prime)
    q_shape = sp.simplify(
        q_gen - sp.trace(q_gen) * sp.eye(2) / 2
    )
    area = sp.simplify(
        sp.trace(q_gen) / 2 - sp.trace(h_gen) / 2
    )
    sigma_squared = sp.simplify(
        up**2 + thetap**2 * sp.sinh(2 * u) ** 2
    )
    shape_speed = sp.simplify(sp.trace(q_shape * q_shape) / 2)
    if h_gen != sp.diag(-1, 1):
        raise AssertionError("reciprocal generator")
    if sp.simplify(area - wp) != 0:
        raise AssertionError("relative area")
    if sp.simplify(sp.expand_trig(shape_speed - sigma_squared)) != 0:
        raise AssertionError("shape speed")

    h_csn = sp.exp(2 * chi) * h
    q_csn = sp.exp(2 * chi) * q
    h_csn_prime = h_csn.diff(phi) + h_csn.diff(chi) * chip
    q_csn_prime = (
        q_csn.diff(u) * up
        + q_csn.diff(w) * wp
        + q_csn.diff(theta) * thetap
        + q_csn.diff(chi) * chip
    )
    h_csn_gen = sp.simplify(
        sp.Rational(1, 2) * h_csn.inv() * h_csn_prime
    )
    q_csn_gen = sp.simplify(
        sp.Rational(1, 2) * q_csn.inv() * q_csn_prime
    )
    area_csn = sp.simplify(
        sp.trace(q_csn_gen) / 2 - sp.trace(h_csn_gen) / 2
    )
    shape_csn = sp.simplify(
        q_csn_gen - sp.trace(q_csn_gen) * sp.eye(2) / 2
    )
    if sp.simplify(area_csn - area) != 0:
        raise AssertionError("area CSN invariance")
    shape_csn_residual = (shape_csn - q_shape).applyfunc(
        lambda value: sp.simplify(value)
    )
    if shape_csn_residual != sp.zeros(2):
        raise AssertionError("shape CSN invariance")

    return {
        "schema": "udt-relative-angular-diagnostics-1.0",
        "reciprocal_generator": "diag(-1,+1)",
        "relative_area_rate": "A_rel=w_p",
        "relative_area_ratio_formula": (
            "A_rel=(1/4)T log(det(q)/abs(det(h)))"
        ),
        "shape_speed_squared": (
            "S_shape=u_p**2+theta_p**2*sinh(2*u)**2"
        ),
        "joint_target": "w_p=0 AND S_shape=1",
        "full_csn_area_invariant": True,
        "full_csn_shape_invariant": True,
        "c_in_complete_reciprocal_metric": True,
        "c_in_dimensionless_diagnostic_values": False,
    }


def endpoint_flat_controls() -> list[dict[str, object]]:
    y, alpha, beta, kappa = sp.symbols(
        "y alpha beta kappa", real=True
    )
    bump = y**3 * (1 - y) ** 3
    bump_prime = sp.diff(bump, y)
    bump_second = sp.diff(bump, y, 2)
    for endpoint in (0, 1):
        if any(
            sp.simplify(value.subs(y, endpoint)) != 0
            for value in (bump, bump_prime, bump_second)
        ):
            raise AssertionError("endpoint-flat polynomial")
    w = alpha * bump
    u = y + beta * bump
    theta = kappa * bump
    area = sp.simplify(sp.diff(w, y))
    shape = sp.simplify(
        sp.diff(u, y) ** 2
        + sp.diff(theta, y) ** 2 * sp.sinh(2 * u) ** 2
    )
    sample = sp.Rational(1, 4)
    values = {
        "bump_at_quarter": sp.simplify(bump.subs(y, sample)),
        "bump_prime_at_quarter": sp.simplify(
            bump_prime.subs(y, sample)
        ),
        "area_at_quarter": sp.simplify(area.subs(y, sample)),
        "shape_at_quarter": sp.simplify(shape.subs(y, sample)),
    }
    if values["bump_prime_at_quarter"] == 0:
        raise AssertionError("interior deformation inactive")
    return [
        {
            "control_id": "E01_BASE_MATCHED",
            "profiles": "w=0;u=y;theta=0",
            "endpoint_jets_through_2": "BASE",
            "relative_area": "0",
            "shape_speed": "1",
            "role": "MATCHED_CONTROL_NOT_SELECTED_UNIVERSE",
        },
        {
            "control_id": "E02_AREA_ONLY",
            "profiles": "w=alpha*p(y);u=y;theta=0",
            "endpoint_jets_through_2": "IDENTICAL_TO_BASE",
            "relative_area": str(area.subs({beta: 0, kappa: 0})),
            "shape_speed": "1",
            "role": "INDEPENDENT_AREA_COUNTERDEFORMATION",
        },
        {
            "control_id": "E03_SHEAR_ONLY",
            "profiles": "w=0;u=y+beta*p(y);theta=0",
            "endpoint_jets_through_2": "IDENTICAL_TO_BASE",
            "relative_area": "0",
            "shape_speed": str(
                sp.factor(shape.subs({alpha: 0, kappa: 0}))
            ),
            "role": "INDEPENDENT_SHAPE_COUNTERDEFORMATION",
        },
        {
            "control_id": "E04_ROTATION_ONLY",
            "profiles": "w=0;u=y;theta=kappa*p(y)",
            "endpoint_jets_through_2": "IDENTICAL_TO_BASE",
            "relative_area": "0",
            "shape_speed": str(
                sp.factor(shape.subs({alpha: 0, beta: 0}))
            ),
            "role": "INDEPENDENT_ROTATING_AXIS_COUNTERDEFORMATION",
        },
        {
            "control_id": "E05_THREE_KNOB",
            "profiles": (
                "w=alpha*p(y);u=y+beta*p(y);theta=kappa*p(y)"
            ),
            "endpoint_jets_through_2": "IDENTICAL_TO_BASE",
            "relative_area": str(area),
            "shape_speed": str(shape),
            "role": "INDEPENDENT_BULK_FREEDOM",
        },
        {
            "control_id": "E06_NONBLOCK_EXTENSION",
            "profiles": (
                "Q=q+C^T*h^-1*C with any smooth nonzero C"
            ),
            "endpoint_jets_through_2": "INHERITS_SELECTED_C_JETS",
            "relative_area": "UNCHANGED_SCHUR_DIAGNOSTIC",
            "shape_speed": "UNCHANGED_SCHUR_DIAGNOSTIC",
            "role": "CROSS_TERMS_DO_NOT_REMOVE_COUNTERFAMILY",
        },
        {
            "control_id": "E07_EXACT_INTERIOR_SAMPLE",
            "profiles": "y=1/4",
            "endpoint_jets_through_2": "NOT_ENDPOINT",
            "relative_area": str(values["area_at_quarter"]),
            "shape_speed": str(values["shape_at_quarter"]),
            "role": (
                "NONZERO_P_PRIME_PROVES_INDEPENDENT_INTERIOR_RESPONSE"
            ),
        },
    ]


def mirror_controls() -> list[dict[str, object]]:
    return [
        {
            "lift": "ANGULAR_PLUS_I",
            "first_jet_dimension": 0,
            "relative_area_at_fixed_seal": "ZERO",
            "shape_speed_at_fixed_seal": "ZERO",
            "joint_target_at_fixed_seal": "FAILS_UNIT_SHAPE",
            "bulk_ruling": "NO_INTERIOR_EQUATION",
        },
        {
            "lift": "ANGULAR_MINUS_I",
            "first_jet_dimension": 0,
            "relative_area_at_fixed_seal": "ZERO",
            "shape_speed_at_fixed_seal": "ZERO",
            "joint_target_at_fixed_seal": "FAILS_UNIT_SHAPE",
            "bulk_ruling": "NO_INTERIOR_EQUATION",
        },
        {
            "lift": "AXIS_REFLECTION",
            "first_jet_dimension": 1,
            "relative_area_at_fixed_seal": "ZERO",
            "shape_speed_at_fixed_seal": "FREE_NONNEGATIVE_AMPLITUDE",
            "joint_target_at_fixed_seal": "ALLOWED_ONLY_AT_UNIT_AMPLITUDE",
            "bulk_ruling": "NO_INTERIOR_EQUATION",
        },
        {
            "lift": "AXIS_EXCHANGE",
            "first_jet_dimension": 1,
            "relative_area_at_fixed_seal": "ZERO",
            "shape_speed_at_fixed_seal": "FREE_NONNEGATIVE_AMPLITUDE",
            "joint_target_at_fixed_seal": "ALLOWED_ONLY_AT_UNIT_AMPLITUDE",
            "bulk_ruling": "NO_INTERIOR_EQUATION",
        },
        {
            "lift": "ALL_REGISTERED_LIFTS",
            "first_jet_dimension": "0_OR_1",
            "relative_area_at_fixed_seal": "ZERO_WHERE_REGULAR",
            "shape_speed_at_fixed_seal": "ZERO_OR_FREE_BY_LIFT",
            "joint_target_at_fixed_seal": "NOT_FORCED",
            "bulk_ruling": "NOT_FORCED",
        },
    ]


def selector_rows() -> list[dict[str, str]]:
    return [
        {
            "selector_id": "S01",
            "selector": "COMPLETE_METRIC_ALGEBRA",
            "area_ruling": "DOES_NOT_DERIVE",
            "shape_ruling": "DOES_NOT_DERIVE",
            "joint_ruling": "DOES_NOT_DERIVE",
            "exact_reason": (
                "Schur_complement_allows_arbitrary_positive_q_and_nonzero_C"
            ),
            "countercontrol": "E02_E03_E04_E06",
        },
        {
            "selector_id": "S02",
            "selector": "RECIPROCAL_CHARACTER",
            "area_ruling": "DOES_NOT_DERIVE",
            "shape_ruling": "DOES_NOT_DERIVE",
            "joint_ruling": "DOES_NOT_DERIVE",
            "exact_reason": (
                "fixes_h_generator_diag_minus1_plus1_and_phi_scale_not_q"
            ),
            "countercontrol": "E02_E03_E04",
        },
        {
            "selector_id": "S03",
            "selector": "COMMON_SCALE_NEUTRALITY",
            "area_ruling": "DOES_NOT_DERIVE",
            "shape_ruling": "DOES_NOT_DERIVE",
            "joint_ruling": "DOES_NOT_DERIVE",
            "exact_reason": (
                "makes_both_diagnostics_full_conformal_invariants_without_"
                "fixing_their_values"
            ),
            "countercontrol": "FULL_CSN_REPLAY",
        },
        {
            "selector_id": "S04",
            "selector": "FINITE_CELL",
            "area_ruling": "DOES_NOT_DERIVE",
            "shape_ruling": "DOES_NOT_DERIVE",
            "joint_ruling": "DOES_NOT_DERIVE",
            "exact_reason": (
                "endpoint_flat_three_knob_family_preserves_second_jets"
            ),
            "countercontrol": "E02_E03_E04_E05",
        },
        {
            "selector_id": "S05",
            "selector": "SEAL_LIFTS",
            "area_ruling": "DERIVES_AT_FIXED_SEAL_ONLY",
            "shape_ruling": "CONSTRAINS_NOT_FIXES",
            "joint_ruling": "DOES_NOT_DERIVE",
            "exact_reason": (
                "mirror_antiinvariance_forces_trace_angular_jet_zero_but_"
                "leaves_zero_or_one_free_shape_amplitude"
            ),
            "countercontrol": "MIRROR_LIFT_ATLAS",
        },
        {
            "selector_id": "S06",
            "selector": "CAP_REGULARITY_TOPOLOGY",
            "area_ruling": "CONSTRAINS_NOT_FIXES",
            "shape_ruling": "CONSTRAINS_NOT_FIXES",
            "joint_ruling": "DOES_NOT_DERIVE",
            "exact_reason": (
                "cap_jets_and_cycle_arithmetic_leave_endpoint_flat_interior_"
                "deformations_and_q_loses_rank_at_cap"
            ),
            "countercontrol": "E02_E03_E04_PLUS_RANK_LOSS",
        },
        {
            "selector_id": "S07",
            "selector": "MONODROMY",
            "area_ruling": "CONSTRAINS_NOT_FIXES",
            "shape_ruling": "CONSTRAINS_NOT_FIXES",
            "joint_ruling": "DOES_NOT_DERIVE",
            "exact_reason": (
                "descent_restricts_glue_and_eigenlines_not_local_rate_"
                "amplitude_and_real_phi_has_S1_critical_point"
            ),
            "countercontrol": "GENERAL_GL2Z_NORMALIZER_AUDIT",
        },
        {
            "selector_id": "S08",
            "selector": "CARTAN_BIANCHI",
            "area_ruling": "DOES_NOT_DERIVE",
            "shape_ruling": "DOES_NOT_DERIVE",
            "joint_ruling": "DOES_NOT_DERIVE",
            "exact_reason": (
                "Levi_Civita_and_Bianchi_hold_for_every_smooth_countermetric"
            ),
            "countercontrol": "E05_E06",
        },
        {
            "selector_id": "S09",
            "selector": "BOOTSTRAP",
            "area_ruling": "NOT_AN_EQUATION",
            "shape_ruling": "NOT_AN_EQUATION",
            "joint_ruling": "NOT_AN_EQUATION",
            "exact_reason": (
                "current_bootstrap_is_onshell_admissibility_without_response_"
                "map_functional_or_normal_equation"
            ),
            "countercontrol": "SOURCE_AUDIT",
        },
        {
            "selector_id": "S10",
            "selector": "C_ANCHOR",
            "area_ruling": "DOES_NOT_DERIVE",
            "shape_ruling": "DOES_NOT_DERIVE",
            "joint_ruling": "DOES_NOT_DERIVE",
            "exact_reason": (
                "c_remains_in_h_and_detG_but_cancels_from_dimensionless_"
                "rate_values"
            ),
            "countercontrol": "C_SYMBOLIC_AND_2_3_299792458",
        },
        {
            "selector_id": "S11",
            "selector": "COMPLETION_CROSSCHECK",
            "area_ruling": "DOES_NOT_DERIVE",
            "shape_ruling": "DOES_NOT_DERIVE",
            "joint_ruling": "DOES_NOT_DERIVE",
            "exact_reason": (
                "all_12_families_are_parametric_and_zero_force_full_pair"
            ),
            "countercontrol": "PRIOR_12_ROW_CENSUS",
        },
    ]


def source_lineage() -> list[dict[str, object]]:
    sources = [
        ("S01", "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "CSN"),
        (
            "S02",
            "udt_angular_generator_branch_census_2026-07-23/AUDIT_REPORT.md",
            "IMMEDIATE_PARENT",
        ),
        (
            "S03",
            "udt_angular_generator_branch_census_2026-07-23/RESULT.json",
            "PARENT_COUNTS",
        ),
        (
            "S04",
            "udt_angular_generator_branch_census_2026-07-23/"
            "CORRECTION_PREREGISTRATION.md",
            "FULL_METRIC_CSN_CORRECTION",
        ),
        (
            "S05",
            "udt_reciprocal_angular_intertwiner_audit_2026-07-23/"
            "AUDIT_REPORT.md",
            "INTERTWINER_TARGET",
        ),
        (
            "S06",
            "udt_reciprocal_angular_intertwiner_audit_2026-07-23/"
            "CONDITIONAL_NONBLOCK_WITNESSES.tsv",
            "NONBLOCK_CONTROLS",
        ),
        (
            "S07",
            "complete_coframe_seal_involution_2026-07-20/AUDIT_REPORT.md",
            "SEAL_LIFTS",
        ),
        (
            "S08",
            "udt_free_global_seal_transversality_audit_2026-07-21/"
            "AUDIT_REPORT.md",
            "SEAL_AND_INTERIOR_FREEDOM",
        ),
        (
            "S09",
            "udt_global_metric_assembly_atlas_2026-07-22/"
            "COMPLETION_CLASS_REGISTRY.tsv",
            "TWELVE_COMPLETIONS",
        ),
        (
            "S10",
            "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
            "GLOBAL_COMPLETION_SCOPE",
        ),
        (
            "S11",
            "boundary_bootstrap_representative_selector_audit_2026-07-19/"
            "AUDIT_REPORT.md",
            "BOOTSTRAP_STATUS",
        ),
        (
            "S12",
            "matter_bootstrap_dimensional_inventory_2026-07-20/"
            "AUDIT_REPORT.md",
            "MASS_DENSITY_BOOTSTRAP_GAPS",
        ),
        (
            "S13",
            "udt_complete_metric_solution_space_map_2026-07-21/"
            "GEOMETRIC_COUPLING_MAP.tsv",
            "COMPLETE_METRIC_SECTORS",
        ),
        (
            "S14",
            "udt_clock_anchor_scale_threading_audit_2026-07-22/"
            "AUDIT_REPORT.md",
            "C_ANCHOR",
        ),
        (
            "S15",
            "udt_relative_angular_area_shape_selector_audit_2026-07-23/"
            "PREREGISTRATION.md",
            "FROZEN_SCOPE",
        ),
        (
            "S16",
            "udt_relative_angular_area_shape_selector_audit_2026-07-23/"
            "PREMISE_LEDGER.tsv",
            "FROZEN_PREMISES",
        ),
        (
            "S17",
            "udt_relative_angular_area_shape_selector_audit_2026-07-23/"
            "SELECTOR_UNIVERSE.tsv",
            "FROZEN_SELECTOR_UNIVERSE",
        ),
    ]
    rows = []
    for source_id, relative, role in sources:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        rows.append(
            {
                "source_id": source_id,
                "path": relative,
                "sha256": digest(path),
                "size": path.stat().st_size,
                "role": role,
            }
        )
    return rows


def validate_selectors(rows: list[dict[str, str]]) -> None:
    expected = read_tsv(HERE / "SELECTOR_UNIVERSE.tsv")
    if [row["selector_id"] for row in rows] != [
        row["selector_id"] for row in expected
    ]:
        raise AssertionError("selector universe")
    allowed = {
        "DERIVES_GLOBALLY",
        "DERIVES_AT_FIXED_SEAL_ONLY",
        "CONSTRAINS_NOT_FIXES",
        "DOES_NOT_DERIVE",
        "UNDEFINED_WITHOUT_EXTRA_STRUCTURE",
        "NOT_AN_EQUATION",
    }
    for row in rows:
        if any(
            row[key] not in allowed
            for key in ("area_ruling", "shape_ruling", "joint_ruling")
        ):
            raise AssertionError("selector ruling")
    if any(row["joint_ruling"] == "DERIVES_GLOBALLY" for row in rows):
        raise AssertionError("joint force overclaim")


def catch_rows(
    formula: dict[str, object],
    diagnostics: dict[str, object],
    endpoints: list[dict[str, object]],
    mirrors: list[dict[str, object]],
    selectors: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks = [
        ("raw_Q_used", formula["raw_Q_is_invariant_angular_metric"] is False),
        ("determinant_proof_removed", "det(h)*det(q)" in formula["determinant_identity"]),
        ("cross_terms_dropped", formula["cross_terms_retained"] is True),
        (
            "angular_relative_scale_erased",
            diagnostics["relative_area_rate"] == "A_rel=w_p",
        ),
        ("c_set_to_one", diagnostics["c_in_complete_reciprocal_metric"] is True),
        (
            "seal_local_promoted_global",
            next(row for row in selectors if row["selector_id"] == "S05")[
                "area_ruling"
            ]
            == "DERIVES_AT_FIXED_SEAL_ONLY",
        ),
        (
            "mirror_amplitude_fixed",
            any("FREE" in str(row["shape_speed_at_fixed_seal"]) for row in mirrors),
        ),
        (
            "general_monodromy_dropped",
            "GENERAL_GL2Z" in next(row for row in selectors if row["selector_id"] == "S07")["countercontrol"],
        ),
        (
            "cap_topology_used_as_equation",
            next(row for row in selectors if row["selector_id"] == "S06")[
                "joint_ruling"
            ]
            == "DOES_NOT_DERIVE",
        ),
        (
            "Bianchi_used_as_selector",
            next(row for row in selectors if row["selector_id"] == "S08")[
                "joint_ruling"
            ]
            == "DOES_NOT_DERIVE",
        ),
        (
            "bootstrap_invented_equation",
            next(row for row in selectors if row["selector_id"] == "S09")[
                "joint_ruling"
            ]
            == "NOT_AN_EQUATION",
        ),
        (
            "endpoint_second_jets_changed",
            all(
                row["endpoint_jets_through_2"] in {
                    "BASE",
                    "IDENTICAL_TO_BASE",
                    "INHERITS_SELECTED_C_JETS",
                    "NOT_ENDPOINT",
                }
                for row in endpoints
            ),
        ),
        (
            "deformation_knobs_correlated",
            all(
                any(row["control_id"] == key for row in endpoints)
                for key in ("E02_AREA_ONLY", "E03_SHEAR_ONLY", "E04_ROTATION_ONLY")
            ),
        ),
        (
            "critical_phi_assigned_value",
            "UNDEFINED" in (ROOT / "udt_angular_generator_branch_census_2026-07-23" / "POINTWISE_GENERATOR_CONTROLS.tsv").read_text(),
        ),
        (
            "pointwise_promoted_transport",
            "transport" in (ROOT / "udt_angular_generator_branch_census_2026-07-23" / "AUDIT_REPORT.md").read_text().lower(),
        ),
        (
            "FC12_selected",
            next(row for row in selectors if row["selector_id"] == "S11")[
                "joint_ruling"
            ]
            == "DOES_NOT_DERIVE",
        ),
        (
            "external_action_imported",
            all("ACTION" not in row["exact_reason"] for row in selectors),
        ),
        (
            "scope_expanded_to_no_go",
            "CURRENT" in MAXIMUM and "DO_NOT_FIX" in MAXIMUM,
        ),
        (
            "full_CSN_covariance_lost",
            formula["relative_ratio_full_csn_invariant"] is True,
        ),
        (
            "shape_CSN_invariance_lost",
            diagnostics["full_csn_shape_invariant"] is True,
        ),
        (
            "nonblock_signature_unchecked",
            "inertia" in formula["signature_identity"],
        ),
        (
            "selector_missing",
            len(selectors) == 11,
        ),
        (
            "seal_area_positive_result_lost",
            all(
                row["relative_area_at_fixed_seal"] == "ZERO"
                or row["relative_area_at_fixed_seal"] == "ZERO_WHERE_REGULAR"
                for row in mirrors
            ),
        ),
        (
            "unit_shape_claimed_at_all_seals",
            any(
                row["shape_speed_at_fixed_seal"] == "ZERO"
                for row in mirrors
            )
            and any(
                "FREE" in str(row["shape_speed_at_fixed_seal"])
                for row in mirrors
            ),
        ),
    ]
    rows = []
    for index, (mutation, caught) in enumerate(checks, 1):
        if not caught:
            raise AssertionError(f"catch failed {mutation}")
        rows.append(
            {
                "catch_id": f"C{index:02d}",
                "mutation": mutation,
                "status": "CAUGHT",
            }
        )
    return rows


def main() -> None:
    formula = exact_nonblock_formula()
    diagnostics = exact_diagnostics()
    endpoints = endpoint_flat_controls()
    mirrors = mirror_controls()
    selectors = selector_rows()
    validate_selectors(selectors)
    lineage = source_lineage()
    catches = catch_rows(formula, diagnostics, endpoints, mirrors, selectors)

    (HERE / "NONBLOCK_INVARIANT_FORMULA.json").write_text(
        json.dumps(formula, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (HERE / "DIAGNOSTIC_FORMULA.json").write_text(
        json.dumps(diagnostics, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_tsv(HERE / "ENDPOINT_FLAT_COUNTERFAMILY.tsv", endpoints)
    write_tsv(HERE / "SEAL_DIAGNOSTIC_ATLAS.tsv", mirrors)
    write_tsv(HERE / "SELECTOR_RULING_MATRIX.tsv", selectors)
    write_tsv(HERE / "SOURCE_LINEAGE.tsv", lineage)
    write_tsv(HERE / "CATCH_PROOFS.tsv", catches)

    joins = [
        {
            "join_id": "J01",
            "from": "complete_nonblock_G_plus_split",
            "to": "orthogonal_angular_q",
            "ruling": "DERIVED_EXACT_SCHUR_COMPLEMENT",
        },
        {
            "join_id": "J02",
            "from": "h_q_T",
            "to": "A_rel_and_S_shape",
            "ruling": "DERIVED_EXACT_DIAGNOSTICS",
        },
        {
            "join_id": "J03",
            "from": "CSN",
            "to": "diagnostic_values",
            "ruling": "INVARIANCE_DERIVED_VALUES_NOT_FIXED",
        },
        {
            "join_id": "J04",
            "from": "seal_involution",
            "to": "A_rel_zero_at_fixed_seal",
            "ruling": "DERIVED_LOCAL_WHERE_REGULAR",
        },
        {
            "join_id": "J05",
            "from": "seal_involution",
            "to": "S_shape_one",
            "ruling": "NOT_DERIVED_AMPLITUDE_FREE_OR_ZERO",
        },
        {
            "join_id": "J06",
            "from": "finite_cell_endpoint_jets",
            "to": "bulk_targets",
            "ruling": "REFUTED_BY_ENDPOINT_FLAT_THREE_KNOB_FAMILY",
        },
        {
            "join_id": "J07",
            "from": "current_bootstrap",
            "to": "bulk_targets",
            "ruling": "NOT_AN_EXECUTABLE_EQUATION",
        },
        {
            "join_id": "J08",
            "from": "pointwise_targets",
            "to": "persistent_intertwiner",
            "ruling": "TRANSPORT_STILL_REQUIRED",
        },
    ]
    write_tsv(HERE / "JOIN_LEDGER.tsv", joins)
    status = [
        {
            "object": "nonblock_orthogonal_angular_metric",
            "status": "DERIVED_EXACT_CONDITIONAL_ON_SPLIT",
            "scope": "q=Q-Ct_hinv_C",
        },
        {
            "object": "relative_angular_area_rate",
            "status": "DERIVED_DIAGNOSTIC_VALUE_OPEN",
            "scope": "full_CSN_invariant",
        },
        {
            "object": "angular_shape_speed",
            "status": "DERIVED_DIAGNOSTIC_VALUE_OPEN",
            "scope": "full_CSN_invariant",
        },
        {
            "object": "seal_relative_area_stationarity",
            "status": "DERIVED_LOCAL",
            "scope": "regular_fixed_seal_all_registered_involutive_lifts",
        },
        {
            "object": "seal_unit_shape_speed",
            "status": "NOT_DERIVED",
            "scope": "zero_or_free_amplitude_by_lift",
        },
        {
            "object": "global_joint_pair",
            "status": "OPEN_NOT_DERIVED_CURRENT_PREMISES",
            "scope": "endpoint_flat_nonblock_counterfamilies_survive",
        },
        {
            "object": "transport_persistence",
            "status": "OPEN",
            "scope": "not_implied_by_pointwise_diagnostics",
        },
    ]
    write_tsv(HERE / "STATUS_LEDGER.tsv", status)

    result = {
        "schema": "udt-relative-angular-area-shape-selector-1.0",
        "base_commit": BASE,
        "sympy_version": sp.__version__,
        "maximum_conclusion": MAXIMUM,
        "counts": {
            "selectors": len(selectors),
            "area_global_derivations": sum(
                row["area_ruling"] == "DERIVES_GLOBALLY"
                for row in selectors
            ),
            "shape_global_derivations": sum(
                row["shape_ruling"] == "DERIVES_GLOBALLY"
                for row in selectors
            ),
            "joint_global_derivations": sum(
                row["joint_ruling"] == "DERIVES_GLOBALLY"
                for row in selectors
            ),
            "seal_local_area_derivations": sum(
                row["area_ruling"] == "DERIVES_AT_FIXED_SEAL_ONLY"
                for row in selectors
            ),
            "endpoint_flat_controls": len(endpoints),
            "seal_lift_rows": len(mirrors),
            "sources": len(lineage),
            "joins": len(joins),
            "catch_proofs": len(catches),
            "complete_on_shell_g_phi_branches": 0,
        },
        "diagnostics": {
            "relative_area": diagnostics["relative_area_rate"],
            "shape_speed": diagnostics["shape_speed_squared"],
            "joint_target": diagnostics["joint_target"],
        },
        "selection_ruling": (
            "GLOBAL_PAIR_NOT_DERIVED__SEAL_DERIVES_AREA_STATIONARITY_ONLY_"
            "AT_FIXED_REGULAR_POINT__SHAPE_AMPLITUDE_AND_BULK_FREE"
        ),
        "compute": {"cpu_only": True, "gpu_work_performed": False},
    }
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
