# BG1 fresh adversarial review

Verdict: **VERIFIED-WITH-CAVEATS** for the frozen conditional mathematical
candidate. No unresolved load-bearing defect and no scientific repair is
required. This is review of BG1's small global constraint family, not scientific
premise adoption, canon, BG2 line drift, or review of the reviewer's auxiliary
construction as a new promoted result.

## Exact target and exposure

Author candidate: CANDIDATE_INITIAL.md,
SHA-256 ea499eede1127128eb5426e46a591cac71b9422f87b8982d9f7cf17212e55b9a.
Author checker: check_bg1.py,
SHA-256 aba081f421ff440d66a0f22e3047fced037cc579e14b67346c1f5eec747a35d8.
The three identities in CANDIDATE_FREEZE.md, including the initial baseline
output, were authenticated exactly. Detailed source and exposure pins are in
SOURCE_INPUT_SHA256SUMS, SOURCE_FIRST_SHA256SUMS, and POST_EXPOSURE_CHECKS.json.

Reviewer `/root/bg1_review` is an actual fresh separate context with no author
conversation fork. Exact backend/model and different-model independence are
UNTESTED. The source-first argument and separately written implementation were
sealed at 2026-09-08T19:31:42.525979+00:00, after notification that the parent had
frozen its candidate at 19:28 UTC, but before opening that candidate, checker,
outputs or methods record. The parent then explicitly permitted exposure.
The reviewer has not read the campaign log, former whiteboard, other reviewer
material or protected payloads. Parent startup receipt streams were
authenticated; the full startup verifier and Git synchronization were not
independently replayed by this reviewer.

Before exposure, the reviewer independently obtained the same scalar split,
mean-rigidity restriction, Cotton argument excluding proper conformal Killing
fields, and kernel-complement nonlinear existence argument. The code uses the
same installed SymPy library as the author, so separate implementation is not
a separate computer-algebra engine or numerical certification. Post-exposure
author replays are regression and reproducibility evidence. These independence
axes are not interchangeable.

## Mathematical scrutiny

The candidate's statement survives for every fixed a,c>0 with a!=c and every
fixed signed h!=0, with gamma fixed and Lambda=R/2+3h² fixed. It does not
quietly assume R>0 or Lambda>0. G310/G312 remain owner-provisional premises;
G315 and G330 retain their exact conditional scopes and sign convention.

1. **Original constraints and free trace.** With K=H gamma+A, tr A=0, the
   equations are exactly H²=h²+|A|²/6 and div A=2dH. The selected sign branch
   H=h sqrt(1+|A|²/(6h²)) works for either sign of h. A nonzero perturbation
   requires an O(|A|²) mean-trace change. The obstruction at fixed mean(H)=h
   is real but depends on an additional data restriction. Fixing gamma and
   Lambda does not add that restriction.

2. **Global adjoint compatibility.** Momentum paired with a conformal Killing
   field yields integral H div X=0. Thus the kernel must actually be addressed.
   Independent Koszul/Ricci reconstruction gives |C|²=3q²Delta², where
   q=2c/a² and Delta=4(c²-a²)/a⁴. This is a strictly positive spatial constant
   throughout the declared nonround family. The covariant three-index Cotton
   form is conformally invariant in dimension three; its norm scales through
   three inverse metrics. Therefore a conformal field with L_X gamma=2psi gamma
   obeys 0=X(|C|²)=-6psi|C|², hence is Killing. The proof fails at roundness
   exactly as the candidate says. I checked the author's cited transformation
   identity in Garcia et al., equations 79–86, and independently used
   Moroianu, Proposition 15. Neither source contributes a field law here.

3. **Function spaces and invertibility.** The energy identity for P=div L
   has the correct sign and factor -1/2. Its symbol is
   -|xi|² I-(1/3)xi tensor xi, with determinant -(4/3)|xi|⁶. Its kernel is
   precisely the conformal Killing fields. Compactness, smoothness and absence
   of boundary justify the elliptic Fredholm/Schauder method on the stated
   L2-orthogonal complements in C^(k+1,alpha) and C^(k-1,alpha), k>=3.
   The TT subspace of C^(k,alpha) is closed. The candidate does not invert P
   on all vector fields or assume the metric has no isometries.

4. **Nonlinear target and existence.** PW and dH are each orthogonal to every
   Killing field, for every small input, so F really maps into the selected
   target space. Composition and one derivative have the asserted Hölder
   mapping properties. At zero, D_W F=P and D_T F=0. The Banach IFT therefore
   gives an actual global solution W(T), with W=O(T²), not only a formal
   linearized solution. Substitution into the original constraints preserves
   the original gamma and Lambda exactly.

5. **Smoothness.** The candidate gives the correct linearization
   D_W F[V]=PV-(1/3)d(<A,LV>/H). Writing tau=3H, the negative principal symbol is
   |xi|² I+(1/3)xi tensor xi-(2/tau)xi tensor(A xi). Its real quadratic form is
   at least (1-2|A|/|tau|)|xi|²|v|². Taking |A|/|tau|<1/4 supplies an explicit
   sufficient coercivity margin within the candidate's smaller neighborhood.
   Smooth metric and TT seed then allow quasilinear elliptic bootstrapping.
   No uniform estimate toward h=0, roundness or degenerating radii is implied.

The imported theorems are ordinary analytical methods with hypotheses checked
here. Their general proofs were not reproduced computationally. Bartnik and
Isenberg's cited discussion explicitly warns about the conformal Killing
kernel; the candidate addresses that warning correctly instead of transferring
an unrestricted inverse or a conformally varied metric construction.

## Computation and false-pass audit

The sealed independent source-first run passed 25 exact identities and caught
four executed hostile algebra changes. Its original-equation family checks
and invariant-frame momentum calculation are distinct analytical controls;
they do not establish the author's IFT theorem by numerical testing.

After exposure, the frozen author baseline was rerun successfully and all six
actual author mutations were rerun. Every stdout and stderr was byte-identical
to its corresponding saved artifact, including failing outputs; expected
return codes were 0 for baseline and 1 for each mutant. The mutations change
the Cotton factor, h-sign branch, Hamiltonian denominator, momentum factor,
trace subtraction and operator sign. Their matching failures are recorded in
POST_EXPOSURE_CHECKS.json and the author_replay_* streams.

One limitation must accompany the 44-check count: the author's
covariant_rank3_norm_weight assertion differentiates a hard-coded exp(-6t).
It is arithmetic bookkeeping, not an independent test of the Cotton
transformation law or its tensor type. The finite checks therefore cannot be
used as the proof of that transformation. The analytical identity and the
three-metric contraction support it. I independently assembled that contraction
after exposure, but it too assumes conformal invariance as the stated external
mathematical identity. No hostile test of the full transformation law was
executed. This limitation requires accurate evidence wording, not a change to
the mathematical candidate or an exhausted scientific repair cycle.

The final aggregate replay used the existing shared run_capture.py with
512 MiB address-space limit, 60 CPU/wall seconds and one library thread. It
completed in 5.0633 seconds, maximum RSS 50,968 KiB, return code 0, no timeout.
Exact command, streams and resource record are final_bounded_capture.*.
Source-first streams and manifests were preserved unchanged. No GPU/PDE solve.

## Disposition and limits

No blocking objection was found. The strongest surviving statement is:
for each fixed positive nonround Berger metric and h!=0, every sufficiently
small smooth global TT seed produces, by the stated construction, an actual
smooth global solution of the original constraints at the fixed Lambda.
The trace changes as required by those constraints. This is a local family
in data space on the entire initial S3, with the inherited conditional
premises; it is not a complete global moduli classification or a selected
physical datum.

No repair is required. The minimum evidence clarification is to retain the
hard-coded norm-weight check only as bookkeeping. The source-first document's
auxiliary explicit Killing-vector family is reviewer-produced reconstruction,
not an additional independently reviewed author result, and must not silently
be promoted or used as a new accepted dependency. It supplies no BG2 drift
claim. A global TT direction with nonzero full marked Ricci-line drift still
requires BG2's separately framed computation and fresh review. No time
persistence, closed-orbit persistence, stability, action, matter, source, scale,
physical selection, or canon claim follows here.

External mathematical identities checked: Garcia et al.,
https://arxiv.org/pdf/gr-qc/0309008, section IV; Moroianu,
https://arxiv.org/pdf/1509.05156, Proposition 15; Bartnik–Isenberg,
https://arxiv.org/html/gr-qc/0405092, equation 49 and footnote 4 near equation 60.
The review did not replay earlier packages' full historical suites or external
reviews, prove their scientific premises, or verify host-wide process/backup
state. No grade, source, premise registry, accepted file or canon was changed.
