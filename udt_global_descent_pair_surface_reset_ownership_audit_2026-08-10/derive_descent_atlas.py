#!/usr/bin/env python3
"""Build the preregistered 24 x 10 global-descent ownership atlas."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

INS = "INSUFFICIENT_EVIDENCE"
TYPE = "TYPE_INAPPLICABLE"
OWN = "OWNED_EXACT"
COND = "CONDITIONAL_AFTER_QUERY"
PATH = "PATH_LABELLED_HOLONOMY"
MEMBER = "MEMBER_DEPENDENT"
OPEN = "OPEN_OWNER"


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(name: str, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_rows(source_id: str) -> list[dict[str, str]]:
    manifest = {row["source_id"]: row for row in table(HERE / "SOURCE_MANIFEST.tsv")}
    direct = ROOT / manifest[source_id]["path"]
    sealed = ROOT / "sources" / manifest[source_id]["path"]
    return table(direct if direct.exists() else sealed)


# Semantic rulings over the exact pinned corpus. Each row follows D01..D10. These are deliberately
# explicit rather than inferred from branch names. Source-field consistency assertions below fail
# closed if the pinned parent classifications no longer support the ruling.
RULINGS: dict[str, tuple[str, ...]] = {
    "R01": (INS, INS, INS, INS, INS, INS, INS, INS, INS, INS),
    "R02": (INS, INS, INS, INS, INS, INS, INS, INS, INS, INS),
    "R03": (INS, INS, INS, INS, INS, INS, INS, INS, INS, INS),
    "R04": (MEMBER, MEMBER, MEMBER, MEMBER, MEMBER, MEMBER, MEMBER, MEMBER, INS, MEMBER),
    "R05": (INS, INS, INS, INS, INS, INS, INS, INS, INS, INS),
    "R06": (TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE),
    "R07": (INS, INS, INS, INS, INS, INS, INS, INS, INS, INS),
    "R08": (INS, INS, INS, INS, INS, INS, INS, INS, INS, INS),
    "R09": (INS, INS, INS, INS, INS, INS, INS, INS, INS, INS),
    "R10": (INS, INS, INS, INS, INS, INS, INS, INS, INS, INS),
    "R11": (INS, INS, INS, INS, INS, INS, INS, INS, INS, INS),
    "R12": (INS, INS, INS, INS, INS, INS, INS, INS, INS, INS),
    "R13": (OWN, COND, OPEN, COND, OPEN, OPEN, COND, PATH, COND, OPEN),
    "R14": (OWN, COND, OPEN, COND, OPEN, OPEN, COND, PATH, COND, OPEN),
    "R15": (TYPE, COND, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, COND, TYPE),
    "R16": (TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE),
    "R17": (OWN, OWN, OWN, PATH, OWN, OPEN, PATH, PATH, COND, OPEN),
    "R18": (OWN, OPEN, OPEN, OWN, OWN, OWN, OWN, TYPE, OPEN, OPEN),
    "R19": (OWN, OPEN, OPEN, PATH, OPEN, OPEN, PATH, PATH, OPEN, OPEN),
    "R20": (OWN, OPEN, OPEN, MEMBER, OPEN, OPEN, MEMBER, MEMBER, COND, OPEN),
    "R21": (TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE, TYPE),
    "R22": (OWN, OPEN, OPEN, COND, OPEN, OPEN, COND, TYPE, OPEN, OPEN),
    "R23": (OWN, OPEN, OPEN, PATH, OPEN, OPEN, PATH, PATH, COND, OPEN),
    "R24": (OWN, TYPE, TYPE, PATH, MEMBER, MEMBER, PATH, PATH, TYPE, TYPE),
}


def evidence(branch: str, axis: str) -> str:
    if axis == "D01":
        return f"S04::{branch}"
    if axis in {"D02", "D03"}:
        return f"S05::{branch}" + (";S13::C01-C05;S14" if branch == "R17" else "")
    if axis in {"D04", "D07", "D08"}:
        extra = ";S15;S16" if branch == "R17" else ""
        return f"S05::{branch};S08::{branch}{extra}"
    if axis in {"D05", "D06"}:
        extra = ";S10::C01-C06;S11::M01-M12;S12" if branch == "R17" else ""
        return f"S05::{branch};S08::{branch}{extra}"
    if axis == "D09":
        return f"S03::{branch}/A03;S18::M02"
    return f"S02::{branch};S05::{branch}"


def caveat(branch: str, axis: str, disposition: str) -> str:
    special = {
        ("R04", "D09"): "G55 correction forbids inheriting a member reciprocal panel into the aggregate class.",
        ("R17", "D02"): "The owned foliation is a family of Hopf-cylinder leaves; no one physical leaf is selected.",
        ("R17", "D03"): "Global on the regular supplied stationary R17 configuration, not across excluded degeneracies or time-live branches.",
        ("R17", "D05"): "The metric owns the full SO(2) alignment bitorsor and its representative-free balanced composition; one calibration representative remains unselected.",
        ("R17", "D06"): "Projector alignment composes, but calibration-density reset and one representative remain open.",
        ("R17", "D10"): "Surface, path functor, and terminal readout are partial links; the physical query/path/reset selector remains open.",
        ("R18", "D04"): "Exact only for the one shared Killing clock state; no intrinsic ruler or complete pair flag is owned.",
        ("R18", "D05"): "The shared middle object is the clock line only.",
        ("R18", "D06"): "Identity carry is exact for the shared clock state, not a complete reciprocal pair reset.",
        ("R18", "D07"): "Endpoint clock coboundary descends exactly; complete pair descent remains open.",
        ("R24", "D04"): "Exact only as set-equivariant projector transport with tie-wall branches retained.",
        ("R24", "D05"): "The unordered set is owned; one selected member is not.",
        ("R24", "D06"): "Set transport does not own a clock/ruler calibration reset.",
    }
    if (branch, axis) in special:
        return special[(branch, axis)]
    generic = {
        OWN: "Exact only in the declared branch-scoped object named by the evidence.",
        COND: "Requires supplied query, path, orientation, or presentation data and is not physical ownership.",
        PATH: "Composition is path-labelled and any recorded holonomy is retained rather than erased.",
        MEMBER: "The aggregate or choice family contains inequivalent member-level answers and selects none.",
        OPEN: "The pinned corpus contains a relevant structure but no owner for this link.",
        INS: "The pinned corpus lacks an actual typed complete witness for this link.",
        TYPE: "The declared object is absent, local-only, singular, transitional, or of the wrong type for this link.",
    }
    return generic[disposition]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true", help="verify existing outputs without writing")
    args = parser.parse_args()
    branches = source_rows("S04")
    axes = table(HERE / "DESCENT_AXES.tsv")
    globals_by_id = {row["branch_id"]: row for row in source_rows("S05")}
    profiles = {row["branch_id"]: row for row in source_rows("S02")}
    matrix = {(row["branch_id"], row["axis_id"]): row for row in source_rows("S03")}
    transitions = {row["branch_id"]: row for row in source_rows("S08")}

    ids = [row["branch_id"] for row in branches]
    assert ids == [f"R{i:02d}" for i in range(1, 25)]
    assert set(ids) == set(RULINGS) == set(globals_by_id) == set(profiles) == set(transitions)
    assert [row["axis_id"] for row in axes] == [f"D{i:02d}" for i in range(1, 11)]
    assert all(len(RULINGS[branch]) == 10 for branch in ids)

    # Fail closed on the highest-risk semantic inputs.
    assert globals_by_id["R17"]["primary_disposition"] == "PATH_BRANCH_GROUPOID_OWNED"
    assert "GLOBAL_FIXED_RANK" in globals_by_id["R17"]["overlap_domain_and_rank"]
    assert "PATH_STATE_CARRIED" in globals_by_id["R17"]["middle_state_ownership"]
    assert "OPEN_M_B" in transitions["R17"]["middle_state_rule"]
    assert globals_by_id["R18"]["primary_disposition"] == "COMMON_CALIBRATED_ATLAS_OWNED"
    assert transitions["R18"]["middle_state_rule"] == "ONE_SHARED_KILLING_CLOCK_STATE"
    assert transitions["R23"]["nonisometric_transition"] == "NONE__OWNED_PATH_ARROW_IS_METRIC_COMPATIBLE"
    assert "SET_OWNED_SINGLE_MEMBER_UNOWNED" in transitions["R24"]["middle_state_rule"]
    assert matrix[("R04", "A03")]["disposition"] == "INSUFFICIENT_EVIDENCE"
    assert profiles["R04"]["pattern_family"] == "F02_AGGREGATE_MEMBER_DEPENDENT"

    branch_by_id = {row["branch_id"]: row for row in branches}
    rows: list[dict[str, object]] = []
    for branch in ids:
        for idx, axis_row in enumerate(axes):
            axis = axis_row["axis_id"]
            disposition = RULINGS[branch][idx]
            assert disposition in axis_row["allowed_outputs"].split(";")
            rows.append({
                "branch_id": branch,
                "stable_identity": branch_by_id[branch]["stable_identity"],
                "axis_id": axis,
                "disposition": disposition,
                "scope_caveat": caveat(branch, axis, disposition),
                "evidence": evidence(branch, axis),
            })
    assert len(rows) == len({(row["branch_id"], row["axis_id"]) for row in rows}) == 240
    atlas_fields = ["branch_id", "stable_identity", "axis_id", "disposition", "scope_caveat", "evidence"]
    if args.check_only:
        assert table(HERE / "GLOBAL_DESCENT_ATLAS.tsv") == rows
    else:
        write_tsv("GLOBAL_DESCENT_ATLAS.tsv", atlas_fields, rows)

    summaries: list[dict[str, object]] = []
    for branch in ids:
        cells = [row for row in rows if row["branch_id"] == branch]
        counts = Counter(row["disposition"] for row in cells)
        complete = all(row["disposition"] == OWN for row in cells)
        summaries.append({
            "branch_id": branch,
            "stable_identity": branch_by_id[branch]["stable_identity"],
            "owned_exact_axes": counts[OWN],
            "conditional_axes": counts[COND],
            "path_holonomy_axes": counts[PATH],
            "member_dependent_axes": counts[MEMBER],
            "open_axes": counts[OPEN],
            "insufficient_axes": counts[INS],
            "type_inapplicable_axes": counts[TYPE],
            "complete_descent_selector": "YES" if complete else "NO",
        })
    summary_fields = ["branch_id", "stable_identity", "owned_exact_axes", "conditional_axes",
                      "path_holonomy_axes", "member_dependent_axes", "open_axes", "insufficient_axes",
                      "type_inapplicable_axes", "complete_descent_selector"]
    if args.check_only:
        expected_summary = [{key: str(value) for key, value in row.items()} for row in summaries]
        assert table(HERE / "BRANCH_DESCENT_SUMMARY.tsv") == expected_summary
    else:
        write_tsv("BRANCH_DESCENT_SUMMARY.tsv", summary_fields, summaries)

    counts = Counter(row["disposition"] for row in rows)
    result = {
        "status": "PASS",
        "branch_count": len(ids),
        "axis_count": len(axes),
        "cell_count": len(rows),
        "disposition_counts": dict(sorted(counts.items())),
        "complete_descent_selector_count": sum(
            row["complete_descent_selector"] == "YES" for row in summaries
        ),
        "r17_owned_links": [
            row["axis_id"] for row in rows
            if row["branch_id"] == "R17" and row["disposition"] == OWN
        ],
        "r18_owned_links": [
            row["axis_id"] for row in rows
            if row["branch_id"] == "R18" and row["disposition"] == OWN
        ],
        "r17_open_links": [
            row["axis_id"] for row in rows
            if row["branch_id"] == "R17" and row["disposition"] == OPEN
        ],
        "landing": "NO_COMPLETE_DESCENT_SELECTOR_IN_PINNED_CORPUS",
    }
    if args.check_only:
        assert json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")) == result
    else:
        (HERE / "DERIVATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    print("atlas_sha256", hashlib.sha256((HERE / "GLOBAL_DESCENT_ATLAS.tsv").read_bytes()).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
