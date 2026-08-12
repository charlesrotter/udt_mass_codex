#!/usr/bin/env python3
"""Exercise fail-closed G76 artifact-verifier catches with in-memory mutations."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def expected_class(row: dict[str, str]) -> str:
    resolved = (
        float(row["time_refinement_endpoint_max_chord"]) <= 5.0e-5
        and int(row["time_refinement_mask_mismatch"]) == 0
        and float(row["mesh_degree_drift_level3_to4"]) <= 5.0e-4
        and float(row["max_abs_hamiltonian"]) <= 1.0e-6
        and int(row["reflection_mask_mismatch"]) == 0
        and float(row["reflection_max_chord"]) <= 2.0e-5
    )
    if not resolved:
        return "NUMERICALLY_UNRESOLVED"
    if int(row["finest_missing_vertices"]) or int(row["finest_nonfinite_count"]):
        return "SAMPLED_MISSING_OR_MULTIBRANCH_CANDIDATE"
    if int(row["finest_negative_faces"]) or int(row["finest_negative_intrinsic_face_maps"]):
        return "SAMPLED_ORIENTATION_REVERSING_OR_FOLD_CANDIDATE"
    return "SAMPLED_COMPLETE_ORIENTATION_PRESERVING"


def valid(atlas: list[dict[str, str]], mesh: list[dict[str, str]]) -> bool:
    ids = [row["profile_id"] for row in atlas]
    mesh_keys = [(row["profile_id"], row["level"], row["steps"]) for row in mesh]
    return (
        len(ids) == len(set(ids)) == 591
        and len(mesh_keys) == len(set(mesh_keys)) == 2364
        and all(row["sample_class"] == expected_class(row) for row in atlas)
        and all(row["physical_status"] == "CHOSE_CONTROL_NOT_SELECTED" for row in atlas)
    )


def main() -> None:
    atlas, mesh = rows("WHOLE_SKY_RELATION_ATLAS.tsv"), rows("MESH_CONVERGENCE_ATLAS.tsv")
    assert valid(atlas, mesh)
    catches: dict[str, bool] = {}

    mutated = copy.deepcopy(atlas[:-1])
    catches["missing_profile_rejected"] = not valid(mutated, mesh)

    mutated = copy.deepcopy(atlas)
    mutated[-1] = copy.deepcopy(mutated[0])
    catches["duplicate_profile_rejected"] = not valid(mutated, mesh)

    mutated = copy.deepcopy(atlas)
    target = next(row for row in mutated if row["profile_id"] == "G75_AM_S03_E100")
    target["sample_class"] = "SAMPLED_COMPLETE_ORIENTATION_PRESERVING"
    catches["unresolved_promotion_rejected"] = not valid(mutated, mesh)

    mutated = copy.deepcopy(atlas)
    mutated[0]["time_refinement_endpoint_max_chord"] = "1e-2"
    catches["stale_class_after_error_mutation_rejected"] = not valid(mutated, mesh)

    mutated_mesh = copy.deepcopy(mesh[:-1])
    catches["missing_mesh_trial_rejected"] = not valid(atlas, mutated_mesh)

    mutated = copy.deepcopy(atlas)
    mutated[0]["physical_status"] = "DERIVED_PHYSICAL_PROFILE"
    catches["physical_promotion_rejected"] = not valid(mutated, mesh)

    result = {
        "schema": "udt-cmb-g76-catch-proofs-v1",
        "status": "PASS" if all(catches.values()) else "FAIL",
        "catch_count": len(catches),
        "catches": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
