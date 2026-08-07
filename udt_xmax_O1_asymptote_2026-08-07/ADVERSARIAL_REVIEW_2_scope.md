# Adversarial review 2 — triviality / faithfulness / scope (O1 asymptote probe)

Date: 2026-08-07 | Reviewer: same-session adversarial (scope direction), independent reasoning +
independent symbolic recompute (fresh sympy script, scratchpad `indep_check.py`; not the probe's
`derive_o1.py`). Reviewed: `PREREGISTRATION.md`, `DERIVATION_NOTES.md`, `derive_o1.py`,
`run_output.txt`; at source `udt_complete_pair_phi_orchestra_audit_2026-08-05/EXACT_DERIVATION.md`
+ `AUDIT_REPORT.md`; CP1 text in `udt_xmax_pair_question_MAP_2026-08-06.md`.

Independent recompute results (all confirm the probe):
- Trace law cosh(2δ) = cosh(2(p+q)) + 2 sinh²w sinh2p sinh2q re-derived exactly; det C = 1. CONFIRMED.
- Timelike labeling of the SMALL eigenvalue checked at 4 additional general (p,q,w) points beyond
  the probe's witnesses — eta-norm negative at all. CONFIRMED (probe only checked witness points;
  this closes a small verification gap in its favor).
- 3-leg twisted chain: half-trace 3944177/32768 ≈ 120.4 vs additive cosh(6 log 2) ≈ 32.0 —
  super-additivity persists beyond chain length 2. CONFIRMED.
- NEW WITNESS (item 5 below): infinite chain, leg depths log(1+2⁻ⁿ) (total budget ≈ 0.853,
  SUMMABLE), twists sinh wₙ = 2ⁿ: composite depth after legs 1..6 = 0.405, 0.739, 1.071, 1.412,
  1.758, 2.105 — grows ~linearly, DIVERGES. Bounded total depth budget does NOT keep an infinite
  chain away from the wall.

## Item 1 — the load-bearing typing (invertibility: derived or CHOSE?)

**Verdict: CHOSE at source; the probe states it honestly; headline needs the conditionality
elevated, not buried in the scope clause.**

At source (EXACT_DERIVATION.md sec.2) invertibility enters as a definition: "Let A ... be a typed
invertible comparison arrow." Nothing in the audit derives it. The nearest structural support is
sec.6: a physical signed depth MUST satisfy δ(γ⁻¹) = −δ(γ) — reciprocity motivates invertibility
for depth-CARRYING arrows — but the audit itself calls the cocycle laws "the REQUIRED type," not a
banked theorem, and the probe quotes exactly that (Ground, and (e)). AUDIT_REPORT's own OPEN line
("which strain/cocycle, if any, is the physical UDT pair depth") means the arrow set is part of an
unselected framing. So: invertibility = definitional CHOSE (motivated, not derived).

Nuance in the probe's favor, correctly drawn by the probe: ON the mu=0 lock the singular face is
closed by the reciprocal tie λ_t·λ_r = 1 (a derived structural fact of that stratum — λ_t → 0
forces partner blow-up; det C cannot pass through 0), so on-lock unreachability is tie-derived,
not pure typing. OFF the lock it is typing all the way down: the one-step singular arrow
diag(0,2,1) ATTAINS λ_t = 0 at finite entries and is excluded solely by the banked definition.
The probe's "ideal on the lock; singular off it" is the exact honest statement.

Honesty check: the probe's (d)1 states the scope edge verbatim ("If a future completion admits
degenerate/limit arrows (e.g. an actual horizon comparison), the theorem does NOT cover them");
(e) S4 relocates the content correctly ("the unreachability theorem is ABOUT the groupoid"); the
landed-outcome headline carries "within the banked groupoid of typed INVERTIBLE comparison
arrows." No overclaim in the document as written. The residual hazard is RELAY compression:
"unreachability holds" without the typing clause would overclaim, because the wall's attainability
is genuinely a TYPING/COMPLETION question (does the physical cocycle selection admit limit
arrows?), not settled physics. AMENDMENT 1: the typing-conditionality must travel in the single
headline sentence itself, on-lock/off-lock split included, in anything relayed upward.

## Item 2 — SR-parallel honesty

**Verdict: stated honestly and prominently; the asymptote reading survives at the topological
level; the SR QUANTITATIVE content is dead and the probe says so — but the death is bigger than a
"mechanism" footnote and should be named as such.**

What SURVIVES of the CP1 analogy ("same kind of function as can't-reach-c"):
- the wall is an ideal boundary point — approached, never attained, by any finite composition;
- representatives diverge on approach (entries → ∞, like SR boost matrices as v → c);
- one statement covers both extremes via reversal (δ → ±∞), as Charles asked on 08-06;
- the composition law has exactly SR's law-of-cosines FORM.

What DIED:
- sub-additivity (the actual mechanism of SR's unreachability). The inequality REVERSES:
  super-additive under boost twist, equality iff collinear/rotational.
- the uniform floor / budget control. In SR, total rapidity budget W bounds you away from c
  (v ≤ tanh W): bounded resources ⇒ bounded approach. Here two legs of FIXED depth get
  arbitrarily close as twist grows — pure boosts are DEPTH-ZERO arrows (C_L = I) living in a
  NON-COMPACT group, so "depth" is not a resource measure that controls approach at all. SR's
  zero-rapidity orientation factor is compact (rotations); that compactness is what the analogy
  loses, and it is load-bearing for SR's version of the statement.
So the result is quantitatively WEAKER than the CP1 framing (no budget protection) and
qualitatively FASTER (approach amplified, not capped). The probe's "exact in FORM, loose in
MECHANISM" plus the landed bullet "NO uniform floor on twisted chains" is honest and prominent
(it is in the landed outcome and the single-load-bearing-step line). The asymptote reading itself
survives FAIRLY — CP1 was a hard-bound-NO / asymptote-YES ruling, and asymptote-YES stands —
provided the relay says the unattainability is structural (typing + tie), not budget-enforced.

## Item 3 — super-additivity's physical reading (F-STEER check)

**Verdict: clean — no owner-favorable spin found.** The probe nowhere connects super-additivity
to the phi-angular discreteness hunch or to any coupling; its only gloss ("reverse-triangle
Lorentzian character, fitting delta_t being the TIMELIKE readout") is structural, not hunch-
flavored. Reviewer's own observation, with exact scope: the enhancement lives in the BOOST-twist
channel; the SPATIAL-ROTATION (angular) twist is EXACTLY additive/inert in this composition
(probe Q2a(iii), machine-checked for general theta) — so at this layer the datum, if anything,
points AWAY from an angular role in depth composition. Scope of that observation: kinematic
composition fact on the mu=0 stratum, 2x2/3x3 diagonal-plus-twist controls, no coupling claim, no
bearing (either way) on the hunch's actual domain (metric-function phi-angular coupling).

## Item 4 — outcome class + anti-tautology ledger + Q1 scope

**Class: O1-CONDITIONAL is the contract-honest bin — CONFIRMED.** The prereg hard-codes "the
general inequality fails or reverses — report the exact boundary of validity" as CONDITIONAL, and
it reversed; O1-THEOREM's own definition required "additivity subgroup + the general-chain
inequality," which failed. Note the fine print honestly: what is conditional is the MECHANISM/
floor (and, deeper, the invertible TYPING per item 1); unreachability-within-typing itself holds
on ALL finite chains, not just collinear ones. CONDITIONAL-in-mechanism, not
CONDITIONAL-in-conclusion. The bin is right; the reading must not degrade to "holds only for
collinear chains."

**Ledger: fair.** The definitional list (finite products of invertibles are invertible; det ≠ 0 ⇒
λ_t ≠ 0; reversal-given-banked-law) is correctly identified as the F-TRIVIAL core. S2 (the trace
law) is genuinely substantive — independently re-derived here. S3, S4, S5 substantive as scope/
structure facts. S1 (multi-axis + rotation-twist additivity) is a routine commuting computation
but a real extension of the banked collinear scope; acceptable as a derived scope fact, not
padding. F-PIN respected (depth-only, no separation measure); F-SCOPE respected (no x_max value,
no law, scale-free); F-LEGACY clean (grounds are 08-05/08-06 orchestra-era docs, cited not
imported). F-STEER credibly discharged: five escape routes genuinely hunted, and the steered-for
SR mechanism is the one thing refuted.

**Q1 characterization — one scope nick (AMENDMENT 2).** The "rank-1 projective limit with the
timelike eigenline as kernel" was computed along the reciprocal path at FIXED screen strain
(s = 1). Reviewer check: if the screen strain co-diverges at the partner's rate (s² ~ 1/λ_t) the
projective boundary point is RANK-3 diag(0,1/3,1/3,1/3); at subdominant divergence (s² ~ λ_t^{-1/2})
rank-1 is recovered. So the rank-1 statement holds only for screen strain subdominant to the
reciprocal partner; the wall's boundary stratum is a FAMILY of ideal points, of which the rank-1
point is the pure-reciprocal-path one. "Two faces" and "ideal boundary point" stand; "rank-1"
needs the subdominant-screen qualifier. Minor, but S3 as worded overclaims by that qualifier.

## Item 5 — the infinite-chain question (NEW finding, AMENDMENT 3)

The theorem is quantified over FINITE chains, and that quantifier is load-bearing. Reviewer
witness (confirmed exactly, table above): an infinite chain with SUMMABLE leg depths (total
budget < 0.86) and growing twists has composite depth diverging without bound — its partial
composites escape to the ideal point. In SR the analogous statement is FALSE (summable rapidities
⇒ bounded away from c); here super-additivity plus non-compact zero-depth twists make the wall a
LIMIT POINT of infinite chains of arbitrarily shallow comparisons. The infinite composite is not
an arrow of the banked groupoid (no finite limit exists), so attainment still fails WITHIN the
banked objects — but only because the groupoid contains no infinite composites: this is the SAME
door as item 1 (what the completion admits), not an independent protection. The probe's "already
at chain length 2" remark shows it saw the quantitative side but it never states the infinite-
chain fact. The honest physical statement is:

> No FINITE sequence of admissible (invertible-typed) comparisons attains the wall, and on the
> lock the reciprocal tie closes the singular route; but there is no depth-budget protection —
> finitely many observers with arbitrarily small total depth, or an infinite sequence of
> observers with summable depths, approach the wall arbitrarily closely / have it as their limit
> point. Attainment is a question about the completion (limit arrows), which the banked
> definition excludes and the physical cocycle selection has not yet ruled on.

## Verdict

**AMENDED — sustained on the mathematics (all load-bearing algebra independently confirmed; no
false pass found; labeling gap closed in the probe's favor), with three required amendments
before any banking:**
1. The typing-conditionality (item 1) travels in the headline sentence itself, with the
   on-lock (tie-derived) / off-lock (typing-only) split.
2. Q1's "rank-1" boundary characterization gains the subdominant-screen-strain qualifier
   (family of ideal points; rank-1 = the pure-reciprocal-path member).
3. The infinite-chain / summable-budget fact (item 5) is added to the theorem's scope statement;
   "no sequence of observers reaches the wall" must be quantified as FINITE, with the
   no-budget-protection clause stated.
O1-CONDITIONAL confirmed as the bin. Same-session caveat applies to this review as to review 1;
the external bar travels with any banking.

Honest headline for Charles (lay): "The wall really can't be reached — but not for the reason we
guessed: it's not that depths add up too slowly like speeds in relativity; it's that the wall
simply isn't a member of the comparison family, and on the locked stratum the reciprocity tie
slams that door — while, surprisingly, twisting between legs lets even shallow comparisons race
arbitrarily close, with no budget holding them back."
