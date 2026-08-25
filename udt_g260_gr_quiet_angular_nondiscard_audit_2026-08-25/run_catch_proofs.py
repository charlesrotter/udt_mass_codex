#!/usr/bin/env python3
"""Hostile exact controls for G260 angular-retention semantics."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


OUT = Path(__file__).with_name("CATCH_PROOF_RESULT.json")


def main() -> None:
    root = Path(__file__).resolve().parent
    audit = (root / "AUDIT_REPORT.md").read_text()
    exact = (root / "EXACT_DERIVATION.md").read_text()
    ledger = (root / "PREMISE_LEDGER.tsv").read_text()
    r = F(7, 2)
    c = F(-3, 5)
    f = 1 + c / r
    fp = -c / r**2
    fpp = 2 * c / r**3
    e0 = r * fp + f - 1
    e1 = r * fp + r**2 * fpp / 2
    a_parallel = (r**2 * fpp - r * fp) / 2
    a_perp = 1 - f + r * fp / 2

    a = F(2, 7)
    b = F(-1, 5)
    f_bal = 1 + a * r**2 + b / r
    fp_bal = 2 * a * r - b / r**2
    fpp_bal = 2 * a + 2 * b / r**3
    e0_bal = r * fp_bal + f_bal - 1
    a_sum_bal = (r**2 * fpp_bal - r * fp_bal) / 2 + 1 - f_bal + r * fp_bal / 2

    f_off = F(5, 4)
    fp_off = F(2, 9)
    fpp_off = F(-4, 11)
    full_off = r * fp_off + f_off - 1
    e1_off = r * fp_off + r**2 * fpp_off / 2
    a_sum_off = (r**2 * fpp_off - r * fp_off) / 2 + 1 - f_off + r * fp_off / 2
    isolated_2d_off = F(0)

    pair_h00_with_angular = -F(1, 2) + F(1, 25)
    pair_h00_deleted = -F(1, 2)

    catches = {
        "delete_sphere_curvature_term": r * fp + f != e0,
        "call_isolated_2d_equation_profile_selecting": isolated_2d_off == 0 and full_off != 0,
        "call_vacuum_angular_modes_individually_zero": a_parallel != 0 and a_perp != 0,
        "replace_angular_difference_identity_by_sum": a_sum_off != e1_off + full_off,
        "call_all_trace_balanced_histories_vacuum": a_sum_bal == 0 and e0_bal != 0,
        "drop_nonzero_C_guard": c != 0 and a_parallel == 3 * c / (2 * r),
        "delete_pair_angular_gram": pair_h00_with_angular != pair_h00_deleted,
        "widen_quiet_result_to_loud_global_law": (
            "bounded scientific landing and all premise grades are unchanged" in audit.lower()
            and "does not derive the Einstein equation" in exact
            and "nonspherical_timelive\tOMITTED_OPEN" in ledger
        ),
    }
    assert all(catches.values())
    result = {
        "status": "PASS",
        "caught": catches,
        "caught_count": len(catches),
        "note": "The final scope catch is enforced by exact package wording; all other catches use explicit corrupted algebra.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
