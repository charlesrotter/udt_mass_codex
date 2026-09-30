# NGD1 substantive candidate and fidelity review

Verdict: **VERIFIED-WITH-CAVEATS** for the fixed conditional candidate and its
scoped descendant assessment, read with the accepted semantic repair below.
No blocking scientific defect or scientific solver repair was found. The result remains conditional numerical evidence,
UNPROMOTED, plus the exact identity in its declared ansatz. It does not close
native UDT dynamics or select observers, physical content, a scale or canon.
Final central integration and accepted-file attestation are separate gates.

## Actual review context and versions

Reviewer `/root/ngd1_equations`, the same actual separate scoped context that
produced EQUATION_REVIEW.md. Parent-inherited Codex model; exact identifier not
exposed here, different-model independence UNTESTED. Parent startup/sync is
attributed; reviewer independently checked grok HEAD
`5b4aa5456b307f2be94ccdeadf9dfd7bc6677d28` and scoped status again. Protected work
was not opened, mined or modified. Writes are confined to review/fidelity.

The accepted direct-review candidate is INITIAL_CANDIDATE.md SHA256
`0efe785af286920d52f2a8426b65502768a3fcf037d69b4dbc32ee3a6f95f7a9`;
DESCENDANT_REVIEW.md SHA256
`d8b76bf4aa8fd6561441d9af3ac101fceaee2f6f2f9c3adfd29f84ed9dd40fe8`.
All six CANDIDATE_FREEZE bindings matched at review. Frozen survey code/spec
bindings also matched. Hashes establish correspondence, not chronology or truth.

Exposure is explicit: the earlier equation review saw the target equations and
NE1 proof but independently built metric-to-Ricci algebra. This direct stage
also read production evolve.py/analyze.py, survey freeze/supplement, metadata,
saved fields, numeric-review code and reports, candidate/descendant text and
the figure. Reviewer guidance on the precise Taub baseline, equality scope,
profile projections and sampling limits reached the parent before this fixed
candidate was saved. Thus "before direct review" means before review of this
fixed file, not blind author construction or absence of prior review guidance.
The outcome-informed identity is correctly disclosed in the frozen candidate.

## Argument tested and surviving scope

The independent original-Ricci derivation in EQUATION_REVIEW.md remains valid:
both evolution equations, both lambda constraints and all off-sector components
are accounted for at t>0. G312 GR FILTER ONLY qualifies the imported comparison
arena; R9 does not supply the missing E=Ric identification. The extra unpolarized
metric coordinate Q releases the polarized restriction while leaving periodicity,
orthogonal transitivity, two Killing fields, vacuum/Lambda=0 and areal marking
supplied. It is not coverage of every metric with two Killing fields or all UDT.

For s=+1 or -1 the actual future longitudinal null lift has
`x(t)=x_e+s(t-t_e)`. The two constraints give

    d lambda(t,x(t))/dt
      = lambda_t+s lambda_x
      = t[(P_t+s P_x)^2+exp(2P)(Q_t+s Q_x)^2] >= 0.

This is an exact algebraic identity followed by integration, not inference from
sampled monotonicity. Together with the independently checked affine null
tangent and fixed-coordinate clock factors it yields

    log Z = (lambda_o-lambda_e)/4 - log(t_o/t_e)/4,
    log Z >= -log(t_o/t_e)/4.

The right side is specifically the constant-lambda, zero-velocity Taub control
with the same marked query. Attempted strengthenings fail: a different
homogeneous solution can have `lambda=lambda0+v^2 log(t/t0)`, so the inequality
does not order arbitrary homogeneous controls; neither does it order full
Q evolution against a different polarized history. Equality requires the two
directional field derivatives to vanish along the chosen segment and does not
establish global homogeneity. Nonnegative correction does not imply Z>=1.
These distinctions are present in the fixed candidate.

The observer congruence is supplied and can accelerate. The clock law is a
metric query on the conditional geometry; calling its geometric readout
"native" would not select a native null protocol or native metric evolution.
EQUATIONS.md's frozen shorthand "Native readout, conditional geometry" must be
read under this explicit candidate qualification. The final candidate itself
correctly calls it the ordinary metric proper-clock/null readout. No frozen
equation file needs scientific alteration.

On a periodic x-circle, the momentum current must have zero mean; the PDE
propagates this compatibility condition. Production constructs the initial
constraint and evolves lambda rather than resetting it to a spatial primitive
on each step. Independent full-snapshot constraints therefore test an actual
evolution condition. The x lift/winding is part of the query. Changing k changes
supplied geometry/data/marking; it is not a coordinate invariance check, chosen
physical scale or infinite-volume limit. Candidate caveats preserve these facts.

## Independent recomputation from saved artifacts

`check_saved_clocks.py` imports neither production code nor numerical-review
code. It reconstructs Fourier coefficients and displaced lambda values with
dense complex exponential matrices, then computes clock ratios directly.
It differentiates all saved P,Q,lambda fields using a cotangent collocation
matrix, providing another implementation of the momentum/mean-current check.
This is different implementation, with the same spectral approximation and
NumPy arithmetic; it is not different-method continuum certification.

All final N256 survey, challenge and k=.5,1 period histories were loaded and
checked. For the survey, all 192 case/query summary rows agree with the parent
clock table within `4.330e-14`. The final challenge has 480 case/query rows and
each period variant 112. Sampled logZ ranges independently recovered are:

| Final run | Minimum | Maximum |
| --- | ---: | ---: |
| survey | -0.5493061443 | 1.1249531371 |
| challenge | -0.5493061443 | 1.3893147212 |
| k=.5 | -0.5493061443 | 1.6171893713 |
| k=1 | -0.5493061443 | 1.5032307480 |

The maximum independently recomputed full-snapshot momentum residual across
these four sets is `7.520e-10`; maximum mean current `4.444e-11`. Dense DFT
roundoff gives minimum delta relative to the constant-lambda control about
`-1.3e-14`, consistent with its exact zero control. This is a numerical
reconstruction check, not the proof of the exact sign bound.

Independent inspection of raw seed velocities versus the saved initial fields
finds maximum relative L2 projection change `0.8084393863` at profile_a0_p2.
Thus the twelve spatial-profile cases are projected admissible families, not
small perturbations. The two designated perturb_a2 cases instead change their
second velocity mode by 0.1%; all have initially zero profiles and meet the
periodic constraint. The final candidate distinguishes these categories.

Machine output and input hashes are in SAVED_CLOCK_CHECK.json, with stdout and
empty stderr retained. Command:

    timeout 180s python3 udt_gpu_time_live_discovery_2026-09-30/review/fidelity/check_saved_clocks.py > udt_gpu_time_live_discovery_2026-09-30/review/fidelity/saved_clock_check.stdout 2> udt_gpu_time_live_discovery_2026-09-30/review/fidelity/saved_clock_check.stderr

Exit 0; 0.591 seconds, peak RSS 187040 KiB. CPU<=180s/address-space<=2GiB
limits enforced inside the script. No GPU use. Metadata independently totals
12 runs/158 repeated trajectory executions, 32.344734994 summed evolution
seconds, peak allocated GPU memory 4119552 bytes, and 118247476 NPZ bytes.
These figures are not a GPU/CPU performance comparison or continuum proof.

## Numerical evidence boundaries and figure

The separate numerical reviewer owns the DOP853 replays and generic
Christoffel/Ricci contractions. I inspected that implementation and its result
summaries; I did not independently rerun all those checks. Its time derivatives
come from saved metric histories, not substitution of the production RHS,
which avoids a circular residual. Both orthonormal and t^2 N^2-scaled Ricci
diagnostics are retained; the latter addresses large-lapse suppression.
Sampled maxima, CPU differences and refinements support the candidate's
declared finite numerical scope. The candidate correctly discloses shared
Fourier spatial discretization, finite stencil centers, finite emitter mesh,
roundoff-limited temporal differentiation and absence of an interval enclosure.

The plotted three amplitudes are prelisted phase0 cases, and all other outcomes
are retained. The figure correctly labels conditional geometry, areal time,
longitudinal branch duration and the zero-velocity control. Bands are sampled
emitter ranges, not uncertainty or convergence enclosures. Its d=.25,.5,...,8
samples are additional post-outcome visualization of already saved histories;
the preregistered clock table uses d=1,2,4,8. This illustration must not be
described as expanding the preregistered tests. No defect in the plotted clock
formula was found. No inference about general null directions is warranted.

## Descendants, verdict and omissions

### Actual same-premise semantic repair review

The numerical reviewer identified ambiguous candidate wording, "Longitudinal
affine null branches have dx/dt=+1 or-1". I inspected REPAIR.md SHA256
`cf397b818e1248af175cace817c81b0e4fc5216d5774a7561ef6015f25179187`
and REVIEWED_RESULT.md SHA256
`3c044c464096529d9fa636b98310f95a62d314f9da6c758caf9e225c692981d1`.
The repair correctly distinguishes the affine coordinate arrival map
`t_o=t_e+d` from an affine ray parameter: t generally is not the latter, while
an actual affine null tangent is `C N^(-2)(1,+/-1,0,0)`. This matches the original
metric/geodesic check and preserves both endpoint frequency and proper-clock
derivations. It is a minimal semantic repair, not a changed equation or numerical
repair. The frozen candidate is preserved. The wrapper correctly records prior
review guidance, outcome-informed identity and added illustrative figure samples.
Verdict after actual argument re-review: repair/wrapper accepted with the same
conditional and numerical limits; no unresolved objection. No rerun of unchanged
numerical grids or full source-package tests is needed for this wording repair.

DESCENDANT_REVIEW correctly leaves R12/NE1's exact polarized argument unchanged,
uses the R10 comparison as an explicit condition, and leaves the R9 response
identity unresolved. Clock/readout results supply the query without choosing
the observer/population. Transverse/path data remain necessary outside this
longitudinal subset. The positive and negative R18 connections are reconsidered:
these finite histories neither close native admission nor prove UDT insufficient,
and they do not refute prior clock-score obstructions with different hypotheses.
No new protected/carrier/mass/source dependency or X_max construction is inserted.

No additional scientific repair is required. The accepted parameter clarification
and provenance qualifications above control the frozen candidate's interpretation. What survives is a validated
finite comparison engine and campaign, together with an exact branch-relative
clock inequality. Formal numerics, every-time curvature control, generic-data
stability, general directions, physical adoption and native selection remain
unproved. Final integration/source binding, full406 and repository closure are
not certified by this direct-review verdict.
