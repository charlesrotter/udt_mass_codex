#!/usr/bin/env python3
"""W6 FLUX VERIFIER — curvature exponents at D=0, INDEPENDENT engine.

Reproduces arm's claim (C): on the static (time-row OFF) member,
R ~ D^{-3/2}, K ~ D^{-3} on the q* (tangential) branch, and
R ~ D^{-2}, K ~ D^{-4} for a generic transversal q. Confirm the
float64 catastrophic-cancellation trap near D ~ 1e-7. mpmath 80 dps.

Engine: w6_flux_verifier_engine (own, Schwarzschild-validated).
"""
import sys
import time
import math
import mpmath as mp
import sympy as sp
from w6_flux_verifier_engine import kretschmann_ricci

t0 = time.time()
mp.mp.dps = 80
T, ph = sp.symbols('T phi', real=True)
r = sp.Symbol('r', positive=True)
th = sp.Symbol('theta', real=True)


def build_static(qfun, wval=0):
    f = (1 + sp.Rational(1, 10) * sp.cos(th)**2) / r
    W = (1 + wval)**2
    g = sp.Matrix([[-f, 0, 0, 0],
                   [0, 1 / f, qfun, 0],
                   [0, qfun, r**2 * W, 0],
                   [0, 0, 0, r**2 * sp.sin(th)**2 / W]])
    D = sp.simplify(r**2 * W - f * qfun**2)
    return g, D, f


def qstar(f, W):
    fr, fth = sp.diff(f, r), sp.diff(f, th)
    P = f * r**2 * W * fr**2 + fth**2
    return 2 * r**2 * W * fr * fth / P


def fit(rows, idx):
    xs, ys = [], []
    for (_, Dv, Rv, Kv) in rows[-6:]:
        v = Rv if idx == 'R' else Kv
        if Dv != 0 and v != 0:
            xs.append(math.log(abs(float(Dv))))
            ys.append(math.log(abs(float(v))))
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sl = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) \
        / sum((x - mx)**2 for x in xs)
    pred = [my + sl * (x - mx) for x in xs]
    rms = (sum((y - p)**2 for y, p in zip(ys, pred)) / n)**0.5
    return sl, rms


def run_member(name, qfun, th0, rstar_hint=None):
    print(f"\n=== {name} ===", flush=True)
    g, D, f = build_static(qfun)
    K, Rs, _, _, _ = kretschmann_ricci(g, [T, r, th, ph])
    print(f"   [curvature built {time.time()-t0:.0f}s]", flush=True)
    Rs3 = sp.simplify(Rs.subs(th, th0))
    K3 = sp.simplify(K.subs(th, th0))
    D3 = sp.simplify(D.subs(th, th0))
    numD = sp.numer(sp.together(D3))
    poly = sp.Poly(sp.expand(numD), r)
    roots = mp.polyroots([mp.mpf(str(c)) for c in poly.all_coeffs()],
                         maxsteps=300, extraprec=300)
    rstar = None
    for rt in roots:
        if abs(mp.im(rt)) < mp.mpf('1e-40') and mp.re(rt) > 0:
            if rstar_hint is None or abs(mp.re(rt) - rstar_hint) < 2:
                rstar = mp.re(rt)
                break
    print(f"   r* = {mp.nstr(rstar, 20)}", flush=True)
    Rf = sp.lambdify(r, Rs3, 'mpmath')
    Kf = sp.lambdify(r, K3, 'mpmath')
    Df = sp.lambdify(r, D3, 'mpmath')
    # float64 trap callables
    Rf64 = sp.lambdify(r, Rs3, 'numpy')
    Kf64 = sp.lambdify(r, K3, 'numpy')
    Df64 = sp.lambdify(r, D3, 'numpy')
    rows, rows64 = [], []
    for k in range(2, 11):
        dl = mp.mpf(10)**(-k)
        rv = rstar * (1 + dl)
        rows.append((float(dl), Df(rv), Rf(rv), Kf(rv)))
        try:
            rv64 = float(rstar) * (1 + 10**(-k))
            rows64.append((10**(-k), float(Df64(rv64)),
                           float(Rf64(rv64)), float(Kf64(rv64))))
        except Exception:
            rows64.append((10**(-k), None, None, None))
    slR, rmsR = fit(rows, 'R')
    slK, rmsK = fit(rows, 'K')
    print(f"   mpmath80: R ~ D^{slR:+.4f} (rms {rmsR:.1e}), "
          f"K ~ D^{slK:+.4f} (rms {rmsK:.1e})")
    # float64 sign behavior near D~1e-7
    print("   float64 K near D->0 (delta, D, K):")
    for (dl, Dv, Rv, Kv) in rows64:
        if Dv is not None:
            print(f"      {dl:.0e}  D={Dv:+.2e}  K={Kv:+.3e}")
    k_signs = [math.copysign(1, x[3]) for x in rows64 if x[3] is not None]
    f64_flip = len(set(k_signs)) > 1
    print(f"   float64 K sign-flips: {f64_flip}")
    return slR, slK, rmsR, rmsK, f64_flip


if __name__ == '__main__':
    PASS, FAIL = [], []

    def ck(tag, cond, note=''):
        (PASS if cond else FAIL).append(tag)
        print(f"{tag}: {'PASS' if cond else 'FAIL'} {note}", flush=True)

    f0 = (1 + sp.Rational(1, 10) * sp.cos(th)**2) / r
    qs = qstar(f0, sp.Integer(1))
    slR, slK, rmsR, rmsK, flip = run_member("q* branch (tangential)", qs,
                                            sp.pi / 3)
    ck("qstar-R-exp", abs(slR - (-sp.Rational(3, 2))) < 0.1,
       f"R~D^{slR:.3f} (claim -3/2)")
    ck("qstar-K-exp", abs(slK - (-3)) < 0.15, f"K~D^{slK:.3f} (claim -3)")
    ck("qstar-clean", rmsR < 0.05 and rmsK < 0.05, "clean power law")
    ck("qstar-f64trap", flip, "float64 sign-flips (cancellation trap)")

    # generic transversal q reaching D=0 at (r0,pi/3)
    r0 = sp.Rational(10)
    f0v = (1 + sp.Rational(1, 10) * sp.Rational(1, 4)) / r0
    q0 = r0 / sp.sqrt(f0v)
    qg = q0 + sp.Rational(1, 7) * (r - r0) \
        + sp.Rational(1, 5) * (sp.cos(th)**2 - sp.Rational(1, 4))
    sR, sK, mR, mK, fl = run_member("generic transversal q", qg,
                                    sp.pi / 3, rstar_hint=10)
    ck("gen-R-exp", abs(sR - (-2)) < 0.15, f"R~D^{sR:.3f} (claim -2)")
    ck("gen-K-exp", abs(sK - (-4)) < 0.2, f"K~D^{sK:.3f} (claim -4)")
    ck("gen-clean", mR < 0.05 and mK < 0.05, "clean power law")

    print(f"\nVERIFIER CURV: {len(PASS)} PASS / {len(FAIL)} FAIL "
          f"({time.time()-t0:.0f}s)")
    for x in FAIL:
        print("FAILED:", x)
    sys.exit(0 if not FAIL else 1)
