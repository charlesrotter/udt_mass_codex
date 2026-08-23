#!/usr/bin/env python3
"""Aggregate verification for G228, with an in-memory no-write replay."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess

from derive_neighboring_curvature_first_variation import derive as derive_production
from run_hostile_catches import derive_catches
from verify_full_index_anchor import derive as derive_full_index
from verify_neighboring_curvature_independent import derive as derive_independent


ROOT = Path(__file__).resolve().parent


def normalized_production_census(subsets):
    keys = ("key", "size", "target_dimension", "image_rank", "codimension", "image_sha256")
    return [{key: row[key] for key in keys} for row in subsets]


def verify(require_saved: bool = True) -> dict[str, object]:
    production, syzygies, subsets = derive_production()
    independent = derive_independent()
    full_index = derive_full_index()
    hostile = derive_catches()

    census_match = normalized_production_census(subsets) == independent["subset_census"]
    scalar_match = all(
        production[key] == independent[key]
        for key in (
            "differential_bianchi_generated_rows",
            "differential_bianchi_independent_rank",
            "compatible_module_dimension",
            "bianchi_matrix_sha256",
            "kernel_matrix_sha256",
            "first_restricted_subset_size",
        )
    )
    screen_match = all(bool(value) for value in independent["screen_and_phase"].values())

    full_index_census = [
        {
            "key": row["key"],
            "size": row["size"],
            "target_dimension": row["intrinsic_target_dimension"],
            "image_rank": row["image_rank"],
            "codimension": row["intrinsic_codimension"],
        }
        for row in full_index["subset_census"]
    ]
    production_census_without_hash = [
        {key: row[key] for key in ("key", "size", "target_dimension", "image_rank", "codimension")}
        for row in subsets
    ]
    full_index_match = (
        full_index["raw_full_slot_variables"] == 84
        and full_index["algebraic_bianchi_rank"] == 4
        and full_index["combined_constraint_rank"] == 24
        and full_index["differential_incremental_rank"] == 20
        and full_index["compatible_module_dimension"] == 60
        and full_index_census == production_census_without_hash
    )

    saved_json_match = True
    saved_census_match = True
    saved_syzygy_match = True
    saved_source_hashes_match = True
    saved_checked = False
    if require_saved:
        saved_checked = True
        saved_production = json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
        saved_independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
        saved_hostile = json.loads((ROOT / "HOSTILE_CATCH_RESULT.json").read_text())
        saved_full_index = json.loads((ROOT / "FULL_INDEX_ANCHOR.json").read_text())
        saved_json_match = (
            saved_production == production
            and saved_independent == independent
            and saved_hostile == hostile
            and saved_full_index == full_index
        )

        census_columns = (
            "key", "size", "target_dimension", "image_rank", "codimension", "syzygy_count",
            "syzygies_pass_seeded_control", "within_image_perturbation_accepted",
            "hostile_one_entry_index", "hostile_one_entry_detected", "hostile_syzygy_residual",
            "image_sha256",
        )
        with (ROOT / "SUBSET_CENSUS.tsv").open(newline="") as handle:
            saved_census = list(csv.DictReader(handle, delimiter="\t"))
        expected_census = [
            {column: str(row[column]) for column in census_columns}
            for row in subsets
        ]
        saved_census_match = saved_census == expected_census
        saved_syzygy_match = json.loads((ROOT / "SYZYGY_BASIS.json").read_text()) == syzygies

        with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
            source_rows = list(csv.DictReader(handle, delimiter="\t"))
        saved_source_hashes_match = True
        for row in source_rows:
            frozen = subprocess.run(
                ["git", "show", f"b54f4c51:{row['path']}"],
                cwd=ROOT.parent,
                check=True,
                capture_output=True,
            ).stdout
            if hashlib.sha256(frozen).hexdigest() != row["sha256"]:
                saved_source_hashes_match = False
                break

    value_generation_guard = (
        "cannot generate curvature values" in (ROOT / "PREREGISTRATION.md").read_text()
        and "Physical history and population: `OPEN`" in (ROOT / "MAP.md").read_text()
    )

    checks = {
        "production_independent_scalar_match": scalar_match,
        "production_independent_all_15_subsets_match": census_match,
        "independent_screen_phase_checks_pass": screen_match,
        "production_all_subset_controls_pass": bool(production["all_subset_controls_pass"]),
        "production_screen_phase_checks_pass": bool(production["all_screen_and_phase_checks_pass"]),
        "orthogonal_84_slot_full_index_anchor": full_index_match,
        "hostile_catches_11_of_11": hostile["passed"] == hostile["total"] == 11,
        "selected_preregistered_alternative_B": production["landing"] == "B_ONE_DIRECTION_SURJECTIVE__FIRST_RESTRICTION_AT_THREE_DIRECTIONS",
        "value_generation_nonpromotion_guard": value_generation_guard,
        "saved_json_artifacts_match_replay": saved_json_match,
        "saved_subset_census_matches_replay": saved_census_match,
        "saved_syzygy_basis_matches_replay": saved_syzygy_match,
        "source_manifest_hashes_match": saved_source_hashes_match,
    }
    return {
        "checks": checks,
        "passed": sum(bool(value) for value in checks.values()),
        "total": len(checks),
        "all_pass": all(bool(value) for value in checks.values()),
        "saved_artifacts_checked": saved_checked,
        "landing": production["landing"],
        "module_dimension": production["compatible_module_dimension"],
        "first_restricted_subset_size": production["first_restricted_subset_size"],
        "full_star_codimension": next(row["codimension"] for row in subsets if row["size"] == 4),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--skip-saved", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "VERIFICATION_RESULT.json")
    args = parser.parse_args()
    result = verify(require_saved=not args.skip_saved)
    if not args.no_write:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    elif args.output.exists():
        saved_result = json.loads(args.output.read_text())
        if saved_result != result:
            raise SystemExit("saved VERIFICATION_RESULT.json does not match no-write replay")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
