# Exact derivation — intrinsic two-form distribution and complete-cell degeneration

## Scope

This is an exact CPU, stationary, off-shell audit of the same 18-member `R x S3` ensemble frozen by
the immediate parent. No metric profile, action, source, carrier, boundary, density, or physical
branch was added. The result applies intrinsically only to the 15 branches on which the parent
certified a unique clock line, nonzero twist ruler, and pair/screen projector.

The only nonzero intrinsic two-form tested is

```text
W=dPhi_contact wedge dSigma_contact=(du wedge dV)/(2 u V).
```

For the six independent-area intrinsic branches, `V=1+V0/10`. The nine intrinsic controls with
constant/slaved depth-area data remain identically zero. C14 and C15 remain configuration-only
controls because their intrinsic projector gate fails; C18 remains metric-degenerate.

## 1. Exact global Maurer-Cartan dual frame

For the frozen unit quaternion `(q0,q1,q2,q3)`, the three vector fields dual to
`(sigma1,sigma2,sigma3)` are

```text
X1=(-q1, q0, q3,-q2),
X2=(-q2,-q3, q0, q1),
X3=(-q3, q2,-q1, q0).
```

Each is tangent to `sum qi^2=1`, and exact contraction with the registered coframe gives
`sigma_i(X_j)=delta_ij` on the sphere. For

```text
u =3+q0^2+2 q1^2+4 q2^2+8 q3^2,
V0=  q0^2+3 q1^2+7 q2^2+9 q3^2,
```

the exact derivatives are

```text
X1 u =2(q0 q1-4 q2 q3),       X1 V0= 4(q0 q1-q2 q3),
X2 u =6(q0 q2+2 q1 q3),       X2 V0=12(q0 q2+q1 q3),
X3 u =2(7 q0 q3-2 q1 q2),     X3 V0= 8(2 q0 q3-q1 q2).
```

Writing

```text
W=c12 sigma1^sigma2+c13 sigma1^sigma3+c23 sigma2^sigma3,
```

the common positive normalization is `1/(20 u V)`, while the raw numerators factor as

```text
c12_raw=-24 q3 f12,  f12=q0 q1^2+3 q0 q2^2+2 q1 q2 q3,
c13_raw=-24 q3 f13,  f13=q0^2 q1+3 q0 q2 q3-2 q1 q2^2,
c23_raw=-24 q3 f23,  f23=3 q0^2 q2-q0 q1 q3+2 q1^2 q2.
```

No denominator vanishes: `u>=4` and `V>0` on the complete cell.

## 2. The full zero locus is exact

There is a short support proof, independent of plotting. The two diagonal quadratic profiles have
coefficient pairs

```text
(A_i,B_i)=(1,1),(2,3),(4,7),(8,9).
```

Restricted gradients on the sphere are linearly dependent exactly when all coefficient pairs in
the nonzero coordinate support lie on one affine line. The four triple determinants are

```text
det(012)=0, det(013)=-6, det(023)=-18, det(123)=-12.
```

Thus every point with `q3=0` is zero. If `q3!=0`, at most one of `q0,q1,q2` may also be nonzero.
Consequently the exhaustive zero set is

```text
Z(W)=E union C03 union C13 union C23,

E:   q3=0                         (an equatorial S2),
C03: q1=q2=0,
C13: q0=q2=0,
C23: q0=q1=0.                    (three great circles)
```

The equator separates `S3` into `q3>0` and `q3<0`. In each open hemisphere the remaining zero set
is a finite one-dimensional embedded graph. Such a codimension-two graph does not separate a
connected three-manifold (equivalently, use general-position path perturbation or Alexander
duality after compactification). Therefore `S3\Z(W)` has exactly two connected components. This is
an exact topological conclusion, not a numerical component count.

## 3. Hodge line, kernel, and indexed convention

Choose an oriented orthonormal coframe with `theta1` on the metric-derived ruler and
`theta2,theta3` on the screen. Write

```text
W=A theta1^theta2+B theta1^theta3+C theta2^theta3.
```

In signature `(-+++)`, with `T_flat=-theta0`, direct Hodge calculation gives

```text
N_flat=star(T_flat wedge W)=C theta1-B theta2+A theta3.
```

Therefore

```text
g(N,N)=A^2+B^2+C^2,
i_T W=0,
i_N W=0.
```

For `W!=0`, the antisymmetric matrix has rank two and

```text
ker(W)=span(T,N),  dim ker(W)=2.
```

At `W=0`, its rank is zero and its kernel is the entire four-dimensional tangent space; there is no
unique residual line.

For the registered general screen,

```text
F=u^lambda V,
theta2=sqrt(F)(r sigma1+b sigma2),
theta3=sqrt(F) r^(-1) sigma2,
theta1=sqrt(u) sigma3.
```

If `k=1/(20 u V)`, exact conversion gives

```text
A=-k c13_raw/(sqrt(F) r sqrt(u)),
B= k(b c13_raw-r c23_raw)/(sqrt(F) sqrt(u)),
C= k c12_raw/F.
```

Since `F,r,u` are positive, this conversion is smooth and invertible. It proves, rather than
guesses, the type convention:

```text
RULER_ALIGNED    iff c13=c23=0 and c12!=0,
SCREEN_CONTAINED iff c12=0 and (c13,c23)!=(0,0),
GENERIC_MIXED    iff c12!=0 and (c13,c23)!=(0,0).
```

Screen-frame rotations, orientation reversal, and representative signs change components or the
sign of `N`, but not the line, projector, or these three coordinate-free types.

## 4. Exact line-type atlas

On `q3!=0`, set `q3=1` projectively. A Groebner reduction gives

```text
remainder(f12^2 modulo <f13,f23>)=0.
```

Hence `f13=f23=0` forces `f12=0`; the nonzero ruler-aligned locus is empty. This is not a failure to
find a sample.

The screen-contained locus is nonempty. The exact projective representative

```text
[q0:q1:q2:q3]=[1/2:1:-1/3:1]
```

has `(f12,f13,f23)=(0,-17/36,-17/12)`. The generic-mixed locus is also nonempty; the registered
exact representative `[1/5:1/7:1/11:1]` has all three factors nonzero. Thus every one of the six
intrinsic independent-area candidates realizes two nonzero types on different loci:

```text
SCREEN_CONTAINED and GENERIC_MIXED,
```

and none realizes `RULER_ALIGNED`.

The screen shears and `lambda` change the metric components and actual direction within the screen,
but not the zero/type partition. C16/C17's contact-sign strata likewise do not alter this algebraic
partition.

## 5. Projective continuation across the zeros

The raw coefficient vector has the common factor `q3`. At a point of the equator where
`(f12,f13,f23)!=0`, canceling that common scalar gives a unique limit of the sign-independent line.
The only equatorial points where the residual vector also vanishes are the six `q0/q1/q2` axis
points. Therefore the line extends uniquely through

```text
E minus (C03 union C13 union C23).
```

It does not extend through any of the three great circles. At a generic point on each circle, the
exact transverse leading maps have determinants

```text
C03:  3 q0^2(q0^2+q3^2),
C13:  2 q1^2(q1^2+q3^2),
C23: -6 q2^2(q2^2+q3^2).
```

They have rank two whenever the indicated non-`q3` coordinate is nonzero, so two transverse paths
give different projective limits. This includes the six equatorial intersections. At the shared
`q3=+/-1` poles, two explicit tangent paths give leading factor directions `[1:0:0]` and
`[0:1:0]`; the limit is again path-dependent.

The metric Hodge map is smooth and invertible on every intrinsic nondegenerate candidate, so it
cannot turn these distinct projective limits into one. The exact maximal continuation statement is:

```text
the line extends across the generic equatorial sheet,
but a complete-cell line is obstructed on C03 union C13 union C23.
```

## 6. Candidate census and limits

The exact candidate census is

```text
9  ZERO intrinsic controls,
6  MULTIPLE_NONZERO_TYPES_ON_DIFFERENT_LOCI,
2  PROJECTOR_BLOCKED configuration controls (C14,C15),
1  METRIC_DEGENERATE control (C18).
```

All seven registered stereographic checks agree with the global algebra: p1-p6 are generic-mixed;
p7 lies on the extendable part of the equator. These points are checks only and were not used to
establish exhaustiveness.

## Maximum conclusion

Within the frozen stationary ensemble, the intrinsic depth/area two-form supplies a spacelike
kernel line on its nonzero locus. The line is screen-contained on one exact locus, generic-mixed on
another, never ruler-aligned, and has an exact singular great-circle obstruction to global
continuation.

This is a bounded metric-distribution/degeneration atlas. It does not select a carrier or section,
derive Hopf charge, choose a metric branch, put the configuration on shell, or supply dynamics,
action, source, boundary, density/bootstrap value, `X_max`, matter, mass, stability, or
phenomenology.
