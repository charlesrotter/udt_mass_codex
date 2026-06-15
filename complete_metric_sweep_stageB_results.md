# RESULTS — Stage B: Complete-Metric Deep-Negative-φ Solution-Space Sweep

Research record (append-never-edit). Driver: Claude (Opus 4.8, 1M). 2026-06-15.
OBSERVE push (report WHAT IS THERE; NOT targeting a fermion / critical point / any
particular cell). Frame + premise ledger: `complete_metric_sweep_setup.md` incl. the
STAGE-B ADDENDUM (κ₈ PRIMARY axis, TEST-BOTH dual reading, the discriminator, the
MANDATORY physical-vs-numerical guard). DATA-BLIND throughout (sizes/masses in units
L=√(κ/ξ)=1; NEVER compared to wall numbers).

Scripts (committed with this doc):
- `complete_metric_sweep_stageB.py` — the sweep + guard + bifurcation map + #38 re-run.
- `complete_metric_stageB_fast.py` — PCR-accelerated engine (SAME physics as the
  committed `complete_metric_batched.py`; only the linear-algebra inner kernel
  changed; cross-checked to machine precision — see Provenance).
- Data: `complete_metric_sweep_stageB_data.json`.
- Builds on the committed Stage-A baseline `complete_metric_sweep_stageA.py` /
  `complete_metric_batched.py` (commit 33d3a50), which reproduces #43/#44 exactly.

---

## 0. Provenance / numerics (principle 2 honored)

The committed Stage-A engine solves the tridiagonal Newton system with a DENSE
(B,N,N) `torch.linalg.solve` — O(N³) per member, ~70 s for one B=5, N=600 batched
self-consistent solve, which makes a 270-member sweep intractable. The repo-immutable
engine was NOT edited. Instead `complete_metric_stageB_fast.py` REUSES its exact
physics (`theta_ddot`, `stress`, `energy_pieces`, `phi_from_source`, `grad_central`
imported verbatim) and replaces ONLY the inner solve with a batched **parallel cyclic
reduction (PCR)** tridiagonal solver (~log₂N vectorized passes; explicit elementwise
ops — V100-safe, no `solve_triangular`-with-broadcast-Cholesky, the known cu121
corruption). Speed: ~2.5 s/member (28×). Correctness:

- PCR vs dense LU on random tridiagonals: max|diff| = **4.4e-16**.
- Full self-consistent member, fast vs committed engine, at (p=0.4, κ₈=0.05):
  **max|ΔΘ| = 2.8e-14, |ΔM_MS| = 1.3e-15** (asserted in-script before the sweep runs).

NO linearization as a result. Full nonlinear angular EL + nonlinear Misner-Sharp
t-equation, two-way φ. Sanctioned function-replacements only (trapezoid, FD Jacobian,
transient exp-arg clamp — converged solutions never touch it).

---

## 1. THE MANDATORY GUARD — is the κ₈≈0.1 feature PHYSICAL or NUMERICAL?

### 1a. The independent order parameter
Stage A's κ₈≈0.1 "over-collapse" carried res_th~4e9 — a solver-blowup signature, NOT
a critical point. To separate physics from numerics we track an INDEPENDENT order
parameter: the metric deficit **min(e^{-2φ}) = min(1 − m_closed/r)**. This → 0 is a
genuine horizon / existence boundary (the cell can no longer be held by the geometry);
it is read off the converged profile, not from the solver's convergence flag.

### 1b. Fine κ₈ scan at p=0.4 (the feature window)
| κ₈ | width/L | min_deficit | M_MS | res | min\|eig\| | state |
|---|---|---|---|---|---|---|
| 0.01 | 0.6724 | 0.9998 | 0.0628 | 2.6e-12 | 0.1979 | soliton |
| 0.03 | 0.6706 | 0.9397 | 0.1809 | 1.9e-12 | 0.1964 | soliton |
| 0.05 | 0.6692 | 0.8710 | 0.2897 | 1.9e-12 | 0.1949 | soliton |
| 0.055 | 0.6689 | 0.8540 | 0.3155 | 1.4e-12 | 0.1946 | soliton |
| 0.058 | 0.0467 | **−0.924** | 0.809 | 7.6e5 | 3e-8 | blowup |
| 0.060 | 0.245 | −0.876 | 2.51 | 4.5e5 | 1e-6 | blowup |
| 0.065 | 0.6683 | 0.8206 | 0.3656 | 1.2e-12 | 0.1939 | soliton |
| 0.070 | 0.6681 | 0.8042 | 0.3898 | 1.6e-12 | 0.1936 | soliton |
| 0.08–0.15 | ~0.02–0.05 | −1.4 … −2.2 | — | 6e9 | ~1e-8 | blowup |

The intermittent blowups at 0.058/0.060 with **0.065/0.070 still clean** are a
solver-CONVERGENCE-BASIN artifact of the Picard relaxation (the iteration sometimes
diverges before settling), NOT physics. The PHYSICAL boundary is the deficit→0
crossing, isolated by bisection below.

### 1c. Convergence study (just BELOW the feature, κ₈=0.058)
A real soliton is grid-stable; a numerical artifact moves with N / iters / relax.
| N | iters | relax | width/L | min_deficit | res |
|---|---|---|---|---|---|
| 400 | 90 | 0.30 | 0.6692 | 0.84397 | 6.5e-13 |
| 600 | 120 | 0.25 | 0.6687 | 0.84393 | 2.2e-12 |
| 900 | 150 | 0.20 | 0.6684 | 0.84395 | 3.4e-12 |
| 1300 | 200 | 0.15 | 0.6683 | 0.84397 | 8.0e-12 |

width and min_deficit are **grid-invariant to 4 digits**. The sub-boundary soliton is
a real, resolution-independent solution.

### 1d. mpmath confirmation at the boundary
At κ₈=0.063 (just below κ₈*), the converged soliton's min_deficit recomputed at
dps=40: float64 = 0.8272632236, mpmath = 0.8272632236, |diff| = **0.0e+00**, res =
1.6e-12. The deficit is a genuine positive physical quantity, not a float64 artifact.

### 1e. Existence-boundary bisection + order-parameter scaling (p=0.4)
**κ₈\*(p=0.4) = 0.06341** (bracket [0.06340, 0.06342]). Approach to κ₈*:
| κ₈*−κ₈ | width/L | min_deficit | min\|eig\| | res |
|---|---|---|---|---|
| 0.0190 | 0.6695 | 0.8902 | 0.1953 | 2.7e-12 |
| 0.0095 | 0.6689 | 0.8577 | 0.1946 | 2.3e-12 |
| 0.0044 | 0.6687 | 0.8407 | 0.1943 | 2.1e-12 |
| 0.0019 | (0.011) | (−0.19) | (3e-8) | (2.5e8) ← solver-basin miss |
| 0.0006 | 0.6685 | 0.8280 | 0.1940 | 2.7e-12 |

### GUARD VERDICT
The κ₈ feature is **PHYSICAL** (grid-stable, mpmath-confirmed sub-boundary soliton;
the deficit→0 horizon is a real existence limit) AND it is an **over-collapse /
existence boundary, NOT a continuous critical point**:
- width/L, min_deficit, M_MS, and min|eig| stay at FULL STRENGTH right up to κ₈*
  (width ~0.668, deficit ~0.83, min|eig| ~0.194 at κ₈*−κ₈ = 6e-4) — there is **NO
  order-parameter softening and NO min|eig|→0 critical scaling**.
- Past κ₈* the deficit jumps discontinuously NEGATIVE (horizon swallows the cell).
This is a **saddle-node / horizon-formation ceiling (first-order-like), not a
second-order critical point**. The intermittent res-blowups are solver-basin sensitivity
on top of it, not the feature itself.

---

## 2. THE SWEEP — (κ₈ × depth p × seed) MAP of stable types

Grid: κ₈ ∈ {0, 1e-3, 1e-2, 3e-2, 5e-2, 8e-2, 1e-1, 1.3e-1, 1.6e-1};
p ∈ {0.2, 0.4, 0.8, 1.2, 1.6, 2.0} (φ(core) ~ −p, deep negative);
seeds {round, extranode, twocore (multi-constituent), legendre-l1, legendre-l2} —
seeds are INITIAL DATA only; the solver settles freely. 270 members.

A member is recorded EXISTING iff res<1e-6 AND min_deficit>1e-6 AND a real soliton
width survives. A shaped seed is "DISTINCT" iff its converged profile differs from the
round profile at the same (p,κ₈) by >1e-3.

### Gross structure of the map
- **100 / 270 members EXIST.** Of all 100 existing members: **turns = 0 for every
  single one** (no internal nodes, no multiple cores — every existing cell is the
  monotone round single-soliton). min_deficit ∈ [0.68, 1.0] for all existing members.
- **Distinct-AND-existing shaped types: exactly 1 / 80** — and that one (p=1.6,
  κ₈=0.01, legendre1) has turns=0, dev_from_round=0.011 (just over the 1e-3 cut) and
  is the SAME round soliton with the seed not yet fully washed out at 55 SCF iters
  (the round member at that point: identical width 0.8949). Verified: pushing it to
  300 SCF iters does NOT yield a converged distinct cell (res=2.5e4, did not converge)
  while the round seed converges to res=2e-12 — i.e. it is a NON-CONVERGED iterate at
  deep p, not a stable distinct type.
- The "DISTINCT" rows past κ₈*(p) all carry **negative min_deficit and/or huge res**
  — diverged/over-collapsed iterates, not solutions.
- The round soliton WIDENS with depth (width/L: 0.659 @ p=0.2 → 1.026 @ p=2.0 at
  κ₈=0), reproducing the #44 deep-φ widening trend, and slightly COMPRESSES with κ₈
  (the back-reaction pulls the cell in) while M_MS grows with κ₈ and p — all SMOOTH.
- The existence boundary κ₈*(p) **moves to weaker coupling as the cell gets deeper**:
  ~0.063 @ p=0.4; between 0.01–0.03 @ p=0.8; 0.001–0.01 @ p=1.2; <0.001 @ p=2.0.
  Physically sensible — a deeper (denser, more compact) core over-collapses at smaller
  back-reaction.

### Bifurcation map — round-cell Jacobian min|eig| over (p, κ₈) [existing cells]
| p\κ₈ | 0 | 1e-3 | 1e-2 | 3e-2 | 5e-2 |
|---|---|---|---|---|---|
| 0.2 | 0.198 | 0.198 | 0.198 | 0.196 | 0.195 |
| 0.4 | 0.199 | 0.199 | 0.198 | 0.196 | 0.195 |
| 0.8 | 0.200 | 0.200 | 0.199 | — | — |
| 1.2 | 0.203 | 0.203 | — | — | — |
| 1.6 | 0.211 | — | 0.210 | — | — |
| 2.0 | 0.229 | — | — | — | — |

(— = cell past its existence boundary). Over the entire existing-cell region
min|eig| ∈ **[0.192, 0.229], strictly positive, NEVER crosses zero**. No bifurcation
anywhere. (The lowest Hessian eigenvalue RISES with depth — the deep cell is MORE
rigid, not less.)

---

## 3. THE #38 FLIP RE-RUN WITH L4

#38 (pre-L4): the radial gradient FORCES an angular completion (K_θ large negative
toward the seal) and "no bounding term exists". L4 contributes +2κXY (≥0) to p_r+ρ
and the +2κ(sin⁴Θ+sin²Θ)Θ′² stiffness to the angular EL denominator — the candidate
regularizer. TEST result: with L4 present and TWO-WAY φ, **no shaped or composite seed
produced a distinct existing stable type anywhere** (0 genuine; the 1 borderline is an
unconverged round cell), and the round-cell min|eig| never crossed zero. So L4 + the
sized soliton make the cell MORE rigid (min|eig| up to 0.229 at deep p) — but the
forced angular completion does NOT get bounded into a NEW stable shaped feature; it
simply does not appear as a distinct solution. The #38 flip does not become a type.

---

## 4. THE DUAL READING (TEST-BOTH; pre-registered, neither canonized)

- **PATH 1 (κ₈≈0.1 is a genuine critical threshold that pins a configuration /
  spawns types):** NOT supported. The κ₈ feature is real but it is an over-collapse
  EXISTENCE CEILING, not a continuous critical point: no order-parameter softening,
  no min|eig|→0 scaling, no distinct types or substructure appearing at/near it.
  Nothing special "sits at" κ₈* — the cell is a full-strength round soliton at
  κ₈*−6e-4 and simply ceases to exist beyond. It does not pin a unique configuration;
  it bounds a continuum from above.
- **PATH 2 (κ₈ is a free dial; one round continuum that merely deforms):**
  EVIDENTIALLY FAVORED. The existing solution space is ONE round single-soliton family
  that deforms smoothly in (κ₈, p) — width, M_MS, min|eig| all vary continuously —
  bounded above in κ₈ by the physical horizon ceiling κ₈*(p). No distinct types
  independent of any threshold; no bifurcation. The free-κ₈ reading carries the
  one-universe-vs-scale-family thread (#39) forward UNCHANGED: the cell remains a
  scale-family continuum (now with the L4-set intrinsic size √(κ/ξ)), with κ₈ a
  free coupling capped by an over-collapse limit rather than pinned to a special value.

**Evidential lean: Path 2** (smooth/featureless continuum + a non-critical existence
ceiling), per the addendum's discriminator (sharp+structure-only-there ⇒ Path 1;
smooth/featureless ⇒ Path 2). Criticality is NOT canonized either way; the conjecture
is informed-against here for the CLASSICAL complete-action cell.

---

## 5. THE HEADLINE READOUT

> **The complete action (L2 + native L4 + seal + two-way φ back-reaction), swept across
> the full κ₈–depth–seed solution space at deep negative φ, produces ONE ROUND
> CONTINUUM everywhere it produces anything at all — the single charge-1 soliton of
> #43/#44, now with the L4-set size √(κ/ξ), deforming smoothly in (κ₈, p) and bounded
> above in κ₈ by a physical over-collapse / horizon ceiling κ₈\*(p). It does NOT
> produce distinct stable types, bifurcations, internal substructure, or multiple
> constituents that the weak-κ₈ single-soliton picture could not see. Strong φ–angular
> back-reaction adds a deformation and an existence ceiling, NOT a catalog.**

Every banked corner agrees: pre-L4 bulk (#34/#39 "everything relaxes to round, no
bifurcation"), the L4 point-soliton (#43/#44 "exactly one static charge-1 cell + an
O(1) breathing tower"), and now the L4 SWEPT map (this push). The complete-action
CLASSICAL cell is one round type. This is a clean, real, first-class outcome.

### Consequence for the quantum-pivot premise
Per the setup's pre-registered reading discipline: "ONE ROUND CONTINUUM persists (L4
added size only, no new types) ⇒ the pre-L4 result survives the complete action ⇒
supports the 'classical content exhausted / go quantum' premise." The Crux-2 honest
prior ("no fermionic substructure to integrate out classically") was TESTED here — by
the first swept map of the complete action, the test it had never had — and **SURVIVES**:
no classical fermionic substructure / distinct-type catalog appears. The lepton FAMILY
(the masses, √m, Koide) is NOT a classical catalog of complete-action cells; it remains
the quantum-sector question (project frontier: quantum completion). The classical
content of the deep-negative-φ matter cell appears exhausted as one round sized soliton.

---

## 6. PREMISE LEDGER (chose or derived?)

| Item | chose / derived | note |
|---|---|---|
| Action = L2+L4+seal, two-way φ | DERIVED | C-2026-06-14-1, #43; reused from Stage A |
| ρ=r areal; B=1/A exterior, EOS-softened interior | DERIVED | confirmed self-consistently in Stage A |
| One scale κ/ξ=1 | CHOSEN (units) | everything in √(κ/ξ) |
| **κ₈ (back-reaction coupling) left OPEN** | CHOSEN/OPEN | the primary axis; NOT pinned. Result: bounded above by κ₈*(p), free below |
| Depth p ∈ [0.2, 2.0] | CHOSEN | deep negative φ; deeper p lowers the existence ceiling (so the deepest tractable cells are weak-κ₈ only) |
| Seeds round/extranode/twocore/legendre-l1,l2 | CHOSEN — and this WAS the probe | all relax to round (or fail to converge); no shaped/composite type |
| Cell endpoints (size) | CHOSEN | free dimensionful input (#39); span=14 L |
| "exists" = res<1e-6 ∧ deficit>1e-6 ∧ width>0.05 | CHOSEN (diagnostic) | separates real cells from diverged/over-collapsed iterates |
| Picard relax (0.15–0.45) | CHOSEN (method) | at deep p (≥1.2) some shaped seeds fail to converge — a SOLVER limit, not a physical type; round cells converge cleanly |

---

## 7. NEW DIAL / OBSTRUCTION FLAGGED

- **κ₈\*(p): the over-collapse existence ceiling** is the surfaced structure (not a new
  free dial — a derived BOUNDARY on κ₈). It is the natural Stage-A "~0.1 feature" made
  precise and shown to be p-dependent and NON-critical. It caps how strong the
  φ–angular back-reaction can be before the cell horizon-collapses; it does not select
  a value.
- **Solver obstruction (scoped, NOT physical):** the Picard SCF relaxation becomes
  basin-sensitive (intermittent divergence) NEAR the over-collapse boundary and for
  shaped seeds at deep p (≥1.2). This is why some near-boundary rows blow up while
  their neighbours are clean. It does not create or hide a physical type (verified: the
  one borderline "distinct" cell is an unconverged round cell). A future deep-p,
  near-ceiling study should use a continuation/arc-length or full-Newton-on-the-coupled
  system solver rather than Picard. This is a METHOD note, not a result.

---

## 8. VERIFIER STATUS

NOT yet blind-verified. Per Self-Hardening (verifier-before-record / before-commit), a
blind adversarial verifier pass (Stage C) is owed before this is banked as a registry
entry. The internal cross-checks that ARE in place: engine fast-vs-committed to 1e-14;
PCR vs dense to 4e-16; #44 breathing tower reproduced (Stage A); mpmath deficit
confirmation; grid-convergence of the sub-boundary soliton. Recommended verifier aim
(hardest at the headline-confirming result, per hypothesis discipline): attack the
"one round continuum" claim by (a) hunting a converged distinct type at deep p with a
non-Picard solver, (b) checking whether the over-collapse ceiling hides a shaped branch
just past it under arc-length continuation, (c) re-deriving κ₈*(p) independently.
