# UDT kinematic time-extendability constraint audit

Date: 2026-07-20

## Result first

Allowing the registered complete reciprocal metrics to vary along a path does **not** create a
kinematic selector for the remaining invariant `mu`.

All four registered complete lift classes possess exact smooth Lorentzian histories with nonzero
angular cross coupling and nonconstant `mu`. Metric compatibility and metric-plus-seal compatibility
both admit those histories. Positive CSN normalization can keep the full determinant fixed throughout.

One stronger condition does change the answer:

> If the reciprocal generator itself is required to be covariantly parallel together with the
> complete metric and seal, then `dot(mu)=0`.

That condition conserves whichever value was initially supplied; it does not select the value. Every
constant `mu>1` remains possible. Current UDT evidence does not yet select reciprocal-generator
parallelism as the physical transport law, so this is `DERIVED_CONDITIONAL`, not a closed UDT
evolution theorem.

The frozen audits are therefore not invalidated by this kinematic time test. They remain honest
snapshot classifications. They are not complete dynamical results because the action, physical
connection, boundary evolution, and physical meaning of the path parameter remain open.

## Lay picture

The previous audit inspected still photographs of the metric. This audit asked whether those
photographs can be joined into a smooth film without breaking UDT's reciprocal mirror.

They can. We built two different films through every registered angular completion. The metric and
mirror remain consistent in every frame, and the angular sector is genuinely coupled rather than
discarded.

There is also a stricter way to carry the geometry from frame to frame: demand that the reciprocal
operator itself never turn relative to the connection. Under that extra rule, the film may retain
one `mu`, but it cannot change it. The rule behaves like conservation of a label printed on the first
frame; it does not tell us which label nature prints.

UDT has not yet supplied the physical rule saying that this stricter transport is mandatory. Thus
time dependence has exposed a meaningful possible conservation law, not the missing value selector.

## Exact history census

Use

```text
H(k)=[[1,-k],[-k,1]],        mu=k^2,
F=[[0,1],[1,0]],             L=diag(-1,1,0,0).
```

For each of the four angular lifts, use its complete parity-compatible cross pattern with
`u=v=1/10`, angular metric `I2`, and either

```text
k_lower(s)=2+s/10,
k_upper(s)=3+s/10,          0<=s<=1.
```

This gives eight exact nonconstant histories. Their `mu` ranges are respectively

```text
4 -> 441/100,
9 -> 961/100.
```

Every full determinant remains negative, while the transverse Schur complement remains positive.
Therefore each full metric has signature `(-,+,+,+)` throughout the interval. Exact affine-factor
certificates, rather than endpoint sampling alone, establish the interval statement.

The pointwise identities and their derivatives vanish identically:

```text
R^2=I,
R^T G R=G,
R L R=-L,
R^T dot(G) R=dot(G).
```

## CSN and fixed-volume diagnostic

For any history with negative determinant, the positive common scale

```text
a(s)=(-det G)^(-1/4)
```

makes `det(aG)=-1`. Dividing its tangent by `a` gives

```text
dot(G)_volume = dot(G) - (1/4) tr(G^-1 dot(G)) G,
```

whose metric trace is exactly zero and whose seal parity is unchanged.

This is a legitimate CSN gauge diagnostic. It is not a physical representative-selection theorem:
CSN declares positive local common scale calibrational and does not demand this particular gauge.
The dimensionless pair invariant continues to change along each history.

## Three connection levels

With convention

```text
nabla_s G=dot(G)-Gamma^T G-G Gamma,
nabla_s R=dot(R)+Gamma R-R Gamma,
nabla_s L=dot(L)+Gamma L-L Gamma,
```

the levels are distinct.

### Metric compatibility

For every history,

```text
Gamma_G=(1/2)G^-1 dot(G)
```

is an exact compatible connection. The general solution also contains the six-dimensional
metric-skew freedom expected in four dimensions. Nothing fixes `mu` or `dot(mu)`.

### Metric plus seal compatibility

Because `dot(G)` has the same seal parity as `G`, `Gamma_G` commutes with the fixed seal. Exact
linear-system ranks at a rational load-bearing sample leave three connection freedoms for the
`+I/-I` lifts and two for the reflection/exchange lifts. Nonzero `dot(mu)` remains consistent.

### Add reciprocal-generator parallelism

Commutation with `L=diag(-1,1,0,0)` removes base-angular connection mixing and makes the two base
diagonal entries independent. Commutation with the swap seal then makes those entries equal,
`Gamma_base=alpha I2`.

Allow both a common scale rate `sigma` and a genuine invariant rate `dot(k)`:

```text
dot(H)=2 sigma H + dot(k) partial_k H.
```

The diagonal metric-compatibility equation gives `alpha=sigma`. The off-diagonal equation then gives

```text
dot(k)=0,
```

and hence `dot(mu)=0`. No equation contains an isolated value of `k`; conservation is not selection.

The exact full 16-component connection systems confirm this result in every lift: for `dot(k)=1`,
coefficient rank is 16 and augmented rank is 17; for the static sample the system is consistent.
A common CSN scaling remains possible through `Gamma=sigma I4` while `mu` stays constant.

## Moving-frame check

A nonconstant full-frame conjugation

```text
S(s)=I+sN,        N_0_2=1/7,        N^2=0
```

produces time-dependent components in `G`, `R`, and `L`. The required comparison connection is

```text
Gamma=-dot(S)S^-1 + S Gamma_base S^-1.
```

For constant `mu`, all component motion is removed covariantly: it is pure frame motion. For a
genuinely varying `mu`, the metric and seal remain parallel but the covariant derivative of `L` is
nonzero. A coordinate/coframe change therefore cannot disguise invariant deformation as gauge.

This reproduces the useful mathematical distinction in the earlier dynamic-frame work without
reinstating its withdrawn Xmax observer interpretation.

## Source and authority ruling

- `CSN` authorizes local positive conformal equivalence but no preferred representative or physical
  connection.
- Cartan/Levi-Civita connection data are derived after a representative is supplied; their
  identities are not evolution equations.
- The finite-cell seal supplies a static reciprocal ratio datum, not complete time-on boundary
  transport.
- Projective/conformal transport propagates supplied data and does not select initial physical data.
- Current bootstrap is an after-solution admissibility predicate with no varied functional,
  representative map, or local evolution operator.

Therefore no current source promotes full reciprocal-generator parallelism—or any other compatible
connection in the census—to the physical UDT movie rule.

## Supported preregistered outcomes

- `POINTWISE_TIME_PRESERVATION_ALLOWS_INEQUIVALENT_MU_HISTORIES`;
- `ALL_REGISTERED_FROZEN_LIFTS_HAVE_KINEMATIC_TIME_EXTENSIONS`;
- `METRIC_SEAL_COMPATIBILITY_ALLOWS_DOT_MU`;
- `FULL_RECIPROCAL_PARALLELISM_ONLY_CONSERVES_MU`;
- `FULL_RECIPROCAL_PARALLELISM_DOES_NOT_SELECT_MU_VALUE`;
- `PHYSICAL_TRANSPORT_LAW_REMAINS_OPEN`; and
- `KINEMATIC_TIME_EXTENDABILITY_REMAINS_UNDERDETERMINED`.

## Scientific consequence

The concern about frozen analysis was valid and worth testing, but it does not overturn the frozen
lift census. Kinematic time consistency supplies no missing numerical selector. The only new
conditional structure is a possible conservation law if UDT later derives full reciprocal
parallelism.

The next scientifically decisive object is now sharper: a native rule deciding **how reciprocal
structure is transported through the complete time-dependent metric**. It must follow from the
metric, finite-cell closure, or bootstrap—not from choosing Levi-Civita parallelism merely because
it is familiar.

A time-live soliton calculation is still premature as an unconditional UDT test. It would require a
selected geometry evolution and boundary law. It can later be run conditionally across an explicit
census of inequivalent completions.

No action, field equation, topology, boundary functional, physical time, carrier, source, mass,
scale, `X_max`, GPU result, or canon entry was selected.

## Four evidence gates

1. **Preregistered:** yes, commit `b8b17b6`, before new source inspection and algebra.
2. **Full space or bounded scope:** complete for the registered constant real isotropic lift classes,
   their nonzero parity-compatible constant cross patterns, the declared histories, and the three
   connection levels; not arbitrary global bundles or dynamics.
3. **Independent verification:** separate standard-library rational matrix/rank reconstruction,
   interval certificates, source/status replay, and exercised fail-closed mutations.
4. **Premise audit:** CSN, seal, connection, transport, bootstrap, boundary, action, and physical-time
   statuses are explicit.

Maximum conclusion:

`UDT_KINEMATIC_TIME_EXTENDABILITY_STATUS_CHARACTERIZED`.

