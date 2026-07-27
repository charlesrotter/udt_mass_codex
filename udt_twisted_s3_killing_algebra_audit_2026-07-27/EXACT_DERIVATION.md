# Exact derivation — full Killing algebra of a complete twisted reciprocal configuration

## Status and premise stamps

This is a metric-configuration existence result, not a selected UDT solution.

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

## 1. Complete metric and explicit global profile

Use the registered global coframe on `M=R x S3`, with unit-quaternion Maurer-Cartan forms:

```text
tau = c_E dt + a sigma_3,
theta_0 = exp(-phi) tau,
theta_1 = R exp(phi) sigma_3,
theta_2 = R exp(lambda phi) sigma_1,
theta_3 = R exp(lambda phi) sigma_2,
g = -theta_0^2 + theta_1^2 + theta_2^2 + theta_3^2.
```

For one exact Category-A witness, set units `c_E=R=1`, and choose

```text
a=1/10,  lambda=2/3.
```

Let `(w,x,y,z)` be the global embedding coordinates of the unit `S3`. The profile is the restriction
of the following ambient polynomial:

```text
400 phi = x+2y+3z+4xy+5yz+6zx+7x^2+11y^2+13z^2
          +17xyz+19x^3+23y^3+29z^3.
```

It is therefore globally smooth. Since every embedding coordinate and every displayed monomial has
absolute value at most one,

```text
|phi| <= 140/400 = 7/20.
```

The strict `t=constant` slice condition is

```text
exp(2phi)-a^2 exp(-2phi)
 = exp(-2phi)[exp(4phi)-1/100] > 0.
```

Indeed `phi>=-7/20`, so `exp(4phi)>=exp(-7/5)>1/100`. The global coframe is nonsingular and gives
Lorentz signature everywhere. Thus this has complete **global spatial/coframe coverage** on
`R x S3`, not a local cap or an unextended coordinate jet. Lorentzian geodesic completeness is a
different property and is neither needed nor claimed here.

## 2. Intrinsic rank certificate

Define the three scalar polynomial curvature invariants

```text
I1 = R,
I2 = trace[(Ric^a_b)^2],
I3 = trace[(Ric^a_b)^3].
```

In the north-pole chart, the exact third metric jet suffices to obtain the first spatial derivatives
of all three invariants: curvature uses two metric derivatives and its gradient uses three. The
primary SymPy calculation keeps exact rationals and finds at `(x,y,z)=(0,0,0)`:

```text
d(I1,I2,I3)/d(x,y,z) =
[-1648731/4000000,             -2823943/6000000,             -1342193/4000000]
[-14675109230869/5760000000000,-2838215263223/960000000000, -5257543404469/1920000000000]
[-6884057597873547527/921600000000000000,
 -1334199641416668509/153600000000000000,
 -7536697493832806581/921600000000000000].
```

Its exact determinant is

```text
330801319823081673814309577 / 159252480000000000000000000000 != 0.
```

Continuity makes the rank three on a nonempty open neighborhood. This statement is intrinsic: a
Killing field preserves every scalar polynomial curvature invariant.

## 3. Why this solves the unrestricted Killing problem

Let `X` be any Killing field, with arbitrary time dependence and arbitrary mixed components. On the
rank-three neighborhood,

```text
X(I_A)=0, A=1,2,3.
```

The invariants are stationary and their three spatial gradients are independent, so every spatial
component of `X` vanishes there. Hence `X=f partial_t` on that neighborhood. Since
`K=partial_t` is Killing and `g(K,K)=-exp(-2phi)` is nonzero,

```text
L_(fK) g = df tensor K_flat + K_flat tensor df = 0
```

forces both `K(f)=0` and every derivative orthogonal to `K` to vanish. Thus `f` is constant there.

For `Y=X-fK`, both `Y` and its first covariant derivative vanish at an interior point. The Killing
identity

```text
nabla_a nabla_b Y_c = R_cb a d Y^d
```

is a finite-type linear propagation equation. Along geodesics, zero initial data remain zero; broken
geodesics extend the result across the connected manifold. Therefore

```text
Kill(g) = span_R{partial_t}
```

for this complete configuration. This includes and rules out hidden time-dependent, time-space-mixed,
and non-split-preserving Killing fields.

## 4. The depth and ruler occur in the same metric

Because the stationary line is now intrinsic and unique,

```text
g(K,K) = -c_E^2 exp(-2phi),
delta_K(p,q) = log[sqrt(-g(K,K))_p/sqrt(-g(K,K))_q]
             = phi(q)-phi(p).
```

The explicit `phi` is nonconstant, so the depth is nontrivial. The previously verified exact twist
identity applies without changing configuration:

```text
star(K_flat wedge dK_flat)
 = plus_or_minus (c_E^2 a kappa/R^2) exp[-(3+2lambda)phi] theta_1.
```

Here `a=1/10` and the displayed unit-quaternion convention has `kappa=-2`; hence the twist is
nonzero and selects the **unoriented** `theta_1` ruler line. The founded inverse clock/ruler weights
therefore coexist with the unique stationary line in one complete smooth metric.

## 5. Exact degeneracy controls

- `a=0`, with the same global profile and `lambda=2/3`, still has a nonzero invariant-gradient
  determinant, hence a one-dimensional Killing algebra, but its twist ruler vanishes.
- `lambda=0` and `lambda=1`, with `a=1/10` and the same profile, each have a nonzero exact rank
  determinant. Neither value alone forces an extra Killing symmetry.
- With `lambda` left symbolic for this fixed profile, the determinant is a nonzero ninth-degree
  polynomial. It has isolated real roots (recorded in `SYMBOLIC_LAMBDA_RESULT.json`). At those roots
  this particular three-invariant certificate is **inconclusive**; a zero determinant neither proves
  nor suggests an additional Killing field without another certificate or the full Killing PDE.
- If `phi` is constant, the metric coefficients in the global Maurer-Cartan coframe are constant.
  The three-dimensional left action preserves the coframe and metric. Together with `K`, the Killing
  algebra has dimension at least four, so the timelike line is not unique.
- More generally, a continuous left-action stabilizer of the complete profile/coframe data supplies
  an independent spatial Killing field. Compactness then makes `K+epsilon Y` timelike for all
  sufficiently small `epsilon`, so multiple timelike Killing lines exist.
- At equality or failure of the strict slice inequality, the configuration is not admitted as the
  regular witness established here.

## 6. What is and is not closed

Closed, exactly:

- the registered family contains a complete smooth twisted configuration whose **full** Killing
  algebra is exactly one-dimensional;
- in that same configuration the norm depth is nonconstant and the twist ruler is nonzero;
- constant and continuously symmetric profile strata remain nonunique;
- twist-free uniqueness does not create a ruler;
- `lambda=0` and `lambda=1` do not automatically create hidden symmetry for the tested profile.

Still open:

- classification at the exceptional real roots of the fixed-profile determinant, and of every
  smooth profile;
- selection of the explicit profile, `a`, `lambda`, `R`, topology, or stationary branch;
- any action, EOM, source, carrier, boundary functional, density/bootstrap closure, mass, `X_max`,
  dynamics, signalling law, or observation model.

Thus the earlier same-branch existence gap is closed only at the configuration level. UDT has not
yet supplied the law that chooses this member of the available metric family.
