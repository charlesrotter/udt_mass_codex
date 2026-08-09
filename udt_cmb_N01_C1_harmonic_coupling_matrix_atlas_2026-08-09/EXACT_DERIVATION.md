# Exact N01 C1 harmonic coupling derivation

## Scope

C1 remains `CHOSE`: it is the conditional round, axis-regular, axially mixed representative. The
scalar `Box_g` remains a chosen metric diagnostic, not native UDT dynamics. This tile derives its
complete angular Galerkin architecture; it does not select C1 or solve its radial equation.

## From the exact C1 equation to matrices

With `x=cos(theta)` define

```text
B=h^2/(A r^2),        F=sqrt(1+B(1-x^2)).
```

The C1 volume becomes `S=r^2 sin(theta)F`. Multiplying the exact scalar equation by `S`, changing
from `theta` to `x`, and projecting on normalized associated-Legendre functions gives

```text
d_r[r^2 A W(B) d_r R]
- [K(B)+H_m(B)]R
+ [(r^2 omega^2+2h omega m)/A]M(B)R = 0.                 (1)
```

The matrix definitions are

```text
W_lk = integral p_l F p_k dx
M_lk = integral p_l F^-1 p_k dx
K_lk = integral (1-x^2)F p'_l p'_k dx
H_lk = integral m^2/[(1-x^2)F] p_l p_k dx.
```

For `m=0`, `H=0`. For negative `m`, the same angular matrices apply because they depend on `m^2`,
but the external `2h omega m` coefficient in (1) preserves the sign. The derivative in the first
term acts on the entire `r^2 A W(B(r))d_r R`; thus the metric-supplied `B'(r)` coupling is retained.

## Exact label and parity structure

`F(x)` is even. Since `p_lm(-x)=(-1)^(l+m)p_lm(x)`, every one of `W,M,K,H,L=K+H` has zero matrix
elements between opposite north/south parities. The C1 architecture therefore retains fixed
`|m|`, the sign through the external rotation-linear coefficient, and two parity blocks. It does
not retain `ell` as an exact label when `B` is nonzero.

At `B=0`,

```text
W=M=I,        K+H=diag[l(l+1)].
```

For `|m|>0`, `K` and `H` are individually dense within parity but cancel off diagonal in their
sum. This is a useful completeness warning: either angular piece alone falsely reports round-limit
mixing.

## First-order structure

For normalized associated-Legendre functions,

```text
x p_l = a_l p_(l+1)+a_(l-1)p_(l-1),
a_l^2=[(l+1)^2-m^2]/[(2l+1)(2l+3)],

(1-x^2)p'_l=(l+1)a_(l-1)p_(l-1)-l a_l p_(l+1).
```

Using `F=1+B(1-x^2)/2+...` and `F^-1=1-B(1-x^2)/2+...` gives exact first derivatives by finite
matrix products. They couple only `Delta ell=0,2`; the `Delta ell=4` controls vanish exactly.
`FIRST_ORDER_COUPLING.tsv` preserves 36 exact radical entries.

For every `B>0`, `W`, `M`, and `L` are genuinely infinite-band in the complete basis. If the lowest
`W` or `M` column had finite support, respectively `F p_m` or `F^-1 p_m` would be a finite sum of
associated Legendre functions. Dividing out their common `(1-x^2)^(m/2)` factor would make `F` or
`F^-1` a polynomial, which it is not. For the strong operator represented by `L`, direct application
to the lowest function gives, for `m>0`,

```text
(L p_m)/p_m = m[(m+1)+B(1-(m+2)x^2)]/F,
```

which is nonpolynomial. For `m=0`, applying it to `p_1` gives

```text
(L p_1)/p_1 = [2+3B(1-x^2)]/F,
```

also nonpolynomial. `B=0` is the explicit diagonal exception. Thus parity is exact while no finite
band can contain these three complete-basis operators. The separate `K` and `H` tables are retained
as complete-term diagnostics; no additional infinite-band theorem for either one alone is needed.

Within the registered `ell<=16` atlas and `1e-12` characterization threshold, `W` and `M` reach the
largest available same-parity separation (`Delta ell=16`) in at least one block; `L` reaches
`Delta ell=14`. These are bounded-basis observations, not infinite-basis nonzero proofs.

## Numerical certification

All 15,420 upper-triangle entries were evaluated at registered Gauss-Legendre orders 256 and 512.
The same orders were retained after a failed double-precision implementation; their nodes and
weights were refined and accumulated in long double. Maximum gates were:

```text
256/512 disagreement       8.881784197001252e-16
opposite-parity leakage    5.551115123125783e-17
matrix asymmetry           5.551115123125783e-17
round L error              2.3592239273284576e-16.
```

Order-256/order-512 agreement is a same-implementation convergence check over all 15,420 stored
elements. A separate local implementation uses adaptive quadrature and SciPy associated-Legendre
functions on eight deterministic elements spanning round, weak, moderate, and strong mixing
controls, and independently integrates all 36 first-order rows. The fresh cold review additionally
used symbolic integration for all 180 first-order values and 50-digit quadrature for 18 hard matrix
controls.

## Exact landing

Derived within conditional C1:

- matrix equation (1), including the complete radial matrix flux;
- exact `|m|` and north/south parity block ownership;
- exact round-limit cancellation and first-order `Delta ell=0,2` structure;
- exact infinite-band `W`, `M`, and `L` structure for every `B>0`, with `B=0` diagonal;
- a fully preserved bounded matrix atlas.

No eigenvalue, radial solution, physical `B(r)`, boundary, screen selection, population, source,
polarization channel, CMB prediction, FD2 restart, or GPU work is derived.
