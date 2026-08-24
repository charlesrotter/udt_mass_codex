# G242 exact derivation — coefficient-free quiet family

Date: 2026-08-24

## 1. Bounded conditional identification

G201 uses the primary static-spherical metric

\[
g=-f(r)(dx^0)^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad f=e^{-2\phi}.
\]

G236/G237 conditionally identify the processed SNe state with relative areal radius on the same
bounded central-static query. G241 retains the conditional inverse map from one smooth monotone
relative \(R(\phi)\) to the G127 local tidal contrast. G242 does not globalize that identification.

## 2. Exact simultaneous cancellation

G201 derives both dimensionless angular modes

\[
A_\parallel=e^{-2\phi}(2p^2+p-q),
\qquad
A_\perp=1-e^{-2\phi}(1+p),
\]

with \(p=r\phi'\) and \(q=r^2\phi''\). They vanish simultaneously for

\[
f(r)=1+Cr^2.
\]

The frozen SNe interval has positive pair depth. On the conditional positive-depth branch,
\(C<0\), so

\[
r(\phi)^2=\frac{1-e^{-2\phi}}{-C}.
\]

After anchoring at \(\phi_0\), both \(C\) and the absolute ruler cancel:

\[
\boxed{
\theta_{\rm quiet}(\phi)
=5\log_{10}\frac{r(\phi)}{r(\phi_0)}
=\frac52\log_{10}
\frac{1-e^{-2\phi}}{1-e^{-2\phi_0}}.
}
\]

This is not a fitted profile.

## 3. Independent differential check

Writing \(s=\log[r(\phi)/r(\phi_0)]\),

\[
s'=\frac1{e^{2\phi}-1}>0,
\qquad
p=\frac1{s'}=e^{2\phi}-1,
\]

and

\[
q=-\frac{s''+(s')^2}{(s')^3}=2p^2+p.
\]

Substitution in the G241 dimensionless contrast

\[
J=e^{-2\phi}(2p^2-q+2p)-(1-e^{-2\phi})
\]

gives \(J=0\) identically.

## 4. Frozen full-covariance result

For the eleven non-anchor G237 coordinates,

\[
\chi^2=(\theta-\theta_{\rm quiet})^T
C_\theta^{-1}(\theta-\theta_{\rm quiet})
=8519.009211032242.
\]

There are eleven coordinates and no fitted parameters. The preregistered 0.999 ceiling is

\[
\chi^2_{0.999,11}=31.264133620239985.
\]

Therefore the exact classification is

```text
EXACT_QUIET_SUBFAMILY_INCOMPATIBLE__SMALL_NONZERO_RESPONSE_REMAINS_OPEN
```

The exact-zero family is rejected on this processed conditional state. No magnitude bound on a
small nonzero tidal history follows.
