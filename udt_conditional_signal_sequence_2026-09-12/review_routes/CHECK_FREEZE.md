# Independent route checks: finite pre-outcome freeze

Source-first notes were sealed before reading the CSS4 candidate. The candidate
was read after that seal and its equations are now exposed. No parent CSS4
scientific implementation or numeric output has been read. This is a distinct
implementation and direct full-metric root calculation, not blind prediction.

CPU FLOAT64 with SciPy DOP853; no parent scientific functions imported. Integrate
angle in actual coordinate time using the roots of the full Cartesian metric
quadratic on the supplied circular tangent. Stop at angle=2pi or at the strict
slice guard |A|=(1-1e-6)R. A numerical formula using the integrating factor is
comparison-side only. Every admitted finite sample includes its full traversal
and its emission finite-difference neighborhood.

Frozen finite cases: R in {0.6,1.3}, A(0)/R in {-0.25,0,0.25},
q=R² bdot/2 in {-0.04,-1e-12,0,1e-12,0.04},
e in {0,0.35,0.9}; both orientations. L=0.7 and L=2.4 alternate across
cases; c_E=1 is the chosen output time-unit convention, not a fitted constant.
The independent integration horizon is e+12R. Derivatives use e+-h with
h=1e-3 R. DOP853 rtol=2e-12, atol=2e-13, max_step=R/10.
Arrival relative/absolute guard 3e-10*(1+abs(expected)); pulse slope error
guard 3e-8; normalized full-metric null residual <=2e-12; future root >0;
slice margin >1e-6; finite whole-duration relative error <=3e-10.

Adverse/control checks: zero-rate stationary OB1 limit; tiny-rate removable
limit; physical proper-time factor from sqrt(-g00); q!=0 and A_e=0 timing
asymmetry; sign reversal with R=1,A_e=-0.03,q=0.02; fixed frozen profile
versus a profile re-frozen at each emission; full-domain rejection at
R=1,A_e=0,q=0.2 although the initial slice is positive; the flat circular
null route's non-geodesic acceleration. Check direct symbolic projection
of dU-flat in the full metric and its contraction for W=b²/(2L²), and the
literal G405 K=partial_t clock norm T=L.

Catch controls compare against independently integrated records: frozen-only
arrivals; first-order-in-rate arrival approximation; reversed slope sign;
omitted proper L factor; tiny-rate naive exp subtraction; initial-only slice
eligibility. These are explicit artificial wrong computations/guards, not
physical alternatives. An expected rejection is distinct from a failed test.
Preserve any actual script failure and use a new capture stem for a repair.

Existing capture_existing.py, 180 seconds / 2048 MiB; single library thread,
PYTHONDONTWRITEBYTECODE=1, one science subprocess in this context at a time.
Maximum result: finite numerical anchors and analytical-source review for CSS4,
conditional and UNPROMOTED. No instrument error, energy or native-light claim.
