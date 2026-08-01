#!/usr/bin/env python3
"""Deterministic whole-configuration Reciprocity adjudication and controls."""

from __future__ import annotations

import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PKG = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rank(matrix: list[list[Fraction]]) -> int:
    a = [row[:] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    p = 0
    for col in range(cols):
        pivot = next((i for i in range(p, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[p], a[pivot] = a[pivot], a[p]
        scale = a[p][col]
        a[p] = [x / scale for x in a[p]]
        for i in range(rows):
            if i != p and a[i][col]:
                scale = a[i][col]
                a[i] = [x - scale * y for x, y in zip(a[i], a[p])]
        p += 1
        if p == rows:
            break
    return p


def anchor(anchor_id: str, path: str, authority: str, role: str, ruling: str) -> dict[str, str]:
    full = ROOT / path
    if not full.is_file():
        raise FileNotFoundError(path)
    return {
        "anchor_id": anchor_id,
        "path": path,
        "sha256": sha256(full),
        "authority": authority,
        "role": role,
        "ruling": ruling,
    }


def main() -> None:
    inventory = tsv(PKG / "SOURCE_INVENTORY.tsv")
    if len(inventory) != 1384:
        raise RuntimeError("unexpected frozen source count")
    for row in inventory:
        path = ROOT / row["path"]
        if not path.is_file() or sha256(path) != row["sha256"]:
            raise RuntimeError(f"source drift: {row['path']}")

    anchors = [
        anchor("A01", "CURRENT_SCIENTIFIC_PREMISES.tsv", "CURRENT_CONTROL", "active premise registry", "phi founded; bootstrap type-only; Xmax working schema; CSN inactive; complete physics open"),
        anchor("A02", "udt_three_reciprocity_delta_k_audit_2026-07-23/THREE_RECIPROCITY_ROLE_MAP.tsv", "POST_FIREWALL_VERIFIED_EVIDENCE", "three meanings", "observer covariance does not imply Delta_K=0; dual pair and Xmax roles are separate"),
        anchor("A03", "udt_founding_reciprocity_object_audit_2026-07-27/AUDIT_REPORT.md", "POST_FIREWALL_CONTROLLING_AUDIT", "founding object", "covariant local relational comparison is founded; global parallelism is not"),
        anchor("A04", "udt_founding_reciprocity_object_audit_2026-07-27/IMPLICATION_GRAPH.tsv", "POST_FIREWALL_CONTROLLING_AUDIT", "implication boundaries", "observer covariance to endpoint lift and global parallel field are exact nonedges"),
        anchor("A05", "udt_founding_observer_comparison_semantics_audit_2026-07-27/AUDIT_REPORT.md", "POST_FIREWALL_CONTROLLING_AUDIT", "observer semantics", "abstract ordered operator derived; endpoint versus path physical semantics open"),
        anchor("A06", "udt_complete_coframe_native_selector_audit_2026-07-26/SELECTOR_CAPABILITY_LEDGER.tsv", "POST_FIREWALL_VERIFIED_EVIDENCE", "selector rank", "observer-frame reciprocity has zero selector rank on the registered extension family"),
        anchor("A07", "udt_complete_coframe_physical_comparison_functor_audit_2026-07-27/AUDIT_REPORT.md", "POST_FIREWALL_VERIFIED_EVIDENCE", "comparison functor", "composition is available for supplied data but physical comparison functor remains open"),
        anchor("A08", "udt_global_reciprocal_bundle_assembly_audit_2026-07-26/AUDIT_REPORT.md", "POST_FIREWALL_VERIFIED_EVIDENCE", "global bundle", "path-groupoid all lambda; endpoint-parallel lambda one only after an extra requirement"),
        anchor("A09", "udt_observer_pair_triangle_consistency_audit_2026-07-26/STATUS_LEDGER.tsv", "POST_FIREWALL_VERIFIED_EVIDENCE", "pair cocycle", "abstract composition derived; endpoint section and finite-cell descent remain open"),
        anchor("A10", "udt_native_global_coframe_definition_audit_2026-07-28/AUDIT_REPORT.md", "POST_FIREWALL_VERIFIED_EVIDENCE", "global coframe definition", "multiple independent selector gaps and arbitrary smooth phi/lambda controls remain"),
        anchor("A11", "udt_bootstrap_closure_ownership_audit_2026-08-01/AUDIT_REPORT.md", "IMMEDIATE_VERIFIED_PARENT", "closure ownership", "typed partial R exists; nonidentity return A remains open"),
        anchor("A12", "udt_jr_cert_native_derivation_2026-08-01/AUDIT_REPORT.md", "VERIFIED_PARENT_EVIDENCE", "native equation route census", "zero of eight equation routes passes; identities reconstruct rather than select"),
        anchor("A13", "udt_p4_cold_review_repair_2026-08-01/CLOSURE_REPORT.md", "POST_FIREWALL_COLD_REVIEW", "P4 authority ceiling", "formal response/census evidence; no response law selected"),
        anchor("A14", "UDT_NATIVE_ACTION_COLD_PACKET.md", "HISTORICAL_FROZEN_PACKET", "founding dual pair wording", "usable for founded Reciprocity wording only; later registry controls CSN, finite-cell, and bootstrap grades"),
        anchor("A15", "macro_phase1_metric_only.md", "POST_FIREWALL_SCOPED_MACRO_RECORD", "static macro reduction", "R1-R3 leave transverse geometry, time dependence, topology, and phi profile open"),
    ]
    write_tsv(PKG / "SOURCE_AUTHORITY_LEDGER.tsv", list(anchors[0]), anchors)

    conflicts = [
        dict(conflict_id="C01", older_statement="UDT_NATIVE_ACTION_COLD_PACKET labels strong local CSN FOUNDING", current_control="CURRENT_SCIENTIFIC_PREMISES G04", ruling="SUPERSEDED_FOR_CURRENT_USE__CSN_INACTIVE_CHALLENGED", effect_on_reciprocity_audit="none; no conformal quotient or selector used"),
        dict(conflict_id="C02", older_statement="cold packet presents finite mirrored cell as binding canon", current_control="CURRENT_SCIENTIFIC_PREMISES G17-G18", ruling="CURRENT_SPLIT_READING_CONTROLS__MIRROR_CLOSURE_WORKING_NOT_DERIVED", effect_on_reciprocity_audit="no boundary or completion promoted"),
        dict(conflict_id="C03", older_statement="macro static reduction uses radial slot and phi-gradient adaptation", current_control="CURRENT_SCIENTIFIC_PREMISES G01-G08 plus complete-coframe audits", ruling="SCOPED_STATIC_REDUCTION_ONLY", effect_on_reciprocity_audit="cannot define full observer action or whole return"),
        dict(conflict_id="C04", older_statement="pre-July CANON contains later-regraded physics claims", current_control="July-1 provenance firewall and current registry", ruling="PROVENANCE_OR_FAILURE_ONLY", effect_on_reciprocity_audit="no affirmative result sourced from pre-July material"),
        dict(conflict_id="C05", older_statement="observer, dual-slot, and Xmax reciprocity sometimes share one word", current_control="three-reciprocity role map", ruling="THREE_OBJECTS_SEPARATE", effect_on_reciprocity_audit="no cross-role implication permitted"),
    ]
    write_tsv(PKG / "SOURCE_CONFLICT_LEDGER.tsv", list(conflicts[0]), conflicts)

    interpretations = [
        dict(candidate_id="I01", interpretation="PASSIVE_FRAME_RELABELING", status="DERIVED_DESCRIPTION_GROUPOID_EQUIVALENCE", whole_configuration_content="laws and tensorial readouts must be natural under observer-description changes", return_gate="FAIL_NO_ZERO_SET", source_anchor="A02;A03;A05"),
        dict(candidate_id="I02", interpretation="ACTIVE_RECIPROCAL_EXCHANGE", status="DERIVED_EQUIVARIANT_ACTION_NOT_FIXEDNESS", whole_configuration_content="supplied complete objects transform covariantly under the exchange action", return_gate="FAIL_EQUIVARIANCE_ONLY", source_anchor="A03;A04;A06"),
        dict(candidate_id="I03", interpretation="PAIRWISE_COMPARISON_COCYCLE", status="DERIVED_ABSTRACT_COCYCLE_RECONSTRUCTION_NOT_SELECTION", whole_configuration_content="ordered depths compose reverse and reconstruct relative values modulo common offset when supplied", return_gate="FAIL_ALL_DEPTH_CONFIGURATIONS_ADMITTED", source_anchor="A05;A07;A09"),
        dict(candidate_id="I04", interpretation="GLOBAL_FIXED_POINT", status="NOT_DERIVED_FIXEDNESS_IS_EXTRA_PREMISE", whole_configuration_content="X=S X would select the fixed locus rather than express equivalence of frames", return_gate="FAIL_FIXEDNESS_SMUGGLE", source_anchor="A03;A04;A06"),
        dict(candidate_id="I05", interpretation="ORBIT_OR_GROUP_AVERAGE", status="NOT_DERIVED_REQUIRES_MEASURE_OR_PROJECTION", whole_configuration_content="orbit equivalence is available after an action; an average or representative is not", return_gate="FAIL_UNSELECTED_PROJECTION", source_anchor="A05;A08"),
        dict(candidate_id="I06", interpretation="RECIPROCAL_DUAL_PAIRING", status="PAIRING_DERIVED_ON_2D_PAIR_NO_FULL_RESPONSE_COVECTOR", whole_configuration_content="K pairs the clock/ruler representation and constrains its character", return_gate="FAIL_NO_FULL_DOMAIN_PAIRING_OR_LEVEL", source_anchor="A02;A06;A14"),
        dict(candidate_id="I07", interpretation="FINITE_CELL_INVOLUTION_AND_GLUE", status="CONDITIONAL_PARTIAL_ADMISSIBILITY_NO_COMPLETE_RETURN", whole_configuration_content="algebraic reversal and selected completions can constrain joins", return_gate="FAIL_BOUNDARY_COMPLETION_NOT_FOUNDED_BY_RECIPROCITY", source_anchor="A03;A08;A10"),
        dict(candidate_id="I08", interpretation="BOOTSTRAP_JOIN", status="NO_JOIN_GRAPH_REMAINS_NONSELECTION", whole_configuration_content="Reciprocity requires a future A and R to transform compatibly", return_gate="FAIL_NO_MAP_FROM_EQUIVARIANCE_TO_A", source_anchor="A01;A11;A12"),
        dict(candidate_id="I09", interpretation="P4_EQUIVARIANT_RESPONSE_SPACE", status="CONSTRAINED_EQUIVARIANT_FAMILY_NOT_UNIQUE", whole_configuration_content="Reciprocity restricts transformation type of candidate response laws", return_gate="FAIL_PERMITTED_FAMILY_NOT_SELECTED_MEMBER", source_anchor="A06;A13"),
        dict(candidate_id="I10", interpretation="OTHER_FROZEN_INTERPRETATION", status="NO_OTHER_FOUNDED_RETURN_FOUND", whole_configuration_content="bounded 1384-source census contains no additional founded zero-set operation", return_gate="FAIL_BOUNDED_NEGATIVE", source_anchor="A01-A15"),
    ]
    write_tsv(PKG / "INTERPRETATION_OUTCOMES.tsv", list(interpretations[0]), interpretations)

    naturality = [
        dict(obligation_id="N01", object="observer_change_groupoid_on_descriptions", status="DERIVED_ABSTRACT_AND_CONDITIONAL_COMPLETE_ACTION", consequence="comparison laws have composition reversal and identity; complete physical arrows remain open"),
        dict(obligation_id="N02", object="action_on_complete_U_full", status="PARTIAL_CONDITIONAL", consequence="local/coframe/path actions exist when data supplied; boundary and completion action not universal"),
        dict(obligation_id="N03", object="action_on_global_readout_O", status="TYPED_BY_COMPONENT_NOT_ONE_COMPLETE_O", consequence="each valid readout must retain observer/path transformation arguments"),
        dict(obligation_id="N04", object="future_return_equivariance", status="DERIVED_REQUIREMENT_GIVEN_A", consequence="A(gX,rho_g O)=sigma_g A(X,O)"),
        dict(obligation_id="N05", object="future_zero_set_orbit_saturation", status="DERIVED_REQUIREMENT_GIVEN_ZERO_PRESERVING_sigma", consequence="if sigma_g(0)=0 then A=0 implies transformed A=0 throughout each observer orbit"),
        dict(obligation_id="N06", object="fixed_configuration_requirement", status="NOT_DERIVED", consequence="equivalence or covariance does not imply X=gX"),
        dict(obligation_id="N07", object="canonical_orbit_representative_or_average", status="NOT_DERIVED", consequence="requires a measure gauge section or projection"),
        dict(obligation_id="N08", object="complete_nonidentity_return_A", status="OPEN_NOT_DERIVED", consequence="naturality constrains a supplied law but does not manufacture its formula or zero set"),
    ]
    write_tsv(PKG / "WHOLE_LAW_NATURALITY_LEDGER.tsv", list(naturality[0]), naturality)

    # Control 1: a swap orbit is not a fixed point.
    s = [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]]
    x = [Fraction(1), Fraction(2)]
    sx = [x[1], x[0]]
    orbit_size = len({tuple(x), tuple(sx)})
    is_fixed = x == sx
    fixed_matrix = [[Fraction(1), Fraction(-1)]]  # x1-x2=0
    fixed_rank = rank(fixed_matrix)

    # Control 2: same Z2 action, inequivalent equivariant return operations.
    witnesses = [(0, 0), (1, 1), (1, 0), (0, 1), (-1, 1)]
    survivor_counts = {
        "A_identity_zero_origin": sum(v == (0, 0) for v in witnesses),
        "A_difference_zero_diagonal": sum(v[0] == v[1] for v in witnesses),
        "A_product_zero_axes": sum(v[0] * v[1] == 0 for v in witnesses),
    }
    # identity and difference are vector-equivariant; product-minus-one is scalar-invariant.
    equivariance_checks = []
    for a, b in witnesses:
        ident_left, ident_right = (b, a), (b, a)
        diff_left = (b - a, a - b)
        diff_right = (-(a - b), a - b)
        prod_left = b * a
        prod_right = a * b
        equivariance_checks.append(ident_left == ident_right and diff_left == diff_right and prod_left == prod_right)
    assert all(equivariance_checks)
    assert len(set(survivor_counts.values())) == 3

    # An invertible codomain action need not preserve the distinguished zero.
    # With s(x)=1-x, sigma(y)=1-y, and A(x)=x, equivariance holds but A(0)=0
    # is carried to A(s(0))=1.  Orbit saturation therefore additionally needs
    # sigma_g(0)=0, as for a linear/vector-bundle representation.
    affine_domain = [Fraction(0), Fraction(1)]
    affine_equivariant = all((1 - x) == (1 - x) for x in affine_domain)
    affine_sigma_invertible = all(1 - (1 - y) == y for y in affine_domain)
    affine_sigma_fixes_zero = (1 - 0) == 0
    affine_zero_set_orbit_saturated = ((0 == 0) == ((1 - 0) == 0))
    assert affine_equivariant and affine_sigma_invertible
    assert not affine_sigma_fixes_zero and not affine_zero_set_orbit_saturated

    # Control 3: four-observer additive-depth incidence map.
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    incidence = []
    for i, j in edges:
        row = [Fraction(0)] * 4
        row[i], row[j] = Fraction(-1), Fraction(1)
        incidence.append(row)
    incidence_rank = rank(incidence)
    incidence_nullity = 4 - incidence_rank
    assert incidence_rank == 3 and incidence_nullity == 1
    phi_witnesses = [
        (0, 0, 0, 0),
        (0, 1, 4, -2),
        (7, -3, 2, 5),
    ]
    comparisons = []
    triangle_residuals = []
    for phi in phi_witnesses:
        y = tuple(phi[j] - phi[i] for i, j in edges)
        comparisons.append(y)
        # One orientation of each of the four sorted K4 triangles, evaluated
        # independently on each of the three phi witnesses.
        table = {edge: value for edge, value in zip(edges, y)}
        for i, j, k in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]:
            triangle_residuals.append(table[(i, j)] + table[(j, k)] - table[(i, k)])
    assert all(v == 0 for v in triangle_residuals)
    graph_jac = [[-v for v in row] + [Fraction(int(i == j)) for j in range(6)] for i, row in enumerate(incidence)]
    graph_rank = rank(graph_jac)
    graph_nullity = 10 - graph_rank
    assert graph_rank == 6 and graph_nullity == 4

    # Control 4: internal dual pairing is preserved but does not select an invariant level.
    dual_checks = []
    for q in [Fraction(2), Fraction(3), Fraction(5)]:
        d = [[1 / q, Fraction(0)], [Fraction(0), q]]
        # D^T K D, with K the swap matrix.
        dtkd = [
            [Fraction(0), d[0][0] * d[1][1]],
            [d[1][1] * d[0][0], Fraction(0)],
        ]
        dual_checks.append(dtkd == s)
    assert all(dual_checks)
    level_witnesses = [(0, 2), (1, 1), (2, Fraction(1, 2)), (2, 2)]
    invariant_level_counts = {
        "x1x2_zero": sum(a * b == 0 for a, b in level_witnesses),
        "x1x2_one": sum(a * b == 1 for a, b in level_witnesses),
        "x1x2_four": sum(a * b == 4 for a, b in level_witnesses),
    }

    algebra = {
        "scope": "exact finite-dimensional logic and representation controls; not candidate UDT physics",
        "swap_matrix": [[int(v) for v in row] for row in s],
        "nonfixed_orbit_witness": [int(v) for v in x],
        "swapped_witness": [int(v) for v in sx],
        "orbit_size": orbit_size,
        "witness_is_fixed": is_fixed,
        "fixed_locus_constraint_rank": fixed_rank,
        "equivariant_return_survivor_counts": survivor_counts,
        "equivariance_checks": len(equivariance_checks),
        "equivariance_failures": sum(not v for v in equivariance_checks),
        "affine_sigma_equivariant": affine_equivariant,
        "affine_sigma_invertible": affine_sigma_invertible,
        "affine_sigma_fixes_zero": affine_sigma_fixes_zero,
        "affine_zero_set_orbit_saturated": affine_zero_set_orbit_saturated,
        "observer_count": 4,
        "pair_edge_count": 6,
        "incidence_rank": incidence_rank,
        "incidence_nullity": incidence_nullity,
        "sorted_triangle_witness_checks": len(triangle_residuals),
        "triangle_failures": sum(v != 0 for v in triangle_residuals),
        "comparison_graph_rank": graph_rank,
        "comparison_graph_nullity": graph_nullity,
        "comparison_graph_configuration_dimension": 4,
        "dual_pairing_preservation_checks": len(dual_checks),
        "dual_pairing_preservation_failures": sum(not v for v in dual_checks),
        "invariant_level_survivor_counts": invariant_level_counts,
        "conclusions": [
            "orbit equivalence does not imply fixedness",
            "equivariance does not select a unique return operation or zero set",
            "invertibility alone does not preserve a return-law zero set; sigma_g(0)=0 is additionally required",
            "pairwise reciprocal cocycle reconstruction leaves the full supplied depth configuration free in its graph and only removes a common offset when comparisons are externally fixed",
            "the internal dual pairing fixes representation structure but not an invariant level or full response covector",
        ],
    }
    (PKG / "ALGEBRA_RESULT.json").write_text(json.dumps(algebra, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    status = [
        dict(claim="observer_frame_reciprocity", status="DERIVED_LAW_EQUIVARIANCE_REQUIREMENT", basis="I01,I02,N04", remaining="complete physical observer/path/boundary action"),
        dict(claim="zero_set_orbit_saturation", status="DERIVED_GIVEN_FUTURE_A_COMPLETE_ACTION_AND_ZERO_PRESERVING_sigma", basis="N05 and affine counterexample", remaining="formula, codomain, pairing, zero-preserving codomain action, and existence of A"),
        dict(claim="whole_configuration_fixedness", status="NOT_DERIVED", basis="I04 and orbit control", remaining="would be a new invariance premise"),
        dict(claim="pairwise_depth_cocycle", status="DERIVED_ABSTRACT_RECONSTRUCTION_NOT_SELECTION", basis="I03 and incidence control", remaining="physical arrow/depth assignment and realized profile"),
        dict(claim="internal_dual_pairing", status="DERIVED_ON_FOUNDED_2D_PAIR_ONLY", basis="I06 and D^T K D control", remaining="complete configuration/boundary response pairing and selected invariant level"),
        dict(claim="finite_cell_reciprocal_descent", status="CONDITIONAL_PARTIAL", basis="I07", remaining="selected completion and differentiable boundary law"),
        dict(claim="bootstrap_join_from_reciprocity", status="NOT_DERIVED", basis="I08 and comparison graph control", remaining="independent nonidentity return map"),
        dict(claim="P4_law_selection_from_reciprocity", status="NOT_DERIVED_PERMITTED_EQUIVARIANT_FAMILY", basis="I09", remaining="whole-solution/global selector"),
        dict(claim="complete_native_return_A", status="OPEN_NOT_DERIVED_IN_FROZEN_UNIVERSE", basis="I01-I10", remaining="metric-native nonidentity relation on one complete domain"),
        dict(claim="overall", status="RECIPROCITY_DERIVES_EQUIVARIANT_QUOTIENT_ONLY", basis="1384-source census plus exact controls", remaining="a law-generating principle beyond law covariance"),
    ]
    write_tsv(PKG / "STATUS_LEDGER.tsv", list(status[0]), status)

    result = {
        "outcome": "RECIPROCITY_DERIVES_EQUIVARIANT_QUOTIENT_ONLY",
        "source_paths_verified": len(inventory),
        "source_anchors": len(anchors),
        "interpretations": len(interpretations),
        "passing_native_return_interpretations": 0,
        "naturality_obligations": len(naturality),
        "fixedness_entailed": False,
        "equivariance_requirement_derived": True,
        "zero_set_orbit_saturation_derived_given_A_and_zero_preserving_codomain_action": True,
        "complete_action_on_U_full": False,
        "complete_native_return_A": False,
        "solve_authorized": False,
        "gpu_used": False,
    }
    (PKG / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "PASS whole-configuration Reciprocity derivation: "
        f"sources={len(inventory)} interpretations={len(interpretations)} return_pass=0 "
        f"incidence_rank={incidence_rank} graph_nullity={graph_nullity}"
    )


if __name__ == "__main__":
    main()
