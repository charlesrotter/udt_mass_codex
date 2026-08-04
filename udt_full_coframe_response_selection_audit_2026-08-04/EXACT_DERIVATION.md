# Exact derivation — what the full coframe does and does not select

## 1. Configuration map

Let `theta` be an invertible four-coframe and

```text
g = theta^T eta theta,        eta=diag(-1,1,1,1).
```

For an infinitesimal coframe generator `X=delta(theta) theta^{-1}`, the orthonormal-frame metric
tangent is

```text
T_X = X^T eta + eta X.
```

The exact coefficient map from all sixteen entries of `X` to the ten symmetric entries of `T_X`
has rank ten. Its kernel has dimension six and is exactly the Lorentz-gauge algebra

```text
X^T eta + eta X = 0.
```

Thus the complete coframe supplies all ten local metric directions while retaining six
presentation-gauge directions. This is a pointwise tangent statement, not a propagating-mode count
and not a native variation-domain selection.

## 2. Pullback theorem for response covectors

Represent an ambient metric response by a symmetric tensor `E`. Its pairing with a coframe tangent
is, up to the conventional density and an irrelevant overall factor,

```text
alpha_E(X) = (1/2) E:T_X.
```

The exact linear map

```text
E -> alpha_E
```

has rank ten. It is injective on the ten-dimensional symmetric response space. It also annihilates
all six Lorentz-gauge generators because their `T_X` vanishes identically.

Therefore:

```text
FULL_COFRAME_PULLBACK_PRESERVES_EVERY_AMBIENT_METRIC_RESPONSE_AND_ITS_DISTINCTIONS;
IT_DOES_NOT_SELECT_ONE_RESPONSE.
```

This is the central new bounded theorem. It connects the August 4 full-coframe skeleton to the July
29 P4 response program without repeating the latter's formal response census.

## 3. Founded `phi` is a direction, not a response selector

In a supplied local realization the founded reciprocal generator is

```text
H=diag(-1,+1,0,0),       tr(H)=0.
```

Its induced metric tangent is

```text
T_H=H^T eta+eta H=diag(2,2,0,0).
```

The volume response is proportional to `g^{-1}`. Its reciprocal-direction pairing is

```text
(1/2) eta:T_H = 0.
```

This is the determinant-one reciprocal cancellation: a pure volume response is blind to the founded
`phi` direction. But an anisotropic symmetric response, for example the registered algebraic control
`diag(1,0,0,0)`, pairs to `2`. Hence founded `phi` does not make every response blind and does not
choose the response that sees it.

The correct chain rule is:

```text
R_phi = alpha_E(H)
```

after a physical local realization has been supplied or derived. `phi` is not an independent
eleventh field and it does not generate an independent scalar equation. The choice of `E` remains
upstream.

## 4. Multiple metric-natural variational responses survive covariance

For a local scalar functional

```text
S_f = integral sqrt(|g|) f(R),
```

inverse-metric variation has constant-curvature bulk coefficient

```text
E_f = [R f'(R)/4 - f(R)/2] g
```

on a four-dimensional constant-curvature metric. For `f(R)=R^n`, this becomes

```text
E_n = [(n-2)/4] R^n g.
```

The exact controls give:

```text
n=0: -g/2
n=1: -(R/4)g        (Einstein-Hilbert bulk response on this control)
n=2: 0              (R^2 is stationary on this control)
n=3: +(R^3/4)g.
```

At `R=4,12`, the `n=1` and `n=3` coefficient vectors have determinant `-384`; their response
dependence is inequivalent. This finite control does not classify all `f(R)` theories. It proves
only that general covariance, metric ownership and variationality do not collapse the registered
natural response class to one shape.

The repository's stronger source-backed comparison also survives unchanged: the EH/Einstein bulk
is conditional on post-scale metric-only Lovelock/minimality premises, while the `C^2`/Bach bulk is
unique only in the inactive pre-scale strong-CSN class. On a nonzero constant-curvature metric the
Einstein response is nonzero while the Bach response vanishes. Their conditional zero sets are not
the same.

All scalar metric actions are diffeomorphism covariant and their bulk Euler tensors obey the
associated Noether/divergence identity. Covariance and gauge horizontality therefore do not choose
between them.

## 5. Calibration supplies units but not the missing selector

Let a monomial `c_E^a G_obs^b` be required to have inverse-length-squared dimensions. The exact
dimension equations have coefficient rank two and augmented rank three, so they are inconsistent.
`c_E` and `G_obs` alone cannot manufacture an independent curvature scale such as a cosmological
coefficient without mass, density, length, or another anchor.

This does not restore scale neutrality and does not reject calibrated EH. It says only that the two
observational anchors do not choose every relative coefficient or supply the missing global scale.

## 6. Universal observer queries leave an exact trace ambiguity

For a supplied symmetric ambient tensor `S`, the exact nine-query control imposes

```text
S(u,u)+S(n,n)=0
```

for nine normalized observer/ruler pairs. Its coefficient rank is nine and its one-dimensional
kernel is the metric line. Thus the all-query condition is exactly the trace-free reduction already
banked by the universal-query audit.

This has two consequences here:

1. an all-query rule does not choose which metric functional supplies `S[g]`; and
2. it cannot see the metric-proportional response component.

Observer Reciprocity therefore constrains covariance and query treatment but does not close the
response selection.

## 7. Regular reductions and global objects do not repair the selection gap

A metric-derived regular projector or reciprocal/screen split can pull a parent response into
branch components by the chain rule. It cannot select the parent response, and the current split
does not continue uniquely through null, tie, round, degenerate and rank-change strata.

Holonomy and period objects are genuine global metric data, but the composition audit proves that
concatenation does not select a zero-period or trivial-return equation. Boundary/completion data
change legal endpoint jets, but no current source supplies the boundary polarization or a map from
those data to one bulk response. Bootstrap supplies a coherent two-arrow type only; its nontrivial
membership relation is still absent.

## 8. Exact bounded conclusion

Within the preregistered classes:

```text
NONZERO_COVARIANT_RESPONSE_FORMS_ARE_MATHEMATICALLY_AVAILABLE;
THE_COMPLETE_COFRAME_PULLS_THEM_BACK_FAITHFULLY;
FOUNDED_PHI_AND_UNIVERSAL_QUERY_STRUCTURE_CONSTRAIN_THEIR_COMPONENTS;
NO_ACTIVE_FOUNDATIONAL_PREMISE_SELECTS_ONE_RESPONSE_DERIVATIVE_ORDER_COEFFICIENT
QUERY_QUANTIFIER_BOUNDARY_COMPLETION_OR_GLOBAL_LOCAL_RELATION.
```

This is a selection result, not an impossibility theorem over future UDT principles or all natural
operators.
