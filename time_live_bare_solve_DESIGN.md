# Time-Live Bare-Metric Solve — BUILDABLE DESIGN (no compute)

Date: 2026-06-18. Driver: Claude (Opus 4.8, 1M). MODE = DESIGN/SCOPE ONLY
(no solve run, no long compute; tiny feasibility checks at most). DATA-BLIND.
Category-A discipline (borrow GR numerics for TRACTABILITY only, never to impose
physics). Frame: whole_metric_bare_solve_MAP.md + CANON C-2026-06-18-1
(relativistic bare metric form) + C-2026-06-10-2 (finite mirrored cell).
Owner decision honored: KEEP TIME ALIVE (a time-live / dynamical solve, NOT a
frozen static snapshot). Brought to Charles for check BEFORE anything is built.

This document changes nothing committed. It is a plan, not a result.

---

## 0. THE TARGET (restated, frozen)

Find PERSISTENT TIME-LIVE self-gravitating solutions of Einstein's equations on
the FINITE MIRRORED CELL (seal = same-minus / time-reversal mirror fold = a
REFLECTING boundary), holding the C-2026-06-18-1 relativistic structure
(exponential dilation law + B=1/A reciprocal tie along grad phi), with NOTHING
external in the matter slot (the only energy is the metric's OWN content).
Misner-Sharp energy is READ OFF the result. Observe what structure emerges; name
nothing in advance.

Physical object designed-for: a SELF-GRAVITATING STANDING WAVE — a breathing or
spinning cavity mode of pure geometry. Open-space pure-gravity geons radiate and
die; the reflecting seal lets the radiation return so a standing-wave mode can
persist. No matter field.

---

## 1. THE FORMULATION (item 1 — RECOMMENDED)

### 1.1 The unknown functions

Coordinates (T, r, theta, psi) on the finite cell r in [0, R_seal]. Metric kept
in the C-2026-06-18-1 form along the dilation-gradient direction and FREE
everywhere else (the MAP's HELD/FREE split is binding):

- HELD: g_TT = -e^{-2 phi} c^2 and the reciprocal tie B = 1/A along grad phi,
  i.e. g_TT g_rr = -c^2. phi = phi(T, r, theta, psi), defined up to an additive
  constant (gauge, R1).
- FREE (the solution space, NOT smuggled): the angular/transverse block (the
  r^2 dOmega^2 form is a CHOICE), all off-diagonal/shift terms (g_Tr, g_Tpsi =
  rotation/frame-dragging, and spatial off-diagonals), and the TIME-dependence.

So the unknowns are: phi (radial dilation potential) + the transverse-block warps
{a_theta, b_psi, ...} + the shift/off-diagonal fields {g_Tr, g_Tpsi, ...}. The
matter slot is empty: the ONLY field content is the metric itself. There is no
Theta, no n_a, no xi/kappa here — the L2+L4 angular matter Lagrangian is
EXCLUDED. (This is the load-bearing difference from every prior soliton solve and
is exactly why the scale question in section 5 is sharp.)

### 1.2 The equations

1. Einstein, source-free: G_{mu nu}[g] = 0 (vacuum; the only energy is the
   geometry's own dynamical content carried in the off-diagonal/time-derivative
   terms — the geon mechanism, candidate (b) of the MAP).
2. The held tie: g_TT g_rr = -c^2 enforced as a constraint along grad phi
   (per C-2026-06-18-1 the Einstein identity G^t_t - G^r_r = -(AB)'/(r A B^2)
   then vanishes identically — the tie is consistent, not over-determining).
3. The seal reflecting BC at r = R_seal: the same-minus involution
   sigma:(fields) -> (-fields with time-reversal T -> -T). Coded as the derived
   PARITY rule (w7_a_mirror_bc.py, already on paper): sigma-EVEN fields get
   Neumann at the seal, sigma-ODD fields get Dirichlet at the seal. Because sigma
   is a TIME-REVERSAL on the time-row content (f_T -> -f_T), the parity rule maps
   directly onto the TIME-HARMONIC parity (see 1.4) — the reflecting wall is what
   makes a standing mode possible.
4. Regularity at the core r -> 0 (and the canon phi -> -infinity core endpoint
   for the inside-out matter cell, C-2026-06-10-2): r=0 regularity forces only a
   node condition, not a value — keep it as a regularity row, not a chosen value.
5. Periodicity in time: all fields periodic with period 2 pi / omega, omega a
   FREE unknown to be solved for self-consistently. STATIC is the omega -> 0
   special case and MUST be contained (the solve can return static if preferred).

### 1.3 Posing: (a) nonlinear eigenvalue problem for omega — RECOMMENDED

Three candidate posings:

- (a) NONLINEAR EIGENVALUE PROBLEM for omega (cavity modes): solve for a
  self-consistent metric oscillating with period 2 pi / omega; omega is the
  eigenvalue, the mode shape is the eigenvector, fully nonlinear (NOT linearized
  about static). The seal reflecting BC + regularity + periodicity quantize the
  admissible omega.
- (b) time-periodic boundary-value problem: same content, posed as a BVP on the
  space-time slab [0, 2pi/omega] x cell with periodic-in-T faces.
- (c) full forward time-evolution (NR Cauchy march): the most general, the
  hardest, no periodicity assumed.

RECOMMENDATION: pose as (a), a nonlinear eigenvalue problem for omega,
implemented via HARMONIC BALANCE (Fourier-in-T truncation, 1.4). Reasons:
- It is the LEAST-SMUGGLING form of "time alive" that still yields a clean,
  well-posed, tractable problem: a free omega with static contained as omega -> 0.
- It matches the persistent-standing-wave object we are designing for (a cavity
  mode is by definition a self-consistent periodic orbit), and the reflecting
  seal is precisely the BC that makes such modes discrete.
- (b) is mathematically the same content; (a)'s eigenvalue framing makes the
  central physics question — WHAT PINS omega — the explicit output, which is what
  the validity gate (section 5) must interrogate.
- (c) is the honest most-general route and the eventual goal, but it is NR-grade
  (section 6); we build TOWARD it and use it as the relax-and-test on the
  periodicity choice, not as the first pass.

Note (a) and (b) are the SAME object viewed two ways; harmonic balance turns the
time-periodic BVP into a coupled set of spatial BVPs for the Fourier-in-T
harmonics, with omega entering nonlinearly — i.e. a genuine nonlinear eigenvalue
problem. We solve that.

### 1.4 Harmonic balance (the concrete time discretization)

Expand every field in time harmonics of the unknown omega:
  f(T, x) = sum_{k=0}^{K} [ f_k^c(x) cos(k omega T) + f_k^s(x) sin(k omega T) ].
- k=0 is the static background (so static is literally the K=0 / omega->0 limit —
  static contained by construction).
- The seal time-reversal parity selects which harmonics survive for which field
  (sigma-even fields keep cos / even-k structure; sigma-odd keep sin / odd-k) —
  the w7 parity rule ported to T-harmonics. This is the reflecting-wall standing
  condition made algebraic.
- Substituting into G_{mu nu}=0 and projecting onto harmonics (Galerkin/collocation
  in T) gives (2K+1) coupled spatial systems for the harmonic amplitudes, with
  omega as the extra scalar unknown closed by an amplitude-normalization /
  phase-fixing row. Truncation order K is a CHOICE with a convergence test
  (section 4).

This is the standard breather/time-periodic technology (section 2) and it reuses
the repo's existing spatial spectral machinery essentially unchanged — only the
T-axis and the time-row metric terms are new (section 3).

---

## 2. THE CORPUS MINE (item 2 — borrow for tractability only)

| GR / numerical method | Fit | Why |
|---|---|---|
| Gravitational GEONS (Brill-Hartle / Wheeler self-trapped EM-or-grav waves; modern Choptuik-Pretorius-type time-periodic gravitational geons) | STRONG | This is exactly "self-gravitating standing wave, no matter." The modern construction IS a nonlinear eigenvalue solve for the geon frequency. Borrow the construction logic; the matter slot stays empty (our energy is purely geometric dynamical content). |
| AdS time-periodic / "boson-star-without-the-boson" cavity solutions (the AdS box as a reflecting cavity; gravitational breathers; islands of stability) | STRONG | AdS gives a reflecting cavity that confines radiation so periodic gravitational solutions exist — the SAME persistence mechanism as our seal. Borrow: the reflecting-wall-makes-discrete-frequencies framing and the harmonic-balance machinery. We borrow the CAVITY method, NOT the AdS cosmological-constant physics (category-A). |
| HARMONIC BALANCE / Fourier-in-time spectral methods (breather and time-periodic-solution literature) | STRONG — chosen | Turns the periodic problem into coupled spatial BVPs + a frequency eigenvalue. Cleanest fit to our existing spatial spectral engines. |
| Boson-star solvers (frequency-omega ansatz e^{-i omega t}, nonlinear eigenvalue for omega) | MODERATE | The omega-as-eigenvalue mechanics and the seed/continuation discipline port directly. But a boson star's omega is pinned by the SCALAR FIELD MASS — we have no such field. Borrow the numerics; the absence of their scale-setter is precisely our crux (section 5). |
| Newton-Kantorovich / Gauss-Newton + pseudo-arclength CONTINUATION | STRONG | Continue from omega=0 (static seed) into omega>0; trace the solution branch; detect bifurcations (where structure would appear). The repo already has the LM/Gauss-Newton driver. |
| Numerical Relativity full Cauchy evolution (BSSN / generalized-harmonic) | RESERVE | The honest most-general route (posing (c)); genuinely NR-grade. Reserve as the relax-and-test on periodicity and the fallback if harmonic balance cannot close (section 6). We do NOT start here. |
| Spectral-in-space (Chebyshev_r x Gauss-Legendre_theta x Fourier_psi) | STRONG — reuse | The repo's existing basis; reuse as-is for the spatial part of each harmonic. |

Methods deliberately NOT borrowed: any that import a matter field or a fixed
background to set the frequency (would smuggle a scale and defeat the whole test).

---

## 3. REUSE vs BUILD-NEW (item 3)

Verdict from infrastructure recon (agent af00692770e806119): EVERY committed
full-Einstein solver is STATIC (d_T = 0 hard-wired). No committed time-periodic
coupled-Einstein solve exists anywhere. The geometry kernels are reusable; the
time machinery is the build.

### REUSE essentially as-is
- whole_metric_3d_core.py — general 4x4 Christoffel->Einstein kernel. CRITICAL:
  its derivative array dg[...,k,m,n] ALREADY has a k=t slot; every current caller
  zeroes the t-row. We simply supply d_T g != 0. Single most reusable piece.
- spectral_cheb.py, spectral_sph.py (Chebyshev interval + Clenshaw-Curtis;
  theta Gauss-Legendre; psi Fourier) — spatial discretization of each harmonic.
- einstein_3d_eval.py (einstein_mixed_weyl) — pole-stable analytic Einstein for
  the diagonal block; use for diagonal-class first passes.
- full3d_solver.py — matrix-free + dense Gauss-Newton/Levenberg-Marquardt driver
  (dense_lm_solve, lm_solve with autograd JVP/VJP). Reuse the driver; extend the
  residual vector with time-row rows.
- Misner-Sharp readouts — BOTH the source-integrated form (radial_Bfree_soliton.py
  ~L280) and the metric-deficit form m = r(1 - e^{-2phi}) (whole_metric_3d_gate.py
  ~L235). Reuse the deficit form as the primary READ-OFF (no source here).
- radial_Bfree_soliton.py converged static soliton AND/OR the bare static
  closure (Registry #33 continuum) — the obvious SEED = the k=0 zeroth harmonic.
- The w7_a_mirror_bc.py / wcc_closed_cell.py PARITY CLASSIFICATION (sigma-even ->
  Neumann, sigma-odd -> Dirichlet; sigma = time-reversal f_T -> -f_T) — derived on
  paper, ports directly as the T-harmonic parity rule.

### BUILD NEW (the time-dependence)
- The TIME AXIS: a Fourier-in-T harmonic basis (harmonic-balance), K+1 cos and K
  sin amplitudes per field; the projection of G=0 onto harmonics.
- The LIVE time-row metric content: g_Tr, g_Tpsi shift/off-diagonal warps (the
  current 3D solver explicitly hard-sets these to zero) and d_T phi terms.
- The G^t_mu RESIDUAL ROWS (current residual has only spatial off-diagonal Einstein
  rows; the time-momentum constraints G^t_r, G^t_psi and the time-evolution
  rows are absent).
- The omega EIGENVALUE closure: the extra scalar unknown + its normalization/
  phase-fixing row (and a Newton update that includes d/d omega).
- The CODED TIME-MIRROR seal BC: parity on the T-harmonics (even/odd-k for
  sigma-even/odd fields) — never implemented before, but the rule is already
  derived.
- Continuation in omega from the static (omega=0) seed.

The existing 1-D time machinery (dyn1_evolve_implicit.py = robust implicit
trapezoidal; ns_scan_evolve.py = leapfrog radial) is REUSE-FOR-CROSS-CHECK only:
it evolves a single reduced field on a frozen-FORM metric, not the coupled
periodic Einstein system. Use it to validate that a found periodic mode actually
persists under forward evolution (a relax-and-test on the periodicity choice).

---

## 4. THE CHOICE-LEDGER (item 4 — every reduction tagged, with relax-and-TEST)

| Reduction (first tractable pass) | tag | relax-and-TEST plan |
|---|---|---|
| TIME-PERIODIC (free omega) rather than full forward evolution | CHOICE | Relax to forward Cauchy evolution (pose (c), reserve NR) on a found mode; TEST that the periodic mode persists (does not radiate away) under evolution. If it decays, the seal does not confine it / periodicity was wrong. |
| Time itself is an INTERVAL [0, 2pi/omega] with periodic faces (not literally closed/cyclic time) | CHOICE (the closed-time hinge — Charles, sec 7) | TEST by comparing periodic-BVP vs an explicitly closed-time identification of the T-faces; do the spectra differ? This is a framing fork for Charles, not just a numeric. |
| Harmonic truncation order K (start K=1: background + first harmonic) | CHOICE | Increase K (1->2->3...); TEST omega and mode-shape convergence; report the K at which omega stabilizes. A mode that needs large K is strongly nonlinear (informative, not disqualifying). |
| SPHERICAL symmetry for the first pass (theta-, psi-independent; breathing-only) | CHOICE (NOT a consequence — C-2026-06-18-1) | TEST by adding a theta-harmonic / a g_Tpsi shift (spinning mode) and checking whether the spherical branch is stable to / connected with non-spherical branches. Per the carrier audit (STATE 2026-06-18) the angular block is exactly where native structure may live — so spherical-first is a tractability scaffold to be removed early, not a resting place. |
| DIAGONAL metric (no off-diagonal/shift) for the very first pass | CHOICE | TEST by turning on g_Tr then g_Tpsi (the geon / frame-dragging content of candidate (b)); a pure-diagonal breather may be trivial precisely because candidate (b) needs the off-diagonal dynamical content — so this relax is physically load-bearing, do it second. |
| AREAL radius (rho = r chart) | CHOICE (a chart; theorem only under macro anchoring) | TEST chart-independence of any emergent feature (curvature concentration, omega) under a chart change. |
| Grid: Chebyshev_r N_r x (theta Gauss-Legendre) x Fourier_psi x Fourier_T | category-A | Convergence/conditioning checks only (section 5); never physics. |
| R_seal value (the physical cell size) | CHOICE at the size level (Registry #32: absolute scale is a proven FREE one-parameter family) | THE central test (section 5): relocate R_seal and watch omega. This is the box-control gate, not a convenience. |

Explicit answer to the spatial-symmetry question: NO spatial symmetry is forced;
spherical + diagonal are tractability scaffolds for pass-1, both flagged CHOICE,
both with an early relax-and-test, and the angular/off-diagonal relax is
PHYSICALLY load-bearing (it carries candidate (b)'s geon energy and the carrier
audit's native-structure suspect), so it is scheduled second, not deferred
indefinitely.

---

## 5. THE VALIDITY GATES (item 5 — the load-bearing section)

### 5.1 THE BOX-CONTROL GATE (the key validity question — do NOT hand-wave)

Recon (agent ae10d61bb5698ccd4) establishes the hard fact: in the BARE
source-free metric (C-2026-06-18-1: exponential dilation + B=1/A, matter slot
empty) there is NO intrinsic dimensionful scale.
- phi-differences are dimensionless and gauge-defined-up-to-a-constant; the
  exponential law is a pure number.
- Registry #32 (theorem-grade): under r->lr, M->lM, t->lt every closure is
  rescale-invariant; absolute size is a proven FREE one-parameter family.
- Registry #33: the bare static closure is a CONTINUUM in compactness X, not
  discrete. ln(1101) is a FREE dimensionless cosmological anchor, not a scale.
- The one intrinsic length the program ever produced, sqrt(kappa/xi), comes
  ENTIRELY from the angular MATTER Lagrangian, which is EXCLUDED here.

Therefore the DEFAULT expectation is that any cavity frequency will be pinned to
the wall, omega ~ 1/R_seal — i.e. box-controlled in exactly the Registry #1 / W7
/ #44 / CS4 sense (CS4 already found a LINEARIZED time-row rest-clock mode on the
static soliton is box-controlled: omega^2 ~ 1/R^2, Neumann AND Dirichlet,
M_MS-independent). We are NOT re-walking CS4: we run the FULL NONLINEAR
NONSTATIONARY solve (where the time derivative f_T enters genuinely), with the
linearized box-control as the PRE-REGISTERED FOIL. CS4's CONDITIONS-CHANGED
reopener is precisely "full nonstationary solve; corrected S^2 carrier;
production resolution" — this design.

The gate (pre-registered, three criteria; a PASS requires all three):
1. NO 1/R scaling: omega must NOT scale as 1/R_seal. Equivalently omega * R_seal
   must NOT be bounded as R_seal grows; for a box mode omega*R -> const, for a
   physical mode omega*R -> infinity (does not collapse to continuum).
2. WALL-RELOCATION INVARIANCE: omega (and any emergent curvature/energy
   concentration) must be STABLE under relocation of the seal/outer boundary.
   The historical diagnostic threshold: box artifacts moved 394-1152% under
   relocation; genuine structure (weld-jet-tied ladder) moved <= 2.3%. Adopt
   "< few %" as PASS, "tens of % or more" as box-artifact.
3. INTRINSIC LOCK: omega must track an INTRINSIC dimensionful quantity, not the
   cell size. CANDIDATE LOCKS to test for (the live hypotheses for what a
   nonlinear nonstationary mode could lock onto, none guaranteed): the SELF-
   CONSISTENT AMPLITUDE of the mode (a nonlinear breather's frequency-amplitude
   relation omega(A) — genuinely absent from the linearized CS4 problem), or a
   self-trapping radius set by the mode's own energy (the geon mechanism,
   candidate (b)), or a closed-time periodicity condition. If omega depends ONLY
   on R_seal and on nothing intrinsic, it is box-controlled — record it as a
   reproduction of #1/#44/CS4, NOT a physical result.

HONEST PRIOR (stated up front, not after a residual): on present canon there is
NO bare-metric quantity for a frequency to lock onto, so the most likely outcome
is box-control again. A PASS would therefore be a genuinely NEW structure — most
plausibly from the nonlinear amplitude-frequency relation or the off-diagonal
geon content, NOT from the diagonal linearized-background mode. We design to
DETECT either verdict cleanly; we do not target the pass.

### 5.2 STATIC (omega -> 0) LIMIT RECOVERY
The K=0 harmonic / omega->0 limit MUST reproduce the known bare static closure
(Registry #33 continuum) and, with the static soliton seed, the
radial_Bfree_soliton result. A solve that cannot return static is broken.

### 5.3 ANALYTIC / KNOWN-LIMIT CHECK
- Flat limit: phi -> const must give Minkowski; G=0 exactly.
- Known-geon / linear-wave limit: at small amplitude the nonlinear breather must
  reduce to a linear standing gravitational wave in the cavity with the expected
  cavity-mode frequency (which, per 5.1, is the box mode omega~1/R) — i.e. the
  SMALL-AMPLITUDE limit should REPRODUCE CS4's box-controlled mode. This is a
  positive consistency requirement (our foil is the correct linear limit) AND it
  means any departure from box-control MUST appear at FINITE amplitude — sharpening
  exactly where to look.

### 5.4 CATEGORY-A CONDITIONING CHECKS
- Spectral convergence in N_r, N_theta, N_psi, K (exponential for smooth modes).
- Per-batch CPU asserts on every GPU eigensolve (the known V100/cu121
  solve_triangular broadcast-corruption pitfall — use explicit inverse + batched
  matmul, CPU spot-checks).
- Constraint-residual monitoring: G^t_mu momentum constraints must stay at
  machine zero along the solution (a constraint-violating "solution" is numerics,
  not geometry).
- Einstein-residual gate (the existing radial_Bfree_validate.py / whole_metric
  gate discipline) extended to the time rows.

---

## 6. TRACTABILITY HONESTY (item 6)

### Feasible to build/run now
- The harmonic-balance pose (a) at K=1, SPHERICAL + DIAGONAL, on the existing
  spectral spatial grid, seeded from the static soliton, continued in omega from
  0. This reuses ~80% of existing code; the genuinely new pieces are the T-Fourier
  projection, the omega closure row, and the time-mirror parity BC. This is the
  smallest honest first pass that KEEPS TIME ALIVE. Estimated build: moderate
  (days), runtime small (GPU eigensolves are ~14ms/1024^2 batched).

### Genuinely NR-grade-hard
- Full forward Cauchy evolution (pose (c)): BSSN/generalized-harmonic on the cell
  with a reflecting time-mirror seal — gauge choice, constraint damping,
  well-posedness of the reflecting BC, long-time stability. This is the honest
  most-general route and is hard; reserve it.
- The FULLY-FREE periodic solve (all 10 components live, no symmetry, large K):
  the off-diagonal time-row coupling + many harmonics is a large nonlinear
  eigenvalue system; tractable but heavier (the angular + shift relax of section 4).

### Where it might be intractable, and the fallback
- RISK A (TOP RISK — physics, not numerics): the bare problem may have NO physical
  frequency to find, so the solve returns ONLY box-controlled modes (section 5.1
  prior). Then time-live on the BARE metric is trivial-or-box, and the honest
  conclusion is that persistent structure requires either the matter/angular
  sector back IN (the carrier object, not bare) or the closed-time identification
  to supply the missing scale. FALLBACK: this is itself a clean, informative
  result (candidate (c) of the MAP: structure is not in the bare time-live diagonal
  mode) — record it scoped, do not patch a scale in.
- RISK B: harmonic balance fails to converge (strongly nonlinear, needs large K,
  or no periodic orbit exists). FALLBACK: short-time forward evolution
  (dyn1_evolve_implicit-style, extended) to test persistence directly, then NR
  reserve.
- RISK C: the reflecting time-mirror BC is ill-posed for evolution (common for
  reflecting BCs in NR). FALLBACK: keep it as a parity constraint in
  harmonic-balance (where it is algebraic and well-posed) and only attempt
  evolution as a cross-check.

### Phased build order (smallest honest first pass -> grow)
- PHASE 0 (feasibility, tiny compute OK): confirm whole_metric_3d_core accepts a
  nonzero d_T g and returns finite G; wire the static soliton as the k=0 seed;
  check the omega->0 limit reproduces static. No physics claim.
- PHASE 1 (the first time-live pass): K=1, spherical, diagonal, free omega,
  continued from omega=0. Run the box-control gate (5.1) immediately. This alone
  decides RISK A for the diagonal sector.
- PHASE 2: turn on the off-diagonal/shift time-row content (g_Tr, g_Tpsi) — the
  geon mechanism candidate (b); re-run the gate. This is where a nonlinear /
  amplitude-locked frequency could first appear.
- PHASE 3: relax spherical (add theta-harmonics / spinning modes) — the
  angular-block native-structure suspect.
- PHASE 4 (reserve): full forward evolution as the periodicity relax-and-test.

A null at Phase 1 does NOT end the program (orchestra principle): it scopes the
DIAGONAL time-live mode as box-or-trivial and routes to Phases 2-3.

---

## 7. OPEN DESIGN DECISIONS FOR CHARLES (item 7 — lay-statable)

1. PERIODIC vs EVOLUTION (the first-pass framing). We propose to start by looking
   for solutions that REPEAT with a free rhythm (a self-consistent breathing/
   spinning mode), with "frozen/static" included as the no-rhythm special case.
   The fully general alternative is to let the geometry just run forward in time
   and watch — far harder (full numerical-relativity grade). We recommend
   periodic-first, growing toward forward-running later. OK to start periodic?

2. IS TIME CLOSED, OR AN INTERVAL? (the closed-time hinge.) A repeating solution
   can mean two physically different things: (i) time is a finite LOOP that closes
   on itself (closed time — the long-standing seal/closed-time hinge), or
   (ii) time is an ordinary stretch that we happen to make repeat at its two ends.
   These can give different spectra. Which does Charles intend the seal's
   time-reversal mirror to mean? This is a framing call, not a numeric one, and it
   may BE the missing ingredient that pins the rhythm (section 5.1 candidate).

3. THE BOX-CONTROL VERDICT, ACCEPTED IN ADVANCE. Honest prior: with nothing in the
   matter slot, the bare geometry has no built-in size, so the most likely outcome
   is that the breathing rhythm is set ENTIRELY by the cell wall (an artifact of
   where we put the wall, not real physics). We have designed a clean three-part
   test to catch this. Does Charles accept that a "rhythm = wall artifact" outcome
   is a legitimate, recordable result (it would say persistent structure needs the
   matter/angular sector back in, or closed time), and NOT something to be rescued
   by inserting a scale by hand?

4. SPHERICAL/DIAGONAL SCAFFOLD vs ANGULAR FIRST. We propose a spherical, diagonal
   first pass for tractability, then turn on the angular and rotational content
   (where the recent carrier audit suggests native structure actually lives).
   Acceptable to scaffold this way, or does Charles want the angular content live
   from the start (more expensive, but closer to the suspected home of structure)?

5. MATTER SLOT STAYS EMPTY — confirm. This solve deliberately EXCLUDES the angular
   L2+L4 matter Lagrangian (and hence its scale sqrt(kappa/xi)). That exclusion is
   what makes the box-control question sharp. Confirm the intent is the PURELY
   geometric content (a true geon test), with the matter sector a separate later
   study — not to be quietly reintroduced to manufacture a frequency.

---

## ATTACK HERE (for a later DESIGN verifier)

A blind adversarial verifier of THIS DESIGN should attack:

- SMUGGLE CHECK on the formulation (item 1): does the time-periodic / harmonic-
  balance pose covertly impose a structure that should be free? Specifically: does
  fixing the time-mirror parity (sigma-even->Neumann etc.) over-constrain the
  T-harmonics in a way that PRE-SELECTS a frequency (smuggling the answer)? Is
  static genuinely contained as omega->0, or is the omega-eigenvalue framing
  unable to return omega=0 (which would mean static is excluded, not contained)?
- SCALE SMUGGLE: trace every dimensionful quantity entering the numeric solve.
  Confirm NO scale other than R_seal enters (no hidden xi/kappa, no hidden
  c/G-derived length, no grid spacing masquerading as physics). If any intrinsic
  length sneaks in, the box-control gate is compromised.
- HELD/FREE FIDELITY: is B=1/A enforced ONLY along grad phi (not transverse, per
  the C-2026-06-18-1 caveat P8)? Are the angular block and off-diagonals genuinely
  free, or quietly diagonalized?
- GATE ADEQUACY (item 5.1): are the three box-control criteria jointly sufficient
  to distinguish a physical frequency from an artifact, or could a box mode pass
  one of them spuriously? Is the wall-relocation test run at FIXED physical content
  (so relocation does not also change the seed)?
- CS4 NON-REPETITION: confirm the design's small-amplitude limit REPRODUCES CS4's
  box mode (it should — that is the correct linear limit) AND that the design's
  novelty (a departure from box-control) is sought only at FINITE amplitude /
  off-diagonal content where CS4 did not look. If the design's only regime is the
  linearized one, it IS CS4 and must be flagged.
- TRACTABILITY HONESTY (item 6): is Phase 1 actually buildable from the claimed
  reusable pieces, or does the "build new" list hide an NR-grade dependency
  (e.g. is the reflecting time-mirror BC well-posed enough for the harmonic-balance
  Newton solve to converge)?
- ORCHESTRA / NULL HANDLING: is a Phase-1 null correctly scoped (diagonal time-live
  mode box-or-trivial) rather than over-read as "time-live fails"?

## STATUS
DESIGN only. No solve run. Awaiting Charles's check + the five open decisions
(section 7). Nothing committed changed by this document.

---

## DECISIONS LOCKED (Charles, 2026-06-18) — all Einstein-grounded

- OPEN TIME (interval, NOT a closed loop). Einstein-orthodox (loops = causality violation,
  excluded). A rhythm needs NO time-loop (a pendulum beats on open time). => the "closed-time"
  thread is DROPPED; we look for persistent periodic motion on ordinary open time.
- RHYTHM-FIRST: solve for a free oscillation frequency omega; STATIC = the omega->0 case is
  CONTAINED, not excluded. Full forward-evolution (NR-grade) held in reserve. Grounded in
  Einstein: isolated gravity RADIATES (no persistent open-space lump); a REFLECTING cavity
  (the seal) traps it into a persistent standing-wave => rhythm is the physically-pointed target.
- SHAPE / ANGULAR METRIC CONTENT LIVE EARLY (not scaffolded round-first; "round" is a smuggled
  symmetry). Phased build for tractability, every reduction tagged + relax-and-tested. NB this is
  the METRIC's own angular DOF (gravity), NOT a matter field.
- MATTER SLOT EMPTY, but BARE-FIRST: the self-gravitating "mass background" is gravity's OWN
  motion + shape energy (a Wheeler GEON; vacuum, no matter — pure Einstein). IF nothing persistent
  forms, that IS Einstein saying a mass background is required => THEN add ONLY UDT's NATIVE
  (metric-derived) matter, as a gated second step. Never external matter.
- SCALE HANDLING (binding, Charles 2026-06-18): bare gravity is SCALE-INVARIANT (Einstein
  vacuum theorem) => it yields RATIOS + SHAPES, NOT an absolute size. The absolute scale enters
  from ONE external observation = the CMB temperature / dilation-depth anchor (7.004 = ln(1+z_CMB)),
  admitted ONLY IF the metric is shown to ALLOW it (a consistency the geometry passes), NEVER
  hand-inserted. STRETCH GOAL: the whole-metric closure DERIVES the anchor (predicts z_CMB) — the
  critical-universe determines-vs-relates bet. A "rhythm = box size" / scale-free outcome is a
  LEGITIMATE recordable result (the physics is in the ratios), NOT to be patched with a hand-scale.

STATUS: decisions locked; design pending a blind faithfulness red-team, then Phase-0 build.

---

## RED-TEAM REVISIONS ADOPTED (2026-06-18, verifier ac721580ce18bc99c; Charles: go)

Verdict was REVISE-FIRST. Frame + all DECISIONS-LOCKED survive; these are technical fixes:
1. *** BIRKHOFF ***: the ROUND (spherical) + diagonal + vacuum class is STATIC BY THEOREM —
   the vacuum momentum constraint gives G_Tr = 2 d_T(phi)/r, so G_Tr=0 => d_T phi = 0. UDT's
   B=1/A tie IS Schwarzschild's AB=1 (no extra DOF), so Birkhoff stands. => a round empty cell
   CANNOT have a rhythm. C-2026-06-13-1's "diagonal sector propagates in T" does NOT rescue it
   (that carried the L2+L4 MATTER source; empty => gone). CONSEQUENCE: "round" and "static" are
   the SAME trap (round forces static). Structure (a vacuum geon) can ONLY live in the NON-ROUND
   class: quadrupole (l>=2) and/or rotation (off-diagonal g_Tpsi, frame-dragging). => Phase-1 is
   the NON-ROUND solve; the round/diagonal case is demoted to a static/gauge SANITY CHECK only;
   the box-control gate is only meaningful at Phase 2/3 (non-round).
2. TIME-MIRROR BC: do NOT let the SPATIAL seal parity (Neumann/Dirichlet at the wall) dictate
   which TIME-harmonics (cos/sin) survive — they are independent axes; tying them can pre-select
   omega (a smuggle). Impose only the spatial wall BC; keep the full cos+sin (free-phase) harmonic
   content; let the eigenvalue solve quantize omega honestly.
3. SOLVER: commit to explicit-Jacobian dense Newton + pseudo-arclength continuation
   (full3d_newton.py lineage). The matrix-free Jacobi-PCG is KNOWN to stall (CG step not a descent
   direction) — NOT a fallback.
4. PHASE-0 (re-targeted): (a) symbolically CONFIRM + BANK Birkhoff (round+diagonal+vacuum =>
   d_T phi=0); (b) show the MINIMAL non-round extension (g_Tpsi rotation and/or l>=2) ESCAPES
   Birkhoff (the constraint no longer forces d_T=0) => time-life is possible there; (c) feasibility:
   the committed Einstein kernel accepts a live time-derivative slot + omega->0 returns static.

STATUS: revisions adopted; Phase-0 build STARTED (Charles: go).
