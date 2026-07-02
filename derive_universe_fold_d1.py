"""D1 — fold junction conditions, CAS verification.
Banked reduced system (repo-confirmed):
  L_P = (Z/2) rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2      (Branch P, W=1)
  L_G = (Z/2) rho^2 phi'^2 - 2 rho'^2 + 2                (Branch G, W=e^{2phi})
Checks:
 A. reduction from native action integrand (round h = rho^2 Omega)
 B. EL equations match banked EOMs; E first integral; flux law Phi'=4e^{-2phi}rho'^2
    robust to ANY phi-blind rho''-source
 C. pointwise identification (phi->-phi, rho->g(rho,phi), optional radial weight w):
    phi-kinetic forces g=rho and the R^(2) constant forces w=1; then L_P is NOT
    invariant (residual -4 sinh(2phi) rho'^2) while L_G IS invariant.
 D. mirrored bulk extension violates the P EOMs unless rho'=0 (flux-monotonicity clash);
    exact bulk symmetry in G.
 E. IBP identity underlying boundary-term collection; doubled-action momenta at the fold;
    variable-endpoint (transversality) identity; fold values of E, Phi, H.
"""
import sympy as sp

r, u, rs, Z, sig = sp.symbols('r u r_s Z sigma', real=True, positive=False)
Zp = sp.Symbol('Z', positive=True)

phi = sp.Function('phi')
rho = sp.Function('rho')
P, R = phi(r), rho(r)
Pp, Rp = P.diff(r), R.diff(r)

OK = []

def check(name, expr_zero):
    val = sp.simplify(expr_zero)
    OK.append((name, val == 0 or val == sp.S.Zero, val))
    print(f"[{'PASS' if OK[-1][1] else 'FAIL'}] {name}" + ("" if OK[-1][1] else f"  residual={val}"))

# ---------- A. reduction from the native action ----------
theta = sp.Symbol('theta')
# h_AB = diag(rho^2, rho^2 sin^2 theta); sqrt(h) = rho^2 sin(theta)
hAB = sp.Matrix([[R**2, 0],[0, R**2*sp.sin(theta)**2]])
sqrth = sp.sqrt(sp.det(hAB))          # rho^2 sin(theta) (rho>0, 0<theta<pi assumed)
sqrth = R**2*sp.sin(theta)
R2 = 2/R**2                            # intrinsic curvature of round sphere radius rho
KAB = sp.Rational(1,2)*sp.exp(-P)*hAB.diff(r)
Kud = hAB.inv()*KAB                    # K^A_B
K = sp.trace(Kud)
KK = sp.trace(Kud*Kud)
scrK = sp.simplify(KK - K**2)
check("A1: scrK = -2 e^{-2phi} rho'^2/rho^2", scrK + 2*sp.exp(-2*P)*Rp**2/R**2)
# reduced L per sin(theta): rho^2 * [ (Z/2)phi'^2 + R2 + W*scrK ]
L_P = sp.expand(R**2*(Zp/2*Pp**2 + R2 + 1*scrK))
L_G = sp.expand(R**2*(Zp/2*Pp**2 + R2 + sp.exp(2*P)*scrK))
check("A2: L_P = (Z/2)rho^2 phi'^2 - 2e^{-2phi}rho'^2 + 2",
      L_P - (Zp/2*R**2*Pp**2 - 2*sp.exp(-2*P)*Rp**2 + 2))
check("A3: L_G = (Z/2)rho^2 phi'^2 - 2rho'^2 + 2",
      L_G - (Zp/2*R**2*Pp**2 - 2*Rp**2 + 2))

# ---------- B. EL equations, E, flux law ----------
def EL(L, q):
    return sp.diff(L, q.diff(r)).diff(r) - sp.diff(L, q)

elphi = sp.simplify(EL(L_P, P))    # = d/dr(Z rho^2 phi') - 4 e^{-2phi} rho'^2
elrho = sp.simplify(EL(L_P, R))
# banked EOMs
phipp_b = 4*sp.exp(-2*P)*Rp**2/(Zp*R**2) - 2*Pp*Rp/R
rhopp_b = 2*Pp*Rp - Zp/4*R*sp.exp(2*P)*Pp**2
sol = sp.solve([elphi, elrho], [P.diff(r,2), R.diff(r,2)], dict=True)[0]
check("B1: EL_phi gives banked phi''", sp.simplify(sol[P.diff(r,2)] - phipp_b))
check("B2: EL_rho gives banked rho''", sp.simplify(sol[R.diff(r,2)] - rhopp_b))

E = sp.expand(Pp*sp.diff(L_P, Pp) + Rp*sp.diff(L_P, Rp) - L_P)  # Legendre
check("B3: E+2 = (Z/2)rho^2 phi'^2 - 2e^{-2phi}rho'^2  (H=E_doc-2 convention)",
      E - (Zp/2*R**2*Pp**2 - 2*sp.exp(-2*P)*Rp**2 - 2))
# conservation on-shell WITH an arbitrary phi-blind rho'' source S(r):
S = sp.Function('S')(r)
subs_src = {P.diff(r,2): phipp_b, R.diff(r,2): rhopp_b + S}
dE = sp.simplify(E.diff(r).subs(subs_src))
print("   dE/dr with arbitrary rho''-source S:", sp.simplify(dE))
check("B4: dE/dr = -4 e^{-2phi} rho' S  (E_geo conserved iff S=0; source term exact)",
      sp.simplify(dE + 4*sp.exp(-2*P)*Rp*S))
Phi = Zp*R**2*Pp
check("B5: flux law Phi' = 4 e^{-2phi} rho'^2 for ANY rho''-source",
      sp.simplify(Phi.diff(r).subs(subs_src) - 4*sp.exp(-2*P)*Rp**2))

# ---------- C. pointwise identification class ----------
# jet-level involution: phi -> -phi, phi' -> +phi' (odd field, reflected coordinate),
# rho -> g(rho,phi), rho' -> -(g_rho rho' + g_phi phi'); radial weight w(r) (reparam).
p_, pp_, r_, rp_ = sp.symbols('p pp rho rhop', real=True)
g = sp.Function('g')(r_, p_)
w = sp.Symbol('w', positive=True)
Ljet = lambda p, pp, rho_, rhop_: Zp/2*rho_**2*pp**2 - 2*sp.exp(-2*p)*rhop_**2 + 2
gt = -(g.diff(r_)*rp_ + g.diff(p_)*pp_)
# w-reparametrized pullback of one copy: w * L(phit, phit'/w, rhot, rhot'/w)
Ltil = sp.expand(w*Ljet(-p_, pp_/w, g, gt/w))
Lorig = Ljet(p_, pp_, r_, rp_)
diff_ = sp.expand(Ltil - Lorig)
poly = sp.Poly(diff_, pp_, rp_)
c_const = poly.coeff_monomial(1)
c_pp2 = poly.coeff_monomial(pp_**2)
c_rp2 = poly.coeff_monomial(rp_**2)
c_cross = poly.coeff_monomial(pp_*rp_)
print("   invariance conditions (must all vanish):")
print("    const:", sp.simplify(c_const), "  -> w = 1")
print("    phi'^2:", sp.simplify(c_pp2))
print("    phi'rho':", sp.simplify(c_cross), " -> g_rho g_phi = 0")
print("    rho'^2:", sp.simplify(c_rp2))
# impose w=1, g_phi=0 (g_rho=0 kills rho-dependence of the phi'^2 coeff -> dead):
c_pp2_1 = sp.simplify(c_pp2.subs({w:1, g.diff(p_):0}))
check("C1: [w=1, g_phi=0] phi'^2-coeff = (Z/2)(g^2-rho^2) -> g = rho",
      c_pp2_1 - Zp/2*(g**2 - r_**2))
c_rp2_1 = sp.simplify(c_rp2.subs({w:1, g.diff(p_):0, g.diff(r_):1, g:r_}))
check("C2: with g=rho the rho'^2 residual = 2e^{-2phi} - 2e^{2phi} = -4 sinh(2phi) != 0",
      c_rp2_1 - (2*sp.exp(-2*p_) - 2*sp.exp(2*p_)))
# Branch G: same test
LjetG = lambda p, pp, rho_, rhop_: Zp/2*rho_**2*pp**2 - 2*rhop_**2 + 2
diffG = sp.expand(LjetG(-p_, pp_, r_, -rp_) - LjetG(p_, pp_, r_, rp_))
check("C3: L_G exactly invariant under the odd fold (g=rho, w=1)", diffG)

# ---------- D. mirrored bulk extension vs the EOMs (jet level, exact) ----------
# Chain rule for phit(r) = -phi(2rs-r), rhot(r) = rho(2rs-r) at the mirrored point:
#   (phit, phit', phit'') = (-p0, +f1, -f2) ; (rhot, rhot', rhot'') = (r0, -g1, +g2)
p0,f1,f2,r0g,g1,g2 = sp.symbols('p0 f1 f2 r0 g1 g2', real=True)
f2P = 4*sp.exp(-2*p0)*g1**2/(Zp*r0g**2) - 2*f1*g1/r0g        # banked P phi''
g2P = 2*f1*g1 - Zp/4*r0g*sp.exp(2*p0)*f1**2                  # banked P rho''
resP_phi = ((-f2) - (4*sp.exp(2*p0)*g1**2/(Zp*r0g**2) + 2*f1*g1/r0g)).subs(f2, f2P)
check("D1a: odd-mirror P phi-residual = -(4 rho'^2/(Z rho^2))(e^{-2phi}+e^{2phi}) [zero iff rho'=0]",
      sp.expand(sp.simplify(resP_phi).rewrite(sp.exp)
                + 4*g1**2*(sp.exp(-2*p0)+sp.exp(2*p0))/(Zp*r0g**2)))
resP_rho = (g2 - (-2*f1*g1 - Zp/4*r0g*sp.exp(-2*p0)*f1**2)).subs(g2, g2P)
check("D1b: odd-mirror P rho-residual = 4 phi'rho' + (Z/4)rho phi'^2(e^{-2phi}-e^{2phi})",
      sp.simplify(resP_rho - (4*f1*g1 + Zp/4*r0g*f1**2*(sp.exp(-2*p0)-sp.exp(2*p0)))))
f2G = -2*f1*g1/r0g; g2G = -Zp/4*r0g*f1**2                    # banked G EOMs
check("D2: odd-mirror extension is an EXACT G-solution (phi-eq)",
      sp.simplify(((-f2) - (-2*f1*(-g1)/r0g)).subs(f2, f2G)))
check("D3: odd-mirror extension is an EXACT G-solution (rho-eq)",
      sp.simplify((g2 - (-Zp/4*r0g*f1**2)).subs(g2, g2G)))
# EVEN mirror jet in P: (p0, -f1, +f2), (r0, -g1, +g2)
check("D4: EVEN mirror extension is an EXACT P-solution (phi-eq)",
      sp.simplify((f2 - (4*sp.exp(-2*p0)*g1**2/(Zp*r0g**2) - 2*(-f1)*(-g1)/r0g)).subs(f2, f2P)))
check("D5: EVEN mirror extension is an EXACT P-solution (rho-eq)",
      sp.simplify((g2 - (2*(-f1)*(-g1) - Zp/4*r0g*sp.exp(2*p0)*f1**2)).subs(g2, g2P)))

# ---------- E. boundary-term machinery ----------
# E1: IBP identity  deltaL = -EL*eta + d/dr( p * eta )   (boundary-term collection)
eta_p = sp.Function('eta_phi')(r); eta_r = sp.Function('eta_rho')(r)
first_var = (sp.diff(L_P, P)*eta_p + sp.diff(L_P, Pp)*eta_p.diff(r)
             + sp.diff(L_P, R)*eta_r + sp.diff(L_P, Rp)*eta_r.diff(r))
elform = (-EL(L_P, P))*eta_p + (-EL(L_P, R))*eta_r \
         + sp.diff(sp.diff(L_P, Pp)*eta_p + sp.diff(L_P, Rp)*eta_r, r)
check("E1: first-variation = -EL*eta + d/dr(p*eta)  (boundary-term collection identity)",
      sp.expand(first_var - elform))

# E2: pullback of the partner copy across the odd fold (change of variables):
#     L[phihat,rhohat](r), r=2rs-u, phihat(r)=-phi(2rs-r), rhohat(r)=rho(2rs-r)
Ph = -phi(2*rs - r); Rh = rho(2*rs - r)
Lhat = Zp/2*Rh**2*Ph.diff(r)**2 - 2*sp.exp(-2*Ph)*Rh.diff(r)**2 + 2
Lhat_u = sp.simplify(Lhat.subs(r, 2*rs - u))    # integrand at the cell point u
Ltil_expected = Zp/2*rho(u)**2*phi(u).diff(u)**2 - 2*sp.exp(2*phi(u))*rho(u).diff(u)**2 + 2
check("E2: partner pullback = (Z/2)rho^2 phi'^2 - 2e^{+2phi}rho'^2 + 2 (the sign-flipped copy)",
      sp.simplify(Lhat_u - Ltil_expected))

# E3: doubled-action fold momenta (odd fold), evaluated with the fold pin phi(rs)=0:
Ltot = sp.expand(L_P + (Zp/2*R**2*Pp**2 - 2*sp.exp(2*P)*Rp**2 + 2))
p_tot_phi = sp.diff(Ltot, Pp)
p_tot_rho = sp.diff(Ltot, Rp)
check("E3a: p_tot_phi = 2 Z rho^2 phi'", p_tot_phi - 2*Zp*R**2*Pp)
check("E3b: p_tot_rho|_{phi=0} = -8 rho'  -> stationarity with free d(rho) pins rho'(rs)=0",
      p_tot_rho.subs(P, 0) + 8*Rp)

# E4: variable-endpoint identity  delta S_end = p*Dq - H*Drs  (algebraic identity):
pq, qp, Lsym, Drs, dq = sp.symbols('p q_prime L Delta_rs delta_q')
lhs = pq*dq + Lsym*Drs                       # boundary term from expanding S over moved endpoint
rhs = pq*(dq + qp*Drs) - (pq*qp - Lsym)*Drs  # p*(total endpoint variation) - H*Drs
check("E4: p*dq + L*Drs == p*Dq - H*Drs", sp.expand(lhs - rhs))

# E5: fold values of E, Phi, H (odd fold: phi=0, rho'=0):
q = sp.Symbol('q', real=True)
E_doc = Zp/2*R**2*Pp**2 - 2*sp.exp(-2*P)*Rp**2       # doc's E (no -2)
E_at_fold = E_doc.subs({P:0, Rp:0, Pp: q/(Zp*R**2)})
check("E5a: E(rs) = q^2/(2 Z rho_s^2)", sp.simplify(E_at_fold - q**2/(2*Zp*R**2)))
E_at_core = E_doc.subs({Pp:0, Rp:0})
check("E5b: E(rc) = 0 at the even mirror", E_at_core)
# H_geo = E_doc - 2; transversality H_tot(rs)=0 with matter Legendre E_m:
Em = sp.Symbol('E_m', real=True)
H_fold = E_at_fold - 2 + Em
print("   E6: free-fold transversality  H_tot(rs)=0  <=>  q^2/(2 Z rho_s^2) = 2 - E_m(rs):",
      sp.simplify(sp.solve(H_fold, q**2)[0]), "= q^2")

n_fail = sum(1 for _,ok,_ in OK if not ok)
print(f"\n{len(OK)-n_fail}/{len(OK)} checks passed")
