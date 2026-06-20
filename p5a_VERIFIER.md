# P5a — INDEPENDENT BLIND ADVERSARIAL VERIFIER RECORD

Append-only. Verifier: claude-opus-4-8[1m] (independent, data-blind). Date: 2026-06-20.
Branch: `p5a-jfnk-precond`. Target: `p5a_jfnk_precond_results.md` + `p5a_jfnk_precond.py`.
Method: independently rebuilt the dense Jacobian J of the COMMITTED
`full3d_solver.residual_vector` via per-row autograd on grid (12,6,8) (the grid the
report inspected), nU=2880, nF=2688; SVD/eig of J and J^TJ; nullspace support analysis;
body-DOF restriction; matrix-free JVP cross-check. Scripts: /tmp/verify_p5a*.py.

## HEADLINE RULINGS

**(a) Is J genuinely ~22% rank-deficient (κ astronomical)? — STANDS (qualitatively),
numbers are threshold/method-sensitive.**
- Massive rank deficiency CONFIRMED. The exact "622/2880 = 22% at <1e-8" is REPRODUCED
  *only* via eig of the explicitly-formed dense J^TJ: I get 622 (21.6%) at 1e-8 by that
  method. But it is highly threshold/method dependent:
  - eig(dense J^TJ): 776 (1e-6) / 698 (1e-7) / **622 (1e-8)** / 580 (1e-9).
  - SVD of J (cleaner, no squaring): 430 (1e-8); rank-deficiency of J itself ~216-252.
- κ: report says 2.3e20. Independent κ(J^TJ)=max/min = **1.98e37** (SVD) — even worse,
  not 2.3e20. min eig of formed J^TJ went negative (-2.5e-13) i.e. lost SPD. Order of
  magnitude claim ("≥1e20, Krylov-fatal") STANDS; the precise figure is unreliable.
- FACTUAL ERROR in §4: "diagonals are uniform (~900)". Independent mean(diag J^TJ)=**128**,
  not ~900 (off ~7x). Not load-bearing, but the diagnosis text is wrong here.
RULING: STANDS that J^TJ is massively rank-deficient and κ is astronomical (Krylov-fatal).
The specific "22% / κ=2.3e20 / diag~900" numbers are NOT robust — calibrate to
"~10-25% near-rank-deficient, κ≥1e20, diag~O(1e2)".

**(b) Is the nullspace the edge-mask excision (supported on excised DOF, dim matches)? —
PARTIAL. Directionally right, but the report OVERSTATES it.**
- Support: 90.4% of the near-null subspace energy sits on the `Grid3D.body`-excised radial
  edge DOF (10% on body). So edge-excision is the DOMINANT driver — diagnosis is
  directionally correct.
- BUT dimension does NOT match: nullspace dim ≈ 430–622, while excised-edge DOF = 1440
  (1056 of them truly unconstrained-by-any-residual). It is NOT a 1:1 "excised DOF = null".
- The report's MECHANISM is FALSE AS STATED: §4/§1 say the excised DOF "appear in no body
  residual row → **near-zero columns in J**." Independently, edge column norms are LARGE
  (mean ~9.2, larger than body ~3.1; ZERO edge columns are near-zero). The deficiency is
  unconstrained edge-DOF *combinations* (spectral-derivative coupling + strong-BC rows
  leave a low-rank null subspace), NOT zero columns.
RULING: PARTIAL — nullspace is predominantly (90%) edge-excision-supported (path-relevant
conclusion survives), but it is NOT "the body-mask excision" wholesale and the "near-zero
columns" mechanism is wrong.

**(c) THE FORK (decisive) — restricting to body DOF MAKES J ESSENTIALLY WELL-CONDITIONED.
=> RE-POSE (option 2) WOULD RESCUE JFNK. POINTS TO #1-via-re-pose, NOT KEH-as-forced.**
- Drop the excised-edge columns (solve only body DOF): near-zero count collapses
  **430 → 1**; κ(restricted J^TJ) collapses **1.98e37 → 5.3e10**.
- The residual 5.3e10 is ONE outlier eig (4e-9). Excluding it, κ = max/2nd-min = **9.8e5**
  — healthy. Interior-rows-only on body cols: κ=2.3e5, 1 near-zero.
- The single leftover near-null mode is an inner-body (rows 3-8) a/b/c/d-coupled mode
  (likely a genuine gauge/coupling mode), NOT an edge artifact.
RULING: STANDS that re-posing to full-rank (the report's option 2) removes the
rank-deficiency cheaply. This is the report's own option-2, and it is VINDICATED as the
cheap fix. The report frames the fork as "KEH (#2) OR re-pose (#2-alt)" and leans KEH
("this result promotes it"); the EVIDENCE points to RE-POSE first: it is a small
re-scoping that recovers a well-conditioned operator and makes the anchor's success
transferable to matrix-free Krylov — KEH is the heavier fallback only if re-pose's
remaining κ~1e6 (+ that 1 mode) proves insufficient in the nonlinear tail.

**(d) Is the FAIL an honest operator property (not a JFNK/Krylov bug)? — STANDS.**
- Matrix-free JVP vs dense J@v: max rel err **1.0e-16**; VJP vs J^T@w: **1.5e-16**. The
  matrix-free operators are exact. The rank-deficiency is a property of the COMMITTED
  residual's dense Jacobian, computed independently of the JFNK loop. The FAIL is an
  honest operator property, not a JVP/Krylov implementation bug.

## DISCIPLINE CHECKS
- Residual is the committed `full3d_solver.residual_vector`, unmodified (the autograd J is
  built from it byte-for-byte). No frozen DOF / gauge / BC introduced by the verifier.
- The body-mask (`Grid3D.body`, rows [3:Nr-3]) is INHERITED from `full3d_spectral`, a
  pre-existing choice — confirmed not a P5a invention. Data-blind throughout (no wall
  numbers touched; units L=1).
- Gates not independently re-run (the §2/§3 floor numbers); the OPERATOR root-cause is the
  load-bearing claim and it is what determines the fork — that is fully verified here. The
  gate FAILs follow from κ≥1e20 on the full operator, which is confirmed.

## NET
P5a's FAIL is SOUND and its root cause is CORRECT IN DIRECTION (massive J^TJ rank
deficiency, ~90% supported on the inherited body-mask edge excision, κ astronomical;
honest operator property, not a solver bug). Three corrections to the record: (1) the
"22% / κ=2.3e20 / diag~900" figures are not robust (calibrate to ~10-25% / κ≥1e20 /
diag~1e2); (2) the nullspace is predominantly-but-not-wholly the edge excision and its
dimension does not equal the excised-DOF count; (3) the "near-zero columns in J" mechanism
is FALSE (edge columns are large; the deficiency is unconstrained DOF *combinations*).

DECISIVE FORK RESULT: restricting to body DOF collapses the deficiency (430→1) and κ
(1e37→5e10, ~1e6 excluding one mode). The evidence points to **RE-POSE the discretization
to full-rank (the report's option 2) as the cheap, JFNK-rescuing path to TRY FIRST**, with
KEH/SCF as the heavier fallback — rather than treating the FAIL as a forced jump to KEH.
Charles's call.
