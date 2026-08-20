# G186 exact derivation — nonradial completed-pair channel resolution

Date: 2026-08-20

## 1. Bounded metric and supplied query

Use dimension-matched time \(x^0=c_Et\) in the declared primary metric,

\[
g=-e^{-2\phi}(dx^0)^2+e^{2\phi}dr^2+r^2\gamma_{S^2}.
\]

At one event with \(r>0\), supply two angular vectors \(w_0,w_1\in T_\Omega S^2\) and

\[
X_0=\partial_{x^0}+w_0,\qquad X_1=v\partial_r+w_1.
\]

This is a chosen local clock/ruler query slice, not a universal observer selector. Define

\[
A=\gamma(w_0,w_0),\quad B=\gamma(w_1,w_1),\quad
C=\gamma(w_0,w_1),\quad \nu^2=e^{2\phi}r^2A.
\]

These are invariant under changes of angular coordinates and orthonormal angular basis.

## 2. Full pullback

Direct evaluation gives

\[
\boxed{
h=
\begin{pmatrix}
-e^{-2\phi}+r^2A&r^2C\\
r^2C&e^{2\phi}v^2+r^2B
\end{pmatrix}.}
\]

Thus

\[
-h_{00}=e^{-2\phi}(1-\nu^2).
\]

The clock leg is timelike exactly when \(\nu^2<1\). The angular Gram determinant is

\[
AB-C^2=\lvert w_0\wedge w_1\rvert_\gamma^2\ge0.
\]

## 3. Completed density, shift, and depth

Only after the complete pullback is formed, completed-pair Dual Reciprocity gives

\[
\boxed{
m^2=-\det h
=(1-\nu^2)v^2+e^{-2\phi}r^2B-r^4(AB-C^2),}
\]

\[
\boxed{
\beta=\frac{h_{01}}{h_{00}}
=-\frac{e^{2\phi}r^2C}{1-\nu^2},}
\]

and

\[
\boxed{
\Phi=-\frac12\log(-h_{00})
=\phi-\frac12\log(1-\nu^2).}
\]

No scalar remains after \(h\) is supplied. The clock-angular norm \(A\) changes endpoint depth;
the ruler-angular norm \(B\) changes tape density; the cross Gram \(C\) changes shift and tape;
and non-collinearity contributes through the squared angular area \(AB-C^2\). Neither \(B\) nor
\(C\) is appended to \(\Phi\) after normalization.

The apparent negative wedge term cannot destroy regularity when \(X_0\) is timelike and \(X_1\ne0\).
Indeed,

\[
e^{-2\phi}r^2B-r^4(AB-C^2)
=e^{-2\phi}r^2\left[B-e^{2\phi}r^2(AB-C^2)\right],
\]

and \(AB-C^2\le AB\) with \(e^{2\phi}r^2A=\nu^2<1\). Hence the bracket is positive for \(B>0\);
the radial term is positive for \(v\ne0\). Therefore \(m^2>0\) whenever the ruler leg is nonzero.

## 4. Local screen is derived, not fitted

Let \(J=(X_0,X_1)\). On the regular Lorentzian pair plane, the mixed-index projector onto its
ambient orthogonal complement is

\[
\boxed{\Pi=I-J(J^TgJ)^{-1}J^Tg.}
\]

Exact algebra gives

\[
\Pi^2=\Pi,\qquad \Pi J=0,\qquad \Pi^Tg=g\Pi,
\qquad \operatorname{tr}\Pi=2.
\]

Because the ambient metric has index one and the pair plane is Lorentzian, the rank-two image of
\(\Pi\) is positive definite. Thus the local screen and its area metric are fixed by \(g\) and the
supplied germ without a coefficient or independent screen selector.

This local projector is not G119's finite Jacobi map. A finite observed beam still requires its
declared propagation query and curvature integration. G186 does not infer flux or luminosity from
\(\Pi\).

## 5. Static-clock boundary explains G185

For a static clock leg \(w_0=0\), \(\nu=0\) and \(C=0\), so

\[
\boxed{
\Phi=\phi,\qquad
\beta=0,\qquad
m^2=v^2+e^{-2\phi}r^2B.}
\]

The nonradial ruler remains physically live in the tape even though it does not alter the completed
endpoint scalar. The radial boundary is \(B=0\). This is why G185 can reproduce the previous radial
SNe scalar exactly without having turned off the angular metric: its supplied static radial query
does not place angular motion in the clock leg, while the separate finite sky area remains live.

## 6. Endpoint-relative response

For two endpoints in one consistent reciprocal calibration class,

\[
\boxed{
\delta_{AB}=\Phi_B-\Phi_A
=(\phi_B-\phi_A)
-\frac12\log\frac{1-\nu_B^2}{1-\nu_A^2}.}
\]

Thus the metric supplies an exact query-dependent angular contribution without a fitted mixing
law. It is controlled by the angular norm of the calibrated clock legs, not merely by coordinate
radius. Static endpoints recover \(\delta_{AB}=\phi_B-\phi_A\).

As \(\nu^2\to1^-\), \(\Phi\) diverges because the chosen clock leg approaches the null boundary.
This is a local causal-stratum boundary, not a derivation of X_max or a cosmological regime.

## 7. Exact witnesses and covariance

With \(e^{2\phi}=4\), \(r=3\), and \(v=1/2\), take an orthonormal angular basis. For
\(w_0=(1/12,0)\), \(w_1=(1/3,0)\),

\[
h=\begin{pmatrix}-3/16&1/4\\1/4&2\end{pmatrix},
\quad m^2=7/16,\quad \beta=-4/3,\quad \Phi=\log(4/\sqrt3).
\]

For the non-collinear \(w_1=(0,1/3)\),

\[
h=\operatorname{diag}(-3/16,2),\quad m^2=3/8,\quad \Phi=\log(4/\sqrt3).
\]

For the static clock \(w_0=0\), \(w_1=(1/3,0)\),

\[
h=\operatorname{diag}(-1/4,2),\quad m^2=1/2,\quad \Phi=\log2.
\]

An exact \(3/5\)-\(4/5\) angular rotation leaves \(A,B,C,h,m,\beta,\Phi\) unchanged. Under
\(X_1\mapsto kX_1\), \(h_{01}\mapsto kh_{01}\), \(h_{11}\mapsto k^2h_{11}\), and
\(m^2\mapsto k^2m^2\), while \(\Phi\) is unchanged. Negative \(k\) reverses ruler orientation; it is
not observer-pair reversal.

## 8. Verification and ceiling

The production derivation passes 14 symbolic identities. An independent standard-library
Fraction implementation passes 20,000 regular witnesses and 320,000 exact assertions, including
the positive local screen, arbitrary angular directions, exact rotations, and signed ruler
reparameterizations. Eighteen executable mutation catches and twelve semantic guards pass.

The bounded landing is:

NONRADIAL_COMPLETED_PAIR_CHANNELS_RESOLVE_WITHOUT_EXTRA_SCALAR
__CLOCK_ANGULAR_NORM_CONTROLS_DEPTH
__FULL_ANGULAR_GRAM_CONTROLS_TAPE_SHIFT_AND_LOCAL_SCREEN

This is a local conditional theorem on the supplied query family. It does not select observer
germs, derive a finite sky response, alter the G185 SNe curve, derive R(Z), or establish a global
history, dynamics, action, source, matter, bootstrap, X_max, or signalling law.
