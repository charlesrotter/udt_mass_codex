# G264 exact derivation — native selectivity of negative-phi regions

Date: 2026-08-25

Primary landing:

```text
NEGATIVE_PHI_SIGN_ALONE_DOES_NOT_SELECT
__FINITE_ARBITRARILY_DEEP_SMOOTH_ASYMPTOTICALLY_FLAT_SLICE_COMPLETE_COUNTERFAMILY_EXISTS
__UNBOUNDED_NEGATIVE_ENDS_HAVE_AN_ALPHA_TWO_CURVATURE_ACCELERATION_AND_SLICE_COMPLETENESS_THRESHOLD
__THE_ALPHA_TWO_CRITICAL_REPRESENTATIVE_IS_THE_G201_ZERO_TIDE_FAMILY
```

This is a bounded theorem about the primary static-spherical metric. It is not a history law.

## 1. Metric-native invariants

On

\[
ds^2=-f(r)c_E^2dt^2+\frac{dr^2}{f(r)}+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0,
\]

the determinant is

\[
\det g=-c_E^2r^4\sin^2\theta,
\]

which is independent of `f`. A direct four-dimensional Christoffel/Riemann calculation gives

\[
\mathcal R=-f''-\frac{4f'}r-\frac{2(f-1)}{r^2},
\]

and

\[
\mathcal K=R_{abcd}R^{abcd}
=(f'')^2+4\left(\frac{f'}r\right)^2
+4\left(\frac{f-1}{r^2}\right)^2.
\]

The mixed Einstein-tensor channels, used only as geometric diagnostics and not as field equations,
are

\[
G^t{}_t=G^r{}_r=\frac{rf'+f-1}{r^2},
\qquad
G^\theta{}_{\theta}=G^\varphi{}_{\varphi}=\frac{f''}{2}+\frac{f'}r.
\]

These formulas show immediately that finite `phi<0`, hence finite `f>1`, is not by itself a
singularity or a failure of Lorentzian signature. The invariant behavior depends on the profile and
its first two radial derivatives.

## 2. Exact negative counterfamily

Let

\[
x=\frac{r^2}{L^2},
\qquad
f_\epsilon(r)=1+\epsilon x e^{-x},
\qquad \epsilon,L>0.
\]

For every finite `r>0`,

\[
f_\epsilon>1,
\qquad
\phi_\epsilon=-\frac12\log f_\epsilon<0.
\]

The maximum occurs at `r=L`:

\[
f_{\max}=1+\frac{\epsilon}{e},
\qquad
\phi_{\min}=-\frac12\log\left(1+\frac{\epsilon}{e}\right).
\]

Thus the finite negative depth can be made arbitrarily large in magnitude by increasing
`epsilon`, while every fixed family member remains regular.

At the areal center,

\[
\phi_\epsilon(r)=-\frac{\epsilon}{2L^2}r^2+O(r^4),
\]

\[
\mathcal R(0)=-\frac{12\epsilon}{L^2},
\qquad
\mathcal K(0)=\frac{24\epsilon^2}{L^4}.
\]

Both are finite for finite `epsilon,L`. At infinity, `f -> 1`, `R -> 0`, and `K -> 0`.

Because

\[
1\le f_\epsilon\le 1+\frac\epsilon e,
\]

the static spatial metric

\[
d\ell^2=f_\epsilon^{-1}dr^2+r^2d\Omega^2
\]

is bounded below by a positive constant multiple of the Euclidean metric. Its radial proper length
to infinity diverges, and the complete centered static slice is metrically complete. This is a
conditional property of the witness, not a theorem of full Lorentzian geodesic completeness.

Therefore the sign condition `phi<0` alone selects no physical profile.

## 3. Unbounded negative ends

Now conditionally assume an unbounded power end

\[
f(r)\sim C\left(\frac rL\right)^\alpha,
\qquad C>0,\quad \alpha>0.
\]

Then `phi -> -infinity`, and the leading invariant behavior is

\[
\mathcal R\sim
-\frac{C(\alpha+1)(\alpha+2)}{L^2}
\left(\frac rL\right)^{\alpha-2},
\]

\[
\mathcal K\sim
\frac{C^2}{L^4}
\left[\alpha^2(\alpha-1)^2+4\alpha^2+4\right]
\left(\frac rL\right)^{2\alpha-4}.
\]

For normalized static observers, the proper acceleration magnitude is

\[
|a|=\left|\frac{d\sqrt f}{dr}\right|
\sim \frac{\sqrt C\,\alpha}{2L}
\left(\frac rL\right)^{\alpha/2-1}.
\]

The static-slice radial length and volume behave as

\[
\int^\infty\frac{dr}{\sqrt f}
\sim\int^\infty d\rho\,\rho^{-\alpha/2},
\]

\[
\operatorname{Vol}\sim\int^\infty d\rho\,\rho^{2-\alpha/2}.
\]

Hence:

| growth | curvature and acceleration | radial slice length | spatial volume |
|---|---|---|---|
| `0<alpha<2` | tend to zero | infinite | infinite |
| `alpha=2` | finite nonzero limits | logarithmically infinite | infinite |
| `2<alpha<=6` | diverge | finite | infinite |
| `alpha>6` | diverge | finite | finite |

The threshold is controlled by growth and derivatives, not by negative sign alone.

## 4. The alpha-two intersection

The simplest exact critical representative is

\[
f(r)=1+C\frac{r^2}{L^2},
\qquad C>0.
\]

For the G201 angular-tide channels

\[
A_\parallel=\frac{r^2f''-rf'}2,
\qquad
A_\perp=1-f+\frac{rf'}2,
\]

one obtains exactly

\[
A_\parallel=A_\perp=0.
\]

At the same time,

\[
\mathcal R=-\frac{12C}{L^2},
\qquad
\mathcal K=\frac{24C^2}{L^4},
\]

the radial proper length diverges logarithmically, and

\[
|a|\longrightarrow\frac{\sqrt C}{L}.
\]

So the critical unbounded negative end is not a newly invented mechanism. It is the negative
`C>0` member of the already derived G201 zero-angular-tide family. This is a genuine structural
intersection. It still does not establish that Nature selects this family or that it realizes
`X_max`.

## 5. Exact ownership ceiling

`DERIVED_CONDITIONAL`:

- the invariant formulas;
- finite-negative sign nonselection by explicit counterfamily;
- the `alpha=2` growth threshold under the registered power-law assumption;
- the exact coincidence of the critical representative with the G201 zero-tide family.

`OPEN`:

- physical history and dynamics;
- whether any unbounded negative end is populated;
- whether the power-law assumption is physical;
- source, matter, mass positivity, and energy conditions;
- relation to `X_max`;
- nonspherical and time-live extension of this classification.

The result narrows the geometry of possible negative ends. It does not choose one.
