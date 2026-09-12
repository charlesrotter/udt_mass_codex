# NTB1 source-first reconstruction

2026-09-12. Reviewer context `/root/ntb1_beam_review`, fresh separate context.
Runtime model/version UNATTESTED; different-model axis UNTESTED. Parent startup
is attributed: synchronized grok at f5c6696ada572ae93e17914233badbbceaae97ff,
original 46 untracked payloads preserved; full398 audit was RUNNING at dispatch.
Reviewer independently checked current HEAD, origin/grok and status, without
switching/synchronizing. No protected payload read, no subdelegation.

Before this seal I read only dispatch, WORK_ORDER, SOURCE_PINS, AGENTS, relevant
CLAUDE sections, no-shortcuts/completeness-map/verifier-before-record protocols,
the explicitly named G394/G415/G348/NCR1 scientific sources, and the existing
capture utility plus underlying runner. Parent disclosed its intended reduced
Hamiltonian variational route, but no new candidate/code/outcomes were read.
Methods below are my independent source-first reconstruction, with that method
exposure acknowledged. Source formulas and general Jacobi theorem are reused.

## Admitted scope and source fidelity

G394 supplies the ENTIRE positive-time compact polarized metric, exact Bessel F
and full exponential lambda response. G415 supplies axial positive two-screen
quadratures and axial nonconjugacy only. G348 supplies quotient Jacobi geometry,
observer covariance and same-segment reversal. NCR1 is prior reviewed conditional
UNPROMOTED clock work, not an accepted dependency or focusing result. Current G312
GR FILTER ONLY controls inherited ownership wording. Physical observer/path
selection, native response membership and full pair-kernel assembly stay OPEN.

At t=1 choose unit local source frequency and unit sky in the areal frame. Same
marked reception t permits different receiver labels. Areal observers, polarization,
marking and compact lifts are supplied/pinned-by-HABIT, not a preferred physical
frame. Amplitude, phase and sky are free-and-explored. The metric is pinned to
G394, not selected by this review. CPU numerical tolerances are method controls.

## Original-geodesic finite-angle variation route

Write the diagonal metric as g_aa=s_a exp(2q_a), s=(-1,1,1,1),
q=(a,a,(log t+P)/2,(log t-P)/2), and d_b q_a=0 for b=y,z.
Direct Christoffels are

    Gamma^a_bc = delta_ab q_a,c + delta_ac q_a,b
                 - delta_bc (g_bb/g_aa) q_b,a.

For t-parameter curves w=(1,v), the ORIGINAL full geodesic equations are

    x_i'=v_i,
    v_i'=-Gamma^i_ab w^a w^b + v_i Gamma^0_ab w^a w^b,
    (log omega)'=a_t+a_xi v_xi-Gamma^0_ab w^a w^b.

The last equation follows from omega=N k^t and d log k^t/dt=-Gamma^0 ww;
it provides a clock check without reduced Hamiltonian evolution. Start
v=(s_xi,N_e s_y,N_e s_z), N_e=3/4, source omega=1. Vary source sky on
great circles s(h)=cos(h)s+sin(h)e_A with orthonormal tangent e_A.
Centered differences of endpoints at equal t give the exact Jacobi derivative
in the h->0 limit; finite h is ONLY a numerical approximation with refinement.
An affine-endpoint connecting field differs by a multiple of k, so its quotient
class is unchanged by the fixed-t endpoint convention. Differentiating nullness
and the common source event gives k.J=0; hence at fixed t the metric-weighted
spatial endpoint derivative is perpendicular to the reception sky.

Use the fixed-t screen Gram matrix G_AB=sum_i exp(2q_i) dx_i/dtheta_A
dx_i/dtheta_B, with independent check of its reception-ray orthogonality.
sqrt(det G) is positive area and singular values detect rank. A signed determinant
requires an explicitly continuous oriented reception frame. Sampling det G>0
cannot prove absence of rank loss between samples; det G also discards sign.

## Exact invariant transverse-ray diagnostic

At xi=0 (also the other cosine extrema), take a pure y ray. Reflection symmetry
keeps xi=0 and z fixed, with y'=N/b_y. The xi and z sky variations decouple.
Let X=partial xi/partial theta_xi, q_y=log b_y and r=a-q_y. Direct linearization
of the above original geodesic equations gives

    X''+r_t X'+r_xixi X=0, X(1)=0, X'(1)=1,
    r_t=-3/(4t)+epsilon^2 t F'^2/4-epsilon F'/2,
    r_xixi=(k^2 epsilon F/2)(1-epsilon t F').

The physical xi separation is N X. The other screen mode is

    D_z=b_z(t) integral_1^t N/(b_y b_z^2) du > 0.

This follows from conserved p_z and source b_z(1)=1. Therefore a nonvertex
zero/sign crossing of X is precisely a rank-one conjugate endpoint on this
invariant family. At epsilon=0, r_xixi=0 and X is an increasing positive
quadrature. At nonzero epsilon r_xixi changes sign; positivity of the axial
quadratures does not extend by the same argument. No focusing/nonfocusing
outcome is presumed before execution.

## Frozen source-first numerical contract

One CPU science process per reviewer; float64/scipy solve_ivp DOP853, ordinary
capture <=180s and <=2048MiB, library thread environment all one. First diagnostic:
the scalar invariant equation above for effective amplitudes +/-1/6,+/-.5,+/-1,
+/-2, t in [1,80], max_step=.05, rtol=2e-10, atol=2e-12, save every .1 plus
every located sign crossing. This finite grid is not a universal search or an
infinite-time result. Any crossing candidate will receive a predeclared tighter
repeat (rtol=2e-12, atol=2e-14, max_step=.025), full-original-geodesic angular
finite differences at h=1e-3,5e-4,2.5e-4, and saved brackets/signs. Agreement
criterion: root times within 2e-6, normalized derivative differences <=2e-5,
nullness/frequency consistency <=2e-8. Numerical sign brackets are floating-point
support, not interval certification. If no crossing appears, report only the
finite diagnostic. General finite-sky cross-check cases will be frozen before
execution after candidate exposure, recording that exposure separately.

Maximum conclusion: exact conditional beam evaluator plus a bounded independently
checked extension/counterexample/diagnostic. No new physics, observational light
law, physical finite beam, universal no-conjugacy, all-time area asymptotic or
promotion follows. Algebraic derivation owns exact claims; finite differences
and tolerance repeats support implementation only.
