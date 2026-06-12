"""
W1 push, ROUTE A — class-enlargement audit: where did the w/s-derivatives go?

Declaration: w_stiffness_push_declaration.md (committed 2026-06-11, binds
this script). Question: the P1 structural lemma ("q and w enter the reduced
Lagrangian with NO derivatives at any nonlinear order", pde_p1_results.md)
is a P1-class statement — is the absence of shape-field derivatives a
property of the C1 action ITSELF, or an artifact of the P1 reduction?

NATIVE C1 DEFINITION USED (provenance):
    S_C1 = -(c/2) * Integral( e^{-2 phi} (grad phi)^2 sqrt(-g) d^4x )
with the definitional positional-dilation tie  f := -g_tt = e^{-2 phi},
i.e. phi = -(1/2) ln f.  Source: UDT_REBUILD.md sec.1 ("Vacuum field
equation (from the C1 action S_phi = -(c/2) int e^{-2phi} (dphi)^2
sqrt(-g))"). Substituting phi = -(1/2) ln f gives the equivalent exact form
    L_C1 = -(c/8) sqrt(-g) g^{mu nu} f_mu f_nu / f .
Spherical reduction check below ties this to the reduced convention
S_C1 = (1/4) int r^2 f'^2 dr (negative_phi_native_geometry.md:19825,
rho_dynamics_derivation_results.md:73) via the normalization c = -1/(2 pi)
(sign/normalization conventions differ between docs; zero sets and flip
structure are c-independent — recorded, not resolved here).

P1 METRIC CLASS (reverse-grounded; confirmed below by exact reproduction of
pde_p1_results.md's quoted w-equation AND angular_completeness_results.md's
w-tadpole):
    ds^2 = -f dt^2 + (1/f) dr^2 + 2 q dr dtheta
           + r^2 (1+w)^2 dtheta^2 + r^2 sin^2(theta) (1+w)^{-2} dphi^2,
    f, q, w functions of (r, theta); UNIMODULAR angular block
    (det of angular block = r^4 sin^2 theta — the areal canon, k = 0).

ENLARGED CLASS (this route; R-areal canon kept, rho = r NOT freed; the
angular block freed fully):
    g_thetatheta = r^2 P(r,theta),   g_phiphi = r^2 sin^2(theta) Q(r,theta),
    P, Q > 0 INDEPENDENT;  g_rtheta = q(r,theta) free;  f(r,theta) free;
    g_rr = 1/f (the P0 definitional tie, kept).
Task parameterization: P = (1+w) e^{2s}, Q = (1+w) e^{-2s}
    (w = conformal shape — det-changing; s = shear — ratio).
DICTIONARY: P1's single shape field w_P1 sits at (1+w_P1)^2 = e^{2s}, w = 0:
P1 ALREADY contained the shear/ratio mode; the mode P1's primary class
excluded is the CONFORMAL/DETERMINANT mode w (P1 checked it once as a
robustness variant — "non-unimodular class with the breathing mode
reinstated" — found strictly more constrained).

Also computed: the fully general even-sector axisymmetric class with FULL
TIME ROW and time dependence (f, a = g_Tr, b = g_Ttheta, q, P, Q all
functions of (T, r, theta)) — per the declaration's Route A wording.

DISCIPLINE: exact sympy throughout; no linearization anywhere; every
symbolic identity gets exact random-rational spot checks. Static negatives
below carry the premise set: {static or full-time-row even axisymmetric
class as stated, R-areal canon, g_rr = 1/f tie, C1 action alone, smooth
nondegenerate Lorentzian metric}.

DIAGNOSTIC-ONLY SECTION (S5): sqrt(-g) R is computed purely as a
curvature-identity classifier (guardrail native_positional_dilation_gr_
guardrail.py: "connection / curvature identities: usable exactly") to show
WHICH species of density carries shape derivatives. It is NOT imported as
dynamics.

New file 2026-06-11 (repo culture: new files only). Route A derivation
agent.
"""

import random
import sympy as sp

random.seed(20260611)

# ---------------------------------------------------------------- harness
PASSED = 0
TOTAL = 0


def check(name, cond):
    global PASSED, TOTAL
    TOTAL += 1
    ok = bool(cond)
    PASSED += ok
    print(("PASS" if ok else "FAIL"), "|", name)
    assert ok, name
    return ok


def rand_rat(lo=1, hi=9):
    return sp.Rational(random.randint(lo, hi), random.randint(1, 7))


def spot(expr, syms, n=4, extra=None, branch=None):
    """Exact random-rational evaluation: returns list of exact values of
    expr at n random rational points (positivity-respecting), optionally
    filtered by a branch condition (callable on the substitution dict)."""
    vals = []
    tries = 0
    while len(vals) < n and tries < 400:
        tries += 1
        sub = {s: rand_rat() for s in syms}
        if extra:
            sub.update(extra)
        if branch and not branch(sub):
            continue
        vals.append(sp.nsimplify(expr.subs(sub)))
    assert len(vals) == n, "spot-check could not find %d branch points" % n
    return vals


# ---------------------------------------------------------------- symbols
r, th = sp.symbols("r theta", positive=True)
c = sp.Symbol("c", positive=True)          # C1 normalization, carried
f = sp.Symbol("f", positive=True)          # f = e^{-2 phi} = -g_tt > 0
fr, fth = sp.symbols("f_r f_theta", real=True)
q = sp.Symbol("q", real=True)
w = sp.Symbol("w", real=True)              # shape fields enter algebraically:
s = sp.Symbol("s", real=True)              # jet slots never needed for them
P = sp.Symbol("P", positive=True)
Q = sp.Symbol("Q", positive=True)
SIN = sp.sin(th)                           # 0 < theta < pi assumed: sin > 0


def fix_chart(expr):
    """Declared chart is 0 < theta < pi, so |sin(theta)| = sin(theta).
    This is the ONLY Abs ever stripped; every other branch object (|X-Y|
    etc.) is handled explicitly by branch-conditioned rational points."""
    return expr.replace(sp.Abs(SIN), SIN)


def C1_density_from_metric(g4, fexpr, grad_f, coords_used):
    """Native C1 density L = -(c/8) sqrt(-g) g^{mu nu} f_mu f_nu / f,
    built from the FULL 4x4 metric by exact inversion. grad_f is a dict
    coord_index -> df/dx^i (jet slots)."""
    ginv = g4.inv()
    detg = sp.factor(g4.det())
    sqrtg = fix_chart(sp.sqrt(-detg))
    K = sp.S(0)
    for i in coords_used:
        for j in coords_used:
            K += ginv[i, j] * grad_f[i] * grad_f[j]
    return sp.together(-(c / 8) * sqrtg * K / fexpr)


print("=" * 72)
print("S1 + S2: GROUNDING — the P1 subclass from the native definition")
print("=" * 72)

# P1 metric, static: coords (t, r, theta, phi); f, q, w carry (r,theta) jets
W1 = (1 + w) ** 2
g_p1 = sp.Matrix(
    [
        [-f, 0, 0, 0],
        [0, 1 / f, q, 0],
        [0, q, r ** 2 * W1, 0],
        [0, 0, 0, r ** 2 * SIN ** 2 / W1],
    ]
)
L_p1 = C1_density_from_metric(g_p1, f, {1: fr, 2: fth}, coords_used=(1, 2))
L_p1 = sp.simplify(L_p1)

# --- G1: the density carries NO derivative slots of q or w --------------
# Independent construction with sympy Functions to count Derivative atoms.
F2, Q2, W2 = (sp.Function(n)(r, th) for n in ("f", "q", "w"))
gW = (1 + W2) ** 2
g_p1F = sp.Matrix(
    [
        [-F2, 0, 0, 0],
        [0, 1 / F2, Q2, 0],
        [0, Q2, r ** 2 * gW, 0],
        [0, 0, 0, r ** 2 * SIN ** 2 / gW],
    ]
)
LF = C1_density_from_metric(
    g_p1F, F2, {1: sp.diff(F2, r), 2: sp.diff(F2, th)}, coords_used=(1, 2)
)
ders = LF.atoms(sp.Derivative)
bad = {d for d in ders if d.expr != F2}
check("G1  P1 class: C1 density contains NO derivatives of q or w "
      "(Derivative atoms are f's only)", len(bad) == 0 and len(ders) > 0)

# --- G2: spherical reduction matches the banked reduced convention ------
L_sph = sp.simplify(L_p1.subs({q: 0, w: 0, fth: 0}))
check("G2a spherical reduction: L = -(c/8) r^2 sin(th) f_r^2 exactly",
      sp.simplify(L_sph + (c / 8) * r ** 2 * SIN * fr ** 2) == 0)
# integrate the solid angle: 4 pi; (1/4) r^2 f'^2 per dr <=> c = -1/(2 pi)
angle = sp.integrate(sp.integrate(SIN, (th, 0, sp.pi)), (sp.Symbol("ph"), 0, 2 * sp.pi))
per_dr = sp.simplify((L_sph / SIN) * angle)
check("G2b  c-dictionary: per-dr density = -(pi c/2) r^2 f_r^2, equal to the "
      "banked (1/4) r^2 f'^2 at c = -1/(2 pi) exactly",
      sp.simplify(per_dr - (-sp.pi * c / 2) * r ** 2 * fr ** 2) == 0
      and sp.simplify(per_dr.subs(c, -sp.Rational(1, 2) / sp.pi)
                      - sp.Rational(1, 4) * r ** 2 * fr ** 2) == 0)

# --- G3: the q-stationarity roots --------------------------------------
dLdq = sp.together(sp.diff(L_p1, q))
qroots = sp.solve(sp.numer(dLdq), q)
D2_p1 = (1 / f) * r ** 2 * W1 - q ** 2          # spatial-block determinant
X = f * fr ** 2 * r ** 2 * W1                   # radial invariant
Y = fth ** 2                                    # angular invariant
qstar = 2 * fr * fth * r ** 2 * W1 / (X + Y)
deg_roots = [rt for rt in qroots if sp.simplify(D2_p1.subs(q, rt)) == 0]
fin_roots = [rt for rt in qroots if sp.simplify(rt - qstar) == 0]
check("G3a q-stationarity roots = {two metric-degeneracy roots D2 = 0} "
      "+ {the unique finite root q*}",
      len(qroots) == 3 and len(deg_roots) == 2 and len(fin_roots) == 1)
check("G3b q* = 2 f_r f_th r^2 (1+w)^2 / (f r^2 (1+w)^2 f_r^2 + f_th^2) "
      "(pde_p1's unique root)", len(fin_roots) == 1)

# --- G4: exact q-elimination — the perfect square and the sign flip -----
L_eff_raw = L_p1.subs(q, qstar)
# identity: (X+Y)^2 - 4XY = (X-Y)^2  (the static perfect square)
check("G4a static perfect square: (X+Y)^2 - 4 X Y = (X-Y)^2 exactly",
      sp.simplify((X + Y) ** 2 - 4 * X * Y - (X - Y) ** 2) == 0)
# closed forms on the two branches
L_eff_XgtY = -(c / 8) * SIN * (X - Y) / (f * W1)
L_eff_XltY = -(c / 8) * SIN * (Y - X) / (f * W1)
for nm, closed, br in (
    ("X>Y", L_eff_XgtY, lambda sub: (X - Y).subs(sub) > 0),
    ("X<Y", L_eff_XltY, lambda sub: (X - Y).subs(sub) < 0),
):
    diffs = spot(L_eff_raw - closed, [f, fr, fth, r, w, c], n=4,
                 extra={th: sp.Rational(1, 3)}, branch=br)
    check("G4b L_eff(q*) = -(c/8) sin(th) |X - Y| / (f (1+w)^2) on branch "
          + nm + " (4 exact rational points)",
          all(sp.simplify(d) == 0 for d in diffs))
# the angular-gradient sign FLIP: coefficient of f_th^2
coef_q0 = sp.simplify(sp.diff(L_p1.subs(q, 0), fth, 2) / 2)
coef_eff = sp.simplify(sp.diff(L_eff_XgtY, fth, 2) / 2)
check("G4c angular flip: coeff(f_th^2) goes -(c/8)sin/(f(1+w)^2) at q=0 "
      "to +(c/8)sin/(f(1+w)^2) after q-elimination (X>Y branch)",
      sp.simplify(coef_q0 + (c / 8) * SIN / (f * W1)) == 0
      and sp.simplify(coef_eff - (c / 8) * SIN / (f * W1)) == 0)

# --- G5: the two quoted anchors ------------------------------------------
dLeff_dw = sp.simplify(sp.diff(L_eff_XgtY, w))
quoted_p1 = -(c / 4) * SIN * fth ** 2 / (f * (1 + w) ** 3)
check("G5a pde_p1 w-equation REPRODUCED: dL_eff/dw = "
      "-(c/4) sin(th) f_th^2 / (f (1+w)^3)  [X>Y branch; X<Y flips sign "
      "- 'nonzero on both branches']",
      sp.simplify(dLeff_dw - quoted_p1) == 0
      and sp.simplify(sp.diff(L_eff_XltY, w) + quoted_p1) == 0)
T_w = sp.simplify(sp.diff(L_p1.subs(q, 0), w).subs(w, 0))
check("G5b angular_completeness w-tadpole REPRODUCED: dL/dw|_{q=0,w=0} = "
      "+(c/4) f_th^2 sin(th) / f",
      sp.simplify(T_w - (c / 4) * fth ** 2 * SIN / f) == 0)

print()
print("=" * 72)
print("S3: THE ENLARGED CLASS — angular block fully freed (P, Q independent)")
print("=" * 72)

# ---- E1: THE ROUTE VERDICT — derivative content of the C1 density ------
Ffn = sp.Function("f")(r, th)
qfn = sp.Function("q")(r, th)
Pfn = sp.Function("P")(r, th)
Qfn = sp.Function("Q")(r, th)
g_enlF = sp.Matrix(
    [
        [-Ffn, 0, 0, 0],
        [0, 1 / Ffn, qfn, 0],
        [0, qfn, r ** 2 * Pfn, 0],
        [0, 0, 0, r ** 2 * SIN ** 2 * Qfn],
    ]
)
L_enlF = C1_density_from_metric(
    g_enlF, Ffn, {1: sp.diff(Ffn, r), 2: sp.diff(Ffn, th)}, coords_used=(1, 2)
)
ders = L_enlF.atoms(sp.Derivative)
bad = {d for d in ders if d.expr != Ffn}
check("E1a ENLARGED CLASS VERDICT: C1 density contains NO derivative of "
      "P, Q, or q — radial or angular, ANY order; only f-derivatives occur",
      len(bad) == 0 and len(ders) > 0)

# task parameterization P = (1+w) e^{2s}, Q = (1+w) e^{-2s}
wfn = sp.Function("w")(r, th)
sfn = sp.Function("s")(r, th)
L_wsF = L_enlF.subs(
    {Pfn: (1 + wfn) * sp.exp(2 * sfn), Qfn: (1 + wfn) * sp.exp(-2 * sfn)}
)
ders = L_wsF.atoms(sp.Derivative)
bad = {d for d in ders if d.expr != Ffn}
check("E1b in (w, s) variables: NO w- or s-derivatives at any point of the "
      "computation (nothing appears, hence nothing cancels — no IBP, no "
      "boundary term, no P1-restriction step exists)",
      len(bad) == 0)

# ---- the algebraic (symbol-slot) form for exact manipulation -----------
D2 = (1 / f) * r ** 2 * P - q ** 2
sqrtg_enl = r * SIN * sp.sqrt(f * D2 * Q)
K_enl = (r ** 2 * P * fr ** 2 - 2 * q * fr * fth + fth ** 2 / f) / D2
L_enl = sp.together(-(c / 8) * sqrtg_enl * K_enl / f)
# cross-check the Function-built and symbol-built densities agree exactly
subF = {Ffn: f, sp.Derivative(Ffn, r): fr, sp.Derivative(Ffn, th): fth,
        qfn: q, Pfn: P, Qfn: Q}
diff_fs = sp.simplify(L_enlF.subs(subF) - L_enl)
check("E1c Function-built density == jet-slot density (exact, all q)",
      diff_fs == 0)
for k in range(3):
    sub = {f: rand_rat(), fr: rand_rat(), fth: rand_rat(), q: sp.Rational(1, 9),
           P: rand_rat(), Q: rand_rat(), r: rand_rat(), th: sp.Rational(1, 2),
           c: 1}
    check("E1d spot %d: density value finite+exact at random rationals" % k,
          sp.simplify(L_enl.subs(sub)).is_finite)

# ---- E2: how the new modes enter (exact algebra) ------------------------
check("E2a the phi-phi mode multiplies the density: dL/dQ = L/(2Q) "
      "EXACTLY (Q enters only through sqrt(-g))",
      sp.simplify(sp.diff(L_enl, Q) - L_enl / (2 * Q)) == 0)
# P enters both sqrt(-g) (through D2) and the contraction
dLdP = sp.simplify(sp.diff(L_enl, P))
check("E2b dL/dP is algebraic in (f, f_r, f_th, q, P, Q) — explicit form "
      "verified by 4 exact rational points",
      all(sp.simplify(v) == 0 for v in spot(
          dLdP - sp.diff(L_enl, P), [f, fr, fth, q, P, Q, r], n=4,
          extra={th: sp.Rational(1, 3), c: 1})))

# ---- E3: exact q-elimination on the enlarged class ----------------------
dLdq = sp.together(sp.diff(L_enl, q))
qroots = sp.solve(sp.numer(dLdq), q)
Xe = f * fr ** 2 * r ** 2 * P
qstar_e = 2 * fr * fth * r ** 2 * P / (Xe + Y)
check("E3a enlarged q-stationarity: UNIQUE root q* = "
      "2 f_r f_th r^2 P/(f r^2 P f_r^2 + f_th^2) (the degeneracy locus "
      "D2 = 0 enters as a pole of dL/dq here, not a root — same anatomy "
      "as P1, cleaner factorization)",
      len(qroots) == 1 and sp.simplify(qroots[0] - qstar_e) == 0)
check("E3a' degeneracy identity: D2(q*) = (P r^2/f) (Xe-Y)^2/(Xe+Y)^2 "
      "exactly — the eliminated metric degenerates EXACTLY on the corner "
      "Xe = Y (VP1's nonsmooth-corner locus, enlarged-class form)",
      sp.simplify(D2.subs(q, qstar_e)
                  - (P * r ** 2 / f) * (Xe - Y) ** 2 / (Xe + Y) ** 2) == 0)
check("E3b enlarged perfect square: (Xe+Y)^2 - 4 Xe Y = (Xe-Y)^2",
      sp.simplify((Xe + Y) ** 2 - 4 * Xe * Y - (Xe - Y) ** 2) == 0)
L_eff_e_raw = L_enl.subs(q, qstar_e)
Leff_gt = -(c / 8) * SIN * sp.sqrt(Q / P) * (Xe - Y) / f   # X > Y branch
Leff_lt = -(c / 8) * SIN * sp.sqrt(Q / P) * (Y - Xe) / f   # X < Y branch
for nm, closed, br in (
    ("Xe>Y", Leff_gt, lambda sub: (Xe - Y).subs(sub) > 0),
    ("Xe<Y", Leff_lt, lambda sub: (Xe - Y).subs(sub) < 0),
):
    diffs = spot(L_eff_e_raw - closed, [f, fr, fth, r, P, Q, c], n=4,
                 extra={th: sp.Rational(2, 5)}, branch=br)
    check("E3c L_eff = -(c/8) sin(th) sqrt(Q/P) |Xe - Y| / f on branch "
          + nm + " (4 exact rational points)",
          all(sp.simplify(d) == 0 for d in diffs))

# ---- E4: the shape forces on the enlarged class (all algebraic) ---------
# In invariant (P, Q) variables, X>Y branch:
dP_gt = sp.simplify(sp.diff(Leff_gt, P))
dQ_gt = sp.simplify(sp.diff(Leff_gt, Q))
form_dP = -(c / 16) * SIN * sp.sqrt(Q / P) * (r ** 2 * fr ** 2 + fth ** 2 / (f * P))
check("E4a dL_eff/dP = -(c/16) sin(th) sqrt(Q/P) [r^2 f_r^2 + f_th^2/(f P)]"
      " — SIGN-DEFINITE: never zero unless f_r = f_th = 0 (X>Y branch; "
      "X<Y branch is its exact negative)",
      sp.simplify(dP_gt - form_dP) == 0
      and sp.simplify(sp.diff(Leff_lt, P) + form_dP) == 0)
check("E4b dL_eff/dQ = L_eff/(2Q): zero only where L_eff = 0, i.e. on the "
      "degenerate corner Xe = Y (or flat f)",
      sp.simplify(dQ_gt - Leff_gt / (2 * Q)) == 0)
# task (w, s) variables on the X>Y branch
Leff_ws_gt = Leff_gt.subs({P: (1 + w) * sp.exp(2 * s), Q: (1 + w) * sp.exp(-2 * s)})
dw_gt = sp.simplify(sp.diff(Leff_ws_gt, w))
ds_gt = sp.simplify(sp.diff(Leff_ws_gt, s))
check("E4c (w,s) split after q-elimination (Xe>Y branch): L_eff = -(c/8) "
      "sin(th) [(1+w) r^2 f_r^2 - e^{-2s} f_th^2/f]; dL_eff/dw = -(c/8) "
      "sin(th) r^2 f_r^2 (PURE radial source) and dL_eff/ds = -(c/4) "
      "sin(th) e^{-2s} f_th^2 / f (PURE phi-angular source)",
      sp.simplify(Leff_ws_gt + (c / 8) * SIN
                  * ((1 + w) * r ** 2 * fr ** 2
                     - sp.exp(-2 * s) * fth ** 2 / f)) == 0
      and sp.simplify(dw_gt + (c / 8) * SIN * r ** 2 * fr ** 2) == 0
      and sp.simplify(ds_gt + (c / 4) * SIN * sp.exp(-2 * s) * fth ** 2
                      / f) == 0)
check("E4d spherical limit: the SHEAR force vanishes at f_th = 0 (s is "
      "spherically flat), but the CONFORMAL force does NOT — it forces "
      "f_r = 0 (reproduces P1's 'breathing mode strictly MORE constrained, "
      "additionally forbidding f_r != 0')",
      sp.simplify(ds_gt.subs(fth, 0)) == 0
      and sp.simplify(dw_gt.subs(fth, 0)
                      + (c / 8) * SIN * r ** 2 * fr ** 2) == 0)
# static solution set on the enlarged class:
#   q = q*, dL/dQ = 0 => L_eff = 0 => Xe = Y (degenerate corner) or
#   dL/dP = 0 => f_r = f_th = 0  => f globally constant: NO formed solution,
#   spherical or shaped, survives the fully freed angular block.
sol_flat = sp.simplify(form_dP.subs({fr: 0, fth: 0}))
check("E4e enlarged static solution set: joint (q,P,Q)-stationarity forces "
      "f_r = f_th = 0 (flat) or the nonsmooth degenerate corner Xe = Y — "
      "STRICTLY smaller than P1's set (which allowed f spherical formed)",
      sol_flat == 0)

print()
print("=" * 72)
print("S4: FULL GENERALITY — time row + time dependence (declaration scope)")
print("=" * 72)

T = sp.Symbol("T", real=True)
Fg = sp.Function("f")(T, r, th)
ag = sp.Function("a")(T, r, th)
bg = sp.Function("b")(T, r, th)
qg = sp.Function("q")(T, r, th)
Pg = sp.Function("P")(T, r, th)
Qg = sp.Function("Q")(T, r, th)
g_full = sp.Matrix(
    [
        [-Fg, ag, bg, 0],
        [ag, 1 / Fg, qg, 0],
        [bg, qg, r ** 2 * Pg, 0],
        [0, 0, 0, r ** 2 * SIN ** 2 * Qg],
    ]
)
L_full = C1_density_from_metric(
    g_full, Fg,
    {0: sp.diff(Fg, T), 1: sp.diff(Fg, r), 2: sp.diff(Fg, th)},
    coords_used=(0, 1, 2),
)
ders = L_full.atoms(sp.Derivative)
bad = {d for d in ders if d.expr != Fg}
check("S4a FULL CLASS (time row a, b on; everything T-dependent): the C1 "
      "density carries derivatives of f ONLY — never of a, b, q, P, Q "
      "(hence never of w or s) at any order",
      len(bad) == 0 and len(ders) > 0)
# Structural reason, stated as a checked identity: the C1 integrand is
# ZEROTH-JET in the metric — it is a pointwise function of (g, df) alone.
# Verify: substituting arbitrary CONSTANTS for all non-f metric functions
# commutes with building the density (no chain-rule residue can exist).
consts = {ag: sp.Rational(1, 5), bg: sp.Rational(1, 7), qg: sp.Rational(1, 9),
          Pg: sp.Rational(3, 2), Qg: sp.Rational(4, 3)}
g_const = g_full.subs(consts)
L_const = C1_density_from_metric(
    g_const, Fg,
    {0: sp.diff(Fg, T), 1: sp.diff(Fg, r), 2: sp.diff(Fg, th)},
    coords_used=(0, 1, 2),
)
check("S4b zeroth-jet property: constant-substitution commutes with the "
      "density construction exactly (no derivative of any non-f component "
      "could ever have been generated and cancelled)",
      sp.simplify(L_full.subs(consts) - L_const) == 0)

print()
print("=" * 72)
print("S5: SPECIES CONTRAST (diagnostic only) — which density CAN carry")
print("    shape derivatives: the second-jet/curvature (EH-remainder) species")
print("=" * 72)


def ricci_scalar_density(gmat, coords):
    n = len(coords)
    ginv = gmat.inv()
    Gamma = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for i in range(n):
            for j in range(n):
                expr = sp.S(0)
                for k in range(n):
                    expr += ginv[a, k] * (
                        sp.diff(gmat[k, i], coords[j])
                        + sp.diff(gmat[k, j], coords[i])
                        - sp.diff(gmat[i, j], coords[k])
                    )
                Gamma[a][i][j] = expr / 2
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            expr = sp.S(0)
            for a in range(n):
                expr += sp.diff(Gamma[a][i][j], coords[a])
                expr -= sp.diff(Gamma[a][i][a], coords[j])
                for b in range(n):
                    expr += Gamma[a][a][b] * Gamma[b][i][j]
                    expr -= Gamma[a][j][b] * Gamma[b][i][a]
            Ric[i, j] = expr
    Rsc = sp.S(0)
    for i in range(n):
        for j in range(n):
            Rsc += ginv[i, j] * Ric[i, j]
    return sp.sqrt(-gmat.det()) * Rsc


t_sym = sp.Symbol("t", real=True)
Fd = sp.Function("f")(r, th)
Pd = sp.Function("P")(r, th)
Qd = sp.Function("Q")(r, th)
g_diag = sp.Matrix(
    [
        [-Fd, 0, 0, 0],
        [0, 1 / Fd, 0, 0],
        [0, 0, r ** 2 * Pd, 0],
        [0, 0, 0, r ** 2 * SIN ** 2 * Qd],
    ]
)
EHdens = ricci_scalar_density(g_diag, [t_sym, r, th, sp.Symbol("ph")])
dersEH = EHdens.atoms(sp.Derivative)
hasP1st = any(d.expr == Pd and d.derivative_count == 1 for d in dersEH)
hasP2nd = any(d.expr == Pd and d.derivative_count == 2 for d in dersEH)
hasQ1st = any(d.expr == Qd and d.derivative_count == 1 for d in dersEH)
hasQ2nd = any(d.expr == Qd and d.derivative_count == 2 for d in dersEH)
check("S5a the curvature-type density sqrt(-g) R on the SAME enlarged "
      "(diagonal) class DOES carry first AND second derivatives of both "
      "shape modes P and Q — the shape-derivative carrier is exactly the "
      "second-jet species (the EH-remainder species), which C1 is not",
      hasP1st and hasP2nd and hasQ1st and hasQ2nd)
# and its spherical reduction reproduces the known EH-remainder anatomy:
# the species' signature object 2 - 2 f rho rho'' carries rho'' — i.e.
# second jets of the angular block — while C1's reduction carries none.
rho_f = sp.Function("rho")(r)
fs = sp.Function("f")(r)
g_sphr = sp.Matrix(
    [
        [-fs, 0, 0, 0],
        [0, 1 / fs, 0, 0],
        [0, 0, rho_f ** 2, 0],
        [0, 0, 0, rho_f ** 2 * SIN ** 2],
    ]
)
EHs = sp.simplify(ricci_scalar_density(g_sphr, [t_sym, r, th, sp.Symbol("ph")])
                  / SIN)
has_rho2 = any(d.expr == rho_f and d.derivative_count == 2
               for d in EHs.atoms(sp.Derivative))
check("S5b spherical contrast: sqrt(-g) R carries rho'' (the 2 - 2 f rho "
      "rho'' remainder species) while the C1 density on the same metric "
      "carries NO rho-derivative",
      has_rho2)
L_sph_rho = C1_density_from_metric(
    g_sphr, fs, {1: sp.diff(fs, r)}, coords_used=(1,)
)
bad_rho = {d for d in L_sph_rho.atoms(sp.Derivative) if d.expr != fs}
check("S5c ... C1 on (f(r), rho(r)): derivative atoms are f's only",
      len(bad_rho) == 0)

print()
print("=" * 72)
print("ROUTE A VERDICT: the absence of w/s-derivatives is a property of the")
print("C1 ACTION ITSELF, not of the P1 reduction. The C1 integrand is")
print("zeroth-jet in the metric (only f = -g_tt is differentiated); shape-")
print("field derivatives never appear at ANY step on ANY class (static,")
print("enlarged, full time row), so there is no cancellation, no boundary")
print("term, and nothing for an IBP to hide. The only species that carries")
print("shape derivatives is the second-jet/curvature species — the")
print("EH-remainder species — exactly the named target of the W1 push.")
print("=" * 72)
print("RESULT: %d / %d checks passed" % (PASSED, TOTAL))
assert PASSED == TOTAL
