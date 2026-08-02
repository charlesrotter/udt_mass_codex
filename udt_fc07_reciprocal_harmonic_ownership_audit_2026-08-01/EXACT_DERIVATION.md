# Exact derivation — FC07 reciprocal/harmonic ownership

Date: 2026-08-01  
Preregistration: `37df6a1`  
Source freeze: `08823ce`

## 1. Complete bounded coframe

On a universal-cover chart `(t,s,y1,y2)`, retain the founded reciprocal pair and a bounded
descending lower-triangular mixing class

```text
theta0 = p(s) dt,                         p=c_E exp(-phi)>0,
theta1 = a(s) ds,                         a=L exp(+phi)>0,
thetaA = u_A(s)dt+b_A(s)ds+P_Aa(s)dy^a,
g      = -theta0^2+theta1^2+theta2^2+theta3^2.
```

`P` is an oriented invertible screen coframe. Write

```text
h=P^T P,       D=det(P)=sqrt(det(h))>0,       v=P^-1 b.
```

All functions are arbitrary smooth descending functions. The function-level mixing family is a
`CHOSE` bounded generalization containing the registered pointwise E02 members; it is not a
derived field promotion. This statement is conditional on a supplied global descent law and does
not solve the still-open J07/J11 mixing cocycle. See `SCOPE_CORRECTION.md`.

The full determinant is

```text
det(g)=-(p a D)^2.
```

On a constant-time spatial completion,

```text
q = (a ds)^2+(b ds+P dy)^T(b ds+P dy)
  = [[a^2+b^T b, b^T P],
     [P^T b,     P^T P]],

det(q)=a^2 D^2.
```

The inverse is

```text
q^-1 = [[a^-2,              -a^-2 v^T],
        [-a^-2 v, h^-1+a^-2 v v^T]].
```

Thus the metric dual of the founded ruler is

```text
E1=(theta1)^sharp=(1/a)[partial_s-v^a partial_ya].
```

The clock-screen mixing `u` does not enter `E1`; the spatial mixing `b` changes its coordinate
components but not the founded coframe line.

## 2. Complete harmonic equation in the base class

For an invariant base-class one-form

```text
beta=f(s) ds,
```

closedness is automatic. Its co-closure is

```text
delta beta = -(1/(aD)) d/ds[D f/a].
```

The apparent screen components of `q^-1 beta` contribute no divergence because all registered
coefficients are fiber-independent. Therefore

```text
beta harmonic  iff  D f/a = constant.
```

Unit period around the mapping-torus base fixes

```text
I = integral_cell a(s)/D(s) ds
  = integral_cell L exp(phi(s))/sqrt(det(h(s))) ds,

alpha = [a/(I D)] ds
      = theta1/[I sqrt(det(h))].
```

For every smooth compact nondegenerate member, `I` is finite and positive.

## 3. Why this is the unique harmonic line

For a mapping torus,

```text
b1=1+dim ker(M^T-I).
```

For minus-identity, order-four, order-six, and hyperbolic monodromy,

```text
det(M)=1,      det(M^T-I) != 0,      b1=1.
```

An invariant closed one-form can contain a constant fiber covector `w`, but descent requires

```text
M^T w=w.
```

The zero kernel forces `w=0`. The displayed `alpha` is a nonzero harmonic representative of the
base class, and `b1=1` makes its line the complete metric's unique harmonic one-form line.
Unimodularity also gives `det(M^T h M)=det(h)`, so `D` and `alpha` descend.

## 4. Exact ownership theorem

Because `alpha=theta1/(I D)`, their covector lines coincide. More strongly,

```text
|theta1|^2=1,                    |alpha|^2=1/(I^2 D^2),

P_alpha=(alpha^sharp tensor alpha)/|alpha|^2
       =E1 tensor theta1
       =P_theta1.
```

This equality holds for arbitrary smooth finite descending `phi`, arbitrary full positive screen
`P`, and every descending `u,b` in the bounded lower-triangular class containing the registered
E02 members. The mixing functions cancel exactly. They are not required to vanish.

This establishes `LINE_OWNERSHIP` and `RESCALED_FORM_OWNERSHIP` throughout the bounded
nondegenerate family.

## 5. The founded ruler is not generically harmonic

The unrescaled ruler is closed:

```text
d theta1=d[a(s)ds]=0.
```

Its co-closure is

```text
delta theta1 = -D'/(aD).
```

Therefore

```text
theta1 itself is harmonic  iff  d/ds sqrt(det(h))=0.
```

Variable `phi` cancels from this condition. The condition permits changing area-preserving shear;
it does not require a constant screen metric.

For the registered symmetric interpolation `h=h0+chi Delta`, equal endpoint determinants imply

```text
det(h)=det(h0)+det(Delta)(chi^2-chi).
```

Every nonconstant unimodular interpolation has `det(Delta)<0`, so its screen area varies in the
interior. Its reciprocal **line** remains harmonic-owned, but the unrescaled `theta1` is not itself
harmonic. Constant-screen controls satisfy the stronger condition. Other descending
area-preserving screen paths remain mathematical controls outside that particular interpolation.

## 6. What the angular sector does

The angular/screen sector does not rotate the unique harmonic line away from the founded ruler.
Instead it modulates the harmonic amplitude through

```text
alpha/theta1 = 1/[I D(s)],
I = integral_cell L exp(phi)/D ds.
```

The local coefficient uses the local angular area `D(s)` and a normalization depending on the
complete cell's `phi` and angular-area profiles. This is an exact phi–angular global-to-local
compatibility readout.

It is not yet a return equation. Unit-period normalization chooses the representative of a known
cohomology class; it does not restrict `phi`, `h`, `u`, or `b`.

## 7. Background-window and density rulings

Line/projector ownership is an identity on the entire open domain

```text
a>0, D>0, smooth compact descent, b1=1.
```

No curvature scalar, curvature inequality, or finite parameter interval enters it. Loss of
`a>0`, `D>0`, compactness, or finite `I` is a coframe/Hodge domain boundary, not a derived
bootstrap window. The area-constant condition for the unrescaled ruler is an equality stratum,
not a finite curvature range, and no active premise requires it.

This does **not** rule out a limited background range for matter. It shows only that the present
kinematic ownership machinery is already available throughout the bounded nondegenerate family.
A matter-supporting range would have to enter through a later native admissibility/equation and a
same-solution return law.

No native map relates total proper density or energy to these curvature/completion data here.
Consequently no density value or density window is computed.

## 8. Scope boundary

Not covered:

- upper-right screen-to-pair extensions;
- non-torus-invariant or time-live fields;
- construction/selection of the J07/J11 mixing descent cocycle;
- a native equation requiring the harmonic normalization;
- density–curvature/source closure;
- physical completion selection, `X_max`, action, carrier, matter, mass, or stability.
