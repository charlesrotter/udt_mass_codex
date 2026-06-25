# P5c-step-2 BASIN CHARACTERIZATION — BLIND ADVERSARIAL VERIFIER

Verifier: claude-opus-4-8[1m] (independent, DATA-BLIND). Date: 2026-06-20.
Branch: `p5c-basins`. Method: RECOMPUTE-ON-SAVED-FIELDS (no re-solve; anti-hang
held — single sequential reads of the 9 `/tmp/p5c_basin_*.pt` floored
checkpoints, never a solve, never concurrent, never backgrounded). Energy was
recomputed with my OWN evaluation assembled from the committed primitives
(`build_metric`/`metric_inverse`/`field_dn`/`MAT.field_metric`/`MAT.lagrangian`),
NOT by importing the agent's `energy_proxy`. Residual recomputed via the
committed `residual_vector`. Pairwise distances recomputed independently.

## HEADLINE

(a) **ENERGY ORDERING — CONFIRMED, round IS the energy minimum.** My independent
action recompute matches the agent's recorded S to **machine zero (reldiff =
0.00e+00) on ALL 9 saved fields** (6 @Nr12, 3 @Nr16). Ordering @Nr12:
round(84) < oblate(117) < pert_s(118) < prolate(133) < toroidal(179) — round is
the clear minimum, 39% gap to the next. @Nr16: round(76) < toroidal(167) <
pert_s(556, under-floored) — round still the minimum, 2.2x gap to toroidal.
The committed-`matter_action` bug is REAL and the workaround is CORRECT (see §1).

(b) **ENERGY-REGULARITY COINCIDENCE — CONFIRMED on the winner.** round is FIRST
in BOTH the energy order AND my independent regularity order (lowest nonmono,
lowest warp, axisymmetric psivar~5e-14) at BOTH grids. The two criteria pick the
SAME branch (round). NB the MIDDLE of the two orderings differs (energy:
oblate<pert_s<prolate<toroidal; regularity: pert_s<prolate<oblate<toroidal) —
but the agent only claims they agree on the SELECTED branch, and that holds. No
disagreement that would undercut the selection principle.

(c) **BASINS GENUINELY DISTINCT + SPURIOUS CRITERION HONEST — CONFIRMED.**
Physical branches are 0.17–0.42 apart in field, with the separation carried in
Theta itself (max|dTheta| 0.13–0.42), not just gauge warps — genuinely different
configurations, not gauge/seed copies. My pairwise numbers match the agent's
exactly. pert_L is ~14 away (separate well). The spurious criterion is
pre-stated, 10x-loose, applied uniformly, and flags EXACTLY pert_L (next-worst
on every axis is an order of magnitude inside threshold: Theta_min -0.149 vs
-0.2 cut, warp 0.54 vs 2.0, |S| 179 vs 1e4; pert_L: -1.93, 14.2, 1.03e8). Not
over-broad, not discarding an inconvenient branch.

(d) **Nr-TREND SURVIVES the under-floored caveats — CONFIRMED.** round-vs-
toroidal M_MS spread = 75%@Nr12 → 104%@Nr16 (WIDER). toroidal @Nr16 is at
machine floor (6.99e-17), round @Nr16 at 1.01e-10 (honestly flagged
under-floored but matches step-1/verifier 0.292 to 0.3%), pert_s @Nr16 at 2.7e-7
(honestly parenthesized, not counted). The growing-spread / non-collapsing-count
conclusion does not depend on the two soft floors — it rests on the two
distinct, well-separated, certified-or-near-certified basins (round, toroidal).

**NET: SOUND.** The basin map, the round-as-candidate identification, and the
energy-minimization recommendation are all verified. Energy-minimization is a
defensible native selection principle to build next — it is instrumented
correctly (independently reproduced bit-for-bit), it cleanly orders the basins
with a clear gap, and it coincides with regularity/symmetry on the winner. No
over-claim found. No energy-proxy error found.

## DETAIL

### 1. The committed-`matter_action` bug + the workaround
`full3d_spectral.matter_action` (line 270) returns `..., L, n, dn, ...` but `n`
is NEVER defined in the function (it computes `dn = field_dn(...)`, not `n`) —
calling it raises `NameError`. The bug is in the RETURN PACKAGING, not in the
action value `S` itself (line 269 `S = (sqrtg * L * dV).sum()` is correct). The
agent's inline `energy_proxy` reproduces lines 263–269 verbatim (dn → Gmn →
lagrangian → sqrtg(clamp 1e-30) → S = sum(sqrtg·L·dV)). My fully independent
assembly gives reldiff 0.00e+00 vs the agent on all 9 fields → the workaround is
algebraically identical and correct, and the bug does NOT affect any reported
energy or the ordering. The sqrt clamp never activates (nclamp=0, detg_min
~1e-6 > 0 on every physical field), so it distorts nothing.

### 2. Independent recompute table (mine, on saved fields)
Nr=12 (all Phi recomputed < 1e-12, all floored):
  round  S=-8.37153e1  M_MS 0.30904  psivar 4e-14  warp 0.361  nonmono 0.000  Th[-0.000,3.142]
  oblate S=-1.17493e2  M_MS 0.40471  psivar 1e-13  warp 0.373  nonmono 0.182  Th[-0.149,3.142]
  prolate S=-1.32870e2 M_MS 0.44001  psivar 1e-13  warp 0.370  nonmono 0.182  Th[-0.134,3.142]
  pert_s S=-1.17811e2  M_MS 0.37465  psivar 2.2e-1 warp 0.542  nonmono 0.091  Th[-0.131,3.142]
  pert_L S=-1.02559e8  M_MS 43.749   psivar 1.7e0  warp 14.197 nonmono 0.273  Th[-1.926,3.615]  SPURIOUS
  toroidal S=-1.79260e2 M_MS 0.54068 psivar 2e-13  warp 0.373  nonmono 0.364  Th[-0.003,3.142]
Nr=16:
  round  Phi=1.01e-10 S=-7.58973e1 M_MS 0.29153 warp 0.146 nonmono 0.067 (under-floored, flagged)
  pert_s Phi=2.68e-7  S=-5.55765e2 M_MS 2.067   warp 0.889 nonmono 0.133 psivar 1.8e-1 (under-floored, not counted)
  toroidal Phi=6.99e-17 S=-1.66696e2 M_MS 0.595 warp 0.181 nonmono 0.400 (machine floor)
All match `p5c_basins_results.md` §1/§3 exactly.

### 3. Discipline
DATA-BLIND: yes — no wall numbers, no observational comparison, M_MS/energy are
dimensionless working-unit readouts; "round candidate" tagged OBSERVED-not-
chosen; nothing banked. Energy proxy is the NATIVE matter action (committed
`lagrangian`), not imported. round seed = committed `spectral_radial_soliton`
(#56) embedded, not hand-tuned. Dense free Newton (`newton_solve`) is the
committed Category-A anchor step. Anti-hang held (recompute only, no solve).

## RESIDUAL ATTACK SURFACE (not blocking, for the next step)
- The "round = GLOBAL minimum" claim is over 6 seeds only (the agent's own
  attack #1). I confirm round is the min of the 6 SAVED branches; a denser /
  below-round seed ensemble could in principle find a lower-|S| charge-1 well.
  The selection-principle step should run a wider seed sweep before banking.
- The full Nr=16 ordering is established only for round<toroidal (oblate/prolate
  not re-floored @Nr16). The ordering is resolution-stable where sampled; a
  fuller Nr=16/24 sweep would firm it. Throughput-limited, not a defect.
- round @Nr16 at 1e-10 (not machine floor) is honestly flagged; its M_MS/|S|
  match the deeper-floored references, so the candidate identification holds.
These are scope caveats the agent ALREADY stated, not errors.
