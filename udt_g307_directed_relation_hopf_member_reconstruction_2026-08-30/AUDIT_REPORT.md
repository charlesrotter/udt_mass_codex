# G307 audit report — conditional Hopf-member reconstruction from a complete directed germ

Date: 2026-08-30
Status: `INTERNALLY_DERIVED_AND_INDEPENDENTLY_VERIFIED_WITH_CAVEATS`

## Primary landing

```text
SUPPLIED_DIRECTED_GERM_SELECTS_ONE_MEMBER_PER_CHIRAL_FAMILY
__SIGNED_TRANSVERSE_SCREEN_GERM_SELECTS_ONE_MEMBER_CONDITIONALLY
__ACTIVE_PREMISES_POPULATE_NEITHER__PHYSICAL_MEMBER_REMAINS_OPEN
```

## What was learned

G306's metric-only ambiguity is not an unrestricted field once an actual directed relation is
supplied. A point and ordered tangent select exactly one Hopf member in each of the two chiral
families. Those two members generate the same complete great-circle route and agree on its tangent
plane, so no amount of one-dimensional route following distinguishes them.

Their difference appears in the transverse screen. Relative to one supplied screen orientation,
one member rotates the screen by `+90` degrees and the other by `-90` degrees. One signed
transverse-screen first derivative therefore reduces the two candidates to one.

This is a substantial narrowing of G306's continuous family ambiguity:

```text
metric alone:          two continuous S2 families
point + direction:     two members
signed transverse jet: one member
```

## What was not learned

Active premises still do not select which physical observer/event/route queries Nature populates,
nor do they supply the transverse sign for such a population. Conditional reconstruction must not
be renamed physical selection. The result introduces no action, source, mass law, scale, fit,
history, observation, or `X_max`, and it modifies neither the primary metric nor the reciprocal
kernel.

## Scope and evidence

The theorem is complete on the positive-radius round G305 completion, both G306 chiralities, all
regular directed point/tangent germs, all regular oriented transverse screens, and all positive
radii. Nonspherical, quotient, singular/cut/caustic, topology-changing, and dynamically populated
cases remain outside scope.

The landing was preregistered at pushed commit `1bdfe7d2`. Exact production supplied 1,806 rational
assertions. An unrelated outer-product implementation supplied 17,000 checks over 1,000 random
frames with maximum error `4.1389114358025836e-13`. All 14 hostile mutations were caught. The
current premise registry passed. Fresh external adversarial review is still required before the
bounded package can be called externally closed.
