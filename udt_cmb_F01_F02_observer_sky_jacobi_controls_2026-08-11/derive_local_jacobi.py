#!/usr/bin/env python3
"""Exact local screen-Jacobi coefficient for the preregistered F01/F02 query.

This production implementation constructs the metric, Levi-Civita connection, and Riemann
curvature directly in coordinates before imposing the equatorial observer query.  It does not
import any repository physics implementation.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent


def build_result() -> dict:
    t, r, th, ps = sp.symbols("t r theta psi", real=True)
    coords = (t, r, th, ps)
    A = sp.Function("A")(r)
    h = sp.Function("h")(r)
    s = sp.sin(th)

    g = sp.zeros(4)
    g[0, 0] = -A
    g[1, 1] = 1 / A
    g[2, 2] = r**2
    g[3, 3] = r**2 * s**2
    g[0, 3] = g[3, 0] = h * s**2
    gi = sp.simplify(g.inv())

    Gamma = [[[sp.S.Zero for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                Gamma[rho][mu][nu] = sp.factor(
                    sp.Rational(1, 2)
                    * sum(
                        gi[rho, lam]
                        * (
                            sp.diff(g[lam, nu], coords[mu])
                            + sp.diff(g[lam, mu], coords[nu])
                            - sp.diff(g[mu, nu], coords[lam])
                        )
                        for lam in range(4)
                    )
                )

    # R^rho_{ sigma mu nu }, with R(X,Y)Z = X^mu Y^nu Z^sigma R^rho_{sigma mu nu}.
    def riemann(rho: int, sig: int, mu: int, nu: int) -> sp.Expr:
        return sp.factor(
            sp.diff(Gamma[rho][nu][sig], coords[mu])
            - sp.diff(Gamma[rho][mu][sig], coords[nu])
            + sum(
                Gamma[rho][mu][lam] * Gamma[lam][nu][sig]
                - Gamma[rho][nu][lam] * Gamma[lam][mu][sig]
                for lam in range(4)
            )
        )

    D = A * r**2 + h**2 * s**2
    u = sp.Matrix([1 / sp.sqrt(A), 0, 0, 0])
    n = sp.Matrix([0, sp.sqrt(A), 0, 0])
    e_th = sp.Matrix([0, 0, 1 / r, 0])
    e_ps = sp.Matrix(
        [
            h * s / (sp.sqrt(A) * sp.sqrt(D)),
            0,
            0,
            sp.sqrt(A) / (s * sp.sqrt(D)),
        ]
    )
    k = u + n
    frame = (u, n, e_th, e_ps)

    gram = sp.Matrix(
        [[sp.factor((va.T * g * vb)[0]) for vb in frame] for va in frame]
    )
    null_norm = sp.factor((k.T * g * k)[0])

    screen = (e_th, e_ps)
    tidal = sp.zeros(2)
    for aa, ea in enumerate(screen):
        ea_cov = g * ea
        for bb, eb in enumerate(screen):
            value = sp.S.Zero
            for rho in range(4):
                if ea_cov[rho] == 0:
                    continue
                for sig in range(4):
                    if k[sig] == 0:
                        continue
                    for mu in range(4):
                        if eb[mu] == 0:
                            continue
                        for nu in range(4):
                            if k[nu] == 0:
                                continue
                            value += (
                                ea_cov[rho]
                                * riemann(rho, sig, mu, nu)
                                * eb[mu]
                                * k[nu]
                                * k[sig]
                            )
            tidal[aa, bb] = sp.factor(value.subs(th, sp.pi / 2))

    # Replace functions and jets by compact algebraic symbols after all coordinate derivatives.
    A0, A1, A2, h0, h1, h2 = sp.symbols("A0 A1 A2 h0 h1 h2", real=True)
    jet_subs = {
        A: A0,
        sp.diff(A, r): A1,
        sp.diff(A, (r, 2)): A2,
        h: h0,
        sp.diff(h, r): h1,
        sp.diff(h, (r, 2)): h2,
    }
    tidal_jets = sp.Matrix(
        [[sp.factor(tidal[i, j].subs(jet_subs)) for j in range(2)] for i in range(2)]
    )
    round_tidal = sp.Matrix(
        [
            [
                sp.factor(
                    tidal_jets[i, j].subs({h0: 0, h1: 0, h2: 0})
                )
                for j in range(2)
            ]
            for i in range(2)
        ]
    )
    trace = sp.factor(sp.trace(tidal_jets))
    shear_plus = sp.factor((tidal_jets[0, 0] - tidal_jets[1, 1]) / 2)
    shear_cross = sp.factor((tidal_jets[0, 1] + tidal_jets[1, 0]) / 2)
    antisymmetric = sp.factor((tidal_jets[0, 1] - tidal_jets[1, 0]) / 2)
    eps = sp.symbols("epsilon", real=True)
    weak_series = sp.series(
        tidal_jets[1, 1].subs({h0: eps * h0, h1: eps * h1, h2: eps * h2}),
        eps,
        0,
        5,
    ).removeO()
    weak_quadratic = sp.factor(sp.expand(weak_series).coeff(eps, 2))
    weak_quartic = sp.factor(sp.expand(weak_series).coeff(eps, 4))
    mixing_polynomial = sp.factor(
        tidal_jets[1, 1] * 4 * A0 * (A0 * r**2 + h0**2) ** 2 / h0
    )

    def sstr(expr: sp.Expr) -> str:
        return sp.sstr(expr)

    result = {
        "curvature_convention": "R(X,Y)Z=nabla_X_nabla_Y_Z-nabla_Y_nabla_X_Z-nabla_[X,Y]_Z",
        "query": {
            "event": "(t0,r0,pi/2,psi0)",
            "observer": "A^(-1/2) partial_t",
            "radial_direction": "A^(1/2) partial_r",
            "generator": "k=u+n",
            "screen_theta": "r^(-1) partial_theta",
            "screen_psi": "h/(sqrt(A)*sqrt(D)) partial_t + sqrt(A)/sqrt(D) partial_psi at theta=pi/2",
        },
        "frame_gram_before_equator": [[sstr(x) for x in row] for row in gram.tolist()],
        "generator_norm": sstr(null_norm),
        "F02_tidal_matrix_equator": [[sstr(x) for x in row] for row in tidal_jets.tolist()],
        "F01_induced_limit": [[sstr(x) for x in row] for row in round_tidal.tolist()],
        "trace": sstr(trace),
        "shear_plus": sstr(shear_plus),
        "shear_cross": sstr(shear_cross),
        "antisymmetric": sstr(antisymmetric),
        "mixing_polynomial_N": sstr(mixing_polynomial),
        "weak_mixing_linear": "0",
        "weak_mixing_quadratic": sstr(weak_quadratic),
        "weak_mixing_cubic": "0",
        "weak_mixing_quartic": sstr(weak_quartic),
        "special_subloci": {
            "h_at_event_zero": "T=0 at cubic Jacobi order even when h1 or h2 is nonzero",
            "nonzero_h_cancellation": "N=0 is a codimension-one local-jet cancellation condition",
            "generic": "h0*N != 0 gives one-axis cubic screen distortion",
        },
        "local_Jacobi_series": "D(s)=s I-s^3 T/6+O(s^4)",
        "primary_landing": "LOCAL_SKY_MAP_GEOMETRY_DISTINGUISHES_F01_F02_WITH_PROFILE_REMAINDER",
        "maximum_conclusion": "local two-control screen-Jacobi classification only; no finite CMB angular map, TT power, screen selection, source/population, local signal law, FD2 restart, action, bootstrap, Xmax value, or dynamics",
    }
    return result


def main() -> None:
    result = build_result()
    output = ROOT / "DERIVATION_RESULT.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
