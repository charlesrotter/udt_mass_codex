# Preregistration — twisted `S3` all-gate reciprocal reduction

Date: 2026-08-02  
Branch: `grok`  
Base: `aff38f85c55fc18961f55b57d12d8fadebc2669d`

## Whole question

In the already registered complete stationary twisted reciprocal `R x S3` configuration family,
does one explicit metric make its stationary timelike Killing line intrinsic and unique while
retaining nonzero Killing twist, the founded reciprocal ruler weight, global regularity, and a
strictly spacelike displayed slice? If so, do the unique clock line and twist-derived ruler line
assemble into one smooth equivariant rank-two reduction through the complete cell?

This is metric-led and configuration-level. It does not seek a physical branch, action, carrier,
source, density, mass, `X_max`, or observation.

## Frozen family

On `M=R x S3`, use global Maurer-Cartan forms and the already registered coframe

```text
tau=c_E dt+a sigma3,
theta0=exp(-phi) tau,
theta1=R exp(phi) sigma3,
theta2=R exp(lambda phi) sigma1,
theta3=R exp(lambda phi) sigma2,
g=-theta0^2+theta1^2+theta2^2+theta3^2.
```

No field equation is supplied. The primary analytic profile is registered before curvature is
evaluated. For unit-quaternion coordinates `q0^2+q1^2+q2^2+q3^2=1`, set

```text
u=exp(2 phi)=3+q0^2+2 q1^2+4 q2^2+8 q3^2.
```

The dimensionless existence calculation uses `c_E=R=1` as coordinate/unit normalization and
`a=1` as a free witness parameter. These values are not physical selections. The registered
transverse weights are `lambda=-1,0,+1`; none is preferred or inferred to be selected.

## Exact uniqueness route

Use the global scalar polynomial curvature invariants

```text
I1 = scalar curvature,
I2 = Ric_ab Ric^ab,
I3 = Ric^a_b Ric^b_c Ric^c_a.
```

In the preregistered stereographic chart, evaluate the exact spatial Jacobian
`d(I1,I2,I3)/d(x,y,z)` at only the registered points in `CANDIDATE_UNIVERSE.tsv`. No point,
profile, invariant, or `lambda` may be added after seeing an outcome.

If one determinant is exactly nonzero, analyticity makes the three invariants functionally
independent on an open dense subset. Any four-dimensional Killing field must annihilate all three,
so its spatial component vanishes there and hence everywhere. The full Killing equation then
forces its coefficient along `partial_t` to be constant. This is a full-Killing-field argument;
it does not assume stationarity of the candidate Killing field.

If every registered determinant vanishes, this route is inconclusive. A zero is not a no-go for
uniqueness and no replacement diagnostic may be introduced in this audit.

## Complete strata retained

- all three registered `lambda` witnesses;
- constant-depth symmetry control;
- twist-free control;
- repeated-profile-coefficient control;
- strict-slice and slice-null strata;
- discrete isometries, critical points, invariant-Jacobian zero sets, and possible global descent
  failures;
- all other smooth profiles and real `lambda` as untested open family members.

## Certification and maximum conclusion

A positive all-gate witness requires every gate in `GEOMETRIC_GATES.tsv`: exact global profile
range, strict slice, nonconstant timelike norm, one-dimensional full Killing algebra, nonzero
global twist, smooth independent clock/ruler lines, sign-independent projector/generator, and
equivariance. It may conclude only:

```text
ONE_EXPLICIT_COMPLETE_OFF_SHELL_TWISTED_S3_METRIC_HAS_A_METRIC_INTRINSIC_RECIPROCAL_RANK2_REDUCTION.
```

It may not conclude universal selection, an on-shell branch, physical observer semantics,
selection of the profile/`lambda`/twist, a response law, action, source, boundary law, bootstrap
closure, matter, mass, or canon.

## Evidence gates

Before banking: exact source freeze; deterministic exact derivation; independent implementation
or fresh zero-context adversarial review of the load-bearing uniqueness argument; exercised
catch-proofs; premise audit; frozen-manifest/current-path/frontier/link replay; and repository tests.

