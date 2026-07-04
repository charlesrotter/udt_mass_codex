"""microphysics_E1_composite_conditions.py -- E1 CAS derivations (sympy) for the composite
two-domain closure: particle cell (native S^2 L2+L4 carrier) EMBEDDED in the real N=0
fundamental universe cell. Pre-registration: microphysics_reentry_miniMAP.md (Stage E1).

SOURCES (cited per check):
  - L_bar cell (carrier):  f2d_virial_step0_results.md:34-38 (V2, blind-verified) ==
      cell_solver_f2d.py:14-44 docstring (EOMs, H, Derrick densities).
  - L_bar ambient (universe): cell_solver_universe_T3.py:18-20 (EOMs), :119 (H_amb) ==
      microphysics_E0_ambient_tables.md:5 (H_amb def).
  - Two-domain corner machinery (C1 momentum continuity + C2 H-continuity): BLIND-VERIFIED,
      embedded_cell_closure_H_amb_results.md:19-38 -- INHERITED for shared fields; the f-sector
      (field present on ONE side only) is NEW and derived here (K1).
  - Fold pins / transversality with essential phi(fold)=0: universe_cell_fold_jc_sigma_results.md:
      26-35 (odd fold), 37-39 (even fold), 54-57 (transversality/critical closure).
  - Center exclusions: universe_cell_vacuum_impossibility_results.md R2 (:75-82, blind-verified:
      no regular center even with phi-blind matter; carrier kappa-term diverges inward).

Both media are round-static Branch-P (W=1) reduced Lagrangians -- the seal at r_p is a P|P
interface (matter-content jump only); the G|P weight-jump machinery of
seal_matching_junction_results.md is NOT triggered at r_p (no branch change).

All checks print PASS/FAIL; exit nonzero on any FAIL. Symbolic only (fast, bounded).
"""
import sys
import sympy as sp

r, th = sp.symbols('r theta', real=True)
Z, xi, kap, N = sp.symbols('Z xi kappa N', positive=True)
FAILED = []


def check(name, cond):
    ok = bool(cond)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        FAILED.append(name)
    return ok


# ---------------------------------------------------------------------------------------------
# Field setup (density level; f = f(r,theta) generic)
# ---------------------------------------------------------------------------------------------
phi = sp.Function('phi')(r)
rho = sp.Function('rho')(r)
f = sp.Function('f')(r, th)
U = sp.Function('U')  # ambient potential-only matter (T3 slice family; CHOSE, per bracket)

phip, rhop = sp.diff(phi, r), sp.diff(rho, r)
fr, fth = sp.diff(f, r), sp.diff(f, th)

# Geometry part of BOTH reduced Lagrangians (identical skeleton; Branch P, per-4pi units)
# f2d_virial_step0_results.md:35  /  cell_solver_universe_T3.py (EOMs it generates)
G_geo = (Z / 2) * rho**2 * phip**2 + 2 - 2 * sp.exp(-2 * phi) * rhop**2

# Carrier matter theta-DENSITY m(theta):  L_bar_cell = G_geo + Int_0^pi m dtheta
# (I_r = 1/2 Int sin f_r^2; I_th = 1/2 Int sin f_th^2; I_s = 1/2 Int sin^2 f/sin;
#  I_4th = 1/2 Int (sin^2 f/sin) f_th^2; I_4r = 1/2 Int (sin^2 f/sin) f_r^2)
m_dens = (-(xi / 2) * (rho**2 * sp.sin(th) * fr**2 / 2 + sp.sin(th) * fth**2 / 2
                       + N**2 * sp.sin(f)**2 / sp.sin(th) / 2)
          - (kap * N**2 / 2) * (sp.sin(f)**2 / sp.sin(th) * fr**2 / 2
                                + sp.sin(f)**2 / sp.sin(th) * fth**2 / (2 * rho**2)))

# Ambient matter:  L_bar_amb = G_geo - U(rho)   (potential-only, phi-blind; T3 slice family)
L_amb = G_geo - U(rho)

# ---------------------------------------------------------------------------------------------
# K0a: the ambient EOMs from L_amb match the banked T3 solver EOMs (native re-derivation)
# ---------------------------------------------------------------------------------------------
EL_phi_amb = sp.diff(sp.diff(L_amb, phip), r) - sp.diff(L_amb, phi)
EL_rho_amb = sp.diff(sp.diff(L_amb, rhop), r) - sp.diff(L_amb, rho)
# T3 lines 19-20:
phipp_T3 = 4 * sp.exp(-2 * phi) * rhop**2 / (Z * rho**2) - 2 * phip * rhop / rho
rhopp_T3 = (2 * phip * rhop - (Z / 4) * rho * sp.exp(2 * phi) * phip**2
            + sp.exp(2 * phi) / 4 * sp.diff(U(rho), rho))
sol_pp = sp.solve([EL_phi_amb, EL_rho_amb], [sp.diff(phi, r, 2), sp.diff(rho, r, 2)], dict=True)[0]
check("K0a ambient EOMs == banked T3 EOMs (phi'', rho'')",
      sp.simplify(sol_pp[sp.diff(phi, r, 2)] - phipp_T3) == 0
      and sp.simplify(sol_pp[sp.diff(rho, r, 2)] - rhopp_T3) == 0)

# ---------------------------------------------------------------------------------------------
# K0b: the carrier f-EL density reproduces the banked f-PDE (cell_solver_f2d.py:25-26), and the
#      cell (phi,rho)-EOMs reproduce f2d docstring lines 18-19 (with theta-moments abstracted).
# ---------------------------------------------------------------------------------------------
ELf = (sp.diff(m_dens, f) - sp.diff(sp.diff(m_dens, fr), r) - sp.diff(sp.diff(m_dens, fth), th))
A_coef = xi * rho**2 * sp.sin(th) + kap * N**2 * sp.sin(f)**2 / sp.sin(th)
B_coef = xi * sp.sin(th) + kap * N**2 * sp.sin(f)**2 / (rho**2 * sp.sin(th))
fPDE = (sp.diff(A_coef * fr, r) + sp.diff(B_coef * fth, th)
        - (N**2 * sp.sin(f) * sp.cos(f) / sp.sin(th)) * (xi + kap * fr**2 + kap * fth**2 / rho**2))
check("K0b f-EL density == +(1/2) * banked f-PDE", sp.simplify(ELf - fPDE / 2) == 0)

# rigid residual (V1 re-check): f = theta
check("K0b' rigid f=theta residual == xi(1-N^2)cos(theta) * sin-weight/... (V1)",
      sp.simplify(fPDE.subs(f, th).doit() - xi * (1 - N**2) * sp.cos(th)) == 0)

# ---------------------------------------------------------------------------------------------
# K1: the seal variation, f-sector piece (NEW vs the banked two-domain derivation).
#     For a field present on ONE side only, the moving-endpoint term at r_p is
#     pi_f * Delta_f  - (f-part of H_cell) * dr_p, with Delta_f FREE  =>  pi_f(r_p,theta)=0.
#     We verify the pointwise IBP identity behind the endpoint formula at density level:
#        d/dr [ (dm/df_r) eta ] = eta*ELf_r-part + (dm/df eta + dm/df_r eta_r + dm/df_th eta_th)
#                                  - d/dth[(dm/df_th) eta]
#     which is exactly what reduces delta S to  Int ELf*eta + endpoint pi_f*eta + pole flux.
# ---------------------------------------------------------------------------------------------
eta = sp.Function('eta')(r, th)
lhs = sp.diff(sp.diff(m_dens, fr) * eta, r)
rhs = (eta * (sp.diff(m_dens, f) - sp.diff(sp.diff(m_dens, fr), r) - sp.diff(sp.diff(m_dens, fth), th))
       - (sp.diff(m_dens, f) * eta + sp.diff(m_dens, fr) * sp.diff(eta, r)
          + sp.diff(m_dens, fth) * sp.diff(eta, th)) * (-1)
       - sp.diff(sp.diff(m_dens, fth) * eta, th) - eta * 0)
# rearranged: d/dr(pi_f eta) + d/dth(pi_fth eta) = eta*ELf + full first variation of m
first_var = (sp.diff(m_dens, f) * eta + sp.diff(m_dens, fr) * sp.diff(eta, r)
             + sp.diff(m_dens, fth) * sp.diff(eta, th))
identity = sp.simplify(sp.diff(sp.diff(m_dens, fr) * eta, r)
                       + sp.diff(sp.diff(m_dens, fth) * eta, th)
                       + eta * ELf - first_var)
check("K1 IBP identity (f-sector endpoint term = pi_f * eta, pole-flux term explicit)",
      identity == 0)

# pi_f density and its sign/positivity structure:
pi_f = sp.diff(m_dens, fr)
check("K1' pi_f = -(1/2) A(r,theta) f_r  (A>0 on theta in (0,pi) for xi,rho>0)",
      sp.simplify(pi_f + A_coef * fr / 2) == 0)
# => natural BC pi_f = 0 <=> f_r = 0 pointwise in theta (A>0 interior). DERIVED, not chosen.

# ---------------------------------------------------------------------------------------------
# K2: H densities.  H = q' dL/dq' - L (theta-integrated).  Verify:
#     (a) H_amb form == cell_solver_universe_T3.py:119
#     (b) H_cell density == f2d docstring lines 38-39 (moment level)
# ---------------------------------------------------------------------------------------------
H_amb = phip * sp.diff(L_amb, phip) + rhop * sp.diff(L_amb, rhop) - L_amb
H_amb_T3 = (Z / 2) * rho**2 * phip**2 - 2 * sp.exp(-2 * phi) * rhop**2 - 2 + U(rho)
check("K2a H_amb == (Z/2)rho^2 phi'^2 - 2e^{-2phi}rho'^2 - 2 + U  (T3:119)",
      sp.simplify(H_amb - H_amb_T3) == 0)

# cell: theta-density of H's matter part = f_r * dm/df_r - m ; geometry part as ambient minus U
h_m_dens = fr * sp.diff(m_dens, fr) - m_dens
# docstring moment form: -(xi/2)rho^2 I_r + (xi/2)(I_th + N^2 I_s) - (kap N^2/2) I_4r
#                        + (kap N^2/2) I_4th / rho^2   -- as a theta-density:
h_m_doc = (-(xi / 2) * rho**2 * sp.sin(th) * fr**2 / 2
           + (xi / 2) * (sp.sin(th) * fth**2 / 2 + N**2 * sp.sin(f)**2 / sp.sin(th) / 2)
           - (kap * N**2 / 2) * sp.sin(f)**2 / sp.sin(th) * fr**2 / 2
           + (kap * N**2 / 2) * sp.sin(f)**2 / sp.sin(th) * fth**2 / (2 * rho**2))
check("K2b H_cell matter density == f2d docstring lines 38-39 moment form",
      sp.simplify(h_m_dens - h_m_doc) == 0)

# ---------------------------------------------------------------------------------------------
# K3: conservation of H_cell at density level (Step-0 V4, independent re-check):
#     d/dr[H_geo + Int h_m] = -EL_phi*phi' - EL_rho*rho' - Int ELf*f_r + [pole flux]
# ---------------------------------------------------------------------------------------------
L_cell_geo = G_geo   # theta-independent part
H_geo = phip * sp.diff(L_cell_geo, phip) + rhop * sp.diff(L_cell_geo, rhop) - L_cell_geo
# EL for phi/rho from the FULL cell Lagrangian: geometry + theta-integral of m.
# At density level the rho-EOM gets Int dm/drho dtheta; carry it symbolically:
ELphi_geo = sp.diff(sp.diff(L_cell_geo, phip), r) - sp.diff(L_cell_geo, phi)
ELrho_geo = sp.diff(sp.diff(L_cell_geo, rhop), r) - sp.diff(L_cell_geo, rho)
# d/dr h_m_dens + f_r*ELf must equal a theta-divergence + dm/drho * rho' (the rho-coupling flux)
resid_cons = sp.simplify(
    sp.diff(h_m_dens, r) + fr * ELf
    + sp.diff(fr * sp.diff(m_dens, fth), th)
    + sp.diff(m_dens, rho) * rhop)
check("K3a matter-density conservation identity (theta-flux + rho-coupling explicit)",
      resid_cons == 0)
resid_geo = sp.simplify(sp.diff(H_geo, r) - phip * ELphi_geo - rhop * ELrho_geo)
check("K3b geometry H conservation identity", resid_geo == 0)
# Sum: dH/dr = -phi' ELphi_tot - rho' ELrho_tot - Int f_r ELf + pole flux, since the
# rho-coupling terms  Int dm/drho * rho'  pair with ELrho_tot = ELrho_geo - Int dm/drho.
# Pole flux f_r * dm/df_th -> 0 at theta=0,pi under the pole BCs f(r,0)=0, f(r,pi)=pi
# (f_r=0 at poles; banked V4). => dH_cell/dr = 0 on-shell.  Same for H_amb (autonomous, 1-D).

# ---------------------------------------------------------------------------------------------
# K4: the seal collapse.  With continuity of (phi, rho, phi', rho')  [C1a,b <=> momentum
#     continuity since pi_phi = Z rho^2 phi', pi_rho = -4 e^{-2phi} rho' share Z, rho, phi]
#     and the derived f_r(r_p,theta)=0 (K1'):
#        C2:  H_cell(r_p) - H_amb(r_p)  ==  E_ang(r_p) - U(rho_p)
#     where E_ang := (xi/2)(I_th + N^2 I_s) + (kap N^2/2) I_4th/rho^2  (transverse angular energy)
# ---------------------------------------------------------------------------------------------
h_m_at_seal = h_m_dens.subs(fr, 0)
E_ang_dens = ((xi / 2) * (sp.sin(th) * fth**2 / 2 + N**2 * sp.sin(f)**2 / sp.sin(th) / 2)
              + (kap * N**2 / 2) * sp.sin(f)**2 / sp.sin(th) * fth**2 / (2 * rho**2))
check("K4 C2 collapse: (H_cell - H_amb)|seal density == E_ang_dens - U-part  (f_r=0)",
      sp.simplify((h_m_at_seal - E_ang_dens)) == 0)
# geometry parts cancel identically (same G_geo both sides, continuous data), so
#   C2  <=>  Int E_ang_dens dtheta = U(rho_p).     [E_ang == E_m^ang,perp in the results doc]

# ---------------------------------------------------------------------------------------------
# K5: core evaluation.  At an even mirror core (phi'=rho'=f_r=0, natural BCs from K1'-type
#     momenta: pi_phi = Z rho^2 phi', pi_rho = -4e^{-2phi} rho', pi_f = -(1/2)A f_r):
#        H_cell(0) = E_ang(0) - 2
# ---------------------------------------------------------------------------------------------
H_cell_full_geo = H_geo  # = (Z/2)rho^2 phi'^2 - 2e^{-2phi}rho'^2 - 2
H_core_geo = sp.simplify(H_cell_full_geo.subs([(phip, 0), (rhop, 0)]))
check("K5 H_cell(core) = -2 + E_ang(core)  (geometry part -> -2; matter part -> E_ang, f_r=0)",
      H_core_geo == -2 and sp.simplify(h_m_dens.subs(fr, 0) - E_ang_dens) == 0)
# => chain (algebra):  H_amb(fold)=0 [outer transversality] + dH_amb/dr=0  => H_amb(r_p)=0
#    C2 => H_cell(r_p)=0 ; dH_cell/dr=0 => H_cell(0)=0  =>  E_ang(core) = 2.
# The critical-closure condition MIGRATES from the ambient core (U(rho_c)=2, now cut out)
# to the particle core (E_ang(core)=2): criticality is a property of whatever closes the center.

# ---------------------------------------------------------------------------------------------
# K6: outer odd fold, transversality with the essential constraint Delta phi(fold)=0
#     (fold pins DERIVED in universe_cell_fold_jc_sigma_results.md:26-35; re-check the
#     endpoint algebra):  endpoint term = pi_rho*Delta_rho + pi_phi*Delta_phi - H*ds
#     with Delta_phi = 0 (odd identification), Delta_rho free, ds free
#     =>  rho'(fold) = 0  and  H_amb(fold) = 0.   phi'(fold) stays FREE (q output).
# ---------------------------------------------------------------------------------------------
pi_phi = sp.diff(L_amb, phip)
pi_rho = sp.diff(L_amb, rhop)
# endpoint term with Delta_phi=0: pi_rho*Dr + (L - phi' pi_phi - rho' pi_rho)*ds = pi_rho*Dr - H*ds
endpoint = sp.simplify(L_amb - phip * pi_phi - rhop * pi_rho + H_amb)
check("K6 (L - Sum q' pi) == -H  (transversality coefficient of ds is -H_amb)", endpoint == 0)
check("K6' pi_rho = -4 e^{-2phi} rho'  (rho'(fold)=0 from free Delta_rho)",
      sp.simplify(pi_rho + 4 * sp.exp(-2 * phi) * rhop) == 0)
check("K6'' pi_phi = Z rho^2 phi'  (phi' free at fold: [pi_phi]==0 identically under odd map)",
      sp.simplify(pi_phi - Z * rho**2 * phip) == 0)

# ---------------------------------------------------------------------------------------------
# K7: flux law + phi -> -infinity core exclusion (power-law class).
#     phi-EOM (phi-blind matter, BOTH Lagrangians):  (rho^2 phi')' = (4/Z) e^{-2phi} rho'^2 >= 0.
# ---------------------------------------------------------------------------------------------
flux_lhs = sp.diff(rho**2 * phip, r)
flux_rhs = (4 / Z) * sp.exp(-2 * phi) * rhop**2
# substitute the phi'' EOM:
flux_check = sp.simplify(flux_lhs.subs(sp.diff(phi, r, 2), phipp_T3) - flux_rhs)
check("K7 flux law (rho^2 phi')' = (4/Z) e^{-2phi} rho'^2  (monotone Phi; matter-independent)",
      flux_check == 0)

# Power-law core probe: rho = a s^alpha, phi = beta ln s + phi0  (phi -> -inf needs beta > 0)
s_ = sp.symbols('s', positive=True)  # radial coordinate near the would-be core, s -> 0+
a_, al, be, p0 = sp.symbols('a alpha beta phi0', positive=True)
rho_p = a_ * s_**al
phi_p = be * sp.log(s_) + p0
lhs_p = sp.diff(rho_p**2 * sp.diff(phi_p, s_), s_)                   # ~ s^{2 alpha - 2}
rhs_p = (4 / Z) * sp.exp(-2 * phi_p) * sp.diff(rho_p, s_)**2         # ~ s^{2 alpha - 2 - 2 beta}
rat_l = sp.powsimp(sp.simplify(lhs_p / (a_**2 * be * (2 * al - 1) * s_**(2 * al - 2))), force=True)
rat_r = sp.powsimp(sp.simplify(
    rhs_p / ((4 / Z) * sp.exp(-2 * p0) * a_**2 * al**2 * s_**(2 * al - 2 - 2 * be))), force=True)
check("K7' power-law clash: LHS ~ r^{2a-2}, RHS ~ r^{2a-2-2b}; equality forces beta = 0",
      rat_l == 1 and rat_r == 1)
# beta > 0 => RHS/LHS ~ r^{-2 beta} -> infinity as r -> 0: the EOM cannot hold at leading order
# unless 2a-1 = 0 (alpha = 1/2, LHS leading term vanishes) -- but then RHS ~ r^{-1-2b} still
# diverges with NO LHS term to match (any correction to Phi = const enters at HIGHER order).
# => no power-law (rho -> 0, phi -> -infinity) core.  rho bounded below: Phi monotone and
# finite at the seal => phi' <= Phi(r_p)/rho_min^2 bounded => phi bounded below. (prose, exact)

# ---------------------------------------------------------------------------------------------
# K8: rigid-N reduction.  f = theta: I_th = I_s = I_4th = 1, I_r = I_4r = 0 (exact integrals);
#     the cell Lagrangian becomes the T3 form with U_eff(rho) = (xi/2)(1+N^2) + kap N^2/(2 rho^2).
#     Exact carrier configuration ONLY at N=1 (V1/K0b').
# ---------------------------------------------------------------------------------------------
I_th_r = sp.integrate((sp.sin(th) * 1) / 2, (th, 0, sp.pi))
I_s_r = sp.integrate(sp.sin(th)**2 / sp.sin(th) / 2, (th, 0, sp.pi))
I_4th_r = sp.integrate(sp.sin(th)**2 / sp.sin(th) * 1 / 2, (th, 0, sp.pi))
check("K8 rigid moments I_th = I_s = I_4th = 1", (I_th_r, I_s_r, I_4th_r) == (1, 1, 1))
m_rigid = sp.integrate(m_dens.subs(f, th).doit(), (th, 0, sp.pi))
U_eff = (xi / 2) * (1 + N**2) + kap * N**2 / (2 * rho**2)
check("K8' L_cell(rigid) == G_geo - U_eff(rho)   [U_eff = (xi/2)(1+N^2) + kap N^2/(2 rho^2)]",
      sp.simplify(m_rigid.subs(fr, 0) + U_eff) == 0)

# ---------------------------------------------------------------------------------------------
# K9: embedded Derrick / Pohozaev identity.
#     Scaling variation delta_phi = -r phi', delta_rho = rho - r rho', delta_f = -r f_r.
#     Pointwise (off-shell, density level):
#       dens_a - dens_b = d/dr[ -r*H + rho*pi_rho ] + EL_phi*(-r phi') + EL_rho*(rho - r rho')
#                         + Int ELf*(-r f_r)  + d/dth[theta-flux]
#     On-shell with H == 0:  S_a - S_b = [rho pi_rho]_{r_p} - [rho pi_rho]_0 = -4 e^{-2phi_p} rho'_p rho_p
# ---------------------------------------------------------------------------------------------
dens_a_geo = G_geo  # geometry+2 part of dens_a
dens_a_m = (-(xi / 2) * (rho**2 * sp.sin(th) * fr**2 / 2 + sp.sin(th) * fth**2 / 2
                         + N**2 * sp.sin(f)**2 / sp.sin(th) / 2))          # xi-sector density
dens_b_m = (-(kap * N**2 / 2) * (sp.sin(f)**2 / sp.sin(th) * fr**2 / 2
                                 + sp.sin(f)**2 / sp.sin(th) * fth**2 / (2 * rho**2)))  # kappa
# full L density = dens_a_geo + dens_a_m + dens_b_m ; dens_a = geo + xi part; dens_b = kappa part
Ldens = dens_a_geo + dens_a_m + dens_b_m
H_dens = (phip * sp.diff(Ldens, phip) + rhop * sp.diff(Ldens, rhop)
          + fr * sp.diff(Ldens, fr) - Ldens)
pi_rho_c = sp.diff(Ldens, rhop)
ELphi_d = sp.diff(sp.diff(Ldens, phip), r) - sp.diff(Ldens, phi)
ELrho_d = sp.diff(sp.diff(Ldens, rhop), r) - sp.diff(Ldens, rho)
ELf_d = (sp.diff(sp.diff(Ldens, fr), r) + sp.diff(sp.diff(Ldens, fth), th)
         - sp.diff(Ldens, f))
dphi_v, drho_v, df_v = -r * phip, rho - r * rhop, -r * fr
poho = sp.simplify(
    (dens_a_geo + dens_a_m) - dens_b_m
    - sp.diff(-r * H_dens + rho * pi_rho_c, r)
    + ELphi_d * dphi_v + ELrho_d * drho_v + ELf_d * df_v          # sign: EL as d/dr(dL/dq')-dL/dq
    - sp.diff(sp.diff(Ldens, fth) * df_v, th))
check("K9 Pohozaev density identity: dens_a - dens_b = d/dr[-rH + rho pi_rho] "
      "- Sum EL*delta_scaling + theta-flux", poho == 0)
# theta-flux = d/dth[ dL/df_th * (-r f_r) ] -> 0 at poles (f_r(r,0)=f_r(r,pi)=0, banked V4).
# core boundary: r=0 kills -rH; pi_rho(0)=0 at even fold kills rho pi_rho.
# => on-shell, H==0:   S_a - S_b = rho_p * pi_rho(r_p) = -4 e^{-2 phi_p} rho'_p rho_p   ("tax" B)

# ---------------------------------------------------------------------------------------------
# K10: the bulge identity.  Substitute pointwise H_dens = 0 into dens_a - dens_b:
#      dens_a - dens_b == 4 + kappa-radial-part - xi*(I_th + N^2 I_s)-part (theta-density form).
#      Integrated:  xi Int (I_th + N^2 I_s) dr = 4 r_p + kap N^2 Int I_4r dr - B .
# ---------------------------------------------------------------------------------------------
# theta-density bookkeeping: write dens_a - dens_b with the geometry eliminated via H_dens = 0.
K_geo = (Z / 2) * rho**2 * phip**2 - 2 * sp.exp(-2 * phi) * rhop**2
E_dens = h_m_dens  # matter Legendre density (theta level)
# H = K_geo - 2 + Int E_dens  => at theta-integrated level: K_geo = 2 - Int E_dens
# dens_a - dens_b (integrated over theta):
da_minus_db_int = sp.Symbol('da_db')  # do the algebra with integrated symbols instead:
Ith, Is, I4th, Ir, I4r = sp.symbols('I_th I_s I_4th I_r I_4r', nonnegative=True)
E_int = -(xi / 2) * rho**2 * Ir - (kap * N**2 / 2) * I4r + (xi / 2) * (Ith + N**2 * Is) \
        + (kap * N**2 / 2) * I4th / rho**2
Kgeo_sym = 2 - E_int                      # from H = 0
densa_int = Kgeo_sym + 4 - 2 - (xi / 2) * rho**2 * Ir - (xi / 2) * (Ith + N**2 * Is)
# careful: dens_a = K_geo + 2 - (xi/2)(rho^2 I_r + I_th + N^2 I_s)  (f2d docstring line 43)
densa_int = Kgeo_sym + 2 - (xi / 2) * (rho**2 * Ir + Ith + N**2 * Is)
densb_int = -(kap * N**2 / 2) * (I4r + I4th / rho**2)
bulge = sp.simplify(densa_int - densb_int - (4 + kap * N**2 * I4r - xi * (Ith + N**2 * Is)))
check("K10 bulge identity: (dens_a - dens_b)|_{H=0} == 4 + kap N^2 I_4r - xi (I_th + N^2 I_s)",
      bulge == 0)

# ---------------------------------------------------------------------------------------------
# K11: rigid-N=1 Derrick contradiction.
#      rigid: I_th + I_s = 2, I_4r = 0  =>  dens_a - dens_b = 4 - 2 xi  =>  B = (4 - 2 xi) r_p.
#      B = -4 e^{-2phi_p} rho'_p rho_p <= 0 for rho'_p >= 0 (every E0 station)  =>  xi >= 2.
#      Core closure (K5 + K8): U_eff(rho_c) = xi + kap/(2 rho_c^2) = 2  =>  xi < 2 (kap > 0).
#      CONTRADICTION: rigid-N=1 closes NOWHERE (any bracket, any position, any kap > 0).
# ---------------------------------------------------------------------------------------------
lhs_r = (4 + kap * N**2 * I4r - xi * (Ith + N**2 * Is)).subs(
    [(Ith, 1), (Is, 1), (I4r, 0), (N, 1)])
check("K11 rigid-N=1: dens_a - dens_b == 4 - 2 xi  (so B <= 0 forces xi >= 2; core forces xi < 2)",
      sp.simplify(lhs_r - (4 - 2 * xi)) == 0)

# ---------------------------------------------------------------------------------------------
# K12: moment bounds (Cauchy-Schwarz machinery).
#      (a) Int_0^pi sin(f) f_th dtheta = cos f(0) - cos f(pi) = 2 for any profile with
#          f(r,0)=0, f(r,pi)=pi (exact differential; NO monotonicity needed).
#      (b) equality/rigid saturation: I_th*I_s = 1 and I_4th = 1 at f = theta (K8).
#      (c) numeric C-S check on random admissible profiles (bounds hold, rigid saturates).
# ---------------------------------------------------------------------------------------------
g_ = sp.Function('g')(th)
exact_diff = sp.simplify(sp.integrate(sp.diff(-sp.cos(g_), th), (th, 0, sp.pi))
                         - (-sp.cos(g_.subs(th, sp.pi)) + sp.cos(g_.subs(th, 0))))
check("K12a Int sin(f) f_th dth = [-cos f] = 2 under pole BCs (exact differential)",
      exact_diff == 0)

import numpy as np
rng = np.random.default_rng(7)
tt = np.linspace(1e-6, np.pi - 1e-6, 4001)
ok_bounds, saturate = True, None
for trial in range(200):
    amps = rng.normal(0, 0.4, 5) / np.arange(1, 6)
    fprof = tt + sum(a * np.sin(k * tt) for k, a in enumerate(amps, start=1))
    fth_n = 1 + sum(a * k * np.cos(k * tt) for k, a in enumerate(amps, start=1))
    Ith_n = 0.5 * np.trapezoid(np.sin(tt) * fth_n**2, tt)
    Is_n = 0.5 * np.trapezoid(np.sin(fprof)**2 / np.sin(tt), tt)
    I4th_n = 0.5 * np.trapezoid(np.sin(fprof)**2 / np.sin(tt) * fth_n**2, tt)
    if Ith_n * Is_n < 1 - 1e-9 or I4th_n < 1 - 1e-9:
        ok_bounds = False
        break
# rigid saturation
Ith_0 = 0.5 * np.trapezoid(np.sin(tt), tt)
Is_0 = 0.5 * np.trapezoid(np.sin(tt), tt)
I4_0 = 0.5 * np.trapezoid(np.sin(tt), tt)
check("K12b C-S bounds I_th*I_s >= 1, I_4th >= 1 on 200 random admissible profiles; "
      "rigid saturates (numeric)",
      ok_bounds and abs(Ith_0 * Is_0 - 1) < 1e-6 and abs(I4_0 - 1) < 1e-6)

# ---------------------------------------------------------------------------------------------
# K13: plateau identity. H_amb = 0  =>  U - 2 = 2 e^{-2phi} rho'^2 - (Z/2) rho^2 phi'^2:
#      the ambient's deviation of U from criticality IS its gradient content, exactly.
# ---------------------------------------------------------------------------------------------
K13res = sp.simplify((U(rho) - 2) - (2 * sp.exp(-2 * phi) * rhop**2
                                     - (Z / 2) * rho**2 * phip**2) - H_amb_T3)
check("K13 (U-2) - gradient-content == H_amb identically (so H_amb=0 => U-2 = gradient content)",
      K13res == 0)

print()
if FAILED:
    print("FAILED checks:", FAILED)
    sys.exit(1)
print("ALL CHECKS PASS")
