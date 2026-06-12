#!/usr/bin/env python3
"""Script 2c (final): matter-side formation flows, corrected t-formulation."""
import numpy as np
from scipy.integrate import solve_ivp

SQ3 = np.sqrt(3.0)

def Hfun(k):
    k = min(abs(k), 1-1e-15)
    if k < 0.05:
        k2 = k*k
        return k2*(1/3 + k2*(1/5 + k2*(1/7 + k2/9)))
    return np.log((1+k)/(1-k))/(2*k) - 1

def Wpfun(k):
    s = np.sign(k); k = min(abs(k), 1-1e-15)
    if k < 0.05:
        k2 = k*k
        return s*k*(1/3 + k2*(2/15 + k2*(3/35 + k2*4/63)))
    L = np.log((1+k)/(1-k))
    return s*(L*(1+k*k)-2*k)/(8*k*k)

def rhs(t, w):
    u, v, g, h = w
    k = SQ3*v/u; e = np.exp(-t)
    return [-u-g, -v-h, e*Hfun(k), -e*2*SQ3*Wpfun(k)]

def ev_seal(t, w): return abs(SQ3*w[1]/w[0]) - (1-1e-7)
ev_seal.terminal = True
def ev_u0(t, w): return w[0] - 1e-12
ev_u0.terminal = True

def flow(gamma, c, a1=0.0, tmax=35.0, rtol=1e-10, audit=False):
    sol = solve_ivp(rhs, [0, tmax], [1.0, a1, -gamma, -c], events=[ev_seal, ev_u0],
                    rtol=rtol, atol=1e-14, method='DOP853', dense_output=audit)
    out = {}
    if len(sol.t_events[0]):
        te = sol.t_events[0][0]; w = sol.y_events[0][0]
        out = dict(type='TERM', y_end=np.exp(-te), F_end=w[0]*np.exp(te))
    elif len(sol.t_events[1]):
        out = dict(type='F0DEG', y_end=np.exp(-sol.t_events[1][0]), F_end=0.0)
    else:
        u, v, g, h = sol.y[:, -1]
        out = dict(type='SAT', kinf=abs(SQ3*v/u), B=-g, y_end=np.exp(-tmax),
                   F_end=u*np.exp(tmax))
    if audit:
        ts = np.linspace(0, sol.t[-1], 8000)
        W = sol.sol(ts)
        K = np.abs(SQ3*W[1]/W[0]); Fv = W[0]*np.exp(ts)
        out['minF'] = Fv.min()
        fmin = Fv*(1-np.clip(K, 0, 1))
        out['min_fmin'] = fmin.min()
        bel = ts[fmin < 1-1e-12]
        out['y_pw_onset'] = float(np.exp(-bel.min())) if len(bel) else None
        out['traj'] = (np.exp(-ts), Fv, K)
    return out

def threshold(gamma, a1=0.0, lo=1e-9, hi=8.0, iters=52):
    if flow(gamma, lo, a1)['type'] != 'SAT': return None
    if flow(gamma, hi, a1)['type'] != 'TERM': return None
    for _ in range(iters):
        mid = np.sqrt(lo*hi)
        if flow(gamma, mid, a1)['type'] == 'SAT': lo = mid
        else: hi = mid
    return np.sqrt(lo*hi)

if __name__ == '__main__':
    print("=== A. outcome monotone in c? (gamma=1/3) ===")
    types = [(c, flow(1/3, c)['type']) for c in
             [1e-4, 0.005, 0.01, 0.02, 0.03, 0.04, 0.044, 0.046, 0.05, 0.06, 0.1, 0.5, 2.0]]
    print("  " + " | ".join(f"{c:g}:{t}" for c, t in types))
    mono = all(t2 != 'SAT' or t1 == 'SAT' for (_, t1), (_, t2) in zip(types, types[1:]))
    print("  monotone (SAT block then TERM block):", mono)

    print("\n=== B. threshold c*(gamma), a(1)=0 ===")
    gammas = [0.01, 0.02, 0.05, 0.1, 0.2, 1/3, 0.5, 1.0, 2.0]
    cst = {}
    print(f"{'gamma':>7} {'c*':>15} {'c*/g^2':>9} {'c*/(sq3g^2/2)':>14} {'g/sq3':>9} {'clean band?':>11}")
    for gam in gammas:
        cs = threshold(gam); cst[gam] = cs
        if cs:
            print(f"{gam:7.3f} {cs:15.10f} {cs/gam**2:9.5f} {cs/(SQ3*gam**2/2):14.5f} "
                  f"{gam/SQ3:9.5f} {str(cs < gam/SQ3):>11}")
        else: print(f"{gam:7.3f}  no bracket")

    print("\n=== C. gamma=0 census ===")
    for c in [1e-6, 1e-3, 0.1]:
        r = flow(0.0, c, audit=True)
        print(f"  c={c:g}: {r['type']} y_end={r['y_end']:.6f} minF={r['minF']:.6f}")

    print("\n=== D. formed cavity vs c (gamma=1/3), audits ===")
    cs = cst[1/3]
    print(f"  c* = {cs:.10f}")
    print(f"{'c':>13} {'type':>5} {'y_dgn':>10} {'F_seal':>10} {'depth':>8} {'minF':>9} {'min_fmin':>10} {'pw_onset':>9}")
    for dc in [1e-6, 1e-4, 1e-3, 0.01, 0.05, 0.1, 0.3, 1.0, 3.0]:
        r = flow(1/3, cs+dc, audit=True)
        on = f"{r['y_pw_onset']:.4f}" if r['y_pw_onset'] else "none"
        dep = 0.5*np.log(r['F_end']) if r['F_end'] > 0 else float('nan')
        print(f"{cs+dc:13.8f} {r['type']:>5} {r['y_end']:10.6f} {r['F_end']:10.4f} {dep:8.4f} "
              f"{r['minF']:9.6f} {r['min_fmin']:10.6f} {on:>9}")

    print("\n=== E. near-threshold limit (gamma=1/3) ===")
    for dc in [1e-4, 1e-6, 1e-8, 1e-10]:
        r = flow(1/3, cs+dc)
        dep = 0.5*np.log(r['F_end'])
        print(f"  c-c*={dc:.0e}: {r['type']} y_dgn={r['y_end']:.8f} F_seal={r['F_end']:.5f} depth={dep:.5f}")
    for dc in [1e-4, 1e-6, 1e-8]:
        r = flow(1/3, cs-dc)
        print(f"  c*-c={dc:.0e}: {r['type']} kinf={r.get('kinf', float('nan')):.8f} B={r.get('B', float('nan')):.7f}")

    print("\n=== F. seal-depth law: y_dgn(c), depth(c) fits (gamma=1/3) ===")
    dcs = np.array([1e-5, 1e-4, 1e-3, 0.003, 0.01, 0.03])
    yd = []; dep = []
    for dc in dcs:
        r = flow(1/3, cs+dc)
        yd.append(r['y_end']); dep.append(0.5*np.log(r['F_end']))
    yd = np.array(yd); dep = np.array(dep)
    y0 = yd[0]
    p = np.polyfit(np.log(dcs), np.log(yd-y0+1e-12), 1)
    print(f"  y_dgn(c*)+ ~ y0 + k (c-c*)^p: y0={y0:.6f}, p={p[0]:.3f}")
    print("  depths:", " ".join(f"{d:.4f}" for d in dep), " (max at threshold)")

    print("\n=== G. monopole exponent of forming flows ===")
    for dc, lab in [(0.01, 'c*+0.01'), (0.3, 'c*+0.3')]:
        r = flow(1/3, cs+dc, audit=True)
        ys, Fv, K = r['traj']
        sel = (ys > 1.5*r['y_end']) & (ys < 0.9)
        if sel.sum() > 10:
            p = np.polyfit(np.log(ys[sel]), np.log(Fv[sel]), 1)
            print(f"  {lab}: F ~ y^{p[0]:.4f} over ({1.5*r['y_end']:.3f},0.9)  [collar -1/3]")

    print("\n=== H. threshold with amplitude loading a(1)=a1 (mixed class) ===")
    for a1 in [0.0, 0.1, 0.2, 0.394385]:
        cs1 = threshold(1/3, a1=a1)
        print(f"  a1={a1:: .4f}: c* = {cs1 if cs1 else 'none'}")
