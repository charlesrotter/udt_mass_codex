# Sealed Cavity — Stage S2 (Compact-Domain Mode Problem) Results

Status: working audit, not canonical. Created: 2026-06-11. Process:
S2 derivation agent + collector/continuation agent (the production
solve outlived the first session; collector found and fixed a sign
bug, re-ran refined stages, preserved as-run artifacts), then a blind
adversarial verifier (VS2: 44 checks, 39 adjudicated PASS, 0 package
refutations; independent FEM + shooting + exact-Bessel adjudication;
~54,000 GPU-batched eigensolves in the hostile mode hunt). New files
only. DATA-BLIND throughout.

## What was solved

Per formed-cavity background (M1/M2/M4, M3 probe; S1 library) and per
azimuthal block m = 0..3 (channels ell = m..3), the compact-domain
generalized eigenproblem in t = ln(1/y) on [0, t_b]:
A u = sigma B u, A = -(e^{-t}u')' + 2 e^{-t} H^{(m)}(t) u,
B = e^{-3t} G^{(m)}(t), omega^2 = -sigma (the H1-elimination flip).
H^{(m)} = exact second variation of the reduced potential (full
ell-ell' coupling; S1's x2 amendment verified in place). Time weights
W_A = <R R'/f^2> (licensed primary) and W_B = <R R'/f^3>
(hypothesis-grade) carried in parallel. Outer BC: the weld jet + the
banked exterior DtN D_+ (bracketed [0.5x, 2x] + Dirichlet/Neumann).
Inner BC at the trust-boundary stand-in t_b for the seal: the FORCED
v-hat Dirichlet (S1) + the one-parameter Robin family (h = cot theta)
on every other direction, scanned over 15 points.

## VERDICT (as amended by VS2)

NO NATIVE DISCRETENESS FROM THE SEALED CAVITY'S BULK — and the
"bulk cannot ring" leg is now THEOREM-GRADE ON THE FULL SEALED
INTERIOR:
1. STRUCTURAL THEOREM (VS2-strengthened): H^{(m)}(t) is pointwise PSD
   wherever f > 0 — not merely on the trust domain — because
   |grad_Omega f|^2/f is the perspective of a quadratic, jointly
   convex for f > 0 (verified on 48,000 grid points to the
   f_min = 0.002 cutoff; the m=0 zero floor is the exact homogeneity
   kernel). M_out is PSD over the whole outer bracket.
   sigma_min(h) is strictly monotone decreasing in h (analytic +
   numeric, all 12 blocks). Hence omega^2 > 0 occurs IFF the inner
   boundary is attractive beyond a positive threshold (h > h_c > 0):
   the interior cannot produce oscillation. Conditional on: the
   ell<=3 reduced model and the derived time weight.
2. FOR THE ENTIRE FAMILY h <= h_c: a PURE RELAXATION LADDER
   (omega^2 < 0), robust across both weights, the full outer bracket,
   and the stand-in placement (<= 2.3% under t_b 1% -> 5%). The
   lowest rungs (h = 0, W_A, banked D_+, weld units), all
   verifier-reproduced to <= 5e-6:
   M1 m=0: -7.057579, -16.193966, -28.772125, -44.662375
   M2 m=0: -7.134399, -16.362024, -28.699050, -44.637223
   M4 m=0: -4.238126, -12.546068, -24.160764, -38.714955
   (full 4-member x 4-block x 4-rung tables in the S2 logs;
   /tmp/seal_s2/ archives). Ladder character: tracks the weld jet
   (gamma), NOT the cavity scale; c-independence clean for M1<->M2,
   ~10% for the thin-trust M3 probe; higher-m rungs
   centrifugal-dominated, near-member-universal. NO SCALE AUTONOMY
   anywhere.
3. THE COMPUTED POSITIVE MODES (h > h_c) ARE ARTIFACTS OF THE
   TRUNCATION SURFACE — they collapse under the LOCAL stand-in
   boundary scale (leading-order; spread 1.044x across members vs
   6.6x raw) and move 394-1152% when the stand-in is relocated while
   the ladder moves <= 2.3%. AMENDED SCOPE (binding, VS2): whether
   the TRUE seal supports its own surface-trapped sector
   (theta-dependent, seal-scale) IS NOT DECIDABLE FROM THE STAND-IN —
   the h > h_c sector is undecided at the true seal, not empty. The
   attractive third of the real, unselected theta-family does ring at
   the stand-in.
4. THE WEIGHT FORK IS LOAD-BEARING EXACTLY HERE (VS2-confirmed
   endpoint classifications): under W_A (licensed) the theta-family
   survives at the seal in every non-forced channel — a physical
   degree of freedom of sealed cavities with NO native selector found
   in S2; under W_B (hypothesis) the m=1 endpoint is limit-point and
   the BC is FORCED. The two weights agree on every S2 sign/structure
   result and disagree ONLY on the m=1 endpoint class at the true
   seal. (The measure-fork push, running, owns the resolution.)
5. Hostile mode hunt (VS2): 504 GPU + 24 CPU configurations over
   h <= 0 x 7 outer conditions x both weights x all members/blocks —
   no missed positive mode (global min at the pure-Neumann
   homogeneity soft mode, positive as the theorem requires).

## Incident record (process integrity)

- Sign bug in the original s2_solve.py shooting refinement (roots =
  negated eigenvalues): diagnosed by the collector, adjudicated
  DECISIVELY by VS2 against the exact Bessel solution of the
  constant-coefficient case; one-line fix; FEM outputs unaffected;
  as-run artifacts preserved.
- A concurrent edit to s2_sens.py during the inter-session gap was
  cross-checked number-by-number by the collector and re-verified by
  VS2 (the -61.0487 provenance pinned: it is sigma at FEM N=300;
  omega^2 = +61.0516 by independent shooting).
- VS2 found a GPU-stack bug IN ITS OWN HARNESS (torch batched
  solve_triangular with broadcast Cholesky factor silently corrupts
  at large batch on this V100/cu121 stack) — diagnosed, fixed,
  re-run clean. Recorded in CLAUDE.md's GPU note as a standing
  pitfall.
- Wording amendments (VS2): t_b robustness "<= 2.3%"; M3
  c-independence ~10% (probe-grade); the quarantined ladder ratio
  6.257 (rounding). The near-10 collapse triple {9.787, 9.999,
  9.575} and ladder ratios remain UNCLAIMED (null discipline).

## Consequences

- Registry entry #1 (open-domain empty-point-spectrum suspension):
  PARTIALLY RESOLVED — the bulk/interior question for formed cells is
  settled (no interior discreteness; relaxation only; the convexity
  theorem extends the silence to every sealed interior in the class).
  WHAT REMAINS OPEN is precisely the seal-surface BC sector: the
  theta-family under W_A (or the forced BC under W_B) at the true
  seal. The suspension narrows to that sector.
- The discreteness search after S2: (i) the true-seal surface sector
  (gated on the W_A/W_B fork resolution + a native theta-selector or
  controlled seal asymptotics); (ii) ENSEMBLES (collective modes —
  the leading linear candidate; Charles-ordered next); (iii) the
  nonlinear/nonstationary sector. The measure-fork push (running)
  gates (i) and feeds the dressed operator (the half-2 result: the
  native completion's derived H1^2 loading must enter the assembled
  operator — neither S2 weight candidate included it; S2's
  sign-structure robustness across W_A/W_B bounds the expected
  impact, but the completed operator is the honest final form).

## Verifier record

VS2: blind pass 2026-06-11; independent backgrounds, blocks (2D
sphere-quadrature FD Hessian incl. the phi-sector), vector-P1 FEM
(different quadrature), opposite-direction shooting, exact-Bessel
sign adjudication, own r-coordinate weld anchors; 44 checks, 39 PASS,
0 package refutations (5 verifier-side fails, incl. its own torch
bug, all resolved); ruling SURVIVES WITH AMENDMENTS (all incorporated
above).
