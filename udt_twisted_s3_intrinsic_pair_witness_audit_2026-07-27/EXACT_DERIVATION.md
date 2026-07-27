# Exact derivation — one complete intrinsic clock/ruler configuration

## 1. Premise boundary

The calculation carries, but does not use as a field equation, the following stamps:

```text
COPRESENCE = WORKING_INTERPRETIVE_FRAME
METRIC_CAUSAL_STRUCTURE = DERIVED_CONDITIONAL
INSTANTANEOUS_OPERATIONAL_ACCESS = NOT_DERIVED
COMPLETE_WHOLE_SOLUTION_LAW = OPEN
```

Accordingly, the result below is a statement about complete metric configurations. It remains true
whether the configurations are read as globally co-present candidates or simply as stationary
Lorentzian geometries. Nothing below supplies a signal equation or makes a configuration on shell.

## 2. Global complete family

Use unit-quaternion coordinates `q=(q0,q1,q2,q3)` on `S3` and the global left Maurer-Cartan forms
`sigma_i`. The independent exact coframe verifier obtains

```text
sum_i q_i^2 = 1,
det(sigma_i/dx_j) = 8/(1+r^2)^3,
d sigma_1 = -2 sigma_2 wedge sigma_3,
d sigma_2 = -2 sigma_3 wedge sigma_1,
d sigma_3 = -2 sigma_1 wedge sigma_2.
```

The finite determinant is a stereographic-chart statement; the Maurer-Cartan definition is global
and supplies the second chart at the omitted pole.

For the frozen smooth global profile `phi=epsilon f(q)`, define

```text
theta_0 = exp(-phi) (dt+a sigma_3),
theta_1 = exp(+phi) sigma_3,
theta_2 = exp(lambda phi) sigma_1,
theta_3 = exp(lambda phi) sigma_2,
g = -theta_0^2+theta_1^2+theta_2^2+theta_3^2.
```

Relative to `(dt,sigma_3,sigma_1,sigma_2)`, the coframe determinant is
`exp(2 lambda phi)`, and the metric determinant is `-exp(4 lambda phi)`. They never vanish for a
finite smooth `phi`.

The coefficient of `sigma_3^2` on a `t=constant` slice is

```text
exp(2phi)-a^2 exp(-2phi).
```

The frozen polynomial obeys `|f|<=29`. Hence C01–C07 have `|phi|<=29/50<1`. For the twisted
candidates, `a^2=1/4096`. Since `e<3`,

```text
exp(4phi) > exp(-4) > 1/81 > 1/4096=a^2.
```

Thus every frozen displayed slice is globally spacelike; this was not inferred from the north-point
certificate.

## 3. Exact invariant gradients

Let

```text
I1 = scalar curvature,
I2 = Ricci_ab Ricci^ab,
I3 = Riemann_abcd Riemann^abcd.
```

`exact_invariant_jets.py` expands the complete four-metric through total spatial degree three at the
north-chart event. That order is sufficient: a curvature invariant uses two metric derivatives, and
its first gradient uses three. The calculation then:

1. exactly inverts the metric jet;
2. forms the Levi-Civita connection through degree two;
3. forms the full four-dimensional Riemann tensor through degree one;
4. checks connection symmetry, Riemann antisymmetry and pair symmetry, and Ricci symmetry;
5. performs complete Lorentzian contractions; and
6. records the exact rational `3 x 3` spatial-gradient matrix.

The exact determinants are in `CANDIDATE_OUTCOMES.tsv`. They are nonzero for C01–C07 and zero for
the constant-depth control C08. In particular all six nonzero-twist candidates C01–C06 have rank
three. No floating tolerance enters that ruling.

The independent implementation uses nested Torch automatic differentiation and a direct full-index
Riemann contraction. It imports no production geometry module. Across all eight candidates its
largest gradient discrepancy from the exact fractions is `1.2434497875801753e-14`, and its largest
determinant discrepancy is `2.2737367544323206e-13`.

## 4. Why rank three makes the clock line intrinsic

Let `K=partial_t`. Every coefficient is stationary, so `K` is Killing, and

```text
g(K,K)=-exp(-2phi)<0.
```

The invariants are stationary, hence `dI_j(K)=0`. At the certificate event, the three exact
independent covectors `dI_j` have a one-dimensional common kernel. Since that kernel contains `K`, it
is exactly the line spanned by `K`.

Every Killing field `X` preserves scalar curvature invariants, so

```text
dI_j(X)=0
```

for all three `j`. Therefore `X` at the certificate event is `cK`. Set `Y=X-cK`; then `Y` is Killing
and vanishes at that event.

Let `A=(nabla Y)` there. The Killing equation makes `A` skew with respect to `g`. Because
`L_Y(dI_j)=0` and `Y=0` at the event,

```text
dI_j composed_with A = 0.
```

Thus the image of `A` lies in the common kernel, namely the timelike line `span(K)`. Skewness first
gives `A(K)=0`; it then makes every `A(v)` both proportional and orthogonal to `K`, forcing `A(v)=0`.
Therefore `A=0`.

A Killing field is determined by its value and first derivative: along geodesics it obeys the
Jacobi/Killing-transport equation. Zero initial value and derivative give zero on a normal
neighborhood and then throughout the connected spacetime. Hence `Y=0` and every continuous Killing
field is a constant multiple of `K`.

The full local and global continuous Killing algebra of C01–C07 is therefore exactly one-dimensional.
This is stronger than identifying a convenient stationary coordinate. It also does not require
analytic continuation; connected smooth Killing transport suffices.

## 5. The same clock line selects the ruler

For this same complete metric, the parent exact calculation gives

```text
omega_K = star(K_flat wedge dK_flat)
        = plus_or_minus a kappa exp[-(3+2lambda)phi] theta_1,
```

in the present units, with `kappa=-2`. In C01–C06, `a*kappa` is nonzero everywhere. The twist of the
now-intrinsic clock line therefore spans exactly the reciprocal ruler line `theta_1` in the same
configuration. Its sign remains orientation dependent, so the metric selects an unoriented line,
not an ordered positive spatial direction.

The clock and ruler weights are respectively `exp(-phi)` and `exp(+phi)`. The stationary norm ratio
continues to give the branch depth `phi(q)-phi(p)`. This joins the clock depth and ruler line without
splicing two metrics.

## 6. Controls and exact scope

- C07 has rank-three curvature fingerprints and an intrinsic clock line, but `a=0`; its clock twist
  vanishes and it fails the ruler gate.
- C08 has nonzero `a` but `phi=0`; all three invariant gradients vanish and there is no nontrivial
  reciprocal depth.
- C01–C06 all pass despite six distinct sampled `lambda` values. Configuration existence therefore
  does not select `lambda`.

The result proves that the complete metric family contains all-gate intrinsic-pair configurations.
It does not prove that the frozen profile solves an equation, that UDT selects this topology or
branch, or that any member describes the universe. Action, whole-solution law, boundary selection,
time-live dynamics, matter, signalling, carrier, source, density, bootstrap, mass, physical scale,
and `X_max` remain open or conditional exactly as before.
