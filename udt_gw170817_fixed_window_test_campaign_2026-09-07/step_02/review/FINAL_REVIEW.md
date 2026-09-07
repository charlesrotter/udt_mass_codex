# FW2 R1 final adversarial review

2026-09-07 23:50 UTC. Reviewer `/root/fw2_fresh_capacity_check`, fresh built-in
separate context, exact model UNKNOWN. Different-model, human-specialist and
formal-verification axes UNTESTED.

VERIFIED-WITH-CAVEATS for the failed, precisely frozen off-source finite-
statistic screen. The single grouped same-premise R1 repair is closed; no
load-bearing objection remains at this scope. This supports stopping this
procedure at its supplied resolution query. It supplies no event result,
population power, geometric constraint, physical-content identification,
instrument-wide exclusion, scientific promotion or UDT confirmation/refutation.
The event remains UNEXAMINED. Physical response/error eligibility stays OPEN.

## Exact reviewed versions

Paths below are relative to step_02. Actual hashes were checked, including all
initial-preservation entries in AUTHOR_REPAIR_READY.json. Candidate text's
pending-review label is historical; this review owns the present verdict.

| Artifact | SHA256 |
|---|---|
| CANDIDATE.md | f32a1ec5bd01ac5922fbc5da7cdefa77d90f8c9bfa3ca6e9f377493352d0f1e5 |
| screen.py | d8229dbd658f9503bcb59e2356f99ae160d5a96d98bf2e4155fd12f9f3326396 |
| evaluation_R1_run.stdout | d61503205be13c68d9137a289cf78d704cf5ce544ab9831c1e94a301a43a9c9f |
| reinjection_coefficients_R1.npz | 0bc7cf0bb448636fdb691fd4b538ee9983a003b69dc3b9148b4a07051194831b |
| PSD_training.npz | 6cf4c75cac9a38318311da37a16de0bb6b7c629643d52008b2eb2b8b70b758ea |
| training_run.stdout | 33a7cff5cc4504888f8550d9925c0a3a445b10919a05b1a84e1788ce406e527a |
| diagnostic_run.stdout | 15c2d0328daff630af79aeda79a5a8b05d7ee6be5ea3b894498ec958471ce023 |
| AUTHOR_REPAIR_READY.json | a6b67a34835e5d15f4ece720b534b61a077f72169b1b7e9a47016d2fcc3cc1fe |
| review/SOURCE_FIRST_SEAL.md | 1d29131ba82d068495c634cc6d8c9e77b2db878a68ae2dd371912266567e1c6f |
| review/INITIAL_REVIEW.md | 3d33ec38bbf7fb67b3622190f8005956ef83aa7df2c7edfa9ed6a2b58edcb150 |
| review/independent_R1_replay_run.stdout | 78ce4f3625607eebee53dd684ba60fc623a7915b4d3c0b42b1264f65204c543d |
| review/focused_R1_run.stdout | cee6edfb14a797395b62a3d69f8ca5beb555f598231520c29cbdf1a20efd4cfc |

Controlling FW1 R1 freeze remains
fa0506eaea5ef20dcd92aabf3b2d1a0efc7fb75ef6c7272c00e5e6764c591324.
CO1/CO2 and source/version/exposure pins are in the unchanged source-first seal.
Checksums establish correspondence, not truth or independent chronology.

## Independent result

The 99 saved detector extracts match all hashes, sizes and 33 frozen supports;
none intersects GPS[1187008680,1187008980). All three original HDF5 file hashes
independently match FW1. Hash-only comparison also confirms the three repeated
extreme-record extracts are byte-identical. No new sample support was read.
H/L continuous-wave injections remain part of the released background.

An independently written pipeline uses full complex FFT shifts, explicit
44-segment Welch averages, determinant-derived null coefficients and a
polarization-identity covariance decomposition. It does not import screen.py
or call its scipy Welch/csd helpers. Mean training PSD agrees to 3.57e-16
relative L2 and 2.84e-13 maximum relative discrepancy on retained bins.
The retained physical PSD minimum is 2.96248e-46 strain^2/Hz, with zero floor
activations. Actual covariance cross terms are retained; their band L2
contribution is 2.74698e-5, not an assumed zero.

Every reference Q agrees within 7.94e-15 relative. Core1187011516 sets
Q=31313.959932212096, versus ordinary values about1; max/min is34778.94553.
Chronological medians reproduce0.96140951 and1.06111690. Independent channel
decomposition gives H0.02138267, L0.04743757, V31314.13760614 and cross sum
about-0.24649417, reproducing the extreme Q. Thus the large value belongs to
this actual functional of the released channels and is Virgo-dominated.
Its physical/instrumental cause is not identified; metadata quality does not
prove stationarity or quietness. The record was retained throughout.

At h_rss=1e-21 strain sqrt(second), normalized on the90s core before Hann,
direct recomputation of all504 background/waveform additions gives:

| Inclusive synthetic band | Strict crossings /168 | Required |
|---|---:|---:|
|30--500Hz|5|152|
|30--100Hz|3|152|
|100--500Hz|3|152|

All three complete frozen amplitude curves independently match. At1e-19,
each has8/168 crossings. Direct target additions agree with independent
quadratic evaluation within6.17e-15 relative;18 full raw-channel V inverse-delay
injections, including the extreme background and upper grid endpoint, agree
within6.59e-15. The smallest target decision margin is3.10e-8 of threshold,
well separated from the observed numerical discrepancies. Saved cross and
signal quadratic coefficients agree within6.41e-14 and6.30e-15 relative L2.

These reused-background fractions are descriptive finite outcomes, not
independent Bernoulli trials, population detection power or confidence.
Rank1/22 would require a separate exchangeable noise-only statistic conditional
on training; neither that condition nor selection-corrected coverage is proved.
The algebraic beyond-grid roots are checked threshold-equality roots/strict-
crossing infima, not directly injected trials or a second decision rule.

## Argument, defect and repair

Source-first reconstruction established the finite all-vectors identity:
on the zero-DC/Nyquist image, cyclic alignment inverts the supplied delays,
constant F commutes with that projection, and bF=0 annihilates both arbitrary
tensor functions before common crop/taper. This is finite algebra, not an
empirical inference from passing injections. Static cyclic boundary data do
not establish physical periodicity, finite-arm/rotating response, calibration
coverage or upstream signal retention. An alternative in col(F) is invisible.

Independent dense-DFT and full-size source-first controls reject wrong delay
sign, omitted H coefficient and premature taper. Full-size correct relative
residual is3.25e-16, versus0.831 and0.334 for the two principal defects;
the invalid zero assertions actually fail. Norm/scaling checks avoid an
absolute tolerance that would accept any physically tiny strain. All24
source-defined waveform norms and V inverse-delay round trips were checked.
Direct Fourier-sum anchors independently match FFT within2.83e-14.

R1 fixed a real mismatch: floating labels29.999999999999996 and
99.99999999999999 excluded the mathematically inclusive lower bin. The missing
bin changed PCG64 draw counts/assignment, so initial4/168,3/168,4/168 counts
were not the frozen experiment. Exact integer membership restores
46061/6861/39201 bins. Original candidate/source, coefficients, outputs and
initial review survive byte-identically. Only synthetic()/the output filename
in evaluate() change function definitions; the core-band membership is
independently unchanged. Seeds, draw order, freeze, data, PSD, query, target
and stopping rule remain fixed. Reinserted legacy masks and defective null
operators actually fail their guards in this review's same-code replays;
those reruns are regression evidence, distinct from the independent pipeline.

## Execution, exposure and limits

Review source definitions, upstream proofs/verdicts and public event identity
were exposed before sealing; FW2 proof/code/output and the permitted samples
were exposed afterward. This is fresh-context, source-first, independent-method
review using the same data and specified NumPy PCG64 generator. Shared FFT
software families, supplied F/delays and datasets remain shared foundations;
different implementation is not a formal proof or independent instrument.

Review runs used the inspected existing run_capture.py, SHA
8ff5469ace76bdfc84188915242abbf3baff35516f9ee3f9ba4b1cbfeb2573ef,
with512MiB AS/60s CPU/wall, CPU float64/complex128, no GPU/install/download,
one numerical child at a time. OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1
were set; author catch replays also set MKL_NUM_THREADS=1. Each saved run.json
records the exact command, cwd, timing, limits and peak; stdout/stderr remain.
Final independent replay exited0 in6.795974s, peak203596KiB, empty stderr,
no timeout, Python3.10.12/NumPy2.2.6. Focused preservation/root and actual
author endpoint/null catch replays also exited0.

Failures remain evidence: reviewer JSON serialization, initial synthetic
mismatches, and a reviewer large-angle trigonometric accuracy failure are
preserved with their sources. Exact modular phase reduction repaired the
last from2.81e-10 to2.83e-14 without changing the Fourier sum or1e-10 tolerance.
The author's two overlapping R1 launches both returned-9 near59.45s; records
substantiate the overlap. This operational deviation is disclosed, not erased.
Serial single-thread retries passed without scientific changes. No unproven
cause is assigned. Failed CLI exit0 is not counted as a completed review.

Not repeated: FW1 metadata/calibration-source parsing, CO1/CO2 theorem and
astrometric derivations, upstream physical retention tests, physical response
model construction, full349 audit, stationarity/coverage proof, new validation
data, or event analysis. The inspected saved full349 audit is PASS/exit0,
399.424107s, SHA f775459039552d8604e4f9efd1777217611506b6e872c1f75d898cda5f513d38;
review does not upgrade its sources or the registry.

HEAD independently remains grok/b11fcea356f60dfdeee38843bff46d626fbc8295.
Parent-owned tracking dirt and unrelated local work were preserved. This
review changed only step_02/review; no git mutation, protected-payload mining,
GOCE work, correspondence, physical adoption, grades/canon/manuscript change,
or host-wide process/remote-freshness claim. The review closes within70minutes.
