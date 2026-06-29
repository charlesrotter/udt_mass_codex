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
