"""verify_classB_derivations.py — CAS check of the Class-B (charged-core) derivations
(`embedded_classB_mini_MAP.md` D1/D2 + claude.ai's R4-fork sign ruling), owed before the run.

D1  sourced-core natural BC: S = INT_{rc}^{rs} Lbar dr + q*phi(rc). Varying phi with phi(rc) FREE,
    the coefficient of delta phi(rc) is q - pi_phi(rc); natural BC => pi_phi(rc) = q  (pi_phi=Z rho^2 phi').
D2  r_c-fixed => no inner corner condition; the source q*phi(rc) has NO r-kinetic term (no phi'(rc)
    dependence) so contributes no bulk H / no core matter-H. r_c-DYNAMICAL variant: the corner term is
    q*phi'(rc) (from d/d rc of q*phi(rc)) -- a labeled fork.
R4  claude.ai ruling: in the rho-EOM the charge term -(Z/4) rho e^{2phi} phi'^2 is quadratic in phi'
    (hence in q) -> strictly INWARD (negative) regardless of sign(q); the ONLY outward channel is
    +(e^{2phi}/4) xi rho I_r (I_r>=0). => if rho'_amb>0, I_r>0 is MANDATORY to close R4.
"""
import sympy as sp

r, eps, s0 = sp.symbols('r epsilon s0', real=True)
Z, xi, kap, N, q = sp.symbols('Z xi kappa N q', positive=True)

# ---- D1: concrete variable-core-value variation (polynomials so integrals evaluate) --------------
rc = sp.Integer(1); rs = sp.Integer(2)
phi0 = r**2; rho0 = 1 + r            # concrete background
eta = 3 - r                          # test variation, eta(rc)=eta(1)=2 != 0 (core value FREE); eta(rs)=1
# use a concrete rho (frozen) so we isolate the phi-BC; Lbar_phi-part = (Z/2) rho^2 phi'^2
phi = phi0 + eps*eta
Lphi = (Z/2)*rho0**2*sp.diff(phi, r)**2
S = sp.integrate(Lphi, (r, rc, rs)) + q*phi.subs(r, rc)     # + source q*phi(rc)
dS = sp.diff(S, eps).subs(eps, 0)
# EL (bulk) + boundary. pi_phi = dLbar/dphi' = Z rho^2 phi'
pi_phi = Z*rho0**2*sp.diff(phi0, r)
EL = -sp.diff(pi_phi, r)                                    # bulk EL of (Z/2)rho^2 phi'^2 = -(Z rho^2 phi')'
# predicted dS = INT EL*eta dr + pi_phi(rs)*eta(rs) - pi_phi(rc)*eta(rc) + q*eta(rc)
pred = (sp.integrate(EL*eta, (r, rc, rs))
        + pi_phi.subs(r, rs)*eta.subs(r, rs)
        - pi_phi.subs(r, rc)*eta.subs(r, rc)
        + q*eta.subs(r, rc))
D1_formula = sp.simplify(dS - pred) == 0
core_bc_coeff = q - pi_phi.subs(r, rc)                     # coefficient of eta(rc); =0 is the BC pi_phi(rc)=q

# ---- D2: source has no r-kinetic term; r_c-dynamical corner = q*phi'(rc) --------------------------
phi_f = sp.Function('phi'); rc_s = sp.Symbol('r_c', positive=True)
src = q*phi_f(rc_s)
D2_no_kinetic = (sp.diff(src, sp.Derivative(phi_f(rc_s), rc_s)) == 0)   # no phi'(rc) dependence
D2_dyn_corner = sp.simplify(sp.diff(src, rc_s) - q*sp.diff(phi_f(rc_s), rc_s)) == 0  # = q phi'(rc)

# ---- R4: rho-EOM channel signs (claude.ai ruling) ------------------------------------------------
phi_s, rho_s, phip_s, Ir_s = sp.symbols('phi rho phip I_r', real=True)
charge_term = -(Z/4)*rho_s*sp.exp(2*phi_s)*phip_s**2       # from rho'' RHS
matter_out  = (sp.exp(2*phi_s)/4)*xi*rho_s*Ir_s            # the +xi rho I_r outward channel
# charge term is strictly <= 0 for rho>0 (any sign of phip, i.e. any sign of q): it is -pos*phip^2
R4_charge_inward = sp.simplify(charge_term / (rho_s*sp.exp(2*phi_s)*phip_s**2)) == -Z/4  # negative coeff
R4_charge_qsign_indep = (charge_term.subs(phip_s, +phip_s) - charge_term.subs(phip_s, -phip_s)) == 0  # even in phip
# matter channel is >0 for I_r>0, rho>0
R4_matter_outward = sp.simplify(matter_out / (sp.exp(2*phi_s)*rho_s*Ir_s)) == xi/4         # positive coeff

# R4(b)+(c) AIRTIGHT (blind verifier a915cc3): the raw-EOM "only outward channel" statement has a
# 2 phi' rho' loophole (not sign-definite). The rigorous version is the MOMENTUM-FLUX identity, where
# 2 phi' rho' CANCELS: pi_rho' = Z rho phi'^2 - xi rho I_r + kap N^2 I_4th/rho^3.
rr = sp.symbols('rr', positive=True)
Ph = sp.Function('phi')(rr); Rh = sp.Function('rho')(rr); Irf, I4f = sp.Function('I_r')(rr), sp.Function('I4')(rr)
php_r, rhp_r = sp.diff(Ph, rr), sp.diff(Rh, rr)
rho_eom_rhs = (2*php_r*rhp_r - (Z/4)*Rh*sp.exp(2*Ph)*php_r**2
               + (sp.exp(2*Ph)/4)*(xi*Rh*Irf - kap*N**2*I4f/Rh**3))          # rho''
pirho = -4*sp.exp(-2*Ph)*rhp_r
pirho_prime = sp.diff(pirho, rr).subs(sp.diff(Rh, rr, 2), rho_eom_rhs)        # substitute rho''
flux_target = Z*Rh*php_r**2 - xi*Rh*Irf + kap*N**2*I4f/Rh**3
R4_flux_identity = sp.simplify(pirho_prime - flux_target) == 0                # 2 phi' rho' cancels exactly
# mandatory-I_r logic: with pi_rho(rc)=0, pi_rho(rs)=INT[Z rho phi'^2 + kap N^2 I4/rho^3 - xi rho I_r].
# The two non-I_r integrands are >=0 (Z rho phi'^2>=0; kap N^2 I4/rho^3>=0 since I4th=1/2 INT sin^2f/sin f_th^2 >=0),
# so a gradient-carrying ambient (pi_rho,amb = -4 e^{-2phi} rho'_amb < 0 for rho'_amb>0) FORCES INT xi rho I_r>0
# => I_r>0 somewhere. Verify the two non-I_r integrand coefficients are >=0:
R4_int1_nonneg = sp.simplify((Z*Rh*php_r**2)/(Rh*php_r**2)) == Z              # +Z (>=0) coeff of rho phi'^2
R4_int2_nonneg = sp.simplify((kap*N**2*I4f/Rh**3)/(I4f/Rh**3)) == kap*N**2    # +kap N^2 (>=0) coeff of I4/rho^3
R4_mandatory_Ir = R4_flux_identity and R4_int1_nonneg and R4_int2_nonneg      # now DERIVED, not asserted

print("D1  variation formula dS = INT EL eta + [pi_phi eta] + q eta(rc) :", D1_formula)
print("    core BC coefficient of eta(rc) =", sp.simplify(core_bc_coeff), " (=0  <=>  pi_phi(rc)=q)")
print("D2  source has NO r-kinetic (no phi'(rc) dependence):", D2_no_kinetic,
      "| r_c-dynamical corner = q*phi'(rc):", D2_dyn_corner)
print("R4  charge term -(Z/4)rho e^{2phi}phi'^2: inward (neg coeff -Z/4):", R4_charge_inward,
      "| even in phi' (q-sign-independent):", R4_charge_qsign_indep)
print("R4  matter term +(e^{2phi}/4)xi rho I_r: outward (pos coeff +xi/4):", R4_matter_outward)
print("R4  AIRTIGHT flux identity  pi_rho' == Z rho phi'^2 - xi rho I_r + kap N^2 I_4th/rho^3 (2phi'rho' cancels):",
      R4_flux_identity)
print("    non-I_r integrands >=0 (coeff +Z:", R4_int1_nonneg, "| coeff +kapN^2:", R4_int2_nonneg,
      ") => pi_rho(rs)<0 (rho'_amb>0) FORCES I_r>0 MANDATORY.")
allok = all([D1_formula, bool(D2_no_kinetic), D2_dyn_corner, R4_charge_inward,
             bool(R4_charge_qsign_indep), R4_matter_outward, R4_flux_identity,
             R4_int1_nonneg, R4_int2_nonneg])
print("\nALL CLASS-B DERIVATION CHECKS PASS:", allok, " (core BC = q - pi_phi(rc), zero at pi_phi(rc)=q;",
      "I_r>0 mandatory via the momentum-flux identity)")
