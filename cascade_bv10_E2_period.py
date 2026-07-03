"""bv10_E2_period.py -- independent derivation of the per-half-cycle phase excess.

Frozen-Phi zero-energy orbit (E1, CAS-verified):
  theta_half = int sqrt(Qhat/What) dx  between the two roots of What,
  What(x) = E(1+x)^{-2} + u(x),  u(x) = 2*dh*x - x^2 + c3*x^3 + c4*x^4,
  Qhat(x) = 1 + E(1+x)^{-4},
  E = Phi^2/(4 Z |s1|),  dh = deltat/|s1|,  c3 = U'''(1)/(12|s1|), c4 = U''''(1)/(48|s1|).

PART A: symbolic (sympy) via z-substitution  2*Vt(x) = E - What -> z^2, x = x(z) series;
        theta_half = int x'(z) dz / sqrt(E - z^2)  (exact endpoint mapping), even part only.
        Scaling x ~ eps, E ~ eps^2, dh ~ eps^2; result to O(eps^2) = O(E).
PART B: mpmath quadrature of the EXACT integrand; extract coefficients numerically.
"""
import sympy as sp
import mpmath as mp

# ---------------------------------------------------------------- PART A: symbolic
eps = sp.symbols('epsilon', positive=True)
x, z = sp.symbols('x z')
E_, dh_, c3, c4 = sp.symbols('Ehat dhat c3 c4', positive=True)

ORD = 7  # x-power cutoff (x~eps; need relative O(eps^2))
Xs = eps*x
E = eps**2*E_
dh = eps**2*dh_

geom = sp.series(E/ (1+Xs)**2, eps, 0, ORD).removeO()
u = 2*dh*Xs - Xs**2 + c3*Xs**3 + c4*Xs**4
What = sp.expand(geom + u)
# 2*Vt(x) = E - What  (so that What = E - z^2 exactly under z^2 = 2 Vt)
twoV = sp.expand(E - What)
# invert z^2 = twoV(x): write x = z*(1 + a1*z + a2*z^2 + ...) with z ~ eps
a1, a2, a3 = sp.symbols('a1 a2 a3')
Zs = eps*z
xser = Zs*(1 + a1*Zs + a2*Zs**2 + a3*Zs**3)
expr = sp.expand(twoV.subs(Xs, xser) - Zs**2)
expr = sp.expand(sp.series(expr, eps, 0, ORD).removeO())
# solve order by order in eps (coefficients of eps^3, eps^4, eps^5 as polys in z)
sols = {}
for k, sym in ((3, a1), (4, a2), (5, a3)):
    ck = sp.Poly(expr.subs(sols), eps).coeff_monomial(eps**k)
    s = sp.solve(sp.Eq(ck, 0), sym)
    # ck is a polynomial in z; require it to vanish identically: collect in z
    ck = sp.expand(ck)
    polyz = sp.Poly(ck, z)
    # each z-coefficient must vanish; a_k appears linearly -- solve from the leading one
    eqs = [c for c in polyz.coeffs()]
    s = sp.solve(eqs, sym)
    if isinstance(s, dict):
        sols[sym] = sp.simplify(s[sym])
    else:
        sols[sym] = sp.simplify(s[0][0] if isinstance(s[0], tuple) else s[0])
    sols = {kk: sp.simplify(vv.subs(sols)) for kk, vv in sols.items()}
print("x(z) inversion coefficients (z-units eps*z):")
for kk, vv in sols.items():
    print("  ", kk, "=", sp.simplify(vv))

xp = sp.diff(xser.subs(sols), Zs).doit()
xp = sp.expand(sp.series(sp.expand(xp), eps, 0, 4).removeO())
# theta_W = int_{-sqrt(E)}^{sqrt(E)} x'(z) dz/sqrt(E - z^2); with z = eps*zh, E = eps^2 Ehat:
# int zh^{2k} dzh/sqrt(Ehat - zh^2): k=0 -> pi, k=1 -> pi*Ehat/2 ; odd -> 0
zh = z
xp_poly = sp.Poly(xp, zh)
theta_W = 0
for mono, coef in zip(xp_poly.monoms(), xp_poly.coeffs()):
    k = mono[0]
    if k % 2 == 1:
        continue
    if k == 0:
        theta_W += coef*sp.pi
    elif k == 2:
        theta_W += coef*sp.pi*E_/2
    elif k == 4:
        theta_W += coef*sp.pi*sp.Rational(3,8)*E_**2
theta_W = sp.expand(sp.series(theta_W, eps, 0, 4).removeO())
print("\ntheta_W (W-part) =", sp.simplify(theta_W))

# Q-part: (E/2) * int (1+x)^{-4} dx/sqrt(What) -> leading (E/2)*pi (corrections O(eps^3))
theta_Q = sp.pi*E/2
theta = sp.simplify(theta_W + theta_Q)
print("theta_half = pi +", sp.simplify(theta - sp.pi))
# claimed: pi*E*(2 + 15/16 c3^2 - 3/2 c3 + 3/4 c4) + pi*(3 c3/2)*dh
claim = sp.pi*E*(2 + sp.Rational(15,16)*c3**2 - sp.Rational(3,2)*c3 + sp.Rational(3,4)*c4) \
        + sp.pi*sp.Rational(3,2)*c3*dh
print("theta_half - pi - CLAIM =", sp.simplify(sp.expand(theta - sp.pi - claim)))

# ---------------------------------------------------------------- PART B: numeric exact
mp.mp.dps = 40

def theta_num(E, dh, c3, c4, geom=True, Qon=True):
    E, dh, c3, c4 = map(mp.mpf, (E, dh, c3, c4))
    def W(xx):
        g = E/(1+xx)**2 if geom else E
        return g + 2*dh*xx - xx**2 + c3*xx**3 + c4*xx**4
    def Q(xx):
        return 1 + E/(1+xx)**4 if (Qon and geom) else (1 + E if Qon else mp.mpf(1))
    # bracket roots around x0 ~ dh with half-width ~ sqrt(E+dh^2)
    x0 = dh
    a = mp.sqrt(E + dh**2)
    lo, hi = x0 - 3*a - mp.mpf('1e-30'), x0 + 3*a + mp.mpf('1e-30')
    xm = mp.findroot(W, (x0 - a*mp.mpf('0.5'), lo), solver='bisect', tol=mp.mpf('1e-60')) \
        if W(lo) < 0 else None
    # robust: bisect on [lo, x0] and [x0, hi]
    def bis(aa, bb):
        fa, fb = W(aa), W(bb)
        assert fa*fb < 0, (aa, bb, fa, fb)
        for _ in range(220):
            mm = (aa+bb)/2
            fm = W(mm)
            if fa*fm <= 0: bb, fb = mm, fm
            else: aa, fa = mm, fm
        return (aa+bb)/2
    xL = bis(lo, x0)
    xR = bis(x0, hi)
    mid, hw = (xL+xR)/2, (xR-xL)/2
    def integrand(t):
        xx = mid + hw*mp.sin(t)
        base = (xR-xx)*(xx-xL)
        R = W(xx)/base
        return mp.sqrt(Q(xx)/R)
    return mp.quad(integrand, [-mp.pi/2, 0, mp.pi/2])

pi = mp.pi
print("\n--- numeric coefficient extraction (E-slope at dh=0), Elist=[1e-5,1e-6] Richardson ---")
cases = [
    ("c3=0,c4=0 full",      0.0, 0.0, True,  True,  mp.mpf(2)),
    ("c3=0,c4=0 no-geom+Q", 0.0, 0.0, False, True,  mp.mpf(1)/2),
    ("c3=0,c4=0 geom,no-Q", 0.0, 0.0, True,  False, mp.mpf(3)/2),
    ("c3=0.3,c4=0 no-geom no-Q", 0.3, 0.0, False, False, mp.mpf(15)/16*mp.mpf('0.09')),
    ("c3=0,c4=1 no-geom no-Q",   0.0, 1.0, False, False, mp.mpf(3)/4),
    ("c3=0.3,c4=1 full",    0.3, 1.0, True,  True,
        2 + mp.mpf(15)/16*mp.mpf('0.09') - mp.mpf(3)/2*mp.mpf('0.3') + mp.mpf(3)/4),
]
for name, C3, C4, g, qq, expect in cases:
    D = []
    for Ev in ('1e-5', '1e-6'):
        th = theta_num(mp.mpf(Ev), 0, C3, C4, geom=g, Qon=qq)
        D.append((th/pi - 1)/mp.mpf(Ev))
    B = (10*D[1] - D[0])/9   # Richardson (linear in E)
    print(f"  {name:28s} B_num = {mp.nstr(B, 10):>14s}  expect {mp.nstr(expect, 10):>14s}  diff {mp.nstr(B-expect, 3)}")

print("\n--- dh-slope at E=1e-9 (expect 3/2*c3) ---")
for C3 in (0.3, 1.0):
    s = []
    for dv in ('1e-4', '1e-5'):
        th = theta_num(mp.mpf('1e-9'), mp.mpf(dv), C3, 0.7, geom=True, Qon=True)
        s.append((th/pi - 1)/mp.mpf(dv))
    S = (10*s[1] - s[0])/9
    print(f"  c3={C3}: slope = {mp.nstr(S, 8)}  expect {mp.nstr(mp.mpf(3)/2*C3, 8)}")

print("\n--- additivity/truncation at rung-like values (E=9.3e-3, dh=6.26e-3, m3 coeffs) ---")
C3, C4 = 0.29817, 1.25121   # will be recomputed exactly in the assembly script
E0, D0 = mp.mpf('9.31e-3'), mp.mpf('6.26e-3')
th = theta_num(E0, D0, C3, C4)
form = pi*(1 + E0*(2 + mp.mpf(15)/16*C3**2 - mp.mpf(3)/2*C3 + mp.mpf(3)/4*C4)
           + mp.mpf(3)/2*C3*D0)
print(f"  exact quadrature theta/pi = {mp.nstr(th/pi, 10)}")
print(f"  claimed formula theta/pi  = {mp.nstr(form/pi, 10)}")
print(f"  difference (units of pi)  = {mp.nstr((th-form)/pi, 4)}   [O(E^2)+O(dh^2) truncation at seal-cycle]")
