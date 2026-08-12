# Exact derivation — pair-terminal reachability atlas

Date: 2026-08-12

Status: **DERIVED IN PREREGISTERED ZERO-ORDER SCOPE; ADVERSARIAL REVIEW PENDING**

## 1. Bounded question

Fix one symbolic A-calibrated Lorentzian base pair form and release the entire pointwise Gram
image supplied by the pair-first theorem. Classify every completed signature and every terminal
state reachable while the declared A-clock remains timelike.

This is a local algebraic solution-space result. It does not select a physical metric history,
query, immersion, branch, path, action, source, matter sector, bootstrap rule, `X_max`, SNe, CMB,
or dynamics.

## 2. Remove the base shift without reducing the solution space

Write the fixed base as

```text
h0=-T0^2(dy0+beta0 dy1)^2+L0^2(dy1)^2,
t=T0^2>0,
ell=L0^2>0.
```

The pair-first result supplies

```text
h=h0+P,
P=C^T q C>=0.
```

Use the covector basis `u=dy0+beta0 dy1`, `v=dy1`. Congruence by this invertible shear preserves
the full positive-semidefinite cone. In that basis,

```text
h0=diag(-t,ell),
G=[[p,m],[m,n]]>=0,
h=[[p-t,m],[m,ell+n]],                         (1)
```

where

```text
p>=0,
n>=0,
m^2<=p n.                                      (2)
```

No physical shift was set to zero. The calculation uses an algebraic basis and transforms the
terminal result back to the original A calibration.

## 3. Complete signature atlas

Since `ell+n>0`, the determinant

```text
D=(p-t)(ell+n)-m^2                              (3)
```

classifies the completed two-form:

```text
D<0  : Lorentzian,
D=0  : degenerate with one positive and one zero direction,
D>0  : positive definite.
```

Negative-definite forms cannot occur because the second diagonal entry is positive. More
explicitly:

```text
p<t : always Lorentzian and A-clock timelike;
p=t : Lorentzian when m!=0, degenerate when m=0;
p>t : Lorentzian / degenerate / positive according as
      m^2 is greater than / equal to / less than (p-t)(ell+n).
```

Thus `h00=0` is not synonymous with a degenerate pair form. At `p=t,m!=0`, the completed form is
still Lorentzian, but the chosen A-clock line is null and the A-calibrated terminal decomposition
is unavailable.

## 4. Forward terminal map

On the complete A-calibrated stratum `p<t`, define `A=t-p>0`. Equation (1) gives exactly

```text
T^2=A=t-p,
beta-beta0=-m/A,
L^2=ell+n+m^2/A,                                (4)
det(h)=-T^2 L^2<0.                              (5)
```

Every PSD Gram matrix with `p<t` is therefore terminal-admissible. The determinant condition is
automatic once the A-clock remains timelike.

## 5. Necessary-and-sufficient terminal image

Let

```text
A=T^2,
B=L^2,
Delta=beta-beta0.
```

Solving (4) backward gives the unique shift-removed Gram matrix

```text
G(A,B,Delta)=
[[t-A,              -A Delta],
 [-A Delta, B-ell-A Delta^2]].                  (6)
```

Its determinant is

```text
det G=(t-A)(B-ell)-t A Delta^2.                 (7)
```

Consequently a terminal state is reachable if and only if

```text
0<A<=t,
B>=ell,
(t-A)(B-ell)>=t A Delta^2.                     (8)
```

Necessity follows from (4) and `G>=0`. For sufficiency, (8) makes (6) positive semidefinite;
adding it to `diag(-t,ell)` returns exactly the target pair form. Undoing the shear yields a PSD
Gram matrix in the original calibrated basis. Since the parent theorem proves that every PSD
matrix is `C^T q C`, every state satisfying (8) has a complete-orchestra witness.

## 6. Terminal-coordinate form and exact consequences

Write the base and target terminal densities as

```text
t=exp[2(kappa0-phi0)],
ell=exp[2(kappa0+phi0)],
A=exp[2(kappa-phi)],
B=exp[2(kappa+phi)].
```

Then (8) is the complete nonlinear image in `(kappa,phi,beta)` coordinates. It is not called a
cone. Three immediate projections are exact:

1. `phi>=phi0`. Equality occurs only at the base state. Thus every nonzero PSD addition that
   remains in this A-terminal chart strictly increases reciprocal depth relative to this fixed
   calibrated base.
2. The conditional pair calibration obeys

   ```text
   (c_eff^(pair)/c_E)_target <= (c_eff^(pair)/c_E)_base,
   ```

   with strict inequality away from the base. This remains an observer-pair calibration readout,
   not a local material signal speed.
3. Across the full terminal image, the separate coordinate projections satisfy

   ```text
   kappa in all real numbers,
   beta  in all real numbers,
   phi   in [phi0,infinity).
   ```

   They are not jointly independent; inequality (8) is their exact coupling.

Constructive projection witnesses are simple. For `kappa>=kappa0`, hold `T=T0`, `beta=beta0`
and increase `L`; for `kappa<=kappa0`, hold `L=L0`, `beta=beta0` and decrease `T`. For any real
`Delta`, choose `A=t/2` and `B=ell+t Delta^2`, which saturates (8). For any `phi>=phi0`, hold
`T=T0`, `beta=beta0` and set `L=T0 exp(2 phi)`.

The monotonic statement is an ordering statement. If `P2-P1>=0` and both completed forms remain in
the same A-calibrated chart, then `phi(P2)>=phi(P1)`. An arbitrary parameterized family `P(s)` need
not be monotone in the PSD order, so no monotonicity in an arbitrary profile parameter follows.

The completed form `h`, its inertia, and Gram rank are covariant under invertible pair-domain
congruence. The displayed terminal coordinates `(T,L,beta,kappa,phi)` and inequality (8) are instead
readouts in the declared A calibration. They are not invariants under an arbitrary change of the
observer calibration axis. This is deliberate: the atlas answers a typed observer-A query.

## 7. Rank and boundary strata

Equation (7) gives the exact Gram-rank atlas inside the terminal chart:

```text
rank 0 : A=t, B=ell, Delta=0;
rank 1 : (t-A)(B-ell)=t A Delta^2, excluding the base;
rank 2 : (t-A)(B-ell)>t A Delta^2.
```

Both pure rank-one axes survive:

- `A<t`, `B=ell`, `Delta=0` changes only the clock density;
- `A=t`, `B>ell`, `Delta=0` changes only the ruler density.

Mixed rank-one states saturate the coupled inequality. Rank-two states fill its strict interior.

As `A->0+`, `phi->+infinity` and `c_eff^(pair)/c_E->0`. This is the boundary where the chosen
A-clock density vanishes. At the exact boundary the completed form may be degenerate or remain
Lorentzian, depending on `m`. Nothing here identifies this chart boundary with physical `X_max`,
a horizon, a finite distance, or a global completion.

## 8. Factorization fibers and non-identifiability

For positive `q`, set `K=q^(1/2) C`. A fixed Gram matrix satisfies

```text
K^T K=P.
```

Every factor is represented by

```text
C=q^(-1/2) O P^(1/2),
```

with `O` an orthogonal extension of the polar partial isometry. For fixed positive-definite `P`,
the factors are faithfully parameterized by `O(2)`; rank one retains a stabilizer redundancy in
that parameterization; rank zero forces `C=0`. This algebraic factorization does not identify
every factor as the same physical realization.

Moreover, the pair-first reduction contains

```text
C=S+W,
W=Z Y^-1.
```

For fixed `C`, infinitely many affine decompositions `(S,W)` survive. The terminal pair form hears
their sum; it cannot separately reconstruct ambient mixing and immersion slope.

## 9. Exact evidence

The SymPy route passes 12 exact identities: base shear, Gram shear, completed form, determinant,
clock, shift, ruler, inverse determinant, inverse reconstruction, target determinant, pair-basis
congruence, and screen-frame rotation. Its separately enumerated production rational atlas contains 324
distinct PSD controls:

```text
Gram ranks       : 1 rank-zero, 64 rank-one, 259 rank-two;
signatures       : 231 Lorentzian, 5 degenerate, 88 positive definite;
A-terminal status: 169 true, 155 false.
```

A hermetic stdlib `Fraction` implementation imports no production code and reads no production
artifact. It checks 328 independently generated forward controls, including all ranks and
signatures, plus 146 inverse target reconstructions:

```text
forward ranks      : 1 / 60 / 267;
forward signatures : 325 Lorentzian, 2 degenerate, 1 positive definite;
terminal status    : 322 true, 6 false;
inverse targets    : 12 rank-boundary, 134 rank-interior.
```

Eight hostile controls catch removal of the cross term, reversal of the clock or ruler bounds,
omission of the beta coupling, rank-boundary misclassification, conflation of clock-null with
degenerate, loss of the positive stratum, and failure to prove the uniquely reconstructed zero
Gram matrix at the base.

## 10. Exact bounded landing

```text
EXACT_ZERO_ORDER_PAIR_TERMINAL_REACHABILITY__FOR_ONE_FIXED_SYMBOLIC_A_CALIBRATED_LORENTZIAN_BASE_
THE_FULL_COMPLETE_ORCHESTRA_GRAM_IMAGE_HAS_AN_EXACT_THREE_SIGNATURE_ATLAS__THE_TERMINAL_IMAGE_IS_
NECESSARY_AND_SUFFICIENTLY_DEFINED_BY_0_LT_T2_LE_T02__L2_GE_L02__AND_
(T02-T2)(L2-L02)_GE_T02*T2*(BETA-BETA0)^2__RANK_ZERO_ONE_TWO_ARE_BASE_EQUALITY_INTERIOR__EVERY_
NONZERO_PSD_ADDITION_REMAINING_IN_THE_A_TERMINAL_CHART_STRICTLY_INCREASES_PHI_RELATIVE_TO_THE_
FIXED_BASE__NO_HISTORY_QUERY_BRANCH_
DERIVATIVE_ACTION_SOURCE_MATTER_BOOTSTRAP_XMAX_SNE_CMB_SIGNAL_OR_DYNAMICS_IS_SELECTED.
```
