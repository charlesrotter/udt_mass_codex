# Exact derivation

## 1. General extension preserves the founded pair laws

In the registered triangular section, write

```text
X = [[H,0],
     [C,K]],

H = diag(-1,+1),
K = [[a,b],[0,d]].
```

There are three independent entries of `K` and four of `C`. For every
positive integer `n`, block multiplication gives

```text
(X^n)_base = H^n,
(X^n)_upper-right = 0.
```

Consequently the exponential power series has

```text
exp(phi X)_base = exp(phi H)
                 = diag(exp(-phi),exp(+phi)).
```

Because one fixed generator commutes with itself,

```text
exp(phi X) exp(psi X) = exp((phi+psi) X),
exp(-phi X) = exp(phi X)^-1.
```

Thus pair projection, additive composition, and observer-order reversal hold
for the entire seven-parameter extension class. They do not constrain `K` or
`C`.

## 2. The seven directions are physical metric tangents

With internal readout

```text
eta = diag(-1,+1,+1,+1),
g(phi) = E(phi)^T eta E(phi),
```

the tangent at `phi=0` is

```text
Q = X^T eta + eta X.
```

For the extension part alone,

```text
Q_ext = [[0, C^T],
         [C, K^T+K]].
```

The map from

```text
(a,b,d,C11,C12,C21,C22)
```

to `Q_ext` has rank seven. Setting `Q_ext=0` forces all seven parameters to
zero.

The full coframe presentation kernel is the six-dimensional local Lorentz
algebra

```text
Y^T eta + eta Y = 0.
```

Its intersection with the seven-dimensional triangular extension tangent is
zero. Local Lorentz equivalence therefore removes no direction from this
bounded extension class. These are possible physical metric responses, not
merely rotations of an unchanged coframe.

This is a pointwise tangent statement, not a count of propagating modes.

## 3. Full-frame reciprocity requires equivariance, not a fixed plane

If one incorrectly requires one component matrix `X` to remain unchanged
under every connected local Lorentz transformation, then `X` must commute
with all six Lorentz generators. Exact linear algebra gives

```text
centralizer_SO+(1,3) in M4(R) = {lambda I}.
```

The founded base generator has unequal entries `-1,+1`, so it is not in that
centralizer. Fixed full-frame invariance is therefore incompatible with any
nontrivial founded reciprocal generator.

This is not a failure of frame reciprocity. A tensorial generator or its
reciprocal two-plane must transform by conjugation when the observer frame
changes:

```text
X -> Lambda X Lambda^-1.
```

That is equivariance. It carries the family consistently between frames but
does not select the reciprocal plane, `K`, or `C`. The registered sources do
not yet supply the covariant slot/lift rule.

## 4. Exact non-spectator survivors

The angular family

```text
E_k(phi) = diag(exp(-phi), exp(phi), exp(-k phi), exp(k phi))
```

has determinant one, exact composition and reversal, and the founded pair
projection for every real `k`. For nonzero `k`, its angular metric changes.

The mixing family

```text
E_s(phi)[2,0] = s(1-exp(-phi))
```

with founded diagonal base and identity elsewhere has the same pair laws and
determinant one. For nonzero `s`, its physical metric has a nonzero
base-angular cross term.

These are countermodels to unconditional spectator uniqueness. They are not
proposed realized UDT branches.

## 5. Conditional ranks are not active selection

Extra conditions have exact ranks:

- complete determinant one: rank one, leaving six;
- unchanged positive transverse metric: rank three, leaving four;
- no base-angular metric mixing: rank four, leaving three;
- unchanged transverse metric plus no mixing: rank seven, uniquely leaving
  the spectator extension in this section.

The first does not follow from determinant one of the founded pair. The next
two are precisely the additional spectator premises. Strong local CSN would
remove only the angular trace in the recorded counterfactual branch, but it
is challenged and inactive.

## 6. Why the remaining premises have zero or undefined rank

- `c_E` and `G_obs` calibrate physical units but no registered source maps
  them to equations for the dimensionless `K,C` coefficients.
- Coordinate covariance specifies how the generator and metric transform; it
  does not fix their components.
- At the scalar seal value `phi=0`, every one-parameter exponential equals
  the identity. The registered seal has no selected complete lift.
- Finite-cell records classify global completion types but provide no
  off-shell equation on this pointwise family.
- Current bootstrap accepts or rejects completed on-shell solutions; it has
  no operation on the off-shell extension family.
- `X_max` lacks its native pair-separation functional, observer domain, and
  angular/global completion, so it supplies no pointwise extension equation.
- Conditional toric/Hopf data, carrier, action, source, and boundary
  functional are downstream or open and cannot be used as selectors.

The joint active selector rank is therefore zero in the bounded class. All
seven physical tangent directions survive. This does not prove that future
native global closure cannot select among them.

## 7. Variation-domain consequence

Selecting a complete extension and selecting a variation domain are distinct
steps. The present result says that the founded scalar direction has a known
clock/ruler projection but an unselected angular/mixing lift. It does not say
that the seven lift coefficients are seven independent dynamical fields.

Until a covariant complete-coframe lift or section rule is derived, current
authority cannot decide which full metric directions are tied to `delta phi`,
which are independently varied, or what boundary variations accompany them.
The complete variation domain therefore remains open.
