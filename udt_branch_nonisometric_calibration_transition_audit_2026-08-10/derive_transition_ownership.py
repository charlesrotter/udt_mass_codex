#!/usr/bin/env python3
"""Classify branch-local transition ownership and verify the path-carried positive control."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PARENT = ROOT / "udt_global_relation_family_branch_classification_2026-08-10/GLOBAL_RELATION_FAMILY_CLASSIFICATION.tsv"
ATLAS = HERE / "TRANSITION_OWNERSHIP_ATLAS.tsv"
RESULT = HERE / "DERIVATION_RESULT.json"

FIELDS = (
    "branch_id", "stable_identity", "parent_disposition", "intrinsic_clock_scale",
    "intrinsic_ruler_or_grading", "owned_geometric_transport", "nonisometric_transition",
    "middle_state_rule", "terminal_reciprocal_status", "degeneracy_or_branch_handling",
    "primary_disposition", "scope_caveat", "evidence",
)


def load(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def controls() -> dict[str, bool]:
    eta = sp.diag(-1, 1, 1, 1)
    x = sp.diag(-1, 1, sp.Rational(1, 2), sp.Rational(1, 2))
    e = sp.diag(sp.Rational(1, 4), 4, 2, 2)  # z=4, lambda=1/2
    u1 = sp.Matrix(
        [
            [sp.Rational(5, 3), 0, sp.Rational(4, 3), 0],
            [0, 1, 0, 0],
            [sp.Rational(4, 3), 0, sp.Rational(5, 3), 0],
            [0, 0, 0, 1],
        ]
    )
    u2 = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, sp.Rational(3, 5), 0, -sp.Rational(4, 5)],
            [0, 0, 1, 0],
            [0, sp.Rational(4, 5), 0, sp.Rational(3, 5)],
        ]
    )
    a1 = u1 * e
    xq = u1 * x * u1.inv()
    eq = u1 * e * u1.inv()
    a2 = u2 * eq
    composite = a2 * a1
    expected = u2 * u1 * e * e
    strain = eta * a1.T * eta * a1
    pair_gram = a1[:, :2].T * eta * a1[:, :2]
    reset = sp.diag(sp.Rational(1, 9), 9, 3, 3)
    reset_composite = u2 * (u1 * reset * u1.inv()) * eq * a1

    clock_only = sp.diag(sp.Rational(1, 4), 1, 1, 1)
    reciprocal_completion = sp.diag(sp.Rational(1, 4), 4, 1, 1)
    clock_pair = clock_only[:, :2].T * eta * clock_only[:, :2]
    reciprocal_pair = reciprocal_completion[:, :2].T * eta * reciprocal_completion[:, :2]

    return {
        "u1_lorentz": u1.T * eta * u1 == eta,
        "u2_lorentz": u2.T * eta * u2 == eta,
        "grading_self_adjoint": eta * x == x.T * eta,
        "carried_grading": xq == u1 * x * u1.inv(),
        "transition_nonisometric": a1.T * eta * a1 != eta,
        "strain_exact": strain == e * e,
        "complete_mixing_present": any(a1[i, j] != 0 for i in (0, 2) for j in (0, 2) if i != j),
        "pair_gram_terminal": pair_gram == sp.diag(-sp.Rational(1, 16), 16),
        "reciprocal_root_multiplier": sp.Rational(1, 16) == sp.Rational(1, 4) ** 2,
        "composition_exact": composite == expected,
        "reversal_exact": a1.inv() * a1 == sp.eye(4),
        "coincidence_identity": u1.inv() * u1 == sp.eye(4),
        "unmatched_reset_changes_composite": reset_composite != composite,
        "clock_only_underdetermines_terminal": clock_pair != reciprocal_pair,
        "clock_factor_matches_both_completions": clock_pair[0, 0] == reciprocal_pair[0, 0],
        "isometric_path_has_identity_strain": eta * u1.T * eta * u1 == sp.eye(4),
    }


def classify(parent: list[dict[str, str]]) -> list[dict[str, str]]:
    expected_ids = [f"R{i:02d}" for i in range(1, 25)]
    assert [row["branch_id"] for row in parent] == expected_ids

    dispositions = {
        "R01": "INSUFFICIENT_TYPED_EVIDENCE", "R02": "INSUFFICIENT_TYPED_EVIDENCE",
        "R03": "INSUFFICIENT_TYPED_EVIDENCE", "R04": "AGGREGATE_MEMBER_DEPENDENT",
        "R05": "INSUFFICIENT_TYPED_EVIDENCE", "R06": "NO_COMPLETE_REGULAR_BRANCH",
        "R07": "INSUFFICIENT_TYPED_EVIDENCE", "R08": "INSUFFICIENT_TYPED_EVIDENCE",
        "R09": "INSUFFICIENT_TYPED_EVIDENCE", "R10": "INSUFFICIENT_TYPED_EVIDENCE",
        "R11": "INSUFFICIENT_TYPED_EVIDENCE", "R12": "HISTORICAL_REDERIVATION_REQUIRED",
        "R13": "CONDITIONAL_QUERY_OR_PRESENTATION_TRANSITION_ONLY",
        "R14": "CONDITIONAL_QUERY_OR_PRESENTATION_TRANSITION_ONLY",
        "R15": "NO_COMPLETE_REGULAR_BRANCH", "R16": "NO_COMPLETE_REGULAR_BRANCH",
        "R17": "COMPLETE_NONISOMETRIC_TRANSITION_OWNED",
        "R18": "PARTIAL_CLOCK_SCALE_TRANSITION_OWNED",
        "R19": "ISOMETRIC_PATH_TRANSPORT_ONLY",
        "R20": "CONDITIONAL_QUERY_OR_PRESENTATION_TRANSITION_ONLY",
        "R21": "NO_COMPLETE_REGULAR_BRANCH",
        "R22": "CONDITIONAL_QUERY_OR_PRESENTATION_TRANSITION_ONLY",
        "R23": "ISOMETRIC_PATH_TRANSPORT_ONLY",
        "R24": "STRATIFIED_PROJECTOR_TRANSPORT_ONLY",
    }

    rows = []
    for source in parent:
        branch_id = source["branch_id"]
        disposition = dispositions[branch_id]
        common = {
            "branch_id": branch_id,
            "stable_identity": source["stable_identity"],
            "parent_disposition": source["primary_disposition"],
            "intrinsic_clock_scale": "UNSUPPLIED",
            "intrinsic_ruler_or_grading": "UNSUPPLIED",
            "owned_geometric_transport": source["transition_or_path_arrow"],
            "nonisometric_transition": "UNSUPPLIED",
            "middle_state_rule": source["middle_state_ownership"],
            "terminal_reciprocal_status": source["scalar_reciprocal_reduction"],
            "degeneracy_or_branch_handling": source["degeneration_handling"],
            "primary_disposition": disposition,
            "scope_caveat": "No stronger transition owner than the parent typed evidence.",
            "evidence": source["evidence"],
        }
        if branch_id == "R04":
            common.update(
                intrinsic_clock_scale="MEMBER_DEPENDENT",
                intrinsic_ruler_or_grading="MEMBER_DEPENDENT",
                nonisometric_transition="R17_PATH_CARRIED_COMPLETE;R18_CLOCK_ONLY;OTHER_MEMBERS_OPEN_OR_ZERO",
                middle_state_rule="MEMBER_DEPENDENT",
                terminal_reciprocal_status="NO_CLASS_WIDE_SCALAR",
                scope_caveat="FC04 is an aggregate; the R17 positive may not be promoted to every member.",
            )
        elif branch_id == "R17":
            common.update(
                intrinsic_clock_scale="KILLING_NORM_N=C_E_EXP_MINUS_PHI__ENDPOINT_RATIO_OWNED",
                intrinsic_ruler_or_grading="GLOBAL_INTRINSIC_PU_PN_H_AND_X_LAMBDA_MINUS_PU_PLUS_PN_PLUS_LAMBDA_H",
                owned_geometric_transport="LEVI_CIVITA_PATH_U_GAMMA_WITH_FULL_AMBIENT_MIXING_AND_HOLONOMY",
                nonisometric_transition="A_GAMMA=U_GAMMA_EXP[DELTA_K(P,Q)X_P]",
                middle_state_rule="TARGET_GRADING_IS_PATH_CARRIED__MATCHED_NEXT_LEG_STARTS_FROM_THAT_STATE",
                terminal_reciprocal_status="DELTA_RF=PHI_PAIR=DELTA_K_ON_CARRIED_FLAG_RESTRICTION",
                degeneracy_or_branch_handling="C01_C06_REGULAR;PATH_LABELS_RETAINED;LOOPS_RETURN_HOLONOMY;RESET_TO_INTRINSIC_ENDPOINT_REQUIRES_OPEN_M_B",
                scope_caveat="Complete only on the named off-shell C01-C06 path-carried enriched-state groupoid; no physical path selection or rebuild rule.",
                evidence="udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/EXACT_DERIVATION.md;udt_finite_cell_reciprocal_quotient_reduction_audit_2026-07-27/EXACT_DERIVATION.md;udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/EXACT_DERIVATION.md",
            )
        elif branch_id == "R18":
            common.update(
                intrinsic_clock_scale="UNIQUE_KILLING_NORM_ENDPOINT_RATIO_OWNED",
                intrinsic_ruler_or_grading="NO_SAME_BRANCH_INTRINSIC_RULER",
                nonisometric_transition="CLOCK_LINE_SCALE_ONLY",
                middle_state_rule="ONE_SHARED_KILLING_CLOCK_STATE",
                terminal_reciprocal_status="UNDERDETERMINED_UNTIL_RULER_SCALE_OR_TL_EQUAL_1_IS_OWNED",
                scope_caveat="A genuine non-isometric clock transition, not a complete reciprocal pair transition.",
            )
        elif branch_id in {"R19", "R23"}:
            common.update(
                intrinsic_clock_scale="ZERO_OR_NO_OWNED_NONTRIVIAL_SCALE",
                intrinsic_ruler_or_grading="CONDITIONAL_OR_PATH_CARRIED_ONLY",
                nonisometric_transition="NONE__OWNED_PATH_ARROW_IS_METRIC_COMPATIBLE",
                terminal_reciprocal_status="ZERO_CONTROL_OR_OPEN",
                scope_caveat="Path composition and holonomy survive, but every owned linear transport is isometric.",
            )
        elif branch_id == "R24":
            common.update(
                intrinsic_clock_scale="NONE",
                intrinsic_ruler_or_grading="UNORDERED_SHORTEST_LINE_SET",
                nonisometric_transition="NONE__SET_EQUIVARIANT_PROJECTOR_TRANSPORT_ONLY",
                middle_state_rule="SET_OWNED_SINGLE_MEMBER_UNOWNED_AT_TIE",
                terminal_reciprocal_status="NOT_TYPED",
                scope_caveat="Projector transport supplies no clock/ruler density scale.",
            )
        elif disposition == "CONDITIONAL_QUERY_OR_PRESENTATION_TRANSITION_ONLY":
            common.update(
                nonisometric_transition="AVAILABLE_ONLY_AFTER_UNOWNED_QUERY_LINE_OR_PRESENTATION_CHOICE",
                terminal_reciprocal_status="CONDITIONAL_OR_OPEN",
                scope_caveat="The branch does not own the extra query, direction, or selected line needed for a complete transition.",
            )
        rows.append(common)

    validate(rows, parent)
    return rows


def validate(rows: list[dict[str, str]], parent: list[dict[str, str]]) -> None:
    assert len(rows) == len({row["branch_id"] for row in rows}) == 24
    assert [row["branch_id"] for row in rows] == [row["branch_id"] for row in parent]
    assert [row["stable_identity"] for row in rows] == [row["stable_identity"] for row in parent]
    by_id = {row["branch_id"]: row for row in rows}
    positive = [row for row in rows if row["primary_disposition"] == "COMPLETE_NONISOMETRIC_TRANSITION_OWNED"]
    assert len(positive) == 1 and positive[0]["branch_id"] == "R17"
    assert "A_GAMMA=U_GAMMA_EXP" in by_id["R17"]["nonisometric_transition"]
    assert "GLOBAL_INTRINSIC_PU_PN_H" in by_id["R17"]["intrinsic_ruler_or_grading"]
    assert "KILLING_NORM" in by_id["R17"]["intrinsic_clock_scale"]
    assert "PATH_CARRIED" in by_id["R17"]["middle_state_rule"]
    assert "OPEN_M_B" in by_id["R17"]["degeneracy_or_branch_handling"]
    assert "no physical path selection" in by_id["R17"]["scope_caveat"]
    assert by_id["R18"]["primary_disposition"] == "PARTIAL_CLOCK_SCALE_TRANSITION_OWNED"
    assert "NO_SAME_BRANCH_INTRINSIC_RULER" in by_id["R18"]["intrinsic_ruler_or_grading"]
    assert by_id["R23"]["primary_disposition"] == "ISOMETRIC_PATH_TRANSPORT_ONLY"
    assert by_id["R24"]["primary_disposition"] == "STRATIFIED_PROJECTOR_TRANSPORT_ONLY"
    assert by_id["R12"]["primary_disposition"] == "HISTORICAL_REDERIVATION_REQUIRED"
    assert all("kernel_plane_global_curvature" not in row["evidence"] for row in rows)
    assert all("PHYSICAL_RELATION_SELECTED" not in row["terminal_reciprocal_status"] for row in rows)


def main() -> None:
    checks = controls()
    assert all(checks.values()), [name for name, ok in checks.items() if not ok]
    rows = classify(load(PARENT))
    with ATLAS.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    for row in rows:
        key = row["primary_disposition"]
        counts[key] = counts.get(key, 0) + 1
    result = {
        "schema": "udt-branch-nonisometric-transition-v1",
        "status": "PASS",
        "branch_count": len(rows),
        "disposition_counts": counts,
        "exact_checks": checks,
        "atlas_sha256": hashlib.sha256(ATLAS.read_bytes()).hexdigest(),
        "positive_branch": "R17_W01_TWISTED_RECIPROCAL_S3_C01_C06_PATH_CARRIED",
        "physical_selection": "OPEN",
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {len(rows)} branches; {len(checks)}/{len(checks)} exact controls")
    print(result["atlas_sha256"])


if __name__ == "__main__":
    main()
