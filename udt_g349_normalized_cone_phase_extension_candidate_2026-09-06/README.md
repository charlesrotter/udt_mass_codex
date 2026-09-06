# Decision brief: one normalized cone admits local phase extensions

Status: **VERIFIED-WITH-CAVEATS after fresh separate-context review; unpromoted candidate**.
Source snapshot: `5ef2f971805ee23383cad694c5cb058124614a5d`.
Reviewed candidate: `f14098737a7bd571aff79bef09ccffdc22135853`.
Current review record: [review summary](review_2026-09-06/REVIEW_SUMMARY.md).
Initial work-order, argument and coverage labels retain their construction-stage
history; the owner's [review extension](review_2026-09-06/REVIEW_DISPATCH.md)
authorized the completed review cycle without changing scientific promotion limits.

The reviewed bounded argument supports compatibility, with substantial freedom left over.
On a small regular piece of G349's supplied cone, away from the vertex and rank
loss, the candidate construction extends a scalar phase into a neighborhood
without changing the cone's prescribed affine tangent normalization. It does
not identify a physical phase object or choose a neighboring ray population.
G349's mathematical normalization is not thereby a physical frequency unit or
an operational calibration of G352's dimensionless phase.

The exact framing is

    g^-1(dTheta,dTheta)=0,
    Theta|N=0,
    dTheta_q=g_q(k_q,.) at every point q of the retained cone patch.

The last equality concerns the full spacetime covector. A restriction to tangent
vectors of the cone would read zero equals zero and would not fix frequency.
The argument is local around each regular point; it does not promise a single
extension over an arbitrary whole cone or over distant cuts.

## What was learned

1. A spacelike proof slice permits initial scalar data matching the cone's full
   first derivative. Smooth geodesic characteristics extend those data locally.
   Uniqueness of the affine geodesics preserves the originally supplied k.
2. Those slice data have a free smooth remainder, schematically
   `phi=a(y)rho+rho^2 b(rho,y)`. Explicit flat examples show that neighboring phase
   surfaces can genuinely differ, not merely receive different names, while
   agreeing in value and full gradient on the original cone.
3. That freedom does not affect the local G352 readout on the original cuts
   contained in a common extension domain, when the measure, spacing, observers
   and cut maps remain fixed:

       omega_i=-g(u_i,k),
       Gamma_i=(omega_i/DeltaTheta) s/J_i.

   Even the absolute Gamma_i agrees, not just its nonzero-density ratio R/A.
   Values at neighboring phases or over finite observer-worldline intervals
   are not fixed by this statement.

## What remains supplied or open

The supplied metric and G349 cone data determine the geometric tangent and
sheet area on that cone; geometry also supplies source solid angle. Neither
geometric measure is automatically G351's physical carried measure.
G351's conservation and G352's clock-rate interpretation remain
owner-adopted provisional premises. G352's continuous product, common spacing,
phase-independent population and cross-phase label identification remain chosen
or supplied, not consequences of this construction. No light, energy, source,
detector, history, matter or scale has been selected.

This result therefore does not force a new premise, establish a native physical
derivation, or decide that neither is possible. It removes a proposed local
mathematical incompatibility only at candidate level.

## Checks and next stop

The exact witness checks passed 53 assertions. Four deliberate code mutations
were rejected at the intended checks: zeroed acceleration, tangent-only
normalization matching, omitted frequency, and radius substituted for area.
A separate stdlib rational implementation reproduced the saved-input finite
cut readouts (areas 9 and 25, frequencies 1 and 2/3, ratio 6/25). This is the same
author/context, not itself an independent review. Subsequently, a fresh reviewer
reconstructed the general argument from accepted sources before candidate
exposure, directly scrutinized the proof, independently checked the distinct
foliation by a pullback-metric calculation, and replayed the recorded checks.
Its verdict is VERIFIED-WITH-CAVEATS, with no mathematical defect or required
scientific repair. Exact reviewer model is UNKNOWN; no different-model claim.
The current 335-row premise audit passed; it does not establish backup
completeness or unsaved-state disposition.

Operational caveat: `run_checks.py` is capture-only. Exit 0 means capture
completed, not that the checks passed. Verify baseline exit 0 with the expected
result, and each mutant's exit 1 at its intended AssertionError; an unrelated
exception or timeout is not a successful defect catch. The actual child outcomes
were checked by the reviewer. The frozen scripts and mathematical argument are
unchanged; the reviewer's own checker failure/repair history is preserved.

This completes the authorized verification cycle at a reviewed conditional
candidate, not an accepted dependency or new frontier entry. Scientific
promotion, physical commitments and a new research question remain outside this
authorization. There is no archive-dependent blocker for the completed review.

The completed infrastructure audit and fixed-snapshot manuscript are unchanged.
Backup completeness and pre-reboot unsaved-state disposition remain UNVERIFIED.
ScratchDisk remains a blocker only for archive-dependent work. Protected local
payloads and unrelated work were not inspected or altered.

Details: [candidate argument](CANDIDATE_ARGUMENT.md), [work order](WORK_ORDER.md),
[premise/coverage ledger](PREMISE_AND_COVERAGE.tsv), and
[check and review record](REVIEW_RECORD.md).
