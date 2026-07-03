"""bv13 W2 + W3(CAS part):
W2: linearized H; natural BC at r_s of the reduced quadratic form == deltaH(r_s)=0; inner pairing.
W3: quadratic integrand of the second variation; kinetic block diag((Z/2)rho^2, -2e^{-2phi}), no cross.
"""
import sympy as sp

Z = sp.Symbol('Z', positive=True)
phi, phip, rho, rhop = sp.symbols('phi phip rho rhop', real=True)
u, up, v, vp = sp.symbols('u up v vp', real=True)      # (delta phi, delta phi', delta rho, delta rho')
beta = sp.Symbol('beta', real=True)
Uf = sp.Function('U')

P, PP, R, RP = sp.symbols('P PP R RP')
L = (Z/2)*R**2*PP**2 - 2*sp.exp(-2*P)*RP**2 + 2 - Uf(R)
H = PP*sp.diff(L, PP) + RP*sp.diff(L, RP) - L
sub = {P: phi, PP: phip, R: rho, RP: rhop}

# ---- W2 chunk A: linearized H (exact, generic point) ----
eps = sp.Symbol('eps')
Hp = H.subs({P: P+eps*u, PP: PP+eps*up, R: R+eps*v, RP: RP+eps*vp}, simultaneous=True)
dH = sp.diff(Hp, eps).subs(eps, 0).subs(sub)
dH = sp.expand(dH)
print("[W2-A] deltaH generic =", sp.collect(dH, [u, up, v, vp]))
dH_s = sp.simplify(dH.subs({phi: 0, rhop: 0}))
print("[W2-A] deltaH(r_s) =", sp.collect(sp.expand(dH_s), [up, v]))
q = Z*rho**2*phip
claim_s = q*up + (Z*rho*phip**2 + sp.diff(Uf(rho), rho))*v
print("[W2-A] deltaH(r_s) - [q u' + (Z rho phip^2 + U')v] =", sp.simplify(dH_s - claim_s))
dH_c = sp.simplify(dH.subs({phip: 0, rhop: 0}))
print("[W2-A] deltaH(r_c) =", dH_c, "  (claim: U'(rho_c) v(0))")

# ---- W3 chunk: quadratic integrand (generic point), kinetic block ----
Lp = L.subs({P: P+eps*u, PP: PP+eps*up, R: R+eps*v, RP: RP+eps*vp}, simultaneous=True)
quad = sp.expand(sp.diff(Lp, eps, 2).subs(eps, 0)/2).subs(sub)   # (1/2) d^2L/deps^2 = quadratic part
quad = sp.collect(sp.expand(quad), [up**2, vp**2, up*vp, u*up, v*up, u*vp, v*vp, u**2, v**2, u*v])
print("[W3-CAS] quadratic integrand (1/2)delta2L =")
for mono in [up**2, vp**2, up*vp, v*up, u*vp, u*up, v*vp, u*v, u**2, v**2]:
    c = quad.coeff(mono) if mono.is_Mul or mono.is_Pow else None
    print("   coeff", mono, "=", sp.simplify(quad.coeff(mono)))
print("[W3-CAS] kinetic block: coeff up^2 =", sp.simplify(quad.coeff(up**2)),
      "; coeff vp^2 =", sp.simplify(quad.coeff(vp**2)),
      "; CROSS up*vp =", sp.simplify(quad.coeff(up*vp)))

# ---- W2 chunk B: natural BC at r_s from the reduced form ----
# Reduced form (1/2)S'' = int quad dr + L_rho(r_s) beta v(r_s) + U'(rho_c) alpha v(0),
# subject to essential u(r_s) = -phip_s beta.  Vary beta (and u(r_s) with it):
# boundary term from u-variation at r_s: (d quad/d up)|_{r_s} * delta u(r_s) = (...)*(-phip_s dbeta)
# plus explicit L_rho(r_s) v(r_s) dbeta.  Collect -> compare with deltaH(r_s).
dquad_dup = sp.diff(quad, up)
bnd_u_s = sp.simplify(dquad_dup.subs({phi: 0, rhop: 0}))
print("[W2-B] (d quad/d u')|_{r_s} =", bnd_u_s)
Lrho_s = (Z*rho*phip**2 - sp.diff(Uf(rho), rho))
nbc_beta = sp.expand(bnd_u_s*(-phip) + Lrho_s*v)
print("[W2-B] beta natural BC expression =", sp.collect(nbc_beta, [up, v]))
# claim: this equals -(deltaH(r_s)) with u(r_s)=-phip beta eliminated... compare directly:
print("[W2-B] beta-NBC + deltaH(r_s) =", sp.simplify(nbc_beta + dH_s))
# ---- W2 chunk C: alpha natural BC (inner pairing) ----
print("[W2-C] alpha-variation gives U'(rho_c) v(0) = deltaH(r_c):",
      sp.simplify(dH_c - sp.diff(Uf(rho), rho)*v) == 0)
