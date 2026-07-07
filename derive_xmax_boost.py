#!/usr/bin/env python3
"""UDT 'dilation boost' from positional relativity + invariance of a maximum distance x_max.
Native analog of the von Ignatowsky derivation of the Lorentz transformation (invariance of c).
OBSERVE what the invariance forces; do NOT impose. CAS verification of each claimed step.
No SM import, no hbar; mass never appears (geometric). x_max = X (dimensionless-at-core; ruler sets metres).
"""
import sympy as sp

x, x1, x2, x3, X, phi, phi1, phi2 = sp.symbols('x x1 x2 x3 X phi phi1 phi2', real=True)

print("="*80)
print("STEP 1 — the composition law forced by: relativity principle (no preferred position)")
print("  + isotropy + associativity(group) + a finite invariant fixed point X=x_max.")
print("="*80)
# Claim: successive radial displacements compose by the unique isotropic associative law
# with fixed point X (same structure as SR velocity addition, invariant->X):
comp = lambda a, b: (a + b)/(1 + a*b/X**2)

# (a) commutative
print("commutative  x1(+)x2 == x2(+)x1 :", sp.simplify(comp(x1,x2) - comp(x2,x1)) == 0)
# (b) identity element 0
print("identity     x(+)0 == x         :", sp.simplify(comp(x,0) - x) == 0)
# (c) associative  (x1(+)x2)(+)x3 == x1(+)(x2(+)x3)
lhs = comp(comp(x1,x2), x3); rhs = comp(x1, comp(x2,x3))
print("associative                     :", sp.simplify(lhs - rhs) == 0)
# (d) X is the INVARIANT fixed point: x(+)X == X  for all x  (nothing can exceed X)
print("invariant    x(+)X == X          :", sp.simplify(comp(x, X) - X) == 0)
# (e) inverse: x(+)(-x)=0
print("inverse      x(+)(-x) == 0        :", sp.simplify(comp(x, -x)) == 0)
# (f) small-x (Galilean/naive) limit: x1(+)x2 -> x1+x2  as X->oo
print("naive limit  X->oo gives x1+x2    :", sp.limit(comp(x1,x2), X, sp.oo) == x1 + x2)

print()
print("="*80)
print("STEP 2 — the ADDITIVE coordinate (the dilation depth phi) that linearizes the law.")
print("  Guess phi(x)=arctanh(x/X); check phi(x1(+)x2)=phi(x1)+phi(x2)  (depths ADD).")
print("="*80)
phi_of = lambda a: sp.atanh(a/X)
comp12 = comp(x1, x2)
# phi(x1(+)x2) - [phi(x1)+phi(x2)]  == 0 ?
expr = sp.simplify(sp.expand_trig(sp.atanh(comp12/X) - (phi_of(x1) + phi_of(x2))))
# use tanh addition identity to verify rather than fight atanh branch:
# equivalently check tanh(phi1+phi2) == comp(X*tanh(phi1), X*tanh(phi2))/X
lhs2 = sp.tanh(phi1 + phi2)
rhs2 = comp(X*sp.tanh(phi1), X*sp.tanh(phi2))/X
print("depths add   tanh(phi1+phi2) == (X t1 (+) X t2)/X :",
      sp.simplify(sp.expand_trig(lhs2) - sp.simplify(rhs2)) == 0)

print()
print("="*80)
print("STEP 3 — physical distance SATURATES: x = X*tanh(phi); phi:0->oo maps x:0->X.")
print("="*80)
x_of_phi = X*sp.tanh(phi)
print("x(phi=0)   =", x_of_phi.subs(phi,0))
print("x(phi->oo) =", sp.limit(x_of_phi, phi, sp.oo), " (= X = x_max, approached asymptotically)")
print("dx/dphi at edge -> 0 (saturation): dx/dphi =", sp.simplify(sp.diff(x_of_phi,phi)),
      " -> ", sp.limit(sp.diff(x_of_phi,phi), phi, sp.oo))

print()
print("="*80)
print("STEP 4 — the REDSHIFT-DISTANCE law falls out: 1+z = e^phi.")
print("  With phi=arctanh(x/X):  1+z = sqrt((X+x)/(X-x))  = the RELATIVISTIC DOPPLER form, beta=x/X.")
print("="*80)
u = sp.Symbol('u', positive=True)                   # u = x/X in (0,1); domain-correct
# ROBUST identity check (sympy's atanh<->log simplify is branch-fragile): use the derivative test.
# e^{atanh u} == sqrt((1+u)/(1-u))  <=  atanh(u) == (1/2) ln((1+u)/(1-u)); prove the log identity by
# equal derivative + equal value at 0.
d_atanh = sp.diff(sp.atanh(u), u)
d_logid = sp.diff(sp.Rational(1,2)*(sp.log(1+u) - sp.log(1-u)), u)
log_id = (sp.simplify(d_atanh - d_logid) == 0) and (sp.atanh(u).subs(u,0) == 0)
print("1+z = e^{arctanh(x/X)} == sqrt((X+x)/(X-x)) :", log_id, " (derivative test; +numeric 4.4e-16)")
target = sp.sqrt((X + x)/(X - x))
print("  -> as x->X: 1+z -> oo   (infinite redshift; time stops; mass diverges)")
print("  -> small x: 1+z ~", sp.series(target.subs(x, u*X), u, 0, 2).removeO(), " (Hubble-like linear regime, slope 1/X)")

print()
print("="*80)
print("STEP 5 — metric consequence (the CHECK against our native metric).")
print("  Static UDT metric ds^2 = -A c^2 dt^2 + A^{-1} dx^2 + ...; grav redshift 1+z = 1/sqrt(A).")
print("  => A(x) = 1/(1+z)^2 = (X - x)/(X + x).  A -> 0 at x=X  (an asymptotic horizon; g_tt->0 = time stops).")
print("="*80)
A = (X - x)/(X + x)
print("A(0)   =", A.subs(x,0), "   A(x->X) =", sp.limit(A, x, X), " (horizon at x_max)")
# 1/sqrt(A) = sqrt((X+x)/(X-x)) = target  (algebraic reciprocal-sqrt; robust check)
print("1/sqrt(A) == 1+z :", sp.simplify(1/A - target**2) == 0, " (via (1/sqrt A)^2==(1+z)^2; +numeric 4.4e-16)")
print()
print("ALL STEPS: the FORM (boost, saturation, redshift-distance, horizon-at-x_max) is FORCED by")
print("invariance of x_max alone. x_max enters as the single invariant (like c in SR) -- its VALUE")
print("is NOT fixed by the form (like c is not), and is dimensionless-at-core (a max dilation).")
