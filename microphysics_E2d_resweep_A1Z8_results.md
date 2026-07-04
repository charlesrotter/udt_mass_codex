# E2d — CONTINUATION+MULTI-START DRIVER build + MMS field-axis certification (OBSERVE mode)

**Date:** 2026-07-04. **Owed step:** PURSUIT_CHARTER §5 E2d — build the multi-start+continuation
driver on the E2c-hardened `lm_hardened`, CERTIFY it on the MMS field-axis problem FIRST, THEN (if
certified to seed-class distance) run the gated A1Z8 re-sweep. **Category:** A (numerical
conditioning / globalization — HOW we solve; the always-green lane). **No physics/equation change:**
`residual_comp` and `lm_hardened` are BYTE-IDENTICAL (`git diff --stat cell_solver_composite.py` =
empty; all E2d code lives in new files). **Data-blind** (synthetic MMS; no observational numbers).
**pytest 32/1xfail** (unchanged; E2d adds no test-touching code). **Status: PROVISIONAL — builder
output, NOT yet blind-verified, NOT banked.**

**HEADLINE (scoped to this grid / these MMS / these levers):** the driver is BUILT and it
substantially EXTENDS the certified convergence reach — but the FIELD axis is **NOT UNIFORMLY
CERTIFIED to the charter's seed-class target O(0.3–1.5)**. Per the brief's pre-registered gate
("if it cannot certify to seed-class distance, STOP and report the residual gap honestly — do NOT
run the real sweep on an uncertified tool") **the A1Z8 real re-sweep is GATED OUT and was NOT run.**
What IS newly certified: the **boundary/soft-dilation axis holds at ≥30** (E2c preserved, no
regression) and the **deviation-field (u) axis is certified to ~0.3** on both MMS. The **combined-
cell field axis** (perturbing φ_c, ρ_c, u together — exactly E2c's "field-distant" direction) is
reached only in a **PATCHY subset** of cases: continuation reaches roots single-shot entirely
misses (e.g. A3Z1 combined-cell 0.3 → max|F| 1.4e-12), but folds short on others (even at 0.05),
so there is **no clean certified radius** on that axis. Mechanism identified below.

Files (committed with this doc, NOT run as a sweep): `e2d_continuation_driver.py` (the driver),
`e2d_mms_fieldaxis_certification.py` (+ `.json`, `e2d_cert.log`), `e2d_gridhomotopy_probe.py`
(+ `.json`, `e2d_gridprobe.log`).

---

## 1. THE DRIVER (`e2d_continuation_driver.py`) — Category-A, wraps the untouched corrector

Four composable globalization techniques built AROUND the byte-identical `lm_hardened`/
`residual_comp`. Each is an always-green-lane numerical technique (charter: "continuation/
homotopy"); the FINAL solve of every path is on the true residual.

1. **Multi-start** — run the corrector from a LIST of seeds; keep the best (lowest max|F|).
2. **Newton (source) homotopy** — `g_s(v) = R(v) − (1−s)·R(v0)`, s:0→1. At s=0, v0 is an EXACT root
   of g_0; at s=1, g_1 = R. Uses ONLY the seed v0 — it NEVER peeks at the true root, so it is an
   honest sweep technique. Jacobian(g_s)=Jacobian(R) (constant shift) so `jacrev` is unchanged.
3. **Pseudo-arclength continuation** on the Newton homotopy — the augmented (n+1) system
   `[R(v)−(1−s)F0 ; t·(y−y_pred)]` parametrized by arclength, so s may DECREASE/increase to pass
   s-TURNING POINTS (folds). The corrector is the same hardened `lm_hardened`; the path tangent is
   the nullspace of `[J_R | F0]` (one Ruiz-equilibrated lstsq).
4. **Grid homotopy** — solve on a coarse radial grid (fewer field DOFs → smoother, wider-basin
   ‖F‖² landscape), barycentric-prolongate to the fine grid, polish. `prolongate()` uses
   barycentric-Lagrange matrices on the Cheb-GL (radial), Legendre-GL (angular) and ambient Cheb-GL
   nodes; round-trip identity verified to 1.8e-15.
5. (Also built, for robustness/sweep use) an INDEPENDENT **fixed-point homotopy**
   `H(v,s)=s·R(v)+(1−s)(v−v0)` and **(ξ,κ) parameter continuation** (residual_comp takes prm
   natively — no edit).

Soundness (per technique): all are root-preserving path methods — the s=1 / fine-grid / target-prm
endpoint is the byte-identical true residual; homotopy/arclength only change the ROUTE to it; the
boundary positivity/order guards are feasibility (provenance), never merit.

---

## 2. MMS FIELD-AXIS CERTIFICATION (`e2d_mms_fieldaxis_certification.py`)

Two manufactured solutions with EXACT roots (forcing-subtraction `R(v)=residual(v)−residual(v*)`,
same Jacobian/stiffness as the physical system): **MMS#1 = A1 Z=8 wall-slice** (the representative
sweep cell), **MMS#2 = A3 Z=1 plateau-slice + nonzero θ-bulge 0.4**. Perturb v* by seed-class
amounts on separate axes; a "REACH" requires BOTH true-residual max|F|≤1e-8 (GPU) with independent
CPU spot-check ≤1e-7 AND proximity to v* (dist<5, boundary ratio 0.5–2.0) — a dilation runaway gives
small max|F| at infinity and is REJECTED as a false reach. Grid Nr12/Nθ8/Na192, kmap 2.5, GPU V100
float64, CPU cross-checks on every declared reach.

### 2a. Boundary (soft-dilation) axis — E2c-certified ≥30 is PRESERVED (no regression)
| axis | MMS#1 A1Z8 | MMS#2 A3Z1 |
|---|---|---|
| boundary dr=10 | REACH 7.1e-10 | REACH 1.2e-12 |
| boundary dr=20 | REACH 9.6e-10 | REACH 5.0e-13 |
| boundary dr=30 | REACH 2.4e-9  | REACH 4.4e-12 |

### 2b. Deviation-field (u) axis — NEWLY CERTIFIED to ~0.3 (both MMS, both methods)
u-perturbations 0.05 / 0.1 / 0.15 / 0.2 / 0.3 all REACH (max|F| 1e-9…1e-12) via BOTH single-shot
`lm_hardened` and arclength continuation, on both brackets. (MMS#1 u=0.3 arclen sits at 1.11e-8 —
the float64 residual edge, dist 3.5e-9 — a marginal pass.)

### 2c. Combined-cell field axis (φ_c+ρ_c+u together = E2c's "field-distant") — PATCHY, no clean radius
| sc | MMS#1 direct | MMS#1 arclen | MMS#1 grid | MMS#2 direct | MMS#2 arclen | MMS#2 grid |
|---|---|---|---|---|---|---|
| 0.05 | no (runaway) | no (fold s_max 0.155) | — | **REACH** | **REACH** | — |
| 0.10 | no | no (fold 0.190) | — | no (runaway) | **REACH** (fold 0.847→polish) | **REACH** |
| 0.15 | no | **REACH** (fold 0.098→polish) | **REACH** | no | no (fold 0.700) | no |
| 0.20 | no | no (fold 0.111) | — | no | no (fold 0.358) | — |
| 0.30 | no | no (fold 0.142) | — | no | no (fold 0.215) | **REACH** |

Robustness cross-check (independent homotopy): fixed-point homotopy on the cell-0.3 case FAILS on
BOTH MMS (max|F| 2.9e-3 / 4.9e0, runaway) — the obstruction is the LANDSCAPE, not the homotopy
choice (matching E2c's "dogleg AND pure-GN both stall short").

**Reading:** reach on the combined-cell axis is NOT a monotone radius — some larger perturbations
are reachable (A3Z1 0.3 ✓) while some smaller ones are not (A3Z1 0.15 ✗; A1Z8 0.05/0.1 ✗). It is a
PATCHY basin structure. The three continuation levers (arclength / grid / fixed-point) reach
DIFFERENT subsets; together they far exceed single-shot (which reaches essentially NONE of the
combined-cell cases) but their union still leaves combined-cell directions uncertified.

---

## 3. THE MECHANISM — NEWTON-HOMOTOPY-PATH component separation (why the field axis is hard)

> **VERIFIER SCOPING (a5e1960b6f90b4686, applied):** the separation below is a property of the
> **Newton/fixed-point homotopy SOLUTION SETS, NOT an absolute landscape disconnection.** GRID
> HOMOTOPY demonstrably BRIDGES several of the same distances (A3Z1 cell-0.3 REACH; A1Z8 cell-0.15
> REACH) — a connecting path EXISTS, just not along these two homotopy families. Read every
> 'different connected components' below as scoped to the Newton/fp homotopy path, not the manifold.

The pseudo-arclength corrector is numerically FLAWLESS on these problems: on a 400-step trace it
held physF ~ 1e-9 at EVERY step with ZERO corrector failures. The obstruction is not the corrector
— it is the **shape of the Newton-homotopy solution path**:

- From a combined-cell field-distant seed, the path `{v : R(v)=(1−s)R(v0)}` has a **global
  s-maximum well below 1** (measured s_max: A1Z8 cell-0.3 → 0.142; A3Z1 cell-0.3 → 0.215; A1Z8
  cell-0.15 → 0.098; …). Past that fold the path **turns back to DECREASING s** and the state runs
  off along the **soft dilation direction** (the E2c translation gauge): boundaries blow up
  (r_p ratio → ∞, dist-to-v* → 10²–10³).
- Therefore the field-distant seed v0 and the true root v* lie on **different connected components
  OF THE NEWTON-HOMOTOPY SOLUTION SET** (verifier-scoped — NOT the full manifold; grid homotopy
  bridges some of these same distances) — the Newton/fp homotopy provably cannot bridge them, and the
  observed reaches (A1Z8 cell-0.15, A3Z1 cell-0.1) occur when the arclength/grid EXCURSION repositions
  the state into v*'s basin so the final true-residual polish finishes (not because that path reached
  s=1). **Implication: a CONNECTING PATH EXISTS; the fix is a better seed / grid-homotopy route into
  v*'s basin, not a stronger corrector.**
- This is the precise, mechanistic explanation of E2c's "intrinsic local-NLLS minima": the
  combined-cell field basin of a composite root is SMALL and is separated from field-distant seeds
  by a fold that recruits the dilation runaway. It ties the field axis and the boundary-slide axis
  together as one coupled landscape feature.

---

## 4. THE GATE OUTCOME (pre-registered by the brief) + honest residual gap

The charter's certification target = REACH combined-cell field distances **O(0.3–1.5)**. This is
the direction that matters for a real sweep: `seed_comp` differs from any putative solution mainly
in (i) the u bulge amplitude (u-axis — CERTIFIED to 0.3), (ii) φ_c/ρ_c set to continuity-flats that
may be O(1) off a solution's core profile (the combined-cell axis — UNCERTIFIED), (iii) the
boundaries (CERTIFIED ≥30). The binding uncertified direction (the core φ/ρ profile) IS the
combined-cell axis.

- **Boundary axis:** CERTIFIED ≥30 (E2c preserved). 
- **Deviation-field (u) axis:** CERTIFIED ~0.3 (NEW). 
- **Combined-cell field axis (the target):** NOT certified — patchy, folds to a different component
  under every lever tried; residual gap = from combined-cell distances ≳0.05–0.2 in unfavorable
  directions the driver floors at ~1e-4–1e0 or runs away, the SAME signature as the E2b sweeps.

**Per the brief's pre-registered gate, the A1Z8 real re-sweep is GATED OUT and was NOT run.**
Running the full sweep on a tool that cannot uniformly reach seed-class field-distant roots would
risk exactly the misread the charter warns of (trap #1: a null read as nonexistence) — the E2b
0/62 lesson. The disciplined action is to STOP at certification and report the gap.

---

## 5. Premise ledger (Category-A conditioning; provenance/soundness, no merit)
- Grid Nr12/Nθ8/Na192, kmap 2.5; coarse Nr8 for grid homotopy — CHOSE (Category-A, bounded per
  anti-hang; the E2c/E2b production grid).
- MMS = forcing-subtraction, two brackets + a bulged root — CHOSE (the E2 blind-verifier's decisive
  instrument, reused). Synthetic, data-blind.
- REACH criterion max|F|≤1e-8 (GPU) ∧ CPU≤1e-7 ∧ dist<5 ∧ 0.5<r_p ratio<2.0 — CHOSE (provenance/
  feasibility gate; the dist+ratio clause rejects the runaway false-floor, honesty not merit).
- Continuation params (ds, trust radius, s-schedule, fold_abort=0.03, maxit caps, budgets) —
  Category-A soundness knobs, bounded.
- Perturbation SHAPES (which analytic mode is added per axis) — CHOSE; the combined-cell axis is
  E2c's own `cell_sc` direction (φ_c+ρ_c+u simultaneously). Reach is shape-dependent (Sec. 2c) — a
  reported caveat, not a hidden pin.
- Physics untouched: `residual_comp`/`lm_hardened` byte-identical (git-verified); no equation,
  coupling, BC or source changed.

## 6. Verifier-before-record (owed; NOT yet done)
A blind adversarial verifier should: (i) confirm `git diff` shows NO change to `residual_comp`/
`lm_hardened` and pytest 32/1xfail; (ii) re-derive that Newton-homotopy Jacobian = R's Jacobian and
that arclength/grid/fixed-point endpoints are the TRUE residual (root-preserving); (iii) re-run the
MMS gauntlet fresh and confirm boundary ≥30 + u-axis ~0.3 REACH and the combined-cell PATCHY/fold
map (s_max<1 on the failing cases; runaway on the false floors); (iv) confirm the REACH criterion
cannot pass a runaway (dist/ratio clause) and that declared REACHes are real roots near v* (CPU
spot-check); (v) attack the GATE OUTCOME — is "combined-cell not certified → STOP the sweep" correctly
scoped (not overclaimed as nonexistence, not underclaimed — the boundary+u certifications and the
partial combined-cell reaches are real); (vi) sanity-check that the fold/component-separation claim
is not an artifact of tangent orientation or the fold_abort threshold.

---

## VERIFIER RECORD (blind adversarial pass — agent a5e1960b6f90b4686, 2026-07-04): SAFE TO BANK (1 scoping edit, applied)

Independent re-runs (GPU, bounded); pytest 32/1xfail reproduced.
- **Physics untouched + homotopy lands on the TRUE root — HOLDS (exact).** git diff empty; residual_comp/
  lm_hardened byte-identical; g(s=1)−residual = 0.0 EXACTLY, final polish on the true residual, MMS
  max|R(v*)|=0.0. The homotopy changes only the route.
- **Component separation — HOLDS-WITH-CORRECTION (applied above):** real, reproduced with the verifier's
  OWN seed shapes, independent-homotopy-confirmed (fp fails the same cases) — but scoped to the Newton/fp
  homotopy solution set, NOT an absolute landscape disconnection (grid homotopy bridges some of the same
  distances ⇒ a connecting path exists). Same over-read class the E2c verifier already corrected.
- **Certification radii — REAL:** boundary ≥30 + u-axis ~0.2–0.3 reproduced with the verifier's own
  perturbation shapes; combined-cell patchy/uncertified. REACH criterion is provenance-not-merit (the
  dist/ratio clause rejects the soft-dilation runaway false-floor; NO real root maxF≤1e-8 is ever rejected).
- **The STOP — HOLDS (defensible), mildly over-cautious:** gating out on the uncertified combined-cell axis
  is disciplined (trap #1); BUT a SCOPED sweep (positives = real H_cell-honest finds; nulls = coverage-
  limited, "not found from these seeds+continuation") would ALSO be legitimate and could surface real
  positives the certification can't predict — the STOP errs conservative.
- **Hygiene — HOLDS** (prolongation round-trip = 0.0 exact; data-blind synthetic MMS; CHOSE tags complete).
**Verifier fork recommendation:** pursue the PHYSICS-INFORMED SEED (multi-start over derived core φ/ρ
profiles to pull the combined-cell distance inside the certified u+boundary reach — the "fix the flaw"
move), with a scoped-caveated sweep as the OBSERVE fallback; treat component-separation as INFORMATIVE
(a real landscape feature), not as evidence the roots are unreachable.
