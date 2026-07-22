#!/usr/bin/env python3
"""Build the preregistered complete-connector assembly audit.

This generator is deliberately stdlib-only.  It treats the retained registries as
evidence rows, not as a finite list of solved universes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "5457a36f96e46424032899dcb1a1a0874f273c58"


SOURCES = [
    ("SRC01", "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv", "completion_id", "GLOBAL_COMPLETION_FAMILY"),
    ("SRC02", "udt_global_metric_assembly_atlas_2026-07-22/MOTIF_COMPLETION_ATLAS.tsv", "motif,completion_id", "MOTIF_COMPLETION_CROSS_ROW"),
    ("SRC03", "udt_global_metric_assembly_atlas_2026-07-22/BUNDLE_HOLONOMY_ATLAS.tsv", "completion_id", "COMPLETION_SUMMARY_OR_HOLONOMY_WITNESS"),
    ("SRC04", "udt_global_metric_assembly_atlas_2026-07-22/SELECTOR_MATRIX.tsv", "selector_id,completion_id", "SELECTOR_COMPLETION_CROSS_ROW"),
    ("SRC05", "udt_global_kinematic_assembly_p03g_2026-07-21/ASSEMBLY_INPUT_REGISTRY.tsv", "id", "ASSEMBLY_INPUT"),
    ("SRC06", "udt_global_kinematic_assembly_p03g_2026-07-21/COVER_AND_COCYCLE_BRANCHES.tsv", "id", "COCYCLE_BRANCH"),
    ("SRC07", "udt_global_kinematic_assembly_p03g_2026-07-21/GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv", "axis_id", "ASSEMBLY_AXIS"),
    ("SRC08", "udt_global_kinematic_assembly_p03g_2026-07-21/GLOBAL_COUNTERMODEL_LEDGER.tsv", "id", "SELECTOR_COUNTERMODEL"),
    ("SRC09", "udt_global_kinematic_assembly_p03g_2026-07-21/LOCAL_TO_GLOBAL_EXTENSION_GATES.tsv", "id", "LOCAL_BRANCH_EXTENSION_GATE"),
    ("SRC10", "udt_global_kinematic_assembly_p03g_2026-07-21/SEAL_LIFT_AND_TANGENT_BRANCHES.tsv", "id", "SEAL_LIFT_OR_BOUNDARY_WITNESS"),
    ("SRC11", "udt_global_kinematic_assembly_p03g_2026-07-21/TOPOLOGY_AND_COMPLETION_BRANCHES.tsv", "id", "TOPOLOGY_WITNESS_OR_REMAINDER"),
    ("SRC12", "udt_global_kinematic_assembly_p03g_2026-07-21/UNCOUNTED_GLOBAL_MODULI.tsv", "id", "OPEN_GLOBAL_MODULUS"),
    ("SRC13", "udt_global_coframe_cocycle_audit_2026-07-20/COCYCLE_CLASSIFICATION.tsv", "id", "COCYCLE_RESULT"),
    ("SRC14", "udt_global_coframe_cocycle_audit_2026-07-20/GLOBAL_WITNESSES.tsv", "witness_id", "LOCAL_OR_CONDITIONAL_WITNESS"),
    ("SRC15", "udt_global_coframe_cocycle_audit_2026-07-20/TANGENT_CLASSIFICATION.tsv", "class_id", "TANGENT_CLASS"),
    ("SRC16", "udt_complete_lift_mu_closure_audit_2026-07-20/GLOBAL_SELECTOR_TYPE.tsv", "candidate", "SELECTOR_CANDIDATE"),
    ("SRC17", "udt_complete_lift_mu_closure_audit_2026-07-20/LIFT_CLASSIFICATION.tsv", "lift", "LIFT_CLASS"),
    ("SRC18", "udt_complete_lift_mu_closure_audit_2026-07-20/WITNESS_CENSUS.tsv", "id", "EXACT_LOCAL_METRIC_WITNESS"),
    ("SRC19", "udt_complete_seal_fixed_set_selector_audit_2026-07-21/COMPLETE_LIFT_CLASSIFICATION.tsv", "lift", "COMPLETE_LOCAL_LIFT_CLASS"),
    ("SRC20", "udt_complete_seal_fixed_set_selector_audit_2026-07-21/COMPLETENESS_SCOPE.tsv", "criterion", "SCOPE_RECORD"),
    ("SRC21", "udt_complete_seal_fixed_set_selector_audit_2026-07-21/FIRST_JET_PARITY.tsv", "lift", "FIRST_JET_CLASS"),
    ("SRC22", "udt_complete_seal_fixed_set_selector_audit_2026-07-21/INTERPRETATION_SELECTOR.tsv", "interpretation_id", "INTERPRETATION_SELECTOR"),
    ("SRC23", "udt_complete_seal_fixed_set_selector_audit_2026-07-21/NONZERO_CROSS_WITNESSES.tsv", "witness_id", "EXACT_LOCAL_METRIC_WITNESS"),
]

SUPPORTING_SOURCES = [
    ("SUP01", "udt_motif_hopf_correspondence_audit_2026-07-22/TORIC_CONTROL_RESULT.json", "LOAD_BEARING_TORIC_METRIC_CONTROL"),
    ("SUP02", "udt_two_frame_regime_metric_limit_audit_2026-07-22/DERIVATION_RESULT.json", "LOAD_BEARING_STATIONARY_CONNECTOR_IDENTITY"),
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def connector_checks() -> dict[str, bool]:
    checks: dict[str, bool] = {}
    samples = [
        (Q(5, 2), Q(7, 3), Q(1, 5), Q(11, 4)),
        (Q(9, 4), Q(2, 3), Q(-2, 7), Q(5)),
        (Q(13, 6), Q(4, 5), Q(0), Q(17, 3)),
    ]
    for i, (n, h, b, c) in enumerate(samples):
        gtt = c * c * (-n * n + h * h * b * b)
        gtl = c * h * h * b
        gll = h * h
        checks[f"determinant_{i}"] = gtt * gll - gtl * gtl == -c * c * n * n * h * h
        for sign in (-1, 1):
            v = c * (-b + sign * n / h)
            checks[f"null_root_{i}_{sign}"] = gtt + 2 * gtl * v + gll * v * v == 0
            checks[f"orthonormal_rate_{i}_{sign}"] = h * (v / c + b) / n == sign

    # Reciprocal control and the three exact lapse counterfamilies.
    for i, d in enumerate([Q(2), Q(7, 3), Q(11, 2)]):
        h = 1 / d
        f_two = Q(1)
        n_two = f_two * d
        f_cancel = 1 / d
        n_cancel = f_cancel * d
        f_reverse = 1 / (d * d)
        n_reverse = f_reverse * d
        checks[f"two_ended_{i}"] = n_two == d and n_two / h == d * d
        checks[f"cancelled_{i}"] = n_cancel == 1 and n_cancel / h == d
        checks[f"reversed_{i}"] = n_reverse == 1 / d and n_reverse / h == 1
        checks[f"proper_two_ended_order_{i}"] = d > 1 and 1 / d < 1

    # Uniform lapse cancels every positive spatial/angular line weight.
    h1, h2, l1, l2, n = Q(2), Q(5), Q(3), Q(7), Q(5)
    length = h1 * l1 + h2 * l2
    time = h1 * l1 / n + h2 * l2 / n
    checks["uniform_lapse_path_cancel"] = length / time == n

    # Nonuniform lapse makes the angular/spatial weights load-bearing.
    n1, n2 = Q(2), Q(9)
    rate_a = length / (h1 * l1 / n1 + h2 * l2 / n2)
    rate_b = (Q(4) * l1 + h2 * l2) / (Q(4) * l1 / n1 + h2 * l2 / n2)
    checks["nonuniform_path_weight"] = rate_a != rate_b

    # A finite ordinary segment bottlenecks two high-rate endpoint segments.
    d = Q(10**6)
    checks["endpoint_only_insufficient"] = Q(3) / (Q(2) / d + 1) < 3
    checks["uniform_high_rate_connector"] = Q(2) / (1 / d + 1 / d) == d

    # Near-null shift cancels one large-D one-way rate and the round trip.
    d = Q(10**6)
    n = d
    hb = n - 1
    forward, backward = n - hb, n + hb
    roundtrip = Q(2) / (1 / forward + 1 / backward)
    checks["near_null_forward_finite"] = forward == 1
    checks["near_null_other_direction_large"] = backward > d
    checks["near_null_roundtrip_bounded"] = roundtrip < 2
    checks["near_null_thread_timelike"] = abs(hb) < n

    # Oscillatory positive lapse has no asymptotic limit along two subsequences.
    vals_a = [2 + math.sin(2 * math.pi * k) for k in range(1, 6)]
    vals_b = [2 + math.sin(math.pi / 2 + 2 * math.pi * k) for k in range(1, 6)]
    checks["oscillatory_positive"] = min(vals_a + vals_b) > 0
    checks["oscillatory_distinct_subsequences"] = abs(vals_a[-1] - vals_b[-1]) > 0.9
    return checks


def main() -> None:
    source_rows: list[dict[str, object]] = []
    candidate_rows: list[dict[str, object]] = []
    expected_total = 0

    for source_id, rel, key_spec, role in SOURCES:
        path = ROOT / rel
        rows = read_tsv(path)
        base_bytes = subprocess.check_output(["git", "show", f"{BASE}:{rel}"], cwd=ROOT)
        base_blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{rel}"], cwd=ROOT, text=True).strip()
        if path.read_bytes() != base_bytes:
            raise RuntimeError(f"source changed from preregistered base: {rel}")
        expected_total += len(rows)
        key_fields = key_spec.split(",")
        keys: list[str] = []
        for index, row in enumerate(rows, start=1):
            key = "::".join(row[field] for field in key_fields)
            keys.append(key)
            identity_relation = "INDEPENDENT_EVIDENCE_AXIS_NOT_COMPLETE_UNIVERSE"
            if source_id == "SRC01":
                identity_relation = "CANONICAL_COMPLETION_FAMILY_AXIS"
            elif source_id == "SRC02":
                identity_relation = "CROSS_PRODUCT_PRESENTATION_NOT_SOLVED_UNIVERSE"
            elif source_id == "SRC03" and index <= 12:
                identity_relation = "OVERLAP_SUMMARY_OF_SRC01_COMPLETION"
            elif source_id == "SRC04":
                identity_relation = "SELECTOR_APPLICATION_NOT_PHYSICAL_BRANCH"
            elif "WITNESS" in role:
                identity_relation = "BOUNDED_OR_LOCAL_WITNESS_NOT_GLOBAL_UNIVERSE"
            connector_relevance = "NO_COMPLETE_GLOBAL_CONNECTOR"
            if source_id == "SRC02" and row["motif"] == "RECIPROCAL_TORIC_CONTROL":
                connector_relevance = "CONDITIONAL_COMPLETE_METRIC_FORM__GLOBAL_PREMISES_OPEN"
            candidate_rows.append({
                "candidate_row_id": f"{source_id}:{index:04d}",
                "source_id": source_id,
                "source_path": rel,
                "source_key": key,
                "record_role": role,
                "identity_relation": identity_relation,
                "connector_relevance": connector_relevance,
            })
        if len(keys) != len(set(keys)):
            raise RuntimeError(f"duplicate source key in {rel}")
        source_rows.append({
            "source_id": source_id,
            "path": rel,
            "source_kind": "CANDIDATE_REGISTRY",
            "row_count": len(rows),
            "git_blob": base_blob,
            "sha256": hashlib.sha256(base_bytes).hexdigest(),
            "key_fields": key_spec,
            "record_role": role,
        })

    for source_id, rel, role in SUPPORTING_SOURCES:
        path = ROOT / rel
        base_bytes = subprocess.check_output(["git", "show", f"{BASE}:{rel}"], cwd=ROOT)
        base_blob = subprocess.check_output(["git", "rev-parse", f"{BASE}:{rel}"], cwd=ROOT, text=True).strip()
        if path.read_bytes() != base_bytes:
            raise RuntimeError(f"supporting source changed from preregistered base: {rel}")
        source_rows.append({
            "source_id": source_id,
            "path": rel,
            "source_kind": "LOAD_BEARING_SUPPORT",
            "row_count": 0,
            "git_blob": base_blob,
            "sha256": hashlib.sha256(base_bytes).hexdigest(),
            "key_fields": "-",
            "record_role": role,
        })

    if expected_total != 380:
        raise RuntimeError(f"candidate total changed: {expected_total}")

    completions = read_tsv(ROOT / SOURCES[0][1])
    motifs = read_tsv(ROOT / SOURCES[1][1])
    selectors = read_tsv(ROOT / SOURCES[3][1])
    completion_by_id = {row["completion_id"]: row for row in completions}
    completion_ids = list(completion_by_id)
    if len(completion_ids) != 12:
        raise RuntimeError("completion count")
    motif_names = sorted({row["motif"] for row in motifs})
    if len(motif_names) != 7 or len(motifs) != 84:
        raise RuntimeError("motif cross-product count")
    if {(m, c) for m in motif_names for c in completion_ids} != {
        (row["motif"], row["completion_id"]) for row in motifs
    }:
        raise RuntimeError("motif cross-product incomplete")

    control_compatibility = {
        "FC01_BOUNDARY_BOUNDARY": "CONDITIONAL_COMPATIBILITY__BOUNDARY_DATA_REQUIRED",
        "FC02_ONE_CAP_BOUNDARY": "CONDITIONAL_COMPATIBILITY__PRIMITIVE_CAP_JETS_REQUIRED",
        "FC03_TWO_CAP_P0": "CONDITIONAL_COMPATIBILITY__SAME_CYCLE_CAP_PROFILES_REQUIRED",
        "FC04_TWO_CAP_P1": "CONDITIONAL_COMPATIBILITY__OPPOSITE_PRIMITIVE_CAPS_REQUIRED",
        "FC05_TWO_CAP_P_GT1": "CONDITIONAL_COMPATIBILITY__LENS_CAP_PROFILES_REQUIRED",
        "FC06_NONPRIMITIVE_CAP": "CONDITIONAL_SINGULAR_REALIZATION__NONPRIMITIVE_CAP",
        "FC07_PERIODIC_TORUS_BUNDLE": "RESTRICTED_METRIC_PRESERVING_MONODROMY_SUBSET_ONLY",
        "FC08_MIRROR_DOUBLE": "OPEN_LIFT_PARITY_PROFILE_CHECK_REQUIRED",
        "FC09_NONORIENTABLE_GLUE": "OPEN_ORIENTATION_REVERSING_GLUE_CHECK_REQUIRED",
        "FC10_STRATIFIED_PROJECTOR": "OPEN_STRATIFICATION_AND_PROFILE_CHECK_REQUIRED",
        "FC11_NONINTEGRABLE_DISTRIBUTION": "INCOMPATIBLE_AS_SAME_NONINTEGRABLE_TORIC_DISTRIBUTION",
        "FC12_RECIPROCAL_TORIC_DIAGONAL": "CONDITIONAL_COMPATIBILITY__OWN_PROFILE_ENDPOINT_DATA_REQUIRED",
    }
    control_compatibility_class = {
        **{cid: "CONDITIONAL" for cid in [
            "FC01_BOUNDARY_BOUNDARY", "FC02_ONE_CAP_BOUNDARY", "FC03_TWO_CAP_P0",
            "FC04_TWO_CAP_P1", "FC05_TWO_CAP_P_GT1", "FC12_RECIPROCAL_TORIC_DIAGONAL",
        ]},
        "FC06_NONPRIMITIVE_CAP": "CONDITIONAL_SINGULAR",
        "FC07_PERIODIC_TORUS_BUNDLE": "RESTRICTED_SUBSET",
        "FC08_MIRROR_DOUBLE": "OPEN_CHECK_REQUIRED",
        "FC09_NONORIENTABLE_GLUE": "OPEN_CHECK_REQUIRED",
        "FC10_STRATIFIED_PROJECTOR": "OPEN_CHECK_REQUIRED",
        "FC11_NONINTEGRABLE_DISTRIBUTION": "INCOMPATIBLE_AS_SAME_DISTRIBUTION",
    }
    branch_rows: list[dict[str, object]] = []
    for row in motifs:
        motif = row["motif"]
        cid = row["completion_id"]
        completion = completion_by_id[cid]
        if motif == "RECIPROCAL_TORIC_CONTROL":
            sufficiency = "CONNECTOR_CONDITIONAL"
            control_identity = "TC01_RECIPROCAL_TORIC_STATIC_METRIC"
            metric = "g=-c_E^2dt^2+A(phi)^2dphi^2+Omega(phi)^2[e^-2phi_dxi1^2+e^2phi_dxi2^2]"
            threading = "N=1_IN_DECLARED_REPRESENTATIVE"
            shift = "B=0"
            spatial = "H_FROM_A_OR_OMEGA_EXP_WEIGHTS__PATH_NOT_SELECTED"
            regime = "SIGNED_PHI_PRESENT__GLOBAL_RANGE_AND_ANCHOR_CONDITIONAL"
            access = "FINITE_OR_CANCELLED"
            local_access = "FINITE_OR_CANCELLED"
            global_compatibility = control_compatibility[cid]
            compatibility_class = control_compatibility_class[cid]
            global_connector_status = "NOT_SUPPLIED__LOCAL_CONTROL_PRESENTATION_ONLY"
            if cid == "FC06_NONPRIMITIVE_CAP":
                completion_status = "GLOBAL_ORBIFOLD_OR_SINGULAR_COMPLETION"
                guard = "DO_NOT_CONFLATE_GLOBAL_ORBIFOLD_OR_SINGULAR_STATUS_WITH_FINITE_INTERIOR_OPTICAL_RATE"
            elif cid == "FC11_NONINTEGRABLE_DISTRIBUTION":
                completion_status = "NOT_REALIZED_AS_SAME_TORIC_DISTRIBUTION"
                guard = "COMMUTING_TORIC_COORDINATE_PLANES_CONFLICT_WITH_REGISTERED_NONINTEGRABLE_ORBIT_DISTRIBUTION"
            else:
                completion_status = "OPEN_NOT_CONSTRUCTED"
                guard = "INTERIOR_RATE_ONLY__GLOBAL_COMPATIBILITY_AND_COMPLETION_UNPROVED"
        else:
            sufficiency = "DISTRIBUTION_ONLY"
            control_identity = "-"
            metric = "LOCAL_REGISTERED_CHART_MOTIF__NO_COMPLETE_GLOBAL_METRIC_WITNESS"
            threading = "NOT_SUPPLIED"
            shift = "NOT_SUPPLIED"
            spatial = "PROJECTOR_OR_DISTRIBUTION_DATA_ONLY__CONNECTOR_PATH_NOT_SUPPLIED"
            regime = "NO_GLOBAL_PHI_PROFILE_OR_EXTREME_INCIDENCE"
            access = "UNDEFINED_MISSING_CONNECTOR_DATA"
            local_access = "UNDEFINED_MISSING_CONNECTOR_DATA"
            global_compatibility = "NOT_EVALUABLE_NO_COMPLETE_METRIC_CONTROL"
            compatibility_class = "NOT_EVALUABLE"
            global_connector_status = "NOT_SUPPLIED"
            completion_status = "NOT_EVALUABLE_FROM_PRESENTATION"
            guard = "DO_NOT_PROMOTE_COMPATIBILITY_ROW_TO_SOLVED_UNIVERSE"
        branch_rows.append({
            "assembly_id": f"{motif}::{cid}",
            "motif": motif,
            "completion_id": cid,
            "data_sufficiency": sufficiency,
            "metric_control_identity": control_identity,
            "lorentzian_metric": metric,
            "time_threading": threading,
            "shift": shift,
            "spatial_or_angular_connector": spatial,
            "regime_field_and_anchor": regime,
            "global_completion": completion["orbit_completion"],
            "global_compatibility": global_compatibility,
            "global_compatibility_class": compatibility_class,
            "global_connector_status": global_connector_status,
            "global_completion_status": completion_status,
            "accessibility_class": access,
            "interior_optical_class": local_access,
            "regularity_or_scope_guard": guard,
            "selection_status": row["global_selection"],
        })

    completion_summary: list[dict[str, object]] = []
    for cid in completion_ids:
        c = completion_by_id[cid]
        rows = [row for row in branch_rows if row["completion_id"] == cid]
        unresolved = sum(row["accessibility_class"] == "UNDEFINED_MISSING_CONNECTOR_DATA" for row in rows)
        presentations = sum(row["metric_control_identity"] == "TC01_RECIPROCAL_TORIC_STATIC_METRIC" for row in rows)
        control_row = next(row for row in rows if row["motif"] == "RECIPROCAL_TORIC_CONTROL")
        completion_summary.append({
            "completion_id": cid,
            "topology_family": c["topology_family"],
            "cross_rows": len(rows),
            "undefined_connector_rows": unresolved,
            "conditional_control_presentations": presentations,
            "unique_control_identity": "TC01_RECIPROCAL_TORIC_STATIC_METRIC_SHARED_ACROSS_12_PRESENTATIONS",
            "control_interior_accessibility": control_row["interior_optical_class"],
            "control_global_compatibility": control_row["global_compatibility"],
            "control_global_compatibility_class": control_row["global_compatibility_class"],
            "control_global_completion_status": control_row["global_completion_status"],
            "completion_level_ruling": "ACCESSIBILITY_NOT_SELECTED",
            "kinematic_example_scope": "LOCAL_STATIONARY_CONNECTOR_ONLY__GLOBAL_EXTENSION_UNPROVED",
            "selection_status": c["selection_status"],
        })

    counterfamilies = [
        {"id": "CF01", "N": "D", "H": "1/D", "HB": "0", "proper_or_anchor_rate": "D", "coordinate_rate": "D^2", "class": "FORCED_TWO_ENDED_WITHIN_THIS_EXTRA_THREADING", "scope": "F=1_DIAGONAL_CONTROL", "global_extension_status": "UNPROVED"},
        {"id": "CF02", "N": "1", "H": "1/D", "HB": "0", "proper_or_anchor_rate": "1", "coordinate_rate": "D", "class": "FINITE_OR_CANCELLED", "scope": "F=1/D__MATCHES_DECLARED_TORIC_TIME_LEG", "global_extension_status": "UNPROVED"},
        {"id": "CF03", "N": "1/D", "H": "1/D", "HB": "0", "proper_or_anchor_rate": "1/D", "coordinate_rate": "1", "class": "REVERSED", "scope": "F=1/D^2", "global_extension_status": "UNPROVED"},
        {"id": "CF04", "N": "2+sin(log(D))", "H": "1/D", "HB": "0", "proper_or_anchor_rate": "2+sin(log(D))", "coordinate_rate": "D[2+sin(log(D))]", "class": "OSCILLATORY_OR_NO_LIMIT", "scope": "POSITIVE_F=[2+sin(log(D))]/D", "global_extension_status": "UNPROVED"},
        {"id": "CF05", "N": "D", "H": "1/D", "HB": "D-1", "proper_or_anchor_rate": "forward=1;backward=2D-1", "coordinate_rate": "PATH_DEPENDENT", "class": "FINITE_OR_CANCELLED_ONE_WAY_AND_ROUNDTRIP_LARGE_D", "scope": "D>1_NEAR_NULL_SHIFT__TIMELIKE_THREAD", "global_extension_status": "UNPROVED"},
        {"id": "CF06", "N": "uniform_n", "H": "arbitrary_positive_path_weight", "HB": "0", "proper_or_anchor_rate": "n", "coordinate_rate": "PATH_CHART_DEPENDENT", "class": "ANGULAR_WEIGHT_CANCELS_FOR_UNIFORM_LAPSE", "scope": "ANY_FIXED_SPATIAL_PATH", "global_extension_status": "UNPROVED"},
        {"id": "CF07", "N": "nonuniform_N(lambda)", "H": "angular_or_spatial_H(lambda)", "HB": "0", "proper_or_anchor_rate": "L/integral(H_dlambda/N)", "coordinate_rate": "PATH_CHART_DEPENDENT", "class": "ANGULAR_WEIGHT_LOAD_BEARING", "scope": "ANY_FIXED_SPATIAL_PATH", "global_extension_status": "UNPROVED"},
        {"id": "CF08", "N": "D,D,1_on_three_segments", "H": "1,1,1", "HB": "0", "proper_or_anchor_rate": "3/(2/D+1)->3", "coordinate_rate": "SAME_IN_UNIT_LINE_CHART", "class": "FINITE_OR_CANCELLED_BY_CONNECTOR_BOTTLENECK", "scope": "ENDPOINT_REGIMES_ALONE_INSUFFICIENT", "global_extension_status": "UNPROVED"},
    ]

    selector_axes = sorted({row["selector_id"] for row in selectors})
    if len(selector_axes) != 7 or len(selectors) != 84:
        raise RuntimeError("selector matrix count")
    selector_rows: list[dict[str, object]] = []
    selector_class = {
        "RECIPROCITY": ("CONSTRAINS_NOT_SELECTS", "Fixes reciprocal comparison/transition parity; no clock threading, cover, path, or global section"),
        "CSN": ("CONSTRAINS_NOT_SELECTS", "Removes common pre-material scale from normalized objects; does not choose representative lapse or connector"),
        "FINITE_CELL": ("CONSTRAINS_NOT_SELECTS", "Removes spatial infinity and requires completion; does not choose boundary/cap/path/threading"),
        "STATIC_SEAL": ("CONSTRAINS_NOT_SELECTS", "Constrains signed phi at the static seal; multiple lifts and polarizations survive"),
        "BOOTSTRAP": ("OPEN", "Current bootstrap is after-solution admissibility with no varied selector functional"),
        "SCALE_MATTER_INVENTORY": ("SILENT", "No native matter scale/source/action coefficient currently supplies connector data"),
        "DENSITY_BOOTSTRAP": ("OPEN", "Density fixed-point route lacks native mass, varied closure, and response map"),
    }
    for selector in selector_axes:
        rows = [row for row in selectors if row["selector_id"] == selector]
        if len(rows) != 12 or {row["completion_id"] for row in rows} != set(completion_ids):
            raise RuntimeError(f"selector coverage {selector}")
        classification, effect = selector_class[selector]
        selector_rows.append({
            "selector": selector,
            "completion_rows": 12,
            "audit_class": classification,
            "connector_effect": effect,
            "existing_selection_power": sorted({row["selection_power"] for row in rows})[0],
            "sources": ";".join(sorted({row["source"] for row in rows})),
        })

    bundle_rows = read_tsv(ROOT / SOURCES[2][1])
    lift_a = read_tsv(ROOT / SOURCES[16][1])
    lift_b = read_tsv(ROOT / SOURCES[18][1])
    lift_c = read_tsv(ROOT / SOURCES[20][1])
    witness_a = read_tsv(ROOT / SOURCES[17][1])
    witness_b = read_tsv(ROOT / SOURCES[22][1])
    if {row["completion_id"] for row in bundle_rows[:12]} != set(completion_ids):
        raise RuntimeError("completion overlap map")
    if not ({row["lift"] for row in lift_a} == {row["lift"] for row in lift_b} == {row["lift"] for row in lift_c}):
        raise RuntimeError("lift overlap map")
    if {row["id"] for row in witness_a} != {row["witness_id"] for row in witness_b}:
        raise RuntimeError("witness overlap map")
    overlap_rows = [
        {"equivalence_id": "EQ01", "logical_identity": "GLOBAL_COMPLETION_FAMILY_AXIS", "source_paths": f"{SOURCES[0][1]};{SOURCES[2][1]}[base_rows]", "unique_identity_count": 12, "presentation_count": 24, "exact_relation": "SAME_12_COMPLETION_IDS__SECOND_SOURCE_ADDS_HOLONOMY_COLUMNS", "physical_universe_ruling": "PARAMETRIC_FAMILY_AXIS_NOT_SOLVED_UNIVERSES"},
        {"equivalence_id": "EQ02", "logical_identity": "MOTIF_COMPLETION_CROSS_PRODUCT", "source_paths": SOURCES[1][1], "unique_identity_count": 84, "presentation_count": 84, "exact_relation": "SEVEN_MOTIF_PRESENTATIONS_CROSSED_WITH_TWELVE_COMPLETIONS", "physical_universe_ruling": "COMPATIBILITY_PRESENTATIONS_NOT_SOLVED_UNIVERSES"},
        {"equivalence_id": "EQ03", "logical_identity": "TC01_RECIPROCAL_TORIC_STATIC_METRIC", "source_paths": f"{SUPPORTING_SOURCES[0][1]};{SOURCES[1][1]}[RECIPROCAL_TORIC_CONTROL]", "unique_identity_count": 1, "presentation_count": 12, "exact_relation": "ONE_LOCAL_METRIC_FORM_REPEATED_ACROSS_TWELVE_COMPLETION_PRESENTATIONS", "physical_universe_ruling": "NO_COMPLETE_GLOBAL_CONNECTOR_REALIZATION_SUPPLIED"},
        {"equivalence_id": "EQ04", "logical_identity": "FOUR_REGISTERED_LOCAL_LIFT_CLASSES", "source_paths": f"{SOURCES[16][1]};{SOURCES[18][1]};{SOURCES[20][1]}", "unique_identity_count": 4, "presentation_count": 12, "exact_relation": "SAME_FOUR_LIFT_NAMES_WITH_DIFFERENT_CLASSIFICATION_COLUMNS", "physical_universe_ruling": "LOCAL_LIFT_CLASSES_NOT_GLOBAL_UNIVERSES"},
        {"equivalence_id": "EQ05", "logical_identity": "EIGHT_NONZERO_CROSS_LOCAL_WITNESSES", "source_paths": f"{SOURCES[17][1]};{SOURCES[22][1]}", "unique_identity_count": 8, "presentation_count": 16, "exact_relation": "SAME_EIGHT_WITNESS_IDS_WITH_METRIC_AND_SEAL_READOUTS", "physical_universe_ruling": "LOCAL_EXACT_WITNESSES_NOT_GLOBAL_UNIVERSES"},
        {"equivalence_id": "EQ06", "logical_identity": "SELECTOR_COMPLETION_APPLICATIONS", "source_paths": SOURCES[3][1], "unique_identity_count": 84, "presentation_count": 84, "exact_relation": "SEVEN_SELECTOR_AXES_APPLIED_TO_TWELVE_COMPLETIONS", "physical_universe_ruling": "SELECTOR_APPLICATIONS_NOT_BRANCHES"},
    ]

    checks = connector_checks()
    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise RuntimeError("connector algebra failed: " + ",".join(failed))

    write_tsv(HERE / "SOURCE_CENSUS.tsv", list(source_rows[0]), source_rows)
    write_tsv(HERE / "CANDIDATE_ROW_LEDGER.tsv", list(candidate_rows[0]), candidate_rows)
    write_tsv(HERE / "ASSEMBLED_BRANCH_ATLAS.tsv", list(branch_rows[0]), branch_rows)
    write_tsv(HERE / "COMPLETION_SUMMARY.tsv", list(completion_summary[0]), completion_summary)
    write_tsv(HERE / "COUNTERFAMILY_ATLAS.tsv", list(counterfamilies[0]), counterfamilies)
    write_tsv(HERE / "SELECTOR_EFFECT_ATLAS.tsv", list(selector_rows[0]), selector_rows)
    write_tsv(HERE / "IDENTITY_EQUIVALENCE_MAP.tsv", list(overlap_rows[0]), overlap_rows)

    control_rows = [row for row in branch_rows if row["metric_control_identity"] == "TC01_RECIPROCAL_TORIC_STATIC_METRIC"]
    compatibility_counts = {
        key: sum(row["global_compatibility_class"] == key for row in control_rows)
        for key in ["CONDITIONAL", "CONDITIONAL_SINGULAR", "RESTRICTED_SUBSET", "OPEN_CHECK_REQUIRED", "INCOMPATIBLE_AS_SAME_DISTRIBUTION"]
    }

    payload = {
        "base": BASE,
        "source_files": len(source_rows),
        "source_registries": len(SOURCES),
        "supporting_sources": len(SUPPORTING_SOURCES),
        "candidate_rows": len(candidate_rows),
        "completion_families": len(completions),
        "motif_completion_cross_rows": len(branch_rows),
        "conditional_control_presentations": len(control_rows),
        "unique_conditional_metric_controls": len({row["metric_control_identity"] for row in control_rows}),
        "undefined_connector_rows": sum(row["accessibility_class"] == "UNDEFINED_MISSING_CONNECTOR_DATA" for row in branch_rows),
        "finite_or_cancelled_control_presentations": sum(row["interior_optical_class"] == "FINITE_OR_CANCELLED" for row in branch_rows),
        "complete_global_connectors": sum(row["global_connector_status"] == "SUPPLIED" for row in branch_rows),
        "control_global_compatibility_counts": compatibility_counts,
        "overlap_equivalence_rows": len(overlap_rows),
        "selector_axes": len(selector_rows),
        "checks": checks,
        "check_count": len(checks),
        "formulas": {
            "stationary_connector": "ds^2=-c_E^2*N^2*dt^2+H^2*(dlambda+c_E*B*dt)^2",
            "null_roots": "dlambda/dt=c_E*(-B+/-N/H)",
            "local_orthonormal_rate": "H*(dlambda/dt/c_E+B)/N=+/-1",
            "one_way_optical_time": "T_+=[1/c_E]*integral[H*dlambda/(N-HB)]",
            "return_optical_time": "T_-=[1/c_E]*integral[H*dlambda/(N+HB)]",
            "path_effective_rate": "chi_+/c_E=L_proper/integral[H*dlambda/(N-HB)]",
            "reciprocal_control": "N=F*D;H=1/D;D=exp(-phi)",
            "toric_control": "N=1;B=0;H_path_from_A,Omega*exp(+/-phi);chi/c_E=1_for_any_fixed_path",
        },
        "maximum_conclusion": "NO_COMPLETE_GLOBAL_CONNECTOR_SELECTED__ONE_CONDITIONAL_TORIC_CONTROL_HAS_C_E_INTERIOR_FIXED_PATH_RATE__GLOBAL_COMPATIBILITY_AND_THREADING_OPEN",
        "information_transfer": "OPEN_NOT_TESTED",
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    (HERE / "DERIVATION_RESULT.json").write_text(rendered, encoding="utf-8")
    (HERE / "BUILD_STDOUT.txt").write_text(rendered, encoding="utf-8")
    (HERE / "BUILD_STDERR.txt").write_text("", encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
