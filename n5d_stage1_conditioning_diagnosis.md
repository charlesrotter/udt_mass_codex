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

## 4d. Source–cell pullback / L-scaling audit (PROVISIONAL, no verdict)

**Date:** 2026-07-06 · script `n5d_pullback_audit.py` · HEAD after `bd944c8` · equations/BCs/readouts/seal/
verdict-logic UNCHANGED · no FIX-2 · no finite-L barrier/penalty/target · no verdict pilot. **Question:** is
the frozen H3 stress pulled back into the live cell consistently as L changes, or frozen at seed L0 while the
geometric operator uses current L?

**Finding: (i) YES there is a pullback inconsistency — the source is frozen at seed L0 while the operator uses
current L; native-correct is current-L interpolation. (ii) But that inconsistency does NOT cause the
L-collapse — the collapse is the ABSENT finite-L closure; fixing the pullback would not stop it.**

1–2. **Coordinate maps / source convention.** Solver `fields`: nodal φ,ρ,a2 at Chebyshev ζ∈[−1,1], d/dr=(2/L)
   d/dζ with **current L**; physical r(ζ)=rc+(L/2)(ζ+1). Source `build_Tshear`: T_shear=amp·sh2(r_phys)·P2,
   r_phys=rc+(**L0**/2)(ζ+1), **L0=seed=1.0 fixed**. `stress_profiles.npz 'rc'` = physical hopfion radius
   [0.047,5.95]; `sh2` = ⟨shear·P2⟩_shell, shear=T_θθ−T_φφ in the **orthonormal frame** (stress component, not
   density-weighted, already ℓ=2-projected). **Confirmed inconsistency: operator uses current L, source uses
   seed L0.**
3. **Native pullback rule (derived).** The shear row is the POINTWISE E^AB=−T^AB at each node (collocation, no
   dr-integral). T_s is a physical stress component in the same orthonormal frame ⇒ evaluate it at the SAME
   physical point as E_s_geom: r(ζ)=rc+(L/2)(ζ+1) with **current L** — **interpolation-only at current-L
   physical r, no amplitude L-Jacobian** (φ-blind S²/H3 matter enters only the h_AB row, no φ-source). =
   registration **B**. Registration A (seed L0) mis-locates T_s once L≠L0. Registration C (fixed ζ-profile)
   is what A ALREADY is (L0 fixed ⇒ sh2(r(ζ)) is a fixed ζ-function) — **C not distinct from A here.**
   *(Residual question for a later CAS check, not affecting the placement finding: an orthonormal-vs-coordinate
   ρ² frame factor between the flat-space stored stress and the cell-frame component.)*
4. **Three registrations vs L** (round-flat bg, S-Dir, amp=1): at **L=L0=1.0 A≡B** (‖rhs‖=3.01, a2peak=2.12).
   As L shrinks: **A** holds ‖rhs‖=3.01 (fixed ζ-values) and gives **a2∝L² exactly** (a2/L²=2.115 across all
   L); **B** samples a shrinking physical window (‖rhs‖ tracks local sh2), a2/L² varies. **Both give a2→0 as
   L→0** — the (2/L)² geometric stiffening, not the registration, sets the L-power. Registration sets the
   source VALUES/placement, not the collapse.
5. **Fixed-L=L0 diagnostic** (pin L=L0, drop the Hseal closure row — diagnostic only, NOT physics closure):
   a2_peak = **8.6e−2** (vs free-L pilot 5e−3, **~17× larger**), with **Hseal=−0.83** (the cell is far from
   closed at L=L0). ⇒ the free-L solve collapses L *trying and failing* to satisfy H=0; **the L-collapse is
   driven by the absent finite-L closure, not by source detachment** (fixing L recovers a2 without touching
   the source).
6. **S-Dir block balance (A vs B):** at the seed (L=L0) A and B give **identical** blocks (they coincide at
   L=L0); the pullback diverges only once L≠L0. So the pullback does not change the seed-state blocker
   (Hseal + shear_ODE + boundary rows).

**Classification:** a COMBINATION — **(a) source pullback bug: present** (seed-L0 vs current-L; native fix =
registration B, current-L interpolation, no amplitude Jacobian); **(b) source scaling correct but finite-L
closure absent: the DOMINANT driver** (a2∝L² is native; the collapse is the missing finite-L closure — fixing
L recovers a2 ~17×); **(c) frozen-source approximation inconsistent under free L: yes** (a fixed physical object
cannot register consistently into a collapsing cell). NOT (d) unresolved — the mechanism is now resolved. The
pullback fix (A→B) is a genuine correctness improvement but would NOT stop the L-collapse (that needs the
finite-L closure = the round-continuum degeneracy, gated; and no anti-collapse fudge is permitted here).
**No physics verdict, no Outcome A/B, no continuum lead. Outcome D / tool-limited stands.**

## 4e. Registration-B pullback correctness patch (implemented 2026-07-06)

**Patch (correctness only — NOT an anti-collapse change):** the frozen ℓ=2 source is now pulled back at
the CURRENT physical cell coordinate r(ζ)=rc+(L/2)(ζ+1), live inside the residual, instead of frozen at the
seed L0. Files: `n5d_shear.source_interp` (new, torch-differentiable linear interp of sh2(r), clamp→0
outside support, no amplitude Jacobian); `cell_solver_f2d.fields` (new `n5d["src"]=(rc,sh2,amp)` path —
interpolates at current L each residual eval; legacy `n5d["Tshear"]` precomputed-array path kept for
tests/diagnostics); `n5d_pilot.build_Tshear` (now takes current L; routes through `source_interp`) and
`run_one_bc` (uses the live `src` path). Equations/BCs/readouts/seal/H-closure/verdict-logic/solver-limits
UNCHANGED; no FIX-2; no finite-L barrier/penalty/target/anti-collapse term. Tests: `tests/test_n5d_pullback.py`
(8 tests) + full suite **56 passed / 1 xfailed**; L_bare 7 PASS; N5d preflight both BCs square, base-row match 0.0.

Before/after (fixed-state comparison; no verdict pilot): at **L=L0 new≡old** to 2.2e−16 (identical source,
identical shear_res); for **L≠L0** the source is sampled at current-L physical r (e.g. L=0.1: |ΔTshear|max
2.99, ‖shear_res‖ 3.076→1.637). **Readouts q_raw/Pi_phi/M_readout/Hseal are identical old-vs-new at every
fixed state** (they read φ,ρ,a2, not the source). The patch is a genuine correctness fix but does **not** stop
the L-collapse (gated round-continuum closure; confirmed in §4d) — it makes the source physically consistent
as L varies.

**LEDGER — source-normalization / frame factor: RESOLVED → ×ρ²/2 (see §4f).** (Superseded the earlier "open"
note here.) The separate flat-hopfion→cell-frame embedding of the orthonormal COMPONENT remains the frozen-source
approximation (§4d), still ledgered.

## 4f. Source frame-factor audit — RESOLVED to ×ρ²/2 (implemented 2026-07-06)

**Question:** does the stored `sh2 = ⟨T_θ̂θ̂ − T_φ̂φ̂⟩(ℓ2)` (orthonormal/mixed component from the hopfion's flat
lab frame) equal the cell-frame `T_s` in `E_s + T_s = 0` as-is, or need a ρ²/frame factor? **Answer: it needs
×ρ²/2 — cleanly derived (CAS), implemented.** Script `n5d_frame_factor_cas.py`.

1–2. **What sh2 stores** (`h4_scripts/h4_n4_phaseB_stress.py`): the flat-space Faddeev–Skyrme Hilbert stress
   `σ_ij` (Cartesian), projected onto flat spherical ORTHONORMAL vectors → `shear = T_θ̂θ̂ − T_φ̂φ̂`, then the
   count-normalized shell moment `⟨shear·P2⟩`. So `sh2` is an **orthonormal/mixed stress component** (`= T^θ_θ −
   T^ψ_ψ`), not a coordinate/density-weighted/scalar-coefficient object.
3. **Native relation (CAS-decisive).** The geometric shear action density is `L_geo = e^{−2φ}·ell`,
   `ell = −½ sinθ·a'bt'/√(ab)` (`op_derive2.py`). CAS (`n5d_frame_factor_cas.py`): the round (trace) part of
   `δL_geo/δs` = 0, and **`(δL_geo/δs)/(sinθ·E_s_coded) = ρ²/√(ρ⁴) = 1`** — i.e. the coded `E_s`
   (`EAB_shear_row`) **is the action-density form** `(δL_geo/δs)/sinθ = (ρ²/2)(E^θ_θ − E^ψ_ψ)`, carrying the
   √h=ρ² measure weight. With the repo convention **`E^{AB} = (2/√h)δS_geo/δh_AB`, `T^{AB} = (2/√h)δS_m/δh_AB`,
   `E^{AB}=−T^{AB}`** (H4_N1:19–24), matching `E_s + T_s = 0` forces the SAME weight on the matter side:
   **`T_s = (ρ²/2)·sh2`.** ρ = areal radius (h_AB-side, **φ-blind** → no direct φ-source).
4. **Decision: ×ρ²/2** (a ρ² factor — r-dependent, reshapes the source — times the constant ½ from the shared
   (2/√h) convention). Not unchanged; not ÷ρ²; not another basis factor.
5. **CAS check:** `n5d_frame_factor_cas.py` (sympy) — ratio = 1 exactly, multiplier = √(ρ⁴)/2 = ρ²/2 exactly.
6. **Diagnostic (unchanged vs corrected; no verdict solve):** ρ²/2≈0.25 on the cell → projected ℓ=2 ‖rhs‖
   3.008→0.752, linear S-Dir a2_peak 2.115→0.529 (×0.25 at the seed where ρ≈const; reshaped by ρ(r)² on a real
   solution). φ/ρ/f rows stay **exactly source-blind** (Δphi_ode=Δrho_ode=Δres_f=0); only shear_res moves.
7. **Implemented** in `cell_solver_f2d.fields` live-src path: `Tshear = amp·(ρ²/2)·sh2(r_cur)·P2`. Tests
   `tests/test_n5d_pullback.py` (+3 frame-factor: exact `(ρ²/2)·sh2·(2/5)` match, ρ²-scaling, φ-blindness);
   full suite **59 passed / 1 xfailed**; L_bare 7 PASS; N5d preflight both BCs base-row match 0.0.

**Still-separate open item (frozen-source approximation, §4d):** the flat-hopfion stress is used as the
cell-frame orthonormal COMPONENT directly (flat vs curved-cell embedding); that is a distinct approximation,
untouched by this frame-factor resolution. **No physics verdict, no Outcome A/B, no continuum lead. Outcome D
stands.**

## 5. Scope / discipline
- ONE tile: static, Branch P, block-diagonal, ℓ=2 axisymmetric shear, frozen H3-hopfion source, whole cosmic cell.
- Premise ledger unchanged from the pilot: ξ FREE, κ FREE-units, Z_φ=8 (CHOSE — Route-A carrying the Route-B
  number), source FROZEN (ledgered), source registration CHOSE, shear seal BC CHOSE-provisional (both run), ℓ=2 SCOPED.
  All conditioning params (Nr, Nth, maxit, seed a2, continuation, equilibration) = category-A.
- Registry: this SHARPENS the Outcome-D pilot (it does not overturn or add any negative). No banked result changes.
