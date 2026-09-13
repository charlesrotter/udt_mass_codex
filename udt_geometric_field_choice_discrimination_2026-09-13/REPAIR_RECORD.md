# NR2 — bounded same-premise implementation repair

Initial candidate_exact: exit1,49/50. Finite coincident_diagnostic: exit1,5/6.
Both original failures remain. The original matrix at t=1 is finite and has
repeated measurement rows, rank2 and determinant0. The determinant limit is0.
SymPy1.13.1 produced a removable 0/0 determinant representation; even simplify
retained the quotient. Thus the extra diagnostic expectation that simplify
would resolve substitution also failed. Neither failure changes the analytic
map or the candidate claim.

Repair: evaluate the ORIGINAL matrix at the specified coincident event BEFORE
computing its determinant; add exact repeated-row and rank2 checks. Only this
evaluation order and those two checks change in check_candidate_repaired.py.
Original check_candidate.py, EXACT_RESULT.json and captures remain untouched.
No tolerances, physical premises or claim scope are changed. This record and
the repaired-script hash are frozen before the repaired run. Fresh review must
inspect the actual matrix and proof, not count the first failure as a pass.

Two-sample b=2 proof detail: 0<nu log2<3/2<pi because sqrt7/2<3/2 and
0<log2<1. Hence sin(nu log2)>0 and the x coefficient is also nonzero.
This exact inequality is the proof; the50-digit determinant is descriptive.

The larger arbitrary smooth aligned-profile family is not covered by the
finite-family uniqueness or sign-classification claims. Smooth flat zeros can
permit independent sign changes between disjoint profile lobes while retaining
quadratic histories. No complete quadratic-history classification is asserted.
