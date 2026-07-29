# P4 Route A Stage 1 — THE POSED RESPONSE INVERSE PROBLEM (TA2 + TA3 + TA4)

Date: 2026-07-29. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before derivation).
This document POSES the inverse problem Stage 2 will attack. It selects NO candidate
response, NO action, NO modulus value, NO pairing, NO completion class (F-A1/F-A2). The
L6 fork is carried BOTH ways (F-A3). Named checks in `monospace` are zero-residual
checks in `derive_routeA_stage1.py` (40/40, exit 0; pre-amendment 34/34).
**AMENDED 2026-07-29 per `VERIFIER_REPORT.md`** (A1: character-matched relative
invariance in §2.1; A3: narrowed channel class in §3 R4; A4: clash-scan additions in
§3.2). Amendment record: `CORRECTION_LAYER.md`.

**Stamps carried by every statement here:** the domain footing is the Route B bank
(7-parameter E02 class, two-scalar seat, EXACT K₄ residual chart quotient; L1/L2
MODULUS-CARRIED); the MAP's "E07 k = λ" seat equation is REFUTED (Route B T4) and never
used; base-data names (c_E, α, f, b/q_B) are the registered stationary-family
presentation (Route C TC1); all pointwise statements are registered-chart,
one-parameter, off-shell (Route B scope stamps travel).

---

## 1. TA2 — the typed variation domain 𝒟

### 1.1 What the configuration space IS

A point of 𝒟 is a tuple, with every entry from the census
(`VARIATION_DOMAIN_CENSUS.tsv`, one row per object; forks typed there, none chosen):

    ( φ ;  base data (c_E, α, f, b/q_B — stationary presentation; general coframe
           data otherwise) ;
      moduli m = (λ, k_mod, k10, C)  [per fork: a point of ℝ⁷, or fields] ;
      boundary data on the finite-cell wall strata (mirror parity φ→−φ; sector split) ;
      completion label 𝔠  [per fork L4: supplied, or a discrete configuration direction] )

read MODULO the local-Lorentz equivariance quotient (E11; requirement 7): configurations
are chart representatives with the operation transforming as X ↦ ΛXΛ⁻¹; on the
registered positive triangular chart the infinitesimal stabilizer is trivial (Route B
T1) and the residual gauge is the EXACT discrete Klein four-group

    K₄ = {I, diag(1,1,−1,−1), diag(1,−1,−1,1), diag(1,−1,1,−1)},

acting on the moduli as (K,C) ↦ (K,−C), k10 ↦ −k10 with signed C-flips; λ and k_mod are
invariant (recomputed: `A2_*`, `A3_*`). So, per the constant-moduli fork option, the
moduli factor of 𝒟 is the quotient

    M = ( ℝ²_{(λ,k_mod)} × ℝ_{k10} × ℝ⁴_C ) / K₄ ,

an orbifold with fixed strata where k10 = 0 and/or C-blocks vanish; per the
field-promotion fork option it is sections into that quotient (typed only — promotion
extends the banked pointwise class; census row consequence). No stratum of the E02 class
is removed: strata (E03…E08) are LOCI in M, not choices (L1 MODULUS-CARRIED).

### 1.2 Where the boundary/corner strata sit

The finite-cell canon (CANON C-2026-06-10-2: finite mirrored cells, no spatial
infinity; seal-involution sector split C-2026-07-04-1) stratifies each cell:

    interior  ⊔  wall strata (codim 1: the mirror/seal boundary; CMB-type outer wall
    for the universe cell, φ=0 interface for matter cells)  ⊔  corner strata (codim 2).

Boundary data live on the wall strata with the mirrored parity as SUPPLIED structure;
whether they are varied or held is an OPEN-FORK (census row; both typed). The
completion label 𝔠 indexes which of the 12 FC families closes the cell — supplied
(within-one-family fork) or a discrete direction of 𝒟 (over-the-class fork).

### 1.3 Where the three gaps live as explicit moduli directions

- **Physical comparison/depth gap**: the φ-direction plus the anchor structure
  (c_E; shift-equivariance forced — `D3_*`, F-RA4). Not a free modulus; a field
  direction plus supplied calibration.
- **Finite reciprocal full-frame lift gap (the λ seat)**: exactly the moduli factor M —
  now the TWO-scalar seat (λ, k_mod) plus (k10, C) mod K₄ (Route B; NOT one scalar).
- **Global completion/interfaces gap**: the boundary-data strata + the completion label
  𝔠 + the J07/J11 transition data (the E08-type twisted-cocycle law is the required
  transition-data TYPE — stated, not filled; Route B T3).

### 1.4 What a tangent vector IS

A tangent vector at a configuration is the equivalence class (mod infinitesimal gauge;
on the registered chart, mod nothing continuous — the quotient is discrete K₄):

    δ𝒳 = ( δφ ; δ(base data) = (δf, δbh [, δα if active fork][, δc_E if promoted]) ;
            δm = (δλ, δk_mod, δk10, δC)  [ℝ⁷-vector, or field variations per fork] ;
            δ(boundary data)  [if varied fork] )

with NO tangent component along 𝔠 (discrete). The pointwise infinitesimal content of a
frame variation is the banked physical tangent

    T = Xᵀη + ηX = [[2I₂, Cᵀ],[C, K+Kᵀ]]      (`T2_tangent_block_form`),

transporting as a bilinear form, T ↦ Λ⁻ᵀTΛ⁻¹ (`T2_tangent_transport_bilinear_*`).
THIS is the object the response pairs with.

### 1.5 The pairing structures available (L7 typed — ENUMERATED, NONE ADOPTED)

The response is a one-form on 𝒟: it eats tangent vectors. Three pairing structures are
available to REPRESENT it by component densities; each has requirements; adopting one
is Stage-2+ business:

| Pairing | Definition sketch | What it requires (supplied structure) | Notes |
|---|---|---|---|
| **P1 metric-induced** | L²-type: ⟨𝓡, δ𝒳⟩ = ∫_cell R·δ𝒳 dV_g with dV from the physical metric g(φ,…) | a VOLUME FUNCTIONAL choice — and Route B T4 proves the choice is load-bearing: 4D coframe volume is blind on {λ=0}, ruler+screen triad volume on {λ=−1/2}, witness slice needs λ=−1/2 AND zero twist shift; plus density weights per slot | the volume choice is itself a supplied structure to be tagged; silently picking one = F-A2 |
| **P2 duality-natural** | canonical T*𝒟 pairing: 𝓡 is intrinsically a section of the cotangent structure; ⟨𝓡, δ𝒳⟩ needs no metric | only the smooth/jet structure of 𝒟 + a declared distributional class and jet-order grading (the dual space choice) | purest typing; components then live in the declared dual — the functional-analytic class is the open datum (L7's "part of the missing object itself", S13) |
| **P3 boundary-extended** | relative pairing: ⟨𝓡, δ𝒳⟩ = ∫_bulk + ∮_walls + Σ_corners with paired (bulk, wall, corner) densities | the finite-cell stratification + trace/jet maps onto each stratum; REQUIRED reading whenever boundary data are in the varied fork (requirement 6) | subsumes P1/P2 bulk choices; the wall jet-depth is candidate-jet-order dependent (Route C TC5 cited as examples only) |

---

## 2. TA3 — the most general response object 𝓡

### 2.1 Component structure over the census

The most general metric-native off-shell global-local response one-form on 𝒟:

    𝓡 = ( R_φ ; R_f , R_bh [, R_α][, R_{c_E}] ;            — field-direction components
          R_λ , R_{k_mod} , R_{k10} , R_C ;                 — moduli components
          {R_∂ per wall stratum} ; {R_corner per corner} )  — boundary/corner components

with, per census fork: moduli components are global scalars (constant fork — one
relation per cell per modulus) or densities (field fork); boundary components exist as
slots in either boundary fork (as consistency conditions if data are held). Under the
equivariance quotient the components are FORCED (candidate-free) to be:

- an EQUIVARIANT family, never an invariant object (no Lorentz-invariant member exists
  in the class: scalar-only centralizer + founded H — `A1_*`, `A5_*`; F-RA1);
- contragredient to the tangent transport (`T2_*`);
- K₄-quotient-honest via CHARACTER-MATCHED RELATIVE INVARIANCE (A1-amended, F-RA1):
  each component R_v transforms with the K₄ character of its paired direction dv
  (component character × direction character = trivial — `A6_*`); components along
  K₄-invariant directions (δφ, base data, δλ, δk_mod, boundary data) factor verbatim
  through the exact K₄ invariants (k10², the C character-class quadratics, the four
  mixed cubics k10·{c00,c11}·{c01,c10} — `A4_*`; a verifier-proven GENERATING set of
  the full invariant ring), while R_k10 is χ_a-relative (e.g. k10·invariant or
  c_b·c_c·invariant) and R_C components are χ_b/χ_c-relative; character-MISMATCHED
  dependence is not well defined on 𝒟 (counterexample on record: ω = k10·dk10 =
  ½d(k10²), K₄-invariant and exact with a bare-k10-linear component);
- shift-equivariant in φ with the shift absorbed into the anchor (`D3_*`; F-RA4);
- carrying the trace-free screen slot k_mod·diag(−1,1) as a component slot (F-RA2 —
  slot PRESENCE forced by requirement 4 + J06's structure; no value demanded).

### 2.2 Locality grading by jet order

Each component is graded by the jet order N of its dependence on the fields. NO order
is adopted. The known spread (cited as jet-order EXAMPLES only, F-A1): the EH-type
conditional equations carry ≤ 2nd jets while the C2/Bach-type carry 3rd/4th jets on
every component (Route C TC2/TC3 — the same seven-component census splits 2nd vs
3rd/4th order); the boundary/corner slot depth grows with N (1-jet wall vs 2-jet wall +
3rd-derivative momenta; Route C TC5). The grading is a SLOT of the general object: a
candidate declares its N; the domain typing is N-agnostic.

### 2.3 The L6 fork — formalized BOTH ways (F-A3)

- **Exact (variational) subcase — a TESTABLE property, never a filter:** 𝓡 is exact
  iff 𝓡 = δS for some action functional S on 𝒟, which holds locally iff the Helmholtz
  condition holds — the formal Fréchet derivative D𝓡 is self-adjoint with respect to
  the DECLARED pairing (P1/P2/P3 — the test is pairing-relative), plus boundary
  integrability (gate 5) and vanishing/quantized periods (gate 6) for global exactness.
  This SUBCASE is characterized so it can be TESTED (gate 3); it is not demanded.
- **Nonvariational case — fully in scope:** 𝓡 an arbitrary section satisfying
  requirements 1–15 with no exactness. The closure audit deliberately phrased the
  missing object as a RESPONSE; the unwritten CM0-C nonvariational completion is the
  recorded-exclusion EXAMPLE of this class (Route C census row; cited as an exclusion
  record, not a candidate). Zeros of 𝓡 are then equations of motion without an action.

### 2.4 The inverse problem (posed; NOT solved here)

    Find the space  ℛ = { 𝓡 as in §2.1–§2.3  |  𝓡 satisfies R1–R15 of §3 } ,
    and determine whether ℛ is empty, a point, or a family (with its moduli).

Emptiness, uniqueness, and non-uniqueness are ALL first-class Stage-2+ outcomes
(MAP §5). Stage 1 ends at the posed problem plus the forced structure (EXACT_DERIVATION).

---

## 3. TA4 — the fifteen requirements as exact conditions on 𝓡

Classification key: **PW** = POINTWISE-DECIDABLE (decidable on the object's definition /
jet-level data at a point), **WS** = WHOLE-SOLUTION (needs a solution of 𝓡=0),
**GC** = GLOBAL-COMPLETION (needs completion/boundary/holonomy data). Mixed
requirements are split into stamped sub-conditions (F-A6).

| # | Requirement (MAP §2 order) | Exact condition on 𝓡 | Class | Source |
|---|---|---|---|---|
| R1 | native provenance | every component of 𝓡 is built from census objects + derived structure only; no fitted density, posited carrier, or GR-imported charge appears in any component definition (provenance audit on the definition) | PW (definition-level) | MAP §2; adjudication CM0-C/G09 rows |
| R2 | explicit field census | the component list of 𝓡 is exactly indexed by `VARIATION_DOMAIN_CENSUS.tsv`; a missing component = a silent freeze (F-A2); extra components = unregistered DOF | PW (definition-level) | MAP L3; this package TA1 |
| R3 | global-completion feedback | the completion data (𝔠, boundary data, transition data) appear as ARGUMENTS of the local components (the local equations may depend on the completion), with the dependence explicit — not through a fitted global average (see R13) | GC | MAP §2; three-gap decomposition |
| R4 | trace-free anisotropic screen response | the screen sector of 𝓡 decomposes as r_tr·I₂ + r_tf·diag(−1,1) (+ mixing slots) on the seat (`B2_*`); EXACT condition (A3-amended): functionals of tr X and of det e^{φX} have identically zero k_mod-pairing (`B3_*`) — not every trace-built channel (tr(X²) pairs, `B5_*`) — and the slot theorem ⟨r_tr·I₂, diag(−1,1)⟩ ≡ 0 holds exactly (`B5_*`): any k_mod-pairing routes through the trace-free part, so selection of the transverse line ⟹ the r_tf slot is present (F-RA2) | PW (seat-level) | banked no-go (MAP §2); Route B T4; J06 |
| R5 | same-solution mass/volume/density relation | mass, volume, and density functionals evaluated on ONE solution of 𝓡=0 must satisfy the closure relation on that same solution (no cross-solution splicing) | WS | MAP §2; adjudication three-part mass ruling |
| R6 | finite-cell boundary+corner differentiability | for varied boundary data, the total pairing ⟨𝓡, δ𝒳⟩ contains no unpaired wall/corner jet terms (every boundary jet slot up to the candidate's N is paired); the mirrored-cell parity (spatial mirror for static sectors, temporal for time-on; CANON sector split) constrains the wall data the components may use; seal VALUE alone is insufficient | GC (with a PW jet-count sub-check per stratum) | CANON C-2026-06-10-2/C-2026-07-04-1; requirement 6; Route C TC5 examples |
| R7 | gauge/Noether on the quotient | (a) equivariance: 𝓡(Λ·𝒳)[Λ·δ𝒳] = 𝓡(𝒳)[δ𝒳] for local Lorentz Λ, i.e. components transform contragradiently (`T2_*`), character-matched on the K₄ chart (`A3_*`,`A4_*`,`A6_*`; A1-amended) — **PW**; (b) Noether: ⟨𝓡, δ_gauge𝒳⟩ ≡ 0 identically for gauge directions (off-shell Bianchi-type identities) — **PW as an identity, checked componentwise**; current conservation statements — **WS** | PW (a,b) + WS (currents) | E11; J10; Route B T1 |
| R8 | Helmholtz testability | the object's definition permits computing D𝓡 and testing self-adjointness w.r.t. the declared pairing; the test is a GATE property (gate 3), never a definitional filter (F-A3) | PW (jet-level conditions) | MAP L6; requirement 8 |
| R9 | global periods | in the exact subcase: periods of 𝓡 over nontrivial cycles of 𝒟 (completion-class cycles, K₄-orbifold cycles, J11 loop holonomies) vanish or are explicitly quantized; in the nonvariational case: the corresponding holonomy of the closure data is classified | GC | MAP §2; J11 |
| R10 | extension-gate precedence | 𝓡 is defined on the E02 footing (coframe extension selected/carried FIRST), never on the generic F4[6] arena (G07) — honored by construction: 𝒟 is built on the Route B bank | PW (definition-level; satisfied by construction) | MAP §2 requirement 10; G07/G08 |
| R11 | the J01–J15 obligations | each J-row instantiated as a condition on 𝓡 — see §3.1 | per-row (§3.1) | JOINT_OPERATION_OBLIGATIONS.tsv (verbatim) |
| R12 | restrict-then-vary FORBIDDEN | 𝓡 carries components along EVERY census direction before any restriction; stratum restrictions are pullbacks of the full object (post-composition); exact inequivalence witness `C1_*`/`C2_*` (F-RA3); the EH-RED scar is the banked instance | PW (definitional/structural) | adjudication (EH-RED); requirement 12; Route C F-C1 discipline |
| R13 | no fitted global average as local coupling | no component contains a global functional of the solution fitted from data as a pointwise coupling constant; global data may enter only as the explicit completion arguments of R3 | PW (definition-level) with a GC cross-check | MAP §2 |
| R14 | bootstrap stays on-shell-admissibility | no bootstrap/fixed-point structure (G12) is written into the DEFINITION of 𝓡; bootstrap statements are admissibility checks on solutions of 𝓡=0 until a varied form is DERIVED | WS (by definition of the requirement) | G12; MAP §2 |
| R15 | topology alone is not matter | a nonzero topological charge/completion label alone must not force a matter source component of 𝓡: components may not convert 𝔠 or winding data into a source term absent field support | GC (honesty condition on the 𝔠-dependence) | MAP §2; matter-carrier-is-posit bedrock |

**Tallies (primary class):** PW 8 (R1, R2, R4, R7, R8, R10, R12, R13) · WS 2 (R5, R14) ·
GC 4 (R3, R6, R9, R15) · R11 = per-row (below). Mixed sub-parts stamped in-row (F-A6).

### 3.1 J01–J15 instantiated on 𝓡 (rows verbatim from the joint bank)

| J | Instantiation on the typed domain | Class |
|---|---|---|
| J01 | 𝒟-points carry one coherent nondegenerate 4D coframe/metric (census row 1 + base data); piecewise/disconnected configurations are not points of 𝒟 | PW |
| J02 | the founded reciprocal pair (G01/G02) is the base-block structure of every configuration (H fixed); observer typing enters through the readout (c_E row) | PW |
| J03 | the comparison arrows/pairing domain is the declared pairing structure of §1.5 — a supplied choice to be tagged, not free-floating | PW (typing) |
| J04 | depth enters components only as the additive-log φ with shift-equivariance (`D3_*`); arbitrary f(q)−f(p) substitutes are excluded by R1 provenance | PW |
| J05 | the response pairs with the FULL tangent T (all coframe slots, `T2_tangent_block_form`) — pair-only/infinitesimal-only rules are incomplete by typing | PW |
| J06 | **on the two-scalar seat:** the (λ, k_mod, k10, C) components of 𝓡 either determine the moduli (which for k_mod REQUIRES the trace-free slot — `B3_*`, F-RA2) or the undetermined moduli are explicitly retained and reported; the named false pass ("spectator screen isotropy or trace zero assumed") = silently deleting those components (F-A2) | PW (slot structure) + WS (actual determination) |
| J07 | chart-overlap transition data for the mixing block must satisfy the banked two-sided twisted 1-cocycle law L(γ₂∘γ₁)=Q(γ₂)L(γ₁)+L(γ₂)ρ(γ₁) (Route B T3 — the required TYPE; not filled here) | GC |
| J08 | completion/descent data (𝔠, caps/seams/quotients) are supplied per fork L4; 𝓡's 𝔠-dependence is explicit (R3) | GC |
| J09 | null/type-changing strata of a configuration require an explicit continuation or exclusion statement in the candidate's domain declaration | GC |
| J10 | **with the exact gauge group:** equivariance under local Lorentz (connected part: contragredient transport `T2_*`; trivial infinitesimal stabilizer on the registered chart) AND well-definedness on the K₄ quotient via character-matched relative invariance (`A3_*`/`A4_*`/`A6_*`; A1-amended); no preferred fixed plane exists to anchor an invariant object (`A5_*`, F-RA1); covariance of the FAMILY is not unique selection (false-pass guard) | PW |
| J11 | composition/reversal/loop consistency of the closure data; loop holonomy of the J07 cocycle trivial or classified | GC |
| J12 | one source lineage: 𝓡's components on all three layers (depth, lift, global) derive from the same census + banked structure (this package is the typed import record) | PW (provenance) |
| J13 | 𝓡 must distinguish λ-profile, cocycle twist, and completion controls: the discriminator content lives exactly in the retained moduli slots (E07 content = k_mod; E08 content = C/s-cocycle; completion = 𝔠); deleting them = imposition (Route B C4 typing) | PW (slot) + GC (completion control) |
| J14 | **built into the definition (F-RA3):** 𝓡 is an off-shell one-form; its zero set is a DERIVED subset (on-shell selection separate from configuration existence); the exact witness `C2_*` shows the orders are inequivalent | PW (definitional) |
| J15 | Stage-2+ outcomes must report the full surviving space ℛ (empty/point/family with moduli); one witness is never promoted to unique law | status (reporting discipline) |

### 3.2 Clash scan (OA3 watch)

No pair of R1–R15 was found to CLASH on the typed domain at Stage-1 depth: the
candidate-free forced statements (F-RA1..F-RA4) are mutually consistent (equivariant
family + trace-free slot + full-domain definition + shift-equivariance impose
conditions on DIFFERENT component axes). The nearest tension — R4's trace-free slot vs
a hypothetical volume-only pairing choice (P1 with 4D volume, which is k_mod-blind,
`B3_volume_density_channel_blind_to_kmod`) — is NOT a clash: it is exactly why the
pairing choice is load-bearing and enumerated-not-adopted (§1.5). OA3 not reached;
watch stays open for Stage 2 (where Helmholtz/gauge conditions become computations).

**Additions per the verifier's clash constructions (A4-amended; `VERIFIER_REPORT.md`
§5, `VERIFIER_INDEPENDENT_CHECK.py` V8):**

- **The φ=0 mirror-interface zero-point vs shift-equivariance tension (verifier
  construction 1 — a REAL tension the original scan omitted).** The finite-cell φ=0
  mirror/seal interface (§1.2; census row 16) anchors an absolute φ zero-point, while
  F-RA4 / census row 6 forbid any component from depending on one. The mirror and the
  shift do NOT commute: −(φ+s) ≠ −φ+s for s ≠ 0 (`V8_clash1_mirror_breaks_shift`).
  RESOLUTION (typed, not decided — per the verifier's construction): the mirror
  interface is a SUPPLIED structure whose anchor is absorbable into the c_E anchor
  (`D3_anchor_absorption`), so components may use the anchored φ only THROUGH
  supplied-structure slots (boundary-data components / the c_E calibration), never as
  a bare absolute-φ dependence in a bulk component. Not a proven requirement clash;
  recorded with its resolution so Stage 2 candidates are checked against it.
- **The K₄-torsion-period vacuity note (verifier construction 2 — a spec scope note,
  not a clash).** The gate-6/R9 period condition on K₄-orbifold cycles is VACUOUS for
  closed one-forms: over an order-2 (torsion) orbifold class, 2·period = period over
  γ² = 0, so the period vanishes automatically (`V8_clash2_torsion_periods_vacuous`).
  Gate 6 carries the corresponding scope note; the R9 content on those cycles lives
  entirely in the non-closed / nonvariational-holonomy reading and in the
  completion-class and J07/J11 cocycle cycles.
