# Exact original-metric check plan

Frozen before execution. Question: do direct differentiation of the physical
four-metric and actual proper-clock histories give the claimed radial null
frequencies, held-clock accelerations and echo factors? This is a finite
algebraic verification of stated formulas, not a numerical discovery sweep.

Input frame: g=Omega(t,r)^2 diag(-f,1/f,r^2,r^2 sin(theta)^2), f=1-2m/r;
r>2m>0, Omega smooth positive, regular angular chart. Schwarzschild reference
is a supplied GR comparison, not UDT-selected geometry. All parameters and
Omega are free-and-explored. m and H/beta are symbolic, not fitted scales.

Check count: one held-clock normalization; four acceleration components;
two null norms; eight original affine-geodesic residual components;
two frequency readouts; one echo product; two reference-leg contrasts;
one independent proper-history derivative; one echo/tidal-weight identity.
Total 22 exact symbolic zero identities. One separate exact exponential
false-positive witness H=1,beta=2,L=1 has echo>1 and return contrast<1.
Dimensionless witness values are controls, not scientific constants.

The Christoffels are built directly from the 4x4 metric, not imported from the
analytic conformal-connection formula. The proper-history derivative is built
from an antiderivative of the actual held-clock lapse for H!=0; its H=0 limit
is continuous. No numerical tolerance or sampling inference is involved.
The Weyl scalar's transformation weight enters only an algebraic echo check;
this script does not recompute full curvature or certify that theorem.

Omissions: nonradial paths, global/horizon behavior, empirical calibration and
noise, reference reconstruction, physical attribution, field/source dynamics.
Maximum claim: exact symbolic regression of these scoped identities. The
analytic proofs and later separate-context review remain distinct.

Resources: one CPU process, BLAS threads=1, 2GiB virtual memory via existing
TPS1 capture.py, tiny JSON/text outputs, no CPU/wall killing timeout, manual
interruption authoritative. Expected seconds; request parent slot before run.
Capture uses unique prefix researcher_a/runtime/echo_check; output refuses
overwrite. Preserve code, plan, JSON, stdout/stderr, versions and input hashes.

Command after slot approval:

    python3 udt_time_live_production_survey_2026-10-01/capture.py --memory-mib 2048 udt_positional_effect_assignment_2026-10-13/researcher_a/runtime/echo_check python3 udt_positional_effect_assignment_2026-10-13/researcher_a/check_echo.py
