# Exact derivation — zero-order pair-chord network descent

Date: 2026-08-12

Status: **INTERNALLY DERIVED AND INDEPENDENTLY REPLAYED; FRESH ADVERSARIAL REVIEW PENDING**

## 1. Result first

For the endpoint terminal channels, chords are conditionally sufficient. No derivative or
time-live law is required merely to compose the unique terminal states of one common calibrated
family.

Two different structures had been superposed:

1. positive-semidefinite Gram reachability is a directed partial order; it is not Reciprocity and
   has no nontrivial reverse;
2. the calibrated endpoint transition is an invertible upper-triangular groupoid arrow; it
   composes, reverses, and carries the additive reciprocal character exactly.

The first describes how one base-plus-orchestra presentation can lie above another. The second
describes the reversible comparison of their calibrated endpoint states. Keeping them separate
removes the apparent conflict between positive Gram addition and observer Reciprocity.

## 2. Complete A-terminal state space

Every regular A-calibrated Lorentzian terminal chord has the unique form

```text
h(T,L,beta)
  =-T^2(dy0+beta dy1)^2+L^2(dy1)^2,
T>0, L>0.
```

Define its positive upper-triangular terminal coframe

```text
B(T,L,beta)=[[T,T beta],[0,L]],
eta=diag(-1,+1).
```

Then

```text
h=B^T eta B.                                      (1)
```

Conversely, every symmetric `2 x 2` form with `h00<0` and `det h<0` reconstructs uniquely

```text
T=sqrt(-h00),
beta=h01/h00,
L=sqrt(h11-h01^2/h00).                            (2)
```

Thus the declared terminal-state space is in bijection with the group of positive
upper-triangular `2 x 2` matrices. This uniqueness is in the fixed A calibration. A Lorentz change
of the calibration axis changes the representative and is outside the claimed invariance.

## 3. Reversible endpoint-comparison groupoid

For two states `i` and `j`, define

```text
R_ij=B_j B_i^-1.                                  (3)
```

Exactly,

```text
R_ij=
[[T_j/T_i, T_j(beta_j-beta_i)/L_i],
 [0,       L_j/L_i]].                             (4)
```

For three literally matched endpoint states,

```text
R_jk R_ij=B_k B_j^-1 B_j B_i^-1=R_ik,             (5)
R_ji=R_ij^-1,
R_ii=I.
```

This is the endpoint pair groupoid represented in the positive upper-triangular group. Equation
(5) is exact because the same `B_j` is used as the target of the first arrow and source of the
second. It does not assert that an independently supplied direct path arrow must equal a composed
path arrow.

### 3.1 Common-scale and reciprocal characters

Write

```text
kappa=(1/2)log(TL),
phi=(1/2)log(L/T).
```

Then

```text
det R_ij=(T_j L_j)/(T_i L_i)=exp[2(kappa_j-kappa_i)],          (6)

(R_ij)_11/(R_ij)_22
   =(T_j/L_j)/(T_i/L_i)
   =exp[-2(phi_j-phi_i)].                                     (7)
```

Therefore

```text
Delta kappa_ij=(1/2)log det R_ij,
Delta phi_ij=-(1/2)log[(R_ij)_11/(R_ij)_22]                   (8)
```

compose additively and reverse sign. On the conditional terminal interpretation,

```text
(c_eff_j/c_E)/(c_eff_i/c_E)=exp[-2 Delta phi_ij].             (9)
```

`c_E` calibrates the dimension-matched endpoint states but cancels from the relative network
character. It supplies no path, branch, or material signal law.

### 3.2 The shift channel

The endpoint coordinate difference telescopes in one common A calibration:

```text
(beta_j-beta_i)+(beta_k-beta_j)=beta_k-beta_i.                 (10)
```

But the off-diagonal transition entry is not additive. For upper-triangular matrices

```text
[[e,f],[0,g]] [[a,b],[0,d]]
  =[[ea, e b+f d],[0,gd]].                                    (11)
```

Equation (11), not addition of the raw matrix shear, is the complete zero-order composition law.
The shift difference is also calibration-dependent; it is not promoted to an arbitrary-frame
scalar.

## 4. Positive Gram reachability is a partial order

On the same fixed pair-domain vector space define

```text
h_i <=_G h_j  iff  P_ij=h_j-h_i is positive semidefinite.     (12)
```

Using the `i`-shifted covector basis, (12) is exactly equivalent to

```text
0<T_j^2<=T_i^2,
L_j^2>=L_i^2,
(T_i^2-T_j^2)(L_j^2-L_i^2)
  >=T_i^2 T_j^2 (beta_j-beta_i)^2.                            (13)
```

This is the parent reachability theorem rebased at an arbitrary terminal state.

The relation is:

- reflexive because `P_ii=0`;
- transitive because

  ```text
  P_ik=(h_k-h_j)+(h_j-h_i)=P_jk+P_ij>=0;                      (14)
  ```

- antisymmetric because a symmetric matrix that is both positive and negative semidefinite is
  zero, and the A-terminal decomposition is unique.

It is therefore a partial order, not a groupoid. If `h_i<_G h_j`, the reverse increment is
negative semidefinite and cannot also be an allowed nonzero Gram addition. Any directed loop

```text
h_0<=_G h_1<=_G ... <=_G h_0
```

is consequently constant. Positive Gram reachability cannot itself be observer Reciprocity.

## 5. Rank composition

For positive-semidefinite increments,

```text
ker(P_ij+P_jk)=ker(P_ij) intersect ker(P_jk).                  (15)
```

The proof is immediate from

```text
v^T(P_ij+P_jk)v=0
```

and nonnegativity of each summand. In two dimensions this gives the full rule:

- adding rank zero changes nothing;
- if either increment has rank two, the total has rank two;
- two rank-one increments remain rank one when their kernels coincide;
- two rank-one increments with distinct kernels produce rank two.

There is no positive-semidefinite rank cancellation. The cumulative orchestra may stay on one
rank-one direction or fill the two-dimensional interior.

## 6. How the order and groupoid coexist

Every ordered endpoint pair has the invertible transition `R_ij`, whether or not its two terminal
forms are Gram-comparable. On the ordered subset `h_i<=_G h_j`, equation (13) further gives

```text
phi_j>=phi_i,
(c_eff_j/c_E)/(c_eff_i/c_E)<=1,                 (16)
```

strictly for a nonidentity increment. Reversing the observer order uses `R_ji=R_ij^-1` and changes
the sign of `Delta phi`; it does not pretend that `h_i-h_j` is another positive Gram addition.

This is the simple conceptual join:

```text
PSD orchestra increment  = directed construction/order statement;
calibrated endpoint ratio = reversible observer-comparison statement.
```

No contradiction remains once they are not assigned the same type.

## 7. When chords are sufficient

If one common calibrated family assigns exactly one terminal state `B_A`, `B_B`, `B_C`, ... to
each network object, then the zero-order chord data suffice for its endpoint channels:

```text
R_AB=B_B B_A^-1,
Delta phi_AB=phi_B-phi_A,
Delta kappa_AB=kappa_B-kappa_A.
```

All scalar triangle periods vanish and all endpoint matrices telescope. Derivatives, time-live
evolution, and a new scalar reset law are unnecessary for this conditional endpoint descent.

This does not erase other channels. A normal connection, Jacobi map, path holonomy, or extrinsic
embedding datum is not reconstructible from the zero-order chord. Such data may remain genuinely
path- or query-labelled.

## 8. Independently rebuilt middle states

Suppose an `A-B` tape ends at `B_in` while a separately constructed `B-C` tape begins at `B_out`.
The valid composite needs

```text
M_B=B_out B_in^-1,
R_AC=R_BC M_B R_AB.                              (17)
```

Omitting `M_B` silently identifies different objects. Neither local `c_E` calibration nor the
terminal chord theorem supplies that identification. Thus chord sufficiency is conditional on a
common calibrated state assignment; it does not select the physical global family.

Likewise, an independently supplied direct path arrow may differ from the endpoint ratio by
holonomy. Equation (5) is endpoint descent, not a theorem that all physical paths are equivalent.

## 9. Boundaries and degeneracies

The endpoint groupoid is defined on the regular A-terminal stratum `T,L>0`. At `T=0`, the chosen
A-clock line is null and the terminal coframe is noninvertible, so (3) is unavailable. The full
pair form may nevertheless remain Lorentzian when off-diagonal content survives. Nothing in this
network theorem identifies that chart boundary with physical `X_max`, a horizon, or a global end.

## 10. Exact evidence

The production route passes 15 symbolic identities and exhausts a deterministic rational family:

```text
terminal states                         100
all ordered endpoint pairs              10,000
PSD ordered pairs                       1,698
  identities / rank one / rank two      100 / 358 / 1,240
incomparable pairs                       8,302
PSD chains                              10,518
  zero / one / two nonidentity edges    100 / 3,196 / 7,222
total ranks zero / one / two            100 / 1,016 / 9,402
nontrivial PSD reverses                  0
nontrivial directed loops                0
```

A hermetic standard-library `Fraction` route uses a different 64-state family and imports no
production code or result:

```text
all endpoint pairs                       4,096
all matched endpoint triples checked     262,144
PSD ordered pairs                        786
PSD chains                               3,955
inverse checks                           4,096
character checks                         8,192
strict phi-order checks                  722
nontrivial PSD reverses / loops           0 / 0
explicit missing-middle witness          passed
```

Eleven hostile controls catch the major type and algebra regressions.

## 11. Exact bounded landing

```text
EXACT_ZERO_ORDER_CHORD_NETWORK_CLASSIFICATION_ON_ONE_COMMON_A_CALIBRATED_TERMINAL_FAMILY__
THE_UNIQUE_TERMINAL_COFRAMES_DEFINE_INVERTIBLE_UPPER_TRIANGULAR_ENDPOINT_TRANSITIONS__
TRANSITIONS_COMPOSE_REVERSE_AND_CARRY_EXACT_COMMON_SCALE_AND_RECIPROCAL_CHARACTERS__
PSD_GRAM_REACHABILITY_IS_A_PARTIAL_ORDER_WITH_NO_NONTRIVIAL_REVERSE_OR_DIRECTED_LOOP__
THUS_PSD_ADDITION_IS_NOT_RECIPROCITY__CHORDS_ARE_SUFFICIENT_FOR_CONDITIONAL_ENDPOINT_DESCENT__
INDEPENDENT_MIDDLE_CALIBRATION_PHYSICAL_RELATION_FAMILY_PATH_CHANNELS_AND_GLOBAL_OWNERSHIP_REMAIN_
OPEN__NO_DERIVATIVE_HISTORY_ACTION_SOURCE_MATTER_BOOTSTRAP_XMAX_COSMOLOGY_SIGNAL_OR_DYNAMICS_IS_
DERIVED.
```
