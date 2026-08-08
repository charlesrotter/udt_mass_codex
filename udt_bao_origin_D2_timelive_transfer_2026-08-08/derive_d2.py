#!/usr/bin/env python3
# derive_d2.py -- D2: the TIME-LIVE transfer function (mixing unmuted). Exact sympy, float-free.
# Contract: PREREGISTRATION.md (frozen). Every boxed claim in DERIVATION_NOTES.md cites a KEY here.
# Bounded: pure symbolics, no gruntz limits on symbolic exponents, no solves beyond quadratics,
# single process. Chunk-built per the chunked-output rule.
import sympy as sp

RESULTS = []
def key(name, val):
    ok = bool(val)
    RESULTS.append((name, ok))
    print(f"KEY {name} = {ok}")

# ---------------- symbols ----------------
# rho = e^{delta} >= 1 boost/clock ratio of the pair (1+z at mu=0); s = screen ratio R_q/R_p;
# mu = clock->screen mixing (declared positive wlog: lambda_t depends on mu^2 only -- evenness
# is explicit in the charpoly; sign-odd content lives in the k-field channel, Block B).
rho, s, mu = sp.symbols('rho s mu', positive=True)
lam = sp.Symbol('lam')
m2 = sp.Symbol('m2', positive=True)          # m2 = mu^2
w = sp.Symbol('w', positive=True)            # s = 1/rho + w parametrizes the s > 1/rho window
th = sp.Symbol('theta', positive=True)       # angular separation
n_, Rw = sp.symbols('n R_w', positive=True)  # class-(i) profile symbols (n FREE, n>0 slice)
q_ = sp.Symbol('q', positive=True)           # q = 1 - r/R_w in (0,1)
z_ = sp.Symbol('z', positive=True)

# ============ BLOCK A: the mixing block, exactly (arrow layer; lane ground re-derived) ============
eta = sp.diag(-1, 1, 1)
A_arrow = sp.Matrix([[1/rho, 0, mu], [0, rho, 0], [0, 0, s]])
Adag = eta.inv() * A_arrow.T * eta
C = sp.simplify(Adag * A_arrow)

# A1: full 3x3 charpoly factors as (lam - rho^2)*(lam^2 - T*lam + d): radial slot DECOUPLES.
T2 = 1/rho**2 + s**2 - mu**2
d2 = s**2/rho**2
cp = C.charpoly(lam).as_expr()
target = (lam - rho**2) * (lam**2 - T2*lam + d2)
key('A1_full_charpoly_radial_decouples', sp.simplify(sp.expand(cp - target)) == 0)

# A2: discriminant identities -- the real-spectrum window structure.
Tm = 1/rho**2 + s**2 - m2
discm = Tm**2 - 4*d2
u_ = s**2 - m2 - 1/rho**2
key('A2a_disc_u_identity', sp.simplify(sp.expand(discm - (u_**2 - 4*m2/rho**2))) == 0)
disc_mu = T2**2 - 4*d2
key('A2b_disc_window_factorization',
    sp.simplify(sp.expand(disc_mu - ((1/rho - s)**2 - mu**2)*((1/rho + s)**2 - mu**2))) == 0)

# A4: mu=0 roots of the clock-screen block are exactly {1/rho^2, s^2} (D1 static pair).
p0 = lam**2 - Tm.subs(m2, 0)*lam + d2
key('A4a_static_root_reciprocal', sp.simplify(p0.subs(lam, 1/rho**2)) == 0)
key('A4b_static_root_screen', sp.simplify(p0.subs(lam, s**2)) == 0)

# A5: exact mu-monotonicity. lam_min/max = (T -/+ sqrt(disc))/2; d lam/d(mu^2) identities.
lam_min = (Tm - sp.sqrt(discm))/2
lam_max = (Tm + sp.sqrt(discm))/2
dlam_min = sp.diff(lam_min, m2)
key('A5a_dlam_implicit_identity', sp.simplify(dlam_min - lam_min/(Tm - 2*lam_min)) == 0)
key('A5b_dlam_min_over_sqrtdisc', sp.simplify(dlam_min - lam_min/sp.sqrt(discm)) == 0)
dlam_max = sp.diff(lam_max, m2)
key('A5c_dlam_max_negative_form', sp.simplify(dlam_max + lam_max/sp.sqrt(discm)) == 0)
# => on the real window sqrt(disc) > 0: lam_min strictly INCREASES in mu^2, lam_max strictly
#    DECREASES; product lam_min*lam_max = d = s^2/rho^2 (mu-independent):
key('A5d_product_tie', sp.simplify(sp.expand(lam_min*lam_max - d2)) == 0)

# A6: perturbative coefficient at mu=0 on the s>1/rho window (branch continuous to 1/rho^2).
# DECIDABLE RESTATEMENT (D1-precedent; same claim): sympy cannot auto-resolve sqrt(disc)|_{m2=0}
# = sqrt(u^2) in the raw radical, so the perfect square is FACTORED first (exact) and the
# positive root extracted under the declared s = 1/rho + w > 1/rho window; then A5b gives
# d lam_min/d m2 |_0 = lam_min0/sqrt_disc0, evaluated exactly.
sub0 = lambda e: e.subs(m2, 0).subs(s, 1/rho + w)
sqrt_disc0 = sp.sqrt(sp.factor(sub0(discm)))       # -> w*(rho*w + 2)/rho, positive symbols
lam_min0 = sp.simplify((sub0(Tm) - sqrt_disc0)/2)  # -> 1/rho^2 (checked as F1a below)
key('A6_dlam_at_mu0_equals_inv_rho2s2_minus_1',
    sp.simplify(lam_min0/sqrt_disc0 - sub0(1/(rho**2*s**2 - 1))) == 0)

# A7: window-edge trace identity T(mu_c) = 2s/rho (positivity of T on the near window).
key('A7_Tm_edge_identity', sp.simplify((1/rho**2 + s**2 - (1/rho - s)**2) - 2*s/rho) == 0)

# A8: at the elliptic threshold m2 = (s-1/rho)^2 the colliding eigenvalue is s/rho exactly.
key('A8_threshold_lambda_is_s_over_rho',
    sp.simplify((Tm/2).subs(m2, (s - 1/rho)**2) - s/rho) == 0)

# A9: causal labeling. Eigenvector of the block for eigenvalue lam is v = (mu/rho, lam - 1/rho^2).
# (a) the on-shell relation (lam - 1/rho^2)(s^2 - m2 - lam) = m2/rho^2 is the charpoly itself:
rel = (lam - 1/rho**2)*(s**2 - m2 - lam) - m2/rho**2
key('A9a_eigvec_onshell_relation', sp.simplify(sp.expand(rel + (lam**2 - Tm*lam + d2))) == 0)
# (b) the eta-timelike condition for the min branch factorizes to |mu| < s - 1/rho exactly:
key('A9b_labeling_window_factorization',
    sp.simplify(sp.expand((s**2 - mu**2 - 1/rho**2 - 2*mu/rho)
                          - (s - mu - 1/rho)*(s + mu + 1/rho))) == 0)
# (c) partner identity: s^2 - m2 - lam_min = lam_max - 1/rho^2 (used in the labeling chain):
key('A9c_partner_identity', sp.simplify((s**2 - m2 - lam_min) - (lam_max - 1/rho**2)) == 0)

# A10: AT the threshold the labeled eigenline goes eta-NULL (labeling degenerates exactly there).
v0 = (s - 1/rho)/rho          # mu/rho at mu = s - 1/rho
v2 = s/rho - 1/rho**2         # lam - 1/rho^2 at lam = s/rho
key('A10_threshold_eigline_null', sp.simplify(-v0**2 + v2**2) == 0)

# ============ BLOCK B: the direction-dependent channel -- statistics transfer ============
# Redshift dictionary at mu != 0 (P-D2-5): 1+z = lam_t^{-1/2}, lam_t = causally-labeled branch.
onez = lam_min**sp.Rational(-1, 2)

# B1: pointwise per-direction map, linear coefficient in m2 = mu^2:
#     ln(1+z) = ln rho - K(rho,s)*mu^2 + O(mu^4),  K = rho^2 / (2 (rho^2 s^2 - 1)).
K_coef = rho**2 / (2*(rho**2*s**2 - 1))
# DECIDABLE RESTATEMENT (same claim): d ln lam_min/d m2 |_0 assembled from the A5b/A6 resolved
# forms (lam_min0, sqrt_disc0) instead of the raw radical sympy cannot decide.
dlnz0 = sp.simplify(-sp.Rational(1, 2)*(lam_min0/sqrt_disc0)/lam_min0)
key('B1_lnz_linear_coeff_is_minus_K', sp.simplify(dlnz0 + sub0(K_coef)) == 0)

# B2: depth law of the transfer coefficient K (T2' content): strictly monotone, saturating.
key('B2a_dK_drho_negative_closed_form',
    sp.simplify(sp.diff(K_coef, rho) + rho/((rho**2*s**2 - 1)**2)) == 0)
key('B2b_K_deep_limit_1_over_2s2', sp.simplify(sp.limit(K_coef, rho, sp.oo) - 1/(2*s**2)) == 0)

# B3: quadratic pointwise map of a featureless field: (M th^-g)^2 has CONSTANT log-slope -2g.
g, Mmu = sp.symbols('g_mu M_mu', positive=True)
def logslope(expr):
    return sp.simplify(th*sp.diff(expr, th)/expr)
Cmu = Mmu*th**(-g)
key('B3_squared_powerlaw_slope_constant', sp.simplify(logslope(2*Cmu**2) + 2*g) == 0)

# B4: the coboundary channel (lane-forced form mu = a k(q) - s k(p), a = 1/rho): exact
# Gaussian 2-pt transfer. Cov(mu1^2, mu2^2) = 2 a^4 c^2 + 4 a^2 s^2 k_p^2 c (unit-variance k).
from sympy.stats import Normal, E
c_ = sp.Symbol('c')                       # normalized angular correlation of k, |c|<1
kp = sp.Symbol('k_p', positive=True)      # the observer's own k value (one number)
X = Normal('X', 0, 1); Y = Normal('Y', 0, 1)
k1 = X
k2 = c_*X + sp.sqrt(1 - c_**2)*Y
a_ = 1/rho
mu1 = a_*k1 - s*kp
mu2 = a_*k2 - s*kp
cov = sp.simplify(E(sp.expand(mu1**2 * mu2**2)) - E(sp.expand(mu1**2))*E(sp.expand(mu2**2)))
key('B4_coboundary_cov_two_power_structure',
    sp.simplify(cov - (2*a_**4*c_**2 + 4*a_**2*s**2*kp**2*c_)) == 0)

# B5: THE FEATURELESS-SUM LEMMA (3-term machine witness of the n-term variance identity):
# any positive-coefficient sum of power laws has log-slope = -E_w[g] with
# d(logslope)/d(ln th) = +Var_w[g] >= 0: STRICTLY MONOTONE slope -- no interior slope
# extremum, i.e. no LOCALIZED feature; crossovers are amplitude-set.
K1, K2, K3, g1, g2, g3 = sp.symbols('K1 K2 K3 g1 g2 g3', positive=True)
u1, u2, u3 = K1*th**(-g1), K2*th**(-g2), K3*th**(-g3)
wsum = u1 + u2 + u3
L = th*sp.diff(wsum, th)/wsum
dL = sp.simplify(th*sp.diff(L, th))
varnum = (g1**2*u1 + g2**2*u2 + g3**2*u3)*(u1 + u2 + u3) - (g1*u1 + g2*u2 + g3*u3)**2
key('B5_slope_derivative_is_weight_variance',
    sp.simplify(sp.expand(dL*(u1 + u2 + u3)**2 - varnum)) == 0)

# B6 (AMENDED per R1-A1): the crossover is amplitude-SET but map-STEERED. Generic layer:
# theta_x = (K2/K1)^{1/(g2-g1)} solves equality of the two terms [B6a, DECIDABLE
# RESTATEMENT in LOG form (positive symbols; expand_log exact) -- sympy cannot cancel the
# symbolic exponent ratio (g2-g1)/(g2-g1) in the raw power form; same claim].
theta_x = (K2/K1)**(1/(g2 - g1))
log_thx = sp.log(K2/K1)/(g2 - g1)
key('B6a_crossover_solves',
    sp.simplify(sp.expand_log(sp.log(K1) - g1*log_thx - (sp.log(K2) - g2*log_thx),
                              force=True)) == 0)
# CHANNEL layer (coboundary coefficients from KEY B4: K_lin = 4 a^2 s^2 k_p^2 M,
# K_quad = 2 a^4 M^2, indices g and 2g): theta_x^g = M a^2/(2 s^2 k_p^2), a = 1/rho --
# the crossover CARRIES DEPTH (drifts as (1+z)^{-2/g}) and the screen ratio s:
# D1-window-break class (input-set location, MAP-STEERED drift). The earlier generic-layer
# free-symbol key was VACUOUS as machine evidence (R1 catch) -- replaced by these two:
Mamp = sp.Symbol('M_amp', positive=True)
Xc = sp.Symbol('X_c', positive=True)       # X_c = C_k(theta) value at the crossover
theta_xg = Mamp*a_**2/(2*s**2*kp**2)       # = theta_x**g at the channel layer
key('B6b_channel_crossover_solves',
    sp.simplify((4*a_**2*s**2*kp**2*Xc - 2*a_**4*Xc**2).subs(Xc, 2*s**2*kp**2/a_**2)) == 0
    and sp.simplify(Mamp/theta_xg - 2*s**2*kp**2/a_**2) == 0)
key('B6c_channel_crossover_carries_depth_and_screen',
    (rho in theta_xg.free_symbols) and (s in theta_xg.free_symbols))

# B7: chain/composition (SS7): the lane composition law re-verified -- mixing ACCUMULATES
# LINEARLY (a1 m2 + m1 s2) with smooth weights; composition acts inside the Lorentzian block,
# no operator on the sky coordinate appears.
a1, a2, s1, s2v, mm1, mm2 = sp.symbols('a1 a2 s1 s2v mm1 mm2', positive=True)
def Arr(av, sv, mv):
    return sp.Matrix([[av, 0, mv], [0, 1/av, 0], [0, 0, sv]])
comp = Arr(a1, s1, mm1)*Arr(a2, s2v, mm2)
diffm = (comp - Arr(a1*a2, s1*s2v, a1*mm2 + mm1*s2v)).applyfunc(sp.simplify)
key('B7_composition_law_linear_mixing_accumulation', diffm == sp.zeros(3, 3))

# ============ BLOCK C: metric realization -- rays under the mixing cross term ============
# Stationary slice SS3: ds^2 = -A dt^2 + dr^2/A + S dpsi^2 + 2 h dt dpsi (equatorial, S = g_psipsi),
# linear order in h. (r,(t,psi)) block-diagonal => g^rr = A exactly.
r_ = sp.Symbol('r', positive=True)
Ef = sp.Symbol('E', positive=True)
h = sp.Symbol('h')
Af = sp.Symbol('A_f', positive=True)     # A(r) at the field point (generic positive)
Sf = sp.Symbol('S_f', positive=True)     # g_psipsi at the field point
gblock = sp.Matrix([[-Af, h], [h, Sf]])
ginv = gblock.inv()
gtt, gtpsi = ginv[0, 0], ginv[0, 1]

# G1: coframe realization of the clock->screen mix reproduces g_tpsi = h exactly; the g_tt
# deviation is O(h^2) -- the metric-level redshift shift is O(h^2), coherent with lam_t = O(mu^2).
dt_, dpsi_ = sp.symbols('dt dpsi')
e0 = sp.sqrt(Af)*dt_
e2 = sp.sqrt(Sf)*dpsi_ + (h/sp.sqrt(Sf))*dt_
quad = sp.expand(-e0**2 + e2**2)
key('G1a_coframe_cross_term_is_h', sp.simplify(quad.coeff(dt_).coeff(dpsi_) - 2*h) == 0)
key('G1b_gtt_deviation_O_h2', sp.simplify(quad.coeff(dt_, 2) - (-Af + h**2/Sf)) == 0)

# C: arriving ray with p_psi = 0: p^psi = g^{psi t} p_t drags the sky position.
p_t = -Ef
p_r = -Ef*sp.sqrt(Sf/(Af*(Af*Sf + h**2)))     # ingoing root of the null condition
key('C3_null_condition_consistency', sp.simplify(gtt*p_t**2 + Af*p_r**2) == 0)
p_psi_up = gtpsi*p_t
p_r_up = Af*p_r
dpsi_dr = sp.simplify(p_psi_up/p_r_up)
dpsi_dr_lin = sp.series(dpsi_dr, h, 0, 2).removeO()
key('C1_drift_rate_linear_in_h', sp.simplify(dpsi_dr_lin - h/(Af*Sf)) == 0)
key('C2_static_recovery_no_drift', sp.simplify(dpsi_dr.subs(h, 0)) == 0)

# E2: achromatic -- the drift rate carries NO frequency symbol (E cancels exactly).
key('E2_achromatic_drift_E_free', Ef not in sp.simplify(dpsi_dr).free_symbols)

# ============ BLOCK D: TIME LIVE -- the exact depth law and the fold condition ============
# Eikonal crest transport (SS: geometric optics, radial rays to O(h)): crest paths obey
# dt/dr = -1/A(t,r); the crest separation obeys d(dt)/dr = (A_t/A^2) dt.
tt = sp.Symbol('t')
Atr = sp.Function('A_fun', positive=True)
expr_ode = -1/Atr(tt, r_)
key('D1_crest_transport_coefficient',
    sp.simplify(sp.diff(expr_ode, tt) - sp.diff(Atr(tt, r_), tt)/Atr(tt, r_)**2) == 0)

# All sightlines to one observation event lie on ONE past cone t_c(r) => the LOS integral's
# r_s-derivative is the integrand at r_s. Assembling (chain rule along the cone, dt_c/dr = -1/A):
#   d ln(1+z)/dr_s = -(1/2)[A_r + A_t*(-1/A)]/A - A_t/A^2 = -(A_r + A_t/A)/(2A)   [EXACT]
Asym, At, Ar = sp.symbols('A_sym A_t A_r')
total = -Ar/(2*Asym) + At/(2*Asym**2) - At/Asym**2
key('D2_exact_timelive_depth_law', sp.simplify(total + (Ar + At/Asym)/(2*Asym)) == 0)
# chain-rule assembly of the -(1/2)ln A(t_c(r_s), r_s) piece, machine-checked:
rs_ = sp.Symbol('r_s', positive=True)
tcf = sp.Function('t_c')(rs_)
piece = -sp.Rational(1, 2)*sp.log(Atr(tcf, rs_))
dpiece = sp.diff(piece, rs_).subs(sp.Derivative(tcf, rs_), -1/Atr(tcf, rs_))
# DECIDABLE RESTATEMENT (same claim): the partials are built as the Subs objects sympy's own
# chain rule emits (the earlier draft compared against TOTAL Derivative objects -- a wrong
# construction, not a wrong claim).
xi_ = sp.Symbol('xi')
At_sub = sp.Subs(sp.diff(Atr(xi_, rs_), xi_), xi_, tcf)
Ar_sub = sp.Subs(sp.diff(Atr(tcf, xi_), xi_), xi_, rs_)
tgt_piece = -(Ar_sub - At_sub/Atr(tcf, rs_))/(2*Atr(tcf, rs_))
key('D3_conepoint_chain_rule', sp.simplify(dpiece - tgt_piece) == 0)

# D5: the FOLD (caustic) condition: d ln(1+z)/dr_s = 0 <=> A_t = -A*A_r exactly.
key('D5_fold_condition_At_eq_minus_A_Ar', sp.solve(sp.Eq(total, 0), At) == [-Asym*Ar])

# D4: the static gradient never vanishes on the class-(i) profile (0 < q < 1, n > 0):
# -A0'/(2A0) = n/(2 R_w q) > 0 strictly -- statically NO fold exists (D1 monotonicity);
# a fold REQUIRES time-variation rate comparable to the static gradient (outside SS4).
# RELABELED TRUE-BY-FORM (R1-S3 / R2-A-6): positivity decided by symbol declarations; the
# form n/(2 R_w q) is ASSERTED here (derived from A = q^n independently by R1's recompute);
# the substantive machine content rides D1 K17/K18 + KEYs F4a/F4b.
grad_static = n_/(2*Rw*q_)
key('D4_static_gradient_strictly_positive', bool(grad_static > 0))

# ============ BLOCK F: T6' STATIC-LIMIT RECOVERY (mandatory, machine-checked) ============
# F1: mu -> 0: lam_t -> 1/rho^2 and 1+z -> rho exactly (banked c_eff ratio reading).
# DECIDABLE RESTATEMENT (same claim): uses the A6-resolved perfect-square root sqrt_disc0.
key('F1a_lambda_static', sp.simplify(lam_min0 - 1/rho**2) == 0)
key('F1b_onez_static', sp.simplify(lam_min0**sp.Rational(-1, 2) - rho) == 0)

# F2: D1 G7 dictionary re-derived: r(z) = R_w(1 - (1+z)^{-2/n}) inverts A = (1-r/R_w)^n.
rz = Rw*(1 - (1 + z_)**(-2/n_))
Az = (1 - rz/Rw)**n_
key('F2_D1_G7_dictionary', sp.simplify(sp.powsimp(Az - (1 + z_)**(-2), force=True)) == 0)

# F3: D1 K4 re-derived: identity angular map => w_obs = K (r_s th)^{-gamma}, log-slope -gamma.
gam, Ksrc, rsh = sp.symbols('gamma K_src r_sh', positive=True)
key('F3_D1_K4_logslope', sp.simplify(logslope(Ksrc*(rsh*th)**(-gam)) + gam) == 0)

# F4: D1 K17/K18 re-derived: static depth law -A'/(2A); class-(i) J(z) = (n/2R_w)(1+z)^{2/n}.
key('F4a_static_depth_law', sp.simplify(total.subs(At, 0) + Ar/(2*Asym)) == 0)
zq = q_**(-n_/2) - 1                       # z at q = 1 - r/R_w
Jq = n_/(2*Rw*q_)                          # dz/dl_p computed on the class-(i) profile
key('F4b_D1_K18_J_recovery',
    sp.simplify(sp.powsimp(Jq - (n_/(2*Rw))*(1 + zq)**(2/n_), force=True)) == 0)

# F6: radial monotonicity WITH mixing at O(mu^2): the per-direction dictionary coefficient
# 1/rho - m2*dK/drho = 1/rho + m2*rho/(rho^2 s^2 - 1)^2 -- a sum of positives: monotonicity
# is PRESERVED (indeed strengthened) at this order.
key('F6_radial_monotone_coefficient_positive_sum',
    sp.simplify((1/rho - m2*sp.diff(K_coef, rho)) - (1/rho + m2*rho/((rho**2*s**2 - 1)**2))) == 0)

# ===== A-11 (R2): the WINDOW-BREAK re-check, TIME-LIVE (prereg deliverable (iv), derived) =====
# D1's break: theta_break = Delta_l_p(bin)/r(z), Delta_l_p = Delta_z/J. Time-live the
# dictionary rate generalizes via the EXACT depth law (KEY D2) and dl_p = dr/sqrt(A)
# (the SS9 chart ansatz): J_tl = dz/dl_p = (1+z) * [-(A_r + A_t/A)/(2A)] * sqrt(A) --
# a smooth composition of smooth dictionary elements, modulated per direction by the F6
# positive coefficient at O(mu^2). ANSWER: the live map does NOT move the break beyond the
# (now time-live) smooth dictionary drift + a smooth per-direction modulation -- EXCEPT at
# the fold onset, where J_tl -> 0 and theta_break DIVERGES (the R1-A3 interaction, named;
# there the no-feature guarantee is already void).
onez_s = sp.Symbol('onez_s', positive=True)   # (1+z) at emission, time-live value
J_tl = onez_s * (-(Ar + At/Asym)/(2*Asym)) * sp.sqrt(Asym)
key('A11a_Jtl_static_matches_D1_K17',
    sp.simplify(J_tl.subs(At, 0).subs(onez_s, Asym**sp.Rational(-1, 2)) + Ar/(2*Asym)) == 0)
key('A11b_Jtl_zero_at_fold', sp.simplify(J_tl.subs(At, -Asym*Ar)) == 0)
Dz = sp.Symbol('Delta_z_bin', positive=True)
r_area = sp.Symbol('r_area', positive=True)
theta_break_tl = Dz/(J_tl*r_area)
key('A11c_thetabreak_no_angular_symbol', th not in theta_break_tl.free_symbols)

# E1: operator symbol audit (D1 K14 analog, time-live): the map expressions carry only
# geometry/comparison symbols -- no source-property symbol exists in the operator.
# WEIGHT DOWNGRADED (R1-S3): vacuous-by-construction as MACHINE evidence (tests absence of
# symbols never introduced); the claim stands by inspection of the audited expression list.
source_props = set(sp.symbols('b_tracer M_source L_source f_emit'))
map_syms = set()
for e in (lam_min, onez, K_coef, dpsi_dr, total, grad_static, rz, J_tl):
    map_syms |= e.free_symbols
key('E1_operator_free_of_source_symbols', map_syms.isdisjoint(source_props))

# F-RETRO machine discharge: no float atom enters any audited expression.
audit = [C, cp, lam_min, lam_max, onez, K_coef, cov, dpsi_dr, total, rz, Az, Jq, theta_x,
         theta_xg, J_tl, theta_break_tl, comp]
def has_float(e):
    return any(isinstance(a, sp.Float) for a in sp.preorder_traversal(e))
key('K_FRETRO_no_float_atoms_in_derivation', not any(has_float(e) for e in audit))

# ---------------- summary ----------------
npass = sum(1 for _, ok in RESULTS if ok)
print(f"\nCHECKS PASSED: {npass} / {len(RESULTS)}")
for nm, ok in RESULTS:
    if not ok:
        print(f"  FAILED: {nm}")
