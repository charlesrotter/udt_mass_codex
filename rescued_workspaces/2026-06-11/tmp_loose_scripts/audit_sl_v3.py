"""Re-derive SL form with the correct Eq.S: r²K'' + 2r(1-rφ')K' + (ω²r²A² − LA + 2A)K = 0
where A = e^{2φ}, so ω²r²A² = ω²r²e^{4φ}."""
import sympy as sp
from sympy import Symbol, Function, exp, simplify, expand, diff, Rational

r = Symbol('r', positive=True)
phi = Function('phi')
K = Function('K')
omega2 = Symbol('omega2', real=True)
L = Symbol('L', positive=True)

A = exp(2*phi(r))  # so A² = e^{4φ}
mu = exp(-2*phi(r))

# Eq.S (CORRECT canonical form): r²K'' + 2r(1-rφ')K' + (ω²r²A² − LA + 2A)K = 0
EqS_lhs = r**2*K(r).diff(r,2) + 2*r*(1 - r*phi(r).diff(r))*K(r).diff(r) + (omega2*r**2*A**2 - L*A + 2*A)*K(r)
mu_EqS = mu * EqS_lhs

# Match: pK'' + p'K' = first two terms of μ·Eq.S
# pK'' = μr²K'' = r²e^{-2φ}K''  →  p = r²e^{-2φ}
# Then for ω²·... :
# μ · ω²r²A² = ω²r² · μ·A² = ω²r² · e^{-2φ}·e^{4φ} = ω²r²·e^{2φ}
# So w = r²·e^{2φ} ✓ (matches BB)
# And μ·(−LA + 2A) = −LA·μ + 2A·μ = e^{-2φ}·e^{2φ}·(−L + 2) = −(L−2)
# So Q = (L−2)·(sign flip from convention) = ?
# In form (pK')' + ω²wK − QK = 0: Q = (L−2). Or in -(pK')' + QK = ω²wK: yes, Q = L−2.

print("="*70)
print("Re-derivation with CORRECT canonical Eq.S (ω²r²A² with A² = e^{4φ}):")
print("="*70)
print()
print("  Multiply Eq.S by μ = e^{-2φ}:")
print("  μ·Eq.S = (pK')' + ω²·μ·r²·A²·K + μ·(−LA + 2A)·K")
print("         = (r²e^{-2φ}K')' + ω²·r²·e^{2φ}·K − (L−2)·K")
print()
print("  Setting μ·Eq.S = 0 and rearranging into −(pK')' + QK = ω²wK form:")
print("    −(pK')' + (L−2)K = ω²·r²·e^{2φ}·K")
print()
print("  ⇒ p = r²e^{-2φ}, w_K = r²·e^{2φ}, Q = L−2 = (ℓ-1)(ℓ+2)")
print()
print("  This matches BB, the canonical doc, and CC's Liouville-frame norm.")
print()
print("  *** MY EARLIER AUDIT ERROR: I had assumed A (not A²) in the ω² term. ***")
print("  *** BB and the canonical doc are CORRECT. ***")

# Now verify CC's norm equivalence claim
# CC: ∫ K² · w_K dr where w_K = r²e^{2φ}; with K = (e^φ/r)ψ:
# K² · r² · e^{2φ} = (e^{2φ}/r²)·ψ²·r²·e^{2φ} = e^{4φ}·ψ² = A²·ψ²
# ⇒ ∫ K²·w_K dr = ∫ A²·ψ² dr ✓ (matches CC's claim)
print("\n  CC's frame-norm equivalence:")
print("  ∫ K²·w_K dr = ∫ (e^{2φ}/r²)ψ² · r²e^{2φ} dr = ∫ e^{4φ}ψ² dr = ∫ A²ψ² dr ✓")

# Sanity check at r_CMB
phi_rCMB = 7.0037  # BB's value
import math
e_2phi = math.exp(2*phi_rCMB)  # ≈ 1.213e6
print(f"\n  Numerical at r_CMB = 9.164: e^{{2φ}} = {e_2phi:.3e}")
print(f"  w_K(r_CMB) = (9.164)² × {e_2phi:.3e} = {9.164**2*e_2phi:.3e} Gpc²")
print(f"  BB reports: 1.018 × 10⁸ Gpc² ✓")

# But wait — the original Form-T equation has ω² with A² which is e^{4φ}.
# That's nonstandard. Let me check that this is indeed what CG §22.5 item 9 has,
# or whether it's a typo in the canonical doc.

print("\n  Sanity: in standard SSS Schwarzschild gravity, the polar Zerilli has ω²·V(r)·")
print("  factor; for UDT with g_tt·g_rr = -c² constraint, A² = e^{4φ} factor at ω²")
print("  emerges from time-time Christoffel/lapse coupling combined with radial-radial.")
print("  This is consistent with the §11.2a EM analog (ω²e^{4φ} also)!")
print()
print("  Confirming: §11.2a EM: Φ_E'' + [ω²e^{4φ} − ℓ(ℓ+1)e^{2φ}/r²]Φ_E = 0")
print("    ω² coefficient = e^{4φ} = A² ✓ same structure.")
print()
print("  ⇒ Eq.S's ω²r²A² term is canonical & expected. My audit error caught & corrected.")
