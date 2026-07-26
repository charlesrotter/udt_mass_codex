# Exact derivation

## 1. The correct local object

At one event, supply a future unit observer `u` and an orthogonal unit spatial ruler direction `n`.
Their metric projectors define

```text
X_lambda(u,n)=-P_u+P_n+lambda(I-P_u-P_n).
```

This is coordinate-free, metric-self-adjoint, and has the founded clock/ruler eigenvalues `-1,+1`.
The two-dimensional screen receives the still-open scalar weight `lambda`.

A rotation of the screen fixes `u` and `n` and commutes with `X_lambda`. Therefore the endomorphism
is defined by the ordered pair without selecting an oriented screen basis. The full screen coframe
still has an `SO(2)` gauge, but the reciprocal endomorphism and its scalar-screen finite character
do not.

This is why the correct object is an ordered pair frame—equivalently a point of the local
`SO+(1,3)/SO(2)` pair-frame bundle—not a bare spacetime event.

## 2. Path transport

For a supplied complete metric and regular path `gamma`, let `U_gamma` be metric parallel transport.
Transport the pair endomorphism by

```text
X_B=U_gamma X_A U_gamma^-1.
```

For concatenated paths,

```text
U_(beta circle alpha)=U_beta U_alpha,
```

so conjugation composes and reverses exactly for every real `lambda`. No endpoint section and no
flatness premise are required when the path label and transported pair are retained.

Two paths to the same endpoint give the same `X_B` exactly when their relative loop holonomy
centralizes `X_A`. Otherwise they are distinct valid path-labelled arrows. This is path dependence,
not an algebraic contradiction.

## 3. The old middle mismatch is a vertical arrow

Suppose the incoming comparison reaches event `B` with pair frame `f_(B|A)`, while the outgoing
comparison is written in a different pair frame `f_(B|C)`. These are two distinct objects in the
same fiber. A Lorentz map `V_B` relating them is a vertical pair-change arrow.

The covariance identity is

```text
X_(B|C) V_B = V_B X_(B|A).
```

Any two Lorentz maps carrying the same ordered input pair to the same ordered output pair differ by
a screen rotation. Since the screen response is scalar, both induce the same conjugated
`X_lambda`. Including `V_B` makes composition exact. Omitting it while changing pairs creates the
previously recorded middle factor.

At `lambda=1`, changing only the ruler direction of one fixed observer has no effect because the
entire spatial complement carries one weight. Changing the observer still changes `X_1`. Thus
`lambda=1` does not turn the pair-frame bundle into bare events.

## 4. Adding reciprocal depth

For a signed depth `delta`, define

```text
D_f(delta)=exp(delta X_f).
```

Transport intertwines the characters:

```text
D_(U f)(delta) U = U D_f(delta).
```

If `delta` is an additive real cocycle on path-labelled arrows, then

```text
T_gamma=U_gamma D_f(delta_gamma)
```

obeys exact typed composition and reversal for every `lambda`.

This is a conditional kinematic completion, not a derivation of `delta`. Levi-Civita transport is a
metric isometry. A nonzero aligned reciprocal character changes the metric readout and is Lorentz
isometric only at `delta=0`. Therefore metric parallel transport cannot silently serve as the
missing depth character.

## 5. Endpoint-only depth is necessarily a potential difference

Suppose a real endpoint function obeys

```text
delta(A,B)+delta(B,C)=delta(A,C),
delta(B,A)=-delta(A,B).
```

Choose any base event `O` and define `phi(A)=delta(O,A)`. The triangle `(O,A,B)` gives

```text
delta(A,B)=phi(B)-phi(A).
```

Thus every endpoint-only exact real cocycle is a potential difference, unique up to one additive
constant. This does not choose a privileged physical center; the basepoint only fixes the additive
zero.

The prior round-branch theorem remains decisive: one scalar difference cannot also represent every
strictly positive isotropic pair distance on a centerless complete round geometry. Therefore exact
endpoint additivity forces a choice of meaning. `phi(B)-phi(A)` may be an ordered solution-field
difference, but it cannot simultaneously be the universal nonnegative distance magnitude for every
pair.

## 6. Path depth and periods

For any one-form `alpha`,

```text
delta_gamma=integral_gamma alpha
```

composes under path concatenation and changes sign under reversal. Closedness gives local endpoint
independence; global endpoint independence additionally requires every loop period to vanish.

The positive reciprocal character is faithful:

```text
D(Pi)=I  iff  Pi=0
```

for real `Pi`. A nonzero real period therefore produces visible reciprocal loop holonomy. It cannot
be hidden as a nonzero period of an ordinary compact phase.

## 7. What is now closed

The local and pathwise kinematic structure is no longer missing:

- ordered clock/ruler pairs define `X_lambda` without a screen orientation;
- metric path transport carries them covariantly;
- explicit vertical arrows resolve pair resets;
- typed path composition works for every `lambda`; and
- an additive signed depth would complete the full reciprocal comparison exactly.

The smallest remaining kinematic join is the metric-native assignment of that signed depth to the
typed pair-frame arrows. Current evidence allows several inequivalent types:

1. a global signed solution-field difference;
2. a path-integrated depth with possible periods;
3. an observer-chart accumulation law; or
4. a nonadditive bilocal magnitude whose general composition necessarily includes angular data.

The audit selects none of them.

