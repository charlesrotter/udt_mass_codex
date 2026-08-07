# O3 ADVERSARIAL REVIEW 2 — F-LAWHUNT / F-STEER / F-PIN neutrality + scope + tagging honesty

Reviewer: R2 (independent, hostile; adjudicates honesty, not primarily algebra — leaned-on cells
spot-verified by hand). Date 2026-08-07. Inputs read: PREREGISTRATION.md, DERIVATION_NOTES.md,
derive_o3.py, run_output.txt, parent MAP `udt_xmax_pair_question_MAP_2026-08-06.md` (X3 scope,
falsifiers, CP2 NO-PIN ruling), O2 DERIVATION_NOTES.md CONSOLIDATED (license verbatim duty).
Nothing committed by this review.

## 0. Contract conformance + machine checks run by R2

- Derivation stayed inside the frozen prereg: deliverables D1/D2/D3 all present, shortlist S1-S9b
  all carried, family (i)/(ii)/(ii')/(iii)+essential-noted matches prereg §3, no additions.
- run_output.txt: 94 keys, all True; script has exactly 94 `key(` calls; float-free (grep clean);
  exact sympy only; bounded (~2 s CPU). NOTE: run_output.txt contains NO language scan (the
  dispatch expected one included); R2 ran its own — see §5d.
- Legacy scan: every date cited is 2026-08-06/07; 08-05 material reached only through O2. Clean.
- Scope scan: no x_max value, no cosmology numbers, no mass, no law claim; the only "the law"
  tokens are inside falsifier definitions. Clean.
- **License verbatim check (machine diff): PASS.** The P-opt license in O3 §5b is character-
  identical to O2 CONSOLIDATED (379 chars, whitespace-normalized across markdown line-wraps only).

## 1. Spot-verifications by hand (cells my adjudication leans on) — ALL CONFIRMED

- S4/(ii') alpha=2: A=(1+r/X)^-2, 1+z=1+r/X, r/(1+z)=rX/(X+r) monotone -> X; sigma4=X^2/(X+r);
  (1+z)*sigma4 = X exact, all r. The headline surprise is real.
- S1 window/value: finite iff n<2, 2R_w/(sqrt(c0)(2-n)). S2: finite iff n<1, R_w/(c0(1-n));
  n=1 exactly log-divergent, partial length R_w*t = 2R_w*delta at c0=1,n=1.
- kappa's: S3 n/2 (exact residual), S1 n/(2-n), S2 n/(2(1-n)); 1/kappa = 2/n - 2m linear, slope
  -2; spacing 1/k_areal - 1/k_proper = 1/k_proper - 1/k_optical = 1, n-free. Confirmed.
- kappa sweeps (0,oo) in each surviving window: n/2 on (0,oo); n/(2-n) on (0,2); n/(2(1-n)) on
  (0,1) — each is a continuous bijection onto (0,oo). The F-LAWHUNT discharge is genuine, not a
  paper-over: no branch constrains the coefficient, so nothing soft-selects an n.
- S5 identity ln d_L = 2*delta + ln r (delta = -(1/2)ln A): immediate. Edge witnesses (proper
  p=-4: delta*ell -> 1; optical p=-2: delta*sigma -> 1/2), S7 exact witness 2R_w(sqrt(1+h^2)-h),
  S4(i) interior max u=n/(n+2), essential delta = 1/(2s) exact: all re-derived, correct.
- No leaned-on cell found wrong.

## 2. F-LAWHUNT (primary): DOES NOT FIRE

- Every D2 statement is a class with (n, p, alpha) free; the kappa-sweep argument (above) is the
  substantive discharge — the approach COEFFICIENT is unconstrained by every branch, so the class
  statement cannot smuggle a value of n.
- The reciprocal-kappa arithmetic progression is presented as a family invariant ("independent of
  the free profile data"), not as evidence for any law or member — checked: no "natural/
  distinguished/uniquely" language anywhere near it. NOT dressed as law-evidence.
- The S4/alpha=2 cell: the exact kappa=1 profile is the one place a member is singled out. §3
  states it correctly as CONDITIONAL selection ("Under S4 the posit selects EXACTLY {(ii'),
  alpha=2}"). §4e's gloss "selected by nothing" is in slight tension with §3 — amendment A5
  (wording only; the conditional architecture holds).
- n=1 named only with the license attached (verbatim — §0). No drift into deriving P-opt.

## 3. F-PIN under the NO-PIN ruling: DOES NOT FIRE — AMENDED (rhetoric, not architecture)

- Architecture sound: all nine branches carried with per-branch conditional statements, same
  format, same standard applied (S4's degenerate cells and S9a graded by the same zero-separation
  criterion); no branch named "the natural spatial"; ordering = prereg shortlist order.
- The distance-role/rapidity-role split ITSELF is a neutral, checkable classification (can the
  wall sit at finite separation for some family member — a fact per row), and CP1 (Charles's own
  SR ruling) licenses reading divergence as the asymptote. The split is legal.
- BUT four sentences cross from classification into PRESCRIPTION — telling Charles what his posit
  "is about" or where it "belongs," which under NO-PIN narrows his choice by rhetoric:
  (a) §2 opening: "The kernel's posit ... IS a statement about a DISTANCE-like row being finite
      WHILE the depth-like rows diverge" — asserts the posit's meaning; that assignment is
      exactly the choice Charles declined to make. [A1]
  (b) §3 S6: "the honest conclusion under this branch is that the posit was never about this
      row" — interprets Charles's intent for him. [A2]
  (c) §3 S8: "The kernel needs no finite value HERE; its 'finite' clause belongs on a
      distance-role branch while S8 plays the rapidity role" — prescribes relocation of the
      posit. [A3]
  (d) S5 garnish: "a depth-carrier in disguise" / "wearing a distance name" — the identity
      ln d_L = 2*delta + ln r is honest math and stays; the disguise rhetoric argues d_L is not
      really eligible as a distance. [A4]
- LOAD TEST after amendments: Charles can adopt ANY row. For z/d_L the package's statement is the
  clean modus tollens (posit unsatisfiable in the frozen family — an outcome, with the CP1
  reading available), which is forced by the mathematics, not by rhetoric. PASSES with A1-A4.
- The modus-tollens entries (S5/S6/S8/S9b) otherwise read as honest per-branch outcomes; the
  "in the frozen family" scoping (the second exit: the family, not the posit, could give) is
  carried on S5 and stated definitionally-family-independent on S6 — correct and honest.

## 4. F-STEER: DOES NOT FIRE

- KERNEL-FAVORABLE hazard (blanket infinite-radius exclusion): NOT granted. §5a R-1 is explicitly
  qualified per-branch, the S4 break is stated inside R-1 itself at the same temperature, and the
  S4/alpha=2 anti-blanket cell is SURPRISE #1 in §7 — headline weight, not buried. Verified the
  break is real by hand (§1).
- L-UNFAVORABLE hazard (optical kills n=1): stated with the O2 license character-for-character
  (machine diff, §0); the exclusion is bolded exactly as the favorable S4 break is bolded — equal
  temperature; the §5b sentence "the optical branch excluding n=1 is exactly as conditional as
  the (ii)-exclusions that flatter the kernel; neither is savored" is accurate to the text.
- SR framing: "exactly SR's structure" is licensed by CP1 verbatim ("the SAME math", Charles
  2026-08-06). The S8 superlative "the branch where the wall behaves most like SR's c" is
  supported by the cited pair (O1 unreachability + O2 full-budget divergence) — S8 is the unique
  row carrying both protections, so "most" is cell-supported, not flattery. No cell claims the
  gamma-asymptote reading beyond what the divergences show. A1's rewrite removes the one place
  the SR frame was attached to the KERNEL rather than to the family.

## 5. F-SHOP-CLASS / F-SCOPE / F-LEGACY + tagging honesty: AMENDED (minor)

- (a) F-SHOP-CLASS: DISCHARGED. No family additions. The (ii') exact representative
  (1+r/X)^(-alpha) is a representative CHOICE inside an already-frozen class, declared up front
  (§1 + script header) with a stated non-verdict cause (regularity at r=0; A(0)=1 matches the
  banked observer normalization phi(0)=0 — the singular (r/X)^(-alpha) form cannot satisfy it).
  Legal. HOWEVER the S4-genuine cell leans on the representative: R2 checked that the wall value
  X is TAIL-GENERAL (any A ~ (r/X)^(-2) gives r*sqrt(A) -> X) but MONOTONICITY/injectivity is a
  member property of the declared representative. One honesty line owed. [A7c]
- (b) F-SCOPE: DISCHARGED (scan §0).
- (c) F-LEGACY: DISCHARGED (scan §0; 08-05 reached only through O2, as prereg requires).
- (d) Tagging: chart tags present in §3 (S3 "lock+areal anchor", S5 "anchor+observable", per
  canon C-2026-08-06-1) but D2 rows carry them only by reference — one traveling line owed
  [A7b]. S7 worldline-posit tag travels (§3, §5c) — GOOD. Asymptotic-vs-exact labeled precisely
  throughout D2 (exact residuals vs o(1) vs exact-everywhere) — GOOD. ESS hand-check tags honest
  (assembly by hand, ingredients machine-checked). FIVE keys are hardcoded `True` definitional
  placeholders (chart-location-by-construction: S3_ii, S3_iiprime, S3_iii, ESS_S3,
  D3_S4gen_excluded_S3) and S2_i_n1_rate is a hand-substituted tautology — the claims are true
  but "94 machine-check keys" overstates what the machine verified; one honesty line owed. [A7a]
- (e) Outcome class: O3-MAP is the right landing (branches do not collapse; the map completed).
  BUT §7's "neither of which obstructs its whole branch question" contradicts §3's own grade of
  S9a ("obstruction-grade ... as a selection question" — there the whole branch question IS the
  obstruction). Wording fix owed. [A6]

## 6. AMENDMENTS OWED (exact wording where demanded)

- **A1 (§2 first sentence — F-PIN).** Replace "The kernel's posit "x_max is finite" is a
  statement about a DISTANCE-like row being finite WHILE the depth-like rows diverge — exactly
  SR's structure:" with: "Within the frozen family, some rows CAN carry a finite wall value
  while others necessarily diverge — SR's structure (CP1): the bounded speed variable vs the
  divergent rapidity. WHICH role the kernel's 'spatial' plays is Charles's open choice (CP2
  no-pin); the split below classifies the ROWS, it does not assign the KERNEL."
- **A2 (§3 S6 — F-PIN).** Strike "the honest conclusion under this branch is that the posit was
  never about this row." Replace with: "the modus tollens is the outcome: IF spatial = z, THEN
  the finiteness posit is unsatisfiable — an outcome, not a failure; under CP1 this divergence
  is the asymptote statement itself."
- **A3 (§3 S8 — F-PIN).** Strike "The kernel needs no finite value HERE; its "finite" clause
  belongs on a distance-role branch while S8 plays the rapidity role." Replace with: "Reading 2
  is available regardless of whether S8 is adopted as the kernel's spatial; adopted as spatial,
  S8 renders the posit unsatisfiable — an outcome, not a failure."
- **A4 (S5 rhetoric, §2 and §3 — F-PIN).** Keep the identity and the near-wall form; strike
  "a depth-carrier in disguise" and "its divergence is the S6 divergence wearing a distance
  name"; use "d_L's divergence is depth-driven (the (1+z)^2 factor; ln d_L = 2*delta + ln r)".
- **A5 (§4e — F-LAWHUNT hygiene).** Replace "selected by nothing (F-PIN)" with "selected by no
  branch unconditionally; conditionally under S4 it is the unique genuine survivor (§3)".
- **A6 (§7 — outcome tagging).** Replace "neither of which obstructs its whole branch question,
  so O3-OBSTRUCTED is not the landing" with: "the S4 cells do not obstruct the S4 branch
  question (one genuine member exists); the S9a row IS obstruction-grade as a whole branch
  question (§3) and is carried as row-grade O3-OBSTRUCTED(S9a) INSIDE the O3-MAP landing".
- **A7 (tagging honesty, three lines).** (a) After "94 machine-check keys, all True" add: "(5
  keys are definitional placeholders — chart location by class construction — and the S2 n=1
  rate key is a hand-substituted identity; the remaining 88 are computed)". (b) Add to the §4
  header: "the §3 branch tags (areal-anchor chart tag on S3/S5; the S7 worldline posit +
  proviso) travel into every D2 row". (c) Add to the §3 S4 entry or §4e: "wall value X is
  tail-general within (ii'); the monotonicity/injectivity statement is for the declared regular
  representative". (d) Record in the notes that run_output.txt carries no language scan; R2's
  independent scan (superlatives/selection language/scope/legacy/floats) came back clean.

## 7. §final — CONDITIONAL ADOPTION AID (one neutral sentence per branch; no recommendation)

What adopting each row as the kernel's "spatial" would commit to, per this package:

- **S1 (proper length):** a finite-chart-radius wall with profile class (i) n < 2 or the n=2
  log-suppressed edge (p < -2); n=1 survives; approach class log-depth with kappa = n/(2-n).
- **S2 (optical/travel time):** a finite-chart-radius wall with n < 1 or the n=1 edge
  (p < -1); the n=1 member itself is excluded (license: this locates, does not derive, and
  selection content was zero until precisely this choice); kappa = n/(2(1-n)); strictest window.
- **S3 (areal/d_A):** only that the wall sits at finite chart radius — every steepness survives
  (all n, all p, essential walls); carries the areal-anchor chart tag; kappa = n/2.
- **S4 (r/(1+z)):** exactly the (ii') alpha=2 member (an infinite-chart-radius wall at finite
  separation X, exact kappa = 1), incompatible with jointly demanding S1/S2/S3/S7 finiteness;
  every other member renders the row non-injective (zero-separation degeneracy).
- **S5 (d_L):** the finiteness posit is unsatisfiable in the frozen family (d_L diverges in
  every member; divergence is depth-driven) — either the posit or the family would have to give.
- **S6 (z/depth):** the posit is unsatisfiable definitionally (the wall IS delta -> oo);
  finiteness and z-as-spatial cannot be held together; the divergence is CP1's asymptote.
- **S7 (infall proper time):** the same in/out pattern and approach class as S3 (kappa = n/2)
  at the price of the worldline posit and the eps^2 > sup A proviso — no added selection power.
- **S8 (full budget):** the posit is unsatisfiable in every class; the wall is then doubly
  protected (unreachable and infinitely costly) — the SR-like reading needs no finite value.
- **S9a (depth-only budget):** a degenerate row (inf = 0; not a distance) — "finite" is vacuous
  and selects nothing.
- **S9b (leg count):** the wall at no finite count (finite chains; the infinite-chain caveat
  travels) — finiteness unsatisfiable there.

## VERDICT: AMENDED (A1, A2, A3, A4, A5, A6, A7)

No falsifier fires. F-LAWHUNT: does not fire (kappa-sweep discharge genuine; no member
soft-selected). F-PIN: does not fire as architecture — but four prescriptive sentences (A1-A4)
must be neutralized for the NO-PIN load test to pass cleanly. F-STEER: does not fire (S4
anti-blanket cell at headline weight; the n=1 exclusion carries the O2 license character-for-
character at equal temperature). F-SHOP-CLASS/F-SCOPE/F-LEGACY: discharged (A7c one-line
representative tag owed). Tagging: honest with the A6/A7 fixes. All spot-verified cells correct;
no leaned-on cell wrong. Reviewer: R2, 2026-08-07. Nothing committed by this review.
