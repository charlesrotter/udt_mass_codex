# Complete-seal fixed-set and orientation selector audit

Date: 2026-07-21

## Result first

The finite-cell seal does not currently select the reflection-type angular lift needed by the
boundary-seeded full two-pair proposal.

The exact C0/C1 authority says only:

```text
phi is odd at the seal,
phi=0 there,
the normal derivative of phi is free.
```

It explicitly leaves the transverse metric, time-on data, full induced metric, normal metric jet,
and complete coframe action open. The prior boundary audit also ruled that the word “mirror” does
not make the complete metric an ordinary pointwise reflection.

Fixed-set geometry nevertheless gives exact conditional classifications:

- If the seal were a pointwise fixed codimension-one metric hypersurface preserving time, only the
  angular `+I` lift would qualify. It has fixed/anti-fixed multiplicity `3/1` and reverses only the
  radial spatial normal.
- If the seal were required to preserve four-dimensional orientation, the axis-reflection and local
  Hopf-exchange lifts would remain. Both have multiplicity `2/2`; they are the same local reflection
  conjugacy class.
- The angular `-I` lift has multiplicity `1/3` and would be a codimension-three, time-axis-type fixed
  set.
- Time-orientation preservation distinguishes none of them: every lift fixes the conditional
  timelike base line.

None of those added interpretations is current UDT authority. In particular, orientability of the
spacetime does not require every isometry to preserve orientation; an ordinary spatial mirror is an
exact orientation-reversing isometry of an orientable Lorentz metric.

The resulting status is:

```text
COMPLETE_LIFT_REMAINS_OPEN_BECAUSE_SEAL_POINTWISE_ACTION_IS_UNDERDETERMINED.
```

This closes one tempting shortcut. The desired second reciprocal pair cannot be used to choose the
reflection lift that is required to construct it.

## Lay interpretation

Calling the edge a “mirror” sounds as though it should settle everything. It does not.

The established rule says that one quantity—reciprocal depth—changes sign across the fold and is
zero at the fold. It does not say what happens to every direction lying along the fold.

If this were an ordinary wall mirror, the clock and both sideways directions would stay fixed while
only the outward direction reversed. That would select the simplest transverse-identity lift. But
that same lift cannot create the second angular reciprocal pair.

To obtain the second pair, the seal must also flip one sideways angular direction. Then the fixed
set is no longer an ordinary three-dimensional boundary mirror; it is a different, codimension-two
identification. UDT has not supplied that extra angular operation.

So the boundary has not secretly solved the full-pair problem. It has told us exactly what extra
statement would be required.

## Complete lift table

Use the normalized conditional base seal

```text
R_base=diag(+1,-1),
```

where the timelike line is fixed and the radial spacelike line is reversed. Appending the four
registered angular lifts gives:

| angular lift | full determinant | fixed/anti-fixed | fixed-set codimension if pointwise | second angular pair |
|---|---:|---:|---:|---|
| `+I` | `-1` | `3/1` | 1 | no |
| `-I` | `-1` | `1/3` | 3 | no |
| axis reflection | `+1` | `2/2` | 2 | conditional yes |
| local Hopf exchange | `+1` | `2/2` | 2 | conditional yes |

The determinant always equals `(-1)^(anti-fixed dimension)`. Removing the fixed time line gives
spatial anti-fixed dimensions `1,3,2,2`, respectively.

The axis reflection and local Hopf exchange are related by an exact 45-degree orthogonal basis
change. They are locally the same kind of mirror. Distinguishing them requires global angular data
such as a preferred integral basis, periods, cover, or quotient action—none of which is selected.

## What a pointwise fixed set would mean

For a smooth involutive isometry at a fixed point,

```text
T Fix(R)=ker(R-I),
N Fix(R)=ker(R+I).
```

Thus the anti-fixed dimension is the local codimension of the fixed set. A pointwise fixed
three-dimensional seal in four-dimensional spacetime has exactly one reversed normal direction and
therefore selects the `3/1` or `+I` class.

But that is an additional premise. Current authority establishes a scalar zero-locus, not pointwise
fixation of every angular and time-on coordinate.

There is also a derivative consequence. If an ordinary mirror sends `n` to `-n` while leaving a
tangential metric component fixed, then

```text
h(n)=h(-n)
```

forces its first normal derivative to vanish at the mirror. By contrast, the allowed odd profile

```text
phi=a n
```

has a free nonzero slope. In the declared diagonal reciprocal readout,

```text
h_tt=-exp(-2an),
partial_n h_tt at n=0 = 2a.
```

This is precisely why the prior boundary audit rejected converting the scalar fold into an ordinary
even tangential metric. A future complete coframe involution could transform sectors nontrivially,
but that transformation is the missing object; it cannot be assumed.

## Orientation does not rescue the reflection lift

If one separately demands `det(R)=+1`, the two reflection lifts survive and the two identity lifts
are removed. This is an exact conditional class selection.

No existing UDT rule makes that demand. An orientable manifold can possess orientation-reversing
symmetries. The canonical radial mirror

```text
diag(+1,-1,+1,+1)
```

is an isometry of the oriented Minkowski metric and has determinant `-1`. Moreover, the orientation
of a gluing transition between two oppositely oriented copies is not the same question as the
determinant of the physical involution on one tangent space.

Even if orientation preservation were added, it would leave both axis reflection and Hopf exchange.
Choosing the latter because it resembles the desired Hopf completion would be circular.

## First normal metric jets

For a supplied full involution with `f` fixed and `a` anti-fixed directions, a symmetric metric jet
splits into

```text
even dimension = f(f+1)/2 + a(a+1)/2,
odd dimension  = f a.
```

The four lifts therefore give:

- `3/1` and `1/3`: seven even and three odd symmetric jet components;
- `2/2`: six even and four odd components.

An odd full metric jet can live only between fixed and anti-fixed subspaces. Current scalar parity
does not specify which complete tensor components carry that oddness, so these counts classify
possible completions but do not select one.

## Nonzero cross-coupling

All eight exact nonzero-cross witnesses—four lifts at `mu=4` and `mu=9`—retain Lorentz signature,
their determinant orientation, and their fixed/anti-fixed multiplicities. Coordinate mixing between
the base and angular blocks therefore does not convert one fixed-set class into another.

The result is geometric rather than an artifact of a product metric.

## Consequence for the two-pair lead

The parent audit established:

- identity angular lifts have zero anticommutant and cannot seed a second reciprocal pair;
- reflection angular lifts plus the screen metric determine a complementary pair at the seal.

The present audit establishes that current finite-cell authority does not select between those
classes. Requiring the desired second pair would select the reflection class only by assuming the
answer.

The boundary-seeded full-pair route therefore remains

```text
CONDITIONAL_ON_A_SEPARATELY_DERIVED_NON_POINTWISE_ANGULAR_IDENTIFICATION.
```

This is not a proof that no such identification exists. It is a proof that scalar fold parity,
orientation, time orientation, fixed-set regularity, and the registered nonzero cross coupling do
not presently derive it.

## Scientific consequence

The full two-pair tangent-bundle idea has now accumulated two independent missing premises:

1. a non-pointwise angular seal identification selecting the reflection class; and
2. a bulk holonomy-reduction law extending the seal-local pair consistently.

That makes it less economical as the immediate foundational interpretation.

A cleaner possibility already visible in the parent connection algebra is that UDT requires only
the **reciprocal longitudinal two-plane** to be preserved, not two individually fixed angular
reciprocal axes. The seal-local clock/radial soldering and metric-orthogonal screen already provide
the relevant plane projector conditionally, while the angular screen is then allowed to possess its
own intrinsic rotation and holonomy.

That projector interpretation has not been newly derived here. It is the highest-value next audit
because it tests whether the full-pair detour was an overconstraint rather than adding another
mechanism.

No lift, orientation law, angular quotient, transport law, action, topology, carrier, source,
boundary charge, mass, scale, GPU result, or canon entry was adopted.

## Four evidence gates

1. **Preregistered:** yes, commit `f9b9057`, before source adjudication and algebra.
2. **Full space or bounded scope:** complete for the four registered constant angular lift classes,
   their local fixed-set/orientation meanings, first symmetric metric jets, and eight nonzero-cross
   witnesses; not field-dependent lifts or global quotient topology.
3. **Independent verification:** separate standard-library rational reconstruction, source/status
   replay, and exercised fail-closed mutations.
4. **Premise audit:** scalar versus metric mirror, pointwise versus setwise action, orientation,
   time orientation, cross coupling, two-pair circularity, global angular data, boundary, action, and
   carrier limits are explicit.

Maximum conclusion:

`UDT_COMPLETE_SEAL_FIXED_SET_SELECTOR_STATUS_CHARACTERIZED`.
