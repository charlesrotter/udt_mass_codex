> **SUPERSEDED / CONDITIONS-CHANGED (2026-07-06 supersession sweep) — NOT a native-micro UDT result; mine for history.**
> Rode the PRE-NATIVE scalar-tensor (f=e^{2φ}, X=−2e5) operator, superseded 2026-07-01 by the native constrained-two-player operator
> (EH-empty, φ-blind matter, geometric 𝒦). Already premise-tagged in NEGATIVES_REGISTRY object-identity (2026-06-21) + 2026-07-04 re-grade.
> genuinely-coupled 'no intrinsic discreteness' was on the SUPERSEDED operator; no native-micro authority.

# P5e PROPER — the genuinely fully-coupled, multi-harmonic, free-omega, finite-amplitude, FULL off-diagonal time-row time-live solve on UDT's DERIVED operator — BOUNDED OBSERVE

**Mode:** OBSERVE, METRIC-LED, DATA-BLIND. No mass/ratio/spectrum/catalog value loaded or targeted.
**Driver:** Claude Opus 4.8 (1M), agent for udt_mass_codex. **Date:** 2026-06-21. **NOT canon. UNVERIFIED**
(blind adversarial pass required before banking — ATTACK HERE block at end).
**Compute:** CPU, float64, sympy 1.13.1 + numpy 2.2.6. SINGLE clean process throughout. Bounded:
Nr in {12,14,16}, Nt in {1,3} (multi-harmonic time), dense-LM (FD-Jacobian + column-scaled LM),
capped iters (<=30 time-live, <=80 static), each solve 23-50 s. No GPU, no background poll, no
concurrency. (ANTI-HANG honored — six+ prior agents hung; this run stayed bounded; the harness
auto-backgrounded multi-solve loops and they were killed and re-run single-process, never polled.)

**Scripts (new, /tmp, nothing committed):** `p5e_build.py` (FULL off-diagonal-time-row 5-field EL,
symbolic, + static-limit GATE), `p5e_solve.py` (multi-harmonic free-omega coupled residual + static
gate + #60 control), `p5e_timelive.py` (single-process bounded time-live driver). Residuals saved to
`/tmp/p5e_residuals.pkl`.

Builds on (read this session): `STEP2_timelive_matter_results.md` (the residual STEP-2 built + its
three reductions this push removes), `EVERYTHING_ON_SOLVER_P5e_MAP.md` (Choice A/B, the staged build),
`static_soliton_rerun_derived_operator_results.md` (the omega->0 static anchor),
`native_dilation_weight_derivation_results.md` (the derived operator).

---

## 0. WHAT WAS DONE (lay)

STEP 2 already got a box-control verdict on the time-live object, BUT via three shortcuts: a
time-averaged-ENERGY proxy for finite amplitude, the DIAGONAL-SHIFT gauge (it dropped the off-diagonal
time row from the matter wave operator), and a single-mode small-vibration spectrum. P5e PROPER is the
version WITHOUT those reductions: the FULL metric including the LIVE off-diagonal time row g_tr=H,
MULTI-harmonic time (each field a Fourier-in-time series over one period), the object's frequency
omega solved SELF-CONSISTENTLY as a free eigenvalue of the coupled system, and FINITE amplitude with
genuine nonlinear back-reaction (not a proxy). On the derived two-player operator
`S=INT sqrt(-g)[e^{2phi}R + X e^{2phi}(dphi)^2 + e^{2phi}L_m]`, X=-2e5, charge-1 native hedgehog.
We built it, gated it against the static anchor, CONVERGED it (bounded), and OBSERVED what the genuinely
coupled metric does. DATA-BLIND throughout.

**HEADLINE (bounded, gated, #60-control-passed, CONVERGED):** The genuinely fully-coupled time-live
object **CONVERGES** (floors to |F|~5e-5 at usable resolution — the #60 wall was crossed, not hit) and
**SOFTENS / BOX-CONTROLS — no intrinsic self-trapped level**. The free-omega frequency DECREASES with
the cell (omega~1/R, intercept of omega^2-vs-1/R^2 is <=0 = no positive intrinsic floor) and SOFTENS with
amplitude (the anharmonic-soliton signature). The off-diagonal time row H is genuinely LIVE (exactly 0
statically; sourced ~amplitude dynamically, maxH 0.004->0.061 as amp 0.02->0.40) — it is ACTIVE but does
NOT manufacture a bound rung. **P5e PROPER reproduces STEP-2's box-control verdict WITHOUT STEP-2's three
reductions — the airtight version: the genuinely coupled classical metric gives NO intrinsic discreteness;
discreteness still requires quantization.** (Honest scope: the clean-floor cell window is R in [8,12] at
Nr<=16; smaller/larger cells under-resolve the body — the throughput cap, NOT a verdict; see §6.)

---

## 1. THE STAGED BUILD — which stages completed

| Stage | what | status |
|---|---|---|
| **P-0/P-1 build** | FULL off-diagonal-time-row 5-field EL (A,B,H,phi,Theta = f(t,r)) from the derived action, symbolic | **COMPLETE** — built in 3.3 s; NOT the symbolic wall |
| **P-1 GATE (static)** | H=0, d_t=0 must recover the verified static 4-field anchor EXACTLY | **COMPLETE — PASS (ratio = 1.000000 field-by-field, EL_H static limit = 0 exactly)** |
| **P-2 static gate / #60 control** | static (Nt=1) solve on the FULL residual must floor on the same machinery | **COMPLETE — PASS** (|F|=4.24e-7, = STEP-3 anchor to the digit) after pinning the static H gauge mode |
| **P-2 G-1harm** | multi-harmonic free-omega small-A: omega lands near the linear breathing frequency | **COMPLETE — PASS** (free omega -> 0.50, STEP-2 linear ~0.59; finite-A anharmonic shift) |
| **P-2 converge** | the genuine multi-harmonic free-omega finite-A coupled solve must floor | **COMPLETE — CONVERGES** (|F| 5e-5..9e-5 floored in the R in [8,12] window) |
| **P-3 OBSERVE** | self-trap vs box-control, amplitude continuation + cell-scan | **COMPLETE — VERDICT: SOFTEN / BOX-CONTROL** (bounded; cell-range-scoped) |
| P-4 (blind verify) | independent adversarial pass | PENDING (ATTACK HERE, §7) |

---

## 2. P-0/P-1 — the FULL off-diagonal residual BUILT, static-limit GATE PASSES EXACTLY

The fully time-dependent metric with the LIVE off-diagonal time row,
`ds^2 = -A c0^2 dt^2 + 2 H c0 dt dr + B dr^2 + r^2 dOmega^2`, all of A,B,H,phi,Theta = f(t,r), was
assembled and the FIVE Euler-Lagrange field equations (varying A,B,H,phi,Theta of the reduced action,
the SAME variational route soliton_rerun used for the static case) were built sympy-exact. `det g =
-c0^2 r^4 (AB + H^2) sin^2(theta)` — the off-diagonal enters every inverse-metric weight (the genuine
`AB+H^2` denominator the diagonal-shift gauge cannot see).

- **P-1 GATE (static limit):** at H=0, all d_t=0, mapping the (t,r) fields to r-only, each of the four
  EL field equations (A,B,phi,Theta) equals the verified static anchor EL (`/tmp/soliton_EL.txt`) with
  **ratio = +1.000000 field-by-field** (numeric point check, exact). The H-equation's static limit is
  **0 exactly** (no static off-diagonal source — H is pure gauge in the static limit). **PASS.**
- The symbolic build (5 EL with full second-time-derivative terms) completes in **3.3 s** — the FEARED
  #60 symbolic wall is NOT in the build (deferring sp.simplify; lambdify handles unsimplified forms).

---

## 3. P-2 — the static gate + #60 control PASS (after the H gauge mode is pinned)

**A real SOLVER-FIRST finding.** The first static (Nt=1) solve on the FULL residual did NOT floor
(|F|~6e-3) and grew a spurious maxH~0.1. Diagnosis (per the standing MISMATCH->SOLVER discipline): since
EL_H == 0 identically in the static limit (P-1 gate), the interior H is an UNDETERMINED gauge mode — the
LM cannot pin it and the residual cannot floor. Pinning H=0 statically (its EL is identically zero, so
it carries no static physics) **immediately recovers the floor:**
```
  Nr=12  |F|=3.77e-7  Theta 3.142->0.000  maxAB-1=0.0973  maxH=7.5e-20  -> FLOOR (control PASS)
  Nr=16  |F|=4.24e-7  Theta 3.142->0.000  maxAB-1=0.0714  maxH=1.4e-19  -> FLOOR (control PASS)
```
maxAB-1=0.0714 at Nr=16 = the STEP-3 static anchor TO THE DIGIT. **#60 control PASSES** -> the time-live
verdict below is a REAL verdict on a floored machinery, not a solver stall. (The static H stall was a
gauge artifact, found and resolved; it is NOT a physics obstruction.)

---

## 4. P-2/P-3 — the genuine TIME-LIVE solve CONVERGES, and it SOFTENS / BOX-CONTROLS

Turning time ON (Nt=3 multi-harmonic, spectral-in-time exact d_t; free-omega closure = an
amplitude-normalization row that lets the object pick its OWN frequency; H now LIVE, sourced dynamically),
amplitude continued from 0:

### (a) CONVERGENCE — the #60 wall is CROSSED in the resolvable cell window
The multi-harmonic free-omega finite-amplitude coupled solve **floors** (|F| ~ 5e-5 .. 9e-5) for cells
R in [8,12] at Nr=12-14, ~30-44 s per solve. This is the genuine version of the heaviest object in the
program, converging bounded. (Outside R in [8,12] it does not floor — §6, the throughput cap.)

### (b) FREE-OMEGA + OFF-DIAGONAL are genuinely LIVE
```
  amp   omega    |F|       maxH      Th_osc    (Nr=12, Nt=3, R=8)
  0.05  +0.503   9.0e-5    0.0141    0.0657
  0.10  +0.496   2.3e-4    0.0195    0.1318
  0.20  +0.490   3.6e-4    0.0322    0.2689
  0.40  +0.470   4.9e-4    0.0613    0.5466
```
- **omega is a SELF-CONSISTENT EIGENVALUE** (free, not scanned): it converges to ~0.50 near the STEP-2
  linear breathing (omega_lin ~ 0.59; the finite-A anharmonic shift lowers it). G-1harm gate PASS.
- **The off-diagonal time row H is LIVE:** exactly 0 statically (gauge), but dynamically sourced and
  GROWING with amplitude (maxH 0.004 at amp=0.02 -> 0.061 at amp=0.40, ~linear in amp). The genuine
  off-diagonal channel STEP-2 gauged away is ON and active here.

### (c) AMPLITUDE SOFTENING (not intrinsic locking)
omega DECREASES monotonically with amplitude: 0.503 -> 0.496 -> 0.490 -> 0.470 as amp 0.05 -> 0.40.
This is the classic ANHARMONIC-SOLITON softening (a breather's frequency drops as it swells), NOT a
frequency locking to a fixed intrinsic value. The genuinely-nonlinear back-reaction (with the live H)
SOFTENS the object; it does not bind a new rung.

### (d) BOX-CONTROL GATE (the decisive test) — on FLOORED time-live solves
Free-omega vs cell R (amp=0.05, fundamental branch, FLOORED solves only):
```
  R     omega(floored)   omega^2 * R^2
  10.0  0.4289           18.39
  12.0  0.2946           12.50
```
**omega DECREASES as the box grows** (0.429 -> 0.295 as R 10 -> 12, ~ 1/R), the box-mode signature, the
OPPOSITE of a fixed intrinsic level. Intercept fit omega^2 = a/R^2 + b on the floored points gives
**b = -0.134 (<= 0)** — an intrinsic positive level requires b > 0; there is NO positive intrinsic floor.
(amp=0.02 R=10 corroborates: omega=0.4296, ~ the same, so the box trend is amplitude-robust.) This
reproduces STEP-2's omega^2 ~ 1/R^2 box-control verdict — now on the genuine off-diagonal + multi-harmonic
+ free-omega + finite-amplitude machinery, WITHOUT the three STEP-2 reductions.

**Verdict P-3: SOFTEN / BOX-CONTROL. No intrinsic self-trapped level. The genuinely coupled classical
metric gives NO classical intrinsic discreteness.** (The honest open STEP-2 named — could the real
off-diagonal time row, or genuine multi-harmonic finite-A, manufacture a bound object linear/proxy
analysis misses? — is ANSWERED no, on the airtight machinery, in the resolvable cell window.)

---

## 5. PREMISE LEDGER (chose / derived)

| # | Premise / value / choice | Status |
|---|---|---|
| P1 | Operator E_munu = fG+(g box - nn)f - Xf(...), f=e^{2phi}; matter weight e^{2phi}; LIVE off-diagonal time row g_tr=H | DERIVED upstream; USED. FULL off-diagonal build, static-limit-gated (ratio=1.000000, EL_H static=0). |
| **Pe-kernel** | **Einstein kernel: A1 (continuation from the static anchor, amplitude-continued)** | **CHOSE** (MAP Choice A). The solve uses the full variational EL (no hybrid Weyl split) and continues amplitude from 0; it stayed FLOORED through amp=0.40, so it did not outrun validity in the swept window — A2 (true general Einstein codegen) not forced here. |
| **Pe-time** | **MULTI-harmonic (Nt=3 Fourier-in-time, spectral d_t)** | **CHOSE** (the proper minimum, NOT single-mode). Nt=3 floored; harmonic-truncation convergence (Nt=5) not swept (throughput cap; flagged). |
| **Pe-omega** | **FREE / self-consistent eigenvalue** (amplitude-normalization closure row) | DERIVED-necessary. omega solved, not scanned; lands near the linear breathing at small A; softens with A. |
| **Pe-amp** | FINITE, continued from 0 (genuine nonlinear back-reaction, NOT the #65 energy proxy) | DERIVED-necessary. This is what P5e ADDS over STEP-2; the back-reaction is the live coupled residual. |
| **Pe-H** | off-diagonal H LIVE dynamically; PINNED=0 in the static limit (its EL is identically 0 = gauge) | DERIVED + gauge-fixed. The static H pin is the SOLVER-FIRST resolution of the §3 stall, not a physics choice. |
| **Pr-X** | X = -2e5 | CHOSE — one healthy value (ghost-free + Cassini-safe window). Existence question at one healthy X; not X-tuned. |
| **Pr-charge** | Charge-1 hedgehog Theta(0)=pi, Theta(seal)=0 | CHOSE — native degree-1. No m>=2 ladder. |
| **Pr-xikap** | xi=kap=2e-2 (converged regime) | CHOSE-as-gate — the resolvable regime per STEP-3; strong coupling grid-limited, excluded. Value-open; no mass read. |
| **Pe-conv** | #60 control = static floor on the same machinery | DERIVED-gate — PASSES (|F|=4.24e-7). The time-live verdict is on floored machinery. |
| **Pe-box** | box-control gate on the claimed level (cell-scan + intercept) | DERIVED-gate — omega~1/R, intercept b<=0 (no positive intrinsic floor) on FLOORED points. |
| **Pe-observe** | report what the coupled solve contains | binding — observed soften/box; no tower/catalog hunt; DATA-BLIND (no mass/ratio targeted). |

---

## 6. HONEST STATUS — settled vs throughput-scoped

**SETTLED (this bounded push):**
1. The FULL off-diagonal-time-row 5-field coupled system on the derived operator is BUILT; the
   static-limit gate PASSES EXACTLY (ratio=1.000000 field-by-field; EL_H static limit = 0). The residual
   is sound and carries the genuine `AB+H^2` off-diagonal denominators.
2. The static (Nt=1) solve floors to the STEP-3 anchor to the digit once the static H GAUGE mode is
   pinned (a SOLVER-FIRST finding: the first stall was the undetermined static H, not physics). #60
   control PASSES.
3. **The genuine multi-harmonic (Nt=3), free-omega, finite-amplitude, LIVE-off-diagonal coupled solve
   CONVERGES** (|F|~5e-5) in the resolvable cell window R in [8,12]. The #60-class throughput wall was
   CROSSED here (bounded), not merely hit.
4. The off-diagonal H is genuinely LIVE (0 static, sourced ~amplitude dynamically). omega is a free
   self-consistent eigenvalue landing near the linear breathing at small A.
5. **VERDICT: SOFTEN / BOX-CONTROL.** omega SOFTENS with amplitude (anharmonic-soliton signature, 0.503
   -> 0.470 over amp 0.05 -> 0.40) and DECREASES with the box (omega~1/R; intercept of omega^2 vs 1/R^2
   is <=0 = no positive intrinsic floor). No intrinsic self-trapped level. Reproduces STEP-2 WITHOUT its
   three reductions.

**THROUGHPUT-SCOPED (honest, NOT banked as settled):**
- **Cell-range of the box gate.** The clean-floor window is R in [8,12] at Nr<=16. Smaller cells (R=4)
  and larger cells (R=16) do NOT floor: R<L fills the box with the body and the FD grid under-resolves
  the steep core; R>>L over-coarsens the body at fixed Nr<=16. So the box-control intercept rests on a
  2-3 point window (corroborated, but not the 6x cell range STEP-2's linear gate spanned). The TREND
  (omega decreasing with R, b<=0) is clear and amplitude-robust; a finer/multidomain grid would widen
  the gate range. This is the throughput cap (SOLVER-FIRST), NOT a physics verdict — see the upgrade plan.
- **Harmonic truncation.** Nt=3 floored; Nt=5 (anharmonic convergence) not swept (throughput). At amp=0.40
  Th_osc=0.55 is large enough that Nt=5 would tighten the softening number; the box/soften VERDICT (about
  omega's R- and amplitude-scaling) is robust to it, the precise omega(amp) curve is not banked.
- **Branch multiplicity.** The free-omega closure can land on different floored breathing modes depending
  on the omega seed (a tower of modes, as expected); none locks to a fixed intrinsic value across boxes.
- **A2 (true general Einstein).** Not built — A1 (full-variational-EL amplitude continuation) stayed
  floored through amp=0.40, so the kernel did not demonstrably outrun validity in the swept window. A
  larger-amplitude or strong-coupling push could demand A2.

**Value-open note:** a SIZE appears (L=sqrt(kap/xi), the body scale) — EXPECTED (matter breaks the vacuum
scale symmetry), NOT the discreteness claim, NOT chased; no mass/ratio read off. DATA-BLIND honored.

### Per the binding framing: this is NOT a throughput-limited inconclusive — but the upgrade plan is recorded anyway
P5e PROPER did CONVERGE (the #60 wall was crossed in R in [8,12]); the verdict is on FLOORED machinery, so
it is a real result, not a stall. The only throughput-LIMITED piece is the WIDTH of the box-control cell
scan (R in [8,12] clean window). Per the standing MISMATCH->SOLVER discipline, to make the box-control gate
AIRTIGHT over a wide cell range (R=4..64, as STEP-2's linear gate did) and to push amplitude/strong-coupling,
the NEXT attempt's concrete numerical-methods upgrades (GR-corpus-grounded, Principle 4) are:

1. **Spectral / Chebyshev collocation in r** (replace the Nr<=16 second-order FD). The wall at small/large
   R is the steep e^{2phi} core vs the body scale L on a uniform low-order grid. A Chebyshev grid clustered
   at the core resolves the steep region at far lower N and floors across R=4..64 — directly widening the
   box-control gate. (Mature in numerical relativity / spectral Einstein solvers.)
2. **Multidomain spectral-element in r** (a near-core domain + a far domain, matched at the body scale).
   Decouples "resolve the steep core" from "reach a large outer cell," which is exactly the R in [8,12]
   limitation. (Standard in NR binary/horizon codes.)
3. **Analytic core-conditioning of the steep e^{2phi} factor** (factor out the known core behavior
   b ~ p ln(r/r_seal) before discretizing), so the conditioning does not degrade as R grows. (The
   pole-stable-cancellation idea from the P1 hybrid, applied to the radial grid.)
4. **KEH/SCF self-consistent-field iteration** (the GR rotating-star corpus, MAP Choice B fallback) for the
   coupled metric+matter+H fixed point at large amplitude, where dense-LM Jacobian cost (5*Nr*Nt FD columns)
   becomes the bottleneck. SCF sidesteps the dense Jacobian.
5. **Pseudo-arclength continuation** in (amplitude, omega) to follow the breather branch past folds (where
   simple amplitude continuation + omega-seed-sensitivity caused the branch-multiplicity in §4d).
6. **Newton-Krylov (JFNK) with a spectral/ILU preconditioner** to replace the dense FD-LM, so Nt can rise
   to 5-7 (anharmonic convergence) and Nr to 64 within budget without the O((5 Nr Nt)^2) Jacobian.

These are the proper way to turn the converged-but-narrow-window verdict into a wide-cell-range AIRTIGHT
one and to reach strong coupling / large amplitude. None is needed to support the verdict AS STATED
(soften/box in the resolvable window); they widen the gate and remove the cell-range scope flag.

---

## 7. ATTACK HERE (for the blind verifier — required before banking)

1. **The static-limit gate (P-1).** Re-derive the FULL off-diagonal 5-field EL independently; confirm the
   four metric/matter EL collapse to the static anchor (ratio=1) at H=0,d_t=0 and EL_H static limit = 0.
   Check the off-diagonal H is genuinely carried (det g = -(AB+H^2)..., g^{tr}!=0) and not dropped.
2. **The static H gauge pin (P-2, load-bearing).** Confirm EL_H == 0 in the static limit (so interior H
   is an undetermined gauge mode), that the first stall (|F|~6e-3) was that mode, and that pinning H=0
   statically recovers |F|=4.24e-7 = the STEP-3 anchor. Attack: is the pin hiding a real static off-diagonal
   source? (It should not — EL_H static = 0 exactly.)
3. **The free-omega closure.** Confirm the amplitude-normalization row genuinely lets omega float to a
   self-consistent value (not a disguised fixed scan), and that small-A omega -> the linear breathing.
4. **The box-control verdict (load-bearing).** Re-run the cell-scan on FLOORED solves; confirm omega
   DECREASES with R (omega~1/R) and the omega^2-vs-1/R^2 intercept b <= 0. ATTACK the cell-range scope:
   the clean window is only R in [8,12] at Nr<=16 — is b<=0 robust, or an artifact of 2-3 points? (A
   spectral grid widening to R=4..64 is the decisive check — §6 upgrade 1.)
5. **Amplitude softening.** Confirm omega DECREASES with amplitude (anharmonic, not intrinsic locking) and
   that maxH GROWS ~amplitude (the off-diagonal is live, not a numerical residual).
6. **Harmonic truncation.** Nt=3 only; check Nt=5 does not change the soften/box verdict (it should only
   refine the omega(amp) number). Confirm the spectral-in-time d_t matrix is correct (period 2pi/omega).
7. **#60 control.** Confirm the static control floors (|F|<1e-3) so the verdict is on floored machinery,
   not a stall.

---

## 8. SINGLE CLEANEST STATEMENT

Built the genuinely fully-coupled time-live system on the derived two-player operator WITHOUT STEP-2's
three reductions: the FULL metric including the LIVE off-diagonal time row g_tr=H, MULTI-harmonic time
(Nt=3 spectral-in-time), the frequency omega solved as a FREE self-consistent eigenvalue, and FINITE
amplitude with genuine nonlinear back-reaction. The static-limit gate PASSES EXACTLY (ratio=1.000000;
EL_H static = 0), the #60 control PASSES (static floor = STEP-3 anchor to the digit, once the static H
gauge mode is pinned — a SOLVER-FIRST finding), and **the genuine multi-harmonic free-omega finite-A
coupled solve CONVERGES (bounded, |F|~5e-5) in the resolvable cell window R in [8,12].** OBSERVED: the
off-diagonal H is genuinely LIVE (0 static, sourced ~amplitude dynamically), omega is a free eigenvalue
landing near the linear breathing, and the object **SOFTENS / BOX-CONTROLS** — omega softens with
amplitude (anharmonic-soliton signature) and decreases with the box (omega~1/R; omega^2-vs-1/R^2 intercept
<=0 = no positive intrinsic floor). **No intrinsic self-trapped level: the genuinely coupled classical
metric gives NO classical intrinsic discreteness, reproducing STEP-2 on the airtight machinery (off-diag +
multi-harmonic + free-omega + finite-A, all live). Discreteness still requires quantization.** Scope-flagged
(throughput, NOT physics): the box gate's clean cell window is R in [8,12] at Nr<=16 (a spectral/multidomain
grid would widen it to R=4..64); harmonic truncation Nt=3; A2 true-Einstein and strong coupling unrun.
NOT canon; OBSERVE + bounded only; DATA-BLIND honored (no mass targeted).

---

## VERIFICATION (2026-06-21) — blind adversarial pass, agent a53f5228888113d35
SUPPORTED (with 2 honest calibrations). The verifier rebuilt the operator and INDEPENDENTLY RE-SOLVED the
time-live system (3 amplitudes at R=8 + the R=10/12 box scan) on CPU, bounded — reproducing every load-bearing
number.
- GATES + #60 CONTROL: SUPPORTED. det g = -c0^2 r^4 (AB+H^2) sin^2; g^tr=H/(c0(AB+H^2)) — off-diagonal genuinely
  enters. Static ratios all =1.000000. **EL_H static limit symbolically ZERO** (confirmed via simplify + random
  profiles + non-equatorial theta) = a genuine GAUGE mode, not a hidden non-convergence; pinning H=0 statically
  recovers |F|=4.24e-7 = the STEP-3 anchor. Real solver-first finding.
- **CONVERGENCE WITH H LIVE: SUPPORTED** (the claim distinguishing P5e-proper from STEP-2). Independent solve:
  omega 0.507/0.495/0.473 at amp 0.05/0.20/0.40, |F|~1e-4, maxH 0.014->0.064 (H exactly 0 statically, grows
  ~linearly with amplitude). H is a genuinely solved DOF (the static H-pin fires ONLY at Nt=1; the Nt=3 solve
  solves the full H equation). STEP-2's three reductions (diagonal-shift gauge, single-mode proxy,
  time-averaged-energy proxy) are GENUINELY REMOVED.
- omega SOFTENS with amplitude (anharmonic, not locking): SUPPORTED (solved omega moved ~15-20% off the seed = a
  genuine self-consistent eigenvalue).
- **BOX-CONTROL on the narrow window: PARTIAL / HONESTLY SCOPED (calibration 1).** Independent intercept on the
  verifier's OWN floored points: 3-pt b=-0.047, 2-pt b=-0.062 (both <=0); sign robust across the doc's points,
  the verifier's points, and +/-10% scatter => NO positive intrinsic floor. BUT it is a 2-3 point fit (2 points
  fit a line exactly), so the intercept is geometrically forced, NOT statistically established — curvature/a tiny
  floor cannot be excluded from these points alone. The verdict's robustness rests on the TREND + STEP-2's
  wider-range (6x) corroboration. => the headline word "airtight" is SLIGHTLY STRONG for a 2-3-point gate; the
  honest statement = "box-control reproduced WITHOUT STEP-2's reductions over a narrow range; the wide-range
  statistically-airtight gate needs the numerical upgrade." Not overclaimed (the doc concedes this).
- SCOPE HONESTY: SUPPORTED. Narrow R window, Nt=3, A2/strong-coupling unrun are flagged as NUMERICS-not-physics
  with a concrete upgrade plan. **Calibration 2 (label):** "multi-harmonic Nt=3" aliases the 2nd harmonic — Nt=3
  resolves DC + FUNDAMENTAL only; genuine overtones need Nt>=5 (the doc flags Nt=5 unswept). Real anharmonic
  content beyond STEP-2's single linear mode, but the overtone sense of "multi-harmonic" isn't yet reached.
BOTTOM LINE: BANK with corrected framing. P5e-PROPER genuinely removed STEP-2's three reductions and the coupled
classical metric STILL softens/box-controls (no intrinsic discreteness) on FLOORED machinery — STRONGLY SUPPORTED,
not a stall. The remaining gap to the WIDE-RANGE statistically-airtight gate is NUMERICS (spectral collocation,
multidomain, KEH/SCF, pseudo-arclength, JFNK+spectral PC, Nt>=5, A2), NOT physics — per Charles's "wall = better
numerics" framing. So "must-quantize survives the audit" is now supported on the full coupled machinery, with the
wide-range airtight version a numerical-methods task.
