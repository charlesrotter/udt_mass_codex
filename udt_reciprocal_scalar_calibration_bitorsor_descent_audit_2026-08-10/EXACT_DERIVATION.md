# Exact derivation — reciprocal scalar/calibration descent through the alignment bitorsor

Date: 2026-08-10

Current grade: **VERIFIED-WITH-CAVEATS**

Preregistered landing:

```text
RECIPROCAL_READOUT_DESCENT_DERIVED__CALIBRATION_MAGNITUDE_NOT_GENERATED
```

## 1. Result first

On every retained regular C01--C06 full-projector stratum, the free middle screen phase is invisible
to each already-defined reciprocal readout in its properly conditional domain:

- the clock-line and clock/ruler-plane density ratios;
- `delta_RF` formed from those ratios;
- the terminal reciprocal log imbalance of a supplied regular calibrated pair metric;
- the reciprocal exponent in the conditional R17 assembly.

This is exact for independent source and target screen rotations, not only for one matched rotation.
Balanced middle-gauge composition preserves the density telescoping law exactly.

The same derivation proves a strict limitation: every carried-to-intrinsic projector alignment is a
Lorentz isometry, so its clock and plane density ratios are both one. It transports a supplied
calibration magnitude but cannot generate a nonzero one. The screen-phase problem is gauge
bookkeeping; the physical non-isometric calibration owner remains open.

## 2. Correct gauge action

At each regular endpoint let

```text
R=(P_u,P_n,H)
```

be the metric-owned clock/ruler/screen projector triple. Its connected stabilizer is

```text
K_R ~= SO(2),
```

acting in the positive screen and fixing the clock line `L_t`, ruler line `L_r`, and Lorentzian
clock/ruler plane `P_tr=L_t+L_r`.

For a supplied complete comparison arrow `A:V_p->V_q`, independent adapted-screen changes act by

```text
A -> A' = h_q A h_p^-1,
h_p in K_p,
h_q in K_q.
```

This is a representation change on the full arrow. It does not set its mixing blocks to zero. If
`A u` has a screen component, `h_q` rotates that component while preserving every metric norm and
Gram determinant used below.

## 3. Density-line descent theorem

Let `F=(u,r)` be any regular basis of `P_tr`, with `u` timelike. Define the positive ratios

```text
rho_1(A,F) = |g_q(Au,Au)| / |g_p(u,u)|,

rho_2(A,F) = |det Gram_q(Au,Ar)| / |det Gram_p(u,r)|.
```

The logarithmic densities in the reciprocal-root audit are

```text
b_1=(1/2) log rho_1,
b_2=(1/2) log rho_2,
delta_RF=(1/2)b_2-b_1.
```

Equivalently,

```text
exp(4 delta_RF)=Q(A,F)=rho_2/rho_1^2.
```

Because `h_p` fixes `P_tr` and `h_q` is a Lorentz isometry,

```text
Gram_q(h_q A h_p^-1 F)=Gram_q(A F).
```

Therefore

```text
rho_1(A',F)=rho_1(A,F),
rho_2(A',F)=rho_2(A,F),
Q(A',F)=Q(A,F),
delta_RF(A',F)=delta_RF(A,F).
```

The proof also covers any discrete sign extension preserving the two lines: the definitions use
absolute norms and Gram determinants. The banked connected stabilizer is `SO(2)`; no stronger global
stabilizer claim is required.

## 4. Terminal pair-metric descent

Restrict the supplied arrow to the clock/ruler pair plane and form the induced metric

```text
h=F^T A^T g_q A F.
```

For source flag `F=(u,r)`, write its source Gram matrix as `s`, and let

```text
rho_1=|h_00|/|s_00|,
rho_2=|det h|/|det s|.
```

The exact identity is

```text
(-det h)/h_00^2
  = Q * |det s|/|s_00|^2.
```

Therefore, in the explicitly normalized reciprocal calibration

```text
|det s|=|s_00|^2,
```

the terminal audit gives

```text
phi_pair=(1/4) log[(-det h)/h_00^2].
```

and its bracket is exactly `Q=rho_2/rho_1^2`. The audit witness has
`s=diag(-1,1)` and satisfies that normalization. Since `h` itself is unchanged by independent
screen stabilizers, the normalized terminal readout descends. An explicit unnormalized witness
with source rescaling `diag(2,3)` gives the required source factor `9/4`, proving that the factor
cannot be silently omitted. This does not construct `A`, `F`, or the pair surface; it proves
invariance after those conditional inputs and the stated source calibration are supplied.

The complete mixed witness

```text
A=[[1/2,0,0,0],
   [0,2,0,0],
   [1/4,0,1,0],
   [0,0,0,1]]
```

keeps the clock-to-screen mixing component `1/4` active. Exact values are

```text
rho_1=3/16,
rho_2=3/4,
Q=64/3,
delta_RF=phi_pair=(1/4)log(64/3).
```

Arbitrary independent source and target screen rotations change the displayed mixed components but
leave the induced pair metric and all four values exactly unchanged.

## 5. Exact composition and path labels

For composable supplied flag arrows `A:F_1->F_2` and `B:F_2->F_3`, norm and area ratios telescope:

```text
rho_k(BA,F_1)=rho_k(B,A F_1) rho_k(A,F_1),  k=1,2.
```

Hence

```text
Q(BA,F_1)=Q(B,A F_1)Q(A,F_1)
```

and `delta_RF` is additive on that correctly typed action groupoid. Under a middle screen change
`h_2`,

```text
A -> h_2 A,
B -> B h_2^-1,
```

so the product is unchanged and each density factor is unchanged. The production derivation proves
this with a noncommuting rational three-arrow witness; the independent verifier reproduces it using
only `Fraction` arithmetic.

This does not erase paths. The 36/36 frozen nonclosing loops remain path-labelled holonomy. Descent
means the scalar does not depend on the arbitrary screen representative *within a fixed path-labelled
arrow*. It does not equate different paths.

## 6. Conditional R17 descent

On each retained stratum,

```text
X_lambda=-P_u+P_n+lambda H.
```

Every screen stabilizer commutes with all three projectors and therefore with `X_lambda` and
`exp(delta X_lambda)`. The coefficient `delta` and the reciprocal clock/ruler exponent consequently
survive screen-gauge changes for all six `lambda` values, including the `lambda=+/-1` grading
degeneracies once the full projector triple is retained.

This is only a descent statement. G42 still controls ownership: R17 is a lawful conditional
assembly, not a branch-selected physical comparison law.

## 7. Why calibration ownership does not follow

Let `M` be any member of the carried-to-intrinsic alignment bitorsor. By construction

```text
M in SO^+(V,g).
```

Therefore, for every regular clock/ruler flag,

```text
rho_1(M,F)=1,
rho_2(M,F)=1,
Q(M,F)=1,
delta_RF(M,F)=0.
```

An isometric alignment can rotate, boost, and identify the two projector reductions. It cannot
produce the non-isometric clock-versus-ruler scale change whose amount is the physical calibration
magnitude. If a supplied comparison arrow already carries that magnitude, the bitorsor transports
it without screen ambiguity. Its origin remains in the still-open physical pair relation,
pair-surface Jacobian, global completion, or another genuinely owned non-isometric object.

No such owner is invented here.

## 8. Scoped landing

The exact bounded landing is

```text
RECIPROCAL_READOUT_DESCENT_DERIVED__CALIBRATION_MAGNITUDE_NOT_GENERATED.
```

It applies to the six retained regular full-projector strata with supplied flags, arrows, pair
metrics, and paths. It does not cover null/degenerate flags, select a physical arrow or scalar law,
derive universal `c_eff`, or infer dynamics, matter, mass, bootstrap closure, `X_max`, CMB physics,
or signalling.
