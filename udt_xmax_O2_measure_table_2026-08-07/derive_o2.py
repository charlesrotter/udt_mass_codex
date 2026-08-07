# O2 measure table — exact symbolic derivation (sympy, CPU, float-free).
# Contract: PREREGISTRATION.md (frozen). Characterize only; select nothing.
# Classes: (i) A = c0*(1 - r/Rw)**n, n>0 (wall at finite areal radius Rw; L = n=1, c0=1, Rw=X)
#          (ii) A = exp(-r/X)          (wall at infinite chart radius)
#          (iii) boundary-resolving log refinement (n=1,2 knife-edges) — leading-order checks.
import sympy as sp

r, Rw, X, n, c0, u, p = sp.symbols('r R_w X n c_0 u p', positive=True)
e_over_c = sp.symbols('epsilon', positive=True)  # conserved e/c^2 for infall row (>= sqrt(A) en route)
checks = {}

def bank(key, val):
    checks[key] = val
    print(f"{key}: {val}")

# ---------- Class (i): A = c0*(1-r/Rw)^n ; substitution u = 1-r/Rw, dr = -Rw du ----------
Ai = c0*(1 - r/Rw)**n

# depth delta = -(1/2) log A  -> divergence at wall (u->0+)
delta_i = -sp.Rational(1,2)*sp.log(c0*u**n)
bank('i_depth_limit_wall', sp.limit(delta_i, u, 0, '+'))          # expect oo

# proper radial length: int A^(-1/2) dr = Rw*c0^(-1/2) * int_0^1 u^(-n/2) du
Ip_i = sp.integrate(u**(-n/2), (u, 0, 1), conds='separate')
bank('i_proper_integral_and_condition', Ip_i)                      # 1/(1-n/2) for n<2
proper_general = Rw/sp.sqrt(c0) * 2/(2-n)
bank('i_proper_closed_form_nlt2', sp.simplify(proper_general))
# witnesses
for nv in [sp.Rational(1,2), 1]:
    val = sp.integrate((c0*(1-r/Rw)**nv)**sp.Rational(-1,2), (r, 0, Rw))
    bank(f'i_proper_witness_n={nv}', sp.simplify(val))
bank('i_proper_witness_n=2_divergent',
     sp.integrate((c0*(1-r/Rw)**2)**sp.Rational(-1,2), (r, 0, Rw)))  # expect oo (log boundary)
# banked L cross-check: n=1, c0=1, Rw=X -> 2X
Lproper = sp.integrate((1-r/X)**sp.Rational(-1,2), (r, 0, X))
bank('CROSSCHECK_L_proper_eq_2X', sp.simplify(Lproper - 2*X) == 0)

# optical / Fermat path: int dr/A = Rw/c0 * int_0^1 u^(-n) du
Io_i = sp.integrate(u**(-n), (u, 0, 1), conds='separate')
bank('i_optical_integral_and_condition', Io_i)                     # 1/(1-n) for n<1
for nv in [sp.Rational(1,2)]:
    val = sp.integrate(1/(c0*(1-r/Rw)**nv), (r, 0, Rw))
    bank(f'i_optical_witness_n={nv}', sp.simplify(val))
bank('i_optical_witness_n=1_divergent', sp.integrate(1/(1-r/Rw), (r, 0, Rw)))  # expect oo
# the log-divergence RATE at n=1 (boundary case): partial integral to r = Rw(1-u)
opt_partial_n1 = sp.integrate(1/(1-r/Rw), (r, 0, Rw*(1-u)))
bank('i_optical_n1_partial_log_rate', sp.simplify(opt_partial_n1)) # expect -Rw*log(u)
bank('i_optical_witness_n=2_divergent', sp.integrate(1/(1-r/Rw)**2, (r, 0, Rw)))

# light travel time: int dr/c_eff with c_eff = c*A (lock; c_eff ratio = lambda_t = A, phi_obs=0)
# => identically (1/c) * optical row. Symbolic statement, no separate integral needed.
c = sp.symbols('c', positive=True)
bank('travel_time_equals_optical_over_c', sp.Eq(sp.Symbol('T'), sp.Symbol('ell_opt')/c))

# areal radius at wall: r -> Rw (finite, definitional in class i)
bank('i_areal_limit', Rw)

# redshift: 1+z = A^(-1/2) -> oo
bank('i_redshift_limit_wall', sp.limit((c0*u**n)**sp.Rational(-1,2), u, 0, '+'))

# d_L = (1+z)^2 * r = r/A  (banked: d_L/X = z(z+2) <=> d_L = (1+z)^2 r; verify on L)
zL = 1/sp.sqrt(1-r/X) - 1
dL_banked_form = X*zL*(zL+2)
bank('CROSSCHECK_dL_convention_L', sp.simplify(dL_banked_form - (zL+1)**2*r) == 0)
bank('i_dL_limit_wall', sp.limit(Rw*(1-u)/(c0*u**n), u, 0, '+'))   # expect oo all n

# d_A adjudication: Etherington d_L=(1+z)^2 d_A with banked d_L=(1+z)^2 r forces d_A = r.
dA = Rw*(1-u)
bank('i_dA_limit_wall_convention_r', sp.limit(dA, u, 0, '+'))       # finite Rw
# variant (prereg wording d_A = r/(1+z)) reported neutrally:
bank('i_dA_variant_r_over_1pz_limit', sp.limit(Rw*(1-u)*sp.sqrt(c0*u**n), u, 0, '+'))  # 0

# infalling radial geodesic proper time (lock metric, static Killing energy e = A c^2 dt/dtau):
# rdot^2 = e^2/c^2 - c^2 A ; tau = int dr / sqrt(e^2/c^2 - c^2 A); near wall integrand -> c/e finite.
# finiteness governed by chart range: class (i) FINITE for all n (bounded integrand, finite range).
integrand_wall_limit = sp.limit(1/sp.sqrt(e_over_c**2 - c0*u**n), u, 0, '+')
bank('i_infall_integrand_wall_limit', integrand_wall_limit)         # 1/epsilon (bounded)

# ---------- Class (ii): A = exp(-r/X), wall at r -> oo ----------
Aii = sp.exp(-r/X)
bank('ii_depth_limit', sp.limit(-sp.Rational(1,2)*sp.log(Aii), r, sp.oo))       # oo
bank('ii_proper_divergent', sp.integrate(sp.exp(r/(2*X)), (r, 0, sp.oo)))       # oo (banked)
bank('ii_optical_divergent', sp.integrate(sp.exp(r/X), (r, 0, sp.oo)))          # oo
bank('ii_areal_limit', sp.limit(r, r, sp.oo))                                   # oo (chart)
bank('ii_redshift_limit', sp.limit(sp.exp(r/(2*X)), r, sp.oo))                  # oo
bank('ii_dL_limit', sp.limit(r*sp.exp(r/X), r, sp.oo))                          # oo
bank('ii_dA_limit_convention_r', sp.limit(r, r, sp.oo))                         # oo
bank('ii_dA_variant_limit', sp.limit(r*sp.exp(-r/(2*X)), r, sp.oo))             # 0
bank('ii_infall_integrand_limit', sp.limit(1/sp.sqrt(e_over_c**2 - Aii), r, sp.oo))  # 1/eps>0, infinite range -> divergent

# ---------- Class (iii): log-refined knife-edges (completeness of the parametrization) ----------
# proper at n=2 with A = c0 (1-r/Rw)^2 |log u|^(-p_) : integrand ~ u^(-1) |log u|^(p_/2)... resolve:
# proper integrand u^{-1}*|ln u|^{q}: finite iff q < -1
# substitute t = -log u (u->0+ <=> t->oo); du/u = -dt. Edge integrand becomes t^q dt on (log 2, oo).
t, qq = sp.symbols('t q', real=True)
I_edge = sp.integrate(t**qq, (t, sp.log(2), sp.oo), conds='separate')
bank('iii_edge_t^q_on_(log2,oo)', I_edge)   # finite iff q < -1 (proper n=2 edge: q = p/2 -1... see notes)
# optical at n=1 with A = c0*u*(-log u)^p: int du/(u*(-log u)^p) = int t^(-p) dt: finite iff p > 1
I_opt_edge = sp.integrate(t**(-p), (t, sp.log(2), sp.oo), conds='separate')
bank('iii_optical_n1_logcorrected_t^-p', I_opt_edge)
# explicit witnesses
bank('iii_witness_p=2_finite', sp.integrate(t**(-2), (t, sp.log(2), sp.oo)))   # 1/log 2
bank('iii_witness_p=1_divergent', sp.integrate(t**(-1), (t, sp.log(2), sp.oo)))  # oo

print("\nALL_KEYS:", len(checks))
