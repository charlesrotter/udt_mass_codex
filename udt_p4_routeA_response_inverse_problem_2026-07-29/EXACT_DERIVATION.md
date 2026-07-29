# P4 Route A Stage 1 — exact derivation record (TA6 + TA2/TA4 identities)

Date: 2026-07-29. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
derivation). Script: `derive_routeA_stage1.py` — **40/40 zero-residual exact-SymPy
checks, exit 0** (pre-amendment 34/34; +3 `A6_*` and +3 `B5_*` amendment checks),
deterministic (no floats/randomness/network; JSON byte-identical across reruns), single
CPU process, < 1 s (FULL SCOPE, not throughput-limited). Outputs:
`routeA_stage1_results.json`, `DERIVATION_STDOUT.txt`. Every check named in `monospace`
below is one of the 40.

**AMENDED 2026-07-29 per `VERIFIER_REPORT.md` (verdict PASS-WITH-REQUIRED-AMENDMENTS):**
A1 — the F-RA1 K₄ clause is restated as character-matched RELATIVE invariance (§1); A3 —
the F-RA2 channel class is narrowed to the exactly-proven class with the slot theorem
(§2). Both were F-A6-class quantifier slips, caught by the verifier with exact
counterexamples; the forcing SURVIVES in corrected form in both cases. Amendment record:
`CORRECTION_LAYER.md`.

**Standing stamps (travel with every statement):** registered positive triangular
chart; conventions copied from the banked Route B registration (η = diag(−1,1,1,1);
L{ab}[a,b]=1, L{ab}[b,a]=−η_aa/η_bb; X = [[H,0],[C,K]], H=diag(−1,1)); all pointwise
statements are one-parameter, off-shell, registered-chart; NOTHING global, dynamical,
or physical is selected; NO candidate response exists or is constructed (F-A1). Where a
banked fact is used, it is RECOMPUTED as a consistency check and cited — never
re-derived as new, never adopted beyond its banked scope (F-A4).

---

## 0. Premises (chose or derived — stamped)

| Premise | Tag |
|---|---|
| Registered chart + generator conventions | THEORY (banked 07-25 E02 registration; Route B script lines 40–48 convention copy) |
| 7-param E02 footing; two-scalar seat (λ, k_mod); EXACT K₄ residual | DERIVED input (Route B bank da301b1; recomputed here as consistency: `A2_*`, `A3_*`, `B1_*`) |
| Fifteen requirements + J01–J15 as the constraint set | THEORY (MAP §2; JOINT_OPERATION_OBLIGATIONS.tsv verbatim) |
| Response one-form as object type; L6 both ways | THEORY (closure-audit localization; F-A3 discipline) |
| Toy witness domain for the C-block (2 directions, polynomial) | FREE (Category-A: an exact finite-dimensional witness of a structural inequivalence; carries no physics) |
| SymPy exact, CPU, single process | Category-A conditioning |

## 1. TA6(a) — what J10 + scalar-only centralizer + K₄ force on the covariance type

**Computation.**
- The commutant of so(1,3) in gl(4) is exactly the scalars: the 96×16 linear system
  [B, L_i] = 0 over the six generators has rank 15 (`A1_so13_commutant_rank_15`) and
  nullspace = span{I} (`A1_so13_commutant_solution_is_scalar`) — recomputing the banked
  scalar-only-centralizer fact (07-26/07-28).
- The K₄ residual is recomputed exactly: all four elements proper orthochronous
  (`A2_klein_elements_proper_orthochronous`), closed (`A2_klein_closure`), involutive
  (`A2_klein_involutions`), R12(π)·R13(π)=R23(π) (`A2_klein_R12_R13_product_is_R23`);
  its action on the class: (K,C)↦(K,−C) under R23(π) (`A3_R23_action_C_negated_K_fixed`),
  k10↦−k10 with (c00,c11)-flip under R12(π) (`A3_R12_action_flips_k10_c00_c11`), with
  (c01,c10)-flip under R13(π) (`A3_R13_action_flips_k10_c01_c10`); λ and k_mod invariant
  (`A3_lambda_kmod_K4_invariant`) — all matching the Route B bank (F-A4 clean).
- Invariance certification: the monomials k10², {c00², c11², c00c11}, {c01², c10²,
  c01c10}, and the four mixed cubics k10·{c00,c11}·{c01,c10} are K₄-invariant
  (`A4_invariant_monomials_certified`); bare k10, bare C entries, k10·c-linear, and
  cross-class quadratics are each FLIPPED by at least one K₄ element
  (`A4_noninvariant_monomials_certified`).
- No Lorentz-invariant member exists in the class: any generator invariant under all
  of SO⁺(1,3) is scalar c·I (from A1), but the founded base block H = diag(−1,1)
  forces c = −1 and c = +1 simultaneously — inconsistent
  (`A5_no_lorentz_invariant_generator_in_class`).
- **[A1 amendment] Character-matched relative invariance** (the corrected K₄ clause):
  the verifier's counterexample ω = k10·dk10 = ½d(k10²) — an EXACT, K₄-INVARIANT
  one-form whose R_k10 component is bare-k10-linear (component and dk10 flip TOGETHER
  under R12/R13) — is embodied as a zero-residual check: ω is K₄-invariant as a
  one-form while its component is not verbatim-invariant, and ω is exact
  (`A6_counterexample_omega_k10_dk10_invariant_component_not_verbatim`). The corrected
  rule holds on a generic component set in every character class: component character ×
  direction character = trivial ⟹ K₄-invariant one-form
  (`A6_character_matching_rule_generic_component_set`); the actual failure mode is
  character MISMATCH, not bare-linearity
  (`A6_character_mismatch_breaks_invariance_contrast`). Characters under (R12, R13):
  trivial for φ/λ/k_mod-type directions; χ_a = (−,−) for k10; χ_b = (−,+) for c00, c11;
  χ_c = (+,−) for c01, c10.
- **[Verifier positive finding, recorded with A1]** The 11 listed generators (k10²; the
  six within-character-class C quadratics; the four mixed cubics) DO generate the FULL
  invariant ring of polynomial functions of (k10, C) — proven by the verifier two ways:
  (a) the character/parity argument (invariance ⇔ e+p+q even AND e+r+s even; e≥2 ⇒
  divisible by k10²; e=1 ⇒ divisible by a mixed cubic; e=0 ⇒ product of within-class
  quadratics), and (b) exhaustive factorization of all 127 invariant monomials of
  degree ≤ 6 through the 11. Preserved in `VERIFIER_INDEPENDENT_CHECK.py`
  (`V2_direction2_generation_to_degree6`, `V2_direction2_parity_structure`).
- Transport: the physical tangent T = Xᵀη + ηX = [[2I₂, Cᵀ],[C, K+Kᵀ]]
  (`T2_tangent_block_form`) transports as a bilinear form, T ↦ Λ⁻ᵀTΛ⁻¹, verified on a
  generic 16-parameter X under the exact boost exp(tL01) and all nontrivial K₄
  elements (`T2_tangent_transport_bilinear_boost`, `_klein`; `T2_boost_is_lorentz`).

> **FORCED F-RA1 (A1-AMENDED) [SCOPE: POINTWISE — registered chart, one-parameter,
> off-shell; global assignment J07/J11 untouched].** The response CANNOT be a
> Lorentz-invariant object anchored on a fixed preferred generator/plane: no such
> member exists in the class. Its covariance type is forced to be an EQUIVARIANT
> FAMILY whose components transform contragradiently to T ↦ Λ⁻ᵀTΛ⁻¹; and on the
> registered chart the K₄ quotient forces CHARACTER-MATCHED RELATIVE INVARIANCE per
> component: a component R_v must transform with the K₄ character of its paired
> direction dv (component character × direction character = trivial, `A6_*`). Verbatim
> factoring through the exact K₄ invariants (a verifier-proven GENERATING set: k10²,
> the C character-class quadratics, the four mixed cubics) holds exactly for components
> along K₄-invariant directions (δφ, base data, δλ, δk_mod, boundary data); R_k10 must
> be χ_a-relative (e.g. k10·invariant, or c_b·c_c·invariant), R_C components
> χ_b/χ_c-relative. Character-MISMATCHED dependence is what is not well defined on the
> quotient domain. Counterexample on record: ω = k10·dk10 = ½d(k10²) is K₄-invariant
> and exact with a bare-k10-linear component.

## 2. TA6(b) — what requirement 4 + J06 force on the screen sector over (λ, k_mod)

**Computation.** On the banked seat a = λ−k_mod, d = λ+k_mod
(`B1_seat_reconstruction`):
- tr X_seat = 2λ exactly, with ∂(tr)/∂k_mod ≡ 0 (`B1_trace_channel_blind_to_kmod`).
- The screen block decomposes uniquely as K_seat = λ·I₂ + k_mod·diag(−1,1); the
  anisotropic (trace-free) slot IS the k_mod direction
  (`B2_screen_trace_tracefree_decomposition`).
- ANY functional F(tr) has identically zero pairing with ∂/∂k_mod
  (`B3_generic_trace_functional_zero_kmod_pairing`); the volume/density channel
  det e^{φX_seat} = e^{2λφ} is likewise k_mod-blind
  (`B3_volume_density_channel_blind_to_kmod` — matching banked `T4_vol4_scaling`).
- Contrast (characterize, not filter): det K_seat = λ²−k_mod² DOES pair with k_mod
  generically (`B3_det_screen_channel_pairs_kmod_contrast`) — the blindness is
  channel-specific, not universal; and the two seat axes meet only at the spectator
  (`B4_axes_intersect_only_at_spectator` — the MAP's "k = λ" REFUTATION stands).
- **[A3 amendment] The channel class narrowed to the exactly-proven theorem.** The
  verifier's counter-channel tr(X²) = 2 + 2λ² + 2k_mod² is trace-BUILT yet pairs with
  k_mod (∂/∂k_mod = 4k_mod ≠ 0) — embodied as
  `B5_counter_channel_trX2_pairs_with_kmod`. The k_mod-blind class that is exactly
  proven: functionals of tr X (first trace) and of det e^{φX}. The surviving EXACT slot
  theorem: a screen pairing kernel with zero trace-free part has identically zero
  k_mod-pairing, ⟨r_tr·I₂, diag(−1,1)⟩ ≡ 0
  (`B5_slot_theorem_pure_trace_kernel_zero_kmod_pairing`); and d(tr X²)'s kernel
  2K = 2λI₂ + 2k_mod·diag(−1,1) pairs with k_mod PRECISELY through its trace-free part
  (the pure-trace part contributes 0 — as the verifier proved it;
  `B5_trX2_kmod_pairing_routes_through_tracefree_slot`).

> **FORCED F-RA2 (A3-AMENDED) [SCOPE: POINTWISE on the seat; the whole-solution/global
> selection of moduli VALUES is untouched — 07-26 rank zero respected].** Any response
> whose screen sector factors through functionals of tr X (first trace) and of the
> volume density det e^{φX} has identically zero pairing with the k_mod direction —
> NOT "every trace/volume/density channel" (counter-channel on record: tr(X²) pairs,
> ∂/∂k_mod = 4k_mod). The exact slot theorem holds: a screen pairing kernel with zero
> trace-free part has identically zero k_mod-pairing (⟨r_tr·I₂, diag(−1,1)⟩ ≡ 0), and
> any channel that DOES pair with k_mod — d(tr X²) included — does so precisely through
> its trace-free part. Therefore J06's "determined" branch for k_mod is reachable ONLY
> by a response carrying the trace-free screen slot k_mod·diag(−1,1) (and/or the k10/C
> mixing slots) — the trace-free slot is still FORCED for k_mod sensitivity. A
> candidate lacking the slot can pass J06 only via the explicit-residual-modulus
> branch; silent omission = J06's named false pass. This forces SLOT PRESENCE in the
> general object — no candidate value is demanded (F-A1 respected).

## 3. TA6(c) — what requirement 12 + J14 force structurally

**Computation (exact finite-dimensional witness).** F(x,y) = x² + y + y² on a
two-direction domain with the stratum {y=0}:
- restrict-then-vary yields the critical point x = 0
  (`C1_restricted_stationarity_witness`);
- the FULL response at that point is (0, 1): normal residual exactly 1, not 0
  (`C1_full_response_normal_residual_nonzero`);
- the full zero set is {(0, −1/2)}, disjoint from the stratum: the system
  {F_x = 0, F_y = 0, y = 0} is exactly inconsistent
  (`C2_full_zero_set_disjoint_from_restricted_critical`).

> **FORCED F-RA3 [SCOPE: STRUCTURAL/DEFINITIONAL — pointwise-decidable on the object's
> definition; instantiated by an exact witness].** The response must be DEFINED on the
> full typed domain with components along every census direction (fields; moduli under
> both fork options; boundary data); every stratum restriction is a pullback of the
> full object performed AFTER definition (vary-then-restrict). Restrict-then-vary is
> inequivalent — witnessed exactly, and banked as the EH-RED scar (requirement 12).
> J14's off-shell/on-shell separation is thereby built into the object's TYPE: the
> on-shell set is a derived subset of the off-shell domain, never an input.

## 4. TA6(d) — what the additive-depth law (G01) forces pointwise

**Computation.**
- Per-member additivity: e^{φ₂X}e^{φ₁X} = e^{(φ₁+φ₂)X} on the seat
  (`D1_seat_same_member_additivity`) and for the E04 closed form M(φ;C) =
  [[e^{φH},0],[CH(e^{φH}−I),I]] (ODE, initial condition, additivity —
  `D1_E04_closed_form_ODE_init_additive`, recomputing the banked T2 closed form).
- The every-scalar-f witness: δ_f(p,q) = f(q)−f(p) satisfies reversal + three-point
  composition for EVERY f (`D2_every_scalar_f_depth_composition` — recomputing the
  joint audit §1): additivity has zero selector rank on pointwise functional form.
- Shift structure: e^{(φ+s)X} = e^{sX}e^{φX} (`D3_shift_is_left_group_translation`);
  on the founded stationary readout Q = c_E e^{−φ} the shift is absorbed into the
  anchor, c_E ↦ c_E e^{−s} (`D3_anchor_absorption` — joint audit §3).

> **FORCED F-RA4 [SCOPE: POINTWISE; the realized-profile/whole-solution content of G01
> untouched].** G01 forces ONLY shift-equivariance of the response's φ-dependence (a
> covariance: constant depth shifts act by left group translation, absorbable into the
> anchor c_E — so no component may depend on an absolute φ zero-point). It forces
> NOTHING further about the pointwise functional form — **reported as-is (near-null;
> the OA2-flavored item of this stage).**

## 5. TA2/TA4 identities banked by this stage

1. The physical tangent block form T = [[2I₂, Cᵀ],[C, K+Kᵀ]] and its bilinear-form
   transport law (`T2_*`) — the object a response pairs with (POSED_INVERSE_PROBLEM
   §1.4).
2. The seat decomposition K_seat = λI₂ + k_mod·diag(−1,1) with the narrowed
   channel-blindness theorem (tr X and det e^{φX} functionals; `B1_*`–`B3_*`) and the
   exact slot theorem ⟨r_tr·I₂, diag(−1,1)⟩ ≡ 0 (`B5_*`; requirement 4's exact form,
   A3-amended).
3. The K₄ invariant/non-invariant monomial certification (`A4_*`) plus the
   character-matched relative-invariance rule (`A6_*`; A1-amended) — the
   quotient-honesty condition on components (gate 4, step 2): character match with the
   paired direction, verbatim invariance on K₄-invariant directions.
4. The restrict-then-vary inequivalence witness (`C1_*`/`C2_*`) — requirement 12/J14
   as a property of the object's type (gate-independent).

## 6. Outcome and falsifier record (derivation-side; verifier pass COMPLETE — see below)

**Outcome class: OA1/OA2 MIXED.** Nontrivial candidate-free forced structure exists
(F-RA1, F-RA2, F-RA3 — OA1 items); the G01 item is near-null pointwise (F-RA4 — OA2
item); most requirement content classifies as whole-solution/global-completion
(POSED_INVERSE_PROBLEM §3 tallies), so the typed problem statement is itself the main
deliverable — consistent with OA2's honest reading. **No requirement clash surfaced:
OA3 not reached** (clash scan: POSED_INVERSE_PROBLEM §3.2).

- F-A1 (candidate smuggle): none — no response constructed; EH/Bach/CM0-C appear only
  as cited jet-order examples / recorded exclusion.
- F-A2 (census freeze): none — every fork typed both ways in the census; the script
  fixes no modulus value.
- F-A3 (L6 imposition): none — Helmholtz appears only as gate-3 testable property.
- F-A4 (bank contradiction): none — every recomputed banked fact matched exactly
  (K₄ actions, seat, tangent block, closed forms, volume scaling).
- F-A5 (symbolic failure): none — 40/40, exit 0 (pre-amendment 34/34).
- F-A6 (scope slip): every forced statement carries its scope stamp inline (above) and
  in `routeA_stage1_results.json` → forced_statements[].scope. **Verifier record: TWO
  F-A6-class universal-quantifier slips were found by the blind verifier** (the F-RA1
  K₄ component clause; the F-RA2 channel clause) — both amended above (A1/A3) with the
  verifier's exact counterexamples embodied as zero-residual checks (`A6_*`, `B5_*`).
  All other forced statements survived independent re-derivation unchanged
  (`VERIFIER_REPORT.md`, 31/31 independent checks).
