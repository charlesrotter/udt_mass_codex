# ADVERSARIAL REVIEW 2 — classification / steer / scope (Step 2, survivor-closure admissibility)

Reviewer: adversarial classification review agent, 2026-08-06. Target: `DERIVATION_NOTES.md`
against `PREREGISTRATION.md` (frozen), the MAP spine (`udt_global_cell_assembly_MAP_2026-08-06.md`
§0/§2), and Step 1 CONSOLIDATED (`udt_two_mirror_rigidity_regrade_2026-08-06/REGRADE_REPORT.md`).
Independent work: re-ran `step2_checks.py` (10/10 PASS, exit 0); hand-re-derived §I.1(c) growth
bound (Cauchy–Schwarz chain, s(r) ≥ (r/L)², r₁ ≤ L/√ε, D ≥ (ln ε)/(2Z) — sound; note ε̄ ≥ 1 is
needed for ρ to reach 2ρ_c since s ≤ 1, and ε̄ > 1101^{2Z} satisfies it); hand-re-derived the §III
quadratic and root product (−ZX/(8m³), matches); verified Δφ_L = (1/2)ln((X−r_c)/(X−r_s)); read
the closure pins at source (`universe_cell_fold_jc_sigma_results.md`:20-42,
`universe_cell_vacuum_impossibility_results.md`:40-80, 139-156, 165-176).

## Item 1 — Is fold-CONSTRAINS honestly attributed? SUSTAINED AS CLASS; ROW WORDING AMENDED

The prereg's own outcome-class definition ("the admitted class is a proper, exactly-described
subclass") is met: 𝒜_fold is proper and exactly described, and — decisively — the fold/glue
CONTRAST is genuine per-closure discrimination: 𝒜_fold = 𝒜_glue ∩ {ρ'(r_s) = 0}, a codim-1 cut
the glue does not make. The spine question ("does each freedom constrain the other?") gets, for
the fold, a genuine but MODEST two-way answer: closure→profile = the seam ρ-pin (one pointwise
boundary cut, real, source-derived — the fold doc's verifier found ρ'(r_s)=0 by three independent
routes, "stronger than claimed"); profile→closure = q, E(r_s) slaved. That IS an interlock in the
MAP-§0 sense. BUT the §IV table cell "**S2-CONSTRAINS** (CUT-1..4; interlock: seam data slaved to
bulk)" lets the row carry CUT-1..3's weight, which the notes' own §I.3 honest-attribution
paragraph concedes belongs to S + the inner core and which the GLUE row correctly labels
"closure-independent." A table-only reader credits the fold with cuts every closure shares. Also:
the q-slaving half of "the interlock" is itself closure-independent (the glue row calls the
identical fact "one-way slaving, not an interlock"); the fold-distinctive content is the pin (and
its derived consequence Φ'(r_s) = 0, seam-critical flux). Answer to the posed question: the spine
gets YES-BUT-THIN, not "mostly S constrains" — the closure's own cut is real, exact, and codim-1,
but it is ONE boundary pin; the deep structure (φ slaved, monotone, Z>0, flat-then-rising) is
S + geometry. **AMENDED ROW WORDING (mandatory), Q2c fold cell:**
> **S2-CONSTRAINS — marginal to the closure: CUT-4 only** (seam ρ-pin ρ'(r_s)=0, codim-1:
> 𝒜_fold = 𝒜_glue ∩ {ρ'(r_s)=0}; q, E(r_s) slaved to bulk with q>0 anchor-forced ⇒ Φ'(r_s)=0
> seam-critical). CUT-1..3 (φ slaved to ρ; monotone/Z>0; flat-then-rising) are S + inner-core
> cuts, shared by every closure.

## Item 2 — L-OUTSIDE scoping + Step-1/Step-2 geometry consistency: THE KEY ADJUDICATION

**(2a) The proposed re-headline "L incompatible with the even-core inner end, NOT the fold
universe" is REJECTED for the fold row and already-implemented for the glue row.** Parsing the
three violations of §I.4: (i) inner φ-pin, (ii) ρ'=0 unsatisfiable at ANY point — which strikes
BOTH the inner ρ-pin AND the odd fold's OWN seam ρ-pin, (iii) = (ii) at the seam. The seam ρ-pin
ρ'(r_s)=0 is intrinsic to the odd fold itself (source-derived, three routes, holds for ANY φ_s —
`universe_cell_fold_jc_sigma_results.md`:26-29; NOT an even-fold import: the fold quotient makes
ρ even ⇒ ρ' odd ⇒ ρ'(r_s)=0, while φ odd ⇒ φ(r_s)=0, φ' free). So the FOLD closure excludes the
L-lead independently of the inner end; the exclusion does NOT hinge on the even core alone. The
honest per-closure headline is exactly what §II.4/§III already state: **fold = OUTSIDE by both
ends independently (inner core pins AND the fold's own seam ρ-pin); glue = OUTSIDE via the inner
end ONLY, bulk-inside.** Suggested (optional) sharpening of the fold Q2d cell: "OUTSIDE — excluded
independently by BOTH ends (violations i,ii-inner = inner core; ii-seam,iii = the fold's own seam
ρ-pin); bulk-inside per §III." The notes' "boundary-excluded, not bulk-excluded" summary is
accurate and honest against owner steer (F-STEER discharge is real here: §III plainly reports the
owner-unfavorable bulk-inside fact plus both rescue limits and their blocks).

**(2b) Geometry consistency with the row-1 kill: CONSISTENT — no straddle. This is the important
adjudication and it comes out clean, for four independent reasons.**
1. The amended row-1 kill is keyed to the BC-CLASS "**φ' = 0 at BOTH ends**" (a conjunction over
   the pair of ends), not to the even germ per se. Step 2's cell imposes φ'=0 at exactly ONE end
   (the inner core); the outer end is φ'-FREE (odd fold) or unpinned (glue). One even end was
   never killed; only the pairing was.
2. Step-1's sharpened leg killed "regular CENTER + one φ'=0 outer mirror." Step 2's inner end is
   a finite core ρ_c > 0 — a DIFFERENT class from a regular center (ρ→0), a distinction the fold
   doc itself draws (":66 — the round solver's ρ'_c=1 finite core is a different class"), and the
   outer closures examined are precisely the non-φ'=0 ones anyway.
3. Constructive proof: the §I.1 witness (checks C7, re-run PASS) EXHIBITS a member of the
   even-core + odd-fold class carrying the anchor — the configuration is non-empty, so it cannot
   be inside any kill. Step 2 in fact UPGRADES Step-1's escape from "not killed" to "witnessed."
4. The chain is not merely consistent but mutually load-bearing: GIVEN the even-core inner end,
   row 1 is exactly what narrows the outer fork to {odd fold, generic glue B≢0} — even-core +
   open-end and even-core + glue-B≡0 both re-enter the killed both-ends class, and §II.3(b)
   states the B≡0 re-entry explicitly. Step 2 examined precisely the two survivors of its own
   inner-end choice. Also consistent with the fold-doc verifier corollary (even-core VACUUM cells
   = constant cylinder): the witness carries σ ≢ 0, as it must.
   Residual honest tension (already flagged, keep it): the even-core inner end is itself a CHOSE
   (OC2 germ freedom; caveat 2), and CUT-2/3 + the Z>0 forcing ride on it; §II.4's free-core fork
   (L-lead → INSIDE the glue bulk class) is correctly labeled "a fork, not a finding."

## Item 3 — The two sharpenings: NO overstatement; ONE MIS-ATTRIBUTION (in the safe direction)

- **Anchor forces Z > 0 (§I.0):** exact within its stated scope, and the scope IS stated inline
  (Route-A orientation; inner even-core pin — both dependencies visible in the two-line
  derivation; caveats 2/4/5 cover the forks). Re-checked: Φ' = 4e^{−2φ}ρ'² is Z-free, Φ(r_c)=0,
  so Z<0 ⇒ φ' ≤ 0 everywhere ⇒ Δφ ≤ 0 ≠ ln(1101). Sound. The whole doc is headed LEAD/UNBANKED,
  which covers it. MINOR AMEND: any row/registry line quoting "Z>0 forced" must carry
  "(Route-A orientation; even-core inner end — caveats 2/5)" since under Route B the monotone
  object changes and the forcing was not re-derived.
- **Finite core forced for ALL φ-blind matter (§0):** labeled "LEAD sharpening (unbanked)" — but
  this is ALREADY BANKED AT SOURCE. `universe_cell_vacuum_impossibility_results.md` R2 ("Even
  WITH matter, no regular center — VERIFIED"): "the verifier proved the no-cure for an ARBITRARY
  φ-blind ρ''-source, not just the banked winding form" (blind-verified 2026-07-02, agents at
  source). The Step-2 line under-claims (offers as a new lead what is a banked fact). AMEND: cite
  R2 as the banked authority; drop the "unbanked lead" framing. Strengthens, not weakens; no
  overstatement anywhere in item 3.

## Item 4 — Scope/steer hygiene: PASS, two minor notes

- S-caveat: quoted VERBATIM in the header with explicit travels-on-every-claim declaration +
  caveat 1. Matches Step-1 amendment 3 word-for-word. PASS.
- G18: no ruling, no germ adopted (caveat 6; §IV "no closure adopted"). The fold-CONSTRAINS cell
  is spine-favorable but is an admissibility characterization, not a germ selection. PASS.
- Mass content: none. E(r_s) = q²/(2Zρ_s²) is cited seam energy (source-forced), budget/
  transversality explicitly "cited, unused." No spectrum/discreteness. F-TARGET clean. PASS.
- σ-realizability: caveat 3 + §I.2 honestly split prescribed-S(r) (exact, apples-to-apples with
  the Step-1 comparison class — confirmed: R2/C2 at source is "arbitrary φ-blind ρ''-source")
  from autonomous-L_m (D3's endpoint ρ'=0 scope edge, flagged at source and here). PASS.
- Route-B: caveat 5 honest (Q2a existence NOT re-derived under Route B; monotone cut survives in
  modified form). MINOR AMEND: the §IV table's "YES (exact IVT + witness)" cells should carry
  "(Route A; Route-B existence not re-derived — caveat 5)" so the table is self-contained.
- Glue ADMITS-ALL action-level condition: stated BOTH in §II.3(b) (B must exist; B≡0 ⇒ q=0 ⇒
  re-enters the Step-1 dead class) AND in the table row ("B-existence = action-level only").
  PASS. The anti-spine cell is reported plainly, with the one-way q-slaving precision note —
  F-STEER discharged on the glue side too.

## VERDICT

**S2-MIXED SUSTAINED — with amendments** (none overturning): (1) fold Q2c row cell re-worded per
Item 1 (attribution inside the row: closure's marginal cut = CUT-4 only; CUT-1..3 = S+inner-core,
closure-shared); (2) the Item-2 proposed "inner-end-only" re-headline REJECTED for the fold
(fold-own seam ρ-pin excludes L independently), sustained as already written for the glue;
Step-1/Step-2 geometries adjudicated CONSISTENT (no row-1 straddle; four grounds above);
(3) finite-core sharpening re-attributed to banked R2 (not a new lead); "Z>0 forced" carries its
Route-A/even-core scope wherever quoted; (4) Q2a table cells gain the Route-B flag. Status
remains LEAD/UNBANKED pending consolidation; nothing here is committed by this reviewer.
