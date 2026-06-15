# RESULTS — The WHOLE-METRIC Solve, realization (A): full STATIONARY 3-D soliton

Research record (append-never-edit). Driver: Claude (Opus 4.8, 1M). 2026-06-15.
OBSERVE mode (report WHAT IS THERE; NOT targeting any result). Frame + premise
ledger: `whole_metric_solve_MAP.md`. DATA-BLIND throughout (sizes/masses in units
L = sqrt(kappa/xi) = 1; NEVER compared to wall numbers).

Scripts (committed with this doc):
- `whole_metric_3d_core.py` — the full-4-D numerical Einstein engine: a GENERAL
  metric g_{mu nu}(r,theta,psi) → FD → Christoffel → Riemann → Ricci → Einstein
  G_{mu nu}, ALL components (the standard NR route, charter principle 4: transformed
  numerics, no imported new physics). GPU torch float64, V100.
- `whole_metric_3d_validate_core.py` — SELF-VALIDATION of that engine against EXACT
  analytic Einstein tensors (flat, Schwarzschild, and a generic OFF-DIAGONAL
  psi-dependent metric).
- `whole_metric_3d_matter.py` — the matter sector: the unit S^3 Skyrme hedgehog field
  and its full stress tensor T_{mu nu} (L2 + native-L4 in Lagrange-identity form),
  ALL components incl. off-diagonal.
- `matter_ansatz_derive.py` — the EXACT (sympy) derivation that fixed the correct
  unit-vector ansatz (see §2).
- `whole_metric_3d_gate.py` — THE MANDATORY VALIDATION GATE.

Blind verifier: PENDING (verifier-before-record; attack-here block at the end).

---

## 0. WHAT WAS BUILT (the unreduced machinery)

Per the MAP §10.1–10.2, two engines, each validated against ground truth BEFORE use:

**(i) The full-4-D numerical Einstein engine.** A general stationary metric
g_{mu nu}(r,theta,psi) — all 10 components live, NO symmetry, NO diagonal-only — is
carried on a 3-D (r,theta,psi) grid (psi PERIODIC, 4th-order central everywhere; r,
theta 4th-order interior + 4th-order one-sided edges). The pipeline is the textbook NR
route computed numerically: g → (FD) → ∂g → Christoffel Γ^a_{bc} → (FD) → ∂Γ →
Riemann R^a_{bcd} → Ricci → R → Einstein G_{mu nu}. No closed-form G is assumed for a
general 4-D metric (the MAP forbids it). Stationary ⇒ ∂_t = 0 in the adapted gauge.

**Self-validation (`whole_metric_3d_validate_core.py`, all PASS):**
| test | result |
|---|---|
| flat Minkowski (spherical) → G=0 | max\|G\| interior = 5.7e-5, → 2.8e-6 refining theta (FD truncation) |
| Schwarzschild vacuum (M=1) → G=0 | max\|G\| = 5.6e-5 → 9.6e-6, convergence order ~2.0 |
| **generic OFF-DIAGONAL psi-dependent metric** (g_tpsi frame-drag, g_rtheta shear, g_tr, theta- & psi-dependence) vs INDEPENDENT exact-analytic Einstein | **max\|G_num − G_exact\| = 5.1e-6**, → 2.6e-7 refining, ~2nd order |

The off-diagonal test is the load-bearing one: it proves the time-row / shear / twist
sector (the whole point of the unreduced solve) is computed correctly and is NOT gauged
away. The independent reference computes G EXACTLY from analytic first/second metric
derivatives via a separate numpy tensor-algebra code path (no FD, no symbolic-inverse
blow-up).

**(ii) The matter stress tensor T_{mu nu}** for the unit field n on its target, full
contraction with the full inverse metric, all components incl. off-diagonal
momentum/shear, via the Hilbert variation T_{mu nu} = −2 ∂L/∂g^{mu nu} + g_{mu nu} L
(L = L2 + native L4; no metric-derivative coupling). **Validated:** the general T
reproduces the committed reduced (rho, p_r) [`complete_metric_batched.stress`] to
**max\|diff\| = 5.7e-14** over 200 random (r,theta,psi,phi,Theta,Theta') points.

---

## 2. THE FIELD ANSATZ — a DERIVED correction (matter_ansatz_derive.py)

Building the unreduced matter sector forced into the open an ambiguity the reduced
record never resolved: the field written in `native_stabilizer_results.md` as
`n = (sinTheta sin th cos ps, sinTheta sin th sin ps, cosTheta)` is **NOT a unit
vector** (|n|^2 = 1 − cos^2 th sin^2 Theta). An exact sympy derivation
(`matter_ansatz_derive.py`) settles it:

- The committed POINTWISE stress (rho, p_r) — the object that SOURCES phi via Einstein
  G = kappa T — is reproduced EXACTLY (rho − rho_committed = 0 and p_r − p_r_committed
  = 0, sympy-simplify, for ALL theta) by the **unit S^3 / SU(2) Skyrme hedgehog**:

      n = ( sinTheta(r) sin th cos ps,
            sinTheta(r) sin th sin ps,
            sinTheta(r) cos th,
            cosTheta(r) ),                 |n| = 1 exactly.

  For this unit 4-vector the native Skyrme L4 must be taken in the Lagrange-identity
  form S_{mn}.S_{pq} = (d_m n.d_p n)(d_n n.d_q n) − (d_m n.d_q n)(d_n n.d_p n) (the
  literal 3-vector cross product only exists for a 3-vector S^2 target). With it,
  L2 = −(xi/2)(X+2Y), L4 = −(kappa/2)(2XY+Y^2), and p_r+rho = X(xi+2kappa Y) — all the
  committed reduced forms, EXACTLY.

- The committed ENERGIES E2_r, E4_r come from the DIFFERENT non-unit S^2 field; they do
  NOT equal the S^3 hedgehog's integrated energy. **Flagged provenance issue** (the
  reduced engine uses the S^3-hedgehog stress in `stress()` but the S^2-field energy in
  `energy_pieces()`). NOT patched — recorded. It does not affect this push: the gate
  tests the Einstein equations, which source from T_{mu nu} (the stress), and the stress
  is the S^3-hedgehog one we validated to 5.7e-14.

**Premise tag:** the unit S^3 ansatz is DERIVED (it is the field whose stress matches
the committed source, exactly). This is a small derived correction to the record's
stated (non-unit) ansatz, surfaced by demanding |n|=1 in the unreduced build.

---

## 3. THE GAUGE (chosen, flagged, non-restrictive)

The metric is carried in FULL generic 4×4 form on the (r,theta,psi) grid — all 10
components are independent allocated unknowns; NO chart condition is imposed to evaluate
the residual of a given configuration. DOF count: a stationary 4-D metric has 10
components; 4 coordinate freedoms fix a chart ⇒ 6 physical metric DOF + the matter
field. The reduced diagonal soliton (g_tr=g_ttheta=g_rtheta=g_tpsi=g_rpsi=g_thetapsi=0,
g_thth=r^2, g_psps=r^2 sin^2 th) is ONE point of this chart. The chart is
non-restrictive by construction: it CONTAINS the reduced solution as a special case
(the 3-D exploration step would FREE the 6 off-diagonals from zero). Per the MAP
tripwire we did NOT pick a diagonal gauge and did NOT impose rho=r as a gauge.
**(G4): PASS.**

---

## 4. THE SEAL ON THE FULL METRIC (BC; partial)

The same-minus mirror fold (time-reversal at the interface) is, for the diagonal
soliton, the Neumann/gauge closure phi(seal)=0 (it sets a global additive constant on
phi = −½ ln(−g_tt)). Its action on the off-diagonal components (g_ttheta, g_tpsi, …)
— flagged NEW in the MAP — was NOT needed at the gate stage (the gate tests the existing
diagonal soliton, where the off-diagonals are zero) and is left for the gated 3-D step.
**Honest state: the seal's full-metric action is UNCOMPUTED**, as the MAP anticipated.

---

## 5. THE VALIDATION GATE — OUTCOME: **FAIL** (a SCOPE FINDING, not a build bug)

Per the MAP, before ANY 3-D exploration the full-3-D code MUST reproduce the reduced
#52 soliton as a stationary solution of the FULL Einstein-matter system. We seeded the
committed #52 round soliton (p=0.4, kappa8=0.05; Theta(r), phi(r) from
`complete_metric_batched.selfconsistent_batched`, the engine that reproduces #43/#44/#52)
onto the 3-D grid and evaluated the FULL Einstein equations component by component.

### The decisive result (mixed components — the physical Einstein equations):
| equation | max\|G^μ_ν − kappa8 T^μ_ν\| | verdict |
|---|---|---|
| G^t_t = kappa8 T^t_t  (the Misner-Sharp eq) | ~0.10 (FD-level) | **satisfied** |
| G^r_r = kappa8 T^r_r | **1.64** | **VIOLATED, O(1)** |
| G^th_th = kappa8 T^th_th | **0.37** | **VIOLATED, O(1)** |
| G^ps_ps = kappa8 T^ps_ps | **0.35** | **VIOLATED, O(1)** |

### Why (root cause, proven):
The reduced solve enforces **only** the (t,t) Einstein equation (the Misner-Sharp mass
relation m'(r) = kappa8 r^2 rho) and the matter EL for Theta. It **assumes** B=1/A
(g_tt g_rr = −1) and never checks the (r,r) or angular equations. But B=1/A together
with G^t_t = kappa8 T^t_t **forces p_r = −rho**. The soliton is EOS-softened
(p_r ≠ −rho; p_r+rho = e^{−2phi}Theta'^2(xi + 2kappa sin^2Theta/r^2) > 0 wherever
Theta' ≠ 0 — exactly `native_stabilizer_results.md` Task 3, verifier-cleared). So the
off-(t,t) equations CANNOT hold for the twisted body.

### Spatial confirmation (the residual tracks the EOS-softening, not a bug):
The (r,r) residual is **O(1) in the twisted BODY** (Theta' ≠ 0): max 2.75, mean 0.13;
and **~5e-4 in the unwound EXTERIOR** (Theta' → 0, p_r = −rho exactly). The engine
satisfies Einstein precisely where B=1/A is exact and fails precisely where the soliton
softens — i.e. the violation IS the p_r ≠ −rho softening, quantified at the level of the
full Einstein equations. (Convergence check: the (r,r) residual does NOT fall toward
zero with resolution — it is a genuine inconsistency, not truncation.)

### On M_MS (G2): the committed M_MS = 0.28964 is the SOURCE mass m_areal (it includes
the depth-dial core term + the linear seal-defect the reduced code injects to close the
cell); the 3-D metric DEFICIT mass r(1−e^{−2phi}) = 0.06128 is a different quantity.
The Theta profile (width/L = 0.6689) is carried exactly; B=1/A holds by construction.

### GATE VERDICT
**FAIL.** The reduced #52 round soliton satisfies only the (t,t) Einstein equation; the
(r,r) and angular equations are violated at O(1). It is **NOT a stationary solution of
the full Einstein-matter system.** The full-3-D MACHINERY is independently validated
(flat / Schwarzschild / generic-off-diagonal-analytic to ~5e-6 with ~2nd-order
convergence; committed reduced stress to ~5e-14), so this is a **scope finding about the
reduced construction, not a build defect.**

Per the MAP's mandatory gate ("If the gate FAILS, STOP and report the build problem
honestly — do NOT proceed to 3-D results"): **we STOP. No 3-D exploration was run.**

---

## 6. WHAT THIS MEANS (PONDER, lay terms — for Charles)

The earlier "one round knot" soliton (#52) was solved by enforcing ONE of Einstein's
equations (the one that fixes how the dilation phi piles up — the time-time / mass
equation) plus the rule for the twist field, and by ASSUMING the clean relation B=1/A
between the time-warp and the radial-warp. When you now demand that the SAME object
satisfy ALL of Einstein's equations at once — including the radial-pressure equation and
the two angular ones — it does not. The radial equation is off by an order-1 amount, and
it is off exactly inside the twisted body, exactly where the twist makes the radial
pressure differ from the energy density. In the calm exterior, where the twist has
unwound, everything is consistent.

So the unreduced solve has, at its very first gate, already found something the reduced
solves could not see: **the round soliton as currently built is not a full solution of
the metric** — it is a solution of a reduced subset (one Einstein equation + an assumed
B=1/A). A genuine whole-metric round soliton must RELAX the B=1/A assumption (let g_tt
and g_rr be independent), so that the radial and angular Einstein equations can be
satisfied by the metric responding to the soliton's actual (softened) pressures. That is
a real, concrete next step — and it is exactly the kind of overturn the MAP §9 flagged
(#52's scope is "static, diagonal, spherical, B=1/A, rho=r"; the B=1/A premise is now
shown to be incompatible with the full equations for the twisted body).

This does NOT say the soliton does not exist. It says: to find the TRUE round (and then
3-D) soliton of the whole metric, B=1/A must be dropped and the (r,r)+angular Einstein
equations solved together with (t,t) and the matter EL — a 2-function radial metric
(g_tt, g_rr independent) at minimum, before any off-diagonal freeing. The DERIVE of that
true soliton is gated (Charles's call); this OBSERVE push delivers the validated
machinery and the precise diagnosis that motivates it.

---

## 7. PREMISE LEDGER (chose or derived?)

| Item | tag | note |
|---|---|---|
| Action L2 + native L4 + seal, two-way phi | DERIVED | C-2026-06-14-1, #43; reused |
| Unit S^3 Skyrme hedgehog ansatz (4-vector) | DERIVED (this push, matter_ansatz_derive.py) | the unit field whose stress = committed source, exactly; corrects the record's non-unit ansatz |
| Lagrange-identity L4 (for the unit 4-vector) | DERIVED | the native form for S^3; reproduces committed L4 |
| Full-4-D numerical Einstein route | DERIVED-numerics (principle 4) | validated vs flat/Schwarzschild/off-diagonal-analytic |
| psi periodic, 4th-order FD | CHOSEN (method) | azimuth genuinely periodic |
| Gauge = full generic 4×4 chart (non-diagonal) | CHOSEN (flagged; proven non-restrictive) | contains the diagonal soliton as a special case |
| B=1/A | NOT imposed by the engine — TESTED | result: B=1/A is INCOMPATIBLE with the full Einstein system for the twisted body |
| kappa8 = 0.05, p = 0.4 | CHOSEN | inside Stage-B existence ceiling; the gate target |
| Seal action on off-diagonals | OPEN | uncomputed; not needed at gate; gated 3-D step |
| Time closed to a circle? | OPEN HINGE | untouched (realization B not reached) |

---

## 8. THE OVERTURN LIST (re-graded per the MAP §9)

- **#52 (complete-action sweep = one round charge-1 continuum):** CONDITIONS-CHANGED.
  Its scope premise "B=1/A" is now shown INCOMPATIBLE with the full Einstein system for
  the twisted body (only the exterior, Theta'=0, is B=1/A-consistent). #52 remains a
  valid solution of {(t,t) Einstein + matter EL + assumed B=1/A}; it is NOT a solution
  of the full metric. Its "one round knot" headline is scoped to that reduced subset and
  loses blocking authority for the whole-metric question until re-graded under a
  B=1/A-free (2-function radial metric) solve.
- **#34 / #39 (bulk = one round continuum):** same B=1/A / diagonal scope — CONDITIONS-
  CHANGED for the whole-metric question (untested here; flagged).
- **#54 (depth a continuum, no native selector):** untouched (realization B / time-
  periodicity not reached); remains as banked, scope unchanged by this push.
- The fermion negatives, spin-structure hinge (#47b): untouched (no off-diagonal solve
  was reached); remain banked.

NOTHING is deleted; #52/#34/#39 are FLAGGED pending re-grade under a B=1/A-free solve.

---

## 9. HONEST STATE OF THE BUILD

- DONE & VALIDATED: the full-4-D numerical Einstein engine (all components, off-diagonal
  correct to ~5e-6, ~2nd order); the full matter stress tensor (committed stress to
  ~5e-14); the corrected unit S^3 ansatz (exact derivation).
- DONE: the validation gate — and it **FAILED**, with a precise, proven diagnosis (the
  reduced soliton satisfies only the (t,t) equation; B=1/A is incompatible with the full
  system for the twisted body).
- NOT DONE (correctly, per the gate rule): the full-3-D nonlinear relaxation/Newton
  solver and the 3-D exploration (round/shaped/lobed/off-axis/multi-center seeds). These
  are NOT trusted until a soliton passes the gate, and the gate showed the right soliton
  to solve for is a B=1/A-FREE one — a DERIVE-gated decision for Charles.
- The MANDATORY VALIDATION GATE did its job: it caught, at the cheap stage, that the
  object we were about to explore in 3-D is not a full-metric solution.

---

## 10. BLIND VERIFIER — PENDING. ATTACK HERE:

1. **Engine correctness:** re-derive the off-diagonal Einstein test independently (your
   own exact G for a metric with g_tpsi and g_rtheta) and confirm the engine matches.
   Confirm the matter T reproduces the committed `stress()` rho,p_r. Confirm the unit
   S^3 ansatz (matter_ansatz_derive.py) is genuinely |n|=1 and its Hilbert stress equals
   the committed (rho,p_r) symbolically.
2. **The gate failure:** re-confirm, with your OWN numerical Einstein code (not this
   engine), that the #52 soliton has G^t_t ≈ kappa8 T^t_t but G^r_r ≠ kappa8 T^r_r at
   O(1). Confirm the (r,r) residual concentrates in the body (Theta'≠0) and vanishes in
   the exterior. Check it is NOT an interpolation/edge artifact (try evaluating phi,Theta
   analytically-smoothly rather than interp; vary theta-range; vary kappa8 and p).
3. **The root cause:** verify symbolically that B=1/A + G^t_t = kappa8 T^t_t ⇒ p_r=−rho
   for this metric class, and that the soliton has p_r ≠ −rho in the body. I.e. the gate
   failure is forced by the EOS-softening, not a bug.
4. **Scope:** is the right correction really "drop B=1/A → 2-function radial metric", or
   does the reduced solve have a different repairable inconsistency? Stress the claim
   that #52 satisfies ONLY (t,t) (look for any other equation it secretly satisfies).
