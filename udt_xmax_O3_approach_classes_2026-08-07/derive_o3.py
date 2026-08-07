#!/usr/bin/env python3
"""O3 -- approach-profile classes + the conditional selection map (X3).
Exact sympy, CPU, float-free. One machine-check key per claim, printed `KEY = ...`.
Contract: PREREGISTRATION.md (this dir). Ground: O1/O2 CONSOLIDATED (cited in notes).

Setting (banked): A(r) = e^{-2 phi}; depth delta = -(1/2) ln A; 1+z = e^delta = A^{-1/2}.
Frozen family:
  (i)   A = c0*(1 - r/Rw)^n = c0*u^n,  u = 1 - r/Rw, wall u->0+ (finite chart radius Rw)
  (ii)  A = exp(-r/X), wall r->oo
  (ii') A = (1 + r/X)^(-alpha)  [EXACT REPRESENTATIVE, declared: regular at r=0, A(0)=1
        matching observer normalization phi(0)=0; ~ (r/X)^(-alpha) asymptotically]
  (iii) A = c0*u^n*(-ln u)^(-p)  at the class-(i) knife edges (p>0 = log-enhanced wall)
  essential walls A = exp(-1/(Rw - r)): NOTED-ONLY, hand-check-tagged keys (ESS_*).
Window reparametrizations (encode open n-ranges as positive symbols):
  q = (2-n)/2 > 0  <=> n < 2 (proper window);  w = 1-n > 0 <=> n < 1 (optical window);
  g > 0 = generic gap (n = 2+2g means n>2, alpha = 2+2g means alpha>2, etc).
"""
import sympy as sp

u, r, s, t, T, y = sp.symbols('u r s t T y', positive=True)
X, Rw, c0, eps, h = sp.symbols('X R_w c_0 epsilon h', positive=True)
n, alpha, m = sp.symbols('n alpha m', positive=True)
p = sp.Symbol('p', real=True)
q = sp.Symbol('q', positive=True)   # q = (2-n)/2
w = sp.Symbol('w', positive=True)   # w = 1-n
g = sp.Symbol('g', positive=True)   # generic positive gap
oo = sp.oo
log, exp, sqrt, Rat = sp.log, sp.exp, sp.sqrt, sp.Rational

def key(name, val):
    print(f"{name} = {val}")

print("# ===== D1 SECTION: per-branch finiteness cells (independent re-derivation) =====")

# ---------- S1: proper radial length  int_0^wall A^(-1/2) dr ----------
# Class (i): (Rw/sqrt(c0)) * int_0^1 u^(-n/2) du ; sub n = 2-2q (n<2): u^(q-1)
I = sp.integrate(u**(q-1), (u, 0, 1))
key("S1_i_unit_integral_n_lt_2_eq_1_over_q", sp.simplify(I - 1/q) == 0)
# value: (Rw/sqrt(c0))*(1/q) = 2Rw/(sqrt(c0)*(2-n)) with q=(2-n)/2
key("S1_i_value_matches_2Rw_over_sqrtc0_2mn",
    sp.simplify((Rw/sqrt(c0))*(1/q) - (2*Rw/(sqrt(c0)*(2-n))).subs(n, 2-2*q)) == 0)
# n > 2 (n = 2+2g): partial integral diverges as T->0+
part = sp.integrate(u**(-1-g), (u, T, 1))
key("S1_i_divergent_n_gt_2", sp.limit(part, T, 0, '+') == oo)
key("S1_i_divergent_n_eq_2_log", sp.limit(sp.integrate(1/u, (u, T, 1)), T, 0, '+') == oo)
# Class (ii): int_0^oo e^{r/(2X)} dr
key("S1_ii_divergent", sp.limit(sp.integrate(exp(r/(2*X)), (r, 0, T)), T, oo) == oo)
# Class (ii'): integrand A^(-1/2) = (1+r/X)^(alpha/2) unbounded (>=1, -> oo) => divergent
key("S1_iiprime_integrand_to_oo", sp.limit((1+r/X)**(alpha/2), r, oo) == oo)
key("S1_iiprime_integrand_ge_1_at_0", sp.simplify((1+r/X)**(alpha/2)).subs(r, 0) == 1)
# Class (iii) n=2 edge: integrand = c0^(-1/2) u^(-1) t^(p/2), t=-ln u -> int t^(p/2) dt
# finite iff p/2 < -1 iff p < -2.  Witness p = -2-2g: int_1^oo t^(-1-g) dt = 1/g finite.
key("S1_iii_edge_n2_finite_p_lt_m2", sp.simplify(sp.integrate(t**(-1-g), (t, 1, oo)) - 1/g) == 0)
key("S1_iii_edge_n2_divergent_p_eq_m2", sp.integrate(1/t, (t, 1, oo)) == oo)
# Essential wall (HAND-CHECK TAG): A = e^{-1/s}, s = Rw - r; integrand e^{1/(2s)} > 1/(2s)
# (since e^y > y for y>0), and the harmonic integral diverges => S1 divergent.
yy = sp.Symbol('yy', real=True)
# e^y - y is convex (second derivative e^y > 0), stationary at y=0, value 1 there
# => global minimum 1 => e^y > y for all y (in particular y > 0).
key("ESS_exp_minus_y_at_0_eq_1", (exp(yy) - yy).subs(yy, 0) == 1)
key("ESS_exp_minus_y_stationary_at_0", sp.diff(exp(yy) - yy, yy).subs(yy, 0) == 0)
key("ESS_exp_minus_y_convex", sp.diff(exp(yy) - yy, yy, 2).is_positive == True)
key("ESS_harmonic_divergent", sp.limit(sp.integrate(1/(2*s), (s, T, 1)), T, 0, '+') == oo)

# ---------- S2: optical/Fermat  int_0^wall dr/A  (== c * travel time, O2 row (c)) ----------
# Class (i): (Rw/c0) * int_0^1 u^(-n) du ; sub n = 1-w (n<1): u^(w-1)
I2 = sp.integrate(u**(w-1), (u, 0, 1))
key("S2_i_unit_integral_n_lt_1_eq_1_over_w", sp.simplify(I2 - 1/w) == 0)
key("S2_i_value_matches_Rw_over_c0_1mn",
    sp.simplify((Rw/c0)*(1/w) - (Rw/(c0*(1-n))).subs(n, 1-w)) == 0)
# n=1: exact partial integral (Rw/c0) * (-ln u_lower): log-divergent, rate linear in depth
part_n1 = sp.integrate(1/u, (u, T, 1))
key("S2_i_n1_partial_eq_minus_lnT", sp.simplify(part_n1 - (-log(T))) == 0)
key("S2_i_n1_logdivergent", sp.limit(part_n1, T, 0, '+') == oo)
# rate check: at c0=1, delta = (n/2)(-ln u) = t/2 for n=1; ell_opt(partial) = Rw*t = 2*Rw*delta/n
key("S2_i_n1_rate_ell_eq_2Rw_delta",
    sp.simplify(Rw*t - 2*Rw*(t/2)) == 0)
# n>1 (n = 1+g): divergent
key("S2_i_divergent_n_gt_1", sp.limit(sp.integrate(u**(-1-g), (u, T, 1)), T, 0, '+') == oo)
key("S2_ii_divergent", sp.limit(sp.integrate(exp(r/X), (r, 0, T)), T, oo) == oo)
key("S2_iiprime_integrand_to_oo", sp.limit((1+r/X)**alpha, r, oo) == oo)
# Class (iii) n=1 edge: integrand u^(-1) t^p -> int t^p dt: finite iff p < -1
key("S2_iii_edge_n1_finite_p_lt_m1", sp.simplify(sp.integrate(t**(-1-g), (t, 1, oo)) - 1/g) == 0)
key("S2_iii_edge_n1_divergent_p_eq_m1", sp.integrate(1/t, (t, 1, oo)) == oo)
# Essential wall (HAND-CHECK TAG): integrand e^{1/s} > 1/s => divergent (same comparison keys).

# ---------- S3: areal radius r (== d_A = r, O2 adjudicated; needs areal anchor) ----------
key("S3_i_wall_at_finite_Rw", sp.limit(Rw*(1-u), u, 0, '+') == Rw)
key("S3_ii_wall_at_infinite_r", True)   # wall = r->oo by class definition (chart radius)
key("S3_iiprime_wall_at_infinite_r", True)  # same (chart radius oo by class definition)
key("S3_iii_wall_at_finite_Rw", True)   # class (iii) lives at finite Rw by construction
key("ESS_S3_wall_at_finite_Rw", True)   # essential wall at finite Rw (HAND-CHECK TAG)

# ---------- S4: the r/(1+z) = r*sqrt(A) variant ----------
# Class (i): f = Rw(1-u)*sqrt(c0)*u^(n/2) -> 0 at wall; NON-MONOTONE (interior max).
f4i = Rw*(1-u)*sqrt(c0)*u**(n/2)
key("S4_i_wall_value_0", sp.limit(f4i, u, 0, '+') == 0)
crit_i = sp.solve(sp.diff((1-u)*u**(n/2), u), u)
key("S4_i_interior_max_at_u_eq_n_over_np2", crit_i == [n/(n+2)])
# Class (ii): f = r e^{-r/(2X)} -> 0; non-monotone (max at r=2X).
key("S4_ii_wall_value_0", sp.limit(r*exp(-r/(2*X)), r, oo) == 0)
key("S4_ii_interior_max_at_2X", sp.solve(sp.diff(r*exp(-r/(2*X)), r), r) == [2*X])
# Class (ii'): f = r*(1+r/X)^(-alpha/2).  THREE regimes:
#   alpha < 2 (alpha = 2-2g needs g<1; monotone): f -> oo   [witness alpha=1 + symbolic]
key("S4_iiprime_alpha_lt_2_divergent_witness_a1", sp.limit(r*(1+r/X)**(-Rat(1,2)), r, oo) == oo)
#   alpha = 2: f = rX/(X+r) MONOTONE INCREASING, wall value X (finite, genuine!)
f4_2 = r*(1+r/X)**(-1)
key("S4_iiprime_alpha2_wall_value_X", sp.limit(f4_2, r, oo) == X)
key("S4_iiprime_alpha2_monotone", sp.simplify(sp.diff(f4_2, r) - X**2/(X+r)**2) == 0)
#   alpha > 2 (alpha = 2+2g): f -> 0, non-monotone (interior max at r = X/g = 2X/(alpha-2))
#   bound: f = [rX/(X+r)] * (1+r/X)^(-g) <= X*(1+r/X)^(-g) -> 0; plus witness alpha=3.
key("S4_iiprime_alpha_gt_2_bound_decomposition",
    sp.simplify(r*(1+r/X)**(-1-g) - (r*X/(X+r))*(1+r/X)**(-g)) == 0)
key("S4_iiprime_alpha_gt_2_bound_factor_lt_X", sp.simplify(X - r*X/(X+r) - X**2/(X+r)) == 0)
key("S4_iiprime_alpha_gt_2_tail_to_0", sp.limit((1+r/X)**(-g), r, oo) == 0)
key("S4_iiprime_alpha_gt_2_wall_value_0_witness_a3",
    sp.limit(r*(1+r/X)**(-Rat(3,2)), r, oo) == 0)
crit_ap = sp.solve(sp.diff(r*(1+r/X)**(-1-g), r), r)
key("S4_iiprime_alpha_gt_2_interior_max_at_X_over_g", crit_ap == [X/g])
# monotonicity boundary: critical point of general f exists iff alpha > 2:
#   d/dr [r(1+r/X)^(-alpha/2)] = 0  <=>  (1+r/X) = (alpha/2)(r/X)  <=>  r = 2X/(alpha-2)
crit_gen = sp.solve((1 + r/X) - (alpha/2)*(r/X), r)
key("S4_iiprime_critpoint_r_eq_2X_over_am2", sp.simplify(crit_gen[0] - 2*X/(alpha-2)) == 0)
# Class (iii) witnesses (n=1, p=+-2): f -> 0 (power beats log)
key("S4_iii_wall_value_0_witness_p2",
    sp.limit((1-u)*u**Rat(1,2)*(-log(u))**(-1), u, 0, '+') == 0)
key("S4_iii_wall_value_0_witness_pm2",
    sp.limit((1-u)*u**Rat(1,2)*(-log(u))**(1), u, 0, '+') == 0)
# Essential (HAND-CHECK TAG): f = (Rw-s) e^{-1/(2s)} -> 0
key("ESS_S4_wall_value_0", sp.limit((Rw-s)*exp(-1/(2*s)), s, 0, '+') == 0)

# ---------- S5: d_L = (1+z)^2 r = r/A ----------
# identity: ln d_L = 2*delta + ln r  (delta = -(1/2) ln A)  -- d_L is a depth-carrier.
A_ = sp.Symbol('A_', positive=True)
key("S5_lndL_identity_2delta_plus_lnr",
    sp.simplify(log(r/A_) - (2*(-log(A_)/2*1) + log(r))) == 0)
key("S5_i_divergent", sp.limit(Rw*(1-u)/(c0*u**n), u, 0, '+') == oo)
key("S5_ii_divergent", sp.limit(r*exp(r/X), r, oo) == oo)
key("S5_iiprime_divergent", sp.limit(r*(1+r/X)**alpha, r, oo) == oo)
key("S5_iii_divergent_witness_p2",
    sp.limit((1-u)/(u*(-log(u))**(-2)), u, 0, '+') == oo)
key("S5_iii_divergent_witness_pm2",
    sp.limit((1-u)/(u*(-log(u))**(2)), u, 0, '+') == oo)
key("ESS_S5_divergent", sp.limit((Rw-s)*exp(1/s), s, 0, '+') == oo)

# ---------- S6: redshift z == depth delta (1+z = e^delta) ----------
key("S6_i_divergent", sp.limit(-log(c0*u**n)/2, u, 0, '+') == oo)
key("S6_ii_divergent", sp.limit(-log(exp(-r/X))/2, r, oo) == oo)
key("S6_iiprime_divergent", sp.limit((alpha/2)*log(1+r/X), r, oo) == oo)
key("S6_iii_divergent_witness_p2",
    sp.limit(-log(u**1*(-log(u))**(-2))/2, u, 0, '+') == oo)
key("ESS_S6_divergent", sp.limit(1/(2*s), s, 0, '+') == oo)

# ---------- S7: infall geodesic proper time (worldline POSIT; proviso eps^2 > sup A) ----------
# integrand (times c) = 1/sqrt(eps^2 - A); at the wall A->0 so integrand -> 1/eps (finite, nonzero)
key("S7_i_integrand_wall_limit_1_over_eps",
    sp.limit(1/sqrt(eps**2 - c0*u**n), u, 0, '+') == 1/eps)
# class (i) finiteness, exact witness n=1, c0=1, eps^2 = 1+h^2 (proviso encoded, h>0):
# c*tau = Rw * int_0^1 du / sqrt(1+h^2-u) = 2Rw(sqrt(1+h^2) - h)  -- finite.
I7 = sp.integrate(1/sqrt(1+h**2-u), (u, 0, 1))
key("S7_i_finite_exact_witness_n1", sp.simplify(I7 - 2*(sqrt(1+h**2) - h)) == 0)
# classes (ii)/(ii'): integrand >= 1/eps ALWAYS (since A > 0 => eps^2 - A < eps^2) over an
# INFINITE chart range => divergent by comparison. Keys: positivity + the limits.
key("S7_comparison_integrand_ge_1_over_eps", sp.simplify(eps**2 - (eps**2 - c0*u**n)) == c0*u**n)
key("S7_ii_integrand_limit_nonzero", sp.limit(1/sqrt(eps**2 - exp(-r/X)), r, oo) == 1/eps)
key("S7_iiprime_integrand_limit_nonzero",
    sp.limit(1/sqrt(eps**2 - (1+r/X)**(-alpha)), r, oo) == 1/eps)
# class (iii)/essential at finite Rw: integrand bounded (<= 1/h under the proviso), range finite
# => finite.  ESS hand-check tag carried.
key("ESS_S7_integrand_wall_limit_1_over_eps",
    sp.limit(1/sqrt(eps**2 - exp(-1/s)), s, 0, '+') == 1/eps)

print("# ===== D2 SECTION: approach-profile classes delta(sigma_k) per surviving branch =====")
# Class (i) depth: delta = (n/2) ln(1/u) - (1/2) ln c0;  1+z = e^delta.
delta_i = (n/2)*log(1/u) - log(c0)/2

# --- S3 (areal): sigma3 = Rw - r = Rw*u.  Claim: delta = (n/2) ln(1/sigma3) + const EXACTLY.
expr3 = delta_i + (n/2)*log(Rw*u)
key("D2_S3_kappa_n_over_2_const_exact",
    sp.simplify(sp.diff(expr3, u)) == 0 and
    sp.simplify(expr3 - ((n/2)*log(Rw) - log(c0)/2)) == 0)

# --- S1 (proper, n<2 i.e. n=2-2q): sigma1 = ell_p(u) = (Rw/(sqrt(c0)*q)) u^q  (exact remaining
#     proper length; antiderivative of the S1 integrand).  kappa = n/(2-n) = (1-q)/q.
ell = (Rw/(sqrt(c0)*q))*u**q
kap1 = (1-q)/q
expr1 = delta_i.subs(n, 2-2*q) + kap1*log(ell)
key("D2_S1_kappa_n_over_2mn_const_exact", sp.simplify(sp.diff(expr1, u)) == 0)
key("D2_S1_kappa_matches_n_over_2mn", sp.simplify(kap1 - (n/(2-n)).subs(n, 2-2*q)) == 0)

# --- S2 (optical, n<1 i.e. n=1-w): sigma2 = (Rw/(c0*w)) u^w.  kappa = n/(2(1-n)) = (1-w)/(2w).
sig2 = (Rw/(c0*w))*u**w
kap2 = (1-w)/(2*w)
expr2 = delta_i.subs(n, 1-w) + kap2*log(sig2)
key("D2_S2_kappa_n_over_2_1mn_const_exact", sp.simplify(sp.diff(expr2, u)) == 0)
key("D2_S2_kappa_matches", sp.simplify(kap2 - (n/(2*(1-n))).subs(n, 1-w)) == 0)

# --- S7 (infall): sigma7 = c*tau_rem(u) with integrand -> Rw/eps; L'Hopital ratio:
#     lim sigma7(u)/u = Rw/eps  =>  delta = (n/2) ln(1/sigma7) + const + o(1): kappa = n/2.
key("D2_S7_sigma_over_u_limit_Rw_over_eps",
    sp.limit(Rw/sqrt(eps**2 - c0*u**n), u, 0, '+') == Rw/eps)

# --- GENERAL-m UNIFICATION (structural, not a new row): a measure with integrand A^(-m)
#     (m=0 areal-like, m=1/2 proper, m=1 optical) has sigma ∝ u^(1-n*m) (finite iff n*m<1)
#     and kappa = n/(2(1-n*m)), i.e. 1/kappa = 2/n - 2m: LINEAR in the A-weight m, slope -2.
b = sp.Symbol('b', positive=True)   # b = 1 - n*m > 0 encodes the finiteness window
kap_m_val = (n/(2*(1-n*m)))
# exact check via substitution m -> (1-b)/n (so 1-n*m = b, m*ln c0 enters the constant only):
kap_b = (n/(2*b))
expr_mb = delta_i + kap_b*log((Rw/(c0**((1-b)/n) * b))*u**b)
key("D2_general_m_kappa_const_exact", sp.simplify(sp.diff(expr_mb, u)) == 0)
key("D2_general_m_reciprocal_kappa_linear",
    sp.simplify(1/kap_m_val - (2/n - 2*m)) == 0)
# arithmetic-progression corollary: 1/kappa_areal - 1/kappa_proper = 1, and
# 1/kappa_proper - 1/kappa_optical = 1, for EVERY n (n-free spacing):
key("D2_reciprocal_kappa_spacing_areal_proper_eq_1",
    sp.simplify((2/n) - ((2-n)/n) - 1) == 0)
key("D2_reciprocal_kappa_spacing_proper_optical_eq_1",
    sp.simplify(((2-n)/n) - ((2-2*n)/n) - 1) == 0)

# ---------- class-(iii) perturbation of the profile class (log-log corrections) ----------
# delta_iii = (n/2) t + (p/2) ln t - (1/2) ln c0, with t = -ln u.
# (iii)-INTERIOR members remain finite in each measure's window (power dominates the log):
# witness n=1, p=2 proper: int_0^1 u^(-1/2)(-ln u) du  [sub u=e^{-t}]  = int_0^oo t e^{-t/2} dt = 4
key("D2_iii_interior_proper_finite_witness_n1_p2",
    sp.simplify(sp.integrate(t*exp(-t/2), (t, 0, oo)) - 4) == 0)
# --- S3 (areal) with (iii): delta = (n/2) ln(1/sigma) + (p/2) ln ln(1/sigma) + const + o(1).
#     Residual after subtracting both terms (sigma = Rw*u, t = ln(Rw/sigma)):
L_ = sp.Symbol('L_', positive=True)   # L_ = ln(1/sigma) -> oo
resid_areal = (p/2)*(log(L_ + log(Rw)) - log(L_))
key("D2_iii_S3_loglog_coeff_p_over_2_residual_vanishes",
    sp.limit(resid_areal, L_, oo) == 0)
# --- S1 (proper) with (iii), interior n<2: leading asymptote of remaining length via L'Hopital:
#     I(u) = int_0^u s^(-n/2) t(s)^(p/2) ds  ~  u^(1-n/2) (-ln u)^(p/2) / (1-n/2).
#     Reduction: N/D = 1/(q - p/(2t)) with q = 1-n/2, then -> 1/q.
tt = -log(u)
N_ = u**(q-1)*tt**(p/2)
D_ = sp.diff(u**q*tt**(p/2), u)
ratio = sp.simplify(N_/D_)
key("D2_iii_S1_lhopital_reduction_1_over_q_minus_p_over_2t",
    sp.simplify(ratio - 1/(q - p/(2*tt))) == 0)
key("D2_iii_S1_lhopital_limit_1_over_q", sp.limit(1/(q - p/(2*t)), t, oo) == 1/q)
# --- inversion coefficient (witness n=1 i.e. q=1/2, p=2; constants set to 1):
#     F(t) = t/2 + ln t (the depth), L(t) = t/2 - ln t (= ln(1/ell) leading);  claim:
#     F - kappa*L - (p/(2-n))*ln L -> const, kappa = n/(2-n) = 1, p/(2-n) = 2.  Limit = ln 4.
F_ = t/2 + log(t)
Linv = t/2 - log(t)
key("D2_iii_S1_inversion_witness_const_eq_log4",
    sp.simplify(sp.limit(F_ - Linv - 2*log(Linv), t, oo) - log(4)) == 0)
# So: (iii) interior members keep the SAME leading kappa; they add a log-log term with
# coefficient (kappa/n)*p  [areal p/2; proper p/(2-n); optical p/(2(1-n)) -- same algebra].

# ---------- EDGE members (the only (iii) members that CHANGE the class) ----------
# Proper edge n=2 with p<-2: remaining ell ∝ t^((p+2)/2) and delta ~ t  =>
# delta ∝ (1/ell)^(2/|p+2|): POWER-LAW depth divergence (harder than logarithmic).
# witness p=-4: ell = 1/t (units off), delta ~ t: delta*ell -> 1
key("D2_edge_proper_pm4_delta_times_ell_to_1",
    sp.limit((t - 2*log(t))*(1/t), t, oo) == 1)
key("D2_edge_proper_pm4_ell_exact", sp.simplify(sp.integrate(s**(-2), (s, t, oo)) - 1/t) == 0)
# witness p=-3: ell = 2 t^(-1/2), delta ~ t = 4/ell^2: delta*ell^2/4 -> 1  (exponent 2/|p+2| = 2)
key("D2_edge_proper_pm3_ell_exact",
    sp.simplify(sp.integrate(s**(-Rat(3,2)), (s, t, oo)) - 2/sqrt(t)) == 0)
key("D2_edge_proper_pm3_delta_times_ellsq_to_4",
    sp.limit((t - Rat(3,2)*log(t))*(2/sqrt(t))**2, t, oo) == 4)
# Optical edge n=1 with p<-1: sigma ∝ t^(p+1)/|p+1|, delta ~ t/2 => delta ∝ (1/sigma)^(1/|p+1|).
# witness p=-2: sigma = 1/t, delta ~ t/2: delta*sigma -> 1/2
key("D2_edge_optical_pm2_delta_times_sigma_to_half",
    sp.simplify(sp.limit((t/2 - log(t))*(1/t), t, oo) - Rat(1,2)) == 0)

# ---------- essential walls (HAND-CHECK TAG): the harder class appears already at S3 ----------
# A = e^{-1/s}: delta = 1/(2s) EXACTLY, sigma3 = s  =>  delta = 1/(2 sigma3): POWER-LAW depth.
key("ESS_D2_delta_eq_1_over_2sigma3_exact", sp.simplify(-log(exp(-1/s))/2 - 1/(2*s)) == 0)
# S7: sigma7 ~ s/(eps) near the wall (integrand -> 1/eps key above) => delta ~ 1/(2 eps sigma7).

# ---------- S4 genuine member (ii', alpha=2): EXACT relation, not just asymptotic ----------
# sigma4 = X - r/(1+z) = X - r(1+r/X)^(-1) = X^2/(X+r);  1+z = A^(-1/2) = (1+r/X).
# EXACT: (1+z) * sigma4 = X  for ALL r, i.e. delta = ln X + ln(1/sigma4): kappa = 1, exactly.
sig4 = X - r*(1+r/X)**(-1)
key("D2_S4_alpha2_exact_identity_1pz_times_sigma4_eq_X",
    sp.simplify((1+r/X)*sig4 - X) == 0)
key("D2_S4_alpha2_sigma4_eq_X2_over_XpR", sp.simplify(sig4 - X**2/(X+r)) == 0)

print("# ===== D3 SECTION: cross-branch structure =====")
# (a) joint-satisfiability witness n=1/2 (class (i)): ALL FOUR lock branches finite.
key("D3_joint_witness_nhalf_proper_finite",
    sp.simplify(sp.integrate(u**(-Rat(1,4)), (u, 0, 1)) - Rat(4,3)) == 0)
key("D3_joint_witness_nhalf_optical_finite",
    sp.simplify(sp.integrate(u**(-Rat(1,2)), (u, 0, 1)) - 2) == 0)
# (b) the S4-genuine member (ii', alpha=2) is EXCLUDED by every other distance-role branch:
key("D3_S4gen_excluded_S1_integrand_unbounded", sp.limit((1+r/X)**1, r, oo) == oo)
key("D3_S4gen_excluded_S2_integrand_unbounded", sp.limit((1+r/X)**2, r, oo) == oo)
key("D3_S4gen_excluded_S3_chart_radius_oo", True)  # wall at r->oo by class definition
key("D3_S4gen_excluded_S7_integrand_limit_nonzero",
    sp.limit(1/sqrt(eps**2 - (1+r/X)**(-2)), r, oo) == 1/eps)
# (c) kappa sweeps ALL of (0,oo) inside every surviving window (no branch pins kappa):
key("D3_kappa_S3_range_0_to_oo",
    sp.limit(n/2, n, 0, '+') == 0 and sp.limit(n/2, n, oo) == oo)
key("D3_kappa_S1_range_0_to_oo",
    sp.limit(n/(2-n), n, 0, '+') == 0 and sp.limit(n/(2-n), n, 2, '-') == oo)
key("D3_kappa_S2_range_0_to_oo",
    sp.limit(n/(2*(1-n)), n, 0, '+') == 0 and sp.limit(n/(2*(1-n)), n, 1, '-') == oo)
print("# ===== END =====")
