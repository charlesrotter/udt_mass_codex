"""Re-derive SL form carefully. Multiply Eq.S by e^{-2φ}."""
import sympy as sp
from sympy import Symbol, Function, exp, simplify, expand, diff, Rational

r = Symbol('r', positive=True)
phi = Function('phi')
K = Function('K')
omega2 = Symbol('omega2', real=True)
L = Symbol('L', positive=True)

# Eq.S: r² K'' + 2r(1−rφ') K' + (ω²r²A − LA + 2A) K = 0
# A = e^{2φ}
A = exp(2*phi(r))

# Multiply by e^{-2φ}:
mu = exp(-2*phi(r))
EqS_lhs = r**2*K(r).diff(r,2) + 2*r*(1 - r*phi(r).diff(r))*K(r).diff(r) + (omega2*r**2*A - L*A + 2*A)*K(r)
mu_EqS = mu * EqS_lhs
mu_EqS_expanded = sp.expand(mu_EqS)
print("μ·Eq.S expanded:")
print(sp.pretty(mu_EqS_expanded))

# Now check: -(pK')' + QK − ω²w_K K = 0  with p, w_K, Q TBD
# This is equivalent to: -p K'' - p' K' + Q K − ω² w_K K = 0
# OR multiplying by -1: p K'' + p' K' − Q K + ω² w_K K = 0
# 
# So if we want μ·Eq.S = +p K'' + p' K' + (...) K  to match this ansatz:
#   p = μ r² = e^{-2φ} r²
#   p' K' coefficient must equal μ · 2r(1-rφ') = 2r e^{-2φ}(1 - rφ')
#   d/dr(r² e^{-2φ}) = 2r e^{-2φ} - 2r² e^{-2φ}·φ' = 2r e^{-2φ}(1 - rφ') ✓
#
# Then: μ·Eq.S = (pK')' + μ·(ω²r²A − LA + 2A) K = 0
#              = (pK')' + (ω²r² − L + 2) K = 0   [since μ·A = 1]
#              = (pK')' + ω²r² K − (L−2) K = 0
#
# Compare to ansatz: pK'' + p'K' − QK + ω² w_K K = 0
# i.e., (pK')' − QK + ω² w_K K = 0
# Match: ω² w_K K = ω² r² K → w_K = r²
#       −QK = −(L−2)K → Q = L − 2

print("\n  *** Direct match: ***")
print("    p   = r² e^{-2φ}")
print("    w_K = r²            (NOT r² e^{2φ})")
print("    Q   = L − 2 = (ℓ-1)(ℓ+2)")

# So BB's claim of w_K = r² e^{2φ} is mismatched.
# Let me check the alternative form. Maybe BB uses canonical SL form:
#  -(pψ')' + QΨ = ω² w Ψ  with ω² w Ψ being the "right side" of eigenvalue problem
# Substituting: ω² · r² · K is the RHS, so w = r² regardless of side convention.

# Maybe BB is computing the "canonical SL norm" weight via the integration measure
# from variational form? Let me check by computing the L²-norm dx-measure such that
# ω²-eigenproblem is positive-definite.

# Actually: perhaps BB's claim is that the SL operator L = -(pK')' + QK with
# weight w (the normalization for the inner product) needs w such that
# < L φ, ψ >_w = < φ, L ψ >_w. Self-adjointness on ∫ (Lφ) ψ w dr, integration by parts:
# ∫ -(pφ')' ψ w dr = -[pφ' ψ w]_a^b + ∫ pφ' (ψw)' dr
# For self-adjointness via Lagrange ID, w must be such that w·1 = 1·w in product. 
# Standard Hilbert space for SL: ∫ φ ψ w dr where ω² w appears on RHS.
# So w is determined by where ω² appears: ω² w K = ω² r² K  →  w = r².

# CONCLUSION: BB's claim w_K = r² e^{2φ} is INCORRECT.
# The correct w_K is r² (φ-independent).

print("\n  ⇒ BB's stated w_K = r² e^{2φ} is INCONSISTENT with the SL-form")
print("    derivation BB describes (multiply Eq.S by e^{-2φ}).")
print("  ⇒ The CORRECT w_K = r² (also φ-independent).")
print("  ⇒ This is a bookkeeping error in BB's report and the canonical")
print("    doc CG §23.5 paragraph that quotes 'w_K = r² e^{2φ}'.")
print("    The physics (Q φ-independent, p = r²e^{-2φ}, Robin BC) are unaffected.")
print("    But Lagrange-identity, integration measure, and CC's frame translation")
print("    need this corrected.")

# Cross-check via the integral-norm equivalence claim.
# BB says: K-frame norm with w_K = r²e^{2φ} equals Liouville norm with weight A² (= e^{4φ}).
# CC's K = (e^φ/r)ψ, so ∫ K² · w_K dr = ∫ (e^{2φ}/r²) ψ² · r²e^{2φ} dr = ∫ e^{4φ} ψ² dr ✓
# This IS what CC computes. So if BB's w_K = r²e^{2φ} is correct, then norm equivalence holds.
# But if w_K should be r² (from SL-derivation), then K² · r² = (e^{2φ}/r²) ψ² · r² = e^{2φ} ψ²
# ∫ e^{2φ} ψ² dr would be the Liouville-frame norm — different from BB's ∫ A² ψ² dr = ∫ e^{4φ} ψ² dr.
# CC integrates ∫ A² ψ² dr — corresponding to BB's w_K = r²e^{2φ}.

# So which is right?  Let me recompute the SL form more carefully — maybe I'm missing a factor.

print("\n  Re-deriving from scratch:")
print("  Eq.S: r²K'' + 2r(1-rφ')K' + (ω²r²e^{2φ} − Le^{2φ} + 2e^{2φ})K = 0")
print()
print("  SL form: -(pK')' + QK = ω² w K  (Sturm-Liouville eigenvalue problem)")
print("  Expanding: -pK'' - p'K' + QK = ω² w K")
print()
print("  Multiply Eq.S by some μ(r):")
print("    μr²K'' + μ·2r(1-rφ')K' + μ(ω²r²e^{2φ} − Le^{2φ} + 2e^{2φ})K = 0")
print()
print("  To match: -p = μr² (sign-flip allowed)")
print("    Then -p' = μ·2r(1-rφ') is automatic if p = -μr² with μ = e^{-2φ}.")
print("  Hmm, sign of p is conventional. Let's pick p = -μr² → p = -r²e^{-2φ}? No, p>0 by convention.")
print("  Actually: standard SL has p > 0. So we want pK'' + p'K' = (pK')' to MATCH the form")
print("    of μr²K'' + μ·2r(1-rφ')K'.")
print("  So pK'' = μr²K'' → p = μr² = r²e^{-2φ} > 0 ✓")
print("  And p'K' must equal μ·2r(1-rφ')K' = 2r e^{-2φ}(1-rφ')K' ")
print("    p' = d/dr[r²e^{-2φ}] = 2re^{-2φ} − 2r²e^{-2φ}·φ' = 2re^{-2φ}(1-rφ') ✓")
print()
print("  So μ·Eq.S = (pK')' + μ·(ω²r²A − LA + 2A)K = 0")
print("  Now -(pK')' + QK = ω²wK ⇒ (pK')' − QK + ω²wK = 0")
print()
print("  Matching: μ·(ω²r²A − LA + 2A) = ω²w − Q")
print("    Splitting: ω² · μr²A = ω² · w → w = μ·r²·A = e^{-2φ}·r²·e^{2φ} = r²  ✓")
print("    And: μ·(−LA + 2A) = −Q → Q = μ·(LA − 2A) = e^{-2φ}·e^{2φ}·(L−2) = L−2  ✓")
print()
print("  ⇒ DEFINITIVE: p = r²e^{-2φ}, w_K = r², Q = L − 2.")
print("  ⇒ BB's stated w_K = r²e^{2φ} is INCORRECT.")
