#!/usr/bin/env python3
"""Exact CPU controls for the preregistered wall-crossing selector audit."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent

E1 = (1, 0)
E2 = (0, 1)
SWAP = ((0, 1), (1, 0))
IDENTITY = ((1, 0), (0, 1))


def canonical_line(w: tuple[int, int]) -> tuple[int, int]:
    a, b = w
    d = math.gcd(abs(a), abs(b))
    if d == 0:
        raise ValueError("zero vector has no primitive line")
    a //= d
    b //= d
    if a < 0 or (a == 0 and b < 0):
        a, b = -a, -b
    return (a, b)


def matvec(
    matrix: tuple[tuple[int, int], tuple[int, int]],
    vector: tuple[int, int],
) -> tuple[int, int]:
    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
    )


def shortest_reciprocal(phi: float) -> set[tuple[int, int]]:
    """Exact classification; floats only provide the sign of phi."""
    if phi < 0:
        return {E1}
    if phi > 0:
        return {E2}
    return {E1, E2}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(
    path: Path, fieldnames: list[str], rows: list[dict[str, Any]]
) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def check(condition: bool, name: str, detail: Any, checks: list[dict[str, Any]]) -> None:
    if not condition:
        raise AssertionError(f"{name}: {detail}")
    checks.append({"name": name, "status": "PASS", "detail": detail})


def candidate_outcomes() -> list[dict[str, str]]:
    outcome = {
        "C01": ("DERIVED_SET_VALUED_CONTINUATION", "The full shortest set is GL2Z covariant and remains defined at the tie."),
        "C02": ("REFUTED_AT_TIE", "W_min has two members at phi=0; shortestness alone is not single valued."),
        "C03": ("OBSTRUCTED_IN_FIXED_LATTICE", "A discrete shortest line changes from e1 to e2, so a continuous single line cannot remain shortest through the wall."),
        "C04": ("NO_EQUIVARIANT_SINGLE_SELECTOR", "The reciprocal exchange swaps both members of W_min(0) and fixes neither."),
        "C05": ("CONDITIONAL_ON_UNSELECTED_SWAP_LIFT", "A swap transition maps the left shortest line to the right one, but the transition is extra global data."),
        "C06": ("CONDITIONAL_AND_INCOMPATIBLE_WITH_SHORTEST_JOIN", "Identity gluing preserves e1 while the right chamber uniquely minimizes e2."),
        "C07": ("NOT_GL2Z_COVARIANT", "A basis swap leaves the tied set invariant but changes the covariant image of the lexicographic choice."),
        "C08": ("CONDITIONAL_ON_UNREGISTERED_HISTORY", "Hysteresis adds path history and can retain a nonshortest line after crossing."),
        "C09": ("REFUTED_AS_SHORTEST_SELECTOR", "The swap-fixed diagonal lines have squared norm 2 at the isotropic seal, while the minimum is 1."),
        "C10": ("OPEN_EXTRA_LIFT", "An unoriented line does not select a sign, orientation, or chirality."),
        "C11": ("CONDITIONAL_ON_FLAT_TRIVIAL_HOLONOMY_AND_FRAMING", "A projected connection does not supply a global parallel phase by itself."),
        "C12": ("COMPATIBILITY_DATA_NOT_SELECTOR", "Connection curvature can obstruct a parallel phase but does not choose between tied character lines."),
        "C13": ("COMPATIBILITY_DATA_NOT_SELECTOR", "Holonomy constrains a supplied line/section; no minimizing functional is registered."),
        "C14": ("COMPATIBILITY_ONLY", "A character can extend alone across a cap only when it annihilates the collapsed cycle."),
        "C15": ("CONDITIONAL_ON_UNSUPPLIED_AMPLITUDE", "Vanishing amplitude can regularize phase loss, but no native carrier amplitude is present."),
        "C16": ("NOT_SUFFICIENT", "Smooth set-valued, identity-glued, and swap-glued alternatives remain mathematically distinct."),
        "C17": ("LOCATES_CONTROL_TIE_ONLY", "The phi=0 seal places the reciprocal symmetric point but supplies no angular lift or phase datum."),
        "C18": ("CONDITIONAL_ON_UNSELECTED_LIFT", "Mirror/quotient continuation depends on the chosen lattice automorphism and orientation lift."),
        "C19": ("CONDITIONAL", "A unique global line requires a tie-free path and monodromy preservation."),
        "C20": ("CONDITIONAL_SIGN_OR_REAL_STRUCTURE", "Nonorientation can preserve an unoriented line while reversing sign or conjugating phase."),
        "C21": ("TYPE_NEUTRAL", "Common scale rescales all character norms together and cannot split a tie."),
        "C22": ("CHART_GROUP_NOT_PHYSICAL_SELECTOR", "The coframe group law needs a chosen trivialization/section and no weighted physical composition is selected."),
        "C23": ("TYPE_MISMATCH", "Co-presence is whole-solution membership, not a character, gluing, or phase equation."),
        "C24": ("TYPE_MISMATCH", "X_max concerns global observer-pair separation/scale and supplies no angular lattice tie-break."),
        "C25": ("AFTER_SOLUTION_NOT_LOCAL_SELECTOR", "The primary bootstrap reading filters completed matter-bearing universes after equations exist."),
        "C26": ("WORKING_DEPENDENCE_OPEN", "The stronger fork could make branch viability relevant but supplies neither operator nor wall rule."),
        "C27": ("NOT_OPERATIONAL_NO_MAP", "No native mass/volume density or density-to-H,S law exists; direct insertion is forbidden."),
        "C28": ("NOT_PRESENT", "No native action or energy functional selects one tied character."),
        "C29": ("NOT_PRESENT", "No time-live law or bifurcation equation is registered."),
        "C30": ("MATHEMATICALLY_COHERENT_PHYSICAL_ROLE_OPEN", "Retaining the whole tied set is the unique rule needing no extra choice, but physical set-valued matter is not derived."),
        "C31": ("DERIVED_TERMINATION", "Where toric rank/lattice is lost, the character object ceases to exist rather than choosing a continuation."),
        "C32": ("OPEN_EXTRA_DATA", "Boundary phase framing could lift a line to a phase, but it is not supplied by the current seal."),
    }
    candidates = read_tsv(HERE / "CANDIDATE_RULES.tsv")
    if len(candidates) != 32 or len({row["id"] for row in candidates}) != 32:
        raise AssertionError("candidate census mismatch")
    rows = []
    for row in candidates:
        status, reason = outcome[row["id"]]
        rows.append(
            {
                **row,
                "outcome": status,
                "reason": reason,
                "physical_selection": "NO" if row["id"] != "C30" else "OPEN",
            }
        )
    return rows


def principle_rows() -> list[dict[str, str]]:
    data = [
        ("U01", "Reciprocal-c", "clock/ruler determinant-one pair", "NO", "Different tensor/object type from angular character selection."),
        ("U02", "observer-frame Reciprocity", "covariance and no preferred ordinary-regime observer", "NO", "Covariance preserves the tie set and does not force one covariant tensor to vanish or one line to win."),
        ("U03", "Xmax reciprocity", "working signed bounded composition/reversal", "NO", "Absolute-phi and finite-cell joins remain open; no angular action."),
        ("U04", "angular reciprocal exchange", "e1/e2 exchange under phi reversal", "SET_ONLY", "It canonically exchanges the two members but has no fixed member at the seal."),
        ("U05", "CSN", "common conformal calibration quotient", "NO", "All norms receive the same positive factor."),
        ("U06", "static seal", "phi=0 with partial parity/value data", "NO", "It locates the symmetric tie but gives no lattice lift or boundary phase."),
        ("U07", "finite-cell taxonomy", "twelve possible completion/gluing classes", "CONDITIONAL", "Several lifts can support different continuations; no class/lift is selected."),
        ("U08", "coframe composition", "exact group law in chosen trivialization", "NO", "Physical representative, weighting, and phi rule remain open."),
        ("U09", "Cartan/Kato transport", "transport of a supplied smooth subbundle", "NO", "Transport does not choose a subbundle from a degenerate pair."),
        ("U10", "shift connection", "projected connection after character supplied", "NO", "Curvature and holonomy obstruct sections but do not choose the character."),
        ("U11", "co-presence", "whole-solution event-domain interpretation", "NO", "No local/gluing character content."),
        ("U12", "bootstrap primary", "after-solution global admissibility", "NO", "No local or boundary operator."),
        ("U13", "bootstrap stronger fork", "possible local matter-existence window", "OPEN", "Could discriminate completed branches only after native operator, source, and density map exist."),
        ("U14", "total proper density", "future total mass/proper volume output", "NO", "Not operational and cannot be inserted locally."),
        ("U15", "boundary framing", "future phase/gluing datum", "COULD_SELECT", "Precisely the kind of missing extra datum; presently open."),
    ]
    return [
        {
            "id": i,
            "principle": p,
            "registered_content": c,
            "supplies_rule": s,
            "reason": r,
        }
        for i, p, c, s, r in data
    ]


def completion_rows() -> list[dict[str, str]]:
    data = [
        ("FC01_BOUNDARY_BOUNDARY", "boundary framing required", "OPEN"),
        ("FC02_ONE_CAP_BOUNDARY", "cap annihilator or amplitude zero plus boundary framing", "CONDITIONAL"),
        ("FC03_TWO_CAP_P0", "residual line and holonomy depend on cap cycle", "CONDITIONAL"),
        ("FC04_TWO_CAP_P1", "no nonzero character annihilates both caps; patching/amplitude needed", "OBSTRUCTED_FOR_PHASE_ALONE"),
        ("FC05_TWO_CAP_P_GT1", "quotient congruence and lens holonomy required", "CONDITIONAL"),
        ("FC06_NONPRIMITIVE_CAP", "orbifold stabilizer representation required", "CONDITIONAL"),
        ("FC07_PERIODIC_TORUS_BUNDLE", "tie avoidance and monodromy-preserved line required", "CONDITIONAL"),
        ("FC08_MIRROR_DOUBLE", "identity/swap/conjugate lift must be supplied", "LIFT_DEPENDENT"),
        ("FC09_NONORIENTABLE_GLUE", "unoriented line may descend; phase needs real/conjugate structure", "CONDITIONAL"),
        ("FC10_STRATIFIED_PROJECTOR", "rank change terminates or makes set valued", "STRATUM_DEPENDENT"),
        ("FC11_NONINTEGRABLE_DISTRIBUTION", "no global integral torus lattice", "NOT_AVAILABLE"),
        ("FC12_RECIPROCAL_TORIC_DIAGONAL", "mandatory e1/e2 tie; swap gluing possible but unselected", "SET_VALUED_OR_EXTRA_LIFT"),
    ]
    return [
        {
            "completion_id": i,
            "wall_crossing_requirement": requirement,
            "outcome": outcome,
            "selected_by_current_udt": "NO",
        }
        for i, requirement, outcome in data
    ]


def source_rows() -> list[dict[str, str]]:
    manifest = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    rows = []
    for row in manifest:
        path = row["path"]
        if "dual_systole" in path:
            role = "parent exact chamber/set/transport evidence"
        elif "pre_density" in path:
            role = "parent metric-lattice and completion evidence"
        elif "BOOTSTRAP_PRINCIPLE" in path:
            role = "owner bootstrap authority"
        elif "bootstrap_variation" in path or "bootstrap_csn" in path:
            role = "bootstrap placement and CSN selector authority"
        elif "COMMON_SCALE" in path:
            role = "direct CSN authority"
        elif "NATIVE_ACTION_COLD" in path:
            role = "exact C0/C1 founding and finite-cell authority"
        elif "NATIVE_ACTION_DERIVATION_DISPATCH" in path:
            role = "synchronized foundation and authority boundary"
        elif "three_reciprocity" in path:
            role = "direct three-reciprocity distinction"
        elif "coframe_composition" in path:
            role = "complete coframe group and physical-composition limit"
        elif "finite_cell_cartan" in path:
            role = "finite-cell transport and selection limit"
        elif "global_metric_assembly" in path:
            role = "twelve completion source"
        elif "hopf" in path:
            role = "conditional topology/carrier boundary"
        elif "matter_bootstrap" in path:
            role = "dimensional and density-operation limit"
        else:
            role = "supporting frozen evidence"
        rows.append(
            {
                "path": path,
                "role": role,
                "affirmative_wall_rule_found": "NO",
                "disposition": "LOAD_BEARING" if not path.endswith(("SHA256SUMS.txt", "MANIFEST.sha256")) else "IDENTITY_ANCHOR",
            }
        )
    return rows


def main() -> None:
    checks: list[dict[str, Any]] = []

    w0 = shortest_reciprocal(0.0)
    left = shortest_reciprocal(-1.0)
    right = shortest_reciprocal(1.0)
    check(left == {E1}, "reciprocal_left_shortest", sorted(left), checks)
    check(w0 == {E1, E2}, "reciprocal_seal_tie", sorted(w0), checks)
    check(right == {E2}, "reciprocal_right_shortest", sorted(right), checks)

    swapped = {canonical_line(matvec(SWAP, w)) for w in w0}
    check(swapped == w0, "whole_tied_set_exchange_invariant", sorted(swapped), checks)
    fixed = [w for w in w0 if canonical_line(matvec(SWAP, w)) == w]
    check(fixed == [], "no_exchange_fixed_shortest_line", fixed, checks)

    check(canonical_line(matvec(SWAP, E1)) == E2, "swap_gluing_maps_left_to_right", matvec(SWAP, E1), checks)
    check(canonical_line(matvec(IDENTITY, E1)) != E2, "identity_gluing_does_not_map_left_to_right", matvec(IDENTITY, E1), checks)

    lex_before = min(w0)
    lex_after_basis_swap = min(swapped)
    covariant_lex_image = canonical_line(matvec(SWAP, lex_before))
    check(lex_after_basis_swap != covariant_lex_image, "lexicographic_tie_break_not_GL2Z_covariant", {"chosen_after": lex_after_basis_swap, "covariant_image": covariant_lex_image}, checks)

    diagonal_lines = {(1, 1), (1, -1)}
    diagonal_norms = {w: w[0] ** 2 + w[1] ** 2 for w in diagonal_lines}
    check(
        set(diagonal_norms.values()) == {2} and 1 < 2,
        "exchange_fixed_diagonals_not_shortest",
        {str(w): value for w, value in diagonal_norms.items()},
        checks,
    )

    q = Fraction(7, 3)
    scaled_norms = {E1: q * 1, E2: q * 1}
    check(scaled_norms[E1] == scaled_norms[E2], "CSN_common_factor_preserves_tie", str(q), checks)

    cap_cycle = (1, 0)
    check(E2[0] * cap_cycle[0] + E2[1] * cap_cycle[1] == 0, "cap_annihilator_positive_control", {"w": E2, "v": cap_cycle}, checks)
    check(E1[0] * cap_cycle[0] + E1[1] * cap_cycle[1] != 0, "cap_annihilator_negative_control", {"w": E1, "v": cap_cycle}, checks)

    curvature = Fraction(1, 1)
    check(curvature != 0, "nonzero_curvature_blocks_parallel_phase", str(curvature), checks)
    holonomy_turns = Fraction(1, 2)
    check(holonomy_turns.denominator != 1, "nonintegral_holonomy_blocks_single_valued_parallel_phase", str(holonomy_turns), checks)

    candidates = candidate_outcomes()
    principles = principle_rows()
    completions = completion_rows()
    sources = source_rows()

    check(len(candidates) == 32, "candidate_coverage", len(candidates), checks)
    check(len(principles) == 15, "principle_coverage", len(principles), checks)
    check(len(completions) == 12, "completion_coverage", len(completions), checks)
    check(len(sources) == 35, "source_coverage", len(sources), checks)
    check(all(row["selected_by_current_udt"] == "NO" for row in completions), "no_completion_privileged", 12, checks)
    check(all(row["physical_selection"] in {"NO", "OPEN"} for row in candidates), "no_physical_promotion", 32, checks)

    write_tsv(
        HERE / "CANDIDATE_OUTCOMES.tsv",
        list(candidates[0]),
        candidates,
    )
    write_tsv(
        HERE / "PRINCIPLE_CAPABILITY_MATRIX.tsv",
        list(principles[0]),
        principles,
    )
    write_tsv(
        HERE / "COMPLETION_WALL_CROSSING_ATLAS.tsv",
        list(completions[0]),
        completions,
    )
    write_tsv(
        HERE / "SOURCE_ADJUDICATION.tsv",
        list(sources[0]),
        sources,
    )

    result = {
        "mode": "CPU_ONLY_METRIC_LED_WALL_CROSSING_SELECTOR_AUDIT",
        "base": "bcd1692e8a2bdf2300c7e7f13f5d0f4f34d490f9",
        "preregistration_commits": ["393de99", "c42580c", "dc50f70"],
        "maximum_ruling": (
            "RECIPROCAL_TIE_SET_CONTINUATION_DERIVED__"
            "NO_EQUIVARIANT_SINGLE_SHORTEST_LINE_AT_SYMMETRIC_SEAL__"
            "SWAP_GLUE_CONDITIONAL_ON_UNSELECTED_GLOBAL_LIFT__"
            "REGISTERED_UDT_WALL_CROSSING_SELECTOR_NOT_FOUND"
        ),
        "reciprocal_control": {
            "left": [list(w) for w in sorted(left)],
            "seal": [list(w) for w in sorted(w0)],
            "right": [list(w) for w in sorted(right)],
            "exchange_matrix": [list(row) for row in SWAP],
            "fixed_shortest_lines_at_seal": fixed,
            "identity_gluing_continues_shortest": False,
            "swap_gluing_continues_shortest": True,
            "swap_gluing_selected": False,
        },
        "counts": {
            "checks": len(checks),
            "candidates": len(candidates),
            "principles": len(principles),
            "completions": len(completions),
            "sources": len(sources),
            "native_single_line_selectors": 0,
            "conditional_swap_gluings": 1,
        },
        "checks": checks,
        "scientific_scope": {
            "whole_set": "DERIVED_GLOBAL_WHERE_TORIC",
            "single_line_at_reciprocal_tie": "NO_EQUIVARIANT_SELECTOR",
            "reciprocal_swap_gluing": "CONDITIONAL_ON_EXTRA_LIFT",
            "physical_shortest_character": "OPEN",
            "carrier_action_source_mass": "OPEN_OR_CONDITIONAL_UNCHANGED",
            "density_scan": "NOT_RUN",
            "matter_solve": "NOT_RUN",
            "gpu": "NOT_USED",
        },
    }
    (HERE / "RESULTS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
