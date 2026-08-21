# G205 exact derivation — geodesic and causal completion

Date: 2026-08-21

## Landing

```text
FULL_GEODESIC_COMPLETENESS_AND_GLOBAL_HYPERBOLICITY_SURVIVE_ALL_REGISTERED_PARAMETERS
__NULL_TRAPPING_HAS_SUBCRITICAL_CRITICAL_AND_SUPERCRITICAL_STRATA
__NO_PARAMETER_XMAX_OR_PHYSICAL_HISTORY_SELECTION
```

## 1. Supplied family and exact type

On the declared manifold `M=R_t x R3`, G204 supplies the exact witness family

\[
ds^2=-f(r)dt^2+\frac{dr^2}{f(r)}+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0,
\]

\[
\phi(r)=\frac{a}{2^n}x^2(x^2-1)^n,
\qquad x=r/r_0,
\qquad n\ge3\text{ odd},\quad a,r_0>0.
\]

The metric and family are supplied. Levi-Civita geodesics and the optical metric are standard
geometric evaluators. No field equation, source, action, transfer law, or `X_max` condition enters.

## 2. All geodesic types reduce to one radial identity

By spherical symmetry every geodesic lies in a plane; choose the equatorial plane. Let an overdot
denote affine parameter and normalize

\[
g(\dot\gamma,\dot\gamma)=\epsilon,
\qquad \epsilon=-1,0,+1
\]

for timelike, null, and spacelike geodesics. The Killing constants are

\[
E=f\dot t,
\qquad L=r^2\dot\varphi.
\]

Direct Christoffel reconstruction and the normalization independently give

\[
\boxed{
\dot r^2=E^2+\epsilon f-\frac{fL^2}{r^2}.
}
\]

Differentiation agrees with the radial geodesic equation:

\[
\ddot r
=\frac{\epsilon}{2}f'
-\frac{L^2}{2}\left(\frac{f'}{r^2}-\frac{2f}{r^3}\right).
\]

This covers radial and nonradial trajectories; `L=0` is only one subcase.

## 3. The center is crossed, avoided, or approached only lawfully

G204 established that `phi` is analytic in `r^2` and

\[
f=1+O(r^2).
\]

In Cartesian spatial coordinates,

\[
g_{ij}=\delta_{ij}
+\frac{f^{-1}-1}{r^2}x_i x_j
\]

is analytic. Thus `r=0` is an ordinary smooth point, not a boundary. A radial geodesic that reaches
it continues uniquely through the Cartesian chart. A geodesic with `L!=0` cannot reach it because
the `fL^2/r^2` term creates the usual centrifugal turning barrier. Neither case is incomplete.

## 4. Every outer-reaching geodesic has infinite affine length

As `r->infinity`,

\[
\phi\to+\infty,
\qquad f\to0.
\]

### Nonzero energy

For every finite `E!=0`, finite `L`, and every `epsilon`,

\[
f\left(\epsilon-\frac{L^2}{r^2}\right)\to0.
\]

Hence beyond some finite radius,

\[
\frac{E^2}{2}\le \dot r^2\le\frac{3E^2}{2}.
\]

An escaping geodesic therefore requires

\[
|\lambda-\lambda_0|
\ge \sqrt{\frac{2}{3}}\frac{|r-r_0|}{|E|}
\longrightarrow\infty.
\]

### Zero energy

A nonzero causal geodesic cannot have `E=0`: the timelike radial square is strictly negative, while
the null one is nonpositive and vanishes only for the zero tangent. The remaining case is spacelike.
For `E=0` and sufficiently large `r>|L|`,

\[
\dot r^2=f\left(1-\frac{L^2}{r^2}\right)\le f,
\]

so

\[
\frac{d\lambda}{dr}\ge\frac1{\sqrt f}=e^\phi.
\]

Its affine length diverges even faster.

### Finite-radius imprisonment

If a geodesic remains in a bounded radial interval away from the center, `f` has positive finite
upper and lower bounds. The constants `E,L,epsilon` bound `tdot`, the physical angular velocity, and
`rdot`, so the geodesic state stays in a compact subset of the smooth tangent bundle on each finite
affine interval. If the interval includes `r=0`, then either `L!=0` excludes approach to the center,
or `L=0` invokes the smooth Cartesian-center continuation proved in Section 3. After that chart
change the same smooth-spray extension theorem applies. Turning, oscillatory, circular, and
center-crossing trajectories therefore do not create incompleteness.

The three cases exhaust every maximal geodesic. The supplied metric is therefore timelike, null,
spacelike, and hence fully geodesically complete for every registered `n,a,r0`.

## 5. Optical completeness and global hyperbolicity

Because `f>0` everywhere on the manifold, the metric is conformal to

\[
f^{-1}g=-dt^2+h_{\rm opt},
\]

where

\[
h_{\rm opt}
=\frac{dr^2}{f^2}+\frac{r^2}{f}d\Omega^2.
\]

The center is smooth. Any spatial curve escaping to unbounded `r` has optical length bounded below
by

\[
\int\frac{|dr|}{f}.
\]

Outside the quiet radius `phi>0`, so `0<f<1`; the integral diverges, in fact super-exponentially.
Thus the optical Riemannian metric is complete.

For the ultrastatic representative, `t` is a time function and a causal curve parametrized by `t`
satisfies

\[
\left|\frac{dx}{dt}\right|_{h_{\rm opt}}\le1.
\]

If an inextendible causal curve had a finite upper or lower `t` endpoint, its spatial projection
would have finite optical length and would converge by completeness, allowing the causal curve to
extend. Therefore `t` ranges from minus to plus infinity along every inextendible causal curve and
each `t=constant` slice is Cauchy. The ultrastatic representative is globally hyperbolic. Positive
conformal rescaling preserves its causal curves, so the original metric is also globally
hyperbolic. This is an evaluated property of the supplied history, not a newly adopted postulate.

## 6. Horizon and boundary precision

The static Killing field satisfies

\[
g(\partial_t,\partial_t)=-f<0
\]

at every finite radius. There is no finite-radius Killing horizon. The limit `f->0` occurs only at
`r->infinity`, which is at infinite affine, ordinary spatial, and optical reach.

This does not by itself define conformal infinity, prove maximal analytic inextendibility, or settle
event-horizon language relative to a separately defined asymptotic boundary. It is not standard
asymptotic flatness and is not identified with `X_max`.

## 7. A new parameter-dependent null-trapping stratum

For a nonradial null geodesic the effective potential is

\[
V_{\rm null}=\frac{L^2f}{r^2}.
\]

A circular null orbit requires

\[
r f'-2f=0
\quad\Longleftrightarrow\quad
p:=r\phi'=-1.
\]

Put `y=x^2`. On the only interval where `p<0`, namely `0<y<1/(n+1)`,

\[
-p=\frac{a}{2^{n-1}}q_n(y),
\qquad
q_n(y)=y(1-y)^{n-1}[1-(n+1)y].
\]

For general odd `n>=3`,

\[
q_n'(y)=(1-y)^{n-2}
\left[(n+1)^2y^2-(3n+2)y+1\right].
\]

The smaller quadratic root lies strictly inside `0<y<1/(n+1)` and the larger root lies beyond that
interval. Thus `q_n'` is positive before the smaller root and negative afterward. Since `q_n` is
positive inside and zero at both endpoints, it has exactly one maximum at

\[
y_*(n)=
\frac{3n+2-\sqrt{n(5n+4)}}{2(n+1)^2}.
\]

Define

\[
\boxed{
a_{\rm crit}(n)=\frac{2^{n-1}}{q_n(y_*)}.
}
\]

Then:

- `a<a_crit`: no circular null orbit;
- `a=a_crit`: one degenerate circular null orbit;
- `a>a_crit`: two circular null orbits.

At a root,

\[
V_{\rm null}''=-\frac{2V_{\rm null}}r p'.
\]

The inner root has `p'<0` and is a stable minimum; the outer root has `p'>0` and is an unstable
maximum. These trapped orbits are complete because they remain in a smooth compact region.

For reference, the first thresholds are approximately

| n | `a_crit(n)` |
|---:|---:|
| 3 | 81.9515544384 |
| 5 | 526.712128219 |
| 7 | 2901.82466951 |
| 9 | 14786.2777304 |
| 11 | 71859.2830685 |

The threshold is independent of `r0`; the orbit radii scale with `r0`. This is an exact causal
stratification, not a parameter selection or observational fit. The displayed derivative and root
argument prove the result for every odd `n>=3`. The finite order lists in the scripts are numerical
and symbolic regression checks, not the proof of the universal quantifier.

## Maximum conclusion

The exact G204 witness family supplies a smooth, fully geodesically complete, globally hyperbolic
static spacetime for every registered parameter value. Its null-trapping content changes at an
exact amplitude threshold. The theorem does not select the family, its parameters, a physical UDT
history, maximal extension, transfer, observations, or `X_max`.

## Evidence-type precision

The general completeness, optical-completeness, global-hyperbolicity, and all-odd-`n` results above
are analytic theorems. A fresh external mathematical review found the arguments adequate and
retained the landing. The production script mechanizes the Christoffel, first-integral, limit,
lower-bound, and sampled trapping algebra. The separate 10,000-case implementation independently
checks the algebraic core only. Neither finite script is represented as a machine proof of the
global theorems or of an infinite parameter quantifier.
