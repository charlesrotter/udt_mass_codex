#!/usr/bin/env python3
"""
E-hard-4 probe: Is there a finite phi ceiling on Path B vacuum?
CAS Lyapunov/monotonicity attempts + dense numerical max-phi survey.
Parents: HE1 results, Path B vacuum characterize.
"""
from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

Z = 1.0

print("=" * 70)
print("PATH B φ CEILING — CAS + numeric")
print("=" * 70)

# --- CAS: rewrite system ---
r = sp.symbols("r", positive=True)
Zs = sp.symbols("Z", positive=True)
phi = sp.Function("phi")
D = sp.Function("D_A")
ph, php = phi(r), sp.diff(phi(r), r)
Dp = sp.diff(D(r), r)

# From EL_phi with vacuum: d/dr(Z D^2 php) = 4 D e^{-2phi} Dpp
# Hard to get global bound. Note S2 exact: php=0, Dpp=0, any phi=const.
print("\n[1] Exact solutions with arbitrary constant phi:")
print("    phi=const (any real), D''=0 (D=a+br) => EL satisfied.")
print("    => NO universal upper bound on the value of phi itself:")
print("    phi=100, D=r is an exact vacuum solution.")
print("    Ceiling, if any, is on DYNAMICS from regular data — not on admissible phi values.")

print("\n[2] What numerics saw as '~2' is seed/attractor relative to phi(0)=0 gauge.")
print("    Shift: if phi -> phi + c, Path B EL is NOT invariant (e^{±2phi} in EH).")
print("    So phi=0 at core is a physical normalization of the seed, not pure gauge.")
print("    Delta-phi = phi_infty - phi_core can still have structure.")

# For D=v*r (linear), EL_phi => (r^2 phi')'=0 => phi=c0-q/r
# EL_D residual forbids q≠0. So only q=0 on exact linear D.
print("\n[3] On exact linear D=vr: only phi=const allowed (q=0).")
print("    Redshifting trajectories must have non-linear D_A evolution.")

# Try: define u = e^{-phi}. As phi increases u decreases to 0.
# Numeric survey of max (phi - phi0) from varied seeds.

def rhs(r, y):
    D, S, phi, Q = y
    De = max(D, 1e-14)
    e2 = np.exp(np.clip(2 * phi, -40, 40))
    em2 = np.exp(np.clip(-2 * phi, -40, 40))
    A11 = 4 * De * em2
    A12 = -Z * De * De
    A21 = -4.0
    A22 = 4 * De
    b1 = 2 * Z * De * S * Q
    b2 = -Z * De * e2 * Q * Q + 8 * De * Q * Q - 8 * S * Q
    det = A11 * A22 - A12 * A21
    if abs(det) < 1e-30:
        return [S, 0.0, Q, 0.0]
    Sp = (b1 * A22 - A12 * b2) / det
    Qp = (A11 * b2 - b1 * A21) / det
    return [
        S,
        float(np.clip(Sp if np.isfinite(Sp) else 0, -1e6, 1e6)),
        Q,
        float(np.clip(Qp if np.isfinite(Qp) else 0, -1e6, 1e6)),
    ]


def run(y0, r0=0.2, r_max=20.0):
    sol = solve_ivp(rhs, (r0, r_max), y0, method="RK45", rtol=1e-7, atol=1e-9, max_step=0.05)
    if len(sol.t) < 2:
        return None
    phi = sol.y[2]
    return {
        "ok": sol.success,
        "phi0": float(phi[0]),
        "phi_max": float(np.nanmax(phi)),
        "phi_end": float(phi[-1]),
        "dphi": float(np.nanmax(phi) - phi[0]),
        "D_end": float(sol.y[0, -1]),
        "S_end": float(sol.y[1, -1]),
        "Q_end": float(sol.y[3, -1]),
        "r_end": float(sol.t[-1]),
    }


print("\n[4] Numeric survey: max Delta-phi from core phi0=0, D0=1, S0=0, vary Q0")
dphis = []
for Q0 in np.linspace(0, 5, 51):
    o = run([1.0, 0.0, 0.0, float(Q0)])
    if o:
        dphis.append((Q0, o["dphi"], o["phi_end"], o["S_end"]))
# report
arr = np.array([d[1] for d in dphis])
print(f"  n={len(dphis)}  Δφ max={arr.max():.4f}  at Q0={dphis[int(np.argmax(arr))][0]:.3f}")
print(f"  Δφ p50={np.percentile(arr,50):.4f} p90={np.percentile(arr,90):.4f} p99={np.percentile(arr,99):.4f}")
print("  sample:")
for Q0, dp, pe, Se in dphis[::10]:
    print(f"    Q0={Q0:.2f}  Δφ={dp:.4f}  φ_end={pe:.4f}  S_end={Se:.3f}")

print("\n[5] Vary D0, S0, Q0 (wider)")
best = 0.0
best_lab = ""
vals = []
for D0 in (0.5, 1.0, 2.0, 5.0):
    for S0 in (0.0, 0.5, 1.0, 2.0, -0.5):
        for Q0 in (0.0, 0.2, 0.5, 1.0, 2.0, 3.0):
            o = run([D0, S0, 0.0, float(Q0)], r0=0.15, r_max=25.0)
            if not o or not o["ok"]:
                continue
            vals.append(o["dphi"])
            if o["dphi"] > best:
                best = o["dphi"]
                best_lab = f"D0={D0} S0={S0} Q0={Q0} Δφ={o['dphi']:.4f} φe={o['phi_end']:.4f}"
print(f"  n_ok={len(vals)}  max Δφ={max(vals):.4f}  ({best_lab})")
print(f"  p50={np.percentile(vals,50):.4f} p90={np.percentile(vals,90):.4f} p99={np.percentile(vals,99):.4f}")

print("\n[6] Shift seed phi0 (not gauge): start phi0≠0, same Q0=0.5 D0=1 S0=0")
for phi0 in (-1.0, -0.5, 0.0, 0.5, 1.0, 2.0):
    o = run([1.0, 0.0, float(phi0), 0.5])
    if o:
        print(
            f"  phi0={phi0:+.1f}  φ_max={o['phi_max']:.4f}  Δφ={o['dphi']:.4f}  "
            f"φ_end={o['phi_end']:.4f}"
        )

print("\n[7] Interpretation notes for theorem attempt:")
print("  - No bound on absolute phi (const-phi solutions unbounded).")
print("  - From phi0=0 flat-core family, Δφ appears capped near ~2.05 in dense scans.")
print("  - Capping is of (phi_infty - phi_core) for this data class, not of phi in field space.")
print("  - Full theorem needs: (i) precise data class; (ii) Lyapunov or first integral;")
print("    (iii) proof Δφ ≤ Δ* or counterexample with Δφ >> 2.")

# Try to find counterexample: large Q0 with small D0
print("\n[8] Hunt counterexample Δφ >> 2.1")
found = False
for D0 in np.logspace(-1, 1, 15):
    for Q0 in np.logspace(-2, 1.5, 20):
        for S0 in (0.0, 0.1, 1.0):
            o = run([float(D0), float(S0), 0.0, float(Q0)], r0=max(0.05, 0.1 * D0), r_max=30.0)
            if o and o["dphi"] > 2.2:
                print(
                    f"  FOUND Δφ={o['dphi']:.4f} D0={D0:.3g} S0={S0} Q0={Q0:.3g} "
                    f"φe={o['phi_end']:.4f} ok={o['ok']}"
                )
                found = True
if not found:
    print("  No Δφ>2.2 found in counterexample hunt (this grid).")

print("\nDONE ceiling probe")
