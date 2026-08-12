#!/usr/bin/env python3
"""Independent exact verification of the G84 completion and profile census."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROFILE_PATH = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def verify_sources() -> int:
    manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
    assert len(manifest) == 14
    for row in manifest:
        assert digest(ROOT / row["path"]) == row["sha256"]
    return len(manifest)


def embedded_checks() -> dict[str, object]:
    chi, tau, theta, psi, R, separation = sp.symbols(
        "chi tau theta psi R separation", real=True, positive=True,
    )
    n = sp.Matrix([
        sp.sin(theta) * sp.cos(psi),
        sp.sin(theta) * sp.sin(psi),
        sp.cos(theta),
    ])
    spatial = sp.Matrix([2 * R * sp.cos(chi), *[2 * R * sp.sin(chi) * item for item in n]])
    spatial_coordinates = (chi, theta, psi)
    induced_spatial = sp.Matrix([
        [sp.simplify(sp.diff(spatial, a).dot(sp.diff(spatial, b))) for b in spatial_coordinates]
        for a in spatial_coordinates
    ])
    expected_spatial = sp.diag(
        4 * R**2,
        4 * R**2 * sp.sin(chi)**2,
        4 * R**2 * sp.sin(chi)**2 * sp.sin(theta)**2,
    )
    assert all(sp.trigsimp(induced_spatial[i, j] - expected_spatial[i, j]) == 0 for i in range(3) for j in range(3))

    spacetime = sp.Matrix([
        2 * R * sp.cos(chi) * sp.sinh(tau / 2),
        *[2 * R * sp.sin(chi) * item for item in n],
        2 * R * sp.cos(chi) * sp.cosh(tau / 2),
    ])
    eta = sp.diag(-1, 1, 1, 1, 1)
    spacetime_coordinates = (tau, chi, theta, psi)
    induced_spacetime = sp.Matrix([
        [sp.simplify((sp.diff(spacetime, a).T * eta * sp.diff(spacetime, b))[0]) for b in spacetime_coordinates]
        for a in spacetime_coordinates
    ])
    expected_spacetime = sp.diag(
        -R**2 * sp.cos(chi)**2,
        4 * R**2,
        4 * R**2 * sp.sin(chi)**2,
        4 * R**2 * sp.sin(chi)**2 * sp.sin(theta)**2,
    )
    assert all(sp.trigsimp(induced_spacetime[i, j] - expected_spacetime[i, j]) == 0 for i in range(4) for j in range(4))

    phi = -sp.log(sp.cos(separation / (2 * R)))
    ratio = sp.cos(separation / (2 * R))**2
    assert sp.simplify(sp.exp(-2 * phi) - ratio) == 0
    assert sp.limit(phi, separation, sp.pi * R, dir="-") == sp.oo
    assert sp.limit(ratio, separation, sp.pi * R, dir="-") == 0
    return {
        "spatial_embedding_reproduced": True,
        "zero_mix_spacetime_embedding_reproduced": True,
        "spatial_radius_over_R": 2,
        "spatial_diameter_over_R": "2*pi",
        "center_to_static_horizon_over_R": "pi",
        "recentered_phi_limit": "POSITIVE_INFINITY",
        "recentered_c_eff_limit": "ZERO",
    }


def independent_profile_census() -> tuple[list[dict[str, object]], Counter[str]]:
    s = sp.symbols("s", real=True)
    profiles = [row for row in rows(PROFILE_PATH) if row["lapse_name"] == "AM"]
    assert len(profiles) == len({row["profile_id"] for row in profiles}) == 197
    output = []
    for row in profiles:
        expression = sp.sympify(row["q_of_s"], locals={"s": s})
        q4 = sp.simplify(expression.subs(s, 4))
        if row["shape_id"] == "ZERO":
            classification = "ZERO_MIXING_CONSTANT_CURVATURE_GLOBAL_EXTENSION_EXISTS"
        elif q4 != 0:
            classification = "NONZERO_BIFURCATION_MIXING__STANDARD_SMOOTH_SYMMETRY_EXTENSION_OBSTRUCTED"
        else:
            classification = "MIXING_VANISHES_AT_BIFURCATION__FURTHER_EXTENSION_AUDIT_REQUIRED"
        output.append({
            "profile_id": row["profile_id"],
            "q4": sp.sstr(q4),
            "h2": sp.sstr(sp.simplify(4 * q4)),
            "classification": classification,
        })
    return output, Counter(str(row["classification"]) for row in output)


def main() -> None:
    source_rows = verify_sources()
    embedded = embedded_checks()
    independent, counts = independent_profile_census()
    production = rows(HERE / "PROFILE_COMPLETION_ATLAS.tsv")
    assert len(production) == len(independent) == 197
    production_by_id = {row["profile_id"]: row for row in production}
    mismatches = []
    for row in independent:
        saved = production_by_id[row["profile_id"]]
        if (
            saved["q_at_s_4_exact"] != row["q4"]
            or saved["h_at_x_2_exact"] != row["h2"]
            or saved["extension_class"] != row["classification"]
        ):
            mismatches.append(row["profile_id"])
    assert not mismatches
    assert counts == {
        "ZERO_MIXING_CONSTANT_CURVATURE_GLOBAL_EXTENSION_EXISTS": 1,
        "NONZERO_BIFURCATION_MIXING__STANDARD_SMOOTH_SYMMETRY_EXTENSION_OBSTRUCTED": 196,
    }

    recentered = rows(HERE / "RECENTERED_OBSERVER_LIMIT_ATLAS.tsv")
    assert len(recentered) == 4
    for row in recentered:
        receiver = float(sp.Rational(row["fixed_chart_receiver_x"]))
        expected = math.pi - 2 * math.asin(receiver / 2)
        observed = float(sp.N(sp.sympify(row["fixed_chart_distance_to_original_horizon_over_R"]), 40))
        assert math.isclose(observed, expected, rel_tol=1e-15)
        assert row["recentered_own_horizon_distance_over_R"] == "pi"

    result = {
        "schema": "udt-cmb-g84-independent-verification-v1",
        "status": "PASS",
        "source_manifest_rows": source_rows,
        "embedded_checks": embedded,
        "profile_rows": len(independent),
        "profile_mismatches": mismatches,
        "extension_class_counts": dict(sorted(counts.items())),
        "recentered_rows": len(recentered),
        "scope": "zero-mixing constant-curvature branch plus exact continued q(4) census; generic time-live mixed completion remains open",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
