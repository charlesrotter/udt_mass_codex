# G75 audit report — center-regular axial profile family

Date: 2026-08-11

## Landing

`CENTER_REGULAR_FAMILY_HAS_MULTIPLE_EXACT_SHAPE_STRATA`

Status: `INTERNALLY_REPLAYED_BOUNDED_LEAD_PENDING_FRESH_ADVERSARIAL_REVIEW`.

## What was learned

G74's topology atlas could not globally adjudicate twelve tapered/sign-changing controls because
their supplied metrics were not `C2` at the center. G75 does not patch those files. It constructs a
new, preregistered, role-neutral family in which axial mixing has the center-smooth form
`h=x^2 q(x^2)`.

The frozen family contains exactly 49 primitive quadratic shape rays, four normalized amplitudes,
three positive lapse controls, and three zero-mixing controls: 591 metric profiles total. Every
profile is Cartesian `C-infinity` at the center and Lorentz-regular on the full symbolic cell.

The family is not featureless. It contains 28 persistent-sign shapes, nine interior sign changes,
six center-off shapes, five endpoint tapers, and one shape vanishing at both boundaries. Eight exact
root/boundary strata survive. This gives the next sky calculation an outcome-independent vocabulary
of globally admissible controls instead of repairing or hand-selecting the blocked G74 rows.

## Evidence gates

1. Preregistered: **yes**, commit `e88d7511` before scripts or outputs.
2. Full space: **yes only within the frozen 49-ray quadratic definition**; no claim about all smooth
   profiles or the generic complete coframe.
3. Independently verified: **partially**. A separate exact root-isolation implementation replays all
   rows, but it was produced in the same active context; a fresh blind reviewer has not yet run.
4. Premises audited: **yes for the bounded family**, in `PREMISE_LEDGER.tsv` and
   `OWNERSHIP_LEDGER.tsv`.

Therefore the package is a `LEAD`, not a settled or externally verified verdict.

## Exact results

- source-manifest rows: 5
- primitive shapes: 49
- nonzero profiles: 588
- zero-mixing controls: 3
- total profiles: 591
- production exact checks: 10/10
- separate exact replay: 10/10
- package checks: 16/16
- hostile catches: 10/10
- protected stopped draft read: no

See `EXACT_DERIVATION.md`, `SHAPE_ATLAS.tsv`, `PROFILE_ATLAS.tsv`, and the three JSON verification
records for the load-bearing details.

## Scope boundary

No profile is ranked or selected. `R` remains symbolic. No source, sky ensemble, CMB endpoint,
`X_max`, SNe coefficient, bootstrap rule, action, matter law, spectrum, ODE/PDE, geodesic, Jacobi,
or GPU work enters G75. The original G74 blocked profiles remain blocked and unchanged.

## Next bounded gate

After a fresh adversarial review, preregister an outcome-independent whole-sky follow-up. It should
either cover the complete 591-member family if computationally reasonable or select a finite
representative set solely by the exact G75 stratum labels before seeing any sky response. That solve
may then map angular scale, transport, branching, and critical behavior across nonzero source
ensembles. It must not fit peaks or select a physical profile.
