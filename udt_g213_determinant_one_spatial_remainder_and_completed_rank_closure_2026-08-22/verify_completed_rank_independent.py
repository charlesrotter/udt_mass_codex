#!/usr/bin/env python3
"""Dependency-free exact-Fraction replay of the G213 rank bridge; writes no files."""

from fractions import Fraction as F
import json
import random


SEED = 21320260822
CASES = 10_000
rng = random.Random(SEED)
assertions = 0


def demand(condition, message):
    global assertions
    assertions += 1
    if not condition:
        raise AssertionError(message)


def det3(K):
    return (
        K[0][0] * (K[1][1] * K[2][2] - K[1][2] * K[2][1])
        - K[0][1] * (K[1][0] * K[2][2] - K[1][2] * K[2][0])
        + K[0][2] * (K[1][0] * K[2][1] - K[1][1] * K[2][0])
    )


def make_metric():
    """Build rational data whose six preregistered pair densities are rational."""
    while True:
        b = [F(rng.randint(-40, 40), 1000) for _ in range(3)]
        m_axis = [F(1000 + rng.randint(-40, 40), 1000) for _ in range(3)]
        cdiag = [m_axis[i] ** 2 - b[i] ** 2 for i in range(3)]
        m_pair = [F(1414 + rng.randint(-30, 30), 1000) for _ in range(3)]
        pair_indices = [(0, 1), (0, 2), (1, 2)]
        cross = {}
        for mval, (i, j) in zip(m_pair, pair_indices):
            csum = mval**2 - (b[i] + b[j])**2
            cross[(i, j)] = (csum - cdiag[i] - cdiag[j]) / 2
        K = [
            [cdiag[0], cross[(0, 1)], cross[(0, 2)]],
            [cross[(0, 1)], cdiag[1], cross[(1, 2)]],
            [cross[(0, 2)], cross[(1, 2)], cdiag[2]],
        ]
        if K[0][0] > 0 and K[0][0] * K[1][1] - K[0][1] ** 2 > 0 and det3(K) > 0:
            return b, K, m_axis + m_pair


directions = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]


def pair_entries(b, K, v):
    a = F(-1)
    bv = sum((b[i] * v[i] for i in range(3)), F(0))
    cv = sum((F(v[i]) * K[i][j] * v[j] for i in range(3) for j in range(3)), F(0))
    return a, bv, cv


def reconstruct_metric(tuples):
    a = tuples[0][0]
    b = [tuples[i][1] for i in range(3)]
    diag = [tuples[i][2] for i in range(3)]
    sums = [tuples[i][2] for i in range(3, 6)]
    k01 = (sums[0] - diag[0] - diag[1]) / 2
    k02 = (sums[1] - diag[0] - diag[2]) / 2
    k12 = (sums[2] - diag[1] - diag[2]) / 2
    return a, b, [[diag[0], k01, k02], [k01, diag[1], k12], [k02, k12, diag[2]]]


changed_metrics = 0
for case in range(CASES):
    b, K, registered_m = make_metric()
    completed = []
    reconstructed_pairs = []
    completed_blind = []
    completed_blind_scaled = []
    scale = F(3 + (case % 7), 2 + (case % 3))
    if scale == 1:
        scale = F(5, 3)

    for index, v in enumerate(directions):
        a, bv, cv = pair_entries(b, K, v)
        m = registered_m[index]
        demand(bv**2 - a * cv == m**2, f"registered rational density {case}:{index}")

        # h_s = diag(1,m)^(-T) h_sigma diag(1,m)^(-1)
        hs00 = a
        hs01 = bv / m
        hs11 = cv / m**2
        demand(hs00 * hs11 - hs01**2 == -1, f"completed determinant {case}:{index}")

        # Typed completed tuple round trip.
        a_back = hs00
        b_back = m * hs01
        c_back = m**2 * hs11
        demand((a_back, b_back, c_back) == (a, bv, cv), f"pair roundtrip {case}:{index}")
        completed.append((m, hs00, hs01, hs11))
        reconstructed_pairs.append((a_back, b_back, c_back))

        # Delete m: spatial rescaling changes h_sigma and m but not h_s.
        b_scaled = scale * bv
        c_scaled = scale**2 * cv
        m_scaled = scale * m
        blind_scaled = (a, b_scaled / m_scaled, c_scaled / m_scaled**2)
        blind = (hs00, hs01, hs11)
        demand(blind_scaled == blind, f"density blind family {case}:{index}")
        completed_blind.append(blind)
        completed_blind_scaled.append(blind_scaled)

    a_back, b_back, K_back = reconstruct_metric(reconstructed_pairs)
    demand(a_back == -1, f"ambient clock reconstruction {case}")
    demand(b_back == b, f"ambient time-space reconstruction {case}")
    demand(K_back == K, f"ambient spatial reconstruction {case}")
    demand(completed_blind_scaled == completed_blind, f"network blind family {case}")

    b_scaled = [scale * value for value in b]
    K_scaled = [[scale**2 * value for value in row] for row in K]
    demand(b_scaled != b or K_scaled != K, f"ambient metric actually changes {case}")
    demand(det3(K_scaled) > 0, f"scaled spatial positivity {case}")
    changed_metrics += 1


# Independent integer rank of the G129 design, using exact row reduction.
rows = []
for v1, v2, v3 in directions:
    rows.extend([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, v1, v2, v3, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, v1*v1, 2*v1*v2, 2*v1*v3, v2*v2, 2*v2*v3, v3*v3],
    ])


def rank(matrix):
    work = [[F(value) for value in row] for row in matrix]
    pivot_row = 0
    for col in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work)) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        lead = work[pivot_row][col]
        work[pivot_row] = [value / lead for value in work[pivot_row]]
        for row in range(len(work)):
            if row != pivot_row and work[row][col]:
                factor = work[row][col]
                work[row] = [left - factor * right for left, right in zip(work[row], work[pivot_row])]
        pivot_row += 1
    return pivot_row


design_rank = rank(rows)
demand(design_rank == 10, "independent G129 design rank")

# Independent exact mode census. Rows are x00,x01,x02,x11,x12 and columns are
# gamma,w1,w2,s1,s2. The first column is the grading coordinate; columns 1:5 are the
# G208 mixing and G207 trace-free screen-shape coordinates.
mode_map = [
    [2, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [-1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
]
mode_census_rank = rank(mode_map)
g207_g208_union_rank = rank([row[1:] for row in mode_map])
grading_completion_rank = rank([[row[1], row[2], row[3], row[4], row[0]] for row in mode_map])
demand(mode_census_rank == 5, "independent five-mode census")
demand(g207_g208_union_rank == 4, "independent G207 G208 union rank")
demand(grading_completion_rank == 5, "independent grading completion rank")

print(json.dumps({
    "audit": "G213",
    "status": "PASS",
    "method": "stdlib_fraction_rational_density_construction_independent_mode_census_and_row_reduction",
    "seed": SEED,
    "cases": CASES,
    "assertions": assertions,
    "changed_density_blind_metrics": changed_metrics,
    "g129_design_rank": design_rank,
    "mode_census_rank": mode_census_rank,
    "g207_g208_union_rank": g207_g208_union_rank,
    "grading_completion_rank": grading_completion_rank,
    "all_pair_roundtrips_exact": True,
    "density_blind_counterfamily_exact": True,
}, sort_keys=True))
