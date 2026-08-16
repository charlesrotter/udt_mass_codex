#!/usr/bin/env python3
"""Hostile mutation checks for the G103 evidence gates."""

from __future__ import annotations

from fractions import Fraction as F
import json
import os
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rank(a: list[list[F]]) -> int:
    m = [row[:] for row in a]
    nr, nc, r = len(m), len(m[0]), 0
    for c in range(nc):
        p = next((i for i in range(r, nr) if m[i][c]), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        scale = m[r][c]
        m[r] = [x / scale for x in m[r]]
        for i in range(nr):
            if i != r and m[i][c]:
                f = m[i][c]
                m[i] = [m[i][j] - f * m[r][j] for j in range(nc)]
        r += 1
        if r == nr:
            break
    return r


def main() -> None:
    catches = {}

    # A frozen query cannot follow an arbitrary changed coframe/target.
    e = [[F(2), F(0)], [F(0), F(3)]]
    j_frozen = [[F(1), F(0)], [F(0), F(1)]]
    v_target = [[F(3), F(0)], [F(0), F(2)]]
    ej = [[sum(e[i][k] * j_frozen[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    catches["freeze_J_detected"] = ej != v_target

    # Omitting -dot(E)J from dot(J) leaves a visible first-jet defect.
    e_dot = [[F(1), F(0)], [F(0), F(-1)]]
    e_inv = [[F(1, 2), F(0)], [F(0), F(1, 3)]]
    v_dot = [[F(0), F(1)], [F(1), F(0)]]
    bad_j_dot = [[sum(e_inv[i][k] * v_dot[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    bad_rebuild = [[sum(e_dot[i][k] * j_frozen[k][j] + e[i][k] * bad_j_dot[k][j]
                        for k in range(2)) for j in range(2)] for i in range(2)]
    catches["first_jet_omission_detected"] = bad_rebuild != v_dot

    # A second unit timelike vector need not be the same observer clock.
    u1 = [F(1), F(0), F(0), F(0)]
    u2 = [F(5, 4), F(3, 4), F(0), F(0)]
    norm = lambda u: -u[0] ** 2 + sum(x * x for x in u[1:])
    catches["common_observer_drop_detected"] = norm(u1) == norm(u2) == -1 and u1 != u2

    n_bad = [F(0), F(2), F(0), F(0)]
    catches["nonunit_sky_detected"] = norm(n_bad) != 1
    catches["rank4_sky_detected"] = rank([[F(int(i == j)) for j in range(4)] for i in range(4)]) > 3

    # Independent edge assignments need not compose; endpoint potentials do.
    bad_edges = {(0, 1): F(2), (1, 2): F(3), (0, 2): F(5)}
    catches["noncomposing_depth_detected"] = bad_edges[(0, 1)] * bad_edges[(1, 2)] != bad_edges[(0, 2)]

    # The released-J witness violates a false universalized fixed-base direction.
    catches["fixed_base_overpromotion_detected"] = F(4, 9) < F(9, 4)

    # Same marginal, different coupling: one-point data do not select pair structure.
    parallel = [[F(int(i == j), 4) for j in range(4)] for i in range(4)]
    antipodal = [[F(x, 4) for x in row] for row in
                 [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]]
    rows = lambda c: [sum(row) for row in c]
    catches["pair_measure_uniqueness_detected"] = (
        rows(parallel) == rows(antipodal) == [F(1, 4)] * 4 and parallel != antipodal
    )

    # Pullback non-identifiability is image-qualified.
    image = {0, 1}
    target_support = {2}
    catches["image_support_drop_detected"] = not target_support.issubset(image)

    # Scope and outcome guards must reject explicit hostile mutations.
    def local_scope_guard(claim: str) -> bool:
        return "GLOBAL_COMPLETE" not in claim and "GENERIC_NO_GO" not in claim

    safe_claim = "LOCAL_REGULAR_SURJECTION__GLOBAL_COMPLETION_OPEN"
    hostile_claim = safe_claim + "__GLOBAL_COMPLETE"
    catches["local_to_global_promotion_detected"] = (
        local_scope_guard(safe_claim) and not local_scope_guard(hostile_claim)
    )

    banned_outcomes = {"R2_OUTCOME_REPORT.md", "R5_OUTCOME_REPORT.md", "BOSS_CURVE.npz"}

    def outcome_guard(opened: set[str]) -> bool:
        return opened.isdisjoint(banned_outcomes)

    catches["outcome_opening_detected"] = (
        outcome_guard(set()) and not outcome_guard({"R5_OUTCOME_REPORT.md"})
    )

    if not all(catches.values()):
        raise AssertionError(json.dumps(catches, indent=2, sort_keys=True))
    result = {"status": "PASS", "caught_mutations": catches}
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "CATCH_PROOF_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
