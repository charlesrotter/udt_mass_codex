# ACP1 exposed mathematical review and repair assessment

Verdict: **VERIFIED-WITH-CAVEATS for the conditional construction after REPAIR.md**.
This is not an empirical fit, selected metric, physical-premise adoption, grade
upgrade or canon. Source-first reconstruction is preserved separately and was
sealed before this reviewer read the candidate. The parent disclosed exposure
to reviewer summaries before writing its candidate, so this is not a mutually
blind derivation. Same inherited model; exact revision not exposed. Fresh
context, independent argument and separate implementation are established;
different-model, human and formal-proof review are unavailable.

Initial candidate reviewed: SHA-256
4f477ceaadf4139045b63d6aa8df35c0f2b75c8482062aa87f2a31fc67f9fac4.
The initial candidate is preserved. Its controlling repair is bound in
DIRECT_REVIEW_PINS.json. The analysis below examines the argument and hypotheses,
not only finite checks.

## Defects, survivors and smallest repairs

**1. Signed sky map.** Initial section 4 wrote J=omega_o B_eo and allowed the
sign to be absorbed into a compatible orientation without fixing the affine
direction of B_eo. With G348's reverse block on the same future-affine k and
already fixed endpoint screens, x_e=omega_o B_eo delta n_prop and
delta n_prop=-delta n_sky. Therefore J=-omega_o B_eo. A silent sign flip would
reverse predicted source offsets in the calibrated frame. Area, similarity,
affine invariance and determinant conclusions survive because det(-J)=det(J)
in two dimensions. Repair1 fixes B's convention and requires transforming
source coordinates with any actual basis change. This is the smallest repair,
and it resolves the issue.

**2. Source systemic clock.** Section 6 connected the published systemic model
parameter z0 to R6's clock leg without supplying the additional reference-clock
realization. An inferred SMBH systemic parameter is not a measured ordinary
emitter clock, and a black-hole center cannot silently supply the regular
timelike endpoint required by R6. The source-conditioned ratio and its arithmetic
transforms survive, as does R6 for actual maser spot histories. Repair2 calls
the computed values Phi_summary and chi_summary and requires a consistent
regular reference history, branch and source-reduction realization before
identifying an actual R6 clock leg. No reference clock is invented. This resolves
the overidentification while preserving the conditional forward construction.

Repair3 correctly replaces a blanket two-year fitted slope by the actual finite
monitoring-window estimator. Repair4 keeps the statistical distance interval
separate from XI's model-choice systematics and retains XIII's rounded source
summary. Those are source-fidelity matters; this reviewer independently saw
XI's nine-epoch fitting description and Table5 systematics, but defers complete
source-table/likelihood fidelity to the dedicated reviewer.

## General mathematical assessment

The received-tick proof uses a supplied regular smooth null family, ordinary
proper clocks and the same metric connection at both endpoints. Changing ray
normalization uniformly along each ray leaves Z and its family derivative
invariant. Stable or explicitly supplied intrinsic transition evolution is a
separate physical readout hypothesis. The derivative in candidate equation2
correctly includes both the reciprocal arrival-time conversion and intrinsic
frequency change. For Z=Z0 Q, the optical convention produces the logarithmic
source-time derivative in equation3; an additional division by constant Z0
would double count. This neither derives disk motion nor certifies an exact
source-time convention in unavailable astrophysical fitting code.

Exact ray/source incidences precede local screen reduction. G348 supplies an
infinitesimal quotient map, not a finite disk image. A determinant determines
area only: J=d I and J=d diag(q,1/q) have the same determinant but different
directional lengths. The similarity condition J^T J=d^2 I characterizes the
scalar-length mapping up to a specified orthogonal map; rank loss and source
disk projection need separate attention. The C2 Taylor remainder is valid on
the declared convex regular chart with an actual Hessian bound; no such bound
is inferred merely from the galaxy's small angular extent. The candidate and
repair retain these hypotheses and do not claim the scalar approximation for
every supplied metric.

At a receiver replacement with frequency ratio F, Z transforms by F^-1,
solid angle by F^-2 and angular-area distance by F when the same intrinsic
source screen is used. These are observer changes, not passive frame rotations;
the candidate labels this distinction. The source-reported CMB correction is
retained as a conventional reduction and is not made a native observer choice.

Summary distances and systemic factors are outputs of a conventional source
model. Their comparison needs the matching scalar-map/source assumptions or
a refit with the actual map. Full metric ray/clock evaluation must not acquire
extra local Doppler/gravity corrections already included in that geometry.
The construction explicitly requires compatible source realization and does
not use the distance posterior twice as independent data. A full candidate
geometry and source/statistical replay remain missing; the paper-level forward
design is what has been constructed and checked.

## Independent computation actually performed

The reviewer froze check_readout.py and its inputs before running. Initial
execution failed at parsing because one check line lacked a closing parenthesis.
The initial code, empty stdout, stderr and exit1 record are preserved. A one-
character syntax repair was frozen before rerun; no equation, input, tolerance
or test changed and no finite case had executed on the failed attempt.

The corrected run exited0: **18 finite cases, 101 checks** (the count includes
the case-budget assertion). It uses Fraction exact arithmetic plus 70-digit
Decimal log/exp, CPU, one BLAS/OMP thread, 2GiB address space, no timeout/GPU/grid.
The parent implementation was never imported or read. Parent numerical output
was first read after this independent run completed.

Eight proper-clock samples reconstruct hyperbolic emitter motion in Minkowski
coordinates, calculate arrival time as t+x, and independently obtain Z from
the null endpoint contraction. They test the drift by differentiating received
frequency, including intrinsic line evolution and ray-dependent affine scaling.
Four screen controls test GL coordinate/covector typing, metric area factors,
source inversion and the fixed-screen sign. Three exact boosts derive the local
celestial-angle factor from a rational direction chart. Three CGCG marginal
points independently convert the printed units and square the distance.
Finite wrong-rule separators reject an extra arrival divisor, one-endpoint
affine scaling, the wrong fixed-screen sign and determinant-as-map substitution.
These finite examples supplement the analytic argument; they do not certify
every matrix, physical source history or mutation class.

The median arithmetic is

    Z0 = 1.023923884035801861299659513115570105502787531766392869...
    Phi_summary = -0.023642191858269052790840690421693890758572156169302967...
    chi_summary = -0.023637787883032223031340033341612980798916922064433517...
    D^2 = 7673.76 Mpc^2.

The statistical marginal distance endpoints square to 6464.16 and 9120.25
Mpc^2. They are separate marginal transformations, not a joint confidence region.
The CMB center minus the source's 263.3km/s convention gives 6908.9km/s.
Fifteen median/bound/area fields were compared with CONSTRUCTION_RESULT.json;
the maximum absolute difference is 3.675243291e-60, from printed precision,
below the declared comparison allowance 1e-55. Exact squared distances agree.

The parent's saved execution receipts were inspected: initial exit1 with a
path-variable shadowing error after algebra, followed by a frozen repaired
exit0. The initial printed success is not counted as completed execution.
This reviewer did not replay or inspect the parent's implementation and does
not claim that this output comparison audits every one of its diagnostics.

## Retained caveats and final scope

No full source-table acquisition, data posterior fit, raw spectrum replay,
actual metric proposal, empirical confirmation, universal clock-history theorem,
microscopic signal model or native equation selection was done. The old FSL1
and G348 computational packages were not replayed; their source arguments and
controlling scopes were checked where load-bearing. Current premise verification
and central integration remain the parent closure gates. All four protected
prefix payloads remain unread/unhashed. This review wrote only review_math/.

The repaired result is a concrete conditional forward specification and a
source-conditioned summary restriction with two important tested joins: full
angular map rather than determinant alone, and correct receiver-time optical
drift accounting. The still-open native selection and reference/statistical
realizations are stated, not filled by a fitted redshift curve or new law.
