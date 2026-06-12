"""BLIND ADVERSARIAL VERIFIER for w_stiffness_routeB_forced_completion.py
(W1 Route B, 2026-06-11). New file; no committed file edited.

Independent re-derivations with OWN code paths:
  V0  grounding: matrix-route C1 density, own closed form, sign audit
      against the rescued pde_p1 workspace convention (c = -2, minus
      prefactor) vs the route's (c = +2, plus prefactor).
  V1  claim 1 (no-obstruction): confirm the spherical homogeneity, then
      ATTACK with the banked Class-A cell configurations (w = q = 0,
      f_theta != 0: the M2 library / sourced collar class): the survival
      demand there is INHOMOGENEOUS -- the balance method revives.
      Determine what it forces: an algebraic w-slope counterterm, never
      a stiffness (stiffness ELs are invisible on every w = 0 config).
  V2  claim 2: independent rerun of the 28-monomial family, negative
      controls, M5, and a SECOND-JET member (w * w_rr) showing the
      multi-parameter verdict survives (worsens) under jet enlargement.
  V3  claim 3: own EL of C1 + D_rep; exact solutions ell = 1, 2, 3;
      axis-regularity (elementary flatness) of the shaped solutions;
      no-go for axis-regular superpositions; action finiteness and
      boundedness on a finite cell.
  V4  claim 4 (A1-native): TRUE second-order Euler-Lagrange operator on
      the EH density (the route used a FIRST-ORDER operator on a
      SECOND-ORDER density); Einstein-tensor cross-check; the f-channel
      within the P1 ansatz (g_tt g_rr = -1 locked, rho = r locked).
  V5  route-script defect anatomy: the 2 sin(th) is exactly the missing
      +d_th^2 (dL/dw_thth) term.

All algebra exact (sympy); radicals resolved only on the declared
positivity domain (f > 0, 1+w > 0, r > 0, sin th > 0, D2 > 0), each
closed form validated against the radical matrix construction at exact
rational spots before use.
"""

import sympy as sp

PASS, FAIL = [], []


def check(name, cond):
    (PASS if cond else FAIL).append(name)
    print(("PASS " if cond else "FAIL ") + name, flush=True)


t, r, th, ph = sp.symbols("t r theta varphi", positive=True)
C, a, cc, kap = sp.symbols("C a c kappa", positive=True)
A1, B1, A2, B2 = sp.symbols("A1 B1 A2 B2", real=True)
r1, r2 = sp.symbols("r1 r2", positive=True)

f = sp.Function("f")(r, th)
q = sp.Function("q")(r, th)
w = sp.Function("w")(r, th)
F = sp.Function("F")   # arbitrary spherical f
G = sp.Function("G")   # arbitrary axisymmetric f (cell configurations)
alpha = sp.Function("alpha")

fr, fth = sp.Derivative(f, r), sp.Derivative(f, th)
wr, wth = sp.Derivative(w, r), sp.Derivative(w, th)
qr, qth = sp.Derivative(q, r), sp.Derivative(q, th)

W = (1 + w) ** 2
D2 = r**2 * W - f * q**2   # f * det of (r,theta) block (pde_p1 convention)
xs = [t, r, th, ph]

# ======================================================================
# V0 -- grounding: independent matrix construction and closed form
# ======================================================================
print("\n=== V0: grounding ===")

g4 = sp.Matrix([
    [-f, 0, 0, 0],
    [0, 1 / f, q, 0],
    [0, q, r**2 * W, 0],
    [0, 0, 0, r**2 * sp.sin(th) ** 2 / W],
])
g4inv = g4.inv()
detg4 = sp.factor(g4.det())
phi = -sp.log(f) / 2
grad2 = sum(g4inv[i, j] * sp.diff(phi, xs[i]) * sp.diff(phi, xs[j])
            for i in range(4) for j in range(4))
L_matrix = (cc / 2) * sp.exp(-2 * phi) * grad2 * sp.sqrt(-detg4)

# my own closed form (derived by hand from the pde_p1 Lclosed, sign-resolved
# to the route's +c/2 convention):
L_v = (cc / 8) * r * sp.sin(th) \
    * (f * r**2 * W * fr**2 - 2 * f * q * fr * fth + fth**2) \
    / (f * (1 + w) * sp.sqrt(D2))

# fresh rational spots (different from the route's), positivity respected
spots = [
    {f: sp.Rational(9, 4), q: sp.Rational(-2, 7), w: sp.Rational(2, 5),
     fr: sp.Rational(-3, 4), fth: sp.Rational(5, 6), r: sp.Rational(7, 3),
     th: sp.pi / 5},
    {f: sp.Rational(1, 2), q: sp.Rational(1, 9), w: sp.Rational(-2, 5),
     fr: 3, fth: sp.Rational(-1, 8), r: sp.Rational(3, 2), th: sp.pi / 7},
    {f: 4, q: sp.Rational(3, 8), w: sp.Rational(1, 6),
     fr: sp.Rational(2, 9), fth: -3, r: 2,
     th: 2 * sp.pi / 5},
]


def eval_at(expr, pt):
    e = expr
    for d, k in ((sp.Derivative(f, r), fr), (sp.Derivative(f, th), fth),
                 (sp.Derivative(w, r), wr), (sp.Derivative(w, th), wth),
                 (sp.Derivative(q, r), qr), (sp.Derivative(q, th), qth)):
        e = e.subs(d, pt.get(k, 0))
    e = e.subs(f, pt[f]).subs(q, pt[q]).subs(w, pt[w])
    e = e.subs(r, pt[r]).subs(th, pt[th])
    return sp.simplify(e)


for k, pt in enumerate(spots):
    # positivity-domain sanity of the spot itself
    d2v = (pt[r] ** 2 * (1 + pt[w]) ** 2 - pt[f] * pt[q] ** 2)
    ok = d2v > 0 and (1 + pt[w]) > 0 and pt[f] > 0
    d = sp.simplify(eval_at(L_matrix, pt) - eval_at(L_v, pt))
    check(f"V0.{k+1} own closed form == matrix C1 density (fresh spot {k+1})",
          ok and d == 0)

# q = 0 reduced density (radical resolved on 1+w > 0)
L_q0 = (cc / 8) * sp.sin(th) * (r**2 * fr**2 + fth**2 / (f * (1 + w) ** 2))
d = sp.simplify(sp.powdenest(L_v.subs(q, 0), force=True) - L_q0)
check("V0.4 L_C1(q=0) == (c/8) sin th [r^2 f_r^2 + f_th^2/(f(1+w)^2)] "
      "(claim 5 reduced form)", d == 0)

# SIGN AUDIT (claim 5 / attack E): the rescued pde_p1 workspace builds
# L = -(c/2)(...) and banks c = -2 (its check D-16/17 print); the route
# builds L = +(c/2)(...) with 'repo-matched c = 2'.  Physical densities:
phys_route = L_q0.subs(cc, 2)              # route convention
phys_pde = (-(sp.Symbol("cp") / 8) * sp.sin(th)
            * (r**2 * fr**2 + fth**2 / (f * (1 + w) ** 2))).subs(
                sp.Symbol("cp"), -2)       # pde_p1 convention, c = -2
check("V0.5 route(c=+2) and pde_p1(c=-2) give the IDENTICAL physical "
      "density (conventions compatible)",
      sp.simplify(phys_route - phys_pde) == 0)

# the two 'tadpole' formulas that share the string -(c/4)...:
tad_q0 = sp.simplify(sp.diff(phys_route, w))        # at q = 0 (route T3 object)
# pde_p1's quoted w-equation is on the q = q* branch: angular sign flipped
phys_qstar = (sp.Rational(1, 4) * sp.sin(th)
              * (r**2 * fr**2 - fth**2 / (f * (1 + w) ** 2)))  # physical, c=-2 resolved
tad_qstar = sp.simplify(sp.diff(phys_qstar, w))
check("V0.6 PHYSICAL q=0 tadpole = -(1/2) sin th f_th^2/(f(1+w)^3)",
      sp.simplify(tad_q0 + sp.Rational(1, 2) * sp.sin(th) * fth**2
                  / (f * (1 + w) ** 3)) == 0)
check("V0.7 PHYSICAL q=q* tadpole = +(1/2) sin th f_th^2/(f(1+w)^3): "
      "OPPOSITE sign -- the route's T3 'verbatim' match with pde_p1 is a "
      "string-level coincidence (q=0 branch, c=+2) vs (q* branch, c=-2); "
      "double sign flip makes the SYMBOL strings coincide",
      sp.simplify(tad_qstar - sp.Rational(1, 2) * sp.sin(th) * fth**2
                  / (f * (1 + w) ** 3)) == 0)

# ======================================================================
# Euler-Lagrange machinery: first-order AND full second-order operators
# ======================================================================


def EL1(L, X):
    """First-order EL (valid only for first-order densities)."""
    return (sp.diff(L, X)
            - sp.Derivative(sp.diff(L, sp.Derivative(X, r)), r)
            - sp.Derivative(sp.diff(L, sp.Derivative(X, th)), th))


def EL2(L, X):
    """Full EL through second-order jets:
    dL/dX - D_i dL/dX_i + D_i D_j dL/dX_ij (mixed counted once)."""
    e = sp.diff(L, X)
    e -= sp.Derivative(sp.diff(L, sp.Derivative(X, r)), r)
    e -= sp.Derivative(sp.diff(L, sp.Derivative(X, th)), th)
    e += sp.Derivative(sp.diff(L, sp.Derivative(X, (r, 2))), r, 2)
    e += sp.Derivative(sp.diff(L, sp.Derivative(X, (th, 2))), th, 2)
    e += sp.Derivative(sp.diff(L, sp.Derivative(X, r, th)), r, th)
    return e


def denest(e):
    """Resolve radicals of perfect squares on the declared positivity
    domain: factor non-integer-power bases, then powdenest(force)."""
    e = e.replace(lambda x: x.is_Pow and not x.exp.is_Integer,
                  lambda x: sp.Pow(sp.factor(x.base), x.exp))
    return sp.powdenest(e, force=True)


def on_bg(expr, fexpr, wexpr=0, qexpr=0):
    e = expr.subs(w, wexpr).subs(q, qexpr).subs(f, fexpr)
    e = e.doit()
    return sp.simplify(denest(sp.simplify(denest(e))))


ELf_C1, ELq_C1, ELw_C1 = EL1(L_v, f), EL1(L_v, q), EL1(L_v, w)
f_vac = C + a / r

# ======================================================================
# V1 -- claim 1: homogeneity on spherical, INHOMOGENEITY on banked cells
# ======================================================================
print("\n=== V1: claim 1 (no-obstruction) and its scope ===")

check("V1.1 EL_f[C1] == 0 on banked vacuum", on_bg(ELf_C1, f_vac) == 0)
check("V1.2 EL_q[C1] == 0 on banked vacuum", on_bg(ELq_C1, f_vac) == 0)
check("V1.3 EL_w[C1] == 0 on banked vacuum", on_bg(ELw_C1, f_vac) == 0)
check("V1.4 EL_q[C1] == 0 on every spherical F(r)", on_bg(ELq_C1, F(r)) == 0)
check("V1.5 EL_w[C1] == 0 on every spherical F(r)", on_bg(ELw_C1, F(r)) == 0)

# ATTACK: the banked Class-A cell class (w = q = 0, f_theta != 0:
# M2 library cells, sourced collars f = F(y)(1 + kappa u)).  There the
# w-tadpole of C1 is NONZERO -- the survival demand is INHOMOGENEOUS:
ELw_cell = on_bg(ELw_C1, G(r, th))
tad_cell = sp.simplify(ELw_cell + (cc / 4) * sp.sin(th)
                       * sp.Derivative(G(r, th), th) ** 2 / G(r, th))
check("V1.6 INHOMOGENEITY REVIVES on banked cells: EL_w[C1] = "
      "-(c/4) sin th G_th^2 / G != 0 at (w=q=0, f_theta != 0)",
      tad_cell == 0 and sp.simplify(ELw_cell) != 0)

# the q-equation ALSO obstructs the cells (the measure-fork tadpole):
ELq_cell = on_bg(ELq_C1, G(r, th))
check("V1.6b ...and EL_q[C1] = -(c/4) sin th G_r G_th != 0 there "
      "(the measure-fork flag is the q-channel obstruction)",
      sp.simplify(ELq_cell + (cc / 4) * sp.sin(th)
                  * sp.Derivative(G(r, th), r)
                  * sp.Derivative(G(r, th), th)) == 0)

# class-G members that cancel BOTH tadpoles POINTWISE for EVERY f
# (algebraic slope counterterms; monomials f_th^2 and f_r*f_th with
# w- and q-dependent coefficients -- note f_r*f_th is in the declared
# class G but NOT among the route's 28 shape-pair monomials):
D_a = (cc / 4) * sp.sin(th) * w * fth**2 / f
D_q = (cc / 4) * sp.sin(th) * q * fr * fth
D_cell = D_a + D_q
check("V1.7 D_a = (c/4) sin th w f_th^2/f cancels the cell w-tadpole "
      "for EVERY axisymmetric f: EL_w[C1 + D_a] == 0 at w = q = 0",
      on_bg(EL1(L_v + D_a, w), G(r, th)) == 0)
check("V1.8 D_q = (c/4) sin th q f_r f_th cancels the cell q-tadpole: "
      "EL_q[C1 + D_q] == 0 at w = q = 0",
      on_bg(EL1(L_v + D_q, q), G(r, th)) == 0)
check("V1.8b D_cell = D_a + D_q leaves the f-equation untouched at "
      "w = q = 0: every Class-A cell SOLUTION (M2 library, collars) "
      "becomes an EXACT full-system static of C1 + D_cell -- a "
      "stiffness-free member of the family resurrects static cells",
      on_bg(EL1(D_cell, f), G(r, th)) == 0
      and on_bg(EL1(L_v + D_cell, q), G(r, th)) == 0
      and on_bg(EL1(L_v + D_cell, w), G(r, th)) == 0)
check("V1.9 D_cell vanishes on the spherical locus and preserves "
      "vacuum/macro survival (route conditions (ii),(ii'),(iii))",
      sp.simplify(D_cell.subs(w, 0).subs(q, 0)) == 0
      and on_bg(EL1(D_cell, w), F(r)) == 0
      and on_bg(EL1(D_cell, q), F(r)) == 0
      and on_bg(EL1(D_cell, f), F(r)) == 0)

# but the revived balance still selects NOTHING unique: stiffness terms are
# INVISIBLE on every w = 0 configuration (their EL_w vanishes identically
# there), so D_a + (any stiffness) cancels equally well:
for nm, Dst in (("w_r^2", alpha(f, q, w, r) * sp.sin(th) * wr**2),
                ("w_th^2", alpha(f, q, w, r) * sp.sin(th) * wth**2),
                ("w_r*w_th", alpha(f, q, w, r) * sp.sin(th) * wr * wth)):
    check(f"V1.10[{nm}] stiffness EL_w INVISIBLE on every w=0 config "
          "(arbitrary alpha, arbitrary f)",
          on_bg(EL1(Dst, w), G(r, th)) == 0)
check("V1.11 NON-UNIQUENESS of the revived balance: D_a + kappa sin th "
      "(r^2 w_r^2 + w_th^2) cancels the cell tadpole identically as well",
      on_bg(EL1(L_v + D_a + kap * sp.sin(th) * (r**2 * wr**2 + wth**2), w),
            G(r, th)) == 0)

# ======================================================================
# V2 -- claim 2: independent re-run of the family
# ======================================================================
print("\n=== V2: claim 2 (exact family) ===")

gens = {"w": w, "q": q, "f_th": fth, "w_r": wr, "w_th": wth,
        "q_r": qr, "q_th": qth}
names = list(gens)
n_ok = 0
for i in range(len(names)):
    for j in range(i, len(names)):
        M = gens[names[i]] * gens[names[j]]
        D = alpha(f, q, w, r) * sp.sin(th) * M
        ok = sp.simplify(D.subs(w, 0).subs(q, 0).subs(f, F(r)).doit()) == 0
        for X in (f, q, w):
            ok = ok and on_bg(EL1(D, X), F(r)) == 0
        n_ok += ok
check("V2.1 all 28 shape-ideal-squared monomials pass survival + locus "
      "(independent EL code)", n_ok == 28)

e = on_bg(EL1(alpha(f, q, w, r) * sp.sin(th) * wth, w), f_vac)
check("V2.2 negative control alpha sin th w_th fails (EL_w = -alpha cos th "
      "- ... != 0 for every alpha)", sp.simplify(e) != 0)
e = on_bg(EL1(f * sp.sin(th) * wr, w), f_vac)
check("V2.3 negative control f sin th w_r fails on vacuum", sp.simplify(e) != 0)

M5 = sp.sin(th) * (f + r * fr) * wr
check("V2.4 M5 = sin th (rf)' w_r passes banked-vacuum-only survival "
      "(all three ELs)",
      all(on_bg(EL1(M5, X), f_vac) == 0 for X in (f, q, w)))
check("V2.5 ...and fails macro-grade survival (general F)",
      sp.simplify(on_bg(EL1(M5, w), F(r))) != 0)

# jet enlargement: a SECOND-JET member also passes -> the multi-parameter
# verdict only worsens when the class is enlarged toward where EH lives
D_2jet = alpha(f, q, w, r) * sp.sin(th) * w * sp.Derivative(w, (r, 2))
ok = sp.simplify(D_2jet.subs(w, 0).doit()) == 0
for X in (f, q, w):
    ok = ok and on_bg(EL2(D_2jet, X), F(r)) == 0
check("V2.6 second-jet member alpha sin th w w_rr ALSO passes (full "
      "second-order EL): under-determination grows with the jet order", ok)

# ======================================================================
# V3 -- claim 3: exact shaped solutions; regularity; action
# ======================================================================
print("\n=== V3: claim 3 (exact shaped solutions of C1 + D_rep) ===")

D_rep = kap * sp.sin(th) * (r**2 * wr**2 + wth**2)

# Radical-free verification on the q = 0 slice. EXACTNESS NOTE: C1
# carries q only ALGEBRAICALLY (no q-derivatives), so on a q == 0
# background (a) EL_q[L] = dL/dq, and (b) EL_f, EL_w of L coincide with
# the ELs of the q = 0 restriction L|_{q=0} (cross terms q*h(...) drop
# at q = 0 under every jet derivative). No linearization involved.
L0 = L_q0 + D_rep
ELf0, ELw0 = EL1(L0, f), EL1(L0, w)
dLdq = sp.diff(L_v + D_rep, q)
dLdq_0 = sp.simplify(denest(sp.simplify(denest(dLdq.subs(q, 0)))))
check("V3.0 EL_q[C1+D_rep]|_{q=0} == -(c/4) sin th f_r f_th/(1+w)^2 "
      "(closed form; vanishes iff f_r f_th = 0, ANY w)",
      sp.simplify(dLdq_0 + (cc / 4) * sp.sin(th) * fr * fth
                  / (1 + w) ** 2) == 0)

Aa, Bb = sp.symbols("A B", real=True)
for ell in (1, 2, 3):
    w_sol = (Aa * r**ell + Bb * r ** (-ell - 1)) * sp.legendre(ell, sp.cos(th))
    ok = (on_bg(ELf0, f_vac, wexpr=w_sol) == 0
          and on_bg(ELw0, f_vac, wexpr=w_sol) == 0
          and on_bg(dLdq_0, f_vac, wexpr=w_sol) == 0)
    check(f"V3.{ell} ell={ell}: f = C + a/r, q = 0, "
          f"w = (A r^{ell} + B r^-{ell+1}) P_{ell} solves all three ELs "
          "(own derivation)", ok)

# REGULARITY ATTACK: elementary flatness on the symmetry axis requires
# w = 0 at the poles; the metric's axis deficit ratio is (1+w)^-4:
ratio = sp.simplify((r**2 * sp.sin(th) ** 2 / W)
                    / (sp.sin(th) ** 2 * r**2 * W))
check("V3.4 axis deficit ratio g_phph/(sin^2 g_thth) == (1+w)^-4 "
      "(elementary flatness iff w = 0 on the axis)",
      sp.simplify(ratio - 1 / (1 + w) ** 4) == 0)
w1_pole = ((Aa * r + Bb / r**2) * sp.legendre(1, sp.cos(th))).subs(th, 0)
check("V3.5 the ell=1 member has w != 0 on the axis (P_1(1) = 1): every "
      "exhibited shaped solution carries a CONICAL AXIS DEFECT, deficit "
      "varying with r (a curvature-singular axis line)",
      sp.simplify(w1_pole - (Aa * r + Bb / r**2)) == 0)

# no-go: NO nontrivial axis-regular superposition (ell = 1 and 2 mix):
w_mix = ((A1 * r + B1 / r**2) * sp.legendre(1, sp.cos(th))
         + (A2 * r**2 + B2 / r**3) * sp.legendre(2, sp.cos(th)))
condN = sp.expand(w_mix.subs(th, 0))        # w(r, north pole) = 0 for all r
condS = sp.expand(w_mix.subs(th, sp.pi))    # w(r, south pole) = 0 for all r
polyN = sp.Poly(condN * r**3, r)
polyS = sp.Poly(condS * r**3, r)
sol = sp.solve(polyN.coeffs() + polyS.coeffs(), [A1, B1, A2, B2], dict=True)
check("V3.6 axis-regular superposition NO-GO: w(r, poles) = 0 for all r "
      "forces A1 = B1 = A2 = B2 = 0 (powers of r independent)",
      sol == [{A1: 0, B1: 0, A2: 0, B2: 0}])

# ACTION on a finite cell [r1, r2] x [0, pi] (ell = 1, physical c = 2):
w1 = (Aa * r + Bb / r**2) * sp.cos(th)
S_C1_val = sp.integrate(sp.integrate(
    (sp.Rational(1, 4) * r**2 * sp.diff(f_vac, r) ** 2 * sp.sin(th)),
    (th, 0, sp.pi)), (r, r1, r2))
dens_rep = kap * sp.sin(th) * (r**2 * sp.diff(w1, r) ** 2
                               + sp.diff(w1, th) ** 2)
S_rep_val = sp.simplify(sp.integrate(sp.integrate(dens_rep, (th, 0, sp.pi)),
                                     (r, r1, r2)))
check("V3.7 cell action of the shaped solution is FINITE for 0 < r1 < r2",
      S_C1_val.is_finite is not False and not S_rep_val.has(sp.zoo, sp.oo)
      and sp.simplify(S_C1_val - sp.Rational(1, 2) * a**2 *
                      (1 / r1 - 1 / r2)) == 0)
# positive-definiteness of the (A,B) quadratic form (kappa > 0):
QAA = sp.simplify(S_rep_val.diff(Aa, 2) / 2)
QBB = sp.simplify(S_rep_val.diff(Bb, 2) / 2)
QAB = sp.simplify(S_rep_val.diff(Aa).diff(Bb) / 2)
detQ = sp.simplify(QAA * QBB - QAB**2)
num = {r1: sp.Rational(1, 2), r2: 3, kap: 1}
check("V3.8 shaped-action quadratic form in (A,B) is positive definite "
      "(kappa > 0): action bounded below; shaped members cost MORE action "
      "than the unshaped vacuum (they are boundary-data-supported, not "
      "energetically preferred)",
      QAA.subs(num) > 0 and detQ.subs(num) > 0
      and sp.simplify(S_rep_val.subs({Aa: 0, Bb: 0})) == 0)
# kappa < 0 unboundedness witness: D_rep scales as lam^2 under
# w -> sin(lam r) ripple while |w| stays bounded -- exhibit exactly:
lam = sp.Symbol("lambda", positive=True)
eps = sp.Rational(1, 10)
w_rip = eps * sp.sin(lam * r) * sp.cos(th)
S_rip = sp.integrate(sp.integrate(
    kap * sp.sin(th) * (r**2 * sp.diff(w_rip, r) ** 2
                        + sp.diff(w_rip, th) ** 2),
    (th, 0, sp.pi)), (r, r1, r2))
lead = sp.limit(sp.expand(S_rip).subs({r1: 1, r2: 2}) / lam**2, lam, sp.oo)
check("V3.9 kappa sign UNFORCED by the route's conditions; for kappa < 0 "
      "the completed action is UNBOUNDED BELOW (ripple energy ~ kappa "
      "lambda^2 with |w| <= 1/10 fixed)", sp.simplify(lead) != 0)

# ======================================================================
# V4 -- claim 4: the EH density's TRUE Euler-Lagrange on the class
# ======================================================================
print("\n=== V4: claim 4 (A1-native) -- independent Ricci + full EL ===")

gd = sp.diag(-f, 1 / f, r**2 * (1 + w) ** 2,
             r**2 * sp.sin(th) ** 2 / (1 + w) ** 2)
gu = gd.inv()
n = 4
Gam = [[[sp.cancel(sum(gu[l, s] * (sp.diff(gd[s, i], xs[j])
                                   + sp.diff(gd[s, j], xs[i])
                                   - sp.diff(gd[i, j], xs[s])) / 2
                       for s in range(n)))
         for j in range(n)] for i in range(n)] for l in range(n)]
Ric = [[sp.together(
    sum(sp.diff(Gam[l][i][j], xs[l]) for l in range(n))
    - sum(sp.diff(Gam[l][i][l], xs[j]) for l in range(n))
    + sum(Gam[l][l][s] * Gam[s][i][j] for l in range(n) for s in range(n))
    - sum(Gam[l][j][s] * Gam[s][i][l] for l in range(n) for s in range(n)))
    for j in range(n)] for i in range(n)]
Rsc = sp.simplify(sum(gu[i, j] * Ric[i][j] for i in range(n) for j in range(n)))
densEH = sp.expand(r**2 * sp.sin(th) * Rsc)

check("V4.1 sqrt(-g) = r^2 sin th exactly (w-blind volume) on this class",
      sp.simplify(-gd.det() - r**4 * sp.sin(th) ** 2) == 0)
check("V4.2 densEH carries w_thth LINEARLY with coeff 2 sin th/(1+w)^3 "
      "(it IS a second-order density in w)",
      sp.simplify(densEH.coeff(sp.Derivative(w, (th, 2)))
                  - 2 * sp.sin(th) / (1 + w) ** 3) == 0)

# the route's operator (first-order EL) reproduces its 2 sin th:
ELw_first = sp.simplify(EL1(densEH, w).subs(w, 0).subs(f, F(r)).doit())
check("V4.3 FIRST-ORDER EL operator on densEH gives 2 sin th on every "
      "spherical background (the route's P4.8/P4.9 number reproduced)",
      sp.simplify(ELw_first - 2 * sp.sin(th)) == 0)

# the TRUE (second-order) EL:
ELw_true = sp.simplify(EL2(densEH, w).subs(w, 0).subs(f, F(r)).doit())
check("V4.4 TRUE EL_w[sqrt(-g) R] == 0 on EVERY spherical background "
      "(claim 4's 2 sin th is an operator artifact: a first-order EL "
      "applied to a second-order density)", ELw_true == 0)

# defect anatomy: the missing term is exactly +d_th^2(dL/dw_thth):
miss = sp.diff(densEH.coeff(sp.Derivative(w, (th, 2))), th, 2)
miss_sph = sp.simplify(miss.subs(w, 0).doit())
check("V4.5 the missing Euler-Lagrange term +d_th^2(dL/dw_thth)|sph "
      "== -2 sin th: it cancels the artifact exactly",
      sp.simplify(miss_sph + 2 * sp.sin(th)) == 0)

# geometric corroboration: the w-variation probes G^th_th - G^ph_ph,
# identically zero on any spherical metric. Verify the variational
# identity EL2_w[densEH] = -sqrt(-g)[G^thth dg_thth/dw + G^phph dg_phph/dw]
# at an exact rational off-spherical spot (validates my EL2 operator):
Gmix = [[sp.together(sum(gu[i, k] * Ric[k][j] for k in range(n))
                     - sp.Rational(1, 2) * Rsc * (1 if i == j else 0))
         for j in range(n)] for i in range(n)]
rhs_id = -(r**2 * sp.sin(th)) * (
    Gmix[2][2] * gu[2, 2] * sp.diff(gd[2, 2], w)
    + Gmix[3][3] * gu[3, 3] * sp.diff(gd[3, 3], w))
lhs_id = EL2(densEH, w).doit()
fx = sp.exp(r) * (2 + sp.sin(th) / 3)          # generic shaped f
wx = sp.Rational(1, 5) * r * sp.cos(th)        # generic shaped w
pt = {r: sp.Rational(3, 2), th: sp.pi / 3}
dnum = sp.simplify((lhs_id - rhs_id).subs(w, wx).subs(f, fx).doit().subs(pt))
check("V4.6 variational identity EL2_w = -sqrt(-g) G^munu d_w g_munu "
      "verified exactly at an off-spherical spot (operator validated)",
      sp.simplify(dnum) == 0)

# f-channel: within the P1 ansatz g_tt g_rr = -1 is LOCKED, so the
# f-variation probes G^t_t - G^r_r == 0 on every spherical metric:
ELf_true = sp.simplify(EL2(densEH, f).subs(w, 0).subs(f, F(r)).doit())
check("V4.7 TRUE EL_f[sqrt(-g) R] == 0 on EVERY spherical background "
      "within the P1 ansatz (B = 1/f locked, rho = r locked)",
      ELf_true == 0)

# q-channel: dg_rtheta/dq = 1 -> EL_q probes G^{r theta}; R_rtheta of the
# spherical diagonal metric vanishes identically:
gs = sp.diag(-F(r), 1 / F(r), r**2, r**2 * sp.sin(th) ** 2)
gsu = gs.inv()
GamS = [[[sp.cancel(sum(gsu[l, s] * (sp.diff(gs[s, i], xs[j])
                                     + sp.diff(gs[s, j], xs[i])
                                     - sp.diff(gs[i, j], xs[s])) / 2
                        for s in range(n)))
          for j in range(n)] for i in range(n)] for l in range(n)]
R_rth = sp.simplify(
    sum(sp.diff(GamS[l][1][2], xs[l]) for l in range(n))
    - sum(sp.diff(GamS[l][1][l], xs[2]) for l in range(n))
    + sum(GamS[l][l][s] * GamS[s][1][2] for l in range(n) for s in range(n))
    - sum(GamS[l][2][s] * GamS[s][1][l] for l in range(n) for s in range(n)))
check("V4.8 R_rtheta == 0 on every spherical background: the q-equation of "
      "kappa*EH is also blind (G^rth = 0)", sp.simplify(R_rth) == 0)

print("""
V4 CONSEQUENCE (claim 4 REFUTED): on the P1 class the EH density
contributes ZERO to all three field equations on every spherical
configuration -- C1 + kappa*EH ADMITS the banked vacuum for EVERY kappa.
The nonzero Einstein content of the banked vacuum (G^t_t = G^r_r =
(C-1)/r^2) lives entirely in the directions the P1 ansatz FREEZES
(the tt+rr trace combination and rho); the rho-sector A1 refusal
(a^2/2r^3) is INVISIBLE on this class. Far from being refused, the EH
density (after by-parts, first-order) is itself a SURVIVAL-PASSING
member of the completion family carrying w-derivatives -- the exact
opposite of the script's P4.8/P4.9 narrative. The 'no counterterm'
step and the kappa(r)/kappa(f) question are MOOT: nothing needs
cancelling.""")

# corroborate the Einstein content statement exactly:
Gtt_vac = sp.simplify((Gmix[0][0]).subs(w, 0).subs(f, f_vac).doit())
check("V4.9 G^t_t|banked = (C-1)/r^2 (nonzero for C != 1; the refusal "
      "content sits in the FROZEN directions)",
      sp.simplify(Gtt_vac - (C - 1) / r**2) == 0)
Gthth_vac = sp.simplify((Gmix[2][2]).subs(w, 0).subs(f, f_vac).doit())
check("V4.10 G^th_th|banked == 0 (the unfrozen angular direction sees "
      "nothing)", Gthth_vac == 0)

# ======================================================================
# summary
# ======================================================================
print("\n=== VERIFIER SUMMARY ===")
print(f"PASS: {len(PASS)}  FAIL: {len(FAIL)}")
if FAIL:
    print("FAILED CHECKS:")
    for nm in FAIL:
        print("  ", nm)
    raise SystemExit(1)
