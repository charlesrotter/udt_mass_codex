# G204 exact derivation — global regularity and asymptotic profile class

Date: 2026-08-21

## Landing

```text
SMOOTH_CENTER_EXCLUDES_MONOTONE_TWO_SIDED_LOG_EXTENSION
__EVEN_AREAL_INNER_TROUGH_AND_OUTER_RECIPROCAL_ASYMPTOTE_FAMILY_SURVIVES
__GLOBAL_REGULARITY_DOES_NOT_SELECT_N_R0_OR_A
```

## 1. Full-metric curvature reconstruction

Set the constant clock unit \(c_E=1\) inside curvature invariants and write

\[
ds^2=-f(r)dt^2+\frac{dr^2}{f(r)}+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0.
\]

Direct construction of the Christoffel symbols and four-dimensional Riemann tensor gives

\[
R=-f''-\frac{4f'}r+\frac{2(1-f)}{r^2},
\]

and

\[
\boxed{
K=R_{abcd}R^{abcd}
=f''^2+4\left(\frac{f'}r\right)^2
+4\left(\frac{1-f}{r^2}\right)^2.
}
\]

The coordinate determinant is

\[
\det g=-r^4\sin^2\theta,
\]

independent of \(f\). Every finite positive radius with finite positive \(f\) is therefore in the
regular metric chart. Endpoint limits require separate analysis.

## 2. Necessary regular-center behavior

Every term in \(K\) is nonnegative. If \(K\le C\) near \(r=0\), then

\[
|1-f|\le\frac{\sqrt C}{2}r^2,
\qquad
|f'|\le\frac{\sqrt C}{2}r,
\qquad
|f''|\le\sqrt C.
\]

Hence

\[
f=1+O(r^2),
\qquad
\boxed{\phi=O(r^2).}
\]

For a genuinely smooth spherical center, the metric coefficients must moreover be smooth in
Cartesian coordinates. A sufficient analytic form is that \(\phi\) is analytic in \(r^2\). Then

\[
g_{ij}=\delta_{ij}
+\frac{f^{-1}-1}{r^2}x_i x_j
\]

is smooth because \((f^{-1}-1)/r^2\) is analytic in \(r^2\).

Thus a smooth center is itself zero-depth and quiet. A profile that diverges negatively at
\(r=0\) cannot represent that center in this static areal branch.

## 3. Why the log-monomial extension fails at the center

For odd \(n\ge3\),

\[
\phi_{\log}=a[\log(r/r_0)]^n
\]

has \(\phi\to-\infty\) and \(f\to+\infty\) as \(r\to0\). The angular term alone gives

\[
K\ge \frac{4(1-f)^2}{r^4}\longrightarrow\infty.
\]

Its inward radial spatial length is finite. With \(y=-\log(r/r_0)\),

\[
\int_0^{r_0}e^\phi dr
=r_0\int_0^\infty e^{-y-a y^n}dy<\infty.
\]

Radial null geodesics also reach \(r=0\) in finite affine parameter. Conservation of
\(E=f\dot t\) and nullity imply

\[
\dot r^2=E^2.
\]

The log-monomial center is therefore a finite-affine curvature singularity, not a smooth center.

## 4. Failure and repair of the first bounded-curvature witness

The initially preregistered replacement

\[
\phi=a x^2(x-1)^n,
\qquad x=r/r_0,
\]

has finite center curvature, but its expansion contains the nonzero \(x^3\) coefficient \(an\).
It is not smooth as a rotation-invariant Cartesian scalar. The claim was failed closed and the
repair was separately preregistered at `785b0447`.

The repaired control is

\[
\boxed{
\phi_{n,r_0,a}(r)
=\frac{a}{2^n}x^2(x^2-1)^n,
\qquad n\ge3\text{ odd},\quad a,r_0>0.
}
\]

It is analytic in \(x^2\). Near the center,

\[
\phi=-\frac{a}{2^n}\frac{r^2}{r_0^2}+O(r^4),
\]

and

\[
\boxed{
K(0)=\frac{96a^2}{4^n r_0^4}<\infty.
}
\]

The spatial Cartesian coefficient is finite and analytic. Thus this is a genuine smooth-center
control, not merely a bounded-curvature control.

## 5. The quiet crossing and inner trough

Put \(s=\log(r/r_0)\), so \(x=e^s\). Since

\[
x^2-1=e^{2s}-1=2s+O(s^2),
\]

the repaired profile satisfies

\[
\phi=a s^n+O(s^{n+1}).
\]

It retains the G202 quiet second jet and the G203 leading steepness \(a\).

Its radial derivative factors as

\[
\frac{d\phi}{dx}
=\frac{2a}{2^n}x(x^2-1)^{n-1}\big[(n+1)x^2-1\big].
\]

There is exactly one noncentral inner extremum,

\[
\boxed{
\frac{r_{\min}}{r_0}=\frac1{\sqrt{n+1}},
}
\]

with

\[
\boxed{
\phi_{\min}
=-\frac{a n^n}{2^n(n+1)^{n+1}}<0.
}
\]

The profile begins at the regular zero-depth center, descends to a finite negative trough, rises
through the quiet crossing at \(r_0\), and grows positively outside.

This nonmonotonicity is necessary for any nontrivial negative inner regime with both
\(\phi(0)=0\) and \(\phi(r_0)=0\). A continuous nondecreasing function whose two endpoint values
are both zero must vanish throughout the interval.

## 6. Outer behavior

For both controls, \(\phi\to+\infty\) and \(f\to0\) as \(r\to\infty\). Polynomial derivatives
multiplied by \(f\) vanish faster than the areal powers, so

\[
K\sim\frac4{r^4}\longrightarrow0.
\]

The outer spatial length diverges,

\[
\int^{\infty}e^\phi dr=\infty,
\]

and radial null affine parameter is proportional to \(r\), so the end is also at infinite null
affine reach.

This is a curvature-decaying, infinite-distance reciprocal asymptote of the supplied controls. It
is not standard asymptotic flatness because \(f\not\to1\). It is also not, from these facts alone,
a finite wall, horizon, `X_max`, or selected global completion.

## 7. What global regularity selected

It selected a structural condition:

\[
\phi=O(r^2)\quad\text{and smooth dependence on }r^2\text{ at a regular center}.
\]

It rejected the monotone log-monomial extension and the first merely bounded-curvature repair. It
did not select the discrete order \(n\), quiet radius \(r_0\), steepness \(a\), or a unique global
profile. The repaired counterfamily survives for all of them.

## Maximum conclusion

The primary metric supports a coherent smooth-center/inner-trough/quiet-crossing/outer-asymptote
shape without adding a post-kernel mechanism. The displayed family proves existence and
nonselection; it is not the physical UDT profile or a completion theorem.
