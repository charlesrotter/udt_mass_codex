# Throughput / Coverage — the two routes when compute becomes the ceiling

*An assessment, not canon. Applies once the solution space begins to take shape under the guardrails
and the practical ceiling stops being "is the solver trustworthy" and becomes "can we actually cover
enough of the space — especially the unplayed time-live and ensemble regimes — within realistic
compute." Two routes were proposed: (1) established numeric techniques that make the calculations
tractable; (2) with the shape firming up, look for algebraic solutions. The core finding: they are not
an either/or — they are a pipeline.*

---

## Framing: a pipeline, not a fork

The two routes are not alternatives at the same moment.

- **Route 1 is first and mandatory** — solver-first discipline already requires exhausting numeric
  technique before anything else, and Route 1 is also what *generates the shape* Route 2 needs.
- **Route 2 is the gated endgame** — it only becomes available once numeric exploration has revealed
  enough structure to spot the right ansatz / symmetry / conserved quantity.

So the real decision is not "1 or 2." It is: aim Route 1 at the techniques that *reveal structure*
(not just raw speed), let the revealed structure show *where* algebraic closure is plausible, and
pursue Route 2 there. The workhorse finds out whether the high-payoff move is even available.

---

## Route 1 — established numeric techniques

**The trap:** reading "make calculations tractable" as "speed up one solve." That raises the ceiling
by a constant factor. The ceiling that actually matters here is **coverage** — mapping a branched,
multi-regime space — and there is a specific family of established techniques built for exactly that,
not for raw speed:

- **Deflation / deflated continuation** (Farrell-style): systematically finds *distinct* solutions of
  the same nonlinear system — almost purpose-built for the particle-catalog frame ("what are all the
  stable solutions," not "solve this one faster").
- **Pseudo-arclength / arc-length continuation** (Keller) and **bifurcation tracking**: walk the
  solution branches *through* folds and bifurcations — how you map a structured space instead of
  sampling it blindly.
- **Reduced-basis / model-order reduction**: solve a few full solves, then explore the rest of a
  family at near-zero cost — attacks coverage directly.

**Pros.** Stays squarely in the allowed lane (technique, not mechanism — category-A); low conceptual
risk (same equations, solved more cleverly); and the structure-mappers attack *coverage itself*, not
just per-solve cost.

**Cons / limits.** Improvement of *degree*, not *kind* — if a regime is genuinely high-dimensional
(ensembles), faster points still may not cover it. Each technique needs its own soundness/convergence
check (category-A is verified, not assumed); we have already been burned by conditioning artifacts
(Ruiz-equilibration confusion, the risk of spurious deflated roots), so the verification overhead is
real and non-optional.

---

## Route 2 — algebraic solutions once the shape firms up

When it works, it is a change of *kind*: an exact family solution costs nothing to evaluate anywhere,
removes the compute ceiling for the region it covers, and *is* the structure rather than a sampling of
it. It is also the project's native register — the founding "digits are search keys into algebraic
space," and the cleanest standing wins (q=1/3, N=3, η=1/18, 1+z=e^φ) are all algebraic.

**Three honest caveats.**

- **Gated / downstream.** It needs the shape to firm up before the right ansatz / symmetry / conserved
  quantity is visible. You cannot start here.
- **Not guaranteed to exist.** A nonlinear coupled φ-angular time-live system may simply not be
  integrable. You cannot will a closed form into being; if the physics is not algebraically tractable,
  Route 2 returns nothing.
- **It is where the most dangerous import lives.** Reaching for a textbook structure — a known
  soliton, an integrable-system ansatz, a WZW/Chern-Simons term — that "fits" and calling it native is
  the same sin as a smuggled boundary condition, and it feels *cleaner*, which makes it more dangerous.
  Plus the numerology trap: an algebraic form that matches sampled points but is a coincidental fit.
  Route 2 therefore demands the **fullest** provenance discipline (the allowed lane's category-B gate;
  the TEST-B-style N-specificity null test). Its saving grace is that its verification standard is
  *exact* — substitute the candidate back into the native equations — which is a genuine strength.

---

## The regime-specific point (where Route 2 bites hardest)

The two regimes named as the ceiling have *different tractability characters*, and Route 2 is most
relevant exactly there:

- **Time-live** is a time-dependent PDE. The classic algebraic move is a **symmetry reduction** — a
  self-similar or traveling-wave ansatz that collapses the PDE to an ODE. That is a Route-2 reduction
  that *makes the time-live solve tractable in the first place.* For time-live, Route 2 is not just an
  endgame; it may be the thing that opens the regime.
- **Ensembles** are a dimensionality explosion (many cells, multi-body). Brute-force numeric coverage
  of that space does not scale — no preconditioner saves you from the curse of dimensionality. Here a
  **reduced / effective description** — an effective algebraic law for cell-cell coupling — may be not
  merely higher-leverage but *necessary*. Pure Route-1 numerics likely cannot cover the ensemble
  space; this is where a structural collapse is most needed.

---

## Bottom line

It is not "1 or 2." Run **Route 1 now**, but aim it at the **structure-mapping** techniques (deflation,
arc-length continuation, reduced-basis), because those simultaneously push the ceiling, map the
coverage, *and* hand Route 2 the firmed-up shape it requires. Then let the revealed structure tell you
**where** algebraic closure is plausible — and pursue **Route 2** there, under full provenance
discipline, expecting it to bite hardest on time-live (symmetry reduction) and ensembles (effective
description).

The one caution: do not bet the whole ceiling problem on Route 2 *existing*. It is the high-payoff move
you cannot force; Route 1 is the reliable workhorse you can. Use the workhorse to find out whether the
high-payoff move is even available.

---

*Both routes live inside the "allowed lane": numerical/mathematical technique and structural/algebraic
reduction are category-A (how we solve) and category-B-done-natively (structure derived, not imported)
respectively — neither is the forbidden import of a physics mechanism. The guardrails keep the search
honest; these routes keep it tractable.*
