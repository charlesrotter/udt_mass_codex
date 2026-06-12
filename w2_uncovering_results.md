# W2 — Uncovering What the Metric Does in the Shape Sector: Results

Date: 2026-06-11/12. Driver: Claude. Charles-ordered launch
("derive the stiffness"; framing correction of record in
w_stiffness_push_declaration.md: uncovering only, no tack-on
mechanisms — both arms compute EXISTING structure).
Arms: Arm 1 (metric's deeper geometry; scripts
w2_arm1_line{1,2,3,4}_*.py, 68 checks) and Arm 2 (seal/continuation
demands on the shaped class; scripts w2_arm2_*.py, 61 checks).
Blind adversarial verifiers, independent machinery: VW1 = agent
a89ceb5c17191a902 (59 checks: w2_arm1_verifier_l4.py 22/22,
w2_arm1_verifier_l1_l2.py 24/24, w2_arm1_verifier_l3.py 13/13);
VW2 = agent ac489491778457e91 (58 checks: w2_arm2_verifier{1,2,3,4}*,
15+17+9+17). All arm scripts rerun bit-identical. Everything below is
recorded WITH verifier amendments folded in. Interrogation
declaration: metric-led (uncovering); pre-registered failure criteria
in every script; the confirming hopes that died are recorded as
deaths.

## Headline (the composed picture, verifier-ruled)

THE METRIC ALREADY CONTAINS THE STIFFNESS SPECIES — AS A WAVE SECTOR
IT CANNOT YET USE, POLICED BY AN INTERFACE LAW THE ACTION CANNOT SEE,
AND ABSENT EXACTLY WHERE THE CLOSE EXPECTED IT (the seal):

1. **The wave sector (theorem-grade, VW1-strengthened to a larger
   class than the arm ran).** On the shaped class, the curvature
   species' only EL-visible w-dynamics is the bulk quadratic
   [2 r^2 sin(theta)/(1+w)^2] (w_T^2/f - f w_r^2) — an f-weighted
   hyperbolic wave operator with characteristic speed
   dr/dT = +-f = c_eff, the postulate's own clock-rate speed.
   Right-sign kinetic under +Int sqrt(-g) R; principal symbol
   verified independently (coeff[w_TT]/coeff[w_rr] = -1/f^2). THE
   FIBER CANCELLATION (VW1-corrected, STRONGER than the arm claimed):
   the density's w_rr, w_Tr, w_Ttheta coefficients vanish identically
   at ALL q, not just q = 0 (the arm's "q-mediated w_rr" was spurious
   uncancelled atoms — refuted; corrected exact q-on row:
   c[w_thth] = 2 r sin(theta)/((1+w)^2 sqrt(f D2)),
   c[w_TT] = q^2 c[w_thth], c[w_rth] = -2 f q c[w_thth]). The angular
   second jets are boundary-concentrated and EL-INVISIBLE (w_thth
   coefficient 2 sin(theta)/(1+w)^3, f-free, pure divergence; the
   bulk is completely w_theta-free). EL-trap audit clean both ways:
   the full second-order jet EL matches -sqrt(-g) G^{mu nu}
   d g_{mu nu}/dw exactly (the W1-Route-B trap not repeated).
   SONIC CONSILIENCE (the close's fingerprint, exact): g =
   (f f_r - f_T)(f f_r + f_T)/f — C1's w-force flip locus IS the wave
   cone of this sector, and C1's entire time-dependent solution set
   (subsonic, |f_T| < f |f_r|) lives strictly INSIDE the cone.
   Provenance: postulate -> metric -> curvature identities
   (guardrail-legal diagnostics) -> exact coefficient extraction.
   NOTHING IMPORTS IT AS DYNAMICS: what is banked is what the
   geometry contains.

2. **The interface law (mathematics confirmed; status CONDITIONAL —
   VW2's demand-species ruling).** C1 is totally blind to
   w-discontinuities (pi_w == 0 covariantly; a kinked or even
   discontinuous w on a spherical-f exterior is an exact
   distributional solution of the full C1 EL system; zero action
   cost, premise: 1+w bounded away from 0). The metric's curvature
   carries the objection: a w_r-kink deposits an equal-and-opposite
   orthonormal curvature sheet (+-f/(1+w) [w_r]; Ricci-carrying in
   theta-theta/phi-phi, blind in rr and scalar R), with layer
   Kretschmann Int K = 8 (Int m''^2) f^2 [w_r]^2/((1+w)^2 eps) ->
   infinity (cubic mollifier is the strict minimizer: 96 is the
   floor, not universal). IF layer-curvature integrability (C^{1,1}
   angular block) is adopted as a native demand, the metric forces
   [w] = [w_r] = 0 across every interface ([w_rr] free). BUT
   (VW2 adjudication): the corpus's banked metric-own demand species
   are action-stationarity and action-finiteness ONLY — both w-blind
   here; Int-K-finiteness appears nowhere in the corpus, the seal
   itself is banked as real curvature-singular structure, and GR
   practice admits Israel shells. THE REGULARITY DEMAND IS UNBANKED —
   ITS ADOPTION IS CHARLES-CANONIZATION TERRITORY. Until adjudicated,
   the interface law is exactly derived but CONDITIONAL.

3. **Continuation failure = the forced object's job description
   (VW2-STRENGTHENED).** Unique smooth continuation FAILS in the
   w-channel: exact C1 exterior statics with identical interface jets
   TO ALL ORDERS (VW2's flat-bump exhibit upgrades the arm's
   2nd-order exhibit) and different bulk shape; the mirror theorem
   ("the exterior carries zero free structure") is f-sector-scoped.
   The missing sector's derived job: restore uniqueness in the
   w-channel — supply a radial w-operator at interfaces. That
   operator is exactly the wave sector of (1).

4. **The locus inversion (confirmed).** The close located the missing
   object "at exactly the curvature-singular seal". Computed: the
   seal is where the metric's w-vigilance VANISHES — the shaped
   on-axis Kretschmann is the new closed form
   K_axis = a''^2 + 4 a'^2/y^2 + 4[(1-f) + 4 w_thth]^2/y^4
   + 4 f_thth^2/(f^2 y^4), the SINGULAR law stays exactly
   4 f_u(pole)^2/y^4 with zero w-jet content (robust to order-3
   transverse jets; VW2 re-derived the +4 with no 4D engine via pole
   Gauss curvature = (1 + 4 w_thth)/y^2, and by mpmath-60 Richardson;
   the 12-vs-24-erratum convention trap explicitly excluded); the
   junction demand dies at the seal as f^4; no w-BC exists at the
   seal (the w-channel second variation is potential-only — no
   Sturm-Liouville operator on delta-w at any fluctuation order).
   The metric polices shape at INTERIOR interfaces, not the seal.

5. **The phi-angular pairing (Charles's hunch species, exact).** The
   clock deficit and the shape's transverse curvature are
   interchangeable inside a single curvature component:
   R_th^ph^th^ph^ = [(1-f) + 4 w_thth]/y^2 — the w-jet lives NOWHERE
   else on the axis; a third native perfect square in a
   dilation-adjacent variable, and a derived phi-angular interaction.

6. **THE CROSS-BLOCK DISCOVERY (VW2's load-bearing find; the arm was
   silent on it).** The w-f and w-q second-variation cross blocks are
   NONZERO (L_wf_theta = (c/2) sin(theta) f_theta/(f(1+w)^3),
   L_wq = -(c/2) sin(theta) f_r f_theta/(1+w)^3). Schur-eliminating
   the algebraic delta-w FLIPS the f-channel angular gradient
   coefficient -c/4 -> +c/12 (the registry-#20 angular-flip species,
   now inside the static diagonal+w class), and the joint
   (delta-w, delta-q) elimination gives an effective angular
   stiffness whose numerator is EXACTLY Delta_w =
   f r^2 (1+w)^2 f_r^2 - f_theta^2 — the w-dressed sonic locus,
   which reaches the pole exactly at seal touchdown (f_theta/f ->
   infinity). CONSEQUENCE: S1's seal fluctuation problem and the
   theta-dial selector question must be RE-POSED on the w-completed
   fluctuation class; the "no theta-dial selector" reading in (4) is
   conditional on frozen delta-w. This is the immediate compute
   frontier.

## Deaths and unforced forks (recorded per discipline)

- Rate-transport holonomy: d(d phi) = 0 — zero w-content (death;
  foreordained for an exact 1-form, recorded honestly). The
  SYNCHRONIZATION transport on C1's nondegenerate branch is the
  nontrivial one: omega = lambda d_spatial f, lambda = 2 D2 f_T/Q;
  loop density H* = lambda_r f_theta - lambda_theta f_r — first-jet
  in w, vanishes on spherical AND static, diverges on the sonic
  locus; VW1-strengthened rigidity: no class-preserving time
  relabeling kills it (the unique nontrivial relabeling branch has
  integrability obstruction exactly H = 0; the arm's "licensed
  Killing rescaling" framing was empty — the legal group is smaller,
  H* MORE rigid).
- The tie fork: the corpus ties phi at the metric-component level
  (g_tt = -e^{-2 phi} c^2, primitive; only named observer family is
  stationary). The normal-observer reading R-norm (under which w
  enters the tied slot and C1 becomes w-dynamical at zero new
  postulates, at the price of a second-jet f-sector) is NOT
  corpus-forced; VW1 adjudicated the ranking FOR R-stat (corpus
  search: "normal observer"/"Eulerian"/"weld frame" nowhere;
  "comoving" only in LCDM-comparison text). Declining the
  w-dynamical C1 was correct under the program's own discipline. The
  fork stands recorded; on C1's branch N^2 = f R^2/Q^2 exactly — the
  opener's perfect square IS the lapse factorization N|Q| =
  sqrt(f) R.
- The perfect squares: ONE origin theorem for the two elimination
  squares (C1's density is N/sqrt(Delta) on any symmetric 2x2 block;
  envelope/discriminant identity, degree-1 stationarity); the rho
  square has a different origin (forced completion). The angular
  u-variable identity (u = f r (1+w):
  u_theta^2/r^2 - (1+w)^2 f_theta^2 = 2(1+w) f f_theta w_theta
  + f^2 w_theta^2) is exact but VW1-adjudicated SELECTION-POWERLESS:
  it is completing-the-square for ANY weight (infinite-dimensional
  brick fork; u_det exactly w-blind; matching the curvature species'
  weight forces the w-blind member). Banked as structure, not as a
  candidate.
- The EH-remainder species lives in the BREATHING (rho) mode, not the
  shear: sqrt(-g) R/sin(theta) + d/dr[rho^2 f' + 2 f rho rho'] =
  2 - 2 f rho rho'' on the spherical face (raw rho'' coefficient
  -4 f rho).

## What "derive the stiffness" now requires (the narrowed step)

The species, the operator, the locus, and the job description are all
computed. What remains underived is the single step that FORCES the
wave sector into the dynamics. The live, derived dials (each
Charles-relevant):
(a) the curvature-regularity demand (adopt/reject — decides the
    interface law's status and, with it, whether the metric's own
    consistency forces a w-operator at interfaces);
(b) the tie fork (R-stat corpus-ranked; R-norm would hand C1 the
    w-dynamics directly — a canon question about what phi measures,
    not a computation);
(c) the cross-block re-pose of S1/theta-dial (pure computation, next
    in queue): the w-completed fluctuation problem may already
    contain the selector the close ordered as the follow-on question.
Normalization of the wave sector remains the underived object in
every branch (W1 #24's kappa-sign result stands).

## Verifier records

VW1 (2026-06-11/12): 59 independent checks; one substantive
refutation (the q-mediation wording, corrected above); hygiene: arm
honest independent counts ~15/18, ~12/13, ~21/23, ~12/14 (duplicates/
prose checks named); L4-02's two-point numeric Gamma-Gamma split now
covered symbolically at q=0 + hostile q-on points.
VW2 (2026-06-12): 58 independent checks; mathematics confirmed or
strengthened everywhere (claims 2,3 upgraded); two structural
rulings: the interface law is CONDITIONAL (unbanked demand species —
canonization territory), and the cross-block finding forces the S1/
theta-dial re-pose; hygiene: two vacuous banner checks named (honest
59 real checks), the 96-is-mollifier-floor and 1+w-bounded premises
recorded.
