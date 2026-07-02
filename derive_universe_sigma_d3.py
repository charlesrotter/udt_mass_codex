"""D3(a)(b) — phi-blind bulk source sigma(r): what a real matter action forces.
Banked geometric L: L_geo = (Z/2)rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2.
General phi-blind reduced matter: L_m = L_m(rho, rho', psi, psi')  (NO phi anywhere).
Checks:
 A. sigma formula: rho'' = 2phi'rho' - (Z/4)rho e^{2phi}phi'^2 + sigma with
    sigma = (e^{2phi}/4) [ d/dr(dL_m/drho') - dL_m/drho ]   (general),
          = -(e^{2phi}/4) dL_m/drho                          (rho'-independent L_m);
    banked winding form reproduced exactly.
 B. phi-EL untouched by ANY phi-blind L_m  ->  flux law robust (T1's tooth).
 C. E_tot = E_geo + E_m conserved for the general quadratic-velocity family
    L_m = -K2(rho,psi,velocities) - U(rho,psi) type (winding shape: L_m = -Khat - Uhat),
    with E_m = -Khat + Uhat  (Legendre); reproduces the R3 doc's H_m for winding.
 D. flux-budget identity: with even fold at rc (phi'=rho'=0) and odd fold at rs
    (phi=0, rho'=0, matter momenta zero at both folds):
        q^2/(2 Z rho_s^2) = E_m(rc) - E_m(rs)   and  q >= 0.
 E. realizability: potential-only U(rho) gives sigma = -(e^{2phi}/4) U'(rho);
    both signs realizable (no universal sign); the banked winding sigma is a signed
    difference of nonneg-invariant terms.
"""
import sympy as sp

r = sp.Symbol('r', real=True)
Z, xi, kap, N = sp.symbols('Z xi kappa N', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho')(r); psi = sp.Function('psi')(r)
Pp, Rp, Sp_ = phi.diff(r), rho.diff(r), psi.diff(r)

OK = []
def check(name, expr_zero):
    val = sp.simplify(expr_zero)
    ok = (val == 0)
    OK.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  residual={val}"))

L_geo = Z/2*rho**2*Pp**2 - 2*sp.exp(-2*phi)*Rp**2 + 2

def EL(L, q):
    return sp.diff(L, q.diff(r)).diff(r) - sp.diff(L, q)

# ---------- A. sigma formula ----------
# A1 (general, incl. rho'-dependence) verified on the general quadratic-velocity family
# L_m = -(A/2 psi'^2 + B rho'psi' + C/2 rho'^2) - U  with arbitrary A,B,C,U(rho,psi):
A_ = sp.Function('A')(rho, psi); B_ = sp.Function('B')(rho, psi)
C_ = sp.Function('C')(rho, psi); U_ = sp.Function('U')(rho, psi)
Lm_g = -(A_/2*psi.diff(r)**2 + B_*Rp*psi.diff(r) + C_/2*Rp**2) - U_
els_g = [EL(L_geo + Lm_g, f) for f in (phi, rho, psi)]
sol_g = sp.solve(els_g, [phi.diff(r,2), rho.diff(r,2), psi.diff(r,2)], dict=True)[0]
sig_claim = (sp.exp(2*phi)/4)*(sp.diff(sp.diff(Lm_g, Rp), r) - sp.diff(Lm_g, rho))
claim = 2*Pp*Rp - Z/4*rho*sp.exp(2*phi)*Pp**2 + sig_claim
check("A1: rho'' = 2phi'rho' - (Z/4)rho e^{2phi}phi'^2 + (e^{2phi}/4)[(dLm/drho')' - dLm/drho] (general family, on-shell)",
      sp.simplify(sol_g[rho.diff(r,2)] - claim.subs(sol_g).doit()))

# rho'-independent L_m: sigma = -(e^{2phi}/4) dL_m/drho
Lm2 = sp.Function('V')(rho, psi)
el_rho2 = EL(L_geo + Lm2, rho)
rho_pp2 = sp.solve(el_rho2, rho.diff(r,2))[0]
sig2 = sp.simplify(rho_pp2 - (2*Pp*Rp - Z/4*rho*sp.exp(2*phi)*Pp**2))
check("A2: rho'-independent L_m -> sigma = -(e^{2phi}/4) dL_m/drho",
      sp.simplify(sig2 + sp.exp(2*phi)/4*sp.diff(Lm2, rho)))

# banked winding: L_m = -(xi/2)(rho^2 Ir + Ith + N^2 Is) - (kap N^2/2)(I4r + I4th/rho^2)
Ir, Ith, Is, I4r, I4th = sp.symbols('I_r I_theta I_s I_4r I_4theta', nonnegative=True)
Lm_w = -(xi/2)*(rho**2*Ir + Ith + N**2*Is) - kap*N**2/2*(I4r + I4th/rho**2)
el_rho_w = EL(L_geo + Lm_w, rho)   # moments treated as fixed functionals (rho-dependence explicit)
rho_pp_w = sp.solve(el_rho_w, rho.diff(r,2))[0]
sig_w = sp.simplify(rho_pp_w - (2*Pp*Rp - Z/4*rho*sp.exp(2*phi)*Pp**2))
check("A3: banked winding sigma = (e^{2phi}/4)(xi rho I_r - kap N^2 I_4th / rho^3)",
      sp.simplify(sig_w - sp.exp(2*phi)/4*(xi*rho*Ir - kap*N**2*I4th/rho**3)))

# ---------- B. phi-EL untouched ----------
check("B1: d(L_m)/dphi = 0 and d(L_m)/dphi' = 0 for any phi-blind L_m (flux law robust)",
      sp.diff(Lm_g, phi) + sp.diff(Lm_g, Pp))
el_phi = EL(L_geo + Lm_g, phi)
check("B2: phi-EL with matter == phi-EL without matter (exactly)",
      sp.expand(el_phi - EL(L_geo, phi)))

# ---------- C. E_tot conservation, general quadratic-velocity family ----------
A_ = sp.Function('A')(rho, psi); B_ = sp.Function('B')(rho, psi)
C_ = sp.Function('C')(rho, psi); U_ = sp.Function('U')(rho, psi)
Lm_q = -(A_/2*Sp_**2 + B_*Rp*Sp_ + C_/2*Rp**2) - U_     # winding shape: L_m = -Khat - Uhat
Ltot_q = L_geo + Lm_q
E_tot = (Pp*sp.diff(Ltot_q, Pp) + Rp*sp.diff(Ltot_q, Rp) + Sp_*sp.diff(Ltot_q, Sp_)) - Ltot_q
E_m = (Rp*sp.diff(Lm_q, Rp) + Sp_*sp.diff(Lm_q, Sp_)) - Lm_q
check("C1: E_m = -Khat + Uhat  (Legendre flips the velocity block, keeps +U)",
      sp.simplify(E_m - (-(A_/2*Sp_**2 + B_*Rp*Sp_ + C_/2*Rp**2) + U_)))
# on-shell conservation: solve the three ELs for (phi'', rho'', psi'') and substitute
els = [EL(Ltot_q, f) for f in (phi, rho, psi)]
sol = sp.solve(els, [phi.diff(r,2), rho.diff(r,2), psi.diff(r,2)], dict=True)[0]
dEtot = sp.simplify(E_tot.diff(r).subs(sol))
check("C2: dE_tot/dr = 0 on-shell (r-translation invariance; autonomous L_m)", dEtot)
# winding H_m at the R3-doc level: E_m with Khat=(xi/2)rho^2 I_r + (kap N^2/2) I_4r,
# Uhat=(xi/2)(Ith+N^2 Is) + (kap N^2/2) I_4th/rho^2  ->  matches doc's H_m. (structural, C1)

# ---------- D. flux budget + sign of q ----------
q, rho_s, Em_c, Em_s = sp.symbols('q rho_s E_m^c E_m^s', real=True)
E_geo = Z/2*rho**2*Pp**2 - 2*sp.exp(-2*phi)*Rp**2
E_geo_rc = E_geo.subs({Pp: 0, Rp: 0})                      # even fold
E_geo_rs = E_geo.subs({phi: 0, Rp: 0, Pp: q/(Z*rho**2)})   # odd fold, q = Z rho^2 phi'
budget = sp.Eq(E_geo_rc + Em_c, sp.simplify(E_geo_rs.subs(rho, rho_s)) + Em_s)
check("D1: conservation across the cell -> q^2/(2 Z rho_s^2) = E_m(rc) - E_m(rs)",
      sp.simplify((budget.rhs - budget.lhs) - (q**2/(2*Z*rho_s**2) - (Em_c - Em_s))))
print("   D2 (logic, CAS-anchored): Phi(rc)=Z rho_c^2 * 0 = 0, Phi' = 4e^{-2phi}rho'^2 >= 0")
print("   for ANY phi-blind source (B2)  =>  q = Phi(rs) >= 0, strict > 0 iff rho' not== 0.")

# ---------- E. realizability / sign structure ----------
Urho = sp.Function('U')(rho)
sig_U = -sp.exp(2*phi)/4*sp.diff(-Urho, rho)   # L_m = -U(rho): sigma = +(e^{2phi}/4)U'(rho)
print("   E1: potential-only L_m=-U(rho):  sigma = (e^{2phi}/4) U'(rho); U'(rho) free of sign")
sigA = sig_U.subs(sp.diff(Urho, rho),  2*rho)  # U=rho^2
sigB = sig_U.subs(sp.diff(Urho, rho), -2*rho)  # U=-rho^2
check("E2: U=+rho^2 gives sigma>0-type (+e^{2phi}rho/2), U=-rho^2 the negative -> both signs realizable",
      sp.simplify(sigA - sp.exp(2*phi)*rho/2) + sp.simplify(sigB + sp.exp(2*phi)*rho/2))

print(f"\n{sum(OK)}/{len(OK)} checks passed")
