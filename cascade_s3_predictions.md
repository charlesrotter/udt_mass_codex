# s3 PRE-REGISTERED prediction table — written BEFORE any T1–T6 measurement
Date: 2026-07-03 (stage-3 soft-mode identification agent). Rungs: B00 (m=3,Z=8,a*=1.4813439655),
SM2 (m=2,Z=8,a*=0.9860738239), SZ1 (m=3,Z=1,a*=1.4942743252). Seed data (banked, bv14):
soft eig (mass-normalized FREE full form, non-translation near-zero) at M/2M:
B00 -3.8398e-7/-3.8318e-7 (M=6348), SM2 -2.8023e-7/-2.7994e-7 (M=5963), SZ1 -3.3221e-8/-3.3220e-8 (M=6835).

## Candidates
C1 genuine converged shallow negative; C2 exact continuum zero approached from below (grid artifact
in the sign); C3 fixed-U shadow of the solution-manifold tangent (the (a, phi_c) critical curve,
anchor-relaxation); C4 scale/homothety (fold-breathing; u=-r phi', v=rho-r rho', alpha=0, beta=r_s;
known Jacobi residual J_rho=-(e^{2phi}/4)(rho U''+U')); C5 detuning/shooting (d/dphi_c at fixed a;
u(0)=1 Jacobi field; known to fail the v(r_s) natural BC).

Rung-selection premise (read off the machinery, tagged DERIVED-from-code): a* is pinned by the seal
pair {phi(r_s)=0 (event), rho'(r_s)=0 (odd-fold/even-rho mirror)}; cons_res = 2 rho'_s^2 ~ 1e-11 in
all three backgrounds confirms. The manifold tangent (C3) is the (delta_a, delta_phi_c, delta_r_s)
null direction of the linearized pair.

## Predictions (stated before the numbers)

### T1 Richardson (deflated soft eig at M, 2M, 4M[, 8M])
- C1: converges to finite negative; |lambda(h)-lambda_inf| = O(h^2) with lambda_inf < 0.
- C2: |lambda| -> 0 from below, ~x4 shrink per doubling (O(h^2)) or other p>0. NOTE: seed data
  (0.2%/0.003%/0.1% change under one doubling) already strains C2 UNLESS the undeflated value is
  translation-contaminated; the deflated Richardson is the decider.
- C3/C4/C5: converged finite value equal to that direction's Rayleigh quotient (T1 alone cannot
  separate C1 from C3/C4/C5; it only kills or supports C2).

### T2 anatomy (deflated eigenvector at 2M: alpha,beta content; u/v weight; r-localization)
- C3: u(0) = delta_phi_c generally nonzero; beta nonzero; alpha=0; fields spread through the cell.
- C4: the specific homothety shape — u(0)=0 (u=-r phi', phi'(0)=0), v(0)=1 (v=rho-r rho'), beta=r_s
  (large fold-motion fraction), alpha=0.
- C5: u(0)=1, v(0)=0, beta=-u(r_s)/phi'_s, alpha=0.
- C1/C2: no shape prediction (a genuinely distinct direction; low overlap with all of C3-C5).
- Control: translation content ~0 after exact projection.

### T3 W-overlaps (deflated soft mode vs candidate directions at 2M)
- Support C3/C4/C5 iff overlap >~0.9 with that direction AND grid-stable; all overlaps <~0.3
  supports C1/C2. Translation overlap (control) < 1e-6-ish (exact projection).
- da/ds of the tangent: if the tangent is ~parallel to fixed-U space (da/ds ~ 0) C3 becomes hard to
  distinguish from C1 by T3 alone; if da/ds is O(1) the "shadow" interpretation carries a large
  off-space component and its RQ need not match lambda_soft.

### T4 ANCHORED (u(0)=0) vs FREE, same grids
- C1: soft eig ~unchanged (continuum mode not tied to u(0)).
- C2: ~unchanged (zero in both columns).
- C3: killed/shifted substantially IFF its u(0)=delta_phi_c component is significant; if measured
  delta_phi_c/||tangent||_W ~ 0, T4 does not discriminate C3 (state the measured value first).
- C4: unchanged (homothety u(0)=0 exactly); also predicts ABSENT in FIXED (beta=r_s) — consistent
  with the banked FIXED datum.
- C5: KILLED (u(0)=1 is exactly the anchored-out direction). Stage-2 already reports the soft mode
  present in ANCHORED = strong prior strain on C5; T4 quantifies.
Known stage-2 datum (FREE=ANCHORED pairs at all three fundamentals) is a PRIOR, not this test.

### T5 exact-action ray probe (S[bg + eps*mode], both signs, eps 1e-3..1e-1 of natural scale)
- C1: Delta S = c2 eps^2 with c2 ~ lambda_soft(grid) < 0, quadratic through the range.
- C2: the EXACT functional should show c2 ~ 0 (continuum-accurate evaluation), i.e., a measured c2
  much smaller in magnitude than lambda_soft(grid) — mismatch c2 << lambda supports C2.
- C3/C4/C5: c2 = that direction's RQ; quadratic; possible cubic turn from fold-motion/anharmonicity
  (report shape, no verdict from shape alone).
- Built-in validation: c2 must match the discrete lambda_soft if the moving-endpoint handling is
  right (S(eps) = S(0) + eps^2 * x^T Q x + O(eps^3) for W-normalized x).

### T6 universality scaling (raw table, no fits)
lambda ratios (B00:SM2:SZ1) = 11.6 : 8.4 : 1 (from seed data).
- C4 predicts tracking of the homothety RQ ratios across rungs.
- C3 predicts tracking of the tangent(-shadow) RQ ratios.
- C5 predicts tracking of the shooting-direction RQ ratios.
- C2 predicts tracking of grid scales (h^2-ish), not any physical direction's scale.
- A-priori comparator U'(rho_c)^2 = (0.0746^2 : 0.0557^2 : 0.0229^2) = 10.6 : 5.9 : 1 (noted BEFORE
  measurement; raw comparison only).

## Budget (pre-declared)
- Nonlinear IVP shots (hard cap 10): 0 planned background shots (cached s2 pickles + bv14 arrays);
  up to 3 seal-extension continuations (T5 moving-fold tail, 1/rung, short integrations from the
  seal state); up to 3 spare background re-shoots ONLY if a cached pickle fails validation.
- Linear variational (Jacobi) integrations off the cached dense background (not nonlinear shots,
  ledgered anyway): 2 per rung (Y_a, Y_phi_c) + tolerance re-runs; <= 12 total.
- Machinery reused: cascade_bv14_lib.py (assembly, orderings, band inertia, translation vector),
  bv14 mass convention (lumped h; v0,vM half; alpha,beta weight 1) so eigenvalues are comparable to
  the banked seed numbers; backgrounds from cached s2_bg_*.pkl dense interpolants (validated against
  bv14_bg_*.json scalars before use).
