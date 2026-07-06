# N5d Stage-1 Conditioning Diagnosis — PROVISIONAL / TOOL-LIMITED (Outcome D only)

**Date:** 2026-07-06 · **Driver:** Claude Opus 4.8 (1M) · **Class:** category-A conditioning diagnosis
(numerical technique / *how* we solve — NOT a physics change). **Build:** reproduced exactly at `bf54957` /
current HEAD. **Scripts (working, this repo root):** `n5d_conditioning_diag.py`, `n5d_conditioning_diag2.py`,
`n5d_conditioning_diag3.py`.

## Status labels (binding, read first)
- **PROVISIONAL / TOOL-LIMITED.** This is a solver conditioning diagnosis, not a verifier-banked result.
- **Outcome D only.** NO Outcome A, NO Outcome B. The pin-vs-continuum question is UNANSWERED and unanswerable
  from the Stage-1 pilot until the solve converges.
- **NO continuum lead.** No genuine physical soft *shear* mode was found (see §3). The near-singularity is
  numerics + an unpinned gauge offset — not signal.
- **NO physics verdict.** Nothing here bears on the metric. `solver-first` (Charles 2026-06-19): a mismatch /
  pathology indicts the SOLVER first; this doc stays entirely on the numerics.

## 0. What was diagnosed
The Stage-1 pilot (`n5d_pilot_stage1_results.md`, Outcome D) returned `converged=False` for both seal BCs with a
near-singular Jacobian (`jac_cond` ≈ 4.2e15 S-Dir / 9.2e16 S-JC2, at the float64 floor). This diagnosis SVD-analyzes
the reproduced non-converged states (and the nonzero shear seed) to classify the near-zero direction(s) and test
category-A fixes. **No physics pilot was re-run as a verdict run.**

**Reproduction check (states are exact):** re-running the pilot continuation reproduced the banked diagnostics —
S-Dir `jac_cond=4.175e15`, `a2_peak=5.140e-3`, `H_seal=-5.578e-3`; S-JC2 `jac_cond=9.203e16`, `a2_peak=1.911e-5`,
`H_seal=-6.376e-3`. Frozen H3-hopfion source confirmed (Q=0.9917).

## 1. Headline
The "single ambiguous near-singular direction" flagged by the pilot is, on SVD, **three stacked, mutually distinct,
all-unobservable near-null modes** — none of them the shear physics. The near-singular Jacobian is a **compound
NUMERICAL-CONDITIONING artifact**, dominated by pre-existing base-solver issues, not by the shear extension.

## 2. The three near-null contributors (SVD, both BCs)

Variable layout (Nr=16, Nth=8 → 177 unknowns): `phi[0:16] · rho[16:32] · u_field[32:160] · a2[160:176] · L[176]`.
Full-Jacobian smallest singular values — S-Dir: `[5.5e-2, 3.3e-2, 1.6e-2, 4.0e-3, 7.8e-8]`;
S-JC2: `[1.7e-2, 8.0e-3, 2.0e-3, 8.9e-7, 3.7e-7]`. `smin/(smax·ε)` ≈ 1.6 (S-Dir) / 2.0 (S-JC2) → the smallest
mode sits AT the float64 assembly floor (numerically null).

| # | contributor | dominant variables | classification | key evidence |
|---|---|---|---|---|
| **1** | **row/column scaling imbalance** | all rows; the **L** column | **(b) block-scaling** | `smax ≈ 1e8` from the Chebyshev 2nd-derivative ODE rows [(2/L)²·D2 ~ N⁴] vs O(1) BC/H-seal rows; the **L column is under-scaled by ~10⁴×** (col-norm ≈ 9e2 vs field cols ≈ 1e7). **Inherited from the BASE (no-shear) system:** base cond ≈ 1e17 at every Nr∈{8,12,16,24}, worst mode = the L column (L-fraction ≈ 0.98). |
| **2** | **S-JC2 constant-a2 offset null** | **a2** (overlap w/ constant = 1.000) | **(a) redundant / unpinned-BC — EXACT structural null** | `EAB_shear_row` has NO zeroth-order term in `s`, so under S-JC2's Neumann–Neumann (`a2'(r_c)=0` AND `a2'(r_s)=0`) a **constant a2 is an exact homogeneous null**. Shear sub-block `d(shear)/d(a2)` smin = 5.3e-12 (S-JC2) with null-vector overlap-with-constant = 1.000; present already at the seed (amplitude-independent). S-Dir's Dirichlet seal (`a2(r_s)=a2_mirror`) removes it → S-Dir shear sub-block cond only 1.2e8. This is the whole ~5-order gap between S-JC2 (9e16) and S-Dir (4e15). |
| **3** | **stalled-state constant-phi near-null** | **phi** (overlap w/ constant = 1.000) | **(d) degenerate / non-convergence artifact** | The solve stalled at a **near-homogeneous state** (ρ essentially constant, max\|ρ'\|≈3e-3; φ essentially constant, max\|φ'\|≈1e-7). There a constant-φ shift is flat because it enters the φ-ODE only through `e^{−2φ}·ρ'² ≈ 0`. A genuine converged soft mode would persist under real gradients; this one does not (see §3, CONFIRM-2). |

## 3. All near-null modes are UNOBSERVABLE (the load-bearing finding)

Moving the state a step `ε=1e-4` along each near-null right-singular vector, vs along a generic unit direction:

| readout | Δ along null mode | Δ along generic direction |
|---|---|---|
| `q_raw` | ≤ 1.6e-11 | ~0.70–1.4 |
| `Pi_phi` | ≤ 1.2e-10 | ~5.6–11 |
| `M_readout` | ≤ 1.6e-11 | ~0.70–1.4 |
| `H_seal` | ≤ 8e-14 | ~0.07–0.27 |
| `phi_node_count` | 0 | 0 |
| `reduced-source turning points` | 0 | +5 / −1 |

**Every near-null mode leaves `q_raw`, `Pi_phi`, `M_readout`, `H_seal`, node count, and turning-point count
unchanged to ≤ 1e-11**, while a generic direction of the same size moves them O(1). The near-singular direction(s)
carry NO observable content ⇒ there is no physical soft *shear* mode here, hence **no continuum lead** (per the
Stage-1 pre-registration, a genuine flat shear direction would have been a continuum-toward-no-pin lead; these are
not it — they are scaling + an unpinned constant offset + a stalled-state φ artifact).

**Constructive confirmations:**
- **CONFIRM-1 (mode 2 is the unpinned offset):** Ruiz equilibration alone barely helps S-JC2 (9.2e16 → 2.4e16,
  because the null is exact). Ruiz **+ pinning the constant-a2 offset → 9.2e16 → 1.5e11** (~6 orders). The S-JC2
  blow-up *is* the unpinned constant-shear offset.
- **CONFIRM-2 (mode 3 is a stalled-state artifact):** injecting genuine φ/ρ structure (max\|ρ'\| 3e-3 → O(1–80))
  lifts smin **7.8e-8 → 4e-3 (5 orders)**, drops cond 2.8e15 → 5.5e10, and the smallest mode stops being
  φ-dominated (phi-fraction 1.0 → 0). The φ-null vanishes under real gradients ⇒ artifact of the stall.
- **Seed vs final SVD:** S-Dir seed cond 1.05e11 (smin above floor) degrades to 2.8e15 as the state collapses
  toward homogeneity; S-JC2 seed already 1.13e16 at the floor (constant-a2 null is structural, present at any
  amplitude). Category-A fix tests: Jacobi (column-only) scaling and an a2-block scale sweep were ineffective
  (cond stays ~4e15/6e16) — neither addresses an exact null or a stalled state.

## 4. Recommended solver fixes (category-A, ordered) — for the gated next step

1. **FIX-1 — equilibrate the linear step inside `newton_lm_solve`** (highest value; helps the base solver too).
   Two-sided Ruiz / explicit row–column nondimensionalization: scale down the 2nd-derivative ODE rows, scale up the
   L column, solve, unscale the LM step; judge acceptance/convergence on the TRUE (unscaled) residual. Removes the
   `smax≈1e8` / L-column imbalance (contributor 1).
2. **FIX-2 — make S-JC2 well-posed** (SEPARATE DESIGN-GATE; touches BC well-posedness — Charles call, NOT done
   here). The source-free Neumann–Neumann shear problem is structurally rank-1-deficient by a constant offset.
   Either (i) an explicit ledgered numerical gauge pin on the constant-a2 offset, or (ii) read pin-vs-continuum on
   **S-Dir** (already well-posed) and use S-JC2 only as a post-gauge cross-check. Even if numerically "gauge", this
   changes BC handling, so it is deferred to its own gate.
3. **FIX-3 — escape the trivial state** (initial guess). Once 1–2 restore conditioning, LM should relax off the
   near-homogeneous stall; if not, seed from the converged round-static solution rather than the flat seed.
4. **FIX-4 — higher precision is NOT the first move.** `smin/(smax·ε)≈1–2` sits at the float64 floor, but that
   floor is reached via fixable scaling + an exact gauge null, not genuine precision loss. Revisit float128/mpmath
   only if an equilibrated, gauge-fixed, structured-seed solve still floors.

Only a **converged** solve (Φ→tol, cond ≲ 1e8–1e10) can then read Outcome A/B for the ℓ=2 tile.

## 4b. FIX-3 attempt — structured seed / continuation repair (PROVISIONAL, no verdict)

**Date:** 2026-07-06 · script `n5d_pilot_fix3.py` · FIX-1 active · no S-JC2 gauge pin · equations/BCs/
source/readouts/residual/seal UNCHANGED (only the SEED is new). Bounded: Nr=16, Nth=8, maxit=30,
budget ≤100 s/BC, one foreground process. **NOT a verdict run** — no pin-vs-continuum read, no A/B.

Two variants of a mirror-BC-respecting structured Branch-P seed (nontrivial interior φ′/ρ′ via a
cos(π(ζ+1)/2) bump; max|φ′|=0.46, max|ρ′|=0.25): (A) relax through the base system first, then add
shear; (B) seed the coupled shear continuation directly at matched L0=1.0.

**Result: structured seeding does NOT rescue convergence — the solve FLATTENS the structure back to
the near-homogeneous state in both variants.**

| variant | BC | finalPhi | converged | raw cond | eff cond | H_seal | max\|ρ'\| (seed→final) |
|---|---|---|---|---|---|---|---|
| A (pre-relax) | S-Dir | 6.4e-3 | False | 1.3e16 | 5.5e15 | −7.9e-2 | 0.25 → 2.9e-3 |
| A (pre-relax) | S-JC2 | 6.6e-3 | False | 1.1e17 | 6.2e16 | −8.0e-2 | 0.25 → 1.9e-3 |
| B (direct, L0=1) | S-Dir | 6.7e-3 | False | 2.7e15 | 2.0e15 | −7.8e-2 | 0.25 → 2.7e-3 |
| B (direct, L0=1) | S-JC2 | 7.9e-3 | False | 6.1e17 | 2.0e17 | −8.7e-2 | 0.25 → 1.4e-3 |

Stage-A on its own: the structured base relaxed max\|ρ'\| 0.25→0.08 (still falling), L collapsed
1.0→0.21, H_seal=−0.085 — i.e. it heads toward near-homogeneous, not a structured closed cell.

**Interpretation (classification of the remaining S-Dir failure, per the FIX-3 gate):** the remaining
failure is **φ/ρ DEGENERACY, not scaling** (FIX-1 is active and eff_cond ≈ raw_cond here — column scaling
barely moves it) **and not a mere seed artifact** (a genuinely structured seed is flattened by the solve).
The φ/ρ degeneracy has a physical root that **rides on the already-banked round-continuum picture**
(depth/size Outcome C, `native_readout_map_depth_size_results.md`): the round Branch-P bulk is
scale-invariant with monotone φ, so the mirror BCs (φ′=0 at BOTH ends) admit only near-constant φ — there
is **no non-trivial structured ROUND base for the solver to converge to**. This SHARPENS contributor 3:
it is not a curable stall — the round base is genuinely near-flat, so any size/mass structure must come
from the SHEAR sector (h_AB), whose induced response here stays tiny (a2_peak ≤ 2.5e-2, non-converged).
**NO physics verdict, NO Outcome A/B, NO S-Dir tile lead (S-Dir did not converge).**

**Consequence for the fix ladder:** FIX-3 is INEFFECTIVE for the round base by itself. FIX-1 (scaling) and
FIX-3 (seed) both leave the Stage-1 pilot non-converged. The binding constraints are the S-JC2 exact
constant-a2 null (→ FIX-2, gated) and the round-flatness φ/ρ degeneracy (a genuine feature, not a bug to
seed around) — the pin-vs-continuum question for the ℓ=2 shear tile remains UNANSWERED (Outcome D stands).

## 4c. Shear-forcing / residual-balance audit (PROVISIONAL, no verdict)

**Date:** 2026-07-06 · scripts `n5d_shear_forcing_audit.py`, `n5d_shear_forcing_audit2.py` · HEAD after
`fc1e4fa` · equations/BCs/source/readouts/residual/seal UNCHANGED · no FIX-2 · no verdict pilot.
**Question:** is the ℓ=2 shear sector actually forced strongly+correctly by the frozen H3 source, or is
the pilot seeing a near-zero/cancelled/misnormalized shear projection?

**Finding: the shear sector IS strongly and correctly forced. The pilot's tiny a2 is a SOLVER artifact
(L-collapse stall), NOT a forcing defect.**

1. **Raw source (real & strong):** file `h4_scripts/stress_profiles.npz`; Q_H=0.9917; virial E2/E4=0.99946.
   Full-field (256³, GPU): ‖T^AB‖=82.8, ‖shear‖(T_θθ−T_φφ)=47.7. Angular power of the traceless shear:
   **ℓ=0 = 81.3%, ℓ=2 = 17.6%, ℓ=4 = 0.03%.** On the cell (r∈[0.5,1.5]) sh2∈[−3.27,0.90], rms 1.90;
   projected source ‖rhs‖=3.01 — **not near-zero, not cancelled.**
2. **Normalization/sign CORRECT:** ΣⱼwⱼP2ⱼ² = 0.400000 (=2/5 exact), ΣⱼwⱼP2ⱼ = −9e−16 (⊥P0). The 2/5
   weight is applied identically to the geometric E_s row (s=a2·P2) and the source (amp·sh2·P2) → it
   cancels in the a2-ODE. Sign: rows set ΣwP2(E_s_geom+Tshear)=0 ⇒ E_s_geom=−Tshear, consistent with
   E^AB=−T^AB (Tshear = +T_s = T_θθ−T_φφ). No normalization or sign error.
3. **Residual blocks (which block blocks convergence):** at the final stalled state the shear-ODE residual
   is SMALL (S-Dir 4.1e−4) — the shear is NOT the blocker; the largest blocks are **Hseal (5.6e−3)** +
   the boundary/closure rows (shear_seal_BC 5.0e−3, rho_BC 4.5e−3, f_BC 2.3e−3). For S-JC2 the shear BC
   rows are large (9.3e−3) — the unpinned constant-a2 null. The blocker is the H=0 closure / mirror BCs,
   not the shear forcing.
4. **Linearized shear response (category-A):** freezing φ,ρ at the seed background (L=1.0) and solving the
   LINEAR shear rows on the frozen source gives **expected a2_peak ≈ 2.1** (S-Dir; shear-op cond=1.19e4,
   full rank, source solvable) — on BOTH round-flat and structured backgrounds. The nonlinear pilot got
   a2_peak ≈ 5.1e−3 (S-Dir) / 1.9e−5 (S-JC2). **The ~400× shortfall is the L-COLLAPSE:** the coupled solve
   collapses L 1.0→9.1e−3 (S-Dir, 110×) / 4.6e−3 (S-JC2, 218×); the source is registered at the fixed seed
   L0=1.0 while the geometric coeff ∝(2/L)² stiffens ~10⁴× ⇒ predicted a2 ~ source/coeff ~ 1.2e−4 / 3.1e−5,
   matching the observed a2_peak to order. At a physical finite-L cell the shear response is O(1).
5. **Compatibility/solvability:** **S-Dir** shear op is full rank (cond 1.19e4) ⇒ source COMPATIBLE/solvable.
   **S-JC2** has the exact constant-a2 null (right-null overlap-with-constant=1.000); the source EXCITES the
   left-null by ⟨u_null,rhs⟩/‖rhs‖ = **0.68** ⇒ the ℓ=2 source is INCOMPATIBLE with S-JC2 until the null is
   pinned (the linear solve blows up to ~1e13). Per the gate, NOT pinned/interpreted here (FIX-2).

**Classification of the tiny shear response:** primarily **(d) solver residual imbalance / non-convergence**
— the L-collapse stall stiffens the operator so the fixed-L0 source under-drives the shrunken cell; the
forcing itself is strong (‖rhs‖=3.0), correctly normalized, and well-conditioned/compatible for S-Dir
(linear a2≈2.1). Secondarily **(b) projection/truncation** — the ℓ=2-only tile couples to just **17.6%** of
the traceless shear power (ℓ=0 dominates at 81.3%; flagged for higher-ℓ). **NOT (a)** cancellation, **NOT
(c)** normalization/sign, **NOT (e)** weak coupling. For S-JC2, an additional compatibility failure vs the
unpinned constant-a2 null (→ FIX-2). The L-collapse ties to the round-continuum/closure degeneracy already
seen in FIX-3 (the round base does not close to a finite-L cell). **No physics verdict, no Outcome A/B, no
continuum lead.** FLAG (category-A, not changed here): the source registration pins to the seed L0 while the
solve collapses L — the source detaches from the cell scale as L→0.

## 5. Scope / discipline
- ONE tile: static, Branch P, block-diagonal, ℓ=2 axisymmetric shear, frozen H3-hopfion source, whole cosmic cell.
- Premise ledger unchanged from the pilot: ξ FREE, κ FREE-units, Z_φ=8 (CHOSE — Route-A carrying the Route-B
  number), source FROZEN (ledgered), source registration CHOSE, shear seal BC CHOSE-provisional (both run), ℓ=2 SCOPED.
  All conditioning params (Nr, Nth, maxit, seed a2, continuation, equilibration) = category-A.
- Registry: this SHARPENS the Outcome-D pilot (it does not overturn or add any negative). No banked result changes.
