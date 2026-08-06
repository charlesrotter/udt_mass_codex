# ADVERSARIAL REVIEW 1 — algebra + presentation-invariance + germ scoping

Date: 2026-08-06. Reviewer: independent adversarial agent (fresh sympy; NO code imported from
`verify_regrade_r1_fresh.py` or the 2026-07-02 scripts). Recompute:
`ADVERSARIAL_REVIEW_1_recompute.py` (this package, written from source docs only), stdout
`ADVERSARIAL_REVIEW_1_STDOUT.txt` — **28/28 checks pass**. Target: `REGRADE_REPORT.md`
(RG-DISCRIMINATOR) and its self-named load-bearing step (presentation-invariance). NOT committed.

Sources read at origin: `universe_cell_vacuum_impossibility_results.md` (07-02),
`cell_solver_round.py:8-13` (EOMs + JC1), `round_matter_reduction_results.md` (07-01 matter
reduction + ρ-source), `udt_relational_phi_dependency_regrade_2026-08-05/AUDIT_REPORT.md`,
`udt_p4_seam_closure_derivation_2026-07-30/EXACT_DERIVATION.md` (OC2 germ table, K4/K6),
`weld_two_sided_results.md:30-32` (glue jump ΔΠ=q/2), `universe_cell_fold_jc_sigma_results.md:104`
(fold pins: φ(r_s)=0, ρ'(r_s)=0, **q free at fold**).

---

## ATTACK 1 — presentation-invariance: **CONFIRMED, with the missing lemma supplied**

The suspicion was correct in its premise and wrong in its conclusion. Exact findings:

1. **The flux identity is NOT invariant under a bare φ → φ+c.** Recomputed (B1): the identity
   (Zρ²φ')' = 4e^{−2φ}ρ'² maps to (Zρ²ψ')' = 4e^{−2c}·4e^{−2ψ}ρ'²-type form — the absolute-φ
   factor e^{−2φ} rescales the RHS by e^{−2c}; the difference is certified nonzero. The re-grade's
   one-line justification ("the shift moves φ, not φ' or Δφ") is TRUE of the conclusion's
   variables but does not by itself carry the derivation; as written it skips the e^{−2φ} factor
   the attack targeted.
2. **The constant absorbs EXACTLY into Z — the missing lemma.** Recomputed (B2, B3): substituting
   φ = ψ+c maps BOTH EOMs (φ-EL, and the ρ-EOM with an ARBITRARY φ-blind source S, S untouched)
   onto the same law-set with the single recalibration **Z → Z e^{2c}** (e^{2c} > 0: sign of Z
   preserved; Z is FREE under Route A per the source doc itself). The flux rescales by a positive
   multiple, Φ → e^{2c}Φ (B4), so its zeros, sign, and monotonicity are presentation-invariant;
   φ' and Δφ are trivially invariant (B5). The squeeze uses e^{−2φ} ONLY through positivity of
   the RHS, and Z only through Z ≠ 0 — both shift-stable. Hence **φ'≡0 ⇒ ρ'≡0 ⇒ Δφ = 0 ≠
   ln(1101) genuinely survives at ratio level**: the conclusion is a theorem UNIFORM over the
   shift-orbit of the law-set, not a fact of one presentation.
3. **Route B included** (stronger than the re-grade checked): for the general coefficient family
   L = (Z/2)ρ²φ'² + Mρρ'φ' − We^{−2φ}ρ'² + Λ the general flux identity is (Zρ²φ' + Mρρ')' =
   2We^{−2φ}ρ'² (E2); the shift absorbs as (Z,M) → e^{2c}(Z,M) with the forced Route-B ratio
   M/Z preserved (E6); the squeeze closes for ALL (Z≠0, M, W>0) (E4/E5). So the fork-robust leg
   is also presentation-invariant, by coefficient-family uniformity.
4. **Two scope caveats (owed, not breaking):** (i) the adjudication rides on the 08-05 freedom
   being a CONSTANT reference shift — which is what the 08-05 audit states (presentation
   potential from "changing the factorization reference"; stationary Killing depth
   δ_K = log(N(p)/N(q)) composes additively on this arena). A point-DEPENDENT representation
   freedom is NOT licensed by 08-05 and would be a law-set change, outside this adjudication.
   (ii) One number in the re-grade's R1 table IS chart-dressed: C5's "Φ'(0)=4 exactly" holds in
   the supplied presentation only; under the shift it becomes 4e^{2c} (D3). Only its POSITIVITY
   is invariant — which is all the no-solution argument uses, so C5's conclusion stands, but
   "independent of φ₀ and Z" should not be read as "presentation-invariant value."

**Adjudication, exactly:** the DERIVATION does touch absolute φ (through e^{−2φ}), but the
dependence factors entirely through (a) the free coupling Z (exact absorption Z → Ze^{2c}) and
(b) positivity of the RHS — both invariant under the 08-05 constant-reference freedom. The
conclusion (fold-fold admits no profile carrying Δφ = ln(1101)) survives at ratio level. The
re-grade's load-bearing step is SOUND but UNDER-ARGUED; this review supplies the absorption lemma
that makes it rigorous.

## ATTACK 2 — algebra at source: **CONFIRMED (28/28 fresh checks); two restatement notes**

Re-derived from the 07-01 law-set with no reuse: the φ-EL of L = (Z/2)ρ²φ'² − 2e^{−2φ}ρ'² + 2
IS the flux identity (A1) and reproduces the banked φ''- and ρ''-forms verbatim
(`cell_solver_round.py:8-9`; A2, A3). The φ-EL contains no ρ'', so an arbitrary φ-blind
ρ''-source can never enter it (A4); the RHS is Z-free (A5). Squeeze legs C1–C3 exact; sharpened
center leg: regularity (no conical defect) gives ρ'(0)=e^{φ₀}, hence Φ(0)=0 and Φ'(0)=
4e^{−2φ₀}e^{2φ₀}=4 > 0, Z- and φ₀-free in the supplied chart (D1, D2) ⇒ Φ > 0 off-center under
Φ'≥0 ⇒ no outer φ'=0 end reachable ⇒ NO solution. Route-B mixing term independently re-reduced
from the stated ingredients (√h=ρ², 2e^{φ}Kφ', K=2e^{−φ}ρ'/ρ) to 4ρρ'φ' (E1) and its flux and
seal behavior confirmed (E3, E4). Gaps between source and re-grade restatement: only two, both
minor — (i) the C5 "=4" chart-dressing above (the source doc never states 4; the re-grade
introduced it correctly-in-chart); (ii) C6 hardcodes Z=8 where the source keeps general
Φ̃ = Zρ²φ' + 4ρρ' (immaterial: Route B forces Z=8). No error found in any load-bearing step.

## ATTACK 3 — the premise tag table / germ scoping: **tag (c) MISKEYED — amendment required**

The specific suspicion (glue also forces φ'=0, rigidity under-scoped) is HALF right, and the real
error runs in BOTH directions. At source:

- **OC2's FOLD-QUOTIENT germ is the ODD fold** (K4b: δφ(r_s)=0 essential, **φ'(r_s) FREE**,
  q = Zρ_s²φ' an OUTPUT; ρ'(r_s)=0 natural). Confirmed independently at
  `universe_cell_fold_jc_sigma_results.md:104`: "q free at fold; q ≥ 0 — DERIVED." A φ'-free end
  does NOT zero the flux (F3) — this is exactly the source doc's L1 escape class (verified
  numeric counterexample, Δφ=+0.26 nonconstant) and its fork 1 (the odd fold is the UNIQUE
  in-reduction SURVIVOR). **So within OC2's taxonomy, the (fold, fold) row is NOT bound by the
  rigidity — the re-grade's Q1 row label "(fold, fold) × S → INADMISSIBLE," keyed to "each
  closure germ pair (from OC2's set)," is FALSE as literally indexed.** The rigidity's seal
  φ'=ρ'=0 is the 07-02 doc's Class-A EVEN fold — a germ ABSENT from OC2's four-element set
  {fold-quotient, partner, glue+B, open-end}.
- **The germ in OC2's set that DOES impose the rigidity's BC is OPEN-END** (K6d): the bare free
  endpoint's natural BCs are π_φ=0 ⇒ φ'=0 AND ρ'=0 — recomputed exactly (F2). Open-end zeroes
  BOTH flux forms (Route A and Route B), so open-end×open-end and every mixed pairing with an
  even fold is ALSO rigidity-bound. "Binds ONLY the fold-fold closure" therefore UNDERSTATES the
  reach (misses open-end) while simultaneously OVERSTATING it (includes OC2's odd fold, which
  escapes). Note the banked universe-cell chain itself uses the mixed escape: inner core
  φ'(r_c)=ρ'(r_c)=0 "from stationarity alone" + outer odd fold with q free — one sealed end only,
  no squeeze, Φ monotone ⇒ q ≥ 0 — the fold-JC "q ≥ 0" row IS the rigidity's monotonicity used
  one-sidedly. Full consistency at source; the re-grade's row label just misnames the bound class.
- **Glue (the asked direction):** generically NO — the banked glue carries jump ΔΠ = q/2 with a
  seam functional B, B'(ρ_s) = q/2 (K6c; `weld_two_sided_results.md:30-32` has Π_inner = −q/2,
  q ≠ 0 banked-in-use), so φ' is free/flux-carrying at a glue seam. BUT in the B ≡ 0 limit
  well-posedness forces q = 0 ⇒ φ'(r_s) = 0 (F4): **glue-without-a-boundary-action IS
  rigidity-bound** — a conditional extra reach the re-grade does not record (and D-a, the seam
  boundary-action status, is exactly the named open datum).

**Correct scoping (proposed amendment):** the rigidity binds the BC-CLASS "both ends impose
φ'=0" — even-fold (Class-A, not in OC2's set), open-end, and glue-with-B≡0 — under Route A;
under Route B it binds the full-seal/open-end versions (φ'=ρ'=0). It does NOT bind OC2's
fold-quotient (odd fold, φ' free), whose row in the Q1 table is OPEN, not INADMISSIBLE. The Q1
table should be indexed by end-BC classes (or OC2's set extended with the even fold), and the
re-grade's R3 sentence "IF the anchor is carried and S holds, the closure is NOT fold-fold" must
be re-worded — as literally read against OC2's germ naming it wrongly suggests the canon fold is
excluded, when the canon (odd) fold is precisely the surviving seal (fork 1).

---

## VERDICT

- Attack 1 (presentation-invariance): **CONFIRMED** — conclusion survives; absorption lemma
  Z → Ze^{2c} supplied; two precision caveats (constant-shift scope; Φ'(0)=4 chart-dressed).
- Attack 2 (algebra): **CONFIRMED** — 28/28 fresh independent checks; no load-bearing error.
- Attack 3 (premise tags): **BROKEN AS WRITTEN — tag (c) and the Q1 row label are miskeyed to
  OC2's germ taxonomy** (OC2's fold = odd fold = the ESCAPE, not the bound germ; open-end and
  glue-with-B≡0 are bound but unlisted). Content salvageable by relabeling to BC-classes.

**Overall: RG-DISCRIMINATOR AMENDED** (sustained in substance): the algebra and the
presentation-invariance step stand — RG-DISSOLVES is correctly rejected — but the discriminator
row must be re-labeled from "(fold, fold)" to the φ'=0-seal BC-class before any registry edit,
and the reach corrected in both directions. As drafted, the first row of the Q1 table is wrong
under the very germ taxonomy it cites.
