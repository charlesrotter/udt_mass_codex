# Initial direct adversarial review

Date: 2026-09-28 UTC. Reviewer `/root/july_optical_review`; same independence
record as SOURCE_FIRST_REVIEW.md, now exposed to the frozen new candidate,
author script, output, and the preserved failed initial script/diagnostic.

Reviewed initial candidate SHA-256:
`a8ac6f12056d82c4d9a1e4c6e763d661353bfeb95d537c7131ac1e77210f132e`.
All five entries in INITIAL_REVIEW_FREEZE.json matched before replay. The
CANDIDATE.md and INITIAL_CANDIDATE.md bytes were identical at this stage.
Author script SHA-256:
`acd60e5ce1f4ecbb9c1c3d13af0f93bffb695fcdc34fe86317cda1b2199dbb42`.
Scientific source hashes and source-first exposure are in SOURCE_FIRST_CHECKS.json.

**Verdict: VERIFIED-WITH-CAVEATS for the core conditional mathematical
application; one small domain statement is REFUTED as written and requires the
precision repair below.** No core equation was refuted. This initial review is
preserved for the authorized single repair/re-review cycle. It does not adopt
P-opt, a physical history, response class, universal observer rule or new premise.

## The user's concern about reversal

The parent relayed the active steering: “That sounds like the July work may be
flawed. A reversal is unlikely.” The mathematical inference is narrower than
“July or UDT predicts reversal”: **given** this stationary metric and these
stationary endpoint clocks, the exact two future clock-exchange ratios are
reciprocal. That is ordinary static gravitational/accelerated-clock behavior.
It does not establish that this supplied construction represents the intended
mutual positional effect. That identification remains unestablished.

The candidate properly excludes a universal reversal assertion and retains the
no-required-Hubble-expansion aim. Neither the user's concern nor founding
observer neutrality licenses a new requirement that every total received-clock
comparison redshift positively. Doppler and gravitational contributions remain
permitted. The candidate should be read as auditing this old realization, not
using its stationary prediction to define or refute the owner's intended effect.

Removing stationarity changes the applicable relation. Independently computing
the connection for `g=-f(T,x)dT^2+dx^2/f`, `T=c_E t`, and fixed-coordinate
unit clocks gives, for future radial sign `epsilon=+/-1`,

```
d log r / dO = -f_T/(2f) + epsilon f_x/2,
dO=|dx|/f=dT>0 on that ray.
```

Equivalently the rate is `phi_T-epsilon f phi_x`. This is the total clock
accumulation rate; it is not the derivative of a globally assigned endpoint
scalar in arbitrary time-dependent geometry. The spatial algebraic P-opt
restriction fixes `f_x` but leaves `f_T` open. Therefore the static reversal
does not survive as a generic theorem after that restriction is lifted.
No alternative physical model is selected by this observation. The root is
preparing a separately labeled bounded follow-up, to be reviewed in the same
authorized cycle rather than silently changing the frozen initial candidate.

## Required precision repair

Defective step: section 2 states “If f is any decreasing positive profile,
defining the variable kappa(x)=-2/f'(x) rewrites the differential equality.”

Counterexample: `f(x)=exp(-x^3)` is smooth, positive and strictly decreasing on
any interval around zero, but `f'(0)=0`. Its proposed coefficient is
`2 exp(x^3)/(3x^2)`, which is not finite at zero. Non-strict monotonicity permits
still more zero-derivative examples. The source-stage affine characterization
has nonzero derivative and is unaffected.

Strongest survivor: the variable-coefficient rewriting holds on intervals
where `f'<0`; it is not a smooth finite rewriting across stationary points.
Smallest repair: replace “any decreasing positive profile” by the explicit
`f'<0` interval condition and exclude stationary points. This changes no
physical premise, candidate equation or source grade.

An additional recommended wording refinement concerns the next gate. A full
metric/query construction is sufficient to determine received clocks, but is
not a demonstrated necessary prerequisite to every future bounded result.
“Physical geometric and observer/path data sufficient to determine the rate
or received-clock map” would make the actual missing dependency more precise.
The candidate already explicitly denies an all-UDT insufficiency/no-new-premise
necessity theorem, so this is not a refuted scientific conclusion.

## Core argument and hypotheses

1. **Profile restriction:** the original signed differential relation is exactly
   equivalent to `f'=-2/kappa` where f>0 and kappa is positive constant. The
   counterprofile breaks the claimed implication from reciprocal form alone.
   The candidate labels that counterprofile as supplied, without native
   membership. No positive or negative all-UDT conclusion follows.
2. **Proper clocks:** coordinate travel time has unit arrival-map slope in this
   stationary setup; the endpoint normalizations give the proper-clock ratio.
   The candidate correctly distinguishes this ratio from travel duration.
   Reference normalization gives `kappa_0=sqrt(f0) kappa`, preserving clock
   ratios while changing the optical calibration. No preferred observer is
   inferred solely from that normalization change.
3. **Direction:** the signed depth and positive travel length are kept distinct.
   The stated inverse applies to opposite future exchanges on the same
   stationary worldlines. It is not a generic later-return inverse theorem.
4. **Flat versus areal controls:** the explicit Minkowski pullback proves the
   flat Cartesian transverse control. Independently computing the full 4D
   Riemann tensor for the areal alternative gives `R=6b/x` and
   `R_abcd R^abcd=8b^2/x^2` on its positive regular patch. Thus the additional
   angular geometry changes the tensor despite the common longitudinal
   timing law. Neither metric is declared a native physical history.
5. **Covariant accumulation:** the candidate faithfully applies the repaired
   G402/G403 identity with supplied congruence and endpoint observers. The
   local rest measure and optical coordinate measure differ by the stated
   factors. A constant optical rate cannot silently become a constant rate
   per local rest length.
6. **All-direction total rate:** the at-event theorem is correct. The odd part
   forces zero acceleration, the trace-free quadratic part forces zero shear,
   and the remainder is H. The candidate explicitly makes this a separate
   hypothesis on the TOTAL observable and does not identify one summand as
   a new positional effect. The homogeneous exponential-scale control is
   free-and-explored and does not require Hubble expansion for UDT. The
   constant-rate property, owner neutrality, and stationarity are different
   assertions; their conflation would be a defect, but it does not occur here.

For the exponential-scale control, a regular future segment must exist in the
positive scale-factor metric. When solving its positive-h incidence explicitly,
`exp(-h T_A)-h L>0` is the reception condition; absent this, the chosen pair has
no finite reception event in that patch. The candidate's “regular radial null
segment” qualification includes this restriction. The independent implicit
calculation verifies the received slope without imposing a sign on h and has
the correct h=0 limit.

## Checks and adversarial probes

Executed command (exit 0, approximately 1.53 seconds):

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 timeout 60s python3 udt_july_optical_time_dilation_lead_2026-09-28/review/direct_checks.py > udt_july_optical_time_dilation_lead_2026-09-28/review/DIRECT_CHECKS.json 2> udt_july_optical_time_dilation_lead_2026-09-28/review/direct_checks.stderr
```

Python 3.10.12; SymPy 1.13.1. Eight additional exact checks passed; stderr
empty. This stage used small 4D coordinate tensors for the areal control,
two-dimensional time-dependent connection algebra, and an implicit null-arrival
derivative. The source-first 26 exact checks remain separate evidence.

Four wrong assertions were contradicted by exact nonzero witnesses: effective
kappa derivative `2`, exchanged rate difference `3/2`, normalization error
`-1/2`, and unequal trace-free shear readings differing by `3`. These are
wrong-assertion probes, not a demonstrated general implementation-mutation
harness. No false claim of injected-bug test coverage should be attached to them.

The author scripts were replayed **only under review-owned copies**, preserving
root frozen artifacts. Their identities were checked by SHA-256. This replay
is same-code regression, distinct from the independent calculations above.

- The preserved initial author script exited 1 at `two_direction_clock_product`,
  reproducing the stated symbolic-positivity limitation. The surviving radical
  expression is indeed one on the declared positive f domain; this failure is
  not evidence against the physical clock normalization.
- The revised author script uses a separately positive endpoint lapse. Its
  result exactly matches the frozen JSON: 20 exact checks, four rejected wrong
  assertions, three pulse controls, maximum pulse error
  `3.647304680498564e-11` against the `1e-8` declared threshold.
- Those floating-point controls are diagnostics, not physical certification.
  The static controls' arbitrary constant delay verifies only the arrival-map
  slope; it does not independently recompute travel time. The exact optical
  derivative and independent metric derivations cover the corresponding
  algebraic statements. No broad null solver or sampling completeness is claimed.

Skipped: full historical package replays, full premise verifier (parent-owned),
source/action dynamics, global metric/query realization, observational fits,
moving-observer time-live classification, all nonradial histories, a physical
scale, human/different-model/formal review. These omissions limit the verdict;
they do not upgrade or downgrade the current source grades.

## Return to the author

Preserve the initial bytes and this review. Apply the derivative-domain repair;
optionally narrow the next-gate wording to sufficient geometric/query data.
Submit the repair and the bounded time-dependent clarification for the one
authorized re-review. The conditional profile result survives. Whether that
profile realizes the intended positional effect remains OPEN; an unsupported
identification cannot be repaired by adopting the historical wall package,
fitting the target redshift, or imposing isotropic positive total rate.
