# Exact derivation — broader-coframe exact/harmonic response

Date: 2026-08-02

Outcome: `MINIMAL_CROSS_SECTOR_RESPONSE_EXISTS__LAW_SELECTION_OPEN`

This is a theorem plus constructive-control result over the exact bounded layers in the
preregistration. It does not select a UDT equation.

## 1. Universal compact-Hodge obstruction

Let `(Sigma,q)` be compact, oriented, Riemannian, and boundaryless. For every smooth real
single-valued scalar `f` and harmonic one-form `h`, Hodge adjointness gives

```text
<df,h> = <f,delta h> = 0.
```

Therefore the harmonic projection of every exact one-form is zero:

```text
Pi_H(df)=0.
```

This is independent of lower-triangularity, torus invariance, the detailed metric coefficients,
and upper-right mixing. In particular, a single-scalar response

```text
F(phi)dphi=dH(phi),       H'(phi)=F(phi),
```

remains exact for the founded real single-valued `phi`. No integrating factor depending only on
`phi` can create a nonzero harmonic response on a compact boundaryless cell.

The theorem is deliberately typed. A boundary, a circle-valued replacement scalar, a twisted
coefficient bundle, or time-live/non-Riemannian problem would be a different domain.

## 2. Complete minimal two-scalar first-derivative census

Inside the registered screen split, define

```text
D>0,
sigma=log(D/D0),
```

where `D0>0` is an arbitrary constant used only to type the logarithm. The most general one-form
whose coefficients are affine in `(phi,sigma)` has six constant directions. The preregistered basis
is

```text
dphi,
dsigma,
phi dphi,
sigma dsigma,
phi dsigma + sigma dphi,
lambda=(phi dsigma-sigma dphi)/2.
```

The first five are exact:

```text
dphi                  = d(phi),
dsigma                = d(sigma),
phi dphi              = d(phi^2/2),
sigma dsigma          = d(sigma^2/2),
phi dsigma+sigma dphi = d(phi sigma).
```

The alternating direction obeys

```text
dlambda=dphi wedge dsigma.
```

Thus the quotient of this six-dimensional response space by its exact subspace is exactly
one-dimensional. This is a bounded algebraic uniqueness statement only: it does not say that UDT
selects `lambda`, or that higher-derivative, curvature, nonpolynomial, or nonlocal responses do not
exist.

## 3. The reference constant drops out of harmonic content

Under constant shifts

```text
phi   -> phi+A,
sigma -> sigma+B,
```

the response changes by

```text
Delta lambda = (A dsigma-B dphi)/2
             = d[(A sigma-B phi)/2].
```

Its harmonic projection therefore does not depend on the additive zero of `phi` or the arbitrary
area reference `D0`. This does not create an absolute area scale.

## 4. Global base-loop witness

On the normalized closed base, take the smooth admissible profiles

```text
phi(s)=sin(2 pi s),
sigma(s)=cos(2 pi s),
D(s)=D0 exp(sigma(s))>0.
```

Then

```text
lambda=-pi ds,
integral_base lambda=-pi.
```

For the flat base control, `ds` spans the one-dimensional harmonic space, so this is a constructive
nonzero harmonic response. Geometrically,

```text
integral lambda = (1/2) integral (phi dsigma-sigma dphi)
```

is the signed area enclosed by the closed path in the `(phi,sigma)` plane. A single metric sector
retraces a line and leaves only an exact note; two sectors can trace a loop and leave a global
residue.

This is the exact mathematical content of the “orchestra” lead. The chosen sinusoidal profiles are
constructive witnesses, not realized UDT solutions or fitted physics.

## 5. Non-torus local-curl witness

On the minus-identity mapping torus, the fields

```text
phi(y,z)=cos(2 pi y),
sigma(y,z)=cos(2 pi z)
```

descend under `(y,z)->(-y,-z)`. They give

```text
dlambda
  = 4 pi^2 sin(2 pi y) sin(2 pi z) dy wedge dz,
```

which is not identically zero. Thus away from base-only dependence, the same alternating motif has
a local curl and can populate the coexact as well as harmonic Hodge channels. The actual Hodge
coefficients remain global metric readouts, not selected levels.

## 6. Exact upper-right control

Use the spatial coframe

```text
eta1=ds+dpsi,
eta2=dy,
eta3=dz,
psi=epsilon cos(2 pi y),
q=eta1^2+eta2^2+eta3^2.
```

The metric determinant is exactly one. `psi` is even under the minus-identity monodromy, so the
metric and transitioned coframe descend. `eta1` is closed and coclosed and represents the primitive
base class. But `ds` is generically not coclosed in this metric. Therefore the primitive cohomology
class stays the same while its harmonic representative follows the full metric:

```text
[eta1]=[ds],
eta1-ds=dpsi,
harmonic representative=eta1.
```

Cohomological ownership alone does not fix a pointwise representative independently of the metric.

## 7. Nonclosed upper-right control

Now take

```text
eta1=ds+f(y)dz,
f(y)=epsilon sin(2 pi y),
q=eta1^2+dy^2+dz^2.
```

The product `f(y)dz` is invariant under the minus-identity monodromy because both factors reverse
sign. Again `det q=1`. Exact algebra gives

```text
d eta1 = 2 pi epsilon cos(2 pi y) dy wedge dz != 0,
delta eta1=0,
d ds=0,
delta ds=0.
```

Hence `eta1` is coclosed but not harmonic, while `ds` is harmonic. Since `b1=1`, the harmonic
projection is

```text
Pi_H(eta1)=[1/(1+epsilon^2/2)] ds
```

on the unit coordinate cell. The raw ruler line and primitive harmonic line are not pointwise the
same. The earlier projective ownership result is therefore exact only in its lower-triangular
family; it is not robust under this explicit upper-right extension.

This witness is registered only on the minus-identity FC07 completion. It is not a construction for
all four monodromies or a derivation that UDT must activate upper-right mixing.

## 8. Naturality and selection

The result has three different grades:

1. `Pi_H(df)=0` is universal mathematics on the stated compact boundaryless Hodge domain.
2. The one-dimensional alternating quotient is exact in the preregistered minimal two-scalar basis.
3. `lambda` is only `AVAILABLE`: the current metric premises do not select this response, set its
   harmonic coefficient, equate it to another geometric object, or make it an equation.

Moreover `sigma` currently uses the registered oriented screen split. Its constant reference is
harmless, but a unique extension under arbitrary complete-frame pair/screen mixing is open.
Observer Reciprocity therefore requires any future law to carry naturally; it does not promote the
present split-relative response to a fully frame-independent law.

The internal dual reciprocal pairing likewise fixes the founded clock/ruler representation, not a
response covector or level. `Xmax` reciprocity remains excluded/open.

## 9. Density and physics gate

The audit found a nonidentity same-configuration metric response motif, but not a return equation.
There is still no derived statement of the form

```text
R(lambda,alpha,connection,curvature,rho_tot)=0
```

that fixes a response or relates it to total proper density. Density bracketing therefore remains
unauthorized. No action, source, carrier, mass, bootstrap fixed point, physical branch, or time-live
law follows from this result.

## Exact ruling

```text
single-sector exact-to-harmonic linear response       DERIVED_ZERO
minimal two-sector alternating response direction    DERIVED_BOUNDED_BASIS
nonzero harmonic and local-curl witnesses             DERIVED_CONSTRUCTIVE_CONTROLS
lower-triangular pointwise ruler ownership             NOT_ROBUST_UNDER_UPPER_RIGHT_CONTROL
complete-frame natural response                       OPEN
native response law or selected level                 OPEN
density bracket                                       NOT_AUTHORIZED
```
