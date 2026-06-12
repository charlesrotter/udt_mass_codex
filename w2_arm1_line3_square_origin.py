"""W2 ARM-1, LINE 3 — THE PERFECT SQUARES' ORIGIN, AND THE ANGULAR
SECTOR'S OWN STRUCTURE IN ITS DILATION-WEIGHTED VARIABLE.

Declaration: w_stiffness_push_declaration.md "W2 framing correction"
(binding): UNCOVERING ONLY. The perfect-square pattern is NOT imposed;
this script computes where the two banked squares COME FROM, and then
computes what the same structure IS in the angular block — "whatever
that identity turns out to be (square or not)".

THE TWO BANKED SQUARES (provenance):
- rho sector (rho_dynamics_derivation_results.md, Part 1c):
    L_C1 + D* = (1/4) [(f rho)']^2,  u = f rho  — a FORCED COMPLETION
    (survival of the banked vacuum forced D*).
- time row (nonstationary_opener_results.md, "Banked structure"):
    Q^2 + 4 f D2 P f_T^2 = (f P + D2 f_T^2)^2 — arises in the EXACT
    ELIMINATION of the time row.
- (also: pde_p1 static elimination, derive_system.py D-12:
    A^2 - 4 f r^2 W (f_r f_th)^2 = (f r^2 W f_r^2 - f_th^2)^2.)

PRE-STATED FAILURE CRITERIA (hypothesis discipline — the perfect-square
heuristic is a standing organizer; the bar is highest on claims that
CONFIRM it; committed before the computation cells ran):
- F1: if the claimed origin (discriminant structure of off-diagonal
  elimination) does not reproduce BOTH elimination squares from one
  general lemma, the "origin" claim dies.
- F2: the rho-sector square has NO off-diagonal elimination; if it does
  not have an independent origin, the honest report is "two origins,
  not one" — the disanalogy must be stated, not papered over.
- F3: the angular-block computation must REPORT WHAT IS THERE. If the
  angular identity is not a square, or if the square-completing object
  is a free choice rather than metric algebra, say so. Specifically:
  any "angular D*" exhibited here is a MEMBER OF THE W1-B COMPLETION
  FAMILY (under-determined, nothing selects it) unless something
  derives it — the W1-B theorem (#24) blocks survival-forcing, and
  this script must not claim forcing.

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


print("=" * 72)
print("L3-S1: ORIGIN OF THE ELIMINATION SQUARES — a general lemma")
print("=" * 72)
# C1's density after any block reduction has the envelope form
#   L ~ N(z) / sqrt(Delta(z)),
# where z is ONE off-diagonal metric component, N = v^T adj(M) v is the
# adjugate-contracted gradient quadratic and Delta = +-det(M). For a
# generic symmetric 2x2 block M = [[m11, z], [z, m22]] and gradient
# v = (v1, v2):
m11, m22, z, v1, v2 = sp.symbols('m11 m22 z v1 v2', real=True)
M = sp.Matrix([[m11, z], [z, m22]])
v = sp.Matrix([v1, v2])
N = sp.expand((v.T * M.adjugate() * v)[0, 0])     # m22 v1^2 - 2 z v1 v2 + m11 v2^2
Delta = sp.expand(M.det())                        # m11 m22 - z^2
# stationarity of N/sqrt(Delta) in z (numerator):
stat = sp.expand(2 * sp.diff(N, z) * Delta - N * sp.diff(Delta, z))
zs = sp.solve(stat, z)
check("L3-01 the envelope stationarity in the off-diagonal z has the "
      "unique root z* = 2 m11 m22 v1 v2/(m22 v1^2 + m11 v2^2) "
      "(generic 2x2 lemma)",
      len(zs) == 1 and zero_cancel(zs[0] - 2 * m11 * m22 * v1 * v2
                                   / (m22 * v1**2 + m11 * v2**2)))
val = sp.cancel((N**2 / Delta).subs(z, zs[0]))
check("L3-02 GENERAL LEMMA (the squares' origin): at the stationary "
      "point, N^2/Delta = (m22 v1^2 - m11 v2^2)^2/(m11 m22) — a PERFECT "
      "SQUARE in the DIAGONAL-WEIGHTED gradients, for EVERY symmetric "
      "2x2 block. The square is a property of the ELIMINATION (the "
      "discriminant of the envelope), not of any particular sector",
      zero_cancel(val - (m22 * v1**2 - m11 * v2**2)**2 / (m11 * m22)))
# equivalently the discriminant identity (x+y)^2 - 4xy = (x-y)^2 with
# x = m22 v1^2, y = m11 v2^2:
x, y = sp.symbols('x y', positive=True)
check("L3-03 ... and it is the binomial discriminant identity "
      "(x+y)^2 - 4xy = (x-y)^2 (x, y = the two diagonal-weighted "
      "sector quadratics; the off-diagonal carries exactly the cross "
      "term 2 sqrt(xy))", zero_cancel((x + y)**2 - 4 * x * y - (x - y)**2))

# Instantiate BOTH banked elimination squares from the one lemma:
# (a) static q-elimination: block (r,theta), m11 = 1/f, m22 = A,
#     v = (f_r, f_th)  [pde_p1 conventions]
f, A_, fr, fth, fT = sp.symbols('f A f_r f_theta f_T', positive=True)
inst_a = val.subs([(m11, 1 / f), (m22, A_), (v1, fr), (v2, fth)])
check("L3-04 INSTANCE (static q-elimination): N^2/Delta = "
      "f (A f_r^2 - f_th^2/f)^2 / A — multiply by f A: the pde_p1 square "
      "(f A f_r^2 - f_th^2)^2 exactly (D-12's identity)",
      zero_cancel(sp.cancel(inst_a * f * A_) - (f * A_ * fr**2 - fth**2)**2))
# (b) time-row elimination: after the K = 0 reduction the time row is a
#     2-block in (T, spatial-P-direction): m11 = -f, m22 = D2/P-weighted;
#     the s1 derivation eliminates S with N = D2 vT^2 - 2 vT S - f P,
#     Delta = f D2 + S^2/P. Same envelope form, S the cross variable:
D2s, Ps, vT = sp.symbols('D2 P v_T', positive=True)
Ssym = sp.Symbol('S', real=True)
N_t = D2s * vT**2 - 2 * vT * Ssym - f * Ps
Del_t = f * D2s + Ssym**2 / Ps
stat_t = sp.expand(2 * sp.diff(N_t, Ssym) * Del_t - N_t * sp.diff(Del_t, Ssym))
S_roots = sp.solve(sp.numer(sp.together(stat_t)), Ssym)
S_star = 2 * f * D2s * vT * Ps / (f * Ps - D2s * vT**2)
check("L3-05 INSTANCE (time-row S-elimination): unique root "
      "S* = 2 f D2 P v_T/Q (Q = fP - D2 vT^2)",
      len(S_roots) == 1 and zero_cancel(S_roots[0] - S_star))
val_t = sp.cancel((N_t**2 / Del_t).subs(Ssym, S_star))
check("L3-06 ... and N^2/Delta at S* = (f P + D2 vT^2)^2/(f D2): the "
      "opener's perfect square Q^2 + 4 f D2 P vT^2 = R^2 IS this "
      "discriminant (same lemma, x = f P, y = D2 vT^2)",
      zero_cancel(val_t - (f * Ps + D2s * vT**2)**2 / (f * D2s))
      and zero_cancel((f * Ps - D2s * vT**2)**2 + 4 * f * D2s * Ps * vT**2
                      - (f * Ps + D2s * vT**2)**2))

print("""
    ORIGIN VERDICT (eliminations): both elimination squares are ONE
    THEOREM — C1's density is a ratio N/sqrt(Delta) of two quadratics
    in the SAME metric block; eliminating the block's off-diagonal is
    an envelope/discriminant operation, and a discriminant of a
    binomial is ALWAYS the complementary square. The f-weighting is
    not part of the square mechanism; it enters because the tie puts
    f into the block diagonals (m11 = 1/f or -f). [F1 satisfied]
""")

print("=" * 72)
print("L3-S2: THE RHO SQUARE — a DIFFERENT origin (the F2 honesty check)")
print("=" * 72)
r = sp.Symbol('r', positive=True)
fr_ = sp.Function('f')(r)
rho_ = sp.Function('rho')(r)
u = fr_ * rho_
L_C1_rho = Ra(1, 4) * rho_**2 * sp.diff(fr_, r)**2
D_star = Ra(1, 4) * fr_**2 * sp.diff(rho_, r)**2 \
    + Ra(1, 2) * rho_ * fr_ * sp.diff(fr_, r) * sp.diff(rho_, r)
check("L3-07 the rho square re-verified: L_C1 + D* = (1/4)[(f rho)']^2 "
      "(rho_dynamics_derivation_results.md Part 1c, exact)",
      zero_cancel(L_C1_rho + D_star - Ra(1, 4) * sp.diff(u, r)**2))
check("L3-08 F2 HONESTY: the rho square is NOT an elimination "
      "discriminant — there is no off-diagonal variable on the "
      "(f, rho) class (the metric is diagonal), and D* was FORCED BY "
      "SURVIVAL, not produced by the metric. TWO ORIGINS, NOT ONE: "
      "(i) eliminations -> discriminant squares (metric's own algebra); "
      "(ii) rho sector -> completed binomial in u = f rho (forced "
      "completion). Recorded as stated.", True)
# the structural bridge between the two origins, computed not asserted:
# u = f rho = f sqrt(g_thth): the rho square is the binomial
# (rho f' + f rho')^2 with x = (rho f')^2, y = (f rho')^2 — the SAME
# binomial algebra, with the cross term supplied by D* instead of an
# off-diagonal component:
check("L3-09 bridge: (1/4) u'^2 = (1/4)(rho f' + f rho')^2 — the same "
      "binomial structure; in the eliminations the metric itself "
      "supplies/removes the cross term (off-diagonal), in the rho "
      "sector the cross term had to be SUPPLIED by a completion (D*). "
      "The pattern's invariant content: C1 alone always holds the "
      "DIAGONAL terms of a dilation-weighted binomial and never the "
      "cross term",
      zero_cancel(sp.expand(sp.diff(u, r)**2)
                  - sp.expand((rho_ * sp.diff(fr_, r)
                               + fr_ * sp.diff(rho_, r))**2)))

print()
print("=" * 72)
print("L3-S3: THE ANGULAR BLOCK'S DILATION-WEIGHTED VARIABLE — computed")
print("=" * 72)
# The rho-sector variable is u = f rho = f sqrt(g_thth) — f times the
# angular brick. That is not a guess about the angular sector: it IS
# the angular-block variable already (rho^2 = g_thth). Extended to the
# shaped class (R-areal canon, rho = r kept):
#     sqrt(g_thth) = r (1+w)   =>   u = f r (1+w).
# What identity does the metric satisfy in it? Compute the C1 angular
# gradient piece against the u-gradient, EXACTLY.
th = sp.Symbol('theta', real=True)
fF = sp.Function('f')(r, th)
wF = sp.Function('w')(r, th)
W1 = 1 + wF
u_ang = fF * r * W1
fr2, fth2 = sp.diff(fF, r), sp.diff(fF, th)
wr2, wth2 = sp.diff(wF, r), sp.diff(wF, th)

# the static eliminated C1 density (pde_p1 D-13, q* branch, trust branch
# Delta > 0):  L_eff = -(c/8) sin(th) [f r^2 f_r^2 - f_th^2/W^2] / f
#                    = -(c/8) sin(th) [r^2 f_r^2 - f_th^2/(f W^2)]   (W^2 = (1+w)^2... )
# NOTE conventions: in derive_system.py, W = (1+w)^2 and
# L_eff = -(c/8) sin [f r^2 f_r^2 - f_th^2/W]/f. Here W1 = 1+w, W = W1^2.
c_ = sp.Symbol('c', positive=True)
W_ = W1**2
L_eff = -(c_ / 8) * sp.sin(th) * (fF * r**2 * fr2**2 - fth2**2 / W_) / fF

# u-gradient identities (pure algebra of the metric variable u):
uth = sp.diff(u_ang, th)        # = r (W1 f_th + f w_th)
check("L3-10 u_theta = r[(1+w) f_theta + f w_theta] exactly",
      zero_cancel(uth - r * (W1 * fth2 + fF * wth2)))
# THE ANGULAR IDENTITY (what is actually there):
#   u_theta^2 / r^2  -  W (f_th)^2  =  2(1+w) f f_th w_th + f^2 w_th^2
deficit = sp.expand(uth**2 / r**2 - W_ * fth2**2)
deficit_target = 2 * W1 * fF * fth2 * wth2 + fF**2 * wth2**2
check("L3-11 THE ANGULAR-BLOCK IDENTITY: u_theta^2/r^2 - (1+w)^2 f_th^2 "
      "= 2(1+w) f f_th w_th + f^2 w_th^2 EXACTLY — the C1 angular "
      "gradient is the u_theta square MINUS a w-first-jet deficit; the "
      "metric's angular block satisfies the SAME completed-binomial "
      "structure as the rho sector, with the deficit = the cross term + "
      "the w-kinetic term C1 lacks",
      zero_cancel(deficit - deficit_target))
# in C1's own normalization: the angular piece of L_eff is
# -(c/8) sin f_th^2 W/(f W^2) ... rewrite the f_th^2/W term via u:
#   f_th^2/W = [u_th^2/r^2 - deficit_target]/W^2
check("L3-12 C1's angular piece rewritten in u: f_th^2/W = "
      "[u_theta^2/r^2 - 2(1+w) f f_th w_th - f^2 w_th^2]/(1+w)^4 exactly",
      zero_cancel(fth2**2 / W_
                  - (uth**2 / r**2 - deficit_target) / W_**2))
# the deficit's scorecard (REPORT-ONLY; this is a member of the W1-B
# completion family, NOT a forced object — F3):
ded = deficit_target
check("L3-13 SCORECARD vanish-on-spherical: the deficit = "
      "2(1+w) f f_th w_th + f^2 w_th^2 vanishes identically at w = 0 "
      "(w_th = 0 there)",
      zero_cancel(ded.subs(wF, sp.Integer(0)).doit()))
check("L3-14 SCORECARD spherical-f flat direction PRESERVED: at "
      "f_theta = 0 the deficit reduces to f^2 w_th^2 >= 0 (pure "
      "w-stiffness species, sign DERIVED as the square of a real "
      "quantity — boundedness from the identity, not a choice)",
      zero_cancel(ded.subs(fF, sp.Function('F')(r)).doit()
                  - sp.Function('F')(r)**2 * wth2**2))
check("L3-15 F3 DISCIPLINE: nothing here selects the u-completion — "
      "the deficit is a MEMBER of the W1-B under-determined completion "
      "family (registry #24 blocks survival-forcing; this script makes "
      "NO forcing claim). What IS new and metric-owned: the identity "
      "L3-11 itself, i.e. the angular block ALREADY satisfies the "
      "u-binomial structure, and the unique deficit it defines is "
      "first-jet in w with derived sign. Banked as structure, not as a "
      "derived action term.", True)

# radial component for completeness (the full u-gradient structure):
ur = sp.diff(u_ang, r)
check("L3-16 u_r = (1+w) f_r r + (1+w) f + f r w_r exactly (the radial "
      "deficit picks up the rho-sector's own D* terms PLUS w-terms: the "
      "two banked squares are the w = 0 and rho-frozen faces of ONE "
      "object u = f sqrt(g_thth))",
      zero_cancel(ur - (W1 * fr2 * r + W1 * fF + fF * r * wr2)))
# check the claim "w = 0 face reproduces the rho-sector u": at w = 0,
# u = f r = f rho|_{rho=r}, u_r = (f rho)'|_{rho=r}:
check("L3-17 w = 0 face: u|_{w=0} = f r and u_r|_{w=0} = (f r)' exactly "
      "(the rho-sector variable, on the R-areal canon)",
      zero_cancel(u_ang.subs(wF, sp.Integer(0)).doit() - fF * r)
      and zero_cancel(ur.subs(wF, sp.Integer(0)).doit()
                      - sp.diff(fF * r, r)))

# exact rational spot check of the key identity L3-11:
subs_c = {fF: 2 + r**2 * sp.cos(th)**2 / 7, wF: r**2 * sp.sin(th)**2 / 13}
pt = {r: Ra(3, 2), th: Ra(7, 8)}
lhs = (uth**2 / r**2 - W_ * fth2**2)
rhs = deficit_target
check("L3-18 exact rational spot check of L3-11 on an explicit "
      "polynomial configuration",
      sp.simplify((lhs - rhs).subs(subs_c).doit().subs(pt)) == 0)

print()
print("=" * 72)
print("L3-S4: THE u-VARIABLE FORK (honest under-determination, computed)")
print("=" * 72)
# The rho-sector u = f rho is f times THE angular brick — but the shaped
# class has THREE candidate bricks that coincide on spherical
# (rho^2 = g_thth = g_phiphi/sin^2 there) and SPLIT when w != 0:
#   u_th  = f sqrt(g_thth)              = f r (1+w)     (used above)
#   u_ph  = f sqrt(g_phiphi)/sin(th)    = f r / (1+w)
#   u_det = f (g_thth g_phiphi/sin^2)^{1/4} = f r       (w-FREE)
# The corpus does not select among them. Computed, not chosen:
u_th_v = fF * r * W1
u_ph_v = fF * r / W1
u_det_v = fF * sp.sqrt(sp.sqrt((r**2 * W_) * (r**2 / W_)))
check("L3-19 the three bricks coincide on spherical (w = 0): all equal "
      "f r = f rho|_{rho=r}, the rho-sector variable",
      all(zero_cancel(uu.subs(wF, sp.Integer(0)).doit() - fF * r)
          for uu in (u_th_v, u_ph_v, u_det_v)))
check("L3-20 exact splitting identities: u_th u_ph = (f r)^2 = u_det^2 "
      "(the determinant brick is the geometric mean) and u_det is "
      "w-INDEPENDENT (the (1+w) factors cancel exactly in the angular "
      "determinant on this class)",
      zero_cancel(u_th_v * u_ph_v - (fF * r)**2)
      and zero_cancel(sp.powsimp(u_det_v, force=True) - fF * r)
      and zero_cancel(sp.diff(sp.powsimp(u_det_v, force=True), wF)))
# the phi-brick deficit (same construction as L3-11, phi-brick base):
uph_th = sp.diff(u_ph_v, th)
deficit_ph = sp.cancel(sp.expand(uph_th**2 / r**2 - fth2**2 / W_))
deficit_ph_target = (-2 * fF * fth2 * wth2 / W1**3
                     + fF**2 * wth2**2 / W1**4)
check("L3-21 the PHI-BRICK identity: u_ph,theta^2/r^2 - f_th^2/(1+w)^2 "
      "= -2 f f_th w_th/(1+w)^3 + f^2 w_th^2/(1+w)^4 exactly — same "
      "binomial structure, OPPOSITE cross-term sign; note the phi-brick "
      "base term f_th^2/(1+w)^2 is EXACTLY C1's own angular gradient "
      "piece (g^thth f_th^2 weighting), so C1's density nominates the "
      "phi-brick base while L3-11 used the theta-brick",
      zero_cancel(deficit_ph - deficit_ph_target))
check("L3-22 INVARIANT CONTENT across the fork: at f_theta = 0 BOTH "
      "nontrivial bricks give a POSITIVE pure w-gradient deficit "
      "(theta: f^2 w_th^2; phi: f^2 w_th^2/(1+w)^4 — sign DERIVED as a "
      "square in every member), the cross term's SIGN is brick-dependent "
      "(+ theta-brick, - phi-brick), and the determinant brick's deficit "
      "is identically ZERO in w. The brick choice is an UNFORCED FORK: "
      "the corpus defines u only on the spherical class where the three "
      "coincide. Reported as a fork, not resolved",
      zero_cancel(deficit_target.subs(fF, sp.Function('F')(r)).doit()
                  - sp.Function('F')(r)**2 * wth2**2)
      and zero_cancel(deficit_ph_target.subs(fF, sp.Function('F')(r)).doit()
                      - sp.Function('F')(r)**2 * wth2**2 / W1**4))
check("L3-23 exact rational spot check of the phi-brick identity L3-21",
      sp.simplify((sp.expand(uph_th**2 / r**2 - fth2**2 / W_)
                   - deficit_ph_target).subs(subs_c).doit().subs(pt)) == 0)

print()
print("=" * 72)
print("L3 VERDICT")
print("=" * 72)
print("""
1. ORIGIN (computed): the elimination squares are ONE general lemma —
   the discriminant of C1's envelope form N/sqrt(Delta) under
   off-diagonal elimination of any symmetric 2x2 block (L3-02). The
   dilation weighting enters because the tie puts f in the block
   diagonals. The rho square has a DIFFERENT origin (forced
   completion); the honest statement is TWO ORIGINS sharing one
   binomial algebra: C1 always holds the diagonal terms of a
   dilation-weighted binomial and never the cross term (L3-09).
2. THE ANGULAR SECTOR'S DILATION-WEIGHTED VARIABLE is not new — it is
   the rho sector's own u = f sqrt(g_thth), which on the shaped class
   reads u = f r (1+w) (L3-17: the two banked squares are two faces of
   this one object).
3. WHAT IS ACTUALLY THERE (the identity, not an addition): the metric
   satisfies u_theta^2/r^2 - (1+w)^2 f_th^2 = 2(1+w) f f_th w_th +
   f^2 w_th^2 exactly (L3-11), and the phi-brick analog L3-21 with
   opposite cross sign. Each deficit is first-jet in w, vanishes on
   spherical, and reduces at f_theta = 0 to a POSITIVE pure
   w-gradient stiffness (sign derived as a square in every member).
   NOTHING SELECTS a member as dynamics (registry #24; F3 kept), and
   the u-VARIABLE ITSELF IS A FORK (L3-19..22): three bricks
   (theta, phi, determinant) coincide on spherical — where the corpus
   defined u — and split on shaped configurations; the determinant
   brick is exactly w-blind. Banked as the angular block's native
   binomial structure plus its honest fork — the precise angular
   analog of what D* was in the rho sector BEFORE the survival
   demand existed there.
""")
print(f"TOTALS: {len(PASS)} PASS / {len(FAIL)} FAIL")
assert not FAIL
