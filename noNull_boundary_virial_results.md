# Boundary-virial closure before F — RESULTS

**Date:** 2026-07-16 · **Dispatch:** `UDT_H3_BOUNDARY_VIRIAL_CLOSURE_BEFORE_F_DISPATCH.md` · grok
**Observing or targeting:** OBSERVING (does |δ_vir| fall as the wall recedes? — both outcomes reportable). DATA-BLIND.
**Verifier status:** independent verifier `verify_noNull_boundary_virial.py` **PASS 38/38** (own
orientations/stress/quadrature/scalars + all decision-table predicates); CAS identity verifier
**PASS 4/4** (after correcting a sign my first EL transcription got wrong — caught BY the CAS pass;
production numerics unaffected, they use the audited `grad_noNull`).
**NOT claimed:** the L→∞ limit (forbidden by dispatch from a bounded scout); an exact lattice Noether
theorem (V3 is a convergence test); any native-UDT mass; V4 fields as production carriers (scout only).

## §2.1 G evidence gap — CLOSED
Deterministic rerun of the exact G commands: verifier PASS 90/90 again, ZERO non-timing scalar diffs
vs commit 493d104 (committed-JSON SHA-256s recorded); both raw logs captured (the omission was
`.gitignore:12 *.log`). Committed here.

## V1 — identity DERIVED + CAS-verified
E₄−E₂ = ∫S dV = B_∂Ω + W_res (finite domain), hence **M_N⁽⁰⁾ = E_carrier + B_∂Ω (+W_res)** under the
conditional EH lapse premise. Record: `noNull_virial_identity_derivation.md` (with the corrected-sign
note); CAS: `verify_virial_identity_cas.py` → 4/4.

## V2 — exact discrete scale response: EXACT
E(λ)=λE₂+λ⁻¹E₄ verified to worst rel **2–4e-16** (gate 1e-9) at all grids and ε; ∫S=E₄−E₂ to 9e-15;
dE/dlnλ = E₂−E₄ confirmed. Interior residual work W_res = −0.084 at 256³ (1.0% of the gap; Cauchy
bound 0.46). The gap is an exact conjugate response of the fixed-box family.

## V3 — localization + surface stress: CONVERGING, NOT CLOSED
- NEW: E₂ localization (G had only E₄): inside the a=2.5 cube, E₄ fraction 99.5–99.6% but E₂ only
  **85.5–86.3%** — an **E₂-rich boundary skin** (the pinned wall forces the hopfion tail), exactly
  where box support must live. V(2.95)=19.4 > full gap 8.8 ⇒ the outer shell carries large NEGATIVE ∫S.
- Surface closure error |V−B−W|/|V| at a=2.95: **33.3% (128³) → 15.4% (192³) → 8.5% (256³)**.
  Successive empirical powers p = log(e_i/e_{i+1})/log(h_i/h_{i+1}) = **1.88 and 2.07** —
  approximately SECOND order over these three grids (an empirical observation, NOT a proven
  asymptotic order; three points cannot establish a theorem). [CORRECTED 2026-07-16 audit patch:
  the original text characterized this as ≈O(h); the measured powers are ≈2.] Face placement
  (site vs half-cell) shifts B by ≤0.4%. Label: **surface construction CONVERGING (~h² empirically);
  local boundary theorem OPEN**.

## V4 — bounded fixed-spacing box scout: MONOTONE AND CLEAN (both h)
| box | h | L | E | δ_vir | Q_fwd | ‖g_f‖_M⁻¹ |
|---|---|---|---|---|---|---|
| N=128 | h_c | 6.00 | 271.831 | −0.05211 | −0.9673 | 0.041 ✓ |
| N=160 | h_c | 7.51 | 270.790 | −0.04390 | −0.9679 | 0.012 ✓ |
| N=192 | h_c | 9.02 | 270.329 | −0.03793 | −0.9683 | 0.020 ✓ |
| N=192 | h_f | 6.00 | 274.181 | −0.03627 | −0.9862 | 0.017 ✓ |
| N=240 | h_f | 7.51 | 273.073 | −0.02560 | −0.9865 | 0.010 ✓ |

- |δ_vir| decreases monotonically with L at BOTH resolutions (×0.84, ×0.86 per step at h_c; ×0.71 at h_f).
- E decreases as the wall recedes (the box was confining); topology and charges stable; all
  criticality gates met without loosening; θ_max stable; core localization unchanged.
- Literal 1/L fits [CORRECTED 2026-07-16 audit patch — the original "fine-pair intercept ≈ 0"
  phrase is DELETED as unsupported]: gap intercepts: coarse 3-point **+2.537** (slope +69.9);
  fine 2-point **−4.759** (slope +88.2). |δ_vir| intercepts: coarse 3-point **+0.0100**; fine
  2-point **−0.0168**. The fine two-point intercepts are NONPHYSICAL/UNSTABLE (negative gap is
  impossible; two points cannot constrain an intercept) and support **no limit inference**; the
  coarse three-point intercept is likewise h-contaminated. **No intercept is identifiable from this
  scout.** Raw numbers reported; **no limit claimed**.

## Decision-table outcome
V2 exact ✓; V4 |δ_vir| decreases cleanly with L at both h ✓; V3 converging but not closed at
available h. Allowed conclusion (rows 1–2 of the dispatch table, graded honestly):

**BOX-STRESS LEAD (STRONG on the V2 exact response + V4 two-resolution monotone scout): the fixed-box
virial gap is carried by boundary dilation stress — the E₂-rich pinned-wall skin. The local surface
theorem (V3) remains OPEN pending finer grids or the analytic boundary-layer treatment. Infinite-volume
closure remains OPEN.**

Standing status (unchanged from the dispatch box): M_N⁽⁰⁾=2E₄ conditional Gauss/lapse identity;
M_N⁽⁰⁾=E_carrier OPEN (∫S≠0 at finite box); boundary-stress explanation now a STRONG LEAD, not proven.

**STOP: F not run.**
