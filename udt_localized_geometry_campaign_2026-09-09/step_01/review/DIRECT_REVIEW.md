# LG1 direct adversarial review

Verdict: VERIFIED-WITH-CAVEATS, exactly for the local adjoint classification and
necessary matching identities stated below. Candidate remains UNPROMOTED.
No unresolved load-bearing objection; no scientific repair/re-review was needed.
This is not a gluing existence verdict or a grade/ownership change.

Reviewer `/root/lg1_review`, fresh separate context, exact model UNKNOWN.
Different-model review UNTESTED. Baseline grok
`78c3092b2120a80c8bbabb8024b4448d27c36a00` verified. Review date 2026-09-09.

## Exposure, freeze, and independence

SOURCE_FIRST.md was saved and its hash transmitted before candidate exposure:
`ca977370ad8c18ee177401fa1290c108d4d405037382d312e7ebd05b3dd12b59`.
The reviewer knew the question, admitted sources, and requested scope. The
parent's candidate proof/code/output and NR1/NR2 proofs were not exposed in
stage A. Two independently written symbolic checks completed in that stage.

Direct review began only after the parent's freeze notice. Read CANDIDATE.md,
author_check.py, author stdout and capture metadata, and FREEZE_SHA256SUMS.
The frozen candidate hash was independently confirmed as
`bcbeafc7f19bf29a298244bac7664748668175fe8b4a53f4a7d13db1c258098e`.
`sha256sum --check step_01/FREEZE_SHA256SUMS` passed all five listed files.

The independent argument differs from the author's argument: the author uses
the nonconstant spacetime curvature invariant to eliminate Killing lapse;
the reviewer directly solves the full constraint adjoint by a finite
symmetric-gradient compatibility identity. The reviewer recomputed the
nonlinear momentum-density identity from arbitrary metric/density first jets
and reconstructed the linear adjoint by varying the original mixed-index
momentum constraint. Author code was inspected but not rerun; it is not counted
as reviewer-independent evidence.

## Load-bearing argument review

1. The supplied G324 future orientation gives
   K0=diag(1,-2,-2)/(3T0), with gamma0=I after a constant chart rescaling.
   Matching both tensors on a nonempty exterior open set fixes the connected
   comparison sector to Lambda=0. This uses the admitted G303/G315 constraints;
   it supplies no physical scalar selection.

2. The author correctly obtains Kretschmann=64/(27T^4) from G324's
   12mu^2/R^6 and T=2R^(3/2)/(3sqrt(mu)). Its nonzero T derivative eliminates
   a temporal Killing component. The remaining time-independent spatial
   Killing equations separate the unequal Kasner powers and leave exactly
   three translations and the transverse rotation. The full-adjoint/Killing
   correspondence is a checked standard method on this actual smooth vacuum
   development. Independently, stage A's adjoint PDE proof reaches precisely
   the same complete four-dimensional local kernel without that correspondence.

3. The local-versus-global distinction is essential and correct. The rotation
   need not be a globally defined torus field for the integration-by-parts
   gate on an embedded ball/collar. With a full-rank translation lattice the
   exact stronger statement is that only the three translations descend.
   A cutoff of a local field outside the support, or a chart-with-boundary
   calculation as in the candidate, gives the same necessary local pairing.

4. The displayed coordinate momentum-density equation retains the inverse
   metric, determinant, and all connection contributions. Its integration
   identity follows with the stated density weight. Background symmetry kills
   the background Lie derivative and, by integration by parts, the linear
   background-density cross term. Matching both tensors fixes the outer flux.
   Thus every exact supported lawful completion satisfies all four finite
   identities integral p:L_Y h=0. Rotation uses the entire tensor Lie derivative.
   These statements do not require small amplitudes.

5. For an exact family through background, twice differentiating the finite
   identity correctly gives 2 integral v:L_Y u=0. Terms involving second
   family derivatives multiply the zero background differences and vanish.
   Hence a violated quadratic tangent balance cannot be repaired solely by
   changing higher-order supported coefficients of that same family.

6. Interior charge is not by itself an obstruction to fixed-exterior matching:
   the collar contributes to the same exact integral. The candidate keeps this
   distinction. It also keeps linear-source cokernel orthogonality, tangent
   integrability necessity, finite exact necessity, and nonlinear PDE existence
   separate. It does not apply an absent-KID theorem to the symmetric data.

## Adversarial controls and precision notes

The two independent scripts check the actual adjoint and momentum identity;
they do not merely assert four selected fields or re-evaluate parent formulas.
Mutation controls reject omitted metric connections, an x-y rotation, and
dropping the tensor-index terms of the yz rotation. Full records and resource
receipts are in RUN_RECORD.md and the captured outputs.

For a nonvacuous analytic false-sufficiency control inside the matching class,
take gamma=I and K=K0+epsilon b(x) I, where b is a nonzero C-infinity bump
supported strictly inside the ball. Then h=0 makes all four finite charges zero,
while H=-12a epsilon b+6epsilon^2 b^2 and M_i=-2epsilon partial_i b generally
do not vanish. For example at a point b=1 and epsilon=a, H=-6a^2 differs from
zero. Positivity and smooth support hold. This supplies the supported
interpretation of the author's symbolic b control; it is invalid constraint
data deliberately used to reject sufficiency, not a lawful counterexample.

The candidate's phrase that rotation "usually" does not descend is weaker than
the exact full-rank-lattice statement, not an overclaim. The precise result is
three global and four local modes. Neither minor wording point changes the
frozen candidate's necessary-only conclusion.

The family statement is read in a common topology allowing spatial derivatives
and differentiation under the integral, e.g. a C2 parameter family of smooth
data on the fixed compact support with the needed uniform spatial regularity.
Mere pointwise parameter differentiability without interchange hypotheses is
not covered. An isolated exact solution is not automatically a family tangent.

One reviewer reporting field is EXCLUDED: `zero_residuals: 18` in the second
source-first output is an inaccurate hard-coded summary, not a computed count.
RUN_RECORD.md identifies the actual component identities and preserves the
source/output. No verdict depends on that number. This is not a parent-proof
defect. The meaningful identities and controls are assessed individually.

## Exact surviving boundary

COMPLETE WITHIN SCOPE: the local smooth adjoint kernel of the full constraints
on the supplied embedded connected ball/collar is exactly the four-dimensional
zero-lapse space. This is a kernel classification, not a constraint-data census.

NECESSARY: four linear source pairings for a supported linear solve; four exact
finite momentum balances for any smooth lawful supported completion; and their
four quadratic tangent conditions for a suitably differentiable exact family.

NOT SUFFICIENT: these conditions do not imply the nonlinear Hamiltonian and
momentum equations, existence of a smooth collar completion for given lawful
interior data, a projected inverse with controlled estimates, a finite-dimensional
nonlinear balancing solution, or a geometrically nontrivial three-dimensional
witness. No universal impossibility of matching has been established either.

An exact solution of the full constraints with the required smooth positive
matching data would be a completion by definition and would obtain only the
conditional local development allowed by G303/G315. LG1 constructs no such new
solution and proves no all-time exterior agreement, stability, physical identity,
carrier/source/action, topology change, selected population, mass, or scale.

Review omissions: no full source-package replay, no NR1/NR2 proof review, no
numerical solve, no generic smooth-surjectivity theorem, no small-data gluing
existence proof, no evolution, no specialist human review, and no different-model
independence. Public PDF versions were read but their bytes not saved by this
reviewer. Parent owns full365; its known G325 failure remains NOT_PASSED and is
not waived. Review cannot authorize banking or promote the scientific result.

Disposition: LG1 may be used only as this reviewed UNPROMOTED conditional
necessary-gate result in the already-authorized LG2 stage. Full matching
existence/nonexistence remains open for that next stage.
