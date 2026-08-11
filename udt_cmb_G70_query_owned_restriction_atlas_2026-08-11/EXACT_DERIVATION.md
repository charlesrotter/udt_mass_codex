# G70 exact derivation — query-owned restriction and channel atlas

## Status

- covariance transfer and positive-definite logarithmic coordinates: `DERIVED`;
- ranks on the frozen G69 control tile: `OBSERVED`;
- source shapes, source normalizations, carry access, and parameter restrictions: `CHOSE_CONTROL`;
- physical source/state, endpoint, profile, and observation-channel ownership: `OPEN`;
- primary landing: `IDENTIFIABILITY_NUMERICALLY_UNRESOLVED`.

The strict primary landing records `15` preregistered cells whose smallest normalized singular value
lies between the frozen full-rank and deficient thresholds. It does not erase the robust sub-results
below.

## 1. Covariance coordinates

For every positive-definite local screen covariance `C`, its symmetric logarithm exists. In the
fixed screen basis of the supplied G68 control query, define

```text
A(C)  = 1/2 log det(C),
S1(C) = 1/2[(log C)_00-(log C)_11],
S2(C) = (log C)_01.
```

`A` is the common logarithmic area/amplitude coordinate; `(S1,S2)` is the traceless shape and
orientation pair. These are smooth analysis coordinates on the positive-definite cone. Production
eigendecomposition reconstructs every covariance after exponentiation within
`3.8659e-16` relative. An independent SciPy `logm/expm` route agrees with every finite-difference
matrix within `8.2474e-15` relative and reconstructs covariances within `1.0807e-14`.

For the supplied screen map `D` and source covariance `C_src`,

```text
C_obs = D C_src D^T.
```

If `C_src=alpha C0`, then changing the unknown positive amplitude `alpha` adds `log(alpha) I` to
`log C_obs`. It changes `A` but not `(S1,S2)`. Hence unknown-amplitude models may use only the two
shape coordinates without silently treating source normalization as geometry.

## 2. Exact unrestricted-source result

For invertible `D` and arbitrary positive-definite observed covariance,

```text
C_src(D) = D^-1 C_obs D^-T
```

is positive definite and exactly returns the target. Therefore unrestricted `C_src` profiles all
covariance coordinates out. Appending the separately supplied geometric carry `psi` leaves only one
scalar channel and cannot identify three controls.

The independent route also checks 100 nonsymmetric deterministic transfer matrices: maximum
congruence reconstruction relative is `6.4254e-16`, and every constructed source stays positive
definite.

## 3. Frozen sensitivity construction

At every one of the `15` G69 sensitivity centers, each observation model is differentiated with the
same registered endpoint/lapse averages and amplitude secant. Every column is normalized before
rank classification. Rectangular singular spectra are padded with exact zeros to the parameter
dimension, so a one- or two-output model cannot be called full rank for three parameters.

The atlas contains `19` model variants and `285` rows:

```text
FULL_RANK_OBSERVED           46
RANK_DEFICIENT_OBSERVED     224
RANK_NUMERICALLY_UNRESOLVED  15
```

The independent implementation reproduces every classification and every one of the `285 x 3`
two-parameter restriction classifications.

## 4. Restriction ladder

### R00 — unrestricted source covariance

`0/15` full rank. Exact source profiling removes all covariance information about `D`.

### R01/R02 — fixed source shape, unknown amplitude

Every full three-parameter matrix is rank deficient. Two smooth covariance-shape coordinates cannot
identify three controls. The correlated control sometimes separates two-parameter restrictions,
but this is neither uniform across source shapes nor currently owned.

### R03 — known source covariance, covariance-only readout

No row is full rank: the identity and diagonal controls are deficient in all `30/30` cells; the
correlated control is deficient in `11/15` and numerically unresolved in `4/15`. Nevertheless all
three two-parameter restrictions are full rank in all `45/45` source/shape/endpoint rows. Thus a
known covariance would locally distinguish any two of `(x,a,epsilon)` if the third were independently
selected, but it does not robustly identify all three on this query.

### R04 — fixed source shape with unknown amplitude plus carry

The identity, isotropic duplicate, and diagonal controls remain deficient in all `45/45` rows. The
correlated control yields `1/15` full, `3/15` deficient, and `11/15` unresolved; its sole full cell
has condition number `6.14e5`. All two-parameter restrictions are full rank, but the full result is
not robust enough to claim that unknown source amplitude plus carry solves the three-control inverse
problem.

### R05 — known source covariance plus carry

All `45/45` cells are `FULL_RANK_OBSERVED`. The smallest normalized singular-value ratio is
`7.4439e-6`, above the frozen `1e-6` gate, and the largest condition number is `1.3434e5`. This is a
real bounded separation but remains poorly conditioned. It assumes both complete source covariance,
including normalization, and independent access to `psi`.

### R06 — two fixed-shape channels with independent unknown amplitudes

`0/45` full rank. Adding a second normalized shape channel does not recover the missing third
direction on this stationary/equatorial control query.

### R07 — unrestricted covariance plus carry

`0/15` full rank. The exact source freedom removes covariance information, leaving carry alone.

## 5. Parameter-restriction result

Fixing one parameter changes the question from three-column to two-column identifiability. In
particular:

- every R03 known-source row separates every remaining parameter pair (`45/45` for each pair);
- every R04 source-shape-plus-carry row separates every remaining pair (`60/60` for each pair);
- every R05 known-source-plus-carry row also separates every pair (`45/45`).

This proves only a conditional algebraic statement. The current query supplies endpoint and profile
as controls but does not select their physical values. No current source independently fixes `x`,
`a`, or `epsilon` for the physical CMB query.

Across the full atlas, pair classifications are:

```text
                 FULL  DEFICIENT  UNRESOLVED
(x,a)             153      90          42
(x,epsilon)       189      90           6
(a,epsilon)       187      90           8
```

## 6. Ownership result

The current metric/query sources own the control-query screen map `D` and the geometric carry `psi`
once that control query is supplied. They do not own:

- the physical CMB query or endpoint;
- a physical F01/F02 profile or coefficient;
- source isotropy, fixed shape, normalization, or covariance;
- scalar-TT access to `psi`;
- a physical polarization/independent orientation channel.

Metric symmetry does not imply source-state symmetry. Query input does not imply physical selection.
Therefore the algebraically successful R05 model is not presently a native UDT prediction.

The conditional P1 SNe result remains only a low-redshift observer-pair compatibility anchor. It
does not select the CMB endpoint, profile, or source. `X_max`, bootstrap, action, source law, and
local signalling remain inactive and open at this gate.

## 7. Maximum conclusion

The strongest robust tested local inverse model needs a known source covariance including amplitude
plus an independently read carry channel. A separately owned parameter value can lower that burden
to a two-parameter problem. Current UDT owns none of those missing restrictions for the physical CMB
query. Fifteen weaker-model cells remain numerically unresolved, so G70 cannot claim a unique
smallest sufficient restriction or begin a fit.

