# ADVERSARIAL REVIEW 2 — classification / steer / scope (Step 3)

Reviewer: blind adversarial pass (classification review per PREREGISTRATION.md §Method).
Date: 2026-08-06. Inputs: PREREGISTRATION.md (frozen), DERIVATION_NOTES.md, step3_checks.py
(re-run independently: 13/13 PASS, exit 0, sympy-exact, no data file touched), Step-2
consolidated notes + amended table, Step-1/regrade package, MAP, CANON.md (C-2026-07-02-1,
C-2026-08-06-1/2 read at source), WR-L seat citations read at source
(`simple_metric_L_native_optical_derive_results.md:72`, `simple_metric_DA_native_derive.md:55,69,80`),
G18 at source (C-2026-07-30-1 split-and-keep; re-grade proposal pending, P4_ARC_SUMMARY:85).
Scope of this review: classification honesty, steer (F-STEER both heads), scope/rail
hygiene, prominence. Algebra is review 1's; two classification-relevant structural catches
below are flagged TO review 1 / next step, not independently derived to bank grade.

**VERDICT: SUSTAINED — AMENDED. S3-MIXED stands as the outcome class; four amendments.**

---

## 1. Is S3-MIXED the honest class? YES — but two cells are mis-graded inside it.

**1a. S3-FOLD-STRUCK verbatim is correctly NOT assigned.** Its frozen definition carries an
entailment rider — "within S+D1, glue is sole survivor" — that did NOT land: §Q3c.1's
outer-closure-blindness makes glue-as-admitted equally struck/conditional at low z, and the
sole D1-consistent row rides the free-core fork, OUTSIDE both admitted classes. Assigning
FOLD-STRUCK would smuggle a false glue-survives claim. S3-MIXED ("per the table; all
first-class") is the honest bin. SUSTAINED.

**1b. AMENDMENT A1 — fold × off-core D1-lin: CONDITIONAL is too generous; the honest grade
is STRUCK-in-effect (rescue named-but-dead at leading order).** Adjudication of the rail's
line, as tasked:

- The prereg's own class taxonomy already drew the line: S3-FOLD-VIABLE(cond) contemplated
  "off-core seat with BOUNDED anisotropy"; S3-FOLD-STRUCK contemplated "anisotropy or other
  exact obstruction off-core." The derivation itself settles which side this lands on: the
  dipole is the ENTIRE leading signal, dipole/monopole → ∞ as d → 0, half the sky
  blueshifted at leading order, sky-mean law quadratic (C3b, re-verified). The anisotropy is
  UNBOUNDED in the only structural sense available. The prereg's named viability condition
  is therefore REFUTED by the step's own exact result — the notes derive this and then
  decline to apply it to the grade.
- **F-DATA adjudication (the "no half-sky blueshift is observed" question):** F-DATA as
  frozen fires on "numerical fit / chi2 / data-file touch." D1 is a PREREGISTERED, GRADED
  datum ("the LOW-Z LINEAR Hubble law (model-independent)"), and Step 3's frozen mandate is
  to "adjudicate ... against DATA, with the data GRADED." Reading D1's qualitative content —
  the observed low-z law is linear in the sky-mean AND positive-z in all directions; it is
  not a half-sky-blueshift pure dipole with a quadratic mean — is a structural
  characterization against the preregistered datum, exactly the step's job. It is NOT a new
  data touch, fit, or quantification (Q3b's "do not quantify against sky data" is obeyed:
  no amplitude, no statistic, no file). RULING: citing that fact is LEGITIMATE, with one
  duty — it is a one-inference-step READING of D1's content and must be tagged as such,
  symmetric with how the Q3a canon pin was tagged. The line: preregistered-datum qualitative
  content = usable; any numerical sky statistic, fit, or file = F-DATA.
- Under EITHER available reading of D1 (sky-mean linearity; or per-direction linear with
  positive z both hemispheres) the off-core pairing fails at leading order: the mean is
  quadratic, and half the sky is blueshifted. The only reading that survives —
  "anisotropic directional linearity, sign disregarded" — is not a rescue of D1 but a
  replacement of it. Grade the cell: **STRUCK-in-effect; rescue named-but-dead** (named:
  anisotropic-linear reading; dead: refutes the prereg's own bounded-anisotropy condition
  and D1's qualitative content). Same amendment carries to glue × off-core (identical cell).
- Steer note (F-STEER head 1): the notes' conservatism here is fold-FAVORABLE — the
  canon-flavored class was left "conditional" when the step's own exact result kills the
  named rescue. That is the direction F-STEER head 1 watches. The amendment goes AGAINST
  the owner-favorable class and is forced by the derivation, not by taste.

**1c. AMENDMENT A2 — the free-core fork's presentation: "fold gives at BOTH ends" is
correct ONLY as scoped, and a combination is UNCOVERED.**

- As written, resolution 2 conditions "both ends" on keeping the L/SNe structure WHOLE
  (D1-lin + z(z+2)). Under φ_L the outer strike is exact and seat-independent (Step-2
  §I.4(ii): ρ' = 0 impossible anywhere ⇒ the fold's seam ρ-pin unsatisfiable). So scoped,
  the sentence is accurate. BUT:
- **The outer-end strike rides the z(z+2) ⇒ φ_L identification, whose in-cell d_L readout
  is exactly what R-a/R-b leave OPEN** (ρ₊ ≠ r [C5]; no areal center, D_A = r
  seat-conditional and unavailable in-cell [C6]). If the in-cell D_A modifies the d_L
  shape, the profile matching SNe in-cell need not be φ_L, and the outer strike does not
  transfer. Caveat 7 names this link; the tension-resolution text does not carry it. The
  honest statement: **D1-linearity alone pressures only the SEAT / inner end (low-z
  structure is outer-closure-blind — the notes' own §Q3c.1, applied symmetrically); the
  fold's OUTER seam is struck only through the L-identification, which is conditional on
  the open in-cell D_A.**
- **Coverage gap (answering the tasked question directly): a free-core-inner × odd-fold-OUTER
  cell is NOT covered by Step 2's classes** (both 𝒜_fold and 𝒜_glue bake in the even-core
  inner end; Step 3's row 5 pairs the fork with glue only, justified via φ_L — which is the
  conditional leg above). For non-L profiles, nothing exhibited forbids φ'(inner seat) ≠ 0
  with ρ'(r_s) = 0 at an outer fold (the flux identity permits Φ(r_in) ≠ 0 with no inner
  pin). So on the record as it stands, **the fold is NOT shown struck at both ends
  unconditionally; the unconditional D1 pressure is seat-side.** The assembly table and any
  quotation of "fold gives at both ends" must carry this scope. (This does NOT rescue the
  fold within the admitted classes — rows 1-4 stand — it bounds what the fork's existence
  implies about the outer closure.)

**1d. AMENDMENT A3 — row 5's D1-lin grade "STRUCTURALLY-CONSISTENT (isotropic linear)" is
chart-level and should be CONDITIONAL, like its shape column.** The linear onset in proper
d carries exactly (shared g_tt, g_rr — sound). The ISOTROPY does not yet: the banked
isotropy argument lives in the chart where the observer sits at an areal center (rays
converge at a point, D_A = r derivation, DA_native §1) — and the step's own R-b shows no
areal center is S-available even under the fork (u₊(0) finite ⇒ ρ(0) > 0). At a seat with
ρ(seat) > 0 and φ'(seat) ≠ 0 the §Q3b.2 static-readout argument generically produces the
same leading-order direction dependence (tangential Δφ = 0 at equal r). Whether the fork's
inner-end geometry evades this is precisely the OPEN in-cell question. So row 5 currently
enjoys an asymmetric grading: its shape column carries the R-a/R-b conditionality, its
linearity column silently keeps the chart-level isotropy. Grade both CONDITIONAL on the
in-cell derivation; strike the sentence "the ONLY row with an unconditional D1-lin pass"
(it contradicts the row's own residues). FLAGGED to review 1 / Step 4 for the exact
in-cell statement — classification impact is only the label, and it is load-bearing for
how clean the "sole survivor" looks. Consequence, stated plainly: **on the current record
NO row — admitted or forked — carries isotropic linear D1 in-cell unconditionally; the
WR-L story survives at chart level only.** This deepens, not weakens, S3-MIXED, and it
transfers weight onto the seat-conflict finding (§2 below).

**1e. Minor (to review 1):** §Q3b.1's "ISOTROPIC" at the core seat is loose — sign and
onset-order are direction-independent, but the quartic coefficient carries the direction
(δr ~ d cosθ ⇒ ~cos⁴θ). No verdict rides on it (struck in every direction regardless).
Also the exact z ≡ 0 shell for flat-segment seats (r_obs < r*) is itself a qualitative
D1 tension worth one line in the table row — it reinforces the core-seat strike.

## 2. The seat question's provenance — GENUINE RECORD-INCONSISTENCY; PROMINENCE INSUFFICIENT.

- The Q3a pin is honestly derived and honestly tagged: C-2026-07-02-1 states
  Δφ = φ(CMB fold) − φ(core) with 1+z = e^{Δφ} (verified at source, CANON.md:235-245); the
  static readout then pins φ(obs) = φ(core) in ONE inference step, and the notes tag it so
  (caveat 4). Correct handling.
- The WR-L seat is equally banked at source: observer at chart origin, φ(0) = 0, relational
  seat (verified at both cited lines), with φ_L'(0) = 1/(2X) ≠ 0. The φ-shift is absorbable
  (Step-2 C3); φ' at the seat is not. **Two banked pictures place the SAME physical observer
  in incompatible forced local germs (dφ/dℓ = 0 vs ≠ 0). That is a genuine banked-record
  inconsistency, not a citation ambiguity — ADJUDICATED AS SUCH.**
- And it is arguably the step's most consequential output, because Step 3's central
  technical finding (low-z structure is SEAT-determined and outer-closure-blind) means D1
  discriminates between the two banked PICTURES — the single-round-cell picture (whose
  forced φ-floor seat starts at d⁴, and whose off-floor seats carry the dead dipole) and
  the relational/WR-L picture (each observer at their own chart origin; isotropic linear +
  z(z+2) at chart level) — MORE than it discriminates fold vs glue. The fork, the seat
  conflict, and rows 1-4 are three faces of the same fact.
- Prominence as landed: the conflict lives inside §Q3a and caveat 4 only. It is ABSENT from
  the landed-outcome section, the one-line, and any named flag. **AMENDMENT A4: raise a
  named RECORD-SEAT-CONFLICT flag, co-equal with the G18-pressure flag, on Charles's desk.**
  Suggested wording: "Two banked pictures, incompatible observer germs: the canon anchor's
  readout form pins the receiver to the φ-floor (φ' = 0, forced); the banked WR-L seat is
  the chart origin with φ' = 1/(2X) ≠ 0. D1 adjudicates between the pictures; no banked
  record adjudicates between the seats. Record-inconsistency finding; Charles's ruling or a
  derivation (in-cell D_A / fork geometry) is required before any seat is used as an input
  again."

## 3. Scope / steer / rail hygiene — CLEAN, with the items above.

- **F-DATA: CLEAN.** Independent re-run: 13/13 PASS, exit 0; script inspected — sympy only,
  no floats beyond the labeled series bookkeeping, no data file, no fit, no chi2. The
  notes even under-use the permitted qualitative D1 content (§1b) — the rail line is drawn
  in §1b for the record.
- **S-caveat:** header verbatim + by-reference in every table cell; travels. CLEAN.
- **G18:** flag-not-ruling respected throughout ("CANON-ADJACENT ... NO ruling here" at
  every occurrence; checked against C-2026-07-30-1's split and the pending re-grade
  proposal). CLEAN. The flag is properly two-legged after A2: seat-side pressure
  (unconditional, within admitted classes) + outer-seam pressure (conditional on the
  L-identification / open D_A).
- **D3:** never decisive — only "conditional(-consistent)" cells; never used to strike or
  save. CLEAN. Note for the table: row 2/4's D3 cell rightly records the canon-equality
  break as a COST of the off-core seat; after A1 that row is dead anyway.
- **C5/C6 residues (R-a/R-b):** properly labeled LEAD/UNBANKED, "found here, offered to
  review," conditioning-not-voiding. CLEAN — indeed they are the step's best self-audit;
  A3 simply applies them symmetrically.
- **Measure hygiene:** the 08-06 no-silent-substitution lesson is honored (proper d
  primary; chart/areal conversions printed; areal rejected as observer-distance with the
  banked ρ_c > 0 reason). CLEAN.
- **Over-deflation check (F-STEER head 2):** the restored off-core linearity and the fork
  row ARE reported with full force; no material over-deflation found. The two grading
  errors found run in OPPOSITE directions (fold left too alive in row 2; row 5 left too
  clean), which is the signature of grade-by-cell drift, not directional steer. The
  "unconditional D1-lin pass" sentence is the single over-claim (A3).

## 4. The map handoff — exact text proposed for the assembly-table rows.

**ROW 4 (Step 3, Q2 discrimination):** "Within S + the source-doc cell geometry, low-z
structure is SEAT- and INNER-END-determined and OUTER-CLOSURE-BLIND (fold vs glue
undiscriminated at low z). Every forced φ'=0 seat starts z at d⁴ (exact; no linear, no
quadratic term); every φ'≠0 seat restores directional linearity only with an exact
leading-order dipole (half-sky blueshift; sky-mean quadratic) — the prereg's
bounded-anisotropy rescue is refuted, so BOTH admitted closures fail D1 at every seat
(rescue named-but-dead). The lone D1-consistent structure is the WR-L germ: chart-level
exact (z(z+2), H_* = 1/(2X)) but outside both admitted classes (free-core fork) and
conditional in-cell on two named residues (ρ₊ ≠ r; no areal center ⇒ in-cell D_A AND seat
isotropy underived). Class S3-MIXED (amended per review 2). Flags: G18-pressure
(CANON-ADJACENT, no ruling) + RECORD-SEAT-CONFLICT. Coverage gap logged: free-core-inner ×
fold-outer not enumerated by Step 2; 'fold gives at both ends' is scoped to keeping the
L/SNe structure whole and its outer-end leg is conditional on the L-identification."

**ROW 5 (desk items for Charles, in order of consequence):**
1. **RECORD-SEAT-CONFLICT flag (new, this step):** two banked pictures, incompatible
   observer germs (§2 wording). D1 discriminates between the PICTURES; ruling or the
   in-cell derivation needed before any seat is re-used as an input.
2. **G18-pressure flag:** the ratified fold closure is under D1 pressure (seat-side
   unconditional within the admitted classes; outer-seam conditional). Activates the
   pending 07-30 re-grade proposal per MAP CP2. Flag only; no ruling here.
3. **Free-core fork ELEVATED:** from "a fork, not a finding" (Step 2) to the record's only
   load-bearing D1 rescue. The decisive bounded derivation is named and open: the IN-CELL
   D_A (and seat isotropy) under the fork — R-a/R-b make it well-posed. Natural Step-4
   item alongside the mapped x_max seat report (Q3) and matter-seat naming (Q4); note the
   fork and the x_max/relational reading are entangled through the seat conflict.
4. **Step-2 coverage gap:** enumerate the free-core-inner × {fold, glue, open, partner}
   outer combinations before any "struck at both ends" is quoted unconditionally.

## Verdict

**SUSTAINED — AMENDED.** Outcome class: **S3-MIXED** (correctly not S3-FOLD-STRUCK — its
glue-sole-survivor rider is false on this record; correctly not S3-FOLD-VIABLE(cond) — the
sole named rescue fails the prereg's own boundedness condition). Amendments: **A1**
fold/glue × off-core D1-lin re-graded CONDITIONAL → STRUCK-in-effect (rescue
named-but-dead; the qualitative-D1 reading is legitimate and rail-clean, tagged as one
inference step); **A2** "fold gives at BOTH ends" scoped — outer-end leg conditional on the
z(z+2) ⇒ φ_L identification (open in-cell D_A); free-core × fold-outer logged as uncovered;
**A3** row 5 D1-lin re-graded CONDITIONAL (chart-level isotropy; R-b applies symmetrically;
"unconditional pass" sentence struck) — leaving NO row unconditionally D1-clean in-cell;
**A4** the seat conflict promoted to a named co-equal flag (RECORD-SEAT-CONFLICT) — the
step's most consequential output. Rails: F-DATA clean (re-run 13/13), S-caveat travels,
G18 flag-only, D3 never decisive, C5/C6 properly LEAD/UNBANKED. Nothing committed by this
reviewer; same-session review caveat applies — the external bar is still owed for any bank.
