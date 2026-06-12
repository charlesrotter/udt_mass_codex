"""
N1 script 4c: m=1 path, radial-kinetic factor fix.
<delta f_t^2> = a^2 |u'|^2 exactly (channels <R_lm^2>=1-orthonormal);
4b had an extra 0.5 on that one term (caught by pre-registered N1-P3b,
recorded FAIL; K(0) and the P sector were already exact).
"""
import numpy as np, pickle, sys
sys.path.insert(0, '/tmp/seal_s1')
from s1_potential import Quad
from scipy.special import lpmv
from math import factorial

C = pickle.load(open('/tmp/nonstat_n1/cache.pkl', 'rb'))
fine, MODES, MOUTC = C['fine'], C['MODES'], C['MOUT']
Q = Quad(800)
PASSN = []
def checkN(name, ok, detail=""):
    PASSN.append((name, bool(ok)))
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")

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
Nl = np.array([np.sqrt(2*(2*l+1)*factorial(l-1)/factorial(l+1)) for l in ls])
Rl = Nl[:, None]*np.array([lpmv(1, l, uu) for l in ls])
dRl = Nl[:, None]*np.array([((l+1)*lpmv(1, l-1, uu)
                             - l*uu*lpmv(1, l, uu))/(1-uu**2) for l in ls])

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
                               + a*a*(du1[i] @ du1[i])) + P)
        dfi = (u1[i] @ Rl)
        K += wq[i]*np.exp(-3*t)*0.25*0.5*(Q.w @ ((dfi[:, None]**2
             * cph[None, :]**2/fc**2).mean(axis=1)))
        j = np.unravel_index(np.argmin(f), f.shape)
        if f[j] < fmin: fmin = f[j]; loc = (t, uu[j[0]])
    return E, K, fmin, loc

E0, K0, _, _ = E_K_m1(0.0)
h = 0.02
Epp = (E_K_m1(+h)[0] - 2*E0 + E_K_m1(-h)[0])/h**2 + 0.5*(u1[0] @ Mo1 @ u1[0])
checkN("N1-P3c m=1 fixed kinetic: E''(0) == sigma/2",
       abs(Epp/(sig1/2) - 1) < 0.03, f"E'' {Epp:.4f} vs {sig1/2:.4f}")
checkN("N1-P4c K(0) == 1/4", abs(K0/0.25 - 1) < 0.02, f"{K0:.5f}")
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
KK = np.array([x[2] for x in tr]); fmv = np.array([x[3] for x in tr])
turned = np.any(dE < -1e-9)
Tt = np.trapezoid(np.sqrt(KK/np.maximum(dE, 1e-12)), aa)
print(f"  M2 m=1: " + (f"CORNER f_min={fmv[-1]:.3f} at (t,u)="
      f"({tr[-1][4][0]:.2f},{tr[-1][4][1]:+.2f})" if hit else "NO corner")
      + f" at a={aa[-1]:.3f}; dE_end {dE[-1]:+.3f}; turned {turned}; "
      f"T {Tt:.3f} (~{Tt*np.sqrt(sig1):.1f} e-folds)")
print("   a:  " + " ".join(f"{v:+7.3f}" for v in aa))
print("   dE: " + " ".join(f"{v:+7.3f}" for v in dE))
checkN("N1-Q3c m=1 corner at finite a, E rising, no turning point",
       hit and not turned and dE[-1] > 0)
n = sum(1 for _, ok in PASSN if ok)
print(f"\nN1-SAT-M1FIX PASS {n}/{len(PASSN)}")
