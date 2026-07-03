"""bv10_E2_symbolic.py -- PART A redone properly: shift to the W-maximum x*, then the
exact canonical substitution z^2 = twoV(x) - twoV(x*) (turning points -> z = +-sqrt(h) exactly,
h = W(x*)), theta_W = int x'(z) dz / sqrt(h - z^2); only even z-powers survive.
Orders: x ~ eps, E ~ eps^2, dh ~ eps^2; theta to relative O(eps^2) = O(E).
"""
import sympy as sp

eps = sp.symbols('epsilon', positive=True)
x, zt = sp.symbols('x zt')
E_, dh_, c3, c4 = sp.symbols('Ehat dhat c3 c4', real=True)
E, dh = eps**2*E_, eps**2*dh_

ORD = 8
Xs = eps*x
geom = sp.series(E/(1+Xs)**2, eps, 0, ORD).removeO()
u = 2*dh*Xs - Xs**2 + c3*Xs**3 + c4*Xs**4
What = sp.expand(geom + u)
twoV = sp.expand(E - What)

# --- center x* : twoV'(x*) = 0, x* = eps^2*(s2) + eps^3*(s3) + eps^4*(s4)... (x* ~ eps^2)
s2, s3, s4 = sp.symbols('s2 s3 s4')
xstar = eps**2*s2 + eps**3*s3 + eps**4*s4      # in TRUE units (x* = eps * (eps s2 + ...)? see note)
# NOTE: What is written in terms of Xs = eps*x (true variable X = eps*x). Work in TRUE variable X:
X = sp.symbols('X')
WhatX = What.subs(x, X/eps)
WhatX = sp.expand(WhatX)
dW = sp.diff(WhatX, X)
eq = sp.expand(dW.subs(X, xstar))
sol = {}
for k, sym in ((2, s2), (3, s3), (4, s4)):
    ck = sp.expand(sp.series(eq.subs(sol), eps, 0, k+1)).coeff(eps, k)
    r = sp.solve(sp.Eq(ck, 0), sym)
    sol[sym] = sp.simplify(r[0])
    sol = {kk: sp.simplify(vv.subs(sol)) for kk, vv in sol.items()}
print("x* =", sp.simplify(xstar.subs(sol)), "  [true units; expect (dh-E)*eps^2 + O(eps^4)]")

xs_val = sp.expand(xstar.subs(sol))
h = sp.expand(sp.series(WhatX.subs(X, xs_val), eps, 0, ORD).removeO())
print("h = W(x*) =", sp.simplify(h), "  [expect E + (dh-E)^2 eps^4 + ...]")

# --- z-substitution about x*: y = X - x*, z^2 = twoV(x) - twoV(x*) = h - What
F = sp.expand(h - WhatX.subs(X, xs_val + sp.symbols('y')))     # = z^2 as series in y
y = sp.symbols('y')
F = sp.expand(sp.series(F, eps, 0, ORD).removeO())
# ansatz y(z) = z*(g0 + g1*z + g2*z^2 + g3*z^3), z ~ eps; g1,g2,g3 = O(1) (c3,c4 are O(1)),
# g0 = 1 + eps^2*g0a.  Solve F(y(z)) = z^2 order by order in eps.
g0a, g1a, g2a, g3a = sp.symbols('g0 g1 g2 g3')
z = sp.symbols('z')
Zs = eps*z
g0 = 1 + eps**2*g0a
yz = Zs*(g0 + g1a*Zs + g2a*Zs**2 + g3a*Zs**3)
expr = sp.expand(sp.series(sp.expand(F.subs(y, yz) - Zs**2), eps, 0, 6).removeO())
poly = sp.Poly(expr, eps)
solg = {}
# eps^3, z^3  -> g1a
c3ord = sp.expand(poly.coeff_monomial(eps**3))
solg[g1a] = sp.simplify(sp.solve(sp.Poly(c3ord, z).coeff_monomial(z**3), g1a)[0])
# eps^4: z^2 -> g0a ; z^4 -> g2a
c4ord = sp.expand(poly.coeff_monomial(eps**4)).subs(solg)
pz = sp.Poly(c4ord, z)
r = sp.solve([pz.coeff_monomial(z**2), pz.coeff_monomial(z**4)], [g0a, g2a], dict=True)[0]
solg[g0a] = sp.simplify(r[g0a]); solg[g2a] = sp.simplify(r[g2a])
print("g0 =", sp.simplify(g0.subs(solg)))
print("g1 =", sp.simplify(solg[g1a]))
print("g2 =", sp.simplify(solg[g2a]))
# eps^5: z^5 -> g3a (odd, irrelevant to theta); z^3 residual absorbed by eps^2-corr of g1 (odd too)
c5ord = sp.expand(poly.coeff_monomial(eps**5)).subs(solg)
pz5 = sp.Poly(c5ord, z)
print("eps^5 even-z residual (must be 0):",
      sp.simplify(pz5.coeff_monomial(z**2)), sp.simplify(pz5.coeff_monomial(z**4)))

# --- theta_W = int dy/dz dz/sqrt(h - z^2), z in (-sqrt(h), +sqrt(h)); even powers only:
# int dz/sqrt(h-z^2) = pi ; int z^2 dz/sqrt(h-z^2) = pi*h/2   (true z units)
dydz_true = sp.expand(sp.diff(yz.subs(solg), z)/eps)   # d y/d z_true (z_true = eps*z)
P = sp.Poly(dydz_true, z)
even0 = P.coeff_monomial(1)
even2 = P.coeff_monomial(z**2)/eps**2      # coefficient wrt true z^2
theta_W = even0*sp.pi + even2*sp.pi*h/2
theta_W = sp.expand(sp.series(sp.expand(theta_W), eps, 0, 5).removeO())
theta_Q = sp.pi*E/2
theta = sp.expand(theta_W + theta_Q)
print("\ntheta_half = ", sp.simplify(theta))
claim = sp.pi*(1 + E*(2 + sp.Rational(15,16)*c3**2 - sp.Rational(3,2)*c3 + sp.Rational(3,4)*c4)
               + sp.Rational(3,2)*c3*dh)
print("theta_half - CLAIM =", sp.simplify(sp.expand(theta - claim)))
