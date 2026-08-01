# F01 lambda/mu Schur audit

Date: 2026-08-01  
Preregistration commit: `af71724`  
Mode: CPU-only, exact response plus validated interval enclosures

## Result first

**`SCHUR_SIGN_MIXED_ACROSS_OWNED_BRANCHES`**, verified in the exact bounded conditional scope.

There is exactly one registered massive crease root in `s in (1,3)`, bracketed by
`1.68102 < s* < 1.68103`. On both owned `p` right-trace variants:

- R05/free angular traces has strictly positive lambda/mu Schur scalar, so its exact reduced-field
  index one stays joint index one.
- R06/supplied odd zero angular traces has an explicit strictly negative joint witness. Its exact
  positive reduced-field core therefore becomes joint index one when `mu` is restored.

The earlier apparent R06 positive survivor was only positive on a field slice with `mu` held fixed.
All four full local conditional domains have one negative direction, though it lives in different
sectors.

## Exact evidence

The root count is analytic: after `z=s(x+1)`, the integrand is
`log(1-z+z^2/2)`, negative on `(0,2)` and positive on `(2,infinity)`. The primitive is strictly
increasing beyond two, negative at two, and positive by six.

For R05, angular elimination leaves

```text
L0[p]=-(w p')'-s^2 p/w.
```

The formerly “dilogarithmic” response has the elementary particular solution `1-log(w)` and
homogeneous basis `{w'/w, 1-1/w}`. Exact endpoint matching gives both the Dirichlet and inhomogeneous
free-right responses. The resulting representative-mu Schur enclosures are:

| domain | enclosure |
|---|---:|
| R05 Dirichlet | `[2.081935542306277, 2.094564007954956]` |
| R05 free right | `[2.005554573547819, 2.016641905660295]` |

For R06, explicit exact-decimal-rational polynomial witnesses give:

| domain | full joint-Q enclosure |
|---|---:|
| R06 Dirichlet | `[-0.667353248254471, -0.642796186731147]` |
| R06 free right | `[-1.414417787892328, -1.390607716360248]` |

The primary arithmetic used nested 80/100-digit outward interval runs. All refined intervals lie
inside the coarse intervals. `diagnostic_spectral.py` independently assembles the unreduced full
Hessian over six polynomial sizes and is retained only as corroboration.

## Cold adversarial review and repair

A fresh implementation rehashed all 12 frozen sources, rederived the raw Hessian and scale factor,
checked both response boundary problems, independently enclosed all four signs at 90/100 digits,
checked exact R06 trace admissibility, and exercised 14 mutations. It found no mathematical
contradiction.

Its first verdict was `PASS-WITH-CAVEATS` because the primary scripts initially missed the
preregistered 80-digit floor. The historical review is preserved. After the 80/100-digit repair,
the same verifier returns `PASS`, all four independent enclosures overlap the primary ones, and no
required repair remains. See `INDEPENDENT_REVIEW.md`, `PRECISION_REPAIR.md`, and
`INDEPENDENT_RESULT.json`.

## Scientific interpretation

This is a clean premise-scoped negative for F01 under the conditional P4 response,
`ell=1`, the named trace forks, and germ-Hessian-flat wall witnesses. It removes F01's apparent
local joint-stable survivor from the presently tested scope.

It does not refute the stability hypothesis in `PONDER_MATH_ELEGANCE_2026-07-31.md`. That hypothesis
concerns a larger native global-local closure. This calculation instead demonstrates why a field
slice cannot stand in for the complete allowed variation space.

The independently free second wall germ remains unowned at the banked jet<=2 layer; existing N4
content is typed but supplies no equation. A full chain, physical boundary, native response/action,
time persistence, carrier, source, matter, mass, and bootstrap selection all remain open.

## Four evidence gates

1. **Preregistered:** yes, commit `af71724`; source base `53bdc2c`.
2. **Full or bounded:** complete over every root and all four exact owned local domains; explicitly
   not a full-chain or native/global theorem.
3. **Independent:** yes after repair; fresh algebra, source/domain audit, independent interval
   implementation, 14/14 catches, final `PASS`.
4. **Premises:** all 16 rows audited; conditional/selected/open objects travel in
   `PREMISE_LEDGER.tsv`.

Repository preservation gates pass: six frozen manifests/133 package paths, 18 current-premise
guards plus 9 startup controls and 754 dispositions, and 70 tests passed with 1 expected failure.
