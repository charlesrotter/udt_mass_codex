#!/usr/bin/env python3
"""Deterministic source/ontology adjudication for the seven inherited F labels."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str, base: Path = PKG) -> list[dict[str, str]]:
    with (base / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, records: list[dict[str, object]]) -> None:
    with (PKG / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def require(path: str, needles: list[str]) -> None:
    text = (ROOT / path).read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise RuntimeError(f"missing source anchor in {path}: {needle}")


def lineage(path: str) -> tuple[str, str, str, str]:
    first = subprocess.check_output(
        ["git", "log", "--follow", "--diff-filter=A", "--format=%H%x09%aI", "--", path],
        cwd=ROOT,
        text=True,
    ).splitlines()[-1].split("\t")
    last = subprocess.check_output(
        ["git", "log", "-1", "--format=%H%x09%aI", "--", path], cwd=ROOT, text=True
    ).strip().split("\t")
    return first[0], first[1], last[0], last[1]


def main() -> None:
    anchors = [
        ("A01", "udt_p4_stability_slice_2026-07-30/AUDIT_REPORT.md", "P4 parent response/census", "S-i S-ii controls and empty scopes share one conditional P4 program"),
        ("A02", "udt_p4_stability_slice_2026-07-30/STABILITY_LEDGER.tsv", "P4 mechanical branches", "F01 F02 F03 and F06 roles are rows/strata of one package"),
        ("A03", "udt_p4_stability_slice_2026-07-30/EXACT_DERIVATION.md", "P4 fields domains and operators", "conditional stationary response and tangent scopes"),
        ("A04", "udt_p4_period_gate_2026-07-30/AUDIT_REPORT.md", "completion/period structure", "rings constrain P4 branches but supply no stability response"),
        ("A05", "udt_p4_period_gate_2026-07-30/PERIOD_LEDGER.tsv", "completion branch matrix", "cyclic acyclic quotient mass and germ rows"),
        ("A06", "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "Hopfion object identity", "full 3D conditional S2 L2+L4 finite-box object"),
        ("A07", "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv", "Hopfion status mechanics", "carrier physical boundary and time remain open"),
        ("A08", "udt_stability_foundations_audit_2026-08-01/AUDIT_REPORT.md", "stability ontology separation", "P4 and Hopfion are distinct conditional streams"),
        ("A09", "udt_stability_foundations_audit_2026-08-01/FIXED_REALIZATION_GATE.tsv", "realization gates", "formal modules do not supply one realized object"),
        ("A10", "udt_joint_realization_closure_audit_2026-08-01/AUDIT_REPORT.md", "joint-realization ruling", "formal P4 modules remain unrealized jointly"),
        ("A11", "udt_joint_realization_closure_audit_2026-08-01/JOINT_GATE_MATRIX.tsv", "joint gate mechanics", "field equation boundary tangent and common premise gates"),
        ("A12", "udt_stability_hypothesis_cross_family_atlas_2026-08-01/FAMILY_ATLAS.tsv", "inherited operational labels", "seven evidence categories to be re-audited"),
        ("A13", "udt_stability_derivation_closure_sweep_2026-08-01/OBJECT_STATUS_LEDGER.tsv", "corrected upstream objects", "six objects underdetermined and no readiness promotion"),
        ("A14", "CURRENT_SCIENTIFIC_PREMISES.tsv", "premise controller", "carrier action boundary time bootstrap and mass statuses"),
        ("A15", "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "action/source ceiling", "complete native action source boundary charge and mass open"),
        ("A16", "udt_p4_bookkeeping_forcing_2026-07-29/EXACT_DERIVATION.md", "P4 census-fork domain relation", "constant-section pullback versus field-domain pointwise variation; fork open"),
        ("A17", "udt_p4_routeD_field_registration_2026-07-29/AUDIT_REPORT.md", "P4 field-census registration", "both branches register at class grade; field response typed not exhausted; no fork selected"),
        ("A18", "NEGATIVES_REGISTRY.md", "historical negative registry", "premise-scoped historical negatives and current-registry crosswalk"),
    ]
    require(anchors[0][1], ["P4 stability slice", "S-i", "S-ii"])
    require(anchors[2][1], ["Standing scope stamps", "massless", "N=2 wall layer"])
    require(anchors[3][1], ["THE SECTOR MAP", "NO POSTURE SELECTION"])
    require(anchors[5][1], ["FULL_3D_HOPF_CAPABLE", "CARRIER_CONDITIONAL_HOPF_SECTOR_AVAILABLE"])
    require(anchors[7][1], ["CONDITIONAL_STABILITY_ONLY", "Realization join", "Persistence join"])
    require(anchors[9][1], ["FORMAL_COMPATIBILITY_ONLY_COMMON_REALIZATION_OPEN", "JR_CERT_NATIVE"])
    require(anchors[15][1], ["PULLBACK of the field-fork one-form", "Census-fork verdict: OPEN"])
    require(anchors[16][1], ["Both census branches now stand on registered class", "response space is defined + typed, NOT exhausted"])
    require(anchors[17][1], ["NEGATIVES REGISTRY", "CONDITIONS-CHANGED"])
    source_inventory = {row["path"] for row in rows("EFFECTIVE_SOURCE_INVENTORY.tsv")}
    authority_rows = []
    for anchor_id, path, role, ruling in anchors:
        if path not in source_inventory:
            raise RuntimeError(f"authority outside freeze: {path}")
        first_commit, first_date, last_commit, last_date = lineage(path)
        authority_rows.append({
            "anchor_id": anchor_id,
            "path": path,
            "sha256": sha256(ROOT / path),
            "first_commit": first_commit,
            "first_date": first_date,
            "last_commit": last_commit,
            "last_date": last_date,
            "role": role,
            "ruling": ruling,
        })
    write_tsv("SOURCE_AUTHORITY_LEDGER.tsv", authority_rows)

    family_rows = [
        {"family_id": "F01", "primary_ontology": "CONDITIONAL_REALIZED_SOLUTION_FAMILY", "parent_object": "P4_CONSTANTS_CENSUS_CONDITIONAL_DOMAIN", "realization_status": "CONDITIONAL_REDUCED_MASSIVE_WITNESS", "independence_status": "CENSUS_FORK_OPEN_NO_COMMON_SOLUTION_SET", "source_basis": "A01-A03;A16-A17", "exact_ruling": "S-i constants-census stationary family under integrated moduli rows and branch premises", "maximum_claim": "conditional P4 census family; not native or a physical species"},
        {"family_id": "F02", "primary_ontology": "CONDITIONAL_REALIZED_SOLUTION_FAMILY", "parent_object": "P4_FIELDS_CENSUS_CONDITIONAL_DOMAIN", "realization_status": "CONDITIONAL_LANDING_FAMILY_TYPED_NOT_EXHAUSTED", "independence_status": "CENSUS_FORK_OPEN_NO_COMMON_SOLUTION_SET", "source_basis": "A01-A03;A16-A17", "exact_ruling": "S-ii fields-census P1-4D landing under pointwise/live-modulus rows", "maximum_claim": "conditional P4 census family at registered class grade; not native or a physical species"},
        {"family_id": "F03", "primary_ontology": "CONTROL_STRATUM", "parent_object": "P4_CONDITIONAL_RESPONSE_PROGRAM", "realization_status": "UNION_OF_EXACT_MASSLESS_CONTROL_MEMBERS", "independence_status": "CONTROL_UNION_NOT_CANDIDATE_FAMILY", "source_basis": "A01-A03;A16-A17", "exact_ruling": "E0=0 constants and triad-locked PSD-degenerate controls validate separate response branches", "maximum_claim": "union of control/limiting components only; no whole-label containment theorem"},
        {"family_id": "F04", "primary_ontology": "CONDITIONAL_REALIZED_SOLUTION_FAMILY", "parent_object": "ROUND_S2_L2_PLUS_L4_FINITE_BOX_MODEL", "realization_status": "OBSERVED_STATIC_FINITE_BOX_CARRIER_CONDITIONAL", "independence_status": "OBJECT_INEQUIVALENT_TO_P4_NO_NATIVE_JOIN", "source_basis": "A06-A08;A14-A15", "exact_ruling": "full-3D Hopf-capable conditional model with banked Q-near-1 configuration", "maximum_claim": "conditional model family; carrier/action/boundary/time not native"},
        {"family_id": "F05", "primary_ontology": "STRUCTURAL_COMPLETION_CLASS", "parent_object": "P4_COMPLETION_AND_PERIOD_OPERATOR", "realization_status": "MASSLESS_RING_WITNESS_STRUCTURAL_ONLY", "independence_status": "CROSS_CUTTING_CONSTRAINT_NOT_RESPONSE_FAMILY", "source_basis": "A04-A05;A13", "exact_ruling": "cyclic/acyclic/quotient completion and real-period classifier across P4 branches", "maximum_claim": "completion/closure taxonomy; not a stability-testable family"},
        {"family_id": "F06", "primary_ontology": "EXACT_EMPTY_SCOPE", "parent_object": "P4_MULTIPLE_REGISTERED_NEGATIVE_SCOPES", "realization_status": "UNION_EMPTY_IN_REGISTERED_MASSIVE_SCOPES", "independence_status": "EMPTY_SCOPE_UNION_NOT_FAMILY", "source_basis": "A01-A05;A18", "exact_ruling": "union of massive cyclic-N1 and double-crease premise scopes eliminated by different closure legs", "maximum_claim": "union of scoped nonexistence controls; no whole-label containment or global nonexistence"},
        {"family_id": "F07", "primary_ontology": "FORMAL_MODULE_CLASS", "parent_object": "P4_STATIC_TIME_ANGULAR_FORMAL_ASSEMBLY", "realization_status": "FORMAL_ONLY_COMMON_REALIZATION_OPEN", "independence_status": "MODULE_CLASS_NOT_SOLUTION_SET", "source_basis": "A08-A11;A13", "exact_ruling": "static/time/angular restriction modules without one common nonzero on-shell field", "maximum_claim": "formal compatibility and missing-join locator only"},
    ]
    write_tsv("FAMILY_ONTOLOGY_LEDGER.tsv", family_rows)

    axis_findings = {
        "F01": [
            ("DEFINED_CONDITIONAL", "P4 S-i stationary quadratic fields/moduli; massive constants census"),
            ("CONDITIONAL_REDUCED", "P4 reduced/joint second variation; no native complete action"),
            ("BOUNDED_SECTOR", "jet<=2 cells and mixed crease-glue/open branches"),
            ("SUPPLIED_AND_OPEN", "posture/parity supplied; higher wall-germ curvature unowned"),
            ("DEFINED_BY_BRANCH", "joint field/modulus variations with parity-specific traces"),
            ("NONE_SELECTED", "no carrier or Hopf topology is part of the P4 definition"),
            ("STATIONARY_ONLY", "Hessian/response result; physical time remains open"),
            ("CONDITIONAL_MIXED", "pairing census posture parity normalization and wall-response premises"),
            ("LINEAGE_FIXED", "constants census predates and conditions the banked P4 stability slice"),
            ("CENSUS_FORK_RELATION", "constant-domain one-form is a pullback of the field-domain form; solution-set relation remains open"),
        ],
        "F02": [
            ("DEFINED_CONDITIONAL", "P4 S-ii fields-census landing with live lambda subclasses"),
            ("CONDITIONAL_SECTOR", "no-m-jet and jet-quadratic sector forms; no whole native equation"),
            ("BOUNDED_SECTOR", "registered P1-4D landing and trace-zero witnesses"),
            ("PARTIAL", "zero-trace witness is germ-independent; complete physical boundary open"),
            ("DEFINED_BY_SUBCLASS", "joint depth/angular/live-modulus sector variations"),
            ("NONE_SELECTED", "no carrier or topology is owned"),
            ("STATIONARY_ONLY", "sector Hessian threshold is not time persistence"),
            ("CONDITIONAL_MIXED", "census pairing jet stiffness and existence premises travel"),
            ("LINEAGE_FIXED", "field census was separately registered before the P4 stability slice"),
            ("CENSUS_FORK_RELATION", "field domain contains constant sections but pointwise stationarity is stronger than pullback stationarity"),
        ],
        "F03": [
            ("DEFINED_CONTROL", "E0=0 constant and triad-locked massless control members"),
            ("SAME_PARENT_RESPONSE", "P4 quadratic control forms, not an independent equation"),
            ("CONTROL_DOMAINS", "registered limiting/control branches"),
            ("REGISTERED_CONTROL", "control trace/parity domains only"),
            ("DEGENERATE_CONTROL", "PSD form with exact flat zero-mode directions"),
            ("NONE_SELECTED", "no carrier/topology"),
            ("STATIONARY_CONTROL", "run validation, not persistence"),
            ("E0_ZERO_CONTROL", "massless/triad premises define the control"),
            ("LINEAGE_FIXED", "same P4 stability package as F01/F02"),
            ("CONTROL_UNION", "components validate separate P4 response branches; no whole-label containment follows"),
        ],
        "F04": [
            ("OBSERVED_CONDITIONAL", "full-3D finite-box map into a supplied round S2 carrier"),
            ("CHOSEN_CONDITIONAL", "audited no-null L2+L4 static functional, not a native complete action"),
            ("COMPUTATIONAL_DOMAIN", "finite box and compactified implementation; physical completion open"),
            ("COMPUTATIONAL_ONLY", "solver boundary is owned but no UDT physical carrier boundary is selected"),
            ("STATIC_DOMAIN_ONLY", "corrected static perturbation domain; physical time domain absent"),
            ("CARRIER_POSIT", "round S2 and Hopf sector are conditional, not metric-derived carrier emergence"),
            ("STATIC_ONLY", "relaxation and static Hessian evidence do not establish time persistence"),
            ("POSIT_AND_CONDITIONAL", "carrier POSIT, L2+L4 conditional, finite-box boundary chosen, time open"),
            ("LINEAGE_FIXED", "banked native-Hopfion topology audit lineage"),
            ("SEPARATE_MODEL_STREAM", "no derived injection or projection joins this model to the P4 field space"),
        ],
        "F05": [
            ("CROSS_CUTTING_CLASS", "completion and period classes over P4 configurations, not an independent field set"),
            ("STRUCTURAL_ONLY", "period and holonomy constraints supply no response or stability functional"),
            ("COMPLETION_TAXONOMY", "acyclic, cyclic, and quotient completions with real-period tests"),
            ("SEAM_DATA", "closure/posture data classify completion but do not select a physical boundary"),
            ("ABSENT", "no family-owned perturbation domain exists because this is not a response family"),
            ("NO_CARRIER", "cycle and holonomy structure do not derive a matter carrier"),
            ("NON_DYNAMICAL", "global completion classifier only"),
            ("CONDITIONAL_P4", "inherits the conditional P4 construction and completion premises"),
            ("LINEAGE_FIXED", "introduced by the P4 period-gate package"),
            ("CONSTRAINT_ON_REGISTERED_BRANCHES", "constrains F01/F02 completion branches and contributes scoped negatives collected in F06; no whole-label F03 map is derived"),
        ],
        "F06": [
            ("EMPTY_SCOPES", "no configurations survive in the registered massive cyclic-N1 and double-crease scopes"),
            ("INHERITED_CONSTRAINTS", "emptiness follows P4 closure and wall-trace equations, not a stability response"),
            ("SCOPED_COMPLETIONS", "massive cyclic N1 and double-crease premise domains only"),
            ("ELIMINATING_TRACES", "closure and wall traces eliminate the scoped candidate loci"),
            ("NOT_APPLICABLE", "an empty configuration set has no stability tangent space"),
            ("NONE", "no carrier or topology is selected"),
            ("NOT_APPLICABLE", "no solution exists in scope to evolve"),
            ("PREMISE_SCOPED_NEGATIVE", "exact only under the registered mass, closure, and crease premises"),
            ("LINEAGE_FIXED", "P4 stability and period-gate lineages"),
            ("EMPTY_SCOPE_UNION", "separate exact negative scopes grouped operationally; no one-parent containment theorem"),
        ],
        "F07": [
            ("PARTIAL_FORMAL_MODULES", "static, time, and angular modules are separately written but no common field is owned"),
            ("WHOLE_EQUATION_OPEN", "restriction equations exist; a native complete equation does not"),
            ("FORMAL_RESTRICTIONS", "module domains are formal and a complete finite-cell realization remains open"),
            ("OPEN", "no compatible differentiable physical boundary has been derived"),
            ("UNDEFINED_FOR_REALIZED_SET", "no base realization exists on which to define the full tangent space"),
            ("NO_COMPLETE_OWNERSHIP", "formal angular structure does not select a carrier or topology"),
            ("FORMAL_TIME_LABELS_ONLY", "time labels are not physical persistence or a time-live solution"),
            ("COMMON_STACK_PARTIAL", "field equation, boundary, tangent domain, and common premise stack remain open"),
            ("LINEAGE_FIXED", "stability-foundations and joint-realization audit lineages"),
            ("FORMAL_EMBEDDINGS_ONLY", "no constructive common nonzero on-shell object is established"),
        ],
    }

    axis_defs = rows("ONTOLOGY_AXIS_UNIVERSE.tsv")
    axis_rows = []
    source_by_family = {row["family_id"]: row["source_basis"] for row in family_rows}
    for family_id in [f"F{i:02d}" for i in range(1, 8)]:
        findings = axis_findings[family_id]
        if len(findings) != len(axis_defs):
            raise RuntimeError(f"axis cardinality mismatch for {family_id}")
        for axis, (axis_status, finding) in zip(axis_defs, findings):
            axis_rows.append({
                "family_id": family_id,
                "axis_id": axis["axis_id"],
                "axis": axis["axis"],
                "axis_status": axis_status,
                "finding": finding,
                "source_basis": source_by_family[family_id],
            })
    write_tsv("FAMILY_AXIS_MATRIX.tsv", axis_rows)

    relations = {
        ("F01", "F02"): ("FORMAL_EMBEDDING_ONLY", "constant sections embed in the field domain and the constant one-form is its pullback; the stationarity conditions and solution-set relation remain open", "A16-A17"),
        ("F01", "F03"): ("CONDITIONAL_ANALOGY_ONLY", "one F03 control component calibrates the constants-census response, but F03 is a union and is not contained in F01", "A01-A03;A16-A17"),
        ("F01", "F04"): ("NO_DERIVED_RELATION", "P4 and conditional Hopfion field spaces/functionals have no owned map", "A06-A11"),
        ("F01", "F05"): ("STRUCTURAL_CONSTRAINT_ON", "completion and period classes constrain S-i branches", "A01-A05"),
        ("F01", "F06"): ("NO_DERIVED_RELATION", "a double-crease component is linked to F01, but the union-valued F06 label has no whole-label containment relation", "A01-A05;A18"),
        ("F01", "F07"): ("NO_DERIVED_RELATION", "the frozen joint-realization closure rows do not establish an F01-to-F07 embedding", "A08-A13"),
        ("F02", "F03"): ("CONDITIONAL_ANALOGY_ONLY", "the triad control component calibrates a fields-census response, but F03 is a union and is not contained in F02", "A01-A03;A16-A17"),
        ("F02", "F04"): ("NO_DERIVED_RELATION", "P4 and conditional Hopfion field spaces/functionals have no owned map", "A06-A11"),
        ("F02", "F05"): ("STRUCTURAL_CONSTRAINT_ON", "completion and period classes constrain S-ii branches", "A01-A05"),
        ("F02", "F06"): ("NO_DERIVED_RELATION", "a massive cyclic component is linked to P4 completion, but the union-valued F06 label has no whole-label containment relation", "A01-A05;A18"),
        ("F02", "F07"): ("FORMAL_EMBEDDING_ONLY", "S-ii supplies one formal sector but not the joint realized F07 object", "A08-A13"),
        ("F03", "F04"): ("NO_DERIVED_RELATION", "no field-space or operator map is derived", "A06-A11"),
        ("F03", "F05"): ("NO_DERIVED_RELATION", "massless constants occur in both records but no whole-label configuration or response map is derived", "A01-A05"),
        ("F03", "F06"): ("DISJOINT_BY_FIELDS_OR_PREMISES", "F03 is massless control evidence while F06 records massive empty scopes", "A01-A05"),
        ("F03", "F07"): ("NO_DERIVED_RELATION", "controls diagnose missing joins but the frozen record proves no F03-to-F07 embedding", "A08-A13"),
        ("F04", "F05"): ("NO_DERIVED_RELATION", "P4 completion taxonomy is not derived for the Hopfion model", "A04-A08"),
        ("F04", "F06"): ("NO_DERIVED_RELATION", "P4 empty scopes do not exclude or contain the conditional Hopfion model", "A01-A08"),
        ("F04", "F07"): ("NO_DERIVED_RELATION", "architectural resemblance supplies no common realized field or map", "A06-A11"),
        ("F05", "F06"): ("STRUCTURAL_CONSTRAINT_ON", "period/closure conditions generate the exact empty subscopes", "A01-A05"),
        ("F05", "F07"): ("NO_DERIVED_RELATION", "completion taxonomy does not close the formal joint realization", "A04-A13"),
        ("F06", "F07"): ("NO_DERIVED_RELATION", "scoped P4 emptiness neither realizes nor globally excludes the formal modules", "A01-A13"),
    }
    pair_rows = []
    for pair in rows("PAIRWISE_UNIVERSE.tsv"):
        left, right = pair["left_family"], pair["right_family"]
        if left == right:
            relation, finding, basis = "SELF", "identity relation only", source_by_family[left]
        else:
            relation, finding, basis = relations[(left, right)]
        pair_rows.append({
            "pair_id": pair["pair_id"],
            "left_family": left,
            "right_family": right,
            "relation": relation,
            "finding": finding,
            "source_basis": basis,
        })
    write_tsv("PAIRWISE_RELATION_ATLAS.tsv", pair_rows)

    relation_axis_templates = {
        "STRUCTURAL_CONSTRAINT_ON": [
            ("CLASSIFIER_VERSUS_CONFIGURATION", "the structural side classifies admissibility of parent configurations"),
            ("NO_SHARED_RESPONSE", "completion/period law constrains but does not supply a stability response"),
            ("COMPLETION_CONSTRAINT", "cyclic/acyclic/quotient data restrict admissible global completion"),
            ("SEAM_CONSTRAINT", "seam/posture conditions constrain boundary compatibility"),
            ("NO_STRUCTURAL_TANGENT", "the classifier has no independent perturbation space"),
            ("NO_CARRIER_RELATION", "no carrier/topology map follows"),
            ("NON_DYNAMICAL_CONSTRAINT", "period/completion is structural, not time evolution"),
            ("INHERITED_P4_STACK", "constraint applies only inside the registered P4 premises"),
            ("RELATED_P4_LINEAGES", "stability and period packages establish the relation"),
            ("EXACT_ONE_WAY_CONSTRAINT", "constraint acts on the parent sector without becoming its subset"),
        ],
        "FORMAL_EMBEDDING_ONLY": [
            ("FORMAL_CONFIGURATION_EMBEDDING", "one registered domain or module embeds into the other only at the formal configuration level"),
            ("RESPONSE_RELATION_INCOMPLETE", "pullback/restriction data do not prove equality of on-shell responses"),
            ("DOMAIN_MAP_PARTIAL", "an exact domain/module map exists without a common realized global solution set"),
            ("BOUNDARY_JOIN_UNPROVED", "no common physical boundary completion follows from the embedding"),
            ("TANGENT_JOIN_UNPROVED", "the embedding does not identify full stability tangent spaces"),
            ("NO_CARRIER_COMPLETION", "no carrier/topology identity follows"),
            ("NO_DYNAMICAL_IDENTITY", "formal correspondence does not establish time persistence"),
            ("PREMISE_STACK_NOT_IDENTIFIED", "conditional premises remain branch-specific"),
            ("SOURCE_DERIVED_FORMAL_MAP", "the named source derives a formal pullback or module embedding"),
            ("NO_SOLUTION_SET_RELATION", "the exact relation stops before equality, inclusion, or overlap of realized solution sets"),
        ],
        "CONDITIONAL_ANALOGY_ONLY": [
            ("COMPONENT_LEVEL_ANALOGY", "one component calibrates or resembles the other label without a whole-label set relation"),
            ("RESPONSE_CONTROL_ANALOGY", "response forms are compared only under branch-specific conditional premises"),
            ("NO_WHOLE_DOMAIN_MAP", "union-valued and candidate labels lack a common exact domain map"),
            ("BRANCH_SPECIFIC_BOUNDARY", "boundary/posture comparisons do not lift to the whole labels"),
            ("NO_TANGENT_IDENTITY", "control and candidate perturbation spaces are not identified"),
            ("NO_CARRIER_RELATION", "no carrier/topology statement follows"),
            ("STATIONARY_ANALOGY_ONLY", "no time-persistence relation follows"),
            ("CONDITIONAL_COMPONENT_PREMISES", "the comparison depends on named census/control premises"),
            ("RELATED_PROGRAM_LINEAGE", "sources place the components in a shared P4 evidence program"),
            ("NO_CONTAINMENT_OR_IDENTITY", "component-level calibration does not prove whole-label containment or identity"),
        ],
        "DISJOINT_BY_FIELDS_OR_PREMISES": [
            ("PREMISE_DISJOINT", "massless control and massive empty scopes use mutually exclusive registered premises"),
            ("NOT_COMPARABLE_RESPONSES", "one side is a control response and the other an eliminated scope"),
            ("DISTINCT_SCOPES", "registered domains do not overlap under the mass premise"),
            ("DISTINCT_CONTROL_NEGATIVE_ROLES", "control and eliminating boundaries serve different logical roles"),
            ("NOT_A_COMMON_TANGENT", "no shared nonempty configuration set exists in scope"),
            ("NO_CARRIER_RELATION", "no carrier/topology follows"),
            ("NOT_APPLICABLE", "neither relation establishes time persistence"),
            ("MASS_PREMISE_EXCLUSION", "E0=0 and massive premises are mutually exclusive"),
            ("RELATED_P4_LINEAGES", "the same P4 program records both roles"),
            ("SCOPED_DISJOINTNESS_ONLY", "disjointness is premise-scoped, not a global species theorem"),
        ],
        "NO_DERIVED_RELATION": [
            ("NO_COMMON_FIELD_MAP", "no injection, projection, or common ambient physical field set is derived"),
            ("NO_OPERATOR_MAP", "no response/action equivalence or transfer is derived"),
            ("NO_DOMAIN_MAP", "no global completion map is established"),
            ("NO_BOUNDARY_MAP", "no physical boundary correspondence is established"),
            ("NO_TANGENT_MAP", "no perturbation-space correspondence is established"),
            ("NO_CARRIER_MAP", "no carrier/topology identity is established"),
            ("NO_DYNAMICAL_MAP", "no time-evolution correspondence is established"),
            ("INCOMPATIBLE_OR_UNJOINED_STACKS", "premise stacks are not proven common"),
            ("DISTINCT_SOURCE_LINEAGES", "sources establish separate objects or logical roles"),
            ("RELATION_OPEN", "absence of a derived relation is not a proof of physical disjointness"),
        ],
    }
    pair_axis_rows = []
    same_p4_no_map_pairs = {
        ("F01", "F06"), ("F01", "F07"), ("F02", "F06"), ("F03", "F05"),
        ("F03", "F07"), ("F05", "F07"), ("F06", "F07"),
    }
    for pair in pair_rows:
        if pair["left_family"] == pair["right_family"]:
            continue
        templates = relation_axis_templates[pair["relation"]]
        if len(templates) != len(axis_defs):
            raise RuntimeError(f"pair-axis template mismatch: {pair['relation']}")
        for axis, (comparison_status, finding) in zip(axis_defs, templates):
            if axis["axis_id"] == "A09" and (pair["left_family"], pair["right_family"]) in same_p4_no_map_pairs:
                comparison_status = "RELATED_P4_LINEAGES_NO_OBJECT_MAP"
                finding = "sources belong to related P4 audit lineages, but lineage proximity does not derive the missing whole-label object relation"
            pair_axis_rows.append({
                "pair_id": pair["pair_id"],
                "left_family": pair["left_family"],
                "right_family": pair["right_family"],
                "axis_id": axis["axis_id"],
                "axis": axis["axis"],
                "comparison_status": comparison_status,
                "finding": finding,
                "source_basis": pair["source_basis"],
            })
    write_tsv("PAIR_AXIS_MATRIX.tsv", pair_axis_rows)

    partition_gates = [
        {"gate_id": "G01", "gate": "DEFINED_CONFIGURATION_UNIVERSE", "status": "FAIL", "mechanical_finding": "F05 is a classifier, F06 is empty scope, and F07 is formal modules; the seven labels do not share one defined configuration universe", "consequence": "cannot interpret seven labels as seven solution families", "source_basis": "A01-A13"},
        {"gate_id": "G02", "gate": "OWNED_GOVERNING_EQUATION_OR_RESPONSE", "status": "FAIL", "mechanical_finding": "P4 owns conditional sector responses, F04 owns a different chosen functional, F05 has no response, and F07 lacks a complete equation", "consequence": "no common membership law partitions the labels", "source_basis": "A01-A15"},
        {"gate_id": "G03", "gate": "DISJOINTNESS_OR_EXPLICIT_OVERLAP", "status": "FAIL", "mechanical_finding": "F01/F02 have a formal constant-section pullback but no derived solution-set relation; F03/F06 are unions; F05 cross-cuts P4 completions", "consequence": "family counts are not counts of nonoverlapping physical types", "source_basis": "A01-A05;A16-A18"},
        {"gate_id": "G04", "gate": "COVERAGE_OF_PARENT_SOLUTION_SPACE", "status": "FAIL", "mechanical_finding": "no complete native UDT configuration/solution universe has been derived or exhaustively partitioned", "consequence": "the ledger is not a completeness theorem", "source_basis": "A08-A15"},
        {"gate_id": "G05", "gate": "COMMON_PREMISE_AND_BOUNDARY_STACK", "status": "FAIL", "mechanical_finding": "F01/F02 use an unresolved census-domain fork, while P4 and Hopfion use different conditional objects, functionals, carriers, and boundaries", "consequence": "cross-family stability comparison is premise-scoped only", "source_basis": "A06-A17"},
        {"gate_id": "G06", "gate": "REALIZED_OBJECTS_SEPARATED_FROM_FORMAL_AND_EMPTY_CLASSES", "status": "PASS_AFTER_CORRECTION", "mechanical_finding": "the present audit explicitly separates conditional realized objects, sectors, controls, constraints, empty scopes, and formal modules", "consequence": "the operational evidence map becomes honest and usable", "source_basis": "A01-A15"},
        {"gate_id": "G07", "gate": "NATIVE_UDT_REALIZATION", "status": "FAIL", "mechanical_finding": "neither P4 nor the Hopfion model supplies a carrier-independent native complete matter realization", "consequence": "zero native realized stability families are established", "source_basis": "A08-A15"},
    ]
    write_tsv("PARTITION_GATE_LEDGER.tsv", partition_gates)

    taxonomy_rows = [
        {"taxonomy_id": "T01", "object": "P4_CONDITIONAL_EVIDENCE_PROGRAM", "members_or_components": "F01;F02;F03;F06", "cross_cutting_classes": "F05", "formal_extensions": "F07", "status": "MULTIPLE_CENSUS_DOMAINS_NO_COMMON_SOLUTION_SET", "exact_scope": "stationary fields/moduli, completion, controls, and scoped negatives under registered but unresolved P4 census premises", "not_claimed": "one parent solution object, native matter field, species partition, or time-live universe"},
        {"taxonomy_id": "T02", "object": "P4_STABILITY_EVALUATED_CONDITIONAL_FAMILIES", "members_or_components": "F01;F02", "cross_cutting_classes": "F03;F05;F06", "formal_extensions": "F07", "status": "TWO_CENSUS_CONDITIONAL_RESULTS_FORK_OPEN", "exact_scope": "S-i constants-census and S-ii fields-census stationary responses", "not_claimed": "one parent solution set, exhaustive alternatives, or physical species"},
        {"taxonomy_id": "T03", "object": "P4_NONCANDIDATE_SUPPORT_CLASSES", "members_or_components": "F03;F05;F06;F07", "cross_cutting_classes": "F05", "formal_extensions": "F07", "status": "CONTROL_STRUCTURAL_EMPTY_AND_FORMAL", "exact_scope": "validation, completion, negative, and missing-join evidence", "not_claimed": "stable matter candidates"},
        {"taxonomy_id": "T04", "object": "HOPFION_CONDITIONAL_MODEL_STREAM", "members_or_components": "F04", "cross_cutting_classes": "none derived", "formal_extensions": "none derived", "status": "CONDITIONAL_REALIZED_STATIC_FINITE_BOX", "exact_scope": "supplied round-S2 carrier and corrected L2+L4 finite-box model", "not_claimed": "native carrier, physical boundary, time persistence, or emergence"},
        {"taxonomy_id": "T05", "object": "NATIVE_UDT_REALIZED_STABILITY_FAMILY_SET", "members_or_components": "none established", "cross_cutting_classes": "none", "formal_extensions": "none", "status": "OPEN_EMPTY_EVIDENCE_NOT_EMPTY_PHYSICS", "exact_scope": "native carrier/action/source/boundary/time join", "not_claimed": "nonexistence of native matter families"},
        {"taxonomy_id": "T06", "object": "STABILITY_HYPOTHESIS_SUPPORT_PROGRAMS", "members_or_components": "P4 conditional evidence program;Hopfion conditional exemplar", "cross_cutting_classes": "architectural comparison only", "formal_extensions": "joint realization remains open", "status": "TWO_RESEARCH_PROGRAMS_NO_DERIVED_JOIN", "exact_scope": "evidence that finite-cell and topological structures can support bounded conditional stability statements", "not_claimed": "two solution families, one theory, a selector, a bootstrap theorem, or mass emergence"},
    ]
    write_tsv("CORRECTED_STABILITY_TAXONOMY.tsv", taxonomy_rows)

    regrades = [
        {"regrade_id": "N01", "prior_wording_or_inference": "seven noninterchangeable stability families", "corrected_wording": "seven operational evidence categories of different ontological types", "status": "NARROWED", "reason": "partition gates G01-G05 fail", "source_basis": "A01-A13"},
        {"regrade_id": "N02", "prior_wording_or_inference": "F01 and F02 are sectors of one exact parent solution object", "corrected_wording": "F01 and F02 are conditional census families with an exact formal constant-section pullback but open solution-set relation", "status": "CORRECTED_AFTER_SOURCE_EXPANSION", "reason": "the census fork is an unresolved domain-definition choice and field response is typed not exhausted", "source_basis": "A16-A17"},
        {"regrade_id": "N03", "prior_wording_or_inference": "F03 is one candidate or one contained control family", "corrected_wording": "F03 is a union of massless/triad control components with no whole-label containment theorem", "status": "RECLASSIFIED", "reason": "its components validate different response branches", "source_basis": "A01-A03;A16-A17"},
        {"regrade_id": "N04", "prior_wording_or_inference": "F04 is a native realized family", "corrected_wording": "F04 is a conditional realized static finite-box model family", "status": "PREMISE_RESTATED", "reason": "round S2 carrier, L2+L4 functional, physical boundary, and time completion are not native", "source_basis": "A06-A08;A14-A15"},
        {"regrade_id": "N05", "prior_wording_or_inference": "F05 is a structural-existence solution family", "corrected_wording": "F05 is a cross-cutting completion/period classification", "status": "RECLASSIFIED", "reason": "no family-owned response or perturbation domain exists", "source_basis": "A04-A05;A13"},
        {"regrade_id": "N06", "prior_wording_or_inference": "F06 is an empty family contained wholesale in F01 or F02", "corrected_wording": "F06 is a union of exact empty premise scopes from different closure legs", "status": "RECLASSIFIED", "reason": "componentwise negative relations do not imply whole-label containment", "source_basis": "A01-A05;A18"},
        {"regrade_id": "N07", "prior_wording_or_inference": "F07 is a surviving family", "corrected_wording": "F07 is a formal module class with common realization open", "status": "RECLASSIFIED", "reason": "no common nonzero on-shell field, complete equation, boundary, or tangent space", "source_basis": "A08-A13"},
        {"regrade_id": "N08", "prior_wording_or_inference": "survivor count measures candidate physical species", "corrected_wording": "survivor labels are premise-scoped evidence states within heterogeneous categories", "status": "WITHDRAWN_AS_PHYSICAL_COUNT", "reason": "no native parent universe or exhaustive partition exists", "source_basis": "A01-A15"},
    ]
    write_tsv("NEGATIVE_AND_CLAIM_REGRADE.tsv", regrades)
    negative_crosswalk = [
        {"crosswalk_id": "X01", "current_scope": "F01 constants-census stability", "registry_match": "NO_EXACT_CURRENT_ENTRY", "registry_effect": "no historical negative is transported; current scoped instability/positive-core statements remain in A01-A03", "source_basis": "A01-A03;A18"},
        {"crosswalk_id": "X02", "current_scope": "F02 fields-census stability", "registry_match": "NO_EXACT_CURRENT_ENTRY", "registry_effect": "no historical negative is transported; current sector dichotomy remains in A01-A03", "source_basis": "A01-A03;A18"},
        {"crosswalk_id": "X03", "current_scope": "F03 control union", "registry_match": "NO_EXACT_CURRENT_ENTRY", "registry_effect": "controls remain validation evidence, not a negative physical family", "source_basis": "A01-A03;A18"},
        {"crosswalk_id": "X04", "current_scope": "F04 conditional Hopfion model", "registry_match": "RELATED_HISTORICAL_ENTRY_61", "registry_effect": "the imported winding-catalog BC negative is premise-distinct and does not erase the later conditional full-3D Hopf-capable object", "source_basis": "A06-A08;A18"},
        {"crosswalk_id": "X05", "current_scope": "F05 completion/period class", "registry_match": "NO_EXACT_CURRENT_ENTRY", "registry_effect": "current all-definite massive-ring exclusion retains only A04-A05 premises", "source_basis": "A04-A05;A18"},
        {"crosswalk_id": "X06", "current_scope": "F06 empty-scope union", "registry_match": "NO_EXACT_CURRENT_ENTRY", "registry_effect": "each current negative retains its own cyclic-N1 or double-crease premise scope", "source_basis": "A01-A05;A18"},
        {"crosswalk_id": "X07", "current_scope": "F07 formal modules", "registry_match": "NO_EXACT_CURRENT_ENTRY", "registry_effect": "missing joint realization is an open join, not a historical nonexistence theorem", "source_basis": "A08-A13;A18"},
        {"crosswalk_id": "X08", "current_scope": "seven-label physical family count", "registry_match": "RELATED_HISTORICAL_CATALOG_NEGATIVES_ONLY", "registry_effect": "older catalog negatives use different carriers/operators and cannot decide the current ontology; the count is withdrawn by present partition-gate failure", "source_basis": "A12-A13;A18"},
    ]
    write_tsv("NEGATIVE_REGISTRY_CROSSWALK.tsv", negative_crosswalk)

    readiness_rows = [
        {"family_id": "F01", "inherited_readiness": "CPU_EXACT_CHECK_READY_LAMBDA_SCHUR_ONLY", "ontology_corrected_readiness": "UNCHANGED_CPU_EXACT_CHECK_READY_LAMBDA_SCHUR_ONLY", "promotion": "NO", "reason": "bounded calculation remains valid for the S-i sector despite family relabeling"},
        {"family_id": "F02", "inherited_readiness": "BLOCKED_MISSING_FIXED_REALIZATION", "ontology_corrected_readiness": "UNCHANGED_BLOCKED_MISSING_FIXED_REALIZATION", "promotion": "NO", "reason": "sector identity does not supply the missing joint realization"},
        {"family_id": "F03", "inherited_readiness": "CONTROL_ONLY", "ontology_corrected_readiness": "UNCHANGED_CONTROL_ONLY", "promotion": "NO", "reason": "control stratum is not a candidate solve target"},
        {"family_id": "F04", "inherited_readiness": "BLOCKED_MISSING_TIME_EQUATION", "ontology_corrected_readiness": "UNCHANGED_BLOCKED_MISSING_TIME_EQUATION", "promotion": "NO", "reason": "conditional model identity does not derive physical time or boundary"},
        {"family_id": "F05", "inherited_readiness": "BLOCKED_MISSING_NATIVE_RESPONSE", "ontology_corrected_readiness": "NOT_A_STABILITY_SOLVE_TARGET_WITHOUT_NEW_RESPONSE", "promotion": "NO", "reason": "completion classifier cannot be tested as a stability family"},
        {"family_id": "F06", "inherited_readiness": "NOT_APPLICABLE_EMPTY", "ontology_corrected_readiness": "UNCHANGED_NOT_APPLICABLE_EMPTY", "promotion": "NO", "reason": "exact empty premise scopes contain no object to perturb"},
        {"family_id": "F07", "inherited_readiness": "BLOCKED_MISSING_FIXED_REALIZATION", "ontology_corrected_readiness": "UNCHANGED_BLOCKED_MISSING_FIXED_REALIZATION", "promotion": "NO", "reason": "formal modules do not supply their missing common object"},
    ]
    write_tsv("READINESS_REGRADE.tsv", readiness_rows)

    premise_rows = [
        {"premise_id": "L01", "scope": "F01;F02;F03;F05;F06;F07", "premise": "P4 conditional response/evidence program", "status": "CONDITIONAL", "audit_effect": "does not supply a complete native matter solution universe", "source_basis": "A01-A05;A08-A11;A15-A17"},
        {"premise_id": "L02", "scope": "F01", "premise": "BASE constants census with seven constant moduli directions", "status": "CARRIED_FORK_NOT_SELECTED", "audit_effect": "integrated moduli rows define F01's conditional domain", "source_basis": "A16-A17"},
        {"premise_id": "L03", "scope": "F02", "premise": "BR-M fields census with live moduli directions", "status": "CARRIED_FORK_NOT_SELECTED", "audit_effect": "pointwise rows define F02's conditional domain", "source_basis": "A16-A17"},
        {"premise_id": "L04", "scope": "F01;F02", "premise": "constants-versus-fields census fork", "status": "OPEN_DOMAIN_DEFINITION_CHOICE", "audit_effect": "forbids a common parent-solution-set or physical-family claim", "source_basis": "A16-A17"},
        {"premise_id": "L05", "scope": "F01;F02", "premise": "pairing family P1-4D P1-triad P2 with symbolic a_F", "status": "CARRIED_NOT_ADOPTED", "audit_effect": "pairing-specific response statements cannot be generalized", "source_basis": "A01-A03;A16"},
        {"premise_id": "L06", "scope": "F01;F02;F03;F06", "premise": "posture census open crease glue cyclic quotient acyclic", "status": "CARRIED_NOT_SELECTED", "audit_effect": "completion and negative claims remain posture-scoped", "source_basis": "A01-A05"},
        {"premise_id": "L07", "scope": "F01;F02", "premise": "depth mirror parity canonical and f/bh/moduli parities", "status": "MIXED_DERIVED_AND_SUPPLIED", "audit_effect": "positive/negative stability branches retain exact parity stamps", "source_basis": "A01-A03;A16"},
        {"premise_id": "L08", "scope": "F01", "premise": "wall first germs pinned or forced while second and higher germs are free", "status": "BOUNDED_OPEN", "audit_effect": "prevents full F01 Hessian/stability certification", "source_basis": "A01-A03;A13"},
        {"premise_id": "L09", "scope": "F01;F02", "premise": "jet order at most two with N4 typed not run", "status": "BOUNDED_SCOPE", "audit_effect": "all P4 stability statements stop at the registered layer", "source_basis": "A01-A03;A13"},
        {"premise_id": "L10", "scope": "F01", "premise": "ell equals one normalization and g_p positive scale normalization on certified branch", "status": "CHOSE_SIGN_INVARIANT_SCOPE", "audit_effect": "certified branch verdict is not an all-scale theorem", "source_basis": "A03"},
        {"premise_id": "L11", "scope": "F01", "premise": "germ-Hessian-flat realized wall responses for trace-active verdicts", "status": "CONDITIONAL_WITNESS_RESPONSE", "audit_effect": "free second-germ curvature remains unowned", "source_basis": "A01-A03;A13"},
        {"premise_id": "L12", "scope": "F02", "premise": "P1-4D landing p=0 lambda=0 with affine angular fields", "status": "CONDITIONAL_LANDING", "audit_effect": "F02 result is not a complete joint realized universe", "source_basis": "A01-A03;A17"},
        {"premise_id": "L13", "scope": "F02", "premise": "AM-1 AM-2 p0==0 and moduli-jet subclasses", "status": "CONDITIONALITIES_TRAVEL", "audit_effect": "field-census response is registered/typed but not exhausted", "source_basis": "A03;A17"},
        {"premise_id": "L14", "scope": "F02", "premise": "positive jet stiffness c_m and sector parameters E0 ell g_p", "status": "FREE_CONDITIONAL_PARAMETERS", "audit_effect": "the stability threshold is continuous and sector-scoped", "source_basis": "A01-A03"},
        {"premise_id": "L15", "scope": "F03", "premise": "E0=0 constants control and triad-locked control are grouped", "status": "OPERATIONAL_UNION", "audit_effect": "component controls do not imply whole-label containment", "source_basis": "A01-A03"},
        {"premise_id": "L16", "scope": "F05", "premise": "real period and cyclic/acyclic/quotient completion laws", "status": "DERIVED_STRUCTURAL_SCOPED", "audit_effect": "classifies completion but supplies no stability response", "source_basis": "A04-A05;A13"},
        {"premise_id": "L17", "scope": "F06", "premise": "massive cyclic single-cell N1 scope", "status": "EXACT_EMPTY_SCOPED", "audit_effect": "negative reopens if mass or completion premise changes", "source_basis": "A01-A05;A18"},
        {"premise_id": "L18", "scope": "F06", "premise": "massive double-crease wall-trace scope", "status": "EXACT_EMPTY_SCOPED", "audit_effect": "separate negative component cannot be merged into a whole-label subset theorem", "source_basis": "A01-A05;A18"},
        {"premise_id": "L19", "scope": "F07", "premise": "static time-live and angular-live restriction modules", "status": "FORMAL_EXACT_SEPARATELY", "audit_effect": "separate modules cannot be spliced into a field", "source_basis": "A08-A11;A13"},
        {"premise_id": "L20", "scope": "F07", "premise": "one common nonzero on-shell field and native whole equation", "status": "OPEN", "audit_effect": "blocks realized-family and stability claims", "source_basis": "A08-A11;A13-A15"},
        {"premise_id": "L21", "scope": "F07", "premise": "compatible differentiable boundary tangent domain and one premise stack", "status": "OPEN_OR_PARTIAL", "audit_effect": "blocks joint realization even when modules are separately nonempty", "source_basis": "A08-A11;A13"},
        {"premise_id": "L22", "scope": "F04", "premise": "round S2 carrier", "status": "POSIT", "audit_effect": "conditions the Hopfion object; cannot establish native family ontology", "source_basis": "A06-A08;A14-A15"},
        {"premise_id": "L23", "scope": "F04", "premise": "corrected no-null L2+L4 functional", "status": "CONDITIONAL", "audit_effect": "owns static response only and is not a native complete matter action", "source_basis": "A06-A08;A14-A15"},
        {"premise_id": "L24", "scope": "F04", "premise": "finite computational box and solver boundary", "status": "CHOSE_COMPUTATIONAL", "audit_effect": "does not select physical finite-cell completion", "source_basis": "A06-A08;A13"},
        {"premise_id": "L25", "scope": "F04;F07;global", "premise": "native physical time equation and perturbation domain", "status": "OPEN", "audit_effect": "no family has native time-persistence certification", "source_basis": "A08-A15"},
        {"premise_id": "L26", "scope": "global", "premise": "bootstrap membership and family selection", "status": "WORKING_OPEN", "audit_effect": "not used to define or promote any family", "source_basis": "A08-A15"},
        {"premise_id": "L27", "scope": "global", "premise": "complete native matter action source boundary and mass", "status": "OPEN", "audit_effect": "prevents a native exhaustive solution-family partition", "source_basis": "A14-A15"},
        {"premise_id": "L28", "scope": "global", "premise": "inherited F01-F07 labels", "status": "WORKING_OPERATIONAL", "audit_effect": "retained as stable evidence identifiers, not physical-family names", "source_basis": "A12-A13"},
        {"premise_id": "L29", "scope": "negative regrades", "premise": "historical negative registry premise continuity", "status": "AUDITED_NO_SILENT_TRANSPORT", "audit_effect": "current P4/Hopfion claims do not inherit older operator/carrier negatives without matching premises", "source_basis": "A18"},
    ]
    write_tsv("PREMISE_LEDGER.tsv", premise_rows)

    status_counts: dict[str, int] = {}
    for row in family_rows:
        status_counts[row["primary_ontology"]] = status_counts.get(row["primary_ontology"], 0) + 1
    relation_counts: dict[str, int] = {}
    for row in pair_rows:
        relation_counts[row["relation"]] = relation_counts.get(row["relation"], 0) + 1
    result = {
        "audit": "UDT stability family ontology audit",
        "outcome": "OPERATIONAL_EVIDENCE_MAP_NOT_SOLUTION_PARTITION",
        "source_artifact_count": len(source_inventory),
        "authority_count": len(authority_rows),
        "inherited_label_count": len(family_rows),
        "axis_cell_count": len(axis_rows),
        "pair_count": len(pair_rows),
        "pair_axis_cell_count": len(pair_axis_rows),
        "primary_ontology_counts": status_counts,
        "pair_relation_counts": relation_counts,
        "native_realized_family_count": 0,
        "conditional_realized_family_count": 3,
        "conditional_research_program_count": 2,
        "readiness_promotions": 0,
        "solves_run": 0,
        "gpu_runs": 0,
        "maximum_conclusion": "Within the corrected 1,608-source freeze, the inherited F01-F07 ledger is an operational evidence map, not an exhaustive or disjoint physical solution-family partition. F01 and F02 are separate conditional P4 census families linked only by a formal constant-section pullback while their solution-set relation and physical census choice remain open; F03/F05/F06/F07 are control, structural, empty, and formal evidence classes; F04 is a separate conditional Hopfion model. No native UDT realized stability family or bootstrap-selected matter taxonomy is derived.",
    }
    (PKG / "AUDIT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
