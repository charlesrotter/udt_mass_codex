#!/usr/bin/env python3
"""Execute the preregistered G165 conformal-fiber rank audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_sources() -> list[dict[str, str]]:
    rows = read_tsv(PKG / "SOURCE_MANIFEST.tsv")
    assert len(rows) == 19
    for row in rows:
        payload = (ROOT / row["path"]).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == row["sha256"]
    return rows


def conformal_algebra() -> dict[str, object]:
    h00, h01, h11, w = sp.symbols("h00 h01 h11 w", real=True)
    h = sp.Matrix([[h00, h01], [h01, h11]])
    factor = sp.exp(2 * w)
    hs = factor * h
    det_h = sp.factor(h.det())
    det_hs = sp.factor(hs.det())

    phi_ratio = sp.simplify((-det_hs / hs[0, 0] ** 2) / (-det_h / h00**2))
    beta_delta = sp.simplify(hs[0, 1] / hs[0, 0] - h01 / h00)
    ceff_ratio = sp.simplify(
        ((-hs[0, 0]) ** 2 / (-det_hs)) / (((-h00) ** 2) / (-det_h))
    )
    half_density_fourth_ratio = sp.simplify((-det_hs) / (-det_h))

    q = sp.symbols("q", positive=True)
    chi = (1 - q) / (1 + q)
    chi_same = sp.simplify(chi.subs(q, q) - chi)

    v0, v1 = sp.symbols("v0 v1", real=True)
    v = sp.Matrix([v0, v1])
    causal_scale = sp.simplify((v.T * hs * v)[0] / (v.T * h * v)[0])

    x = sp.symbols("x", real=True)
    a = sp.Rational(1, 3)
    b = sp.Rational(2, 3)
    d = (x - a) * (b - x)
    bump_inside = sp.exp(-1 / d)
    center = sp.Rational(1, 2)
    bump_center = sp.simplify(bump_inside.subs(x, center))
    bump_prime_center = sp.simplify(sp.diff(bump_inside, x).subs(x, center))
    bump_second_center = sp.simplify(sp.diff(bump_inside, x, 2).subs(x, center))
    conformal_scalar_curvature_center = sp.simplify(
        -6 * sp.exp(-2 * bump_center) * bump_second_center
    )

    dimensional_matrix = sp.Matrix([[1, -1, 0], [3, -2, -1]])
    dimensional_nullspace = dimensional_matrix.nullspace()

    checks = {
        "determinant_weight_four": sp.simplify(det_hs / det_h - sp.exp(4 * w)) == 0,
        "phi_pair_invariant": phi_ratio == 1,
        "beta_invariant": beta_delta == 0,
        "ceff_ratio_invariant": ceff_ratio == 1,
        "chi_invariant_given_q": chi_same == 0,
        "half_density_weight_one_via_fourth_power": half_density_fourth_ratio == sp.exp(4 * w),
        "causal_polynomial_positive_scale": causal_scale == sp.exp(2 * w),
        "bump_nonzero_at_center": bump_center == sp.exp(-36),
        "bump_stationary_at_center": bump_prime_center == 0,
        "bump_changes_curvature": conformal_scalar_curvature_center != 0,
        "ce_g_dimensional_rank_two": dimensional_matrix.rank() == 2,
        "ce_g_leave_one_unit_direction": len(dimensional_nullspace) == 1,
        "ce_g_null_direction_equal_units": dimensional_nullspace[0] == sp.Matrix([1, 1, 1]),
    }
    assert all(checks.values())

    return {
        "checks": checks,
        "determinant_ratio": str(sp.exp(4 * w)),
        "causal_polynomial_ratio": str(sp.exp(2 * w)),
        "kappa_shift": "w",
        "bump_center": str(bump_center),
        "bump_second_center": str(bump_second_center),
        "conformal_scalar_curvature_center": str(conformal_scalar_curvature_center),
        "dimensional_rank": int(dimensional_matrix.rank()),
        "dimensional_nullspace": [[str(x) for x in dimensional_nullspace[0]]],
    }


def classify_candidates() -> tuple[list[dict[str, object]], dict[str, int]]:
    g155 = read_tsv(ROOT / "udt_g155_scale_sector_closure_whiteboard_2026-08-18/EQUATION_ROLE_LEDGER.tsv")
    assert len(g155) == 41
    physical_roles = {"PHYSICAL_HISTORY_CONSTRAINT", "PHYSICAL_HISTORY_EVOLUTION"}
    rows: list[dict[str, object]] = []
    for row in g155:
        survives = row["role"] in physical_roles and row["active_status"].startswith("ACTIVE")
        rows.append(
            {
                "candidate_id": f"G155_{row['equation_id']}",
                "source_scope": row["scope"],
                "source_role": row["role"],
                "g165_class": "OWNED_METRIC_RESTRICTOR" if survives else "EXCLUDED_BY_PREREGISTERED_ROLE",
                "survives_metric_restrictor_filter": survives,
                "conformal_rank": "UNTESTED" if survives else "0",
                "rationale": row["rationale"],
            }
        )

    post_classes = {
        "C01": ("META_CENSUS", False, "The frozen ledger is evidence, not a metric equation."),
        "C02": ("DEFINITION_OR_EVALUATOR", False, "Half-density is computed from supplied h."),
        "C03": ("SUPPLIED_CARRY_CHARACTER", False, "The physical cross-query carry is open."),
        "C04": ("CONDITIONAL_FLAT_SUBFAMILIES", False, "Chart, overlap, and Levi-Civita carries do not own physical nonisometric carry."),
        "C05": ("REPRESENTATION_CONSTRAINT", False, "Semidirect composition does not assign metric values."),
        "C06": ("REPRESENTATION_AND_EVALUATOR", False, "The score differentiates a supplied coframe history."),
        "C07": ("DEFINITION_OR_EVALUATOR", False, "Terminal descent reads supplied first jets."),
        "C08": ("NETWORK_ADMISSIBILITY", False, "Three-observer composition assumes supplied carries."),
        "C09": ("PRESENTATION_QUOTIENT", False, "The positive section removes gauge scaffolding only."),
        "C10": ("DEPENDENCY_CLASSIFICATION", False, "Rapidity absence does not restrict common scale."),
        "C11": ("DEPENDENCY_CLASSIFICATION", False, "X-free kernel closure is common-scale blind."),
        "C12": ("OPEN_PROPOSAL", False, "G164 is a ponder lead, not an active restriction."),
        "C13": ("VALUED_NETWORK_RECONSTRUCTION", False, "Complete pullback values already contain g."),
        "C14": ("VALUED_NETWORK_RECONSTRUCTION", False, "Equivalence decodes supplied values."),
        "C15": ("CALIBRATION_WITHOUT_BRIDGE", False, "c_E and G_obs leave one dimensional direction and no metric equation."),
        "C16": ("CONFORMAL_INVARIANT_READOUT", False, "Response and cones are conformally invariant."),
        "C17": ("UNVALUED_INCIDENCE", False, "Incidence contains no scale valuation."),
        "C18": ("FINITE_ANCHOR_DATA", False, "A compact smooth bump can vanish on every finite anchor neighborhood."),
    }
    candidates = read_tsv(PKG / "CANDIDATE_UNIVERSE.tsv")
    assert len(candidates) == 18
    for candidate in candidates:
        cls, survives, rationale = post_classes[candidate["candidate_id"]]
        rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "source_scope": candidate["source_scope"],
                "source_role": candidate["candidate_statement"],
                "g165_class": cls,
                "survives_metric_restrictor_filter": survives,
                "conformal_rank": "UNTESTED" if survives else "0",
                "rationale": rationale,
            }
        )

    counts = {
        "g155_rows": len(g155),
        "post_g155_candidates": len(candidates),
        "total_rows": len(rows),
        "owned_metric_restrictors": sum(bool(row["survives_metric_restrictor_filter"]) for row in rows),
        "valued_network_reconstruction_rows": sum(row["g165_class"] == "VALUED_NETWORK_RECONSTRUCTION" for row in rows),
        "conformal_invariant_or_anchor_rows": sum(
            row["g165_class"] in {"CONFORMAL_INVARIANT_READOUT", "UNVALUED_INCIDENCE", "FINITE_ANCHOR_DATA", "CALIBRATION_WITHOUT_BRIDGE"}
            for row in rows
        ),
    }
    assert counts == {
        "g155_rows": 41,
        "post_g155_candidates": 18,
        "total_rows": 59,
        "owned_metric_restrictors": 0,
        "valued_network_reconstruction_rows": 2,
        "conformal_invariant_or_anchor_rows": 4,
    }
    return rows, counts


def write_census(rows: list[dict[str, object]]) -> None:
    fields = [
        "candidate_id",
        "source_scope",
        "source_role",
        "g165_class",
        "survives_metric_restrictor_filter",
        "conformal_rank",
        "rationale",
    ]
    with (PKG / "CONDITION_CENSUS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    sources = verify_sources()
    algebra = conformal_algebra()
    rows, counts = classify_candidates()
    write_census(rows)

    primary = "NO_OWNED_NONIDENTITY_CONDITION"
    secondary = {
        "current_anchor_readout_map": "FUNCTIONAL_KERNEL",
        "full_valued_rank_complete_network": "VALUED_NETWORK_RECONSTRUCTION_ONLY",
        "anchor_only_closure": "FAILS_IN_FROZEN_REGULAR_ARENA",
    }
    result = {
        "primary_landing": primary,
        "secondary_classifications": secondary,
        "source_count": len(sources),
        "candidate_counts": counts,
        "algebra": algebra,
        "nonlinear_catch": {
            "compact_support_interval": ["1/3", "2/3"],
            "anchor_neighborhoods_preserved": True,
            "curvature_changed_at_center": True,
        },
        "maximum_conclusion": (
            "No owned metric restriction survives G165. The anchor map has a functional conformal "
            "kernel; a complete valued network reconstructs only its supplied scale."
        ),
    }
    (PKG / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
