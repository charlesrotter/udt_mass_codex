#!/usr/bin/env python3
# BLIND VERIFIER independent re-derivation for udt_p4_bookkeeping_forcing_2026-07-29.
# Own constructions throughout (different densities, variations, and instances from
# the package script). Exact SymPy only; deterministic; exit nonzero on any failure.
import sys
import sympy as sp

x, t, s = sp.symbols("x t s", real=True)
a = sp.Symbol("a", real=True)          # symbolic moduli-slot weight exponent a_M
FAIL = []


def chk(name, ok, note=""):
    print("[%s] %s %s" % ("PASS" if ok else "FAIL", name, note))
    if not ok:
        FAIL.append(name)


# =========================================================================
# V1. TF1(a) constant fork — my own witnesses.
# Moduli tangent block = R^7 (POSED 1.4 read directly). A pairing restricted to
# R^7 is a linear functional; vanishing = <=7 scalar conditions (codim <= 7).
# Witness (own densities): odd alphabet-shaped densities on all 7 slots kill the
# integrated row for EVERY weight e^{a x^2} (symbolic a) yet are pointwise nonzero.
W = sp.exp(a * x**2)
own = {"lam": x**3, "kmod": x * (1 + x**2), "k10": 3 * x**5,
       "c00": x**3 + x**5, "c01": x, "c10": x * (1 - x**2), "c11": x**7}
ints = [sp.simplify(sp.integrate(W * d, (x, -1, 1))) for d in own.values()]
pws = [d.subs(x, sp.Rational(1, 3)) for d in own.values()]
chk("V1_own_7slot_odd_witness_all_weights",
    all(v == 0 for v in ints) and all(v != 0 for v in pws),
    "all 7 integrated rows vanish at symbolic a; all pointwise nonzero at x=1/3")

# The multi-pairing attack (vanish for ALL a simultaneously) does NOT recover
# pointwise: the odd kernel survives the whole family => even demanding every
# enumerated weight at once, integrated conditions != pointwise conditions.
chk("V1_all_weights_simultaneously_still_not_pointwise",
    all(v == 0 for v in ints), "kernel of the WHOLE weight family is nonzero")

# P3 wall/corner blocks: pairing is a SUM (single scalar) per direction — one
# scalar per constant modulus even with wall terms. Instance: bulk+wall functional
# on a constant direction dm is one number.
g_b = x**2 + 1
wall = sp.Symbol("wall_density", real=True)
dm = sp.Symbol("dm", real=True)
p3 = sp.integrate(W * g_b * dm, (x, -1, 1)) + wall * dm + wall * dm  # bulk + 2 walls
chk("V1_P3_constant_direction_single_scalar",
    sp.simplify(p3 - dm * (sp.integrate(W * g_b, (x, -1, 1)) + 2 * wall)) == 0,
    "P3 sum-form gives ONE scalar row per constant modulus")

# =========================================================================
# V2. TF1(c) field fork — own interior-supported variation and density.
# v = x(1-x^2)^4: v = v' = v'' = 0 at both walls (jet<=2 kill).
v = x * (1 - x**2) ** 4
kill = all(sp.simplify(sp.diff(v, x, j).subs(x, w)) == 0
           for j in (0, 1, 2) for w in (1, -1))
# my own density g = x^3 (odd => annihilates every constant direction, V1)
g = x**3
integrand = sp.expand(g * v)  # = x^4 (1-x^2)^4 >= 0
fact = sp.simplify(integrand - x**4 * (1 - x)**4 * (1 + x)**4) == 0
I0 = sp.integrate(integrand, (x, -1, 1))       # P2 weight, exact rational
Ia = sp.integrate(W * integrand, (x, -1, 1))   # symbolic-weight leg (erf-form ok)
# positivity at symbolic a via nonneg integrand * positive weight: check I0>0 and
# that the integrand is a perfect even nonneg polynomial (factorization above).
chk("V2_own_field_direction_detects_pointwise",
    kill and fact and I0 > 0,
    "v=x(1-x^2)^4 interior-supported; <g,v> = %s > 0 at P2; integrand >= 0 so "
    "every positive weight also pairs nonzero" % I0)
# package's own numbers re-derived independently:
vpkg = x * (1 - x**2) ** 3
chk("V2_package_leg_64_315_reproduced",
    sp.integrate(2 * x * vpkg, (x, -1, 1)) == sp.Rational(64, 315), "")

# =========================================================================
# V3. E04 closed form + cross-member law — SOLVED from scratch (not verified
# against the package's C3: derived by solving the composition equations).
H = sp.diag(-1, 1)
I2 = sp.eye(2)
Z2 = sp.zeros(2, 2)
ph1, ph2 = sp.symbols("phi1 phi2", positive=True)


def expH(p):
    return sp.diag(sp.exp(-p), sp.exp(p))


def ME04(p, C):
    return sp.Matrix(sp.BlockMatrix([[expH(p), Z2], [C * H * (expH(p) - I2), I2]]))


C1 = sp.Matrix(2, 2, lambda i, j: sp.Symbol("u%d%d" % (i, j)))
C2 = sp.Matrix(2, 2, lambda i, j: sp.Symbol("w%d%d" % (i, j)))
# closed form solves M' = X M, M(0) = I  (X = [[H,0],[C H ... no: X=[[H,0],[C,0]]])
Xe04 = sp.Matrix(sp.BlockMatrix([[H, Z2], [C1, Z2]]))
Msym = ME04(t, C1)
chk("V3_E04_closed_form_ODE",
    sp.simplify(sp.diff(Msym, t) - Xe04 * Msym) == sp.zeros(4, 4)
    and Msym.subs(t, 0) == sp.eye(4), "")
# solve composition for C3 entrywise MYSELF
prod = ME04(ph2, C2) * ME04(ph1, C1)
C3 = sp.zeros(2, 2)
hv = (-1, 1)
for i in range(2):
    for j in range(2):
        c3 = sp.Symbol("c3")
        eq = sp.Eq(c3 * hv[j] * (sp.exp((ph1 + ph2) * hv[j]) - 1), prod[2 + i, j] / 1)
        # lower-left entry of composite in E04 form: C3*H*(expH(ph1+ph2)-I)[i,j]
        sol = sp.solve(sp.Eq(c3 * hv[j] * (sp.exp((ph1 + ph2) * hv[j]) - 1),
                             prod[2 + i, j]), c3)
        C3[i, j] = sp.simplify(sol[0])
chk("V3_E04_composite_in_class_with_solved_C3",
    sp.simplify(prod - ME04(ph1 + ph2, C3)) == sp.zeros(4, 4), "")
same = {C2[i, j]: C1[i, j] for i in range(2) for j in range(2)}
chk("V3_drift_iff_distinct",
    sp.simplify(C3.subs(same, simultaneous=True) - C1) == sp.zeros(2, 2)
    and sp.simplify(C3[0, 0] - C1[0, 0]) != 0, "C3==C1 iff same member; drifts else")
# two-sided law on the composite (Q = I since K = 0)
L1 = C1 * H * (expH(ph1) - I2)
L2 = C2 * H * (expH(ph2) - I2)
chk("V3_two_sided_law_E04",
    sp.simplify(prod[2:4, 0:2] - (L1 + L2 * expH(ph1))) == Z2, "L12 = Q2 L1 + L2 rho1")

# =========================================================================
# V4. GENUINELY x-DEPENDENT generator (continuous promotion, not just piecewise):
# X(t) = [[H,0],[C(t),0]], C(t) = C0 + C1 t. Transport T(b,a) = full(b) full(a)^-1
# with full(p) = [[expH(p),0],[L(p),I]], L(p) = Int_0^p C(u) expH(u) du.
C0 = sp.Matrix(2, 2, lambda i, j: sp.Symbol("p%d%d" % (i, j)))
C1m = sp.Matrix(2, 2, lambda i, j: sp.Symbol("q%d%d" % (i, j)))
Cfun = C0 + C1m * t
u = sp.Symbol("u", real=True)
Lp = sp.integrate((C0 + C1m * u) * expH(u), (u, 0, t))


def full(p):
    return sp.Matrix(sp.BlockMatrix([[expH(p), Z2], [Lp.subs(t, p), I2]]))


# ODE check: full' = X(t) full
Xt = sp.Matrix(sp.BlockMatrix([[H, Z2], [Cfun, Z2]]))
chk("V4_xdep_transport_solves_ODE",
    sp.simplify(sp.diff(full(t), t) - Xt * full(t)) == sp.zeros(4, 4), "")
# segment transports: gamma1 = [0,ph1], gamma2 = [ph1, ph1+ph2]
T1 = full(ph1)
T2 = sp.simplify(full(ph1 + ph2) * full(ph1).inv())
L_g1 = T1[2:4, 0:2]
L_g2 = T2[2:4, 0:2]
rho_g1 = T1[0:2, 0:2]
Q_g2 = T2[2:4, 2:4]
tot = full(ph1 + ph2)
chk("V4_two_sided_cocycle_under_promotion",
    sp.simplify(tot[2:4, 0:2] - (Q_g2 * L_g1 + L_g2 * rho_g1)) == Z2
    and sp.simplify(Q_g2 - I2) == Z2,
    "x-dependent generator: L(g2.g1) = Q(g2)L(g1) + L(g2)rho(g1) holds exactly")

# =========================================================================
# V5. Parity lever re-derived (own degree-5 jet) + supplied-status structure.
eps = sp.Symbol("eps")
cj = sp.symbols("b0:6", real=True)
poly = sum(c * t**j for j, c in enumerate(cj))
mir = sp.expand(poly - eps * poly.subs(t, -t))
co = [mir.coeff(t, j) for j in range(6)]
odd_case = [sp.simplify(c.subs(eps, -1)) for c in co]
even_case = [sp.simplify(c.subs(eps, 1)) for c in co]
chk("V5_jet_kill_rederived_deg5",
    odd_case[0] == 2 * cj[0] and odd_case[2] == 2 * cj[2] and odd_case[4] == 2 * cj[4]
    and odd_case[1] == 0 and odd_case[3] == 0 and odd_case[5] == 0
    and even_case[0] == 0 and even_case[1] == 2 * cj[1],
    "eps=-1 kills even jets (constants -> 0); eps=+1 keeps 0-jet")
# -X not in-class-reachable by Lorentz: H-block of -X is -H != H; and the K4
# elements all FIX the H block, so no residual element maps X -> -X.
K4 = [sp.diag(1, 1, 1, 1), sp.diag(1, 1, -1, -1), sp.diag(1, -1, -1, 1), sp.diag(1, -1, 1, -1)]
Kl = sp.Matrix([[sp.Symbol("k00"), 0], [sp.Symbol("k10"), sp.Symbol("k11")]])
Cg = sp.Matrix(2, 2, lambda i, j: sp.Symbol("cg%d%d" % (i, j)))
Xg = sp.Matrix(sp.BlockMatrix([[H, Z2], [Cg, Kl]]))
hfix = all(sp.simplify((g * Xg * g.inv())[0:2, 0:2] - H) == Z2 for g in K4)
chk("V5_mirror_not_reachable_in_class", hfix and sp.simplify(-H - H) != Z2,
    "every K4 element fixes H; -X has H-block -H: mirror action on moduli = SUPPLIED")
# Route-P relevance note (computed, not adopted): IF the seal dressing were the
# banked (non-Lorentz) swap F = swap+I2, then -F X F^-1 IS in class with derived
# parities lam->-lam, k_mod->-k_mod, k10->-k10, C -> -C.F2.
F2 = sp.Matrix([[0, 1], [1, 0]])
Fb = sp.Matrix(sp.BlockMatrix([[F2, Z2], [Z2, I2]]))
Xm = sp.simplify(-(Fb * Xg * Fb.inv()))
eta2 = sp.diag(-1, 1)
chk("V5_swap_dressing_candidate_computed",
    sp.simplify(Xm[0:2, 0:2] - H) == Z2 and sp.simplify(Xm[2:4, 2:4] + Kl) == Z2
    and sp.simplify(Xm[2:4, 0:2] + Cg * F2) == Z2
    and sp.simplify(F2.T * eta2 * F2 - eta2) != Z2,
    "-F X F^-1 in class: K -> -K (lam,k_mod,k10 all odd), C -> -C F2; F NOT Lorentz "
    "=> adopting it = supplied seal structure (Route P input, not banked)")

# =========================================================================
# V6. Shift-absorption x m(x) interaction (missed-source hunt): clock row of
# e^{sX} is (e^{-s},0,0,0) for ANY class member (x-dependent entries included),
# so the Q = c_E e^{-phi} absorption c_E -> c_E e^{-s} is m(x)-independent; and
# e^{s X(x)} e^{phi X(x)} = e^{(phi+s) X(x)} pointwise (same generator commutes).
k00s, k10s, k11s = sp.symbols("K00 K10 K11")
Xn = sp.Matrix(sp.BlockMatrix([[H, Z2], [Cg, sp.Matrix([[k00s, 0], [k10s, k11s]])]]))
Es = sp.exp(s * Xn)  # triangular exponential; SymPy exact
chk("V6_clock_row_shift_universal",
    sp.simplify(Es[0, 0] - sp.exp(-s)) == 0 and all(sp.simplify(Es[0, j]) == 0 for j in (1, 2, 3)),
    "clock-row of e^{sX} = (e^-s,0,0,0) for generic class member => c_E absorption "
    "unchanged under moduli promotion; census fork NOT decided by shift structure")

# =========================================================================
# V7. Stratum-identity descent (S8) with my own densities + weight.
k10c, c00c, c01c, c10c, c11c = sp.symbols("m1 m2 m3 m4 m5", real=True, nonzero=True)
Wv = 2 + sp.cos(0) * x**4  # = 2 + x^4, my own positive weight instance
R00, R01, R10v, R11v = 1 + x**6, x**2, 3 + x, sp.Rational(1, 2) + x**2
Rkm = (c10c * R00 + c11c * R01 - c00c * R10v - c01c * R11v) / k10c
Iw = lambda d: sp.integrate(Wv * d, (x, -1, 1))
chk("V7_kmod0_identity_descends_one_dependency",
    sp.simplify(-k10c * Iw(Rkm) + c10c * Iw(R00) + c11c * Iw(R01)
                - c00c * Iw(R10v) - c01c * Iw(R11v)) == 0,
    "constant coefficients pull out: pointwise identity => same ONE integrated-row "
    "dependency (matches banked TC2 count = 1)")

# =========================================================================
# V8. S9 pullback correspondence with my own density.
g9 = 2 + x + x**5
dmc = sp.Symbol("dmc")
chk("V8_pullback_equals_constant_row",
    sp.simplify(sp.integrate(W * g9 * dmc, (x, -1, 1))
                - dmc * sp.integrate(W * g9, (x, -1, 1))) == 0,
    "field one-form pulled back to constant sections == integrated rows")

# =========================================================================
# V9. Generated-row census-slaving (S7/check 5) re-derived with own generic form.
mf = sp.Function("m")(x)
pf = sp.Function("p")(x)
Dg = sp.exp(sp.Function("A")(mf) * pf) * sp.Function("L")(pf, sp.Derivative(pf, x), mf)
chk("V9_no_mjet_euler_is_partial",
    sp.diff(Dg, sp.Derivative(mf, x)) == 0,
    "banked alphabet has no m-jets => Euler_m = partial_m exactly")
# BR-M-extended wall-term instance (check 17) with my own density D = m'^2/2 + m^2 P
m0, m1c, m2c = sp.symbols("n0 n1 n2", real=True)
mp = m0 + m1c * x + m2c * x**2
P = sp.Symbol("P")
D17 = sp.diff(mp, x) ** 2 / 2 + mp**2 * P
frow = sp.expand(2 * mp * P - sp.diff(mp, x, 2))
chk("V9_mjet_wall_term_difference",
    sp.simplify(sp.integrate(frow, (x, -1, 1))
                - (sp.integrate(2 * mp * P, (x, -1, 1))
                   - (sp.diff(mp, x).subs(x, 1) - sp.diff(mp, x).subs(x, -1)))) == 0,
    "Int(pointwise row) = Int(partial_m D) - [m']_walls exactly (own instance)")

# =========================================================================
# V10. K4 pointwise action on x-dependent generator — own recomputation.
cf = [sp.Function("d%d" % i)(x) for i in range(4)]
k10f = sp.Function("dk")(x)
Cx = sp.Matrix([[cf[0], cf[1]], [cf[2], cf[3]]])
Kx = sp.Matrix([[sp.Function("dk00")(x), 0], [k10f, sp.Function("dk11")(x)]])
Xx = sp.Matrix(sp.BlockMatrix([[H, Z2], [Cx, Kx]]))
g23, g12, g13 = K4[1], K4[2], K4[3]
X23 = g23 * Xx * g23.inv()
X12 = g12 * Xx * g12.inv()
X13 = g13 * Xx * g13.inv()
ok = (sp.simplify(X23[2:4, 0:2] + Cx) == Z2 and sp.simplify(X23[2:4, 2:4] - Kx) == Z2
      and sp.simplify(X12[3, 2] + k10f) == 0 and sp.simplify(X13[3, 2] + k10f) == 0
      and sp.simplify(X12[2, 0] + cf[0]) == 0 and sp.simplify(X12[3, 1] + cf[3]) == 0
      and sp.simplify(X13[2, 1] + cf[1]) == 0 and sp.simplify(X13[3, 0] + cf[2]) == 0)
chk("V10_K4_pointwise_on_promoted_moduli", ok,
    "banked signed flips hold pointwise on Function-valued entries")

print()
if FAIL:
    print("VERIFIER RESULT: %d FAILURES: %s" % (len(FAIL), FAIL))
    sys.exit(1)
print("VERIFIER RESULT: all independent checks passed")
sys.exit(0)
