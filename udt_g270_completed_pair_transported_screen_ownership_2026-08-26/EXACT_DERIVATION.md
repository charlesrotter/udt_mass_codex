# G270 exact derivation — completed pair versus transported screen mismatch

Date: 2026-08-26

## Primary landing

```text
FULL_SUPPLIED_REALIZATION_EVALUATES_TRANSPORTED_SCREEN_MISMATCH
__COMPLETED_PAIR_DUAL_RECIPROCITY_NORMALIZES_ONLY_THE_INTRINSIC_PULLBACK
__EXACT_SAME_PULLBACK_TILTED_NULL_RIBBONS_HAVE_DIFFERENT_W
__NO_UNIVERSAL_W_VALUE_POPULATION_HISTORY_DISTANCE_OR_XMAX_SELECTION
```

This selects preregistered alternative
`C__REALIZATION_EVALUATES_W__INTRINSIC_COMPLETED_PAIR_DOES_NOT_SELECT_IT`.

## 1. Two different ownership levels

For one supplied regular pair immersion, the intrinsic pair metric is

\[
h=F^*g.
\]

G176--G180 completed-pair Dual Reciprocity acts on this two-dimensional metric. In an auxiliary
pair chart it fixes

\[
m=\sqrt{-\det h_\sigma},
\qquad
\det h_s=-1.
\]

This is intrinsic data: it depends only on contractions of the two tangent vectors spanning the
pair plane.

G269's transported mismatch is different. Given a supplied affine null branch, source and target
unit clocks, and Levi-Civita transport, it decomposes the target clock relative to the transported
source clock/null plane:

\[
U_B=\Gamma_{\rm PT}\widetilde U_A+a\widetilde n_A+W,
\qquad W\perp\operatorname{span}(\widetilde U_A,\widetilde n_A).
\]

Thus `W` is bilocal ambient Gram data. Once the full realization is supplied, its projection and
norm are unique. The question is whether intrinsic completed reciprocity restricts that norm across
admissible realizations.

## 2. Exact flat tilted family

Work in flat `1+2` spacetime with signature `(-++)` and choose

\[
U_A=(1,0,0),qquad n_A=(0,1,0),qquad k=(1,1,0).
\]

Parallel transport is the identity. For arbitrary `r>0` and real `w`, put

\[
\Gamma=\frac12\left(r+r^{-1}+rw^2\right),
\qquad
a=\Gamma-r^{-1},
\qquad
U=(\Gamma,a,w).
\]

Direct contraction gives

\[
g(U,U)=-1,
\qquad
-g(k,U)=r^{-1}.
\]

The target frequency-one null vector and completed ruler are

\[
K=rk,
\qquad
N=K-U.
\]

They obey

\[
g(N,N)=1,
\qquad
g(U,N)=0,
\qquad
K=U+N.
\]

Therefore every real `w` supplies a regular completed pair plane containing the same null line and
having the same frequency ratio `r`.

Relative to the transported source plane,

\[
U=\Gamma U_A+a n_A+w e_\perp,
\]

so

\[
\boxed{\lVert W\rVert^2=w^2.}
\]

The full supplied realization therefore evaluates `W` without a fit or new coefficient.

## 3. The intrinsic pullback cannot hear the tilt

Use the auxiliary null-ribbon basis `(U,k)`. Its pair metric is

\[
\boxed{
h_\sigma=
\begin{pmatrix}
-1&-r^{-1}\\
-r^{-1}&0
\end{pmatrix}.}
\]

Every entry is independent of `w`, and

\[
\det h_\sigma=-r^{-2}<0.
\]

The shifted decomposition gives

\[
T=1,
\qquad
\beta=r^{-1},
\qquad
L_\sigma=r^{-1}.
\]

Completed-pair Dual Reciprocity therefore fixes

\[
m=T L_\sigma=r^{-1}.
\]

In the completed ruler coordinate,

\[
\boxed{
h_s=
\begin{pmatrix}
-1&-1\\
-1&0
\end{pmatrix},
\qquad
\det h_s=-1.}
\]

This completed metric is independent of both `r` and `w`. Hence two realizations with the same
`r` and different `w^2` have exactly the same auxiliary and completed intrinsic pullbacks while
their ambient transported-clock comparisons differ.

At `r=2`, the planar and unit-tilt cases give

\[
\begin{array}{c|c|c}
\lVert W\rVert^2&M_{\rm PT}&h_\sigma\\ \hline
0&4/5&\begin{pmatrix}-1&-1/2\\-1/2&0\end{pmatrix}\\
1&4/9&\begin{pmatrix}-1&-1/2\\-1/2&0\end{pmatrix}.
\end{array}
\]

This is a same-intrinsic-pullback separator, not merely two unrelated metrics.

## 4. Smooth completed null-ribbon realization

The separator is not confined to isolated endpoint vectors. On the half-ribbon `lambda>=0`, let

\[
r(\lambda)=1+\lambda,
\qquad
w(\lambda)=\lambda,
\qquad
\gamma(\lambda)=\lambda k,
\]

and construct `U(lambda)` by the preceding formulas. Define

\[
F(\tau,\lambda)=\gamma(\lambda)+\tau U(\lambda).
\]

Along `tau=0`,

\[
F_*\partial_\tau=U,
\qquad
F_*\partial_\lambda=k.
\]

Because `g(U,U)=-1`, differentiation gives `g(U,U')=0`. Also

\[
g(k,U')=\frac{d}{d\lambda}g(k,U)
=\frac1{r^2}.
\]

The axis pullback is therefore exactly the displayed `h_sigma`, with

\[
\det h|_{\tau=0}=-\frac1{(1+\lambda)^2}<0.
\]

The full pullback determinant, not merely its axis value, is

\[
\det F^*g
=-
\frac{A(\lambda)\tau^2+2\tau+1}{(1+\lambda)^2},
\qquad
A(\lambda)=4\lambda^2+4\lambda+2.
\]

For `lambda>=0`, `A>=2`, and its numerator has the exact positive completion

\[
A\left(\tau+\frac1A\right)^2+\frac{A-1}{A}>0.
\]

Therefore the determinant is strictly negative for every real `tau` on the declared half-ribbon.
This directly proves a smooth regular completed null-ribbon family, stronger than the earlier
axis-continuity argument, while `W` varies continuously and the completed intrinsic axis metric
remains fixed.

## 5. Consequence for the G269 interlock

G269 remains exact:

\[
\Gamma_{\rm PT}
=\cosh\delta+\frac r2\lVert W\rVert^2,
\qquad
0<M_{\rm PT}\leq\operatorname{sech}\delta.
\]

G270 shows how to type it:

- `DERIVED_CONDITIONAL`: the full supplied metric, branch, and endpoint realization evaluate
  `W`, `Gamma_PT`, and `M_PT` uniquely;
- `NOT_DERIVED`: completed-pair Dual Reciprocity does not force `W=0` or make `W` a function of
  `delta`;
- `EXACT_STRATUM`: `M_PT=sech(delta)` precisely on the transported-planar `W=0` stratum;
- `OPEN`: no existing result selects which `W` values are physically populated.

No free orchestra coefficient has appeared. The remaining variation is ordinary ambient
realization data already present in the metric and observer query. `W` is not the G188 Jacobi area
or G225 shared-event screen holonomy.

## 6. Verification

The repaired production derivation passes 39 exact symbolic checks, including the full determinant
and positivity decomposition. The independent implementation imports no production function and
reads no production artifact; it performs 368,165 exact-rational assertions over 12,000 frames,
1,001 smooth-ribbon axis samples, and 40,040 nonzero-`tau` ribbon samples with `-4<=tau<=4`. At fixed
`r=2`, 101 nonnegative tilts give 101 distinct transport values with the same intrinsic pair metric.
Eight formula-level implementation mutations and five separately labelled typed-ledger mutations
are caught.

## 7. Ceiling

This theorem distinguishes intrinsic completed-pair normalization from bilocal ambient transport.
It does not select a physical observer population, branch, metric history, distance law, numerical
`X_max`, observation, action, source, matter, transfer, bootstrap, mass, or signalling mechanism.
