# G334 exact derivation — boosted pair first-jet response

Date: 2026-09-03
Status: `DERIVED_CONDITIONAL_BOUNDED_PENDING_EXTERNAL_REVIEW`

## 1. Inherited metric first jet

Let `n` be the future unit normal to a G332 initial slice and let `v` be any unit spatial direction.
G333 gives the invariant first normal logarithmic length rate

```text
q := gamma(Hv,v) = (b-C)/2-b*mu,
mu = gamma(v,xi)^2 in [0,1].
```

Here `q` is local shorthand for this scalar and is unrelated to the complete-coframe matrix `Q`.
Both G332 square-root branches remain present through `b`. In the declared Gaussian extension with
`[n,v]=0`, the pair metric and its first normal jet in the `(n,v)` coordinate germ are

```text
h(0) = eta = diag(-1,1),
D0 := n(h)|0 = [[0,0],[0,2q]].
```

This is a tensor first jet in one declared transport presentation, not a finite-time solution.

## 2. Every finite local boost in the inherited class

At the evaluation point choose any finite rapidity `z` and write

```text
u = cosh(z)n+sinh(z)v,
s = sinh(z)n+cosh(z)v.
```

With

```text
B(z) = [[cosh(z),sinh(z)],[sinh(z),cosh(z)]],
B^T eta B = eta,
```

the inherited first-response matrix is the exact Lorentz congruence

```text
D(z) = B(z)^T D0 B(z)
     = 2q [[sinh(z)^2, sinh(z)cosh(z)],
            [sinh(z)cosh(z), cosh(z)^2]].
```

Thus

```text
n(h00) = 2q sinh(z)^2,
n(h01) = 2q sinh(z)cosh(z),
n(h11) = 2q cosh(z)^2.
```

A constant boost of the commuting `(n,v)` coordinate germ is itself a valid local coordinate
change. If `z` varies normally, its first rate generates an infinitesimal Lorentz transformation.
The two basis-rate terms cancel because the Lorentz generator is `eta`-antisymmetric. Therefore
the displayed first component jet does not depend on `n(z)` within this Lorentz-carried frame
class. A spatially varying frame has separate integrability conditions and is not silently called a
coordinate pullback.

## 3. What is unchanged by the boost

The mixed first-response endomorphism is `A=eta^{-1}D(z)`. It has

```text
tr(A)  = 2q,
det(A) = 0,
spec(A) = {0,2q}.
```

Equivalent exact identities are

```text
n(h11)-n(h00) = 2q,
n(h01)^2 = n(h00)n(h11).
```

Under boost reversal `z -> -z`, the two diagonal derivatives are even, the cross derivative is
odd, and the characteristic data remain unchanged. The boost therefore redistributes G333's one
directional response; it creates no new invariant response channel.

## 4. Terminal scalar

On the regular calibrated stratum,

```text
Phi = -(1/2)log(-h00).
```

Since `h00=-1` at the evaluation point,

```text
n(Phi) = (1/2)n(h00) = q sinh(z)^2
```

in the inherited transport class. Consequently:

- at `z=0`, terminal `Phi` has zero first normal derivative for every `q`;
- at `q=0`, the entire inherited first-response matrix vanishes;
- at finite `z != 0`, `q=n(Phi)/sinh(z)^2` if the boost and transport are supplied;
- near `z=0`, that terminal reconstruction is ill-conditioned;
- the complete inherited matrix recovers `q=[n(h11)-n(h00)]/2` at every finite boost, including
  `z=0`.

This is a comparison of channels within one declared germ transport. It is not a claim that raw
matrix components are invariant under arbitrary first-order reparameterization.

## 5. General first-order pair transport

For any supplied pair-frame extension `e0=u`, `e1=s`, tensor differentiation gives

```text
n(h_ab) = (L_n g)(e_a,e_b)
          +g([n,e_a],e_b)+g(e_a,[n,e_b]).
```

At the evaluation point decompose the in-plane parts as

```text
[n,u] = alpha u+beta s+W0,
[n,s] = gamma u+delta s+W1,
```

where `W0,W1` are orthogonal to the pair plane. Their screen-orthogonal parts do not contribute to
this first component derivative. The full component jet is

```text
D_general = D(z)+[[-2alpha, beta-gamma],
                  [beta-gamma, 2delta]].
```

Hence the pointwise boost value and `q` do not determine an arbitrary pair first jet. First-order
transport is part of the supplied germ. A pure Lorentz boost rate has
`alpha=delta=0` and `beta=gamma`, so it contributes zero, agreeing with Section 2.

A moving frame continuously re-orthonormalized along `n` can choose

```text
alpha = n(h00)_inherited/2,
delta = -n(h11)_inherited/2,
beta-gamma = -n(h01)_inherited,
```

which makes every raw component derivative zero even when `q` is nonzero. The geometry has not
vanished; its first response has moved into the frame transport. This is why transport must remain
explicit and why `BOOST_VALUE_SUFFICIENT` is rejected.

## 6. Normal derivative is not observer-time evolution

The derivative tested throughout is along `n`. For a boosted observer,

```text
u(f) = cosh(z)n(f)+sinh(z)v(f).
```

At nonzero boost, knowing `n(f)` does not determine `u(f)` without the spatial derivative `v(f)`.
G333/G334 do not supply that additional spacetime jet, acceleration, or a finite-time development.
Therefore this result cannot be promoted into the time history measured along the boosted observer.

## 7. Evidence and bounded landing

The production implementation uses exact rational and quadratic-extension arithmetic over 2,520
G332/direction/boost controls, retains both algebraic branches, and passes 43,026 exact checks. Its
rational half-rapidity controls are finite samples; the all-finite-boost statement rests on the
analytic identities above.

The independent implementation imports no production code and reads no production output. It
reconstructs the response by centered finite differences with independently varying rapidity and
passes 580 checks. Twelve preregistered hostile scientific mutations are caught.

The bounded landing is

```text
G333_FIRST_NORMAL_RESPONSE_HAS_EXACT_FINITE_BOOST_CONGRUENCE
__ARBITRARY_PAIR_FIRST_JET_REMAINS_TRANSPORT_QUALIFIED
__COMPLETE_MATRIX_EXCEEDS_TERMINAL_PHI_ON_INHERITED_GERMS
__NO_NEW_CHANNEL_OR_OBSERVER_TIME_EVOLUTION
```

This modifies neither the metric nor the reciprocal kernel. It selects no pair population,
topology, datum, history, matter/mass law, observation, scale, physical `X_max`, or canon.
