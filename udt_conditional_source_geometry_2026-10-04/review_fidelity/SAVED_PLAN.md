# Saved-artifact recomputation freeze

Exposure now additionally includes repaired check_construction.py,
CONSTRUCTION_RESULT.json, CHECK_REPAIR.md, REPAIRED_CHECK_FREEZE.json, and actual
original/diagnostic/repaired capture receipts, stdout/stderr. The diff of frozen
INITIAL_CHECK.py against the current checker is exactly the one denominator
repair described in CHECK_REPAIR. No other reviewer implementation or result
has been read. Mathematical/source-first work and both independent checkers
predate this implementation exposure.

Before execution freeze saved_checks.py and all input hashes. CPU, 2 GiB,
one BLAS thread, no timeout. Use only 60-digit mpmath arithmetic. Recompute all
40 stored endpoint contractions and receiver sky directions from metric/tetrad
vectors; tolerances 1e-28 for 36-digit records and 1e-50 for 60-digit records.
For the four 60-digit midpoint rays independently use Gauss–Legendre quadrature
(parent used default tanh–sinh) to recompute both incidence equations, arrival
proper time and the implicit-map determinant; absolute tolerance 1e-45.
No root solve or new parameter tuning. Recompute both already-frozen arrival
difference steps and spectral drift at all eight precision/query groups; retain
the parent's 1e-7 accuracy and .4 contraction bounds. Add analytic implicit-map
drift at the four midpoint rays and compare to the saved finite-difference
spectral slope with 1e-7 tolerance. Reproduce the original extra-denominator
defect and require it exceed 1e-4 in the original first case.

These forty saved cases plus fourteen earlier exact cases total fifty-four
finite cases for this review implementation. Midpoint/step reuses are the same
cases, not a new survey. This is independently reconstructed postprocessing,
not an independently solved complete ray family or interval-certified quadrature.
