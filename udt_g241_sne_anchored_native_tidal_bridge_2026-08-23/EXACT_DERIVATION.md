# G241 exact derivation — SNe anchor to native tidal response

Date: 2026-08-23

## 1. Registered carrier

For the frozen G237 depth interval, set

\[
t(\phi)=2\frac{\phi-\phi_0}{\phi_1-\phi_0}-1.
\]

For each preregistered degree \(d\in\{2,3,4\}\), the anchored relative state is

\[
\theta_d(\phi)=\sum_{k=1}^d c_k\bigl[T_k(t(\phi))-T_k(-1)\bigr].
\]

The coefficients are the full-covariance GLS solution. No angular coefficient, smoothing
parameter, physical-profile optimizer, or held-out outcome enters.

## 2. Exact radial-to-tidal identity

Define

\[
s(\phi)=\log\frac{R(\phi)}{R(\phi_0)}=\frac{\log 10}{5}\theta_d(\phi).
\]

On a branch with \(s'>0\), inverse differentiation gives

\[
p:=R\frac{d\phi}{dR}=\frac1{s'},
\qquad
q:=R^2\frac{d^2\phi}{dR^2}
=-\frac{s''+(s')^2}{(s')^3}.
\]

Substituting these into the G127 primary-metric curvature contrast gives

\[
\boxed{
J(\phi):=R^2\Xi
=e^{-2\phi}\left(2p^2-q+2p\right)-\left(1-e^{-2\phi}\right).
}
\]

Multiplying \(R\) by any positive constant leaves \(p\), \(q\), and \(J\) unchanged. Thus the
absolute SNe ruler zero point is not needed for this local dimensionless angular response.

## 3. Preregistered evaluation

| coefficients | chi-square | dof | 0.999 ceiling | minimum \(s'\) | result |
|---:|---:|---:|---:|---:|---|
| 2 | 1034.00221658 | 9 | 27.87716487 | -2.01016470 | inadequate and noninvertible |
| 3 | 176.31976397 | 8 | 26.12448156 | 0.71523495 | invertible but inadequate |
| 4 | 29.17846576 | 7 | 24.32188635 | -1.41016629 | inadequate and noninvertible |

No registered degree passes every gate. The exact landing is therefore

```text
NO_REGISTERED_SMOOTH_ANCHOR_ADEQUATE__STOP_BEFORE_BOSS
```

The degree-four residual is numerically nearer the ceiling, but it is still outside the frozen
contract and develops a negative derivative. It is not accepted or repaired.

## 4. Meaning

The radial-to-angular identity is retained. What fails is only the attempt to compress the frozen
SNe relative state into this particular two-to-four-coefficient polynomial carrier. No conclusion
about the unrestricted continuous history, the reciprocal kernel, BOSS, BAO, or UDT follows.
