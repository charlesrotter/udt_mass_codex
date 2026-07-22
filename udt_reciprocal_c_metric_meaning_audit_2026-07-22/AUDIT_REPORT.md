# UDT reciprocal-c metric meaning and observational-frame audit

Date: 2026-07-22

Base: `f5f30018dda111f4bf131a5675f8480ca605a268`

Preregistration commits: `bd43cdb0ad11ae7fa12e20c9d19794e996b460de`,
`c5913a551402286d0a372916da475e1eda52017c`

Mode: source-led exact CPU algebra; no ODE/PDE, GPU, action, carrier, or artifact mutation

Grade: `VERIFIED-WITH-CAVEATS`; independent standard-library rational verification passes, while no
fresh external-model semantic review was authorized

## Result first

The owner correction is significant and the post-firewall source chain confirms it.

The current foundation already contains two distinct founding statements:

```text
Reciprocal-c: c_E and 1/c_E are coequal directions of one clock-length conversion.
UDT Reciprocity: positional comparison acts contragrediently on those directions.
```

For the registered positive diagonal comparison `P=diag(u,v)` and pairing
`K=[[0,1],[1,0]]`, the second statement gives exactly

```text
P^T K P = K  =>  uv=1.
```

Regular additive composition then gives, up to the recorded sign/unit convention,

```text
D(phi)=diag(exp(-phi),exp(phi)).
```

With the separately declared local Lorentzian quadratic readout, the dimension-matched
clock–distance block is

```text
g_2=diag(-exp(-2phi),exp(2phi)),   det(g_2)=-1.
```

Therefore the reciprocal measurement block is `DERIVED / CONDITIONAL` on the already explicit
composition, regularity, sign/unit, CSN representative, and local interval-readout premises. It was
not waiting for a universal preferred rank-two subbundle to be discovered.

The recorded static spherical metric is likewise recovered exactly in its declared realization:

```text
ds^2 = -c_E^2 exp(-2phi) dt^2
       + exp(2phi) dr^2
       + r^2 dtheta^2
       + r^2 sin(theta)^2 dvarphi^2.
```

Its four-volume is independent of `phi`. Its premise stamp includes the temporal/radial coframe
slots, local Lorentzian readout, diagonal transverse completion, and spherical areal angular
coframe. The result does not derive `phi(r)`, an action, or a general nonspherical/time-live metric.

## Observational-frame reciprocity

Charles additionally owner-clarified a GR-like reciprocity of macro observational frames: no
observer is privileged by the laws, and the reciprocal measurement relation must have the same
physical content in different descriptions.

The exact ordinary-regime Lorentz control separates two meanings that had been conflated. Under a
coframe change `Lambda`, the reciprocal endomorphism transforms by conjugation,

```text
D' = Lambda D Lambda^-1,
```

and the induced metric transforms tensorially. The two constructions agree exactly. Thus nonzero
reciprocal dilation is compatible with observer reciprocity.

By contrast, a nontrivial diagonal `D` does not commute with a boost. Requiring the same numerical
diagonal array in every boosted observer coframe forces the trivial `phi=0` branch. Identical
components are not covariance.

A particular solution may still contain distinguished fields, gradients, symmetries, clock
congruences, or matter rest frames. Those solution data transform under observer changes and do not
make one observer fundamental in the laws.

This audit does not import Einstein equations, an EH action, a gravity–acceleration equivalence, the
complete GR observer formalism, universal Lorentz behavior at extreme `phi`, or a micro-UDT frame
theorem.

## Why the general four-dimensional join remains open

A relational clock–displacement rule is complete for the compared `1+1` pair, but it does not by
itself specify one arbitrary `3+1` metric.

The production and independent calculations exhibit three exact controls:

1. Applying the reciprocal factor to the `x` direction versus the `y` direction produces distinct
   four-metrics for nonzero `phi`.
2. Scaling one clock reciprocally against all three spatial axes as
   `diag(exp(-phi),exp(phi),exp(phi),exp(phi))` has determinant `exp(2phi)`, not one.
3. At least two inequivalent determinant-one spatial-weight assignments exist:
   exponent weights `(-1,1/3,1/3,1/3)` and `(-3,1,1,1)`.

Therefore pair Reciprocity does not uniquely determine how reciprocal weight is distributed over a
general three-dimensional spatial sector. The static spherical metric has already declared its
radial/areal realization. What remains `OPEN` is its covariant nonspherical, shift-bearing,
time-live, and possibly micro extension.

## Regrade of the immediately prior audit

The reciprocal-subbundle package's exact stabilizer, causal-stratum, curvature, seal, and transport
calculations remain valid. Its universal no-selector conclusion also remains valid against a
candidate law-fixed rank-two plane.

The semantic correction is:

```text
A universal law-fixed rank-two plane is not required by PAIR_RELATIONAL meaning.
```

Consequently the lack of such a selector is no longer the leading missing UDT premise. The smaller
open join is a general metric/coframe assembly rule that tells how the founded reciprocal
clock–distance relation meets the angular and shift sectors away from the declared static spherical
realization.

The earlier `phi` ontology result is narrowed in the same way. `phi` already owns the logarithmic
imbalance in the reciprocal measurement block. Which general complete off-shell geometric object
owns and varies that block remains open.

## Configuration-atlas qualification

The independent-amplitude and structural-ensemble atlases deliberately varied ten complete metric
amplitudes and `phi` independently. Their exact tensor and invariant results are retained. In the
absence of a native action or assembly law, however, they are configuration atlases, not the UDT
solution space. Their breadth cannot be used to undo the founded reciprocal subfamily.

## Source and verification record

Twelve exact post-firewall sources are frozen in `SOURCE_LINEAGE.tsv`. The SymPy production route
passes 20/20 exact checks. A separate implementation using only Python's `Fraction` arithmetic
reconstructs 17 load-bearing algebra controls, validates all five ledgers and all source identities,
and passes 18/18 exercised catch-proofs.

## Evidence gates

1. **Preregistered:** yes. Both the initial scope and Charles's observer-frame clarification were
   committed before production algebra.
2. **Full or bounded scope:** complete for the enumerated reciprocal pair, ordinary-regime passive
   Lorentz control, directional/isotropic weight controls, and static spherical reconstruction. It
   is not a classification of all observer groups, all possible 3+1 representations, or dynamics.
3. **Independently verified:** yes for the load-bearing algebra, tables, sources, and repository
   state. No fresh external-model semantic review was authorized, so the grade is
   `VERIFIED-WITH-CAVEATS`.
4. **Premises audited:** reciprocal-c, dual Reciprocity, composition, nontriviality, CSN, interval
   readout, coframe slots, angular completion, observer scope, action, carrier, boundary, scale, and
   micro limitations are explicit.

## Stop line

No navigation control, prior evidence, action, source, carrier, boundary charge, mass, scale,
`X_max`, time-live law, GPU computation, canon, or repository organization is changed.

Maximum conclusion:

```text
THE_FOUNDING_POSTULATES_PLUS_THEIR_REGISTERED_COMPOSITION_AND_READOUT_PREMISES
DERIVE_THE_RECIPROCAL_CLOCK_DISTANCE_METRIC_BLOCK;
GR_LIKE_MACRO_OBSERVER_RECIPROCITY_IS_TENSORIALLY_COMPATIBLE_WITH_NONZERO_DILATION;
THE_RECORDED_STATIC_SPHERICAL_METRIC_REMAINS_DERIVED_CONDITIONAL;
ONLY_THE_GENERAL_NONSHPERICAL_TIME_LIVE_MICRO_3PLUS1_ASSEMBLY_REMAINS_OPEN.
```
