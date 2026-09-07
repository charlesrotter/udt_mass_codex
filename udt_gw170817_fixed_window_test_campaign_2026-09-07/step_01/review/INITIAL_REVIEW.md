# FW1 initial adversarial review

2026-09-07 23:07 UTC. Fresh separate-context reviewer `/root/fw1_release_review`;
exact model UNKNOWN; other-model/human/formal axes UNTESTED. Source-first seal
3928ce7fb67a5a44e379bbdd365203cc000177c9421905b5373c76079b0dd623 preceded
FW1 target exposure. Candidate first read after the parent's23:04UTC seal notification.

Pinned initial CANDIDATE SHA
5cf764588c4b2abc627d89b7256837ad60975e61068bb93af8b83f0f4a139b08;
FREEZE SHA05a3fdfc8920e4255603696d0abc3a98fc388b09645647b8aee468a500cb8b7d;
metadata_filtered_run.stdout SHA
9e6c1d6fa98e14e0b2c060e18d4e7b46aacc35890aff46c51474ca03ce1f74af.

The narrowed off-source finite-statistic scope is sound, subject to one grouped
R1 freeze-completion repair before strain exposure. No physical-premise,
release-identity or finite-model algebra objection was found. R1 does not
require expanding the measurement model or finding all missing physical bounds.

## R1: fully specify numerical controls before observing backgrounds

The proposed fixed24 synthetic waveforms are load-bearing for the descriptive
crossing fractions and stopping rule. Seed base352170817 alone does not select
them: NumPy RandomState versus Generator, generator family, stream reuse versus
per-draw reseeding, and real/imaginary draw order all produce different arrays.
The smallest repair is an exact generator/seed/draw-order convention and
normalization formula in the freeze before any off-source sample is read.

Likewise specify h_rss=sqrt(sum_n (C s)_n^2/fs). The text's physical units imply
this, but an unweighted Euclidean normalization would differ by sqrt(fs)=64.
No source amplitude is being inferred; this is the supplied effect-size query.

The PSD positivity check must inspect the pre-floor estimate and record any
floor use. Positivity after max(S,1e-60) alone would be a tautology, unable to
detect a failed estimator. Freeze the response if pre-floor values are invalid,
and report floor activation; a finite declared floor is a legitimate control.

Freeze scale-normalized residual/difference checks. A broken1e-22 strain signal
can pass an absolute1e-10 tolerance. The current name numeric_relative_tolerance
points in the right direction but needs an explicit scale/norm and zero-scale
handling. These concerns are prospective guard defects, not claims that an
unwritten FW2 implementation already contains them. Code and actual defect
reinsertion remain an FW2 gate before its outcome claim.

Survivor: exact release match; reproducible metadata selection; exact finite
cyclic/static null algebra; legitimate predeclared off-source reinjection
screen with no population-power, event-significance or domination claim. Preserve
initial candidate/freeze bytes and complete the numerical specification in one
source-preserving repair; then focused re-review suffices.

## Independent evidence already obtained

All three completed files' streaming SHA256 and MD5 match the producer record
and official checksum rows. Independent h5dump text parsing verifies start
1187008512,4096s duration,16777216 samples, and exact Xspacing0.000244140625.
Actual source-channel/frame metadata match H/L C02 and Virgo Repro2A. This exact
rate evidence is stronger than the producer's rounded-spacing substring guard.

The independently decoded core masks are DQ127 for90s in all three detectors;
H/L injection23 throughout4096s and V1 injection31 throughout. Source bit3 means
NO_CW_HW_INJ, so H/L are not injection-free. Candidate retains the CW background
and makes no astrophysical residual claim. Independent98s-support reconstruction
reproduces36 proposals, exclusions9316/10516/11916 (full GPS in saved output),
33 survivors, first12 training and21 reference. Rank resolution1/22 is only
a conditional exchangeability fact, not supplied coverage.

Standard-library calibration archive parsing independently finds H1 preceding
1187007982 and following1187008882; L1 preceding1187008729 and following1187008882.
The chosen common event epoch is nearest to the core midpoint. All inspected
records have100 rows5–5000Hz,41 sampled rows30.679536–500Hz. The band values and
true/model versus model/true distances agree with the candidate. These are
sampled pointwise estimates, not hard, continuous or joint uncertainty bounds.
Swope's explicit J2000 label and its stated centroid/WCS standard uncertainties
were independently read. They do not certify the original GCN query's complete
detector-frame/finite-arm response.

The finite identity follows directly: on the zero-DC/Nyquist image P, cyclic
shifts A_i are invertible and commute with P; constant F_i acts on two waveform
components and preserves that image. Hence A_i P A_i^{-1}(F_i h)=F_i h, and
C sum_i b_i F_i h=0 because bF=0. A common crop, taper and DFT preserve zero.
This argument allows every vector h in the declared finite domain and does
not supply continuum/time-dependent/finite-arm response or physical periodicity.

Separate exact finite counterexamples give2/3 spurious residual when a common
smoothing operator is applied before a varying response null, and nonzero
residuals when tapering precedes an unequal delay. The invalid zero assertions
were actually executed and failed. These are reviewer finite controls, not a
catch-proof of nonexistent FW2 producer code. Candidate correctly avoids both
universal physical claims and an unsupported bound on a different improved test.

No observational samples, PSD, target contrast, protected payload or GOCE
evidence was inspected. No git mutation, physical adoption, accepted grade,
canon or fixed-manuscript change. Full349 audit record was inspected and hashed
f775459039552d8604e4f9efd1777217611506b6e872c1f75d898cda5f513d38:
PASS/exit0,399.424107s,empty stderr,no timeout,2GiB/900s. Not replayed here.

Reviewer diagnostic history is retained: initial h5dump showed a truly partial
H1 file, later completed by parent; initial metadata text parser failed on
HDF5 null-padded string names and was repaired without changing mask predicates.
Original reviewer code and failed run survive. These were pre-target diagnostic
issues, not repairs of candidate science. All short review runs use existing
run_capture.py,512MiB AS/60s CPU/wall,one CPU child at a time,no GPU/install.
