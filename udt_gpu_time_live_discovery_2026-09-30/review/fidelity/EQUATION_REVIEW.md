# NGD1 independent fidelity review: equation gate

Verdict: **VERIFIED-WITH-CAVEATS** for the exact conditional two-Killing
Ricci reduction and the stated longitudinal clock query. No equation defect
was found. This gate does not verify the numerical evolution or its outcomes,
and does not establish native UDT dynamics, source selection, stability or canon.

## Context, authority and exposure

Reviewer `/root/ngd1_equations`, 2026-09-30. Actual separate scoped context;
parent-inherited model, exact identifier not exposed here. Different-model
review is UNTESTED. Parent startup synchronization and premise checks are
attributed to its report, not independently claimed. The reviewer independently
verified branch `grok`, HEAD `5b4aa5456b307f2be94ccdeadf9dfd7bc6677d28`, and
dirty status. Unrelated/protected untracked work was neither opened nor changed.
All reviewer writes are inside this `review/fidelity` directory.

Read AGENTS.md, specified CLAUDE sections, triggered no-shortcuts,
completeness-map/verifier-before-record protocols, CROSS_MODEL_VERIFY.md and
development MAINTENANCE.md. Scientific exposure before computation: parent's
expected metric/equations, NGD1 PLAN/SOURCE_PINS, central R9/R10/R12, current
G312 authority, NE1 original and reviewed scope, and FSL1 clock law/repair.
This is not a blind review. No author solver code, numerical output or prior
NGD1 equation-check implementation was used. The source pins all matched at
the equation-check run. Source documents' historical stronger-GR language is
qualified by current G312 GR FILTER ONLY authority.

Method: independently implemented exact algebraic two-jets of the original
four-metric, its inverse, Christoffel connection and all original Ricci entries.
SymPy 1.13.1/Python 3.10.12; no author code imports. This gives an independent
implementation and direct argument, not different-library/formal-proof evidence.
Duplicate/structurally zero entries are coverage, not sixteen independent proofs.

## Exact reduction

Let `a=lambda/4-log(t)/4`, `A=exp(2a)=N^2`, `E=exp(P)`, and

    g = A(-dt^2+dx^2)+t[E(dy+Q dz)^2+E^(-1)dz^2].

Hypotheses: t>0, finite real sufficiently smooth P,Q,lambda, signature -+++,
two supplied commuting spacelike Killing coordinates, and the supplied regular
chart. For the C2 local identities the coordinate jets commute; propagation
uses the additional differentiability needed for the differentiated equations.
The determinant is `-A^2 t^2`; the orbit block is positive definite, determinant
`t^2`. Consequently the marked orbit area remains t for nonzero Q too.

Define the actual equation residuals

    EP = Ptt+Pt/t-Pxx-E^2(Qt^2-Qx^2),
    EQ = Qtt+Qt/t-Qxx+2(Pt Qt-Px Qx).

Direct metric reconstruction returns

    Rtt = -att+axx+at/t+1/(2t^2)-(Pt^2+E^2 Qt^2)/2,
    Rtx = ax/t-(Pt Px+E^2 Qt Qx)/2,
    Rxx = att-axx+at/t-(Px^2+E^2 Qx^2)/2,
    Ryy = t E EP/(2A),
    Ryz = t E(Q EP+EQ)/(2A),
    Rzz = t E[(Q^2-E^(-2))EP+2Q EQ]/(2A).

Other entries vanish or are symmetry duplicates. Because t,E,A are positive,
Ryy=Ryz=0 force EP=EQ=0. Rtt+Rxx=0 and Rtx=0 then force, respectively,

    lambda_t = H = t[Pt^2+Px^2+E^2(Qt^2+Qx^2)],
    lambda_x = M = 2t[Pt Px+E^2 Qt Qx].

Conversely these equations and their compatible derivatives annihilate every
original Ricci entry. No extra off-sector Ricci equation was discarded. With
the evolution equations imposed, independent differentiation gives

    H_x-M_t = 0,
    H_t-M_x = -(Pt^2-Px^2+E^2(Qt^2-Qx^2)).

These supply the needed lambda second derivatives. The formulas are exact in
this supplied ansatz; its symmetry/twist restrictions do not cover all metrics
having merely two Killing vectors, let alone all four-dimensional spacetimes.

## Global constraint and numerical implication

On a supplied periodic x-circle of length L, a single-valued periodic lambda
exists only if `integral_0^L M dx=0` initially. This condition is sufficient
for integrating its spatial constraint, up to the supplied additive constant.
The equations preserve it because `d/dt integral M dx=integral H_x dx=0`.
When lambda is evolved by lambda_t=H, the defect `lambda_x-M` is time independent
analytically. Numerical checks must measure this constraint, including its mean.
Silently deleting a nonzero zero-mode in a Fourier inverse derivative would
change invalid data instead of solving the constraint. A local Ricci reduction
alone does not certify periodic global data.

For an independent original-equation numerical check, obtain time derivatives
from saved histories or another independently controlled method. Reusing the
same right-hand side to define Ptt/Qtt and to check EP/EQ is an algebraic
substitution check; it cannot detect time-integrator error. Reconstructing
lambda spatially after every step can likewise hide its evolution defect.
Both constraints, temporal equation errors and original metric residuals need
their declared scaling and convergence controls.

## Longitudinal clocks

Use fixed-coordinate observers `u=N^(-1) partial_t`, same y,z, and a supplied
regular future +x null branch of fixed lift separation `x_o-x_e=d>0`.
These observers may accelerate when lambda_x is nonzero; they are not silently
replaced by freely falling observers. On this branch,

    t_o=t_e+d,
    k=C N^(-2)(1,1,0,0), C>0,
    omega=-g(u,k)=C/N,
    Z=d tau_o/d tau_e=omega_e/omega_o=N_o/N_e,
    log Z=(lambda_o-lambda_e)/4-log(t_o/t_e)/4.

The reviewer directly checked nullity and all four affine geodesic equations
for k. The same result follows by differentiating t_o=t_e+d and using the
proper-clock factors. On a circle choose a lift/winding; it cannot change
silently during a comparison. A finite pulse duration requires integrating
Z, rather than multiplying by an arbitrary single endpoint value. Q influences
this readout through the solved lambda, though it does not appear explicitly
in the longitudinal null slope. No physical protocol or distance-redshift
law is selected by this calculation.

## Independent checks and an additional exact anchor

`check_original_ricci.py` constructs metric/connection/Ricci from first
principles and compares to the displayed reductions before on-shell substitution.
Its exact rational nonzero-jet mutations all produce nonzero original residuals:
dropping the P nonlinearity, reversing Q coupling, dropping Q's momentum term,
and retaining only the background lapse. Exact residuals are retained in
`EQUATION_CHECK.json`; these controls expose those specific omissions, not all
possible defects.

A genuinely unpolarized homogeneous analytic test is available without solving
a numerical ODE. For arbitrary finite real p0,q0,v and t0>0, put

    tau=log(t/t0),
    P=p0+log(cosh(v tau)),
    Q=q0+exp(-p0)tanh(v tau),
    lambda=lambda0+v^2 tau.

Direct differentiation gives `P_tautau=exp(2P)Q_tau^2`,
`Q_tautau=-2P_tau Q_tau`, and `P_tau^2+exp(2P)Q_tau^2=v^2`.
The script verifies these exact identities. This is a useful nonlinear
homogeneous control in the same conditional arena, not a new native premise
or a statement about general initial data. NE1 is the separate inhomogeneous
polarized anchor; this review has not replayed all of NE1's source tests.

## Execution and omissions

Command from repository root:

    timeout 180s python3 udt_gpu_time_live_discovery_2026-09-30/review/fidelity/check_original_ricci.py > udt_gpu_time_live_discovery_2026-09-30/review/fidelity/equation_check.stdout 2> udt_gpu_time_live_discovery_2026-09-30/review/fidelity/equation_check.stderr

Exit 0; stdout, empty stderr, exact identities, versions, elapsed time and peak
RSS retained. Script enforces CPU<=180s and address space<=2GiB. No GPU process.
An initial passing run preceded adding the additional homogeneous control;
the final run passed both the unchanged Ricci checks and that new control.
No scientific repair was needed. Machine results own measured runtime values.

Not performed at this gate: author solver review, independent replay of grid
artifacts, numerical convergence/certification, transverse clocks, generic
topologies or t=0/asymptotic analysis, final central-integration review, full406
replay. Those remain separate gates. No sources, registry grades or CANON bytes
were changed. The strongest surviving conclusion is exact correctness of this
conditional metric reduction and its declared longitudinal readout.
