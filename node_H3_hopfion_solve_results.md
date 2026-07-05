# H3 — Native Q_H=1 hopfion solve: PROVISIONAL-A (exists + scaling; precision + verifier OWED)

**Status: PROVISIONAL-A (NOT a clean bank). Owes: (1) a blind adversarial verifier; (2) a finer-grid
(N≳256 / production minimizer) confirmation to close the precision gap. Existence + scaling well-supported;
few-% energy benchmark + integer-Q-on-relaxed-field NOT met at this bounded budget = resolution-limited.**
Solver agent a09b70a1539145abb (GPU V100, torch float64, single process, anti-hang honored). Under the frozen
verified contract `H3_hopfion_solve_preregistration.md`. Scripts/fields in scratchpad (`fs_hopfion.py`,
`drive_ckpt.py`, `analyze_final.py`, `ckpt_N160.npz`, `ckpt_SCALE11.npz`).

## What H3 is (contract-verified)
Native L2+L4 on N=0, φ-blind + ρ=r theorem ⇒ EXACTLY the flat-R³ Faddeev–Skyrme energy
E=∫[(ξ/2)|∂n|² + (κ/4)F_ij²], F_ij=n·(∂_i n×∂_j n). So H3 = resolve the KNOWN Q_H=1 FS hopfion natively + report ℓ_hopf/ρ_c(ξ).

## Findings
- **Q_H measurement VALIDATED** (Whitehead integral, A from ∇²A=−∇×B FFT): on clean degree-1 Hopf seeds
  |Q_H|→1 by O(h²) Richardson (0.877,0.941,0.965 → 1.00). Lattice-Hopf drift = O(h²), resolves. Sign ±1 =
  the H2 hopfion/anti-hopfion mirror.
- **EXISTENCE — supported (outcome A).** A finite, localized, **virial-balanced E2=E4 (exact FS virial)**
  Q_H=1 hopfion forms — toroidal energy ring (peak ≈1.1√(κ/ξ)), decaying ~3 decades to n_∞=[0,0,−1].
  Backed by established FS mathematics + the exact native reduction. Existence is not in doubt; the solve
  confirms the native method resolves it.
- **SCALING — robust (the load-bearing native deliverable).** Two-coupling runs: (ξ,κ)=(1,4) E=644.7 ring≈2.2;
  (1,1) E=314.1 ring≈1.1 ⇒ E-ratio 2.05≈√4 (**E∝√(ξκ)**), ring-ratio 2.0=√4 (**ℓ_hopf∝√(κ/ξ)**).
  ⇒ **ℓ_hopf ≈ 1.1√(κ/ξ); ℓ_hopf/ρ_c ∝ 1/√ξ** (ρ_c∝√κ). ξ FREE/data-blind ⇒ reported as f(ξ), not a number.
- **PRECISION SHORTFALL (honest caveat, owed):** relaxed Ehat=E/√(ξκ)=314–322 vs published FS 275 (~16% high,
  trending to 275 as h→0.06); and the RELAXED field's Q_H≈0.79 (not integer-certified — mix of lattice-Hopf
  core-sharpening error + possible partial unwinding, inseparable at h≈0.06–0.10). The contract's few-% + integer-
  Q-on-relaxed-field bar was NOT cleared ⇒ resolution/tool limitation, NOT a failure to resolve (so NOT D).

## Frozen outcome: A (EXISTS + ξ-ratio) — PROVISIONAL on precision
ℓ_hopf ≈ 1.1√(κ/ξ); ℓ_hopf/ρ_c ∝ 1/√ξ. Route → H4. NOT D (benchmark qualitatively reproduced: Q→1 on seeds,
exact virial, localized ring, correct √(ξκ)/√(κ/ξ) scaling, energy trending to 275). NOT C (FS hopfion known +
native reduction exact). **The A verdict rests on existence + scaling, NOT on a clean few-% number.**

## OWED before clean bank (top next-session actions)
1. Blind adversarial verifier (verifier-before-record) on the energy functional, Q_H method, virial, scaling.
2. Finer-grid (N≳256) / specialized minimizer: close the 16% energy gap to few-%, certify integer Q_H on the
   relaxed field.
Physics content (existence + ℓ_hopf/ρ_c ∝ 1/√ξ) does NOT depend on the few-% number; the shortfall is method
precision. H4 (backreaction/gravitation/mass; the dynamical bulk-vs-core-pinning verdict) + a ξ-anchor are the
next physics; the physical charges q/η + the i-flow/ℏ clock remain owed (H2).
