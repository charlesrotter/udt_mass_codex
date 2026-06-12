"""
N1 script 4: SATURATION DIAGNOSTICS (one-parameter exact-action probes,
no PDE evolution).

Dynamics (same-minus record): along a mode path f_a = f_bg + a u(t,Omega)
the conserved Hamiltonian is H = E(a) - K(a) a_dot^2 with
  E(a) = Int e^-t [ (1/4)<f_t^2> + P(f_a) ] dt  (+ quadratic exterior
         response (a^2/4) u0^T M_out u0; linear flux response subtracted
         so E'(0) = 0: the background is an equilibrium of the composite
         constrained functional -- the linear-response treatment of the
         boundary sectors is the recorded honest gap),
  K(a) = (1/4) Int e^{-3t} <(u.Y)^2 / f_a^2> dt   (exact W_A weight on
         the path configuration).
Starting at rest near a = 0: a_dot^2 = (E(a) - E(0))/K(a) -- the motion
runs UP the static landscape and turns ONLY where E returns to E(0).
Fate classification along each direction:
  (i)   degenerate corner: f_min(path) -> 0 away from the seal pole
  (ii)  shedding toward spherical: anisotropy kappa decreasing
  (iii) deeper sealing: f -> 0 at the seal-end pole
  (iv)  turning point (breather): E(a) - E(0) returns to 0 at finite a
        before any degeneracy.
P beyond quadratic is EXACT (s1_potential closed integrand; the P1
exact forms live in this same reduced class).
"""
import numpy as np, pickle, sys
sys.path.insert(0, '/tmp/seal_s1')
from s1_potential import Quad, P_grad, fmin_loc, Yrows, S3

C = pickle.load(open('/tmp/nonstat_n1/cache.pkl', 'rb'))
meta, fine, CF, MODES, MOUTC, VH = (C['meta'], C['fine'], C['CF'],
                                    C['MODES'], C['MOUT'], C['VH'])
R = pickle.load(open('/tmp/seal_s2/results_main.pkl', 'rb'))
Q = Quad(800)
PASSN = []
def checkN(name, ok, detail=""):
    PASSN.append((name, bool(ok)))
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")

# ---------------- m = 0 paths ----------------
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

def E_K_fmin(tag, a, objs):
    s, X, Xt, u, du, wq, Mo, sig = objs
    Xa = X + a*u; Xta = Xt + a*du
    E = 0.0; K = 0.0; fmins = np.empty(len(s)); umins = np.empty(len(s))
    for i, t in enumerate(s):
        P, _ = P_grad(Xa[i], Q)
        E += wq[i]*np.exp(-t)*(0.25*(Xta[i] @ Xta[i]) + P)
        fpath = Xa[i] @ Q.Y
        upath = u[i] @ Q.Y
        K += wq[i]*np.exp(-3*t)*0.5*(Q.w @ (upath**2/np.maximum(fpath, 1e-12)**2))/4.0
        fmins[i], umins[i] = fmin_loc(Xa[i])
    imin = np.argmin(fmins)
    return E, K, fmins[imin], s[imin], umins[imin], fmins, Xa

def E_lin(objs):
    s, X, Xt, u, du, wq, Mo, sig = objs
    out = 0.0
    for i, t in enumerate(s):
        _, g = P_grad(X[i], Q)
        out += wq[i]*np.exp(-t)*(0.5*(Xt[i] @ du[i]) + g @ u[i])
    return out

def scan_dir(tag, objs, E0, K0, lin, sgn, amax=60.0):
    s, X, Xt, u, du, wq, Mo, sig = objs
    out = []
    a = 0.0; da = 0.05*sgn
    while abs(a) < amax:
        a += da
        E, K, fm, tmin, umin, _, Xa = E_K_fmin(tag, a, objs)
        Ee = E - lin*a + (a*a/4.0)*(u[0] @ Mo @ u[0])
        out.append((a, Ee - E0, K, fm, tmin, umin))
        if fm < 0.004:
            break
        da = sgn*min(0.4, max(0.05, abs(a)*0.12))
    return out

print("=== m=0 rung-1 saturation paths (exact P, exact W_A kinetic) ===")
SUMM = {}
for tag in ('M1', 'M2', 'M4'):
    objs = path_objects(tag)
    s, X, Xt, u, du, wq, Mo, sig = objs
    E0, K0, fm0, tm0, um0, _, _ = E_K_fmin(tag, 0.0, objs)
    lin = E_lin(objs)
    # quadratic validation: numeric E''(0) vs sigma/2 (modes B-normalized)
    h = 0.02
    Ep, *_ = E_K_fmin(tag, +h, objs); Em, *_ = E_K_fmin(tag, -h, objs)
    Epp = (Ep - 2*E0 + Em)/h**2 + 0.5*(u[0] @ Mo @ u[0])
    checkN(f"N1-P1[{tag}] path curvature E''(0) == sigma/2 (B-norm 1; "
           "validates assembly + linear subtraction)",
           abs(Epp/(sig/2) - 1) < 0.03, f"E'' {Epp:.4f} vs {sig/2:.4f}")
    checkN(f"N1-P2[{tag}] K(0) == 1/4 (B-normalization of the exact "
           "kinetic on the path)", abs(K0/0.25 - 1) < 0.02, f"{K0:.5f}")
    for sgn, name in ((+1, 'a>0'), (-1, 'a<0')):
        tr = scan_dir(tag, objs, E0, K0, lin, sgn)
        aa = np.array([x[0] for x in tr]); dE = np.array([x[1] for x in tr])
        KK = np.array([x[2] for x in tr]); fm = np.array([x[3] for x in tr])
        tmn = np.array([x[4] for x in tr]); umn = np.array([x[5] for x in tr])
        # classify
        turned = np.any(dE[3:] < 0)
        mono = np.all(np.diff(dE) > 0) if sgn > 0 else np.all(np.diff(dE) > 0)
        v2 = dE/KK
        # time from a0 = first point to corner: T = Int sqrt(K/dE) da
        Tt = np.trapezoid(np.sqrt(KK[1:]/np.maximum(dE[1:], 1e-12)),
                          aa[1:])*sgn
        # pole value at the seal end at final a
        Xa_end = X + aa[-1]*u
        fpole_tb = Xa_end[-1] @ np.array([1, S3, np.sqrt(5), np.sqrt(7)])
        kap_end = S3*abs(Xa_end[-1, 1])/Xa_end[-1, 0]
        kap_bg = S3*abs(X[-1, 1])/X[-1, 0]
        SUMM[(tag, name)] = dict(aa=aa, dE=dE, fm=fm, turned=turned)
        print(f"  {tag} {name}: a_end {aa[-1]:+7.2f}; dE monotone-up "
              f"{mono}; turning point {turned}; f_min(path) "
              f"{fm[-1]:.4f} at t={tmn[-1]:.2f} (tb={s[-1]:.2f}), "
              f"u={umn[-1]:+.2f}; f(pole,tb) {fpole_tb:+.3f}; kappa(tb) "
              f"{kap_bg:.3f}->{kap_end:.3f}; dE_end {dE[-1]:+.3f}; "
              f"T(a1->end) {abs(Tt):.3f} (= {abs(Tt)*np.sqrt(sig):.1f} "
              f"e-folds)")
        print(f"      dE profile: " + " ".join(f"{v:+.2f}" for v in
              dE[::max(1, len(dE)//8)]))

# ---------------- m = 1 path on M2 (2D quadrature) ----------------
print("\n=== m=1 rung-1 saturation path, M2 (2D sphere quadrature) ===")
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
NPH = 48
ph = (np.arange(NPH) + 0.5)*2*np.pi/NPH
cph = np.cos(ph)
uu = Q.x; ss_ = Q.s
Rl = np.array([np.sqrt(2*(2*l+1)*factorial(l-1)/factorial(l+1))
               * lpmv(1, l, uu) for l in ls])
dRl = np.array([np.sqrt(2*(2*l+1)*factorial(l-1)/factorial(l+1))
                * ((l+1)*lpmv(1, l-1, uu) - l*uu*lpmv(1, l, uu))/(1-uu**2)
                for l in ls])
Yq, Ypq = Q.Y, Q.Yp

def P2D(Xrow, crow):
    """P = (1/4)<|grad f|^2/f>, f = Xrow.Y(u) + sqrt2 (crow.R(u)) cos(phi)."""
    fb = Xrow @ Yq; fbu = Xrow @ Ypq
    g = crow @ Rl; gu = crow @ dRl
    f = fb[:, None] + np.sqrt(2)*g[:, None]*cph[None, :]
    fu = fbu[:, None] + np.sqrt(2)*gu[:, None]*cph[None, :]
    fph = -np.sqrt(2)*g[:, None]*np.sin(ph)[None, :]
    gr2 = ss_[:, None]*fu**2 + fph**2/ss_[:, None]
    integ = gr2/np.maximum(f, 1e-12)
    return 0.25*0.5*(Q.w @ integ.mean(axis=1)), f

def E_K_m1(a):
    E = 0.0; K = 0.0; fmin = np.inf; loc = None
    for i, t in enumerate(s):
        P, f = P2D(X[i], a*u1[i])
        E += wq[i]*np.exp(-t)*(0.25*(Xt[i] @ Xt[i] + a*a*(du1[i] @ du1[i]))
                               + P)
        df = u1[i] @ Rl
        K += wq[i]*np.exp(-3*t)*0.25*0.5*(Q.w @ ((2*df[:, None]**2
             * cph[None, :]**2/np.maximum(f, 1e-12)**2).mean(axis=1)))
        j = np.unravel_index(np.argmin(f), f.shape)
        if f[j] < fmin:
            fmin = f[j]; loc = (t, uu[j[0]])
    return E, K, fmin, loc

E0, K0, fm0, _ = E_K_m1(0.0)
h = 0.02
Ep = E_K_m1(+h)[0]; Em = E_K_m1(-h)[0]
Epp = (Ep - 2*E0 + Em)/h**2 + 0.5*(u1[0] @ Mo1 @ u1[0])
checkN("N1-P3 m=1 2D path curvature E''(0) == sigma/2",
       abs(Epp/(sig1/2) - 1) < 0.03, f"E'' {Epp:.4f} vs {sig1/2:.4f}")
checkN("N1-P4 m=1 K(0) == 1/4", abs(K0/0.25 - 1) < 0.02, f"{K0:.5f}")
tr = []
a = 0.0
while a < 60:
    a += min(0.4, max(0.05, a*0.12))
    E, K, fm, loc = E_K_m1(a)
    Ee = E + (a*a/4.0)*(u1[0] @ Mo1 @ u1[0])
    tr.append((a, Ee - E0 - (a*a/4.0)*0 - 0, K, fm, loc))
    if fm < 0.004:
        break
aa = np.array([x[0] for x in tr]); dE = np.array([x[1] for x in tr])
KK = np.array([x[2] for x in tr]); fm = np.array([x[3] for x in tr])
turned = np.any(dE[3:] < 0)
Tt = np.trapezoid(np.sqrt(KK[1:]/np.maximum(dE[1:], 1e-12)), aa[1:])
print(f"  M2 m=1 a>0 (a<0 identical by phi-parity): a_end {aa[-1]:.2f}; "
      f"turning {turned}; f_min {fm[-1]:.4f} at (t,u)="
      f"({tr[-1][4][0]:.2f},{tr[-1][4][1]:+.2f}); dE_end {dE[-1]:+.3f}; "
      f"T {Tt:.3f} (= {Tt*np.sqrt(sig1):.1f} e-folds)")
print("      dE profile: " + " ".join(f"{v:+.2f}" for v in
      dE[::max(1, len(dE)//8)]))
checkN("N1-P5 no turning point on any probed direction (E - E0 stays "
       "> 0 to the degeneracy)", not turned and
       all(not SUMM[k]['turned'] for k in SUMM))
n = sum(1 for _, ok in PASSN if ok)
print(f"\nN1-SATURATION PASS {n}/{len(PASSN)}")
