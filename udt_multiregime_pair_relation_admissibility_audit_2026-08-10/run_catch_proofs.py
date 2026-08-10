#!/usr/bin/env python3
"""Exercise fail-closed semantic mutations against the G55 atlas."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def validate(profiles: list[dict[str, str]], matrix: list[dict[str, str]], axes: list[dict[str, str]], families: list[dict[str, str]]) -> None:
    assert len(profiles) == len({row["branch_id"] for row in profiles}) == 24
    assert len(matrix) == len({(row["branch_id"], row["measurement_id"]) for row in matrix}) == 144
    assert len(axes) == len({(row["branch_id"], row["axis_id"]) for row in axes}) == 240
    assert len(families) == 11 and sum(int(row["branch_count"]) for row in families) == 24
    assert all(row["physical_regime_label"] == "OPEN_NOT_ASSIGNED" for row in families)
    assert not any(row["disposition"] in {"BRANCH_OWNED", "GLOBAL_COMPLETION_OWNED"} and row["axis_id"] in {"A01", "A07", "A08", "A10"} for row in axes)
    assert {row["branch_id"] for row in axes if row["axis_id"] == "A09" and row["disposition"] == "GLOBAL_COMPLETION_OWNED"} == {"R04", "R17", "R18", "R23", "R24"}
    cells = {(row["branch_id"], row["measurement_id"]): row for row in matrix}
    assert cells[("R17", "M02")]["disposition"] == "FOUNDED_AFTER_PAIR_SUPPLIED"
    assert cells[("R17", "M05")]["disposition"] == "CONDITIONALLY_AVAILABLE"
    assert cells[("R18", "M02")]["disposition"] == "OPEN_OWNER"
    assert cells[("R23", "M05")]["disposition"] == "INSUFFICIENT_EVIDENCE"
    assert cells[("R24", "M02")]["disposition"] == "TYPE_INAPPLICABLE"
    assert all(cells[("R04", f"M{i:02d}")]["disposition"] == "INSUFFICIENT_EVIDENCE" for i in range(1, 6))
    axis_cells = {(row["branch_id"], row["axis_id"]): row for row in axes}
    assert all(axis_cells[("R04", f"A{i:02d}")]["disposition"] == "INSUFFICIENT_EVIDENCE" for i in range(2, 7))
    assert any(row["measurement_id"] == "M01" and row["object"] == "kappa" for row in matrix)
    assert any(row["measurement_id"] == "M03" and row["object"] == "beta" for row in matrix)
    assert any(row["measurement_id"] == "M04" and row["object"] == "U_gamma" for row in matrix)
    assert all("S11::" in row["evidence"] and "S15::" in row["evidence"] for row in profiles)


def mutate(rows: list[dict[str, str]], predicate, field: str, value: str) -> list[dict[str, str]]:
    result = deepcopy(rows)
    target = next(row for row in result if predicate(row))
    target[field] = value
    return result


def main() -> int:
    profiles = table("BRANCH_ADMISSIBILITY_PROFILES.tsv")
    matrix = table("BRANCH_MEASUREMENT_MATRIX.tsv")
    axes = table("BRANCH_AXIS_MATRIX.tsv")
    families = table("GEOMETRIC_PATTERN_FAMILIES.tsv")
    validate(profiles, matrix, axes, families)

    cases = []
    cases.append((profiles[:-1], matrix, axes, families))
    cases.append((profiles + [deepcopy(profiles[0])], matrix, axes, families))
    cases.append((profiles, matrix[:-1], axes, families))
    cases.append((profiles, matrix + [deepcopy(matrix[0])], axes, families))
    cases.append((profiles, matrix, axes[:-1], families))
    cases.append((profiles, matrix, axes + [deepcopy(axes[0])], families))
    cases.append((profiles, matrix, axes, mutate(families, lambda r: r["pattern_family"] == "F07_FULL_RECIPROCAL_PATH_CONDITIONAL", "physical_regime_label", "MICRO")))
    cases.append((profiles, matrix, mutate(axes, lambda r: r["branch_id"] == "R17" and r["axis_id"] == "A01", "disposition", "BRANCH_OWNED"), families))
    cases.append((profiles, matrix, mutate(axes, lambda r: r["branch_id"] == "R17" and r["axis_id"] == "A07", "disposition", "BRANCH_OWNED"), families))
    cases.append((profiles, matrix, mutate(axes, lambda r: r["branch_id"] == "R18" and r["axis_id"] == "A08", "disposition", "GLOBAL_COMPLETION_OWNED"), families))
    cases.append((profiles, matrix, mutate(axes, lambda r: r["branch_id"] == "R23" and r["axis_id"] == "A10", "disposition", "BRANCH_OWNED"), families))
    cases.append((profiles, mutate(matrix, lambda r: r["branch_id"] == "R17" and r["measurement_id"] == "M02", "disposition", "BRANCH_OWNED"), axes, families))
    cases.append((profiles, mutate(matrix, lambda r: r["branch_id"] == "R17" and r["measurement_id"] == "M05", "disposition", "BRANCH_OWNED"), axes, families))
    cases.append((profiles, mutate(matrix, lambda r: r["branch_id"] == "R18" and r["measurement_id"] == "M02", "disposition", "FOUNDED_AFTER_PAIR_SUPPLIED"), axes, families))
    cases.append((profiles, mutate(matrix, lambda r: r["branch_id"] == "R23" and r["measurement_id"] == "M05", "disposition", "CONDITIONALLY_AVAILABLE"), axes, families))
    cases.append((profiles, mutate(matrix, lambda r: r["branch_id"] == "R24" and r["measurement_id"] == "M02", "disposition", "OPEN_OWNER"), axes, families))
    cases.append((profiles, [row for row in matrix if row["measurement_id"] != "M01"], axes, families))
    cases.append((profiles, [row for row in matrix if row["measurement_id"] != "M03"], axes, families))
    cases.append((profiles, [row for row in matrix if row["measurement_id"] != "M04"], axes, families))
    cases.append((mutate(profiles, lambda r: r["branch_id"] == "R17", "evidence", "filename_prefix"), matrix, axes, families))
    cases.append((profiles, mutate(matrix, lambda r: r["branch_id"] == "R04" and r["measurement_id"] == "M02", "disposition", "CONDITIONALLY_AVAILABLE"), axes, families))
    cases.append((profiles, matrix, mutate(axes, lambda r: r["branch_id"] == "R04" and r["axis_id"] == "A04", "disposition", "CONDITIONALLY_AVAILABLE"), families))

    rejected = 0
    for candidate in cases:
        try:
            validate(*candidate)
        except AssertionError:
            rejected += 1
    result = {
        "status": "PASS" if rejected == len(cases) else "FAIL",
        "rejected": rejected,
        "total": len(cases),
    }
    (HERE / "CATCH_PROOF_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if rejected == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
