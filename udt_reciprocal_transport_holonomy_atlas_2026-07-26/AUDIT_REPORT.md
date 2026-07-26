# Reciprocal transport and holonomy atlas

Date: 2026-07-26

Preregistration commit: `0e385cb`

Grade: `VERIFIED_WITH_CAVEATS`

## Result first

The complete metric does supply the previously missing frame join **along
one supplied path**: Levi-Civita parallel transport carries the reciprocal
lift by conjugation, composes exactly, reverses exactly, and works for every
`lambda`.

It does not supply a unique path-independent or global join by itself.
Different paths differ by metric holonomy. An ordinary global reciprocal
lift exists only when that holonomy commutes with the lift.

The exact classification reveals three distinguished values with three
different geometric meanings:

| Global structure supplied | Conditional value |
|---|---:|
| parallel timelike line with full spatial `SO(3)` holonomy | `lambda=+1` |
| parallel spacelike ruler line with full `SO+(1,2)` complement holonomy | `lambda=-1` |
| complete lift is odd under reciprocal `Z2` inversion | `lambda=0` |

Trivial or screen-only `SO(2)` holonomy leaves every `lambda` possible.
Full Lorentz holonomy, base-boost holonomy, and the null stabilizer preserve
no regular member of the founded semisimple lift family.

Current UDT premises select none of those holonomy reductions or global
bundle ontologies. Therefore:

```text
NO_UNCONDITIONAL_LAMBDA_SELECTION.
```

## What has actually closed

The local “missing connection” is no longer vague. Once a complete metric is
given, no additional transport mechanism is needed along a curve; the metric
already provides Levi-Civita transport.

The open seam has moved outward. To obtain one global observer-pair clock and
coframe law, UDT must select:

1. a complete metric branch and its actual restricted holonomy;
2. the relevant paths and global/discrete monodromy; and
3. whether the reciprocal object is an ordinary endomorphism or an odd
   sign-twisted line under reciprocal inversion.

Those are global structural data, not another local scalar coefficient.

## Ordinary holonomy classification

For

```text
X_lambda=diag(-1,+1,lambda,lambda),
```

ordinary path independence is equivalent to

```text
H X_lambda H^-1=X_lambda
```

for every holonomy element `H`.

- `lambda=+1` merges the ruler and screen into one three-dimensional spatial
  eigenspace. Spatial rotations are allowed; boosts out of the observer line
  are not.
- `lambda=-1` merges the clock and screen into a Lorentzian
  three-dimensional eigenspace. `SO+(1,2)` is allowed while the spacelike
  ruler line remains fixed.
- generic `lambda`, including zero, preserves the ordered clock line, ruler
  line, and screen separately; only screen rotation remains.
- no `lambda` permits a boost mixing the founded clock and ruler eigenlines.

This is a classification of conditional reductions. It is not evidence that
the universe has a parallel timelike or spacelike line.

## Twisted reciprocal descent

The previously derived reciprocal normalizer contains an inverting
transition `F`. Requiring the **complete** lift, not only its clock/ruler
block, to be odd gives

```text
F X_lambda F^-1=-X_lambda
```

only at `lambda=0`. The finite identity

```text
F D_lambda(phi) F^-1=D_lambda(-phi)
```

gives the same unique conditional value for nonzero `phi`.

This is a real new reduction of the extension family. It remains
`UNIQUE_CONDITIONAL_TWISTED`, because the reciprocal swap is not a
Levi-Civita holonomy of the diagonal Lorentz readout. Prior work permits a
conditional compatible mixed readout, but does not select that solder or the
odd complete-lift ontology.

## Twelve-family global cross

Every registered finite-cell row was classified. The important distinctions
are:

- simple connectivity removes topological monodromy but not curvature
  holonomy from contractible loops;
- solid-torus, `S2 x S1`, lens, and torus-bundle families add nontrivial
  global monodromy gates;
- mirror and reciprocal-toric families contain an exact conditional route to
  the `lambda=0` odd lift, but do not select it or its physical readout;
- nonorientable, stratified, and singular families require their own lift,
  matching, or regular-complement data; and
- none of the twelve rows contains a complete on-shell metric, `phi`,
  physical coframe solder, and actual holonomy.

No family was ranked or selected.

## Kato control

A Kato/projected connection can preserve any already chosen smooth spectral
reduction. This remains a useful mathematical transport control. Because it
is constructed from the chosen projector, it cannot decide which projector,
`lambda`, or connection is physically UDT.

## What remains open

- complete four-dimensional reciprocal-angular extension;
- selected complete metric branch and holonomy;
- ordinary versus twisted global reciprocal object;
- physical path or path-family selection and cut-locus handling;
- full metric/readout/seam solder;
- action, carrier, source, boundary functional, density response, bootstrap
  fixed point, mass, and dynamics.

`c_E` and `G_obs` retain observational calibration roles. Provisional `hbar`
was not activated and none of the scalar anchors selects holonomy.

## Evidence gates

1. **Preregistered:** yes, commit `0e385cb` before outcome algebra.
2. **Full or bounded:** complete for twelve routes, fifteen registered
   holonomy/transition strata, the entire one-modulus lift family, and all
   twelve fixed finite-cell types; not arbitrary subgroups or solved metrics.
3. **Independent:** yes, a standard-library exact-rational implementation
   with no SymPy or production import checks path transport, all principal
   connected stabilizers, null obstruction, and finite reciprocal inversion.
4. **Premises audited:** yes. Path, metric branch, ordinary/twisted ontology,
   holonomy, monodromy, seam, singularity, scalar anchors, and excluded
   physics are separately stamped.

No fresh external-model review was authorized; that is the caveat.

Maximum conclusion:

```text
BOUNDED_RECIPROCAL_TRANSPORT_HOLONOMY_ATLAS_FOR_REGISTERED_STRATA;
PATHWISE_METRIC_TRANSPORT_DERIVED_GIVEN_INPUTS;
PLUS_ONE_MINUS_ONE_AND_ZERO_ARE_DISTINCT_CONDITIONAL_GLOBAL_REDUCTIONS;
COMPLETE_BRANCH_AND_GLOBAL_REDUCTION_REMAIN_OPEN.
```
