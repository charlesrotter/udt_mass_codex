#!/usr/bin/env python3
"""Additions-only strengthened hostile mutations required by the G75 external review."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path

from verify_profile_family_correction import validate_shape_rows


HERE = Path(__file__).resolve().parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def accepted(shapes: list[dict[str, str]], profiles: list[dict[str, str]], result: dict) -> bool:
    return (
        len(shapes) == len({row["shape_id"] for row in shapes}) == 49
        and validate_shape_rows(shapes)
        and len(profiles) == len({row["profile_id"] for row in profiles}) == 591
        and all(row["center_status"] == "CENTER_C_INFINITY" for row in profiles)
        and all(row["signature_status"] == "LORENTZ_REGULAR_ALL_X" for row in profiles)
        and all(row["physical_status"] == "CHOSE_CONTROL_NOT_SELECTED" for row in profiles)
        and result["scale_status"] == "R_POSITIVE_SYMBOLIC_NOT_SELECTED"
        and result["physical_owner"] == "OPEN_NO_OWNER"
        and result["original_G74_blocked_profiles_repaired"] is False
    )


def main() -> None:
    shapes = table("SHAPE_ATLAS.tsv")
    profiles = table("PROFILE_ATLAS.tsv")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert accepted(shapes, profiles, result)
    catches = {}

    for name, mutate in (
        ("missing_shape", lambda s, p, r: s.pop()),
        ("duplicate_shape", lambda s, p, r: s.append(deepcopy(s[0]))),
        ("missing_profile", lambda s, p, r: p.pop()),
        ("duplicate_profile", lambda s, p, r: p.append(deepcopy(p[0]))),
        ("center_odd_profile", lambda s, p, r: p[3].__setitem__("center_status", "NOT_C2")),
        ("signature_failure", lambda s, p, r: p[4].__setitem__("signature_status", "DEGENERATE")),
        ("physical_selection", lambda s, p, r: p[5].__setitem__("physical_status", "SELECTED_PHYSICAL")),
        ("scale_selected", lambda s, p, r: r.__setitem__("scale_status", "R_SELECTED")),
        ("source_activated", lambda s, p, r: r.__setitem__("physical_owner", "SOURCE_FIT")),
        ("G74_repair_claim", lambda s, p, r: r.__setitem__("original_G74_blocked_profiles_repaired", True)),
        ("wrong_exact_root", lambda s, p, r: next(row for row in s if row["open_roots_exact"] != "-").__setitem__("open_roots_exact", "1/3@1")),
        ("wrong_distinct_root_count", lambda s, p, r: next(row for row in s if row["open_root_count_distinct"] != "0").__setitem__("open_root_count_distinct", "2")),
        ("wrong_normalization", lambda s, p, r: s[0].__setitem__("normalization_M", "2")),
        ("wrong_exact_extremum", lambda s, p, r: next(row for row in s if row["interior_extrema_exact"] != "-").__setitem__("interior_extrema_exact", "1/2:0")),
        ("behavior_labels_swapped_same_census", lambda s, p, r: (s[0].__setitem__("behavior_class", s[1]["behavior_class"]), s[1].__setitem__("behavior_class", "CENTER_OFF_NO_INTERIOR_ROOT"))),
        ("strata_swapped_same_census", lambda s, p, r: (s[0].__setitem__("stratum_code", s[1]["stratum_code"]), s[1].__setitem__("stratum_code", "C2_E0_O0_T0"))),
    ):
        test_shapes, test_profiles, test_result = deepcopy(shapes), deepcopy(profiles), deepcopy(result)
        mutate(test_shapes, test_profiles, test_result)
        catches[name] = not accepted(test_shapes, test_profiles, test_result)
    assert all(catches.values())
    payload = {
        "schema": "udt-cmb-g75-corrected-catches-v1",
        "status": "PASS",
        "catches": catches,
        "passed": sum(catches.values()),
        "total": len(catches),
        "protected_draft_read": False,
    }
    (HERE / "CORRECTED_CATCH_PROOF_RESULTS.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
