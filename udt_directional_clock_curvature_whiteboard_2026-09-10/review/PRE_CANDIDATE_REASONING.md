# Reviewer reasoning before candidate exposure

Reviewer `/root/clock_kernel_adversarial_review`; fresh separate context, inherited model;
exact runtime model/version UNATTESTED. Opened WORK_ORDER and DATA_FREEZE first, then
AGENTS, required CLAUDE sections and the three assigned review protocols. Candidate text,
author implementation, whiteboard implementation and their result files NOT yet opened.
The candidate hash was checked without opening its text: expected and observed
`b11326b4f316f675a9c3ecc596d47e33c0e39215c591fddde1013c37c68d2375`.
Independently observed HEAD `896da97dc2484b72fa346d0c0ab17055a1dd6fcd`.
Top-level startup, synchronization and premise-verifier pass are attributed to the parent;
I have not repeated or independently certified those runs. Start 2026-09-10 20:24:33 UTC.

## Independent data-map argument

For affine null k, omega=-g(U,k), metric compatibility and the geodesic equation give
`k(omega)=-k^a k^b nabla_a U_b`. Writing k=omega(U+n), normalization of U gives
`q(n)=-a.n-S(n,n)`, where S is the projected symmetric derivative of U.
Thus m=-theta/3; dipole is minus acceleration; the centered even part is minus
sigma(n,n). In three spatial dimensions the exact spherical fourth moment gives
`V=2 sigma_ab sigma^ab/15`. Antisymmetric vorticity is absent from this scalar contraction.

Commuting derivatives in div(a)=div(nabla_U U) should give
`Ric(U,U)=A-U(theta)-theta^2/3-sigma^2+W`, with the frozen sign convention.
Accordingly the proposed universal formula should be
`Ric(U,U)=A+W+3 dot(m)-3 m^2-(15/2)V`.
This is standard geometric Raychaudhuri, not an independent dynamics or novel identity.
I will test signs against coordinate curvature and independently use a frame calculation.

Independent motion data need not be statistically or physically independent: the positive
claim is a factorization through the declared map. A and W do depend on the underlying
metric/congruence; supplying the entire metric would make the inference trivial, but the
freeze instead supplies two scalar channels. Their operational acquisition remains open.
One may supply A+W instead; no unique minimal encoding follows from channel omission tests.

## Pre-exposure candidate attacks and comparison metrics

1. Missing dot(m): synchronous diagonal metrics with equal first time jets but different
second time jets should retain q,A,W and alter Ric(U,U).
2. Missing A: static lapse `g=-N(x)^2 dt^2+dx^2+dy^2+dz^2`, U=N^-1 d_t, at a critical
point of positive N gives q=0, dot(m)=0,W=0, but Ric(U,U)=Delta(N)/N. N=1+c x^2/2
should witness the omitted divergence. N=1 at the point matches normalization.
3. Missing W: a unit Killing congruence for
`g=-(dt+B)^2+dx^2+dy^2+dz^2`, with B=b x dy, is geodesic, expansion/shear-free,
and has identically zero depth along all affine null geodesics. Yet dB supplies vorticity
and nonzero Ric(U,U). Local coframe guarantees Lorentz signature independently of
coordinate minors. Derive curvature without Raychaudhuri to avoid a circular witness.
4. Missing even quadrupole: different tracefree spatial time jets should retain the
mean, its time derivative, and a=w=0, while changing Ric through shear norm.

Identical q at a point and dot(m) are far less data than equal finite path maps.
Even a unit Killing example with equal zero depth must not be advertised as equal null
incidence, flight times, pullbacks, distances, or complete operational records.

## Scope and planned checks

Review only the declared smooth local Lorentz metric/congruence class. Explicit witnesses
are targeted mathematical choices, free-and-explored in this class, not physical ansatzes.
No action, matter, field equation, physical light or instrument model, boundaries, numerical
grids, approximation, or GPU. Exact CPU algebra and geometry; each symbolic process has
timeout <=120 seconds. Review target 20 minutes from start, leaving authorized repair time.
No construction/whiteboard code will be imported into the independent check. This record
documents reasoning before text exposure, not blindness to the question or frozen proposal.
