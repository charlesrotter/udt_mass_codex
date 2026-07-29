# P4 Route A Stage 3 (Slice 1) — exact derivation record: the candidate-free gate cuts on ℛ_PW (TC1–TC5)

Date: 2026-07-29. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
derivation). Script: `derive_routeA_stage3.py` — **52/52 checks, exit 0 = 33 SUBSTANTIVE
zero-residual exact-SymPy checks + 19 CITATION GUARDS** (guards = typing-table/citation/
bookkeeping rows, labeled `[guard]` in-script and in the JSON, never counted as residual
computations; A4 amendment: three guard-grade checks reclassified substantive → guard —
`TC4_torsion_period_vacuous`, `TC1_no_empty_adjudicated_cell`,
`TC2_kmod0_identity_is_row_dependency`), deterministic (no floats/randomness/network; JSON,
ledger, and stdout byte-identical across reruns — verified), single CPU process, ~61 s
(FULL DECLARED SCOPE — no scope reduction taken; the jet-3/4 typing is retained as the
order-4 anchor). Outputs: `routeA_stage3_results.json`, `DERIVATION_STDOUT.txt`,
`GATE_CUT_LEDGER.tsv`, `SLICE2_SURFACE.md` (TC6). Every check named in `monospace` below is
one of the 52.

**AMENDED (A1/A3/A4, 2026-07-29, per `VERIFIER_REPORT.md`; record = `CORRECTION_LAYER.md`):**
the §1.2.6 anchored-log forcing claim was REFUTED AS PHRASED by the verifier's in-family
counterexample (V10b) — an F-S3-class quantifier slip — and is restated below with its exact
iff condition, banked as three new zero-residual `A1_*` checks. The computations behind the
original statement were correct; the corrected statement is strictly narrower. Nothing else
changed: the partition, witnesses, transversality, boundary census, typing tables, ledger
map, and outcome class are untouched.

**Slice-1 boundary (binding, carried on every statement):** candidate-free gate cuts ONLY.
NO member of ℛ_PW selected/privileged/ranked (F-S1); NO solution of 𝓡 = 0 computed and no
solution-dependent conclusion drawn (F-S6); NO completion class chosen, NO boundary-data
choice, NO pairing adopted (F-S2 — every G3 statement carries its pairing-branch label, or a
PROOF of branch-independence); every only/all/none/exhaustive/vacuous/empty claim carries its
stratum + scope stamp (F-S3 — the named recurring error class, policed first).

**Standing scope stamps (travel with every statement):** jet ≤ 2 exhaustive layer on the
registered stationary one-parameter presentation (fields (φ, f, bh), jets p/f/h 0..2; the
banked Stage-2 EXHAUSTED scope), registered positive triangular chart, BASE branch (moduli
constant; BR-A carries the same theorems at jet ≤ 2; BR-M/BR-CE typed NOT-EXHAUSTED),
polynomial/formal in the (k10, C) moduli, off-shell, one-parameter. Components depend on p0
only through the anchored Q = c_E e^{−p0} at supplied c_E; using p0 as the grade-0 argument
at fixed supplied c_E is an exact relabeling (`J0_anchored_relabeling`: log(c_E/Q) = p0 —
the anchored depth is alphabet-legal; J04 provenance carried, not altered). The coordinate
measure dx on the registered chart is Category-A conditioning. Banked inputs are RECOMPUTED
as consistency and cited, never re-derived as new (`S0_*`).

**Resonance rule (inherited, binding):** every adjudication specific to sub-families
contacting the resonance locus (λ∓k_mod ∈ {±1}) beyond the banked k_mod = 0 codim-1
identity is DEFERRED — the RES-CNEQ0 rows of the ledger are stamped CENSUS-REQUIRED; the
banked shear-identity example is CITED only.

---

## 0. Premises (chose or derived — stamped)

| Premise | Tag |
|---|---|
| Registered chart + Route B conventions; K₄; E02 footing | THEORY (banked; recomputed `S0_K4_and_X_recomputed`) |
| ℛ_PW stratified parametrization + k_mod = 0 identity + shear example | DERIVED input (Stage-2 bank 2c0e7cc; recomputed `S0_generic_pointwise_stabilizer_trivial`, `S0_kmod0_identity_recomputed`) |
| Gate specs (amended); P1/P2/P3 pairing enumeration §1.5 | DERIVED input (Stage-1 bank; NONE adopted — F-S2) |
| Pairing-relative Helmholtz / jet-slot bookkeeping / integrability typing / twisted-cocycle machines | METHOD (recon shortlist, lane clause Category-A; twisted-H¹ row MODEL-KNOWLEDGE — F-S7 flag) |
| Route C TC5 boundary instances | DERIVED input, cited as the anchor (reproduced as special cases) |
| Anchored-weight representation of the bulk pairings (w = e^{a(m)p0} per slot) | DERIVED-from-enumeration: P2 = a ≡ 0; P1 instances = the T4-enumerated volume exponents (2λ; 1+2λ) with per-slot moduli weights SUPPLIED (tagged open structure); P3 = declared bulk + wall/corner densities |
| Field parities at the mirror wall | SUPPLIED wall structure (canon instance ε_φ = −1 spatial mirror, THEORY-cite C-2026-06-10-2 / C-2026-07-04-1; f, bh parities tagged SUPPLIED, not derived) |
| Jet order ≤ 2 for exhaustive layer; order-4 anchor 2-field instance | Category-A bounded scope (stamps travel) |
| SymPy exact, CPU, single process | Category-A conditioning |

## 1. TC1 — the Helmholtz partition (gate 3), pairing-relative, per stratum

### 1.1 The condition system (derived, not imported)

For a member with field components R_a(p0, f0, h0, p1, f1, h1, p2, f2, h2; m) and moduli
components R_μ (same arguments), under a bulk pairing with per-slot anchored weights
W_F = e^{a_F(m)p0}, W_M = e^{a_M(m)p0}, write Δ_a = W_F R_a. The member is LOCALLY-EXACT
under the declared pairing iff (necessity DERIVED; sufficiency = the banked bicomplex/
Vainberg statement, Category-A cited, witness-instantiated):

- **(i) field–field, top order:** ∂Δ_a/∂u_b″ = ∂Δ_b/∂u_a″ — equivalently
  ∂R_a/∂u_b″ = ∂R_b/∂u_a″ (the weight cancels).
- **(ii) field–field, first order:** ∂Δ_a/∂u_b′ + ∂Δ_b/∂u_a′ = 2 D_x(∂Δ_b/∂u_a″) —
  equivalently on R: ∂R_a/∂u_b′ + ∂R_b/∂u_a′ = 2 D_x(∂R_b/∂u_a″) + **2 a_F p1 ∂R_b/∂u_a″**.
- **(iii) field–field, zeroth order:** ∂Δ_a/∂u_b − ∂Δ_b/∂u_a + D_x(∂Δ_b/∂u_a′)
  − D_x²(∂Δ_b/∂u_a″) = 0 — the R-form shift (a_F-terms incl. the asymmetric p0-column
  contributions) is recorded exactly in the JSON (`condition_iii_shift_sample_pf`).
- **(H4) field–moduli:** ∂(W_F R_a)/∂m_μ = E_a(W_M R_μ) (the μ-row adjoint IS the Euler
  operator — by-parts certificate `TC1_H4_byparts_identity`; the boundary residue Ξ routes
  to the gate-5 wall census under P3).
- **(H5) moduli–moduli:** the antisymmetrized ∂(W_M R_μ)/∂m_ν lies in im(D_x)
  (Euler-certificate criterion; for field-independent moduli sectors this is closedness of
  the moduli one-form).

Proofs, all zero-residual: the condition families are EXACTLY Fréchet self-adjointness
(adjoint-comparison on the GENERAL component triple — `TC1_conditions_are_selfadjointness`);
Δ = E(L) for the generic order-1 Lagrangian satisfies (i)–(iii) identically
(`TC1_helmholtz_necessity_generic_L`); the generated family R_a = W_F^{-1}E_a(W_F L̃),
R_μ = W_M^{-1}∂_μ(W_F L̃) satisfies H4 and H5 identically for the generic L̃
(`TC1_H4_generated_witness`, `TC1_H5_generated_witness`). Weight-shift forms:
`TC1_weight_top_condition_invariant`, `TC1_weight_shift_condition_ii`,
`TC1_weight_shift_condition_iii_vanishes_at_aF0`.

### 1.2 The pairing-dependence map (a deliverable)

1. **Condition (i) is pairing-INDEPENDENT across the anchored family** — scope stamp: the
   enumerated anchored bulk family (P1 instances / P2 / P3-bulk) at jet ≤ 2 on the
   registered stationary presentation; NOT arbitrary unenumerated pairings.
2. Conditions (ii)/(iii)/H4/H5 shift by the exact a_F/a_M terms above; a_F = a_M = 0
   recovers P2.
3. **The partitions are isomorphic-but-distinct cuts:** multiplication by e^{−a_F p0} is a
   K₄-inert, parametrization-preserving bijection of ℛ_PW intertwining the P1-instance and
   P2 partitions (`TC1_weight_map_K4_inert_and_invertible`, guard
   `TC1_weight_map_preserves_characters`). Cell membership of a FIXED component tuple is
   pairing-RELATIVE — computed witnesses:
   - W1 = (p2, f2, h2): LOCALLY-EXACT under P2, NONVARIATIONAL under P1-4D with defect
     −4λ p1 e^{2λp0} — nonzero exactly off the T4 blindness locus λ = 0
     (`TC1_W1_LE_P2_NV_P1_4D`).
   - W2′ = field sector e^{−2λp0}E(e^{2λp0}L̃₀) PLUS the generated λ-slot 2p0·L̃₀: the full
     tuple is LOCALLY-EXACT under P1-4D (field–field conditions checked directly; H4/H5 by
     the generated-family checks — the field-only tuple with zero moduli slots FAILS H4(λ),
     which is exactly the anchored-log forcing of §1.2.6 — its ∂λ(W_F R_a) ≢ 0, the A1 iff
     condition); the SAME field sector under P2 is
     NONVARIATIONAL (`TC1_W2_LE_P1_NV_P2`; scope: off λ = 0).
   - W3 = (p1, 0, 0): NONVARIATIONAL with **PROVEN branch-independence** across the entire
     enumerated anchored family (Hi1 = 2e^{a_F p0} ≠ 0 — `TC1_W3_allbranch_NV`; F-S2
     discharged by proof for this adjudication).
   - ω-shape (R_k10 = k10): LOCALLY-EXACT under P2/P3-bulkP2 and under P1 instances with
     λ-INDEPENDENT moduli-slot weight; NONVARIATIONAL under P1 instances with a_M = 2λ
     (`TC1_omega_moduli_LE_P2_NV_P1_lamdep` — observation, per-instance stamps; stratum
     stamps banked and cited).
4. **T4 blindness consistency (recomputed):** P1-4D ≡ P2 at λ = 0; P1-triad ≡ P2 at
   λ = −1/2 (`TC1_T4_blindness_consistency`) — the pairing-dependence degenerates exactly
   on the banked Route B T4 blindness loci.
5. **P3 inherits its bulk partition:** a bulk self-adjointness defect is detected by
   interior-supported variations, which kill every wall/corner term — computed nonzero
   interior defect certificate for the NV member W3 with variations vanishing to second
   order at both walls (`TC1_P3_interior_defect_wall_immune`). The wall-density block adds
   its OWN symmetry conditions (typed; per declared N — Slice 2).
6. **The anchored-log structure (computed observation, NOT an obstruction) — A1-AMENDED
   (verifier):** under the two ENUMERATED λ-dependent P1 volume instances (both have
   da_F/dλ = 2 — `TC1_both_volumes_same_dlambda`), the mixed (field, λ) condition carries
   the additive anchored-depth term a_F′(λ) p0 W_F R_a (`TC1_H4_lambda_anchored_log_term`).
   **The corrected statement (verifier-derived, adopted exactly): the LE cell's λ-slot is
   forced nonzero — and carries the log(c_E/Q) dependence via the a_F′·p0 term — IFF
   ∂λ(W_F·R_a) ≢ 0 for some field slot a; in particular for every λ-INDEPENDENT nonzero
   field sector.** NOT "whenever the field sector is nonzero": the in-family counterexample
   (verifier V10b, banked zero-residual as `A1_V10b_counterexample_LE_zero_lambda_slot`) is
   R_a = e^{−2λp0}(p2, f2, h2) — generated by the anchored formal-in-λ L̃ = e^{−2λp0}L̃₀
   inside the banked alphabet class — with ALL moduli slots zero, fully LOCALLY-EXACT under
   P1-4D, zero λ-slot, no log anywhere. The exact iff condition is banked on a generic
   member (`A1_anchored_log_iff_condition`: with a zero λ-slot the H4(λ) residual is exactly
   ∂λ(W_F R_a) = W_F[∂λR_a + a_F′ p0 R_a], both directions instantiated); on the
   λ-independent sub-case the forcing IS real and the generated witness has R_λ = 2p0 L̃₀
   exactly (`A1_lambda_independent_sector_forcing_real`,
   `TC1_H4_witness_lambda_slot_contains_log`). The log is alphabet-legal at supplied c_E
   (`J0_anchored_relabeling`), so this is forced STRUCTURE inside the LE cell, not an
   emptiness. *Bare-φ reconciliation (A3): the log(c_E/Q) = a·p0-type dependence is ANCHORED
   (supplied-c_E) exactly as Stage-2's (c_E/Q)^a alphabet entries are — no bare-φ
   readmission; the Stage-2 anchoring rule (anchored-exponent condition, supplied-c_E
   reading) is the same rule under which Stage-2's "bare φ excluded" headline stands.* Scope
   stamp: the two enumerated λ-dependent P1 instances, jet ≤ 2, stationary presentation,
   BASE branch.

### 1.3 The stratum layer

The condition families are stratum-uniform jet-level identities; the k_mod = 0 stratum
enters through the FAMILY cut (the banked identity). On KMOD0 under P2 (moduli sector,
jet-blind) all four corners of (G3-cell × identity-cut) are populated
(`TC1_kmod0_fourcorner_transversality`):

| | identity-satisfying | identity-violating |
|---|---|---|
| LOCALLY-EXACT | ω-shape (R_k10 = k10) | R_kmod = 2 (violates at k10 ≠ 0 — the banked off-stratum-scoped witness, cited) |
| NONVARIATIONAL | R_λ = k_mod | R_λ = k_mod plus R_kmod = 2 |

**The Helmholtz cut and the stratum Noether cut are TRANSVERSE at witness level** — scope
stamp: witness-level transversality on KMOD0 under P2 at jet ≤ 2, NOT a full-cell census.
RES-CNEQ0: CENSUS-REQUIRED (resonance rule); the banked facts (ω violates the shear
identity; the corrected trace-free witness and field-sector members survive) are cited, not
re-adjudicated.

### 1.4 Cell emptiness (OS2 watch)

**No adjudicated cell is empty** (`TC1_no_empty_adjudicated_cell`) — scope stamp:
witness-level nonemptiness at jet ≤ 2, BASE branch, enumerated pairing branches, GENERIC
and KMOD0 strata; the 10 RES-CNEQ0 composite cells are CENSUS-REQUIRED, not adjudicated.
OS2 is not triggered; neither is OS3 (no rigid collapse — the cells remain
functional-dimension-sized families, cf. the Stage-2 parametrization).

## 2. TC2 — the integrability typing (gate 1), per cell and stratum

- **GENERIC stratum: DETERMINED-TYPE.** 3 field equations + 7 moduli relations vs 3 field
  unknowns + 7 moduli; NO pointwise Noether identity (per-member stabilizer trivial —
  recomputed `S0_generic_pointwise_stabilizer_trivial`); NO Bianchi-type differential
  identity assumed (banked input carried). Gate 1's on-shell leg here = explicit
  integrability of the joint system on ONE solution (the R5 closure) — Slice 2. No
  existence claim (F-S6). (`TC2_counts_determined_type` [guard].)
- **KMOD0 stratum: CONSTRAINED-TYPE (balanced).** The banked identity is exactly ONE linear
  row dependency among the moduli equations, −k10·R_kmod + c10·R_c00 + c11·R_c01 −
  c00·R_c10 − c01·R_c11 = 0, matched by exactly ONE tangent gauge direction (L23; nullspace
  dim 1) — identity count = gauge dimension = 1 (`TC2_kmod0_identity_is_row_dependency`).
  The identity is a POINTWISE ALGEBRAIC relation, NOT a Bianchi-type differential identity
  (handoff warning carried): gate 1 must still resolve overdetermination by explicit
  integrability AND carry the L23-orbit quotient.
- **LE-cell extra (both strata):** the principal symbol is SYMMETRIC (condition (i)),
  pairing-independently across the anchored family (`TC2_LE_symbol_symmetry_restatement`
  [guard]); the NV cell carries no symbol-symmetry constraint. Per-candidate symbol
  nondegeneracy is Slice-2 business.
- **RES-CNEQ0: CENSUS-REQUIRED** (`TC2_resonance_census_required` [guard]).

## 3. TC3 — the boundary census (gate 5), per jet order, on the mirrored cell

Derived on the one-parameter mirrored model (generic Lagrangians, all fields symbolic);
the Route C TC5 instances are REPRODUCED as special cases (the recon TG3#2 soundness duty —
`TC3_routeC_TC5_anchor_reproduced` [guard]). Counterterms are NOT available (Category-B,
banked): differentiability must live inside the candidate.

- **N = 2 (exhaustive layer):** δ∫L = ∫ΣE_a(L)v_a + [Θ₂], Θ₂ = Σ ∂L/∂u_a′·v_a
  (`TC3_byparts_N2_identity`): wall slots = the 0-jet traces {v_a}; momenta = functions of
  1-jet traces → available at wall grade ≤ 2 (Stage-2 wall-alphabet rule, trace jets ≤
  grade−1, cited): **LE-cell 2nd-order sub-families CAN self-pair every parity-surviving
  slot from their own R_wall** (`TC3_wall_grade_availability_jet2` [guard]).
- **N = 4 (typed):** Θ₄ pairs BOTH {v_a, v_a′} (`TC3_byparts_N4_identity`) and the
  v_a-momentum ∂L/∂u′ − D_x(∂L/∂u″) CONTAINS THIRD JETS
  (`TC3_N4_momentum_contains_3rd_jet`): wall grade 4 needed → **4th-order sub-families are
  STRUCTURALLY UNABLE to self-pair within the jet ≤ 2 layer** — the typed jet-3/4 extension
  is required (NOT-EXHAUSTED stamp travels; the Bach-side class lives here). N = 3: typed
  by the same enumeration, not run (stamp).
- **Mirror parity (the parity-halving):** at a mirror wall a field of parity ε has
  u^{(j)}(wall) = 0 exactly for (−1)^j ε = −1 (`TC3_parity_jet_kill`): N = 2 slot {v_a}
  survives iff ε = +1 (odd fields self-pair by parity — zero slots); N = 4: {v_a} iff
  ε = +1, {v_a′} iff ε = −1 — exactly half per field either way
  (`TC3_slot_survival_table` [guard]). Parity assignments are SUPPLIED wall structure; the
  canon instance ε_φ = −1 (spatial mirror, static sector) is THEORY-cited, f/bh parities
  tagged SUPPLIED (`TC3_mirror_canon_parity_instance` [guard]).
- **Anchored-φ wall rule (recomputed):** wall coefficients c_E^p e^{−qφ_w} are orbit-
  invariant iff p = q — a Q_wall-power (`TC3_anchored_wall_rule`; Stage-1 V8 cited).
- **NV cell: NO-BULK-FORCED-SLOTS** — the source-form pairing needs no by-parts, so the
  bulk forces zero unpaired wall jets; gate 5's live content for NV members = parity/
  sector-split + anchored-φ admissibility of their OWN R_wall/R_corner + (varied fork)
  wall-equation closure — Slice 2 (`TC3_NV_cell_no_forced_slots` [guard]; scope: slot
  OBLIGATIONS only, no differentiability verdict on any member).
- **Corners: TYPED-ONLY** (codim-2, absent from the one-parameter presentation; Route C
  TC5 corner examples cited; general-arena corner census = a Slice-2 cost item)
  (`TC3_corner_census_typed_only` [guard]).

## 4. TC4 — the period typing (gate 6), per cell; type-level only

- **K₄-orbifold cycles, LE cell: VANISHING-BY-TORSION.** Every K₄ element squares to the
  identity (`TC4_K4_all_torsion`); for closed one-forms 2P = P(γ²) = 0 forces P = 0
  (`TC4_torsion_period_vacuous`). Scope stamp (banked, carried): vacuous FOR CLOSED FORMS
  on the K₄-torsion cycles ONLY — non-torsion cycles remain live.
- **Completion-class cycles (both cells): NEEDS-COMPLETION-DATA** — the L4 fork stays open
  (Slice-1 boundary); BR-C pointwise branch-independence (banked) makes the obligation TYPE
  branch-uniform (`TC4_completion_cycles_need_data` [guard]).
- **J07/J11 cocycle loops:** mixing sub-families (M ≢ 0 or r_sh ≢ 0 across charts) carry
  CLASSIFICATION-REQUIRED obligations of the banked two-sided twisted-cocycle TYPE; the
  classification MACHINERY (twisted-H¹ analog) is MODEL-KNOWLEDGE — **F-S7 flag carried on
  every such row; no banked G6 claim rests on it** (`TC4_FS7_flag_carried` [guard]).
  Non-mixing single-chart sub-families: NO-TRANSITION-DATA-OBLIGATION (handoff §4 typing,
  cited).
- **NV cell:** gate-6 step 3 — holonomy of the closure data CLASSIFICATION-REQUIRED
  [F-S7] + NEEDS-COMPLETION-DATA; the torsion vacuity does NOT auto-transfer (closed-form
  scope) (`TC4_typing_table_assembled` [guard]).

## 5. TC5 — the joint gate-cut map (THE deliverable)

`GATE_CUT_LEDGER.tsv`: **30 composite rows = 5 pairing branches (P1-4D, P1-triad, P2,
P3-bulkP2, P3-bulkP1) × 3 strata (GENERIC, KMOD0, RES-CNEQ0) × 2 G3-cells** + 4
known-object OBSERVATION rows. Per row: the G3 condition set, G1 type, G5 status, G6 type,
witnesses, parametrization/stratum, open forks (L4/BR-C, BR-B, L8/BR-A, BR-M, BR-CE, P1
weight supply, P2 dual class), and the Slice-2 duties. Counts
(`TC5_ledger_coverage_counts` [guard]): **20 adjudicated composite cells, all
witness-nonempty; 10 RES-CNEQ0 cells CENSUS-REQUIRED.**

**Known-object locations (OBSERVATIONS ONLY — F-S1;
`TC5_known_object_rows_are_observations` [guard]):**

| Object | Cell location |
|---|---|
| ω-shape | LE(P2 / P3-bulkP2 / P1 with λ-independent a_M); NV(P1 with a_M = 2λ) — computed; banked stratum stamps cited (off RES-CNEQ0; on-stratum witness for KMOD0) |
| EH-form (stationary restriction) | variational w.r.t. its metric-volume (P1-4D-type) pairing BY CONSTRUCTION of its action (Route C banked; GR-as-reference lane) — the RESTRICTED system's G3 status under the enumerated pairings is NOT adjudicated here (R12 restrict-vs-vary caveat; a Slice-2 cost item) |
| Bach-form | typed jet-3/4 class (outside the exhaustive layer); G5: EXTENSION-REQUIRED at jet ≤ 2 (derived); the order-4 condition machinery is anchored (`TC_jet34_order4_selfadjointness_anchor`, 2-field instance — the jet-3/4 G3 layer stays TYPED-NOT-EXHAUSTED) |
| CM0-C-type nonvariational members | the NV cell is their home CLASS (banked; none instantiated) |

## 6. Outcome and falsifier record (derivation-side)

**Outcome class: OS1** — the joint gate-cut map is a populated partition (20 adjudicated
composite cells, all witness-nonempty; 10 CENSUS-REQUIRED; forks carried). No gate empties
ℛ_PW at the declared scope (OS2 not triggered); no rigid low-parameter collapse (OS3 not
triggered). **The L6 fork is now the computed partition:** LOCALLY-EXACT vs NONVARIATIONAL
is a pairing-relative, computed cut with both cells populated under every enumerated branch
— both first-class. Ceiling respected: no member selected, no existence/uniqueness verdict
on the full ℛ (the WS legs are undischarged), no action adopted, no physics.

- **F-S1:** clean — no member selected/ranked; known-object rows are observations.
- **F-S2:** clean — every G3 statement carries its pairing-branch label; the W3
  adjudication carries a PROOF of branch-independence; no pairing adopted.
- **F-S3:** TWO instances of the named error class, both caught and cured — (1) the
  derivation's SELF-CATCH: the W2 "LE under P1" claim was first drafted field-sector-only
  and corrected to the full W2′ tuple statement before the verifier round; (2) the
  VERIFIER'S CATCH (A1): the anchored-log "whenever the field sector is nonzero" quantifier,
  refuted in-family (V10b) and restated as the exact iff condition at every occurrence
  (three `A1_*` zero-residual checks adopted). Otherwise policed — every only/all/none/empty
  statement carries its stratum + scope stamp (partition claims scoped to the enumerated
  branches, jet ≤ 2, witness-level; torsion vacuity scoped to closed forms on torsion
  cycles; blindness statements scoped to the T4 loci; the anchored-log statement now carries
  its exact iff condition and scope).
- **F-S4:** clean — banked facts recomputed as consistency (K₄, stabilizer ranks, the
  k_mod = 0 identity, T4 blindness, TC5 boundary instances); no contradiction found.
- **F-S5:** none — 52/52 (33 substantive + 19 guards, post-A1/A4), exit 0; deterministic
  rerun byte-identical (three consecutive post-amendment runs).
- **F-S6:** clean — no solution computed; TC2 is typing only; TC3 states slot OBLIGATIONS
  only; TC4 is type-level only.
- **F-S7:** carried — every J07/J11 classification row flags the twisted-H¹ machinery as
  MODEL-KNOWLEDGE; no banked G6 claim rests on it.

**Limits that travel:** (i) all adjudications at jet ≤ 2, BASE branch (+BR-A), registered
stationary presentation, enumerated pairing branches; (ii) nonemptiness is WITNESS-LEVEL,
not a full-cell census; (iii) RES-CNEQ0 CENSUS-REQUIRED throughout; (iv) jet-3/4 typed via
the order-4 anchor (2-field instance) only; (v) corners typed-only; (vi) sufficiency of the
Helmholtz conditions = the banked bicomplex statement (Category-A, cited) plus witness
instantiation — necessity is derived; (vii) P3's wall-block symmetry conditions and the
per-candidate wall depth are typed, per-declared-N (Slice 2); (viii) all WS/GC
solution-dependent legs untouched (R5, R14, gate 2, gate-1 on-shell, gate-4 currents).
