# Exact derivation and conventions

## 1. Frozen coframe

The audit changes no geometry:

```text
theta0=e^-phi(dt+a sigma3)
theta1=e^+phi sigma3
theta2=e^(lambda phi) sigma1
theta3=e^(lambda phi) sigma2
g=-(theta0)^2+(theta1)^2+(theta2)^2+(theta3)^2.
```

In its orthonormal frame, define

```text
X_lambda=diag(-1,+1,lambda,lambda).
```

This is the parent reciprocal clock/ruler grading with an isotropic screen weight.  It is an
endomorphism diagnostic, not an action, matter carrier, or new field.

## 2. Covariant derivative

The matrix entries of `X_lambda` are constant in the adapted frame.  Therefore

```text
(nabla_c X)^a_b = Gamma^a_cb (x_b-x_a),
x=(-1,+1,lambda,lambda).
```

At the quaternion north event P00, the frozen polynomial gives exactly

```text
(E1 phi,E2 phi,E3 phi)=(3/50,1/50,2/50).
```

The Cartan connection then contains

```text
Gamma^0_01=-3/50,
```

so, for symbolic real `lambda`,

```text
(nabla_E0 X)^0_1=(-3/50)[(+1)-(-1)]=-3/25 != 0.
```

This term contains no `lambda`.  Hence no real screen weight makes this particular
`X_lambda` parallel on the frozen nonconstant profile.  This is an exact local statement about the
registered witness, not a no-go for every UDT metric.

The sampled block atlas also exposes the two expected degeneracies:

- at `lambda=-1`, clock–screen mixing is invisible to `nabla X`, but clock–ruler and ruler–screen
  mixing remain;
- at `lambda=+1`, ruler–screen mixing is invisible, but clock–ruler and clock–screen mixing remain.

For all other sampled weights, all three inter-sector blocks are present.  Screen-internal rotation
commutes with `X_lambda` because the two screen eigenvalues are equal.

## 3. Curvature-generated holonomy

For each event, form the six Lorentz endomorphisms

```text
R_cd=R(E_c,E_d), 0<=c<d<=3.
```

Their registered six coordinates are the three boost and three rotation entries.  With relative
SVD threshold `1e-9`, all 18 event/branch sets have rank six before any commutator is added.
Ambrose–Singer therefore places a full `so(1,3)` curvature span in the restricted holonomy algebra;
because the Levi-Civita algebra is at most `so(1,3)`, it is exactly full at these sampled events.

The coordinate-metric/Torch implementation independently reproduces rank six in all 18 cases and
agrees with the frame curvature to maximum scaled error
`2.0532409106266414e-10`.

A path-independent endpoint endomorphism would require every loop holonomy `U` to obey

```text
U X_lambda U^-1=X_lambda,
```

equivalently every infinitesimal holonomy generator would commute with `X_lambda`.  Full Lorentz
holonomy cannot centralize this non-scalar endomorphism because its clock and ruler eigenvalues are
always different.  The subalgebra that happens to commute with it has dimension one for generic
sampled `lambda` and dimension three at `lambda=+/-1`; it is never the full six-dimensional
holonomy algebra.

## 4. Closed-loop transport

For a prescribed quaternion path `q(s)`, let

```text
omega=q^-1 dq=(sigma1,sigma2,sigma3).
```

At constant coordinate time, its orthonormal tangent components are

```text
v=(a e^-phi sigma3dot,
   e^+phi sigma3dot,
   e^(lambda phi) sigma1dot,
   e^(lambda phi) sigma2dot).
```

The fundamental transport matrix obeys

```text
dU/ds=-Gamma(v) U, U(0)=I.
```

All 36 registered loops are closed in `q`, preserve the Lorentz metric numerically, and return a
nonidentity `U`.  Every one gives nonzero ordinary closure residual.  This is a concrete witness of
the local curvature conclusion, not its only support.

## 5. Ordinary holonomy is not reciprocal inversion

Odd closure would require

```text
U X_lambda U^-1=-X_lambda
```

for a Lorentz `U`.  Lorentz conjugacy preserves both each eigenvalue multiplicity and the Lorentz
signature of its eigenspace.  The `-1` eigenspace of `X_lambda` always contains the timelike clock
line.  The `-1` eigenspace of `-X_lambda` is the `+1` eigenspace of `X_lambda`, which contains the
spacelike ruler line and is entirely spacelike.  Degeneracies at `lambda=+/-1` do not repair this
signature mismatch.  Thus ordinary Lorentz holonomy cannot implement this inversion for any real
`lambda`.

This does not derive or forbid a distinct non-Lorentz reciprocal transition, seam, quotient, or
observer-comparison operation.  None is supplied here.

## 6. What still composes exactly

For a specified path `gamma:p->q`,

```text
X_gamma(q)=U_gamma X(p) U_gamma^-1
```

composes exactly under path concatenation.  Different paths can give different endpoint lifts,
because their difference is precisely a loop holonomy.  Therefore the path-groupoid cocycle remains
valid.

Separately, on this stationary branch the scalar intrinsic clock comparison remains

```text
log Q(p,q)=phi(q)-phi(p),
```

and is endpoint-only.  The audit therefore separates a closing scalar clock law from a
path-dependent full clock–ruler–screen lift.
