# G306 audit report

Date: 2026-08-30
Status: EXTERNAL_SCIENCE_SUPPORTED__PREREGISTERED_PORTABILITY_REPAIRS_COMPLETE__FOLLOWUP_PENDING

## Primary landing

ROUND_S3_METRIC_INTRINSICALLY_DEFINES_TWO_ORIENTED_HOPF_CONGRUENCE_FAMILIES
__ISOTROPY_SELECTS_NO_PHYSICAL_MEMBER
__SUPPLIED_GEOMETRIC_MEMBER_HAS_FRAME_INDEPENDENT_SCALE_BLIND_NORMALIZED_HELICITY
__RAW_COMPONENT_HOPF_NUMBER_FAILS_FULL_LOCAL_FRAME_DESCENT
__FIELD_QUERY_POPULATION_TARGET_ACTION_DYNAMICS_HISTORY_MAGNITUDE_MASS_AND_XMAX_REMAIN_OPEN

## Result

G305 supplied more than an empty compact domain, but less than a physical field. Every
positive-radius round \(S^3\) slice intrinsically defines two orientation-relative \(S^2\)
families of unit Killing fields whose integral curves are closed geodesic circles and whose
screens undergo pure rotation. Each supplied member defines a Hopf fibration and has
frame-independent normalized geometric helicity \(+1\) or \(-1\), independent of the slice
radius.

The full round-slice isotropy group selects no member: at each point its \(SO(3)\) isotropy fixes
no nonzero tangent vector. A raw component Hopf map also remains unphysical by itself; a smooth
basepoint-fixed local frame rotation changes its component charge from zero to \(-1\). The
surviving invariant uses a supplied geometric vector field, not a fixed component target.

Thus the metric narrows arbitrary \(S^3\to S^2\) maps to an intrinsic highly symmetric candidate
family, but it does not populate a field, select a query, choose a chirality or member, import an
action, or determine dynamics, history, curvature magnitude, mass, or physical \(X_{\max}\).

## Scope and evidence

The result is complete only for the positive G305 standard connected simply connected round-slice
completion, all positive radii, and both chiralities. Nonspherical, quotient, singular,
topology-changing, dynamically populated, and route-conditioned cases remain open.

Preregistered at pushed commit c5873d2c; 172 production assertions; 22,237 independent checks;
17 direct hostile mutations caught. Fresh external review returned `REPAIRABLE_DEFECTS` while
explicitly finding no bounded scientific defect and independently reproducing the quaternionic,
isotropy, frame-descent, Hopf, and helicity results.

The three defects were replay portability only: repository-only commands were not distinguished
from sealed commands, the source verifier assumed repository layout, and production imported
unsealed SymPy. Repairs R1--R4 were preregistered and banked at commit 1298deea before repair. The
production derivation now uses exact standard-library integer/rational/polynomial algebra under
`python3 -S` and reproduces the original JSON and census byte-for-byte. All four sealed commands
pass in a fresh copied intake; missing and ambiguous source layouts are rejected. Premise and full
repository gates also pass. External repair-only follow-up remains pending, so the result is not
yet graded externally accepted.
