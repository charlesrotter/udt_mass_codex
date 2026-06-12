# W5 ARM-1 (UNCOVER) — Results: the -2/f Origin, the Full Species EL
# Map, the f = 2 kappa Locus, and the q*-Branch Adjudication

Date: 2026-06-12. Agent: W5 ARM-1 (uncover arm). Declaration: W5
section of w_stiffness_push_declaration.md (binding).
STATUS: **ARM REPORT — UNVERIFIED.** Verifier-before-record applies:
nothing below is banked until a blind adversarial verifier pass is
recorded here with agent id and date. Registry edits (#28
CONDITIONS-CHANGED) are deferred to post-verification.

Scripts (new, committed, assert-laden, all run to completion):
- `w5_arm1_relation_origin.py` — 17/17 PASS (23 s)
- `w5_arm1_qon_angular.py` — 18/18 PASS (90 s)
- `w5_arm1_locus_pencil.py` — 12/12 PASS (19 s)
Total 47 checks. METHOD NOTE (on record): exploratory dev passes in
/tmp (w5_explore*.py, w5_dev_*.py; not committed) computed the exact
forms first; every assert target in the committed scripts is a
COMPUTED value from those passes, none is a retrofitted hope. The
pre-stated failure criteria (F1-F4, G1-G3, H1-H3 in the script
headers) were stated in the session record before the dev passes ran.
Two of my own guessed targets died on computation and were corrected
to the computed truth before commit (S1-16 sign of the w_T^2 stress
term; the whole drafted "elliptic angular stiffness" block of the
first S2 draft — see (iv)). Backgrounds: /tmp/w4b_bg.npz (the W4-B
regeneration, verified bit-identical against the banked library;
re-anchored here in S3-05).

## (i) THE -2/f ORIGIN (script 1)

**Third-route verification (F1 bar passed).** EL_w[L_GG] =
EL_w[W_wave] - (2/f) dL_C1/dw holds IDENTICALLY (full symbolic
cancellation) on the full q=0 time-on class, where L_GG is the
Gamma-Gamma bulk of sqrt(-g)R and EL_w[div V] == 0 under the full
second-order EL operator (exact rational points, hostile w<0). This
route (split + first-order bulk EL) is neither of VA4's two (Einstein
tensor; euler_equations on the full density). The relation now stands
on three independent routes.

**Slot localization (F2 bar passed).** The species' algebraic
w-content lives ENTIRELY in the f_th^2 slot of the bulk: d/dw of
every other slot (f_T^2, f_r^2, all crosses, all linears, jet-free)
vanishes identically.

**The weight-stripping identity (exact, all w).**
  LGG_alg(w) - LGG_alg(0) = -(2/f) [L_C1_ang(w) - L_C1_ang(0)]
i.e. the species' algebraic w-channel IS C1's angular density with
the postulate weight e^{-2phi} stripped and replaced by the curvature
scalar's native weight -2 e^{0}; the slot equals
-2 sqrt(-g) g^{thth} phi_th^2 exactly. **-2/f = -2 e^{2phi} is a
WEIGHT MISMATCH**: C1 carries the postulate's e^{-2phi}, the
curvature's own clock-gradient quadratic carries weight 1.

**Tie deformation (the origin's provenance).** On g_TT = -f^a,
g_rr = f^b (postulate point (1,-1)), the algebraic w-EL is
  [f_th^2 slot]  sin(th) f^{(a+b)/2 - 2} P(a,b) / (1+w)^3,
      P(a,b) = a^2/2 - a + b^2/2 - b  =  [(a-1)^2 + (b-1)^2]/2 - 1
  [f_thth slot]  (a+b) f^{(a+b)/2 - 1} sin(th)/(1+w)^3
with P(1,-1) = 1 (the species tadpole) and ALL other slots zero at
the postulate point. Readings, as computed:
- On the **unimodular line a + b = 0** (g_TT g_rr = -1 — the
  postulate's static T-r pairing) the f_thth contamination vanishes
  IDENTICALLY and P(a,-a) = a^2: pure clock-tie scaling, exactly the
  universal -2 (grad Phi)^2 content of R with Phi = (a/2) ln f. The
  tadpole's slot-purity and its a^2 law are STRUCTURAL consequences
  of the dilation tie's unimodular pairing.
- The specific normalization "-2" is the static-slicing (grad Phi)^2
  coefficient of the scalar curvature — R-specific. **So: the
  EXISTENCE, slot, weight, and scaling of the species' algebraic
  w-force follow from the dilation postulate's structure; only its
  absolute normalization (-2, i.e. the ratio's "2") is EH-specific.**
  The guardrail question is correspondingly sharpened, not settled:
  any curvature-grade scalar built on the tie carries this channel;
  R fixes its size. (F3 honored: scoped to the power-law tie family
  probed.)
- Zero set of P: the circle (a-1)^2 + (b-1)^2 = 2, through (0,0),
  (2,0), (0,2), (2,2) — tadpole-free tie deformations exist but the
  postulate point is not on them. (Verifier attack target V-2.)

## (ii) THE FULL SPECIES EL MAP ON P1 (q=0; scripts 1, 2)

Channels of Delta_w := the species' w-content (EL-equivalent
representative: the bulk's w-content; div V is EL-invisible in every
channel):
- **E_w**: EL_w[W_wave] - (2/f) dL_C1/dw (the known relation).
- **E_f** (script 1, full time-on class): vanishes IDENTICALLY at
  w == 0 (macro gate at fluctuation orders 0 and 1, F4 passed); at
  linearized order it feeds the f-equation NO w second jets (w_TT,
  w_rr, w_thth, all crosses = 0 at w=0); its O(w) source is
  2[f_th^2 sin - f f_th cos - f f_thth sin]/f^3 * w
  - (2 f_th sin/f^2) * w_th — shaped-only (vanishes when
  f_th = f_thth = 0). On spherical f the full-w content is EXACTLY
  dL_Wwave/df = -2 r^2 sin [w_r^2 + w_T^2/f^2]/(1+w)^2: the
  untruncated species adds NO new spherical-f source beyond the
  W4-known wave stress.
- **E_q at q = 0** (script 2): NONZERO on shaped w-on configurations:
  principal piece -2 f sin(th) w_rth/(1+w)^3, every term carrying
  w_r, w_rth or f_rth; vanishes at w == 0 (the macro gate extends to
  the q-channel). At O(kappa) the species SHIFTS the q*-branch.

## (iii) THE f = 2 kappa LOCUS AND THE UNTRUNCATED PENCIL (script 3)

**Exact structure.** With S = C1 + beta D_cell + kappa Delta_w at
q=0: the w-equation's algebraic sector is
(1 - 2 kappa/f) dL_C1ang/dw + beta (1/2) sin f_th^2/f; at w = 0 it is
(1/2)(sin f_th^2/f)(beta - 1 + 2 kappa/f). OFF-branch: zero exactly
on f = 2 kappa, force flips across. ON-branch: residual
kappa sin f_th^2/f^2 != 0 — **the W4-P1 ON-branch property "banked
cells are exact full-system statics at every kappa" is DESTROYED by
the untruncated species** (it was a property of the truncation;
w = 0 is off-shell on BOTH branches at kappa != 0). The w-Hessian
carries the same factor: (3/2)(sin f_th^2/f)(1 - 2 kappa/f),
beta-blind.

**The geometry correction (the declaration's premise refuted as
worded).** On the banked M1/M2/M4 cells the locus is NOT "an interior
surface crossing every cell": f = 1 at the weld and GROWS inward on
most rays (f_max 6.8-33); f < 1 only in the seal funnel. Even at
2 kappa = 0.5 only 0.4-1.9% of rays cross; the locus is a narrow
SEAL-FUNNEL CAP in the last ~1-2% of t before t_stop. Ordering,
every resolvable ray, every member, every 2 kappa in
{0.5...0.004}: **t_turn(Delta_w) < t_loc < t_stop**, and the whole
structure lies beyond the 1% trust window (t_turn_min > t1pc on all
members): every locus statement is seal-layer territory (registry-#1
species). [M2 turning anchor 1.2551 reproduced < 5e-3.]

**The untruncated pencil (exact decomposition).**
  -(e^{-t} fbar psi')' - (3/(8k)) e^{-t} s fbar_u^2 (1 - 2k/fbar)
      /fbar psi = omega^2 e^{-3t} psi/fbar
  ==  [the W4/VA4 pencil]  +  the kappa-INDEPENDENT positive
      potential (3/4) e^{-t} s fbar_u^2/fbar^2.
Corollary (V2 >= 0): kappa_c can only SHRINK. Computed (VA4 anchors
0.01160/0.00789/0.00829 reproduced < 2e-4 first; grid-converged):
- trust windows (t1pc): kappa_c^new/kappa_c^old = 0.990 / 0.991 /
  0.991 (M1/M2/M4) — a ~1% effect;
- full domain (seal-dominated, labeled): 0.783 / 0.841 / 0.844.
**No mode trapping at the locus**: the lowest mode carries < 1e-6 of
its mass in the f < 2 kappa cap (old and new pencils, kappa = 0.3
and 0.1, M1 full domain, most-unstable node — whose ray never even
reaches f = 2 kappa: the instability does not live where the locus
is). The added potential is algebraic in w — per-u decoupling
persists at q = 0, so the locus CANNOT produce angular quantization.
**Verdict: the locus is a force/selection structure in the seal
funnel, not a spectral trap; the hoped-for trapping/quantization
mechanism is DEAD at this level** [premises: frozen-f pencil, q = 0,
w = 0 background (off-shell, see above), Dirichlet inner, banked
library]. Its surviving roles: (1) the OFF-branch static force flip
inside the cap (Arm-2 statics territory); (2) the uniform stabilizing
V2 shift (band shrink, computed above).

## (iv) THE q*-BRANCH ADJUDICATION (script 2 — the deliverable)

**The inventory (the central uncovering).** On the static q-on class,
across ALL THREE EL channels, the only nonzero (w,q)-second-jet
coefficients are (D := r^2 W - f q^2 > 0):
  E_w: c[w_rr]  =  4 f r^3 sin/((1+w) sqrt(D))
  E_w: c[q_rth] = E_q: c[w_rth] = -2 f r sin/((1+w)^2 sqrt(D))
  E_f: c[w_rth] = -2 q r sin/((1+w)^2 sqrt(D))
  E_f: c[q_rth] = +r sin/((1+w) sqrt(D))
In particular **c[w_thth] = 0 IDENTICALLY AT ALL q IN ALL THREE
CHANNELS**. On the full TIME-ON q-on class: c[w_TT] = -4 r^3 sin/
((1+w) f sqrt(D)), c[w_rr] = +4 r^3 f sin/((1+w) sqrt(D)) — **the
wave cone dr/dT = +-f is q-INVARIANT (ratio -1/f^2 at all q)** — and
c[w_Tr] = c[w_Tth] = c[w_rth] = c[w_thth] = 0 at all q: the
EL-level fiber cancellation is TOTAL; angular structure enters only
through the q-jet couplings c[q_TT] = +2 r q sin/((1+w)^2 sqrt(D))
and c[q_rth] = -2 r f sin/((1+w)^2 sqrt(D)).

**The w_thth theorem on the branch (G2 realized).** The reduced
branch w-EL of S = C1 + kappa Delta_w on the C1-q* branch at
O(kappa) has w_thth coefficient ZERO IDENTICALLY (every carrier
vanishes: the inventory zeros + the chain carriers + quasi-linearity,
each asserted separately). **The q*-branch supplies NO pure angular
w-stiffness at any q. Bands cannot become lines through an angular
SL well at this order.** [Premises: static P1 q-on class, C1-q*
branch, O(kappa), EL level.]

**What IS there (exact).** The reduced branch w-EL carries exactly
one angular-derivative term, the MIXED coupling S_rth * w_rth, with
(at w = 0, subsonic Delta_w = f r^2 f_r^2 - f_th^2 > 0; supersonic
flips the sign):
  S_rth = -16 f r^2 sin f_r f_th^3 / [(f r^2 f_r^2 + f_th^2) Delta_w]
and the two members are EQUAL: m1 (the species' own chain member,
c_w[q_rth] dq*/dw) == m2 (the C1-response member, -L_wq q1-channel)
— forced by the implicit-function identity dq*/dw = -L_wq/L_qq plus
the cross-block symmetry c_w[q_rth] = c_q[w_rth]. Properties: odd in
f_th (odd across the equator), vanishes on spherical as f_th^3,
axis-regular. The branch radial stiffness is c[w_rr]|_* =
4 f r^2 sin (f r^2 f_r^2 + f_th^2)/Delta_w.

**The turning-surface consilience (exact).** D|_{q*, w=0} =
r^2 Delta_w^2/(f r^2 f_r^2 + f_th^2)^2: **the q*-branch metric
degenerates EXACTLY on W3's Delta_w turning surface**, and both
surviving principal coefficients diverge there (their ratio
-4 f_r f_th^3/(f r^2 f_r^2 + f_th^2)^2 stays finite). The W3
chart-robust turning surface, the branch signature degeneracy, and
the divergence of the branch w-operator are ONE locus.

**Structural verdict for registry #28 (post-verification edit).** The
unadjudicated q*-branch is now adjudicated: NO angular stiffness —
but the surviving mixed term BREAKS #28's premise "per-u radial SL
pencils" on the branch (the principal form xi_r (c_rr xi_r + S_rth
xi_th) is degenerate along pure-theta directions: a COUPLING, not a
well). Bands-not-lines survives at the principal-symbol level; the
honest residual is the 2D mixed-coupled operator on the branch
(never solved; Arm-2/W6 target), and the TIME-dependent delta-q
channel (c[q_TT] != 0; the static q* elimination does not capture
it) — both named, neither computed here.

## (v) THE PHI-ANGULAR PAIRING'S DYNAMICAL STATUS (negative)

The W2 pairing R_thphthph = [(1-f) + 4 w_thth]/y^2 acquires **NO EL
channel at this order**: c[w_thth] = 0 identically at all q in all
three EL channels, and the branch carriers vanish — w_thth remains
EL-invisible everywhere (it stays boundary/curvature-diagnostic
structure). What the f-channel acquires instead is the q-MEDIATED
mixed coupling c_f[w_rth] = -2 q r sin/((1+w)^2 sqrt(D)). Recorded
as a death of the hoped-for dynamical entry for Charles's hunch
species at this order [premises: P1 q-on class, EL level, O(kappa);
hypothesis discipline: this hope was aimed at hardest, and it died].

## Deaths and corrections (recorded per discipline)

1. The declaration's "the locus f = 2 kappa is an interior surface
   crossing EVERY cell" — REFUTED on banked geometry (seal-funnel
   cap; (iii)).
2. Mode trapping / locus quantization — DEAD (frozen-f pencil level;
   (iii)).
3. Angular w-stiffness from the q*-branch — DEAD (w_thth theorem;
   (iv)); the branch supplies a mixed coupling instead.
4. The pairing's dynamical entry — DEAD at this order ((v)).
5. W4-P1's ON-branch exact-statics property — DESTROYED by the
   untruncated species ((iii)); W4's P1 verdict carries a TRUNCATION
   premise now made explicit.
6. My own drafted S2 asserts (elliptic angular stiffness ansatz)
   died on computation and were replaced by the computed inventory
   before commit (method note above).

## (vi) Scripts and counts

| script | checks | runtime |
|---|---|---|
| w5_arm1_relation_origin.py | 17/17 | 23 s |
| w5_arm1_qon_angular.py | 18/18 | 90 s |
| w5_arm1_locus_pencil.py | 12/12 | 19 s |

## (vii) Verifier attack list (for the blind pass)

- V-1: the third route's independence — the div-V EL-invisibility
  used 5 exact rational points; close it symbolically or at more
  hostile points; confirm no shared machinery with VA4's scripts.
- V-2: the tie-deformation engine (symbolic exponents f^a) — verify
  P(a,b) by direct integer-exponent metrics: (a,b) = (2,0), (0,2),
  (0,0) must be tadpole-FREE; (2,-2) must give P = 4; check the
  f_thth slot's (a+b) law at (1,1).
- V-3: the branch bookkeeping — redo the reduced O(kappa) variation
  WITHOUT the chain-rule decomposition (direct substitution
  q = q* + kappa q1 into the action at exact rational spot
  configurations) and confirm S_rth and the m1 == m2 split.
- V-4: sign/orientation of E_w (-sqrt(-g) G dg/dw vs jet-EL) through
  to S_rth's sign; the |Delta_w| handling subsonic vs supersonic.
- V-5: the pencil numerics — lumped-potential FEM vs consistent
  assembly; reproduce kappa_c^new ratios with an independent
  discretization; check the V2-shift corollary against a direct
  sweep crossing.
- V-6: the no-trapping readout used the most-unstable node; attack
  with the seal-pole ray (the ray that actually reaches f = 2 kappa)
  and with Robin BCs (the W4 h-dial species).
- V-7: the geometry correction — regenerate from bg_*.dat directly
  (not the npz), finer u-grid near the seal pole; confirm the
  cap fractions and orderings.
- V-8: the time-dependent delta-q channel (c[q_TT] != 0) — confirm
  it is genuinely open (not closable by the same chain argument) and
  scope what a dynamical-q mode problem would need.
