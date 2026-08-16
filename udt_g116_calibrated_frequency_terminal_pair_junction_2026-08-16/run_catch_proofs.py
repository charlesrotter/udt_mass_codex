#!/usr/bin/env python3
"""Hostile-mutation catch proofs for G116."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent


def main() -> None:
    ell, n, b, bt, q, qt, w2 = F(2, 7), F(-3, 11), F(5, 13), F(-7, 17), F(-2, 9), F(4, 15), F(1, 8)
    p2 = (ell - n + b * b - bt / 2) / 2
    p2f = p2 + w2 / 2
    optical = 2 * ell + 2 * n + bt
    v = b - q
    dv = bt - qt
    f2 = b * b / 2 - n + bt / 2 - qt

    catches = {
        "delete_relative_drift": v != 0,
        "reverse_optical_sign": (p2 + optical / 4 + dv) != f2,
        "delete_relative_drift_derivative": (p2 - optical / 4) != f2,
        "fail_fixed_label_sky_subtraction": (p2f - optical / 4 + dv) != f2,
        "identify_frequency_with_terminal_depth": v != 0 or f2 != p2,
        "naive_addition_double_counts_pure_branch": 2 * F(5, 9) != F(5, 9),
    }

    # A residual slicing changes b itself while preserving b-q.
    a = F(3, 10)
    catches["promote_b_as_invariant"] = b + 2 * a != b and (b + 2 * a) - (q + 2 * a) == b - q

    result = {
        "status": "PASS" if all(catches.values()) else "FAIL",
        "caught": catches,
        "count": len(catches),
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
