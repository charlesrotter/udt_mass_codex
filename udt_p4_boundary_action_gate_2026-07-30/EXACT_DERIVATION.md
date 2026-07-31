# P4 boundary-action gate — exact derivation record (TW1–TW5)

Date: 2026-07-30. Contract: `PREREGISTRATION.md` (frozen before this run).

**AMENDMENT BANNER (2026-07-30, post-verifier).** Blind verifier verdict
**PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md`; AM-V1, AM-V2 + minor
notes — all applied; record = `CORRECTION_LAYER.md`). **No pre-amendment
computed claim changed.** AM-V1: the crease no-active-action result is restated
POSTURE-CONDITIONAL (given the quotient posture); the banked two-sided
conditional-forces-fold theorem keeps ALL its premises — **its premise set
loses ZERO members** (credited note `AMV1`). AM-V2: inertness /
effective-uniqueness statements carry "at the realized seam germ / per realized
configuration" (germ-locality counter-computation credited, `AMV2a`/`AMV2b`);
**OW2 unaffected.** Minor: BDY-TD gloss softened; J07/J08 discharge-by-typing
noted; the mirror-wall theorem doubly proven (symmetrization credited,
`AMV3a`–`AMV3d`).

Script: `derive_boundary_action.py` — post-amendment **64/64 checks, exit 0 =
55 SUBSTANTIVE zero-residual exact-SymPy checks (49 original + 6
verifier-credited: AMV2a/b, AMV3a–d) + 9 GUARDS (8 original + the AMV1
cited-argument note)** (guards = citation/bookkeeping rows, labeled `[guard]`
in-script and in the JSON; credited checks print `[verifier-credited]`),
deterministic (no floats, no randomness, no numeric solvers, no GPU; stdout
byte-identical across reruns — reverified ×3 post-amendment), single CPU
process, < 1 min wall (**FULL DECLARED SCOPE — no scope-ladder reduction
taken**: all four closure candidates at the 2nd-order layer, both arenas, the
4th-order layer typed). Outputs: `boundary_action_results.json`,
`DERIVATION_STDOUT.txt`, `WALL_RESPONSE_LEDGER.tsv`,
`DECISION_SURFACE_UPDATE.md`. Every check named in `monospace` below is one of
the 64. **Status: VERIFIED-WITH-AMENDMENT — amendments applied; nothing
adopted** (the §4 ceiling of the contract honored; driver bank pending).

**Honesty note (one check-formulation bug, found and fixed during the run):**
the first coding of `TW5c_affine_odd_kills_field` tested parity about the cell
CENTER instead of about BOTH WALLS (the banked gradient-seat form) and failed;
the check condition was corrected to the per-wall form (even ⇒ 1-jet vanishes at
each wall; odd ⇒ 0-jet vanishes at each wall). No physics content changed; the
banked lemma is what was always claimed.

**FULL STAMPS (F-B3, travel with every claim):**
- **arena W-1D** = round-static radial reduction (1D r-profiles; banked Branch
  G/P reduced Lagrangians; **pairing = NONE used**, matching the banked seam
  package; crease reading = pointwise-in-r; the screen/angular action of any
  involution is NOT specified — the banked 07-20 non-uniqueness stands).
- **arena W-REG** = registered positive triangular chart, stationary
  one-parameter presentation, fields (φ, f, bh), jets ≤ 2; **pairing branches
  P1-4D / P1-triad / P2 / P3-bulkP2 / P3-bulkP1 carried, none adopted**; census
  BASE exhaustive at jet ≤ 2, BR-M typed (the J05 leg); corners TYPED-ONLY.
- **jet layer:** N = 2 (the banked 2nd-order self-pairing layer) EXHAUSTIVE;
  N = 4 TYPED (2-jet wall + 3rd-normal-derivative momenta), not run.
- **parity:** ε_φ = −1 **DEFINITIONAL** (CANON C-2026-07-30-1 layer 3 — the
  status travels on every use); ρ-evenness = the banked fold-JC mirror-jet
  structure; f/bh parities SUPPLIED (definite per realized outcome under R-A —
  angular-completion bank — else free); moduli parities per Route P
  (P2-conditional; R-A discharges).
- **Guards held (F-B4):** G18/the fold never assumed (the fold enters only as an
  interrogated candidate); no x_max content; no anchor values (c_E, q, Z, ρ_s
  symbolic throughout); no census or pairing adopted.
- **F-B5 typing (one-way, per contract):** the bulk by-parts structure of the
  DECLARED pairing SUPPLIES the wall slot census (which jets pair at which
  order — `S0c`, `TW2f`); **B is an ELEMENT of the resulting slot space**; the
  natural BCs / germ pins are then DERIVED. The pairing is never defined via B
  anywhere in this package. (For NV-cell members the same slot space carries a
  free-standing R_wall instead of δB — same cuts, no germ-pin reading; stamped.)
- **F-B2 (Tonti scar):** no wall kernel/counterterm/functional is INVENTED
  anywhere — the general B is PARAMETRIZED (a generic function over the census
  alphabet) and the requirements are imposed ON it; every pin below is a derived
  condition, every freedom is exactly characterized. Well-posedness is never
  used to smuggle a preferred B: where well-posedness constrains (fold crease),
  the constraint is derived from R6 + parity and both readings are stated.

---

## TW1 — the wall-object census (exact; `WALL_RESPONSE_LEDGER.tsv` rows C01–C14)

**Arena W-1D (the seam):** 0-jet traces φ_s (ODD — crease-killed; essential
slot), ρ_s (EVEN — survives); 1-jet traces φ′_s, ρ′_s (momentum arguments ONLY —
see the R6 cut; ρ′_s is the D-b datum); the banked composite flux
q = Zρ_s²φ′_s; the anchored trace Q_s = c_E e^{−φ_s} (the ONLY legal
φ_s-dependence — `S0e`); and the seam functional 𝔅 itself — **the 07-18 OPEN
object (D-a; the M19/S24 rows), entered as a GENERIC function, not a
candidate.** Topology per candidate: fold = single-copy mirrored crease (Z₂
quotient); partner = two-sided seam, no surface term; glue+B = two-sided
interface carrying 𝔅; open-end = bare endpoint carrying 𝔅.

**Arena W-REG (the cell walls):** 0-jet traces (Q_w, f0_w, bh0_w) — trivial
K₄ character (`S0f`, cited Stage-2); 1-jet traces (p1_w, f1_w, h1_w) — momentum
arguments; moduli + invariants as wall arguments (BASE spectators; BR-M live);
the Route-D N3 wall m-jet slots on the varied fork (the J05 identity recomputed,
`TW2f`); corner slots TYPED-ONLY; the completion label 𝔠 as a discrete argument
(R3); the 2-jet/3rd-momentum objects of the N = 4 TYPED layer.

Parity gradings and provenance per row are in the ledger; the parity jet-kill
itself is recomputed (`S0d`: at a mirror wall u^{(j)} = 0 exactly for
(−1)^j ε = −1, both parities, generic degree-5 jet).

## TW2 — the general wall response (the analog of ℛ_PW for the wall)

**Parametrization (derived, candidate-free):** at the banked 2nd-order layer the
most general wall response consistent with equivariance/character/anchoring is,
**per wall stratum, ONE trivial-character smooth function of the
parity-surviving 0-jet traces** (+ moduli invariants per census fork; + 𝔠 as a
discrete argument), with φ-dependence only through Q (the anchored p = q rule,
recomputed `S0e`) — for the seam: 𝔅(Q_s, ρ_s).

Four exact structural theorems on it:

1. **The anchored variation** (`TW2a`): ∂𝔅/∂φ_s = −Q·𝔅_Q; at the seam locus
   φ_s = 0 the δφ-coefficient is −c_E·𝔅_Q(c_E, ρ_s). **An anchored wall
   functional CAN pair δφ at the seam through its Q-germ** — bare-φ stays
   excluded, Q-dependence is alphabet-legal and δφ-active. (This is the
   structural fact the q-datum results below ride.)
2. **First-germ-only activity** (`TW2b`, `TW2c_*`): the seam variation of the
   general 𝔅 is exactly −c_E𝔅_Q·δφ + 𝔅_ρ·δρ evaluated at the realized point —
   the constant term and ALL second-and-higher germ coefficients are
   variationally INERT **at the realized seam germ (per realized
   configuration)** [AM-V2]. **The active content of the wall response at
   N = 2 is EXACTLY the first germ (𝔅_Q, 𝔅_ρ)(c_E, ρ_s).** The inertness is
   GERM-LOCAL, not global: a pure (ρ−ρ_s)³ perturbation is inert at ρ_s but
   has active content 3(ρ₁−ρ_s)² at a different realized trace ρ₁ — the
   verifier's counter-computation, adopted as credited zero-residual checks
   `AMV2a`/`AMV2b`. Gloss (softened per the verifier's distinction): the inert
   germs shift NOTHING at the realized point — closer to PRIMITIVE
   nonuniqueness than to the banked BDY-TD momentum-shifting total-derivative
   freedom (07-18); the BDY-TD comparison is an interpretive analogy, not an
   identification.
3. **The R6 unpaired-jet cut** (`TW2d`, `TW2e`): a 1-jet-trace argument of 𝔅
   produces a δρ′ wall term with no bulk partner at N = 2 (the by-parts residue
   `S0c` pairs only 0-jet variations); R6 (no unpaired wall jets) forces that
   dependence to vanish IDENTICALLY — and the cut is pairing-weight-ROBUST
   (W_F = e^{a_F p0} ≠ 0). Same cut at the moduli-jet layer for B(m′_w) via the
   J05 identity (`TW2f`; BR-M).
4. **Dimensions per candidate (active moduli at N = 2):** fold **0** (forced —
   TW3); partner **0** (the germ-flat stratum); glue+B **0 free** (first germ
   uniquely pinned — TW3); open-end **2 germ functions free**. The N = 4 layer
   TYPED: Θ₄ pairs {v, v′}, so the 1-jet germ content of B ACTIVATES there —
   EXTENSION-REQUIRED stamp travels; not run.

## TW3 — the requirement cut, per closure candidate

Convention (banked K6c): stationarity ⟺ seam boundary residue = δ𝔅.

**Contract note (minor amendment):** the contract's "R6/R12/R13/J07/J08
imposed exactly" is, for **J07/J08, DISCHARGED BY TYPING** — their banked
class is typing/GC requirements (the 𝔠-argument + per-stratum typing), so
"imposed exactly" for them = typed exactly, not a seam computation; consistent
with the bank and stamped in limits (iv). R6/R12/R13 are imposed
computationally/definitionally as recorded below.

**FOLD (mirrored crease, quotient).** δφ essential-zero (v = −v ⇒ v = 0,
`TW3_fold_essential_dphi_zero`) ⇒ **the Q-germ of 𝔅 is INERT at the crease**
(`TW3_fold_Q_germ_inert`). The natural BC with the general 𝔅 reads
ρ′(r_s) = −𝔅_ρ/8 (`TW3_fold_natural_BC_with_B`; banked doubled momentum
−8cosh(2φ)ρ′). R6's differentiability reading of the MIRRORED configuration
(ρ EVEN across the crease — banked mirror jets; = the banked K3h kinematic C¹
fact) kills the crease 1-jet: ρ′(r_s) = 0. Jointly:
**𝔅_ρ(c_E, ρ_s) = 0 FORCED** (`TW3_fold_R6_forces_rho_germ_zero`). So at the
fold **the active germ is forced trivial — GIVEN the single-copy quotient
posture, the crease cannot carry an active 2nd-order wall action** [AM-V1:
this whole result is POSTURE-CONDITIONAL — the quotient posture is the fold
candidate's defining datum, interrogated not adopted] (equivalently: a fold
with an active ρ-germ has NO R6-admissible stationary configuration).
Consistency: 𝔅 ≡ 0 reproduces the banked K4d pin ρ′(r_s) = 0
(`TW3_fold_consistency_K4d`). Premise bookkeeping (credited note `AMV1`): this
crease fact is a COUSIN of — not the same object as — the banked two-sided
forcing theorem's "no seam surface term" premise, which governs the TWO-SIDED
matching problem before any fold is concluded; **that theorem's premise set
loses ZERO members** (see TW5(iii)).

**The W-REG mirror-wall theorem** (the same result at the general registered
member): for a MIRROR-COMPATIBLE member (parity-even density — the fold
candidate is undefined otherwise), every parity-even field's natural-BC momentum
vanishes KINEMATICALLY at the wall (`TW3_WREG_mirror_momentum_kill_f/h`, generic
parity-even density via the even-invariant construction, guard-verified
parity-even), so stationarity forces the corresponding B-germs to zero at the
realized traces; the parity-odd field's variation is essential-zero (its π_p is
generically nonzero but unpaired — `TW3_WREG_pi_p_wall_generic_nonzero`).
**Effective wall response at a mirror wall ≡ 0 at N = 2.** The theorem is now
**DOUBLY PROVEN**: the even-invariant construction here PLUS the verifier's
strictly-more-general SYMMETRIZATION proof (generic degree-4 polynomial density
in all six jets, even part under (p0, f1, h1) → −(…), no invariant basis
assumed), adopted as credited checks `AMV3a`–`AMV3d`. The
mirror-compatibility stamp is LOAD-BEARING and witnessed (a parity-odd density
term escapes the kill — `TW3_WREG_mirror_compat_load_bearing`; re-proven on
the full generic density, `AMV3d`). The theorem is
**pairing-branch-INDEPENDENT**: p0(wall) = 0 (ε_φ kill) ⇒ W_F(wall) = 1 for
every enumerated branch (`TW3_pairing_weight_drops_at_mirror_wall`); at
non-mirror walls W_F(wall) = (c_E/Q_w)^{a_F} — anchored-legal, so germ-pin
VALUES are branch-weighted but the cut STRUCTURE is branch-uniform
(`TW3_pairing_weight_anchored_nonmirror`).

**PARTNER / GLUE+B (two-sided).** The jump laws with the general 𝔅
(`TW3_twosided_jump_laws`): **[π_φ] = −c_E·𝔅_Q and [π_ρ] = 𝔅_ρ** at the seam
germ. Hence:
- **partner (no surface term) = the germ-flat stratum (0, 0)**: jumps vanish,
  WE continuity reproduced (`TW3_partner_WE_phi_continuity`,
  `TW3_partner_WE_rho_continuity_PP/PG`), ρ′(r_s) stays FREE
  (`TW3_partner_rhop_free` — banked K4g). The partner and glue candidates are
  strata of ONE variational structure, distinguished by the B-germ.
- **glue+B (the banked matter-cell seam):** the banked jump ΔΠ = q/2 pins
  **𝔅_ρ(c_E, ρ_s) = q/2** — K6c reproduced exactly
  (`TW3_glue_reproduces_K6c`) — and the banked FLUX SEAL ([π_φ] = 0, the weld
  chain's continuous q) holds **IFF 𝔅_Q(c_E, ρ_s) = 0**
  (`TW3_glue_flux_seal_iff_Q_flat`) — a NEW exact equivalence: **the banked glue
  pins the ENTIRE active germ uniquely.** With the higher content inert at the
  realized seam germ (TW2), the banked glue's wall action is **effectively
  UNIQUE at N = 2 — at the realized seam germ / per realized configuration**
  [AM-V2].

**OPEN-END (bare endpoint + 𝔅).** Free δφ, δρ give
(`TW3_openend_germ_laws`): **q = Zρ_s²φ′(r_s) = −c_E·𝔅_Q(c_E, ρ_s)**
(`TW3_openend_q_is_Q_germ`) and **ρ′(r_s) = −𝔅_ρ/4**. Consistency: 𝔅 ≡ 0
reproduces the banked K6d forcing q = 0 AND ρ′ = 0
(`TW3_openend_consistency_K6d_q0/rhop0`). **NEW map fact (certified
`TW3_openend_q_nonzero_off_germflat`): the banked "open-end kills the flux
seal" is the GERM-FLAT stratum statement only — with a Q-active germ, q is a
wall-response OUTPUT.** The q=0-under-no-choice leg re-derives exactly as
demanded, now exhibited as a stratum of the general law.

## TW4 — the selection verdict

**Outcome class: OW2 — a FAMILY with exact wall-moduli.** Per candidate
(ledger rows V01–V06):

| candidate | required-B space | active moduli at N=2 | D-b (ρ′_s) | q-datum |
|---|---|---|---|---|
| fold | NONEMPTY (witness 𝔅=0, `TW4_witness_fold_B0`); **effectively UNIQUE at the realized seam germ (per realized configuration) [AM-V2] — active germ FORCED trivial** (Q-germ inert; ρ-germ forced 0) | 0 | **0 (forced)** | OUTPUT (unconstrained by B) |
| partner | the germ-flat stratum (candidate definition) | 0 | **FREE** (continuity only) | continuous, data-determined |
| glue+B | NONEMPTY (witness (q/2)ρ, `TW4_witness_glue_*`); **first germ UNIQUELY PINNED** (𝔅_ρ=q/2; 𝔅_Q=0 ⟺ flux seal) — effectively unique at the realized seam germ / per realized configuration [AM-V2] | 0 free | jump q/2 carried by B | continuous ⟺ Q-flat germ (forced by the banked seal) |
| open-end | **FREE 2-germ-function FAMILY** — realizes ANY (q, ρ′_s) output pair (`TW4_openend_germ_plane_realizes_any_output`) | 2 germ functions | −𝔅_ρ/4 (germ output) | −c_E𝔅_Q (0 iff germ-flat) |

Non-uniqueness of the FULL space is certified: two members differing beyond the
first germ give IDENTICAL stationarity conditions **at the realized seam germ
(per realized configuration)** [AM-V2]
(`TW4_nonuniqueness_inert_content_*`, `TW4_nonuniqueness_members_distinct`) —
the family's inert directions are exact and nonempty AT the realized
configuration; away from it the "inert" content re-activates (credited
`AMV2a`/`AMV2b`: active content 3(ρ₁−ρ_s)² at a different realized trace ρ₁),
so the members are genuinely distinct FUNCTIONS agreeing only in their
realized-point stationarity data.

**The selection content (the contract's core question):** the banked
requirements **EMPTY no candidate and UNIQUE-select none.** Sharper — and this
is the structural finding: **B's variationally active content at the banked
layer is candidate-RELATIVE data (forced-trivial at mirror creases; uniquely
pinned at the banked glue; free exactly at open ends), NOT a candidate
discriminator.** The discriminating datum among the closure candidates is the
**POSTURE** (single-copy quotient / two-sided / open) — a topological datum
that is not a value of B. The 07-18/K6 expectation "the boundary action is the
selector" is hereby adjudicated AT THE 2ND-ORDER LAYER: B cannot select there;
whatever selective content the boundary action has must live in the TYPED-OPEN
layers (N = 4 activation of 1-jet germs; R9 periods; J07/J11
transition/holonomy — all GC, not run). **Three-way honesty (F-B1): this is
neither fold-selection, nor glue-selection, nor status-quo freedom — every
candidate's required-B space is exactly characterized and two of them are
effectively UNIQUE (at the realized seam germ / per realized configuration
[AM-V2]); the verifier should attack the family verdict hardest by
hunting a banked requirement that pins the open-end germ (the hunt run here:
R1/R13 pin the ARGUMENTS not the function; R9/J07/J08/R15 are GC/typed; M19 and
BDY-TD record exactly this openness).** [The verifier RAN that hunt
independently — R9/GC, R13, K₄ character, J07/J08, N=4 — and the no-selection
headline SURVIVED it, stamped at-N=2 throughout; see `VERIFIER_REPORT.md`
duty 1.]

**Consistency reproductions (contract duty):** the TS1 handshake
underdetermination (`S0b_*`); K6c B′ = q/2; K6d q = 0 under no-choice; K4d fold
ρ′ = 0; K4e–K4g partner WE; Slice-2b M-WALL = a_F·M-GEN. All zero-residual.

**Bank-contradiction sweep (F-B6): none found.** The fold result STRENGTHENS
K6a (not only is no surface term needed — GIVEN the quotient posture, no
active one is admissible) without contradiction; the conditional-forces-fold
theorem's premise set is untouched — **it loses ZERO members** (its "no seam
surface term" premise governs the TWO-SIDED WE matching; the new crease result
is a POSTURE-CONDITIONAL cousin fact, not a derivation of that premise —
[AM-V1], credited note `AMV1`, see TW5(iii)); TC3's
"LE-cell 2nd-order sub-families CAN self-pair" and NV no-forced-slots rows,
Slice-2b's M-WALL canon-parity caveat, and the M19/BDY-TD OPEN rows are all
consistent with (and sharpened by) the above.

## TW5 — consequences as map facts (details in `DECISION_SURFACE_UPDATE.md`)

- **G18 / closure surface: REDUCED, not decided.** The seam-closure package's
  two named data {D-a, D-b} REFINE: (i) at N = 2, D-a's variationally active
  content is FINITE — the first-germ pair per seam (fold: none; glue: pinned;
  open-end: 2 free germ functions); everything else is inert at this layer
  (N = 4 typed). (ii) **D-b is NOT independent of D-a** at the fold/open-end
  postures — ρ′_s is a derived function of the B-germ. (iii) [AM-V1,
  posture-conditional form] **The fold POSTURE is self-consistent: GIVEN the
  single-copy quotient posture, no active wall action is admissible at N = 2
  (R6 + parity), so WITHIN that posture the no-surface-term condition is
  automatic.** This is a COUSIN of — not a derivation of — the banked
  conditional-forces-fold theorem's "no seam surface term" premise: that
  theorem operates in the TWO-SIDED matching problem (deciding fold-vs-partner
  on the double cover, BEFORE any fold is concluded) and **keeps ALL its
  premises — its premise set loses ZERO members** (credited note `AMV1`). The
  closure question becomes: **one discrete POSTURE datum + the germ data**,
  with the germ data forced or pinned everywhere except at open ends.
- **Massive-branch wall conditions:** the fields cutting condition (a):
  **E0-collapse under definite realized parities is B-INDEPENDENT** (parity
  kinematics precede natural BCs — the affine lemma reproduced per-wall,
  `TW5c_*`; the ¬R-A escape keeps its banked status; under ¬R-A with free wall
  data the free-slope question becomes a B-germ question — TYPED, banked
  machinery does not reach the general-B wall equations there). **M-WALL:**
  = a_F·M-GEN reproduced on the quadratic class (`TW5a`); at FREE walls M-WALL
  = B⁺_p-germ + B⁻_p-germ — **exactly a B-germ functional** (`TW5b`); at mirror
  walls it remains a trace functional (banked caveat travels). **Triad branch:**
  germ pins carry a_F = 1+2λ; at the Route-P forced locus λ = 0 the triad
  weight is 1 — coinciding with the Slice-2b all-four consensus background
  a_F = 1 (map-fact observation, `TW5d`, nothing adopted).
- **Census/pairing surface: UNCHANGED** — both census branches carried (BASE
  exhaustive, BR-M typed via `TW2f`); verdict pairing-branch-UNIFORM (mirror
  walls weight-free; non-mirror pins branch-weighted).

## Falsifier record (derivation-side)

- **F-B1 (three-way steering): structure audit, both directions.** The landed
  verdict is OW2 (family) — the "status-quo comfort" direction — so the package
  attacks it in-text: the per-candidate spaces are NOT amorphous freedom (two
  are effectively unique, one forced-trivial); the free directions are exactly
  localized (open-end germs; inert content); and the pin-hunt over the
  remaining requirements is recorded. No step was phrased to favor
  fold/glue/free.
- **F-B2 (Tonti scar): not fired** — no functional invented; the general B is
  parametrized and cut; well-posedness only ever CONSTRAINS the general object.
- **F-B3 (stamps): policed** — every claim carries arena / candidate / pairing
  / census / jet-layer / parity stamps incl. ε_φ-DEFINITIONAL; the
  mirror-compatibility stamp is explicitly witnessed as load-bearing.
- **F-B4 (assumption smuggle): not fired** — fold interrogated, never assumed;
  no x_max; no anchor values; no census/pairing adopted.
- **F-B5 (pairing circularity): not fired** — the relation is typed one-way at
  the top of this record and in the JSON stamps.
- **F-B6 (bank contradiction): none found** (sweep above; all banked legs
  reproduced zero-residual).
- **F-B7 (symbolic failure): none** — 64/64 post-amendment (57 pre-amendment
  computations all surviving, none altered; +7 verifier-credited), exit 0,
  byte-identical rerun ×3; ONE check-formulation bug (TW5c odd-parity coding)
  found, fixed, and recorded in the honesty note — the verifier adjudicated
  the fix CLEAN (the original center-parity premise was genuinely WRONG; the
  per-wall replacement is the banked gradient-seat form and STRONGER); no
  check condition was weakened.

**Limits that travel:** (i) the exhaustive layer is N = 2 on the banked wall
census; the N = 4 layer (where 1-jet germ content ACTIVATES and could carry
selective content) is TYPED, not run — **the crease kill is N=2-scoped: at
N = 4 a ρ″-germ would survive the crease parity kill (verifier's note)**;
(i-b) [AM-V2] all inertness / effective-uniqueness statements are **germ-LOCAL
— at the realized seam germ, per realized configuration** (credited
`AMV2a`/`AMV2b`); (i-c) [AM-V1] the crease no-active-action result is
**POSTURE-CONDITIONAL** (given the single-copy quotient posture); the banked
two-sided forcing theorem's premise set loses ZERO members; (ii) corners
typed-only; (iii) the W-1D
candidate analysis is pairing-free by construction (banked seam arena); the
W-REG pairing statements cover the five enumerated branches only; (iv) R9
periods, J07/J11 holonomy, R5/R14 WS legs untouched (GC/WS — could in principle
further cut the open-end germ family; typed); (v) the mirror-wall theorem
requires mirror-compatibility of the member (witnessed load-bearing); (vi) the
glue germ-pin rides the banked weld jump ΔΠ = q/2 and the banked flux-seal
continuity — banked-in-use premises, cited not re-derived; (vii) f/bh parity
statements ride the SUPPLIED/realized-outcome status of the angular-completion
bank (R-A typed, not derived); (viii) NV-cell members carry the same slot cuts
with a free-standing R_wall (no germ-pin reading) — stamped, not separately
adjudicated.
