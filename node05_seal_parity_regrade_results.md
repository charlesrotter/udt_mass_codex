# NODE 0.5 — Seal parity→BC rule re-graded on the native field equations (Fork-3b, ω≠0 reframe)

**Status: BANKED (Charles 2026-07-04). Blind-verified. No numeric compute — symbolic/CAS re-grade.**
Deriver agent a648221a6b7df3aba; blind adversarial verifier ad14fbc6898ee1930.
Part of the ω≠0 angular-sector reframe (`microphysics_reentry_omega_reframe_MAP.md`, NODE 0.5).

## Purpose
Re-grade the pre-foundation seal parity rule (`seal_junction_condition_results.md`, 2026-06-21 —
predates the 2026-07-01 native field equations) against the current native foundation, per Charles's
MAP ruling #2 ("durable canon = only seal = t→−t mirror fold; even/odd→Neumann/Dirichlet must be
re-derived or corrected"). Load-bearing because NODE 1 (the parity crux) rests on it.

## Verdict: CORRECTED (mechanism survives natively; the involution is sector-split; φ's BC flips to Dirichlet)

### 1. The reflection BC structure is native (C1 SUPPORTED)
Varying `S = ∫ c√h[(Z_φ/2)φ'² + R^{(2)} + W_χ𝒦 + L_m]` (native_geometric_action_results.md:13;
native_field_equations_constrained_two_player_results.md:98) in r gives the boundary term on
`π_φ = ∂ℒ/∂φ' = c√h·Z_φ·φ'` (round `q=Zρ²φ'`), reproducing the banked JC1 `[π_φ]=0`
(universe_cell_fold_jc_sigma_results.md:26-30). The Weierstrass–Erdmann/Z₂-quotient dichotomy —
**field ODD under the seal involution → Dirichlet (field=0, normal-deriv free); EVEN → Neumann
(normal-deriv=0)** — is the correct native boundary structure. Caveat (the C2/C4 seam): "Dirichlet/
Neumann as a RADIAL BC at the seal" holds only when the involution's fixed surface IS the spatial
fold r=r_s; for a purely temporal involution the fixed surface is t=0 and "Dirichlet" degenerates to
a node-in-time (ω-blind).

### 2. SECTOR SPLIT: static seal BCs from the spatial depth mirror, not t→−t (C2 SUPPORTED as re-localization)
The involution that sets the STATIC fields' seal BCs is the **spatial depth mirror
σ_φ:(φ→−φ, r→radial reflection)**, NOT the temporal t→−t. Independently verified:
- (a) a static φ=φ(r) is t-independent ⇒ t→−t acts trivially ⇒ imposes NO radial BC (only a
  node-in-time, satisfied ∀ω — seal_junction_condition_results.md:95-101);
- (b) under the reciprocal tie g_tt g_rr=−c² (C-2026-06-18-1, CANON.md:186), φ→−φ SWAPS g_tt↔g_rr
  (a "c dt ↔ dr" duality), categorically distinct from t→−t (which leaves the static diagonal metric
  invariant). σ_φ's fixed surface is φ=0=r_s (spatial) ⇒ it CAN impose a radial BC;
- (c) in the record the "seal = t→−t" LABEL was only ROW-CONDITIONAL / slot-dependent
  (F4_seal_boundary_MAP.md:58,79,262-267; competing P×T at seal_junction_condition_results.md:46-47);
  the theorem-grade pillar was always the FOLD (seal≠edge, Z₂ quotient), never the temporal label.

**This RE-LOCALIZES, it does not contradict, the canon.** Canon's primary wording is "mirrored across
φ→−φ" (CANON.md:30); the fold-JC derivation ALREADY used φ→−φ to pin the static fields
(universe_cell_fold_jc_sigma_results.md:14,26-30). Canonized as clarification **C-2026-07-04-1**:
σ_φ governs static fields; t→−t governs the time-on/off-diagonal sector.

### 3. φ's seal BC is CORRECTED Neumann→Dirichlet (C3 SUPPORTED, strengthened)
φ is ODD under σ_φ (φ→−φ) ⇒ **Dirichlet φ(r_s)=0**, φ' FREE ⇒ flux seal q=Zρ_s²φ'
(universe_cell_fold_jc_sigma_results.md:26-30) — matches the already-derived fold JC. The
pre-foundation doc assigned φ EVEN→Neumann d_nφ=0 (seal_junction_condition_results.md:69,92) — the
OPPOSITE, and a genuine ERROR: Neumann φ'(r_s)=0 would zero q, destroying the flux seal (q>0 forced,
universe_cell_fold_jc_sigma_results.md:35). **The old φ-Neumann wording is retired.**

### 4. Per-field native seal BC inventory (under σ_φ for static, t→−t for time-on)
| Field | parity | native seal BC |
|---|---|---|
| φ(r) depth | ODD under σ_φ | Dirichlet φ(r_s)=0; φ' free ⇒ q=Zρ_s²φ' (flux seal) |
| h_AB/ρ transverse | EVEN under σ_φ | Neumann ρ'(r_s)=0 |
| H=g_tr off-diagonal | ODD under spatial P (one dr flips) | Dirichlet H(r_s)=0 (value robust; mechanism = spatial P, not t→−t; frozen in round-static) |
| n_a/Θ carrier, internal phase | matter-sector fork (f_r=0 CHOSE); time-on phase → t→−t sector | OPEN — NODE 1 |

## What is NOT banked (held open → NODE 1)
The "seal ignores ω" lead (a spinning phase is even under σ_φ) is **INCOMPLETE / unsafe** (C4). A
spinning phase Nψ+ωt is a TIME-ON object, governed by t→−t (→ Nψ−ωt, the counter-rotating mirror);
applying only the static-sector σ_φ to it is a category error (it switches to the involution that
gives the vacuous "ignore" answer — an observing-vs-targeting tripwire, and it contradicts the
approved MAP:233 which already states the phase is odd under t→−t). Verifier verdict: not refuted
but not bankable; must be run through NODE 1's t→−t test. **NODE 1 = whether the seal kills / pins /
permits ω for the counter-rotating-mirror matching.**

## Provenance / discipline
- Symbolic/CAS/paper only; no numeric solve, no grid. Derived natively from δS / Weierstrass–Erdmann;
  no GR tensor or GR junction form invoked (verifier GR-smuggle check: none in C1–C4).
- Deriver a648221a6b7df3aba (2026-07-04). Blind adversarial verifier ad14fbc6898ee1930 (2026-07-04):
  C1 SUPPORTED, C2 SUPPORTED-as-re-localization (revision: word as sector-split, folded in), C3
  SUPPORTED-strengthened, C4 INCOMPLETE (held open).
- Canon: C-2026-07-04-1 (clarification). Premise tags: odd φ→−φ identification DERIVED within the
  pointwise class (class = CHOSE, loophole probed); φ(r_s)=0 DERIVED given φ-continuity (continuity
  posture CHOSE-cited, canon-anchored C-2026-06-10-2).
