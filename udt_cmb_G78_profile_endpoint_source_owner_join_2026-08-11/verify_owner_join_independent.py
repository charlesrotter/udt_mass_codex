#!/usr/bin/env python3
"""Independent reconstruction of the load-bearing G78 claims."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "9a78af889321d84914ae5eb2c066da56bc957719"


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    manifest = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == len({row["path"] for row in manifest}) == 20
    for row in manifest:
        data = subprocess.check_output(["git", "show", f"{BASE}:{row['path']}"], cwd=ROOT)
        assert hashlib.sha256(data).hexdigest() == row["sha256"]

    profiles = table(ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv")
    replay = table(ROOT / "udt_cmb_G77_full_family_direct_christoffel_replay_2026-08-11/DIRECT_CHRISTOFFEL_ATLAS.tsv")
    profile_ids = {row["profile_id"] for row in profiles}
    replay_ids = {row["profile_id"] for row in replay}
    assert len(profiles) == len(profile_ids) == len(replay) == len(replay_ids) == 591
    assert profile_ids == replay_ids
    assert sum(row["shape_id"] == "ZERO" for row in profiles) == 3
    assert sum(row["direct_class"] == "STRONG_DIRECT_AGREEMENT" for row in replay) == 590
    assert sum(row["direct_class"] == "REGISTERED_DIRECT_AGREEMENT" for row in replay) == 1
    assert all(int(row["crossed_vertices"]) == 2562 for row in replay)
    assert all(int(row["missing_vertices"]) == 0 for row in replay)
    assert all(int(row["negative_faces"]) == 0 for row in replay)
    assert all(int(row["negative_projected_face_maps"]) == 0 for row in replay)
    assert all(int(row["near_area_1e2"]) == 0 for row in replay)
    assert max(abs(float(row["degree"]) - 1.0) for row in replay) < 5e-15

    R, c_e, A, h, st = sp.symbols("R c_E A h sin_theta", positive=True)
    dt = R / c_e
    normalized = sp.Matrix([
        -A * c_e**2 * dt**2 / R**2,
        (R**2 / A) / R**2,
        R**2 / R**2,
        (2 * R * c_e * h * st**2 * dt) / R**2,
    ])
    expected = sp.Matrix([-A, 1 / A, 1, 2 * h * st**2])
    assert all(sp.simplify(value) == 0 for value in normalized - expected)

    rng = np.random.default_rng(7801)
    max_relative = 0.0
    min_source_eigenvalue = float("inf")
    for _ in range(256):
        D = rng.normal(size=(2, 2))
        while abs(np.linalg.det(D)) < 0.15:
            D = rng.normal(size=(2, 2))
        B = rng.normal(size=(2, 2))
        C_obs = B @ B.T + 0.1 * np.eye(2)
        D_inv = np.linalg.inv(D)
        C_src = D_inv @ C_obs @ D_inv.T
        reconstructed = D @ C_src @ D.T
        max_relative = max(max_relative, float(np.linalg.norm(reconstructed - C_obs) / np.linalg.norm(C_obs)))
        min_source_eigenvalue = min(min_source_eigenvalue, float(np.linalg.eigvalsh(C_src).min()))
    assert max_relative < 2e-13 and min_source_eigenvalue > 0

    routes = table(HERE / "OWNER_ROUTE_LEDGER.tsv")
    assert [row["route"] for row in routes] == [
        "P_REGULARITY", "P_GLOBAL_RELATION", "E_SCALE", "E_SNE", "E_XMAX",
        "S_GEOMETRY", "S_MULTICHANNEL",
    ]
    expected_status = {
        "P_REGULARITY": "OPEN_NO_OWNER",
        "P_GLOBAL_RELATION": "OPEN_NO_OWNER",
        "E_SCALE": "OPEN_NO_OWNER",
        "E_SNE": "COMPATIBILITY_ANCHOR_ONLY",
        "E_XMAX": "NECESSARY_REQUIREMENT_ONLY",
        "S_GEOMETRY": "OPEN_NO_OWNER",
        "S_MULTICHANNEL": "CONDITIONAL_IDENTIFIABILITY_ONLY",
    }
    assert {row["route"]: row["status"] for row in routes} == expected_status
    assert all(row["evidence"] and row["blocker"] for row in routes)

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert result["landing"] == "NO_PHYSICAL_PROFILE_ENDPOINT_SCALE_OR_SOURCE_OWNER_IN_FROZEN_G78_UNIVERSE"
    assert result["owned_native_routes"] == 0
    assert result["scale_factorization"]["non_implication"] == "does_not_make_UDT_scale_free_or_select_R_endpoint_or_Xmax"

    output = {
        "schema": "udt-cmb-g78-independent-verification-v1",
        "status": "PASS",
        "source_rows": len(manifest),
        "profile_rows": len(profiles),
        "replay_rows": len(replay),
        "scale_factorization_reproduced": True,
        "source_congruence_controls": 256,
        "source_congruence_maximum_relative_residual": max_relative,
        "source_congruence_minimum_source_eigenvalue": min_source_eigenvalue,
        "route_rows": len(routes),
        "owned_native_routes": 0,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
