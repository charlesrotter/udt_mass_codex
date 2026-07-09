#!/usr/bin/env python3
"""
GR mine: EH static SSS free (ν,λ), then reciprocity ν+λ=0.

Re-run: python3 simple_metric_mine_EH_constraint.py
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent


def main():
    t, r, th, ph = sp.symbols("t r theta phi", positive=True)
    nu = sp.Function("nu")
    lam = sp.Function("lam")
    phi = sp.Function("phi")
    n, l = nu(r), lam(r)

    print("=" * 70)
    print("Mine: EH free (ν,λ) + reciprocity constraint")
    print("=" * 70)

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
    Lfull = sp.simplify(sp.exp(n + l) * r**2 * Rscal)
    print("\n[1] L_EH ~", Lfull)

    def el(Lexpr, f):
        f = f(r)
        fp = sp.diff(f, r)
        fpp = sp.diff(f, r, 2)
        L = Lexpr.doit()
        return sp.simplify(
            sp.diff(L, f)
            - sp.diff(sp.diff(L, fp), r)
            + sp.diff(sp.diff(L, fpp), r, 2)
        )

    EL_nu = el(Lfull, nu)
    EL_lam = el(Lfull, lam)
    print("\n[2] Free EL")
    print("  EL_ν =", EL_nu)
    print("  EL_λ =", EL_lam)

    sub = {nu(r): -phi(r), lam(r): phi(r)}
    L_rec = sp.simplify(Lfull.subs(sub).doit())
    EL_phi = el(L_rec, phi)
    print("\n[3] Substitute reciprocal into L, vary φ")
    print("  EL_φ =", EL_phi)
    print("  empty?", sp.simplify(EL_phi) == 0)

    EL_nu_c = sp.simplify(EL_nu.subs(lam(r), -nu(r)).doit())
    EL_lam_c = sp.simplify(EL_lam.subs(lam(r), -nu(r)).doit())
    print("\n[4] Restrict ELs to λ=-ν")
    print("  EL_ν =", EL_nu_c)
    print("  EL_λ =", EL_lam_c)
    print("  difference =", sp.simplify(EL_nu_c - EL_lam_c))

    A = sp.Function("A")
    # A = e^{2ν}, vacuum A + r A' = 1
    sol = sp.dsolve(sp.Eq(A(r) + r * A(r).diff(r), 1), A(r))
    print("\n[5] EL_ν=0 on constraint ⇒", sol)

    out = {
        "EL_nu": str(EL_nu),
        "EL_lam": str(EL_lam),
        "EL_phi_after_substitute": str(EL_phi),
        "substitute_empty": bool(sp.simplify(EL_phi) == 0),
        "EL_equal_on_constraint": bool(sp.simplify(EL_nu_c - EL_lam_c) == 0),
        "vacuum_A": str(sol),
        "fallout": [
            "free EH: nontrivial EL_ν, EL_λ",
            "substitute reciprocity into L then vary φ: empty EL",
            "restrict ELs to ν+λ=0: EL_ν=EL_λ, set 0 ⇒ A=1+C/r",
            "E-primary = constrained Einstein eqs, not substituted-φ EH",
            "not equal to R1 Coulomb vacuum",
        ],
        "verdict": (
            "Order of operations: constrain equations ≠ substitute into action; "
            "only the former yields Schw vacuum on reciprocal family."
        ),
    }
    print("\n" + out["verdict"])
    path = ROOT / "simple_metric_mine_EH_constraint_out.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {path.name}")
    print("DONE")


if __name__ == "__main__":
    main()
