# PRI1 source-first mathematical review

Status: independent conditional argument, sealed before PRI1 candidate exposure;
not adoption, canon, a physical population or a native source identification.

## Context and scope

This is a fresh delegated reviewer context, inherited model (the runtime identifies
Codex/GPT-6; an exact backend variant is not independently exposed), not a
different-model or human review. Parent startup is attributed: synchronized grok
at da27f0b3c64d4eb5eed81732da1ab8964d4a7bac, prior normal guard PASS and unchanged-
science full406 receipt reused, with a fresh final audit still a parent gate.
I independently observed grok and that HEAD, tracked clean, plus PRI1 and the
existing unrelated untracked names. I did not inspect or hash protected payloads.
AGENTS.md and the PRI1 work order govern this bounded review. I read the specified
CLAUDE sections and no-shortcuts, completeness-map, verifier-before-record and
solution-space-not-imposition protocols. The parent owns the top-level orientation.

Scientific exposure: central R9/R17/R18; original PCW1 initial synthesis, repair
and reviewed result; original CCR1 candidate, repair and reviewed result. No PRI1
parent candidate/check code, peer-review argument or candidate result was read.
One prior CCR1 math capture-provenance receipt was read solely to locate the shared
capture utility; no prior reviewer scientific argument/code was read. Shared
Python/SymPy and the standard capture utility are not independent libraries.

The question is pointwise Lorentzian mathematics, signature -+++, on a supplied
time-oriented four-dimensional tangent space V with a nonzero nonnegative Borel
measure mu on future nonzero null vectors. Assume a finite second moment in one
orthonormal frame; finite-dimensional changes of frame preserve this property.
The metric and measure are free-and-explored conditional inputs. All conventional
kinetic/clock identifications remain UNADOPTED. Mathematical frame coordinates,
normalization and exact example weights below are controls, not physical pins.
No spectrum, density, scale, center, source law, action or coupling is selected.

## Independent observer construction and exact degeneracies

Define the symmetric covariant second moment

    T_ab = integral k_a k_b dmu(k),    Q(U)=T_ab U^a U^b,
    Hplus = {U: g(U,U)=-1, U future}.

Finite second moment makes T and Q finite. Nonzero mu on nonzero future null
vectors implies Q(U)>0 for every U in Hplus. Positivity here is ordinary
quadratic positivity of a sum/integral of squares, not positive-definiteness of
the Lorentz metric. No total finite population count or finite first moment is
required.

Let U(t)=cosh(t)U0+sinh(t)V0 be a unit-speed hyperbolic geodesic, with V0 unit
spacelike and orthogonal to U0. Then U''=U and

    d²Q(U(t))/dt² = 2 T(U',U') + 2 Q(U) > 0.

Thus Q is strictly geodesically convex, including for a beam. Strict convexity
alone does not imply existence on this noncompact domain.

For existence, use any future orthonormal frame, k=omega(1,m), omega>0,
|m|=1. Let nu be the finite positive angular measure obtained by pushing forward
omega² dmu. For n on S² put A(n)=integral(1-n dot m)² dnu. A is continuous by
dominated convergence. A(n)=0 precisely when mu is concentrated on the null ray
with direction n, modulo null sets. If no such ray carries all mu, compactness
of S² gives a=min A>0. For U=(cosh r,sinh r n), r>=0,

    Q(U) = integral[cosh r - sinh r(n dot m)]² dnu
         >= (exp(2r)/4) A(n) >= (a/4) exp(2r).

The inequality follows because both terms in
(exp(r)(1-n dot m)+exp(-r)(1+n dot m))/2 are nonnegative.
Consequently Q is proper/coercive on Hplus and attains a minimum. Strict
geodesic convexity and connected geodesic convexity of Hplus give uniqueness.
The constrained critical equation is

    T_ab U^b = -rho U_a,       rho=Q(U)>0.

Conversely a future unit timelike solution is a critical point and hence this
unique minimizer. This is a comparison-observer assignment from (g,mu), without
presupposing its rest frame. It is not an observer selected by g alone.

If mu is a single ray, T=c ell_flat tensor ell_flat with c>0 after normalization.
Boosting toward the ray makes Q tend to zero, while Q>0 at every timelike U.
There is no timelike minimizer/eigenobserver. If mu=0, Q is identically zero and
every observer minimizes, so there is no unique assignment. These cover the
actual degeneracies within the stated positive finite-second-moment domain.
They do not cover signed measures, infinite moments or non-null supports.

Uniqueness gives covariance: for a time-orientation-preserving Lorentz isometry
and the pushed-forward measure, the minimizer is the image of U. This is not
Lorentz invariance of one fixed physical distribution. Overall positive
rescaling of mu changes rho but not U. On a spacetime region where T is smooth
and nowhere beam/zero, the positive Hessian on the hyperboloid gives smooth local
dependence by the implicit function theorem; uniqueness glues these solutions.
For merely measurable data, no smooth congruence follows. Approaching beam
degeneracy can send rapidity to infinity; no uniform conditioning or global
completeness of the resulting clock curves is asserted.

An elementary finite-first-moment alternative is normalization of J=integral k
dmu, when that integral exists. For nonparallel future rays J is timelike, but
this is a different assignment in general. Opposing unit beams with weights16
and1 have moment minimizer U=(5/4,3/4,0,0), velocity3/5, while J=(17,15,0,0)
has velocity15/17. Neither choice is physically compelled by covariance alone.
Finite second moment does not imply finite first moment for the authorized
general measure: atoms k_n=2^(-n)(1,m_n), weights2^n, n>=1, with alternating
nonparallel directions have second energy moment1 but first moment infinity.
This does not affect the Q construction. Finite total count plus finite second
moment would ensure a finite first moment by Cauchy-Schwarz.

## Direct DDR obstruction for the raw moment

Null support gives g^{ab}T_ab=integral g(k,k)dmu=0. Therefore TF(T)=T.
Nonzero positivity gives T!=0. Central R9's all-pair annihilator says DDR for a
specified covariant response requires E=lambda g. Applied to E=T this would
force lambda=0 by the trace, contradicting T!=0.

There is a stronger explicit sign diagnostic for every orthonormal pair (u,n):

    <T,H(u,n)>_g = 2 integral[(g(k,u))²+(g(k,n))²]dmu > 0.

The first squared term is positive for each nonzero null k and timelike u.
This works whether or not the population has a rest observer. No metric with
such a nonzero population can satisfy this particular raw-moment response
identification and all-pair DDR at that point. Adding qg cannot fix it, because
trace terms annihilate H; multiplying T by a nonzero scalar cannot fix it either.
No geometric/population cancellation or coupling is selected by this negative
result. Signed weights are outside the theorem; zero population has trivial
DDR but no unique population observer. The conclusion is about one proposed
response identification, not a no-matter or no-UDT theorem.

Equal-weight null beams in the six coordinate directions give T=diag(6,2,2,2).
Their U=e0 is unique, but <T,H(e0,e1)>=16. Even second-moment spatial isotropy
does not imply full angular/spectral isotropy: the same six-beam distribution
is atomic and anisotropic at the distribution level. Thus observer existence
does not establish C1's Liouville law, exact isotropy, conformal-Killing condition
or endpoint-temperature clock relation. C1 with its extra original hypotheses
survives at its prior scope.

## The physical joins stay separate

L1 defines C[g]=(1/2)integral D_g² dmu_g over physically specified clock queries.
Its derivative contains integral D delta D dmu plus
(1/2)integral D² delta(dmu), with the complete query motion in delta D.
There is no derivation here identifying this coefficient with T_ab. The null
moment is pointwise in supplied state; the clock score depends on queries and
can be nonlocal or lack a smooth-volume representation. Positivity of mu alone
does not force this variational response to be a positive null moment.

Supplying the minimizer U gives a possible comparison-clock direction, not the
emitter/receiver ensemble, a distribution of pair separations, a measure on
those queries, its continuation as g varies, or the stationarity principle.
If actual population data change with g, their full variation must be supplied.
Holding independent counting labels fixed is compatible with metric-dependent
physical images only when that motion is already included, as in CCR1.

CCR1's strict-sign mean obstruction remains valid under its fixed-product-label,
regular rank-four tube, support separation, once-crossing and ordinary-clock
hypotheses. Choosing U from a moment does not invalidate it or automatically
put a new population into its domain. Mixed-sign means remain unclassified;
mean cancellation is neither full stationarity nor a justified weight choice.
The all-laboratory version adds a quantifier and cannot be imposed on a single
physical population. No exact-flat requirement is introduced here.

Population selection, metric selection, physical response identity, population
transport, action variation and any geometric/population balance remain distinct
unadopted joins. No new density, light/matter emergence, native source, Einstein
equation, action, coupling, empirical fit, X_max realization or cosmic center is
inferred. Existing premises have not been proved completely insufficient.

## Evidence ceiling and omissions

The analytic proof carries the universal conditional claim. The separately
frozen exact CPU checks anchor signs, tensor type, covariance, degeneracies and
counterexamples; finite examples do not prove the theorem. No GPU, discretized
solver, observational comparison, transport integration, smooth-volume L1
construction, native matter derivation or full prior-package replay is done.
Checks use one process/thread,60seconds/512MiB per run, within the20MiB package
budget. Any check failure is retained. Direct candidate and final integration
reviews remain pending at this source-first stage.
