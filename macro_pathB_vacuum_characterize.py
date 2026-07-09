#!/usr/bin/env python3
"""
Path B vacuum characterization: free D_A + EH + R1 kinetic, NO matter.
Parents: macro_phase3_pathB_freeDA_EH_results.md, Path A baseline.

L ~ D_A^2 R + (Z/2) D_A^2 (phi')^2
"""
from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

Zsym = sp.symbols("Z", positive=True)
r = sp.symbols("r", positive=True)
phi = sp.Function("phi")
DA = sp.Function("D_A")
ph = phi(r)
D = DA(r)
php = sp.diff(ph, r)
phpp = sp.diff(ph, r, 2)
Dp = sp.diff(D, r)
Dpp = sp.diff(D, r, 2)

R = (
    2
    * sp.exp(-2 * ph)
    / D**2
    * (
        -2 * D**2 * php**2
        + D**2 * phpp
        + 4 * D * Dp * php
        - 2 * D * Dpp
        + sp.exp(2 * ph)
        - Dp**2
    )
)
L = sp.simplify(D**2 * R + (Zsym / 2) * D**2 * php**2)


def el(L, f):
    fp = sp.diff(f, r)
    fpp = sp.diff(f, r, 2)
    return sp.simplify(
        sp.diff(L, f) - sp.diff(sp.diff(L, fp), r) + sp.diff(sp.diff(L, fpp), r, 2)
    )


el_phi = el(L, ph)
el_D = el(L, D)

print("=" * 70)
print("PATH B VACUUM — CAS structure")
print("=" * 70)
print("EL_phi =", el_phi)
print("EL_D   =", el_D)

# Rewrite EL_phi as divergence form if possible
# From earlier: EL_phi = -Z D^2 phi'' - 2 Z D D' phi' + 4 D e^{-2phi} D''
# = - d/dr(Z D^2 phi') + 4 D e^{-2phi} D''
flux = Zsym * D**2 * php
print("\nEL_phi + d/dr(Z D^2 phi') - 4 D e^{-2phi} D'' =",
      sp.simplify(el_phi + sp.diff(flux, r) - 4 * D * sp.exp(-2 * ph) * Dpp))

# Special solutions catalog
print("\n--- Special solutions ---")

# S1: D=r, Coulomb phi = c0 - q/r  (Path A) — check EL_D residual
q, c0 = sp.symbols("q c0", real=True)
phi_c = c0 - q / r
# substitute D=r, phi=phi_c into el_D and el_phi
subs_pathA = {
    D: r,
    Dp: 1,
    Dpp: 0,
    ph: phi_c,
    php: sp.diff(phi_c, r),
    phpp: sp.diff(phi_c, r, 2),
}
# Use replace on expressions carefully
el_phi_A = sp.simplify(
    el_phi.subs(php, sp.diff(phi_c, r))
    .subs(phpp, sp.diff(phi_c, r, 2))
    .subs(ph, phi_c)
    .subs(D, r)
    .subs(Dp, 1)
    .subs(Dpp, 0)
    .doit()
)
el_D_A = sp.simplify(
    el_D.subs(php, sp.diff(phi_c, r))
    .subs(phpp, sp.diff(phi_c, r, 2))
    .subs(ph, phi_c)
    .subs(D, r)
    .subs(Dp, 1)
    .subs(Dpp, 0)
    .doit()
)
print("S1 Path A (D=r, phi=c0-q/r):")
print("  EL_phi residual:", el_phi_A)
print("  EL_D   residual:", el_D_A)
print("  => Path A sits in EL_phi; EL_D residual is constraint (generally nonzero unless q=0)")

# For q=0, phi=const, D=r
el_D_flat = sp.simplify(el_D_A.subs(q, 0))
print("  EL_D at q=0:", el_D_flat)

# S2: phi=const, D=a+b*r
a, b = sp.symbols("a b", real=True)
# EL with php=phpp=0: need D''=0
print("\nS2 phi=const, D''=0 (D=a+b r): both EL require D''=0 — family OK")

# S3: try D^2 = alpha + beta r^2 or similar — leave numeric

print("\n" + "=" * 70)
print("PATH B VACUUM — numeric IVP observe")
print("=" * 70)

# First-order system: y = [D, Dp, phi, pi] with pi = Z D^2 phi'
# From EL_phi: d/dr(Z D^2 phi') = 4 D e^{-2phi} D''
# That still has D'' on RHS — coupled.
# Use y = [D, S, phi, Q] with S=D', Q=phi'
# EL_phi: -Z D^2 phi'' - 2 Z D S phi' + 4 D e^{-2phi} S' = 0
# => 4 D e^{-2phi} S' - Z D^2 Q' - 2 Z D S Q = 0
# EL_D: e^{-2phi}( Z D e^{2phi} Q^2 - 8 D Q^2 + 4 D Q' + 8 S Q - 4 S' ) = 0
# => Z D e^{2phi} Q^2 - 8 D Q^2 + 4 D Q' + 8 S Q - 4 S' = 0

# Solve linear system for (S', Q'):
# (eq1)  4 D e^{-2phi} S'  -  Z D^2 Q'  =  2 Z D S Q
# (eq2) -4 S'  +  4 D Q'  =  -Z D e^{2phi} Q^2 + 8 D Q^2 - 8 S Q
# Simplify eq2: -S' + D Q' = (-Z D e^{2phi}/4 + 2 D) Q^2 - 2 S Q


def rhs_factory(Z=1.0):
    def f(r, y):
        D, S, phi, Q = y
        # protect
        if D <= 1e-12:
            D = 1e-12
        e2 = np.exp(np.clip(2.0 * phi, -40, 40))
        em2 = np.exp(np.clip(-2.0 * phi, -40, 40))
        # Matrix: [ 4 D em2 ,  -Z D^2 ] [S'] = [ 2 Z D S Q ]
        #         [ -4      ,   4 D   ] [Q']   [ -Z D e2 Q^2 + 8 D Q^2 - 8 S Q ]
        A11 = 4.0 * D * em2
        A12 = -Z * D * D
        A21 = -4.0
        A22 = 4.0 * D
        b1 = 2.0 * Z * D * S * Q
        b2 = -Z * D * e2 * Q * Q + 8.0 * D * Q * Q - 8.0 * S * Q
        det = A11 * A22 - A12 * A21
        if abs(det) < 1e-30:
            return [S, 0.0, Q, 0.0]
        Sp = (b1 * A22 - A12 * b2) / det
        Qp = (A11 * b2 - b1 * A21) / det
        if not np.isfinite(Sp):
            Sp = 0.0
        if not np.isfinite(Qp):
            Qp = 0.0
        Sp = float(np.clip(Sp, -1e6, 1e6))
        Qp = float(np.clip(Qp, -1e6, 1e6))
        return [S, Sp, Q, Qp]

    return f


def integrate(y0, r0, r_max, Z=1.0):
    return solve_ivp(
        rhs_factory(Z),
        (r0, r_max),
        y0,
        method="RK45",
        rtol=1e-7,
        atol=1e-9,
        max_step=0.05,
        dense_output=False,
    )


def report(label, sol, r0):
    if sol is None or len(sol.t) < 2:
        print(f"  [{label}] empty")
        return None
    r = sol.t
    D, S, phi, Q = sol.y
    out = {
        "label": label,
        "ok": bool(sol.success),
        "msg": sol.message,
        "r_end": float(r[-1]),
        "D0": float(D[0]),
        "Dend": float(D[-1]),
        "Dmin": float(np.min(D)),
        "S_end": float(S[-1]),
        "phi0": float(phi[0]),
        "phi_end": float(phi[-1]),
        "dphi": float(phi[-1] - phi[0]),
        "Q0": float(Q[0]),
        "Qmax": float(np.nanmax(np.abs(Q))),
        "finite": bool(np.all(np.isfinite(sol.y))),
    }
    print(
        f"  [{label}] ok={out['ok']} r→{out['r_end']:.4g} "
        f"D:{out['D0']:.4g}→{out['Dend']:.4g} "
        f"Δφ={out['dphi']:+.4f} |Q|max={out['Qmax']:.3e} fin={out['finite']}"
    )
    return out


rows = []

print("\n[N1] Path A seed: D=r, phi=c0-q/r near r0 — expect EL_D drift")
for q in (0.0, 0.1, 0.5, 1.0):
    r0 = 0.5
    # D=r0, S=1, phi=-q/r0 (c0=0), Q=q/r0^2
    y0 = [r0, 1.0, -q / r0, q / (r0**2)]
    sol = integrate(y0, r0, 5.0)
    rows.append(report(f"PathA-seed q={q:g} r0=0.5", sol, r0))

print("\n[N2] Regular-ish core seed: D=Dc, S=0, phi=0, Q=0 (flat vacuum core)")
for Dc in (0.5, 1.0, 2.0):
    sol = integrate([Dc, 0.0, 0.0, 0.0], 1e-3, 10.0)
    rows.append(report(f"flat-core Dc={Dc:g}", sol, 1e-3))

print("\n[N3] Linear D seed: D=a+b r at r0, phi=0, Q=0")
for a, b in [(1.0, 0.0), (0.0, 1.0), (1.0, 0.5), (0.5, 1.0)]:
    r0 = 0.5
    D0 = a + b * r0
    sol = integrate([D0, b, 0.0, 0.0], r0, 10.0)
    rows.append(report(f"linear a={a:g} b={b:g}", sol, r0))

print("\n[N4] Small kick Q at flat core (try redshift seed)")
for Q0 in (0.01, 0.1, 0.5, 1.0):
    sol = integrate([1.0, 0.0, 0.0, Q0], 0.2, 8.0)
    rows.append(report(f"core Q0={Q0:g}", sol, 0.2))

print("\n[N5] Small kick S at flat core")
for S0 in (0.01, 0.1, 0.5, 1.0):
    sol = integrate([1.0, S0, 0.0, 0.0], 0.2, 8.0)
    rows.append(report(f"core S0={S0:g}", sol, 0.2))

print("\n[N6] Combined mild kick S and Q")
for S0, Q0 in [(0.1, 0.1), (0.5, 0.1), (0.1, 0.5), (0.5, 0.5)]:
    sol = integrate([1.0, S0, 0.0, Q0], 0.2, 8.0)
    rows.append(report(f"kick S={S0:g} Q={Q0:g}", sol, 0.2))

# Residual check on a successful nontrivial trajectory
print("\n[N7] Residual spot-check on best growing-phi run")
ok = [x for x in rows if x and x.get("ok") and x.get("finite") and abs(x.get("dphi", 0)) > 0.05]
if ok:
    best = max(ok, key=lambda x: abs(x["dphi"]))
    print(f"  re-integrate {best['label']} for residual...")
    # parse not easy — re-run kick S=0.5 Q=0.5
    sol = integrate([1.0, 0.5, 0.0, 0.5], 0.2, 5.0)
    if sol.success:
        r = sol.t
        D, S, phi, Q = sol.y
        # numerical D'', phi''
        Sp = np.gradient(S, r)
        Qp = np.gradient(Q, r)
        Z = 1.0
        # EL_phi residual: -Z D^2 Q' - 2 Z D S Q + 4 D e^{-2phi} S'
        elp = -Z * D**2 * Qp - 2 * Z * D * S * Q + 4 * D * np.exp(-2 * phi) * Sp
        # EL_D residual interior
        eld = (
            Z * D * np.exp(2 * phi) * Q**2
            - 8 * D * Q**2
            + 4 * D * Qp
            + 8 * S * Q
            - 4 * Sp
        ) * np.exp(-2 * phi)
        print(
            f"  median|EL_phi|={np.median(np.abs(elp[2:-2])):.3e} "
            f"median|EL_D raw|={np.median(np.abs(eld[2:-2])):.3e}"
        )

# Summary classification
print("\n" + "=" * 70)
print("CLASSIFICATION")
print("=" * 70)
okf = [x for x in rows if x and x.get("ok") and x.get("finite")]
print(f"  OK finite: {len(okf)} / {len([x for x in rows if x])}")
dphi = [x["dphi"] for x in okf]
print(f"  Δφ range among OK: [{min(dphi):+.4f}, {max(dphi):+.4f}]")
nontriv = [x for x in okf if abs(x["dphi"]) > 0.05]
print(f"  |Δφ|>0.05: {len(nontriv)}")
for x in sorted(nontriv, key=lambda z: -abs(z["dphi"]))[:12]:
    print(
        f"    {x['label']}: Δφ={x['dphi']:+.4f} D:{x['D0']:.3g}→{x['Dend']:.3g} "
        f"r_end={x['r_end']:.3g}"
    )
collapse = [x for x in rows if x and x.get("Dmin", 1) < 1e-3]
print(f"  D near-collapse (Dmin<1e-3): {len(collapse)}")
print("DONE")
