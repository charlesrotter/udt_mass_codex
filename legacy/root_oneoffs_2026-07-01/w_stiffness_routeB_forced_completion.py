"""ROUTE B OF THE W1 PUSH (w_stiffness_push_declaration.md, 2026-06-11):
the forced-completion / balance method, rerun in the ANGULAR (w) sector.

PRECEDENT (rho_dynamics_derivation_results.md, Route A there): demanding
that the banked two-parameter vacuum (rho = r, f = C + a/r, all C and a)
SURVIVE as a solution of a completed variational problem on the enlarged
(f, rho) class forced the unique completion
L_C1 + D* = (1/4)[(f rho)']^2 (class-relative), because C1's rho-tadpole
EL_rho[L_C1] = (1/2) rho (f')^2 = a^2/(2 r^3) is NONZERO on the banked
vacuum -- a genuine obstruction that only a completion could cancel.

THIS SCRIPT poses the same problem for the shape sector on the P1 static
axisymmetric class and determines whether the completion is FORCED,
MULTI-PARAMETER, or EMPTY.

GROUNDING / CONVENTIONS (declared; P1 scripts were not committed, so the
reduced Lagrangian is REBUILT here from the C1 covariant definition and
validated against every exactly-quoted P1/measure-fork structure):

  * C1 covariant density (rho_dynamics script, repo-matched c = 2):
        L_C1 = (c/2) e^{-2 phi} g^{mu nu} d_mu phi d_nu phi sqrt(-g),
        f = e^{-2 phi}  (phi = -(1/2) ln f).
  * P1 static axisymmetric even-sector class (pde_p1_results.md:
    areal canon k = 0, g_rr = 1/f, fields f, q, w of (r, theta)):
        ds^2 = -f dt^2 + (1/f) dr^2 + 2 q dr dtheta
               + r^2 (1+w)^2 dtheta^2 + r^2 sin^2(theta) (1+w)^{-2} dphi^2.
    The angular block is unimodular-deformed: det(angular) = r^4 sin^2
    independent of w (w is SHAPE, not size; areal canon rho = r intact).
  * Positivity conventions (nondegenerate Lorentzian class, P1):
    f > 0, 1 + w > 0, r > 0, sin(theta) > 0, Det2 := r^2 W / f - q^2 > 0.
  * Statics: time row off; the Q != 0 / same-minus conventions of the
    nonstationary sector are not engaged here.

VALIDATION TARGETS (must reproduce EXACTLY or the reconstruction fails):
  (T1) spherical reduction  -> (c/8) r^2 f_r^2 sin(theta)
       [= (1/4) r^2 (f')^2 per steradian at c = 2; rho_dynamics S_C1]
  (T2) structural lemma: q and w enter L_C1 with NO derivatives
       [pde_p1_results.md lines 27-28]
  (T3) w-tadpole at q = 0:
       dL/dw = -(c/4) sin(th) f_theta^2 / (f (1+w)^3)
       [pde_p1_results.md lines 28-29, quoted verbatim]
  (T4) g_rtheta tadpole at the diagonal point:
       |dL/dq| = (c/4) f_r f_theta sin(theta)
       [measure_fork_results.md line 81]

THE POSED COMPLETION PROBLEM (generating class declared as the premise
set):  seek D*_w added to the C1 density on the P1 class, with

  GENERATING CLASS G:  D = sin(theta) * sum_M alpha_M(f, q, w, r) * M,
  M monomials of degree <= 2 in the first-derivative jets
  (f_r, f_theta, q_r, q_theta, w_r, w_theta) and the fields (q, w),
  alpha_M arbitrary smooth coefficient functions of (f, q, w, r).
  (First-order jet, quadratic grading -- the same class grading as the
  rho precedent's "at most quadratic in first derivatives". Even-sector
  parity is an additional downstream filter, not imposed here.)

  CONDITIONS:
  (i)   D built from metric fields and derivatives only  [class G]
  (ii)  the completed problem admits the banked spherical vacuum
        (f = C + a/r, q = 0, w = 0, ALL C and a) exactly -- all three
        field equations;
  (ii') strengthened macro variant: admits EVERY spherical background
        (f = F(r) arbitrary, q = 0, w = 0) without disturbing the
        f-equation [acceptance test (b), preserve the macro stack];
  (iii) D vanishes identically on the spherical locus
        (w = 0, q = 0, f_theta = 0);
  (iv)  the completed w-equation carries w-derivative terms.

NO LINEARIZATION ANYWHERE: all checks are exact symbolic algebra or
exact rational spot-checks (sanctioned by the task contract). The EH
anatomy in Part 5 is INFORMATIONAL GEOMETRY ONLY (guardrail: curvature
identities usable exactly; EH as dynamics NOT imported -- it is the
named species of the target, never a source here).

New file 2026-06-11 (W1 Route B). No committed file is edited.
"""

import sympy as sp

PASS = []
FAIL = []


def check(name, cond):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name)


def denest(e):
    """Resolve radicals of perfect squares under the declared positivity
    conventions (f > 0, 1+w > 0, r > 0, sin th > 0): factor every
    non-integer-power base, then powdenest with force=True."""
    e = e.replace(lambda x: x.is_Pow and not x.exp.is_Integer,
                  lambda x: sp.Pow(sp.factor(x.base), x.exp))
    return sp.powdenest(e, force=True)


# ----------------------------------------------------------------------
# coordinates, fields, conventions
# ----------------------------------------------------------------------
t, r, th, ph = sp.symbols("t r theta varphi", positive=True)
C, a, c, kap = sp.symbols("C a c kappa", positive=True)
Amp, Bmp = sp.symbols("A B")  # existence-solution amplitudes (any sign)

f = sp.Function("f")(r, th)
q = sp.Function("q")(r, th)
w = sp.Function("w")(r, th)
F = sp.Function("F")  # arbitrary spherical background f = F(r)

fr = sp.Derivative(f, r)
fth = sp.Derivative(f, th)
wr = sp.Derivative(w, r)
wth = sp.Derivative(w, th)
qr = sp.Derivative(q, r)
qth = sp.Derivative(q, th)

W = (1 + w) ** 2          # unimodular shape factor, sqrt(W) := 1 + w > 0
Det2 = r**2 * W / f - q**2  # det of the (r,theta) metric block

# ----------------------------------------------------------------------
# PART 0 -- the C1 reduced density on the P1 class, built two ways
# ----------------------------------------------------------------------
print("\n=== PART 0: grounding -- rebuild and validate the P1 reduced C1 density ===")

# (A) matrix route, straight from the covariant definition
g4 = sp.Matrix([
    [-f, 0, 0, 0],
    [0, 1 / f, q, 0],
    [0, q, r**2 * W, 0],
    [0, 0, 0, r**2 * sp.sin(th) ** 2 / W],
])
g4inv = g4.inv()
detg4 = sp.simplify(g4.det())
phi = -sp.log(f) / 2
xs = [t, r, th, ph]
grad2 = sum(
    g4inv[i, j] * sp.diff(phi, xs[i]) * sp.diff(phi, xs[j])
    for i in range(4) for j in range(4)
)
L_matrix = (c / 2) * sp.exp(-2 * phi) * grad2 * sp.sqrt(-detg4)

# (B) closed form with the positivity conventions resolved by hand:
# sqrt(-detg4) = r sin(th) sqrt(f Det2 / W);  sqrt(W) := (1+w);
# sqrt(f Det2) = sqrt(r^2 W - f q^2).
L_C1 = (c / (8 * f)) * (r**2 * W * fr**2 - 2 * q * fr * fth + fth**2 / f) \
    / Det2 * r * sp.sin(th) * sp.sqrt(r**2 * W - f * q**2) / (1 + w)

# exact-rational spot-check equality of the two constructions
# (radicals evaluate exactly on rational data; positivity respected)
spots = [
    {f: sp.Rational(3, 2), q: sp.Rational(1, 5), w: sp.Rational(1, 3),
     fr: 2, fth: sp.Rational(-1, 2), r: 2, th: sp.pi / 3},
    {f: sp.Rational(5, 4), q: sp.Rational(-1, 7), w: sp.Rational(1, 9),
     fr: sp.Rational(1, 3), fth: 1, r: 3, th: sp.pi / 4},
    {f: 2, q: sp.Rational(2, 5), w: sp.Rational(-1, 4),
     fr: -1, fth: sp.Rational(3, 7), r: sp.Rational(5, 2), th: sp.pi / 6},
    {f: sp.Rational(7, 3), q: 0, w: sp.Rational(1, 2),
     fr: sp.Rational(4, 5), fth: -2, r: 1, th: sp.pi / 2},
]


def eval_at(expr, pt):
    e = expr
    # substitute derivative slots first, then field values
    e = e.subs(sp.Derivative(f, r), pt.get(fr, 0))
    e = e.subs(sp.Derivative(f, th), pt.get(fth, 0))
    e = e.subs(sp.Derivative(w, r), pt.get(wr, 0))
    e = e.subs(sp.Derivative(w, th), pt.get(wth, 0))
    e = e.subs(sp.Derivative(q, r), pt.get(qr, 0))
    e = e.subs(sp.Derivative(q, th), pt.get(qth, 0))
    e = e.subs(f, pt[f]).subs(q, pt[q]).subs(w, pt[w])
    e = e.subs(r, pt[r]).subs(th, pt[th])
    return sp.simplify(e)


for k, pt in enumerate(spots):
    d = sp.simplify(eval_at(L_matrix, pt) - eval_at(L_C1, pt))
    check(f"P0.{k+1} matrix == closed-form C1 density (exact rational spot {k+1})", d == 0)

# T1: spherical reduction
L_sph = sp.simplify(
    L_C1.subs({sp.Derivative(f, th): 0, q: 0, w: 0,
               sp.Derivative(w, r): 0, sp.Derivative(w, th): 0,
               sp.Derivative(q, r): 0, sp.Derivative(q, th): 0})
)
T1 = sp.simplify(L_sph - (c / 8) * r**2 * sp.Derivative(f, r) ** 2 * sp.sin(th))
check("P0.T1 spherical reduction = (c/8) r^2 f_r^2 sin(th)  [rho_dynamics S_C1]",
      sp.powdenest(T1, force=True) == 0 or sp.simplify(T1) == 0)

# T2: structural lemma -- no q or w derivatives anywhere in L_C1
check("P0.T2 structural lemma: L_C1 carries NO w-derivatives",
      not (L_C1.has(sp.Derivative(w, r)) or L_C1.has(sp.Derivative(w, th))))
check("P0.T2 structural lemma: L_C1 carries NO q-derivatives",
      not (L_C1.has(sp.Derivative(q, r)) or L_C1.has(sp.Derivative(q, th))))

# T3: the quoted w-tadpole at q = 0 (pde_p1_results.md, verbatim)
dLdw_q0 = sp.powdenest(sp.simplify(sp.diff(L_C1, w).subs(q, 0)), force=True)
target_T3 = -(c / 4) * sp.sin(th) * fth**2 / (f * (1 + w) ** 3)
check("P0.T3 dL/dw|_{q=0} == -(c/4) sin(th) f_th^2 / (f (1+w)^3)  [pde_p1 quote]",
      sp.simplify(denest(sp.simplify(dLdw_q0 - target_T3))) == 0)

# T4: the measure-fork g_rtheta tadpole at the diagonal point
dLdq_diag = sp.powdenest(sp.simplify(sp.diff(L_C1, q).subs({q: 0, w: 0})), force=True)
target_T4 = -(c / 4) * fr * fth * sp.sin(th)
check("P0.T4 dL/dq|_{q=0,w=0} == -(c/4) f_r f_th sin(th)  [measure-fork flag, magnitude]",
      sp.simplify(dLdq_diag - target_T4) == 0)

# the q=0 reduced density used downstream (radical-free; W = (1+w)^2)
L_C1_q0 = sp.simplify(sp.powdenest(L_C1.subs(q, 0), force=True))
check("P0.5 L_C1(q=0) == (c/8) sin(th) [r^2 f_r^2 + f_th^2/(f (1+w)^2)]",
      sp.simplify(L_C1_q0 - (c / 8) * sp.sin(th)
                  * (r**2 * fr**2 + fth**2 / (f * (1 + w) ** 2))) == 0)

# ----------------------------------------------------------------------
# Euler-Lagrange machinery
# ----------------------------------------------------------------------


def EL(L, X):
    """Euler-Lagrange expression for field X(r,th) of density L (first-order jet)."""
    return (sp.diff(L, X)
            - sp.Derivative(sp.diff(L, sp.Derivative(X, r)), r)
            - sp.Derivative(sp.diff(L, sp.Derivative(X, th)), th))


def on_background(expr, fexpr, wexpr=0, qexpr=0):
    """Evaluate an EL expression on f = fexpr(r,th), w = wexpr, q = qexpr exactly."""
    e = expr.subs(w, wexpr).subs(q, qexpr).subs(f, fexpr)
    e = e.doit()
    e = sp.powdenest(e, force=True)
    return sp.simplify(e)


EL_f_C1 = EL(L_C1, f)
EL_q_C1 = EL(L_C1, q)
EL_w_C1 = EL(L_C1, w)

# ----------------------------------------------------------------------
# PART 1 -- THE NO-OBSTRUCTION THEOREM (the disanalogy with the rho case)
# ----------------------------------------------------------------------
print("\n=== PART 1: the no-obstruction theorem ===")

f_vac = C + a / r  # banked two-parameter vacuum family

check("P1.1 EL_f[L_C1] == 0 on banked vacuum (all C, a)",
      on_background(EL_f_C1, f_vac) == 0)
check("P1.2 EL_q[L_C1] == 0 on banked vacuum (all C, a)",
      on_background(EL_q_C1, f_vac) == 0)
check("P1.3 EL_w[L_C1] == 0 on banked vacuum (all C, a)",
      on_background(EL_w_C1, f_vac) == 0)

# stronger: on EVERY spherical background the shape-sector ELs vanish
check("P1.4 EL_q[L_C1] == 0 on ANY spherical f = F(r) (macro grade)",
      on_background(EL_q_C1, F(r)) == 0)
check("P1.5 EL_w[L_C1] == 0 on ANY spherical f = F(r) (macro grade)",
      on_background(EL_w_C1, F(r)) == 0)
ELf_sph = on_background(EL_f_C1, F(r))
check("P1.6 EL_f[L_C1] on spherical f = F(r) is the banked f-equation "
      "-(c/4) sin(th) (r^2 F')'",
      sp.simplify(ELf_sph + (c / 4) * sp.sin(th)
                  * sp.diff(r**2 * sp.diff(F(r), r), r)) == 0)

# the rho-precedent anchor: the obstruction that FORCED D* in the rho sector
rr = sp.Symbol("r", positive=True)
fro = sp.Function("f")(rr)
rho = sp.Function("rho")(rr)
L_rho = sp.Rational(1, 4) * rho**2 * sp.Derivative(fro, rr) ** 2
EL_rho = (sp.diff(L_rho, rho)
          - sp.Derivative(sp.diff(L_rho, sp.Derivative(rho, rr)), rr))
obstr = sp.simplify(EL_rho.subs(rho, rr).subs(fro, C + a / rr).doit())
check("P1.7 rho-sector obstruction EL_rho[L_C1]|banked == a^2/(2 r^3) != 0 "
      "(the quantity that FORCED D*)",
      sp.simplify(obstr - a**2 / (2 * rr**3)) == 0 and obstr != 0)

print("""
P1 VERDICT: in the rho sector the banked vacuum FAILED C1's enlarged-class
EL system (obstruction a^2/(2r^3)) -- cancellation forced D*. In the w
sector the banked vacuum (and every spherical background) ALREADY SOLVES
C1's full P1-class EL system exactly: the w-tadpole and q-tadpole are
proportional to f_theta(^2) and vanish wherever f is spherical. The
balance method therefore has NO obstruction to cancel: conditions
(ii)+(iii) are HOMOGENEOUS in D and cannot force a unique completion.""")

# ----------------------------------------------------------------------
# PART 2 -- the completion family in the declared generating class
# ----------------------------------------------------------------------
print("=== PART 2: the completion family (28-monomial spanning set, "
      "arbitrary coefficient functions) ===")

# shape ideal generators on the P1 class
gens = {
    "w": w, "q": q, "f_th": fth,
    "w_r": wr, "w_th": wth, "q_r": qr, "q_th": qth,
}
alpha = sp.Function("alpha")

names = list(gens)
n_pass_mono = 0
for i in range(len(names)):
    for j in range(i, len(names)):
        nm = f"{names[i]}*{names[j]}"
        M = gens[names[i]] * gens[names[j]]
        D = alpha(f, q, w, r) * sp.sin(th) * M
        # (iii) locus vanishing
        loc = sp.simplify(D.subs(w, 0).subs(q, 0).subs(f, F(r)).doit())
        ok_loc = loc == 0
        # (ii') all-spherical survival, all three field equations
        ok = ok_loc
        for X, Xn in ((f, "f"), (q, "q"), (w, "w")):
            e = on_background(EL(D, X), F(r))
            ok = ok and (e == 0)
        check(f"P2 [{nm}] vanishes on locus + EL_f,q,w == 0 on every spherical bg", ok)
        if ok:
            n_pass_mono += 1

check("P2.A ALL 28 shape-ideal-squared monomials pass (i)-(iii) with ARBITRARY "
      "coefficient functions alpha(f,q,w,r)", n_pass_mono == 28)

# negative controls: generic shape-LINEAR members FAIL -- the conditions are
# not vacuous
D_lin1 = alpha(f, q, w, r) * sp.sin(th) * wth
e_lin1 = on_background(EL(D_lin1, w), f_vac)
check("P2.B negative control: D = alpha sin(th) w_th FAILS vacuum survival "
      "(EL_w = -d_th(alpha sin th) != 0)", sp.simplify(e_lin1) != 0)

D_lin2 = f * sp.sin(th) * wr  # alpha = f, shape-linear in w_r
e_lin2 = on_background(EL(D_lin2, w), f_vac)
check("P2.C negative control: D = f sin(th) w_r FAILS vacuum survival "
      "(EL_w = -sin(th) f_r != 0)", sp.simplify(e_lin2) != 0)

# the vacuum-only linear survivor M5 = sin(th) (f + r f_r) w_r = sin(th)(rf)' w_r:
# passes the BANKED-VACUUM demand (because (rf)'' = 0 exactly on f = C + a/r)
# but FAILS the macro-grade demand (general spherical F)
M5 = sp.sin(th) * (f + r * fr) * wr
ok5 = all(on_background(EL(M5, X), f_vac) == 0 for X in (f, q, w))
check("P2.D vacuum-only linear survivor: D = sin(th)(rf)' w_r passes ALL "
      "three ELs on the banked vacuum", ok5)
e5F = on_background(EL(M5, w), F(r))
check("P2.E ...but FAILS on general spherical F(r): EL_w = -sin(th)(rF)'' != 0",
      sp.simplify(e5F + sp.sin(th) * sp.diff(r * F(r), r, 2)) == 0
      and sp.simplify(e5F) != 0)

# (iv): representative members supply genuine w-derivative dynamics
K1 = sp.sin(th) * wr**2
K2 = sp.sin(th) * wth**2
K3 = sp.sin(th) * f * r**2 * wr**2
check("P2.F (iv): EL_w[sin(th) w_r^2] contains w_rr (second-derivative stiffness)",
      EL(K1, w).doit().has(sp.Derivative(w, (r, 2))))
check("P2.G (iv): EL_w[sin(th) w_th^2] contains w_thth",
      EL(K2, w).doit().has(sp.Derivative(w, (th, 2))))

# inequivalence of K1, K2, K3 modulo total divergences:
# c1 K1 + c2 K2 + c3 K3 is null (a divergence) iff all three EL expressions
# vanish identically; extract jet coefficients of EL_w.
c1s, c2s, c3s = sp.symbols("c1 c2 c3")
ELw_lin = sp.expand((EL(c1s * K1 + c2s * K2 + c3s * K3, w)).doit())
co_wrr = sp.simplify(ELw_lin.coeff(sp.Derivative(w, (r, 2))))
co_wtt = sp.simplify(ELw_lin.coeff(sp.Derivative(w, (th, 2))))
sol = sp.solve([sp.Eq(co_wtt, 0),
                sp.Eq(co_wrr.subs({f: 1, r: 1}), 0),
                sp.Eq(co_wrr.subs({f: 2, r: 3}), 0)],
               [c1s, c2s, c3s], dict=True)
check("P2.H K1, K2, K3 are mutually inequivalent mod divergences "
      "(null combination forces c1 = c2 = c3 = 0)",
      sol == [{c1s: 0, c2s: 0, c3s: 0}])

print("""
P2 VERDICT: the completion problem is MULTI-PARAMETER -- massively under-
determined. EVERY density of shape-degree >= 2 (the square of the shape
ideal I = (w, q, f_theta, w_r, w_theta, q_r, q_theta)) with ARBITRARY
coefficient functions alpha(f,q,w,r) satisfies (i)-(iii), and infinitely
many inequivalent members satisfy (iv). The family is parametrized by
free FUNCTIONS, not parameters. Under the weaker banked-vacuum-only
demand the family is strictly larger still (shape-linear members like
sin(th)(rf)' w_r join). No forcing occurs at any grading.""")

# ----------------------------------------------------------------------
# PART 3 -- exact shaped solutions of a completed system (acceptance (a))
# ----------------------------------------------------------------------
print("=== PART 3: exact shaped static solutions of a representative "
      "completed system ===")

# representative member (simplest f-decoupled stiffness; one of infinitely many)
D_rep = kap * sp.sin(th) * (r**2 * wr**2 + wth**2)
L_full = L_C1 + D_rep

EL_f_full = EL(L_full, f)
EL_q_full = EL(L_full, q)
EL_w_full = EL(L_full, w)

# the completed w-equation off-spherical (q = 0), for the record:
w_eq_q0 = sp.powdenest(sp.simplify(EL_w_full.subs(q, 0).doit()), force=True)
print("completed w-equation (q = 0):  ", sp.simplify(w_eq_q0), " = 0")
check("P3.0 completed w-equation = stiffness operator MINUS the P1 tadpole "
      "(the bare tadpole is no longer unbalanceable)",
      sp.simplify(
          w_eq_q0
          - (-(c / 4) * sp.sin(th) * fth**2 / (f * (1 + w) ** 3)
             - 2 * kap * (sp.diff(sp.sin(th) * r**2 * wr, r)
                          + sp.diff(sp.sin(th) * wth, th)))
      ).doit().simplify() == 0)

# exact solution family:  f = C + a/r, q = 0,
# w = (A r^l + B r^{-l-1}) P_l(cos th),  l = 1, 2  (both radial branches)
for ell in (1, 2):
    Pl = sp.legendre(ell, sp.cos(th))
    w_sol = (Amp * r**ell + Bmp * r ** (-ell - 1)) * Pl
    ok_all = True
    for ELX, nmX in ((EL_f_full, "f"), (EL_q_full, "q"), (EL_w_full, "w")):
        e = on_background(ELX, f_vac, wexpr=w_sol, qexpr=0)
        ok_all = ok_all and (sp.simplify(e) == 0)
    check(f"P3.{ell} EXACT shaped solution, ell={ell}: f = C + a/r, q = 0, "
          f"w = (A r^{ell} + B r^-{ell+1}) P_{ell}(cos th) solves ALL THREE "
          "field equations of L_C1 + D_rep", ok_all)
    check(f"P3.{ell}b solution is genuinely shaped: w_theta != 0",
          sp.simplify(sp.diff(w_sol, th)) != 0)

# the macro sector is untouched by D_rep: every spherical background still
# solves the shape-sector equations of the COMPLETED system
check("P3.4 completed system still admits every spherical background "
      "(EL_q, EL_w == 0 at f = F(r), q = w = 0)",
      on_background(EL_q_full, F(r)) == 0
      and on_background(EL_w_full, F(r)) == 0)
check("P3.5 completed f-equation on spherical bg unchanged "
      "(D_rep is f-decoupled: macro stack untouched)",
      sp.simplify(on_background(EL_f_full, F(r))
                  - on_background(EL_f_C1, F(r))) == 0)

# honesty datum: the exact shaped solutions above carry f_theta = 0 (the
# phi-angular tadpole is OFF on them); whether f_theta != 0 solutions of
# the completed system exist is NOT settled here (full nonlinear PDE).
check("P3.6 honesty: the exhibited shaped solutions have f_theta == 0 "
      "(tadpole off; balance never tested nonlinearly)",
      sp.simplify(sp.diff(f_vac, th)) == 0)

print("""
P3 VERDICT: acceptance test (a) datum -- for the representative member the
completed system admits EXACT nonconstant-shape static solutions
(w = harmonics, f spherical, q = 0; valid wherever 1 + w > 0, i.e. on
finite cells per the finite-cell canon), while the spherical/macro
sector survives untouched (test (b)). The static no-go's mechanism (the
pointwise-algebraic unbalanceable tadpole) is removed EXACTLY. Open and
honestly scoped: existence of f_theta != 0 (phi-shaped) solutions of any
completed system is NOT settled -- that is the full nonlinear PDE.""")

# ----------------------------------------------------------------------
# PART 4 -- the species comparison (INFORMATIONAL GEOMETRY, NOT A SOURCE)
# ----------------------------------------------------------------------
print("=== PART 4: EH-remainder species anatomy on this class "
      "(informational only; guardrail: not imported as dynamics) ===")

gd = sp.diag(-f, 1 / f, r**2 * (1 + w) ** 2, r**2 * sp.sin(th) ** 2 / (1 + w) ** 2)
gu = gd.inv()
n = 4
Gamma = [[[sp.simplify(sum(gu[l, s] * (sp.diff(gd[s, i], xs[j])
                                       + sp.diff(gd[s, j], xs[i])
                                       - sp.diff(gd[i, j], xs[s])) / 2
                           for s in range(n)))
           for j in range(n)] for i in range(n)] for l in range(n)]
Ric = [[sp.simplify(
    sum(sp.diff(Gamma[l][i][j], xs[l]) for l in range(n))
    - sum(sp.diff(Gamma[l][i][l], xs[j]) for l in range(n))
    + sum(Gamma[l][l][s] * Gamma[s][i][j] for l in range(n) for s in range(n))
    - sum(Gamma[l][j][s] * Gamma[s][i][l] for l in range(n) for s in range(n)))
    for j in range(n)] for i in range(n)]
Rscal = sp.simplify(sum(gu[i, j] * Ric[i][j] for i in range(n) for j in range(n)))

check("P4.1 -det(g) == r^4 sin^2(th) exactly on the unimodular-shape class "
      "(w never enters the volume -- the structural root of T2)",
      sp.simplify(-gd.det() - r**4 * sp.sin(th) ** 2) == 0)

densEH = sp.expand(r**2 * sp.sin(th) * Rscal)
co_wr2 = sp.simplify(densEH.coeff(sp.Derivative(w, r), 2))
co_wth2 = sp.simplify(densEH.coeff(sp.Derivative(w, th), 2))
co_wrr = sp.simplify(densEH.coeff(sp.Derivative(w, (r, 2))))
co_wtt = sp.simplify(densEH.coeff(sp.Derivative(w, (th, 2))))
check("P4.2 EH density on this class DOES carry w_r^2 terms", co_wr2 != 0)
check("P4.3 EH density on this class DOES carry w_th^2 terms", co_wth2 != 0)
check("P4.4 EXACT cancellation: the EH w_rr coefficient is IDENTICALLY ZERO "
      "on this class (the radial second-derivative w-sector cancels)",
      co_wrr == 0)
check("P4.5 w_thth enters LINEARLY with coefficient 2 sin(th)/(1+w)^3 "
      "(removable by parts)",
      sp.simplify(co_wtt - 2 * sp.sin(th) / (1 + w) ** 3) == 0
      and sp.simplify(sp.diff(densEH, sp.Derivative(w, (th, 2)), 2)) == 0)
# explicit boundary reduction of the w_thth term:
densEH_red = sp.expand(densEH - sp.Derivative(co_wtt * sp.Derivative(w, th), th).doit())
second_w = [d for d in densEH_red.atoms(sp.Derivative)
            if d.expr == w and sum(k for _, k in d.variable_count) >= 2]
check("P4.6 after one exact integration by parts the EH density carries NO "
      "second w-derivatives (all collected coefficients identically zero): "
      "the EH w-species is FIRST-ORDER -- it lies INSIDE the declared "
      "generating class G (allowed, hence NOT selected)",
      all(sp.simplify(densEH_red.coeff(d)) == 0 for d in second_w))
check("P4.7 the exact contrast: C1 carries NO w-derivatives (T2), EH carries "
      "them -- the species exists on this class but C1 never produces it",
      co_wr2 != 0 and not L_C1.has(sp.Derivative(w, r)))
print("EH w_r^2 coefficient (anatomy, informational): ", sp.factor(co_wr2))
print("EH w_th^2 coefficient (anatomy, informational): ", sp.factor(co_wth2))
print("EH w_th^2 coefficient AFTER the by-parts reduction: ",
      sp.factor(sp.simplify(densEH_red.coeff(sp.Derivative(w, th), 2))))
print("EH w_r x f_r cross coefficient (anatomy, informational): ",
      sp.factor(sp.simplify(densEH.coeff(sp.Derivative(w, r), 1)
                            .coeff(sp.Derivative(f, r), 1))))

# A1-IN-THE-w-SECTOR (exact, the balance method's own refusal of the EH
# import -- informational confirmation of the guardrail, not a source):
# the literal EH density FAILS vacuum survival in the w-equation by a
# UNIVERSAL constant: EL_w[sqrt(-g) R] = 2 sin(th) on EVERY spherical
# background (f-independent -- the same species constant as the EH
# remainder's "2" in 2 - 2 f rho rho''). And since sqrt(-g) = r^2 sin(th)
# is w-blind on this class, no volume/cosmological counterterm can cancel
# it: no C1 + kappa*EH system admits the banked vacuum on the P1 class
# for any kappa != 0. This re-derives rho_dynamics A1 natively in the
# shape sector.
ELw_EH_vac = sp.simplify(EL(densEH, w).subs(w, 0).subs(f, f_vac).doit())
ELw_EH_sph = sp.simplify(EL(densEH, w).subs(w, 0).subs(f, F(r)).doit())
check("P4.8 EL_w[sqrt(-g) R] == 2 sin(th) on the banked vacuum (exact, "
      "f-independent): the literal EH density FAILS vacuum survival",
      sp.simplify(ELw_EH_vac - 2 * sp.sin(th)) == 0)
check("P4.9 ...and == 2 sin(th) on EVERY spherical background: A1 "
      "re-derived in the w sector (no C1 + kappa*EH system admits the "
      "banked vacuum on this class; volume terms are w-blind, cannot cancel)",
      sp.simplify(ELw_EH_sph - 2 * sp.sin(th)) == 0)

# ----------------------------------------------------------------------
# summary
# ----------------------------------------------------------------------
print("\n=== SUMMARY ===")
print(f"PASS: {len(PASS)}  FAIL: {len(FAIL)}")
if FAIL:
    print("FAILED CHECKS:")
    for nm in FAIL:
        print("  ", nm)
print("""
ROUTE B VERDICT: MULTI-PARAMETER (not forced, not empty).
The rho-precedent forcing engine -- a nonzero obstruction on the banked
vacuum -- DOES NOT EXIST in the w sector: every shape-sector EL of C1
vanishes identically on every spherical configuration, and every banked
static solution is spherical (P1 theorem). Vacuum/macro survival is
therefore a homogeneous condition and admits the entire shape-ideal-
squared module with free coefficient functions. The balance method
cannot derive the w-stiffness; forcing must come from elsewhere
(Route A class enlargement, Route C second sectors, or a new native
principle). PREMISE SET for this negative-of-forcing: P1 static
axisymmetric even-sector class (f, q, w; rho = r areal canon; g_rr=1/f;
unimodular shape block W=(1+w)^2), C1 density as grounded in Part 0,
generating class G (first-order jet, degree <= 2, coefficients
alpha(f,q,w,r)), survival demanded on the banked vacuum family and on
all spherical backgrounds, statics only.""")

if FAIL:
    raise SystemExit(1)
