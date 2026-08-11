#!/usr/bin/env python3
"""Render machine-readable G68 census tables from the raw JSON result."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent


def write_tsv(name: str, fields: list[str], rows: list[dict]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, delimiter="\t", lineterminator="\n", fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    payload = json.loads((HERE / "FINITE_PATH_RESULT.json").read_text(encoding="utf-8"))
    f01 = {row["lapse_a"]: row for row in payload["profiles"] if row["family"] == "F01"}
    main_rows = []
    for row in payload["profiles"]:
        D = np.asarray(row["endpoint_D"], dtype=float)
        base = f01[row["lapse_a"]]
        area_change = 0.0 if row["family"] == "F01" else row["det_D"] / base["det_D"] - 1.0
        mean_diag = 0.5 * (D[0, 0] + D[1, 1])
        anisotropy = 0.0 if mean_diag == 0.0 else (D[0, 0] - D[1, 1]) / mean_diag
        main_rows.append(
            {
                "profile_id": row["profile_id"],
                "family": row["family"],
                "lapse_a": row["lapse_a"],
                "mix_shape": row["mix_shape"],
                "mix_epsilon": row["mix_epsilon"],
                "status": row["status"],
                "affine_final": format(row["affine_final"], ".17g"),
                "endpoint_psi": format(row["endpoint_coordinates"][3], ".17g"),
                "D_theta_theta": format(D[0, 0], ".17g"),
                "D_theta_psi": format(D[0, 1], ".17g"),
                "D_psi_theta": format(D[1, 0], ".17g"),
                "D_psi_psi": format(D[1, 1], ".17g"),
                "det_D": format(row["det_D"], ".17g"),
                "area_change_vs_matched_F01": format(area_change, ".17g"),
                "diagonal_anisotropy": format(anisotropy, ".17g"),
                "polar_rotation": format(row["polar_rotation"], ".17g"),
                "first_caustic_affine": "NONE" if row["first_caustic_affine"] is None else format(row["first_caustic_affine"], ".17g"),
                "turning_count": len(row["turning_events"]),
                "max_null": format(row["residuals"]["null"], ".17g"),
                "max_gram": format(row["residuals"]["screen_gram"], ".17g"),
                "max_wronskian": format(row["residuals"]["wronskian"], ".17g"),
                "refined_D_relative": format(row["convergence"]["production_refined_D_relative"], ".17g"),
                "second_method_D_relative": format(row["convergence"]["refined_second_D_relative"], ".17g"),
            }
        )
    write_tsv("FINITE_PATH_ATLAS.tsv", list(main_rows[0]), main_rows)

    reflection_rows = []
    for profile_id, row in sorted(payload["reflection_checks"].items()):
        reflection_rows.append({"profile_id": profile_id, **row})
    write_tsv("REFLECTION_ATLAS.tsv", list(reflection_rows[0]), reflection_rows)

    epsilon_rows = []
    for row in payload["epsilon_limit_checks"]:
        epsilon_rows.append(
            {
                "lapse_a": row["lapse_a"],
                "mix_shape": row["mix_shape"],
                "epsilon_large": row["controls"][0]["epsilon"],
                "error_large": format(row["controls"][0]["D_error_from_F01"], ".17g"),
                "epsilon_small": row["controls"][1]["epsilon"],
                "error_small": format(row["controls"][1]["D_error_from_F01"], ".17g"),
                "large_to_small_error_ratio": format(row["large_to_small_error_ratio"], ".17g"),
                "nonincrease_or_below_floor": row["nonincrease_or_below_floor"],
            }
        )
    write_tsv("EPSILON_LIMIT_ATLAS.tsv", list(epsilon_rows[0]), epsilon_rows)
    print(f"finite_rows={len(main_rows)} reflection_rows={len(reflection_rows)} epsilon_rows={len(epsilon_rows)}")


if __name__ == "__main__":
    main()
