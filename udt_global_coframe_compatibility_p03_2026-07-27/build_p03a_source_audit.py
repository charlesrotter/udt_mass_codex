#!/usr/bin/env python3
"""Build the preregistered P03-A source-availability audit.

This program is deliberately fail-closed.  It reads only paths frozen in
SOURCE_MANIFEST.tsv.  In particular it does not import the unregistered P02
detailed ledgers needed to manufacture a lossless motif-family projection.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
MANIFEST = OUT / "SOURCE_MANIFEST.tsv"

CLASSES = {
    "GLOBALLY_CONSTRUCTIBLE_REGISTERED",
    "CONDITIONAL_COMPLETE_GIVEN_EXPLICIT_SUPPLIED_DATA",
    "LOCAL_OR_FORMAL_ONLY",
    "PARTIAL_GLOBAL_DEFINITION",
    "NAME_ONLY_OR_SCHEMA_ONLY",
    "BLOCKED_CONFLICTING_PROVENANCE",
    "OUT_OF_SCOPE_PHYSICS_DEPENDENT",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_rule(path: str) -> dict[str, str]:
    """Return an explicit, conservative rule for one frozen source."""
    name = Path(path).name
    common = {
        "domain_chart_cover": "NOT_A_COMPLETE_CHART_COVER",
        "complete_coframe_metric": "NOT_SUPPLIED",
        "overlap_transition_maps": "NOT_SUPPLIED",
        "finite_cell_completion_data": "NOT_SUPPLIED",
        "regularity_nondegeneracy": "NOT_COMPLETE",
        "causal_interface_rules": "NOT_COMPLETE",
        "topology_global_descent": "NOT_COMPLETE",
        "construction_sufficiency": "INSUFFICIENT_FOR_ONE_COMPLETE_P03_OBJECT",
        "provenance": "FROZEN_REGISTERED_EVIDENCE",
    }

    if path == "CURRENT_SCIENTIFIC_PREMISES.tsv":
        return common | {
            "audit_rule": "CURRENT_PREMISE_CONTROL",
            "source_role": "controlling premise and precedence registry",
            "classification": "LOCAL_OR_FORMAL_ONLY",
            "provenance": "CURRENT_CONTROLLING_PREMISE_REGISTRY",
            "ruling": "Controls interpretation; it is not itself a global metric candidate.",
        }

    if path.startswith("udt_full_local_jet_strata_p02_2026-07-27/"):
        role = {
            "AUDIT_REPORT.md": "bounded P02 local-atlas report",
            "STATUS_LEDGER.tsv": "bounded P02 claim ledger",
            "AXIS_CONTRACT.tsv": "P02 local-axis definitions",
            "STRATUM_CENSUS.json": "aggregate P02-A census",
            "P02B_CENSUS.json": "aggregate P02-B census",
            "NEXT_STEP.md": "P02 handoff and limit statement",
        }[name]
        return common | {
            "audit_rule": "P02_LOCAL_AGGREGATE",
            "source_role": role,
            "classification": "LOCAL_OR_FORMAL_ONLY",
            "domain_chart_cover": "BOUNDED_LOCAL_CARTESIAN_JET_CHART",
            "causal_interface_rules": "LOCAL_CAUSAL_CLASSES_ONLY_NO_GLOBAL_INTERFACE",
            "construction_sufficiency": "LOCAL_OR_AGGREGATE_ONLY;DETAILED_PROJECTION_LEDGERS_NOT_FROZEN",
            "ruling": "Supplies local ranks/counts but no global coframe; frozen inputs cannot enumerate the 7,897 constructive strata losslessly.",
        }

    if path.startswith("udt_founded_phi_complete_coframe_extension_audit_2026-07-25/"):
        return common | {
            "audit_rule": "FOUNDED_EXTENSION_CLASS",
            "source_role": f"founded-phi extension evidence: {name}",
            "classification": "PARTIAL_GLOBAL_DEFINITION",
            "domain_chart_cover": "ONE_REGISTERED_POSITIVE_TRIANGULAR_CHART",
            "complete_coframe_metric": "POINTWISE_EXTENSION_CLASS_NOT_SELECTED_FIELD",
            "regularity_nondegeneracy": "POINTWISE_POSITIVE_TRIANGULAR_AND_DETERMINANT_CONDITIONS",
            "construction_sufficiency": "POINTWISE_CLASSIFICATION_ONLY;PROFILE_JOIN_AND_BOUNDARY_OPEN",
            "provenance": "FOUNDED_TWO_CHANNEL_ACTION_DERIVED;FOUR_DIMENSIONAL_EXTENSION_UNSELECTED",
            "ruling": "Defines local extension freedom but no unique global coframe, profile, overlap, or completion.",
        }

    if path.startswith("complete_coframe_seal_involution_2026-07-20/"):
        cls = "PARTIAL_GLOBAL_DEFINITION"
        return common | {
            "audit_rule": "SEAL_INVOLUTION_FAMILY",
            "source_role": f"conditional seal/involution evidence: {name}",
            "classification": cls,
            "domain_chart_cover": "BLOCKWISE_LOCAL_EXTENSION_AND_SEAL_ACTION",
            "complete_coframe_metric": "CONDITIONAL_BLOCK_WITNESSES_NOT_SELECTED_COFRAME",
            "finite_cell_completion_data": "ALGEBRAIC_SEAL_LIFTS_ONLY",
            "regularity_nondegeneracy": "BLOCKWISE_ALGEBRAIC_CONDITIONS",
            "topology_global_descent": "GLOBAL_CAP_TOPOLOGY_AND_LIFTS_OPEN",
            "construction_sufficiency": "MULTIPLE_CONDITIONAL_COMPLETIONS;NO_COMPLETE_GLOBAL_FIELD",
            "provenance": "CONDITIONAL_SUPPLIED_SEAL_AND_LIFT_PREMISES",
            "ruling": "Records alternative seal actions; none supplies the full charted finite-cell coframe.",
        }

    if path.startswith("udt_global_metric_assembly_atlas_2026-07-22/"):
        if name == "COMPLETION_CLASS_REGISTRY.tsv":
            cls = "NAME_ONLY_OR_SCHEMA_ONLY"
            role = "twelve completion-type schemas"
        elif name == "MOTIF_COMPLETION_ATLAS.tsv":
            cls = "PARTIAL_GLOBAL_DEFINITION"
            role = "motif/completion compatibility requirements"
        elif name == "CAP_PAIR_WITNESSES.tsv":
            cls = "PARTIAL_GLOBAL_DEFINITION"
            role = "exact cap-pair lattice/topology witnesses"
        elif name == "TORUS_MONODROMY_REGISTRY.tsv":
            cls = "PARTIAL_GLOBAL_DEFINITION"
            role = "exact torus monodromy examples"
        elif name == "BUNDLE_HOLONOMY_ATLAS.tsv":
            cls = "PARTIAL_GLOBAL_DEFINITION"
            role = "bundle/holonomy obligation atlas"
        else:
            cls = "PARTIAL_GLOBAL_DEFINITION"
            role = f"global assembly evidence: {name}"
        return common | {
            "audit_rule": "GLOBAL_COMPLETION_SCHEMA",
            "source_role": role,
            "classification": cls,
            "domain_chart_cover": "COMPLETION_TYPES_AND_LOCAL_ORBIT_CHART_REQUIREMENTS",
            "overlap_transition_maps": "REQUIREMENTS_RECORDED;ACTUAL_MAPS_NOT_GENERALLY_SUPPLIED",
            "finite_cell_completion_data": "CAP_GLUE_MONODROMY_SCHEMAS_AND_EXACT_SUBCONTROLS",
            "regularity_nondegeneracy": "CONDITIONAL_REQUIREMENTS_NOT_SOLVED_PROFILES",
            "topology_global_descent": "TOPOLOGY_CLASSES_REGISTERED;GLOBAL_METRIC_DESCENT_OPEN",
            "construction_sufficiency": "COMPATIBILITY_SCHEMA_NOT_COMPLETE_METRIC_WITNESS",
            "ruling": "The atlas itself states that its crosses are requirements, not complete global metric realizations.",
        }

    if path.startswith("udt_finite_cell_cartan_transport_atlas_2026-07-23/"):
        cls = "LOCAL_OR_FORMAL_ONLY" if name in {"CAUSAL_TRANSITION_ATLAS.tsv", "CONNECTION_BLOCK_ATLAS.tsv"} else "PARTIAL_GLOBAL_DEFINITION"
        return common | {
            "audit_rule": "CARTAN_LOCAL_RULE_COMPLETION_CROSS",
            "source_role": f"Cartan causal/transport evidence: {name}",
            "classification": cls,
            "domain_chart_cover": "EXACT_LOCAL_CAUSAL_NORMAL_FORMS_CROSSED_WITH_COMPLETION_TYPES",
            "causal_interface_rules": "NULL_AND_ZERO_DEGENERATION_CLASSIFIED;THROUGH_INTERFACE_LAW_OPEN",
            "topology_global_descent": "TWELVE_CLASS_CROSS_WITHOUT_COMPLETE_FIELDS",
            "construction_sufficiency": "LOCAL_TRANSPORT_RULES_ONLY;ZERO_COMPLETE_ON_SHELL_FIELDS",
            "provenance": "EXACT_LOCAL_CARTAN_ALGEBRA;GLOBAL_PROFILE_CONDITIONAL",
            "ruling": "Classifies persistence/mixing/degeneration but supplies no complete (g,phi) field.",
        }

    if path.startswith("udt_global_reciprocal_bundle_assembly_audit_2026-07-26/"):
        return common | {
            "audit_rule": "GLOBAL_PAIR_BUNDLE_ASSEMBLY",
            "source_role": f"global pair-bundle evidence: {name}",
            "classification": "PARTIAL_GLOBAL_DEFINITION",
            "domain_chart_cover": "REGULAR_ORDERED_PAIR_FRAME_PATH_BUNDLE;TWO_S3_CONTROLS",
            "complete_coframe_metric": "TWO_COMPLETE_ULTRASTATIC_S3_CONTROLS_ONLY",
            "overlap_transition_maps": "PAIR_BUNDLE_CONJUGATION_AND_PATH_COMPOSITION_EXACT",
            "finite_cell_completion_data": "ONLY_FC04_HAS_CONCRETE_CONTROLS",
            "regularity_nondegeneracy": "REGULAR_PAIR_BUNDLE;CUT_LOCI_PATH_SET_VALUED",
            "causal_interface_rules": "SEPARATE_GRADIENT_DERIVED_PAIR_NOT_SUPPLIED",
            "topology_global_descent": "PATHWISE_ALL_LAMBDA;ENDPOINT_PARALLELISM_CONTROL_SPECIFIC",
            "construction_sufficiency": "GLOBAL_TYPED_READOUT_EXISTS;SIGNED_DEPTH_AND_PHYSICAL_BRANCH_ABSENT",
            "provenance": "RELATIONAL_READOUT_CONDITIONAL;NO_SELECTED_DEPTH_OR_VARIATION",
            "ruling": "Global bundle assembly is real, but it does not furnish the founded physical phi profile required by P03.",
        }

    if path.startswith("udt_complete_branch_founded_pair_pullback_audit_2026-07-26/"):
        cls = "CONDITIONAL_COMPLETE_GIVEN_EXPLICIT_SUPPLIED_DATA" if name == "CONCRETE_REPRESENTATIVE_ATLAS.tsv" else "PARTIAL_GLOBAL_DEFINITION"
        return common | {
            "audit_rule": "COMPLETE_BRANCH_PULLBACK",
            "source_role": f"complete-control pullback evidence: {name}",
            "classification": cls,
            "domain_chart_cover": "ROUND_AND_BERGER_S3_PRODUCT_CONTROLS_PLUS_INCOMPLETE_WRL",
            "complete_coframe_metric": "Q01_CONDITIONAL_ON_SHELL;Q02_COMPLETE_OFF_SHELL;Q03_LOCAL;Q04_ABSENT",
            "overlap_transition_maps": "Q01_Q02_GLOBAL_HOMOGENEOUS_JOINS_SUPPLIED",
            "finite_cell_completion_data": "Q01_Q02_ONLY_IN_FC04",
            "regularity_nondegeneracy": "Q01_Q02_REGULAR_COMPLETE_CONTROLS",
            "causal_interface_rules": "NO_FOUNDED_DPHI_PROFILE_OR_INTERFACE",
            "topology_global_descent": "Q01_Q02_S3_GLOBAL;OTHER_CLASSES_NO_REPRESENTATIVE",
            "construction_sufficiency": "COMPLETE_METRIC_CONTROLS_EXIST_BUT_FOUNDED_PAIR_DEPTH_GATE_FAILS",
            "provenance": "Q01_CONDITIONAL_C2;Q02_OFF_SHELL_CONTROL;NO_SELECTED_PHYSICAL_BRANCH",
            "ruling": "The only complete metrics are ultrastatic and do not supply founded observer-pair depth; cross-splicing WR-L is forbidden.",
        }

    if path.startswith("udt_complete_relational_configuration_variation_domain_audit_2026-07-26/"):
        return common | {
            "audit_rule": "RELATIONAL_TYPE_AND_VARIATION_OWNERSHIP",
            "source_role": f"configuration/variation type evidence: {name}",
            "classification": "LOCAL_OR_FORMAL_ONLY",
            "domain_chart_cover": "TYPE_CLASSIFICATION_NOT_METRIC_CHART_CONSTRUCTION",
            "causal_interface_rules": "NOT_A_FIELD_PROFILE",
            "construction_sufficiency": "OWNERSHIP_AND_OPEN_GATE_CLASSIFICATION_ONLY",
            "provenance": "FOUNDED_PHI_NOT_INDEPENDENT;FULL_METRIC_VARIATION_REQUIRED;DOMAIN_OPEN",
            "ruling": "Prevents category errors but supplies neither a global branch nor its variation law.",
        }

    if path.startswith("udt_global_functional_dof_constraint_rank_audit_2026-07-26/"):
        return common | {
            "audit_rule": "CORRECTED_DOF_AND_COMPLETION_COUNT",
            "source_role": f"corrected degree-of-freedom evidence: {name}",
            "classification": "LOCAL_OR_FORMAL_ONLY",
            "domain_chart_cover": "GENERIC_LOCAL_METRIC_AND_COMPLETION_COUNTING",
            "construction_sufficiency": "COUNTING_AND_PREMISE_CORRECTION_ONLY",
            "provenance": "FOUNDED_PHI_PRECEDENCE_CORRECTION;STRONG_CSN_INACTIVE",
            "ruling": "Constrains interpretation; it does not construct a complete coframe.",
        }

    raise AssertionError(f"No source audit rule for {path}")


# Tables whose rows actually name construction candidates, compatibility
# cases, or ontology/variation candidates.  Status ledgers are source evidence
# but are not duplicated as candidate objects here.
OBJECT_TABLES: dict[str, tuple[str, str]] = {
    "udt_founded_phi_complete_coframe_extension_audit_2026-07-25/EXTENSION_CLASS_LEDGER.tsv": ("EXTENSION_CLASS", "PARTIAL_GLOBAL_DEFINITION"),
    "complete_coframe_seal_involution_2026-07-20/EXTENSION_FAMILY_LEDGER.tsv": ("SEAL_EXTENSION_FAMILY", "PARTIAL_GLOBAL_DEFINITION"),
    "complete_coframe_seal_involution_2026-07-20/COMPLETE_EXTENSION_WITNESSES.tsv": ("SEAL_EXTENSION_WITNESS", "PARTIAL_GLOBAL_DEFINITION"),
    "complete_coframe_seal_involution_2026-07-20/REQUIREMENT_MATRIX.tsv": ("SEAL_REQUIREMENT_CASE", "PARTIAL_GLOBAL_DEFINITION"),
    "complete_coframe_seal_involution_2026-07-20/OUTCOME_BRANCH_LEDGER.tsv": ("SEAL_OUTCOME_BRANCH", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv": ("COMPLETION_CLASS", "NAME_ONLY_OR_SCHEMA_ONLY"),
    "udt_global_metric_assembly_atlas_2026-07-22/MOTIF_COMPLETION_ATLAS.tsv": ("MOTIF_COMPLETION_COMPATIBILITY", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_global_metric_assembly_atlas_2026-07-22/CAP_PAIR_WITNESSES.tsv": ("CAP_PAIR_TOPOLOGY_WITNESS", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_global_metric_assembly_atlas_2026-07-22/BUNDLE_HOLONOMY_ATLAS.tsv": ("BUNDLE_HOLONOMY_OBLIGATION", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_global_metric_assembly_atlas_2026-07-22/TORUS_MONODROMY_REGISTRY.tsv": ("TORUS_MONODROMY_CASE", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_finite_cell_cartan_transport_atlas_2026-07-23/FINITE_CELL_CARTAN_TRANSPORT_ATLAS.tsv": ("CARTAN_COMPLETION_CASE", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_finite_cell_cartan_transport_atlas_2026-07-23/COMPLETION_CAUSAL_CROSS.tsv": ("COMPLETION_CAUSAL_CASE", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_finite_cell_cartan_transport_atlas_2026-07-23/CAUSAL_TRANSITION_ATLAS.tsv": ("CAUSAL_TRANSITION_CONTROL", "LOCAL_OR_FORMAL_ONLY"),
    "udt_finite_cell_cartan_transport_atlas_2026-07-23/CONNECTION_BLOCK_ATLAS.tsv": ("CONNECTION_DOMAIN", "LOCAL_OR_FORMAL_ONLY"),
    "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/COMPLETION_UNIVERSE.tsv": ("PAIR_BUNDLE_COMPLETION_CASE", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/COMPLETION_ASSEMBLY_ATLAS.tsv": ("PAIR_BUNDLE_ASSEMBLY_CASE", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/ASSEMBLY_GATE_UNIVERSE.tsv": ("ASSEMBLY_GATE", "LOCAL_OR_FORMAL_ONLY"),
    "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/ASSEMBLY_GATE_OUTCOMES.tsv": ("ASSEMBLY_GATE_OUTCOME", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/HOMOGENEOUS_HOLONOMY_ATLAS.tsv": ("HOMOGENEOUS_HOLONOMY_CONTROL", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/BRANCH_PULLBACK_ATLAS.tsv": ("BRANCH_PULLBACK_CASE", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/COMPLETION_PULLBACK_ATLAS.tsv": ("COMPLETION_PULLBACK_CASE", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/CONCRETE_REPRESENTATIVE_ATLAS.tsv": ("CONCRETE_REPRESENTATIVE", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/EIGHT_GATE_MATRIX.tsv": ("CONCRETE_REPRESENTATIVE_GATE_CASE", "PARTIAL_GLOBAL_DEFINITION"),
    "udt_complete_branch_founded_pair_pullback_audit_2026-07-26/HOMOGENEOUS_MOTIF_PULLBACK.tsv": ("HOMOGENEOUS_MOTIF_CASE", "LOCAL_OR_FORMAL_ONLY"),
    "udt_complete_relational_configuration_variation_domain_audit_2026-07-26/CONFIGURATION_OBJECT_UNIVERSE.tsv": ("CONFIGURATION_OBJECT", "LOCAL_OR_FORMAL_ONLY"),
    "udt_complete_relational_configuration_variation_domain_audit_2026-07-26/CONFIGURATION_OBJECT_ADJUDICATION.tsv": ("CONFIGURATION_ADJUDICATION", "LOCAL_OR_FORMAL_ONLY"),
    "udt_complete_relational_configuration_variation_domain_audit_2026-07-26/VARIATION_CANDIDATE_UNIVERSE.tsv": ("VARIATION_CANDIDATE", "OUT_OF_SCOPE_PHYSICS_DEPENDENT"),
    "udt_complete_relational_configuration_variation_domain_audit_2026-07-26/VARIATION_DOMAIN_ADJUDICATION.tsv": ("VARIATION_ADJUDICATION", "OUT_OF_SCOPE_PHYSICS_DEPENDENT"),
    "udt_complete_relational_configuration_variation_domain_audit_2026-07-26/OPEN_GATE_MATRIX.tsv": ("OPEN_CONFIGURATION_GATE", "OUT_OF_SCOPE_PHYSICS_DEPENDENT"),
    "udt_global_functional_dof_constraint_rank_audit_2026-07-26/COMPLETION_UNIVERSE.tsv": ("DOF_COMPLETION_CASE", "NAME_ONLY_OR_SCHEMA_ONLY"),
    "udt_global_functional_dof_constraint_rank_audit_2026-07-26/COMPLETION_DOF_ATLAS.tsv": ("DOF_COMPLETION_ADJUDICATION", "LOCAL_OR_FORMAL_ONLY"),
}


def availability_for(kind: str, row: dict[str, str], base_class: str) -> dict[str, str]:
    cls = base_class
    first_value = next(iter(row.values()))
    domain = "PARTIAL_OR_SCHEMA"
    coframe = "NO_COMPLETE_COFRAME_IN_THIS_ROW"
    overlaps = "NOT_COMPLETE"
    completion = "PARTIAL_OR_CONDITIONAL"
    regularity = "PARTIAL_OR_CONDITIONAL"
    causal = "NOT_A_COMPLETE_FIELD_HISTORY"
    topology = "PARTIAL_OR_CONDITIONAL"
    construction = "NOT_SUFFICIENT_FOR_P03_B"
    provenance = "FROZEN_SOURCE_ROW;NO_PHYSICAL_SELECTION"
    p03_gate = "FAIL_INCOMPLETE_GLOBAL_OBJECT"
    ruling = "Named evidence row is not one coherent complete founded-(g,phi) finite-cell construction."

    if kind == "CONCRETE_REPRESENTATIVE":
        rep = row["representative_id"]
        if rep in {"Q01_ROUND_S3_B19", "Q02_SQUASHED_S3_OFF_SHELL"}:
            cls = "CONDITIONAL_COMPLETE_GIVEN_EXPLICIT_SUPPLIED_DATA"
            domain = "COMPLETE_S3_PRODUCT_CONTROL"
            coframe = "YES_COMPLETE_METRIC_CONTROL"
            overlaps = "YES_GLOBAL_HOMOGENEOUS_JOINS"
            completion = "YES_FC04_TWO_CAP_P1_CONTROL"
            regularity = "YES_WITH_RECORDED_CONDITIONAL_OR_OFF_SHELL_STATUS"
            causal = "NO_FOUNDED_DPHI_FIELD_OR_INTERFACE"
            topology = "YES_S3_CONTROL"
            construction = "METRIC_COMPLETE;FOUNDED_PAIR_DEPTH_ABSENT"
            p03_gate = "FAIL_MISSING_FOUNDED_PHI_PROFILE"
            ruling = "Complete metric control, but it is ultrastatic and lacks the founded observer-pair depth needed to join P02 motifs."
        elif rep == "Q03_WRL_LOCAL":
            cls = "LOCAL_OR_FORMAL_ONLY"
            domain = "LOCAL_STATIC_SPHERICAL_CHART"
            coframe = "LOCAL_ONLY"
            p03_gate = "FAIL_INCOMPLETE_GLOBAL_REPRESENTATIVE"
            ruling = "Nontrivial local clock profile without a complete recentered finite cell."
        elif rep == "Q04_PHYSICAL_XMAX_JOIN":
            cls = "NAME_ONLY_OR_SCHEMA_ONLY"
            p03_gate = "FAIL_ABSENT_REPRESENTATIVE"
            ruling = "Registered missing-object label; no representative exists."

    if kind == "CAP_PAIR_TOPOLOGY_WITNESS":
        topology = "EXACT_LATTICE_TOPOLOGY_CLASS_FOR_SAMPLED_CAP_PAIR"
        completion = "CAP_PAIR_ONLY_NO_METRIC_PROFILE"
        ruling = "Exact cap lattice/topology witness, not a coframe or cap-jet construction."
    elif kind == "TORUS_MONODROMY_CASE":
        topology = "EXACT_REGISTERED_GL2Z_MONODROMY"
        completion = "MONODROMY_ONLY_NO_METRIC_PROFILE"
        ruling = "Exact monodromy data, not a descended complete metric."
    elif kind == "CAUSAL_TRANSITION_CONTROL":
        causal = "EXACT_LOCAL_TRANSITION_OR_DEGENERATION_CONTROL"
        ruling = "Local causal transition control; no global through-interface law or field supplied."
    elif kind in {"CONFIGURATION_OBJECT", "CONFIGURATION_ADJUDICATION"}:
        ruling = "Type/ownership evidence only; not a global metric candidate."
    elif kind.startswith("VARIATION") or kind == "OPEN_CONFIGURATION_GATE":
        p03_gate = "EXCLUDED_OPEN_DOWNSTREAM_VARIATION_DOMAIN"
        ruling = "Variation-domain candidate is open/downstream and cannot supply P03 geometry."

    assert cls in CLASSES
    return {
        "classification": cls,
        "domain_chart_cover": domain,
        "complete_coframe_metric": coframe,
        "overlap_transition_maps": overlaps,
        "finite_cell_completion_data": completion,
        "regularity_nondegeneracy": regularity,
        "causal_interface_rules": causal,
        "topology_global_descent": topology,
        "construction_sufficiency": construction,
        "provenance": provenance,
        "P03B_gate": p03_gate,
        "ruling": ruling,
        "source_row_label": first_value,
    }


def main() -> None:
    manifest = read_tsv(MANIFEST)
    assert len(manifest) == 57
    assert len({r["path"] for r in manifest}) == 57
    by_path = {r["path"]: r for r in manifest}

    source_rows: list[dict[str, object]] = []
    for item in manifest:
        path = item["path"]
        absolute = ROOT / path
        assert absolute.is_file(), path
        assert sha256(absolute) == item["sha256"], path
        assert absolute.stat().st_size == int(item["size_bytes"]), path
        rule = source_rule(path)
        assert rule["classification"] in CLASSES
        source_rows.append({
            "source_id": item["source_id"],
            "path": path,
            "sha256": item["sha256"],
            **rule,
        })

    source_fields = [
        "source_id", "path", "sha256", "audit_rule", "source_role", "classification",
        "domain_chart_cover", "complete_coframe_metric", "overlap_transition_maps",
        "finite_cell_completion_data", "regularity_nondegeneracy", "causal_interface_rules",
        "topology_global_descent", "construction_sufficiency", "provenance", "ruling",
    ]
    write_tsv(OUT / "SOURCE_ADJUDICATION.tsv", source_fields, source_rows)

    object_rows: list[dict[str, object]] = []
    for path, (kind, base_class) in OBJECT_TABLES.items():
        assert path in by_path, f"unfrozen candidate table {path}"
        source_id = by_path[path]["source_id"]
        for index, row in enumerate(read_tsv(ROOT / path), start=1):
            availability = availability_for(kind, row, base_class)
            row_digest = hashlib.sha256(
                "\t".join(row.values()).encode("utf-8")
            ).hexdigest()
            object_rows.append({
                "object_occurrence_id": f"{source_id}:R{index:04d}",
                "object_kind": kind,
                "source_id": source_id,
                "source_path": path,
                "source_row_number": index,
                "source_row_label": availability.pop("source_row_label"),
                "source_row_sha256": row_digest,
                **availability,
            })
    assert len({r["object_occurrence_id"] for r in object_rows}) == len(object_rows)
    object_fields = [
        "object_occurrence_id", "object_kind", "source_id", "source_path",
        "source_row_number", "source_row_label", "source_row_sha256", "classification",
        "domain_chart_cover", "complete_coframe_metric", "overlap_transition_maps",
        "finite_cell_completion_data", "regularity_nondegeneracy", "causal_interface_rules",
        "topology_global_descent", "construction_sufficiency", "provenance", "P03B_gate", "ruling",
    ]
    write_tsv(OUT / "NAMED_OBJECT_ADJUDICATION.tsv", object_fields, object_rows)

    # The exact preregistered source freeze contains aggregate counts but omits
    # both detailed ledgers required to enumerate a lossless family projection.
    required_projection_sources = [
        "udt_full_local_jet_strata_p02_2026-07-27/STRATUM_LEDGER.tsv",
        "udt_full_local_jet_strata_p02_2026-07-27/P02B_CANDIDATE_LEDGER.tsv",
    ]
    projection_rows = []
    for path in required_projection_sources:
        projection_rows.append({
            "required_path": path,
            "present_on_disk": "YES" if (ROOT / path).is_file() else "NO",
            "frozen_in_P03_source_manifest": "YES" if path in by_path else "NO",
            "permitted_as_P03_input": "YES" if path in by_path else "NO",
            "ruling": "AVAILABLE_FOR_LOSSLESS_PROJECTION" if path in by_path else "BLOCKED_UNREGISTERED_SOURCE",
        })
    write_tsv(
        OUT / "P02_MOTIF_PROJECTION_AVAILABILITY.tsv",
        ["required_path", "present_on_disk", "frozen_in_P03_source_manifest", "permitted_as_P03_input", "ruling"],
        projection_rows,
    )

    completion_rows = read_tsv(ROOT / "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/COMPLETION_UNIVERSE.tsv")
    gate_rows: list[dict[str, object]] = []
    for row in completion_rows:
        cid = row["completion_id"]
        has_metric = row["concrete_metric_status"]
        gate_rows.append({
            "candidate_id": cid,
            "candidate_kind": "REGISTERED_COMPLETION_CLASS",
            "complete_metric_or_coframe": has_metric,
            "founded_phi_profile": "NO_REGISTERED_FOUNDED_DEPTH",
            "all_charts_and_overlaps": "ONLY_CONCRETE_CONTROLS_IN_FC04" if cid == "FC04_TWO_CAP_P1" else "NO",
            "completion_data": "TYPE_REGISTERED;FULL_FIELD_DATA_NOT_SUPPLIED" if cid != "FC04_TWO_CAP_P1" else "TWO_CONCRETE_S3_CONTROLS",
            "P03B_eligibility": "FAIL",
            "failure": "NO_ACTUAL_COMPLETE_REPRESENTATIVE" if cid != "FC04_TWO_CAP_P1" else "COMPLETE_CONTROLS_LACK_FOUNDED_PHI_PROFILE",
        })
    for rep in ("Q01_ROUND_S3_B19", "Q02_SQUASHED_S3_OFF_SHELL"):
        gate_rows.append({
            "candidate_id": rep,
            "candidate_kind": "CONCRETE_COMPLETE_METRIC_CONTROL",
            "complete_metric_or_coframe": "YES_CONDITIONAL_ON_SHELL" if rep.startswith("Q01") else "YES_OFF_SHELL_CONTROL",
            "founded_phi_profile": "NO",
            "all_charts_and_overlaps": "YES_S3_PRODUCT_CONTROL",
            "completion_data": "YES_FC04_TWO_CAP_P1",
            "P03B_eligibility": "FAIL",
            "failure": "ULTRASTATIC_CONTROL_HAS_NO_FOUNDED_OBSERVER_PAIR_DEPTH",
        })
    write_tsv(
        OUT / "P03B_GATE_LEDGER.tsv",
        ["candidate_id", "candidate_kind", "complete_metric_or_coframe", "founded_phi_profile", "all_charts_and_overlaps", "completion_data", "P03B_eligibility", "failure"],
        gate_rows,
    )

    p02a = json.loads((ROOT / "udt_full_local_jet_strata_p02_2026-07-27/STRATUM_CENSUS.json").read_text())
    p02b = json.loads((ROOT / "udt_full_local_jet_strata_p02_2026-07-27/P02B_CENSUS.json").read_text())
    constructive_strata = (
        p02a["stratum_classification_counts"]["CONSTRUCTIVE_BOTH"]
        + p02a["stratum_classification_counts"]["CONSTRUCTIVE_ONE"]
    )
    assert constructive_strata == 7897
    assert p02b["candidates"] == 12594
    assert all(r["P03B_eligibility"] == "FAIL" for r in gate_rows)
    census = {
        "schema": "udt-p03a-source-availability-census-1.0",
        "status": "OPEN_MISSING_GLOBAL_DEFINITION",
        "source_count": len(source_rows),
        "source_classification_counts": dict(sorted(Counter(r["classification"] for r in source_rows).items())),
        "named_object_occurrence_count": len(object_rows),
        "named_object_classification_counts": dict(sorted(Counter(r["classification"] for r in object_rows).items())),
        "named_object_kind_counts": dict(sorted(Counter(r["object_kind"] for r in object_rows).items())),
        "registered_completion_classes": 12,
        "concrete_complete_metric_controls": 2,
        "P03B_eligible_global_objects": 0,
        "P02_constructive_strata_aggregate_count": constructive_strata,
        "P02_lossless_projection_rows_generated": 0,
        "P02_lossless_projection_status": "BLOCKED_REQUIRED_DETAIL_NOT_FROZEN_IN_P03",
        "P02B_candidate_aggregate_count": p02b["candidates"],
        "gate_failures": [
            "NO_COMPLETE_FOUNDED_(g,phi)_FINITE_CELL_OBJECT",
            "ONLY_COMPLETE_METRIC_CONTROLS_ARE_ULTRASTATIC_AND_LACK_FOUNDED_DEPTH",
            "DETAILED_P02_PROJECTION_LEDGERS_NOT_FROZEN_IN_P03_SOURCE_UNIVERSE",
            "CROSS_SPLICING_WRL_WITH_S3_CONTROLS_FORBIDDEN",
        ],
        "maximum_conclusion": "OPEN_MISSING_GLOBAL_DEFINITION",
    }
    (OUT / "P03A_CENSUS.json").write_text(json.dumps(census, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
