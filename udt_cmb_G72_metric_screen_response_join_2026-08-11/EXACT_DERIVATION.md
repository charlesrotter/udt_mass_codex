# G72 exact derivation — metric screen-response join

Date: 2026-08-11

Primary landing:

`METRIC_OWNS_SOURCE_FREE_SCREEN_RESPONSE__PHYSICAL_OBSERVABLE_OPEN`

This is a conditional geometric response theorem on one supplied regular observer-sky query. It is
not a physical CMB query, source, spectrum, polarization law, or prediction.

## 1. Correctly typed screen data

Let `S_s` and `S_o` be oriented positive-definite two-dimensional screen spaces at the source and
observer ends of one supplied path/query. The complete metric conditionally owns:

```text
D:S_s -> S_o       finite Jacobi/image response,
U:S_s -> S_o       metric screen isometry along the same supplied path.
```

Strictly, a null Jacobi map sends an initial transverse derivative/angle into endpoint separation.
The comparison with `U` is therefore well typed only after the query supplies the source-screen
metric, affine calibration, and identification used in the Jacobi initial condition. G68 does this
by setting `P_B(0)=E_B` in its registered affine parameter. A positive rescaling of that affine
parameter changes the common response scale but not shear ratio or polar angle.

The result does not authorize combining a Jacobi map from one query with normal transport from a
different pair immersion or path.

## 2. Endpoint gauges and why one open transport has no angle

In oriented orthonormal endpoint frames, let independent frame changes be

```text
R_s in SO(2),  R_o in SO(2).
```

Then

```text
D -> D' = R_o D R_s^-1,
U -> U' = R_o U R_s^-1.                                      (1)
```

The displayed rotation angle of `U` changes by the independent source/observer frame angles. The
left-right action is transitive on `SO(2)`, so no order-zero real angular scalar belongs to `U`
alone on one unframed open path. This reproduces the banked open-path gauge result.

## 3. The relative response is a new, correctly typed object

Because `D` and `U` share both endpoints, define

```text
M = U^-1 D:S_s -> S_s.                                      (2)
```

Equation (1) gives

```text
M -> M' = R_s M R_s^-1.                                    (3)
```

The observer-end gauge has cancelled. The remaining source gauge acts by conjugation, not by
independent left and right multiplication. That change of type is what permits relative angular
information to survive.

This is not a preferred path or physical query selector. It is the response assigned after the
path/query has already been supplied.

## 4. Exact polar response and its complete generic invariant set

On the oriented regular stratum `det(M)>0`, write

```text
M = R(theta) P,
P=(M^T M)^(1/2)>0,
R(theta) in SO(2).                                           (4)
```

For

```text
M=[[a,b],[c,d]],
q=a+d,
p=c-b,
z=sqrt(q^2+p^2),
```

the polar rotation is exactly

```text
R(theta)=(1/z)[[q,-p],[p,q]],
theta=atan2(c-b,a+d).                                       (5)
```

If `det(M)>0`, `q` and `p` cannot vanish together. Direct symbolic calculation verifies

```text
R^T R=I,  det(R)=1,  P=R^T M=P^T,  RP=M.                   (6)
```

Diagonalize the positive factor as

```text
P=R(alpha) diag(ell exp(chi),ell exp(-chi)) R(alpha)^-1,
ell>0, chi>=0.                                              (7)
```

Under source conjugation, `alpha` changes while rotations commute in two dimensions, so

```text
ell=sqrt(det M),
chi=(1/2)log(s_max/s_min),
theta modulo 2 pi                                           (8)
```

remain invariant. Conversely every positive-determinant `M` is conjugate to the canonical form

```text
R(theta) diag(ell exp(chi),ell exp(-chi)).                  (9)
```

Thus `(ell,chi,theta)` is a complete generic invariant set for the oriented order-zero pair
`(D,U)` under independent endpoint frame gauges. The count agrees with the quotient dimension:
`D` contributes four parameters, `U` one, and two endpoint rotations remove two, leaving three.

At `chi=0` the shear axis is undefined but the invariants remain regular. If reflections are
allowed, conjugation sends `theta -> -theta`; only its reflection orbit, for example `cos(theta)`,
is unoriented scalar data.

## 5. Tensor response versus a physical observable

The positive factor also supplies a covariant source-side shear tensor

```text
Q_s = [log P]_TF.                                            (10)
```

Its eigenvalues are `(+chi,-chi)`. It transforms by source conjugation. An equivalent
observer-side tensor can be formed from the positive factor of `D D^T`; its components rotate with
the observer's chosen sky frame. These are genuine source-free geometric response tensors.

They are not automatically temperature or polarization. A scalar source field is locally remapped
by the observer-sky relation, but

```text
zero -> zero,
constant -> constant.                                       (11)
```

Geometry can relocate, focus, or shear structure that exists; a pure pullback cannot populate a
nonconstant scalar sky from absent or constant source data. Likewise any homogeneous tensor
transport sends a zero orientation tensor to zero. To obtain physical TE/EE/BB, one must still
specify which orientation-sensitive source/state exists and which tensor representation and
measurement contraction define the observation. The metric can evaluate a declared tensor type;
it does not thereby derive the source or choose the physical detector law.

The absolute response scale `ell` is also dimensionful for the G68 Jacobi convention (initial
angle/derivative to endpoint separation). Its logarithm needs an independently declared reference
length. `c_E` calibrates clock length but does not by itself select the global endpoint or universe
size. A later global completion or `X_max` construction could supply that reference; it is not
owned here. The dimensionless shear `chi` and relative angle `theta` do not need that common-scale
reference.

## 6. G68 control replay

G68 writes `D` in its registered parallel-transported endpoint screen, so `U=I` in that
representation. Re-evaluating all `21` frozen maps gives

```text
rows                                      21
max |relative polar angle|                3.549305994648684e-24
max |new angle - saved polar rotation|    1.435469059354858e-20
max shear magnitude                       0.0023238059699749714.
```

Thus the bounded stationary/equatorial controls carry nonzero source-free area and shear response,
but no resolved image rotation. Their endpoint azimuthal coordinate carry `psi` reaches order
`10^-1`; it is not the polar rotation of the Jacobi response. Therefore G72 does not retroactively
turn the `psi` channel used in G69/G70 into a physical polarization or scalar-TT observable.

General angular, non-equatorial, time-live, or globally completed queries may produce nonzero
`theta`; that is open and must be calculated on those queries rather than inferred from `psi`.

## 7. Why the endpoint Jacobi block is not a network functor

The response `D` is one block of the full Jacobi transfer state. Even flat one-dimensional free
propagation supplies the exact transfer

```text
T(L)=[[1,L],[0,1]].                                          (12)
```

For `L1=2`, `L2=3`,

```text
T(3)T(2)=T(5),
D_total=5,
D_2 D_1=6.                                                   (13)
```

The full transfer matrices compose; their upper-right endpoint blocks do not multiply. G72's
response is therefore an endpoint evaluation on one supplied query, not a new groupoid arrow law.

## 8. Independent verification

The production route uses the closed two-dimensional polar formula and `512` random
`SO(2)xSO(2)` endpoint-gauge trials. Maximum errors are

```text
M gauge covariance          1.175e-15
common scale                6.661e-16
shear                       6.217e-15
relative angle              4.441e-16
reflection angle            0
source congruence replay    1.189e-14.
```

The independent route constructs positive-determinant maps from unrelated polar factors and uses
SVD rather than equation (5). Across `1000` trials its maximum scale, shear, angle, and reflection
errors are respectively

```text
4.441e-15, 5.551e-15, 6.661e-16, 0.
```

Every independently gauged raw open-path `U` angle changed, while every relative angle remained
fixed. Both routes verify that zero source tensors remain zero. The exact rational transfer witness
reproduces `D_total=5 != 6=D_2 D_1`.

## 9. Domain boundaries

- `det(D)=0`: Jacobi caustic; polar response is singular and no extension is asserted.
- `det(D)<0`: parity-reversing branch; an `O(2)` polar factor exists but the oriented angle needs a
  separate parity label.
- missing screen orientation: only the reflection quotient of `theta` survives.
- missing common source-screen/affine calibration: `U^-1 D` is not yet physically typed.
- different paths: each path/query has its own response; no selector is supplied.
- cut/focal locus: return the branch-labelled response family, not one preferred member.
- absent global scale: keep `ell` dimensionful; do not manufacture a logarithmic scale.

## 10. Exact ownership landing

`DERIVED_CONDITIONAL_ON_QUERY`:

- the relative response endomorphism `M=U^-1D`;
- common response density/scale as a dimensionful geometric output;
- dimensionless shear magnitude and covariant shear tensor;
- relative polar rotation on an oriented regular query.

`OPEN_NO_OWNER`:

- the physical CMB observer query, endpoint, profile, and global scale;
- source population, covariance, normalization, or polarization state;
- the rule turning the geometric response into physical TT/TE/EE/BB;
- a nonzero relative rotation on a complete physical CMB branch.

The result strengthens the observer-effect route in one precise sense: the complete geometry can
own a three-channel local screen response after a query is supplied. It simultaneously preserves
G71's boundary: response is not source creation, physical query selection, or observation.
