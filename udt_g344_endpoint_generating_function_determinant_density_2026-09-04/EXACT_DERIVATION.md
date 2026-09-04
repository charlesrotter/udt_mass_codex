# G344 exact derivation — endpoint generating function and determinant density

Date: 2026-09-04
Grade: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Bounded landing

```text
GLOBAL_NONCOINCIDENT_QUADRATIC_SCREEN_ENDPOINT_GENERATOR_CLOSES
__MIXED_HESSIAN_IS_A_TYPED_AFFINE_WEIGHTED_ENDPOINT_BIDENSITY
__EXACT_STATIONARY_COMPOSITION_REVERSAL_REFERENCE_AND_SCREEN_COVARIANCE
__BOTH_PRINCIPAL_LIMITS_AND_EACH_COMPACT_PATH_LABEL_RETAINED
__NO_LIGHT_FLUX_DISTANCE_PROBABILITY_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED
```

G344 selects preregistered alternatives `A`, `C1`, `R1`, `A1`, `S1`, `P1`, and `Q1`, with the
additive endpoint-function qualification recorded at commit `9701e595`. This is a geometric result
on the supplied G343 spacetime and labelled null rays. It changes neither the metric, completed-pair
kernel, angular sector, nor owner-provisional response equation.

## 1. Exact noncoincident domain

In G343's common affine gauge write the two-screen canonical state as

\[
 z_i=(x_i,p_i),\qquad p_i={dx_i\over ds},
\]

and the exact propagator as

\[
 \binom{x_1}{p_1}=
 M_{10}\binom{x_0}{p_0},\qquad
 M_{10}=\begin{pmatrix}A&B\\C&D\end{pmatrix},\qquad
 M_{10}^{T}JM_{10}=J.
\tag{1}
\]

In the G341 parallel screen, `B` is diagonal with entries

\[
 B_j(T_1,T_0)
 ={T_*^{1/3}\over\nu}y_j(T_1)y_j(T_0)
 \int_{T_0}^{T_1}w_j(u)\,du,
\tag{2}
\]

where all prefactors, both `y_j`, and both weights `w_j` are strictly positive for `T>0`.
Therefore

\[
 \operatorname{sign}B_j=\operatorname{sign}(T_1-T_0),\qquad
 B_j=0\iff T_1=T_0.
\tag{3}
\]

It follows analytically, not from sampling, that

\[
 \boxed{\det B=B_\parallel B_Z>0}
\tag{4}
\]

for every distinct positive endpoint pair, every mixed direction, both principal directions, and
either endpoint order. Hence one type-I generating chart covers the complete noncoincident domain.
There are no interior screen conjugate points in this bounded ray family.

At coincidence, `M=I` and `B=0`; this type-I chart must be singular there. That is the identity-map
chart boundary, not a physical caustic or rejected solution.

## 2. Metric-owned homogeneous quadratic generator

Solving the first row of (1) gives

\[
 p_0=B^{-1}(x_1-Ax_0).
\tag{5}
\]

The symplectic identities imply

\[
 DB^{-1}=(DB^{-1})^T,\qquad
 B^{-1}A=(B^{-1}A)^T,
\tag{6}
\]

and

\[
 C-DB^{-1}A=-B^{-T}.
\tag{7}
\]

Thus the exact homogeneous quadratic representative is

\[
 \boxed{
 S^0_{10}(x_1,x_0)=
 {1\over2}x_1^TDB^{-1}x_1-x_0^TB^{-1}x_1
 +{1\over2}x_0^TB^{-1}Ax_0.}
\tag{8}
\]

It obeys

\[
 \boxed{p_1=+\partial_{x_1}S^0_{10}},\qquad
 \boxed{p_0=-\partial_{x_0}S^0_{10}},
\tag{9}
\]

and (7) recovers the second row of (1). Therefore the generator reproduces all four G343 blocks,
not only the beam-position block.

This is the endpoint generator of the linear screen Jacobi system. It is not a newly selected
spacetime action, electromagnetic action, or quantum phase.

## 3. Exact additive freedom

The canonical map determines every position-dependent coefficient in (8), but screen derivatives
cannot detect

\[
 S_{10}=S^0_{10}+k(T_1,T_0).
\tag{10}
\]

The homogeneous representative chooses `k=0`. This is a mathematical normalization, not physics.
If a general representative is required to compose and reverse, its additive term must obey

\[
 k(T_2,T_0)=k(T_2,T_1)+k(T_1,T_0),\qquad
 k(T_0,T_1)=-k(T_1,T_0).
\tag{11}
\]

On one ray interval every regular solution is an endpoint coboundary

\[
 k(T_1,T_0)=f(T_1)-f(T_0).
\tag{12}
\]

It alters neither the phase-space map nor any Hessian or determinant below. The frozen
preregistration's stronger constant-only wording was explicitly qualified before rerun rather than
silently retained.

## 4. Mixed Hessian and determinant density

Define the negative mixed endpoint Hessian

\[
 \boxed{K_{10}=-\partial_{x_1}\partial_{x_0}S^0_{10}=B^{-T}.}
\tag{13}
\]

Its oriented determinant coefficient and positive density coefficient are

\[
 \delta_{10}=\det K_{10}={1\over\det B},\qquad
 \boxed{\Delta_{10}=|\delta_{10}|={1\over|\det B|}.}
\tag{14}
\]

In the transported oriented screen (4) makes `delta_10=Delta_10>0` for both endpoint orders. This
does not turn (14) into an unweighted physical scalar. It is the inverse determinant of the map
from initial screen opening to final screen separation in the declared affine and screen units.

For independent endpoint orthonormal basis changes

\[
 x_i'=R_i x_i,\quad p_i'=R_i p_i,\quad R_i\in O(2),
\tag{15}
\]

the blocks and mixed Hessian transform as

\[
 B'=R_1BR_0^T,\qquad K'=R_1KR_0^T.
\tag{16}
\]

The generator is a scalar under the simultaneous coordinate change. The oriented coefficient
acquires `det(R_1)det(R_0)`, while the absolute coefficient `Delta` is unchanged. Intrinsically,
`K` is a two-endpoint screen tensor and its determinant is a bidensity paired with the endpoint
screen area elements.

## 5. Exact stationary composition

For three endpoints with `T_2` distinct from `T_0`, the G343 block law gives

\[
 B_{20}=A_{21}B_{10}+B_{21}D_{10}.
\tag{17}
\]

The Hessian with respect to the joined screen position is

\[
 \boxed{
 H_1=B_{21}^{-1}A_{21}+D_{10}B_{10}^{-1}
 =B_{21}^{-1}B_{20}B_{10}^{-1}.}
\tag{18}
\]

All three `B` blocks are invertible on this domain, so `H_1` is invertible. Direct elimination of
`x_1` yields

\[
 \boxed{
 S^0_{20}(x_2,x_0)=
 \operatorname{stat}_{x_1}
 \left[S^0_{21}(x_2,x_1)+S^0_{10}(x_1,x_0)\right].}
\tag{19}
\]

Taking determinants in (18) gives the exact density gluing law

\[
 \boxed{
 \Delta_{20}={\Delta_{21}\Delta_{10}\over|\det H_1|}.}
\tag{20}
\]

This was checked for all six endpoint orderings, not only an intermediate point lying between the
outer endpoints. When `T_2=T_0`, `B_20=0` and `H_1` is singular: the composed map is the identity and
leaves the type-I chart exactly as required.

## 6. Reversal and affine-unit typing

G343 reversal gives

\[
 M_{01}=M_{10}^{-1},\qquad B_{01}=-B_{10}^T.
\tag{21}
\]

For the homogeneous representative,

\[
 \boxed{S^0_{01}(x_0,x_1)=-S^0_{10}(x_1,x_0)},\qquad
 \boxed{\Delta_{01}=\Delta_{10}}.
\tag{22}
\]

Under one common positive affine rescaling `nu -> a nu`, G343 gives `p' = a p` and `B'=B/a`.
Consequently

\[
 \boxed{S^{0\prime}=aS^0},\qquad
 \boxed{K'=aK},\qquad
 \boxed{\Delta'=a^2\Delta}.
\tag{23}
\]

Thus the determinant is explicitly affine-weighted. It does not supply an absolute intensity or
distance without an additional operational attachment.

If the two endpoints independently rescale derivative units by `a_0` and `a_1`, then

\[
 M'=S_{a_1}MS_{a_0}^{-1},\qquad
 M'^TJM'={a_1\over a_0}J.
\tag{24}
\]

Unless `a_1=a_0`, this is conformally symplectic rather than canonical in one common `J`. The
separately unit-frequency endpoint convention in G343 therefore requires its already-derived
frequency weights; it may not be treated as a bare canonical generating chart.

## 7. Reference-event covariance

Changing the marked ray event from `T_*` to `T_*'` while converting `rho` and `nu` through the same
invariant ray leaves every G343 block unchanged. Equations (8), (13), and (14) are algebraic in
those blocks, so

\[
 \boxed{S^{0\prime}_{10}=S^0_{10}},\qquad
 \boxed{K'_{10}=K_{10}},\qquad
 \boxed{\Delta'_{10}=\Delta_{10}}.
\tag{25}
\]

The production maximum reference-covariance relative error was
`2.004548090802836e-14`; the independent route obtained `1.2266145247958771e-14`. No reference
event becomes a hidden scale.

## 8. G342 recovery and principal limits

With `T_*=T_0` and `nu=1`, `B` is exactly G342's source-normalized two-screen width map. Hence

\[
 \det B=B_\parallel B_Z
\tag{26}
\]

is its oriented screen-area response, and `Delta` is its inverse determinant coefficient. The
production recovery error was `1.218934242084337e-15`. This is still geometric screen response,
not a flux or observational-distance law.

For the longitudinal principal family, with

\[
 \ell={3T_*^{1/3}\over2\nu}
 (T_1^{2/3}-T_0^{2/3}),
\tag{27}
\]

both screen channels are free:

\[
 M_j=\begin{pmatrix}1&\ell\\0&1\end{pmatrix},\qquad
 \boxed{S^0_{10}={|x_1-x_0|^2\over2\ell}},\qquad
 \boxed{\Delta_{10}={1\over\ell^2}}.
\tag{28}
\]

For the transverse principal family put `kappa=nu T_*^(2/3)`, `r=T_1/T_0`, and use power pairs

\[
 (m,n)=(-1/3,2)\quad\hbox{or}\quad(2/3,1)
\tag{29}
\]

for the parallel and azimuthal screen channels. Their exact scalar blocks are

\[
 A={nr^m-mr^n\over n-m},\qquad
 B={T_0^{5/3}(r^n-r^m)\over\kappa(n-m)},
\tag{30}
\]

\[
 C={\kappa mn T_0^{-5/3}\left(r^{m-5/3}-r^{n-5/3}\right)\over n-m},\qquad
 D={-mr^{m-5/3}+nr^{n-5/3}\over n-m}.
\tag{31}
\]

Both `B` entries are nonzero for `r` different from one, so (8) and (14) remain regular. In
particular

\[
 B_\parallel={3\over7\kappa}
 \left(T_1^2T_0^{-1/3}-T_1^{-1/3}T_0^2\right),
\tag{32}
\]

\[
 B_Z={3\over\kappa}
 \left(T_1T_0^{2/3}-T_1^{2/3}T_0\right),\qquad
 \Delta={1\over|B_\parallel B_Z|}.
\tag{33}
\]

Thus neither principal family loses a generating direction.

## 9. Coincidence behavior and compact lifts

For affine separation `epsilon=s_1-s_0` approaching zero,

\[
 B=\epsilon I_2+O(\epsilon^3),\qquad
 S^0_{10}={|x_1-x_0|^2\over2\epsilon}+O(1),\qquad
 \Delta_{10}=|\epsilon|^{-2}(1+O(\epsilon^2)).
\tag{34}
\]

The pole is the standard boundary singularity of this generating chart at the identity map. Every
noncoincident interior point remains finite and nonzero.

Each supplied compact lift `L` retains its own ray, screen, blocks, generator, and density:

\[
 (S^0_L,\Delta_L).
\tag{35}
\]

Composition occurs only along one fixed lift. Nothing in G344 sums, weights, identifies, or selects
different lifts.

## 10. Evidence and ownership

The repaired production route passed `13580/13580` checks. Its largest generator composition,
Hessian identity, density composition, reference covariance, and principal relative errors were
`3.2374849128501303e-13`, `9.094947017729282e-13`, `1.0032514674597403e-14`,
`2.004548090802836e-14`, and `1.272872367168619e-13`.

The implementation-distinct verifier rebuilt both unit-Wronskian scalar bases by Simpson
quadrature, differentiated the on-shell boundary action numerically, and integrated the Jacobi
state plus quadratic action by RK4. It imported neither production nor G343 implementation and
passed `4882/4882`. Its largest finite mixed-Hessian, density, state-integration, and action-
integration errors were `4.765060002218977e-08`, `9.420668713310874e-11`,
`2.2394617948529441e-13`, and `5.380906802026781e-14`. All fourteen hostile mutations were caught.

Fresh external `gpt-5.4` authenticated all 29 sealed payloads, replayed the registered `19/19`
package gates, performed a separate scratch reconstruction, and accepted the result without repair
or any high-, medium-, or blocking low-severity finding. It retained the non-blocking caveats that
the compact-lift executable checks are documentary in the absence of aggregation code and that
text-token gates are integrity guards rather than analytic proof.

The result is `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`. It is a metric-derived geometric
consequence of the G343 map conditional on the supplied spacetime, ray, screen, affine
gauge, endpoint data, and path label. It supplies no light/flux/probability law, observational
distance, route or population, topology or occupancy, generic stability, matter/mass, scale,
`X_max`, or canon.
