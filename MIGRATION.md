# MIGRATION — extend the hardened p1 solver to the derived-operator native-S² physics

**Decided 2026-06-24 (Charles):** do NOT canonize the `branchGP` prototype — it is un-harnessed and
exhibits a matter-sourced resolution-divergent metric warp. Instead EXTEND the hardened
`p1_residual_general_einstein.py` (the solver the purity harness was built to make solid) to absorb
branchGP's physics, **incrementally, with a convergence guard live at each step** so the divergence
gets caught where it appears. `branchGP` becomes a reference prototype; its one-off drivers get archived.

## Why (the experiment that settled it, 2026-06-24)
Same physics (winding matter + gravity), same grid:
- **p1 (hardened)** matter-on Nr=10: **Phi=1.0e-14** (machine precision), warps max|a|=1.08 |b|=1.00
  |c|=0.38 |d|=0.23 — small, clean.
- **branchGP (prototype)** matter-on Nr=10: Phi floor **~0.18** (never lower), warps **3–7, GROWING with Nr**.
So the matter-sourced divergence is a **branchGP-specific flaw** (its hand-inlined derived operator,
X=−2e5 kinetic term, Branch-P U term, and/or kap8=1), NOT generic winding gravity. Also: the derived
operator already exists AUDITED as a drop-in (`branch_operator.py` → `b1prime.E_mixed`); branchGP
bypassed it by re-inlining (`E_mixed_s2`).

## The guard
`migration_convergence_guard.py` — runs the CURRENT production solver matter-on at two grids and asserts
(a) it floors below 1e-6, (b) metric warps don't grow with Nr. Run after EVERY increment; the increment
that turns it RED is the culprit. (The fast pytest harness only checks OPERATOR-level N-convergence on an
analytic metric — it cannot catch a solve-level divergence; this guard can.)

## Baseline (current p1: a=−1 GR baseline, S³ winding, kap8=0.05)
- pytest tests/: 23 pass / 5 documented-gap xfails (the migration targets).
- guard: **GREEN** — Nr=10 Phi=1.0e-14 warp=1.085; Nr=14 Phi=1.3e-13 warp=1.168
  (FLOOR pass, N-CONVERGE pass: warp grows only 1.08→1.17). This is the clean behavior every
  increment must preserve.

## Increments (each: EDIT p1 in place → guard → `pytest tests/` → commit)
- [x] **M1 — derived operator + φ, small X. DONE 2026-06-24, GUARD GREEN.** Replaced pack8→pack6
  (a,b,c,d,Th,**φ**); residual now uses the audited `branch_operator.E_mixed_branch` + `EL_phi_branch`
  (e^{2φ} weight) at **X=−1** (small/non-stiff — X=0 is degenerate: φ drops out of its own EL), Branch G,
  S³ matter, kap8=0.05, diagonal (off-diagonals DROPPED — deferrable). Added φ(seal)=0 BC.
  - **jacrev-safety fix** (the guard caught it): `b1prime.EL_Th_3d` uses `requires_grad_` (functorch
    forbids it under jacrev) → wrote `_el_Th_weighted` using `torch.func.grad` (the validated branchGP
    pattern). The guard caught this on the first run — the migration working as intended.
  - guard: **GREEN** — Nr=10 Phi=1.2e-17 warp=1.043 (30s); Nr=14 Phi=1.6e-14 warp=1.119. FLOOR+N-CONVERGE
    pass. ~5× faster than the 8-field baseline. pytest: 23 pass / 5 xfail (flipped `test_derived_a_phi_in_operator`).
  - **Localizes the divergence:** the e^{2φ} weight + φ at small X are CLEAN → branchGP's divergence is NOT
    here; it's in M2 (X→−2e5), M3 (Branch-P U), or M4 (native S²/kap8=1).
- [x] **M2 — X-kinetic to −2e5 via continuation. DONE 2026-06-25, GUARD GREEN.** Added
  `continuation_solve_p1` (adaptive geometric X-ladder −1→−2e5, warm-start, SUBDIVIDE on stall so a stalled
  step can't cascade). Guard now targets the production X=−2e5.
  - guard **GREEN**: Nr=10 Phi=4.2e-11 warp=1.048; Nr=12 Phi=7.1e-12 warp=1.167. FLOOR + N-CONVERGE pass.
  - **MAJOR RESULT:** the production X=−2e5 floors to near-machine-precision with clean N-convergent warps
    (~1.05). **The X-kinetic stiffness is NOT branchGP's divergence** — it's fully solvable in the clean p1
    framework (branchGP was stuck at 0.18 / warps 3-7 even with its own continuation). => the divergence is
    cornered into M3 (Branch-P U) or M4 (native S²/kap8=1) — the only remaining differences from branchGP.
  - **COST CAVEAT:** the guard took ~hours (Nr=12 = 8.6h) — the dense-jacrev continuation is heavy. For
    M3+: streamlined to guard grids (8,10) + lighter continuation (n_steps=10, maxit=12); Nr=8→10 still
    catches a branchGP-type warp-growth. (A matrix-free per-step solver would help further if needed.)
- [x] **M3 — Branch-P U term. DONE 2026-06-25, GUARD GREEN.** Switched guard to `branch="P"` (the
  operator/φ-EL already carry the +δU / −2U' terms via branch_operator). Streamlined the continuation
  (n_steps=10, maxit=12) + guard grids → (8,10).
  - guard **GREEN**: Nr=8 Phi=8.9e-9 warp=3.478; Nr=10 Phi=1.7e-15 warp=3.457. FLOOR + N-CONVERGE pass.
  - **MILESTONE:** the scale-breaker `e^{2φ}−1` ACTS — it pulls φ **deep (φ=2.2)** and warps the metric
    strongly (~3.5), but the solution is **resolution-STABLE** (warp 3.48→3.46) and floors to machine
    precision. So (a) Branch-P U is NOT branchGP's divergence (large but stable warp); (b) **we reached the
    deep/strong-field regime CLEANLY** — the frame the deep-regime exploration wanted — where branchGP was
    stuck at 0.18. => the divergence is cornered into **M4** (native S² matter / kap8=1), the only
    remaining difference from the prototype.
- [ ] **M4 — native S² matter.** Swap S³ `field_n` → `free_s2_matter` 3-vector + `gtw` DOF + free BC.
  Guard. Flips xfail `test_matter_winding_is_native_S2`.
- [ ] **M5 — tags + defaults.** core_mode default → 'free'; source/tag kap8, xi, kap. Flips xfails
  `test_kap8_callers_tagged`, `test_matter_couplings_tagged`, `test_derived_a_phi_in_operator`,
  `test_default_core_mode_is_native_free`.
- [ ] **M6 — harden + reconcile.** Extend pytest harness: assert the DERIVED operator's flat/Schwarzschild/
  de-Sitter limits + N-convergence + operator==EL-of-action. Mark branchGP a reference prototype; archive
  the session's one-off drivers (jfnk_*, equilibrated_*, x_continuation, sharpen_*, grid_refine_*, seal_test)
  to a `scripts/` or `prototype/` dir.

## Notes
- Each increment is one commit, rollback-able (git as git; the immutability rule is repealed).
- The migration also ISOLATES the divergence: whichever increment first turns the guard RED is the cause —
  diagnosis and construction in one pass.
- Update `migration_convergence_guard._solve()` as the pack/interface grows (pack8 → pack9 with φ → …).
