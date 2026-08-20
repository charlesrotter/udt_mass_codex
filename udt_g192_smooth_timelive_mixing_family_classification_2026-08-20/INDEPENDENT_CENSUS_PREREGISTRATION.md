# G192 independent census preregistration

Date: 2026-08-20

This census was frozen after the production symbolic reconstruction but before the independent
implementation was written or run. It may verify or falsify the symbolic landing; it may not alter
the function family or conclusion ceiling.

Write `a(eta)=exp(L(eta))`. Every named control uses `0<=eta<=eta_end`, hence `a>0` exactly.

| ID | `L(eta)` | `mu(eta)` | `eta_end` | Required coverage |
|---|---|---|---:|---|
| C01 | `0.35 eta` | `0.22` | 1.2 | exact G191 constant control |
| C02 | `0.20 eta + 0.08 eta^2` | `0` | 1.1 | nonconstant conformal G190 limit |
| C03 | `0.55 eta - 0.55 eta^2` | `0.15 + 0.08 sin(2 eta)` | 1.2 | one frequency turn |
| C04 | `0.12 sin(4 eta)` | `0.18 sin(3 eta)` | 1.5 | multiple frequency turns and signed mixing |
| C05 | `-0.18 eta + 0.04 eta^2` | `0.28 cos(2.5 eta)-0.12` | 1.3 | increasing frequency and mixing sign changes |
| C06 | `0.10 eta` | `0.30(eta-0.5)` | 1.2 | mixing zero crossing |
| C07 | `-1.40 eta` | `0.35 exp(-0.5 eta)` | 1.5 | small but regular common scale |
| C08 | `0.25 eta` | `-1/(sqrt(2)(2 eta+3))` | 1.4 | nonzero mixing with central trace-free tide identically zero |
| C09 | `0.15 eta` | `0.25 eta/sqrt(2)` | 1.2 | derivative-dominated negative cross response |
| C10 | `0` | `0.31` | 1.1 | exact G188 static-mixing control |

The random census is frozen at seed `19220260820` with 256 cases:

```text
L(eta)=c1 eta+c2 eta^2+c3 sin(w eta)
mu(eta)=m0+m1 eta+m2 sin(v eta)
c1 in [-0.5,0.7]
c2 in [-0.3,0.3]
c3 in [-0.15,0.15]
w in [0.5,4.0]
m0 in [-0.4,0.4]
m1 in [-0.35,0.35]
m2 in [-0.3,0.3]
v in [0.5,4.0]
eta_end in [0.2,1.5]
```

No case is rejected for having a frequency turn, signed cross response, small scale, or unexpected
screen shape. The independent code must integrate the affine Jacobi system directly and compare it
with a separately evaluated factorized quadrature. Registered maximum frequency/Jacobi error is
`2e-9`. Positivity of the factorized modes is checked at all internal nodes but is not used to alter
the census.

Required hostile controls are: delete `mu'`; delete `mu^2`; reverse curvature sign; reverse frequency
sign; use nonaffine `eta` as affine parameter; scalarize the screen; force monotone frequency; force
positive cross response; call every nonzero mixing history trace-free; force global `d_A(Z)` across a
turn; substitute the G191 constant formulas; insert P1/G116/G189, transfer, or `X_max`.
