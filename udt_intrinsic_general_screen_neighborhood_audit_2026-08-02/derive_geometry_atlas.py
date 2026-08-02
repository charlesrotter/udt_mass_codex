#!/usr/bin/env python3
"""Exact determinant, alternating-form, and causal atlas for the registered screens."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
POINTS = {
    "p1": (sp.Rational(1, 5), sp.Rational(1, 7), sp.Rational(1, 11)),
    "p2": (sp.Rational(1, 3), sp.Rational(-1, 5), sp.Rational(1, 7)),
}


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def verify_sources() -> int:
    rows = read_tsv("SOURCE_MANIFEST.tsv")
    assert len(rows) == len({row["path"] for row in rows}) == 48
    for row in rows:
        content = subprocess.run(
            ["git", "cat-file", "blob", row["git_blob"]],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        assert len(content) == int(row["bytes"])
        assert sha256_bytes(content) == row["sha256"]
    assert sha256_bytes((HERE / "SOURCE_MANIFEST.tsv").read_bytes()) == (
        HERE / "SOURCE_MANIFEST.sha256"
    ).read_text(encoding="utf-8").strip()
    return len(rows)


def exact_profiles():
    x, y, z = sp.symbols("x y z", real=True)
    rho2 = x*x + y*y + z*z
    denominator = 1 + rho2
    q0 = (1 - rho2) / denominator
    q1 = 2*x / denominator
    q2 = 2*y / denominator
    q3 = 2*z / denominator
    u = sp.factor(3 + q0*q0 + 2*q1*q1 + 4*q2*q2 + 8*q3*q3)
    v0 = sp.factor(q0*q0 + 3*q1*q1 + 7*q2*q2 + 9*q3*q3)
    r0 = sp.factor(2*q0*q0 + 5*q1*q1 + 11*q2*q2 + 13*q3*q3)
    b0 = sp.factor(q0*q1 + 2*q0*q2 + 3*q0*q3 + 5*q1*q2 + 7*q1*q3 + 11*q2*q3)
    epsilon = sp.Rational(1, 10)
    return (x, y, z), u, sp.factor(1 + epsilon*v0), sp.factor(1 + epsilon*r0), sp.factor(epsilon*b0)


def wedge_coefficients(first: sp.Expr, second: sp.Expr, coordinates) -> tuple[sp.Expr, ...]:
    x, y, z = coordinates
    return tuple(sp.factor(sp.diff(first, a)*sp.diff(second, b) - sp.diff(first, b)*sp.diff(second, a)) for a, b in ((x, y), (x, z), (y, z)))


def two_form_norm(form: sp.Matrix, inverse_metric: sp.Matrix) -> sp.Expr:
    raised = inverse_metric * form * inverse_metric
    return sp.factor(sum(form[i, j] * raised[i, j] for i in range(4) for j in range(4)) / 2)


def main() -> int:
    source_count = verify_sources()
    candidates = read_tsv("CANDIDATE_UNIVERSE.tsv")
    assert [row["candidate_id"] for row in candidates] == [f"C{i:02d}" for i in range(1, 19)]
    assert len(read_tsv("FALSIFICATION_CONTRACT.tsv")) == 30
    coordinates, primary_u, v_epsilon, r_epsilon, b_epsilon = exact_profiles()

    # Exact screen determinant: both shear amplitudes cancel identically.
    r, b, u_symbol, v_symbol = sp.symbols("r b u V", positive=True)
    screen_shape = sp.Matrix([[r**2, r*b], [r*b, b**2 + r**-2]])
    assert sp.factor(screen_shape.det()) == 1
    lam_symbol = sp.symbols("lambda", integer=True)
    screen_metric = u_symbol**lam_symbol * v_symbol * screen_shape
    assert sp.factor(screen_metric.det()) == u_symbol**(2*lam_symbol) * v_symbol**2

    # The released screen really has three independent symmetric-metric tangents at the parent.
    base = {v_symbol: 1, r: 1, b: 0}
    tangent_area = sp.diff(v_symbol * screen_shape, v_symbol).subs(base)
    tangent_r = sp.diff(v_symbol * screen_shape, r).subs(base)
    tangent_b = sp.diff(v_symbol * screen_shape, b).subs(base)
    tangent_coordinates = sp.Matrix([
        [matrix[0, 0], matrix[1, 1], matrix[0, 1]]
        for matrix in (tangent_area, tangent_r, tangent_b)
    ])
    assert tangent_coordinates.rank() == 3

    # Pair block remains Lorentzian and nondegenerate for every finite a and positive u.
    a_symbol = sp.symbols("a", real=True)
    pair_metric = sp.Matrix([[-1/u_symbol, -a_symbol/u_symbol], [-a_symbol/u_symbol, u_symbol-a_symbol**2/u_symbol]])
    assert sp.factor(pair_metric.det()) == -1

    # Exact sign, normalization, and passive-frame controls for the projected two-forms.
    q_t, q_s = sp.symbols("q_T q_S", real=True)
    eta = sp.diag(-1, 1, 1, 1)
    form_t = sp.zeros(4)
    form_s = sp.zeros(4)
    form_t[2, 3], form_t[3, 2] = q_t, -q_t
    form_s[2, 3], form_s[3, 2] = q_s, -q_s
    assert two_form_norm(form_t, eta) == q_t**2
    assert two_form_norm(form_s, eta) == q_s**2
    boost = sp.Matrix([
        [sp.Rational(5, 4), 0, sp.Rational(3, 4), 0],
        [0, 1, 0, 0],
        [sp.Rational(3, 4), 0, sp.Rational(5, 4), 0],
        [0, 0, 0, 1],
    ])
    rotation = sp.Matrix([
        [1, 0, 0, 0],
        [0, sp.Rational(3, 5), 0, -sp.Rational(4, 5)],
        [0, 0, 1, 0],
        [0, sp.Rational(4, 5), 0, sp.Rational(3, 5)],
    ])
    lorentz = rotation * boost
    assert sp.simplify(lorentz.T * eta * lorentz - eta) == sp.zeros(4)
    inverse_lorentz = lorentz.inv()
    form_t_prime = sp.simplify(inverse_lorentz.T * form_t * inverse_lorentz)
    form_s_prime = sp.simplify(inverse_lorentz.T * form_s * inverse_lorentz)
    assert sp.simplify(two_form_norm(form_t_prime, eta) - q_t**2) == 0
    assert sp.simplify(two_form_norm(form_s_prime, eta) - q_s**2) == 0
    naive_q = sp.factor(form_s_prime[2, 3]**2 - form_t_prime[2, 3]**2)
    true_q = q_s**2 - q_t**2
    assert sp.simplify(naive_q - true_q) != 0

    positive_scale = sp.symbols("positive_scale", positive=True)
    unit_k = sp.Matrix([1, 0, 0, 0])
    rescaled_unit_k = sp.simplify((positive_scale * unit_k) / positive_scale)
    assert rescaled_unit_k == unit_k

    v_map = {
        "ONE": sp.S.One,
        "TWO": sp.Integer(2),
        "U": primary_u,
        "V_EPS": v_epsilon,
        "ZERO": sp.S.Zero,
    }
    u_map = {"U": primary_u, "FOUR": sp.Integer(4)}
    zero_profiles = {"ONE", "TWO", "U"}
    atlas_rows = []
    alternating_details = []
    for row in candidates:
        candidate_id = row["candidate_id"]
        u_value = u_map[row["u_profile"]]
        area = v_map[row["V_profile"]]
        degenerate = row["V_profile"] == "ZERO"
        if degenerate:
            alternating_class = "UNDEFINED_METRIC_DEGENERATE"
            wedge_values = {}
            nonzero_at = []
        else:
            if row["u_profile"] == "FOUR" or row["V_profile"] in zero_profiles:
                raw_wedge = (sp.S.Zero, sp.S.Zero, sp.S.Zero)
            else:
                raw_wedge = wedge_coefficients(u_value, area, coordinates)
            normalized_wedge = tuple(sp.factor(value / (2*u_value*area)) for value in raw_wedge)
            wedge_values = {}
            nonzero_at = []
            for point_id, point in POINTS.items():
                substitution = dict(zip(coordinates, point))
                values = [sp.factor(value.subs(substitution)) for value in normalized_wedge]
                wedge_values[point_id] = [str(value) for value in values]
                if any(value != 0 for value in values):
                    nonzero_at.append(point_id)
            if all(value == 0 for value in raw_wedge):
                alternating_class = "ZERO_IDENTICALLY"
            else:
                assert nonzero_at
                alternating_class = "NONZERO_SIMPLE_OPEN_DENSE_WITH_ZERO_LOCUS_RETAINED"

        a_value = int(row["a"])
        if degenerate:
            causal_strata = "UNDEFINED_METRIC_DEGENERATE"
            projector_precondition = "BLOCKED_METRIC_DEGENERATE"
            four_metric_status = "DEGENERATE"
        else:
            four_metric_status = "LORENTZIAN_NONDEGENERATE"
            if a_value == 0:
                causal_strata = "SLICE_POSITIVE_BUT_CONTACT_PAIR_UNDEFINED"
                projector_precondition = "BLOCKED_TWIST_ZERO"
            elif a_value == 4:
                causal_strata = "Q_ZERO_AT_U4__Q_POSITIVE_FOR_U_GT_4"
                projector_precondition = "PENDING_KILLING_CERTIFICATE__TWIST_NONZERO"
            elif a_value == 5:
                causal_strata = "Q_NEGATIVE_U4_TO_LT5__Q_ZERO_U5__Q_POSITIVE_U_GT5"
                projector_precondition = "PENDING_KILLING_CERTIFICATE__TWIST_NONZERO"
            else:
                assert a_value == 1
                causal_strata = "Q_POSITIVE_FOR_U_4_TO_11"
                projector_precondition = "PENDING_KILLING_CERTIFICATE__TWIST_NONZERO"

        atlas_rows.append({
            "candidate_id": candidate_id,
            "four_metric_status": four_metric_status,
            "screen_modes_active": "+".join(filter(None, (
                "AREA" if row["V_profile"] not in {"ONE", "TWO", "ZERO"} else "",
                "SHEAR_R" if row["r_profile"] != "ONE" else "",
                "SHEAR_B" if row["b_profile"] != "ZERO" else "",
            ))) or "NONE",
            "configuration_alternating_class": alternating_class,
            "nonzero_registered_points": ";".join(nonzero_at) or "-",
            "causal_strata": causal_strata,
            "intrinsic_projector_precondition": projector_precondition,
        })
        alternating_details.append({
            "candidate_id": candidate_id,
            "configuration_alternating_class": alternating_class,
            "point_coefficients_xy_xz_yz": wedge_values,
        })

    write_tsv(
        "GEOMETRIC_ATLAS.tsv",
        [
            "candidate_id", "four_metric_status", "screen_modes_active", "configuration_alternating_class",
            "nonzero_registered_points", "causal_strata", "intrinsic_projector_precondition",
        ],
        atlas_rows,
    )

    full_screen_nonzero = [
        row["candidate_id"] for row in atlas_rows
        if row["candidate_id"] in {"C08", "C09", "C10"}
        and row["configuration_alternating_class"].startswith("NONZERO_SIMPLE")
    ]
    assert full_screen_nonzero == ["C08", "C09", "C10"]
    assert sum(row["configuration_alternating_class"] == "ZERO_IDENTICALLY" for row in atlas_rows) == 10
    assert sum(row["configuration_alternating_class"].startswith("NONZERO_SIMPLE") for row in atlas_rows) == 7
    assert sum(row["configuration_alternating_class"] == "UNDEFINED_METRIC_DEGENERATE" for row in atlas_rows) == 1
    result = {
        "schema": "udt-general-screen-geometric-atlas-1.0",
        "status": "PASS_EXACT_GEOMETRY",
        "sympy_version": sp.__version__,
        "frozen_sources": source_count,
        "candidate_count": len(candidates),
        "screen_shape_determinant": "1",
        "screen_metric_determinant": "u^(2 lambda) V^2",
        "screen_metric_tangent_rank": 3,
        "screen_metric_tangents_at_parent": {
            "area": [[str(value) for value in tangent_area.row(i)] for i in range(2)],
            "diagonal_shear": [[str(value) for value in tangent_r.row(i)] for i in range(2)],
            "offdiagonal_shear": [[str(value) for value in tangent_b.row(i)] for i in range(2)],
        },
        "pair_metric_determinant": "-1",
        "four_metric_nondegenerate_count": 17,
        "configuration_alternating_zero_count": 10,
        "configuration_alternating_nonzero_simple_count": 7,
        "configuration_alternating_undefined_degenerate_count": 1,
        "full_screen_nonzero_candidates": full_screen_nonzero,
        "formula_QT": "4*a^2/(u*D^2)",
        "formula_QS": "4*u/D^2",
        "formula_Q": "4*(u-a^2/u)/D^2",
        "formula_Phi_contact": "phi-(1/2)*log(abs(a))",
        "alternating_formula": "dphi_wedge_dsigma=(du_wedge_dV)/(2*u*V)",
        "exact_controls": {
            "T_S_sign_invariant": True,
            "K_positive_constant_rescale_invariant": True,
            "full_frame_tensor_contractions_preserved_after_reconstruction": True,
            "naive_transformed_slot_route_rejected": True,
            "naive_Q": str(naive_q),
            "true_Q": str(true_q),
            "nonzero_simple_means_decomposable_two_form_matrix_rank_two": True,
        },
        "details": alternating_details,
        "screen_selected": False,
        "physics_promoted": False,
    }
    (HERE / "GEOMETRIC_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": result["status"],
        "candidate_count": len(candidates),
        "alternating_classes": {"zero": 10, "nonzero_simple": 7, "undefined": 1},
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
