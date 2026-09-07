# LC2 initial adversarial review

2026-09-07 21:27 UTC. Reviewer `/root/clock_step2_review`, fresh separate
context; exact model UNKNOWN; different-model/human/formal axes UNTESTED.
Source-first reconstruction and independent Fraction/binary64 calculation
preceded exposure to the new candidate, code and saved benchmark output.
The seal and independent files were sent to the parent before candidate
hashes were supplied. Published paper results and prior source review were
known throughout; no outcome-blind empirical review is claimed.

Initial disposition: actual conditional arithmetic and scientific scope are
VERIFIED-WITH-CAVEATS. One grouped implementation-guard objection R1 remains
open for the authorized same-premise repair/focused re-review. No benchmark
number or physical premise was refuted. The final review must distinguish
this correct result from incomplete output-validation coverage.

## Exact inspected candidate

| File | SHA256 |
|---|---|
| step_02/CANDIDATE_RESULT.md | c55bf4a085d9c94a50e9f2cb9b168c03143b15304beb52a9be596f7a38982710 |
| step_02/evaluate_benchmark.py | 27c87e02c3cc2591b6735ef80e9fb40161cbf234733263600105271db2d65240 |
| step_02/benchmark_run.stdout | 94f823ad0475c487f412d0ef0d3871d505a78e914da47f40825904465e77d1b8 |
| DECISION_BRIEF.md | e698a87014c4de8ed2d6fc92ee44e9c78500736c6cbe2216ed6708a85f276bcb |

All hashes independently matched. The parent's benchmark capture reports
exit0, empty stderr,0.02203013s,2026-09-07T21:21:40.544720Z. Its60digit
Decimal implementation is distinct from the source-first exact Fraction
implementation. inspect_candidate_checks.py replayed the actual candidate,
compared its saved result exactly, compared load-bearing quantities with the
sealed independent output using relative tolerance5e-15 and zero absolute
tolerance, and reconstructed all seven hostile mutations itself. Captured
command/output/environment/limits are in candidate_inspection_run.*: Python
3.10.12,512MiB AS,60s CPU/wall, one CPU child, exit0,0.02355s, empty stderr.
This replay checks executable evidence, not the source experiment.

## R1 — incomplete output-validation coverage

Defect: validate() accepts all four of these corrupted copies of its actual
result, even though their reported scientific quantities are wrong:

1. Set clock_only.standard_uncertainty_acceleration_m_s2 to0.000001.
2. Replace the clock-only lapse-gradient band by[1.23e-16,1.25e-16]m^-1.
3. Set zero_mismatch_displacement to0.
4. Negate Q's standard-uncertainty width, reverse its endpoints accordingly,
   set zero-inclusion false and all-shifts threshold null, and set each Q
   scenario's zero-inclusion false. The squared-width equation still passes;
   the remaining checks never require a nonnegative width.

These are concrete false passes, saved under hostile_checks. They do not
show that evaluate() generated a wrong result: its actual saved result is
independently correct. They also do not negate the accurate report that the
seven advertised mutations were caught. They identify limited validation
coverage for primary outputs, so the passing guard suite cannot certify
those omitted properties by itself.

Strongest survivor: mu,D,Q,C,clock-only conversion, scenario memberships and
thresholds match the sealed independent calculation. Scientific interpretation
is appropriately conditional, and the old-center mistake is caught.

Smallest repair: preserve initial candidate/code/output, then add checks for
the acceleration uncertainty conversion, clock-only band endpoints,
b0=-D and nonnegative standard-uncertainty widths; catch-proof the four
reported defects, rerun the same input and document unchanged scientific
result. This is one bounded same-premise guard repair, not new research,
an uncertainty-model change or an additional campaign step. No need to
rewrite the independent source-first arithmetic or reprocess observations.

## Scope, arithmetic and source assessment

The source-first result gives mu=-10.907308499493622U and
D=-1.4926915005063786U, with Q upper SD2.6019223662515376U and C2.7U.
Both nominal bands contain zero. The clock-only effective upward log-lapse
gradient is(1.24+/-0.26)e-16m^-1, equivalent to
11.144564216336539+/-2.336763464715726m/s². Its error correctly uses only
the clock marginal2.6U. It is not another gravimeter record.

Five predeclared centers and memberships match exactly in the independent
rational implementation; both Q/C membership sequences are false,false,
true,true,true. The all-shifts thresholds are1.109230865745159U(Q) and
1.2073084994936214U(C), with b0=1.4926915005063786U. Generic quantifiers
follow the source-first variance/Cauchy-Schwarz and max|D+b| arguments,
not the finite numerical checks. The candidate already notes that the
negative-half C scenario's exclusion is fragile under source rounding.

Table1 and Methods use total2.6U, first/runwise corrected gradient-12.4U,
and two analyses of the same data. Supplement3H supplies rounded independent
gravimetry and DDS/camera height; no Fig4 inversion enters the prediction,
and no array-length or height error is added a second time. Source covariance
within the paired analysis is inherited, not recertified. Q adds zero
cross-covariance only as a comparator. C permits arbitrary admissible
cross-correlation of two supplied marginals, not arbitrary omitted bias.
Centering and adequate marginal uncertainties remain explicit assumptions.
No Gaussian distribution, coverage probability or realized-error bound follows.

The Killing identity applies to a supplied stationary congruence and proper
path. The actual reported slope identifies only an effective local linear
combination under stationarity, finite-cloud and metrology/readout assumptions.
G261 W4 is working physical-metric identification, not an atom/device
derivation; G276 does not let dimensionless ratios fix global scale. The
candidate and brief preserve these limitations, source-outcome exposure,
same-datum acceleration conversion, unrestricted-bias nonidentifiability and
non-distinctive metric agreement. For terminological precision, kappa is
the log-lapse gradient d ln N/dh; the stated equations give this meaning.

Not replayed: full theorem suites, all atomic/control coefficients, raw
instrument processing, pair covariance or metrology accuracy, different-model
or human review, and the parent's full349-row premise audit. That saved audit
was inspected and hashed b4c3136a75ec73e16b7966ed10df5095817920fad0c3393704e56ea6f73bb029.
No protected payload or GOCE work was accessed, no correspondence occurred,
and no premise, scientific grade, canon or manuscript changed.
