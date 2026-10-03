# CBR1 pre-execution smoke

Metric-led diagnostic only. Parent forward.py uses actual exponential preparation,
parallel transport, conserved spatial momenta for timelike geodesics, quadrature
of conformal null incidence and endpoint frequency ratio. Source-first math
review supplied matching equations while parent reasoning was unsealed; no blind
parent discovery is claimed. No leading curvature formula generates log p.

Smoke controls: flat and supplied cubic a=1+.03t³ at t=0, L=.02,.01,.005,
v=3/5; three unique isometry classes (rest, boosted-longitudinal,
boosted-transverse). All21 frame/direction labels in a homogeneous isotropic
geometry reduce to these three solves, not21 independent forward simulations.
Flat clock shifts must be <1e-11; prep norm and null incidence <2e-10 and2e-11.
The cubic t=0 case has R=0 with nonzero time derivative; no recovery threshold
is asserted before measuring finite-separation behavior. The smoke must also
read serialized observations through the separate inverse estimator, demonstrate
domain-stop behavior, and compare coarse/fine numerical settings.

Float64, SciPy1.15.3 DOP853; coarse rtol2e-12/atol2e-14, fine3e-14/3e-16;
16/32-point Gauss-Legendre quadrature; root absolute5e-14/5e-15, rtol1e-14.
Preparation step at most L/4. Positive-history interpolation uses supplied
ERC1 ODE and max time step .02/.01 on[-1.5,1.5]. Smoke does not run the main
variable-curvature positive case or select fitting/noise thresholds from it.
No GPU, real observation, field-law adoption or elapsed cutoff. Existing
capture2GiB/oneBLAS; finite query100000/iteration100/domain limits remain.
Budget and main grids/tolerances are fixed after actual-workload sizing and before
main outcome exposure. Preserve every failed smoke rather than silently replace it.
