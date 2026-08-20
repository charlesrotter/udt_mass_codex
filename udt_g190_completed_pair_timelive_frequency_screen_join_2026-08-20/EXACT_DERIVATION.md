# G190 exact derivation — completed-pair time-live frequency/screen join

Date: 2026-08-20

## 1. Result first

On one supplied smooth regular completed observer-pair family, the full pair pullback determines an
orthonormal clock/ruler frame. That frame contains exactly two future normalized null directions.
After a ruler orientation chooses one of them, the supplied complete metric determines the local
affine null geodesic uniquely. Endpoint clocks from the same typed observer-family query then give
the frequency ratio, while the same ray and metric curvature give the finite Jacobi screen.

Thus one supplied regular branch owns the joint parametric response

\[
\boxed{
\lambda\longmapsto
\left(
Z(\lambda),\;\mathcal D(\lambda),\;
d_A(\lambda)=\sqrt{|\det\mathcal D(\lambda)|}
\right).
}
\]

Where `Z` is locally one-to-one and the Jacobi position block is noncaustic, the inverse-function
theorem gives a derived branch relation

\[
\boxed{d_A(Z)=d_A(\lambda(Z)).}
\]

No static `phi(R)`, P1 chord, `R(Z)`, `X_max`, fitted coefficient, or post-readout angular term is
present. At a frequency turn the honest answer is branch-parametric rather than a single-valued
function. At a caustic the carried Jacobi phase remains the lawful object; no inverse position map
is asserted.

The result is conditional on the working completed-pair clarification and on a supplied metric and
typed observer-family query. It does not select their physical population or derive radiative
transfer.

## 2. The completed pair fixes its local null germ

Write the auxiliary pair pullback in its unique shifted form,

\[
h_\sigma=-T^2(d\tau+\beta\,d\sigma)^2+L_\sigma^2d\sigma^2,
\qquad T,L_\sigma>0.
\]

Let

\[
X_0=F_*\partial_\tau,
\qquad X_\sigma=F_*\partial_\sigma.
\]

The G179--G180 completed ruler density is

\[
m=T L_\sigma=\sqrt{-\det h_\sigma},
\qquad ds=m\,d\sigma,
\qquad B=\frac\beta m.
\]

The completed pair metric is

\[
h_s=-T^2(d\tau+B\,ds)^2+T^{-2}ds^2.
\]

Its dual orthonormal frame, pushed into the ambient tangent space, is

\[
\boxed{U=T^{-1}X_0,}
\]

\[
\boxed{
N=L_\sigma^{-1}(X_\sigma-\beta X_0)
=T(X_s-BX_0).
}
\]

Direct contraction gives

\[
g(U,U)=-1,
\qquad g(N,N)=1,
\qquad g(U,N)=0.
\]

Therefore

\[
\boxed{\ell_\pm=U\pm N}
\]

satisfy

\[
g(\ell_\pm,\ell_\pm)=0,
\qquad -g(U,\ell_\pm)=1.
\]

They exhaust the normalized future null directions in the pair plane: any vector in the plane is
`aU+bN`, and nullity gives `b=+/-a`; future unit-frequency normalization gives `a=1`.

Thus the completed pair does not need a continuously adjustable path coefficient to supply its
local null germ. It has a discrete two-direction choice. Reversing the ruler orientation sends
`N -> -N` and exchanges `ell_+` with `ell_-`.

For a smooth metric, either initial condition

\[
\gamma(0)=p,
\qquad \dot\gamma(0)=\ell_\pm
\]

has one unique local affinely parametrized geodesic solution. This is an initial-value theorem. It
does not guarantee that the branch meets an arbitrarily specified second observer, nor choose
among multiple later intersections, cut branches, or caustics. Those remain typed query/branch
data.

## 3. Exact frequency channel

Let `k=dot(gamma)` and let the declared endpoint observer clocks be the unit timelike vectors
`U_o` and `U_s` supplied by the same completed observer-family query. Define

\[
\omega_i=-g(k_i,U_i)>0.
\]

The endpoint frequency ratio is

\[
\boxed{
Z=\frac{\omega_s}{\omega_o}
=\frac{-g(k_s,U_s)}{-g(k_o,U_o)}.
}
\]

It is unchanged by one common positive affine rescaling `k -> c k`. In G190 the initial
normalization `-g(U_o,k_o)=1` already fixes that scale.

If the completed observer-family query supplies a smooth unit clock field `U(lambda)` along the
sampled branch, then

\[
\omega=-g(U,k)
\]

obeys, using metricity and affine geodesicity,

\[
\begin{aligned}
\frac{d\omega}{d\lambda}
&=-g(\nabla_kU,k)-g(U,\nabla_kk)\\
&=\boxed{-k^ak^b\nabla_aU_b}.
\end{aligned}
\]

Hence

\[
\boxed{
\log Z(\lambda)
=-\int_0^\lambda
\frac{k^ak^b\nabla_aU_b}{\omega}\,d\lambda'.
}
\]

No drift coefficient, optical coefficient, or terminal-depth correction has been inserted. Those
quantities may appear after expanding this exact contraction in a specialized chart, as G116 did;
they are not inputs to G190.

Endpoint frequency requires only the two endpoint clocks and the common ray. The differential form
requires a smooth clock carry and is therefore stated only when the typed query supplies one.

## 4. Exact screen channel on the same ray

The completed pair plane has positive orthogonal complement

\[
\operatorname{span}(U,N)^\perp.
\]

For `k=U+N` this is the natural source representative of G188's quotient screen

\[
\mathcal S=k^\perp/\langle k\rangle.
\]

The metric Levi-Civita connection induces the quotient-screen connection, and the curvature fixes

\[
\mathcal T([X])=[R(X,k)k].
\]

In any parallel orthonormal screen frame the finite vertex-normalized map obeys

\[
\boxed{
\mathcal D''+\mathcal T\mathcal D=0,
\qquad
\mathcal D(0)=0,
\qquad
\mathcal D'(0)=I.
}
\]

The scalar area readout is

\[
\boxed{d_A^2=|\det\mathcal D|.}
\]

The full matrix is retained. The G188 genuine-mixing regression has

\[
\mathcal T=
\begin{pmatrix}-2&-2\\-2&-2\end{pmatrix}
\]

and

\[
\mathcal D_{12}=\frac{\sinh(2\lambda)}4-\frac\lambda2
=\frac{\lambda^3}{3}+O(\lambda^5),
\]

so joining the frequency channel does not scalarize or diagonalize the orchestra.

## 5. Why the join is metric-native

At the initial and endpoint pair germs,

\[
h=J^TgJ=J^TE^T\eta EJ.
\]

Therefore all complete-coframe, screen, mixing, and pair-tangent channels enter before `U`, `N`,
and the endpoint clocks are read. Along the ray, the same complete metric supplies

\[
\Gamma[g,\partial g],
\qquad
R[g,\partial g,\partial^2g],
\]

which govern `k`, `omega`, and `D`. Time dependence is retained in the metric and observer family;
it is not appended as a correction.

The joint first-order/second-order system may be written schematically as

\[
\dot x^a=k^a,
\qquad
\nabla_kk=0,
\]

\[
\dot\omega=-k^ak^b\nabla_aU_b,
\]

\[
\mathcal D'=\mathcal P,
\qquad
\mathcal P'=-\mathcal T\mathcal D.
\]

Given the supplied regular inputs, standard ODE uniqueness fixes all of these simultaneously. The
frequency and screen are distinct outputs, not rival definitions of one scalar.

## 6. Descent from affine parameter to frequency

The joint curve exists without assuming that frequency is monotone. On any interval where

\[
\frac{dZ}{d\lambda}\ne0,
\]

the inverse-function theorem supplies a local inverse `lambda(Z)`. On a noncaustic portion of that
interval,

\[
d_A(Z)
=\sqrt{|\det\mathcal D(\lambda(Z))|}
\]

is metric-derived from the supplied history and query.

If `Z` turns, two or more affine locations can share the same frequency while having different
screens. The correct result is then the branch-labelled set

\[
\left\{
(Z(\lambda),\mathcal D(\lambda))
\right\},
\]

not an averaged or fitted single curve. This is precisely where a static algebraic `R(Z)` shortcut
would lose information.

If the already authorized transparent-transfer bridge is imported later,

\[
d_L=Z^2d_A
\]

may be evaluated on the same parametric branch. G190 does not derive that bridge.

## 7. Exact time-live control

Use the chosen mathematical metric

\[
g=a(\eta)^2(-d\eta^2+dr^2+dx^2+dy^2),
\qquad
a(\eta)=e^{H\eta},
\qquad H>0,
\]

and the completed pair family

\[
F(\tau,\sigma)=(\eta=\tau,r=\sigma,x=0,y=0).
\]

Its auxiliary pullback is

\[
h_\sigma=a^2(-d\tau^2+d\sigma^2),
\]

so

\[
T=L_\sigma=a,
\qquad m=a^2,
\qquad \Phi=-\log a=-H\eta,
\]

and

\[
U=a^{-1}\partial_\eta,
\qquad
N=a^{-1}\partial_r.
\]

Normalize at `eta=0`, where `a=1`. The outgoing affine geodesic is

\[
k=a^{-2}(\partial_\eta+\partial_r),
\]

and direct Christoffel reconstruction gives `nabla_k k=0`. Its measured frequency is

\[
\omega=-g(U,k)=a^{-1},
\qquad
Z=e^{-H\eta}=e^\Phi.
\]

The parallel screen basis is

\[
s_1=a^{-1}\partial_x,
\qquad
s_2=a^{-1}\partial_y,
\]

and direct Riemann reconstruction gives

\[
\mathcal T=H^2a^{-4}I_2.
\]

Along the ray,

\[
\lambda=\frac{e^{2H\eta}-1}{2H}.
\]

The exact vertex-normalized Jacobi map is

\[
\boxed{
\mathcal D(\lambda)
=\frac{\sqrt{1+2H\lambda}\,
\log(1+2H\lambda)}{2H}I_2
=a\eta\,I_2.
}
\]

It satisfies the full Jacobi equation and unit vertex derivative exactly. Hence, on `eta>=0`,

\[
d_A=a\eta,
\]

and eliminating `eta` using the metric-produced frequency gives

\[
\boxed{
d_A(Z)=-\frac{\log Z}{H Z}.
}
\]

This curve was not fitted and is not proposed as a physical cosmology. It is an exact witness that
a supplied time-live metric and completed pair can generate their own frequency-area relation
without a separate static profile.

## 8. Static and local boundaries

### G189 static specialization

For the primary static metric and its completed radial pair,

\[
U=\frac{e^\phi}{c_E}\partial_t.
\]

Stationarity conserves `E=-k_t`, so

\[
\omega=\frac{E}{c_E}e^\phi,
\qquad
\boxed{Z=e^{\phi_s-\phi_o}.}
\]

On the central spherical branch G119/G188 gives `D=R O` and `d_A=R`. Thus G189 is recovered after
the general joint evaluator is specialized. A static `d_A(Z)` still requires the supplied static
profile to eliminate `R`; that is a property of the static history, not a missing screen law.

### G116 local regression

Expanding the exact contraction `omega=-g(U,k)` and the same curvature system in G115's supplied
regular central spherical two-jet reproduces G116's coefficient-free local identity. The symbolic
regression residual is zero. Its `v_rel`, `A_opt`, and chart coefficients were not used to derive
the general theorem or time-live control.

## 9. Certification

The production implementation verifies exactly:

- nine completed-pair determinant, orthonormality, nullity, and normalization identities;
- the full coordinate geodesic equation in the time-live control;
- parallel transport of both screen vectors;
- the frequency derivative by an independently reconstructed covariant derivative;
- the full Riemann screen tide;
- the Jacobi equation and vertex data;
- `log Z=Phi` in the declared witness;
- the static G189 and local G116 post-result regression limits;
- the nonzero G188 matrix cross-screen response.

An implementation-distinct standard-library replay imports no production module and reads no
production artifact. It checks 20,000 random completed-pair frames and 256 independently integrated
Jacobi branches: 161,024 assertions pass. The maximum RK4-versus-exact Jacobi error is
`1.9984e-14`; the maximum frequency/descent error is `1.5544e-15`.

## 10. Landing and ceiling

```text
COMPLETED_PAIR_NULL_GERM_AND_TIMELIVE_FREQUENCY_SCREEN_JOINT_EVALUATOR_DERIVED_CONDITIONALLY
__DA_OF_Z_DESCENDS_ONLY_ON_MONOTONE_NONCAUSTIC_BRANCHES
__STATIC_G189_AND_LOCAL_G116_ARE_POST_RESULT_SPECIALIZATIONS
```

The local null germ is metric-derived from the supplied completed pair, up to the discrete ruler
orientation. The global endpoint intersection, metric history, and observer-family population are
not selected. Native radiative transfer, emission, source standardization, caustic aggregation,
global completion, observations, `X_max`, dynamics, action, matter, mass, bootstrap, and signalling
remain outside this theorem.
