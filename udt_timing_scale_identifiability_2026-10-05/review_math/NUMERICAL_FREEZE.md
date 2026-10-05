# Source-first numerical freeze

Before running confirmation, use independent mpmath50-digit inverse-radius
quadratures and implicit incidence solves, no parent functions or output.
Metric-led free-and-explored controls: m=1,a=8,H=.02,E=1.3;
b_*=0,2,-3; x=1e-3,1e-4,1e-5. Each central case plus x(1+-1e-5)
gives27 actual-incidence solves. A matched lambda=3.7 solve for each central
case adds9, total36 finite cases. All failures and reruns count; remaining
budget64/100 reserved for scoped diagnostic/replay. Source phases are chosen
by the limiting incidence; this supplies preparation rather than fitting data.

Compute frequency from outgoing metric formulas, exact original incidence
residuals, source time, receiver direction and optical J. Estimate dlogZ/dell
by a centered x difference times -x w, with full re-solving of incidence.
Verify normalized incidence<=1e-35, unit direction error<=1e-35, homothety
relative invariance<=1e-30, finite derivative agreement with an independently
differentiated implicit branch<=2e-8 relative. For each b_*, require late drift
at x=1e-5 within1% ofH and late errors smaller than at x=1e-3; this finite test
is supporting agreement, never the proof of a limit. Save all inputs and
solutions. Parent saved-output recomputation is a later frozen stage.

CPU only;2GiB address-space cap; one BLAS thread; no CPU/wall timeout; no GPU;
output expected<1MiB. Stop on first implementation/numerical failure after
saving diagnostics. Inspect equations, residuals and numerical control before
any bounded same-premise repair. Do not widen physical scope or discard failed
runs. No long production or empirical calibration.
