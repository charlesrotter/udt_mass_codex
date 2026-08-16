# Exact derivation — G111 nonflat R17 full differential

## 1. Supplied conditional metric

On `R x S3`, use the registered R17 coframe

```text
theta0=u^-1(dt+a sigma3),  theta1=u sigma3,
theta2=v sigma1,           theta3=v sigma2,
u=exp(phi),                v=exp(lambda_R phi).
```

The analytic control profile is `phi(q)=epsilon q0` on unit quaternions. It is
`FREE_AND_EXPLORED`, not a field equation or selected history. The six registered values of
`lambda_R`, both signs of `epsilon` and `a`, all eight preregistered points, and all six axial sky
directions are retained.

## 2. Metric-native geometry

Let `e_a` be the frame dual to the coframe and

```text
[e_a,e_b]=C_ab^c e_c.
```

The Levi-Civita coefficients are obtained from the Koszul formula,

```text
2 <nabla_ea eb,ec>
 = <[ea,eb],ec>-<[eb,ec],ea>+<[ec,ea],eb>.
```

With the noncoordinate-frame correction included, the curvature is

```text
R(ea,eb)ec
 = ea(Gamma_bc^d)e_d-eb(Gamma_ac^d)e_d
   +Gamma_bc^m Gamma_am^d e_d-Gamma_ac^m Gamma_bm^d e_d
   -C_ab^m Gamma_mc^d e_d.
```

The production route constructs these expressions symbolically before substituting any control.
Metricity, zero torsion, both Riemann antisymmetries, pair exchange, and the first Bianchi identity
all vanish exactly. The scalar two-jet obeys the noncommuting-frame relations recorded in
`CORRECTION_RECORD.md`.

## 3. One observer exponential, two distinct differential blocks

For supplied observer tangent `U=e0`, unit celestial direction `n`, and `K=U+n`, the conditional
observer exponential is

```text
F(tau,lambda,n)=Exp_z(tau)[lambda K(tau,n)].
```

Its full differential has pair columns `(F_tau,F_lambda)` and angular columns `F_n`. They share
the same `F` and ambient metric but are not the same matrix.

The observer-time Jacobi field has

```text
J_tau(0)=U,
nabla_K J_tau(0)=nabla_U K =: A.
```

Consequently,

```text
J_tau(lambda)=U+lambda A-(lambda^2/2) R(U,K)K+O(lambda^3).
```

The regular terminal pair metric is the pullback of `g` to `(J_tau,K)`. In particular,

```text
h00(lambda)
 = -1 + 2 lambda <U,A>
   + lambda^2 [<A,A>-<U,R(U,K)K>] + O(lambda^3).
```

The registered A-calibrated terminal formula then gives the local reciprocal readout. In this
normalization its first coefficient is

```text
phi_pair'(0)=<U,A>.
```

This is a pair-block statement. It does not turn the sky map into a terminal strain extractor.

## 4. Angular block

Choose a matched orthonormal screen basis `E_A` at the vertex. The angular Jacobi map obeys

```text
D_sky(0)=0,  D_sky'(0)=I,
D_sky(lambda)=lambda I-(lambda^3/6) T+O(lambda^4),
T_AB=<E_A,R(E_B,K)K>.
```

All 1,152 controls have nonzero `T`. Of these, 1,088 have nonzero cubic shear. Thus the complete
metric's angular and twist sectors are genuinely audible in this bounded nonflat replay; they were
not appended after terminal readout.

## 5. Mixed block and rank theorem

Because `K` is null and the screen is orthogonal to `K`, the canonical projection of the two pair
columns onto the screen has one identically zero column. It therefore has rank at most one. Its
leading nonzero column is

```text
W_A(lambda)=lambda <A,E_A>+O(lambda^2).
```

The same contraction appears in the mixed part of the full differential, and the registered
compatibility residual is exactly zero. This is a joined geometric object without a false
identification of `W_pair` and `D_sky`.

## 6. Bounded result

```text
G110_DISTINCT_BLOCK_FULL_DIFFERENTIAL_SURVIVES_BOUNDED_NONFLAT_ANALYTIC_R17_REPLAY
__PHYSICAL_HISTORY_AND_GLOBAL_WEIGHTS_OPEN
```

This derives a conditional evaluator on supplied controls. It does not select R17, the profile,
an observer population, global branch weights, an observational law, or `X_max`.
