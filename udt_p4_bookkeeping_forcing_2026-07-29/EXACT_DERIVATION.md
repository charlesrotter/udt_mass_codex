# P4 bookkeeping-forcing — exact derivation record (TF1–TF4)

Date: 2026-07-29. Branch: grok. Contract: `PREREGISTRATION.md` (frozen before this
derivation). Script: `derive_bookkeeping_forcing.py` — **21/21 checks, exit 0 = 13
SUBSTANTIVE zero-residual exact-SymPy checks + 8 CITATION GUARDS** (guards =
definitional-unpacking / citation / typing bookkeeping, labeled `[guard]` in-script and
in the JSON, never counted as residual computations), deterministic (no floats, no
randomness, no network, no numeric solvers, no GPU; stdout byte-identical across reruns —
re-verified ×3 post-amendment), single CPU process, < 1 min (FULL DECLARED SCOPE —
**no scope-ladder reduction taken**; all eight TF2 source families interrogated, not
only the load-bearing four). Outputs: `bookkeeping_forcing_results.json`,
`DERIVATION_STDOUT.txt`, `FORCING_LEDGER.tsv`, `RESIDUAL_DECISION_SURFACE.md`. Every
check named in `monospace` below is one of the 21.

**AMENDMENT BANNER (2026-07-29, post-verifier; verdict PASS-WITH-REQUIRED-AMENDMENTS —
`VERIFIER_REPORT.md`; record = `CORRECTION_LAYER.md`):** A1 (required) — the §4
field-census massless bullet now carries the no-moduli-jet-alphabet clause (echoed in
the TF4 JSON detail and `RESIDUAL_DECISION_SURFACE.md`); A2 (recommended, implemented)
— the S1 record now cites and adjudicates the upstream 07-25 phrase "exactly seven
pointwise extension parameters" (at-a-point count; decides neither census branch); plus
two verifier legs ADOPTED as credited in-package checks
(`ADOPTED_xdep_duhamel_two_sided_cocycle`, `ADOPTED_swap_dressing_parity_candidate` —
the latter a Route-P CANDIDATE INPUT, explicitly not banked as a parity derivation).
**No computed claim, verdict, or outcome class changed.**

**Binding boundary (carried on every statement):** NO fork decided by preference (F-K1 —
the INTEGRATED answer is the named temptation and received the adversarial-first
treatment; see §5); the crux DERIVED from the banked tangent/pairing definitions, never
imported as textbook variational habit (F-K2 — discharge record in §1.3); every
forced/open/reduces claim carries sector + cell + pairing + stratum + census-branch
stamps (F-K3); the census fork is NOT silently adopted — it goes to Charles with its
exact residual freedom (F-K4; `RESIDUAL_DECISION_SURFACE.md`); no contradiction with the
Slice-2b theorem, the E02 record, the cocycle laws, the stratum identities, or the
anchored alphabet was found or introduced (F-K5); no symbolic failure (F-K6: 21/21).

**Standing scope stamps (travel with every statement):** registered positive triangular
chart; registered stationary one-parameter presentation (fields (φ, f, bh), jets ≤ 2);
enumerated anchored pairing family (P1-4D a_F = 2λ, P1-triad a_F = 1+2λ, P2 a_F = 0,
P3-bulk* = declared bulk + wall/corner blocks) with moduli-slot weight W_M = e^{a_M p0}
— **W_M provenance (a task-named duty): the Stage-3 TC1 premise row is its banked
source: P2 ⇒ a_M = 0; P1 instances ⇒ per-slot moduli weights SUPPLIED (tagged open
structure); the integrated row FORM ∫W_M R_μ dx = 0 entered the bank as Slice-2's
`T0_base_branch_integrated_row` [guard] (definitional unpacking), and the banked λ-row
is a_M-INDEPENDENT (W_M cancels — `TD2_lambda_row_exact_form`)** — so nothing physical
rides the open W_M supply for the banked tie. Off-shell typing computations throughout;
both census branches carried (BASE = constant moduli, BR-M = field moduli), neither
adopted. Cells: {LE, NV} × {GENERIC, KMOD0}; RES-CNEQ0 entered by the banked
shear-identity EXAMPLE only (deeper stratification CENSUS-REQUIRED upstream, inherited).

---

## 0. Premises (chose or derived — stamped)

| Premise | Tag |
|---|---|
| Stage-1 bank: tangent definition §1.4-as-amended; §1.5 pairing enumeration; census rows 11–14 (fork typed BOTH ways); R/J tables | DERIVED input (banked; read verbatim, never re-derived) |
| Route B bank: E02 constant-generator class, T1 stabilizers/K₄, T2 composition/drift, T3 cocycle laws | DERIVED input (recomputed as consistency: checks 8, 9, 11) |
| Stage-2 bank: anchored alphabet (no moduli jets on BASE; BR-M row typed), character modules, k_mod = 0 identity, shear example | DERIVED input (reused: checks 5, 11, 14) |
| Stage-3 bank: anchored-weight representation (the W_M provenance row), H4 machinery, TC3 parity kill, interior-supported-variation precedent | DERIVED input (reused: checks 3, 4, 5, 10) |
| Slice-2/2b bank: `T0_base_branch_integrated_row`, λ-row a_M-independence, the R2 bookkeeping theorem with stamps | DERIVED input (restated §4 only, stamps intact) |
| CANON C-2026-06-10-2 / C-2026-07-04-1 (mirrored finite cell; sector split; ε_φ = −1 instance) | CANON cite; **moduli parities ε_m NOT derived — SUPPLIED** (check 10) |
| Sample densities/configurations in witnesses (p0 = x², f = x², polynomial weights) | FREE off-shell instances (typing witnesses — a pairing-form theorem is off-shell; instances chosen for exact integrability, alphabet-legality noted per check) |
| Category-A named steps: Picard uniqueness (block-ODE), integral positivity, continuity + bump density (localization closure) | Category-A (cited calculus, named where used; banked Slice-2 precedent lane) |
| SymPy exact, CPU, single process; coordinate measure dx | Category-A conditioning (banked) |

## 1. TF1 — the pairing-form theorem

### 1.1 Statement (derived)

Let 𝓡 have moduli components R_μ (μ over the seven directions λ, k_mod, k10, c00, c01,
c10, c11), realized per the banked Stage-2 parametrization as pointwise densities over
the alphabet, and let the pairing be any member of the enumerated anchored family
(bulk weight W_M = e^{a_M p0} on the moduli slots; P3 adds wall/corner blocks). Then:

- **(a) Constant-moduli census branch (BASE).** The moduli tangent block is ℝ⁷ — ONE
  direction per modulus per cell (POSED §1.4, read exactly: δm = (δλ, δk_mod, δk10, δC)
  an ℝ⁷-vector). The pairing restricted to it is a linear functional on a 7-dimensional
  space, so ⟨𝓡, δ𝒳⟩ = 0 supplies **EXACTLY seven scalar relations per cell** — in the
  enumerated representation, exactly the integrated rows ∫W_M R_μ dx = 0 (constants pull
  out: `TF1_constant_fork_integrated_row_definitional` [guard], restating the banked
  Slice-2 T0 guard). On P3 the constant-fork row is ∫bulk + Σwall-terms — still one
  scalar per modulus (the direction is still one-dimensional). Representation-free form:
  the constant fork supplies conditions of codimension ≤ 7; the integrated FORM is the
  enumerated-representation instance.
- **(b) The pointwise row is an EXTRA condition the pairing does not supply on (a).**
  Exhibited exactly, on the whole weight family at once: an alphabet-legal density
  (f1 = 2x at the configuration f = x², p0 = x²) has ∫e^{a_M x²}·2x dx = 0 EXACTLY at
  symbolic a_M and at a_M = 0, yet equals 1 at x = 1/2
  (`TF1_separation_witness_odd_density_all_weights`); and TWO members differing by odd
  densities on ALL seven moduli slots have IDENTICAL integrated rows on every branch
  weight while differing pointwise on every slot
  (`TF1_two_members_same_integrated_rows_differ_pointwise`). (The banked on-shell
  instance of the same separation is the Slice-2b massive locus {I_p = 0, E0 > 0}:
  integrated λ-row zero, pointwise λ-row 2E0·p0(x) ≢ 0 — cited, not re-derived.)
- **(c) Field-moduli census branch (BR-M).** δm_μ(x) ranges over the declared class
  (POSED §1.4 "field variations per fork"), which CONTAINS interior-supported
  variations — the banked record already uses them (Stage-3
  `TC1_P3_interior_defect_wall_immune`). Exact leg: the interior-supported
  v = x(1−x²)³ (v = v′ = v″ = 0 at both walls, verified) pairs with the SAME witness
  density to 64/315 > 0 at P2 exactly, and to a positive value on every anchored branch
  (integrand = 2x²(1−x)³(1+x)³ ≥ 0, zero-residual factorization; W_M > 0 banked;
  integral positivity named Category-A) — `TF1_field_direction_detects_pointwise_content`.
  With W_M invertible/positive (banked T0) and the localization closure (continuity +
  bump density — a NAMED Category-A step), ⟨𝓡, δm(x)⟩ = 0 for all declared-class δm(x)
  supplies **the pointwise rows R_μ = 0**.

**Verdict: the pre-stated crux is PROVEN.** The vanishing condition's FORM is fully
determined by the census status of the moduli directions: constants ⟹ integrated rows
(and nothing more); fields ⟹ pointwise rows. **R2 REDUCES to the census fork (BR-M,
census rows 13–14 and their (λ, k_mod) siblings 11–12).** No banked structure supplies
the extra pointwise condition on the constant branch — the eight candidate sources are
each interrogated in §2 and none does.

Stamps: all moduli sectors; LE and NV cells alike (the theorem is pairing-typing,
member-independent); GENERIC and KMOD0 strata (RES-CNEQ0 by the cited example only);
all enumerated anchored branches; jet ≤ 2 stationary presentation; off-shell.

### 1.2 The generated-row confirmation (LE cells)

For generated members the same reduction falls out of the banked H4 machinery: with the
banked BASE alphabet (NO moduli jets), the field-fork Euler operator in m of
W_F(m)·L̃(…, m) is exactly ∂_m(W_F L̃) (the m′-slot is absent — zero residual), while
the constant fork pairs the SAME density integrated; the GEN-QUAD λ-slot instance
∂_λ(e^{2λp0}L̃₀) = 2p0·W_F·L̃₀ is re-derived zero-residual
(`TF1_generated_rows_census_slaved`). The generating functional's m-variation
REPRODUCES whichever row form the census status dictates — it forces neither.

### 1.3 The F-K2 discharge record

The reduction is NOT the textbook "global parameters give integrated conditions" habit
imported: (i) the load-bearing step is the banked TANGENT-SPACE definition (§1.4 —
ℝ⁷ vs field variations), read verbatim; (ii) the integrated FORM rides the banked
enumerated representation (Stage-3 anchored-weight premise) with W_M's supplied status
stamped; (iii) the field-fork "fundamental lemma" is NOT cited bare — its applicability
is derived from the banked declared class (interior-supported variations are banked
usage), the banked W_M positivity, and ONE named Category-A closure step (continuity +
bump density), with an exact in-family witness computed
(`TF1_declared_class_localization_footing` [guard]). (iv) Both directions are
witness-backed, not asserted (checks 2, 3, 6).

## 2. TF2 — the census interrogation (does banked structure force constants vs fields?)

Full table with citations = `FORCING_LEDGER.tsv` (sources S1–S9). Summary:

| # | Source | Verdict | Core of the basis |
|---|---|---|---|
| S1 | E02 record's own typing | **FORCES-CONSTANT-ON-BANKED-FOOTING** — the field branch is a TYPED, UNREGISTERED class extension | Route B derived everything FOR constant generators; census fork (ii) verbatim: "a class extension beyond the banked footing, typed only"; BR-M NOT-EXHAUSTED. Provenance asymmetry, NOT a prohibition (`TF2_E02_record_constant_generator_typing`). **A2 adjudication (verifier-recommended, adopted):** the upstream 07-25 registration phrase "exactly seven pointwise extension parameters" (and the MAP G08 echo "7 pointwise params") is an AT-A-POINT parameter count — it decides NEITHER census branch (neither forces cell-constancy nor x-dependence); the S1 verdict rests on Route B's constant-generator derivations and the census's own fork wording, with the one banked phrase a field-branch advocate could cite named and disposed on the record |
| S2 | J07/T3 cocycle laws under m → m(x) | **PERMITS-BOTH** — composition still closes; the law does NOT break | The two-sided law IS the block-lower-triangular composition identity (zero residual, generic blocks; upper-right stays 0 for x-dependent X with fixed H — Picard); the E04 cross-member recompute shows the banked law was BUILT to absorb x-dependent effective members (member drift) (`TF2_blocktriangular_composition_is_twosided_cocycle`, `TF2_E04_crossmember_drift_absorbed_by_law`); **strengthened (verifier leg adopted, credited):** a genuinely CONTINUOUSLY x-dependent generator's Duhamel transport satisfies the two-sided law exactly over concatenated segments (`ADOPTED_xdep_duhamel_two_sided_cocycle`) |
| S3 | Mirrored-cell parity | **PERMITS-BOTH-CONDITIONAL** — an exact lever awaiting SUPPLIED data | ε_m = −1 would force the constant sector to 0 (0-jet killed at the wall) with odd fields; ε_m = +1 leaves constants free with even fields — derived exactly on the m-jet. But ε_m is NOT banked-derived: the depth mirror is not representable in-class by generator negation (−X has H-block −H ≠ H), so the mirror's moduli action is SUPPLIED seal structure; canon derives ε_φ = −1 only (`TF2_parity_jet_kill_and_constant_lever`). **Route-P candidate input (verifier-computed, adopted, credited — NOT a parity derivation):** IF the seal dressing were the banked non-Lorentz swap F, −FXF⁻¹ is in-class with derived parities λ, k_mod, k10 all odd, C → −C·F₂ (`ADOPTED_swap_dressing_parity_candidate`; the seal-dressing premise is unestablished — see the Route-P entry of `RESIDUAL_DECISION_SURFACE.md`) |
| S4 | Provenance/anchoring (R1/J04/R10) | **PERMITS-BOTH structurally; constant-only at current REGISTRATION grade** | m(x)+jets are census-typed, shift-inert, character-typed — no alphabet obstruction; but R10 defines 𝓡 on the E02 footing and the field branch is stamped beyond it: a Route-B-analog registration is REQUIRED before any response is DEFINED there (`TF2_R10_footing_field_branch_unregistered` [guard]) |
| S5 | K₄ quotient / character rule | **PERMITS-BOTH** — extends verbatim | K₄ conjugation computed on Function-valued entries: banked signed flips hold POINTWISE; ∂_x commutes with the action so moduli jets inherit the characters; all five χ_a prefactors transform pointwise (`TF2_K4_pointwise_action_and_jet_characters`) |
| S6 | J05 full tangent; J06 branches | **NEUTRAL** | J05 forbids deleted slots; both branches pair every direction; it cannot enlarge the tangent space. J06 is about determination, orthogonal to row form (`TF2_J05_J06_row_completeness_neutral` [guard]) |
| S7 | LE generated-tuple identities | **PERMITS-BOTH** — census-slaved (§1.2); with m-jets (BR-M-extended typing) the branches differ further by a wall term | ∫(pointwise row) = ∫∂_m D − [∂_{m′}D]_walls exactly on the typed instance (`TF2_mjet_extension_row_difference_wall_term`) |
| S8 | Descent gates / stratum Noether structure | **PERMITS-BOTH** — reshapes row COUNTING per branch, never the branch | Constant fork: the k_mod = 0 identity (and the cited shear example) descends to exactly ONE integrated-row dependency (constants pull out — zero residual; matches the banked TC2 count). Field fork: identities bind pointwise; x-dependent stratum loci add J09-type typed obligations (`TF2_stratum_identities_descend_to_integrated_rows`, `TF2_field_branch_stratum_crossing_typed` [guard]) |
| S9 | R12 vary/restrict order | **NEUTRAL-BY-SCOPE** — and the sharpest structural reading | The constant fork = the PULLBACK of the field-fork one-form to the constant-section submanifold (zero residual), and pullback-vanishing is strictly weaker than pointwise vanishing: the R2 fork IS the vary/restrict order question at DOMAIN level — a domain-definition question ("what ARE the moduli directions of 𝒟"), which the census deliberately types both ways; R12's binding scope is moduli strata INSIDE the typed domain (`TF2_restrict_vs_vary_pullback_correspondence`) |

**A near-miss source, addressed explicitly (verifier watch):** the H4 Helmholtz
field–moduli condition is POINTWISE in form — but it is a G3 cell-MEMBERSHIP condition
on the components of 𝓡 (self-adjointness), not an on-shell row of 𝓡 = 0; it cannot
convert the constant fork's integrated rows into pointwise equations. No other banked
pointwise structure touches the moduli ROW form.

**Census-fork verdict: OPEN at the derivable level**, with a derived two-sided shape:
(i) the ONLY branch on which the banked response object is DEFINED today is the
constant branch (S1/S4 — the E02 footing); (ii) every computed leg of the field
extension is FORM-STABLE (S2/S5/S7/S8 — cocycle, K₄, characters, generated rows,
stratum identities), i.e. the extension looks DERIVABLE, it is just UNDERIVED; (iii)
one exact conditional lever exists (S3 parity) whose input (ε_m per modulus) is
supplied, not derived. Neither branch is forced; neither is obstructed.

## 3. TF3 — the composite verdict (stamped)

Per moduli sector × cell class × pairing × stratum × census branch:

- **(λ, k_mod) sector** (trivial K₄ character; the seat scalars): **REDUCED(census:
  OPEN)**. Constant census ⟹ FORCED-INTEGRATED (∫W_M R_λ dx = 0, ∫W_M R_kmod dx = 0 —
  one scalar each per cell); field census ⟹ FORCED-POINTWISE. Stamps: LE+NV cells,
  GENERIC+KMOD0 (on KMOD0 the k_mod row joins the one-dependency bookkeeping, S8),
  all enumerated branches (P1 W_M supply open — but the banked λ-row is
  a_M-independent), jet ≤ 2, stationary presentation.
- **(k10, C) sector** (χ_a/χ_b/χ_c-graded): **REDUCED(census: OPEN)** — identically,
  with the character rule extending pointwise under promotion (S5). Same stamps.
- **Stratum-identity combinations**: KMOD0 — the identity cuts COMPONENTS pointwise
  (banked) and induces exactly one row dependency in EITHER census branch (integrated
  dependency for constants, pointwise dependency for fields) — no fork forcing;
  RES-CNEQ0 — same statement for the cited shear example ONLY; the deeper C ≠ 0
  stratification stays CENSUS-REQUIRED (inherited stamp).
- **Cell classes**: the TF1 theorem is member-independent (LE and NV alike); the S7
  confirmation is LE-only (NV has no generator — banked refusal honored).

**Outcome class: OF3** — REDUCED to the census fork; the census fork is OPEN with the
exact residual freedom handed to Charles (`RESIDUAL_DECISION_SURFACE.md`). Not OF1 (no
style is forced outright), not OF2 (the census is not derived), not OF4 (the pairing
level is settled, not open).

## 4. TF4 — the stakes restated as map facts (zero promotion)

By TF1, Slice-2b's INTEGRATED column **is** the constant-moduli census branch and its
POINTWISE column **is** the field-moduli census reading on the BASE arena (exactly as
Slice-2b labeled it). The banked theorem, restated under the reduction with its stamps
(fiberwise-quadratic p-unmixed LE class, P1-side pairings, jet ≤ 2, stationary
presentation, BASE arena, READY bin; definite sub-class where noted):

- **Constant-moduli census** ⟹ integrated λ-row 2E0·I_p = 0 ⟹ survivors
  {E0 = 0} ∪ {I_p = 0}; the massive locus {I_p = 0, E0 > 0} is NONEMPTY at every
  a_F ≠ 0 background (banked A2 + the exact in-package sign-change certificate) and
  carries nonzero mass under ALL FOUR labeled mass branches simultaneously (banked tie
  fate map).
- **Field-moduli census** (read on the BASE arena) ⟹ pointwise λ-row 2E0·p0(x) = 0 ⟹
  survivors {E0 = 0}: **massless under all four labeled mass readings** on the definite
  sub-class (constants) — at the banked no-moduli-jet response alphabet (§1.2); a
  registered BR-M response could carry moduli-jet row content (check 17) and the
  massless statement would need re-derivation there (A1 clause); on the indefinite
  sub-class nonconstant E0 = 0 members exist (banked witness — the massless statement
  is definiteness-scoped).
- P2 side (a_F′ = 0): no λ-row either way — the divergence is P1-side (banked
  pairing-relativity, full-cell general).

**The massive/massless divergence therefore attaches to the census fork** — which is
OPEN (§2/§3). This is a map fact; no census branch, pairing, or mass branch is adopted
or preferred here (F-K1/F-K4; ceiling respected).

## 5. Falsifier record (derivation-side)

- **F-K1 (merit steering): not fired — structure audit.** The interrogation order was
  fixed by the prereg source list; the constant-favoring findings (S1/S4) are verbatim
  readings of banked scope stamps, and the SAME package computes the field branch's
  form-stability on every computed leg (S2/S5/S7/S8) and the parity lever that can cut
  AGAINST constants (S3, ε_m = −1 collapses the constant sector to 0). Both sides of
  every asymmetry are stated with equal precision; the massive-branch-favoring outcome
  (FORCED-INTEGRATED) was NOT reached — the verdict is REDUCED/OPEN.
- **F-K2 (convention import): not fired** — discharge record §1.3; the localization
  step is named Category-A with banked declared-class footing, both directions
  witness-computed.
- **F-K3 (scope stamps): policed** — every forced/open/reduces claim above carries
  sector + cell + pairing + stratum + census-branch stamps; RES-CNEQ0 statements are
  example-scoped with the CENSUS-REQUIRED inheritance; the TF4 massless statement is
  definiteness-scoped.
- **F-K4 (census pre-emption): not fired** — no branch adopted; the fork goes to
  Charles with `RESIDUAL_DECISION_SURFACE.md`.
- **F-K5 (bank contradiction): none found** — recomputed banked facts matched
  everywhere (T0 guard, E04 law + drift, K₄ actions, TC2 row-dependency count, TC3
  parity kill, H4 form, λ-row integrand); the reduction is CONSISTENT with Slice-2b's
  own column labeling (it derives the labeling's content rather than contradicting it).
- **F-K6 (symbolic failure): none** — 21/21, exit 0, deterministic (rerun
  byte-identical ×3, re-verified post-amendment).

**Amendment record (this pass; `VERIFIER_REPORT.md` → `CORRECTION_LAYER.md`):** A1
(required) installed in §4 + the TF4 JSON detail + `RESIDUAL_DECISION_SURFACE.md`; A2
(recommended) implemented in §2 S1, the S1 ledger row, and the S1 guard's detail; two
verifier legs adopted as credited checks (§2 S2/S3 rows). No computed claim, no S1–S9
verdict, no TF1/TF3 verdict, and no outcome class changed by the amendments.

**Limits that travel:** (i) all computational legs at jet ≤ 2 on the registered
stationary one-parameter presentation, enumerated anchored branches; the
representation-free form of TF1(a) (codim ≤ 7) is presentation-independent, the
integrated FORM is representation-instantiated; (ii) P1 moduli-slot weights W_M remain
SUPPLIED open structure (banked) — TF1's reduction is uniform in a_M (symbolic), and
the banked λ-row is a_M-independent; (iii) the field-fork pointwise reduction uses one
named Category-A closure (continuity + bump density) on the banked declared class —
for an abstract P2 dual class narrower than that (excluding interior-supported
variations) the pointwise conclusion would weaken to the declared-class-dense
statement; that dual-class choice is itself banked-open (L7/S13); (iv) the parity
lever's input ε_m is SUPPLIED — deriving it from the seal-involution structure is a
further derivable question (TF5); (v) RES-CNEQ0 = cited example only; deeper
stratification CENSUS-REQUIRED (inherited); (vi) BR-M itself remains
TYPED-NOT-EXHAUSTED upstream — nothing here registers the field extension; the
form-stability results are legs OF the would-be registration, not the registration.
