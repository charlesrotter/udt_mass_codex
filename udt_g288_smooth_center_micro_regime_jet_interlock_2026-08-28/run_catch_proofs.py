#!/usr/bin/env python3
"""Executable hostile-regression catches for G288's bounded landing."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RESULT = HERE / "DERIVATION_RESULT.json"
OUT = HERE / "CATCH_PROOF_RESULT.json"

LANDING = (
    "PARTIAL_CENTER_INTERLOCK_ONLY"
    "__QUADRATIC_NEGATIVE_PROFILE_GERM_IS_ZERO_TIDE_CONSTANT_CURVATURE"
    "__ANGULAR_TIDE_BEGINS_AT_INDEPENDENT_QUARTIC_JET"
    "__NO_PLANCK_SCALE_OR_HISTORY_SELECTED"
)


def validate(d: dict) -> None:
    if d.get("landing_candidate") != LANDING:
        raise AssertionError("landing changed")
    fresh = d["fresh_metric_expressions"]
    center = d["center_series"]
    quad = d["quadratic_family"]
    guards = d["interpretive_guards"]
    if center["angular_parallel"] != "4*r**4*(c4 + 3*c6*r**2 + 6*c8*r**4)":
        raise AssertionError("parallel center map changed")
    if center["angular_perpendicular"] != "r**4*(c4 + 2*c6*r**2 + 3*c8*r**4)":
        raise AssertionError("perpendicular center map changed")
    if quad["angular_parallel"] != "0" or quad["angular_perpendicular"] != "0":
        raise AssertionError("quadratic family no longer zero tide")
    if quad["weyl_squared"] != "0":
        raise AssertionError("quadratic family no longer conformally flat")
    if fresh["normalized_local_radial_null_speed"] != "c_E":
        raise AssertionError("coordinate slope promoted to local speed")
    if guards != {
        "mu_is_physical_mass": False,
        "planck_scale_inserted": False,
        "xmax_inserted": False,
        "negative_profile_is_negative_distance": False,
        "negative_profile_is_pair_arrow_reversal": False,
        "old_audit_formula_imported": False,
    }:
        raise AssertionError("interpretive guard changed")
    if not all(d["checks"].values()) or d["check_count"] != len(d["checks"]):
        raise AssertionError("production check ledger invalid")


def main() -> None:
    base = json.loads(RESULT.read_text())
    validate(base)
    mutations = []

    def add(name: str, mutate) -> None:
        trial = deepcopy(base)
        mutate(trial)
        caught = False
        try:
            validate(trial)
        except AssertionError:
            caught = True
        mutations.append({"name": name, "caught": caught})

    add("insert_quadratic_parallel_tide", lambda d: d["center_series"].__setitem__("angular_parallel", "2*c2*r**2 + 4*c4*r**4"))
    add("change_leading_angular_ratio", lambda d: d["center_series"].__setitem__("angular_parallel", "5*r**4*(c4 + 3*c6*r**2 + 6*c8*r**4)"))
    add("make_quadratic_weyl_nonzero", lambda d: d["quadratic_family"].__setitem__("weyl_squared", "12*C**2"))
    add("promote_mu_to_physical_mass", lambda d: d["interpretive_guards"].__setitem__("mu_is_physical_mass", True))
    add("promote_coordinate_slope_to_local_speed", lambda d: d["fresh_metric_expressions"].__setitem__("normalized_local_radial_null_speed", "c_E*f"))
    add("insert_planck_scale", lambda d: d["interpretive_guards"].__setitem__("planck_scale_inserted", True))
    add("insert_xmax", lambda d: d["interpretive_guards"].__setitem__("xmax_inserted", True))
    add("alias_profile_sign_to_arrow", lambda d: d["interpretive_guards"].__setitem__("negative_profile_is_pair_arrow_reversal", True))
    add("trust_old_audit_as_input", lambda d: d["interpretive_guards"].__setitem__("old_audit_formula_imported", True))

    if not all(row["caught"] for row in mutations):
        raise AssertionError("one or more hostile mutations escaped")
    out = {
        "status": "PASS",
        "baseline_valid": True,
        "caught": sum(row["caught"] for row in mutations),
        "total": len(mutations),
        "mutations": mutations,
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
