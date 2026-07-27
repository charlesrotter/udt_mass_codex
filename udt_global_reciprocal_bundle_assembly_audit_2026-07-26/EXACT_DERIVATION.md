# Exact global reciprocal-bundle assembly

## 1. Local family and overlap law

For a supplied unit timelike observer `u` and orthogonal unit spacelike ruler `n`,

```text
X_lambda(u,n) = -P_u + P_n + lambda(I-P_u-P_n).
```

Under a frame change `Lambda`, every projector transforms by conjugation, hence

```text
X_lambda(Lambda u,Lambda n)
  = Lambda X_lambda(u,n) Lambda^-1.
```

This is the chart-overlap law of an endomorphism-valued function on the ordered pair-frame bundle.
It holds for every real constant `lambda`. A global section `(u,n)` is not required for this bundle
object to exist.

Metric path transport and explicit vertical pair changes then give the already derived exact typed
path-groupoid composition. Noncentralizing holonomy changes the endpoint pair-frame value along a
different path; it does not make either arrow ill-defined.

## 2. Four exact `lambda` strata

In an ordered orthonormal basis `(u,n,s1,s2)`,

```text
X_lambda = diag(-1,+1,lambda,lambda).
```

The connected Lorentz-centralizer dimensions are:

| stratum | dimension | retained connected symmetry |
|---|---:|---|
| generic `lambda not in {-1,0,+1}` | 1 | screen `SO(2)` |
| `lambda=-1` | 3 | `SO+(1,2)` on the ruler complement |
| `lambda=0` | 1 | screen `SO(2)` |
| `lambda=+1` | 3 | spatial `SO(3)` |

The two degeneracy identities are

```text
X_+1 = I-2P_u,
X_-1 = 2P_n-I.
```

Thus `lambda=+1` forgets the ruler direction for fixed `u`, while `lambda=-1` forgets the observer
direction for fixed `n`. `lambda=0` is trace-free but has no enlarged stabilizer. None of these
identities selects a stratum.

## 3. Homogeneous complete controls

For the round and Berger spatial `S3` controls, use the global orthonormal coframe

```text
de1 = p e2 wedge e3,
de2 = p e3 wedge e1,
de3 = q e1 wedge e2,
```

with ultrastatic time `u` and conditional Hopf ruler `n=e3`. The torsion-free connection is

```text
omega12=(p-q/2)e3,
omega13=-(q/2)e2,
omega23=(q/2)e1.
```

Its sectional curvatures are

```text
K12 = p q - 3q^2/4,
K13 = q^2/4,
K23 = q^2/4.
```

Because `q>0`, the curvature contains nonzero `J13` and `J23`; their commutator supplies `J12`.
The spatial holonomy Lie algebra therefore spans all of `so(3)`, including at any positive
homogeneous squashing and at the round locus.

## 4. Parallelism selects one stratum only conditionally

The ultrastatic projectors `P_u` and `P_space` are parallel. Therefore

```text
nabla X_lambda = (1-lambda) nabla P_n.
```

On the homogeneous controls,

```text
nabla_e1 n = +(q/2)e2,
nabla_e2 n = -(q/2)e1,
```

so `nabla P_n` is nonzero. Exactly,

```text
nabla X_lambda=0  iff  lambda=1.
```

Equivalently, full spatial holonomy is contained in the stabilizer of `X_lambda` only at
`lambda=1`. Thus on both concrete complete `S3` controls:

- every `lambda` defines a valid path-labelled pair-frame comparison;
- only `lambda=1` transports to the same ordinary endpoint endomorphism along every path.

This is a conditional selector theorem. It becomes a physical selection only if UDT independently
requires a parallel, endpoint-only reciprocal endomorphism. The founded observer-pair postulates and
current path-groupoid result do not yet supply that requirement.

## 5. Metric naturality is different from parallelism

On round B19, the metric has a global parallel ultrastatic time line but round isotropy selects no
spatial ruler. Consequently only `X_1=I-2P_u` is metric-natural without extra ruler data.

On the squashed control, the simple Ricci eigenspace distinguishes an unoriented Hopf line. Since
`P_n` is orientation-insensitive, the metric can construct `X_lambda` for every supplied value of
`lambda`. Those fields are generally not parallel. The control is also off shell and does not
select the numerical value of `lambda`.

Thus “constructed naturally from the metric” and “preserved by parallel transport” are logically
independent properties.

## 6. Caps and cut loci

The global left-invariant coframe proves that the pair-frame bundle and chosen Hopf fields are smooth
on the concrete `S3` controls. Collapse of toric orbit coordinates at a cap is not degeneration of
the tangent metric or pair-frame bundle.

At an antipodal cut locus, several geodesic arrows can connect the same endpoints. The path groupoid
retains all of them. Generic `lambda` can give holonomy-related endpoint pair frames; `lambda=1`
collapses those spatial rotations on the two ultrastatic controls. The cut locus is therefore a
path-uniqueness issue, not a bundle-existence failure.

## 7. Remaining completion classes

The other eleven registered completion classes do not contain actual complete metrics. Their exact
status is consequently structural:

- regular boundary/cap/quotient classes admit a pair-frame bundle if a regular Lorentz metric and
  compatible join are supplied;
- mapping-torus, mirror, nonorientable, and lens-space single-field descent depends on the actual
  deck, monodromy, or lift action;
- the nonprimitive class is only a regular-stratum statement until orbifold/singular isotropy is
  resolved;
- projector-rank transitions obstruct a projector-derived pair, not an independently supplied typed
  pair;
- a nonintegrable distribution does not obstruct the pair-frame bundle because no orbit surface is
  required; and
- FC12 remains a parametric ansatz with open profiles and endpoint data.

No absent metric is promoted to a witness.

## 8. Causal type

The typed family assumes regular timelike `u` and spacelike `n`. It does not derive either from
`dphi`. A null, zero, or type-changing `dphi` obstructs a separately assumed normalized-gradient
lift, not the pair-frame family itself. Importing that obstruction here would change the ontology.

## 9. Signed depth and variation

Assembly supplies the endomorphism container but no scalar

```text
delta[g; gamma,(u,n), ...].
```

B19 and the squashed control have trivial ultrastatic clock ratios; neither supplies founded
normalization. No other complete representative exists. Physical signed depth therefore remains
open.

Tensorial bundle existence places no field equation on `g`, so the full metric variation remains
the open candidate. Imposing `nabla X=0` would be an additional differential restriction and would
select `lambda=1` on the two controls, but it is not current variation authority. Boundary
variations remain open.
