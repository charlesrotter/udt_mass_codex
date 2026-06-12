"""B1: source second-order content, coordinate measure. Independent recomputation.
 (a) N3's c_n = -c r^2 f^2 E0 f0^{-n}/(2n)  ==  record c_n = J f0^{1-n}/n on collar  (fix c)
 (b) criticality on GENERAL static backgrounds (E0 general)
 (c) full linearized phi-EL on general background: target (r^2 f^2 dphi')' - (4-2n) r^2 f^2 E0 dphi
 (d) sign of the single second-order action term (claim: +c n r^2 f^2 E0 dphi^2)
 (e) collar map to (y^2 u')' = (lam y^q + mu) u, mu = (1-n) q (1-q); omega^2 -> +omega^2 y^{2+2q} u
"""
import sympy as sp

r, n, q, lam, w = sp.symbols('r n q lambda omega', positive=True)
y = r
cc = sp.Symbol('c', positive=True)

# general static background
p0 = sp.Function('phi0')(r)
f0g = sp.exp(-2*p0)
E0 = sp.diff(p0, r, 2) + 2*sp.diff(p0, r)/r - 2*sp.diff(p0, r)**2

# (a) c fixed by collar comparison
p0c = q*sp.log(y)/2
f0c = sp.exp(-q*sp.log(y))
s = q*(1-q)/2
J = -s*y**(-q)
cn_rec = J*f0c**(1-n)/n
E0c = (sp.diff(p0c, y, 2) + 2*sp.diff(p0c, y)/y - 2*sp.diff(p0c, y)**2)
print("E0 on collar - s/y^2:", sp.simplify(E0c - s/y**2))
cn_N3_collar = -cc*y**2*f0c**2*E0c*f0c**(-n)/(2*n)
csol = sp.solve(sp.simplify(sp.powsimp(cn_N3_collar - cn_rec, force=True)), cc)
print("B1(a) c that makes N3 c_n == record c_n on collar:", csol)
cval = csol[0]

# (b) criticality on general backgrounds with that c:
cn_gen = -cval*r**2*f0g**2*E0*f0g**(-n)/(2*n)
crit = sp.diff(sp.Rational(1,2)*r**2*sp.diff(f0g, r), r) - n*cn_gen*f0g**(n-1)
print("B1(b) general-background criticality residual:", sp.simplify(crit))

# (c) full linearized EL in the phi slot, general background
e = sp.Symbol('epsilon')
dp = sp.Function('dphi')(r)
phi = p0 + e*dp
L = r**2*sp.diff(phi, r)**2*sp.exp(-4*phi) + cn_gen*sp.exp(-2*n*phi)
# manual Euler-Lagrange in dp at O(e):
Lser = sp.expand(sp.series(L, e, 0, 3).removeO())
L2 = Lser.coeff(e, 2)          # quadratic action density
EL_lin = sp.diff(sp.diff(L2, sp.diff(dp, r)), r) - sp.diff(L2, dp)
target = 2*(sp.diff(r**2*f0g**2*sp.diff(dp, r), r) - (4-2*n)*r**2*f0g**2*E0*dp)
print("B1(c) linearized EL - 2[(r^2f^2 dphi')' - (4-2n) r^2 f^2 E0 dphi]:",
      sp.simplify(sp.expand(EL_lin - target)))

# (d) the single second-order action term (pure source part of L2)
L2_src = sp.expand(sp.series(cn_gen*sp.exp(-2*n*phi), e, 0, 3).removeO()).coeff(e, 2)
claimed = +cval*n*r**2*f0g**2*E0*dp**2
print("B1(d) L2_src  + c n r^2 f^2 E0 dphi^2  (claim => 0):", sp.simplify(L2_src - claimed))
print("B1(d) L2_src  - (-c n r^2 f^2 E0 dphi^2)         :", sp.simplify(L2_src + claimed))

# (e) collar map: static op  (y^2 f^2 dphi')' - (4-2n) y^2 f^2 E0 dphi - lam f dphi  (+ time)
u = sp.Function('u')(y)
dpc = y**q*u
op = (sp.diff(y**2*f0c**2*sp.diff(dpc, y), y)
      - (4-2*n)*y**2*f0c**2*(s/y**2)*dpc - lam*f0c*dpc - w**2*y**2*dpc)  # time: +r^2 d_t^2 -> -w^2 r^2
mapped = sp.expand(sp.powsimp(op*y**(2*q)/y**q, force=True))  # multiply by y^{2q}, divide by y^q
mu_target = (1-n)*q*(1-q)
target_u = sp.expand(sp.diff(y**2*sp.diff(u, y), y) - (lam*y**q + mu_target)*u - w**2*y**(2+2*q)*u)
print("B1(e) collar map residual (incl. omega term):", sp.simplify(mapped - target_u))
print("B1(e) mu(n) =", sp.simplify(mu_target), "; 1+4mu at q=1/3:",
      sp.simplify((1+4*mu_target).subs(q, sp.Rational(1,3))))
