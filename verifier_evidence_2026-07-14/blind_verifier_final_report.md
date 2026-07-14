# Blind adversarial verifier — final report (verbatim), 2026-07-14
# Agent: zero-context, adjudicate-(A)-vs-(B) framing; independent code (verify_*.py in this directory).
# This is the verdict recorded in commit 1c2196c. Raw tool I/O: blind_verifier_raw_output.txt.

All checks complete (total GPU ~35 min, sequential single-process, everything bounded). Final report:

## CHECK 1 — CRITICALITY: PASS-for-(A)
| grid | E | ||P_free P_tan grad|| | RMS/free-DOF | ratio vs unit-kick force ||H t_rand|| |
|---|---|---|---|---|
| 128 | 271.831076 | 1.195e-3 | 5.0e-7 | 1.79e-3 |
| 192 | 274.180597 | 2.722e-4 | 6.1e-8 | 6.13e-4 |
| 256 | 274.958191 | 1.601e-4 | 2.3e-8 | 4.81e-4 |
Residual force ~2000x smaller than force response to unit-norm perturbation, shrinking with N.
Gradient overlap with doublet ~1e-8..1e-10; with isolated mode 1.09e-3/2.53e-4/5.24e-5 -> implied
Newton displacement ~4.0/3.2/1.6 global-L2 units (per-site angles ~1e-3 rad), shrinking with grid,
does not move lambda at 1e-3 level. Unit-norm to 2e-16; pinning exact.

## CHECK 2 — EIGENPAIR AUDIT (seed-0, all grids): PASS with one scoped finding
- Independent HVP reproduces every file eigenvalue to <=2e-9 (256: 0.2508821344/0.2508821363/0.3226095628).
  Operator symmetric to rel 1.6e-9; doublet Gram asymmetry <=1.3e-15.
- Hygiene: ||v||=1 to 1e-12; tangency ~1e-19; outer 2 layers exactly zero; |<v,u1>|<=3e-18;
  max T/R overlap <=3.5e-17; doublet orthogonality ~5e-18.
- Isolated: RAW backward error 3.60e-5 / 7.22e-5 / 7.37e-4 — raw-converged.
- KEY FINDING — doublet: RAW backward error 3.34e-2 / 3.38e-2 / 3.36e-2 (grid-independent); the 2x2
  invariant-subspace residual same 3.4e-2; residual lies almost entirely in the 6-dim T/R span —
  projecting only that span out drops it to 5.7e-4..1.1e-3, matching file eta_c (~8.3e-4).
  The doublet is converged as an eigenpair of the T/R-DEFLATED operator, not of the raw operator.

## CHECK 3 — INDEPENDENT NEGATIVE-MODE HUNT (N=128): PASS-for-(A)
Own LOBPCG ([X,W,P] Rayleigh-Ritz) + own FFT diagonal preconditioner; 2 independent random starts;
2 deflation variants; operator symmetry verified rel 3.8e-10.
- Genuine subspace (u1+6 T/R deflated), 30 iters: floor = +0.2529, +0.2530, +0.3211 with overlaps
  0.999/0.999/1.000 vs file vectors; next +0.484/+0.486/+0.545. Ritz values are variational upper
  bounds; the 706 -> 0.25 descent found no lower basin.
- Full space (only u1 deflated), 36 iters: lowest 5 = +0.0029..+0.024, ALL POSITIVE, s_TR=0.97-1.00;
  above them the same doublet (+0.2542/+0.2543) and isolated (+0.3209, overlap 1.000).
- Exact 15-dim Rayleigh-Ritz over span{u1, 6 T/R, 8 hunt vectors}: ALL positive — lowest u1 +0.00208,
  then T/R cluster +0.0029..+0.022, then +0.2542/+0.2543/+0.3209.
- Lowest RQ found anywhere: +0.00208 (exact U(1)); lowest non-u1: +0.0029 (s_TR=0.997).
  NO direction with RQ<+0.2 outside symmetry/pseudomode span; NO negative RQ found anywhere.
- Perturbation bound: doublet<->T/R coupling ~1.7e-2 -> second-order shift ~(1.7e-2)^2/0.245 ~ 1.2e-3.
  Full-space doublet = 0.2509 +/- ~1e-3 — positivity unthreatened.

## CHECK 4 — FD-STEP SANITY: PASS
256^3 doublet member 0: lambda = 0.250882134435/0.250882134441/0.250882134440 at eps=5e-5/1e-4/2e-4.

## CHECK 5 — ARITHMETIC/RICHARDSON: values match; h^2-purity does NOT
Table matches file contents exactly. Fine-pair Richardson: doublet 0.24977, isolated 0.32270
(3-pt h^2+h^4: 0.24943, 0.32232). FLAG: not pure h^2 (slope ratios 0.47 / 8.0). Cross-seed principal
cosines = 1.0 to 1e-8 — seeds converged to identical vectors (fixed-point check, not independent).

## OVERALL: evidence supports (A); amendments: (i) doublet convergence T/R-deflation-scoped
(raw 3.4e-2, wholly T/R-coupled; bound => 0.2509 +/- ~1.2e-3); (ii) impure h^2 (~1e-3 systematic);
(iii) seeds not independent evidence (the hunt is). NOT checked: hunts at 192/256; T/R cluster floor
below ~+3e-3 (unconverged; >=97% translation/rotation of the pinned box = boundary class).
