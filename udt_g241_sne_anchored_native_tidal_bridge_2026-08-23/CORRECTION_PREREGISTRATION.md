# G241 independent-replay correction preregistration

Date: 2026-08-23

The production evaluation completed and returned
`NO_REGISTERED_SMOOTH_ANCHOR_ADEQUATE__STOP_BEFORE_BOSS`. The independent route then stopped before
producing any candidate result because this installed `mpmath` version does not accept a matrix
right-hand side in `lu_solve`.

The only authorized repair is mechanical:

```text
replace lu_solve(C, B) and lu_solve(C, theta)
with an explicitly formed high-precision inverse C^-1 multiplied by B and theta.
```

No candidate degree, threshold, covariance entry, carrier formula, monotonicity gate, tidal sign,
source/query premise, or landing may change. The repaired independent implementation must still be
high-precision and must not read the production result. A different landing or a disagreement above
the registered comparison tolerances fails the package.

## R2 — failed-candidate pole-neighborhood comparison

After R1, the independent route reproduced the landing. Package comparison then stopped on the
degree-two dense-grid minimum: the two values are approximately `-3.766906274e8` and differ by
`7.22e-4` (`1.92e-12` relative). This candidate already fails the registered positive-slope gate;
its grid approaches a zero-slope tidal pole, so a fixed `1e-7` absolute comparison is ill-scaled.

The only R2 change authorized is to compare the dense tidal extrema with
`absolute_tolerance=1e-7` plus `relative_tolerance=5e-10`. Coefficients, chi-square, derivative
minimum, classifications, knot values, scale-invariance checks, candidate order, and landing keep
their original tolerances and formulas. R2 may not suppress or relabel the noninvertible candidates.

## R3 — scale-invariance residual normalization

After R2, package verification reached the scale-invariance guard. The float64 production residuals
are `1.79e-7` and `3.58e-7` only for the already rejected degree-two and degree-four candidates,
whose dense grids approach zero-slope poles with tidal magnitudes of order `1e9`. Their relative
residuals are below `4e-16`; the monotone degree-three candidate has absolute residual `1.78e-15`.

The only R3 change authorized is to grade the production scale-invariance check by

```text
residual <= 1e-12 * max(1, abs(dense_J_min), abs(dense_J_max)).
```

The independent high-precision residual remains required below `1e-50`. No formula, candidate,
classification, or landing may change.

## R4 — sealed replay layout and command-scope repair

The fresh external review retained the bounded scientific landing but found that the sealed intake
was not directly self-replaying. The production and independent scripts resolve the frozen G237
state as a sibling of the G241 package, while the intake builder placed manifested sources below a
separate `sources/` prefix. The reviewer could replay only after relocating the sealed sources in a
scope-authorized scratch copy. The command sheet also advertised the repository-wide premise
verifier and test suite even though neither was included in the sealed intake.

The only authorized R4 changes are mechanical:

1. build the sealed intake with every manifested source at its original repository-relative path,
   so the copied G241 scripts replay directly without moving files;
2. make the sealed command sheet distinguish commands runnable inside the intake from repository-
   only integration checks, and do not advertise absent repository checks as sealed replay steps;
3. add bounded guards proving the repaired intake contains the expected sibling source, contains no
   duplicate `sources/` tree, and directly passes the registered no-write production, independent,
   package, and catch-proof replays in an ephemeral copy.

R4 may not change a scientific formula, source hash, covariance entry, candidate degree, threshold,
fit, derivative classification, tidal value, premise status, outcome boundary, or the landing
`NO_REGISTERED_SMOOTH_ANCHOR_ADEQUATE__STOP_BEFORE_BOSS`. A changed scientific artifact or landing
fails the repair.

## R5 — post-acceptance registry banking replay

The accepted sealed intake correctly fixes the preregistration-era 223-row
`CURRENT_SCIENTIFIC_PREMISES.tsv` hash. Final banking necessarily appends the new G241 authority row,
so a repository-root replay can no longer require the live 224-row registry to have the historical
223-row hash.

The only authorized R5 change is for `verify_package.py` to treat that one manifest row as an
append-only banking boundary: require the live registry to contain exactly one G241 row, remove
that exact row in memory, and require the reconstructed bytes to match the sealed historical hash.
Every other source retains direct byte-hash verification. Add a banking note and a hostile guard
for any non-G241 mutation. No sealed manifest, scientific formula, candidate value, threshold,
classification, status, outcome boundary, or landing may change.
