"""Blind verifier: C1 closed forms, re-derived from scratch in sympy.

Conventions re-pinned independently:
  f = F(y)(1 + kappa cos th),  a = F kappa / sqrt(3)
  P(F,a) = (3 a^2 / (8F)) G1(kappa),  kappa = sqrt(3) a / F
  G1 = (2k + (k^2-1)L)/k^3,  L = ln((1+k)/(1-k))
  EL: (y^2 F')' = 2 P_F, (y^2 a')' = 2 P_a
"""
import sympy as sp
import mpmath as mp

F, a, k, y = sp.symbols('F a kappa y', positive=True)
lam = sp.symbols('lambda', positive=True)

L  = sp.log((1+k)/(1-k))
G1 = (2*k + (k**2-1)*L)/k**3

# P as explicit function of (F, a):
kap = sp.sqrt(3)*a/F
P = (3*a**2/(8*F)) * G1.subs(k, kap)

# ---- degree-1 homogeneity ----
hom = sp.simplify(P.subs({F: lam*F, a: lam*a}) - lam*P)
print("homogeneity residual (expect 0):", hom)

# ---- P_F closed form: H := -2 P_F =?= L/(2k) - 1 ----
P_F = sp.diff(P, F)
H_claim = (L/(2*k) - 1).subs(k, kap)
res_H = sp.simplify(sp.together(-2*P_F - H_claim))
print("H residual (expect 0):", res_H)
if res_H != 0:
    # numeric fallback
    import random
    bad = 0
    for _ in range(20):
        Fv = random.uniform(0.2, 5.0); kv = random.uniform(1e-3, 0.999)
        av = Fv*kv/sp.sqrt(3)
        d = ((-2*P_F) - H_claim).subs({F: Fv, a: av}).evalf(30)
        if abs(d) > 1e-22: bad += 1
        print("  numeric H check:", float(d))
    print("  bad:", bad)

# ---- P_a closed form: P_a =?= sqrt(3) * [L(1+k^2)-2k]/(8k^2) ----
P_a = sp.diff(P, a)
Wp_claim = (sp.sqrt(3)*(L*(1+k**2) - 2*k)/(8*k**2)).subs(k, kap)
res_Pa = sp.simplify(sp.together(P_a - Wp_claim))
print("P_a residual (expect 0):", res_Pa)
if res_Pa != 0:
    import random
    for _ in range(10):
        Fv = random.uniform(0.2, 5.0); kv = random.uniform(1e-3, 0.999)
        av = Fv*kv/3**0.5
        d = (P_a - Wp_claim).subs({F: Fv, a: av}).evalf(30)
        print("  numeric P_a check:", float(d))

# ---- rank-1 Hessian / exact screening: P_FF - P_Fa^2/P_aa = 0 ----
P_FF = sp.diff(P, F, 2); P_aa = sp.diff(P, a, 2); P_Fa = sp.diff(P, F, a)
scr = sp.simplify(sp.together(P_FF - P_Fa**2/P_aa))
print("screening residual (expect 0):", scr)
if scr != 0:
    import random
    for _ in range(10):
        Fv = random.uniform(0.2, 5.0); kv = random.uniform(1e-3, 0.99)
        av = Fv*kv/3**0.5
        d = (P_FF - P_Fa**2/P_aa).subs({F: Fv, a: av}).evalf(30)
        print("  numeric screening check:", float(d))

# ---- collar criticality: F0 = y^-q  =>  (y^2 F0')' = -2 s y^-q, s=q(1-q)/2
q = sp.Rational(1,3); s = q*(1-q)/2
F0 = y**(-q)
lhs = sp.simplify(sp.diff(y**2*sp.diff(F0, y), y))
print("s =", s, "; (y^2 F0')' + 2*s*y^-q (expect 0):",
      sp.simplify(lhs + 2*s*y**(-q)))
# EL F-eq: (y^2F')' = 2P_F = -H  => criticality H(kappa(y)) = 2 s y^-q. Confirmed iff above is 0.

# ---- interface condition: H(k)=2s at y=1  <=>  L = 2k(1+2s); root for s=1/9
kk = sp.symbols('kk')
Lk = mp.mpf(2)  # placeholder
def Hnum(kv):
    kv = mp.mpf(kv)
    return mp.log((1+kv)/(1-kv))/(2*kv) - 1
root = mp.findroot(lambda kv: Hnum(kv) - mp.mpf(2)/9, 0.7)
print("interface root kappa(1) =", mp.nstr(root, 12), " (claim 0.6830951)")
print("check L=2k(1+2s):", mp.nstr(mp.log((1+root)/(1-root)) - 2*root*(1+mp.mpf(2)/9), 5))

# ---- legacy slip identity: 0.230329 =?= sqrt(6 s / (4 pi)), s = 1/9
val = mp.sqrt(6*mp.mpf(1)/9/(4*mp.pi))
print("sqrt(6s/4pi) =", mp.nstr(val, 10), " (claim 0.230329)")

# ---- bonus: re-derive P from angular quadrature with density f_theta^2/(4f)
th = sp.symbols('theta')
kk2 = sp.symbols('k2', positive=True)
f_ang = F*(1+kk2*sp.cos(th))
dens = sp.diff(f_ang, th)**2/(4*f_ang)
avg = sp.integrate(dens*sp.sin(th), (th, 0, sp.pi))/2
avg = sp.simplify(avg)
P_claim = (3*(F*kk2/sp.sqrt(3))**2/(8*F))*((2*kk2+(kk2**2-1)*sp.log((1+kk2)/(1-kk2)))/kk2**3)
print("quadrature re-derivation residual (expect 0):",
      sp.simplify(sp.together(avg - P_claim)))
