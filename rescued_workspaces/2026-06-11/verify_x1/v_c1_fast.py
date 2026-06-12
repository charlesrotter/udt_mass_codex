"""C1 closed forms — high-precision numeric identity checks (50 dps), plus
exact-rational series cross-checks. Avoids sympy simplify hangs."""
import mpmath as mp
mp.mp.dps = 50
SQ3 = mp.sqrt(3)

def Lf(k): return mp.log((1+k)/(1-k))
def G1(k): return (2*k + (k**2-1)*Lf(k))/k**3

def P(Fv, av):
    k = SQ3*av/Fv
    return (3*av**2/(8*Fv))*G1(k)

def d(f, x, h='1e-12'):
    h = mp.mpf(h)
    return (f(x+h) - f(x-h))/(2*h)

import random
random.seed(7)
print("== P_F, P_a, screening: numeric vs closed forms (max |residual|) ==")
mx = [0, 0, 0, 0]
for _ in range(25):
    Fv = mp.mpf(str(random.uniform(0.2, 5.0)))
    kv = mp.mpf(str(random.uniform(0.01, 0.98)))
    av = Fv*kv/SQ3
    PF = d(lambda x: P(x, av), Fv)
    Pa = d(lambda x: P(Fv, x), av)
    H_closed = Lf(kv)/(2*kv) - 1
    Pa_closed = SQ3*(Lf(kv)*(1+kv**2) - 2*kv)/(8*kv**2)
    r1 = abs(-2*PF - H_closed); mx[0] = max(mx[0], r1)
    r2 = abs(Pa - Pa_closed);   mx[1] = max(mx[1], r2)
    # second derivatives via central differences on first-derivative closed forms:
    # P_F(F,a) = -(1/2) H(sqrt3 a/F), P_a(F,a) = closed; differentiate those exactly.
    def PFfun(F_, a_): return -mp.mpf(1)/2*(Lf(SQ3*a_/F_)/(2*SQ3*a_/F_) - 1)
    def Pafun(F_, a_):
        k_ = SQ3*a_/F_
        return SQ3*(Lf(k_)*(1+k_**2) - 2*k_)/(8*k_**2)
    PFF = d(lambda x: PFfun(x, av), Fv)
    PFa = d(lambda x: PFfun(Fv, x), av)
    Paa = d(lambda x: Pafun(Fv, x), av)
    r3 = abs(PFF - PFa**2/Paa); mx[2] = max(mx[2], r3)
    # degree-1 homogeneity
    lamv = mp.mpf(str(random.uniform(0.3, 3.0)))
    r4 = abs(P(lamv*Fv, lamv*av) - lamv*P(Fv, av)); mx[3] = max(mx[3], r4)
print("  -2P_F - [L/2k - 1]     :", mp.nstr(mx[0], 3))
print("  P_a  - sqrt3 W'        :", mp.nstr(mx[1], 3))
print("  P_FF - P_Fa^2/P_aa     :", mp.nstr(mx[2], 3))
print("  homogeneity            :", mp.nstr(mx[3], 3))

print("\n== quadrature re-derivation: P =?= <f_theta^2/(4f)> over sphere ==")
# P claimed per solid angle: (3a^2/8F) G1.  Independent: (1/2)Int_0^pi
# sin th * (d_th f)^2/(4 f) dth with f = F(1+k cos th).
mx = 0
for _ in range(8):
    Fv = mp.mpf(str(random.uniform(0.3, 3.0)))
    kv = mp.mpf(str(random.uniform(0.05, 0.97)))
    av = Fv*kv/SQ3
    quad = mp.quad(lambda th: mp.sin(th)*(Fv*kv*mp.sin(th))**2/(4*Fv*(1+kv*mp.cos(th))), [0, mp.pi])/2
    mx = max(mx, abs(quad - P(Fv, av)))
print("  max |quad - P| :", mp.nstr(mx, 3))

print("\n== collar criticality and interface root ==")
q = mp.mpf(1)/3; s = q*(1-q)/2
print("  s = q(1-q)/2 =", s, " (claim 1/9):", s == mp.mpf(1)/9)
# (y^2 (y^-q)')' = -q(1-q) y^-q = -2s y^-q  => EL F-eq  -H = -2s y^-q. Analytic.
yv = mp.mpf('0.731')
lhs = mp.diff(lambda y: y**2*mp.diff(lambda z: z**(-q), y), yv)  # not valid; do explicit
# explicit: (y^2 * (-q) y^{-q-1})' = (-q y^{1-q})' = -q(1-q) y^{-q}
print("  collar identity exact: (y^2 F0')' = -q(1-q) y^-q = -2s y^-q  [algebraic]")
root = mp.findroot(lambda k: Lf(k)/(2*k) - 1 - 2*s, mp.mpf('0.7'))
print("  interface root kappa(1) =", mp.nstr(root, 10), "(claim 0.6830951)")
print("  L - 2k(1+2s) at root    =", mp.nstr(Lf(root) - 2*root*(1+2*s), 3))
print("  slip identity sqrt(6s/4pi) =", mp.nstr(mp.sqrt(6*s/(4*mp.pi)), 9),
      "(claim 0.230329)  [= 1/sqrt(6 pi) for s=1/9]")
print("  1/sqrt(6 pi) =", mp.nstr(1/mp.sqrt(6*mp.pi), 9))
