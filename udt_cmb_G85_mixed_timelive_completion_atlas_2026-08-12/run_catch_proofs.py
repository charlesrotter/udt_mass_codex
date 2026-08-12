#!/usr/bin/env python3
"""Hostile in-memory mutations for the preregistered G85 gates."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(atlas: list[dict[str, str]], result: dict[str, object], manifest: list[dict[str, str]]) -> None:
    assert len(atlas) == 980
    pairs = [(row["profile_id"], row["archetype_id"]) for row in atlas]
    assert len(set(pairs)) == 980
    assert len(set(row["profile_id"] for row in atlas)) == 196
    for row in atlas:
        archetype = row["archetype_id"]
        if archetype in {"A01_PRESERVE_STATIONARY_GERM", "A02_MIXING_ONLY_TIMELIVE"}:
            assert row["classification"] == "POINTWISE_DEGENERATE"
        elif archetype == "A03_RADIAL_SHIFT_TIMELIVE":
            assert row["classification"] == "CONDITIONAL_ON_NONVANISHING_SHIFT"
            assert "!=0" in row["b_H_condition"]
        elif archetype == "A04_LAPSE_LIFT_TIMELIVE":
            assert row["classification"] == "REGULAR_LORENTZ_NONNULL_SEAM"
            assert "<0" in row["u_H_condition"]
        elif archetype == "A05_MIXING_TAPER_BEFORE_SEAM":
            assert row["classification"] == "REGULAR_LORENTZ_UNIFORM_NULL_SEAM"
            assert "A*h_tilde_Kruskal_smooth" in row["h_H_condition"]
        else:
            raise AssertionError(archetype)
        assert row["frozen_cell_preserved"] == "true"
        assert row["physical_status"] == "CONTROL_CLASSIFICATION_NOT_SELECTED_PHYSICS"
    for key in (
        "physical_profile_selected", "physical_topology_selected",
        "physical_Xmax_selected", "native_dynamics_selected",
    ):
        assert result[key] is False
    assert len(manifest) == len({row["path"] for row in manifest}) == 11
    for row in manifest:
        assert digest(ROOT / row["path"]) == row["sha256"]


def expect_failure(name: str, callback) -> dict[str, str]:
    try:
        callback()
    except (AssertionError, KeyError, ValueError):
        return {"catch": name, "status": "PASS", "meaning": "hostile mutation rejected"}
    raise AssertionError(f"catch did not fire: {name}")


def main() -> None:
    atlas = rows(HERE / "PROFILE_ARCHETYPE_ATLAS.tsv")
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    validate(atlas, result, manifest)
    catches: list[dict[str, str]] = []

    catches.append(expect_failure("missing_move_equivalent_profile_row", lambda: validate(atlas[:-1], result, manifest)))

    duplicate = copy.deepcopy(atlas)
    duplicate[-1] = copy.deepcopy(duplicate[0])
    catches.append(expect_failure("duplicate_profile_archetype_pair", lambda: validate(duplicate, result, manifest)))

    derivative_repair = copy.deepcopy(atlas)
    target = next(row for row in derivative_repair if row["archetype_id"] == "A02_MIXING_ONLY_TIMELIVE")
    target["classification"] = "REGULAR_LORENTZ_NONNULL_SEAM"
    catches.append(expect_failure("time_derivative_falsely_repairs_rank", lambda: validate(derivative_repair, result, manifest)))

    shift_zero = copy.deepcopy(atlas)
    target = next(row for row in shift_zero if row["archetype_id"] == "A03_RADIAL_SHIFT_TIMELIVE")
    target["b_H_condition"] = "b_H(t)=0_allowed"
    catches.append(expect_failure("shift_zero_crossing_admitted", lambda: validate(shift_zero, result, manifest)))

    false_null = copy.deepcopy(atlas)
    target = next(row for row in false_null if row["archetype_id"] == "A03_RADIAL_SHIFT_TIMELIVE")
    target["classification"] = "REGULAR_LORENTZ_UNIFORM_NULL_SEAM"
    catches.append(expect_failure("nonzero_mix_falsely_uniform_null", lambda: validate(false_null, result, manifest)))

    weak_taper = copy.deepcopy(atlas)
    target = next(row for row in weak_taper if row["archetype_id"] == "A05_MIXING_TAPER_BEFORE_SEAM")
    target["h_H_condition"] = "h=A*h_tilde_of_singular_tau"
    catches.append(expect_failure("mere_zero_value_substituted_for_order_A_taper", lambda: validate(weak_taper, result, manifest)))

    cell_mutation = copy.deepcopy(atlas)
    cell_mutation[0]["frozen_cell_preserved"] = "false"
    catches.append(expect_failure("frozen_cell_modified", lambda: validate(cell_mutation, result, manifest)))

    promotion = copy.deepcopy(result)
    promotion["physical_Xmax_selected"] = True
    catches.append(expect_failure("physical_Xmax_promoted", lambda: validate(atlas, promotion, manifest)))

    status_promotion = copy.deepcopy(atlas)
    status_promotion[0]["physical_status"] = "SELECTED_PHYSICS"
    catches.append(expect_failure("control_promoted_to_physics", lambda: validate(status_promotion, result, manifest)))

    manifest_mutation = copy.deepcopy(manifest)
    manifest_mutation[0]["sha256"] = "0" * 64
    catches.append(expect_failure("frozen_source_hash_mutated", lambda: validate(atlas, result, manifest_mutation)))

    output = {
        "schema": "udt-cmb-g85-catch-proofs-v1",
        "status": "PASS",
        "catch_count": len(catches),
        "all_hostile_mutations_rejected": True,
        "catches": catches,
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
