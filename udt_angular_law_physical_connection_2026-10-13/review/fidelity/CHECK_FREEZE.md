# Fidelity complementary check freeze

Question: for one fixed Lorentz boost, do independently integrated emission and
reception uniform-sky log means have opposite signs, and does carrying the actual
angular Jacobian recover the reception mean? This probes the load-bearing
measure/physical-attribution distinction in ALP1 section 2.

Candidate exposure: SOURCE_FIRST.md preceded exposure; now read joint candidate,
A/B candidates, B provenance/freeze and saved exact-run output/receipt. B checker
source was not read, imported or run. The method here was independently proposed
in SOURCE_FIRST and implemented below after candidate-formula exposure.

Equations are derived from a +x boost of l=(1,n): with x=n_x,
f=cosh(rho)+sinh(rho)x, y=(sinh(rho)+cosh(rho)x)/f,
p_emit=1/f, p_receive=cosh(rho)-sinh(rho)y, dy/dx=f^-2.
The normalized axisymmetric measure is dx/2 or dy/2 respectively. Test rho in
{0.25,0.8,1.5}; use the zero-boost unit-ratio control separately. Simpson grids
1024/4096/16384 over [-1,1], Python float64-like binary double and math.fsum.
Compare the direct reception integral, direct emission integral, carried
reception integral and direct normalization against elementary antiderivatives.
Finest absolute tolerance 2e-10; report every grid result. This is floating
quadrature confirmation with refinement, not interval certification or a proof
for every boost. Analytic derivation belongs in DIRECT_REVIEW.

False-pass probes: omit the Jacobian and require a sign-opposite answer; substitute
the inverse Jacobian f^2 and require failure of normalization by at least 0.01
at every nonzero boost. No candidate code is used. No clock-ray integration,
FAC1 theorem recomputation, instrument claim or physical law is tested.

One process, one BLAS thread, 2GiB address-space cap, no GPU, no timeout;
expected <60 CPU sec, <100KiB outputs. Parent authorized this launch; at most the
math reviewer can run the second scientific process. Stop on failed assertion;
preserve stdout/stderr/receipt without automatic repair or overwrite.

Exact command from repository root:

    python3 udt_time_live_production_survey_2026-10-01/capture.py --memory-mib 2048 udt_angular_law_physical_connection_2026-10-13/review/fidelity/checks/boost_measure_01 python3 udt_angular_law_physical_connection_2026-10-13/review/fidelity/check_boost_measure.py
