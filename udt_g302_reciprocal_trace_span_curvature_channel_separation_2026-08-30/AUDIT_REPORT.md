# G302 audit report

## Landing

```text
RECIPROCAL_SHAPE_SPANS_NINE_AND_COMPLETE_SCALE_RESTORES_TEN
__NO_G301_CLASS_SELECTED__TRACEFREE_BRANCH_HAS_EXACT_CHANNEL_SEPARATION
```

Status: `EXTERNALLY_VERIFIED_REPAIRED_BOUNDED_CLASSIFICATION`.

## Decisive results

- Exact rational Lorentz-orbit span: reciprocal shape rank `9`.
- Exact rank after adding retained common metric scale: `10`.
- Independent implementation: standard-library `Fraction` rank plus a separately written full
  Christoffel/Riemann tensor calculation; `PASS`.
- Conditional trace-free primary solution:

  \[
  f=1+b/r-R_0r^2/12.
  \]

- Exact registered angular channels: `+3b/(2r)` and `-3b/(2r)`; `R0` cancels.
- Exact invariants: `R=R0`, `RicciSquared=R0^2/4`, `WeylSquared=12b^2/r^6`.
- Smooth areal center requires `b=0`.
- All eight positive-`f` sign and repeated-root strata recorded and independently exhaustively
  verified by dependency-free parameter-cell/Sturm certification.
- Eleven original hostile scientific mutations and six domain-certification mutations rejected.
- Current 285-row scientific premise registry passed.
- Repository purity suite passed: 197 tests, with one registered expected xfail.

## Scope audit

Gate A covers the complete four-dimensional local metric tangent over an algebraic all-plane control
family.  It does not establish physical plane population.  Gate B covers only the exact static,
diagonal, areal-spherical metric and does not extend to nonspherical or time-live solutions.

The G301 trace-free residual remains `FREE_AND_EXPLORED_CONDITIONAL_CLASS`.  No field equation,
source, action, mass interpretation, observational anchor, scale value, history, or boundary was
adopted.  Metric and reciprocal kernel are unchanged.

## Certification boundary

Preregistration was committed at `887a91ad` before production files existed. Fresh external review
returned `VERIFIED-WITH-CAVEATS` without scientific refutation. Its representative-domain-coverage
caveat was repaired internally under commit-prior repair preregistration. The sealed repair-only
external follow-up returned `ACCEPT_REPAIRS`: all eight exact domain rows and all six hostile
domain mutations replayed successfully, with no remaining defect and no scientific-claim change.
