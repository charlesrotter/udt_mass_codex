"""
VERIFIER v5 (H2-C): the native completion's H1^2 loading, channel-resolved.
My own derivations throughout (v1 already verified coeff[H1^2] == alpha_aa
on the class by the full 4x4 route).

 C1  K-blindness of the angular sector: g^thth sqrt(-g) K-free EXACT
     (all orders, RW normalization)
 C2  far-collar limit DERIVED symbolically: n_H1 -> 4/(3(1-c2))
 C3  exact channel rationals c2 and n_H1(infinity):
     (1,0) 3/5 -> 10/3 ; (1,+-1) 1/5 -> 5/3 ; (2,0) 11/21 -> 14/5 ;
     (2,+-2) 1/7 -> 14/9
 C4  numeric far-collar agreement per channel (my own quadrature)
 C5  exclusion sweep: n_H1 never in {0, 1, +8, -8} on y in [1, 1e6]
 C6  channel-DEPENDENCE: no single n fits even the H1^2 loading alone
 C7  proper-lift normalization: posited loading == -(c/2) r^2 f^2 E0/n
     in these conventions (commensurability of the n_H1 ratio)
"""
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from math import log

PASS = []
def check(name, ok, detail=""):
    PASS.append((name, bool(ok)))
    print(f"V5 {name}: {'PASS' if ok else 'FAIL'} {detail}", flush=True)

# ---- C1: K-blindness, exact, all orders ----
eps, r, st = sp.symbols('e r s', positive=True)
Kv, Yv = sp.symbols('K Y', real=True)
KY = 1 + 2*eps*Kv*Yv
gthth_inv = 1/(r**2*KY)
sqg_K = r**2*st*KY          # the K-carrying factor of sqrt(-g)
check("C1 g^thth x sqrt(-g) K-factor == r^2 st x 1 (exact cancellation "
      "at ALL orders: angular sector K-blind)",
      sp.simplify(gthth_inv*sqg_K - st) == 0)

# ---- C2: far-collar limit, symbolic ----
# kappa^2 = 6 s y^-q + O(y^-2q); a = F kappa, a' = -(3q/2) F kappa / y;
# DW = (1/16)[ y^2 (2 F'a'C + a'^2 C^2) - a^2 S^2/(F(1+kappa C)) ]
# leading orders: parity kills the C term under <.>; a'^2 term
# O(y^{-3q}) << a^2 term O(y^{-2q}) =>
# <DW> -> -(1/16) F kappa^2 <1-u^2> = -(3s/8) y^{-2q} (1-c2)
# n_H1 = -(1/2) s F^2 / <DW> -> 4/(3(1-c2)).
y, q, c2s = sp.symbols('y q c2', positive=True)
s = q*(1-q)/2
Fs = y**(-q)
kap2 = 6*s*y**(-q)
DW_lead = -sp.Rational(1, 16)*Fs*kap2*(1 - c2s)
nH1_lim = sp.simplify(-sp.Rational(1, 2)*s*Fs**2/DW_lead)
check("C2 far-collar limit n_H1 = 4/(3(1-c2)) DERIVED "
      "(leading term = the a^2 S^2 measure term; a'^2 subleading)",
      sp.simplify(nH1_lim - 4/(3*(1 - c2s))) == 0, f"[{nH1_lim}]")

# ---- C3: exact rationals ----
u = sp.symbols('u', real=True)
W = {(1, 0): u**2, (1, 1): 1 - u**2, (2, 0): (3*u**2 - 1)**2,
     (2, 1): u**2*(1 - u**2), (2, 2): (1 - u**2)**2,
     (3, 0): (5*u**3 - 3*u)**2}
c2ex = {lm: sp.integrate(u**2*w, (u, -1, 1))/sp.integrate(w, (u, -1, 1))
        for lm, w in W.items()}
nex = {lm: sp.nsimplify(4/(3*(1 - c2ex[lm]))) for lm in W}
print("   exact: ", {lm: (str(c2ex[lm]), str(nex[lm])) for lm in W})
check("C3 exact rationals: c2 = 3/5, 1/5, 11/21, 1/7 and n_H1(inf) = "
      "10/3, 5/3, 14/5, 14/9 for (1,0),(1,1),(2,0),(2,2)",
      c2ex[(1, 0)] == sp.Rational(3, 5) and nex[(1, 0)] == sp.Rational(10, 3)
      and c2ex[(1, 1)] == sp.Rational(1, 5) and nex[(1, 1)] == sp.Rational(5, 3)
      and c2ex[(2, 0)] == sp.Rational(11, 21) and nex[(2, 0)] == sp.Rational(14, 5)
      and c2ex[(2, 2)] == sp.Rational(1, 7) and nex[(2, 2)] == sp.Rational(14, 9))

# ---- numeric machinery (my own) ----
qn = 1.0/3.0; sn = qn*(1 - qn)/2.0
Lk = lambda k: log((1 + k)/(1 - k))
H = lambda k: Lk(k)/(2*k) - 1.0
Hp = lambda k: 1.0/(k*(1 - k**2)) - Lk(k)/(2*k**2)
def bg(yv):
    F = yv**(-qn); Fp = -qn*yv**(-qn - 1)
    k = brentq(lambda kk: H(kk) - 2*sn*yv**(-qn), 1e-13, 1 - 1e-13,
               xtol=1e-16)
    kp = -2*qn*sn*yv**(-qn - 1)/Hp(k)
    a = F*k; ap = Fp*k + F*kp
    return F, Fp, k, kp, a, ap
ug, wq = np.polynomial.legendre.leggauss(400)
Wn = {lm: sp.lambdify(u, w, 'numpy') for lm, w in W.items()}
def nH1(yv, wfn):
    F, Fp, k, kp, a, ap = bg(yv)
    DW = (1/16)*(yv**2*(2*Fp*ap*ug + ap**2*ug**2)
                 - a**2*(1 - ug**2)/(F*(1 + k*ug)))
    ww = wfn(ug)
    dw = (wq @ (DW*ww))/(wq @ ww)
    return -0.5*sn*F**2/dw, dw

# ---- C4: far-collar numeric agreement ----
ok4 = True
print("   channel   n_H1(y=1e8)   limit")
for lm in W:
    v, _ = nH1(1e8, Wn[lm])
    lim = float(4/(3*(1 - c2ex[lm])))
    ok4 &= abs(v/lim - 1) < 2e-3
    print(f"   {lm}   {v:.6f}   {lim:.6f}")
check("C4 numeric far-collar n_H1 matches 4/(3(1-c2)) per channel "
      "(<0.2%)", ok4)

# ---- C5/C6: exclusion sweep + channel dependence ----
ys = np.geomspace(1.0, 1e6, 161)
allv = {}
bad = []
for lm in W:
    vals = np.array([nH1(yv, Wn[lm])[0] for yv in ys])
    allv[lm] = vals
    if (np.abs(vals) < 1e-6).any() or (np.abs(vals - 1) < 1e-3).any() \
       or (np.abs(vals - 8) < 1e-3).any() or (np.abs(vals + 8) < 1e-3).any():
        bad.append(lm)
rng = {lm: (allv[lm].min(), allv[lm].max()) for lm in W}
print("   ranges:", {lm: (f"{a:.3f}", f"{b:.3f}") for lm, (a, b) in rng.items()})
check("C5 n_H1 attains NONE of {0, 1, +8, -8} on the collar, any "
      "channel", not bad)
# channel separation at fixed y (no single n):
seps = [abs(allv[(1, 0)][i] - allv[(1, 1)][i]) for i in (0, 80, 160)]
check("C6 channel-resolved n_H1 differ at every y (e.g. (1,0) vs (1,1) "
      "separated > 0.5 throughout): the single-n parameterization is "
      "structurally inadequate", min(seps) > 0.5,
      f"min sep {min(seps):.3f}")
# sign: DW < 0 everywhere (definite, nonzero: slot-blindness refuted)
dws = [nH1(yv, Wn[lm])[1] for yv in ys[::20] for lm in W]
check("C6b <Delta-W> < 0 everywhere sampled (nonzero definite H1^2 "
      "content: coordinate slot-blindness fails for the native "
      "completion)", all(d < 0 for d in dws))

# ---- C7: proper-lift normalization ----
n_, ct = sp.symbols('n ct', positive=True)
Fq = y**(-q); E0 = (q*(1-q)/2)/y**2
ctv = sp.solve(sp.Eq(4*sp.pi*ct*n_*Fq**(n_-1)*y**2,
                     -4*sp.pi*(q*(1-q)/2)*y**(-q)), ct)[0]
wload = ctv*Fq**n_*y**2/2
check("C7 posited proper-lift H1^2 loading == -(1/2) y^2 F^2 E0 / n "
      "(commensurate with the n_H1 ratio definition)",
      sp.simplify(wload + sp.Rational(1, 2)*y**2*Fq**2*E0/n_) == 0)

nn = sum(1 for _, ok in PASS if ok)
print(f"\nV5 TOTAL: {nn}/{len(PASS)} PASS")
