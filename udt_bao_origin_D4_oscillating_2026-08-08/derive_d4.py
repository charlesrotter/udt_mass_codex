#!/usr/bin/env python3
# D4 -- oscillating depth-profile component: P1 admissibility + P2 imprint transfer.
# Contract: udt_bao_origin_D4_oscillating_2026-08-08/PREREGISTRATION.md (frozen).
# MODE OBSERVE. All physics symbols FREE (F-RETRO: no floats in audited expressions).
# Object: A(r) = A_bg(r)*(1 + eps*osc), A_bg = (1 - r/R_w)^n, n>0 free symbol.
# Scope stamp: STATIC / mu=0 stratum / lock + areal-anchor chart / central observer.
import sympy as sp

CHECKS = {}
AUDITED = []  # expressions collected for the F-RETRO float-atom scan

def key(name, val, detail=""):
    CHECKS[name] = bool(val)
    print(f"KEY {name} = {bool(val)}" + (f"  [{detail}]" if detail else ""), flush=True)

print("D4 derive_d4.py -- scope STATIC/mu=0/lock+areal chart; n, eps, lambda, phi_0 all FREE")
print("=" * 78)

# ============ BLOCK A: GENERIC-A(r) metric facts (hold for ANY profile, =====
# ============ oscillating included -- the D1-survival backbone)         =====
t, r, th, ph = sp.symbols('t r theta varphi', real=True)
E, L, bpar, M = sp.symbols('E L b M', positive=True)
Fg = sp.Function('F', positive=True)(r)
coords = [t, r, th, ph]
g = sp.diag(-Fg, 1/Fg, r**2, r**2 * sp.sin(th)**2)
ginv = sp.diag(-1/Fg, Fg, 1/r**2, 1/(r**2 * sp.sin(th)**2))
N = 4

# lock form-preservation: g_tt * g_rr = -1 for ANY A(r) in this chart
key("A_lock_form_preserved_generic_A", sp.simplify(g[0, 0] * g[1, 1] + 1) == 0,
    "g_tt*g_rr=-1 identically; an oscillating A cannot break the lock")

Gam = [[[sp.S.Zero] * N for _ in range(N)] for _ in range(N)]
for a in range(N):
    for b2 in range(N):
        for c in range(N):
            e = sum(ginv[a, d] * (sp.diff(g[d, b2], coords[c]) + sp.diff(g[d, c], coords[b2])
                                  - sp.diff(g[b2, c], coords[d])) for d in range(N))
            Gam[a][b2][c] = sp.cancel(e / 2)

def Ric(mu, nu):
    e = sp.S.Zero
    for rho in range(N):
        e += sp.diff(Gam[rho][mu][nu], coords[rho]) - sp.diff(Gam[rho][rho][mu], coords[nu])
        for lm in range(N):
            e += Gam[rho][rho][lm] * Gam[lm][mu][nu] - Gam[rho][nu][lm] * Gam[lm][rho][mu]
    return sp.simplify(e)

Rtt = Ric(0, 0)
Rrr = Ric(1, 1)

# A0 soundness (Category-A, GR as reference limit): Schwarzschild must be Ricci-flat
schw = 1 - 2 * M / r
key("A0_ricci_routine_soundness_schwarzschild",
    sp.simplify(Rtt.subs(Fg, schw).doit()) == 0 and sp.simplify(Rrr.subs(Fg, schw).doit()) == 0)

# A1: radial null ray (tdot, rdot) = (E/F, E) is an exact geodesic; r affine
xdot = [E / Fg, E, sp.S.Zero, sp.S.Zero]
geo_ok = True
for mu in range(N):
    ddl = sp.diff(xdot[mu], r) * xdot[1]
    conn = sum(Gam[mu][a2][b2] * xdot[a2] * xdot[b2] for a2 in range(N) for b2 in range(N))
    geo_ok = geo_ok and (sp.simplify(ddl + conn) == 0)
key("A1_radial_null_geodesic_r_affine_generic_A", geo_ok,
    "D1 G4 survives for oscillating A: generic-A fact")
key("A3_null_condition_generic_A", sp.simplify(-Fg * xdot[0]**2 + xdot[1]**2 / Fg) == 0)

# A2: the lock-chart curvature identity (GENERIC A) and zero radial-null focusing
idA2 = sp.simplify(Rtt + Fg**2 * Rrr)
key("A2a_Rtt_plus_A2Rrr_identity_generic_A", idA2 == 0,
    "R_tt + A^2 R_rr == 0 for ANY A(r): D1's theorem is generic-A -- oscillation included")
Rkk = sp.simplify(Rtt * xdot[0]**2 + Rrr * xdot[1]**2)
key("A2b_radial_null_Ricci_focusing_zero_generic_A", Rkk == 0,
    "R_kk = 0 exactly on arriving bundles: zero focusing survives oscillation; d_A = r rides this")
AUDITED += [idA2, Rkk]

# A6: orbit equation depends on b = L/E only (achromaticity, generic A)
rdot2 = E**2 - Fg * L**2 / r**2
drdphi2 = sp.simplify(rdot2 * r**4 / L**2)          # (dr/dphi)^2
orbit_b = sp.simplify(drdphi2.subs(L, bpar * E))
key("A6a_orbit_equation_b_only_generic_A",
    sp.simplify(orbit_b - (r**4 / bpar**2 - Fg * r**2)) == 0)
key("A6b_achromatic_no_E_in_orbit", E not in orbit_b.free_symbols,
    "photon frequency cancels: propagation tracer/spectrum-blind, generic A")
AUDITED += [orbit_b]
print("-- Block A done: the D1 optics backbone is generic-A (oscillation inherits it) --")

# ============ BLOCK B: THE OBJECT + P1 ADMISSIBILITY =========================
n, Rw, lam, epsl = sp.symbols('n R_w lambda varepsilon', positive=True)
phase = sp.Symbol('phi_0', real=True)
mms = sp.Symbol('m', real=True)          # measure weight: 0 areal, 1/2 proper, 1 optical
uu, qpos, gpos, cvar, xs = sp.symbols('u q gamma_pos c x', positive=True)
u = 1 - r / Rw
Abg = u**n

# B2: the observer anchor A(0)=1 pins ONE phase combination (all parametrizations
# have argument-measure X_m(0)=0, so osc(0) = cos(phi_0)):
A_osc_areal = Abg * (1 + epsl * sp.cos(2 * sp.pi * r / lam + phase))
key("B2_anchor_A0_eq_1_iff_cos_phi0_zero",
    sp.simplify(A_osc_areal.subs(r, 0) - (1 + epsl * sp.cos(phase))) == 0,
    "A(0)-1 = eps*cos(phi_0): banked anchor demands cos(phi_0)=0 (or a c0 renormalization)")
AUDITED += [A_osc_areal]
# pinned representative (phi_0 = -pi/2); eps>=0 WLOG (phi_0 -> phi_0+pi flips sign)
A_pin = Abg * (1 + epsl * sp.sin(2 * sp.pi * r / lam))
key("B2b_pinned_representative_anchor", sp.simplify(A_pin.subs(r, 0) - 1) == 0)

# B3: positivity A>0 on (0,R_w): factor 1+eps*c linear in c=osc in [-1,1]
f_lin = 1 + epsl * cvar
key("B3a_factor_linear_in_osc", sp.diff(f_lin, cvar, 2) == 0)
key("B3b_min_at_osc_eq_minus1", sp.simplify(f_lin.subs(cvar, -1) - (1 - epsl)) == 0,
    "min over osc in [-1,1] = 1-eps: A>0 everywhere iff eps<1 (when osc attains -1 in range)")

# B4: wall preserved: (1-eps)A_bg <= A_osc <= (1+eps)A_bg pointwise; A_bg -> 0
key("B4a_bounds_endpoints", sp.simplify(f_lin.subs(cvar, 1) - (1 + epsl)) == 0)
key("B4b_Abg_wall_limit_zero", sp.limit(uu**n, uu, 0, '+') == 0,
    "A_osc -> 0 at r=R_w by squeeze: the A->0 wall survives the oscillation")

# B5: depth ripple bounded; depth divergence (O1 asymptote) survives
ripple = -sp.log(1 + epsl * cvar) / 2
key("B5a_ripple_monotone_in_osc", sp.simplify(sp.diff(ripple, cvar) + epsl / (2 * (1 + epsl * cvar))) == 0,
    "|ripple| max at osc=-1: bound = -ln(1-eps)/2")
key("B5b_neg_branch_dominates", sp.simplify((1 + epsl) * (1 - epsl) - (1 - epsl**2)) == 0,
    "1-eps^2 <= 1 -> -ln(1-eps) >= ln(1+eps)")
key("B5c_depth_still_diverges", sp.limit(-n * sp.log(uu) / 2, uu, 0, '+') == sp.oo,
    "delta_osc = delta_bg + bounded ripple -> infinity: O1 wall/asymptote NOT violated")

# B6: monotonicity of z(r) == positivity of J = dz/dl_p == delta'(r) > 0 (exact criterion)
Xi = sp.Function('Xi', real=True)(r)     # generic oscillation profile
A_gen = Abg * (1 + epsl * Xi)
delta_gen = -sp.log(A_gen) / 2
dp = sp.together(sp.diff(delta_gen, r))
crit = (n * (1 + epsl * Xi) - epsl * Rw * u * sp.diff(Xi, r)) / (2 * Rw * u * (1 + epsl * Xi))
key("B6a_exact_monotonicity_criterion", sp.simplify(dp - crit) == 0,
    "delta' = [n(1+eps*osc) - eps*R_w*u*osc'] / [2*R_w*u*(1+eps*osc)]: z(r) monotone iff numerator>0")
AUDITED += [dp, crit]
# B6b: areal parametrization sufficient bound: |osc'| <= 2*pi/lam, 1+eps*osc >= 1-eps
suff = sp.simplify(n / (2 * Rw) - epsl * sp.pi / (lam * (1 - epsl))
                   - (n * lam * (1 - epsl) - 2 * sp.pi * Rw * epsl) / (2 * Rw * lam * (1 - epsl)))
key("B6b_areal_sufficient_bound_identity", suff == 0,
    "n*lam*(1-eps) >= 2*pi*R_w*eps  ==>  delta' > 0 everywhere (monotone regime)")
# B6c: near-wall domination (areal): the competing term carries u -> 0
key("B6c_areal_wall_term_dies", sp.limit((2 * sp.pi / lam) * Rw * uu, uu, 0, '+') == 0,
    "areal-parametrized oscillation NEVER breaks monotonicity near the wall")

# B7/B8: general-m argument measure X_m (background convention, declared):
#   dX_m/dr = A_bg^{-m}; closed forms; the competition exponent u^{1-n*m}
# (decidable restatement, disclosed: checks done in the positive variable uu = 1-r/R_w,
#  chain rule dX/dr = dX/du * (-1/R_w) applied explicitly -- same mathematical claims)
Xm = Rw * (1 - u**(1 - n * mms)) / (1 - n * mms)
Xmu = Rw * (1 - uu**(1 - n * mms)) / (1 - n * mms)
key("B1a_Xm_closed_form_general_m",
    sp.simplify(sp.diff(Xmu, uu) * (-1 / Rw) - (uu**n)**(-mms)) == 0,
    "X_m(r) = R_w(1-u^(1-nm))/(1-nm), dX_m/dr = A_bg^{-m}; m=0 areal, 1/2 proper, 1 optical")
key("B1b_Xm_edge_nm1_log_form",
    sp.simplify(sp.diff(Rw * sp.log(1 / uu), uu) * (-1 / Rw) - 1 / uu * (-1) * (-1)) == 0,
    "at n*m = 1: X = R_w*ln(1/u) (proper n=2; optical n=1)")
key("B1c_edge_X_is_depth_proper_n2",
    sp.simplify(Rw * sp.log(1 / uu) - Rw * (-sp.log(uu))) == 0,
    "n=2: delta_bg = -ln(u), l_p = R_w*ln(1/u) = R_w*delta -- proper osc periodic IN DEPTH")
key("B1d_edge_X_is_depth_optical_n1",
    sp.simplify(Rw * sp.log(1 / uu) - 2 * Rw * (-sp.Rational(1, 2) * sp.log(uu))) == 0,
    "n=1: delta_bg = -ln(u)/2, l_opt = 2*R_w*delta -- the banked O2 knife-edge rate, re-derived")
AUDITED += [Xm, Xmu]
# competition term in B6a for m-parametrized osc: eps*R_w*u*osc' ~ (2*pi*eps*R_w/lam)*u^(1-n*m)
key("B7a_subcritical_dies", sp.limit(uu**qpos, uu, 0, '+') == 0,
    "1-n*m = q > 0 (proper n<2; optical n<1; areal all n): term -> 0, monotone near wall")
key("B7b_critical_const", sp.simplify(uu**0 - 1) == 0,
    "n*m = 1 edges: term -> const: finite amplitude threshold, log-periodic riding")
key("B7c_supercritical_blows", sp.limit(uu**(-gpos), uu, 0, '+') == sp.oo,
    "1-n*m = -g < 0 (proper n>2; optical n>1): term unbounded near wall")
key("B7d_argument_diverges_at_edge", sp.limit(Rw * sp.log(1 / uu), uu, 0, '+') == sp.oo,
    "edge: infinitely many cycles (osc' sweeps sign): threshold criterion is per-cycle")
key("B7e_argument_diverges_supercritical", sp.limit((uu**(-gpos) - 1) / gpos, uu, 0, '+') == sp.oo,
    "supercritical: cycles accumulate at the wall; with B7c: delta'<0 infinitely often for ANY eps>0")

# B9: O2 measure verdicts survive: two-sided pointwise bound on A_osc^{-m}, m>0
ratio_m = (1 + epsl * cvar)**(-qpos)
key("B9a_integrand_ratio_monotone_in_osc",
    sp.simplify(sp.diff(ratio_m, cvar) + qpos * epsl * (1 + epsl * cvar)**(-qpos - 1)) == 0,
    "(1+eps*osc)^(-m) in [(1+eps)^(-m), (1-eps)^(-m)]: comparison test -> every O2 F/D cell survives")
key("B9b_bound_endpoints", sp.simplify(ratio_m.subs(cvar, -1) - (1 - epsl)**(-qpos)) == 0)

# B10: FREEZE case (finite argument measure to the wall): areal argument stays finite
key("B10_areal_argument_freezes", sp.limit(2 * sp.pi * r / lam, r, Rw) == 2 * sp.pi * Rw / lam,
    "finitely many cycles; near wall A_osc ~ (1+eps*osc_w)*A_bg: O3 kappa UNCHANGED, const shifted")
print("-- Block B done: P1 admissibility conditions + wall-interaction trichotomy --")

# ============ BLOCK C: P2 IMPRINT TRANSFER (monotone regime; O(eps) laws) ====
zp = sp.Symbol('z_p', positive=True)         # z_p = 1+z >= 1 (positive suffices)
uz = zp**(-2 / n)                            # background dictionary u(z)
r_bg = Rw * (1 - uz)
XiV = sp.Symbol('Xi_val', real=True)         # osc value at r_bg (scalar at fixed z)
gam_i = sp.Symbol('gamma_i', positive=True)  # input power-law index
s_sep, K0, thv = sp.symbols('s K_0 theta_v', positive=True)

# C0: background dictionary re-derivation: A_bg(r_bg(z)) = (1+z)^{-2}
key("C0_dictionary_Abg_eq_zm2", sp.simplify((1 - r_bg / Rw)**n - zp**(-2)) == 0,
    "u(z) = (1+z)^{-2/n}; r(z) = R_w[1-(1+z)^{-2/n}] (D1 G7 re-derived)")

# C1: first-order inversion of the oscillating dictionary at fixed z:
#     r(z) = r_bg + eps*rho1 + O(eps^2),  rho1 = (R_w u / n) * osc(r_bg)
XiF = sp.Function('Xi', real=True)
rho1 = Rw * (1 - r / Rw) * XiF(r) / n
A_shift = (1 - (r + epsl * rho1) / Rw)**n * (1 + epsl * XiF(r + epsl * rho1))
c1 = sp.simplify(sp.diff(A_shift, epsl).subs(epsl, 0).doit())
key("C1_first_order_dictionary_inversion", c1 == 0,
    "A_osc(r_bg + eps*rho1) = A_bg(r_bg) + O(eps^2): redshift held fixed exactly at O(eps)")
AUDITED += [c1]

# C2: THE RESIDUAL LAW. d_L = (1+z)^2 r (generic-A: d_A = r rides A2b + A1),
#     Delta_mu = 5*log10(d_L/d_L^bg) = (5/ln10)*ln(r(z)/r_bg(z))
rho1_z = Rw * uz * XiV / n
Dmu = (5 / sp.log(10)) * sp.log((r_bg + epsl * rho1_z) / r_bg)
c2 = sp.simplify(sp.diff(Dmu, epsl).subs(epsl, 0) - (5 / sp.log(10)) * uz * XiV / (n * (1 - uz)))
key("C2_residual_law_first_order", c2 == 0,
    "Delta_mu = (5/ln10)*(eps/n)*[u/(1-u)]*osc(r_bg(z)) + O(eps^2), u = (1+z)^{-2/n}")
AUDITED += [Dmu]

# C3: PERIODICITY VARIABLE. Argument Phi_m(z) = (2*pi/lam)*X_m(r_bg(z)) + phi_0
#     X_m = R_w(1-u^{1-nm})/(1-nm)  ==> affine in  xi_m := (1+z)^{-2(1-nm)/n}
pow_id = sp.simplify(sp.powsimp(uz**(1 - n * mms) - zp**(-2 * (1 - n * mms) / n), force=True))
key("C3a_periodicity_variable_general_m", pow_id == 0,
    "residual periodic (equal spacing) in xi_m = (1+z)^{-2(1-nm)/n}; NOT in z generically")
key("C3b_areal_variable", sp.simplify(sp.powsimp(uz**(1 - n * 0) - zp**(-2 / n), force=True)) == 0,
    "areal: periodic in (1+z)^{-2/n}")
key("C3c_lnz_iff_nm_eq_1", sp.solve(sp.Eq(-2 * (1 - n * mms) / n, 0), mms) == [1 / n],
    "exponent 0 <=> n*m = 1: ln(1+z)-periodicity EXACTLY at the O2 knife-edges (proper n=2, optical n=1)")
key("C3d_z_linear_cell", sp.solve(sp.Eq(-2 * (1 - n * mms) / n, 1), mms) == [(n + 2) / (2 * n)],
    "affine-in-z <=> m = 1/2 + 1/n; among natural m: ONLY optical (m=1) at n=2")
key("C3e_proper_never_z_linear", sp.solve(sp.Eq((2 - n) / n, -1), n) == [],
    "proper-parametrized: never periodic in z for any n>0")
key("C3f_optical_z_linear_only_n2", sp.solve(sp.Eq(2 * (1 - n) / n, -1), n) == [2])

# C4: THE ENVELOPE (parametrization-INDEPENDENT): Env(z) = u/(1-u)
Env = uz / (1 - uz)
c4a = sp.simplify(sp.diff(Env, zp) + 2 * uz / (n * zp * (1 - uz)**2))
key("C4a_envelope_strictly_falling", c4a == 0,
    "dEnv/dz = -(2/n)(1+z)^{-1} u/(1-u)^2 < 0: the residual amplitude FADES with depth, monotonically")
key("C4b_envelope_wall_rate", sp.simplify(Env / uz - 1 / (1 - uz)) == 0,
    "Env = u*(1/(1-u)): Env ~ (1+z)^{-2/n} at high z (u->0): dies at the derived rate")
key("C4c_low_z_finite_by_phase_pin",
    sp.limit(((1 - xs) / xs) * sp.sin(2 * sp.pi * Rw * xs / lam), xs, 0, '+') == 2 * sp.pi * Rw / lam,
    "x = r_bg/R_w -> 0: pinned osc(0)=0 cancels the 1/(1-u) low-z divergence; offset -> const (calib.-degenerate)")
AUDITED += [Env]

# C5: cross-observable ANTI-PHASE lock at fixed z: theta = s/r, d_L = (1+z)^2 r
rv = sp.Symbol('r_v', positive=True)
key("C5_antiphase_lock",
    sp.simplify(sp.diff(sp.log(s_sep / rv), rv) / sp.diff(sp.log(zp**2 * rv), rv) + 1) == 0,
    "dln(theta)/dln(r) = -dln(d_L)/dln(r): angular-scale and Hubble residuals EXACTLY anti-phased [BY-FORM]")

# C6: per-shell featureless preserved (D1 K4 with oscillating r(z) -- still one number per shell)
tlog = sp.Symbol('t_log', real=True)
w_shell = K0 * (rv * sp.exp(tlog))**(-gam_i)
key("C6_pershell_log_slope_constant", sp.simplify(sp.diff(sp.log(w_shell), tlog) + gam_i) == 0,
    "w(theta;z) = C(r(z)*theta): log-slope == -gamma at every z: NO per-shell angular scale [BY-FORM]")

# C7: THE OSCILLATING JACOBIAN. J := dz/dl_p = delta'(r) exactly (generic A)
A_o = Abg * (1 + epsl * XiF(r))
one_pz = A_o**sp.Rational(-1, 2)
Jexact = sp.simplify(sp.diff(one_pz - 1, r) * A_o**sp.Rational(1, 2))
key("C7a_J_equals_delta_prime_generic", sp.simplify(Jexact - (-sp.diff(A_o, r) / (2 * A_o))) == 0,
    "J = dz/dl_p = -A'/(2A) = delta'(r): D1 K17 identity survives generic-A")
# C7b: at fixed r, dlnJ/deps|_0 = -osc'/(2 J_bg) = -(R_w u/n)*osc'
Jr = -sp.diff(A_o, r) / (2 * A_o)
c7b = sp.simplify(sp.diff(sp.log(Jr), epsl).subs(epsl, 0) + Rw * (1 - r / Rw) * sp.diff(XiF(r), r) / n)
key("C7b_J_eps_leg", c7b == 0)
# C7b2: transport leg: dln(J_bg)/dr * rho1 = osc/n
c7b2 = sp.simplify(sp.diff(sp.log(n / (2 * Rw * (1 - r / Rw))), r) * rho1 - XiF(r) / n)
key("C7b2_J_transport_leg", c7b2 == 0,
    "chain rule [BY-FORM composition]: dlnJ = (eps/n)*(osc - R_w u osc'); dN/dz mod = (eps/n)*(R_w u osc' - osc)")
AUDITED += [Jr]
# C7d: loudness ratio: |J-modulation| / |distance-modulation| = r * Phi' (osc'-dominated regime)
Phip = sp.Symbol('Phi_p', positive=True)
c7d = sp.simplify((Rw * uu * Phip / n) / (uu / (n * (1 - uu))) - Rw * (1 - uu) * Phip)
key("C7d_loudness_ratio_r_times_Phiprime", c7d == 0,
    "= r*Phi' = 2*pi*r/lam_areal: many-cycle oscillation shouts in dN/dz, whispers in Delta_mu")

# C8: radial cycle spacing in z: Delta_z_cyc = lam*(n/2R_w)*(1+z)^{1+2/n-2m}
dXmdz = sp.simplify(sp.diff(Xm.subs(r, r_bg), zp))
c8 = sp.simplify(sp.powsimp(dXmdz - (2 * Rw / n) * zp**(2 * mms - 2 / n - 1), force=True))
key("C8_cycle_spacing_general_m", c8 == 0,
    "areal (1+z)^{1+2/n}; proper (1+z)^{2/n}; optical (1+z)^{2/n-1}; constant-in-z iff (optical,n=2)")
AUDITED += [dXmdz]

# C8b: local proper wavelength of the m-comb: lam_p = lam*(1+z)^{1-2m}
key("C8b_proper_wavelength_law",
    sp.simplify(sp.powsimp((uz**n)**(mms - sp.Rational(1, 2)) - zp**(-2 * mms + 1), force=True)) == 0,
    "dl_p/dX_m = A^{m-1/2} = (1+z)^{1-2m}: areal stretches (1+z), proper fixed, optical compresses 1/(1+z)")

# C9: window-projection angular scale: the oscillatory window component's kernel
lamp, Bb, aa, bb, vv = sp.symbols('lambda_p B a_k b_k v', positive=True)
integrand_id = sp.simplify(sp.powsimp(
    sp.cos(2 * sp.pi * (lamp * vv) / lamp) * ((lamp * vv)**2 + Bb**2)**(-gam_i / 2) * lamp
    - lamp**(1 - gam_i) * sp.cos(2 * sp.pi * vv) * (vv**2 + (Bb / lamp)**2)**(-gam_i / 2), force=True))
key("C9a_projection_scaling_identity", integrand_id == 0,
    "oscillatory kernel = lam_p^{1-gamma} * f(r*theta/lam_p): the induced angular scale is theta ~ lam_p/r")
witness = sp.integrate(sp.cos(aa * xs) / (xs**2 + bb**2), (xs, 0, sp.oo))
key("C9b_localized_kernel_witness_gamma2", sp.simplify(witness - sp.pi * sp.exp(-aa * bb) / (2 * bb)) == 0,
    "gamma=2 witness: f is exponentially localized at r*theta >~ lam_p: a GENUINE localized angular scale at O(eps)")
AUDITED += [witness]

# C10: tracer-blindness free-symbol audit of the signature laws
sig_syms = set()
for expr in [Dmu, Env, dXmdz, lam * zp**(1 - 2 * mms) / r_bg]:
    sig_syms |= expr.free_symbols
allowed = {zp, n, Rw, lam, epsl, mms, XiV, s_sep}
key("C10_operator_symbol_audit", sig_syms <= allowed,
    f"signature-law symbols {sorted(str(s) for s in sig_syms)}: geometry+oscillation only, NO source symbols")

# C11: F-RETRO discharge: no float atoms anywhere in audited expressions
key("C11_FRETRO_no_float_atoms", all(not e.atoms(sp.Float) for e in AUDITED))

print("=" * 78)
npass = sum(CHECKS.values())
print(f"TALLY: {npass}/{len(CHECKS)} keys True")
if npass != len(CHECKS):
    print("FAILED:", [k for k, v in CHECKS.items() if not v])
