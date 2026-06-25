# RESULTS — Micro Mass-Shape of UDT's Own Soliton (DEPTH × WINDING)

Research record (append-never-edit). Driver: Claude (Opus 4.8, 1M). 2026-06-15.
OBSERVE push, first step of the observation-led reframe ([[reframe-observation-led]]):
characterize the mass-pattern UDT's geometry NATURALLY makes across its two native
axes — dilation DEPTH (p) and topological WINDING (m) — and report WHAT IS THERE.

*** DATA-BLIND ***: NO empirical particle data loaded, recalled, fit, or compared.
Everything in intrinsic units L = √(κ/ξ) = 1 and as INTERNAL ratios. The
comparison-to-nature is a separate gated step, NOT made here.

NOT a type-sweep (that is closed: #52, ONE round charge-1 continuum). This takes the
SETTLED soliton and maps the SHAPE of M_MS(p, m), the charge along each axis, where
native discreteness lives, and the raw size/energy/deficit structure.

Scripts (committed with this doc):
- `micro_mass_shape.py` — the depth march, winding tower, surface, charge/energy
  readouts, mpmath anchor, grid check.
- Data: `micro_mass_shape_data.json`.
- REUSES the committed physics primitives (`theta_ddot`, `stress`, `energy_pieces`,
  `phi_from_source`, `grad_central` from `complete_metric_batched.py`) VERBATIM,
  driven by the INDEPENDENT damped full-Newton on the joint (Θ,φ) field
  (`CoupledSystem`, `coupled_newton` from `verify_stageB_indep.py`) — the robust
  non-Picard solver. Physics not rebuilt; the solver's USE extended.

---

## 0. Numerics / provenance (principle 2 honored)

Full nonlinear angular EL + nonlinear Misner-Sharp t-equation, two-way φ. NO
linearization as a result. Sanctioned function-replacement only (trapezoid, FD
Jacobian, transient exp-arg clamp — converged solutions never touch it). V100 float64;
the independent full-Newton uses a dense numerical Jacobian (no banded ansatz that
could mask a nonlocal branch). Anchors / checks:
- **mpmath dps=40** at the deepest cell (p=6.0): M_MS float64 = 5720.4424933391,
  mpmath = 5720.4424933391, |diff| = **2.7e-12** — the deep-φ M_MS is not a float64
  artifact.
- **grid refinement** (m=2 winding, p=0.4): M_MS 0.19018 (N=240) → 0.18940 (N=360);
  min|eig| 0.1851 → 0.1814; res ~1e-13 — the winding-2 cell is resolution-stable.

---

## 1. MAP 1 — M_MS(DEPTH) at fixed winding m=1 (kap8=0.01, sub-ceiling)

Warm-started depth march, the round charge-1 soliton, p ∈ [0.2, 6.0]. (p = the
core-depth dial; |φ_core| = the genuine deepest φ realized in the cell.)

| p | φ_min (true depth) | M_MS | width/L | min_deficit | min\|eig\| | degree | E2 | E4 |
|---|---|---|---|---|---|---|---|---|
| 0.2 | −1.128 | 0.06046 | 0.664 | 0.983 | 0.1975 | 1.000 | 23.31 | 22.44 |
| 0.4 | −1.128 | 0.06263 | 0.679 | 1.000 | 0.1978 | 1.000 | 23.79 | 22.42 |
| 0.6 | −1.128 | 0.06572 | 0.698 | 1.000 | 0.1983 | 1.000 | 24.45 | 22.41 |
| 0.8 | −1.128 | 0.07010 | 0.723 | 1.000 | 0.1991 | 1.000 | 25.35 | 22.43 |
| 1.0 | −1.128 | 0.07624 | 0.755 | 1.000 | 0.2003 | 1.000 | 26.53 | 22.51 |
| 1.2 | −1.128 | 0.08480 | 0.794 | 1.000 | 0.2022 | 1.000 | 28.07 | 22.67 |
| 1.6 | −1.269 | 0.11313 | 0.893 | 1.000 | 0.2095 | 1.000 | 32.51 | 23.40 |
| 2.0 | −1.658 | 0.16823 | 1.017 | 1.000 | 0.2271 | 1.000 | 39.34 | 25.01 |
| 2.5 | −2.152 | 0.32373 | 1.196 | 1.000 | 0.2840 | 1.000 | 52.67 | 28.99 |
| 3.0 | −2.649 | 0.75516 | 1.376 | 1.000 | 0.4433 | 1.000 | 73.92 | 36.68 |
| 3.5 | −3.145 | 2.27364 | 1.517 | 1.000 | 0.9148 | 1.000 | 106.99 | 51.66 |
| 4.0 | −3.637 | 10.4502 | 1.564 | 1.000 | 2.4312 | 1.000 | 154.27 | 87.10 |
| 5.0 | −4.541 | 442.814 | 1.084 | 1.000 | 18.437 | 1.000 | 229.96 | 684.92 |
| 6.0 | −5.436 | 5720.44 | 0.394 | 1.000 | 135.77 | 1.000 | 303.20 | 3227.6 |

### Functional form of M_MS(depth) — THE HEADLINE OF THIS AXIS
- **Faster-than-exponential, faster-than-power-law in the dial p.** Best single-form
  fits over the whole range: ln M = −4.569 + **1.903 p** (R²=0.908); M ~ p^2.75
  (R²=0.586). Neither is clean — the GROWTH ACCELERATES.
- **The slope is NOT constant** (not geometric): the local logarithmic derivative
  **d ln M_MS/dp rises monotonically from ~0.18 (shallow) to ~3.3 (deep)** before the
  cell starts compressing near p~5–6. So M_MS(depth) is a *super-exponential* /
  upward-curving function of the dial, not a fixed-ratio ladder.
- **Cleaner against the TRUE depth |φ_core|** (the realized deepest φ, the
  physically meaningful "depth"): ln M = −5.72 + **2.45 |φ_core|** (R²=0.965). Still
  the slope drifts (d ln M/d|φ_core| ≈ 1.2 → 3.5 across the deep span), so even
  against true depth it is upward-curving, not a single exponential rate.
- **A two-regime structure emerges in the dial→depth map (unforced):** for p ≲ 1.2 the
  realized |φ_core| sits PINNED at ~1.13 (the L4 stiffness / closure floor: the dial
  barely deepens the core) while M_MS still creeps up via the WIDTH (0.66→0.79); for
  p ≳ 1.6 the core genuinely deepens (|φ_core| → 5.4) and M_MS turns sharply upward.
  The mass family along depth is SMOOTH and CONTINUOUS — no steps, no gaps.

### κ8-dependence of the shape (new dial; sub-ceiling)
The depth-slope is itself κ8-dependent: at κ8=0.03 the shallow-range slope drops to
ln M = −1.82 + **0.29 p** (R²=0.973) vs **1.90 p** at κ8=0.01 (note the κ8=0.03 fit
spans only p≤1.0 — the over-collapse ceiling κ8*(p) of #52 forbids the deep cells at
κ8=0.03). κ8 sets the OVERALL mass scale (M_MS grows with κ8, #52) AND modulates the
depth-growth rate; it does NOT change the qualitative upward-curving form.

---

## 2. MAP 2 — M_MS(WINDING) tower (kap8=0.01)

The winding sector m=1,2,3,… (cold full-Newton from a monotone degree-m hedgehog seed).

### What ROBUSTLY converges (grid-stable, min|eig|>0)
| depth p | m | M_MS | M_MS/M_MS(1) | width/L | ncross | min\|eig\| | degree | area_form | E2 | E4 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.4 | 1 | 0.06275 | 1.000 | 0.684 | 1 | 0.1977 | 1.000 | 0.636 | 23.97 | 22.35 |
| 0.4 | 2 | 0.18981 | **3.025** | 1.165 | 2 | 0.1837 | 2.000 | 1.270 | 102.28 | 97.46 |
| 0.8 | 1 | 0.08056 | 1.000 | 0.733 | 1 | 0.1988 | 1.000 | 0.636 | 25.75 | 22.25 |

- **m=1 and m=2 are genuine, distinct, grid-stable solitons** (min|eig|>0). m=2 carries
  degree 2 (ncross=2; area_form 1.270 = 2×0.636) — a genuinely DIFFERENT topological
  charge. Reproduces the #52 verifier's m=2 grid-stable result.
- **Internal winding ratio M_MS(2)/M_MS(1) = 3.02 at p=0.4.** Mass grows
  SUPER-LINEARLY with winding (3× the mass for 2× the charge), broadly the standard
  topological-soliton behaviour where higher charge costs more than proportional
  energy. Both E2 and E4 jump ~4× from m=1 to m=2.

### What did NOT robustly converge (solver-scoped, NOT a physics claim)
m=3, m=4 did not converge to a grid-stable cell with the cold full-Newton at any tested
(p, κ8); m=2 at p=0.8 and even m=1 at p=1.2 failed from the COLD seed though MAP 1's
warm-started march holds m=1 to p=6. This is a **solver-basin limitation of the cold
dense-Jacobian Newton at higher m / deeper p**, the same fragility the #52 verifier
flagged (m=3 "borderline": converged at N=240 but failed to grid-refine). It is NOT
evidence the higher-winding cells do not exist — only that they are not robustly
reachable cold. The robust tower content here is m=1 (all depths) and m=2 (shallow).
The winding family beyond m=2 remains an OPEN topological route (registry #52d).

---

## 3. MAP 3 — the COMBINED M_MS(p, m) surface (kap8=0.01)

| M_MS | m=1 | m=2 | m=3 |
|---|---|---|---|
| p=0.4 | 0.06275 | 0.18981 | (cold-seed non-conv) |
| p=0.8 | 0.08056 | (cold-seed non-conv) | (cold-seed non-conv) |
| p=1.2 | (cold-seed non-conv*) | — | — |

(*m=1 p=1.2 DOES exist — MAP 1's warm-started march gives M_MS=0.0848; the blank here
is the cold-seed solver failing, not absence.) The robustly-mapped corner of the
surface shows the two axes act roughly MULTIPLICATIVELY on the mass scale: depth lifts
M_MS smoothly at fixed m; winding multiplies it by ~3 per unit charge at fixed p.

---

## 4. THE DISCRETENESS QUESTION (honest verdict)

> **Native discreteness lives in the WINDING axis ONLY. The DEPTH axis is a
> CONTINUUM with no native selector.**

- **DEPTH (p / φ_core): CONTINUOUS, no native discreteness.** Every value of p tested
  converged to a soliton; M_MS(p) is a smooth, continuous, monotone function (§1). The
  #52 guard already showed the κ8 over-collapse ceiling κ8*(p) is a NON-critical
  saddle-node/horizon existence edge with no order-parameter softening — it CAPS the
  cell, it does not SELECT special depths. The seal/regularity/min|eig| all vary
  smoothly with depth (min|eig| stays >0, in fact RISES — the deep cell is more
  rigid). **Nothing picks out discrete depths.** A family-at-discrete-depths would
  REQUIRE an external selector that this geometry does not contain.
- **WINDING (m): NATIVELY DISCRETE.** m is the topological degree of the n: cell→S²
  map — an integer Dirichlet label (Θ(core)=mπ), not a continuous dial. The charge
  readouts confirm it: degree ∈ {1, 2}, area_form ∈ {0.636, 1.270} = integer multiples
  of the unit. There is no "m=1.5". This is the one place a native, integer, gap-free
  discreteness lives.

CONTRAST: the depth axis supplies a CONTINUOUS one-parameter mass family at fixed
charge; the winding axis supplies a DISCRETE charge ladder. They are different KINDS
of structure.

---

## 5. CHARGE ALONG EACH AXIS (verdict)

> **CONFIRMED: DEPTH = same-charge / different-mass; WINDING = different-charge.**

- **Along DEPTH (m=1, p=0.2…6.0):** topological degree = **1.000 at every depth**
  (charge spread = 0.00000). The area_form drifts only mildly (0.636→0.583) as the
  deep profile compresses — that is a *shape* deformation of a fixed-degree map, not a
  charge change; the degree (the topological invariant) is pinned at 1. **The depth
  axis is the SAME-CHARGE mass-family axis** — a one-parameter family of charge-1 cells
  of different mass. This is the "generation-like" axis (same charge, different mass),
  CONFIRMED.
- **Along WINDING:** degree = m exactly (1, 2; ncross=1, 2; area_form 0.636, 1.270).
  **The winding axis is the DIFFERENT-CHARGE axis.** CONFIRMED.

So the two native axes cleanly separate: WINDING moves the charge (discrete), DEPTH
moves the mass at fixed charge (continuous).

---

## 6. OTHER NATIVE STRUCTURE (raw "what these knots are like")

- **Size (width/L):** along DEPTH the cell WIDENS with p (0.66 → ~1.56 at p=4) then
  COMPRESSES at extreme depth (0.39 at p=6) — a non-monotone size response: moderate
  deepening swells the knot, extreme deepening crushes it. Along WINDING the cell
  widens with m (0.68 → 1.16 from m=1 to m=2 at p=0.4) — higher charge is a bigger knot.
- **Energy decomposition (E2 / E4):** at shallow depth E2 ≈ E4 (~23 each, near-BPS-like
  balance). Deepening grows E2 while E4 stays ~flat until p≳3, then at extreme depth
  (p≥5) E4 EXPLODES and dominates (E4=3228 vs E2=303 at p=6) — the runaway mass at deep
  φ is L4 (the stabilizer / winding-current term) driven, coincident with the
  super-exponential M_MS turn-up and the size compression. Along WINDING both E2 and E4
  scale up together (~4× from m=1 to m=2).
- **Deficit:** min_deficit ≈ 1.0 across the entire depth range at κ8=0.01 (the cell is
  far from the horizon ceiling at weak κ8) — confirming the deep-mass growth here is
  NOT a near-collapse artifact.
- **Rigidity:** min|eig| > 0 everywhere mapped (0.18–136), RISING with depth — every
  cell is a stable soliton, the deep ones increasingly rigid.

---

## 7. PREMISE LEDGER (chose or derived?)

| Item | chose / derived | note |
|---|---|---|
| Action = L2+L4+seal, two-way φ | DERIVED | C-2026-06-14-1, #43; reused verbatim |
| ρ=r areal; B=1/A exterior, EOS-softened interior | DERIVED | confirmed in #52 |
| One scale κ/ξ=1 | CHOSEN (units) | everything in √(κ/ξ) |
| κ8 = 0.01 (primary depth march) | CHOSEN | sub-ceiling weak coupling; κ8 is the #52 free dial capped by κ8*(p). κ8=0.03 cross-check shows κ8 modulates the depth-slope |
| Depth dial p ∈ [0.2, 6.0] | CHOSEN | the same-charge mass-family axis; the realized depth is |φ_core| |
| Winding m (integer Dirichlet label) | DERIVED (topological) | the native discrete charge axis; degree = m |
| Charge = topological degree / H1 area-form | DERIVED | the native winding charge (registry C-2026-06-14-1); reported unit-free (q=1/3 a fixed multiplier, never compared to data) |
| Cell endpoints (size), span=14 L | CHOSEN | free dimensionful input (#39) |
| "exists" = res<1e-6 ∧ deficit>1e-6 ∧ width>0 ∧ converged | CHOSEN (diagnostic) | separates real cells from non-converged iterates |
| Cold full-Newton seed for the tower | CHOSEN (method) | basin-fragile at m≥3 / deep p — a SOLVER limit, not a physical absence |

---

## 8. NEW DIAL / STRUCTURE FLAGGED

- **The dial→depth saturation (p ≲ 1.2 pins |φ_core| ~ 1.13):** the core-depth DIAL p
  and the REALIZED depth |φ_core| are NOT equal at shallow p — the L4 stiffness/closure
  imposes a depth floor, so the dial only bites for p ≳ 1.6. Reported as a structural
  observation; the mass-form headline is stated against both the dial and the true depth.
- **κ8 modulates the depth-growth RATE** (slope 1.90 → 0.29 from κ8=0.01 → 0.03), not
  just the overall scale — a new facet of Charles's φ-angular-coupling axis. Sub-ceiling
  only (κ8*(p) caps the deep cells).
- **Solver obstruction (scoped, NOT physical):** the cold dense-Jacobian full-Newton is
  basin-fragile for m≥3 and for any m at deeper p from a cold seed; warm-starting
  (MAP 1) cures it for m=1. A future tower study should warm-start in m (continuation
  m→m+1) and/or in p. METHOD note, not a result.

---

## 9. THE HEADLINE READOUT (DATA-BLIND)

> **UDT's own soliton makes mass on two cleanly-separated native axes. The DEPTH axis
> is a CONTINUOUS, SAME-CHARGE (degree-1) mass family whose M_MS grows
> SUPER-EXPONENTIALLY / upward-curving with depth — d ln M_MS/dp climbs from ~0.2 to
> ~3.3, NOT a fixed-ratio geometric ladder — driven at extreme depth by the L4 winding-
> current energy, with NO native selector picking out special/discrete depths. The
> WINDING axis is NATIVELY DISCRETE (integer degree m): a DIFFERENT-CHARGE ladder whose
> mass grows super-linearly with charge (M_MS(2)/M_MS(1) ≈ 3.0). Native discreteness
> lives in WINDING; the depth mass-family is a continuum.**

### What raw material this hands the (later, gated) comparison-to-observation step
(ONE honest sentence, NO comparison made): the geometry natively offers a continuous,
same-charge, super-exponentially-growing one-parameter mass family (DEPTH) and a
discrete different-charge ladder (WINDING) — and whether a same-charge mass pattern in
nature lines up with the depth family's specific upward-curving shape (and what would
fix the depths, since the geometry supplies no native selector) is exactly the question
the gated step would ask, NOT settled here.

---

## 10. VERIFIER STATUS

NOT yet blind-verified. Per Self-Hardening (verifier-before-record), a blind
adversarial verifier pass is owed before this is banked as a registry entry. Internal
checks in place: mpmath dps=40 deep-M_MS anchor (|diff|=2.7e-12); m=2 grid refinement
(N=240→360 stable); reuse of the #52-validated independent full-Newton engine; the m=2
result reproduces the #52 verifier's independent finding. Recommended verifier aim
(hardest at the headline-confirming result): (a) re-derive the M_MS(depth) slope and
its curvature with an independent quadrature / higher dps at several depths; (b)
warm-start the winding tower in m to test whether m≥3 cells exist and where they
destabilize (does the tower TERMINATE at a native max winding, or is it solver-limited);
(c) independently confirm degree=1 is pinned along the whole depth axis (the
same-charge verdict) and degree=m along winding.
