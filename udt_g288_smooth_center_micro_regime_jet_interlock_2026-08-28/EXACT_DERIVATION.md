# G288 exact derivation — smooth-center micro-regime jet interlock

Date: 2026-08-28

## 1. Evidence reset and scope

This derivation does not trust an earlier audit formula.  It starts from the current bounded primary
metric in dimension-matched time \(x^0=c_Et\),

\[
ds^2=-f(r)(dx^0)^2+\frac{dr^2}{f(r)}+r^2d\Omega^2,
\qquad f=e^{-2\phi}>0,
\]

and rebuilds the inverse metric, Levi-Civita connection, Riemann tensor, Ricci tensor, scalar
invariants, nonradial null screen, static acceleration, and radial null normalization.  Prior G201,
G262, G264, and historical center formulas are comparison targets only.

The local center class is the analytic even germ

\[
f(r)=1+c_2r^2+c_4r^4+c_6r^6+c_8r^8+O(r^{10}).
\]

Analytic evenness is a bounded method choice, not a universal physical postulate.

## 2. Fresh metric reconstruction

Direct tensor contraction gives

\[
R=-f''-\frac{4f'}r+\frac{2(1-f)}{r^2},
\]

\[
R_{abcd}R^{abcd}
=(f'')^2+4\left(\frac{f'}r\right)^2
+4\left(\frac{f-1}{r^2}\right)^2,
\]

and

\[
C_{abcd}C^{abcd}
=\frac{\left(r^2f''-2rf'+2f-2\right)^2}{3r^4}.
\]

For a normalized nonradial future null vector whose spatial direction has nonzero angular sine
\(s_\alpha\), direct contraction with its two orthonormal screen vectors gives

\[
T_\parallel
=\frac{s_\alpha^2}{2r}\left(rf''-f'\right),
\qquad
T_\perp
=\frac{s_\alpha^2}{2r^2}\left(rf'-2f+2\right),
\]

with zero off-diagonal term.  Removing only the declared incidence and areal factors produces

\[
A_\parallel=\frac{r^2f''-rf'}2,
\qquad
A_\perp=1-f+\frac{rf'}2.
\]

These agree with the older banked expressions, but the agreement is a regression result, not an
input.

The static lapse is \(N=\sqrt f\).  Computing \(a^b=U^a\nabla_aU^b\) from the rebuilt connection
gives

\[
a_{\hat r}=\frac{f'}{2\sqrt f}=N'.
\]

The geometric areal mass-aspect variable is defined only by

\[
g^{-1}(dr,dr)=f=1-\frac{2\mu}{r},
\qquad
\mu=\frac r2(1-f).
\]

It is a change of metric variables, not a physical mass law.

Radial metric-null curves satisfy

\[
\frac{dr}{dt}=\pm c_E f.
\]

For a static normalized clock and ruler,

\[
d\tau=\sqrt f\,dt,
\qquad
d\ell=\frac{dr}{\sqrt f},
\qquad
\left|\frac{d\ell}{d\tau}\right|=c_E.
\]

Thus the changing coordinate slope is not a changing local normalized signal speed.

## 3. Exact center hierarchy

The reciprocal presentation begins as

\[
\phi
=-\frac{c_2}{2}r^2
+\left(\frac{c_2^2}{4}-\frac{c_4}{2}\right)r^4
+O(r^6),
\]

while

\[
N
=1+\frac{c_2}{2}r^2
+\left(\frac{c_4}{2}-\frac{c_2^2}{8}\right)r^4
+O(r^6),
\]

\[
a_{\hat r}=c_2r+\left(2c_4-\frac{c_2^2}{2}\right)r^3+O(r^5),
\]

and

\[
\mu=-\frac{c_2}{2}r^3-\frac{c_4}{2}r^5+O(r^7).
\]

The angular modes are more strongly suppressed:

\[
\boxed{A_\parallel=4c_4r^4+12c_6r^6+24c_8r^8+O(r^{10}),}
\]

\[
\boxed{A_\perp=c_4r^4+2c_6r^6+3c_8r^8+O(r^{10}).}
\]

The quadratic coefficient cancels exactly from both.  If \(c_4\ne0\), their first nonzero
coefficient ratio is fixed:

\[
\frac{A_\parallel}{A_\perp}\longrightarrow4.
\]

The invariant series begin as

\[
R=-12c_2-30c_4r^2-56c_6r^4-90c_8r^6+O(r^8),
\]

\[
C_{abcd}C^{abcd}=12c_4^2r^4+80c_4c_6r^6+O(r^8),
\]

\[
R_{abcd}R^{abcd}=24c_2^2+120c_2c_4r^2+O(r^4).
\]

Therefore \(c_2\) owns the leading reciprocal clock, acceleration, curvature, and geometric
mass-aspect germ, while the first angular/Weyl departure depends on the independent coefficient
\(c_4\).

## 4. General coefficient theorem

For one even monomial perturbation

\[
f=1+c_{2k}r^{2k},
\]

the fresh formulas give

\[
A_\parallel=2k(k-1)c_{2k}r^{2k},
\]

\[
A_\perp=(k-1)c_{2k}r^{2k},
\]

\[
R=-2(2k+1)(k+1)c_{2k}r^{2k-2}.
\]

The \(k=1\) term is therefore invisible to both angular channels.  The first possible angular term
is \(k=2\), or quartic order in the regular metric germ.

## 5. Exact quadratic class

For

\[
f=1+Cr^2,
\]

the direct tensor reconstruction gives

\[
A_\parallel=A_\perp=0,
\qquad
R_{ab}=-3C g_{ab},
\]

\[
R=-12C,
\qquad
R_{abcd}R^{abcd}=24C^2,
\qquad
C_{abcd}C^{abcd}=0.
\]

It is an exact constant-sectional-curvature family with sectional curvature \(K=-C\) in the
registered Riemann convention.  For \(C>0\),

\[
\phi=-\frac12\log(1+Cr^2)<0
\]

for every \(r>0\), yet its angular screen tide vanishes exactly.  This is a native metric class,
not a microphysical selection theorem.

## 6. What the solution space has actually supplied

Smooth-center regularity does give a nontrivial local universality statement: every analytic even
regular germ is tangent to the exact quadratic zero-tide constant-curvature family.  But it gives
only a partial interlock.  The coefficient \(c_2\) remains free, and \(c_4,c_6,\ldots\) independently
control departure from that leading class.

For \(c_2>0\), the profile is negative sufficiently near but away from the center.  The exact center
itself returns to \(\phi=0\).  Nothing in this local theorem identifies a Planck radius, selects the
coefficient values, turns \(\mu\) into physical mass, or chooses a global trough/history.

## Landing

```text
PARTIAL_CENTER_INTERLOCK_ONLY
__QUADRATIC_NEGATIVE_PROFILE_GERM_IS_ZERO_TIDE_CONSTANT_CURVATURE
__ANGULAR_TIDE_BEGINS_AT_INDEPENDENT_QUARTIC_JET
__NO_PLANCK_SCALE_OR_HISTORY_SELECTED
```
