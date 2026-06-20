# P4 — Time Live: Turn On the Live Time Row in the Everything-On Solver

**Mode:** BUILD + OBSERVE (the everything-on solver, EVERYTHING_ON_SOLVER_BUILD_MAP.md §III, P4).
**Agent:** claude-opus-4-8[1m].  **Date:** 2026-06-20.  **Status:** NOT canon.  Append-only.
**Branch:** `p4-time-live`.  **DATA-BLIND** (units L=sqrt(kappa/xi)=1; no lepton/mass/ratio/wall
numbers; the only quantities are residuals, omega-scalings, and M_MS in code units).
**Scripts (NEW, committed with this doc):** `p4_time_live.py` (the live-time machinery),
`p4_validate.py` (containment + anchor + observation).
**Discipline:** OPEN time only (NO closed-time import).  a(phi)=-1 GR baseline (P3 ruler weight
k=0 -> W==1).  Native S^2 carrier (P2).  B=1/A FREE.  Observe-not-target (NO tower/catalog hunt;
#65 retired and NOT re-litigated).

---

## 0. WHAT P4 IS (and is not)

P4 completes the time-on WIRING of the everything-on solver and OBSERVES what the wired metric
does.  The kernel `whole_metric_3d_core` has a `dg[...,T,...]` (time) slot that EXISTS but is
ZEROED by every caller (`full3d_spectral.einstein_mixed` fills only R/TH/PS; `einstein_3d_eval.
einstein_mixed_weyl` is purely static/diagonal).  P4 supplies `d_T g != 0` to the kernel via
OPEN-TIME HARMONIC BALANCE and brings the MATTER profile's time-dependence live so `T_tr != 0`
can source `G_tr` (escapes Birkhoff -> unfreezes time).

P4 does NOT re-hunt a tower or a catalog (retired #65).  It does NOT run the FULL off-round +
time-live COUPLED solve to a free-omega eigenvalue — that is the P5 throughput build (the #60 wall);
where it would be needed it is reported P5-DEFERRED, not as a verdict or a null.

---

## 1. WHAT I BUILT (the time row is now live in the P1-P3 stack)

### `p4_time_live.py`

**Open-time harmonic balance.**  Every field carries a single live harmonic about its static
profile (phase0 (C), DERIVED-from-kernel):
```
u(t,r,..) = u0(r,..) + u1(r,..) cos(omega t)
  d_t u   = -omega u1 sin(omega t)     (algebraic in omega)
  d_t^2 u = -omega^2 u1 cos(omega t)   (algebraic in omega)  ->  d_t^2 -> -omega^2 on u1
```
`omega` is FREE; static is the `omega->0` limit (`d_t g -> 0`).  OPEN time only.

* `build_metric_live(...)` — diagonal Weyl metric (round channel: c=d=0) with live time-amplitudes
  a1,b1.  Returns the metric VALUE `g` at a representative phase AND its analytic time partials
  `d_t g`, `d_t^2 g` (algebraic in omega; the kernel's `d_dx` is spatial-only, phase0 (C)4, so the
  time content MUST be supplied analytically).

* `einstein_live_kernel(...)` — the literal CORE kernel with the live t-row WIRED:
  `dg[...,T,..] <- d_t g` (the P4 wiring) and `dGamma[...,T,..] <- d_t Gamma` built analytically
  (`d_t Gamma = 1/2[d_t ginv . Tterm + ginv . d_t Tterm]`, with `d_t ginv = -ginv d_t g ginv` and
  `d_t Tterm` carrying both the mixed `d_x(d_t g)` and the t-row `d_t^2 g`).  omega->0 zeroes both.

* `einstein_live(...)` — **POLE-STABLE HYBRID** (the load-bearing conditioning fix, §4):
  `G_live = G_weyl(a,b,c,d) + [kernel(time ON) - kernel(time OFF)]`.  The bracket is the time-row
  DELTA (well-conditioned, O(omega)); the diagonal/spatial backbone is the analytic pole-stable
  Weyl.  At omega=0 the bracket is IDENTICALLY ZERO -> `G_live == G_weyl` EXACTLY.

* `field_dn_s2_live(...)` — the native S^2 unit-3-vector with a LIVE time slot:
  `dn[...,T,:] = (dn/dF) d_t F`, `d_t F = -omega F1 sin(omega t)`.  So `T_tr != 0` is sourced by
  the matter's own time-dependence (the `native_matter_timelive_probe` object, in production).

* `stress_live` (ruler weight k=0 = GR), `T_tr_anchor` (<T_tr>_{l=0}), `M_MS_of` (the static
  readout on the live rho).

### `p4_validate.py`
P4b containment (kernel + full-stack + T_tr anchor) and P4c observation.

---

## 2. P4b — CONTAINMENT (the binding check) — PASS

### (i) KERNEL: omega->0 returns the static Einstein EXACTLY
Background = the converged round-S^2 soliton; a non-trivial live amplitude (a1,b1) imposed.
```
omega=0 live-kernel (hybrid) vs static einstein_mixed_weyl:  max|dG| body = 0.000e+00  (BITWISE)
```
The live-time DELTA (bracket = kernel(time on) - kernel(time off)) vanishes continuously to 0:
```
 omega   max|live-time delta|(body)
 1.00    4.708e-02
 0.50    1.177e-02   (x4.0)
 0.10    2.232e-03   (x5.3)
 0.01    2.232e-04   (x10.0)
 0.00    0.000e+00   (EXACT)
```
The delta is dominated by the O(omega) `G^t_r` momentum constraint (hence the ~x10, not x100, drop
at small omega — the LINEAR Birkhoff-escape channel; see P4c(b)).  At omega=0 it is exactly zero.

### (ii) FULL STACK: omega->0 returns the static P3 soliton — BITWISE
The round time-live residual (unknowns a0,b0,F0,a1,b1,F1; rows = harmonic-balanced G^t_t, G^r_r,
matter EL, the G^t_r momentum row, + the live-amplitude closure pinned at omega=0), seeded by the
static soliton:
```
STATIC anchor (p2_round_s2, Nr=32): Phi=1.612e-16   M_MS=73.720638
live residual at omega=0, static-seeded:           Phi = 1.612e-16   (= the static floor EXACTLY)
omega=0 live solution (after Newton refine):        Phi = 1.612e-16   M_MS = 73.720638
  |M_MS(live,omega=0) - M_MS(static)| = 0.000e+00   (CONTAINED, bitwise)
  max|static-field drift|             = 0.000e+00
  live-amplitude max                  = 0.000e+00   (-> 0)
```
The static P3 soliton IS the omega=0 fixed point of the live residual, exactly.  (The static
M_MS at Nr=40 is 122.982071 — the anchor used for higher resolution; Nr=32 used for the solver
loop throughput, dM=0 at both.)

### (iii) T_tr ANCHOR (the physical justification, in THIS stack) — CONFIRMED
A time-live native profile (F1 != 0) on the round soliton:
```
omega   max|<T_tr>_l0|    max|T_tr(point)|
0.00    0.000e+00         0.000e+00        <- d_t F = 0: T_tr IDENTICALLY 0 (static, Birkhoff)
0.01    4.124e-04         1.408e-03
0.10    4.124e-03         1.408e-02
1.00    4.124e-02         1.408e-01
```
omega=0 (d_t F=0) gives T_tr identically 0; omega!=0 gives T_tr != 0, scaling linearly in omega.
=> the time-live native profile SOURCES `G_tr` => escapes Birkhoff => time unfreezes.  This
reproduces `native_matter_timelive_probe` in the production P1-P3-P4 stack (not just the sympy probe).

---

## 3. P4c — OBSERVE (the tractable round time-live channel; NO tower hunt)

### (a) <T_tr> is ODD in omega (open-time momentum-flux signature)
```
omega=+0.30:  <T_tr>_l0 peak = +1.237e-02
omega=-0.30:  <T_tr>_l0 peak = -1.237e-02
```
Reversing the time-direction reverses the momentum flux — the OPEN-time signature (a static read,
or a closed-time read, would miss this).  This is what a live, open time axis looks like in the
stress: a genuine T_tr momentum flux that is antisymmetric under t -> -t.

### (b) G^t_r momentum-constraint strength is LINEAR in omega (the live channel)
```
omega   max|G^t_r| body
0.00    0.000e+00
0.10    2.232e-03
0.30    6.696e-03
1.00    2.232e-02
```
`G^t_r` grows ~linearly in omega (a FIRST-order momentum constraint) — the live time row genuinely
reaches the Einstein residual.  This is the Birkhoff-escape channel: in the round vacuum class
`G_tr = 2 d_t phi/r` forces static; here the live amplitude + matter T_tr keep it nonzero.

### (c) The DIAGONAL G^t_t time-kinetic shift is at MACHINE FLOOR (honest, two-edged)
```
omega   max|dG^t_t|
0.10    1.42e-14
0.30    1.42e-14
1.00    2.13e-14
```
**HONEST READ:** the diagonal `G^t_t` shift is at machine floor (~1e-14), NOT a growing O(omega^2).
The live time does NOT show up in the diagonal `G^t_t` for the ROUND class at this order — it shows
up in the MOMENTUM CONSTRAINT `G^t_r` (part b).  This is EXACTLY Birkhoff/phase0: round + diagonal
freezes the diagonal time-kinetics; the escape is the `G_tr` channel.  The `d_t^2` content IS wired
(verified: the live Christoffels differ from static by 0.062 with dg[T] populated; `dtt_g`~0.15
reaches `dGamma[T]` -> Riemann), but its net DIAGONAL contribution CANCELS for the round metric.
The non-round l>=2 wave channel (phase0 B2, where `d_t^2 h` survives the angular projection) is
where the diagonal `d_t^2` would persist — that is the OFF-ROUND time-live solve, P5-deferred.

### What is GENUINELY NEW here vs #65
- #65 (`timelive_nonround_native_solve`) was a STRUCTURAL-FIRST + reduced-operator read: a modeled
  radial profile, a single-carrier SL eigenproblem, the full coupled solve NOT built (its own §4/§6
  flagged both shortcuts).  Its verdict (intrinsic centrifugal floor + box-continuum, no new bound
  tower) STANDS and is NOT re-litigated.
- P4 is the FULL-STACK WIRING: the live time row reaches the GENERAL 4x4 Einstein (the P1 hybrid
  engine), with the 3-D native S^2 matter (P2) and the a(phi) ruler weight (P3), with omega-free
  harmonic balance — and PROVES containment BITWISE (omega->0 == the static P3 soliton) and the
  T_tr Birkhoff-escape anchor IN PRODUCTION (not just sympy).  This is infrastructure #65 never had:
  a time-live solver whose omega=0 limit is provably the validated static soliton.
- What P4 did NOT do (vs a hypothetical "P4 spectrum"): it did NOT solve the full off-round +
  time-live coupled system to a free-omega eigenvalue.  That is P5.  P4 makes NO omega claim, so
  there is NO box-control verdict to assert (correctly — an intrinsic-omega claim would REQUIRE the
  box-control gate, and that gate lives on the P5 solve).

### Throughput-limited / P5-deferred (named plainly)
- The FULL COUPLED time-live solve with omega a FREE eigenvalue on the OFF-ROUND off-diagonal stack
  (joint a0,b0,c0,d0,F0 + e_rt,e_rp,e_tp + a1,b1,...,F1 + omega closure) driven to a clean floor is
  the P5 dense-Newton / Newton-Krylov build (the #60 wall).  NOT run here.  The column-FD Jacobian
  over 6*Nr unknowns with autograd EL per column is already the throughput edge at Nr<=40 on the
  V100; the joint off-round time-live Jacobian is the P5 research-grade driver.

---

## 4. AUDIT — every compromise / freeze, flagged

| Item | tag | note |
|---|---|---|
| Open-time single harmonic `u0 + u1 cos(wt)` | CHOSE + truncation (L-trunc) | one harmonic; multi-harmonic convergence is a P5 truncation test.  OPEN time (no closed-time import). |
| `d_t^2 -> -omega^2`, omega free, static=omega->0 | DERIVED-from-kernel (phase0 (C)) | algebraic in omega; containment proven bitwise. |
| **POLE-STABLE HYBRID** (Weyl backbone + kernel time-DELTA) | CHOSE (category-A conditioning) | **LOAD-BEARING.** The raw CORE-kernel general Einstein is core-edge ill-conditioned on steep soliton warps (gives G^t_t~16, G^r_r~33 vs Weyl ~0.28 — a NUMERIC artifact).  The hybrid (same as P1's off-diagonal fix) subtracts the shared conditioning error; field equations UNCHANGED; omega=0 -> Weyl EXACTLY.  Flagged, not hidden. |
| Round channel (c=d=0, diagonal) for the OBSERVE/containment | CHOSE (tractable per #65) | the round time-live channel is the tractable one; off-round is P5.  Declared. |
| Containment closure pins a1=b1=F1=0 at omega=0 | CHOSE | this is the CORRECT static limit (no live amplitude at omega=0); it makes containment a clean bitwise check, NOT a hidden freeze of dynamics (omega!=0 dynamics is the P5 solve, separately). |
| a(phi)=-1 (k=0, W==1) | BASELINE (L-a) | GR baseline; a(phi)!=-1 is P3 exploration, NOT P4. |
| Native S^2 carrier, deg-1 node, NO Skyrme BC | DERIVED/HONORED (L-carrier, L-BC3D) | grep: the only m*PI is the labelled negative control in the imported P1/P2 modules; P4 adds none. |
| B=1/A FREE (a,b independent) | HONORED | static anchor shows max|a+b|=0.477 != 0 (B=1/A not injected). |
| Core cutoff rc=0.05 | inherited (L-core) | the #61 scar; inherited from the static anchor, scoped, P6 retires it. |

**Is time GENUINELY live?**  YES.  `d_T g != 0` reaches the residual: `dt_g`~0.15 populates the
kernel's t-slot; the live Christoffels differ from static by 0.062 (dg[T] reaches Gamma);
`dtt_g`~0.15 enters `dGamma[T]` -> Riemann; and the result is a nonzero `G^t_r` (linear in omega)
and a nonzero matter `T_tr` (linear in omega).  Nothing stayed static except where Birkhoff FORCES
it (the round diagonal G^t_t — correctly, and observed as such).  **Open-time only** (no closed-time
object anywhere).  **Data-blind** (only residuals / omega-scalings / code-unit M_MS).

---

## 5. SCOPED STATUS

**P4 = DONE for its scope (wiring + containment + observation), PARTIAL on the full physics.**
- DONE: the live time row is wired into the full P1-P3 stack (general Einstein hybrid + 3-D native
  S^2 matter + a(phi) ruler weight); CONTAINMENT proven BITWISE (omega->0 == static P3 soliton,
  dM_MS=0, Phi=static floor); the T_tr Birkhoff-escape anchor CONFIRMED in production.
- OBSERVED (round channel): T_tr is the live, odd-in-omega momentum flux; G^t_r is the live linear
  channel; the diagonal G^t_t is Birkhoff-frozen (the escape is G_tr, as predicted).  NO tower,
  NO catalog, NO omega claim, NO box-control verdict (none is warranted without the P5 solve).
- P5-DEFERRED (throughput): the full off-round + time-live COUPLED solve to a free-omega eigenvalue
  (the #60 wall) — the research-grade driver.  P5 inherits a VALIDATED time-live residual whose
  omega=0 limit is provably the static soliton, so P5 can build continuation in omega from a known
  good anchor.

**What P5 inherits:** `p4_time_live.einstein_live` (pole-stable hybrid, time row live),
`field_dn_s2_live` (live matter), and `p4_validate.residual_round_live` (the harmonic-balanced
time-live residual, containment-validated).  P5's job is the driver (preconditioned Newton-Krylov /
sparse-direct) to push the joint off-round + time-live system to a clean floor with omega free.

---

## 6. ATTACK HERE (for a blind verifier)

- **CONTAINMENT bitwise-ness:** re-run `p4_validate.p4b_fullstack_containment`.  Confirm the live
  residual at omega=0 seeded by the static soliton is at the STATIC floor (Phi~1.6e-16) and the
  Newton refine does NOT move M_MS (dM=0).  If it drifts, the hybrid is not recovering the static
  engine — check `einstein_live` at omega=0 gives `G_weyl` bitwise (it should: the bracket is 0).
- **The HYBRID is the load-bearing choice — is it legitimate?**  The raw CORE kernel gives
  G^t_t~16 on the soliton (a conditioning artifact).  Verify: (i) at omega=0 the bracket
  `kernel(on)-kernel(off)` is identically 0 (so G_live=G_weyl exactly — no contamination of the
  static sector); (ii) the bracket at omega!=0 is well-conditioned (O(omega), not O(1e1)); (iii)
  the field equations are UNCHANGED (it is the same general 4x4 Einstein, only the EVALUATION is
  pole-stable).  ATTACK: does the bracket subtraction drop any genuine time content?  It should
  not — both kernel evals share the same g; only the t-row differs, so the difference IS the time
  content.  Confirm the live `G^t_r` (0.022 at omega=1) matches an independent harmonic-balance
  G_tr computation.
- **Is the time row genuinely live (not a relabel)?**  Confirm `dg[...,T,..]` is nonzero and that
  `christoffel(time on) != christoffel(time off)` (0.062 here), i.e. d_T g reaches Gamma.  Confirm
  `dGamma[...,T,..]` (the analytic d_t Gamma) carries `dtt_g` (the d_t^2 content) by an independent
  finite-difference-in-t check on a toy harmonic metric.
- **T_tr anchor:** independently compute T_{tr} for the time-dependent unit-S^2 field (the
  native_matter_timelive_probe object) and confirm it is 0 iff d_t F = 0, scaling linearly in omega
  (the 4.124e-02 at omega=1).  Confirm it is ODD in omega.
- **G^t_t machine-floor claim (the honest two-edged part):** confirm the diagonal G^t_t shift is
  genuinely ~1e-14 (Birkhoff freeze of the round diagonal), NOT a wiring miss.  Best attack: turn on
  a NON-round amplitude (c1 != 0, the l>=2 channel) and check whether a surviving d_t^2 appears in
  G^th_th (phase0 B2 says it should — that is the off-round wave channel P5 must solve).
- **Open-time discipline:** grep p4_time_live.py / p4_validate.py for any closed-time object (none
  should exist).  Confirm a(phi)=-1 baseline (k=0 -> W==1), no Skyrme BC, no B=1/A injection.
- **Over/under-claim:** confirm the doc claims NO omega, NO tower, NO box-control verdict; confirm
  the P5 deferral is named as throughput-limited, not as a null or a physics verdict.

## STATUS
P4 COMPLETE for wiring + containment + observation; PARTIAL on full physics (P5-deferred coupled
off-round time-live solve).  Containment BITWISE (omega->0 == static P3 soliton).  T_tr Birkhoff-
escape anchor CONFIRMED in production.  Round channel OBSERVED (live odd-in-omega T_tr + linear
G^t_r; round diagonal Birkhoff-frozen, correctly).  NO tower/catalog hunt.  Native, open-time,
data-blind.  Pole-stable hybrid flagged as the load-bearing conditioning fix.  NOT canon.  Blind
verifier next.
