# ALP1 direct fidelity and physical-meaning review

Verdict: **VERIFIED-WITH-CAVEATS for the frozen candidate's stated conditional
claims and source fidelity.** No substantive scientific or fidelity defect was
found that requires a repair to INITIAL_CANDIDATE. This is not physical adoption,
an independent proof of FAC1, a full-postulate insufficiency theorem, human
validation or cross-model verification. Final integration remains to be read.

## Identity, versions and exposure

Reviewer `/root/alp_review_fidelity`, same inherited Codex/GPT-6 model family;
fresh separate context, independent source-first frame and separate implementation.
SOURCE_FIRST.md and its pins preceded candidate exposure. Direct exposure then
included ALP1 INITIAL_CANDIDATE, SCIENCE_FREEZE, both original researcher
candidates, B WORK_RECORD/FREEZE and saved moments_01 stdout/receipt. B's checker
implementation was not read or reused. The ALP1 notebook, PRIMARY_METHOD_NOTES,
other review findings and any integration draft had not been read at this verdict.
Original owner statements and central source scopes were read first as recorded.

Independent hash check agrees with the dispatched science freeze:
`9a502898d0aac7f7bb0e6eb7dad3d6477617a5d1c2b20405c462221b44d95092`.
Joint candidate SHA-256:
`b510d53aeef4093cbd727d57f2ca3179b59dd3547c1539a95c756bd05513339f`.
Other directly exposed artifacts and this check have their hashes in DIRECT_PINS.
Parent startup/full406 evidence remains attributed through RECOVERY_RECEIPT;
this reviewer did not replace that with a fabricated independent startup pass.

## The physical inference survives at its written scope

The original statements fix actual received ticks, ordinary local proper clocks,
one geometry with SR/gravity and an additional positional contribution, and a
universal law whose numerical comparisons may depend on circumstances. They do
not explicitly specify FAC1 weighting, logarithmic angular averaging, or a
universal total-net sign. The candidate reports precisely that source observation,
and repeatedly declines a theorem of full-postulate insufficiency. It preserves
the tentative status of the combined-net-redshift and solar-distance expectations.
No source is downgraded merely because the proposed statistic is not derived.

FAC1 remains a conditional regional-vacuum theorem on a specified laboratory
and its original preparation sphere. The candidate neither replaces that sphere
with the detector sky nor changes two independent first signals into an inverse
or an echo. It preserves the fixed-worldline derivative, the regional rather
than pointwise vacuum hypothesis, fixed finite U, uniform small-L angular
remainders and equality-case caveat. It does not infer a selected physical
vacuum, observer population or absolute scale.

The common-D family has the intended limited force: a supplied regular family
of actual parallel-prepared free clocks has opposite local signs despite the
same first-reception boundary size and distant divergence power. Calling D a
comparison boundary is correct: at D the limiting receiving proper time is
infinite; there is no finite receiving event or inserted spacetime wall. The
construction is explicitly nonvacuum, frame-specific and untested as an
empirical GR limit. Thus it is a valid counterexample to the named kinematic
implication, not to all owner commitments, physical X_max, every recovery regime
or a distant positional effect. The comparison scale is supplied, not fitted
or derived. This reviewer checked the preparation/incidence logic and the
scope; the separate math review owns the complementary detailed finite-control
recalculation and any numerical confirmation of it.

## Independent reconstruction of the central measure argument

For a boost along one spatial axis, set a=cosh rho, b=sinh rho and x=n_x.
Acting on the future null vector (1,n) gives f=a+bx and received direction
y=(b+ax)/(a+bx). Direct differentiation, using a²-b²=1, gives
`dy/dx=(a+bx)^-2`. The clock ratio is p=1/f=a-by. This independently fixes
which Jacobian carries which sky measure and avoids borrowing a sign from the
candidate's terminology.

With normalized measures dx/2 and dy/2, direct integration gives reception
`<p^-2>=1` and `<log p>=rho coth rho-1`, while the emission uniform mean is its
negative. Positivity follows from the derivative of `rho cosh rho-sinh rho`,
not from a physical positional premise. The same result follows by carrying
dx/2 with the Jacobian before integrating. Rotation-invariant finite sky
probability is uniform, and this boost changes that measure. The candidate's
no-common-Lorentz-invariant-probability claim is therefore correctly bounded;
it does not deny observer covariance with a carried measure.

The separate finite numerical implementation in check_boost_measure.py verifies
this argument at rho=0.25,0.8,1.5 on 1024/4096/16384 Simpson panels. It passed
the frozen absolute tolerance 2e-10. Maximum finest discrepancy was
`6.67021993194794e-13`. At rho=1.5 the maximum discrepancy fell from
`4.3681909311921174e-8` to `1.7085832748620078e-10` to that final value.
Omitting the Jacobian changed the sign; replacing it with its inverse failed
normalization by 0.0850839768 or more. The zero-boost control gives log mean 0
and normalization 1. These are finite double-precision confirmations, not
interval certification or proof for every boost.

TPS1 capture `checks/boost_measure_01.json` reports exit 0, 0.061031681 seconds
wall, 2GiB address-space cap and 10,752KiB maximum RSS. The checker reports
0.044503233 CPU seconds. One process, one-thread environment, no GPU, no killing
timeout, empty stderr. CHECK_FREEZE and its hashes preceded the unique launch;
no failure was discarded and no output was overwritten.

## Normalization and moment consequence

There is an independent scalar way to check the variance bookkeeping. Put
d=log p and M=<d>. Uniform d=O(L²) implies

    log <exp(t d)> = t M + (t²/2) Var(d) + O(L⁶)

for each fixed finite t; the expansion is local to the fixed laboratory.
At t=-2, `<p^-2>` differs from the geometric mean precisely by the variance
term at order L⁴. This explains why redefining a normalized density cannot
establish the proposed equality or sign: its required normalizing constant is
the very observable N under test.

Diagonalize the symmetric trace-free E by an orthogonal frame change. The
ordinary sphere moments `<n_i^4>=1/5` and `<n_i²n_j²>=1/15` give
`<E(n,n)²>=(sum lambda_i²)/5 + 2(sum_(i<j)lambda_i lambda_j)/15
=2 E²/15`, since the eigenvalues sum to zero. Thus
`Var(d)=E²L⁴/30+O(L⁵)`; M² is O(L⁸) under regional vacuum. Combining this with
the supplied FAC1 m4 yields `n4=-2m4+E²/15=(8E²+3B²)/180` independently of
B's basis-code implementation. Solving these two scalar relations gives exactly
`E²=15(n4+2m4)` and `B²=20n4-80m4`.

This is a conditional inference from ideal asymptotic moments. It cannot infer
vacuum from finite clock records, reconstruct a full curvature tensor or certify
noisy measurements. The candidate says so. The positive-square obstruction is
strict at a nonzero-Weyl event for every fixed finite U because E and B together
determine Weyl relative to that observer. It leaves vanishing Weyl at one point
and higher-order behavior open. The all-event/all-observer exact-SCN2 corollary
correctly first forces Ric=0 regionally using the quadratic term, then invokes
the vacuum result to obtain flatness. SCB2 is not given that equality step.
Neither trial is adopted, and their rejection does not reject the weaker AMS.

The direction-map decomposition is also correctly typed. Actual sourceward
arrival directions on A, with its freely transported frame, supply a small-L
map from the preparation sphere; C1 closeness to identity and compactness give
a degree-one local diffeomorphism and then a diffeomorphism. Its positive
Jacobian is an angular measurement independent of p. The identity for M is
bookkeeping; only its Jacobian term has the Jensen sign. Delta is not an
identified physical positional component. The candidate does not extrapolate
the map through caustics, sky gaps or distant multiple images.

## Defect hunt and smallest repairs

No substantive defect was found in the frozen synthesis. The tested potential
defects — source/reception swap, dropped Jacobian, false normalization from a
density definition, inverse-versus-first-return confusion, pointwise-vacuum
replacement, scalar diagnostic promoted to vacuum detection, common D promoted
to physical X_max, and a partial source search promoted to full-postulate
insufficiency — are explicitly avoided by its equations and qualifications.
Researcher B's preserved `folds,+multiple` typo is already explained in its
WORK_RECORD and absent from the joint synthesis; no scientific repair is needed.

Integration should retain the individual first-signal inequalities and the
words regional vacuum, fixed finite laboratory, ideal asymptotic and unadopted
where they are load-bearing. It should lead with the rejected identification
and surviving conditional diagnostic rather than imply that no physical
selection route remains. These are integration review conditions, not a request
to strengthen or repair the science.

## Is return warranted, or should the campaign keep exploring?

My source-first suggested same-record statistic/measure test is adequately
answered here. The candidate does more than restate a missing join: it shows
opposite sky means for a fixed map, computes the variance term that defeats the
proposed prepared-clock normalization even in positive-AMS vacuum controls,
and retains a concrete two-moment curvature diagnostic. The independent
measure integration and cumulant reconstruction support that assessment.
Calculating more arbitrary power means or curvature-dependent weights would
alter procedural choices without supplying a new physical discriminator.

The strongest surviving positive alternative is an independently motivated
relation between actual arrival-angle and clock records, or a finite-distance
relation tied to a physically specified comparison family. The candidate makes
that route more concrete through its independently measurable Jacobian and
uncontrolled Delta. A further expansion of that map could be mathematically
useful, but by itself would not explain why the uncontrolled term obeys a physical
sign law; no source-backed sign principle is newly available in the inspected
packet. Restricted contrast or distant-onset proposals likewise remain possible,
without treating a GR reference as mandatory or inventing a source law.

I therefore support the work-order return point **precise rejected identification
with a surviving useful route/diagnostic**. This is a decision about the learning
value already obtained, not a proof of exhausted hypotheses or a declaration that
new premise adoption is necessary. Continuing solely to avoid a negative return
would be unwarranted; a new concrete principle with an informative test could
legitimately reopen the route under appropriate authority. This judgment uses
the work order's decision-ready return criterion, not a time or resource cutoff.

## Omitted checks and conclusion ceiling

No independent FAC1 quartic theorem proof, Kerr curvature/ray replay, general
nonvacuum quartic expansion, finite-distance error bound, empirical filter,
instrument model, global sky map, external-literature census or full-native-UDT
admission check was performed. B's exact run was inspected as attributed
evidence; my direct mathematical reconstruction and independent quadrature are
the independent checks. No protected payload was accessed. The independent
math review is complementary and is not silently credited as work done here.
The present verdict is on the frozen candidate; review of repaired or integrated
text requires its actual later versions.
