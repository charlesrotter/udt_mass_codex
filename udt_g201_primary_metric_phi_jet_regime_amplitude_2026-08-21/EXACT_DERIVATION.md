# G201 exact derivation — reciprocal magnitude and angular channel volume

Date: 2026-08-21

## 1. Scope

The only ambient input is the primary static-spherical metric

\[
g=-f(r)(dx^0)^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0.
\]

G200 already derives the two same-event nonradial quotient-screen tides.  G201 changes variables;
it does not add a profile or mechanism.

At a normalized source, write

\[
p=r\phi',\qquad q=r^2\phi'',\qquad L=r\sin\alpha,
\]

and remove the supplied incidence and areal factors by defining

\[
A_A=\frac{r^2T_A}{\sin^2\alpha}.
\]

## 2. Exact angular amplitudes

Using

\[
f'=-2f\phi',
\qquad
f''=f(4\phi'^2-2\phi''),
\]

the two G200 modes become

\[
\boxed{A_\parallel=e^{-2\phi}(2p^2+p-q),}
\]

\[
\boxed{A_\perp=1-e^{-2\phi}(1+p).}
\]

Therefore angular volume is not a function of \(\phi\) alone.  It hears the local radial slope and
curvature of the same primary metric history.

## 3. What “quiet middle” actually requires

At \(\phi=0\),

\[
A_\parallel=2p^2+p-q,
\qquad
A_\perp=-p.
\]

Hence both modes vanish if and only if

\[
\boxed{\phi=0,\quad p=0,\quad q=0.}
\]

The value \(\phi=0\) alone is insufficient.  For example,

\[
(\phi,p,q)=(0,1,0)
\quad\Longrightarrow\quad
(A_\parallel,A_\perp)=(3,-1).
\]

Thus the GR-overlap or quiet regime requires a local overlap of the metric history and its first
two radial jets, not merely a zero crossing of the presentation potential.

## 4. Exact cancellation at arbitrary phi

For any supplied value of \(\phi\), both angular modes vanish when

\[
\boxed{p=e^{2\phi}-1,}
\]

\[
\boxed{q=2p^2+p.}
\]

These are not isolated formal jets.  They integrate exactly to

\[
\boxed{f(r)=1+Cr^2}
\]

on every domain where \(f>0\).  Direct substitution into the original G200 tides gives

\[
r f''-f'=0,
\qquad
r f'-2f+2=0,
\]

so

\[
T_\parallel=T_\perp=0.
\]

For \(C>0\), \(\phi\to-\infty\) as \(r\to\infty\) while both angular tides remain zero.  For
\(C<0\), \(\phi\to+\infty\) as the positive-\(f\) domain approaches its finite endpoint, again
with both tides zero.  Therefore neither signed extreme forces angular loudness in the unrestricted
primary-metric profile space.

## 5. Lawful subclasses can still be loud

For the illustrative constant-\(\phi\)-jet subclass \(p=q=0\),

\[
A_\parallel=0,
\qquad
A_\perp=1-e^{-2\phi}.
\]

It is quiet at zero, approaches \(1\) for \(\phi\to+\infty\), and diverges negatively for
\(\phi\to-\infty\).  Other supplied jet histories can amplify, suppress, exchange, or cancel the
two modes.  These are native metric possibilities, not external post-processing, but the metric
form alone does not choose among them.

## 6. The reciprocal channel is different

The founded block on supplied completed depth is

\[
D(\Delta)=\operatorname{diag}(e^{-\Delta},e^{+\Delta}).
\]

An algebraic contrast diagnostic is

\[
\mathcal C_{\rm rec}
=\frac12\operatorname{tr}(D^TD)-1
=\cosh(2\Delta)-1
=2\sinh^2\Delta.
\]

It is even, zero at \(\Delta=0\), and divergent at both signed extremes.  This is not introduced as
a new observable or universal loudness score.  It proves only that the reciprocal block itself has
an intrinsic two-sided magnitude, while angular channels need not march in lockstep with it.

## 7. Bounded landing

```text
TWO_SIDED_RECIPROCAL_MAGNITUDE
__ANGULAR_VOLUME_IS_PHI_JET_DEPENDENT
__NO_LOCKSTEP_LOUDNESS_FORCED
```

The primary metric permits regime-dependent instrument ratios.  G201 does not derive the physical
profile, a universal orchestra norm, observational transfer, `X_max`, time-live completion,
source, action, matter, mass, bootstrap, or signalling.
