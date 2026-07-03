# θ₀ at second order DERIVED — and the accumulation law falls out of the same closure
# (the "unclassified accumulation" verdict resolves: the true law is IMPLICIT, which is WHY no frozen form could fit it)

**Date:** 2026-07-02. **Derivation agent:** `a6b59e7212c33361e` (23 shots; STOP-rule armed, never
tripped; the sole code fix was a units bug caught by an internal cross-check before any
comparison). **Blind adversarial verifier:** agent `a954b5c15ec7ee2ca` (5 shots + ~60 cheap 1-D
integrations; own symbolic derivation of every coefficient; own direct θ₀ pipeline; derivation
scripts avoided). **Verdict: E1–E5 ALL CONFIRMED** (E3 with the N≳8 scope; E4's double-counting
attack EXCLUDED a double-count by ~40×; γ-provenance CLEAN — no θ₀-matched quantity anywhere).
Scripts: `cascade_th2_*.py`, `cascade_bv10_*.py`, table `cascade_th2_final_table.json`.
**Status: DERIVED-AT-SECOND-ORDER** (Taylor-ruling instrument; open slivers named below).
Scope: round-static Branch-P reduction, potential-only φ-blind slices, banked pins; N ≳ 8.

## Part 1 — θ₀ derived (the banked hypothesis PART-REFUTED, and better for it)

The banked attribution (O(a²Θ) secular + anharmonic) was PART-CONFIRMED, PART-REFUTED: those
terms are real, derived, and carry the Z- and family-dependence — but supply only ~25–35%. The
**dominant ~65–75% sits at the BOTTOM**: the leading-order launch had imposed the cycle-averaged
background inside the ramp (no cycles there); the self-consistent bottom system closes it.

- **W-orbit reformulation (EXACT; E1):** H≡0 makes the oscillation a zero-energy orbit in
  W(ρ,Φ) = Φ²/(2Zρ²) + U(ρ) − 2 — **Theorem B is literally "the seal is a W=0 turning point"**;
  in dτ = e^φdr, φ drops out; half-cycle phase = √2∫√(Q/W)dρ. One quadrature unifies the
  ρ⁻²-backreaction, ALL-order anharmonicity, and the offset. [Verifier caveat: W(node)=0 per se
  ≡ H-conservation at a node — a solver check; the STRUCTURE is the new content.]
- **Per-node-interval excess (E2, every coefficient verified symbolically):**
  P = πE[2 + (15/16)ĉ₃² − (3/2)ĉ₃ + (3/4)ĉ₄] + π(3ĉ₃/2)δ̂, E = Φ²/(4Z|s̃₁|),
  ĉ₃ = U'''(1)/12|s̃₁|, ĉ₄ = U''''(1)/48|s̃₁| — **U'''' enters at the same order as U'''²**
  (missed in all prior lists). The "2" = 3/2 geometric (ρ⁻²) + 1/2 from Q. Summed:
  ΣP_E ∝ Z(1−x_c)²/Θ (1/N decay + Z-linearity DERIVED); the δ̂-part grows with Θ (scope note).
- **The bottom system (E3, the dominant channel):** exact ramp flux ⇒ universal one-parameter
  system v_ζζ − p·v_ζ + v = 1, ψ_ζ = p, p_ζ = γe^{−2ψ}v_ζ² − p², zero ICs,
  **γ = 4δ̃²/(Z s̃₁² x_c²)** — provenance CLEAN (δ̃, s̃₁ at the seal-root-pinned d*, x_c, Z; no
  free convention, no mod-π freedom). Launch offset z*_eff(γ) replaces the old 0.067π.
  Emergent: **γ(N=8) ≈ 2.33–2.36 across all families AND both Z** — quantization forces γ
  quasi-universal; THIS is the derived reason θ₀ is family- and Z-quasi-stable.
- **Assembly test (no fits, 11 rungs + verifier's own 5):** |Δ| ≤ 0.012π everywhere; verifier's
  independent recomputation from banked pins reproduces 0.3271π/0.2583π vs measured
  0.3209π/0.2533π; the family ordering AND spacing across m=2,3,4 predicted (+0.0107π/step vs
  measured +0.0111π — the mechanism is the ĉ₄ term: Δĉ₄ = 1/2 per m-step).
- **Open slivers (quantified):** the bottom↔oscillation handover, a systematic +2.0% (N=8) →
  +0.9% (N=22) of θ₀ — term-split proven clean, the residual is the flagged O(ε) truncations
  (≈⅓ identified as using z*∞ at finite node count); and the within-cycle parity-alternating
  per-interval structure (the smooth model matches sums, not individual intervals; the O(a)
  turning-point boundary term is identified, not derived).

## Part 2 — THE ACCUMULATION LAW: from "unclassified" to DERIVED (Charles's step 2, closed by step 1's by-product)

The Stage-B/C frozen-fit guard returned "unclassified accumulation" — all five pre-committed
closed forms (power/exponential/log/linear) showed structured residuals, IDENTICAL across all
six ladders. **Now derived: the true law is IMPLICIT — the quantization closure of the bottom
system:**

    **d*(N) solves  z_c_eff(γ(d)) = Θ(N)·√x_c/√(1−x_c),   γ(d) = 4δ̃(d)²/(Z s̃₁² x_c²),
    Θ(N) = (N+1)π + θ₀(N)** (θ₀ from Part 1).

- Verified by the blind verifier's OWN d→γ→z_c_eff chain against banked pins: **−0.38% (N=8),
  +0.08% (N=16), +0.13% (N=22), −0.49% (Z=1 N=8)**; degrades to ~1.3–1.7% at N=4 (asymptotic
  construction; scoped N≳8).
- **This RESOLVES the fit-guard verdict rather than overriding it:** an implicit closure is not
  a power, exponential, or log — the frozen forms COULDN'T fit it, and the identical residual
  sign strings across families are explained by γ's quasi-universality (the law is one
  family-quasi-blind object, exactly as the sign strings hinted). "Unclassified" was the honest
  reading of a law that has no closed form in N — the guard's entire payoff realized: no fit
  ever touched the record, and the derivation arrived by mechanism, not curve-shape.
- Per Charles's directive the fits remain characterization-only; this law enters as DERIVED
  (second-order, scoped) with the two open slivers above as its error budget.

## Provenance ledger
Banked-verified inputs: T3 EOMs/H; flux law; Θ/θ₀ definition + banked measurements; k, Q, s̃₁;
universal-ODE leading launch (reproduced); rung pins; x_c. New-and-now-verified: W-orbit
reformulation; per-node-interval quadrature + analytic coefficients (incl. the U''''-term); the
γ-bottom system + z*_eff + quantization closure; the derived d*(N) law; θ₀ table (9 new direct
measurements + verifier's independent 5); γ quasi-universality. Open: handover sliver; parity
boundary term. Everything above the slivers is closed at its stated order.
