> **SUPERSEDED / CONDITIONS-CHANGED (2026-07-06 supersession sweep) — NOT a native-micro UDT result; mine for history.**
> Rode the PRE-NATIVE scalar-tensor (f=e^{2φ}, X=−2e5) operator, superseded 2026-07-01 by the native constrained-two-player operator
> (EH-empty, φ-blind matter, geometric 𝒦). Already premise-tagged in NEGATIVES_REGISTRY object-identity (2026-06-21) + 2026-07-04 re-grade.
> box-control / must-quantize was demonstrated on the SUPERSEDED operator; no authority as native-micro.

# STEP 2 — TIME-LIVE COUPLED NATIVE-MATTER SOLVE on UDT's DERIVED operator — BOUNDED OBSERVE

**Mode:** OBSERVE, METRIC-LED, DATA-BLIND. No mass/ratio/spectrum/catalog value loaded or targeted.
**Driver:** Claude Opus 4.8 (1M), agent for udt_mass_codex. **Date:** 2026-06-21. **NOT canon. UNVERIFIED**
(blind adversarial pass required before banking — ATTACK HERE block at end).
**Compute:** CPU, float64, sympy 1.13.1 + numpy 2.2.6. Single clean process. Bounded: Nr in {16,24,32,40,48,60,64},
dense-LM (FD-Jacobian + column-scaled LM) static anchor, self-adjoint Sturm-Liouville standing-wave
eigenproblem, capped iters (<=80), each solve seconds. No GPU, no background poll, no concurrency.
(ANTI-HANG honored — six+ prior agents hung; this run stayed bounded throughout.)

**Scripts (new, /tmp, nothing committed):** `step2_s20_build.py` (time-live metric operator + static-limit
Ricci gate), `step2_matter_tl.py` (time-live matter EL with live e^{2phi} weight + static-limit gate),
`step2_solve.py` (GATE A static anchor), `step2_spectrum.py` (self-adjoint standing-wave spectrum +
box-control cell-scan), `step2_boxgate.py` (box-control gate + negative-mode diagnosis + action-fragility),
`step2_finiteamp.py` (finite-amplitude back-reaction + #60 control gate). Time-live matter EL in
`/tmp/step2_ELtl.txt`.

Builds on (read this session): `STEP2_timelive_matter_MAP.md` (the plan executed),
`static_soliton_rerun_derived_operator_results.md` (STEP 3, the omega->0 anchor + static solver),
`coupled_timelive_solve_results.md` (#65, the OLD-operator time-live precedent — its box-control machinery reused),
`native_dilation_weight_derivation_results.md` / `matter_regrade_derived_operator_results.md` (operator + weight).

---

## 0. WHAT WAS DONE (lay)

The static charge-1 soliton (STEP 3) showed the new operator changes the STATIC profile only modestly and
NAMED the time-live coupled solve as where its teeth might bite. STEP 2 turns time ON: it builds the
fully time-dependent coupled system (metric A,B + the live time-row off-diagonal + the depth field phi +
the native matter field Theta, all functions of (t,r)), with the matter riding the derived e^{2phi} weight,
and ASKS: when the object is allowed to breathe/oscillate at finite amplitude, does it lock into a
self-trapped state with an INTRINSIC scale (a real, discrete, box-independent level) — or does it stay a
CONTINUUM whose "levels" are just the cell wall (omega ~ 1/R)? Built in stages, each anchor-gated and
bounded; observed what is there; applied the mandatory box-control gate. DATA-BLIND throughout.

**HEADLINE (bounded, grid-converged, #60-control-passed):** On the DERIVED operator WITH the now-physical
matter coupling, the time-live coupled object is **BOX-CONTROLLED — a continuum, no intrinsic discrete level**,
exactly as the OLD-operator #65 found. The standing-wave tower scales as omega^2 ~ 1/R^2 (the cell wall);
finite amplitude does NOT open a new bound level; the only non-continuum feature is a SINGLE negative mode
= the static soliton's Derrick/dilatation breathing instability, which itself disperses to zero with the
box and is not L4-specific. **The last classical redoubt closes the same way on the derived operator: no
classical intrinsic discreteness; discreteness still requires quantization.**

---

## 1. THE STAGED BUILD — which stages completed

| Stage | what | status |
|---|---|---|
| **S2-0** | time-live 5-field residual built symbolically (metric incl. live time-row off-diagonal g_tr=H, phi(t,r), Theta(t,r); the live e^{2phi} matter weight) | **COMPLETE** — both static-limit gates PASS |
| **S2-1 / GATE A** | omega->0 must recover the STEP-3 static soliton | **COMPLETE — PASS** |
| **S2-1 / GATE B** | small-amplitude => the linear standing-wave spectrum | **COMPLETE** — spectrum built, self-adjoint, grid-converged |
| **S2-2** | nonlinear finite-amplitude coupled solve + #60 control gate | **COMPLETE (bounded)** — #60 control PASSES (real verdict); finite-A back-reaction via #65-style harmonic-balance proxy (flagged, see §5) |
| **S2-3 / OBSERVE** | self-trap vs box-control, with the mandatory box-control gate | **COMPLETE — VERDICT: BOX-CONTROL** |
| S2-4 (persistence evolution) | 3-cell evolution persistence | NOT RUN (gated on a positive; verdict was box-control, so not triggered) |
| S2-5 (blind verify) | independent adversarial pass | PENDING (ATTACK HERE, §8) |

---

## 2. S2-0 — the time-live operator BUILT, static-limit gates PASS

The fully time-dependent metric with the live time-row off-diagonal was assembled
(`ds^2 = -A c0^2 dt^2 + 2 H c0 dt dr + B dr^2 + r^2 dOmega^2`, all of A,B,H,phi,Theta = f(t,r)),
its Ricci scalar + the covariant scalar-tensor operator + the time-live matter EL built sympy-exact.

- **S2-0a GATE (Ricci static-limit):** `Rsc(time-live)|_{H=0, d_t=0} - Rsc(static) == 0` **exactly** (sympy).
  The time-live curvature collapses to the static Ricci with zero residual. **PASS.**
- **S2-0b GATE (matter EL static-limit):** the time-live Theta EL with the live e^{2phi} weight, taken at
  `d_t Theta=0`, equals the STEP-3 static matter EL **exactly** (sympy, zero difference). **PASS.**

The deepening is confirmed structurally: the time-live kinetic invariant
`X_k = [c0^2 A Th_r^2 + 2 c0 H Th_r Th_t - B Th_t^2] / [c0^2 (AB + H^2)]` carries the time-kinetic term with
`g^{tt}` (opposite metric weight to `g^{rr}`) — the second, dynamical scale-symmetry channel the static
analysis cannot see. It is built and live in the EL.

---

## 3. GATE A (omega->0 anchor) — PASS

The static limit on the SAME machinery reproduces the STEP-3 static charge-1 soliton:
```
xi=kap=2e-2 (converged regime), X=-2e5:  |F|=4.2e-7
  Theta core->seal: 3.142 -> 0.000  (clean charge-1, pi->0)
  max|A*B-1| = 7.14e-2  (B=1/A break peaking at core — the matter-kinetic break, operator-independent)
  phi range [-8.6e-7, 6.0e-7]  (tiny 1/r hair at the Cassini-safe X)
  sin^2(Theta) peak at r=1.11  (localized body, L=sqrt(kap/xi))
```
This matches STEP-3's verified static structure (localized charge-1, tiny hair, core B=1/A break ~0.07 at
this coupling) to the digit. **GATE A PASS — the time-live residual reduces correctly to the static soliton.**

---

## 4. GATE B + S2-3 OBSERVE — the standing-wave spectrum is BOX-CONTROLLED

The small-amplitude standing-wave spectrum was built as a SELF-ADJOINT Sturm-Liouville problem from the
quadratic action (`omega^2 m u = -(k u')' + V u`, Dirichlet both ends), with the mass density
`m = sqrt(AB) r^2 e^{2phi}(xi+2kap Y)/A` carrying the LIVE e^{2phi} weight and the `g^{tt}` time factor —
the genuinely new-operator ingredient vs #65.

### Grid-converged spectrum (R=8 cell, xi=kap=2e-2):
```
  Nr= 32: w_pos_low=0.35368  w_neg=[-0.25721]
  Nr= 40: w_pos_low=0.35336  w_neg=[-0.25217]
  Nr= 48: w_pos_low=0.35302  w_neg=[-0.25137]
  Nr= 64: w_pos_low=0.35443  w_neg=[-0.25242]
```
Grid-stable to ~0.4% (positive) — a real spectrum, not under-resolution.

### BOX-CONTROL GATE (the decisive test) — lowest POSITIVE mode vs cell R:
```
  R     w_pos_low      w_pos_low * R^2
  4.0   1.763e+00      28.21
  6.0   6.769e-01      24.37
  8.0   3.530e-01      22.59
 12.0   1.483e-01      21.35
 16.0   7.826e-02      20.03
 24.0   5.394e-02      31.07
  -> w_pos_low spread: 0.054 .. 1.763  (33x — NOT constant => NOT intrinsic)
  -> w_pos_low * R^2 :  ~20-31 (roughly constant => 1/R^2 BOX MODE)
```
**The lowest positive level scales as omega^2 ~ 1/R^2 — it is the CELL WALL, not an intrinsic level.**
Box-control criterion 1 (no 1/R scaling): **FAIL** (it DOES scale ~1/R^2). Criterion 2 (wall-relocation):
**FAIL** (the level moves by far more than a few % when the seal is relocated). This is the same signature
the scale-symmetry analysis predicted (box-control = the dilatation fingerprint) and #65 found on the old
operator. **The positive standing-wave tower is a BOX-CONTROLLED CONTINUUM.**

### The single NEGATIVE mode = the Derrick/dilatation breathing instability (NOT a discrete level)
Exactly ONE negative mode at every cell size, and its magnitude vanishes as the box grows:
```
  R= 4.0: n_neg=1  w_neg=-0.287
  R= 8.0: n_neg=1  w_neg=-0.251
  R=16.0: n_neg=1  w_neg=-0.131
  R=32.0: n_neg=1  w_neg=-0.00069   (-> 0 with the box)
```
One negative mode that disperses to zero with R is the static soliton's SCALING/breathing direction
(the classic Derrick instability of a static field-theory soliton), NOT a bound spectral LEVEL. It is a
property of the static lump, expected, and it too is box-sensitive. It does NOT multiply (always n_neg=1).

---

## 5. S2-2/S2-3 finite amplitude — #60 control PASSES, finite-A does NOT open a level (still box-controlled)

The #60 convergence-control gate PASSES (the static control floors to |F|=1.4e-5), so the box-control
verdict is a REAL verdict, NOT a solver stall. The finite-amplitude back-reaction (the genuinely nonlinear
ingredient) was run #65-style: the time-averaged mode kinetic energy injected self-consistently into the
(t,t) source, background + metric + phi re-solved, the standing-wave recomputed on the back-reacted field.
```
  amp | lowest_pos w^2 | n_neg | max|AB-1|
  0.0 |   0.35336      |   1   |   0.090
  0.5 |   0.37769      |   1   |   0.046
  1.0 |   0.37700      |   1   |   0.054
  2.0 |   0.37852      |   1   |   0.079
  4.0 |   0.37328      |   1   |   0.150
```
Finite amplitude does NOT raise the lowest positive level into a discrete bound state, and n_neg stays
exactly 1. Box-control on the a=2 finite-amplitude level:
```
  R= 4.0 | w=1.724e+00 | w*R^2=27.6
  R= 8.0 | w=3.785e-01 | w*R^2=24.2
  R=16.0 | w=7.952e-02 | w*R^2=20.4   (still ~1/R^2 box-controlled)
```
**The finite-amplitude coupled level is STILL box-controlled.** This reproduces #65's verdict on the
DERIVED operator: the back-reaction is active but does NOT manufacture a new bound rung. (HONEST SCOPE
FLAG, §5-proxy: the finite-A back-reaction here uses the #65 time-averaged-energy harmonic-balance proxy,
NOT a full multi-harmonic free-omega PDE; |F| degrades at large amplitude as the injected energy strains
the coarse grid. The box-control verdict — about omega^2's R-scaling — is robust to the proxy and to the
grid, but the precise finite-A back-reaction direction (#65 saw softening-to-tachyon; here it is roughly
flat) is proxy-dependent and is NOT banked. What IS banked: no intrinsic level appears, box-control holds.)

---

## 6. ACTION-FRAGILITY CHECK (Pr-action: {L2,L4} minimal-not-unique)

Scanning the L4 coefficient kap with the L2 coefficient xi fixed:
```
  kap=0    : n_neg=1  lowest3=[-0.0063, 0.4987, 1.321 ]   (L2 only: still 1 neg + box tower)
  kap=1e-2 : n_neg=1  lowest3=[-0.446 , 0.337 , 1.027 ]
  kap=2e-2 : n_neg=1  lowest3=[-0.251 , 0.353 , 1.075 ]
  kap=4e-2 : n_neg=1  lowest3=[-0.132 , 0.387 , 1.163 ]
```
The qualitative structure — ONE negative (Derrick) mode + a box-controlled positive tower — is present
even at kap=0 (L2-only) and unchanged in character across the L4 weight. **No self-trapped object appears
that DEPENDS on the L4-vs-X^2 matter-term choice** (the F2 fragility worry). The box-control verdict is
action-robust: it is not a feature of one non-unique term. (There is nothing to bank AS a positive, so
action-fragility cannot corrupt a positive — the verdict is a clean negative either way.)

---

## 7. PREMISE LEDGER (chose / derived)

| # | Premise / value / choice | Status |
|---|---|---|
| P1 | Operator E_munu = fG+(g box - nn)f - Xf(...), f=e^{2phi}; matter weight e^{2phi}; live time-row g_tr | DERIVED upstream; USED. Time-live build static-limit-gated (both gates exact). |
| **Pr-X** | **X = -2e5** (fixed) | **CHOSE** — one healthy value in the ghost-free + Cassini-safe window (per MAP Pr-X). Existence question answered at one healthy X; not X-tuned to manufacture a state. |
| **Pr-charge** | **Charge-1 hedgehog Theta(0)=pi, Theta(seal)=0** | **CHOSE** — native degree-1 (per MAP Pr-charge). No m>=2 winding ladder built. |
| **Pr-action** | **{L2, L4}** | **CHOSE-minimal** (F2: minimal-not-unique). Checked for fragility (§6): verdict action-robust, nothing fragile to bank. |
| Pr-amp | FINITE, continued from 0 | DERIVED-necessary. Finite-A run (§5); box-control holds at finite A. |
| Pr-harm | single-fundamental harmonic-balance + time-averaged back-reaction | CHOSE (#65 proxy). FLAGGED scope cost: not full multi-harmonic free-omega PDE (§5). Verdict (box-control) robust to it. |
| Pr-B | B=1/A FREE | DERIVED-necessary. Free + measured; break ~0.07-0.15 at core (matter-kinetic, operator-independent). |
| Pr-xikap | xi=kap=2e-2 (converged regime) | CHOSE-as-gate — the resolvable regime per STEP-3 (strong coupling xi=kap~1 is grid-limited, excluded). Value-open; no mass read. |
| Pr-chart | areal static-limit chart; live time-row built symbolically | CHOSE (CANON slice). The wave operator uses the diagonal-shift gauge at leading order; the off-diagonal g_tr is built and live in the metric EL. |
| D1 | time-live 5-field operator + matter EL | DERIVED (sympy-exact, both static-limit gates PASS) |
| D2 | self-adjoint standing-wave SL spectrum, grid-converged | DERIVED (Nr=32..64 stable to 0.4%) |
| D3 | box-control: w^2 ~ 1/R^2 (positive tower), single Derrick negative mode -> 0 with box | DERIVED (cell-scan + grid-convergence) |

---

## 8. HONEST STATUS — settled vs scope-flagged

**SETTLED (this bounded push):**
1. The time-live 5-field coupled system on the derived operator is BUILT; both static-limit gates PASS
   (Ricci + matter EL collapse exactly to the static system). The residual is sound.
2. GATE A: omega->0 recovers the STEP-3 static soliton exactly (localized charge-1, tiny hair, core
   B=1/A break). The anchor holds.
3. The small-amplitude standing-wave spectrum is grid-converged (Nr 32-64, 0.4%) — a real spectrum.
4. **S2-3 VERDICT = BOX-CONTROL.** The positive standing-wave tower scales omega^2 ~ 1/R^2 (the cell wall,
   33x variation in omega^2 across a 6x cell range; omega^2*R^2 roughly constant). No intrinsic discrete
   level survives the box-control gate. The single negative mode is the Derrick/dilatation breathing
   instability of the static lump (n_neg=1 at all R; disperses to zero with the box; present at kap=0).
5. #60 control gate PASSES => the box-control is a REAL VERDICT, not a solver stall.
6. Finite amplitude does NOT open a new bound level; the finite-A lowest level is still box-controlled.
7. Action-robust: the box-control verdict holds across the L4 weight (including kap=0); nothing fragile.

**SCOPE-FLAGGED (honest, NOT banked as settled):**
- The finite-amplitude back-reaction uses the #65 time-averaged-energy harmonic-balance PROXY, not a full
  multi-harmonic free-omega PDE solve (the program's heaviest object, deliberately not attempted unbounded
  per anti-hang). The box-control VERDICT is robust to this; the precise finite-A back-reaction direction
  is proxy-dependent and NOT banked.
- Strong coupling (xi=kap~1) is grid-limited on Nr<=24 (per STEP-3); the converged regime (xi=kap<=2e-2)
  is where structure is read. A research-grade driver could read the strong-field object, but the
  box-control signature (the symmetry fingerprint) is not expected to change with resolution.
- The live time-row off-diagonal g_tr is built symbolically and present in the metric EL, but the
  standing-wave eigenproblem uses the leading diagonal-shift gauge; a full off-diagonal time-row coupled
  PDE solve is the unbounded object not attempted here.

**Value-open note:** a SIZE appears (L=sqrt(kap/xi), the body scale) — EXPECTED (matter breaks the vacuum
scale symmetry) and NOT the discreteness claim, NOT chased; no mass/ratio read off. DATA-BLIND honored.

---

## 9. WHAT THIS MEANS (the deliverable)

STEP 2 closes the last classical redoubt the MAP named. The genuine open was: the derived operator's teeth
are in DYNAMICS (STEP 3's headline), and the now-physical matter coupling (the exchange law, no relabeling
to GR) is the new ingredient vs #65 — MIGHT the nonlinear matter+time+new-operator coupling lock a
self-trapped intrinsic-scale object that linear analysis misses? **Answer (bounded, grid-converged,
control-passed): NO. It box-controls, same as the old operator.** The new operator changes the static
profile modestly and, even with time live and matter coupled at finite amplitude, does NOT manufacture a
classical intrinsic discrete level. This makes "discreteness requires quantization" airtight on the DERIVED
operator WITH physical matter — the expected outcome, now demonstrated rather than assumed. (A self-trapped
intrinsic level would have reopened the quantization question; it did not appear.)

---

## 10. ATTACK HERE (for the blind verifier — required before banking)

1. **The static-limit gates (S2-0).** Re-derive the time-live Ricci and matter EL independently; confirm
   both collapse to the static system with ZERO residual at H=0, d_t=0. A bug here would invalidate the
   whole time-live claim. (Check the off-diagonal g_tr=H term is genuinely carried, not dropped.)
2. **GATE A.** Confirm omega->0 reproduces the STEP-3 static soliton (pi->0, max|AB-1|~0.07, tiny hair) on
   the SAME machinery — not a re-seeded different object.
3. **The box-control verdict (load-bearing).** Re-run the cell-scan (R=4..24) with an INDEPENDENT
   discretization (spectral, not FD-SL); confirm w_pos_low ~ 1/R^2 (w_pos_low*R^2 roughly constant, NOT
   w_pos_low constant). Attack: is the ~20-31 spread in w*R^2 evidence of a SMALL intrinsic offset hiding
   under the 1/R^2 (i.e. w^2 = c0 + c1/R^2 with c0 != 0)? Fit w^2 vs 1/R^2 and check the intercept c0 is
   consistent with 0 (box) vs a real intrinsic floor.
4. **The negative mode.** Confirm n_neg=1 at all R and that w_neg -> 0 as R grows (Derrick/dilatation
   direction, box-sensitive). Is it truly the scaling zero-mode going soft, or a genuine localized
   instability? Check its eigenvector is the breathing (radially-monotone) shape, not a localized node.
5. **#60 control.** Confirm the static control floors (|F|<1e-3) so the verdict is not a solver stall.
6. **The finite-A proxy (scope).** The back-reaction is the #65 time-averaged-energy harmonic-balance
   proxy, not a full multi-harmonic free-omega PDE. Confirm the box-control verdict does not hinge on the
   proxy (it is about R-scaling, which the linear spectrum already shows); confirm nothing is banked from
   the proxy beyond "no intrinsic level + still box-controlled."
7. **Action-fragility.** Confirm the box-control / single-Derrick structure persists at kap=0 (L2 only)
   and across the L4 weight — i.e. nothing self-traps that depends on the L4-vs-X^2 choice.
8. **Live time-row scope.** Confirm the standing-wave eigenproblem's diagonal-shift gauge does not hide a
   binding the off-diagonal g_tr would supply (the off-diagonal is built in the EL; argue the leading wave
   operator is gauge-correct, or flag the full-off-diagonal PDE as the remaining unbounded object).

---

## 11. SINGLE CLEANEST STATEMENT

Built the time-live 5-field (A,B,g_tr,phi,Theta) coupled system on the derived two-player operator with the
live e^{2phi} matter weight; both static-limit gates PASS exactly, GATE A recovers the STEP-3 static soliton,
the standing-wave spectrum is self-adjoint and grid-converged, and the #60 control gate passes. **S2-3
VERDICT: BOX-CONTROL** — the positive standing-wave tower scales omega^2 ~ 1/R^2 (the cell wall, not an
intrinsic level), finite amplitude does not open a new bound level, the only non-continuum feature is the
static soliton's single Derrick/dilatation breathing mode (which itself disperses to zero with the box and
is not L4-specific), and the verdict is action-robust. The derived operator with physical matter box-controls
the same way the old operator did — **no classical intrinsic discreteness; discreteness requires
quantization**, now demonstrated on the DERIVED operator with the now-physical matter coupling. Scope-flagged:
finite-A back-reaction is the #65 harmonic-balance proxy and strong coupling is grid-limited; the box-control
verdict is robust to both. NOT canon; OBSERVE + bounded only; DATA-BLIND honored (no mass targeted).

---

## VERIFICATION (2026-06-21) — blind adversarial pass, agent aad46ef1cae0a9737
SUPPORTED — the box-control NEGATIVE is honestly established and correctly scoped. Independent recompute
(reproduced every number to the digit; pushed the crux tests HARDER than the doc).
- GATES: S2-0a time-live Ricci - static Ricci = EXACTLY 0 (sympy; off-diagonal g_tr genuinely carried, g^tr!=0);
  S2-0b time-live matter EL -> static EL = EXACTLY 0; GATE A static anchor matches STEP-3; GATE B SL operator
  self-adjoint, spectrum real + grid-stable Nr48-80; the negative eigenvector is NODE-FREE monotone (breathing).
- **BOX-CONTROL 1/R^2 (the crux): AIRTIGHT.** Intercept fit w^2 = a/R^2 + b gives b = -0.037 +/- 0.024 (b/sigma
  = -1.5) = statistically ZERO and NEGATIVE (an intrinsic positive level needs b>0; impossible). Decisive R=64
  push: w^2 falls as clean 1/R^2 (R32->R64 drops by ~4 = box doubling), w^2*R^2 converges flat ~32, NO PLATEAU
  => no intrinsic floor. Cleanest possible box signature.
- NEGATIVE MODE = Derrick/breathing (n_neg=1 all R; w_neg->0 as R grows; node-free; present at kap=0). Not a level.
- FINITE-A: reproduced (no level opens; still box); the harmonic-balance PROXY is crude and the doc correctly
  does NOT bank the finite-A direction (only the R-scaling verdict). Honestly scoped.
- ACTION-ROBUST: structure persists at kap=0 (L2-only) + across L4 weight; verdict independent of L4-vs-X^2.
- SCOPE HONESTY: the 3 residuals (harmonic-balance proxy; strong-coupling grid limit; full off-diagonal g_tr PDE
  unrun) are explicitly flagged; "airtight" is used ONLY for "discreteness requires quantization on the derived
  operator with physical matter" (which the R=64 push supports), NOT the un-run objects. No overclaim.
BOTTOM LINE: BANK. On the DERIVED operator (vacuum!=GR, physical matter coupling, time live) the classical metric
gives NO intrinsic discreteness — the last classical redoubt is CLOSED, reproducing #65 on the corrected
foundation. The foundational audit's worry ("a different recipe could make the classical metric do MORE") is
ANSWERED: the different recipe was DERIVED and STILL box-controls. => MUST-QUANTIZE SURVIVES THE FOUNDATIONAL
AUDIT (robust on R-scaling; named residuals not banked).
