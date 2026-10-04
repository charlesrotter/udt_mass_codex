# CPR1 numerical repair and saved-artifact review

Reviewer `/root/cpr_fidelity`, continued separate review context. This stage is
fully exposed to the parent implementation/results. It is not blind numerical
construction or a different-model review. CHECK_REVIEW_SNAPSHOT.json pins the
exact reviewed inputs and independent review outputs. The initial source-first
and exposed argument seals remain unchanged.

Verdict: **VERIFIED-WITH-CAVEATS for the repaired finite checks, their documented
provenance, and the corresponding claim limits**. The repair is appropriate and
does not relax the original acceptance standard. No remaining substantive defect
was found in this bounded numerical use. This verdict does not establish native
physics, interval certification, a global ray census, orbit stability or an
empirical bound. Final central integration is still pending its separate review.

## Repair and preservation

I read INITIAL_CHECK.py, check_restriction.py, the original and repaired freezes,
CHECK_REPAIR.md, both diagnostic sources/freezes, CLARIFICATIONS.md, all four
execution receipts and stdout/stderr, and CONSTRUCTION_RESULT.json. The code diff
contains only the narrowed finite-case list, the stricter internal stopping
threshold, and corresponding case-count labels. All original assertion thresholds
remain intact. CANDIDATE_FREEZE's original code hash matches INITIAL_CHECK.py;
all initial/repaired freeze hashes and receipt stdout/stderr hashes match their
actual retained bytes.

The old root stop was 10^(-dps+10), looser than its original-incidence acceptance
10^(-dps+9). The retained center diagnostic reproduces a 70-digit residual of
4.0998519464711163e-61 at E=1,R=1e6: below the old 1e-60 stop but above the
1e-61 acceptance. The original run exited nonzero at that acceptance assertion;
the failure was not suppressed. The repaired internal stop 10^(-dps+7) is tighter
than acceptance and retains the failing parameter point.

The stated accounting is consistent with the fixed loop order, traceback and
diagnostics: 56 original attempts, five first-case diagnostic attempts, four
center-diagnostic attempts, and 30 repaired attempts, totaling 95. This is a
documented reconstruction, not a claim that the first run preserved every
intermediate numerical state. The repaired run returns zero, with 30 successful
incidences at 40/70 digits and max RSS 57,784 KiB in the receipt. All receipts
declare the 2 GiB address-space cap and null wall/CPU timeouts. I did not rerun
the original failed run or add to the parent attempt count.

The coverage reduction is honestly stated. The final E=1 rows lie outside the
outer horizon, whereas E=10,R=100 is in the static patch. They are examples with
different receiver energies; they do not numerically trace the same history
continuously across a horizon. Regular-chart exact algebra owns the crossing.

## Code and numerical meaning

The symbolic function constructs the original outgoing-coordinate Christoffel
symbols and all Ricci components, rather than assuming the Einstein result.
Both vector norms and all geodesic acceleration components are reduced using
their declared energy relations. The equatorial restriction and positive
denominators are inside the supplied regular branch. The Weyl check uses a
declared spherical sectional-curvature formula and is not a separate full Weyl
tensor reconstruction. I inspected these steps; I did not claim an independent
symbolic replay or a formal proof-checker result.

The finite code solves the correct angular incidence after constructing the
time incidence. Its Newton derivative I(1-Omega b) follows from the original
integrals. The time-equation residual from te=-d-U is zero by construction;
by itself it is not independent confirmation. The angular residual, direct
arrival-time derivative, and separately contracted frequency supply substantive
checks. Precision agreement is same-code numerical consistency, not a separate
physical or implementation-independent proof.

The stored maximum original residuals are approximately 3.67342e-40 and
2.89782e-70 at 40 and 70 digits, below their unchanged acceptance thresholds.
The stored maximum normalized cross-precision difference is 3.65245e-40,
below 1e-25. The largest finite-step arrival error is 7.74536e-9; halving the
step reduces each error by approximately one quarter, as expected for these
centered differences. These facts support only the supplied finite examples.

The product H Z (tau_e,star-tau_e) at E=1 is 0.9210477 at R=1000 and
0.99994155 at R=1e6. The E=10,R=100 value is 1.2813837. The latter is a
finite-domain control, not a false claimed asymptotic pass. The final high-radius
acceptance is explicitly illustrative and does not certify an error envelope
for the analytic limit or establish universality from three rows.

## Independent saved-artifact recomputation

Before execution I froze SAVED_RECOMPUTE_FREEZE.md, its code/input hashes and
command. The implementation reads the three saved 70-digit central incidences
but imports no parent module and never calls its root solver. It integrates the
original r-coordinate ray/receiver expressions using different quadrature
variables and partitions, then contracts the original outgoing metric matrix
to obtain frequency and the limiting product. It ran at the reviewer's original
50/90-digit precisions, six finite recomputations, bringing this reviewer's
total finite/exact cases to 43, below 100.

All six recomputations pass. At 90 digits, the largest reconstructed incidence
residual is 2.86861e-69, consistent with rounding of the saved 70-digit inputs;
the largest relative frequency difference is 2.59367e-70 and product difference
1.06766e-70. At 50 digits the largest residual is 4.27643e-50. These are
independent arithmetic checks of the saved load-bearing states and contractions,
using the same mpmath library but a distinct implementation/integration variable.
They are neither independent source observations nor interval certification.

Satellite incidence states were not saved in CONSTRUCTION_RESULT. I inspected
the actual satellite-solving/arrival-derivative code and checked the saved error
thresholds/convergence ratios, but did not independently reconstruct those
satellite states or call their derivative-error values independently reproduced.
This omission is limited: the analytic timing derivation and independently
recomputed central original equations/contractions remain the load-bearing
evidence; the satellite errors are parent regression/finite checks.

## Clarifications and physical ceiling

CLARIFICATIONS implements both requested fidelity refinements: finite limiting
emitter time versus infinite receiver time, and conservation of b on each ray
while b varies between rays. Its monotonicity argument for f/r^2 supplies the
uniform outward ray-regularity hypothesis. Its statement that orbital-rate
recovery does not establish stability/disk behavior is appropriate. These are
source-preserving repairs with no changed candidate equation or physical premise.

The numerical pass does not close the owner's separation-to-asymptote attachment,
make a new angular loud regime, identify areal radius with physical separation or
X_max, adopt the response class, or select Lambda in native UDT. All such limits
from the source-first/exposed reviews remain in force.
