# G191 exact derivation — nonconformal time-live mixing join

Date: 2026-08-20

## 1. Result first

The preregistered complete coframe gives one exact control in which the metric is simultaneously
time-live, nonconformally flat, and mixing-active. The completed pair, affine frequency, and full
matrix screen remain one initial-value problem.

On the declared branch, define

\[
q(\lambda)=1+2H\lambda.
\]

Then

\[
Z(\lambda)=q^{-1/2}
\]

and the screen has symmetric and antisymmetric eigenmodes

\[
f_+(\lambda)=
\frac{\sqrt q}{2\sqrt2\,\mu}
\sinh\!\left(\frac{\sqrt2\mu}{H}\log q\right),
\]

\[
f_-(\lambda)=\frac{\sqrt q}{2H}\log q.
\]

In the fixed source screen,

\[
\boxed{
\mathcal D=
\frac12
\begin{pmatrix}
f_++f_-&f_+-f_-\\
f_+-f_-&f_++f_-
\end{pmatrix}.
}
\]

Thus mixing produces a live cross-image response while the same branch carries nontrivial
frequency evolution. No post-readout coefficient joins them.

## 2. Complete coframe and pair pullback

Let

\[
a(\eta)=e^{H\eta},\qquad H>0,\quad\mu>0,
\]

and

\[
\begin{aligned}
\theta^0&=a\,d\eta,\\
\theta^1&=a\,dz,\\
\theta^2&=a\left[dx+\frac{\mu}{\sqrt2}(x+y)(d\eta+dz)\right],\\
\theta^3&=a\left[dy+\frac{\mu}{\sqrt2}(x+y)(d\eta+dz)\right].
\end{aligned}
\]

The coframe determinant and metric determinant are

\[
\det E=a^4>0,
\qquad
\det g=-a^8<0.
\]

Hence the coframe is regular and the metric has Lorentzian signature everywhere in the declared
finite chart.

For

\[
F(\tau,\sigma)=(\eta=\tau,z=\sigma,x=0,y=0),
\]

the auxiliary pair metric is

\[
F^*g=a^2(-d\tau^2+d\sigma^2).
\]

Thus `T=L_sigma=a`, `m=T L_sigma=a^2`, and the orthonormal pair frame is

\[
U=a^{-1}\partial_\eta,
\qquad
N=a^{-1}\partial_z.
\]

The ruler orientation selects

\[
\ell_+=U+N=a^{-1}(\partial_\eta+\partial_z).
\]

At the source `a(0)=1`, so the source-normalized affine initial tangent agrees with `ell_+`.

## 3. Affine ray and frequency

Direct Christoffel reconstruction gives the central affine ray

\[
k=a^{-2}(\partial_\eta+\partial_z),
\qquad x=y=0,
\]

with all four components of `nabla_k k` equal to zero. Integrating `d eta/d lambda=a^{-2}` gives

\[
\lambda=\frac{e^{2H\eta}-1}{2H},
\qquad
q=1+2H\lambda=e^{2H\eta}.
\]

The pair clock measures

\[
\omega=-g(U,k)=a^{-1}.
\]

The independently reconstructed differential contraction gives

\[
\frac{d\omega}{d\lambda}
=-k^ak^b\nabla_aU_b
=-H e^{-3H\eta}.
\]

With source normalization `omega(0)=1`,

\[
\boxed{Z(\lambda)=q^{-1/2}.}
\]

For `H>0` and `lambda>=0`, `dZ/dlambda=-Hq^{-3/2}<0`; this control has no frequency turn.

## 4. Parallel screen and curvature tide

The two vectors

\[
s_1=a^{-1}\partial_x,
\qquad
s_2=a^{-1}\partial_y
\]

are orthonormal and parallel along the central affine ray. Direct Riemann reconstruction gives

\[
\boxed{
\mathcal T(\lambda)=\frac1{q^2}
\begin{pmatrix}
H^2-4\mu^2&-4\mu^2\\
-4\mu^2&H^2-4\mu^2
\end{pmatrix}.
}
\]

The operator is self-adjoint. Its trace-free screen part is

\[
\mathcal T_{\mathrm{TF}}=
\frac1{q^2}
\begin{pmatrix}
0&-4\mu^2\\
-4\mu^2&0
\end{pmatrix}.
\]

For `mu!=0` this is nonzero, so the witness is not conformally flat. The mixing is geometric; it
cannot be absorbed into the common conformal factor.

The symmetric screen eigenvalue is `(H^2-8mu^2)/q^2`; the antisymmetric eigenvalue is `H^2/q^2`.
Solving both Euler equations with `f(0)=0`, `f'(0)=1` gives the modes displayed in Section 1.
Substitution gives exactly

\[
\mathcal D''+\mathcal T\mathcal D=0,
\qquad
\mathcal D(0)=0,
\qquad
\mathcal D'(0)=I.
\]

## 5. Area, descent, and branch classification

The eigenmode factorization gives

\[
\det\mathcal D=f_+f_-.
\]

For `lambda>0`, `H>0`, and `mu>0`, both factors are positive. Therefore the declared outgoing
branch has no post-vertex caustic and

\[
d_A^2=f_+f_-.
\]

Since `Z` is strictly monotone, `q=Z^{-2}` and the branch descends to

\[
\boxed{
d_A^2(Z)=
\frac{(-\log Z)
\sinh\!\left[-\frac{2\sqrt2\mu}{H}\log Z\right]}
{2\sqrt2\,H\mu\,Z^2},
\qquad 0<Z\le1.
}
\]

This is not an imported `R(Z)`. It is the elimination of the affine parameter after the same
metric produced both frequency and screen.

The cross response is `(f_+-f_-)/2`. Because `sinh(r w)/r>w` for `r,w>0`, it is strictly positive
for `lambda>0`. Near the vertex it begins at cubic order; deeper on the branch its relative weight
changes automatically with `mu/H` and `log q`. This is a property of this supplied metric control,
not a universal loud/quiet/loud law.

## 6. Exact regression limits

### Mixing deletion

As `mu -> 0`, `f_+ -> f_-` and

\[
\mathcal D\to
\frac{\sqrt q\log q}{2H}I.
\]

This is exactly the G190 conformal time-live control.

### Static limit

As `H -> 0+`,

\[
f_-\to\lambda,
\qquad
f_+\to\frac{\sinh(2\sqrt2\mu\lambda)}{2\sqrt2\mu}.
\]

The tidal matrix becomes `-4mu^2` in every entry. This is the G188 mixing family with the present
source tangent scaled by `sqrt(2)` relative to its null-coordinate normalization, so the factor of
two in the tide is required.

## 7. Maximum conclusion and boundary

G191 proves only that this one exact nonconformally-flat, time-live, mixing-active complete metric
witness produces frequency and a full matrix screen through one G190 initial-value problem. It
does not select a physical metric or observer population, supply a later endpoint intersection,
derive emission or radiative transfer, predict SNe, aggregate branches, or establish `X_max`,
dynamics, action, matter, mass, bootstrap, or signalling.
