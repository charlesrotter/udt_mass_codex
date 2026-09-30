# NGD1 independent numerical review

Verdict on the saved numerical campaign: **VERIFIED-WITH-CAVEATS**. Every
preregistered trajectory was retained and independently replayed. The observed
finite-time fields, constraints and longitudinal clock readouts pass the stated
numerical gates. This does not establish continuum existence by validated
numerics, genericity, stability for untested data, asymptotics, a native UDT
field law, observer selection, or a universal redshift law.

## Context, exposure and scope

Reviewer is actual separate context `/root/ngd1_numerics`, inherited Codex model
from the parent; no different-model independence is claimed. Parent startup and
remote synchronization are attributed to the parent. I independently checked
branch `grok` and HEAD `5b4aa5456b307f2be94ccdeadf9dfd7bc6677d28`, read AGENTS,
CLAUDE's required sections, the triggered no-shortcuts/completeness/verifier
protocols, the central maintenance procedure, PLAN, EQUATIONS and freeze files.
Protected work was neither opened nor used. Only `review/numerics/` was written.

Before implementation, I was exposed to the declared metric, reduced equations,
initial-data idea and pilot workflow. I did not read or import `evolve.py` or
`analyze.py`. I implemented the NumPy/SciPy solver and the generic Ricci routine
before seeing production numerical outputs. Metadata and outcomes were exposed
sequentially during review. This is independent implementation and separate
context, not blind independent selection of equations or initial data. The
parent supplies those conditional comparison choices. The CPU and GPU codes
share the Fourier-collocation method and admitted equations; they do not share
RHS code, integrator or tensor contraction. Both use floating-point arithmetic.

All runs are in the supplied periodic, orthogonally transitive two-Killing,
areal-time, Lambda=0 comparison sector under G312's GR FILTER ONLY restriction.
The native R9 response identity remains open. Sources, twist, three-dimensional
spatial variation, general ray directions, arbitrary observers and topology
selection were not checked. Period variants change supplied data/marking and
coordinate circumference; they are not gauge-equivalent copies or scale
selection evidence.

## Independent checks and results

`independent_numerics.py` reconstructs the metric from saved P,Q,lambda alone.
Nine saved times at spacing .004 and .002 give eighth-order centered first and
second time derivatives; Fourier derivatives supply x derivatives. A generic
coordinate Christoffel/Ricci contraction then uses those metric derivatives.
No reduced RHS is substituted into those time derivatives. Reports retain
coordinate, orthonormal and dimensionless `t^2 N^2 |Ric_hat|` maxima, symmetry and
determinant diagnostics. This guards both circular equation substitution and
suppression of absolute frame residuals by a growing lapse. It remains a finite
sample check: all spatial collocation points at t=2,3 for pilots; t=2,8,15 for
the survey; and t=2,8,31 for longer challenges/period variants.

The independent CPU evolution is NumPy real-FFT collocation with SciPy DOP853,
rtol=2e-12 and atol=2e-13, starting from the saved initial state and compared at
every saved time. All 158 trajectories across 12 runs, including repeated grid
and timestep versions, were replayed; no trajectory was omitted from CPU or
original-metric checks. The reviewer's tighter CPU threshold 2e-7 was declared
before seeing pilot outputs; the parent's pilot threshold is 2e-6. Ricci gates
are 2e-5, with the dimensionless gate added and frozen before any survey output.

| Quantity | Worst observed value |
| --- | ---: |
| CPU/GPU absolute field difference, all trajectories | 3.676e-8 |
| Original-metric orthonormal Ricci maximum | 4.621e-9 |
| Dimensionless original-metric Ricci maximum | 9.647e-7 |
| Momentum constraint over every survey/challenge/period snapshot | 4.395e-9 |
| Initial field reconstruction from frozen mode/projection specifications | 7.139e-14 |
| Survey/challenge/period spatial refinement at common nodes, all field components | 1.848e-13 |
| Independent timestep halving difference, all field components | 3.447e-8 |
| Survey/challenge/period spatial refinement at common nodes, logZ | 3.331e-14 |
| Independent timestep halving difference, logZ | 5.364e-9 |

Initial-data reconstruction used the listed cosine modes and their analytic
derivatives, independently recomputed the momentum projection coefficient, and
integrated the zero-mean constraint spectrally. It confirms both the supplied
profiles and the periodic lambda constraint. The full-snapshot check avoids
relying only on terminal constraint values. `SUPPLEMENTAL.json` records each
case, all prescribed clock sample ranges and every refinement comparison.

The CPU checker passed exact homogeneous polarized Ricci data (6.94e-17), a
homogeneous unpolarized analytic evolution (1.80e-13 field error), and two
nonvacuum differential-geometric controls (2.23e-16). An off-shell smooth lambda
perturbation gave orthonormal Ricci 0.01276 and failed the vacuum criterion.
Those control geometries are tests of numerical tensor contraction, not physical
premises. No claim of exact symbolic equivalence is based on these numerical
controls. The initial schema compatibility adjustment and later addition of
the dimensionless residual diagnostic did not alter either evolution equation
or metric contraction; earlier reports and captures are preserved.
`source_history/independent_pilot.py` preserves the exact checker bytes named by
the original pilot reports; it is an inert provenance copy, not a second
maintained checker.

After completing those independent numerical checks I read central R9-R12 and
the G312 authority/NE1 reviewed qualifications. A separate direct replay of R12's
printed Bessel formula, without production code, agrees with all saved NE1
trajectories through t=32 within 4.381e-10; the pilot maximum is 1.246e-12.
`NE1_EXACT.json` binds this additional analytic-anchor check and its inputs.

## Clock interpretation and independent algebra

For a supplied fixed-coordinate emitter and receiver linked by a prescribed
lifted longitudinal null branch, `to=te+d` and `dx/dt=+1`. The independent
readout computes the final lambda trigonometric polynomial directly at x+d,
then `logZ=(lambda_o-lambda_e-log(to/te))/4`. Here d specifies branch travel
time/separation, possibly with winding on the periodic circle; it is not a
shortest spatial distance or cosmological distance. Negative logZ is a
blueshift for this convention. The endpoints alone are sufficient because
the arrival map is affine in areal time, while proper-clock increments include
the endpoint lapse factors.

The exact conditional algebra uses both lambda equations:

    lambda_t +/- lambda_x
      = t[(P_t +/- P_x)^2 + exp(2P)(Q_t +/- Q_x)^2] >= 0.

For either future longitudinal orientation at t>0, integration therefore gives
`Delta lambda>=0` and `logZ>=-(1/4)log(to/te)`. Equality requires the two
corresponding null-direction field derivatives to vanish along the path. This
bound is a consequence of the stated conditional equations; it neither derives
them natively nor guarantees total redshift. The zero-velocity homogeneous
control saturates the bound. The unpolarized homogeneous control generally does
not. All prescribed saved readouts satisfy the bound, with minimum Delta lambda
zero because the zero-velocity control is retained.

Independent survey sampled logZ range is [-0.5493061443, 1.1249531408]; the
longer challenge maximum is 1.3893147212. Fine-grid sampled maxima in the period
variants are 1.6171893713 (k=.5) and 1.5032307480 (k=1). These are maxima over
the declared sampled clocks, not certified continuum extrema. In particular,
the period-run maxima change by about 1e-4 when the fine grid adds new spatial
sample points, while common-node readouts agree to about 3e-14. This is spatial
sampling of an extremum, not a failed common-node field convergence claim.

## Reproducibility and limits

The per-run JSON reports bind input NPZ/metadata and checker SHA-256 hashes.
Exact commands, stdout, stderr, exit codes, versions, memory and timing are
preserved by the existing pinned capture utility. Longest numerical check was
17.19 seconds; largest working set was approximately 250 MiB for the combined
supplement, below the 180-second/2048-MiB per-check ceiling. No GPU was used by
this reviewer. Implementations use Python3.10.12, NumPy2.2.6 and SciPy1.15.3.

These are numerical agreement and finite residual/convergence checks, not
interval certificates or proof of behavior between all sampled times and
points. Nonpolynomial aliasing is addressed by spatial refinement, not by a
formal aliasing bound. Temporal metric differences reach a floating-point noise
floor; smaller stencil spacing need not monotonically reduce a residual already
near that floor. No all-data stability or complete-sector search is asserted.
The independent solver cannot validate an equation's physical adoption.

Final central integration and exact accepted-file binding are pending and will
be recorded separately after the parent freezes the integration candidate.

## Direct candidate review

I read `INITIAL_CANDIDATE.md` at its CANDIDATE_FREEZE hash
`0efe785af286920d52f2a8426b65502768a3fcf037d69b4dbc32ee3a6f95f7a9`
and the scoped DESCENDANT_REVIEW. Numerical maxima, restrictions, retained
outcomes and the distinction between the homogeneous control and arbitrary
homogeneous data agree with my independent computations and algebra. The
outcome-informed identity is properly disclosed. Existing R9-R12/NE1/G312
meanings survive as the impact note states; no native response law is supplied.

One wording defect was returned: “Longitudinal affine null branches” can be read
as asserting that areal t is an affine geodesic parameter. For variable lapse it
generally is not. The null trajectory obeys dx/dt=+/-1, and the endpoint arrival
map to=te+d is affine. Removing “affine” from the trajectory description and
explicitly distinguishing the arrival map repairs the wording without changing
the readout, identity, fields or scientific conclusion. Preserve the initial
candidate and record this clarification in the reviewed interpretation.

Re-review: `REPAIR.md` implements that clarification and `REVIEWED_RESULT.md`
controls its use. The affine tangent is proportional to
`N^-2(1,+/-1,0,0)`: the derivative of N^-2 along the ray cancels the conformal
base Christoffel term. Thus the proposed repair is mathematically sound and
leaves the endpoint readout and every numerical output intact. The frozen
initial candidate retains its original hash. The reviewed disposition also
explicitly distinguishes the later plot's d=.25,.5,...,8 visualization samples
from the original frozen clock queries. No numerical/argument objection remains
to this bounded interpretation; exact central binding is still pending.
