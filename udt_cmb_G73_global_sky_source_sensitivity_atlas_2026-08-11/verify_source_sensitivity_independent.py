#!/usr/bin/env python3
"""Independent numerical/exact replay of the G73 source-sensitivity result."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G68 = ROOT / "udt_cmb_G68_F01_F02_finite_path_jacobi_controls_2026-08-11/FINITE_PATH_ATLAS.tsv"
LANDING = (
    "REGULAR_SKY_RESPONSE_SOURCE_INVERTIBLE__"
    "ROBUST_KALEIDOSCOPE_REQUIRES_GLOBAL_BRANCHING_SINGULARITY_OR_SOURCE_RESTRICTION"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def rank_fraction(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix]
    rows, cols = len(work), len(work[0])
    rank = 0
    for col in range(cols):
        pivot = next((index for index in range(rank, rows) if work[index][col] != 0), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][col]
        work[rank] = [value / scale for value in work[rank]]
        for index in range(rows):
            if index == rank:
                continue
            factor = work[index][col]
            if factor:
                work[index] = [left - factor * right for left, right in zip(work[index], work[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def angle_fraction_grid(chi: float, cone_degrees: float, count: int = 400_000) -> float:
    alpha = (np.arange(count, dtype=float) + 0.5) * (math.pi / count)
    output = np.arctan2(np.exp(-chi) * np.sin(alpha), np.exp(chi) * np.cos(alpha))
    distance = np.minimum(np.abs(output), np.abs(math.pi - np.abs(output)))
    return float(np.mean(distance <= math.radians(cone_degrees)))


def main() -> None:
    manifest = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 9
    assert all(digest(ROOT / row["path"]) == row["sha256"] for row in manifest)

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    derived_atlas = {row["profile_id"]: row for row in table(HERE / "G68_SOURCE_SENSITIVITY_ATLAS.tsv")}
    original = table(G68)
    errors = []
    max_condition = 0.0
    max_chi = 0.0
    for row in original:
        D = np.array(
            [[float(row["D_theta_theta"]), float(row["D_theta_psi"])],
             [float(row["D_psi_theta"]), float(row["D_psi_psi"])]], dtype=float
        )
        singular = np.linalg.svd(D, compute_uv=False)
        ratio = float(singular[0] / singular[1])
        chi = 0.5 * math.log(ratio)
        saved = derived_atlas[row["profile_id"]]
        errors.append(abs(ratio - float(saved["singular_value_ratio_exp_2chi"])))
        errors.append(abs(chi - float(saved["shear_chi"])))
        max_condition = max(max_condition, ratio)
        max_chi = max(max_chi, chi)

    analytic = {
        angle: (2.0 / math.pi) * math.atan(math.exp(2.0 * max_chi) * math.tan(math.radians(angle)))
        for angle in (5.0, 15.0, 30.0)
    }
    grid = {angle: angle_fraction_grid(max_chi, angle) for angle in analytic}
    max_grid_error = max(abs(analytic[angle] - grid[angle]) for angle in analytic)

    # Independent exact ranks using Fraction Gaussian elimination.
    regular = [[Fraction(0) for _ in range(6)] for _ in range(6)]
    blocks = (((2, 0), (0, 1)), ((1, 1), (0, 1)), ((3, 0), (0, 2)))
    order = (2, 0, 1)
    for target, source in enumerate(order):
        for i in range(2):
            for j in range(2):
                regular[2 * target + i][2 * source + j] = Fraction(blocks[source][i][j])
    duplicate = [
        [Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)],
    ]
    rank_loss = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(0)]]

    checks = {
        "landing": production["landing"] == LANDING,
        "source_manifest": len(manifest) == 9,
        "g68_rows": len(original) == len(derived_atlas) == 21,
        "g68_direct_svd": max(errors) < 2e-14,
        "g68_max_condition": abs(max_condition - 1.0046584288394136) < 2e-14,
        "g68_max_chi": abs(max_chi - 0.0023238059699749714) < 2e-14,
        "alignment_grid": max_grid_error < 8e-6,
        "regular_global_rank": rank_fraction(regular) == 6,
        "duplication_rank_and_constraints": rank_fraction(duplicate) == 2 and duplicate[0] == duplicate[2] and duplicate[1] == duplicate[3],
        "rank_loss": rank_fraction(rank_loss) == 1,
        "physical_owner_open": production["status"]["physical_cmb_source_and_observable"] == "OPEN_NO_OWNER",
    }
    assert all(checks.values()), [name for name, value in checks.items() if not value]
    payload = {
        "schema": "udt-cmb-g73-source-sensitivity-independent-v1",
        "status": "PASS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "max_direct_atlas_error": max(errors),
        "max_alignment_grid_error": max_grid_error,
        "alignment_analytic": {str(key): value for key, value in analytic.items()},
        "alignment_grid": {str(key): value for key, value in grid.items()},
        "protected_draft_read": False,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
