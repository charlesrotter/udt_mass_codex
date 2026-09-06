# Local phase compatibility and remaining data — unpromoted candidate

Date: 2026-09-06. Source snapshot: `0c9c6db68ab08618e750c57c0d8f166434aae043`.
Status: `CANDIDATE_ONLY__SAME_CONTEXT_CHECKED__SEPARATE_REVIEW_OUTSTANDING`.
This is an authorized mathematical compatibility test, not G353, an accepted
dependency, a new physical premise, or a selected UDT solution.

## 1. Question and ownership

On a supplied smooth time-oriented four-dimensional Lorentzian manifold of
signature `(-,+,+,+)`, supply a smooth nonzero future null field `ell` on an
open neighborhood. A congruence on a neighborhood is more data than one ray.
Ask whether, after shrinking around a point, there are smooth `alpha>0` and
dimensionless phase `Theta` such that

\[
\beta=g(\ell,\cdot),\qquad d\Theta=\alpha\beta.                 \tag{1}
\]

This tests the null **direction** completion proposed in the decision brief.
It does not assume that rescaling a prescribed frequency is allowed. If the
fully normalized vector itself must be the phase gradient, the question is
instead `dTheta=beta` and has a stronger compatibility condition below.

G348 supplies geometric operations, the positive quotient screen
`ell^perp/span(ell)`, null-geodesic/Jacobi geometry and observer frequency on
supplied data. Its Jacobi phase space is not a scalar phase `Theta` or a
population measure. G349 concerns a supplied finite source-vertex wavefront
map, not every arbitrary null congruence. Neither package selects this
neighborhood, a metric development, a ray population, or phase normalization.

G351's source-free conservation and G352's clock-rate readout are
owner-adopted **provisional** premises. G352 additionally chooses the
continuous product realization with common positive spacing and the same
label measure at each phase. This test keeps those roles separate.

## 2. Exact local compatibility criterion

For the stated smooth nonvanishing one-form, the following local equivalence
is the candidate mathematical conclusion:

\[
\boxed{\text{(1) exists locally}\quad\Longleftrightarrow\quad
              \beta\wedge d\beta=0\text{ on a neighborhood}.} \tag{2}
\]

Necessity follows by differentiating (1):
`0=dalpha wedge beta + alpha dbeta`; wedging with `beta` gives (2).
For sufficiency, the smooth codimension-one Frobenius theorem applied to
`ker(beta)` gives a local submersion `Theta` and a nowhere-zero function `h`
with `beta=h dTheta`. Shrink to a connected chart; reversing `Theta` if
necessary makes `h>0`, so `alpha=1/h>0`. These are the hypotheses and use of
a standard mathematical method, not a UDT physical law.

When the input is already G352's supplied exact phase, take `ell=k` and
`alpha=1`: (2) holds automatically. This test concerns completion from weaker
ray data, not a defect in the accepted readout package.

The condition must hold on an open neighborhood, not just at one point.
The conclusion is local after shrinking. No global integrating factor,
global real-valued phase, leaf-space separation, absence of caustics, or
global product follows merely from contractibility or local Frobenius.

Let `k=(dTheta)^sharp=alpha ell`. Nullness follows from (1). Metric
compatibility and the symmetry of the Hessian of a scalar imply

\[
 k^a\nabla_a k_b=k^a\nabla_b k_a
             =\tfrac12\nabla_b(k^ak_a)=0.                    \tag{3}
\]

Thus this phase gradient is affinely geodesic. If the supplied field obeys
`nabla_ell ell=kappa ell`, a necessary rescaling relation is

\[
 \ell(\log\alpha)=-\kappa.                                \tag{4}
\]

In particular an already affine `ell` requires `ell(alpha)=0`. Equation (4)
alone is not sufficient for (1): it has no transverse integrability check.
Twist-free null directions do imply pregeodesicity through (1)--(3), but
geodesicity alone does not imply twist-freedom.

If normalization is prescribed and cannot be changed, `alpha=1` is required;
the local criterion becomes `dbeta=0` (local Poincare lemma), not merely
`beta wedge dbeta=0`. More generally a prescribed `alpha_0` must satisfy
`d(alpha_0 beta)=0`. Additional normalization data cannot be silently repaired
by a newly selected phase.

## 3. Compatible local phase/label/cut construction

Suppose (1) exists. Choose a sufficiently small smooth spacelike three-slice
`S` transverse to `k`. Its restriction `Theta|S` is a submersion: otherwise
the nonzero null covector `dTheta` would be proportional to the timelike
normal covector of `S`. Choose coordinates `(theta,lambda^1,lambda^2)` on
`S` with `theta=Theta|S`. Flow along the nonzero field `k`, using affine
parameter `r`. The local flow theorem, transversality, and inverse function
theorem give, after shrinking, a coordinate map

\[
 F:I\times\Lambda\times(-\epsilon,\epsilon)\longrightarrow M,
 \quad \partial_rF=k,\quad \Theta\circ F=\theta.             \tag{5}
\]

The last equality follows from `k(Theta)=g(k,k)=0` and its initial value.
Thus phase is constant **along** a null generator; it varies when an
observer crosses phase sheets. This is not an evolution of phase along its
own null ray.

On `S`, each fixed-theta two-surface is spacelike. In a sufficiently small
flow neighborhood its two connecting vectors remain of positive screen
rank two. They annihilate `dTheta`, so lie in `k^perp`. A smooth variable cut
`r=r_i(theta,lambda)` adds only `(partial_lambda r_i)k` to each connecting
vector. Nullness and orthogonality remove those added terms from their
metric Gram matrix. This is the local metric mechanism used by G349;
it does not identify this arbitrary congruence with G349's full source-vertex
construction or transfer its global finite-map conclusions.

The slice, labels, their identification between phase sheets, and cuts in
(5) are supplied mathematical query data. They are not canonical metric
choices. This is not a claim that a single supplied G349 cone uniquely
determines a neighboring family of cones or its phase spacing.

On a compact label subpatch choose any finite nonnegative countably additive
Borel measure `mu`, and choose `DeltaTheta>0`. On a bounded phase interval,

\[
 d\Xi={|d\theta|\over\Delta\Theta}\otimes d\mu              \tag{6}
\]

is a finite measure. For fixed phase, each cut pushes the same `mu` forward
by `X_i(lambda)=F(theta,lambda,r_i(theta,lambda))`. Therefore (6) is a
mathematically compatible implementation of the declared G351/G352 source-free
product conditions. It is **not** a proof that there is nonzero carried
content. Zero is included.

For supplied smooth future unit observers on a compact retained regular
patch, `omega_i=-u_i(dTheta)>0` is bounded. This is a sufficient condition
for frequency integrability against finite `mu`; for more general supplied
observers one must require that integrability explicitly. On the absolutely
continuous part, with `dmu_ac=s dlambda` and `dA_i=J_i dlambda`, `J_i>0`,

\[
 \Gamma_i={\omega_i\over\Delta\Theta}{s\over J_i},\qquad
 {\Gamma_j\over\Gamma_i}=R_{ji}A_{ji}^{-1}\quad(s>0).         \tag{7}
\]

Equation (7) reconstructs accepted G352; it is not a newly derived physical
readout law. Zero density does not define the ratio. Singular measures have
no ordinary two-area density for that part. Literal atomic phase crossings
remain distinct from continuous phase intensity. This local construction
does not extend the density formula through rank loss.

## 4. Remaining data and representation freedoms

### Phase

On a sufficiently small connected foliation chart, any two phases with
positive gradients aligned to the same null line distribution satisfy
`Psi=f(Theta)`, `f'>0`. Indeed `dPsi` annihilates all tangent vectors to each
connected Theta leaf, so Psi depends only on Theta. Locally this describes
the phase freedom for the fixed foliation; it is not a global classification.

G352 treats `Theta -> b Theta+c`, `DeltaTheta -> b DeltaTheta`, `b>0`, as a
common affine gauge. A nonlinear `f` changes fixed phase increments and is
not that gauge. At a fixed prescribed spacing it rescales local intensity
by `f'(Theta)`. Since `Theta` is constant along each ray, it can leave
same-ray two-cut ratios unchanged. Agreement of those ratios consequently
cannot establish the absolute phase profile. If normalized `k` is fixed,
this freedom is restricted; it must not be confused with a freedom preserving
every supplied datum.

### Measure and population

Equations (1)--(7) do not determine `mu`. For the same metric, phase, labels,
and endpoint maps, `mu=0`, constant densities of different totals, and
distinct positive densities of the same total are compatible data. For
example on the unit square, densities `1` and `x+1/2` both have total one
but give masses `1/2` and `3/8` to `x<=1/2`. With the endpoint map held fixed,
these are different measures on the same geometric regions, not merely
different names for the labels. The square and its numbers are exact test
controls, not a selected physical support or scale.

This establishes underdetermination by the **stated conditions**. It does
not prove that no further accepted argument, initial-data convention,
observational input, or future metric functional could select particular
data. No universal no-go or mandatory-new-premise conclusion is claimed.

### Conservation along cuts versus independence across phase

On the supplied product chart, a family `mu_theta` may be conserved across
all `r` cuts at each theta while differing between theta values. For example
`mu_theta=(2+theta)mu_0`, `theta in (-1,1)`, satisfies that per-phase
conservation but is not the same-mu factorization (6) in the fixed phase
coordinate and fixed cross-phase identification. Its total slice mass varies,
so bijective relabeling within a phase sheet cannot remove the difference.
This control is outside G352's chosen product branch, not a refutation of it
and not a newly adopted source law. A nonlinear phase-coordinate change can
absorb some scalar variation into the phase factor, but changes the supplied
phase and fixed-increment rule; that is not the declared affine gauge.

Conversely `lambda'=(exp(theta)x,y)` can make a genuine product look
phase-dependent: density becomes `exp(-theta)` on
`[0,exp(theta)] x [0,1]`. Its mass stays one. When measures and cut maps are
transformed together this is only passive relabeling, not physical
nonuniqueness. The product condition has meaning relative to a specified
identification of labels across phases. The metric does not supply that
identification in this argument.

## 5. Explicit exact controls

All examples are mathematical tests in Minkowski geometry, not selected UDT
developments, physical emitters, units, frequencies, or sources.
Their coordinates are dimensionless test-chart parameters; no relation to
observed clock/ruler calibration is supplied.

1. Plane: `ell=partial_t+partial_z`, `beta=-dt+dz`,
   `Theta=z-t`. A product chart is
   `F(theta,x,y,r)=(r,x,y,r+theta)` and its transverse Gram matrix is the
   identity. This witnesses compatibility, not generality or determination.
2. Integrating factor needed: multiply the plane field by `1+x^2`.
   It remains affine and null, `dbeta` is nonzero off `x=0`, but
   `beta wedge dbeta=0` and `alpha=1/(1+x^2)` gives the same exact phase.
   Thus closedness of the unscaled form is too strong for the direction
   question but is the correct requirement for the fixed-normalization question.
3. Obstruction to weaker input: `ell=(1,cos z,sin z,0)` in `(t,x,y,z)`
   is smooth future null and affine geodesic. Direct differentiation gives
   the `(t,x,z)`, `(t,y,z)`, `(x,y,z)` components of `beta wedge dbeta`
   as `-sin z`, `cos z`, `-1`. No local integrating factor exists anywhere.
   This does not satisfy an orthogonal wavefront-foliation hypothesis.
   It is **not** a counterexample to G349's source-vertex wavefront or to
   G352 on its supplied exact-phase domain.
4. Pointwise caution: replace `z` in that field by `z^2`. The last component
   becomes `-2z`; all components vanish on `z=0`, but not on any open
   neighborhood there. Pointwise testing would falsely certify local phase.
5. Nonlinear phase: `Psi=Theta+Theta^3` preserves direction and affine
   geodesicity, with multiplier `1+3Theta^2>0`. It changes absolute rates at
   fixed DeltaTheta; equal same-ray transfer ratios do not remove this freedom.
6. Expanding regular cones: in spherical Minkowski coordinates
   `g=diag(-1,1,r^2,r^2 sin^2 vartheta)`, take `Theta=r-t`,
   `k=(1,1,0,0)`, `r>0`, and an angular patch away from poles. The chart
   `F(theta,a,b,r)=(r-theta,r,a,b)` has `J=r^2` relative to solid-angle labels.
   Fixed-theta sheets are portions of source-vertex cones with excluded apex
   `t=-theta,r=0`. This exhibits a compatible mathematical family without
   asserting actual emission. At radii `2,3`, use respectively rest observer
   and radial observer `(5/4,3/4,0,0)`. Their frequencies are `1,1/2`;
   `A=9/4`, `R=1/2` and direct density transfer is `2/9`.
   All radii and boosts are exact witness controls, not imposed physics.

`check_witnesses.py` recomputes the finite examples from metric matrices,
fields, derivatives, Gram determinants, contractions and measure integrals.
The analytic arguments, not a finite assertion count, support the general
local statements. The examples are not a solution-space census.

## 6. Decision ceiling and next gate

The compatible branch needs no additional physics merely to construct local
mathematical examples. Not every weaker null-geodesic input admits the chosen
phase realization. Even when compatible, the stated conditions leave phase
assignment/normalization, cross-phase identification, spacing and measure
data open. Whether any physical content realizes them remains open.

This package stops before choosing among native determination, admissible
initial/source data, an optional readout construction, an additional physical
premise, or a different realization. These are alternatives, not a forced
binary of native derivation versus new postulate.

The next permitted procedural step is source-first separate-context
substantive review of this pinned candidate. If it survives, a subsequent
bounded question could ask which of its residual data are already fixed by
a **specified accepted** source/family/normalization construction. That
requires identifying the exact construction, not inventing one here.
Promotion/direction-gating awaits that review; no archive access is needed.

Backup completeness and pre-reboot unsaved-state disposition remain
unverified. ScratchDisk remains a blocker only for archive-dependent work.
