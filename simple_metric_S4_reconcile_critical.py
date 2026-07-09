#!/usr/bin/env python3
"""
S4 reconcile: Einstein continuum vs R1+dust EL + critical/closure mass.

Load-bearing CAS:
  - Full curvature Einstein tensor on simple metric ds²=-A dt² + A^{-1} dr² + r² dΩ²
  - Scar: old S3 G^r_r formula was wrong → p_r=-ρ identity
  - Critical M=X/2 closes A(X)=0; does not glue R1 EL to ceiling

Re-run: python3 simple_metric_S4_reconcile_critical.py
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
t, r, th, ph = sp.symbols("t r theta phi", positive=True)
X, Z = sp.symbols("X Z", positive=True)
vars4 = [t, r, th, ph]


def einstein_mixed_general():
    """G^μ_ν for general A(r) on simple metric — full curvature."""
    A = sp.Function("A")(r)
    gdd = sp.diag(-A, 1 / A, r**2, r**2 * sp.sin(th) ** 2)
    guu = sp.diag(-1 / A, A, 1 / r**2, 1 / (r**2 * sp.sin(th) ** 2))
    Gam = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for s in range(4):
        for i in range(4):
            for j in range(4):
                tot = 0
                for k in range(4):
                    tot += guu[s, k] * (
                        sp.diff(gdd[k, i], vars4[j])
                        + sp.diff(gdd[k, j], vars4[i])
                        - sp.diff(gdd[i, j], vars4[k])
                    )
                Gam[s][i][j] = sp.simplify(tot / 2)
    Ric = sp.zeros(4)
    for sig in range(4):
        for nu in range(4):
            tot = 0
            for rho in range(4):
                tot += sp.diff(Gam[rho][nu][sig], vars4[rho])
                tot -= sp.diff(Gam[rho][rho][sig], vars4[nu])
                for lam in range(4):
                    tot += Gam[rho][rho][lam] * Gam[lam][nu][sig]
                    tot -= Gam[rho][nu][lam] * Gam[lam][rho][sig]
            Ric[sig, nu] = sp.simplify(sp.trigsimp(tot))
    Rscal = sp.simplify(
        sum(guu[i, j] * Ric[i, j] for i in range(4) for j in range(4))
    )
    Gdd = sp.zeros(4)
    for i in range(4):
        for j in range(4):
            Gdd[i, j] = sp.simplify(Ric[i, j] - sp.Rational(1, 2) * gdd[i, j] * Rscal)
    Gmix = sp.zeros(4)
    for i in range(4):
        for j in range(4):
            Gmix[i, j] = sp.simplify(
                sum(guu[i, k] * Gdd[k, j] for k in range(4))
            )
    return Gmix


def main():
    out: dict = {}
    print("=" * 60)
    print("S4 reconcile — critical mass + G^r_r scar + R1 residual")
    print("=" * 60)

    # --- Full G ---
    print("\n[1] Full curvature Einstein (general A)")
    Gmix = einstein_mixed_general()
    A = sp.Function("A")(r)
    Gt, Gr, Gth = Gmix[0, 0], Gmix[1, 1], Gmix[2, 2]
    print("  G^t_t =", sp.simplify(Gt))
    print("  G^r_r =", sp.simplify(Gr))
    print("  G^θ_θ =", sp.simplify(Gth))
    print("  G^t_t == G^r_r ?", sp.simplify(Gt - Gr) == 0)

    rho = sp.simplify(-Gt / (8 * sp.pi))
    pr = sp.simplify(Gr / (8 * sp.pi))
    pt = sp.simplify(Gth / (8 * sp.pi))
    print("  ρ =", rho)
    print("  p_r =", pr)
    print("  p_t =", pt)
    print("  p_r + ρ =", sp.simplify(pr + rho), "  (must be 0: identity)")
    out["pr_plus_rho"] = str(sp.simplify(pr + rho))
    out["identity_pr_eq_minus_rho"] = sp.simplify(pr + rho) == 0

    # vacuum check Schw
    rs = sp.symbols("rs", positive=True)
    Gschw = [sp.simplify(Gmix[i, i].subs(A, 1 - rs / r)) for i in range(4)]
    print("\n[2] Vacuum Schw check G^μ_μ:", Gschw)
    out["schw_vacuum_G"] = [str(g) for g in Gschw]

    # old vs new Grr
    old_Grr = (-A + r * sp.diff(A, r) + 1) / r**2
    print("\n[3] Scar: old S3 G^r_r - correct =", sp.simplify(old_Grr - Gr))

    # p_r=0 true solution
    print("\n[4] True p_r=0 ⇒ G^r_r=0")
    ode = sp.Eq(sp.simplify(Gr) * r**2, 0)
    sol = sp.dsolve(sp.Eq(r * A.diff(r) + A - 1, 0), A)
    print("  ", sol)
    out["pr0_solution"] = str(sol)

    # ceiling stresses CORRECTED
    print("\n[5] Ceiling A=1-r/X corrected stresses")
    Ac = 1 - r / X
    rho_c = sp.simplify(rho.subs(A, Ac))
    pr_c = sp.simplify(pr.subs(A, Ac))
    pt_c = sp.simplify(pt.subs(A, Ac))
    m_c = sp.simplify(r * (1 - Ac) / 2)
    print("  ρ =", rho_c)
    print("  p_r =", pr_c, "  (= -ρ, not 0)")
    print("  p_⊥ =", pt_c)
    print("  m(r) =", m_c, "  M_crit =", X / 2)
    out["ceiling"] = {
        "rho": str(rho_c),
        "p_r": str(pr_c),
        "p_perp": str(pt_c),
        "M_crit": "X/2",
    }

    # R1 residual
    print("\n[6] R1 compensated residual on ceiling")
    phi = -sp.Rational(1, 2) * sp.log(Ac)
    LHS = sp.simplify(sp.diff(r**2 * sp.diff(phi, r), r))
    RHS = sp.simplify(2 * rho_c * r**2 * Ac)
    ratio = sp.simplify(LHS / RHS)
    print("  ratio LHS/RHS =", ratio)
    print("  r-dependent?", sp.diff(ratio, r) != 0)
    out["residual_ratio"] = str(ratio)
    out["critical_mass_closes_geometry"] = True
    out["critical_mass_closes_EL_mismatch"] = False

    samples = {}
    for f in [
        sp.Rational(1, 10),
        sp.Rational(1, 4),
        sp.Rational(1, 2),
        sp.Rational(3, 4),
        sp.Rational(9, 10),
    ]:
        val = sp.simplify(ratio.subs(r, f * X).subs(X, 1))
        samples[str(float(f))] = str(val)
        print(f"  r={f}X → {val} ≈ {float(val):.4g}")
    out["ratio_samples"] = samples

    # mean critical density
    rho_mean = sp.simplify((X / 2) / (sp.Rational(4, 3) * sp.pi * X**3))
    print("\n[7] Critical closure numbers")
    print("  M_crit = X/2")
    print("  ρ_mean =", rho_mean)
    out["rho_mean"] = str(rho_mean)

    out["verdict"] = (
        "Critical M=X/2 closes geometric sphere. "
        "Does not glue R1 EL to Einstein. "
        "S3 p_r=0 selection withdrawn: simple metric has p_r=-ρ always; "
        "ceiling has p_r=-ρ, p_perp=-ρ/2."
    )
    print("\n" + out["verdict"])

    path = ROOT / "simple_metric_S4_reconcile_critical_out.json"
    path.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {path.name}")
    print("DONE")
    return out


if __name__ == "__main__":
    main()
