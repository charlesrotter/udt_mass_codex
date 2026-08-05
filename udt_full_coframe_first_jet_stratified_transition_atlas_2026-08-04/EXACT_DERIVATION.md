# Exact derivation — full first jets and stratified transitions

## 1. Every metric first jet survives

At any invertible coframe value, use frame/coordinate presentation to evaluate the differential at
`theta=I`. For each spacetime direction `mu`, write

```text
X_mu = partial_mu(theta) theta_inverse,
partial_mu(g) = X_mu^T eta + eta X_mu.
```

The exact map from the sixteen entries of `X_mu` to the ten symmetric entries of
`partial_mu(g)` has rank `10` and nullity `6`. The kernel is precisely

```text
X_mu^T eta + eta X_mu = 0,
```

the local Lorentz-presentation algebra. Taking all four derivative directions gives

```text
64 coframe-jet components -> 40 metric-jet components,
rank 40, nullity 24.
```

No spatial jet was frozen. A local construction

```text
theta(x)=I+x^mu X_mu
```

realizes arbitrary prescribed first jets near the base point, so first-jet realizability imposes no
additional equation.

An exact rank-ten physical tangent basis separates:

```text
1 founded reciprocal direction H,
2 other base-metric directions,
3 screen-metric directions (area and two shears),
4 base-screen mixing directions.
```

The founded generator `H=diag(-1,+1,0,0)` induces
`T_H=diag(2,2,0,0)`. Its coefficient is not fixed by the kinematics.

## 2. The reciprocal causal class is jointly angular

In the exact factorized witness, let

```text
A=diag(exp(-phi),exp(+phi)),
E=[[A,0],[Q S,Q]],
g=E^T eta E,
```

with invertible screen coframe `Q` and arbitrary mixing `S`. Split a coordinate depth covector as
`p=(p_base,p_screen)`. Exact block inversion gives

```text
u = A^-T (p_base-S^T p_screen),
v = Q^-T p_screen,
s_phi = g^-1(p,p) = u^T eta_base u + v^T v.
```

This is the precise reciprocal–angular “orchestra” joint. It is not an added coupling: it is the
inverse of the complete metric.

Hold `phi=0`, `p=(1,0,1,0)`, and `Q=I` fixed. Three exact mixing matrices give

```text
s_phi = -3, 0, +1.
```

Thus mixing alone moves the same coordinate `dphi` through timelike, null, and spacelike classes.
Now hold `S=0` and use unit-determinant screen shears

```text
Q=diag(2,1/2), I, diag(1/2,2).
```

Their screen areas are identical, yet

```text
s_phi = -3/4, 0, +3.
```

Angular shape alone can therefore change the depth-gradient causal class. This does not select a
profile or dynamics; it proves that a frozen or round angular screen can hide genuine transition
structure.

## 3. Nonzero-null transition: the line survives, normalization fails

In the exact Minkowski control take

```text
p(lambda)=(1,lambda,0,0),
s(lambda)=lambda^2-1.
```

At `lambda=1`, `p` is nonzero null and `ds/dlambda=2`. The covector `p`, its sharp vector
`p_sharp=(-1,1,0,0)`, and the unnormalized tensor `p_sharp tensor p` remain finite and nonzero.
But the normalized mixed projector

```text
P=p_sharp tensor p / s
```

has the entry

```text
P^0_0=-1/[(lambda-1)(lambda+1)],
```

with a simple pole. The complete metric can pass smoothly through this causal transition while the
normalized reciprocal/screen reduction cannot.

## 4. Zero-gradient transition has no path-independent projector

Approach `p=0` along the timelike path `lambda(1,0,0,0)` or the spacelike path
`lambda(0,1,0,0)`. Away from zero, the normalized projectors are constant, but their limits are
respectively the time-axis and space-axis projectors. They are unequal.

Therefore the zero-gradient point retains no direction from first-jet data and has no universal
path-independent normalized-projector continuation. Higher jets or a separate global rule may
resolve a particular branch; first-jet kinematics does not.

## 5. Rank loss is a different stratum from a null depth gradient

For any coframe,

```text
det(g)=det(eta) det(theta)^2=-det(theta)^2.
```

The exact path

```text
theta(lambda)=diag(1,1,1,lambda)
```

gives

```text
g=diag(-1,1,1,lambda^2),
det(g)=-lambda^2,
g_inverse_33=lambda^-2.
```

At zero the metric and coframe have rank three. The inverse metric and Levi-Civita construction are
lost. The polynomial adjugate remains finite with limit `diag(0,0,0,-1)`, but choosing the
adjugate—or any generalized connection—as fundamental would be additional architecture, not a
consequence of the current metric theory.

The rank-`<=r` varieties in a four-by-four coframe have codimensions `1,4,9,16` for
`r=3,2,1,0`. In the two-by-two screen block the rank-`<=1` and zero varieties have codimensions
`1,4`. Because `det(E)=det(Q)` in the factorized chart, screen rank loss is full-coframe rank loss,
not merely a harmless angular coordinate event.

The founded reciprocal pair itself has determinant one for every finite `phi`, and its two-metric
has determinant `-1`. Finite `phi` does not cause rank loss. At `phi -> +/- infinity`, individual
fixed-chart components vanish/diverge and no finite nondegenerate fixed-chart tensor limit exists;
that limit alone does not derive `X_max` or a physical endpoint.

## 6. The intrinsic symmetry algebra changes at the causal strata

Solving the exact Lorentz-algebra stabilizer equations gives:

| `dphi` stratum | stabilizer | dimension | Killing rank | inertia `(+, -, 0)` |
|---|---|---:|---:|---:|
| timelike | `so(3)` | 3 | 3 | `(0,3,0)` |
| spacelike | `so(1,2)` | 3 | 3 | `(2,1,0)` |
| nonzero null | `iso(2)` | 3 | 1 | `(0,1,2)` |
| zero | `so(1,3)` | 6 | 6 | `(3,3,0)` |

The three nonzero strata all have stabilizer dimension three, but their algebra types differ. The
null stratum is a genuine non-semisimple contraction with two Killing-null directions; the zero
stratum restores the full six-dimensional Lorentz stabilizer. This is intrinsic stratified
geometry, not a selection of the null branch.

## 7. Why this still is not time evolution

The Maurer–Cartan relation differentiates the first-jet matrices and therefore begins at second-jet
order. For an actual coframe it is an identity. At one point every set of four `X_mu` is realized by
the local construction above. Hence the complete first jet supplies zero kinematic evolution
constraints.

A physical time-live solve still needs a parent bulk operator, its constraints, a boundary/global
completion, and a statement of which configurations are varied. Calling an arbitrary
configuration-space path “time evolution” would import precisely the missing law.

## 8. Exact bounded conclusion

The first-jet atlas is richer than the smooth supplied-split audit because it releases every metric
jet and proves exact angular/mixing control of the `dphi` causal strata. It also locates the objects
that survive: the unnormalized founded covector and its sharp vector survive a nonzero-null crossing,
while normalized reduction fails; at full rank loss even the inverse metric is gone.

None of these kinematic transition facts selects a physical path. Therefore:

```text
DERIVED_FULL_METRIC_FIRST_JET_SURJECTION;
DERIVED_JOINT_RECIPROCAL_ANGULAR_CAUSAL_STRATA;
NORMALIZED_REDUCTION_HAS_NO_UNIVERSAL_STRATIFIED_EXTENSION;
NO_KINEMATIC_EVOLUTION_RETURN.
```
