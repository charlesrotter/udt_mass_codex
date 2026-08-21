# G202 exact derivation — quiet overlap, profile families, and anchors

Date: 2026-08-21

## 1. Logarithmic radial variable

On a supplied positive radial reference scale \(r_0\), define

\[
s=\log(r/r_0),
\qquad
P=\frac{d\phi}{ds},
\qquad
Q=\frac{d^2\phi}{ds^2}.
\]

Then

\[
p=r\phi'=P,
\qquad
q=r^2\phi''=Q-P.
\]

G201's exact primary-metric amplitudes become

\[
\boxed{A_\parallel=e^{-2\phi}(2P^2+2P-Q),}
\]

\[
\boxed{A_\perp=1-e^{-2\phi}(1+P).}
\]

## 2. Exact quiet-overlap condition

At a zero-depth crossing \(\phi=0\),

\[
A_\parallel=2P^2+2P-Q,
\qquad
A_\perp=-P.
\]

Therefore

\[
\boxed{A_\parallel=A_\perp=0
\quad\Longleftrightarrow\quad
\phi=P=Q=0.}
\]

The quiet middle is second-order flat in logarithmic radius.  This is metric-derived and is
stronger than merely requiring \(\phi\approx0\).

## 3. Analytic sign-changing crossings

Suppose \(\phi(s)\) is real analytic near \(s=0\), changes sign there, and is not identically zero.
Its first nonzero Taylor term must have odd order.  Quiet overlap removes orders one and two, so
the first possible order is an odd integer \(n\ge3\).

The minimal nondegenerate control is

\[
\phi=a s^3,
\qquad a>0.
\]

It is monotone because \(P=3as^2\ge0\), is regular at every finite \(s\), and reaches
\(-\infty\) and \(+\infty\) at the two ends.  It is a `CHOSE_CONTROL`, not a selected UDT history.

Its local amplitudes are

\[
A_\parallel
=e^{-2as^3}(18a^2s^4+6as^2-6as),
\]

\[
A_\perp
=1-e^{-2as^3}(1+3as^2).
\]

Near the overlap,

\[
A_\parallel=-6as+6as^2+O(s^4),
\]

\[
A_\perp=-3as^2+2as^3+O(s^5),
\]

while the reciprocal-block contrast begins at

\[
\mathcal C_{\rm rec}=2a^2s^6+O(s^{12}).
\]

Thus even a perfectly quiet central jet does not make every instrument widen at the same order.

## 4. Infinite native profile family

For nonnegative coefficients and \(a>0\),

\[
\phi(s)=a s^3+b s^5+c s^7+\cdots
\]

is odd and has

\[
P=s^2(3a+5bs^2+7cs^4+\cdots)\ge0.
\]

Every member has the same quiet second jet and two-sided reciprocal growth.  The higher odd terms
change the transition shape and angular volumes.  Hence the metric requirements define a lawful
profile class, not one formula.

For smooth nonanalytic histories, the freedom is larger: a sign-changing function can be flat to
all orders at the crossing.  The odd-order statement is therefore explicitly analytic or
finite-order-nondegenerate, not a theorem about every smooth function.

## 5. Why finite anchors do not select the global profile

For any finite collection of anchor points and derivative orders, construct a smooth perturbation
whose corresponding jets vanish at every anchor.  The recorded analytic example

\[
h(s)=e^{-s^2}(s+1)^3s^3(s-1)^3
\]

preserves value, first derivative, and second derivative at \(s=-1,0,1\), decays at both ends, and
is not identically zero.  Therefore

\[
\phi_\epsilon(s)=a s^3+\epsilon h(s)
\]

shares those finite anchors and asymptotics for every \(\epsilon\).  For sufficiently small
\(|\epsilon|\), monotonicity is preserved because the perturbation derivative is bounded relative
to the positive base derivative away from the quiet point and vanishes to adequate order at it.

The same construction generalizes using products of sufficiently high powers at any finite anchor
set.  Consequently, finite observations can calibrate coefficients **after** a finite-dimensional
profile family is independently justified, but cannot derive an unrestricted smooth history.

## 6. Dimensional role of c_E and G_obs

Write dimensions as powers of length \(L\), mass \(M\), and time \(T\):

\[
[c_E]=LT^{-1},
\qquad
[G_{\rm obs}]=L^3M^{-1}T^{-2}.
\]

No monomial in \(c_E\) and \(G_{\rm obs}\) alone has dimension \(L\): eliminating the mass power
forces the power of \(G_{\rm obs}\) to zero, and eliminating time then forces the power of
\(c_E\) to zero.

With a mass anchor \(M_*\), dimensional analysis permits

\[
r_0\propto\frac{G_{\rm obs}M_*}{c_E^2}.
\]

With a density anchor \(\rho_*\), it permits

\[
r_0\propto\frac{c_E}{\sqrt{G_{\rm obs}\rho_*}}.
\]

These are dimensional candidates only.  Neither the proportionality, the relevant mass/density,
nor its physical role follows from dimensional analysis or the present metric algebra.

## 7. Bounded landing

```text
QUIET_OVERLAP_FORCES_SECOND_ORDER_FLATNESS
__TWO_SIDED_GROWTH_HAS_INFINITE_NATIVE_PROFILES
__ANCHORS_CALIBRATE_BUT_DO_NOT_DERIVE_HISTORY
```

The kernel is not missing another mixing mechanism.  What remains for applications is a typed
choice or future derivation of the radial profile class and its legitimate calibration—not a
modification of the reciprocal pair law.
