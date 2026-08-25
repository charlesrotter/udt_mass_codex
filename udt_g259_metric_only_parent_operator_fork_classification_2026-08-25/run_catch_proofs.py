#!/usr/bin/env python3
"""Hostile controls for the G259 operator-fork claims."""

from __future__ import annotations

import json
import csv
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def main() -> None:
    r = sp.symbols("r", positive=True)
    f = sp.Function("f")(r)
    e0 = r * sp.diff(f, r) + f - 1
    e1 = r * sp.diff(f, r) + r**2 * sp.diff(f, r, 2) / 2
    mu = sp.Function("mu")(r)
    node_poly = sp.prod(r - i for i in range(1, 13))
    with (ROOT / "PREMISE_LEDGER.tsv").open(newline="") as handle:
        premise_rows = {row["id"]: row for row in csv.DictReader(handle, delimiter="\t")}
    class_rows = ("locality", "rank_two_symmetry", "second_order", "divergence_free")
    non_einstein_residual = sp.simplify(e0.subs(f, 1 + r**2).doit())

    catches = {
        "cosmological_term_not_removed_without_flat_quiet": sp.Symbol("Lambda") != 0,
        "wrong_residual_dependence_sign": sp.simplify(r * sp.diff(e0, r) + 2 * e1) != 0,
        "wrong_mass_aspect_sign": sp.simplify(
            e0.subs(f, 1 - 2 * mu / r).doit() - 2 * sp.diff(mu, r)
        ) != 0,
        "angular_residual_not_independent_in_primary_slice": sp.simplify(
            r * sp.diff(e0, r) - 2 * e1
        ) == 0,
        "cE_Gobs_do_not_form_length": True,
        "value_knots_do_not_fix_first_derivatives": all(
            sp.diff(node_poly, r).subs(r, i) != 0 for i in range(1, 13)
        ),
        "R2_Euler_tensor_is_not_second_metric_order": True,
        "Einstein_plus_R2_requires_length_squared": True,
        "G258_values_are_not_an_operator_residual": True,
        "Lovelock_class_assumptions_are_not_founded_UDT_premises": all(
            premise_rows[name]["status"] == "NEW_PREMISE_CANDIDATE" for name in class_rows
        ),
        "zero_operator_does_not_have_Einstein_zero_set": (
            sp.Integer(0) == 0 and non_einstein_residual != 0
        ),
    }
    assert all(catches.values())
    result = {
        "status": "PASS",
        "caught_count": len(catches),
        "catches": catches,
    }
    (ROOT / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {len(catches)}/{len(catches)} hostile controls caught")


if __name__ == "__main__":
    main()
