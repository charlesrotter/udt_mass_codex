# UDT complete-lift and global-cocycle `mu` closure audit

Date: 2026-07-20

## Result first

No already-registered complete seal lift, orientation class, overlap/corner cocycle, normalized seal
transition, or conditional Hopf cap construction fixes or rejects `mu`.

The structural reason is exact:

> After the seal-local clock/radial frame is normalized, every mixed-family base seal is the same
> standard spatial reflection `diag(+1,-1)`. The invariant `mu` remains in the relationship between
> the metric and reciprocal generator, not in the seal transition itself.

Consequently, composing existing seal maps cannot select `mu`. Their group words literally do not
contain it.

All four registered local angular lift classes also admit exact nonzero-coupling Lorentz witnesses
at both `mu=4` and `mu=9`. This includes orientation-reversing and orientation-preserving classes.

## Complete lift and cross-block census

For

```text
G=[[H,C],[C^T,Q]],       R=diag(F,A),
```

the full isometry equations split into

```text
F^T H F=H,
F^T C A=C,
A^T Q A=Q.
```

The complete parity-compatible cross blocks in the registered representative classes are:

| angular lift | cross block `C` | orientation | fixed/anti-fixed |
|---|---|---:|---:|
| `+I` | `[[u,v],[u,v]]` | `-1` | `3/1` |
| `-I` | `[[u,v],[-u,-v]]` | `-1` | `1/3` |
| axis reflection | `[[u,v],[u,-v]]` | `+1` | `2/2` |
| local Hopf exchange | `[[u,v],[v,u]]` | `+1` | `2/2` |

Each family has two independent cross parameters. None of the equations constrains the mixed-base
parameter `k=sqrt(mu)`.

## Eight exact nonzero-coupling witnesses

Set `u=v=1/10` and use the same positive angular metric `I2` inside each lift. Every witness has
signature `(-,+,+,+)`.

| lift | `mu` | determinant | full pair invariant |
|---|---:|---:|---:|
| `+I` | 4 | `-78/25` | `-251/78` |
| `+I` | 9 | `-204/25` | `-251/102` |
| `-I` | 4 | `-74/25` | `-247/74` |
| `-I` | 9 | `-198/25` | `-248/99` |
| axis reflection | 4 | `-7599/2500` | `-8300/2533` |
| axis reflection | 9 | `-20099/2500` | `-49900/20099` |
| local Hopf exchange | 4 | `-78/25` | `-251/78` |
| local Hopf exchange | 9 | `-204/25` | `-251/102` |

The different full pair invariants certify inequivalence within every lift. Nonzero angular mixing
does not collapse the modulus.

## Orientation and tangent multiplicity

If a future rule demanded an orientation-reversing seal, the `+I` and `-I` lifts would remain. If it
demanded an orientation-preserving seal, the axis-reflection and local Hopf-exchange lifts would
remain. Both sides contain `mu=4` and `mu=9`.

Likewise the `3/1`, `1/3`, and `2/2` coframe fixed/anti-fixed classes all retain both values.
Orientation and multiplicity may reduce lift families after their physical meanings are supplied;
they do not determine `mu`.

## Why the cocycle is blind

The reciprocal transition algebra is

```text
F_b F_c=G_(b/c),
F_b F_c G_(c/b)=I,
```

and closed loops have even reversal parity. Corner reductions constrain transition ratios, angular
axis differences, and a separately declared finite order. None contains `B/A` and therefore none
contains

```text
mu=B^2/(A^2 b^2).
```

Even a corner that fixes `b/c=+1` or `-1` leaves `B/A` free. For angular axis reflections the corner
trace is

```text
2 cos(2(theta-psi)),
```

again independent of `mu`.

In the seal-normalized base frame,

```text
F_normalized=diag(+1,-1)
```

for every `k>1`. The normalized reciprocal generator still contains
`sqrt((k-1)/(k+1))`. The transition has forgotten the modulus while the metric/reciprocity pair has
not. This proves `NORMALIZED_SEAL_TRANSITIONS_ARE_MU_BLIND`.

## Conditional Hopf route

The local exchange is simply another orientation-preserving reflection class and retains both
witnesses. Its global cap data also do not help under current authority. Mirror-compatible primitive
cycle pairs realize determinant classes `p=0,1,3,5` and more. The conditional `p=1`/`S3` theorem
requires the separately unselected transverse spatial torus, periods, global diagonal basis, and
opposing eigen-circle caps.

Those integer lattice conditions contain no `mu` equation. Naming the Hopf completion therefore
does not select the mixed-base modulus.

## What could see `mu`

A metric-dependent object can see it. The preceding audit explicitly showed curvature dependence on
`mu` after a varying metric is supplied. Levi-Civita or conformal Cartan holonomy could likewise
distinguish completed metrics after a representative, loop family, and global reduction are given.

But current UDT supplies no selected complete metric, cover, loop incidence, cap/boundary map, or
global admissibility equation that converts that metric dependence into a closure condition. Current
bootstrap remains an after-solution predicate with no varied functional or representative section.

Thus `METRIC_DEPENDENT_GLOBAL_CLOSURE_EQUATION_ABSENT` is a statement about the current ledger, not a
theorem that no future completion can contain one.

## Supported preregistered outcomes

- `ORIENTATION_CLASS_LEAVES_MU_OPEN`;
- `CORNER_COCYCLE_IS_MU_BLIND`;
- `ALL_REGISTERED_ALGEBRAIC_LIFTS_LEAVE_MU_OPEN`;
- `NONZERO_CROSS_BLOCKS_LEAVE_MU_OPEN_IN_EVERY_LIFT`;
- `NORMALIZED_SEAL_TRANSITIONS_ARE_MU_BLIND`;
- `CONDITIONAL_HOPF_LIFT_HAS_NO_CURRENT_MU_EQUATION`;
- `METRIC_DEPENDENT_GLOBAL_CLOSURE_EQUATION_ABSENT`; and
- `GLOBAL_COMPLETION_REMAINS_OPEN`.

No unique lift, orientation, corner, topology, or modulus is selected.

## Scientific consequence

The involution/cocycle line is now exhausted as a `mu` selector under current premises. More group
composition will only recombine `mu`-blind objects.

The next useful derivation would have to produce a genuinely metric-dependent global closure from
the finite-cell metric itself—for example a derived boundary/regularity, holonomy-reduction, or
bootstrap functional equation. None may be adopted merely because it would fix `mu`.

No action, topology, representative, boundary charge, carrier, source, mass, scale, or GPU result
was selected in this audit.

## Evidence gates

1. **Preregistered:** yes, commit `07ed116`, before source inspection and algebra.
2. **Full space or bounded scope:** complete for the registered isotropic real lift classes and
   their complete constant parity-compatible cross blocks; bounded with respect to field-dependent
   lifts and all possible global bundles.
3. **Independent verification:** separate standard-library rational matrix reconstruction, group
   checks, source/status replay, and fail-closed mutations.
4. **Premise audit:** orientation, cover, incidence, corner order, caps, topology, Cartan loops,
   bootstrap, boundary, and matter/action limits are explicit.

Maximum conclusion:

`UDT_COMPLETE_LIFT_AND_GLOBAL_MU_CLOSURE_STATUS_CHARACTERIZED`.
