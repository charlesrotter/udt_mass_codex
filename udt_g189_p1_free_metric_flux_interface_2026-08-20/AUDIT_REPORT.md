# G189 audit — P1-free metric/flux interface

Date: 2026-08-20

## Result

G189 closes the regular static-query metric-to-flux algebra conditionally:

```text
Z=exp(phi_s-phi_o),
d_A=sqrt(abs(det D)),
d_L^2=Z^3 d_A^2/(eta epsilon),
eta=1 and epsilon=1/Z [IMPORTED_CONDITIONAL],
d_L=Z^2 d_A.
```

For the central spherical specialization, `d_A=R`, so every supplied monotone profile predicts

```text
d_L(Z)=Z^2 phi_inverse(log Z+phi_o).
```

P1 is exactly one supplied `phi(R)` profile, not an independent screen tensor or reciprocal
kernel.

## Preregistered P1-free control

The coefficient-free join `R=R0 chi`, `chi=tanh(phi)`, uses no P1 shape parameter, `X_max`, fitted
regime switch, or appended angular factor. It fails twice:

1. `phi=artanh(R/R0)` has nonzero radial derivative at the center and is not a smooth regular
   central-static scalar history.
2. As a formal annular/catalog curve under the imported transfer, it gives chi-squares
   `3204.950963265004` (Pantheon+) and `2685.911034093437` (DES), above the preregistered
   `1627.342686907440` and `1906.780617317963` ceilings.

This rejects only the provisional screen-position identification. It does not reject completed-pair
Reciprocity, `chi`, G188, a time-live history, or UDT.

## Evidence

- exact symbolic static-frequency, Jacobi-area, transfer, profile-inverse, and regular-center checks;
- frozen source-hash gate over 17 repository/data sources;
- production Cholesky likelihood calculation with zero shape parameters;
- implementation-distinct Pantheon precision and DES Schur-complement replay;
- 9 algebraic mutation catches and 9 semantic/scope guards;
- frozen P1 reference reproduced without entering the candidate.

## Premise ownership

| item | status |
|---|---|
| primary static metric and supplied profile | `DERIVED_CONDITIONAL` configuration |
| static-query `Z=exp(phi_s-phi_o)` | `DERIVED_CONDITIONAL` |
| G188/G119 screen area | `DERIVED_CONDITIONAL` |
| regular flux factorization | `DERIVED_CONDITIONAL` |
| `eta=1`, `epsilon=1/Z` | `IMPORTED_CONDITIONAL` |
| `R=R0 chi` | `CHOSE_PROVISIONAL_CONTROL`, rejected |
| P1 | `FROZEN_REFERENCE`; exact supplied profile only |
| physical time-live frequency/screen history | `OPEN` |

## Four gates

1. Preregistered: **PASS**, including a separately committed regular-center scope correction.
2. Full or bounded: **PASS** for the declared static central regular algebra and formal annular
   catalog control; time-live/global/singular/source strata remain open.
3. Independently verified: **PASS** by a different formula and precision-domain likelihood route.
4. Premises audited: **PASS internally** for metric, query, screen, transfer, profile, and data roles.

## Grade

```text
INTERNALLY_VERIFIED_WITH_CAVEATS
__STATIC_CHI_SCREEN_JOIN_TYPE_FAILS_REGULAR_CENTER
__FORMAL_ANNULAR_CURVE_REJECTED_BY_BOTH_SNE_INTERFACES
__METRIC_TO_FLUX_FACTORIZATION_CONDITIONALLY_CLOSED
__P1_REMAINDER_IS_PROFILE_OR_FREQUENCY_HISTORY_NOT_SCREEN_SCAFFOLDING
```

Fresh external adversarial review remains open before stronger banking.
