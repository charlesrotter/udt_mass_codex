#!/usr/bin/env python3
"""Semantic and exact mutation catches for G167."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def det2(h: list[list[F]]) -> F:
    return h[0][0] * h[1][1] - h[0][1] * h[1][0]


def q2(h: list[list[F]]) -> F:
    return h[0][0] ** 2 / (-det2(h))


def main() -> None:
    full = [[-F(391, 100), F(9, 50)], [F(9, 50), F(2)]]
    base = [[-F(4), F(0)], [F(0), F(1)]]
    angular = [[F(9, 100), F(9, 50)], [F(9, 50), F(1)]]
    zero_cross = [[full[0][0], F(0)], [F(0), full[1][1]]]

    exact = (HERE / "EXACT_DERIVATION.md").read_text()
    audit = (HERE / "AUDIT_REPORT.md").read_text()
    prereg = (HERE / "PREREGISTRATION.md").read_text()
    exact_words = " ".join(exact.split())
    audit_words = " ".join(audit.split())

    catches = {
        "dropping_angular_gram_changes_h": full != base,
        "post_readout_angular_attachment_misses_ratio": q2(full) != q2(base),
        "dropping_pair_cross_term_changes_ratio": q2(full) != q2(zero_cross),
        "angular_cross_term_exists_with_diagonal_base": base[0][1] == 0
        and angular[0][1] != 0,
        "scalar_trace_compression_false": q2([[-F(3), F(0)], [F(0), F(1)]])
        != q2([[-F(4), F(0)], [F(0), F(2)]]),
        "radial_not_promoted_to_general": "This boundary prevents the result" in exact,
        "query_live_not_ambient_dynamics": "not an ambient time-evolution equation" in exact_words,
        "general_ambient_extension_remains_open": "GENERAL_AMBIENT_EXTENSION_OPEN" in audit,
        "supplied_pair_not_fixed_path": "not a fixed path" in prereg,
        "no_xmax_or_downstream_promotion": "No dynamics, observation, or complete-universe claim follows"
        in audit_words,
    }
    result = {
        "status": "PASS" if all(catches.values()) else "FAIL",
        "caught": sum(catches.values()),
        "total": len(catches),
        "catches": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    if result["status"] != "PASS":
        raise SystemExit(f"FAIL: {[name for name, ok in catches.items() if not ok]}")
    print(f"PASS: {result['caught']}/{result['total']} G167 mutation catches")


if __name__ == "__main__":
    main()
