# MAP — P5e: the fully-coupled time-live solve (built PROPERLY, no shortcuts)

**Mode:** MAP (no compute). **Status:** for Charles's steer; the build is GATED on his go.
**NOT canon.** **Driver:** claude-opus-4-8[1m]. **Date:** 2026-06-20.
Charles's directive: build the infrastructure PROPERLY; do P5e; no shortcuts for exciting results.
This is the hardest, most-unscoped build in the program (the #60-class throughput wall), and it forces
the two pieces we deferred. Parent: EVERYTHING_ON_SOLVER_BUILD_MAP.md, EVERYTHING_ON_SOLVER_P5_MAP.md
(the survey: #1 JFNK, #2 KEH). Governing: POST_POSTULATE_PROGRAM.md, [[solver-first-not-mechanism]].

---

## 0. WHAT P5e IS — and why it's the proper completion

P5e = the **fully-coupled off-round + time-live solve**: the metric (diagonal warps a,b,c,d AND the
off-diagonals INCLUDING the time row g_tr/g_tψ), the native matter (Θ AND its live time-dependence
d_t Θ), and the frequency ω — ALL solved together, self-consistently, at FINITE amplitude. Not a
frozen background; not a small-vibration linearization; not a single deferred ingredient. This is the
genuine version of what every prior step did a piece of.

What it completes (the deferred gaps, now closed PROPERLY):
- P1's Einstein was the small-shear pole-stable HYBRID -> P5e needs validity at FINITE shear/ω.
- P4's time was single-mode harmonic balance with containment (amplitudes pinned to 0 at ω=0) ->
  P5e turns the amplitude ON and lets the back-reaction act.
- P5a'/b's solver was proven STATIC -> P5e needs the coupled time-live free-ω solve.
- The off-round classical-discreteness gate was FIXED-BACKGROUND + structural -> P5e is the COUPLED
  (full back-reaction) version = the airtight answer.

What it delivers: (1) the AIRTIGHT discreteness verdict off-round (coupled, not fixed-bg — closes the
"#65 + structural say coupling softens, but not theorem-grade" ceiling); (2) genuinely NONLINEAR
time-dependent bound objects (breathers/geons) if any exist — the one place a classical surprise could
still hide; (3) the COMPLETE classical foundation a proper quantization (Step B/C) must sit on. (Adjacent
capability, separable: rotation/g_tψ spinning objects — note as P5f, not core P5e.)

HONEST EXPECTATION (anti-false-convergence, stated up front): #65 (reduced) + the off-round gate
(fixed-bg + structural) both indicate the off-round channel SOFTENS / BOX-CONTROLS under coupling. So
the LIKELY P5e outcome is to CONFIRM that with full back-reaction (the airtight box-control / no-tower
verdict). The genuine open is whether a finite-amplitude NONLINEAR bound object appears that linear
analysis structurally cannot see. Either is a real, first-class result. We are NOT building this to
get discreteness; we are building it to COMPLETE the solver and learn what the coupled metric does.

---

## 1. THE TWO DEFERRED PIECES — the real open choices (the heart of this MAP)

### CHOICE A — the Einstein kernel: hybrid+continuation vs the TRUE general Einstein
The pole-stable hybrid (G_weyl + [general(full) - general(diag)]) is accurate only at SMALL shear/ω
(P1/P4 verifiers: err ~0.5*A). Finite-amplitude coupled WILL test that. Two proper routes:
- **A1 — continuation in amplitude, staying inside hybrid validity.** Ramp A from 0; at each small
  step the hybrid is valid; re-solve coupled; march up. CHEAPER (reuses the hybrid). Risk: if a bound
  object/instability lives at LARGE A beyond hybrid validity, continuation can't reach it cleanly;
  must monitor max|A| vs the hybrid error bound and STOP/flag when exceeded.
- **A2 — build the TRUE general Einstein** (well-conditioned on the steep core, for the FULL
  off-diagonal+time metric). This is the genuine "no shortcut" kernel. It's a real build: the steep-core
  conditioning (b=p*ln(r/r_seal)) is WHY the hybrid was made; doing it properly = extend the analytic
  pole-stable cancellation (the cot/(1/sin) cancellations) from the diagonal Weyl block to ALL
  off-diagonal + time components (a gen_einstein_3d codegen). Medium-to-large effort; removes the
  small-shear ceiling permanently.
- **Recommendation:** start A1 (continuation) to map the small/moderate-A regime cheaply + instrument
  max|A| vs hybrid validity; build A2 ONLY when continuation demonstrably outruns the hybrid (don't
  build the expensive kernel until the physics demands it — that's the solver-first ordering, not a
  shortcut). Charles decides if "properly" means A2 up front regardless.

### CHOICE B — the coupled solver + the ω treatment
- Solver: the re-posed full-rank JFNK (P5a', static-proven) extended to the time-live residual +
  free-ω closure; pair with PSEUDO-ARCLENGTH CONTINUATION for the ω/amplitude branch (the principled
  replacement for the warm-start that failed). GR-corpus fallback (#2 KEH/SCF) if JFNK stalls on the
  coupled system (Principle 4: mine the corpus before reinventing).
- ω treatment: P4 used SINGLE-MODE harmonic balance. At finite amplitude the breather is ANHARMONIC ->
  proper P5e likely needs MULTI-HARMONIC balance (a few time-Fourier modes) or genuine time EVOLUTION.
  Single-mode is the shortcut to avoid; multi-harmonic is the proper minimum. (Evolution = the heaviest;
  reserve as a cross-check / persistence test.)
- Free-ω = the object picks its OWN frequency self-consistently (an eigenvalue of the coupled system),
  not a scanned external ω.

---

## 2. PREMISE LEDGER

| # | choice | proper default | CHOSE / DERIVED | risk / guard |
|---|---|---|---|---|
| Pe-kernel | Einstein kernel | A1 continuation-in-hybrid first; A2 true-Einstein when A outruns validity | CHOSE | instrument max|A| vs hybrid err bound EVERY step; STOP+flag (or switch to A2) when exceeded — never silently run the hybrid out of regime |
| Pe-amp | amplitude | FINITE, continued from 0 (the back-reaction is the whole point) | DERIVED-necessary | this is what P5e ADDS over fixed-bg/linear; a "result" at A->0 is just the prior linear answer |
| Pe-time | time treatment | MULTI-harmonic balance (single-mode is the shortcut); evolution as cross-check | CHOSE | report harmonic-truncation convergence; a strongly anharmonic regime needs more modes — don't trust single-mode at large A |
| Pe-solver | coupled solver | re-posed JFNK + pseudo-arclength continuation; KEH/SCF fallback | CHOSE | the #60 wall; anchor-validate (below); a new solver converging to a WRONG fixed point is the #1 risk |
| Pe-repose | full-rank body DOF | re-pose (P5a') carries over | DERIVED (P5a') | the committed Jacobian is rank-deficient without it; keep it |
| Pe-a | a(φ) coupling | a=-1 baseline (P3); a(φ)!=-1 a SEPARATE declared run | CHOSE-baseline | never present a=-1 as "the UDT answer"; a!=-1 unforced |
| Pe-omega | ω | free / self-consistent eigenvalue | DERIVED-necessary | containment: ω->0 returns the static round ground state (sanity) |
| Pe-box | box-control gate | any ω/level claimed intrinsic passes the 3-criteria gate | DERIVED-gate | THE standing trap; cell-scan + wall-relocation + intrinsic-lock (not l(l+1)W_inf, not j_l-zero) on EVERY claimed level |
| Pe-conv | #60 convergence gate | a known-relax control converges to floor on the same machinery | DERIVED-gate | if the control stalls, the off-round coupled solve is SOLVER-LIMITED -> INCONCLUSIVE, not a null |
| Pe-anchor | correctness reference | dense-LM static (ω->0) + the fixed-bg eigenspectrum (small-A) | DERIVED | the coupled solve must reproduce BOTH limits before its finite-A results are trusted |
| Pe-observe | observe vs target | report what the coupled solve contains | binding | NO tower/catalog hunt (#44/#65 settled the classical one carrier); observe-not-target; DATA-BLIND |

The two for YOUR eye: **Pe-kernel** (A1 continuation-first vs A2 true-Einstein up front — is "properly"
the staged route, or the full kernel regardless?) and **Pe-time** (multi-harmonic is the proper minimum;
confirm we're not accepting single-mode).

---

## 3. THE STAGED BUILD (proper; each stage anchor-validated + verified)
- **P5e-0 (cheap, decide):** instrument the hybrid's validity bound (max|A| where err crosses, say, 1%);
  decide A1 vs A2 with that number in hand. (Closes Choice A on evidence, not guess.)
- **P5e-1 (build):** the coupled time-live residual = P1 off-diagonals (incl. time row) + P2 native S^2
  matter EL + P3 a(φ)=-1 weight + P4 time term, on the re-posed full-rank DOF, with multi-harmonic time +
  free-ω closure. NEW FILES.
- **P5e-2 (converge):** re-posed JFNK + pseudo-arclength continuation in amplitude. ANCHOR GATES: ω->0 =
  static round ground state (dense-LM); small-A = the fixed-bg eigenspectrum. #60 control converges. If
  JFNK stalls -> KEH/SCF (Principle 4).
- **P5e-3 (OBSERVE):** ramp amplitude; does the coupled finite-A solve TOWER/BIND (a nonlinear bound
  object) or SOFTEN/BOX-CONTROL (the airtight #65-consistent verdict)? Box-control gate on EVERY level.
  Report what's there. DATA-BLIND, observe-not-target.
- **P5e-4 (verify):** independent blind verifier — aimed hardest at any positive (a claimed bound object)
  and at the hybrid-validity / harmonic-truncation / anchor-reproduction gates.

---

## 4. RISKS (ranked) + the honest ceiling
1. **Throughput wall (#60-class) — the feasibility risk.** The coupled time-live free-ω solve may not
   reach a clean floor at usable resolution. Guard: the #60 control gate (stall = INCONCLUSIVE, not null);
   Principle-4 GR-corpus contingency (KEH/SCF, multidomain spectral). Honest: even built properly, P5e
   MAY be throughput-limited — that is itself a real, reportable finding about the solver, not a fudge.
2. **Hybrid outrun (Choice A).** Finite-A exceeds hybrid validity -> need A2 (true Einstein). Guard: the
   instrumented max|A| bound; build A2 when the data demands.
3. **Single-mode insufficiency (Pe-time).** Anharmonic at large A -> need multi-harmonic/evolution.
   Guard: harmonic-truncation convergence reported.
4. **Convergence-to-wrong-answer.** A strong new solver lands on a wrong fixed point. Guard: the dual
   anchor (static ω->0 + fixed-bg small-A).
5. **Box-control trap / observe-vs-target.** Any "intrinsic" level must pass the gate; no tower hunt.

SMUGGLED-FRAME CHECK: P5e is squarely metric-led + solver-completeness (build the solver properly,
observe). The honest residual: if it's throughput-limited, the airtight coupled verdict stays open (we'd
have the fixed-bg + structural answer + a documented solver ceiling) — that's an honest stopping point,
not a failure. P5e does NOT touch the deepest open Principle-7 item (UDT's native curvature-sector action),
which remains unbuilt and is separate.

## 5. WHAT IT TAKES (scoping, honest)
- P5e-0: cheap (instrument hybrid validity) — days.
- P5e-1/2: the real build — the multi-harmonic coupled residual + the continuation solver. Multi-week;
  the #60 throughput wall is the gating uncertainty; A2 (true Einstein) adds a codegen build if needed.
- P5e-3/4: the observe + verify once it converges.
This is a heavy, multi-agent build best run with FRESH context (it will not fit cleanly in a session
already at high usage). Recommend: do P5e-0 (cheap) to settle Choice A on evidence, then launch P5e-1+
in a fresh session. Anti-hang LOCKED throughout (bounded, single process, dense-LM flooring, NEVER
background-poll; the coupled solves are the slow ones — cap them).
