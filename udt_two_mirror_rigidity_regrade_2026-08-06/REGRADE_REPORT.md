# RE-GRADE REPORT — the 2026-07-02 two-mirror rigidity (point-of-use)

Date: 2026-08-06. Branch: grok. Contract: `PREREGISTRATION.md` (frozen; obeyed).
Target: NEGATIVES_REGISTRY.md universe-cell banner (lines 160–182, T1 leg + sharpened corollary);
source doc `universe_cell_vacuum_impossibility_results.md` (2026-07-02, verifiers a717881d0ebb76695
and ae809e82d61ee86a2). Mode: documentary + bounded symbolic; no new physics; registry NOT edited
(reviews come first); nothing committed.

---

## R1 — EXACT ALGEBRA AT SOURCE: **YES, EXACT** (fresh independent sympy; 17/17 checks True)

Script: `verify_regrade_r1_fresh.py` (this package; written from the source doc's stated premise
set, NOT copied from the 2026-07-02 scripts). Stdout: `R1_STDOUT.txt`. Premise set re-derived from
scratch: reduced Lagrangian L = (Z/2)ρ²φ'² − 2e^{−2φ}ρ'² + 2 on the round-static Branch-P metric
ds² = −e^{−2φ}c²dt² + e^{2φ}dr² + ρ²dΩ; arbitrary φ-blind source S(r) in the ρ-equation only.

| Check | Result |
|---|---|
| C1 EL equations of L reproduce the banked 07-01 EOMs verbatim | True (both) |
| C2 flux identity (Zρ²φ')' = 4e^{−2φ}ρ'² on the φ-EOM ALONE; ρ'' never appears (so an arbitrary φ-blind ρ''-source can never enter); Z cancels in the RHS | True (all three) |
| C3 rigidity chain: Φ(a)=Φ(b)=0 + Φ'≥0 ⇒ Φ≡0 ⇒ φ'≡0 (ρ>0, Z≠0) ⇒ Φ'≡0 ⇒ ρ'≡0 | True (each algebraic step exact) |
| C4 φ'≡0 ⇒ Δφ = 0 ≠ ln(1101) — the anchor cannot be carried | True |
| C5 SHARPENED leg: regular center ⇒ Φ(0)=0 AND Φ'(0)=4 exactly (independent of φ₀ and Z) ⇒ Φ>0 off-center, monotone ⇒ can never meet an outer φ'=0 mirror ⇒ NO solution | True (exact series) |
| C6 Route-B fork: mixing term = 4ρρ'φ' exactly; Φ_B = 8ρ²φ'+4ρρ'; SAME nonneg RHS; full mirror seal zeroes Φ_B at both ends (rigidity survives); φ'-only seal leaves Φ_B = 4ρρ' ≠ 0 (L1/L2 sharpness confirmed) | True (all five) |
| C7 flipped EL-sign convention: Φ non-INCREASING, same squeeze | True |

**Verdict R1: the original derivation stands as exact conditional mathematics, INCLUDING the
sharpened center+one-mirror no-solution leg and both recorded fork-robustness legs (Route-B with
full mirror seal; sign convention).** The single mathematical load-bearing object is the flux
monotonicity identity (Zρ²φ')' = 4e^{−2φ}ρ'² ≥ 0 for arbitrary φ-blind sources; every conclusion
is squeeze logic on it. No error found; nothing weaker than claimed; C5/C6 are if-anything STRONGER
at source than the registry's one-line summary.

---

## R2 — PREMISE RE-TAG under the corrected frame (every premise, one tag each)

| Premise | Tag | Citation |
|---|---|---|
| (a) The specific 2026-07-01 native EOM set (Route-A action L, or Route-B + forced mixing) | **CHOSEN-LAW** | `udt_vary_phi_not_metric_probe_2026-08-06/` (EH on the lock = null Lagrangian; 2 reviews) + LIVE.md 08-06 block items 2–3: the depth profile is left unconstrained by every structure examined — free-data inference; no structure forces this bulk law-set. It is A lawful reduction, not THE law. |
| (b) Pointwise-φ reading | **CONDITIONS-CHANGED — but the CONCLUSION survives at ratio level** | `udt_relational_phi_dependency_regrade_2026-08-05/AUDIT_REPORT.md`: pointwise φ = presentation potential; this entry is one of exactly three negatives stripped of UDT-wide blocking authority ("their exact ODE or algebra can still be true inside the explicitly supplied pointwise scalar, action, source, branch and boundary premises"). The rigidity's DERIVATION runs inside the supplied pointwise presentation (absorbed into S), but its CONCLUSION is a two-point difference: φ'≡0 ⇒ Δφ = 0. The anchor is already a Δφ statement (canon C-2026-07-02-1; LIVE 08-06: the invariant is the two-point ratio e^{−2Δφ}). Constant-reference presentation freedom moves φ, not φ' or Δφ. The discriminator does NOT lean on the withdrawn absolute-φ ownership. |
| (c) Mirror seal φ'=ρ'=0 at both ends | **CHOSEN-GERM** | `udt_p4_seam_closure_derivation_2026-07-30/AUDIT_REPORT.md` OC2: closure is genuinely free on the banked record — τ ∈ {fold-quotient, partner, glue+B, open-end}; the selector (boundary action D-a/D-b/D-c) is MISSING. The rigidity binds ONLY the fold-fold closure. (The source doc itself tagged this "CHOSE" and noted the canon odd fold φ→−φ pins φ=0 with φ' FREE — a Class-B escape; consistent, now germ-precise.) |
| (d) φ-blind matter (all matter/interface/seal sources) | **CHOSEN-LAW (component of S)** | Source doc's own ledger: DERIVED for the winding sector — but that derivation lives inside the 07-01 law-set (tag (a)) and the winding carrier is itself a posit (memory: matter-carrier-is-a-posit, 2026-07-10); PREMISE outright for the N=0 bulk (fork 2 in the source doc). Net: conditional, rides S. |
| (e) Round-static Branch-P reduction (static, round h=ρ²Ω, diagonal, W=1) | **STANDS as-scoped** | Correctly scoped at source ("all results SCOPED to this reduction — none is a frame verdict"); nothing in the corrected frame changes the scoping; it is a regime restriction inside S, not a law claim. |
| (f) ρ>0 on the closed interval; Z≠0 (values Z-independent) | **STANDS** | Re-verified: Z cancels in the flux identity (C2); ρ>0 is the cell definition (source L4: ρ→0 = metric degeneration terminating the geometry). |
| (g) Route-A φ-equation | **STANDS (fork-robust for the fold-fold seal)** | Re-verified C6: under Route B the full mirror seal still zeroes Φ̃ at both ends. The φ'-only version fails under Route B — exactly as the source recorded. The Z=8/Route-B live-solver tension remains OWED (source doc NEXT #3), untouched here. |

---

## R3 — THE RE-GRADED STATEMENT

**Surviving conditional (exact):**

> **WITHIN S** = { the round-static Branch-P reduction (static, round, diagonal, W=1) of the
> CHOSEN 2026-07-01 native law-set (Route-A action L = (Z/2)ρ²φ'² − 2e^{−2φ}ρ'² + 2, or Route-B
> with its forced mixing term); ALL matter/interface/seal sources φ-blind; ρ>0 on the closed cell;
> Z≠0; the supplied pointwise-φ chart as presentation }:
> **the fold-fold (two-mirror, φ'=ρ'=0 both ends) closure admits NO profile carrying
> Δφ = ln(1101) — indeed no non-constant profile at all (φ'≡ρ'≡0, the constant cylinder); and the
> center + one-fold configuration admits NO solution whatsoever.** The Δφ-form of the conclusion
> is presentation-invariant (survives the 08-05 constant-reference freedom).

**What does NOT survive:** any unconditional "the universe cell cannot be two-mirror." Three
independent conditionalities each block the unconditional reading: (i) S is a CHOSEN law-set — the
08-06 free-data inference finds no structure forcing it, so the rigidity says nothing about other
lawful completions of the profile; (ii) the fold germ is CHOSEN — OC2's germ freedom {fold, glue+B,
partner, open-end} with the selector missing means "the universe cell's closure IS fold-fold" was
never derived; (iii) the 08-05 regrade strips UDT-wide blocking authority — the entry cannot
exclude relational observer-pair laws, native matter, or stability families. Also not surviving:
R3's original "falsifiable BVP" framing (already superseded at source by T1 itself).

**Contribution as the FIRST ROW of the Global Cell Assembly closure-admissibility table (Q1
prototype):** precisely scoped, this entry becomes the prototype row of a closure↔profile-data
admissibility table: for each closure germ pair (from OC2's set) × law-set, does the closure class
admit the anchor data Δφ = ln(1101)? Row 1 reads: **(fold, fold) × S → INADMISSIBLE (exact,
blind-verified twice at source + fresh re-verification here); moreover (regular-center, fold) × S →
EMPTY.** The row's value to the assembly is exactly its conditionality: it converts "which closure
does the universe cell take?" from taste into a discriminator — IF the anchor datum is carried and
S holds, the closure is NOT fold-fold (within S the unique in-reduction survivor is a Class-B
φ'≠0/flux-type outer seal, the source doc's fork 1). It rules on no other row, selects no germ, and
says nothing outside S. No G18 ruling is made or implied here (F-SCOPE).

---

## OUTCOME CLASS: **RG-DISCRIMINATOR**

Algebra stands exactly (R1, 17/17, sharpened leg included); the entry re-grades from a scoped
universe-cell impossibility to a clean conditional closure↔profile discriminator — fold-fold + S
forbids the anchor data — first row of the Q1 table. RG-DISSOLVES was given equal care (F-STEER):
dissolution would require a corrected-frame premise change that breaks applicability entirely, but
(1) the 08-05 regrade explicitly PRESERVES the algebra inside the supplied premises, (2) the
fold germ remains a live, corpus-banked closure (OC2: both witness germs banked in use), so the row
is non-empty, and (3) the conclusion's Δφ form survives the presentation-freedom correction — no
leg of the derivation's applicability is broken, only its unconditional force. RG-STANDS-STRONGER
was also rejected: the unconditional universe-cell reading is genuinely lost (tags a–d).

**Single load-bearing step of the re-grade:** the presentation-invariance of the conclusion —
φ' and Δφ are unchanged under the 08-05 constant-reference freedom, so the 08-05 pointwise-φ
withdrawal (the corrected frame's sharpest premise change) demotes the entry's SCOPE without
touching its ALGEBRA; this is what lands RG-DISCRIMINATOR rather than RG-DISSOLVES, and it is the
step reviews should attack first (is the presentation freedom really only reference-shift at the
level this conclusion uses? — the anchor's canon form C-2026-07-02-1 and the LIVE 08-06 invariant
ratio both say yes at ratio level).

Package: `verify_regrade_r1_fresh.py`, `R1_STDOUT.txt`, this report. Registry edit deferred to
post-review per contract. Agent: point-of-use re-grade agent, 2026-08-06.

## CONSOLIDATED (2026-08-06, both reviews in): RG-DISCRIMINATOR — AMENDED (sustained in substance)

Files: ADVERSARIAL_REVIEW_1_algebra_invariance.md (AMENDED), ADVERSARIAL_REVIEW_2_classification.md
(SUSTAINED-as-class / AMENDED-as-row). Independent recomputes: 17/17 and 28/28, all exact.

**Sustained:** the algebra (flux identity = the phi-EL; squeeze; sharpened center leg) is exact; the
load-bearing presentation-invariance step HOLDS with R1's supplied lemma (phi -> phi + c maps the
law-set to itself with Z -> Z e^{2c}, Phi -> e^{2c} Phi; the squeeze uses only shift-stable
positivity, so phi' == 0 => Delta phi = 0 survives at ratio level, Routes A and B). RG-DISSOLVES
rightly rejected. NOT vacuous: S is the unique banked law-set candidate, robust across Routes A/B.

**AMENDMENTS (mandatory, applied here):**
1. **Re-key the row to the BC-CLASS, not germ names.** The rigidity binds the class
   **"both ends impose phi' = 0"** = {the EVEN fold seal (phi'=rho'=0); OPEN-END (natural BCs force
   phi'=0 both ends, both routes — new reach, previously unrecorded); glue with B==0 (well-posedness
   forces q=0 => phi'=0 — conditional reach, previously unrecorded)}. **The canon/OC2 ODD fold
   (phi -> -phi: phi=0 at the seam, phi' FREE) ESCAPES** — it is the source's own fork-1 survivor;
   generic glue (Delta Pi = q/2, flux-carrying) also escapes. **NO pressure on G18's fold.**
2. **Two-direction caveat:** the row rules out the CONJUNCTION {phi'=0-both-ends closure, S, the
   anchor} — it cannot say which member fails; independently adopting the BC-class would indict S.
3. **S-caveat:** S (the 2026-07-01 law-set + phi-blind sources) is UNFORCED (08-06 free-data
   inference) but the unique banked candidate; conditional robust across Routes A/B.
4. Chart-dressing nit: "Phi'(0)=4" is chart-dressed (4e^{2c}); only its POSITIVITY is invariant
   (which is all the argument uses).

**Q1 TABLE ROW 1 (final, amended wording):** WITHIN S, given the anchor Delta phi = ln(1101):
closures imposing phi'=0 at BOTH ends (even-fold seal; open-end; glue-B==0) admit NO carrying
profile (and regular-center + even seal admits NO solution at all); the ODD fold and generic glue
ESCAPE (admissible at this row's level). Conjunction-scoped per caveats 2-3.
