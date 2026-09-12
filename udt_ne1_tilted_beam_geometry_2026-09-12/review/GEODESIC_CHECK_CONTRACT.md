# Original-geodesic check contract

Frozen after source-first scalar outcomes but before parent candidate/code/outcomes.
The scalar eight-case diagnostic had no X zero through t=80; it supplies neither
general nonconjugacy nor an all-time conclusion. No scalar crossing follow-up is
triggered. The original source-first formulas remain unchanged.

Independently integrate the complete original metric geodesic equations derived in
SOURCE_FIRST_NOTES.md. Fixed cases (epsilon,xi_e,mu,psi,t_o):
(1/6,.3,.6,0,12), (1/6,.3,-.6,pi/2,12), (.5,.7,.6,.7,12),
(.5,.7,-.6,.7,12), (1,.4,.2,1.1,8), (-.5,.9,-.3,.4,12),
(.5,0,0,0,12), (.5,0,0,pi/2,12), (.5,.3,1,0,12),
(.5,.3,-1,0,12), (0,.7,.6,.7,12).
Both longitudinal signs, both transverse axes, mixed directions, both exact axial
directions, a background case and invariant pure-transverse controls are covered;
this is a finite declared set, not a whole-sky census or absence certificate.

Great-circle source variations h=1e-3,5e-4,2.5e-4, each with positive/negative
offsets in two source-screen directions. DOP853 rtol=2e-11,atol=2e-13,max_step=.05.
Compare each h-pair derivative and Richardson h^2 limit. Criteria: normalized
finest-versus-extrapolated screen derivative <=2e-5; metric nullness <=2e-8;
reception-screen orthogonality residual <=2e-5 before extrapolation. Background
and axial maps independently checked with quadratures, tolerance 2e-5; invariant
pure y/z physical longitudinal width checked against independently integrated
source-first scalar equation (effective epsilon +/-epsilon), tolerance 2e-5.
Clock contraction values and area/singular values saved for later parent comparison.

Finite-angle differences are derivatives only in their h->0 limit and can fail
near ill conditioning. Preserve all failures; report unresolved precision issues
instead of silently dropping cases. No threshold proves absence at untested times.
Float64, CPU, one science process, one library thread, capture <=180s,<=2048MiB.
