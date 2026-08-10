#!/usr/bin/env python3
"""Independent set-based reconstruction of the G56 descent atlas."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def source_table(source_id: str) -> list[dict[str, str]]:
    manifest = {row["source_id"]: row for row in table("SOURCE_MANIFEST.tsv")}
    direct = HERE.parent / manifest[source_id]["path"]
    sealed = HERE.parent / "sources" / manifest[source_id]["path"]
    path = direct if direct.exists() else sealed
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="verify without writing")
    args = parser.parse_args()
    rows = table("GLOBAL_DESCENT_ATLAS.tsv")
    cells = {(row["branch_id"], row["axis_id"]): row["disposition"] for row in rows}
    checks: list[str] = []

    def check(condition: bool, label: str) -> None:
        if not condition:
            raise SystemExit(f"FAIL: {label}")
        checks.append(label)

    branches = {f"R{i:02d}" for i in range(1, 25)}
    axes = {f"D{i:02d}" for i in range(1, 11)}
    check(len(rows) == 240, "240 rows")
    check(set(row["branch_id"] for row in rows) == branches, "24 branches")
    check(set(row["axis_id"] for row in rows) == axes, "10 axes")
    check(len(cells) == 240, "unique Cartesian cells")

    # Reconstruct the load-bearing semantic inputs from the pinned sources. This is intentionally
    # independent of derive_descent_atlas.py and does not import its ruling vectors.
    branch_source = source_table("S04")
    global_source = {row["branch_id"]: row for row in source_table("S05")}
    profile_source = {row["branch_id"]: row for row in source_table("S02")}
    g55_source = {(row["branch_id"], row["axis_id"]): row for row in source_table("S03")}
    transition_source = {row["branch_id"]: row for row in source_table("S08")}
    surface_source = {row["candidate_id"]: row for row in source_table("S13")}
    middle_source = {row["candidate_id"]: row for row in source_table("S11")}
    check(len(branch_source) == len(global_source) == len(profile_source) == len(transition_source) == 24,
          "source branch censuses")
    check({row["branch_id"] for row in branch_source} == branches, "source branch identities")
    check(len(g55_source) == 240, "source G55 axis census")
    check(surface_source["C01"]["local_integrability"] == "INVOLUTIVE_FOR_GENERAL_STATIONARY_PHI",
          "source R17 involutivity")
    check("R_x_S1_HOPF_CYLINDER" in surface_source["C01"]["global_structure"],
          "source R17 global leaves")
    check("NO_ONE_LEAF_SELECTED" in surface_source["C01"]["metric_ownership"],
          "source R17 leaf nonselection")
    check(middle_source["M03"]["ownership_ruling"] == "DERIVED_PATH_LABELLED_SET",
          "source R17 alignment bitorsor")
    check(middle_source["M12"]["ownership_ruling"] == "DERIVED_PROJECTOR_ALIGNMENT_COMPOSITION",
          "source R17 balanced composition")
    check("OPEN_M_B" in transition_source["R17"]["middle_state_rule"], "source R17 calibration reset open")
    check(transition_source["R18"]["middle_state_rule"] == "ONE_SHARED_KILLING_CLOCK_STATE",
          "source R18 shared clock state")
    check(transition_source["R23"]["nonisometric_transition"] == "NONE__OWNED_PATH_ARROW_IS_METRIC_COMPATIBLE",
          "source R23 isometric-only")
    check("SET_OWNED_SINGLE_MEMBER_UNOWNED" in transition_source["R24"]["middle_state_rule"],
          "source R24 set/member distinction")
    check(g55_source[("R04", "A03")]["disposition"] == "INSUFFICIENT_EVIDENCE",
          "source R04 aggregate correction")
    check(global_source["R15"]["primary_disposition"] == "NO_COMPLETE_FAMILY_ON_DECLARED_BRANCH",
          "source R15 local-only")

    # Independent axis-by-axis reconstruction. This is organized by output sets, not by the
    # production script's branch vectors or its decision procedure.
    expected: dict[str, dict[str, set[str]]] = {
        "D01": {
            "OWNED_EXACT": {"R13", "R14", "R17", "R18", "R19", "R20", "R22", "R23", "R24"},
            "MEMBER_DEPENDENT": {"R04"},
            "TYPE_INAPPLICABLE": {"R06", "R15", "R16", "R21"},
        },
        "D02": {
            "OWNED_EXACT": {"R17"},
            "CONDITIONAL_AFTER_QUERY": {"R13", "R14", "R15"},
            "MEMBER_DEPENDENT": {"R04"},
            "OPEN_OWNER": {"R18", "R19", "R20", "R22", "R23"},
            "TYPE_INAPPLICABLE": {"R06", "R16", "R21", "R24"},
        },
        "D03": {
            "OWNED_EXACT": {"R17"},
            "MEMBER_DEPENDENT": {"R04"},
            "OPEN_OWNER": {"R13", "R14", "R18", "R19", "R20", "R22", "R23"},
            "TYPE_INAPPLICABLE": {"R06", "R15", "R16", "R21", "R24"},
        },
        "D04": {
            "OWNED_EXACT": {"R18"},
            "CONDITIONAL_AFTER_QUERY": {"R13", "R14", "R22"},
            "PATH_LABELLED_HOLONOMY": {"R17", "R19", "R23", "R24"},
            "MEMBER_DEPENDENT": {"R04", "R20"},
            "TYPE_INAPPLICABLE": {"R06", "R15", "R16", "R21"},
        },
        "D05": {
            "OWNED_EXACT": {"R17", "R18"},
            "MEMBER_DEPENDENT": {"R04", "R24"},
            "OPEN_OWNER": {"R13", "R14", "R19", "R20", "R22", "R23"},
            "TYPE_INAPPLICABLE": {"R06", "R15", "R16", "R21"},
        },
        "D06": {
            "OWNED_EXACT": {"R18"},
            "MEMBER_DEPENDENT": {"R04", "R24"},
            "OPEN_OWNER": {"R13", "R14", "R17", "R19", "R20", "R22", "R23"},
            "TYPE_INAPPLICABLE": {"R06", "R15", "R16", "R21"},
        },
        "D07": {
            "OWNED_EXACT": {"R18"},
            "CONDITIONAL_AFTER_QUERY": {"R13", "R14", "R22"},
            "PATH_LABELLED_HOLONOMY": {"R17", "R19", "R23", "R24"},
            "MEMBER_DEPENDENT": {"R04", "R20"},
            "TYPE_INAPPLICABLE": {"R06", "R15", "R16", "R21"},
        },
        "D08": {
            "PATH_LABELLED_HOLONOMY": {"R13", "R14", "R17", "R19", "R23", "R24"},
            "MEMBER_DEPENDENT": {"R04", "R20"},
            "TYPE_INAPPLICABLE": {"R06", "R15", "R16", "R18", "R21", "R22"},
        },
        "D09": {
            "CONDITIONAL_AFTER_QUERY": {"R13", "R14", "R15", "R17", "R20", "R23"},
            "OPEN_OWNER": {"R18", "R19", "R22"},
            "TYPE_INAPPLICABLE": {"R06", "R16", "R21", "R24"},
        },
        "D10": {
            "MEMBER_DEPENDENT": {"R04"},
            "OPEN_OWNER": {"R13", "R14", "R17", "R18", "R19", "R20", "R22", "R23"},
            "TYPE_INAPPLICABLE": {"R06", "R15", "R16", "R21", "R24"},
        },
    }
    all_statuses = {
        "OWNED_EXACT", "CONDITIONAL_AFTER_QUERY", "PATH_LABELLED_HOLONOMY",
        "MEMBER_DEPENDENT", "OPEN_OWNER", "INSUFFICIENT_EVIDENCE", "TYPE_INAPPLICABLE",
    }
    for axis, groups in expected.items():
        assigned: set[str] = set()
        for status, group in groups.items():
            check(all(cells[(branch, axis)] == status for branch in group), f"{axis} {status} set")
            assigned |= group
        remainder = branches - assigned
        check(all(cells[(branch, axis)] == "INSUFFICIENT_EVIDENCE" for branch in remainder),
              f"{axis} insufficient remainder")
        check(assigned | remainder == branches, f"{axis} complete partition")
        check(set(groups) <= all_statuses, f"{axis} allowed status vocabulary")

    counts = Counter(cells.values())
    check(dict(sorted(counts.items())) == {
        "CONDITIONAL_AFTER_QUERY": 15,
        "INSUFFICIENT_EVIDENCE": 101,
        "MEMBER_DEPENDENT": 14,
        "OPEN_OWNER": 36,
        "OWNED_EXACT": 16,
        "PATH_LABELLED_HOLONOMY": 14,
        "TYPE_INAPPLICABLE": 44,
    }, "global disposition counts")
    check(not any(cells[(branch, "D10")] == "OWNED_EXACT" for branch in branches),
          "zero complete selector owners")
    check(cells[("R04", "D09")] == "INSUFFICIENT_EVIDENCE", "R04 correction retained")
    check(cells[("R17", "D02")] == cells[("R17", "D03")] == "OWNED_EXACT",
          "R17 global pair foliation retained")
    check(cells[("R17", "D05")] == "OWNED_EXACT", "R17 alignment bitorsor retained")
    check(cells[("R17", "D06")] == "OPEN_OWNER", "R17 calibration reset seam retained")
    check(cells[("R18", "D04")] == cells[("R18", "D07")] == "OWNED_EXACT",
          "R18 clock-only descent retained")
    check(cells[("R23", "D04")] == "PATH_LABELLED_HOLONOMY",
          "R23 path family retained")
    check(cells[("R24", "D05")] == "MEMBER_DEPENDENT",
          "R24 set/member distinction retained")

    result = {"status": "PASS", "passed": len(checks), "total": len(checks), "checks": checks}
    if args.check_only:
        assert json.loads((HERE / "INDEPENDENT_VERIFICATION_RESULT.json").read_text(encoding="utf-8")) == result
    else:
        (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(f"PASS: independent descent reconstruction {len(checks)}/{len(checks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
