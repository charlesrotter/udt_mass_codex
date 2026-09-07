# LC2 — conditional published-summary clock benchmark

Candidate, not scientific promotion. Evaluated only after the reviewed LC1
contract/inputs were committed and pushed at dd6260e6. Exact frozen contract
ac6cbaeb359713d90abb71b43e83a47bc2e7d669f878c01c1b1455cb1c8541e4;
inputsa006e39a03b2ee70418ecee614c9056fe3e1c4a04b110478cdb536d01f410b9f.
Published outcome exposure is known; this is not a new blind experiment.

## 1. Result in the source's measurement units

Let U=10^-19 fractional frequency per proper centimetre in the source's
top-to-bottom ordering. Use one published corrected gradient y=-12.4U with
reported TOTAL standard uncertainty2.6U, not a new fit. Independently supplied
g_mag=9.803m/s², c_E=299792458m/s and the exact unit conversion give

    mu = -g_mag*.01/(c_E²*10^-19) = -10.9073084994936... U.

Difference from source's printed -10.9 is -0.0073085...U, below the frozen
0.05U rounding-check tolerance. Printed g precision is not independently
certified gravimeter accuracy. Extra arithmetic digits establish correspondence,
not additional experimental precision. At source precision the reference is
-10.9U and the residual is approximately -1.5U.

| Frozen comparison | Residual D=y-mu | Displayed upper standard uncertainty | Descriptive D±U band | Zero inside? |
|---|---:|---:|---:|---|
| Q: zero cross-covariance comparator | -1.49269 |2.60192|[-4.09461,1.10923]|Yes|
| C: arbitrary admissible cross-correlation | -1.49269 |2.70000|[-4.19269,1.20731]|Yes|

Table units are U; extra digits identify the implemented calculation only.
The nominal residual is approximately0.57 of Q's displayed width,0.55 of C's.
No p-value, validated confidence interval or "UDT passes" claim follows.
The C bound is SD(e_y-e_ref)<=u_y+u_ref<=2.7U, conditional on the reported
marginal scales and centered-error model. It does not cover arbitrary omitted
bias, certify the source's internal covariance or turn1σ into a hard bound.
Q's zero cross-covariance is a declared comparator, not experimentally proven.

## 2. The local geometric constraint actually obtained

Under G261 W4's working physical-metric identification and the source's
stationary, effective-linear-gradient/readout/finite-cloud assumptions,
the upward logarithmic lapse gradient kappa_up=d ln N/dh is

    kappa_up = (1.24 +/- 0.26) * 10^-16 m^-1,
    a_clock = 11.14 +/- 2.34 m/s².

These are source-standard-uncertainty summaries, not confidence or hard-bound
intervals. a_clock=c_E² kappa_up is the SAME clock datum expressed as an
equivalent supported-acceleration component, not another measurement or a
new force law. Its clock-only error uses2.6U alone, not the reference error.
Compare it with the separately supplied gravimeter magnitude9.803m/s² only
under the declared metrological bridge. No retuning of g, height or corrections
was performed to improve agreement.

The source's approximately1cm extent is not applied a second time: these are
per-proper-length quantities using the source's calibrated height normalization.
For a general non-linear/nonstationary field, the published slope is a weighted
source summary and does not identify an arbitrary pointwise derivative. No
new acceleration-variation bound, Earth/source solution or vacuum equation
inside apparatus matter is supplied. The exact conditional Killing identity
a=c_E²d ln N is geometric; the atomic/laser/gravimeter realization is supplied.

## 3. Robustness: correlation is not arbitrary bias

Actual nominal inputs stay fixed. The prescribed displacements b=t*2.5U
are diagnostic shifts of the corrected gradient, not fitted or reapplied
calibrations. They are not known hard bounds on actual bias and are not added
to the existing error budget as independent noise.

| t | b/U | Shifted residual (D+b)/U | Zero in shifted Q band? | Zero in shifted C band? |
|---:|---:|---:|---|---|
|-1|-2.50|-3.99269|No|No|
|-1/2|-1.25|-2.74269|No|No|
|0|0|-1.49269|Yes|Yes|
|1/2|1.25|-0.24269|Yes|Yes|
|1|2.50|1.00731|Yes|Yes|

The widths remain fixed, centers move, and the exact test is |D+b|<=U_Q/C.
The negative-half scenario is close to C's boundary: its all-printed-input
classification is not a robust claim against source rounding or alternative
justified uncertainty conventions. None of these counterfactual rows establishes
that a correction error occurred or creates a new experimental significance.
The adverse scenarios are retained rather than discarded.

A shift b0=+1.49269...U would set the central mismatch to zero. This is a
sensitivity threshold, NOT a fitted recommendation to change calibration.
For all displacements |b|<=B, zero remains within the displayed band precisely
when B<=U-|D| (with nonnegative right side): approximately1.10923U for Q,
1.20731U for C at the printed inputs. Those are conditional algebraic
thresholds, not measured bounds on bias. If an unrestricted additive gradient
bias is admitted, any clock slope can be explained and this comparison ceases
to identify the geometric gradient separately. The source's bounded/modelled
corrections, not unique selection of every legitimate input, supply the needed
restriction. Cauchy–Schwarz does not repair unbounded-bias nonidentifiability.

## 4. Checks, provenance and limits

evaluate_benchmark.py reads only the frozen LC1 JSON/contract. First execution
2026-09-07T21:21:40.544720+00:00, exit0,0.02203013s,15168KiB peak RSS;
512MiB AS/60s CPU/wall. Python3.10.12, Decimal60digits, arithmetic regression
tolerance1e-45. Exact command/environment/output are in benchmark_run.*.
No GPU, raw arrays, observation fit or new public search/contact.

Seven deliberately injected defects were rejected: sign reversal, missing
cm conversion, statistical-only uncertainty, duplicate experiment count,
target-derived reference, the LC1 R1 old-center rule, and an unsupported
coverage label. These are implementation/claim regression controls, not proof
of experimental validity. Generic covariance and bias-threshold statements
depend on the actual LC1 mathematical argument, not on a finite test count.
Fresh LC2 review must independently recompute the load-bearing quantities,
inspect implementation and attempt false passes before downstream use.

LC2 R1 review found four additional guard false passes, while independently
confirming every actual numerical result. Initial code/candidate/brief and
benchmark_run.* are retained; review/INITIAL_REVIEW.md and
review/candidate_inspection_run.* preserve the counterexamples. One same-premise
repair adds acceleration-uncertainty conversion, clock-only band endpoints,
b0=-D and nonnegative-width guards. The four corrupted outputs are now also
rejected, for eleven finite regression cases total. repair_run.* records the
same frozen inputs, exit0,0.021189s,15552KiB RSS at21:30:26 UTC. The entire
scientific result object is exactly unchanged, not just rounded agreement.
Focused re-review must close R1; finite guards still are not exhaustive proof.

Source: Zheng et al., Nature Communications14,4886(2023),
https://www.nature.com/articles/s41467-023-40629-8, Table1/Methods and
Supplement3. Exact source pins and all supplied assumptions remain in LC1.
No second same-data analysis or clock-inverted height was used as independent
evidence. Control-response calibration can leave a gravity-only target, but
shared records and published outcome exposure are retained. This is a
retrospective constraint under a trusted published summary, not independent
raw metrology/covariance certification.

What remains free: unsampled lapse/spatial metric, curvature, global family,
initial data/history, matter/content and physical realization. Ratios alone
leave homothety invariant; fixed dimensional anchors can fix it within an
identified model, which is not a new global scale inference here. The result
does not select the phase/current/product recipe or identify G352 content.
Agreement is shared metric consistency, including GR. A disagreement would
concern the combined geometry/readout/correction contract, not automatically
all UDT or a new mechanism. No adopted premise/grade/canon/manuscript change.
