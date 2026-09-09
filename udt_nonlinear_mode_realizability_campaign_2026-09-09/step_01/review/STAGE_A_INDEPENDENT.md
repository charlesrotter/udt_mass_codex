# NR1 Stage A — independent source-first mathematical analysis

Recorded 2026-09-09 16:04:35 UTC, before candidate proof/code exposure.
Reviewer context: actual separate `/root/nr1_review` context. Exact model identifier
not exposed: UNKNOWN. No different-model or human/formal review claim.
Baseline directly checked: grok, HEAD 454bd6ffd24e0f13dfca6ee0a3e8df1c795e2ad6.
Unrelated/protected untracked paths were visible only in git status and were not read.
Synchronization is parent-owned; the review does not independently assert remote freshness.

## Exposure and source pins

Read AGENTS, bounded LIVE/HANDOFF/current-program/premises startup, relevant CLAUDE
sections, no-shortcuts/completeness-map/solver-first/verifier-before-record skills,
INDEX/MEMORY, campaign log, exact G312/G324/G327 rows, and both controlling G324/G327
AUDIT_REPORT and EXACT_DERIVATION files. Did not inspect candidate proof or code.
The parent dispatch stated the constraint question, and the campaign log disclosed
the integrated-translation-momentum hypothesis. Thus source-first argument and
implementation independence are claimed, not blindness to that hypothesis.

SHA-256 pins observed at this stage:

| Source | SHA-256 |
|---|---|
| CURRENT_SCIENTIFIC_PREMISES.tsv | bee5059ab5528282420c5cd833d0aadfd4946d64820ba0c7bde1c1a98e09e165 |
| G324/AUDIT_REPORT.md | 7e0c9988e4af291bfbda89bf662a3c10e0205e29620cc00a599bc59a110dc873 |
| G324/EXACT_DERIVATION.md | 5563c949b952fd0ddd0365f58e24eb14894d8bdaae7cab8a6bc5fad983bee776 |
| G327/AUDIT_REPORT.md | 505d0d91e4b66862d95c0b541f6c226ad8f262fa2ab5bb58c67bba029593d4ce |
| G327/EXACT_DERIVATION.md | cb8212fe3b584bd3ba42240e7234f15571b4571f347d2003bc9f9a20b5dd3835 |
| campaign CAMPAIGN_LOG.md | 20c36b1fcc59c9c6b5abc70f241b2ddb5b11afccb990dce71a46b1149069b7c1 |
| shared run_capture.py | 8ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef |
| startup full365_final.json | e43beeefd1a3a84980ae3831e37488c615008dddd7d397d10f90ed5c2ad95807 |

G324 and G327 abbreviations denote the exact repository packages identified in
the dispatch. G324 controls the supplied compact split translation quotient;
G327 controls its eight-real-constant first variation. The historical pending
review heading inside G327 EXACT_DERIVATION does not supersede its current audit
and registry grade. No source package has been replayed by this review yet.
The parent-owned full365 receipt was read: exit 1 at G325 DERIVATION_RESULT.json
replay. It is NOT_PASSED and is neither waived nor repaired here. It blocks any
assertion of full integration/banking but not this explicitly bounded review.

## Quantifiers and choices

Question: full second-order initial-constraint obstruction to a C2 parameter family
with exactly the prescribed G327 first variation on a common neighborhood of the
complete compact T0 slice. Fields are smooth in space/time, with sufficient mixed
parameter/spacetime regularity to differentiate induced initial data twice.
All higher-order metric, extrinsic-curvature, scalar and harmonic corrections are
free-and-explored. Smooth periodic gauge changes are allowed. Supplied quotient,
T0>0, C1,Cperp>0 and primitive k=2pi/LX are pinned-by-THEORY only in the sense of
G324/G327's conditional supplied-domain definitions, not physically selected.
The Einstein equation remains conditional on owner-provisional G310/G312 premises.
No topology/carrier/physical-identity/stability or exact-family sufficiency claim.

Method: exact ADM constraint identities as geometry of the admitted equation,
finite Fourier algebra, then independently implemented full constraint expansion.
Any CPU capture: one library thread, 512 MiB address space, 60 seconds, no GPU;
stop at a load-bearing unresolved disagreement or the delegated 75-minute limit.

## Independent analytic calculation

Use K=(1/2)partial_T q and pi^{ij}=sqrt(det q)(K^{ij}-tau q^{ij}).
The Einstein momentum constraint is D_j(K^j_i-tau delta^j_i)=0 for every Lambda.
For any smooth periodic Y, compact integration by parts implies

    I_Y(q,K) = integral pi^{ij} (L_Y q)_{ij} d^3x = 0.

Take Y=partial_X, a globally defined translation of the supplied quotient.
At the background q0 and pi0 have constant spatial coefficients. For
q=q0+eps q1+(eps^2/2)q2+o(eps^2), similarly pi, the order eps^2 coefficient is

    integral pi1^{ij} partial_X(q1)_{ij} d^3x,

because partial_X q0=0 and the pi0 contraction of partial_X q2 integrates to zero.
Thus arbitrary second-order fields, including homogeneous and higher harmonics,
cannot affect this necessary condition. No use was made of a nonlinear tensor
ansatz. Lambda(eps) cannot affect the momentum identity.

Write q1_AB=2 b^2 H_AB, H=[[p,c],[c,-p]], b=Cperp T^(2/3).
Let hp=2/(3T), tau=1/T and dot denote partial_T. Direct variation gives

    pi1_AB(with upper indices) = sqrt(det q0)/b^2 *
                                [dot H + 2(tau-hp)H].

Consequently the surviving pairing equals

    2 sqrt(det q0) integral tr(dot H H_X) d^3x
      = 4 sqrt(det q0) integral (dot p p_X + dot c c_X) d^3x,

the H H_X term being an exact periodic derivative. For each polarization write

    h = (Ac J+Bc Y)cos(kX) + (As J+Bs Y)sin(kX),
    J=J0(z(T)), Y=Y0(z(T)), W=J dot Y-dot J Y=8/(3pi T).

The average dot h h_X is

    -(k/2) W (Ac Bs-As Bc).

All positive quotient factors are nonzero, hence necessarily

    D = (Ac Bs-As Bc)_plus + (Ac Bs-As Bc)_cross = 0.

The transverse translation pairings vanish because q1 is independent of y,z.
The condition is not separate vanishing by polarization: equal and opposite
polarization contributions cancel. It is also not exclusion of Y0 or of a spatial
phase. A single-polarization independent cosine-J/sine-Y choice has D!=0 and
supplies a falsifier for universal exact realizability of all eight constants.

## Full second-order constraint solvability, not exact sufficiency

At fixed T0 use an orthonormal frame for q0. Then

    K0=diag(-1,2,2)/(3T0), tau0=1/T0,
    A=tau0 I-K0=diag(4,1,1)/(3T0).

For the linearized constraint operator, restrict the correcting spatial metric
variation to u=0 and permit an arbitrary symmetric correcting K variation v.
The Hamiltonian and momentum linearizations are

    delta H=2 A:v-2 delta Lambda,
    delta M_i=partial_j v_ji-partial_i tr(v).

Quadratic forcing from the declared single axial harmonic has only mean and
twice-axial harmonics. At a nonzero axial physical frequency kappa,

    delta M=i kappa(-v22-v33, v12, v13),
    delta H=2(4v11+v22+v33)/(3T0)-2 delta Lambda.

This map has full rank four: v22+v33 handles M1, v12/v13 handle M2/M3,
and v11 handles H. At zero frequency the mean Hamiltonian is freely adjustable
through v11 (even with delta Lambda=0); all mean momenta are annihilated.
The global pairing identifies the only potentially nonzero mean forcing, M1,
and the transverse means vanish. Thus D=0 is sufficient for solving the FULL
second-order constraint coefficient using finite Fourier corrections; it is
not sufficient by itself for an exact constrained family or spacetime solution.

This finite-mode right-inverse argument avoids reliance on an unverified general
linearization-stability theorem. A corroborating adjoint check: any background
Killing initial datum obeys sym(partial Y)=2 N K0. Each nonzero Fourier coefficient
on the torus has left rank at most two while K0 is invertible, so N=0 and then
Y=0 at nonzero frequency. The mean equation gives N0=0; Y0 may be any translation.
Only the three translation obstructions survive. The right-inverse proof above
is the load-bearing completeness argument; the adjoint check is corroboration.

## Gauge and remaining review work

Existence modulo a legal parameter-dependent periodic spacetime diffeomorphism
can be pulled back to a representative with the declared first variation;
constraints and compact pairing remain exact. Illegal nonperiodic transformations
or replacing the fixed supplied quotient are outside this necessity argument.
Candidate must state adequate C2 regularity for its Taylor steps and must not
confuse the absence of any further second-order obstruction with exact existence.

No candidate verdict yet. Next: independently reconstruct the local second-order
momentum and Hamiltonian forcing, run exact Fourier/right-inverse checks and real
mutated-check controls, then inspect the parent's frozen candidate directly.
