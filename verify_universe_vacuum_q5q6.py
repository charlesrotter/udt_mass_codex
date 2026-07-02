"""Q5: phi-blind matter vs the center obstruction. Q6: two-mirror conservation condition.
Matter (round S2 winding, repo round_matter_reduction_results.md):
  L_m = -(xi/2)(rho^2 I_r + I_th + N^2 I_s) - (kap N^2/2)(I_4r + I_4th/rho^2)
  theta-density: Lm(th) = -(xi/2)[rho^2 s f_r^2/2 + s f_th^2/2 + N^2 sin^2 f/(2s)]
                          -(kap N^2/2)[sin^2 f f_r^2/(2s) + sin^2 f f_th^2/(2 s rho^2)],  s=sin(th)
Geometry theta-density: Lg(th) = (s/2)[(Z/2)rho^2 phi'^2 - 2 e^{-2phi} rho'^2 + 2]
"""
import sympy as sp

r, th = sp.symbols('r theta')
Z, xi, kap, N = sp.symbols('Z xi kappa N', positive=True)
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
f = sp.Function('f')(r, th)
s = sp.sin(th)
phip, rhop = phi.diff(r), rho.diff(r)
fr, fth = f.diff(r), f.diff(th)

Lg = (s/2)*((Z/2)*rho**2*phip**2 - 2*sp.exp(-2*phi)*rhop**2 + 2)
Lm = -(xi/2)*(rho**2*s*fr**2/2 + s*fth**2/2 + N**2*sp.sin(f)**2/(2*s)) \
     - (kap*N**2/2)*(sp.sin(f)**2*fr**2/(2*s) + sp.sin(f)**2*fth**2/(2*s*rho**2))
Lam = Lg + Lm

print("="*70)
print("Check 0: EL equations of the summed density reproduce the banked EOMs")
# f-EL (2-D):  d/dr dL/df_r + d/dth dL/df_th - dL/df = 0
ELf = sp.diff(sp.diff(Lam, fr), r) + sp.diff(sp.diff(Lam, fth), th) - sp.diff(Lam, f)
A = xi*rho**2*s + kap*N**2*sp.sin(f)**2/s
B = xi*s + kap*N**2*sp.sin(f)**2/(rho**2*s)
banked_f = sp.diff(A*fr, r) + sp.diff(B*fth, th) \
           - (N**2*sp.sin(f)*sp.cos(f)/s)*(xi + kap*fr**2 + kap*fth**2/rho**2)
print("  -2*ELf - banked_f  =", sp.simplify(-2*ELf - banked_f), "  (0 => f-EOM matches repo)")

# rho-EL: theta-INTEGRATED. Do it with symbolic integrals via the I-coefficients:
Ir, I4th = sp.symbols('I_r I_4theta', positive=True)
LG = (Z/2)*rho**2*phip**2 - 2*sp.exp(-2*phi)*rhop**2 + 2
LM = -(xi/2)*(rho**2*Ir) - (kap*N**2/2)*(I4th/rho**2)   # only rho-dependent pieces matter
LT = LG + LM
EL_rho = sp.diff(sp.diff(LT, rhop), r) - sp.diff(LT, rho)
# solve for rho'':
rpp = sp.solve(sp.Eq(EL_rho, 0), rho.diff(r, 2))[0]
banked_rpp = 2*phip*rhop - (Z/4)*rho*sp.exp(2*phi)*phip**2 \
             + (sp.exp(2*phi)/4)*(xi*rho*Ir - kap*N**2*I4th/rho**3)
print("  rho'' from EL - banked rho''(matter) =", sp.simplify(rpp - banked_rpp),
      " (0 => matter rho-source matches repo EXACTLY, incl. e^{2phi}/4)")

# phi-EL: matter must be ABSENT (phi-blind)
print("  dLm/dphi =", sp.diff(Lm, phi), "  dLm/dphi' =", sp.diff(Lm, phip),
      " (both 0 => phi-blind confirmed)")

print("="*70)
print("Q5: can the rho-source cure the center obstruction? The obstruction lives in the")
print("phi-EOM: phi'' = 4e^{-2phi}rho'^2/(Z rho^2) - 2 phi' rho'/rho  -- matter-free.")
# For the r^-2 obstruction to cancel WITHOUT matter in the phi-eq, need the -2phi'rho'/rho
# term to cancel the source at O(1/r^2): 2 phi' rho'/rho = 4 e^{-2phi} rho'^2/(Z rho^2)
phi0 = sp.symbols('phi0')
phip_needed = sp.solve(sp.Eq(2*sp.Symbol("phip")*sp.Symbol("rhop")/sp.Symbol("rho"),
                             4*sp.exp(-2*phi0)*sp.Symbol("rhop")**2/(Z*sp.Symbol("rho")**2)),
                       sp.Symbol("phip"))[0]
print("  cancellation requires phi' =", phip_needed, "  -> with regular rho'=e^{phi0}, rho~e^{phi0}r:")
print("  phi' =", sp.simplify(phip_needed.subs({sp.Symbol('rhop'): sp.exp(phi0),
      sp.Symbol('rho'): sp.exp(phi0)*sp.Symbol('r_')})), " ~ (2/Z)/r  -> phi ~ (2/Z) ln r, NOT smooth.")
print("  => phi-blind matter CANNOT cure the center; only a phi-equation source could.")

print("="*70)
print("Q6: conserved H of the coupled system + two-seal condition")
# H density: h = phi' dLam/dphi' + rho' dLam/drho' + f_r dLam/df_r - Lam
h = phip*sp.diff(Lam, phip) + rhop*sp.diff(Lam, rhop) + fr*sp.diff(Lam, fr) - Lam
h = sp.expand(h)
# claim: H_m (theta-integrated) = -(xi/2)rho^2 I_r - (kap N^2/2) I_4r
#        + (xi/2)(I_th + N^2 I_s) + (kap N^2/2) I_4th/rho^2
# check the density-level version:
hm_claim = -(xi/2)*(rho**2*s*fr**2/2) - (kap*N**2/2)*(sp.sin(f)**2*fr**2/(2*s)) \
           + (xi/2)*(s*fth**2/2 + N**2*sp.sin(f)**2/(2*s)) \
           + (kap*N**2/2)*(sp.sin(f)**2*fth**2/(2*s*rho**2))
hg_claim = (s/2)*((Z/2)*rho**2*phip**2 - 2*sp.exp(-2*phi)*rhop**2 - 2)
print("  h - (hg_claim + hm_claim) =", sp.simplify(h - (hg_claim + hm_claim)))

# conservation: dh/dr = phi'*(ELphi-density) + rho'*(ELrho-density) + d/dth[f_r dLam/df_th] ... sign check
# standard identity: dh/dr + d/dth (f_r * dLam/df_th) = phi'*ELphi_d + rho'*ELrho_d + f_r*ELf
ELphi_d = sp.diff(sp.diff(Lam, phip), r) - sp.diff(Lam, phi)
ELrho_d = sp.diff(sp.diff(Lam, rhop), r) - sp.diff(Lam, rho)
ident = sp.diff(h, r) + sp.diff(fr*sp.diff(Lam, fth), th) \
        - (phip*ELphi_d + rhop*ELrho_d + fr*ELf)
print("  conservation identity residual (0 => dH/dr=0 on shell up to pole boundary term):",
      sp.simplify(ident))
print("  [pole term [f_r dLam/df_th]_0^pi = 0 since f(r,0)=0, f(r,pi)=pi pin f_r=0 at poles]")
print("  [phi,rho are 1-D: their ELs are the theta-INTEGRALS of ELphi_d, ELrho_d; since phi',rho'")
print("   are theta-independent they factor out of the integral -> the integrated terms vanish on shell]")

print("="*70)
print("Q6 final condition (with f-mirror f_r=0 at both seals, phi'=rho'=0):")
print("  H_geo(seal) = -2 (both seals, constant) -> drops out. Conservation =>")
print("  (xi/2)(I_th + N^2 I_s) + (kap N^2/2) I_4th/rho^2  EQUAL at r_in and r_out")
print("  (general seal, f_r free:  add  -(xi/2)rho^2 I_r - (kap N^2/2) I_4r  on each side)")
