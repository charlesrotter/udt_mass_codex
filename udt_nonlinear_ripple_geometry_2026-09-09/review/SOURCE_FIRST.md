# Sealed source-first reconstruction — UNPROMOTED

Reviewer `/root/nrgeom_review`, separate context, 2026-09-09. Baseline personally
checked: grok b64700a6954b1fc3e7b1d80b9d30c4833a7ff7ea. Exact model UNKNOWN;
different-model and different-library independence are not established.

This note and the three named source-first scripts were constructed without
reading the new author candidate, code or outputs. The parent supplied the
question, old controlling sources, and the suggestion to examine a polarized
Gowdy method. The parent disclosed prior hand exploration of the areal/Bessel/
constraint-response route and reading Jurke before this review. Consequently
this is source-first reconstruction with route exposure, not hypothesis-blind
discovery, not evidence that the parent's reasoning was independently frozen,
and not a different-model review. No scientific finding was messaged to the
parent before sealing. Only readiness, names and hashes may be sent until
the author confirms its initial candidate is frozen.

## Sources, scope and premise audit

I read AGENTS and the bounded startup documents in order, the actual triggered
shared no-shortcuts, completeness-map, verifier-before-record, solver-first
and solution-space protocols, and CROSS_MODEL_VERIFY. I read both G310/G312
adoption records, G303/G315 exact derivations and full reports, G327 exact
derivation and full report, and SE1's entire candidate, provenance correction,
direct review and provenance followup. Their source pins are recorded separately.

The personally executed full365 audit exited 1 at G325's
`replay_exact:DERIVATION_RESULT.json`; later gates were not passed. The parent
preserves a separate startup capture. This failure blocks promotion, not this
authorized UNPROMOTED bounded reconstruction. No accepted scientific file,
registry, protected payload, canon or tracking file was changed by this review.

The equation is the OWNER-PROVISIONAL bounded metric-only vacuum arena,
Ric(g)=Lambda g, specialized to the existing Lambda=0 data. G303/G315's
smooth local development/uniqueness method remains conditional mathematics.
The exact construction below proves an actual development directly; no NR2
existence or tangent assertion is needed as a logical input. SE1 is reviewed
UNPROMOTED source data. No imported source, action, physical energy, light,
stability, arbitrary-data theorem, selected slicing or scale is asserted.

Supplied split translation T3, x period 2*pi, arbitrary positive transverse
periods, initial unit metric, plus-polarized cosine and amplitude e are
free-and-explored data/comparison choices. For the SE1 witness e=1/6. The
formulas happen to work for each finite real e; this does not classify all data.
The background and sign are pinned by the cited G327/G315 conventions. The
positive areal coordinate t excludes t=0 and imposes no endpoint condition.

## Independent construction and full-equation check

Put b=3/4 and, for t>0, use

    g = exp(L/2)t^(-1/2)(-b^2 dt^2+dx^2)
        +t(exp(P)dy^2+exp(-P)dz^2).                 (SF1)

Direct coordinate differentiation of this four-metric, without inserting a
reduced field equation in the Ricci constructor, gives full Ricci zero when

    P_tt + P_t/t - b^2 P_xx = 0,
    L_t=t(P_t^2+b^2 P_x^2), L_x=2tP_tP_x.          (SF2)

All sixteen original components are formed; their off-shell expressions and
on-shell zeros are saved. This also independently verifies the method relation
to Jurke's equations after changing the base coordinate to b*t. Jurke is a
mathematical method reference, not an adopted physical equation or authority
for a completeness conclusion here.

Let f solve f''+f'/t+b^2 f=0 with f(1)=0, f'(1)=3/2. Explicitly,

    f(t)=(3*pi/4)[J0(b)Y0(bt)-Y0(b)J0(bt)].         (SF3)

The standard Bessel Wronskian fixes the derivative including its sign. Set

    P=e f(t)cos x,
    L=(e^2/2){t^2[f'^2+b^2 f^2]
              +t f f'[1+cos(2x)]-9/4}.            (SF4)

Differentiating (SF4) and using the ODE yields both equations for L in (SF2).
Its spatial period integral is zero exactly, so this is a globally periodic
function, with L(1,x)=0. There is no hidden monodromy or integration constant.

The positive lapse is N=(3/4)exp(L/4)t^(-1/4), future n=N^-1 partial_t,
and K=-L_n gamma/2. On t=1 the complete data, not only their first variation,
are

    gamma=I,
    K=diag(1/3-3e^2 cos^2(x)/4,-2/3-e cos x,-2/3+e cos x).

All six K entries including the zero off-diagonals match SE1. The Hamiltonian
and all momentum constraints vanish. Smooth periodic f,L,P at every finite
positive t give a Lorentzian exact solution on (0,infinity) times T3. Thus an
actual development of the full datum is exhibited, not merely formal jets.
On compact time intervals its coefficients are bounded and lapse positive.
The G315 conditional uniqueness theorem relates this to a Gaussian presentation
near the initial slice up to diffeomorphism; N is not 1 away from that slice.
Nothing here identifies a maximal development or proves geodesic completeness.

## Link to G327 and the nonuniform nonlinear limit

At e=0, let T=t^(3/4). Then SF1 is exactly

    -dT^2+T^(-2/3)dx^2+T^(4/3)(dy^2+dz^2).

L is quadratic in e. The first variation of the transverse block is
t f cos(x) diag(1,-1), so G327's h=f/2 for this parameterization. The ODE
transforms exactly to h_TT+h_T/T+T^(2/3)h=0. Its declared relative phase-space
norm decays as T^(-2/3)=t^(-1/2), using also the derivative Bessel asymptotics.
For nonzero e this T is a background comparison parameter; it is not proper
time of SF1. The exact polarization P itself also decays uniformly in x.

Write f=D t^(-1/2)cos(bt+delta)+O(t^(-3/2)), with

    D^2=(3*pi/2)[J0(3/4)^2+Y0(3/4)^2] > 0.

The corresponding derivative expansion gives
t^2(f'^2+b^2f^2)=b^2 D^2 t+O(1) and t f f'=O(1). Therefore, uniformly in x,

    L=c_e t+O(1),
    c_e=e^2*(27*pi/64)[J0(3/4)^2+Y0(3/4)^2] >0     (e !=0). (SF5)

The O(1) bounds follow from the usual fixed-order real large-positive-argument
Bessel expansions, not from sampled numbers. The Wronskian prevents J0 and
Y0 at 3/4 from both vanishing. This is an exact family whose second-order
metric response is O(e^2 t) while its first-order polarization decays. Taking
e to zero on compact time intervals and t to infinity at fixed nonzero e are
different limits. An endpoint-uniform nonlinear estimate cannot be inferred
from G327's first-order decay.

## Geometric comparisons and their precise markings

Fix the supplied transverse T2 orbits and periods. Their normalized area is
t; the actual area is t*L_y*L_z. Its gradient is timelike, so the future normal
to its level sets is geometrically defined given this action/marking. Define
Theta_A=n(log area). Directly from the inverse metric,

    Theta_A=(4/3)exp(-L/4)t^(-3/4),
    Theta_A/Theta_A_Taub=exp(-L/4) ->0              (same orbit area). (SF6)

Equivalently the ratio of squared norms of d log(area) is exp(-L/2). These
are geometric scalars for the supplied action and corresponding equal-area
events. A coordinate time change cannot remove this ratio. They are not
invariants of an unspecified choice of orbits in a completely unmarked metric.

On that same areal slice the axial quotient-circle length has Taub ratio
(2*pi)^-1 integral exp(L/4) dx. Uniform (SF5) sends this ratio to infinity,
although both transverse metric ratios exp(+-P) tend to 1. This circle length
is intrinsic to the quotient by the supplied orthogonal T2 action. A constant
rescaling of the markings cannot cancel its growing ratio.

The independent intrinsic spatial-Ricci construction gives

    R3=-(1/2)t^(1/2)exp(-L/2)P_x^2,
    R3/Theta_A^2=-(9/32)t^2 P_x^2.                (SF7)

Taub has R3=0 on these slices. Absolute R3 tends uniformly to zero here too;
that absolute limit alone would miss the distinction. At, for example, the
marked x=pi/2, the normalized scalar in SF7 is unbounded negative along
subsequences on which cos(bt+delta) is bounded away from zero. It is not a
pointwise monotone divergence: the exact f has recurring zeros, at which
this diagnostic vanishes. This slice curvature diagnostic is not a claim
about physical instability or a complete spacetime invariant classification.

Full spacetime Ricci and scalar curvature are zero for both solutions and
therefore do not distinguish their remaining geometry. No full-Weyl invariant
or frame-curvature late-time assertion is needed for SF6–SF7; none is being
passed here merely from scalar Ricci zero. A future direct review may demand
an additional full Riemann calculation if the author's claim makes it load-bearing.

## Computation evidence, adverse checks and omissions

source_first_tensor.py is a new, implementation-distinct coordinate tensor
calculation using SymPy 1.13.1, Python 3.10.12. Its first run passed in 1.31 s,
max RSS 53052 KiB. It independently differentiates the full 4D metric and
the induced 3D metric, verifies exact initial data, constraint primitives,
periodicity, and the G327 change of time. No author code/formulas were imported.

source_first_bessel.py uses mpmath 1.3.0, 50 decimal digits. Direct quadrature
of the nonnegative L_t at three times and three points agrees with SF4 with
max error 6.69e-52. Its first run passed in 4.45 s, max RSS 15936 KiB.
At e=1/6 it gives c_e=0.0281908023272879221702749597368. These are finite
floating-point consistency checks, not interval certification or asymptotic
proof. The written expansion argument supplies the infinite-time conclusion.

An actual in-memory deletion of the L_t response in source_first_mutation.py
was rejected by the original_Ricci assertion, exit 1 in 0.82 s, max RSS
61916 KiB. The corresponding nonzero symbolic matrix is preserved in stderr.
This is a matching failure, not a timeout or dependency error. The unmutated
tensor also gives R_tt=-1/32 at a stated nontrivial initial-rate probe if L
is held identically zero. Frozen files were not modified to run this control.

Each mathematical check ran through the pre-existing run_capture.py wrapper
with one library thread, 512 MiB address-space and 60-second CPU/wall limits.
Captured argv, stdout/stderr, timestamps, resource records and hashes are
preserved. Timestamps and hashes establish recorded versions and correspondence;
they do not independently date unsaved hand reasoning.

Not replayed: all upstream package code, G327's entire eight-constant census,
general Cauchy/CK theorems, NR2, PDE integration, arbitrary perturbations,
geodesic completeness, all-isometry comparisons, physical identification,
observations, specialist-human or formal-proof review. The source-first verdict
is feasibility and exact bounded reconstruction, pending direct review of
the frozen author candidate. No scientific promotion follows.

Primary mathematical references actually consulted:
[Jurke, equations (1)–(5)](https://arxiv.org/pdf/gr-qc/0210022),
[NIST DLMF 10.17](https://dlmf.nist.gov/10.17), and
[NIST DLMF 10.5](https://dlmf.nist.gov/10.5).
