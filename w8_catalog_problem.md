# W8 PHASE-A (ASSEMBLE) — The Catalog Problem, Stated Explicitly

Date: 2026-06-13. Driver: W8 Phase-A agent. Declaration binding:
w_stiffness_push_declaration.md (W8 section); frame: CATALOG_FRAME.md.
Mode: ASSEMBLE ONLY (no GPU, no heavy compute). This document states
the catalog problem precisely enough that a Phase-B solver agent can
execute it directly. Light-sympy confirmation of every load-bearing
form: w8a_formula_confirm.py (15/15 PASS, /tmp/w8a_formula_confirm.log).

DISCIPLINE (binding throughout): mechanism-OPEN (static AND breather
allowed; angular sector's role — algebraic vs oscillatory — to be
revealed, not pre-decided); UNCOVER don't propose; DATA-BLIND (no tuning
to the wall numbers); classification not deformation. Every banked
condition below is flagged THEOREM-GRADE or HYPOTHESIS-GRADE. All
kappa != 0 / time-dependent physics is HYPOTHESIS-GRADE until derived +
blind-verified + Charles-canonized.

THE FRAME (do not drift): a particle = ONE STABLE SELF-CONSISTENT
SOLUTION of the metric field equations. The discrete CATALOG of such
solutions = the candidate particles. Their Misner-Sharp masses = the
candidate spectrum. This is a nonlinear EXISTENCE/STABILITY problem, NOT
a mode-spectrum / eigenvalue problem.

---

## (i) THE FIELD SYSTEM (exact)

### Fields and metric (R-areal canon rho = r; w8a-1a/1b)

Three bulk fields f, q, w on (T, r, theta), axisymmetric even sector,
plus the time row (a, b) = (g_Tr, g_Tth) for the nonstationary /
breather branch. The P1 metric class:

    ds^2 = -f dT^2 + f^{-1} dr^2 + 2 q dr dtheta
           + r^2 (1+w)^2 dtheta^2 + r^2 sin^2(theta) (1+w)^{-2} dphi^2

    det g4 = -(r^2 sin^2/W) D,   W = (1+w)^2,   D = r^2 W - f q^2
    sqrt(-g) = r sin(theta) sqrt(D)/(1+w)

The areal canon rho = r survives ALL w: g_thth g_phph = r^4 sin^2
exactly (w8a-1b). rho = r is THEOREM-GRADE (R-areal canon, CANON.md,
macro-validated SNe/BAO/Misner-Sharp stack). The (a,b) time row is
needed only for the breather/nonstationary branch and the fold closure
(see (ii.4)); on the static branch a = b = 0.

### The action (the forced system)

    S[f, q, w] = S_C1 + kappa * S_species + beta * S_Dcell

- **C1 (the dilation kinetic action; THEOREM-GRADE, the metric's own
  single derivative channel via the tie phi = -(1/2) ln f, registry
  #23):**

      L_C1 = (c/2) e^{-2 phi} g^{ab} (d_a phi)(d_b phi) sqrt(-g),
             phi = -(1/2) ln f,   c = 2 (positive banked convention)

  Reduced at q = 0, static (w8a-2a):

      L_C1|_{q=0,static} = (c/8) sin(theta)
                           [ r^2 f_r^2 + f_theta^2/(f (1+w)^2) ]

  The angular piece L_C1ang = (c/8) sin f_theta^2/(f(1+w)^2) carries the
  RUNAWAY TADPOLE dL_C1/dw|_{q=0} = -(c/4) sin f_theta^2/(f(1+w)^3)
  (w8a-2b) — this is exactly why C1 ALONE holds no shaped static matter
  (registry #21/#22, THEOREM-GRADE): the tadpole drives w to runaway
  with no restoring term.

- **W_species = the curvature w-content (mechanism-open; carry kappa as
  a parameter; HYPOTHESIS-GRADE that kappa != 0 is the physical
  completion).** The species is the Gamma-Gamma bulk of sqrt(-g) R minus
  its w-free part (w6_arm1_lib build_all_jets: Dw = LGG - LGG0). At q = 0
  it equals EL[W_wave + D_alg], with:

  - **W_wave (W2/VW1, THEOREM-GRADE as the EL-visible w-content of the
    species at q = 0):**

        L_Wwave = [2 r^2 sin(theta)/(1+w)^2] (w_T^2/f - f w_r^2)

    f-weighted hyperbolic wave operator; characteristics dr/dT = +-f
    (rides the sonic locus). Right-sign kinetic. The static row is the
    regular geometry (w8a-3a):

        L_Wwave|_static = -2 r^2 sin f w_r^2/(1+w)^2

  - **D_alg (W5, THEOREM-GRADE algebraic w-potential; the untruncated
    completion):**

        L_Dalg = -(1/2) sin(theta) f_theta^2/(f^2 (1+w)^2) = -(2/f) L_C1ang

    so that L_C1ang + kappa*L_Dalg = (1 - 2 kappa/f) L_C1ang (w8a-3b/3c):
    the C1 angular obstruction is RESCALED pointwise — it cancels on the
    locus f = 2 kappa and FLIPS SIGN for f < 2 kappa. (The f = 2 kappa
    locus is dynamically INERT as a trap/selector, registry #29
    THEOREM-grade-on-its-premises; but the FACTOR (1-2kappa/f) is the
    real structure that makes the seal-side w-potential a wall.)

- **D_cell (test-both branch; UNADJUDICATED FORK awaiting Charles):**

      L_Dcell = (c/4) sin(theta) [ w f_theta^2/f + q f_r f_theta ]

  Adopting D_cell (beta = 1) cancels both C1 tadpoles exactly AT w = 0,
  making banked cells exact C1+D_cell statics with NO stiffness (registry
  #24); rejecting it (beta = 0) leaves shape non-dynamical until the
  stiffness sector. Phase B must carry BOTH branches (test-both,
  standing protocol).

### The exact field equations (committed; cite w5_arm2_sym, w4a_system)

- **w-equation (untruncated, w5_arm2_sym C1):**

      kappa EL_w[W_wave] + (1 - 2 kappa/f) dL_C1ang/dw
        + beta dL_Dcell/dw = 0

  In v = ln(1+w) the wave sector is exactly free (w5_arm2_sym C2); the
  per-ray frozen-f reduced PDE (w4b_evolib header, the Phase-B solve
  variable; tortoise dr/dx = f):

      v_TT = v_xx + 2 (f/r) v_x + S(v; x)
      S_off(primary) = -(c/(16 kappa)) (f_theta^2/r^2) e^{-2v}
      S_on (primary, D_cell) = +(c/(16 kappa)) (f_theta^2/r^2)(e^v - e^{-2v})

  ON-branch algebraic equilibrium e^{3v} = 1 - 2 kappa/f (exists only
  where f > 2 kappa; w8a-6a); v = 0 is NOT an equilibrium at kappa != 0
  (w8a-6b): every shaped cell self-dresses.

- **f-equation (w4a_system D2):** the w-GRADIENT sources f at kappa != 0
  (back-reaction):

      -(c/4) sin (r^2 f_r)_r - (c/4) d_th[sin f_th/(f(1+w)^2)]
        - beta(c/2) d_th[sin w f_th/f] - (c/8) sin f_th^2/(f^2(1+w)^2)
        - 2 kappa r^2 sin w_r^2/(1+w)^2 - beta(c/4) sin w f_th^2/f^2 = 0

- **q-equation:** angular sector closes ALGEBRAICALLY (w4a_system A6;
  w8a-4a). The q-stationary branch:

      q* = 2 r^2 (1+w)^2 f_r f_theta
           / (f r^2 (1+w)^2 f_r^2 + f_theta^2)

  and Delta_w = f r^2 (1+w)^2 f_r^2 - f_theta^2 (the elimination-breakdown
  / mirror-fold surface; w8a-4b). On the diagonal/Class-A library, q = 0
  is a class restriction, not a free-q solution. THE SAME-MINUS TIME ROW
  IS THE REGULAR GEOMETRY (W6): with the time row on, det g4 lifts off
  the static D = 0 degeneracy (w8a-1c/1d) — D = 0 is a FOLD (mirror
  crease), not a curvature edge.

**Macro-invariance gate (THEOREM-GRADE, w4a_system C1-C3, w5_arm2_sym
F2):** every species/D_cell EL contribution vanishes IDENTICALLY on
w = 0, f_theta = 0; the banked spherical vacuum f = C + a/r solves the
full completed system at every kappa, beta. The macro sector cannot see
kappa. This is the binding acceptance test (b) — any Phase-B variant
must re-confirm it.

---

## (ii) THE CELL-DEFINING CONDITIONS (what makes a solution a CELL)

A solution of (i) is a CELL only if it ALSO satisfies the banked
cell-defining conditions. Each stated explicitly with file:line + grade.

### (ii.1) CLOSURE SELECTOR — sigma != 0 (matter is forced)

CONDITION: a closed cell that contains its deep endpoint, has FINITE C1
action, and is nontrivial MUST have nonzero source sigma (= the
dilation-response source W_ff). Equivalently: a nontrivial finite-action
closed cell cannot be vacuum; it owns its center.

> "CLOSURE + FINITE ACTION + NONTRIVIALITY => sigma != 0. Scoped: cells
> owning their center; annular cells evade; Galerkin class."
> — sourced_second_jet_results.md:114-117. **GRADE: THEOREM** (S2 + V2,
> verifier-adjudicated).

### (ii.2) JOINT TERMINATION — finite depth = native compactness

CONDITION: a nontrivial closed finite-action cell TERMINATES at finite
depth (metric degeneration, kappa->1, EL-correct y ~ 0.22-0.62). Escape
branches ride the B/y vacuum mode whose C1 action is non-integrable, so
the selector kills them. The domain is COMPACT, not open.

> "NONTRIVIAL CLOSED FINITE-ACTION CELLS TERMINATE AT FINITE DEPTH (the
> selector theorem kills every escape) ... Native compactness ...
> theorem-grade statement in the Galerkin class."
> — sourced_second_jet_results.md:118-127. **GRADE: THEOREM** (V2).
> CONSEQUENCE FOR THE REGISTRY: #1 (open-domain empty point spectrum)
> is CONDITIONS-CHANGED here — the domain is not open.

### (ii.3) SEAL = MIRROR FOLD (the closure / boundary condition)

CONDITION: the cell closes on its own mirror. The seal is the
fixed-point set of the same-minus involution (a,b) -> (-a,-b); D = 0 is
that fold (w8a-1c/1d). The closure imposes a MIRROR (parity) boundary
condition at the fold, NOT a torn-edge Dirichlet. Static-slice curvature
is singular there (24 a^2/y^4 on axis, erratum) but that is the
measure-zero crease; the time-on geometry is regular Lorentzian and
geodesics cross smoothly.

> "the Delta_w = 0 surface is a mirror-fold closure (same-minus fixed
> surface), not an edge; ... the time-row completion is regular
> Lorentzian (det g4|_{D=0} = -(r sin)^2 (b-fqa)^2/[f(1+w)^2], exact)"
> — w6_results.md:122-127; NEGATIVES_REGISTRY #30 RE-AMENDED:428-456.
> **GRADE: THEOREM** (class-general exact determinant identity;
> finite-K values member-numerical; TIME-DEPENDENT physics
> HYPOTHESIS-GRADE).

The W7 solve (registry #1 W7 re-confirmation:458-477) found the mirror
BC LABELS parity and adds a depth-invariant overtone ratio (the
2pi^2/(3G*) Gelfand-Bratu shape factor), but supplies NO absolute scale
on its own — the outer finite-cell Dirichlet quantizes. SCALE comes from
the cell's own size/termination, not from a mode ladder. (This is
consistent with the catalog frame: distinct cells, not rungs.)

### (ii.4) CENTER OWNERSHIP

CONDITION: a cell bound by the selector OWNS its center (the selector
binds it); a terminated cell that does not own a center is not a
selector-bound cell.

> "cells owning their center; annular cells evade"
> — sourced_second_jet_results.md:115. **GRADE: THEOREM.**
> "terminated cells own no center (selector doesn't bind them)"
> — STATE.md:366 (exterior-field picture). **GRADE: THEOREM consequence.**

### (ii.5) FORMATION LAW — c* = chat gamma^2 (formation <-> shaping)

CONDITION (provenance of a candidate cell, not an independent constraint
on the solved field): cells precipitate from the universe-side medium
under the threshold c* = chat gamma^2, chat = 0.498912 +- ~1e-5 (NOT
1/2). gamma SHAPES the cell (monopole dilation gradient); c SEALS it
(angular momentum flux). Depth diverges at c -> c*; deepest cells
precipitate just above critical driving.

> "c* = chat gamma^2 asymptotically exactly ... chat = 0.498912 +- ~1e-5
> (NOT 1/2). BOTH channels required: gamma shapes ..., c seals."
> — exterior_cavity_results.md:63-73. **GRADE: THEOREM** (within the
> diagonal class; VX1-confirmed). NOTE registry blanket premise #21: all
> banked cell objects are CONSTRAINED-CLASS flows (diagonal or Class B),
> not full-class statics — the formation law is a diagonal-class result.

The formation flow itself is the committed EL flow (w4b_backgrounds
flow()): X_tt - X_t = 2 P_X with weld data X(0) = (1,0,0,0),
X_t(0) = (gamma, -c, 0, 0). The candidate cell parameters (gamma, c)
enter HERE.

### (ii.6) FINITE C1 ACTION

CONDITION: the cell's total C1 action is bounded (vacuum B/y modes cost
non-integrable action and are excluded). Load-bearing in BOTH (ii.1) and
(ii.2). — sourced_second_jet_results.md:108-127. **GRADE: THEOREM** (V2).

---

## (iii) THE LIMITED VARIABLE LIST (the search space — free vs fixed)

This is Charles's crux: the catalog = the discrete subset of this
limited parameter space that yields stable self-consistent cells.

| Parameter | Role | FREE / FIXED | What fixes it (cite) |
|---|---|---|---|
| **gamma** (shaping; monopole dilation gradient) | sets cell shape via formation flow weld data X_t(0)=(gamma,...) | **FREE** | continuous formation input (w4b_backgrounds; exterior_cavity) |
| **c** (seal/formation flux) | seals the cell; weld data X_t(0)=(...,-c,...) | **FREE but THRESHOLD-CONSTRAINED**: must satisfy c* = chat gamma^2 to form a deep cell; c is given as a multiple of c*(gamma) (M1 = 1.3 c*, M2 = 2.0 c*) | formation law (exterior_cavity:63-73, THEOREM) |
| **kappa** (species coupling, magnitude AND sign) | strength of the w-stiffness completion | **FREE / UNDERIVED** — swept both signs | NOT fixed by the metric yet; the watched import thread (#23 caveat, "-2" provenance). HYPOTHESIS-GRADE. Deriving it is queue item 2. |
| **beta** (D_cell on/off) | which completion fork | **FORK (test-both)**, beta in {0, 1} | UNADJUDICATED, awaiting Charles (registry #27) |
| **w-shape g(u)** (angular profile of the cell) | the shaped-matter content | **FREE within the ell-truncated angular basis** (g1,g2,g3 = ell 0/1/2 shapes; w4b_evolib bump_profile) | the catalog selects which shapes hold |
| **ell-structure / N = 3** | angular vector-space dimension | **FIXED = 3** | unique antisymmetric triplet from the H1 area form (negative_phi:2590-2594, DERIVED); q = 1/dim H1 = 1/3 (particle_spectrum:415, DERIVED) |
| **q = 1/3** | angular charge | **FIXED** | H1 area form (particle_spectrum:415-420; THEOREM-grade via H1 projector, negative_phi:29174). On a solved cell q = q* algebraic (w4a A6) — q is NOT an independent dynamical DOF. |
| **eta = 1/18** | interface action / source normalization | **FIXED** | eta = 2/dim(Lambda^2 End(H1)) = 1/18 (particle_spectrum:418, DERIVED); selector-echo q^2/4 = eta/2 (mass_audit). The N=3 -> eta=1/(2N^2) route is HYPOTHESIS-grade (negative_phi:2595). |
| **depth / termination y_stop** | where the cell terminates | **FIXED by the dynamics** (joint termination, ii.2) given (gamma, c) | NOT free; an output of the formation flow + selector |
| **time row (a, b) / breather frequency** | static vs breather mechanism | **OPEN** (mechanism-open): static = a=b=0; breather = nonzero periodic | to be REVEALED by the solve, not pre-set |

So the EFFECTIVE FREE SEARCH SPACE for a candidate cell is:

    { gamma (>0), c/c*(gamma) (>=1, the seal multiple),
      w-shape g(u) in the ell-basis, kappa (both signs), beta in {0,1},
      static-vs-breather mechanism }

with q = 1/3, eta = 1/18, N = 3, depth, and the seal-fold closure FIXED
by the metric. The simplest base cell (lepton candidate) is the
LOWEST-ell shaped cell: g1 (ell <= 1 angular content) on a single-center
gamma~1 member near threshold.

---

## (iv) THE OBSERVABLE — Misner-Sharp mass

The one public number a cell carries (mass_audit_results.md, DERIVED,
VMA 112/112). In areal radius:

    m_MS(r) = (r/2)(1 - f)                      (w8a-5a)

The cell's exterior CHARGE is the interface-momentum jet functional
(Legendre transform of the mass function):

    p_F = y M0'(y) - M0(y) = MS exterior mass   (mass_audit:50-52; w8a-5b)
    Q = 2 p_F                                   (CATALOG_FRAME:38)

On a C = 1 exterior weld leaf f = 1 + a/y, M0 = -a/2 is constant and
p_F = -M0 = +a/2, Q = a (w8a-5b). p_F is linear, superposable, conserved
to ~2.5% along formation. **GRADE: DERIVED (THEOREM).**

THE CATALOG OUTPUT = { p_F(cell) : cell in the stable catalog }. Their
RATIOS are the data-blind falsification quantity, compared LATER (NOT in
the scan) to the six lepton wall numbers (contract 26fc757,
lepton_ladder_falsification_contract.md):

    C_M1 = 0.977679087638,  C_E1 = 1.93121474779,
    ratio C_E1/C_M1 = 1.97530536575   (+ the warped triple
    C_M1=0.936832609588, C_E1=1.81920864981, ratio=1.94187161205)

These are the FALSIFICATION TARGET. NO tuning toward them (binding).

---

## (v) OPERATIONAL "STABLE SELF-CONSISTENT CELL" (mechanism-open)

A solution is a STABLE SELF-CONSISTENT CELL iff ALL of:

1. **SELF-CONSISTENT:** solves the full coupled (f, q, w) field system
   (i) — w-equation, f-equation back-reaction, q = q* algebraic — to the
   declared residual, on its own self-dressed background (not frozen-f as
   a final answer; frozen-f is the inner loop, then iterate to
   self-consistency / quasi-static coupling, w4b_coupled). The macro gate
   must hold exactly at the run's kappa, beta.

2. **FINITE C1 ACTION + PROPER CLOSURE:** finite C1 action (ii.6) and
   closes on the same-minus mirror FOLD at D = 0 (ii.3) — mirror/parity
   BC at the fold, finite-cell outer condition at the weld. Terminates at
   finite depth (ii.2).

3. **PERSISTENCE (the stability test, mechanism-open):** bounded-in-T
   under the dynamics (W4 definition). Using the committed classifier
   (w4b_evolib classify, priority COLLAPSE > GROW > BREATHER > RING >
   DISPERSE > QUIET):
   - **STATIC = trivially persistent**: a static equilibrium (D_cell-off
     Newton solution v_eq exists, w4b_evolib equilibrium_newton) whose
     small perturbations do not grow (RING/BREATHER about v_eq).
   - **BREATHER = bounded oscillation**: env grows < 3x then saturates,
     |log-envelope slope| < 0.005/crossing (BREATHER), or bounded
     ringing (RING, env in [0.2, 3]x, >= 3 sign changes).
   - **UNSTABLE = collapse/runaway**: COLLAPSE- (min v <= ln 0.05, metric
     degeneracy), COLLAPSE+ (max v >= 8 / nonfinite), or GROW (env grows
     and slope > +0.02). These are NOT cells.
   - Validity gates (binding, w4b_gates): G1 energy secular drift <= 1e-6
     (else INVALID, excluded); G2 grid-doubling classification-stable; G3
     GPU-vs-CPU <= 1e-11; UNRESOLVED-STIFF override (integrator failure,
     never banked).

The persistence test reuses W4's evolve + energy gate verbatim (w4b_evolib
evolve_np / evolve_torch + classify + energy); the static existence test
reuses equilibrium_newton; the coupled trust-window machinery is w5_arm2.
The linear gap map (w4b_gates kappa_c_ray) predicts the unstable band
kappa in (0, kappa_c) for cross-check (P3-F3: dynamical threshold within
10% of spectral, else not banked).

NOTE the standing W4 finding (registry #28, scoped): at q = 0 there is NO
angular gradient stiffness — the w-spectrum is radial-discrete x
angular-continuum (bands). In the CATALOG frame this does NOT block:
discreteness comes from WHICH whole cells persist (existence/stability),
not from an angular mode ladder. The q*-branch coupled operator (W6,
registry #30) carries the f-row w_thth door — the phi-angular coupling's
first derived equation — and is where any genuine cross-sector stiffness
would live; Phase B should include the q*-coupled run, not only q = 0.

---

## (vi) THE GPU SOLVE SPEC (Phase B) — with pre-registered outcome criteria

### Base cell first (simplest = lepton candidate)

Start with the SIMPLEST shaped cell: a single-center, low-ell (g1,
ell <= 1) shaped cavity at gamma ~ 1, c just above c*(1) (the M1 member,
c = 1.3 c*). This is the lepton base-cell candidate. Establish the
machinery and the outcome classifier on it before scanning.

### Parameters to scan (the limited space of (iii))

- gamma in {0.5, 0.75, 1.0, 1.5, 2.0} (shape; FREE)
- c/c*(gamma) in {1.05, 1.3, 1.7, 2.0, 3.0} (seal multiple; threshold-
  constrained, formation law fixes c*(gamma))
- w-shape g in {g1, g2, g3} (ell 0/1/2 angular content)
- kappa over a grid BOTH signs spanning the linear-gap kappa_c per member
  (e.g. {-2, -1, -0.5} and {0.25, 0.5, 0.9, 1.1, 2}*kappa_c); subtracted
  species force (registry #29 erratum — bare D_alg artifacts)
- beta in {0, 1} (test-both fork)
- mechanism: BOTH static (equilibrium_newton + perturbation persistence)
  AND breather (full evolve from bumped initial data) per point

### Per-point solve

1. Build the member background by the formation flow (w4b_backgrounds
   flow(gamma, c) -> npz; trust windows t1/t5 from headers; convergence
   anchors B-F1/B-F2 binding).
2. STATIC branch: equilibrium_newton for v_eq (D_cell-off) / direct
   stationary point (D_cell-on); check existence + axis regularity (w8a:
   axis flatness forces w(poles)=0).
3. Self-consistency: iterate the (f, q*, w) coupled system on the trust
   window (w5_arm2_coupled / w4b_coupled), subtracted species force, true
   units c = 2 (member-unit kappa erratum: kappa_banked = kappa_true
   c_m/2 — carry the convention explicitly).
4. BREATHER/persistence: evolve_torch batched over (kappa, amplitude) on
   the V100 (float64; CLAUDE.md pitfalls — no batched solve_triangular
   with broadcast Cholesky; per-batch CPU asserts; G3 trust gate).
   Classify (classify_batch). Mirror/parity BC at the fold, finite-cell
   outer Dirichlet/Neumann at the weld.
5. MS-mass readout: p_F = MS exterior mass of the persisting cell
   (m_MS = (r/2)(1-f); p_F = y M0' - M0 at the exterior leaf). Record
   p_F per stable cell.

### Resolution / convergence (binding)

Nx in {1024, 2048, 4096} grid-doubling classification-stability (G2);
Nu = 24 Gauss-Legendre angular; energy drift <= 1e-6 (G1); GPU-vs-CPU
<= 1e-11 (G3); mpmath 50-digit anchor on source/potential/energy (T-G4);
no 3-term extrapolations bankable; trust windows (1% / 5%) carried — the
full-domain collapse is a seal-margin artifact (VB4), runs on
t <= t_5% domains.

### PRE-REGISTERED OUTCOME CRITERIA (fixed before any scan)

- **"A DISCRETE CATALOG EMERGED"** = stable self-consistent cells exist
  at ISOLATED points / thin slices of the (gamma, c, g, kappa, beta)
  space, separated by regions of COLLAPSE/GROW, such that the stable set
  is a discrete (or low-dimensional, non-space-filling) subset and yields
  a FINITE list of p_F values with computable RATIOS. (This is
  program-confirming — VERIFY HARDEST, per grading (i). Earn it with
  convergence evidence + blind verifier + a derivation of why those
  points and not others.)
- **"A CONTINUUM"** = stable cells fill an open region of the parameter
  space (p_F varies continuously over a 2+ dimensional patch). Then
  stability does not discretize at this order (first-class; would
  CHALLENGE the catalog frame — scope it precisely, report which
  parameters vary continuously).
- **"NOTHING STABLE"** = no shaped (f_theta != 0) cell persists at any
  scanned point (all COLLAPSE/GROW). Then back to the forced-object /
  stiffness question (grading (iii)); record the premise set.

Mechanism stays open: report static vs breather per stable cell; report
whether the angular sector entered algebraically (q* closed) or
oscillated (delta-q dynamical channel active). Do NOT compare to the wall
numbers inside the scan; compute the catalog DATA-BLIND, then compare in
a separate, pre-registered step.

---

## (vii) REUSABLE-MACHINERY INVENTORY (committed scripts)

- **Field system (exact symbolic):** w4a_system.py (C1 + W_wave, P4 gate,
  static field eqs, fluctuation operator); w5_arm2_sym.py (untruncated
  species, (1-2kappa/f) factor, v-chart sources, energy law);
  w6_arm1_lib.py (the unreduced coupled (f,q,w) time-on operator builders
  — geom/gg_split/Jets/blocks; build_all_jets, qstar_expr).
- **Backgrounds / formation:** w4b_backgrounds.py (flow(gamma, c) EL flow,
  member regeneration M1/M2/M4, trust windows, npz export); the formation
  law / threshold lives in exterior_cavity_results.md.
- **Evolution / persistence (the stability test):** w4b_evolib.py
  (evolve_np, evolve_torch batched GPU, classify/classify_batch, energy,
  equilibrium_newton, bump_profile, Geo per-ray tortoise grids,
  pre-registered classifier + validity gates).
- **Trust gates / linear gap map:** w4b_gates.py (T-G1..4 integrator
  trust, kappa_c_ray Rayleigh quotient for the unstable band, omega2_min,
  L-1..4 gates).
- **Coupled / untruncated runs:** w4b_coupled.py, w5_arm2_coupled.py,
  w5_arm2_gates.py (member-unit kappa erratum), w5_arm2_lib.py.
- **MS mass / p_F:** mass_audit_results.md (DERIVED expressions);
  rescued_workspaces/2026-06-11/tmp_loose_scripts/ms_bh.py (reference
  m_MS = (r/2)(1-e^{-2phi})); native_angular_ms_subtraction.py.
- **W6/W7 fold + ensemble machinery:** w6_arm1_*.py (coupled operator),
  w6_flux_*.py (fold/curvature/time-on verifiers), w7_*.py (folded
  time-on ensemble solve, mirror BC, Poschl-Teller spine).
- **This push:** w8a_formula_confirm.py (15/15, /tmp/w8a_formula_confirm.log).

---

## (viii) HONEST BLOCKERS — ill-posedness / under- or over-determination

1. **kappa is UNDERIVED (the central under-determination).** The whole
   species completion hangs on one free number kappa (magnitude AND
   sign), HYPOTHESIS-GRADE, not fixed by the metric (registry #23 caveat;
   the "-2" provenance is one number between native and import). If the
   catalog's existence/ratios depend on kappa, the scan produces a
   kappa-FAMILY of catalogs, not THE catalog. Phase B must report the
   kappa-dependence explicitly; a kappa-INDEPENDENT catalog (or a derived
   kappa) is what would make this well-posed. SWEEP, do not choose.

2. **The D_cell fork (beta) is UNADJUDICATED (registry #27).** beta = 1
   makes banked cells exact statics with NO stiffness AT w = 0 (so shape
   is non-dynamical and "persistence" is trivial there); beta = 0 leaves
   every fluctuation conclusion chart-conditional until the stiffness
   sector. The two branches can give DIFFERENT catalogs. Test-both;
   neither is banked as physical until Charles adjudicates.

3. **All cell objects are CONSTRAINED-CLASS flows (registry #21 blanket
   premise).** The formation law, seals, thresholds, library members are
   diagonal/Class-B flows, NOT full-class statics — full static shaped
   cells are eliminated by theorem under C1 alone (#21/#22). The catalog
   therefore EXISTS ONLY in the completed (kappa != 0) or nonstationary
   class. If kappa != 0 is wrong, the static catalog is empty by theorem
   and only breathers remain.

4. **Bands-not-lines at q = 0 (registry #28).** No angular gradient
   stiffness at q = 0 means a single base cell has a continuum of angular
   shapes at the MODE level. The catalog frame's escape is that WHOLE-CELL
   existence/stability (not modes) discretizes — but this is a BET, not
   yet shown. If stability also fails to discretize (outcome "continuum"),
   the frame is challenged. The q*-coupled run (#30 f-row w_thth door) is
   the one place cross-sector angular stiffness could enter and must be
   included.

5. **Self-consistency vs frozen-f.** W4/W5 mostly froze f (quasi-static).
   A genuine cell is self-consistent (f back-reacts on w-gradient,
   w4a D2). The coupled system marches only on trust windows (full-domain
   collapse is a seal-margin artifact, VB4); the SEAL region itself is not
   resolved by the bulk solver — the fold closure (ii.3) is imposed as a
   BC, and whether the imposed mirror BC is the metric's own demand is
   itself open (the crease fork, W2). Over-reliance on frozen-f or on a
   stand-in seal BC could manufacture or destroy "stability" artificially.

6. **Mechanism genuinely open (a feature, but an under-determination for
   the solver).** Static vs breather is not pre-decided; the solver must
   search both, and a cell stable as a breather but not static (or vice
   versa) is a legitimate, expected outcome that the spec must keep
   distinct in the catalog.

7. **Convention bookkeeping (member-unit kappa).** kappa_banked =
   kappa_true c_member/2 (registry #29 erratum); the band-edge ratio is
   convention-graded (Newton-basin 1.84 vs dynamic ~2.12). Phase B must
   carry true units (c = 2) and the subtracted species force, or it will
   re-import the W4-B convention defect.

END W8 PHASE-A. The problem is stated; Phase B (GPU) can execute from
(vi) directly. All kappa != 0 / time-dependent content is HYPOTHESIS-
GRADE; verifier-before-record and Charles-canonization bind any positive
catalog claim.
