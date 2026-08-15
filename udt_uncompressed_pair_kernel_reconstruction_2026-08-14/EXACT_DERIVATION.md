# Exact derivation — uncompressed complete-pair evaluator

Date: 2026-08-14  
Scope: local algebraic and first-variation theorem for a supplied complete metric and supplied pair
realization  
Status before external adversarial review: `VERIFIED-WITH-CAVEATS`

## 1. Types first

The complete coframe chart is

```text
E = [[B,   0],
     [Q S, Q]],
```

with

```text
B in GL(2,R),       Q in GL(2,R),       S in Mat(2,R).
```

`B` is the base clock/ruler coframe block. `Q` is a screen coframe. `S` contains four
base-to-screen mixing components.

A supplied regular pair realization has Jacobian

```text
J = [Y; Z],          rank(J)=2,
```

where `Y` and `Z` are its base and screen projections. `Y,Z` belong to the realized observer query,
not to the ambient metric.

The signature matrices are

```text
eta_2 = diag(-1,+1),
eta_4 = diag(eta_2,I_2).
```

The words **supplied complete metric** and **supplied pair realization** are load-bearing. Nothing in
this derivation constructs their histories or selects them as physical.

## 2. The exact uncompressed map

Define

```text
U = B Y,
R = S Y + Z,
A = Q R.
```

Then the complete pair coframe is

```text
V = E J = [U; A].
```

Therefore its first fundamental form is exactly

```text
h = J^T E^T eta_4 E J
  = V^T eta_4 V
  = U^T eta_2 U + A^T A
  = Y^T B^T eta_2 B Y
    + (S Y+Z)^T Q^T Q (S Y+Z).                 (1)
```

The production script proves the residual between the first and last expressions vanishes
entry-by-entry for symbolic `2x2` matrices.

Equation (1) is the no-shortcut form. It retains:

- the base/reciprocal block `B`;
- the screen shape and scale through `Q`;
- all four modern mixing entries through `S`;
- both pair-immersion blocks `Y,Z`.

It also proves that one terminal pair metric is assembled **before** any `phi_pair` or `c_eff`
readout. In that precise conditional sense, the orchestra is internal to the pair relation rather
than added after the redshift or clock ratio is calculated.

## 3. Column form: what every pair component sees

Let `u_0,u_1` be the columns of `U` and `a_0,a_1` the columns of `A`. Then

```text
h00 = <u_0,u_0>_eta + a_0.a_0,
h01 = <u_0,u_1>_eta + a_0.a_1,
h11 = <u_1,u_1>_eta + a_1.a_1.                 (2)
```

Thus angular/screen response does not wait until two different angular directions are compared. It
can modulate the clock/ruler relation of one ordered pair through the norms and inner product of
`a_0,a_1`.

On a single A-calibrated snapshot with invertible `Y`, right-calibrate by `Y^-1` and write

```text
B = [[T,T beta],[0,L]],
W = Z Y^-1,
C = S+W,
a_i = column_i(Q C).
```

If

```text
x = a_0.a_0,
z = a_0.a_1,
y = a_1.a_1,
```

then

```text
h00 = -T^2 + x,
h01 = -T^2 beta + z,
h11 = -T^2 beta^2 + L^2 + y.                  (3)
```

No scalar mixing coefficient has been introduced. `x,z,y` are the three entries of the full screen
Gram matrix for this pair snapshot.

The regular A-clock condition is

```text
T^2 > x.                                      (4)
```

The determinant is

```text
-det(h)
  = (T^2-x)(L^2+y) + x T^2 beta^2 - 2 T^2 beta z + z^2
  = (T^2-x)L^2 + T^2(y-2 beta z+beta^2 x) + (z^2-xy).   (5)
```

Equations (3)--(5) display the complete snapshot interaction among reciprocal scale, base shift,
screen shape, mixing, and pair embedding.

## 4. Terminal reciprocal-`c_E` readout

In dimension-matched A-observer pair coordinates

```text
y^0=c_E tau_A,        y^1=s_A,
```

assume only the terminal regularity conditions

```text
h00<0,        det(h)<0.
```

The unique positive triangular clock/ruler decomposition gives

```text
T_pair^2  = -h00,
beta_pair = h01/h00,
L_pair^2  = h11-h01^2/h00.                    (6)
```

Because

```text
-det(h)=T_pair^2 L_pair^2,
```

the pair depth is

```text
phi_pair
  = (1/2) log(L_pair/T_pair)
  = (1/4) log[(-det h)/h00^2].                 (7)
```

The reciprocal endpoint calibration then reads

```text
c_eff^(pair)/c_E
  = T_pair/L_pair
  = exp(-2 phi_pair)
  = (-h00)/sqrt(-det h).                       (8)
```

Equation (8) is the complete conditional endpoint formula the previous compressed work was trying
to express. By (1), every retained complete-metric and pair-realization channel reaches the one final
ratio through `h`. `c_E` is the observed calibration of the dimension-matched coordinates; it is not
a path selector or a separately appended correction.

On the calibrated snapshot (3), equation (8) becomes

```text
c_eff^(pair)/c_E
 = (T^2-x)
   / sqrt[(T^2-x)(L^2+y)+xT^2 beta^2-2T^2 beta z+z^2].  (9)
```

This is not yet a cosmological or microphysical profile. The functions entering it remain supplied.

## 5. Exact first variation and time-live identity

Let every object vary independently. Direct differentiation gives

```text
delta U = delta B Y + B delta Y,

delta R = delta S Y + S delta Y + delta Z,

delta A = delta Q R + Q delta R,               (10)
```

and

```text
delta h
 = delta U^T eta_2 U + U^T eta_2 delta U
   + delta A^T A + A^T delta A
 = 2 sym(U^T eta_2 delta U + A^T delta A).      (11)
```

For any generic live parameter `lambda`, replace `delta` by a dot. This retains separately

```text
dot B, dot Q, dot S, dot Y, dot Z.              (12)
```

The terminal derivative is

```text
dot phi_pair
 = (1/4) tr(h^-1 dot h) - (1/2) dot h00/h00,   (13)

d/dlambda(c_eff/c_E)
 = -2 dot phi_pair (c_eff/c_E).                 (14)
```

Equations (10)--(14) are exact kinematic identities. They do **not** determine any of the five live
matrix histories. Consequently they do not supply an equation of motion, regime score, or physical
observer-pair assignment.

## 6. Sensitivity result: every input block can matter

One preregistered exact rational witness was evaluated with an independent `E00` perturbation in
each matrix block. It is regular:

```text
h00 = -131543704739/38635833600 < 0,
det(h) = -836141019434549027/91628742965760000 < 0.
```

The exact `dot phi_pair` values were:

| varied block | exact `dot phi_pair` | meaning |
|---|---:|---|
| `B` | `-33028920008308704836397871620 / 109989087380664777943307738953` | base/reciprocal block active |
| `Q` | `16947498911352416709543033019 / 329967262141994333829923216859` | screen geometry active |
| `S` | `32976619891669139675721317145 / 219978174761329555886615477906` | four-component mixing active |
| `Y` | `-61603981750872241682815778328 / 109989087380664777943307738953` | pair base projection active |
| `Z` | `17926538407835482078345353480 / 109989087380664777943307738953` | pair screen projection active |

All are nonzero. The independent Fraction/black-box replay reproduced the decimal values without
importing the production implementation.

At the pure-base symmetric point

```text
Q=I, S=0, Y=I, Z=0,
```

the first derivatives with respect to `Q,S,Z` vanish. This is exact because `A=0` and the screen
contribution `A^T A` begins quadratically. The generic witness proves those zero derivatives do not
mean the sectors are absent. This directly limits the previous quiet-middle interpretation: a quiet
channel at a symmetric point can be a local order-of-variation fact rather than a derived physical
regime law.

## 7. What the Gram reduction preserves

On `det(Y) != 0`, define

```text
W = Z Y^-1,
C = S+W,
q = Q^T Q,
P = C^T q C.
```

Then exactly

```text
Y^-T h Y^-1 = B^T eta_2 B + P.                (15)
```

Therefore `P` is a sufficient compression for the **zero-order A-calibrated pair metric** once
`B` and the calibration are supplied. The earlier endpoint arithmetic based on `P` is not thereby
invalid.

The important correction is that sufficiency for `h` is not ownership of the underlying geometry
or of its history.

## 8. What the Gram reduction erases

### 8.1 Ambient mixing versus pair embedding

For any `D in Mat(2,R)`, set

```text
S' = S+D,
W' = W-D.
```

Then

```text
C'=S'+W'=C,
```

so both `P` and the calibrated pair metric are unchanged. The pair scalar cannot reconstruct how
much of `C` came from ambient coframe mixing and how much came from the chosen pair embedding.

### 8.2 Screen coframe gauge

For `O^T O=I`,

```text
Q' = OQ
```

leaves `q=Q^TQ` and `P` unchanged. This is the expected left screen-frame gauge.

### 8.3 Gram representative fiber

Even at `q=I`,

```text
C' = O C
```

has the same `P=C^TC`. The zero-order pair metric sees lengths and inner products of the two screen
columns, not their absolute screen-frame representative.

### 8.4 Live information

At `q=I,C=I`:

- a stationary path has `dot C=0`, `dot P=0`;
- a symmetric path `dot C=E00` starts from the same `P=I` but has `dot P=2E00`;
- a rotating path with skew `dot C=K` also has `dot P=0` while `dot A=K` is nonzero.

Thus:

1. zero-order `P` does not determine `dot P` or the live pair history;
2. even `(P,dot P)` does not retain rotating screen/coframe motion that may matter to connection or
   holonomy channels, although it is sufficient for `(h,dot h)` at that instant.

This is the precise information-loss theorem. It replaces the vague claim that the Gram reduction
was simply “wrong.”

## 9. The `mu` correction

The present complete-coframe mixing object is

```text
S in Mat(2,R),
```

not a scalar.

The older July object was

```text
mu_old = B_old^2/(A_old^2 b_old^2) > 1,
```

defined in a separate conditional mixed-base seal ansatz. That audit itself concluded the available
lift/cocycle structures did not select its value.

No current source supplies a type-correct map

```text
mu_old -> S, C, P, tr(P), det(P), or an eigenvalue ratio.
```

Nor does complete-pair covariance select a new scalar `mu`. Already on positive-definite `P`, both

```text
tr(P)
```

and

```text
sqrt(det P)
```

are lawful screen-frame invariant scalars, and they are inequivalent: `tr(P)/sqrt(det P)` equals `2`
at `P=I` and `13/6` at `P=diag(4,9)`. Many further invariant functions survive. Without a physical
selection rule, naming one of them `mu` would be an ansatz.

The justified status is therefore

```text
NO_SCALAR_MU_OWNED
```

within the declared algebraic class. This does not prove that no future global or dynamical law can
derive a scalar; it proves the present pair evaluator does not.

## 10. Primary landing and ownership boundary

The preregistered landing reached by production and independent checks is

```text
FULL_UNCOMPRESSED_TERMINAL_EVALUATOR_DERIVED
__NO_SCALAR_MU_OWNED
__PHYSICAL_PAIR_AND_HISTORY_OPEN
```

Premise-stamped meaning:

- `DERIVED CONDITIONAL`: equations (1), (6)--(15) for supplied regular `E,J`;
- `OBSERVED`: `c_E` as the calibration anchor;
- `CONDITIONAL`: complete-coframe chart and supplied pair realization;
- `OPEN`: the physical assignment of `J`, all five live histories, regime dependence, and global
  completion;
- `OPEN/no owner`: a unique scalar `mu`;
- inactive: observations, `X_max`, bootstrap, action, source, and matter carrier.

## 11. What this does and does not repair

It repairs the reciprocal kernel in three ways:

1. the orchestra is carried inside the pair metric before the terminal readout;
2. all metric and pair-realization first derivatives are exposed separately;
3. the two incompatible meanings previously associated with `mu` are separated.

It does not yet provide the “score” that makes different channels louder in different regimes. Such
a score would be a history or admissibility law, not a consequence of differentiating the supplied
matrices.

