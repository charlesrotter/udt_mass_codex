# F02 global-completion admissibility — exact derivation

Date: 2026-08-01  
Preregistration commit: `92c63d6`  
Mode: CPU-only exact algebra; no GPU, new action, carrier, source, boundary law, or bootstrap equation

## 1. Object being tested

The inherited conditional F02 landing is

```text
p=0, lambda=0,
u=(f,bh)=u0+a x,
E0=(1/2) a^T G a,
G=[[g_f,g_x],[g_x,g_h]].
```

On the positive Dirichlet-Hessian sector used by the preceding local witness, `G` is positive
definite. The local package established one nonperiodic example with `E0=1/8`; it did not establish
a complete global field.

The present audit exhausts the nine preregistered completion rows in `COMPLETION_CENSUS.tsv`.

## 2. Ordinary cyclic joins: the inherited shorthand is narrowed, then strengthened

The banked period-gate statement `Delta f=f1 L=0` is literally a one-cell/globally affine proof.
`D01` reproduces it and does not present it as a multi-cell theorem.

For an untwisted multi-cell chain, cell `i` has

```text
S_i=(1/2) integral u_i'^T G_i u_i' dx,
c_i=G_i u_i'.
```

At an ordinary two-sided seam with no field-sector surface source, Weierstrass-Erdmann momentum
matching gives one common covector `c_i=c`. Thus

```text
u_i'=G_i^-1 c,
0=oint du=sum_i L_i G_i^-1 c=A c.
```

For one common response matrix, `A=(sum_i L_i)G^-1`, which is invertible whenever the inherited
`Delta_G!=0` condition holds; positivity is not needed. More generally, every `G_i` in the positive
angular Hessian sector is positive definite, so for every nonzero vector `v`,

```text
v^T A v=sum_i L_i v^T G_i^-1 v > 0.
```

Therefore `A` is positive definite, `Ac=0` implies `c=0`, every slope vanishes, and every local
`E0_i` vanishes. `D02-D03` instantiate the heterogeneous algebra exactly; `D03b` verifies the
common-member determinant identity. The displayed quadratic-form argument is the general positive-
sector finite-cell proof.

This is stronger and more accurate than copying the one-cell equation to many cells. It covers
ordinary flux-sealed/partner seams in the positive Dirichlet sector.

## 3. Why raw slope cancellation is not yet an escape

Two equal cells with slopes `a` and `-a` do make the raw field increments cancel. But at an
ordinary seam their momenta jump by

```text
Delta c=G(-a)-Ga=-2Ga,
```

which is nonzero for nonzero `a` and invertible `G` (`D04`). That construction is not a joined
Euler solution without an active seam source or a field transition.

A sign transition `T=-I` does transport momentum consistently:

```text
c_next=T^-T c=-c=G(-a)
```

(`D05`). This is an algebraic transition-twisted witness only. The bank records J07/J11 and the
periodic/mirror/nonorientable completion classes as requiring transition or monodromy data. It does
not provide the complete F02 field target, transformation of the response density, first-jet seam
law, cap compatibility, and coframe descent for this `T=-I` member. Consequently this route cannot
be called either a complete witness or an impossibility. It is the first reason the final status is
`OPEN`, not an exhaustive no-go.

There is a second exact cross-family control (`D05b`). On two equal cells let
`G_2=-G_1=diag(-1,+1)` and use the same momentum `c=(1,0)`. Then the slopes are opposite, their
periods cancel, the momentum matches, and the local energies are `+1/2` and `-1/2`. This abandons
the positive Hessian sector and changes the response member between cells. The repository does not
register a common moving-seam/cross-member F02 response law that makes this a completed global
solution. It therefore strengthens the `OPEN` classification of piecewise/mixed joins; it is not a
physical or stable witness.

## 4. Regular caps independently exclude affine F02

In the registered toric metric, the F02 variables are the connection moment `f` and the horizontal
squared norm `bh=b`. The cap-gluing audit derived, at every regular cap and in transverse geodesic
distance `rho`,

```text
f=f_cap+f2 rho^2+...,
b=b2 rho^2+...,
df -> 0,
db -> 0.
```

At `p=0` the F02 cell coordinate has the registered unit spatial weight, so the affine first jets
are the cap first jets. One regular cap therefore forces both affine slopes to zero globally
(`D06`). On the registered two-cap `S3` class, regularity also gives opposite moment values
`f_cap=+1,-1`; an affine function with zero derivative cannot take both values (`D07`).

This cap obstruction does not require `R-A`. Supplying `R-A` adds the already-banked definite-
parity collapse (`D08`) but is not load-bearing for the cap result.

Thus the registered one-cap and two-cap smooth toric completions cannot carry a nonzero affine F02
member in this stationary presentation. This is a completion obstruction, not a statement that the
full metric lacks non-affine smooth complete profiles.

## 5. Per-candidate ruling

`COMPLETION_CENSUS.tsv` is controlling. In summary:

- mirrored/quotient: definite-parity lifts kill F02, but quotient periods alone do not; without a
  selected complete coframe lift the remaining reading is open;
- one-cell cyclic: nonzero F02 excluded exactly;
- homogeneous common-response multi-cell cyclic: nonzero F02 excluded for every nondegenerate `G`;
  heterogeneous positive-sector chains are also excluded by the common-momentum theorem;
- transition-twisted cyclic: open because the needed complete F02 transition/descent data are not
  registered;
- open/acyclic: the local witness survives, but the endpoint and boundary functional do not turn it
  into a physical complete global object;
- regular two-cap `c=1`, with or without `R-A`: nonzero affine F02 excluded by cap regularity;
- mixed-posture/cross-census/cross-pairing: open because no complete common response and first-jet
  join is registered;
- same-closer: excluded because it is an unregistered class outside the banked two-cap arena.

## 6. Result and exact scope

```text
OPEN_INCOMPLETE_REGISTERED_CLOSURE_DATA
```

No registered complete nonzero F02 witness was found. A no-witness theorem was also not earned:
transition-twisted and mixed-family joins lack the data needed for either construction or
elimination. The old sentence “cyclic completion forces slopes zero” is valid for one-cell cycles
and, with the proof above, for homogeneous common-response multi-cell cycles and heterogeneous
positive-sector cycles. It is not valid as an unqualified theorem over transition-twisted or
cross-member indefinite completions.

The three nonzero candidate readings of the local witness remain local labels; `M_WALL=0` still
dissents. No mass reading is promoted. Native response, complete action, time persistence, full
stability, physical boundary, bootstrap selection, matter source, and species remain open.
