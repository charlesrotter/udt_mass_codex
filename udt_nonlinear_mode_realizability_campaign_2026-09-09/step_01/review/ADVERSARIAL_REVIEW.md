# NR1 adversarial review — VERIFIED-WITH-CAVEATS

Completed 2026-09-09 16:11:05 UTC. UNPROMOTED review of a conditional mathematical
candidate; no banking, physical adoption, canon or integration claim.

The frozen NR1 **necessary obstruction** survives. No load-bearing mathematical
defect was found in the candidate. On its fixed supplied compact quotient, a
prescribed G327 tangent to a regular C2 exact family must obey

    Q = v_c dot u_s - v_s dot u_c = 0,
    equivalently sum_polarizations(A_cos B_sin-A_sin B_cos)=0.

This does not say that every Q=0 tangent has an exact realization. The candidate
explicitly does not claim that sufficiency, and this verdict does not add it.

## Exact objects reviewed and independence

Baseline directly checked: grok, 454bd6ffd24e0f13dfca6ee0a3e8df1c795e2ad6.

| Object | SHA-256 |
|---|---|
| step_01/INITIAL_CANDIDATE.md | 871a64977c723db32fa4697c4b61cd3a57ec7f318c061585b187774549731f86 |
| step_01/check_nr1.py | e1957936ebbdb0348e13e63f17003aea5e3f8d9b3ab895dce7df48c0c1f93357 |
| review/STAGE_A_INDEPENDENT.md | 2e7159bf1a0193780d1441a26b38eea910a34df3815680f0a93734ae5d0b19a9 |
| review/independent_adm_check.py | ca53b67447808a22b61fcb14eef02912180ea71430dde45539980d4cf785a23e |
| review/harmonic_guard_followup.py | 21feabc105e96dcd35c15453270790d69a65d2581345ac82e079de03c2bf384b |

Stage A owns the initial source pins and exposure. The candidate freeze was
announced only after Stage A had been saved and the independent geometry script
had been written. The script's first capture also preceded direct candidate reads.
The full initial candidate manifest was checked: all five entries matched.

Reviewer: actual separate `/root/nr1_review` context; exact model UNKNOWN.
Source-first independent argument: yes, but the campaign log had disclosed the
momentum-pairing hypothesis. Different implementation: yes, direct local ADM
constraint expansion plus exact Laurent algebra, with no candidate imports.
Different model/human/formal proof review: not established. Both implementations
use SymPy 1.13.1, so shared library risk is retained. Candidate code replays below
are regression evidence and are not counted as implementation independence.

Direct-review source addition: G303 audit and exact Gauss--Codazzi/constant-Lambda
sections were read after the candidate identified that interface. SHA-256:

    G303/AUDIT_REPORT.md
    8830a1b8fba6e82fd964508c6df766f0b9227affbd64dc12a19f4d585d07e3fc
    G303/EXACT_DERIVATION.md
    4eb48002d2424e9745d92fcbf734213dec81a912343057d76775961f93b6b378

The G303/G312/G324/G327 current registry scopes agree with the claimed use.
Accepted source reviews, whole package replays and their historical repair chains
were not independently repeated; only the source interfaces made load-bearing
by this necessity proof were examined. No protected payload was read or modified.

## Adversarial argument audit

1. **Arbitrary higher-order correction.** The exact momentum constraint paired
   with the fixed global translation gives integral(pi L_X gamma)=0 for each
   epsilon. The background L_X gamma0 vanishes pointwise. Its constant pi0
   contracts any second-order metric correction to a periodic total derivative.
   The pi2 term vanishes pointwise. Therefore no shape, harmonic, lapse, shift,
   embedding or homogeneous correction at second order can cancel the surviving
   bilinear term. This is an exact identity, not a finite ansatz assertion.

2. **Connected scalar freedom.** G303 gives M=0 in every connected constant-Lambda
   sector. Lambda(epsilon) can affect the Hamiltonian equation but never the
   translation momentum pairing. The proof neither freezes Lambda nor inserts
   an independently propagating scalar. No new physical conservation law follows.

3. **Density and raising signs.** Candidate K=-gamma_dot/2 yields
   pi1_AB(upper)=(V0/b^2)[-Hdot-2H/(3T0)]. The terms proportional to H integrate
   to zero; the remaining coefficient is exactly the candidate's
   -2 V0 A_perp k LX Q. Both inverse factors used in raising K matter. The
   reviewer used K=+gamma_dot/2 and reversed the overall momentum sign; the zero
   set agrees. No sign ambiguity affects the claimed obstruction.

4. **All eight constants.** Exact Fourier averaging gives the sum over the two
   polarizations, not separate vanishing. A plus cosine-J/sine-Y example fails
   the necessary condition. A two-polarization example with opposite nonzero
   contributions survives it. Neither spatial phase nor Bessel branch can be
   discarded. G327 supplies the nonzero Wronskian 8/(3pi T), and its ODE gives
   Q'=-Q/T; the restriction is independent of the positive reference slice.

5. **Gauge.** A smooth periodic infinitesimal spacetime gauge vector has a
   parameter flow on a common smaller neighborhood of the compact slice. Pulling
   a putative exact family back removes its pure-gauge tangent and preserves the
   equation and compact constraint identities. The fixed translation need not be
   Killing after deformation. Nonperiodic transformations, changing the supplied
   quotient problem, or adding physical first-order modes do not test this claim.

6. **Regularity and domain.** The verdict interprets a C2 parameter family in the
   usual sufficiently differentiable field topology: induced gamma and K and the
   compact integral admit the stated two parameter derivatives. Merely separate
   pointwise differentiability without the requisite mixed control is not covered.
   The interval stays strictly inside T>0 and contains the complete compact slice.
   There is no boundary flux, asymptotic endpoint condition or whole-time claim.

## Independent recomputation and actual false-pass controls

`independent_adm_check.py` reconstructs the spatial inverse, all Christoffel/Ricci
components, mixed K, trace, Hamiltonian and all momentum components to order eps^2
in a q0-orthonormal frame at T0. Write (p,c) for polarizations and (u,v) for their
time derivatives. In the reviewer's positive-K convention the local result is

    M1^(2)=4(p u_x+c v_x)+2(p_x u+c_x v)
            +4(p p_x+c c_x)/T,
    M2^(2)=M3^(2)=0,
    H^(2)=8(p p_xx+c c_xx)+6(p_x^2+c_x^2)
            -2(u^2+v^2)-8(pu+cv)/(3T).

The mean first momentum is exactly

    kappa*(J Ydot-Jdot Y)*sum(Ac Bs-As Bc),

which independently matches the candidate's zero set. No trigonometric numerical
quadrature or finite tolerance is used: Laurent coefficients are exact.

The first capture reported 17 symbolic predicates and eight rejected corruptions.
One of the 17 predicates, named `quadratic_forcing_only_zero_and_second_harmonics`,
only checked absence of powers +/-1. It was **insufficient and is EXCLUDED as full
support evidence**. Inspection exposed that weakness. The original script/output
are preserved byte-unchanged; `harmonic_guard_followup.py` injects actual +/-3
terms, reproduces the old false pass, checks every Laurent exponent, and rejects
the third- and fourth-harmonic mutations. Both actual constraint supports are
exactly {-2,0,2}. This reviewer-only repair has no consequence for NR1 necessity;
the candidate did not rely on this additional support predicate.

Other independent corruption controls reject omission of geometric connection/
inverse terms, reversal of the velocity derivative term, omission of cross
polarization, wrong Wronskian orientation, lost linear constraint correction
directions, separate polarization restrictions and universal realizability.

The finite constraint right inverse and adjoint discussion saved in Stage A are
exploratory corroboration only. They are not a separately reviewed result, and
neither the candidate nor this verdict uses them to assert exact sufficiency.

Candidate regression replay: all 20 symbolic checks passed. The three candidate
mutants were rerun literally by the reviewer and each exited 1 specifically at
`full_fourier_integral_matches_candidate`; this was not a missing-dependency or
resource failure. Each capture preserves its exact command, stdout, stderr,
versions, duration, return code and memory receipt. CPU only, one library thread,
512 MiB address space, 60-second per-capture budget; actual durations below one
second each, peak recorded child RSS at most 63,284 KiB.

The parent count is 20 executed predicates, **not 20 independent mathematical
checks**. Of its nine density-matrix component comparisons, five are structurally
zero outside the declared transverse block; the four transverse entries comprise
only two distinct component identities because of symmetry/trace relations.
The zero first-order trace/volume tests are also TT-sector regressions. The
load-bearing algebraic support is the actual raised-density variation, full
Fourier pairing, ODE propagation and Bessel coefficient conversion, alongside
nonzero and cancellation examples. The finite polynomial periodicity check
illustrates integration by parts but does not prove arbitrary-correction scope;
the written compact integration argument does. The standalone original-zero
example is a boundary control, not affirmative evidence for nonlinear existence.

## Defect, survivor, smallest repair and limits

Candidate defect: none found in the stated necessary-condition proof.
Survivor: every admitted exact-family tangent in precisely this compact G327
sector must have Q=0. The nonzero-Q example refutes universal exact realizability
of all eight constants, without refuting the accepted linear solution census.
Candidate repair: none required. Retain the above regularity interpretation and
the candidate's explicit necessary-only ceiling in every downstream description.

Reviewer check defect and smallest repair: the incomplete harmonic-support guard,
with explicit reproducer and exhaustive support replacement preserved above.
This is a same-reviewer check repair, not another separate-context review.

The prior full365 receipt at startup_surface_current_tracking_compaction_2026-09-09/
full365_final.json is exit 1 at the G325 replay. It remains NOT_PASSED and is not
waived. The parent reported a separate new small-budget audit stopped earlier at
a git subprocess and a later 2 GiB retry reached the G325 failure again. Those new
receipts remain parent-owned; this reviewer did not inspect or rerun them and does
not substitute that report for the personally read prior failure receipt. No
global premise-audit PASS or banking follows.

An initial attempted read of nonexistent `step_01/CANDIDATE_PROOF.md` returned
exit 2; the freeze manifest then identified `INITIAL_CANDIDATE.md`, which was read
and hash-checked. This was a navigation error, not a lost scientific calculation.
All scientific attempts, guard exposure and corrections are retained in review/.

Exact-family sufficiency, common developments for survivors, endpoint behavior,
other tangent sectors, genericity, stability, sources, physical matter/modes and
topology or scale selection remain outside this review. All sources keep their
existing premise stamps and limits. No source/current document was modified.
