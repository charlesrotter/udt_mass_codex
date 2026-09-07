# LC1 initial adversarial review

2026-09-07 21:16 UTC. Reviewer `/root/clock_step1_review`; separate context,
exact model UNKNOWN; different-model/human/formal axes UNTESTED. Source-first
seal preceded new contract/input exposure. Public outcomes and ORS reviews
were already known. No new benchmark outcome was calculated.

Verdict: REPAIRABLE_DECISION_RULE_AMBIGUITY, conditional scientific contract
otherwise retained. One wording repair is required before LC2 execution.

Reviewed exact initial bytes:

- COMPARISON_CONTRACT.md:
  `7070320ff58c38b43f2e73c667cd27824a0947eed613b0a2fcc13a0017a88842`.
- INPUTS.json:
  `a006e39a03b2ee70418ecee614c9056fe3e1c4a04b110478cdb536d01f410b9f`.
- Source-first seal:
  `638894d4a32139727ba8ca8374b6e64bba2a3976deab3af090520277333e37e4`.

## R1: specify what shifts in the displayed uncertainty band

The error-model section first defines the residual D and its uncertainty
bands, conventionally [D-U,D+U]. Robustness item(ii) subsequently requests
membership of D(b)=D+b in the "fixed Q/C displayed bands". Taken literally,
this tests membership in [D-U,D+U], equivalent to |b|<=U. But item(iii)'s
threshold U-|D| tests the intended zero inclusion after displacement,
|D+b|<=U. Those are different decision rules.

Exact counterexample independent of this experiment: let U=1, D=3/4 and
b=1/2. Then D+b=5/4 belongs to the original interval [-1/4,7/4]; nevertheless
zero does not belong to the shifted interval [1/4,9/4]. The former wording
can therefore label a scenario as retaining overlap when the intended rule
does not. This is an ambiguity in the prospective recipe, not evidence of
a numerical wrong result: no benchmark implementation/output was reviewed.

Smallest repair: state explicitly in items(ii)/(iii) that the Q/C widths
remain fixed while centers move to D+b, and the test is |D+b|<=U_Q or U_C,
equivalently zero in [D+b-U,D+b+U]. The all-|b|<=B threshold U-|D| is correct
for that rule. Preserve the initial contract and objection; inputs need no
change. This consumes the one allowed same-premise repair/focused re-review.

## Strongest surviving contract and checks

The stationary Killing identity, sign, cm-to-m conversion and effective
linear-gradient restriction agree with the independent source reconstruction.
The clock-only inferred kappa/a is correctly separated from independent
gravimetry, and its uncertainty correctly uses u_y alone. No vacuum equation
is extended into the apparatus; no Earth geometry or distinctive UDT signal
is inferred. The source-controlled finite-cloud/stationarity approximations
remain explicit and are not certified by the exponential remainder alone.

Direct main Table1/Methods and Supplement3 comparison confirms the primary
corrected y=-12.4, total2.6, documented split .7/2.5, correction+122.8,
rounded g magnitude9.803 and expected-reference uncertainty<.1. The JSON
pins match independently hashed sources. Printed -10.9 is only a rounding
check; .01m is unit conversion, not a duplicated .99cm height correction.
The first/runwise gradient alone is primary; repeated analyses and inverted
heights do not become independent evidence. Control responses, including
Zeeman/lattice shared response and the conditional DC model, remain supplied.

For centered square-integrable errors, Cauchy-Schwarz gives the stated
covariance envelope, and independent/zero-cross-covariance quadrature is
properly labeled as a comparator assumption. Sharpness follows by taking
e_y=u_y Z and e_ref=-u_ref Z for any mean-zero unit-variance Z. Gaussianity is
unneeded; these are variance/standard-uncertainty conclusions. The contract
explicitly rejects hard-error bounds, validated confidence coverage and
unbounded omitted-bias protection. It does not sum per-row standard errors
as an unsupported new total. Counterfactual bias shifts remain scenarios
with unchanged calibration, not fitted nuisance corrections.

The source uncertainties are rounded reported marginal scales and the
reference cap is used conditionally at that precision. No extra precision
or fresh instrument/error certification follows. Source unblinding history
does not confer outcome blindness on this retrospective benchmark.

The saved shared-session premise audit was actually inspected: returncode0,
PASS for349-row registry and named current guards, empty stderr,
400.2323792249954seconds. Audit-file SHA256:
`b4c3136a75ec73e16b7966ed10df5095817920fad0c3393704e56ea6f73bb029`.
Its command was python3 verify_current_scientific_premises.py. G261/G276/
G312/G313 exact active-scope/source columns were checked afterward. This is
verification of the parent's saved run, not an independently rerun full audit.

One small standard-library Python check parsed the frozen JSON assumptions
and independently evaluated the exact hypothetical R1 counterexample; PASS,
exit0, Python3.10.12. An attempted jq check could not run because jq is
absent (exit127); it supplied no scientific evidence and was replaced by
Python. Commands/outputs are preserved in REVIEW_CHECK_RESULT.json. The
Python check ran under512MiB AS/60sCPU/wall and calculated no experiment
residual, reference, inferred acceleration or other new benchmark outcome.

No full source theorem tests, instrument/raw-processing pipeline, raw pair
covariance or external calibration were replayed; this review concerns LC1's
source/statistical comparison contract. No GOCE search/action/contact,
protected payload access, external fetch, raw fit, solver/GPU, new premise,
grade/canon/manuscript change or write outside step_01/review/ occurred.
