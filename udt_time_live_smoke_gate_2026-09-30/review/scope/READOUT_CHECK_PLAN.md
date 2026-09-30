# Narrow saved-clock correspondence check

After the first smoke result disclosed only a comparison error, the parent
accepted the request to retain actual marked outputs. Before reading the repaired
outputs, this reviewer will check the committed initial/final float64 arrays
without importing the runner or checkpoint implementation. Independently verify
metadata and payload SHA-256, construct real trigonometric interpolation weights
directly (no FFT), and evaluate central R12N's endpoint formula for te=1,to=4,
the supplied positive longitudinal branch d=3 and fixed-coordinate clocks.

Compare retained per-case sampled logZ/Z readouts to those values. Agreement
within 2e-12 absolute logZ and 2e-12 absolute Z is sufficient for this float64
correspondence check; no continuum-extremum or independent-dynamics claim follows.
This repeats neither NGD1's Ricci audit nor its independent evolution. Its only
purpose is to check that the new operational report faithfully reads its saved
checkpoint states and marking. Existing outcomes were exposed; repaired readout
numbers have not yet been inspected.

No GPU. CPU <=180 seconds/2 GiB. Record exact input paths, hashes, arrays, versions
and execution output under review/scope/. Preserve all attempts. This plan is an
additional bounded correspondence check, not an expanded physical premise.
