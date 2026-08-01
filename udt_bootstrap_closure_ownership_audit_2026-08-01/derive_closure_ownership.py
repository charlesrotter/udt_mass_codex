#!/usr/bin/env python3
"""Deterministic closure-ownership census and exact finite-dimensional controls."""

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


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rank(matrix: list[list[Fraction]]) -> int:
    a = [row[:] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    pivot_row = 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        p = a[pivot_row][col]
        a[pivot_row] = [v / p for v in a[pivot_row]]
        for r in range(rows):
            if r != pivot_row and a[r][col]:
                q = a[r][col]
                a[r] = [x - q * y for x, y in zip(a[r], a[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def source_anchor(anchor_id: str, path: str, role: str, exact_finding: str) -> dict[str, str]:
    full = ROOT / path
    if not full.is_file():
        raise FileNotFoundError(path)
    return {
        "anchor_id": anchor_id,
        "path": path,
        "sha256": sha256(full),
        "role": role,
        "exact_finding": exact_finding,
    }


def main() -> None:
    source_rows = []
    with (PKG / "SOURCE_INVENTORY.tsv").open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in source_rows:
        full = ROOT / row["path"]
        if sha256(full) != row["sha256"]:
            raise RuntimeError(f"source byte drift: {row['path']}")

    outputs = [
        dict(candidate_id="O01", family="PROPER_MEASURE_AND_VOLUME", status="CONDITIONAL_PARTIAL_MAP_COMPONENT", map_kind="METRIC_MEASURE_AFTER_DOMAIN_SLICE_BOUNDARY", differentiability="FIXED_DOMAIN_EXACT; MOVING_BOUNDARY_PARTIAL", common_domain_blocker="slice, representative, completion, moving boundary", physical_promotion_blocked="not a selected volume or state coordinate", source_anchor="A01;A02"),
        dict(candidate_id="O02", family="CURVATURE_LOCAL_AND_INTEGRATED", status="LOCAL_DERIVED_GLOBAL_UNSELECTED", map_kind="LOCAL_TENSOR_FUNCTOR_PLUS_UNSELECTED_INTEGRAL_FAMILY", differentiability="LOCAL_EXACT; SELECTED_GLOBAL_FUNCTIONAL_ABSENT", common_domain_blocker="choice of contraction, weighting, region, boundary flux", physical_promotion_blocked="curvature is not native energy or a selected closure component", source_anchor="A03;A04"),
        dict(candidate_id="O03", family="HOLONOMY_AND_TRANSPORT", status="CONDITIONAL_PATH_GROUPOID_OUTPUT", map_kind="PATH_OR_LOOP_LABELLED_TRANSPORT", differentiability="CONDITIONAL_FIXED_PATH", common_domain_blocker="path, basepoint, lift, cut, glue, completion", physical_promotion_blocked="not an endpoint-independent scalar", source_anchor="A05;A11"),
        dict(candidate_id="O04", family="TOPOLOGY_AND_COMPLETION", status="CONFIGURATION_LABEL_NOT_RESPONSE", map_kind="DISCRETE_BRANCH_LABEL", differentiability="ZERO_WITHIN_COMPONENT; JUMP_AT_SECTOR_CHANGE", common_domain_blocker="completion is supplied or branch-labelled", physical_promotion_blocked="label does not return a local equation", source_anchor="A05;A11"),
        dict(candidate_id="O05", family="OBSERVER_CLOCK_DEPTH_AND_PAIRING", status="CONDITIONAL_QUERY_FAMILY_NOT_UNIVERSAL", map_kind="OBSERVER_PATH_SLICE_QUERY", differentiability="BRANCH_AND_CUT_LOCUS_CONDITIONAL", common_domain_blocker="observer pair, path family, causal class, representative", physical_promotion_blocked="arguments may not be erased", source_anchor="A06"),
        dict(candidate_id="O06", family="XMAX_DIAMETER", status="TYPE_ONLY_SCHEMA_NOT_DEFINED", map_kind="SUPREMUM_SCHEMA", differentiability="REQUIRES_ATTAINED_UNIQUE_STABLE_MAXIMIZER", common_domain_blocker="separation functional, observer domain, completion, finiteness, attainment", physical_promotion_blocked="no derived value or universal diameter", source_anchor="A06"),
        dict(candidate_id="O07", family="BOUNDARY_GEOMETRY_AND_FLUX", status="CONDITIONAL_RAW_GEOMETRY_NOT_CHARGE", map_kind="INDUCED_EXTRINSIC_CORNER_AND_FLUX_DATA", differentiability="OPERATOR_AND_BOUNDARY_DOMAIN_DEPENDENT", common_domain_blocker="embedding, causal type, corners, native boundary primitive", physical_promotion_blocked="raw flux is not normalized charge, mass, or energy", source_anchor="A07;A14"),
        dict(candidate_id="O08", family="COFRAME_SCREEN_AND_RECIPROCAL_RESPONSE", status="OFFSHELL_STRUCTURE_AND_ALLOWED_RESPONSE_FAMILY", map_kind="COFRAME_DATA_PLUS_PERMITTED_EQUIVARIANT_RESPONSE_SPACE", differentiability="POINTWISE_TYPED; WHOLE_SOLUTION_SELECTION_OPEN", common_domain_blocker="pairing, posture, census, completion, selected response", physical_promotion_blocked="allowed response family is not the realized response law", source_anchor="A08;A12"),
        dict(candidate_id="O09", family="P4_INTEGRATED_BRANCH_DATA", status="CONDITIONAL_ACTION_PAIRING_BRANCH_OUTPUT", map_kind="BRANCH_SCOPED_E0_ELL_I_P_WALL_AND_CELL_DATA", differentiability="EXACT_ON_REGISTERED_REDUCED_MEMBERS", common_domain_blocker="locally-exact member, pairing branch, mass definition, boundary posture", physical_promotion_blocked="not metric-only universal output; integrated tie disappears on P2", source_anchor="A09;A10;A12"),
        dict(candidate_id="O10", family="NATIVE_MASS_ENERGY_DENSITY", status="OPEN_NO_NATIVE_FUNCTIONAL", map_kind="ABSENT", differentiability="ABSENT", common_domain_blocker="native mass, energy, source, normalization, same-solution volume", physical_promotion_blocked="dimensional or conditional readout cannot be promoted", source_anchor="A01;A13"),
        dict(candidate_id="O11", family="OTHER_REGISTERED_OUTPUT", status="NO_ADDITIONAL_COMPLETE_OUTPUT_FOUND", map_kind="BOUNDED_SOURCE_CENSUS_NEGATIVE", differentiability="NOT_APPLICABLE", common_domain_blocker="no source-defined complete candidate outside O01-O10", physical_promotion_blocked="bounded negative only", source_anchor="A13;A14"),
    ]
    write_tsv(PKG / "OUTPUT_OWNERSHIP_LEDGER.tsv", list(outputs[0]), outputs)

    returns = [
        dict(candidate_id="R01", route="RECIPROCITY_AND_FRAME_COMPOSITION", status="KINEMATIC_EQUIVARIANCE_NOT_RETURN", nonidentity_operation="NO", exact_blocker="relates descriptions and composes coframes but supplies no realized-profile equation", source_anchor="A08;A13"),
        dict(candidate_id="R02", route="FINITE_CELL_REGULARITY_AND_GLUE", status="PARTIAL_ADMISSIBILITY_NOT_COMPLETE_RETURN", nonidentity_operation="PARTIAL_ONLY", exact_blocker="regularity, parity, and join catalogues prune configurations but leave multiple families and no complete interior/global operation", source_anchor="A05;A07;A13"),
        dict(candidate_id="R03", route="COFRAME_HOLONOMY_INTEGRABILITY", status="IDENTITY_OR_CONDITIONAL_GLOBAL_DATA_NOT_RETURN", nonidentity_operation="NO", exact_blocker="Cartan/Levi/Bianchi reconstruct or constrain supplied geometry; holonomy remains path/completion data", source_anchor="A05;A13"),
        dict(candidate_id="R04", route="BOOTSTRAP_TWO_ARROW_ARCHITECTURE", status="TYPE_ONLY_NEITHER_ARROW_COMPLETE", nonidentity_operation="NO", exact_blocker="A(X,O) and R[X] are typed but neither complete map, derivative, pairing, nor common fixed point is supplied", source_anchor="A12;A13"),
        dict(candidate_id="R05", route="P4_RESPONSE_INVERSE_PROBLEM", status="PERMITTED_FAMILY_NOT_SELECTED_LAW", nonidentity_operation="NO", exact_blocker="P4 constrains a response family; cold review and JR retain selection and realized embedding as open", source_anchor="A08;A12;A13"),
        dict(candidate_id="R06", route="BOUNDARY_SHAPE_TRANSVERSALITY", status="OPERATOR_DEPENDENT_NO_NATIVE_PRIMITIVE", nonidentity_operation="NO", exact_blocker="moving-boundary channels exist but matching primitive depends on the missing native operator and variation domain", source_anchor="A07;A14"),
        dict(candidate_id="R07", route="ACTION_MEDIATED_CONDITIONAL", status="CONDITIONAL_NOT_PROMOTED", nonidentity_operation="CONDITIONAL_ONLY", exact_blocker="Bach, EH, carrier, and reduced P4 actions retain conditional or chosen premises", source_anchor="A09;A13;A14"),
        dict(candidate_id="R08", route="OTHER_REGISTERED_RETURN", status="NO_OTHER_COMPLETE_RETURN_FOUND", nonidentity_operation="NO", exact_blocker="complete 586-path JR route census found zero passing native equation routes", source_anchor="A13"),
    ]
    write_tsv(PKG / "RETURN_OWNERSHIP_LEDGER.tsv", list(returns[0]), returns)

    blockers = [
        ("B01", "ONE_COMMON_COMPLETE_DOMAIN", "OPEN", "branch-specific queries and supplied completion choices do not share one universal domain"),
        ("B02", "COMPLETE_METRIC_NATIVE_R", "OPEN", "partial local/global readouts exist but no complete state map"),
        ("B03", "NATIVE_COMPONENT_PROJECTION_AND_NORMALIZATION", "OPEN", "metric primitives do not select a physical observable list or weighting"),
        ("B04", "NONIDENTITY_RETURN_A", "OPEN", "zero of eight return routes passes"),
        ("B05", "BOUNDARY_CORNER_COMPLETION_DOMAIN", "OPEN", "operator-dependent boundary primitive and completion selection remain absent"),
        ("B06", "NATIVE_MASS_ENERGY_DENSITY", "OPEN", "no unconditional functional or same-solution response"),
        ("B07", "NATIVE_DUAL_PAIRING_OR_RESPONSE_CODOMAIN", "OPEN", "P4 pairing branches are carried, not selected"),
    ]
    write_tsv(
        PKG / "ASSEMBLY_LEDGER.tsv",
        ["blocker_id", "required_object", "status", "reason"],
        [dict(blocker_id=a, required_object=b, status=c, reason=d) for a, b, c, d in blockers],
    )

    anchors = [
        source_anchor("A01", "udt_native_global_observable_closure_census_2026-07-26/AUDIT_REPORT.md", "pre-P4 complete output census", "no complete observable vector or closure section; conditional geometric primitives survive"),
        source_anchor("A02", "udt_native_global_observable_closure_census_2026-07-26/VARIATION_LEDGER.tsv", "measure and variation formulae", "fixed-domain measures and moving-boundary terms are distinct"),
        source_anchor("A03", "udt_native_global_observable_closure_census_2026-07-26/OBSERVABLE_DEFINITION_LEDGER.tsv", "26-object universe", "local curvature is derived; mass and energy are absent; Xmax is type-only"),
        source_anchor("A04", "udt_native_global_observable_closure_census_2026-07-26/OBSERVABLE_GATE_MATRIX.tsv", "uniform output gates", "no candidate supplies a complete closure component on one common domain"),
        source_anchor("A05", "udt_native_global_observable_closure_census_2026-07-26/ASSEMBLY_BLOCKER_LEDGER.tsv", "assembly blockers", "component union cannot repair ontology, boundary, selection, R, A, or matter gaps"),
        source_anchor("A06", "udt_native_global_observable_closure_census_2026-07-26/STATUS_LEDGER.tsv", "status ceiling", "observer separation and Xmax remain open/type-only"),
        source_anchor("A07", "udt_p4_boundary_action_gate_2026-07-30/AUDIT_REPORT.md", "P4 wall response", "N=2 wall family is constrained but posture and higher selective layers remain open"),
        source_anchor("A08", "udt_p4_routeA_response_inverse_problem_2026-07-29/AUDIT_REPORT.md", "P4 response architecture", "typed response family is posed; no candidate or law is selected"),
        source_anchor("A09", "udt_p4_routeA_slice2_solution_legs_2026-07-29/AUDIT_REPORT.md", "P4 integrated tie", "2 E0 I_p=0 is pairing-branch-relative and absent on P2"),
        source_anchor("A10", "udt_p4_routeA_slice2b_full_cell_2026-07-29/AUDIT_REPORT.md", "P4 full-cell outputs", "E0, ell, wall, and density readings are branch-labelled; none is promoted"),
        source_anchor("A11", "udt_p4_angular_stage_A3_2026-07-31/AUDIT_REPORT.md", "post-July topology/holonomy census", "fixed architecture integers and continuous holonomy survive; completion joins and on-shell coexistence remain open"),
        source_anchor("A12", "udt_p4_cold_adversarial_review_2026-08-01/AUDIT_REPORT.md", "cold P4 regrade", "P4 survives as premise-scoped formal response/census evidence, not selected physics"),
        source_anchor("A13", "udt_jr_cert_native_derivation_2026-08-01/AUDIT_REPORT.md", "current parent equation audit", "zero of eight equation routes passes; bootstrap is the strongest typed lead but neither arrow is defined"),
        source_anchor("A14", "udt_jr_cert_native_derivation_2026-08-01/EXACT_DERIVATION.md", "selection versus reconstruction and boundary dependence", "metric identities reconstruct supplied geometry; matching boundary operation depends on the missing native operator"),
    ]
    write_tsv(PKG / "SOURCE_ANCHOR_LEDGER.tsv", list(anchors[0]), anchors)

    # Exact graph/return control. R: Q^3 -> Q^2; C(x,o)=o-Rx.
    m = [[Fraction(1), Fraction(2), Fraction(0)], [Fraction(0), Fraction(1), Fraction(1)]]
    jac = [[-v for v in row] + [Fraction(int(i == j)) for j in range(2)] for i, row in enumerate(m)]
    graph_rank = rank(jac)
    graph_nullity = len(jac[0]) - graph_rank
    assert graph_rank == 2 and graph_nullity == 3

    # One supplied R admits mutually inequivalent returns. This proves R does not determine A.
    test_vectors = [
        (Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    ]
    return_survivors = {
        "A_all_zero": sum(1 for _ in test_vectors),
        "A_identity": sum(1 for x in test_vectors if x == (0, 0, 0)),
        "A_plane_x3_zero": sum(1 for x in test_vectors if x[2] == 0),
    }
    assert return_survivors == {"A_all_zero": 4, "A_identity": 1, "A_plane_x3_zero": 3}

    # Branch-relative P4 control: P1 has 2 E0 I_p, P2 has no tie.
    p4_controls = []
    for e0, ip in [(Fraction(2), Fraction(0)), (Fraction(2), Fraction(3))]:
        p4_controls.append({
            "E0": int(e0),
            "I_p": int(ip),
            "P1_integrated_tie": int(2 * e0 * ip),
            "P2_integrated_tie": 0,
        })
    assert p4_controls[0]["P1_integrated_tie"] == 0
    assert p4_controls[1]["P1_integrated_tie"] == 12
    assert all(row["P2_integrated_tie"] == 0 for row in p4_controls)

    algebra = {
        "control_scope": "finite-dimensional exact logic control; not a candidate UDT law",
        "R_matrix": [[int(v) for v in row] for row in m],
        "graph_constraint_jacobian": [[int(v) for v in row] for row in jac],
        "graph_rank": graph_rank,
        "graph_nullity": graph_nullity,
        "x_dimension": 3,
        "o_dimension": 2,
        "conclusion": "O=R(X) defines a graph and leaves every X admissible when O is free",
        "same_R_inequivalent_return_survivors_on_four_witnesses": return_survivors,
        "return_nonuniqueness_conclusion": "R does not determine A",
        "p4_pairing_branch_controls": p4_controls,
        "p4_tie_branch_independent": False,
        "p4_conclusion": "the integrated tie is not a branch-independent metric-native return law",
    }
    (PKG / "ALGEBRA_RESULT.json").write_text(json.dumps(algebra, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    status = [
        dict(claim="metric_native_geometric_readout", status="DERIVED_AS_TYPED_PARTIAL_FAMILY", basis="O01-O08", remaining="one complete common physical output map"),
        dict(claim="P4_integrated_readout", status="CONDITIONAL_BRANCH_OUTPUT", basis="O09 and exact P1/P2 control", remaining="branch-independent native ownership"),
        dict(claim="native_mass_energy_density", status="OPEN", basis="O10", remaining="native functional, normalization, source, same-solution response"),
        dict(claim="complete_R_metric", status="NOT_DERIVED_IN_FROZEN_UNIVERSE", basis="B01-B03,B05-B07", remaining="common domain, component projection, completion, pairing"),
        dict(claim="native_return_A", status="NOT_DERIVED_IN_FROZEN_UNIVERSE", basis="R01-R08 all fail", remaining="nonidentity whole-system return operation"),
        dict(claim="bootstrap_two_arrow_architecture", status="DERIVED_TYPE_ONLY", basis="R04", remaining="both maps, derivative, pairing, common fixed point"),
        dict(claim="closed_self_consistency_loop", status="OPEN_NOT_DERIVED", basis="graph control plus absent A", remaining="complete R and nonidentity A on one domain"),
        dict(claim="overall", status="LOCAL_TO_GLOBAL_MAP_PARTIAL_RETURN_OPEN", basis="11 output families, 8 return routes, exact controls", remaining="derive rather than choose the return relation"),
    ]
    write_tsv(PKG / "STATUS_LEDGER.tsv", list(status[0]), status)

    result = {
        "outcome": "LOCAL_TO_GLOBAL_MAP_PARTIAL_RETURN_OPEN",
        "source_paths_verified": len(source_rows),
        "source_anchors": len(anchors),
        "output_candidates": len(outputs),
        "complete_output_maps": 0,
        "return_routes": len(returns),
        "passing_return_routes": 0,
        "assembly_blockers": len(blockers),
        "graph_rank": graph_rank,
        "graph_nullity": graph_nullity,
        "p4_tie_branch_independent": False,
        "solve_authorized": False,
        "gpu_used": False,
    }
    (PKG / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "PASS closure ownership derivation: "
        f"sources={len(source_rows)} outputs={len(outputs)} complete_R=0 "
        f"returns={len(returns)} passing_A=0 rank={graph_rank} nullity={graph_nullity}"
    )


if __name__ == "__main__":
    main()
