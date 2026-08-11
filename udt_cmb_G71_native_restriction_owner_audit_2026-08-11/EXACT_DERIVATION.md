# G71 exact derivation — native restriction ownership

## Status

Primary landing:

`GEOMETRIC_CARRY_OWNED__OBSERVABLE_AND_SELECTION_OWNERS_OPEN`

This is a source-bounded ownership theorem over the exact 21-file manifest. It is not a universal
no-go and not a CMB model.

## 1. Exact source freedom

For an invertible geometric screen map `D`, positive-definite source covariance `C_src`, and
observed covariance `C_obs`, the current query supplies the congruence

```text
C_obs = D C_src D^T.
```

For any positive-definite target `C_obs` and any invertible `D`, define

```text
C_src(D) = D^-1 C_obs D^-T.
```

Then

```text
D C_src(D) D^T = C_obs
```

exactly, and for every nonzero vector `v`,

```text
v^T C_src(D) v = (D^-T v)^T C_obs (D^-T v) > 0.
```

Thus the metric transports a supplied source state but does not, through this map alone, populate
or normalize it. The production verifier checks 12 exact rational cases; the independent route
checks 200 random positive-definite cases.

## 2. Amplitude is not shape

Let `C_src=alpha C0` with `alpha>0`. Since scalar multiplication commutes with every matrix,

```text
log(alpha B) = log(alpha) I + log(B)
```

for positive-definite `B`. Therefore the traceless logarithmic shape coordinates are unchanged,
while the trace/log-area coordinate shifts. Normalized shape data cannot own source normalization.
The independent verifier checks this on 200 random cases.

## 3. Evaluation is not selection

G68 derives a complete finite screen map and an azimuthal carry `psi` after a metric profile,
endpoint, path, screen, and observer query are supplied. The declared `r/R=1` endpoint is explicitly
a control surface, not `X_max` or last scattering. The banked global-completion, time-live, network,
and solved-branch results provide conditional geometries and compatibility identities, but no map

```text
complete global metric -> physical CMB endpoint or intervening profile.
```

The current `X_max` premise is an observer-pair asymptotic guard, not a surface selector. The SNe
P1 result is a conditional low-redshift compatibility anchor, not ownership of a centered CMB
profile.

## 4. Carry is geometric before it is observable

On a supplied path/query, the metric and screen transport derive geometric carry. This owns the
target `GEOMETRIC_CARRY_OWNER` only at status `DERIVED_CONDITIONAL_ON_QUERY`.

Scalar TT covariance does not directly read a pure screen orientation. An observable carry channel
would require a typed response map and, for polarization, an orientation-sensitive source/state.
Neither is present in the frozen source universe. Therefore geometric carry cannot be counted as an
independent observed datum merely because it is stored by the geometric calculation.

## 5. Exact ownership census

The six targets land as follows:

```text
SOURCE_SHAPE_OWNER          OPEN_NO_OWNER
SOURCE_NORMALIZATION_OWNER  OPEN_NO_OWNER
PHYSICAL_ENDPOINT_OWNER     OPEN_NO_OWNER
PHYSICAL_PROFILE_OWNER      OPEN_NO_OWNER
GEOMETRIC_CARRY_OWNER       DERIVED_CONDITIONAL_ON_QUERY
OBSERVABLE_CARRY_OWNER      OPEN_NO_OWNER
```

No target is `OWNED_NATIVE`. The one surviving owned object is a conditional geometric channel,
not one of the physical restrictions that made G70's inverse test full rank.

## 6. Maximum conclusion

Current banked geometry tells us how a supplied source and query are transported and proves that a
real carry channel exists on that supplied construction. It does not yet select the source shape or
normalization, the physical CMB endpoint/profile, or a physical observation map that reads carry.

This does not prove that a future native source law, global completion, or observation law cannot
own one of those objects. It proves only that none is already derived in the exact frozen source
universe.
