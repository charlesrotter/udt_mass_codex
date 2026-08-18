#!/usr/bin/env python3
"""Independent coordinate calculation for the frozen G151 Jacobi witness."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def main() -> None:
    t, x, y, z = sp.symbols("t x y z", real=True)
    coords = (t, x, y, z)
    L = 1 + t / sp.Integer(10) + t**2 / sp.Integer(20)
    T = sp.simplify(L * (2 - L) / (2 + L))
    g = sp.diag(-T**2, L**2, 1, 1)
    gi = sp.simplify(g.inv())
    dim = 4

    Gamma = [[[sp.S.Zero for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for r in range(dim):
        for m in range(dim):
            for nidx in range(dim):
                Gamma[r][m][nidx] = sp.simplify(sum(
                    gi[r, s] * (
                        sp.diff(g[s, nidx], coords[m])
                        + sp.diff(g[s, m], coords[nidx])
                        - sp.diff(g[m, nidx], coords[s])
                    ) / 2
                    for s in range(dim)
                ))

    def covD(X: sp.Matrix, V: sp.Matrix) -> sp.Matrix:
        return sp.Matrix([
            sp.simplify(
                sum(X[m] * sp.diff(V[r], coords[m]) for m in range(dim))
                + sum(Gamma[r][m][nidx] * X[m] * V[nidx]
                      for m in range(dim) for nidx in range(dim))
            )
            for r in range(dim)
        ])

    def Rcomponent(r: int, s: int, m: int, nidx: int):
        # R^r_{s m n}: R(partial_m,partial_n)partial_s.
        return sp.simplify(
            sp.diff(Gamma[r][nidx][s], coords[m])
            - sp.diff(Gamma[r][m][s], coords[nidx])
            + sum(
                Gamma[r][m][k] * Gamma[k][nidx][s]
                - Gamma[r][nidx][k] * Gamma[k][m][s]
                for k in range(dim)
            )
        )

    u = sp.Matrix([1 / T, 0, 0, 0])
    xi = sp.Matrix([0, 1, 0, 0])
    nvec = sp.Matrix([0, 1 / L, 0, 0])

    acceleration = sp.simplify(covD(u, u))
    Dxi = sp.simplify(covD(u, xi))
    D2xi = sp.simplify(covD(u, Dxi))
    Rxi = sp.Matrix([
        sp.simplify(sum(
            Rcomponent(r, s, m, nidx) * u[s] * xi[m] * u[nidx]
            for s in range(dim) for m in range(dim) for nidx in range(dim)
        ))
        for r in range(dim)
    ])

    bracket = sp.Matrix([
        sp.simplify(
            sum(u[m] * sp.diff(xi[r], coords[m]) for m in range(dim))
            - sum(xi[m] * sp.diff(u[r], coords[m]) for m in range(dim))
        )
        for r in range(dim)
    ])

    phi_ratio = sp.simplify(L / T)
    rho_from_terminal = sp.simplify(2 * (phi_ratio - 1) / (phi_ratio + 1))
    rho_dot = sp.simplify(u[0] * sp.diff(rho_from_terminal, t))
    rho_ddot = sp.simplify(u[0] * sp.diff(rho_dot, t))

    def at_zero(v):
        if isinstance(v, sp.MatrixBase):
            return v.applyfunc(lambda q: sp.simplify(q.subs(t, 0)))
        return sp.simplify(v.subs(t, 0))

    g0, T0, L0 = at_zero(g), at_zero(T), at_zero(L)
    acceleration0 = at_zero(acceleration)
    bracket0 = at_zero(bracket)
    D2xi0 = at_zero(D2xi)
    Rxi0 = at_zero(Rxi)
    jacobi0 = sp.simplify(D2xi0 + Rxi0)
    n0 = at_zero(nvec)
    Kn0 = sp.simplify((n0.T * g0 * (Rxi0 / L0))[0])

    wrong_u = sp.Matrix([1, 0, 0, 0])
    wrong_D2 = at_zero(covD(wrong_u, covD(wrong_u, xi)))

    gates = {
        "lorentz_regular": T0 > 0 and g0.det() < 0,
        "terminal_rho_equals_L": sp.simplify(rho_from_terminal - L) == 0,
        "T0_frozen": T0 == sp.Rational(1, 3),
        "rho0_frozen": at_zero(rho_from_terminal) == 1,
        "rho_dot0_frozen": at_zero(rho_dot) == sp.Rational(3, 10),
        "rho_ddot0_frozen": at_zero(rho_ddot) == sp.Rational(93, 100),
        "connecting_bracket_zero": all(q == 0 for q in bracket0),
        "geodesic_congruence": all(q == 0 for q in acceleration0),
        "connecting_bracket_zero_all_t": all(sp.simplify(q) == 0 for q in bracket),
        "geodesic_congruence_all_t": all(sp.simplify(q) == 0 for q in acceleration),
        "jacobi_residual_zero_all_t": all(sp.simplify(q) == 0 for q in D2xi + Rxi),
        "direct_second_equals_rho_ddot_n": all(
            sp.simplify(q) == 0 for q in D2xi0 - sp.Rational(93, 100) * n0
        ),
        "curvature_Kn_frozen": Kn0 == -sp.Rational(93, 100),
        "jacobi_residual_zero": all(q == 0 for q in jacobi0),
        "mutation_wrong_curvature_sign_rejected": any(
            sp.simplify(q) != 0 for q in D2xi0 - Rxi0
        ),
        "mutation_coordinate_time_used_as_unit_clock_rejected": any(
            sp.simplify(q) != 0 for q in wrong_D2 - D2xi0
        ),
    }
    gates = {name: bool(value) for name, value in gates.items()}

    result = {
        "schema": "udt.g151.exact_warped_witness.v1",
        "status": "PASS" if all(gates.values()) else "FAIL",
        "marked_point": {
            "T": str(T0),
            "L": str(L0),
            "rho": str(at_zero(rho_from_terminal)),
            "rho_dot": str(at_zero(rho_dot)),
            "rho_ddot": str(at_zero(rho_ddot)),
            "acceleration": [str(q) for q in acceleration0],
            "bracket": [str(q) for q in bracket0],
            "D_u2_xi": [str(q) for q in D2xi0],
            "R_xi_u_u": [str(q) for q in Rxi0],
            "K_n": str(Kn0),
            "jacobi_residual": [str(q) for q in jacobi0],
        },
        "gates": gates,
        "scope": "exact coordinate sign/type witness; not a selected physical history",
    }
    (HERE / "WITNESS_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
