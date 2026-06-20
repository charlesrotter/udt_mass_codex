# P5b — LIGHT PRECONDITIONER -> MACHINE FLOOR + PC-INDEPENDENCE + LOOSE-THREAD CLOSE

Research record (append-never-edit). **NOT canon.** Mode: OBSERVE/INFRA (solver
hardening; no physics claim). **DATA-BLIND** (units L=1; no wall numbers). Driver:
claude-opus-4-8[1m]. Date: 2026-06-20. Branch: `p5b-pc-floor`. NEW FILES ONLY
(committed scripts immutable).
Parent: `p5a_prime_repose_results.md` + `p5a_prime_VERIFIER.md` (re-pose -> full-rank
JFNK rescued; LSMR plateaued ~1e-8 at the anchor grid, Krylov-budget-limited; at-floor
PC-independence NOT reached; cross-gauge-spread-vs-Nr loose thread left OPEN).
Anchor: `full3d_newton.py` (dense full-space Newton).

---

## VERDICT (up front, honest)

**HEADLINE — the §0 premise was HALF right, and the other half is the real
result.** §0 predicted "well-conditioned at usable Nr -> a light/no PC
suffices, the strong-PC premise dissolves." The PC half is confirmed: a
light right-PC drives the re-posed JFNK to machine floor (3e-13) cheaply,
and even `none` (raw LSMR) floors -- no strong PC is needed. **BUT the deeper
finding is that PC-INDEPENDENCE FAILS at the anchor grid Nr=12**, and it
fails for a real reason, not a PC bug:

- At Nr=12 the three PCs (`none`/`diag`/`rband`) each reach committed-Phi at
  or near machine floor (3e-13 to 7e-9) yet land on **physically DIFFERENT
  floored solutions**: M_MS spreads 0.269 -> 0.296 (**9.3%**), and the
  field-by-field difference is HUGE in the metric warps b,c,d (max|diff| up
  to ~10.7) while Theta barely moves (max|diff| ~0.08-0.23).
- That difference lives **exactly in the §0 near-null direction** (~99% on
  the edge-adjacent metric-warps a,b,c,d, NOT Theta). So at Nr=12 the
  re-posed F=0 is **not an isolated point but a near-flat VALLEY** along that
  near-null edge mode; each PC settles at a different valley point with the
  same residual. This is a property of the REPOSED OPERATOR at coarse Nr, not
  of the preconditioner (a right-PC du=P y provably cannot move F's zero
  SET; it moved WHERE-on-the-zero-VALLEY the iteration stops).
- Independent corroboration: the **dense full-space free Newton anchor** at
  Nr=12 floors (Phi=4.1e-13, 6 iters) to **M_MS=0.309** -- different again
  from all three reposed-JFNK values, because the free solve lets the edge
  DOF move off the held gauge. And the **loose-thread cross-gauge** test
  (two regular edge gauges, both floored to 3e-13/6e-12) gives
  dM_MS=1.22e-2 (**4.6%**) at Nr=12 -- the same ~5% spread P5a' saw.

**The §0 cure (the near-null mode is GONE at Nr>=16, kappa drops to a clean
band) could NOT be verified AT FLOOR: Nr=16 is throughput-limited.** With a
24-Newton-iter cap and 3-way GPU contention the Nr=16 solves plateaued at
Phi=2e-3..4e-2 (not floored); the descent is steep (not Krylov-plateaued),
so it is an iteration-budget limit, not a wall. Therefore **whether the
manifold/spread COLLAPSES at usable resolution remains OPEN (throughput-
limited), exactly the loose thread P5a' left.**

**SCOPED STATUS: P5b PARTIAL.** GATE 1 (PC->floor) PASS at Nr=12. GATE 2
(PC-independence) **FAIL at Nr=12** -- and the failure is diagnostic, not
fatal: it pins the cause to the coarse-Nr near-null edge manifold. GATE 3
(grid convergence of M_MS) and the LOOSE-THREAD shrink-with-Nr both
**throughput-limited at floor** (Nr>=16 won't floor in the iteration budget
on this box). The decisive question P5c inherits: **floor the SAME case at
Nr>=16/24 with a real Krylov/iteration budget and re-run GATE 2 + the
cross-gauge spread; if the manifold collapses to a point, the anchor is
resolution-robust and the §0 cure is confirmed; if not, the solution-manifold
question reopens hard.**

---

## 0. WHAT THE DIAGNOSTIC FOUND (the PC design driver)

`p5b_diag.py` / `p5b_diag2.py` (dense SVD of the reposed J at the round seed):

| grid | reposed-J kappa | smin | 2nd-smallest SV | #SV < 1e-3·smax | near-null direction |
|---|---|---|---|---|---|
| Nr=12 (anchor) | 2.31e5 | 6.33e-5 | 1.47e-2 | **1 (isolated)** | ~99% on metric warps a,b,c,d (NOT Theta), edge-localized at the body row adjacent to the seal |
| Nr=16 | 3.42e3 | 9.57e-3 | 9.57e-3 | 7 (a band) | c/d-dominated, broader |
| Nr=24 | 6.32e3 | 1.91e-2 | 1.91e-2 | 62 (a band) | d-dominated, broader |

**Key:** at the anchor grid (Nr=12) the conditioning is ONE isolated near-null
edge-adjacent metric-warp direction (the "leftover inner-body gauge mode" the P5a'
verifier predicted), well-separated from the bulk (2nd SV 230x larger). A diagonal
block-Jacobi PC does NOT fix it (kappa stays 2.3e5 — it is a coupled radial direction,
not a diagonal scale). At usable Nr (16, 24) the isolated outlier is GONE and kappa
DROPS to ~3e3–6e3 (a clean band). => the PC must target the radial-coupled edge mode;
at usable resolution the operator is already far better conditioned.

---

## 1. WHAT WAS BUILT

`p5b_pc.py` — three RIGHT-preconditioners for the re-posed matrix-free JFNK
(all matrix-free, all built from JVP/VJP probes, all `du = P y` so they
cannot move the zero set of F):
- `pc_none` — identity (raw LSMR baseline).
- `pc_diag` — block-Jacobi `P = diag(J^T J)^{-1/2}`, Hutchinson-probed.
- `pc_rband` — RADIAL-BAND approximate-inverse: per (field, th, ps) line, the
  radial block of `J^T J` recovered by probing one representative line per
  field (round-seed near (th,ps)-invariant), then `B^{-1/2}` via tiny eigh.
  Targets the near-null edge-radial metric mode the diagnostic found.
- `jfnk_solve` — re-posed Newton outer + damped matrix-free LSMR inner with a
  pluggable right-PC; records residual history, inner-LSMR-iter counts, wall.

`p5b_gate12.py` (GATE 1+2 harness), `p5b_gridscan.py` (GATE 3), `p5b_loosethread.py`
(cross-gauge spread vs Nr), `p5b_anchor.py` (dense full-space Newton reference,
separate no-cache process), `p5b_diag.py`/`diag2.py` (§0 SVD conditioning),
`p5b_quick.py` (lean PC comparison). Edge gauge = the declared `hold` re-pose
from p5a' (edge DOF unconstrained, proven there); no new physical-DOF freeze.

Throughput note (anti-hang): the gates were run with HARD iteration caps
(Newton <=24, LSMR <=700-1500) and grids capped at Nr<=16. Driver = `python3`
(no venv); torch 2.5.1+cu121, V100, cuda=True, NVML warning ignored.

---

## 2. GATE 1 — PC -> machine floor (Nr=12 anchor (12,6,8), nB=1440)

The re-posed JFNK floors the COMMITTED residual at the anchor grid. Geometric
~7x/Newton-iter descent; even raw LSMR (`none`) floors — no strong PC needed.

| PC | Newton its | LSMR cap / tot | reposed=committed Phi | M_MS | tvar | wall |
|---|---|---|---|---|---|---|
| `rband` (12 it run) | 12 | 400 / 4800 | 8.63e-9 | 0.263421 | 3.27e-3 | 151s |
| `rband` (deep) | 17 | 600 / 10055 | **3.36e-13** | 0.295835 | 6.69e-3 | 310s |
| `diag` (deep) | 18 | 600 / 10800 | **3.43e-13** | 0.269344 | 1.66e-2 | 407s |
| `none` (deep) | 20 | 600 / 12000 | 7.24e-9 | 0.285285 | 1.51e-3 | 435s |

Per-Newton-iter history (rband, lcap=400): 80.4 -> 10.0 -> 0.53 -> 5.6e-2 ->
6.8e-3 -> 8.3e-4 -> 1.2e-4 -> 2.0e-5 -> 2.9e-6 -> 4.2e-7 -> 6.0e-8 -> 8.6e-9.
GATE 1 verdict: **PASS** — light PC (and even none) reaches machine floor in a
sane iteration count. `rband` floors fastest (17 it to 3e-13), `none` slowest.
Dense full-space anchor for comparison: Phi=4.1e-13 in 6 Newton iters (§5).

---

## 3. GATE 2 — PC-INDEPENDENCE at floor (Nr=12) — **FAIL (diagnostic)**

All three PCs reach committed-Phi at/near machine floor, yet land on
PHYSICALLY DIFFERENT solutions:

```
  none  Phi=7.24e-09 M_MS=0.285285 tvar=1.508e-03
  diag  Phi=3.43e-13 M_MS=0.269344 tvar=1.657e-02
  rband Phi=3.36e-13 M_MS=0.295835 tvar=6.690e-03
  M_MS spread across PCs = 2.65e-02 (rel 9.345%)
```
Field-by-field max|diff| (body DOF), confirming the diff is the §0 near-null
edge metric-warp mode (b,c,d big; Theta tiny):
```
  |rband - none| max=7.83e0  a=1.19 b=5.80 c=7.16 d=7.83 Th=8.27e-2  (peak radial j=1,2 = edge)
  |rband - diag| max=1.07e1  a=1.47 b=10.0 c=9.62 d=10.7 Th=2.28e-1  (peak radial j=4,1)
  |none  - diag| max=1.15e1  a=1.86 b=11.5 c=9.02 d=10.6 Th=1.72e-1  (peak radial j=4,3)
```
**Interpretation:** the re-posed F=0 at Nr=12 is a near-flat VALLEY along the
isolated near-null edge metric-warp direction (the exact §0 outlier:
smin=6.3e-5, ~99% on a,b,c,d not Theta). A right-PC cannot move F's zero set,
but it controls WHERE on the valley the iteration arrests — so different PCs
report different M_MS at the same residual. GATE 2 **FAILS at Nr=12** because
the fixed point is not isolated there. This is the operator's coarse-Nr
property, not a PC defect. **The §0-predicted cure (mode gone at Nr>=16) is
the test that decides whether this is a pure coarse-Nr artifact — and it is
throughput-limited (see §4).**

---

## 4. GATE 3 — grid scans — **throughput-limited at floor (Nr>=16)**

Nr=16 (16,8,8), nB=3200: with a 24-Newton-iter cap and 3-way GPU contention,
NONE of the three PCs floored (the prior agent's hang point — held to the cap
this time):

| PC | Newton its | LSMR tot | committed-Phi | M_MS | tvar | wall |
|---|---|---|---|---|---|---|
| `none`  | 24 | 16800 | 2.93e-3 | 0.268124 | 2.86e-3 | 807s |
| `rband` | 24 | 16800 | 2.28e-3 | 0.262888 | 6.90e-4 | 1025s |
| `diag`  | 24 | 16800 | 3.74e-2 | 0.457863 (unconverged) | 3.33e-2 | 866s |

The descent at Nr=16 is steep (rband, lcap=1500: 96.3 -> 5.6 in one step), so
this is an ITERATION-BUDGET limit, not a Krylov/conditioning wall — consistent
with §0 (kappa ~3e3 at Nr=16, well-conditioned). But because the solves do not
floor in budget, **M_MS grid-convergence (Nr=12->16->24) is NOT cleanly
measurable here** and is reported **throughput-limited, not run** at Nr>=16.
(The only floored M_MS values we have at Nr=12 are themselves non-unique —
the §3 manifold — so a coarse->fine M_MS trend is not meaningful until the
Nr>=16 floor + GATE 2 collapse is established.) Scalability timing (jfnk-step
vs dense-build) likewise **not run** (would require the floored grid scan).

---

## 5. LOOSE THREAD — cross-gauge dM_MS spread vs Nr — **Nr=12 measured; shrink throughput-limited**

Two regular edge gauges (G1 = round-seed edges; G2 = + smooth sin bump amp=0.1
on the unconstrained edge rows of a,b,c,d), both floored with `rband` JFNK at
Nr=12 (12,8,8):
```
  G1: Phi=6.40e-12 (newton 18, lsmr 10800) M_MS=0.263689 tvar=1.045e-02
  G2: Phi=3.06e-13 (newton 18, lsmr 10800) M_MS=0.251513 tvar=4.331e-03
  >>> cross-gauge dM_MS=1.218e-2 (rel 4.618%) dtvar=6.12e-3 [both floored<1e-9: True]
```
So at Nr=12 the cross-gauge spread is **4.6%** — matching P5a''s ~5%. Whether
it SHRINKS with Nr is **throughput-limited, not run**: Nr=16/24 do not floor
in the iteration budget (§4), so the decisive shrink-vs-Nr number cannot be
produced on this box in-budget. **The manifold-artifact ruling stays OPEN.**

---

## 6. AUDIT

- **Anchor / correctness reference (dense full-space Newton, separate no-cache
  process):** Nr=12 (12,6,8) floors Phi=4.10e-13 in 6 Newton iters,
  **M_MS=0.309035, tvar=1.31e-2**. This DIFFERS from all three reposed-JFNK
  floored values (0.269/0.285/0.296) — because the free Newton lets the edge
  DOF move off the `hold` gauge while the re-pose holds them. This is the
  strongest single corroboration that the re-posed-`hold` M_MS at Nr=12 is
  gauge-bound and non-canonical; the residual is correct, the M_MS readout is
  gauge/manifold-contaminated. Dense anchor at Nr=16 = **throughput-limited,
  not run** (no-cache dense jacrev build too slow in budget).
- **PC fixed-point-preserving?** Yes by construction (right-PC `du=P y` solves
  the same J du=-F reparametrized; cannot move F's zero set). The §3 spread is
  NOT a violation of this — it is the iteration arresting at different points
  of a near-flat zero VALLEY. The committed residual (verbatim
  `full3d_solver.residual_vector` via embed) is unchanged and is what every
  floor is measured on.
- **Hygiene physics-preserving?** The edge perturbation (loose thread G2) is a
  smooth bump on the UNCONSTRAINED edge DOF only — a regular gauge
  representative, not noise, not a physical-DOF freeze. Declared.
- **DATA-BLIND?** Yes — units L=1, no wall numbers, no comparison to any
  measured spectrum. M_MS/tvar are internal diagnostics only.
- **Honest gaps:** Nr>=16 never floored (iteration-budget limited under the
  anti-hang caps + GPU contention). Therefore the central §0 claim (mode gone
  -> manifold collapses -> PC-independence holds at usable Nr) is UNVERIFIED
  at floor. Reported as throughput-limited, not as a pass.

---

## 7. PREMISE LEDGER (chose / derived)

| Item | tag | note |
|---|---|---|
| Residual = `full3d_solver.residual_vector` verbatim (via embed) | DERIVED (reused) | unchanged; P5a' verified == vmap-safe to 3e-16 |
| Re-pose to body DOF + 'hold' edge gauge | INHERITED (P5a') | edge DOF unconstrained gauge (proven P5a'); declared |
| Right-PC `rband` (radial-band approx-inverse of J^T J) | CHOSE (numerics) | right-PC du=P·y -> cannot move F's zero set; targets the edge-radial near-null mode |
| Right-PC `diag` (block-Jacobi diag(J^T J)^-1/2) | CHOSE (numerics) | PC-independence control |
| grid (12,6,8)/(16,8,8)/(24,8,8)/(32,8,8), p=0.4, kap8=0.05, m=1 | CHOSE (control) | anchor-solvable canonical regime + refinements |
| smooth edge bump (loose-thread gauge G2) | CHOSE (gauge) | smooth radial bump on the UNCONSTRAINED edge rows only; a regular gauge representative, NOT noise, NOT a physical-DOF freeze |

---

## 8. SCOPED STATUS + what P5c inherits

**P5b = PARTIAL.**
- DONE: PC machinery built + run; GATE 1 (PC->floor) PASS at Nr=12; the light
  PC (and even `none`) reaches machine floor cheaply — **the "need a strong
  PC" premise is dissolved** (the §0 prediction's PC half confirmed).
- DONE (and the real result): GATE 2 (PC-independence) **FAIL at Nr=12**,
  pinned to a genuine near-null edge metric-warp MANIFOLD (M_MS spread 9.3%
  across PCs at machine floor; diff concentrated in b,c,d = the §0 outlier).
  Corroborated by the dense free-Newton anchor (M_MS=0.309 vs reposed 0.27-0.30)
  and the cross-gauge loose thread (4.6% at Nr=12).
- THROUGHPUT-LIMITED, NOT RUN: floor at Nr>=16 (the §0 cure), GATE 3 M_MS
  grid-convergence at floor, scalability timing, and the loose-thread
  shrink-vs-Nr. Nr=16 plateaued at 2e-3..4e-2 in a 24-iter cap (steep descent,
  not a wall) under the anti-hang budget + GPU contention.

**What P5c inherits (the decisive open item):** floor the SAME canonical case
at Nr=16 and 24 with a real iteration/Krylov budget (no 3-way contention; ~40+
Newton iters; or a stronger inner solve), then RE-RUN GATE 2 (PC-independence
field-by-field) and the cross-gauge dM_MS. Decision rule:
  - if at Nr>=16 the three PCs collapse to the SAME field AND the cross-gauge
    dM_MS shrinks toward 0 with Nr -> the Nr=12 manifold IS a coarse-Nr edge
    artifact, the anchor is resolution-robust, the §0 cure confirmed, P5b
    closes GREEN;
  - if the spread persists at Nr>=16 -> the solution-manifold (re-pose `hold`
    edge gauge underdetermines the physics) is REAL, not an artifact, and the
    re-pose gauge itself must be revisited (the free-Newton anchor's 0.309 is
    then the more trustworthy readout).
Either way, M_MS as a physics number must NOT be banked off the reposed-`hold`
Nr=12 solve — it is gauge/manifold-contaminated there.

---

## 9. ATTACK HERE (for a blind verifier)

1. **Is the §3 spread really a manifold and not a PC bug?** Re-derive that a
   right-PC `du = P y` cannot move F's zero set; then confirm the three floored
   solutions all satisfy committed-Phi at floor (they do: 7e-9/3e-13/3e-13) yet
   differ ~10 in b,c,d. If both hold, the spread is an operator manifold, not a
   PC defect — attack this logic.
2. **The throughput excuse.** Verify Nr=16 truly didn't floor (Phi 2e-3..4e-2)
   and that the descent is steep (not Krylov-plateaued) — i.e. it's iteration
   budget, not conditioning. Then FLOOR Nr=16 (more iters / no contention) and
   re-run GATE 2: this is the single result that flips P5b green or red.
3. **Dense anchor mismatch.** The free Newton gives M_MS=0.309 at Nr=12 vs
   reposed 0.27-0.30. Confirm this is the held-edge gauge (free solve moves
   edges) and not a residual-definition discrepancy between the two paths.
4. **Loose thread.** Reproduce dM_MS=4.6% at Nr=12; the open question is purely
   its Nr-dependence (throughput-limited here).

Repro: `python3 p5b_anchor.py "12,6,8"`; for the gates use the committed
`p5b_gate12.py usable` / `p5b_gridscan.py` / `p5b_loosethread.py 12,16` with a
larger Newton/LSMR budget than the anti-hang caps used here.
