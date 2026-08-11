#!/usr/bin/env python3
"""Exact G62 three-/four-observer network assembly algebra."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def rotation(p: sp.Expr, q: sp.Expr) -> sp.Matrix:
    """Rational SO(2) rotation from a Pythagorean pair."""
    den = p * p + q * q
    return sp.Matrix([[p * p - q * q, -2 * p * q], [2 * p * q, p * p - q * q]]) / den


def frame(seed: int, t: sp.Symbol) -> sp.Matrix:
    """Full lower-block time-live witness with every declared block active."""
    s = sp.Integer(seed)
    return sp.Matrix([
        [s + 2 + t, 1 + s * t, 0, 0],
        [0, s + 3, 0, 0],
        [1 + t, s, s + 4 + t, 1],
        [s - 1, 1 + 2 * t, 1 + s * t, s + 5],
    ])


def derive() -> dict[str, object]:
    checks: dict[str, bool] = {}
    one = sp.Integer(1)

    # Founded reciprocal character and terminal ratio.
    za, zb = sp.symbols("z_a z_b", nonzero=True)
    D = lambda z: sp.diag(1 / z, z)
    checks["reciprocal_character_composes"] = sp.simplify(D(zb) * D(za) - D(za * zb)) == sp.zeros(2)
    checks["reciprocal_character_reverses"] = sp.simplify(D(za).inv() - D(1 / za)) == sp.zeros(2)
    checks["terminal_ratio_composes_on_carried_depth"] = sp.simplify(
        za**-2 * zb**-2 - (za * zb)**-2
    ) == 0

    # Four object potentials: every triangle closes with no restriction on their values.
    phi = sp.symbols("phi0:4")
    kap = sp.symbols("kap0:4")
    delta = {(i, j): phi[j] - phi[i] for i in range(4) for j in range(4) if i != j}
    dkap = {(i, j): kap[j] - kap[i] for i in range(4) for j in range(4) if i != j}
    for i, j, k in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
        checks[f"phi_triangle_{i}{j}{k}"] = sp.expand(delta[i, j] + delta[j, k] - delta[i, k]) == 0
        checks[f"kappa_triangle_{i}{j}{k}"] = sp.expand(dkap[i, j] + dkap[j, k] - dkap[i, k]) == 0

    # General antisymmetric edge cochain and its four face periods.
    e01, e02, e03, e12, e13, e23 = sp.symbols("e01 e02 e03 e12 e13 e23")
    edges = {(0, 1): e01, (0, 2): e02, (0, 3): e03, (1, 2): e12, (1, 3): e13, (2, 3): e23}
    edges.update({(j, i): -value for (i, j), value in list(edges.items())})
    face = lambda i, j, k: sp.expand(edges[i, j] + edges[j, k] + edges[k, i])
    omega012, omega013 = face(0, 1, 2), face(0, 1, 3)
    omega023, omega123 = face(0, 2, 3), face(1, 2, 3)
    checks["pair_labelled_triangle_period_is_not_identity"] = omega012 != 0
    checks["tetrahedral_boundary_of_boundary_identity"] = sp.expand(
        omega123 - omega023 + omega013 - omega012
    ) == 0

    # Direct/composite and c_E terminal-ratio mismatch are the same scalar period.
    z01, z12, z02 = sp.symbols("z01 z12 z02", positive=True)
    monodromy = sp.simplify(z01 * z12 / z02)
    checks["direct_composite_depth_mismatch"] = monodromy != 1
    checks["direct_composite_terminal_ratio_mismatch"] = sp.simplify(
        (z01**-2 * z12**-2) / z02**-2 - monodromy**-2
    ) == 0
    checks["all_endpoint_ce_equality_trivializes_depth"] = sp.simplify(D(one) - sp.eye(2)) == sp.zeros(2)

    # SO(2) path carry with nonzero holonomy and exact four-face identity.
    R01, R02, R03 = rotation(2, 1), rotation(3, 1), rotation(4, 1)
    R12, R13, R23 = rotation(3, 2), rotation(4, 3), rotation(5, 2)
    Rs = {(0, 1): R01, (0, 2): R02, (0, 3): R03, (1, 2): R12, (1, 3): R13, (2, 3): R23}
    Rs.update({(j, i): value.T for (i, j), value in list(Rs.items())})
    for key, value in list(Rs.items())[:6]:
        checks[f"rotation_{key[0]}{key[1]}_orthogonal"] = sp.simplify(value.T * value) == sp.eye(2)
    H = lambda i, j, k: sp.simplify(Rs[k, i] * Rs[j, k] * Rs[i, j])
    H012, H013, H023, H123 = H(0, 1, 2), H(0, 1, 3), H(0, 2, 3), H(1, 2, 3)
    checks["angular_triangle_holonomy_nontrivial"] = H012 != sp.eye(2)
    checks["angular_holonomy_reversal"] = sp.simplify(H(0, 2, 1) - H012.inv()) == sp.zeros(2)
    # SO(2) is abelian, so oriented face products obey the discrete Bianchi identity.
    checks["angular_tetrahedral_bianchi_identity"] = sp.simplify(
        H123 * H023.inv() * H013 * H012.inv() - sp.eye(2)
    ) == sp.zeros(2)

    # Full time-live endpoint frames: direct transitions descend identically for arbitrary t.
    t = sp.symbols("t")
    frames = [frame(seed, t) for seed in (1, 2, 3, 4)]
    transitions = {(i, j): sp.simplify(frames[j] * frames[i].inv()) for i in range(4) for j in range(4) if i != j}
    for i, j, k in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)):
        checks[f"complete_frame_triangle_{i}{j}{k}"] = sp.simplify(
            transitions[j, k] * transitions[i, j] - transitions[i, k]
        ) == sp.zeros(4)
    checks["complete_frame_reversal"] = sp.simplify(transitions[1, 0] - transitions[0, 1].inv()) == sp.zeros(4)
    checks["complete_frame_time_derivative_of_descent"] = sp.simplify(
        sp.diff(transitions[1, 2] * transitions[0, 1] - transitions[0, 2], t)
    ) == sp.zeros(4)

    # Pair metric decomposition retains shift and a complete mixed supplied-Jacobian witness.
    V = sp.Matrix([[sp.Rational(1, 2), 0], [0, 2], [sp.Rational(1, 4), sp.Rational(1, 3)], [0, 0]])
    h = sp.simplify(V.T * sp.diag(-1, 1, 1, 1) * V)
    T2 = -h[0, 0]
    beta = sp.simplify(h[0, 1] / h[0, 0])
    L2 = sp.simplify(h[1, 1] - h[0, 1] ** 2 / h[0, 0])
    checks["mixed_pair_metric_exact"] = h == sp.Matrix([
        [sp.Rational(-3, 16), sp.Rational(1, 12)],
        [sp.Rational(1, 12), sp.Rational(37, 9)],
    ])
    checks["mixed_shift_retained"] = beta == sp.Rational(-4, 9)
    checks["mixed_orthogonal_ruler_retained"] = L2 == sp.Rational(112, 27)
    checks["mixed_metric_reconstruction"] = sp.simplify(
        sp.Matrix([[-T2, -T2 * beta], [-T2 * beta, L2 - T2 * beta**2]]) - h
    ) == sp.zeros(2)

    assert all(checks.values()), [key for key, value in checks.items() if not value]
    return {
        "status": "ASSEMBLY_IDENTITIES_ONLY_WITH_ROUTE_DEPENDENCE_OPEN",
        "exact_check_count": len(checks),
        "exact_checks": checks,
        "observer_count": 4,
        "triangle_count": 4,
        "scalar_face_periods": [str(omega012), str(omega013), str(omega023), str(omega123)],
        "nontrivial_scalar_period_witness": str(monodromy),
        "nontrivial_angular_holonomy_witness": str(H012),
        "owned_nonidentity_metric_history_restrictions": 0,
        "conditional_restriction": "ALL_ROUTE_DIRECT_EQUALS_COMPOSITE_IFF_RELEVANT_FACE_PERIODS_AND_HOLONOMIES_VANISH",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--read-only", action="store_true")
    args = parser.parse_args()
    result = derive()
    if not args.read_only:
        (HERE / "DERIVATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(
        f"PASS exact={result['exact_check_count']} observers={result['observer_count']} "
        f"triangles={result['triangle_count']} selected={result['owned_nonidentity_metric_history_restrictions']}"
    )


if __name__ == "__main__":
    main()
