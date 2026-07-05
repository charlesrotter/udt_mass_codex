import sympy as sp

r, eps, Zf = sp.symbols('r epsilon Z_phi', positive=True)
q = sp.Function('phi_amb')
dphi = sp.Function('dphi')

# ---- ITEM 1: linearize round Branch-P eq  Zf*(r^2 phi')' = 4 e^{-2 phi}  about phi = phi_amb + eps*dphi ----
phi = q(r) + eps*dphi(r)
LHS = Zf*sp.diff(r**2*sp.diff(phi, r), r)
RHS = 4*sp.exp(-2*phi)
resid = sp.expand(LHS - RHS)

# zeroth order (eps^0)
o0 = resid.subs(eps, 0)
print("ZEROTH ORDER  LHS-RHS =", sp.simplify(o0))
print("  => zeroth-order eq:  Zf*(r^2 phi_amb')' = 4 e^{-2 phi_amb} :",
      sp.simplify(o0 - (Zf*sp.diff(r**2*sp.diff(q(r),r),r) - 4*sp.exp(-2*q(r))))==0)

# first order (coeff of eps^1)
o1 = sp.diff(resid, eps).subs(eps, 0)
o1 = sp.simplify(o1)
print("\nFIRST ORDER (coeff eps^1)  LHS-RHS =", o1)
# expected: Zf*(r^2 dphi')' + 8 e^{-2 phi_amb} dphi = 0
expected = Zf*sp.diff(r**2*sp.diff(dphi(r),r),r) + 8*sp.exp(-2*q(r))*dphi(r)
print("matches  Zf*(r^2 dphi')' + 8 e^{-2 phi_amb} dphi ? ->", sp.simplify(o1 - expected)==0)

# ---- ITEM 3: indicial roots with e^{-2 phi_amb}=W0 frozen constant ----
W0, s = sp.symbols('W0 s')
dphi2 = sp.Function('f')
# operator: Zf*(r^2 f')' + 8 W0 f = 0 ; try f=r^s
f = r**s
op = Zf*sp.diff(r**2*sp.diff(f,r),r) + 8*W0*f
op = sp.simplify(op / r**s)
print("\nINDICIAL polynomial (÷r^s):", sp.expand(op))
roots = sp.solve(sp.Eq(op,0), s)
print("roots s =", [sp.simplify(rt) for rt in roots])
# compare to catch's -1/2 ± sqrt(Zf-32 W0)/(2 sqrt(Zf))
claim = [-sp.Rational(1,2)+sp.sqrt(Zf-32*W0)/(2*sp.sqrt(Zf)),
         -sp.Rational(1,2)-sp.sqrt(Zf-32*W0)/(2*sp.sqrt(Zf))]
print("catch roots  =", [sp.simplify(c) for c in claim])
print("difference set-equal?:", sp.simplify((roots[0]-claim[0])*(roots[0]-claim[1]))==0)

# W0 -> 0 limit
print("\nW0->0 roots:", [sp.simplify(rt.subs(W0,0)) for rt in roots])

# critical depth: discriminant Zf - 32 W0 = 0
print("critical W0 = Zf/32 ; at Zf=1 -> W0=", sp.Rational(1,32),
      " phi_amb=", sp.nsimplify(-sp.log(sp.Rational(1,32))/2), "=", float(-sp.log(sp.Rational(1,32))/2))
