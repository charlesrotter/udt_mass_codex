# G249 certification-repair result

Date: 2026-08-24

## R1 — claim-directed independent replay: PASS

The replacement standard-library Fraction implementation has no SymPy, production import, or
production-output read. It directly verified:

- 10,000 non-diagonal homothety/Jacobi/area/shape cases;
- 10,000 same-`phi`, different-G201-jet cases;
- 10,000 lawful vertex-normalized noninjective-`phi` branch cases with unequal positive areas and
  symmetric derived tidal matrices;
- 512 constant-tidal IVPs through order 16, with the second-order Jacobi recurrence exactly equal
  to the upper-right block of the independently assembled first-order phase recurrence;
- 10,000 exact positive rational one-anchor scale recoveries;
- 248,310 exact assertions in total.

All six claim-class flags passed.

## R2 — formula-level hostile mutations: PASS

The replacement suite contains no phrase matching or unrelated-number tautologies. All 23
executable controls and mutations passed, including wrong Jacobi/tidal powers, wrong area/shape
normalizations, false clock/coarea invariance, same-`phi` collapse, noninjective-branch collapse,
an invalid IVP cubic coefficient, wrong anchor laws, caustic inversion, and signed-determinant
scalarization.

## R3 — aggregate verifier: PASS

The package verifier now requires all six claim flags, per-class case floors, 512 degree-16 IVP
comparisons, the formula-level mutation implementation identifier, exact mutation-ledger coverage,
and exact saved/live replay equality. Volume and landing strings are no longer sufficient.

## Scientific landing

Unchanged. The fresh reviewer found no dimensional, homothety, Jacobi, clock, branch, or scope
refutation. These repairs strengthen certification only; they do not extend the theorem or inspect
observations.

Status before repair-only follow-up:
`DERIVED_CONDITIONAL__REPAIRED_INDEPENDENTLY_VERIFIED_WITH_CAVEATS`.
