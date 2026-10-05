# Saved parent-state replay freeze

Parent NUMERICAL_FREEZE.md and CONSTRUCTION_RESULT.json schema/results have
now been read. Parent implementation has not been read or imported. Replay
the 25 high-precision saved incidences by independent direct quadrature of
original equations and exact readout formulas at 90 digits. No root solving
or copying parent derivatives: compute them anew from the saved state and
owned equations. Independently integrate proper time in log radial coordinate,
including E=10. Check stored B, b_x, t_e, Z, logZ, K, angular direction and rate.
Tolerance 1e-55 for residuals and 1e-50 relative/absolute-scaled readout error.

Recompute all finite midpoint-window certificates and sign-aware H intervals,
including E=10 long interval and angular separation. Verify the parent result
is attached to this exact frozen candidate/output snapshot. Two corruption
controls replay one saved case with R multiplied by1.001 and b multiplied by
1.01; require nonzero original proper-time/incidence residual respectively.
These controls consume two additional cases and are not physical countermodels.

Prior cases36; this pass25+2; cumulative63/100. CPU2GiB1BLAS, no timeout,
capture.py, small JSON. Preserve failed outputs and stop on unexpected failure.
No empirical/native interpretation is tested or established by this replay.
