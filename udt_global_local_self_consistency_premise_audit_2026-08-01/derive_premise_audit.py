#!/usr/bin/env python3
"""Deterministic premise-level audit of global/local self-consistency."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (PKG / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def anchor(anchor_id: str, path: str, authority: str, role: str, ruling: str) -> dict[str, str]:
    full = ROOT / path
    if not full.is_file():
        raise RuntimeError(f"missing anchor {path}")
    return {
        "anchor_id": anchor_id,
        "path": path,
        "sha256": sha256(full),
        "authority": authority,
        "role": role,
        "ruling": ruling,
    }


def main() -> None:
    inventory = read_tsv(PKG / "SOURCE_INVENTORY.tsv")
    premises = read_tsv(PKG / "PREMISE_LEDGER.tsv")
    candidates = read_tsv(PKG / "INTERPRETATION_CANDIDATES.tsv")
    return_candidates = read_tsv(PKG / "RETURN_TYPE_CANDIDATES.tsv")
    if (len(inventory), len(premises), len(candidates), len(return_candidates)) != (1424, 18, 12, 8):
        raise RuntimeError("preregistered census mismatch")
    for row in inventory:
        path = ROOT / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            raise RuntimeError(f"frozen source changed: {row['path']}")

    anchors = [
        anchor("A01", "CURRENT_SCIENTIFIC_PREMISES.tsv", "CURRENT_CONTROL", "premise status", "bootstrap is WORKING on-shell admissibility; complete action/source/boundary/mass open"),
        anchor("A02", "CURRENT_SCIENTIFIC_PREMISES.md", "CURRENT_CONTROL", "term separation", "metric ontology and current correction layers do not promote dynamics or global completion"),
        anchor("A03", "udt_global_local_relational_closure_audit_2026-07-25/AUDIT_REPORT.md", "POST_FIREWALL_VERIFIED_EVIDENCE", "relational architecture", "coherent architecture; joined native closure and downstream action not derived"),
        anchor("A04", "udt_global_local_relational_closure_audit_2026-07-25/DEPENDENCY_ARCHITECTURE.tsv", "POST_FIREWALL_VERIFIED_EVIDENCE", "dependency type", "native response and same-solution fixed point are open"),
        anchor("A05", "udt_bootstrap_to_local_response_map_audit_2026-07-25/AUDIT_REPORT.md", "POST_FIREWALL_VERIFIED_EVIDENCE", "two-arrow architecture", "two-way owner hypothesis is coherent; neither arrow, derivative, or objective is selected"),
        anchor("A06", "udt_bootstrap_to_local_response_map_audit_2026-07-25/GLOBAL_LOCAL_CLOSURE_LEDGER.tsv", "POST_FIREWALL_VERIFIED_EVIDENCE", "arrow ledger", "both arrows and their fixed point remain working or open"),
        anchor("A07", "udt_native_global_observable_closure_census_2026-07-26/AUDIT_REPORT.md", "POST_FIREWALL_VERIFIED_EVIDENCE", "observable census", "metric supplies exact primitives and partial variations, not a complete state vector or closure section"),
        anchor("A08", "udt_native_global_observable_closure_census_2026-07-26/ASSEMBLY_BLOCKER_LEDGER.tsv", "POST_FIREWALL_VERIFIED_EVIDENCE", "assembly blockers", "complete R, complete A, boundary domain, and native component selection are independently open"),
        anchor("A09", "udt_stability_foundations_audit_2026-08-01/BOOTSTRAP_FIXED_POINT_SCHEMA.tsv", "POST_FIREWALL_VERIFIED_EVIDENCE", "fixed-point schema", "B=R(u) is type-only; A, R, fixed-point existence, uniqueness, derivative, and stability remain open"),
        anchor("A10", "udt_joint_realization_closure_audit_2026-08-01/AUDIT_REPORT.md", "POST_FIREWALL_VERIFIED_EVIDENCE", "joint realization", "formal compatibility does not establish one realized on-shell configuration"),
        anchor("A11", "udt_jr_cert_native_derivation_2026-08-01/AUDIT_REPORT.md", "IMMEDIATE_VERIFIED_PARENT", "equation ownership", "identities reconstruct supplied geometry; zero of eight native equation routes pass"),
        anchor("A12", "udt_bootstrap_closure_ownership_audit_2026-08-01/AUDIT_REPORT.md", "IMMEDIATE_VERIFIED_PARENT", "closure ownership", "partial R exists; graph R does not select X; nonidentity A remains open"),
        anchor("A13", "udt_whole_configuration_reciprocity_audit_2026-08-01/AUDIT_REPORT.md", "IMMEDIATE_VERIFIED_PARENT", "Reciprocity reach", "future law must be natural; Reciprocity does not manufacture a return"),
        anchor("A14", "udt_mirror_canon_provenance_audit_2026-07-30/PROVENANCE_REPORT.md", "POST_FIREWALL_CONTROLLING_PROVENANCE", "finite-cell scope", "finiteness and mirror closure are split; closure remains an owner-ratified working proposal"),
        anchor("A15", "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "POST_FIREWALL_CONTROLLING_ADJUDICATION", "complete physics ceiling", "complete action, source, boundary charge, and mass remain open"),
        anchor("A16", "LIVE.md", "CURRENT_NAVIGATION_AT_BASE", "bootstrap posture", "bootstrap is a lens, never a filter; no response law may be assumed"),
    ]
    write_tsv("SOURCE_AUTHORITY_LEDGER.tsv", list(anchors[0]), anchors)

    terms = [
        {"term_id": "D01", "term": "complete_metric_configuration", "definition": "all declared fields charts sectors joins boundaries and moduli for one supplied branch are specified", "does_not_mean": "physically realized unique or on shell"},
        {"term_id": "D02", "term": "forward_readout", "definition": "a map or relation assigning derived local or global data to a supplied configuration", "does_not_mean": "feedback selection or dynamics"},
        {"term_id": "D03", "term": "admissibility", "definition": "membership in a stated nontrivial subset or relation", "does_not_mean": "existence uniqueness persistence or evolution"},
        {"term_id": "D04", "term": "existence", "definition": "at least one member satisfies a stated relation", "does_not_mean": "which member or why it is realized"},
        {"term_id": "D05", "term": "selection", "definition": "a rule distinguishes a proper subset orbit or branch", "does_not_mean": "a readout graph containing every supplied input"},
        {"term_id": "D06", "term": "return_operation", "definition": "a nonidentity relation or map that makes global data constrain complete configurations", "does_not_mean": "the forward recomputation map"},
        {"term_id": "D07", "term": "fixed_point", "definition": "a supplied return and forward map agree under a defined equality or zero", "does_not_mean": "the assertion that agreement ought to occur"},
        {"term_id": "D08", "term": "bootstrap_weak", "definition": "realized configurations are globally and locally mutually admissible", "does_not_mean": "an operational equation"},
        {"term_id": "D09", "term": "bootstrap_operational", "definition": "an observer-natural relation on independently varied complete-configuration and global-data arguments with nontrivial dependence on both and a nonempty proper intersection with Graph(R)", "does_not_mean": "a unique action optimizer solution or theorem of deductive independence"},
        {"term_id": "D10", "term": "metric_is_theory", "definition": "physical structures claimed as UDT must trace to the UDT metric and stated premises", "does_not_mean": "every needed physical law follows from the bare phrase"},
    ]
    write_tsv("TERM_DEFINITION_LEDGER.tsv", list(terms[0]), terms)

    outcomes = [
        {"candidate_id": "I01", "status": "NOT_DERIVED_ONTOLOGY_IS_TRACE_RULE", "basis": "A01;A02;A11;D10", "ruling": "metric ownership rejects imports but supplies no nonidentity consistency relation"},
        {"candidate_id": "I02", "status": "COMPLETE_SPECIFICATION_NOT_PHYSICAL_SELECTION", "basis": "A03;A07;A10;D01-D05", "ruling": "a complete problem or field record can have zero one or many realized solutions"},
        {"candidate_id": "I03", "status": "DERIVED_PARTIAL_READOUT_NO_SELECTED_SECTION", "basis": "A05-A08;A12;finite restriction control", "ruling": "same readout admits multiple sections and return relations"},
        {"candidate_id": "I04", "status": "GRAPH_IS_NONSELECTION_EXACT", "basis": "A05;A12;graph control", "ruling": "the readout graph projects onto every supplied configuration"},
        {"candidate_id": "I05", "status": "FINITE_DOMAIN_NOT_BOUNDARY_OR_RETURN", "basis": "A08;A14;finite predicate control", "ruling": "finiteness supplies no preferred admissibility predicate or differentiable boundary law"},
        {"candidate_id": "I06", "status": "NATURALITY_GATE_NOT_LAW_GENERATOR", "basis": "A13;observer-orbit relation control", "ruling": "Reciprocity requires observer-saturated closure but permits inequivalent closures"},
        {"candidate_id": "I07", "status": "PAIRING_SCOPED_NO_WHOLE_RELATION", "basis": "A13;parent dual-pair control", "ruling": "the founded clock-ruler pairing supplies neither full response pairing nor selected level"},
        {"candidate_id": "I08", "status": "OPEN_NO_SELECTED_VARIATIONAL_RULE", "basis": "A03;A11;A15", "ruling": "action variation and boundary completion remain possible stronger realizations only"},
        {"candidate_id": "I09", "status": "CONDITIONAL_STABILITY_IS_DOWNSTREAM", "basis": "A09;A10;A15", "ruling": "persistence needs a supplied solution law topology or update and cannot create them"},
        {"candidate_id": "I10", "status": "CALIBRATION_OR_DISCRIMINATION_NOT_DERIVATION", "basis": "A01;A05;A07", "ruling": "observed anchors can calibrate or reject candidate closures but do not define one"},
        {"candidate_id": "I11", "status": "WORKING_SEMANTIC_POSIT_OPERATIONALLY_INCOMPLETE", "basis": "A01;A05;A06;A09;D08-D09", "ruling": "mutual tuning is coherent owner-guided architecture; operation requires a relation on independent X and O with both-argument dependence whose membership is absent"},
        {"candidate_id": "I12", "status": "NO_OTHER_COMPLETE_ROUTE_IN_FROZEN_UNIVERSE", "basis": "A01-A16;1424-source census", "ruling": "no current source passes all seven preregistered derivation gates"},
    ]
    write_tsv("INTERPRETATION_OUTCOMES.tsv", list(outcomes[0]), outcomes)

    return_outcomes = [
        {"type_id": "T01", "status": "NOT_DERIVED_MULTIPLE_SECTIONS", "relative_strength": "STRONGER_THAN_RELATION", "ruling": "the forward readout does not select a right inverse"},
        {"type_id": "T02", "status": "NOT_DERIVED_READOUT_NONINJECTIVE", "relative_strength": "STRONGER_THAN_RELATION", "ruling": "current partial readouts do not reconstruct a unique complete configuration"},
        {"type_id": "T03", "status": "OPEN_STRONGER_REALIZATION", "relative_strength": "STRONGER_THAN_RELATION", "ruling": "fixed-point operator requires a selected endomorphism and equality"},
        {"type_id": "T04", "status": "OPEN_REQUIRES_ACTION_AND_BOUNDARY", "relative_strength": "STRONGER_THAN_RELATION", "ruling": "no native variational Euler map is selected"},
        {"type_id": "T05", "status": "OPEN_REQUIRES_BOUNDARY_EXTENSION_LAW", "relative_strength": "STRONGER_THAN_RELATION", "ruling": "finite-cell types do not choose bulk extension"},
        {"type_id": "T06", "status": "OPEN_REQUIRES_OBSERVABLE_RESPONSE_PAIRING", "relative_strength": "STRONGER_THAN_RELATION", "ruling": "global geometric vocabulary does not select a physical response"},
        {"type_id": "T07", "status": "MINIMUM_ADDITIONAL_LOGICAL_TYPE_NOT_DERIVED", "relative_strength": "MINIMAL_OPERATIONAL_MUTUAL_DETERMINATION_TYPE", "ruling": "an observer-natural relation on independent X and O with nontrivial dependence on both and nonempty proper Graph(R) intersection expresses mutual admissibility without assuming action dynamics or uniqueness"},
        {"type_id": "T08", "status": "OPEN_STRONGER_SELECTION_SEMANTICS", "relative_strength": "STRONGER_THAN_RELATION", "ruling": "set-valued probability measure or ranking requires further physical semantics"},
    ]
    write_tsv("RETURN_TYPE_OUTCOMES.tsv", list(return_outcomes[0]), return_outcomes)

    minimum_levels = [
        {"level_id": "M01", "level": "SEMANTIC_WORKING_HYPOTHESIS", "minimum_object": "realized whole and local data are mutually admissible", "status": "CURRENT_WORKING_LANGUAGE", "does_not_supply": "membership test or calculation"},
        {"level_id": "M02", "level": "NONTRIVIAL_ADMISSIBILITY_ONLY", "minimum_object": "nonconstant observer-invariant predicate on X equivalently a nonempty proper observer-saturated subrelation of Graph(R)", "status": "TYPE_IDENTIFIED_INSUFFICIENT_FOR_MUTUAL_DETERMINATION", "does_not_supply": "evidence that global readout O is load-bearing"},
        {"level_id": "M03", "level": "OPERATIONAL_MUTUAL_DETERMINATION_TYPE", "minimum_object": "observer-natural relation on independent X times O with nontrivial dependence on both and nonempty proper intersection with Graph(R)", "status": "MINIMUM_EXTRA_POSIT_TYPE_NOT_DERIVED_OR_ADOPTED_HERE", "does_not_supply": "exact metric-native membership rule or proof no future same-premise theorem exists"},
        {"level_id": "M04", "level": "OPERATIONAL_MEMBERSHIP_RULE", "minimum_object": "explicit metric-native definition of the M03 relation", "status": "OPEN", "does_not_supply": "differentiability action dynamics uniqueness or stability"},
        {"level_id": "M05", "level": "DIFFERENTIAL_RESPONSE", "minimum_object": "differentiable residual or response one-form with pairing and complete variation domain", "status": "OPEN_STRONGER_REQUIRED_FOR_LINEAR_RESPONSE_OR_ACTION_TEST", "does_not_supply": "global variational potential"},
        {"level_id": "M06", "level": "VARIATIONAL_REALIZATION", "minimum_object": "action plus boundary/corner completion", "status": "OPEN_STRONGER_OPTION", "does_not_supply": "realized branch or persistence"},
        {"level_id": "M07", "level": "DYNAMICAL_OR_STABILITY_REALIZATION", "minimum_object": "evolution or update law topology/norm and persistence test", "status": "OPEN_DOWNSTREAM", "does_not_supply": "premise derivation"},
    ]
    write_tsv("MINIMUM_LEVEL_LEDGER.tsv", list(minimum_levels[0]), minimum_levels)

    # Exact finite logic control.  The complete states G have a two-valued
    # readout R.  Observer change S acts inside each readout fiber.
    global_states = tuple(range(4))
    local_states = (0, 1)
    readout = {0: 0, 1: 0, 2: 1, 3: 1}
    observer = {0: 1, 1: 0, 2: 3, 3: 2}
    graph = {(g, readout[g]) for g in global_states}
    assert all(readout[observer[g]] == readout[g] for g in global_states)

    sections = []
    for low in (0, 1):
        for high in (2, 3):
            section = {0: low, 1: high}
            assert all(readout[section[value]] == value for value in local_states)
            sections.append(section)
    section_images = {tuple(sorted(section.values())) for section in sections}

    closure_low = {(g, readout[g]) for g in (0, 1)}
    closure_high = {(g, readout[g]) for g in (2, 3)}
    proper_saturated = [closure_low, closure_high]
    for closure in proper_saturated:
        assert closure < graph
        assert all((observer[g], value) in closure for g, value in closure)
    assert closure_low.isdisjoint(closure_high)

    # As subsets of Graph(R), the two relations above are extensionally only
    # predicates on X.  To express mutual determination at the type level,
    # treat X and O as independent before imposing O=R(X), and require both
    # arguments to affect relation membership.
    cartesian = {(g, value) for g in global_states for value in local_states}

    def depends_on_both(relation: set[tuple[int, int]]) -> tuple[bool, bool]:
        depends_x = any(
            ((g1, value) in relation) != ((g2, value) in relation)
            for value in local_states
            for g1 in global_states
            for g2 in global_states
        )
        depends_o = any(
            ((g, value1) in relation) != ((g, value2) in relation)
            for g in global_states
            for value1 in local_states
            for value2 in local_states
        )
        return depends_x, depends_o

    operational_low = {(0, 0), (1, 0)}
    operational_high = {(2, 1), (3, 1)}
    operational_relations = [operational_low, operational_high]
    operational_dependence = [depends_on_both(relation) for relation in operational_relations]
    assert all(x_dep and o_dep for x_dep, o_dep in operational_dependence)
    assert all(relation < cartesian for relation in operational_relations)
    assert all(relation & graph for relation in operational_relations)
    assert all((relation & graph) < graph for relation in operational_relations)
    assert all(
        (observer[g], value) in relation
        for relation in operational_relations
        for g, value in relation
    )

    # Reciprocity alone does not guarantee a proper saturated relation.  A
    # transitive action has one orbit and hence only empty/full saturated sets.
    transitive_observer_orbit_count = 1
    transitive_saturated_relation_count = 2 ** transitive_observer_orbit_count
    transitive_nonempty_proper_saturated_count = transitive_saturated_relation_count - 2

    fixed_sets = []
    for section in sections:
        fixed = tuple(g for g in global_states if section[readout[g]] == g)
        fixed_sets.append(fixed)
    assert set(fixed_sets) == section_images

    finite_admissibility_predicate_count = 2 ** len(global_states)
    observer_orbits = ({0, 1}, {2, 3})
    observer_saturated_relation_count = 2 ** len(observer_orbits)
    nonempty_proper_saturated_count = observer_saturated_relation_count - 2

    algebra = {
        "scope": "finite implication controls only; no candidate UDT closure law",
        "complete_state_count": len(global_states),
        "readout_state_count": len(local_states),
        "readout_graph_size": len(graph),
        "readout_graph_configuration_survivors": len({g for g, _ in graph}),
        "readout_fiber_sizes": {"0": 2, "1": 2},
        "readout_is_surjective": set(readout.values()) == set(local_states),
        "readout_is_injective": len(set(readout.values())) == len(global_states),
        "right_inverse_section_count": len(sections),
        "distinct_section_image_count": len(section_images),
        "section_fixed_set_sizes": sorted(len(fixed) for fixed in fixed_sets),
        "finite_admissibility_predicate_count": finite_admissibility_predicate_count,
        "observer_orbit_count": len(observer_orbits),
        "observer_saturated_relation_count": observer_saturated_relation_count,
        "nonempty_proper_observer_saturated_relation_count": nonempty_proper_saturated_count,
        "proper_saturated_relation_sizes": [len(closure) for closure in proper_saturated],
        "proper_saturated_relations_disjoint": closure_low.isdisjoint(closure_high),
        "graph_subrelation_equivalent_to_X_predicate": True,
        "operational_independent_product_size": len(cartesian),
        "operational_relation_count_tested": len(operational_relations),
        "operational_relations_depend_on_X": all(value[0] for value in operational_dependence),
        "operational_relations_depend_on_O": all(value[1] for value in operational_dependence),
        "operational_graph_intersection_sizes": [len(relation & graph) for relation in operational_relations],
        "transitive_control_observer_orbit_count": transitive_observer_orbit_count,
        "transitive_control_nonempty_proper_saturated_relation_count": transitive_nonempty_proper_saturated_count,
        "conclusions": [
            "a complete forward readout graph retains every supplied configuration",
            "the same readout admits multiple sections and fixed sets",
            "finiteness does not select an admissibility predicate",
            "the chosen two-orbit observer action permits multiple disjoint proper saturated graph subrelations but does not model the complete UDT observer action",
            "a subrelation of Graph(R) is only an X-admissibility predicate and does not make O load-bearing",
            "mutual determination minimally requires an observer-natural relation on independent X and O with nontrivial dependence on both before imposing O=R(X)",
            "the current frozen record supplies the type skeleton but no membership rule",
        ],
    }
    (PKG / "ALGEBRA_RESULT.json").write_text(json.dumps(algebra, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    countermodels = [
        {"countermodel_id": "C01", "tempting_implication": "complete readout implies inverse", "exact_witness": "R fibers each have size 2; four right inverses exist", "ruling": "REFUTES_IMPLICATION"},
        {"countermodel_id": "C02", "tempting_implication": "readout graph selects X", "exact_witness": "Graph(R) projects onto all four complete states", "ruling": "REFUTES_IMPLICATION"},
        {"countermodel_id": "C03", "tempting_implication": "finite domain selects admissibility", "exact_witness": "four-state domain admits 16 Boolean predicates", "ruling": "REFUTES_IMPLICATION"},
        {"countermodel_id": "C04", "tempting_implication": "Reciprocity selects one closure", "exact_witness": "two disjoint nonempty proper observer-saturated subrelations", "ruling": "REFUTES_IMPLICATION"},
        {"countermodel_id": "C05", "tempting_implication": "existence selects realized branch", "exact_witness": "both disjoint proper closures are nonempty", "ruling": "REFUTES_IMPLICATION"},
        {"countermodel_id": "C06", "tempting_implication": "section existence selects fixed-point law", "exact_witness": "four sections yield four distinct two-state fixed sets", "ruling": "REFUTES_IMPLICATION"},
        {"countermodel_id": "C07", "tempting_implication": "Reciprocity guarantees a nonempty proper saturated closure", "exact_witness": "a transitive observer action has one orbit and zero nonempty proper saturated subsets", "ruling": "REFUTES_IMPLICATION_AND_SCOPES_CHOSEN_TWO_ORBIT_CONTROL"},
    ]
    write_tsv("COUNTERMODEL_LEDGER.tsv", list(countermodels[0]), countermodels)

    implications = [
        {"implication_id": "L01", "from_object": "metric_is_theory", "to_object": "native_provenance_requirement", "status": "DERIVED_METHOD_RULE", "reason": "all affirmative UDT physics must trace to the metric and stated premises"},
        {"implication_id": "L02", "from_object": "metric_is_theory", "to_object": "global_local_consistency_relation", "status": "NONEDGE_NOT_DERIVED", "reason": "provenance rule supplies no relation formula or subset"},
        {"implication_id": "L03", "from_object": "complete_metric_configuration", "to_object": "well_typed_full_domain", "status": "DERIVED_REQUIREMENT", "reason": "completeness requires all active data and joins to be represented"},
        {"implication_id": "L04", "from_object": "complete_metric_configuration", "to_object": "physical_selection", "status": "NONEDGE_NOT_DERIVED", "reason": "specification and solution selection are different quantifiers"},
        {"implication_id": "L05", "from_object": "forward_readout_R", "to_object": "readout_graph", "status": "DERIVED_PARTIAL", "reason": "each supplied configuration has its derived scoped outputs"},
        {"implication_id": "L06", "from_object": "readout_graph", "to_object": "proper_consistency_relation", "status": "NONEDGE_EXACT_COUNTERMODEL", "reason": "graph projects onto every input"},
        {"implication_id": "L07", "from_object": "finite_domain", "to_object": "boundary_or_admissibility_law", "status": "NONEDGE_NOT_DERIVED", "reason": "finiteness supplies domain type but no predicate or differentiable boundary functional"},
        {"implication_id": "L08", "from_object": "observer_reciprocity", "to_object": "observer_saturation_of_supplied_relation", "status": "DERIVED_REQUIREMENT_GIVEN_RELATION", "reason": "physical admissibility cannot favor an equivalent observer description"},
        {"implication_id": "L09", "from_object": "observer_reciprocity", "to_object": "unique_proper_relation", "status": "NONEDGE_EXACT_COUNTERMODEL", "reason": "multiple disjoint saturated relations survive"},
        {"implication_id": "L10", "from_object": "weak_bootstrap_language", "to_object": "minimum_relation_type", "status": "TYPE_SHARPENED", "reason": "mutual determination requires independent X and O arguments with nontrivial dependence on both before graph closure"},
        {"implication_id": "L11", "from_object": "minimum_relation_type", "to_object": "relation_definition", "status": "OPEN_NOT_DERIVED_IN_FROZEN_RECORD", "reason": "current source record does not choose membership"},
        {"implication_id": "L12", "from_object": "proper_relation", "to_object": "action_dynamics_uniqueness", "status": "NONEDGE_STRONGER_STRUCTURE", "reason": "admissibility need not be variational dynamic or unique"},
    ]
    write_tsv("IMPLICATION_LEDGER.tsv", list(implications[0]), implications)

    status = [
        {"claim": "metric_is_theory_reach", "status": "DERIVED_NATIVE_PROVENANCE_RULE_ONLY", "basis": "I01;L01-L02", "remaining": "an actual metric-native selection relation"},
        {"claim": "complete_metric_reach", "status": "DERIVED_COMPLETE_SPECIFICATION_REQUIREMENT_NOT_SELECTION", "basis": "I02;L03-L04", "remaining": "existence admissibility selection and persistence"},
        {"claim": "forward_readout", "status": "DERIVED_PARTIAL_GRAPH_NONSELECTION", "basis": "I03-I04;C01-C02", "remaining": "complete R and observer-natural independent-X/O operational relation"},
        {"claim": "finite_cell_reach", "status": "WORKING_DOMAIN_STRUCTURE_NOT_RETURN", "basis": "I05;C03;A14", "remaining": "selected completion and differentiable boundary relation"},
        {"claim": "reciprocity_reach", "status": "DERIVED_NATURALITY_OF_SUPPLIED_RELATION_NOT_RELATION", "basis": "I06-I07;C04;L08-L09", "remaining": "membership law and complete action on all data"},
        {"claim": "bootstrap_current", "status": "WORKING_COHERENT_ARCHITECTURE_NOT_DERIVED_OPERATION", "basis": "I11;A03-A09", "remaining": "independent-X/O relation definition complete domain and readout"},
        {"claim": "minimum_extra_premise_type", "status": "OBSERVER_NATURAL_RELATION_ON_INDEPENDENT_X_AND_O_WITH_NONTRIVIAL_BOTH_ARGUMENT_DEPENDENCE", "basis": "T07;M02-M04;L10-L12;operational relation control", "remaining": "nonempty proper graph intersection; Charles adoption or future metric derivation; exact membership rule"},
        {"claim": "action_or_fixed_point_requirement", "status": "NOT_MINIMALLY_REQUIRED_STRONGER_REALIZATIONS", "basis": "T03-T06;T08", "remaining": "may be tested only after relation ownership"},
        {"claim": "overall", "status": "BOOTSTRAP_IS_DISTINCT_POSIT", "basis": "current frozen-record epistemic routing;1424-source audit;I01-I12;T01-T08;C01-C07", "remaining": "not adopted; not an independence theorem; future same-premise metric theorem remains possible"},
    ]
    write_tsv("STATUS_LEDGER.tsv", list(status[0]), status)

    result = {
        "outcome": "BOOTSTRAP_IS_DISTINCT_POSIT",
        "source_paths_verified": len(inventory),
        "source_anchors": len(anchors),
        "premises": len(premises),
        "interpretations": len(outcomes),
        "interpretations_passing_derived_mutual_determination": 0,
        "return_types": len(return_outcomes),
        "minimum_extra_logical_type": "OBSERVER_NATURAL_RELATION_ON_INDEPENDENT_X_TIMES_O_WITH_NONTRIVIAL_DEPENDENCE_ON_BOTH_AND_NONEMPTY_PROPER_GRAPH_INTERSECTION",
        "minimum_type_derived": False,
        "frozen_record_derivation_found": False,
        "deductive_independence_proved": False,
        "future_same_premise_metric_theorem_excluded": False,
        "bootstrap_adopted_by_audit": False,
        "candidate_formula_constructed": False,
        "solve_authorized": False,
        "gpu_used": False,
    }
    (PKG / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "PASS global/local premise audit: sources=1424 interpretations=12 derived_pass=0 "
        "minimum_type=independent_X_O_observer_natural_relation"
    )


if __name__ == "__main__":
    main()
