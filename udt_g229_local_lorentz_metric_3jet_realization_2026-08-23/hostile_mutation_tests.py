#!/usr/bin/env python3
"""Hostile controls for the bounded G229 metric-jet theorem."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

import verify_metric_3jet_independent as iv


ROOT = Path(__file__).resolve().parent


def one_sided_quartic_gauge() -> list[list[F]]:
    matrix = iv.zeros(200, 140)
    for row, ((i, j), (c, d, e)) in enumerate(iv.K_COLS):
        matrix[row][iv.B_INDEX[(j, tuple(sorted((i, c, d, e))))]] += F(iv.SIGNS[j])
    return matrix


def unsymmetrized_k_inverse(target_basis: list[list[F]]) -> list[list[F]]:
    columns = iv.transpose(target_basis)
    matrix = iv.zeros(200, len(columns))
    for row, ((a, b), (c, d, e)) in enumerate(iv.K_COLS):
        for basis_index, vector in enumerate(columns):
            matrix[row][basis_index] = -iv.d_component(vector, e, a, c, b, d)
    return matrix


def run() -> dict[str, object]:
    c2 = iv.c2_matrix()
    c3 = iv.c3_matrix()
    alg = iv.algebraic_bianchi()
    constraints = iv.full_d_constraints()
    d_basis = iv.nullspace_columns(constraints)
    normal3 = iv.normal3_constraints()
    gauge3 = iv.quartic_gauge()

    c2_wrong_sign = iv.c2_matrix(last_sign=1)
    c3_wrong_sign = iv.c3_matrix(last_sign=1)
    shortened_normal3 = normal3[:-35]
    shortened_gauge3 = [row[:-1] for row in gauge3]
    one_sided_gauge = one_sided_quartic_gauge()
    bad_d = [[F(0)] for _ in range(84)]
    bad_d[iv.SLOT_INDEX[(0, 5)]][0] = F(1)
    bad_d_constraint = iv.matmul(constraints, bad_d)
    naive_k = unsymmetrized_k_inverse(d_basis)

    prereg = (ROOT / "PREREGISTRATION.md").read_text(encoding="utf-8")
    map_text = (ROOT / "MAP.md").read_text(encoding="utf-8")
    exact = json.loads((ROOT / "exact_results.json").read_text(encoding="utf-8"))

    catches = {
        "c2_sign_mutant_detected": not iv.is_zero(iv.matmul(alg, c2_wrong_sign)),
        "c3_sign_mutant_detected": not iv.is_zero(iv.matmul(constraints, c3_wrong_sign)),
        "omitted_normal3_family_detected": iv.rank(shortened_normal3) < 140,
        "truncated_quartic_gauge_detected": iv.rank(shortened_gauge3) < 140,
        "one_sided_quartic_index_wiring_detected": not iv.is_zero(
            iv.matmul(c3, one_sided_gauge)
        ),
        "non_bianchi_D_detected": not iv.is_zero(bad_d_constraint),
        "unsymmetrized_K_inverse_detected": not iv.equal(iv.matmul(c3, naive_k), d_basis),
        "tangent_frame_scope_explicit": "a fixed tangent frame at the event" in map_text
        and "normal-coordinate uniqueness claim made before fixing the tangent frame" in prereg,
        "global_history_promotion_blocked": "does not generate values" in exact["scope_ceiling"]
        and "A local existence result is not a physical-history law" in map_text,
    }
    all_pass = all(catches.values())
    return {
        "landing": "ALL_HOSTILE_MUTATIONS_CAUGHT" if all_pass else "HOSTILE_CONTROL_FAILURE",
        "all_caught": all_pass,
        "count": len(catches),
        "catches": catches,
        "control_notes": {
            "omitted_normal3_rows": 35,
            "shortened_normal3_rank": iv.rank(shortened_normal3),
            "shortened_quartic_gauge_rank": iv.rank(shortened_gauge3),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = run()
    if not args.no_write:
        (ROOT / "hostile_results.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_caught"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
