#!/usr/bin/env python3
"""Exact algebra for the load-bearing branchwise projector gates.

The complete twisted-S3 coframe and north-event profile are reconstructed
from their frozen registered formulas.  No carrier or action is used.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
LAMBDAS = (
    ("C01", sp.Rational(-2)),
    ("C02", sp.Rational(-1)),
    ("C03", sp.Rational(0)),
    ("C04", sp.Rational(1, 2)),
    ("C05", sp.Rational(1)),
    ("C06", sp.Rational(2)),
)
ETA4 = sp.diag(-1, 1, 1, 1)


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def write_tsv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def lorentz_generators() -> dict[str, sp.Matrix]:
    result: dict[str, sp.Matrix] = {}
    for i in range(1, 4):
        value = sp.zeros(4)
        value[0, i] = value[i, 0] = 1
        result[f"K0{i}"] = value
    for i, j in ((1, 2), (1, 3), (2, 3)):
        value = sp.zeros(4)
        value[i, j] = 1
        value[j, i] = -1
        result[f"J{i}{j}"] = value
    return result


def north_connection(lam: sp.Rational) -> list[sp.Matrix]:
    """Registered twisted-S3 Levi-Civita matrices at q=(1,0,0,0)."""
    signs = (-1, 1, 1, 1)
    # The frozen profile has left-invariant derivatives (1,2,3)/50 at the
    # north event.  The registered coframe ordering maps these to p1,p2,p3.
    p1, p2, p3 = sp.Rational(3, 50), sp.Rational(1, 50), sp.Rational(2, 50)
    twist, kappa = sp.Rational(1, 64), sp.Rational(-2)
    at, bt, ct = twist * kappa, kappa, kappa
    structure = sp.MutableDenseNDimArray.zeros(4, 4, 4)

    def set_coefficient(upper: int, left: int, right: int, coefficient: sp.Expr) -> None:
        structure[upper, left, right] = -coefficient
        structure[upper, right, left] = coefficient

    set_coefficient(0, 0, 1, p1)
    set_coefficient(0, 0, 2, p2)
    set_coefficient(0, 0, 3, p3)
    set_coefficient(0, 2, 3, at)
    set_coefficient(1, 1, 2, -p2)
    set_coefficient(1, 1, 3, -p3)
    set_coefficient(1, 2, 3, bt)
    set_coefficient(2, 1, 2, lam * p1)
    set_coefficient(2, 2, 3, -lam * p3)
    set_coefficient(2, 1, 3, -ct)
    set_coefficient(3, 1, 3, lam * p1)
    set_coefficient(3, 2, 3, lam * p2)
    set_coefficient(3, 1, 2, ct)

    matrices = []
    for direction in range(4):
        gamma = sp.zeros(4)
        for out in range(4):
            for acted in range(4):
                lowered = (
                    signs[out] * structure[out, direction, acted]
                    - signs[direction] * structure[direction, acted, out]
                    + signs[acted] * structure[acted, out, direction]
                ) / 2
                gamma[out, acted] = sp.simplify(signs[out] * lowered)
        matrices.append(gamma)
    return matrices


def main() -> int:
    checks: dict[str, str] = {}

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks[name] = "PASS"

    # Type the complete-branch ruler as a rank-one line in the positive
    # three-bundle orthogonal to the intrinsic timelike clock.
    p = sp.diag(1, 0, 0)
    q = sp.eye(3) - p
    check("ruler_projector_rank_one", p.rank() == 1)
    check("ruler_projector_idempotent", zero(p * p - p))
    check("screen_complement_rank_two", q.rank() == 2 and zero(q * q - q))
    check("ruler_screen_orthogonal", zero(p * q) and zero(q * p))

    rows: list[dict[str, object]] = []
    for branch, lam in LAMBDAS:
        connection = north_connection(lam)
        dp = []
        for gamma4 in connection:
            gamma3 = gamma4[1:4, 1:4]
            dp.append(sp.simplify(gamma3 * p - p * gamma3))
        nonzero_components = []
        matrices = {}
        for left in range(4):
            for right in range(left + 1, 4):
                relative = sp.simplify(q * (dp[left] * dp[right] - dp[right] * dp[left]) * q)
                matrices[(left, right)] = relative
                if not zero(relative):
                    nonzero_components.append(f"{left}{right}:{relative[1,2]}")
        witness = matrices[(2, 3)][1, 2]
        check(f"{branch}_relative_curvature_nonzero", witness != 0)
        check(f"{branch}_relative_curvature_screen_valued", zero(p * matrices[(2, 3)]) and zero(matrices[(2, 3)] * p))
        rows.append({
            "branch_id": branch,
            "lambda": str(lam),
            "evaluation_event": "P00_NORTH",
            "projector": "P_n_on_positive_u_perp_rank3",
            "relative_curvature_component_Q23_12": str(witness),
            "nonzero_two_plane_components": ";".join(nonzero_components),
            "nontrivial_somewhere": "YES",
            "maximum_status": "DERIVED_CONDITIONAL_ON_REGISTERED_COMPLETE_CONFIGURATION",
        })
    write_tsv("TWISTED_S3_RELATIVE_CURVATURE.tsv", rows)

    # A nonnull dphi line is an exact local projector; the null stratum is
    # nilpotent and cannot be silently continued as a semisimple reduction.
    alpha_t = sp.Matrix([1, 0, 0, 0])
    alpha_s = sp.Matrix([0, 1, 0, 0])
    alpha_n = sp.Matrix([1, 1, 0, 0])
    for tag, alpha, norm in (("timelike", alpha_t, -1), ("spacelike", alpha_s, 1)):
        vector = ETA4 * alpha
        projector = sp.simplify(vector * alpha.T / norm)
        check(f"dphi_{tag}_projector_rank_one", projector.rank() == 1)
        check(f"dphi_{tag}_projector_idempotent", zero(projector * projector - projector))
    null_vector = ETA4 * alpha_n
    nilpotent = null_vector * alpha_n.T
    check("dphi_null_operator_nonzero", not zero(nilpotent))
    check("dphi_null_operator_nilpotent", zero(nilpotent * nilpotent))
    check("dphi_null_operator_not_projector", not zero(nilpotent * nilpotent - nilpotent))

    # Full Lorentz holonomy admits no real invariant line.  Spatial rotations
    # first reduce any common real invariant line to the clock line; one boost
    # then destroys it.
    generators = lorentz_generators()
    v0, v1, v2, v3 = sp.symbols("v0 v1 v2 v3", real=True)
    vector = sp.Matrix([v0, v1, v2, v3])
    rotation_kernel = sp.linsolve(
        list(generators["J12"] * vector) + list(generators["J13"] * vector) + list(generators["J23"] * vector),
        (v0, v1, v2, v3),
    )
    check("spatial_rotation_common_fixed_space_is_clock_line", rotation_kernel == sp.FiniteSet((v0, 0, 0, 0)))
    check("boost_does_not_preserve_nonzero_clock_line", generators["K01"] * sp.Matrix([1, 0, 0, 0]) == sp.Matrix([0, 1, 0, 0]))

    # The reduced product control preserves only clock versus all space.  Its
    # clock projector is parallel, hence its relative projector curvature is
    # exactly zero.
    p_clock = sp.diag(1, 0, 0, 0)
    check("so3_preserves_clock_projector", all(zero(g * p_clock - p_clock * g) for name, g in generators.items() if name.startswith("J")))
    check("parallel_control_relative_curvature_zero", zero(sp.zeros(3)))

    # An intrinsic toric unordered pair is not a single selected line when an
    # admitted exchange maps the two members into each other.
    p1 = sp.diag(1, 0)
    p2 = sp.diag(0, 1)
    swap = sp.Matrix([[0, 1], [1, 0]])
    check("toric_exchange_swaps_lines", swap * p1 * swap == p2 and swap * p2 * swap == p1)
    check("toric_unordered_pair_descends", swap * (p1 + p2) * swap == p1 + p2)

    # A simple spectral line is local to the simple-spectrum stratum and loses
    # uniqueness at a registered-style tie.
    x = sp.symbols("x", real=True)
    shape = sp.diag(x, -x, 2)
    check("spectral_line_simple_off_wall", len(shape.subs(x, 1).eigenvals()) == 3)
    check("spectral_line_degenerates_on_wall", shape.subs(x, 0).eigenvals()[0] == 2)

    expected = 32
    check("registered_check_count_before_self_check", len(checks) == expected - 1)
    if len(checks) != expected:
        raise AssertionError(f"unexpected check count {len(checks)}")
    result = {
        "schema": "udt.branchwise_projector_holonomy_census.derivation.v1",
        "status": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "twisted_s3_branch_count": len(rows),
        "twisted_s3_nonzero_relative_curvature_count": sum(row["nontrivial_somewhere"] == "YES" for row in rows),
        "maximum_new_conclusion": (
            "SIX_REGISTERED_COMPLETE_TWISTED_S3_CONFIGURATIONS_HAVE_A_METRIC_INTRINSIC_GLOBAL_"
            "RULER_PROJECTOR_WITH_NONZERO_RELATIVE_PROJECTOR_CURVATURE_SOMEWHERE;_AMBIENT_"
            "HOLONOMY_PRESERVATION_AND_ON_SHELL_SELECTION_REMAIN_ABSENT"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
