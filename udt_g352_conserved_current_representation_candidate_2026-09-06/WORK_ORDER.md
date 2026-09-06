# Authorized conserved-current representation test

Status: BOUNDED MATHEMATICAL EXPLORATION; NO ACCEPTED SCIENCE CHANGE.
Authorization: Charles's 2026-09-06 “Proceed” to the complete-cycle proposal.
Source snapshot: `3a31db478b094efc9bce5291349b552aed95059c`, branch `grok`.
Budget starts 2026-09-06 17:54:16 UTC; hard return by 19:24:16 UTC.

## Question and maximum conclusion

On a sufficiently small regular caustic-free phase patch, with smooth nonnegative
label density, does the supplied G352 product

    dXi=(|dTheta|/DeltaTheta) tensor dmu

have a covariant representation by C=rho k, k=grad Theta, div C=0? Under precisely
which conditions is this representation possible and unique for FIXED data;
does -g(u,C) equal the prescribed Gamma? Conversely, what conserved currents
does that product omit, and which data remain free at fixed metric and phase?

This is a targeted local representation/data-ownership question. No physical
current or new conservation law is adopted. A scalar/vector/form construction
is a mathematical representation only if the argument supplies the connection;
calling it covariant is not evidence that the metric supplies physical content.
Allowed return: reviewed conditional candidate, narrowed result, refutation, or
unresolved objection. No claim about all possible physical realization routes.

## Premises, scope, and choices

- Metric-led, arbitrary supplied smooth time-oriented Lorentzian 4-metric with
  signature -+++. No field equation, metric selection, action, carrier, or source.
- G352 supplies a smooth phase with nonzero future null raised gradient and
  fixed positive spacing. Supply a smooth regular flow patch and cross-phase
  identification of two transverse labels, transported along k. Local chart,
  orientation and proof slices are mathematical choices, free-and-explored;
  no preferred spacetime orientation or reference slice is physical input.
- G351's conservation of a supplied finite nonnegative countably additive label
  measure and G352's clock-rate readout retain OWNER_ADOPTED_PROVISIONAL_PREMISE
  status. The phase-independent continuous product is CHOSEN/SUPPLIED, not a
  further owner-adopted premise or a metric consequence.
- Restrict this test to the smooth nonnegative density part on a relatively
  compact regular label chart. Smoothness and no-caustic restriction narrow the
  question, not the accepted measure theory. Allow zero density division-free.
  Ratios only where both required densities are nonzero. Singular/atomic
  measures and global measure-valued currents are outside this smooth test.
- Pinned-by-THEORY within the conditional source domains: null quotient metric
  and cut-gradient area cancellation (G349 sections 1–2), regular density s/J
  (G351 section 3), Gamma=omega s/(DeltaTheta J) and positive affine phase gauge
  (G352 sections 1–4). None pins s, population, DeltaTheta, or physical phase.
- Free-and-explored: smooth nonnegative label densities, mathematical initial
  data, transverse phase-dependent measure families as comparison objects,
  local charts/cuts and exact witness parameters. A comparison outside the
  chosen product is not an adopted new physical branch. No physical habit-pin.
- The prior normalized-cone extension at f1409873, reviewed at 3a31db4, remains
  an UNPROMOTED CONDITIONAL CANDIDATE. This test may start directly with G352's
  supplied phase and must not silently upgrade that candidate to accepted input.

## Methods and falsification ceiling

Use exact local differential geometry, flow coordinates, volume densities/forms,
and bounded symbolic/rational examples. Derive any divergence relation from the
measure representation; do not import a wave, Maxwell, transport, or field
equation as a physical law. Check quantifiers and both directions of any proposed
equivalence, normalization, coordinate dependence, and the readout's exact type.

Possible outcomes include exact conditional representation, representation only
with additional compatibility conditions, or obstruction. A surviving arbitrary
population function defeats selection from these data alone, not every native
realization route. A conserved current failing phase-independent factorization
defeats equivalence with the product, not G351/G352 within their conditions.
An area/volume Jacobian mismatch or observer/cut counterexample defeats the
claimed representation as stated and must be retained and repaired or reported.

Mathematical exploration may precede candidate freezing; the preceding proposal
already exposed the current ansatz and alternative outcomes. This is not blind
observational preregistration. Preserve the initial frozen candidate, actual
commands/outputs, failures, review exposure and any repair history.

## Resources, verification cycle, and stop

Repository workspace: this new candidate directory only, plus bounded /tmp
scratch. One author construction pass; one fresh separate-context source-first
adversarial review followed by direct candidate review; at most ONE same-premise
candidate repair/re-review if needed. Reviewer must examine the general argument
and independently recompute a load-bearing witness, not merely replay counts.
Different-model status is UNTESTED unless actually exposed and established.

CPU exact/symbolic only, Python 3.10.12 / SymPy 1.13.1 measured at start.
No GPU, grid, floating tolerance, production PDE solve or resource expansion.
At most one check process per context, two such processes concurrently; each
check has a 60-second timeout and target memory below 512 MiB. These are chosen
operational ceilings, not measured peak use. Read-only premise/repository checks
are separate; retain timeouts/failures. The parent sandbox's `free -m` snapshot
reported 124032 MiB available; it is not a reservation or a host-process audit.

Run the current premise audit and relevant checks before banking the candidate.
Authenticate frozen sources and initial candidate bytes, catch intended code
defects and check actual child exits/results (a capture runner exit is not a
scientific or test verdict). Record checks omitted. Preserve and commit one
logical evidence change at a time on grok and push after sync/permission checks;
a candidate commit preserves, never accepts.

Stop at the reviewed bounded return or budget/real blocker. No new question,
premise adoption, physical-content/population/source selection, accepted grade,
registry, LIVE, HANDOFF, manuscript, CANON or accepted-source change. No disk
mount/repair, worktree pruning, protected-payload inspection, infrastructure
refactor, or resumed/forked historical research session. The explicitly approved
review uses a new context without inherited conversation.

## Preservation and operational boundary

At orientation HEAD and origin/grok both equal the source snapshot; fetch/pull
succeeded. Tracked tree clean, original 46 unrelated untracked entries preserved.
Those paths are status metadata only; payloads must not be inspected or staged.
Backup completeness and pre-reboot unsaved-state disposition remain UNVERIFIED.
ScratchDisk blocks archive-dependent tasks only and is not needed here. Completed
infrastructure and the fixed-snapshot manuscript do not establish this science.
