#!/usr/bin/env python3
"""Independent exact witness replay for G152."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def rho(T, L, X):
    return sp.simplify(X * (L - T) / (L + T))


def bracket_u_xi(T, beta, f, tau, sigma):
    """Coordinate components for u=(1/T,0), xi=(-f*beta,f)."""
    u = sp.Matrix([1 / T, 0])
    xi = sp.Matrix([-f * beta, f])
    coords = (tau, sigma)
    return sp.Matrix([
        sp.simplify(
            sum(u[j] * sp.diff(xi[i], coords[j]) for j in range(2))
            - sum(xi[j] * sp.diff(u[i], coords[j]) for j in range(2))
        )
        for i in range(2)
    ])


def main() -> None:
    tau, sigma = sp.symbols("tau sigma", real=True)
    cases = []

    for eps, T0 in ((1, sp.Rational(1, 3)), (-1, sp.Rational(3))):
        L0, X0 = sp.Rational(1), sp.Rational(2)
        rho0 = rho(T0, L0, X0)
        C = bracket_u_xi(T0, sp.S.Zero, sp.Rational(eps), tau, sigma)
        cases.append({
            "name": f"oriented_match_{eps}",
            "epsilon": eps,
            "rho": str(rho0),
            "matches": bool(rho0 == eps * L0),
            "bracket": [str(q) for q in C],
            "carried": all(q == 0 for q in C),
        })

    # Equality with the orthogonal ruler everywhere, but transverse lapse variation prevents carry.
    Ls = 1 + sigma / 10
    Ts = sp.simplify(Ls * (2 - Ls) / (2 + Ls))
    Cs = bracket_u_xi(Ts, sp.S.Zero, sp.S.One, tau, sigma)
    Cs0 = [sp.simplify(q.subs({tau: 0, sigma: 0})) for q in Cs]
    # C is returned in (partial_tau, partial_sigma).  Its normalized-u
    # coefficient is T*C^tau because u=(1/T)partial_tau.
    Cu0 = sp.simplify(Ts.subs(sigma, 0) * Cs0[0])

    # Constant connecting chord with half the natural ruler magnitude.
    fhalf = sp.Rational(1, 2)
    Chalf = bracket_u_xi(sp.S.One, sp.S.Zero, fhalf, tau, sigma)

    # Nonzero shift separates coordinate variation from the orthogonal ruler even when xi=r.
    shift = sp.Rational(1, 7)
    J1_un = sp.Matrix([shift * sp.Rational(1, 3), 1])
    xi_un = sp.Matrix([0, 1])

    gates = {
        "positive_oriented_match_carried": cases[0]["matches"] and cases[0]["carried"],
        "negative_oriented_match_carried": cases[1]["matches"] and cases[1]["carried"],
        "equality_without_carry_exact": (
            Cs0 == [-sp.Rational(1, 10), 0]
            and Cu0 == -sp.Rational(1, 30)
        ),
        "connecting_without_equality_exact": all(q == 0 for q in Chalf),
        "shift_separates_coordinate_and_orthogonal_variations": any(
            sp.simplify(q) != 0 for q in J1_un - xi_un
        ),
        "terminal_match_holds_in_shift_control": rho(sp.Rational(1, 3), 1, 2) == 1,
    }
    gates = {name: bool(value) for name, value in gates.items()}

    result = {
        "schema": "udt.g152.independent_witnesses.v1",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "orientation_cases": cases,
        "equality_without_carry": {
            "coordinate_bracket_at_origin": [str(q) for q in Cs0],
            "normalized_u_coefficient_at_origin": str(Cu0),
        },
        "connecting_without_equality": {
            "rho_over_L": "1/2",
            "bracket": [str(q) for q in Chalf],
        },
        "shift_control": {
            "J1_in_u_n": [str(q) for q in J1_un],
            "xi_in_u_n": [str(q) for q in xi_un],
        },
        "gates": gates,
        "scope": "exact finite witness replay; not a physical query or Xmax value",
    }
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
