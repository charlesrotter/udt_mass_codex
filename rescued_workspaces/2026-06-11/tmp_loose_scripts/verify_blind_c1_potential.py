"""BLIND VERIFIER C1: exact reduced potential P(F,a), homogeneity, rank-1, Hessian.

Conventions under test (the derivation agent's, reconstructed):
  f(y,th) = F(y)(1 + kappa cos th),  kappa = (a/F)*sqrt(3/4pi)  [a = Y_10 coeff]
  P(F,a) := sphere-integrated angular term  Int dOmega |grad_Omega f|^2 / f
  claimed P = (3 a^2 / 2F) G1(kappa),  G1 = (2k + (k^2-1)L)/k^3, L = ln((1+k)/(1-k))
  V_ij := (1/4) d^2 P / dc_i dc_j  with u = UNIFORM shift dF (not Y00 coeff),
          a0 = Y10 coeff.
  claimed: V_uu = (pi/k) W / F, V_ua0 = -(sqrt(3pi)/(2k^2)) W/F,
           V_a0a0 = (3/(4k^3)) W/F, V_a1a1 = (3/(8k^3)) U/F,
           W = 2k/(1-k^2) - L, U = (1+k^2)L - 2k.
"""
import numpy as np
import mpmath as mp
from scipy import integrate
mp.mp.dps = 30

c = np.sqrt(3.0/(4.0*np.pi))   # Y10 = c cos(theta)

def L_(k): return np.log((1+k)/(1-k))
def G1(k): return (2*k + (k*k-1)*L_(k))/k**3
def W_(k): return 2*k/(1-k*k) - L_(k)
def U_(k): return (1+k*k)*L_(k) - 2*k

# ---------- exact functional via 2D quadrature ----------
# real harmonics used: Y00, Y10, Y11r, Y20, Y21r, Y22r
def Y(lm, th, ph):
    x = np.cos(th)
    if lm == 'Y00': return 0.5/np.sqrt(np.pi) + 0*th
    if lm == 'Y10': return np.sqrt(3/(4*np.pi))*x
    if lm == 'Y11': return np.sqrt(3/(4*np.pi))*np.sin(th)*np.cos(ph)
    if lm == 'Y20': return np.sqrt(5/(16*np.pi))*(3*x*x-1)
    if lm == 'Y21': return np.sqrt(15/(4*np.pi))*np.sin(th)*x*np.cos(ph)
    if lm == 'Y22': return np.sqrt(15/(16*np.pi))*np.sin(th)**2*np.cos(2*ph)
    raise ValueError

def dY_dth(lm, th, ph):
    x, s = np.cos(th), np.sin(th)
    if lm == 'Y00': return 0*th
    if lm == 'Y10': return -np.sqrt(3/(4*np.pi))*s
    if lm == 'Y11': return np.sqrt(3/(4*np.pi))*x*np.cos(ph)
    if lm == 'Y20': return np.sqrt(5/(16*np.pi))*(-6*x*s)
    if lm == 'Y21': return np.sqrt(15/(4*np.pi))*(x*x - s*s)*np.cos(ph)
    if lm == 'Y22': return np.sqrt(15/(16*np.pi))*2*s*x*np.cos(2*ph)
    raise ValueError

def dY_dph(lm, th, ph):
    x, s = np.cos(th), np.sin(th)
    if lm in ('Y00','Y10','Y20'): return 0*th
    if lm == 'Y11': return -np.sqrt(3/(4*np.pi))*s*np.sin(ph)
    if lm == 'Y21': return -np.sqrt(15/(4*np.pi))*s*x*np.sin(ph)
    if lm == 'Y22': return -np.sqrt(15/(16*np.pi))*s*s*2*np.sin(2*ph)
    raise ValueError

MODES = ['Y00','Y10','Y11','Y20','Y21','Y22']

def Qfunc(F, kappa, coeffs):
    """Int dOmega |grad f|^2/f with f = F(1+kappa cos th) + sum coeffs[lm] Y_lm."""
    def integrand(th, ph):
        f   = F*(1+kappa*np.cos(th))
        fth = -F*kappa*np.sin(th)
        fph = 0.0
        for lm, cc in coeffs.items():
            f   = f   + cc*Y(lm, th, ph)
            fth = fth + cc*dY_dth(lm, th, ph)
            fph = fph + cc*dY_dph(lm, th, ph)
        s = np.sin(th)
        grad2 = fth**2 + (fph/np.where(s == 0, 1, s))**2
        return grad2/f*s
    val, err = integrate.dblquad(integrand, 0, 2*np.pi, 0, np.pi,
                                 epsabs=1e-12, epsrel=1e-12)
    return val

print("=== C1.1 exact reduced potential P(F,a) = (3a^2/2F) G1(kappa) ===")
fails = 0
for F, k in [(1.0,0.1),(1.0,0.5),(2.0,0.7),(0.5,0.9),(3.0,0.99)]:
    a = k*F/c
    Pq = Qfunc(F, k, {})
    Pc = (3*a*a/(2*F))*G1(k)
    ok = abs(Pq-Pc) < 1e-8*max(1, abs(Pc))
    fails += (not ok)
    print(f"  F={F} k={k}: quad={Pq:.12f} claimed={Pc:.12f} {'OK' if ok else 'FAIL'}")

print("\n=== C1.2 degree-1 homogeneity P(lam F, lam a) = lam P(F,a) ===")
for lam in [0.5, 2.0, 7.3]:
    F, k = 1.3, 0.6; a = k*F/c
    P1 = (3*a*a/(2*F))*G1(k)
    P2 = (3*(lam*a)**2/(2*lam*F))*G1(k)   # kappa invariant under scaling
    ok = abs(P2 - lam*P1) < 1e-12
    fails += (not ok)
    print(f"  lam={lam}: {'OK' if ok else 'FAIL'}")

print("\n=== C1.3 Hessian entries via finite differences of exact functional ===")
def hess_entry(F, k, m1, m2, h=1e-4):
    """(1/4) d2 Q/dc1 dc2 ; m='u' means uniform shift of F (kappa fixed a => recompute)."""
    a = k*F/c
    def Qof(d1, d2):
        dd = {}
        FF = F
        for m, d in ((m1, d1), (m2, d2)):
            if m == 'u':
                FF = FF + d
            else:
                dd[m] = dd.get(m, 0.0) + d
        kk = c*a/FF   # background a fixed; uniform shift changes F hence kappa
        return Qfunc(FF, kk, dd)
    if m1 == m2:
        v = (Qof(h, 0) - 2*Qof(0, 0) + Qof(-h, 0))/h**2 if m1 == 'u' else \
            (Qfunc(F, k, {m1: h}) - 2*Qfunc(F, k, {}) + Qfunc(F, k, {m1: -h}))/h**2
    else:
        v = (Qof(h, h) - Qof(h, -h) - Qof(-h, h) + Qof(-h, -h))/(4*h*h)
    return v/4.0

F, k = 1.7, 0.55
a = k*F/c
W, U = W_(k), U_(k)
claims = {
    ('u','u'):     np.pi/k*W/F,
    ('u','Y10'):  -np.sqrt(3*np.pi)/(2*k*k)*W/F,
    ('Y10','Y10'): 3/(4*k**3)*W/F,
    ('Y11','Y11'): 3/(8*k**3)*U/F,
}
H = {}
for (m1, m2), cl in claims.items():
    v = hess_entry(F, k, m1, m2)
    H[(m1, m2)] = v
    ok = abs(v-cl) < 1e-5*max(1, abs(cl))
    fails += (not ok)
    print(f"  V_{m1},{m2}: fd={v:.10f} claimed={cl:.10f} {'OK' if ok else 'FAIL'}")

print("\n=== C1.4 rank-1 identity V_uu V_a0a0 - V_ua0^2 = 0, null dir = scaling ===")
det = H[('u','u')]*H[('Y10','Y10')] - H[('u','Y10')]**2
print(f"  det = {det:.3e} (vs entries ~{H[('u','u')]:.3f}) "
      f"{'OK' if abs(det) < 1e-5 else 'FAIL'}")
# null vector should be (dF, da) prop (F, a)
nv = np.array([F, a])
M = np.array([[H[('u','u')], H[('u','Y10')]], [H[('u','Y10')], H[('Y10','Y10')]]])
r = M @ nv
print(f"  M.(F,a) = {r} (should be ~0) "
      f"{'OK' if np.allclose(r, 0, atol=1e-4) else 'FAIL'}")
fails += (abs(det) >= 1e-5) + (not np.allclose(r, 0, atol=1e-4))

# analytic confirmation of the same entries (independent algebra)
print("\n=== C1.5 analytic cross-check (sympy) ===")
import sympy as sp
ks, Fs, asym = sp.symbols('k F a', positive=True)
cs = sp.sqrt(sp.Rational(3,4)/sp.pi)
Ls = sp.log((1+ks)/(1-ks))
P = 2*sp.pi*Fs*(2 + (ks-1/ks)*Ls)         # = 2 pi F h(k)
Pfa = P.subs(ks, cs*asym/Fs)
PFF = sp.simplify(sp.diff(Pfa, Fs, 2))
PFa = sp.simplify(sp.diff(Pfa, Fs, asym))
Paa = sp.simplify(sp.diff(Pfa, asym, 2))
Wsym = 2*ks/(1-ks**2) - Ls
checks = [
    ("V_uu",   PFF/4 - (sp.pi/ks*Wsym/Fs).subs(ks, cs*asym/Fs)),
    ("V_ua0",  PFa/4 - (-sp.sqrt(3*sp.pi)/(2*ks**2)*Wsym/Fs).subs(ks, cs*asym/Fs)),
    ("V_a0a0", Paa/4 - (3/(4*ks**3)*Wsym/Fs).subs(ks, cs*asym/Fs)),
]
for name, expr in checks:
    z = sp.simplify(expr)
    ok = (z == 0) or abs(sp.N(z.subs({Fs: 1.7, asym: 0.55*1.7/float(cs)}))) < 1e-25
    fails += (not ok)
    print(f"  {name}: residual {'0 OK' if ok else f'NONZERO FAIL: {z}'}")

print(f"\nC1 TOTAL FAILS: {fails}")
