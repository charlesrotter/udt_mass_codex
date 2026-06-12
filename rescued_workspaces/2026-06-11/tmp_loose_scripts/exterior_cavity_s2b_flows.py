#!/usr/bin/env python3
"""Script 2b: robust flow integration in t = ln(1/y), scaled vars.
u = yF, v = ya, g = y^2 F', h = y^2 a'.
du/dt = -u - g ; dv/dt = -v - h ; dg/dt = e^-t H(kappa) ; dh/dt = e^-t 2 sqrt3 W'
kappa = sqrt3 v/u.  SAT fixed point: g->-B, u->B, kappa_inf = sqrt3 v/u < 1.
TERM: kappa -> 1 at finite t (seal; y_dgn = e^-t).
"""
import numpy as np
from scipy.integrate import solve_ivp

SQ3 = np.sqrt(3.0)

def Hfun(k):
    k = min(abs(k), 1 - 1e-15)
    if k < 1e-5: return k*k/3 + k**4/5
    return np.log((1+k)/(1-k))/(2*k) - 1

def Wpfun(k):
    s = np.sign(k); k = min(abs(k), 1 - 1e-15)
    if k < 1e-5: return s*(k/3 + 2*k**3/15)
    L = np.log((1+k)/(1-k))
    return s*(L*(1+k*k) - 2*k)/(8*k*k)

def rhs(t, w):
    u, v, g, h = w
    k = SQ3*v/u
    e = np.exp(-t)
    return [-u - g, -v - h, e*Hfun(k), e*2*SQ3*Wpfun(k)]

KSEAL = 1 - 1e-7
def ev_seal(t, w): return abs(SQ3*w[1]/w[0]) - KSEAL
ev_seal.terminal = True
def ev_u0(t, w): return w[0] - 1e-12
ev_u0.terminal = True

def flow(gamma, c, a1=0.0, F1=1.0, tmax=30.0, rtol=1e-10):
    w0 = [F1, a1, -gamma, -c]
    sol = solve_ivp(rhs, [0.0, tmax], w0, events=[ev_seal, ev_u0],
                    rtol=rtol, atol=1e-14, method='Radau', dense_output=True)
    out = {'ok': sol.status >= 0}
    if len(sol.t_events[0]):
        t_e = sol.t_events[0][0]; w = sol.y_events[0][0]
        out.update(type='TERM', y_end=np.exp(-t_e), F_end=w[0]*np.exp(t_e))
    elif len(sol.t_events[1]):
        t_e = sol.t_events[1][0]
        out.update(type='F0DEG', y_end=np.exp(-t_e), F_end=0.0)
    elif sol.status == 0:
        u, v, g, h = sol.y[:, -1]
        out.update(type='SAT', y_end=np.exp(-tmax), B=-g, kinf=abs(SQ3*v/u),
                   F_end=u*np.exp(tmax))
    else:
        out.update(type='STALL', y_end=np.exp(-sol.t[-1]), F_end=np.nan)
    ts = np.linspace(0, sol.t[-1], 6000)
    W = sol.sol(ts)
    K = np.abs(SQ3*W[1]/W[0])
    Fv = W[0]*np.exp(ts)
    out['minF'] = Fv.min()
    fmin = Fv*(1 - np.clip(K, 0, 1))
    out['min_fmin'] = fmin.min()
    bel = ts[fmin < 1 - 1e-12]
    out['y_pw_onset'] = float(np.exp(-bel.min())) if len(bel) else None
    out['traj'] = (np.exp(-ts), Fv, K)
    return out

def outcome_scan(gamma, cs):
    return [(c, flow(gamma, c)['type']) for c in cs]

def threshold(gamma, a1=0.0, lo=1e-8, hi=4.0, iters=55):
    if flow(gamma, lo, a1)['type'] != 'SAT': return None
    if flow(gamma, hi, a1)['type'] != 'TERM': return None
    for _ in range(iters):
        mid = np.sqrt(lo*hi)
        if flow(gamma, mid, a1)['type'] == 'SAT': lo = mid
        else: hi = mid
    return np.sqrt(lo*hi)

if __name__ == '__main__':
    print("=== A. monotonicity check of outcome in c (gamma=1/3) ===")
    for c, ty in outcome_scan(1/3, [1e-4, 1e-3, 5e-3, 0.01, 0.02, 0.03, 0.04, 0.045,
                                    0.05, 0.06, 0.08, 0.1, 0.3, 1.0]):
        print(f"  c={c:9.5f} -> {ty}")

    print("\n=== B. banked-flow reproduction (corrected demand jet, gamma=1/3) ===")
    r = flow(1/3, 0.1762261451, a1=0.394385163)
    print(f"corrected: {r['type']} y_end={r['y_end']:.6f} (banked 0.621)  F_seal={r['F_end']:.4f}")
    k1s = 0.23032943298089031; q = 1/3
    r2 = flow(q, (q*k1s + 0.5*q*k1s)/SQ3, a1=k1s/SQ3)
    print(f"slipped:   {r2['type']} y_end={r2['y_end']:.6f} (banked 0.221)")

    print("\n=== C. threshold c*(gamma), momentum-only class a(1)=0 ===")
    print(f"{'gamma':>8} {'c*':>14} {'c*/g^2':>10} {'c*/(sq3 g^2/2)':>15} {'g/sq3':>9} {'clean band?':>11}")
    gammas = [0.01, 0.02, 0.05, 0.1, 0.2, 1/3, 0.5, 1.0, 2.0]
    cst = {}
    for gam in gammas:
        cs = threshold(gam); cst[gam] = cs
        if cs:
            print(f"{gam:8.3f} {cs:14.9f} {cs/gam**2:10.5f} {cs/(SQ3*gam**2/2):15.5f} "
                  f"{gam/SQ3:9.5f} {str(cs < gam/SQ3):>11}")
        else:
            print(f"{gam:8.3f}   no bracket")

    print("\n=== D. gamma=0: outcome census ===")
    for c in [1e-5, 1e-3, 0.1]:
        r = flow(0.0, c)
        print(f"  c={c:8.5f}: {r['type']} y_end={r['y_end']:.6f} minF={r['minF']:.6f}")

    print("\n=== E. formed cavity vs c (gamma=1/3) ===")
    cs = cst[1/3]
    print(f"c* = {cs:.9f}")
    hdr = f"{'c':>12} {'type':>5} {'y_dgn':>10} {'F_seal':>10} {'depth':>8} {'minF':>8} {'min_fmin':>9} {'pw_onset_y':>10}"
    print(hdr)
    for dc in [1e-7, 1e-5, 1e-3, 0.01, 0.05, 0.1, 0.3, 1.0, 3.0]:
        r = flow(1/3, cs*(1+0) + dc) if True else None
        r = flow(1/3, cs + dc)
        on = f"{r['y_pw_onset']:.4f}" if r['y_pw_onset'] else "none"
        dep = 0.5*np.log(r['F_end']) if r['F_end'] and r['F_end'] > 0 else float('nan')
        print(f"{cs+dc:12.8f} {r['type']:>5} {r['y_end']:10.6f} {r['F_end']:10.4f} "
              f"{dep:8.4f} {r['minF']:8.5f} {r['min_fmin']:9.6f} {on:>10}")

    print("\n=== F. near-threshold: limiting seal data (gamma=1/3) ===")
    for dc in [1e-3, 1e-5, 1e-7, 1e-9, 1e-11]:
        r = flow(1/3, cs + dc)
        dep = 0.5*np.log(r['F_end']) if r['F_end'] > 0 else float('nan')
        print(f"  c-c*={dc:.0e}: {r['type']} y_dgn={r['y_end']:.7f} F_seal={r['F_end']:.5f} depth={dep:.5f}")
    print("  SAT side kappa_inf approach:")
    for dc in [1e-3, 1e-5, 1e-7]:
        r = flow(1/3, cs - dc)
        print(f"  c*-c={dc:.0e}: {r['type']} kinf={r.get('kinf', float('nan')):.8f} B={r.get('B', float('nan')):.6f}")

    print("\n=== G. monopole exponent of forming flow (gamma=1/3, c=c*+0.01) ===")
    r = flow(1/3, cs + 0.01)
    ys, Fv, K = r['traj']
    sel = (ys > 1.5*r['y_end']) & (ys < 0.9)
    p = np.polyfit(np.log(ys[sel]), np.log(Fv[sel]), 1)
    print(f"  F ~ y^p, p = {p[0]:.4f} over ({1.5*r['y_end']:.3f}, 0.9)   [collar -1/3]")
    sel2 = (ys > 0.5) & (ys < 0.95)
    p2 = np.polyfit(np.log(ys[sel2]), np.log(Fv[sel2]), 1)
    print(f"  outer collar region (0.5,0.95): p = {p2[0]:.4f}")
