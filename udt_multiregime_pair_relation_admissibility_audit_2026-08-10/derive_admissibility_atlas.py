#!/usr/bin/env python3
"""Build the preregistered branch-by-measurement and ownership-axis atlases."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

INS = "INSUFFICIENT_EVIDENCE"
COND = "CONDITIONALLY_AVAILABLE"
OPEN = "OPEN_OWNER"
TYPE = "TYPE_INAPPLICABLE"
FOUNDED = "FOUNDED_AFTER_PAIR_SUPPLIED"
GLOBAL = "GLOBAL_COMPLETION_OWNED"

PROFILE_MEMBERS = {
    "F01_SCHEMA_ONLY": ("R01", "R02", "R03", "R05", "R07", "R08", "R09", "R10", "R11"),
    "F02_AGGREGATE_MEMBER_DEPENDENT": ("R04",),
    "F03_NO_COMPLETE_REGULAR_BRANCH": ("R06", "R16", "R21"),
    "F04_HISTORICAL_REDERIVATION_REQUIRED": ("R12",),
    "F05_GLOBAL_METRIC_QUERY_UNOWNED": ("R13", "R14", "R20"),
    "F06_LOCAL_PROFILE_ONLY": ("R15",),
    "F07_FULL_RECIPROCAL_PATH_CONDITIONAL": ("R17",),
    "F08_CLOCK_ONLY": ("R18", "R22"),
    "F09_ZERO_ISOMETRIC_PATH_CONTROL": ("R19",),
    "F10_COMPLETE_SCREEN_PATH_NO_SCALE": ("R23",),
    "F11_SET_VALUED_PROJECTOR": ("R24",),
}

PROFILE_DESCRIPTION = {
    "F01_SCHEMA_ONLY": "completion or topology schema without an actual typed complete metric",
    "F02_AGGREGATE_MEMBER_DEPENDENT": "aggregate completion class whose members carry different apparatus",
    "F03_NO_COMPLETE_REGULAR_BRANCH": "singular absent or transition-stratum object rather than a complete regular branch",
    "F04_HISTORICAL_REDERIVATION_REQUIRED": "historical ansatz requiring current phi-orchestra rederivation",
    "F05_GLOBAL_METRIC_QUERY_UNOWNED": "global metric or control with natural candidates but no selected complete query",
    "F06_LOCAL_PROFILE_ONLY": "valid local relational profile without a complete global relation family",
    "F07_FULL_RECIPROCAL_PATH_CONDITIONAL": "intrinsic reciprocal grading plus endpoint depth and path transport; full assembly conditional",
    "F08_CLOCK_ONLY": "global or supplied clock relation without an intrinsic reciprocal ruler completion",
    "F09_ZERO_ISOMETRIC_PATH_CONTROL": "zero-depth control with isometric transport and unowned pair state",
    "F10_COMPLETE_SCREEN_PATH_NO_SCALE": "complete screen/coframe path groupoid without owned non-isometric scale",
    "F11_SET_VALUED_PROJECTOR": "stratified unordered projector transport without clock-ruler density",
}

MEASUREMENT_BY_PROFILE = {
    "F01_SCHEMA_ONLY": (INS, INS, INS, INS, INS, INS),
    # The aggregate owns the existence of unlike member types, not one class-wide
    # instrument panel.  Per-member availability is represented by the member rows
    # (for example R17 and R18), never inherited by the R04 aggregate itself.
    "F02_AGGREGATE_MEMBER_DEPENDENT": (INS, INS, INS, INS, INS, OPEN),
    "F03_NO_COMPLETE_REGULAR_BRANCH": (TYPE, TYPE, TYPE, TYPE, TYPE, INS),
    "F04_HISTORICAL_REDERIVATION_REQUIRED": (INS, INS, INS, INS, INS, INS),
    "F05_GLOBAL_METRIC_QUERY_UNOWNED": (COND, FOUNDED, COND, COND, OPEN, OPEN),
    "F06_LOCAL_PROFILE_ONLY": (OPEN, COND, OPEN, TYPE, TYPE, OPEN),
    "F07_FULL_RECIPROCAL_PATH_CONDITIONAL": (COND, FOUNDED, COND, COND, COND, OPEN),
    "F08_CLOCK_ONLY": (OPEN, OPEN, OPEN, OPEN, OPEN, OPEN),
    "F09_ZERO_ISOMETRIC_PATH_CONTROL": (OPEN, OPEN, OPEN, COND, OPEN, OPEN),
    "F10_COMPLETE_SCREEN_PATH_NO_SCALE": (COND, FOUNDED, COND, COND, INS, OPEN),
    "F11_SET_VALUED_PROJECTOR": (TYPE, TYPE, TYPE, TYPE, TYPE, OPEN),
}


def table_from_ref(source_ref: str) -> list[dict[str, str]]:
    raw = subprocess.check_output(["git", "show", source_ref], cwd=ROOT, text=True)
    return list(csv.DictReader(raw.splitlines(), delimiter="\t"))


def local_table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(name: str, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def profile_index() -> dict[str, str]:
    result: dict[str, str] = {}
    for profile, members in PROFILE_MEMBERS.items():
        for branch in members:
            assert branch not in result
            result[branch] = profile
    return result


def main() -> int:
    sources = {row["source_id"]: row for row in local_table("SOURCE_MANIFEST.tsv")}
    for row in sources.values():
        raw = subprocess.check_output(["git", "show", row["source_ref"]], cwd=ROOT)
        assert len(raw) == int(row["size"])
        assert hashlib.sha256(raw).hexdigest() == row["sha256"]

    branches = table_from_ref(sources["S10"]["source_ref"])
    relations = {row["branch_id"]: row for row in table_from_ref(sources["S11"]["source_ref"])}
    transitions = {row["branch_id"]: row for row in table_from_ref(sources["S15"]["source_ref"])}
    measurements = table_from_ref(sources["S03"]["source_ref"])
    regimes = table_from_ref(sources["S08"]["source_ref"])
    owners = table_from_ref(sources["S17"]["source_ref"])

    assert len(branches) == len(relations) == len(transitions) == 24
    assert len({row["branch_id"] for row in branches}) == 24
    assert len(measurements) == 6 and len({row["measurement_id"] for row in measurements}) == 6
    assert all(row["physical_regime"].startswith("OPEN") for row in regimes)
    assert any("OPEN" in row["selection_effect"] for row in owners)
    assert relations["R04"]["local_observer_query_object"] == "MEMBER_DEPENDENT"
    assert relations["R04"]["transition_or_path_arrow"] == "MEMBER_DEPENDENT"
    assert relations["R04"]["middle_state_ownership"] == "MEMBER_DEPENDENT"
    assert transitions["R04"]["intrinsic_clock_scale"] == "MEMBER_DEPENDENT"
    assert transitions["R04"]["intrinsic_ruler_or_grading"] == "MEMBER_DEPENDENT"
    assert transitions["R04"]["owned_geometric_transport"] == "MEMBER_DEPENDENT"
    assert transitions["R04"]["terminal_reciprocal_status"] == "NO_CLASS_WIDE_SCALAR"

    profiles = profile_index()
    assert set(profiles) == {row["branch_id"] for row in branches}
    branch_rows: list[dict[str, str]] = []
    for branch in branches:
        branch_id = branch["branch_id"]
        relation = relations[branch_id]
        transition = transitions[branch_id]
        profile = profiles[branch_id]
        branch_rows.append({
            "branch_id": branch_id,
            "stable_identity": branch["stable_identity"],
            "pattern_family": profile,
            "parent_relation_disposition": relation["primary_disposition"],
            "transition_disposition": transition["primary_disposition"],
            "pair_relation_owner": OPEN if profile not in {"F01_SCHEMA_ONLY", "F03_NO_COMPLETE_REGULAR_BRANCH", "F04_HISTORICAL_REDERIVATION_REQUIRED", "F11_SET_VALUED_PROJECTOR"} else (TYPE if profile in {"F03_NO_COMPLETE_REGULAR_BRANCH", "F11_SET_VALUED_PROJECTOR"} else INS),
            "owned_structural_restriction": (
                "GLOBAL_PATH_HOLONOMY_TYPE" if branch_id in {"R17", "R23"}
                else "GLOBAL_CLOCK_ONLY_TYPE" if branch_id == "R18"
                else "GLOBAL_STRATIFIED_MEMBER_TYPE" if branch_id == "R04"
                else "GLOBAL_SET_VALUED_PROJECTOR_TYPE" if branch_id == "R24"
                else "NONE_COMPLETE_AND_OWNED"
            ),
            "physical_regime_owner": OPEN if profile not in {"F01_SCHEMA_ONLY", "F03_NO_COMPLETE_REGULAR_BRANCH", "F04_HISTORICAL_REDERIVATION_REQUIRED"} else INS,
            "description": PROFILE_DESCRIPTION[profile],
            "evidence": f"S11::{branch_id};S15::{branch_id}",
        })

    measurement_rows: list[dict[str, str]] = []
    for branch in branches:
        branch_id = branch["branch_id"]
        profile = profiles[branch_id]
        statuses = list(MEASUREMENT_BY_PROFILE[profile])
        if branch_id == "R20":
            statuses[3] = OPEN
        for measurement, disposition in zip(measurements, statuses, strict=True):
            measurement_rows.append({
                "branch_id": branch_id,
                "stable_identity": branch["stable_identity"],
                "pattern_family": profile,
                "measurement_id": measurement["measurement_id"],
                "object": measurement["object"],
                "disposition": disposition,
                "ownership_boundary": (
                    "FOUNDING_SCALAR_ONLY_AFTER_PAIR" if disposition == FOUNDED
                    else "MATHEMATICAL_AVAILABILITY_NOT_PHYSICAL_SELECTION" if disposition == COND
                    else "NO_OWNER_IN_PINNED_CORPUS" if disposition == OPEN
                    else "SOURCE_EVIDENCE_INCOMPLETE" if disposition == INS
                    else "REQUIRED_OBJECT_TYPE_ABSENT"
                ),
                "evidence": f"S03::{measurement['measurement_id']};S11::{branch_id};S15::{branch_id}",
            })

    by_branch_measure = {
        (row["branch_id"], row["measurement_id"]): row["disposition"]
        for row in measurement_rows
    }
    global_owned = {"R04", "R17", "R18", "R23", "R24"}
    axis_rows: list[dict[str, str]] = []
    for branch in branches:
        branch_id = branch["branch_id"]
        profile = profiles[branch_id]
        pair_owner = next(row["pair_relation_owner"] for row in branch_rows if row["branch_id"] == branch_id)
        scalar_2 = by_branch_measure[(branch_id, "M02")]
        status = {
            "A01": pair_owner,
            "A02": COND if scalar_2 in {FOUNDED, COND} else scalar_2,
            "A03": scalar_2,
            "A04": by_branch_measure[(branch_id, "M01")],
            "A05": by_branch_measure[(branch_id, "M03")],
            "A06": by_branch_measure[(branch_id, "M04")],
            "A07": TYPE if profile in {"F03_NO_COMPLETE_REGULAR_BRANCH", "F06_LOCAL_PROFILE_ONLY", "F11_SET_VALUED_PROJECTOR"} else INS if profile in {"F01_SCHEMA_ONLY", "F04_HISTORICAL_REDERIVATION_REQUIRED"} else OPEN,
            "A08": TYPE if profile in {"F03_NO_COMPLETE_REGULAR_BRANCH", "F06_LOCAL_PROFILE_ONLY", "F11_SET_VALUED_PROJECTOR"} else INS if profile in {"F01_SCHEMA_ONLY", "F04_HISTORICAL_REDERIVATION_REQUIRED"} else OPEN,
            "A09": GLOBAL if branch_id in global_owned else COND if branch_id in {"R13", "R14", "R19", "R20", "R22"} else TYPE if profile in {"F03_NO_COMPLETE_REGULAR_BRANCH", "F06_LOCAL_PROFILE_ONLY"} else INS,
            "A10": OPEN if profile not in {"F01_SCHEMA_ONLY", "F03_NO_COMPLETE_REGULAR_BRANCH", "F04_HISTORICAL_REDERIVATION_REQUIRED"} else INS,
        }
        for axis_id, disposition in status.items():
            axis_rows.append({
                "branch_id": branch_id,
                "stable_identity": branch["stable_identity"],
                "axis_id": axis_id,
                "disposition": disposition,
                "evidence": f"S11::{branch_id};S15::{branch_id}",
            })

    pattern_rows = []
    for profile, members in PROFILE_MEMBERS.items():
        pattern_rows.append({
            "pattern_family": profile,
            "branch_count": str(len(members)),
            "branch_ids": ";".join(members),
            "mathematical_structure": PROFILE_DESCRIPTION[profile],
            "physical_regime_label": "OPEN_NOT_ASSIGNED",
        })

    assert len(branch_rows) == 24
    assert len(measurement_rows) == 144
    assert len(axis_rows) == 240
    assert len({(row["branch_id"], row["measurement_id"]) for row in measurement_rows}) == 144
    assert len({(row["branch_id"], row["axis_id"]) for row in axis_rows}) == 240
    assert not any(row["disposition"] in {"BRANCH_OWNED", GLOBAL} for row in axis_rows if row["axis_id"] == "A01")
    assert not any(row["disposition"] in {"BRANCH_OWNED", GLOBAL} for row in axis_rows if row["axis_id"] in {"A07", "A08", "A10"})
    assert sum(row["disposition"] == GLOBAL for row in axis_rows if row["axis_id"] == "A09") == 5

    write_tsv("BRANCH_ADMISSIBILITY_PROFILES.tsv", tuple(branch_rows[0]), branch_rows)
    write_tsv("BRANCH_MEASUREMENT_MATRIX.tsv", tuple(measurement_rows[0]), measurement_rows)
    write_tsv("BRANCH_AXIS_MATRIX.tsv", tuple(axis_rows[0]), axis_rows)
    write_tsv("GEOMETRIC_PATTERN_FAMILIES.tsv", tuple(pattern_rows[0]), pattern_rows)

    result = {
        "schema_version": 1,
        "status": "PASS",
        "branch_count": 24,
        "measurement_count": 6,
        "measurement_cells": 144,
        "axis_count": 10,
        "axis_cells": 240,
        "pattern_family_count": len(pattern_rows),
        "physical_pair_relation_owners": 0,
        "physical_nonisometric_arrow_owners": 0,
        "optional_measurement_selector_owners": 0,
        "physical_regime_owners": 0,
        "global_structural_restriction_owners": 5,
        "full_multichannel_conditional_branch": "R17",
        "measurement_disposition_counts": dict(sorted(Counter(row["disposition"] for row in measurement_rows).items())),
        "axis_disposition_counts": dict(sorted(Counter(row["disposition"] for row in axis_rows).items())),
        "maximum_ruling": "BRANCH_DEPENDENT_INSTRUMENT_AVAILABILITY_PATTERN_DERIVED__FIVE_GLOBAL_STRUCTURAL_RESTRICTIONS_OWNED__NO_PHYSICAL_PAIR_RELATION_MEASUREMENT_SELECTOR_OR_REGIME_MAP_OWNED",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
