# Exact derivation: intrinsic clock/transverse solder

## 1. Three bundles that must not be conflated

Given a Lorentzian metric, a typed observer `u`, and a supplied path
direction, the tangent space can be reduced locally to a longitudinal
two-plane and a two-dimensional screen. This introduces three distinct
objects:

1. the founding reciprocal rank-two channel `E_rec`;
2. spacetime two-forms `Lambda2(TM)`;
3. transverse Jacobi phase space
   `V_J=S_screen direct_sum S_screen`.

The first-order transverse state contains screen separation and its path
derivative. It is not a spacetime area bivector.

## 2. The real metric-derived area duality

On an oriented Lorentzian four-manifold, choose an oriented orthonormal
`2+2` split only for displaying the tensorial result:

`B=e0 wedge e1`,

`A=e2 wedge e3`.

The Hodge operation gives, up to the frozen orientation convention,

`star B=A`, `star A=-B`,

and `star^2=-I` on real two-forms. Levi-Civita transport preserves the
Hodge operation:

`nabla star=0`.

This is an exact, frame-independent relation between the longitudinal and
screen **area planes**, conditional on the observer/path split and
orientation.

It does not retain reciprocal depth. A reciprocal two-channel boost has

`det S(delta)=1`,

so its longitudinal area bivector is unchanged for every `delta`.
Likewise an oriented screen rotation has determinant one. Hodge duality
therefore relates the invariant plane areas while erasing the nontrivial
clock dilation parameter.

It also has the wrong target type: `star B` is a spacetime two-form,
whereas the full Jacobi propagator acts on
`S_screen direct sum S_screen`.

Status:

`ORIENTED_NORMAL_SCREEN_AREA_HODGE_DUALITY_DERIVED_GIVEN_TYPED_SPLIT`;

`HODGE_AREA_DUALITY_AS_CLOCK_JACOBI_SOLDER_FALSE_TYPE`.

## 3. Endpoint screen gauge forbids a linear solder without a reduction

The reciprocal clock/ruler channel is a scalar under an independent change
of endpoint screen basis. The screen vector representation transforms under
`SO(2)`, and Jacobi phase space carries two copies of that representation.

Let

`J=[[0,-1],[1,0]]`

be the infinitesimal screen rotation. On phase space the generator is

`J_4=diag(J,J)`.

A screen-gauge-equivariant linear map `H:E_rec->V_J` would have to obey

`J_4 H=0`.

But `J_4` is invertible, so `H=0`. The contragredient calculation gives the
same result for a bilinear clock/screen cross block.

This obstruction disappears only after another object selects a screen
line or supplies a matched nontrivial angular representation. That is
exactly the conditional premise in the prior reciprocal-angular
intertwiner theorem; the complete metric has not selected it.

## 4. Exact criterion for an invariant transverse phase mode

Let `P` be a rank-one projector on the screen and lift it to Jacobi phase
space:

`P_J=diag(P,P)`.

In a parallel screen frame the Jacobi generator is

`A_J=[[0,I],[-T,0]]`,

where `T` is the symmetric screen tidal operator. Direct block algebra gives

`[A_J,P_J]=[[0,0],[-[T,P],0]]`.

In a general screen frame the corresponding covariant condition is

`D P/dlambda=0`.

Therefore the rank-two phase subbundle

`image(P) direct sum image(P)`

is preserved exactly if and only if:

1. the screen line is parallel; and
2. the tidal operator preserves it, `[T,P]=0`.

A distinct tidal eigenvalue may identify an instantaneous unoriented line,
but it does not make that line parallel along the complete path. If `T` is
isotropic, every line is an eigenline and none is selected.

## 5. Exact pointwise generator-matching condition

After a parallel tidal-invariant screen line has been supplied, one scalar
Jacobi mode has generator

`A_J=[[0,1],[-K,0]]`.

The reciprocal clock generator, with the same path parameter, is

`A_R=diag(-a,a)`,

where `a=d(delta)/dlambda`.

Their characteristic polynomials are

`lambda^2+K`

and

`lambda^2-a^2`.

For `a!=0`, a real pointwise intertwiner exists exactly when

`K=-a^2`.

Sufficiency is constructive. For `K=-a^2`,

`H=[[1,1],[-a,a]]`

satisfies

`A_J H=H A_R`

and has determinant `2a`.

Thus a nontrivial matched transverse mode must have negative curvature and
a magnitude fixed by the clock-dilation rate. This is a characterized
condition, not a UDT equation or selected branch.

When `a=K=0`, the natural Jacobi generator remains the nonzero nilpotent
free-drift matrix, while the clock generator is zero. They are not similar.

The condition is pointwise in the natural parallel screen frame. An
arbitrary path-dependent `H(lambda)` can always be manufactured by solving

`H'=A_J H-H A_R`

after both transports and initial `H` are supplied. That construction is
not an intrinsic metric-selected solder and is not excluded by the
pointwise result.

## 6. B19 and WR-L

### B19 round branch

The complete ultrastatic round branch has

`a=0`, `K=1/b^2>0`.

Its clock block is identity, while the scalar screen propagator is

`[[cos(L/b), b sin(L/b)],`

` [-sin(L/b)/b, cos(L/b)]]`.

At `L=pi b/2` this is not identity. B19 therefore supplies complete
transverse path transport and the area Hodge relation, but no nontrivial
clock/transverse solder.

### WR-L local radial branch

In proper distance `D`,

`N=1-D/(2X)`,

`R=D-D^2/(4X)`,

`K=1/(2XR)>0`,

`a=-d(log N)/dD=1/(2XN)>0`.

Therefore

`K+a^2>0`,

so the natural scalar Jacobi and reciprocal generators are not pointwise
real-similar.

There is nevertheless an exact branch-specific scalar relation. Since the
centered clock ratio is `Q=1/N`,

`R=X(1-N^2)=X(1-Q^-2)`.

This is a genuine local clock/area profile identity. It is not an
equivariant map between the clock channel and the complete Jacobi
phase-space transport, and it does not repair WR-L's missing global
all-observer recentering.

## 7. Full coframe connection and the `dphi` 3+3 reduction

On nonnull `dphi`, the registered field-assisted two-form split has two
real rank-three sectors. In an adapted basis the induced Lorentz connection
has the form

`A_Lambda2=[[R,B],[-B,R]]`.

It commutes with Hodge, but the off-stabilizer block `B` mixes the two
rank-three sectors. For the exact one-direction witness the mixing map has
rank four. The split is Levi-Civita parallel if and only if `B=0`.

Kato transport can preserve the moving split on a smooth fixed-rank
nonnull region, but it does not select a physical connection or a rank-two
screen phase subbundle. At null `dphi`, the induced two-form map is rank-two
nilpotent rather than a semisimple `3+3`; at `dphi=0`, no line is present.

Consequently the `dphi` result remains a genuine reciprocal-bearing
two-form reduction, not the missing clock-to-Jacobi solder.

## 8. Finite-cell and branch result

Every one of the twelve completion families still has:

- no complete on-shell `(g,phi)` witness;
- conditional or obstructed global `dphi` reduction;
- orientation, cap, singularity, monodromy, or interface qualifications;
- no selected matched angular representation; and
- no intrinsic clock/Jacobi solder.

All twenty-eight equation families remain retained and unpromoted.

The prior conditional angular theorem remains exact: a supplied
two-dimensional angular generator supports a full-rank reciprocal
intertwiner precisely when it is similar to the reciprocal generator, with
a matched mirror reducing the family to one relative scale. No registered
complete branch supplies those inputs.

## 9. Final status

- Normal/screen area Hodge duality:
  `DERIVED_GIVEN_TYPED_2PLUS2_SPLIT`.
- Screen-gauge-equivariant linear clock-to-phase map:
  `OBSTRUCTED_WITHOUT_SCREEN_REDUCTION`.
- Parallel tidal-invariant phase-line criterion:
  `DERIVED_IFF`.
- Pointwise scalar-generator match:
  `UNIQUE_CONDITION_CHARACTERIZED`, `K=-a^2` for `a!=0`.
- WR-L centered scalar profile relation:
  `DERIVED_LOCAL`.
- WR-L pointwise natural-frame generator similarity:
  `NO_POINTWISE_SIMILARITY_IN_EXACT_LOCAL_RADIAL_CONTROL`.
- Intrinsic irreducible clock/transverse solder:
  `OPEN_NO_REGISTERED_WITNESS`.
- Reducible same-path direct sum:
  `DERIVED_REMAINS_STRONGEST_CURRENT_ASSEMBLY`.

No action, source, carrier, boundary law, density, bootstrap closure,
physical `X_max`, signal ontology, or observational claim was used or
derived.
