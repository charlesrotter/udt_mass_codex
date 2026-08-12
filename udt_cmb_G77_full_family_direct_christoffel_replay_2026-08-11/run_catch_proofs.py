#!/usr/bin/env python3
"""Exercise G77 fail-closed semantic and artifact catches in memory."""

from __future__ import annotations

import copy
import csv
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def expected_class(row: dict[str, str]) -> str:
    chord = float(row["direct_G76_max_chord"])
    unresolved = (
        int(row["crossing_mask_mismatch"]) != 0
        or chord > 5.0e-5
        or float(row["maximum_null_backward_error"]) > 2.0e-7
        or float(row["G76_degree_difference"]) > 5.0e-4
    )
    if unresolved:
        return "CROSS_METHOD_NUMERICALLY_UNRESOLVED"
    return "STRONG_DIRECT_AGREEMENT" if chord <= 2.0e-5 else "REGISTERED_DIRECT_AGREEMENT"


def valid(atlas: list[dict[str, str]], completed: np.ndarray, refinement: list[dict[str, str]]) -> bool:
    ids = [row["profile_id"] for row in atlas]
    refinement_ids = [row["profile_id"] for row in refinement]
    return (
        len(ids) == len(set(ids)) == 591
        and completed.shape == (591,)
        and bool(np.all(completed))
        and all(row["direct_class"] == expected_class(row) for row in atlas)
        and len(refinement_ids) == len(set(refinement_ids)) == 4
        and all(row["G76_sample_class"] == "NUMERICALLY_UNRESOLVED" for row in refinement)
        and all(row["G77_refinement_status"] == "DIRECT_TIME_REFINEMENT_RESOLVED" for row in refinement)
        and all(float(row["direct_2048_4096_max_chord"]) <= 5.0e-5 for row in refinement)
    )


def main() -> None:
    atlas = rows("DIRECT_CHRISTOFFEL_ATLAS.tsv")
    refinement = rows("UNRESOLVED_REFINEMENT_ATLAS.tsv")
    completed = np.load(HERE / "DIRECT_COMPLETED.npy")
    assert valid(atlas, completed, refinement)
    catches = {}

    catches["missing_profile_rejected"] = not valid(atlas[:-1], completed, refinement)

    mutated = copy.deepcopy(atlas)
    mutated[-1] = copy.deepcopy(mutated[0])
    catches["duplicate_profile_rejected"] = not valid(mutated, completed, refinement)

    mutated = copy.deepcopy(atlas)
    target = next(row for row in mutated if row["profile_id"] == "G75_AM_S03_E100")
    target["direct_class"] = "STRONG_DIRECT_AGREEMENT"
    catches["strict_tier_promotion_rejected"] = not valid(mutated, completed, refinement)

    mutated = copy.deepcopy(atlas)
    mutated[0]["direct_G76_max_chord"] = "1e-2"
    catches["stale_class_after_endpoint_mutation_rejected"] = not valid(mutated, completed, refinement)

    mutated_completed = completed.copy()
    mutated_completed[42] = False
    catches["incomplete_checkpoint_rejected"] = not valid(atlas, mutated_completed, refinement)

    catches["missing_refinement_row_rejected"] = not valid(atlas, completed, refinement[:-1])

    mutated_refinement = copy.deepcopy(refinement)
    mutated_refinement[0]["G76_sample_class"] = "SAMPLED_COMPLETE_ORIENTATION_PRESERVING"
    catches["G76_history_rewrite_rejected"] = not valid(atlas, completed, mutated_refinement)

    mutated_refinement = copy.deepcopy(refinement)
    mutated_refinement[0]["direct_2048_4096_max_chord"] = "1e-3"
    catches["refinement_threshold_violation_rejected"] = not valid(atlas, completed, mutated_refinement)

    result = {
        "schema": "udt-cmb-g77-catch-proofs-v1",
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
