# G225 preregistration — shared-event normal-screen carry

Date: 2026-08-22

Question type: `METRIC_LED`.

## Frozen alternatives

- `A_ENDPOINT_ONLY_EXACT_SCREEN_COCYCLE`
- `B_LOCAL_DIRECT_ISOMETRY_WITH_NONTRIVIAL_COMPOSITION_HOLONOMY`
- `C_SCREEN_SPACES_ONLY_NO_CANONICAL_DIRECT_MAP`
- `D_SCREEN_NOT_METRIC_DERIVED`

The result will be selected by the exact tests below. No alternative will be added after outcome
inspection.

## Frozen candidate construction

For normalized sight directions `n,m` in the observer rest space, set

```text
c = <n,m>
A = m n^T - n m^T
R(m<-n) = I + A + A^2/(1+c)
```

only on the non-antipodal stratum `c != -1`. The screen candidate is the restriction of `R` from
`n_perp` to `m_perp`.

No alternative angle, fitted coefficient, screen basis, spatial orientation, or post-readout
rotation may be inserted.

## Required exact checks

1. normalized null directions give unit rest-space sight vectors;
2. each sight vector gives the positive G188/G222 screen plane;
3. `R n=m`;
4. `R^T R=I` and `det R=1`;
5. `R` fixes the common perpendicular line pointwise;
6. the restricted map is a screen isometry;
7. identity and inverse hold;
8. passive orthogonal covariance holds;
9. the formula remains regular for orthogonal directions;
10. the antipodal stratum has no unique metric-natural least-turning map;
11. three-direction composition is tested against the direct map;
12. coplanar/great-circle controls and a genuinely noncoplanar witness are both included;
13. the composition defect acts orthogonally on the starting screen;
14. G224 scalar line carry remains separate and exactly multiplicative;
15. no pointwise screen map is called the G188 finite Jacobi propagator.

## Certification contract

- Production: exact symbolic/rational algebra with a declared check count.
- Independent replay: standard-library exact `Fraction` arithmetic on at least 20,000 seeded
  rational unit-direction triples, with independent matrix routines and at least one fixed
  nontrivial-holonomy witness.
- Hostile catches: wrong Rodrigues sign, omitted quadratic term, false cocycle, false antipodal
  uniqueness, screen scalarization, and independent-direct-relation promotion must all fail.
- All nine frozen source hashes must match.
- Aggregate package replay must be no-write.

## Falsification

The local-map claim fails if the frozen candidate is not orthogonal, does not map `n` to `m`, fails
passive covariance, or fails to map screens isometrically. The holonomy claim fails if every regular
noncoplanar triple composes exactly or if the registered nontrivial witness has identity defect. A
global endpoint-only cocycle claim is forbidden if the antipodal or isotropy obstruction survives.

## Maximum conclusion

At most G225 may classify pointwise screen spaces, a metric-natural non-antipodal direct
identification, its finite vertex-composition defect, and degenerate strata. It cannot select the
null protocol, populate relations, replace G188 path/Jacobi transport, select a metric history, or
derive `X_max`, observations, action, source, matter, bootstrap, mass, or signalling.
