"""
N1 script 4b: SATURATION DIAGNOSTICS, corrected run.
Fixes over n1_saturation.py (recorded):
  (F1) corner overshoot: the scan stepped past f = 0 and reported the
       1e-12-floor garbage energy; now bisect the path endpoint to
       f_min(path) ~= 0.012 and report diagnostics THERE.
  (F2) m=1 basis: S2's implemented real-harmonic normalization is
       R_lm = N_lm P_l^m cos(m phi)  (pref = 0.5 N N' in s2_blocks +
       its own <R^2>=1 check pin this; the header's sqrt2 wording is
       loose). First run used an extra sqrt2 => K(0)=0.5 and E''(0)
       1.34x high (both caught by the pre-registered checks N1-P3/P4,
       recorded FAIL). Corrected here.
"""
import numpy as np, pickle, sys
sys.path.insert(0, '/tmp/seal_s1')
from s1_potential import Quad, P_grad, fmin_loc, S3

C = pickle.load(open('/tmp/nonstat_n1/cache.pkl', 'rb'))
meta, fine, CF, MODES, MOUTC, VH = (C['meta'], C['fine'], C['CF'],
                                    C['MODES'], C['MOUT'], C['VH'])
Q = Quad(800)
PASSN = []
def checkN(name, ok, detail=""):
    PASSN.append((name, bool(ok)))
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")

YP = np.array([1, S3, np.sqrt(5), np.sqrt(7)])

def path_objects(tag):
    dd = MODES[(tag, 0)]
    u = dd['modes'][0]; s = dd['sgrid']; sig = dd['sig'][0]
    ft, fX, fXt = fine[tag]['t'], fine[tag]['X'], fine[tag]['Xt']
    X = np.array([np.interp(s, ft, fX[:, j]) for j in range(4)]).T
    Xt = np.array([np.interp(s, ft, fXt[:, j]) for j in range(4)]).T
    du = np.gradient(u, s, axis=0)
    wq = np.full(len(s), s[1]-s[0]); wq[0] *= 0.5; wq[-1] *= 0.5
    Mo = MOUTC[tag][0]['scr']
    return s, X, Xt, u, du, wq, Mo, sig

def E_K_fmin(a, objs):
    s, X, Xt, u, du, wq, Mo, sig = objs
    Xa = X + a*u; Xta = Xt + a*du
    E = K = 0.0; fmins = np.empty(len(s)); umins = np.empty(len(s))
    for i, t in enumerate(s):
        P, _ = P_grad(Xa[i], Q)
        E += wq[i]*np.exp(-t)*(0.25*(Xta[i] @ Xta[i]) + P)
        fpath = np.maximum(Xa[i] @ Q.Y, 1e-9)
        upath = u[i] @ Q.Y
        K += wq[i]*np.exp(-3*t)*0.5*(Q.w @ (upath**2/fpath**2))/4.0
        fmins[i], umins[i] = fmin_loc(Xa[i])
    i0 = np.argmin(fmins)
    return E, K, fmins[i0], s[i0], umins[i0]

def E_lin(objs):
    s, X, Xt, u, du, wq, Mo, sig = objs
    out = 0.0
    for i, t in enumerate(s):
        _, g = P_grad(X[i], Q)
        out += wq[i]*np.exp(-t)*(0.5*(Xt[i] @ du[i]) + g @ u[i])
    return out

def scan_dir(tag, objs, E0, lin, sgn, amax=60.0, ftarg=0.012):
    s, X, Xt, u, du, wq, Mo, sig = objs
    bnd = 0.25*(u[0] @ Mo @ u[0])
    out = []; a_prev = 0.0
    a = 0.0
    while abs(a) < amax:
        da = sgn*min(0.4, max(0.02, abs(a)*0.12))
        E, K, fm, tmin, umin = E_K_fmin(a + da, objs)
        if fm < ftarg:        # bisect endpoint to ftarg
            lo, hi = a, a + da
            for _ in range(40):
                mid = 0.5*(lo + hi)
                fmm = E_K_fmin(mid, objs)[2]
                if fmm > ftarg: lo = mid
                else: hi = mid
            a = lo
            E, K, fm, tmin, umin = E_K_fmin(a, objs)
            out.append((a, E - lin*a + bnd*a*a - E0, K, fm, tmin, umin))
            return out, True
        a = a + da
        out.append((a, E - lin*a + bnd*a*a - E0, K, fm, tmin, umin))
    return out, False

print("=== m=0 rung-1 saturation paths (corrected endpoints) ===")
for tag in ('M1', 'M2', 'M4'):
    objs = path_objects(tag)
    s, X, Xt, u, du, wq, Mo, sig = objs
    E0 = E_K_fmin(0.0, objs)[0]
    lin = E_lin(objs)
    for sgn, name in ((+1, 'a>0'), (-1, 'a<0')):
        tr, hit = scan_dir(tag, objs, E0, lin, sgn)
        aa = np.array([x[0] for x in tr]); dE = np.array([x[1] for x in tr])
        KK = np.array([x[2] for x in tr]); fm = np.array([x[3] for x in tr])
        turned = np.any(dE < -1e-9)
        mono = np.all(np.diff(np.abs(aa)) > 0) and np.all(np.diff(dE) > 0)
        Tt = abs(np.trapezoid(np.sqrt(KK/np.maximum(dE, 1e-12)), aa))
        Xe = X + aa[-1]*u
        kap0 = S3*abs(X[-1, 1])/X[-1, 0]
        kape = S3*abs(Xe[-1, 1])/Xe[-1, 0]
        tail = (f"CORNER f_min={fm[-1]:.3f} at t={tr[-1][4]:.2f}, "
                f"u={tr[-1][5]:+.2f}" if hit else
                f"NO corner by a={aa[-1]:+.1f} (f_min={fm[-1]:.2f} rising)")
        print(f"  {tag} {name}: {tail}; dE_end {dE[-1]:+.3f}; E monotone "
              f"up {mono}; turned {turned}; kappa(tb) {kap0:.3f}->"
              f"{kape:.3f}; f(pole,tb) {Xe[-1] @ YP:+.3f}; "
              f"T(path) {Tt:.3f} (~{Tt*np.sqrt(sig):.1f} e-folds)")
        print("      a:  " + " ".join(f"{v:+7.2f}" for v in
              aa[::max(1, len(aa)//7)]))
        print("      dE: " + " ".join(f"{v:+7.3f}" for v in
              dE[::max(1, len(aa)//7)]))
        if name == 'a<0':
            checkN(f"N1-Q1[{tag}] corner reached on a<0 at finite a with "
                   "E still rising (terminal runaway, no turning point)",
                   hit and not turned and dE[-1] > 0,
                   f"a_c={aa[-1]:+.3f}, dE_c={dE[-1]:+.3f}")
        else:
            checkN(f"N1-Q2[{tag}] a>0: no turning point; amplitude "
                   "inflation with kappa decreasing (spheroidalizing "
                   "dissolution direction)", (not turned) and kape < kap0)

# ---------------- m=1, corrected basis ----------------
print("\n=== m=1 rung-1 path, M2, corrected R = N P cos(phi) basis ===")
from scipy.special import lpmv
from math import factorial
tag = 'M2'
dd = MODES[(tag, 1)]
u1 = dd['modes'][0]; s = dd['sgrid']; sig1 = dd['sig'][0]
ls = C['LBLK'][1]
ft, fX, fXt = fine[tag]['t'], fine[tag]['X'], fine[tag]['Xt']
X = np.array([np.interp(s, ft, fX[:, j]) for j in range(4)]).T
Xt = np.array([np.interp(s, ft, fXt[:, j]) for j in range(4)]).T
du1 = np.gradient(u1, s, axis=0)
wq = np.full(len(s), s[1]-s[0]); wq[0] *= 0.5; wq[-1] *= 0.5
Mo1 = MOUTC[tag][1]['scr']
NPH = 64
ph = (np.arange(NPH) + 0.5)*2*np.pi/NPH
cph, sph = np.cos(ph), np.sin(ph)
uu, ss_ = Q.x, Q.s
Nl = np.array([np.sqrt(2*(2*l+1)*factorial(l-1)/factorial(l+1))
               for l in ls])
Pl = np.array([lpmv(1, l, uu) for l in ls])
dPl = np.array([((l+1)*lpmv(1, l-1, uu) - l*uu*lpmv(1, l, uu))/(1-uu**2)
                for l in ls])
Rl = Nl[:, None]*Pl; dRl = Nl[:, None]*dPl

def E_K_m1(a):
    E = K = 0.0; fmin = np.inf; loc = None
    for i, t in enumerate(s):
        fb = X[i] @ Q.Y; fbu = X[i] @ Q.Yp
        g = (a*u1[i]) @ Rl; gu = (a*u1[i]) @ dRl
        f = fb[:, None] + g[:, None]*cph[None, :]
        fu = fbu[:, None] + gu[:, None]*cph[None, :]
        fph = -g[:, None]*sph[None, :]
        fc = np.maximum(f, 1e-9)
        gr2 = ss_[:, None]*fu**2 + fph**2/ss_[:, None]
        P = 0.25*0.5*(Q.w @ (gr2/fc).mean(axis=1))
        E += wq[i]*np.exp(-t)*(0.25*(Xt[i] @ Xt[i]
                               + 0.5*a*a*(du1[i] @ du1[i])) + P)
        dfi = (u1[i] @ Rl)
        K += wq[i]*np.exp(-3*t)*0.25*0.5*(Q.w @ ((dfi[:, None]**2
             * cph[None, :]**2/fc**2).mean(axis=1)))
        j = np.unravel_index(np.argmin(f), f.shape)
        if f[j] < fmin: fmin = f[j]; loc = (t, uu[j[0]])
    return E, K, fmin, loc

# NOTE the kinetic: <(d_T delta f)^2> = (a_dot^2/2)|u'... for the path
# variable: delta f = a * (u1.Rl) cos(phi); <cos^2> = 1/2 and <Rl Rl'>
# carries the 1/2 already via the B-normalization -- validated by the
# two checks below (the only purpose of the 0.5 factors).
E0, K0, fm0, _ = E_K_m1(0.0)
h = 0.02
Ep = E_K_m1(+h)[0]; Em = E_K_m1(-h)[0]
Epp = (Ep - 2*E0 + Em)/h**2 + 0.5*(u1[0] @ Mo1 @ u1[0])
checkN("N1-P3b m=1 corrected basis: E''(0) == sigma/2",
       abs(Epp/(sig1/2) - 1) < 0.03, f"E'' {Epp:.4f} vs {sig1/2:.4f}")
checkN("N1-P4b m=1 corrected basis: K(0) == 1/4",
       abs(K0/0.25 - 1) < 0.02, f"{K0:.5f}")
bnd1 = 0.25*(u1[0] @ Mo1 @ u1[0])
tr = []; a = 0.0; hit = False
while a < 60:
    da = min(0.4, max(0.02, a*0.12))
    E, K, fm, loc = E_K_m1(a + da)
    if fm < 0.012:
        lo, hi = a, a + da
        for _ in range(40):
            mid = 0.5*(lo + hi)
            if E_K_m1(mid)[2] > 0.012: lo = mid
            else: hi = mid
        a = lo; E, K, fm, loc = E_K_m1(a)
        tr.append((a, E + bnd1*a*a - E0, K, fm, loc)); hit = True
        break
    a += da
    tr.append((a, E + bnd1*a*a - E0, K, fm, loc))
aa = np.array([x[0] for x in tr]); dE = np.array([x[1] for x in tr])
KK = np.array([x[2] for x in tr]); fm = np.array([x[3] for x in tr])
turned = np.any(dE < -1e-9)
Tt = np.trapezoid(np.sqrt(KK/np.maximum(dE, 1e-12)), aa)
print(f"  M2 m=1 (a<0 = mirror by phi-parity): "
      + (f"CORNER f_min={fm[-1]:.3f} at (t,u)=({tr[-1][4][0]:.2f},"
         f"{tr[-1][4][1]:+.2f})" if hit else "NO corner")
      + f" at a={aa[-1]:.3f}; dE_end {dE[-1]:+.3f}; turned {turned}; "
      f"T {Tt:.3f} (~{Tt*np.sqrt(sig1):.1f} e-folds)")
print("      a:  " + " ".join(f"{v:+7.3f}" for v in aa[::max(1,len(aa)//7)]))
print("      dE: " + " ".join(f"{v:+7.3f}" for v in dE[::max(1,len(aa)//7)]))
checkN("N1-Q3 m=1: corner at finite a, E rising, no turning point "
       "(off-axis f->0: tilt/reorientation runaway hits degeneracy)",
       hit and not turned and dE[-1] > 0)
n = sum(1 for _, ok in PASSN if ok)
print(f"\nN1-SATURATION-2 PASS {n}/{len(PASSN)}")
