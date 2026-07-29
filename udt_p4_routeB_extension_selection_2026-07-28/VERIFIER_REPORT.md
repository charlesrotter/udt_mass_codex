# BLIND ADVERSARIAL VERIFIER REPORT — Route B Stage 1

Agent designation: **blind verifier, same-session-spawned**. Date: 2026-07-28.
Caveat (travels per the uniqueness-consumer META finding): this verifier is
**not a hosted external model**; it is a zero-context adversarial agent spawned
in the same session/toolchain as the derivation.

Target: `udt_p4_routeB_extension_selection_2026-07-28/` against its binding
contract `PREREGISTRATION.md` (incl. the pre-derivation T4 amendment).
Independent script preserved as `VERIFIER_INDEPENDENT_CHECK.py` (own
construction: own so(1,3) parametrization via η·antisymmetric, own matrix
exponentials, own commutant solves, own monomial substitution for the witness
slice; exit 0, 33/33 checks after fixing two of my own coeff-extraction bugs —
both mine, not the package's).

## VERDICT: **PASS-WITH-REQUIRED-AMENDMENTS** (one amendment, A1 below)

The load-bearing deliverables — the stratum survival ledger, the T5 forcing
table, the T4 plane/volume-loci derivation, the T3 cocycle law, and the T6
L1/L2 MODULUS-CARRIED re-tags — all verify independently and are correctly
scoped. One claim is refuted **as stated** by an explicit counterexample: the
finite residual chart symmetry is NOT only Z₂ = {I, R_π}. The error is
localized (no survival verdict, forcing cell, or re-tag changes); it corrupts
the moduli-quotient bookkeeping only, hence amendment, not refutation of the
package.

## Duty 1 — RERUN

- `python3 derive_routeB_stage1.py`: **exit 0**, ~2 s, single process, CPU.
- `routeB_stage1_results.json` after rerun: **byte-identical** to the
  committed one. Stdout identical to `DERIVATION_STDOUT.txt` modulo the
  absolute `wrote <path>` line. 85/85 PASS, 0 FAIL, all falsifier flags False.
- Grep + read of the script: **no floats** (Rational/Integer/symbols only),
  **no randomness**, **no network**, no numpy. Deterministic. Confirmed.

## Duty 2 — INDEPENDENT RE-DERIVATION (all in `VERIFIER_INDEPENDENT_CHECK.py`)

(a) **(a,d)-plane decomposition — CONFIRMED.** Rebuilt the E07 generator from
the banked 07-25 frame diag(e^{−φ},e^{φ},e^{−kφ},e^{kφ}): generator is
diag(−1,1,−k,k), trace 0, so the E07 axis IS the det-one line {a+d=0}; the
isotropic axis {a=d} meets it only at the origin (spectator). Solving
{−k=λ, k=λ} gives only k=λ=0. **Adjudication: the package's statement "the
MAP's 'E07 k = joint-audit λ' is FALSE at matrix level" is CORRECT** — the two
seats are orthogonal axes, equal only at the E06 point.

(b) **Volume loci — CONFIRMED, with correct convention stamps.** From my own
matrix exponential of diag(−1,1,a,d)·φ: (i) 4D coframe volume-blind ⟺
a+d=0 (isotropic point: λ=0, NOT −1/2); (ii) ruler+screen spatial-triad
volume-blind ⟺ 1+a+d=0, isotropic point 1+2λ=0 ⟺ λ=−1/2; (iii) witness
slice: blind ⟺ λ=−1/2 AND zero twist shift; c1-coefficient alone pins
λ=−1/2, c2 then forces shift=0; no λ works with nonzero shift. The package
stamps 4D vs triad vs slice as **convention-dependent derived readings**, and
identifies "1+2λ=0" as the spatial-triad reading only — honored, not cited as
banked (T4 amendment satisfied; see Duty 4).

(c) **Stabilizer / residual — CONFIRMED for the connected part; finite
residual claim REFUTED AS STATED (→ A1).** With my own parametrization:
registered-chart connected stabilizer trivial; block-form stabilizer exactly
the screen rotation, acting (K,C)↦(SKS⁻¹, SC) — action law verified; R_π =
diag(1,1,−1,−1) acts (K,C)↦(K,−C) — verified. **Counterexample:** R12(π) =
diag(1,−1,−1,1) and R13(π) = diag(1,−1,1,−1) are both in SO⁺(1,3) (det 1,
orthochronous, π-rotations in the ruler-screen planes), fix X₀, and preserve
the registered class (top block [H,0] and K-lower-triangularity intact),
acting as k10↦−k10 with signed C-flips (R12π: (c00,c11)↦(−c00,−c11); R13π:
(c01,c10)↦(−c01,−c10)). So the finite residual contains at least the **Klein
four-group** {I, R23(π), R12(π), R13(π)}; the claimed "Z₂ = {I, R_π}" is a
proper subgroup. Robustness checked: all stratum-defining conditions (tr K,
K=0, C=0) are invariant under the full Klein group, and the E08 orbit is
still {s, −s} — so strata well-definedness, every ledger verdict, and the
"s mod sign" modulus survive unchanged; only the stated moduli quotient
(k10 and C as carried moduli) is coarser than claimed.

(d) **E08 cocycle — CONFIRMED.** σ(φ)=1−e^{−φ} matches the banked 07-25 E08
definition (lower shift s·(1−e^{−φ})). My own matrix exponential of the E08
generator reproduces the map; the composition law s₁₂ = [s₁σ(φ₁) +
s₂e^{−φ₁}σ(φ₂)]/σ(φ₁+φ₂) verified from the product; associativity verified
directly **on the induced s-law** over three segments (stronger than matrix
associativity alone).

(e) **T5 cells (4 spot-checked, independent constructions of the supplied
conditions):** (E03, SO(3)) EMPTY — my own rotation-algebra commutant forces
K=I so tr K=+2 vs the required 0; (E05, SO⁺(1,2)) dim 0 = X₋₁ =
diag(−1,1,−1,−1) — my own boost+rotation commutant; (E08, swap F) dim 0, s
forced 0 — my own solve of FXF⁻¹=−X gives {c00=−c01, c10=−c11, K=0}, matching
the banked 07-27 line "reciprocal odd F: (−a,+a,−b,+b,0,0,0)"; (E02, screen
SO(2)) dim 1 = the isotropic axis with C=0, k10=0. All match the table.
Bonus: rank-13 (7 extension directions ⊕ so(1,3)) rebuilt independently.

## Duty 3 — FALSIFIER HUNTS

- **F-A: NOT FIRED.** Read the 07-26 audit's `PREMISE_SELECTOR_UNIVERSE.tsv`
  (P01–P18). Every forcing/conditioning column in T5 and every T4 pin is a
  SUPPLIED structure (stratum registrations 07-25; SO(3)/SO⁺(1,2)/swap-F/
  screen-SO(2) holonomy 07-27) — none is in the rank-zero 18-family active
  set. That set, the seal, and strong CSN appear only as UNCONSTRAINED/
  INACTIVE rows and force nothing. C1 produces typings, not eliminations.
- **F-B: NOT FIRED.** No pointwise metric-only selection of a non-scalar
  generator is claimed anywhere; "E03 covariantly defined" is a typing, not a
  selection. Spectator uniqueness is stated only in the joint stronger class
  (transverse-invariance + no-mixing, rank 7), consistent with countermodels
  E07/E08, which are carried live throughout.
- **F-D: ONE SLIP FOUND** — the finite-residual claim (Duty 2c): "the finite
  residual IS Z₂" where only "⊇ Z₂" (plus connected-stabilizer triviality)
  was derived. Exhaustiveness was never computed; explicit counterexample
  above. This is the A1 amendment. All other uniqueness/forcing statements
  checked scope-clean: every T5 EMPTY/forced cell is conditional on its
  supplied column; T6 L1 MODULUS-CARRIED and L2 MODULUS-CARRIED/two-scalar
  match the ledger evidence exactly; the E04/E05/E06 split-relative typing is
  stated as relative to the registered split, not absolute; scope stamps on
  det-exp, diagonal-K T3, full-class triad, and generic-λ centralizer are
  present and honest.

## Duty 4 — CONTRACT COMPLIANCE

T1–T6 all addressed (sections 1–6 of script and EXACT_DERIVATION.md; every
named check exists in the JSON). **T4 amendment honored:** the volume-blind
loci are DERIVED from the coframe with explicit convention stamps (4D ⇒ λ=0
axis; ruler+screen triad ⇒ λ=−1/2 line; witness slice ⇒ λ=−1/2 AND zero
shift); "1+2λ=0" is presented only as the spatial-triad reading, never cited
as banked. No acceptance criterion judges merit (F-E clean): all checks are
identity/provenance checks; the covariance typing is explicitly flagged
non-elimination. Outcome ceiling respected: no adoption, no physics selected;
outcome class O2/O3 as pre-committed. Note: `AUDIT_REPORT.md` (a promised
deliverable) is not yet in the package — expected to be written after this
verifier pass; flagging for completeness.

## REQUIRED AMENDMENT

- **A1 (finite residual understated).** Amend: EXACT_DERIVATION.md T1(b)
  ("Finite residual of the registered chart: Z₂ = {I, R_π}") and the T3
  echo ("s up to the residual Z₂ sign" — conclusion right, group wrong);
  ledger rows E02/C1 ("residual chart symmetry Z2 acts (K,C)->(K,-C)") and
  E08/C1; JSON `results.residual_finite_chart_symmetry` and
  `results.T1.equivariance_law`. Correct statement: the finite residual
  contains (at least) the Klein four-group of diagonal sign matrices
  {I, diag(1,1,−1,−1), diag(1,−1,−1,1), diag(1,−1,1,−1)} ⊂ SO⁺(1,3), acting
  by k10↦±k10 and signed C-flips; either prove exhaustiveness of this group
  or stamp "at least". Downstream: strata verdicts, T5 table, s-mod-sign all
  unchanged (verified); the carried moduli k10 and C must be read modulo
  this larger finite quotient.

Nothing committed by this verifier. Files added to the package:
`VERIFIER_INDEPENDENT_CHECK.py`, `VERIFIER_REPORT.md`.

---

# A1 CLOSURE — adjudication of the amendment (blind verifier, same-session-spawned; 2026-07-28)

Caveat travels: this verifier is **not a hosted external model**.

## VERDICT: **A1-CLOSED**

The amendment implements A1 fully and goes beyond it legitimately: the EXACT
finite-residual claim (Stab = Klein four-group, exhaustiveness proven) survives
every attack I mounted. Attack script preserved as
`VERIFIER_A1_CLOSURE_CHECK.py` (15/15, exit 0; own construction, incl. a
staging-free brute-force classification).

### 1. Rerun
Amended `derive_routeB_stage1.py`: **exit 0, 100/100**, ~2 s; regenerated JSON
**byte-identical** to committed; stdout identical to `DERIVATION_STDOUT.txt`
modulo the `wrote <path>` line. Still no floats/randomness/network.

### 2. Attack on the exhaustiveness proof — HELD
- **(a) Quantification.** The script defines the residual correctly as
  Stab = {Λ ∈ SO⁺(1,3) : ΛX₀Λ⁻¹−X₀ ∈ V and ΛVΛ⁻¹=V}, which I confirmed is
  equivalent to "Λ maps the whole affine registered class onto itself"
  (v=0 gives the X₀ condition; subtracting gives ΛVΛ⁻¹ ⊆ V, = V by
  dimension). Steps 1–4 are necessary-condition (probe) arguments correctly
  quantified over ALL class-preserving Λ — the probe member C=I₂,K=0 is IN V,
  so any class-preserving Λ must keep it in V; rows of (Λv*)Λ⁻¹ vanish iff
  rows of Λv* vanish (Λ⁻¹ invertible — the one non-machine step, elementary);
  those rows ARE the upper-right entries of Λ (re-verified independently).
  Sufficiency is separately verified per element on a GENERIC member (step 5),
  so necessity+sufficiency close the exactness pattern with no gap.
- **Independent brute force (no staging):** I handed the JOINT polynomial
  system (SᵀS=I, SᵀXb=0, Aᵀη₂A+XbᵀXb=η₂, AH₂=H₂A, k10-probe) over all 12
  block unknowns to sp.solve, filtered det=+1 and Λ⁰₀>0: **exactly four
  solutions, no free-parameter families, precisely K₄**
  (`A1c_bruteforce_*`). This reproduces the classification without the
  package's step ordering.
- **(b) η/orthochronicity legitimacy.** Classifying within SO⁺(1,3) is
  contract-correct (gauge group = connected local Lorentz group, premise
  ledger / requirement 7; matches my A1 framing "⊂ SO⁺(1,3)"). The blockwise
  ΛᵀηΛ=η identities re-verified; orthochronicity is applied only to exclude
  clock sign −1 (e.g. diag(−1,−1,1,1) has det 1 but Λ⁰₀=−1<0 — outside SO⁺),
  which is a group-membership fact, not a merit filter.
- **(c) Fifth-element hunts — all fail.** Screen rotation S(θ): k10-probe
  gives −sin²θ ⇒ θ ∈ {0,π} only. Reflection-at-angle-θ S (det −1,
  compensable by A=diag(1,−1)): conjugation entry = +sin²θ ⇒ θ ∈ {0,π},
  landing exactly on R13(π)/R12(π) — already in K₄. Screen swap: maps the
  k10 generator E21 to the UPPER-triangular E12 — breaks the chart. A
  clock-screen boost exp(ζL02) (upper-right block nonzero): maps the probe
  member out of V for ζ≠0. Degenerate-q loophole: none — q real, −q²=0 ⇒ q=0
  exactly. **No fifth element exists.**

### 3. Other A1 items — all implemented correctly
- EXACT_DERIVATION.md T1(b): exact K₄ + proof chain + named checks; T3 echo
  corrected (K₄-orbit of s = {s,−s}; R13(π) fixes s — verified: it flips
  (c01,c10) only). Ledger rows E02/C1, E08/C1 corrected; E05/C1 annotated
  (k10 mod sign) as declared. JSON `residual_finite_chart_symmetry`,
  `T1.equivariance_law`, `T3.E08_residual_orbit`, `T4.honest_L2_modulus`,
  `T6` all carry the K₄ statements.
- Moduli quotient verified independently: (λ, k_mod) K₄-invariant (diagonal
  members are fixed points); k10 orbit = {k10, −k10}; C orbits under the two
  signed-flip actions; E08 modulus still s mod sign.
- **CORRECTION_LAYER.md accuracy: HOLDS.** The did-NOT-change list checks
  out: T5 table byte-for-byte identical in content, all survival verdicts
  and L1/L2 tags unchanged; only moduli readings coarsened, exactly as
  stated. The what-changed list matches the actual diffs (T1(b), T3, T4/T6
  moduli text, ledger rows E02/E05/E08 C1, JSON, stdout, 85→100).
- **AUDIT_REPORT.md verifier record: FAITHFUL** (byte-identical rerun,
  PASS-WITH-REQUIRED-AMENDMENTS, one F-D slip = A1, robustness findings,
  caveat present). One trivial count correction, mine not theirs: my
  independent script, after I fixed two of my own coefficient-extraction
  bugs, contains **34** checks (the "33/33" in my Duty-2 text and echoed in
  AUDIT_REPORT.md was the pre-final count); all 34 pass, exit 0. No claim
  rides on the count.

Files added by this closure pass: `VERIFIER_A1_CLOSURE_CHECK.py`, this
section. Nothing git-committed by the verifier.
