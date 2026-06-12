# W4 — Solution-Space Probe of C1 + kappa*W_wave: Results

Date: 2026-06-12. Driver: Claude. Declaration: W4 section of
w_stiffness_push_declaration.md (probes P1-P5 and outcome grading
pre-registered before any run; Charles's instruction "instead of
proposing what the metric does, solve it"). EVERYTHING AT kappa != 0
IS HYPOTHESIS-GRADE: numerics are the telescope; nothing here is
banked as theory — what is banked is the solution-space MAP with its
premise sets, plus the exact structures (sympy) that survived
verification.
Solvers: Agent A (P4/P1/P2; w4a_system.py 38/38, w4a_p1_existence.py
9/9, w4a_p2_spectra.py 8/8) and Agent B (P3/P5; w4b_* suite, 822-cell
catalog). Blind verifiers, independent machinery: VA4 = agent
afe10632dcc95ae3a (w4a_verifier1_sym.py 28/28, w4a_verifier2_blowup.py
11/11, w4a_verifier3_spectra.py 8/8; all agent scripts rerun
bit-identical) and VB4 = agent aa44564952c4d0767 (w4b_verifier_* suite
incl. 7 fresh library members and the trust-window coupled test).
Verdicts below carry all verifier amendments.

## Pre-registered grading: OUTCOME (ii) — A GENUINE kappa-BAND

Durable shaped matter (T-bounded ringing cells; static shaped
equilibria with stable oscillation; formation events that settle onto
shaped equilibria) EXISTS at every swept kappa OUTSIDE a computed
instability band (0, kappa_band). The wave-sector completion is NOT
falsified; PERSISTENCE SELECTS. The band edges are spectral objects
of one shared weighted Sturm-Liouville operator:
- kappa_c (D_cell-ON gap edge; generalized Rayleigh quotient) —
  VA4-corrected, grid-converged: M1 0.01160, M2 0.00789, M4 0.00829
  for the w-channel pencil; Agent B's evolution-side edges (t-FEM,
  VB4 thrice-confirmed incl. independent shooting): M1 0.070620
  (banked 0.070346 was 0.4% underconverged), M2 0.025560, M4
  0.009013. [The two kappa_c families live on different operators —
  the spectral pencil vs the evolution Rayleigh functional; both
  carried, labeled.]
- kappa_s (D_cell-OFF static-existence fold, Bratu/Liouville-type):
  M1 0.13365, M2 0.04863, M4 0.01715.
- THE RATIO kappa_s/kappa_c: holds at 1.894-1.9026 across TEN members
  (3 original + 7 fresh, gamma 0.25-2, c/c* 1.3-4.0 — VB4). It is NOT
  a rational constant (flat-weight exact value 1.87253 =
  2 pi^2/(3 * 3.513830719), the classical Gelfand fold; generic
  smooth weights span 1.81-2.03): the member-independence is genuine
  structural information driven by the shared SEAL-LAYER WEIGHT SHAPE
  (p = f e^{-t} decaying, b = (f_theta^2/f) e^{-t} growing toward the
  seal) — a derivable weight-shape proximity, not numerology. This is
  the sharpest derivation target the probe produced.

## The verified solution-space map (premise sets binding)

- **P4 macro gate (exact, by-construction content):** the spherical
  sector is kappa-blind at every kappa, both D_cell branches — and
  VA4's new species tadpole (below) is also ∝ f_theta^2, so the gate
  survives the truncation question too.
- **Exact structure (VB4-upheld):** in v = ln(1+w) the wave sector is
  EXACTLY FREE; per-theta-ray decoupling on frozen f; the source is
  Liouville-type (D_cell OFF: -(c/16 kappa)(f_theta^2/r^2) e^{-2v},
  one-sided pull) or sinh-Gordon-type (D_cell ON: v = 0 equilibrium,
  exact linear slope +3); exact boundary-only energy flux law (both
  branches).
- **P1 static existence (VA4-amended):** D_cell ON — banked cells are
  exact full-system statics at every kappa (the tadpole cancellation
  is an identity in the f-jets). D_cell OFF — shaped static cells
  exist ABOVE the fold (qualitative map confirmed; quoted thresholds
  were grid brackets — true M1 edges 0.122/-0.0768; edge failures
  were guard-defined: with guards removed both M1 edge cases seal);
  "exist iff |kappa| >= threshold" REFUTED AS STATED — it is a
  statement about the w(weld) = 0 slice only (sub-threshold dressed
  welds seal; the w0 = 0 choice rests on the CONDITIONAL W2 interface
  law — premise named). The f-spherical branch carries an exact
  action-degenerate ZERO-COST SHEAR CONTINUUM {f = C+a/r, q = 0,
  w = g(theta), g(poles) = 0} (closed form extended by VA4 to general
  spherical f; the K == 0 collapse is load-bearing on elementary
  flatness — dropping flatness admits off-axis shear-hair).
- **P3 persistence catalog (VB4-upheld; frozen-f premise on the full
  domain):** kappa < 0 RINGS at all |kappa| (M1 dominant omega
  13.1246 + sidebands; the theory's first bulk ringing); D_cell ON
  0 < kappa < kappa_c GROWS (true rates 0.5-1.1/T — the report's
  0.21-0.38 understated) -> terminal collapse, NO breathers (implicit
  Radau resolved the stiff kappa = +-1e-3 cells: +1e-3 collapses,
  -1e-3 bounded); kappa > kappa_c rings; D_cell OFF above the fold:
  eq+bump RINGS about the shaped equilibrium (displacement
  kappa*min(v_eq) = -0.0329), bump-only SETTLES onto it (formation
  events); amplitude-independent except band edges (exact
  v-linearity).
- **P2 spectra (VA4-amended):** anchor gate passed (banked rungs to
  5.3e-6). The w-channel pencil: per-u radial SL, NO w_u stiffness —
  radial-discrete x angular-continuum => **BANDS, NOT LINES** (M1
  band [2.185, 3.953] vs gap ~60). VA4's adjudication upgraded this:
  on D_cell-ON, w-bar = 0, q = 0, the ENTIRE delta-w/delta-f cross
  block vanishes identically — bands-not-lines is THEOREM-GRADE on
  that branch (true normal modes); on D_cell-OFF the frozen spectra
  are diagonal-block readouts on an off-shell background; the
  q*-branch is unadjudicated. Notes track the f-weighted crossing
  time within ~11%; HONEST box-control verdict: the 1% -> 5% trust
  cut shifts omega^2_1 by 31-35% — SCALE AUTONOMY NOT ESTABLISHED on
  truncated domains (the seal-region treatment owns the notes;
  registry-#1 species). kappa < 0 all-ringing is NOT BC-robust
  (Robin h = 5 injects deep negative modes — h-dial species);
  small-kappa>0 instability IS BC-robust.
- **P5/coupled, the mechanism VINDICATED (VB4's trust-window test —
  the probe's biggest single upgrade):** the full-domain coupled
  (f,w) system cannot be marched because the banked backgrounds sit
  at f_min = 0.002 with ZERO seal margin (kappa > 0 wave stress
  deepens the seal -> f crosses 0; kappa < 0 UNSEALS the cell,
  f_min -> ~1, characteristic speeds explode). On the TRUST-WINDOW
  domain (t <= t_5%) the SAME coupled machinery MARCHES REGULARLY
  (all four (kappa-sign, amp) tests; f_min stays at 1.0000; bounded
  envelopes; the kappa < 0 run shows the predicted unsealing
  max f/f_b = 3.36 yet stays stable) — the full-domain collapse is a
  SEAL-MARGIN DOMAIN ARTIFACT, not intrinsic; the frozen-f premise is
  a boundary-layer artifact. Durable shaped matter survives full
  back-reaction on trust domains.
- **BC structure (VB4-upheld):** every observed BC delta is predicted
  by the kappa_c(BC) formula (dir/dir vs dir/neu factor 1.9428;
  Robin/Neumann constant mode; outgoing -> DISPERSE, no shape memory
  without reflection).
- **Sign chain (VA4-settled, no relabel error):** the conventions are
  consistent end-to-end. Invariant reading: C1's own f time-kinetic
  is NEGATIVE in the banked convention (density ∝ the sonic g), so
  the ringing branch (kappa < 0) is the branch whose w-kinetic is
  SIGN-MATCHED to C1's f-kinetic, and the growing branch (small
  kappa > 0) is the relative-ghost pairing. The W2 label "right-sign
  kinetic under +sqrt(-g) R" is standalone-only.

## THE TRUNCATION FINDING (VA4, verifier-grade, two independent
## routes — the named W5 target)

The declared W_wave was the species' w-JET content only. The full
curvature species carries an additional EL-visible ALGEBRAIC
w-tadpole:
  E_w[sqrt(-g) R] = EL_w[W_wave] + sin(theta) f_theta^2/((1+w)^3 f^2)
                  = EL_w[W_wave] - (2/f) dL_C1/dw   (exact, q=0 class)
— w-jet-free (the W2 jet claims survive), vanishing on spherical (P4
survives), but NONZERO at w = 0 on shaped cells. The W4 system
therefore SOLVED A TRUNCATION of the species (jets kept, algebraic
force dropped), and the declaration's "the unique EL-visible
w-content" is wrong as worded (unique w-JET content). The exact
relation to C1's own tadpole (-(2/f) dL_C1/dw) is structural and is
the most derivation-suggestive single line of the push: the FULL
species' algebraic force and C1's w-force have a fixed ratio -2/f —
the untruncated system C1 + kappa*(full species w-content) has a
natural balance structure never yet solved. W5 = re-solve with the
untruncated species; every W4 map quantity (folds, gaps, the 1.90
proximity) gets re-derived there.

## Registry / discipline

- NEW #28 appended: no angular quantization from the wave sector at
  this order (bands not lines) — theorem-grade on D_cell-ON
  (w-bar = 0, q = 0; cross-block vanishes identically), diagonal-
  block-only on D_cell-OFF, q*-branch unadjudicated. The angular
  discreteness gap persists at this order; premise set carries the
  TRUNCATION flag above.
- Scale autonomy NOT established on truncated domains (seal-cut owns
  the notes) — recorded inside #28's premise set, registry-#1
  species.
- Hygiene on record: Agent A check-count inflation (5 of P2's 8 were
  banners), kappa_c interpolation bias (+10-11%), guard-defined
  edges, Agent B GROW-rate understatement, M1 kappa_c 0.4%
  underconvergence, the energy-gate kappa<0 normalization pathology
  (correctly unbanked), Agent B's frame-mixing premise (f-sector in
  library frame, w-channel in primary frame — named, verifier attack
  target for W5).

## Queue implication (next, in order)

1. W5: the UNTRUNCATED species solve (the -2/f balance structure) —
   re-derive the band, the fold, and the 1.90 proximity on the full
   w-EL content; trust-window domains (the coupled system is regular
   there); fully-primary-frame f-flow (kill the frame-mixing
   premise).
2. Derive the seal-weight Bratu ratio analytically (the 1.90
   proximity as a theorem about the seal-layer weight shape).
3. The kappa-selection question vs the three standing forks (D_cell;
   regularity demand; tie) — the solution space now DISCRIMINATES:
   D_cell-ON vs OFF give different durable objects (oscillation about
   spherical vs about shaped equilibria) — a physics-level
   discriminator for Charles's test-both adjudication, downstream of
   W5.
