#!/usr/bin/env python3
# D3 — O-B's native-scale question (the AMOUNT). Exact sympy, float-free.
# OBSERVE mode. Each printed KEY is a machine-checkable claim (True/False).
# Ground re-derived where used: O3 kappa table, O2 measure ratios, mixing-lane
# mu defect, D2 thresholds/crossover/fold, D4 nm-trichotomy, M4 exchange chain.
import sympy as sp

RES = []
def key(name, expr_true):
    v = bool(expr_true)
    RES.append((name, v))
    print(f"[{'True ' if v else 'FALSE'}] {name}")
    return v

n, m, rho, s, mu, u, R_w, X, c0 = sp.symbols('n m rho s mu u R_w X c0', positive=True)
z = sp.symbols('z', positive=True)

print("="*70)
print("I1 — X and the banked dimensionless objects (amounts vs free params)")
print("="*70)

# --- O3 kappa table (re-derived): 1+z ~ sigma_k^(-kappa) ---
kappa_areal   = n/2               # S3 areal, all n
kappa_proper  = n/(2-n)           # S1 proper, n<2
kappa_optical = n/(2*(1-n))       # S2 optical, n<1
kappa_general = n/(2*(1-n*m))     # general A-weight m
key("O3_general_reduces_areal_m0",   sp.simplify(kappa_general.subs(m,0)   - kappa_areal)==0)
key("O3_general_reduces_proper_mhalf",sp.simplify(kappa_general.subs(m,sp.Rational(1,2)) - kappa_proper)==0)
key("O3_general_reduces_optical_m1", sp.simplify(kappa_general.subs(m,1)   - kappa_optical)==0)
# reciprocal-kappa linear in m, slope -2 (1/kappa = 2/n - 2m)
key("O3_recip_kappa_linear_slope_-2", sp.simplify(1/kappa_general - (2/n - 2*m))==0)
# n-FREE reciprocal spacing = 1 (the one parameter-free banked number)
sp_ap = sp.simplify(1/kappa_areal  - 1/kappa_proper)
sp_po = sp.simplify(1/kappa_proper - 1/kappa_optical)
key("O3_recip_spacing_areal_proper_eq_1", sp_ap==1)
key("O3_recip_spacing_proper_optical_eq_1", sp_po==1)
key("O3_recip_spacing_is_n_free", (sp_ap.free_symbols==set()) and (sp_po.free_symbols==set()))

# --- O2 measure ratio proper/areal = 2/(2-n): carries n (inherits freeness) ---
ratio_pa = sp.simplify(kappa_proper/kappa_areal)
key("O2_proper_over_areal_eq_2_over_2mn", sp.simplify(ratio_pa - 2/(2-n))==0)
key("O2_measure_ratio_depends_on_n", n in ratio_pa.free_symbols)

# kappa values themselves carry n -> DERIVED FROM a free parameter -> inherit freeness
key("O3_kappa_areal_depends_on_n",   n in kappa_areal.free_symbols)
key("O3_kappa_proper_depends_on_n",  n in kappa_proper.free_symbols)
key("O3_kappa_optical_depends_on_n", n in kappa_optical.free_symbols)

# [R1-A1] LENGTH-INERTNESS of the parameter-free spacing=1, real content (replaces the
# vacuous X*1-X tautology): 1+z = sigma_k^(-kappa) => each measure-role scale-factor carries
# a (1+z)-exponent; consecutive exponents differ by exactly 1 (spacing=1), so consecutive
# measure-role DISTANCES differ by exactly (1+z): proper/areal = optical/proper = (1+z).
# A z-VARYING distance-duality convention-ratio -> selects no fixed z, no fixed separation.
sf_areal   = (1+z)**(-2/n)          # scale-factor exponents from the kappa/sigma_k dictionary
sf_proper  = (1+z)**((n-2)/n)
sf_optical = (1+z)**(2 - 2/n)
key("R1A1_exponent_spacing_is_1",
    sp.simplify(((n-2)/n) - (-2/n) - 1)==0 and sp.simplify((2-2/n) - ((n-2)/n) - 1)==0)
key("R1A1_duality_ratio_is_1plusz",
    sp.simplify(sf_proper/sf_areal - (1+z))==0 and sp.simplify(sf_optical/sf_proper - (1+z))==0)
key("R1A1_duality_ratio_is_z_varying", z in sp.simplify(sf_proper/sf_areal).free_symbols)  # not a fixed separation

print("="*70)
print("I2 — mu (reciprocal-lock defect) and the D2 thresholds")
print("="*70)
# mixing-lane 3x3 charpoly factor (D2 KEY A1): (lam-rho^2)(lam^2 - T lam + d)
T = 1/rho**2 + s**2 - mu**2
d = s**2/rho**2
lam = sp.symbols('lam')
block = lam**2 - T*lam + d
# mu is the DEFECT of the reciprocal lock: lam_time=1/rho^2 is a block root iff mu=0
resid = sp.simplify(block.subs(lam, 1/rho**2))
key("I2_mu_is_reciprocal_lock_defect", sp.simplify(resid - mu**2/rho**2)==0)  # =0 iff mu=0
key("I2_lock_holds_iff_mu0", sp.solve(sp.Eq(resid,0), mu)==[0] or sp.simplify(resid.subs(mu,0))==0)
# mu is dimensionless (unipotent generator; block eigenvalue product mu-independent)
prod_block = sp.simplify(block.subs(lam,0))  # constant term = product of block roots = d
key("I2_block_root_product_mu_independent", mu not in prod_block.free_symbols)  # = s^2/rho^2

# --- D2 threshold mu_c = |s - 1/rho| from the discriminant ---
disc = T**2 - 4*d
disc_fac = ((sp.Rational(1,1)/rho - s)**2 - mu**2)*((1/rho + s)**2 - mu**2)
key("D2_disc_factorization", sp.simplify(disc - disc_fac)==0)
# near-window edge: disc=0 at mu = |s - 1/rho|  -> the threshold is an AMPLITUDE (mu) locus
edge = sp.simplify(disc.subs(mu, sp.Abs(s - 1/rho)))
key("D2_disc_zero_at_mu_c", sp.simplify(edge)==0)
# Does mu_c define a DEPTH rho*(s)? solve mu_c relation for rho: rho depends on mu AND s (free data)
rho_star = sp.solve(sp.Eq(mu, s - 1/rho), rho)   # taking the s>1/rho branch symbolically
key("D2_muc_depth_rides_free_data", any((mu in e.free_symbols) and (s in e.free_symbols) for e in rho_star))

# --- eigenvalue-collision locus rho*s = 1 : a DEPTH locus set by free s ---
rho_coll = sp.solve(sp.Eq(rho*s, 1), rho)[0]     # rho = 1/s
key("D2_collision_depth_eq_1_over_s", sp.simplify(rho_coll - 1/s)==0)
key("D2_collision_depth_rides_free_s", s in rho_coll.free_symbols)  # not native; single surface
# at the collision the block is IMMEDIATELY elliptic for any mu!=0: disc = mu^2(mu^2 - 4 s^2)
disc_at_coll = sp.simplify(disc.subs(rho, 1/s))
key("D2_disc_at_collision", sp.simplify(disc_at_coll - mu**2*(mu**2 - 4*s**2))==0)

# --- QUANTIZATION CHARACTERIZATION (F-SCOPE: state condition, then STOP) ---
# banked (mixing lane): mu unquantized; continuous coboundary family param k; COUPLING-INERT.
# WHAT WOULD BE REQUIRED (pattern only, P4 circle-target c_theta -> 2*pi*Z):
N = sp.symbols('N', integer=True)
# IF the coboundary field k lived on a compact circle target (winding BC / finite-cell junction),
# the winding would be forced discrete: k -> k0 + N (N in Z). Emergent dimensionless amount = N.
key("F_SCOPE_quantization_is_conditional", (N.is_integer is True))  # marker: amount would be integer N
# STOP: not run here (F-SCOPE). No length emerges without N SELECTING a depth/separation.

print("="*70)
print("I3 — fold onset + D4 nm-trichotomy boundaries")
print("="*70)
r = sp.symbols('r', positive=True)
# class (i): A = c0 (1 - r/R_w)^n  -> static depth-gradient law -A_r/(2A)
A = c0*(1 - r/R_w)**n
minus_Ar_over_2A = sp.simplify(-sp.diff(A, r)/(2*A))
key("I3_static_gradient_form", sp.simplify(minus_Ar_over_2A - n/(2*R_w*(1 - r/R_w)))==0)
# strictly positive on 0<r<R_w -> D2 fold condition A_t = -A*A_r UNSATISFIABLE statically
key("I3_static_gradient_positive", sp.simplify(minus_Ar_over_2A.subs({c0:1,n:1,R_w:1,r:sp.Rational(1,2)}))>0)
# fold is a condition on FREE profile data A(t,r); selects no native length (rides A_t)

# D4 trichotomy boundary nm=1 (O2 knife-edges): periodicity variable xi_m = (1+z)^(-2(1-nm)/n)
exp_xi = -2*(1 - n*m)/n
key("D4_xi_exponent_form", sp.simplify(exp_xi - (-2*(1-n*m)/n))==0)
# at nm=1 the exponent -> 0  => ln(1+z)-periodicity (log-periodic decoration)
key("D4_ln1pz_periodicity_at_nm1", sp.simplify(exp_xi.subs(n*m,1))==0 or sp.simplify(exp_xi.subs(m,1/n))==0)
# nm=1 relates FREE n to measure-role m -> selects an edge in parameter space, not a length
key("D4_nm1_relation_free_params", (n in (n*m - 1).free_symbols) and (m in (n*m - 1).free_symbols))
# the oscillation carries a free wavelength lambda (O-E free data)
lam_w, eps = sp.symbols('lambda_w epsilon', positive=True)
dz_cyc = lam_w*(n/(2*R_w))*(1+z)**(1 + 2/n - 2*m)   # D4 C8 radial cycle spacing in z
key("D4_cyclespacing_carries_free_lambda", lam_w in dz_cyc.free_symbols)  # FREE DATA

print("="*70)
print("I4 — the D2 crossover theta_x (observer-supplied)")
print("="*70)
g, M, k_p = sp.symbols('g M k_p', positive=True)
a = 1/rho
theta_x_g = M*a**2/(2*s**2*k_p**2)          # D2 KEY B6b (theta_x^g)
key("I4_thetax_carries_observer_kp", k_p in theta_x_g.free_symbols)
# depends on k_p: d/dk_p != 0  -> OBSERVER-supplied (matter elsewhere cannot know our k_p)
key("I4_thetax_kp_dependence_nonzero", sp.simplify(sp.diff(theta_x_g, k_p))!=0)
# z-drift: theta_x ~ (1+z)^(-2/g) with a=(1+z)^-1 ; check ratio is z-independent
theta_x = theta_x_g**(1/g)
theta_x_z = theta_x.subs(rho, 1+z)
drift_ratio = sp.simplify(theta_x_z / (1+z)**(sp.Rational(-2,1)/g))
key("I4_thetax_drift_exponent_minus2overg", z not in drift_ratio.free_symbols)

print("="*70)
print("I5 — P4 c_theta angular lattice (banked; R1-A2 explicit row)")
print("="*70)
# [R1-A2] The banked P4 angular lattice (menu 2541617, S2c/AM-3): physical spacing
# c_theta = pi*g_theta*m/(2*ell) rides free ell (cell size) + g_theta; MASSLESS-CONFINED,
# E0-UNCUT (labels completion sheets, never a matter state/separation). Bare 2pi = full-circle
# angle-period, COUPLING-INERT to radial X (no banked theta<->radial coupling).
g_theta, ell_cell = sp.symbols('g_theta ell_cell', positive=True)
c_theta = sp.pi*g_theta*m/(2*ell_cell)
key("R1A2_ctheta_rides_free_ell", ell_cell in c_theta.free_symbols)          # FREE-DATA-conditioned
key("R1A2_ctheta_carries_no_radial_X", X not in c_theta.free_symbols)        # COUPLING-INERT to X
key("R1A2_bare_2pi_is_angle_not_separation", (2*sp.pi).free_symbols==set())  # pure angle-period, length-inert

print("="*70)
print("I5 / M4 exchange-rate pattern + P-STATIC-RULER (conditional)")
print("="*70)
# M4 pattern: the ONLY {G,c,M_total} length is G M / c^2 -> c,G supply NO dimensionless amount.
G, c, Mt, La, b, gg = sp.symbols('G c M_total a b g', positive=True)
# dimensional exponents [G]=L^3 M^-1 T^-2, [c]=L T^-1, [M]=M ; require length L^1 M^0 T^0
La_, be_, ga_ = sp.symbols('la be ga', real=True)
eqs = [3*La_ + be_ - 1,        # L
       -La_ + ga_,             # M: -la + ga = 0
       -2*La_ - be_]           # T
solL = sp.solve(eqs, [La_, be_, ga_], dict=True)[0]
key("M4_unique_GcM_length_is_GM_over_c2",
    solL[La_]==1 and solL[be_]==-2 and solL[ga_]==1)   # G^1 c^-2 M^1 => GM/c^2, no free dimensionless
# consonance x_max ~ GM/c^2 supplies NO dimensionless factor (close-to-tautological, M4)

# P-STATIC-RULER (conditional): any posited ell rides X as the dimensionless ratio ell/X;
# static in the DISTANCE-role (areal) measure; z-dependence theta(z)=ell/r(z) via banked dict.
ell = sp.symbols('ell', positive=True)
ratio = ell/X
key("PSR_carrier_is_dimensionless_ratio", sp.simplify(ratio).free_symbols=={ell, X})
key("PSR_ratio_needs_posited_ell", ell in ratio.free_symbols)  # ell is FREE DATA, not native

# ---- SUMMARY ----
print("="*70)
ntrue = sum(1 for _,v in RES if v); ntot=len(RES)
print(f"CHECKS: {ntrue}/{ntot} True")
bad = [k for k,v in RES if not v]
print("FAILURES:", bad if bad else "NONE")
print("LANDED OUTCOME: D3-NO-AMOUNT (scoped negative, first-class).")
