#!/usr/bin/env python3
"""
Continue Path B vacuum: first-integral hunt + edge-oriented shooting.
No matter stand-ins. Gravity = free D_A + EH + R1 kinetic.
"""
from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

Z = 1.0

# =============================================================================
# CAS
# =============================================================================
print("=" * 70)
print("CAS — Path B structure / integrals")
print("=" * 70)

r = sp.symbols("r", positive=True)
Zs = sp.symbols("Z", positive=True)
phi = sp.Function("phi")
D = sp.Function("D_A")
ph, php, phpp = phi(r), sp.diff(phi(r), r), sp.diff(phi(r), r, 2)
Dp, Dpp = sp.diff(D(r), r), sp.diff(D(r), r, 2)

el_phi = (
    -Zs * D(r) ** 2 * phpp
    - 2 * Zs * D(r) * Dp * php
    + 4 * D(r) * sp.exp(-2 * ph) * Dpp
)
el_D = (
    Zs * D(r) * sp.exp(2 * ph) * php**2
    - 8 * D(r) * php**2
    + 4 * D(r) * phpp
    + 8 * Dp * php
    - 4 * Dpp
) * sp.exp(-2 * ph)

# pi = Z D^2 phi'
pi = Zs * D(r) ** 2 * php
# EL_phi: pi' = 4 D e^{-2phi} D''
print("EL_phi as pi' - 4 D e^{-2phi} D'' =", sp.simplify(sp.diff(pi, r) - 4 * D(r) * sp.exp(-2 * ph) * Dpp + 0 * el_phi))
print("check:", sp.simplify(sp.diff(pi, r) - 4 * D(r) * sp.exp(-2 * ph) * Dpp - (-el_phi)))
# actually EL_phi = -pi' + 4 D e^{-2phi} D'' = 0
print("EL_phi + pi' - 4 D exp(-2phi) Dpp =", sp.simplify(el_phi + sp.diff(pi, r) - 4 * D(r) * sp.exp(-2 * ph) * Dpp))

# Autonomous: no explicit r in L if we use D as coordinate?
# Try r as dependent, D as independent: common spherical trick
# For now document flux relation and numerical conserved candidates

# Change variable: use D as independent if S=D' != 0
# d/dr = S d/dD, etc. — skip heavy rewrite; numerical conservation scan below

print("\nKnown exact: phi=const, D''=0.")
print("No simple Coulomb free-D_A integral (EL_D blocks q≠0 on D∝r).")


# =============================================================================
# Numeric engine
# =============================================================================
def rhs(r, y):
    D, S, phi, Q = y
    De = max(D, 1e-14)
    e2 = np.exp(np.clip(2.0 * phi, -40, 40))
    em2 = np.exp(np.clip(-2.0 * phi, -40, 40))
    A11 = 4.0 * De * em2
    A12 = -Z * De * De
    A21 = -4.0
    A22 = 4.0 * De
    b1 = 2.0 * Z * De * S * Q
    b2 = -Z * De * e2 * Q * Q + 8.0 * De * Q * Q - 8.0 * S * Q
    det = A11 * A22 - A12 * A21
    if abs(det) < 1e-30:
        return [S, 0.0, Q, 0.0]
    Sp = (b1 * A22 - A12 * b2) / det
    Qp = (A11 * b2 - b1 * A21) / det
    Sp = float(np.clip(Sp if np.isfinite(Sp) else 0.0, -1e6, 1e6))
    Qp = float(np.clip(Qp if np.isfinite(Qp) else 0.0, -1e6, 1e6))
    return [S, Sp, Q, Qp]


def integrate(y0, r0, r_max, events=None):
    return solve_ivp(
        rhs,
        (r0, r_max),
        y0,
        method="RK45",
        rtol=1e-8,
        atol=1e-10,
        max_step=0.05,
        events=events,
        dense_output=False,
    )


def event_phi(phi_cut):
    def ev(r, y):
        return y[2] - phi_cut

    ev.terminal = True
    ev.direction = 1
    return ev


def event_S_zero(r, y):
    return y[1]  # D'

event_S_zero.terminal = False
event_S_zero.direction = -1


def event_D_floor(r, y):
    return y[0] - 1e-4

event_D_floor.terminal = True
event_D_floor.direction = -1


print("\n" + "=" * 70)
print("NUMERIC — conservation diagnostics + edge shooting")
print("=" * 70)

# --- Conservation candidates along a Q-kick trajectory ---
print("\n[C1] Scan possible 'constants' along core Q0=0.5 trajectory")
sol = integrate([1.0, 0.0, 0.0, 0.5], 0.2, 10.0)
r, D, S, phi, Q = sol.t, sol.y[0], sol.y[1], sol.y[2], sol.y[3]
pi = Z * D**2 * Q
# candidates
cands = {
    "pi": pi,
    "Q": Q,
    "S": S,
    "phi": phi,
    "D/r": D / np.maximum(r, 1e-12),
    "pi/D": pi / np.maximum(D, 1e-12),
    "e^{-2phi}*S": np.exp(-2 * phi) * S,
    "S e^{-phi}": S * np.exp(-phi),
    "Q D^2": Q * D**2,
    "Q D^2 e^{2phi}": Q * D**2 * np.exp(2 * phi),
}
print(f"  n={len(r)} r∈[{r[0]:.3g},{r[-1]:.3g}] Δφ={phi[-1]-phi[0]:+.4f}")
for name, arr in cands.items():
    a = arr[5:-5] if len(arr) > 20 else arr
    span = np.nanmax(a) - np.nanmin(a)
    med = np.nanmedian(np.abs(a))
    rel = span / (med + 1e-15)
    print(f"  {name:20s}  span={span:.4e}  rel_span={rel:.4e}  end={arr[-1]:.6g}")


# --- Edge-oriented tests ---
# E1: can any seed hit phi >= phi_cut?
print("\n[E1] Max φ reachable in vacuum IVP (scan Q0, S0)")
best_phi = -1e9
best_lab = None
results_e1 = []
for Q0 in np.linspace(0.01, 3.0, 25):
    for S0 in [0.0, 0.1, 0.5, 1.0, 2.0]:
        for D0 in [0.5, 1.0, 2.0]:
            sol = integrate([D0, S0, 0.0, float(Q0)], 0.15, 15.0, events=[event_phi(20.0), event_D_floor])
            if len(sol.t) < 2:
                continue
            phimax = float(np.nanmax(sol.y[2]))
            results_e1.append(phimax)
            if phimax > best_phi:
                best_phi = phimax
                best_lab = f"D0={D0:g} S0={S0:g} Q0={Q0:.3g} r_end={sol.t[-1]:.3g}"
print(f"  scanned {len(results_e1)} seeds; max φ reached = {best_phi:.4f}  at {best_lab}")
print(f"  φ distribution: p50={np.percentile(results_e1,50):.3f} p90={np.percentile(results_e1,90):.3f} p99={np.percentile(results_e1,99):.3f}")

# E2: can D' cross zero (turnover) with phi still increasing?
print("\n[E2] D' zero-crossings (turnover) while integrating")
n_turn = 0
turn_examples = []
for Q0 in np.linspace(0.05, 2.0, 20):
    for S0 in np.linspace(-1.0, 2.0, 13):
        sol = integrate([1.0, float(S0), 0.0, float(Q0)], 0.2, 12.0)
        if not sol.success and len(sol.t) < 5:
            continue
        S = sol.y[1]
        # sign change + to -
        for i in range(1, len(S)):
            if S[i - 1] > 0.02 and S[i] <= 0:
                n_turn += 1
                if len(turn_examples) < 8:
                    turn_examples.append(
                        f"Q0={Q0:.2g} S0={S0:.2g} r={sol.t[i]:.3g} φ={sol.y[2][i]:.3f} D={sol.y[0][i]:.3g}"
                    )
                break
print(f"  turnovers found: {n_turn}")
for t in turn_examples:
    print(f"    {t}")

# E3: shooting — fix outer r_out, try match S(r_out)=0 (marginal outer slope)
print("\n[E3] Shooting: free Q0 on flat core, target S(r_out)=0")
r_out = 5.0


def S_at_out(Q0):
    sol = integrate([1.0, 0.0, 0.0, float(Q0)], 0.2, r_out)
    if len(sol.t) < 2:
        return 1e6
    return float(sol.y[1][-1])


# sample
Qs = np.linspace(0.01, 2.5, 40)
Ss = [S_at_out(q) for q in Qs]
print("  Q0 scan -> S(r_out):")
for q, s in zip(Qs[::5], Ss[::5]):
    print(f"    Q0={q:.3f}  S({r_out})={s:+.4f}")
# sign changes?
roots = []
for i in range(len(Qs) - 1):
    if Ss[i] * Ss[i + 1] < 0 and abs(Ss[i]) < 1e5 and abs(Ss[i + 1]) < 1e5:
        try:
            rt = brentq(S_at_out, Qs[i], Qs[i + 1])
            roots.append(rt)
        except Exception:
            pass
print(f"  roots S(r_out)=0: {roots if roots else 'none in scan'}")
for rt in roots[:5]:
    sol = integrate([1.0, 0.0, 0.0, rt], 0.2, r_out)
    print(
        f"    Q0*={rt:.4g}: φ_end={sol.y[2][-1]:.4f} D_end={sol.y[0][-1]:.4g} "
        f"S_end={sol.y[1][-1]:.3e} Q_end={sol.y[3][-1]:.3e}"
    )

# E4: target large phi at fixed r_out by varying Q0 — max only
print("\n[E4] Max φ(r_out=5) over Q0 (same family)")
phis = []
for q in Qs:
    sol = integrate([1.0, 0.0, 0.0, float(q)], 0.2, r_out)
    phis.append(float(sol.y[2][-1]) if len(sol.t) else np.nan)
print(f"  max φ(5)={np.nanmax(phis):.4f} at Q0={Qs[int(np.nanargmax(phis))]:.3f}")
print(f"  min φ(5)={np.nanmin(phis):.4f}")

print("\nDONE")
