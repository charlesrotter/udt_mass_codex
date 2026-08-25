# G257 exact derivation — GR quiet-limit embedding

Date: 2026-08-25

## 1. Supplied primary metric

On one connected static spherical interval with `f>0`, take

\[
ds^2=-f(r)c_E^2dt^2+f(r)^{-1}dr^2+r^2d\Omega^2,
\qquad
f=e^{-2\phi}.
\]

The determinant is

\[
\det g=-c_E^2r^4\sin^2\theta,
\]

independent of `f`. This is the founded primary metric form; no profile equation has been used.

## 2. Imported GR vacuum comparison condition

A direct Christoffel-to-Ricci calculation gives the mixed Einstein components

\[
G^t{}_t=G^r{}_r
=\frac{rf'+f-1}{r^2},
\]

\[
G^\theta{}_\theta=G^\varphi{}_\varphi
=\frac12f''+\frac{f'}r.
\]

Define the dimensionless reduced residuals

\[
\mathcal E_0:=r^2G^t{}_t=rf'+f-1,
\]

\[
\mathcal E_1:=r^2G^\theta{}_\theta=rf'+\frac{r^2}{2}f''.
\]

They obey the exact dependence identity

\[
\boxed{r\frac{d\mathcal E_0}{dr}=2\mathcal E_1.}
\]

Thus, inside this already restricted determinant-one primary family, the vacuum system has one
independent radial residual. Solving `E0=0` gives the complete family

\[
\boxed{f(r)=1+\frac Cr.}
\]

Direct substitution zeros the full Ricci and Einstein tensors. No angular equation imposes an
additional condition.

The integration constant `C` is free. Writing `C=-r_s` gives the familiar positive-mass exterior
form

\[
f=1-\frac{r_s}{r},
\]

but the identification

\[
r_s=\frac{2G_{\rm obs}M}{c_E^2}
\]

is a conditional GR mass/source attachment, not a result of this vacuum metric calculation or a
UDT source law.

## 3. Native phi-jet form of the GR residual

Let

\[
p=r\phi',
\qquad
\zeta=r^2\phi''.
\]

Since `f=e^{-2 phi}`,

\[
\boxed{\mathcal E_0=e^{-2\phi}(1-2p)-1,}
\]

\[
\boxed{\mathcal E_1=e^{-2\phi}(2p^2-2p-\zeta).}
\]

These are exact bounded measures of departure from the static spherical GR vacuum branch. They
are not a proposed UDT extension equation. Their one-residual dependence is a property of the
primary symmetry reduction and does not establish the rank of a four-dimensional parent law.

## 4. Completed reciprocal kernel on the GR branch

In the positive-mass notation define

\[
u=\frac{r_s}{r},
\qquad
f=1-u,
\qquad
\phi=-\frac12\log(1-u).
\]

For matched static endpoint calibrations,

\[
V(r)=-\frac12\log f(r),
\qquad
\delta_{AB}=V(r_B)-V(r_A).
\]

The dimensionless reciprocal outputs are therefore

\[
\boxed{q_{AB}=e^{-2\delta_{AB}}=\frac{f(r_B)}{f(r_A)},}
\]

\[
\boxed{\chi_{AB}=\tanh\delta_{AB}
=\frac{f(r_A)-f(r_B)}{f(r_A)+f(r_B)}.}
\]

For the matched local static clock, `T=sqrt(f)=e^{-phi}` and

\[
\widehat\Phi_{\rm pair}=\phi
\]

in the declared unit calibration. No P1 profile, angular correction, transfer function, or fitted
coefficient has been added.

## 5. Native angular interlock on the same branch

The exact GR-branch jets are

\[
p=-\frac{u}{2(1-u)},
\qquad
\zeta=\frac{u(2-u)}{2(1-u)^2}.
\]

Substitution into the already derived primary angular amplitudes

\[
A_\parallel=e^{-2\phi}(2p^2+p-\zeta),
\qquad
A_\perp=1-e^{-2\phi}(1+p)
\]

gives

\[
\boxed{A_\parallel=-\frac32u,}
\qquad
\boxed{A_\perp=+\frac32u,}
\qquad
\boxed{A_\parallel+A_\perp=0.}
\]

These `A` variables are the exact G201 primary angular amplitudes, not a claim about every possible
GR tidal eigenvalue. They are nonzero on a nonflat GR exterior and arise from the same metric
without a post-kernel orchestra.

For `|u|<<1`,

\[
\phi=\frac u2+\frac{u^2}{4}+O(u^3),
\qquad
p=-\frac u2-\frac{u^2}{2}+O(u^3),
\qquad
\zeta=u+\frac32u^2+O(u^3).
\]

The angular amplitudes are exactly first order in `u`. Therefore GR quietness on a weak exterior is
not the statement `phi=p=zeta=0` at every finite radius. It is the conjunction of the exact GR
residual `E0=0` with a small dimensionless field strength `|u|<<1`. Exact zero depth and zero
angular amplitude describe the flat/asymptotic point, not the whole GR branch.

## 6. Curvature check

The Ricci tensor vanishes on `f=1-r_s/r`, but the spacetime is not flat:

\[
R_{abcd}R^{abcd}=\frac{12r_s^2}{r^6}.
\]

This confirms that the GR overlap retains genuine geometry while the GR vacuum residual vanishes.

## 7. Exact conclusion

The primary UDT metric contains the full one-parameter static spherical GR vacuum exterior. The
completed reciprocal kernel and native angular response evaluate that branch without scaffolding.
The newly adopted W3 premise therefore passes this first bounded compatibility test.

What remains absent is the UDT parent law determining how the full metric departs from
`E0=E1=0` outside the quiet regime and how that law extends through matter, time dependence, and
nonspherical sectors.
