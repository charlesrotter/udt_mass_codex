# Source-first check freeze

Question: do the independently derived reciprocal-tube algebra and proper-clock
variation retain the factors, affine normalization and arrival terms required
by FCV1? Exact finite symbolic controls; no claim that arbitrary symbolic clock
maps are realized by a metric or that checks prove geometric regularity.

Plan frozen before running source_first_checks.py: check the reciprocal trace,
null contraction, exact Lorentz2 family tangent/determinant, affine cancellation,
moving-arrival derivative, moment derivative, integration-by-parts expression,
and the Minkowski proper-rapidity anchor. Reject omission of the D_s term,
failure to differentiate omega_o, omission of the reciprocal factor two, and
omission of the weight derivative using explicit nonzero algebraic differences.

Inputs pinned in SOURCE_PINS.json. The independent script imports Python/SymPy
only. One CPU process/thread, 60 seconds wall/CPU, 512 MiB address space, no GPU,
no grid, no observations. Existing unchanged run_capture.py captures stdout,
stderr and resource receipt. Stop after these anchors and source-first report;
actual producer and integration review require the parent dispatch.
