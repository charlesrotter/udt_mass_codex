# Phase-1 Results — Bare Time-Live Whole-Metric Solve (the non-round l=2 vacuum geon)

Date: 2026-06-18. Driver: Claude (Opus 4.8, 1M). MODE = OBSERVE (report what is there;
no result forced). DATA-BLIND (no mass/ratio/wall numbers; sizes in units of the cell
radius R_seal only). Category-A (GR numerics borrowed for tractability ONLY; no physics,
no matter, no scale imposed). Frame: time_live_bare_solve_DESIGN.md (DECISIONS-LOCKED +
RED-TEAM-REVISIONS) + phase0_time_live_results.md (Birkhoff bank + l=2 physical-GW finding
+ kernel feasibility) + CANON C-2026-06-18-1 (held metric structure) + C-2026-06-10-2
(finite mirrored cell + seal).

Scripts (all NEW, prefix phase1_; nothing committed changed):
- phase1_master_reduce.py / phase1_master_project.py -- l=2 master operator reduction (1a/1b)
- phase1_spectrum.py -- 1a gates + 1b linear spectrum (Chebyshev + GPU batch)
- phase1_core_regularity.py -- the two core-BC premises laid side by side (1b)
- phase1_geon_zerilli.py -- the clean full {H0,H1,H2,K} Zerilli master (1c)
- phase1_geon_check_warp.py -- shows the naive single-warp ansatz is over-constrained (1c)
- phase1_geon_backreact.py -- exact O(A^2) GW-stress backreaction source (1c)
- phase1_geon_solve.py -- dense-Newton + pseudo-arclength amplitude continuation (1c)
- phase1_geon_boxtest.py -- the box-control-at-finite-amplitude test (1c)
- (helpers) phase1_geon_reduce.py / phase1_geon_reduce_fast.py / phase1_geon_coeffs.py

---

## THE THREE-OUTCOME VERDICT: OUTCOME B (box-controlled / scale-free), with a scoped (4).

The bare time-live solve lands in **OUTCOME B of the design**: the bare metric is
scale-free with NO rich structure beyond box geometry. Both the linear spectrum (1b)
and the load-bearing finite-amplitude "escape" claim (1c) are box-controlled. A single
bare l=2 mode additionally does NOT carry a clean positive self-gravitating mass (a
scoped negative). This points, per the design, to closure/CMB-anchor or NATIVE matter
as the gated next step -- NOT to patching a scale by hand.

Single most decisive piece of evidence: the finite-amplitude frequency bend dw/dA^2
scales as 1/R^2 at fixed physical warp amplitude (VIEW3: dw/dA^2 * R^2 = -0.377 flat at
R=1,2,4); the "universal -1.705 * max|phi| law" that appeared to escape box-control is a
normalization tautology -- both (w-w0)/w0 and max|phi| are linear in A^2 at O(A^2) (ratio
A-independent by truncation, not physics), and the R-invariance comes from choosing
max|phi| (itself ~1/R) as the knob, cancelling the 1/R powers by construction. No
intrinsic length exists in the bare problem (the GW-stress source is scale-homogeneous,
length-weight 2 in every term; the only scale is R_seal).

---

## PHASE 1a -- MACHINERY + VALIDATION (the time axis), ALL GATES PASS

Harmonic balance in time wired in: every field f(t,x) = sum_k [a_k(x) cos(k w t) +
b_k(x) sin(k w t)], so d_t -> algebraic factor (k w); static is literally the omega->0 /
k=0 limit (contained by construction). For the linear problem one harmonic k=1 with
frequency w suffices.

KEY BACKGROUND FACT (confirmed symbolically, drives everything): the bare round STATIC
vacuum background holding the UDT tie (g_tt g_rr = -c^2) + core regularity on a finite
cell satisfies 2 r phi' + e^{2phi} - 1 = 0 (the Schwarzschild equation); regularity at
the core forces m=0 => phi = const => **FLAT MINKOWSKI**. The linear l>=2 standing waves
therefore live on a FLAT background -- ordinary linear vacuum gravitational waves
(Regge-Wheeler / Zerilli) confined in a spherical REFLECTING cavity. c=1 throughout.

The l=2 even-parity vacuum master operator (derived TWO ways): the naive single-angular-
warp ansatz from Phase-0 is OVER-CONSTRAINED (phase1_geon_check_warp.py: its trace-Ricci
component 2(2-9cos^2 th)H/r^2 cannot vanish for the profile that solves the traceless
part). The genuine l=2 even-parity vacuum DOF is the FULL Regge-Wheeler/Zerilli set
{H0,H1,H2,K}, which reduces CONSISTENTLY (all 10 dG residuals = 0, NOT over-constrained,
phase1_geon_zerilli.py) to the single master

    -Psi'' + (6 / r^2) Psi = w^2 Psi      (l=2 Zerilli, flat background),  regular sol Psi = r * j_2(w r).

This RESOLVES the Phase-1b core-BC ambiguity in favor of the textbook l(l+1)/r^2 barrier
form (the j_2 ladder), and the verifier independently confirmed both the operator and the
over-constraint of the naive ansatz.

VALIDATION GATES (numbers reported in scripts; all PASS):
- (i)  w->0 returns static: number of eigenvalues with w<1e-4 = 0; the static regular
       solution cannot also satisfy the wall BC nontrivially => no spurious w=0
       propagating mode; w->0 is the clean no-rhythm limit. PASS.
- (ii) flat/linearized limit reproduces the Phase-0 l=2 physical-GW operator: the d_t^2 h
       coefficient and operator structure match Phase-0 G_thth O(eps) exactly (same
       lineage). PASS.
- (iii) round limit reproduces Birkhoff: l=0 carries no centrifugal barrier and is the
       non-radiative monopole (the empty-box 1D ladder), not a confined GW DOF;
       consistent with Birkhoff (round vacuum static). PASS.
- (iv) category-A conditioning: spectral convergence is machine-exact -- w_1..w_4 match
       analytic Bessel zeros to ~1e-13 at N=24, flat through N=160 (spectral accuracy);
       GPU (V100 float64) matches CPU to ~1e-12 on every R_seal row. PASS.

---

## PHASE 1b -- LINEAR MODE SPECTRUM (tag: LINEARIZED-stepping-stone) -> BOX-CONTROLLED

Eigenvalue problem -Psi'' + (6/r^2)Psi = w^2 Psi on r in [0, R_seal], l=2 (l=3,4 also
reported), core regular (Psi ~ r^{l+1}), seal wall: BOTH Dirichlet AND Neumann reported
(red-team revision #2: ONLY the spatial wall BC imposed; spatial-seal parity NOT tied to
time-harmonic parity; full cos+sin content kept; w quantized honestly).

Spectrum (R=1, first 6 modes; numeric = analytic spherical-Bessel zeros to ~1e-10..1e-13):
- l=2 Dirichlet w_n: 5.7635, 9.0950, 12.3229, 15.5146, 18.6890, 21.8539
  ratios w_n/w_1 = 1, 1.5780, 2.1381, 2.6919, 3.2427, 3.7918  (= j_2-zero ratios)
- l=2 Neumann w_n: 3.8702, 7.4431, 10.7130, 13.9205, 17.1027, 20.2720
  ratios = 1, 1.9232, 2.7680, 3.5968, 4.4190, 5.2379
- l=3 Dirichlet ratios: 1, 1.4907, 1.9602, ...; l=4 Dirichlet ratios: 1, 1.4305, 1.8380, ...
- SHAPES: mode n has exactly n-1 interior radial nodes (clean overtone tower; no
  degeneracy splitting, no avoided crossings).

BOX-CONTROL GATE (R_seal relative factors 1,2,4,8):
- 1/R scaling: EXACT. w_n * R is constant across all four boxes to machine precision.
- Ratio drift under wall relocation: 0.0000e+00 %. The ratios are perfectly R-invariant.

READ: Phase-1b is BOX-CONTROLLED -- a featureless 1/R cavity ladder. The scale-free
content (ratios) is fixed but is JUST the spherical-cavity Bessel-zero ladder (the j_2
zeros for l=2). The l label shifts which Bessel order sets the ratios but does NOT make
the spectrum richer than a single-l cavity ladder. This is a GENUINE "no richer
structure" result, not solver-limited (convergence machine-exact at low N; CPU/GPU agree
to 1e-12). Consistent with the banked single-cell-box-controlled negative (Registry
#1/#44/CS4).

---

## PHASE 1c -- THE NONLINEAR GEON (the real target) -> EXISTS, but box-controlled

Formulation: SYMBOLIC O(A^2), exact (sympy), then dense numerical Newton. The periodic
l=2 wave Psi (harmonic balance, k=1) couples to a static l=0 background correction
phi(r) = A^2 F(r) DETERMINED by the time-averaged O(A^2) gravitational-wave stress (the
geon backreaction; NO matter slot -- the only "source" for phi is the wave's own
quadratic content). Cross-verified TWO ways (complex time-average vs explicit real
cos/sin standing wave: identical G_tt source, diff = 0). The backreaction is a clean
Misner-Sharp constraint (rF)' = -(r^2/2) S[Psi] with an exact quadratic GW-stress S[Psi].
Solved with dense explicit-Jacobian LM/Newton + pseudo-arclength amplitude continuation
(NO matrix-free PCG, per design); Chebyshev pseudospectral; core regular branch Psi ~ r^3,
Dirichlet wall Psi(R)=0, F fixed by m(0)=0; amplitude normalized by ||Psi||_2 = A.

WHAT EXISTS (genuine, verified):
- A finite-amplitude self-bound time-periodic standing wave EXISTS and CONVERGES to the
  residual floor (~5e-12..7e-12, N-independent: w(A=0.1)=5.76251612 identical to 8 digits
  across N=60/80/120/160) up to A ~ 0.35. Beyond A ~ 0.5 the branch is HONESTLY
  SOLVER-LIMITED (O(A^2) truncation + single-harmonic + mode spreading), NOT a physics
  null -- flagged ok=False in-script.
- A->0 recovers the Phase-1b linear box value w_0 = 5.7634592 = j_2-zero/R exactly.
- The frequency BENDS with amplitude: leading dw/dA^2 ~ -0.094 (small-A, R=1).
- The bend is GENUINELY backreaction-driven: with phi-dressing of the wave operator OFF,
  w stays pinned at w_0 to 1e-13 for ALL A (the bend is the self-gravity, not numerics).

THE LOAD-BEARING POSITIVE CLAIM -- OVERCLAIMED (refuted by blind verifier):
The headline "(w-w0)/w0 = -1.705 * max|phi|, universal across A and R => escapes
box-control" does NOT hold as physics. It is a normalization tautology:
- "Constant across A" is TAUTOLOGICAL: at O(A^2) both (w-w0)/w0 and max|phi| are linear in
  A^2, so their ratio is A-independent by the truncation, not by physics. (The genuine
  nonlinear content is the DRIFT -1.7052 -> -1.7121 as A grows, not the locked constant.)
- "R-invariant across R=1,2,4" is FORCED BY MODE-SHAPE UNIVERSALITY, not self-binding:
  max|F| ~ 1/R exactly (0.960,0.480,0.240,0.120) and dw/dA^2 ~ 1/R^2 exactly
  (-9.43,-2.36,-0.590,-0.147), so the R-powers cancel in the ratio. -1.705 is a pure
  ratio of two functionals of the R-independent shape; the verifier reproduced -1.70487
  independently at R=1,2,4,8 identical.
- It is RELABELED box-control, not escape: at fixed physical warp the bend still falls as
  1/R (VIEW1) and dw/dA^2 * R^2 is FLAT (VIEW3: -0.377 at R=1,2,4) -- i.e. the bend is
  ~1/R^2, even STEEPER than the linear 1/R law. Choosing max|phi| (itself ~1/R) as the
  knob absorbs the box scaling by construction. No intrinsic length exists (the GW-stress
  source is scale-homogeneous, length-weight 2 in every term; the only scale is R_seal).

EFFECTIVE MASS (scoped negative, verified): the integrated Misner-Sharp mass
m(r) = A^2 r F(r) for ONE bare l=2 mode is SIGN-INDEFINITE -- m(R)/A^2 = R*F(R) = -0.90544
(R-independent, net NEGATIVE); the local density oscillates sign (neg core, pos mid, neg
wall). A single bare eigenmode does NOT carry a clean positive self-gravitating mass. (A
positive finite geon mass plausibly needs a confined/normalizable packet or a mode
ensemble -- consistent with the finite-cell canon and the orchestra metaphor; FLAGGED,
not forced.)

NOTE (verifier-caught, recorded NOT edited per new-work-is-new-files discipline):
phase1_geon_backreact.py prints a closing NARRATION "monotonically growing positive m(R)
=> positive geon mass" that CONTRADICTS its own numeric output (m(R) sign-flipping,
net negative). That comment is FALSE; it integrated at fixed w=1 on an unnormalized mode
(a different, less meaningful quantity than the on-cell eigenmode). The correct mass
read-off is the on-cell eigenmode value -0.905 (sign-indefinite). Do not let the false
comment survive into any record.

---

## PREMISE LEDGER (chose / derived / leading-order)

| Item | tag | note |
|---|---|---|
| Exponential dilation g_tt=-e^{-2phi}, B=1/A tie (c=1) | DERIVED (C-2026-06-18-1, R1/R3+P8) | held structure |
| Vacuum T_munu=0 (matter slot empty) | CHOSE | the bare-first decision (DESIGN, locked) |
| Round static bare background = FLAT (m=0) | DERIVED | Schwarzschild eqn + core regularity on finite cell |
| l=2 even-parity Zerilli master -Psi''+6/r^2 Psi = w^2 Psi | DERIVED | full {H0,H1,H2,K} reduces consistently; naive single-warp REJECTED (over-constrained) |
| Core r->0 regularity Psi ~ r^{l+1} (regular branch) | DERIVED/forced | no value pre-selecting w |
| Seal wall BC (Dirichlet AND Neumann both reported) | CHOSE | ONLY spatial wall BC; NOT tied to time-harmonic parity (red-team #2) |
| Harmonic balance k=1 + DC phi | CHOSE | exact to O(A^2) (k=2 enters only at O(A^4)) |
| phi = A^2 F(r) backreaction (starts at O(A^2)) | DERIVED | O(A^1) tadpole = 0, verified |
| O(A^2) backreaction truncation | CHOSE | the A-independence of the ratio is a CONSEQUENCE of this (tautology), not physics |
| phi-dressing of the wave operator | CHOSE | relax-tested: undressed => zero shift (bend existence robust; precise -1.705 coeff depends on dressing) |
| ||Psi||_2 = A amplitude normalization | CHOSE | the box-"escape" depends on this convention (max|phi| knob) |
| Areal radius (rho = r chart) | CHOSE | chart-independence not separately tested here |

REGIME STAMPS:
- 1a gates / Zerilli master: exact (sympy), flat round vacuum background, l=2 (also l=3,4).
- 1b linear spectrum: exact eigenvalue problem, flat cavity, machine-precision-converged,
  R in {1,2,4,8}. Genuine (NOT solver-limited).
- 1c geon: O(A^2) backreaction (single harmonic, single l=2 mode), dense Newton +
  continuation, converged to floor for A <~ 0.35, R in {1,2,4}; A >~ 0.5 SOLVER-LIMITED.

---

## ATTACK HERE (for a blind verifier)

The 1c claims were ALREADY put through a blind adversarial verifier (agent a190c021f71ada7df,
2026-06-18): geon existence/convergence (STANDS), bend-is-backreaction (STANDS), Zerilli
operator (STANDS, independently re-derived), backreaction source + sign-indefinite mass
(STANDS), and the "-1.705 escapes box-control" headline (OVERCLAIMED -> recorded here as
box-control / OUTCOME B). A further verifier should attack:

- TRUNCATION HONESTY: is the OUTCOME-B verdict an artifact of the O(A^2) single-harmonic
  truncation? At A ~ 0.35 the ratio already drifts -1.7052 -> -1.7121; a multi-harmonic
  (k=2,3...) or higher-order-in-A solve might reveal genuine A-dependence that the O(A^2)
  tautology masks. Push the continuation harder (more harmonics, larger A, finer N) and
  see whether ANY box-invariant intrinsic structure survives at finite amplitude -- or
  confirm the branch terminates (spreads to wall / collapses) with no intrinsic lock.
- THE NORMALIZATION ARGUMENT (C, the crux): re-derive how max|phi| scales with R at fixed
  ||Psi||_2 and confirm the -1.705 R-invariance is the 1/R cancellation (max|Psi| ~ A/sqrt(R),
  max|phi| ~ A^2/R), NOT intrinsic self-binding. Find any normalization-free diagnostic
  (a dimensionless ratio of two intrinsic functionals) that would distinguish a true geon
  from a relabeled cavity mode, and apply it.
- THE SIGN-INDEFINITE MASS: is a single bare l=2 mode the wrong object? Test a CONFINED /
  normalizable packet or a MULTI-MODE ensemble (orchestra principle) for a net-positive
  Misner-Sharp mass before concluding the bare vacuum cannot self-bind. The (4) negative
  is scoped to the SINGLE BARE EIGENMODE premise.
- ROTATION COMPANION (Phase-2): Phase-0 B1 (off-diagonal g_tpsi frame-dragging) was the
  recommended Phase-2/3 spinning companion and was NOT exercised here. A rotating
  (stationary off-diagonal) geon could lock onto a different (angular-momentum) intrinsic
  quantity; the bare-diagonal box-control verdict does NOT cover it.
- l>=3 / mixed-l: only l=2 (with l=3,4 linear ratios) was solved nonlinearly. Mode-mode
  coupling across l (the angular-sector suspect of the carrier audit) was not opened.
- BACKGROUND-FLAT CLAIM: confirm the round static bare background is forced flat (m=0) by
  core regularity -- if a non-flat (m != 0) regular background is admissible under some
  relaxed core condition, the geon sits on a curved background and the analysis changes.

---

## STATUS

Phase-1 COMPLETE. OUTCOME B (box-controlled / scale-free) banked, with a scoped (4)
single-bare-mode no-positive-mass negative. The bare time-live diagonal l=2 vacuum sector
yields RATIOS + SHAPES that are just the spherical-cavity Bessel ladder (box geometry),
no intrinsic-length structure; the finite-amplitude geon EXISTS and converges but its
frequency bend is box-controlled (~1/R^2 at fixed physical warp), the "escape" being a
normalization tautology. Per the DECISIONS-LOCKED scale handling, this is a LEGITIMATE
recordable result -- the physics is in the ratios, NOT to be patched with a hand-scale --
and per the design it routes to: (a) the rotation/off-diagonal companion (Phase-2), (b)
multi-mode/confined-packet ensembles for a positive mass, (c) closure/CMB-anchor for the
absolute scale, or (d) the gated NATIVE-matter step (Einstein saying a mass background is
required). Nothing committed changed. Awaiting Charles.

---

## BLIND VERIFIER VERDICT — 2026-06-18 (verifier agent a955621ebe9538f70): STANDS

Independent driver-level pass (own sympy tensor algebra, own Bessel/quadrature, own scaling
argument; also ran the author solver as cross-check). All five load-bearing claims reproduced.
- C1 CONFIRMS: round static vacuum => Schwarzschild form e^{-2phi}=1-2m/r; core regularity on the
  finite cell forces m=0 => FLAT. The single-warp ansatz IS over-constrained (a non-vanishing trace
  Ricci); the full {H0,H1,H2,K} Zerilli reduction to -Psi''+(6/r^2)Psi=w^2 Psi (Psi=r j_2) is correct.
  Phase-0's "l=2 carries a physical GW DOF" SURVIVES (only the ansatz was incomplete).
- C2 CONFIRMS (strongest): w_n*R = j_2 zeros ANALYTICALLY EXACTLY for all R; single-l Sturm-Liouville
  => degeneracy/avoided-crossings mathematically impossible. Genuinely box-controlled, not solver-limited.
- C3 CONFIRMS: geon exists, converges ~1e-12 up to A~0.35 (A>=0.5 residual-blowup => honestly
  solver-limited, not a null); bend vanishes with self-gravity off => backreaction-driven.
- C4 CONFIRMS (the crux): the "-1.705 universal escape" is a NORMALIZATION TAUTOLOGY (both numerator
  and max|phi| ~ A^2/R, the 1/R cancels by construction); at fixed PHYSICAL warp the bend ~1/R^2
  (steeper box-control); dw/dA^2 * R^2 = const. GW-stress is length-weight-2 in every term => NO
  intrinsic length can appear (structural at O(A^2), not numerical).
- C5 CONFIRMS: single bare l=2 eigenmode has sign-indefinite, net-NEGATIVE self-gravitating mass
  (m/A^2 ~ -0.905 in the ||Psi||=A convention) => carries no clean positive mass.
- (T) clean: data-blind, category-A; the false positive was caught by the author's own internal pass
  (anti-verdict-hunting); solver-limited honestly residual-distinguished from a null.

SCOPE (bankable statement, correctly scoped): the bare DIAGONAL l=2 vacuum geon at O(A^2) single-
harmonic single-l is BOX-CONTROLLED with NO intrinsic length and NO positive mass -- structurally
rigorous at that order. GENUINELY OPEN (the next attacks, NOT closed): multi-harmonic / O(A^4) /
mixed-l / ROTATION (g_tpsi) / multi-mode ensembles / whole-cell closure. NET = OUTCOME B (scale-free),
honest and verified; a single bare standing wave of pure gravity is NOT a particle.
