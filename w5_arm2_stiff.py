#!/usr/bin/env python3
"""W5 ARM-2 — SCRIPT 9: STIFF-CELL ADJUDICATION (implicit Radau).

Date: 2026-06-12.  The W4 verifier lesson (w4b_verifier_stiff):
explicit RK4 cannot resolve the |kappa| ~ 1e-3..1e-2 source stiffness
(sqrt(|dS/dv|) dT >> 1); cells flagged UNRESOLVED-STIFF in the W5
catalog are re-solved here implicitly on the most-unstable ray (rays
decouple exactly on frozen f), W5 untruncated source, TRUE units.

Cells: M1 full domain, dominant ray, kappa {+-0.01, +-0.1} x D_cell
{ON, OFF}, amp 0.01 (the catalog's stiff corner).  Pre-stated: the
Radau label (collapse vs ring vs grow) REPLACES the RK4 label for
these cells; UNRESOLVED-STIFF is never banked as physics.

Log: /tmp/w5_arm2_stiff.log.  New file.  2026-06-12, W5 Arm-2.
"""
import sys, time
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, "/home/udt-admin/udt_mass_codex")
import w4b_verifier_lib as vl
import w5_arm2_lib as w5

def log(*a):
    print(*a, flush=True)

mem = vl.Member(1.0, 0.18413678, Nu=24, Nt=8000)
geo = w5.GeoW5(mem, t_b=None, Nt=4000, Nx=320)
K = int(np.argmax(geo.b_t.sum(0)))
Nx = geo.Nx
xg = geo.xg[K]
dx = geo.dx[K]
f = geo.f[K]
fth2 = geo.fth2[K]
r = geo.r[K]
a1 = 2 * f / r
sc = 2.0 * fth2 / (16 * r ** 2)
xmax = geo.xmax[K]
log(f"dominant ray k={K} u={mem.u[K]:+.4f} xmax={xmax:.4f}")


def run_ray(kappa, dcell, amp, T_end, tag):
    fac = 1.0 - 2.0 * kappa / f
    v0 = np.log1p(amp * np.exp(-((xg - 0.55 * xmax)
                                 / (0.10 * xmax)) ** 2))
    v0[0] = 0.0
    y0 = np.concatenate([v0, np.zeros(Nx)])

    def rhs(t, y):
        v, vt = y[:Nx], y[Nx:]
        lap = np.empty(Nx)
        lap[1:-1] = (v[2:] - 2 * v[1:-1] + v[:-2]) / dx ** 2
        lap[0] = 0.0
        lap[-1] = 2 * (v[-2] - v[-1]) / dx ** 2
        gr = np.empty(Nx)
        gr[1:-1] = (v[2:] - v[:-2]) / (2 * dx)
        gr[0] = gr[-1] = 0.0
        if dcell:
            S = sc / kappa * (np.exp(v) - fac * np.exp(-2 * v))
        else:
            S = -sc / kappa * fac * np.exp(-2 * v)
        dvt = lap + a1 * gr + S
        dv = vt.copy()
        dv[0] = 0.0
        dvt[0] = 0.0
        return np.concatenate([dv, dvt])

    def ev_dn(t, y):
        return np.min(y[:Nx]) - np.log(0.05)
    ev_dn.terminal = True

    def ev_up(t, y):
        return np.max(y[:Nx]) - 8.0
    ev_up.terminal = True
    t0 = time.time()
    s = solve_ivp(rhs, (0, T_end), y0, method='Radau', rtol=1e-8,
                  atol=1e-10, events=[ev_dn, ev_up],
                  dense_output=True, max_step=0.5)
    tq = np.linspace(0, s.t[-1], 1200)
    Z = s.sol(tq)
    env = np.max(np.abs(Z[:Nx]), axis=0)
    term = None
    if len(s.t_events[0]):
        term = ("COLLAPSE-", float(s.t_events[0][0]))
    if len(s.t_events[1]):
        term = ("COLLAPSE+", float(s.t_events[1][0]))
    m = len(env)
    sl = np.polyfit(tq[3 * m // 4:],
                    np.log(np.maximum(env[3 * m // 4:], 1e-300)), 1)[0]
    log(f"[{tag}] kappa={kappa:+.3g} dcell={dcell}: T={s.t[-1]:.3f}/"
        f"{T_end} term={term} env0={env[0]:.3g} envmax={env.max():.3g}"
        f" envfin={env[-1]:.3g} late-rate={sl:+.4f} "
        f"({time.time()-t0:.0f}s, {s.nfev} fev)")
    return term


T = 7.2
log("=" * 72)
log("STIFF CELLS (W5 untruncated, TRUE units, implicit Radau)")
log("=" * 72)
for dc in (True, False):
    for kap in (+0.01, -0.01, +0.1, -0.1):
        run_ray(kap, dc, 0.01, T, "W5")
log("reference (species OFF = W4 truncation):")
for dc in (True, False):
    for kap in (+0.01, -0.01):
        fac_save = None
        # quick species-off variant: rebuild with fac = 1
        fac = 1.0
        # inline: reuse run_ray with kappa trick not possible; redo:
        def run_off(kappa, dcell, amp, T_end, tag):
            v0 = np.log1p(amp * np.exp(-((xg - 0.55 * xmax)
                                         / (0.10 * xmax)) ** 2))
            v0[0] = 0.0
            y0 = np.concatenate([v0, np.zeros(Nx)])

            def rhs(t, y):
                v, vt = y[:Nx], y[Nx:]
                lap = np.empty(Nx)
                lap[1:-1] = (v[2:] - 2 * v[1:-1] + v[:-2]) / dx ** 2
                lap[0] = 0.0
                lap[-1] = 2 * (v[-2] - v[-1]) / dx ** 2
                gr = np.empty(Nx)
                gr[1:-1] = (v[2:] - v[:-2]) / (2 * dx)
                gr[0] = gr[-1] = 0.0
                if dcell:
                    S = sc / kappa * (np.exp(v) - np.exp(-2 * v))
                else:
                    S = -sc / kappa * np.exp(-2 * v)
                dvt = lap + a1 * gr + S
                dv = vt.copy()
                dv[0] = 0.0
                dvt[0] = 0.0
                return np.concatenate([dv, dvt])

            def ev_dn(t, y):
                return np.min(y[:Nx]) - np.log(0.05)
            ev_dn.terminal = True

            def ev_up(t, y):
                return np.max(y[:Nx]) - 8.0
            ev_up.terminal = True
            s = solve_ivp(rhs, (0, T_end), y0, method='Radau',
                          rtol=1e-8, atol=1e-10,
                          events=[ev_dn, ev_up], max_step=0.5)
            term = None
            if len(s.t_events[0]):
                term = ("COLLAPSE-", float(s.t_events[0][0]))
            if len(s.t_events[1]):
                term = ("COLLAPSE+", float(s.t_events[1][0]))
            log(f"[{tag}] kappa={kappa:+.3g} dcell={dcell}: "
                f"T={s.t[-1]:.3f}/{T_end} term={term}")
        run_off(kap, dc, 0.01, T, "W4ref")
log("done.")
