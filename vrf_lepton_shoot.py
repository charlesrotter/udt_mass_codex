"""
RESCUE A (independent method 2): SHOOTING for static excited solitons.
Integrate the EOM from r_core with Th(core)=pi and varied Th'(core)=s<0;
record Th(r_int) as a function of s. Each sign change of [Th(r_int)] vs s
that hits 0 is a soliton; count distinct branches & their node structure.
A genuine excited (1-node, 2-node) static soliton would appear as additional
roots with interior turning points. agent: blind-verifier 2026-06-14
"""
import numpy as np
from scipy.integrate import solve_ivp
import sympy as sp

r_s, Th_s, p_s = sp.symbols('r Th p', real=True)
TWO_PI_3 = 2*sp.pi/3
S = sp.sin(Th_s)
ep = sp.exp(p_s)
a_sym = TWO_PI_3*sp.exp(-p_s)*(r_s**2*S**2 + 2*r_s**2 + 2*S**4 + 2*S**2)
b_sym = TWO_PI_3*sp.exp(-p_s)*(4*ep**2*S**2 + ep**2*S**4/r_s**2)
af = sp.lambdify((r_s, Th_s, p_s), a_sym, 'numpy')
aThf = sp.lambdify((r_s, Th_s, p_s), sp.diff(a_sym, Th_s), 'numpy')
bThf = sp.lambdify((r_s, Th_s, p_s), sp.diff(b_sym, Th_s), 'numpy')
a_rf = sp.lambdify((r_s, Th_s, p_s), sp.diff(a_sym, r_s), 'numpy')
a_pf = sp.lambdify((r_s, Th_s, p_s), sp.diff(a_sym, p_s), 'numpy')

def phi_funcs(p_depth, r_int):
    if p_depth == 0:
        return (lambda r: 0.0, lambda r: 0.0)
    return (lambda r: -p_depth*np.log(r_int/r), lambda r: p_depth/r)

def shoot(s, p_depth, r_core, r_int):
    phf, fpf = phi_funcs(p_depth, r_int)
    def rhs(r, y):
        Th, Thp = y
        p = phf(r); dp = fpf(r)
        a = af(r, Th, p)
        dadr = a_rf(r, Th, p) + a_pf(r, Th, p)*dp + aThf(r, Th, p)*Thp
        Thpp = (aThf(r, Th, p)*Thp**2 + bThf(r, Th, p) - 2*dadr*Thp)/(2*a)
        return [Thp, Thpp]
    sol = solve_ivp(rhs, [r_core, r_int], [np.pi, s], rtol=1e-9, atol=1e-11,
                    dense_output=True, max_step=(r_int-r_core)/2000)
    if not sol.success:
        return None
    rr = np.linspace(r_core, r_int, 4000)
    Th = sol.sol(rr)[0]
    return rr, Th

def analyze(p_depth=0.0, r_core=0.05, cellL=14.0):
    r_int = r_core + cellL
    # scan Th'(core) negative (profile descends from pi). Range broad.
    svals = -np.geomspace(1e-2, 5e2, 800)
    endTh = []
    for s in svals:
        out = shoot(s, p_depth, r_core, r_int)
        endTh.append(out[1][-1] if out is not None else np.nan)
    endTh = np.array(endTh)
    # find roots Th(r_int)=0 (the seal BC). bracket sign changes.
    roots = []
    for i in range(len(svals)-1):
        a, b = endTh[i], endTh[i+1]
        if np.isfinite(a) and np.isfinite(b) and a*b < 0:
            # bisect
            lo, hi = svals[i], svals[i+1]
            for _ in range(60):
                mid = 0.5*(lo+hi)
                out = shoot(mid, p_depth, r_core, r_int)
                fm = out[1][-1]
                if (fm*np.sign(a)) > 0: lo = mid
                else: hi = mid
            sroot = 0.5*(lo+hi)
            out = shoot(sroot, p_depth, r_core, r_int)
            rr, Th = out
            # node structure: interior turning points (extrema), overshoots
            turns = np.sum(np.diff(np.sign(np.diff(Th))) != 0)
            over = np.sum((Th < -0.02) | (Th > np.pi+0.02))
            roots.append((sroot, turns, over, Th))
    return svals, endTh, roots, r_int

if __name__ == '__main__':
    for p_depth in [0.0, 1.0]:
        svals, endTh, roots, r_int = analyze(p_depth)
        print(f"\np_depth={p_depth}: found {len(roots)} shooting solution(s) hitting Th(seal)=0")
        for k, (s, turns, over, Th) in enumerate(roots):
            label = 'MONOTONE (ground)' if (turns == 0 and over == 0) else f'EXCITED? turns={turns} over={over}'
            print(f"   root {k}: Th'(core)={s:.4e}  interior-turns={turns} out-of-range={over}  -> {label}")
        # also report how many sign changes the endpoint map has (potential roots)
        sc = np.sum(np.diff(np.sign(endTh[np.isfinite(endTh)])) != 0)
        print(f"   endpoint-map sign changes (candidate roots incl far-overshoot): {sc}")
