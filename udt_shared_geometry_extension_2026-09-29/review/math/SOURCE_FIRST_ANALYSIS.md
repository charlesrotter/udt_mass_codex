# SGE1 mathematical source-first reconstruction

Reviewer: `/root/sge_math`, fresh separate context, 2026-09-29. This is a
review-stage analysis, not an accepted scientific result. Parent startup is
attributed; reviewer independently observed branch `grok` and HEAD/origin-grok
`2187825a5a9077d2078deeecb386632d7ab31018`, with no tracked dirt at inspection.
Unrelated untracked files and protected path names appeared in `git status`;
none of their payloads were read, hashed or changed. Parent owns remote-sync
verification and the full premise audit. The reviewer has not read SGE1's
candidate, author implementation or outputs at this stage.

## Scope, sources and review independence

Read AGENTS.md; CLAUDE How we work, DRIVER TRIGGERS and Repo discipline;
no-shortcuts, completeness-map and verifier-before-record protocols;
CROSS_MODEL_VERIFY; authorized SGE1 WORK_ORDER; development definitions,
R1--R8 and R16--R18. Exact clock sources read: FSL1 initial+repair; ICN1
reviewed result; G220 audit; NCI1 initial+repair; DCI1 initial sections1--3;
PGC1 CANDIDATE sections1--4; CRD1 initial sections1--7 and reviewed result.
G220/G402/G403/G415 registry rows were inspected to establish actual scope
and source grades. The latter is only contextual, no G415 result is used below.
Original source review verdicts and proofs were therefore exposed: this is
source-first relative to the new SGE1 candidate, not blind to prior science.

Same inherited model; exact runtime identifier unavailable. Different-model,
human specialist, formal-proof and different-library independence UNTESTED.
The source-first checks are reviewer-written, share Python/SymPy and standard
geometry with the project, and import no author code. Existing full historical
checks, observational fits, raw fields and native metric admission are not
replayed. Hashes establish correspondence only.

Mathematics is on a supplied smooth time-oriented Lorentz4 region with
Levi-Civita connection, ordinary timelike proper clocks and regular future-null
comparison branches. The conditional interface and W4 retain their existing
grades. No new physical congruence, action, source, population, scale or law is
adopted. Symbols set c_E=1 in proper-length units; c_E remains observed.
Free observer extensions, directions, chart choices and restricted diagnostic
metrics are free-and-explored query/method data, not selected UDT solutions.

Before computation: exact algebra and one direct null-incidence example test
the identities below; individual checks are capped at60s/512MiB, threads1,
CPU only, no grids/GPU. Maximum conclusion is scoped geometric necessity and
countercontrols against wider claims. No physical or empirical validation.

## 1. One metric fixes the finite received-clock functional

For a smooth ray family with tangent k and variation J, torsion-free metric
compatibility gives d[g(k,J)]/dλ=0. At endpoint proper-clock curves this yields
Z=dτ_o/dτ_e=ω_e/ω_o>0, ω=-g(k,u). Consequently any proposed additional
positional effect, while retaining the interface, must alter the actual metric,
observer/event/path assignment or their realized relations so that this SAME
functional has the required value. Appending an independent clock multiplier
to fixed identical g, curves, rays and calibrations would contradict the
already fixed received-tick definition. This is consistency for fully specified
inputs, not proof that the full current UDT premises are underdetermined.

Extra effect and ordinary SR/GR behavior need not be separate metric summands
or scalar factors. No invariant subtraction is defined without a comparison
geometry, mapping, matched observer/ray protocol and physical attribution.
Even if such a diagnostic split is declared, it is not thereby a native law.
Finite durations require integrating Z over source proper time.

## 2. A useful exact local directional restriction

Choose any smooth future unit extension U along the ray matching the endpoint
clocks; write k=ω(U+n), g(n,n)=1, g(U,n)=0. Put

    ∇_a U_b = -U_a a_b + H(g_ab+U_a U_b) + σ_ab + w_ab,
    H=div(U)/3,        dℓ_U=ω dλ>0.

Then null parallel transport gives

    d log Z/dℓ_U = H + a·n + σ(n,n) =: B(n),
    log Z_AB = ∫_ray B(n) dℓ_U.

Here Z along the ray is ω_e/ω; this is not the observer-time drift of a tracked
source. Vorticity cancels from this one contraction, but can enter derivatives,
curvature and frame transport. B has only scalar, dipole and trace-free
quadrupole angular content at one point. An alleged smooth-metric clock-rate
field with higher angular harmonics for this exact query definition would fail
the interface. This is a restriction on the ideal local record, not a claim
that all directions are populated or instrumentally available.

If an additional assumption requires B(n)=H for EVERY direction, comparing n
and -n forces a=0, and comparing all quadratic directions forces σ=0.
Isotropy is not inferred from the word positional. Conversely opposite local
directions are both positive precisely when H+σ(n,n)>|a·n|. These rates are at
one event; this is not a theorem about a finite outbound and later return ray.

For |B|≤K on a regular ray with accumulated ℓ_U-length L, |log Z|≤KL and
|Z-1|≤exp(KL)-1. Thus smooth bounded same-congruence rate effects vanish as
L→0. Fixed nonzero endpoint relative rapidity is a different limit, retaining
ordinary SR Doppler contrast; a uniformly bounded interpolating U cannot be
silently assumed there. Local SR does not force a finite signal comparison to
have unit Z, nor does it say its leading variation is purely curvature.

This identity and endpoint-potential restrictions are established G402/G403
mathematics, not new SGE1 discoveries. In the stronger sector where all short
null comparisons share one scalar Ψ with log(ω_B/ω_A)=Ψ(B)-Ψ(A), the positive
vector e^-Ψ U must be conformal Killing. To reconstruct this, constancy of
e^-Ψω along every null direction forces S_ab k^a k^b=0 for
S_ab=∇_(a(e^-ΨU_b)); the null-quadratic lemma forces S proportional to g.
Equivalently σ=0 and α=a_flat-H U_flat is exact. Closed α is only locally
sufficient; global periods matter. A one-endpoint scalar potential is an extra
representation property, not a requirement on all UDT pair comparisons.

## 3. An exact obstruction in a restricted stationary sector

Let ξ be a timelike Killing field on the entire compared region and let BOTH
clocks follow its normalized stationary orbits, U=ξ/N, N=sqrt(-g(ξ,ξ)).
For every connecting affine null ray,

    E=-g(k,ξ)=constant,       ω=E/N,       Z=N_o/N_e.

N is constant along each stationary orbit. Thus an immediate later future
return, if available on regular branches, has p=N_B/N_A and q=N_A/N_B,
so pq=1. A fixed proper relay delay changes the delay but retains unit relay
derivative and the same slope conclusion. A nonconstant relay map is different.
Stationary shift/Sagnac timing does not defeat the frequency argument: ξ need
not be hypersurface orthogonal. Chronology or separately checked ordered
return is still needed to interpret radar distance as positive.

Therefore BOTH NET-redshifted legs cannot arise in this restricted stationary
observer sector. They require abandoning at least one listed hypothesis or
changing the query, but this theorem does not select which. Static field
geometry with moving observers lies outside the sector. The owner speaks of
an additional positional effect within combined observations, so this theorem
does not by itself refute that component or the founding interpretation.
It neither proves cosmic expansion nor requires a new physical premise.

The reviewer check uses direct incidence in a positive Rindler strip
ds²=-(1+ax)²dt²+dx²+dy²+dz², stationary clocks at0,d, a,d>0. A one-way
coordinate delay is log(1+ad)/a. Differentiating actual proper-clock arrival
maps gives p=1+ad, q=1/(1+ad), and F'=1. This is an independently implemented
control, not native admission or proof of the general theorem by sampling.

## 4. Actual two-way and asymptotic restrictions survive

On actual relay events, F=f_BA∘f_AB and F'=pq>0. When F>s,
T=(s+F)/2, R=c_E(F-s)/2 imply β_rad=(pq-1)/(pq+1).
For S=(log p+log q)/2, K=(log p-log q)/2, both legs have net redshift iff
S>|K|; both diverge iff S-|K|→∞. Positive radar drift alone does not imply
both legs redshift. This is ICN1's exact protocol restriction, with its
chronology and longitudinal-inverse hypotheses retained; it is not a
cosmological expansion or physical local-speed theorem.

Likewise a transport arrow with future clock column (γ,s), χ=s/γ and actual
reception propagation direction n_o gives Z=γ-s·n_o. Let r=|χ|→1 and
μ=χ·n_o/r. Then Z→∞ iff (1-μ)/sqrt(1-r)→∞. Norm saturation alone does not
force divergent redshift; the source's exact (γ,s)=(1+q²/2,(q²/2,q,0))
has Z=1 for n_o=(1,0,0) and r→1. This does not refute a physically selected
asymptotic family; no distance or X_max identification has been supplied.

## 5. SR/GR recovery is a scoped physical correspondence requirement

A smooth Lorentz metric admits a local orthonormal frame and normal coordinates
with g=η, ∂g=0 at a regular event. With W4/ordinary clocks this supplies the
local SR form, including its sole local null cone and c_E calibration. It does
not impose GR's field equation, eliminate finite curvature, select an observer
population or establish solar-system precision.

A useful SUFFICIENT mathematical continuity route, if a family is supplied,
is C2 convergence g_ε→g_GR on a common compact regular ray tube with uniformly
nondegenerate signature, C1 convergence of endpoint curves and regular stable
transverse ray incidence. Geodesic/transport ODE continuous dependence and the
implicit incidence map then give Z_ε→Z_GR. Such uniform hypotheses also control
curvature observables. This route is not a necessary tensor-norm definition of
empirical correspondence; actual observational tolerances and protocol coverage
must be specified, and coordinate/gauge identification is needed before norms.
The work order supplies neither a selected perturbation nor observational bounds.

An exact comparison statement is simpler: if g, full endpoint curves, branch
and calibration agree with a GR control on the whole causal query, the clock
answer agrees. To differ while retaining the same functional, some relevant
input must differ. Equality merely at one endpoint or one finite jet does not
fix distant finite-path comparisons (FCV1 already retains that distinction).

If two metrics at a point have exactly the same null cone, the null-quadratic
lemma makes them conformally related. If, in addition, their proper-time
quadratic forms agree on every timelike tangent, they are equal by polarization.
These are fully quantified exact rigidity statements, not consequences of a
finite set of successful GR tests. Extra finite effects are not ruled out by
limited or approximate correspondence.

## 6. First unsupported join and strongest return

One geometry gives real consistency conditions: finite frequency transport,
directional angular form, path/event composition, stationary-sector obstruction,
regular local limit, and directional conditions on any claimed asymptote.
These are mathematically useful without becoming a selector for actual metric
histories. Complete reciprocal normalization must retain its clock calibration
and density; chi_clock and the full projective norm remain differently typed.

The first unsupported join is assigning a physically realized family of
geometries and event/observer/ray data to the intended additional positional
effect, with correspondence and boundary targets, from the current admitted
UDT relations. Identifying DDR's unknown E[g] with a chosen tide, Ricci tensor,
single-query variation or expansion scalar would not follow from these
identities. Neither local response dynamics nor a new postulate is proved
necessary for every possible successful route. Ordinary initial/measurement
data are legitimate; lack of an intrinsic scale is not a ban on them.

This is not a proof of general UDT underdetermination. Supplied-metric controls
only test the geometric implication whose hypotheses they satisfy. They are
not alternative native UDT worlds. All statements here stay conditional and
source-graded. Await direct candidate review.

## Read/check failure history

An initial source lookup tried the nonexistent paths
`udt_clock_curvature_derivation_2026-09-28/INITIAL_CANDIDATE.md` and
`udt_positional_geometry_clock_connection_2026-09-28/REVIEWED_RESULT.md`.
The shell reported those lookup errors; `rg --files` then identified the actual
`INITIAL_DERIVATION.md` and `CANDIDATE.md`. This was a file-discovery failure,
not scientific evidence. No source, candidate or check was overwritten.
