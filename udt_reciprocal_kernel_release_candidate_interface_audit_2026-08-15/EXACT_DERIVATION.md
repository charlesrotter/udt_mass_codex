# Exact derivation — reciprocal-kernel release-candidate interfaces

Date: 2026-08-15  
Status: `INTERNALLY_VERIFIED_WITH_CAVEATS`; fresh semantic review owed

## 1. One complete conditional pipeline

For every supplied regular state,

```text
E=[[B,0],[Q S,Q]],       J=[Y;Z],
U=BY,                    A=Q(SY+Z),
h=J^T E^T eta_4 E J=U^T eta_2 U+A^T A.             (1)
```

On `h00<0`, `det h<0`, the unique positive A-calibrated terminal state is

```text
T_pair^2=-h00,
beta_pair=h01/h00,
L_pair^2=h11-h01^2/h00,
Bpair=[[T_pair,T_pair beta_pair],[0,L_pair]],
h=Bpair^T eta_2 Bpair.                               (2)
```

The endpoint reciprocal readout is

```text
phi_pair=(1/2)log(L_pair/T_pair),
c_eff^(pair)/c_E=T_pair/L_pair=exp(-2 phi_pair).     (3)
```

Equations (1)--(3) form the release-candidate kernel. There is no separate `mu`, angular, or Gram
correction after (3). Every complete channel enters through (1) before the terminal decomposition.

The primary harness supplies three dense rational states. Every `B,Q,S,Y,Z` block changes between
every pair of states; all three `h` are regular; the direct and factored forms of (1) agree exactly;
and (2) reconstructs each `h` exactly.

## 2. Two lawful transition systems

With a supplied common tangent-space carry, complete ambient endpoint transitions are

```text
A_ij=E_j E_i^-1.                                     (4)
```

For literally matched middle coframes,

```text
A_12 A_01=A_02,       A_10=A_01^-1.                 (5)
```

The terminal pair states separately define

```text
R_ij=Bpair_j Bpair_i^-1,                             (6)
R_12 R_01=R_02,       R_10=R_01^-1.                 (7)
```

The reciprocal character in (3) telescopes through (7). These statements do not identify the
four-dimensional ambient arrow (4) with the two-dimensional terminal arrow (6), nor do they assert
path-flatness. An independently rebuilt middle state still requires an explicit reset.

## 3. The recovered `mu_lock` channel is not appended to the pair result

G92 places the scoped August coefficient inside a supplied ambient transition. The modern pair
metric instead depends on the screen leg

```text
R_screen=SY+Z.                                       (8)
```

For any matrix `D`,

```text
S'=S+D,       Z'=Z-DY                               (9)
```

preserves (8), hence preserves `h`, `Bpair`, `phi_pair`, `c_eff/c_E`, and every terminal transition
`R_ij`. It changes the ambient coframe and generally changes `A_ij` and its full-arrow mixing
invariants. The primary and independent implementations verify this exact separation.

Therefore the endpoint-transition `mu_lock` may affect a pair readout only through the supplied
complete `(E,J)` relation. It cannot be universally recovered from, or appended to, the terminal
scalar.

## 4. Every complete channel remains live at a generic point

Direct differentiation of (1) gives

```text
delta U=delta B Y+B delta Y,
delta R_screen=delta S Y+S delta Y+delta Z,
delta A=delta Q R_screen+Q delta R_screen,
delta h=2 sym(U^T eta_2 delta U+A^T delta A).         (10)
```

For

```text
delta phi_pair=(1/4)tr(h^-1 delta h)
               -(1/2)delta h00/h00,                 (11)
```

separate exact `E00` perturbations of `B,Q,S,Y,Z` give five nonzero `delta h` and five nonzero
`delta phi_pair` values. Both implementations reproduce the same exact fractions. This proves
sensitivity, not a physical dynamics or regime score. G90 remains binding: all instruments may be
active along flat, monotone, or loud-quiet-loud supplied histories.

## 5. SNe-facing interface

The release-candidate ownership chain is:

```text
complete supplied (E,J)
-> h
-> phi_pair                                      DERIVED CONDITIONAL,

phi_pair -> 1+z=exp(phi_pair)                    CONDITIONAL registered SNe readout,

supplied null/screen/Jacobi query -> D -> d_A    DERIVED CONDITIONAL,

(z,d_A) -> d_L/flux/magnitude                    CONDITIONAL source/flux premise.
```

The `c_eff` consistency identity follows from the first two lines:

```text
c_eff^(pair)/c_E=(1+z)^-2.                         (12)
```

It is not an independent observable correction or a material signal speed.

The old native SNe replay is correctly typed but only re-expresses frozen P1/P2/P3 profiles in
`phi_pair`; it does not run the rebuilt complete kernel. Its `d_A=r` and
`d_L=(1+z)^2d_A` relations remain conditional readout premises. G79 is a stronger constructive
witness: one chosen complete geometry/query produced both endpoint redshift and a full Jacobi
`d_A/R`. It still did not select a physical profile, scale, endpoint family, or SNe likelihood.

Thus the kernel now has the correct geometry-level SNe ports—terminal redshift and screen angular
distance—but not the physical history or native flux/source law needed for an unconditional SNe
prediction.

## 6. Landing

```text
KERNEL_COHERENT
__GEOMETRIC_SNE_QUERY_READY_CONDITIONALLY
__FULL_SNE_VALIDATION_BLOCKED_BY_PHYSICAL_HISTORY_AND_FLUX_OWNERSHIP
```

- `DERIVED CONDITIONAL`: complete evaluator, terminal decomposition, reciprocal identity, matched-
  middle composition, reversal, and the ambient/terminal channel separation.
- `OBSERVED/CONDITIONAL`: `c_E` calibration and the registered SNe redshift identification.
- `DERIVED CONDITIONAL`: Jacobi angular distance on a supplied null/screen query.
- `OPEN`: physical complete history, pair family, flux/source law, and full SNe prediction.

The kernel itself does not require another algebraic mechanism before returning to the SNe lane.
The next SNe rung must be called a **geometry-level replay**: map supplied complete histories through
one typed redshift-plus-Jacobi query before any fit. A full validation claim remains unavailable.
