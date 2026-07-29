# CORRECTION LAYER — P4 Route A Stage 2 (amendments A1–A3, per VERIFIER_REPORT.md)

Date: 2026-07-29. Branch: grok. Amendment agent (post-verifier), applied against the
blind verifier's verdict **PASS-WITH-REQUIRED-AMENDMENTS** (`VERIFIER_REPORT.md` §5).
A1 is SUBSTANTIVE: one load-bearing claim (the R7(b) pointwise vacuity) was REFUTED
AS STATED, with the verifier's own exact counter-computation; the refutation does NOT
overturn the outcome class (OB1 survives on corrected witnesses) but it makes the
pre-amendment parametrization a strict SUPERSET of the true ℛ_PW on a codimension-1
stratum. A2/A3 are honesty/convention amendments. Nothing here changes the outcome
class, the module bases, the slot decomposition math, the located-objects map, or
the branch stamps.

## 1. Original claims (as they stood pre-amendment)

- **R7(b) vacuity** (EXACT_DERIVATION §2; script `PW2_R7b_noether_pointwise_vacuous`;
  JSON verdict; ledger implicitly): "the pointwise Noether identity set is EMPTY —
  there is no continuous gauge direction tangent to the registered-chart
  configuration space (trivial stabilizer)… R7(b) is VACUOUSLY satisfied by every
  member of ℛ_PW at the pointwise layer."
- **STAGE3_HANDOFF gate-1 note**: "gate 4's identity input is the derived R7(b)
  pointwise VACUITY (no continuous chart-gauge identities)"; **gate-4 row**:
  "pointwise part ALREADY DISCHARGED in ℛ_PW".
- **Nonemptiness witnesses** (TB5/`PW5_verdict_nonempty_OB1`): the ω-shape AND "the
  unit trace-free screen kernel with R_kmod = 2" (constant r_tf = 1), the latter
  stated unscoped.
- **Headline count**: "53/53 zero-residual checks" with no substantive-vs-bookkeeping
  split.
- **E12 slot** (EXACT_DERIVATION §3; `PW3_screen_pairing_basis_unique`): "a NULL E12
  slot, unpaired by every δK direction" — stated without its convention scope.

## 2. Verifier findings (cited from `VERIFIER_REPORT.md`; independent artifacts
preserved in `VERIFIER_INDEPENDENT_CHECK.py`, **33/33 checks, exit 0**)

- **A1 (the §2b refutation — COMPUTATION CORRECT, INTERPRETATION REFUTED AS
  STATED).** The class-wide rank-6/empty-nullspace computation is right, but it is
  the CLASS-WIDE stabilizer; R7(b) is a PER-MEMBER identity statement. Verifier
  counter-computation (`VC_*`, `VH_*`, exact): at generic members the pointwise
  stabilizer is trivial (the claim holds GENERICALLY); on the codim-1 stratum
  **k_mod = 0** the rank drops to 5, nullspace = span(L23), with
  **[L23,X]|_{k_mod=0} = [[0,0],[J·C, k10·diag(1,−1)]] ≠ 0** — a continuous gauge
  direction tangent to the registered class (Route B's FINITE-residual enumeration
  is unaffected: the finite orbit exits the class). The induced exact pointwise
  Noether identity: **−2k10·r_tf + m00c10 + m01c11 − m10c00 − m11c01 = 0 at
  k_mod = 0** (K₄-consistent, χ_a-graded). The package's own constant trace-free
  witness (r_tf = 1) VIOLATES it (pairs to −2k10 ≠ 0); the ω-shape witness
  SATISFIES it, so **OB1 survives**. Further higher-codim resonance strata exist
  (C = 0 with λ∓k_mod ∈ {±1}, rank 5); an exhaustive enumeration was owed. The same
  generic-only gloss sits upstream (Stage-1 POSED §1.4 "mod nothing continuous";
  Route B T1 headline) — flagged for the driver.
- **Positive finding recorded WITH A1 (verifier-flagged):** the stratum identity is
  the FIRST nontrivial pointwise Noether content of the response problem, tying the
  forced trace-free slot r_tf to the mixing kernel exactly on the
  reciprocal-isotropy locus.
- **UPGRADE recorded (verifier-derived, §2a):** the anchored-exponent condition is
  forced by shift-equivariance + the banked D3 absorption ALONE — the verifier's
  orbit-space argument (invertible change of variables (φ,c_E) ↔ (φ,Q); shift
  transitive on φ, trivial on Q; d/ds F(φ+s,Q)|₀ = F_φ) proves the GENERAL exclusion,
  stronger than the package's power-family check (which proves only p = q within
  c_E^p e^{−qφ}). No V8 smuggle.
- **Confirmations:** contract-first in git (b741add); byte-identical rerun 53/53;
  character-module bases independently reproved to degree 8 + an all-degree
  Davenport-style argument; slot algebra verified (one convention note → A3);
  branch independence graded genuine; located objects verified (EH jets ≤ 2, Bach
  3/4, exclusions witnessed); jet-3/4 order-independence HOLDS including the new
  stratum identities (moduli-sector, order-independent); prose falsifier hunts
  F-B1/F-B2/F-B6 CLEAN, F-B3/F-B4 clean-with-the-A1-item.
- **A2:** ~8 of the 53 checks are bookkeeping/citation guards (list-copy equality,
  `4 > 2`, string scans) — honest in their detail strings, but the headline must
  distinguish computational checks from citation guards.
- **A3:** "E12 is a null unpaired slot" is a chart-δK pairing-convention statement;
  against the physical δ(K+Kᵀ) the pairings read (4r_tr, 4r_tf, r_sh + r_nl) — an
  isomorphic component space.

## 3. Changes made (this amendment pass)

1. **`derive_routeA_stage2.py`** —
   - `PW2_registered_stabilizer_trivial` detail relabeled CLASS-WIDE (computation
     unchanged); `PW2_R7b_noether_pointwise_vacuous` REPLACED by
     `PW2_R7b_noether_generic_vacuous_stratum_identities` (now an actual per-member
     computation at generic moduli).
   - **13 new zero-residual A1 checks** (verifier computation adopted, then
     extended): `A1_kmod0_rank_drop_all_members` (ALL 36 nonzero 6×6 minors of the
     pointwise system divisible by (k00−k11) — an all-member stratum proof, stronger
     than point checks), `A1_kmod0_nullspace_is_L23` (symbolic on the stratum),
     `A1_L23_obstruction_is_2kmod` ([L23,X](2,3) = 2k_mod is the ONLY obstruction),
     `A1_gauge_direction_tangent_nonzero`, `A1_gauge_chart_components_field_sector_zero`
     (δλ = δk10 = 0, δk_mod = −k10, δC = J·C; field sector zero on the registered
     stationary presentation, general arenas typed),
     `A1_stratum_noether_identity_form` (r_tr, r_sh, r_nl all drop out —
     r_nl-independence is new), `A1_identity_chi_a_graded_K4_consistent`,
     `A1_old_witness_violates_on_stratum`, `A1_omega_witness_satisfies_identity`,
     `A1_corrected_tracefree_witness_on_stratum` ((r_tf, m00) = (c01c10, 2k10c01):
     character-matched, satisfies the identity identically, R_kmod ≢ 0 on-stratum),
     `A1_resonance_named_strata_identities` (all four named strata: gauge directions
     + identities derived symbolically),
     `A1_resonance_identities_auto_satisfied_in_class` (χ_b/χ_c generators vanish at
     C = 0 ⟹ auto-satisfied in the declared class),
     `A1_rank_drop_confined_to_resonances` ((k00²−1)(k00−k11)(k11²−1) in the minor
     ideal via Gröbner reduction ⟹ the stratum enumeration is exhaustive at this
     level; C ≠ 0 resonance components typed).
   - **1 new A3 check**: `A3_pairing_convention_isomorphic` (pairing against
     δ(K+Kᵀ) gives (4r_tr, 4r_tf, r_sh + r_nl); convention note embedded in
     `PW3_screen_pairing_basis_unique`'s detail).
   - **A2 split**: every check carries `kind` = substantive | citation-guard (the 8
     guards: `PW1_bare_phi_excluded`, `PW4_R2_census_component_coverage`,
     `PW4_J05_full_tangent_paired`, `PW4_J13_discriminator_slots_retained`,
     `PW4_R13_no_global_entries_in_alphabet`, `PW4_functional_dimensions_per_grade`,
     `PW5_obs_EH_form_lands_in_jet2_class`, `PW5_obs_Bach_form_typed_class_only` —
     the verifier's five named + the three remaining list/arithmetic guards); stdout
     tags `[guard]`; summary/JSON report the split.
   - `PW5_verdict_nonempty_OB1` amended: on-stratum witnesses = ω-shape + the
     corrected trace-free witness (both checked against the identity); the constant
     unit trace-free kernel SCOPED off-stratum. `PW4_jet34_extension_is_alphabet_only`
     detail now carries the stratum identities as order-independent.
   - Ledger emission: R_kmod/R_C row conditions reference the cut; **two new
     STRATUM-IDENTITY constraint rows** (kmod0 = the genuine cut; resonance =
     derived + auto-satisfied + typed remainder); header stamp extended. JSON gains
     `amendments`, `check_split_A2`, `stratum_noether_identities_A1` (including the
     four resonance records and the positive observation); verdict statement, scope
     stamps, and falsifier record amended. Docstring amendment banner.
2. **`EXACT_DERIVATION.md`** — header (67/67 = 59 substantive + 8 guards; amendment
   banner); standing stamps gain the A1 "exact OFF the strata / cut ON them" stamp;
   §2 R7(b) fully restated (generic vacuity + the k_mod = 0 identity + the resonance
   strata + the K₄ grading + the field-sector scope) with the A1 OBSERVATION recorded
   (first nontrivial pointwise Noether content; one-line factual twist/angular
   cross-thread note); §3 A3 convention note; §4 parametrization CUT BY the
   identities + strict-superset note + jet-3/4 wording corrected; §5 witness record
   amended; §6 falsifier record (F-B3 slip recorded as caught-and-amended; F-B4
   upstream-gloss routing) and limits-that-travel extended.
3. **`STAGE3_HANDOFF.md`** — header amendment note; §1 lines 1–2 carry the cut and
   the stratum tie; gate-1 note corrected (must NOT assume "no continuous chart-gauge
   identities" on the strata; the no-Bianchi-TYPE warning STANDS — the stratum
   identities are algebraic pointwise, not differential); gate-2 note; gate-4 row
   corrected (discharged INCLUDING the stratum identities; gates carry the strata).
4. **`UPSTREAM_PRECISION_FLAG.md`** (NEW; DRAFT — no upstream file touched): exact
   proposed edits for the two banked glosses (Stage-1 POSED §1.4 "mod nothing
   continuous"; Route B T1 registered-class headline + its script/JSON gloss), each
   adding the class-wide-vs-per-member scope note + pointer to this package. Driver
   applies as separate visible edits.
5. **Regenerated deterministically by rerun:** `routeA_stage2_results.json`,
   `RESIDUAL_SPACE_LEDGER.tsv` (43 data rows: 36 component + 5 branch + 2
   constraint), `DERIVATION_STDOUT.txt`.
6. **Rerun record:** `python3 derive_routeA_stage2.py` → **67/67, exit 0 = 59
   substantive zero-residual checks + 8 citation guards**, < 2 s, single CPU
   process. Three consecutive runs: JSON sha256
   295ca4e88930d2d8ee8b324b9e30fcca0c9fb63d5390e3fb4dc606c50068fbdf, ledger sha256
   880108dee766584e96d44cf4d71f54aca813370579ca05379010d026ad30bd09, stdout sha256
   5eb16eceb699419973bda04731031e527c309e50d7d417fd614ead00bc346e71 — all
   byte-identical; determinism reconfirmed post-amendment.

## 4. Explicitly NOT changed (the verdict-preserving list)

- **The outcome class** — OB1 (ℛ_PW nonempty) — untouched; the verifier itself
  established OB1 survives the refutation (the ω-shape satisfies the corrected
  identity), and the amendment ADDS a second on-stratum witness.
- **The building-block alphabet (TB1)** — every block, grading, exclusion, and the
  anchored-exponent condition: byte-equivalent (the verifier UPGRADED the anchoring
  provenance — forced by shift-equivariance alone — recorded here, no change
  needed to the checks).
- **The character-module bases (TB2)** — generators, generation, minimality,
  syzygies, generic-rank-1: untouched (verifier independently reproved to degree 8 +
  all-degree).
- **The slot decomposition MATH (TB3)** — Gram, component pairings, slot theorem,
  transport laws: untouched (A3 adds a convention NOTE + one check; the component
  space is isomorphic under either convention).
- **The located-objects map (TB5)** — ω INSIDE (now also identity-checked), EH
  inside jet ≤ 2, Bach in the typed extension, CM0-C not excluded, the exclusion
  fences: untouched.
- **Branch stamps (TB4)** — six branches, BR-B/BR-C independence proofs, BR-M/BR-CE
  TYPED/NOT-EXHAUSTED: untouched.
- **Order-independence** — the structural layer remains order-independent, and the
  verifier confirmed the NEW stratum identities are themselves order-independent
  (moduli-sector, jet-blind).
- **All 52 surviving original checks — math and results unchanged** (the amendment
  REPLACED one check with its corrected per-member form and ADDED 14). PRECISE
  accounting (closure-verifier C6 nit, corrected): 40 survivors byte-equal; the 8
  guards carry only the `[guard]` relabel (content unchanged); 4 survivors
  (`PW2_registered_stabilizer_trivial`, `PW3_screen_pairing_basis_unique`,
  `PW4_jet34_extension_is_alphabet_only`, `PW5_verdict_nonempty_OB1`) carry added
  annotation TEXT only — and `PW5_verdict_nonempty_OB1` a STRENGTHENED pass
  condition — with the underlying math and results unchanged in all 52.
- **The prereg contract, the ceiling, and the F-B1 discipline** — no member
  selected, no WS/GC gate run, no physics; the maximum-conclusion ceiling stands.

## 5. ROUND 2 (closure) — the C3 defect and its fix

Date: 2026-07-29. Amendment agent, round 2, applied against the same blind
verifier's **AMENDMENT CLOSURE** pass (verdict **NEW-DEFECT**, scoped to one
A1-extension headline claim; everything else CLOSED — `VERIFIER_REPORT.md`
"AMENDMENT CLOSURE" §C1–C7; counter-computation `VERIFIER_CLOSURE_PROBE.py`).

### 5.1 The defect (C3)

The round-1 amendment's extension headline — **"the ONLY genuine new cut on the
published parametrization is the k_mod = 0 identity"** — was REFUTED. The
auto-satisfaction computation was correct as computed (every χ_b/χ_c generator
vanishes at C = 0), but it covers ONLY the four NAMED C = 0 strata, while the
resonance rank-drop locus has substantial **C ≠ 0 sub-varieties** whose identities
are NOT auto-satisfied. Closure counter-computation (probe P3/P5, adopted here as
the 8 `A1R2_*` zero-residual checks):

- the k00 = −1 slice of the minor ideal has 7 solution branches, incl.
  {c00 = c01 = 0, c10, c11 free} and {k11 = 1, c10 = −c00k10/2, c11 = −c01k10/2}
  (fully generic C ≠ 0);
- on **{λ−k_mod = −1 (k00 = −1), c00 = c01 = 0}** (codim 3, K₄-stable) the
  pointwise nullspace is 1-dim = span(L02), class-tangent, imposing the exact
  identity **−c10·r_sh − k10·m10 = 0** — it cuts the SHEAR slot (unlike the named
  C = 0 identities); χ_b-graded, K₄-consistent;
- the character-matched member R_c10 = c10 pairs to −c10·k10 ≢ 0 (a GENUINE
  further cut); the ω-shape witness ALSO violates it there;
- OB1 is NOT threatened: the corrected trace-free witness vanishes on the found
  strata, and field-sector members pair to zero with every gauge direction.

### 5.2 Provenance (the verifier's pattern note, adopted)

Per the closure verdict: this is **the same error CLASS as the original A1
refutation — a stratum-blind uniqueness gloss — one level down**. Round 1 fixed
"vacuous everywhere" into "vacuous generically + strata", then committed the same
over-claim about the strata themselves ("only cut = k_mod = 0") without checking
the C ≠ 0 sub-varieties of the resonance locus. Method observation recorded in
`AUDIT_REPORT.md`.

### 5.3 Changes made (round 2)

1. **`derive_routeA_stage2.py`** — 8 new zero-residual `A1R2_*` checks (the closure
   counter-computation adopted + the survival/coverage checks):
   `A1R2_resonance_locus_has_Cneq0_branches`, `A1R2_Cneq0_stratum_nullspace_L02`,
   `A1R2_Cneq0_stratum_shear_identity`,
   `A1R2_shear_identity_chi_b_graded_K4_consistent`, `A1R2_member_Rc10_genuine_cut`,
   `A1R2_omega_witness_violates_on_Cneq0_stratum`,
   `A1R2_corrected_witness_vanishes_on_found_strata`,
   `A1R2_field_sector_members_carry_all_strata`. Headline corrected in the two
   round-1 check details that carried it
   (`A1_resonance_identities_auto_satisfied_in_class`,
   `A1_rank_drop_confined_to_resonances`); ω-witness re-scoped in
   `A1_omega_witness_satisfies_identity`, `PW5_obs_omega_shape_in_RPW`, and
   `PW5_verdict_nonempty_OB1` (verdict condition STRENGTHENED: adds the corrected
   witness's survival of the new cut + the field-sector all-strata coverage);
   `A1_corrected_tracefree_witness_on_stratum` notes the survival. Ledger: header
   stamp corrected; resonance row re-scoped to the NAMED strata; **one new
   STRATUM-IDENTITY shear constraint row** (the C ≠ 0 sub-variety identity); R_k10
   rows reference the shear cut. JSON: `amendments.A1_R2`, corrected
   `resonance_note`, new `Cneq0_subvarieties_R2` record, corrected verdict
   statement / ω location / A1 scope stamp / F-B3 record. Docstring round-2 banner.
2. **`EXACT_DERIVATION.md`** — round-2 banner; standing A1 stamp corrected; §2
   resonance bullet corrected + a new C ≠ 0 sub-varieties bullet (full derived
   example with check names + the TYPED-NOT-EXHAUSTED stamp); §4 cut block and
   strict-superset note extended; §5 witness record re-scoped (per-witness stratum
   stamps) and the ω located-objects row scoped; §6 F-B3 (two slips), F-B5 counts,
   limits-that-travel (v) corrected.
3. **`STAGE3_HANDOFF.md`** — round-2 header note; §1 line 2 shear tie; gate-1 row
   corrected (the C3-inherited phrase replaced by the corrected statement; gates
   must carry the not-yet-enumerated deeper sub-varieties too); gate-2 and gate-4
   rows extended; §5 ω location scoped.
4. **`AUDIT_REPORT.md`** — corrected cut statement throughout (incl. the STAGE-3
   surface paragraph); verifier CLOSURE record added (C1–C7 incl. the C3 defect and
   its resolution); the pattern note quoted as a method observation; counts/hashes
   updated.
5. **`UPSTREAM_PRECISION_FLAG.md`** — resonance phrasing adjusted per the closure
   consistency note (the named C = 0 strata do NOT exhaust the resonance content);
   both proposed upstream edits otherwise kept as endorsed.
6. **§4 above** — the "52 surviving checks byte-equivalent" wording corrected to
   the precise 40/8/4 accounting (closure C6 nit).
7. **Rerun record (round 2):** `python3 derive_routeA_stage2.py` → **75/75, exit 0
   = 67 substantive zero-residual checks + 8 citation guards**, < 2 s, single CPU
   process. Three consecutive runs byte-identical: JSON sha256
   fb07909a3a668c4a164dd4185680dabda3679423f9b908b993cc01fe834a48b6, ledger sha256
   f6d4c6a277d782caa3c69f5dcea95821c9d8176cad3e2d5e9dc87b5663ea1d06, stdout sha256
   83a423c8be4777be514f7af92214c2f98b8046b9a3986c969b5e9956fb4d4e68. Ledger = 44
   data rows (36 component + 5 branch + 3 constraint).

### 5.4 Explicitly NOT changed (round 2)

- **The outcome class** — OB1 untouched (the closure verifier itself established
  OB1 is not threatened: field-sector members carry all-strata nonemptiness and
  the corrected trace-free witness survives the new cut).
- **The building-block alphabet (TB1), the character-module bases (TB2), the slot
  decomposition math (TB3), the branch stamps (TB4)** — all untouched.
- **The located-objects map (TB5)** — EH/Bach/CM0-C rows and every exclusion fence
  untouched; only the ω row gained its per-witness stratum SCOPE (an honesty
  stamp, not a relocation — ω remains INSIDE off the C ≠ 0 sub-varieties).
- **The round-1 A1 mathematics** — the k_mod = 0 identity, the all-member minor
  proof, the named-strata identities, the Gröbner codim-1 confinement, the
  corrected witness: all stand (closure C2 CLOSED); round 2 only removed the
  uniqueness gloss layered on top of them.
- **Order-independence** — the shear identity is moduli-sector and jet-blind like
  the round-1 identities; the structural layer remains order-independent.
- **The prereg contract, the ceiling, and the F-B1 discipline** — no member
  selected, no WS/GC gate run, no physics; the maximum-conclusion ceiling stands.

## Round-2 closure residue (applied by the driver, 2026-07-29)

The ROUND-2 CLOSURE verdict was CLOSED with two non-gating precision notes. N1 applied: the
"7 solution branches" phrase in EXACT_DERIVATION.md §2 now carries the verifier's parenthetical
(raw sp.solve census; irreducible-component count ~4; {k11=−1} = the k_mod=0 intersection;
nothing rides on the raw count). N2 (the OBSERVATION cross-thread note names only the screen
rotation) left as-is — harmless as scoped, per the verifier. Item 6 adjudicated by the verifier:
TYPED-NOT-EXHAUSTED is an honest resting point for the bank; the full deeper census is a
QUEUED follow-up tile, REQUIRED before adjudicating any Stage-3 candidate contacting the
resonance locus (recorded in LIVE.md).
