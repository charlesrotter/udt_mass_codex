# G153 exact derivation — finite relational position versus metric ruler

Date: 2026-08-17

## 1. The source chain answers the ownership question

G137's adopted working constitution owns the signed finite relational position

\[
\rho=X_{\max}\tanh\phi_{\rm pair}.
\]

It explicitly leaves the proper-length join open. G147 then introduces
\(\boldsymbol\xi=\rho n\) only as a `DEFINED / SUPPLIED_CONDITIONAL_QUERY_RELATIVE_LIFT` and states
that it is not a spacetime displacement, exponential-map vector, proper length, or areal radius.
G152 derives the metric ruler \(r=Ln\) and proves that equality with the conditional lift is not
automatic.

Therefore the active premises do not own

\[
\boldsymbol\xi=\epsilon r.
\]

That equality compares a finite relation-ball coordinate with one local tangent variation. It is
permitted as an additional calibrated query condition, but it is not the native consequence of the
adopted position constitution.

G135's exact common-scale countermodel makes the obstruction concrete. Positive common rescaling
\((T,L)\mapsto(\Omega T,\Omega L)\) preserves \(\phi_{\rm pair}\), \(\rho\), and the projective
position while changing the metric ruler density. At

\[
T=\frac13,\quad L=1,\quad X_{\max}=2,
\]

one has \(\rho=L=1\). After common rescaling by two, \(\rho=1\) but \(L=2\). Thus finite equality
cannot be a universal consequence of projective position.

## 2. The correctly typed local join is differential

For one supplied smooth regular calibrated pair immersion, write

\[
h=-T^2(d\tau+\beta d\sigma)^2+L^2d\sigma^2.
\]

Its orthonormal coframe and dual frame are

\[
\theta^0=T(d\tau+\beta d\sigma),
\qquad
\theta^1=Ld\sigma,
\]

\[
u=\frac1T\partial_\tau,
\qquad
n=\frac1L(\partial_\sigma-\beta\partial_\tau).
\]

The metric owns \(\theta^1\) as the local ruler covector. Because \(\rho\) is a scalar on the
supplied pair family, its exact differential decomposes as

\[
\boxed{d\rho=u(\rho)\theta^0+n(\rho)\theta^1.}
\]

Using the adopted position law and retaining the still-open possibility that the asymptotic scale
varies across the supplied relation family gives

\[
\boxed{
u(\rho)=\tanh\phi_{\rm pair}\,u(X_{\max})
+X_{\max}\operatorname{sech}^2\phi_{\rm pair}\,u(\phi_{\rm pair}),
}
\]

\[
\boxed{
n(\rho)=\tanh\phi_{\rm pair}\,n(X_{\max})
+X_{\max}\operatorname{sech}^2\phi_{\rm pair}\,n(\phi_{\rm pair}).
}
\]

In pair coordinates,

\[
u(\rho)=\frac{1}{T}
\left[
\tanh\phi\,\partial_\tau X_{\max}
+X_{\max}\operatorname{sech}^2\phi\,\partial_\tau\phi
\right],
\]

\[
n(\rho)=
\frac{1}{L}
\left[
\tanh\phi\,(\partial_\sigma-\beta\partial_\tau)X_{\max}
+X_{\max}\operatorname{sech}^2\phi
(\partial_\sigma-\beta\partial_\tau)\phi
\right].
\]

This retains time-live behavior and shift. It is not an added orchestra coefficient: once a smooth
complete pair history and an `X_max` realization are supplied, both response coefficients are
derived. If `X_max` is constant on that family, the first term in each box vanishes; that is a
conditional subcase, not silently assumed in the generic formula.
Their squared-gradient diagnostic is

\[
h^{-1}(d\rho,d\rho)=-u(\rho)^2+n(\rho)^2.
\]

Its causal type is history-dependent; the zero-order terminal law does not fix it.

## 3. Common scale is retained correctly

Under positive common rescaling of the pair coframe,

\[
\theta^a\mapsto\Omega\theta^a,
\qquad
u,n\mapsto\Omega^{-1}(u,n),
\]

while \(\phi\), \(X_{\max}\), \(\rho\), and \(d\rho\) remain unchanged when the asymptotic-scale
realization itself is common-scale invariant. Consequently

\[
u(\rho),n(\rho)\mapsto
\Omega^{-1}\bigl(u(\rho),n(\rho)\bigr),
\]

and the products with the coframe remain unchanged. The response coefficient absorbs the live
metric scale; no strong local CSN or scale-free metric is implied.

## 4. What an additional unit-ruler statement would say

If one separately chose to identify local spatial relational-position increments with unit metric
ruler increments, the typed condition would be

\[
(d\rho)_\perp=\epsilon\theta^1
\quad\Longleftrightarrow\quad
n(\rho)=\epsilon,
\qquad \epsilon=\pm1.
\]

The stronger full one-form equality

\[
d\rho=\epsilon\theta^1
\]

would additionally require \(u(\rho)=0\). These are proper-ruler calibration conditions. They are
not contained in G137 and are not adopted here.

## 5. Consequence for the program

G152's finite-value candidate

\[
X_{\max}^{(\epsilon)}=\epsilon L\frac{L+T}{L-T}
\]

remains valid only inside its explicitly supplied finite-equality branch. It is not the next native
route to \(X_{\max}\). The premise-owned route is instead to evaluate the derived differential
response \(u(\rho),n(\rho)\) on one coherent supplied metric history. Doing that globally still
requires a physical history/query family and does not determine the value of \(X_{\max}\).

## Maximum conclusion

```text
G137_OWNS_FINITE_RELATIONAL_POSITION_NOT_METRIC_PROPER_RULER_LENGTH__
G147_REST_SPACE_VECTOR_LIFT_REMAINS_CONDITIONAL__
FINITE_CHORD_EQUALS_LOCAL_RULER_IS_NOT_THE_NATIVE_JOIN__
ON_A_SUPPLIED_SMOOTH_PAIR_FAMILY_D_RHO_HAS_AN_EXACT_METRIC_FRAME_DECOMPOSITION_WITH_DERIVED_TEMPORAL_AND_SPATIAL_RESPONSE_COEFFICIENTS__
UNIT_RULER_IDENTIFICATION_PROPER_LENGTH_HISTORY_XMAX_VALUE_AND_GLOBAL_COMPLETION_OPEN
```
