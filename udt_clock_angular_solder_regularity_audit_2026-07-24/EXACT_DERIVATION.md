# Exact clock/angular solder derivation

## 1. What is being joined

The founding reciprocal clock/parallel comparison has coframe characters

```text
exp(-phi), exp(+phi).
```

The conditional reciprocal-toric angular geometry has characters

```text
exp(-kappa phi), exp(+kappa phi),
```

where `kappa>0` is the free relative unit between the clock and angular depth
parameters. The audit asks whether one scalar `phi` can carry both pairs in a
regular complete static diagonal metric.

Strong local CSN is not used. Common amplitudes remain physical functions.

## 2. Complete fixed-pairing algebra

For a diagonal character map with weights `a_i`,

```text
P(phi)=diag[exp(a_i phi)],
```

a fixed pairing component `K_ij` can be nonzero only if

```text
a_i+a_j=0.
```

For the complete weight set

```text
(-1,+1,-kappa,+kappa),
```

the generic fixed pairing is therefore uniquely blockwise:

```text
(clock,depth), (angular-minus,angular-plus).
```

When `kappa=1`, the two negative-weight and two positive-weight planes can be
cross-paired. That is a coframe-pairing degeneracy. It creates no new
diagonal metric family: it is a relabeling or a constrained subfamily of the
same four legs.

The most general tested double-pair coframe is

```text
theta0 = C(phi) exp(-phi) c dt,
theta3 = ell C(phi) exp(+phi) dphi,
theta1 = R(phi) exp(-kappa phi) dxi1,
theta2 = R(phi) exp(+kappa phi) dxi2.
```

`C` and `R` are positive physical amplitudes, not discarded gauges.

## 3. Round spatial control

The conditional round reciprocal-toric relation is

```text
tan(eta)=exp(2 kappa phi).
```

For a round three-sphere of radius `b`,

```text
A_round = b kappa sech(2 kappa phi),
R_round = b/sqrt[2 cosh(2 kappa phi)].
```

These reproduce exactly

```text
b d eta,
b cos(eta) dxi1,
b sin(eta) dxi2.
```

The neutral torus is `phi=0`, `eta=pi/4`.

For any static lapse `N(eta)` over this round space, the four-dimensional
scalar curvature is

```text
R4 = 6/b^2
     - (2/b^2) [N''+2 cot(2 eta)N']/N.
```

This supplies an invariant cap test. A divergent scalar curvature cannot be
removed by a coordinate relabeling.

## 4. F01: isolated founding clock factor

Keeping the round spatial metric and inserting

```text
N=exp(-phi)
```

gives

```text
N(eta)=tan(eta)^[-1/(2 kappa)]
```

and exactly

```text
R4 = 6/b^2
     - 2/[b^2 kappa^2 sin^2(2 eta)].
```

The scalar curvature diverges at both primitive caps for every finite
positive `kappa`. Reversing `phi` exchanges the two lapse limits but leaves
the squared curvature pole.

Therefore the isolated same-scalar insertion is not a regular two-cap
spacetime.

## 5. F02: fixed-pairing double reciprocal solder

The round radial coefficient and the depth leg require, with the ordinary
normalization `ell=b kappa`,

```text
C(phi)=sech(2 kappa phi) exp(-phi).
```

The lapse is no longer merely `exp(-phi)`:

```text
N(phi)=sech(2 kappa phi) exp(-2phi)
      =sin(2eta) tan(eta)^(-1/kappa).
```

Near the two caps, in proper cap radius `rho`,

```text
N_minus ~ rho^(1-1/kappa),
N_plus  ~ rho^(1+1/kappa).
```

At a smooth primitive toric cap, a radial power `N~rho^p` contributes

```text
Delta N/N ~ p^2/rho^2,
R4 ~ -2p^2/rho^2.
```

The minus-cap power vanishes only at `kappa=1`. The plus-cap power never
vanishes for any finite positive `kappa`. Hence:

```text
no finite positive kappa makes both primitive caps regular.
```

At `kappa=1`, the exact control is

```text
N=2 cos^2(eta).
```

The `eta=0` cap is regular with finite scalar limit `14/b^2`; the opposite
cap has the expected curvature pole. This independently checks the general
power ruling.

## 6. F03: physical common factor

Consider

```text
g_tilde=Omega_phys(eta)^2
        [-exp(-2phi)c^2dt^2+h_round].
```

If `Omega_phys` is smooth, finite, and nonzero at an original round cap, its
logarithm has only finite covariant derivatives there. The conformal scalar
formula therefore adds finite terms, while the F01 `1/rho^2` pole persists,
multiplied by the finite positive factor `Omega_cap^-2`.

A common factor can cancel the clock zero or pole only by itself vanishing or
diverging. That changes the physical metric's nondegeneracy or completion and
is not a repair of the original two caps. Such changed completions remain
open; they are not quotiented away as CSN copies.

## 7. F04: open/asymptotic profiles

For arbitrary positive `C(phi)` the metric gives exactly

```text
N = C(phi) exp(-phi),
A = ell C(phi) exp(+phi),
B = exp(-2phi)/[ell^2 C(phi)^2],
dD/dphi = ell C(phi) exp(phi),
A/N = ell exp(2phi).
```

The last ratio is profile-independent within the fixed-pairing branch. The
endpoint distance is

```text
D_infinity-D_0
  = integral_0^infinity ell C(phi)exp(phi)dphi.
```

It may converge or diverge depending on the unselected physical profile
`C`. The angular amplitude `R`, global completion, cut locus, and
observer-event pairing are also unselected. Consequently the open family is
nonempty but does not calculate a unique endpoint or `X_max`.

If an open profile is forced into two ordinary primitive toric caps, the
smooth-cap asymptotics reproduce the F02 powers and the same obstruction.

## 8. Exact scope of the result

The bounded result is:

```text
NO REGULAR TWO-PRIMITIVE-CAP SAME-SCALAR CLOCK/ANGULAR SOLDER EXISTS
IN THE STATIC DIAGONAL FIXED-PAIRING RECIPROCAL-TORIC CLASS.
```

This is not a theorem that the two meanings of `phi` are globally distinct in
all UDT realizations. It leaves open:

- open or excluded asymptotic endpoints;
- multiple charts and cut loci;
- a clock variable separate from angular depth;
- nonintegrable horizontal distance;
- time-live or shifted coframes;
- and an observer-pair/configuration-space depth.

It also does not determine a global observer-pair diameter.
