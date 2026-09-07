# FW2 initial adversarial review — one grouped repair requested

2026-09-07 23:36 UTC. Fresh built-in reviewer
`/root/fw2_fresh_capacity_check`; exact model UNKNOWN. Source-first seal
preceded all FW2 target and observed-sample exposure. Human/formal/different-
model axes UNTESTED. This is not scientific promotion.

Verdict: the initial synthetic generator's fidelity to FW1's inclusive-band
freeze is REFUTED. The final FW2 verdict is unresolved pending the one allowed
same-premise repair/re-review. The large reference statistic and resulting
failure of this particular procedure survive independent recomputation.

## R1 — inclusive endpoint omitted by floating frequency comparison

The initial screen.py synthetic() computes active=(f>=low)&(f<=high), where
f=scipy.fft.rfftfreq(401408,1/4096). Although the exact frequency is k/98,
the displayed floating labels are f[2940]=29.999999999999996 and
f[9800]=99.99999999999999. Thus all three bands omit their frozen inclusive
lower endpoint. Counts are 46060/6860/39200 instead of 46061/6861/39201 for
30--500/30--100/100--500 Hz. The actual false assertion and exact-integer
repair demonstration are saved in bin_edge_diagnostic_run.*.

This is not merely a negligible one-bin energy issue: changing active-bin
count changes the seeded real/imaginary draw split and waveform assignment.
The source-first integer-bin independent generator produces target counts
5/168, 3/168, 3/168, versus the initial reported 4/168, 3/168, 4/168. Other
grid entries differ as documented in independent_initial_complete_anchor_repair_run.stdout.
All 504 corrected-definition target additions were recomputed directly in the
time domain, agreeing with the independent quadratic values within 6.17e-15
relative. Eighteen actual V inverse-delay/raw-channel injections, including
the extreme reference and grid upper endpoint, agree within 6.59e-15.

Smallest source-preserving repair: preserve initial candidate, generator,
evaluation/coefficients/method/catch outputs and ready pins; choose active
bins by exact integer inequalities for k/98, with both inclusive endpoints;
retain the identical frozen bands, seeds, draw order, normalization, source
records, PSD, sky/delays, statistic, amplitude grid/target and decision rule.
Recompute affected synthetic/method/catch/evaluation outputs and update their
numbers and provenance. Add an actual endpoint-membership/count guard with
the original floating mask reinserted and rejected. Do not re-extract, retune,
delete an inconvenient record, alter the freeze or open the event.

Minor same-repair wording: if retaining the algebraic roots beyond the frozen
grid, describe them as threshold-equality roots and the 90% crossing infimum;
strict Q>threshold is not guaranteed at the equality root itself. These
diagnostics remain outside the directly injected grid and unnecessary to the
declared stopping result. No new search or amplitude grid is requested.

## Independently surviving result and checks

All 99 saved allowed extract hashes, sizes and declared supports match the
three manifests and exact 33 FW1 starts. No support intersects the event
exclusion. The source-first replay uses full complex FFTs, a hand-segmented
Welch estimator, determinant-derived b, and a covariance polarization identity;
it does not import author screen.py or scipy Welch/csd. Shared supplied source
data and PCG64 definitions remain shared inputs; this is not a different dataset.

The independent mean PSD matches to 3.57e-16 relative L2 and at most 2.84e-13
pointwise on retained bins. No floor activates; minimum retained physical PSD
is 2.96248e-46 strain^2/Hz. Polarization-identity covariance reconstruction has
maximum relative error 7.14e-16; actual band cross-term fraction is 2.74698e-5.
Every reference Q agrees within 7.94e-15 relative. The same record at core
1187011516 sets Q=31313.959932212096, with maximum/minimum 34778.94553.
The ordinary reference at core1187010216 gives Q=0.9388275248150578.

Independent channel-energy decomposition of the extreme gives H0.02138267,
L0.04743757, V31314.13760614 and cross sum approximately -0.24649417,
reconstructing its Q. This is an actual property of the selected functional
of released channels, dominated by the Virgo contribution; physical cause
is OPEN. Neither DQ nor these calculations certify stationary noise.

Each source-correct target family still fails the required 152/168 crossing
count by a wide margin. At the frozen grid top, each gives 8/168. These are
descriptive reused-background fractions, not population detection power or
confidence. No alternate statistic/full operator is bounded by this failure.
The event stays UNEXAMINED; physical response/upstream/calibration gates remain
OPEN. No empirical UDT, physical-content or metric-history conclusion follows.

## Reviewer diagnostics and preservation

Initial dense-DFT synthetic checking failed only on JSON serialization of a
NumPy boolean; original source/output are preserved and the representation
was repaired. Two observed replays intentionally stopped on synthetic-fidelity
mismatch, preserved before completing the diagnostic. The first complete
replay then stopped at the reviewer's direct trigonometric-sum accuracy guard:
unnecessarily large phase arguments lose precision for a weak selected bin.
The original independent operator is preserved. Exact integer modular phase
reduction repaired that method without changing its Fourier functional or
loosening 1e-10; direct-sum/FFT anchors now agree within 2.83e-14. These
reviewer failures are distinct from the author endpoint defect.

Successful complete initial diagnostic used 512 MiB AS/60 s CPU/wall,
6.806951 s and 206100 KiB peak, no timeout/stderr, Python3.10.12/NumPy2.2.6.
Exit0 means this diagnostic completed; its author_synthetic_fidelity_pass is
explicitly FALSE, not a review pass. Exact commands and versions are saved.

Initial candidate SHA256 d4ec21b1cab3fd8672f7b4b2be8bf67d78e5f460bd78930fbafe386baa458f82;
screen.py fa865d46e6b728d2ac978e962067260ea4e9052d8f1b17f0e01a6f523de23ba2;
evaluation 6d8abeba36f7c4d26983bdde1a5343158bf3678ca77079cac1e547fff69e9bc8;
PSD 6cf4c75cac9a38318311da37a16de0bb6b7c629643d52008b2eb2b8b70b758ea;
coefficients 6b3406738442832c25286cdf7abce2a8e8c64b728963bc4b97ed10a3189b7932;
ready 442f39011dfeb553a4b03a77908e2f444272767a8366a8b26c4e9bd33e296b0e.
The FW1 freeze remains fa0506eaea5ef20dcd92aabf3b2d1a0efc7fb75ef6c7272c00e5e6764c591324.
