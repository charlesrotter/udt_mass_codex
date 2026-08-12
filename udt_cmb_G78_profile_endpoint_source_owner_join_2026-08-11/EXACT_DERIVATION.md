# G78 exact derivation — profile, endpoint/scale, and source-owner join

Date: 2026-08-11

## 1. What is being joined

G77 supplies a verified evaluator for 591 stationary axial control geometries under one supplied
observer and comparison sphere. G78 asks whether any current result supplies the missing physical
owner of the profile, endpoint/global scale, or source state. It does not ask which control looks
most like the CMB.

The frozen source universe has twenty individually adjudicated records. Seven candidate routes are
typed in `OWNER_ROUTE_LEDGER.tsv`; none is silently enlarged after seeing the outcome.

## 2. Regularity and topology do not select inside this family

The exact G75 identity is

```text
591 = 49 primitive quadratic shapes * 4 amplitudes * 3 lapse controls + 3 zero controls.
```

G77 returns `590 STRONG_DIRECT_AGREEMENT`, one `REGISTERED_DIRECT_AGREEMENT`, and zero unresolved
rows. All 591 maps have all 2,562 sampled directions crossing, sampled degree one, and zero missing,
negative-face, negative-projected-map, or registered near-area defects.

Therefore the registered center/signature/finite-mesh relation gates characterize all 591 controls
as survivors. They select zero rows. This is not a continuum injectivity theorem and not a claim
that regularity can never select in a broader family.

## 3. Exact scale factorization

The G75 metric is

```text
ds^2 = -A(x)c_E^2 dt^2 + R^2 dx^2/A(x)
       + R^2 x^2(dtheta^2 + sin^2(theta)dpsi^2)
       + 2 R c_E h(x) sin^2(theta) dt dpsi.
```

Define the dimensionless time coordinate

```text
tau = c_E t/R.
```

Then exactly

```text
ds^2 = R^2[-A dtau^2 + dx^2/A
            + x^2(dtheta^2 + sin^2(theta)dpsi^2)
            + 2 h sin^2(theta) dtau dpsi]
     = R^2 dSigma^2.
```

Because `R` is constant, the Levi-Civita connection of `R^2 dSigma^2` in these dimensionless
coordinates equals that of `dSigma^2`. Hence the unparameterized null paths and their dimensionless
angular relation are independent of the numerical value of `R`. The same substitution uses `c_E`
to define the clock/ruler-compatible time coordinate, after which `c_E` is absent from the
dimensionless angular map.

This does **not** mean UDT is scale-free. `c_E` remains the observed clock/ruler calibration and
`R` remains the conversion from dimensionless `x` to physical length. The result is narrower:

```text
the G75--G77 dimensionless angular relation cannot determine its own absolute R.
```

An external distance/clock observable or a same-geometry cross-query relation is required.

## 4. The control endpoint is not `X_max`

G76/G77 choose the first outward crossing of `x=1`. The choice is part of the observer query. The
current `X_max` frame instead requires a nonnegative observer-pair separation to approach a shared
asymptote only as reciprocal depth diverges. It explicitly supplies no separation law, numerical
value, chart endpoint, or identification with `R`.

Thus `x=1`, `R`, and `X_max` have different types. No frozen source contains a map identifying
them. The asymptotic requirement remains necessary for a future physical realization but is not an
endpoint or scale owner here.

## 5. The SNe anchor has the wrong current input type to select G75

The frozen SNe P1 relation is

```text
r(phi_pair)=R_w[1-exp(-2 phi_pair/n)].
```

It is an observed conditional low-redshift observer-pair relation. G75 instead supplies a lapse
control `A(x)=1+a x^2`, an axial mixing profile `h=x^2 q(x^2)`, and a chosen comparison sphere.
No frozen source maps `(R_w,n,phi_pair)` into `(R,a,q,x_endpoint)` by deriving both from one complete
geometry and query.

P1 may later test a complete geometry for compatibility. Copying it into `A` or `q` would be a
role error. It therefore remains `COMPATIBILITY_ANCHOR_ONLY`.

## 6. Geometry transports source state but does not populate it

For any invertible screen response `D` and positive-definite observed covariance `C_obs`, define

```text
C_src(D)=D^-1 C_obs D^-T.
```

Then exactly

```text
D C_src(D) D^T = C_obs,
```

and `C_src(D)` remains positive definite. G78 verifies the symbolic identity and an independent
256-case nonsymmetric numerical reconstruction. Therefore an unrestricted source can absorb an
invertible geometric response. The response evaluates and transports a source; it does not derive
the source's shape, normalization, or statistics.

G70's known-source-plus-carry model can distinguish controls conditionally. But the known source
and observable carry channel are themselves unowned premises. Conditional identifiability is not
physical ownership.

This exact source statement applies on the invertible-response stratum. G77 supplies strong finite-
mesh evidence that all 591 sampled relation maps are regular and orientation preserving, but G78
does not promote that evidence to a continuum diffeomorphism theorem.

## 7. Landing and smallest remaining joint

The seven-route result is:

```text
4 OPEN_NO_OWNER
1 COMPATIBILITY_ANCHOR_ONLY
1 NECESSARY_REQUIREMENT_ONLY
1 CONDITIONAL_IDENTIFIABILITY_ONLY
0 OWNED_NATIVE
```

Primary bounded landing:

```text
NO_PHYSICAL_PROFILE_ENDPOINT_SCALE_OR_SOURCE_OWNER_IN_FROZEN_G78_UNIVERSE
```

The smallest constructive next joint is not another ray solver or an attractive-profile ranking.
It is one same-complete-geometry realization linking an actual observer query to both a dimensional
distance/clock observable and the angular relation. The most accessible existing compatibility
test is SNe, but its full query must be derived or explicitly supplied before P1 can constrain the
G75 family. A native source-state law is the separate, deeper route. Bootstrap remains a hypothesis
and did not enter G78.

