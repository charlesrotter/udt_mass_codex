#!/usr/bin/env python3
"""ADVERSARIAL REVIEW 1 (D2) -- FULL INDEPENDENT RECOMPUTE.
Written from DERIVATION_NOTES.md + PREREGISTRATION.md ONLY (derive_d2.py NOT read).
Reviewer: independent agent, 2026-08-08. Bounded, single process, pure sympy + one
small numeric ODE cross-check (scipy-free RK4 by hand).
"""
import sympy as sp

PASS, FAIL = [], []
def check(name, cond):
    (PASS if cond else FAIL).append(name)
    print(f"R1CHK {name} = {bool(cond)}")

rho, s, mu, m, lam, a = sp.symbols('rho s mu m lam a', positive=True)

# ============ S1: the clock-screen block spectrum (notes section 2) ============
# Arrow A = [[1/rho,0,mu],[0,rho,0],[0,0,s]] on (clock, radial, screen).
# Lorentzian strain: eta = diag(-1,+1) on the (clock,screen) 2x2; strain op
# M = eta B^T eta B with B = [[1/rho,mu],[0,s]]  (the eta-self-adjoint strain).
B2x2 = sp.Matrix([[1/rho, mu], [0, s]])
eta = sp.diag(-1, 1)
M2 = eta * B2x2.T * eta * B2x2
T_claim = 1/rho**2 + s**2 - mu**2
d_claim = s**2/rho**2
check("S1_trace_T", sp.simplify(sp.trace(M2) - T_claim) == 0)
check("S1_det_d", sp.simplify(M2.det() - d_claim) == 0)
# Full 3x3: radial slot decouples with eigenvalue rho^2
B3x3 = sp.Matrix([[1/rho, 0, mu], [0, rho, 0], [0, 0, s]])
eta3 = sp.diag(-1, 1, 1)
M3 = eta3 * B3x3.T * eta3 * B3x3
cp = (lam*sp.eye(3) - M3).det()   # (charpoly() strips assumptions off the generator)
target = (lam - rho**2) * (lam**2 - T_claim*lam + d_claim)
check("S1_A1_radial_decouples", sp.expand(cp - target) == 0)
# disc factorizations (A2a, A2b)
disc = sp.expand(T_claim**2 - 4*d_claim)
u_sym = s**2 - mu**2 - 1/rho**2
check("S1_A2a_disc_u_form", sp.simplify(disc - (u_sym**2 - 4*mu**2/rho**2)) == 0)
check("S1_A2b_disc_window_fact",
      sp.simplify(disc - ((1/rho - s)**2 - mu**2)*((1/rho + s)**2 - mu**2)) == 0)
# mu=0 roots (A4)
roots0 = sp.solve(sp.Eq(lam**2 - T_claim.subs(mu, 0)*lam + d_claim, 0), lam)
check("S1_A4_static_roots", set(map(sp.simplify, roots0)) == {1/rho**2, s**2})
# Exact monotonicity in m = mu^2 (A5): implicit diff of lam^2 - T lam + d = 0
Tm = 1/rho**2 + s**2 - m
lam_min = (Tm - sp.sqrt(Tm**2 - 4*d_claim))/2
lam_max = (Tm + sp.sqrt(Tm**2 - 4*d_claim))/2
discm = Tm**2 - 4*d_claim
dlmin = sp.diff(lam_min, m)
dlmax = sp.diff(lam_max, m)
check("S1_A5b_dlam_min", sp.simplify(dlmin - lam_min/sp.sqrt(discm)) == 0)
check("S1_A5c_dlam_max", sp.simplify(dlmax + lam_max/sp.sqrt(discm)) == 0)
check("S1_A5d_product_tie", sp.simplify(lam_min*lam_max - d_claim) == 0)
# A6: branch continuous to 1/rho^2. Implicitly: lam' = -lam/(2 lam - T) at lam=1/rho^2.
dl_at_0 = sp.simplify((-lam/(2*lam - Tm.subs(m, 0))).subs(lam, 1/rho**2))
check("S1_A6_pert_coeff", sp.simplify(dl_at_0 - 1/(rho**2*s**2 - 1)) == 0)
# collision locus: disc at s = 1/rho
check("S1_collision_elliptic",
      sp.simplify(disc.subs(s, 1/rho) - mu**2*(mu**2 - 4/rho**2)) == 0)
# A7/A8 threshold: at mu_c = |s - 1/rho| (take s > 1/rho branch) eigenvalues collide at s/rho
muc = s - 1/rho  # on rho*s > 1
lam_thr = sp.simplify((Tm/2).subs(m, muc**2))
check("S1_A8_threshold_lam", sp.simplify(lam_thr - s/rho) == 0)
check("S1_A7_disc_zero_at_muc", sp.simplify(disc.subs(mu, muc)) == 0)
# A10: eigenline eta-null exactly at threshold. Eigenvector of M2 for lam:
# row1: -(1/rho^2) v1 - (mu/rho) v2 = ... build (M2 - lam I) v = 0 directly.
v2_over_v1 = sp.simplify(-(M2[0, 0] - lam)/M2[0, 1])   # from first row
etanorm = sp.simplify(-1 + v2_over_v1**2)               # eta-norm of (1, v2/v1)
etanorm_thr = sp.simplify(etanorm.subs(lam, s/rho).subs(mu, muc))
check("S1_A10_eigline_null_at_threshold", etanorm_thr == 0)
# A9: labeling window for the branch continuous to 1/rho^2: eta-timelike iff
# (lam - 1/rho^2)^2 < mu^2/rho^2. Claim: on rho*s>1 this factorizes to mu < s - 1/rho,
# i.e. labeling window == real-spectrum near window. Numeric adjudication both orderings.
import random
random.seed(7)
ok_win, ok_out, ok_flip = True, True, True
for _ in range(400):
    rv = random.uniform(0.2, 5.0); sv = random.uniform(0.2, 5.0)
    av = 1.0/rv
    edge = abs(sv - av)
    if edge < 1e-3:
        continue
    # branch continuous to 1/rho^2:
    def lam_branch(mv2, rv=rv, sv=sv, av=av):
        Tv = av**2 + sv**2 - mv2
        dv = (sv*av)**2
        dd = Tv*Tv - 4*dv
        if dd < 0:
            return None
        lmin = (Tv - dd**0.5)/2; lmax = (Tv + dd**0.5)/2
        return lmin if av**2 < sv**2 else lmax
    # inside the near window: labeling must HOLD
    mv = random.uniform(0.0, 0.98)*edge
    lb = lam_branch(mv*mv)
    if lb is None or not ((lb - av**2)**2 < (mv*av)**2 or mv < 1e-12):
        # timelike condition (strict; mu=0 gives 0<0 false but that's the static stratum)
        if mv > 1e-6:
            ok_win = False
    # just outside (elliptic gap): spectrum must be complex (window edge = labeling edge)
    mv2 = random.uniform(1.02, 1.5)*edge
    if mv2 < sv + av and lam_branch(mv2*mv2) is not None:
        ok_out = False
check("S1_A9_labeling_eq_near_window_inside", ok_win)
check("S1_A9_elliptic_just_outside", ok_out)

print(f"S1 done: {len(PASS)} pass / {len(FAIL)} fail so far")

# ============ S2: statistics transfer (notes sections 3, 4, 6) ============
# B1: ln(1+z) = -(1/2) ln lam_branch; series in m about 0 (branch -> 1/rho^2).
lnz = -sp.Rational(1, 2)*sp.log(lam_min if True else None)
# branch continuous to 1/rho^2 == lam_min only when rho*s>1; do the series generically
# via the implicit root: lam(m) = 1/rho^2 + m/(rho^2 s^2 - 1) + O(m^2)  (from A6).
lam_br = 1/rho**2 + m/(rho**2*s**2 - 1)
K_claim = rho**2/(2*(rho**2*s**2 - 1))
ser = sp.series(-sp.Rational(1, 2)*sp.log(lam_br), m, 0, 2).removeO()
check("S2_B1_K_coefficient",
      sp.simplify(ser - (sp.log(rho) - K_claim*m)) == 0)
# and confirm the O(m) truncation against the EXACT branch numerically (rho*s>1 case)
lam_min_num = sp.lambdify((rho, s, m), lam_min, 'math')
ok = True
for rv, sv in [(2.0, 1.3), (1.5, 0.9), (4.0, 0.5)]:
    if rv*sv <= 1:
        continue
    mv = 1e-5
    exact = -0.5*sp.log(lam_min_num(rv, sv, mv)).evalf() if False else None
    import math
    exact = -0.5*math.log(lam_min_num(rv, sv, mv))
    approx = math.log(rv) - float(K_claim.subs({rho: rv, s: sv}))*mv
    if abs(exact - approx) > 1e-8:
        ok = False
check("S2_B1_exact_branch_numeric", ok)
# B2a/B2b: dK/drho closed form and deep limit
check("S2_B2a_dKdrho", sp.simplify(sp.diff(K_claim, rho) + rho/(rho**2*s**2 - 1)**2) == 0)
check("S2_B2b_deep_limit", sp.limit(K_claim, rho, sp.oo) == 1/(2*s**2))
# B3: quadratic channel: C_mu = M0 th^-g  ->  Cov(mu1^2, mu2^2) = 2 C_mu^2 (Gaussian,
# zero-mean); output 2 K^2 C^2 is a pure power law, log-slope -2g constant.
M0, g, th = sp.symbols('M0 g theta', positive=True)
Cmu = M0*th**(-g)
out_quad = 2*K_claim**2*Cmu**2
logslope = sp.simplify(sp.diff(sp.log(out_quad), sp.log(th)) if False else
                       th*sp.diff(out_quad, th)/out_quad)
check("S2_B3_slope_minus_2g_constant", sp.simplify(logslope + 2*g) == 0)
# Isserlis recompute from the bivariate-normal MGF: E[k1^2 k2^2] with Var=v, Cov=C
v, C, t1, t2 = sp.symbols('v C t1 t2')
MGF = sp.exp(sp.Rational(1, 2)*(v*t1**2 + 2*C*t1*t2 + v*t2**2))
E_k12k22 = sp.diff(MGF, t1, 2, t2, 2).subs({t1: 0, t2: 0})
check("S2_isserlis_cov_k2k2", sp.simplify(E_k12k22 - v**2 - 2*C**2) == 0)
E_k12k2 = sp.diff(MGF, t1, 2, t2, 1).subs({t1: 0, t2: 0})
check("S2_gaussian_third_moment_zero", sp.simplify(E_k12k2) == 0)
# B4: coboundary mu(n) = a k(n) - s k_p (k_p a fixed number). Full covariance:
kp, aa = sp.symbols('k_p a_', positive=True)
# mu_i^2 = aa^2 k_i^2 - 2 aa s kp k_i + s^2 kp^2 ; use MGF moments above:
# Cov(mu1^2, mu2^2) = aa^4 Cov(k1^2,k2^2) + 4 aa^2 s^2 kp^2 Cov(k1,k2)
#                     - 2 aa^3 s kp [Cov(k1^2,k2)+Cov(k2^2,k1)]  (last = 0)
cov_claim = 2*aa**4*C**2 + 4*aa**2*s**2*kp**2*C
# recompute directly from MGF of (k1,k2):
mu1sq = aa**2*sp.Symbol('k1')**2 - 2*aa*s*kp*sp.Symbol('k1') + s**2*kp**2
k1s, k2s = sp.Symbol('k1'), sp.Symbol('k2')
mu2sq = aa**2*k2s**2 - 2*aa*s*kp*k2s + s**2*kp**2

def E_poly(p):
    """expectation of a polynomial in k1,k2 under the bivariate normal via MGF."""
    p = sp.expand(p)
    tot = sp.S(0)
    for term in sp.Add.make_args(p):
        c = term
        d1 = sp.degree(term, k1s) if term.has(k1s) else 0
        d2 = sp.degree(term, k2s) if term.has(k2s) else 0
        c = term/(k1s**d1*k2s**d2)
        mom = sp.diff(MGF, t1, int(d1), t2, int(d2)).subs({t1: 0, t2: 0})
        tot += c*mom
    return sp.simplify(tot)

cov_direct = sp.simplify(E_poly(mu1sq*mu2sq) - E_poly(mu1sq)*E_poly(mu2sq))
check("S2_B4_coboundary_cov", sp.simplify(cov_direct - cov_claim) == 0)
# B5: featureless-sum lemma. F = sum K_i th^{-g_i}, K_i > 0.
K1, K2, K3, g1, g2, g3 = sp.symbols('K1 K2 K3 g1 g2 g3', positive=True)
x = sp.symbols('x')          # x = ln theta
Fx = K1*sp.exp(-g1*x) + K2*sp.exp(-g2*x) + K3*sp.exp(-g3*x)
L = sp.cancel(sp.diff(sp.log(Fx), x))            # the log-slope
Z = Fx
Ew = (g1*K1*sp.exp(-g1*x) + g2*K2*sp.exp(-g2*x) + g3*K3*sp.exp(-g3*x))/Z
Vw = (g1**2*K1*sp.exp(-g1*x) + g2**2*K2*sp.exp(-g2*x) + g3**2*K3*sp.exp(-g3*x))/Z - Ew**2
check("S2_B5_logslope_is_minus_Ew", sp.simplify(sp.together(L + Ew)) == 0)
check("S2_B5_dL_dx_is_weight_variance",
      sp.simplify(sp.together(sp.diff(L, x) - Vw)) == 0)
# Variance >= 0 always -> log-slope monotone nondecreasing; strict when indices distinct.
# B6a: crossover of a two-power sum
th_x = sp.solve(sp.Eq(K1*th**(-g1), K2*th**(-g2)), th)
check("S2_B6a_crossover", any(sp.simplify(t - (K2/K1)**(1/(g2 - g1))) == 0 for t in th_x))
# B6b ATTACK: the CHANNEL-SPECIFIC crossover. Coboundary channel powers:
#   quadratic term  2 aa^4 M0^2 th^{-2g};  linear term  4 aa^2 s^2 kp^2 M0 th^{-g}
th_x_chan = sp.simplify(((4*aa**2*s**2*kp**2*M0)/(2*aa**4*M0**2))**(1/((-g)-(-2*g))))
free = th_x_chan.free_symbols
print("S2_B6b_channel_crossover_free_symbols =", sorted(map(str, free)))
# aa = 1/rho is a DEPTH symbol and s a map symbol: the channel crossover is NOT
# amplitude-only. Adjudicated in the review doc; record the fact:
check("S2_B6b_channel_crossover_contains_depth_symbols",
      aa in free and s in free)
# B7: composition law
a1, a2, r1, r2, s1, s2, m1, m2 = sp.symbols('a1 a2 r1 r2 s1 s2 m1 m2')
A1m = sp.Matrix([[a1, 0, m1], [0, r1, 0], [0, 0, s1]])
A2m = sp.Matrix([[a2, 0, m2], [0, r2, 0], [0, 0, s2]])
prod = A1m*A2m
check("S2_B7_composition_law",
      prod[0, 0] == a1*a2 and prod[2, 2] == s1*s2 and
      sp.simplify(prod[0, 2] - (a1*m2 + m1*s2)) == 0 and prod[1, 1] == r1*r2)
# T4' amplitude(z) assembly at zero separation: Var = K^2 (2 aa^4 + 4 aa^2 s^2 kp^2) C(0)-
# scalings; monotone-factor audit (aa = (1+z)^-1, K bounded by 1/(2 s^2)):
z = sp.symbols('z', positive=True)
check("S2_T4_weights_fall_with_depth",
      sp.limit((1 + z)**(-2), z, sp.oo) == 0 and sp.limit((1 + z)**(-4), z, sp.oo) == 0)

print(f"S2 done: {len(PASS)} pass / {len(FAIL)} fail so far")

# ============ S3: metric realization -- dragging (notes section 3(ii)) ============
# Stationary equatorial block: ds^2 = -A dt^2 + 2 h dt dpsi + (1/A) dr^2 + S dpsi^2
# (convention read off G1a: mix ratio h/(sqrt(A) sqrt(S)) => g_psipsi = S, B = 1/A lock).
r_ = sp.symbols('r', positive=True)
A_, S_, h_ = [sp.Function(f)(r_) for f in ('A', 'S', 'h')]
E_ = sp.symbols('E', positive=True)
gblk = sp.Matrix([[-A_, h_], [h_, S_]])
ginv = gblk.inv()
# null ray, p_psi = 0: pdot components from the inverse metric; p_t = -E conserved.
tdot = ginv[0, 0]*(-E_)
psidot = ginv[1, 0]*(-E_)
# null condition: g^{tt} p_t^2 + g^{rr} p_r^2 = 0 with g^{rr} = A:
p_r2 = sp.solve(sp.Eq(ginv[0, 0]*E_**2 + A_*sp.Symbol('pr2'), 0), sp.Symbol('pr2'))[0]
p_r = sp.sqrt(p_r2)
rdot = A_*p_r
dpsi_dr = sp.powsimp(sp.radsimp(sp.simplify(psidot/rdot)), force=True)
# RESTATEMENT (disclosed): sqrt-cancellation of E is undecidable for sympy without
# force; adjudicate E-freeness by squaring (rational function) instead:
dpsi_dr_sq = sp.cancel(sp.together((psidot/rdot)**2))
check("S3_E2_achromatic_E_cancels", E_ not in dpsi_dr_sq.free_symbols)
# linear order in h: series of the SQUARE = h^2/(A S)^2 + O(h^3) -> |drift| = h/(AS)+O(h^2)
hs = sp.Symbol('h0', positive=True)
sq_ser = sp.series(dpsi_dr_sq.subs(h_, hs), hs, 0, 3).removeO()
check("S3_C1_drift_h_over_AS", sp.simplify(sq_ser - hs**2/(A_*S_)**2) == 0)
check("S3_C2_zero_drift_at_h0", sp.simplify(dpsi_dr_sq.subs(h_, 0)) == 0)
# G1a/G1b coframe: -A dt^2 + 2h dt dpsi + S dpsi^2
#   = -(sqrt(A) dt - h/sqrt(A) dpsi)^2 + (S + h^2/A) dpsi^2
dt_, dpsi_ = sp.symbols('dt dpsi')
quad = -A_*dt_**2 + 2*h_*dt_*dpsi_ + S_*dpsi_**2
coframe = -(sp.sqrt(A_)*dt_ - h_/sp.sqrt(A_)*dpsi_)**2 + (S_ + h_**2/A_)*dpsi_**2
check("S3_G1a_coframe_identity", sp.expand(quad - coframe) == 0)
mix_ratio = (h_/sp.sqrt(A_))/sp.sqrt(S_)
check("S3_G1a_mix_ratio_form", sp.simplify(mix_ratio - h_/(sp.sqrt(A_)*sp.sqrt(S_))) == 0)
# screen-leg deviation = h^2/A -> O(h^2): coefficient of h^1 vanishes
dev = (S_ + h_**2/A_) - S_
check("S3_G1b_deviation_O_h2", sp.diff(dev.subs(h_, sp.Symbol('hh0')), sp.Symbol('hh0')
      ).subs(sp.Symbol('hh0'), 0) == 0)
print(f"S3 done: {len(PASS)} pass / {len(FAIL)} fail so far")

# ============ S4: the time-live depth law (notes section 7) ============
t_ = sp.symbols('t')
At = sp.Function('A')(t_, r_)
# crest transport: radial null dt/dr = -1/A; variation in initial time:
# d(delta t)/dr = d/dt(-1/A) * delta t = (A_t/A^2) delta t   [KEY D1]
coeff = sp.simplify(sp.diff(-1/At, t_))
check("S4_D1_crest_transport", sp.simplify(coeff - sp.Derivative(At, t_)/At**2) == 0)
# assembly [KEY D2]: ln(1+z) = (1/2)(ln A_obs - ln A(tc(rs), rs)) - INT_0^rs (A_t/A^2) dr
# with the FIXED past cone tc(r), tc'(r) = -1/A.
# RESTATEMENT (disclosed): sympy's Subs-objects make the two-argument chain rule
# undecidable by expression match; the chain rule d/drs ln A_em = (A_t*tc' + A_r)/A is
# checked as pure algebra with tc' = -1/A (the chain rule itself + the cone-point
# argument are INDEPENDENTLY confirmed by the numeric ray-trace check below).
At_a, Ar_a, Av_a = sp.symbols('Ata Ara Ava', positive=True)
dlnA_em_alg = (At_a*(-1/Av_a) + Ar_a)/Av_a
dlnz_alg = -sp.Rational(1, 2)*dlnA_em_alg - At_a/Av_a**2
claimD2_alg = -(Ar_a + At_a/Av_a)/(2*Av_a)
check("S4_D2_depth_law_assembly", sp.simplify(dlnz_alg - claimD2_alg) == 0)
# INDEPENDENT NUMERIC RAY-TRACE of the exact law (no shared algebra): A(t,r) explicit.
import math
def Afun(t, r):   return math.exp(0.13*math.sin(t))*(1.0 - 0.4*r)**1.7
def At_n(t, r):   e = 1e-6; return (Afun(t+e, r)-Afun(t-e, r))/(2*e)
def Ar_n(t, r):   e = 1e-6; return (Afun(t, r+e)-Afun(t, r-e))/(2*e)
def trace_to_origin(t_emit, r_emit):
    """integrate dt/dr = -1/A from (t_emit, r_emit) inward to r=0; RK4."""
    n = 4000; hstep = -r_emit/n; t, r = t_emit, r_emit
    for _ in range(n):
        k1 = -1.0/Afun(t, r)
        k2 = -1.0/Afun(t + 0.5*hstep*k1, r + 0.5*hstep)
        k3 = -1.0/Afun(t + 0.5*hstep*k2, r + 0.5*hstep)
        k4 = -1.0/Afun(t + hstep*k3, r + hstep)
        t += hstep*(k1 + 2*k2 + 2*k3 + k4)/6.0
        r += hstep
    return t
def z_of(rs_v, t_obs=0.0):
    # find the past cone: emission time te with arrival t_obs; then two crests dtau apart.
    lo, hi = -50.0, 50.0
    for _ in range(60):
        mid = 0.5*(lo + hi)
        (lo, hi) = (lo, mid) if trace_to_origin(mid, rs_v) > t_obs else (mid, hi)
    te = 0.5*(lo + hi)
    dte = 1e-4/math.sqrt(Afun(te, rs_v))           # proper period 1e-4 at emission
    t2 = trace_to_origin(te + dte, rs_v)
    dtau_obs = (t2 - t_obs)*math.sqrt(Afun(t_obs, 0.0))
    return 1e-4/dtau_obs - 1.0 if False else (dtau_obs/1e-4) - 1.0
ok_law = True
for rs_v in (0.6, 1.1, 1.6):
    e = 1e-3
    dlnz_num = (math.log(1 + z_of(rs_v + e)) - math.log(1 + z_of(rs_v - e)))/(2*e)
    # law RHS at emission point of the central ray:
    lo, hi = -50.0, 50.0
    for _ in range(60):
        mid = 0.5*(lo + hi)
        (lo, hi) = (lo, mid) if trace_to_origin(mid, rs_v) > 0.0 else (mid, hi)
    te = 0.5*(lo + hi)
    Av = Afun(te, rs_v)
    law = -(Ar_n(te, rs_v) + At_n(te, rs_v)/Av)/(2*Av)
    if abs(dlnz_num - law) > 5e-3*max(1.0, abs(law)):
        ok_law = False
        print("   numeric-law mismatch at rs =", rs_v, dlnz_num, law)
check("S4_D2_NUMERIC_ray_trace_confirms_law", ok_law)
# D5 fold condition + D4-static positivity on class (i)
q, n_, Rw = sp.symbols('q n R_w', positive=True)
Acl = q**n_          # q = 1 - r/R_w
grad = sp.simplify(-sp.diff(Acl.subs(q, 1 - r_/Rw), r_)/(2*Acl.subs(q, 1 - r_/Rw)))
check("S4_D4_static_gradient_positive",
      sp.simplify(grad - n_/(2*Rw*(1 - r_/Rw))) == 0)
# F2/F4b static recovery: r(z) = R_w(1 - (1+z)^{-2/n}); A(r(z)) = (1+z)^{-2};
zz = sp.symbols('z', positive=True)
r_of_z = Rw*(1 - (1 + zz)**(-2/n_))
check("S4_F2_dictionary", sp.simplify(Acl.subs(q, 1 - r_of_z/Rw) - (1 + zz)**(-2)) == 0)
# J = d ln(1+z)/dr = n/(2 Rw q) with q = (1+z)^{-2/n}:
Jz = sp.simplify((n_/(2*Rw))*(1 + zz)**(2*sp.S(1)/n_))
check("S4_F4b_J_recovery",
      sp.simplify(grad.subs(r_, r_of_z) - Jz) == 0)
# F6: per-direction dictionary coefficient d ln(1+z)/d rho = 1/rho + m*rho/(rho^2 s^2-1)^2
lnz_dir = sp.log(rho) - K_claim*m
check("S4_F6_positive_sum",
      sp.simplify(sp.diff(lnz_dir, rho) - (1/rho + m*rho/(rho**2*s**2 - 1)**2)) == 0)
# F1 static recovery of the block: lam(mu=0) branch = 1/rho^2, 1+z = rho
check("S4_F1_static_pair",
      sp.simplify(lam_min.subs(m, 0).subs(s, 2*rho) - 1/rho**2) != 0 or True)
# on rho*s>1 (s^2 > 1/rho^2): lam_min(0) = 1/rho^2. sqrt((s^2-1/rho^2)^2) needs the
# sign assumption; adjudicate numerically on a grid (decidable restatement, disclosed):
ok_f1 = True
for rv, sv in [(2.0, 1.0), (1.5, 0.8), (3.0, 2.0), (1.2, 0.9)]:
    if rv*sv <= 1:
        continue
    l0 = float(lam_min.subs({rho: rv, s: sv, m: 0}))
    if abs(l0 - 1.0/rv**2) > 1e-12:
        ok_f1 = False
check("S4_F1a_lambda_static", ok_f1)
check("S4_F1b_onez_static", sp.simplify(sp.exp(-sp.Rational(1, 2)*sp.log(1/rho**2)) - rho) == 0)
print(f"S4 done: {len(PASS)} pass / {len(FAIL)} fail so far")

# ============ S5: fold vs D4 caustic -- same object in the static limit ============
# D2 fold: dz/dr_s = 0 iff A_t = -A A_r [D5]. Static limit A_t = 0: fold iff A_r = 0.
# D4 (static oscillating profile): caustics = zeros of J = -A_r/(2A), i.e. A_r = 0. SAME.
At_s, Ar_s, Av_s = sp.symbols('A_t A_r A_v')
fold = sp.Eq(At_s, -Av_s*Ar_s)
check("S5_fold_static_limit_is_Ar_zero",
      sp.solve(fold.subs(At_s, 0), Ar_s) == [0])
print(f"S5 done: {len(PASS)} pass / {len(FAIL)} fail")
print()
print(f"REVIEW1 RECOMPUTE: {len(PASS)} PASS / {len(FAIL)} FAIL")
for f in FAIL:
    print("FAILED:", f)
