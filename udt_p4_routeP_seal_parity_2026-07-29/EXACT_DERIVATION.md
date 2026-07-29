# P4 Route P — the seal-parity derivation (TP1–TP4), exact record

Date: 2026-07-29. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
derivation). Script: `derive_routeP_seal_parity.py` — **41/41 checks, exit 0 = 33
SUBSTANTIVE zero-residual exact-SymPy checks + 8 guards** (guards = citation/assembly
bookkeeping, labeled `[guard]`; the 34 pre-amendment checks all surviving, plus the A1
distinction check and 6 adopted verifier legs, credited), deterministic (no floats, no
randomness, no numeric solvers, no GPU; rerun byte-identical ×3), single CPU process,
< 2 s wall. FULL DECLARED SCOPE — no scope-ladder reduction taken. Outputs:
`routeP_results.json`, `DERIVATION_STDOUT.txt`, `DRESSING_CLASSIFICATION_LEDGER.tsv`.
Every check named in `monospace` below is one of the 41. **Outcome class: OP3 (mixed
per-sector).**

**AMENDMENT BANNER (2026-07-29, post-verifier; `VERIFIER_REPORT.md` verdict
PASS-WITH-REQUIRED-AMENDMENTS; record = `CORRECTION_LAYER.md`).** A1 (required,
load-bearing textual): the TP4 anchored-pairing landing prose mis-cited the banked
no-λ-row criterion — it is **a_F′ = 0** (the P2 pairing's identically-zero anchor-weight
λ-DERIVATIVE), NOT the weight VALUE a_F = 0; under P1-4D at the λ = 0 landing,
a_F′ = 2 ≠ 0, so the λ-row does NOT vanish by banked pairing-relativity there and the
a_F = 0 background's status is UNDERIVED (the quadratic atlas and the I_p certificate
presuppose a_F ≠ 0). The corrected statement (below, TP4) is: certificate-PREMISE
failure ⇒ massive-locus nonemptiness UNCERTIFIED at the landing — never "divergence
ABSENT". The drift direction was CUTTING-side inflation (anti-massive) — memorialized
in the falsifier record. A2: the dropped prime in the TP4 quote restored. A3: the
"catch-proofs verified" sentence substantiated by ADOPTING the verifier's mutation set
as in-package checks (credited). A4: check-22 sign slip fixed (−k10); family parameter
count per-branch; η-readout stamp on the ledger's Lorentz row; the verifier's completed
K₄-honesty leg adopted. No pre-amendment computed claim changed; OP3 stands.

**Binding boundary (carried on every statement):** the steering hazard is INVERTED here
and both directions were audited (F-P1): the cutting legs carry their premise ladder
visibly (the load-bearing premise P2 is TYPED, not derived, and an escape witness
against it is computed in-package); the harmless legs carry the exact missing datum.
No dressing is adopted (F-P2: the V5 swap is adjudicated INSIDE the classification and
found non-forced). No census branch is adopted (F-P4); both are carried. No banked
contradiction found (F-P5; the banked swap locus and the 07-20 family are RECOVERED as
consistency checks). No symbolic failure (F-P6: 41/41, exit 0).

---

## TP1 — the seal record, exactly (reading-and-tagging; every element tagged)

| Element | What the bank fixes | Tag |
|---|---|---|
| Mirror on coordinates | σ_φ: (φ→−φ, r→radial reflection); fixed surface φ=0=r_s (spatial crease); the seal is a FOLD (seal ≠ edge; Z₂ quotient), theorem-grade | **CANON** (C-2026-06-10-2 "mirrored across φ→−φ"; C-2026-07-04-1 sector split) |
| Mirror on the depth field | ε_φ = −1. **Provenance, re-read exactly: not derived from deeper structure — it is the canon's DEFINING wording of the finite-cell mirror** ("mirrored across φ→−φ" is what the fold IS). C-2026-07-04-1 (node05, blind-verified) DERIVES which involution governs which sector (σ_φ = static; t→−t = time-on) and the BC consequence (φ ODD ⇒ Dirichlet φ(r_s)=0, φ′ free ⇒ flux seal q=Zρ_s²φ′) from the native boundary term + the Weierstrass–Erdmann/Z₂ dichotomy | **CANON** (definitional) + **DERIVED** (sector localization, BC consequence — banked) |
| Mirror on time-on sector | t→−t governs time-on/off-diagonal; ω-question OPEN (not settled by canon) | **CANON** (split) / **OPEN** (spin) |
| Other field parities | f/bh parities at the wall | **SUPPLIED** (tagged so in Stage-3/Slice-2, verbatim) |
| Mirror on the FRAME/coframe | **Not fixed by canon.** The banked 07-20 adjudication (`complete_coframe_seal_involution_2026-07-20`) closed this as **MULTIPLE_COMPLETIONS**: base-block real involution family F_b = [[0,b],[1/b,0]] (b≠0); the raw clock/ruler swap is an η-ANTI-isometry in the diagonal readout (no positive-conformal-η solution); angular extension NON-UNIQUE (+I / −I / axis-reflection continuum; "selector: not supplied"); time-on open. Smallest missing object (banked): "a source-authorized physical quadratic readout/slot map plus a complete normal-angular-time-on coframe lift of the seal involution" | **SUPPLIED** (beyond the derived family constraints) — banked adjudication |
| Mirror on the MODULI | Previously wholly SUPPLIED: −X not in-class (H-block obstruction, banked S3, recomputed `S0_minus_X_H_block_obstruction`); V5 swap candidate = candidate only (recomputed `S0_swap_F_candidate_action`, `S0_swap_F_eta_behavior`) | **was SUPPLIED → this package's target** |

## TP2 — the dressing classification (the core derivation)

**Setup (premise ladder, chose-or-derived):**

- **P0 (CANON):** the fold is a Z₂ identification and flips depth, φ→−φ.
- **P1 (DERIVED — L0):** on the registered anchored one-parameter presentation
  (E(0)=I, constant generator), a constant invertible linear frame dressing J
  transcribes the mirror on generators as **X ↦ −J X J⁻¹**: verified zero-residual on
  the exact E04 exponential with fully generic block J (`L0_E04_closed_form_recompute`,
  `L0_dressed_family_solves_dressed_ODE`; the algebraic cancellation adj(J)·J = det(J)·I
  proven for fully generic 16-symbol J, `L0_adjugate_cancellation_generic_J`; Picard
  uniqueness named Category-A). The re-anchoring (right J⁻¹) is forced by E(0)=I.
  Linearity + φ-independence of J = the registered presentation's own footing
  (φ-dependent dressings would leave the constant-generator presentation — TYPED out of
  scope, not classified).
- **P2 (TYPED, NOT derived — the load-bearing premise):** chart-representability —
  the mirror acts ON the registered class (member-to-member). The alternative (the
  mirror image lives in another chart) requires J07-type cross-chart transition data,
  banked-open; on that alternative ε_m is UNDEFINED on the banked footing. P2 is the
  premise a field-branch/harmless-outcome advocate would attack; its load-bearing role
  is made checkable by the in-package escape witness (below).

**Classification (Route-B probe/necessity/enumeration method), all zero-residual:**

1. **Q = 0 forced** (upper-right block): the class condition puts J·v in V·J, whose top
   block-row is zero; probing the 7 V-directions forces exactly {j02,j03,j12,j13} = 0
   and nothing else (`TC_VJ_top_rows_zero` [guard], `TC_Q_block_zero_forced`).
2. **S lower-triangular forced**: (S K adj S)[0,1] = t00·t01·(k11−k00) − t01²·k10 ≡ 0
   ⇔ t01 = 0 (`TC_S_lower_triangular_forced`; sufficiency verified).
3. **P anti-diagonal forced**: −P H P⁻¹ = H ⇔ PH + HP = 0 ⇔ P = antidiag(p, q), pq≠0
   (`TC_P_antidiagonal_forced`). **This reproduces, inside the registered class, the
   banked 07-20 base family F_b = [[0,b],[1/b,0]]** — the classification transports the
   coframe-involution record onto the P4 chart rather than contradicting it.
4. **No Lorentz dressing exists** (in the registered diagonal η₂ readout): PᵀηP =
   diag(q², −p²) = η₂ needs q² = −1 — empty over the reals
   (`TC_no_lorentz_dressing_exists`). EVERY compatible dressing is non-Lorentz in that
   readout; the banked "F non-Lorentz" fact is family-general, and consistent with
   07-20's no-positive-conformal-η result. **η-readout caveat travels (A4):** the
   banked 07-20 record notes every F_b is an exact O(1,1) reflection under the
   ADDITIONAL null-coordinate choice of K as metric — the EMPTY verdict is
   readout-scoped.
5. **R (base→screen mixing) unconstrained by class-preservation**; exact block laws
   K̃ = −S K S⁻¹ (R-free) and C̃ = −(RH + SC)P⁻¹ + SKS⁻¹RP⁻¹ (affine: constant offset
   −RHP⁻¹ + a K→C shear) (`TC_R_unconstrained_and_blocks_exact`).
6. **Involution + realness**: commutant of the class = scalars
   (`S0_class_commutant_is_scalars`) ⇒ J² = μI; block form gives μ = pq, S² = pq·I,
   RP + SR = 0; lower-tri realness forces **pq = s00² > 0** (no real J² = −I branch);
   scale gauge normalizes pq = 1 (`TC_involution_and_realness`). S branches: **(a)**
   S = ±I (s10 = 0) or **(b)** S = [[s0,0],[s1,−s0]], s0 = ±1, s1 free. R solves
   RP + SR = 0 on an exactly 2-dimensional space per branch
   (`TC_R_solution_space_dim_2_per_branch`).

**Verdict (`TC_family_assembly` [guard]): the compatible set is a NONEMPTY FAMILY, not
unique and not empty** — J = [[antidiag(p,1/p), 0],[R, S]] with p ≠ 0 free, S in branch
(a)/(b), R in its 2-dim space; continuous parameters PER BRANCH (A4): branch (a) has
3 (p + 2 R; σ = ±1 discrete), branch (b) has 4 (p, s1 + 2 R; s0 = ±1 discrete), modulo
scale. The cutting conditions are exactly: class-preservation, fold composition
(J² scalar), realness.

**V5 adjudication (`TC_V5_adjudicated_inside_family`):** the banked swap F = diag(F₂,I)
IS the family member (p=1, S=+I, R=0); a distinct compatible member (p=2) is exhibited;
**the swap premise is NOT forced** — F-P2 honored. But (TP3) the λ/k_mod parities V5
computed hold for EVERY family member: V5's cutting content was family-uniform, its
member-specific content (k10 odd, C→−C·F₂) was not.

**K₄ honesty (`TP4_K4_composition_honesty` + adopted `ADOPTED_K4_R13_non_involutive`,
verifier-credited):** R23(π)∘J stays in-family (= the σ→−σ member; already counted);
R12(π)∘J AND R13(π)∘J both square to diag(−1,−1,1,1) ≠ scalar — all THREE nontrivial
K₄ elements now checked (the pre-amendment package checked two; the verifier completed
the leg): the residual chart quotient CANNOT flip the k10-parity branch within the
real family. The classification is honest modulo the banked K₄ quotient — complete,
not sampled.

## TP3 — the parity verdict, per moduli sector (full stamps)

Stamps on all rows: registered positive triangular chart (07-25); anchored constant-
generator presentation; premise ladder P0/P1/P2 as marked; both census branches
carried; moduli read modulo the banked K₄ quotient.

| Sector | Verdict | Exact basis |
|---|---|---|
| **λ** | **DERIVED: ε_λ = −1** — needs only P0+P1; **dressing-INDEPENDENT** | tr(−JXJ⁻¹) = −tr X for ANY invertible linear J (16-symbol identity, `TP3_trace_similarity_generic_J`); λ = tr X/2. No linear dressing whatsoever can give ε_λ = +1; the only escapes are abandoning the linear-dressing transcription itself (= leaving the registered presentation). |
| **k_mod** | **DERIVED under P2: ε_kmod = −1**, family-uniform; **CONSTRAINED without P2** | diag(SKS⁻¹) = diag K for lower-tri S ⇒ K̃-diag = −K-diag for every family member (`TP3_lambda_kmod_odd_family_uniform`). **Escape witness (F-P1 duty, computed):** J_out = diag(F₂,F₂) satisfies J_out X J_out⁻¹ = −X at X = diag(−1,1,−k,k) — a fold-invariant member with k_mod ≠ 0 exists IF the dressing may leave the chart (F₂ on the screen breaks K-triangularity) (`TP3_chart_escape_witness_kmod`). P2 is exactly what the k_mod-kill rides on. |
| **k10** | **CONSTRAINED** (branch-split) | branch (a): k̃10 = −k10 (ODD); branch (b): k̃10 = +k10 + 2(s1/s0)k_mod (EVEN + shear; shear vanishes on the fixed locus) (`TP3_k10_branch_split`). **Missing datum, named exactly:** the screen/angular completion of the seal involution — the banked 07-20 non-uniqueness (angular +I/−I vs axis-reflection; "selector: not supplied"). |
| **C** | **CONSTRAINED** (signature forced; basis supplied) | The C-action C ↦ −SCP has charpoly (x−1)²(x+1)² in EVERY branch at symbolic p, s1: **exactly 2 ODD + 2 EVEN combinations, family-uniform** (`TP3_C_signature_2odd_2even_forced`). WHICH combinations: at S=+I the odd pair is μ_i+ = p·c_i0 + c_i1 — explicitly p-dependent, σ-flippable, R-shiftable (`TP3_C_basis_p_dependent`, `TP3_R_affine_offset_and_triangularity`). **Missing datum:** the completion calibration (p, S-branch, R) + the quadratic readout — the banked 07-20 "smallest missing object". |

**ε_φ = −1 relation:** the moduli parities are NOT new instances of ε_φ; they are the
in-chart representation consequences of the SAME canon fold, obtained through L0 + the
classification. The bank's prior tag "moduli parities SUPPLIED" is now split: (λ, k_mod)
move to DERIVED (P2-conditional for k_mod); (k10, C) remain supplied-in-part with the
supplied remainder exactly localized.

## TP4 — consequences as map facts (no promotion, no eulogy)

All facts below are stamped: constant-moduli census branch (BASE) where marked; premise
ladder P0+P1(+P2) as marked; pairing branches cited, none adopted.

- **Fixed loci (mirror-invariant class members), exact** (`TP4_fixed_locus_branch_a`,
  `TP4_fixed_locus_branch_b`): branch (a): k00 = k11 = k10 = 0 (K = 0 — the E04
  stratum) + two C-conditions — a dim-2 locus (affine-shifted when R ≠ 0). At the F
  member (p=1, σ=1, R=0) this is **K = 0, (c00,c10) = (−c01,−c11) — EXACTLY the banked
  Route-B T5 swap-column cell (dim 2)**: the banked swap locus is recovered as this
  family member's fixed locus (F-P5 consistency). Branch (b): k00 = k11 = 0 with
  **k10 FREE** + two C-conditions (dim 3).
- **The S3 lever, applied with derived parities** (`TP4_S3_lever_application` [guard];
  the lever itself reused from the banked forcing package, never re-derived):
  - **Constant census (BASE), under P0+P1+P2: the constant λ and k_mod dials are
    parity-killed** — value forced to 0 and the constant direction fold-inadmissible.
    **The CUTTING outcome FIRES for the (λ, k_mod) sector,** conditional exactly on P2.
  - k10 constant: killed on branch-(a) completions only (supplied datum decides).
  - C constants: two combinations forced (to 0 at R=0; to affine R-shifted values
    otherwise); two free.
  - **Field census (BR-M): no collapse** — λ(x), k_mod(x) forced ODD about the wall;
    k10/C per branch. Both census branches carried; neither adopted.
- **Anchored-pairing landing** (`TP4_aF_anchor_landing` +
  `A1_aFprime_vs_aF_distinction`; **A1/A2-corrected — the pre-amendment text here
  overstated the cut**): on the forced locus λ = k_mod = 0: **P1-4D weight
  a_F = 2λ → 0** — the 4D-anchored branch lands ON a_F = 0, where the banked
  massive-locus certificate's PREMISE ("nonempty at every a_F ≠ 0 background") FAILS:
  **massive-locus nonemptiness at the landing is UNCERTIFIED on banked footing, NOT
  refuted** (premise-failure ≠ massless verdict; the quadratic atlas and the I_p
  sign-change certificate both presuppose a_F ≠ 0). The banked "P2 side (a_F′ = 0):
  no λ-row either way" statement is the **a_F′ = 0 criterion** (the P2 pairing, whose
  anchor weight is identically zero) — NOT the weight VALUE a_F = 0: under P1-4D at
  λ = 0, a_F′ = 2 ≠ 0 (checked zero-residual), so the λ-row does NOT vanish by banked
  pairing-relativity there; its status at an a_F = 0 background is UNDERIVED. The
  package's own fold-quotient statement (no constant-branch λ-carrier under P0+P1+P2,
  next bullets) stands independently of this. **P1-triad weight a_F = 1 + 2λ → 1 ≠ 0**
  — the triad-anchored branch's certificate premise is INTACT. The parity cut thus
  BIFURCATES by pairing branch — **UNCERTIFIED (P1-4D) vs INTACT (P1-triad), never
  ABSENT**; no branch is adopted here.
- **T4/stratum landings**: the forced locus is λ = 0 — the banked det-one/E07 axis
  (4D volume-blind; det e^{φX} ≡ 1 recomputed) — and k_mod = 0 — the banked KMOD0
  stratum, so the banked stratum-identity bookkeeping (one row dependency per census
  branch) applies to every mirror-invariant constant member
  (`TP4_kmod0_stratum_landing` [guard]). The triad-blind line λ = −1/2 is NOT hit.
- **Tie carrier (map fact, ceiling-respecting):** with the constant λ-direction
  parity-killed (BASE, P2), the banked integrated λ-row — the tie the Slice-2b
  massive/massless divergence rides — has no constant-branch carrier in the
  mirror-quotiented variation space; on the field branch the λ-row persists on odd
  λ(x). Stated as geometry of the variation domain only; no massive-branch verdict
  language (pre-committed ceiling).

## Falsifier record (derivation-side)

- **F-P1 (steering, both directions): structurally not fired — with ONE verifier-caught
  drift, in the CUTTING direction (the A1 mis-citation; memorialized).** The cutting
  legs (λ/k_mod) were NOT reached by choosing a dressing: λ's oddness is proven
  dressing-independent, k_mod's oddness family-uniform, and the SAME package computes
  the strongest known attack on its own cut (the chart-escape witness) and types P2 as
  NOT derived. The harmless legs (k10, C) are not left vague: the missing datum is
  localized to the banked-open 07-20 completion, with the forced signature (2+2)
  extracted anyway. **THE MEMORIAL:** the one drift the blind verifier found (A1) made
  the λ = 0 landing sound tie-free ("divergence ABSENT at that weight") — STRONGER
  than banked, in the ANTI-massive direction. The prereg named exactly this inverted
  hazard (§0: here the cutting outcome is the tempting-adjacent overstatement) and the
  steering discipline caught it — the first observed catch in the cutting direction
  (all prior catches of the named scope class were massive-favoring inflations).
  Corrected per `CORRECTION_LAYER.md`; with the correction, no eulogy/drama language
  remains (ceiling respected — verifier-confirmed).
- **F-P2 (invented dressing): not fired** — V5 adjudicated inside the classification;
  found to be one member of a derived family; its premise explicitly non-forced.
- **F-P3 (scope class): ONE FIRING — the A1 mis-citation (verifier-caught, corrected).**
  The check-25/TP4/JSON prose mis-scoped a banked citation (a_F′ = 0 rendered as
  a_F = 0), inflating one map fact on the CUTTING side — the EIGHTH catch of the named
  scope class (ordinal per this package's prereg watch; closure-corrected), and the
  first verified in the anti-massive direction.
  Corrected at every occurrence + a zero-residual distinction check added
  (`A1_aFprime_vs_aF_distinction`). All OTHER claims: premise ladder + census branch +
  branch (a)/(b) + R-status stamps present (verifier-hunted, no other firing);
  φ-dependent dressings typed out of scope.
- **F-P4 (census pre-emption): not fired** — both branches carried; no Route-D result
  cited (Route D runs independently; nothing here registers or adopts an extension).
- **F-P5 (bank contradiction): none found** — recomputed: the −X obstruction, the V5
  facts, the E04 closed form, the banked T5 swap cell (recovered as a fixed locus), the
  07-20 F_b family (recovered as the forced base block), K₄ actions (composition
  honesty). The 07-20 MULTIPLE_COMPLETIONS verdict is REFINED (family narrowed by
  involution/realness; parity facts extracted), not contradicted.
- **F-P6 (symbolic failure): none** — 41/41, exit 0, deterministic (rerun
  byte-identical ×3). Catch-proofs: now IN EVIDENCE as adopted in-package checks
  (A3, credited to the blind verifier's `VERIFIER_INDEPENDENT_CHECK.py` mutation set):
  wrong-parity (`ADOPTED_catch_wrong_parity_kmod_even`), wrong-signature
  (`ADOPTED_catch_wrong_C_signature`), k10-odd-on-branch-(b)
  (`ADOPTED_catch_k10_odd_on_branch_b`), and screen-swap-in-class
  (`ADOPTED_catch_screen_swap_in_class`) all FAIL the same machinery — CAUGHT. (The
  pre-amendment record asserted "catch-proofs verified" with no artifact in the
  package; the verifier flagged it and supplied the evidence.)

## Limits that travel

(i) Everything is at the registered positive triangular chart and the anchored
constant-generator presentation; P2 (chart-representability of the fold) is TYPED, not
derived — the k_mod/k10/C statements are conditional on it (λ's is not, within linear
dressings). (ii) φ-dependent dressings and cross-chart fold identifications (J07-type
transition data) are typed out of scope — classifying them is Route-D-adjacent
territory and was not entered (F-P4). (iii) The C-sector affine offsets at R ≠ 0 mean
"parity" there is affine-parity; forced VALUES shift with R while the forced COUNT
(two combinations) does not. (iv) The screen/angular completion (branch (a) vs (b),
p, R) remains the banked-open 07-20 non-uniqueness — this package localizes, and does
not close, it. (v) The consequences in TP4 are map facts conditional on the S3 lever's
own banked footing (jet-kill at the wall on the m-jet; constant vs field census both
carried). (vi) The "no Lorentz dressing" / "Lorentz membership EMPTY" statement is
scoped to the registered diagonal η₂ readout (A4): under the banked 07-20
null-coordinate choice of K as metric, every F_b is an exact O(1,1) reflection — the
caveat travels with any reuse of that row. (vii) The anchored-pairing landing statement
is A1-corrected: at the P1-4D λ = 0 landing the massive-locus certificate's premise
fails — nonemptiness there is UNCERTIFIED, not refuted; the λ-row's status at an
a_F = 0 background is UNDERIVED on banked footing (never "divergence ABSENT").
