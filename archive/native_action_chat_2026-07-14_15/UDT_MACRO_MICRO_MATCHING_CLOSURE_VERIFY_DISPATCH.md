# DISPATCH — independent macro–micro conformal matching closure audit

## Mission

Independently verify or falsify the claimed source-free matching impossibility between a smooth
reciprocal core and the exact WR-L exterior in the conditional metric-only `C^2` branch. This is a
final closure audit, not a request to invent an interface action.

Do not update `LIVE.md` or `CANON.md`, start GPU numerics, or adopt a matter-transition postulate.

## Cold inputs

Read in this order:

1. `UDT_MACRO_MICRO_MATCHING_CLOSURE_MAP.md`
2. `UDT_MACRO_MICRO_MATCHING_CLOSURE_DERIVATION_RESULTS.md`
3. `verify_udt_macro_micro_matching_closure.py` only after constructing an independent derivation

Use

\[
I[A]=\int dr\,\frac{W[A]^2}{r^2},
\qquad
W=r^2A''-2rA'+2(A-1).
\]

## Required variational audit

1. Derive the complete first variation from scratch, including all endpoint signs.
2. Verify or falsify

   \[
   E[A]=2(W''+2W'/r),
   \]

   \[
   P_1=2W,
   \qquad
   P_0=-2W'-4W/r.
   \]

3. Derive internal junction conditions for continuous `A,A'` with no interface action.
4. Audit the distributional claim for jumps in `A` or `A'`; state exactly which regularity class
   makes `C^2` locally integrable.
5. Derive the moving-interface/transversality condition independently and verify its value on both
   zero-Weyl phases.

## Required solution audit

1. Solve the fourth-order radial Euler equation without importing the recorded solution.
2. Independently evaluate the full Bach tensor on that family and recover or falsify its algebraic
   constraint.
3. Impose a smooth normalized center and test matching to

   \[
   A_L=1-r/X
   \]

   on both a single sphere and an exterior open interval.
4. Explicitly test whether any source-free intermediate annulus evades uniqueness once all four
   junction data are imposed.
5. Search for a counterexample with finite `C^2` action before accepting the no-go.

## Interface nonuniqueness audit

As a diagnostic only, vary a generic

\[
B(A,A',R)
\]

and verify which momentum/transversality conditions it changes. Do not select coefficients. State
whether any already adopted UDT postulate uniquely fixes `B`.

## Evidence package

Return independent source, raw stdout/stderr, machine-readable JSON, exact commands/software
versions, tensor and jump conventions, and SHA-256 hashes.

## Verdict

Return exactly one primary verdict:

1. `SOURCE-FREE MATCH IMPOSSIBLE CONFIRMED`
2. `UNIQUE SOURCE-FREE MATCH FOUND`
3. `MATCH EXISTS WITH RADIUS MODULUS`
4. `AUDIT UNRESOLVED`

Then answer separately:

- Does zero-Weyl transversality select `R/X`?
- Is a new transition law required in the reciprocal spherical branch?
- What is the narrowest assumption behind any counterexample?

## Stop condition

Stop after the evidence package. Do not propose, fit, or bank the missing transition law, carrier,
radius, mass, or recycling mechanism.
