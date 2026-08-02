# Exact derivation — complete-cell Cartan alternating production

Date: 2026-08-02

## 1. Frozen complete-cell families

Two actual complete families in the frozen source universe carry the required exact Cartan data.

1. On the stationary complete `S3` control,

   ```text
   theta0 = exp(-phi)(c_E dt+alpha sigma3),
   theta1 = exp(+phi) sigma3,
   (theta2,theta3)^T = P(sigma1,sigma2)^T,
   D=det(P) != 0.
   ```

   Smooth finite `phi` and smooth invertible `P:S3->GL(2,R)` are arbitrary within this chosen
   off-shell existence family.
2. The FC07 mapping-torus family has full screen Cartan/curvature data but fixes `phi=phi0`.
   It is therefore an actual complete pullback-collapse control, not a failed candidate.

Taxonomy-only completion rows without a joined coframe and first-Cartan system are not filled in.

## 2. The actual contact coefficient

The complete `S3` first structure equations include

```text
dtheta1 = dphi wedge theta1 + t1 theta2 wedge theta3,
t1 = kappa exp(phi)/D.
```

`t1=dtheta1(E2,E3)` is the contact coefficient of the founded ruler one-form against the oriented
screen area. Under a local orientation-preserving `O(2)` change of screen coframe,
`theta2 wedge theta3` is unchanged. Under a screen reflection, `t1` changes sign, so `|t1|` and
`d log|t1|` remain well defined on either connected orientation stratum. This is still relative to
the registered ruler/screen split; it is not a scalar under arbitrary complete-frame mixing.

Define the cold-reviewed log-area scalar

```text
sigma=log(|D|/D0),       D0>0 constant.
```

Then, with `B=log(|kappa|/D0)` constant,

```text
v := log|t1| = B+phi-sigma,
dv = dphi-dsigma.
```

Consequently the actual first-Cartan contact coefficient gives

```text
-dphi wedge dlog|t1| = dphi wedge dsigma.                 (1)
```

The coefficient is exactly one in the registered `sigma=log(|D|/D0)` normalization. Equation (1)
is a split-relative Cartan differential identity. It is not an equation of motion or selected
response.

## 3. The alternating primitive and its exact ambiguity

The cold-reviewed candidate is

```text
lambda_phi_sigma=(phi dsigma-sigma dphi)/2,
dlambda_phi_sigma=dphi wedge dsigma.
```

Using the actual contact log `v`, define

```text
lambda_phi_v=(v dphi-phi dv)/2.
```

Direct substitution gives

```text
lambda_phi_v
  = (phi dsigma-sigma dphi)/2 + (B/2)dphi
  = lambda_phi_sigma + d(B phi/2).
```

Thus the founded depth and the contact coefficient reconstruct the same alternating primitive
modulo the already-permitted exact reference shift. Cartan geometry supplies an available
representative of the formal alternating class inside the chosen split; it does not select the
primitive as a law or set a harmonic level.

## 4. Why `m` is not load-bearing

The displayed general-screen equations also write

```text
d(theta_screen)=sum_A L_A thetaA wedge theta_screen
                +m theta1 wedge C theta_screen,
m=kappa exp(-phi).
```

It is tempting to call `m` a second scalar Cartan coefficient. That is not presentation-safe. A
position-dependent screen rotation contributes `(dO)O^-1` to `L_A`; its `theta1` skew component can
mix with the displayed `mC` term. The split between `L1_skew` and `mC` therefore uses the supplied
Maurer-Cartan presentation. The production claim does **not** use `m`. The invariant route is the
founded `dphi` plus the contact coefficient `t1` from `dtheta1`.

## 5. Formal rank versus fixed pullback rank

For the six-dimensional affine coefficient family

```text
(a0+a1 phi+a2 sigma)dphi+(b0+b1 phi+b2 sigma)dsigma,
```

the exterior derivative is

```text
(b1-a2)dphi wedge dsigma.
```

The universally exact kernel has dimension five and the formal quotient has rank one. A fixed
configuration has rank one only where `dphi wedge dsigma` is nonzero. It collapses for
`sigma=F(phi)`, constant `phi`, or constant angular area.

The collapse is not merely formal. On every frozen FC07 mapping torus, `dphi=0`, so the alternating
object is zero. Conversely, the chosen complete `S3` family contains a constructive global rank-one
witness. On the unit `S3` in `R4`, take

```text
phi=x1,
sigma=x2,
P=exp(x2/2) I.
```

`P` is smooth and invertible everywhere. At `(0,0,1,0)`, `dx1` and `dx2` are independent tangent
covectors, so `dphi wedge dsigma` is nonzero. This is an off-shell geometry witness, not a realized
UDT solution.

## 6. Connection and curvature audit

A Levi-Civita connection one-form is not a tensor. Under a local coframe transformation it has an
inhomogeneous `Lambda d(Lambda^-1)` term. Therefore connection coefficients alone cannot supply an
observer-natural scalar one-form without an independently selected reduction or tensorial
construction. The available `lambda_phi_v` remains split-relative.

As a direct curvature control, the production calculation restricts only the screen shape—not the
independent depth and area fields—to the exact complete subfamily

```text
P=exp(sigma/2) I,   alpha=0,
```

and retains arbitrary spatial first jets of `phi` and `sigma` on `S3`. It derives all structure
equations, solves the torsion-free metric-compatible connection, imposes `d(dphi)=0` and
`d(dsigma)=0`, verifies all four `d^2 theta^a=0` identities, and computes the full curvature.

The independent verifier instead reconstructs the connection through the anholonomic Koszul
formula and curvature through frame commutators. Both routes agree:

```text
nonzero lower curvature-pair blocks             6
curvature rows containing p_i sigma_j products  0
nonzero alternating p/sigma projections         0
nonzero symmetric p/sigma projections           0
```

So the alternating form is not secretly an isolated Levi-Civita curvature term on this exact
complete isotropic-screen control. This is a bounded negative only. Full `GL(2,R)` shear first jets
may create additional split-relative curvature components and have not been exhaustively reduced.

## 7. Naturality ruling

The contact construction is invariant under local screen `O(2)` presentation changes and screen
orientation after taking `|t1|`. It still requires the registered founded ruler and complementary
screen. An arbitrary pair/screen-changing Lorentz coframe transformation changes which two-plane is
called the screen and which coefficient is `t1`. No split-free angular scalar or complete-frame
descent has been derived.

Therefore the exact bounded outcome is

```text
SPLIT_RELATIVE_DIFFERENTIAL_PRODUCTION_ONLY__PRIMITIVE_AND_NATURALITY_OPEN
```

Meaning:

- the complete `S3` first-Cartan system really carries the alternating differential class;
- its primitive is available modulo an exact reference term, not selected;
- fixed branch pullbacks can retain or collapse it;
- FC07 collapses it;
- the exact isotropic curvature control does not isolate it;
- full-screen curvature production and complete-frame naturality remain open; and
- no response law, equation, density return, bootstrap closure, action, carrier, source, mass, or
  matter statement follows.

