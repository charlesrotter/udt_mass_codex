# Independent global proof for the positive product witness

Date: 2026-09-01
Role: G313 repair R2; mathematical witness only

For positive `Lambda`, the explicit metric is

\[
g=\Lambda^{-1}\left[-d\tau^2+\cosh^2\tau\,d\chi^2+d\Omega_2^2\right],
\qquad \tau\in\mathbb R,\quad \chi\sim\chi+2\pi.
\]

`verify_independent.py` starts from this coordinate metric, its inverse, and its nonzero first and
second coordinate derivatives. Its generic Christoffel/Ricci contraction independently verifies
`Ric_ab=Lambda g_ab` at multiple exact rational hyperbolic and spherical points and at four positive
values of `Lambda`. It does not call the production implementation or assume the product Ricci
formula.

The global claims follow separately:

1. Each constant-`tau` slice is `S1 x S2`: periodic `chi` supplies `S1`, and the angular factor is
   the complete round `S2`. A finite product of compact spaces is compact.
2. The inverse metric gives `g^{-1}(d tau,d tau)=-Lambda<0`, so `tau` is a temporal function and is
   strictly monotone on every future-directed causal curve.
3. Suppose an inextendible causal curve had a finite upper or lower endpoint in `tau`. On every
   bounded `tau` interval the spatial metric is uniformly positive and the causal inequality bounds
   spatial speed with respect to `tau`. Compactness of `S1 x S2` then gives a limiting spacetime
   point, through which the causal curve can be extended. This contradicts inextendibility.
4. Therefore `tau` ranges from minus infinity to plus infinity on every inextendible causal curve.
   Strict monotonicity makes each constant-`tau` slice intersect that curve exactly once. The slices
   are Cauchy surfaces.

This establishes a smooth, globally hyperbolic, compact-slice, non-round positive Einstein witness.
It does not assert that UDT physically populates it.
