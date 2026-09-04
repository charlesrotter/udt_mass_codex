# G341 exact derivation — nonprincipal finite null relation and screen carry

Date: 2026-09-04
Grade: `EXTERNALLY_ACCEPTED_DERIVED_CONDITIONAL_BOUNDED`

## Bounded landing

```text
EACH_NONZERO_UNIVERSAL_COVER_LIFT_HAS_ONE_REGULAR_FUTURE_NULL_SOLUTION
__NO_INTERIOR_CONJUGATE_CAUSTIC_ON_THE_SUPPLIED_TAUB_KASNER_NULL_CONE
__MIXED_RAYS_HAVE_NONZERO_G269_NULL_ROTATION_WITH_TRIVIAL_SCREEN_QUOTIENT_ROTATION
__COMPACT_MULTIPLICITY_IS_PATH_LABELLED_NOT_PER_LIFT_NONUNIQUENESS
__NO_LIGHT_MODEL_ROUTE_POPULATION_SCALE_OR_XMAX_SELECTED
```

G341 selects preregistered alternative A on the exact supplied G340 spacetime. This is a
one-spacetime, fixed-normal-observer, supplied-lattice classification. It neither changes the
metric/kernel nor supplies radiative physics or a physical branch population.

## 1. Exact spacetime and reduction

Use

\[
 g=-dT^2+a(T)^2dX^2+b(T)^2(dy^2+dz^2),
\]

\[
 a=C_XT^{-1/3},\qquad b=C_\perp T^{2/3},\qquad T>0.
\tag{1}
\]

Translation symmetry conserves the spatial covector `(p_X,p_y,p_z)`. Rotate only the transverse
coordinate labels so that `p_perp=sqrt(p_y^2+p_z^2)` lies along `Y`; the orthogonal azimuthal
screen direction is retained. For `p_X` and `p_perp` both nonzero define

\[
 \lambda={C_Xp_\perp\over C_\perp|p_X|}>0.
\tag{2}
\]

Positive rescaling of all momenta is affine gauge. With

\[
 \omega(T)={|p_X|\over C_X}T^{-2/3}\sqrt{T^2+\lambda^2},
\tag{3}
\]

the magnitudes of a future ray's longitudinal and transverse displacements are

\[
 Q_X(T_r,\lambda)={1\over C_X}\int_{T_e}^{T_r}
 {T^{4/3}\over\sqrt{T^2+\lambda^2}}\,dT,
\tag{4}
\]

\[
 Q_\perp(T_r,\lambda)={\lambda\over C_\perp}\int_{T_e}^{T_r}
 {T^{-2/3}\over\sqrt{T^2+\lambda^2}}\,dT.
\tag{5}
\]

The signs and transverse azimuth equal those of the conserved momenta. Thus (4)--(5), the two
signs, and one azimuth cover every mixed direction without deleting the second screen direction.

## 2. Local endpoint rank

Put

\[
 I(T_r,\lambda)=\int_{T_e}^{T_r}
 {T^{4/3}\over(T^2+\lambda^2)^{3/2}}\,dT>0.
\tag{6}
\]

At fixed arrival time,

\[
 \partial_\lambda Q_X=-{\lambda I\over C_X}<0,
 \qquad
 \partial_\lambda Q_\perp={I\over C_\perp}>0.
\tag{7}
\]

At fixed direction,

\[
 \partial_{T_r}Q_X={T_r^{4/3}\over C_X\sqrt{T_r^2+\lambda^2}}>0,
\]

\[
 \partial_{T_r}Q_\perp={\lambda T_r^{-2/3}\over
 C_\perp\sqrt{T_r^2+\lambda^2}}>0.
\tag{8}
\]

Consequently the mixed two-variable endpoint determinant is

\[
 \boxed{
 \mathcal D=
 \partial_{T_r}Q_X\,\partial_\lambda Q_\perp
 -\partial_\lambda Q_X\,\partial_{T_r}Q_\perp>0.
 }
\tag{9}
\]

The direction-to-wavefront derivative at fixed `T_r` is also nonzero by (7), and the azimuthal
derivative has length `Q_perp>0`. Thus the future null cone is an immersion throughout the mixed
stratum.

The apparent loss of the azimuth coordinate at `lambda=0` is polar-coordinate degeneracy, not
geometric rank loss. In Cartesian transverse direction coordinates,

\[
 Q_\perp={\lambda\over C_\perp}\int_{T_e}^{T_r}T^{-5/3}dT+O(\lambda^3),
\tag{10}
\]

with a strictly positive linear coefficient. At the transverse principal boundary use
`mu=1/lambda`; then

\[
 Q_X={\mu\over C_X}\int_{T_e}^{T_r}T^{4/3}dT+O(\mu^3),
\tag{11}
\]

again with positive coefficient. The second tangent direction there is transverse azimuth. Both
principal limits are therefore regular in nonsingular direction charts.

Because `dT/ds=omega>0`, replacing affine length `s` by `T_r` is a smooth change of parameter on
every regular future leg. Equations (7), (10), and (11) therefore show that the null exponential
map has no positive-time interior conjugate caustic on this supplied universal-cover cone. The cone
vertex `T_r=T_e`, zero momentum, and the spacetime boundary `T=0` remain excluded boundaries.

## 3. Global endpoint inverse

Fix `q_X>0`. For each finite `lambda>=0`, `Q_X` grows continuously from zero to infinity with
`T_r`, so there is one arrival `T_r=L(lambda)` satisfying `Q_X=q_X`. Equation (7) and the implicit
function theorem give

\[
 L'(\lambda)=-{\partial_\lambda Q_X\over\partial_{T_r}Q_X}>0.
\tag{12}
\]

Along this constant-`Q_X` curve,

\[
 {dQ_\perp\over d\lambda}\bigg|_{Q_X}
 ={\mathcal D\over\partial_{T_r}Q_X}>0.
\tag{13}
\]

At `lambda=0`, `Q_perp=0`. As `lambda` tends to infinity, (4) forces `L(lambda)` to infinity for
fixed positive `q_X`. Moreover,

\[
 Q_\perp\ge {1\over\sqrt2C_\perp}
 \int_{T_e}^{\min(L(\lambda),\lambda)}T^{-2/3}dT\longrightarrow\infty.
\tag{14}
\]

Thus (13) maps `lambda in [0,infinity)` continuously and strictly increasingly onto every
`q_perp>=0`. Every mixed `(q_X,q_perp)` has exactly one `(T_r,lambda)`. The principal endpoints are
the exact G340 limits and are unique as well. Restoring signs and azimuth proves:

\[
 \boxed{
 \text{Every nonzero universal-cover spatial lift and }T_e>0
 \text{ determine one future null leg and one arrival time.}
 }
\tag{15}
\]

This is an analytic global result. Numerical root convergence is only regression evidence for it.

## 4. Compact branches

For a supplied translation lattice `Gamma`, every nonzero lift

\[
 q_\ell=\Delta x+\ell,\qquad \ell\in\Gamma,
\tag{16}
\]

has the unique branch (15). Hence the quotient generally has a countable path-labelled family,
not a multivalued inverse within one lift. For any finite arrival bound the wavefront is compact,
so only finitely many lattice vectors arrive below that bound; an earliest branch exists. Several
lifts can tie by lattice or metric symmetry. Such a quotient branch crossing/cut tie is not a
conjugate caustic of an individual universal-cover branch. No route is removed or physically
populated by this classification.

## 5. General frequency and a zero-shift mixed direction

Let

\[
 \alpha(T)={\omega(T)\over\omega(T_e)}
 =\left({T\over T_e}\right)^{-2/3}
 {\sqrt{T^2+\lambda^2}\over\sqrt{T_e^2+\lambda^2}}.
\tag{17}
\]

At reception,

\[
 r={\omega_e\over\omega_r}=\alpha_r^{-1},
 \qquad \delta=-\log r=\log\alpha_r.
\tag{18}
\]

These expressions continuously join the longitudinal and transverse G340 formulas. For
`R=T_r/T_e>1`, exactly one mixed direction has `r=1`:

\[
 \boxed{
 {\lambda_0^2\over T_e^2}
 ={R^{4/3}\over R^{2/3}+1}.
 }
\tag{19}
\]

This is a zero ordered frequency depth, not zero displacement or zero complete relation.

## 6. Exact screen transport

Use the orthonormal frame

\[
 e_0=\partial_T,\quad e_1=a^{-1}\partial_X,\quad
 e_2=b^{-1}\partial_Y,\quad e_3=b^{-1}\partial_Z.
\tag{20}
\]

Its only needed expansion rates are

\[
 H_1=-{1\over3T},\qquad H_\perp={2\over3T}.
\tag{21}
\]

Write the local ray direction and natural in-plane screen as

\[
 n=c e_1+s e_2,\qquad S=-s e_1+c e_2,
\]

\[
 c={\operatorname{sgn}(p_X)T\over\sqrt{T^2+\lambda^2}},
 \qquad s={\lambda\over\sqrt{T^2+\lambda^2}}.
\tag{22}
\]

Direct evaluation of the Levi-Civita connection gives

\[
 \nabla_{e_0+n}S={cs\over T}(e_0+n),
 \qquad \nabla_{e_0+n}e_3=0.
\tag{23}
\]

Normalize the affine tangent at emission,

\[
 \ell={k\over\omega_e}=\alpha(e_0+n),\qquad \nabla_k\ell=0,
\tag{24}
\]

and define

\[
 \mathcal J(T)=\int_{T_e}^{T}{c(u)s(u)\over u\alpha(u)}du.
\tag{25}
\]

Then the exact parallel screen basis is

\[
 \boxed{E=S-\mathcal J\ell,\qquad Z=e_3.}
\tag{26}
\]

The source and target local in-plane screen vectors therefore represent the same class in the
screen quotient `ell-perp/span(ell)`: the difference is a null-gauge multiple of `ell`. The natural
screen-quotient rotation is zero, and `Z` is parallel even before quotienting. This does not make
the full transported source pair plane equal to the target-local pair plane.

## 7. G269 mismatch and G298 pair planes

Let the source clock and source ray direction be transported to reception. A null-frame
decomposition using (26) gives

\[
 U_r=\Gamma\widetilde U_e+A\widetilde n_e+W,
\]

\[
 \boxed{W=\alpha_r\mathcal J_r E,}
\tag{27}
\]

\[
 \Gamma={1\over2}\left(\alpha_r+\alpha_r^{-1}
 +\alpha_r\mathcal J_r^2\right),
\]

\[
 A={1\over2}\left(-\alpha_r+\alpha_r^{-1}
 +\alpha_r\mathcal J_r^2\right).
\tag{28}
\]

Since the integrand in (25) has one fixed nonzero sign on every mixed ray,

\[
 \boxed{W\ne0\quad\Longleftrightarrow\quad p_Xp_\perp\ne0.}
\tag{29}
\]

It vanishes on both principal families. With `r=alpha_r^{-1}`, (27)--(28) reproduce G269 exactly:

\[
 \Gamma=\cosh\delta+{r\over2}\lVert W\rVert^2,
 \qquad M_{\rm PT}=\Gamma^{-1}<\operatorname{sech}\delta
\tag{30}
\]

on every mixed branch. Under mathematical reversal,

\[
 \lVert W_{reversed}\rVert^2=r^2\lVert W\rVert^2,
\tag{31}
\]

and (30) keeps the same `Gamma`; a later physical return remains a separate future leg.

At the zero-shift direction (19), `delta=0` while `W` is nonzero, so

\[
 \boxed{M_{\rm PT}<1=\operatorname{sech}(0).}
\tag{32}
\]

This is a clean example in which terminal reciprocal depth is quiet but the complete relation is
not.

G298's transported-source and target-local pair one-jets both remain regular:

\[
 \det h_T=-r^2(1+A^2)<0,\qquad \det h_L=-r^2<0.
\tag{33}
\]

Their image-plane separator is proportional to `-r^2 W` and is nonzero on every mixed branch.
Thus the complete relation state owns both planes and their carry, but G341 does not choose one
rank-two projection as the unique physical kernel input.

## 8. Evidence and ownership

Production passed `8992/8992` nonlinear endpoint, rank, inverse, frequency, screen, reversal,
axis-limit, zero-shift, and lattice checks. An implementation-distinct reconstruction from the
coordinate metric and Christoffel symbols used composite-Simpson quadrature, a slope-first inverse,
and direct RK4 vector transport; it imported no production code or results and passed `4400/4400`.
Sixteen hostile mutations were all caught by the same validator used for the baseline.

The no-caustic statement is restricted to the null cone of one event in this exact universal-cover
spacetime for `T>T_e>0`; it is not a theorem for generic G332 developments or perturbed metrics.
Jacobi intensity, brightness, polarization dynamics, sources, and detection remain outside scope.

The metric, completed-pair kernel, angular sector, and provisional equation are unchanged. No
physical route, distance protocol, observer population, topology, occupancy, stability, scale,
`X_max`, or canon is selected.

Fresh sealed external `gpt-5.4` review authenticated all 30 manifest payloads, reproduced
production `8992/8992`, implementation-distinct direct metric/Christoffel `4400/4400`, hostile
`16/16`, and aggregate no-write `20/20`, independently rederived the bounded result, and found
no defect at any severity. The implementation-distinct replay is not premise-independent, and the
aggregate verifier is an integrity gate rather than the analytic proof.
