# G192 exact derivation — smooth time-live mixing family

Date: 2026-08-20

## 1. Bounded result

For the preregistered smooth family, the common scale and mixing functions remain inside one
complete metric initial-value problem. The exact native output is

\[
\eta\longmapsto\bigl(\lambda(\eta),Z(\eta),\mathcal D(\eta),d_A(\eta)\bigr).
\]

The frequency need not be monotone. In contrast, the vertex-normalized screen has no nonvertex
caustic anywhere on a regular connected interval of this family. These are family-scoped
statements, not general theorems for every complete coframe.

## 2. Complete coframe and regularity

Let `a(eta)>0`, `a(0)=1`, and let `mu(eta)` be real. The original fixed source-screen coframe is

\[
\begin{aligned}
\theta^0&=a\,d\eta,\\
\theta^1&=a\,dz,\\
\theta^2&=a\left[dx+\frac{\mu}{\sqrt2}(x+y)(d\eta+dz)\right],\\
\theta^3&=a\left[dy+\frac{\mu}{\sqrt2}(x+y)(d\eta+dz)\right].
\end{aligned}
\]

The constant screen rotation

\[
p=\frac{x+y}{\sqrt2},\qquad w=\frac{x-y}{\sqrt2},\qquad A(\eta)=\sqrt2\,\mu(\eta)
\]

gives

\[
\theta^+=a[dp+A p(d\eta+dz)],\qquad \theta^-=a\,dw.
\]

Direct reconstruction gives

\[
\det E=a^4>0,\qquad \det g=-a^8<0.
\]

Thus every member is Lorentzian and regular wherever `a>0`. On the supplied central pair

\[
F(\tau,\sigma)=(\eta=\tau,z=\sigma,p=w=0),
\]

the pullback and completed frame are

\[
F^*g=a^2(-d\tau^2+d\sigma^2),
\]

\[
U=a^{-1}\partial_\eta,\qquad N=a^{-1}\partial_z,
\qquad \ell_+=U+N.
\]

## 3. Affine ray and frequency turns

The direct Christoffel calculation gives the central affine tangent

\[
k=a^{-2}(\partial_\eta+\partial_z),
\qquad \nabla_k k=0.
\]

Consequently

\[
\boxed{
\lambda(\eta)=\int_0^\eta a(s)^2\,ds
}
\]

is strictly increasing on every regular interval. The completed pair clock measures

\[
\boxed{Z(\eta)=-g(U,k)=\frac1{a(\eta)}}.
\]

The independent contraction identity gives

\[
\frac{dZ}{d\lambda}
=-k^ak^b\nabla_aU_b
=-\frac{a'(\eta)}{a(\eta)^4}.
\]

Therefore:

- `a'>0` gives decreasing frequency;
- `a'<0` gives increasing frequency;
- `a'=0` gives a frequency stall;
- a sign change of `a'` gives a true turn.

Monotonicity in G191 came from `a=exp(H eta)`, not from the coframe architecture alone.

## 4. Full matrix tide

The vectors

\[
s_+=a^{-1}\partial_p,\qquad s_-=a^{-1}\partial_w
\]

are parallel and orthonormal along the central affine ray. Define

\[
\mathcal H=\frac{a'}a,
\]

\[
\tau_0=\frac{\mathcal H^2-\mathcal H'}{a^4},
\qquad
c=\frac{A'-2A^2}{a^4}
=\frac{\sqrt2\,\mu'-4\mu^2}{a^4}.
\]

In the fixed original `(x,y)` screen, direct Riemann reconstruction gives

\[
\boxed{
\mathcal T=
\begin{pmatrix}
\tau_0+c&c\\
c&\tau_0+c
\end{pmatrix}.
}
\]

Its trace-free part is

\[
\mathcal T_{\rm TF}=
\begin{pmatrix}0&c\\c&0\end{pmatrix}.
\]

The constant screen rotation diagonalizes this only for analysis:

\[
\tau_+=\tau_0+2c
=\frac{\mathcal H^2-\mathcal H'+2A'-4A^2}{a^4},
\qquad
\tau_-=\tau_0.
\]

The `mu'` and `mu^2` terms are both load-bearing. A nonzero coframe mixing function does not by
itself guarantee nonzero central trace-free tide: `A'=2A^2` makes `c=0` while `A` may remain
nonzero.

## 5. Exact Jacobi factorization

Let

\[
I(\eta)=\int_0^\eta A(s)\,ds,
\qquad
J(\eta)=\int_0^\eta e^{4I(s)}\,ds.
\]

After writing the physical plus-mode amplitude as `f_+=a y_+`, its affine Jacobi equation becomes

\[
y_+''+(2A'-4A^2)y_+=0.
\]

The differential operator factorizes:

\[
\left(\frac d{d\eta}-2A\right)
\left(\frac d{d\eta}+2A\right)y_+=0.
\]

With vertex data `f_+(0)=0` and `(df_+/d lambda)(0)=1`, the exact solution is

\[
\boxed{
y_+(\eta)=e^{-2I(\eta)}J(\eta),
\qquad
f_+(\eta)=a(\eta)e^{-2I(\eta)}J(\eta).
}
\]

The passive mode is

\[
\boxed{f_-(\eta)=a(\eta)\eta.}
\]

Rotating back to the fixed source screen gives the full matrix

\[
\boxed{
\mathcal D=
\frac12
\begin{pmatrix}
f_++f_-&f_+-f_-\\
f_+-f_-&f_++f_-
\end{pmatrix},
}
\]

with exact affine vertex normalization

\[
\mathcal D(0)=0,
\qquad
\frac{d\mathcal D}{d\lambda}(0)=I_2.
\]

## 6. Caustic and cross-response classification

Because `exp(4I)>0`, the integral `J(eta)` has the same sign as `eta`. Hence on every connected
regular interval containing the vertex,

\[
f_+(\eta)f_-(\eta)
=a(\eta)^2\eta e^{-2I(\eta)}J(\eta)>0
\qquad(\eta\ne0).
\]

Therefore

\[
\boxed{
\det\mathcal D>0\quad\text{for every nonvertex point in this family}.
}
\]

There is no nonvertex screen caustic in the displayed two-function family. This result does not
extend by assertion to arbitrary complete coframes, other mixing channels, other pair germs, or
global topology.

The cross response

\[
\mathcal D_{xy}=\frac{f_+-f_-}{2}
\]

has no universal sign. The frozen census contains positive, negative, and exactly zero controls.
Thus G191's positive cross response was also control-specific.

The angular area is

\[
d_A^2=\det\mathcal D
=a^2\eta e^{-2I}J.
\]

The native result remains parametric. A local `d_A(Z)` exists wherever `a'` is nonzero. Across a
frequency turn, equal `Z` values can carry different `d_A`, so the correct result is branch-labelled.

## 7. Exact limits

### G191

For `a=exp(H eta)` and constant positive `mu`,

\[
f_+=a\frac{\sinh(2\sqrt2\mu\eta)}{2\sqrt2\mu},
\qquad
f_-=a\eta,
\]

and substituting `q=a^2=1+2H lambda` reproduces G191 exactly.

### G190

For `mu=0`, `I=0` and `J=eta`, so

\[
\mathcal D=a(\eta)\eta I_2.
\]

This is the arbitrary-smooth conformal time-live screen, with G190's exponential witness as a
special case.

### G188

For `a=1` and constant `mu`, `lambda=eta` and

\[
f_+=\frac{\sinh(2\sqrt2\mu\lambda)}{2\sqrt2\mu},
\qquad
f_-=\lambda,
\]

which is the declared G188 static-mixing normalization.

## 8. Numerical and epistemic boundary

The independent standard-library replay used ten preregistered named histories plus 256 seeded
random smooth histories. Its maximum errors were

\[
6.33\times10^{-14}\quad\text{(frequency)},
\]

\[
1.10\times10^{-12}\quad\text{(Jacobi modes)},
\]

and

\[
1.05\times10^{-12}\quad\text{(affine relation)},
\]

against the registered `2e-9` ceiling. Eighteen hostile catches pass.

This is a complete classification of the displayed two-function family only. It does not select a
physical metric history, complete observer population, transfer law, source state, observation,
global completion, or `X_max`.
