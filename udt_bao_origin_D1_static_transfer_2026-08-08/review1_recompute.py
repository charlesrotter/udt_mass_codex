#!/usr/bin/env python3
"""ADVERSARIAL REVIEW 1 — independent recompute for D1 (static transfer function).
Written BEFORE opening derive_d1.py. Own Christoffel/Ricci code, own checks.
Keys prefixed R1_. Run: timeout 480 python3 -u review1_recompute.py
"""
import sympy as sp

results = []
def key(name, val):
    results.append((name, bool(val)))
    print(f"R1 {name:55s} {bool(val)}")

t, r, th, ph, lam = sp.symbols('t r theta phi lambda', real=True)
Rw, n, E, L, z, s, gam, K = sp.symbols('R_w n E L z s gamma K', positive=True)

# ---------------- Part A: geometry, generic A(r) ----------------
A = sp.Function('A')(r)
g = sp.diag(-A, 1/A, r**2, r**2*sp.sin(th)**2)
ginv = g.inv()
x = [t, r, th, ph]

def christoffel(g, ginv, x):
    N = 4
    Gam = [[[sp.S(0)]*N for _ in range(N)] for _ in range(N)]
    for a in range(N):
        for b in range(N):
            for c in range(N):
                expr = sp.S(0)
                for d in range(N):
                    expr += ginv[a, d]*(sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b]) - sp.diff(g[b, c], x[d]))
                Gam[a][b][c] = sp.simplify(expr/2)
    return Gam

Gam = christoffel(g, ginv, x)

def ricci(Gam, x):
    N = 4
    Ric = sp.zeros(N, N)
    for b in range(N):
        for c in range(N):
            expr = sp.S(0)
            for a in range(N):
                expr += sp.diff(Gam[a][b][c], x[a]) - sp.diff(Gam[a][b][a], x[c])
                for d in range(N):
                    expr += Gam[a][a][d]*Gam[d][b][c] - Gam[a][c][d]*Gam[d][b][a]
            Ric[b, c] = sp.simplify(expr)
    return Ric

Ric = ricci(Gam, x)

# 1(c) KEY THEOREM: R_tt + A^2 R_rr == 0 for GENERIC A(r)
key("Rtt_plus_A2_Rrr_identically_zero_generic_A", sp.simplify(Ric[0, 0] + A**2*Ric[1, 1]) == 0)

# consequence: radial null k = (E/A, ±E, 0, 0): R_mn k^m k^n = 0 exactly
kvec = [E/A, E, 0, 0]
Rkk = sp.simplify(sum(Ric[i, j]*kvec[i]*kvec[j] for i in range(4) for j in range(4)))
key("radial_null_Ricci_focusing_zero", Rkk == 0)
kvec_in = [E/A, -E, 0, 0]
Rkk2 = sp.simplify(sum(Ric[i, j]*kvec_in[i]*kvec_in[j] for i in range(4) for j in range(4)))
key("ingoing_radial_null_Ricci_focusing_zero", Rkk2 == 0)

# sanity: the identity is NOT vacuous — R_tt itself is generically nonzero
key("Rtt_generically_nonzero_identity_not_vacuous", sp.simplify(Ric[0, 0]) != 0)

# radial null ray (tdot, rdot) = (E/A, -E) solves the geodesic equation with r affine
tdot, rdot = E/A, -E
geo_t = sp.simplify(sp.diff(tdot, r)*rdot + Gam[0][0][1]*tdot*rdot + Gam[0][1][0]*rdot*tdot)
geo_r = sp.simplify(sp.diff(rdot, r)*rdot + Gam[1][0][0]*tdot**2 + Gam[1][1][1]*rdot**2)
nullcond = sp.simplify(-A*tdot**2 + rdot**2/A)
key("radial_null_geodesic_r_affine", geo_t == 0 and geo_r == 0 and nullcond == 0)

print("stage: Part A generic-A geometry done", flush=True)

# ---------------- Part B: turning point + class-(i) dictionary ----------------
Ai = (1 - r/Rw)**n   # class-(i) profile

# G1: A(0) = 1
key("class_i_A0_equals_1", sp.simplify(Ai.subs(r, 0)) == 1)

# G2: proper-radius integrand expansion 1 + n r/(2Rw) + O(r^2)
integrand = sp.series(Ai**sp.Rational(-1, 2), r, 0, 2).removeO()
key("center_locally_flat_integrand", sp.simplify(integrand - (1 + n*r/(2*Rw))) == 0)

# 1(a) turning point: null radial potential rdot^2 = E^2 - A L^2 / r^2
# my restatement: r^2 * rdot^2 -> -L^2 as r->0 (generic A with A(0)=1), so rdot^2 -> -inf for L != 0
pot = E**2 - Ai*L**2/r**2
val = sp.limit(r**2*pot, r, 0, '+')
key("turning_point_r2rdot2_to_minus_L2", sp.simplify(val + L**2) == 0)
# and the turning radius is strictly positive: near r=0, pot < 0 (evaluate at small r symbolically)
# pot < 0 iff r^2 E^2 < A L^2 ; at r=0 rhs = L^2 > 0 = lhs -> strict inequality holds in a neighborhood
# (cancel the r^2 first: r^2*pot = E^2 r^2 - A L^2, regular at r=0)
key("pot_negative_at_center_strict", sp.simplify(sp.expand(r**2*pot).subs(r, 0) + L**2) == 0)

# my own derivation of the potential from the null condition + conserved E, L (equatorial):
# ds^2=0: -E^2/A + rdot^2/A + L^2/r^2 = 0  => rdot^2 = E^2 - A L^2/r^2. Verify directly:
rdotsq = sp.symbols('rdotsq')
eqn = -E**2/Ai + rdotsq/Ai + L**2/r**2
sol2 = sp.solve(sp.Eq(eqn, 0), rdotsq)[0]
key("radial_potential_exact_form", sp.simplify(sol2 - (E**2 - Ai*L**2/r**2)) == 0)

# G7: 1+z = A^(-1/2); inversion r(z) = Rw (1 - (1+z)^(-2/n)); check A(r(z)) = (1+z)^(-2)
rz = Rw*(1 - (1 + z)**(-2/n))
Aof = sp.powsimp(Ai.subs(r, rz))
key("depth_dictionary_A_of_rz", sp.simplify(sp.log(Aof) - sp.log((1 + z)**(-2))) == 0 or sp.simplify(Aof - (1 + z)**(-2)) == 0)

# G8: dr/dz closed form and positivity
drdz = sp.simplify(sp.diff(rz, z))
target = (2*Rw/n)*(1 + z)**(-2/n - 1)
key("drdz_closed_form", sp.simplify(drdz - target) == 0)
key("drdz_positive", sp.ask(sp.Q.positive(target), sp.Q.positive(Rw) & sp.Q.positive(n) & sp.Q.positive(z))
    or bool(target.subs({Rw: 3, n: sp.Rational(3, 2), z: sp.Rational(1, 2)}) > 0) and all(
        target.subs({Rw: a, n: b, z: c}) > 0 for a in [1, 5] for b in [sp.Rational(1, 2), 1, 3] for c in [0, 1, 10]))

# r(z) > 0 for z > 0, n > 0: (1+z)^(-2/n) < 1 <=> log-value = (-2/n) log(1+z) < 0.
# machine-decidable pieces: log(1+z) > 0 for z > 0; -2/n < 0 for n > 0; product of pos*neg < 0.
zz, nn = sp.symbols('zz nn', positive=True)
lg = sp.log(1 + zz)                     # zz > 0 => argument > 1 => log > 0
piece1 = sp.ask(sp.Q.positive(lg))
piece2 = sp.ask(sp.Q.negative(-2/nn))
key("rz_positive_for_z_positive", bool(piece1) and bool(piece2))

print("stage: Part B class-(i) dictionary done", flush=True)

# ---------------- Part C: statistics of the transfer map ----------------
lamb, kap, x1, u, W, a = sp.symbols('lambda_s kappa x1 u W a', positive=True)

# K3: scale-covariance ODE s C' = kappa C has power-law solutions; and power laws are scale-covariant
C = sp.Function('C')
odesol = sp.dsolve(sp.Eq(s*sp.Derivative(C(s), s), kap*C(s)), C(s))
key("scalefree_ODE_solution_is_powerlaw", odesol.rhs.has(s**kap))
Cpow = K*s**(-gam)
key("powerlaw_is_scale_covariant", sp.simplify(Cpow.subs(s, lamb*s)/Cpow - lamb**(-gam)) == 0)

# K4 (T1 per shell): w(theta) = C(r_s * theta) for power-law C has constant log-slope -gamma
rs, theta = sp.symbols('r_s theta', positive=True)
wobs = K*(rs*theta)**(-gam)
logslope = sp.simplify(sp.diff(sp.log(wobs), theta)*theta)
key("per_shell_logslope_constant_minus_gamma", sp.simplify(logslope + gam) == 0)

# K8 (as an operator statement): weighted sum of same-index power laws is a power law
w1, w2 = sp.symbols('w1 w2', positive=True)
r1s, r2s = sp.symbols('r1s r2s', positive=True)
binsum = w1*(r1s*theta)**(-gam) + w2*(r2s*theta)**(-gam)
ls2 = sp.simplify(sp.diff(sp.log(binsum), theta)*theta)
key("same_shell_superposition_powerlaw", sp.simplify(ls2 + gam) == 0)

# K8b Limber: integral over full line of sight of xi(sqrt(D^2 + (rbar th)^2)), xi = sigma^-gam
rbar = sp.symbols('rbar', positive=True)
D = sp.symbols('D', real=True)
integ = ((D**2 + (rbar*theta)**2))**(-gam/2)
sub = integ.subs(D, rbar*theta*u)*rbar*theta   # dD = rbar*theta*du
sub = sp.powsimp(sp.simplify(sub))
key("limber_scaling_exponent_1_minus_gamma",
    sp.simplify(sub - (rbar*theta)**(1 - gam)*(1 + u**2)**(-gam/2)) == 0)
Iu = sp.integrate((1 + u**2)**(-sp.S(3)/2), (u, -sp.oo, sp.oo))  # gamma=3 witness of convergence
key("limber_u_integral_converges_gamma_gt_1_witness", Iu == 2)

# --- ATTACK WITNESS: FINITE z-bin w(theta) is NOT a pure power law (cross-shell pairs) ---
# top-hat proper window of half-width W at distance rbar; xi = sigma^-2 (gamma=2, exact integrable)
# pair-separation kernel: w_bin(a) ∝ Int_0^{2W} (2W - D) * (D^2 + a^2)^(-1) dD, a = rbar*theta
Dp = sp.symbols('Dp', positive=True)
wbin = sp.integrate((2*W - Dp)/(Dp**2 + a**2), (Dp, 0, 2*W))
wbin = sp.simplify(wbin)
ls_bin = sp.simplify(sp.diff(sp.log(wbin), a)*a)
slope_small = sp.limit(ls_bin, a, 0, '+')     # 3-D regime -> 1 - gamma = -1
slope_large = sp.limit(ls_bin, a, sp.oo)      # 2-D regime -> -gamma = -2
key("ATTACK_finite_bin_slope_small_angle_eq_1_minus_gamma", sp.simplify(slope_small + 1) == 0)
key("ATTACK_finite_bin_slope_large_angle_eq_minus_gamma", sp.simplify(slope_large + 2) == 0)
# hence log-slope is NOT constant: the binned w(theta) is NOT a pure power law -> K8 prose overreach
mid = ls_bin.subs(a, W)
key("ATTACK_finite_bin_logslope_nonconstant", sp.simplify(mid + 1) != 0 and sp.simplify(mid + 2) != 0)
# the transition scale is theta ~ W/rbar: WINDOW-set (tracer selection), not an A(r) scale.
# check: wbin depends on (a, W) only -> no metric symbol enters; the metric enters only via a = rbar*theta
key("ATTACK_transition_scale_is_window_set", (wbin.free_symbols == {a, W}))

print("stage: Part C statistics + attack witness done", flush=True)

# ---------------- Part D: T2 / T4 / T5 ----------------
# T2: theta(z; s) = s / r(z); monotone, no critical point
thz = s/rz
dthdz = sp.simplify(sp.diff(thz, z))
# dtheta/dz = -s r'/r^2 ; sign = -(positive)/(positive) < 0 given r > 0 (proven) and r' > 0 (proven)
key("T2_dthetadz_identity", sp.simplify(dthdz + s*drdz/rz**2) == 0)
# high-z floor: q = (1+z)^(-2/n) -> 0 (exponent -2/n < 0), theta -> s/Rw
q = sp.symbols('q', positive=True)
th_q = s/(Rw*(1 - q))
key("T2_highz_floor", sp.simplify(th_q.subs(q, 0) - s/Rw) == 0 and bool(sp.ask(sp.Q.negative(-2/nn))))

# T4: value preservation at fixed proper separation; fixed-angle amplitude law
w_at_fixed_s = (K*s**(-gam)).subs(s, rz*(s/rz))       # theta = s/r(z) probes proper sep s
key("T4_value_preserving", sp.simplify(w_at_fixed_s - K*s**(-gam)) == 0)
w_fixed_angle = K*(rz*theta)**(-gam)
dwdz = sp.simplify(sp.diff(w_fixed_angle, z))
# dw/dz = -gam * w * r'/r < 0 : identity check
key("T4_fixed_angle_falling_identity", sp.simplify(dwdz + gam*w_fixed_angle*drdz/rz) == 0)

# T5: radial leg. z(r) = (1-r/Rw)^(-n/2) - 1 ; lp(r) closed form; J(z) = dz/dlp
zr = (1 - r/Rw)**(-n/2) - 1
lp = (2*Rw/(2 - n))*(1 - (1 - r/Rw)**((2 - n)/2))     # n != 2 branch
# positivity substitution r = Rw - xpos (interior: 0 < xpos < Rw) so symbolic powers collapse
xpos = sp.symbols('xpos', positive=True)
def interior(e):
    return sp.simplify(sp.powsimp(e.subs(r, Rw - xpos), force=False))
key("T5_lp_closed_form_by_differentiation", interior(sp.diff(lp, r) - Ai**sp.Rational(-1, 2)) == 0)
key("T5_lp_zero_at_center", sp.simplify(lp.subs(r, 0)) == 0)
# wall value for n<2: (1-r/Rw)^((2-n)/2) -> 0 at r=Rw since exponent m/2 with m=2-n>0
m = sp.symbols('m', positive=True)
key("T5_wall_value_restatement_0_pow_pos_is_0", sp.limit(sp.symbols('eps', positive=True)**(m/2), sp.symbols('eps', positive=True), 0, '+') == 0)

# J = dz/dlp = (dz/dr)/(dlp/dr); closed forms
J = sp.simplify(sp.diff(zr, r)/sp.diff(lp, r))
J_target_r = (n/(2*Rw))/(1 - r/Rw)
key("T5_J_closed_form_in_r", sp.simplify(J - J_target_r) == 0)
# in z: (1+z)^(2/n) = (1-r/Rw)^(-1) exactly (interior substitution for the power collapse)
e_Jz = ((1 + zr)**(2/n) - 1/(1 - r/Rw)).subs(r, Rw - xpos)
key("T5_J_in_z", sp.simplify(sp.powsimp(e_Jz, force=True)) == 0)
# K17 identities: dz/dlp = -A'/(2A) = d(delta)/dr, delta = -(1/2) log A  — GENERIC A
Agen = sp.Function('A')(r)
lhs_gen = -sp.diff(Agen, r)/(2*Agen)
delta = -sp.log(Agen)/2
key("T5_K17_generic_identity", sp.simplify(lhs_gen - sp.diff(delta, r)) == 0)
key("T5_K17_class_i_matches_J", sp.simplify((-sp.diff(Ai, r)/(2*Ai)) - J_target_r) == 0)
# J growing with depth: dJ/dr = n/(2 (Rw - r)^2) > 0 (identity + interior positivity), r increasing with z (proven)
dJdr = sp.simplify(sp.diff(J_target_r, r))
key("T5_J_growing", sp.simplify(dJdr - n/(2*(Rw - r)**2)) == 0
    and bool(sp.ask(sp.Q.positive(dJdr.subs(r, Rw - xpos)))))

# no-extremum: dw/dz2 = C'(lp2 - lp1) * dlp/dz2 ; dlp/dz = 1/J > 0; C' < 0 for falling input
key("T5_no_extremum_sign_product", bool(sp.ask(sp.Q.positive(1/((nn/(2*Rw))*(1 + zz)**(2/nn))))))

# K22: bend scale — my own series. dlp/dz = (2Rw/n)(1+z)^(-2/n)
z1, dz = sp.symbols('z1 Delta_z', positive=True)
lpz = lambda Z: (2*Rw/(2 - n))*(1 - (1 + Z)**(-(2 - n)/n))   # lp as function of z: (1-r/Rw) = (1+z)^(-2/n)
# check lp(z) form first: substitute r(z)
key("T5_lp_of_z_form", sp.simplify(lpz(z) - lp.subs(r, rz)) == 0)
dlp_fin = lpz(z1 + dz) - lpz(z1)
ratio = sp.simplify(dz*sp.diff(dlp_fin, dz)/dlp_fin)
ser = sp.series(ratio, dz, 0, 2).removeO()
key("T5_K22_bend_scale_n_times_1plusz", sp.simplify(ser - (1 - dz/(n*(1 + z1)))) == 0)

# K23: angular dictionary log-slope identically 1 (all orders)
softh = rs*theta
key("T5_K23_angular_logslope_exactly_1", sp.simplify(sp.diff(sp.log(softh), theta)*theta) == 1)

# G5 restatement equivalence (gruntz amendment audit): r^2*rdot^2 -> -L^2  <=>  rdot^2 -> -oo
# formal: rdot^2 = (r^2 rdot^2)/r^2 ; numerator -> -L^2 < 0, denominator -> 0+  => -> -oo. Witness:
key("G5_restatement_equiv_witness", sp.limit((-L**2 + E**2*r**2)/r**2, r, 0, '+') == -sp.oo)

nfail = sum(1 for _, v in results if not v)
print(f"\nR1 CHECKS: {sum(v for _, v in results)} / {len(results)} True ({nfail} False)")
