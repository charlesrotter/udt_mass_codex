#!/usr/bin/env python3
"""Independent exact reconstruction with standard-library Fractions."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def check(checks: dict[str, str], name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def zeros(rows: int, columns: int) -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(columns)] for _ in range(rows)]


def eye(size: int) -> list[list[Fraction]]:
    result = zeros(size, size)
    for index in range(size):
        result[index][index] = Fraction(1)
    return result


def mm(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                Fraction(0),
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def msub(
    left: list[list[Fraction]], right: list[list[Fraction]]
) -> list[list[Fraction]]:
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def mneg(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[-value for value in row] for row in matrix]


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rows, columns = len(work), len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (r for r in range(pivot_row, rows) if work[r][column] != 0),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for r in range(rows):
            if r == pivot_row:
                continue
            factor = work[r][column]
            if factor:
                work[r] = [
                    work[r][c] - factor * work[pivot_row][c]
                    for c in range(columns)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def block(
    upper_left: list[list[Fraction]],
    upper_right: list[list[Fraction]],
    lower_left: list[list[Fraction]],
    lower_right: list[list[Fraction]],
) -> list[list[Fraction]]:
    upper = [a + b for a, b in zip(upper_left, upper_right)]
    lower = [a + b for a, b in zip(lower_left, lower_right)]
    return upper + lower


def exterior_derivation(
    endomorphism: list[list[Fraction]],
) -> list[list[Fraction]]:
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    pair_index = {pair: i for i, pair in enumerate(pairs)}
    result = zeros(6, 6)

    def add(column: int, coefficient: Fraction, i: int, j: int) -> None:
        if i == j or coefficient == 0:
            return
        if i < j:
            result[pair_index[(i, j)]][column] += coefficient
        else:
            result[pair_index[(j, i)]][column] -= coefficient

    for column, (i, j) in enumerate(pairs):
        for a in range(4):
            add(column, endomorphism[a][i], a, j)
            add(column, endomorphism[a][j], i, a)
    return result


def validate_state(state: dict[str, object]) -> None:
    required = {
        "result": "PASS",
        "solder": "OPEN_NO_REGISTERED_WITNESS",
        "direct_sum": "DERIVED_REMAINS_STRONGEST_CURRENT_ASSEMBLY",
        "splice": "FORBIDDEN_NOT_USED",
        "xmax": "OPEN",
        "candidates": 12,
        "generators": 5,
        "branches": 6,
        "causal": 5,
        "completions": 12,
        "equations": 28,
        "sources": 21,
        "hodge_type": "DERIVED_UNIVERSAL_CONTROL_TYPE_MISMATCH_TO_JACOBI_PHASE",
        "screen_map": "OBSTRUCTED_BY_ENDPOINT_SCREEN_GAUGE",
        "wrl": "NO_POINTWISE_SIMILARITY_IN_EXACT_LOCAL_RADIAL_CONTROL",
        "universal": "OPEN",
    }
    if state != required:
        raise AssertionError("state")


def rejected(state: dict[str, object], key: str, value: object) -> str:
    mutated = dict(state)
    mutated[key] = value
    try:
        validate_state(mutated)
    except AssertionError:
        return "PASS_REJECTED"
    raise AssertionError(f"mutation accepted: {key}")


def main() -> None:
    checks: dict[str, str] = {}
    zero3, id3 = zeros(3, 3), eye(3)
    star = block(zero3, mneg(id3), id3, zero3)
    check(checks, "hodge_square", mm(star, star) == mneg(eye(6)))
    check(checks, "hodge_rank", rank(star) == 6)

    j2 = [[Fraction(0), Fraction(-1)], [Fraction(1), Fraction(0)]]
    j4 = block(j2, zeros(2, 2), zeros(2, 2), j2)
    check(checks, "screen_gauge_generator_rank", rank(j4) == 4)
    check(checks, "screen_gauge_fixed_vector_dimension_zero", 4 - rank(j4) == 0)

    # Screen-line commutator in a parallel frame.
    projector = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(0)]]
    tidal_diagonal = [[Fraction(2), Fraction(0)], [Fraction(0), Fraction(5)]]
    tidal_mixed = [[Fraction(2), Fraction(3)], [Fraction(3), Fraction(5)]]
    check(
        checks,
        "diagonal_tidal_preserves_line",
        mm(tidal_diagonal, projector) == mm(projector, tidal_diagonal),
    )
    check(
        checks,
        "mixed_tidal_breaks_line",
        mm(tidal_mixed, projector) != mm(projector, tidal_mixed),
    )

    # Exact nontrivial generator match: a=2, K=-4.
    a = Fraction(2)
    jacobi_matched = [[Fraction(0), Fraction(1)], [a * a, Fraction(0)]]
    reciprocal = [[-a, Fraction(0)], [Fraction(0), a]]
    solder = [[Fraction(1), Fraction(1)], [-a, a]]
    check(
        checks,
        "matched_negative_curvature_intertwiner",
        mm(jacobi_matched, solder) == mm(solder, reciprocal),
    )
    check(checks, "matched_solder_rank_two", rank(solder) == 2)
    jacobi_positive = [[Fraction(0), Fraction(1)], [Fraction(-3), Fraction(0)]]
    check(
        checks,
        "positive_curvature_determinant_mismatch",
        jacobi_positive[0][0] * jacobi_positive[1][1]
        - jacobi_positive[0][1] * jacobi_positive[1][0]
        != reciprocal[0][0] * reciprocal[1][1],
    )
    flat_jacobi = [[Fraction(0), Fraction(1)], [Fraction(0), Fraction(0)]]
    check(checks, "flat_jacobi_nonzero", flat_jacobi != zeros(2, 2))
    check(checks, "flat_jacobi_nilpotent", mm(flat_jacobi, flat_jacobi) == zeros(2, 2))

    # Exact WR-L rational point X=2,D=1.
    X, distance = Fraction(2), Fraction(1)
    lapse = 1 - distance / (2 * X)
    radius = distance - distance * distance / (4 * X)
    curvature = 1 / (2 * X * radius)
    clock_rate = 1 / (2 * X * lapse)
    check(checks, "wrl_lapse", lapse == Fraction(3, 4))
    check(checks, "wrl_radius", radius == Fraction(7, 8))
    check(checks, "wrl_curvature", curvature == Fraction(2, 7))
    check(checks, "wrl_clock_rate", clock_rate == Fraction(1, 3))
    check(
        checks,
        "wrl_generator_mismatch",
        curvature + clock_rate * clock_rate == Fraction(25, 63),
    )
    check(
        checks,
        "wrl_scalar_profile_relation",
        radius == X * (1 - lapse * lapse),
    )

    # Hodge can be parallel while the selected 3+3 sectors mix.
    boost = [
        [Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(-1)],
        [Fraction(0), Fraction(1), Fraction(0)],
    ]
    connection = block(zero3, boost, mneg(boost), zero3)
    check(checks, "connection_hodge_commutation", mm(connection, star) == mm(star, connection))
    projector6 = zeros(6, 6)
    for i in range(3):
        projector6[i][i] = Fraction(1)
    mixing = msub(mm(connection, projector6), mm(projector6, connection))
    check(checks, "connection_split_mixing_rank", rank(mixing) == 4)

    # Null dphi line map and its induced two-form filtration.
    null_map = [
        [Fraction(-1), Fraction(-1), Fraction(0), Fraction(0)],
        [Fraction(1), Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
    ]
    check(checks, "null_line_rank", rank(null_map) == 1)
    check(checks, "null_line_nilpotent", mm(null_map, null_map) == zeros(4, 4))
    null_lift = exterior_derivation(null_map)
    check(checks, "null_lift_rank", rank(null_lift) == 2)
    check(checks, "null_lift_nilpotent", mm(null_lift, null_lift) == zeros(6, 6))

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    candidates = {
        row["candidate"]: row for row in read_tsv(HERE / "SOLDER_TYPE_LEDGER.tsv")
    }
    generators = read_tsv(HERE / "GENERATOR_MATCH_ATLAS.tsv")
    branches = {
        row["branch"]: row for row in read_tsv(HERE / "BRANCH_SOLDER_ATLAS.tsv")
    }
    causal = read_tsv(HERE / "CAUSAL_SOLDER_ATLAS.tsv")
    completions = read_tsv(HERE / "COMPLETION_SOLDER_ATLAS.tsv")
    statuses = {
        row["claim"]: row for row in read_tsv(HERE / "STATUS_LEDGER.tsv")
    }
    equations = read_tsv(
        ROOT
        / "udt_center_free_observer_optical_correspondence_audit_2026-07-24"
        / "EQUATION_FAMILY_OPTICAL_SCREEN.tsv"
    )
    check(checks, "production_result", production["result"] == "PASS")
    check(checks, "production_checks", set(production["checks"].values()) == {"PASS"})
    check(checks, "candidate_count", len(candidates) == 12)
    check(checks, "generator_count", len(generators) == 5)
    check(checks, "branch_count", len(branches) == 6)
    check(checks, "causal_count", len(causal) == 5)
    check(checks, "completion_count", len(completions) == 12)
    check(checks, "completion_unique", len({r["completion_id"] for r in completions}) == 12)
    check(checks, "equation_count", len(equations) == 28)
    check(checks, "equation_unique", len({r["family_id"] for r in equations}) == 28)
    check(
        checks,
        "hodge_type_guard",
        candidates["HODGE_NORMAL_SCREEN_AREA_DUALITY"]["solder_ruling"]
        == "DERIVED_UNIVERSAL_CONTROL_TYPE_MISMATCH_TO_JACOBI_PHASE",
    )
    check(
        checks,
        "screen_map_guard",
        candidates["SO2_EQUIVARIANT_LINEAR_CLOCK_TO_PHASE_MAP"]["solder_ruling"]
        == "OBSTRUCTED_BY_ENDPOINT_SCREEN_GAUGE",
    )
    check(
        checks,
        "wrl_solder_guard",
        statuses[
            "WRL pointwise natural-frame clock-transverse generator solder"
        ]["status"]
        == "NO_POINTWISE_SIMILARITY_IN_EXACT_LOCAL_RADIAL_CONTROL",
    )
    check(
        checks,
        "universal_open",
        branches["UNIVERSAL_PHYSICAL_UDT"]["linear_solder"] == "OPEN",
    )

    sources = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    check(checks, "source_count", len(sources) == 21)
    check(checks, "source_unique", len({row["path"] for row in sources}) == 21)
    for row in sources:
        if row["role"] == "frontier_scope_at_base":
            data = subprocess.run(
                [
                    "git",
                    "show",
                    "2e98f4cc91a0accbfe8a5e96d180ef3f297d8da0:" + row["path"],
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            ).stdout
        else:
            data = (ROOT / row["path"]).read_bytes()
        check(
            checks,
            f"source_hash_{row['role']}",
            hashlib.sha256(data).hexdigest() == row["sha256"],
        )

    state: dict[str, object] = {
        "result": production["result"],
        "solder": production["intrinsic_irreducible_solder"],
        "direct_sum": production["direct_sum_cocycle"],
        "splice": production["cross_branch_splice"],
        "xmax": production["physical_Xmax"],
        "candidates": len(candidates),
        "generators": len(generators),
        "branches": len(branches),
        "causal": len(causal),
        "completions": len(completions),
        "equations": len(equations),
        "sources": len(sources),
        "hodge_type": candidates["HODGE_NORMAL_SCREEN_AREA_DUALITY"]["solder_ruling"],
        "screen_map": candidates[
            "SO2_EQUIVARIANT_LINEAR_CLOCK_TO_PHASE_MAP"
        ]["solder_ruling"],
        "wrl": statuses[
            "WRL pointwise natural-frame clock-transverse generator solder"
        ]["status"],
        "universal": branches["UNIVERSAL_PHYSICAL_UDT"]["linear_solder"],
    }
    validate_state(state)
    catches = {
        "hodge_promoted_to_phase_solder": rejected(
            state, "hodge_type", "DERIVED_CLOCK_PHASE_SOLDER"
        ),
        "preferred_screen_direction_inserted": rejected(
            state, "screen_map", "DERIVED_NONZERO"
        ),
        "wrl_profile_promoted_to_solder": rejected(state, "wrl", "DERIVED"),
        "irreducible_solder_promoted": rejected(state, "solder", "DERIVED"),
        "direct_sum_erased": rejected(state, "direct_sum", "SUPERSEDED"),
        "cross_branch_splice": rejected(state, "splice", "USED"),
        "physical_xmax_promotion": rejected(state, "xmax", "DERIVED"),
        "universal_promotion": rejected(state, "universal", "DERIVED"),
        "candidate_omission": rejected(state, "candidates", 11),
        "generator_omission": rejected(state, "generators", 4),
        "branch_omission": rejected(state, "branches", 5),
        "causal_omission": rejected(state, "causal", 4),
        "completion_omission": rejected(state, "completions", 11),
        "equation_omission": rejected(state, "equations", 27),
        "source_omission": rejected(state, "sources", 20),
    }
    result = {
        "result": "PASS",
        "method": "STANDARD_LIBRARY_FRACTION_LINEAR_ALGEBRA",
        "production_imported": False,
        "check_count": len(checks),
        "checks": checks,
        "catch_count": len(catches),
        "catches": catches,
        "exact_wrl_generator_mismatch": "25/63",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
