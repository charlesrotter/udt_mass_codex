# G275 audit report

Date: 2026-08-26

Status: `VERIFIED_WITH_CAVEATS__PENDING_EXTERNAL_REVIEW`

## Result

Preregistered alternative B survives:

```text
W5_PROJECTIVE_POSITION_IS_HOMOTHETY_INVARIANT
__ONE_MATCHED_NONZERO_WEIGHT_ANCHOR_FIXES_ONE_DIMENSIONAL_SCALE
__DIMENSIONFUL_REPRESENTATIVE_RETAINS_FULL_FRAME_CARRY
__XMAX_EQUALS_SCALE_ONLY_AFTER_SEPARATELY_OWNED_POPULATED_BOUNDARY_COMPLETION
```

The complete normalized pair position adopted in W5 is unchanged by a constant positive metric
homothety. One absolute multiplier therefore remains. One independently calibrated, same-object
datum of known nonzero homothety weight fixes it uniquely; every further anchor must agree.

The resulting \(\mathbf x=\ell\boldsymbol\chi\) is only a conditional dimensionful representative.
It retains active screen components and the G274 full frame-carry requirement. It is not a
vector-only nonradial composition law and is not automatically proper, radar, optical, or areal
distance.

Most importantly, \(\ell\) is not automatically `X_max`. For a supplied populated relation domain,
the supremum is \(X_{\rm sup}=\ell q_{\mathcal R}\). Equality with \(\ell\) requires
\(q_{\mathcal R}=1\), meaning a separately owned physical population approaches the projective
boundary.

## Evidence

- preregistration committed and pushed at `c42da02d` before implementation;
- 26 exact symbolic checks, including a generic non-diagonal connection calculation;
- active nonradial screen witness and exact hidden-carry separator;
- independent standard-library `Fraction` implementation: 20,000 cases and 340,006 exact
  assertions, with no production import or production-output read;
- 20,000 active-screen cases, 20,000 carry separators, both positive and negative anchor weights,
  20,000 finite-domain controls, and 20,000 boundary-approach controls;
- eight hostile implementation/scope mutations caught;
- zero observational values, fits, histories, profiles, field equations, or `X_max` assumptions.

## Gates

1. preregistered: **PASS**;
2. full bounded space: **PASS** for constant positive homothety, matched nonzero-weight attachment,
   arbitrary regular full-frame relations, and supplied projective-domain classes;
3. independently verified: **PASS**;
4. premises audited: **PASS** within the frozen ten-source scope.

## What remains open

- which independent same-object anchor Nature supplies and its value/uncertainty;
- the complete physical history and relation/path population;
- whether the populated domain approaches the projective boundary;
- whether the attached representative corresponds to a particular operational distance;
- numerical `X_max`, global completion, source, transfer, matter, and dynamics.

This is an internal verified-with-caveats result pending fresh external adversarial review. It is not
canonization.
