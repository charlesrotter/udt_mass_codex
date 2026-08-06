# ADVERSARIAL REVIEW 2 — classification / steer / overstatement

Date: 2026-08-06. Branch: grok. Reviewer: independent adversarial agent (review two of two per
`PREREGISTRATION.md`: "classification/steer + does the discriminator reading overstate").
Inputs read at source: `PREREGISTRATION.md`, `REGRADE_REPORT.md`, `verify_regrade_r1_fresh.py` +
`R1_STDOUT.txt`, `udt_global_cell_assembly_MAP_2026-08-06.md`, NEGATIVES_REGISTRY.md universe-cell
banner (lines 160–182), `universe_cell_vacuum_impossibility_results.md` (premise ledger + fork 1),
`udt_p4_seam_closure_derivation_2026-07-30/AUDIT_REPORT.md` (OC2 germ set),
`udt_relational_phi_dependency_regrade_2026-08-05/AUDIT_REPORT.md` (lines 71–77), LIVE.md 08-06
block. Independent check: re-ran `verify_regrade_r1_fresh.py` fresh — all 17 checks True (C1–C7
reproduced; the flux identity, the squeeze chain, C5 center series, C6 Route-B fork, C7 sign flip).
Nothing committed by this review.

---

## Q1 — Does RG-DISCRIMINATOR overstate? **AMENDED on two counts; not vacuous.**

### (i) The vacuity question as posed: the row is NOT vacuous, but it needs an explicit caveat.

The worry: under the 08-06 free-data inference no law-set is forced, so "closure C is inadmissible
under a chosen S" might carry no information beyond "S was chosen" (any closure could be
discriminated by tailoring S). Adjudication — the row survives vacuity on three grounds, each
checked at source:

1. **S is not a tailored law-set; it is the UNIQUE banked candidate.** The 08-06 conclusion is
   "every route examined is depth-blind → the profile behaves as free data" (LIVE.md 08-06 items
   2–3) — i.e., no structure FORCES the 07-01 set, and also NO RIVAL law-set was banked. A
   conditional on the only candidate on the table is informative in exactly the way the Q1 table
   needs; it would become cheap only if rival law-sets existed and S were picked for the verdict.
2. **Within fixed S the table has contrast across germs.** The discriminating content of a Q1 row
   is WITHIN-COLUMN: at the same S, the even-seal fold-fold closure is dead while other closures
   (Class-B/flux seal, ρ'-only seal, the odd fold — see (ii)) survive. "Any closure can be killed
   by a suitable S" would defeat a table that varied S per row; it does not defeat a within-column
   contrast. The row therefore carries information beyond "S was chosen."
3. **Partial cross-S robustness is already in hand.** C6 (re-verified here): the rigidity holds
   under BOTH banked route variants — Route-A and Route-B-with-forced-mixing — for the full
   mirror seal. That is the beginning of exactly the "row survives across multiple candidate S"
   test the vacuity question names. The named non-robust directions (φ-coupled seal source;
   ρ'-only seal) are already recorded as sharp escapes at source.

**But the caveat is still owed**, because the row is logically a THREE-WAY inconsistency
{even-fold-fold closure, S, anchor data}: it cannot select which member fails. The report states
only the spine-favorable direction ("IF the anchor is carried and S holds, the closure is NOT
fold-fold"). Since S is unforced, the symmetric direction is equally licensed and arguably the
more actionable one for the assembly: **IF the closure IS the (even) fold-fold — e.g., were G18
adopted in that form — THEN S fails (the bulk law is not the 07-01 set, or some source is
φ-coupled).** A row read one-directionally under an unforced S is where F-STEER lives; both
directions must travel with the row.

**What exactly would make the row fully load-bearing** (the honest-test answer): (a) S remaining
the only banked law-set candidate — TRUE today, re-check at every table use; (b) the row surviving
across candidate law-sets as they appear — partially done (Route A/B), to be extended if any rival
is ever banked; (c) the killed germ actually being a live universe-cell candidate — see (ii),
where the row as LABELED currently fails this.

### (ii) The sharper overstatement: the germ label. The row as written mislabels its germ.

This is the review's main finding. The rigidity's seal is **φ'=ρ'=0 at both ends — the Class-A
EVEN fold**, tagged **CHOSE** at source ("carried over from the particle-cell Class-A",
`universe_cell_vacuum_impossibility_results.md` ~line 167). But:

- Canon C-2026-06-10-2 states the mirror as **φ→−φ — the ODD fold, which pins φ=0 and leaves φ'
  FREE** (source doc ~lines 151–152, flagged there as "the Class-B/flux-type seal, not the
  Neumann mirror").
- OC2's germ set — the set the report says the Q1 table is built from — is {fold-quotient,
  partner, glue+B, open-end}, and OC2's fold-quotient continuation is **odd** (seam-closure
  AUDIT_REPORT ~line 36: "unique continuation = odd"); the assembly MAP writes the germ as
  "fold/odd-mirror".
- The odd-odd configuration genuinely ESCAPES the anchor conclusion: φ pinned to 0 at both ends
  gives end-to-end Δφ=0, but the flux monotonicity permits a single-signed interior dip
  (Φ=Zρ²φ' nondecreasing allows φ' &lt; 0 then &gt; 0), so an interior observer can sit at
  Δφ = ln(1101) from the fold. The rigidity does not bind it. (The report KNOWS this — R2(c)'s
  parenthetical and R3's "unique in-reduction survivor is a Class-B φ'≠0/flux-type outer seal" —
  but the row label "(fold, fold) × S → INADMISSIBLE" drops it.)

Consequence: read against OC2's germ set, the first row of the Q1 table as labeled would claim
inadmissibility for a germ (the odd fold — the canon-flavored one, G18's fold) that the algebra
does not kill. That is an overstatement-by-labeling with real steer exposure: it would present the
assembly's first row as pressure against the very closure canon favors, which the mathematics does
not deliver. **Required amendment: parity-type the germ.** The row must read
"(even-fold, even-fold)" — equivalently "Neumann seal φ'=ρ'=0 both ends" — and carry an explicit
NOT-COVERED note for the canon/OC2 odd fold. The even seal is still corpus-used (the 07-02 entry
itself; the particle-cell Class-A seal), so the row is non-empty — but it is a row about the even
germ, which is not currently the universe-cell candidate germ.

(Available honest content for a FUTURE odd-fold row, not claimed by anyone yet and not banked
here: the same flux identity constrains odd-odd profiles to the single-dip shape — a profile-CLASS
constraint, not inadmissibility. Left on the table.)

## Q2 — Was RG-DISSOLVES undersold? **NO — classification stands; one count miscalibrated.**

- Count (1) "08-05 preserves the algebra inside supplied premises": VERIFIED at source — the 08-05
  audit's exact words (lines 71, 77) strip UDT-wide blocking authority while allowing "their exact
  ODE or algebra can still be true inside the explicitly supplied pointwise scalar, action, source,
  branch and boundary premises." Sound.
- Count (2) "the fold germ remains live (OC2: both witness germs banked in use), so the row is
  non-empty": **MISCALIBRATED.** OC2's banked witness germs are the flat-exterior glue and the
  ODD mirror — neither of which the rigidity kills. Non-emptiness of the row actually rests on the
  EVEN seal being corpus-used (the 07-02 entry itself; particle-cell Class-A) — a weaker but
  sufficient ground. The count as phrased borrows liveness from the wrong germ and thereby masks
  the parity gap found in Q1(ii). It should be rewritten, not deleted.
- Count (3) presentation-invariance of the Δφ conclusion: SOUND. Under the constant-reference
  shift φ→φ+c, φ' and Δφ are exactly invariant (trivial, and consistent with C4). The richer
  relational freedom (observer-pair laws not reducible to a pointwise potential) is correctly
  fenced OUT of the row by listing the pointwise chart as a member of S and by conditionality
  (iii) in "what does not survive." The report's own "attack this first" invitation is answered:
  yes, at the level this conclusion uses, the 08-05 freedom is reference-shift, and the anchor's
  canon Δφ form (C-2026-07-02-1) is the invariant carrier.

Net: dissolution would need a corrected-frame change that breaks applicability entirely; none
does. RG-DISSOLVES was given genuine care; it was not the right class. But count (2)'s repair
feeds the Q1(ii) amendment.

## Q3 — Scope discipline (F-SCOPE): **CLEAN, with one exposure already covered by the amendment.**

No G18 ruling is made or implied; the report says so explicitly and its "what does NOT survive"
paragraph blocks every unconditional two-mirror reading on three independent grounds (checked:
each ground cites its source correctly). The registry edit is properly DEFERRED per the frozen
contract; no registry language is drafted in the report, so there is no mis-scoped registry text
to police — but the eventual note must inherit the parity-typed label and the two-direction
caveat, or the scope discipline achieved here leaks at the registry. The single exposure found:
the one-directional "the closure is NOT fold-fold" phrasing plus the unqualified "fold" label
(Q1(i)+(ii)) — an unwary reader maps it onto G18's (odd) fold. The amendment closes it.

## Q4 — The sharpened leg (center + one-fold = EMPTY): **matching S-scope YES; same parity
amendment required.**

It sits inside the same WITHIN-S block in R3 and the same row annotation ("moreover
(regular-center, fold) × S → EMPTY") — S-conditionality is carried with matching scope; no
separate leak. But C5's argument (Φ(0)=0, Φ'(0)=4, monotone ⇒ never meets an outer φ'=0 mirror)
binds ONLY a φ'=0 outer seal; an outer ODD fold (φ pinned, φ' free) is not touched. The registry's
own T1 line is already seal-typed ("EVERY φ'=0-outer-seal configuration is dead") — the Q1 row
must keep that typing: "(regular-center, even-fold) × S → EMPTY."

---

## VERDICT

**RG-DISCRIMINATOR — SUSTAINED AS CLASS, AMENDED AS ROW.** The classification is correct (algebra
exact — independently re-run here, 17/17; applicability survives; the conditional is real and
non-vacuous). Two amendments are REQUIRED before the row enters the Q1 table or the registry note
is written:

**A. Germ-parity typing (mandatory):** relabel "(fold, fold)" → "(even-fold, even-fold)
[Neumann seal φ'=ρ'=0 both ends]" and "(regular-center, fold)" → "(regular-center, even-fold)";
add: "NOT covered: the canon/OC2 odd fold (φ→−φ: φ=0 pinned, φ' free) — it lands in the surviving
Class-B/flux class; this row exerts no pressure on G18's fold."

**B. S-conditionality / two-direction caveat (mandatory), exact wording:**

> "S-CAVEAT: S = the CHOSEN 2026-07-01 law-set + φ-blind sources — unforced (08-06 free-data
> inference) but the unique banked candidate; row robust across both banked route variants
> (Route A; Route B with the full seal). This row is a three-way inconsistency
> {even-fold-fold, S, anchor}: with the anchor carried it rules out the CONJUNCTION
> (even-fold-fold ∧ S) — it cannot say which fails. Discriminating force is within-column (fixed
> S); if the even fold-fold closure were independently adopted, the row instead indicts S
> (φ-blindness or the 07-01 bulk law). Re-check 'unique banked candidate' at every use."

With A+B the row carries information beyond "S was chosen" and is fit to seed the Q1 table.
Without A it misstates which germ died; without B it reads one-directionally under an unforced S.
F-STEER: this review looked hardest at the spine-favorable outcome; the two amendments are the
residue. Reviewer: adversarial review 2, 2026-08-06. Not committed.
