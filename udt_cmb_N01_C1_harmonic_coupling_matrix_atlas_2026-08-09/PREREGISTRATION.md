# N01 C1 harmonic coupling-matrix atlas — preregistration

Date: 2026-08-09
Mode: bounded CPU `MAP/DERIVE`; no radial/eigenvalue solve
Base: `b87a35a051b9fad7d784e78e21e97207378725a5`

## Whole question

For the already-conditional axis-regular spherical C1 representative, derive the exact
spherical-harmonic Galerkin matrix form of the stationary scalar diagnostic and characterize every
angular coupling in a fixed, bounded basis. Determine which labels and parity blocks survive and
whether the exact nonzero-mixing coefficients are finite-band or long-range in `ell`.

This is metric-led machinery validation. It does not select C1, solve a spectrum, impose a mode
population, or compare with CMB data.

## Exact object to derive

For fixed axial character `m`, put `x=cos(theta)` and

```text
B(r)=h(r)^2/[A(r)r^2],       F_B(x)=sqrt(1+B(r)(1-x^2)).
```

Use real normalized associated-Legendre functions

```text
p_lm(x)=sqrt((2l+1)/2 * (l-m)!/(l+m)!) P_l^m(x),
integral_-1^1 p_lm p_km dx = delta_lk,
```

with the SciPy/Condon-Shortley phase convention. Expand
`u(r,theta)=sum_l R_l(r)p_lm(cos(theta))`. Direct weak projection of the exact C1 scalar equation
must give

```text
d_r[r^2 A W(B) d_r R]
- [K(B)+H_m(B)]R
+ [(r^2 omega^2+2h omega m)/A] M(B)R = 0,
```

where

```text
W_lk = integral p_l F_B p_k dx
M_lk = integral p_l F_B^-1 p_k dx
K_lk = integral (1-x^2)F_B p'_l p'_k dx
H_lk = integral m^2/[(1-x^2)F_B] p_l p_k dx,
```

and `H=0` identically for `m=0`. The radial derivative remains outside the complete matrix flux;
expanding it automatically carries `B'(r)` and must not be silently frozen.

## Frozen bounded universe

- `|m| = 0,1,2,3`; the angular matrices depend on `m^2`, while the retained external
  `2h omega m` coefficient distinguishes the two signs. No sign is discarded.
- `ell=m,...,16`, with both north/south parity blocks retained.
- `B = 0, 0.01, 0.1, 1, 10, 100`, all tagged `free-and-explored` dimensionless controls.
- Gauss-Legendre orders `256` and `512`; the doubled-order result is recorded.
- Matrices `W`, `M`, `K`, `H`, and `L=K+H`; every upper-triangle element is preserved.
- Numerical structural threshold `1e-12`; quadrature certification tolerance `2e-11` absolute.
  Thresholded counts characterize the bounded representation and never discard entries.

No radial sample, `A(r)`, `h(r)`, wall/center boundary condition, eigenfrequency, source weight,
angular population, observed peak, or physical value of `B` is supplied.

## Premise ledger

| input | status |
|---|---|
| C1 metric and exact scalar equation | `CHOSE` conditional representative; equation `DERIVED` inside it |
| scalar `Box_g` | `CHOSE` metric-native diagnostic, not native UDT dynamics |
| stationary and fixed `m` | `CHOSE`; valid because C1 conditionally has axial `U(1)` |
| normalized associated-Legendre basis | `CHOSE` complete numerical representation |
| north/south parity | `DERIVED` C1 symmetry |
| `B` grid and `ell_max=16` | `free-and-explored` bounded controls, not physical pins |
| quadrature orders/tolerances | numerical controls |
| CMB data, source/state weights, polarization | excluded |

## Preregistered certification and falsification gates

1. Derive the matrix equation from the exact C1 divergence-form operator without dropping radial
   matrix dependence or the `m^2` polar term.
2. At `B=0`, require `W=M=I` and `K+H=diag(l(l+1))` to the registered tolerance for every `m`.
3. Require symmetry of every matrix and zero opposite-parity entries to the registered tolerance.
4. Compare all stored order-256 and order-512 entries; maximum absolute disagreement must be below
   `2e-11`.
5. Record, do not filter, all diagonal/off-diagonal amplitudes and the farthest observed same-parity
   `Delta ell` at every `(B,m,matrix)`.
6. Establish the analytic parity rule. Do not claim exact finite bandwidth merely from a truncated
   numerical matrix.
7. Verify the first `B` derivative at zero independently for low harmonics; it may couple only
   `Delta ell=0,2`. Higher exact powers may extend coupling farther.
8. Fail-closed mutations must catch: omitted `H`; omitted radial `W`; parity mixing; a false
   universal diagonal/fixed-band claim; treating the `B` grid as selected physics; dropping a
   registered `m`, parity block, matrix, or `B`; authorizing an eigensolve; promoting C1; or ranking
   matrices by observational merit.

## Deliverables

- exact derivation and status ledger;
- full matrix-element atlas and block summary;
- round-limit and first-order analytic controls;
- independent implementation and mutation catches;
- completeness/lay/audit reports, raw logs, versions, and SHA-256 manifest.

## Maximum allowed conclusion

A verified bounded map of the harmonic coupling structure of the conditional C1 scalar diagnostic:
good labels, exact parity selection, matrix families, observed bounded-basis coupling reach, and
the correct matrix radial equation. No physical screen, spectrum, boundary, population,
polarization channel, CMB prediction, FD2 restart, or GPU work follows.

## Stop boundary

Stop after exact derivation, bounded matrix characterization, repository gates, and the required
adversarial-review gate. Do not solve the radial matrix equation or launch N02/FD2.
