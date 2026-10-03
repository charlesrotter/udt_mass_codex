# CBR1 mathematical source-first review

Reviewer: `/root/cbr_math`, fresh separate context, inherited model. Parent startup
is attributed to the dispatch and BASELINE; this context independently observed
branch grok, HEAD770c392465fac5e444f21bd2f7adabfaf5aabdb4 and no tracked diff before
its writes. No top-level resync was repeated. Parent process/freshness/full406
claims are attributed, not independently recertified here. Only this package's
`math/` is owned. Protected payloads were not opened, hashed, used or changed.

Exposure before seal: AGENTS, specified CLAUDE sections and triggered no-shortcuts,
completeness-map and verifier-before-record protocols; CBR1 WORK_ORDER/BASELINE;
CMF1 INITIAL_CANDIDATE/REPAIR/REVIEWED_RESULT; PSW1 INITIAL_CANDIDATE/REPAIR;
ERC1 REVIEWED_RESULT; existing capture utility. No new parent implementation or
smoke/main outcomes read. Methods and control classes were disclosed by dispatch.
This is source-first, not question/formula blindness or different-model review.

## Forward geometry, independently reconstructed

Use the supplied smooth positive a(t), g=-dt²+a²dx·dx. Put H=a'/a and use coordinate
four-vectors V=(Vt,Vx). The only Christoffels required are Γt_ij=a²Hδij and
Γi_tj=Γi_jt=Hδij. Along the spacelike preparation γ(s), s∈[0,L], integrate

    x'=V, Vt'=-a²H|Vx|², Vx'=-2H Vt Vx,
    Wt'=-a²H Vx·Wx, Wx'=-H(Vt Wx+Wt Vx),

with x(0)=o, V(0)=n, W(0)=U. Here n is a member of the supplied U-rest triad,
not an unboosted cosmic-time spatial axis. The transported W at s=L prepares
the receiver's future-unit free velocity. Its subsequent geodesic can be solved
directly in proper time or with conserved K=a²Wx and

    ut=sqrt(1+|K|²/a²), dx/dt=K/(a²ut), dτ/dt=1/ut.

An arbitrary initial boost makes preparation times differ from the emitter's
time. Substituting equal-coordinate-time receiver placement is a different
experiment. Norms g(V,V)=1, g(W,W)=-1, g(V,W)=0 and future orientation should be
checked across prep, together with free-clock normalization afterwards.

Spatial homogeneity/conformal flatness imply a straight spatial null direction.
For emitter event (te,xe) and receiver (tr,xr), the outgoing incidence equation is

    η(tr)-η(te)=|xr(tr)-xe(te)|, η'=1/a, N=(xr-xe)/|xr-xe|.

Keep the positive regular root, metric domain and transverse incidence. Along
the ray, with any positive conserved null momentum amplitude κ,

    ω=κ/a (ut-a N·ux),
    p=dτB/dτA=ωA/ωB
     =(ar/ae)(uAt-ae N·uAx)/(uBt-ar N·uBx).

These are actual clocks/ray data; neither R nor the trace equation is input.
An independently differentiated arrival map must vary emissions on the SAME
prepared A and B. Re-preparing B at each emission changes the derivative.
Fixed receivers or p=ar/ae for moving receivers also change the experiment.

The independently authored source_first_check.py integrates the full coordinate
prep, parallel transport and proper-time timelike geodesics with DOP853. The
null root uses analytic η for the supplied a=1+k t². A non-axis boost
(0.2,-0.3,0.25) tests all three boosted triad vectors at five L; separate nearby
emissions on fixed worldlines compare arrival derivatives to endpoint frequency.
Minkowski arbitrary-boost checks have p=1. A 70-digit independently evaluated
analytic comoving check at t=0 uses tb=tan(sqrt(k)L)/sqrt(k), p=1+k tb².
This supplements float64 computation, not an all-stage high-precision replay.
See saved JSON/capture for actual numbers, versions, settings and 21 primary
clock queries. Finite assertions are numerical diagnostics, not interval bounds.

## Reconstruction and principal traps

The sources' triad coefficient is c(U)=-2Σ_i log p_i/L². The seven-frame scalar
map follows directly from a symmetric bilinear Ricci tensor. At v²=1/3,
R=Σ_six c_i±-10c0. For homogeneous/isotropic controls, all six boosted c's agree
and transverse directions repeat, but reuse must be declared as symmetry reuse,
not independent observations or a noise-reduction count. The noisy coefficient
must be reconstructed from perturbed log records, without curvature passed into
the estimator. Exact symmetry cancellation in one family can hide a broken
general reconstruction, so the finite result is scoped to these supplied controls.

Scalar reconstruction at the nine events for Box requires their GEODESIC
placements exp_o(±h e_a). In FLRW, a spatial geodesic initially has
t''=-H and x''=-2Ht'x', and is generally not a constant-coordinate-time segment.
For homogeneous R, its second derivative initially is -H R', each of the three
spatial contributions supplying -H R'. Replacing spatial placements with t=t0
would produce -R'' instead of Box R=-R''-3H R'. Timelike comoving placement does
give t0±h. Parallel/frame/ruler calibration is independent information, not
reconstructed from R alone. The same center has Box weight -4; its noise cannot
be counted four independent times or reduced by averaging repeated copies.

Generic finite-separation error is O(L), not automatically even under n→-n.
Shrinking L at fixed absolute tick noise magnifies curvature error as L^-2;
Box further magnifies it as h^-2. Finite differences at very small h magnify
integrator/roundoff floors as well. Fit/extrapolation assumptions, point reuse,
training/held-out splits, tolerances and noise model belong in the pre-outcome
plan. A polynomial extrapolator is a numerical design with finite checks; it
does not replace independent remainder bounds or make joint limits automatic.

## Original tensor control

For independent supplied-metric checks, write A=a''/a, R=6(A+H²), P=R', Q=R''.
The original response contractions, with normalized spatial component E_s, are

    E00=3H²+α[-6RA+R²/2+6HP]-Λ,
    Es=-(2H'+3H²)+α[2R(A+2H²)-R²/2-2Q-4HP]+Λ.

Their trace is -E00+3Es=6α(-Q-3HP)-R+4Λ. Reconstruction of these from saved a
jets or separately differentiated a-data is stronger than comparing an ODE RHS
to itself. An ERC1 state-variable constraint check remains useful but is not
independent original-equation certification. The a=sqrt(1+2ht) control has
R=0 but E00=3H² for Λ=0, so it must remain a scalar false pass. A positive
equation-generated example tests recoverability only, not that physical law.

## Initial disposition

The forward/inverse interface is viable in this bounded supplied geometry class.
No source-first mathematical objection forces a change in premises. Main-code,
saved-output and final correspondence reviews remain outstanding. Numerical
recoverability, joint-scale behavior and noise claims must await actual frozen
results. No hardware, empirical applicability, generic4D or native selection
claim follows. Shared Python/SciPy infrastructure and same model are disclosed;
independent context, argument and authored implementation are separate axes.
