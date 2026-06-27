> **[ARCHIVED 2026-06-27 — SUBSUMED by the static-solver completion; the live frontier is LIVE.md (detail: HANDOFF.md TOP). Kept for history.]**

# THE PROGRAM — UDT after the postulates (corrected forward plan)

**Status:** DRAFT for Charles's sign-off. **Supersedes** VISION_POST_POSTULATE.md.
**NOT canon** (Charles canonizes). **Driver:** claude-opus-4-8[1m]. **Date:** 2026-06-19 (LATE).
Written in the binding MAP/PONDER spirit and in lay language; the exact math lives in the
solver, the completeness map, and the records.

This doc replaces the VISION because the VISION encoded a misreading of the project's own
history. It is the output of a deep PONDER with Charles (2026-06-19) and it states the program
the way the corrected stance requires.

---

## I. THE CORRECTION — what the VISION got wrong

The VISION (and the recon that built it) **compiled** the pile of results and read it as a *map
of the metric*. It is not. It is a record of what an evolving succession of **imperfect tools**
could and couldn't find. Every solver in the project's life was contaminated or sliced
*somewhere* — it had to be, because the whole metric is intractable: GR-coupled matter (a=−1),
an imported Skyrme boundary condition, B=1/A injected in the reduced solver, box-control,
off-round non-convergence, and the static / round / single-cell / diagonal slices. The negatives
those tools produced are **facts about the tools, scoped to each tool's flaw.**

Stacking scoped negatives from different flawed tools does **not** build a verdict about the
metric. It builds a detailed portrait of the tools. The VISION mistook that portrait for the
territory and called one half "walled." That is the project's own named failure mode —
narrating false convergence — operating at the scale of the **whole history** instead of inside
a single push, which is the one place the discipline never looked.

And underneath: **the whole clean metric has never once been solved.** Every result is about
*the-metric-minus-something*. The entire negative library is the natural history of our own
approximations.

## II. THE TWO PREMISE CHANGES — and the inversion they force

Two of the deepest premises changed at almost the same instant, and the VISION was written as
if neither had:

1. **The postulates were admitted** ([[postulate-A-accepted]]): UDT = quantized
   dilation-geometry. Quantization is, by definition, what turns a continuum into a discrete
   set. By the registry's own discipline this is the largest possible premise change — it
   should flag every "classical" negative as CONDITIONS-CHANGED and strip its blocking
   authority.
2. **The solver only just got clean.** The first genuinely native, Θ-free, no-Skyrme matter
   sector appeared *this* session.

**The inversion:** under the postulates, "no classical discreteness" is the **expected
pre-quantization continuum** — not a wall. A classical field theory *should* give a continuum;
a thing-that-needs-quantizing *must*. So the microphysics negatives flip from walls to
expected-continuum (and some are simply WRONG — buggy solvers — but it does not matter which:
all retired). **The microphysics half is UNENTERED, not walled.**

Consequently the **entire pre-postulate microphysics discreteness / spectrum / catalog /
multiplicity negative corpus is RETIRED — legacy, no blocking authority** (NEGATIVES_REGISTRY
wholesale-retirement banner, 2026-06-19). We do **not** sort it (wrong vs correctly-erroneous is
moot). The **one salvage** is the **tooling** — the later, cleaner solves as source code to
build the clean solver on.

## III. THE GOAL, RESTATED (Principle 1, post-postulate)

The primary goal is to **uncover what the metric does** — now with the postulates incorporated
as **structure**, not chased as a target:
- **i = the S² area form** (native), **spin-½ = the area-form Maslov index**, **ħ-quantization
  acts on the continuous solution family**, statistics. No Dirac / gauge / SM-mass import.

The catalog hunt — "distinct sectors / depth-selector / what label indexes the objects" — was a
**mechanism hunt**: it works backward from the observed three generations to machinery that
produces them, importing the target. That is exactly what Principle 1 forbids. The catalog is an
**observation to be matched**, never a structure to be **engineered**.

So the program is, in order:

> **Solve the WHOLE CLEAN metric with EVERYTHING TURNED ON, plus the postulates as structure →
> OBSERVE the continuous solution structure → QUANTIZE → OBSERVE what gets picked.**

We map the continuum *before* asking whether it is discrete, because we never have — every solve
jumped to "is it discrete yet?" on a slice. Discreteness is downstream of understanding the
continuum the clean metric actually produces.

## IV. THE BINDING DISCIPLINE — solver-first on any mismatch (Charles, 2026-06-19)

**If a result is far from observation, the FIRST hunt is the SOLVER and our application of it —
NEVER a mechanism.** In order:

1. What did we leave **OUT** of the solver? (a term, a coupling, a sector, a boundary)
2. Is it a **numeric** problem? (convergence, box-control, conditioning, a bug, grid)
3. Did we **freeze or forget to turn on** a degree of freedom?
4. Have we actually **explored the solution space with everything on**, or only a corner?

Plus: the many *ways to examine* the same solve (different bases, grids, seeds, continuation,
gauge tests, independent re-derivation). **Reaching for a mechanism to close a gap is
FORBIDDEN** until the solver is demonstrably complete and the solution space genuinely explored.
A mismatch indicts the solver's **completeness** first, the metric last, and a mechanism never
(that is the import reflex). This is Principle 1 applied to our own numerics.

The instrument that makes this operable is **SOLVER_COMPLETENESS_MAP.md** — it shows, before we
trust any result, which DOF/term/coupling is on / off / frozen / never-built, so we *know* which
of the four questions is even answerable yet.

## V. THE EVERYTHING-ON SOLVER — the object to build

A single clean UDT-native solver for the whole metric with nothing silently dropped:
- all 10 metric DOF live — off-diagonals **wired to the field equations** (today they are built
  but dead: the production residual calls the diagonal Einstein), A and B independent (B=1/A free,
  not injected), the **time row live**;
- UDT-native matter: the **S² area-form (π₂) carrier, Θ FREE** (native regularity-node core
  condition, **no Skyrme BC**), native L2+L4 — generalized from the current 1-D radial node EL to
  full 3-D;
- the matter coupling **a(φ) as a FUNCTION**, not silently frozen to a=−1 — the e^{(a+1)φ} weight
  wired into the action/stress (it lives only in symbolic side-scripts today);
- finite mirrored cell + native seal (reflecting, time-live); honest deep core (φ→−∞, not a 0.05
  cutoff);
- the postulates incorporated as structure, applied to the continuous family.

**Foundation to build on (solver-source recon, 2026-06-19):** `whole_metric_3d_core.py` (general
4×4 Einstein, off-diagonal + time slot present, validated) + `whole_metric_3d_matter.py` (general
L2+L4 stress) + `coupled_tl_stage1a.py` (the only native Θ-free node-core EL) + `full3d_newton.py`
(clean dense-Newton, the **correctness anchor**). The three rewires/builds: wire the residual to
the general Einstein; wire a(φ); make the Θ-free node EL 3-D. The off-round coupled solve needs a
**research-grade preconditioned / Newton-Krylov upgrade** (the #60 conditioning wall) — validated
against the dense-Newton anchor. Full status table in SOLVER_COMPLETENESS_MAP.md.

## VI. WHAT STANDS, AND WHAT IS GENUINELY OPEN

**Stands (premise-independent, not retired):**
- The metric form **derived from relativity** (CANON C-2026-06-18-1); B=1/A; ρ=r; the finite-cell
  canon. These are positive derivations, not negatives.
- The **native charge counting** — N=3 (forced unique), q=1/3, η=1/18 from the area form. The
  program's one genuine native discreteness — a *positive*.
- **mass = dilation cost** is exponential / scale-free / box-free in FORM (a durable read-off).
- The **postulate-A wins**: the box-trap broken (first intrinsic discrete level), spin native, i
  native, the time-live operator is a genuine carrier (Charles's φ-angular hunch has a real home).
- The bare-vacuum **structural theorems** (#62/#63/#64): vacuum is barren ⇒ **matter must be
  present**. This motivates the everything-on solve; it does not block it.
- The **cosmology half** (VISION §I) is a separate matter and unaffected — the metric-pure
  distance + redshift + light-element layer that beats ΛCDM at zero params remains the strong,
  durable side, with its own honestly-contested CMB-amplitude frontier.

**Genuinely open / unbuilt:**
- The **everything-on solver itself** (the three rewires + the research-grade off-round driver).
- The **a(φ) coupling in-solver** (whether UDT departs from GR in matter is unforced at the
  principle level; it needs the matter object solved with a(φ) live).
- **UDT's native curvature-sector action** — the deepest open Principle-7 item. "Vacuum = GR" is
  currently true by construction (choice of the standard Einstein tensor), not derived.
- The **scale bridge** (cosmic ln(1+z_CMB) anchor + the particle m_e anchor; the ~40-order
  autonomy gap).

## VII. THE KEPT DISCIPLINE (the engine that caught all of this)

Verifier-before-record (blind, adversarial); provenance / infrastructure audit (audit the TOOLS,
not just results); data-blind derivation under frozen pre-registered contracts; the premise
ledger + NEGATIVES_REGISTRY + the tripwires (whole-before-slice, chose-or-derived,
observing-or-targeting, count-the-refusal-run); the self-hardening ratchet; maximize subagents,
keep the perspective with Charles. **Added this session:** the **solver-first discipline** (§IV)
and the **solver completeness map as the central instrument**.

## VIII. ONE-PARAGRAPH PROGRAM

UDT is one relativistically-derived dilation metric. Its cosmology half is genuinely strong and
metric-pure. Its microphysics half is **unentered, not walled** — the entire pre-postulate
negative corpus was a portrait of contaminated, classical tools, not of the metric, and is
retired. We have never solved the whole clean metric. So we build one clean everything-on solver
(all DOF live, native Θ-free matter, a(φ) a function, postulates as structure), solve it to
**observe what the metric does**, then quantize and observe what is picked — and if it is far
from observation, we interrogate the **solver** (left-out terms, numerics, frozen DOF, unexplored
solution space, and the many ways to examine it), **never** a mechanism. The completeness map
gates trust; the catching-surface discipline keeps it honest. The goal is unchanged from the
charter's Principle 1: uncover what the metric does — now with the postulates in hand.
