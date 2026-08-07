# ADVERSARIAL REVIEW 1 — independent recompute for O3 (written fresh; derive_o3.py NOT read
# before this script was authored and run). Exact sympy, float-free. Keys R1_*.
import sympy as sp

out = []
def K(name, val):
    out.append(f"{name} = {bool(val)}")

r, u, s, t, tau = sp.symbols('r u s t tau', positive=True)
Rw, X, c0, eps, h, c = sp.symbols('R_w X c0 epsilon h c', positive=True)
n = sp.Symbol('n', positive=True)
alpha = sp.Symbol('alpha', positive=True)
p = sp.Symbol('p', real=True)

# ---------- D1 : S1 proper length int A^{-1/2} dr ----------
# class (i): A = c0 u^n, dr = -Rw du, integral over u in (0,1)
n_lt2 = sp.Symbol('n2', positive=True)  # n = 2 - 2q param; use direct assumption instead
q = sp.Symbol('q', positive=True)       # q = (2-n)/2 > 0  <=> n < 2
n_of_q = 2 - 2*q
I_S1_i = sp.integrate(u**(-(n_of_q)/2), (u, 0, 1))   # = 1/q
K('R1_S1_i_unit_integral_eq_1_over_q', sp.simplify(I_S1_i - 1/q) == 0)
val_S1_i = Rw/sp.sqrt(c0) * I_S1_i
K('R1_S1_i_value_eq_2Rw_over_sqrtc0_2mn',
  sp.simplify(val_S1_i - 2*Rw/(sp.sqrt(c0)*(2 - n_of_q))) == 0)
# n = 2: integrand u^{-1} -> log divergent; n > 2: power divergent
part_n2 = sp.integrate(u**-1, (u, t, 1))             # = -ln t
K('R1_S1_i_n2_partial_eq_minus_lnt', sp.simplify(part_n2 + sp.log(t)) == 0)
K('R1_S1_i_n2_divergent', sp.limit(part_n2, t, 0, '+') == sp.oo)
g = sp.Symbol('g', positive=True)                    # n = 2 + 2g > 2
part_ngt2 = sp.integrate(u**(-(2+2*g)/2), (u, t, 1))
K('R1_S1_i_ngt2_divergent', sp.limit(part_ngt2, t, 0, '+') == sp.oo)
# class (ii): integrand e^{r/2X} on (0,oo)
K('R1_S1_ii_divergent', sp.integrate(sp.exp(r/(2*X)), (r, 0, sp.oo)) == sp.oo)
# class (ii'): integrand (1+r/X)^{alpha/2} >= 1, infinite range
K('R1_S1_iiprime_integrand_to_oo', sp.limit((1+r/X)**(alpha/2), r, sp.oo) == sp.oo)
K('R1_S1_iiprime_integrand_ge1_at0', sp.simplify((1+r/X)**(alpha/2)).subs(r, 0) == 1)
# class (iii) edge n=2: proper integrand ~ u^{-1} t^{p/2}; substitute t=-ln u -> int t^{p/2} dt on (T,oo)
Pg = sp.Symbol('Pg', positive=True)                  # -p/2 = 1 + Pg > 1 <=> p < -2
I_edge = sp.integrate(t**(-(1+Pg)), (t, sp.log(2), sp.oo))
K('R1_S1_iii_edge_finite_P_gt1_form', sp.simplify(I_edge - sp.log(2)**(-Pg)/Pg) == 0)
K('R1_S1_iii_edge_p_eq_m2_divergent',
  sp.integrate(t**(-1), (t, sp.log(2), sp.oo)) == sp.oo)
# ESS: A = e^{-1/s}; proper integrand e^{1/(2s)} >= 1/(2s) (since e^x >= x for x>0)
x = sp.Symbol('x', positive=True)
K('R1_ESS_exp_ge_x', sp.simplify(sp.exp(x) - x - 1).subs(x, 0) == 0 and
  sp.diff(sp.exp(x) - x, x).subs(x, 1) > 0)  # e^x - x min at x=0 -> e^x>=1+x>=x
K('R1_ESS_S1_harmonic_divergent', sp.integrate(1/(2*s), (s, 0, Rw)) == sp.oo)

# ---------- D1 : S2 optical int dr/A  (== c * travel time under lock c_eff = cA) ----------
w = sp.Symbol('w', positive=True)                    # w = 1-n > 0 <=> n < 1
n_of_w = 1 - w
I_S2_i = sp.integrate(u**(-(n_of_w)), (u, 0, 1))     # = 1/w
K('R1_S2_i_unit_integral_eq_1_over_w', sp.simplify(I_S2_i - 1/w) == 0)
K('R1_S2_i_value_eq_Rw_over_c0_1mn',
  sp.simplify(Rw/c0*I_S2_i - Rw/(c0*(1 - n_of_w))) == 0)
# n=1 member: partial optical integral = -Rw/c0 * ln u  (exact); log divergent
part_opt_n1 = sp.integrate(Rw/c0 * u**-1, (u, t, 1))
K('R1_S2_i_n1_partial_eq_minus_Rw_lnu_over_c0', sp.simplify(part_opt_n1 - (-Rw/c0*sp.log(t))) == 0)
K('R1_S2_i_n1_logdivergent', sp.limit(part_opt_n1, t, 0, '+') == sp.oo)
# rate: delta(u) = -(n/2) ln u at c0=1 -> ell_opt = -Rw ln u = 2 Rw delta / n  (n=1)
delta_i = -(n/2)*sp.log(u) - sp.Rational(1,2)*sp.log(c0)
K('R1_S2_i_n1_rate_ell_eq_2Rw_delta_over_n',
  sp.simplify((-Rw*sp.log(u)) - 2*Rw*delta_i.subs(c0,1)/n) == 0)
# n>1 divergent
part_ngt1 = sp.integrate(u**(-(1+g)), (u, t, 1))
K('R1_S2_i_ngt1_divergent', sp.limit(part_ngt1, t, 0, '+') == sp.oo)
K('R1_S2_ii_divergent', sp.integrate(sp.exp(r/X), (r, 0, sp.oo)) == sp.oo)
K('R1_S2_iiprime_integrand_to_oo', sp.limit((1+r/X)**alpha, r, sp.oo) == sp.oo)
# (iii) edge n=1: integrand ~ u^{-1} t^p -> int t^p dt finite iff p < -1
Q = sp.Symbol('Q', positive=True)                    # Q = -p > 1
K('R1_S2_iii_edge_finite_Q_gt1',
  sp.simplify(sp.integrate(t**(-(1+Q)), (t, sp.log(2), sp.oo)) - sp.log(2)**(-Q)/Q) == 0)
K('R1_S2_iii_edge_p_eq_m1_divergent',
  sp.integrate(t**(-1), (t, sp.log(2), sp.oo)) == sp.oo)
K('R1_ESS_S2_divergent_by_comparison', True)  # 1/A = e^{1/s} >= e^{1/(2s)} >= 1/(2s): same harmonic bound

with open('review1_output.txt', 'a') as f:
    f.write("# ===== R1 PART 1: D1 S1/S2 =====\n")
    for line in out: f.write(line + "\n")
print("\n".join(out))

# ---------- D1 : S3 areal / S4 r*sqrt(A) / S5 d_L / S6 depth ----------
out = []
A_i   = c0*u**n                       # u = 1 - r/Rw, r = Rw(1-u)
A_ii  = sp.exp(-r/X)
A_iip = (1+r/X)**(-alpha)
A_iii = c0*u**n*(-sp.log(u))**(-p)    # near-wall model (see amendment note)
# S3: wall chart location
K('R1_S3_i_wall_finite_Rw', True)     # definitional: u->0 <=> r->Rw (finite)
K('R1_S3_ii_iiprime_wall_infinite', sp.limit(A_ii, r, sp.oo) == 0 and sp.limit(A_iip, r, sp.oo) == 0)
# S4 class (i): v = Rw(1-u) sqrt(c0) u^{n/2}; wall value 0; interior max u = n/(n+2)
v_i = Rw*(1-u)*sp.sqrt(c0)*u**(n/2)
K('R1_S4_i_wall_value_0', sp.limit(v_i, u, 0, '+') == 0)
crit = sp.solve(sp.diff(v_i, u), u)
K('R1_S4_i_interior_max_u_eq_n_over_np2', sp.simplify(crit[0] - n/(n+2)) == 0 if crit else False)
# S4 class (ii): v = r e^{-r/2X}; max at r=2X; wall value 0
v_ii = r*sp.exp(-r/(2*X))
K('R1_S4_ii_wall_value_0', sp.limit(v_ii, r, sp.oo) == 0)
K('R1_S4_ii_max_at_2X', sp.simplify(sp.solve(sp.diff(v_ii, r), r)[0] - 2*X) == 0)
# S4 class (ii'): v = r (1+r/X)^{-alpha/2}
v_a = r*(1+r/X)**(-alpha/2)
K('R1_S4_iiprime_alpha1_divergent', sp.limit(v_a.subs(alpha,1), r, sp.oo) == sp.oo)
v2 = v_a.subs(alpha, 2)
K('R1_S4_iiprime_alpha2_eq_rX_over_Xpr', sp.simplify(v2 - r*X/(X+r)) == 0)
K('R1_S4_iiprime_alpha2_monotone', sp.simplify(sp.diff(v2, r) - X**2/(X+r)**2) == 0)
K('R1_S4_iiprime_alpha2_wall_value_X', sp.limit(v2, r, sp.oo) == X)
K('R1_S4_iiprime_alpha3_wall_value_0', sp.limit(v_a.subs(alpha,3), r, sp.oo) == 0)
ag = sp.Symbol('ag', positive=True)   # alpha = 2 + ag > 2
crit_a = sp.solve(sp.diff(v_a.subs(alpha, 2+ag), r), r)
K('R1_S4_iiprime_critpoint_2X_over_am2', any(sp.simplify(cc - 2*X/ag) == 0 for cc in crit_a))
# S4 class (iii): wall value 0 (witnesses p=2, p=-2, n=1); OBSERVER-END check p=3 (my attack)
v_iii = Rw*(1-u)*sp.sqrt(A_iii)
K('R1_S4_iii_wall_value_0_p2',  sp.limit(v_iii.subs([(n,1),(p,2)]),  u, 0, '+') == 0)
K('R1_S4_iii_wall_value_0_pm2', sp.limit(v_iii.subs([(n,1),(p,-2)]), u, 0, '+') == 0)
yv = sp.Symbol('yv', positive=True)  # yv = 1-u (observer end yv->0+); avoids sympy branch bug at u->1-
v_iii_p3 = Rw*yv*sp.sqrt(c0)*(1-yv)**sp.Rational(1,2)*(-sp.log(1-yv))**sp.Rational(-3,2)
K('R1_ATTACK_S4_iii_observer_end_divergent_p3',
  sp.limit(v_iii_p3, yv, 0, '+') == sp.oo)  # v -> +oo at r->0 (p>2): "non-mono ->0" needs wall-local scope
# ESS: v = r e^{-1/(2s)}, s = Rw - r
v_ess = (Rw - s)*sp.exp(-1/(2*s))
K('R1_ESS_S4_wall_value_0', sp.limit(v_ess, s, 0, '+') == 0)
# S5: exact identity ln d_L = 2 delta + ln r  (d_L = r/A, delta = -(1/2) ln A)
Asym = sp.Symbol('A', positive=True)
K('R1_S5_identity_lndL_eq_2delta_plus_lnr',
  sp.simplify(sp.log(r/Asym) - (2*(-sp.Rational(1,2)*sp.log(Asym)) + sp.log(r))) == 0)
K('R1_S5_i_divergent',  sp.limit((Rw*(1-u))/A_i, u, 0, '+') == sp.oo)
K('R1_S5_ii_divergent', sp.limit(r/A_ii, r, sp.oo) == sp.oo)
K('R1_S5_iiprime_divergent', sp.limit(r/A_iip, r, sp.oo) == sp.oo)
K('R1_S5_iii_divergent_p2',  sp.limit((Rw*(1-u))/A_iii.subs([(n,1),(p,2)]),  u, 0, '+') == sp.oo)
K('R1_S5_iii_divergent_pm2', sp.limit((Rw*(1-u))/A_iii.subs([(n,1),(p,-2)]), u, 0, '+') == sp.oo)
K('R1_ESS_S5_divergent', sp.limit((Rw-s)/sp.exp(-1/s), s, 0, '+') == sp.oo)
# ATTACK check: d_L = Rw e^{2delta}(1+o(1)) is CLASS-(i/iii/ESS)-scoped; in (ii) d_L = r e^{2delta}
K('R1_ATTACK_S5_ii_dL_eq_r_times_e2delta_not_Rw',
  sp.simplify(r/A_ii - r*sp.exp(2*(-sp.Rational(1,2)*sp.log(A_ii)))) == 0)
# S6: delta -> oo in every class
d_of = lambda A: -sp.Rational(1,2)*sp.log(A)
K('R1_S6_i_divergent',   sp.limit(d_of(A_i), u, 0, '+') == sp.oo)
K('R1_S6_ii_divergent',  sp.limit(d_of(A_ii), r, sp.oo) == sp.oo)
K('R1_S6_iiprime_divergent', sp.limit(d_of(A_iip), r, sp.oo) == sp.oo)
K('R1_S6_iii_divergent_p2', sp.limit(d_of(A_iii.subs([(n,1),(p,2)])), u, 0, '+') == sp.oo)
K('R1_ESS_S6_divergent', sp.limit(d_of(sp.exp(-1/s)), s, 0, '+') == sp.oo)

with open('review1_output.txt', 'a') as f:
    f.write("# ===== R1 PART 2: D1 S3-S6 =====\n")
    for line in out: f.write(line + "\n")
print("\n".join(out))

# ---------- D1 : S7 infall proper time  integrand 1/(c sqrt(eps^2 - A)) ----------
out = []
# class (i) exact witness n=1, c0=1, eps^2 = 1+h^2:  c*tau = Rw*int_0^1 (1+h^2-u)^{-1/2} du
I7 = Rw*sp.integrate((1+h**2-u)**sp.Rational(-1,2), (u, 0, 1))
K('R1_S7_i_exact_witness_n1_eq_2Rw_sqrt1ph2_minus_h',
  sp.simplify(I7 - 2*Rw*(sp.sqrt(1+h**2)-h)) == 0)
# wall-limit of integrand (any class with A->0): 1/sqrt(eps^2 - A) -> 1/eps
K('R1_S7_integrand_wall_limit_1_over_eps',
  sp.limit(1/sp.sqrt(eps**2 - c0*u**n), u, 0, '+') == 1/eps)
# boundedness on (0,1] for class (i) requires eps^2 > c0 = sup A: bound 1/sqrt(eps^2-c0)
e2 = c0 + h**2   # eps^2 = c0 + h^2 > c0 = sup A on the path (class i)
# integrand 1/sqrt(e2 - c0 u^n) is monotone-decreasing toward the wall: sup = 1/h at u=1 (r=0),
# wall limit 1/sqrt(c0+h^2); bounded on all of (0,1] -> finite over finite range for ALL n
K('R1_S7_i_bounded_integrand_all_n',
  sp.simplify(1/sp.sqrt(e2 - c0*u**n).subs(u,1) - 1/h) == 0 and
  sp.limit(1/sp.sqrt(e2 - c0*u**n), u, 0, '+') == 1/sp.sqrt(c0 + h**2))
# comparison: integrand >= 1/eps (since A >= 0) -> infinite range => divergent on (ii)/(ii')
K('R1_S7_comparison_ge_1_over_eps', sp.simplify(1/sp.sqrt(eps**2 - 0) - 1/eps) == 0)
K('R1_S7_ii_divergent_lower_bound', sp.integrate(1/eps, (r, 0, sp.oo)) == sp.oo)
# ATTACK: class (iii) p>0 has A -> oo at the observer end u->1 (proviso eps^2 > sup A unsatisfiable from r=0)
K('R1_ATTACK_S7_iii_p_pos_A_unbounded_at_observer',
  sp.limit(c0*u*(-sp.log(u))**(-2), u, 1, '-') == sp.oo)
# ATTACK: surviving OPTICAL edge member {n=1, p<-1}: 1/A non-integrable at the OBSERVER end r->0
# 1/A ~ c0^{-1} u^{-1} t^{p}, t = -ln u ~ (1-u) -> integrand ~ (1-u)^{p}; int_0 (1-u)^p du div iff p <= -1
y = sp.Symbol('y', positive=True)  # y = 1-u near observer
K('R1_ATTACK_S2_iii_edge_observer_end_divergent_pm2',
  sp.integrate(y**(-2), (y, 0, sp.Rational(1,2))) == sp.oo)   # p=-2 surviving member: divergent at r=0 end
K('R1_ATTACK_S1_iii_edge_observer_end_divergent_pm4',
  sp.integrate(y**(-2), (y, 0, sp.Rational(1,2))) == sp.oo)   # proper p=-4: A^{-1/2} ~ y^{p/2} = y^{-2}
# ESS S7: integrand -> 1/eps at wall; sup A = e^{-1/Rw} < 1 (proviso satisfiable)
K('R1_ESS_S7_integrand_wall_limit', sp.limit(1/sp.sqrt(eps**2 - sp.exp(-1/s)), s, 0, '+') == 1/eps)
K('R1_ESS_A_at_observer_lt_1', (-1/Rw).is_negative and sp.log(sp.exp(-1/Rw)).is_negative)  # exponent < 0 => A(0) = e^{-1/Rw} < 1

with open('review1_output.txt', 'a') as f:
    f.write("# ===== R1 PART 3: D1 S7 + attacks =====\n")
    for line in out: f.write(line + "\n")
print("\n".join(out))

# ---------- D2 : approach-profile classes ----------
out = []
delta_u = -(n/2)*sp.log(u) - sp.Rational(1,2)*sp.log(c0)   # exact for class (i)
# S3: sigma3 = Rw u ; residual delta - (n/2) ln(1/sigma3) must be u-independent, = (n/2)lnRw - (1/2)ln c0
sig3 = Rw*u
res3 = sp.simplify(delta_u - (n/2)*sp.log(1/sig3))
K('R1_D2_S3_residual_u_free', sp.diff(res3, u) == 0)
K('R1_D2_S3_const_exact', sp.simplify(res3 - ((n/2)*sp.log(Rw) - sp.Rational(1,2)*sp.log(c0))) == 0)
# S1: sigma1 = 2Rw u^{(2-n)/2}/(sqrt(c0)(2-n)) with n=2-2q ; kappa = n/(2-n)
nq = 2 - 2*q
sig1 = 2*Rw*u**q/(sp.sqrt(c0)*(2*q))
kap1 = nq/(2 - nq)
res1 = sp.simplify(delta_u.subs(n, nq) - kap1*sp.log(1/sig1))
K('R1_D2_S1_residual_u_free', sp.simplify(sp.diff(res1, u)) == 0)
# S2: sigma2 = Rw u^{1-n}/(c0(1-n)) with n=1-w ; kappa = n/(2(1-n))
nw = 1 - w
sig2 = Rw*u**w/(c0*w)
kap2 = nw/(2*(1 - nw))
res2 = sp.simplify(delta_u.subs(n, nw) - kap2*sp.log(1/sig2))
K('R1_D2_S2_residual_u_free', sp.simplify(sp.diff(res2, u)) == 0)
# S7: sigma7/u -> Rw/(c eps): d(sigma7)/du = Rw/(c sqrt(eps^2 - c0 u^n)) -> Rw/(c eps); L'Hopital
K('R1_D2_S7_sigma_over_u_limit_Rw_over_c_eps',
  sp.limit(Rw/(c*sp.sqrt(eps**2 - c0*u**n)), u, 0, '+') == Rw/(c*eps))
# general-m: sigma_m = Rw c0^{-m} u^{1-nm}/(1-nm); kappa_m = n/(2(1-nm)); 1/kappa = 2/n - 2m
m_, km = sp.symbols('m k', positive=True)
b = sp.Symbol('b', positive=True)   # b = 1 - n*m > 0
m_of_b = (1 - b)/n
sig_m = Rw*c0**(-m_of_b)*u**b/b
kap_m = n/(2*b)
res_m = sp.simplify(delta_u - kap_m*sp.log(1/sig_m))
K('R1_D2_general_m_residual_u_free', sp.simplify(sp.diff(res_m, u)) == 0)
K('R1_D2_general_m_reciprocal_linear',
  sp.simplify(1/kap_m - (2/n - 2*m_of_b)) == 0)
K('R1_D2_reciprocal_spacing_areal_proper', sp.simplify((2/n - 0) - (2/n - 1)) == 1)
K('R1_D2_reciprocal_spacing_proper_optical', sp.simplify((2/n - 1) - (2/n - 2)) == 1)

# ---------- D2 (cont): class (iii) interior log-log corrections ----------
# delta(t) = (n/2) t + (p/2) ln t - (1/2) ln c0,  t = -ln u
delta_t = (n/2)*t + (p/2)*sp.log(t) - sp.Rational(1,2)*sp.log(c0)
# AREAL: sigma3 = Rw e^{-t}; claim: delta = (n/2)ln(1/s3) + (p/2)lnln(1/s3) + C + o(1)
L3 = t + sp.log(1/Rw)*0 + 0  # ln(1/sigma3) = t - ln Rw; use Rw=1 wlog for the o(1) structure
res_areal = (delta_t.subs(c0,1) - (n/2)*t - (p/2)*sp.log(t)).subs(p,2)  # trivially 0: exact at Rw=1
K('R1_D2_iii_areal_loglog_coeff_p_over_2_exact_at_Rw1', sp.simplify(res_areal) == 0)
# with general Rw: lnln(1/s3) = ln(t - lnRw) -> ln t + o(1): residual -> const (limit check, witness n=1,p=2)
res_areal_gen = delta_t.subs([(n,1),(p,2),(c0,1)]) - sp.Rational(1,2)*sp.log(1/(Rw*sp.exp(-t))) - 1*sp.log(sp.log(1/(Rw*sp.exp(-t))))
K('R1_D2_iii_areal_residual_converges_witness',
  sp.limit(res_areal_gen, t, sp.oo).is_finite)
# PROPER L'Hopital: F(u)=int_0^u s^{-n/2} t^{p/2} ds vs G(u)=u^q t^{p/2}  (q=(2-n)/2)
# F'/G' should reduce to 1/(q - p/(2t)) -> 1/q
Fp = u**(-n/2)*(-sp.log(u))**(p/2)
Gp = sp.diff(u**((2-n)/2)*(-sp.log(u))**(p/2), u)
ratio = sp.simplify(Fp/Gp)
target = 1/((2-n)/2 - p/(2*(-sp.log(u))))
K('R1_D2_iii_S1_lhopital_ratio_reduction', sp.simplify(ratio - target) == 0)
K('R1_D2_iii_S1_lhopital_limit_1_over_q',
  sp.limit(ratio.subs([(n, 2-2*q if False else 1), (p, 2)]), u, 0, '+') == 2)  # n=1: q=1/2, 1/q=2
# proper log-log coefficient: kappa/n*p = p/(2-n) -- derive via inversion at witness n=1, p=2:
# EXACT sigma1 at n=1,p=2,c0=1,Rw=1: int_0^u s^{-1/2}(-ln s) ds = 2 sqrt(u)(t+2), t=-ln u
# verify by differentiation + zero boundary value at u->0
cand = 2*sp.sqrt(u)*(-sp.log(u) + 2)
K('R1_D2_iii_S1_exact_sigma_eq_2sqrtu_t_plus_2',
  sp.simplify(sp.diff(cand, u) - u**sp.Rational(-1,2)*(-sp.log(u))) == 0 and
  sp.limit(cand, u, 0, '+') == 0)
# residual: delta - kappa ln(1/sig) - (kappa p / n) lnln(1/sig)  with kappa=1, (kappa p/n)=2
sig1_t = 2*sp.exp(-t/2)*(t+2)   # u = e^{-t}
delta_w = t/2 + sp.log(t)       # n=1, p=2, c0=1
RES = delta_w - 1*sp.log(1/sig1_t) - 2*sp.log(sp.log(1/sig1_t))
RES_limit = sp.limit(RES, t, sp.oo)
K('R1_D2_iii_S1_inversion_residual_converges', RES_limit.is_finite)
K('R1_D2_iii_S1_inversion_const_eq_log4', sp.simplify(RES_limit - sp.log(4)) == 0)
K('R1_D2_iii_S1_inversion_const_eq_log8', sp.simplify(RES_limit - sp.log(8)) == 0)
with open('review1_output.txt','a') as f:
    f.write("# ===== R1 PART 4a: D2 (iii) interior =====\n")
    for line in out: f.write(line+"\n")
print("\n".join(out)); out=[]

# ---------- D2 (cont): edge-rescued members + ESS + S4 alpha=2 ----------
# PROPER edge n=2, p=-4 (c0=1, Rw=1): ell(t) = int_t^oo tau^{-2} = 1/t ; delta ~ t - 2 ln t
ell_pm4 = sp.integrate(tau**(-2), (tau, t, sp.oo))
K('R1_D2_edge_proper_pm4_ell_eq_1_over_t', sp.simplify(ell_pm4 - 1/t) == 0)
K('R1_D2_edge_proper_pm4_delta_ell_to_1',
  sp.limit((t - 2*sp.log(t))*ell_pm4, t, sp.oo) == 1)
# p=-3: ell = int_t^oo tau^{-3/2} = 2/sqrt(t); delta ~ t - (3/2)ln t; delta*ell^2 -> 4
ell_pm3 = sp.integrate(tau**sp.Rational(-3,2), (tau, t, sp.oo))
K('R1_D2_edge_proper_pm3_ell_eq_2_over_sqrtt', sp.simplify(ell_pm3 - 2/sp.sqrt(t)) == 0)
K('R1_D2_edge_proper_pm3_delta_ellsq_to_4',
  sp.limit((t - sp.Rational(3,2)*sp.log(t))*ell_pm3**2, t, sp.oo) == 4)
# general exponent proper edge: ell ~ t^{(p+2)/2} -> t ~ ell^{2/(p+2)}; delta ~ t => delta ~ ell^{-2/|p+2|}: 
K('R1_D2_edge_proper_exponent_pm4_is_1', sp.Rational(2,abs(-4+2)) == 1)
K('R1_D2_edge_proper_exponent_pm3_is_2', sp.Rational(2,abs(-3+2)) == 2)
# OPTICAL edge n=1, p=-2: sigma = int_t^oo tau^{-2} = 1/t; delta ~ t/2 - ln t... p=-2: delta = t/2 + (p/2)ln t = t/2 - ln t
sig_pm2 = sp.integrate(tau**(-2), (tau, t, sp.oo))
K('R1_D2_edge_optical_pm2_delta_sigma_to_half',
  sp.limit((t/2 - sp.log(t))*sig_pm2, t, sp.oo) == sp.Rational(1,2))
# ESS: delta = -(1/2) ln e^{-1/s} = 1/(2s) exact; sigma3 = s
K('R1_ESS_D2_delta_eq_1_over_2s_exact',
  sp.simplify(-sp.Rational(1,2)*sp.log(sp.exp(-1/s)) - 1/(2*s)) == 0)
# S4 alpha=2 exact identity: (1+z) sigma4 = X for all r
opz = 1 + r/X                      # 1+z = A^{-1/2} = 1+r/X
sig4 = X - r*X/(X+r)
K('R1_D2_S4_alpha2_sigma4_eq_X2_over_XpR', sp.simplify(sig4 - X**2/(X+r)) == 0)
K('R1_D2_S4_alpha2_identity_1pz_sigma4_eq_X', sp.simplify(opz*sig4 - X) == 0)
K('R1_D2_S4_alpha2_kappa1_exact',
  sp.simplify(sp.log(opz) - (sp.log(1/sig4) + sp.log(X))) == 0)   # delta = ln(1/sigma4) + ln X
with open('review1_output.txt','a') as f:
    f.write("# ===== R1 PART 4b: D2 edges/ESS/S4 =====\n")
    for line in out: f.write(line+"\n")
print("\n".join(out)); out=[]

# ---------- D3 : cross-branch structure ----------
out = []
# joint witness n = 1/2: proper AND optical finite (values exact)
K('R1_D3_joint_witness_nhalf_proper',
  sp.simplify(sp.integrate(u**sp.Rational(-1,4), (u,0,1)) - sp.Rational(4,3)) == 0)
K('R1_D3_joint_witness_nhalf_optical',
  sp.simplify(sp.integrate(u**sp.Rational(-1,2), (u,0,1)) - 2) == 0)
# S4-genuine atom {(ii') alpha=2} excluded by every other distance branch:
A2 = (1+r/X)**(-2)
K('R1_D3_S4gen_excl_S1', sp.limit(A2**sp.Rational(-1,2), r, sp.oo) == sp.oo)   # integrand unbounded, >=1: divergent
K('R1_D3_S4gen_excl_S2', sp.limit(1/A2, r, sp.oo) == sp.oo)
K('R1_D3_S4gen_excl_S3', sp.limit(A2, r, sp.oo) == 0)                          # wall at infinite chart radius
K('R1_D3_S4gen_excl_S7', sp.limit(1/sp.sqrt(eps**2 - A2), r, sp.oo) == 1/eps)  # nonzero limit over infinite range
# kappa ranges sweep (0,oo):
kS3 = n/2; kS1 = (2-2*q)/(2*q); kS2 = (1-w)/(2*w)
K('R1_D3_kappa_S3_range', sp.limit(kS3, n, 0, '+') == 0 and sp.limit(kS3, n, sp.oo) == sp.oo)
K('R1_D3_kappa_S1_range', sp.limit(kS1, q, 1, '-') == 0 and sp.limit(kS1, q, 0, '+') == sp.oo)  # q=(2-n)/2: n->0 <=> q->1
K('R1_D3_kappa_S2_range', sp.limit(kS2, w, 1, '-') == 0 and sp.limit(kS2, w, 0, '+') == sp.oo)
# lattice chain: n<1 => n<2 (S2-window inside S1-window); optical edge member {n=1,p<-1} inside S1 window (n=1<2)
K('R1_D3_chain_S2_window_subset_S1', True)   # 0<n<1 => 0<n<2, immediate
# S3 == S7 verdict-degeneracy across the family: (i) all n F/F; (ii),(ii') D/D; (iii) F/F; ESS F/F  (cells above)
K('R1_D3_S3_S7_verdict_degenerate_bookkeeping', True)  # assembled from D1 keys, no new math
# R-2 leading-class check: (iii) interior delta/ln(1/sigma3) -> kappa = n/2 > 0 (witness n=1, p=-2: log-suppressed)
dw = t/2 - sp.log(t)          # delta at n=1, p=-2, c0=1
K('R1_D3_R2_iii_interior_leading_log_witness_pm2',
  sp.limit(dw/(t - sp.log(Rw)), t, sp.oo) == sp.Rational(1,2))   # sigma3 = Rw e^{-t}: ln(1/sigma3) = t - ln Rw
# COMPLETENESS ATTACK: log-corrected alpha=2 edge of (ii') under S4 (candidate NEW genuine members?)
# A = (1+r/X)^{-2} L^{nu}, L = ln(e + r/X): v = r sqrt(A) = (rX/(X+r)) L^{nu/2}
Lr = sp.log(sp.E + r/X)
for nu, tag in [(sp.Rational(1,1),'nu_pos'), (sp.Rational(-1,1),'nu_neg')]:
    v_c = (r*X/(X+r))*Lr**(nu/2)
    lim = sp.limit(v_c, r, sp.oo)
    if nu > 0:
        K(f'R1_ATTACK_S4_iiprime_logcorr_{tag}_divergent', lim == sp.oo)          # posit fails
    else:
        K(f'R1_ATTACK_S4_iiprime_logcorr_{tag}_wall_value_0', lim == 0)           # degenerate (0 at wall, 0 at r=0)
# => the alpha=2 genuine member is itself a KNIFE-EDGE: log corrections destroy genuineness either way
with open('review1_output.txt','a') as f:
    f.write("# ===== R1 PART 5: D3 + completeness attacks =====\n")
    for line in out: f.write(line+"\n")
print("\n".join(out))

# ---------- ADJUDICATION vs derive_o3.py (opened only AFTER the recompute above ran) ----------
out = []
# Their key D2_iii_S1_inversion_witness_const_eq_log4 computes: lim F - L - 2 ln L with the
# LEADING form L(t) = t/2 - ln t  (NOT ln(1/sigma1) of the actual member).  Reproduce both:
F_ = t/2 + sp.log(t)
Llead = t/2 - sp.log(t)
K('R1_ADJ_their_leading_form_residual_eq_log4',
  sp.simplify(sp.limit(F_ - Llead - 2*sp.log(Llead), t, sp.oo) - sp.log(4)) == 0)
# Against the member's ACTUAL sigma1 = 2 e^{-t/2}(t+2)  (exact, verified above): const = ln 8
Lact = -sp.log(2*sp.exp(-t/2)*(t+2))
K('R1_ADJ_actual_sigma_residual_eq_log8',
  sp.simplify(sp.limit(F_ - Lact - 2*sp.log(Lact), t, sp.oo) - sp.log(8)) == 0)
K('R1_ADJ_difference_is_log2', sp.simplify(sp.log(8) - sp.log(4) - sp.log(2)) == 0)
# general-m log-log coefficient: integrand A^{-m} ~ u^{-nm} t^{mp}; sigma ~ u^b t^{mp}/b, b=1-nm;
# coefficient of ln t in delta after inversion = (p/2)(n*m + b)/b, and with b = 1-n*m this equals
# p/(2b) = (kappa/n)*p  -> confirms areal p/2 (m=0), proper p/(2-n) (m=1/2), optical p/(2(1-n)) (m=1)
mm, bb = sp.symbols('mm bb', positive=True)
coef = (p/2)*(n*mm + bb)/bb
K('R1_D2_loglog_coeff_general_m_eq_p_over_2b',
  sp.simplify(coef.subs(bb, 1-n*mm) - p/(2*(1-n*mm))) == 0)
K('R1_D2_loglog_coeff_specializations',
  sp.simplify(p/(2*(1-n*0)) - p/2) == 0 and
  sp.simplify(p/(2*(1-n*sp.Rational(1,2))) - p/(2-n)) == 0)
with open('review1_output.txt','a') as f:
    f.write("# ===== R1 PART 6: adjudication vs derive_o3.py + general-m loglog =====\n")
    for line in out: f.write(line+"\n")
print("\n".join(out))
