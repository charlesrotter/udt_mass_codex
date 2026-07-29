# P4 Route A Stage 2 → Stage 3 HANDOFF (TB6) — what the WS/GC gates must decide ON ℛ_PW

Date: 2026-07-29. Contract: `PREREGISTRATION.md`. **This is a HANDLE, not a launch:**
no gate is run here, no candidate declared, no member of ℛ_PW selected (F-B1). ℛ_PW =
the exact pointwise parametrization of `EXACT_DERIVATION.md` §4 +
`RESIDUAL_SPACE_LEDGER.tsv`, **CUT BY the A1 stratum Noether identities on the
degeneration strata** (OB1: nonempty; scope stamps travel). **A1-AMENDED
2026-07-29:** the gate-1/gate-4 notes below are corrected — the R7(b) input to Stage
3 is "generically vacuous + explicit stratum identities on the degeneration strata",
NOT unqualified vacuity (see `CORRECTION_LAYER.md`). **ROUND-2 AMENDED 2026-07-29
(closure item C3):** the stratum content below is further corrected — k_mod = 0 is
the only CODIMENSION-1 cut; the resonance locus carries C ≠ 0 sub-varieties of
higher codimension with additional exact identities (derived example: the shear
identity −c10·r_sh − k10·m10 = 0 on {λ−k_mod = −1, c00 = c01 = 0}); the four NAMED
C = 0 strata identities are auto-satisfied in the declared class; the deeper
stratification is TYPED-NOT-EXHAUSTED.

## 1. The surface in five lines

1. ℛ_PW is a parametrized family: per-component character-matched functions of a
   graded alphabet (dims 10/13/16; module bases 1/5/4/4), cut by the A1 stratum
   Noether identities on the degeneration strata — Stage 3 gates act ON this family,
   never on the raw requirement list again.
2. Open per family: the J06 determined-vs-retained branch for each of λ, k_mod, k10,
   C (both branches open sub-loci; k_mod-determined requires the r_tf slot ≠ 0; on
   the k_mod = 0 stratum r_tf is tied to the mixing kernel by the A1 identity; on
   the found C ≠ 0 resonance sub-variety r_sh is tied to R_c10 by the R2 shear
   identity — deeper sub-variety ties typed-not-exhausted).
3. WS requirements to impose: R5 (same-solution closure relation), R14 (bootstrap
   stays admissibility), R7-currents; GC: R3, R6, R9, R15; J07–J09, J11,
   J13-completion, J15 reporting.
4. Every gate needs a CANDIDATE DECLARATION (D1–D5 of `SIX_GATE_SPECS.md`) — in
   ℛ_PW terms: a point/subfamily of the parametrization + declared pairing P1/P2/P3
   + boundary/completion stances.
5. Completion/boundary data required per family are TYPED (J07 twisted-cocycle type,
   J08 descent data, mirror-parity wall data) — cited below, NOT filled.

## 2. Open J06 branches per moduli family (Stage 3 decides; Stage 2 carried both)

| Family | Determined branch | Retained branch | What Stage 3 must decide |
|---|---|---|---|
| λ | r_tr ≢ 0 | r_tr ≡ 0, λ residual | whether a candidate's zero set actually fixes λ on a solution (WS — gate 1/2 record the branch, R5/J06-WS decide determination) |
| k_mod | r_tf ≢ 0 (slot forced present for this branch — banked F-RA2) | r_tf ≡ 0, k_mod residual | same, on the trace-free slot; trace/volume-channel sectors are confined to the retained branch |
| k10 | r_sh ≢ 0, χ_a-matched | r_sh ≡ 0 | same; character rule already built into ℛ_PW |
| C | mixing kernel M ≢ 0, χ_b/χ_c-matched | M ≡ 0 | same; plus J07 transition data whenever M ≢ 0 travels across charts |

## 3. Which gate-spec tests bind which parameters of ℛ_PW

(Gate specs banked in `../udt_p4_routeA_response_inverse_problem_2026-07-29/SIX_GATE_SPECS.md`; cited, not run.)

| Gate | Binds on ℛ_PW |
|---|---|
| 1 same-solution closure (WS) | the full component tuple + the J06 branch record: system {R_i = 0} compatibility vs the three typed failure modes; NOTE (A1-CORRECTED) — gate 4's identity input is the amended R7(b) content: GENERICALLY no continuous chart-gauge identities (per-member stabilizer trivial at generic moduli), but on the degeneration strata explicit stratum identities EXIST (k_mod = 0 — the only CODIM-1 cut: −2k10·r_tf + ⟨M, J·C⟩ = 0; the four named C = 0 resonance strata: auto-satisfied in the declared class; the C ≠ 0 resonance sub-varieties: FURTHER genuine cuts — derived example −c10·r_sh − k10·m10 = 0 on {λ−k_mod = −1, c00 = c01 = 0}; deeper stratification TYPED-NOT-EXHAUSTED) — gate 1 must NOT assume "no continuous chart-gauge identities" on the strata; it must CARRY the strata (including the not-yet-enumerated deeper sub-varieties: per-candidate stratum contact requires the per-branch identity computation, method recorded). The no-Bianchi-TYPE-assumption warning STANDS (the stratum identities are algebraic pointwise identities, not Bianchi-type differential identities): overdetermination must still be resolved by explicit integrability, never by assumed differential identities |
| 2 sector selection | the slot coefficients (r_tr, r_tf, r_sh, M): per-modulus branch recording; character rule is pre-satisfied by construction of ℛ_PW; on k_mod = 0 the A1 identity ties r_tf to M; on the found C ≠ 0 resonance sub-variety the R2 shear identity ties r_sh to m10 (candidates touching any derived stratum must respect its identity; deeper sub-varieties typed-not-exhausted — per-candidate contact needs the per-branch computation) |
| 3 Helmholtz | the jet structure of all components RELATIVE to the declared pairing (P1/P2/P3 — the pairing declaration is load-bearing supplied structure; Route B T4 volume-blindness loci); outcome = LOCALLY-EXACT vs NONVARIATIONAL classification of the L6 fork per candidate |
| 4 gauge/Noether | pointwise part discharged in ℛ_PW **INCLUDING the A1 stratum identities** (equivariance + character matching built in, `PW2_*`, `PW3_*`; generic vacuity + the k_mod = 0 identity + the named C = 0 resonance strata + the C ≠ 0 sub-variety cuts (derived example; deeper layers typed-not-exhausted), `A1_*`/`A1R2_*` — the gate must CARRY the strata, not assume vacuity, and must not assume the derived examples exhaust the deeper resonance content); remaining: the WS current-conservation leg and the J10 family-vs-selection guard |
| 5 boundary differentiability (GC) | R_wall/R_corner vs the bulk grade: wall jet-depth pairing per declared N (depth example-typed only — Route C TC5; Stage 3 must derive the actual depth per candidate), mirrored parity + sector split, BR-B fork stance |
| 6 periods (GC) | completion fork (BR-C), J07/J11 cocycle holonomy, non-torsion cycles (K₄-torsion cycles vacuous for closed forms — banked scope note) |

## 4. Completion/boundary data each family requires (TYPES cited, NOT filled)

- **Mixing families (M ≢ 0 or r_sh ≢ 0 across charts):** J07 transition data of the
  banked two-sided twisted 1-cocycle TYPE L(γ₂∘γ₁) = Q(γ₂)L(γ₁) + L(γ₂)ρ(γ₁),
  Q = e^{φK}, ρ = e^{φH} (Route B T3), with J11 loop holonomy trivial-or-classified.
- **All families:** J08 descent data = the completion label 𝔠 (12 FC families;
  fork BR-C) entering only as the explicit R3 argument; J09 null/type-changing
  stratum declaration.
- **Boundary components:** mirrored-parity wall data (CANON C-2026-06-10-2 /
  C-2026-07-04-1); anchored-φ wall dependence only through supplied-structure slots
  (Stage-1 V8 clash resolution); depth per candidate jet order (to be derived, not
  the TC5 examples).
- **Anchor:** c_E calibration (G06) — the only φ-zero-point carrier; BR-CE promotion
  remains typed-only/unregistered.

## 5. What Stage 3 may NOT inherit as decided

Nothing in ℛ_PW's nonemptiness says any member closes on a solution (R5), is
differentiable on the finite cell (R6), has controlled periods (R9), respects
R14/R15, or exists globally (J07/J11): the FULL ℛ = ℛ_PW ∩ {WS/GC requirements}
could still be empty, a point, or a family — all three remain first-class (J15).
Known-object locations (EH inside jet ≤ 2; Bach in the typed jet-3/4 class; ω-shape
inside off the C ≠ 0 resonance sub-varieties — R2 per-witness stratum stamps) are
OBSERVATIONS carrying no precedence. Physics adjudication stays with
Charles.
