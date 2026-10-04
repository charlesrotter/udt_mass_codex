# CGE1 source-first mathematical review

Status: `SOURCE_FIRST_COMPLETE; CANDIDATE_REVIEW_PENDING`.
Date: 2026-10-04. Reviewer: actual separate context `/root/cge_math`.

This review supports a restricted conditional construction, not native metric
selection. The exterior, regular orbiting test clock, free receiving clock and
null-frequency/angular readout can be derived consistently from the admitted
conditional metric equation. Source formation, physical mass identification,
response-class membership, Lambda and observer preparation remain additional
unselected inputs. A single received shift does not determine Lambda when the
receiver preparation remains free; an exact three-case witness appears below.

## Context and evidence ownership

Parent startup/synchronization and ACP1 full406/fresh normal premise checks are
attributed to the parent at grok
`cdc94b5d1703d99230afaee632f47376645f5585`, not independently replayed here.
I independently inspected branch, HEAD and status: same HEAD on grok; baseline
untracked names plus this new package; no tracked edit then present. No protected
payload was opened, hashed or used. Only `review_math/` is written by this reviewer.

This is fresh-context and independent-argument/implementation review. A different
model is not established; runtime model identity is not independently attested.
Before this report I saw the dispatch, work order, baseline, AGENTS/CLAUDE and
triggered method skills, bounded central R2/R6/R10/R13/R8ACP and exact current R10
authority/audit sources. I have not read a parent candidate, checker, results or
verdict, nor another review. Mathematical background is shared. SymPy/mpmath are
independent implementations of the reviewer equations, not an independent proof
of their symbolic engines. An initial unanchored registry search unintentionally
matched descendant rows mentioning G301/G310/G312 and its output was truncated;
I then selected only exact row IDs. This exposure did not include a CGE1 candidate.

Current G312 authority qualifies all historical stronger language: full G301
class membership remains unclosed under GR FILTER ONLY. Historical G310
`NOT_ADOPTED` wording is qualified by current owner-provisional DDR adoption, which
is not canon or proof. R10's complete class hypotheses, nonzero Ricci coefficient
and Bianchi argument are inherited conditional inputs; this review does not
reprove the invariant-contraction classification or audit all historical replays.

Sources are version-bound in `SOURCE_HASHES.json`; hashes establish correspondence,
not truth or chronology. No web or literature items were used by this reviewer.

## Restricted exterior from the original equation

Set c_E=1 by expressing time in length units. Use the supplied areal chart

    ds^2 = -f(r) dt^2 + dr^2/f(r) + r^2(dtheta^2 + sin(theta)^2 dphi^2).

This is R2's restricted reciprocal presentation, with f=exp(-2 phi)>0 on the
connected static interval in use. It does not select spherical symmetry, an
actual source, a cosmic center or a global completion. With the ordinary
Levi-Civita curvature convention the original components are

    Ric_tt = f (f''/2 + f'/r),
    Ric_rr = -(f''/2 + f'/r)/f,
    Ric_theta,theta = 1-f-r f',
    Ric_phi,phi = sin(theta)^2 Ric_theta,theta.

The angular Einstein equation gives (r f)'=1-Lambda r^2. Hence on each such
interval

    f(r) = 1 - 2m/r - Lambda r^2/3.

The time/radial equations then hold identically; the independent script constructs
all 4D connection and Ricci components and checks all 16 original residuals.
This classifies only the supplied reciprocal static spherical ansatz. It makes
no theorem about all static spherical charts, constant-areal-radius geometries,
horizon extensions or global spacetimes. m is an integration parameter, with
length units under this convention. Its source/mass identification is not derived.
When m is nonzero r=0 is not an ordinary emitting clock in this exterior.

## Actual circular test clock

At r=a>0, theta=pi/2 the radial geodesic equation is

    f'(a) (u^t)^2/2 = a (u^phi)^2.

Writing Omega=dphi/dt and D=1-3m/a gives

    Omega^2 = m/a^3 - Lambda/3,
    u_e = (1,0,0,Omega)/sqrt(D),
    E_c = f(a)/sqrt(D),       L_c = a^2 Omega/sqrt(D).

Either sign of Omega is allowed. An orbiting future proper clock requires
f(a)>0, D>0 and Omega^2>0. Omega=0 is a separate stationary-geodesic limit,
not an orbit. D's Lambda cancellation is not Lambda-independent orbit existence.
The script checks the original geodesic equations and unit norm directly.

Regular circular does not mean stable. At fixed specific angular momentum L,
V(r)=f(r)(1+L^2/r^2). At the circular orbit

    V''(a) = 2[3ma-18m^2+15 Lambda m a^3-4 Lambda a^4]
             / [3 a^3(a-3m)].

Positive V'' gives the local radial minimum in this reduced test-particle problem;
it is not nonlinear matter/disk stability. For Lambda=0 and m>0 this changes sign
at a=6m, even though circular timelike geodesics exist for a>3m. None of this
creates or self-consistently supports a disk or source population.

## Receiver, null ray, frequency and sky

For an outward free radial receiver set

    u_o = (epsilon/f, W,0,0),   W=sqrt(epsilon^2-f),   epsilon>0.

W>0 gives a strict outward branch. At W=0 an integral using r as parameter
fails and turning-point direction needs separate handling. A positive conserved
photon energy E_gamma and signed impact parameter b give an equatorial direct
outgoing ray

    k = E_gamma (1/f, q,0,b/r^2),   q=sqrt(1-f b^2/r^2)>0.

The script independently checks both original geodesic equations and norms.
All points of the ray must stay in the same regular f>0, q>0 patch. Turning rays,
multiple branches and caustics require more incidence information.

For source radius a and reception radius R,

    omega_e = E_gamma (1-b Omega)/sqrt(D),
    omega_o = E_gamma (epsilon-W q_R)/f_R,
    Z = f_R (1-b Omega) / [sqrt(D)(epsilon-W q_R)].

All frequencies are positive for the regular future-clock/ray incidence; in
particular 1-b Omega>0. A radial ray has b=0 and

    Z = (epsilon+W_R)/sqrt(D).

The orbiting emitter factor is 1/sqrt(D), not the static-clock 1/sqrt(f(a)).
This is exactly why a fictitious central clock cannot replace the source.

An orthonormal receiving tetrad at the equator is

    E_0=u_o, E_1=(W/f,epsilon,0,0),
    E_2=(0,0,1/R,0), E_3=(0,0,0,1/R).

With sky direction opposite future propagation,

    n_1 = (W-epsilon q_R)/(epsilon-W q_R),
    n_2 = 0,
    n_3 = -f_R b/[R(epsilon-W q_R)].

The script checks every tetrad inner product and n.n=1 exactly. Reversing the
radial photon sign consistently replaces q_R by -q_R where appropriate; a
single denominator sign flip without changing the branch is false.
These are finite sky coordinates for a supplied ray. They do not by themselves
give a full source-patch Jacobi map or a scalar distance. ACP1's full-map and
source-compatible-reduction requirements therefore survive unchanged.

## Arrival derivative derived independently from incidence

Let

    T(b,R) = integral_a^R dr/[f(r) q(r,b)],
    P(b,R) = integral_a^R b dr/[r^2 q(r,b)],
    t_o'(R) = epsilon/[f(R) W(R)].

A fixed radial receiver line and circular source solve both

    t_e + T(b,R) = t_o(R),
    Omega t_e + P(b,R) = phi_o.

This is important: neighbouring emissions generally change b. Holding b fixed
would usually miss the receiver. Differentiation gives T_b=b P_b and
T_R-b P_R=q_R/f_R. Eliminating db/dt_e yields

    dR/dt_e = f_R W_R (1-b Omega)/(epsilon-W_R q_R).

Since d tau_o=dR/W and d tau_e=sqrt(D) dt_e, their ratio is the endpoint Z above.
The local two-equation incidence determinant is

    T_b P_R - (T_R-t_o') P_b
      = P_b (epsilon/W-q_R)/f_R > 0

for R>a, W>0, f>0, q>0. Thus this branch is a regular local correspondence by
the implicit-function theorem. This is a separate argument from substituting
the endpoint frequency formula into itself.

The independently coded finite anchor takes m=1, Lambda=1/10000, a=10, R=20,
epsilon=6/5 and b=2. f increases on [10,20], is positive there, and
f b^2/r^2<4/100 throughout, so no radial ray turning is present. The actual
receiver longitude is the integrated P=0.10098868009250229449..., and its initial
reception time is T=11.827054896817631938... . At 50 decimal digits:

    endpoint Z = 2.16321457634827469979828277147877...
    h=1e-4: actual symmetric arrival derivative error = 2.4990766100e-11
    h=1e-5: actual symmetric arrival derivative error = 2.4990766098e-13

Each varied ray solves both endpoint equations independently; maximum saved
incidence residual is 2.14e-50. The factor of approximately 100 is consistent
with the symmetric derivative's second-order truncation, not a universal error
certificate. The false receiver-sign expression gives 0.5121567599503547... and
is decisively detected. The original Ricci check detects a wrong Lambda/6
coefficient with exact angular residual -Lambda r^2/2. Both defects are actually
evaluated, rather than named as hypothetical catches.

## Single-shift ambiguity with free receiver preparation

For a radial event put A=Z sqrt(D)>0. Solving A=epsilon+W gives

    epsilon=(A^2+f_R)/(2A),    W=(A^2-f_R)/(2A).

Whenever A^2>f_R>0 this is a regular outward unit free-clock initial datum.
Changing Lambda within an open regular interval and adjusting epsilon preserves
the same Z. The receiver's timing can be initialized to intersect the actual
radial ray; this is a supplied preparation, not a new source law.

For m=1,a=10,R=20,A=6/5, the exact three-case witness is:

| Lambda | f_R | epsilon | W_R | Z |
|---|---|---|---|---|
| -1/10000 | 137/150 | 353/360 | 79/360 | 6 sqrt(70)/35 |
| 0 | 9/10 | 39/40 | 9/40 | 6 sqrt(70)/35 |
| +1/10000 | 133/150 | 349/360 | 83/360 | 6 sqrt(70)/35 |

Each has a regular circular source (positive Omega^2 and D), a positive static
exterior over this segment and outward free reception. This is an exact
counterexample to unique Lambda recovery from one such shift with free receiver
preparation. It does not refute identification with additional source, clock,
trajectory and angular/time records. Nor does it establish that every selected
shift occurs for every Lambda.

## Execution and limits

`FREEZE.md` and `independent_anchor.py` were saved before execution. Exact command:

    python3 udt_conditional_source_geometry_2026-10-04/review_math/independent_anchor.py > udt_conditional_source_geometry_2026-10-04/review_math/anchor.stdout 2> udt_conditional_source_geometry_2026-10-04/review_math/anchor.stderr

Exit 0; stderr empty. Versions: Python 3.10.12, SymPy 1.13.1, mpmath 1.3.0.
Four finite cases, one decimal precision and two derivative steps, one BLAS
thread, enforced 2GiB address limit, CPU only, no timeout. Results are saved in
`ANCHOR_RESULT.json`; stdout is preserved. No solver or candidate import, no
source data replay, no numerical grid or production run, no fit. This anchor
checks exact algebra and finite high-precision agreement; it does not certify
numerical quadrature intervals, global ray uniqueness, a physical metric,
source population, full disk transfer, matter formation or canon.

Candidate and final central integration review remain pending and must name
their actual later hashes/exposure. No final candidate verdict is issued here.
