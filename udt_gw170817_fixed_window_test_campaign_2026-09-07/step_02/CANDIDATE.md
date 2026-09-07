# FW2 — failed frozen finite-statistic sensitivity screen

Candidate R1,23:44UTC2026-09-07, awaiting focused fresh-context re-review. Question,
premises, exclusions, effect query, estimator and alternative outcomes were
recorded BEFORE sample exposure in reviewed FW1 R1 FREEZE.json. No event
samples or event contrast were opened. This candidate changes no freeze.
Maximum claim is a finite off-source procedure result, not a metric constraint.

## Observed result

All99 permitted detector/block extracts are finite float64 arrays,401408
samples each, with exact98s supports/commands/SHA256 saved. They cover ONLY
the33 preselected off-source supports, never the reserved-event exclusion.
H/L CW injections are retained background; no all-injection-free claim.

Twelve records set the mean residual Welch PSD, including actual channel
cross terms. The retained PSD is finite/positive with zero floor activations.
The21 reference Q values mostly lie near1, but the record starting
GPS1187011516 gives Q=31313.95993221208 and fixes the frozen maximum threshold.
The max/min ratio is34778.9455. Chronological medians are0.96141(first10)
and1.06112(last11); these do not remove or explain away the extreme record,
prove exchangeability, or justify a new exclusion. DQ127 did not guarantee
a quiet background for this statistic.

At the frozen residual h_rss target1e-21 strain sqrt(second), fractions of
the21x8 reinjections crossing the SAME21-record maximum are:

| Synthetic spectral family | Crossings /168 | Fraction | Frozen >=90% gate |
|---|---:|---:|---|
|30–500Hz|5|0.0297619|FAIL|
|30–100Hz|3|0.0178571|FAIL|
|100–500Hz|3|0.0178571|FAIL|

The complete predeclared1e-23 through1e-19 grid is in evaluation_R1_run.stdout.
Even at its upper endpoint all three fractions are8/168=0.0476190, not90%.
These are descriptive in-sample fractions, NOT population detection power,
confidence levels, independent Bernoulli trials or observed source limits.
Tiny nonzero fractions at very small injections chiefly reflect adding a
positive fluctuation to the background record that itself set the maximum.
Do not call those a measured false-alarm probability or useful detection.

The code also algebraically solves the same fixed quadratic for each sample's
threshold-equality amplitude (strict-crossing infimum). Its90%-order-statistic
diagnostics are1.174875743e-18,1.136451302e-18,1.186434575e-18 strain
sqrt(second), respectively; equality itself does not pass the strict guard. These are
postprocessing of the saved quadratic coefficients, OUTSIDE the frozen direct
amplitude grid, not newly sampled injections, empirical confidence limits or
a second tuned decision rule. The declared gate already fails within the grid;
no conclusion depends on extending an observed amplitude range.

## Frozen finite diagnostic, not a repaired outcome

Following the unexpected large reference value, the author recorded a bounded
diagnostic before executing it: re-extract only that previously exposed support,
compare bytes and decompose the UNCHANGED statistic. All three re-extracted
arrays are byte-identical to the originals. The outlier weighted diagonal
contributions are H0.02138, L0.04744, V31314.13761; cross terms sum about
-0.24649, recovering Q31313.95993. A fixed ordinary reference has diagonal
H0.02158,L0.04767,V0.87125 and Q0.93883. Thus this chosen functional's large
value is Virgo-channel-dominated, not an omitted H/L covariance term or a
different retrieved file. The Virgo raw record includes a larger excursion;
its physical/instrumental cause is NOT identified here. This is not a flight-
data bug claim or a statement that the data must violate a physical model.
Author diagnosis shares screen.py and is not an independent review.

No record is deleted, no new transient veto is invented, no PSD/window/sky/
delay/effect threshold is changed, and no event result is examined. The review
must independently recompute the extreme Q and ordinary values from the saved
allowed data before attributing the failure to this actual procedure.

## Mathematical and implementation checks

FW1's exact finite cyclic/static identity remains the ONLY universal null
argument used. The two functions are arbitrary in its finite Fourier domain;
no binary phase/ellipse or physical mechanism is selected. Actual physical
rotating/finite-arm/upstream response retention is still OPEN, not verified
by this calculation. The result is not a power bound on a better statistic.

Author repaired method checks give relative null error4.36e-16, wrong-delay-sign error
0.86802 and omitted-H-term error0.34911. Both defective zero guards genuinely
fail at the frozen relative tolerance; equivalent tests at physical strain
scale also fail for the broken case, avoiding an absolute1e-10 false pass.
V-only inverse-shift injection round trip is7.08e-16 relative; h_rss includes
sample duration and is normalized before Hann. These support numerical fidelity
to the declared finite operator, not universal physical signal preservation.

With fixed PSD, feature Lr gives Q=||Lr||^2. Hence exactly
Q(n+a s)=Q(n)+2a Re <Ln,Ls>+a^2 Q(s). Saved coefficients preserve all21x24
combinations. Independent direct re-FFT of the added sampled core at amplitudes
1 and3 in scaled units agrees with the quadratic expression within4.11e-15
relative. This is author recomputation, not independent-context evidence.
Residual Welch versus the full spectral covariance decomposition agrees within
3.88e-16 relative. The observed band-L2 cross-term contribution is2.75e-5,
not assumed zero. Statistical/algebraic independence are not conflated.

Successful scientific runs used512MiB/60s, no GPU/install. Two R1 method/catch
launches accidentally omitted the single-thread environment and overlapped
after tool yield; both ended with returncode-9 near59.45s, no result, and are
preserved as failures. Serial retries with OPENBLAS_NUM_THREADS=1,
OMP_NUM_THREADS=1 and MKL_NUM_THREADS=1 passed in under0.5s each without
changing the scientific code or limits. The cause of the failed executions is
not diagnosed beyond this launch difference. Largest successful author peak
is206048KiB. NumPy2.2.6/SciPy1.15.3/
Python3.10.12; exact commands, durations, shapes, units and hashes are saved.
The prior CLI tool failure remains an UNPERFORMED review, despite exit0;
the current fresh built-in reviewer sealed its criteria before target exposure.

## One same-premise repair and preserved false-pass evidence

Fresh review independently recovered PSD, all reference Q values and the
extreme-record decomposition, but refuted the initial synthetic-generator
fidelity: rounded rfftfreq values put the nominal30Hz/100Hz lower bin just
below its inclusive boundary. Every family omitted one bin, changing the
PCG64 draw count and waveforms. The initial counts4/168,3/168,4/168 therefore
did not implement the frozen definition. They are superseded, not erased.
Initial candidate/source are preserved byte-identically in initial/; original
method/catch/evaluation outputs, coefficients and AUTHOR_CANDIDATE_READY.json
remain unchanged. Initial review and REPAIR_REQUEST.json identify the defect.

R1 selects exact integer bins low*98 through high*98, with unchanged bands,
seeds, real-then-imag draw order, normalization and all observational choices.
Inclusive counts are46061,6861,39201. endpoint_catch_checks.py actually rejects
the reinstated legacy float mask and accepts the corrected endpoint/count
guard. Core statistic bin membership is unchanged. R1 re-evaluates synthetic,
method/catch and reinjection claims only; the original PSD, reference records
and diagnostic retain their verified scope. training_run's embedded original
synthetic method numbers are historical, not the R1 method evidence.
The machine key finite_90percent_crossing_hrss is retained for compatibility;
it denotes the threshold-equality root/order statistic described above, not
strict crossing at equality. AUTHOR_REPAIR_READY.json pins all current and
preserved artifacts. No fresh noise training or further repair is authorized.

## Decision supported if verified

Stop this frozen maximum-reference broadband procedure at its failed gate;
do not open the event merely to produce a result or manufacture FW3. No new
geometric constraint, calibration of the event, physical-content identification,
UDT refutation/confirmation, scientific promotion or canon follows.
The practical missing step is a separately specified defensible background/
transient-handling and response-error procedure, not automatically a physical
premise. A better future statistic may succeed; this calculation does not
evaluate it. Future choices must disclose these exposed records and preserve
an unused confirmation consequence rather than retune this return into a pass.

Evidence: screen.py; H1/L1/V1_extract_run.*; PSD_training.npz;
training_run.*; reinjection_coefficients_R1.npz; evaluation_R1_run.*;
method_R1_singlethread_run.*; catch_R1_singlethread_run.*; endpoint_catch_run.*;
diagnostic.py/diagnostic_run.*. Dependencies and premise grades remain FW1/CO1/
CO2 and the current exact registry. Review version pins follow in the ready
record. Scientific conclusion awaits fresh separate-context verdict.
