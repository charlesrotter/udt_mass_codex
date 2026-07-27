# Twisted `S3` intrinsic screen and same-branch cocycle audit

Date: 2026-07-27

Preregistration: `de6b2f7`

Pre-result control correction: `dcadc04`

Grade: `VERIFIED_WITH_CAVEATS_BOUNDED_SAME_METRIC_JOIN_AND_CONNECTION_OBSTRUCTION`

## Result first

This was a productive place to look.  One old missing join closes, and the next missing join becomes
an exact geometric condition rather than a vague “underdetermined” seam.

For every complete twisted candidate C01–C06, the same metric now supplies:

- its unique intrinsic clock line;
- its twist-selected reciprocal ruler line;
- the unique orthogonal rank-two screen;
- the exact endpoint clock law `log Q=phi(q)-phi(p)` for intrinsic stationary observers; and
- the full transverse Jacobi propagator on the same supplied geodesic.

Thus a nontrivial reducible longitudinal/transverse path cocycle exists in one complete metric
without borrowing the clock from WR-L and the screen from a different branch.  The prior
branch-splicing objection is closed for bounded configuration existence.

## The more important new finding

The intrinsic screen is not automatically the path's optical screen.  Exact Cartan algebra gives

```text
nabla_(u+n)(u+n) = -p1(u+n)-2p2 E2-2p3 E3,
nabla_(u-n)(u-n) = +p1(u-n)-2p2 E2-2p3 E3,
```

where `dphi=p1 theta1+p2 theta2+p3 theta3`.  The ruler-aligned null directions are geodesic only
where the angular-screen gradient of `phi` vanishes.

On the twisted `S3`, requiring that alignment everywhere forces `dphi=0` because the screen
distribution is bracket generating.  Therefore any nontrivial stationary reciprocal depth forces
the intrinsic pair and the pathwise screen to mix somewhere through the metric connection.

This is a genuine clock–angular interaction emerging from the complete metric.  It is not a new
mechanism, action, force, matter source, or signal law.

## SNe ruling

The preserved WR-L/SNe readout is unchanged.  A raw local screen length `A exp(lambda phi)` cannot
equal the WR-L vertex distance `1-exp(-2phi)` near `phi=0`.  Local screen area and accumulated
optical/Jacobi area are different objects.

There is a visible but unpromoted clue: at `lambda=-2`, the local exponential is the complement
inside the WR-L areal law.  A vertex Jacobi problem naturally has a zero initial area, so this is a
reasonable prospectively testable crosswalk.  It does not select `lambda=-2`, validate the twisted
branch, or constitute a fit.

## What is closed and what is not

Closed in C01–C06:

```text
metric -> intrinsic clock line -> twist ruler line -> orthogonal screen,
metric + supplied geodesic + stationary endpoints -> log Q=Delta phi and symplectic M,
same metric -> S(log Q) direct_sum M.
```

Still open:

```text
physical path/event rule,
transported optical screen versus endpoint intrinsic screen reset,
irreducible or dynamical closure,
on-shell branch and lambda selection,
action/source/carrier/boundary/bootstrap/density/mass/Xmax/dynamics.
```

## Controls and exact census

- C01–C06: pass the local screen and branch clock join; all show nonzero north-event screen gradient.
- C07: nontrivial intrinsic clock but no twist-selected ruler; fails as expected.
- C08: constant depth and no parent intrinsic-pair certificate; fails as expected.
- exact production: SymPy 1.14.0 in an isolated pinned dependency path;
- independent replay: standard-library `Fraction`, no production import;
- four independent exact connection samples plus one contact sample;
- 64 exact depth-composition triangles;
- three exact symplectic controls;
- 24 preregistered false-promotion/corruption contracts exercised.

## Premise boundary

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

The derivation uses none of co-presence, instantaneous access, an action, or an on-shell equation.

## Four evidence gates

1. **Preregistered:** yes, `de6b2f7`; the two mistranscribed control `lambda` cells were corrected
   at `dcadc04` before outcome calculations.
2. **Full or bounded:** complete for the eight frozen candidates, exact local coframe/projector/
   connection identities, every stationary intrinsic endpoint pair on a supplied regular geodesic,
   and the global contact obstruction in this stationary twisted `S3` family.  Not complete for all
   metrics, paths, topologies, or on-shell solutions.
3. **Independently verified:** yes, exact SymPy and a no-import standard-library/Fraction replay.
   No fresh external-model semantic review was used, so the grade retains a caveat.
4. **Every premise audited:** yes; pair selection, signs, orientation, path, endpoint observers,
   optical screen, `lambda`, SNe comparison, solution status, and excluded physics are separate.

Maximum conclusion:

```text
COMPLETE_TWISTED_S3_INTRINSIC_CLOCK_RULER_SCREEN_SPLIT_AND_BRANCH_SPECIFIC_FOUNDED_CLOCK_JOIN_DERIVED;
NONTRIVIAL_SAME_METRIC_REDUCIBLE_PATH_COCYCLE_DERIVED_GIVEN_PATH;
NONTRIVIAL_DEPTH_FORCES_INTRINSIC_NULL_SCREEN_MIXING_SOMEWHERE_IN_THIS_CONTACT_BRANCH;
LOCAL_SCREEN_AREA_NOT_WRL_VERTEX_JACOBI_AREA;
NO_PHYSICAL_SELECTION.
```
