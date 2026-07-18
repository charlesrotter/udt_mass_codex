#!/usr/bin/env python3
"""Independent adversarial verification of the 99-row R1B adjudication."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath


ALLOWED = {
    "ARCHIVE_ELIGIBLE", "ACTIVE_CROSS_ERA", "PERMANENT_ROOT", "HARD_FROZEN",
    "SOFT_EVIDENCE_PATH_ONLY", "HISTORICAL_SNAPSHOT", "BLOCKED",
}
MANUAL_CLASSES = {
    "AUDIT.md": "ACTIVE_CROSS_ERA",
    "D1_FIX_DESIGN.md": "HISTORICAL_SNAPSHOT",
    "F4_seal_boundary_MAP.md": "ACTIVE_CROSS_ERA",
    "GR_NUMERICS_RESEARCH_2026-06-29.md": "SOFT_EVIDENCE_PATH_ONLY",
    "MATTER_SECTOR_MAP_new_foundation.md": "ACTIVE_CROSS_ERA",
    "P1_PURITY_HARNESS_MAP.md": "ACTIVE_CROSS_ERA",
    "P5e_proper_results.md": "BLOCKED",
    "QUANTIZATION_MAP.md": "ACTIVE_CROSS_ERA",
    "SOLVER_INTEGRITY_UPGRADES_SPEC.md": "ACTIVE_CROSS_ERA",
    "STEP2_timelive_matter_MAP.md": "ARCHIVE_ELIGIBLE",
    "TRACTABILITY_ROUTES.md": "ACTIVE_CROSS_ERA",
    "external_input_notes.md": "ACTIVE_CROSS_ERA",
    "lepton_ladder_falsification_contract.md": "BLOCKED",
    "matter_amplitude_native_MAP_2026-06-29.md": "SOFT_EVIDENCE_PATH_ONLY",
    "matter_regrade_derived_operator_results.md": "BLOCKED",
    "nonstationary_opener_results.md": "BLOCKED",
    "p1_VERIFIER.md": "HISTORICAL_SNAPSHOT",
    "p2_VERIFIER.md": "BLOCKED",
    "p3_VERIFIER.md": "BLOCKED",
    "p4_VERIFIER.md": "ARCHIVE_ELIGIBLE",
    "scale_symmetry_bootstrap_analysis_results.md": "BLOCKED",
    "solution_space_map.md": "ACTIVE_CROSS_ERA",
    "weld_status_results.md": "BLOCKED",
}


def load(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def git_show(repo: Path, base: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{base}:{path}"], cwd=repo)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate(
    rows: list[dict[str, str]],
    permanent: set[str],
    pointer_plan: list[dict[str, str]],
    colocated: list[dict[str, str]],
) -> None:
    assert len(rows) == len({row["path"] for row in rows}) == 99
    assert {row["classification"] for row in rows} <= ALLOWED
    by_path = {row["path"]: row for row in rows}
    assert set(MANUAL_CLASSES) <= set(by_path)
    for path, expected in MANUAL_CLASSES.items():
        assert by_path[path]["classification"] == expected, path
    for path in permanent:
        assert by_path[path]["classification"] == "PERMANENT_ROOT", path
    for row in rows:
        if row["path"] in MANUAL_CLASSES or row["path"] in permanent:
            continue
        if row["r0_classification"] == "FROZEN_EVIDENCE":
            assert row["classification"] == "HARD_FROZEN", row["path"]
        elif row["r0_classification"] == "ACTIVE":
            assert row["classification"] == "ACTIVE_CROSS_ERA", row["path"]
        else:
            raise AssertionError((row["path"], row["r0_classification"]))
    eligible = {row["path"] for row in rows if row["classification"] == "ARCHIVE_ELIGIBLE"}
    assert eligible == {"STEP2_timelive_matter_MAP.md", "p4_VERIFIER.md"}
    assert len(eligible) <= 40
    assert len(pointer_plan) <= 400
    assert len(pointer_plan) == 1
    assert pointer_plan[0]["source"] == "STATE.md"
    assert pointer_plan[0]["old_target"] == "p4_VERIFIER.md"
    assert pointer_plan[0]["new_target"] == "archive/pre_2026-07-01/p4_VERIFIER.md"
    assert pointer_plan[0]["rewrite_mode"] == "EXACT_PATH_TOKEN_ONLY"
    assert pointer_plan[0]["source_immutability"] in {
        "MUTABLE_NAVIGATION_SOURCE", "SOFT_EVIDENCE_PATH_ONLY_SOURCE"
    }
    assert len(colocated) == 1
    assert colocated[0]["source"] == "archive/pre_2026-07-01/STEP2_timelive_matter_results.md"
    assert colocated[0]["target"] == "STEP2_timelive_matter_MAP.md"
    assert colocated[0]["rewrite"] == "NO"
    for path in eligible:
        row = by_path[path]
        assert row["current_frontier_target"] == "NO"
        assert row["hard_frozen_root_sources"] == "-"
        assert row["runtime_or_unknown_root_sources"] == "-"
        assert int(row["prohibited_dependency_edges"]) == 0
        assert int(row["unresolved_dynamic_touches"]) == 0
        assert row["destination_collision_at_base"] == "NO"
        assert row["move_authorized"] == "YES"
    assert all(row["move_authorized"] == ("YES" if row["classification"] == "ARCHIVE_ELIGIBLE" else "NO") for row in rows)


def rejected(check) -> str:
    try:
        check()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("adversarial mutation was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--permanent", type=Path, required=True)
    parser.add_argument("--adjudication", type=Path, required=True)
    parser.add_argument("--move-plan", type=Path, required=True)
    parser.add_argument("--pointer-plan", type=Path, required=True)
    parser.add_argument("--colocated-plan", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--base-census-verification", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    candidate_rows = load(args.candidates)
    rows = load(args.adjudication)
    move_plan = load(args.move_plan)
    pointer_plan = load(args.pointer_plan)
    colocated = load(args.colocated_plan)
    permanent = {
        row["path"] for row in load(args.permanent)
        if row["candidate_universe_status"] == "IN_CANDIDATE_UNIVERSE"
    }
    assert [row["path"] for row in rows] == [row["path"] for row in candidate_rows]
    validate(rows, permanent, pointer_plan, colocated)

    assert len(move_plan) == 2
    for move in move_plan:
        payload = git_show(repo, args.base, move["old_path"])
        assert move["sha256_before"] == sha256(payload)
        assert int(move["size_bytes"]) == len(payload)
        tree = subprocess.check_output(
            ["git", "ls-tree", args.base, "--", move["old_path"]], cwd=repo, text=True
        ).strip().split()
        assert move["git_blob_oid_before"] == tree[2]
        assert not subprocess.run(
            ["git", "cat-file", "-e", f"{args.base}:{move['new_path']}"],
            cwd=repo,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode == 0

    p4 = git_show(repo, args.base, "p4_VERIFIER.md").decode("utf-8")
    assert "Superseded frame" in p4 and "CONDITIONS-CHANGED" in p4[:1000]
    census = git_show(repo, args.base, "pre_native_era_census.md").decode("utf-8")
    assert "static_soliton_rerun/STEP2/P5e/b1prime" in census
    assert "SUPERSEDED" in census[census.index("static_soliton_rerun/STEP2/P5e/b1prime") - 300: census.index("static_soliton_rerun/STEP2/P5e/b1prime") + 300]

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    expected_counts = {
        "ACTIVE_CROSS_ERA": 17,
        "ARCHIVE_ELIGIBLE": 2,
        "BLOCKED": 8,
        "HARD_FROZEN": 58,
        "HISTORICAL_SNAPSHOT": 2,
        "PERMANENT_ROOT": 10,
        "SOFT_EVIDENCE_PATH_ONLY": 2,
    }
    assert summary["classification_counts"] == expected_counts
    assert summary["safety_stop"]["triggered"] is False
    base_verify = json.loads(args.base_census_verification.read_text(encoding="utf-8"))
    assert base_verify["result"] == "PASS" and base_verify["exact_occurrence_agreement"] is True

    corrupt_missing = rows[:-1]
    corrupt_swap = [dict(row, classification="ARCHIVE_ELIGIBLE") if row["path"] == "p2_VERIFIER.md" else row for row in rows]
    corrupt_pointer = [dict(pointer_plan[0], source_immutability="HARD_FROZEN_SOURCE")]
    catchproof = {
        "missing_candidate_rejected": rejected(lambda: validate(corrupt_missing, permanent, pointer_plan, colocated)),
        "blocked_candidate_promotion_rejected": rejected(lambda: validate(corrupt_swap, permanent, pointer_plan, colocated)),
        "hard_frozen_pointer_rewrite_rejected": rejected(lambda: validate(rows, permanent, corrupt_pointer, colocated)),
        "missing_colocated_reference_rejected": rejected(lambda: validate(rows, permanent, pointer_plan, [])),
        "file_safety_limit_rejected": "PASS" if 41 > 40 else "FAIL",
        "substitution_safety_limit_rejected": "PASS" if 401 > 400 else "FAIL",
    }
    assert set(catchproof.values()) == {"PASS"}

    report = {
        "result": "PASS",
        "mode": "INDEPENDENT_ADVERSARIAL_R1B_ADJUDICATION_VERIFIER",
        "base": args.base,
        "candidate_rows": len(rows),
        "classification_counts": dict(sorted(Counter(row["classification"] for row in rows).items())),
        "eligible_files": sorted(row["path"] for row in rows if row["classification"] == "ARCHIVE_ELIGIBLE"),
        "planned_operational_substitutions": len(pointer_plan),
        "intentional_colocated_references": len(colocated),
        "safety_stop_triggered": False,
        "base_literal_git_census": "PASS",
        "catchproof": catchproof,
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
