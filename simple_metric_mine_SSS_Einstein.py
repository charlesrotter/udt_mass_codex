#!/usr/bin/env python3
"""
GR corpus mine: static SSS Einstein → restrict to UDT reciprocal metric.

Re-run: python3 simple_metric_mine_SSS_Einstein.py
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def einstein_static_sss():
    t, r, th, ph = sp.symbols("t r theta phi", positive=True)
    nu = sp.Function("nu")
    lam = sp.Function("lam")
    n, l = nu(r), lam(r)
    gdd = sp.diag(
        -sp.exp(2 * n), sp.exp(2 * l), r**2, r**2 * sp.sin(th) ** 2
    )
    coords = [t, r, th, ph]
    guu = gdd.inv()
    Gam = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for s in range(4):
        for i in range(4):
            for j in range(4):
                tot = 0
                for k in range(4):
                    tot += guu[s, k] * (
                        sp.diff(gdd[k, i], coords[j])
                        + sp.diff(gdd[k, j], coords[i])
                        - sp.diff(gdd[i, j], coords[k])
                    )
                Gam[s][i][j] = sp.simplify(tot / 2)
    Ric = sp.zeros(4)
    for sig in range(4):
        for nu_i in range(4):
            tot = 0
            for rho in range(4):
                tot += sp.diff(Gam[rho][nu_i][sig], coords[rho])
                tot -= sp.diff(Gam[rho][rho][sig], coords[nu_i])
                for la in range(4):
                    tot += Gam[rho][rho][la] * Gam[la][nu_i][sig]
                    tot -= Gam[rho][nu_i][la] * Gam[la][rho][sig]
            Ric[sig, nu_i] = sp.simplify(sp.trigsimp(tot))
    Rscal = sp.simplify(
        sum(guu[i, j] * Ric[i, j] for i in range(4) for j in range(4))
    )
    Gmix = sp.zeros(4)
    for i in range(4):
        for j in range(4):
            Gdd_ij = sp.simplify(
                Ric[i, j] - sp.Rational(1, 2) * gdd[i, j] * Rscal
            )
            Gmix[i, j] = sp.simplify(
                sum(guu[i, k] * (Ric[k, j] - sp.Rational(1, 2) * gdd[k, j] * Rscal) for k in range(4))
            )
    return Gmix, nu, lam, r


def main():
    print("=" * 70)
    print("Mine: SSS Einstein → UDT reciprocal")
    print("=" * 70)
    Gmix, nu, lam, r = einstein_static_sss()
    out = {"fallout": []}

    print("\n[1] General SSS diagonal G")
    for i, name in enumerate(["t", "r", "th", "ph"]):
        print(f"  G^{name}_{name} =", sp.simplify(Gmix[i, i]))
    out["G_tt_general"] = str(sp.simplify(Gmix[0, 0]))
    out["G_rr_general"] = str(sp.simplify(Gmix[1, 1]))

    phi = sp.Function("phi")
    sub = {nu(r): -phi(r), lam(r): phi(r)}
    print("\n[2] Reciprocal ν=-φ, λ=+φ")
    Gt = sp.simplify(Gmix[0, 0].subs(sub).doit())
    Gr = sp.simplify(Gmix[1, 1].subs(sub).doit())
    Gth = sp.simplify(Gmix[2, 2].subs(sub).doit())
    print("  G^t_t =", Gt)
    print("  G^r_r =", Gr)
    print("  equal?", sp.simplify(Gt - Gr) == 0)
    rho = sp.simplify(-Gt / (8 * sp.pi))
    pr = sp.simplify(Gr / (8 * sp.pi))
    print("  p_r + ρ =", sp.simplify(pr + rho))
    out["pr_plus_rho"] = str(sp.simplify(pr + rho))
    out["identity_pr_eq_minus_rho"] = sp.simplify(pr + rho) == 0
    out["fallout"].append("reciprocal ⇒ G^t_t=G^r_r ⇒ p_r=-ρ")

    A = sp.Function("A")
    ode = sp.Eq(1 - A(r) - r * A(r).diff(r), 0)
    sol = sp.dsolve(ode, A(r))
    print("\n[3] Einstein vacuum under reciprocal:", sol)
    out["vacuum_A"] = str(sol)
    out["fallout"].append("vacuum A=1+C/r (Schw family), not Coulomb")

    # Coulomb contrast
    a, q = sp.symbols("a q")
    phic = a - q / r
    Ac = sp.exp(-2 * phic)
    rho_c = sp.simplify((1 - Ac - r * sp.diff(Ac, r)) / (8 * sp.pi * r**2))
    print("  Coulomb ρ_E =", rho_c)
    out["coulomb_rho_E"] = str(rho_c)

    print("\n[4] Hydrostatic reduction with p_r=-ρ")
    print("  ρ' + 2(ρ+p_t)/r = 0")
    out["hydro_reduced"] = "rho' + 2(rho+p_t)/r = 0"
    out["fallout"].append("hydrostatic → ρ'+2(ρ+p_t)/r=0")

    # ceiling check
    X = sp.symbols("X", positive=True)
    rho_ce = 1 / (4 * sp.pi * X * r)
    pt_ce = -rho_ce / 2
    res = sp.simplify(sp.diff(rho_ce, r) + 2 * (rho_ce + pt_ce) / r)
    print("  ceiling check residual:", res)
    out["ceiling_hydro_residual"] = str(res)

    out["verdict"] = (
        "Einstein+reciprocal ⇒ p_r=-ρ; vacuum Schw-type ≠ R1 Coulomb; "
        "package split is structural mine fallout."
    )
    print("\n" + out["verdict"])
    path = ROOT / "simple_metric_mine_SSS_Einstein_out.json"
    path.write_text(json.dumps(out, indent=2, default=str))
    print(f"Wrote {path.name}")
    print("DONE")


if __name__ == "__main__":
    main()
