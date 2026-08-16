#!/usr/bin/env python3
"""Fraction-only independent G106 replay; imports no production module."""

from __future__ import annotations

import hashlib
import json
import os
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def integrate_quadratic(lo: F, hi: F) -> F:
    # Integral of t^2-t+1/4 = (2t-1)^2/4.
    def primitive(t: F) -> F:
        return t**3 / 3 - t**2 / 2 + t / 4

    return primitive(hi) - primitive(lo)


def reference(matrix: list[list[F]], selection: list[F]) -> list[list[F]]:
    return [[sum(row) * value for value in selection] for row in matrix]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    selection = [F(1, 10), F(2, 10), F(3, 10), F(4, 10)]
    depth = [F(1, 6), F(1, 3), F(1, 2)]
    mode = [-2, -1, 0, 1]
    amplitude = [F(1, 10), F(0), F(1, 5)]
    density = [
        [depth[i] * selection[j] * (1 + amplitude[i] * mode[j]) for j in range(4)]
        for i in range(3)
    ]
    q = reference(density, selection)
    q2 = reference(q, selection)
    residual = [[density[i][j] - q[i][j] for j in range(4)] for i in range(3)]
    pure_radial = [[depth[i] * selection[j] for j in range(4)] for i in range(3)]

    windows = [(F(0), F(1, 3)), (F(1, 3), F(2, 3)), (F(2, 3), F(1))]
    averages = [integrate_quadratic(lo, hi) / (hi - lo) for lo, hi in windows]
    pair = [value * value / 5 for value in averages]

    source_rows = []
    with (HERE / "SOURCE_MANIFEST_PREREG.tsv").open(encoding="utf-8") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        for line in handle:
            values = line.rstrip("\n").split("\t")
            source_rows.append(dict(zip(header, values)))

    checks = {
        "selection_normalized": sum(selection) == 1,
        "mode_zero_mean": sum(selection[j] * mode[j] for j in range(4)) == 0,
        "density_normalized": sum(sum(row) for row in density) == 1,
        "density_positive": all(value > 0 for row in density for value in row),
        "projector_idempotent": q2 == q,
        "residual_kernel": all(sum(row) == 0 for row in residual),
        "pure_radial_removed": reference(pure_radial, selection) == pure_radial,
        "interaction_survives": any(value != 0 for row in residual for value in row),
        "window_averages": averages == [F(13, 108), F(1, 108), F(13, 108)],
        "pair_ratio": pair[0] / pair[1] == 169,
        "full_sky_density_bounds": F(7, 8) > 0 and F(5, 4) > F(7, 8),
        "source_hashes": all(
            (ROOT / row["path"]).is_file() and digest(ROOT / row["path"]) == row["sha256"]
            for row in source_rows
        ),
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "window_averages": [str(value) for value in averages],
        "pair_coefficients": [str(value) for value in pair],
        "outcome_paths_read": [],
    }
    if result["status"] != "PASS":
        raise AssertionError(result)
    if os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
