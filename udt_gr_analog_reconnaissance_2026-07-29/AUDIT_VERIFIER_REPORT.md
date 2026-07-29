# AUDIT VERIFIER REPORT — GR-analog reconnaissance package

Auditor: blind honesty auditor, same-session-spawned (NOT a hosted external model — the
same-session caveat travels; an independent-context pass, not an independent-model pass).
Date: 2026-07-29. Contract: `PREREGISTRATION.md` @ 6eb0cfe (confirmed committed before the
survey artifacts). Artifacts audited: `GR_ANALOG_MAP.tsv` (26 rows), `ANALOG_RECON_REPORT.md`.
Mode: adjudication per contract §6 — honesty/accuracy pass, no math to re-derive.

## VERDICT: PASS-WITH-REQUIRED-AMENDMENTS

The survey is honest, lane-compliant, and method-only throughout. No falsifier fires.
Four amendments (A1 required-substantive, A2 required-substantive, A3 required-accuracy,
A4 minor-consistency) are owed before banking.

---

## Per-duty findings

### 1. Contract compliance — PASS
- **Lane clause:** extracted from both files and diffed byte-for-byte: IDENTICAL to the
  prereg's §"THE LANE CLAUSE" (7 lines, verbatim, at the report top). PASS.
- **Floor veins:** all 6 present. Veins 1-5 map one-to-one to report veins 1-5; prereg
  vein 6 (junction/DtN-Calderón/geon; Birkhoff; constraint classification) is fully covered
  by report veins 6-9 plus the geon vein 11. Two additions (Fefferman-Graham contrast;
  explicit geon vein) — additions are contract-legal; no deletion. PASS.
- **TSV columns:** the 7 contracted columns present in contracted order (p4_item /
  corpus_result / machinery / transforms_cleanly / disanalogy / import_risk /
  attribution_status) plus one extra `notes` column — an addition, not a deviation. 26 data
  rows confirmed by count. PASS.
- **Disanalogy columns (F-G2):** all 26 read individually. Every one is filled and
  UDT-specific (anchored Q=c_E·e^{−φ}, K₄ characters, registered chart/trivial stabilizer,
  mirror wall parity-lock, finite cells, pairing-relativity, moduli/graded slots, inverted
  inference direction). None boilerplate; no row claims a P4 problem "is" the corpus
  problem — shape-analogy language is consistent. F-G2 does not fire. PASS.

### 2. Import-risk tag audit (F-G1) — PASS
Hunted every row and TG3 for GR-answer adoption. Found none.
- **GHY/Hayward rows (10-11):** jet-slot ENUMERATION tagged GREEN; the counterterm
  (K·√h, corner angle formula) explicitly RED with the gate-5 alternative (candidate's own
  R_wall/R_corner must pair the slots) stated. TG3 item 2 says "enumeration only, never the
  counterterms". Correct per the contract's named danger spot.
- **Wald-charge exclusion:** rationale is structural (no continuous parameter ξ → no seat),
  not merit; charge formulas RED; exclusion marked PROVISIONAL/revisit-after-bank. Correct.
- **DtN row (21):** typing only; uniqueness machinery stated non-transferring. Correct in
  substance — but see A2 (tag granularity).
- **Twisted-cocycle/CS row (16):** the e^{iS} quantization MECHANISM is RED and explicitly
  excluded from the shortlist rationale ("only the classification math is shortlisted");
  the GREEN half (cocycle-holonomy classification) is genuinely mechanism-free. No
  RED-tagged mechanism reappears inside any GREEN shortlist rationale (all 5 TG3 items
  checked). F-G1 does not fire.

### 3. Attribution audit (F-G3) — PASS on accuracy; tally amendment owed (A3)
Six spot-checks run via WebSearch 2026-07-29, statement-level:
- **Lovelock JMP 12, 498-501 (1971)** — CONFIRMED, incl. the load-bearing statement: in 4D
  the only symmetric divergence-free 2-tensor concomitants of (g,∂g,∂²g) are the metric and
  Einstein tensors. Row 1 accurate.
- **Douglas Trans. AMS 50 (1941), 71-128** — CONFIRMED, incl. the "exhaustive treatment of
  the two-degrees-of-freedom (n=2) case" scope claim. Row 7 accurate.
- **Iyer-Wald PRD 50, 846-864 (1994)** — CONFIRMED, incl. content: diffeo-invariant
  Lagrangian → Noether charge (n-2)-form, first law for arbitrary perturbations, dynamical
  entropy proposal. Row 14 accurate. (Cosmetic: authors are Iyer & Wald; row says
  "Wald-Iyer" — harmless.)
- **Anderson-Duchamp Am. J. Math. 102 (1980)** — CONFIRMED (title, venue, content role in
  the local-vs-global variational split). Page end: source record says 781-867; the TSV says
  781-868 — trivial, fold into A4.
- **Moncrief JMP 17, 1893-1902 (1976)** (auditor's pick) — CONFIRMED, incl. the exact
  statement the row leans on: linearization stable iff no global Killing fields. Row 23
  accurate.
- **Israel NCimB 44, 1-14 (1966) + corrections NCimB 48, 463 (1967)** (auditor's pick) —
  CONFIRMED, both ADS records as cited; extrinsic-curvature matching content as stated.
  Row 20 accurate.
Zero misattributions found in 6/6 checks; no fabricated scholarship detected. All 6
MODEL-KNOWLEDGE rows (2, 3, 16, 18, 23 TSV-order: rows for classical invariant theory,
Aldersley, twisted-H¹, invariant-Lagrangian family, Corvino, tetrad-GR) are visibly
flagged in the status column with caveats. **Shortlist item 4's dependence on the
MODEL-KNOWLEDGE twisted-H¹ row carries the required F-G3 flag IN PLACE (TG3 item 4, bold),**
and no other MODEL-KNOWLEDGE row underpins the shortlist — the report's F-G3 self-statement
is accurate. F-G3 does not fire. Tally arithmetic is misleading → A3.

### 4. Shortlist rationale audit (F-G4) — PASS
All 5 TG3 items: prioritization is by gate (3, 5, 1, 6, 5/R3) + transformability; hunted
for physics-merit language ("would give mass / discreteness / the expected structure") —
none found anywhere in TG3 or the exclusion list. Every item names its transform-FIRST step
and a concrete soundness check (classical-limit reduction; TC5 reproduction; cross-check vs
gate-4 identity set + worked example; K₄-torsion vacuity as special case; toy-elliptic
parity-halving). Exclusions are structural (no seat / evaporates / needs symbol first /
irreducibly ODE / no infinity), never merit. F-G4 does not fire.

### 5. PROVISIONAL discipline — amendments A1, A2 owed
The standing caveat is present and the stamp is carried on: the report header, vein 1, vein
3, vein 4 (bracketed throughout), TG2 items 1/4/5, TG3 item 3 (inline, with the "starting
point changes" clause), TG4 D1, TSV rows 1, 2 (as tagged rows), 9, 14, 19, 23, and the
Wald-charge exclusion. GAPS:
- **TG4 D2 and D3 carry NO stamp** while leaning directly on the Stage-2 claims (D2 on the
  vacuity → "no constraint/evolution split is forced… can be fully DETERMINED"; D3 on the
  trivial continuous stabilizer → "no corpus analog" forcing claim). D1 stamps itself; D2/D3
  must too. → **A1.**
- **Survival under the now-known Stage-2 amendment** (verifier refuted the unqualified
  vacuity: generic-stratum-only, with an exact Noether identity on the k_mod=0 stratum):
  adjudicated row-by-row. The gate-1/Fischer-Marsden item (TG3 #3) SURVIVES — it is
  conditionalized in place. The Wald-charge exclusion SURVIVES as reasoning — the machine
  needs a continuous arbitrary-function parameter ξ, and a discrete stratum identity is not
  automatically that seat — but its stated antecedent ("identity set EMPTY") is now the
  superseded unqualified form. TG4 **D2 is the one near-invalidation**: "no
  constraint/evolution split is forced" and "fully DETERMINED" are contradicted ON the
  k_mod=0 stratum by an exact Noether identity; D2's content must be qualified to
  generic-stratum. No row is fully invalidated; the categorical "EMPTY / no seat at all /
  fails at its first line" statements (vein 4, TG2 #1 and #4, TSV rows 1, 14, 23) survive
  only via their flags and must be re-worded to the qualified form (or the standing caveat
  updated to record that the amendment has now landed and what it says). → **A2.**

### 6. Departure-register audit — PASS
D1-D7 each read as observations: structural statements of where corpus arguments fail and
what native structure sits in the vacated seat. No mechanism is proposed, no drill target
named, no "next we should test" language; D5's "must be reborn as R5's relation" is a
descriptive seat statement, not a proposal. The register's own header states the
PONDER-not-leads discipline. Compliant (subject to A1's missing stamps on D2/D3).

---

## REQUIRED AMENDMENTS

- **A1 (PROVISIONAL stamps).** Add PROVISIONAL-pending-Stage-2-bank inline to TG4 D2 and
  D3 (both lean on the Stage-2 vacuity/trivial-stabilizer claims; D1 already carries it).
- **A2 (vacuity refinement pass).** The Stage-2 verifier has refuted the UNQUALIFIED vacuity
  (now: generic-stratum-only + exact Noether identity on the k_mod=0 stratum). Update the
  standing caveat to record this, and qualify the categorical vacuity statements (report
  vein 4, TG2 #1/#4, TG4 D2; TSV rows 1, 14, 23) to the generic-stratum form. D2
  specifically: "fully determined / no forced split" holds at most on the generic stratum —
  the k_mod=0 stratum carries an exact identity. The Wald/Utiyama/constraint failure-surface
  REASONING survives (no continuous arbitrary-function parameter is implied by a stratum
  identity), so this is refinement, not refutation — but the wording must not outlive its
  antecedent.
- **A3 (attribution tally accuracy).** The report's "VERIFIED: 18 (incl. 3 existence) /
  MODEL-KNOWLEDGE: 8" sums to 26 and reads as a row partition; the actual ROW partition
  (recounted from the TSV) is 17 VERIFIED + 3 VERIFIED-existence + 6 MODEL-KNOWLEDGE = 26.
  The "8" reaches its total by counting two SUB-row attributions (the arXiv:0910.2933 scope
  statement inside a VERIFIED-existence row; the Z₂-brane cousin note inside the VERIFIED
  Israel row). Restate as the row partition plus a separate sub-attribution list. (Honesty,
  not concealment — the sub-items are individually disclosed in the rows — but the summary
  arithmetic misleads.)
- **A4 (minor consistency).** (i) TSV row 21 (DtN) tags "any uniqueness-statement transfer"
  AMBER; F-G1 names "uniqueness conclusion" as a forbidden answer class — retag the
  conclusion-transfer half RED (the row's prose already says it does not transfer; the tag
  understates). Consider the same for row 27's "identity-count transfer" AMBER.
  (ii) Report vein 3 calls Hayward "VERIFIED-existence"; TSV row 11 tags it VERIFIED with an
  existence-style caveat — reconcile. (iii) Anderson-Duchamp page range: source record says
  781-867; TSV says 781-868 — fix.

## Falsifier record (auditor's own)
F-G1: no firing. F-G2: no firing. F-G3: no firing (6/6 spot-checks accurate; flags in
place). F-G4: no firing. Ceiling: respected — the strongest claims found are of the
pre-committed "machinery Y transforms up to step Z, breaks on W" form; nothing about what
UDT's equations are; no candidate favored; no gate pre-judged.

---

# AMENDMENT CLOSURE (same auditor, second pass — 2026-07-29)

Re-audit of the amended package (adversarial; nothing taken on the coordinator's word).

## VERDICT: NEW-DEFECT (one exact item, one-word scale) — A1–A4 themselves are ALL CLOSED

- **A1 — CLOSED.** TG4 D2 and D3 headings verified carrying
  `[PROVISIONAL-pending-Stage-2-bank]` in place (report lines 318, 327).
- **A2 — CLOSED at all six named locations; no over-correction.** Standing caveat records
  the refinement verbatim (generic-stratum vacuity; resonance strata k_mod=0 and C=0 with
  λ∓k_mod ∈ {±1}; example identity quoted) and explicitly denies a restored Noether-II
  tower. Vein 4, TG2 #1, TG2 #4, TG4 D2 all read stratum-local + discrete-character-graded;
  every occurrence of "restored/restore" in the document (3 hits) is a DENIAL, none an
  assertion — the rewording did NOT over-correct into "GR-like Noether-II restored". TSV
  rows 1/14/23 verified qualified ("GENERICALLY vacuous", stratum conditions, the example
  identity and not-a-Noether-II-parameter grading in the row-14 notes, PROVISIONAL stamps).
  D2's near-invalidation is now correctly stated (determined GENERICALLY; stratum-local
  constraint seat reintroduced; the stratum-graded alternation itself flagged corpus-less —
  an observation, not a mechanism; PONDER discipline intact).
- **A3 — CLOSED.** Recounted from the amended TSV myself: 17 VERIFIED + 3
  VERIFIED-existence + 6 MODEL-KNOWLEDGE = 26 rows (27 tab-lines = header + 26; no row
  added/deleted). Tally text now states the true row partition with both sub-row
  attributions (0910.2933 scope; Z₂-brane note) listed separately. Matches.
- **A4 — CLOSED.** (i) DtN row import-risk now "RED (any uniqueness-statement/conclusion
  transfer - F-G1 forbidden answer class)" — verified by content match. (ii) Hayward
  reconciled: report vein 3 and TSV both VERIFIED with the exact-1993-citation caveat
  retained in the row. (iii) Anderson–Duchamp 781-867 in the TSV.
- **CORRECTION_LAYER.md — ACCURATE.** Each entry checked against the actual text; the
  did-NOT-change list HOLDS: TG3 shortlist verified untouched (ordering statement, item-3
  conditional clause, item-4 F-G3 flag, RED e^{iS} exclusion, exclusion list all intact);
  **lane clause re-diffed byte-for-byte against the prereg: STILL IDENTICAL**; row-27 AMBER
  left as-is (consistent — my A4 said "consider", not required).
- **AUDIT_REPORT.md — FAITHFUL** to this audit (lane byte-identical; 26/26 disanalogies;
  6/6 spot-checks; zero answer-imports; F-G1..F-G4 none fired; A1–A4 applied; caveats
  travel). Cosmetic nuance only: it says "D1–D3 PROVISIONAL-stamped" — D1 carries the short
  inline "[PROVISIONAL]", not the full stamp; substance accurate.

## THE NEW DEFECT (exact)

**TG4 D1, line 313:** the parenthetical still reads "vacuous identity set [PROVISIONAL]" —
UNQUALIFIED. It is the compressed restatement of TG2 #1, which A2 correctly qualified
("GENERICALLY empty … exact identities survive only stratum-locally"); D1's wording now
contradicts its own source paragraph and violates A2's stated principle (categorical wording
must not outlive its antecedent) in place. Provenance: my own A2 location list named D2 but
not D1 — the implementer executed the spec exactly; this is a spec-omission residue surfaced
at closure, not an implementation error. **Fix: one word-scale edit — "generically vacuous
identity set (stratum-local exceptions; see TG2 #1) [PROVISIONAL]".** Upon that fix the
package closes with no open items. (Noted, not a defect: the TG3 exclusion line "no seat
without continuous gauge" is a conditional that survives the refinement and carries its own
revisit-after-bank flag — acceptable as-is.)
