# Exact derivation — Killing-plane response and the two strata

## 1. Bounded family

The calculation is confined to the registered stationary constant-`alpha` block-screen family on
the chosen `R x S3` control. Full Hopf metric descent supplies two commuting Killing generators:
the stationary generator `K` and the compact free-circle generator `V`. No equation of motion,
action, carrier, source, density, or physical macro/micro assignment is used.

Write `u=exp(-2 phi)>0`. The complete metric restricted to the Killing algebra in the basis `(K,V)`
is

```text
G = [ -c_E^2 u             -c_E alpha u          ]
    [ -c_E alpha u          1/u-alpha^2 u         ].
```

Its determinant is exactly

```text
det G = -c_E^2.
```

Thus the plane is Lorentzian everywhere for nonzero observed `c_E`; neither angular shear enters
this orbit-plane identity.

## 2. Causality does not pick one clock

For every constant Killing direction `W_Omega=K+Omega V`,

```text
g(W_Omega,W_Omega)
 = -exp(-2phi)(c_E+alpha Omega)^2 + exp(2phi) Omega^2.
```

The two pointwise null slopes are

```text
Omega_+ =  c_E/(exp(2phi)-alpha),
Omega_- = -c_E/(exp(2phi)+alpha),
```

with a vanishing denominator interpreted as the projective endpoint `V`. `K` is always timelike,
but on compact smooth finite-depth bases uniform continuity leaves a nonzero interval of nearby
constant `Omega` values timelike everywhere. Causality therefore does not single out `K`.

## 3. The changing Gram metric supplies the missing selector

Let `X` be any direction transverse to the Killing orbits and put `chi=X(phi)`. The metric itself
defines the Killing-algebra endomorphism

```text
D_X = G^-1 X(G).
```

Exact differentiation gives

```text
D_X = [ -2 chi       -4 alpha chi/c_E ]
      [   0                 2 chi      ],

tr D_X=0,
D_X^2=4 chi^2 I.
```

It is self-adjoint with respect to the Lorentzian Gram form because `G D_X=X(G)` is symmetric. For
`chi != 0` it has two distinct, exact eigenlines:

```text
clock:  K,                         eigenvalue -2 chi,
ruler:  V-(alpha/c_E)K,            eigenvalue +2 chi.
```

Their norms and mutual product are

```text
g(K,K)=-c_E^2 exp(-2phi),
g(V-alpha/c_E K,V-alpha/c_E K)=exp(2phi),
g(K,V-alpha/c_E K)=0.
```

These are exactly the founded reciprocal clock/ruler weights. No coordinate basis has been
privileged: under every constant change of Killing basis `B`,

```text
G' = B^T G B,
D'_X = B^-1 D_X B,
```

so its eigenlines transform covariantly. The timelike/spacelike signs order the pair without an
orientation choice.

Equivalently, the norm of a generic helix has the founded clock response only for `Omega=0`:

```text
X g(W_Omega,W_Omega)+2 X(phi)g(W_Omega,W_Omega)
 = 4 X(phi) Omega^2 exp(2phi).
```

When `phi` is nonconstant on the connected quotient base, a regular point exists. The eigenlines
are constant lines in the global Killing algebra, so determining them at any regular point extends
them through the unavoidable extrema where `dphi=0`. The pointwise formula degenerates there, but
the global selector does not.

## 4. Independent depth-mixed twist cross-check

In the coordinate coframe `(dt,sigma3,sigma1,sigma2)`, put

```text
W_Omega-flat = a dt+b sigma3,
a=-c_E(c_E+alpha Omega)exp(-2phi),
b=Omega exp(2phi)-alpha(c_E+alpha Omega)exp(-2phi).
```

Put `dphi=p sigma1+q sigma2` and `d sigma3=kappa sigma1 wedge sigma2`. The complete exact
three-form is

```text
W-flat wedge dW-flat
 = 4 c_E Omega(c_E+alpha Omega)p dt wedge sigma3 wedge sigma1
 + 4 c_E Omega(c_E+alpha Omega)q dt wedge sigma3 wedge sigma2
 + kappa a b dt wedge sigma1 wedge sigma2
 + kappa b^2 sigma3 wedge sigma1 wedge sigma2.
```

For nonzero `dphi`, these vanish on two projective lines. One is `K`; the other is precisely the
spacelike Gram-response ruler `V-alpha/c_E K`. Therefore `K` is the unique timelike line without a
depth-mixed twist component. This independently agrees with the Gram-response result. It is not a
full twist-free claim: when `alpha kappa` is nonzero, both `K` and the ruler generally retain
contact-twist components.

## 5. Constant depth is a real exceptional stratum

If `phi` is constant everywhere, `X(G)=0`, and the response selector disappears. Within the
registered Killing plane, circle topology still identifies `V` up to sign. When `V` is spacelike,
its metric-orthogonal complement has slope

```text
Omega_perp = c_E alpha/(exp(4phi)-alpha^2).
```

For nonzero `alpha` this is not the founded clock `K`; it is also the unique twist-free line in the
nonzero-contact constant-depth subfamily. If `V` is null the orthogonal construction degenerates,
and if `V` is timelike the compact fibers are closed timelike curves and their orthogonal line is
spacelike. Only the special `alpha=0` constant-depth control makes the orthogonal line equal `K`,
while simultaneously removing the prior twist/ruler certificate. In the still more degenerate
`dphi=0=kappa` control, every constant Killing direction is twist-free and `D_X=0`; neither the
Gram response nor twist selects a founded clock.

This is why the primary answer is `MIXED_PARAMETER_STRATA`, not a universal selector theorem.

## 6. Orbit topology and fixed points

On the chosen `R x S3` control, `V` generates free circles and is the registered compact line.
Every `K+Omega V` with nonzero `K` coefficient generates a free noncompact helix because its flow
always advances the noncompact time coordinate. None has a fixed point. Topology distinguishes the
circle line from the helices but cannot distinguish one helix from another.

More explicitly, the automorphisms of the registered `R x S1` orbit group that preserve the
primitive compact lattice have

```text
K -> r K+b V,       V -> epsilon V,
r != 0,             b real,             epsilon=+1 or -1.
```

Thus the unoriented compact `V` line is fixed, while the noncompact generator can be scaled and
sheared by any helix. Generic `GL(2,R)` covariance of the local Gram calculation is stronger
algebraically, but does not replace this global lattice statement. The entire result is conditional
on the registered `(K,V)` plane. Metrics with a larger Killing algebra may contain other Killing
planes or compact circles; selecting among them is outside this audit.

## 7. The two strata are continuously adjacent

Choose any smooth nonconstant descended depth `phi_D` pulled back from the quotient `S2`, and any
positive descended screen metric `h_D`. Let `(phi_C,h_C)` be any one of the six exact old rank-three
configurations. The path

```text
phi_s=(1-s)phi_D+s phi_C,
h_s=(1-s)h_D+s h_C,        0<=s<=1,
```

remains a smooth finite stationary registered metric: convex combinations of positive screen
metrics stay positive. At `s=0` it fully descends, and the Gram-response selector gives `K`. At
`s=1` the frozen scalar-invariant gradient determinant is exactly nonzero and the old rank-three
certificate gives `K`.

That determinant is a real-analytic function of `s`: the metric, inverse, curvature, invariant
gradients, and determinant are analytic along this positive path. It is zero at the descended end
because `V` is a second Killing direction, but it is not identically zero because its exact value at
`s=1` is nonzero. The identity theorem therefore guarantees a sequence of nonzero points arbitrarily
close to `s=0`; it does not say that every sufficiently small nonzero `s` works. The two certificate
strata are disjoint but continuously adjacent, and both identify the same global line `K` at their
respective points.

This is a geometric selector handoff, not an equation selecting where the handoff occurs.
