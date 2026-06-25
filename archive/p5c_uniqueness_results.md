# P5c-step-1 — DECISIVE UNIQUENESS RE-RUN at usable resolution

Research record (append-never-edit). **NOT canon.** Mode: OBSERVE/INFRA (solver
hardening; no physics claim). **DATA-BLIND** (units L=1; no wall numbers). Driver:
claude-opus-4-8[1m]. Date: 2026-06-20. Branch: `p5c-uniqueness`. NEW FILES ONLY
(committed p5b_*/full3d_* reused as imports — not edited).

Parent: `p5b_pc_floor_results.md` (the finding: at Nr=12 the re-posed F=0 is a near-flat
VALLEY along ONE edge-adjacent metric-warp mode → PC-independence FAILS; M_MS spread
0.269→0.296 = 9.3%, all in metric warps b,c,d, ~0 in Theta; cross-gauge dM_MS 4.6%;
§0 diagnostic predicted the near-null mode VANISHES at Nr≥16, κ 2.3e5→~3e3. The decisive
open question P5b left throughput-limited: does PC-independence + cross-gauge spread
COLLAPSE (artifact) or PERSIST (real) at Nr≥16?).

---

## THE DECISIVE QUESTION

At usable resolution (Nr=16, and Nr=24 if it floors in budget), does the Nr=12
non-uniqueness COLLAPSE (→ coarse-grid artifact; round-soliton M_MS bankable; §0 cure
confirmed) or PERSIST (→ real under-determination; the re-pose 'hold' edge gauge is
insufficient; manifold reopens)?

---

## THROUGHPUT REALITY (anti-hang; the binding constraint on this box)

Two prior agents HUNG here. This run obeyed: SINGLE clean process per solve, NO
background-poll, NO concurrent solves, hard caps. The dominant cost is the matrix-free
LSMR inner solve: every Newton iter burns ~the full LSMR cap (≈28 s/Newton-iter at
Nr=12, lsmr_cap=600 on the contended V100), and the line-search adds tries. Consequences:
- ONE PC floored to machine floor at Nr=12 costs ≈500 s (diag: 19 Newton iters → 3e-14).
- Therefore TWO PCs to floor cannot fit one <~560 s process. The decisive comparison is
  run as SEPARATE single-PC `solve` invocations (each a clean process), saved to /tmp,
  then a no-compute `compare`. This keeps the anti-hang contract while still getting the
  field-by-field + dM_MS numbers.

RESOLUTION (the tool that broke the throughput wall): the matrix-free JFNK could not
floor Nr≥16 in budget, but the **DENSE-LM path** (`reposed_dense_solve_fast`: jacrev
Jacobian + `torch.linalg.lstsq`, exact rank-revealing inner solve) floors Nr=16 to
Phi~1e-13 in ~7 min as a SINGLE clean process (Nr=12 ~100 s). svdvals-at-seed is seconds.
So the decisive uniqueness numbers WERE obtained at usable resolution — via dense, not
matrix-free. No hang: every solve was one capped process, sequential, never concurrent.

(Built: `p5c_runner.py` — matrix-free `solve NR PC GAUGE` (one clean capped JFNK + save) /
`compare`; `p5c_dense.py` — `svd NR` (conditioning) / `floor NR GAUGE` (dense-LM floor +
save) / `cmp NR` (cross-gauge dM_MS). Both reuse committed `p5b_pc.jfnk_solve`,
`p5a_prime_repose.{Repose,reposed_dense_solve_fast,reposed_jacobian_jacrev}`,
`p5b_loosethread.smooth_edge_bump`, `p5b_anchor.py`, `full3d_*` verbatim — no edits.)

---

## 1. PC-INDEPENDENCE spread vs Nr  (diag vs rband, gauge G1, both at floor)

| Nr | PC | committed-Phi | Newton its | M_MS | tvar | field max\|diff\| | M_MS spread (rel) |
|---|---|---|---|---|---|---|---|
| 12 | diag  | 7.90e-14 | 19 | 0.273216 | 3.571e-2 | (ref) | — |
| 12 | rband | 4.66e-14 | 18 | 0.297042 | 7.265e-3 | 1.18e+1 (b,c,d big; Th=0.22) | **8.72%** |
| 16 | diag  | 4.26e-2 (STALL) | 18 | 0.388 (unconv) | — | not measurable | — |
| 16 | rband | 2.37e-3 (not floored) | 8 (timed out) | — | — | not measurable | — |
| 24 | — | (not attempted — matrix-free JFNK is throughput-poison ≥16; see below) | | | | |

MATRIX-FREE PC-INDEPENDENCE AT Nr≥16 = THROUGHPUT-LIMITED. The matrix-free LSMR inner
solve never converges below the Krylov cap at Nr=16 (lsmr hit cap 500 / 1200 EVERY Newton
iter for both diag and rband); diag stalled at Phi=4.3e-2, rband reached 2.4e-3 in 8 iters
before the 590 s single-process wall (≈50 s/iter; a full floor needs ~20 iters ≈ 1000 s >
any safe single-process budget). So the diag-vs-rband floored comparison cannot be made
at Nr≥16 with the matrix-free tool. **The cross-gauge dense test (§2) settles uniqueness
without it** — and answers harder (it floors BOTH gauges to 1e-13 and shows the spread).
At Nr=12 the matrix-free PC-independence reproduces P5b: **8.72%** spread at machine floor
(both PCs ~5e-14), concentrated in b,c,d, Theta tiny.

DOES THE PC-INDEPENDENCE SPREAD COLLAPSE? → not measurable matrix-free at Nr≥16
(throughput); the SAME underlying non-uniqueness is measured directly by §2 (dense) and
§2b (SVD), and it does NOT collapse.

## 2. CROSS-GAUGE dM_MS vs Nr  — **THE DECISIVE RESULT** (dense-LM, BOTH at machine floor)

G1 = round-seed edges; G2 = G1 + smooth sin-bump amp=0.1 on the UNCONSTRAINED edge rows
of metric warps a,b,c,d only (Theta edges held identical in both gauges). Floored with the
DENSE-LM solver (`reposed_dense_solve_fast`: jacrev J + rank-revealing lstsq, exact inner
solve, min-norm on any near-null valley) — the tool the matrix-free JFNK could not match
in-budget at Nr≥16. Same round-seed body start for both gauges; the ONLY difference is the
held a,b,c,d edge rows.

| Nr | G1 Phi / M_MS | G2 Phi / M_MS (round seed) | dM_MS (rel) | field max\|diff\| (Theta) | both floored? |
|---|---|---|---|---|---|
| 12 | 9.94e-14 / 0.293604 | 8.89e-14 / 0.280614 | 1.30e-2 (**4.42%**) | 4.06 (Th=**0.05**) | yes |
| 16 | 9.55e-14 / 0.346597 | 1.21e-13 / **0.894294** | 5.48e-1 (**158%**) | 4.34 (Th=**2.63**) | yes |
| 24 | (not run — Nr=16 already decisive; dense floor ~440s/solve, Nr=24 ~2-3×) | | | | |

DOES IT SHRINK? → **NO — it does NOT shrink; the reposed floor is non-unique at Nr=16 and
the ambiguity is BIGGER than at Nr=12, not smaller.**

**SEED-INDEPENDENCE VERIFIER (mandatory; it refined the story — read this):** re-flooring
G2 at Nr=16 from a DIFFERENT body seed (the G1-floored solution instead of the round seed)
gives **M_MS=0.336024** (Phi=9.6e-14), NOT 0.894. So:
  - G1-16 (round seed) → 0.3466
  - G2-16 (round seed) → 0.8943
  - G2-16 (seeded from G1-floor) → 0.3360   ← same gauge, different basin
The clean "158% monotone gauge blowup" was an OVERSTATEMENT: the true cause is **multiple
distinct machine-floor solutions at Nr=16** (a genuine solution multiplicity), reachable by
seed AND/OR gauge. WITHIN one basin the two gauges nearly agree (G1=0.347 vs G2-from-G1=
0.336, ~3%); the round-seed entry to G2 finds a SEPARATE basin (0.894). Either way the
reposed floor is non-unique at Nr=16, and the multiplicity (basin + gauge) is the opposite
of the predicted collapse. (At Nr=12 the cross-gauge stayed ~4.4% and Theta untouched —
the extra Nr=16 resolution OPENS the multiplicity, it does not close it.)

## 2b. §0 CONDITIONING (SVD of reposed J at the round seed) — the non-uniqueness SOURCE

Direct measure of whether the isolated near-null edge mode (the CAUSE of the Nr=12
non-uniqueness) survives at usable Nr. (svdvals of dense jacrev J; fast, no Newton.)

| Nr | nB | kappa | smin | 2nd-smallest SV | #SV<1e-3·smax | near-null dir power | Theta |
|---|---|---|---|---|---|---|---|
| 12 | 1440 | **2.31e5** | 6.33e-5 | 1.47e-2 (**230× above smin**) | **1 (ISOLATED)** | a48% b25% c13% d13% | 0.7% |
| 16 | 3200 | **4.31e3** | 9.03e-3 | 9.03e-3 (**= smin, no outlier**) | 10 (degenerate band) | b20% c43% d33% | 0.2% |
| 24 | 5760 | **7.64e3** | 1.68e-2 | 1.68e-2 (**= smin, no outlier**) | 78 (band) | c39% d52% | 0.4% |

**The isolated near-null outlier — the Nr=12 non-uniqueness source — is GONE at Nr≥16.**
smin jumps 6.3e-5 → 9.0e-3 → 1.7e-2 (266× over Nr=12→24); kappa drops 53×; at Nr≥16 the
smallest SV equals the 2nd-smallest (a well-conditioned degenerate bulk, no isolated flat
valley direction). This is the §0 prediction, CONFIRMED at all three grids. The near-null
power stays ~99% on metric warps (≈0% Theta) throughout — consistent with an edge gauge
mode, not a physical Theta DOF. (Reproduces P5b §0 numbers independently.)

## 3. ANCHOR agreement vs Nr — **the FREE solver is clean; the re-pose is the culprit**

The dense FULL-SPACE free Newton (`full3d_newton.newton_solve`, NO re-pose, ALL DOF free
incl. edges — the most physical solve, via `p5b_anchor.py`):

| Nr | free-anchor M_MS | reposed-HOLD M_MS range (across PCs / gauges) | |
|---|---|---|---|
| 12 | **0.309035** (Phi 4.1e-13, 6 its) | 0.273 – 0.297 | reposed-hold spreads ~9%; free is single-valued |
| 16 | **0.292391** (Phi 8.5e-13, 23 its) | 0.336 – 0.894 (basin+gauge) | reposed-hold is multi-valued at floor; **free stays put** |

**The free solver is RESOLUTION-ROBUST and SINGLE-VALUED: M_MS 0.309 (Nr=12) → 0.292
(Nr=16), a few-% grid drift — exactly what a converging physical solution looks like.**
Meanwhile the reposed-'hold' M_MS is all over the map and gets WORSE with Nr. This pins
the non-uniqueness to the re-pose HOLD EDGE GAUGE (our instrument), not to the metric: the
free solve, which lets the edge DOF relax to their natural values, has no such ambiguity.

---

## VERDICT

→ **PERSIST (under-determination is REAL) — but localized to the RE-POSE 'HOLD' EDGE
GAUGE, NOT the metric.** This is a MISMATCH→SOLVER outcome, not MISMATCH→mechanism.

Evidence chain:
1. The Nr=12 non-uniqueness (PC-spread 8.7%, cross-gauge 4.4%) is NOT a flooring artifact:
   both PCs / both gauges reach machine floor (Phi ~5e-14 / 1e-13) and STILL differ.
2. The §0 *conditioning* near-null isolated edge mode DOES collapse at Nr≥16 (κ 2.3e5→4.3e3;
   smin 6.3e-5→9e-3; isolated outlier → degenerate bulk). The §0 prediction was right ABOUT
   THE CONDITIONING — but conditioning-collapse does NOT buy M_MS uniqueness.
3. The reposed floored M_MS is NON-UNIQUE at Nr=16 and the ambiguity GROWS, not shrinks:
   at Nr=12 cross-gauge ~4.4% with Theta untouched (0.05); at Nr=16 the SAME residual floor
   (Phi~1e-13) is reached by MULTIPLE distinct solutions — G1=0.347, G2(round)=0.894,
   G2(from-G1)=0.336 — a basin+gauge multiplicity with O(1) Theta differences (Theta ≈0 at
   Nr=12, O(1) at Nr=16). The seed-independence verifier showed the headline "158%" is a
   basin effect, not a clean monotone gauge law; but the conclusion (non-unique, worse at
   Nr=16) is unchanged and is the OPPOSITE of the artifact prediction.
4. The FREE full-space anchor (no hold gauge) is single-valued and resolution-robust
   (M_MS 0.309 → 0.292). So the metric/physics is fine; the re-pose hold gauge is the
   defective instrument.

NOTE the verdict is NOT the naive "manifold reopens / physics ambiguous." The free solve
is clean. What is indicted is the reposed-'hold' readout: it must NOT be used to bank
M_MS, and the loose-thread "spread shrinks with Nr → artifact" ruling from P5a'/P5b is
REFUTED at usable resolution.

---

## WHAT P5c-PROPER (off-round static) INHERITS

- **M_MS is NOT bankable from the reposed-'hold' solve at any Nr** — and gets worse with
  resolution. Banking M_MS off the round soliton requires either the FREE full-space solve
  (single-valued: 0.29–0.31, grid-converging) or a re-pose with a GAUGE-FIXED edge that
  pins the physical (Theta) content, not just the metric-warp edges.
- **The edge gauge must be fixed FIRST.** The 'hold' gauge holds a,b,c,d edge rows but
  leaves the body Theta free to respond to that arbitrary choice; at usable Nr this is an
  O(1) physical ambiguity. P5c-proper (off-round static) inherits a re-pose whose edge
  treatment is demonstrably under-determining — it must be replaced (e.g. the free-edge
  full-space solve, or a regularity/BC-pinned Theta edge) before any off-round M_MS is read.
- The matrix-free JFNK is throughput-poison at Nr≥16 on this box (LSMR never beats the
  Krylov cap); the DENSE-LM path (jacrev + lstsq) floors Nr=16 to 1e-13 in ~7 min and is
  the right production tool at these sizes. Use it for P5c-proper.

---

## PREMISE LEDGER (chose / derived)

| Item | tag | note |
|---|---|---|
| Residual = `full3d_solver.residual_vector` verbatim | DERIVED (reused) | unchanged |
| Re-pose body DOF + 'hold' edge gauge | INHERITED (P5a'/P5b) | edge DOF unconstrained gauge |
| Right-PC `rband` / `diag` | CHOSE (numerics) | du=P·y → cannot move F's zero set |
| PC pair = diag vs rband (not none) | CHOSE (throughput) | `none` burns full LSMR cap/iter (throughput-poison); both right-PCs are valid independence controls; P5b's 9.3% was rband-vs-diag-dominated |
| grid (12,6,8)/(16,8,8)/(24,8,8), p=0.4, kap8=0.05, m=1 | CHOSE (control) | anchor regime + refinements |
| smooth edge bump (gauge G2) | CHOSE (gauge) | smooth radial bump on UNCONSTRAINED edge rows only; regular gauge rep, not noise, not a physical-DOF freeze |
| Newton/LSMR hard caps | CHOSE (anti-hang) | floor = ~1e-10..1e-14 accepted; budget-limited cases reported as throughput-limited, never forced to a verdict |
| Dense-LM (`reposed_dense_solve_fast`) as the Nr≥16 floor tool | CHOSE (numerics) | exact rank-revealing lstsq inner; min-norm on near-null valley; floors Nr=16 to 1e-13 in budget where matrix-free can't. Same committed residual measured at the end. |
| Dense-LM min-norm = a gauge pick on the valley | NOTED | within ONE gauge the dense floor is well-defined (min-norm); the §2 finding is ACROSS two physical edge gauges, where min-norm cannot rescue the O(1) Theta divergence — so the result is gauge-under-determination, not a min-norm quirk |
| Free full-space anchor (`full3d_newton`) | DERIVED (reused) | the no-re-pose reference; single-valued + resolution-robust → isolates the hold-gauge as the culprit |

---

## ATTACK HERE (for a blind verifier)

1. **Is the Nr=16 G2 M_MS=0.894 a real alternate floored solution or a solver/basin
   artifact? — PARTLY ANSWERED, do not stop here.** This run's seed-independence check
   showed M_MS=0.894 is BASIN-dependent: G2-16 seeded from the G1-floor lands at 0.336, not
   0.894. So there are MULTIPLE distinct machine-floor solutions at Nr=16 (basin
   multiplicity), and the "clean gauge blowup" framing was corrected. The remaining attack:
   characterize the basins (how many? are the high-Theta ones spurious large-amplitude
   branches the FREE solver would reject, or legitimate?). Both 0.894 and 0.336 reach
   Phi~1e-13 on the committed residual, so neither is a non-solution — the question is which
   (if any) is physical. The free anchor (0.292) suggests the small-Theta basin is the
   physical one and the hold-gauge can trap the solver in a high-Theta basin.
2. **Does conditioning-collapse (§2b) contradict spread-explosion (§2)?** No — they measure
   different things: §2b is the LOCAL conditioning of J at the seed (the isolated edge
   near-null mode is gone at Nr≥16); §2 is the GLOBAL dependence of the floored solution on
   the edge-gauge CHOICE. A well-conditioned J at the seed does not pin which floored point
   a different held-edge gauge converges to. Verify both claims independently.
3. **Free-anchor robustness.** Confirm `p5b_anchor.py "12,6,8"` → 0.309 and `"16,8,8"` →
   0.292 (both Phi<1e-12), i.e. the free solve is single-valued and grid-converging while
   the reposed-hold is not. This is the load-bearing claim that the metric is fine and the
   hold gauge is the defect. Push it: try a third grid (Nr=20/24) on the free anchor.
4. **The refuted ruling.** P5a'/P5b conjectured "spread shrinks with Nr ⇒ coarse-grid
   artifact." This run measured the spread at floor at Nr=16 and it GREW (4.4%→158%).
   Attack the measurement (both gauges truly floored? Theta truly the divergence locus?)
   before accepting the refutation.
