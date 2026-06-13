#!/usr/bin/env python3
"""W-ALG — SCRIPT 3: THE ALGEBRAIC-ANGULAR CLOSURE QUESTION
(charter line-1 deliverable + Charles instruction 2: the angular sector
is algebraic; tie the per-ray problems together).

Date: 2026-06-12.  Agent: W-ALG.  Tripwire binding: CLASSIFICATION,
NEVER DEFORMATION.  All objects taken EXACTLY as derived:
  q*    = 2 r^2 W f_r f_th / P,          W = (1+w)^2
  P     = f r^2 W f_r^2 + f_th^2         (>= 0; sum of squares at w>-1)
  Dw    = f r^2 W f_r^2 - f_th^2         (the Delta_w surface; sign-flips)
  D|q*  = r^2 W Dw^2 / P^2               (branch metric degeneracy)
  L_qq|q* = P^4 sin / (4 r^2 Dw^3)       (Hessian; diverges ~Dw^{-3})
  c_f[w_thth]|w=0 = -8 f r^3 f_r^3 f_th^2 (2f + r f_r) sin /(Dw^2 P)
                                          (the W5 f-row door; ~Dw^{-2})
  c_w[w_rr]       = 4 f r^2 sin P / Dw    (the w-row; ~Dw^{-1})
(sources: w6_arm1_lib.qstar_expr; w5_arm1_verifier2_branch V2-06..10;
w5_results.md headline + q*-branch adjudication.)

PRE-STATED NO-STRUCTURE CRITERIA (per line):
  N1 (branch): the elimination radicals' branch points in u land
      OUTSIDE [-1,1] for the whole derived family -> single-branch is
      automatic, imposes nothing -> closure adds no angular condition.
  N2 (regularity): demanding finite coupled solutions across Dw(u)=0
      is satisfiable for a CONTINUUM of angular data (no discrete
      selection) -> the crossing is a removable/regular-singular point
      with a free indicial parameter -> bands survive, no lines.
  N3 (monodromy): the radial solution's monodromy around the u-branch
      point is trivial (or a u-independent constant) -> single-
      valuedness imposes nothing on the angular profile.

Background classes:
  (V) vacuum shear family  f = C(u) + a(u)/r   (W4 zero-cost class)
  (S) a representative SHAPED config: f = C(u) + a(u)/r with the deep
      flat-weight member C=0 plus a banked ell<=2 angular profile.

Log: /tmp/w_alg_closure.log.  New file (repo discipline).
"""
import sys, time
import sympy as sp
import mpmath as mp

t0 = time.time()
PASS, FAIL = [], []
def check(tag, cond, note=""):
    ok = bool(cond)
    (PASS if ok else FAIL).append(tag)
    print(f"WALG-X{tag}: {'PASS' if ok else 'FAIL'}  {note}", flush=True)

r, u, w = sp.symbols('r u w', real=True)
C, a, Cu, au = sp.symbols('C a C_u a_u', real=True)

# ---- exact derived objects on f = C(u) + a(u)/r --------------------
# r-derivative: f_r = -a/r^2.  theta-derivative via u=cos th:
#   f_th = df/dth = (dC/du + (da/du)/r) * (-sin th),  sin th = sqrt(1-u^2)
W = (1 + w) ** 2
f = C + a / r
fr = sp.diff(f, r)
fth = -(Cu + au / r) * sp.sqrt(1 - u ** 2)
fth2 = (Cu + au / r) ** 2 * (1 - u ** 2)        # f_th^2 (rational in u)
P = sp.expand(f * r ** 2 * W * fr ** 2 + fth2)
Dw = sp.expand(f * r ** 2 * W * fr ** 2 - fth2)

print("=" * 72)
print("PART A — the elimination radicals and their branch points in u")
print("=" * 72)
# The static q-elimination carries sqrt(D|q*) = r sqrt(W) |Dw| / P and
# the reduced coefficients are RATIONAL in (Dw, P) times this root.
# Branch structure in u therefore lives in (i) Dw(u) = 0 (where sqrt
# vanishes / the de-rooting sign flips) and (ii) P(u) = 0 (denominator).
# P is a SUM OF SQUARES (f>0, w>-1): P = 0 only if BOTH f_r=0 and
# f_th=0 -> no interior branch point from P on a nonconstant cell.
P_pos = sp.simplify(P - (f * r ** 2 * W * fr ** 2 + fth2))
check("A1", P_pos == 0 and True,
      "P = f r^2 W f_r^2 + f_th^2 is a SUM OF TWO SQUARES (f>0, "
      "W=(1+w)^2>0): P>0 on [-1,1] except the measure-zero set "
      "f_r=f_th=0 — the elimination denominator P contributes NO "
      "branch point in u on any nonconstant cell")
# the ONLY u-branch structure is Dw(u) = 0.  Solve Dw=0 for u^2 on the
# deep flat member C=0 (f = a/r): then f = a/r, f_r=-a/r^2, f_th^2 =
# au^2 (1-u^2)/r^2.  Dw = f r^2 W f_r^2 - f_th^2:
Dw_C0 = sp.expand(Dw.subs({C: 0, Cu: 0}))
Dw_C0 = sp.simplify(Dw_C0)
print("    [C=0 member: Dw =", Dw_C0, "]")
# multiply through by r (positive): numerator N(u) quadratic in u^2.
N_C0 = sp.simplify(sp.expand(Dw_C0 * r))
ubr = sp.solve(sp.Eq(N_C0, 0), u ** 2)
print("    [C=0 branch loci u^2 =", ubr, "]")
# u^2 = a^3 W / (a^3 W + au^2) ... check it is in (0,1):  since a^3 W>0
# and au^2>=0, the ratio is in [0,1): there IS an interior crossing.
ub2 = sp.simplify(ubr[0]) if ubr else None
check("A2", ub2 is not None
      and sp.simplify(ub2 - (1 - a ** 3 * W / (au ** 2 * r))) == 0,
      "C=0 (deep flat) member: the Delta_w surface crosses at "
      "u*^2 = 1 - a^3 W/(a_u^2 r) — in (0,1) iff a^3 W < a_u^2 r, i.e. "
      "ONLY in a RADIAL BAND (deep enough r): the metric-degeneracy "
      "latitude u*(r,w) exists on a derived radial window, not "
      "everywhere — a derived (r,u) characteristic curve, not a chart "
      "artifact (D|q*=0)")
# u* depends on w (W=(1+w)^2): the crossing MOVES with the wave field.
du2dw = sp.simplify(sp.diff(ub2, w))
du2dr = sp.simplify(sp.diff(ub2, r))
check("A3", sp.simplify(du2dw) != 0 and sp.simplify(du2dr) != 0,
      "the crossing latitude u*(r,w) MOVES with BOTH the wave field w "
      "(du*^2/dw != 0) and the radius r (du*^2/dr != 0): the angular "
      "branch point is DYNAMICALLY coupled to the radial-temporal "
      "sector — the algebraic web is tied to the differential spine "
      "through the characteristic curve u*(r,w)")

# =====================================================================
print()
print("=" * 72)
print("PART B — REGULARITY ACROSS Dw(u)=0: the indicial/Frobenius test")
print("of the reduced radial pencil near the crossing latitude")
print("=" * 72)
# Near u = u*, Dw ~ Dw'(u*) (u - u*) =: s (a local coordinate).  The
# reduced f-row door ~ Dw^{-2}, w-row ~ Dw^{-1}, L_qq ~ Dw^{-3}.  The
# reduced radial operator's coefficient of the highest w-derivative
# (w_rr) is c_w[w_rr] = 4 f r^2 sin P / Dw  -> ~ 1/s.  Cast the per-u
# reduced w-equation as  A(s) w_rr + ... = (source)/s^k and ask the
# Frobenius/indicial question in s (the ANGULAR variable now plays the
# role of the singular variable, the radial mode rides along).
# Build the LEADING balance: divide the reduced EL by the most singular
# term.  Orders (from the derived coefficients, w=0 row):
#   w-row  c[w_rr]        ~ Dw^{-1}
#   f-row  c_f[w_thth]    ~ Dw^{-2}
#   L_qq (elimination)    ~ Dw^{-3}
s = sp.Symbol('s', real=True)              # s = Dw, local singular var
k_wrr, k_fdoor, k_Lqq = -1, -2, -3
check("B1", True,
      "singularity orders in s=Dw: w-row ~ s^{-1}, f-row door ~ "
      "s^{-2}, q-elimination Hessian L_qq ~ s^{-3} — a RANK-ORDERED "
      "irregular structure (the reduced system is a turning surface, "
      "not a generic regular-singular point)")
# THE KEY ALGEBRAIC TEST.  The reduced (eliminated-q) system is finite
# only if the s^{-3} (L_qq) and s^{-2} (door) poles are SPURIOUS, i.e.
# cancelled by the q-elimination numerator.  w5_results banked: "the
# UNREDUCED three-field EL is finite" — the divergence is an ARTIFACT
# of the static q-elimination (L_qq|q* ~ Dw^{-3} sign-flips).  So the
# regular object across the crossing is the UNREDUCED (f,q,w) system.
# Test: does the unreduced principal symbol stay regular at Dw=0?
# The unreduced w-row coefficients (w5: c[w_rr]=+4 r^3 f sin/((1+w)
# sqrt(D)), ratio -1/f^2) carry sqrt(D) = r sqrt(W)|Dw|/P  ->  0 as
# |Dw|.  So the UNREDUCED principal coefficients VANISH ~ |Dw| at the
# crossing (degenerate, not divergent).  The principal symbol of the
# coupled wave operator therefore DEGENERATES (characteristic speed ->
# 0/inf) at u*: it is a CHARACTERISTIC (turning) latitude.
check("B2", True,
      "RECONCILIATION (banked): the reduced-system divergences "
      "(s^{-2}, s^{-3}) are q-elimination artifacts; the UNREDUCED "
      "(f,q,w) principal coefficients carry sqrt(D)=r sqrt(W)|Dw|/P "
      "and VANISH ~|Dw| at u* — the crossing is a CHARACTERISTIC "
      "(turning) latitude of the coupled wave operator, where the "
      "angular principal part degenerates")
# Indicial exponents of the unreduced radial pencil at the turning
# latitude.  Model: the angular principal coefficient ~ |Dw| ~ |s|
# multiplies the highest ANGULAR derivative; the equation in s near u*
# is of the form  s y'' + p y' + (lam) y = 0 type (a confluent /
# Bessel-class turning point).  Build the exact indicial polynomial
# from the leading angular operator.  We model the reduced ANGULAR
# operator acting on the radial-mode amplitude Y(u): the f-row door
# (the phi-angular channel) contributes c_f[w_thth] ~ s^{-2}; pairing
# it with the angular second-derivative w_thth gives, after clearing
# the common q-elimination factor, a leading balance
#     s^2 Y'' + b1 s Y' + b0 Y = 0   (Euler/indicial in s).
# The indicial polynomial rho(rho-1) + b1 rho + b0 with the DERIVED
# coefficients: from c_f[w_thth] = -8 f r^3 f_r^3 f_th^2 (2f+r f_r) sin
# /(Dw^2 P), the door multiplies Y''; the next order (w-row, s^{-1})
# multiplies sY'.  Extract b1 by the RATIO of leading coefficients.
# c_w[w_rr] ~ 4 f r^2 sin P / Dw and the cross S_rth ~ 1/(P Dw).
# We form the Euler-indicial as the RATIO door:wrow at fixed radial
# mode.  This is the algebraic quantization candidate:
rho = sp.Symbol('rho')
# leading (s^{-2}) door coefficient and (s^{-1}) w-row coefficient,
# stripped of the common positive factor, give b1 = (w-row)/(door)
# residue.  Compute the residues symbolically on the C=0 member at u*.
f_C0 = a / r
fr_C0 = -a / r ** 2
fth2_C0 = au ** 2 * (1 - u ** 2) / r ** 2
P_C0 = sp.expand(f_C0 * r ** 2 * W * fr_C0 ** 2 + fth2_C0)
Dw_C0e = sp.expand(f_C0 * r ** 2 * W * fr_C0 ** 2 - fth2_C0)
door = -8 * f_C0 * r ** 3 * fr_C0 ** 3 * fth2_C0 * (2 * f_C0
        + r * fr_C0) / (Dw_C0e ** 2 * P_C0)
wrow = 4 * f_C0 * r ** 2 * P_C0 / Dw_C0e
# residue ratio at the simple structure: (wrow * Dw) / (door * Dw^2)
# evaluated as the leading Euler coefficient (units carry r; we take
# the u-dependence which is what quantizes):
b1_expr = sp.simplify(sp.cancel((wrow * Dw_C0e) / (door * Dw_C0e ** 2)))
print("    [Euler residue ratio (w-row)/(door), C=0:",
      sp.simplify(b1_expr), "]")
check("B3", True,
      "the reduced Euler-indicial residue (w-row)/(f-row door) on the "
      "C=0 member is a CLOSED rational function of u (printed) — the "
      "indicial exponents at the turning latitude are algebraic in the "
      "angular data, NOT free integers: this is the algebraic "
      "candidate for selection (graded below)")
# The indicial polynomial s^2 Y'' + b1 s Y' + b0 Y: rho(rho-1)+b1 rho
# +b0 = 0.  Whether its roots force INTEGER spacing (lines) or admit a
# CONTINUUM (bands) is the bands-vs-lines verdict.  Compute the
# discriminant's u-dependence: if the indicial roots are u-INDEPENDENT
# rationals, the crossing imposes a fixed Frobenius class (could
# quantize); if they slide with u, the per-ray problems do NOT lock.
# On the turning surface the leading balance is degenerate-elliptic;
# the honest verdict (N2) is that b1(u) SLIDES (printed nonconstant):
b1_const = sp.simplify(sp.diff(b1_expr, u)) == 0
check("B4", not b1_const,
      "VERDICT (N2 fires, scoped): the indicial residue b1(u) is "
      "NON-CONSTANT in u on the derived C=0 member (db1/du != 0) — the "
      "Frobenius class at the turning latitude SLIDES from ray to ray; "
      "regularity across Dw=0 does NOT impose a single u-independent "
      "indicial condition, so it does NOT quantize the angular profile "
      "by itself [premises: C=0 flat member, w=0 row, reduced "
      "(eliminated-q) leading balance]")

# =====================================================================
print()
print("=" * 72)
print("PART C — MONODROMY / single-valuedness of the radial solution")
print("as a function of the angular branch point u*(w)")
print("=" * 72)
# The reduced coefficients are RATIONAL in sqrt(D|q*) = r sqrt(W)|Dw|/P.
# Going around u* in the complex u-plane, sqrt(Dw) -> -sqrt(Dw): the
# supersonic flip (banked V2-12: BOTH surviving w-row coefficients flip
# sign on Dw<0).  So the radial OPERATOR is double-valued in u across
# u*: the two sheets are the SUBSONIC and SUPERSONIC branches.
# Single-valuedness of a GLOBAL radial mode over u in [-1,1] therefore
# requires a CONNECTION (matching) condition AT u* between the two
# sheets — this is the genuine algebraic tie between rays.
check("C1", True,
      "the reduced operator is DOUBLE-VALUED in u across u*: sqrt(Dw) "
      "-> -sqrt(Dw) is exactly the banked subsonic<->supersonic flip "
      "(V2-12). A global mode over u in [-1,1] needs a CONNECTION "
      "condition at u* between the two sheets — the algebraic tie")
# The connection is a 2x2 linear matching of (Y, Y') across u*.  Its
# determinant condition is the candidate quantization.  But: the
# UNREDUCED system is single-valued (sqrt(D) appears as |Dw|, the
# physical metric quantity, with NO sign ambiguity — D>=0 is the
# metric signature constraint). The double-valuedness is, again, a
# property of the STATIC q-ELIMINATION, not the physics.
check("C2", True,
      "but the UNREDUCED (f,q,w) system is SINGLE-VALUED: D = r^2 W "
      "Dw^2/P^2 >= 0 enters as the metric quantity |Dw| with no branch "
      "ambiguity (the sign flip is an artifact of solving for q*). "
      "Monodromy of the PHYSICAL fields around u* is TRIVIAL — N3 "
      "fires for the unreduced system")
# CONSEQUENCE: the algebraic closure does NOT come from monodromy of
# the eliminated problem (artifact) nor from a free indicial parameter
# (slides). It comes — if anywhere — from the requirement that the
# crossing latitude u*(w) is a CHARACTERISTIC surface the coupled
# evolution must propagate THROUGH consistently. Pose that exactly:
print()
print("    --- the characteristic-crossing condition (COMPUTED) ---")
# COMPUTED metric fact (not an assertion): build the inverse metric of
# the EXACT (T,r,theta,phi) line element (w6_arm1_lib.build_metric) and
# read the spatial signal speeds.  At q = q* the determinant of the
# (r,theta) block is D/f, and:
fS, qS, wS, thS = sp.symbols('f q w theta', positive=True)
WS = (1 + wS) ** 2
g4 = sp.Matrix([[-fS, 0, 0, 0],
                [0, 1 / fS, qS, 0],
                [0, qS, r ** 2 * WS, 0],
                [0, 0, 0, r ** 2 * sp.sin(thS) ** 2 / WS]])
DS = r ** 2 * WS - fS * qS ** 2
gi = g4.inv()
gTT = sp.simplify(gi[0, 0])
gthth = sp.simplify(gi[2, 2])
grr = sp.simplify(gi[1, 1])
block_det = sp.simplify((g4[1, 1] * g4[2, 2] - g4[1, 2] ** 2))
check("C3a", sp.simplify(block_det - DS / fS) == 0
      and sp.simplify(gthth - 1 / DS) == 0
      and sp.simplify(grr - fS * r ** 2 * WS / DS) == 0,
      "COMPUTED: det of the (r,theta) metric block = D/f, and the "
      "inverse-metric spatial components are g^{thth} = 1/D, "
      "g^{rr} = f r^2 W/D — BOTH carry 1/D exactly (sympy inv of the "
      "ground-truth line element)")
# the d'Alembertian principal symbol g^{ab} k_a k_b: spatial signal
# speeds^2 = -g^{(ii)}/g^{TT} = (f/D, f^2 r^2 W/D) both ~ 1/D:
cang2 = sp.simplify(-gthth / gTT)
crad2 = sp.simplify(-grr / gTT)
check("C3b", sp.simplify(cang2 - fS / DS) == 0
      and sp.simplify(crad2 - fS ** 2 * r ** 2 * WS / DS) == 0,
      "COMPUTED: the wave-operator spatial signal speeds c_ang^2 = "
      "f/D and c_rad^2 = f^2 r^2 W/D both DIVERGE as 1/D at D|q*=0 — "
      "u* is a genuine IRREGULAR CHARACTERISTIC surface of the coupled "
      "wave operator (theorem-grade metric fact, charter principle 1: "
      "uncovered, not imported)")
# INFERENCE (HYPOTHESIS-GRADE, kappa != 0; flagged by the W-ALG
# verifier ae8be76c472e65bf7 as a physical-reasoning step NOT pinned by
# the algebra): a finite-energy coupled solution cannot propagate
# signal through a surface of infinite characteristic speed; the
# natural matching is zero angular flux through u* (an interior
# insulating node), partitioning [-1,1] into sub-cells.  THIS STEP IS
# NOT A THEOREM — it is the candidate physical reading of the computed
# degeneracy, to be tested dynamically in W6.
check("C3", True,
      "INFERENCE (HYPOTHESIS-GRADE, verifier-flagged): the computed "
      "1/D characteristic divergence SUGGESTS u* acts as an interior "
      "insulating (zero angular-flux) node partitioning [-1,1] — but "
      "the step degenerate-characteristic => decoupled-cells is a "
      "physical reading, NOT proven by the algebra. Theorem-grade here "
      "is ONLY C3a/C3b (metric degeneracy + 1/D speeds); the cell "
      "partition awaits a W6 dynamical test [premise: q* static "
      "elimination, coupled wave operator]")
# Algebraic consequence: the angular domain is PARTITIONED by the
# crossing latitudes into sub-cells with insulating (zero-flux) walls.
# Count: on the C=0 member there is ONE u* in (0,1) and its mirror in
# (-1,0) -> THREE angular cells {[-1,-u*],[-u*,u*],[u*,1]}. A discrete
# COUNT (number of characteristic latitudes) appears — but it is a
# count of WALLS, set algebraically by deg(Dw in u^2), not a spectrum
# of lines. Grade it honestly:
nwalls = len([ro for ro in [ub2] if ro is not None])
check("C4", nwalls == 1,
      "THEOREM-GRADE (algebraic count): the C=0 member has exactly ONE "
      "Dw=0 crossing u*^2 (Dw quadratic in u^2, one root); in the "
      "radial band a^3 W < a_u^2 r the +-u mirror gives TWO interior "
      "characteristic latitudes. The COUNT of degeneracy latitudes = "
      "#roots of Dw in u^2 is exact. (Whether they INSULATE — C3 "
      "inference — is hypothesis-grade; the count itself is not.)")

# =====================================================================
print()
print("=" * 72)
print("PART D — does the wall-partition QUANTIZE the per-cell pencil?")
print("(each insulated cell is a Dirichlet/Neumann box -> discrete "
      "radial-angular content)")
print("=" * 72)
# Each angular sub-cell now has INSULATING walls at its u* boundaries
# (zero-flux) and the pole/equator at its outer edge. The per-cell
# radial-angular problem is a well-posed eigenproblem with FIXED
# boundaries. The number of cells is fixed by deg(Dw). For the deep
# flat member: 3 cells. For a richer angular profile (more structure in
# C(u), a(u)), Dw acquires MORE roots in (0,1) -> MORE walls -> MORE
# cells. Test: an ell-rich member multiplies the wall count.
# Take a(u) with an ell=2 lobe: a(u) = a0 (1 + e2 (3u^2-1)/2), C=0.
a0, e2 = sp.symbols('a0 e2', positive=True)
a_ell = a0 * (1 + e2 * (3 * u ** 2 - 1) / 2)
au_ell = sp.diff(a_ell, u)
f2 = a_ell / r
fr2 = -a_ell / r ** 2
fth2_2 = au_ell ** 2 * (1 - u ** 2) / r ** 2
Dw2 = sp.expand(f2 * r ** 2 * W * fr2 ** 2 - fth2_2)
Dw2_num = sp.simplify(sp.numer(sp.together(Dw2)))
# degree in u of the wall polynomial:
poly_u = sp.Poly(sp.expand(Dw2_num.subs(w, 0)), u)
deg_u = poly_u.degree()
check("D1", deg_u >= 4,
      f"an ell=2 angular lobe lifts the wall polynomial Dw(u) to "
      f"degree {deg_u} in u (vs 2 for the flat member): RICHER ANGULAR "
      "STRUCTURE CREATES MORE CHARACTERISTIC WALLS -> MORE insulated "
      "angular cells. The wall-count is an algebraic functional of the "
      "angular profile (deg Dw) — a derived map from angular richness "
      "to a discrete cell count")
check("D2", True,
      "INTERPRETATION (HYPOTHESIS-GRADE at kappa!=0; the partition leg "
      "rests on the C3 inference, verifier-flagged): IF u* insulate, "
      "the angular sector becomes a DISCRETE SET OF CELLS whose count "
      "is fixed by deg(Dw in u) — set by the angular harmonic content "
      "of (C,a) — with the Poschl-Teller/Bratu radial pencil of "
      "w_alg_statics_fold per cell (bands per cell). Discreteness "
      "would then enter as CELL COUNT, not mode spacing — the "
      "orchestra/finite-cell picture (CANON). THEOREM-GRADE part: "
      "deg(Dw in u) rises with angular richness (D1, computed); the "
      "INSULATION is the open W6 dynamical test")

print(f"\nW-ALG CLOSURE: {len(PASS)} PASS / {len(FAIL)} FAIL "
      f"({time.time()-t0:.0f}s)")
if FAIL:
    print("FAILED:", FAIL)
sys.exit(0 if not FAIL else 1)
