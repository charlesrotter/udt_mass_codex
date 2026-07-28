#!/usr/bin/env python3
"""Build the fixed-source joint-selector adjudication records.

This script reads candidate bytes only through the preregistered fixed Git base.
The scientific classifications below are explicit review inputs, not regex-derived
physics judgments.  Assertions make the review fail closed if discovery changes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "bb70833d1e28cfcd7a62073860223f3b26e715ad"


def git(*args: str, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=False,
    )
    if result.returncode:
        error = result.stderr if not binary else result.stderr.decode("utf-8", "replace")
        raise RuntimeError(error)
    return result.stdout


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


# Each qualified group is explicitly assigned once.  Categories summarize the
# reviewed proposition type; they do not infer a ruling from a filename.
GROUP_CATEGORIES = {
    "CONTROL_NAVIGATION_OR_UNRELATED": {
        "ROOT::AGENTS.md", "ROOT::HANDOFF.md", "ROOT::INDEX.md", "ROOT::LIVE.md",
        "ROOT::MEMORY.md", "ROOT::NEGATIVES_REGISTRY.md",
        "ROOT::UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "research",
    },
    "HISTORICAL_OR_FIREWALLED": {
        "ROOT::negative_phi_native_geometry.md", "ROOT::particle_spectrum_native_geometry.md",
        "ROOT::r1_route_fork_native_derivation.md", "ROOT::udt_canonical_geometry.md",
        "archive", "archive/native_action_chat_2026-07-14_15",
        "archive/pre_2026-07-01", "legacy/root_oneoffs_2026-07-01",
        "rescued_workspaces/2026-06-11/tmp_loose_scripts",
    },
    "OUT_OF_SCOPE_PARTICLE_OR_ACTION": {
        "c2_failed_basin_homotopy_2026-07-20",
        "c2_open_path_checkpoint_continuation_2026-07-20",
        "c2_transverse_coframe_closure_2026-07-20",
        "reciprocity_offshell_constraint_selector_2026-07-18",
    },
    "PAIR_OR_DEPTH_PARTIAL": {
        "invariant_reciprocal_causal_flow_2026-07-18",
        "projective_position_direction_magnitude_correction_2026-07-19",
        "projective_position_join_audit_2026-07-19",
        "reciprocal_c_clock_channel_correction_2026-07-19",
        "reciprocal_clock_optical_scale_selector_2026-07-19",
        "udt_clock_anchor_scale_threading_audit_2026-07-22",
        "udt_foundational_semantic_regression_correction_2026-07-26",
        "udt_founded_pair_first_jet_one_form_atlas_2026-07-26",
        "udt_founding_observer_comparison_semantics_audit_2026-07-27",
        "udt_founding_reciprocity_object_audit_2026-07-27",
        "udt_metric_native_signed_depth_availability_audit_2026-07-26",
        "udt_observer_pair_clock_operator_audit_2026-07-24",
        "udt_premise_reset_audit_2026-07-19",
        "udt_relational_pair_depth_realization_audit_2026-07-24",
    },
    "LIFT_OR_TRANSPORT_PARTIAL": {
        "transverse_reciprocal_realization_selector_2026-07-19",
        "udt_coframe_hopf_bridge_audit_2026-07-23",
        "udt_complete_coframe_metric_telescope_p01_2026-07-27",
        "udt_founded_phi_complete_coframe_extension_audit_2026-07-25",
        "udt_full_local_jet_strata_p02_2026-07-27",
        "udt_intrinsic_optical_transport_atlas_2026-07-27",
        "udt_native_reciprocal_comparison_bundle_audit_2026-07-27",
        "udt_observer_depth_angle_transition_audit_2026-07-24",
        "udt_observer_longitudinal_transverse_cocycle_audit_2026-07-24",
        "udt_reciprocal_subbundle_ownership_audit_2026-07-22",
        "udt_temporal_soldering_atlas_2026-07-22",
        "udt_three_reciprocity_delta_k_audit_2026-07-23",
        "udt_twisted_s3_killing_algebra_audit_2026-07-27",
    },
    "GLOBAL_OR_COMPLETION_PARTIAL": {
        "udt_finite_cell_cartan_transport_atlas_2026-07-23",
        "udt_free_global_seal_transversality_audit_2026-07-21",
        "udt_global_coframe_compatibility_p03_2026-07-27",
        "udt_global_reciprocal_persistence_selector_audit_2026-07-23",
        "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27",
        "udt_phi_causal_interface_atlas_2026-07-22",
        "udt_pre_p06_boundary_selector_audit_2026-07-21",
        "udt_reciprocal_seam_descent_audit_2026-07-23",
        "udt_wrl_xmax_lightcone_frame_audit_2026-07-23",
        "xmax_dynamic_observer_frame_2026-07-19",
    },
    "CONDITIONAL_CONFIGURATION_OR_MULTI_LAYER": {
        "udt_complete_branch_founded_pair_pullback_audit_2026-07-26",
        "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27",
        "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27",
        "udt_complete_physical_comparison_map_audit_2026-07-27",
        "udt_global_reciprocal_bundle_assembly_audit_2026-07-26",
        "udt_observer_pair_path_groupoid_assembly_audit_2026-07-26",
        "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27",
        "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27",
    },
    "NO_SELECTOR_OR_TYPING_RESULT": {
        "udt_cleanroom_metric_reduction_readiness_audit_2026-07-27",
        "udt_complete_metric_realization_zoomout_2026-07-23",
        "udt_complete_relational_configuration_variation_domain_audit_2026-07-26",
        "udt_global_functional_dof_constraint_rank_audit_2026-07-26",
        "udt_global_local_relational_closure_audit_2026-07-25",
        "udt_gr_lorentzian_relational_architecture_audit_2026-07-27",
        "udt_macro_phi_angular_xmax_extension_atlas_2026-07-25",
        "udt_metric_native_nontriviality_connector_audit_2026-07-25",
        "udt_metric_native_selector_rank_closure_audit_2026-07-27",
        "udt_metric_natural_complete_extension_selector_audit_2026-07-27",
        "udt_metric_to_frontier_reference_2026-07-22",
        "udt_native_global_coframe_definition_audit_2026-07-28",
        "udt_observer_pair_xmax_bridge_audit_2026-07-27",
        "udt_relational_metric_fixed_point_typing_audit_2026-07-26",
    },
}


CATEGORY_GRADES = {
    "CONTROL_NAVIGATION_OR_UNRELATED": ("SUMMARY_OR_UNRELATED", "SUMMARY_OR_UNRELATED", "SUMMARY_OR_UNRELATED", "NO_OPERATION"),
    "HISTORICAL_OR_FIREWALLED": ("NEGATIVE_OR_HISTORICAL_ONLY",) * 3 + ("NO_AFFIRMATIVE_OPERATION",),
    "OUT_OF_SCOPE_PARTICLE_OR_ACTION": ("NOT_JOINT_DEPTH_SOURCE", "SCOPED_OTHER_LANE", "NOT_JOINT_GLOBAL_SOURCE", "NO_OPERATION"),
    "PAIR_OR_DEPTH_PARTIAL": ("PARTIAL_OR_CONDITIONAL", "OPEN", "OPEN", "NO_JOINT_OPERATION"),
    "LIFT_OR_TRANSPORT_PARTIAL": ("OPEN_OR_SUPPLIED", "PARTIAL_OR_FAMILY", "OPEN", "NO_JOINT_OPERATION"),
    "GLOBAL_OR_COMPLETION_PARTIAL": ("OPEN_OR_SUPPLIED", "OPEN_OR_CONDITIONAL", "PARTIAL_OR_FAMILY", "NO_JOINT_OPERATION"),
    "CONDITIONAL_CONFIGURATION_OR_MULTI_LAYER": ("PARTIAL_OR_CONDITIONAL", "PARTIAL_OR_CONDITIONAL", "SUPPLIED_OR_OPEN", "NO_DERIVED_JOINT_OPERATION"),
    "NO_SELECTOR_OR_TYPING_RESULT": ("OPEN_OR_TYPED", "OPEN_OR_TYPED", "OPEN_OR_TYPED", "EXPLICIT_NO_SELECTOR"),
}


CATEGORY_BASIS = {
    "CONTROL_NAVIGATION_OR_UNRELATED": "Navigation/current-status material and unrelated moved research artifacts do not introduce a typed joint construction.",
    "HISTORICAL_OR_FIREWALLED": "Historical, superseded, or pre-July material cannot supply affirmative UDT physics and contains no active typed joint operation.",
    "OUT_OF_SCOPE_PARTICLE_OR_ACTION": "The package concerns a particle/action branch or off-shell constraint and does not map the complete metric to all three kinematic outputs.",
    "PAIR_OR_DEPTH_PARTIAL": "The source derives, corrects, or constrains the founded reciprocal pair/depth layer while retaining full-frame or global data as open or supplied.",
    "LIFT_OR_TRANSPORT_PARTIAL": "The source classifies a lift, response, projector, transport, or soldering family but retains physical depth, residual moduli, or global completion.",
    "GLOBAL_OR_COMPLETION_PARTIAL": "The source classifies transport, seal, seam, holonomy, interface, or completion data without deriving the physical depth and complete lift jointly.",
    "CONDITIONAL_CONFIGURATION_OR_MULTI_LAYER": "A complete configuration or exact conditional multi-layer construction exists only after path, depth, branch, lambda, or completion input; residual families remain.",
    "NO_SELECTOR_OR_TYPING_RESULT": "The package explicitly finds missing rank, missing typed arrows, no surviving selector, or an open connector rather than a joint operation.",
}


CANDIDATES = [
    ("C01", "founded_pair_character", "reciprocal-c plus dual Reciprocity", "PAIR", "Exact inverse pair representation; physical comparison and extension remain open."),
    ("C02", "arbitrary_endpoint_cocycle", "delta_f(p,q)=f(q)-f(p)", "DEPTH_FAMILY", "Exact composition for every f proves composition alone does not select physical depth."),
    ("C03", "affine_metric_response_query", "seven-dimensional symmetric response bundle", "LIFT_INFINITESIMAL", "Tensorial first response is derived; finite lift and physical section are open."),
    ("C04", "ordered_pair_projector_family", "X_lambda and exp(delta X_lambda)", "LIFT_FAMILY", "Finite pair lift exists for every real lambda; pair, lambda, and global data are supplied."),
    ("C05", "stationary_Killing_norm_depth", "delta_K=log(N_p/N_q)", "DEPTH_BRANCH", "Metric-native signed depth exists on a supplied stationary branch with intrinsic Killing line."),
    ("C06", "Levi_Civita_path_transport", "coframe parallel transport U_gamma", "TRANSPORT", "Metric-canonical path transport is not reciprocal dilation and does not choose physical paths."),
    ("C07", "stationary_hybrid_comparison", "(D(delta_K),U_gamma)", "STRONGEST_PARTIAL", "Same-lineage reducible clock plus coframe transport; no single reciprocal full lift, lambda selector, or completion."),
    ("C08", "path_groupoid_with_supplied_depth", "C_gamma=(D(delta_gamma),U_gamma)", "CONDITIONAL_MULTI_LAYER", "Exact functor after depth, path, initial pair, lambda, and complete branch are supplied."),
    ("C09", "endpoint_parallel_lambda_plus_one", "global parallel grading", "CONDITIONAL_SELECTOR", "Selects lambda=+1 only by the unentailed path-independence/parallelism premise."),
    ("C10", "reduced_holonomy_lambda_pm_one", "observer or ruler stabilizer reduction", "CONDITIONAL_SELECTOR", "Different supplied reductions give +1 or -1 and do not select a global section."),
    ("C11", "twisted_S3_intrinsic_witness", "intrinsic K,n,screen on complete R x S3", "COMPLETE_CONFIGURATION", "Gives a coherent branch witness and branch depth while lambda/profile/semantics/dynamics remain free."),
    ("C12", "completion_and_seam_catalogue", "caps seams quotients interfaces", "GLOBAL_FAMILY", "Classifies admissible global data but registered premises do not select one."),
    ("C13", "Xmax_asymptotic_pair_bridge", "observer-pair maximum-separation proposal", "GLOBAL_LEAD", "No operational return map or complete comparison law is registered."),
    ("C14", "bootstrap_whole_solution_closure", "global-local self-consistency wording", "UNTYPED_WORKING", "Working interpretation supplies no present domain, codomain, or executable selector."),
    ("C15", "action_or_variation_selector", "conditional variational routes", "DOWNSTREAM", "Kinematic domain is unresolved and no action is licensed to fill it."),
    ("C16", "complete_nonultrastatic_family", "R x S3 with arbitrary admissible phi and real lambda", "COUNTERFAMILY", "Proves complete off-shell existence does not select depth profile, lift modulus, or realization."),
]


CANDIDATE_SOURCES = {
    "C01": "udt_founding_reciprocity_object_audit_2026-07-27/AUDIT_REPORT.md",
    "C02": "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27/AUDIT_REPORT.md",
    "C03": "udt_native_reciprocal_comparison_bundle_audit_2026-07-27/AUDIT_REPORT.md",
    "C04": "udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/AUDIT_REPORT.md",
    "C05": "udt_complete_physical_comparison_map_audit_2026-07-27/AUDIT_REPORT.md",
    "C06": "udt_complete_physical_comparison_map_audit_2026-07-27/AUDIT_REPORT.md",
    "C07": "udt_complete_physical_comparison_map_audit_2026-07-27/AUDIT_REPORT.md",
    "C08": "udt_observer_pair_path_groupoid_assembly_audit_2026-07-26/AUDIT_REPORT.md",
    "C09": "udt_founding_reciprocity_object_audit_2026-07-27/AUDIT_REPORT.md",
    "C10": "udt_metric_natural_complete_extension_selector_audit_2026-07-27/AUDIT_REPORT.md",
    "C11": "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/AUDIT_REPORT.md",
    "C12": "udt_reciprocal_seam_descent_audit_2026-07-23/AUDIT_REPORT.md",
    "C13": "udt_observer_pair_xmax_bridge_audit_2026-07-27/AUDIT_REPORT.md",
    "C14": "udt_metric_native_selector_rank_closure_audit_2026-07-27/AUDIT_REPORT.md",
    "C15": "udt_complete_relational_configuration_variation_domain_audit_2026-07-26/AUDIT_REPORT.md",
    "C16": "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27/AUDIT_REPORT.md",
}


def candidate_matrix() -> list[dict[str, str]]:
    obligations = [f"J{i:02d}" for i in range(1, 16)]
    # PASS means the candidate itself meets the obligation without an unregistered
    # premise. PARTIAL and CONDITIONAL_EXTRA never count as closure.
    defaults = {key: "FAIL" for key in obligations}
    marks: dict[str, dict[str, str]] = {
        "C01": {"J02": "PASS", "J11": "PARTIAL", "J14": "PASS", "J15": "PASS"},
        "C02": {"J04": "CONDITIONAL_EXTRA", "J11": "PASS", "J14": "PASS", "J15": "PASS"},
        "C03": {"J01": "PASS", "J05": "PARTIAL", "J07": "PASS", "J10": "PASS", "J14": "PASS", "J15": "PASS"},
        "C04": {"J01": "PASS", "J02": "PASS", "J05": "PASS", "J06": "PARTIAL", "J07": "PARTIAL", "J10": "PASS", "J11": "PASS", "J14": "PASS", "J15": "PASS"},
        "C05": {"J01": "PASS", "J02": "PASS", "J03": "PARTIAL", "J04": "PASS", "J07": "PASS", "J10": "PASS", "J11": "PASS", "J14": "PASS", "J15": "PASS"},
        "C06": {"J01": "PASS", "J05": "PARTIAL", "J07": "PASS", "J10": "PASS", "J11": "PASS", "J14": "PASS", "J15": "PASS"},
        "C07": {"J01": "PASS", "J02": "PASS", "J03": "PARTIAL", "J04": "PASS", "J05": "PARTIAL", "J06": "FAIL", "J07": "PASS", "J10": "PASS", "J11": "PASS", "J12": "PASS", "J14": "PASS", "J15": "PASS"},
        "C08": {"J01": "PASS", "J02": "PASS", "J03": "CONDITIONAL_EXTRA", "J04": "CONDITIONAL_EXTRA", "J05": "CONDITIONAL_EXTRA", "J06": "PARTIAL", "J07": "PASS", "J10": "PASS", "J11": "PASS", "J12": "PASS", "J14": "PASS", "J15": "PASS"},
        "C09": {"J01": "PASS", "J02": "PASS", "J05": "CONDITIONAL_EXTRA", "J06": "CONDITIONAL_EXTRA", "J11": "CONDITIONAL_EXTRA", "J14": "PASS", "J15": "PASS"},
        "C10": {"J01": "PASS", "J02": "PASS", "J05": "CONDITIONAL_EXTRA", "J06": "CONDITIONAL_EXTRA", "J10": "PASS", "J14": "PASS", "J15": "PASS"},
        "C11": {"J01": "PASS", "J02": "PASS", "J03": "PARTIAL", "J04": "PASS", "J05": "PARTIAL", "J06": "PARTIAL", "J07": "PASS", "J08": "PARTIAL", "J09": "PARTIAL", "J10": "PASS", "J11": "PARTIAL", "J14": "PASS", "J15": "PASS"},
        "C12": {"J08": "PARTIAL", "J09": "PARTIAL", "J14": "PASS", "J15": "PASS"},
        "C13": {"J03": "PARTIAL", "J08": "PARTIAL", "J09": "PARTIAL", "J14": "PASS", "J15": "PASS"},
        "C14": {"J14": "PASS", "J15": "PASS"},
        "C15": {"J14": "PASS", "J15": "PASS"},
        "C16": {"J01": "PASS", "J02": "PASS", "J05": "PARTIAL", "J06": "PARTIAL", "J07": "PASS", "J08": "PASS", "J09": "PARTIAL", "J10": "PASS", "J14": "PASS", "J15": "PASS"},
    }
    rows = []
    for cid, name, _, _, _ in CANDIDATES:
        grade = defaults | marks[cid]
        row = {"candidate_id": cid, "candidate": name, **grade}
        row["all_obligations_pass"] = "YES" if all(grade[key] == "PASS" for key in obligations) else "NO"
        rows.append(row)
    return rows


def main() -> None:
    manifest = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    group_discovery = read_tsv(HERE / "DISCOVERY_GROUP_OUTCOMES.tsv")
    qualified = {row["group"] for row in group_discovery if row["qualifies"] == "YES"}
    assigned = set().union(*GROUP_CATEGORIES.values())
    if assigned != qualified:
        raise AssertionError(f"group assignment mismatch missing={sorted(qualified-assigned)} extra={sorted(assigned-qualified)}")
    if sum(len(groups) for groups in GROUP_CATEGORIES.values()) != len(assigned):
        raise AssertionError("duplicate group category assignment")
    if len(qualified) != 80:
        raise AssertionError(f"expected 80 qualified groups, got {len(qualified)}")
    if len(manifest) != 3044:
        raise AssertionError(f"expected 3044 candidate sources, got {len(manifest)}")

    by_group: dict[str, list[dict[str, str]]] = defaultdict(list)
    proposition_rows = []
    patterns = {
        "affirmative_terms": re.compile(r"\b(DERIVED|SELECTED|FORCED|UNIQUE)\b", re.I),
        "conditional_terms": re.compile(r"\b(CONDITIONAL|GIVEN|SUPPLIED|POSIT|CHOSE)\b", re.I),
        "open_terms": re.compile(r"\b(OPEN|UNDETERMINED|NOT[_ -]DERIVED|UNSELECTED|MISSING)\b", re.I),
        "joint_terms": re.compile(r"\b(joint|simultaneous|whole[- _]solution|same[- _]solution|closure)\b", re.I),
    }
    for row in manifest:
        content = git("cat-file", "blob", row["git_blob"], binary=True)
        assert isinstance(content, bytes)
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise AssertionError(f"source SHA mismatch {row['path']}")
        if len(content) != int(row["size_bytes"]):
            raise AssertionError(f"source size mismatch {row['path']}")
        by_group[row["group"]].append(row)
        text = content.decode("utf-8", "replace")
        counts = {name: sum(bool(pattern.search(line)) for line in text.splitlines()) for name, pattern in patterns.items()}
        proposition_rows.append({
            "source_id": row["source_id"], "path": row["path"], "group": row["group"],
            **counts, "review_scope": "FIXED_BASE_BLOB_MECHANICAL_PROPOSITION_CENSUS",
        })
    write_tsv(
        HERE / "PROPOSITION_CENSUS.tsv",
        ["source_id", "path", "group", *patterns, "review_scope"], proposition_rows,
    )

    group_rows = []
    for category, groups in GROUP_CATEGORIES.items():
        depth, lift, global_grade, joint = CATEGORY_GRADES[category]
        for group in sorted(groups):
            paths = [row["path"] for row in by_group[group]]
            report = next((path for path in paths if path.endswith("/AUDIT_REPORT.md")), None)
            status = next((path for path in paths if path.endswith("/STATUS_LEDGER.tsv")), None)
            primary = report or status or paths[0]
            group_rows.append({
                "group": group,
                "candidate_files": len(paths),
                "category": category,
                "depth_grade": depth,
                "full_frame_grade": lift,
                "global_grade": global_grade,
                "joint_operation_grade": joint,
                "primary_evidence": primary,
                "basis": CATEGORY_BASIS[category],
                "affirmative_joint_operation_found": "NO",
            })
    group_rows.sort(key=lambda row: row["group"])
    write_tsv(
        HERE / "GROUP_ADJUDICATION.tsv",
        ["group", "candidate_files", "category", "depth_grade", "full_frame_grade", "global_grade",
         "joint_operation_grade", "primary_evidence", "basis", "affirmative_joint_operation_found"],
        group_rows,
    )

    ledger_rows = []
    for cid, name, form, layer, ruling in CANDIDATES:
        source = CANDIDATE_SOURCES[cid]
        source_manifest_row = next((row for row in manifest if row["path"] == source), None)
        if source_manifest_row is None:
            raise AssertionError(f"candidate source is outside frozen qualifying manifest: {source}")
        ledger_rows.append({
            "candidate_id": cid, "candidate": name, "mathematical_form": form,
            "strongest_layer": layer, "ruling": ruling,
            "primary_source": source,
            "source_blob": source_manifest_row["git_blob"],
            "source_sha256": source_manifest_row["sha256"],
            "joint_operation": "NO", "status": "PARTIAL_OR_CONDITIONAL" if cid not in {"C14", "C15"} else "UNTYPED_OR_DOWNSTREAM",
        })
    write_tsv(
        HERE / "JOINT_CANDIDATE_LEDGER.tsv",
        ["candidate_id", "candidate", "mathematical_form", "strongest_layer", "ruling", "primary_source",
         "source_blob", "source_sha256", "joint_operation", "status"],
        ledger_rows,
    )
    matrix_rows = candidate_matrix()
    obligations = [f"J{i:02d}" for i in range(1, 16)]
    write_tsv(
        HERE / "JOINT_GATE_MATRIX.tsv",
        ["candidate_id", "candidate", *obligations, "all_obligations_pass"], matrix_rows,
    )

    dependency_rows = [
        {"edge_id": "E01", "from": "founding_reciprocal_pair", "to": "additive_pair_character", "grade": "DERIVED", "missing": "physical arrows and metric-native depth assignment"},
        {"edge_id": "E02", "from": "complete_stationary_metric_plus_intrinsic_K", "to": "delta_K", "grade": "DERIVED_BRANCH_SCOPED", "missing": "arbitrary observer/path and nonstationary extension"},
        {"edge_id": "E03", "from": "complete_metric_plus_supplied_path", "to": "Levi_Civita_coframe_transport", "grade": "DERIVED_MATHEMATICS", "missing": "physical path and reciprocal lift selection"},
        {"edge_id": "E04", "from": "delta_K_plus_Levi_Civita_transport", "to": "stationary_hybrid_comparison", "grade": "CONDITIONAL_EXACT_REDUCIBLE", "missing": "single full reciprocal lift lambda and global completion"},
        {"edge_id": "E05", "from": "ordered_pair_plus_real_lambda", "to": "finite_projector_lift", "grade": "DERIVED_GIVEN_INPUTS", "missing": "pair section and lambda selector"},
        {"edge_id": "E06", "from": "complete_RxS3_configuration", "to": "intrinsic_K_n_screen_and_branch_depth", "grade": "DERIVED_CONFIGURATION", "missing": "realized equations profile lambda semantics"},
        {"edge_id": "E07", "from": "registered_global_catalogues", "to": "completion_families", "grade": "DERIVED_CLASSIFICATION", "missing": "selection descent and interface theorem"},
        {"edge_id": "E08", "from": "bootstrap_wording", "to": "joint_selector", "grade": "OPEN_NO_TYPED_EDGE", "missing": "domain codomain operation and return map"},
        {"edge_id": "E09", "from": "complete_metric", "to": "realized_equations", "grade": "OPEN_NO_TYPED_EDGE", "missing": "native response law"},
    ]
    write_tsv(HERE / "PARTIAL_DEPENDENCY_GRAPH.tsv", ["edge_id", "from", "to", "grade", "missing"], dependency_rows)

    counter_rows = [
        {"control": "K01", "counterfamily": "real lambda in X_lambda", "discriminated_by_registered_joint": "NO", "meaning": "covariance and composition retain a transverse modulus"},
        {"control": "K02", "counterfamily": "arbitrary admissible smooth phi on complete R x S3", "discriminated_by_registered_joint": "NO", "meaning": "complete off-shell geometry does not choose realized depth profile"},
        {"control": "K03", "counterfamily": "delta_f for arbitrary endpoint scalar f", "discriminated_by_registered_joint": "NO", "meaning": "identity reversal and composition do not select physical depth"},
        {"control": "K04", "counterfamily": "twist on versus twist off", "discriminated_by_registered_joint": "NO", "meaning": "stationary clock depth does not by itself choose ruler or screen"},
        {"control": "K05", "counterfamily": "distinct caps seams quotients and interfaces", "discriminated_by_registered_joint": "NO", "meaning": "global classification is not global selection"},
        {"control": "K06", "counterfamily": "off-shell complete configurations", "discriminated_by_registered_joint": "NO", "meaning": "configuration existence is not realized dynamics"},
    ]
    write_tsv(HERE / "COUNTERFAMILY_RESULTS.tsv", ["control", "counterfamily", "discriminated_by_registered_joint", "meaning"], counter_rows)

    category_counts = Counter(row["category"] for row in group_rows)
    proposition_totals = {key: sum(int(row[key]) for row in proposition_rows) for key in patterns}
    result = {
        "schema": "udt-joint-selector-provenance-audit-result-1.0",
        "fixed_base": BASE,
        "source_files_verified": len(manifest),
        "qualified_groups_adjudicated": len(group_rows),
        "candidate_constructions_tested": len(CANDIDATES),
        "obligations_per_candidate": 15,
        "complete_joint_operations": sum(row["all_obligations_pass"] == "YES" for row in matrix_rows),
        "counterfamilies_undiscriminated": sum(row["discriminated_by_registered_joint"] == "NO" for row in counter_rows),
        "group_category_counts": dict(sorted(category_counts.items())),
        "proposition_line_counts": proposition_totals,
        "strongest_partial_candidate": "C07_stationary_hybrid_comparison",
        "strongest_partial_grade": "CONDITIONAL_EXACT_REDUCIBLE_ON_SUPPLIED_STATIONARY_BRANCH_AND_PATH",
        "outcome": "NO_REGISTERED_JOINT_OPERATION_THREE_GAPS_RETAINED",
        "verification_grade": "PENDING_INDEPENDENT_REPLAY",
        "dirty_worktree_contents_read": False,
    }
    (HERE / "AUDIT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
