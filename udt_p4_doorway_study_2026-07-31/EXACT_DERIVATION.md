# P4 doorway study — exact derivation record (staged; contract: PREREGISTRATION.md, frozen)

Date: 2026-07-31. Branch: grok. Script: `derive_doorway_study.py` (exact SymPy, no floats/
numeric solvers/GPU, deterministic, exit nonzero on failure). Honest split: SUBSTANTIVE
zero-residual checks vs GUARD citation/typing rows, labeled in-script and in the JSON.

**Standing stamps (travel with every claim):** registered stationary one-parameter
presentation (fields (φ, f, bh), jets ≤ 2); registered positive triangular chart; cell
x ∈ [−ℓ, ℓ]; the R×S³ arena enters ONLY through the banked Hopf connection A = σ₃ and the
banked cap census (dets recomputed here); census/pairing/posture branches carried, NONE
adopted; parity data SUPPLIED never valued; off-shell typing computations; the hopfion lane
appears ONLY as a one-way comparison target (F-D4). Registration ≠ adoption throughout.

## Stage 1 — C1 (the arena's own Hopf fiber circle): FAILS-AS-GLOBAL-PROMOTION;
## DELIVERS the owned target circle + the owned circle-valued transition datum

- `C1a_hopf_connection_not_closed` + `C1a_chern_obstruction_integral`: dσ₃ =
  −sinθ dθ∧dφ ≠ 0 exactly; ∫_{S²} dσ₃ = −4π ≠ 0 (one fiber period 4π; Chern ±1). A global
  fiber-phase FIELD F with dF = σ₃ would force dσ₃ = 0 — **the promotion of the fiber phase
  to a single global circle-valued field FAILS with this exact obstruction** (no global
  section; not a solver gap, a derived topological fact of the banked connection).
- `C1b_local_potentials_both_valid` + `C1b_transition_is_circle_valued_winding_one`:
  per-chart fiber phases DO exist (potentials (cosθ∓1)dφ regular at the respective poles);
  their mismatch is −2dφ, equatorial loop integral −4π = (−1)·(fiber period): **the
  chart-transition datum of the fiber phase is CIRCLE-VALUED with winding 1 — the theory
  OWNS a circle-valued transition law even though it owns no global circle-valued field.**
- `C1a_chern_second_route_stokes_credited` (CREDITED ADOPTION, verifier G1, finishing
  pass): the Chern obstruction −4π re-derived by a SECOND route — Stokes via the verifier's
  own trivializations ψ_N = ψ+φ, ψ_S = ψ−φ (equatorial loop integral of a_N − a_S), exact
  agreement with the direct S² integration: two independent routes, one integer.
- `C1c` [guard]: the registered fields (φ, f, bh) are real; the fiber phase is not among
  them; promotion = ADDING a field = C5's question, with C1 delivering an OWNED target
  (the fiber circle, period 4π) and an OWNED transition datum (the Hopf cocycle).
- `C1d_cap_census_dets_recomputed_all_unit` + `C1d_no_winding_home_in_arena_cycles`: all
  104 banked two-cap pairs' determinants recomputed from the cap vectors, all match the
  banked column, all |det| = 1 ⇒ π₁(capped arena) TRIVIAL (re-instantiated); winding = a
  hom π₁ → ℤ ⇒ **identically zero on every 1-cycle of the capped S³/toric sector.**

**C1 verdict: CONSTRAINED (exact).** No global promotion (Chern obstruction −4π ≠ 0); the
owned content that DOES promote: the target circle and the circle-valued transition law —
routed to C5 as owned inputs. Its R9 content on arena cycles: none (π₁ trivial).

## Stage 1 — C2 (the toric angles): FAILS — the banked capped/torsion obstruction is the killer

- `C2a_toric_angle_winding_one_at_cap` + `C2a_arc_confined_loop_has_zero_winding`: the
  toric angle has winding 1 on any loop around its cap axis (exact); an arc-confined loop
  has winding 0 (the only 2πℤ element with |·| < 2π is 0, exact); with winding's
  homotopy/radius invariance (NAMED Category-A) the angle admits NO continuous extension
  over the cap: **the toric angle is not a field on the capped arena at all.** [O4 note
  (verifier): the SymPy content of C2a is deliberately thin (a period integral + a
  lattice-point fact); the load-bearing step is the NAMED Category-A winding-invariance —
  banked convention, honest because named.]
- `C2b` [guard]: π₁ trivial (C1d, recomputed) + the banked live-cycle census (CITED:
  completion cycle + J11 loops only) ⇒ a toric winding has NOWHERE to live; an x-dependent
  phase on the completion cycle is not a toric angle but a NEW field (= C5).

**C2 verdict: FAILS (exact).** The winding would have to live on capped/torsion cycles that
cannot carry it; the candidate cannot even be globally defined. The failure form is exactly
the banked obstruction, confronted head-on — nothing new was needed to kill it.

## Stage 2 — C3 (the screen SO(2)): FAILS-ON-BANKED-FOOTING — the owned circle was SPENT AS GAUGE

- `C3a_screen_SO2_is_owned_circle`: R′ = J·R, R(0) = I (Picard-named), R(2π) = I,
  R(π) = −I ≠ I: **the screen SO(2) is a genuine owned compact circle** (period 2π) — the
  one compact group anywhere in the banked equivariance.
- `C3b_chart_keeps_only_2torsion_of_circle`: SO(2) ∩ (chart-compatible signed diagonals)
  ⟺ sin t = 0 ⟺ t ∈ πℤ, values diag((−1)ⁿ,(−1)ⁿ) = {I, −I} — the 2-TORSION subgroup only.
- `C3b_K4_characters_are_real_points_of_U1`: {z real, z² = 1} = {±1} exactly — **the banked
  K₄ screen characters ±1 are precisely the REAL POINTS of the owned circle: the
  real-targets theorem and the owned SO(2) are one structure seen through the chart.**
  [O3 nuance (verifier): the identification is of character VALUES {±1} and of the
  chart-surviving subgroup {I, −I}; K₄ itself (order 4) does NOT embed in the circle — two
  of its four screen blocks (diag(−1,1), diag(1,−1)) are det = −1 non-circle members. The
  lay phrase "one structure seen through the chart" is to be read with this nuance.]
- `C3b_triangular_chart_group_no_compact_subgroup`: the registered chart's block group
  (ρ = e^{ΔxH}, positive-triangular Q, L) owns NO nontrivial compact subgroup (diagonal:
  real-exp point kernel; strictly-lower: nilpotent, exp = I + TX).
- `C3c_dressing_anchored_to_zero`: θ′ + 2k_mod(x)θ = 0, θ(0) = 0 ⇒ θ ≡ 0 (exact dsolve;
  Route D §1.5 recomputed): on the anchored footing the SO(2) phase is PURE PRESENTATION.

**C3 verdict: FAILS-ON-BANKED-FOOTING (exact failure form, the informative one):** the
theory OWNS a compact circle, and the banked registration SPENT it — the triangular chart
+ anchor quotient it to its 2-torsion {±1} (= the K₄ characters = the real points of U(1)).
Promotion without unfixing chart/anchor adds no invariant content (F-D5 would fire);
unfixing them is a change of the banked FOOTING itself — typed, out of this study's scope.

## Stage 2 — C4 (E07/E08 ℝ-subgroups): FAILS as expected — adjudicated exactly

- `C4a_E07_point_kernel`: e^{T·diag(−k,k)} = I ⟺ Tk = 0 ⟺ T = 0 (k ≠ 0): closed
  ℝ-embedding, real spectrum, point kernel; same form kills H = diag(−1,+1).
- `C4b_E08_solvable_no_torsion_no_compact`: the banked E08 law u₁₂ = u₁ + e^{−φ₁}u₂
  (associativity recomputed, zero residual) generates ℝ ⋉ ℝ, simply-connected solvable: an
  n-th root of identity forces φ = 0 then u = 0 (n = 2, 3 exact): NO torsion, NO compact
  subgroup at any parameter value.

**C4 verdict: FAILS (exact).** The failure form is the real-targets theorem at GROUP level:
real spectrum / solvable simply-connected. Compactness is unreachable from the banked
strata by parameter motion — the E07/E08 axes can never close into circles.

## Stage 3 — C5 (a NEW registered S¹-valued field θ(x)): REGISTERS at Route-D-analog grade,
## REGISTERED-POSIT tag — every legality DERIVED, none asserted (F-D2)

- `C5a_periodicity_legality_rule`: a bulk entry F(θ) is well-defined on ℝ/2πℤ iff
  F(θ+2π) = F(θ): bare/linear θ EXCLUDED (residual 2π ≠ 0); cos θ, sin θ, e^{iθ} LEGAL
  (zero residual) — **the imaginary exponent enters the alphabet legally through derived
  target well-definedness**, exactly the entry the period gate's real-targets theorem
  said was missing.
- `C5a_jets_are_real_and_lift_independent`: θ′, θ″ lift-independent REAL local entries
  (d/dx kills 2πℤ constants) — N2-analog legality.
- `C5b_nonlocal_exclusion_travels`: the anchored nonlocal entry ∫₀ˣθ′du (= the real lift
  θ̃(x) − θ̃(0)) FAILS the banked co-translation test (witness residual −s², exact): the
  bare-φ/nonlocal-m exclusions TRAVEL — the alphabet sees e^{iθ} and jets, never the lift.
- `C5c_two_sided_law_admits_central_U1_factor`: the banked two-sided twisted law
  L(γ₂∘γ₁) = Q₂L₁ + L₂ρ₁ with an adjoined multiplicative slot u = e^{iψ}: associativity
  zero-residual on fully generic 2×2 blocks; (ρ,Q,L) untouched; reversal u·ū = 1. **The
  compact version of the banked law EXISTS: the law ADMITS a central U(1) factor** — and by
  C3b/C4 the factor is ADJOINED, not owned (this is what earns the REGISTERED-POSIT tag).
  [O1 caveat (verifier): a central U(1) factor is direct-product-admissible for ANY
  associative law — C5c ALONE has no discriminating power; the discriminating content is
  the base-law associativity re-proof plus the C3b/C4 owned-nowhere result. Future readers
  must not read C5c alone as evidence the theory invites a U(1).]
- `C5d_K4_parity_crease_2torsion_datum`: both K₄ characters circle-legal (θ ↦ −θ
  well-defined mod 2π); χ_θ DECLARED; ε_θ SUPPLIED never valued. **New exact fact
  (conditional on supplied ε_θ = −1): the crease value is 2-torsion quantized —
  θ(crease) ∈ {0, π}** — the arc's first discrete TARGET-side datum, derived not imposed.
- `C5e_J05_pairing_pointwise_row_plus_wall_slots`: the J05 identity zero-residual on
  12-free-coefficient witnesses: δθ pairs as a pointwise density row + wall θ-jet slots
  (N3-analog, V8 supplied-structure). Coupling slots DEFINED — registered, not adopted.
- `C5f_FD5_lattice_vs_point_kernel`: e^t = 1 over ℝ: {0}; e^{it} = 1 ⟺ t ∈ 2πℤ (lattice;
  cos-route solveset + the period gate's direct certificates): **F-D5 does NOT fire — the
  holonomy-target situation genuinely changes.**

**C5 verdict: REGISTERS (Route-D-analog grade: coherence / cocycle / alphabet / parity /
slots), REGISTERED-POSIT tag.** [O2 note (verifier), the grade comparison: Route D's grade
also carried an orbits/quotient leg; for θ the ONLY banked actions are K₄/parity, analyzed
in C5d — the leg is vacuous-or-absorbed into C5d, and the frozen contract defined the
five-requirement list pre-derivation, so nothing was waived; if a future coupling ties θ
to screen data, the dressing/orbit question re-opens with it.] Honest conditional slots: ε_θ SUPPLIED; χ_θ DECLARED;
U(1) cocycle factor ADJOINED (admitted by the banked law, not owned); the target circle
MAY be identified with C1's owned fiber circle (period 4π ↔ rescaling) — that
identification is itself a further typed posit, not made here.

## Stage 4 — TD-3 (the integer content of the registered θ; period-gate machinery re-run)

- `TD3a`: quotient posture — winding = hom D∞ → ℤ; 2h = 0 over ℤ ⇒ h ≡ 0 (exact): **the
  banked Hom(D∞,ℝ) = 0 theorem survives the circle target on the winding side.** The
  quotient posture's integer content is TARGET-side instead: the crease ℤ₂ datum (C5d).
- `TD3b_cyclic_winding_condition_live`: the CYCLIC completion cycle — single-valuedness of
  e^{iθ} = the winding condition **Σᵢ cᵢLᵢ + Σₛ Jₛ = 2πn_w, n_w ∈ ℤ — THE FIRST LIVE
  INTEGER CONDITION on the banked cycle census** (N = 1 solved exactly; general N =
  telescoping, the period gate's form with dθ for dπ_p). Exact structure change: real
  targets gave ONE hyperplane; the circle target gives a ℤ-INDEXED family of parallel
  hyperplanes — ℤ-labeled sheets in configuration space.
- `TD3b_telescoping_N2_rederivation_credited` (CREDITED ADOPTION, verifier G9, finishing
  pass): the N = 2 telescoping re-derivation — per-cell lifts θ = cᵢx + bᵢ with seam jumps
  Jₛ telescope to increment = c₁L₁ + c₂L₂ + J₁ + J₂ exactly; the 2π enters ONLY through
  e^{iΔ} = 1 on the registered target (genuine, not inserted); real-target contrast = the
  single hyperplane (banked form); slopes absorb ANY (L, n) pair — the
  no-unconditional-cut scoping is REAL freedom, not an artifact.
- `TD3b_parameter_cut_adjudication` (honest, both directions): at FIXED slope c ≠ 0 the
  length is lattice-cut (L ∈ 2πℤ witness, exact) — CONDITIONAL; slopes are FREE data, so
  **no banked parameter (E0, ℓ, moduli) is unconditionally quantized**; the J05 slots are
  exactly where an ADOPTED coupling would tie cᵢ to E0ᵢ — registered, not adopted; no
  spectrum claimed (ceiling honored).
- `TD3c_torsion_classes_revive_over_U1`: the banked torsion-vacuity proofs are
  TARGET-DEPENDENT: over ℝ, 2P = 0 ⇒ P = 0 (reproduced); over U(1), hol² = 1 has {+1, −1}
  (exact): **the K₄-orbifold order-2 classes revive as LIVE ℤ₂-valued holonomy data**; cap
  classes stay empty (π₁ trivial). The revival is exactly the 2-torsion sector.
- `TD3d` [guard]: J11 loops — the adjoined factor's triviality locus is the 2πℤ lattice vs
  the banked codim-1 real hyperplane: the loop classification gains a discrete winding
  component (conditional on a loop-possessing completion; F-S7 travels).

## Stage 4 — TD-4 (the C6 carrier comparison; one-way characterization, F-D4)

- `TD4a`: **DERIVES: NO** — π₂(S¹) = 0 (lift + straight-line null-homotopy, endpoints
  exact; Category-A named): θ cannot carry the carrier's π₂(S²) content; no S²-valued
  field is derived by anything here.
- `TD4b`: **POSSESSES: PARTIAL-AS-STAGE** — σ₁² + σ₂² = dθ² + sin²θ dφ² exactly,
  ψ-independent ⇒ basic ⇒ the arena natively possesses a round S² as the Hopf BASE (and
  the fiber circle, C1) — DOMAIN/stage structure, never a field target; the bedrock
  stage-not-actors line holds.
- `TD4c`: **EMULATES: PARTIAL** — the equatorial restriction n = (cosθ, sinθ, 0), |n| = 1
  exact, IS an S¹-valued field: θ carries exactly the carrier's U(1)/phase sector (the
  circle its equatorial windings wrap); the π₂ (polar) sector is not emulated.
- `TD4_three_layer_verdict` [guard]: **carrier posit PARTIALLY FOUNDED at the circle/phase
  layer, UNTOUCHED at the π₂(S²)/π₃(S³) layers.** Identifying θ's target with the owned
  fiber circle is a further typed posit, not made.

## Outcome and falsifier record (derivation-side)

**Outcome class: OD-4 (mixed).** No owned structure promotes to a FIELD — C1 Chern-obstructed
(−4π ≠ 0) yet DELIVERS the owned target circle + owned circle-valued transition law; C2
killed by exactly the banked cap/torsion obstruction; C3 the owned SO(2) was SPENT as chart
gauge (its 2-torsion {±1} = the banked K₄ characters = the real points of U(1)); C4
non-compact confirmed at group level. The NEW field REGISTERS at Route-D-analog grade
(OD-2 component, REGISTERED-POSIT tag, honest supplied/declared/adjoined slots), with
OD-1 flavor only at the TARGET level (owned circle + owned transition datum usable as its
ingredients). Script: **35 checks = 31 SUBSTANTIVE + 4 GUARD** (finishing pass: +2
CREDITED verifier-route adoptions — the second Chern route and the N=2 telescoping;
was 33 = 29+4 at verification), 0 failures, exit 0, byte-identical rerun ×2 post-finishing
(stdout AND JSON; sha256 `DERIVATION_STDOUT.txt` 074a3bae…, `doorway_results.json`
8d1a9248…).

- **F-D1:** verdicts landed in MULTIPLE directions (4 failures + 1 registration + a
  conditional-only integer content); the success/integer legs carry their conditions
  explicitly; silence (no unconditional quantization) stated with the same care.
- **F-D2:** every compact entry's legality DERIVED (periodicity rule; co-translation
  witness; cocycle adjunction computed; crease solveset); no requirement waived — the
  supplied/declared slots are named as such, not silently passed.
- **F-D3:** stamps carried (standing block + per-check details).
- **F-D4:** not fired — TD-4 is one-way; no hopfion-lane result transferred; the
  object-identity fault line respected (π₂ carrier vs π₃ hopfion never conflated).
- **F-D5:** adjudicated and PASSED for C5 (lattice vs point kernel, exact); C3's would-be
  promotion is the named F-D5 counter-example (no target change) — recorded as its failure.
- **F-D6:** no bank contradiction — banked facts reproduced (cap dets 104/104, dressing
  ODE, E08 law, two-sided law, real-target point kernels, torsion vacuity over ℝ).
- **F-D7:** no symbolic failure; exit 0.

**Limits that travel:** (i) C5's registration is at Route-D-analog GRADE (class/cocycle/
alphabet/parity/slots typing) — the exhaustive θ-response parametrization (Stage-2-analog)
and any dynamics/coupling derivation are NAMED unrun seats; (ii) ε_θ SUPPLIED, χ_θ
DECLARED, the U(1) cocycle factor ADJOINED — the REGISTERED-POSIT tag travels with every
downstream use; (iii) TD-3's conditions are off-shell winding conditions on free data —
no on-shell selection; (iv) the arena-topology legs ride the banked cap census and the
Euler-chart Hopf presentation; exotic non-Hopf-preserving families remain the banked open
boundary; (v) Category-A named steps: winding homotopy invariance (C2a), covering lifting
(TD4a), Picard uniqueness (C3a/C3c); (vi) verifier observations O1–O4 implemented as
in-place notes at their sites (C5c, the grade comparison, C3b, C2a) — see
`CORRECTION_LAYER.md`; no math changed.
