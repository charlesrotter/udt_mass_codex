# MAP — The Everything-On Solver Build

**Mode:** MAP (no compute, no solve, no derive). **Status:** for Charles's steer; the build is
GATED on his go. **NOT canon.** **Driver:** claude-opus-4-8[1m]. **Date:** 2026-06-19 (LATE).
Frame stated whole + premise ledger, so a smuggled physics-choice gets caught at the cheap stage.
Governing docs: POST_POSTULATE_PROGRAM.md (the program), SOLVER_COMPLETENESS_MAP.md (the instrument).

---

## 0. WHAT THIS BUILD IS — and what it is NOT

It IS **infrastructure**: one clean UDT-native solver for the whole metric with nothing silently
dropped, so that we can finally **observe what the metric does**. It is the precondition for the
program, not the program's result.

It is NOT physics yet, and NOT a catalog hunt. The physics comes from RUNNING it and OBSERVING.
We do not aim it at three generations or any target. We build it to SEE. (Observing, not
targeting — binding.)

The honest danger to name up front: building a big machine can become its own action-bias — a way
to feel productive while deferring the moment of looking, or a machine so large it is never
"done" enough to trust. Two guards, baked into the plan below: (a) build **incrementally** and
**OBSERVE at every completeness level** (each newly-turned-on degree of freedom is itself a small
"what does the metric do here?" observation), and (b) the **completeness bar** (§V) defines, in
advance, when a result is allowed to mean something.

---

## I. THE TARGET (the everything-on standard, from the program doc)

One solver carrying, with nothing silently frozen:
- all 10 metric DOF live — off-diagonals **wired to the field equations**, A and B independent
  (B=1/A free, not injected), the **time row live**;
- UDT-native matter: the **S² area-form (π₂) carrier, Θ FREE** (native regularity-node core
  condition, **no Skyrme BC**), native L2+L4, in full 3-D;
- the matter coupling **a(φ) able to be a FUNCTION** (the e^{(a+1)φ} weight wired in), with a=−1
  (GR) as the validated baseline;
- finite mirrored cell + native seal (reflecting, time-live); honest deep core;
- the postulates as STRUCTURE: i = the S² area form and spin-½ = its Maslov index are already
  structural facts of the carrier; **ħ-quantization is a post-step applied to the continuous
  solution family** the classical solver produces.

So the build is two layers: **(big) the classical everything-on solver → a continuous family**;
**(small) a quantization layer applied to that family.** Observe at both.

## II. THE FOUNDATION (solver-source recon, 2026-06-19 — what we build ON)

Clean, reusable: `whole_metric_3d_core.py` (general 4×4 Einstein, off-diagonal + time slot
present, validated 2.7e-15) · `whole_metric_3d_matter.py` (general L2+L4 stress, exact) ·
`coupled_tl_stage1a.py` (the ONLY native Θ-free node-core EL, 1-D radial) · the spectral bases +
divT gate + M_MS readouts · `full3d_newton.py` (clean dense-Newton, proven ~1e-13 small grid =
the **correctness ANCHOR**). B=1/A is genuinely free (the #55 scar is absent).

The three things contaminated/missing EVERYWHERE (the build's real work): **a(φ) silently frozen
to −1**; **off-diagonals built-but-dead** (production residual calls the diagonal Einstein); **the
Θ-free node EL is only 1-D radial**. Plus the off-round driver does not scale (#60).

## III. THE BUILD, IN PHASES (incremental; each validated against the anchor; OBSERVE at each level)

Each phase turns on ONE thing, validates it against a known answer (the dense-Newton anchor or an
analytic limit), runs the box-control / convergence gates, and OBSERVES what the new DOF does
before the next phase. A phase that cannot converge is reported INCONCLUSIVE (solver-limited),
never a null.

- **P0 — Baseline anchor (cheap).** Reproduce the clean round static native soliton (M_MS≈0.281)
  on the chosen kernel+driver+bases as the validated zero point. (Mostly done this session.)
- **P1 — Wire the residual to the GENERAL Einstein** (the #1 rewire). Off-diagonals reach the
  field equations. Validate: round case unchanged; off-diagonal G verified vs sympy. OBSERVE:
  does anything off-diagonal want to be non-zero once it's allowed to feed back?
- **P2 — 3-D native Θ-free matter** (generalize the node EL from radial to (r,θ,ψ)), no Skyrme
  BC. Validate: round limit recovers P0; divT gate. OBSERVE: the non-round matter shape.
- **P3 — a(φ) capability.** Wire the e^{(a+1)φ} weight into the action/stress, a(φ) a declared
  function; a=−1 reproduces P2 exactly (validation). OBSERVE (separately, never conflated): what
  a(φ)≠−1 does. (See premise ledger L-a — this is the one genuine physics CHOICE in the build.)
- **P4 — Time live.** Turn on the kernel's time row (open-time harmonic balance / evolution).
  Validate: ω→0 returns the static solution. OBSERVE: the time-live structure.
- **P5 — The research-grade driver.** Replace/augment the dense-Newton with a preconditioned /
  Newton-Krylov (or sparse-direct) solver that drives the joint off-round + time-live + coupled
  system to a clean floor, validated against the dense-Newton anchor on every case both can run.
  This is the load-bearing hard part (the #60 wall).
- **P6 — Seal + honest deep core.** Native reflecting seal; log/geometric or analytic core
  (retire the 0.05 cutoff). Validate: cell-size independence (box-control gate).
- **P7 — The quantization layer.** Apply ħ-quantization (Bohr-Sommerfeld / mode quantization) to
  the continuous family P0–P6 produce. OBSERVE what is picked.

Phases P1–P3 are mostly wiring on clean primitives (the recon says the pieces exist). P5 is the
genuine research build. The order can flex, but each step is anchor-validated before the next.

## IV. PREMISE LEDGER — every build choice that could smuggle physics into an "engineering" decision

| # | Choice | Default | CHOSE / DERIVED | Risk / guard |
|---|---|---|---|---|
| L-a | **a(φ): the matter mass-dilation exponent** | a=−1 (GR) baseline; a(φ)=−1+k·eps0^p·e^{−pφ} available | **the FORM is DERIVED (symbolic, field-eqn arc); but k≠0 (whether matter departs from GR) is UNFORCED at the principle level = a CHOSE** | The one genuine physics choice. NEVER silently pick: run a=−1 as the validated baseline AND a(φ)≠−1 as a separate declared exploration; never present either as "the UDT answer." k,p,eps0 are declared parameters, not fitted. |
| L-box | Cell size / grid | cell a SCAN variable | DERIVED-as-gate | Box-control is physics masquerading as a numeric choice (the standing scar). Never fix the cell; verify R-independence (Gate A) for any "intrinsic" claim. |
| L-core | Deep core | log/geometric or analytic core | should be DERIVED (φ→−∞ canon) | The 0.05 cutoff is a CHOSE that smuggles the core endpoint (#61 scar). Retire it (P6); until then, core results are scoped. |
| L-seal | Outer boundary | native seal = mirror fold = time reversal | DERIVED (native) but watch | Do not let an imposed BC pre-select structure; the seal value is a continuous number, not a quantizer. |
| L-BC3D | 3-D Θ-free core BC | native regularity node, value free | DERIVED (node) — DANGER | Generalizing to 3-D must NOT re-import Θ(core)=m·π (#61). Grep-verify; the node is the only core condition. |
| L-trunc | Truncations (time harmonics, spectral order, mode count) | enough to converge | category-A (tractability) | A truncation can hide structure (single-time-harmonic missed nothing in #65 but might elsewhere). Convergence-test the truncation order; report what was dropped. |
| L-drive | Research-grade driver | preconditioned/Newton-Krylov, anchor-validated | category-A | A new solver can "converge" to a WRONG answer. Validate against the dense-Newton anchor on every shared case; gauge-invariant cross-checks. |
| L-quant | The quantization rule | Bohr-Sommerfeld / standard mode quantization | CHOSE (the postulate) | This IS postulate A — declared, minimal {ħ, spin-½, statistics}, i=area-form native. Smuggle no SM (no Dirac/gauge). |
| L-carrier | Carrier | S² area-form (π₂) | DERIVED (canon C-14-1) | Settled; do not drift to S³/Skyrme. |

The two that most need YOUR eye, Charles: **L-a** (the only real physics choice — is a=−1 the
right baseline, and is parameterized a(φ)≠−1 the right way to explore the unforced departure?) and
**L-quant** (the quantization rule — exactly which minimal postulate, applied how).

## V. THE COMPLETENESS BAR — when a mismatch is allowed to mean something

This operationalizes the solver-first discipline. A result that is far from observation may indict
the **metric** ONLY when ALL hold:
1. Every DOF/term/coupling relevant to the question is ON (per the completeness map) — none frozen
   or forgotten.
2. The result is **numerically clean**: converged to floor, grid-stable across ≥2 refinements,
   box-control verified (R-independent), validated against the anchor.
3. The **solution space was explored with everything on** — multiple seeds/branches, continuation,
   not a single corner.
4. Examined **multiple ways** (different bases/grids/seeds, gauge tests, independent re-derivation)
   and they agree.
Until all four hold, a mismatch indicts the **solver's completeness**, not the metric — and a
mechanism is never the move. The completeness map is the checklist that says which of these is even
answerable yet.

## VI. RISKS (ranked)

1. **P5, the research-grade driver (the #60 wall).** The genuine hard part. The off-round +
   time-live coupled system may resist a clean floor; if so the program is solver-limited, not
   metric-limited — and we say INCONCLUSIVE, not null. This is the single biggest schedule/▸
   feasibility risk. The dense-Newton anchor de-risks correctness but not scale.
2. **L-a being made to look forced.** The temptation to pick a k that "works." Guard: declared
   parameter, baseline a=−1, separate reporting.
3. **Over-engineering / deferral.** Building forever, never observing. Guard: observe at every
   phase; the completeness bar is a gate to USE results, not an excuse to withhold them.
4. **A new-driver bug producing a confident wrong answer.** Guard: anchor-validate every shared case.
5. **Re-importing a BC in the 3-D generalization** (L-BC3D). Guard: grep + node-only core.

## VII. SMUGGLED-FRAME CHECK

Is "everything-on solver" itself a smuggled frame? Mostly no — it is the direct expression of
Principle 1 (uncover what the metric does) + the solver-first discipline: you cannot honestly say
"the metric does X" until the metric is actually solved with everything on. The recon shows the
pieces are real and mostly clean; this is assembly + one hard driver, not invention.

The honest caveats: (a) it is INFRASTRUCTURE — it does not by itself answer any physics question;
the answer is downstream, in the running and observing. (b) It does NOT resolve the deepest open
Principle-7 item (UDT's native curvature-sector action is still unbuilt; this solver works within
the GR-form field equation with the matter weight — "vacuum = GR by construction" persists). (c)
The quantization layer (P7) is a postulate applied, not a derivation — the discreteness it
produces is quantization's, on the metric's continuum. None of these is a reason not to build; all
three must stay visible so we don't over-claim what the built solver shows.

## VIII. WHAT IT TAKES (scoping, honest)

- P0–P4: assembly/wiring on existing clean primitives — the recon's "fixable" items. Days-to-weeks
  each, anchor-validated. Tractable on the V100 dense-Newton at small/moderate grids.
- P5: the research-grade solver — the multi-week, genuinely-hard build (preconditioned
  Newton-Krylov / sparse-direct exploiting the spectral structure). The gate on everything off-round.
- P6: moderate (core/seal numerics).
- P7: a smaller, well-defined layer once the continuous family exists.
Build order is incremental so value (observations at each completeness level) lands before P5 is
finished. The completeness map tracks coverage the whole way.
