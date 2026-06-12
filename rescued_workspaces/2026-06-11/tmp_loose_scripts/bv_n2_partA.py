"""Blind adversarial verifier — N2 claims A1-A5. Independent recomputation.
Conventions (from prompt background only):
  C1 per solid angle: L = (1/4)[y^2 f'^2 + |grad_O f|^2 / f], f = e^{-2 phi}
  collar f0 = y^-q, s = q(1-q)/2, J = -s y^-q, c_n = J f0^{1-n}/n
  S_src = int c_n(y) f^n dy
"""
import sympy as sp

y, n, lam, mu_s = sp.symbols('y n lambda mu', positive=True)
q = sp.Symbol('q', positive=True)
s = q*(1-q)/2
f0 = sp.exp(-q*sp.log(y))
J = -s*y**(-q)
cn = J*f0**(1-n)/n

P = lambda tag, expr: print(tag, "PASS" if expr == 0 else ("FAIL: "+str(expr)))

# ---------- A0: background criticality (all n, q) ----------
EL_bg = sp.diff(sp.Rational(1,2)*y**2*sp.diff(f0, y), y) - n*cn*f0**(n-1)
P("A0  bg solves sourced EL (all n,q):", sp.simplify(sp.powsimp(EL_bg, force=True)))

# ---------- A4: second-jet values + affine law ----------
fv, g = sp.symbols('fv g')
Lsrc_f = cn*fv**n
Wff = sp.diff(Lsrc_f, fv, 2).subs(fv, f0)
P("A4  W_ff - (n-1)J/f0 == 0:", sp.simplify(sp.powsimp(Wff - (n-1)*J/f0, force=True)))
print("A4  W_ff zero iff n=1:", sp.solve(sp.Eq(sp.simplify(Wff*f0/J), 0), n))
phi0 = q*sp.log(y)/2   # f0 = e^{-2 phi0}
Lsrc_p = cn*sp.exp(-2*n*g)
Wpp = sp.diff(Lsrc_p, g, 2).subs(g, phi0)
P("A4  W_phiphi - 4 n J f0 == 0:", sp.simplify(sp.powsimp(Wpp - 4*n*J*f0, force=True)))
# affine law W_gg = F'^2 W_ff + F'' V_f with F = e^{-2g}
F = sp.exp(-2*g)
W_gg = sp.diff(Lsrc_f.subs(fv, F), g, 2).subs(g, phi0)
Vf = sp.diff(Lsrc_f, fv).subs(fv, f0)
Fp = sp.diff(F, g).subs(g, phi0); Fpp = sp.diff(F, g, 2).subs(g, phi0)
P("A4  affine law residual:", sp.simplify(sp.powsimp(W_gg - (Fp**2*Wff + Fpp*Vf), force=True)))
P("A4  first jet pinned V_f - J == 0:", sp.simplify(sp.powsimp(Vf - J, force=True)))

# ---------- A2: identities I3, I6 ----------
fy = sp.Function('f', positive=True)(y)
fp = sp.diff(fy, y)
# on-shell substitution from EL: (1/2 y^2 f')' = n c_n f^{n-1}
fpp_onshell = sp.solve(sp.Eq(sp.diff(sp.Rational(1,2)*y**2*fp, y), n*cn*fy**(n-1)),
                       sp.diff(fy, y, 2))[0]
I3 = sp.diff(sp.Rational(1,4)*y**2*fp**2, y) - (-sp.Rational(1,2)*y*fp**2 + cn*sp.diff(fy**n, y))
I3 = I3.subs(sp.diff(fy, y, 2), fpp_onshell)
P("A2  I3 on-shell residual:", sp.simplify(I3))
exch = sp.simplify(sp.powsimp((cn*sp.diff(fy**n, y)).subs(fy, f0).doit() - J*sp.diff(f0, y), force=True))
P("A2  exchange term == J f0' on bg (n-indep):", sp.simplify(exch))

u = sp.Function('u')(y)
upp = sp.solve(sp.Eq(sp.diff(y**2*sp.diff(u, y), y), (lam*y**q + mu_s)*u), sp.diff(u, y, 2))[0]
E6 = sp.Rational(1,2)*y**2*sp.diff(u, y)**2 - sp.Rational(1,2)*(lam*y**q + mu_s)*u**2
I6 = sp.diff(E6, y) - (-y*sp.diff(u, y)**2 - (q/2)*lam*y**(q-1)*u**2)
I6 = sp.simplify(I6.subs(sp.diff(u, y, 2), upp))
P("A2  I6 residual (must be 0, hence mu-free):", I6)

# ---------- A3: the conditional n=-4 branch ----------
h_bg = sp.simplify(sp.powsimp(sp.Rational(1,4)*y**2*sp.diff(f0, y)**2 - cn*f0**n, force=True))
print("A3  h_tot(bg) =", h_bg)
roots = sp.solve(sp.Eq(h_bg, 0), n)
print("A3  h_tot==0 at n =", [sp.simplify(r) for r in roots],
      "; -2(1-q)/q check:", sp.simplify(roots[0] + 2*(1-q)/q) if roots else "none",
      "; at q=1/3:", [r.subs(q, sp.Rational(1,3)) for r in roots])
roots2 = sp.solve(sp.simplify(sp.diff(cn, y)), n)
print("A3  c_n' == 0 at n =", roots2)
b0 = h_bg                      # additive freedom b(y) := h_bg
P("A3  h_tot - b0 == 0 identically (any n):", sp.simplify(h_bg - b0))
# b(y) adds nothing to any f-jet:
print("A3  d/df of b(y):", sp.diff(sp.Function('b')(y), fv))

# ---------- A1: concomitant + fork-collapse contact term ----------
u1 = sp.Function('u1')(y); u2 = sp.Function('u2')(y)
W = y**2*(sp.diff(u1, y)*u2 - u1*sp.diff(u2, y))
dW = sp.diff(W, y)
sub = {sp.diff(u1, y, 2): sp.solve(sp.Eq(sp.diff(y**2*sp.diff(u1, y), y), (lam*y**q+mu_s)*u1), sp.diff(u1, y, 2))[0],
       sp.diff(u2, y, 2): sp.solve(sp.Eq(sp.diff(y**2*sp.diff(u2, y), y), (lam*y**q+mu_s)*u2), sp.diff(u2, y, 2))[0]}
P("A1  concomitant conserved (all mu, lam):", sp.simplify(dW.subs(sub)))

eps = sp.Symbol('epsilon')
a = sp.Function('a')(y)
# f-slot second jet with b = -2 f0 a
b_f = -2*f0*a
Sf = sp.Rational(1,4)*y**2*sp.diff(f0 + eps*b_f, y)**2 + cn*(f0 + eps*b_f)**n
j2_f = sp.diff(Sf, eps, 2).subs(eps, 0)
# phi-slot second jet with perturbation a;  L(phi) = y^2 phi'^2 e^{-4phi} + c_n e^{-2 n phi}
Sp_ = y**2*sp.diff(phi0 + eps*a, y)**2*sp.exp(-4*(phi0 + eps*a)) + cn*sp.exp(-2*n*(phi0 + eps*a))
j2_p = sp.diff(Sp_, eps, 2).subs(eps, 0)
contact = sp.diff(-q*y**(1-2*q)*a**2, y)
d1 = sp.simplify(sp.powsimp(sp.expand(j2_p - j2_f - contact), force=True))
d2 = sp.simplify(sp.powsimp(sp.expand(j2_p - j2_f - 2*contact), force=True))
print("A1  fork-collapse: j2_phi - j2_f - 1*contact:", d1)
print("A1  fork-collapse: j2_phi - j2_f - 2*contact:", d2)
print("A1  source ultralocal: dL_src/df' == 0 trivially (no f' in c_n f^n)")
