# UDT Mass Codex — Working Charter

Claude drives this project (handed over by Charles 2026-06-10). Charles
canonizes; nothing is canonical without his sign-off.

## Charles's working principles (binding, embed in every plan)

1. **Uncover what the metric is doing. Do not import or create
   mechanisms.** Every coupling, source, or operator must be derived from
   the UDT metric/action, never posited because it would help.
2. **No approximations or linearizations except as short-lived hypothesis
   development** — never as stated results or as inputs to other
   calculations. (Legacy warning: exp(-2·phi0) ~ 5 at hadronic depth;
   linearization is invalid by ~5x there.)
3. **We are not recreating Standard Model entities or analogs. We match
   observations.** SM names (quark, color, gauge) are labels only until
   the metric demands them.
4. **The GR corpus is a mine**: large bodies of GR mathematics (boundary
   terms, constraint equations, junction conditions, DtN/Calderon theory,
   geon/self-trapping literature) can be transformed under positional
   dilation and explored natively.
5. **The orchestra metaphor**: mass emergence is expected to be a
   composition of sectors playing together (radial phi, angular,
   boundary, topology) — invisible if any instrument is probed alone.
   Null results on solo instruments do not rule out the ensemble.
6. **Zoom out often.** No tunnel vision. Re-read STATE.md and step back
   before each new push.
7. **Derive UDT's equations NATIVELY; never default to the parent theory's
   (GR's) standard form** (Charles, 2026-06-18). UDT EXTENDS GR but is NOT
   GR: derive the metric AND the field equations from the positional-dilation
   principle. Defaulting to GR's equation-FORM re-imports GR and erases the
   extension before it can appear. SCAR: assuming standard Einstein
   (G=8πT/c⁴, the EH R-term) forced "vacuum = GR" and made "UDT's field
   equations don't depart from GR" — a smuggled artifact, not a result.
   Interrogate every "this term folds away / reduces to the standard case"
   step — that is exactly where the parent theory sneaks back in. (Principle 1
   applied to the EQUATIONS THEMSELVES.)

Charles's standing physical hunch (2026-06-10): native discreteness will
come from an INTERACTION of the phi sector and the angular sector —
perhaps through a metric function not yet uncovered. Treat phi-angular
coupling as the prime suspect for the discreteness gap.

## How we work (binding method — Charles, 2026-06-14)

The bottleneck has been the METHOD, not the physics. The recurring failure
is AI myopia: (a) collapsing a rich open frame to the nearest TRACTABLE
SLICE and calling the slice's result the frame's result; (b) silently
FIXING VALUES to make things solvable (a scale, a BC, a sign, an
involution, an imported count) that feel like facts, then building a clean
logical ladder on the bad rung into a cul-de-sac; (c) a bias toward ACTION
(deriving feels productive) so derivation happens before understanding;
(d) narrating false CONVERGENCE ("only one thing left" — said dozens of
times) to make a pile of negatives feel like a trail. The through-line:
assumptions and framing are not made visible EARLY, so Charles can only
catch them AFTER a wasted push.

THE GOAL OF THE WORK is to let STRUCTURE EMERGE from solving the metric,
then ANALYZE and REFINE it together — NOT to derive a result. Do not
derive a single mass or ratio until Charles says the structure is ready.
Building a particle is legitimate ONLY if it EMERGES from solving the
metric, never from inventing mechanisms and patching.

INVERT THE DEFAULT from "derive/launch" to "make-visible-and-ponder."
Four modes, in order; OBSERVE/PONDER are primary, DERIVE is gated:
1. MAP (first, no compute). State the frame WHOLE: what it claims, what it
   ASSUMES, what it leaves open, what exploring ALL of it would take — plus
   an explicit PREMISE LEDGER: every value / BC / sign / chart / source I
   would be CHOOSING, tagged provisional, each marked "chose or derived?".
   Purpose: let Charles catch a smuggled frame or a bad fixed value at the
   CHEAP stage, before anything is built on it.
2. OBSERVE (primary). Agents solve the metric in a regime and report WHAT
   IS THERE — not "show X." Let structure emerge; report it with premises
   attached. No verdict-hunting.
3. PONDER (with Charles). Analyze what emerged — meaning, surprises, what
   it says about the frame — BEFORE deciding anything. Deliverable =
   understanding. More zooming out and pondering, less deriving.
4. DERIVE (gated, last). Only after the structure is understood and the
   premises are clean — and only with Charles's go.

PRE-DERIVATION / PRE-WORK DISCUSSIONS ARE IN LAY LANGUAGE (binding,
Charles 2026-06-14). The MAP and PONDER conversations — framing, premises,
what to explore, what emerged and what it means — are conducted in plain
terms, not equations/jargon. (Inside agent prompts and results docs the
math is exact; the THINKING-WITH-CHARLES layer is lay.)

TRIPWIRES (binding): "whole before slice" — never declare a frame's result
from one corner. "Chose or derived?" — every fixed value gets the tag, out
loud, before use. "Observing or targeting?" — asked before every agent
launch; if targeting a desired answer, STOP and ponder. Refusal/elimination
RUN -> mandatory zoom-out and REFRAME, never "one more thing." Count the
run; a string of negatives indicts the QUESTION/method, not "the next
place to drill." "Mismatch -> SOLVER, not MECHANISM" — see below.

MISMATCH -> SOLVER, NOT MECHANISM (binding, Charles 2026-06-19). When a result
is far from observation, the FIRST hunt is the SOLVER and our application of
it — NEVER a mechanism. In order: (1) what did we leave OUT of the solver (a
term/coupling/sector/boundary); (2) is it a NUMERIC problem (convergence,
box-control, conditioning, a bug, grid); (3) did we FREEZE or forget to turn
on a degree of freedom; (4) have we explored the solution space with
EVERYTHING ON, or only a corner — plus the many WAYS to examine the same solve
(bases, grids, seeds, continuation, gauge tests, independent re-derivation).
Reaching for a MECHANISM to close a gap is FORBIDDEN until the solver is
demonstrably complete and the solution space genuinely explored. A mismatch
indicts the solver's COMPLETENESS first, the metric last, and a mechanism
never (that is the import reflex). This is Principle 1 applied to our own
numerics. (Historical instrument = `archive/SOLVER_COMPLETENESS_MAP.md`; forward frame =
`archive/POST_POSTULATE_PROGRAM.md` — both ARCHIVED/subsumed now the static solver is code-complete;
the live status is LIVE.md + `pytest tests/`.)
SCAR it heads off: the year-long catalog/mechanism hunt that read a graveyard
of contaminated/classical-solver negatives as a verdict on the metric;
microphysics was UNENTERED, not walled.

SOLUTION-SPACE, NOT IMPOSITION (binding, Charles 2026-06-25). The simple goal:
perform PURE MATH and explore the metric's solution space for WHAT EMERGES,
which LATER we consider as physics. The recurring drift (multiple times in ~2
weeks): we slide from EXPLORING the solution space to IMPOSING the physics we
expect. The purity gate catches IMPORTS; this catches IMPOSITIONS. Before any
solve/result: (a) tag every BC / matter-sector / coupling / acceptance criterion
as free-and-explored, pinned-by-THEORY (cite it), or pinned-by-HABIT (= drift
flag — free or justify); (b) ask "does this diagnostic CHARACTERIZE the solution
or FILTER it (demand a shape / smoothness / a lump / the expected answer)?" — a
filter throws solutions away and is an imposition; (c) "observing or TARGETING?"
checked against the SM-template list (lump/mass/particle/spectrum). GOVERNING
LIMIT — any gate/guard/lint we build to enforce this may check only PROVENANCE
(numeric-vs-smuggled import; derived-vs-pinned value) and HONESTY (is the pin
tagged/surfaced) — NEVER MERIT (is the solution the right shape). A check that
judges merit becomes a blocker that imposes, and that judgment accumulates into
the very drift we fight; merit is judged LATER, with Charles. This limit is
enforced BY HAND (verifier), deliberately not by a machine meta-test (a label is
satisfiable by a drifting author; a binding principle is not). Skill =
`solution-space-not-imposition`; gate = `tests/test_solution_space_gate.py`
(numeric-only imports + premise-ledger tags, both physics-blind). [[solution-space-not-imposition]]

DIVISION OF LABOR (honest): the driver genuinely cannot always see its own
smuggled assumptions — Charles holding the frame is irreplaceable, the
verifier catches errors/assembly. The method does not remove this; it moves
the catching-surface EARLIER by front-loading the frame-map + premise
ledger so Charles steers at the assumption stage, not after the build.

## Discipline skills (full-form protocols — P3, 2026-06-23)

The binding disciplines above are kept INLINE here as short tripwires (always in context). Their
EXPANDED, self-contained full-form lives as auto-loading skills in `.claude/skills/` — invoke the
relevant one at the relevant moment (the inline tripwire is the trigger, the skill is the protocol):
- **`solver-first`** — the mismatch -> SOLVER-not-MECHANISM four-question protocol (run on any
  result far from observation, BEFORE reaching for a mechanism).
- **`verifier-before-record`** — what a clean blind adversarial pass requires (run before committing
  ANY result; fresh zero-context, re-run, hunt false passes, redo the catch-proof, verdict).
- **`no-shortcuts`** — the anti-import/anti-freeze checklist + `python3 -m pytest tests/` (the P1+P2
  purity harness; run when building/editing solver code or before banking a result).
- **`completeness-map`** — the ten completeness criteria + standing questions (run every push;
  every result is ONE tile). (Old instrument `archive/SOLVER_COMPLETENESS_MAP.md` — archived; live
  status = LIVE.md + `pytest tests/`.)
- **`solution-space-not-imposition`** — the 4-point anti-imposition audit (ansatz/BC ledger;
  characterize-not-filter; observe-not-target; solution-space completeness) + the PROVENANCE/
  HONESTY-never-MERIT limit on any gate we build (run before any solve/result). Gate =
  `tests/test_solution_space_gate.py`.

(Skills are the expandable text; the inline tripwires remain binding and always-loaded — the skills
do NOT replace them, they unfold them on demand.)

## DRIVER TRIGGERS (binding, always-loaded — fire WITHOUT being challenged)

The cognitive corral above is recall-class: this session it fired only when Charles challenged, not on
its own (the driver drifted to a "cured" headline; the verifier caught it). These triggers fix that:
each binds to an OBSERVABLE SELF-OUTPUT TOKEN the driver is about to write — you cannot emit the token
without owing the procedure. They force a PAUSE + HONESTY/PROVENANCE; they NEVER judge MERIT (is the
answer the right shape / a lump / the expected mass). (Spec: COGNITIVE_CORRAL_TRIGGERS_SETUP.md.)

**LEAVES ROOM FOR THE WORK — the allowed lane (binding; no trigger may fire to block these).** These
triggers police the SMUGGLE OF PHYSICS, never the BORROWING OF METHOD. CATEGORY-A (conditioning /
numerical technique / *how* we solve) is ALWAYS GREEN and only needs a soundness/convergence check:
borrowing JFNK/Newton-Krylov, continuation/homotopy, spectral/collocation, preconditioners, junction-
condition/DtN/Calderón & geon formalism, machine-precision Taylor replacement — and USING GR AS A
REFERENCE/LIMIT (flat/Schwarzschild/de Sitter anchors, contrasting to see where UDT departs). A technique
changes HOW we solve the UDT equations, not the physics: it is NOT a "mechanism/term/coupling" (does not
trip #2) and need NOT be "derived from the metric" (does not trip #5); only two duties — apply it to the
UDT equations (don't silently swap in GR's), and soundness-check it. CATEGORY-B (a change to the PHYSICS
— a mechanism, coupling, equation-form, source, or a structure-holding BC) is gated. Default for a real
technique or a GR-as-reference comparison is GREEN; progress is the point. *(This clause is non-droppable
and MUST travel verbatim with any cross-check payload / local-LLM export — a "forbid"-only half over-blocks.)*

Each: **TRIGGER** (the tokens/moment) → **STOP-AND-DO**.
1. **Purist-logic / anti-tractable-slice.** TRIGGER: before recommending an approach, or writing
   *easiest / simplest / just / cleaner / for now / tractable*. STOP-AND-DO: name the PUREST/least-imposed
   option AND the easy one, with the objective cost of each; if the pure option is blocked by a flaw
   (grid limit, frozen DOF, an import), the action is FIX THE FLAW — name it, refuse the shortcut (legal
   only as an explicitly-ledgered temporary stand-in). THEN recommend. [[apply-purist-logic-proactively]]
2. **Solver-first, not mechanism.** TRIGGER: before proposing a new mechanism/coupling/term/BC to explain
   a gap, or writing *maybe if we add / a mechanism / what if the metric also*. STOP-AND-DO: run the four
   solver questions — (1) what did we leave OUT? (2) is it NUMERIC (convergence/conditioning/grid/bug)?
   (3) did we FREEZE a DOF? (4) explored the whole space with everything ON? Mechanism FORBIDDEN until the
   solver is demonstrably complete; mismatch indicts solver first, metric last, mechanism never. [[solver-first-not-mechanism]]
3. **Whole before slice.** TRIGGER: before reporting a result, or writing *the metric does / this shows /
   scale-free / no localization / featureless / continuum*. STOP-AND-DO: name the regime actually solved
   and the FREE choices held fixed (static / diagonal / branch G-or-P / grid / frozen rows); label the
   result SCOPED to that regime. Never state a one-corner result as the frame's verdict. [[sweep-whole-not-fragments]]
4. **Provisional until verified.** TRIGGER: before banking a verdict — committing a result doc, or writing
   *cured / conclusive / confirmed / dead / no-go / proven / it works*. STOP-AND-DO: confirm all four —
   pre-registered? full-space (or bounded slice justified)? blind-verified on the load-bearing premise?
   every forced premise audited? If any is missing, label it PROVISIONAL / a LEAD, not a result. [[session-handoff-pointer]] (verifier-before-record)
5. **Chose or derived.** TRIGGER: before any numeric value / BC / sign / chart enters a solve or a banked
   claim. STOP-AND-DO: tag each FREE / THEORY(cite) / HABIT; a HABIT is a drift flag (free or justify it);
   a result riding a FREE constant is conditioned on it — say so. SCOPE: PHYSICS premises only; conditioning/
   solver params (grid, tol, continuation step, preconditioner) are category-A (soundness, not derivation).
6. **Derive natively, not GR's form.** TRIGGER: before writing *folds away / reduces to the standard case /
   as in GR / vacuum is / the usual Einstein*. STOP-AND-DO: that step is the prime suspect for smuggling GR
   back in — show the term's fate from the positional-dilation operator NATIVELY; do not assume the
   inherited form. (GR as reference is allowed (lane #2); ADOPTING GR's answer as UDT's is the smuggle.) [[derive-natively-not-inherited-form]]

## Session workflow

- **Maximize the use of subagents to preserve main context** (Charles,
  2026-06-10): delegate reconnaissance, implementation, verification, and
  doc-drafting to agents; keep only distilled reports in the main loop.
  Present the process plan before launching long pushes.
- **Use the GPU** (Charles, 2026-06-11): a Tesla V100-PCIE-32GB is
  available via PyTorch (`torch.linalg`, float64, cuda=True; note
  nvidia-smi/NVML is broken — driver mismatch — but torch works fine;
  expect an NVML warning, ignore it). Production eigensolves, scans,
  and flow sweeps should use batched torch float64 (~14 ms per
  1024² symmetric eigensolve batched; 6x single-solve). Keep mpmath/
  sympy on CPU for high-precision anchors and symbolic identities;
  GPU results get CPU spot-checks at a few points per run.
  KNOWN PITFALL (found 2026-06-11): on this V100/cu121 stack, batched
  torch.linalg.solve_triangular with a BROADCAST Cholesky factor
  silently corrupts at large batch (~150+); use explicit inverse +
  batched matmul, and always run per-batch CPU asserts.
- **ANTI-HANG (binding operational rule, 2026-06-20 — SIX+ agents hung this
  way).** The coupled solves are SLOW (jacrev/iteration-bound, minutes to
  ~1700s). ALWAYS run solves BOUNDED: cap the grid (Nr<=16/24), cap Newton/
  Krylov iters, and run a SINGLE clean process at a time — NEVER concurrent
  (GPU contention stalls everything), and NEVER launch-a-solve-and-poll a
  background task (agents hang waiting). Fixed-background eigenproblems are
  cheap (5-22s); the dense-LM (jacrev+lstsq) is the flooring tool; recompute
  on SAVED fields where possible. If a solve would exceed budget, REDUCE and
  report "throughput-limited" — a bounded honest partial beats a hang.
  Stability/landscape tests: NEVER blend a field toward a chosen endpoint and
  call it dynamics (a biased artifact — it cost a wrong headline); use unbiased
  kicks + NEB + a 3-cell persistence test (a 2-cell test throws look-elsewhere
  false positives).

## Repo discipline (use git AS git — Charles 2026-06-24)

- **EDIT files in place; let git history be the audit trail.** Commit per
  logical change with a clear message; roll back via `git revert`/history if a
  change regresses. The point of committing is ROLLBACK capability, not freezing.
  REPEALED (Charles 2026-06-24, "patently absurd... the opposite of using a git
  repository"): the old "committed scripts are immutable / new work = new files /
  research-record markdown append-never-edit" rule. It froze improvement and
  caused SOLVER PROLIFERATION — a stale harnessed path (p1_residual) while the
  live work moved to an un-harnessed file (branchGP). When you improve a solver,
  EDIT it (and update its harness); do not spawn branchGP_v2. Append-only is fine
  for a running LAB-LOG section of a results doc, but correcting/superseding an
  earlier claim by EDITING (with the change visible in git) is now preferred over
  piling addenda. A RECONCILIATION is owed: consolidate the proliferated
  solvers/scripts to ONE canonical solver + its harness, retire the rest.
- **Verifier-before-record**: every result (positive or negative) gets a
  blind adversarial verifier pass, recorded in its results doc with agent
  id and date, before commit.
- **Pre-register before testing**: falsification contracts (frozen model,
  candidate lists, tolerances, look-elsewhere accounting) are committed
  BEFORE the test runs. No retuning after.
- Calibrate, never dramatize. Failures are recorded as failures. Negative
  results are first-class deliverables.
- Null-test discipline: exact rational matches are cheap (small-rational
  coverage ~16-23%, see dimension_ladder_null_audit.md). New value
  identities must pass the TEST-B-style classifier (generalize, solve,
  check N-specificity) before being banked as evidence.
- **Negative results are scoped, never absolute** (Charles, 2026-06-11):
  every banked negative/no-go carries its PREMISE SET (background,
  source treatment, boundary conditions, domain class, truncation,
  method). The living index is NEGATIVES_REGISTRY.md. When any premise
  is later revised or refuted, every negative carrying it is flagged
  CONDITIONS-CHANGED in the registry and loses blocking authority until
  re-graded under the new conditions. Check the registry at every push
  plan and every premise-changing result.
- **Hypothesis discipline** (Charles, 2026-06-11: "I'm trying to find
  what's real, not what confirms my priors"): Charles's physical
  pictures are direction, not evidence. Aim verifiers hardest at
  results that would confirm the standing picture; accommodations to a
  hypothesis are pre-registered, never retrofitted after a residual.
- **Interrogation discipline** (Charles, 2026-06-11; adopted after the
  oscillator-thread audit): every push DECLARES up front whether its
  question is METRIC-LED ("what does derived structure X do?") or
  TEMPLATE-LED ("can the metric perform mechanism Y?"). Template-led
  pushes are legal falsification exercises, but their negatives indict
  the TEMPLATE first, the metric second — and a run of template
  refusals triggers a REFRAME, not a deeper drill. Watch the questions
  for smuggled mechanisms (the resonator/mass-as-eigenvalue template
  ran ten months before being named). Principles 1 and 3 police
  answers and vocabulary; this rule polices the questions.
- Commit per result; push to github.com/charlesrotter/udt_mass_codex.

## Canon

Charles-canonized statements live in CANON.md (append-only). As of
2026-06-10: R-areal reading (rho = r is a theorem; branch-(iii) statics
closed), the finite-cell canon (no spatial infinity; universe and matter
cells are finite mirrored domains), and the discreteness-program
redirect (nonstationary weld sector / transfer ladder / ensembles).

## Orientation

- **`LIVE.md` IS THE FIRST READ — the only guaranteed-current file** (frontier + next action). If
  anything else disagrees with it, LIVE.md wins. Read order: **LIVE.md → a `PURSUIT_CHARTER_*.md` ONLY if a current
  one exists for LIVE's arc (the latest, `PURSUIT_CHARTER_2026-07-04.md`, is SUPERSEDED — LIVE.md names the
  current arc; skip the charter / mine it for the traps list only) → CLAUDE.md "How we work" + "DRIVER TRIGGERS" + the `.claude/skills/`
  discipline skills → HANDOFF.md TOP (detailed record; currently the post-LIVE orientation) → INDEX.md (repo map).**
- **Current state / frontier / pending decision: DO NOT TRACK IT HERE — this file goes stale (a 2026-07-04
  dress rehearsal caught exactly this bullet describing an already-superseded "stability arc" frontier).**
  The ONLY current sources are `LIVE.md` TOPMOST + `HANDOFF.md` TOP (+ a `PURSUIT_CHARTER_*.md` ONLY if a current
  one exists — the latest, 07-04, is SUPERSEDED). CLAUDE.md is the BINDING METHOD (principles 1-7, how-we-work,
  DRIVER TRIGGERS, repo discipline) — NOT the frontier. If you want to know what's done / what's next, read LIVE +
  HANDOFF TOP (the charter only if a current one exists), never this bullet. pytest 67/1xfail (2026-07-07; grows as tests land — a HIGHER pass count with 0 failures is fine; just run `python3 -m pytest tests/` and trust the live count).
- **SUBSUMED / HISTORICAL trackers (do NOT treat as the live frontier — moved to `archive/` or tagged):**
  COMPLETION_PROGRAM.md, SOLVER_COMPLETENESS_MAP.md, POST_POSTULATE_PROGRAM.md, MIGRATION.md, REORG_PLAN.md,
  and the FOUNDATIONAL_ASSUMPTIONS_LEDGER.md F0-F8 scoreboard — all superseded by the static-solver
  completion above. STATE.md = a long running LAB-LOG (mine for history; its TOP frontier may be stale —
  LIVE.md is the frontier). The DERIVED-operator arc docs (native_dilation_weight_derivation,
  matter_regrade_derived_operator, F2_matter_action_forcedness, seal_junction_condition, the F-closure
  docs) remain the FOUNDATION record — BUT mine only the SURVIVING sections: per the 2026-07-06 macro-spine
  pass, `native_dilation_weight_derivation` §5-7 is SPLIT/SUPERSEDED (the X=−2e5 scalar-tensor birthplace),
  and `matter_regrade_derived_operator` + F1F3_closure + F5_critical_universe_closure are SUPERSEDED/CC (see
  their in-file banners + `macro_spine_provenance_2026-07-06.md` / `pre_native_era_census.md`).
- **Durable records (current):** CANON.md (Charles-canonized, append-only); NEGATIVES_REGISTRY.md
  (scoped negatives w/ premise sets — check every push). Main research record: negative_phi_native_geometry.md
  (pre-spectrum) + particle_spectrum_native_geometry.md (spectrum stage). Audit/prosecution record:
  mass_emergence_canonical_geometry.md (binding Self-Hardening Protocol — re-read before editing it).
- Legacy (superseded, mine for structure only): udt_canonical_geometry.md via legacy_hadron_survivor_filter.md.
