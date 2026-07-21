# UDT global coframe cocycle and finite-cell tangent audit

Date: 2026-07-20

Base: `c8d337fb06b90126756483af86f105e2fbb4eabb`

## Result first

The global-completion lead does not yet close uniquely, but the derivation found a genuinely useful
positive bridge that was hidden by an overly restrictive basis choice.

The exact outcomes are:

- `COCYCLE_CONSISTENCY_REDUCES_BUT_DOES_NOT_SELECT`;
- `GLOBAL_COCYCLE_CANNOT_BE_POSED_WITHOUT_OPEN_TOPOLOGY_OR_COVER`;
- `BOUNDARY_TANGENT_SPACE_REMAINS_POLARIZATION_DEPENDENT`;
- `CURRENT_DATA_DEFINE_ONLY_LOCAL_OR_SECTORWISE_INVOLUTIONS`;
- `MULTIPLE_GLOBAL_COMPLETIONS_SURVIVE_CONDITIONALLY`.

The preregistered unique global coframe and tangent completion is not earned.

However, the earlier apparent choice between a physically visible diagonal reciprocal metric and a
mirror-compatible but `phi`-invisible dual metric was not exhaustive. The complete constant real
symmetric `2x2` readout classification contains a mixed Lorentzian family that does both jobs.

## The positive mixed-readout theorem

Retain the exact reciprocal operator

```text
P(phi)=diag(exp(-phi),exp(phi))
```

and the complete real constant inverting involution

```text
F_b=[[0,b],[1/b,0]],       b nonzero.
```

Start with the general constant symmetric readout

```text
H0=[[A,B],[B,C]].
```

Require the physical metric block

```text
g(phi)=P(phi)^T H0 P(phi)
```

to close across the seal up to a positive common factor:

```text
F_b^T g(-phi) F_b = Omega^2 g(phi).
```

The exact component equations are

```text
C/b^2 = Omega^2 A,
B     = Omega^2 B,
A b^2 = Omega^2 C.
```

For a Lorentzian solution, `B` cannot vanish. Therefore `Omega^2=1` and

```text
C=A b^2.
```

The complete family in this declared class is consequently

```text
H0=[[A,B],[B,A b^2]],
g(phi)=[[A exp(-2phi), B],
        [B, A b^2 exp(2phi)]],
B^2>A^2 b^2.
```

It obeys the exact mirror identity

```text
F_b^T g(-phi) F_b = g(phi),
```

has constant negative determinant `A^2 b^2-B^2`, and retains physical `phi` dependence whenever
`A` is nonzero. The pure dual-pairing `K` readout is only the limiting case `A=0`, where `phi`
disappears from the isolated metric block.

This exposes the earlier mistake in geometric terms: diagonalizing the reciprocal operator and the
Lorentz readout simultaneously was an additional restriction. They need not share an eigenbasis.

### Explicit spatial-reflection witness

For

```text
A=1, B=-2, b=1,
H0=[[1,-2],[-2,1]],
```

the determinant is `-3`. In the balanced Hadamard basis,

```text
H0 -> diag(-1,3),
F_1 -> diag(1,-1).
```

Thus the same exact candidate looks like an ordinary Lorentzian spatial reflection: it fixes the
timelike line, reverses the spacelike line, keeps `phi` visible, and closes the seal.

This is `DERIVED_CONDITIONAL`, not a selected UDT readout. The finite-cell canon does not yet declare
the complete metric seal to be an isometry, the mixed time/radial soldering is not owner-locked, and
the relationship of its anchor basis to the observed `c` clock/ruler frame remains open.

### The remaining local modulus

After common scale and diagonal reciprocal-frame changes, the dimensionless quantity

```text
mu = B^2/(A^2 b^2) > 1
```

is invariant. Exact full four-metric direct extensions with `mu=4` and `mu=9` both retain Lorentz
signature, `phi` visibility, the same angular `+I` lift, and exact mirror closure. Current CSN,
reciprocity, and involution rules therefore do not select `mu`.

The positive theorem removes a false either/or but replaces it with a sharper question: what fixes
the physical soldering, observer slicing, and invariant mixing modulus while retaining the measured
`c` anchor?

## The reciprocal transition-group theorem

Define the preserving component

```text
G_a=diag(a,1/a)
```

and the inverting component `F_b` above. Exact multiplication gives

```text
G_a G_d = G_ad,
F_b F_c = G_(b/c),
G_a F_b = F_(ab),
F_b G_a = F_(b/a).
```

This is a `Z2`-graded transition group: `G` maps preserve reciprocal depth orientation and `F` maps
reverse it. Every closed transition cocycle has even reversal parity.

In particular,

```text
F_b F_c F_d = F_(bd/c),
```

so three depth-inverting overlap maps cannot multiply to the identity. A valid three-chart witness
is instead

```text
F_b F_c G_(c/b)=I.
```

This is real new structure: UDT's reciprocal data already determine the algebra that a global
coframe bundle must use. But an algebra of transitions is not the chart cover on which they act.
Current finite-cell authority does not supply that cover, its overlap incidence, or its global
`Z2` class.

Conjugation gives

```text
G_a F_b G_a^-1=F_(a^2 b).
```

Thus the magnitude of `b` is conjugate inside each real sign class. Its sign controls which
conditional `K` eigenline is timelike, but even that interpretation presupposes the physical
readout/slot choice.

## Corner constraints reduce only after a corner is supplied

For two declared seal generators, commuting base reflections require `c=+b` or `c=-b`. Angular axis
reflections commute only when their axes are the same or perpendicular. More generally, a declared
finite corner order `m` imposes

```text
b/c=1,
```

or `b/c=-1` for even `m`, and angular axes separated by `pi k/m`.

These are exact reductions. They do not select `m`, a corner angle, the number of seals, or their
incidence graph. Those are precisely the open global data the audit was forbidden to invent.

## Full lifts and boundary tangents remain nonunique

Combining the reciprocal reflection with angular `+I`, angular `-I`, or an angular axis reflection
gives three invariantly distinct full local classes:

| Angular lift | Full determinant | Coframe fixed/anti-fixed | Metric even/odd |
|---|---:|---:|---:|
| `+I` | `-1` | `3 / 1` | `7 / 3` |
| `-I` | `-1` | `1 / 3` | `7 / 3` |
| axis reflection | `+1` | `2 / 2` | `6 / 4` |

Orientation would remove some rows only if the required orientation behavior were supplied. It is
not. Treating the seal as an ordinary fixed hypersurface would select the `3/1` class, but that is
also not present in the scoped canon and cannot be inserted retroactively.

The static rule `delta phi=0` removes one scalar direction from the ten-dimensional symmetric
metric tangent space, leaving nine. It is therefore not any of the complete `6`- or `7`-dimensional
even tangent spaces above. Even after choosing an involution, the conditional bare-`C2` phase space
still permits inequivalent `delta h`, `delta K`, momentum, mixed, and corner polarizations. Symmetry
does not select the variational boundary class.

## Regular caps do not select the topology

Primitive mirror-compatible toric cap cycles retain determinant classes

```text
p=0, 1, 3, 5
```

in exact witnesses, with general lens classes beyond them. Smooth primitivity and angular exchange
therefore do not select the `p=1` `S3` completion. That topology remains unique only after the
previously registered globally diagonal opposing-eigen-circle cap premises are supplied.

## Adjudication

The possible `GLOBAL_COMPLETION_MAP` was not derived. The work did, however, replace a vague gap
with two exact structures:

1. a complete conditional mixed-readout family that reconciles physical reciprocal dilation with
   Lorentzian mirror closure;
2. the `Z2`-graded reciprocal transition algebra every future global completion must carry.

Neither structure selects its invariant modulus, physical soldering, cover, caps, angular lift, or
boundary polarization. The result is therefore a strong lead and a constraint on future answers,
not global closure.

No action, bootstrap selector, scale, `X_max`, topology, carrier, source, or mass has been promoted.

## Evidence gates

1. **Preregistered:** yes, commit `e88ef5c` predates candidate inspection and derivation.
2. **Full space or bounded scope:** complete for constant real symmetric `2x2` readouts and the
   declared full-block/angular/corner witness classes; not a classification of arbitrary
   field-dependent `4x4` solderings or every global bundle.
3. **Independent verification:** yes. A separate Python-standard-library implementation uses exact
   rational matrices and independent rank calculations rather than the SymPy derivation code.
4. **Premise audit:** yes. Every physical readout, topology, corner, orientation, polarization, and
   matter/action premise remains visibly stamped.

Grade: `VERIFIED_WITH_CAVEATS`.

Maximum conclusion: `UDT_GLOBAL_COFRAME_COCYCLE_STATUS_CHARACTERIZED`.
