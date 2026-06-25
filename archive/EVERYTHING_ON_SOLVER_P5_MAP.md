# MAP — P5: the research-grade off-round coupled solver

**Mode:** MAP (no compute). **Status:** for Charles's steer; the build is GATED on his go.
**NOT canon.** **Driver:** claude-opus-4-8[1m]. **Date:** 2026-06-20.
Parent: EVERYTHING_ON_SOLVER_BUILD_MAP.md (P5 = §III, the named feasibility crux). This is the
FIRST genuinely-unscoped phase (P1-P4 were assembly on clean primitives; P5's METHOD is an open
choice) — so the MAP earns its keep here. Build contingency is BINDING (Charles, Principle 4):
mine the GR numerical-relativity corpus before reinventing.

---

## 0. WHAT P5 IS — and is NOT

It IS: a **solver strong enough to drive the full coupled OFF-ROUND + TIME-LIVE + a(φ) system to a
clean floor** (Φ ≲ 1e-9, grid/Nth-converged) where the dense-Newton stalls. It is the **load-bearing
feasibility crux of the whole everything-on program** (named so in the build MAP): every deferral
from P2/P3/P4 comes due here.

It is NOT physics — it is the TOOL. The physics is the off-round time-live coupled SOLVE it enables
(then OBSERVE per the corrected program, then quantize P7). P5 builds the engine; it does not by
itself answer any physics question, and it must not be allowed to manufacture one.

It is NOT a from-scratch invention: Principle 4 (binding contingency) says **survey the GR corpus
and transform a proven method under positional dilation**, rather than reinvent. Many have solved
coupled-Einstein-matter systems with this structure (boson stars, rotating neutron stars, geons).

## I. WHAT P5 MUST DELIVER (the deferred items, all due here)

- **P2-shear:** the off-round coupled solve (the matter EL sees off-diagonals; e_rt etc. solved, not
  imposed) — is the SOLVED object round or non-round? (the genuine version of P2's deferred question)
- **P3-deep-φ:** the deep-core regime where a(φ) departs from GR by O(1) (the shallow-φ anchor
  couldn't reach it) — needs this + an honest deep core (P6).
- **P4-off-round-time-live:** the full off-round time-live coupled solve to a FREE-ω eigenvalue (P4
  wired it + proved containment; the solve itself is here).
- Throughout: validated against the **dense-Newton ANCHOR** (the correctness reference), box-control
  checkable, the pole-stable-hybrid validity respected or upgraded.

## II. THE STARTING POINT + WHAT HAS ALREADY FAILED (do not repeat)

- **Dense-Newton (full3d_newton, jacrev + direct LM): CLEAN + the correctness ANCHOR** — proven to
  ~1e-13 on small grids, no B=1/A tie, no injection. BUT does NOT scale: the jacrev Jacobian BUILD
  dominates (38-133 s/iter at modest grids; ~1700 s/solve under the broken-NVML no-cache allocator),
  and it is too slow at the 32³-class grids the off-round search needs. It is the reference, not the
  production engine.
- **Matrix-free Jacobi-PCG LM (full3d_solver.lm_solve): STALLS off-round** (~1e-5; the preconditioned-
  CG step is not a descent direction; tried with both cheap and geometric coarse). The #60 wall.
- **Warm-start continuation across grids: DRIFTS** (interp injects non-axisym structure into steep
  solitons; m=1 drifts 0.29→0.33). Plain continuation DON'T-retry.
- **The conditioning root:** the steep soliton core (b = p·ln(r/r_seal)) makes the operator badly
  conditioned — the same root that forced the P1/P4 pole-stable hybrid. P5's preconditioner must
  address exactly this.

## III. CANDIDATE GR-CORPUS METHOD FAMILIES (the Principle-4 mine — to be surveyed + ranked)

High level; the ranked selection is P5-step-1 (the survey), gated. Each with fit + risk:

- **Newton-Krylov with a PHYSICS-BASED / elliptic preconditioner** (the recon's lead). Fit: keeps
  Newton's quadratic convergence + the anchor's correctness, fixes the matrix-free stall via a real
  preconditioner (elliptic/operator-split, addressing the steep-core conditioning). Risk: building an
  effective preconditioner for the coupled off-round operator is the hard part.
- **Self-Consistent Field (KEH / Hachisu)** — the workhorse of rotating-neutron-star + boson-star
  solvers. Fit: purpose-built for coupled Einstein-matter equilibria with exactly our structure;
  integral (Green's-function) inversion sidesteps the steep-operator conditioning. Risk: classic SCF
  assumes stationarity/specific gauges — must be transformed for time-live (harmonic-balance) + the
  native S² matter, and not smuggle a frozen DOF or a gauge.
- **Sparse-direct factorization exploiting the spectral structure** — Fit: the dense-Newton is
  correct but dense; exploiting the spectral block-sparsity could make the exact Newton step affordable
  at scale. Risk: the spectral operator may not be sparse enough; engineering-heavy.
- **Multigrid** (geometric/algebraic) — Fit: optimal for elliptic systems; could precondition the
  Newton-Krylov. Risk: the steep-core + spectral bases complicate standard multigrid.
- **Pseudo-arclength continuation** — Fit: for tracking branches/eigenvalues robustly past folds (the
  free-ω eigenvalue, branch structure). Risk: a continuation tool, not a base solver; pairs with one
  of the above. (Plain warm-start continuation already FAILED — this is the principled version.)
- **Boson-star / gravitating-soliton solver techniques** (shooting+relaxation hybrids, frequency
  eigenvalue methods) — Fit: these solve "matter field + metric + a frequency ω" systems exactly like
  our time-live object. Risk: usually 1-D/spherical; the off-round (3-D) generalization is the work.

## IV. THE SELECTION PROCESS + VALIDATION STRATEGY

- **P5-step-1 (gated): GR-corpus SURVEY-AND-SELECT.** A proper survey of the families above (and any
  others), matched to OUR operator (coupled Einstein + native S² matter + a(φ) ruler weight +
  harmonic-balance time, spectral bases, steep-core conditioning), returning a RANKED recommendation
  with the premise ledger per method — brought back for Charles's sign-off BEFORE any solver is built.
- **THE ANCHOR (binding validation):** the dense-Newton is the CORRECTNESS REFERENCE. Any new solver
  must reproduce it on EVERY case both can run (round, mild off-round, small grids) to floor, BEFORE
  its off-round/at-scale results are trusted. A new solver that "converges" to a different answer is
  WRONG until proven otherwise against the anchor. (This is the #1 risk's guard.)
- **The #60 axisym-control gate** stays: a known-relax control case must converge on the new solver,
  or the off-round search is still solver-limited (report INCONCLUSIVE, not a null).

## V. PREMISE LEDGER — where a P5 method could smuggle physics into "numerics"

| # | Choice | Default | CHOSE / DERIVED | Risk / guard |
|---|---|---|---|---|
| P5-method | which GR-corpus method | TBD (survey-and-select, step-1) | CHOSE (engineering) — but anchor-validated | the method is a tool choice; correctness is enforced by the anchor, not the method's pedigree. |
| P5-anchor | correctness reference | dense-Newton (~1e-13 small grid) | DERIVED-as-method | **#1 RISK: a new solver converging to a WRONG answer.** Guard: reproduce the anchor on every shared case before trusting at-scale results. |
| P5-precond | the preconditioner | physics/elliptic, addressing steep-core | CHOSE (engineering) | a preconditioner must NOT change the fixed point (only the path to it) — verify the converged solution is preconditioner-INDEPENDENT. |
| P5-box | box-control | R-independence stays checkable | DERIVED-gate | the standing scar; any "intrinsic" off-round result must pass Gate A. The new solver must not bake in a box dependence. |
| P5-frozen | DOF frozen to aid convergence | NONE | binding | SCF/continuation can tempt freezing a DOF or gauge to converge — FORBIDDEN beyond declared (the everything-on point); flag any. |
| P5-hybrid | the pole-stable hybrid validity | small-shear/small-ω (P1/P4) | scope-honest | the off-round SOLVE may push shear/ω OUTSIDE the hybrid's valid regime (P1: err~0.5·A; P4: O(ω)). Then the HYBRID itself needs upgrading (a true well-conditioned general Einstein) — P5 must check it stays valid or fix it. |
| P5-BC | boundary conditions | native seal + node core (no Skyrme) | DERIVED | no imported BC sneaking in via a borrowed solver template (#61). |
| P5-observe | observe vs target | observe what the off-round solve contains | binding | the whole point: P5 enables the OBSERVE; do not target a tower/catalog (retired). |

The ones for YOUR eye: **P5-method** (the survey's ranked recommendation — you sign off the choice)
and **P5-hybrid** (whether the off-round solve outgrows the pole-stable hybrid, forcing a true
general-Einstein upgrade — a real possible scope expansion).

## VI. THE COMPLETENESS BAR (when a P5 off-round result may mean something)
(1) the new solver reproduces the dense-Newton anchor on every shared case to floor; (2) the #60
axisym-control converges; (3) converged to floor + grid/Nth-converged + box-control checked; (4) the
pole-stable hybrid is verified valid in the solved regime (or upgraded); (5) the converged solution is
preconditioner-independent. Until all hold, an off-round result is solver-limited, not a verdict.

## VII. RISKS (ranked)

1. **Feasibility (the program's load-bearing risk).** No surveyed method may reach a clean off-round
   floor at scale. If so, that is an HONEST solver-limit on the whole everything-on program — reported
   as such, after the corpus is genuinely mined (Principle 4), never dressed as a physics null.
2. **Convergence-to-wrong-answer.** A strong new solver that lands on a wrong fixed point. Guard: the
   anchor (P5-anchor), preconditioner-independence (P5-precond).
3. **The hybrid outgrown.** The off-round solve pushes outside the pole-stable hybrid's validity →
   need a true well-conditioned general Einstein (a real scope expansion, possibly large).
4. **Throughput even if convergent.** A method that converges but is too slow to scan/converge grids
   (the broken-NVML allocator compounds this). May need the GPU-allocator issue addressed.
5. **Smuggled freeze/gauge/BC** via a borrowed solver template. Guard: the premise ledger + greps.

## VIII. WHAT IT TAKES (scoping, honest)
- P5-step-1 (survey-and-select): a focused recon — days — returning a ranked, premise-ledgered method
  recommendation for sign-off.
- The build: research-grade numerics — the multi-week core of the whole program. The payoff: the
  off-round time-live coupled solve becomes reachable → OBSERVE what the metric does (the corrected
  program's actual question) → then quantize (P7). This is where the everything-on solver finally
  pays out — or where the program meets an honest solver-limit.
