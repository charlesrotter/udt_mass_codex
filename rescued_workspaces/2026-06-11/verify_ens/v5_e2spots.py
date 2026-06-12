"""VERIFIER script 5: E2 spot checks with a FRESH ell<=3 engine (own
potential quadrature, own cubic minimizer, own event/threshold code).
Conventions: S1 frozen set (orthonormal Y0..Y3, P = (1/8)Int(1-u^2)f_u^2/f,
EL X_tt - X_t = 2P_X, jet X=(1+eps, eps1, 0, 0),
X_t=(gamma+p*eps, -c-eps1, 0, 0), fstop = 0.02 ABS, DOP853 rtol 1e-11
atol 1e-13 max_step 0.05).
Spots: C1 partials + composition; C4 crowd-out case + reorientation;
C5/C3 M2 action derivatives; weld flux numbers."""
import numpy as np, time
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from multiprocessing import Pool

S3, S5, S7 = np.sqrt(3.), np.sqrt(5.), np.sqrt(7.)
NGL = 800
ug, wg = np.polynomial.legendre.leggauss(NGL)
Y = np.array([np.ones_like(ug), S3*ug, (S5/2)*(3*ug**2 - 1),
              (S7/2)*(5*ug**3 - 3*ug)])
Yp = np.array([np.zeros_like(ug), S3*np.ones_like(ug), 3*S5*ug,
               (S7/2)*(15*ug**2 - 3)])
sw = (1 - ug**2)

def P_grad(X):
    f = X @ Y
    fu = X @ Yp
    fc = np.where(f > 1e-300, f, 1e-300)
    P = np.dot(wg, sw*fu**2/fc)/8.0
    g = ((sw*(2*fu/fc))[None, :]*Yp - (sw*fu**2/fc**2)[None, :]*Y) @ wg/8.0
    return P, g

def fmin_cubic(X):
    F, a, g2, h3 = X
    cands = [(-1.0, F - S3*a + S5*g2 - S7*h3), (1.0, F + S3*a + S5*g2 + S7*h3)]
    A = 7.5*S7*h3; B = 3*S5*g2; C = S3*a - 1.5*S7*h3
    if abs(A) > 1e-15:
        disc = B*B - 4*A*C
        if disc >= 0:
            for r in ((-B + np.sqrt(disc))/(2*A), (-B - np.sqrt(disc))/(2*A)):
                if -1 < r < 1:
                    yv = np.array([1, S3*r, (S5/2)*(3*r**2-1), (S7/2)*(5*r**3-3*r)])
                    cands.append((r, float(X @ yv)))
    elif abs(B) > 1e-15:
        r = -C/B
        if -1 < r < 1:
            yv = np.array([1, S3*r, (S5/2)*(3*r**2-1), (S7/2)*(5*r**3-3*r)])
            cands.append((r, float(X @ yv)))
    um, fm = min(cands, key=lambda t: t[1])[0], min(c[1] for c in cands)
    for r, v in cands:
        if v == fm: um = r
    return fm, um

def rhs(t, z):
    X = z[0::2]
    _, g = P_grad(X)
    dz = np.empty(8)
    dz[0::2] = z[1::2]
    dz[1::2] = z[1::2] + 2*g
    return dz

def run(gamma, c, eps=0.0, p=0.0, eps1=0.0, fstop=0.02, Tmax=120.0,
        dense=False):
    z0 = [1.0+eps, gamma+p*eps, eps1, -c-eps1, 0.0, 0.0, 0.0, 0.0]
    def ev(t, z):
        return fmin_cubic(z[0::2])[0] - fstop
    ev.terminal = True; ev.direction = -1
    sol = solve_ivp(rhs, (0, Tmax), z0, method='DOP853', rtol=1e-11,
                    atol=1e-13, events=ev, max_step=0.05, dense_output=dense)
    return sol, len(sol.t_events[0]) > 0

def cstar(gamma, eps=0.0, p=0.0, eps1=0.0, lo=0.05, hi=0.30, xtol=2e-6):
    f = lambda c: 1.0 if run(gamma, c, eps, p, eps1)[1] else -1.0
    return brentq(f, lo, hi, xtol=xtol)

def action(sol, t_end, n=3000):
    x, w = np.polynomial.legendre.leggauss(n)
    tt = 0.5*t_end*(x + 1); ww = 0.5*t_end*w
    Z = sol.sol(tt)
    Xs = Z[0::2]; Xts = Z[1::2]
    Ps = np.array([P_grad(Xs[:, i])[0] for i in range(len(tt))])
    return float(ww @ (np.exp(-tt)*(0.25*np.sum(Xts**2, axis=0) + Ps)))

def flux_weld(z0):
    X = np.array(z0[0::2]); Xt = np.array(z0[1::2])
    f = X @ Y; ft = Xt @ Y; fu = X @ Yp
    fy = -ft
    L = 0.25*(fy**2 + sw*fu**2/f)
    integ = 0.5*fy*(ug*fy + sw*fu) - ug*L
    return 0.5*np.dot(wg, integ)

def measure(gamma, c, eps=0.0, p=0.0, eps1=0.0, want_action=True):
    sol, sealed = run(gamma, c, eps, p, eps1, dense=True)
    out = dict(sealed=sealed)
    if not sealed:
        return out
    t_stop = sol.t_events[0][0]
    zs = sol.sol(t_stop); Xs = zs[0::2]; Xts = zs[1::2]
    mu, um = fmin_cubic(Xs)
    Ypl = np.array([1.0, S3*um, (S5/2)*(3*um**2-1), (S7/2)*(5*um**3-3*um)])
    mu_t = float(Xts @ Ypl)
    out.update(t_stop=t_stop, t_seal=t_stop + mu/abs(mu_t),
               umin=um, kap=S3*abs(Xs[1])/Xs[0])
    out['y_seal'] = np.exp(-out['t_seal'])
    if want_action:
        S02 = action(sol, t_stop)
        def fmina(t): return fmin_cubic(sol.sol(t)[0::2])[0]
        t04 = brentq(lambda t: fmina(t) - 0.04, 0.3*t_stop, t_stop)
        S04 = action(sol, t04)
        out['S'] = 2*S02 - S04
    z0 = [1.0+eps, gamma+p*eps, eps1, -c-eps1, 0.0, 0.0, 0.0, 0.0]
    out['Fz_weld'] = flux_weld(z0)
    return out

def job(arg):
    kind = arg[0]
    if kind == 'cs':
        _, gamma, eps, p, lo, hi = arg
        return arg, cstar(gamma, eps=eps, p=p, lo=lo, hi=hi)
    if kind == 'epstar':
        _, gamma, c, p, lo, hi = arg
        f = lambda e: 1.0 if run(gamma, c, eps=e, p=p)[1] else -1.0
        return arg, brentq(f, lo, hi, xtol=1e-5)
    if kind == 'meas':
        _, gamma, c, eps, p, eps1, wa = arg
        return arg, measure(gamma, c, eps, p, eps1, want_action=wa)

if __name__ == '__main__':
    t0 = time.time()
    PASS = FAIL = 0
    def check(name, ok, extra=""):
        global PASS, FAIL
        PASS += ok; FAIL += (not ok)
        print(("PASS" if ok else "FAIL") + f"  {name}"
              + (f"  [{extra}]" if extra else ""), flush=True)

    jobs = [
        ('cs', 1.0, 0.0, 0.0, 0.08, 0.25),       # baseline
        ('cs', 0.98, 0.0, 0.0, 0.08, 0.25),
        ('cs', 1.02, 0.0, 0.0, 0.08, 0.25),
        ('cs', 1.0, -0.01, 0.0, 0.08, 0.25),
        ('cs', 1.0, 0.01, 0.0, 0.08, 0.25),
        ('cs', 1.0, -0.01, 1.0, 0.08, 0.25),
        ('cs', 1.0, 0.01, 1.0, 0.08, 0.25),
        ('epstar', 1.0, 0.18413678, 1.0, 0.10, 0.20),
        ('meas', 1.0, 0.18413678, 0.0, 0.0, 0.0, True),     # M1 baseline
        ('meas', 1.0, 0.28328735, 0.0, 0.0, 0.0, True),     # M2 baseline
        ('meas', 1.0, 0.28328735, 0.005, 0.0, 0.0, True),
        ('meas', 1.0, 0.28328735, -0.005, 0.0, 0.0, True),
        ('meas', 1.0, 0.28328735, 0.0, 0.0, 0.01, True),
        ('meas', 1.0, 0.28328735, 0.0, 0.0, -0.01, True),
        ('meas', 1.0, 0.28328735, 0.0, 0.0, 0.005, True),
        ('meas', 1.0, 0.28328735, 0.0, 0.0, -0.005, True),
        ('meas', 0.5, 0.09087158, 0.0, 0.0, 0.4, False),    # reorientation g=.5
        ('meas', 1.0, 0.18413678, 0.0, 0.0, 0.4, False),    # off-pole 1.3c*
        ('meas', 1.0, 0.18413678, 0.13, 1.0, 0.0, False),   # dive pre-crowdout
        ('meas', 1.0, 0.18413678, 0.145, 1.0, 0.0, False),  # nearer the edge
    ]
    with Pool(8) as pool:
        out = dict(pool.map(job, jobs))

    cs0 = out[('cs', 1.0, 0.0, 0.0, 0.08, 0.25)]
    check("V5.1 c*_3(1) = 0.14165 (banked / E2 0.141653)",
          abs(cs0 - 0.141653) < 2e-4, f"{cs0:.6f}")
    dcdg = (out[('cs', 1.02, 0.0, 0.0, 0.08, 0.25)]
            - out[('cs', 0.98, 0.0, 0.0, 0.08, 0.25)])/0.04
    check("V5.2 dc*/dgamma = +0.2248", abs(dcdg - 0.22483) < 3e-3,
          f"{dcdg:+.5f}")
    s0 = (out[('cs', 1.0, 0.01, 0.0, 0.08, 0.25)]
          - out[('cs', 1.0, -0.01, 0.0, 0.08, 0.25)])/0.02
    check("V5.3 dc*/deps|p=0 = +0.0542", abs(s0 - 0.05426) < 2e-3, f"{s0:+.5f}")
    s1 = (out[('cs', 1.0, 0.01, 1.0, 0.08, 0.25)]
          - out[('cs', 1.0, -0.01, 1.0, 0.08, 0.25)])/0.02
    check("V5.4 dc*/deps|p=1 = +0.2790 AND composition p*dcdg + s0",
          abs(s1 - 0.27905) < 3e-3 and abs(s1 - (dcdg + s0)) < 2e-3,
          f"{s1:+.5f} vs composed {dcdg + s0:+.5f}")

    es = out[('epstar', 1.0, 0.18413678, 1.0, 0.10, 0.20)]
    check("V5.5 crowd-out eps*(1.3c*, p=1) = 0.14566", abs(es - 0.14566) < 1e-3,
          f"{es:.5f}")
    # threshold-crossing identity: c*(eps*, p=1) == c_driver
    csb = cstar(1.0, eps=es, p=1.0, lo=0.10, hi=0.28)
    check("V5.6 crowd-out IS the shifted formation threshold: "
          "c*(eps*, p=1) = 0.184137", abs(csb - 0.18413678) < 5e-5,
          f"{csb:.6f}")

    m13 = out[('meas', 1.0, 0.18413678, 0.13, 1.0, 0.0, False)]
    m145 = out[('meas', 1.0, 0.18413678, 0.145, 1.0, 0.0, False)]
    b1 = out[('meas', 1.0, 0.18413678, 0.0, 0.0, 0.0, True)]
    check("V5.7 dive-before-failing: t_seal grows toward eps* "
          "(baseline -> 0.13 -> 0.145, still sealed)",
          m13['sealed'] and m145['sealed']
          and b1['t_seal'] < m13['t_seal'] < m145['t_seal'],
          f"t_seal {b1['t_seal']:.3f} -> {m13['t_seal']:.3f} -> "
          f"{m145['t_seal']:.3f}")

    r05 = out[('meas', 0.5, 0.09087158, 0.0, 0.0, 0.4, False)]
    check("V5.8 seal reorientation at eps1=+0.4, gamma=0.5: umin = -1 (flip)",
          r05['sealed'] and r05['umin'] < -0.99,
          f"umin = {r05.get('umin', np.nan):+.3f}, kap {r05.get('kap', np.nan):.3f}")
    r13 = out[('meas', 1.0, 0.18413678, 0.0, 0.0, 0.4, False)]
    print(f"   1.3c* eps1=+0.4: sealed={r13['sealed']}, "
          f"umin={r13.get('umin', np.nan):+.3f} (E2 logged +0.75 off-pole)")

    # M1/M2 baselines and action spots
    check("V5.9 M1 baseline t_seal 3.5988, S 10.2185, Fz_weld -0.053156",
          abs(b1['t_seal'] - 3.598790) < 2e-3 and abs(b1['S'] - 10.218465) < 2e-2
          and abs(b1['Fz_weld'] + 0.053156) < 1e-6,
          f"t_seal {b1['t_seal']:.6f}, S {b1['S']:.5f}, Fz {b1['Fz_weld']:+.6f}")
    b2 = out[('meas', 1.0, 0.28328735, 0.0, 0.0, 0.0, True)]
    check("V5.10 M2 baseline t_seal 2.1345, S 2.34927",
          abs(b2['t_seal'] - 2.134533) < 2e-3 and abs(b2['S'] - 2.349270) < 5e-3,
          f"t_seal {b2['t_seal']:.6f}, S {b2['S']:.6f}")
    Sp = out[('meas', 1.0, 0.28328735, 0.005, 0.0, 0.0, True)]['S']
    Sm = out[('meas', 1.0, 0.28328735, -0.005, 0.0, 0.0, True)]['S']
    d1 = (Sp - Sm)/0.01
    check("V5.11 M2 dS/deps|p=0 = +2.717 (the C3 meet-test number; "
          "pre-registered meet wanted -gamma/2 = -0.5)",
          abs(d1 - 2.71704) < 0.05, f"{d1:+.5f}")
    St = {e: out[('meas', 1.0, 0.28328735, 0.0, 0.0, e, True)]['S']
          for e in (-0.01, -0.005, 0.005, 0.01)}
    t2 = (St[0.01] + St[-0.01] - 2*b2['S'])/1e-4
    t1 = (St[0.005] - St[-0.005])/0.01
    check("V5.12 M2 tidal: dS/de1 = +2.26, d2S/de1^2 = -53.2 (E2 printed "
          "-26.6 = half-curvature convention; claimed -53)",
          abs(t1 - 2.2567) < 0.08 and abs(t2 + 53.2) < 6,
          f"dS/de1 {t1:+.4f}, d2S/de1^2 {t2:+.2f}")
    kt = {e: out[('meas', 1.0, 0.28328735, 0.0, 0.0, e, True)]['kap']
          for e in (-0.005, 0.005)}
    check("V5.13 M2 dkap/de1 = +0.5515",
          abs((kt[0.005] - kt[-0.005])/0.01 - 0.5515) < 0.02,
          f"{(kt[0.005]-kt[-0.005])/0.01:+.4f}")
    Fzt = {e: out[('meas', 1.0, 0.28328735, 0.0, 0.0, e, True)]['Fz_weld']
           for e in (-0.005, 0.005)}
    check("V5.14 M2 dFz_weld/de1 = -sqrt3/2 (numeric vs exact closed form)",
          abs((Fzt[0.005] - Fzt[-0.005])/0.01 + np.sqrt(3)/2) < 1e-4,
          f"{(Fzt[0.005]-Fzt[-0.005])/0.01:+.6f}")

    print(f"\n=== V5 TOTALS: {PASS} PASS / {FAIL} FAIL ===  "
          f"[{time.time()-t0:.0f}s]")
