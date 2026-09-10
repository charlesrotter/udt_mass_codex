# GL1 direct adversarial review

2026-09-10. Verdict: **VERIFIED-WITH-CAVEATS at the explicitly conditional
mathematical scope; UNPROMOTED.** No unresolved load-bearing mathematical defect
was found in the frozen candidate. No scientific candidate repair is requested.
The author's single syntax-only check repair was inspected and reproduced;
it consumes the work order's one allowed step-1 repair as already recorded.

Target: `step_01/CANDIDATE.md`, SHA-256
`9a390933b76167cbe13741ef0523cd69b06544c66f3e574d2355b27883e7bff1`.
Author check: `step_01/check_candidate.py`, SHA-256
`163d8c9222deae0aad8b4cf04842ff3f942cc9f771c67bd2e4065e0a3e8eb04d`.
All seven SOURCE_SHA256SUMS entries and all six CANDIDATE_SHA256SUMS entries
were actually checked and passed; raw output is preserved in this directory.
Hashes identify correspondence, not scientific truth or independence.

## Exposure and independence

Reviewer: actual separate context `/root/gr_limit_step1_review`; exact model
UNKNOWN, different-model independence UNKNOWN, human review NOT PERFORMED.
The source-first report was saved and sent to the parent before this reviewer
opened the candidate, author code or author results. Its unchanged SHA-256 is
`5824874bf4a87edf5d2b090fc57c7690a2b98da70943993103a40d9d033115cf`.

The independent check source was completed before direct candidate/code
inspection. The parent then disclosed that its implementation independently
used Fraction arithmetic, Kulkarni curvature realizers and the same known
mixed-Ricci involution witness. This is **different implementation with no
author-code imports, overlapping mathematical method**, not different-method
or cross-model independence. My source-first analytical reconstruction is
independent of the parent's proof but necessarily reuses G301's admitted basis
lemma. The later author replay is explicitly same-code regression only.

The source-first report records governing authority, exact scientific source
pins, the bounded startup read, and actual full365 failure. Current GR is FILTER
ONLY. Old W3/principal-overlap prose in historical sources was not used as a
current premise. No source grade, canon, physical coefficient or response
constitution was adopted.

Pinned startup HEAD was `6d463412a01b28819bb2a9f112bdb8b911681972`. During review
the parent preserved the initial candidate/check failure in `fabb3cae`; this
reviewer read that commit but performed no Git mutations. Parent publication
was not independently checked against the remote by this reviewer.

## Argument examination

1. **Domain and linearization.** The candidate explicitly assumes an equivariant
   ambient extension on K direct-sum tensor^j(V*) tensor K, rather than claiming
   a universal replacement theorem for metric jets. Covariant derivatives of
   actual curvature sit in this ambient space, but nonlinear commutator and
   differential Bianchi constraints remain relevant to actual realization.
   A sufficient estimate on the ambient space restricts to the realizable
   subset. No unjustified realizability inference is made.
2. **Zeroth-order trace and basis.** The invariant metric line gives F(0)=beta eta;
   P annihilates it. Differentiating overlapping equivariant germs is legitimate
   for each fixed Lorentz transformation because sufficiently small inputs
   belong to both neighborhoods. Reusing G301 yields A0=aS on K. Neither beta=0
   nor a!=0 is assumed in the general expansion.
3. **Parity.** For full O(1,3), -I acts by (-1)^j on the rank-(4+j) input and
   trivially on the rank-two output. Thus linear odd-slot maps vanish. This is
   exact and uses the stated group. No classification of even-slot maps or
   arbitrary connected-group parity theorem is silently imported.
4. **Uniform remainder.** Frechet differentiability of T at zero, T(0)=0,
   gives a finite nondecreasing supremum modulus omega on a sufficiently small
   ball, with omega(t)->0. For fixed finite m and ||Jj||<=Mj epsilon^(j+2),
   ||J||<=M epsilon^2 and each surviving even j>=2 term is at most
   ||Aj||Mj epsilon^4. Triangle inequality gives equation (7) exactly.
   If M=0 the zero-input case is separately handled. This proves the stated
   uniformity over the supplied input set, not over all maps or boosts.
5. **DDR consequence.** Equation (8) follows only on the explicitly separated
   fixed a!=0 branch. The approximate-balance term rho/|a| is correct. For a=0
   there is no division and no trace-free-Ricci conclusion. A lower bound on
   actual ||J0|| is correctly required to replace epsilon^2 normalization by
   actual curvature normalization.
6. **Optional power rate.** Integrating [DT(tJ)-DT(0)]J for t in [0,1] gives
   H||J||^(1+alpha)/(1+alpha). The extra C1/Holder hypothesis and segment domain
   justify this step. Mere differentiability does not provide that rate.
7. **Exact homogeneity control.** Substituting the weighted dilation into the
   proven expansion and dividing by t^2 leaves aS(J0); even derivative terms
   carry positive extra powers and the differentiable remainder tends to zero.
   The stated ray/domain qualification is necessary and present. This is a
   consistency extension of the old ray argument, not new physical ownership.
8. **Units, frames, and conclusion.** Fixed reporting units make the estimates
   mathematical statements; coefficients that would be dimensionful in a
   physical response are not thereby derived. No arbitrary-boost uniformity,
   physical small parameter, quiet scale, existence, metric convergence,
   principal dynamics, connected scalar constancy or UDT membership is claimed.

The proof is not circular in assuming GR principal overlap. It does assume the
specific response type/regularity/ambient extension and a strong input hierarchy;
these are its openly conditional hypotheses. The new result is the controlled
finite-jet weighted first-order estimate, not the G301 contraction basis or a
new nonselection counterexample.

## Independent checks and false-pass audit

`independent_contraction_check.py` uses exact standard-library Fraction
arithmetic (Python 3.10.12), dictionary curvature components and direct Ricci
contraction. Its source SHA-256 is
`75e8b5b6a2f8e6d70f1ac08ba61ccb958b8777be02081aadaad2714971a28210`.

The successful run contains **33 mathematical witness/identity/covariance/bound
checks plus one bookkeeping assertion** that the expected catch count is 13.
The output's total 34 must not be called 34 independent scientific checks.
There are **13 named deliberately wrong-claim/formula catches**, not a complete
operator mutation campaign. Actual rc=0, wall=0.0387026800s, maxrss=15476KiB.

The decisive degeneracy witness has mixed Ricci diag(1,1,-1,-1), scalar R=0,
S!=0, and Ricci-square equal to eta, hence TF(Ricci-square)=0. An explicit
algebraic-curvature realizer satisfies the curvature identities and contracts
to that Ricci tensor. This confirms an exact a=0 quadratic-response DDR zero
with nonzero S at formal curvature scope; it does not claim a spacetime
development or furnish a new UDT response law.

The nonhomogeneous polynomial witness combines a fixed nonzero Ricci term,
constant trace, a formal Hessian-of-scalar derivative slot and Ricci-square.
Exact remainder identities and triangle bounds were checked at four rational
values. The review code's amplitude variable is epsilon_review=1/k^2 and its
variation variable delta_review=1/k; this is candidate epsilon=1/k, so its
reported error/epsilon_review is the candidate's error/epsilon^2. Measured
exact ratios are 47/16, 47/64, 47/256, 47/1024. These support this polynomial
witness only; they do not prove a universal differentiability modulus.

Checks also demonstrate unsuppressed even-derivative cancellation and covariance
under one rational boost. They deliberately catch dropped derivative terms,
dropped nonlinear terms, omitted trace projection and the false nondegeneracy
inference. The analytic proof, not these finite witnesses, establishes the
general estimate, parity statement and regularity rate.

The author program was inspected for vacuity and circularity. Its explicit
norm1 bound is sound: ||TF X||_1<=2||X||_1,
||Ricci-square||_1<=||Ricci||_1^2 and |R|<=||Ricci||_1 give its
6||H||_1+14||Ricci||_1^2 bound. Exact arithmetic supplies no loose numerical
tolerance. Its constructed-curvature tests check only the generated Ricci
subclass; they are not a full-space basis census. Its four wrong-claim catches
are narrow controls, not complete mutation coverage. Shared tf/square routines
inside author expectations are same-code checks; the independent implementation
and proof review supply the additional scrutiny, with the method overlap noted.

## Check repair and regression

Original script SHA-256
`5e89aa523c07665a6b9e1b1b28d78b23baf76a253b72f50a07eae85f13530aaa`
was verified directly from `fabb3cae`. The retained raw stderr shows
SyntaxError at line 37: the outer list-comprehension closing clause in square()
was missing. Parsing failed before any assertion executed; original rc=1 is
not evidence of a mathematical failure or any passed check.

`git diff fabb3cae -- udt_gr_limit_campaign_2026-09-10/step_01/check_candidate.py`
confirms exactly the declared
one-line completion of that outer loop and bracket. No formula, expected
answer, tolerance or candidate text changed. CHECK_REPAIR.md accurately records
the scope. The reviewer replay of corrected code returned rc=0 in
0.0965032620s, maxrss=11328KiB. Its stdout is byte-identical to the corrected
author stdout. Counts reproduced: 6168 finite constructed-curvature identities,
98 weighted identities, 49 exact bound probes, 13 covariance checks and four
negative controls. These categories retain their limited evidence meanings.

All reviewer captures reuse the inspected existing run_capture.py, with absolute
output stems, 512MiB address-space and 60 CPU/wall-second caps. Each command set
OPENBLAS_NUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=NUMEXPR_NUM_THREADS=1;
only one reviewer CPU check ran at a time. Scripts ran with python3 -S and no
external library imports. Exact argv, cwd, UTC start, rc, wall time and maxrss
are in the corresponding .json; stdout/stderr are preserved verbatim.

## Ceiling, omitted checks, and return

No historical full G301 intertwiner census, whole-repository test suite, actual
metric-jet realization theorem, nonlinear PDE solve, convergence/compactness
theorem, physical filter test or observation was repeated. These are not needed
to validate the stated conditional lemma and are not passed by this review.
Actual full365 remains NOT_PASSED at unchanged G325 replay_exact; no banking or
scientific integration follows.

The strongest survivor is the candidate's weighted response estimate and its
optional rate, with the exact nonzero-a qualification for a Ricci consequence.
All eight source-first objections to stronger claims are handled by explicit
hypotheses or exclusions. The surviving scientific bridge is still whether the
physical UDT response belongs to this class and whether any appropriate DDR
metric family realizes its hierarchy. There is no unresolved mathematical
objection within GL1 and no further repair requested.
