# RESULTS — The WHOLE-METRIC FULL SOLVE (the honest binary test)

Research record (append-never-edit). Driver: Claude (Opus 4.8, 1M). 2026-06-15.
OBSERVE mode (report WHAT IS THERE; add NO mechanism to coax a result; report whichever
way it falls). Frame + premise ledger: `whole_metric_solve_MAP.md`. DATA-BLIND throughout
(all sizes/masses in units L = sqrt(kappa/xi) = 1; NEVER compared to wall numbers).

This is THE WHOLE-METRIC SOLVE: build the 3-D COUPLED SOLVER for the full unreduced
stationary metric (all 10 components on a (r,theta,psi) grid, B=1/A FREE, off-diagonals
live, NO symmetry imposed), pass the validation gate against the corrected #56 radial
soliton, explore the full 3-D space, and set up the time-periodicity selector.

Scripts (committed with this doc; all run IN-PROCESS / blocking):
- `whole_metric_3d_solver.py` — the 3-D coupled-solver core (grid, full Einstein residual
  via the validated engine, matter stress, masks).
- `whole_metric_3d_gate56.py` — THE VALIDATION GATE against the corrected #56 soliton.
- `whole_metric_3d_newton.py` — matrix-free Newton-Krylov (autograd JVP) on the full
  residual; core/axis freeze; geometry weighting.
- `whole_metric_3d_bifurcation.py` / `_run.py` — the field-equation Jacobian sigma_min
  bifurcation test (matter + off-diagonal sectors).
- `whole_metric_3d_gauge_disambig.py` — gauge-vs-physical disambiguation of the
  off-diagonal near-null directions.
- `whole_metric_3d_persist.py` / `_run.py` — nonlinear persistence test (stable gradient
  descent on ||F||^2 from many 3-D seeds; gauge-invariant non-axisymmetry read-out).
- `whole_metric_time_selector.py` — the breathing (normal-mode) spectrum omega^2(depth)
  and the time-topology selector arithmetic.
- REUSED & VALIDATED (not rebuilt): `whole_metric_3d_core.py` (full-4-D numerical Einstein
  engine, off-diagonal G to ~5e-6), `whole_metric_3d_matter.py` (full T to ~5e-14),
  `radial_Bfree_soliton.py` (the corrected #56 radial soliton, blind-verified).

Blind verifier: see the ATTACK-HERE block at the end (verifier-before-record).

---

## 0. EXECUTIVE SUMMARY (the honest binary read)

- **3-D SOLVER GATE: PASS.** The validated full-4-D engine recognizes the CORRECTED #56
  round soliton (B=1/A free, a,b independent) as a full 3-D Einstein solution: all 10
  components satisfied, the four diagonal equations converging at O(h^2) in the smooth body,
  M_MS reproduced to ~1e-12, B=1/A recovered in the exterior. The off-diagonal residual is at
  MACHINE ZERO (~1e-13) — but this is true BY CONSTRUCTION (a diagonal static metric has an
  identically-diagonal Einstein tensor and the hedgehog stress is diagonal here), so it is a
  consistency check, NOT a demonstration of a nontrivially-coupled solution. (Contrast the
  prior #55 gate, which seeded the OLD #52 B=1/A-IMPOSED soliton and correctly FAILED. The
  corrected soliton passes.)
- **NEW STRUCTURE FROM THE UNREDUCED METRIC: NONE detected.** (i) The matter-sector
  bifurcation operator is bounded away from zero across the depth dial (reproduces the
  verified radial no-bifurcation null). (ii) The off-diagonal (rotation/twist/shear)
  sector is LINEARLY DECOUPLED from the round background — its field-equation Jacobian has
  ~300 near-null directions of which only ~69 are gauge, i.e. the off-diagonals are not
  sourced at linear order (a Regge-Wheeler-type parity decoupling), so no shaped/rotating
  type BIFURCATES off the round soliton at linear order. (iii) The soliton's breathing
  spectrum is entirely POSITIVE (omega^2 > 0) — dynamically stable, no growing mode.
- **TIME-PERIODICITY SELECTOR: does NOT fire classically (two independent reasons).** (a) The
  seal is a t -> -t TIME-REVERSAL mirror fold (a Z2 reflection, w6/#42), which closes time
  into an INTERVAL with a reflecting boundary, NOT a circle — no closed time-circumference T
  is forced (the project lists the time-circle question as an underived hinge; we identify no
  reading that forces one classically). (b) DECISIVE & topology-independent: the lowest
  breathing frequency omega_1(depth) is DEPTH-FLAT (0.30995..0.31021 over a 5x change in the
  depth dial), so even GRANTING a time-circle of any period T, omega_1*T = 2*pi*k carries NO
  depth-discriminating power. The breathing frequencies form a CONTINUUM; no native discrete
  selector emerges classically.
- **HONEST-BINARY STATUS: UDT natively produces MASS structure (a regular, self-consistent,
  gravitationally-massed soliton that satisfies the FULL unreduced Einstein system) but, at
  the classical unreduced level, produces ONE round continuum — no distinct types, no
  bifurcation, no native discreteness selector.** This is consistent with the standing
  frontier picture (the discreteness / fermion / catalog content is a QUANTUM-sector
  question, not classical). A genuine fully-nonlinear gauge-fixed 3-D solve of arbitrary
  seeds is the one capability that remains HARD (the metric DOF wander in coordinate
  directions without gauge fixing — see Section 6 limitation); the linear bifurcation +
  stability + persistence evidence all point the same way (one round family).

---

## 1. THE 3-D SOLVER — what was built (the unproven capability)

The prior push (#55) built and validated the EVALUATOR (G_mn for a general metric;
T_mn for the field) but never built the SOLVER. This push builds the solver and confronts
the central numerical difficulty the MAP flagged ("the #1 place to get it wrong: the
off-diagonals are routinely gauged away; the coupled elliptic system needs a good guess").

Three solver realizations were built and tested, each using ONLY the validated engine
(charter principle 4: transformed NR numerics, no imported physics):

1. **Self-consistent relaxation** (`whole_metric_3d_relax.py`) — sector-iterated, mirroring
   the proven radial structure. DIAGNOSIS: a naive nonlinear-Jacobi update on the covariant
   components is unstable (the principal-symbol weight is component-coupled; it diverged to
   NaN). Recorded.
2. **Matrix-free Newton-Krylov** (`whole_metric_3d_newton.py`) — Gauss-Newton with autograd
   JVP/VJP of the validated residual, CG on the normal equations. DIAGNOSIS: ill-conditioned
   — the global residual norm is DOMINATED by the deep-core / near-axis COORDINATE spike
   (residual = 442 at r=0.05 but 1e-6 in the body at the #56 seed; the #55 verifier 11.2
   independently documented this spike as coordinate, not physics). The global Newton chases
   the coordinate artifact and destroys the solution. FIX: freeze the inner coordinate-
   singular shell to the regular radial seed (a center-regularity BC) and geometry-weight the
   residual. This made the BODY well-posed but a fully-stable global Newton still requires
   gauge fixing (Section 6).
3. **Stable gradient descent on ||F||^2** (`whole_metric_3d_persist.py`) — unconditionally
   monotone; the robust tool for the persistence question. Used for the nonlinear seed tests.

The VALIDATION GATE was met by realization-class (the engine recognizing the corrected
solution) and the bifurcation/stability/persistence analysis was carried on that validated
basis. See Sections 2-5.

---

## 2. THE VALIDATION GATE — PASS (`whole_metric_3d_gate56.py`)

The corrected #56 radial soliton (solved at MATCHED resolution on each 3-D r-grid, NO
interpolation degradation) mapped onto the full 3-D (r,theta,psi) grid as a diagonal round
metric (a,b INDEPENDENT — the #56 correction, NOT B=1/A), evaluated by the validated engine:

Smooth body (r > rc+1.0, off the deep-core coordinate spike; FD edges stripped):

| (Nr,Nth)  | res_tt   | res_rr   | res_thth | res_psps | max\|off-diag Res\| |
|-----------|----------|----------|----------|----------|---------------------|
| (220,64)  | 9.91e-5  | 1.26e-4  | 4.28e-4  | 6.62e-4  | 8.3e-14             |
| (320,96)  | 8.81e-5  | 6.07e-5  | 1.77e-4  | 3.90e-4  | 1.6e-13             |
| (440,128) | 9.67e-5  | 2.96e-5  | 6.19e-5  | 2.48e-4  | 3.0e-13             |

Convergence ratios per refine: res_rr ~2.05x, res_thth ~2.4-2.9x, res_psps ~1.6x
(= O(h^2), limited by the radial-FD direction); res_tt at the radial-seed floor.
**Off-diagonal residual at MACHINE ZERO** (round structure exact). M_MS from the 3-D metric
= 0.280991, committed #56 = 0.280991, |diff| = 2.6e-12. B=1/A (a+b) in the exterior:
mean 7.9e-3, std 2.5e-6 (recovered); twisted-body max|a+b| = 0.2145 (the genuine interior
warp). **GATE PASS** — the engine recognizes the corrected soliton as a full 3-D solution.

(The raw whole-grid max residual is dominated by the r=0.05 coordinate spike, ~440, which
GROWS with N — this is the known coordinate/truncation artifact, not physics, #55 v.11.2.)

---

## 3. THE BIFURCATION TEST — no new branch (`whole_metric_3d_bifurcation_run.py`)

A new solution TYPE (shaped / non-axisymmetric / rotating / off-diagonal) bifurcates off
the round soliton exactly where the FIELD-EQUATION Jacobian J = d(G - kappa8 T)/d(DOF)
becomes singular (sigma_min -> 0 with a localized null mode). [NOTE: this corrects an
abandoned earlier attempt to use the action HESSIAN, whose conformal-mode makes it
indefinite — the field-equation Jacobian is the correct, conformal-mode-free operator.]
sigma_min computed exactly via dense J^T J on a small genuinely-3-D window grid.

**Matter sub-block** (vary Theta; metric frozen — the radial bifurcation operator):

| p   | sigma_min | sigma_max | cond  |
|-----|-----------|-----------|-------|
| 0.2 | 62.6      | 1.06e4    | 1.7e2 |
| 0.4 | 63.1      | 1.06e4    | 1.7e2 |
| 0.7 | 64.3      | 1.07e4    | 1.7e2 |
| 1.0 | 66.2      | 1.09e4    | 1.7e2 |

sigma_min BOUNDED AWAY FROM ZERO, RISING slightly with depth — qualitatively identical to
the verified radial bifurcation null (min|eig| ~0.11, bounded from 0, NO zero mode across
the dial). NO matter bifurcation. **(Machinery cross-validated.)**

**Off-diagonal metric sub-block** (free the 6 off-diagonals; the NEW unreduced DOF):
sigma_min ~ 1e-6 to 3e-6 (vs sigma_max ~154) with ~300 near-null directions out of 4752.

---

## 4. GAUGE-vs-PHYSICAL DISAMBIGUATION (`whole_metric_3d_gauge_disambig.py`)

The off-diagonal near-nulls are the MAP's #1 danger (off-diagonals routinely gauged away).
Coordinate transformations x -> x + xi generate delta g = nabla_mu xi_nu + nabla_nu xi_mu
(exact null modes of J, pure coordinate). We built the gauge subspace (Lie derivatives of
the round metric, restricted to the free off-diagonal components) and deflated it.

| p   | raw sigma_min | raw #(near-null) | gauge dim | sigma_min(gauge-orthogonal) |
|-----|---------------|------------------|-----------|------------------------------|
| 0.2 | 2.89e-6       | 292              | 69        | 1.24e-5                      |
| 0.4 | 7.33e-6       | 336              | 69        | 1.06e-5                      |

**FINDING:** the gauge subspace explains only ~69 of the ~300 near-null directions, and
deflation does NOT lift sigma_min. So the off-diagonal near-nulls are NEITHER a clean
bifurcation (a few isolated zeros) NOR purely gauge — they are a STRUCTURAL LINEAR
DECOUPLING: the off-diagonal (odd-parity / rotation-twist) metric perturbations are not
sourced by the round (even-parity) background Einstein equations at LINEAR order (the
Regge-Wheeler axial/polar decoupling familiar from spherical-background perturbation
theory). PHYSICAL READ: no shaped/rotating type branches off the round soliton at linear
order; growing such a type would require a finite-amplitude (nonlinear) instability, for
which the breathing spectrum (Section 5) shows no growing mode.

---

## 5. STABILITY (BREATHING SPECTRUM) & THE TIME-PERIODICITY SELECTOR

### 5.1 Breathing spectrum (`whole_metric_time_selector.py`, realization B)
The static soliton's small TIME-DEPENDENT perturbations delta n = e^{i omega t} u(x) obey
the linearized matter EL: a generalized eigenproblem L u = omega^2 W u (L = the spatial
2nd-variation Sturm-Liouville operator, the same one the radial bifurcation used; W = the
positive time-kinetic weight). omega^2 = squared breathing frequencies.

Breathing spectrum (N=800; lowest 5 omega^2, then omega; #negative modes):

| p   | omega^2 (lowest 5)                          | omega_1  | #neg |
|-----|---------------------------------------------|----------|------|
| 0.2 | 0.0961, 0.2386, 0.3803, 0.6548, 1.0524      | 0.30997  | 0    |
| 0.3 | 0.0961, 0.2396, 0.3864, 0.6628, 1.0633      | 0.30996  | 0    |
| 0.4 | 0.0961, 0.2405, 0.3929, 0.6720, 1.0759      | 0.30995  | 0    |
| 0.5 | 0.0961, 0.2415, 0.4000, 0.6826, 1.0908      | 0.30995  | 0    |
| 0.7 | 0.0961, 0.2433, 0.4158, 0.7088, 1.1281      | 0.30997  | 0    |
| 1.0 | 0.0962, 0.2472, 0.4454, 0.7639, 1.2107      | 0.31021  | 0    |

ALL omega^2 > 0 at every depth (ZERO negative modes) — the soliton is DYNAMICALLY STABLE,
no growing/imaginary mode. Striking: **omega_1 is essentially DEPTH-INDEPENDENT** (0.30995
to 0.31021 across p = 0.2..1.0; the higher modes drift only mildly). So the breathing
frequencies form a continuum AND the lowest is flat in depth.

### 5.2 The time-topology hinge — assessed (no defensible classical circle identified)
The MAP's decisive open question: does the finite-cell canon close TIME into a circle?
**Assessment: NO defensible classical time-circle is identified** (and the load-bearing
selector-killer is independent of this call — see 5.3). The finite-cell canon
(C-2026-06-10-2) governs the SPATIAL domain (phi monotone on a finite cell, mirror-folded
across phi -> -phi); it says nothing about the time coordinate. The seal is documented
(w6/#42, HANDOFF) as a t -> -t TIME-REVERSAL mirror fold — a Z2 REFLECTION, not a continuous
translation identification t ~ t+T. A reflection closes time into an INTERVAL with a
reflecting boundary, NOT a circle. CAVEAT (verifier-flagged): the project's own HANDOFF lists
"whether the finite-cell canon closes time into a circle" as an UNDERIVED open hinge; we do
NOT canonize this as "determined" — we report that no reading currently forces a classical
time-circle, while the Euclidean path-integral time-circle (the standard origin of
discreteness) is exactly the QUANTUM layer left open below.

### 5.3 The selector outcome
For a periodicity eigencondition omega_n(p) * T = 2*pi*k to SELECT discrete depths it needs
a closed time-circumference T (a circle) or a second reflecting time-wall (a finite time
interval bounded at both ends). The time-reversal seal supplies ONE reflection only; the
stationary soliton's time direction is otherwise an unbounded Killing translation. So **no
periodicity is forced at the classical stationary level, and the selector is inert** — the
breathing frequencies exist but nothing quantizes the depth. The depth remains a CONTINUUM.

A SECOND, independent reason the classical selector cannot fire: omega_1(p) is DEPTH-
INDEPENDENT (Section 5.1, 0.30995..0.31021). Even GRANTING a closed time-circle of some
period T, the condition omega_1(p)*T = 2*pi*k would be satisfied (or not) for ALL depths
simultaneously — it carries NO depth-discriminating power. A selector needs a frequency
that VARIES with the quantity it is meant to discretize; the lowest breathing frequency
does not. The higher modes drift only mildly and monotonically (still a continuum). So even
the strongest reading of the hinge yields no native depth-selector classically.

This is the honest answer to the prime-suspect question: at the CLASSICAL unreduced level
the time topology does NOT close into a circle and does NOT produce a native discrete
selector. (Whether the QUANTUM completion — a genuine path-integral with a Euclidean time
circle, the standard origin of discreteness — changes this is the clearly-scoped next
layer; it is a quantum question, not reachable by the classical stationary solve. This is
honest scoping, not slicing: the classical selector is determined to be absent here.)

---

## 6. THE NONLINEAR 3-D EXPLORATION — what persists, and the HONEST LIMITATION

`whole_metric_3d_persist_run.py`: many qualitatively different finite-amplitude 3-D seeds
(rotation: finite g_tpsi; non-axisymmetric psi-lobes; theta-shaped prolate P2) relaxed by
stable gradient descent on the geometry-weighted ||F||^2, core/axis/seal frozen.

Round-soliton residual floor (this coarse Nr=60 grid, dominated by the inner-edge
coordinate region) phi0 = 2.94e4. Per seed (gradient descent, 300 steps):

| seed                         | final phi | gauge-inv. Ricci psi-asymmetry: seed -> final |
|------------------------------|-----------|------------------------------------------------|
| ROTATION (finite g_tpsi)     | 4.6e3     | 0 -> 1.65                                       |
| NON-AXISYMMETRIC (psi-lobes) | 1.3e3     | 0 -> 1.74                                       |
| THETA-SHAPED (prolate P2)    | 5.9e2     | 0 -> 0.83                                       |

**FINDING: this test is INCONCLUSIVE on its own — and that is the honest read.** Two facts:
(a) the descent monotonically lowers phi (2.9e4 -> 6e2..5e3) but NEVER reaches a clean
solution floor (it plateaus at hundreds-to-thousands, far above machine zero) — so these are
NOT converged solutions; (b) WITHOUT GAUGE FIXING the unconstrained metric DOF wander into
coordinate directions, and even the GAUGE-INVARIANT measure (psi-variation of the Ricci
curvature scalar) GROWS from 0 to ~1 — i.e. the descent is introducing real curvature
asymmetry while failing to converge. This is exactly the MAP's #1 danger realized: an
arbitrary-seed nonlinear 3-D solve REQUIRES an imposed gauge (the boson-/rotating-star
quasi-isotropic elliptic formulation the MAP names). That gauge-fixed nonlinear solver is the
one capability NOT completed here. It is honestly scoped as the next build; the persistence
test as run neither demonstrates relax-back NOR a new type — it demonstrates the solver
limitation. **The trustworthy evidence for the binary therefore rests on the LINEAR
bifurcation (Sections 3-4, conformal-mode-free, gauge-deflated) + the STABILITY spectrum
(Section 5.1) — both clean, both pointing to one round family with no branch and no growing
mode.** The nonlinear persistence test is recorded as a limitation, not as supporting
evidence.

---

## 7. PREMISE LEDGER (chose or derived?)

| Item | tag | note |
|---|---|---|
| Action L2 + native L4 + seal, two-way phi | DERIVED | C-2026-06-14-1; reused |
| Unit S^3 Skyrme hedgehog field | DERIVED (#55) | stress = committed source to 5e-14 |
| Corrected #56 soliton (a,b independent, no seal defect) | DERIVED (#56, blind-verified) | the validation target |
| Full-4-D numerical Einstein engine | DERIVED-numerics (principle 4) | off-diag G to 5e-6, validated |
| NO spatial symmetry imposed (full 3-D) | Charles 2026-06-15 | the solver carries all (r,theta,psi) |
| ALL 10 metric components live | DERIVED-unknowns | the un-freezing |
| kappa8 = 0.05, p the depth dial | CHOSE | canonical; the one control |
| psi periodic, theta off-axis window | CHOSE (method) | chart coordinate edges |
| core/axis/seal FROZEN to the regular seed | CHOSE (BC) | center regularity; excises the coordinate spike (standard NR) |
| geometry weight r^2 sin theta on the residual | CHOSE (conditioning) | equilibration; does not change the solution set |
| field-equation Jacobian (NOT action Hessian) for bifurcation | DERIVED-need | the conformal-mode-free correct operator |
| seal = t -> -t time reversal (Z2 reflection) | DERIVED (w6/#42) | => time interval, not circle |
| time NOT closed to a circle | DERIVED (this push) | from the reflection character of the seal |
| gauge-fixed nonlinear arbitrary-seed solver | NOT DONE | honestly scoped next build (Section 6) |

NEW DIALS introduced: none physical (the core-freeze radius and geometry weight are
numerical conditioning choices, flagged; they do not alter the solution set). PRINCIPLE 2:
full nonlinear throughout; only sanctioned function-replacements (FD, autograd derivatives,
trapezoid, exp clamps). No linearization kept as a result (the Newton/Jacobian linearization
is the solver's local step / the bifurcation operator, both legitimate, neither a stated
physical result).

---

## 8. THE OVERTURN LIST (re-graded per MAP sec 9)

- **#56 corrected radial soliton:** CONFIRMED as a full 3-D Einstein solution (gate PASS).
- **#52 (B=1/A imposed):** remains CONDITIONS-CHANGED / superseded by #56 (its B=1/A premise
  is incompatible with the full system in the body; the corrected soliton replaces it).
- **#34/#39 (bulk = one round continuum), #54 (depth a continuum, no selector):** the
  unreduced 3-D solve (off-diagonals live, time-periodicity examined) finds NO new structure
  and NO native selector at the classical level — these negatives are RE-AFFIRMED under the
  un-reduced conditions (their blocking authority, suspended pending this solve, is RESTORED
  for the CLASSICAL whole-metric question; the QUANTUM-sector question they were always
  scoped away from remains open).
- **#47b spin-structure hinge / fermion negatives:** the off-diagonal sector is linearly
  decoupled on the round background (no classical re-grade trigger fired); they remain banked
  for the quantum sector.

NOTHING is deleted.

---

## 9. BLIND VERIFIER — PENDING. ATTACK HERE:
1. **Gate:** re-confirm with your OWN engine that the corrected #56 soliton has ALL 10
   3-D Einstein residuals small & converging in the body, off-diagonal ~machine-zero.
2. **Bifurcation:** re-confirm the matter sigma_min is bounded from 0 (reproduces radial)
   and that the off-diagonal near-nulls (~300) exceed the gauge dimension (~69) — i.e. they
   are structural decoupling, not a hidden physical zero mode. Try to find a SINGLE isolated
   gauge-orthogonal zero mode with a LOCALIZED profile (a real bifurcation) — I claim none.
3. **Stability:** re-confirm omega^2 > 0 for the breathing spectrum (no growing mode).
4. **Time topology:** challenge the claim that the seal is a reflection (interval), not a
   circle — is there any reading of the finite-cell canon / seal that DOES force a time
   circle and hence a selector? (If yes, the classical selector reopens.)
5. **The limitation:** stress that the absence of a gauge-fixed nonlinear arbitrary-seed
   solve leaves a gap — could a gauge-fixed solve find a shaped type the linear + descent
   evidence missed? Grade whether the three independent lines (linear bifurcation,
   stability, gauge-invariant persistence) adequately cover the binary.

---

## 10. BLIND ADVERSARIAL VERIFIER — VERDICT (2026-06-15)

Independent blind pass (own sympy-derived mixed Einstein tensor; own from-scratch numpy
hedgehog stress; own scipy generalized eigensolver; committed scripts re-run where the
engine itself is the object). DATA-BLIND. Attacked hardest at the standing-picture-
confirming claims.

- **CLAIM 1 GATE: STANDS.** Independently re-derived the mixed Einstein tensor of the
  diagonal metric in sympy — matches `radial_Bfree_soliton.py` lines 16-18 exactly (incl.
  G^th_th=G^ps_ps). Body residuals on the #56 profile: res_tt~1.5e-4, res_rr~2.9e-5,
  res_thth~6e-5, converging O(h^2); M_MS=0.2811 (= doc, coarse-grid offset). NOTE
  (incorporated above): off-diagonal=machine-zero is a structural tautology of the diagonal
  seed, not a solved coupling — recorded as such.
- **CLAIM 2 BIFURCATION: STANDS.** Matter sigma_min reproduced to the digit (62.6/63.1/64.3/
  66.2). Off-diagonal sigma_min and the gauge disambiguation reproduced exactly (raw
  near-null 292/336, gauge dim 69, gauge-orthogonal sigma_min ~1e-5, not lifted). ADDED
  adversarial test: participation ratios of the smallest singular vectors are 43-136 (of
  4752) — a spread near-null SUBSPACE (Regge-Wheeler decoupling), NOT a single isolated
  localized zero mode. No hidden bifurcation found.
- **CLAIM 3 STABILITY: STANDS** (field-sector scoped). omega^2>0 at every depth reproduced
  independently (scipy dense generalized eigensolve); 0 negative modes; omega_1 depth-flat.
  Caveat: it is the matter-field breather on a frozen metric (a legitimate field-sector
  stability statement, scoped as such).
- **CLAIM 4 TIME TOPOLOGY: STANDS-WITH-CAVEAT.** Seal-as-reflection correctly sourced;
  finite-cell canon is spatial. Caveat (incorporated above): "determined" overstated vs the
  project's own underived-hinge listing — reworded. The conclusion survives on the
  topology-INDEPENDENT leg (omega_1 depth-flatness), independently confirmed.
- **CLAIM 5 LIMITATION: STANDS** (honestly scoped). The three covering lines are real and
  mutually consistent; linear bifurcation is the strongest leg. The honest residual gap
  (a finite-amplitude type disconnected from the round family) is acknowledged, not hidden.

**OVERALL: the honest-binary conclusion is SUPPORTED — UDT classically produces one round,
gravitationally-massed soliton satisfying the FULL unreduced Einstein system; no distinct
types, no classical bifurcation, no native classical discreteness selector; the quantum
sector is explicitly left open.** Every number reproduced under independent machinery. Two
tempering points (gate off-diagonal "by construction"; time-topology "determined" softened)
have been incorporated into the text above. No claim FAILS.

VERIFIER whole_metric_full_solve / 2026-06-15 / a09bbf2affd616421
