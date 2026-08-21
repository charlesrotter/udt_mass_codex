# G203 exact derivation — invariant quiet-overlap descriptors

Date: 2026-08-21

## Landing

```text
INVARIANT_AFTER_AREAL_AND_DEPTH_CALIBRATION
__FOUNDING_DOES_NOT_SELECT_ORDER_LOCATION_OR_STEEPNESS
__OBSERVATIONS_MAY_CALIBRATE_A_DECLARED_FAMILY
```

## 1. Remove the arbitrary radial-chart appearance

In the declared primary spherical metric, the symmetry-orbit area is

\[
\mathcal A(r)=4\pi r^2.
\]

If the quiet orbit has area \(\mathcal A_0=4\pi r_0^2\), then

\[
s=\frac12\log\frac{\mathcal A}{\mathcal A_0}=\log\frac r{r_0}.
\]

This is not an arbitrary radial chart once the spherical metric and quiet orbit are supplied. If a
second positive coordinate \(R\) represents the same metric in areal form, equality of the orbit
terms gives

\[
R^2d\Omega^2=r^2d\Omega^2,
\]

so \(R=r\). Thus the quiet radius is recovered geometrically from its orbit area,

\[
r_0=\sqrt{\mathcal A_0/(4\pi)}.
\]

This proves that \(r_0\) is not removable areal-coordinate gauge. It does not prove which supplied
history Nature realizes or what numerical value its quiet orbit has.

## 2. The local analytic descriptors

Let a nontrivial analytic crossing have

\[
\phi(s)=a_n s^n+a_{n+1}s^{n+1}+\cdots,
\qquad a_n\ne0.
\]

G202's quiet condition removes orders zero, one, and two. Sign change requires odd leading order.
Therefore

\[
\boxed{n\in\{3,5,7,\ldots\}.}
\]

Under any analytic germ change

\[
s=c_1u+c_2u^2+\cdots,
\qquad c_1\ne0,
\]

the composed profile begins

\[
\phi(s(u))=a_nc_1^n u^n+O(u^{n+1}).
\]

Hence the vanishing order \(n\) is invariant even under this broader coordinate class. The
coefficient transforms unless the radial calibration is fixed. In the log-areal variable above,
the leading coefficient is the dimensionless metric descriptor

\[
\boxed{a_n=\frac1{n!}\left.\frac{d^n\phi}{ds^n}\right|_{s=0}.}
\]

The founded depth unit fixes the vertical normalization of \(\phi\); the areal orbit ratio fixes
the horizontal normalization of \(s\). Neither statement fixes the value of \(a_n\).

Reciprocal reversal sends \(\phi\mapsto-\phi\). It preserves \(n\), \(r_0\), and \(|a_n|\), while
reversing the sign of the leading coefficient. It does not by itself define an involution
\(s\mapsto-s\) on the radial history.

## 3. Exact counterfamily to numerical selection

For every odd \(n\ge3\), \(r_0>0\), and \(a>0\), define

\[
\boxed{\phi_{n,r_0,a}(r)=a\,[\log(r/r_0)]^n.}
\]

On \(r>0\):

\[
\phi(r_0)=\phi_s(r_0)=\phi_{ss}(r_0)=0,
\]

\[
\phi_s=na s^{n-1}\ge0,
\]

and, because \(n\) is odd,

\[
s\to-\infty\Rightarrow\phi\to-\infty,
\qquad
s\to+\infty\Rightarrow\phi\to+\infty.
\]

The corresponding primary metric is Lorentzian and nondegenerate at every finite positive radius.
The founded matrices still obey

\[
D(\phi_2)D(\phi_1)=D(\phi_1+\phi_2),
\qquad
D(-\phi)=D(\phi)^{-1},
\qquad
\det D=1.
\]

The reciprocal algebra contains no \(n\), \(r_0\), or \(a\). Since all triples pass the same
founded and quiet-overlap gates while differing in invariant descriptors, those gates do not
select their values.

The family is a counterfamily, not the physical solution space. Higher Taylor coefficients and
smooth nonanalytic possibilities remain.

## 4. Reversal does not force a globally odd score

The local profile

\[
\phi(s)=s^3+b s^4
\]

has zero second jet and changes sign near zero. Its derivative factors as

\[
\phi_s=s^2(3+4bs),
\]

so it is monotone in a sufficiently small neighborhood. But

\[
\phi(-s)+\phi(s)=2bs^4,
\]

which is nonzero when \(b\ne0\). Arrow reversal supplies \(-\phi\); it does not prove that the
history argument is also reflected. A globally odd radial profile therefore requires a separately
owned radial involution or symmetry.

## 5. Exact role of observations and dimensional anchors

Within a declared finite-dimensional profile family:

- an observed quiet-orbit area calibrates \(r_0\);
- sufficiently resolved local jets can calibrate \(n\) and \(a_n\);
- additional observations can calibrate the retained higher coefficients.

That is empirical selection of a metric realization, not a post-metric correction to the kernel.
Finite observations still do not derive an unrestricted smooth function.

The dimensional results remain

\[
[c_E]=LT^{-1},\qquad [G_{\rm obs}]=L^3M^{-1}T^{-2}.
\]

They cannot form a length alone. Adding a mass or density permits

\[
\frac{G_{\rm obs}M}{c_E^2},
\qquad
\frac{c_E}{\sqrt{G_{\rm obs}\rho}},
\]

respectively. These combinations can calibrate a proposed realization only after a lawful UDT
identification; dimensional analysis does not choose the identification or coefficient.

## Maximum conclusion

The order, quiet-orbit area, and log-areal leading steepness are well-typed metric descriptors after
the declared calibrations. They are not coordinate fluff, and they are not new kernel mechanisms.
The present founding and local metric identities constrain their class but do not select numerical
values or a global profile.
