# MAP — STEP 2: the fully-coupled TIME-LIVE NATIVE-MATTER solve on UDT's DERIVED operator

**Mode:** MAP (no compute, no solve, no derive). **Status:** for Charles's steer; the build is
GATED on his go. **NOT canon.** **Driver:** claude-opus-4-8[1m]. **Date:** 2026-06-21.

**What this MAP is.** STEP 2 = the fully-coupled time-live solve WITH the native matter field Theta
included, on the newly-derived gravity operator. It EXTENDS `EVERYTHING_ON_SOLVER_P5e_REMAP_derived_operator.md`
(which was VACUUM-first: gravity+phi geon, no matter). The matter sector is the ADDITION. Everything
else — the derived operator, the machinery (re-pose/JFNK/dense-LM/gates/anti-hang), the staged-build
skeleton — is inherited from that re-MAP and from `EVERYTHING_ON_SOLVER_P5e_MAP.md` (the original P5e).

**Why STEP 2 now (the premise of this MAP).** `static_soliton_rerun_derived_operator_results.md` (STEP 3,
just done + blind-verified) showed the new operator's STATIC effect is small: the static charge-1 soliton
is "GR + a TINY 1/r hair" at the healthy X, with B=1/A broken dominantly by an operator-INDEPENDENT
matter-kinetic stress. Its verified headline: **"the new operator changes the STATIC structure only
modestly — the real teeth (broken absorbability) are in DYNAMICS, not the static profile" => the time-live
coupled solve (STEP 2) is where the new operator can actually bite.** This MAP sets up that solve, bounded
and anchor-gated.

Parents: `EVERYTHING_ON_SOLVER_P5e_REMAP_derived_operator.md` (the vacuum re-MAP, machinery + operator),
`EVERYTHING_ON_SOLVER_P5e_MAP.md` (original staged build, Choice A/B, gates, anti-hang),
`EVERYTHING_ON_SOLVER_BUILD_MAP.md`, `POST_POSTULATE_PROGRAM.md`, `SOLVER_COMPLETENESS_MAP.md` (governing).
Inputs: `static_soliton_rerun_derived_operator_results.md` (the omega->0 anchor),
`matter_regrade_derived_operator_results.md` (matter sector: coupling PHYSICAL, exchange law),
`F2_matter_action_forcedness_results.md` ({L2,L4} minimal-NOT-unique),
`native_dilation_weight_derivation_results.md` (operator + healthy X window),
`scale_symmetry_bootstrap_analysis_results.md` (box-control = the symmetry's fingerprint; matter = the breaker),
`coupled_timelive_solve_results.md` + `timelive_nonround_native_solve_results.md` (#65, the OLD-operator precedent).

---

## 0. WHAT STEP 2 IS (stated precisely)

> Solve, ALL TOGETHER and self-consistently, at FINITE amplitude, on the DERIVED operator:
> - the metric (A, B + the off-diagonals including the live TIME row g_tr),
> - the depth field phi (independent player, B=1/A NOT slaved),
> - the native matter field Theta WITH its live time dependence d_t Theta,
> - the frequency omega (free, an eigenvalue of the coupled system),
>
> on the two-player DERIVED action
> ```
> S = INT sqrt(-g) [ e^{2phi} R  +  X e^{2phi} g^{ab} d_a phi d_b phi  +  e^{2phi} L_m ],
> L_m = -(xi/2)(X_k + 2Y) - (kap/2)(2 X_k Y + Y^2),  X_k = g^{rr}(d Theta)^2, Y = sin^2(Theta)/r^2,
> ```
> with a(phi)=e^{+phi} (the DERIVED depth-flat weight, no longer a free baseline).
> NOT frozen-background. NOT linearized. NOT single-mode. This is the heaviest solve in the program
> (the #60-class throughput wall) and the one STEP 3 named as where the operator's teeth live.

This DIFFERS from #65 (the prior coupled time-live solve) in TWO ways at once: (i) the operator is the
DERIVED scalar-tensor one (vacuum != GR), not plain-GR a=-1; (ii) the matter coupling is the now-PHYSICAL
a(phi)=e^{+phi} weight whose absorbability the re-grade OVERTURNED. #65 had NEITHER. So STEP 2 is the
first coupled time-live solve where the operator's new dynamical content can act on a live matter field.

---

## 1. THE COUPLED TIME-LIVE RESIDUAL ON THE NEW OPERATOR (schematic)

**Fields (the unknowns of the coupled solve):** {A(r,t), B(r,t), g_tr(r,t)} (metric), phi(r,t) (depth),
Theta(r,t) (matter), omega (frequency). Time enters PERIODICALLY (oscillaton/breather ansatz).

**The four coupled equations the residual must encode** (all from ONE action, mutually consistent by the
scalar-tensor Bianchi/exchange identity, which is built in automatically when varying one action — STEP 3
verified this for the static case):

- **Metric (g-variation), the DERIVED operator with the box-f survivor KEPT:**
  ```
  E_mn := f G_mn + (g_mn box - nabla_m nabla_n) f - X f(d_m phi d_n phi - 1/2 g_mn (dphi)^2) = (1/2) Tw_mn,
  f = e^{2phi},  Tw_mn = e^{2phi} T^bare_mn (the WEIGHTED matter stress).
  ```
  Time-live: d_t != 0 on A, B, phi, Theta, and g_tr live (the time row). The DEEPENING (weight doc Sec 9,
  scale-symmetry Sec 1): g^{tt}~e^{+2phi} and g^{rr}~e^{-2phi} carry OPPOSITE shift-weight, so the phi-TIME
  kinetic sector is the one the uniform weight REFUSES — the second, DYNAMICAL scale-symmetry breaker that
  the static analysis cannot see. STEP 2 is the first solve that turns it on WITH matter.
- **Scalar (phi-variation):** box phi = R/X - (dphi)^2 + (matter source via the e^{2phi}L_m weight). The
  matter now SOURCES phi through the weight — new vs the vacuum re-MAP.
- **Matter (Theta-variation):** the L2+L4 hedgehog EL with the e^{2phi} weight live and d_t Theta != 0.
  This is the carrier #65 found revives into a standing-wave eigenproblem — now on the new operator + with
  the phi-source coupling.
- **The EXCHANGE law (not a separate eq — the consistency the residual must respect):**
  `nabla^mu Tw_mn = 2 e^{2phi} L_m nabla_n phi` (matter_regrade Sec 2). The matter stress is NOT
  separately conserved; it exchanges with phi. This is the TEETH: there is no relabeling to GR.

**Time treatment = MULTI-HARMONIC balance (NOT single-mode).** Expand Theta and phi in cosine harmonics at
fundamental omega, the metric in even harmonics (2omega, 4omega, ...), substitute into the four coupled
equations, set each Fourier coefficient to zero => a closed set of coupled radial ODEs; TRUNCATE at harmonic
N and INCREASE N until converged. Single-mode is the shortcut to AVOID (the finite-amplitude object is
ANHARMONIC; #65 used a single radial breather mode and flagged that as its residual scope-cost). Report
harmonic-truncation convergence.

**Free-omega closure.** omega is an eigenvalue: the object picks its own frequency self-consistently, shot
via the regularity-at-core + asymptotic-flatness BVP (only special omega give a non-dispersing periodic
state). NOT a scanned external omega. Containment: omega->0 MUST return the STEP-3 static soliton.

**Finite-amplitude continuation.** Ramp amplitude A from 0 via pseudo-arclength continuation. The
back-reaction at finite A is the WHOLE POINT — what linear analysis structurally cannot see. An A->0
"result" is just the known linear box-controlled answer.

---

## 2. REUSED vs NEW vs CHANGED (relative to the vacuum P5e re-MAP)

| | REUSED (verbatim from the vacuum re-MAP / P5e) | NEW (the STEP 2 addition) | CHANGED |
|---|---|---|---|
| Operator | the DERIVED e^{2phi}R + X e^{2phi}(dphi)^2 gravity kernel, box-f kept | — | the kernel is SET (the Choice-A fork is dissolved; only steep-core conditioning survives as numerics) |
| Matter | — | **the native Theta field (L2+L4), live d_t Theta, e^{2phi} weight, the phi-source coupling, the exchange law** | this is the whole addition vs the vacuum re-MAP |
| Machinery | re-pose to full-rank, JFNK + pseudo-arclength continuation, dense-LM flooring, KEH/SCF fallback, all gates, anti-hang | — | only the RESIDUAL gains the matter rows + the phi-matter source |
| Time | multi-harmonic balance, free-omega, evolution as cross-check | — | unchanged in form; now must carry the matter harmonics too |
| omega->0 anchor | the static-limit recovery | **= the STEP-3 static soliton** (GR + tiny hair; localized charge-1; B=1/A broken by matter-kinetic stress) — a CONCRETE, blind-verified anchor we now HAVE | the vacuum re-MAP's static anchor was the branch-G/P scale-free vacuum; STEP 2's is the FULL matter soliton STEP 3 just produced |
| small-A anchor | the box-controlled linear spectrum | the linear time-live MATTER spectrum (#65's revived standing-wave carrier, l(l+1) floor + box continuum) | the matter carrier's linear spectrum, not the vacuum's |

**The one-sentence delta:** STEP 2 = the vacuum P5e re-MAP solve PLUS the native matter field (Theta, its
live time-dependence, its e^{2phi} weight, its phi-exchange), anchored at omega->0 to the STEP-3 static
soliton instead of to the vacuum branch.

---

## 3. GATES (anchor-validated; each MUST pass before the next is trusted)

1. **omega->0 => STEP-3 STATIC SOLITON (the lower anchor).** The coupled solve at vanishing frequency MUST
   reproduce the blind-verified STEP-3 result: localized charge-1 hedgehog, GR + tiny 1/r hair (q ~ 1/|X|),
   B=1/A broken dominantly by the operator-independent matter-kinetic stress. Via dense-LM on saved fields.
   If it does not recover STEP 3, the time-live residual is wrong — STOP.
2. **small-amplitude => the LINEAR box-controlled spectrum (the upper anchor).** At A->0 the coupled solve
   MUST reproduce the linear time-live matter spectrum (#65's standing-wave carrier: the l(l+1) angular
   floor + the box continuum, omega^2 ~ 1/R^2 -> 0). If small-A does not match the known linear answer, the
   finite-A results are not trustworthy.
3. **#60 CONVERGENCE-CONTROL gate.** A known-relax control problem must floor on the SAME machinery. If the
   control STALLS, the STEP 2 result is SOLVER-LIMITED => report **INCONCLUSIVE**, never a null. (The
   coupled time-live solve on the steep e^{2phi} core + matter is the program's heaviest; this gate is the
   honest stop.)
4. **BOX-CONTROL gate on ANY claimed intrinsic scale/level** (3-criteria, mandatory): cell-scan +
   wall-relocation + intrinsic-lock. Any omega/size that scales as 1/R or tracks the box wall is a BOX
   artifact, not intrinsic. The scale-symmetry result (box-control = the dilatation fingerprint, vacuum) +
   the AdS-massless precedent make this non-negotiable. NOTE (load-bearing, from scale-symmetry verifier):
   MATTER does pin a real length l=sqrt(kap/xi) the vacuum symmetry would not — so a length appearing is
   EXPECTED and is NOT itself the discreteness claim; the gate is about whether a DISCRETE LEVEL is
   intrinsic, not whether a size exists.
5. **Harmonic-truncation convergence gate.** Increase harmonic order N until the object is stable; report
   what was dropped. (#65's single-mode was its named residual.)
6. **Verifier-before-record.** Blind adversarial pass aimed HARDEST at any positive (a self-trapped
   intrinsic-scale bound object) and at gates 1-5. Record agent id + date.

---

## 4. PREMISE LEDGER (chose / derived)

| # | choice | proper default | CHOSE / DERIVED | risk / guard |
|---|---|---|---|---|
| **Pr-X** (FOR CHARLES) | the X dial | **FIX X at one healthy value (e.g. X = -2e5, inside ghost-free + Cassini-safe |X|>1.7e5, large negative) for the existence question; SCAN only if existence is X-sensitive** | CHOSE | the binary is "does a self-trapped time-periodic object EXIST in the healthy window?"; one healthy X answers it. Do NOT use small/ghost X (forbidden by ghost+Cassini) to manufacture a state. |
| **Pr-charge** (FOR CHARLES) | matter sector | **charge-1 native hedgehog (Theta: pi->0, two opposite nodes, degree-1)** | CHOSE | the NATIVE degree-1 sector (STEP 3's P3), NOT the imported m>=2 winding-BC ladder (#61 import flagged). Do not build the ladder to manufacture a spectrum. |
| **Pr-action** (FOR CHARLES) | matter Lagrangian | **{L2, L4}** | CHOSE-minimal | F2: {L2,L4} is MINIMAL-but-NOT-UNIQUE (X^2 admissible by invariance, not area-form-native). A self-trapped object that DEPENDS on the L4-vs-X^2 choice would be action-fragile — flag if it does. |
| Pr-amp | amplitude | **FINITE, continued from 0** | DERIVED-necessary | the back-reaction is what linear misses; an A->0 result is the known linear answer. |
| Pr-harm | time treatment | **MULTI-harmonic balance; evolution as cross-check** | CHOSE | single-mode is the shortcut (#65's residual); report truncation convergence. |
| Pr-omega | omega | **free / self-consistent eigen-omega** (shot, not externally scanned) | DERIVED-necessary | omega->0 MUST return the STEP-3 static soliton (gate 1). |
| Pr-B | B=1/A | **FREE (not imposed)** | DERIVED-necessary | STEP 3 showed B=1/A breaks in the matter body; imposing it is the #55 scar. Keep free, measure it. |
| Pr-chart | radial chart | **isotropic/horizon-penetrating for the oscillating metric** | CHOSE | areal is the static-exhibit chart; an oscillating throat is stiff in areal. Cross-check chart-robustness of any obstruction. |
| Pr-weight | matter coupling | **S_matter = INT sqrt(-g) e^{2phi} L_m (weight out front, phi indep of g)** | CHOSE (matter_regrade R3) | the alternative non-minimal placement shifts J_phi but NOT the broken-tautology / teeth conclusion. |
| Pr-kernel | gravity operator | **the DERIVED e^{2phi}R + X e^{2phi}(dphi)^2** | DERIVED | NOT the old hybrid; NOT plain Einstein. Choice-A fork dissolved; only steep-core conditioning survives (numerics). |
| Pr-box / Pr-conv / Pr-anchor | the gates | as in Sec 3 | DERIVED-gates | the standing traps; dual-anchor (STEP-3 static + linear small-A) before any finite-A result is trusted. |

### The premises for YOUR eye, Charles — see Sec 7.

---

## 5. THE STAGED BOUNDED BUILD (each stage bounded + anchor-gated + verifiable; ANTI-HANG LOCKED)

**ANTI-HANG LOCKED throughout (binding):** Nr <= 16/24, cap Newton/Krylov iters, **SINGLE clean process
(NEVER concurrent — GPU contention stalls everything)**, dense-LM flooring on SAVED fields, **NEVER
background-poll a solve (6+ agents hung this way)**. The coupled time-live solves are the SLOW ones
(minutes to ~1700s). If a solve would exceed budget, REDUCE (coarser grid / fewer harmonics / weaker
source) and report **throughput-limited** — a bounded honest partial beats a hang. A stage that cannot
converge is **INCONCLUSIVE (solver-limited)**, never a null.

- **S2-0 (cheap — build the matter-coupled time-live residual).** Codegen the four-field time-live residual
  (metric incl. time row + phi + Theta + the e^{2phi} weight + the phi-matter source + the exchange law)
  in the chosen chart, multi-harmonic in time, free-omega. VALIDATE symbolically vs the STEP-3 static EL
  (the omega->0 limit) and vs a sympy recomputation. Instrument steep-core conditioning. *Gate:* symbolic
  match to the STEP-3 static residual at omega->0 + sympy cross-check. (No solve yet.)
- **S2-1 (anchor the two limits).** On the new residual reproduce, on the SAME machinery: (a) **omega->0 =>
  the STEP-3 static soliton** (dense-LM, saved fields) — gate 1; (b) **small-A => the linear box-controlled
  matter spectrum** (#65's carrier) — gate 2. BOTH must pass before any finite-A result. *Gate:* dual-anchor.
- **S2-2 (converge the nonlinear branch).** Re-posed full-rank JFNK + pseudo-arclength continuation in
  amplitude, shooting the eigen-omega, multi-harmonic order increased to convergence. #60 control gate
  (gate 3): a known-relax control floors on this machinery; if it stalls => INCONCLUSIVE. KEH/SCF fallback
  if JFNK stalls (Principle 4). *Gate:* converged floor + control pass + harmonic-truncation convergence.
- **S2-3 (OBSERVE — bounded, data-blind).** Ramp amplitude finite. Does the coupled matter+time+new-operator
  solve produce a **self-trapped time-periodic object with an INTRINSIC scale** (localized, phi->0 and
  Theta->seal at infinity, finite mass-energy, a discrete level that survives the box-control gate) — or
  does it **disperse / box-control** (omega~1/R, the level tracks the wall)? **BOX-CONTROL gate (gate 4) on
  ANY claimed intrinsic level** — remembering matter's l=sqrt(kap/xi) size is expected and is not itself the
  discreteness claim. DATA-BLIND, observe-not-target. Report WHAT IS THERE with premises attached.
- **S2-4 (persistence cross-check).** For ANY claimed self-trapped object: a bounded 1+1 EVOLUTION from the
  constructed initial data, **3-cell persistence test** (not 2-cell — look-elsewhere false positives),
  watching radiative dispersal vs persistence over many periods. Unbiased kicks + NEB if a landscape claim
  is made (NEVER blend a field toward a chosen endpoint — the biased-artifact scar).
- **S2-5 (verify).** Independent BLIND adversarial verifier, aimed HARDEST at any positive and at gates
  1-5 (dual-anchor, box-control, harmonic-truncation, chart-robustness). Verifier-before-record; agent id + date.

---

## 6. RISKS + THE HONEST CEILING

1. **Throughput wall (#60-class) — the feasibility risk, now HEAVIER than the vacuum re-MAP.** STEP 2 adds
   the matter rows + the phi-matter source on top of the steep e^{2phi} core that STEP 3 already showed
   grid-limits at strong coupling (Nr<=24 cannot resolve B~6-8 near-horizon curvature). The coupled
   nonlinear time-live free-omega multi-harmonic solve may not reach a clean floor at usable resolution.
   Guard: the #60 control gate (stall = INCONCLUSIVE, not null); Principle-4 GR-corpus contingency (KEH/SCF,
   oscillaton harmonic-balance BVP machinery). **Honest: STEP 2 MAY be throughput-limited — that is a REAL
   FINDING about the solver, not a null.** We would still hold STEP 3's static structure + the linear
   box-control + a documented nonlinear-matter-solver ceiling. A legitimate stopping point.
2. **Steep-core conditioning of e^{2phi} WITH matter.** STEP 3 saw the strong-coupling regime go
   grid-limited; the time-live version inherits it and adds the time harmonics. Guard: Taylor-accurate
   function replacement through folds (allowed, not the forbidden linearization); honest deep-core treatment
   (no cutoff smuggling the endpoint); start at the resolvable coupling (xi=kap<=2e-2 per STEP 3) and
   continue.
3. **Box-control trap faking a periodic state.** A confined carrier looks periodic because the box confines
   it (the AdS-massless precedent). Guard: the box-control gate is mandatory on every claimed level; a level
   that vanishes under wall-relocation is an artifact.
4. **Harmonic-truncation hiding structure.** Single/low-harmonic at large amplitude misses anharmonic
   structure (#65's named residual). Guard: increase N to convergence; report what was dropped.
5. **Convergence-to-wrong-fixed-point.** A strong driver on the new matter-coupled operator lands on a
   spurious state. Guard: the dual anchor (STEP-3 static omega->0 + linear small-A) before trusting finite-A.
6. **Observe-vs-target.** STEP 2 is the "remaining classical redoubt" — the risk is WANTING the new
   operator to finally bite. Guard: data-blind; box-control gate; verifier aimed hardest at any positive;
   the honest expectation stated up front (below).

**HONEST EXPECTATION (anti-false-convergence, stated UP FRONT).** Everything points to LIKELY box-control:
#65 (OLD operator) was box-controlled; STEP 3 shows the new operator's STATIC effect is tiny; the
scale-symmetry result says vacuum is scale-free and even the LINEAR time-live (new operator) is
box-controlled. So the LIKELY outcome is STILL box-control — closing the last classical redoubt and making
"discreteness requires quantization" airtight on the DERIVED operator WITH matter. The GENUINE OPEN — the
ONLY reason to build this — is that the new operator's teeth ARE in dynamics (STEP 3's verified headline),
and the now-PHYSICAL matter coupling (the exchange law, no relabeling to GR) is the one new ingredient vs
#65: the nonlinear matter+time+new-operator coupling MIGHT lock a self-trapped object with an intrinsic
scale that linear analysis structurally misses. We do not know. **We build to LEARN. Observe-not-target.
DATA-BLIND. Either outcome is first-class** (a clean box-control verdict closes the redoubt; a self-trapped
intrinsic level would be the first classical intrinsic discreteness and would reopen the quantization
question — both real, both major).

**THE HONEST CEILING.** STEP 2 could be INCONCLUSIVE (throughput-limited) — a real finding, a legitimate
stop. If it CONVERGES and box-controls (expected), the last classical redoubt is closed on the derived
operator with physical matter. If it CONVERGES and finds a self-trapped intrinsic-scale object (the genuine
open), that is a major result demanding the hardest verification. We do not know which; we build to find out.

---

## 7. THE PREMISES FOR CHARLES'S EYE (2-3)

**(i) Fix X or scan it?** RECOMMEND **fix X at one healthy value (~ -2e5, large-negative, inside the
ghost-free + Cassini-safe |X|>1.7e5 window) for the EXISTENCE question, then scan only if it matters.**
Lay reasoning: the binary we care about is "does a self-trapped time-periodic object exist AT ALL in the
healthy window?" — a yes/no one healthy X answers. If it exists, we scan X to map how its scale/frequency
move. If existence depends delicately on X, that delicacy is itself a finding. What I will NOT do silently
is reach for a small or ghost-side X (forbidden by ghost+Cassini) to manufacture a bound state — that is
the "fix a value to make it solvable" scar. Your call if you'd rather scan from the start.

**(ii) Charge-1 native hedgehog only, or also the m>=2 winding?** RECOMMEND **charge-1 native degree-1
sector ONLY** for this solve. Lay reasoning: degree-1 is the native two-node hedgehog STEP 3 used; the
m>=2 winding ladder carries an IMPORTED boundary condition (flagged #61) that we do not want manufacturing
a spectrum. The catalog of DISTINCT objects (distinct charges/sectors) is a SEPARATE frontier (the post-#65
pivot); STEP 2 is about whether ONE charge-1 object self-traps with an intrinsic scale, not about the
multi-object catalog. Your call if you'd rather see a charge-2 run as a contrast.

**(iii) {L2,L4} is minimal-but-NOT-unique — do we accept that for this solve?** RECOMMEND **yes, run on
{L2,L4}** (the cleanest, area-form-native basis) but FLAG hard if any self-trapped object turns out to
DEPEND on the L4-vs-X^2 choice (F2: X^2 is admissible by invariance, not area-form-native). A bound state
that exists only for one non-unique action term would be action-fragile and must be reported as such, not
banked as "the metric self-traps." Your call if you want the X^2 contrast run up front rather than only
on a positive.

---

## 8. SMUGGLED-FRAME CHECK

STEP 2 is squarely metric-led + solver-completeness: build the DERIVED operator's matter-coupled time-live
solver properly and OBSERVE. The Principle-7 hole ("vacuum = GR by construction") is CLOSED — the operator
is derived, vacuum != GR, and matter_regrade overturned absorbability so the matter coupling is PHYSICAL.
This is exactly why STEP 2 is worth doing on the OWN operator, not an imported Einstein kernel. The honest
residual: if throughput-limited, the airtight nonlinear-matter verdict stays open (we hold STEP-3 static +
linear box-control + a documented ceiling) — an honest stop, not a failure. Matter is here NOT to
manufacture a scale but because STEP 3 named DYNAMICS-with-matter as where the operator's teeth are; the
box-control gate + data-blind + the up-front honest expectation guard against targeting the hoped-for bite.
A SIZE appearing (l=sqrt(kap/xi)) is EXPECTED (matter breaks the vacuum scale symmetry) and is NOT itself
the discreteness claim — the claim is a DISCRETE intrinsic LEVEL surviving the box-control gate.
