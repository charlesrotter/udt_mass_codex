# Authorized G313 curvature-to-phase/current test

Status: BOUNDED MATHEMATICAL EXPLORATION; NOT ACCEPTED SCIENCE.
Authorization: Charles's 2026-09-06 “proceed” to the complete-cycle proposal.
Source snapshot: b304c89f567b9bc301239b631d7a84c91485767d, branch grok.
Budget: 90 minutes from 18:38:22 UTC; hard return by 20:08:22 UTC.

## Question, quantifier and exact frozen recipe

Use only G313's supplied smooth constant-A plane-wave family

    g=-2 du dv+dx^2+dy^2+A(x^2-y^2)du^2,

with every real constant A!=0 on a regular local coordinate patch, signature
-+++, and supplied time orientation. A=0 is the flat/degenerate control, not
silently discarded from any claimed universal statement. No A(u), different
wave family, perturbation census, global solution or physical metric is selected.

Let W be the Weyl tensor of this metric, all four indices lowered. Freeze the
following geometric recipe, with coefficient exactly one for both terms:

    starW_abcd = (1/2) epsilon_ab{}^{mn} W_mncd,
    B_abcd = g^{ef} g^{hi}
             (W_aech W_bfdi + starW_aech starW_bfdi).

The Hodge dual acts on the FIRST antisymmetric pair and uses the metric volume
form. Start with epsilon_uvxy=+sqrt(-det g); reversing proof orientation must
not change B. Both inverse metrics and the Hodge half-factor are load-bearing.
Convention for checking curvature:
R^a_bcd=partial_c Gamma^a_db-partial_d Gamma^a_cb
       +Gamma^a_ce Gamma^e_db-Gamma^a_de Gamma^e_cb,
R_abcd=g_ae R^e_bcd. Opposite curvature sign cannot change this quadratic B.

Test whether B=beta tensor beta tensor beta tensor beta with a nonzero future-
raised null real beta, whether that root is unique for this fixed recipe and
time orientation, whether d beta=0 and div(beta#)=0. If so, construct the local
phase primitive dTheta=beta and candidate current C=beta#. Determine the induced
nonnegative phase/label quotient measure from i_C vol_g; assess the G352 product
and local observer readout, with every remaining label/spacing/support choice
and normalization exposed. Do not insert a prescribed phase or free amplitude
function to make the recipe work. A failed test may return a partial construction
or obstruction, not an invented repair law.

The recipe is a CHOSEN MATHEMATICAL CONSTRUCTION, not a new physical equation,
energy tensor, adopted current, carrier or selected content. Mathematical
familiarity supplies no physical premise. A unique root for a fixed recipe does
not prove that the theory uniquely chooses that recipe or its coefficient.

## Source ownership and choices

- G313 EXACT_DERIVATION sections1,5,6 and current AUDIT_REPORT admit this exact
  Ricci-flat metric branch and retain the scale/history/population boundary.
  Its relation to the active vacuum arena retains inherited owner-provisional
  G312/Universal-Reciprocity premise stamps. No field equation is changed.
- G351/G352 conservation/readout remain OWNER_ADOPTED_PROVISIONAL_PREMISES.
  Their continuous phase-independent nonnegative product remains CHOSEN/SUPPLIED.
  A geometric induced measure here is not automatically their physical mu.
- The current representation reviewed at b304c89f remains UNPROMOTED. It informs
  the question but is not an accepted dependency; derive the local measure/readout
  identities directly for this metric, or explicitly label any candidate-only
  dependency. No prior candidate is silently promoted.
- Pinned-by-THEORY within the source domains: G313's metric family and metric
  differential operations; G352's readout/gauge definitions as comparison targets.
  The exact quadratic recipe is explicitly CHOSEN, not pinned by theory as physics.
- Free-and-explored: A and its signs, coordinate/volume orientation, the retained
  regular patch, finite observer controls and exact witness parameters. For
  displaying components take partial_v future; the supplied time orientation,
  not a preferred observer or physical clock, resolves a possible root sign.
- Finite retained label patch, cross-phase identification and DeltaTheta>0 are
  mathematical query choices when needed, not selected population/support/spacing.
  No physical habit-pin, fitted normalization, action, boundary term or cutoff.

## Required distinctions and counterchecks

Check full tensors, not merely B_uuuu or one observer contraction. Derive and
verify nullness, future sign, exterior closure and divergence. Include an
explicit nonclosed/nonconserved control so an always-zero differential routine
cannot pass only parallel examples. Check ordinary metric sheet area with
nonconstant cuts, and nonnegative quotient measure rather than a signed count.

Separate four operations: passive coordinate changes (including positive null
coordinate rescaling), G352's common positive affine phase/spacing gauge at
FIXED current/measure, physical metric homothety g->s^2 g, and changing the
chosen recipe coefficient. None is silently substituted for another. Track
covector versus raised-vector, volume/area and observer scaling. State units
and whether a finite physical count would need an additional identification.

The scalar zero-curvature control, A signs and finite positive rescalings test
this recipe's scope. Failure at A=0 blocks a nonzero phase from this recipe there,
not the existence of supplied phases in flat geometry. Successful local algebra
does not establish stability under general perturbation, a preferred history,
finite populated patch, canonical cross-phase labels, or a universal object.

## Methods, resource ceiling, freeze and review

Exact local tensor/differential geometry, analytic reasoning, symbolic/rational
CPU recomputation only. No GPU, floating tolerance, mesh, approximation, PDE
production solve, disk archive, or external physical model. Python3.10.12 and
SymPy1.13.1 measured; available-memory snapshot123790 MiB is not a reservation.
One symbolic check at a time per context, at most author plus one reviewer;
60-second per-check timeout, target under512 MiB, small 4D tensors. Read-only
premise/repository controls are separately timed; the full premise audit has a
900-second limit and must be reported with actual child outcome.

Workspace: this new candidate directory plus bounded /tmp scratch. Use existing
sound tools where applicable, not new infrastructure. Save commands, versions,
inputs, separate stdout/stderr, child exits, failures and SHA256 correspondence.
Finite/symbolic checks support the load-bearing analytic argument; counts are
not a completeness theorem, independent proof or physical confirmation.

The parent considered the algebraic root route during MAP/PONDER, including
possible normalization/support limitations. This is mathematical discovery,
not an outcome-blind observational preregistration. Freeze this exact recipe
before executing outcome checks, then freeze candidate bytes before direct review.

Authorized cycle: construction and checks; one fresh separate-context source-
first adversarial reconstruction followed by direct frozen-candidate review;
at most ONE source-preserving same-premise candidate repair/re-review. Preserve
the original candidate and all review history. Record exact exposed model or
UNKNOWN; fresh context does not imply different-model review. Review general
argument, tensor completeness, native/physical distinctions and false passes.

Return a reviewed conditional candidate, partial/narrowed result, refutation or
unresolved objection, whichever survives. A fidelity check of closing documents
is included, not another independent scientific review. Commit logical evidence
changes and push grok after synchronization/review/permission checks; a commit
preserves, never promotes.

## Stops and preservation

Stop at the reviewed bounded return, hard budget, or actual blocker. No new
scientific question, physical premise, physical content/source/population
selection, accepted grade/dependency, registry, LIVE, HANDOFF, manuscript,
CANON or accepted-source edit. No mount/repair, worktree pruning, protected
payload inspection, infrastructure refactor or historical-session resume/fork.
The explicitly authorized reviewer is a genuinely new context without history.

At orientation HEAD and origin/grok matched the source snapshot after successful
fetch/pull. Tracked files clean; original46 unrelated untracked entries preserved.
Backup completeness and pre-reboot unsaved-state disposition remain UNVERIFIED.
ScratchDisk blocks archive-dependent tasks only and is unnecessary here. Completed
infrastructure and the fixed-snapshot manuscript do not settle this new candidate.
