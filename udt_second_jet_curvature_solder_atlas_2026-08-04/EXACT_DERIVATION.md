# Exact derivation

## 1. What is new and what was already known

The July 21 P02 local-jet atlas already proved that an unrestricted regular metric two-jet spans the
complete 20-dimensional algebraic Riemann module. The July 27 P02 completion further showed that
all three screen-tidal components can be prescribed locally. Those results remain the prior
authority for local curvature freedom.

This audit does not claim that freedom as new. It inserts three pieces that P02 did not join in one
exact calculation:

1. the corrected founded reciprocal generator `H=diag(-1,+1,0,0)`;
2. the complete coframe tangent decomposition into founded, other-base, screen, and mixing motifs;
3. the causal-stratum transition from nonnull orthogonal spaces to the intrinsic null screen
   quotient.

## 2. Complete coframe second jet

At one regular point choose normal coordinates and a parallel orthonormal coframe,

```text
theta=I,  partial_mu theta=0.
```

This is a pointwise presentation choice, not a statement that the first jet vanishes nearby. The
coframe has 16 components and a symmetric coordinate Hessian has ten slots, so its full second jet
has `16*10=160` components. At the point,

```text
g_ab,mn = (X_mn^T eta + eta X_mn)_ab.
```

For each Hessian slot the `16 -> 10` map has rank ten and six-dimensional local-Lorentz
presentation kernel. Across all ten slots the exact map is

```text
160 -> 100, rank 100, nullity 60.
```

No time-time, time-space, or space-space metric Hessian component is frozen.

This normal-frame source atlas and the later supplied-`dphi` tidal atlas are two algebraic axes over
the complete curvature module. They are not silently identified as one physical solution. A
nonzero founded `dphi` cannot be inferred merely from the Hessian-source label while the chosen
point representative has zero first coframe jet. The exact status is
`SAME_SOLUTION_JOIN_OPEN_NOT_DERIVED` pending a metric-native local assignment/embedding rule.

With convention

```text
R_abcd = 1/2 (g_ad,bc + g_bc,ad - g_ac,bd - g_bd,ac),
```

the `100 -> 21` displayed symmetric-bivector map has rank 20. Equivalently the physical algebraic
curvature map is

```text
metric second jets:   rank 20, nullity 80,
coframe second jets:  rank 20, nullity 140.
```

The tensor obeys both pair antisymmetries, pair exchange, and algebraic Bianchi exactly. There is no
additional local kinematic curvature equation. This independently reproduces the load-bearing P02
result in the corrected full-coframe architecture.

## 3. Reciprocal/screen curvature blocks

In the supplied `2+2` display chart order bivectors as

```text
01 | 02,03,12,13 | 23.
```

These are respectively the reciprocal-area bivector, four base-screen mixed bivectors, and the
screen-area bivector. A symmetric curvature bilinear form on this six-dimensional bivector space
has 21 displayed entries. Every block class is individually fully available:

```text
base-base       1/1,
mixed-mixed   10/10,
screen-screen   1/1,
base-mixed      4/4,
mixed-screen    4/4,
base-screen     1/1.
```

The sole universal relation is

```text
R_(01)(23) - R_(02)(13) + R_(03)(12) = 0.
```

This is the algebraic Bianchi identity in the supplied split. It is a genuine reciprocal/angular
curvature join: the direct reciprocal-area/screen-area entry is tied to two off-diagonal entries of
the mixed-bivector block. But it is one identity among 21 displayed entries, leaving the full
20-dimensional curvature module. It is therefore a harmony rule, not a selected physical score or
field equation.

## 4. Source-ensemble atlas

Use the exact ten-direction metric tangent basis from the parent first-jet audit. Give every tangent
direction all ten coordinate-Hessian slots, then map it into curvature. Each individual tangent
generator has curvature-image rank eight. Grouping by intrinsic role gives:

| source ensemble | generator count | image rank |
|---|---:|---:|
| founded reciprocal `H` | 1 | 8 |
| other base | 2 | 11 |
| screen | 3 | 14 |
| base-screen mixing | 4 | 18 |

The support pattern is more informative than the bare ranks:

- founded `H` reaches base-base, base-mixed, and three mixed-mixed directions, but no pure screen,
  mixed-screen, or direct base-screen-area curvature;
- screen sources reach mixed-mixed, mixed-screen, and screen-screen curvature, but no base-base,
  base-mixed, or direct base-screen entry;
- mixing sources reach all ten mixed-mixed entries, all base-mixed and mixed-screen entries, and the
  direct base-screen entry, but not the two pure diagonal area blocks.

The exact union ranks are:

```text
founded+screen = 19, founded+mixing = 19,
other-base+screen = 19, other-base+mixing = 19,
screen+mixing = 19,
founded+other-base+screen = 19,
founded+other-base+mixing = 19.
```

Exactly two category-minimal triples span the full curvature module:

```text
founded + screen + mixing,
other-base + screen + mixing.
```

Thus, in this `SUPPLIED_SPLIT_LOCAL_ATLAS`, complete curvature requires the screen and mixing ensembles plus a
base ensemble. The mixing sector is an exact local bridge between base and screen curvature. The
founded reciprocal direction can fill the base role, but is not uniquely selected because the
other base directions can do so as well. This is the precise sense in which the orchestra picture
gains structure without yet gaining a conductor.

## 5. Unnormalized depth tensor

Let

```text
p=dphi,  v=p_sharp,  s=p(v),
N^a_b = s delta^a_b - v^a p_b.
```

No division by `s` is used. Direct algebra gives the universal identity

```text
N^2=s N.
```

Its ranks are:

```text
timelike 3, spacelike 3, nonzero null 1, zero 0.
```

On nonnull strata, `N/s` is the usual rank-three orthogonal projector. At nonzero null, `N` is a
nonzero rank-one nilpotent with `N^2=0`; it is not a hidden rank-two screen projector. At zero
gradient it vanishes. The unnormalized object therefore crosses the null stratum algebraically but
does not retain a constant-rank screen.

## 6. Intrinsic tidal quotients

Define the curvature tidal form

```text
T_p(x,y)=R(x,v,y,v).
```

Antisymmetry gives `T_p(v,y)=0`. For timelike or spacelike `p`, the form lives on the
three-dimensional orthogonal space and unrestricted curvature spans every symmetric bilinear form
there:

```text
dimension Sym^2(3)=6, exact image rank 6.
```

For nonzero-null `p`, `v` lies in `p_perp`. Because the tidal form annihilates `v`, it descends
without an auxiliary null vector to

```text
p_perp / span(v),
```

the intrinsic two-dimensional null screen quotient. Unrestricted curvature spans every symmetric
form on that quotient:

```text
dimension Sym^2(2)=3, exact image rank 3.
```

The independent standard-library implementation checks this descent again by shifting two quotient
representatives by different multiples of `v` and confirming the complete tidal map is unchanged.

At `p=0`, the tidal form built from `p` vanishes and no depth-selected screen remains. Thus the
metric supplies a clean stratified family of tidal spaces `6 -> 3 -> 0`, not one constant-rank
projector or one selected tidal tensor.

## 7. Relation to the earlier clock/transverse solder result

The July 24 audit derived that a supplied parallel screen line supports a scalar clock/Jacobi
generator match only when its tidal eigenvalue obeys `K=-a^2`. The present atlas neither refutes nor
enforces that conditional theorem. It shows why local curvature alone cannot enforce it: the full
nonnull tidal tensor is arbitrary in six dimensions and the null-screen tidal tensor is arbitrary
in three. No eigenline, sign, repetition, or parallel transport is selected.

## 8. Boundaries and physical ownership

At coframe rank loss the inverse metric and ordinary Levi-Civita curvature cease to exist. A finite
founded `phi` does not cause rank loss; its reciprocal pair determinant remains one. The
`phi -> +/- infinity` entries remain fixed-chart limits only and derive no endpoint or `X_max`.

Curvature reconstruction, Bianchi, and the source-ensemble ranks classify each supplied local
second jet. They do not order those jets into physical time, impose a bulk response, return a
global completion, or select a density. No action, source, carrier, boundary, bootstrap fixed point,
matter, mass, or dynamics enters this derivation.

In particular, no same-solution source/`dphi` join, physical reciprocal/screen split, or global
mixing field is derived.
