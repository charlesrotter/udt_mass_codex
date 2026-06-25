# MAP — P5e RE-POINTED onto UDT's DERIVED gravity operator (vacuum-first nonlinear time-live geon)

**Mode:** MAP (no compute, no solve, no derive). **Status:** for Charles's steer; the build is
GATED on his go. **NOT canon.** **Driver:** claude-opus-4-8[1m]. **Date:** 2026-06-21.
**Supersedes (for the operator only):** EVERYTHING_ON_SOLVER_P5e_MAP.md was written for the OLD
plain-hybrid-Einstein, a=-1 kernel ("Choice A"). The gravity operator is now DERIVED
(`native_dilation_weight_derivation_results.md`), so the kernel is no longer a hybrid choice —
it is fixed by the action. This doc re-points the P5e build onto that derived operator. The OLD
P5e MAP's MACHINERY (re-pose, JFNK, dense-LM, gates, anti-hang) is REUSED; its KERNEL is REPLACED.
Parents: EVERYTHING_ON_SOLVER_BUILD_MAP.md (machinery), POST_POSTULATE_PROGRAM.md,
SOLVER_COMPLETENESS_MAP.md (governing). Inputs: branch_G_/branch_P_characterization_results.md.

---

## 0. THE QUESTION THE NEW SOLVER MUST ANSWER (stated precisely, vacuum-first)

> Does UDT's DERIVED two-player theory
> ```
> S = INT sqrt(-g) [ e^{2phi} R + X e^{2phi} g^{ab} d_a phi d_b phi  ( + Branch P: - 2 U(phi),  U = e^{2phi}-1 ) ],
> ```
> with **phi and the metric INDEPENDENT** (two players, phi NOT slaved), **TIME-LIVE** and
> **spherically symmetric**, admit a genuinely **NONLINEAR, time-periodic, SELF-TRAPPED** bound
> object (an oscillaton/geon) with an **INTRINSIC SCALE** — or does it **DISPERSE / box-control**
> (omega ~ 1/R, continuum)?

**VACUUM FIRST.** No matter field. The obstruction (the angular-curvature survivor / the
phi-time anisotropy) lives in the gravity+phi action ITSELF; the weight derivation and both
branch docs locate the candidate scale-carrier in the vacuum gravity+phi sector, not in an added
matter field. Matter is a LATER add, attempted ONLY if the vacuum sector is scale-free (consistent
with the program: vacuum structural theorems #62-64 say matter is needed for a *static* object —
but the OPEN question here is a *time-live* vacuum geon, which is a different object and must be
checked on its own before concluding "matter required").

**Why this is THE question now.** Everything classical so far points one way:
- BOTH static branches are SCALE-FREE (branch_G: massless scalar-tensor {m,q} hair, monotone,
  phi'~1/r^2, no length; branch_P: scale-invariant master eq, r^2 measure cancels 2/r^2 angular
  curvature, value-pin not size-pin, only log-periodic self-similarity = continuous, no lowest mode).
- The LINEARIZED time-live operator (the NEW vacuum!=GR operator) is STILL box-controlled: the
  branch_P verifier discretized it on boxes R=50..400 and found **omega*R = 2.584 CONSTANT =>
  omega ~ 1/R** (continuum), exactly like all prior time-live work.

So the **ONLY remaining classical redoubt** for scale/discreteness is a genuinely **NONLINEAR**
time-live self-trapped object that **linear analysis structurally cannot see**. The headline
"discreteness must come from QUANTIZATION (postulate A)" hinges on closing THIS redoubt. P5e is
the tool that closes it — built on the DERIVED operator, not the old hybrid.

---

## 1. THE OPERATOR CHANGE (explicit) — what is REUSED vs what CHANGES

### 1.1 The kernel REPLACEMENT (the heart of the re-point)

| | OLD P5e MAP | NEW (this re-point) |
|---|---|---|
| Gravity action | plain Einstein-Hilbert R (hybrid G_weyl + [full-diag] codegen) | **e^{2phi} R** (NON-minimal weight f(phi)=e^{2phi}), DERIVED |
| Scalar/depth term | implicit, phi tied to metric warps | **X e^{2phi}(dphi)^2**, X large NEGATIVE (healthy+Cassini window), phi an INDEPENDENT player |
| Matter mass coupling | a = -1 (GR) baseline, the one physics CHOICE | **MOOT here: vacuum-first, no matter field.** a(phi)=e^{+phi} is DERIVED if/when matter is added later (it is the depth-flat value, no longer a free baseline) |
| Vacuum behaviour | "vacuum = GR by construction" (the old Principle-7 hole) | **vacuum != GR** (box f = 2phi''+4phi'/r survives); the operator is DERIVED, the hole is CLOSED |
| The "Choice A" Einstein-kernel fork | LIVE (A1 continuation-in-hybrid vs A2 true-general-Einstein) | **DISSOLVED.** There is no hybrid to stay inside and no plain-Einstein to build "properly": the kernel is the derived scalar-tensor operator, full stop. The conditioning question (steep core) REMAINS and is now about the e^{2phi}-weighted operator, not about a hybrid's validity bound. |

**Consequence for the old MAP's Choice A.** The single biggest open in the old P5e MAP — A1
(continuation inside hybrid validity) vs A2 (build the true general Einstein) — is **no longer a
physics fork**. The operator is given. What survives of A is purely a NUMERICS/conditioning
concern: the e^{2phi} weight is steep at large |phi| (deep core), and the field equations carry
the box f and (g box - nabla nabla)f terms, so the residual codegen must be built for the
DERIVED operator and well-conditioned on the steep core. That is engineering on a FIXED operator,
not a choice between two physics kernels.

### 1.2 The DERIVED field equations the residual must encode (from branch docs, two-player)

**Metric (g-variation):**
```
f G_mn + (g_mn box - nabla_m nabla_n) f - X f ( d_m phi d_n phi - 1/2 g_mn (dphi)^2 ) [ + g_mn U ] = 0,
f = e^{2phi},  f' = 2f.
```
**Scalar (phi-variation):**
```
Branch G:  R - X (dphi)^2 - X box phi = 0   =>   box phi = R/X - (dphi)^2.   (MASSLESS, V=0)
Branch P:  add the potential:  f' R + X f'(dphi)^2 - 2X nabla(f nabla phi) - 2U' = 0,  U' = 2e^{2phi}.
```
For the **time-live** solve these are taken with d_t phi != 0 and a time-dependent metric (the
clock factor g_tt, the radial g_rr, and — if rotation/g_tr ever turned on — the off-diagonals).
The DEEPENING (weight doc Sec 9): g^{tt}~e^{+2phi} and g^{rr}~e^{-2phi} carry OPPOSITE shift-weight,
so the phi-TIME kinetic sector is the one the uniform weight REFUSES — exactly the sector a
nonlinear time-live solve probes, and the structural reason this is the redoubt.

### 1.3 What of the OLD P5e MAP / BUILD MAP MACHINERY still applies (REUSED, unchanged)

ALL of the following are operator-agnostic plumbing and carry over verbatim:
- **Re-pose to full-rank** (P5a') — the committed Jacobian is rank-deficient without it; keep it.
- **JFNK (re-posed full-rank Newton-Krylov)** as the primary driver; **pseudo-arclength
  continuation** for the omega/amplitude branch (principled replacement for failed warm-starts).
- **dense-LM (jacrev + lstsq) flooring** as the bounded correctness tool on SAVED fields / small grids.
- **GR-corpus fallback (KEH/Hachisu SCF, spectral-elliptic)** if JFNK stalls (Principle 4).
- **Anchor gates, box-control gate (cell-scan + wall-relocation + intrinsic-lock), #60 convergence
  control gate, observe-not-target, DATA-BLIND.**
- **Anti-hang LOCKED:** Nr<=16/24, cap Newton/Krylov iters, SINGLE clean process, dense-LM on saved
  fields, **NEVER background-poll** (6+ agents hung). Time-live coupled solves are the slow ones.

**What CHANGES inside the machinery:** only the RESIDUAL KERNEL (now the derived scalar-tensor
operator with e^{2phi}, box f, X-kinetic, optional U) and the ANCHOR TARGETS (the anchors are now
the branch-G/branch-P static scale-free solutions and the box-controlled linear spectrum the
verifier found — see Stage gates). The solver SKELETON is unchanged.

---

## 2. GR-CORPUS METHOD MINE (Principle 4 — the "build it properly" raw material)

The self-gravitating-time-periodic-scalar literature is a direct, deep mine. Findings (cited):

### 2.1 MASSLESS scalars DISPERSE — confirmed, and it is the central caveat

- **Massless real scalar fields do NOT form compact self-gravitating objects; they disperse,
  and fast.** Massive real scalars collapse to time-periodic **oscillatons** (Seidel-Suen 1991);
  massless ones radiate/disperse. (gr-qc/0310006, Alcubierre et al.; review 1911.03340.)
- **The scale of an oscillaton is the Compton wavelength of the field's MASS.** The size and mass
  of the object are set by m_Phi; remove m_Phi and there is **no inherent length scale and
  localization fails.** Even the EXPONENTIAL-potential oscillaton paper (2511.02878,
  Mahmoodzadeh et al. 2025) — the closest analogue to UDT's e^{2phi} potential — STILL enforces
  `V0 = m^2/(lambda^2 k0)` "for dimensional consistency and the correct quadratic limit": the
  exponential nonlinearity ALONE does not self-trap; a mass scale is required.
- **AdS exception:** time-periodic massless-scalar solutions DO exist with a NEGATIVE cosmological
  constant (the AdS box) (PRL 111.051102, Maliborski-Rostworowski). The AdS curvature radius
  supplies the confining scale — i.e. an EXTERNAL box, the analogue of our "wall-relocation /
  box-control" trap. This is a WARNING, not an encouragement: a confined massless scalar can look
  periodic because the BOX confines it, which is exactly the omega~1/R artifact the gate must kill.

**Read-across to UDT.** Both UDT branches are scale-free in vacuum and the scalar is MASSLESS
(branch_G: explicitly V=0, massless; branch_P: U is a runaway value-pin, not a confining mass
well, and the master eq is scale-invariant). So the corpus's default prediction for UDT-vacuum is
**DISPERSAL / no intrinsic scale** — fully consistent with the static branch results and the
linear box-control. This is the HONEST baseline expectation (Sec 3).

### 2.2 Does the NON-MINIMAL coupling (e^{2phi}R) rescue self-trapping? — the one real "maybe"

The genuinely open physics the linear analysis cannot settle:
- **A direct scalar-Ricci coupling (f(phi)R) GENERATES an effective mass for the scalar**
  (spontaneous scalarization literature: 1903.10471, 2211.01766, 1003.4767). When the curvature
  drives `m_eff^2 < 0` the constant-scalar config is **tachyonically unstable** and the
  nonlinearity quenches it into a **nontrivial scalar configuration that is no longer an Einstein
  solution** — i.e. a self-sourced, finite-amplitude object the LINEAR analysis misses. This is
  precisely "a finite-amplitude nonlinear self-trapped object linear analysis cannot see."
- **BUT (the de-rating, honest):** the scalarization effective mass is sourced by
  CURVATURE/COMPACTNESS (or by a matter source), not by a fixed dimensionful constant in the
  action. In **vacuum, scale-free** Branch G the large-negative-X limit DECOUPLES to GR + a free
  massless scalar (branch_G Sec 3, box phi -> 0, R -> 0 as 1/X), so the effective mass that
  scalarization needs has **no fixed scale to lock onto** — the curvature that would source it is
  itself scale-free. So the non-minimal coupling supplies a MECHANISM (effective mass) but, absent
  a dimensionful source, **not obviously a fixed SCALE**. Whether the nonlinear self-interaction
  (the e^{2phi} survivor in Branch P, an intrinsic-curvature source) supplies enough to lock a
  finite-amplitude time-periodic state is the EXACT open the nonlinear solve must decide. This is
  why Branch P (keep U), not Branch G, is the better first target (Sec 4).

### 2.3 The proper NUMERICAL method (recommendation)

Three method families in the corpus, with tradeoffs:

1. **MULTI-HARMONIC (Fourier-in-time) BALANCE solved as coupled radial ODEs/BVP — RECOMMENDED.**
   Standard oscillaton construction (Ureña-López; Alcubierre gr-qc/0310006; exponential-potential
   2511.02878): expand phi in COSINE harmonics at fundamental omega, the metric in EVEN harmonics
   (2omega, 4omega,...), substitute into Einstein-Klein-Gordon, set each Fourier coefficient to
   zero => a closed set of coupled radial ODEs; TRUNCATE at harmonic N and INCREASE N until
   converged ("2omega dominates, higher even harmonics decay rapidly"). Localization is selected
   by a **BVP: regularity at r=0 (phi'(0)=0) + asymptotic flatness (phi(inf)=0)**, SHOOTING on the
   eigenfrequency omega — only special omega give a non-dispersing periodic state. This maps
   DIRECTLY onto our re-posed JFNK + pseudo-arclength continuation (continue in amplitude/omega,
   shoot the eigen-omega). It is the proper minimum and the natural fit for our machinery.
   **Single-mode harmonic balance is the shortcut to AVOID** (the old MAP flagged this): the
   finite-amplitude object is ANHARMONIC; report harmonic-truncation convergence.
2. **1+1 TIME EVOLUTION (the heaviest) — reserve as CROSS-CHECK / persistence test.** Evolve EKG
   with the static/multi-harmonic solution as initial data; Fourier-transform the evolved field to
   read frequencies independently; watch whether the object PERSISTS or radiates/disperses over
   many periods. This is the unbiased self-trapped-vs-dispersing diagnostic (and the corpus's own
   verification of harmonic-balance solutions). Expensive; use it to CONFIRM a claimed bound object
   and to run the 3-cell persistence test, NOT as the primary constructor. (Honors the anti-hang
   rule: a bounded, low-resolution evolution as a check, not the production tool.)
3. **Periodic-in-time eigenvalue solve** — a variant of (1) posing the whole space-time-periodic
   system as one nonlinear eigenproblem in omega. Folds into the JFNK+arclength route; no separate
   build.

**Diagnostics the corpus uses for self-trapped-vs-dispersing / intrinsic-scale-vs-box:**
- localized BVP fall-off (phi -> 0 at infinity) with a FINITE mass-energy => candidate self-trapped;
- the object's size tracking the field's Compton scale (intrinsic) vs tracking the BOX size (artifact);
- evolution persistence over many periods (self-trapped) vs radiative spread (dispersing);
- (UDT-specific, our standing gate) **box-control: cell-scan + wall-relocation + intrinsic-lock** —
  any claimed omega/size that scales as 1/R or tracks the wall is a BOX artifact, not intrinsic.

---

## 3. THE HONEST EXPECTATION (anti-false-convergence, stated UP FRONT)

Everything so far points to **LIKELY DISPERSAL / BOX-CONTROL**:
- both static branches scale-free (verified);
- the linear time-live operator box-controlled, omega*R = 2.584 const (verified);
- the corpus default: **massless scalars disperse; the scale is the field's mass, which UDT-vacuum
  lacks**; the exponential nonlinearity alone does not self-trap (2511.02878 still needs m_Phi);
  periodic massless states need an external box (AdS) = our box-control artifact.

So the EXPECTED P5e outcome is to CONFIRM, with full nonlinear back-reaction on the DERIVED
operator, that UDT-vacuum **disperses / box-controls** — closing the last classical redoubt and
making "discreteness requires quantization" airtight on the derived (not hybrid) operator.

The GENUINE OPEN — the only reason to build this — is the **non-minimal-coupling effective-mass /
scalarization** channel (Sec 2.2): a finite-amplitude, self-sourced time-periodic configuration
that linear analysis structurally cannot see, where the e^{2phi}R coupling + the Branch-P intrinsic
curvature source conspire to lock a scale. The corpus says this mechanism EXISTS but typically
needs a dimensionful source; whether UDT's scale-free vacuum supplies enough is genuinely unknown
until solved. **We build to LEARN. Observe-not-target. DATA-BLIND. Either outcome is first-class**
(a clean box-control verdict closes the redoubt; a nonlinear self-trapped object would be the first
classical intrinsic scale and would reopen the classical-discreteness question — both are real).

---

## 4. PREMISE LEDGER (chose / derived) — incl. the TWO FOR CHARLES'S EYE

| # | choice | proper default | CHOSE / DERIVED | risk / guard |
|---|---|---|---|---|
| **Pr-branch** (FOR CHARLES) | Branch G (gauge U away) vs Branch P (keep U=e^{2phi}-1) for the FIRST time-live solve | **Branch P first** | CHOSE | see below — Branch P retains the only candidate scale-carrier (the intrinsic-curvature source); Branch G is provably scale-free in vacuum, so it is the NULL control, not the first hunt. |
| **Pr-X** (FOR CHARLES) | the X dial | **FIX X at one healthy value (e.g. X = -2e5, mid Cassini-safe half-line) for the existence question; SCAN only if existence is X-sensitive** | CHOSE | see below — existence of a self-trapped state is the binary; if it exists at one healthy X, scan to map the branch; if it depends delicately on X that is itself a finding. Do NOT use small/ghost X (forbidden by ghost+Cassini). |
| Pr-chart | areal vs isotropic for time-live | **isotropic (or horizon-penetrating) for the time-live solve** | CHOSE | areal is the static-exhibit chart; for a time-live oscillating metric an isotropic/conformal radial chart is the corpus standard (avoids areal-chart coordinate stiffness at oscillating throats). Cross-check the obstruction is chart-robust (weight-doc verifier did this for the static obstruction). |
| Pr-time | time treatment | **MULTI-harmonic balance (single-mode is the shortcut); evolution as cross-check** | CHOSE | report harmonic-truncation convergence; strongly anharmonic large-amplitude needs more modes. |
| Pr-amp | amplitude | **FINITE, continued from 0** | DERIVED-necessary | the whole point: the back-reaction is what linear analysis cannot see; an A->0 "result" is just the known box-controlled linear answer. |
| Pr-vac | scoping | **VACUUM FIRST (no matter field)** | CHOSE | the candidate scale-carrier is the gravity+phi vacuum sector (weight doc, both branch docs); matter is a later add ONLY if vacuum is scale-free. Do not smuggle a matter field to manufacture a scale. |
| Pr-omega | omega | **free / self-consistent eigen-omega** (shot, not scanned externally) | DERIVED-necessary | the object picks its own frequency; containment: omega->0 must return the static branch solution. |
| Pr-kernel | gravity operator | **the DERIVED e^{2phi}R + X e^{2phi}(dphi)^2 [ -2U ]** | DERIVED | NOT the old hybrid; NOT plain Einstein. The Choice-A fork is dissolved. Conditioning on the steep e^{2phi} core is the only A-residue (numerics, not physics). |
| Pr-box | box-control gate | any omega/size claimed intrinsic passes the 3-criteria gate | DERIVED-gate | THE standing trap; the AdS-massless precedent (Sec 2.1) shows a box can FAKE periodicity — cell-scan + wall-relocation + intrinsic-lock on EVERY claimed level. |
| Pr-conv | #60 convergence gate | a known-relax control floors on the same machinery | DERIVED-gate | if the control stalls, the result is SOLVER-LIMITED -> INCONCLUSIVE, not a null. |
| Pr-anchor | correctness reference | omega->0 = static branch (dense-LM); small-A = the box-controlled linear spectrum (omega*R=2.584) | DERIVED | the coupled solve must reproduce BOTH limits before finite-A results are trusted. |

### The TWO for YOUR eye, Charles

**(i) Branch G vs Branch P for the first solve.** RECOMMEND **Branch P first**. Reasoning (lay):
Branch G is the "throw the awkward angular-curvature term away" version — and we already PROVED
(branch_G doc, verified) it is completely scale-free in vacuum: a smooth massless scalar-tensor
family, no length anywhere. So a time-live Branch-G solve is the NULL CONTROL — useful to confirm
"yes, still no scale even with time on and full back-reaction," but it cannot be where a scale
hides, by construction. Branch P KEEPS the one term that could carry a scale (the intrinsic
angular curvature, the e^{2phi}-1 survivor). The static Branch-P analysis showed that term is a
scale-free *value*-pin when time is OFF — but the same doc + verifier flagged that the time
sector escapes the measure cancellation that neutered it statically. So Branch P with time LIVE is
the one place the hunch (phi-angular-time) could finally bite. **Run Branch P first (the real
hunt); run Branch G as the null control (cheap confirmation).** I am NOT steering toward Branch P
because it might give a scale — I am putting the only scale-CAPABLE branch first and labelling the
other a control, which is the honest ordering. Your call if you'd rather see the Branch-G null
first as a calibration.

**(ii) The X dial.** RECOMMEND **fix X at one healthy value (~ -2e5, comfortably inside the
ghost-free + Cassini-safe half-line X < -1.7e5) for the EXISTENCE question, then scan only if it
matters.** Reasoning (lay): the binary we care about is "does a self-trapped time-periodic object
EXIST at all in the healthy window?" That is a yes/no that one healthy X answers. If it exists, we
scan X to map how its scale/frequency move (and whether anything pins X). If existence turns out to
depend delicately on X, that delicacy is itself a finding (and a flag that we may be near the
decoupling limit where the scalar goes free). What I will NOT do silently is reach for a small or
ghost-side X to manufacture a bound state — that side is forbidden by ghost+Cassini and using it
would be exactly the "fix a value to make it solvable" scar. Your call if you'd rather scan X from
the start (more expensive, maps the whole branch) vs the cheaper fix-then-scan.

---

## 5. THE STAGED BUILD (each stage bounded + anchor-gated + verifiable; ANTI-HANG LOCKED)

Anti-hang is LOCKED throughout: **Nr <= 16/24, cap Newton/Krylov iters, SINGLE clean process,
dense-LM flooring on SAVED fields, NEVER background-poll.** Each stage validates against a known
answer before the next; a stage that cannot converge is reported **INCONCLUSIVE (solver-limited)**,
never a null.

- **P5e'-0 (cheap, build the derived kernel).** Codegen the DERIVED time-live residual for the
  scalar-tensor operator e^{2phi}R + X e^{2phi}(dphi)^2 [ -2U ] in the chosen time-live chart
  (Pr-chart), two-player (phi independent), with the box f and (g box - nabla nabla)f terms
  explicit. VALIDATE the kernel symbolically vs the branch-doc field equations (Sec 1.2) and vs a
  sympy recomputation. Instrument steep-core conditioning of the e^{2phi} weight (the only A-residue).
  *Anchor:* none yet (this is the build); the gate is symbolic-match to the derived equations.
- **P5e'-1 (anchor the static + linear limits).** With the new kernel, reproduce on the SAME
  machinery: (a) **omega->0 => the static branch solution** (Branch P relaxing value-pin / Branch G
  {m,q} hair) via dense-LM; (b) **small-amplitude => the box-controlled linear spectrum**
  (omega*R = 2.584, the verifier's number). BOTH anchors must pass before any finite-A result is
  trusted. *Gate:* dual-anchor reproduction.
- **P5e'-2 (converge the nonlinear branch).** Re-posed full-rank JFNK + pseudo-arclength
  CONTINUATION in amplitude, shooting the eigen-omega (multi-harmonic balance, harmonic order
  increased to convergence). #60 control gate: a known-relax control floors on this machinery; if
  it stalls => INCONCLUSIVE. KEH/SCF fallback if JFNK stalls (Principle 4). *Gate:* converged floor
  + control + harmonic-truncation convergence reported.
- **P5e'-3 (OBSERVE — Branch P first, then Branch G null).** Ramp amplitude finite. Does the
  coupled solve produce a **self-trapped time-periodic object with an INTRINSIC scale**
  (localized, phi->0 at infinity, finite mass-energy, scale tracking the field not the box), or
  does it **disperse / box-control** (omega~1/R, size tracks the wall)? **BOX-CONTROL GATE on ANY
  claimed intrinsic scale/level: cell-scan + wall-relocation + intrinsic-lock** (the AdS-massless
  precedent makes this non-negotiable). Run the Branch-G NULL CONTROL the same way. DATA-BLIND,
  observe-not-target. Report WHAT IS THERE with premises attached.
- **P5e'-4 (persistence cross-check).** For ANY claimed self-trapped object: a bounded 1+1
  EVOLUTION from the constructed initial data, **3-cell persistence test** (not 2-cell —
  look-elsewhere false positives), watching for radiative dispersal vs persistence over many
  periods. Unbiased kicks + NEB if a landscape claim is made (never blend toward a chosen endpoint).
- **P5e'-5 (verify).** Independent BLIND adversarial verifier, aimed HARDEST at any POSITIVE (a
  claimed bound object) and at the box-control / harmonic-truncation / dual-anchor / chart-robustness
  gates. Verifier-before-record; record agent id + date.

---

## 6. RISKS + THE HONEST CEILING

1. **Throughput wall (#60-class) — the feasibility risk.** The coupled nonlinear time-live free-omega
   solve on the DERIVED operator (now with box f and the steep e^{2phi} weight) may not reach a clean
   floor at usable resolution. Guard: the #60 control gate (stall = INCONCLUSIVE, not null); Principle-4
   GR-corpus contingency (KEH/SCF, multidomain spectral, the oscillaton harmonic-balance BVP machinery
   the corpus has already built). **Honest:** even built properly, P5e' MAY be throughput-limited — and
   THAT IS A REAL FINDING about the solver, not a null. An inconclusive verdict here is a legitimate
   stopping point (we would still hold the static scale-free branches + the linear box-control + a
   documented nonlinear-solver ceiling).
2. **Steep-core conditioning of the e^{2phi} weight.** The derived operator is stiff at deep core
   (large |phi|). The old hybrid existed precisely to dodge core stiffness; the derived operator must
   face it. Guard: Taylor-accurate function replacement through folds (allowed, [[taylor-expansion-allowed-not-linearization]]); honest deep-core treatment (no 0.05 cutoff smuggling the endpoint).
3. **Box-control trap faking a periodic state.** The AdS-massless precedent (Sec 2.1) is a direct
   warning: a confined massless scalar looks periodic because the BOX confines it. Guard: the
   box-control gate is mandatory on every claimed level; a periodic state that vanishes under
   wall-relocation is an artifact.
4. **Harmonic-truncation hiding structure.** Single/low-harmonic at large amplitude misses anharmonic
   structure. Guard: increase harmonic order to convergence; report what was dropped.
5. **Convergence-to-wrong-fixed-point.** A strong driver on a new operator lands on a spurious state.
   Guard: the dual anchor (static omega->0 + linear small-A box spectrum) before trusting finite-A.
6. **Observe-vs-target on Branch P.** Branch P was chosen first BECAUSE it is the scale-capable branch;
   the risk is wanting it to deliver. Guard: Branch G null control run identically; box-control gate;
   data-blind; verifier aimed hardest at any positive.

**THE HONEST CEILING.** This solve could be INCONCLUSIVE (throughput-limited) — that is a real finding,
not a null, and a legitimate stop. If it CONVERGES and disperses/box-controls (the expected outcome),
the last classical redoubt is closed on the DERIVED operator and "discreteness requires quantization"
is airtight. If it CONVERGES and finds a self-trapped intrinsic-scale object (the genuine open, via the
non-minimal scalarization channel), that is the first classical intrinsic scale and reopens the
classical-discreteness question — a major result demanding the hardest verification. We do not know
which; we build to find out.

---

## 7. SMUGGLED-FRAME CHECK

P5e' is squarely metric-led + solver-completeness: build the DERIVED operator's time-live solver
properly and OBSERVE. The Principle-7 hole the old BUILD MAP flagged ("vacuum = GR by construction")
is now CLOSED — the operator is derived and vacuum != GR — which is the single biggest reason this
re-point is worth doing: it answers the nonlinear-time-live question on UDT's OWN gravity operator,
not on an imported Einstein kernel. The honest residual: if throughput-limited, the airtight nonlinear
verdict stays open (we hold static-scale-free + linear-box-control + a documented ceiling) — an honest
stopping point, not a failure. Vacuum-first is the correct scoping (the candidate scale-carrier is the
gravity+phi vacuum sector); matter is a declared later add, never smuggled in to manufacture a scale.

---

## SOURCES (GR-corpus mine, Principle 4)
- Alcubierre, Becerril, Guzmán, Matos, Núñez, Ureña-López, *Classical and Quantum Decay of
  Oscillatons* — massive scalars form oscillatons, massless disperse: arXiv gr-qc/0310006.
- *A review on radiation of oscillons and oscillatons* — arXiv 1911.03340.
- Mahmoodzadeh, Ghaderi, Amiri, *Oscillatons ... from a Full Fourier Expansion of an Exponential
  Potential* — exponential potential still requires a mass scale V0=m^2/(lambda^2 k0); massless
  has no inherent length: arXiv 2511.02878.
- Maliborski, Rostworowski, *Time-Periodic Solutions in an Einstein AdS--Massless-Scalar-Field
  System* — massless periodic states need the AdS box (external scale): PRL 111, 051102 (arXiv 1303.3186).
- Spontaneous-scalarization corpus (non-minimal f(phi)R generates an effective mass; tachyonic when
  curvature drives m_eff^2<0; nonlinearity quenches into a nontrivial scalar config): arXiv 1903.10471
  (boson stars), 2211.01766 (review), 1003.4767.
- Boson-star numerical-method reviews (harmonic-balance vs evolution, SCF): arXiv 2106.01740,
  gr-qc/9906110; *Dynamical boson stars* (Living Review).
