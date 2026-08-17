# G133 audit report — fixed-`K` two-density and overlap descent

Date: 2026-08-16

Status:

`FRESH_ADVERSARIAL_FOLLOWUP_PASS__FIXED_K_INTERNAL_DENSITY_ONLY__PAIR_DENSITY_DESCENT_CONDITIONAL__FULL_g_AREA_BILINEAR_DERIVED__PHYSICAL_VALUE_LAW_OPEN`

## Result

Fixed `K` supplies an internal invariant determinant density for the abstract reciprocal
clock/ruler representation. It does not by itself supply a query-independent spacetime two-form,
a physical common-scale field, or a solder into every observer plane.

For each supplied regular pair immersion, the complete pullback metric supplies

```text
nu_h=sqrt(-det h)|dy0 wedge dy1|.
```

This is an intrinsic positive density and descends exactly on genuine overlaps of one common pair
atlas. Its coordinate coefficient satisfies

```text
kappa_pair' = kappa_pair + (1/2)log|det J|,
```

so `kappa_pair` is a log-density coefficient. Differences are scalar readouts only after matched
endpoint density trivializations/calibrations are supplied.

Across different observer planes the full metric supplies the correct common object: the symmetric
area bilinear on bivectors

```text
A_g(u wedge v,w wedge z)=g(u,w)g(v,z)-g(u,z)g(v,w).
```

It is derived from full `g`, has conformal weight four (area norm weight two), and is not an
alternating two-form. An exact Minkowski counterexample proves that no one two-form reproduces the
metric areas of every clock/ruler plane.

## Ownership boundary

Writing the same numeric `K` in two channel charts defines one object only when their transition is
`K`-orthogonal. Reciprocal `D(delta)` transitions meet that condition and compose. General complete
pair transitions do not automatically meet it, and independently rebuilt middle calibrations
still require an explicit transition.

Thus the positive descent result is conditional on a supplied common pair atlas or `O(K)` local
system. It does not own the physical query/value network.

## Current evidence

- preregistered and pushed at commit `15386b62` before outcome evaluation;
- corrected exact SymPy route: 29/29 checks pass after one JSON-serialization repair and the two
  external-review evidence repairs;
- corrected independent standard-library `Fraction` route: 25/25 checks pass;
- exact non-diagonal overlaps, determinant weights, `K`-mismatch witnesses, three-observer
  composition, separately declared direct-overlap data, a rejected corrupt-overlap witness,
  separately constructed four-dimensional Gram areas, area-bilinear conformal weights, explicit
  endpoint density re-trivialization, and the no-two-form counterexample exercised;
- fresh external review: `PASS_WITH_REPAIRS`; both required repairs were implemented;
- fresh external repair-only follow-up: `FOLLOWUP_PASS`, with independent reruns at 29/29
  production and 25/25 independent.

## Maximum current conclusion

`DERIVED` in bounded regular scope: fixed-`K` internal determinant density, pair-volume-density
descent on supplied common atlases, `kappa_pair`'s log-density type, and the full-metric area
bilinear.

Still `OPEN`: physical soldering/ownership of the complete observer network, its numerical metric
values, global and singular completion, and all downstream physical or observational claims.
