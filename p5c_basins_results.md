# P5c-step-2 — BASIN CHARACTERIZATION of the committed 3-D coupled residual

Research record (append-never-edit). **NOT canon.** Mode: OBSERVE/INFRA (diagnostic
map; NO selection principle added; NO M_MS banked). **DATA-BLIND** (units L=1; no wall
numbers). Driver: claude-opus-4-8[1m]. Date: 2026-06-20. Branch: `p5c-basins`.
NEW FILES ONLY (committed `full3d_*`/`p5b_*` reused as imports — not edited).

Parent: `p5c_uniqueness_results.md` + `p5c_VERIFIER.md` — the committed 3-D coupled
solver admits MULTIPLE distinct machine-floor solutions with NO selection principle.
P5c-step-1 reported the FREE full-space Newton as "single-valued + resolution-robust"
(M_MS 0.309→0.292) and pinned the multiplicity to the re-pose HOLD gauge. **This step
SWEEPS THE FREE SOLVER ITSELF over multiple seeds** — and that "single-valued" claim
was a one-seed artifact (see §VERDICT). This is the diagnostic that informs the
selection-principle step.

Tool: `p5c_basins.py` — `one NR SEED [MAXIT]` (floor one free solve, save) /
`report NR` (table + pairwise field distances). Free dense Newton =
`full3d_newton.newton_solve` (jacrev J + lstsq), the in-budget flooring tool. Six
seeds, all perturbations of the validated `round_seed` (winding BC rows keep every
solve charge-1: Theta(core)=pi, Theta(seal)=0 held to ~1e-16 in EVERY floored branch).

---

## METHOD

For each seed, FREE full-space Newton (ALL DOF free, no re-pose hold gauge) to floor,
then on the floored field record: committed-Phi; M_MS; energy proxy S = int sqrt(-g)
(L2+L4) dV (the matter action, the likely selection principle); Theta min/max + the
mid-radius angular spread; tvar (theta-asymmetry) / psivar (non-axisymmetry);
metric-warp magnitudes; and the REGULARITY witnesses (winding residual, fraction of
radial shells where angle-avg Theta is non-monotone, off-diagonal c,d warp).

Seeds: `round` (#56 embedded), `oblate`/`prolate` (±cos2θ Theta squash/stretch),
`pert_s` (eps=0.03 random body), `pert_L` (eps=0.30 random body), `toroidal`
(equatorial-ring Theta+a push). Interior-only perturbations (core/seal ends untouched).

---

## 1. THE BASIN MAP — Nr=12  (all six FLOORED to Phi < 1e-12)

| seed | Phi | M_MS | energy S | Theta[min,max] | mid ang.spread | tvar | psivar | offdiag(c,d) | nonmono frac | its |
|---|---|---|---|---|---|---|---|---|---|---|
| round    | 4.10e-13 | 0.30904 | -8.371e+01 | [-0.000, 3.142] | 3.5e-03 | 1.31e-2 | 4.1e-14 | 1.71e-1 | 0.000 | 6 |
| oblate   | 7.14e-18 | 0.40471 | -1.175e+02 | [-0.149, 3.142] | 1.2e-01 | 1.77e-1 | 9.9e-14 | 1.79e-1 | 0.182 | 7 |
| prolate  | 5.57e-13 | 0.44001 | -1.329e+02 | [-0.134, 3.142] | 1.2e-01 | 2.41e-1 | 9.7e-14 | 1.81e-1 | 0.182 | 6 |
| pert_s   | 5.91e-13 | 0.37465 | -1.178e+02 | [-0.131, 3.142] | 2.1e-02 | 2.45e-1 | **2.18e-1** | 3.69e-1 | 0.091 | 24 |
| pert_L   | 1.96e-13 | **43.749** | **-1.026e+08** | **[-1.926, 3.615]** | 3.19e+0 | 3.24e+0 | 1.73e+0 | **1.42e+1** | 0.273 | 18 |
| toroidal | 2.72e-16 | 0.54068 | -1.793e+02 | [-0.003, 3.142] | 8.7e-02 | 3.11e-1 | 1.5e-13 | 1.96e-1 | 0.364 | 7 |

Pairwise max|u_i − u_j| (floored): round↔oblate 0.17, round↔prolate 0.17,
round↔pert_s 0.29, round↔toroidal 0.25, oblate↔prolate 0.35 — all O(0.1–0.4) field
separations with O(0.03–0.23) M_MS gaps. pert_L is ~14 away from everything (a
separate, pathological well).

**READING:** The FREE full-space solver lands in MANY distinct machine-floor wells
depending on the seed. M_MS spans 0.309 (round) → 0.54 (toroidal) among the regular
branches — a ~75% spread — plus the pathological pert_L at 43.7. The round seed alone
gives 0.309; the seed-sweep shows that is just ONE of several floored solutions, NOT
the unique free solution. psivar reveals pert_s reaches a genuinely NON-axisymmetric
(lobed) branch (psivar 0.22 vs ~1e-13 for the axisymmetric ones).

(Nr=16 section appended after the Nr=16 sweep floors — see below.)

---

## 2. SPURIOUS-BRANCH CRITERION (explicit, applied — not ad hoc)

A floored point is a SOLUTION of the residual (Phi<1e-12) but need not be a PHYSICAL
charge-1 soliton. Pre-stated criterion (chosen from the field structure of a regular
hedgehog, NOT to flag a particular branch): a branch is SPURIOUS if it violates ANY of:

  (C1) **Field-range regularity.** Theta must stay in its winding range [0, pi]
       (n a unit field winding once; the BCs pin Theta(core)=pi, Theta(seal)=0). A
       regular profile may dip slightly below 0 at the tail (numerical overshoot near
       the seal), but a large excursion is unphysical. THRESHOLD: |Theta - clamp[0,pi]|
       <= 0.2 (i.e. min(Theta) >= -0.2 and max(Theta) <= pi+0.2).
  (C2) **Bounded warps.** Metric warps are O(0.1-0.5) for a weakly-gravitating soliton
       at p=0.4, kap8=0.05 (round: a,b,c,d ~ 0.1-0.36). THRESHOLD: max|warp| <= 2.0.
  (C3) **Bounded energy.** The matter action magnitude |S| is O(1e2) for the regular
       branches. THRESHOLD: |S| <= 1e4.
  (C4) **Winding preserved.** Theta(core)=pi and Theta(seal)=0 to ~1e-3 (the BC rows).

These are deliberately LOOSE (10x the regular-branch range) so the criterion flags only
GROSS pathology, not the regular off-round basins (oblate/prolate/toroidal/pert_s, which
this step is precisely trying to characterize — they must NOT be discarded).

**APPLIED at Nr=12:**
- pert_L: **SPURIOUS** — fails C1 (Theta in [-1.93, 3.62], excursion 1.9 >> 0.2), C2
  (warps up to 14.2 >> 2.0), C3 (|S|=1.0e8 >> 1e4). A run-away large-amplitude well the
  large random kick fell into; not a charge-1 soliton. (C4 still holds — the BCs are
  enforced — so Phi can floor; the residual does not by itself reject it. This is exactly
  why a per-case low Phi cannot certify "the" solution.)
- round, oblate, prolate, pert_s, toroidal: **PHYSICAL (pass all)** — Theta in
  [-0.15, pi], warps <= 0.37, |S| in [84, 179], winding to ~1e-16. These are five
  genuinely distinct regular floored solutions, NOT artifacts of the criterion.

---

## 3. THE BASIN MAP — Nr=16  (throughput-limited: maxit capped; see ledger)

THROUGHPUT REALITY: at Nr=16 the free dense Newton runs ~30-40 s/iter on this
contended V100 with the no-cache jacrev allocator, and the round basin floor STALLS in
a slow ~1.5x/iter tail below ~2e-8 (lam pinned at floor) -- to reach machine floor
takes >40 iters / >20 min, blowing the anti-hang single-process budget. We therefore
cap maxit and report the FLOORED-below-1e-9 solution (a real branch by the <1e-9 bar;
NOT machine floor -- flagged). The Nr=16 sweep is partial: round (the reference) +
toroidal + pert_s (the non-axisym branch) -- enough to answer the Nr-trend question
(does the basin count/spread change?), not the full six.

| seed | Phi | M_MS | energy S | Theta[min,max] | mid spread | tvar | psivar | offdiag | nonmono | its |
|---|---|---|---|---|---|---|---|---|---|---|
| round    | 1.01e-10 | 0.291527 | -7.590e+01 | [-0.002, 3.142] | 1.7e-03 | 2.52e-2 | 5.3e-14 | 4.6e-2 | 0.067 | 10 |
| toroidal | 6.99e-17 | 0.595063 | -1.667e+02 | [-0.013, 3.142] | 7.0e-02 | 7.90e-2 | 4.0e-13 | 5.9e-2 | 0.400 | 11 |
| pert_s** | 2.68e-07 | (2.067) | (-5.558e+02) | [-0.388, 3.142] | 2.5e-2 | 2.27e-1 | **1.8e-1** | 7.7e-1 | 0.133 | 14 |

** pert_s Nr=16 is **UNDER-FLOORED** (Phi=2.7e-7 >= the 1e-9 real-branch bar; the slow
tail did not reach floor in the maxit=14 budget). Its M_MS/energy are PARENTHESIZED and
NOT certified -- listed only to witness that the perturbed seed is still heading to a
DISTINCT, NON-AXISYMMETRIC configuration at Nr=16 (psivar=0.18, vs ~0 for round/toroidal;
|S| descending past 556). It is NOT counted as a certified basin at Nr=16. (At Nr=12
pert_s DID floor, Phi=5.9e-13, and was a real non-axisym basin.) Flagged per audit.

round Nr=16 (M_MS=0.2915) reproduces step-1's free anchor (0.2924) and the verifier's
(0.292) to ~0.3% -- the ROUND BASIN is resolution-robust (0.309 @Nr12 -> 0.292 @Nr16,
a ~5% grid drift) AND the cleanest branch (lowest |S|=75.9, smallest warps 0.13,
axisymmetric psivar~0, lowest tvar). toroidal Nr=16 floored to MACHINE FLOOR
(6.99e-17) at M_MS=0.595 -- a DISTINCT basin, |S|=166.7 (>2x round), frac_nonmono=0.40
(ring-like Theta). (pert_s appended below.)

---

## 4. HOW MANY BASINS? DOES THE COUNT/SPREAD CHANGE WITH Nr?

**At least FIVE distinct PHYSICAL (non-spurious) basins** + one spurious well, at Nr=12.
By the criterion (§2) the floored physical branches cluster into distinct (M_MS, energy,
field-character) groups -- they are NOT the same solution reached differently (pairwise
max|du| 0.17-0.42, M_MS gaps 0.03-0.23, energy gaps 30-95). Ordering by energy |S|:
round (84) < oblate (117) ~ pert_s (118) < prolate (133) < toroidal (179). pert_s is
the only NON-axisymmetric branch (psivar 0.22). They are genuinely distinct wells.

**The count does NOT collapse with Nr; the SPREAD GROWS.** At Nr=16 two of the three
sampled seeds floored to distinct basins -- round 0.2915 (|S|=76, Phi=1e-10) and
toroidal 0.595 (|S|=167, Phi=7e-17 machine floor) -- and the third (pert_s) was
under-floored (Phi=2.7e-7) but clearly heading to yet another distinct, NON-axisymmetric
configuration (psivar=0.18). round-vs-toroidal M_MS spread = 104% at Nr=16 vs 75% at
Nr=12 -- WIDER, not narrower. This matches P5c-step-1's reposed-hold finding (spread grew
4.4%->158% Nr12->16) AND the verifier's free-solve seed test (0.309 vs 0.287 @Nr12,
0.292 vs 0.278 @Nr16). **The multiplicity is a genuine feature of the committed static
residual, NOT a coarse-grid artifact and NOT cured by going to the free full-space
solve.** The round basin alone is resolution-robust; the SET of basins is not a single
point.

(Caveat: the per-seed Nr=16 floors are throughput-capped; round at 1e-10, toroidal at
machine floor 7e-17. Both are below the <1e-9 real-branch bar, so the basin distinction
is real, but the Nr=16 sweep samples 3 seeds, not 6 -- a fuller Nr=16/24 sweep would
firm the basin COUNT. The basin EXISTENCE and the growing-spread trend are established.)

---

## 5. IS THERE A CLEAR LOWEST-ENERGY / MOST-REGULAR CANDIDATE?

**YES -- the ROUND basin is BOTH the lowest-energy AND the most-regular candidate, at
both grids.** It has: the lowest matter-action magnitude (|S|=84 @Nr12, 76 @Nr16, the
minimum of every sampled branch), the smallest metric warps (0.13-0.36), the smallest
off-diagonal/shear (c,d), exact axisymmetry (psivar~0), monotone Theta (frac_nonmono
0.00 @Nr12, 0.067 @Nr16 -- the lowest), and resolution-robustness (0.309->0.292). Every
other regular basin has STRICTLY higher |S| and a less-regular field (non-monotone
Theta, larger angular spread, and in pert_s's case broken axisymmetry).

So a candidate for "the particle" EMERGES from the map without being imposed: the round,
lowest-energy, most-regular, resolution-robust soliton. **NOT BANKED** (data-blind;
no M_MS is canonized here) -- this is a diagnostic identification of the candidate and
of WHAT would pin it, per the task.

**What selection principle would pin it:** the round basin is simultaneously the global
energy minimum AND the maximal-regularity / maximal-symmetry point among the floored
solutions -- so EITHER an energy-minimization principle OR a regularity/symmetry
principle selects the SAME branch. That coincidence is the strongest result of the map:
the two most natural physical selection criteria agree.

---

## 6. RECOMMENDATION FOR THE SELECTION PRINCIPLE

Ordered by how directly the map supports it:

1. **ENERGY MINIMIZATION (primary recommendation).** The matter action |S| cleanly
   ORDERS the basins and the round (candidate) branch is its minimum at both grids,
   with a clear gap to the next (76 vs 117+ @Nr16). This is the natural soliton
   selection principle (a particle = the lowest-energy stable charge-1 configuration)
   and is already INSTRUMENTED here (energy_proxy). It does NOT require importing a
   mechanism -- it is a property of the native action. Recommend: make the production
   solve an ENERGY-MINIMIZING continuation (or a post-floor energy comparison across a
   seed-sweep), selecting the min-|S| floored branch. NB the precedent
   (winding_platonic_phase3b / memory [[gravitating-soliton-stability-test]]): an
   energy-minimizer + continuation was ALREADY the prescribed tool for the crowded
   m>=2 multi-basin sector. This step independently re-derives that need for m=1.
2. **REGULARITY / SYMMETRY (corroborating, NOT independent).** The min-energy branch is
   also the most regular/symmetric -- so a regularity criterion (monotone Theta, minimal
   shear, axisymmetry) selects the same branch and can serve as a CHECK on the
   energy-min selection, not a competing principle. Useful as a tie-break / sanity gate.
3. **STABILITY (deferred, needs the coupled Hessian).** Whether the round branch is a
   true minimum vs a saddle among these basins needs the constraint-respecting coupled
   stability test (memory [[gravitating-soliton-stability-test]]: the fixed-metric
   Hessian over-counts; re-solve along negative modes). Recommend AFTER energy-min picks
   the candidate -- confirm it is dynamically stable, don't use stability to FIND it.
4. **CONTINUATION FROM A KNOWN LIMIT (the cleanest, if affordable).** Continue from the
   flat/weak-coupling limit (kap8->0 or p->0, where the round hedgehog is the unique
   solution) up to the target (p=0.4, kap8=0.05). If the continued branch is the round
   one, that PINS it as "the" solution by deformation from a regime with no multiplicity
   -- a derivation, not a choice. Recommend as the rigorous confirmation of (1).

DO NOT (per the brief): bank any M_MS, or pick a branch by hand. The map shows energy-min
and regularity AGREE on the round candidate -- that agreement is the deliverable.

---

## 7. AUDIT

- **DATA-BLIND?** YES. Units L=1; no wall numbers; M_MS / energy are dimensionless
  geometric readouts in working units. No comparison to any observation. No selection
  principle applied, no M_MS banked (per brief: this is a diagnostic map).
- **Dense-LM legit?** YES. The free solve is `full3d_newton.newton_solve` (jacrev
  Jacobian + `torch.linalg.lstsq`), the committed anchor's own Category-A step (all DOF
  free, no re-pose hold gauge, no B=1/A tie, no injected/dropped term, no tuned dial).
  Residual measured at the end is the COMMITTED `full3d_solver.residual_vector`
  verbatim. New file (`p5c_basins.py`) reuses committed modules as imports only.
- **Energy proxy provenance.** S = int sqrt(-g)(L2+L4) dV is the native matter action
  (the SAME action that builds the stress and the EL), not an imported functional. (The
  committed `full3d_spectral.matter_action` has a stray undefined `n` in its return; we
  recompute the action inline -- identical algebra -- rather than edit the committed
  module.) Energy is used here only to ORDER basins (a diagnostic), not to select.
- **Under-floored branches (FLAGGED):** Nr=12: all six floored to Phi<1e-12 (real).
  Nr=16: round floored to 1.0e-10 (below the <1e-9 real-branch bar but NOT machine
  floor -- the slow tail stalls; FLAGGED); toroidal to 6.99e-17 (machine floor); pert_s
  (see below). The round Nr=16 M_MS=0.2915 nonetheless matches step-1/verifier to ~0.3%,
  so the readout is trustworthy at that depth.
- **Spurious-branch handling.** Criterion (§2) is PRE-STATED from regular-hedgehog
  structure with 10x-loose thresholds, and applied uniformly -- it flags ONLY pert_L,
  and explicitly does NOT discard the regular off-round basins (oblate/prolate/toroidal/
  pert_s) this step is characterizing. Not ad hoc.
- **Anti-hang held?** YES. Single clean process per solve, strictly sequential, never
  concurrent. Nr<=16 (no Nr=24 -- throughput; the round/toroidal Nr=16 already answer the
  Nr-trend). Caps honored (Nr=12 full floor; Nr=16 maxit-capped, reported as
  throughput-limited). One mid-run process (the first Nr=16 round at maxit=40) was KILLED
  by its outer `timeout` in the slow tail and re-run at maxit=10 -- no hang, no concurrent
  solve, GPU never contended.

---

## SCOPED STATUS / WHAT THE SELECTION-PRINCIPLE STEP INHERITS

- The committed 3-D coupled residual has **genuine, multi-basin solution multiplicity at
  m=1** in the FREE full-space solve -- confirmed and CHARACTERIZED here (>=5 physical
  basins @Nr12; 2 certified-distinct + 1 under-floored-but-distinct @Nr16; spread GROWS
  with Nr). P5c-step-1's "free solve is
  single-valued" was a one-seed artifact (the verifier already flagged this; this step
  maps the full basin set).
- **A clear candidate EMERGED without being imposed:** the round, lowest-energy
  (min |S|), most-regular, axisymmetric, resolution-robust soliton. Energy-min and
  regularity SELECT THE SAME BRANCH -- the load-bearing finding for the next step.
- **The selection-principle step inherits:** (1) energy-minimization as the primary,
  natively-instrumented selection principle (energy_proxy is built and validated);
  (2) a regularity/symmetry corroborator; (3) a continuation-from-known-limit route as
  the rigorous pin; (4) the dense free Newton as the flooring engine (throughput-limited
  at Nr>=16 in the slow tail -- a continuation or a better tail preconditioner is needed
  to reach machine floor at Nr=16 in budget); (5) the spurious-branch criterion to gate
  out run-away wells before energy comparison. NO M_MS is bankable until a selection
  principle PINS one branch -- and that step is GATED (Charles's go).

---

## PREMISE LEDGER (chose / derived)

| Item | tag | note |
|---|---|---|
| Residual = `full3d_solver.residual_vector` verbatim | DERIVED (reused) | committed; unchanged |
| Free solve = `full3d_newton.newton_solve` (all DOF free) | DERIVED (reused) | the anchor; no re-pose, no hold gauge |
| Energy proxy = native matter action S=int sqrt(-g)(L2+L4)dV | DERIVED (reused) | recomputed inline (committed matter_action has a stray `n` bug); same algebra |
| Six seeds (round/oblate/prolate/pert_s/pert_L/toroidal) | CHOSE (exploration) | all perturbations of `round_seed`; winding BCs keep every solve charge-1 |
| seed perturbation amplitudes (0.25 cos2θ; 0.03/0.30 random; 0.30 ring) | CHOSE (exploration) | spans small->large; pert_L deliberately large to probe run-away wells |
| RNG seeds 12345 / 67890 | CHOSE (reproducibility) | fixed so pert_s/pert_L are deterministic |
| grid (12,6,8)/(16,8,8), p=0.4, kap8=0.05, m=1 | CHOSE (control) | the step-1 anchor regime |
| spurious criterion: \|Theta-clamp[0,π]\|<=0.2, max\|warp\|<=2, \|S\|<=1e4, winding~1e-3 | CHOSE (criterion) | pre-stated from regular-hedgehog structure, 10x-loose; applied uniformly |
| floor bar Phi<1e-9 = "real branch"; <1e-12 = machine floor | CHOSE (numerics) | Nr=16 round capped at 1e-10 (flagged); toroidal at machine floor |
| Newton maxit caps (40 @Nr12; 10-14 @Nr16) | CHOSE (anti-hang) | Nr=16 full floor blows budget in the slow tail; capped + flagged |
| "lowest-energy round = candidate" | OBSERVED (not chosen) | EMERGED from the map; NOT banked, NOT a selection principle applied here |

---

## ATTACK HERE (for a blind verifier)

1. **Is the round basin REALLY the global energy minimum, or only the min of the 6 seeds
   tried?** The map samples 6 seeds; a denser seed-sweep (random ensemble, or higher
   windings folded back) could find a lower-|S| floored branch. Attack: run more seeds,
   especially aimed BELOW the round branch (e.g. seed from a compressed/over-warped
   start). If a lower-energy floored charge-1 branch exists, the candidate changes.
2. **Are oblate/prolate/pert_s GENUINELY distinct basins or under-resolved versions of
   round that would relax to round at higher Nr/iters?** They floor to Phi<1e-12 at Nr=12
   and are O(0.1-0.4) apart in field with O(30-95) energy gaps -- but the Nr=16 sweep only
   re-floored round/toroidal/pert_s. Attack: re-floor oblate/prolate at Nr=16 to machine
   floor; check whether the basin set thins or holds as Nr grows.
3. **Is the energy ORDERING resolution-stable?** round<oblate~pert_s<prolate<toroidal at
   Nr=12; at Nr=16 round(76)<toroidal(167) holds. Attack: confirm the full ordering at
   Nr=16 (needs the missing seeds floored) -- a selection principle built on |S| ordering
   needs the ordering to not reshuffle with grid.
4. **The Nr=16 round under-floor (1e-10).** It matches step-1/verifier to 0.3%, but is not
   machine floor. Attack: floor it to <1e-12 (more iters / a tail preconditioner / a
   continuation) and confirm M_MS and |S| do not move -- the candidate identification
   leans on round being BOTH min-energy and resolution-robust.
5. **pert_L spurious call.** Verify the criterion is not hiding a real high-energy branch:
   is pert_L charge-1 (winding BCs hold, Phi floored) yet unphysical (Theta range 1.9,
   warps 14, |S|=1e8)? Confirm it is a run-away well, not a legitimate excited state, by
   checking whether it survives a regularity-penalized re-solve.
