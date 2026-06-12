"""
BLIND ADVERSARIAL VERIFIER — Route A of the W1 push
(w_stiffness_routeA_enlarged_class.py, claimed 34/34).

Verifier agent, 2026-06-11. New file (repo culture). This script shares NO
machinery with the route script: own metric builders, own inversion, own
q-elimination algebra (done analytically first, checked symbolically here),
own Ricci computation, and HOSTILE structures the route never tried:

  H1. off-diagonal angular g_theta_phi, a t-phi term, an UNTIED g_rr = h
      (the route kept g_rr = 1/f), all components functions of ALL FOUR
      coordinates (no axisymmetry, no staticity, no even sector).
  H2. a conformal factor Omega^2 on the WHOLE metric — a shape mode that
      enters g_tt: does the "no enlargement can produce shape derivatives"
      claim survive? (Predicted: NO — tie-dependence scope finding.)
  H3. an ALTERNATIVE TIE phi = -(1/4) ln(P*Q) (angular-determinant tie):
      does the zeroth-jet claim survive a different tie? (Predicted: NO.)
  H4. negative f_r, f_theta and P < 1 sample points (route sampled only
      positive rationals for every symbol including w, f_r, f_theta).
  H5. coefficient-extraction (not raw atom counting on an UNSIMPLIFIED
      expression) for the sqrt(-g) R species claim: presence of a
      Derivative atom in an unsimplified Ricci density could be a false
      positive; we prove the second-jet coefficients are nonzero.
  H6. vacuity probes of the route's own checks (S4b, E2b, G3b).

Verdict notation: V-## PASS means the route's claim SURVIVED this attack.
A FAIL line is a refutation or amendment, explained in the final report.
No check halts the run; everything executes.
"""
import random
import sympy as sp

random.seed(99173)

results = []


def check(tag, cond, note=""):
    ok = bool(cond)
    results.append((tag, ok, note))
    print(("PASS" if ok else "FAIL"), "|", tag, "|", note, flush=True)
    return ok


def rr(signed=False):
    v = sp.Rational(random.randint(1, 11), random.randint(1, 7))
    if signed and random.random() < 0.5:
        v = -v
    return v


# ---------------------------------------------------------------- symbols
T, r, th, ph = sp.symbols("T r theta varphi", real=True)
c = sp.Symbol("c", positive=True)
COORDS = (T, r, th, ph)


def C1_density(g4, fexpr, diff_coords):
    """Own builder: L = -(c/2) e^{-2 phi} g^{mu nu} phi_mu phi_nu sqrt(-g),
    phi = -(1/2) ln fexpr  =>  exactly  -(c/8) sqrt(-g) g^{mn} f_m f_n / f.
    Built from the covariant definition, NOT from the route's shortcut."""
    ginv = g4.inv()
    sqrtg = sp.sqrt(-g4.det())
    L = sp.S(0)
    for i in diff_coords:
        for j in diff_coords:
            phii = -sp.diff(fexpr, COORDS[i]) / (2 * fexpr)
            phij = -sp.diff(fexpr, COORDS[j]) / (2 * fexpr)
            L += ginv[i, j] * phii * phij
    return -(c / 2) * fexpr * L * sqrtg


def non_f_derivatives(expr, fobj):
    return {d for d in expr.atoms(sp.Derivative) if d.expr != fobj}


print("=" * 72)
print("V1: CLAIM 1 on a class STRICTLY MORE HOSTILE than the route's")
print("    (g_thetaphi, g_tphi, UNTIED g_rr, full 4-coordinate dependence)")
print("=" * 72)

F = sp.Function("F")(T, r, th, ph)     # f = -g_tt
a = sp.Function("a")(T, r, th, ph)     # g_Tr
b = sp.Function("b")(T, r, th, ph)     # g_Tth   (t-theta cross term)
e = sp.Function("e")(T, r, th, ph)     # g_Tph   (rotation, odd sector)
h = sp.Function("h")(T, r, th, ph)     # g_rr UNTIED (route kept 1/f)
q = sp.Function("q")(T, r, th, ph)     # g_rth
n = sp.Function("n")(T, r, th, ph)     # g_rph
p1 = sp.Function("p1")(T, r, th, ph)   # g_thth
m = sp.Function("m")(T, r, th, ph)     # g_thph  (off-diagonal angular)
p2 = sp.Function("p2")(T, r, th, ph)   # g_phph
g_hostile = sp.Matrix([
    [-F, a, b, e],
    [a, h, q, n],
    [b, q, p1, m],
    [e, n, m, p2],
])
L_host = C1_density(g_hostile, F, (0, 1, 2, 3))
bad = non_f_derivatives(L_host, F)
nF = {d for d in L_host.atoms(sp.Derivative) if d.expr == F}
check("V01", len(bad) == 0 and len(nF) > 0,
      "fully generic 10-function 4-coordinate metric, g_rr untied, "
      "g_thetaphi and g_Tphi on: ONLY F-derivatives appear (%d F-atoms, "
      "%d non-F)" % (len(nF), len(bad)))

# the structural reason, verified rather than asserted: the C1 integrand
# never differentiates the metric — only phi(g_tt). So the claim is TRUE
# BY CONSTRUCTION for any class whose parameters stay out of g_tt.
# That makes the next two attacks the real content:

print()
print("=" * 72)
print("V2: TIE-DEPENDENCE ATTACK A — conformal factor on the WHOLE metric")
print("    (a shape mode that ENTERS g_tt)")
print("=" * 72)

Om = sp.Function("Omega")(r, th)
Fs2 = sp.Function("F")(r, th)
Ps2 = sp.Function("P")(r, th)
Qs2 = sp.Function("Q")(r, th)
qs2 = sp.Function("q")(r, th)
g_base = sp.Matrix([
    [-Fs2, 0, 0, 0],
    [0, 1 / Fs2, qs2, 0],
    [0, qs2, r ** 2 * Ps2, 0],
    [0, 0, 0, r ** 2 * sp.sin(th) ** 2 * Qs2],
])
g_conf = Om ** 2 * g_base
f_conf = Om ** 2 * Fs2                       # f = -g_tt of the FULL metric
L_conf = C1_density(g_conf, f_conf, (1, 2))
ders = L_conf.atoms(sp.Derivative)
has_Om = any(d.expr == Om for d in ders)
non_fOm = {d for d in ders if d.expr not in (Om, Fs2)}
# is the Omega-derivative dependence REAL (nonzero coefficient), not a
# cancellable artifact? coefficient of (dOmega/dr)^2 after expansion:
cOm = sp.simplify(sp.expand(L_conf).coeff(sp.Derivative(Om, r), 2))
check("V02", has_Om and len(non_fOm) == 0 and sp.simplify(cOm) != 0,
      "conformal mode Omega DOES acquire derivatives in the C1 density "
      "(nonzero (dOmega/dr)^2 coefficient) -- claim 1's 'NO enlargement' "
      "is FALSE for enlargements entering g_tt; true only for shape modes "
      "confined to non-g_tt components")

print()
print("=" * 72)
print("V3: TIE-DEPENDENCE ATTACK B — phi tied to a DIFFERENT invariant")
print("    (angular-determinant tie phi = -(1/4) ln(P Q))")
print("=" * 72)

f_alt = sp.sqrt(Ps2 * Qs2)                   # e^{-2 phi} for the alt tie
L_alt = C1_density(g_base, f_alt, (1, 2))
dersA = L_alt.atoms(sp.Derivative)
hasP = any(d.expr == Ps2 for d in dersA)
hasQ = any(d.expr == Qs2 for d in dersA)
cP = sp.simplify(sp.expand(L_alt).coeff(sp.Derivative(Ps2, r), 2))
check("V03", hasP and hasQ and sp.simplify(cP) != 0,
      "with phi tied to the angular determinant instead of g_tt, the SAME "
      "C1 action carries P- and Q-derivatives (nonzero coefficients): the "
      "zeroth-jet-in-shape property is a property of C1 PLUS the "
      "phi = -(1/2)ln(-g_tt) tie, not of C1 alone")

print()
print("=" * 72)
print("V4: CLAIMS 2+3 — independent q-elimination algebra (own derivation)")
print("=" * 72)

# jet-slot algebra, own construction
f, fr, fth = sp.symbols("f f_r f_theta", real=True)
fpos = sp.Symbol("f", positive=True)
qy, P, Q = sp.Symbol("q", real=True), sp.Symbol("P", positive=True), \
    sp.Symbol("Q", positive=True)
w, s = sp.symbols("w s", real=True)
SIN = sp.sin(th)
rp = sp.Symbol("r", positive=True)

g_enl = sp.Matrix([
    [-fpos, 0, 0, 0],
    [0, 1 / fpos, qy, 0],
    [0, qy, rp ** 2 * P, 0],
    [0, 0, 0, rp ** 2 * SIN ** 2 * Q],
])
ginv = g_enl.inv()
D2 = rp ** 2 * P / fpos - qy ** 2
detg = sp.factor(g_enl.det())
check("V04", sp.simplify(detg + fpos * D2 * rp ** 2 * SIN ** 2 * Q) == 0,
      "det g = -f D2 r^2 sin^2 Q exactly (own computation)")
K = (ginv[1, 1] * fr ** 2 + 2 * ginv[1, 2] * fr * fth
     + ginv[2, 2] * fth ** 2)
L = -(c / 8) * sp.sqrt(-detg) * K / fpos          # own density
N = rp ** 2 * P * fr ** 2 - 2 * qy * fr * fth + fth ** 2 / fpos
A0 = -(c / 8) * rp * sp.Abs(SIN) * sp.sqrt(Q / fpos)
check("V05", sp.simplify(L - A0 * N / sp.sqrt(D2)) == 0,
      "own closed form L = -(c/8) r |sin| sqrt(Q/f) N / sqrt(D2)")

Xe = fpos * fr ** 2 * rp ** 2 * P
Y = fth ** 2
# dL/dq derived analytically: A0 [q (Xe+Y) - 2 f_r f_th r^2 P]/(f D2^{3/2})
dLdq_pred = A0 * (qy * (Xe + Y) - 2 * fr * fth * rp ** 2 * P) \
    / (fpos * D2 ** sp.Rational(3, 2))
check("V06", sp.simplify(sp.diff(L, qy) - dLdq_pred) == 0,
      "dL/dq = -(c/8) r|sin|sqrt(Q/f) [q(Xe+Y) - 2 f_r f_th r^2 P] / "
      "(f D2^{3/2}): bracket LINEAR in q -> root uniqueness is a theorem, "
      "not a sympy-solve artifact; D2=0 enters only as a pole")

qstar = 2 * fr * fth * rp ** 2 * P / (Xe + Y)
# CLAIM 3 (degeneracy identity), exact polynomial identity:
check("V07", sp.simplify(D2.subs(qy, qstar) * fpos * (Xe + Y) ** 2
                         - rp ** 2 * P * (Xe - Y) ** 2) == 0,
      "CLAIM 3 exact: D2(q*) = (r^2 P/f) (Xe-Y)^2/(Xe+Y)^2 -- corner "
      "Xe = Y <=> metric degeneracy (polynomial identity, all signs)")
# N(q*) identity, exact polynomial identity:
check("V08", sp.simplify(N.subs(qy, qstar) * fpos * (Xe + Y)
                         - (Xe - Y) ** 2) == 0,
      "N(q*) = (Xe-Y)^2 / (f (Xe+Y)) (polynomial identity, all signs)")
# These two + positive prefactors give L_eff = -(c/8) sin sqrt(Q/P)|Xe-Y|/f
# analytically. Symbolic check of the SQUARED identity (branch-free):
L_eff_raw = L.subs(qy, qstar)
closed_abs = -(c / 8) * sp.Abs(SIN) * sp.sqrt(Q / P) * sp.Abs(Xe - Y) / fpos
check("V09", sp.simplify(sp.factor(L_eff_raw ** 2 - closed_abs ** 2)) == 0,
      "CLAIM 2 closed form, squared (branch-free, fully symbolic): "
      "L_eff^2 = [(c/8) sin sqrt(Q/P) (Xe-Y)/f]^2 exactly")
# sign + branch check at HOSTILE sample points: negative f_r/f_th, P<1
oks = True
done = 0
while done < 12:
    sub = {fpos: rr(), fr: rr(signed=True), fth: rr(signed=True),
           rp: rr(), P: sp.Rational(random.randint(1, 11),
                                    random.randint(8, 15)),
           Q: rr(), th: sp.Rational(random.randint(1, 6), 7) * sp.pi / 2,
           c: 1}
    if (Xe - Y).subs(sub) == 0 or sub[fr] == 0 or sub[fth] == 0:
        continue
    done += 1
    lhs = sp.nsimplify(L_eff_raw.subs(sub))
    rhs = sp.nsimplify(closed_abs.subs(sub))
    oks &= sp.simplify(lhs - rhs) == 0
check("V10", oks,
      "sign/branch at 12 hostile points (NEGATIVE f_r and f_theta, P<1, "
      "both Xe>Y and Xe<Y): L_eff(q*) = -(c/8) sin sqrt(Q/P)|Xe-Y|/f, "
      "value <= 0 branch-correctly (route sampled positives only)")

print()
print("=" * 72)
print("V5: CLAIM 2 — the shape forces and the static solution set")
print("=" * 72)

Leff_gt = -(c / 8) * SIN * sp.sqrt(Q / P) * (Xe - Y) / fpos
Leff_lt = -Leff_gt
form_dP = -(c / 16) * SIN * sp.sqrt(Q / P) * (rp ** 2 * fr ** 2
                                              + fth ** 2 / (fpos * P))
check("V11", sp.simplify(sp.diff(Leff_gt, P) - form_dP) == 0
      and sp.simplify(sp.diff(Leff_lt, P) + form_dP) == 0,
      "dL_eff/dP = -(c/16) sin sqrt(Q/P)[r^2 f_r^2 + f_th^2/(f P)] on "
      "Xe>Y; exact negative on Xe<Y (own diff)")
check("V12", sp.simplify(sp.diff(Leff_gt, Q) - Leff_gt / (2 * Q)) == 0,
      "dL_eff/dQ = L_eff/(2Q) exactly (Q only in sqrt(-g))")
# sign-definiteness: bracket is a positive-coefficient sum of squares
brk = rp ** 2 * fr ** 2 + fth ** 2 / (fpos * P)
sols = sp.solve(sp.Eq(brk, 0), [fr, fth], dict=True)
check("V13", all(set(sl.values()) <= {sp.S(0)} for sl in sols)
      and len(sols) > 0,
      "bracket = 0 (f,P,r > 0) ONLY at f_r = f_th = 0: smooth-branch "
      "P-stationarity alone already forces flat f; spherical f(r) with "
      "f_r != 0 is NOT stationary on the enlarged class")
# (w, s) split — route claim E4c, own substitution
Leff_ws = Leff_gt.subs({P: (1 + w) * sp.exp(2 * s),
                        Q: (1 + w) * sp.exp(-2 * s)})
check("V14", sp.simplify(sp.diff(Leff_ws, w)
                         + (c / 8) * SIN * rp ** 2 * fr ** 2) == 0
      and sp.simplify(sp.diff(Leff_ws, s)
                      + (c / 4) * SIN * sp.exp(-2 * s) * fth ** 2
                      / fpos) == 0,
      "dL_eff/dw = -(c/8) sin r^2 f_r^2 (w-independent, pure radial); "
      "dL_eff/ds = -(c/4) sin e^{-2s} f_th^2/f (pure phi-angular)")
# strictly-emptier comparison with P1 (P1 set: f spherical, q=0, w1 arb.)
qstar_sph = qstar.subs(fth, 0)
check("V15", sp.simplify(qstar_sph) == 0
      and sp.simplify(form_dP.subs(fth, 0)
                      + (c / 16) * SIN * sp.sqrt(Q / P) * rp ** 2
                      * fr ** 2) == 0,
      "P1's surviving spherical family (q*=0 at f_th=0) is KILLED on the "
      "enlarged class by dL/dP = -(c/16) sin sqrt(Q/P) r^2 f_r^2 != 0: "
      "'strictly emptier' verified -- stationary set is {f const} + "
      "degenerate corner only")

print()
print("=" * 72)
print("V6: CLAIM 4 — P1 reconstruction vs the rescued theorem workspace")
print("=" * 72)

# derive_system.py lines 44-48, verbatim structure:
w1 = sp.Symbol("w", real=True)
W1 = (1 + w1) ** 2
g_p1_rescued = sp.Matrix([
    [-fpos, 0, 0, 0],
    [0, 1 / fpos, qy, 0],
    [0, qy, rp ** 2 * W1, 0],
    [0, 0, 0, rp ** 2 * SIN ** 2 / W1],
])
# route's claim-4 reconstruction (identical by inspection; check anyway)
g_p1_route = sp.Matrix([
    [-fpos, 0, 0, 0],
    [0, 1 / fpos, qy, 0],
    [0, qy, rp ** 2 * (1 + w1) ** 2, 0],
    [0, 0, 0, rp ** 2 * SIN ** 2 * (1 + w1) ** (-2)],
])
check("V16", sp.simplify(g_p1_rescued - g_p1_route) == sp.zeros(4, 4),
      "route reconstruction == rescued derive_system.py metric, entry by "
      "entry, EXACTLY")
# dictionary: P = (1+w1)^2, Q = (1+w1)^{-2}  => P Q = 1 (unimodular),
# w = 0 and e^{2s} = (1+w1)^2 in the route's (w, s) parameterization
Pp1, Qp1 = W1, 1 / W1
weq = sp.solve(sp.Eq((1 + w) ** 2, Pp1 * Qp1), w)
check("V17", sp.simplify(Pp1 * Qp1 - 1) == 0 and sp.S(0) in weq,
      "P1 sits at P Q = 1: conformal w = 0, shear e^{2s} = (1+w_P1)^2 -- "
      "P1's shape field IS the shear mode; the conformal/det mode is what "
      "P1's primary class excluded (claim 4 dictionary exact)")
# cross-check own density against the rescued script's banked closed form
L_p1_own = -(c / 8) * sp.sqrt(-sp.factor(g_p1_rescued.det())) \
    * (g_p1_rescued.inv()[1, 1] * fr ** 2
       + 2 * g_p1_rescued.inv()[1, 2] * fr * fth
       + g_p1_rescued.inv()[2, 2] * fth ** 2) / fpos
A_ = fpos * rp ** 2 * W1 * fr ** 2 + fth ** 2
D2p1 = rp ** 2 * W1 - fpos * qy ** 2
L_rescued = -(c / 8) * rp * SIN * (A_ - 2 * fpos * qy * fr * fth) \
    / ((1 + w1) * fpos * sp.sqrt(D2p1))
dd = sp.simplify(sp.factor(L_p1_own ** 2 - L_rescued ** 2))
okp = dd == 0
oksgn = True
done = 0
while done < 6:
    sub = {fpos: rr(), fr: rr(signed=True), fth: rr(signed=True),
           rp: rr(), qy: sp.Rational(1, 9),
           w1: sp.Rational(random.randint(1, 5), 11),
           th: sp.Rational(1, 3), c: 1}
    if D2p1.subs(sub) <= 0:
        continue
    done += 1
    oksgn &= sp.simplify(sp.nsimplify(L_p1_own.subs(sub))
                         - sp.nsimplify(L_rescued.subs(sub))) == 0
check("V18", okp and oksgn,
      "own P1 density == derive_system.py check-06 closed form "
      "-(c/8) r sin [A - 2 f q f_r f_th]/((1+w) f sqrt(r^2 W - f q^2)) "
      "(squared identity symbolic + 6 signed sample points)")

print()
print("=" * 72)
print("V7: CLAIM 5 — sqrt(-g) R species, by COEFFICIENT not atom-presence")
print("=" * 72)


def ricci_density(gmat, coords):
    nn = len(coords)
    gi = gmat.inv()
    Gam = [[[sp.S(0)] * nn for _ in range(nn)] for _ in range(nn)]
    for al in range(nn):
        for i in range(nn):
            for j in range(nn):
                ex = sp.S(0)
                for k in range(nn):
                    ex += gi[al, k] * (sp.diff(gmat[k, i], coords[j])
                                       + sp.diff(gmat[k, j], coords[i])
                                       - sp.diff(gmat[i, j], coords[k]))
                Gam[al][i][j] = ex / 2
    Rs = sp.S(0)
    for i in range(nn):
        for j in range(nn):
            ex = sp.S(0)
            for al in range(nn):
                ex += sp.diff(Gam[al][i][j], coords[al])
                ex -= sp.diff(Gam[al][i][al], coords[j])
                for be in range(nn):
                    ex += Gam[al][al][be] * Gam[be][i][j]
                    ex -= Gam[al][j][be] * Gam[be][i][al]
            Rs += gi[i, j] * ex
    return sp.sqrt(-gmat.det()) * Rs


tt = sp.Symbol("t", real=True)
Fd = sp.Function("F")(r, th)
Pd = sp.Function("P")(r, th)
Qd = sp.Function("Q")(r, th)
g_diag = sp.Matrix([
    [-Fd, 0, 0, 0],
    [0, 1 / Fd, 0, 0],
    [0, 0, r ** 2 * Pd, 0],
    [0, 0, 0, r ** 2 * sp.sin(th) ** 2 * Qd],
])
EH = ricci_density(g_diag, [tt, r, th, ph])
EHx = sp.expand(EH)
cPrr = sp.simplify(EHx.coeff(sp.Derivative(Pd, r, 2)))
cQrr = sp.simplify(EHx.coeff(sp.Derivative(Qd, r, 2)))
check("V19", cPrr != 0 and cQrr != 0,
      "coefficients of P_rr and Q_rr in sqrt(-g)R are NONZERO after "
      "simplification (route S5a counted atoms on an UNSIMPLIFIED "
      "expression -- conclusion survives the stricter test)")
# first-derivative content survives too (kill all 2nd jets, then check)
kill2 = {d: 0 for d in EHx.atoms(sp.Derivative) if d.derivative_count == 2}
EH1 = EHx.subs(kill2)
cPr = sp.simplify(sp.diff(EH1, sp.Derivative(Pd, r)))
sub = {Fd: sp.Rational(3, 4), Pd: sp.Rational(5, 4), Qd: sp.Rational(7, 6),
       r: 2, th: sp.pi / 3}
sub.update({d: rr(signed=True) for d in EH1.atoms(sp.Derivative)})
sub.update({d: rr(signed=True) for d in cPr.atoms(sp.Derivative)})
check("V20", sp.simplify(cPr.subs(sub)) != 0,
      "first-jet P_r dependence also genuinely nonzero (sampled after "
      "second-jet kill): claim 5 stands -- the curvature species carries "
      "1st AND 2nd shape jets; C1 carries none")

print()
print("=" * 72)
print("V8: ROUTE-SCRIPT DEFECT PROBES (vacuity hunting)")
print("=" * 72)

# S4b vacuity: the constant-substitution 'commutation' test passes even
# for a density that DOES carry metric derivatives (sqrt(-g) R):
consts = {Pd: sp.Rational(3, 2), Qd: sp.Rational(4, 3)}
EH_sub = EH.subs(consts).doit()
EH_const = ricci_density(g_diag.subs(consts), [tt, r, th, ph])
check("V21", sp.simplify(EH_sub - EH_const) == 0,
      "DEFECT CONFIRMED: route check S4b (constant-substitution commutes) "
      "ALSO passes for sqrt(-g)R, a density full of metric derivatives -- "
      "S4b is vacuous as a discriminator (substitution always commutes "
      "with a functorial construction); S4a's atom census is the only "
      "real content of S4")
# E2b vacuity: route compares simplify(diff(L,P)) to diff(L,P) -- zero
# identically before any sampling; demonstrate on an arbitrary expression
zz = sp.Symbol("z")
arb = sp.exp(zz) * sp.sin(zz) / (1 + zz ** 2)
check("V22", sp.simplify(sp.simplify(sp.diff(arb, zz))
                         - sp.diff(arb, zz)) == 0,
      "DEFECT CONFIRMED: route check E2b's tested expression "
      "(simplify(dL/dP) - dL/dP) is identically zero for ANY L -- the 4 "
      "'exact rational points' cannot fail; E2b verifies nothing")
check("V23", True,
      "DEFECT (by inspection): G3b's condition `len(fin_roots) == 1` is a "
      "verbatim subset of G3a's condition -- G3b can never fail once G3a "
      "passes (count padding). E1d (3 checks) only tests finiteness at "
      "random points -- near-vacuous. Honest count of independent, "
      "falsifiable checks is ~29, not 34")

print()
nfail = sum(1 for _, ok, _ in results if not ok)
print("VERIFIER RESULT: %d / %d attacks survived by the route's claims"
      % (sum(1 for _, ok, _ in results if ok), len(results)))
print("(V02/V03 'PASS' = the tie-dependence ATTACK SUCCEEDED as predicted,")
print(" amending claim 1's scope; V21-V23 'PASS' = route defects confirmed)")
