# G271 exact derivation — primary-metric null screen first-jet interlock

Date: 2026-08-26

## Landing

```text
NATIVE_LONGITUDINAL_TRANSVERSE_FIRST_JET_SPLIT
__ONE_PRIMARY_METRIC_GRADIENT_GENERATES_DEPTH_AND_TRANSPORTED_SCREEN_CHANNELS
__RADIAL_AND_QUIET_STRATA_EXACT
__NO_FINITE_PATH_HISTORY_DISTANCE_OR_XMAX_SELECTION
```

This selects preregistered alternative
`C__NATIVE_LONGITUDINAL_TRANSVERSE_FIRST_JET_SPLIT`.

## 1. Supplied metric family

On a regular finite-radius patch set `c_E=1` inside metric-normalized contractions and write

\[
g=-e^{-2\phi(r)}dt^2+e^{2\phi(r)}dr^2+r^2d\Omega^2.
\]

Define

\[
N=e^{-\phi},\qquad A=e^{\phi}=N^{-1},\qquad U=N^{-1}\partial_t.
\]

`U` is the metric-unit static clock field. No equation is imposed on the arbitrary smooth profile
`phi(r)`.

## 2. The metric differentiates the static clocks

A direct Christoffel calculation gives

\[
\Gamma^r{}_{tt}=-e^{-4\phi}\phi',
\qquad
a=\nabla_UU=-e^{-2\phi}\phi'\,\partial_r.
\]

With `e_hat_r=e^{-phi} partial_r`, the physical radial component is

\[
\boxed{a_{\hat r}=-e^{-\phi}\phi'.}
\]

More strongly, the whole static congruence obeys

\[
\boxed{\nabla_XU=-g(X,U)a}
\]

for every tangent vector `X`. This was reconstructed directly from all metric Christoffels, not
imported as a static-spacetime formula.

## 3. Exact transported-screen generation law

Let `k` be the tangent to one supplied future affine null branch and

\[
\omega=-g(k,U)>0,\qquad k=\omega(U+n).
\]

Parallel transport the source clock/null plane and an orthonormal screen basis `E_I` along the same
branch. G269's screen components at each endpoint are

\[
W_I(\lambda)=g(U(\lambda),E_I(\lambda)).
\]

Since `nabla_k E_I=0`, metricity and the static-congruence identity give the exact all-path
evaluator

\[
\boxed{
\frac{dW_I}{d\lambda}
=g(\nabla_kU,E_I)
=\omega\,g(a,E_I).
}
\]

Therefore

\[
\boxed{
W_I(B)=\int_A^B\omega\,g(a,E_I)\,d\lambda,
}
\]

with `W_I(A)=0`. This is not a new field or coefficient: a supplied profile, null branch, and
Levi-Civita transport evaluate the integral. It is not a history-selection law.

## 4. Local longitudinal/transverse split

### Spherical-isometry reduction

The equatorial calculation below represents every regular local null germ at finite `r>0`, modulo
an isometry of the supplied spherical metric. At one event write the spatial null direction as

\[
n=\cos\alpha\,e_{\hat r}+\sin\alpha\,e_{\hat\perp},
\qquad e_{\hat\perp}\in T(S^2),\quad \lVert e_{\hat\perp}\rVert=1.
\]

The `SO(3)` isometry group preserves `r`, `phi(r)`, `U`, `e_hat_r`, the radial acceleration `a`,
Levi-Civita transport, and every metric contraction used in the theorem. A rotation maps the
two-plane spanned by `e_hat_r` and `e_hat_perp` to the equatorial orbital plane and maps
`e_hat_perp` to `e_hat_varphi`. The orthogonal screen direction maps to `e_hat_theta`. Therefore the
equatorial representative has the same `delta` jet, transported-screen jet, norm split, and
radial/quiet strata as the original germ. No preferred orbital plane or new physical premise is
introduced. At `sin(alpha)=0` the orbital plane is nonunique, but spherical symmetry and the exact
radial calculation make every such screen choice equivalent.

Choose that equatorial representative and write

\[
n=\cos\alpha\,e_{\hat r}+\sin\alpha\,e_{\hat\varphi}
\]

and the oriented in-plane screen

\[
s=-\sin\alpha\,e_{\hat r}+\cos\alpha\,e_{\hat\varphi}.
\]

The already-derived static endpoint relation is

\[
\delta(\lambda)=\phi(r(\lambda))-\phi(r_A).
\]

Along the same null germ,

\[
\frac{1}{\omega}\frac{d\delta}{d\lambda}
=e^{-\phi}\phi'\cos\alpha.
\]

The exact screen evolution at the source gives

\[
\frac{1}{\omega}\frac{dW_s}{d\lambda}
=e^{-\phi}\phi'\sin\alpha.
\]

Consequently

\[
\boxed{
\left(\frac{\dot\delta}{\omega}\right)^2
+\left(\frac{\dot W_s}{\omega}\right)^2
=e^{-2\phi}(\phi')^2
=\lVert a\rVert^2.
}
\]

The two channels are therefore the longitudinal and transverse angular projections of the same
metric-owned first jet. Their ratio is `tan(alpha)` whenever the longitudinal component is nonzero.
Affine rescaling multiplies `omega`, `dot(delta)`, and `dot(W_s)` together, so the normalized split
is invariant.

## 5. Exact and local strata

- **Radial:** `sin(alpha)=0`. The angular orthonormal screen vectors are parallel along a radial
  null branch and orthogonal to the radial acceleration. Hence `W=0` exactly along the whole
  regular static-radial branch, recovering `M_PT=sech(delta)`.
- **Tangential at one event:** `cos(alpha)=0`. Direct depth has zero first jet while the in-plane
  screen jet carries the full local amplitude.
- **Quiet first jet:** `phi'=0`. Both channels vanish locally.
- **Nonradial/nonquiet:** `phi' sin(alpha) != 0`. `W` is generated immediately, so universal static
  planarity is false.
- **Profile sign:** the value sign of `phi` alone selects neither channel. `e^{-phi}` changes their
  common magnitude, while `phi'` fixes their local orientation and `alpha` divides the channels.

For an equatorial branch the out-of-plane `e_hat_theta` is parallel and orthogonal to `a`, so the
new mismatch is wholly in the orbital screen direction.

## 6. Leading mutual-clock departure

Let

\[
\delta=d_1\lambda+O(\lambda^2),\qquad
W_s=w_1\lambda+O(\lambda^2).
\]

G269 gives

\[
\Gamma_{\rm PT}=\cosh\delta+\frac{e^{-\delta}}2\lVert W\rVert^2.
\]

Therefore

\[
M_{\rm PT}
=1-\frac12(d_1^2+w_1^2)\lambda^2+O(\lambda^3),
\]

while

\[
\operatorname{sech}\delta
=1-\frac12d_1^2\lambda^2+O(\lambda^3).
\]

The first departure from the planar candidate is

\[
\boxed{
\operatorname{sech}\delta-M_{\rm PT}
=\frac12w_1^2\lambda^2+O(\lambda^3)\ge0.
}
\]

This is precisely G269's sharp bound expressed in the local native generator.

## 7. Reversal compatibility

G269 derives `W_BA^2=r_AB^2 W_AB^2`. For a short segment, `r_AB=1+O(lambda)` and
`W_AB^2=O(lambda^2)`, so the forward and reverse screen norms agree through the load-bearing
quadratic order. `Gamma_PT` and `M_PT` remain reversal-even, while the signed depth is reversal-odd.

## 8. What this does and does not close

G271 closes the local origin of `W` on the supplied primary family: it is accumulated transverse
static-clock acceleration, not an appended orchestra coefficient. It also explains why radial
controls hear only `sech(delta)` and why nonradial geometry can make the inequality strict.

It does not choose `phi(r)`, a finite null path, endpoint population, distance, `X_max`, an evolving
history, a source, dynamics, transfer, or an observation. The finite value requires integrating the
exact evaluator over a supplied branch.

## 9. Verification

- 30 direct symbolic checks from the full metric and Christoffels;
- an implementation-independent generic-lapse derivation;
- 20,000 exact rational angle/slope/frequency cases;
- 207 radial, 199 tangential, 173 exact quiet, and 20,000 sign-pair controls;
- six implementation mutations and six typed overreach mutations caught.
