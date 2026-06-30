# D1 determinacy fix — DESIGN SPEC (PROPOSAL, pending Charles's BC sign-off)

**Status:** design only — no code edited, no solve. Several BC choices are FLAGGED premises requiring Charles's
sign-off before implementation (anti-imposition + a derived-junction conflict). Design agent `a71a5861c6058a3e7`,
2026-06-29. Recipe: `GR_NUMERICS_RESEARCH_2026-06-29.md`; matter model = verified RIGID unit field
(`matter_amplitude_native_MAP_2026-06-29.md` — no amplitude DOF; that's a gated import).

## The determined posing (the category-A part — clean, mechanical)
Current: PDE on `body=[3:Nr-3]` (2 of 8 radial layers at Nr=8) + patchwork BCs = **1776 rows / 4224 cols**
(underdetermined by 2448). Fix: impose the 11 coupled rows at ALL non-endpoint layers `[1:Nr-1]` (6 layers) +
**11 closure rows at each endpoint** (core rc, seal ri):
- interior 6×48×11 = 3168 + endpoints 2×48×11 = 1056 = **4224 == cols.** Square/determined.
- The 11 per node = 4 diagonal + 3 off-diagonal Einstein + φ-EL + (2 tangential matter EOM + 1 |n|=1 algebraic,
  imposed at every node). Matter contributes only **2** genuine endpoint BCs per end (|n|=1 fills the 3rd slot).
- Determinacy self-check (cheap, no solve): Jacobian SVD/rank on the new posing → expect rank==4224, null-dim 0
  (vs current min-SV 0.029, null-dim 2448). Guard: if rank<4224, two closure rows are dependent — inspect/replace.

## The BC ledger (the load-bearing part — FLAGS need your call)
Domain is [rc=0.1, ri], **no r=0 node** — the singular n=x/r core is already excised by the finite core rc.
Tags: gauge/regularity/parity = ALLOWED (provenance-only); structure-holding/shape = FLAG.

| field | CORE (rc) | SEAL (ri) | flag |
|---|---|---|---|
| a | **NEW** d_r a=0 (regularity) | a=0 (gauge) | clean |
| b | b=−p (depth dial; **p FREE**, honoring p fixes the D4 bug) | **NEW** d_r b=0 (σ-even Neumann) | clean |
| c | **change** c=0 → d_r c=0 | **change** c=0 → d_r c=0 | **FLAG** |
| d | **change** d=0 → d_r d=0 | **change** d=0 → d_r d=0 | **FLAG** |
| n1,n2,n3 | d_r n̂_⊥=0 (2 tangential; degree from seed homotopy, no Θ-pin) | n̂→vacuum dir (2 tangential; sector label) | confirm sector-not-shape |
| φ | **NEW** d_r φ=0 (finite-core regularity) | φ=0 (canonical interface C-2026-06-10-2) | **FLAG (×2)** |
| e_rt,e_rp,e_tp | e=0 (regularity) | e=0 | **FLAG (seal); parity owed** |

### The three things for Charles to decide
1. **c,d (both ends) + e_* (seal): Dirichlet value-zeros → switch to Neumann (d_r=0)?** TWO reasons this isn't
   just my preference: (a) the current c=0/d=0 **imposes the metric round / no-shear at the boundaries** =
   structure-holding (the imposition the gate forbids); (b) the current Dirichlet **CONFLICTS with UDT's OWN
   DERIVED mirror-fold seal junction**, which gives σ-even fields (A,B,φ,Θ) **Neumann**, not Dirichlet
   (`seal_junction_condition_results.md:66-93,156-159`). So Neumann is *both* less-imposing *and* consistent with
   the derived junction. **Recommendation: yes, switch — it's more correct, not just a choice.** (Off-diagonal
   e_* parity is component-specific — Boyd per-component rule owed before fixing Neumann-vs-Dirichlet there.)
2. **φ tension:** φ(seal)=0 is the canonical matter-cell interface *definition* (C-2026-06-10-2), but the derived
   σ-even junction would say Neumann d_rφ=0. And the new φ-core Neumann rides the posited inner-core treatment
   (a CHOSE). These touch CANON — your call: keep φ(seal)=0 as the interface definition (my lean — it's a
   definition, not a fold-junction), and take φ-core Neumann provisionally.
3. **Matter seal direction-pin** sets the winding sector (charge-1 label). Legitimate, but it pins a direction
   *value* at the seal — confirm it's a sector label, not a shape imposition.
Clean (no decision needed): a (gauge), b (depth-dial; p tagged FREE).

## Biggest IMPLEMENTATION risk (not a BC choice)
Dropping the body excision **re-exposes the core/seal conditioning the excision was hiding** — Chebyshev endpoint
differentiation-matrix amplification on the steep warps (the b1prime header documents flat-space error 1.2e3→3.8e3
growth in the innermost rows with Nr). We must NOT re-excise (that IS D1). Instead handle endpoints via the
**parity/Galerkin basis-recombination** from the research (bakes regularity into the basis, avoids edge
amplification natively) and/or the pole-stable hybrid backbone — and **re-validate the conditioning** (re-run the
flat-space error-growth test). This is the real work; it's why the fix is not a pure flag-flip.

## Owed items now load-bearing (must close before trusting a non-round determined result)
- **SH-exact d/dθ in the GRAVITY sector** (B1/F-4/G8): the off-diagonal Einstein rows are now active at all layers
  → the grid-Legendre d/dθ (exact only at axisymmetry) mixing with the matter SH-exact d/dθ reintroduces the
  non-convergent winding-sin(θ) error. `full3d_grid_shexact.py` exists but isn't wired in. Close it.
- **Per-component tensor/vector parity** (Boyd) for the off-diagonal warps + c,d — pins Neumann-vs-Dirichlet at
  each endpoint; provisional until derived.

## Re-grade plan (after the determined solve converges)
Recompute on the determined field vs the old min-norm values: ρ_max at core, warp magnitudes (max|a..d|, eoff),
charge profile E(<r), caveat #3 warp-comparison. Large movement ⇒ the quantity was seed/Levenberg-set.
Qualitative/topological claims (winding DEGREE, not-a-horizon, gentle-φ) expected to SURVIVE (constrained subspace).

---

## DERIVED BC TABLE (2026-06-29) — supersedes the proposal above; blind-verified CONFIRMED
Derivation agent `aecae703e65ce043b` + blind adversarial verifier `aeb0ab5cfdb351889` (CONFIRMED; hardest attack
on the parity split survived). The BCs are DERIVED from the seal's mirror-fold geometry (per-component reflection
parity in the radial/normal index) + origin r^l regularity at the core + topological degree-conservation — NOT
posited. This CORRECTS the proposal's table (my blanket "off-diagonals → Neumann" was WRONG).

**Frame:** the seal is the φ=0 spatial mirror fold (radial reflection r→2r_seal−r; canon C-2026-06-10-2). For a
C¹ doubled metric across a totally-geodesic reflection surface, parity = (−1)^(#radial indices): odd → Dirichlet
(=0), even → Neumann (zero normal derivative). The t→−t involution is VACUOUS on static fields (governs only the
absent time-arm g_tr), so the static off-diagonals are fixed by the spatial mirror. Core = finite cutoff (NOT a
mirror) → origin r^l regularity (same off-diagonal pattern, different reason).

| field (slot) | #r-idx | SEAL | CORE | provenance |
|---|---|---|---|---|
| a (g_tt) | 0 even | a=0 (gauge fix, allowed) | d_r a=0 (regularity) | DERIVED (+gauge) |
| b (g_rr) | 2 even | Neumann ∂_r b=0 | b=−p (depth dial, **p FREE**) | DERIVED (+ p CHOSE; fixes D4) |
| c (g_θθ) | 0 even | even→Neumann* | even→Neumann* | DERIVED |
| d (g_ψψ) | 0 even | even→Neumann* | even→Neumann* | DERIVED |
| φ | mirror var (odd) | **φ=0** (=domain definition) | d_r φ=0 (regularity, rides rc model) | DERIVED + residue 5a |
| n1,n2,n3 | tangential | 2×tangential Neumann + \|n\|=1; **NO value-pin** | same | DERIVED (degree topological) |
| **e_rt (g_rθ)** | **1 odd** | **Dirichlet e_rt=0** | Dirichlet (~r¹) | DERIVED (CORRECTS proposal) |
| **e_rp (g_rψ)** | **1 odd** | **Dirichlet e_rp=0** | Dirichlet (~r¹) | DERIVED (CORRECTS proposal) |
| **e_tp (g_θψ)** | **0 even** | **Neumann ∂_r e_tp=0** | Neumann | DERIVED (CORRECTS proposal) |

***Even-sector FORM refinement (verifier):** the even/odd classification is firm, but the even-sector condition
in WARP variables is ROBIN, not pure Neumann — e.g. ∂_r(g_θθ)=0 with g_θθ=e^{2c}r² gives c′=−1/r_seal (an
r-power coefficient), not c′=0. **IMPLEMENTATION: impose the parity condition on the METRIC COMPONENT (∂_r g_θθ=0,
∂_r g_ψψ=0, ∂_r g_rr=0, ∂_r g_θψ=0) — the geometrically correct statement — rather than on the bare warp.** This
sidesteps the warp-vs-component subtlety. Classification unaffected.

**Matter pin DROPPED (derived redundant):** the winding degree ∈π₂(S²) is conserved under continuous relaxation
while |n|=1 (changing degree needs |n|=0, forbidden) — so the seal direction value-pin is redundant/over-imposing;
2×tangential-Neumann + |n|=1 suffices. Sector label (degree 1) set by the seed homotopy class.

**Not an imposition (verified):** e_rt=e_rp=0 is the geometric requirement that normal-tangential shear vanish on
the crease; the tangential shear e_tp is left FREE (Neumann). The seal does NOT flatten the metric — STRICTLY LESS
imposing than the old c=d=0 round-pinning table. BCs come from the fold geometry, not from us.

**Determinacy unchanged:** Dirichlet↔Neumann is a one-for-one row swap → rows==cols==4224 at Nr=8. SVD/rank
self-check still owed (cheap) post-implementation.

**Residues (only non-derived choices):** (5a) φ(seal)=0 — corpus leans DOMAIN DEFINITION (C-2026-06-10-2) + the
mirror-odd Dirichlet branch; the competing Neumann reading comes from the (vacuous-here) time involution. Proceed
with φ=0 as the derived default; flag for Charles's canon confirmation (he can overrule). (5b) the rc finite-core
model + p FREE = justified CHOSE (core derived-singular). EVERYTHING ELSE IS DERIVED.

---

## IMPLEMENTED + DETERMINACY VERIFIED (2026-06-29)
The determined posing is implemented as `residual_vector_p1(..., determined=True)` (a branch; the old
`determined=False` path is byte-unchanged, pytest 32/1xfail intact). Determinacy check
(`d1_determined_posing_check.py`, Jacobian SVD at a GENERIC point — the saved converged field — + a
symmetry-broken-seed cross-check):
- **rank == 4224 == cols, NULL-DIM 0** (vs the old null-dim 2448). The D1 underdetermination is FIXED.
  (Seed-only linearization gives a spurious small-SV band from the round symmetry — must check at a generic
  point; both the converged field and seed+noise give null-dim 0.)
- **Conditioning (the predicted risk): smin≈6e-5, smax≈7e6, condition ≈1e11** — full-rank but ILL-CONDITIONED
  (the Chebyshev endpoint amplification from imposing the PDE adjacent to the endpoints). NOT a determinacy
  failure; it is the flagged "real work." Float64 has ~16 digits so ~1e11 is marginally solvable with LM damping,
  but a clean robust re-solve likely needs the parity/Galerkin basis (research recipe) to improve conditioning.
- **STATUS:** determinacy FIXED (banked-pending-blind-verify); conditioning open; re-solve + re-grade next.
- **NEXT:** (1) blind-verify the determinacy (independent rank check); (2) thread `determined=True` through
  newton/continuation, attempt a BOUNDED re-solve (tests whether ~1e11 conditioning is workable or needs the
  basis); (3) re-grade the soft quantities on the determined field; (4) cross-model verify.

---

## RE-SOLVE ATTEMPT 1 (2026-06-29) — determined posing is full-rank but does NOT yet SOLVE (conditioning work needed)
Cold determined continuation (`d1_resolve_and_regrade.py`) STALLED at the EASIEST end: Phi stuck ~8e-3–9e-2 at
X≈−1 (the non-stiff X), with the adaptive X-continuation subdividing uselessly (X=−1.27→−1.004...). DIAGNOSIS:
the stall is **BC-driven, not X-stiffness** — the round seed is FAR from the new derived BCs (e.g. the seed has
∂_r(g_θθ)=2r≠0, but the BC demands ∂_r(g_θθ)=0 → at the finite core c'(rc)=−1/rc=−10, a stiff Robin condition),
and with cond≈1e11 the plain LM (maxit=12/step) cannot floor it. The X-continuation MIS-reads the BC-stall as
X-stiffness and subdivides → death spiral. So: **the determined posing is CORRECT (full-rank, blind-verified),
but the plain LM + X-continuation is the WRONG machinery for it.** This is precisely the design's flagged
"conditioning is the real work, not a flag-flip."

**NEXT PHASE — make the determined posing SOLVE (substantial; deserves fresh context):**
1. **Better initial guess / solver loop:** the stall is BC-satisfaction at fixed X, not X-stiffness — so warm-
   start from the OLD saved field (interior closer) and iterate MANY newton steps at fixed X to satisfy the new
   BCs, rather than an X-continuation from the round seed. Or relax the BCs gradually (BC-continuation).
2. **Conditioning (cond≈1e11):** the research's **parity/Galerkin basis-recombination** (bakes regularity into
   the basis → avoids the endpoint amplification) + Ruiz equilibration / a preconditioner. The design named this.
3. **Re-examine the core Robin BC:** ∂_r(g_θθ)=0 at the FINITE cutoff core gives c'(rc)=−1/rc=−10 (very stiff) —
   is the metric-component Neumann the right regularity at the rc CUTOFF (vs r=0)? The "per-component parity form
   owed" caveat (verifier) lands here. A gentler/correct core regularity form may remove much of the stiffness.
4. Only once it FLOORS: re-grade the soft quantities + blind/cross-model verify.

**STATUS:** D1 determinacy FIXED + blind-verified (the posing is determined). The determined posing does NOT yet
solve (conditioning/BC-stiffness) — the re-grade is BLOCKED on the conditioning machinery above. `determined=True`
stays NON-default until it solves. Old underdetermined path unchanged (pytest 32/1xfail).

---

## P1-(1) CORE-BC FIX + RE-SOLVE ATTEMPT 2 (2026-06-29, fresh session) — CORE ARTIFACT CONFIRMED; solve UNBLOCKED but does NOT yet floor (conditioning is now the rate-limiter)
Driver + derivation agent `aac508665` + blind verifier `a9c669bf8` + symbolic adjudication (in-loop sympy).

### The core-BC FORM was wrong (DERIVED + symbolically verified) — FIXED
The `determined=True` branch had copied the SEAL's metric-component Neumann `d_r(g_thth)=0` to the CORE (rows
222/223/229). At the finite cutoff rc that forces the spurious stiff Robin `c'(rc) = -1/rc = -10` (the coordinate
Jacobian of flattening g_thth=e^{2c}r^2 in r where its areal behaviour is ~r^2) — the RE-SOLVE-ATTEMPT-1 stall.
The CORRECT core regularity is the gentle bare-WARP Neumann `c'(rc)=0` (the round seed satisfies it exactly).
- **Symbolic proof (in-loop sympy, the arbiter):** for the RIGID UNIT hedgehog `T^th_th = (e^{-2c}-e^{-2d})/2r^2`,
  `T^t_t=T^r_r=-(e^{-2c}+e^{-2d})/2r^2`. The ANGULAR block is NOT singularly sourced: T^th_th VANISHES in the
  round/areal gauge (c=d) and is otherwise just gentle c-d warp anisotropy (global-monopole / Barriola-Vilenkin
  structure; the 1/r^2 load sits in the (t,r) block only). => g_thth ~ r^2, c->const, warp-Neumann is correct.
- **Verifier process note:** the blind verifier CONFIRMED the conclusion but tried to refute the mechanism
  (claimed T^th_th=2eta^2/r^2). That number is an AMPLITUDE-model algebra error (spurious f^2 term; the resolved
  matter model is the rigid unit field, no amplitude). Adjudicated by the symbolic calc above — NOT taken on
  authority. KEPT from the verifier: (a) the false-pass warning (determinacy is BLIND to which core form is
  correct — this is a MERIT call on the derivation, not the SVD; noted in code); (b) the residual conditioning
  risks (phi-log core pin + Chebyshev endpoint amplification), both since confirmed.
- **Implemented:** `p1_residual_general_einstein.py` rows 222/223/229 core slots `drg(.,.)[core]` -> `G.d_r(c|d|e_tp)[core]`.
  pytest 32/1xfail intact (default path unchanged). DETERMINACY PRESERVED (`d1_determined_posing_check.py`:
  null-dim 0, rank 4224). Conditioning improved only modestly (cond ~1.2e11 -> ~8e10; smax~7e6 UNCHANGED = the
  endpoint amplification, a separate source the BC fix does not touch).

### RE-SOLVE ATTEMPT 2 (warm-start from old field, FIXED X=-2e5, determined posing) — UNBLOCKED, not floored
`d1_resolve_and_regrade.py` (edited: cold X-continuation -> warm-start fixed-X LM). 60 iters, 6791s, Nr=8 G kap8=1.
- **Phi: 6.34e10 (warm-start, new posing) -> 9.594e-2 over 60 MONOTONE-ACCEPTED steps** at the PRODUCTION X=-2e5
  (attempt-1 death-spiraled at the EASY X~-1). The BC-form fix removed the stall: Phi drives 11 orders down.
- **Does NOT floor (<1e-6):** from it~16 a slow ~4%/step LINEAR tail = the residual cond~1e11 (endpoint
  amplification / possible phi-log) is now rate-limiting. More LM iters won't fix a conditioning-set RATE.
- **VERDICT:** "BC-form artifact" CONFIRMED (removable, was the binding stall). "re-solve floors with just the BC
  fix" was OVER-OPTIMISTIC — the parity/Galerkin basis + Ruiz equilibration (Category-A conditioning) is
  genuinely needed to floor the determined solve. This is the design's long-flagged "conditioning is the real work."

### RE-GRADE — PROVISIONAL ONLY (Phi=9.6e-2 not floored; numbers NOT banked)
Qualitative (expected to survive, and do at this partial): winding Q_interior=0.990 (old 0.977); |n|=1 exact;
phi in [-0.0012,0.0080] gentle; lapse exp(a)_min=3.21 (>0, NOT a horizon). Quantitative (UNTRUSTWORTHY until
floored): warp max|a,b,c,d|=3.06 (old 1.02); eoff_max=1.76 (old 0.11); rho_max=8.3e-3 (old 0.18). These MOVED a
lot but the solve is not converged — re-grade for real only after the conditioning build floors it.
Field saved `solved_fields_nr8_G_kap8_1_DETERMINED.pt` (PROVISIONAL/partial — do not treat as a result).

### THE FORK (for Charles): build the conditioning machinery now, vs fold into time-live
D1 determinacy is FIXED+verified; the core-BC artifact is FIXED+verified; the solve is UNBLOCKED but needs the
conditioning build (Ruiz equilibration first — cheap; then parity/Galerkin basis) to floor + give a trustworthy
re-grade. Per fix-all-flaws-before-dynamic this is a static RED gate to clear before time-live; and the same
conditioning machinery the time-live solver needs anyway. Recommendation: build it (equilibration-first), floor
the static determined solve, re-grade — but this is the deliberate "real build" decision LIVE flagged for Charles.

---

## CONDITIONING INVESTIGATION (2026-06-29) — equilibration INSUFFICIENT (structural); -> parity/Galerkin or integration-preconditioner build (Charles's call)
After the core-BC fix, the determined posing is UNBLOCKED (solve descends) but does NOT floor: cond~1e9-1e11 is
the rate-limiter. Tried the cheap rung (Ruiz equilibration) thoroughly; it is structurally insufficient:
- **attempt-3 (per-iter Dr+Dc, accept on ||F||^2):** instant STALL at it=0 — row reweighting makes the step a
  non-descent direction for the un-weighted objective.
- **attempt-4 (FROZEN Dr0, accept on ||Dr0 F||^2 -- the consistent fix):** descends in the Dr0 metric (16.4->4.0
  over 80 iters, no stall) BUT the TRUE ||F||^2 ends at 7.0e3 (WORSE than the 9.6e-2 start; eoff 0.11->9.0). The
  ~5000x Ruiz weight spread effectively DELETES the down-weighted endpoint equations -> solver lets their true
  residuals blow up. The re-grade from this field is GARBAGE (NOT banked). [it also overwrote the attempt-2
  partial field -- do not warm-start from `solved_fields_nr8_G_kap8_1_DETERMINED.pt`, it is the attempt-4 garbage.]
- **offline diagnostic (`d1_equilibration_diag.py`):** row+col Ruiz -> cond 3e5 (but objective-corrupting);
  COLUMN-ONLY (objective-preserving) -> cond ~1e9 with a genuine near-null direction (smin~6e-9).
- **VERDICT (recorded negative):** the ill-conditioning is STRUCTURAL — Chebyshev DIFFERENTIATION-matrix endpoint
  amplification (d_r ~O(N^2) at rc, ri), reintroduced by imposing the PDE adjacent to the endpoints + derivative
  BCs. Rescaling cannot fix it (the only objective-preserving rescaling leaves cond~1e9). The equilibration code
  (`ruiz_scales`, `_col_scales`, `newton_solve_p1(equilibrate=True)`) is RETAINED as a tool but does NOT floor it.

**DECISION (Charles, 2026-06-29):** build the principled discretization fix (he chose "build the parity/Galerkin
basis" over a last cheap test or deferring). REFINEMENT before building: the generic parity/r^l recombination is
flagged (research) for SMOOTH r=0 origins, but our domain is a finite shell [rc,ri] with a genuinely SINGULAR core
-> the r^l smoothness does not hold at rc, and the cleaner corpus fix for O(N^2) Chebyshev endpoint amplification
may be INTEGRATION / quasi-inverse (ultraspherical, Olver-Townsend) preconditioning. So: Phase 1 = targeted corpus
research (which well-conditioned spectral method for our annular singular-core coupled mixed-BC system); Phase 2 =
build it + revalidate conditioning (flat-space error-growth test + cond measurement; confirm the F=0 root is
unchanged) + re-solve + re-grade. OPERATIONAL FIX owed: run the next solve with UNBUFFERED output (python3 -u, no
grep pipe) -- the attempt-4 grep pipe block-buffered the per-iter log and hid progress for ~2.5h.

---

## SOFT-MODE CHARACTERIZATION (2026-06-29) — the near-null directions are DERIVED SYMMETRIES, not a flaw (no imposition)
Charles's steer: "derive the path, don't make choices by assertion." So we CHARACTERIZED the 2 near-null
directions (smin~1e-4) instead of imposing a gauge. Result (`d1_softmode_characterize.py`, at the old field;
single-point, blind-verify owed before banking — but the signal is clean):
- **smin SVs ~ [9.1e-5, 3.3e-4]** (NOT the 6e-9 quoted earlier — that was the attempt-4 GARBAGE linearization
  point; at a clean field smin is ~1e-4).
- **Soft mode #1 (SV 9.1e-5):** 77% matter energy; **79% overlap with the DERIVED hedgehog rotation generator
  omega_z x n** (from the matter action's SO(3) invariance). Perturb u->u+eps*v: gauge-invariant observables
  (winding Q, rho_max, lapse_min, max warp) DO NOT MOVE (dQ=0, d-obs ~1e-5 negligible) while the residual changes
  only at SECOND order (|dResidual| ~ eps^2: 0.13/2.1/13.4 at eps 0.05/0.2/0.5 = pure quadratic -> linear response
  ~smin*eps is negligible, confirming near-null). => **mode #1 IS the matter SO(3) ROTATION symmetry** (the
  z-rotation the axisymmetric grid leaves soft). DERIVED, benign.
- **Soft mode #2 (SV 3.3e-4):** off-diagonal-metric dominated (e_rp/e_tp), 0% rotation overlap, 7% matter.
  Invariants likewise unmoved => a **metric DIFFEOMORPHISM (coordinate) gauge mode** (confirmed gauge by
  invariant-preservation; full Lie-derivative generator-match owed if we want it pinned down, but not needed).
- **CONCLUSION (answers Charles): NOTHING TO IMPOSE.** The soft directions are the UDT action's OWN rotation +
  coordinate invariances. The solution is fully determined in every PHYSICAL direction; the gauge orbits are
  handled by the LM damping automatically (it regularizes the soft SVs). So smin is NOT a flooring obstruction.
- **=> the ONLY remaining flooring obstruction is smax~7e6** (Chebyshev endpoint differentiation amplification) —
  a pure Category-A NUMERICAL technique (mapped/declustered grid or integration preconditioner), no physics choice.

---

## NON-FLOORING RESOLVED: it's solver GLOBALIZATION, NOT a posing inconsistency (2026-06-30)
The determined solve does not floor even at the well-conditioned X=-1 (Phi stuck ~2e-3, crawling ~0.3%/iter).
Decisive test (`d1_lsfloor_test.py`, SVD of the determined Jacobian at the X=-1 field): project F onto range(J).
- **F is 99.9% REDUCIBLE** (reducible 2.092e-3 of Phi 2.095e-3; the irreducible left-null/LS floor from the
  4608-vs-4224 over-determination is only **2.67e-6**). So the posing is CONSISTENT — a near-exact solution exists.
- => the non-flooring is **slow convergence (solver globalization)**, NOT a wrong BC / over-determination / physics
  inconsistency. The reducible residual lives in the SOFT directions of J (the benign gauge/rotation modes, small
  SV); the LM's uniform lam*I damping suppresses exactly those while the strong nonlinearity (warps~2.6) makes the
  full step overshoot -> the solver can't efficiently take the step that demonstrably EXISTS.
- **Whole conditioning/flooring saga resolves cleanly:** determinacy FIXED, core-BC FIXED, smax = the X=-2e5 KLUGE
  (pivoted to explore X), soft modes = benign DERIVED symmetries, posing = CONSISTENT, non-flooring = solver
  globalization. Every layer was fixable or benign — none indicted the metric. (Good for solver trust.)
- **NEXT (building): a better Newton step** — SVD-pseudoinverse + line-search (regularize only genuinely-null
  directions, take the reducible directions directly, scale by what the nonlinear residual accepts) replacing the
  uniform-damped LM. Category-A globalization. Then the determined solve should FLOOR -> trustworthy re-grade.

---

## GALERKIN BASIS: CONDITIONING FIXED, but the cold run floors to a SPURIOUS branch (2026-06-30 EOD; honest)
`galerkin_basis.py` (BC-recombined radial basis) + `newton_solve_p1(step='galerkin')` (change-of-vars du=B@da;
physics unchanged; lm default byte-stable, pytest 32/1xfail). Conditioning FIXED: cond(J@B) -38x, near-edge modes
lifted. Seal-BC reconciliation (commit 80d8e37): residual seal rows b,c,d,e_tp changed to the warp-Robin form the
basis uses (c'(ri)=-1/ri; e_tp'(ri)+(2/ri)e_tp=0; == d_r(g_*)=0 in continuum; Category-A; 1/ri,2/ri DERIVED geometry,
registered "/ G.ri" in test_solver_integrity). Without this the projection catapulted Phi 2e-3->7e7 (residual used
SPECTRAL d_r(g_thth), basis used analytic warp -> inconsistent at Nr=8).
- **WORKS for conditioning:** cold round-seed galerkin descends 6 orders (23.8 -> 1.5e-5) where LM/equil/KTE/SVD all
  crawled at 2e-3.
- **BUT the floored field is SPURIOUS (`d1_gauge_check.py`):** the 1.5e-5 residual is 100% in the PHYSICAL singular
  band (0% gauge) => UNDER-CONVERGED, still moving; and the observables moved alarmingly vs the old crawl-floor:
  dilaton phi_max 0.90->0.021 (nearly dead), max warp 2.57->10.1, rho_max 0.0097->3e-8, lapse 0.55->0.31 (Q~1 only).
  The cold galerkin run (big steps from the far round seed) overshot into a degenerate extreme-warp/dead-dilaton
  branch, NOT the physical compact object. **The re-grade is NOT valid on this field.**
- **NEXT (resume): gentler globalization / PHYSICAL warm-start** -- LM-to-close (the physical basin), THEN galerkin
  to POLISH near it -- so the floor lands on the RIGHT branch. (The cold-galerkin overshoot is a globalization bug,
  not a basis or conditioning failure; the basis + seal-BC reconciliation are correct and banked.)
