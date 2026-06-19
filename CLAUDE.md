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
place to drill."

DIVISION OF LABOR (honest): the driver genuinely cannot always see its own
smuggled assumptions — Charles holding the frame is irreplaceable, the
verifier catches errors/assembly. The method does not remove this; it moves
the catching-surface EARLIER by front-loading the frame-map + premise
ledger so Charles steers at the assumption stage, not after the build.

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

## Repo discipline (the Self-Hardening culture — do not soften)

- Research-record markdown docs are append-never-edit; committed audit
  scripts are immutable. New work = new files.
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

- **VISION_POST_POSTULATE.md is the live FORWARD PLAN** (2026-06-19): the compiled
  repo-wide recon + the post-postulate-A vision (UDT = quantized dilation-geometry;
  the catalog hypothesis; the ordered path; the risks). Read it after "How we work".
- Load STATE.md first (frontier snapshot), then INDEX.md (repo map).
- Main research record: negative_phi_native_geometry.md (31k lines,
  pre-spectrum) and particle_spectrum_native_geometry.md (spectrum stage).
- Audit/prosecution record: mass_emergence_canonical_geometry.md
  (binding Self-Hardening Protocol — re-read before editing anything).
- Legacy (superseded, mine for structure only): udt_canonical_geometry.md
  via legacy_hadron_survivor_filter.md.
