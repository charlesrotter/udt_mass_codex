<!-- Auto-generated 2026-06-29 by the solver-audit-broad-sweep workflow (21 agents, 7 regions A-G, each finding adversarially verified). Run id wf_aefc200c-936. Same-model verification; cross-model reserved for the first time-live PHYSICS result. -->

# UDT Mass Codex — Solver Audit Synthesis (2026-06-29)

*Synthesized from six region audits (A-operator, B-matter, C-geometry, D-driver, E-tests, F-legacy, G-completeness), each with an adversarial verifier verdict. "Confirmed" below means the verifier returned `real`; `not-adversarially-checked` items are observation/plan/incompleteness notes (carried per the synthesis spec); `false-positive`/`uncertain` are dismissed or flagged in §5.*

## 1. Executive Summary

**The live static path is TRUSTWORTHY in its physics core but NOT yet clean enough to extend blindly — the verdict is FIX-FIRST on a short, bounded list, not a hard BLOCK.**

What is solid (time-live inherits this): the live operator (`p1_residual_general_einstein.py` → `branch_operator.py` → `b1prime_3d_offround_residual.py`) is a genuine **derived scalar-tensor extension**, not a smuggled GR adoption. The verifier confirmed (A7, G10, C6/C7, B5/B6, E6): the Einstein-tensor backbone is the textbook EH identity (category-A reference, not a smuggle); the native-S² 3-component matter EL is correct, e^{2φ}-weighted consistently on both matter and gravity sides, with the L4 quartic numerically validated as the S² area-form; |n|=1 is a gauge-fix, not a charge imposition, and the imported S³/Skyrme core is genuinely retired from the live path; inv4x4/det4x4 are correct and dodge the V100 broadcast-Cholesky pitfall; and the provenance/anti-imposition gates (`tests/`) are confirmed physics-blind (no merit drift). JFNK/LM/jacrev/X-continuation/the pole-stable hybrid are all category-A technique, correctly out of scope.

What must be addressed before the dynamic build:
- **Determinacy of the banked static result (D1, HIGH).** The static system appears **underdetermined at the grids actually used** (body mask `[3:Nr-3]` + most fields carrying a single BC). At Nr=8 — the grid `check_winding_survival.py` ran — only **two interior radial layers** carry field equations; the damped-LM augmented lstsq makes the rank-deficient step solvable, so residual-smallness may be regularized by seed+Levenberg rather than pinned by the metric. The banked "winding SURVIVED" verdict should be **re-graded** under a determinacy check (singular-value spectrum / numerical rank at the converged point) and a resolved interior grid before it is carried into a costlier dynamic solve. This is the single most load-bearing concern; it was an incompleteness observation (not adversarially re-run), so it needs a cheap confirming check, not acceptance on faith.
- **Two un-derived/un-tagged FREE inputs ride live results (A2, D5).** The e^{2φ} field-matter weight is live in production yet the project's own `solver_action.py` flags it as a not-derived CHOSE; and the live drivers silently ride `xi=kap=1.0` (function defaults) while the docs say production is `2e-2` (50× off), untagged at the call site. Both are surfaced/tagged *somewhere* (so not hidden smuggles) but not at the banking surface.
- **The SH-exact d/dθ asymmetry is an open verify item (B1/F-4/G8).** Matter differentiates θ with the SH-exact operator; the gravity sector still uses the grid Legendre operator (exact only at axisymmetry). LIVE.md already lists this as owed; it must be closed (verify, don't assume) before a non-round/dynamic solve inherits and amplifies a non-convergent winding-sin(θ) error.

What does **not** block: the dynamical/time sector (G1, G2) being blank is *expected* — time-live is the intended next build, not a gap to patch. The off-diagonal wiring on the **live** path is correct (see §3-ii). The proliferation/consolidation items are hygiene, important to do before time-live spawns yet another driver but not correctness blockers.

## 2. Confirmed Findings by Severity

### HIGH

**D1 — Static system is underdetermined at every grid used (incompleteness).**
`p1_residual_general_einstein.py` residual_vector_p1 (lines 197-217) + `full3d_spectral.py` body mask (lines 129-130, `body[3:Nr-3]`). Interior rows enforced only on `[3:Nr-3]`; most fields carry one BC (a: seal only; b: core only; φ: seal only; matter n1/n2/n3: no BC). Row/col = 12·Nr−59 vs 11·Nr unknowns → underdetermined for Nr<59 (short 51 eqns/column at Nr=8, where the winding result ran). LM augmented lstsq (`Jaug=[J; sqrt(lam)·I]`, lam→1e-14) makes the rank-deficient step solvable. **Recommendation:** treat residual-smallness as necessary-not-sufficient; report J's singular-value spectrum / numerical rank at convergence; add the missing BCs or justify the over-parametrization; re-grade the winding-survival result on a grid where the interior is resolved (note `[3:Nr-3]` excises the steep core layers where the soliton lives).

**G1 — Criterion 7 (dynamical character) is a GAP (incompleteness).**
The grid `(Nr,Nth,Nps)` has no time axis; every gradient hardcodes `d_t=0` (`full3d_spectral` grad_coords line 146; `b1prime` coord_grad line 73; einstein_mixed builds dg only for R/TH/PS). Only the elliptic static residual is assembled. **This is the intended next build, flagged so it is not mistaken for "nearly complete":** turning on time is architectural (add a time axis / Fourier-in-t / evolution scheme; replace the `d_t=0` hardcodes; add the 3 time-row off-diagonal unknowns + rows), not a flag-flip.

### MEDIUM

**A2 — The e^{2φ} field-matter weight, flagged NOT-derived, is LIVE (import; real, adj. high→medium).**
`b1prime_3d_offround_residual.py` E_mixed lines 168-172 (`-kap8·f·Tmix`, f=e^{2φ}) and `p1_residual_general_einstein.py` _el_matter_s2_weighted lines 164-173 (`fw=f·√g·wvol`). `solver_action.py` lines 110-125 tags `matter_weight` as MIGRATION-DEFERRED, "explicitly-FLAGGED CHOSE … NOT derived … must be DERIVED or DROPPED at migration — do NOT add to pass a test"; `matter_regrade_derived_operator_results.md` R3 independently tags it CHOSE. It changes the matter field equations (not category-A). Verifier downgraded to medium because honesty is satisfied (tagged in three places) and R3 records the load-bearing ∇E≠0 conclusion is matter-weight-independent. **Recommendation:** derive e^{2φ}·L_m for field matter natively or drop to weight 1; until then tag every live field-matter result "rides the un-derived e^{2φ} matter weight" in the premise ledger.

**D5 — Live drivers ride `xi=kap=1.0`, not the documented production `2e-2`, untagged (approx/provenance; real).**
`p1_residual_general_einstein.py` driver entry points default `xi=1.0, kap=1.0`; `check_winding_survival.py:58` passes only positional p, kap8 → xi,kap inherit 1.0; line 39 hardwires `MAT.stress_tensor(...,1.0,1.0)`. Docs say production `XI_PROD=KAP_PROD=2.0e-2` (`branch_operator.py:86-87`, FREE; `b1prime` header line 17). These are matter-Lagrangian couplings (physics, not method); the chose-or-derived trigger lists them as FREE requiring tags. The winding verdict rides couplings 50× off the documented regime, with the script docstring omitting xi/kap entirely. Mitigation: `xi=kap` keeps L=√(kap/xi)=1, so only the overall matter-gravity coupling magnitude differs. **Recommendation:** decide whether native-S² production xi,kap are 1.0 (fix the docs) or 2e-2 (pass them explicitly); tag at every banking call site.

**C1 — Off-diagonal metric DOF frozen at zero in the superseded residual path while its off-diagonal Einstein rows are still imposed (frozen-dof; real, adj. high→medium).**
`full3d_newton.py` residual_vector_vsafe lines 130-155 (and `full3d_spectral.residuals` lines 322-337): unpack returns only `(a,b,c,d,Th)`; build_metric is diagonal; yet rows for (R,TH),(R,PS),(TH,PS) are appended, and `einstein_3d_weyl_gen.py` confirms G_1_2/G_1_3/G_2_3 are nonzero for a diagonal Weyl metric depending on (r,θ,ψ). The docstring "off-diagonals are FREE to grow … for a genuine 3-D shape" (full3d_spectral lines 37-39) is contradicted by this path. **Important:** the verifier confirmed `p1_residual_general_einstein.py` (the LIVE path) re-routes through the general 4×4 Einstein with e_rt/e_rp/e_tp as live unknowns (pack11/unpack11), so this is a **superseded diagonal residual path**, not the live solve. **Recommendation:** amend the overclaiming docstring; retire the diagonal path or drop its off-diagonal rows; any banked result that rode `residual_vector_vsafe`/`full3d_spectral.residuals` and concluded roundness is biased by this freeze and should be checked.

**B1 / F-4 / G8 — Gravity sector uses grid-Legendre d/dθ; matter uses SH-exact d/dθ (incompleteness; one issue, three regions).**
Matter: `free_s2_matter.field_dn_components_exact` → `spectral_sph_exact.dtheta_exact_torch` (introduced because the GL-μ operator `-sin(θ)·Dμ` mis-differentiates winding sin(θ) at ~0.18 error, non-convergent Nθ=6..20). Gravity: `b1prime` E_mixed → `full3d_spectral.einstein_mixed`/`einstein_mixed_weyl` via `Grid3D.d_th` (GL Legendre, exact only for μ-polynomial / m=0). Agreement is trivial in the round/diagonal regime (θ-independent stress → θ-independent metric), but the off-diagonal rows are LIVE; a non-axisymmetric metric mixes an SH-exact RHS (T) with a grid-inexact LHS (G). `full3d_grid_shexact.py` already overrides `Grid3D.d_th` for both sectors but is NOT imported by the live path. LIVE.md:104 lists this as owed. **Recommendation:** run the named verify — substitute SH-exact d/dθ into the gravity rows (or cheap saved-field re-eval) at the working Nr; if the residual moves, wire SH-exact into the live gravity sector. m=0 round regression is bit-identical.

**A5 — operator==EL proof covers only the GR-baseline φ=0 slice (incompleteness).**
`tests/test_operator_from_action.py` test_residual_assembles_einstein_eq lines 114-147 sets φ=0 (where E_mixed_branch degenerates to G−kap8·T), reconstructs with the same engine (self-labeled a regression lock, not an EL proof); the matter-stress autograd test verifies the *unweighted* Hilbert T, not the e^{2φ}-weighted source. The derived operator's f-terms, X-kinetic, and φ-EOM EL-correctness at nonzero φ rest on the b1prime docstring + "validated upstream." **Recommendation:** add an autograd EL test at nonzero φ — differentiate ∫√−g[fR + Xf(∂φ)² + f·L_m] w.r.t. g^{μν} and φ, compare to E_mixed/EL_phi_3d.

**E1 — Smuggled-literal lint never scans the modules with the real derived-operator math (incompleteness).**
`tests/test_solver_integrity.py` test_no_smuggled_literal_in_operator (lines 157-175) scans only 3 functions in `p1_residual_general_einstein.py`. The actual physics literals live in `b1prime_3d_offround_residual.py` E_mixed/EL_phi_3d and `branch_operator.py`, which are only *called*, never literal-scanned. A re-introduced smuggled coupling inside E_mixed would not be flagged. **Recommendation:** extend the scan to E_mixed/EL_phi_3d/EL_Th_3d and branch_operator's operator functions, or narrow the test docstring to the assembly layer only.

**E2 — X_PROD has no machine-enforced provenance-tag check (incompleteness).**
`branch_operator.py:85` `X_PROD=-2.0e5  # FREE`. KAP8/XI_PROD/KAP_PROD each get a tag-presence test; X_PROD (the most physically loaded FREE coupling — dilaton kinetic/curvature ratio, ghost+Cassini bound) gets none. **Recommendation:** add X_PROD to the tagged-coupling assertions.

**G3 — Criterion 9 (stability spectrum) is a GAP on the current 11-field object (incompleteness).**
No Hessian/eigenvalue/persistence analysis on the converged complete-operator solution; earlier stability work was on different objects. "A particle = a stable solution." **Recommendation:** establish a constraint-respecting static stability notion (fixed-metric Hessian over-counts, per the gravitating-soliton memory) before/as part of the dynamic build.

**G4 — Criterion 6 (topological sector): only m=1 explored (incompleteness).**
`migration_convergence_guard.py:45 M=1`; seed is degree-1 `n=x/r`. Higher sectors unexplored; the catalog over topological sectors is sampled at one point. **Recommendation:** can ride along into time-live as an m=1-conditioned scope stamp, but name the multi-sector catalog as blank.

**G6 — Criterion 10 (regime of validity): warp-trend convergence not closed (incompleteness).**
Characterization is a 2-grid (Nr=8,10) trend, no Richardson/3rd grid; caveat #1 ("Nr=12 required") open; strong-field horizon hypothesis kept alive. The spectral argument shows the *smooth* sector is resolved, but that is a characterization argument, not a convergence proof. **Recommendation:** close the warp-trend (Nr=12 or a verifier-accepted argument) or carry the convergence caveat as a stamp on every time-live result built on this base.

### LOW

**A4 — `branch='G'` is an untagged default of the UNRESOLVED G/P fork (honesty; real, adj. medium→low).** `branch_operator.py` E_mixed_branch line 113, residual_vector_p1 line 176. The fork is a free physics choice documented UNRESOLVED, but the call surface carries no chose/derived tag (the honest "defaulting to G" note lives only in another file's migration_note). Mitigated: docstring names it explicit, invalid branches raise, tests lock the behavior, and `migration_convergence_guard.py` runs BOTH branches. Mislabeled as frozen-dof — it is config selection, not a frozen field DOF. **Recommendation:** carry an explicit ledger tag at the call surface; label single-branch banked results scoped-to-branch.

**C5 — Latent NameError in `full3d_spectral.matter_action` (bug; real).** Lines 262-270: returns `S, L, n, dn, Gmn, SS` but `n` is never bound (field_n not called). Dead/latent — `winding_catalog_map.py:102-117` explicitly avoids it for this reason. **Recommendation:** delete the function or fix the return.

**D4 — `seed_round_native` ignores its `p` argument and seeds `b` with sign opposite its own BC (bug; real).** `p1_residual_general_einstein.py` lines 112-122: body uses literal `-1.0*(1-s)` not `-p*(1-s)`; sets `b=1.0*(1-s)` (docstring says "minimal"); at core gives b=+1 while the BC drives b(core)=−p. The sibling `p5d_timelive.py:130` honors p correctly. Affects convergence robustness, not the converged fixed point (Newton relaxes b regardless), but the dead `p` is a latent trap. **Recommendation:** honor p, reconcile the b-seed with the b(core)=−p BC.

**E3 — Premise-ledger sync is vacuous for single-char tokens 'X' and 'p' (incompleteness).** `tests/test_solution_space_gate.py` lines 207-219: `if token not in f.read()` always passes for single chars. **Recommendation:** anchor 'X'/'p' to distinctive substrings (`X_PROD`, `b(core)=p`).

**G5 — Criterion 8 (branch/bifurcation) is PARTIAL (incompleteness).** G/P operator fork + X-family covered; only one seed relaxed per branch, no multi-seed bifurcation map. Can ride along; name it so "both branches done" is not read as "the static catalog is mapped."

## 3. The Four Concrete Items

**(i) Does the GRAVITY sector need the SH-exact d/dθ?** **OPEN — must verify, do not assume (B1/F-4/G8, medium).** Confirmed by reading: matter uses `spectral_sph_exact.dtheta_exact_torch`; gravity (einstein_mixed/_weyl and the f/kinetic terms) uses `Grid3D.d_th` = the GL grid Legendre operator, exact only at m=0/axisymmetry. They agree at machine zero in the round/diagonal regime currently characterized (θ-independent stress), so the *banked round result is not contaminated*. But the off-diagonal rows are live and the metric carries r²sin²θ factors, so a non-round/dynamic solve would mix an SH-exact RHS with a grid-inexact LHS — reintroducing the non-convergent winding-sin(θ) error the matter fix removed. The fix already exists (`full3d_grid_shexact.py` overrides `Grid3D.d_th` for both sectors) but is not wired into the live `p1`/`branch_operator`/`full3d_spectral` path. **Action:** run the cheap saved-field re-eval (substitute SH-exact d/dθ into the gravity rows, check the metric residual at the working Nr); if it moves, wire SH-exact in. Close before time-live.

**(ii) Is the off-diagonal wiring correct everywhere?** **Correct on the LIVE path; NOT everywhere.** The live `p1_residual_general_einstein.py` carries the **3 spatial off-diagonals (e_rt, e_rp, e_tp) as live unknowns** (pack11/unpack11) routed through the general 4×4 Einstein (the b1prime hybrid: analytic Weyl backbone + `[einstein_mixed(g_full) − einstein_mixed(g_diag)]` bracket) — verifier-confirmed correct and pole-stable. The off-diagonal *placement* machinery in `full3d_spectral.build_metric` (symmetric, correct areal/geometric-mean scaling) and `einstein_mixed` (full 4×4) is also confirmed correct (C7). **Two caveats:** (a) the **superseded** diagonal residual path (`full3d_newton.residual_vector_vsafe`, `full3d_spectral.residuals`) **freezes** e_rt/e_rp/e_tp to zero while still imposing their Einstein rows, and carries a contradicting "FREE to grow" docstring (C1, medium) — retire or fix it; (b) the **3 time-row off-diagonals (g_tr, g_tθ, g_tψ) are zero** (G2) — this is correct and tagged for a *static* metric (THEORY-pinned, not a hidden freeze), and is precisely the DOF time-live must turn on. So: live spatial off-diagonals correct; time-row off-diagonals are the next-build target; the stale diagonal path is the one wiring inconsistency to clean up.

**(iii) Consolidation / retirement plan (one canonical solver + harness).** This reconciliation is **OWED per CLAUDE.md and not done** (A1, A3, C2, D6, F-1/2/3/5, G7). Proposed canonical set:
- **CANONICAL static solver:** `p1_residual_general_einstein.py` (11-field, native-S²) → `branch_operator.py` (derived G/P operator) → `b1prime_3d_offround_residual.py` → {`whole_metric_3d_core`, `whole_metric_3d_matter`, `einstein_3d_eval`/`einstein_3d_weyl_gen`, `einstein_3d_general_eval`/`einstein_3d_general_gen`, `full3d_spectral` (grid + `einstein_mixed` utility), `spectral_cheb`, `spectral_sph`}; matter `free_s2_matter` → `spectral_sph_exact`; `solver_pack`. Harness = `tests/`.
- **RETIRE/ARCHIVE (git mv):** the diagonal residual path `full3d_newton.residual_vector_vsafe` + `full3d_spectral.residuals` and their S³-hedgehog matter (C2; callers energy_minimizer, cross_grid_branch, divT_excised, full3d_campaign, full3d_final_run — migrate or archive); `prototype/branchGP_native_s2_coupled_OBSERVE.py` (rigid-θ hedgehog matter, no off-diagonals — confirm Branch-P reproduces through p1's G/P switch first, G7); the redundant flooring drivers (`jfnk_floor_driver`, `jfnk_equil_floor`, `jfnk_branch_solver` vs the documented `equilibrated_lm_floor`) — name ONE canonical floor driver in INDEX §2; the dead `einstein_general_hybrid` in p1 (live residual uses the duplicate in b1prime.E_mixed — D6); zero-importer Einstein evaluators `gen_einstein_3d_general.py`, `einstein_3d_general_filtered.py`, and `axisym_einstein_analytic.py` (F-2).
- **Repo-wide archival pass (F-1):** 1086 flat root `.py` (511 native_*, 152 w*, 65 importing retired solvers); compute the transitive closure of tests/ + p1 + prototype drivers; `git mv` everything outside it (and not cited in INDEX §3) to `archive/`. The live closure is ~17 modules.
- **Doc corrections owed:** `solver_action.py` is stale — it declares a GR-baseline but the live operator is the derived scalar-tensor theory (A1, HIGH-consolidation); either rewrite it as the source-of-truth for the DERIVED action or mark it historical and point to branch_operator + the regrade docs. Single-source the constants (A3: `XI_PROD/KAP_PROD=2e-2` are dead on the live path which rides 1.0; `kap8` prose says 0.05 but live is 1.0). Fix INDEX §2 (F-5: full3d_solver.py and spectral_radial_soliton.py are listed "import-critical" but are off the live graph). Tidy stale docstrings (B2 S³ Skyrme text in whole_metric_3d_matter; B4 "exact" claim in field_dn_components; E4 stale xfail reason).

**(iv) Import / frozen-dof / approximation pass result.** **No smuggled GR-form or imported mechanism on the live operator path** (A7, C6, G10 — Einstein-as-EH-identity is category-A; hybrid + X-continuation are category-A technique). The real findings are provenance/honesty/completeness, not mechanism imports: **un-derived e^{2φ} matter weight live (A2)**, **untagged xi=kap=1.0 vs documented 2e-2 (D5)**, **untagged branch=G default (A4)**, plus the **two code bugs (C5 NameError dead code, D4 seed sign/ignored-p)**, and the **frozen DOF in the superseded diagonal path (C1)**. The S³ hedgehog (C3) is confirmed test-excised from the live residual and labeled retired (not a live import). The exp/det clamps (B3, D7) are category-A overflow guards, not approximations fed downstream. The kap8=1-vs-½ normalization (A6) is **uncertain** but physically inert (degenerate with the free couplings xi,kap) — a label-hygiene item, not a solve-affecting bug.

## 4. Completeness-Map Grade

Re-graded against the ten criteria (live solver = `p1_residual_general_einstein.py`, 11 fields, derived G/P operator + native-S² matter, kap8 characterization confirmed run on THIS path):

| # | Criterion | Grade | Note |
|---|-----------|-------|------|
| 1 | Fields | **PARTIAL TILE** | 7/10 metric DOF live (4 diagonal + 3 spatial off-diag); 3 time-row off-diagonals frozen (G2, correct for static) |
| 2 | Action terms | **TILE** | fR, X-kinetic, f-weighted L2+L4, Branch-P U, seal BCs — EL-consistent; rides FREE couplings (G9) |
| 3 | Full equations | **TILE (static)** | 4 diag + 3 off-diag Einstein + φ-EL + 3 matter EOM + |n|=1; time-mixed G^t_i vanish identically (correct omission) |
| 4 | Domain & coords | **PARTIAL** | r,θ,ψ live; t frozen (d_t=0 hardcoded) |
| 5 | Boundary & regularity | **TILE** | seal/depth-dial/φ(seal)/winding-from-homotopy/edge-excision; load-bearing CHOSE values tagged |
| 6 | Topological sector | **GAP** | m=1 only (G4) |
| 7 | Dynamical character | **GAP (headline)** | static/elliptic only (G1) |
| 8 | Branch/bifurcation | **PARTIAL** | G/P fork + X-family; no multi-seed map (G5) |
| 9 | Stability spectrum | **GAP** | never computed on the 11-field object (G3) |
| 10 | Regime of validity | **PARTIAL** | smooth sector resolved at Nr=8; warp-trend convergence not closed (G6) |

**Time-live INHERITS as solid foundation:** the derived G/P scalar-tensor operator (EL==operator tested at φ=0; full nonzero-φ EL test still owed, A5); the pole-stable general 4×4 Einstein machinery — crucially `full3d_spectral.einstein_mixed` **already carries all off-diagonals**, so the tensor algebra for time-row coupling exists; native-S² 3-component matter + |n|=1 + grid-exact d/dθ; the X-continuation stiffness fix; finite-cell BC structure; spectral grid + autograd EL.

**Gaps time-live would CARRY:**
- *Must be the build, not a flag-flip:* add a time axis + replace d_t=0 everywhere + add the 3 time-row off-diagonal unknowns/rows (G1, G2) — architectural.
- *Should close BEFORE time-live:* the static stability notion (G3 — time-live needs a persistence notion); the warp-trend convergence caveat (G6 — under-resolution compounds in a costlier solve); the determinacy check (D1 — do not carry an unpinned base forward); the gravity SH-exact d/dθ verify (B1/F-4/G8 — a differentiation error would be inherited and amplified).
- *Can ride along as stamped scope:* m=1-only (G4), single-seed bifurcation (G5), FREE couplings X/xi/kap + CHOSE BCs (G9) — provenance clean, just conditioned.
- *Hygiene before time-live spawns another driver:* the consolidation/retirement plan (§3-iii).

## 5. Dismissed False-Positives (do not re-chase)

- **B3, D7 — exp/det clamps as "approximations."** Category-A float64 overflow/positivity guards; exact below threshold; the converged solution is asserted never to touch the clamp; hadronic depth is deep-*negative* φ (e^{2φ}→small), nowhere near the max=60 positive cap. Optional: add a runtime telemetry assert. *(Verdict: false-positive.)*
- **C3 — S³ hedgehog as a smuggled import.** Self-labeled "Unit S³ hedgehog"; test-excised from the live residual (`tests/test_solver_integrity.py:263-270` asserts field_n/field_dn absent + carrier is the 3-vector); documented retired. Provenance honesty met. *(false-positive.)*
- **C4 — c,d=0 core/seal BCs "undocumented."** Actually documented in the owning `full3d_solver.py` (docstring line 14, inline 79-80, "c,d regular … round limit"); these are endpoint Dirichlet BCs, not a frozen DOF. *(false-positive; minor cross-module doc nit only.)*
- **D3 — jacobian vmap-safety claim "violated" = a bug.** The docstring "no linalg inside" is genuinely stale (delegated operator uses linalg.inv/det), but Newton accepts a step only on TRUE forward-residual decrease, so an inexact Jacobian can only slow/stall, never accept a wrong solution; the live path converged to floor. Stack is torch 2.5.1+cu121 where linalg.inv/det have vmap rules; the V100 pitfall is specifically broadcast-Cholesky solve_triangular. *(false-positive; fix the stale comment, optional FD spot-check.)*
- **G2 — time-row off-diagonals "frozen-dof, HIGH."** g_ti=0 IS the definition of a static spacetime; documented and tagged in two places; LIVE.md already scopes the off-diagonal-completion claim to the spatial ones. *(false-positive; it is the legitimate static boundary and the named next-build DOF.)*
- **A6 — kap8=1 vs the doc's ½ (uncertain).** A hand-variation disputes the in-code verbal reconciliation, but the coefficient is **exactly degenerate** with a rescale of the free couplings xi,kap (no solve can distinguish 1 from ½), so it cannot affect any result — a "DERIVED=1" label-hygiene item, not a bug. A cheap committed numeric check would pin the label.

---

**VERDICT: FIX-FIRST before the time-live build.** The physics core is trustworthy and no mechanism/GR-form is smuggled. Close this bounded list first: (1) **D1** — confirm the static solution is determined (rank/SVD at convergence) and re-grade the winding result on a resolved grid; (2) **B1/F-4/G8** — run the gravity SH-exact d/dθ verify; (3) **A2 + D5** — resolve/tag the un-derived matter weight and the xi=kap provenance at the banking surface; (4) **G3** — establish a static stability notion; (5) **§3-iii consolidation** — retire the superseded diagonal/prototype solvers to one canonical solver+harness so time-live does not branch off a proliferated base. The two code bugs (C5, D4) and the doc-staleness (A1, A3, INDEX, B2/B4/E4) are cheap and should go with the consolidation pass. The dynamical/stability/topology *gaps* (G1, G4-G6) are the build itself or stamped scope, not blockers. Do not begin time-live on top of an undetermined, unconverged, asymmetric-θ static base.

---

## D1 RESOLUTION (2026-06-29, blind-verified `a5e07d7` + localization)

**D1 is CONFIRMED.** Independent recompute: residual = **1776 equations / 4224 unknowns** at Nr=8; Jacobian full
ROW rank 1776 (all rows real — min row-norm 0.85, none padded/dependent; smallest SV 0.029) → **null space = 2448**.
Row accounting verified: 1152 body (12 blocks × 96 body pts on `[3:Nr-3]`) + 624 BC = 1776. Φ=9.13e-22 does NOT pin
the solution; 58% of DOF are seed/min-norm-set. NOT Nr-fixable (rows<cols to Nr≈59) — a formulation flaw.

**Null-space localization (`d1_nullspace_localization.py`):** 85% of the 2448 unconstrained directions live in the
EXCISED core/seal layers; BODY layers carry only 14.5%; φ is least-affected (3% of null weight); warps ~37%, matter
~33%. **Impact MIXED:** qualitative/topological banked claims SURVIVE (winding DEGREE = topological; not-a-horizon =
gross features; gentle-φ = constrained subspace); quantitative core-dominated numbers are SOFT (ρ_max, warp
magnitudes, charge profile) and need re-grade on a determined formulation; caveat #3 warp-comparison wants a re-look.

**Action:** fix the formulation (impose interior PDE on all non-endpoint layers / complete BCs so rows≈cols, a
determined well-posed BVP), then re-grade the quantitative results. Top fix-first item, before time-live.
