#!/usr/bin/env python3
"""Independent G85 verifier; does not import the production derivation."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
G75 = ROOT / "udt_cmb_G75_center_regular_axial_profile_family_2026-08-11/PROFILE_ATLAS.tsv"
G84 = ROOT / "udt_cmb_G84_am_global_completion_pair_diameter_audit_2026-08-12/PROFILE_COMPLETION_ATLAS.tsv"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_manifest() -> None:
    rows = table(HERE / "SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 11
    assert all((ROOT / row["path"]).is_file() and sha(ROOT / row["path"]) == row["sha256"] for row in rows)


def independent_profile_census() -> tuple[dict[str, str], Counter[str], Counter[str]]:
    s = sp.symbols("s", real=True)
    source = {row["profile_id"]: row for row in table(G75) if row["lapse_name"] == "AM"}
    frozen = table(G84)
    assert len(source) == len(frozen) == 197
    q4: dict[str, str] = {}
    signs: Counter[str] = Counter()
    behaviors: Counter[str] = Counter()
    for row in frozen:
        if row["profile_id"] == "G75_F01_AM":
            continue
        src = source[row["profile_id"]]
        expr = sp.Poly(sp.sympify(src["q_of_s"], locals={"s": s}), s).as_expr()
        value = sp.factor(expr.subs(s, 4))
        assert value != 0
        assert sp.simplify(value - sp.sympify(row["q_at_s_4_exact"])) == 0
        q4[row["profile_id"]] = sp.sstr(value)
        signs["positive" if value > 0 else "negative"] += 1
        behaviors[src["behavior_class"]] += 1
    assert len(q4) == 196
    return q4, signs, behaviors


def independent_algebra() -> dict[str, str]:
    # Direct cofactor expansion, deliberately not a Matrix.det replay of production.
    u, b, h, D, z = sp.symbols("u b h D z", real=True)
    C = D * z
    H = h * z
    three_by_three = sp.expand(4 * u * C - b * b * C - 4 * H * H)
    determinant = sp.factor(D * three_by_three)
    schur = sp.factor(u - b * b / 4 - H * H / C)
    induced = sp.factor(D * (u * C - H * H))
    assert determinant == -D * z * (D * b**2 - 4 * D * u + 4 * h**2 * z)
    assert sp.simplify(schur + (D * b**2 - 4 * D * u + 4 * h**2 * z) / (4 * D)) == 0
    assert sp.simplify(induced + D * z * (-D * u + h**2 * z)) == 0
    return {
        "determinant": sp.sstr(determinant),
        "schur": sp.sstr(schur),
        "induced": sp.sstr(induced),
        "axis_gate": sp.sstr(4 * u - b**2),
    }


def smootherstep(y: float) -> float:
    if y <= 0:
        return 0.0
    if y >= 1:
        return 1.0
    return 6 * y**5 - 15 * y**4 + 10 * y**3


def gate(chi: float) -> float:
    edge = math.pi / 6
    plateau = math.pi / 3
    north = smootherstep((chi - edge) / (plateau - edge))
    south = smootherstep(((math.pi - chi) - edge) / (plateau - edge))
    return north * south


def numeric_signature_witnesses(q4: dict[str, str]) -> dict[str, float | int]:
    # Seam and neighboring points; amplitudes of h cannot spoil Lorentz signature because
    # they enter the temporal Schur complement with a negative square.
    min_shift_margin = math.inf
    min_lift_margin = math.inf
    checked = 0
    for tau in np.linspace(-math.pi, math.pi, 17):
        time_factor = 1.0 + 0.25 * math.sin(tau)
        for chi in np.linspace(math.pi / 6, 5 * math.pi / 6, 33):
            A = math.cos(chi) ** 2
            w = gate(chi)
            b = w * time_factor
            u_shift = -A
            u_lift = -A - w * time_factor
            shift_margin = b * b - 4 * u_shift
            lift_margin = -4 * u_lift
            if abs(chi - math.pi / 2) < 1e-12:
                min_shift_margin = min(min_shift_margin, shift_margin)
                min_lift_margin = min(min_lift_margin, lift_margin)
            assert shift_margin >= -1e-14
            assert lift_margin >= -1e-14
            checked += 1
    assert min_shift_margin >= 0.75**2
    assert min_lift_margin >= 3.0
    assert gate(math.pi / 6) == 0.0 and gate(math.pi / 2) == 1.0 and gate(5 * math.pi / 6) == 0.0
    assert len(q4) == 196
    return {
        "grid_checks": checked,
        "minimum_shift_axis_margin_at_seam": min_shift_margin,
        "minimum_lift_axis_margin_at_seam": min_lift_margin,
        "profiles_covered_by_symbolic_square_argument": len(q4),
    }


def kruskal_taper_check() -> dict[str, str]:
    U, V, htilde = sp.symbols("U V htilde", real=True)
    A = U * V / 4
    # h=A*htilde and dτ=dV/V-dU/U.
    coeff_dv = sp.simplify(A * htilde / V)
    coeff_du = sp.simplify(-A * htilde / U)
    assert coeff_dv == U * htilde / 4
    assert coeff_du == -V * htilde / 4
    return {
        "coefficient_dV": sp.sstr(coeff_dv),
        "coefficient_dU": sp.sstr(coeff_du),
        "result": "SMOOTH_WHEN_HTILDE_IS_SMOOTH",
    }


def verify_saved(q4: dict[str, str], signs: Counter[str], behaviors: Counter[str]) -> dict[str, object]:
    atlas = table(HERE / "PROFILE_ARCHETYPE_ATLAS.tsv")
    channels = table(HERE / "SEAM_CHANNEL_ATLAS.tsv")
    saved = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    assert len(atlas) == len({(row["profile_id"], row["archetype_id"]) for row in atlas}) == 980
    assert set(row["profile_id"] for row in atlas) == set(q4)
    assert all(row["q_at_4_exact"] == q4[row["profile_id"]] for row in atlas)
    per_profile = Counter(row["profile_id"] for row in atlas)
    assert set(per_profile.values()) == {5}
    classes = Counter(row["classification"] for row in atlas)
    expected = Counter({
        "POINTWISE_DEGENERATE": 392,
        "CONDITIONAL_ON_NONVANISHING_SHIFT": 196,
        "REGULAR_LORENTZ_NONNULL_SEAM": 196,
        "REGULAR_LORENTZ_UNIFORM_NULL_SEAM": 196,
    })
    assert classes == expected
    assert len(channels) == 8
    assert signs == Counter(saved["q4_sign_counts"])
    assert behaviors == Counter(saved["profile_behavior_counts"])
    assert saved["classification_counts"] == dict(sorted(classes.items()))
    assert not any(
        saved[key] for key in (
            "physical_profile_selected", "physical_topology_selected",
            "physical_Xmax_selected", "native_dynamics_selected",
        )
    )
    return {
        "atlas_rows": len(atlas),
        "unique_pairs": len(set((row["profile_id"], row["archetype_id"]) for row in atlas)),
        "classification_counts": dict(sorted(classes.items())),
        "channel_rows": len(channels),
    }


def main() -> None:
    verify_manifest()
    q4, signs, behaviors = independent_profile_census()
    result = {
        "schema": "udt-cmb-g85-independent-verification-v1",
        "status": "PASS",
        "implementation_independence": "NO_IMPORT_OF_PRODUCTION_DERIVATION",
        "profile_sign_counts": dict(sorted(signs.items())),
        "profile_behavior_counts": dict(sorted(behaviors.items())),
        "independent_algebra": independent_algebra(),
        "numeric_witnesses": numeric_signature_witnesses(q4),
        "kruskal_taper": kruskal_taper_check(),
        "saved_artifacts": verify_saved(q4, signs, behaviors),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
