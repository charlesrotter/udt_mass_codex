#!/usr/bin/env python3
"""Script 2: matter-side formation flows (statics in y, inward from interface).
System (per solid angle, EL of S = int (y^2/4)(F'^2+a'^2) + P):
  (y^2 F')' = 2 P_F = -H(kappa),  H = L/(2k) - 1
  (y^2 a')' = 2 P_a = 2 sqrt3 W'(kappa) sgn(a),  W' = [L(1+k^2)-2k]/(8k^2)
  kappa = sqrt3 a / F, L = ln((1+k)/(1-k))
Interface data (y=1): F=1, F'=-gamma, a=a1, a'=-c.
Outcomes inward: TERM (kappa->1, cavity seals), SAT (rides B/y, infinite action),
F0DEG (F->0, average horizon-touch).
"""
import numpy as np
from scipy.integrate import solve_ivp

SQ3 = np.sqrt(3.0)

def Hfun(k):
    k = abs(k)
    if k < 1e-5:
        return k*k/3 + k**4/5
    if k >= 1.0:
        return np.inf
    return np.log((1+k)/(1-k))/(2*k) - 1

def Wpfun(k):
    s = np.sign(k); k = abs(k)
    if k < 1e-5:
        return s*(k/3 + 2*k**3/15)
    if k >= 1.0:
        return s*np.inf
    L = np.log((1+k)/(1-k))
    return s*(L*(1+k*k) - 2*k)/(8*k*k)

def rhs(y, u):
    F, g, a, h = u            # g = y^2 F', h = y^2 a'
    k = SQ3*a/F
    return [g/y**2, -Hfun(k), h/y**2, 2*SQ3*Wpfun(k)]

def ev_kappa(y, u):           # kappa -> 1 (seal)
    return abs(SQ3*u[2]/u[0]) - (1 - 1e-9)
ev_kappa.terminal = True
def ev_F0(y, u):              # F -> 0
    return u[0] - 1e-10
ev_F0.terminal = True

def flow(gamma, c, a1=0.0, F1=1.0, g1=None, ymin=1e-6, rtol=1e-11):
    u0 = [F1, -gamma if g1 is None else g1, a1, -c]
    sol = solve_ivp(rhs, [1.0, ymin], u0, events=[ev_kappa, ev_F0],
                    rtol=rtol, atol=1e-13, method='LSODA', dense_output=True)
    out = {}
    if len(sol.t_events[0]):
        out['type'] = 'TERM'; out['y_end'] = sol.t_events[0][0]
        out['F_end'] = sol.y_events[0][0][0]
    elif len(sol.t_events[1]):
        out['type'] = 'F0DEG'; out['y_end'] = sol.t_events[1][0]
        out['F_end'] = sol.y_events[1][0][0]
    else:
        out['type'] = 'SAT'; out['y_end'] = sol.t[-1]
        out['B'] = -sol.y[1, -1]   # F ~ B/y
        out['kinf'] = abs(SQ3*sol.y[2, -1]/sol.y[0, -1])
        out['F_end'] = sol.y[0, -1]
    # audits along the trajectory
    ys = np.geomspace(max(out['y_end']*1.0000001, 1e-6), 1.0, 4000)
    ys = ys[ys >= sol.t[-1]] if sol.t[-1] > ys[0] else ys
    U = sol.sol(ys)
    K = np.abs(SQ3*U[2]/U[0])
    out['minF'] = U[0].min()
    fmin = U[0]*(1-np.clip(K, 0, 1))
    out['min_fmin'] = fmin.min()
    below = ys[fmin < 1 - 1e-12]
    out['y_pw_onset'] = below.max() if len(below) else None  # outermost pointwise violation
    out['traj'] = (ys, U, K)
    return out

def threshold(gamma, a1=0.0, lo=1e-6, hi=2.0, iters=60):
    """smallest c with TERM (assumes monotone outcome in c: SAT below, TERM above)"""
    fl = flow(gamma, lo, a1); fh = flow(gamma, hi, a1)
    if fl['type'] != 'SAT' or fh['type'] == 'SAT':
        return None, fl['type'], fh['type']
    for _ in range(iters):
        mid = 0.5*(lo+hi)
        if flow(gamma, mid, a1)['type'] == 'SAT': lo = mid
        else: hi = mid
    return 0.5*(lo+hi), 'SAT', 'TERM'

if __name__ == '__main__':
    print("=== A. banked-flow reproduction attempts (demanded collar data, gamma=q=1/3) ===")
    # corrected demand: a1=0.394385163, a'(1)=-0.176226 (demanded-profile slope)
    r = flow(1/3, 0.1762261451, a1=0.394385163)
    print(f"corrected demand jet: {r['type']} y_end={r['y_end']:.6f} (banked EL-correct: 0.621)")
    # slipped amplitude kappa1=0.230329:
    k1s = 0.23032943298089031
    # slipped demanded profile slope: linearized H=k^2/3 = (2s/4pi) y^-q => k ~ y^-q/2 * k1s
    # a_d = y^-q k_d/sq3 ; a_d' (1) = (-q k1s + k1s*(-q/2))/sq3 = -(3q/2) k1s/sq3 /...
    q = 1/3
    a1s = k1s/SQ3; aps = (-q*k1s - 0.5*q*k1s)/SQ3
    r2 = flow(q, -aps, a1=a1s)
    print(f"slipped-amplitude jet: {r2['type']} y_end={r2['y_end']:.6f} (banked: 0.221)")

    print("\n=== B. threshold bifurcation: momentum-only class a(1)=0, scan gamma ===")
    print(f"{'gamma':>8} {'c*':>14} {'c*/gamma^2':>12} {'c*/(sq3 g^2/2)':>15} {'gamma/sq3':>10}")
    gammas = [0.02, 0.05, 0.1, 1/3, 0.5, 1.0]
    cstars = {}
    for gam in gammas:
        cs, tl, th = threshold(gam)
        cstars[gam] = cs
        if cs:
            print(f"{gam:8.3f} {cs:14.9f} {cs/gam**2:12.6f} {cs/(SQ3*gam**2/2):15.6f} {gam/SQ3:10.6f}")
        else:
            print(f"{gam:8.3f}  no bracket: lo->{tl} hi->{th}")

    print("\n=== C. gamma=0 (no monopole momentum delivered): outcome census ===")
    for c in [1e-4, 1e-2, 0.1, 0.5]:
        r = flow(0.0, c)
        print(f"c={c:8.4f}: {r['type']:6s} y_end={r['y_end']:.6f} minF={r['minF']:.6f}")

    print("\n=== D. formed-cavity scaling at gamma=1/3: y_dgn, depth vs c ===")
    gam = 1/3; cs = cstars.get(gam)
    print(f"c* = {cs:.9f}")
    print(f"{'c':>12} {'type':>6} {'y_dgn':>10} {'F_seal':>12} {'depth=(1/2)lnF':>14} {'minF':>9} {'min f_min':>10} {'y_pw_onset':>11}")
    for dc in [1e-6, 1e-4, 1e-3, 1e-2, 0.05, 0.1, 0.3, 1.0, 3.0]:
        c = cs + dc
        r = flow(gam, c)
        on = f"{r['y_pw_onset']:.4f}" if r['y_pw_onset'] else "none"
        print(f"{c:12.7f} {r['type']:>6} {r['y_end']:10.6f} {r['F_end']:12.5f} "
              f"{0.5*np.log(max(r['F_end'],1e-300)):14.5f} {r['minF']:9.5f} {r['min_fmin']:10.6f} {on:>11}")

    print("\n=== E. near-threshold critical scaling (gamma=1/3) ===")
    for dc in [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]:
        r = flow(gam, cs + dc)
        print(f"c-c*={dc:.1e}: {r['type']} y_dgn={r['y_end']:.7f} F_seal={r['F_end']:.4f} depth={0.5*np.log(r['F_end']):.4f}")

    print("\n=== F. does the forming flow track the y^{-1/3} collar? (gamma=1/3, c=c*+0.01) ===")
    r = flow(gam, cs + 0.01)
    ys, U, K = r['traj']
    sel = (ys > 1.2*r['y_end']) & (ys < 0.9)
    p = np.polyfit(np.log(ys[sel]), np.log(U[0][sel]), 1)
    print(f"local exponent fit F ~ y^p over ({1.2*r['y_end']:.3f},0.9): p = {p[0]:.4f} (collar: -1/3 = -0.3333)")

    print("\n=== G. pointwise-clean formation band? c* vs gamma/sqrt3 (interface-marginal line) ===")
    for gam in gammas:
        cs = cstars.get(gam)
        if cs:
            print(f"gamma={gam:6.3f}: c*={cs:.6f}  gamma/sq3={gam/SQ3:.6f}  band exists: {cs < gam/SQ3}")
