> **CONDITIONS-CHANGED (2026-07-06 pre-native-era census) — NOT current native-micro canon; premise-scoped.**
> Companion verifier to the everything-on P2/P3/P4 arc (frame B, a(φ)=−1 / G=kap8·T), which is CONDITIONS-CHANGED
> (2026-07-06). Verifies DATA-BLIND machinery, banked no native-micro physics. Superseded frame; the 2026-07-01 native
> constrained-two-player operator (EH-empty, φ-blind matter, geometric 𝒦) is the current frame. See
> pre_native_era_census.md + NEGATIVES_REGISTRY.

# P4 — BLIND ADVERSARIAL VERIFIER REPORT

**Verifier:** claude-opus-4-8[1m] (independent, DATA-BLIND).  **Date:** 2026-06-20.
**Branch:** `p4-time-live`.  **Target:** `p4_time_live_results.md`, `p4_time_live.py`, `p4_validate.py`.
**Method:** cheap independent checks only (code audit, greps, independent re-derivation/FD,
reproduce `p4_validate` numbers, small-Nr full-stack containment).  Did NOT run the off-round
time-live coupled solve (P5 throughput wall, deliberately deferred).  Append-only.

Independent cross-check script was scratch (`/tmp`), not committed.  Numbers below are mine unless
quoted as "P4 doc".

---

## HEADLINE RULINGS

(a) **Containment bitwise?**  YES.  Reproduced + independently confirmed.
(b) **Time genuinely live in the residual?**  YES.  d_T g reaches Christoffels (0.067) and a
    nonzero G^t_r (linear in omega) reaches the Einstein residual; not a relabel.
(c) **THE TWO-EDGED (G^t_t machine-floor = Birkhoff cancel, or a wiring bug?)**  BIRKHOFF CANCEL,
    NOT a bug.  Decisively shown: the d_t^2 content ARRIVES (Christoffels differ 0.067, the live
    bracket is nonzero) yet the round diagonal G^t_t nets to ~1e-15 — and a NON-round live amplitude
    makes a diagonal (G^ps_ps) carry surviving time content (6.7e-2).  The cancellation is structural
    (round+diagonal), and it correctly predicts the surviving channel is the off-round wave (P5).
(d) **Hybrid time-delta accurate + omega range?**  YES at omega=0 (bracket==0 bitwise → G_live=G_weyl
    exactly, static sector uncontaminated).  For omega!=0 the bracket is genuine time content (same g,
    only the t-row differs, so the difference IS the time content — confirmed channel-by-channel) and
    is O(omega), well-conditioned (4.7e-2 at omega=1, not the O(1e1) raw-kernel artifact).  Same
    small-shear caveat as P1 inherited (see PARTIAL note).
(e) **"DONE-for-scope / PARTIAL" honest?**  YES.  P4 makes NO omega claim, NO box-control verdict,
    NO tower re-hunt; the off-round coupled solve is named as a throughput deferral (P5), not a null.

**NET: P4 STANDS.**  No smuggled solved-dynamics, no hidden freeze, no closed-time import found.

---

## CLAIM-BY-CLAIM

### 1. CONTAINMENT bitwise — STANDS
- KERNEL (my Nr=24, independent): `omega=0` → `max|dt_g|=0, max|dtt_g|=0`; bracket
  `max|kernel(on)-kernel(off)| = 0.00e+00`; `max|G_live - G_weyl| = 0.00e+00`.  Static sector
  provably uncontaminated.
- KERNEL (reproduced `p4_validate` Nr=40): `omega=0 vs static einstein_mixed: max|dG| = 0.000e+00`;
  delta sweep 4.7076e-2 / 1.1769e-2 / 2.2321e-3 / 2.2321e-4 / 0 — matches the doc table BITWISE.
- FULL STACK (my Nr=16 — the doc's Nr=32/40 didn't fit the verifier time budget; binding quantities
  are resolution-independent): static anchor `Phi=8.59e-16`; live residual at omega=0 seeded by the
  static soliton `Phi=8.59e-16` (= static floor); after Newton: `dM_MS=0.000e+00`,
  `max|field drift|=0.000e+00`, `live-amplitude max=0.000e+00`.  The static soliton IS the omega=0
  fixed point, bitwise.  (M_MS/Phi magnitudes differ from the doc only by resolution; dM=drift=amp=0
  exactly, as the doc claims.)

### 2. TIME GENUINELY LIVE — STANDS
- `dt_g[T-slot]=1.56e-1`, `dtt_g[T-slot]=1.36e-1` at omega=1 (nonzero).
- `max|Gamma(time on) - Gamma(time off)| = 6.68e-2` ≠ 0 — d_T g reaches the Christoffels (matches the
  doc's 0.062; small diff = my Nr=24 vs doc Nr).
- Live Einstein delta channel-by-channel: `G^t_r = 1.83e-2` (and `G^r_t = 1.81e-2`) ≠ 0 → time content
  genuinely reaches the residual; `=0` at omega=0.  Not silently dropped, not a relabel.

### 3. THE TWO-EDGED (Birkhoff cancel vs wiring bug) — STANDS (correct = Birkhoff)
- d_t^2 content ARRIVES then CANCELS in the round diagonal: Christoffels differ (6.68e-2) and the
  live bracket is nonzero, yet `delta G^t_t = 2.67e-15` (machine floor).  This rules out the
  "never-arrived" bug branch (if d_t^2 never wired in, Christoffels would NOT differ).
- DECISIVE off-round probe (my own, the doc's suggested attack): turn on a NON-round live amplitude
  `c1!=0` (theta-warp).  Result: `delta G^ps_ps = 6.72e-2` SURVIVES (a diagonal now carries d_t^2),
  while round `G^t_t`, `G^th_th` stay at floor (~1e-15).  → the diagonal cancellation is specific to
  the round+diagonal class (Birkhoff/phase0), and the off-round wave is exactly where d_t^2 persists.
  P4's prediction that P5's off-round l>=2 wave is the surviving-d_t^2 channel is CORRECT.

### 4. T_tr ANCHOR — STANDS
- `field_dn_s2` (P2) zeroes the T-slot (audited: only R/TH/PS filled); P4 injects
  `dn[...,T,:] = (-omega F1 sin(wt)) * (dn/dF)` — manifestly zero at omega=0, linear in omega, odd in
  omega.  So the analytic form already guarantees the claimed structure.
- INDEPENDENT finite-difference-in-time T_tr (my own, NOT using P4's analytic dn[T]; central FD of the
  unit-S^2 vector): `omega=0 → 0.0000e+00` (exact); `omega=0.1 → 5.90e-3`; `omega=1.0 → 5.90e-2`
  (exactly linear, ×10).  Oddness: `+0.3 → +1.77e-2`, `-0.3 → -1.77e-2` (exactly opposite sign).
  (Absolute value differs from the doc's 4.124e-2 only because I used a different F1/Nr; the
  STRUCTURE — vanishes iff d_t F=0, linear, odd — matches the doc exactly.)
- T_tr ≠ 0 sources the G_tr momentum constraint → escapes Birkhoff.  Confirmed.

### 5. POLE-STABLE HYBRID — STANDS (with the inherited P1 caveat)
- The backbone `F3.einstein_mixed_weyl` resolves to `einstein_3d_eval.einstein_mixed_weyl` (analytic),
  genuinely independent of the core kernel.  At omega=0 the bracket is 0 bitwise → no contamination of
  the static sector (claim 1).
- The bracket is genuine general-kernel time content, not a diagonal stand-in: both kernel evals share
  the SAME g and differ ONLY in the t-row, so the difference IS the time content (verified by the
  nonzero G^t_r/G^ps_ps deltas in claims 2/3).
- O(omega) and well-conditioned (4.7e-2 at omega=1 vs the documented O(1e1) raw-kernel artifact the
  hybrid avoids).  CAVEAT (inherited, flagged): the hybrid's quantitative accuracy at large omega /
  steep off-round shear shares P1's small-shear conditioning regime; this is a P5-inherited accuracy
  question, not a P4 containment problem.  Honestly flagged in the P4 audit table (category-A).

### 6. DISCIPLINE — STANDS
- Open-time only: grep finds "closed-time" ONLY in disavowal comments ("NO closed-time import";
  "a closed-time read would miss this").  No Wick/Euclidean/imaginary-time object.
- a(phi)=-1 baseline: `k=0` everywhere; verified `ruler_exponent(k=0)=0` exactly → `W==1` (GR baseline).
- Native S^2, no Skyrme m*PI: the only `m*PI`/Skyrme references are disavowal comments; P4 adds none.
- B=1/A free: no injection (audit: static anchor max|a+b|≠0); a,b independent.
- NO smuggled omega!=0 solved dynamics: containment closure pins a1=b1=F1=0 at omega=0 (the correct
  static limit, not a hidden freeze of omega!=0 dynamics).  omega!=0 dynamics is explicitly P5.
- Data-blind: only residuals, omega-scalings, code-unit M_MS.  No lepton/mass/ratio/wall numbers.

### 7. "DONE-for-scope / PARTIAL-on-physics" HONEST? — STANDS
- The doc/script explicitly assert NO omega claim, NO box-control verdict, NO tower/catalog re-hunt
  (#65 cited as standing, not re-litigated).  The off-round + time-live coupled free-omega solve is
  named as the P5 dense-Newton/Newton-Krylov throughput build (#60 wall), reported as throughput-
  limited — NOT dressed as a null or a physics verdict.  This is an honest deferral.

---

## WHAT P5 CORRECTLY INHERITS
A VALIDATED time-live residual whose omega=0 limit is provably the static P3 soliton (bitwise
containment), the pole-stable hybrid time-row evaluator, and the confirmed off-round channel
(non-round amplitude → surviving diagonal d_t^2) as the place to push.  P5 inherits the P1/P5 large-
omega / steep-shear hybrid-accuracy question (the small-shear regime) — a quantitative accuracy task,
not a containment defect.

## MINOR NOTES (non-blocking)
- Harmonic balance is evaluated by COLLOCATION at a single representative phase (cph=sph=1/√2), not a
  true Fourier/Galerkin projection onto cos^0/cos^1.  Irrelevant to omega=0 containment (all time
  terms vanish); for omega!=0 multi-harmonic / projection convergence is a P5 truncation test (the doc
  flags "one harmonic; multi-harmonic convergence is a P5 truncation test").
- Verifier could not finish the doc's exact Nr=32/40 full-stack run within budget (timeout 124); the
  binding containment quantities were instead confirmed at Nr=16/24 (resolution-independent: all
  exactly 0) plus the doc's Nr=40 P4b(i) reproduced bitwise.  No discrepancy with the doc found.

## VERDICT
**P4 STANDS** (DONE-for-scope, PARTIAL-on-physics).  Containment BITWISE; time GENUINELY live in the
residual; the round-diagonal G^t_t machine-floor is the BIRKHOFF cancellation (independently shown via
the surviving off-round diagonal), NOT a wiring bug; the hybrid time-delta is exact at omega=0 and
genuine/well-conditioned at omega!=0 (with the inherited P1 small-shear caveat); discipline clean
(open-time, a=-1, native S^2, no Skyrme/B=1/A injection, data-blind); the P5 deferral is honest.
