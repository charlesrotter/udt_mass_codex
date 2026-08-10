#!/usr/bin/env python3
"""Exact production derivation for the non-isometric magnitude-owner audit."""

from __future__ import annotations

import csv
import argparse
import io
import json
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ETA = sp.diag(-1, 1, 1, 1)

FAMILIES = (
    ("F01_PAIR_SURFACE_JACOBIAN", "pair_surface_jacobian"),
    ("F02_ENDPOINT_STATIONARY_CLOCK", "endpoint_stationary_clock"),
    ("F03_PATH_GLOBAL_COMPLETION", "path_global_completion"),
    ("F04_NATIVE_DYNAMICAL_BOOTSTRAP", "native_dynamical_bootstrap"),
    ("F05_NO_CURRENT_KINEMATIC_OWNER", "no_current_kinematic_owner"),
)

UNTYPED = {
    "INSUFFICIENT_TYPED_EVIDENCE",
    "NO_COMPLETE_REGULAR_BRANCH",
    "HISTORICAL_REDERIVATION_REQUIRED",
}


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def render_tsv(rows: list[dict[str, str]]) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def gram(columns: sp.Matrix) -> sp.Matrix:
    return sp.simplify(columns.T * ETA * columns)


def density_arguments(arrow: sp.Matrix, flag: sp.Matrix) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    source = gram(flag)
    target = gram(arrow * flag)
    rho1 = sp.simplify(sp.Abs(target[0, 0]) / sp.Abs(source[0, 0]))
    rho2 = sp.simplify(sp.Abs(target.det()) / sp.Abs(source.det()))
    return rho1, rho2, sp.simplify(rho2 / rho1**2)


def make_row(branch: dict[str, str], transition: dict[str, str], family_id: str, family: str) -> dict[str, str]:
    branch_id = branch["branch_id"]
    identity = branch["stable_identity"]
    parent = transition["primary_disposition"]
    evidence = (
        "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/"
        f"TRANSITION_OWNERSHIP_ATLAS.tsv::{branch_id}"
    )

    base = {
        "branch_id": branch_id,
        "stable_identity": identity,
        "family_id": family_id,
        "family": family,
        "existence_gate": "NOT_APPLICABLE",
        "nonisometry_gate": "NOT_APPLICABLE",
        "typing_gate": "NOT_APPLICABLE",
        "composition_gate": "NOT_APPLICABLE",
        "gauge_descent_gate": "NOT_APPLICABLE",
        "branch_ownership_gate": "NOT_APPLICABLE",
        "terminal_compatibility_gate": "NOT_APPLICABLE",
        "disposition": "UNSET",
        "reason": "",
        "evidence": evidence,
    }

    if family_id == "F04_NATIVE_DYNAMICAL_BOOTSTRAP":
        base.update(
            existence_gate="FAIL_NO_FROZEN_NATIVE_LAW",
            nonisometry_gate="OPEN",
            typing_gate="OPEN_VARIATION_AND_STATE_OWNER",
            composition_gate="OPEN",
            gauge_descent_gate="OPEN",
            branch_ownership_gate="FAIL_NOT_IN_CURRENT_KINEMATIC_FOUNDATION",
            terminal_compatibility_gate="OPEN",
            disposition="BLOCKED_MISSING_DYNAMIC_LAW",
            reason="No frozen native dynamics or bootstrap return supplies a calibration-line magnitude; none is invented.",
            evidence="CURRENT_SCIENTIFIC_PREMISES.tsv::G44",
        )
        return base

    if family_id == "F05_NO_CURRENT_KINEMATIC_OWNER":
        partial = branch_id in {"R17", "R18"}
        base.update(
            existence_gate="SUPPORTED_BY_COMPLETE_F01_F04_CENSUS",
            nonisometry_gate="PARTIAL_CLOCK_MAGNITUDE_EXISTS" if partial else "NO_COMPLETE_NONZERO_OWNER",
            typing_gate="NO_COMPLETE_PHYSICAL_PAIR_OWNER",
            composition_gate="PARTIAL_ONLY" if partial else "UNOWNED_OR_ZERO",
            gauge_descent_gate="SUPPLIED_READOUT_DESCENT_ONLY",
            branch_ownership_gate="NO_COMPLETE_OWNER_IN_CURRENT_RECORD",
            terminal_compatibility_gate="OPEN",
            disposition="SUPPORTED_NO_COMPLETE_PHYSICAL_OWNER",
            reason=(
                "The branch owns a partial endpoint clock magnitude but not the selected complete reciprocal comparison."
                if partial
                else "No family in the current frozen kinematic record owns a complete physical non-isometric magnitude on this identity."
            ),
            evidence="udt_reciprocal_scalar_calibration_bitorsor_descent_audit_2026-08-10/AUDIT_REPORT.md",
        )
        return base

    if parent in UNTYPED:
        base.update(
            existence_gate="FAIL_NO_COMPLETE_TYPED_BRANCH",
            nonisometry_gate="UNTESTABLE",
            typing_gate="FAIL",
            composition_gate="UNTESTABLE",
            gauge_descent_gate="UNTESTABLE",
            branch_ownership_gate="FAIL_CURRENT_EVIDENCE_INSUFFICIENT",
            terminal_compatibility_gate="OPEN",
            disposition="INSUFFICIENT_TYPED_EVIDENCE",
            reason=f"Parent branch status is {parent}; a schema or incomplete branch cannot own the audited magnitude.",
            evidence=(
                "udt_global_relation_family_branch_classification_2026-08-10/"
                f"GLOBAL_RELATION_FAMILY_CLASSIFICATION.tsv::{branch_id}"
            ),
        )
        return base

    if parent == "AGGREGATE_MEMBER_DEPENDENT":
        base.update(
            existence_gate="MEMBER_DEPENDENT",
            nonisometry_gate="MEMBER_DEPENDENT",
            typing_gate="MEMBER_DEPENDENT",
            composition_gate="MEMBER_DEPENDENT",
            gauge_descent_gate="MEMBER_DEPENDENT",
            branch_ownership_gate="FAIL_CLASS_AGGREGATE_NOT_ONE_BRANCH",
            terminal_compatibility_gate="MEMBER_DEPENDENT",
            disposition="AGGREGATE_MEMBER_DEPENDENT",
            reason="FC04 contains R17, R18, zero, open, and degenerate members and owns no class-wide magnitude.",
            evidence=(
                "udt_global_relation_family_branch_classification_2026-08-10/"
                f"GLOBAL_RELATION_FAMILY_CLASSIFICATION.tsv::{branch_id}"
            ),
        )
        return base

    if family_id == "F01_PAIR_SURFACE_JACOBIAN":
        base.update(
            existence_gate="CONDITIONAL_AFTER_COMPLETE_QUERY",
            nonisometry_gate="PASS_ON_SUPPLIED_NONISOMETRIC_JACOBIAN",
            typing_gate="FAIL_PHYSICAL_QUERY_OR_PAIR_SURFACE_UNOWNED",
            composition_gate="OPEN_MIDDLE_PAIR_FUNCTOR",
            gauge_descent_gate="PASS_ON_SUPPLIED_REGULAR_PAIR",
            branch_ownership_gate="FAIL_QUERY_NOT_BRANCH_OWNED",
            terminal_compatibility_gate="PASS_ON_SUPPLIED_NORMALIZED_PAIR",
            disposition="BLOCKED_MISSING_PHYSICAL_QUERY",
            reason="A supplied lawful pair Jacobian can generate the magnitude, but no current branch selects the physical query, surface, or middle carry.",
            evidence="udt_calibrated_pair_map_owner_atlas_2026-08-09/AUDIT_REPORT.md",
        )
        return base

    if family_id == "F02_ENDPOINT_STATIONARY_CLOCK":
        if branch_id == "R17":
            base.update(
                existence_gate="PASS_INTRINSIC_KILLING_NORM_RATIO",
                nonisometry_gate="PASS_NONZERO_ENDPOINT_CLOCK_SCALE",
                typing_gate="PARTIAL_CLOCK_MAGNITUDE_PLUS_INTRINSIC_GRADING",
                composition_gate="PASS_ENDPOINT_COBBOUNDARY",
                gauge_descent_gate="PASS_CONSTANT_K_RESCALING_CANCELS",
                branch_ownership_gate="PASS_MAGNITUDE_ONLY__ASSEMBLY_UNSELECTED",
                terminal_compatibility_gate="CONDITIONAL_ON_UNSELECTED_R17_LIFT",
                disposition="OWNER_CONDITIONAL_BRANCH_ONLY",
                reason="W01 owns delta_K and the reciprocal grading separately; applying the magnitude as the physical non-isometric lift remains unselected.",
            )
        elif branch_id == "R18":
            base.update(
                existence_gate="PASS_UNIQUE_KILLING_NORM_RATIO",
                nonisometry_gate="PASS_NONZERO_ENDPOINT_CLOCK_SCALE",
                typing_gate="PARTIAL_CLOCK_LINE_ONLY",
                composition_gate="PASS_ENDPOINT_COBBOUNDARY",
                gauge_descent_gate="PASS_CONSTANT_K_RESCALING_CANCELS",
                branch_ownership_gate="PASS_CLOCK_MAGNITUDE_ONLY",
                terminal_compatibility_gate="FAIL_RULER_OR_TL_EQUAL_1_UNOWNED",
                disposition="OWNER_CONDITIONAL_BRANCH_ONLY",
                reason="W02 owns one non-isometric clock magnitude, but no intrinsic ruler scale completes the reciprocal terminal readout.",
            )
        elif branch_id == "R19":
            base.update(
                existence_gate="PASS_GLOBAL_ZERO_CLOCK_CONTROL",
                nonisometry_gate="FAIL_ZERO_MAGNITUDE",
                typing_gate="CLOCK_ONLY",
                composition_gate="PASS_TRIVIAL",
                gauge_descent_gate="PASS",
                branch_ownership_gate="PASS_ZERO_CONTROL_ONLY",
                terminal_compatibility_gate="ZERO_OR_OPEN",
                disposition="TRANSPORT_OR_READOUT_ONLY",
                reason="The ultrastatic branch owns only the zero clock response.",
            )
        elif branch_id == "R20":
            base.update(
                existence_gate="PASS_MULTIPLE_KILLING_LINES",
                nonisometry_gate="POSSIBLE_PER_CHOICE",
                typing_gate="FAIL_NO_UNIQUE_CLOCK_LINE",
                composition_gate="PASS_PER_CHOICE",
                gauge_descent_gate="PASS_PER_CHOICE",
                branch_ownership_gate="FAIL_BRANCH_SELECTS_NONE",
                terminal_compatibility_gate="CHOICE_DEPENDENT",
                disposition="BLOCKED_NONUNIQUE_INTRINSIC_CLOCK",
                reason="Enhanced symmetry supplies several clock candidates and no metric-owned selection.",
            )
        elif branch_id == "R22":
            base.update(
                existence_gate="CONDITIONAL_SUPPLIED_CLOCK_PRESENTATION",
                nonisometry_gate="POSSIBLE",
                typing_gate="FAIL_PRESENTATION_NOT_METRIC_SELECTED",
                composition_gate="PASS_AFTER_CHOICE",
                gauge_descent_gate="CONDITIONAL",
                branch_ownership_gate="FAIL_UNOWNED_PRESENTATION",
                terminal_compatibility_gate="CLOCK_ONLY",
                disposition="BLOCKED_MISSING_PHYSICAL_QUERY",
                reason="W06 has a supplied nonconstant clock presentation, not a metric-selected calibration owner.",
            )
        else:
            base.update(
                existence_gate="FAIL_NO_OWNED_NONZERO_UNIQUE_CLOCK_SCALE",
                nonisometry_gate="FAIL_OR_OPEN",
                typing_gate="OPEN_OR_PROJECTOR_ONLY",
                composition_gate="OPEN",
                gauge_descent_gate="OPEN",
                branch_ownership_gate="FAIL",
                terminal_compatibility_gate="OPEN",
                disposition="NO_OWNED_NONZERO_CLOCK_SCALE",
                reason="The branch owns no unique nonzero stationary clock calibration magnitude.",
            )
        base["evidence"] = (
            "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/"
            f"EXACT_DERIVATION.md::{branch_id}"
        )
        return base

    if family_id == "F03_PATH_GLOBAL_COMPLETION":
        if branch_id in {"R17", "R19", "R23", "R24"}:
            base.update(
                existence_gate="PASS_OWNED_PATH_OR_SET_TRANSPORT",
                nonisometry_gate="FAIL_ISOMETRIC_OR_PROJECTOR_ONLY",
                typing_gate="PASS_GEOMETRIC_TRANSPORT_ONLY",
                composition_gate="PASS_PATH_OR_SET_EQUIVARIANT",
                gauge_descent_gate="PASS_WITH_PATH_LABELS_RETAINED",
                branch_ownership_gate="PASS_TRANSPORT_NOT_MAGNITUDE",
                terminal_compatibility_gate="ZERO_OR_NOT_TYPED",
                disposition="TRANSPORT_OR_READOUT_ONLY",
                reason="Owned path/holonomy or projector transport composes but generates no reciprocal density magnitude.",
            )
        elif branch_id == "R18":
            base.update(
                existence_gate="PASS_ENDPOINT_GLOBAL_CLOCK_STATE",
                nonisometry_gate="HANDLED_ONLY_BY_F02_CLOCK_RATIO",
                typing_gate="CLOCK_ONLY",
                composition_gate="PASS_ENDPOINT_COBBOUNDARY",
                gauge_descent_gate="PASS",
                branch_ownership_gate="NO_ADDITIONAL_PATH_MAGNITUDE_OWNER",
                terminal_compatibility_gate="RULER_OPEN",
                disposition="TRANSPORT_OR_READOUT_ONLY",
                reason="Global completion supplies the shared clock state already classified in F02, not a complete path-generated reciprocal magnitude.",
            )
        else:
            base.update(
                existence_gate="CONDITIONAL_AFTER_QUERY_OR_CHOICE",
                nonisometry_gate="FAIL_OWNED_TRANSPORT_IS_ISOMETRIC_OR_UNSUPPLIED",
                typing_gate="FAIL_QUERY_PATH_OR_STATE_UNOWNED",
                composition_gate="CONDITIONAL",
                gauge_descent_gate="CONDITIONAL",
                branch_ownership_gate="FAIL",
                terminal_compatibility_gate="OPEN",
                disposition="BLOCKED_MISSING_PHYSICAL_QUERY",
                reason="Any path/global magnitude needs an unowned path, line, lift, or calibration state; metric-compatible transport itself is isometric.",
            )
        base["evidence"] = (
            "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/"
            f"TRANSITION_OWNERSHIP_ATLAS.tsv::{branch_id};"
            "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27/LOOP_HOLONOMY.tsv"
        )
        return base

    raise AssertionError(family_id)


def exact_algebra() -> dict[str, object]:
    np_, nq, nr, scale = sp.symbols("N_p N_q N_r a", positive=True)
    ratio_pq = np_ / nq
    ratio_qr = nq / nr
    assert sp.simplify(ratio_pq * ratio_qr - np_ / nr) == 0
    assert sp.simplify((scale * np_) / (scale * nq) - ratio_pq) == 0

    # Same clock density, inequivalent ruler completion: the clock magnitude does not fix phi_pair.
    h_complete = sp.diag(-sp.Rational(1, 4), 4)
    h_incomplete = sp.diag(-sp.Rational(1, 4), 1)
    arg_complete = sp.simplify(-h_complete.det() / h_complete[0, 0] ** 2)
    arg_incomplete = sp.simplify(-h_incomplete.det() / h_incomplete[0, 0] ** 2)
    assert arg_complete == 16 and arg_incomplete == 4 and arg_complete != arg_incomplete

    flag = sp.Matrix.hstack(sp.eye(4)[:, 0], sp.eye(4)[:, 1])
    dilation = sp.diag(sp.Rational(1, 2), 2, 1, 1)
    boost = sp.eye(4)
    boost[0, 0] = boost[2, 2] = sp.Rational(5, 4)
    boost[0, 2] = boost[2, 0] = sp.Rational(3, 4)
    assert sp.simplify(boost.T * ETA * boost - ETA) == sp.zeros(4)
    assert density_arguments(boost, flag) == (1, 1, 1)
    assert density_arguments(dilation, flag) == (sp.Rational(1, 4), 1, 16)
    assert density_arguments(boost * dilation, flag) == (sp.Rational(1, 4), 1, 16)

    mixed = sp.Matrix(
        [[sp.Rational(1, 2), 0, 0, 0], [0, 2, 0, 0], [sp.Rational(1, 4), 0, 1, 0], [0, 0, 0, 1]]
    )
    assert density_arguments(mixed, flag) == (sp.Rational(3, 16), sp.Rational(3, 4), sp.Rational(64, 3))

    return {
        "endpoint_clock_multiplier_telescopes": True,
        "constant_killing_rescaling_cancels": True,
        "same_clock_two_terminal_arguments": [str(arg_complete), str(arg_incomplete)],
        "isometric_transport_density_arguments": ["1", "1", "1"],
        "conditional_reciprocal_lift_density_arguments": ["1/4", "1", "16"],
        "complete_mixed_supplied_jacobian_density_arguments": ["3/16", "3/4", "64/3"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="recompute entirely in memory and compare with cached outputs without writing",
    )
    args = parser.parse_args()
    branches = table(ROOT / "udt_global_relation_family_branch_classification_2026-08-10/BRANCH_UNIVERSE.tsv")
    transitions = {
        row["branch_id"]: row
        for row in table(ROOT / "udt_branch_nonisometric_calibration_transition_audit_2026-08-10/TRANSITION_OWNERSHIP_ATLAS.tsv")
    }
    assert len(branches) == len(transitions) == 24
    assert [row["branch_id"] for row in branches] == [f"R{i:02d}" for i in range(1, 25)]

    rows = [make_row(branch, transitions[branch["branch_id"]], family_id, family) for branch in branches for family_id, family in FAMILIES]
    assert len(rows) == 120
    assert len({(row["branch_id"], row["family_id"]) for row in rows}) == 120
    conditional = [
        row for row in rows
        if row["family_id"] == "F02_ENDPOINT_STATIONARY_CLOCK" and row["disposition"] == "OWNER_CONDITIONAL_BRANCH_ONLY"
    ]
    assert [row["branch_id"] for row in conditional] == ["R17", "R18"]
    assert not any(row["disposition"] == "OWNER_DERIVED" for row in rows)
    assert all(
        row["disposition"] == "BLOCKED_MISSING_DYNAMIC_LAW"
        for row in rows if row["family_id"] == "F04_NATIVE_DYNAMICAL_BOOTSTRAP"
    )
    assert all(
        row["disposition"] == "SUPPORTED_NO_COMPLETE_PHYSICAL_OWNER"
        for row in rows if row["family_id"] == "F05_NO_CURRENT_KINEMATIC_OWNER"
    )

    branch_summary = []
    for branch in branches:
        branch_rows = [row for row in rows if row["branch_id"] == branch["branch_id"]]
        partial = [row["family_id"] for row in branch_rows if row["disposition"] == "OWNER_CONDITIONAL_BRANCH_ONLY"]
        branch_summary.append(
            {
                "branch_id": branch["branch_id"],
                "stable_identity": branch["stable_identity"],
                "conditional_magnitude_owner_families": ";".join(partial) if partial else "NONE",
                "complete_physical_magnitude_owner": "NONE",
                "remaining_joint": (
                    "SELECT_RECIPROCAL_LIFT_AND_PAIR_SURFACE" if branch["branch_id"] == "R17"
                    else "DERIVE_INTRINSIC_RULER_OR_RECIPROCAL_COMPLETION" if branch["branch_id"] == "R18"
                    else "NO_CURRENT_COMPLETE_OWNER"
                ),
            }
        )
    algebra = exact_algebra()
    dispositions = Counter(row["disposition"] for row in rows)
    result = {
        "primary_landing": "BRANCH_CONDITIONAL_MAGNITUDE_OWNER_ONLY__NO_UNIVERSAL_OWNER",
        "branch_identities": len(branches),
        "families": len(FAMILIES),
        "atlas_cells": len(rows),
        "conditional_owner_branches": ["R17", "R18"],
        "complete_physical_owner_branches": [],
        "disposition_counts": dict(sorted(dispositions.items())),
        "algebra": algebra,
        "owned": [
            "R17 endpoint Killing-norm magnitude delta_K",
            "R18 unique-Killing endpoint clock magnitude delta_K",
            "exact endpoint multiplier telescoping and constant Killing rescaling invariance",
        ],
        "open": [
            "R17 branch selection of the reciprocal non-isometric lift and physical pair surface",
            "R18 intrinsic ruler scale or TL=1 reciprocal completion",
            "physical pair query and middle carry on every branch",
            "native dynamical or bootstrap calibration return",
            "universal mixed-geometry c_eff",
        ],
    }
    outputs = {
        "MAGNITUDE_OWNER_ATLAS.tsv": render_tsv(rows),
        "BRANCH_OWNER_SUMMARY.tsv": render_tsv(branch_summary),
        "DERIVATION_RESULT.json": json.dumps(result, indent=2, sort_keys=True) + "\n",
    }
    if args.check:
        for name, expected in outputs.items():
            assert (HERE / name).read_text(encoding="utf-8") == expected, name
    else:
        for name, content in outputs.items():
            (HERE / name).write_text(content, encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
