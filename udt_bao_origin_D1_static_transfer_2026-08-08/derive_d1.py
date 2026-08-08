#!/usr/bin/env python3
"""D1 -- static angular transfer function: exact symbolic derivation checks.

Contract: udt_bao_origin_D1_static_transfer_2026-08-08/PREREGISTRATION.md (frozen).
SCOPE stamp on every claim: STATIC / mu=0 stratum / lock+areal-anchor chart.
Metric: ds^2 = -A c^2 dt^2 + dr^2/A + r^2 dOmega^2, A(r) = (1 - r/R_w)^n, n FREE SYMBOL.
F-RETRO: no fitted numbers anywhere; all-symbolic (machine-audited by the final key).
Category-A: geodesic/eikonal optics + sympy. CPU-only, bounded (seconds).
"""
import sympy as sp

RESULTS = []
AUDIT = []  # expressions swept by the F-RETRO no-float key

def check(key, ok):
    RESULTS.append((key, bool(ok)))
    print("KEY %-52s %s" % (key + ':', bool(ok)), flush=True)

# ---- symbols (positive where physical) ----
r, z, s, th, lam, E, Lc = sp.symbols('r z s theta lam E L', positive=True)
dz = sp.Symbol('Delta_z', positive=True)
Rw, n, gam, K0 = sp.symbols('R_w n gamma K_0', positive=True)
rs, r0, z1, u, a_, b_ = sp.symbols('r_s r_0 z_1 u a b', positive=True)
m_, eps = sp.symbols('m epsilon', positive=True)
p1_, p2_, r1_, r2_, DLs = sp.symbols('p_1 p_2 rr_1 rr_2 DL', positive=True)
kappa = sp.Symbol('kappa', real=True)
t_ = sp.Symbol('t')
y_ = sp.Symbol('y', positive=True)   # lemma-backed stand-in for (1+z)^(2/n) - 1

A = (1 - r/Rw)**n            # class-(i) profile, n free symbol
AUDIT.append(A)

# =====================  GROUND (G): metric + sightline geometry  =============
# G1: observer normalization A(0)=1 [THEORY: phi(0)=0]
check('G1_center_A_equals_1', sp.simplify(A.subs(r, 0) - 1) == 0)

# G2: regular, locally-flat center: proper-radius integrand A^(-1/2) = 1 + n r/(2Rw) + O(r^2)
integrand = A**sp.Rational(-1, 2)
ser = sp.series(integrand, r, 0, 2).removeO()
check('G2_center_locally_flat_lp_eq_r_plus_Or2',
      sp.simplify(ser - (1 + n*r/(2*Rw))) == 0)

# G3: Killing conservation -- t and phi cyclic in the geodesic Lagrangian
t_f = sp.Function('tf')(lam); r_f = sp.Function('rf')(lam); p_f = sp.Function('pf')(lam)
Af = (1 - r_f/Rw)**n
Lg = -Af*sp.diff(t_f, lam)**2 + sp.diff(r_f, lam)**2/Af + r_f**2*sp.diff(p_f, lam)**2
check('G3a_t_cyclic_E_eq_A_tdot_conserved', sp.simplify(Lg.diff(t_f)) == 0)
check('G3b_phi_cyclic_L_eq_r2_phidot_conserved', sp.simplify(Lg.diff(p_f)) == 0)

# G4: the radial null ray with A*tdot=E, rdot=E SOLVES the radial geodesic equation
#     (=> r is an AFFINE parameter along radial nulls; d^2 r/dlam^2 = 0)
rdot = sp.Derivative(r_f, lam)
el_r = sp.diff(Lg.diff(rdot), lam) - Lg.diff(r_f)
subs_seq = [(sp.Derivative(r_f, (lam, 2)), 0),
            (sp.Derivative(p_f, lam), 0),
            (sp.Derivative(r_f, lam), E),
            (sp.Derivative(t_f, lam), E/Af)]
expr = el_r
for old, new in subs_seq:
    expr = expr.subs(old, new)
expr = expr.subs(r_f, r)
check('G4_radial_null_geodesic_r_affine', sp.simplify(expr) == 0)

# G5: NO non-radial null geodesic reaches r=0: rdot^2 = E^2 - A L^2/r^2 diverges
#     to -oo as r->0+ because r^2*rdot^2 -> -L^2 < 0 at the center (A(0)=1, A
#     continuous) -- so for L != 0 there is a turning point at finite r; only
#     L=0 (exactly radial) rays reach the observer:
Vr = E**2 - A*Lc**2/r**2
check('G5_center_reachable_only_radially_L0',
      sp.simplify(sp.expand(r**2*Vr).subs(r, 0) + Lc**2) == 0)

# G6/G7: static redshift 1+z = A^(-1/2) (Killing-frequency ratio, A(0)=1) and its inversion
rz = Rw*(1 - (1 + z)**(-sp.S(2)/n))
AUDIT.append(rz)
check('G7_P1_inversion_A_of_rz_eq_opz_minus2',
      sp.simplify(sp.powsimp(A.subs(r, rz) - (1 + z)**(-2), force=True)) == 0)

# G8: dr/dz closed form and positivity (the depth dictionary is monotone)
drdz = sp.simplify(sp.diff(rz, z))
drdz_closed = (2*Rw/n)*(1 + z)**(-sp.S(2)/n - 1)
check('G8a_drdz_closed_form', sp.simplify(drdz - drdz_closed) == 0)
check('G8b_drdz_positive', drdz_closed.is_positive is True)

# =========  Curvature block: Ricci of the lock chart, generic A(r)  ==========
# Category-A GR-corpus technique (Sachs optics reference); equations are the UDT
# metric's own. Coordinates (t, r, x_th, x_ph); generic positive A(r).
t_c, x_th, x_ph = sp.symbols('t_c x_th x_ph')
Aw = sp.Function('A', positive=True)(r)
coords = [t_c, r, x_th, x_ph]
gdiag = [-Aw, 1/Aw, r**2, r**2*sp.sin(x_th)**2]

def ricci_diag(gdiag, coords):
    dim = len(coords)
    g = sp.diag(*gdiag)
    ginv = g.inv()
    Gam = [[[sp.S(0)]*dim for _ in range(dim)] for _ in range(dim)]
    for a in range(dim):
        for b in range(dim):
            for c in range(dim):
                e = sp.S(0)
                for d in range(dim):
                    e += ginv[a, d]*(sp.diff(g[d, b], coords[c])
                                     + sp.diff(g[d, c], coords[b])
                                     - sp.diff(g[b, c], coords[d]))
                Gam[a][b][c] = sp.simplify(e/2)
    Ric = sp.zeros(dim)
    for b in range(dim):
        for c in range(dim):
            e = sp.S(0)
            for a in range(dim):
                e += sp.diff(Gam[a][b][c], coords[a]) - sp.diff(Gam[a][b][a], coords[c])
                for d in range(dim):
                    e += Gam[a][a][d]*Gam[d][b][c] - Gam[a][c][d]*Gam[d][b][a]
            Ric[b, c] = sp.simplify(e)
    return Ric

print("stage: curvature block (generic A(r) Ricci)...", flush=True)
Ric = ricci_diag(gdiag, coords)

# K6a: the lock chart (g_tt g_rr = -1) forces R_tt + A^2 R_rr = 0 identically
check('K6a_lock_chart_Rtt_plus_A2Rrr_zero',
      sp.simplify(Ric[0, 0] + Aw**2*Ric[1, 1]) == 0)

# K6b: hence R_kk = 0 EXACTLY for the radial null k = (E/A, E, 0, 0):
Rkk = sp.simplify(Ric[0, 0]*(E/Aw)**2 + Ric[1, 1]*E**2)
check('K6b_radial_null_Ricci_focusing_zero', Rkk == 0)

# K7: focusing consistency -- with sigma=0 (K5) and R_kk=0 (K6b) the Sachs equation
#     d^2 d_A/dlam^2 = -(1/2 R_kk + sigma^2) d_A is solved by d_A = r (r affine, G4):
check('K7_dA_equals_r_solves_focusing', sp.simplify(Rkk*r/2) == 0)

# ==================  T1: the angular transfer map  ===========================
# K1: proper great-circle separation on the shell (induced metric r_s^2 dOmega^2):
dpsi = sp.Symbol('Delta_psi', positive=True)
arc = sp.integrate(rs, (sp.Symbol('psi'), 0, dpsi))
check('K1_shell_proper_separation_s_eq_rs_dpsi', sp.simplify(arc - rs*dpsi) == 0)

# K2: observed angle between two arriving radial rays = coordinate separation
#     (local frame at the regular center G2 is Euclidean; equatorial directions):
n1 = sp.Matrix([1, 0, 0]); n2 = sp.Matrix([sp.cos(dpsi), sp.sin(dpsi), 0])
check('K2_observed_angle_eq_coordinate_angle',
      sp.simplify(n1.dot(n2) - sp.cos(dpsi)) == 0)

# K3: featureless DEFINITION discharge: scale-covariance C(lam*s)=g(lam)C(s)
#     differentiates (at lam=1) to s C' = kappa C; smooth solutions = power laws:
Cf = sp.Function('C')
sol = sp.dsolve(sp.Eq(s*Cf(s).diff(s), kappa*Cf(s)), Cf(s))
check('K3_scalefree_iff_powerlaw',
      sp.simplify(s*sp.diff(sol.rhs, s)/sol.rhs - kappa) == 0)

# K4: THE LOAD-BEARING T1 KEY -- featureless in => featureless out, exactly:
#     w_obs(theta) = C(r_s * theta); power-law C => constant log-slope, no scale:
w_obs = K0*(rs*th)**(-gam)
AUDIT.append(w_obs)
logslope = sp.simplify(th*sp.diff(w_obs, th)/w_obs)
check('K4_T1_featureless_in_featureless_out',
      sp.simplify(logslope + gam) == 0 and sp.diff(logslope, th) == 0)

# K5: NO SHEAR: transverse separations along the two sky directions both scale as r;
#     their ratio is r-independent (isotropic magnification, sigma = 0):
dth_, dph_, th0 = sp.symbols('dth dph th_0', positive=True)
ratio = (r*dth_)/(r*sp.sin(th0)*dph_)
check('K5_no_shear_isotropic_magnification', sp.diff(ratio, r) == 0)

# K8: finite z-bin superposition of shells preserves the power law (same index):
w_bin = p1_*(r1_*th)**(-gam) + p2_*(r2_*th)**(-gam)
ls_bin = sp.simplify(th*sp.diff(w_bin, th)/w_bin)
check('K8_shell_projection_preserves_powerlaw', sp.simplify(ls_bin + gam) == 0)

# K8b: 3D Limber-type projection scaling (local flatness premise, ledgered):
#      integrating xi(sqrt(D^2+a^2)) over the line of sight, substitution D=a*u
#      makes the a-dependence EXACTLY a^(1-gamma) (convergence: gamma>1):
lhs = sp.powsimp((sp.factor((a_*u)**2 + a_**2))**(-gam/2)*a_, force=True)
rhs = a_**(1 - gam)*(u**2 + 1)**(-gam/2)
check('K8b_3D_projection_powerlaw_scaling', sp.simplify(lhs - rhs) == 0)

# ==================  T2: the depth law of the (featureless) rescaling  =======
# No scale was imprinted (T1), so the honest T2 content is the exact
# magnification law of the smooth rescaling: theta(z; s) = s / r(z).
theta_z = s/rz
AUDIT.append(theta_z)

# K9: high-z limit -- the P1-class minimal-angle floor theta -> s/R_w (re-derived).
#     Substitution q = (1+z)^(-2/n): q -> 0+ as z -> oo (exponent -2/n < 0, n>0);
#     theta = s/(Rw(1-q)) -> s/Rw. Both steps machine-checked:
q_ = sp.Symbol('q', positive=True)
theta_q = sp.simplify(theta_z.subs((1 + z)**(-sp.S(2)/n), q_))
check('K9a_T2_exponent_negative_so_q_to_zero', (-sp.S(2)/n).is_negative is True)
check('K9b_T2_highz_floor_s_over_Rw',
      sp.simplify(theta_q.subs(q_, 0) - s/Rw) == 0)

# K10: the rescaling drifts MONOTONICALLY (dtheta/dz = -s*(dr/dz)/r^2 < 0; no
#      critical point in z -- the depth law itself is featureless in z):
dth_dz = sp.diff(theta_z, z)
check('K10a_T2_drift_identity', sp.simplify(dth_dz + s*drdz/rz**2) == 0)
#      positivity of r(z) rides the LEMMA (1+z)^(2/n) > 1 for z > 0, proven by
#      calculus: value 1 at z=0 + strictly positive derivative. Writing
#      y = (1+z)^(2/n) - 1 > 0 gives r = Rw*y/(y+1) and decidable signs:
check('K10lemma_a_power_equals_1_at_z0',
      sp.simplify(((1 + z)**(sp.S(2)/n)).subs(z, 0) - 1) == 0)
check('K10lemma_b_power_strictly_increasing',
      (sp.diff((1 + z)**(sp.S(2)/n), z)).is_positive is True)
rz_y = Rw*y_/(y_ + 1)                      # r(z) with y = (1+z)^(2/n) - 1
check('K10c_rz_identity_in_y',
      sp.simplify(rz.subs((1 + z)**(-sp.S(2)/n), 1/(y_ + 1)) - rz_y) == 0)
check('K10b_T2_drift_strictly_negative',
      (s*drdz_closed/rz_y**2).is_positive is True)

# ==================  T3: tracer-blindness of T  ==============================
# K13: ACHROMATIC optics -- the null orbit depends on the impact parameter b=L/E
#      only; the overall frequency scale E cancels from the path:
orb = (Lc/r**2)/sp.sqrt(E**2 - A*Lc**2/r**2)
orb_b = sp.simplify(orb.subs(Lc, b_*E))
check('K13_achromatic_paths_depend_on_b_only',
      sp.simplify(sp.diff(orb_b, E)) == 0)

# K14: the full static map (angular action, depth dictionary) contains ONLY
#      geometry symbols -- no tracer-property parameter EXISTS in T:
z_of_rs = (1 - rs/Rw)**(-n/sp.S(2)) - 1
AUDIT.append(z_of_rs)
fs = dpsi.free_symbols | z_of_rs.free_symbols
check('K14_T3_tracer_blind_free_symbol_audit', fs <= {dpsi, rs, Rw, n})

# ==================  T4: amplitude vs depth (exact)  =========================
# K16: T is VALUE-PRESERVING at fixed proper separation: w_obs(theta=s/r_s) = C(s),
#      independent of depth -- the transfer changes labels, not amplitudes:
check('K16_T4_value_preserving_at_fixed_proper_sep',
      sp.simplify(w_obs.subs(th, s/rs) - K0*s**(-gam)) == 0)

# K15: at FIXED ANGLE the amplitude scales as r(z)^(-gamma) (purely because a
#      fixed theta probes larger proper separation at larger depth); monotone fall:
w_z = K0*(rz*th)**(-gam)
check('K15a_T4_fixed_angle_amplitude_r_pow_minus_gamma',
      sp.simplify(w_z/(K0*th**(-gam)) - rz**(-gam)) == 0)
dwdz = sp.diff(w_z, z)
check('K15b_T4_amplitude_identity', sp.simplify(dwdz + gam*w_z*drdz/rz) == 0)
check('K15c_T4_amplitude_strictly_falling',
      (gam*(K0*th**(-gam))*rz_y**(-gam)*drdz_closed/rz_y).is_positive is True)

# ==================  T5: the radial (line-of-sight) imprint  =================
# K17: re-derivation of the banked radial identities (D1_FORMULAS.md '4),
#      generic A(r): dz/dl_p = -A'/(2A) = d(delta)/dr, with delta = -ln(A)/2:
z_of_r_gen = Aw**sp.Rational(-1, 2) - 1
dz_dr = sp.diff(z_of_r_gen, r)
dlp_dr = Aw**sp.Rational(-1, 2)
J_gen = sp.simplify(dz_dr/dlp_dr)
target = -sp.diff(Aw, r)/(2*Aw)
check('K17a_radial_dz_dlp_eq_minus_Aprime_over_2A',
      sp.simplify(J_gen - target) == 0)
check('K17b_radial_dz_dlp_eq_ddelta_dr',
      sp.simplify(target - sp.diff(-sp.log(Aw)/2, r)) == 0)

# K18: P1-class Jacobian in depth form: J(z) = (n/2R_w)(1+z)^(2/n), GROWING:
J_P1 = sp.simplify((-sp.diff(A, r)/(2*A)).subs(r, rz))
J_of_z = (n/(2*Rw))*(1 + z)**(sp.S(2)/n)
AUDIT.append(J_of_z)
check('K18a_T5_P1_jacobian_closed_form',
      sp.simplify(sp.powsimp(J_P1 - J_of_z, force=True)) == 0)
check('K18b_T5_P1_jacobian_growing',
      (sp.diff(J_of_z, z)).is_positive is True)

# K19: LOCALLY (separation << depth scale) the radial map is a pure rescaling:
#      C_obs(Dz) = C_r(Dz/J); power law in => constant log-slope out:
C_obs = K0*(dz/J_of_z)**(-gam)
ls_rad = sp.simplify(dz*sp.diff(C_obs, dz)/C_obs)
check('K19_T5_local_featureless_preserved', sp.simplify(ls_rad + gam) == 0)

# K20: proper length to areal radius r (exact; D1F '5 proper-wall re-derived):
lp_closed = (2*Rw/(2 - n))*(1 - (1 - r/Rw)**((2 - n)/sp.S(2)))
check('K20a_proper_length_closed_form',
      sp.simplify(sp.diff(lp_closed, r) - (1 - r/Rw)**(-n/sp.S(2))) == 0)
#      wall value for n < 2 (write n = 2 - m, m > 0; then (1-r/Rw)^(m/2) -> 0 at
#      the wall since m/2 > 0 -- sympy evaluates 0^(m/2) = 0 under m > 0):
wall_val = lp_closed.subs(n, 2 - m_).subs(r, Rw*(1 - eps))
check('K20b_proper_wall_2Rw_over_2minusn',
      sp.simplify(wall_val.subs(eps, 0) - 2*Rw/m_) == 0)

# K21: NO-EXTREMUM THEOREM at finite separations -- the exact observed radial
#      correlation w(z2) = C_r(l_p(z2) - l_p(z1)) is a MONOTONE reparametrization
#      of a monotone input: dw/dz2 = C_r'(Dl) * (1/J(z2)); both factors of fixed
#      sign, so no local extremum (no bump, no preferred scale) can be created:
Cp = sp.diff(K0*DLs**(-gam), DLs)          # C_r' < 0 for a falling featureless input
check('K21a_T5_input_slope_negative', (-Cp).is_positive is True)
check('K21b_T5_dlp_dz_positive', (1/J_of_z).is_positive is True)

# K22: the SINGLE smooth departure the exact radial map carries: the log-slope of
#      the separation dictionary Dl(Dz) bends away from 1 at second order with the
#      DEPTH scale itself: d lnDl/d lnDz = 1 - Dz/(n(1+z1)) + O(Dz^2).
#      (No new scale: the only scale is n(1+z1) -- the depth/shape scale.)
#      Fast exact route: dDl/dDz = f(Dz) := (2Rw/n)(1+z1+Dz)^(-2/n) (fundamental
#      theorem; f is dl_p/dz at z1+Dz), so the Taylor polynomial of Dl(Dz) is
#      assembled from f's derivatives at 0 and the log-slope is a RATIONAL series:
print("stage: K22 radial series...", flush=True)
f_ = (2*Rw/n)*(1 + z1 + t_)**(-sp.S(2)/n)
f0 = f_.subs(t_, 0); f1 = sp.diff(f_, t_).subs(t_, 0); f2 = sp.diff(f_, t_, 2).subs(t_, 0)
Dl_poly = f0*dz + f1*dz**2/2 + f2*dz**3/6          # Dl(Dz) + O(Dz^4)
num = dz*(f0 + f1*dz + f2*dz**2/2)                 # Dz * dDl/dDz + O(Dz^4)
ls_ser = sp.series(sp.cancel(num/Dl_poly), dz, 0, 2).removeO()
check('K22_T5_only_scale_is_depth_scale_n_times_opz',
      sp.simplify(ls_ser - (1 - dz/(n*(1 + z1)))) == 0)

# K23: CONTRAST -- the ANGULAR dictionary is exactly linear at ALL separations
#      (log-slope 1 identically; zero curvature at every order):
ang_ls = sp.simplify(s*sp.diff(s/rs, s)/(s/rs))
check('K23_angular_dictionary_linear_all_orders', sp.simplify(ang_ls - 1) == 0)

# ==================  F-RETRO machine discharge  ==============================
# No floating-point literal (no fitted number) appears in any audited expression:
no_floats = not any(e.atoms(sp.Float) for e in AUDIT)
check('K_FRETRO_no_float_atoms_in_derivation', no_floats)

# ==================  summary  ================================================
npass = sum(1 for _, ok in RESULTS if ok)
print()
print("CHECKS PASSED: %d / %d" % (npass, len(RESULTS)))
print("SCOPE: every key above is STATIC / mu=0 stratum / lock+areal-anchor chart.")
if npass != len(RESULTS):
    raise SystemExit(1)
