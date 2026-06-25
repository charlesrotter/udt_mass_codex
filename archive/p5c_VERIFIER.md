# P5c-step-1 — INDEPENDENT BLIND ADVERSARIAL VERIFIER RECORD

Append-only. **NOT canon.** Verifier: claude-opus-4-8[1m] (independent, DATA-BLIND),
id `udt-verifier-p5c-1781995207`. Date: 2026-06-20. Branch: `p5c-uniqueness` (head
ef2dfd0). Target: `p5c_uniqueness_results.md` + `p5c_runner.py` + `p5c_dense.py`.
Method: independent re-runs (single clean capped processes, never concurrent) of the
SVD-at-seed conditioning, the reposed-hold dense cross-gauge floor, AND — the decisive
new test the report did NOT do — the FREE full-space Newton from MULTIPLE SEEDS.

---

## HEADLINE

**P5c's PERSIST verdict is SOUND (reposed-hold non-uniqueness is real and worsens with
Nr; the P5a'/P5b "spread shrinks → artifact" ruling is REFUTED). But P5c's
LOCALIZATION — "the defect is the re-pose HOLD edge gauge; the FREE full-space solve is
single-valued and the physics/anchor is fine" — is FALSE. The FREE full-space Newton is
ITSELF NON-UNIQUE (seed-dependent basins): independently measured 0.309 vs 0.287 at
Nr=12 (7.1%, both Phi~1e-13) and 0.292 vs 0.278 at Nr=16 (4.9%; round Phi=8.5e-13,
perturbed Phi=5.1e-11 converging). The multiplicity is GENUINE PHYSICAL SOLUTION
MULTIPLICITY in the committed residual, NOT an artifact of the hold-gauge instrument.**

Consequence: P5c's load-bearing conclusion "the metric/physics is fine; use the
free-edge full-space solve as production to bank M_MS" does NOT hold. The free-edge solve
does not rescue uniqueness; M_MS is NOT bankable from EITHER the reposed-hold OR the free
full-space solve at these grids. The forward path P5c recommends (switch to free-edge
full-space dense as the production readout) is built on a refuted premise.

---

## CLAIM-BY-CLAIM (independent re-runs)

### (1) FREE SOLVE SINGLE-VALUED + resolution-robust — **HALF TRUE, the load-bearing half is FALSE.**
Independent FREE `full3d_newton.newton_solve` (all DOF free, NO re-pose, NO hold gauge):

| Nr | seed=round | seed=perturbed | seed spread (rel) |
|---|---|---|---|
| 12 | M_MS=0.309035 (Phi 4.1e-13, 6 its) | M_MS=0.287086 (Phi 9.8e-13, 6 its) | **7.10%** |
| 16 | M_MS=0.292391 (Phi 8.5e-13, 23 its) | M_MS=0.278185 (Phi 5.1e-11, 40 its) | **4.86%** |

- **Resolution-robust (round-seed branch): CONFIRMED.** 0.309→0.292 reproduces the
  report's §3 numbers to 6 sig figs (0.309035, 0.292391). A converging ~5% grid drift.
- **Single-valued: REFUTED.** The report only ran the free solve from ONE (round) seed.
  A smooth body-perturbed seed (0.05·sin(2πrn) on a,b,c,d) lands at a DIFFERENT floored
  solution (0.287 @Nr12 fully floored Phi~1e-13; 0.278 @Nr16, Phi 5e-11 below the
  report's own <1e-9 "floored" bar, still descending at the 40-it cap). The free solve
  has multiple physical basins at BOTH grids. The report's central claim "free is
  single-valued / free stays put" is an ARTIFACT OF NOT TESTING SEED-INDEPENDENCE of the
  free solve. (The report DID seed-test the reposed-hold solve and found basins there —
  but never applied the same test to the free solve it then declared clean.)

### (2) REPOSED-HOLD NON-UNIQUE + WORSENS (PERSIST) — **CONFIRMED.**
Independent dense-LM (`reposed_dense_solve_fast`, jacrev+lstsq), both gauges to floor:

| Nr | G1 Phi / M_MS | G2 Phi / M_MS | dM_MS rel | Theta max\|diff\| |
|---|---|---|---|---|
| 12 | 9.94e-14 / 0.293604 | 8.89e-14 / 0.280614 | **4.42%** | 0.054 (small) |
| 16 | 1.11e-13 / 0.347091 | 2.13e-13 / 0.878034 | **153%** | 2.62 (O(1)) |

Reproduces the report's §2 to scatter (report: 4.42% / Th 0.05 @12; 158% / Th 2.63 @16;
G2-round 0.894 vs my 0.878 = seed/lstsq scatter, immaterial). The reposed-hold floor is
non-unique at machine floor and the spread GROWS Nr=12→16 with the ambiguity migrating
into Theta (O(1)). **PERSIST is real; the "spread shrinks → coarse-grid artifact" ruling
from P5a'/P5b is REFUTED.** CONFIRMED.

### (2b) §0 CONDITIONING (SVD of reposed-J at seed) — **CONFIRMED.**
Independent svdvals of the dense jacrev reposed-J at the round seed:

| Nr | kappa | smin | 2nd-smallest | #SV<1e-3·smax | near-null Theta power |
|---|---|---|---|---|---|
| 12 | 2.306e5 | 6.33e-5 | 1.47e-2 (230× smin) | 1 (ISOLATED) | 0.7% |
| 16 | 4.312e3 | 9.03e-3 | 9.03e-3 (= smin) | 10 (degenerate band) | 0.2% |

Reproduces §2b to all sig figs. The isolated near-null edge mode (the Nr=12
under-determination source) IS gone at Nr=16; conditioning improves 53×. CONFIRMED —
**but** this conditioning-collapse does NOT buy M_MS uniqueness (see §2): they measure
different things (local J at the seed vs global solution dependence on gauge/basin). The
report's own §2b/§2 distinction is correct; the SVD result is not in tension with PERSIST.

### (3) BASIN vs GAUGE — **RULING: it is PHYSICAL BASIN multiplicity, NOT (only) gauge.**
The agent already found the "158%" was partly a basin effect (G2-from-G1-seed → 0.336,
not 0.894). My free-solve seed test settles the deeper question the agent left open: the
FREE solve — which has NO hold gauge and lets the edges relax — ALSO has multiple basins
(7.1% @12, 4.9% @16). Therefore the multiplicity is NOT created by, nor localized to, the
hold-edge gauge. The committed residual `full3d_solver.residual_vector` has GENUINE
PHYSICAL SOLUTION MULTIPLICITY on these grids. The hold gauge adds a FURTHER (gauge) axis
of ambiguity ON TOP (the cross-gauge O(1) Theta blowup is worse than the free-solve basin
spread), but the underlying disease is physical/basin multiplicity that the free solve
does not cure. "Free solve is clean" is therefore FALSE.

### (4) DOES THIS REFUTE P5a' GATE A? — **GATE A was a MATCHED-GAUGE CONSISTENCY CHECK, not a uniqueness proof. Reconciliation holds.**
P5a' GATE A claimed reposed-dense(G2=anchor edges) == free anchor to dM_MS=5.6e-17 at
Nr=12. This is fully consistent with non-uniqueness: in GATE A, G2's held edges were set
TO THE ANCHOR'S OWN EDGES and the body was seeded from the anchor (`set_edge_hold(uref)`
with uref = the anchor's edge rows). Holding the edges at one specific solution's edges
and starting from that solution recovers THAT solution — a tautological round-trip /
consistency check, not evidence of a unique fixed point. It does NOT contradict: (i) the
4.4% cross-gauge spread at Nr=12 between two OTHER regular gauges (§2), nor (ii) the 7.1%
free-solve basin spread (§1). The honest reading: **GATE A proved the re-pose preserves
the anchor IN THE ANCHOR'S OWN GAUGE/BASIN; it never proved uniqueness, and P5a' itself
flagged this as the one open loose thread (its closing OPEN note: "if a future run floors
two regular gauges at Nr=24/40 and the spread does NOT shrink, this ruling flips"). P5c
flipped it.** The P5a' "manifold is an artifact, anchor SOUND" headline is now REFUTED on
its own stated terms (the spread did not shrink; it grew), AND additionally the free
anchor it leaned on is itself non-unique.

### (5) DISCIPLINE — **CLEAN.**
- **Residual verbatim:** independently confirmed `residual_vector_vsafe` (the dense/jacrev
  path's residual) == committed `full3d_solver.residual_vector` to max|diff|=4.4e-16
  (machine zero) at the anchor grid. The committed residual is reused as an import, not
  edited.
- **Data-blind:** yes (units L=1, no wall numbers; M_MS values are dimensionless geometric
  readouts in the working units).
- **Dense-LM legitimate:** yes — jacrev Jacobian + `torch.linalg.lstsq` (rank-revealing,
  min-norm) is the anchor's own `full3d_newton.newton_solve` step, on body DOF. Category-A.
- New files only (p5c_*); committed p5b_*/full3d_* reused verbatim. Append-never-edit honored.

---

## NET (decisive, for the solver plan)

(a) **FREE full-space solve single-valued + resolution-robust?** NO. Resolution-robust on
the round-seed branch (0.309→0.292, reproduced), but NOT single-valued: a perturbed seed
floors to a distinct basin (7.1% @Nr12 both Phi~1e-13; 4.9% @Nr16). The report's
load-bearing claim is REFUTED. The anchor/physics is NOT demonstrably "fine" — the
committed residual admits multiple physical solutions at these grids.

(b) **Reposed-hold non-uniqueness real + worsening (PERSIST)?** YES — independently
reproduced (4.4% @12 → 153% @16, both machine floor, O(1) Theta divergence). The
P5a'/P5b "shrinks → artifact" ruling is REFUTED.

(c) **Basin vs gauge?** PHYSICAL BASIN multiplicity is the primary disease (present in the
gauge-free free solve); the hold-edge gauge adds a further, larger ambiguity on top. The
non-uniqueness is NOT localized to the hold-gauge instrument, contra P5c.

(d) **P5a' GATE-A reconciliation?** GATE A was a matched-gauge/matched-seed round-trip
consistency check, never a uniqueness proof; it does not survive as evidence of a unique
anchor. P5c correctly flips the P5a' artifact ruling — but over-corrects by exonerating
the free solve.

**CORRECT FORWARD PATH (MISMATCH → SOLVER, not mechanism — and the solver is INCOMPLETE):**
The right diagnosis is NOT "use the free-edge full-space solve as production." Both
readouts are non-unique because the committed static residual has a genuine solution
multiplicity at these grids that NEITHER the re-pose NOR the free edges resolve. Before any
M_MS (round or off-round) is banked, the solver must (1) CHARACTERIZE the basins (how many,
what distinguishes them — are the high-Theta / large-amplitude branches spurious, and by
what physical criterion?); a per-CASE Phi~1e-13 does NOT certify "the" solution when
several distinct floored points exist. (2) Determine whether the multiplicity is a true
continuum feature or shrinks with grid (run the free-solve seed test at Nr=24 — throughput
permitting; this verifier was budget-limited to Nr=12/16). (3) Add a PHYSICAL selection
principle (regularity / BC on Theta, energy/stability, continuation from a known limit)
that PINS one solution — derived, not imposed. Until a basin-selecting criterion exists,
M_MS is not bankable from any current solve. The dense-LM (jacrev+lstsq) tool is the right
flooring engine at these sizes; the matrix-free JFNK scalability win is NOT recovered (it
remains throughput-poison at Nr≥16, per both the report and the unrun-here matrix-free
floor). So at present: dense-only, and NOT YET a trustworthy M_MS readout from any gauge.

**One caveat (honest):** the free-solve perturbed branch at Nr=16 reached Phi=5.1e-11 at
the 40-it cap, not full machine floor (the round branch did, 8.5e-13). It is below the
report's own <1e-9 "floored" criterion and on a clean descending trajectory to a clearly
distinct M_MS (0.278 vs 0.292), so the basin distinction is real; but a fully-floored Nr=16
perturbed re-run (higher it cap) and an Nr=24 seed-sweep would harden the multiplicity
claim and were beyond this verifier's anti-hang budget.
