# ADVERSARIAL REVIEW 2 — F-PIN / F-SHOP-CLASS / scope / tagging honesty

Date 2026-08-07 | reviewer: independent adversarial pass (F-PIN neutrality brief) | branch grok.
Scope of this review: PREREGISTRATION.md, DERIVATION_NOTES.md, derive_o2.py/run_output.txt (language
scan), parent MAP `udt_xmax_pair_question_MAP_2026-08-06.md`, O1 CONSOLIDATED, and the 08-05
copresence/P-opt probe (the posit adjudication). All realization-row integrals were independently
recomputed by hand (proper F iff n<2 with value 2R_w/(sqrt(c_0)(2-n)); optical F iff n<1, n=1
log-divergent with partial -R_w ln u; class-(iii) edges F iff p<-1 (optical n=1) and p<-2 (proper
n=2); class-(ii) divergences; d_A convention forcing via Etherington; infall integrand -> 1/epsilon;
travel time ≡ optical/c; the r/(1+z) variant -> 0 in both declared classes; degeneracy inclusions).
NO cell is wrong. This review adjudicates neutrality, not algebra (review 1 owns the recompute +
completeness attack; overlaps are flagged where language and completeness interact).

## 1. F-PIN — does anything quietly privilege one measure? VERDICT: DOES NOT FIRE; two emphasis
## asymmetries found, sub-falsifier, amendments owed

Hunted: language, row ordering, bolding, coined names, the notable-cells list, script comments.
- **Row ordering** follows the prereg's declared enumeration (abstract first, then realization in
  the contract's order). No reordering that floats finite rows. CLEAN.
- **"Angular-diameter horizon" (3h):** the coinage names the CELL's content (finite d_A at the wall
  = nonzero minimal subtended angle), not the measure's status, and sits in scare quotes with the
  gloss. It is NOT a selection — but it IS the only coined, evocative name in the table ("horizon"
  carries GR resonance), an emphasis asymmetry: divergent cells get no names. AMENDMENT A1: demote
  to a descriptive clause or append "(descriptive label; no selection weight)".
- **The optical knife-edge spotlight (3b):** the n=1 edge gets the most ink and the only bolded
  "EXACTLY the boundary case". Mitigation is real: the proper row's n=2 edge is treated in strict
  parallel (3d resolves BOTH edges, same machinery), and sec. 3d states the load-bearing deflator
  ("knife-edges, not class-stable facts"). Attention tracks mathematical structure (the two boundary
  cases of the declared family), not a wanted measure. Sub-falsifier; see item 2 for the P-opt edge.
- **The notable-cells list** is PLURAL (three cells: optical edge, d_A, budget) — no single "most
  interesting" designation exists anywhere in the package (grep-verified, script and output
  included). Listing three, spanning three different measures, is itself neutrality-preserving.
- **d_A conventions:** both computed, both in the table, three distinct behaviors reported (F,
  D-by-class, ->0). The word "adjudicated" applies to a BOOKKEEPING convention (matching the banked
  d_L record via Etherington), explicitly not physical preference, and the prereg's variant is not
  buried — it has its own table row. CLEAN.
- The load-bearing test: can Charles read the table and choose ANY row as his kernel's "spatial"
  without friction from the text? Yes — the table gives {areal, d_A, infall-tau} all-n-finite,
  proper n<2, optical n<1, budget finite, {depth, z, d_L} divergent, each with its data cost, none
  argued for. F-PIN discharged.

## 2. The P-opt knife-edge observation — VERDICT: HONEST NEUTRAL STRUCTURAL FACT, with the license
## statement owed explicitly (owner-favorable hazard real but contained)

History (re-read at source): the 08-05 probe RETRACTED "copresence derives P-opt"; corrected verdict
REFUTED; "P-opt remains a genuine INDEPENDENT assumption." The hazard: "the banked slogan IS the
n=1 knife-edge" could re-dress P-opt as structurally distinguished ("the boundary case") — a
back-door re-elevation of an adjudicated posit.

Adjudication: the observation as written does NOT re-elevate, for two structural reasons the notes
themselves contain:
1. **Knife-edge status is MEASURE-RELATIVE.** n=1 is the edge of the OPTICAL functional only; n=2
   is the edge of the PROPER functional; every n is the threshold of SOME integral criterion.
   "P-opt sits on a knife-edge" has zero selection content until a measure is chosen — and that
   choice is exactly the F-PIN-guarded choice reserved for Charles. Being the optical edge
   distinguishes P-opt only under an optical reading, which nothing here selects.
2. **The edge is not class-stable.** Sec. 3d proves log corrections push either side of the edge;
   n=1 is a boundary of the pure-power SUB-family only. The notes state this deflator explicitly
   ("knife-edges, not class-stable facts") — which actively DEFLATES rather than elevates.

WHAT THE OBSERVATION LICENSES: (a) locating the banked L/P-opt profile inside the declared class
family (one member, n=1); (b) the exact characterization "at n=1 the optical path meters depth
linearly, rate 2X per unit depth" — a property of the (measure, class) pair; (c) the cross-check
that the banked slogan is reproduced, confirming consistency of the banked record with this table.
WHAT IT DOES NOT LICENSE: deriving P-opt; upgrading its posit status in any registry; calling P-opt
"the boundary case" simpliciter (only: the optical-functional boundary of the power sub-family);
using edge-status as evidence in any later selection argument without re-arguing measure choice.
AMENDMENT A2: append this license sentence to notable-cell (A) in the landed-outcome block, so the
deflators travel with the excerpt (the body has them; the summary list — the quotable part — does
not).

## 3. F-SHOP-CLASS — VERDICT: DISCHARGED; one generality limit to tag

- Classes (i)/(ii) were declared IN THE PREREGISTRATION, committed before any integral; class (iii)
  was pre-authorized ("any further classes... state why") and the stated reason (two real
  log-divergent boundary cases inside class (i); log correction is exactly the resolving
  perturbation) is genuine completeness, verified: (iii) resolves both edges BOTH WAYS (finite iff
  p<-1 / p<-2), so it was not tuned to make a wanted row finite — it makes the wanted-adjacent n=1
  cell's verdict LESS stable, the opposite of owner-favorable tuning. JUSTIFIED.
- No cell's INTEREST depends on a covert family choice: d_A-finite is definitional of a
  finite-areal-radius wall and the table shows its class-(ii) reversal in the same row; the
  knife-edge interest carries the class-(iii) deflator.
- **GENERALITY LIMIT (overlaps review 1's completeness brief):** class (ii) is a SINGLE member
  (A = e^{-r/X}), not a parametrized family — asymmetric with class (i)'s n. Checked adversarially:
  for sub-exponential infinite-radius walls (e.g. A ~ r^{-k}) every realization-row D verdict
  survives (hand-checked), EXCEPT the r/(1+z)-variant cell: r*sqrt(A) = r^{1-k/2} DIVERGES for k<2
  — so that cell's "-> 0" and degeneracy note (4)'s "all divergent except the variant" are
  exponential-member-specific, not infinite-radius-wall facts. Also essential-singularity
  finite-radius walls (A ~ e^{-1/(R_w-r)}) sit outside (i)+(iii); hand-check: they add no new
  finite cells (proper/optical divergent; areal/d_A/infall finite as for all-n class (i)), so no
  verdict flips, but the family's coverage claim should say so. AMENDMENT A3: tag the variant cell
  and degeneracy note (4) "exponential member; member-dependent for slower decay", one line on
  essential-singularity walls.

## 4. Tagging honesty — VERDICT: SOUND; two cell-level nicks

- Data-requirement tags all verified correct at source: depth/leg-count/budget = chain-only (no
  realization used — checked against O1's construction); proper/optical/travel-time = lock (g_rr =
  1/A is the lock relation; without it the radial metric is free data); areal r = lock + areal
  anchor, chart-tagged per canon C-2026-08-06-1 — correctly NOT presented as invariant; z =
  ratio-invariant needing only the profile (1+z = e^{delta} verified); d_L/d_A = areal anchor +
  observable convention; infall = lock + WORLDLINE POSIT, honestly tagged as more structure than
  the pair (the geodesic is an actor choice, not pair data).
- OBSTRUCTED row: sound. Static-clock elapsed time measures a chosen DURATION, not a pair
  separation; any rate-ratio repair collapses into the z row. The obstruction-as-result posture
  matches the prereg's O2-OBSTRUCTED class.
- Degenerate collapse travel-time ≡ optical/c: verified identical under the lock + observer
  normalization (c_eff(r) = cA(r)); keeping the row for enumeration honesty is correct practice.
- NICK 1 (AMENDMENT A4a): the table's leg-count cell says "wall unattained (O1)" WITHOUT the
  infinite-chain caveat; the caveat lives in sec. 2(b) prose. The table is the excerptable
  artifact; the caveat must travel in it (footnote: "finite chains only; infinite summable-budget
  chains accumulate — O1").
- NICK 2 (AMENDMENT A4b): the budget cell "F (<= ~0.85)" states a WITNESS-specific number (O1's R2
  construction) tersely enough to read as universal. Sec. 2(c) is careful ("bounded above by the
  witnesses; infimum not determined"); the cell should say "F (witness-bounded; infimum
  undetermined)".

## 5. Scope + handoff — VERDICT: CLEAN; O3 sentence and decision aid supplied

- Grep-verified: no selection, no kernel ruling, no law language, no x_max value, no cosmology
  numbers anywhere in the package (notes, script, output). The L profile appears only as the n=1
  witness. F-SCOPE discharged. F-LEGACY: all citations 08-05/08-06 banked material — legal.
- The infinite-chain caveat IS carried on the abstract rows in prose (2b, 2c both state it); table
  cell fix = A4a above.
- **O3 handoff sentence (recommended verbatim):** "O2 delivers the characterization only; O3 (the
  approach-profile classes and what the kernel's finiteness posit conditionally selects) is gated
  BEHIND Charles's CP2 ruling — the table now exists, so the kernel's 'spatial' meaning is ripe for
  his choice of row(s), and every O3 selection statement will be conditional on that ruling plus
  the kernel posit, within the MAP's X3 scope (F-LAWHUNT in force: approach-class only, never the
  law's form)."
- **Neutral decision aid for Charles (one paragraph, no recommendation) — see final report; the
  same text should be placed verbatim in the notes' landed-outcome block or the handoff doc.**

## OVERALL VERDICT: **AMENDED** (no cell changes; no falsifier fired)

F-PIN does not fire; the P-opt observation is honest with its license made explicit; the class
family was declared and un-tuned; tags are sound; scope clean. Amendments owed before banking:
A1 (demote/annotate the "angular-diameter horizon" coinage), A2 (license sentence on notable-cell
(A)), A3 (member-specificity tag on the class-(ii) variant cell + degeneracy note 4; one line on
uncovered wall shapes), A4a/A4b (leg-count caveat and witness-bound wording IN the table cells).
All are wording/caveat amendments; the mathematics and the table's verdicts stand as computed.
