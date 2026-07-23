# Reciprocal value-character seam-descent audit

Date: 2026-07-23

## Result

The reciprocal value character has an exact global gluing mechanism that is
strictly more robust than the derivative-based `3+3` reduction.

For the prior exact preserving and inverting transition maps,

```text
G_a D(phi) G_a^-1 = D(phi),
F_b D(phi) F_b^-1 = D(-phi).
```

At the registered static mirror seal, `phi(-x)=-phi(x)`. Therefore

```text
F_b D(phi(-x)) F_b^-1 = D(phi(x)).
```

This is an identity of smooth matrix-valued functions. Consequently every
pulled-back jet matches wherever `phi` is smooth. The preregistered exact
controls explicitly verify the value, first jet, and second jet for

```text
phi=x,
phi=x^3,
phi=x+x^3.
```

The cubic control is decisive: `dphi=0` at the seal, so the normalized
derivative `3+3` reduction is unavailable there, but `D(phi)` and its seam
descent remain exact.

Maximum conclusion:

```text
RECIPROCAL_VALUE_CHARACTER_HAS_EXACT_Z2_GRADED_SEAM_DESCENT_AND_
CAN_SURVIVE_DPHI_DEGENERATION__COMPLETE_PHYSICAL_GLUE_STILL_
REQUIRES_UNSUPPLIED_COVER_EQUIVARIANCE_ANGULAR_SOLDERING_METRIC_
JETS_AND_CONNECTION_DATA__NO_REALIZATION_RELATION_OR_COMPLETION_
SELECTOR_DERIVED
```

## What is new

The July 20 cocycle audit already derived the `Z2`-graded reciprocal
transition group. This audit gives that algebra a new, nonduplicative global
role:

- the reciprocal value character can descend as an associated endomorphism
  when the supplied cover has a reciprocal-normalizer cocycle and `phi`
  transforms with its preserving/inverting grade;
- the static odd seal provides one exact instance of that equivariance;
- the descent remains valid through a critical point of `phi`; and
- the derivative-based `3+3` reduction is therefore one possible local
  realization of reciprocal structure, not the global reciprocal structure
  itself.

This is a positive global-assembly result. Its status is nevertheless
representation-level. The repository does not yet identify the abstract
reciprocal bundle with a unique physical coframe or metric sector.

## Why it does not yet join the angular orchestra

Extend the reciprocal character by the identity on an angular two-plane:

```text
D4(phi)=D(phi) direct_sum I2.
```

For any invertible angular transition `A`,

```text
T=F_b direct_sum A
```

gives

```text
T D4(phi) T^-1 = D4(-phi).
```

The angular factor cancels blockwise. Independent exact controls with a
shear and a quarter-turn both reproduce the result.

This establishes a precise nonselection statement: reciprocal seam descent
places no condition on the angular lift unless an additional
reciprocal-angular soldering is supplied. It does not prove that physical
UDT sectors are dynamically decoupled. It proves only that this value-level
descent identity does not couple them.

The conditional reciprocal-toric row remains an exact compatibility
witness. Its integral torus basis, periods, cap or boundary data,
orientation, normalization, and identification of angular directions with
the reciprocal weights remain supplied inputs rather than consequences of
the seam identity.

## Why it is not yet physical metric or connection glue

Three layers remain distinct:

1. `D(phi)` descending as an associated reciprocal endomorphism;
2. a physical coframe/readout identifying that bundle with spacetime slots;
3. a full metric and connection extending across overlaps and boundaries.

The first layer is exact under its cocycle/equivariance conditions. The
second remains open because multiple conditional readouts and angular lifts
survive. The third additionally requires the complete metric value, first
jets, transition derivatives, cap or boundary extensions, and connection
gluing.

At the static mirror seam the constant reciprocal transition contributes no
transition-derivative term, but this does not create a local connection or
supply the angular and full-metric connection. The result therefore cannot
be promoted to a Levi-Civita gluing theorem for a complete UDT universe.

## Twelve-family census

[COMPLETION_DESCENT_ATLAS.tsv](COMPLETION_DESCENT_ATLAS.tsv) classifies all
twelve registered rows.

Principal outcomes:

- **Boundary rows:** `D(phi)` reaches a boundary whenever finite `phi` does,
  but boundary jets and a physical connection remain free.
- **Regular cap rows:** value descent is conditional on a smooth finite
  `phi` extension and the independently supplied angular cap jets. No cap
  class is selected.
- **Static compact two-cap rows:** the required critical point does not
  destroy `D(phi)`, even though it destroys global derivative `3+3`
  persistence.
- **Singular/nonprimitive row:** `D(phi)` remains classifiable on the regular
  complement; no smooth through-singularity claim is made.
- **Periodic torus bundle:** global descent requires reciprocal-normalizer
  monodromy, graded `phi` equivariance, endpoint-jet matching, and the
  separate `GL(2,Z)` angular monodromy.
- **Mirror double:** the registered odd seal supplies exact reciprocal
  value and jet descent; the angular lift and full physical glue remain
  unselected.
- **Nonorientable row:** the value character can live in a twisted
  reciprocal bundle without choosing an orientation. Ordinary global Hodge
  exchange still needs an orientation or orientation-line treatment.
- **Stratified-projector row:** `D(phi)` survives the degeneration of the
  normalized `dphi` projector wherever the metric and finite `phi` remain
  regular.
- **Nonintegrable row:** value descent does not require orbit surfaces or
  integrability.
- **Reciprocal-toric row:** the known angular compatibility remains exact
  conditional, not a native soldering theorem.

All twelve remain registered alternatives. Eleven are parametric types and
one is a conditional toric control; none supplies a complete on-shell
`(g,phi)` witness.

## Relation to realization and density

The new result narrows the realization gap but does not close it.

```text
local reciprocal character
    -> conditional global twisted reciprocal object
    -> OPEN reciprocal-angular soldering
    -> OPEN physical metric and connection glue
    -> OPEN realized complete branch
    -> OPEN native source, mass, and density response.
```

Thus the reciprocal value character is not confined to regions where
`dphi` is nonzero and nonnull. But no operation yet chooses a cover,
equivariance class, angular lift, physical readout, or complete branch.
Density bracketing remains inactive because the native mass and response
interface is still absent.

## Verification

- deterministic algebra: pinned SymPy `1.14.0`;
- independent implementation: PASS;
- completion rows: 12/12;
- mirror profiles with value/first/second-jet match: 3/3;
- critical-`dphi` controls: 1;
- exact/global theorem rows: 12;
- source identities: 22;
- exercised mutation catches: 25/25;
- fresh zero-context adversarial review: `VERIFIED`, with no load-bearing
  objection after an independent symbolic replay;
- repository and frozen-package gates: recorded separately.

## Four evidence gates

1. **Preregistered:** yes, commit `67ac641`.
2. **Full space or bounded scope:** complete for the twelve registered
   completion rows, prior reciprocal normalizer algebra, and preregistered
   value/jet controls; not arbitrary covers or complete field equations.
3. **Independently verified:** yes, with different numeric normalizer
   representatives, two distinct angular transitions, direct jet algebra,
   source replay, and mutation catches.
4. **Every premise audited:** yes; cover, equivariance, angular lift,
   orientation, singularity, physical readout, metric jets, connection,
   action, source, density, carrier, and scale remain visibly separated.

Banking grade: `VERIFIED-BOUNDED`. The bounds are the registered completion
taxonomy and conditional reciprocal-bundle equivariance, not a remaining
verification defect.
