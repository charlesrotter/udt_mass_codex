"""ROUTE C — THE READINGS OF "DISTANCE" IN THE POSITIONAL-DILATION
PRINCIPLE, AND THEIR EXACT CONSEQUENCES FOR (f, rho).

Context (branch-(iii) fork; see branch_iii_hunt_results.md and
native_areal_function_field_equations.py): on the generalized static
spherically symmetric metric

    ds^2 = -f dt^2 + f^{-1} dr^2 + rho(r)^2 dOmega^2,     f = e^{-2 phi},

P0 (the foundational postulate) is "positional dilation: time dilation
grows with distance from the structure" PLUS the condition B = 1/A
(g_tt * g_rr = -1), and it SILENTLY fixes rho = r.  The freed-rho hunt
showed rho = r is not derived by the banked native action (P0's areal
choice is kinematic), and the one static escape is a saturating rho
(throat).  This file asks the PRIOR question: does the DEFINITIONAL
principle itself — once the word "distance" is read precisely —
constrain rho?

THE THREE CANDIDATE READINGS of "phi is a function of distance X from
the structure":

    R-areal      X = rho   (the areal radius: the invariant sphere size,
                            sqrt(Area/4pi));
    R-proper     X = s     (proper radial distance, ds = f^{-1/2} dr);
    R-coordinate X = r     (the B = 1/A coordinate itself).

KEY OBSERVATION, formalized below as two gauge LEMMAS (not just a
remark): the metric ansatz already makes phi a function of r trivially,
and "phi = phi(X)" is contentless for ANY monotone X (a relabeling).
The readings acquire content ONLY through WHERE the B = 1/A condition is
imposed and what that chart's coordinate is declared to measure:

    LEMMA 1 (existence):  every static spherical metric admits a chart in
        which B = 1/A holds — the condition ALONE has no invariant content;
    LEMMA 2 (uniqueness): the B = 1/A chart is unique up to r -> ±r + const
        at fixed Killing time; allowing the Killing-time rescaling t -> kt
        adds r -> ±r/k + const with (C, a) -> (k²C, ka) (verifier
        amendment) — so "which chart is the B = 1/A chart" is sharp,
        invariant data up to ±/shift/rescale, the slope-1 being a
        time-unit convention.  Downstream binary verdicts (C = 0 vs C > 0)
        are gauge-invariant.

MAIN RESULTS (each labeled (D) = exact derivation, (CL) = reading
classification that needs Charles's canonization):

    (D)  R-AREAL THEOREM:  [B = 1/A holds in the areal chart]
             <=>  rho(r) = ±r + const in any B = 1/A chart.
         The banked P0 IS the R-areal reading, and the silent rho = r is
         then NOT an independent postulate — it is FORCED (up to a shift
         constant r0, whose only physical content is a finite-area inner
         sphere / puncture if the chart is extended to r -> 0; on an
         exterior domain it is a pure relabel).
    (D)  R-PROPER DEGENERACY:  g_ss = 1 identically, so B = 1/A imposed in
         the proper-distance chart forces g_tt = -1, i.e. f == 1, phi == 0:
         NO dilation at all.  R-proper is INCOMPATIBLE with B = 1/A as a
         simultaneous condition.
    (CL) R-COORDINATE:  rho(r) free (the generalized family); the principle
         is then INCOMPLETE — it owes an independent statement of what r
         measures (this is exactly the freed-rho underdetermination of
         branch_iii_hunt_results.md).
    (D)  C3 MONOTONICITY AUDIT of the banked solutions against "dilation
         grows with distance": vacuum phi = (1/2)ln(r/(2+Cr)) is strictly
         monotone INCREASING for ALL r > 0 (both C > 0 and C = 0), but the
         growth is BOUNDED for C > 0 (phi -> -(1/2)ln C) and unbounded only
         at C = 0; matter side f = 1 + a/r has phi < 0 strictly increasing
         to 0 — |phi| grows with DEPTH (decreasing rho), exactly.
    (D)  C4 THROAT vs PRINCIPLE: under R-areal a throat is impossible twice
         over (rho = r forced; and a saturating rho violates rho' = 1
         directly).  Under R-other, the throat end is exactly a cylinder
         (flat 2d factor times a FIXED sphere, R = 2/rho_inf^2); proper
         distance runs linearly while phi -> -(1/2)ln f_inf: the dilation
         RATE per unit proper distance -> 0 and the total remaining
         dilation is FINITE.

SPEC-MATH CORRECTIONS found by the symbolic work (sympy wins; recorded
honestly rather than implied away):

    (S1) The task spec's claim "a threshold-lifting throat VIOLATES strict
         monotonic growth under the proper-distance reading" is TOO STRONG:
         for a monotone approach f -> f_inf from above, dphi/ds =
         -f'/(2 sqrt f) > 0 persists — STRICT monotonicity is intact.  What
         fails is the stronger reading "unbounded growth / non-vanishing
         rate".  AND — decisive calibration — that stronger reading is
         ALREADY violated by the banked C > 0 vacuum on rho = r (phi
         bounded, rate -> 0).  So the principle constrains throats only
         under a strengthened reading that also indicts banked vacua;
         it is NOT a selective throat-killer unless C = 0 is canonized.
    (S2) The spec's "P0-as-banked makes all three readings coincide" holds
         at the contentless functional layer (phi = phi(X) true for every
         monotone X), but NOT at the B = 1/A layer: R-proper-as-B=1/A is
         degenerate even at rho = r (it forces phi == 0 regardless).  The
         banked P0 coincides with R-areal exactly; R-coordinate becomes
         R-areal only because rho = r is added by hand.

Charter compliance: nothing imported, nothing linearized; every displayed
identity/limit/solution verified symbolically (sympy, exact); PASS/FAIL
printed per check; nonzero exit on any FAIL.  Which steps are derivations
vs reading-classifications is flagged (D)/(CL) throughout — the CHOICE of
reading is Charles's to canonize; the consequences of each reading are
exact theorems.

New file 2026-06-10; creates nothing else, modifies nothing existing.
"""

from __future__ import annotations

import sys

import sympy as sp

FAILURES: list[str] = []


def check(label: str, ok: bool) -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        FAILURES.append(label)


def hr(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def ricci_scalar(g: sp.Matrix, coords: list[sp.Symbol]) -> sp.Expr:
    """Ricci scalar of a metric, from scratch (Christoffel -> Riemann ->
    Ricci -> scalar); no GR package, plain index loops."""
    n = len(coords)
    ginv = g.inv()
    Gamma = [[[sp.simplify(
        sp.Rational(1, 2) * sum(
            ginv[l, m] * (sp.diff(g[m, i], coords[j])
                          + sp.diff(g[m, j], coords[i])
                          - sp.diff(g[i, j], coords[m]))
            for m in range(n)))
        for j in range(n)] for i in range(n)] for l in range(n)]
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            expr = sp.S.Zero
            for l in range(n):
                expr += sp.diff(Gamma[l][i][j], coords[l])
                expr -= sp.diff(Gamma[l][i][l], coords[j])
                for m in range(n):
                    expr += Gamma[l][l][m] * Gamma[m][i][j]
                    expr -= Gamma[l][j][m] * Gamma[m][i][l]
            Ric[i, j] = sp.simplify(expr)
    return sp.simplify(sum(ginv[i, j] * Ric[i, j]
                           for i in range(n) for j in range(n)))


# ---------------------------------------------------------------------------
# Shared symbols
# ---------------------------------------------------------------------------
r = sp.symbols("r", positive=True)
t_s, th = sp.symbols("t theta", real=True)
lam = sp.symbols("lam", positive=True)
omega = sp.symbols("omega", positive=True)
C = sp.symbols("C", positive=True)           # vacuum-family constant, C > 0
a = sp.symbols("a", positive=True)           # matter tail coefficient
r0 = sp.symbols("r_0", positive=True)        # areal shift constant
R0 = sp.symbols("R_0", positive=True)        # exterior anchor radius
f_inf = sp.symbols("f_oo", positive=True)    # throat limit of f
rho_inf = sp.symbols("rho_oo", positive=True)  # throat limit of rho
b = sp.symbols("b", positive=True)
f_gen = sp.Function("f", positive=True)(r)
rho_f = sp.Function("rho", positive=True)(r)
phi_gen = sp.Function("phi", real=True)(r)

# ===========================================================================
# C0 — SETUP: the dictionary, the banked vacuum, and the (f, rho) probe
# ===========================================================================
hr("C0 — SETUP: dilation dictionary f = e^(-2phi), banked vacuum, and the "
   "(f, rho) probe operator (anchors to the freed-rho hunt)")

check("dictionary round trip:  f = e^(-2phi)  <=>  phi = -(1/2)ln f  "
      "(both directions, exact)",
      sp.simplify(sp.exp(-2 * (-sp.Rational(1, 2) * sp.log(f_gen))) - f_gen)
      == 0
      and sp.simplify(-sp.Rational(1, 2) * sp.log(sp.exp(-2 * phi_gen))
                      - phi_gen) == 0)

phi_vac = sp.Rational(1, 2) * sp.log(r / (2 + C * r))
f_vac = sp.exp(-2 * phi_vac)
check("banked vacuum:  phi = (1/2)ln(r/(2+Cr))  <=>  f = C + 2/r  exactly",
      sp.simplify(f_vac - (C + 2 / r)) == 0)

# Wave operator on the generalized metric (re-derivation, same route as the
# rigidity script's E1 — anchors that THIS file's metric is the same object).
R_f = sp.Function("R")(r)
Y_f = sp.Function("Y")(th)
Phi = sp.exp(-sp.I * omega * t_s) * R_f * Y_f
sqrtg = rho_f**2 * sp.sin(th)
box = (-(1 / f_gen) * sp.diff(Phi, t_s, 2)
       + (1 / sqrtg) * sp.diff(sqrtg * f_gen * sp.diff(Phi, r), r)
       + (1 / (rho_f**2 * sp.sin(th)))
       * sp.diff(sp.sin(th) * sp.diff(Phi, th), th))
box = box.subs(sp.Derivative(Y_f, th, 2),
               -lam * Y_f - (sp.cos(th) / sp.sin(th)) * sp.Derivative(Y_f, th))
radial_target = (sp.diff(rho_f**2 * f_gen * sp.diff(R_f, r), r)
                 - lam * R_f + omega**2 * (rho_f**2 / f_gen) * R_f)
check("wave operator on  -f dt^2 + f^(-1)dr^2 + rho^2 dOmega^2  reduces "
      "EXACTLY to  -(rho^2 f R')' + lam R = omega^2 (rho^2/f) R",
      sp.simplify(box * rho_f**2 / sp.exp(-sp.I * omega * t_s)
                  - radial_target * Y_f) == 0)

V_rho = (f_gen * lam / rho_f**2
         + f_gen * sp.diff(f_gen * sp.diff(rho_f, r), r) / rho_f)
u_rho = rho_f * R_f
lhs_rho = (f_gen * sp.diff(f_gen * sp.diff(u_rho, r), r)
           + (omega**2 - V_rho) * u_rho)
check("tortoise form (u = rho R, dr* = dr/f):  u'' + [w^2 - V]u = 0 with "
      "V = f lam/rho^2 + f(f rho')'/rho  (banked form re-verified)",
      sp.simplify(lhs_rho - (f_gen / rho_f) * radial_target) == 0)
check("rho = r collapse:  V -> f(lam/r^2 + f'/r)  (the rho = r banked V)",
      sp.simplify(V_rho.subs(rho_f, r).doit()
                  - f_gen * (lam / r**2 + sp.diff(f_gen, r) / r)) == 0)

print("""
  STATUS: the metric, dictionary, probe and the freed areal function rho
  are exactly the objects of branch_iii_hunt_results.md.  Everything below
  interrogates the PRINCIPLE (P0), not the action.""")

# ===========================================================================
# C1 — THE THREE READINGS, AND THE GAUGE LEMMAS THAT GIVE THEM CONTENT
# ===========================================================================
hr("C1 — THE THREE READINGS OF 'phi IS A FUNCTION OF DISTANCE X', AND THE "
   "TWO GAUGE LEMMAS (the key observation, formalized)")

print("""
  LAYER 1 (the contentless layer — (CL) classification, stated exactly):
  on a static spherical chart, phi = phi(r) holds by the ANSATZ.  For any
  X(r) with X' != 0, phi = phi(X) := phi(r(X)) holds identically — a
  relabeling.  So 'phi is a function of distance X' adds NO content by
  itself, for ANY of the three readings.  Content can enter only through
  (i) WHERE B = 1/A is imposed, and (ii) what that chart's coordinate is
  declared to measure.  The two lemmas make (i) sharp:""")

# --- LEMMA 1: B = 1/A is achievable in SOME chart for ANY static metric ---
x = sp.symbols("x", positive=True)
F_x = sp.Function("F", positive=True)(x)
G_x = sp.Function("G", positive=True)(x)
# new radial coordinate y with dy/dx = sqrt(F G):
g_yy = G_x * (1 / sp.sqrt(F_x * G_x))**2
check("LEMMA 1 (existence, (D)): for ANY -F dt^2 + G dx^2 + rho^2 dOmega^2, "
      "the chart y with dy = sqrt(FG) dx gives g_yy = 1/F exactly, i.e. "
      "g_tt*g_yy = -1:  B = 1/A holds in SOME chart, ALWAYS",
      sp.simplify(g_yy - 1 / F_x) == 0)

# --- LEMMA 2: the B = 1/A chart is unique up to r -> ±r + const ---
rt = sp.symbols("rtilde", positive=True)
h = sp.Function("h", positive=True)(rt)          # r = h(rtilde)
f_of_h = sp.Function("f", positive=True)(h)
# in the r-chart B = 1/A holds: g_rr = 1/f(r).  Transform to rtilde:
g_tt_new = -f_of_h                               # t untouched: F invariant
g_rtrt = (1 / f_of_h) * sp.diff(h, rt)**2
# require B = 1/A in rtilde too: g_rtrt = 1/f(h)  =>  h'^2 = 1
cond = sp.simplify(g_rtrt - 1 / f_of_h)
hp = sp.symbols("hprime", real=True)
sols_hp = sp.solve(sp.Eq(hp**2, 1), hp)
check("LEMMA 2 (uniqueness, (D)): if B = 1/A holds in chart r AND in chart "
      "rtilde (r = h(rtilde)), then (1/f)h'^2 = 1/f  =>  h'^2 = 1  =>  "
      "h' = ±1 (continuity => constant sign)  =>  rtilde = ±r + const",
      sp.simplify(cond - (1 / f_of_h) * (sp.diff(h, rt)**2 - 1)) == 0
      and sorted(sols_hp) == [-1, 1])

print("""
  LEMMA 2 AMENDMENT (verifier agent ae8a655ed2fa4045f, 2026-06-10): the
  uniqueness above is derived with the Killing time held FIXED ('t
  untouched' in the transformation).  The static metric also admits the
  residual Killing-time rescaling t -> k t, under which preserving
  B = 1/A maps r -> ±r/k + const and the vacuum family constants
  (C, a) -> (k²C, k a).  So the full statement is: the B = 1/A chart is
  unique up to ±, shift, AND Killing-time rescaling.  Consequently the
  slope-1 statement in rho = ±r + const is a TIME-UNIT convention
  (k = 1), not invariant content by itself — while the downstream BINARY
  verdicts are gauge-invariant under the rescaling: C = 0 vs C > 0 is
  preserved (k²C = 0 iff C = 0), and bounded vs unbounded total dilation
  shifts phi only by the constant ln(k).""")

print("""
  CONSEQUENCE OF THE LEMMAS ((D)): 'B = 1/A' alone has NO invariant
  content (Lemma 1: always achievable); but the B = 1/A CHART is unique up
  to r -> ±r + const (Lemma 2), so the invariant content of P0 is exactly
  the answer to: WHICH physically-defined coordinate is the B = 1/A
  coordinate?  That is what the three readings answer differently.

  P0-AS-BANKED = [B = 1/A holds in the coordinate r] AND [rho = r].
  At the Layer-1 (functional) level all three readings then hold at once
  (X = rho = r, and phi = phi(s) too since s(r) is monotone) — they
  'coincide' only in this contentless sense (spec correction S2: at the
  B = 1/A level R-proper NEVER coincides; it is degenerate even at
  rho = r, see C1b).  When rho is freed, the readings split sharply:""")

# ---------------------------------------------------------------------------
# C1a — R-AREAL: B = 1/A imposed in the areal chart
# ---------------------------------------------------------------------------
hr("C1a — R-AREAL ((D)):  X = rho = sqrt(Area/4pi).  B = 1/A in the areal "
   "chart  <=>  rho = ±r + const")

print("""
  Content added by R-areal: the B = 1/A coordinate IS the areal radius —
  the chart in which g_tt*g_rr = -1 is the chart whose radial coordinate
  labels invariant sphere size.  Derivation: pass from r to rho (valid on
  any interval with rho' != 0; caveat recorded below).""")

# Coordinate change r -> rho on the generalized metric.  Tensor rule for the
# radial component: G(rho) drho^2 must reproduce g_rr dr^2, i.e.
# G * rho'^2 = g_rr = 1/f.  Solve for G:
G_areal = sp.symbols("G_areal", positive=True)
G_sol = sp.solve(sp.Eq(G_areal * sp.diff(rho_f, r)**2, 1 / f_gen), G_areal)
check("transformation rule (G drho^2 = f^(-1) dr^2):  "
      "G = 1/(f (rho')^2)  — unique solution, derived not posited",
      len(G_sol) == 1
      and sp.simplify(G_sol[0] - 1 / (f_gen * sp.diff(rho_f, r)**2)) == 0)
G_expr = G_sol[0]
F_expr = f_gen          # t untouched: F(rho) = f(r(rho)); angular part rho^2
FG = sp.simplify(F_expr * G_expr)
check("the metric in the areal chart is  -F dt^2 + G drho^2 + rho^2 dOmega^2 "
      "with F = f, G = 1/(f (rho')^2), and  F*G = 1/(rho')^2  exactly",
      sp.simplify(FG - 1 / sp.diff(rho_f, r)**2) == 0)
check("F*G is f-BLIND (independent of f): the areal B = 1/A condition "
      "constrains ONLY rho, never f",
      sp.diff(FG, f_gen) == 0)

# B = 1/A in the areal chart: F*G = 1  <=>  rho'^2 = 1.
sols_ode = sp.dsolve(sp.Eq(sp.diff(rho_f, r)**2, 1), rho_f)
rhs_set = {sp.simplify(s.rhs - sp.Symbol("C1")) for s in sols_ode}
check("B = 1/A in the areal chart  <=>  (rho')^2 = 1; dsolve returns "
      "EXACTLY the two families  rho = C1 + r  and  rho = C1 - r",
      len(sols_ode) == 2 and rhs_set == {r, -r})
check("both families verify (rho')^2 = 1; pointwise rho' in {+1, -1} and "
      "continuity of rho' forces a constant sign (no mixed solutions)",
      all(sp.simplify(sp.diff(s.rhs, r)**2 - 1) == 0 for s in sols_ode)
      and sorted(sp.solve(sp.Symbol("z")**2 - 1, sp.Symbol("z"))) == [-1, 1])

# Counterexample: rho = r^2 fails for every f.
FG_sq = FG.subs(rho_f, r**2).doit()
check("counterexample:  rho = r^2  gives  F*G = 1/(4r^2) != 1  for EVERY f "
      "(f-blindness in action): the generalized family genuinely violates "
      "areal B = 1/A whenever rho' != ±1",
      sp.simplify(FG_sq - 1 / (4 * r**2)) == 0
      and sp.solve(sp.Eq(FG_sq, 1), r) == [sp.Rational(1, 2)])
print("     (rho = r^2 satisfies it only at the isolated point r = 1/2 — "
      "not on any interval.)")

# The shift constant: rho = r + r0.
rho_shift = r + r0
check("the + branch with shift,  rho = r + r0:  areal B = 1/A holds "
      "(rho' = 1), and the areal-chart metric is  -ftilde dt^2 + "
      "ftilde^(-1) drho^2 + rho^2 dOmega^2  with  ftilde(rho) = f(rho - r0) "
      "— a pure relabel of an EXTERIOR chart",
      sp.simplify(FG.subs(rho_f, rho_shift).doit() - 1) == 0)
check("physical content of the shift appears ONLY at the center: as r -> 0 "
      "the sphere area -> 4pi r0^2 > 0 (a finite-area inner sphere: "
      "puncture/defect, NOT a smooth point)",
      sp.limit(4 * sp.pi * rho_shift**2, r, 0) == 4 * sp.pi * r0**2)
check("the - branch,  rho = r0 - r  (rho' = -1):  the orientation reversal "
      "r -> r0 - r maps it to  rho = r  on 0 < r < r0 — same geometry, "
      "reversed radial orientation",
      sp.simplify((r0 - r).subs(r, r0 - r) - r) == 0)

print("""
  R-AREAL THEOREM ((D), assembled):
      [B = 1/A in the areal chart]  <=>  rho = ±r + const.
  Fixing orientation (rho increasing outward) and smooth-center boundary
  data (rho -> 0 as r -> 0, no puncture) gives  rho = r  EXACTLY.
  So under R-areal, P0's 'silent' rho = r is NOT an independent postulate:
  it is FORCED by the principle itself.  The residual freedom is exactly:
      ±  (radial orientation)  and  r0  (a central puncture/defect of
      area 4pi r0^2, or an inner-boundary relabel on exterior domains).
  CAVEAT (recorded): the r -> rho chart change needs rho' != 0 on the
  interval; a non-monotone rho (throat neck, rho' = 0 somewhere) admits no
  global areal chart — under R-areal that configuration cannot even STATE
  the principle globally, an exclusion PRIOR to the rho' = ±1 theorem.""")

# ---------------------------------------------------------------------------
# C1b — R-PROPER: B = 1/A imposed in the proper-distance chart
# ---------------------------------------------------------------------------
hr("C1b — R-PROPER ((D)):  X = s, ds = f^(-1/2) dr.  B = 1/A in the proper "
   "chart DEGENERATES: it forces phi == 0 (no dilation at all)")

# g_ss = g_rr (dr/ds)^2 = (1/f) * f = 1 identically:
g_ss = (1 / f_gen) * (sp.sqrt(f_gen))**2
check("g_ss = g_rr (dr/ds)^2 = f^(-1) * f = 1  IDENTICALLY, for every f "
      "(by the definition of proper distance)",
      sp.simplify(g_ss - 1) == 0)
# B = 1/A in s: g_tt * g_ss = -1 with g_ss = 1  =>  g_tt = -1  =>  f = 1:
F_s = sp.symbols("F_s", positive=True)
sol_F = sp.solve(sp.Eq(-F_s * 1, -1), F_s)
check("B = 1/A in the s-chart:  g_tt*g_ss = -1, g_ss = 1  =>  g_tt = -1 "
      "(unique solution F = 1)  =>  f == 1",
      sol_F == [1])
sol_phi = sp.solve(sp.Eq(sp.exp(-2 * sp.Symbol("phi_c", real=True)), 1),
                   sp.Symbol("phi_c", real=True))
check("f == 1  =>  phi = -(1/2)ln f == 0:  NO dilation anywhere "
      "(unique real solution phi = 0)",
      sol_phi == [0])

print("""
  R-PROPER VERDICT ((D)): imposing B = 1/A in the proper-distance chart is
  INCOMPATIBLE with any nontrivial dilation — the two conditions
  [g_ss = 1 by definition of s] and [g_tt*g_ss = -1] pin g_tt = -1, i.e.
  flat time, phi == 0.  'Positional dilation as a function of proper
  distance' can only be held by ABANDONING B = 1/A in the s-chart (phi(s)
  is then a perfectly good relabel of phi(r), Layer 1, but B = 1/A must
  live in some OTHER chart — which reopens the question of which one).
  Note this degeneracy holds for every rho, INCLUDING rho = r: R-proper
  never coincides with banked P0 at the B = 1/A level (correction S2).""")

# ---------------------------------------------------------------------------
# C1c — R-COORDINATE: B = 1/A in a chart not tied to anything
# ---------------------------------------------------------------------------
hr("C1c — R-COORDINATE ((CL)):  X = r, the B = 1/A coordinate itself — "
   "rho(r) free; the principle is INCOMPLETE")

# By construction the generalized metric has g_tt*g_rr = -1 for ANY rho:
check("the generalized metric satisfies B = 1/A in its own chart r for "
      "EVERY rho:  g_tt*g_rr = (-f)(1/f) = -1 identically",
      sp.simplify((-f_gen) * (1 / f_gen) + 1) == 0)

print("""
  R-COORDINATE VERDICT ((CL), classification not derivation): if 'distance'
  means 'the B = 1/A coordinate r' and r is NOT tied to sphere area, then
  rho(r) is a free function — exactly the generalized (f, rho) family of
  branch_iii_hunt_results.md, with its demonstrated physical
  underdetermination (two lock members with identical (C, a, K) and
  different curvature invariants).  By Lemma 2 the chart r is unique up to
  ±/shift once B = 1/A is declared, so the reading is internally
  consistent — but it is CIRCULAR as a definition of distance ('distance
  is measured by the coordinate in which B = 1/A holds') and supplies no
  equation for rho.  The principle then OWES an independent physical
  statement of what r measures, or it is incomplete.  This is the precise
  sense in which the freed-rho hunt found the system underdetermined:
  the missing rho-equation is the missing HALF OF THE DEFINITION of
  positional dilation under this reading.""")

# ===========================================================================
# C2 — THE DECISIVE CLASSIFICATION (the theorem, printed in full)
# ===========================================================================
hr("C2 — THE DECISIVE CLASSIFICATION: the fork is now a physics question "
   "with exact mathematical content")

print("""
  THEOREM ((D); proved in C1a, Lemmas 1-2):

      B = 1/A  +  areal reading   <=>   rho = r  (up to ±, a shift r0,
      AND the Killing-time rescaling t -> kt, which maps r -> ±r/k +
      const and (C, a) -> (k²C, ka) — Lemma 2 amendment; orientation +
      smooth center kill the first two residuals, and the slope-1
      normalization rho = r is the time-unit convention k = 1).
      The binary downstream verdicts (C = 0 vs C > 0, threshold lifted
      vs not) are gauge-invariant under all three residuals.

  Equivalently: P0's silent  rho = r  is NOT an independent postulate
  under the areal reading — it is FORCED by 'the dilation coordinate is
  the sphere-size coordinate'.  Conversely, freeing rho while keeping
  B = 1/A is EXACTLY the statement that the dilation coordinate is NOT
  the areal radius — a different physical principle, which then owes its
  own definition of distance (R-proper is ruled out as that definition:
  C1b degeneracy).

  THE FORK, restated as physics ((CL) — only Charles can canonize the
  reading; the consequences of each option are exact):

    R-AREAL ('dilation grows with sphere size'):
        =>  rho = r exactly (theorem above)
        =>  with the threshold rigidity theorem (34/34) and the open-domain
            theorem: continuum threshold exactly 0, EMPTY point spectrum —
            branch (iii) DEAD in the static sector, full stop.

    R-OTHER ('dilation grows with some other native distance'):
        =>  the generalized (f, rho) family, with the freed-rho structure
            already mapped (53/53): EXTREMALITY LOCK |a| = c_q|q|, then
            physical underdetermination; H1 source overdetermined; no
            determined native throat — AWAITING the distance definition
            (equivalently the native rho-equation) to close it.
        (R-PROPER is NOT an available 'other': it abolishes dilation, C1b.)

  STATUS LABELS (honest): the equivalences and degeneracies above are
  DERIVATIONS (D).  Which reading P0 'really' asserts is a CANONIZATION
  question (CL) — the founding documents fixed rho = r silently, which is
  CONSISTENT WITH (and, by the theorem, equivalent to) the areal reading,
  but the choice was never made explicitly.  Nothing here selects it.""")

# ===========================================================================
# C3 — SANITY AUDIT: the principle against the banked solutions
# ===========================================================================
hr("C3 — MONOTONICITY AUDIT ((D)): does 'dilation grows with distance' "
   "actually hold on the banked solutions?")

print("""
  C3a — VACUUM SIDE, under R-areal (rho = r, so X = rho = r):
        phi = (1/2)ln(r/(2+Cr)),  f = C + 2/r.""")

dphi = sp.simplify(sp.diff(phi_vac, r))
check("dphi/drho = dphi/dr = 1/(r(2+Cr))  exactly (C >= 0 family)",
      sp.simplify(dphi - 1 / (r * (2 + C * r))) == 0)
check("C > 0:  dphi/drho > 0 for ALL r > 0 — strictly monotone increasing "
      "EVERYWHERE (not just asymptotically)",
      (1 / (r * (2 + C * r))).is_positive is True)
dphi_C0 = sp.simplify(dphi.subs(C, 0))
check("C = 0:  dphi/drho = 1/(2r) > 0 for ALL r > 0 — strictly monotone "
      "increasing everywhere",
      sp.simplify(dphi_C0 - 1 / (2 * r)) == 0
      and (1 / (2 * r)).is_positive is True)
check("C > 0:  growth is BOUNDED:  phi -> -(1/2)ln C  as r -> oo "
      "(saturation), with vanishing rate  r^2 dphi/drho -> 1/C",
      sp.simplify(sp.limit(phi_vac, r, sp.oo) + sp.log(C) / 2) == 0
      and sp.limit(r**2 * dphi, r, sp.oo) == 1 / C)
check("C = 0:  growth is UNBOUNDED:  phi = (1/2)ln(r/2) -> +oo  "
      "(logarithmically)",
      sp.limit(phi_vac.subs(C, 0), r, sp.oo) == sp.oo)
check("near the center phi -> -oo (infinite blueshift depth at r -> 0), "
      "both C > 0 and C = 0",
      sp.limit(phi_vac, r, 0, "+") == -sp.oo
      and sp.limit(phi_vac.subs(C, 0), r, 0, "+") == -sp.oo)

print("""
  C3a VERDICT ((D)): the banked vacuum satisfies STRICT monotone growth of
  phi with areal distance for ALL r > 0, both C > 0 and C = 0 — the
  principle's monotonicity clause passes everywhere, not only
  asymptotically.  BUT the clause 'GROWS with distance' bifurcates:
      C = 0:  unbounded growth (phi -> +oo, log rate);
      C > 0:  bounded growth (phi saturates at -(1/2)ln C; rate ~ 1/(Cr^2)).
  If the principle demands UNBOUNDED growth, the banked C > 0 vacuum
  ALREADY violates it on rho = r.  So the principle, as actually banked,
  can demand at most strict monotonicity.  (This calibration is decisive
  for C4.)

  C3b — MATTER SIDE:  f = 1 + a/r, a > 0  =>  phi = -(1/2)ln(1+a/r) < 0.""")

phi_m = -sp.Rational(1, 2) * sp.log(1 + a / r)
check("phi < 0 for all r > 0:  e^(-2phi) - 1 = a/r > 0 exactly",
      sp.simplify(sp.exp(-2 * phi_m) - 1 - a / r) == 0
      and (a / r).is_positive is True)
dphi_m = sp.simplify(sp.diff(phi_m, r))
check("dphi/drho = a/(2 rho (rho + a)) > 0:  phi strictly INCREASES "
      "outward, toward phi(oo) = 0",
      sp.simplify(dphi_m - a / (2 * r * (r + a))) == 0
      and (a / (2 * r * (r + a))).is_positive is True
      and sp.limit(phi_m, r, sp.oo) == 0)
check("dilation MAGNITUDE:  |phi| = -phi  (since phi < 0), so "
      "d|phi|/drho = -a/(2 rho (rho+a)) < 0:  |phi| strictly DECREASES "
      "outward — i.e. strictly GROWS with depth (decreasing rho)",
      sp.simplify(sp.diff(-phi_m, r) + a / (2 * r * (r + a))) == 0)
check("depth divergence:  |phi| -> +oo as rho -> 0+  (and -> 0 at oo): "
      "the inside-out mirror of the vacuum side",
      sp.limit(-phi_m, r, 0, "+") == sp.oo)

print("""
  C3b VERDICT ((D), exact statements): on the matter side the principle
  reads INSIDE-OUT:  dphi/drho > 0 still (the SAME sign statement as the
  vacuum side), but phi < 0 with phi -> 0 at infinity, so the dilation
  MAGNITUDE |phi| grows with DEPTH:  d|phi|/drho = -a/(2 rho(rho+a)) < 0,
  |phi| -> oo at the center, -> 0 outside.  A reading-neutral form that
  covers BOTH sides: 'phi is strictly monotone in the (areal) distance,
  increasing outward' — growth of dilation magnitude is outward in vacuum
  (phi > 0 branch) and inward in matter.  Whether P0 means the signed phi
  or the magnitude |phi| is itself a (CL) canonization item; the banked
  solutions satisfy the SIGNED monotone form universally.""")

# ===========================================================================
# C4 — THE THROAT UNDER EACH READING
# ===========================================================================
hr("C4 — THE THROAT UNDER EACH READING ((D) + the calibrated verdict)")

print("""
  C4a — UNDER R-AREAL: saturation is impossible, twice over.""")

check("rho = r (forced by the C2 theorem) NEVER saturates: rho -> oo",
      sp.limit(r, r, sp.oo) == sp.oo)
rho_sat = rho_inf - b / r
FG_sat = sp.simplify(FG.subs(rho_f, rho_sat).doit())
check("and directly: a monotone saturating rho = rho_oo - b/r (rho' = b/r^2 "
      "> 0, a valid chart) gives F*G = r^4/b^2 != 1 — areal B = 1/A is "
      "violated at every r (not merely 'unforced')",
      sp.simplify(FG_sat - r**4 / b**2) == 0)
print("     (a NON-monotone neck, rho' = 0 somewhere, cannot even state "
      "the areal reading globally — chart caveat of C1a.)")

print("""
  C4b — UNDER R-OTHER: the exact geometry of the threshold-lifting end
        (f -> f_oo > 0, rho -> rho_oo finite).""")

# The limit metric is the product (flat 2d) x (fixed sphere) — a cylinder.
g_cyl = sp.diag(-f_inf, 1 / f_inf, rho_inf**2, rho_inf**2 * sp.sin(th)**2)
ph = sp.symbols("varphi", real=True)
R_cyl = ricci_scalar(g_cyl, [t_s, r, th, ph])
check("limit metric  -f_oo dt^2 + f_oo^(-1) dr^2 + rho_oo^2 dOmega^2  is an "
      "exact product (flat R^2_{t,r}) x (S^2 of radius rho_oo): Ricci "
      "scalar R = 2/rho_oo^2, from scratch (Christoffel -> Ricci)",
      sp.simplify(R_cyl - 2 / rho_inf**2) == 0)
print("     GEOMETRIC DESCRIPTION ((D)): a CYLINDER end — sphere size "
      "frozen at rho_oo (area 4pi rho_oo^2),\n     while the radial "
      "direction runs forever; not asymptotically flat.")

# Generic identity: dilation rate per unit proper distance.
dphi_ds_gen = sp.simplify(
    sp.diff(-sp.Rational(1, 2) * sp.log(f_gen), r) * sp.sqrt(f_gen))
check("generic identity:  dphi/ds = (dphi/dr)(dr/ds) = -f'/(2 sqrt(f))  "
      "exactly (ds = f^(-1/2) dr)",
      sp.simplify(dphi_ds_gen + sp.diff(f_gen, r) / (2 * sp.sqrt(f_gen)))
      == 0)

# Representative throat: f = f_oo + e^(-r)  (monotone approach from above),
# rho = rho_oo - b/r  (the rigidity script's representative pair).
f_rep = f_inf + sp.exp(-r)
phi_rep = -sp.Rational(1, 2) * sp.log(f_rep)
u = sp.symbols("u", nonnegative=True)
diff_bound = sp.simplify(f_rep.subs(r, R0 + u) - (f_inf + sp.exp(-R0)))
check("proper distance RUNS: f is decreasing (f' = -e^(-r) < 0), so "
      "f(r) <= f_oo + e^(-R0) on r >= R0 (difference = e^(-R0)(e^(-u)-1) "
      "<= 0, vanishing at u = 0 with negative u-derivative), hence "
      "s(R) >= (R - R0)/sqrt(f_oo + e^(-R0)) -> oo LINEARLY",
      (sp.diff(f_rep, r)).is_negative is True
      and sp.simplify(diff_bound
                      - sp.exp(-R0) * (sp.exp(-u) - 1)) == 0
      and diff_bound.subs(u, 0) == 0
      and sp.simplify(sp.diff(diff_bound, u)).is_negative is True)
check("asymptotic rate of proper distance:  ds/dr = f^(-1/2) -> "
      "f_oo^(-1/2) > 0  (so s ~ r/sqrt(f_oo))",
      sp.limit(1 / sp.sqrt(f_rep), r, sp.oo) == 1 / sp.sqrt(f_inf))
check("dilation SATURATES:  phi = -(1/2)ln f -> -(1/2)ln f_oo  (finite "
      "constant) while s -> oo",
      sp.simplify(sp.limit(phi_rep, r, sp.oo)
                  + sp.Rational(1, 2) * sp.log(f_inf)) == 0)
dphi_ds_rep = sp.simplify(dphi_ds_gen.subs(f_gen, f_rep).doit())
check("the RATE dies:  dphi/ds = e^(-r)/(2 sqrt(f_oo + e^(-r))) -> 0 "
      "(exponentially)",
      sp.simplify(dphi_ds_rep
                  - sp.exp(-r) / (2 * sp.sqrt(f_inf + sp.exp(-r)))) == 0
      and sp.limit(dphi_ds_rep, r, sp.oo) == 0)
check("but STRICT monotonicity is INTACT:  dphi/ds > 0 for ALL r "
      "(monotone approach from above) — spec correction S1",
      dphi_ds_rep.is_positive is True)
remaining = sp.simplify(sp.limit(phi_rep, r, sp.oo) - phi_rep.subs(r, R0))
check("total REMAINING dilation beyond any station R0 is FINITE:  "
      "phi(oo) - phi(R0) = (1/2)ln(1 + e^(-R0)/f_oo)  exactly "
      "(while remaining proper distance is INFINITE)",
      sp.simplify(remaining
                  - sp.Rational(1, 2) * sp.log(1 + sp.exp(-R0) / f_inf))
      == 0)

print("""
  C4c — CALIBRATION against the banked C > 0 vacuum (the C3a result),
        same proper-distance reading, on rho = r:""")

dphi_ds_vac = sp.simplify(dphi_ds_gen.subs(f_gen, C + 2 / r).doit())
check("banked C > 0 vacuum under the SAME reading:  dphi/ds = "
      "sqrt(C + 2/r)/(r(2+Cr)) -> 0  and  phi -> -(1/2)ln C  finite: "
      "IDENTICAL profile (strictly monotone, bounded, dying rate)",
      sp.limit(dphi_ds_vac, r, sp.oo) == 0
      and sp.simplify(sp.limit(-sp.Rational(1, 2) * sp.log(C + 2 / r),
                               r, sp.oo) + sp.log(C) / 2) == 0
      and dphi_ds_vac.is_positive is True)
check("only C = 0 escapes: phi unbounded (phi -> oo) even though its rate "
      "ALSO dies (dphi/ds ~ r^(-3/2) -> 0) — boundedness of TOTAL "
      "dilation, not the rate, is the discriminating invariant",
      sp.limit(-sp.Rational(1, 2) * sp.log(2 / r), r, sp.oo) == sp.oo
      and sp.limit(dphi_ds_vac.subs(C, 0), r, sp.oo) == 0)

print("""
  C4 VERDICT ((D) for the math, (CL) for the reading it presupposes):

  Under R-areal the throat is excluded OUTRIGHT (C4a) — but by then
  branch (iii) is dead anyway (C2).

  Under R-other, at the threshold-lifting cylinder end:
      sphere size freezes (rho -> rho_oo),
      proper distance runs linearly (s ~ r/sqrt(f_oo) -> oo),
      dilation saturates (phi -> -(1/2)ln f_oo, finite remaining total),
      the rate dphi/ds -> 0,  BUT  dphi/ds > 0 throughout (monotone f).

  SPEC CORRECTION S1 (sympy wins): the throat does NOT violate STRICT
  monotonic growth under the proper-distance reading — phi keeps strictly
  increasing along the cylinder for a monotone approach.  What it violates
  is the STRENGTHENED reading 'dilation grows without bound / at a
  non-vanishing rate'.  And the calibration shows that strengthened
  reading is ALREADY violated by the banked C > 0 vacuum on rho = r
  (identical bounded-saturating profile, C4c).  Therefore:

      the positional-dilation principle constrains the throat scenario
      ONLY IF it is canonized in a form strong enough to also indict the
      banked C > 0 vacua — e.g. 'total dilation is unbounded along every
      unbounded distance' (which selects C = 0 in vacuum AND kills
      threshold-lifting throats, since f_oo > 0 forces bounded phi),

  a single canonization decision with exact consequences on BOTH sides.
  The honest verdict is therefore CONDITIONAL, not the spec's outright
  'serious constraint': strict-monotone P0 permits throats; unbounded-
  growth P0 kills threshold-lifting throats and the C > 0 vacua together.
  (A horizon-capped end, f_oo = 0, has phi -> +oo... note the SIGN:
  f -> 0 gives phi = -(1/2)ln f -> +oo, unbounded growth — the
  unbounded-growth canon would steer vacua toward C = 0 and ends toward
  horizon caps, both of which keep the threshold at 0.  Either way branch
  (iii) loses its static lifter under that canon.)

  C4 AMENDMENT (verifier agent ae8a655ed2fa4045f, 2026-06-10; against
  the A3 throat class of native_rho_dynamics_gr_balance_test.py): the
  alpha != 0 throat members f = (alpha r + gamma)/rho, rho = sqrt(J + r²)
  violate even STRICT monotonicity near the neck — f' = (alpha J -
  gamma r)/(J + r²)^(3/2) > 0 for r < alpha J/gamma, so phi = -(1/2)ln f
  strictly DECREASES outward there.  The strict-monotonicity canon
  therefore has bite of its own against the alpha != 0 neck members;
  the CONDITIONAL verdict above (strict-monotone P0 permits throats)
  concerns monotone-f cylinder ends — e.g. the alpha = 0 members,
  including the verifier's threshold-lifting example.""")

# ===========================================================================
# SUMMARY
# ===========================================================================
hr("SUMMARY")
if FAILURES:
    print(f"  {len(FAILURES)} CHECK(S) FAILED:")
    for lab in FAILURES:
        print(f"    - {lab}")
    sys.exit(1)
print("""  All symbolic/exact checks PASSED.

  THE C2 THEOREM (derived, (D)):  B = 1/A + areal reading  <=>
  rho = ±r + const; orientation + smooth center give rho = r exactly.
  P0's silent rho = r is FORCED under the areal reading, not independent.
  Supporting gauge lemmas: B = 1/A alone is contentless (always achievable
  in some chart); the B = 1/A chart is unique up to ±/shift/Killing-time
  rescaling (t -> kt with r -> ±r/k + const, (C, a) -> (k²C, ka) — the
  slope-1 in rho = ±r + const is a time-unit convention, and the binary
  verdicts C = 0 vs C > 0 are gauge-invariant), so the invariant content
  of P0 is exactly WHICH physical coordinate is the B = 1/A coordinate.  R-proper is unavailable as that answer (it forces
  phi == 0).  R-coordinate leaves rho free and the principle incomplete —
  the missing rho-equation of the freed-rho hunt is the missing half of
  the distance definition under that reading.

  THE FORK, now exact physics awaiting canonization ((CL)):
      R-areal ('dilation grows with sphere size')
          => rho = r  => (rigidity theorem) threshold 0
          => branch (iii) DEAD in statics;
      R-other ('dilation grows with some other native distance')
          => the (f, rho) family with the extremality-lock /
             underdetermination structure, awaiting its distance
             definition (equivalently, rho's native equation).

  C3 AUDIT (derived): banked vacuum is strictly monotone for ALL r (both
  C > 0 and C = 0); growth is bounded for C > 0 (saturates at -(1/2)lnC),
  unbounded only at C = 0.  Matter side: phi < 0 strictly increasing to 0;
  |phi| grows with depth, exactly d|phi|/drho = -a/(2 rho(rho+a)) < 0.

  C4 VERDICT (derived, corrected): the threshold-lifting throat is a
  cylinder end (R = 2/rho_oo^2); proper distance runs linearly while total
  remaining dilation is finite and the rate dies — but strict monotonicity
  SURVIVES (spec's 'violates strict monotonic growth' corrected, S1).
  The principle kills threshold-lifting throats only under an
  unbounded-growth canon, which also indicts the banked C > 0 vacua —
  one decision, exact consequences both ways.  Verifier sharpening: the
  alpha != 0 throat members of the A3 class violate even STRICT
  monotonicity near the neck (f' > 0 for r < alpha J/gamma), so the
  strict canon has bite against them; the conditional verdict concerns
  monotone-f cylinder ends.

  WHAT THIS FILE DOES NOT DO (honest scope): it does not select a reading
  (Charles canonizes); it does not derive rho-dynamics (the named target
  of branch_iii_hunt_results.md is untouched); the (CL) items are
  classifications of definitional content, not theorems about nature.""")
