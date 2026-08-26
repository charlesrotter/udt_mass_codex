# G268 evidence-repair preregistration

Date: 2026-08-26
Trigger: fresh external disposition `ACCEPT_WITH_REPAIRS`

## Frozen repair scope

The scientific question, `R0+R2+O1` landing, source universe, and maximum conclusion are unchanged.
Only the two evidence defects identified in `EXTERNAL_REVIEW.md` may be repaired.

### R1 — symbolic-proof honesty

- Replace hardcoded finite-rank positivity with an exact exponential representation whose numerator
  and denominator positivity are mechanically queried under real-depth assumptions.
- Replace hardcoded composition-denominator positivity with its exact positive rational factorization
  in positive `r1,r2`.
- Replace hardcoded inverse positivity with the already-proved depth parameterization and mechanical
  positivity of `exp(-delta)`.
- Retain a global-diffeomorphism summary only if it is computed as the conjunction of actual inverse,
  rank, and positivity checks; do not count it as an independent symbolic assertion.
- Remove zero relation rejection, zero history rejection, and open operational ownership from the
  symbolic-check dictionary. Retain them only as explicitly labelled analytic or premise-scope
  conclusions in the result ledger.

### R2 — genuine mutation catches

Build one exact-rational `validate(candidate)` path that checks forward/inverse mapping, reversal,
composition, circle membership, ideal-endpoint rejection, zero history selection, and open protocol
ownership. Establish that the baseline candidate passes. Then inject eight separate mutated candidate
functions/flags matching the preregistered failure modes and require each mutation to make that same
validator return at least one named failure. Record the actual failure names, not booleans asserting
that a bad statement is bad.

`verify_package.py` must require baseline success, eight nonempty mutation-failure sets, and the
expected targeted failure class for each mutation.

## Repair falsifiers

- Any hardcoded truth remains in the exact symbolic-check dictionary for a flagged item.
- Any mutation is declared caught without executing changed logic through the shared validator.
- Baseline validation fails.
- A mutation produces no failure or only an unrelated file/metadata failure.
- Scientific landing, physical premise status, or open scope changes.

## Verification and grade

After repair, rerun production, independent exact-rational replay, real mutation injection, package
no-write replay, and the full repository suite. Then seal a repair-only follow-up intake. Until the
same external reviewer or a fresh repair-only reviewer accepts R1 and R2, grade remains
`EXTERNAL_ACCEPT_WITH_REPAIRS__REPAIR_PENDING`.
