# PRI1 source-first fidelity argument

**Conditional local mathematical construction; raw-moment response identification
refuted in the stated positive null sector. No physical adoption.**
Reviewer `/root/pri_fidelity`, 2026-09-30, fresh separate context and same inherited
model. This argument and exact code were constructed from the question and original
sources listed in SOURCE_PINS.json, before PRI1 producer/other-reviewer exposure.
Parent startup, synchronization and earlier full406 evidence are attributed;
independent branch/HEAD/status inspection and limitations are in CHECK_PLAN.md.
This fixed review record is not another maintained scientific summary.

## 1. The conditional observer theorem and its exact exclusions

Fix a time-oriented Lorentz4 tangent space (V,g), signature -+++, and a nonzero
nonnegative measure mu on nonzero future null vectors. Suppose its second moment
is finite: for any one future unit t, integral[-g(t,k)]^2 dmu is finite. A finite
Lorentz transformation bounds any other frame components by a fixed multiple of
that energy, so this assumption gives a finite tensor

    M_ab = integral k_a k_b dmu,      F(u)=M(u,u),

for every unit future timelike u. Lower indices with the supplied g. The measure,
including its radial weighting, is state information, not derived by defining M.
No normalization of mu or finite first moment is needed for the following theorem.

Write k=e(t+s), e=-g(t,k)>0, where s lies on the t-unit direction sphere. Push
e^2 mu to a finite nonzero positive angular measure nu. For u=cosh(r)t+sinh(r)n,

    F(u)=integral [cosh(r)-sinh(r)<n,s>]^2 dnu(s).

If nu is not concentrated at a single direction, the continuous function

    A(n)=integral (1-<n,s>)^2 dnu(s)

is strictly positive on the compact unit sphere: equality would require s=n
nu-almost everywhere. Its minimum a is positive. Because 1+-<n,s> are
nonnegative, expanding the two exponentials gives

    F(u) >= (a/4) exp(2r),

uniformly in n. Thus F is proper/coercive on the future hyperboloid and attains
a minimum. Along any unit-speed hyperbolic geodesic u(z), u''=u, and

    d^2 F/dz^2 = 2 integral[(g(k,u'))^2+(g(k,u))^2] dmu > 0.

This strict geodesic convexity gives a unique global minimizer U. The first
variation along every g-orthogonal tangent v gives M(U,v)=0, equivalently

    M^a_b U^b = -rho U^a,      rho=M(U,U)>0.

Uniqueness makes this construction covariant under simultaneous transformation
of metric and population. Its positive Hessian on spatial v is
2[M(v,v)+rho g(v,v)], so a smooth non-beam moment field gives a locally smooth
U by the implicit-function theorem. Pointwise finite moments alone do not
assert a smooth spacetime field, global regular query branches, completeness of
the congruence, or controlled behavior through a beam/zero limit.

There are exactly two exceptions for this supplied nonnegative null setting:

* A nonzero measure on one null ray has F(u)>0 but infimum zero, approached by
  boosts toward the ray. No finite timelike rest minimizer/eigenvector exists.
* A zero measure has M=0 and every unit future observer minimizes F. It selects
  none. This case is outside the nonzero theorem, retained as a boundary control.

Non-collinear support means support up to mu-null sets, equivalently nu-null
sets; several different frequencies on the same null ray are still a beam.
Full angular support or spectral isotropy is unnecessary for existence. Two
non-collinear beams already suffice. For opposite beams of weights a,b>0 and
unit energy, F(r)=a exp(-2r)+b exp(2r), so r=(1/4)log(a/b) and rho=2sqrt(ab).
As b tends to zero, r diverges. Therefore uniqueness at each non-beam state is
not a uniform conditioning bound near the excluded beam state.

Finite second moment does not imply finite number measure or first moment.
For k_n=2^-n(1,1,0,0) and mu_n=2^n, the second moment is proportional to
sum 2^-n=1 but the first moment is proportional to sum 1=infinity. A proposed
first-moment observer construction needs extra integrability; the theorem above
does not silently use it.

## 2. The raw moment cannot be DDR's balanced response

The null condition gives tr_g M=0. Central R9 constrains a specified symmetric
covariant E: all-pair DDR is equivalent to E=lambda g. Consequently E=M would
imply 0=4lambda and M=0, contradicted by M(u,u)>0 for every timelike u.
An even stronger direct check is, for every reciprocal pair (u,n),

    <M,H(u,n)>_g
      =2 integral[(g(k,u))^2+(g(k,n))^2] dmu >0.

Thus a nonzero positive null moment does not annihilate even one pointwise
reciprocal pair. The obstruction includes the single-beam case, independently
of whether a rest observer exists. Adding qg leaves TF(M+qg)=M; a nonzero scalar
multiple of M also does not fix the shape obstruction. This rejects that direct
identification, not all physical populations, all response architectures, DDR,
or UDT. A proposed additional geometric/population balance would require a new
identified response and physical relationship; no term, coefficient or coupling
is chosen here.

Exact isotropy in a selected U gives the familiar conditional moment form
M=rho U_flat^2+(rho/3)(g+U_flat^2). Spatial isotropy is not pure metric trace:
the timelike/spacelike signs differ and M remains trace-free and positive on U.
The response E_C from L1, when defined, is instead a first-variation coefficient
with respect to a metric perturbation. Its indices, normalization and variation
rule must be identified; covariance or a positive moment does not establish
E_C=M. Lowering the displayed E_C^{ab} is needed to compare it with R9's E_ab.

## 3. What the observer assignment does not reconstruct

M determines this rest observer and its own finite quadratic data. It does not
determine the underlying population: six equal axial null beams and the same
six beams rotated by a rational nontrivial spatial rotation have identical
M=diag(1,1/3,1/3,1/3). Their fourth xy angular moments are respectively 0 and
96/625. Neither population is angularly isotropic despite its isotropic second
moment. Thus a rest eigenvector, zero momentum flux, or isotropic M cannot be
substituted for C1's full spectral/angular assumption f=F(omega/Theta).

PCW1's controlling repair requires an independently supplied actual population,
not one reconstructed from the redshift being tested. Its collisionless transport,
nonconstant spectrum, all-direction isotropy for one U throughout the region,
and physical clock-flow identification are distinct assumptions. With them,
the source derives the conformal-Killing condition and the clock ratio. The
present broader moment theorem does not derive those hypotheses or extend
their clock conclusion to arbitrary anisotropic populations. It also does not
make a near-isotropic approximation quantitative.

The minimization assumes g and mu. It produces U(g,mu), not a metric field
equation or unique g. Actual null-shell/population observations may constrain
geometry under their own data interpretation; this review does not deny that.
The construction itself supplies no geometric selection criterion or scale.
For example nullness alone is unchanged under positive metric homothety. C1's
already preserved static and expanding controls remain, with their residual
metric freedom. Identifying physical clocks with U adds a physical interface;
choosing sources, observers, separations, emission times, branches and counts
for an ensemble adds further data. A local rest direction does not select all
those query labels, provide native matter/light, or impose a cosmic center.

## 4. L1/CCR1: the physical variation is still a separate gate

On a common label space, under hypotheses allowing differentiation,

    C[g]=(1/2) integral D_g(q)^2 dmu_g(q),
    delta C=integral D delta D dmu +(1/2) integral D^2 delta(dmu).

Here delta D is total: metric, path, reception event, emitter/receiver histories,
clock normalization and the chosen physical query continuation. If U is
population-defined, its variation must be induced by the supplied g/mu variation
law, not set to zero by the background eigenvector equation. A physical null-shell
measure may involve the moving shell, distribution, momentum parametrization,
spacetime density and transport/initial-data choices. These need one consistent
rule. Holding k and its measure fixed under arbitrary g variation generally does
not even preserve g(k,k)=0; the shell constraint itself must be differentiated.

CES1 instead fixes an abstract counting measure, and the metric-dependent
physical image is in Q_g. No additional image Jacobian should then be counted a
second time. CCR1 preserves clocks/preparation by support and proves its formula
for that fixed product measure and the specified regular embedded emission tube.
An independently given population can use a fixed-label realization only if its
actual variation law justifies that realization. Baseline positivity, a supplied
U, or the fact that dmu can be written in some coordinates does not justify it.

Therefore CCR1's necessary condition (wM_mean)'=wJ and strict-sign obstruction
remain valid exactly where its fixed protocol/measure and tube hypotheses hold.
Replacing those labels with a physically changing population cannot inherit the
same derivative while dropping the measure/query terms. The extra terms are
uncomputed, not shown to cancel or repair the obstruction. No weights are tuned,
no GR contribution subtracted, and no replacement score is proposed. Inverse
descriptions at moving matched events reverse both D and delta D, so squared
contributions do not cancel automatically. Future return legs remain distinct.

The extra all-laboratory stationarity quantifier in CCR1 cannot be transferred
to one supplied population. Its small-laboratory counterexamples remain useful
for the stronger universal implementation; they neither select nor exclude all
possible single physical ensembles. Even a vanishing necessary derivative would
not prove a smooth response, finite-jet locality, full stationarity or dynamics.

## 5. Checks, strongest survivors, and omissions

The frozen independent Fraction implementation passed 17 exact finite anchors
and four explicit false-claim rejections in 0.033 seconds (receipt owns exact
timing), Python3.10.12, one thread, 60-second/512MiB limits. Stdout JSON, stderr,
code and capture are preserved. No execution failure or implementation repair
occurred. These checks anchor the analytic argument; they do not certify general
existence by sampling. Exact rational arithmetic is independent of producer
scientific code and does not use SymPy. Python and inherited model are shared;
different-model, human and formal verification were not performed.

Strongest survivors: unique local rest observer on the positive finite-second-
moment non-beam sector; exact beam/zero exclusions; direct raw-moment DDR
obstruction; no replacement of population physics by an isotropic moment; and
unchanged CCR1 limits. Required candidate wording: distinguish observer selection,
population state, response identity and metric selection; require smooth input
for a smooth U; keep C1's extra kinetic/isotropy/clock identifications explicit;
carry full measure and query variation; do not impose the extra universal
laboratory quantifier on one population.

Not done: physical population construction, transport solution or source law,
new response/action/coupling, global observer theorem across degeneracies,
empirical/near-isotropy error bounds, metric selection, native matter/light,
observational fits, old CCR1/CES1 computation replay, independent full406, or
scientific promotion. Candidate and final integration review remain next stages.
