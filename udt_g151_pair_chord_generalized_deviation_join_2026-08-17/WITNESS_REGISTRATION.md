# G151 exact witness registration

Date: 2026-08-17
Status: `FROZEN_BEFORE_EXECUTION`

This witness checks the curvature/Jacobi sign and the connecting-field type. It is a mathematical
control, not a selected UDT history.

Set \(X_{\max}=2\) only as a dimensionless witness normalization and define near \(t=0\)

\[
L(t)=1+\frac{t}{10}+\frac{t^2}{20},
\qquad
T(t)=L(t)\frac{2-L(t)}{2+L(t)}.
\]

Use the smooth Lorentz metric

\[
g=-T(t)^2dt^2+L(t)^2dx^2+dy^2+dz^2
\]

and the coordinate pair immersion

\[
F(t,\sigma)=(t,\sigma,0,0).
\]

Then

\[
h=F^*g=\operatorname{diag}(-T^2,L^2),
\qquad
\phi_{\rm pair}=\frac12\log(L/T)=\operatorname{artanh}(L/2),
\]

so the working relation magnitude is exactly

\[
\rho=2\tanh\phi_{\rm pair}=L.
\]

Freeze

\[
u=T^{-1}\partial_t,
\qquad
\xi=\partial_x=Ln,
\qquad
n=L^{-1}\partial_x.
\]

The script must independently verify rather than assume:

- Lorentz regularity at \(t=0\);
- terminal reciprocal equality and \(\rho=L\);
- \([u,\xi]=0\);
- \(\nabla_u u=0\) for the whole local congruence;
- the exact direct second derivative \(\nabla_u^2\xi\);
- the curvature vector \(R(\xi,u)u\) using the preregistered convention;
- the Jacobi residual vanishes exactly.

Expected marked-point values, frozen before execution:

\[
T(0)=\frac13,
\quad
\rho(0)=1,
\quad
\dot\rho(0)=\frac3{10},
\quad
\ddot\rho(0)=\frac{93}{100},
\]

\[
g(R(n,u)u,n)=-\frac{93}{100}.
\]

Any mismatch falsifies the registered witness or sign convention.

