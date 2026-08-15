# Exact derivation — August 6 `mu_lock` and the complete pair kernel

Date: 2026-08-15  
Status: `INTERNALLY_VERIFIED_WITH_CAVEATS`; fresh adversarial semantic review still owed

## 1. The objects have different types

The August lane supplied an endpoint comparison arrow on one clock, one ruler, and one screen slot:

```text
A_u = [[a,0,mu],
       [0,r,0],
       [0,0,s]],          a=1/r,
```

with `eta_3=diag(-1,1,1)`. Its load-bearing object was the full-arrow strain

```text
C_u=A_u^dag A_u.
```

The modern kernel instead supplies a local coframe and a pair immersion:

```text
E=[[B,0],[Q S,Q]],       J=[Y;Z],
h=J^T E^T eta_4 E J.
```

`A_u`, `E`, `J`, and `h` are not interchangeable. To compare endpoint coframes one must additionally
supply a tangent-space carry. This audit uses the explicitly bounded identity/block-preserving
carry in a shared chart. No physical ownership of that carry is claimed.

## 2. Conditional endpoint-coframe transition

For

```text
E_i=[[B_i,0],[Q_i S_i,Q_i]],
```

direct block inversion gives

```text
E_p^-1=[[B_p^-1,0],[-S_p B_p^-1,Q_p^-1]].
```

Hence the supplied identity-carry transition is

```text
A_l=E_q E_p^-1
   =[[B_q B_p^-1,                         0],
     [Q_q(S_q-S_p)B_p^-1,       Q_q Q_p^-1]].              (1)
```

The complete lower mixing transition is therefore the matrix

```text
M_pq=Q_q(S_q-S_p)B_p^-1.                              (2)
```

This is the exact type-correct bridge available after the carry and split are supplied.

## 3. The August scalar is a restricted component of that transition

Take a one-screen reference slice

```text
B_p=I, Q_p=1, S_p=0,
B_q=diag(a,r), Q_q=s, S_q=(-mu/s,0).
```

Equation (1) becomes

```text
A_l=[[a,0,0],
     [0,r,0],
     [-mu,0,s]].                                      (3)
```

But this is exactly the metric adjoint of the August upper arrow:

```text
A_l=A_u^dag.                                          (4)
```

Thus, in this declared convention,

```text
mu_lock=-[M_pq]_(screen,clock).                       (5)
```

The sign is a variance convention, not a discrepancy. The two strains are

```text
C_u=A_l A_u,       C_l=A_u A_l,
```

and are exactly similar:

```text
C_l=A_u C_u A_u^-1.                                  (6)
```

For positive eigenvalues the map `v -> A_u v` preserves causal signature because

```text
eta(A_u v,A_u v)=eta(v,C_u v)=lambda eta(v,v).
```

Therefore the causal-labelled spectra agree. The symbolic derivation reproduces exactly

```text
Tr C = r^2+r^-2+s^2-mu^2,
Inv2 C = 1+r^2s^2+s^2/r^2-mu^2r^2,
det C=s^2.                                           (7)
```

This passes the preregistered reproduction gate. The original `s!=r` generic scope and its exact
`s=r` gauge carve-out remain mandatory; this audit does not alter them.

## 4. What changes when the second screen direction is released

In the full modern chart, equation (2) is a `2x2` matrix. A scalar clock-to-one-screen coefficient
exists only after selecting one clock line, one screen line, the split, endpoint gauges, and the
carry. It is a legitimate coordinate of the restricted transition but is not the whole mixing
object.

The nonuniqueness is exact even on the A-calibrated zero-embedding slice. Put

```text
P=M^T M.
```

On the August rank-one slice,

```text
P=diag(mu^2,0).
```

Every member of

```text
F_alpha(P)=Tr(P)+alpha det(P)                         (8)
```

therefore equals `mu^2`. But on a rank-two slice `P=diag(mu^2,u^2)`,

```text
F_alpha=mu^2+u^2+alpha mu^2u^2.                       (9)
```

Different `alpha` values separate. Thus agreement with `mu^2` on the old one-instrument slice does
not select a unique scalar extension to the complete orchestra.

## 5. The pair pullback is not the full-arrow strain

Insert (3) into the modern evaluator with the base-aligned pair query

```text
Y=I, Z=0.
```

The exact induced pair metric is

```text
h=diag(-a^2+mu^2,r^2).                                (10)
```

For `a=1/r`,

```text
(c_eff/c_E)^2=(1-mu^2 r^2)/r^4.                       (11)
```

This is a conditional pair readout, not the August strain extractor. Equation (10) has no `s`,
whereas the old full-arrow spectrum retains `s` through (7). The independent exact witness gives the
same terminal metric

```text
h=diag(-3/16,4)
```

for `s=3` and `s=4`, while the old strain traces are respectively

```text
211/16,       323/16.                                 (12)
```

The two channels therefore cannot be identified.

There is a stronger non-recovery theorem. The modern pair screen leg is

```text
R=SY+Z.
```

For any `D`,

```text
S -> S+D,
Z -> Z-DY                                             (13)
```

leaves `R`, `h`, `phi_pair`, and `c_eff/c_E` exactly unchanged. But it changes the ambient mixing
coframe and therefore generally changes the endpoint transition (2) and its embedded `mu_lock`.
Consequently no function of the terminal pair metric can universally reconstruct the August
full-arrow scalar.

This does not mean the modern uncompressed input has thrown mixing away: `S` and `Z` remain separate
before pullback. It means the final two-dimensional metric deliberately retains only what the
supplied pair surface samples.

## 6. Landing

The preregistered landing is

```text
MIXED
__RESTRICTED_S_COORDINATE_BRIDGE_EXISTS
__MU_LOCK_INVARIANT_REMAINS_FULL_ARROW_CHANNEL
__TERMINAL_PAIR_RECOVERY_NONUNIQUE
```

Premise-stamped meaning:

- `DERIVED CONDITIONAL`: equations (1)--(13) under the supplied split and identity carry.
- `VERIFIED_WITH_CAVEATS`: the August `mu_lock` is one signed component of the lower endpoint
  transition on its restricted one-screen slice, with the old gauge carve-out retained.
- `DERIVED`: it has no unique scalar extension from the rank-one slice to complete rank-two mixing.
- `DERIVED`: it is not universally reconstructible from terminal `h`, `phi_pair`, or `c_eff/c_E`.
- `OPEN`: the physical endpoint carry, pair realization, complete invariant family, and history.

The operational correction is simple: use the complete pair metric for the reciprocal endpoint
readout; use a separately typed endpoint comparison arrow for full-arrow strain or transport data.
Do not append `mu` after `phi_pair`, and do not rename an `S` entry as a universal invariant.
