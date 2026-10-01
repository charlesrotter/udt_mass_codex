# TDS1 frozen short-history checks

Exposure: exact-control development tests and the N8 seed's independent residual
were seen before this freeze. They are development evidence, not blind predictions.
The first GPU invocation failed before evolution because deterministic CuBLAS
requires CUBLAS_WORKSPACE_CONFIG=:4096:8. Its stderr/receipt is retained; the
same equations passed with that runtime setting. The daemon then restarted;
completed artifacts were verified and preserved. Original review contexts were
lost, so new actual contexts explicitly attribute their saved evidence.

The three-axis seed uses the same declared amplitudes at every mesh. Report
histories at N8,N12,N16 with dt=.005, and N16 with dt=.0025, all t=1..1.1.
Also save a curved homogeneous Kasner control at N8 with both timesteps.
Harmonic coordinate elapsed time is s=t-1; proper Kasner time is exp(s), not t.
No survey outcome has been seen. g,v are stored at every step; the code imposes
no spatial symmetry during evolution. Period2pi and seed restrictions remain.

Runtime guards at every saved state: finite data, positive spatial metric and
negative inverse g00, original ADM Hamiltonian/momentum and harmonic residual
each <=2e-5, allocated GPU memory<=4GiB and output<=128MiB/run. Failed states
remain diagnostic-only. Run exact code/spec signatures through the previously
reviewed immutable checkpoint format. Check initial/resumed states as well as
evolved states, including already-complete endpoints.

Post-run checks: independent original Ricci from five-point saved-metric time
differences and spatial differentiation (not the producer's acceleration), at
multiple interior times/space points, maximum component residual<=2e-5. Compare
refinement at identical marked events. Original residuals should decrease by at
least10x from N8 to N16 unless all values are already <1e-9; otherwise return an
unresolved convergence diagnostic. N16 timestep halving must change final g/v
by <2e-7. Kasner final g/v must agree with exact values within2e-7. These are
finite numerical thresholds, not rigorous continuum error bounds.

Fresh-process pause/resume and actual SIGTERM after a committed checkpoint must
produce bit-identical final g/v against uninterrupted execution. A bounded wall
stop must return CHECKPOINTED_STOP with valid saved evidence. Retain corruption
and invalid-state protection inherited from reviewed checkpoint I/O; assess new
shape/equation guards explicitly. The small suite does not certify all crashes.

Null/clock readout uses supplied fixed-coordinate timelike clocks. Integrate
null geodesics from stored full metric with time interpolation disclosed; compare
at least a homogeneous axis-aligned Kasner query against its exact frequency
ratio. Record emitted/received events, direction, normalization, null residual
and sampled Z. Calculate a corresponding three-direction-history readout with
refinement; never identify these supplied observers with cosmological observers.
No sign/shape of Z is an acceptance target for general data.

The representative short workload is the N16 full-metric run including current
every-step diagnostics/output, not a production-speed prediction. Record exact
wall time, peak memory and output. A multi-hour dispatch remains gated on useful
case/mesh/time coverage, output cadence, reviewed long-slab controls and actual
resource sizing. The five-minute summed GPU ceiling in WORK_ORDER remains.
