# ERC1 actual-candidate mathematical review

Verdict: **VERIFIED-WITH-CAVEATS for the conditional mathematical comparison,
after the bounded implementation repair.** No remaining load-bearing algebraic
defect was found. Neither response is adopted, native UDT dynamics is not derived,
and this verdict does not establish physical truth, empirical recovery or canon.
Final central integration has not yet been reviewed by this report.

## Context, exposure and actual work

This is the same fresh separate-context reviewer whose source-first argument,
code, outputs and seal remain preserved in math/. The initial dispatch exposed
the two response definitions, sources and work-order scope, not the parent
implementation or outcomes. After the source-first seal, this review read the
parent INITIAL_DERIVATION.md, NUMERICAL_PLAN.md, original check_candidates.py,
candidate/output freezes, symbolic/smoke/full summaries, the actual saved metric
arrays used below, and subsequently the disclosed implementation repair. The
parent identified the combined Ric+Q checker weakness before this reviewer tested
it. This reviewer did not originate that finding. No other reviewer result was
supplied. Exact backend model/runtime identity is unavailable; the inherited model
and Python/SymPy/SciPy libraries are shared, so different-model/library review is
not claimed. Independent scientific implementations and derivations are recorded
separately from regression and file correspondence.

Parent startup and prior full406 audit remain attributed to its dispatch. The
reviewer independently checked branch/HEAD/tracked status during source-first
work, read required repository protocols, and wrote only math/. No protected
payload was examined. No full-premise verifier replay, empirical data analysis,
unrestricted PDE solve or source/carrier campaign was performed by this reviewer.

## Argument and scope

The regular A implication agrees with the independent derivation: nonzero scalar
modulation leaves the DDR Einstein-shape solution set invariant, and Bianchi gives
constant R. It does not exclude its separate F=0 stratum or decide whether
conservation should be imposed physically. The B trace-free equation, off-shell
divergence identity, connected integration constant and scalar trace signs are
correct under the stated curvature/signature conventions. DDR alone is not
silently replaced by E=0: the Lambda integration datum is retained. The weak
vacuum exterior is explicitly the Lambda=0 subcase.

The full weak first variation needs both potentials. Their names are interchanged
relative to this reviewer's source-first notation, but both documents explicitly
identify the time and spatial potentials, and the equations agree. The radial
Yukawa member is a declared positive-alpha boundary choice, not an inferred matter
amplitude or uniqueness statement. The compact-domain O(epsilon^2) equation
residual follows from smooth dependence and vanishing zeroth/first coefficients;
it is not a distance bound to an unknown exact nonlinear solution. Static proper
clock ratios retain the lapse contribution although the scalar pieces cancel
from first-order coordinate null travel. No empirical recovery follows.

In the homogeneous slice, the original 00 constraint and Cdot=-4HC are correct.
Constraint-satisfying finite data give an ordinary local ODE solution with a>0
locally; this does not establish well-posedness of the unrestricted fourth-order
metric theory. Tracking R separately introduces additional curvature-derivative
initial data, not an independent UDT matter field. Alpha=0, alpha<0 and F=0
retain their separate stated scopes. Positive alpha's flat scalar-mode sign is
not full nonlinear stability, and sampled F>0 is not a universal principal claim.

The flat-event example is a legitimate conditional refinement of PCC1's supplied
cubic control. H=R=0 gives a'=a''=0 and full FLRW curvature zero at that event;
the initial spatial slice also has zero extrinsic curvature, so the comoving
clocks are parallel-prepared along that initial straight spatial geodesic.
Independent polynomial differentiation yields

    a(t)=1+(P0/36)t^3-(P0/(4320 alpha))t^5+O(t^6).

The null-arrival inversion therefore gives the displayed cubic coefficients 1
and 7. The fifth-order coefficients in log p/log q are -P0/(4320 alpha) and
-31 P0/(4320 alpha). The parent's O(L^5) error statement is correct and differs
appropriately from PCC1's exactly supplied cubic scale factor. Zero quadratic
clock curvature does not freeze higher-order finite-separation information. This
does not assert PCC1's regional all-frame contrast or positional attribution.

**Wording condition for integration:** p and q here are infinitesimal received/
emitted proper-period ratios at finite separation, evaluated at the actual null
arrivals. The saved first/echo arrival times are finite travel intervals from
the initial emission. These ratios must not be described as exact ratios of
arbitrary finite emission periods. This reviewer's separate source-first example
did compute finite pulse-period ratios; it is a different supplied example.

## Independent numerical evidence and its limits

The sealed source-first run used its own Radau implementation and a different
constrained initial state. Its E00/Eii evaluation used derivatives from its own
evolution RHS. Those residuals are useful equation/constraint consistency checks,
but are **not independent numerical backward-error certification**. This was
already disclosed in SOURCE_FIRST_RESULT.md and is retained here prominently.

The exposed direct_saved_check.py instead reads the parent's saved a(t) only,
constructs independent 11-point exact-Vandermonde derivative weights, differentiates
through order four, and evaluates the original metric response. It imports no
parent helpers or RHS. All eight existing finest-solver histories and all three
saved grids were checked without another numerical survey. Maximum finest-grid
absolute tensor residual was 1.0228789434710498e-8, below the predeclared 1e-7
diagnostic threshold. Errors grow from approximately 1e-11 on coarse grids to
approximately 1e-8 on fine grids because fourth derivatives amplify floating
roundoff. This is agreement at an explicit finite accuracy, not a demonstrated
convergence rate. Five boundary samples on each side are omitted by this review
stencil; the parent's H-based stencil omitted four. Neither certifies endpoints
or the continuous interval by sampling alone.

An a-only quintic interpolation/quadrature/root calculation independently
reconstructed the parent's first/echo arrivals and p/q values for all 24 listed
distance/case queries. Maximum finest-grid discrepancy was 2.853273173286652e-14.
It did not use evolved eta or the parent's dense solver object. The saved
flat-event clock remainders also agree with the independently derived quintic
coefficients, with visible small-number floating error at the shortest distance.
Interpolation/quadrature agreement is qualified floating evidence, not interval
certification or an empirical comparison.

118 entries in the original candidate/output freezes were checked against actual
files, mapping the original checker hash to its preserved initial copy. These
hashes establish correspondence, not scientific truth or chronology.

## Defects, repair and surviving conclusion

1. The original combined off-diagonal assertion allowed Ric_ij=1,Q_ij=-1 to pass.
   The smallest repair is separate assertions for each tensor. The independent
   repair check executes the actual extracted original/repaired loops on that
   compensating-error fixture: the original passes, the repaired loop rejects it.
   The repaired symbolic output has 39 exact zero assertions. Their count is not
   a count of independent scientific results.
2. The parent's exposed rational-series checker initially seeded an integer that
   became a binary float under division. The original script, failing capture and
   diagnosis are preserved. Fraction seeds restore exact arithmetic. Inspection
   and this reviewer's independent fifth-order derivation support the repaired
   leading-coefficient claims. The full degree 12 rational recurrence is not an
   interval error bound for the analytic solution.

The AST comparison finds only the symbolic function changed in check_candidates;
all numerical functions are unchanged. Repeating the 24 evolution solves would
therefore add regression without addressing the repaired issue. The original
numerical results remain applicable. Seven repair-checkpoint hashes match actual
files. The checkpoint expressly binds post-execution files; this reviewer did
not observe the parent's repair execution in advance and makes no stronger
chronological-independence claim.

The strongest surviving result is a reviewed conditional comparison: A leaves
regular Einstein geometry unchanged; B is the known unadopted metric-f(R)
response and admits additional nonconstant-curvature histories with actual
metric clock consequences, including the specified flat-event cubic example.
Native response identity, alpha/source/initial-data selection, matter coupling,
positional interpretation, empirical GR recovery, global completion and full
stability remain open. Free initial data or this bounded comparison do not prove
that all current UDT premises are insufficient or require a new postulate.
