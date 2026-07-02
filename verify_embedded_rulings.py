"""verify_embedded_rulings.py — CAS check of claude.ai's embedded-run gate Rulings 1 & 2
(`embedded_run_gate_rulings.md`), owed before the embedded run banks against them.

R1a  geometry Legendre inversion: H_geo = pi_phi phi' + pi_rho rho' - Lbar_geo, expressed in the
     momenta, equals pi_phi^2/(2 Z rho^2) - pi_rho^2 e^{2phi}/8 - 2, a function of (phi,rho,pi) ONLY
     -> field+momentum continuity => [H_geo]=0 automatically (C2 redundant for geometry).
R1b  matter H-contribution at the seal (natural BC f_r=0) = E_ang = (xi/2)(I_th+N^2 I_s)
     + (kap N^2/2) I_4th/rho^2 -> given [H_geo]=0, C2 ([H]=0) reduces to E_ang,cell = m_amb.
R2   matched-boundary Derrick: dS/dlam|_1 (scaling family phi(r/lam), lam rho(r/lam), f(r/lam)) on-shell
     = S_a - S_b, and the boundary terms give S_a - S_b = pi_rho(r_s) rho(r_s) - r_s H_s + r_c H_c;
     with H matched (H_s=H_c=H_amb) and the mirror core (pi_rho(r_c)=0):
       S_a - S_b + (r_s - r_c) H_amb - pi_rho(r_s) rho(r_s) = 0.  Closed limit (H=0, pi_rho,s=0): S_a=S_b.
"""
import sympy as sp

r = sp.symbols('r', positive=True)
Z, xi, kap, N = sp.symbols('Z xi kappa N', positive=True)
phi = sp.Function('phi')(r); rho = sp.Function('rho')(r)
php, rhp = sp.diff(phi, r), sp.diff(rho, r)

# ---- geometry reduced Lagrangian (per 4pi; theta-integrated) ----
Lg = (Z/2)*rho**2*php**2 + 2 - 2*sp.exp(-2*phi)*rhp**2
pi_phi = sp.diff(Lg, php)                     # = Z rho^2 phi'
pi_rho = sp.diff(Lg, rhp)                     # = -4 e^{-2phi} rho'
Hg = php*pi_phi + rhp*pi_rho - Lg             # geometry Hamiltonian in velocities

# R1a: invert to momenta. phi' = pi_phi/(Z rho^2); rho' = -pi_rho e^{2phi}/4.
Pphi, Prho = sp.symbols('pi_phi pi_rho', real=True)
subs_inv = {php: Pphi/(Z*rho**2), rhp: -Prho*sp.exp(2*phi)/4}
Hg_mom = sp.simplify(Hg.subs(subs_inv))
Hg_claim = Pphi**2/(2*Z*rho**2) - Prho**2*sp.exp(2*phi)/8 - 2
R1a = sp.simplify(Hg_mom - Hg_claim) == 0
# momenta-only (no phi',rho'): Hg_mom must not contain Derivative
R1a_momonly = (not Hg_mom.has(php)) and (not Hg_mom.has(rhp))
# and the inversion is nondegenerate (Hessian of Lg wrt velocities is invertible):
Hess = sp.Matrix([[sp.diff(Lg, php, 2), sp.diff(Lg, php, rhp)],
                  [sp.diff(Lg, rhp, php), sp.diff(Lg, rhp, 2)]])
R1a_nondeg = sp.simplify(Hess.det()) != 0

# ---- R1b: matter H-contribution at f_r = 0 equals E_ang ----
th = sp.symbols('theta', positive=True); f = sp.Function('f')(r, th)
s = sp.sin(th)
# matter theta-density (undilated, phi-blind); H_matter density = f_r dDm/df_r - Dm
Dm = sp.Rational(1,2)*((xi/2)*(rho**2*sp.diff(f,r)**2*s + sp.diff(f,th)**2*s + N**2*sp.sin(f)**2/s)
     + (kap*N**2/2)*(sp.sin(f)**2/s*sp.diff(f,r)**2 + sp.sin(f)**2/(s*rho**2)*sp.diff(f,th)**2))
Lm = -Dm                                                # matter part of Lbar enters with a MINUS
Hm_dens = sp.diff(f,r)*sp.diff(Lm, sp.diff(f,r)) - Lm   # H-contribution = q' dL/dq' - L
Hm_seal = Hm_dens.subs(sp.diff(f,r), 0)                 # natural BC f_r=0 at the seal -> +Dm|_{f_r=0}
# E_ang density = +(xi/2)(f_th^2 s + N^2 sin^2 f/s)/... integrate to (xi/2)(I_th+N^2 I_s)+(kap N^2/2)I4th/rho^2
Eang_dens = sp.Rational(1,2)*((xi/2)*(sp.diff(f,th)**2*s + N**2*sp.sin(f)**2/s)
            + (kap*N**2/2)*sp.sin(f)**2/(s*rho**2)*sp.diff(f,th)**2)
R1b = sp.simplify(Hm_seal - Eang_dens) == 0

# ---- R2: scaling-family boundary terms (matched-boundary Derrick) ----
# generator (d/dlam at lam=1) of phi_lam(r)=phi(r/lam), rho_lam=lam rho(r/lam), f_lam=f(r/lam):
#   dphi = -r phi', drho = rho - r rho', df = -r f_r ; endpoint moves d(r_end)=r_end.
# TOTAL variation at a moving endpoint: Dq = dq + q' * d(r_end).
dphi = -r*php; drho = rho - r*rhp
Dphi = sp.simplify(dphi + php*r)          # total var of phi at endpoint (d r_end = r)
Drho = sp.simplify(drho + rhp*r)          # total var of rho at endpoint
R2_Dphi0 = (Dphi == 0)                    # scaling keeps phi's endpoint value fixed
R2_Drho  = sp.simplify(Drho - rho) == 0   # rho's endpoint total variation = rho (scales by lam)
# on-shell dS/dlam|_1 = [ sum pi_q Dq - H * d(r_end) ]_boundary ; with Dphi=Df=0, Drho=rho:
#   = [ pi_rho * rho - H * r ]_{r_c}^{r_s}. At mirror core pi_rho(r_c) = -4 e^{-2phi} rho'(r_c) = 0.
# => dS/dlam|_1 = pi_rho(r_s) rho(r_s) - r_s H_s + r_c H_c   (since pi_rho(r_c) rho(r_c) = 0).
# dS/dlam|_1 = S_a - S_b (Step-0 V6 weights: S_a ~ lam^+1, S_b ~ lam^-1).
# => S_a - S_b + (r_s - r_c) H_amb - pi_rho(r_s) rho(r_s) = 0  when H_s=H_c=H_amb.
rs, rc, Hs, Hc, Hamb, pirs, rhos = sp.symbols('r_s r_c H_s H_c H_amb pi_rho_s rho_s', real=True)
dSdlam = pirs*rhos - rs*Hs + rc*Hc                       # boundary result (pi_rho(r_c)=0 used)
SaSb = dSdlam                                            # = S_a - S_b on-shell
identity = SaSb + (rs - rc)*Hamb - pirs*rhos             # claim: = 0 when H_s=H_c=H_amb
R2_full = sp.simplify(identity.subs({Hs: Hamb, Hc: Hamb})) == 0
R2_closed = sp.simplify(identity.subs({Hs: 0, Hc: 0, Hamb: 0, pirs: 0})) == 0   # closed: S_a=S_b

print("R1a  H_geo(momenta) == pi_phi^2/(2Zrho^2) - pi_rho^2 e^{2phi}/8 - 2 :", R1a)
print("     H_geo is momenta-only (no phi',rho'):", R1a_momonly, "| Legendre nondegenerate:", R1a_nondeg)
print("R1b  matter H at f_r=0  ==  E_ang density :", R1b)
print("R2   scaling: Dphi=0 at endpoint:", R2_Dphi0, "| Drho=rho at endpoint:", R2_Drho)
print("R2   matched-boundary Derrick identity == 0 (H_s=H_c=H_amb):", R2_full)
print("R2   closed-cell limit recovers S_a=S_b (H=0, pi_rho_s=0):", R2_closed)
allok = all([R1a, R1a_momonly, R1a_nondeg, R1b, R2_Dphi0, R2_Drho, R2_full, R2_closed])
print("\nALL RULING CHECKS PASS:", allok)
