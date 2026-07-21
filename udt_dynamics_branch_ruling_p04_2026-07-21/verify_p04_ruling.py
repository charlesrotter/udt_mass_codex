#!/usr/bin/env python3
"""Independent mechanical verifier and corruption catches for P04."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULT = HERE / "RULING_RESULT.json"
MAXIMUM = "DYNAMICS_LANES_AUTHORIZED_OR_REMAIN_OPEN"
TABLES = [
    "DYNAMICS_BRANCH_DISPATCH.tsv",
    "LAW_PREMISE_MANIFEST.tsv",
    "FIELD_REALIZATION_COMPATIBILITY.tsv",
    "GLOBAL_AXIS_CARRYFORWARD.tsv",
    "P05_ENTRY_GATES.tsv",
    "AUTHORITY_AND_STOP_LEDGER.tsv",
    "SOURCE_LINEAGE.tsv",
]
SOURCES = {
    "P03G_MANIFEST": ("udt_global_kinematic_assembly_p03g_2026-07-21/SHA256SUMS.txt", "62f9b3f33409b62fb841734e8a91e61d9b859247bf808c4a6cf3740b6a54b6c9"),
    "P03_MANIFEST": ("udt_founded_constraint_atlas_p03_2026-07-21/SHA256SUMS.txt", "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be"),
    "COMPLETE_MAP_MANIFEST": ("udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt", "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38"),
    "FINAL_ACTION_MANIFEST": ("native_action_final_adjudication_2026-07-18/SHA256SUMS.txt", "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33"),
    "SELECTOR_AUDIT": ("UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md", "db4a426b021e375fa4bca0d870aaf973de319de3b08072195d001a056630832d"),
    "SELECTOR_PREREG": ("UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md", "6a835388e8f7a82a4bb4b9496f99c4a5e4181f5e5ccb2637641a1b4346922cc6"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load():
    return json.loads(RESULT.read_text(encoding="utf-8")), {name: rows(HERE / name) for name in TABLES}


def validate(result: dict, tables: dict[str, list[dict[str, str]]]) -> None:
    require(result["schema"] == "udt-p04-dynamics-branch-ruling-1.0", "schema")
    require(result["status"] == "PASS", "status")
    require(result["evidence_grade"] == "OWNER_AUTHORIZED_CONDITIONAL_DISPATCH_VERIFIED", "grade")
    require(result["maximum_conclusion"] == MAXIMUM, "maximum")
    require(result["controlling_scientific_status"] == "NO_DYNAMICS_DERIVED", "controlling status")
    require(result["counts"] == {"authorized_lanes": 3, "derived_lanes": 0, "field_realization_pairs": 21, "field_realizations_removed": 0, "global_axes_carried_free": 12, "solve_authorizations": 0, "premise_rows": 18}, "counts")
    require(result["lane_rulings"] == {"L01": "UNIQUE_CONDITIONAL_BULK_CLASS_NOT_COMPLETE_ACTION", "L02": "CONDITIONAL_BULK_NOT_NATIVE_UDT_ACTION", "L03": "OPEN_NO_ACTION_OPERATOR_OR_MATCHING_MAP"}, "lane rulings")
    require(not any(result["scope"][key] for key in ("GPU_used", "symbolic_variation_performed", "equations_built", "ODE_or_PDE_run", "comparison_loaded", "P05_launched", "canon_changed")), "scope")

    lanes = tables["DYNAMICS_BRANCH_DISPATCH.tsv"]
    require(len(lanes) == 3 and {row["lane_id"] for row in lanes} == {"L01", "L02", "L03"}, "lane coverage")
    require(len({row["lane_id"] for row in lanes}) == 3, "lane duplicates")
    lane = {row["lane_id"]: row for row in lanes}
    require(all("DERIVED" not in row["epistemic_status"] and row["solve_authority"] == "NONE" for row in lanes), "lane promotion")
    require(lane["L01"]["epistemic_status"] == "UNIQUE_CONDITIONAL_BULK_CLASS_NOT_COMPLETE_ACTION", "C2 status")
    require("before_physical_scale_selection" in lane["L01"]["variation_domain"], "C2 variation stage")
    require(lane["L02"]["epistemic_status"] == "CONDITIONAL_BULK_NOT_NATIVE_UDT_ACTION", "EH status")
    require("after_representative_and_scale_selection" in lane["L02"]["variation_domain"], "EH variation stage")
    require(lane["L03"]["epistemic_status"] == "OPEN_NO_ACTION_OPERATOR_OR_MATCHING_MAP" and lane["L03"]["operator_readiness"].startswith("NOT_OPERATOR_READY"), "bridge status")
    require(all(row["boundary_status"].startswith("OPEN") and row["source_status"].startswith("OPEN") for row in lanes), "boundary source open")

    premises = tables["LAW_PREMISE_MANIFEST.tsv"]
    require(len(premises) == 18 and {row["id"] for row in premises} == {f"P{i:02d}" for i in range(1, 19)}, "premise coverage")
    require(len({row["id"] for row in premises}) == 18 and all(row["source"] for row in premises), "premise uniqueness citations")
    premise = {row["id"]: row for row in premises}
    require(premise["P01"]["premise_or_status"] == "No dynamics is presently derived", "owner status")
    require(premise["P03"]["stamp"] == "OPEN", "field census")
    require(premise["P11"]["stamp"] == "OPEN_NOT_SUPPLIED", "bridge map")
    require(premise["P13"]["stamp"] == "OPEN", "boundary premise")
    require(premise["P16"]["stamp"] == "DOWNSTREAM_CALIBRATION_ONLY", "anchors")
    require(premise["P17"]["stamp"] == "EXCLUDED", "merit")
    require(premise["P18"]["stamp"] == "NONE_IN_P04", "solve")

    compat = tables["FIELD_REALIZATION_COMPATIBILITY.tsv"]
    require(len(compat) == 21 and len({row["pair_id"] for row in compat}) == 21, "pair count")
    require({row["lane_id"] for row in compat} == {"L01", "L02", "L03"} and {row["realization_id"] for row in compat} == {f"C{i:02d}" for i in range(1, 8)}, "pair axes")
    require({(row["lane_id"], row["realization_id"]) for row in compat} == {(lane_id, realization) for lane_id in ("L01", "L02", "L03") for realization in ("C01", "C02", "C03", "C04", "C05", "C06", "C07")}, "pair Cartesian product")
    require(all(row["field_removed"] == "NO" and row["globally_realized"] == "UNEVALUATED" for row in compat), "field/global preservation")
    require(next(row for row in compat if row["pair_id"] == "L01_C02")["compatibility_status"] == "BLOCKED_UNGOVERNED_EXTRA_FIELD", "C2 independent phi")
    require(next(row for row in compat if row["pair_id"] == "L02_C07")["compatibility_status"] == "BLOCKED_UNGOVERNED_EXTRA_FIELD", "EH connection")
    require(next(row for row in compat if row["pair_id"] == "L03_C06")["compatibility_status"] == "NATIVE_BRANCH_MATCH_BUT_OPERATOR_OPEN", "bridge branch")

    axes = tables["GLOBAL_AXIS_CARRYFORWARD.tsv"]
    require(len(axes) == 12 and {row["axis_id"] for row in axes} == {f"A{i:02d}" for i in range(1, 13)}, "axis coverage")
    require(all(row["p04_disposition"] == "FREE_AND_UNSELECTED_IN_ALL_THREE_LANES" and row["selection_or_value"] == "NONE" for row in axes), "axis selection")
    source_axes = rows(ROOT / "udt_global_kinematic_assembly_p03g_2026-07-21/GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv")
    require({(row["axis_id"], row["object"]) for row in axes} == {(row["axis_id"], row["object"]) for row in source_axes}, "axis identity")

    gates = tables["P05_ENTRY_GATES.tsv"]
    require(len(gates) == 3 and {row["lane_id"] for row in gates} == {"L01", "L02", "L03"}, "P05 gates")
    require(all(row["entry_status"] in {"SEPARATE_P05_DISPATCH_REQUIRED", "NOT_OPERATOR_READY"} for row in gates), "P05 authority")
    require(next(row for row in gates if row["lane_id"] == "L03")["entry_status"] == "NOT_OPERATOR_READY", "bridge entry")

    stops = tables["AUTHORITY_AND_STOP_LEDGER.tsv"]
    require(len(stops) == 13 and {row["id"] for row in stops} == {f"S{i:02d}" for i in range(1, 14)}, "stop ledger")
    stop = {row["id"]: row for row in stops}
    require(stop["S01"]["status"] == "NO_DYNAMICS_DERIVED", "stop control")
    require(stop["S05"]["status"] == "21_OF_21_ACCOUNTED_NONE_REMOVED", "stop pairs")
    require(stop["S06"]["status"] == "12_OF_12_FREE_AND_UNSELECTED", "stop axes")
    require(stop["S10"]["status"] == "NOT_LAUNCHED" and stop["S11"]["status"] == "NOT_AUTHORIZED", "stop P05 solve")
    require(stop["S13"]["status"] == MAXIMUM, "stop maximum")

    lineage = tables["SOURCE_LINEAGE.tsv"]
    require(len(lineage) == 6 and {row["role"] for row in lineage} == set(SOURCES), "source coverage")
    for row in lineage:
        path, expected = SOURCES[row["role"]]
        require(row["path"] == path and row["sha256"] == expected and digest(ROOT / path) == expected, f"source {row['role']}")
        require(result["source_sha256"][row["role"]] == expected, f"result source {row['role']}")
    for name, expected in result["table_sha256"].items():
        require(digest(HERE / name) == expected, f"table hash {name}")


def expect_failure(name: str, operation, catches: dict[str, str]) -> None:
    try:
        operation()
    except (AssertionError, KeyError, StopIteration, ValueError):
        catches[name] = "PASS"
        return
    raise AssertionError(f"mutation passed: {name}")


def main() -> None:
    tracked = [RESULT, *[HERE / name for name in TABLES]]
    before = {path.name: digest(path) for path in tracked}
    environment = dict(os.environ); environment["PYTHONDONTWRITEBYTECODE"] = "1"; environment["CUDA_VISIBLE_DEVICES"] = ""
    replay = subprocess.run([sys.executable, "-B", str(HERE / "build_p04_ruling.py")], cwd=ROOT, env=environment, text=True, capture_output=True, timeout=300, check=False)
    require(replay.returncode == 0 and not replay.stderr, replay.stdout + replay.stderr)
    require(replay.stdout == (HERE / "RULING_TRANSCRIPT.txt").read_text(encoding="utf-8"), "transcript replay")
    require(before == {path.name: digest(path) for path in tracked}, "deterministic replay")
    result, tables = load()
    validate(result, tables)
    checks = {"deterministic_replay_and_contract": "PASS", "owner_ruling_exact_three_lane_interpretation": "PASS", "independent_3x7_Cartesian_reconciliation": "PASS", "independent_12_axis_identity_reconciliation": "PASS", "source_hash_replay": "PASS", "zero_solve_authority": "PASS"}

    catches: dict[str, str] = {}
    bad = copy.deepcopy(result); bad["schema"] = "bad"
    expect_failure("schema", lambda: validate(bad, tables), catches)
    bad = copy.deepcopy(result); bad["controlling_scientific_status"] = "DYNAMICS_DERIVED"
    expect_failure("derived_control", lambda: validate(bad, tables), catches)
    bad = copy.deepcopy(result); bad["counts"]["derived_lanes"] = 1
    expect_failure("derived_count", lambda: validate(bad, tables), catches)
    bad = copy.deepcopy(result); bad["scope"]["P05_launched"] = True
    expect_failure("P05_launch", lambda: validate(bad, tables), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["DYNAMICS_BRANCH_DISPATCH.tsv"].pop()
    expect_failure("missing_lane", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["DYNAMICS_BRANCH_DISPATCH.tsv"].append(copy.deepcopy(bad_tables["DYNAMICS_BRANCH_DISPATCH.tsv"][0]))
    expect_failure("duplicate_lane", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["DYNAMICS_BRANCH_DISPATCH.tsv"] if row["lane_id"] == "L01")["epistemic_status"] = "DERIVED_NATIVE"
    expect_failure("C2_promotion", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["DYNAMICS_BRANCH_DISPATCH.tsv"] if row["lane_id"] == "L02")["epistemic_status"] = "NATIVE_UDT_ACTION"
    expect_failure("EH_promotion", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["DYNAMICS_BRANCH_DISPATCH.tsv"] if row["lane_id"] == "L03")["operator_readiness"] = "OPERATOR_READY"
    expect_failure("bridge_operator_invention", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["DYNAMICS_BRANCH_DISPATCH.tsv"] if row["lane_id"] == "L01")["solve_authority"] = "AUTHORIZED"
    expect_failure("solve_authority", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["DYNAMICS_BRANCH_DISPATCH.tsv"] if row["lane_id"] == "L02")["boundary_status"] = "GHY_ADOPTED"
    expect_failure("boundary_import", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["DYNAMICS_BRANCH_DISPATCH.tsv"] if row["lane_id"] == "L01")["source_status"] = "S2_SOURCE_ADOPTED"
    expect_failure("source_import", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["FIELD_REALIZATION_COMPATIBILITY.tsv"].pop()
    expect_failure("missing_pair", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["FIELD_REALIZATION_COMPATIBILITY.tsv"].append(copy.deepcopy(bad_tables["FIELD_REALIZATION_COMPATIBILITY.tsv"][0]))
    expect_failure("duplicate_pair", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["FIELD_REALIZATION_COMPATIBILITY.tsv"] if row["pair_id"] == "L01_C02")["field_removed"] = "YES"
    expect_failure("independent_phi_removed", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["FIELD_REALIZATION_COMPATIBILITY.tsv"] if row["pair_id"] == "L02_C07")["globally_realized"] = "YES"
    expect_failure("global_realization_promoted", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); bad_tables["GLOBAL_AXIS_CARRYFORWARD.tsv"].pop()
    expect_failure("missing_global_axis", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["GLOBAL_AXIS_CARRYFORWARD.tsv"] if row["axis_id"] == "A09")["selection_or_value"] = "S3"
    expect_failure("topology_selected", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["LAW_PREMISE_MANIFEST.tsv"] if row["id"] == "P16")["stamp"] = "PRE_SCALE_SELECTOR"
    expect_failure("anchor_promoted", lambda: validate(result, bad_tables), catches)
    bad_tables = copy.deepcopy(tables); next(row for row in bad_tables["LAW_PREMISE_MANIFEST.tsv"] if row["id"] == "P17")["stamp"] = "GR_MERIT"
    expect_failure("merit_import", lambda: validate(result, bad_tables), catches)
    bad = copy.deepcopy(result); bad["source_sha256"]["P03G_MANIFEST"] = "0" * 64
    expect_failure("source_hash_drift", lambda: validate(bad, tables), catches)
    bad = copy.deepcopy(result); bad["table_sha256"]["AUTHORITY_AND_STOP_LEDGER.tsv"] = "0" * 64
    expect_failure("table_hash_drift", lambda: validate(bad, tables), catches)
    require(len(catches) == 22 and set(catches.values()) == {"PASS"}, "catch count")

    output = {
        "schema": "udt-p04-dynamics-branch-ruling-verification-1.0",
        "status": "PASS",
        "check_count": len(checks),
        "checks": checks,
        "catch_proof_count": len(catches),
        "catch_proofs": catches,
        "main_result_sha256": digest(RESULT),
        "main_transcript_sha256": digest(HERE / "RULING_TRANSCRIPT.txt"),
        "scope": {"independent_implementation": True, "generator_imported": False, "CPU_only": True, "equations_or_solves": False},
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "P04_INDEPENDENT_VERIFICATION=PASS",
        f"checks={len(checks)}",
        f"catch_proofs={len(catches)}",
        "lanes=3_conditional_0_derived",
        "field_pairs=21/21_none_removed",
        "global_axes=12/12_free",
        "solve_authority=0",
        f"main_result_sha256={output['main_result_sha256']}",
    ]
    text = "\n".join(transcript) + "\n"
    (HERE / "VERIFICATION_TRANSCRIPT.txt").write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
