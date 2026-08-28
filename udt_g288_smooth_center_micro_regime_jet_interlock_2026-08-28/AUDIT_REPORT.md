# G288 audit report — smooth-center micro-regime jet interlock

Date: 2026-08-28
Grade: `EXTERNAL_REPAIRS_ACCEPTED__BOUNDED_LANDING_UNCHANGED`

## Primary landing

```text
PARTIAL_CENTER_INTERLOCK_ONLY
__QUADRATIC_NEGATIVE_PROFILE_GERM_IS_ZERO_TIDE_CONSTANT_CURVATURE
__ANGULAR_TIDE_BEGINS_AT_INDEPENDENT_QUARTIC_JET
__NO_PLANCK_SCALE_OR_HISTORY_SELECTED
```

## Result first

The micro-regime solution space has supplied something real, but not yet a unique microphysics.

A from-scratch reconstruction from the current primary metric shows that every analytic even smooth
center begins with

\[
f=1+c_2r^2+O(r^4).
\]

That quadratic germ is exactly the tangent of a constant-curvature, zero-angular-tide metric
family.  The same \(c_2\) controls the leading clock contrast, static acceleration, scalar
curvature, and geometric mass-aspect behavior.  Both angular screen channels cancel the entire
quadratic contribution; their first possible term is quartic and depends on the independently free
coefficient \(c_4\), with a fixed leading amplitude ratio \(4:1\).

For \(c_2>0\), \(\phi<0\) sufficiently near but away from the center.  The center itself remains
\(\phi=0\).  Taking \(r\) smaller therefore does not automatically make every channel louder: the
regular center becomes locally more symmetric, and angular tides are suppressed relative to the
reciprocal clock/curvature germ.

## Why this is new rather than an old-audit replay

- the production implementation begins from the four metric components and rebuilds the full
  connection, Riemann tensor, Ricci tensor, invariants, and nonradial null screen;
- it imports no old audit module or result;
- the independent implementation uses only standard-library exact `Fraction` arithmetic and
  separately rebuilds metric derivatives, inverse-metric derivatives, connection derivatives,
  curvature, and screen contractions;
- prior formulas are accepted only after both fresh routes reproduce them.

## Evidence

- outcome-blind preregistration committed and pushed at `0d57f458`;
- 22/22 from-scratch symbolic/tensor assertions pass in the separately dependency-declared SymPy route;
- the self-contained implementation-distinct replay passes 18,142 exact assertions over 1,000 general rational metric
  germs and 100 exact quadratic controls, covering both signs of \(c_2\);
- an independently noticed unused constant-ledger sign defect was failed closed and repaired before
  acceptance;
- 4/4 geometric mutations are rejected by fresh standard-library tensor recomputation;
- 9/9 saved-artifact and semantic regressions are caught, including Planck/\(X_{\max}\) insertion,
  physical-mass promotion, coordinate-speed promotion, profile/arrow sign aliasing, and trust in an
  old audit; this second harness is explicitly not a scientific recomputation;
- the current 272-row premise/startup verifier passes;
- the repository suite passes 192 tests with one expected `HABIT`-pin xfail;
- external repair-only review reran the self-contained replay and hostile recomputations and
  returned `REPAIRS_ACCEPTED` with no defects;
- the first full suite run exposed an overlong G287-era `INDEX.md` line; it was wrapped without a
  semantic change and the full suite then passed;
- no observation, fit, Planck cutoff, source, action, field equation, matter model, protected input,
  or physical history entered.

`verify_package.py` aggregates integrity, hashes, provenance, and registered replay results.  It is
not counted as an independent geometric derivation.

## Ownership ceiling

`DERIVED_CONDITIONAL` in the declared primary analytic-even center germ:

- the exact center coefficient maps;
- the quadratic zero-tide constant-curvature class;
- the independent quartic onset of angular/Weyl departure;
- normalized local radial null speed \(c_E\) versus coordinate slope \(c_Ef\).

`OPEN`:

- numerical \(c_2,c_4,\ldots\) values and any absolute micro scale;
- whether a physical negative-profile band lies near the Planck length;
- local rest mass, physical total mass, matter/source feedback, and mass emergence;
- the global negative trough, complete time-live/nonspherical history, branch population, and
  observational consequences.

## Maximum conclusion

The metric gives a strong local center universality class and a precise hierarchy of when channels
can first appear.  It does not select the Planck scale or a physical micro history.  Decreasing a
coordinate radius alone is therefore not yet a microphysical prediction.
