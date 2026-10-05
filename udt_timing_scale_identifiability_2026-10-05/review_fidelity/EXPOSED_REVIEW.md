# TSI1 exposed fidelity review

**Verdict: VERIFIED-WITH-CAVEATS for the conditional candidate; final central
integration review pending.** No substantive or implementation repair requested.
No native admission, observational verification, source-grade change or canon.

Reviewed INITIAL_CANDIDATE.md and NUMERICAL_FREEZE.md after completing
SOURCE_FIRST.md. The matching angular argument had independently been derived
by this reviewer; the parent reports freezing its own derivation before reading
the reviewer's matching message. The timing formula was disclosed at dispatch,
so no blindness to it is claimed. Saved output was exposed before the additional
EXPOSED_FREEZE; confirmation is not blind. Producer code was first read only
after independent saved-quantity recomputation completed.

The candidate correctly distinguishes three physically specified data interfaces:
labeled differential source/reception times; the principal point-source angular
track in a radial parallel transported frame against receiver proper time; and
untimed redshift/angle records. The first timing route uses CPR1's actual smooth
varying-b branch. The angular route retains the special b_*=0 preparation and
nonzero Omega a/H coefficient. A radial geodesic's radial unit normal is parallel
transported because the trajectory is geodesic, the radial2-plane is preserved,
and unit norm/orthogonality exhaust its components. The equatorial angular basis
has the expected1/R normalization. The future-photon versus incoming-sky sign
convention is explicit and does not change the displacement decay exponent.

The candidate does not confuse an asymptotic equivalent with derivative control.
The F'/F bound is conditional and branch dependent; it is not presented as a
known observational error bar. Receiver seconds and proper length are correctly
separated: measured K_seconds=c_E H, scale1/H=c_E/K_seconds. Constant unknown
source normalization cancels; arbitrary drift is a nuisance; bounded endpoint
logarithmic drift is a stated additional regularity condition. Finite fixed
cadence cannot supply infinitely many receptions accumulating at the finite
emission endpoint. Finite-data identifiability is explicitly left unproved.

The homothety, angular endpoint and source-size compensation preserve the
existing negative descendants. Dimensional constants alone do not select H;
calibrated timing supplies the missing independent datum. G_obs only forms a
mass-dimension equivalent without a justified physical mass interface. No
geometric m-to-source-mass identification, physical X_max, empirical Hubble
identification or extra effect over matched GR has been introduced.

## Checks and evidence limits

Six independently re-solved saved60-digit cases used the frozen source-first
implementation, evaluated at50 digits, with E=1,10 and b_*=0,2,-3 at R=100000.
No producer source/function was imported. Own R/b partial derivatives and
implicit db/dR reproduced b,A,Z,K_length,theta,angular_rate with largest scaled
error2.23708636e-51. Two saved finite-difference endpoint pairs were independently
integrated in receiver proper time and their logarithmic timing/angular averages
recomputed, maximum scaled error1.07369970e-49. Their inputs are saved producer
values, so these two controls are recomputations of saved quantities, not fresh
incidence solves. The six fresh solves provide the distinct incidence check.

`saved_recheck.json` records the actual1.000s capture with46,808KiB peak,
2GiB virtual limit, one BLAS thread and no timeout. No failed run or repair.
Together with the source-first12 solves this reviewer has used18 independent
finite incidence solves,8 initial exact/control groups and2 saved-average
controls, below100. No producer replay or mutation run was performed.

Inspection of producer code found no contradiction with the checked formulas.
Its `dimensional_group` is explicitly hardcoded exponent arithmetic; analytic
unit covariance supplies the proof, not that arithmetic assertion. Likewise
its omitted-c_E controls compare supplied right/wrong expressions, rather than
mutating the producer and testing a rejection path. They must not be reported
as mutation-tested guards. The candidate itself makes no such claim.

Full4D curvature/Jacobi, all source-package tests, observational inference,
finite-source accuracy, finite-data uniqueness and native selection were not
repeated. Parent closure owns current normal/maintenance/full406 checks.
Current verdict applies to the candidate's source fidelity and scoped analytic
argument, supported by the stated independent finite computations only.
