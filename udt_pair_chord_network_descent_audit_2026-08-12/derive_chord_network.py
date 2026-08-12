#!/usr/bin/env python3
"""Exact zero-order observer-pair chord/network classification."""

from __future__ import annotations

import csv
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def fstr(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def mmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def eye():
    return ((F(1), F(0)), (F(0), F(1)))


def bmat(state):
    t, ell, beta = state
    return ((t, t * beta), (F(0), ell))


def binv(state):
    t, ell, beta = state
    return ((F(1, 1) / t, -beta / ell), (F(0), F(1, 1) / ell))


def hmat(state):
    t, ell, beta = state
    return ((-t * t, -t * t * beta), (-t * t * beta, ell * ell - t * t * beta * beta))


def transition(source, target):
    return mmul(bmat(target), binv(source))


def msub(a, b):
    return tuple(tuple(a[i][j] - b[i][j] for j in range(2)) for i in range(2))


def madd(a, b):
    return tuple(tuple(a[i][j] + b[i][j] for j in range(2)) for i in range(2))


def psd_rank(p):
    a, m, n = p[0][0], p[0][1], p[1][1]
    determinant = a * n - m * m
    if a < 0 or n < 0 or determinant < 0:
        return -1
    if a == 0 and m == 0 and n == 0:
        return 0
    return 1 if determinant == 0 else 2


def symbolic_checks():
    Ti, Li, bi, Tj, Lj, bj, Tk, Lk, bk = sp.symbols(
        "Ti Li bi Tj Lj bj Tk Lk bk", positive=True
    )
    # Re-declare shifts without positivity assumptions.
    bi, bj, bk = sp.symbols("bi bj bk", real=True)
    eta = sp.diag(-1, 1)

    def B(T, L, beta):
        return sp.Matrix([[T, T * beta], [0, L]])

    Bi, Bj, Bk = B(Ti, Li, bi), B(Tj, Lj, bj), B(Tk, Lk, bk)
    hi, hj, hk = Bi.T * eta * Bi, Bj.T * eta * Bj, Bk.T * eta * Bk
    Rij, Rjk, Rik = Bj * Bi.inv(), Bk * Bj.inv(), Bk * Bi.inv()
    delta = bj - bi
    expected_rij = sp.Matrix([[Tj / Ti, Tj * delta / Li], [0, Lj / Li]])

    shear = sp.Matrix([[1, bi], [0, 1]])
    p_shifted = sp.simplify(shear.inv().T * (hj - hi) * shear.inv())
    expected_p = sp.Matrix(
        [
            [Ti**2 - Tj**2, -Tj**2 * delta],
            [-Tj**2 * delta, Lj**2 - Li**2 - Tj**2 * delta**2],
        ]
    )
    det_expected = (Ti**2 - Tj**2) * (Lj**2 - Li**2) - Ti**2 * Tj**2 * delta**2

    checks = {
        "terminal_metric": sp.simplify(hi - sp.Matrix([
            [-Ti**2, -Ti**2 * bi],
            [-Ti**2 * bi, Li**2 - Ti**2 * bi**2],
        ])) == sp.zeros(2),
        "terminal_coframe_unique_reconstruction": sp.simplify(
            sp.Matrix([
                [sp.sqrt(-hi[0, 0]), sp.sqrt(-hi[0, 0]) * hi[0, 1] / hi[0, 0]],
                [0, sp.sqrt(hi[1, 1] - hi[0, 1] ** 2 / hi[0, 0])],
            ]) - Bi
        ) == sp.zeros(2),
        "transition_formula": sp.simplify(Rij - expected_rij) == sp.zeros(2),
        "transition_composition": sp.simplify(Rjk * Rij - Rik) == sp.zeros(2),
        "transition_inverse": sp.simplify(Rij.inv() - Bi * Bj.inv()) == sp.zeros(2),
        "transition_identity": sp.simplify(Bi * Bi.inv() - sp.eye(2)) == sp.zeros(2),
        "det_common_scale_character": sp.simplify(Rij.det() - Tj * Lj / (Ti * Li)) == 0,
        "reciprocal_character": sp.simplify((Rij[0, 0] / Rij[1, 1]) - Tj * Li / (Ti * Lj)) == 0,
        "shifted_gram_formula": sp.simplify(p_shifted - expected_p) == sp.zeros(2),
        "shifted_gram_determinant": sp.simplify(p_shifted.det() - det_expected) == 0,
        "increment_addition": sp.simplify((hk - hi) - ((hj - hi) + (hk - hj))) == sp.zeros(2),
        "raw_beta_telescopes": sp.simplify((bj - bi) + (bk - bj) - (bk - bi)) == 0,
        "offdiagonal_composition": sp.simplify(
            (Rjk * Rij)[0, 1] - (Rjk[0, 0] * Rij[0, 1] + Rjk[0, 1] * Rij[1, 1])
        ) == 0,
        "reciprocal_character_composes": sp.simplify(
            (Rik[0, 0] / Rik[1, 1])
            - (Rjk[0, 0] / Rjk[1, 1]) * (Rij[0, 0] / Rij[1, 1])
        ) == 0,
        "area_character_composes": sp.simplify(Rik.det() - Rjk.det() * Rij.det()) == 0,
    }
    assert all(checks.values()), checks
    return {key: bool(value) for key, value in checks.items()}


def main():
    symbolic = symbolic_checks()
    states = [
        (T, L, beta)
        for T in [F(4), F(3), F(2), F(1)]
        for L in [F(1), F(2), F(3), F(4), F(5)]
        for beta in [F(-1), F(-1, 2), F(0), F(1, 2), F(1)]
    ]
    state_ids = [f"S{i:03d}" for i in range(len(states))]
    hvals = [hmat(s) for s in states]

    pair_rows = []
    pair_counts = Counter()
    order_rank = {}
    for i, source in enumerate(states):
        for j, target in enumerate(states):
            p = msub(hvals[j], hvals[i])
            rank = psd_rank(p)
            reverse_rank = psd_rank(msub(hvals[i], hvals[j]))
            label = "INCOMPARABLE" if rank < 0 else f"PSD_RANK_{rank}"
            pair_counts[label] += 1
            if rank >= 0:
                order_rank[(i, j)] = rank
            r = transition(source, target)
            Ti, Li, bi = source
            Tj, Lj, bj = target
            pair_rows.append(
                {
                    "pair_id": f"P{i:03d}_{j:03d}",
                    "source": state_ids[i],
                    "target": state_ids[j],
                    "T_source": fstr(Ti),
                    "L_source": fstr(Li),
                    "beta_source": fstr(bi),
                    "T_target": fstr(Tj),
                    "L_target": fstr(Lj),
                    "beta_target": fstr(bj),
                    "gram_class": label,
                    "reverse_gram_class": "INCOMPARABLE" if reverse_rank < 0 else f"PSD_RANK_{reverse_rank}",
                    "R11": fstr(r[0][0]),
                    "R12": fstr(r[0][1]),
                    "R22": fstr(r[1][1]),
                    "area_ratio": fstr(Tj * Lj / (Ti * Li)),
                    "reciprocal_ratio": fstr(Tj * Li / (Ti * Lj)),
                    "delta_beta": fstr(bj - bi),
                }
            )

    with (ROOT / "PAIR_ATLAS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(pair_rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(pair_rows)

    chain_rows = []
    chain_counts = Counter()
    successors = {i: [j for j in range(len(states)) if (i, j) in order_rank] for i in range(len(states))}
    for i in range(len(states)):
        for j in successors[i]:
            for k in successors[j]:
                rij = transition(states[i], states[j])
                rjk = transition(states[j], states[k])
                rik = transition(states[i], states[k])
                composed = mmul(rjk, rij)
                p_ij = msub(hvals[j], hvals[i])
                p_jk = msub(hvals[k], hvals[j])
                p_ik = msub(hvals[k], hvals[i])
                rank_total = psd_rank(p_ik)
                assert composed == rik
                assert madd(p_ij, p_jk) == p_ik
                assert rank_total >= 0
                phi_ratio_product = (
                    states[j][0] * states[i][1] / (states[i][0] * states[j][1])
                    * states[k][0] * states[j][1] / (states[j][0] * states[k][1])
                )
                phi_ratio_direct = states[k][0] * states[i][1] / (states[i][0] * states[k][1])
                assert phi_ratio_product == phi_ratio_direct
                nontrivial_edges = int(i != j) + int(j != k)
                chain_counts[f"edge_pattern_{nontrivial_edges}"] += 1
                chain_counts[f"total_rank_{rank_total}"] += 1
                chain_rows.append(
                    {
                        "chain_id": f"C{i:03d}_{j:03d}_{k:03d}",
                        "A": state_ids[i],
                        "B": state_ids[j],
                        "C": state_ids[k],
                        "rank_AB": order_rank[(i, j)],
                        "rank_BC": order_rank[(j, k)],
                        "rank_AC": rank_total,
                        "transition_composes": 1,
                        "Gram_increments_add": 1,
                        "reciprocal_character_composes": 1,
                        "delta_beta_telescopes": int((states[j][2] - states[i][2]) + (states[k][2] - states[j][2]) == states[k][2] - states[i][2]),
                        "nontrivial_directed_loop": int(i == k and (i != j or j != k)),
                    }
                )

    with (ROOT / "CHAIN_ATLAS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(chain_rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(chain_rows)

    nontrivial_reverse_psd = sum(
        1
        for (i, j), rank in order_rank.items()
        if i != j and (j, i) in order_rank
    )
    nontrivial_loops = sum(row["nontrivial_directed_loop"] for row in chain_rows)
    result = {
        "status": "EXACT_ZERO_ORDER_CHORD_NETWORK_ATLAS_COMPLETE",
        "symbolic_checks": symbolic,
        "symbolic_check_count": len(symbolic),
        "state_count": len(states),
        "pair_count": len(pair_rows),
        "pair_counts": dict(sorted(pair_counts.items())),
        "ordered_pair_count": len(order_rank),
        "chain_count": len(chain_rows),
        "chain_counts": dict(sorted(chain_counts.items())),
        "nontrivial_reverse_psd_count": nontrivial_reverse_psd,
        "nontrivial_directed_loop_count": nontrivial_loops,
        "maximum_conclusion": "EXACT_ZERO_ORDER_CHORD_NETWORK_CLASSIFICATION_ON_ONE_COMMON_A_CALIBRATED_TERMINAL_FAMILY",
    }
    assert len(pair_rows) == 10000
    assert len(chain_rows) >= 400
    assert pair_counts["PSD_RANK_0"] > 0
    assert pair_counts["PSD_RANK_1"] > 0
    assert pair_counts["PSD_RANK_2"] > 0
    assert pair_counts["INCOMPARABLE"] > 0
    assert nontrivial_reverse_psd == 0
    assert nontrivial_loops == 0
    (ROOT / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
