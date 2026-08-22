# G221 exact derivation — complete-coframe null clock chord

Date: 2026-08-22

## Primary bounded result

On one supplied regular future-null observer query, the complete `2+2` metric determines one
positive measured-frequency chord. Screen scale/shape and both base-to-screen mixing columns enter
that chord before the reciprocal scalar is read:

\[
r_{AB}=\frac{\mathcal W_A}{\mathcal W_B},
\qquad
\delta_{AB}=-\log r_{AB}.
\]

This is the explicit complete-coframe form of the covariant G220 identity
`r_AB=omega_A/omega_B`. It does not select null incidence as the universal physical observer-pair
protocol.

## 1. Complete coframe and regular stratum

Use coordinates \((t,x,z^1,z^2)\) and the supplied coframe

\[
\theta^0=N(dt+\beta\,dx),
\qquad
\theta^1=A\,dx,
\]

\[
\boldsymbol\theta_S
=Q\bigl(d\mathbf z+\mathbf s_tdt+\mathbf s_xdx\bigr).
\]

Here \(N,A>0\), \(Q\in GL(2,\mathbb R)\), and

\[
H=Q^TQ,
\qquad
D=A^2-N^2\beta^2>0.
\]

The fixed-spatial-coordinate observer has tangent \(\partial_t\) with

\[
g(\partial_t,\partial_t)
=-N^2+\mathbf s_t^TH\mathbf s_t=-P^2.
\]

The declared observer stratum is \(P^2>0\), and its unit future velocity is

\[
U=P^{-1}\partial_t.
\]

Both inequalities are chart/query gates. They are not promoted to universal restrictions on every
UDT observer or metric.

## 2. Exact null-energy roots

Let a supplied null covector have coordinate components

\[
p=p_tdt+p_xdx+\mathbf p_z^Td\mathbf z.
\]

Writing it in the orthonormal coframe gives

\[
\widehat p_0=\frac{p_t-\mathbf s_t^T\mathbf p_z}{N},
\]

\[
\widehat p_1
=\frac{p_x-\mathbf s_x^T\mathbf p_z-N\beta\widehat p_0}{A},
\qquad
\widehat{\mathbf p}_S=Q^{-T}\mathbf p_z.
\]

Define

\[
\Pi=p_x-\mathbf s_x^T\mathbf p_z,
\qquad
q^2=\mathbf p_z^TH^{-1}\mathbf p_z,
\]

\[
R=\sqrt{\Pi^2+Dq^2}.
\]

The null equation

\[
-\widehat p_0^2+\widehat p_1^2+q^2=0
\]

is exactly

\[
D\widehat p_0^2+2N\beta\Pi\widehat p_0-\Pi^2-A^2q^2=0.
\]

Its two roots are

\[
\widehat p_0^{(\varepsilon)}
=\frac{-N\beta\Pi+\varepsilon AR}{D},
\qquad \varepsilon=\pm1.
\]

Because

\[
A^2R^2-(N\beta\Pi)^2
=D(\Pi^2+A^2q^2)>0,
\]

the minus root is strictly negative and the plus root strictly positive for every nonzero spatial
covector. They are the unique future and past cotangent roots on the declared stratum.

## 3. The full null clock chord

For the future root,

\[
p_t^-
=\mathbf s_t^T\mathbf p_z
-\frac{N(AR+N\beta\Pi)}{D}.
\]

The fixed-coordinate observer measures

\[
\boxed{
\mathcal W=-p(U)
=-\frac{p_t^-}{P}
=\frac{1}{P}
\left[
\frac{N(AR+N\beta\Pi)}{D}
-\mathbf s_t^T\mathbf p_z
\right]>0.}
\]

Every complete-coframe channel is upstream:

- \(Q\) enters through \(H^{-1}\) in \(q^2\);
- \(\mathbf s_x\) enters through \(\Pi\);
- \(\mathbf s_t\) enters through both the observer lapse \(P\) and the coordinate energy;
- \(N,A,\beta\) enter through \(D\), the root, and the normalization.

No angular score, `mu`, or fitted mixing coefficient is appended to \(\delta\).

For the supplied regular null correspondence,

\[
\boxed{
r_{AB}=\frac{\mathcal W_A}{\mathcal W_B},
\qquad
\delta_{AB}=-\log r_{AB}.}
\]

A common positive affine rescaling multiplies both endpoint frequencies and cancels from the ratio.
In a time-only spatially homogeneous coframe, \((p_x,\mathbf p_z)\) is conserved along each ray.
For a general supplied null germ, its endpoint covectors are supplied by geodesic transport and need
not have equal coordinate components.

## 4. Null incidence and the multidirectional qualification

In the time-only homogeneous specialization, the coordinate velocities are obtained directly from
the same energy root:

\[
\boxed{
\frac{d\xi^i}{dt}
=-\frac{\partial p_t^-}{\partial p_i}.}
\]

Explicitly,

\[
\frac{dx}{dt}
=\frac{N}{D}
\left(\frac{A\Pi}{R}+N\beta\right),
\]

\[
\frac{d\mathbf z}{dt}
=-\mathbf s_t-\frac{N^2\beta}{D}\mathbf s_x
+\frac{NA}{DR}
\left(-\Pi\mathbf s_x+DH^{-1}\mathbf p_z\right).
\]

Each ray therefore satisfies

\[
\Delta\boldsymbol\xi
=\int_{t_A}^{t_B}\mathbf v(t;\mathbf p)\,dt.
\]

Unlike the one-dimensional G220 control, neighboring rays in a multidirectional endpoint family may
require different momentum directions. The event-pair derivative is the covariant frequency ratio;
it must not be replaced by differentiating the integral while artificially freezing the ray
direction. Finite transverse Jacobi transport remains the separate G188 channel.

## 5. Passive screen covariance

Under a passive screen-coordinate change \(\mathbf z=K\mathbf z'\),

\[
Q'=QK,
\qquad
S'=K^{-1}S,
\qquad
\mathbf p_z'=K^T\mathbf p_z.
\]

Then \(P^2\), \(\Pi\), \(q^2\), \(p_t^-\), and \(\mathcal W\) are unchanged. Thus the formula hears
physical screen geometry and mixing without depending on the passive screen basis.

## 6. Exact G220 reduction

Set

\[
\mathbf p_z=0,
\qquad
\mathbf s_t=\mathbf s_x=0,
\qquad
p_x>0.
\]

Then \(P=N\), \(R=p_x\), and

\[
\mathcal W
=\frac{p_x(A+N\beta)}{A^2-N^2\beta^2}
=\frac{p_x}{A-N\beta}.
\]

Writing \(C_+=A-N\beta\),

\[
\boxed{
r_{AB}
=\frac{p_x/C_{+A}}{p_x/C_{+B}}
=\frac{C_{+B}}{C_{+A}},}
\]

which is exactly G220.

## 7. Same-correspondence completed clock leg

Use \(y=\tau_A\) on the already supplied event correspondence. The target observer tangent is

\[
\frac{dz_B}{dy}=r_{AB}U_B.
\]

Since \(g(U_B,U_B)=-1\), its pulled-back clock norm is

\[
g\left(\frac{dz_B}{dy},\frac{dz_B}{dy}\right)=-r_{AB}^2.
\]

Therefore

\[
\boxed{T_B=r_{AB}},
\qquad
\boxed{\Phi_{AB}=-\log T_B=\delta_{AB}}.
\]

This exact identity includes the full coframe through \(U_B\) and the supplied null relation. It is
still compatibility on one correspondence—not an independent derivation of G176, the second tangent
needed for a full pair plane, or finite screen transport.

## 8. Boundary and ownership

At \(D=0\), this energy chart degenerates. At \(P=0\), the fixed-coordinate observer becomes null.
Zero covectors and nonregular/multiple null branches also leave the declared theorem. They are not
silently continued or collapsed.

The retained landing is

```text
COMPLETE_COFRAME_NULL_CLOCK_CHORD_DERIVED_CONDITIONALLY
__SCREEN_AND_MIXING_ENTER_UPSTREAM
__G220_RECOVERED
__NULL_AND_FULL_PAIR_REMAIN_QUERY_TYPED
```

Physical history, observer/query population, branch aggregation, the full pair plane, finite
screen/Jacobi transfer, global completion, `X_max`, observations, radiative transfer, action, source,
matter, bootstrap, mass, and signalling remain open.

