# P4 Route B Stage 1 — exact derivation (constraint layers C1–C4)

Date: 2026-07-28. Contract: `PREREGISTRATION.md` (this package), including the T4
pre-derivation amendment (no banked volume-blind pin; it must be derived or dropped).
Script: `derive_routeB_stage1.py` — 100/100 zero-residual SymPy checks, exit 0
(`DERIVATION_STDOUT.txt`, `routeB_stage1_results.json`). Every check named below in
`monospace` is one of the 100. AMENDED per the blind verifier's A1
(`VERIFIER_REPORT.md`, `CORRECTION_LAYER.md`): the finite residual chart symmetry is
the Klein four-group, now proven EXACT (15 added checks); the original derivation
overstated a Z₂. Survival verdicts, T5 table, and re-tags are unchanged.

## 0. Premises and conventions (chose or derived — stamped)

| Premise | Tag |
|---|---|
| Registered positive triangular chart; X = [[H,0],[C,K]], H=diag(−1,+1) on slots (0=clock, 1=ruler); K=[[k00,0],[k10,k11]] lower-triangular on slots (2,3 = screen); C=[[c00,c01],[c10,c11]] | THEORY (banked E02 registration, 07-25); chart-covariance is itself T1's question, not assumed |
| η = diag(−1,1,1,1); Lorentz generator convention L{ab}[a,b]=1, L{ab}[b,a]=−η_aa/η_bb | THEORY (copied from the banked 07-27 script, lines 40–48) |
| Banked swap F = [[0,1],[1,0]]⊕I₂ (screen-identity extension) | THEORY (07-27 registered object). Any swap condition below is CONDITIONAL on this specific supplied F |
| Concatenation order: segment 1 then segment 2 ⇒ composite matrix M₂M₁ | FREE (convention; both orders give the mirrored cocycle law) |
| 18-family active premise set has zero selector rank on the 7 directions | DERIVED input (07-26) — the reason no cell below may cite it as forcing (F-A guard `T5_F-A_guard_every_forcing_column_is_supplied`) |
| SymPy exact, CPU, single process | Category-A conditioning |

Banked-input consistency recomputations (`S0_*`, 8 checks): physical-tangent rank 7 and its
block form T = [[2I₂, Cᵀ],[C, K+Kᵀ]]; so(1,3) dimension 6; joint rank 13 of the 7 extension
directions plus so(1,3); full-Lorentz commutant rank 15 with scalar-identity solution; E08
det-one and generator; seal identity.

## T1 — transformation law of (K,C); covariance typing per stratum

**(a) Presentation (gauge) law.** Two constant generators X, X′ present the same anchored
family (E(0)=I, same physical metric family g(φ)=E(φ)ᵀηE(φ)) iff
L(φ) := e^{φX′}e^{−φX} ∈ SO⁺(1,3) for all φ. Differentiating at φ=0: X′ − X ∈ so(1,3).
The 7 extension directions and the 6 so(1,3) generators are jointly independent
(`S0_extension_plus_so13_rank_13`, rank 13), so the intersection is zero: presentation
orbits inside the registered class are **singletons**. Consequence: **no stratum is a
chart/presentation artifact** — each is an honest condition on the physical quotient,
given the registered split. (Recomputes the banked 07-26/07-27 rank facts.)

**(b) Equivariance (frame-rotation) law.** The banked full-frame correction (07-26): the
operation transforms as X ↦ ΛXΛ⁻¹. Exact structure-preserving stabilizers, solved for
B = Σβᵢ Lᵢ with the two conditions [B, X₀] ∈ V and [B, V] ⊆ V:

- Registered class (fixed H block, zero upper-right, K lower-triangular): infinitesimal
  stabilizer **trivial** (`T1_registered_chart_infinitesimal_stabilizer_trivial`).
- Relaxed block form (general K): stabilizer is exactly the screen rotation span(L23),
  dim 1 (`T1_blockform_infinitesimal_stabilizer_dim_1`,
  `T1_blockform_stabilizer_is_screen_rotation_L23`), acting as
  **(K, C) ↦ (S K S⁻¹, S C)**, S ∈ SO(2) (`T1_screen_rotation_K_conjugation_C_left_action`);
  H block and zero upper-right block are preserved. K-triangularity is NOT preserved:
  the (2,3) entry of S K S⁻¹ at θ=π/2 is −k10 ≠ 0
  (`T1_K_triangularity_not_preserved_probe`) — the K-triangularization is what uses up
  the screen SO(2).
- Finite residual of the registered chart (**AMENDED A1 — now EXACT, exhaustiveness
  proven**): the **Klein four-group**

      K₄ = {I, diag(1,1,−1,−1), diag(1,−1,−1,1), diag(1,−1,1,−1)} ⊂ SO⁺(1,3),

  acting as: R23(π)=diag(1,1,−1,−1): **(K,C) ↦ (K,−C)**
  (`T1_R_pi_action_K_fixed_C_negated`); R12(π)=diag(1,−1,−1,1): **k10 ↦ −k10,
  (c00,c11) ↦ (−c00,−c11)** (`T1_R12pi_action_flips_k10_c00_c11`);
  R13(π)=diag(1,−1,1,−1): **k10 ↦ −k10, (c01,c10) ↦ (−c01,−c10)**
  (`T1_R13pi_action_flips_k10_c01_c10`). The original claim "Z₂ = {I, R_π}" was an
  understatement caught by the blind verifier (F-D-class quantifier slip; A1).
  **Exhaustiveness proof** (bounded, four steps, all zero-residual): (1) a probe
  mixing member (C=I, K=0) forces the upper-right block of any class-preserving
  Λ ∈ SO⁺(1,3) to vanish (`T1_residual_probe_forces_upper_right_block_zero`);
  (2) η-preservation then forces Λ block-diagonal — S ∈ O(2), SᵀX_b=0 with
  coefficient determinant (det S)² ≠ 0 kills the off-diagonal block
  (`T1_residual_lorentz_blockform_identities`,
  `T1_residual_offdiag_coefficient_det_is_detS_squared`); (3) fixing the H block
  forces the base block diagonal ([A,H]=0), signed (Aᵀη₂A=η₂), with clock sign +1 by
  orthochronicity (`T1_residual_A_commutes_H_iff_diagonal`, `T1_residual_A_signs_pm1`);
  (4) preservation of K-lower-triangularity forces the screen block signed-diagonal —
  the k10 probe gives (S E21 adj S)[0,1] = −q² (`T1_residual_S_triangularity_forces_q_zero`,
  `T1_residual_S_orthogonality_forces_signed_diag`). Enumerating diag(1,±1,±1,±1)
  with det=+1 yields exactly the four elements; each is proper orthochronous
  Lorentz, fixes X₀, and preserves the class; the set is closed, every element an
  involution, R12(π)·R13(π)=R23(π)
  (`T1_residual_exhaustive_enumeration_klein_four`,
  `T1_residual_klein_elements_preserve_class_and_fix_X0`,
  `T1_residual_klein_group_closure_involutions`, `T1_R_pi_is_klein_R23pi`).
  All stratum-defining conditions (tr K=0; K=0; C=0) are invariant under the full K₄
  and the screen-SO(2) action (`T1_strata_invariant_under_klein_group`,
  `T1_strata_invariant_under_screen_action`), so every stratum is well defined on the
  registered chart modulo its residual symmetry — and the **carried moduli k10 and C
  are read modulo this K₄ quotient** (k10 mod sign; C mod the signed-flip action;
  λ and k_mod are K₄-invariant).

**(c) Covariance typing per stratum (the exact orbit computation).**

- **E03 (det-one): COVARIANTLY DEFINED, fully.** tr X = k00+k11 is invariant under
  conjugation by an arbitrary 16-parameter matrix (`T1_E03_trace_conjugation_invariant`),
  and det e^{φX} = e^{φ tr X}: X is fully lower-triangular, the diagonal projection is
  multiplicative on lower-triangular matrices and det is the diagonal product
  (`T1_lower_triangular_diagonal_multiplicative`, `T1_det_lower_triangular_is_diag_product`;
  instantiated exactly on the diagonal subfamily, E08, and the E04 closed form —
  `S0_E08_det_one`, `T2_E04_det_one_family`). Equivalently: tr(η⁻¹T) = 2 tr X, a
  frame-invariant functional of the physical tangent.
- **E04, E05 (transverse-invariant; no-mixing): SPLIT-RELATIVE (chart-dependent under the
  full connected group).** Exact orbit witness: conjugating a generic E04 member by the
  ruler–screen rotation R12(θ) produces a nonzero upper-right block at θ=π/2
  (`T1_E04_orbit_leaves_chart_class_probe`) — the rotated operator leaves the registered
  class entirely. Deeper: the physical tangent transports as T ↦ Λ⁻ᵀTΛ⁻¹
  (`T1_tangent_transports_as_bilinear_form`) and the chart-anchored top-left block 2I₂
  moves (`T1_E06_topleft_anchor_moves_probe`); the three exact obstruction functionals
  (left-null space of the 13-dim presentable span, `T1_anchored_class_complement_dim_3`)
  are nonzero on the rotated member (`T1_E04_orbit_obstruction_nonzero_probe`) — even the
  spectator's orbit exits the class (`T1_E06_spectator_orbit_also_leaves_class_probe`).
  So "transverse block of T vanishes" / "cross block of T vanishes" are conditions on the
  PAIR (T, supplied base/screen split), not on T alone. They are covariant exactly
  relative to the registered split — not absolutely. This is a typing, not an
  elimination (F-E: no merit judgment).
- **E06 (spectator): SPLIT-RELATIVE as a fixed condition; its equivariant content is the
  conjugacy class of H4.** ηT/2 for the spectator equals H4 = diag(−1,1,0,0)
  (`T1_E06_eta_symmetrization_is_H4`) and transports by conjugation, ηT̃/2 = Λ H4 Λ⁻¹
  (`T1_E06_condition_transports_by_conjugacy_of_H4`) — the banked equivariance correction
  (07-26: scalar-only centralizer, no fixed non-scalar invariant generator) instantiated
  at the stratum level.

## T2 — bracket/subalgebra and finite composition closure

**Brackets (exact, generic members X = X₀ + v):**

- The bracket of any two E02 members lands in the linear part V
  (`T2_E02_bracket_lands_in_V`) and is always traceless — so every bracket lands in the
  E03 linear part (`T2_bracket_always_traceless_lands_in_E03_linear_part`). Every stratum
  span (RH ⊕ its linear part) is a Lie subalgebra; the class group is a solvable
  triangular group with upper block e^{φH}.
- E04: [X₁,X₂] = [[0,0],[(C₁−C₂)H, 0]] exactly (`T2_E04_bracket_exact_form`) — a
  nonabelian shift (affine-type) algebra (`T2_E04_nonabelian`).
- E05: bracket block-diagonal with [K₁,K₂] lower-triangular
  (`T2_E05_bracket_block_diagonal_lower_tri`).

**Finite closure (exact closed forms, no truncations):**

- E04 closed form: M(φ;C) = [[e^{φH}, 0],[C H (e^{φH}−I), I₂]] solves M′ = XM, M(0)=I
  (`T2_E04_closed_form_solves_ODE`, `_initial_condition`) — hence IS the exponential
  (uniqueness of the linear ODE). Same-member composition is exactly additive
  (`T2_E04_same_member_additive`).
- **Exact failure statement (all strata with ≥ 2 members): cross-member composition
  closes in the class GROUP but drifts the member.** For E04 the drift law is exact:
  M(φ₂;C₂)M(φ₁;C₁) = M(φ₁+φ₂; C₃(φ₁,φ₂)) with
  C₃[i,j] = [C₂[i,j](e^{φ₂h_j}−1)e^{φ₁h_j} + C₁[i,j](e^{φ₁h_j}−1)] / (e^{(φ₁+φ₂)h_j}−1),
  h = (−1,+1) (`T2_E04_cross_member_product_equals_effective_member`); C₃ is constant
  iff C₂=C₁ (`T2_E04_effective_member_constant_iff_same_member`,
  `T2_E04_member_drift_nonzero_for_distinct_members`). For E07: the product of members
  k ≠ k′ is never exp((φ₁+φ₂)X_{k″}) for constant k″
  (`T2_E07_cross_member_closure_iff_equal_members`). Even for commuting members the
  effective member is the (φ₁,φ₂)-dependent affine mixture (φ₁X₁+φ₂X₂)/(φ₁+φ₂), which
  stays in the (affine) class but is not a fixed member
  (`T2_affine_effective_member_phi_dependent_iff_distinct`).

Verdict: **every stratum is composition-closed as a family (subalgebra + group closure);
one-parameter anchored closure holds only per member.** Member drift under concatenation
is exactly the structure that makes a global assignment need transition data (→ T3, J07/J11).

## T3 — the mixing cocycle

**E08 exact law** (segment 1 then 2; u := s·σ(φ), σ(φ) = 1−e^{−φ}):

    u₁₂ = u₁ + e^{−φ₁} u₂            (`T3_E08_cocycle_u12`)
    s₁₂ = [s₁σ(φ₁) + s₂ e^{−φ₁} σ(φ₂)] / σ(φ₁+φ₂)   (`T3_E08_composed_map_in_class_with_drifted_s`)

with the cocycle (associativity) identity holding exactly over three segments
(`T3_E08_cocycle_identity_associativity`). The residual chart symmetry acts on the E08
member (AMENDED A1: the residual is the exact Klein four-group, not a Z₂): R23(π) and
R12(π) map s ↦ −s, R13(π) fixes s (`T3_E08_residual_symmetry_flips_s`,
`T3_E08_klein_orbit_is_s_mod_sign`) — the K₄-orbit of s is {s, −s}, so the chart-honest
E08 modulus remains **s up to sign** (conclusion unchanged; group corrected).

**Generalization to the full C block** — exact (all orders, not merely first order) on
the diagonal-K subfamily, Duhamel form for general K: the lower-left block of e^{φX} is
L(φ) = ∫₀^φ e^{(φ−t)K} C e^{tH} dt, characterized by L′ = KL + C e^{φH}, L(0)=0
(`T3_duhamel_lower_left_ODE`, `T3_duhamel_initial_condition`, `T3_full_map_solves_ODE`;
generic-stratum closed form, resonant sub-strata k_i = h_j stamped). Composition obeys the
**two-sided twisted 1-cocycle (crossed-homomorphism) law over the concatenation groupoid**:

    L(γ₂∘γ₁) = Q(γ₂) L(γ₁) + L(γ₂) ρ(γ₁),   Q = e^{φK},  ρ = e^{φH}
    (`T3_two_sided_twisted_cocycle_law`)

**J07-typed requirements (stated, NOT filled in):** a global assignment requires, on every
chart overlap, transition data (φ-anchor, member) satisfying this twisted law tensorially
(J07); loop consistency requires the cocycle holonomy around every loop to be trivial or
classified (J11). Pointwise, a consistent assignment exists trivially (identity cocycle);
whether a global one exists is exactly the open J07/J11 obligation — no answer is claimed.

## T4 — the diagonal (a,d)-plane and the honest L2 modulus

Subfamily b=k10=0, C=0: X = diag(−1, +1, a, d). Adapted coordinates
**λ := (a+d)/2** (isotropic/trace modulus) and **k_mod := (d−a)/2**
(reciprocal-anisotropy/E07 modulus).

- The E07 seat (a,d)=(−k,+k) is the line **λ=0**, which IS the det-one line a+d=0
  (`T4_E07_axis_is_traceless_line`). The isotropic seat (a,d)=(λ,λ) is the line k_mod=0.
  The two axes intersect only at the spectator origin
  (`T4_axes_intersect_only_at_spectator`).
- **The MAP's seat equation "λ (= E07's k)" is corrected: FALSE at matrix level.** E07's k
  and the joint-audit λ are orthogonal coordinates of the plane, equal only at the E06
  point. Any argument transferring a λ result to the E07 family (or vice versa) crosses
  strata.

**Banked pins mapped to loci** (each CONDITIONAL on its cited supplied structure):

| Supplied structure (cite) | Forced locus in (λ, k_mod) |
|---|---|
| det-one / E03 registration (07-25) | λ=0, k_mod free — the whole E07 axis (`T4_vol4_blind_locus_is_traceless_line`) |
| screen SO(2) holonomy alone (banked gate 07-27; full-class solve here) | k_mod=0, λ free — exactly the isotropic axis; on the full class also C=0, k10=0 (`T4_screen_rotation_forces_isotropic_axis`, `T4_screen_rotation_full_class_forces_isotropic_diag`) |
| SO(3) holonomy (07-27 §4) | (λ,k_mod) = (+1, 0) (`T4_SO3_forces_plus_one_point`) |
| SO⁺(1,2) holonomy (07-27 §4) | (λ,k_mod) = (−1, 0) (`T4_SO12_forces_minus_one_point`) |
| banked swap F (07-27 §4; F not Lorentz — `T4_banked_swap_not_lorentz`) | (0,0) on the plane; on the full class K=0 with the two mixing freedoms (c00,c10)=(−c01,−c11) (`T4_banked_swap_forces_origin_on_plane`, `T4_banked_swap_full_class_two_mixing_freedoms`) |
| base boost L01 | empty for every (a,d) (`T4_base_boost_centralizer_empty`) |

Centralizer dimensions of X_λ in so(1,3): generic λ: 1; λ=±1: 3; λ=0: 1
(`T4_centralizer_dims_generic_pm1_zero`) — matches the banked C3 statement. Cross-branch
splices remain forbidden (banked: ±1 belong to different supplied global structures).

**Volume-form behavior, DERIVED from the coframe (per the T4 amendment — the old
"1+2λ=0 volume-blind locus" was unsourced and is NOT cited):**

- **Full 4D coframe volume** θ⁰∧θ¹∧θ²∧θ³ scales by det M(φ) = e^{(a+d)φ}
  (`T4_vol4_scaling`; full class: e^{(k00+k11)φ}). Volume-blind locus = **{a+d=0} = the
  E07/det-one axis**; on the isotropic axis: only λ=0
  (`T4_vol4_blind_locus_is_traceless_line`, `T4_vol4_blind_isotropic_point_lam0`).
- **Spatial-triad volume** (slots 1,2,3 = ruler + screen) scales by e^{(1+a+d)φ}.
  Blind locus = **{1+a+d=0}**, i.e. the line λ=−1/2; on the isotropic axis this is
  **1+2λ=0 ⇔ λ=−1/2** (`T4_triad_blind_locus_line`,
  `T4_triad_blind_isotropic_point_is_lam_minus_half`). **This is the honest source of the
  previously unsourced "1+2λ=0": it is a spatial-triad statement, not a 4D one**, and it
  never meets the E07 axis (on λ=0 the triad factor is e^{φ} ≠ const). Full class: the
  pure-triad coefficient scales as e^{(1+tr K)φ}; with C≠0 the transported triad acquires
  θ⁰ components, so strict triad blindness additionally needs the C-minors to vanish
  (scope-stamped).
- **Joint-audit R×S³ witness** (07-28 §5): rebuilt exactly; det E = c_E R³ e^{2λφ},
  matching the banked det E = R³e^{2λφ} at the c_E=1 unit calibration
  (`T4_witness_det_matches_banked`); 4D-blind ⇔ λ=0 (`T4_witness_4D_blind_iff_lam0`).
  The slice-induced 3-volume on t=const (basis σ₃,σ₁,σ₂):
  det g₃ = (R²e^{2φ} − a²e^{−2φ})·R⁴e^{4λφ}; φ-blind **iff λ=−1/2 AND the twist shift
  a=0**; with a≠0 no λ is volume-blind
  (`T4_witness_slice_blind_iff_lam_minus_half_and_zero_shift`,
  `T4_witness_slice_monomial_representation_exact`).

**The honest L2 modulus, exactly:** on the diagonal subfamily the transverse modulus is
the **pair (λ, k_mod)** — two scalars, not one; the full class adds k10 and the four
mixing parameters C, **read modulo the exact Klein-four residual chart quotient**
(k10 mod sign; C mod the signed-flip action; λ and k_mod are K₄-invariant — A1).
All pins are conditional on their cited supplied structures; the
volume-blind loci are derived facts about which supplied volume functional is held fixed
(4D ⇒ λ=0 axis; ruler+screen triad ⇒ λ=−1/2 line), not selections. No active premise
selects any point of the plane (07-26 rank zero; F-A respected).

## T5 — stratum × supplied-reduction forcing table

Every column is a SUPPLIED structure with its banked citation; the active 18-family set,
the seal, and strong CSN are listed separately as UNCONSTRAINED/INACTIVE columns and are
never used as forcing (F-A guard check). Cells: solution dimension of stratum ∩ supplied
condition inside the 7-parameter class; EMPTY = conditionally incompatible (forcing
identity given). Computed exactly (`T5_forcing_table_key_cells` and neighbors):

| Stratum (dim) | det-one (07-25) | transv-inv (07-25) | no-mixing (07-25) | SO(3) (07-27 §4) | SO⁺(1,2) (07-27 §4) | swap F (07-27 §4) | screen SO(2) (07-27 gate; solve here) |
|---|---|---|---|---|---|---|---|
| E02 (7) | 6 | 4 | 3 | 0 → X₊₁ | 0 → X₋₁ | 2 | 1 (isotropic axis) |
| E03 (6) | 6 | 4 | 2 | EMPTY (tr K forced +2 vs 0) | EMPTY (tr K forced −2 vs 0) | 2 | 0 (spectator) |
| E04 (4) | 4 | 4 | 0 | EMPTY (K forced I vs 0) | EMPTY (K forced −I vs 0) | 2 | 0 |
| E05 (3) | 2 | 0 | 3 | 0 → X₊₁ | 0 → X₋₁ | 0 (spectator) | 1 |
| E06 (0) | 0 | 0 | 0 | EMPTY (K forced ±I vs 0) | EMPTY | 0 | 0 |
| E07 (1) | 1 | 0 | 1 | EMPTY (tr K ±2 vs 0) | EMPTY | 0 (k_mod forced 0) | 0 (k_mod forced 0) |
| E08 (1) | 1 | 1 | 0 | EMPTY (C forced 0 & K forced I) | EMPTY | 0 (s forced 0) | 0 (s forced 0) |

Forced members verified: SO(3) ⇒ X₊₁ = diag(−1,1,1,1); SO⁺(1,2) ⇒ X₋₁ = diag(−1,1,−1,−1)
(`T5_SO3_forced_member_is_X_plus1`, `T5_SO12_forced_member_is_X_minus1`). E06 uniqueness:
only in the JOINT stronger class (transverse-invariance + no-mixing, joint rank 7,
`T5_joint_spectator_rank_7`; banked 07-26) — never promoted to unique-in-class (F-D).
Every EMPTY/forcing cell is conditional on its supplied column; **no unconditional
elimination exists in the table** (F-A, F-E respected). No new gates were invented; the
screen-SO(2) column is the banked 07-27 gate evaluated on the full class (assembly).

## T6 — the L1/L2 re-tag (Stage-1 evidence only)

- **L1 (extension stratum): MODULUS-CARRIED.** No layer C1–C4 unconditionally eliminates
  any stratum. C1 refines the ledger with a covariance typing: **E03 is DERIVED-covariant**
  (its defining condition tr X=0 is fully frame-invariant); **E04/E05/E06 are
  CONDITIONAL on the supplied base/screen split for their very definition**
  (split-relative; exact orbit witnesses); E06's equivariant content is the conjugacy
  class of H4. C2: all strata composition-closed (no elimination); the per-member vs
  cross-member distinction is a derived structure, not a filter. C3: all reductions
  CONDITIONAL(cite 07-27 §4). C4: violations only-if-imposed (J06/J10/J13). The full
  7-parameter family survives (moduli read modulo the exact K₄ residual chart
  quotient — A1). Outcome class **O2/O3 mixed**.
- **L2 (transverse modulus): MODULUS-CARRIED, and RESOLVED IN FORM.** Not one scalar:
  the pair (λ, k_mod) on the diagonal subfamily (+ k10 and C in the full class). The
  MAP's "λ (= E07's k)" identification is corrected (orthogonal axes). Pins:
  CONDITIONAL(07-25 E03) λ=0 with k_mod free; CONDITIONAL(07-27 §4) (±1,0) and the
  swap (0,0)+mixing family; DERIVED(this package) volume-blind loci: 4D ⇔ λ=0;
  ruler+screen triad ⇔ λ=−1/2 (the honest, convention-stamped source of "1+2λ=0");
  witness slice ⇔ λ=−1/2 AND zero twist shift. Full class adds k10 and C as carried
  moduli, **read modulo the exact K₄ residual chart quotient** (k10 mod sign; C mod
  the signed-flip action — A1).

**C4 typing summary** (per-stratum detail in `routeB_stage1_results.json` → C4_typing):
J05 satisfiable for all strata; J06 violated-only-if-imposed for E03/E04/E05/E06
(imposing them without derivation is J06's named false pass — "spectator screen isotropy
or trace zero assumed"); J07 open for all strata (T3 states the required transition-data
type); J10 satisfied by E03 and by the equivariant reading of the split strata,
violated-only-if a fixed plane is imposed; J11 conditional (T2 drift + loop holonomy);
J13 violated-only-if-imposed (E05/E06 impositions erase the E07/E08 discriminators);
J15 satisfied by this ledger.

## Falsifier record

F-A: not fired (no elimination cites the rank-zero active set; structural guard check).
F-B: not fired (no pointwise metric-only selection of a non-scalar generator claimed; no
unconditional spectator uniqueness — E06 stated unique only in the joint stronger class).
F-C: not fired (100/100 checks pass, exit 0). F-D: **one slip found by the blind
verifier and AMENDED (A1)**: the original text asserted the finite residual "IS Z₂"
where only "⊇ Z₂" had been derived — an is/⊇ quantifier slip; the residual is now
proven EXACTLY the Klein four-group (exhaustiveness checks `T1_residual_*`) and every
statement reading a modulus through the quotient is corrected (see
`CORRECTION_LAYER.md`). All other uniqueness statements verified scope-clean by the
verifier. F-E: not fired (all eliminations recorded by
forcing identity; covariance typing is provenance, not merit).

## Scope stamps (travel with the result)

1. det e^{φX} = e^{φ tr X} rides exact triangular lemmas + the standard series-limit
   argument; instantiated exactly on the diagonal subfamily, E08, and the E04 closed form.
2. T3 general-K law proven exactly on the diagonal-K subfamily (generic stratum
   k_i ≠ h_j; resonant sub-strata stamped); general-K = same Duhamel/ODE characterization.
3. Full-class spatial-triad volume: pure-triad coefficient e^{(1+tr K)φ}; C≠0 adds θ⁰
   contamination — strict triad blindness needs tr K=−1 AND vanishing C-minors.
4. Generic-λ centralizer dimension computed over the rational-function field in λ.
5. All statements are pointwise, one-parameter, registered-chart, off-shell; nothing
   global, dynamical, or physical is selected (pre-committed ceiling, contract §5).
