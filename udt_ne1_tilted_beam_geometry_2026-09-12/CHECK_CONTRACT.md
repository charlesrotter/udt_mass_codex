# NTB1 candidate verification freeze

Freeze after reading discovery232 states: no negative sampled areas, max scaled
screen error2.21e-12, max scaled symplectic error7.13e-12. This is disclosed exposure,
not a blind confirmation sample. No independent reviewer result beyond source-first
ODE/no-root and original-geodesic summary was received before this contract.

Verify INITIAL_CANDIDATE.md (1)--(13) with the original source equations and analytic
hypotheses. Independent review owns its source-first original-Christoffel trajectory
and finite-angle implementation. Parent confirmation reuses discover_beams.py's
field/Hessian implementation and is explicitly regression/consistency evidence.

Parent controls:
- complex-step (1e-25) differentiation of original reduced flow versus analytic Hessian
  at three nondegenerate states, max absolute discrepancy<=2e-8;
- direct backward integration along three finite segments (positive/negative oblique,
  mixed/pure transverse) at epsilon=.5, endpoint8, source xi=.7 or0;
  forward/backward flow scaled error<=2e-7 and source-normalized area reciprocity
  relative discrepancy<=2e-7;
- endpoint observers with independently chosen velocities (0.2,-0.1,0.15) and
  (-0.15,0.25,0.1): Lorentz-frame source-sky differentiation, quotient target
  projection and direct Gram determinants; area/frequency transformation <=2e-7;
  these are G348 regression checks, not a new native reciprocity proof;
- epsilon0 oblique width/area from independent quadrature of spatially homogeneous
  Hamiltonian derivative, scaled discrepancy<=2e-7;
- invariant source xi0, epsilon=0,+/-.5,1, psi0,pi/4,pi/2, endpoint40: independently
  integrated positive auxiliary system/quadrature versus full variational widths,
  scaled discrepancy<=2e-7; source normalization checked in actual widths;
- one exposed worst discovery screen case repeated with rtol2e-11,atol2e-13,
  step0.1; scaled state/map/output agreement<=2e-6;
- pure transverse long-reception illustrations at epsilon=+/-1/6,+/-.5,
  psi0,pi/2; t=10,40,100,400. The proof, not finite trends, owns (12)--(13).
  Integrate auxiliary-system/quadrature with rtol2e-10,atol2e-12,step0.2;
  repeat epsilon=.5,psi0 with tighter controls. No infinity certificate.

Actual hostile runs, each must exit nonzero with named reason:
drop_spatial_hessian against discovery screen orthogonality;
drop_source_lapse against invariant widths;
wrong_reverse_normalization against directional area reciprocity.
No full production replay required without change/failure. Preserve all outputs.
CPU float64, SciPy DOP853/QUADPACK, one thread, <=180s/2048MiB per capture.
No interval certification, formal proof or physical observational check is claimed.

Chronology correction: CANDIDATE_FREEZE.json's 'discovery run running' meant its tool
session had not been collected. Capture now shows execution finished22:00:07,
before candidate freeze22:02:58; its output content was first read22:03:27.
No hash claim supplies independent chronology; original receipt remains preserved.
