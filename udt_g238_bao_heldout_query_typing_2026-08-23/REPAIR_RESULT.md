# G238 registered repair result

Date: 2026-08-23

Status: `R1_R2_EXTERNALLY_ACCEPTED__SCIENTIFIC_LANDING_RETAINED`

## R1 — actual frozen-knot counterfamily

Implemented exactly as preregistered:

- frozen JSON decimal spellings are parsed through `Decimal` and converted to exact `Fraction`
  values;
- the actual knots are affinely normalized without assuming uniform spacing;
- the coefficient construction vanishes at all 12 actual normalized roots;
- the registered evaluation point is the exact midpoint of the first two actual roots;
- `q`, `q'`, and `q''` are nonzero there;
- the independent verifier reconstructs the result by direct products and logarithmic derivatives;
- the package validator compares the saved root list and midpoint to a fresh calculation from the
  frozen state;
- a ninth hostile mutation replaces one actual root with `1/10` and is caught.

Internal result: `PASS`.

## R2 — self-contained sealed replay

`COMMANDS.md` now separates repository production from sealed external replay. The sealed route:

1. copies the read-only intake to a fresh disposable directory;
2. makes only that copy writable;
3. runs compilation, derivation, independent verification, package verification, and catches from
   the intake root;
4. does not invoke the repository-wide scientific-premise verifier, which is not part of the seal.

Internal and external result: a newly built read-only intake was copied to a writable disposable
directory and the documented sealed command sequence passed end to end.

## Scientific landing

Unchanged. BOSS outcomes remain closed. No interpolation, profile, feature, P1, `X_max`,
cosmological-distance conversion, source model, or branch population was added.

Fresh external repair-only verdict:
`G238_REPAIRS_ACCEPTED__SCIENTIFIC_LANDING_RETAINED`. No repair remains within R1/R2.
