# BLIND VERIFIER REPORT — P4 boundary-action gate (wall-sector inverse problem)

Date: 2026-07-30. Verifier: blind adversarial verifier, **same-session-spawned**
(zero prior context supplied; worked from the package + banked sources only).
**Caveat: this is NOT a hosted external model** — it is a same-harness agent;
the independence is contextual (blind), not infrastructural.
Independent script: `VERIFIER_INDEPENDENT_CHECK.py` (this package; own layout,
own IBP, own symmetrization construction; 31/31 pass, exit 0, < 1 s CPU).
Target: `derive_boundary_action.py` + `EXACT_DERIVATION.md` +
`WALL_RESPONSE_LEDGER.tsv` + `boundary_action_results.json` +
`DECISION_SURFACE_UPDATE.md` under the frozen `PREREGISTRATION.md` (da29fa0).

## VERDICT: **PASS-WITH-REQUIRED-AMENDMENTS** (AM-V1, AM-V2 below)

The OW2 family verdict, the per-candidate germ laws, the R6 cut, the fold
forcing, the glue pin + flux-seal equivalence, the mirror-wall theorem, the
open-end laws, the D-b non-independence, and all consistency reproductions
were independently re-derived and are CORRECT. No falsifier fired. Two
phrasing-level overclaims require amendment; neither changes the verdict class.

## Duty 0 — rerun / reproducibility / contract-first / forbidden content

- **Contract-first VERIFIED in git**: da29fa0 (2026-07-30 20:26) commits
  `PREREGISTRATION.md` + LIVE.md ONLY; every derivation artifact postdates it
  (mtimes 20:40–20:43).
- **Rerun**: exit 0; **57/57 = 49 SUBSTANTIVE + 8 GUARD** (split audited by
  name: guards = 4 banked-momentum re-runs S0a, 1 citation row S0f, 1
  construction sanity `TW3_WREG_density_parity_even`, 2 trivial-arithmetic
  TW5d rows — honest; if anything the S0a rows are under-billed as guards).
- **Byte-identical**: stdout across two reruns AND against the committed
  `DERIVATION_STDOUT.txt`; regenerated `boundary_action_results.json`
  byte-identical to committed. Pure SymPy, no floats/numeric solvers/GPU,
  single process, ~0.5 s.
- **Forbidden-content grep clean**: no x_max, no anchor values (c_E, q, Z,
  ρ_s symbolic throughout), no G18/fold assumption (fold enters only as an
  interrogated candidate), no census/pairing adoption (branch symbol a_F
  generic; the five branches enter only through W_F ≠ 0).

## Duties 1–9 — independent re-derivations (all on my own layout)

1. **Selector hunt (F-B1, attacked the landed no-selection direction
   hardest).** I imposed the remaining banked requirements myself: **R9** =
   global periods, banked class GC (`POSED_INVERSE_PROBLEM.md` :197; on
   K₄-torsion cycles provably VACUOUS for closed forms per the banked V8
   note; live content = completion-class / J07/J11 cocycle cycles — exactly
   what the package types OPEN); **R13** = no fitted global average as local
   coupling — argument/provenance-level, cannot pin the germ FUNCTION;
   **K₄ character** — trivial on wall directions (banked), argument-level;
   **J07/J08** — banked as typing requirements, discharged by the 𝔠-argument
   + per-stratum typing; **N=4** — a genuinely new derivation (2-jet natural
   BCs), prereg-sanctioned deferral, and the package CORRECTLY scopes the
   crease kill to N=2 (at N=4 a ρ″-germ would survive parity — the
   EXTENSION-REQUIRED stamp travels). **No banked-derivable selector was
   missed**; a further GC cut can only shrink the open-end germ family (the
   fold/glue results are PW-rigid downward). The headline "B has NO
   candidate-selecting content" is correctly stamped "at N=2" everywhere I
   checked. NOT refuted.
2. **Inert-germ theorem** — re-derived on a fully generic `sp.Function` (no
   expansion ansatz): first variation at the seam = first partials at the
   realized point exactly (V2a); a pure ≥2nd-germ perturbation is inert there
   (V2b). **BUT my probe V2c certifies the inertness is GERM-LOCAL**: the
   same perturbation has nonzero active content at a different realized trace
   ρ₁ ≠ ρ_s (residual 3(ρ₁−ρ_s)²) → AM-V2.
3. **R6 unpaired-jet cut** — own IBP (V1a/V1b): the N=2 boundary residue is
   (∂L/∂u′)·v — contains v, never v′ — so a 1-jet B-argument injects an
   unpaired δρ′ term; forced to vanish. Weight-robustness confirmed
   (W_F = e^{a_F p0} never zero; V1c). CORRECT.
4. **Crease-cannot-carry-action** — re-derived: doubled momentum
   −8cosh(2φ)ρ′ from L_P + flipped copy (V3a; matches banked seam pkg :278);
   branch-uniform at the φ=0 locus (V3b — my own check, G-interior gives the
   same −8ρ′ there); δφ essential (V3c); joint forcing 𝔅_ρ = 0 (V3d); the
   even-part slope-kill re-derived symbolically (V3e). The DERIVATION is
   sound. **The FRAMING against the banked conditional-fold theorem is a
   cousin-premise conflation** → AM-V1 (the exact-wording check the task
   demands FAILS as stated; the package's own parenthetical concedes it).
5. **Flux-seal ⟺ 𝔅_Q = 0** — both directions re-derived (V4b/V4c) on the
   jump law [π_φ] = −c_E𝔅_Q (V4a), c_E > 0. CORRECT.
6. **Mirror-wall theorem** — re-derived by SYMMETRIZATION (strictly more
   general than the package's invariant construction): generic degree-4
   polynomial density in all six jets, even part under (p0,f1,h1) → −(…);
   π_f, π_h vanish identically at the kill locus (V5a/V5b), π_p generic
   nonzero with its variation essential-killed (V5c); the UN-symmetrized
   generic density fails the kill (V5d) — the mirror-compatibility stamp is
   genuinely load-bearing. CORRECT and robust beyond the polynomial class
   (even function ⇒ odd-derivative vanishes at the symmetric point).
7. **D-b non-independence + open-end laws** — re-derived: fold
   ρ′_s = −𝔅_ρ/8 → 0 forced; open-end ρ′_s = −𝔅_ρ/4, q = −c_E𝔅_Q; the
   (β₁, β₂) germ plane realizes ANY (q, ρ′_s) (V6d, V8a/V8b). CORRECT.
   The banked K6d q=0 forcing re-derives exactly as the germ-flat stratum
   (V6c) — the "generalized, banked leg reproduced as stratum" reading holds.
8. **Consistency reproductions spot-checked at source** (> 3): K6c
   B′(ρ_s)=q/2 (seam pkg EXACT_DERIVATION :180); K6d q=0 ∧ ρ′=0 (:186); K4d
   (:137); K4g ρ′ free (:141); ΔΠ = q/2 weld jump (banked-in-use, cited);
   TS1/S1f handshake germs (V7d/V7e); M-WALL = a_F·M-GEN re-derived
   independently on the quadratic class (V7c) and matched to Slice-2b (:187);
   M19 row read VERBATIM ("Complete differentiable finite-cell boundary
   action and normalized gravitational charge remain open — OPEN") — the
   in-package citation is exact.
9. **Mid-run bug fix audited**: the original `TW5c` coding tested parity
   about the cell CENTER — a genuinely WRONG premise (odd-about-center
   leaves f = βx alive, so the check rightly failed); the final per-wall
   form (even ⇒ 1-jet zero at each wall; odd ⇒ 0-jet zero at each wall) is
   the banked gradient-seat form and is STRONGER (kills α and β). The fix
   corrected the premise, did not weaken any condition. CLEAN.

## Duty 10 — falsifier hunts

- **F-B3 (hunted FIRST)**: full stamps present and consistent across all
  three surfaces — ledger (dedicated columns incl. ε_φ-DEFINITIONAL per row),
  JSON (`stamps` block, 6 keys), prose (stamps block at head + per-claim).
  No unstamped claim found. NOT fired.
- **F-B1**: see duty 1. The landed family verdict survived my selector hunt;
  the fold/glue rigidity legs got equal attack (their premise stamps —
  ε_φ-definitional, banked mirror jets, banked-in-use ΔΠ=q/2 — are carried
  in limits (vi)/(vii)); the in-package pin-hunt record is accurate against
  the banked sources I read. NOT fired.
- **F-B2 (Tonti scar)**: B enters as `sp.Function` / generic germ expansion;
  witnesses ((q/2)ρ, β-plane) are used ONLY for nonemptiness/realization,
  never as adopted functionals; well-posedness is used only to CONSTRAIN with
  both readings stated. NOT fired.
- **F-B4**: not fired (see duty 0 grep).
- **F-B5**: the one-way typing (pairing supplies slots → B an element) is
  declared in the stamps AND matches the actual script structure (S0c/TW2f
  supply the slot census; B never feeds the pairing). NOT fired.
- **F-B6**: no bank contradiction found; every reproduction zero-residual at
  source. NOT fired.
- **F-B7**: none (57/57; my 31/31; the one independent-check failure during
  my own run was MY cosh-canonicalization coding bug, fixed — the package
  identity is exact).

## Duty 11 — contract compliance

TW1–TW5 all delivered (census C01–C14; parametrization + 4 structural
theorems; per-candidate cut with K6 re-derived not assumed; verdict table
V01–V06; decision surface). Full declared scope run (no scope-ladder
reduction). J07/J08 "imposed exactly" is discharged BY TYPING — consistent
with their banked class (typing/GC requirements) and stamped in limits (iv);
observed compliant, noted for the record. Ceiling respected: no closure /
census / pairing adopted, no law crowned, the G18 update is a PROPOSAL with
"Charles rules" explicit. `AUDIT_REPORT.md` correctly absent at this
pre-verifier stage (method §5 sequences it after this report).

## REQUIRED AMENDMENTS

- **AM-V1 (cousin-premise conflation in the fold-premise framing).** The
  banked conditional-fold theorem's premise (seam pkg, verbatim) — "{no seam
  surface term (⇒ WE C¹ matching)} ∧ {Branch-G on BOTH sides} ∧ {ρ′(r_s)=0}
  ⇒ fold FORCED" — operates in the TWO-SIDED matching problem, BEFORE any
  fold is concluded. The new result is POSTURE-CONDITIONAL: GIVEN the
  quotient posture, no active wall action is admissible at N=2. That derives
  a COUSIN of the premise (no active action ON the crease), not the
  theorem's premise itself — which the package's own parenthetical concedes
  ("the two-sided version … still carries it"). REQUIRED: (a) in
  `EXACT_DERIVATION.md` TW5 bullet (iii), delete/rephrase "the premise set
  of the banked forcing theorem loses one independent member AT THE CREASE"
  — the forcing theorem's premise set loses NO member; (b) in
  `DECISION_SURFACE_UPDATE.md` G18 bullet 1, rephrase "the
  conditional-forces-fold premise 'no seam surface term' is now FORCED …"
  to the posture-conditional form (e.g. "the fold POSTURE is
  self-consistent: it cannot carry an active wall action at N=2, so within
  that posture the no-surface-term condition is automatic; the forcing
  theorem's two-sided premise is untouched"); same for "ρ′_s = 0 …
  automatic at the crease" (posture-conditional). The G18 truth-value
  reduction (posture ∧ Branch-G) survives unchanged under this rephrase.
- **AM-V2 (germ-locality scope on inertness/uniqueness).** Certified by my
  V2c: higher germ content is inert AT THE REALIZED TRACE POINT ONLY (a
  (ρ−ρ_s)³ perturbation has active content 3(ρ₁−ρ_s)² at a different
  realized trace ρ₁). REQUIRED: the flat statements "all higher germ content
  variationally INERT", "two members differing beyond the first germ give
  IDENTICAL stationarity conditions", and the two "effectively UNIQUE" rows
  (V01, V04) must carry "at the realized seam germ / per realized
  configuration" (TW2 item 2 already carries it; TW4 prose and ledger rows
  do not). The open-end "2 germ FUNCTIONS" count already embodies the
  function-level freedom and needs no change; the OW2 verdict is unaffected.

## Minor notes (no amendment required)

- "The exact N=2 form of the banked BDY-TD nonuniqueness" is an interpretive
  analogy: M19/BDY-TD is momentum/primitive-shifting total-derivative
  freedom; the inert germs shift nothing at the realized point (closer to
  primitive nonuniqueness). Flagged as gloss, not load-bearing.
- Several SUBSTANTIVE checks are algebraically thin reproductions
  (`TW3_glue_reproduces_K6c` solves 𝔅_ρ = q/2 for 𝔅_ρ); their load-bearing
  content lives in the jump laws + banked values, which I verified
  independently. Honest but worth knowing when reading "49 substantive".

Verdict repeated: **PASS-WITH-REQUIRED-AMENDMENTS (AM-V1, AM-V2)** — the
derivations are correct and reproducible; the two amendments are
framing/scope corrections that do not change the OW2 outcome class, the
per-candidate table, or the no-selection-at-N=2 adjudication.

Not committed (per instruction; driver banks after amendments).

---

# AMENDMENT CLOSURE (same verifier, second round — 2026-07-30)

## VERDICT: **CLOSED**

Adjudicated adversarially (attack, not confirm) against the amended package.
Same-session-spawned blind verifier; not a hosted external model (caveat
travels).

**1. Rerun (adjudicated PASS).** Three consecutive runs: exit 0 each,
byte-identical stdout AND JSON across all three and against the committed
`DERIVATION_STDOUT.txt` / `boundary_action_results.json`; sha256 of both
committed artifacts match `CORRECTION_LAYER.md` §3.6 exactly (dcd8dbe3…,
a9d2f4cc…). **64/64 = 55 SUBSTANTIVE + 9 GUARD; 7 verifier-credited**, split
verified by name: 49 original substantive + AMV2a/AMV2b + AMV3a–d; 8 original
guards + `AMV1_cousin_premise_distinction_note` (honestly a GUARD — a
cited-argument row, non-computational). **All 57 pre-amendment computations
survive UNALTERED**: stdout PASS-lines (name, kind, detail) byte-identical to
the pre-amendment run after stripping only the new `[verifier-credited]` tag
plumbing; all 57 JSON check rows (kind/passed/detail) compare EQUAL
field-by-field; zero relabeled. **Credited-check fidelity:** AMV2a/b reproduce
my V2c exactly (the (Q−c_E)²(ρ−ρ_s)+(ρ−ρ_s)³ perturbation; zero-residual
against 3(ρ₁−ρ_s)²; certified nonzero off-trace); AMV3a–d reproduce my V5
symmetrization construction faithfully (generic degree-4 polynomial in all six
jets, even part under (p0,f1,h1)→−(…), kill locus, π_p generic-nonzero,
un-symmetrized failure witness).

**2. AM-V1 (adjudicated IMPLEMENTED).** The posture-conditional restatement is
present and correct at every occurrence: `EXACT_DERIVATION.md` TW5(iii)
(verbatim posture-conditional form with the cousin-distinction and "loses ZERO
members"), the TW3 fold paragraph (posture-conditional stamp + premise
bookkeeping citing `AMV1`), the F-B6 sweep, the amendment banner, limits
(i-c); `DECISION_SURFACE_UPDATE.md` G18 bullets 1–2 (with "loses ZERO
members" AND "the G18 reduction (posture ∧ Branch-G ∧ germ data) survives the
amendment unchanged" both explicit; ρ′_s = 0 stated posture-conditional) and
the lay verdict restated conditionally ("IF the seam is a mirrored crease…");
ledger V01 carries the [AM-V1] stamp; the JSON G18 text restated. **Grep
adjudication:** the old "now FORCED / not assumed / loses one independent
member" phrasing survives ONLY inside `CORRECTION_LAYER.md` §1 — quotations of
the pre-amendment text in the correction record, as permitted. (The
`AUDIT_REPORT.md` line 75 "K6 re-derived not assumed" is the contract's own
TW3 wording about K6 re-derivation, not the premise-loss claim — a false grep
positive, inspected and cleared.)

**3. AM-V2 + minors (adjudicated IMPLEMENTED).** Germ-locality scope present
at `EXACT_DERIVATION.md` TW2 item 2, the TW4 nonuniqueness prose AND the TW4
per-candidate table (fold + glue rows), the glue paragraph, the three-way
honesty block, limits (i-b); ledger P02/V01/V04; DSU D-a row; JSON
`active_content` + `per_candidate`. The BDY-TD gloss is softened to
analogy-not-identification at every occurrence found (TW2 item 2, P02, DSU
D-a row, JSON). "OW2 unaffected" stated explicitly (banner, ledger
AMEND-2026-07-30 row, CORRECTION_LAYER §4). The J07/J08 discharge-by-typing
note is present in-prose (TW3 contract note), in-JSON, and in AUDIT_REPORT.
The mirror-wall theorem is marked DOUBLY PROVEN (ledger V02 + prose) with the
symmetrization credited.

**4. CORRECTION_LAYER / AUDIT_REPORT (adjudicated FAITHFUL).** The §4
did-NOT-change list verified BY COMPARISON: the OW2 composite, the C01–C14
census, the TW2 parametrization + R6 cut, the crease derivation itself (all
four fold checks byte-identical), the glue pin + flux-seal equivalence, the
mirror-wall theorem, the open-end laws, the D-b dependence, and all six
consistency reproductions are computationally untouched (the JSON row-diff is
EMPTY on the original 57; prose diffs are confined to banners, scope stamps,
the AM-V1 rewrites, credited-hunt citations, and limits additions — no claim
silently dropped or strengthened). `AUDIT_REPORT.md` is faithful to my round-1
findings on every named item: contract-first at da29fa0, the 31/31
independent artifact, the selector hunt credited WITH its per-requirement
record (R9/GC + torsion-vacuity, R13, K₄, J07/J08, N=4), the N=4 ρ″-germ note
(now also in limits (1)), both over-claim cuts memorialized as
exciting-direction catches, and the AM-V1/AM-V2 dispositions stated exactly.
It also honestly records that this same-verifier closure was OWED — this
section discharges it.

**No new defect found.** The amendment pass changed framing and scope only,
exactly as required; nothing was weakened, nothing new was claimed beyond the
credited checks (which are my own computations, adopted faithfully).

Verdict repeated: **CLOSED** — PASS-WITH-REQUIRED-AMENDMENTS is discharged;
the package stands at VERIFIED-WITH-AMENDMENT with OW2 and the
no-selection-at-N=2 headline intact, fully scoped. Not committed (per
instruction; driver banks).
