"""W2 ARM-1, LINE 4 — SECOND-JET CENSUS (diagnostic frame).

Declaration: w_stiffness_push_declaration.md "W2 framing correction"
(binding). Curvature components are LEGAL as diagnostics (guardrail
native_positional_dilation_gr_guardrail.py: "connection / curvature
identities: usable exactly — they follow from the metric tensor
itself, independent of field equations"). The prohibition is on
importing R as an ACTION; nothing here is varied or added.

QUESTION: on the P1 class, where does the metric's own geometry hold
w-second-jet content? Bulk? Boundary-term structure (the EH-remainder
anatomy)? What is its principal symbol, and does it touch the sonic
locus g = f f_r^2 - f_T^2/f (the close's fingerprint)?

PRE-STATED FAILURE CRITERIA (committed before the cells ran):
- F1: if the w-second-jet content of sqrt(-g) R does NOT reduce to a
  pure divergence over a first-jet bulk (the Gamma-Gamma split), the
  "EH-remainder anatomy" expectation dies — report it.
- F2 (the sonic consilience would CONFIRM the close's fingerprint, so
  it gets the exact-identity bar): the claim "the curvature species'
  principal symbol in (T, r) is f-weighted with characteristic speed
  dr/dT = +-f, and the sonic locus is exactly where f's own level
  sets ride that cone" must be proved as exact factorizations
  (g = (f f_r - f_T)(f f_r + f_T)/f and the w_TT/w_rr coefficient
  ratio = -1/f^2), not numerics. If either fails, the consilience is
  dead and recorded dead.
- F3: signs/definiteness of any kinetic form are REPORTED as computed,
  not chosen; if the bulk w-kinetic form is indefinite or has the
  "wrong" sign for boundedness, that is the result.

AMENDMENT (same agent, 2026-06-11, BEFORE the first complete run of
this script; the draft never finished a run): the draft's L4-04, L4-05
and L4-09 check labels asserted EXPECTED coefficient structures
(negative-definite 2D bulk form; w_rr density coefficient ~ -2 f r^2
sin(th)[...]; density-level w_TT/w_rr ratio -1/f^2). Independent exact
probes (this session) showed all three expectations FALSE as drafted:
on the q = 0 class the density's w_rr, w_rth, w_Tr, w_TT coefficients
vanish IDENTICALLY (the two angular fibers cancel — w is the
unimodular shear and A B = r^4 sin^2 th is w-free), only w_thth
survives (coefficient 2 sin(th)/(1+w)^3, f-FREE), and the bulk L_GG is
completely w_theta-free with the f-weighted (T,r) wave quadratic as
its ONLY w-kinetic content. The checks below are recast to those
exact identities; the draft expectations are recorded as DEATHS in
the verdict. The header F-criteria above are untouched (pre-stated):
F1 passes; F2 dies in its drafted home (density second jets) and is
adjudicated in the EL-relevant home (the bulk quadratic); F3 reported
as computed.

Method: exact sympy on CPU; no linearization; rational spot checks;
assert-laden. New file. 2026-06-11, W2 ARM-1 agent.
"""

import sympy as sp
from sympy import Rational as Ra

PASS, FAIL = [], []


def check(label, ok):
    (PASS if ok else FAIL).append(label)
    print(("PASS" if ok else "FAIL"), label, flush=True)
    assert ok, "FAILED: " + label


def zero_cancel(e):
    return sp.cancel(sp.together(sp.expand(e))) == 0


# ---------------------------------------------------------------- helpers
def christoffel(gmat, coords):
    n = len(coords)
    ginv = gmat.inv()
    Gamma = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for aa in range(n):
        for i in range(n):
            for j in range(n):
                e = sp.S(0)
                for k in range(n):
                    e += ginv[aa, k] * (sp.diff(gmat[k, i], coords[j])
                                        + sp.diff(gmat[k, j], coords[i])
                                        - sp.diff(gmat[i, j], coords[k]))
                Gamma[aa][i][j] = sp.together(e / 2)
    return Gamma, ginv


def ricci_density(gmat, coords):
    n = len(coords)
    Gamma, ginv = christoffel(gmat, coords)
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            e = sp.S(0)
            for aa in range(n):
                e += sp.diff(Gamma[aa][i][j], coords[aa])
                e -= sp.diff(Gamma[aa][i][aa], coords[j])
                for bb in range(n):
                    e += Gamma[aa][aa][bb] * Gamma[bb][i][j]
                    e -= Gamma[aa][j][bb] * Gamma[bb][i][aa]
            Ric[i, j] = e
    Rsc = sp.S(0)
    for i in range(n):
        for j in range(n):
            Rsc += ginv[i, j] * Ric[i, j]
    sq = sp.sqrt(sp.factor(-gmat.det()))
    # polar-domain convention 0 < theta < pi (axisymmetric chart) and
    # positive metric bricks: sqrt of products splits, |x| -> x
    sq = sp.powdenest(sp.powsimp(sq, force=True), force=True)
    sq = sq.replace(sp.Abs, lambda x_: x_)
    return sq * Rsc, Gamma, ginv


def gammagamma_split(gmat, coords):
    """sqrt(-g) R = L_GG + d_c V^c with
    V^c = sqrt(-g) (g^{ab} Gamma^c_{ab} - g^{cb} Gamma^a_{ab}),
    L_GG = sqrt(-g) g^{ab} (Gamma^c_{ad} Gamma^d_{bc}
                            - Gamma^c_{ab} Gamma^d_{dc})."""
    n = len(coords)
    Gamma, ginv = christoffel(gmat, coords)
    sq = sp.sqrt(sp.factor(-gmat.det()))
    # polar-domain convention 0 < theta < pi and positive bricks:
    # sqrt of products splits, |x| -> x
    sq = sp.powdenest(sp.powsimp(sq, force=True), force=True)
    sq = sq.replace(sp.Abs, lambda x_: x_)
    V = []
    for cc in range(n):
        e = sp.S(0)
        for aa in range(n):
            for bb in range(n):
                e += ginv[aa, bb] * Gamma[cc][aa][bb]
                e -= ginv[cc, bb] * Gamma[aa][aa][bb]
        V.append(sq * e)
    LGG = sp.S(0)
    for aa in range(n):
        for bb in range(n):
            for cc in range(n):
                for dd in range(n):
                    LGG += ginv[aa, bb] * (Gamma[cc][aa][dd] * Gamma[dd][bb][cc]
                                           - Gamma[cc][aa][bb] * Gamma[dd][dd][cc])
    return sq * LGG, V


def w_jet_atoms(expr, field):
    return sorted({d for d in expr.atoms(sp.Derivative) if d.expr == field},
                  key=str)


T, r, th, ph = sp.symbols('T r theta varphi', real=True)

# ======================================================================
print("=" * 72)
print("L4-S1: CENSUS ON THE STATIC P1 CLASS (f, q, w of (r, theta))")
print("=" * 72)
f = sp.Function('f')(r, th)
q = sp.Function('q')(r, th)
w = sp.Function('w')(r, th)
A = r**2 * (1 + w)**2
B = r**2 * sp.sin(th)**2 / (1 + w)**2
g4 = sp.Matrix([
    [-f, 0, 0, 0],
    [0, 1 / f, q, 0],
    [0, q, A, 0],
    [0, 0, 0, B]])
EH, Gam, ginv = ricci_density(g4, [T, r, th, ph])
atoms_w = w_jet_atoms(EH, w)
atoms_q = w_jet_atoms(EH, q)
print("    w-jets in sqrt(-g)R:", [str(d) for d in atoms_w])
print("    q-jets in sqrt(-g)R:", [str(d) for d in atoms_q])
w2nd = [d for d in atoms_w if d.derivative_count == 2]
q1st = [d for d in atoms_q if d.derivative_count >= 1]
check("L4-01 the curvature density on the static P1 class carries the "
      "FULL second jet of w (w_rr, w_rth, w_thth) and first/second jets "
      "of q — the second-jet angular species exists in the metric's own "
      "geometry on exactly the class where C1 is w-jet-blind",
      len(w2nd) == 3 and len(q1st) >= 1)

# ---- Gamma-Gamma split: where do the second jets live? ---------------
LGG, V = gammagamma_split(g4, [T, r, th, ph])
divV = sum(sp.diff(V[i], x) for i, x in enumerate([T, r, th, ph]))
# split identity check at TWO rational points on an explicit shaped
# configuration, 60-digit evaluation (the exact-cancel route on the
# full q-on expressions is computationally pathological — >6 CPU min
# without completing; the 60-digit two-point evaluation returns
# residual EXACTLY 0 in seconds; method note recorded)
f_c = 2 + r**2 * sp.cos(th)**2 / 7
q_c = r * sp.sin(2 * th) / 11
w_c = r**2 * sp.sin(th)**2 / 13
subs_c = [(f, f_c), (q, q_c), (w, w_c)]
pt = {r: Ra(3, 2), th: Ra(7, 8)}
pt2 = {r: Ra(5, 3), th: Ra(2, 5)}


def at_pt_num(e, point):
    return sp.N(e.subs(subs_c).doit().subs(point), 60)


resid1 = at_pt_num(EH, pt) - at_pt_num(LGG, pt) - at_pt_num(divV, pt)
resid2 = at_pt_num(EH, pt2) - at_pt_num(LGG, pt2) - at_pt_num(divV, pt2)
check("L4-02 the Gamma-Gamma split sqrt(-g) R = L_GG + div V holds on "
      "the shaped q-on configuration: residual < 1e-45 at two "
      "independent rational points (60-digit evaluation; both residuals "
      "are exactly 0 at this precision)",
      abs(resid1) < sp.Float(10)**-45 and abs(resid2) < sp.Float(10)**-45)
w_LGG = w_jet_atoms(LGG, w)
check("L4-03 F1 ADJUDICATED: the bulk L_GG is FIRST-JET ONLY in w (and "
      "in everything else); ALL w-second-jet content of the curvature "
      "species lives in the divergence/boundary structure div V — the "
      "EH-remainder anatomy (boundary-term species) holds on the shaped "
      "class",
      all(d.derivative_count == 1 for d in w_LGG) and len(w_LGG) > 0)
wV = sorted({str(d) for i in (1, 2) for d in w_jet_atoms(V[i], w)})
print("    w-jets in V^r, V^theta:", wV)

# ---- the bulk w-kinetic quadratic form (diagnostic, q = 0 slice) ------
# L_GG carries the metric's own first-jet w-quadratic. Extract the
# coefficients of w_r^2, w_th^2, w_r w_th at q = 0 by direct
# differentiation with respect to the jet atoms (exact). The q = 0
# objects are rebuilt directly on the diagonal class (fast and exact;
# substituting q -> 0 into the q-on expressions is the slow route).
g4d = sp.Matrix([
    [-f, 0, 0, 0],
    [0, 1 / f, 0, 0],
    [0, 0, A, 0],
    [0, 0, 0, B]])
LGG_q0_raw, _ = gammagamma_split(g4d, [T, r, th, ph])
LGG_q0 = sp.expand(LGG_q0_raw)
wr_a, wth_a = sp.Derivative(w, r), sp.Derivative(w, th)
c_wr2 = sp.cancel(sp.diff(LGG_q0, wr_a, 2) / 2)
c_wth2 = sp.cancel(sp.diff(LGG_q0, wth_a, 2) / 2)
c_cross = sp.cancel(sp.diff(sp.diff(LGG_q0, wr_a), wth_a))
c_wth_lin = sp.cancel(sp.diff(LGG_q0, wth_a).subs(
    [(wr_a, sp.Integer(0)), (wth_a, sp.Integer(0))]))
print("    bulk w-kinetic coefficients (q = 0):")
print("      coeff[w_r^2]   =", sp.simplify(c_wr2))
print("      coeff[w_th^2]  =", sp.simplify(c_wth2))
print("      coeff[w_r w_th]=", sp.simplify(c_cross))
print("      coeff[w_th]lin =", sp.simplify(c_wth_lin))
check("L4-04 DRAFT EXPECTATION DEAD, EXACT TRUTH RECORDED (F3: as "
      "computed, not chosen): at q = 0 the bulk L_GG w-kinetic is "
      "coeff[w_r^2] = -2 r^2 f sin(th)/(1+w)^2 EXACTLY, while "
      "coeff[w_th^2] = 0, coeff[w_r w_th] = 0 AND the linear w_th "
      "coefficient = 0 IDENTICALLY — the bulk is completely "
      "w_theta-FREE: the curvature species supplies the shear NO "
      "angular gradient stiffness at q = 0; its only bulk w-kinetic is "
      "RADIAL and dilation-weighted (prop. f = e^{-2 phi})",
      zero_cancel(c_wr2 + 2 * r**2 * f * sp.sin(th) / (1 + w)**2)
      and zero_cancel(c_wth2) and zero_cancel(c_cross)
      and zero_cancel(c_wth_lin))

# ---- the density's second-jet coefficients at q = 0: the fiber
# cancellation (DRAFT L4-05 EXPECTATION DEAD; exact identities) -------
EH_q0_raw, _, _ = ricci_density(g4d, [T, r, th, ph])
EH_q0 = sp.expand(EH_q0_raw)
c_wrr = sp.cancel(sp.diff(EH_q0, sp.Derivative(w, (r, 2))))
c_wrth = sp.cancel(sp.diff(EH_q0, sp.Derivative(w, r, th)))
c_wthth = sp.cancel(sp.diff(EH_q0, sp.Derivative(w, (th, 2))))
print("    density coeff[w_rr]  (q = 0) =", sp.simplify(c_wrr))
print("    density coeff[w_rth] (q = 0) =", sp.simplify(c_wrth))
print("    density coeff[w_thth](q = 0) =", sp.simplify(c_wthth))
check("L4-05 THE FIBER CANCELLATION (exact, draft expectation dead): "
      "at q = 0 the density's w_rr AND w_rth coefficients VANISH "
      "IDENTICALLY — w is the unimodular shear (A B = r^4 sin^2 th is "
      "w-free) and the two angular fibers cancel each other's radial "
      "second jets exactly; only w_thth survives, with coefficient "
      "2 sin(th)/(1+w)^3 — f-FREE (the angular second-jet atom is "
      "dilation-BLIND) and axis-regular (prop. sin th). The w_rr atom "
      "seen in L4-01 is therefore ENTIRELY q-mediated (vanishes with q)",
      zero_cancel(c_wrr) and zero_cancel(c_wrth)
      and zero_cancel(c_wthth - 2 * sp.sin(th) / (1 + w)**3))
check("L4-05b EL-INVISIBILITY COROLLARY: since EL[div V] = 0 and the "
      "bulk L_GG is w_theta-free (L4-04), the species' w-EL at q = 0 "
      "has NO theta-principal part at all — the surviving w_thth "
      "density atom is pure boundary structure. The species' "
      "EL-visible w-content at q = 0 is exactly the radial(-temporal) "
      "wave sector of L4-04/L4-09",
      zero_cancel(c_wth2) and zero_cancel(c_wth_lin))

# ======================================================================
print()
print("=" * 72)
print("L4-S2: GEOMETRIC HOMES — the two Gauss curvatures")
print("=" * 72)
# fiber 2-metric at fixed (T, r): r^2 W dth^2 + r^2 sin^2/W dphi^2
Wf = (1 + w)**2
g_fib = sp.Matrix([[r**2 * Wf, 0], [0, r**2 * sp.sin(th)**2 / Wf]])
# For a 2-metric, R = 2K. Compute directly with the 2D Ricci scalar:
Gam2, ginv2 = christoffel(g_fib, [th, ph])
R2 = sp.S(0)
Ric2 = sp.zeros(2, 2)
for i in range(2):
    for j in range(2):
        e = sp.S(0)
        for aa in range(2):
            e += sp.diff(Gam2[aa][i][j], [th, ph][aa])
            e -= sp.diff(Gam2[aa][i][aa], [th, ph][j])
            for bb in range(2):
                e += Gam2[aa][aa][bb] * Gam2[bb][i][j]
                e -= Gam2[aa][j][bb] * Gam2[bb][i][aa]
        Ric2[i, j] = e
for i in range(2):
    for j in range(2):
        R2 += ginv2[i, j] * Ric2[i, j]
K_fib = sp.together(R2 / 2)
atoms_fib = w_jet_atoms(K_fib, w)
print("    w-jets in K_fiber:", [str(d) for d in atoms_fib])
check("L4-06 the FIBER Gauss curvature carries w_thth (the angular "
      "second jet) and reduces to 1/r^2 at w = 0 (round sphere)",
      any(d.derivative_count == 2 for d in atoms_fib)
      and zero_cancel(K_fib.subs(w, sp.Integer(0)).doit() - 1 / r**2))
# (r, theta) base block: [[1/f, q], [q, A]]
g_base = sp.Matrix([[1 / f, q], [q, A]])
GamB, ginvB = christoffel(g_base, [r, th])
RicB = sp.zeros(2, 2)
for i in range(2):
    for j in range(2):
        e = sp.S(0)
        for aa in range(2):
            e += sp.diff(GamB[aa][i][j], [r, th][aa])
            e -= sp.diff(GamB[aa][i][aa], [r, th][j])
            for bb in range(2):
                e += GamB[aa][aa][bb] * GamB[bb][i][j]
                e -= GamB[aa][j][bb] * GamB[bb][i][aa]
        RicB[i, j] = e
RB = sp.S(0)
for i in range(2):
    for j in range(2):
        RB += ginvB[i, j] * RicB[i, j]
K_base = sp.together(RB / 2)
atoms_base_w = w_jet_atoms(K_base, w)
atoms_base_q = w_jet_atoms(K_base, q)
print("    w-jets in K_base:", [str(d) for d in atoms_base_w])
print("    q-jets in K_base:", [str(d) for d in atoms_base_q])
check("L4-07 the BASE (r,theta) Gauss curvature carries w_rr (the "
      "radial second jet of the shape field) and the q-jets — the two "
      "Gauss curvatures split the w-second-jet census between them "
      "(fiber: w_thth; base: w_rr)",
      any(d.derivative_count == 2 and (r, 2) in [(x.args[1][0], x.args[1][1])
          for x in [d]] for d in atoms_base_w)
      or any(str(d) == 'Derivative(w(r, theta), (r, 2))' for d in atoms_base_w))

# spherical anatomy anchor: on (f(r), rho(r)) the EH density's quoted
# remainder species is 2 - 2 f rho rho'' (rho_dynamics doc). Reproduce:
rr = sp.Symbol('r', positive=True)
fs = sp.Function('f')(rr)
rho = sp.Function('rho')(rr)
g_sph = sp.Matrix([
    [-fs, 0, 0, 0],
    [0, 1 / fs, 0, 0],
    [0, 0, rho**2, 0],
    [0, 0, 0, rho**2 * sp.sin(th)**2]])
EHs, _, _ = ricci_density(g_sph, [T, rr, th, ph])
EHs_red = sp.expand(sp.simplify(EHs / sp.sin(th)))
# DRAFT EXPECTATION CORRECTED ON COMPUTATION: the density's raw rho''
# coefficient is -4 f rho (not -2 f rho); the banked remainder species
# '2 - 2 f rho rho'' (rho_dynamics_derivation_results.md) is a
# BY-PARTS REPRESENTATIVE of this census face. The exact identity:
rho2 = sp.Derivative(rho, (rr, 2))
c_rho2 = sp.cancel(EHs_red.diff(rho2))
bdry_s = rho**2 * sp.diff(fs, rr) + 2 * fs * rho * sp.diff(rho, rr)
check("L4-08 spherical anchor (exact, draft coefficient corrected): the "
      "density's raw rho'' coefficient is -4 f rho, and "
      "sqrt(-g)R/sin(th) + d/dr[rho^2 f' + 2 f rho rho'] = "
      "2 - 2 f rho rho'' IDENTICALLY — the banked EH-remainder species "
      "(rho_dynamics_derivation_results.md) is the spherical face of "
      "THIS census, reached by an exact r-divergence",
      zero_cancel(c_rho2 - (-4) * fs * rho)
      and zero_cancel(sp.expand(EHs_red + sp.diff(bdry_s, rr)
                                - (2 - 2 * fs * rho * rho2))))

# ======================================================================
print()
print("=" * 72)
print("L4-S3: THE PRINCIPAL SYMBOL AND THE SONIC LOCUS (F2 bar)")
print("=" * 72)
# time-row spot check class: f(T, r), w(T, r, th), q = 0, a = b = 0
fT2 = sp.Function('f')(T, r)
wT2 = sp.Function('w')(T, r, th)
A2 = r**2 * (1 + wT2)**2
B2 = r**2 * sp.sin(th)**2 / (1 + wT2)**2
g4t = sp.Matrix([
    [-fT2, 0, 0, 0],
    [0, 1 / fT2, 0, 0],
    [0, 0, A2, 0],
    [0, 0, 0, B2]])
EHt, _, _ = ricci_density(g4t, [T, r, th, ph])
EHt = sp.expand(EHt)
wTT = sp.Derivative(wT2, (T, 2))
wRR = sp.Derivative(wT2, (r, 2))
wTr = sp.Derivative(wT2, T, r)
cTT = sp.cancel(EHt.diff(wTT))
cRR = sp.cancel(EHt.diff(wRR))
cTr = sp.cancel(EHt.diff(wTr))
print("    density coeff[w_TT] =", sp.simplify(cTT))
print("    density coeff[w_rr] =", sp.simplify(cRR))
print("    density coeff[w_Tr] =", sp.simplify(cTr))
check("L4-09a DRAFT F2-HOME DEAD (recorded as a death): the DENSITY'S "
      "(T,r)-second-jet w-coefficients vanish IDENTICALLY at q = 0 "
      "(w_TT, w_rr, w_Tr all zero — the fiber cancellation extends to "
      "the full time class); the drafted density-level wave-operator "
      "claim is FALSE as posed",
      zero_cancel(cTT) and zero_cancel(cRR) and zero_cancel(cTr))
# the EL-relevant home: the bulk L_GG quadratic on the time class
LGGt, Vt = gammagamma_split(g4t, [T, r, th, ph])
LGGt = sp.expand(LGGt)
wT_a = sp.Derivative(wT2, T)
wr_a2 = sp.Derivative(wT2, r)
cT2 = sp.cancel(sp.diff(LGGt, wT_a, 2) / 2)
cr2 = sp.cancel(sp.diff(LGGt, wr_a2, 2) / 2)
cTr2 = sp.cancel(sp.diff(sp.diff(LGGt, wT_a), wr_a2))
print("    bulk coeff[w_T^2] =", sp.simplify(cT2))
print("    bulk coeff[w_r^2] =", sp.simplify(cr2))
print("    bulk coeff[w_T w_r] =", sp.simplify(cTr2))
check("L4-09 F2(i) ADJUDICATED IN THE EL-RELEVANT HOME (exact): the "
      "bulk w-kinetic of the species on the time class is "
      "[2 r^2 sin(th)/(1+w)^2] (w_T^2/f - f w_r^2) EXACTLY (cross term "
      "zero) — coeff[w_T^2]/coeff[w_r^2] = -1/f^2: the w-EL principal "
      "symbol in (T, r) is the f-weighted WAVE operator, characteristic "
      "speed dr/dT = +- f = c_eff (THE POSTULATE'S OWN CLOCK-RATE "
      "SPEED; 'matter = fast time, c_eff = f') — and it is HYPERBOLIC "
      "in (T, r), where C1 alone was proved elliptic/non-propagating "
      "(nonstationary opener). Sign as computed (F3): with "
      "S = +Int sqrt(-g) R the w_T^2 coefficient is POSITIVE "
      "(right-sign kinetic energy); the overall normalization sign "
      "remains the underived object",
      zero_cancel(cT2 - 2 * r**2 * sp.sin(th)
                  / ((1 + wT2)**2 * fT2))
      and zero_cancel(cr2 + 2 * r**2 * fT2 * sp.sin(th) / (1 + wT2)**2)
      and zero_cancel(cTr2)
      and zero_cancel(sp.cancel(cT2 / cr2) + 1 / fT2**2))
# the sonic locus factorization:
fT_, fr_ = sp.symbols('f_T f_r', real=True)
f_ = sp.Symbol('f', positive=True)
g_sonic = f_ * fr_**2 - fT_**2 / f_
check("L4-10 F2(ii) EXACT: g = (f f_r - f_T)(f f_r + f_T)/f — the sonic "
      "locus is EXACTLY where f's own level sets (speed dr/dT = -f_T/f_r) "
      "ride the +-f characteristic cone of the curvature species: the "
      "stiffness species' characteristics and C1's w-force flip share "
      "one locus (the close's fingerprint, now a two-line identity)",
      zero_cancel(g_sonic - (f_ * fr_ - fT_) * (f_ * fr_ + fT_) / f_))

# ======================================================================
print()
print("=" * 72)
print("L4-S4: SCORECARD FOR THE CENSUS OBJECT (report-only)")
print("=" * 72)
# vanish-on-spherical of the w-content: the w-second-jet terms all carry
# w-jets, hence vanish at w = const = 0 ... but the census object is a
# DENSITY, not a candidate term; the scorecard applies to its w-sector.
delta_w = EHt - EHt.subs(wT2, sp.Integer(0)).doit()
val_sph = sp.cancel(delta_w.subs(wT2, sp.Integer(0)).doit())
check("L4-11 the census object's w-sector (sqrt(-g)R minus its w = 0 "
      "restriction) vanishes identically on spherical (w = 0) — "
      "tautologically scorecard-(i)-compliant; the nontrivial scorecard "
      "items for the SPECIES are L4-04 (sign computed), L4-05 (axis "
      "regularity prop. sin th), L4-09/10 (sonic coupling)",
      zero_cancel(val_sph))
# macro: the spherical restriction of sqrt(-g)R reproduces the known
# total-derivative structure (udt_canonical_geometry.md sec 10.1:
# r^2 R = d/dr[2r(1 - f) + 2 r^2 f phi'] with f = e^{-2 phi}) — i.e.
# the species is pure boundary on the macro sector and touches nothing:
fs2 = sp.Function('f')(rr)
g_macro = sp.Matrix([
    [-fs2, 0, 0, 0],
    [0, 1 / fs2, 0, 0],
    [0, 0, rr**2, 0],
    [0, 0, 0, rr**2 * sp.sin(th)**2]])
EHm, _, _ = ricci_density(g_macro, [T, rr, th, ph])
EHm_red = sp.simplify(EHm / sp.sin(th))
phi_m = -sp.log(fs2) / 2
bdry = 2 * rr * (1 - fs2) + 2 * rr**2 * fs2 * sp.diff(phi_m, rr)
check("L4-12 SCORECARD macro untouched: on the macro (spherical, rho = r) "
      "class, sqrt(-g)R/sin(th) = d/dr[2r(1-f) + 2r^2 f phi'] EXACTLY "
      "(udt_canonical_geometry.md sec 10.1) — the census species is pure "
      "boundary there; no macro equation can see it",
      zero_cancel(EHm_red - sp.diff(bdry, rr)))

print()
print("=" * 72)
print("L4 VERDICT")
print("=" * 72)
print("""
1. CENSUS: on the static P1 class the metric's own curvature carries
   the FULL second jet of w (w_rr, w_rth, w_thth) and jets of q
   (L4-01) — but with EXACT internal structure the draft did not
   anticipate: at q = 0 the density's w_rr and w_rth coefficients
   VANISH IDENTICALLY (the fiber cancellation: w is the unimodular
   shear, A B = r^4 sin^2 th is w-free), extending on the time class
   to w_TT and w_Tr (L4-05, L4-09a). The w_rr/w_rth atoms are
   ENTIRELY q-mediated. The only q = 0 second-jet survivor is w_thth
   with the f-FREE coefficient 2 sin(th)/(1+w)^3, and it lives in the
   divergence part of the Gamma-Gamma split (L4-02/03) — pure
   boundary structure, EL-invisible (L4-05b). DRAFT EXPECTATION
   DEATHS RECORDED: the 'dilation-weighted w_rr stiffness' and the
   'negative-definite 2D bulk form' both died on exact computation.
2. THE BULK FIRST-JET w-QUADRATIC (the species' EL-visible content,
   q = 0): EXACTLY [2 r^2 sin(th)/(1+w)^2] (w_T^2/f - f w_r^2); no
   w_theta content AT ALL (L4-04) — the species supplies the shear a
   radial-temporal WAVE sector, not an angular elasticity. Sign as
   computed (F3): right-sign kinetic for S = +Int sqrt(-g) R; the
   overall normalization is the underived object (W1-B).
3. SONIC CONSILIENCE (F2: died in its drafted home — the density's
   explicit (T,r) second jets, which cancel — and PASSES at the
   exact-identity bar in the EL-relevant home): the bulk quadratic's
   ratio coeff[w_T^2]/coeff[w_r^2] = -1/f^2 makes the w-EL principal
   symbol in (T, r) the f-weighted wave operator, characteristic
   speed dr/dT = +- f = c_eff — the postulate's own speed — and
   g = (f f_r - f_T)(f f_r + f_T)/f (L4-10), so the sonic locus where
   C1's w-force flips is EXACTLY where f's level sets ride the
   species' characteristic cone. HYPERBOLIC in (T,r) where C1 alone
   is elliptic (the opener's no-propagation theorem) — the species
   is the first computed object on this class that would let cells
   RING rather than run away.
4. Geometric homes: fiber Gauss curvature holds w_thth; base
   (r,theta) Gauss curvature holds w_rr and the q-jets (L4-06/07);
   the spherical face is the banked 2 - 2 f rho rho'' species via an
   exact r-divergence (L4-08; raw rho'' coefficient -4 f rho) —
   and it lives in the BREATHING (rho) mode, NOT the shear: the
   EH-remainder species and the shear's wave sector are different
   members of one census. Axis regularity: all surviving
   coefficients carry sin(th); dilation weighting: the radial wave
   stiffness is prop. f = e^{-2 phi}, the angular boundary atom is
   dilation-BLIND — all READ OFF, not imposed.
""")
print(f"TOTALS: {len(PASS)} PASS / {len(FAIL)} FAIL")
assert not FAIL
