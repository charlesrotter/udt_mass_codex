# OB1 frame, exposure and pre-computation plan

Recorded after orientation and the new actual full397 PASS, before any OB1 scientific script.
Baseline grok=origin/grok 4c56085101da045b8d00732528bb6f99ed0fd8e2; no tracked dirt.
Configured gpt-6-astra/xhigh was read from config; runtime identity/version UNATTESTED.
Parent startup capture: /tmp/udt_optics_startup_2026-09-12T133125/premise397.*,
started13:33:22.857289UTC,404.541622s,exit0,120192KiB; it is this session's result.

Metric-led conditional frame: use G405's supplied smooth stationary
g=-N^2(dx0+beta_i dx^i)^2+gamma_ij dx^i dx^j, x0=c_E t, N>0,gamma SPD,
marked U=N^-1 partial_x0, and one closed spatial loop with emitter/detector D at rest.
Require gamma-N^2 beta beta^T SPD on the loop for simple positive coordinate traversal.
N,beta,gamma,loop and witness parameters are free-and-explored within these restrictions.
Stationarity, same loop and marked observer are deliberately pinned class restrictions,
not pinned-by-THEORY native selections. c_E is the supplied observed unit calibration.
G405's entire accepted scope (including G166 OPEN/G176 WORKING) controls the record join.
G407 is calibration-method precedent only; its real linear theorem will NOT be applied
silently to wrapped optical phases. No Einstein/Ric=0 or Maxwell law becomes native input.

Supplied optical bridge: a stationary reciprocal guide/optical path model with coherent
same-frequency counterpropagating transfer, equal local opposite-direction propagation,
proper source/detector clock, and controlled differential boundary/electronic phase. An
arbitrary curved guide is not a freely propagating null geodesic. Vacuum ray optics is an
imported approximation requiring wavelength small against relevant scales and valid boundary
handling; no finite-device remainder is supplied here. Either an explicitly ideal pure-delay
transfer is used, or the physical join remains OPEN. Do not substitute pulse/group delay for
phase delay in a dispersive guide. Apparatus and calibration assumptions are supplied, not
derived or asserted experimentally certified. Native kernel depth is not optical phase.

Hand exploration before this freeze suggested the standard signed loop delay
D=-2 N_D/c_E integral_C beta. G405 suggests beta(v)=m_v B_v in the original common marking,
while Phi=-log N alone loses this information. Candidate witness beta=kappa(x dy-y dx)/2,
N=1,gamma=Euclidean on |kappa|R/2<1, compared to kappa=0, has identical scalar records.
These are planning leads, not yet checked results. No observations were loaded or fit.

The same planning suggested phase model Z_j=exp(i[(omega0+j*domega)D+b+e_j]), j=0,1,2,
constant externally justified residual offset b. Train on0,1; hold2 unused. The proposed
wrapped contrast Z2*Z0/Z1^2=1 would test a shared affine-frequency phase model without
unwrapping, while D remains aliased modulo2pi/domega unless independent coarse information
resolves it. Arbitrary frequency-dependent phase bias can absorb the test. Bound frequency
errors and all phase-transfer errors explicitly; no numerical sensitivity or confidence claim.
This finite algebra is to be rederived, not presumed from G407. A constant extra optical delay
can remain indistinguishable from metric delay even if the contrast passes.

Primary-source exposure: searched/read Ruggiero and Tartaglia arXiv1411.0135v2 SecII (known
stationary same-path/equal-local-speed Sagnac construction) and Dolan1806.08617 introductory
geometrical-optics scope. Existing formulas are credited standard bridge methods. Source-first
review is independent reconstruction after definitions/existing-source exposure, not blind
discovery or different-model review. This study claims no new Sagnac law. Original source
notation/OCR must be checked against the metric, especially the proper-clock square-root sign.

Planned checks: original pulled-back metric/determinant and full-record sign; direct forward
and backward null roots on the witness; loop integral, gauge/time-unit invariance; same-scalar
different-delay controls; common-event phase sign; wrapped prediction/alias exact arithmetic;
detectable and invisible departures; phase/frequency error propagation; explicit mutant catches.
Analytical proofs own quantifiers; finite tests are diagnostic exact algebra/regression only.
No claim of a full Maxwell boundary solution, finite-wave error, device evidence, native assembly,
selected scale, curvature reconstruction from one loop, physical population, long-time result,
uniqueness or genericity. All failed checks and later changes will be retained.
