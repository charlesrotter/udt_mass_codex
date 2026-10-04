# CPR1 exposed mathematical review

Verdict: **VERIFIED-WITH-CAVEATS** for INITIAL_CANDIDATE.md at the hash in
EXPOSED_EXACT_FREEZE.json. No blocking algebraic or scope defect found. This is a
fresh separate-context review with independent implementation and argument, not
attested different-model review. SOURCE_FIRST_SEAL.json predates candidate exposure.
Parent controls, reviewed result and final central integration are not reviewed by
this verdict. No scientific status or native response-class admission is upgraded.

## Load-bearing argument

1. Equation (2) is correct. It has the important uniform source-incidence bound
   and keeps E and the regular circular emitter fixed. The horizon has finite
   received rate; the presentation lapse divergence is not a clock divergence.
2. Equations (3)–(7) correctly continue the same metric and same fixed histories.
   The regular A formula is positive. Differentiating the two actual incidence
   equations gives the stated Jacobian and arrival derivative; b must vary.
3. Equation (8) follows in the specified regular endpoint branch. The endpoint
   limit is not asserted for all source phases or every early emission. The
   witness at b*=0 still has generally nonzero finite-R incidence, so it does
   not replace an orbiting source by a radial emitter. The physical right side
   1/(c_E H) after restoring seconds is correct. Lambda=0 and negative-Lambda
   cases do not realize the same fixed-finite-E unbounded-outward experiment.
4. Equations (9)–(10) use proper angular rate and a supplied tolerance for its
   SQUARE. At fixed geometrically matched a,m this is an exact comparison.
   It is not an empirical solar-system bound or a fractional-period bound.
5. The angular amplitudes correctly reuse G201/G260 on f>0. Their sum vanishes
   for every Lambda, not their separate values. DDR in R10's actual response
   class likewise does not select Lambda. The scalar-gradient response diagnostic
   correctly prevents importing the space-form invariance argument into m>0.
   It is explicitly outside accepted physical dependencies and is no UDT
   countermodel or proposal to adopt a new response.

## Two useful clarifications

The tail implicit-function proof can expose its uniform ray-domain margin in one
line: a>3m implies (f/r²)'=-2(r-3m)/r⁴<0 for every r>=a. Therefore
s²(r,b)>=s²(a,b)>0 for b in a sufficiently small neighborhood of the strict
endpoint emission bound. The finite parts of U,P,I and their b derivatives are
then smooth, while x=1/r makes their infinity tails smooth. This completes the
otherwise compressed regularity argument without a new assumption or mechanism.

The candidate claims circular-orbit recovery, not stability; that statement is
valid without adding a stability premise. To avoid an observational overreading,
add: “This comparison alone does not certify orbital stability or disk recovery.”
If a later claim requires stable positive-Lambda orbits, the separate condition is

    V''(a)=2[m(a-6m)-(Lambda a³/3)(4a-15m)]/[a³(a-3m)]>0,

which requires a>6m and Lambda<3m(a-6m)/[a³(4a-15m)]. A finite ideal circular
geodesic can be compared even when unstable; an enduring astrophysical system
requires additional evidence. No stable-matter or particle-lane result follows.

## Independent evidence and limits

The source-first script uses a different endpoint witness (b*=2), a receiver
with E=1, and one fixed phase. It independently checks original outgoing-chart
metric norms/geodesic equations and actual incidence/arrival records. At 40/70
digits, 24 successful solved cases pass: maximum original-equation residual
2.30e-41, maximum centered-arrival relative error 6.84e-9, and precision comparison
below 9.11e-38. Holding b fixed produces 6.68%–46.9% errors and is rejected.
The four tail products H Z delta_tau_e are 0.93049, 0.991989, 0.999234 and
0.999924. These finite values support the independently derived limit; they do
not prove it. The initial failed R=25 root and frozen tail-domain repair remain
visible. No global nonexistence is inferred from that failed solve.

After candidate exposure, exposed_exact_check.py independently derives the full
four-dimensional diagonal-metric Christoffels/Riemann tensor and checks Ric=Lambda g,
Kretschmann=48m²/r^6+8Lambda²/3 and Weyl²=48m²/r^6. It also exactly checks both
angular amplitudes, the positive-f DDR diagnostic contraction, the V'' formula,
and monotonic f/r². Sympy 1.13.1 exact symbolic checks PASS; no numerical tolerance
or parent script import. Command:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 udt_candidate_commitment_restriction_2026-10-04/review_math/exposed_exact_check.py > udt_candidate_commitment_restriction_2026-10-04/review_math/exposed_exact_stdout.txt 2> udt_candidate_commitment_restriction_2026-10-04/review_math/exposed_exact_stderr.txt
```

The symbolic pass supplements rather than replaces the source-first exposure
boundary. It does not independently recertify every premise/source theorem.
The native clock-to-separation/X_max attachment, all-observer realization,
extra effect relative to matched GR, and response-class selection remain open.
The candidate preserves those exact limits and avoids a whole-postulate
insufficiency theorem. Final integration and parent finite controls await their
own review; this report does not certify artifacts that were unavailable.
