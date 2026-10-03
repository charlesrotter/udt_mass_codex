# CPW1 geometry: finite control freeze

Status: frozen before the one permitted CPU control. This is a contributor
check, not review of the parent synthesis or scientific promotion.

Question: can the outgoing clock ratio alone determine the actual immediate
return ratio when the admitted proper-clock query allows acceleration? This
is deliberately outside ESR1's free-clock PSW preparation, so a counterexample
here cannot refute ESR1 or FC on that restricted preparation.

Metric-led frame: supplied Minkowski metric, signature (-+++), c_E=1 units,
one spatial line, B at x=L>0, emission at t=0. Two free-and-explored mathematical
control worldlines for A are x=0 and x=t^2/(8L). L is a symbolic query length,
not a chosen physical scale. Proper time remains ordinary. The second curve
is timelike on |t|<4L. Outgoing and returning rays are the actual future null
segments, with immediate timing relay at B; no optical reflection or emission
energy law is assumed. No physical UDT admission is inferred for either control.

Freeze: independently differentiate outgoing and return null incidence with
proper-time conversion and compare the endpoint frequency contractions. Verify
the return root, its chronology, timelikeness, and the unequal return ratios
with the same p=1. Two control families/cases, at most30 scalar assertions,
exact SymPy arithmetic; no fit, grid, numerical tolerance or random sample.
These checks corroborate the displayed elementary proof, not an all-metric claim.

Resources: one CPU child under existing TPS capture.py, 2048MiB virtual address
limit, one BLAS thread, no wall/CPU timeout, finite symbolic expressions, no GPU,
outputs under this geometry directory, well below100MiB. Natural exit or manual
interrupt stops the check; preserve any failure and do not launch an automatic
repair/retry. No protected payload is accessed.

Exact command:

    python3 udt_time_live_production_survey_2026-10-01/capture.py --memory-mib 2048 udt_clock_law_physical_whiteboard_2026-10-03/geometry/control python3 udt_clock_law_physical_whiteboard_2026-10-03/geometry/independent_control.py

Omissions: no ESR/IEC universal proof replay, field equation, inverse metric
reconstruction, physical positional attribution, empirical comparison, GPU or
new premise audit. The parent owns the closure premise audit.
