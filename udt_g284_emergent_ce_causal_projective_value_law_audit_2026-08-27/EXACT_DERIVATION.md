# G284 exact derivation — causal tape reconstruction versus value selection

Date: 2026-08-27

The durable production replay uses dependency-free exact Laurent-polynomial algebra. The original
SymPy implementation is retained separately as a supplemental implementation cross-check and is
not required by the registered replay.

## 1. One local `c_E` for every tidal history

Take the preregistered family

\[
g_T=-2\,du\,dv+dx^2+dy^2-Q_T(u,x,y)\,du^2,
\qquad Q_T=x^iT_{ij}(u)x^j.
\]

Its determinant is `-1` for every smooth symmetric `T`, so the metric is Lorentzian without a
condition on the three functions. On the central null relation `x=y=0`, introduce

\[
u=\frac{c_Et-z}{\sqrt2},\qquad v=\frac{c_Et+z}{\sqrt2}.
\]

The metric there is exactly

\[
-c_E^2dt^2+dz^2+dx^2+dy^2.
\]

Thus the two longitudinal null slopes are `dz/dt=+/-c_E` for every `T`. More generally, every
regular Lorentz metric has a local orthonormal frame in which the same clock/ruler conversion
appears. Universal local `c_E` fixes the tangent-cone calibration; it does not prescribe how that
cone changes from event to event.

## 2. The central reciprocal/projective state remains identical

Every member has the same central metric, vanishing first metric jet, connection, parallel screen,
and affine central ray. With the common unit clock

\[
U=(\partial_u+\partial_v)/\sqrt2
\]

and central null tangent `k=partial_u`, the measured frequency is

\[
-g(U,k)=1/\sqrt2
\]

at every central event. Hence every `T` gives the same central frequency ratio, depth, projective
coordinate, and mutual projection:

\[
r=1,\qquad \delta=0,\qquad \chi=0,\qquad M=1.
\]

This is an exact same-`c_E`, same-tape-state counterfamily with different invariant neighboring
curvature.

## 3. Neighboring cones reveal the missing functions exactly

At a neighboring point, consider

\[
k_T=\partial_u+a_T\partial_v.
\]

Nullness gives

\[
0=g_T(k_T,k_T)=-Q_T-2a_T,
\qquad
a_T=-\frac12x^iT_{ij}x^j.
\]

Therefore

\[
\boxed{T_{ij}=-\partial_i\partial_j a_T.}
\]

The same matrix is the central curvature `R_uiuj=T_ij` and the Jacobi coefficient in

\[
D''+T(u)D=0.
\]

This proves Charles's key intuition in a precise bounded sense: the light-cone network contains
more shape than one scalar redshift arrow. The second transverse variation of its delay/slope is
the optical tidal history itself.

It also gives the decisive type distinction. Supplying the full neighboring cone field lets one
*reconstruct* `T`; the null condition does not supply a residual that chooses its values. Every
smooth symmetric `T` produces its own lawful cone field.

## 4. Causality and network closure remain compatible with arbitrary `T`

For every smooth bounded `T`, continuity supplies a sufficiently small causally convex tube around
the central ray. The first-order Jacobi generator

\[
A_T=\begin{pmatrix}0&I\\-T&0\end{pmatrix}
\]

is Hamiltonian for every symmetric `T`. Its interval transfers are therefore symplectic,
invertible under relation reversal, and composable through middle events. These facts ensure that
the causal/projective network is coherent; they do not set `T`.

The conclusion is local and bounded. A future genuinely global causal-completion principle could
be value-bearing, but ordinary local causal regularity and finite path-labelled composition are
not such a principle.

## 5. `c_E` does not attach the absolute tape scale by itself

For any positive constant `lambda`, the homothetic metric

\[
\widehat g_T=\lambda^2g_T
\]

has the same null cones, Levi-Civita connection, frequency ratios, reciprocal depths, projective
states, and coordinate cone slope `c_E`. Proper clock and ruler intervals scale together.

This is the G276 boundary in the present witness: `c_E` converts an independently calibrated clock
interval into length, but `c_E` plus metric self-evaluation does not supply that interval or select
the homothety.

## 6. Which stronger statements would become nonidentity

Three stronger conditions could reject members of the witness family, but none follows from the
tested conjunction:

1. an endpoint-only or path-independent tape law, which would suppress allowed path/screen carry;
2. zero holonomy or all-germ isotropy, which would discard legitimate curved angular sectors;
3. a native nonidentity relation tying the longitudinal projective jet to the transverse
   neighboring-cone Hessian.

The third is the least structurally destructive description of the remaining bridge. It is a law
for the *curvature of the causal tape*, not another definition of the tape and not a fitted optical
profile. G284 derives its mathematical type but not its formula.

## 7. Bounded conclusion

On the frozen 15-source and arbitrary-`T` witness arena,

```text
EMERGENT_CE_CAUSAL_PROJECTIVE_NETWORK_RECONSTRUCTS_BUT_DOES_NOT_SELECT_TIDAL_HISTORY
```

Foundational infinite bare `c` remains a working interpretation rather than a signalling theorem
or canonized postulate. The direct reciprocal redshift, universal metric coupling, complete
projective state, native first-jet orchestra, and causal/Jacobi evaluators remain intact.
