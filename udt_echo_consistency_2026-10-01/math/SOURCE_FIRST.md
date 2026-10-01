# ECS1 separate-context source-first mathematical reconstruction

Status: frozen initial argument and check proposal, before seeing the ECS1
parent candidate or code; not a final integration attestation. Reviewer is
`/root/ecs_math`, a separate context using the inherited model, not a different
model, human reviewer, or formal prover. No subagents were used. This proof is
independently arranged after exposure to existing FPC1 formulas and their
embedding derivation; it is not a blind discovery claim.

Startup is attributed to the parent same top-level session, as AGENTS permits
for scoped reviews. I separately observed branch `grok`, HEAD
`187c5701f7ac5d0c591086c944f1a1568cf4bf12`, no tracked dirt at entry, and the
reported untracked paths plus ECS1. Parent supplied remote synchronization,
host-process and premise-audit evidence; I did not independently repeat those
checks here. I read AGENTS, the required CLAUDE sections and the triggered
no-shortcuts, completeness-map, verifier-before-record and
solution-space-not-imposition protocols. No protected payload was opened.
The source-byte pins are in SOURCE_PINS.sha256; method instructions are not
scientific premises.

## Question, choices and exposure

The work-order question is the first/direct-future-return record on the supplied
parallel-prepared geodesic-clock experiment. Initial proper separation L is
positive; clocks initially have velocities related by parallel transport along
that spacelike preparation segment. Neighboring emissions vary on those fixed
worldlines. Proper times have length units, c_E=1. The signed constant sectional
curvature K and transverse metric are free-and-explored comparisons, not selected
UDT histories. Ordinary Lorentz metric, Levi-Civita geodesics and affine null
correspondence are supplied interfaces. No field equation, physical source,
isotropy premise, preferred observer, boundary reflection, signal speed, scale
selection, microscopic light model or X_max identification is added.

I read FPC1 SPACEFORM_DERIVATION in full (including its quoted p/q, direct-branch
domains and ambient incidence proof), and relevant protocol/definition lines in
PSW1 INITIAL_CANDIDATE and FPC1 REVIEWED_RESULT. I had the proposed elimination
q=p/(2-p^2) in the dispatch. I did not read ECS1 parent argument/checks. After I
sent the reconstruction outline, parent said its route uses static Killing
energy/retarded time; I have not received its equations or proof. My construction
below instead derives a synchronous clock sheet and transports the null phase.
That source exposure limits independence, while the distinct context, argument
and implementation remain actual separate properties.

## Constructing the clock sheet

In a supplied 4D space form, the initial timelike velocity and preparation
direction span a totally geodesic Lorentzian two-surface. This can be seen
directly in the space-form quadric: intersect it with the linear ambient span
of the initial point and those two tangent vectors. Its normal acceleration is
also normal to the 4D quadric, so its intrinsic geodesics remain 4D geodesics.
The flat case uses an affine Lorentzian plane. This is a property of this
comparison and preparation, not an asserted reduction for arbitrary metrics.

Launch unit future geodesics orthogonally from the initial preparation geodesic,
using proper time tau along each and initial arclength x to label them. Gauss's
lemma gives h=-d tau^2+a(tau)^2 dx^2. The variation Jacobi field has initial norm
one and zero covariant derivative because the initial velocities were parallel
transported. With the FPC/PSW sign convention R_{0x0x}=-K in an orthonormal frame,
its scalar Jacobi equation is a''=K a, a(0)=1, a'(0)=0. Thus, on the regular sheet,

    K=+k^2: a(tau)=cosh(k tau),       tau in R;
    K=0:    a(tau)=1,                tau in R;
    K=-k^2: a(tau)=cos(k tau),        |k tau|<pi/2.

The clocks A and B are exactly x=0 and x=L, each with proper time tau. On the
initial slice, h_xx=1; the segment has length L and is a spacetime geodesic
because a'(0)=0. Parallel transport of U=partial_tau along it also holds because
Gamma^x_{x tau}=a'/a=0 there. Every x=constant curve is a unit timelike geodesic
because Gamma^mu_{tau tau}=0. These facts verify the preparation rather than
merely stipulating new coordinate-stationary observers.

## Incidence, affine rays and measured frequency

Define eta(0)=0 and d eta=d tau/a(tau). Then
h=A(eta)^2(-d eta^2+dx^2), where A=a composed with tau(eta):

    K=+k^2: A(eta)=sec(k eta),   |k eta|<pi/2;
    K=0:    A(eta)=1,           eta in R;
    K=-k^2: A(eta)=sech(k eta),  eta in R.

The direct future null branches have x-eta=constant (outgoing) and
x+eta=constant (returning). They are actual affine null geodesics after taking
k_a proportional to -d eta +/- dx: the one-form is exact and null, so
k^b nabla_b k_a=(1/2)partial_a(k^b k_b)=0. With proper-clock velocity
u=A^-1 partial_eta, the local measured frequency is omega=-k_a u^a=C/A,
C>0 fixed along each affine ray. Therefore the ratio of infinitesimal receiving
to emitting proper-time intervals is A_r/A_e=omega_e/omega_r. This agrees with
the derivative of the independently obtained incidence relation
eta_r=eta_e+L; no assumption of coordinate frequency constancy is used.

For emission at A's preparation event eta=0, first reception occurs at eta=L.
An immediate return reaches A at eta=2L if that conformal time is in the sheet.
Varying emission on the fixed worldlines keeps eta_r-eta_e=L. Hence

    p=A(L)/A(0),       q=A(2L)/A(L),       p q=A(2L)/A(0).

Here q is the return-leg clock-map derivative at the later relay. It is not the
separately emitted reverse first-leg derivative, which equals p by x reflection.
The full echo clock-map derivative is p q by the chain rule. Interpreting that
product as the inverse total photon frequency ratio additionally presumes a
frequency-preserving relay in its own proper frame; the clock-map statement
itself does not need a microscopic relay law.

## Every finite branch admitted in this comparison

For positive curvature put alpha=kL. The first future reception is finite for
0<alpha<pi/2 and has tau_b=asinh(tan alpha)/k and p=sec alpha. The echo is finite
only for 0<alpha<pi/4 and has tau_a=asinh(tan(2 alpha))/k,
q=cos alpha/cos(2 alpha). The latter arrival is equivalently
2 artanh(tan alpha)/k on that branch. At alpha=pi/4, the echo conformal endpoint
is the future edge and tau_a diverges; it is not a finite event. For
pi/4<=alpha<pi/2 the first leg remains finite but q is undefined for the specified
finite future echo. Extending its algebraic expression to a negative denominator
does not produce an allowed future return. At alpha=pi/2 the first reception
itself has no finite event. Beyond that direct local branch, winding/antipodal
or different global routes are not this experiment and are not classified here.

For zero curvature tau_b=L, tau_a=2L and p=q=1 at every finite L>0. For negative
curvature, every finite alpha=kL>0 gives

    tau_b=arcsin(tanh alpha)/k=arctan(sinh alpha)/k;
    tau_a=arcsin(tanh(2 alpha))/k=2 arctan(tanh alpha)/k;
    p=sech alpha,       q=cosh alpha/cosh(2 alpha).

Both receptions occur before tau=pi/(2k), so the synchronous caustic causes no
finite-L failure. L tending to infinity is not a finite separation and the
limiting caustic does not supply an extra admitted branch. Use the AdS cover and
the direct local null branch; no late winding or boundary return is inserted.
The zero-separation p=q=1 point is a continuous degenerate limit, not two distinct
clock events.

On all those finite echo branches, the double-angle identities give

    q = p/(2-p^2),             p q = p^2/(2-p^2).

Their union has 0<p<sqrt(2), with p=1 representing flat space at positive L,
0<p<1 the negative branch and 1<p<sqrt(2) the positive branch. Positive first
legs with sqrt(2)<=p<infinity have no finite immediate echo. In particular the
relation is not a universal function for every measured first leg. One exact
positive example cos(alpha)=4/5 gives p=5/4, q=20/7, p q=25/7; reciprocal q=1/p
and mistaking p q for q both fail. Negative cosh(alpha)=5/4 gives p=4/5,
q=10/17, p q=8/17. These are finite regular interior examples.

## Exact 4D nonuniqueness witness and its quantifier

For any one of the clock sheets above and any fixed mu>0, form

    g_tilde = h_K + dy^2 + exp(2 mu y) dz^2.

This is a smooth Lorentzian metric wherever h_K is regular. The y,z surface has
constant Gaussian curvature -mu^2. Product connections split. Thus y=z=0 is a
totally geodesic copy of h_K, and every preparation geodesic, clock, affine ray,
proper-time label, parallel-transport preparation, local endpoint frequency,
and direct incidence event just constructed is identical in g_tilde. It is not
just a match of the two numbers p and q: the entire clock/null record on that
sheet, with all emissions staying in its regular domain, is preserved exactly.

Nevertheless a mixed tangent two-plane has sectional curvature zero, and the
transverse spacelike plane has sectional curvature -mu^2. This cannot be a
4D space form for any K, including K=0. It is not merely a coordinate rewrite.
Its scalar curvature is 2K-2mu^2, compared with 12K for the original4D space form;
the sectional argument remains decisive even if those scalar values happen to
coincide for a chosen negative K. Restricting to any open regular neighborhood
of the finite experiment gives a sufficient smooth local witness; no global
completion claim is required.

Consequently the measured record of this pair/direction does not determine the
full4D metric or prove it is a space form. One witness suffices to refute that
uniqueness claim. It does not refute an all-observer/all-direction theorem and
does not classify all metrics with the relation. The preferred product splitting
of this comparison is not adopted as a universal physical direction. No claim
is made that this witness satisfies a chosen Einstein/Ricci-response, source,
action or native-admission sector. A sector-specific uniqueness statement would
need its own premises and argument. Matching a finite record supplies no missing
physical selection law.

## Frozen computation proposal and evidence limits

One serial SymPy run, CPU only, 2GiB virtual address cap through the existing TPS1
capture utility, no elapsed/CPU timeout. No grids, downloads, installs, solver
or observational fit. Outputs stay under math/ and are tiny compared with ECS1's
64MiB ceiling. The script checks the product metric's original Christoffels,
curvature and affine null transport with generic a(tau); then checks each exact
curvature sign and frequency/ratio expression. It includes explicit bad-q
counterexamples. This is finite exact symbolic regression supporting the stated
analytic proof, not numerical certification or independence from all source
formula exposure. All outcomes, including failures, are retained. No FPC/PSW
whole-package replay or full406 audit is repeated by this reviewer.

Source/code hashes and a pre-run UTC receipt freeze this argument before the
parent candidate is opened. A later source comparison and final edition-bound
attestation remain required. Parent granted the scientific CPU slot for exactly
one finite initial run after that freeze.
