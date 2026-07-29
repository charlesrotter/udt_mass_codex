# P4 Route A Stage 2 — exact derivation record: the pointwise reduction ℛ_PW (TB1–TB6)

Date: 2026-07-29. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
derivation). Script: `derive_routeA_stage2.py` — **75/75 checks, exit 0 = 67
SUBSTANTIVE zero-residual exact-SymPy checks + 8 CITATION GUARDS** (A2 honest split:
guards = list/arithmetic/string bookkeeping of cited banked facts, labeled `[guard]`
in-script and in the JSON, never counted as residual computations), deterministic (no
floats/randomness/network; JSON, ledger, and stdout byte-identical across reruns),
single CPU process, < 2 s (FULL SCOPE at the declared jet ≤ 2 — not
throughput-limited; no scope reduction taken). Outputs:
`routeA_stage2_results.json`, `DERIVATION_STDOUT.txt`, `RESIDUAL_SPACE_LEDGER.tsv`.
Every check named in `monospace` below is one of the 75. TB6 lives in
`STAGE3_HANDOFF.md`.

**AMENDED 2026-07-29 per `VERIFIER_REPORT.md` (verdict PASS-WITH-REQUIRED-AMENDMENTS;
pre-amendment run 53/53, exit 0; amendment record `CORRECTION_LAYER.md`).** A1
(substantive): the §2 R7(b) "pointwise-vacuous" claim was **REFUTED AS STATED** by
the blind verifier — the rank-6/empty-nullspace computation is the CLASS-WIDE
stabilizer; the PER-MEMBER stabilizer jumps on strata. §2 now carries the corrected
statement (generic vacuity + the exact stratum Noether identities, the verifier
counter-computation adopted and extended), §4/§5 the cut parametrization and the
corrected/scoped witnesses. A2: the check split above. A3: the §3 E12 convention
note.

**ROUND-2 AMENDED 2026-07-29 per the `VERIFIER_REPORT.md` "AMENDMENT CLOSURE"
section (verdict NEW-DEFECT, item C3; round-1 run 67/67, exit 0).** The round-1
A1-extension headline "the ONLY genuine new cut is the k_mod = 0 identity" was
**REFUTED** by the closure verifier (`VERIFIER_CLOSURE_PROBE.py` P3/P5) — the same
error CLASS as the original refutation (a stratum-blind uniqueness gloss), one level
down: the auto-satisfaction argument covers ONLY the four NAMED C = 0 strata, while
the resonance rank-drop locus carries substantial C ≠ 0 sub-varieties whose
identities ARE further genuine cuts. **Corrected statement (travels with every
occurrence): k_mod = 0 is the only CODIMENSION-1 cut; the resonance locus carries
C ≠ 0 sub-varieties of higher codimension with additional exact identities** (derived
example: the shear identity −c10·r_sh − k10·m10 = 0 on {λ−k_mod = −1, c00 = c01 = 0});
the four NAMED C = 0 strata identities are auto-satisfied in the declared class. The
closure counter-computation is adopted as the `A1R2_*` checks (§2); the ω witness is
RE-SCOPED (an on-stratum witness for k_mod = 0 only); the FULL deeper stratification
is stamped TYPED-NOT-EXHAUSTED.

**Standing stamps (travel with every statement):** registered positive triangular
chart; conventions copied from the banked Route B registration (η = diag(−1,1,1,1);
X = [[H,0],[C,K]], H = diag(−1,1)); all statements are pointwise, one-parameter,
off-shell. The EXHAUSTED scope of every "exactly parametrized" claim is: **jet ≤ 2 in
the varied fields, on the registered stationary presentation (φ, f, bh in the toric
chart; general arenas replace these by full coframe data with multi-index jets — same
character/shift structure, typed only), polynomial/formal in the (k10, C) moduli**
(the smooth extension is the standard Schwarz-type finite-group statement,
Category-A, cited not re-proven). **A1 stamp (rounds 1+2):** the parametrization is exact OFF the
degeneration strata of the moduli and CUT BY the stratum Noether identities ON them
(§2; k_mod = 0 is the only CODIMENSION-1 genuine cut; the four named C = 0 resonance
identities are auto-satisfied in the declared class; the resonance locus also carries
C ≠ 0 sub-varieties of higher codimension whose identities ARE further genuine cuts —
one derived example, deeper stratification TYPED-NOT-EXHAUSTED). The jet-3/4 case is
TYPED, stamped NOT-EXHAUSTED (F-B3). NO
member of ℛ_PW is selected or privileged (F-B1); NO WS/GC gate is run. Banked facts
are RECOMPUTED as consistency and cited — never re-derived as new, never adopted
beyond banked scope. The Stage-1-A1-amended character rule and Stage-1-A3-amended
channel class are used throughout (F-B4; those are Stage-1 amendment labels, distinct
from THIS package's A1–A3).

**What Stage 2 imposed (exactly the PW layer of the prereg §1):** R1, R2, R4,
R7(a, b-identities), R8, R10, R12, R13; J01–J06(slot), J10, J12, J13(slot), J14.
NOT imposed (Stage 3's gates ON ℛ_PW): R3, R5, R6, R9, R14, R15; J07–J09, J11,
J13-completion, J15.

---

## 0. Premises (chose or derived — stamped)

| Premise | Tag |
|---|---|
| Registered chart + generator conventions | THEORY (banked 07-25 E02 registration; Route B convention copy) |
| Stage-1 bank: typed domain, census, four forced items (A1/A3-AMENDED), R/J tables | DERIVED input (b5aac4a + amendments; recomputed as consistency: `S0_*`, `PW1_*`) |
| Route B bank: E02 footing, T-block, exact K₄ + actions, trivial infinitesimal stabilizer | DERIVED input (recomputed: `S0_*`, `PW2_registered_stabilizer_trivial`) |
| Route C bank: EH ≤ 2-jet / Bach 3rd-4th-jet spread | DERIVED input, cited as EXAMPLES only (TC2/TC3; jet-order guards in `PW5_obs_*`) |
| 11-generator invariant ring generating set | DERIVED input (verifier-proven, Stage-1 bank; recomputed + extended to character modules here) |
| Jet order ≤ 2 for the exhaustive layer | Category-A bounded scope (prereg §2; stamp travels; NOT a freeze — jet 3/4 typed) |
| Degree-6 bound for the exhaustive monomial layer | Category-A conditioning (general degree = the banked parity proof, cited and re-instantiated) |
| SymPy exact, CPU, single process | Category-A conditioning |

## 1. TB1 — the building-block alphabet

**The pointwise blocks admitted by R1/R13/J12 provenance with J04 shift-equivariance
(one row per block; each row's graded assignment is a zero-residual check):**

| Block | Census source | Shift behavior | Local-Lorentz type | K₄ character |
|---|---|---|---|---|
| Q = c_E·e^{−φ} (founded anchored readout) | rows 5+7 | INVARIANT on the shift-with-absorption orbit (φ,c_E)↦(φ+s, c_E e^s) (`PW1_Q_orbit_invariant`, `PW1_D3_anchor_absorption_recomputed`) | chart scalar | trivial |
| φ-jets ∂φ, ∂²φ (and ∂³φ, ∂⁴φ for the typed extension) | row 5 | INVARIANT (`PW1_phi_jets_shift_invariant`) | chart scalar (stationary presentation) | trivial |
| f, ∂f, ∂²f | row 9 | inert | chart scalar | trivial |
| bh, ∂bh, ∂²bh | row 10 (seat factor NOT in bh) | inert | chart scalar | trivial |
| α (+ jets on the active fork) | row 8 | inert | chart scalar | trivial |
| λ, k_mod (seat scalars) | rows 11–12 | inert | K₄-invariant seat coordinates | trivial |
| the 11 invariants I1..I11 = {k10²; c00², c11², c00c11; c01², c10², c01c10; k10·{c00,c11}·{c01,c10}} | rows 13–14 | inert | functions on the moduli quotient | trivial (`PW1_invariant_ring_generators_11`) |
| χ_a prefactors {k10, c00c01, c00c10, c11c01, c11c10} | rows 13–14 | inert | relative (component prefactors, never standalone) | χ_a |
| χ_b prefactors {c00, c11, k10c01, k10c10} | row 14 | inert | relative | χ_b |
| χ_c prefactors {c01, c10, k10c00, k10c11} | row 14 | inert | relative | χ_c |
| T-block entries [[2I₂,Cᵀ],[C,K+Kᵀ]] | banked T2 (`S0_tangent_block_form`) | inert | bilinear form, T↦Λ⁻ᵀTΛ⁻¹ (`S0_tangent_transport_bilinear`) | entries reduce to the moduli blocks above (no new block) |
| e^{φX}-type exponentials | banked closed forms | anchored: e^{aφ} = (c_E/Q)^a (`PW1_cE_over_Q_is_exp_phi`); E04 lower block entry (i,j) = c_ij × φ-scalar (`PW1_expX_lower_block_entries_carry_C_characters`) | reduce to graded blocks | trivial / χ of the C-position |
| wall/corner data | rows 16–17 | supplied; anchored-φ ONLY through supplied-structure slots (Stage-1 V8 clash resolution, cited) | stratum data | trivial (bank) |
| 𝔠 completion label | row 18 | inert discrete argument slot | discrete | trivial |

**Exclusions at the alphabet gate (each a zero-residual witness):** bare φ / any
c_E^p e^{−qφ} with p ≠ q (`PW1_anchored_exponent_condition`, `PW1_bare_phi_excluded`
— the unique invariance condition is p = q, i.e. a Q-power); non-census blocks
(R1/J12 provenance, definition-level). J01/J02 typing: every configuration's coframe
is nondegenerate (`PW1_J01_coframe_nondegenerate`) with the founded base block H
fixed (`PW1_J02_founded_base_block`). K₄ acts ONLY on {k10, c00, c01, c10, c11}
(`PW1_K4_touches_only_k10_C`); the character table is recomputed
(`PW1_K4_characters_of_moduli`).

**Alphabet size (base branch, functional arguments):** grade 0: 10 = {Q, f, bh} +
the 7-dimensional moduli orbit (embedded by the 13 generator functions λ, k_mod,
I1..I11 WITH relations); grade 1: 13; grade 2: 16 — plus the supplied arguments
(α, c_E, wall data, 𝔠) (`PW4_functional_dimensions_per_grade`,
`PW2_invariant_ring_relations_and_orbit_dim`: generic K₄-orbit size 4 ⟹ orbit-space
dimension 5+2 = 7; sample ring relations I2I3 = I4², I5I6 = I7², I8I11 = I9I10 =
I1I4I7, … exact; the FULL relation ideal is stamped not-computed).

## 2. TB2 — the equivariance reduction (R7(a)/J10 solved; R7(b) imposed)

**Theorem (pointwise, registered chart).** The space of contragredient-equivariant,
character-matched component maps from the TB1 alphabet reduces EXACTLY to the K₄
character rule per component, because:

1. the connected local-Lorentz part has TRIVIAL **CLASS-WIDE** infinitesimal
   stabilizer on the registered chart — the linear system "[B,X] tangent to the
   class for every class member" has rank 6 on so(1,3)'s 6 coefficients, nullspace
   empty (`PW2_registered_stabilizer_trivial`, recomputing Route B T1) — so
   connected equivariance is a TRANSPORT/EXTENSION property (it generates the
   off-chart family by T ↦ Λ⁻ᵀTΛ⁻¹, `S0_tangent_transport_bilinear`), imposing no
   pointwise constraint on chart components AWAY from the degeneration strata (A1);
   and
2. the exact discrete residual K₄ imposes character matching (Stage-1-A1-amended
   bank), which is solved below as exhibited module bases.

**R7(b) Noether identities, imposed componentwise (A1-AMENDED — the pre-amendment
claim "the pointwise identity set is EMPTY" was REFUTED AS STATED by the blind
verifier: the class-wide computation is correct but does not decide the PER-MEMBER
question; per-member stabilizers jump on strata):**

- **Generic vacuity:** at a GENERIC member the per-member (pointwise) tangency
  stabilizer is trivial — rank 6, empty nullspace
  (`PW2_R7b_noether_generic_vacuous_stratum_identities`) — so R7(b) is vacuous at
  generic moduli.
- **The k_mod = 0 stratum identity (the verifier's counter-computation, adopted and
  extended).** Every nonzero 6×6 minor of the 9×6 pointwise tangency system is
  divisible by (k00 − k11) = −2k_mod (`A1_kmod0_rank_drop_all_members` — an
  ALL-member proof), so on the ENTIRE codimension-1 stratum **k_mod = 0** (the
  reciprocal-isotropy locus; K₄-stable) the rank drops to 5 with nullspace =
  span(L23), the screen rotation (`A1_kmod0_nullspace_is_L23`, symbolic = generic on
  the stratum). The tangency obstruction at a general member is exactly
  [L23,X](2,3) = 2k_mod (`A1_L23_obstruction_is_2kmod`). On the stratum,
  **[L23, X] = [[0,0],[J·C, k10·diag(1,−1)]] ≠ 0** for (k10, C) ≠ 0
  (`A1_gauge_direction_tangent_nonzero`), with chart reading (δλ, δk_mod, δk10, δC)
  = (0, −k10, 0, J·C) and ZERO field-sector variation on the registered stationary
  presentation (chart scalars carry no frame index; general arenas TYPED —
  `A1_gauge_chart_components_field_sector_zero`). R7(b) there imposes the exact
  pointwise Noether identity

      −2·k10·r_tf + m00·c10 + m01·c11 − m10·c00 − m11·c01 = 0   at k_mod = 0

  (`A1_stratum_noether_identity_form`; r_tr, r_sh AND the null slot r_nl all drop
  out; equivalently −k10·R_kmod + ⟨M, J·C⟩ = 0). The identity is K₄-consistent:
  every term is χ_a-graded and the direction transports as g·L23·g = χ_a(g)·L23
  (`A1_identity_chi_a_graded_K4_consistent`).
- **The resonance strata (higher codimension).** Off k_mod = 0 the
  rank-drop locus is confined EXHAUSTIVELY to the base-block eigenvalue resonances
  λ∓k_mod ∈ {±1} — the product (k00²−1)(k00−k11)(k11²−1) lies in the minor ideal
  (`A1_rank_drop_confined_to_resonances`; the CODIM-1 layer is exhaustive,
  Gröbner-verified). On the four NAMED strata (C = 0 with
  k00 = ∓1 or k11 = ∓1) the gauge directions (base–screen resonance boosts/
  rotations) and identities are DERIVED exactly
  (`A1_resonance_named_strata_identities`): k10·R_c10 = 0 at {C=0, λ−k_mod=−1};
  k10·R_c11 = 0 at {C=0, λ−k_mod=+1}; k10·[(k00+1)R_c00 + k10·R_c10] = 0 at
  {C=0, λ+k_mod=−1}; k10·[(k00−1)R_c01 + k10·R_c11] = 0 at {C=0, λ+k_mod=+1} —
  each involving ONLY mixing-kernel components. These are AUTOMATICALLY satisfied
  by every character-matched member of the declared polynomial/formal class (every
  χ_b/χ_c generator vanishes at C = 0 —
  `A1_resonance_identities_auto_satisfied_in_class`). **R2-CORRECTED:** the
  auto-satisfaction covers ONLY these four named C = 0 strata — **k_mod = 0 is the
  only CODIMENSION-1 cut; the resonance locus carries C ≠ 0 sub-varieties of higher
  codimension with additional exact identities** that ARE further genuine cuts (next
  bullet; the round-1 "the ONLY genuine new cut is the k_mod = 0 identity" was
  REFUTED by the closure verifier).
- **The C ≠ 0 resonance sub-varieties (ROUND-2 CLOSURE AMENDMENT — the closure
  verifier's counter-computation, adopted and check-backed).** The k00 = −1
  (λ−k_mod = −1) slice of the minor ideal has 7 solution branches (raw sp.solve census —
  contains nested/duplicate branches; the irreducible-component count is smaller, ~4, and
  the {k11 = −1} branch is the k_mod = 0 intersection; nothing rides on the raw count), including
  {c00 = c01 = 0, c10, c11 free} and the fully-generic-C branch
  {k11 = 1, c10 = −c00·k10/2, c11 = −c01·k10/2}
  (`A1R2_resonance_locus_has_Cneq0_branches`). On the sub-variety
  **{λ−k_mod = −1 (k00 = −1), c00 = c01 = 0}** (codim 3, K₄-stable) the pointwise
  nullspace is 1-dimensional = span(L02), the MIXED base–screen boost, tangent to
  the class with chart reading (δk10, δc10) = (−c10, −k10), all else zero
  (`A1R2_Cneq0_stratum_nullspace_L02`). R7(b) there imposes the exact pointwise
  Noether identity

      −c10·r_sh − k10·m10 = 0   (equivalently −c10·R_k10 − k10·R_c10 = 0)

  (`A1R2_Cneq0_stratum_shear_identity`) — it **cuts the SHEAR slot r_sh**, unlike
  the k_mod = 0 identity (r_sh drops out there) and the named C = 0 identities
  (mixing-only). The identity is χ_b-graded and K₄-consistent
  (`A1R2_shear_identity_chi_b_graded_K4_consistent`). It is a GENUINE further cut:
  the character-matched member R_c10 = c10 pairs to −c10·k10 ≢ 0
  (`A1R2_member_Rc10_genuine_cut`), and the ω-shape witness (r_sh = k10) ALSO
  pairs to −c10·k10 ≢ 0 there (`A1R2_omega_witness_violates_on_Cneq0_stratum`) —
  the ω witness is hereby RE-SCOPED (an on-stratum witness for k_mod = 0; NOT a
  universal on-resonance witness). The corrected trace-free witness
  (c01c10, 2k10c01) VANISHES on the found strata (c01 = 0 there) and survives the
  new cut (`A1R2_corrected_witness_vanishes_on_found_strata`); field-sector members
  (all moduli components zero, e.g. R_φ = Q) pair to zero with EVERY gauge
  direction on every stratum and carry all-strata nonemptiness
  (`A1R2_field_sector_members_carry_all_strata`). **STAMP: the FULL deeper
  stratification is TYPED-NOT-EXHAUSTED** — the codimension-1 layer is exhaustive
  (the Gröbner minor-ideal proof); the deeper layers are derived EXAMPLES plus the
  method (the same nullspace/pairing computation applied branch-by-branch), NOT a
  census.
- K₄ carries no parameter (discrete); current-conservation statements remain WS
  (Stage 3).

**OBSERVATION (A1, recorded — the positive content of the refutation):** this is the
FIRST nontrivial pointwise Noether content of the response problem — on the
reciprocal-isotropy locus k_mod = 0 the forced trace-free slot r_tf is tied EXACTLY
to the mixing kernel M by the identity above. Scope stamps: registered chart,
registered stationary presentation, pointwise, one-parameter, off-shell,
polynomial/formal in the moduli; order-independent (moduli-sector, jet-blind).
Factual cross-thread note: the identity's gauge direction is the screen rotation
(the twist/angular direction).

**The character modules — computed bases (F-B6):** component dependence on
(k10, C), per K₄ character class, as a module over the invariant ring
R = ⟨I1..I11⟩:

| Class | Paired directions | Minimal generators (EXHIBITED) | Rank |
|---|---|---|---|
| trivial | δφ, δf, δbh [, δα], δλ, δk_mod, boundary | {1} (verbatim factoring through I1..I11) | 1 |
| χ_a | δk10 | {k10, c00c01, c00c10, c11c01, c11c10} | 5 gens; generically 1 |
| χ_b | δc00, δc11 | {c00, c11, k10c01, k10c10} | 4 gens; generically 1 |
| χ_c | δc01, δc10 | {c01, c10, k10c00, k10c11} | 4 gens; generically 1 |

Proofs, all zero-residual: generators carry their class characters
(`PW2_module_generators_have_declared_characters`); GENERATION — every monomial of
degree ≤ 6 in each class factors as (listed generator) × (invariant), exhaustively
(127 trivial + 118 χ_a + 108 χ_b + 108 χ_c monomials;
`PW2_trivial_class_generation_deg6`, `PW2_{chi}_module_generation_deg6`), with the
general-degree argument = the banked parity proof re-instantiated (χ_a: e odd ⟹
divide k10, e even ⟹ p+q and r+s odd ⟹ divide a c_b·c_c pair; χ_b/χ_c mirrored;
remainder parity trivial); MINIMALITY — the invariant ring starts at degree 2
(`PW2_no_degree1_invariants`) and each class's degree ≤ 2 monomials are exactly its
generators (`PW2_chi_a_minimality`, `PW2_chi_b_chi_c_minimality`); the modules are
NOT free — sample syzygies with invariant coefficients exhibited exactly (I1·a2 −
I8·a1 = 0, I4·a2 − I2·a4 = 0, I8·b1 − I2·b3 = 0, I8·c1 − I5·c3 = 0;
`PW2_module_syzygies_exhibited`; full syzygy ideal stamped not-computed);
GENERICALLY RANK 1 — away from the K₄-fixed strata every generator is an
invariant-ratio multiple of one (`PW2_generic_rank_one`): each class is a line over
the orbit space, the extra generators are needed exactly on the fixed strata.

**Resulting per-component-type equivariant spaces (the TB2 deliverable, per grade g ∈
{0,1,2}):** with A_g := functions of the graded alphabet (dims 10/13/16;
polynomial/formal in the moduli functions, smooth in the rest — scope stamp):

    R_φ, R_f, R_bh [, R_α] ∈ A_g                      (trivial; basis {1})
    R_λ, R_k_mod, R_wall, R_corner ∈ A_g              (trivial; basis {1})
    R_k10 ∈ ⊕_{j=1..5} a_j · A_g  (mod syzygies)      (χ_a; basis {a_1..a_5})
    R_c00, R_c11 ∈ ⊕_{j=1..4} b_j · A_g (mod syzygies) (χ_b; basis {b_1..b_4})
    R_c01, R_c10 ∈ ⊕_{j=1..4} c_j · A_g (mod syzygies) (χ_c; basis {c_1..c_4})

## 3. TB3 — the slot/seat reduction (R4/J06 exact)

**Screen sector.** The screen pairing kernel W (⟨W, δK⟩ = tr(Wᵀ δK), δK = δλ·I₂ +
δk_mod·diag(−1,1) + δk10·E21) decomposes UNIQUELY as W = r_tr·I₂ + r_tf·diag(−1,1) +
r_sh·E21 (+ a NULL E12 slot, unpaired by every δK direction, quotiented out) — the
trace-pairing Gram of {I₂, diag(−1,1), E21} is diag(2,2,1), nondegenerate
(`PW3_screen_pairing_basis_unique`). **A3 CONVENTION NOTE:** "E12 is a null unpaired
slot" is a statement in the chart-δK pairing convention; against the PHYSICAL tangent
δ(K+Kᵀ) (Route B T-block) the component pairings read (4r_tr, 4r_tf, r_sh + r_nl) —
the symmetric E12+E21 combination pairs — an invertible reparametrization of the SAME
component space, so the decomposition is convention-independent
(`A3_pairing_convention_isomorphic`; no math changes). The moduli components ARE the
slot coefficients:

    R_λ = 2·r_tr ,   R_k_mod = 2·r_tf ,   R_k10 = r_sh      (`PW3_component_pairings`)

The banked slot theorem holds and is recomputed: ⟨r_tr·I₂, diag(−1,1)⟩ ≡ 0, and a
kernel with ZERO trace-free slot has R_k_mod ≡ 0 identically even with arbitrary
r_sh and null-slot content (`PW3_slot_theorem_recomputed`); d(tr K²)'s k_mod-pairing
routes precisely through its trace-free part (`PW3_trX2_routes_through_tracefree`).

**The slot decomposition is character-graded (ties TB2 to TB3):** under every K₄
element the kernel transports with r_tr, r_tf fixed and r_sh flipping exactly with
χ_a — the characters of the paired directions
(`PW3_kernel_K4_transport_matches_characters`); the mixing kernel M (pairing δC)
transports entrywise with exactly the character of its paired dc_ij
(`PW3_C_kernel_transport_matches_characters`). So the (λ, k_mod, k10, C) component
block is parametrized as:

    R_λ = 2 r_tr ∈ A_g ;  R_k_mod = 2 r_tf ∈ A_g ;  R_k10 = r_sh ∈ χ_a-module ;
    (R_c00, R_c11) ∈ χ_b-module ;  (R_c01, R_c10) ∈ χ_c-module .

**J06 determined-vs-retained branch structure, explicit PER FAMILY (no branch
chosen; both branches are open sub-loci of ℛ_PW —
`PW3_J06_both_branches_nonempty_per_family`):**

| Family | DETERMINED branch (open condition) | RETAINED branch |
|---|---|---|
| λ | r_tr ≢ 0 | r_tr ≡ 0, λ reported residual |
| k_mod | r_tf ≢ 0 — reachable ONLY with the trace-free slot present (slot theorem; A3-amended F-RA2) | r_tf ≡ 0, k_mod reported residual (the ONLY branch open to trace/volume-channel screen sectors) |
| k10 | r_sh ≢ 0 (χ_a-matched, e.g. k10·inv or c_b c_c·inv) | r_sh ≡ 0, k10 retained |
| C | M ≢ 0 entrywise (χ_b/χ_c-matched) | M ≡ 0, C retained |

The named J06 false pass ("spectator screen isotropy or trace zero assumed") =
silently deleting the r_tf or M slots; in ℛ_PW those slots are PRESENT and their
vanishing is an explicit branch, never an omission.

## 4. TB4 — ℛ_PW at the declared scope

**The residual space (the deliverable):** a member of ℛ_PW at jet ≤ 2 is exactly a
choice, per component row of `RESIDUAL_SPACE_LEDGER.tsv`, of an element of the TB2
space (§2) with the TB3 slot structure (§3), over the TB1 alphabet — i.e.

    ℛ_PW ≅ { (R_φ, R_f, R_bh, 2r_tr, 2r_tf, r_sh, M, R_wall, R_corner)
             : trivial-character entries ∈ A_g ; r_sh ∈ χ_a-module ;
               M ∈ (χ_b ⊕ χ_c)-modules ; grades g ≤ 2 declared per component }
             CUT BY the A1 stratum Noether identities (§2, rounds 1+2):
             −2·k10·r_tf + ⟨M, J·C⟩-terms = 0 on k_mod = 0   (the only codim-1 cut)
             −c10·r_sh − k10·m10 = 0 on {λ−k_mod = −1, c00 = c01 = 0}   (R2 example)
             (the four named C = 0 resonance identities are auto-satisfied in this
             class; further C ≠ 0 sub-variety identities TYPED-NOT-EXHAUSTED)

with generators = the alphabet arguments + the character-module generators;
relations = the invariant-ring relations + the module syzygies (samples exhibited,
full ideals stamped not-computed) + the stratum identities (the k_mod = 0 relation —
ONE scalar relation among the on-stratum restrictions of (R_kmod, R_C); the R2 shear
relation among (R_k10, R_c10) on the found C ≠ 0 sub-variety — see the
STRATUM-IDENTITY rows of the ledger; deeper sub-variety relations typed, not
enumerated); dimensions = functional dims 10/13/16 per grade × module ranks
(1/5/4/4, generically 1), unchanged OFF the strata, cut by one functional relation
ON each derived stratum. **A1 note: the pre-amendment parametrization (without the
cuts) is a strict SUPERSET of ℛ_PW on the k_mod = 0 stratum (round 1) and on the
C ≠ 0 resonance sub-varieties (round 2).**

**Typing conditions verified on the family:** R2 census coverage — a component slot
for EVERY census direction, no extras (`PW4_R2_census_component_coverage`); J05 full
tangent paired (`PW4_J05_full_tangent_paired`); J13 discriminator slots retained
(`PW4_J13_discriminator_slots_retained`); R12/J14 — off-shell full-domain type with
the restrict-then-vary inequivalence witness recomputed
(`PW4_R12_J14_witness_recomputed`); R13 — no global entry in the alphabet
(`PW4_R13_no_global_entries_in_alphabet`, definition-level); R10 — E02 footing by
construction (`PW4_R10_E02_footing_by_construction`); R8 — every ledger row carries
its declared grade, so D𝓡 is computable at jet level (typing; the Helmholtz TEST
itself is gate 3, not PW).

**Fork-branch dependence (F-B2 — labels carried or independence proven):**

| Branch | Effect on ℛ_PW | Status |
|---|---|---|
| BASE (moduli-const, α-frozen, c_E-const, bdy-held) | as above | EXHAUSTED at jet ≤ 2 |
| BR-A (α active) | + R_α (trivial character) + α-jets in the alphabet (dims +1 per grade) | EXHAUSTED at jet ≤ 2 (same theorem applies) |
| BR-M (moduli → fields) | + 7 character-typed moduli-jet arguments per jet order; K₄ acts pointwise so the character rule is unchanged | TYPED ONLY — extends the banked pointwise class (census consequence); NOT-EXHAUSTED |
| BR-CE (c_E promoted) | + R_cE + c_E-jets (unregistered DOF) | TYPED ONLY; NOT-EXHAUSTED |
| BR-B (boundary varied vs held) | IDENTICAL component expressions; only the ROLE differs (paired equations vs consistency conditions) | PROVEN pointwise branch-independent; role labeled |
| BR-C (completion within vs over class) | 𝔠 is discrete in both forks and enters only as a supplied argument slot | PROVEN pointwise branch-independent; the difference is GC (Stage 3) |

**The jet-3/4 case (TYPED, NOT-EXHAUSTED — F-B3):** 3rd/4th field jets are
shift-invariant and K₄-inert (`PW1_phi_jets_shift_invariant` n=3,4;
`PW4_jet34_extension_is_alphabet_only`), so the jet > 2 extension is PURELY an
alphabet enlargement (+3 arguments per additional jet order on the base branch, +
wall momenta depth per Route C TC5 examples): the TB2 character modules, TB3 slot
structure, the A1-amended R7(b) content (generic vacuity + the stratum identities —
moduli-sector, hence jet-blind; verifier-confirmed order-independent), and every
exclusion are ORDER-INDEPENDENT; only the exhaustive parametrization is
order-bounded at jet ≤ 2. The Bach-side class lives here (Route C TC2, cited).

## 5. TB5 — the pointwise verdict

**ℛ_PW at the declared scope is NONEMPTY — outcome class OB1**
(`PW5_verdict_nonempty_OB1`; nonzero members exhibited in every character sector).
The exact parametrization (§4 + the ledger, CUT BY the A1 stratum identities) is the
deliverable. OB2/OB3 do not arise; no emptiness argument exists to grade.
**A1-amended witness record (rounds 1+2 — per-witness stratum stamps):** ON the
k_mod = 0 stratum, nonemptiness is witnessed by the ω-shape
(`A1_omega_witness_satisfies_identity`) and by the corrected trace-free witness
(r_tf, m00) = (c01·c10, 2·k10·c01), character-matched with
R_kmod = 2·c01·c10 ≢ 0 — the k_mod-DETERMINED branch stays nonempty on-stratum
(`A1_corrected_tracefree_witness_on_stratum`); the pre-amendment constant witness
(unit trace-free kernel, R_kmod = 2) VIOLATES the stratum identity at k10 ≠ 0
(`A1_old_witness_violates_on_stratum`) and is retained ONLY as the
off-stratum-scoped witness (k_mod ≠ 0). **R2 re-scoping:** the ω-shape is an
ON-STRATUM witness for k_mod = 0 ONLY — it VIOLATES the C ≠ 0 resonance shear
identity (`A1R2_omega_witness_violates_on_Cneq0_stratum`) and is NOT a universal
on-resonance witness; the corrected trace-free witness vanishes on the found C ≠ 0
defect stratum and SURVIVES the new cut
(`A1R2_corrected_witness_vanishes_on_found_strata`); field-sector members (all
moduli components zero, e.g. R_φ = Q) pair to zero with every gauge direction on
EVERY stratum — the all-strata nonemptiness carrier, independent of the
not-exhausted deeper stratification (`A1R2_field_sector_members_carry_all_strata`).

**Known objects located (OBSERVATIONS ONLY — F-B1; nothing selected):**

| Object | Location w.r.t. ℛ_PW |
|---|---|
| Stage-1 ω = k10·dk10 = ½d(k10²) shape | INSIDE off the C ≠ 0 resonance sub-varieties: R_k10 = k10 = a₁×1 (χ_a-matched, exact), all other slots 0 = J06 retained branch for the rest (`PW5_obs_omega_shape_in_RPW`); satisfies the k_mod = 0 identity (on-stratum witness there) but VIOLATES the C ≠ 0 resonance shear identity — R2 per-witness stratum stamps |
| EH-form G_ab + Λg_ab (restricted to the registered stationary family) | INSIDE the jet ≤ 2 class: ≤ 2nd jets on every component (Route C TC3, CITED); φ-dependence through seat exponentials = anchored Q-powers (recomputed); trivial-character field sector; (k10,C)-independent on the diagonal presentation ⟹ J06 retained branch for k10/C there (`PW5_obs_EH_form_lands_in_jet2_class`) |
| Bach-form | OUTSIDE the jet ≤ 2 exhausted scope, INSIDE the typed jet-3/4 extension class (Route C TC2, CITED; `PW5_obs_Bach_form_typed_class_only`) |
| CM0-C-type nonvariational members | NOT excluded pointwise: Helmholtz is gate 3, a classification, not a PW requirement (L6 carried both ways) |

**Banked no-go structures excluded, with the excluding PW requirement (fence
locations, recorded):** character-MISMATCHED components — R7(a)/J10
(`PW5_excl_character_mismatch`); absolute-φ bulk dependence — J04/F-RA4
(`PW5_excl_bare_phi_zero_point`; anchored-φ wall data only through supplied slots,
V8 cited); pure-trace screen kernels claiming k_mod determination — R4/J06
(`PW5_excl_pure_trace_kernel_from_determined_kmod`; they survive only on the
explicit retained branch); restrict-then-vary / EH-RED scar class — R12/J14
(`PW5_excl_restrict_then_vary`); fitted-global-average couplings and non-census
blocks — R1/R13/J12 (definition-level).

## 6. Outcome and falsifier record (derivation-side)

**Outcome class: OB1.** ℛ_PW is nonempty and exactly parametrized at the declared
scope (cut by the A1 stratum Noether identities on the degeneration strata); the
parametrization (this document + `RESIDUAL_SPACE_LEDGER.tsv` +
`routeA_stage2_results.json`) is the deliverable; the Stage-3 surface is
`STAGE3_HANDOFF.md`.

- F-B1 (selection): CLEAN — known-object locations are recorded as observations with
  the TB5 recording rule; no member selected/privileged; no WS/GC gate run.
- F-B2 (silent fork freeze): CLEAN — six branches carried; BR-B and BR-C PROVEN
  pointwise branch-independent, the rest labeled (two of them TYPED/NOT-EXHAUSTED).
- F-B3 (jet-order slip): **TWO F-B3-CLASS SCOPE SLIPS, both verifier-caught and
  AMENDED** — (round 1, A1) the R7(b) vacuity was a GENERIC-stratum truth stated
  unqualified (a class-wide vs per-member conflation); restated with the stratum
  identities and the "exact OFF the strata / cut ON them" stamp. (Round 2, A1-R2 —
  closure verdict NEW-DEFECT C3) the "only genuine cut" headline was the SAME error
  class one level down (a stratum-blind uniqueness gloss over the C ≠ 0 resonance
  sub-varieties); restated as "k_mod = 0 = the only CODIMENSION-1 cut" with the
  derived shear-identity example and the TYPED-NOT-EXHAUSTED deeper-stratification
  stamp. Otherwise clean — every exhaustive claim carries
  the jet ≤ 2 + presentation + polynomial-in-moduli stamp; order-independent
  structural claims (equivariance reduction, character modules, slot structure,
  exclusions, the amended R7(b) content) are stated as such and separately from the
  order-bounded parametrization.
- F-B4 (bank contradiction): CLEAN as to usage — Stage-1-A1-amended character rule
  and Stage-1-A3-amended channel class used throughout; every recomputed banked fact
  matched (K₄ actions, T-block, stabilizer, slot theorem, invariant generators, D3).
  The A1 finding indicts an upstream interpretation-layer GLOSS (Stage-1 POSED §1.4
  "mod nothing continuous"; Route B T1 headline), not Stage 2's use of the banked
  computations — routed to the driver via `UPSTREAM_PRECISION_FLAG.md` (draft, NOT
  applied).
- F-B5 (symbolic failure): none — 75/75 (67 substantive + 8 guards), exit 0
  (pre-amendment 53/53; round-1 67/67).
- F-B6 (equivariance by fiat): CLEAN — every equivariant space carries its computed
  basis: exhibited minimal generators, generation proven exhaustively to degree 6
  with the general-degree parity argument cited, minimality proven, sample syzygies
  and generic-rank-1 computed.

**Limits that travel:** (i) exhaustive layer = jet ≤ 2, registered stationary
presentation, polynomial/formal in (k10,C); (ii) jet 3/4 and BR-M/BR-CE branches
typed only; (iii) wall/corner slot DEPTH is example-typed (Route C TC5 cited), not
proven; (iv) full syzygy/relation ideals not computed; (v) A1 scope (rounds 1+2): the stratum
identities are derived on the registered stationary presentation (field sector
vanishes there; general arenas typed); the C ≠ 0 resonance sub-varieties carry
FURTHER genuine cuts — one derived example (the shear identity), the FULL deeper
stratification TYPED-NOT-EXHAUSTED (codim-1 layer exhaustive; deeper layers =
examples + method, not a census); the resonance auto-satisfaction holds for the four
NAMED C = 0 strata within the declared polynomial/formal class; (vi) all WS/GC content untouched — nothing here says any
member of ℛ_PW closes, is differentiable on the cell, or has controlled periods;
existence/uniqueness on the FULL ℛ is Stage 3's question (pre-committed ceiling
respected).
