# R17 path-labelled connection decomposition audit

Date: 2026-08-10

## Verified result

```text
COMPLETE_METRIC_PROJECTED_H_CONNECTION_AND_PATH_FUNCTOR_DERIVED_ON_SUPPLIED_REGULAR_STATIONARY_R17__FULL_CURVATURE_GENERALLY_NONZERO__PATH_SELECTION_AND_PHYSICAL_ARROW_OPEN
```

On the supplied regular stationary R17/W01 C01--C06 family, projection of the complete
Levi--Civita connection onto the rank-two normal bundle defines one smooth metric connection in
all four directions. For every supplied piecewise-smooth path it produces exact identity,
composition, and reversal transport. The metric therefore owns a complete path-labelled
isometric carry layer; it does not choose the path or supply the physical non-isometric observer
map.

## What the released directions add

All six curvature planes are nontrivially classified. The prior `lambda=-1` flatness is strictly
leafwise: it also removes the other clock-legged components, but ruler--screen and screen--screen
curvature remain generically. `lambda=0` instead makes the normal metric Hopf-basic and the two
horizontal connection coefficients zero in the global left-invariant representative, without
making the complete connection base-basic. `lambda=1` removes a third, different first-gradient
piece from the ruler--screen curvature. No lambda is selected and none is completely flat on the
generic compatible stationary jet space.

## Global result

The inherited `R x S3 -> S2` pair-leaf fibration has a metric-owned Hopf Ehresmann connection.
Given a base path and starting phase, it uniquely lifts the path; it does not select either input.
The complete normal connection is globally compatible across local screen/Hopf charts, while open
transport remains endpoint-gauge covariant and closed-loop conjugacy/trace is representative-free.

No supplied lambda makes the complete curvature horizontal with respect to both vertical pair
directions for arbitrary stationary jets. Thus the path-labelled total-space connection does not
collapse generically into one endpoint-only base rule.

## Evidence

- preregistration commit: `6293130b8b2a2256aff85cb5d376e42915b7c209`;
- 14/14 frozen source identities;
- 10/10 production structure checks;
- 300/300 independent exact Fraction/second-jet checks over six lambdas and both MC signs;
- 7/7 exact path-functor and `O(2)` checks;
- 18/18 exercised mutation catches;
- repository preservation gates recorded separately.

Fresh manifest-confined external `gpt-5.4` review independently reconstructed the complete
connection and all six curvature components and returned `VERIFIED_AS_STATED` with no objection.
The result is therefore `VERIFIED-WITH-CAVEATS` within its exact bounded arena, not canon or an
unconditional UDT theorem.

## Four banking gates

1. Preregistered: **yes**.
2. Full space or bounded scope: **bounded and explicit**—all supplied regular stationary C01--C06
   strata and arbitrary compatible stationary jets; time-live, null, degenerate, and other branch
   families excluded.
3. Independently verified: **yes**—300 exact local independent checks plus a fresh external
   reconstruction returned `VERIFIED_AS_STATED`.
4. Every forced premise audited: **yes for this bounded geometric claim**; physical path,
   non-isometric magnitude, observer arrow, and downstream physics remain open or excluded.
