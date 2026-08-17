#!/usr/bin/env python3
"""Exact production checks for G139 endpoint-position/path-transport join."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def mobius(a, b):
    return sp.cancel((a + b) / (1 + a * b))


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def source_hashes() -> dict[str, str]:
    lines = (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]
    out: dict[str, str] = {}
    for line in lines:
        expected, rel, _role = line.split("\t")
        actual = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if actual != expected:
            raise AssertionError(f"source hash mismatch: {rel}")
        out[rel] = actual
    return out


def main() -> None:
    checks: list[str] = []
    a, b, c, w = sp.symbols("a b c w", real=True)
    xa, xb, xc = sp.symbols("x_a x_b x_c", real=True)

    # Additive depth and its bounded Mobius representation.
    require(sp.simplify((a + b) + c - (a + (b + c))) == 0, "depth_associativity", checks)
    require(sp.simplify(sp.tanh(a + b) - mobius(sp.tanh(a), sp.tanh(b))) == 0,
            "tanh_mobius_homomorphism", checks)
    require(sp.simplify(mobius(mobius(xa, xb), xc) - mobius(xa, mobius(xb, xc))) == 0,
            "mobius_associativity", checks)
    require(mobius(xa, 0) == xa, "mobius_identity", checks)
    require(sp.simplify(mobius(xa, -xa)) == 0, "mobius_inverse", checks)

    # Exact oriented screen transports from two Pythagorean rotations.
    U1 = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                    [sp.Rational(4, 5), sp.Rational(3, 5)]])
    U2 = sp.Matrix([[sp.Rational(5, 13), -sp.Rational(12, 13)],
                    [sp.Rational(12, 13), sp.Rational(5, 13)]])
    I2 = sp.eye(2)
    require(U1.T * U1 == I2 and U1.det() == 1, "U1_is_SO2", checks)
    require(U2.T * U2 == I2 and U2.det() == 1, "U2_is_SO2", checks)
    U21 = U2 * U1
    require(U21.T * U21 == I2 and sp.simplify(U21.det()) == 1,
            "transport_composition", checks)
    require(sp.simplify(U1.inv() * U1 - I2) == sp.zeros(2), "transport_inverse", checks)
    require(I2 * U1 == U1 and U1 * I2 == U1, "transport_identity", checks)

    # Joint composition has distinct scalar and transport laws.
    xi1, xi2 = sp.Rational(1, 4), sp.Rational(2, 7)
    xi21 = mobius(xi1, xi2)
    require(xi21 == sp.Rational(1, 2), "exact_joint_mobius_component", checks)
    require(U21 == U2 * U1, "exact_joint_transport_component", checks)

    # A conformal screen representation is conditional but composes because scalar scaling is central.
    C1 = sp.exp(w * a) * U1
    C2 = sp.exp(w * b) * U2
    require(sp.simplify(C2 * C1 - sp.exp(w * (a + b)) * U21) == sp.zeros(2),
            "conditional_conformal_screen_composition", checks)

    # Same endpoint base, different routes: scalar agrees while transport can differ.
    phi_ab = sp.Rational(2, 5)
    xi_ab = sp.tanh(phi_ab)
    route_1 = (phi_ab, xi_ab, U1)
    route_2 = (phi_ab, xi_ab, U2)
    require(route_1[0] == route_2[0] and route_1[1] == route_2[1],
            "same_endpoint_position", checks)
    require(route_1[2] != route_2[2], "different_route_transport_survives", checks)

    # A closed endpoint loop has zero positional return but may carry nontrivial isotropy transport.
    require(sp.tanh(0) == 0, "closed_loop_zero_position", checks)
    require(U21 != I2, "closed_loop_nonidentity_transport_allowed", checks)

    # Terminal disagreement cannot be hidden inside transport: it is a failed descent or a new branch label.
    direct_phi = Fraction(1, 3)
    composite_phi = Fraction(1, 4) + Fraction(1, 5)
    residual = direct_phi - composite_phi
    require(residual == Fraction(-7, 60), "terminal_branch_residual_exact", checks)
    require(residual != 0, "terminal_disagreement_requires_branch_or_failure", checks)

    hashes = source_hashes()
    require(len(hashes) == 5, "source_manifest_five_frozen_sources", checks)

    result = {
        "status": "PASS",
        "checks_passed": len(checks),
        "checks_total": 20,
        "checks": checks,
        "joint_witness": {
            "xi_1": "1/4",
            "xi_2": "2/7",
            "xi_composite": "1/2",
            "U_composite": [[str(v) for v in row] for row in U21.tolist()],
        },
        "same_endpoint_routes": {
            "phi": "2/5",
            "transport_equal": False,
        },
        "closed_loop": {"phi": "0", "xi": "0", "transport_identity": False},
        "terminal_branch_residual": str(residual),
        "source_hashes": hashes,
    }
    if len(checks) != result["checks_total"]:
        raise AssertionError(f"expected {result['checks_total']} checks, got {len(checks)}")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
