# LG2 source-first adversarial assessment

Recorded 2026-09-09 at approximately 17:39 UTC, before any LG2 candidate,
author proof, code, checks, outputs, or freeze manifest exposure. Reviewer
`/root/lg2_review`, actual fresh separate context; exact model UNKNOWN and
different-model independence UNTESTED. The parent supplied the research
question and identified the proposed literature method before review. This is
therefore source-first independent assessment, not blindness to the method.

Scope: second/final authorized campaign step; review writes only here; at most
90 minutes including one focused same-premise repair/re-review, subject to the
campaign deadline 21:19:47 UTC. Small CPU checks, one at a time, one library
thread, 512 MiB and 60 seconds through unchanged run_capture.py. No numerical
PDE solve, GPU, protected payload, source replay repair, banking or root edit.

## Orientation and admitted dependencies

Verified branch grok and HEAD
78c3092b2120a80c8bbabb8024b4448d27c36a00. Inspected status without reading
protected payloads. Read AGENTS and the exact bounded startup chain, then
triggered no-shortcuts, completeness-map, solution-space-not-imposition,
verifier-before-record, and solver-first protocols. Parent owns shared git
sync and full365: its separately inspected capture records return 1 after
11.157 seconds, G325 replay_exact:DERIVATION_RESULT.json. This remains
NOT_PASSED; downstream full365 gates are unreached. I did not rerun or repair
full365. The parent reports successful fetch with the same origin/grok hash;
this reviewer did not independently contact origin.

G310/G312 adoption records supply owner-provisional premises, not derivation or
canon. G303/G315 admit Ric=Lambda g, one connected constant, and the complete
smooth initial constraints H=R+tau^2-|K|^2=2Lambda and M=div K-d tau=0, with
K=-L_n gamma/2. Smooth local development remains conditional on the imported
ordinary hyperbolic methods and hypotheses; it is not analytic-only here.
G324's exact proper-time Kasner metric has p=(-1/3,2/3,2/3). On T=T0 after
constant spatial chart rescaling, gamma0=I and K0=diag(1,-2,-2)/(3T0).
Fixed exterior on an open set forces this comparison's Lambda=0.

I read G303/G315 audit and exact-derivation sources, G324 audit and exact
derivation, and the permitted reviewed-unpromoted LG1 candidate and complete
direct review. LG1 supplies exactly four LOCAL KIDs on a connected annulus:
three translations and y d_z-z d_y, all with zero lapse. Its necessary balances
are not sufficient gluing criteria. No NR1/NR2 proof or protected work was read.

## Primary method and source pin

Chrusciel--Delay, gr-qc/0301073v2, downloaded from
https://arxiv.org/pdf/gr-qc/0301073; PDF SHA256
953f003fe179d5f686284b5755fcd4df381d3bbd3e9897bc11605650f3832dbb.
The PDF displays v2, 11 Jul 2003, and has 87 pages. Source locations: equation
(2.1), Proposition 3.3, Theorems 3.6 and 3.9, equations (3.13)-(3.14), Theorem
5.9 and (5.10)-(5.11), Proposition 5.10 and Corollary 5.11, Appendix A (A.1),
Appendix B's exponential-weight scaling discussion, and the symmetry/uniqueness
application in section 8.9. Printed pages differ by one from zero-indexed PDF
pages. The downloaded text extraction is retained as an inspection aid.

Method summary: these results give a local inverse for the nonlinear constraint
map after projection off a FIXED REFERENCE adjoint kernel; the orthogonality
inner product may use the nearby metric. Inverse bounds are uniform over a
sufficiently small neighborhood in stated finite-order weighted norms. Compact
smooth boundaries with a smooth positive defining function admit exponential
weights. The regularity result permits smooth zero extension of the correction
across the boundary. It does not alone remove the finite-dimensional residual.
I do not use the absence-of-KIDs or connected-sum gluing theorem.

The printed section 5 uses growing weights for decaying output norms but a
decaying exponential in its correction formula. When connecting to section 3,
the adjoint variational weight must be distinguished from the output norm:
take w=e^(-s/x) in psi^2 Phi^2 P*, while output norms involve e^(s/x).
Calling all of these weights the same positive-exponent psi would be an
incorrect literal substitution in (3.13). This convention needs explicit
attention in direct review; the invariant-kernel argument is weight independent
once its inner product is well defined.

## Independent applicability argument to test against the candidate

Choose a fixed embedded Euclidean annulus with radii 0<r1<r2 below the quotient
injectivity scale. Its two spherical boundaries are smooth. Choose an invariant
positive defining function x, proportional to (r-r1)(r2-r) near its two ends,
and a fixed radial smooth cutoff whose derivatives vanish near both ends.
All these are supplied method controls, not theory-selected boundaries or
scales. A boundary defining function can be rescaled small as needed for the
local weighted coordinate covers; it does not change the matching domain.

For smooth constant diagonal interior Kasner data near the reference, blend
both tensors with the background. The seed is reflection invariant and is
exactly lawful in neighborhoods of both boundaries. Therefore its complete
constraint defect has compact support inside the annulus. Every required
weighted finite-order norm of that defect is O(parameter distance) for this
FIXED cutoff/annulus; arbitrary data small only in C0 would not suffice.
Flat gamma0 and constant K0 satisfy (5.10), and smooth boundary geometry makes
x Hess(x) tend to zero. Smooth coefficients meet the stated regularity and
scaling hypotheses. Initial positive definiteness survives sufficiently small
corrections in the actual C0-controlling norm.

Let F be the group generated by the three coordinate reflections. It acts on
the four LG1 modes by characters. In ordered basis (d_x,d_y,d_z,y d_z-z d_y),
the generator matrices are respectively

    diag(-1, 1, 1, 1),
    diag( 1,-1, 1,-1),
    diag( 1, 1,-1,-1).

Their common invariant subspace is zero. CENTRAL INVERSION ALONE DOES NOT
WORK: it fixes the transverse rotation. This is a meaningful false-sufficiency
control for any parity-only shortcut. The full constraint operator and its
metric formal adjoint are natural under these reflections, including orientation
reversals: these constraint equations use no orientation-sensitive volume form.
The invariant seed metric, radial weights, and invariant reference-kernel
subspace make the orthogonal projection equivariant. An invariant uniqueness
neighborhood can be obtained by intersecting its eight translates.

The locally unique small inverse solution in the prescribed adjoint-image
slice must consequently be F-invariant: applying any group element gives
another solution in the same slice/neighborhood. Thus the corrected constraint
residual is invariant. The projected equation places its weighted version in
the reference kernel, whose invariant part is zero. Therefore ALL constraints
vanish exactly, not just their projection. This argument does not assert that
the perturbed data retain the reference KIDs. Averaging tensor solutions after
solving the nonlinear equation would be invalid; symmetry follows from
equivariance and uniqueness before removing the residual.

Corollary 5.11 is needed for ONE smooth correction extended by zero across BOTH
boundaries, not a sequence of unrelated Ck solutions with shrinking parameter
intervals. The data can be patched back into the same compact slice. No neck,
topology surgery, actual material boundary, source or external compensation is
introduced. G303/G315 then provide the conditional actual local smooth vacuum
development. Exterior agreement propagates only where justified by local
uniqueness and the common domain of dependence, not for all subsequent time.

## Independent nontrivial family and adversarial targets

One convenient independent parametrization of the interior data is

    p(q)=(-q,1+q,q(1+q))/(1+q+q^2), q near 1;
    gamma_in=I, K_in=-diag(p(q))/T0.

Both sum p and sum p^2 are exactly one. For q!=1 close to 1 the three Kasner
electric-Weyl eigenvalues p_i(1-p_i)/T0^2 are distinct, whereas the background
has a repeated pair. Magnetic Weyl vanishes in this Kasner patch. The complex
Weyl-operator discriminant therefore distinguishes the interior geometry from
every patch of the Taub background invariantly, including a changed slicing.
Merely changing K's eigenvalues or a time-dependent curvature value would not
alone exclude gauge. This is a possible independent check, not exposure to the
parent's chosen parametrization or proposed invariant.

Spatial homogeneity inside the prescribed ball is allowed; the global
completion must be localized in three dimensions, with all components and
constraints available in its annulus. Bounded support in the embedded ball
plus an interior invariant differing from the exterior prevents a nonzero
translation-invariant continuation of that invariant on the chart. This does
not claim generic absence of every possible local/global isometry.

The sharp candidate quantifier to inspect is: for each fixed T0, annulus and
chosen smooth cutoff there exists some delta>0, so that every parameter in a
small open interval has an exact smooth completion, nontrivial off the central
reference value. No computed lower bound for delta, uniformity over shrinking
annuli/T0/all C-infinity seminorms, arbitrary interior prescription, uniqueness
of all completions, numerical certification, stability, physical content,
population, scale selection, or UDT-derived matching symmetry follows.

Direct-review targets: sign/interface of J=-2M and rho=H; actual fixed-kernel
space and weights; source support on both boundaries; symmetry of projection
and the inverse; surviving rotation under weak parity; exact versus projected
residual; metric positivity; gauge-independent Weyl test; sufficiently-small
quantifiers and conditional smooth local developments. Passing finite algebra
will not be counted as proving the functional-analytic inverse theorem.

Preliminary source-first disposition: the method appears applicable to this
restricted family with the full reflection group, subject to explicit direct
proof checks above. No candidate verdict has yet been issued.
