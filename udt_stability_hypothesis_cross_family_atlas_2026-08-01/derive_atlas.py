#!/usr/bin/env python3
"""Deterministic lineage and cross-family stability atlas."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (PKG / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (PKG / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def anchor(anchor_id: str, path: str, role: str, ruling: str) -> dict[str, str]:
    source = ROOT / path
    if not source.is_file():
        raise RuntimeError(f"missing anchor: {path}")
    return {"anchor_id": anchor_id, "path": path, "sha256": sha256(source), "role": role, "ruling": ruling}


def main() -> None:
    inventory = read_tsv("SOURCE_INVENTORY.tsv")
    families = read_tsv("FAMILY_UNIVERSE.tsv")
    claims = read_tsv("HYPOTHESIS_CLAIM_UNIVERSE.tsv")
    premises = read_tsv("PREMISE_LEDGER.tsv")
    if (len(inventory), len(families), len(claims), len(premises)) != (1469, 7, 8, 18):
        raise RuntimeError("preregistered census mismatch")
    for row in inventory:
        path = ROOT / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            raise RuntimeError(f"source changed: {row['path']}")

    anchors = [
        anchor("A01", "PONDER_MATH_ELEGANCE_2026-07-31.md", "hypothesis origin", "pure ponder; taxonomy-times-stable-basin conjecture, P4 threshold, ring and Hopf language separated by grade"),
        anchor("A02", "udt_p4_stability_slice_2026-07-30/AUDIT_REPORT.md", "P4 conditional stability", "Hopfion direction was method only; P4 mixed exact conditional outcomes"),
        anchor("A03", "udt_p4_stability_slice_2026-07-30/STABILITY_LEDGER.tsv", "P4 family ledger", "S-i, S-ii, massless controls, empty postures, and out-of-scope sectors typed separately"),
        anchor("A04", "udt_p4_stability_slice_2026-07-30/EXACT_DERIVATION.md", "P4 algebra", "odd-pin reduced-core absorption and jet-sector threshold retain explicit scopes"),
        anchor("A05", "udt_p4_cold_adversarial_review_2026-08-01/AUDIT_REPORT.md", "P4 cold scope regrade", "formal response/census program survives; fixed realized solution and full certificates remain open"),
        anchor("A06", "udt_p4_cold_review_repair_2026-08-01/CLOSURE_REPORT.md", "P4 repair closure", "presentation/provenance repairs closed without promoting physics"),
        anchor("A07", "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md", "ring and completion", "all-definite cyclic rings forced massless; one-cell cyclic massive empty; no real-target mass quantization"),
        anchor("A08", "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv", "ring family ledger", "cyclic, acyclic, quotient, massive, massless, and germ branches remain distinct"),
        anchor("A09", "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "Hopfion scope", "existing object is full 3D and static finite-box stable only under conditional carrier/action/boundary premises"),
        anchor("A10", "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv", "Hopfion mechanical status", "carrier is posit; physical boundary and time-live persistence open"),
        anchor("A11", "stability_branch_follow_256_DECISION.md", "Hopfion numerical lineage", "centered-operator instability retracted as Nyquist artifact; corrected result carries explicit criticality and finite-box history"),
        anchor("A12", "udt_stability_foundations_audit_2026-08-01/AUDIT_REPORT.md", "stability foundations", "P4 and Hopfion are separate conditional streams; realization and persistence joins missing"),
        anchor("A13", "udt_stability_foundations_audit_2026-08-01/STABILITY_REQUIREMENT_MATRIX.tsv", "stability notion separation", "geometric, energetic/spectral, and bootstrap stability require different objects"),
        anchor("A14", "udt_stability_foundations_audit_2026-08-01/FIXED_REALIZATION_GATE.tsv", "joint realization gate", "formal modules exist; common live on-shell field/equation/boundary remains open"),
        anchor("A15", "udt_stability_foundations_audit_2026-08-01/STATUS_LEDGER.tsv", "current conditional statuses", "P4 conditional, Hopfion conditional, native stability and bootstrap selection open"),
        anchor("A16", "udt_global_local_self_consistency_premise_audit_2026-08-01/AUDIT_REPORT.md", "bootstrap ceiling", "bootstrap is a distinct unadopted posit in the frozen record, not a derived selection operation"),
        anchor("A17", "CURRENT_SCIENTIFIC_PREMISES.tsv", "premise controller", "carrier, action, boundary, native mass, and bootstrap operation retain controlling statuses"),
        anchor("A18", "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "action ceiling", "complete action, source, boundary charge, and mass remain open"),
    ]
    inventory_by_path = {row["path"]: row for row in inventory}
    if len(inventory_by_path) != 1469 or any(
        item["path"] not in inventory_by_path
        or inventory_by_path[item["path"]]["sha256"] != item["sha256"]
        for item in anchors
    ):
        raise RuntimeError("controlling anchor absent from effective source freeze")
    write_tsv("SOURCE_AUTHORITY_LEDGER.tsv", anchors)

    atlas = [
        {
            "family_id": "F01", "configuration_type": "P4 stationary quadratic jet<=2 S-i cells and mixed crease-glue chains",
            "equation_or_functional": "conditional P4 reduced second variation", "carrier": "NONE_SELECTED",
            "boundary_completion": "mixed/open posture and supplied parity; higher wall germs open; empty closed postures excluded to F06", "existence": "mixed crease-glue reduced witness and conditional nonclosed branches only",
            "mass_status": "conditional M-GEN/M-WALL readouts; no native unconditional mass", "discrete_structure": "supplied parity and posture labels",
            "continuous_structure": "E0 ell moduli pairing and wall germs", "stability_test": "exact reduced/joint second variation",
            "stability_outcome": "free angular-wall branch unstable; odd pin makes zero-trace core positive; whole certificate still open",
            "time_persistence": "OPEN", "bootstrap_role": "NONE_DERIVED", "hopfion_dependency": "NO_RESULT_TRANSFER_METHOD_SHAPE_ONLY",
            "hypothesis_role": "PRIMARY_NON_HOPF_ALGEBRAIC_SPINE", "overall_grade": "CONDITIONAL_PRUNING_EVIDENCE", "source_basis": "A02-A06"
        },
        {
            "family_id": "F02", "configuration_type": "P4 S-ii fields-census P1-4D landing with live lambda",
            "equation_or_functional": "conditional no-m-jet and jet-quadratic P4 sector forms", "carrier": "NONE_SELECTED",
            "boundary_completion": "all-traces-zero witness is germ-independent; class existence premises travel", "existence": "conditional massive landing class; no complete joint realized universe",
            "mass_status": "conditional E0-based readout", "discrete_structure": "census pairing and posture branch labels",
            "continuous_structure": "E0 ell g_p c_m and live moduli", "stability_test": "exact per-mode 2x2 sector Hessian",
            "stability_outcome": "no-m-jet unstable for E0 nonzero; jet sector stable iff 64 E0^2 ell^4 <= g_p c_m pi^4",
            "time_persistence": "OPEN", "bootstrap_role": "NONE_DERIVED", "hopfion_dependency": "NONE",
            "hypothesis_role": "STRONGEST_NON_HOPF_STABLE_UNSTABLE_DICHOTOMY", "overall_grade": "CONDITIONAL_SECTOR_PRUNING_EVIDENCE", "source_basis": "A02-A06"
        },
        {
            "family_id": "F03", "configuration_type": "P4 E0=0 constant and triad-locked massless controls",
            "equation_or_functional": "same conditional P4 quadratic control forms", "carrier": "NONE_SELECTED",
            "boundary_completion": "registered control domains", "existence": "control members exist in scoped atlas",
            "mass_status": "massless in registered readouts", "discrete_structure": "control branch labels only",
            "continuous_structure": "flat zero-mode directions", "stability_test": "positive-semidefinite control Hessians",
            "stability_outcome": "PSD-degenerate controls reproduce flat directions; not isolated stable basins",
            "time_persistence": "OPEN", "bootstrap_role": "NONE", "hopfion_dependency": "NONE",
            "hypothesis_role": "RUN_VALIDATION_AND_NONISOLATION_CONTROL", "overall_grade": "CONTROL_NOT_SURVIVOR_EVIDENCE", "source_basis": "A02-A04"
        },
        {
            "family_id": "F04", "configuration_type": "full-3D Cartesian no-null Hopfion S3-to-S2 sector",
            "equation_or_functional": "conditional L2+L4 carrier functional", "carrier": "ROUND_S2_POSIT",
            "boundary_completion": "fixed computational finite-box boundary; physical finite-cell carrier completion open", "existence": "observed Q approximately 1 toroidal carrier-conditional configuration",
            "mass_status": "finite-box energy available; native unconditional mass open", "discrete_structure": "conditional Hopf topological sector",
            "continuous_structure": "profile size and deformation modes", "stability_test": "corrected no-null static finite-box operator and basin evidence",
            "stability_outcome": "settled static finite-box conditional; not time-live or infinite-volume persistence",
            "time_persistence": "OPEN", "bootstrap_role": "NONE_DERIVED", "hopfion_dependency": "SELF_ONLY",
            "hypothesis_role": "OBJECT_INEQUIVALENT_FULL3D_CONDITIONAL_EXEMPLAR", "overall_grade": "SETTLED_WITHIN_CONDITIONAL_PREMISES", "source_basis": "A09-A11;A15"
        },
        {
            "family_id": "F05", "configuration_type": "uniform closed cyclic rings and completion classes",
            "equation_or_functional": "P4 real period and completion constraints", "carrier": "NONE_SELECTED",
            "boundary_completion": "two-sided cyclic completion; quotient and acyclic branches separate; empty massive one-cell posture excluded to F06", "existence": "massless constant rings exist; massive all-definite rings forbidden; mixed-sign multi-cell massive completion conditional",
            "mass_status": "all-definite cyclic rings forced massless", "discrete_structure": "cycle/posture labels; no integer mass cut on real targets",
            "continuous_structure": "real E0_i L_i balance and germs", "stability_test": "NONE",
            "stability_outcome": "NOT_TESTED; closure/mass classification only", "time_persistence": "OPEN",
            "bootstrap_role": "whole sum-rule vocabulary only; no selector", "hopfion_dependency": "NONE",
            "hypothesis_role": "STRUCTURAL_TAXONOMY_AND_MASS_NEGATIVE_NOT_STABILITY", "overall_grade": "STRUCTURAL_EVIDENCE_ONLY", "source_basis": "A01;A07-A08"
        },
        {
            "family_id": "F06", "configuration_type": "massive cyclic single-cell and double-crease closed postures",
            "equation_or_functional": "P4 completion and wall-trace conditions", "carrier": "NONE_SELECTED",
            "boundary_completion": "cyclic single-valued or double-crease", "existence": "EMPTY in registered massive scopes",
            "mass_status": "massive locus excluded", "discrete_structure": "posture labels", "continuous_structure": "candidate coefficients eliminated by closure",
            "stability_test": "NOT_APPLICABLE_EMPTY_DOMAIN", "stability_outcome": "nonexistence pruning, not instability",
            "time_persistence": "NOT_APPLICABLE", "bootstrap_role": "NONE", "hopfion_dependency": "NONE",
            "hypothesis_role": "NEGATIVE_EXISTENCE_PRUNING_CONTROL", "overall_grade": "EXACT_SCOPED_EMPTY_CONTROL", "source_basis": "A02-A04;A07-A08"
        },
        {
            "family_id": "F07", "configuration_type": "formal static time-live and angular-live P4 modules",
            "equation_or_functional": "formal pointwise response modules; no complete native whole equation", "carrier": "NO_COMPLETE_FIELD_OWNERSHIP",
            "boundary_completion": "complete differentiable finite-cell boundary open", "existence": "formal embeddings only; common nonzero live on-shell field open",
            "mass_status": "no joint realized mass theorem", "discrete_structure": "module/reading branches", "continuous_structure": "formal amplitudes and fields",
            "stability_test": "NONE_ON_JOINT_REALIZED_OBJECT", "stability_outcome": "BLOCKED_BY_REALIZATION_JOIN",
            "time_persistence": "OPEN", "bootstrap_role": "possible future assembly architecture only", "hopfion_dependency": "NONE",
            "hypothesis_role": "MISSING_REALIZATION_JOIN_CONTROL", "overall_grade": "FORMAL_COMPATIBILITY_NOT_STABILITY", "source_basis": "A05-A06;A12-A15"
        },
    ]
    write_tsv("FAMILY_ATLAS.tsv", atlas)

    partitions = [
        {"family_id": "F01", "effective_partition_key": "P4_SI|MASSIVE|NONEMPTY_OR_CONDITIONAL_MIXED_OR_OPEN|STABILITY_EVALUATED", "explicit_exclusion": "massive cyclic one-cell and double-crease empty postures -> F06"},
        {"family_id": "F02", "effective_partition_key": "P4_SII|MASSIVE|FIELDS_CENSUS|STABILITY_EVALUATED", "explicit_exclusion": "P4 S-i and massless controls"},
        {"family_id": "F03", "effective_partition_key": "P4|MASSLESS|E0_ZERO_OR_TRIAD_CONTROL|CONTROL_ONLY", "explicit_exclusion": "all isolated-survivor claims"},
        {"family_id": "F04", "effective_partition_key": "HOPFION|ROUND_S2_POSIT|FULL3D|STATIC_FINITE_BOX", "explicit_exclusion": "every P4 configuration family"},
        {"family_id": "F05", "effective_partition_key": "P4_PERIOD|CYCLIC|MASSLESS_OR_MULTICELL_MIXED|CLOSURE_CLASSIFICATION", "explicit_exclusion": "massive cyclic one-cell and double-crease empty postures -> F06"},
        {"family_id": "F06", "effective_partition_key": "P4_CLOSED|MASSIVE|N1_CYCLIC_OR_DOUBLE_CREASE|EMPTY", "explicit_exclusion": "nonempty and conditionally nonempty stability branches"},
        {"family_id": "F07", "effective_partition_key": "P4_MODULES|FORMAL_STATIC_TIME_ANGULAR|JOINT_REALIZATION_OPEN|NO_STABILITY_OBJECT", "explicit_exclusion": "every realized candidate-family claim"},
    ]
    write_tsv("FAMILY_PARTITION_LEDGER.tsv", partitions)

    lineage = [
        {"claim_id": "H01", "status": "BANKED_MATH_PLUS_PONDER_INTERPRETATION", "load_bearing_sources": "A01-A04;A07-A10", "hopfion_requirement": "NO_FOR_CONTINUOUS_VS_COMPACT_DISTINCTION", "ruling": "real versus compact character distinction is mathematical; assigning mass and charge roles is ponder-grade"},
        {"claim_id": "H02", "status": "SUPPORTED_CONDITIONALLY_NOT_DERIVED_UNIVERSALLY", "load_bearing_sources": "F01;F02;F04", "hopfion_requirement": "NO_FOR_P4_PRUNING__YES_FOR_PRESENT_OBJECT_INEQUIVALENT_SUPPORT", "ruling": "P4 supplies non-Hopf pruning; Hopfion adds a different conditional stable object"},
        {"claim_id": "H03", "status": "WORKING_MULTI_FAMILY_ARCHITECTURE_NOT_PARTICLE_THEOREM", "load_bearing_sources": "H01-H02;F01-F04", "hopfion_requirement": "NO_FOR_FORMULATION__ITS_REMOVAL_REDUCES_CURRENT_SUPPORT_TO_P4", "ruling": "taxonomy-times-basin is not Hopfion-defined and does not identify any family as matter"},
        {"claim_id": "H04", "status": "DERIVED_CONDITIONAL_REDUCED_CORE", "load_bearing_sources": "A02-A06;F01", "hopfion_requirement": "NONE", "ruling": "odd supplied parity absorbs the reduced negative direction; full certificate remains open"},
        {"claim_id": "H05", "status": "DERIVED_CONDITIONAL_SECTOR_DICHOTOMY", "load_bearing_sources": "A02-A06;F02", "hopfion_requirement": "NONE", "ruling": "exact threshold separates P4 S-ii jet-sector Hessian signs, not physical time stability"},
        {"claim_id": "H06", "status": "BANKED_IDENTITIES_PONDER_CLOSURE_ANALOGY", "load_bearing_sources": "A01;A07-A08;F05-F06", "hopfion_requirement": "NONE", "ruling": "ring and whole-cell identities classify completion/mass; residue or survivor interpretation is not a selector"},
        {"claim_id": "H07", "status": "SETTLED_WITHIN_CONDITIONAL_PREMISES", "load_bearing_sources": "A09-A11;F04", "hopfion_requirement": "DEFINITIONAL_FOR_THIS_EXEMPLAR_ONLY", "ruling": "full-3D conditional static exemplar; carrier emergence and time persistence remain open"},
        {"claim_id": "H08", "status": "WORKING_DISTINCT_POSIT_NO_SELECTION_RULE", "load_bearing_sources": "A12-A18", "hopfion_requirement": "NONE", "ruling": "bootstrap could constrain a survivor catalogue but the frozen record supplies no operational membership relation"},
    ]
    write_tsv("LINEAGE_LEDGER.tsv", lineage)

    components = [
        ("G01", "DECLARED_CONFIGURATION_FAMILY"),
        ("G02", "DISCRETE_TAXON_OR_BRANCH_LABEL"),
        ("G03", "CONTINUOUS_PARAMETERS_OR_MODULI"),
        ("G04", "NONEMPTY_STATIONARY_BACKGROUND"),
        ("G05", "SUPPLIED_RESPONSE_OR_FUNCTIONAL"),
        ("G06", "BOUNDARY_OR_COMPLETION_DOMAIN"),
        ("G07", "EXACT_PRUNING_RESULT"),
        ("G08", "ISOLATED_STABLE_BASIN_IN_STATED_SCOPE"),
        ("G09", "TIME_LIVE_PERSISTENCE"),
        ("G10", "BOOTSTRAP_SELECTION"),
    ]
    statuses = {
        "F01": ["PRESENT_SCOPED", "PRESENT_SUPPLIED", "PRESENT", "PRESENT_CONDITIONAL", "PRESENT_CONDITIONAL", "PARTIAL_OPEN", "PRESENT_CONDITIONAL", "OPEN_FULL_CERTIFICATE", "OPEN", "ABSENT"],
        "F02": ["PRESENT_SCOPED", "PRESENT_BRANCH", "PRESENT", "CONDITIONAL_CLASS", "PRESENT_CONDITIONAL", "PARTIAL", "PRESENT_SECTOR", "PRESENT_SECTOR_ONLY", "OPEN", "ABSENT"],
        "F03": ["PRESENT_CONTROL", "PRESENT_CONTROL", "PRESENT_FLAT", "PRESENT_CONTROL", "PRESENT_CONDITIONAL", "PRESENT_CONTROL", "PRESENT_CONTROL", "ABSENT_PSD_DEGENERATE", "OPEN", "ABSENT"],
        "F04": ["PRESENT_CONDITIONAL", "PRESENT_TOPOLOGICAL", "PRESENT", "OBSERVED_CONDITIONAL", "PRESENT_CHOSEN", "SOLVER_ONLY_PHYSICAL_OPEN", "PRESENT_CONDITIONAL", "PRESENT_STATIC_FINITE_BOX_CONDITIONAL", "OPEN", "ABSENT"],
        "F05": ["PRESENT_SCOPED", "PRESENT_COMPLETION", "PRESENT", "PRESENT_MASSLESS_CONDITIONAL", "PRESENT_PERIOD_LAW", "PRESENT_SCOPED", "PRESENT_EXISTENCE_MASS", "NOT_TESTED", "OPEN", "ABSENT"],
        "F06": ["PRESENT_SCOPED", "PRESENT_POSTURE", "ELIMINATED", "EMPTY", "PRESENT_COMPLETION_LAW", "PRESENT_SCOPED", "PRESENT_NONEXISTENCE", "NOT_APPLICABLE", "NOT_APPLICABLE", "ABSENT"],
        "F07": ["PARTIAL_FORMAL", "PRESENT_MODULE", "PRESENT_FORMAL", "OPEN_JOINT", "ABSENT_COMPLETE", "OPEN", "BLOCKED", "BLOCKED", "OPEN", "ABSENT"],
    }
    grammar = [
        {"family_id": family_id, "component_id": component_id, "component": component, "status": statuses[family_id][index]}
        for family_id in [f"F{i:02d}" for i in range(1, 8)]
        for index, (component_id, component) in enumerate(components)
    ]
    write_tsv("COMMON_GRAMMAR_MATRIX.tsv", grammar)

    dependencies = [
        {"edge_id": "D01", "from": "F01", "to": "H04", "role": "LOAD_BEARING_NON_HOPF_ALGEBRA", "removal_effect": "parity-absorption support lost"},
        {"edge_id": "D02", "from": "F02", "to": "H05", "role": "LOAD_BEARING_NON_HOPF_ALGEBRA", "removal_effect": "mass-size-stiffness dichotomy lost"},
        {"edge_id": "D03", "from": "F04", "to": "H07", "role": "LOAD_BEARING_EXEMPLAR", "removal_effect": "full-3D conditional stable exemplar lost"},
        {"edge_id": "D04", "from": "F05", "to": "H06", "role": "STRUCTURAL_ONLY", "removal_effect": "ring/mass closure analogy lost; stability algebra unchanged"},
        {"edge_id": "D05", "from": "F06", "to": "H06", "role": "NEGATIVE_EXISTENCE_CONTROL", "removal_effect": "nonexistence pruning example lost"},
        {"edge_id": "D06", "from": "F07", "to": "H08", "role": "OPEN_JOIN_CONTROL", "removal_effect": "reason time-live/native stability remains blocked obscured"},
        {"edge_id": "D07", "from": "H04", "to": "H03", "role": "ORIGINAL_P4_SPINE", "removal_effect": "one original stability-taxonomy leg lost"},
        {"edge_id": "D08", "from": "H05", "to": "H03", "role": "ORIGINAL_P4_SPINE", "removal_effect": "principal continuous-family pruning law lost"},
        {"edge_id": "D09", "from": "H07", "to": "H03", "role": "OBJECT_INEQUIVALENT_SUPPORT", "removal_effect": "hypothesis survives but present support becomes P4-only"},
        {"edge_id": "D10", "from": "H06", "to": "H03", "role": "STRUCTURAL_CONTEXT", "removal_effect": "global completion interpretation weakens; stability logic survives"},
        {"edge_id": "D11", "from": "H08", "to": "H03", "role": "FUTURE_SELECTION_ARCHITECTURE", "removal_effect": "basin taxonomy remains; universe-level selection interpretation removed"},
        {"edge_id": "D12", "from": "P07_P08", "to": "F04", "role": "CONDITIONAL_CARRIER_FUNCTIONAL", "removal_effect": "Hopfion stability statement becomes undefined, not refuted"},
        {"edge_id": "D13", "from": "P05_P06", "to": "F01_F02", "role": "CONDITIONAL_P4_RESPONSE", "removal_effect": "P4 stability statements become undefined, not transferred to Hopfion"},
        {"edge_id": "D14", "from": "P12_P13", "to": "H08", "role": "WORKING_POSIT_PLUS_OPEN_OPERATION", "removal_effect": "no operational selection exists in either case"},
    ]
    write_tsv("DEPENDENCY_GRAPH.tsv", dependencies)

    deletion_control = {
        "all_evidence": {
            "original_P4_spine_components": 2,
            "object_inequivalent_stability_support_streams": 2,
        },
        "remove_Hopfion_F04_H07": {
            "original_P4_spine_components": 2,
            "object_inequivalent_stability_support_streams": 1,
            "original_hypothesis_formulation_survives": True,
            "P4_algebra_survives": True,
        },
        "remove_P4_F01_F02_H04_H05": {
            "original_P4_spine_components": 0,
            "object_inequivalent_stability_support_streams": 1,
            "original_July31_algebraic_spine_survives": False,
            "conditional_Hopfion_exemplar_survives": True,
        },
        "scope": "finite dependency deletion control; not counterfactual physics",
    }
    (PKG / "DELETION_CONTROL.json").write_text(json.dumps(deletion_control, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    status = [
        {"claim": "original_hypothesis_lineage", "status": "P4_ALGEBRAIC_SPINE_PLUS_BROADER_STRUCTURAL_PONDER", "basis": "H01-H06;D01-D10", "limit": "ponder identifications not derivations"},
        {"claim": "Hopfion_dependency", "status": "NOT_REQUIRED_FOR_FORMULATION_OR_P4_ALGEBRA", "basis": "F01-F02;H04-H05;D01-D03;D07-D09", "limit": "removal loses current object-inequivalent full-3D exemplar"},
        {"claim": "P4_dependency", "status": "LOAD_BEARING_TO_ORIGINAL_JULY31_ALGEBRAIC_SPINE", "basis": "A01-A06;H04-H05", "limit": "P4 remains conditional formal response/census evidence"},
        {"claim": "cross_family_architecture", "status": "SUPPORTED_CONDITIONALLY_NOT_UNIVERSALLY_DERIVED", "basis": "F01-F04;H02-H03", "limit": "P4 and Hopfion operators/configuration spaces differ"},
        {"claim": "discrete_species_catalog", "status": "NOT_DERIVED_OR_OBSERVED", "basis": "F01-F04;H03-H05;G02-G08", "limit": "P4 threshold leaves a continuous sector; one conditional Hopf sector is not a particle spectrum"},
        {"claim": "shared_metric_native_stability_operator", "status": "NOT_FOUND", "basis": "P05-P11;G05-G09", "limit": "no action/carrier/boundary transfer permitted"},
        {"claim": "rings_and_empty_branches", "status": "STRUCTURAL_OR_EXISTENCE_PRUNING_NOT_STABILITY", "basis": "F05-F06", "limit": "do not count as stable basins"},
        {"claim": "time_live_persistence", "status": "ZERO_OF_SEVEN_FAMILIES_DERIVED", "basis": "G09;A09-A15", "limit": "static/sector Hessians cannot promote"},
        {"claim": "bootstrap_selection", "status": "ZERO_OF_SEVEN_FAMILIES_SELECTED", "basis": "G10;A16-A18", "limit": "bootstrap remains working distinct posit without membership law"},
        {"claim": "overall", "status": "HYPOTHESIS_MULTI_FAMILY_SUPPORTED_NOT_DERIVED", "basis": "F01-F07;H01-H08;G01-G10;D01-D14", "limit": "conditional architecture only; no particle ontology or universal law"},
    ]
    write_tsv("STATUS_LEDGER.tsv", status)

    result = {
        "outcome": "HYPOTHESIS_MULTI_FAMILY_SUPPORTED_NOT_DERIVED",
        "source_paths_verified": 1469,
        "source_anchors": 18,
        "premises": 18,
        "families": 7,
        "family_partition_rows": 7,
        "family_overlap_after_correction": 0,
        "post_prereg_partition_correction": True,
        "post_prereg_source_admission_correction": True,
        "hypothesis_claims": 8,
        "grammar_components": 10,
        "grammar_cells": 70,
        "dependency_edges": 14,
        "object_inequivalent_stability_support_streams": 2,
        "non_hopf_load_bearing_stability_families": 2,
        "Hopfion_required_for_original_hypothesis_formulation": False,
        "Hopfion_required_for_P4_algebra": False,
        "Hopfion_removal_preserves_hypothesis_but_reduces_current_support_to_P4": True,
        "P4_required_for_original_July31_algebraic_spine": True,
        "shared_metric_native_stability_operator_found": False,
        "discrete_species_catalog_derived": False,
        "isolated_multi_basin_spectrum_observed": False,
        "P4_threshold_is_continuous_region": True,
        "time_live_persistence_derived_families": 0,
        "bootstrap_selected_families": 0,
        "bootstrap_law_adopted": False,
        "new_stability_solve_run": False,
        "gpu_used": False,
    }
    (PKG / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS cross-family atlas: sources=1469 families=7 outcome=HYPOTHESIS_MULTI_FAMILY_SUPPORTED_NOT_DERIVED")


if __name__ == "__main__":
    main()
