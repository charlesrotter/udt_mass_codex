"""sf_cas1_bulk.py -- CAS checks for the stability-filter operator derivation, part 1 (bulk).

Checks:
 C1  L reproduces the T3 solver EOMs (repo sign convention wins).
 C2  H = p.q' - L reproduces the solver's H_seal expression ((Z/2)rho^2 phi'^2 - 2e^{-2phi}rho'^2 - 2 + U).
 C3  The second-order Taylor of L gives the bulk quadratic form with coefficients
     A=(Z/2)rho^2, B=-2e^{-2phi}, C=Z rho phi', D=4e^{-2phi}rho', E=-4e^{-2phi}rho'^2,
     F=(Z/2)phi'^2 - U''/2, and NO u'v' cross-kinetic, NO u u', v v', u v terms.
 C4  The Euler-Lagrange equations of Q_bulk == the linearization of the EOMs (Jacobi system).
 C5  deltaH for a perturbation (u,v); at the even fold (phi'=rho'=0): deltaH = U'(rho_c) v.
 C6  At the odd fold (phi=0, rho'=0): deltaH = q u' + (Z rho phi'^2 + U') v, q = Z rho^2 phi'.
 C7  The natural-BC identity at r_s: phi'_s * [Z rho^2 u' + 2 Z rho phi' v] - L_rho v == deltaH(r_s)
     (given phi_s=0, rho'_s=0), i.e. the outer natural BC IS linearized transversality.
"""
import sympy as sp

r, Z, eps = sp.symbols('r Z epsilon', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho')(r)
u = sp.Function('u')(r); v = sp.Function('v')(r)
Uf = sp.Function('U')

def Lag(p, q):  # p=phi-like, q=rho-like
    return sp.Rational(1,2)*Z*q**2*sp.diff(p,r)**2 - 2*sp.exp(-2*p)*sp.diff(q,r)**2 + 2 - Uf(q)

L = Lag(phi, rho)
pphi = sp.diff(L, sp.diff(phi, r)); prho = sp.diff(L, sp.diff(rho, r))

# C1: EOMs
EL_phi = sp.diff(pphi, r) - sp.diff(L, phi)
EL_rho = sp.diff(prho, r) - sp.diff(L, rho)
phipp_sol = sp.solve(EL_phi, sp.diff(phi, r, 2))[0]
rhopp_sol = sp.solve(EL_rho, sp.diff(rho, r, 2))[0]
solver_phipp = 4*sp.exp(-2*phi)*sp.diff(rho,r)**2/(Z*rho**2) - 2*sp.diff(phi,r)*sp.diff(rho,r)/rho
solver_rhopp = (2*sp.diff(phi,r)*sp.diff(rho,r) - sp.Rational(1,4)*Z*rho*sp.exp(2*phi)*sp.diff(phi,r)**2
                + sp.exp(2*phi)/4*sp.diff(Uf(rho), rho))
print("C1 phi-EOM matches solver:", sp.simplify(phipp_sol - solver_phipp) == 0)
print("C1 rho-EOM matches solver:", sp.simplify(rhopp_sol - solver_rhopp) == 0)

# C2: H
H = pphi*sp.diff(phi,r) + prho*sp.diff(rho,r) - L
H_solver = sp.Rational(1,2)*Z*rho**2*sp.diff(phi,r)**2 - 2*sp.exp(-2*phi)*sp.diff(rho,r)**2 - 2 + Uf(rho)
print("C2 H matches solver H_seal form:", sp.simplify(H - H_solver) == 0)

# C3: second-order expansion
Lpert = Lag(phi + eps*u, rho + eps*v)
Q2 = sp.diff(Lpert, eps, 2).subs(eps, 0) / 2       # (1/2) d^2/deps^2 = quadratic integrand
Q2 = sp.expand(Q2)
A = sp.Rational(1,2)*Z*rho**2
B = -2*sp.exp(-2*phi)
Cc = Z*rho*sp.diff(phi,r)
D = 4*sp.exp(-2*phi)*sp.diff(rho,r)
E = -4*sp.exp(-2*phi)*sp.diff(rho,r)**2
F = sp.Rational(1,2)*Z*sp.diff(phi,r)**2 - sp.Rational(1,2)*sp.diff(Uf(rho), rho, 2)
Q_target = (A*sp.diff(u,r)**2 + B*sp.diff(v,r)**2 + 2*Cc*sp.diff(u,r)*v + 2*D*u*sp.diff(v,r)
            + E*u**2 + F*v**2)
print("C3 bulk quadratic integrand matches A..F form:", sp.simplify(Q2 - Q_target) == 0)
# cross-kinetic absent:
print("C3 no u'v' term:", sp.simplify(sp.diff(Q2, sp.diff(u,r), sp.diff(v,r))) == 0)

# C4: EL of Q_bulk == linearized EOMs (on-shell background)
Ju = sp.diff(sp.diff(Q_target, sp.diff(u,r)), r) - sp.diff(Q_target, u)   # = 0 is u-Jacobi eq
Jv = sp.diff(sp.diff(Q_target, sp.diff(v,r)), r) - sp.diff(Q_target, v)
# linearize EOMs: substitute phi->phi+eps u, rho->rho+eps v into (EL_phi, EL_rho), take d/deps at 0
lin_phi = sp.diff(EL_phi.subs({phi: phi+eps*u, rho: rho+eps*v}, simultaneous=True), eps).subs(eps,0)
lin_rho = sp.diff(EL_rho.subs({phi: phi+eps*u, rho: rho+eps*v}, simultaneous=True), eps).subs(eps,0)
print("C4 u-Jacobi == (1/2? scale) linearized phi-EOM:", sp.simplify(Ju/2 - lin_phi/2) == 0,
      "| ratio check:", sp.simplify(Ju - lin_phi) == 0)
print("C4 v-Jacobi == linearized rho-EOM:", sp.simplify(Jv - lin_rho) == 0)

# C5/C6: deltaH
Hpert = H.subs({phi: phi+eps*u, rho: rho+eps*v}, simultaneous=True)
dH = sp.diff(Hpert, eps).subs(eps, 0)
dH = sp.expand(dH)
# even fold: phi'=rho'=0
even = {sp.diff(phi,r): 0, sp.diff(rho,r): 0}
dH_even = sp.simplify(dH.subs(even))
print("C5 deltaH(even fold) == U'(rho) v:", sp.simplify(dH_even - sp.diff(Uf(rho), rho)*v) == 0)
# odd fold: phi=0, rho'=0.  Symbolize point values first (subs of the Function would kill phi').
P, Pp, R, Rp, Uu, Uup, Vv, Vp = sp.symbols('P Pp R Rp uu uup vv vp')  # phi, phi', rho, rho', u, u', v, v'
sub_pt = [(sp.diff(phi,r), Pp), (sp.diff(rho,r), Rp), (sp.diff(u,r), Uup),
          (sp.diff(v,r), Vp), (phi, P), (rho, R), (u, Uu), (v, Vv)]
dH_pt = dH.subs(sub_pt)
dH_odd = dH_pt.subs({Rp: 0, P: 0})
q = Z*R**2*Pp
target_odd = q*Uup + (Z*R*Pp**2 + sp.diff(Uf(R), R))*Vv
print("C6 deltaH(odd fold) == q u' + (Z rho phi'^2 + U') v:", sp.simplify(dH_odd - target_odd) == 0)

# C7: natural-BC identity at r_s.  L_rho at the fold (phi=0, rho'=0):
L_rho_fold = sp.diff(L, rho).subs(sub_pt).subs({Rp: 0, P: 0})
lhs = Pp*(Z*R**2*Uup + 2*Z*R*Pp*Vv) - L_rho_fold*Vv
print("C7 phi'_s*(2A u' + 2C v) - L_rho v == deltaH(r_s):", sp.simplify(lhs - dH_odd) == 0)
