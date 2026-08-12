#!/usr/bin/env python3
"""Implementation-distinct stdlib/Fraction replay of the chord-network theorem.

This file imports no production module and reads no production result or atlas. It independently
replays the supplied closed-form transition algebra and PSD-order claims, but does not rederive the
closed-form arrow from the coframe. Its source-hash provenance check reads parent-repository files.
"""

from __future__ import annotations

import hashlib
import csv
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def metric(x):
    T, L, b = x
    return (-T * T, -T * T * b, L * L - T * T * b * b)


def difference(x, y):
    hx, hy = metric(x), metric(y)
    return hy[0] - hx[0], hy[1] - hx[1], hy[2] - hx[2]


def positive_rank(p):
    a, m, n = p
    d = a * n - m * m
    if a < 0 or n < 0 or d < 0:
        return -1
    if a == 0 and m == 0 and n == 0:
        return 0
    return 1 if d == 0 else 2


def arrow(x, y):
    Ti, Li, bi = x
    Tj, Lj, bj = y
    return Tj / Ti, Tj * (bj - bi) / Li, Lj / Li


def compose(left, right):
    e, f, g = left
    a, b, d = right
    return e * a, e * b + f * d, g * d


def invert(r):
    a, b, d = r
    return Q(1) / a, -b / (a * d), Q(1) / d


def area_character(r):
    return r[0] * r[2]


def reciprocal_character(r):
    return r[0] / r[2]


def source_hashes():
    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    checks = []
    for row in rows:
        path = REPO / row["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        checks.append(path.is_file() and digest == row["sha256"])
    return len(rows), all(checks)


def main():
    states = [
        (T, L, b)
        for T in [Q(5), Q(7, 2), Q(2), Q(1, 2)]
        for L in [Q(3, 2), Q(5, 2), Q(4), Q(6)]
        for b in [Q(-3, 4), Q(-1, 4), Q(1, 3), Q(2, 3)]
    ]
    n = len(states)
    identity = (Q(1), Q(0), Q(1))
    pair_counts = Counter()
    ordered = {}
    uniqueness_checks = 0
    inverse_checks = 0
    character_checks = 0
    strict_phi_checks = 0

    for i, x in enumerate(states):
        h00, h01, h11 = metric(x)
        T, L, b = x
        assert -h00 == T * T
        assert h01 / h00 == b
        assert h11 - h01 * h01 / h00 == L * L
        uniqueness_checks += 1
        for j, y in enumerate(states):
            r = arrow(x, y)
            rinv = arrow(y, x)
            assert compose(rinv, r) == identity
            assert invert(r) == rinv
            inverse_checks += 1
            assert area_character(r) == y[0] * y[1] / (x[0] * x[1])
            assert reciprocal_character(r) == y[0] * x[1] / (x[0] * y[1])
            character_checks += 2
            rank = positive_rank(difference(x, y))
            label = "incomparable" if rank < 0 else f"rank{rank}"
            pair_counts[label] += 1
            if rank >= 0:
                ordered[(i, j)] = rank
                assert y[0] <= x[0]
                assert y[1] >= x[1]
                if i != j:
                    assert reciprocal_character(r) < 1
                    strict_phi_checks += 1

    all_triple_composition_checks = 0
    for i, x in enumerate(states):
        for j, y in enumerate(states):
            rxy = arrow(x, y)
            for k, z in enumerate(states):
                assert compose(arrow(y, z), rxy) == arrow(x, z)
                assert area_character(arrow(x, z)) == area_character(arrow(y, z)) * area_character(rxy)
                assert reciprocal_character(arrow(x, z)) == reciprocal_character(arrow(y, z)) * reciprocal_character(rxy)
                assert (y[2] - x[2]) + (z[2] - y[2]) == z[2] - x[2]
                all_triple_composition_checks += 1

    chain_counts = Counter()
    rank_rule_checks = 0
    increment_checks = 0
    nontrivial_loops = 0
    successors = {i: [j for j in range(n) if (i, j) in ordered] for i in range(n)}
    for i in range(n):
        for j in successors[i]:
            for k in successors[j]:
                pij = difference(states[i], states[j])
                pjk = difference(states[j], states[k])
                pik = difference(states[i], states[k])
                assert tuple(pij[a] + pjk[a] for a in range(3)) == pik
                increment_checks += 1
                rij, rjk, rik = ordered[(i, j)], ordered[(j, k)], positive_rank(pik)
                assert rik >= 0
                if rij == 0:
                    assert rik == rjk
                if rjk == 0:
                    assert rik == rij
                if rij == 2 or rjk == 2:
                    assert rik == 2
                if rij == 1 and rjk == 1:
                    assert rik in (1, 2)
                rank_rule_checks += 1
                chain_counts[f"rank_{rik}"] += 1
                if i == k and (i != j or j != k):
                    nontrivial_loops += 1

    reverse_nontrivial = sum(1 for (i, j) in ordered if i != j and (j, i) in ordered)
    assert reverse_nontrivial == 0
    assert nontrivial_loops == 0

    # Independently rebuilt middle states: the explicit transition is indispensable.
    A = (Q(5), Q(2), Q(-1, 4))
    Bin = (Q(7, 2), Q(5, 2), Q(1, 3))
    Bout = (Q(3), Q(4), Q(2, 3))
    C = (Q(1), Q(6), Q(-3, 4))
    r_ab = arrow(A, Bin)
    middle = arrow(Bin, Bout)
    r_bc = arrow(Bout, C)
    with_middle = compose(r_bc, compose(middle, r_ab))
    without_middle = compose(r_bc, r_ab)
    assert with_middle == arrow(A, C)
    assert without_middle != arrow(A, C)

    source_count, hashes_ok = source_hashes()
    assert source_count == 9 and hashes_ok
    result = {
        "status": "INDEPENDENT_EXACT_FRACTION_CHORD_NETWORK_PASS",
        "implementation": (
            "stdlib Fraction; different state family; no production imports or result reads; "
            "replays supplied closed-form transition and PSD claims; source hashes read parent repo"
        ),
        "state_count": n,
        "pair_count": n * n,
        "pair_counts": dict(sorted(pair_counts.items())),
        "ordered_pair_count": len(ordered),
        "all_triple_composition_checks": all_triple_composition_checks,
        "ordered_chain_count": sum(chain_counts.values()),
        "chain_counts": dict(sorted(chain_counts.items())),
        "terminal_reconstruction_checks": uniqueness_checks,
        "inverse_checks": inverse_checks,
        "character_checks": character_checks,
        "strict_phi_checks": strict_phi_checks,
        "increment_checks": increment_checks,
        "rank_rule_checks": rank_rule_checks,
        "nontrivial_reverse_psd_count": reverse_nontrivial,
        "nontrivial_directed_loop_count": nontrivial_loops,
        "independent_middle_transition_required": True,
        "source_count": source_count,
        "source_hashes": hashes_ok,
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
