# Exact derivation — full GL(2,R) screen curvature and frame descent

## 1. Bounded complete family

The calculation stays inside the preregistered stationary off-shell complete-`S3` family with
arbitrary smooth finite `phi` and arbitrary smooth invertible `P:S3->GL(2,R)`. The screen response
is written in regular first-Cartan variables:

```text
M1 = [[a+h1, h2-r], [h2+r, a-h1]],
```

where `a` is area, `h1,h2` are both shears, and `r` is the displayed screen rotation slot. The two
remaining screen anholonomy coefficients are `u,v`. No screen mode is set to zero.

Together with depth components `p1,p2,p3` and contact coefficients `t0,t1`, the exact exterior
system is

```text
dtheta0 = -dphi wedge theta0 + t0 theta2 wedge theta3,
dtheta1 = +dphi wedge theta1 + t1 theta2 wedge theta3,
dtheta2 = (a+h1)theta1 theta2 + (h2-r)theta1 theta3 + u theta2 theta3,
dtheta3 = (h2+r)theta1 theta2 + (a-h1)theta1 theta3 + v theta2 theta3.
```

Here juxtaposed theta pairs denote wedges. The nine displayed `d^2` rows reduce to five independent
closure equations: three for `d^2 phi=0` and two for the screen. The exact determinant relations

```text
E_i t1 = t1(p_i-sigma_i),
E_i t0 = -t0(p_i+sigma_i),
sigma_1 = 2a
```

are imposed, while `sigma_2,sigma_3` remain free first jets.

## 2. Full curvature

The production route constructs the torsion-free metric-compatible connection with the anholonomic
Koszul formula and computes frame-commutator curvature. The independent route solves 24 connection
unknowns from Cartan torsion plus metric compatibility and computes
`Omega=domega+omega wedge omega`.

Both routes agree on all 36 lowered curvature-pair/two-form rows. All six curvature blocks are
nonzero. Raw sector census counts are:

```text
depth x screen    14 rows
depth x contact   26 rows
screen x contact  15 rows
shear x contact   12 rows
```

These are normal-form component counts, not tensorial multiplicities. The full scalar curvature is

```text
R = -(8 E1(a)-4 E1(p1)+4 E2(v)-4 E3(u)
      +12 a^2-8 a p1+4 h1^2+4 h2^2
      +4 p1^2+4 p2^2+4 p3^2-4 r t1
      -t0^2+t1^2+4 u^2+4 v^2)/2.
```

Thus full metric curvature really contains the contact norm, but only inside a larger invariant
combination with area, shear, rotation, depth, and derivative terms. It does not select the contact
piece or a response law.

## 3. Split-preserving contact invariant

For the registered reciprocal-pair/screen reduction, define the pair-valued screen contact

```text
q^a = dtheta^a(E2,E3),       q=(t0,t1).
```

Under a local pair boost `B(beta)`, the derivative-of-boost term vanishes when restricted to the
screen, so `q'=Bq`. A screen reflection sends `q` to `-q`. Therefore

```text
q^2 = t1^2-t0^2
```

is invariant under the full split-preserving `O(1,1)xO(2)` group. On the exact coframe,

```text
q^2 = kappa^2/D^2 [exp(2phi)-alpha^2 exp(-2phi)].
```

On either non-null stratum,

```text
z = log(sqrt(|q^2|)/T0)
  = constant - sigma + (1/2)log|exp(2phi)-alpha^2 exp(-2phi)|,

dphi wedge dz = -dphi wedge dsigma.
```

This is stronger than the old single-`t1` presentation: the same differential class survives every
frame change preserving the reciprocal pair and screen. At `q^2=0`, the logarithm is undefined and
the null stratum must be treated separately.

## 4. Why complete-frame descent fails

The reduction invariant is not a metric scalar. At a point, take a local pair/screen-changing
spatial rotation whose value is the identity but whose derivative `E3(psi)=g` is arbitrary. Then

```text
t1' = t1-g,
```

so `q^2` changes although the metric and pointwise frame value do not. A pair/screen-changing local
Lorentz boost analogously gives `t0'=t0-g`. Such transformations generally leave the displayed
block-screen ansatz; this is not a physical inconsistency. It proves that the contact extraction
needs the registered reduction and does not descend to the metric alone.

The Riemann tensor and its complete contractions remain fully frame covariant/invariant. Curvature
contractions using pair and screen projectors remain reduction-relative unless those projectors are
independently selected.

## 5. Result

The preregistered headline is

`SPLIT_RELATIVE_ONLY__NO_COMPLETE_FRAME_DESCENT`.

The full screen strengthens the contact object from a single coefficient to an
`O(1,1)xO(2)`-invariant norm and shows that curvature contains it. It does not derive a split-free
metric scalar that uniquely carries the reciprocal/Hopf response. No law, action, carrier, source,
density, bootstrap selector, matter, or mass follows.

