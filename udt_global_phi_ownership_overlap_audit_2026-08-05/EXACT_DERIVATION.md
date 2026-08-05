# Exact derivation — global founded-depth ownership across overlaps

## 1. Local factorization action

Use multiplicative character coordinates

```text
A(z)=diag(z^-1,z),       z=exp(phi)>0,
K(h)=diag(A(h),I_2),     h=exp(chi)>0.
```

For the registered factorized complete-coframe chart

```text
E(z,D,S) = [[A(z), 0],
            [D S,  D]],
theta = E bar_theta,
```

define

```text
z'         = z h,
S'         = S A(h),
bar_theta' = K(h)^-1 bar_theta.
```

Exact block multiplication gives

```text
E(z h,D,S A(h)) K(h)^-1 = E(z,D,S),
theta'=theta.
```

This is the parent local factorization identity expressed without transcendental arithmetic. It is
an identity among presentations of the supplied architecture. It is not promoted to a physical
gauge principle.

## 2. Three-chart overlap calculation

On overlaps let

```text
theta_j     = L_ij theta_i,
bar_theta_j = R_ij bar_theta_i,
E_j         = L_ij E_i R_ij^-1.
```

After independent local factorization shifts `K_i`, the physical transition is unchanged and the
reference transition becomes

```text
R'_ij = K_j^-1 R_ij K_i.
```

Therefore

```text
E'_j = L_ij E'_i (R'_ij)^-1.
```

On a triple overlap,

```text
R_02 = R_12 R_01
```

implies exactly

```text
R'_02 = R'_12 R'_01.
```

Thus a local shift zero-cochain acts by a coboundary change of the reference transitions while
leaving every complete coframe and physical transition unchanged. The production witness uses
three unequal shifts `(7,11,13)`; the independent implementation uses `(5,8,11)`. In both cases the
full three-chart cocycle survives exactly.

The correct global object is consequently a groupoid/orbit of factorized presentations on the
supplied smooth cover. The existence of the cocycle organizes the local non-identifiability; it
does not select one representative.

## 3. Fixed reference transitions are an additional premise

If `R_ij` is separately fixed rather than allowed to transform with the presentation, the surviving
shifts obey

```text
K_j = R_ij K_i R_ij^-1.
```

This is a stabilizer/parallel-section condition for the supplied reference transition system. For
an oriented reciprocal transition it gives equal endpoint shifts. For a reversal transition it
gives inverse multiplicative shifts, equivalently opposite additive shifts. A more restrictive
supplied holonomy could reduce the stabilizer further.

The calculation is exact but its authority is conditional: the current foundation does not own one
fixed reference transition system as physical data. Even in the oriented connected control, equal
chart values leave an arbitrary function over the base, not one unique number or field.

## 4. Global-scalar descent does not select a scalar

For a connected three-chart cover, the overlap incidence matrix has rank two and nullity one at
each base point. Requiring local shifts to agree on overlaps therefore turns `{chi_i}` into one
global function `chi(x)`.

Two exact base-point samples `(7,7,7)` and `(11,11,11)` both descend, showing that scalar descent
does not force the function to be constant over spacetime. If `phi` is independently declared to
be a scalar, the factorization freedom is reduced from arbitrary chart functions to arbitrary
global functions. The scalar architecture remains open and the representative remains unselected.

The observed anchor `c_E` fixes the normalization/units of the founded comparison. It does not by
itself choose the reference zero or a global representative of this factorization orbit.

## 5. Affine and reversal-twisted descent

Allow local representatives to obey

```text
phi_j = epsilon_ij phi_i + a_ij,     epsilon_ij in {+1,-1}.
```

The triple-overlap equations are

```text
epsilon_02 = epsilon_12 epsilon_01,
a_02       = epsilon_12 a_01 + a_12.
```

Under `phi_i'=phi_i+chi_i`,

```text
a'_ij = a_ij + chi_j - epsilon_ij chi_i.
```

Substitution proves the same cocycle equation for `a'`. Exact oriented and two-reversal witnesses
are saved. The `Z2` reversal parity survives. Around an oriented loop (`epsilon=+1`), the affine
translation/period is invariant under a local shift at the base. Around a reversal loop
(`epsilon=-1`), its translation changes by `2 chi_base`, while reversal parity remains.

Hence cocycle-class or period data can be genuine global invariants without choosing local values
of `phi`. The physical lift of a reversal-twisted reciprocal bundle remains conditional on the
complete metric, screen/angular, seam, and boundary data.

## 6. Query equivariance transports every supplied depth

For a supplied observer/ruler plane,

```text
D_01(z_2)D_01(z_1)=D_01(z_1 z_2).
```

A query reset `R` gives

```text
D_02(z)=R D_01(z) R^-1
```

and preserves the same character law for every `z`. The reset changes the actual plane action, so
the object is query-equivariant rather than basic on spacetime. Nothing in this identity assigns a
value of `z` to the query.

## 7. Pair composition and path periods

For four observers and six oriented pair depths, the incidence matrix `B` has rank three. The four
triangle residual rows `C` have rank three and obey

```text
C B = 0.
```

Thus every endpoint potential and every shifted endpoint potential composes. A free non-coboundary
edge cochain fails, proving that the test is nonvacuous on free edge data.

If the pair depths are independently fixed as physical data, preserving them requires

```text
B chi=0,
```

which leaves one common constant on a connected observer graph. That is a useful conditional
ownership result, but the metric-native physical depth assignment is presently `OPEN`.

A loop period annihilates `B chi`, so periods are invariant under endpoint shifts. Concatenation
does not set those periods to zero. Requiring trivial full-loop return is an extra, not-founded
premise; moreover, endpoint potentials already have zero periods for every potential, so that
premise would not select a local profile.

## 8. Finite-cell seam split

A physical seam acts on complete coframes. Under independent endpoint factorization shifts, its
reference representative changes as

```text
R'_seam = K_+^-1 R_seam K_-.
```

Therefore arbitrary endpoint shifts preserve the same physical complete-coframe seam when the
reference presentation transforms honestly. Holding `R_seam` fixed instead imposes the stabilizer
relations of Section 3. The existing finite-cell completion graphs and jet-matching rules restrict
physical endpoint/joint data, but do not by themselves declare a reference seam representative to
be physical.

Global completion data may therefore carry real invariants while factorization ownership remains
open. A selected seam, trivial return, or boundary polarization cannot be inserted to close it.

## 9. Branch-derived ownership

If a regular metric branch independently supplies an intrinsic selector and a rule

```text
phi = Phi[g,query/path data],
```

then changing `phi` alone would violate that rule; ownership would be branch-local and its variation
would follow the parent fields. Existing selector constructions are conditional on regular strata
and fail or become set-valued at collisions, zero/null, causal-change, or rank-changing loci. This
route is retained as conditional, not promoted to a universal section.

## 10. Bounded conclusion

On the supplied smooth fixed-rank cover, the current derived overlap, query, composition, and
finite-cell structures do not select a physical founded-depth representative. They preserve an
exact groupoid of factorized presentations. Global scalar descent, affine cocycles, reversal parity,
and loop periods can reduce or classify the orbit without choosing a section.

Fixed reference transitions, independently physical pair depths, or a regular branch selector can
reduce the freedom, but each requires ownership data not supplied by the founded comparison law.

```text
DERIVED_GLOBAL_FACTORIZATION_GROUPOID_FREEDOM_ON_THE_SUPPLIED_SMOOTH_COVER
DERIVED_COCYCLE_CLASS_AND_PERIOD_INVARIANTS_DO_NOT_SELECT_A_SECTION
CONDITIONAL_REDUCTIONS_REQUIRE_UNOWNED_REFERENCE_DEPTH_OR_BRANCH_SECTION_DATA
NO_GLOBAL_PHI_OWNERSHIP_SELECTION
```

This terminates the present overlap/cocycle route. The smallest missing object is a native,
equivariant ownership morphism relating complete geometry and observer/path query data to a depth
section or equivalence class. Its home may be the query bundle, spacetime, a realized field, or a
stratified branch construction; the current premises do not choose among them.
