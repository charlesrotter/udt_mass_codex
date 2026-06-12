"""Carefully derive the SL form of Eq.S to verify p, w_K, Q."""
import sympy as sp
from sympy import Symbol, Function, Rational, simplify, expand, diff, exp

r = Symbol('r', positive=True)
phi = Function('phi')
K = Function('K')
omega2 = Symbol('omega2', real=True)
L = Symbol('L', positive=True)  # ℓ(ℓ+1)
A_expr = exp(2*phi(r))

# Eq.S homogeneous (set H=0 since BB notes elimination is done already):
# r² K'' + 2r(1−rφ') K' + (ω²r²A − LA + 2A) K = 0
EqS = r**2*K(r).diff(r,2) + 2*r*(1 - r*phi(r).diff(r))*K(r).diff(r) + (omega2*r**2*A_expr - L*A_expr + 2*A_expr)*K(r)
print("Eq.S =", EqS)

# Try multiplying by μ = ?
# General SL form: -(pK')' + QK = ω² w_K K  (homogeneous source-free)
# Expanding: -p K'' - p' K' + Q K = ω² w_K K
# i.e., -p K'' - p' K' + (Q − ω² w_K) K = 0
# Multiply by −1: p K'' + p' K' + (ω² w_K − Q) K = 0

# We want: μ · Eq.S to have form: p K'' + p' K' + (ω² w_K − Q) K = 0
# Match coefficients:
#   μ · r² = p
#   μ · 2r(1 − rφ') = p'
#   μ · (ω²r²A − LA + 2A) = ω² w_K − Q
# 
# Decomposing the K coefficient: ω² (μ r² A) − μ A (L − 2) = ω² w_K − Q
# So w_K = μ r² A and Q = μ A (L − 2)
#
# We have p = μ r². So p' = μ' r² + 2μ r. But we need p' = μ · 2r(1 − rφ') = 2μr − 2μ r² φ'
# Equate: μ' r² + 2μr = 2μr − 2μ r² φ'  →  μ' = -2μ φ' → μ = exp(-2φ).

# So μ = e^{-2φ}, p = r² e^{-2φ}, w_K = e^{-2φ} · r² · e^{2φ} = r²
# w_K = r² (φ-INDEPENDENT)
# Q = e^{-2φ} · e^{2φ} · (L − 2) = L − 2

mu = exp(-2*phi(r))
p_derived = mu * r**2
w_K_derived = mu * r**2 * A_expr
Q_derived = mu * A_expr * (L - 2)

print(f"\np = {sp.simplify(p_derived)}")
print(f"w_K = {sp.simplify(w_K_derived)}")
print(f"Q = {sp.simplify(Q_derived)}")

# So the correct answer is:
# p = r² e^{-2φ}
# w_K = r²  (NOT r² e^{2φ})
# Q = L − 2

# Verify by direct substitution: μ * Eq.S
muEqS = mu * EqS
muEqS_expanded = sp.expand(muEqS)
print(f"\nμ·Eq.S = {muEqS_expanded}")

# Check: p K'' + p' K' should equal first 2 terms of μ·Eq.S
p_Kpp = p_derived * K(r).diff(r, 2)
pp_K = sp.diff(p_derived, r) * K(r).diff(r)
SL_LHS = p_Kpp + pp_K + (omega2 * w_K_derived - Q_derived) * K(r)
diff_check = sp.simplify(muEqS - SL_LHS)
print(f"\nμ·Eq.S − [p K'' + p' K' + (ω² w_K − Q) K] = {diff_check}")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("""
The CORRECT SL identification is:
  p   = r² e^{-2φ}    [matches BB]
  w_K = r²             [does NOT match canonical doc 'r²e^{2φ}']
  Q   = L − 2          [matches BB up to overall sign convention]

The canonical doc states 'w_K = r² e^{2φ}' which is INCORRECT under straightforward
multiplication by μ = e^{-2φ}.  The correct weight is w_K = r².

UNLESS — BB's convention is multiplying by a DIFFERENT integrating factor or using
a different convention that absorbs e^{2φ} differently.  Let's check by trying
NO multiplication, i.e., raw Eq.S.  Eq.S has:
  r² K'' + 2r(1−rφ') K' + (ω²r²e^{2φ} − Le^{2φ} + 2e^{2φ}) K = 0
  
For this to be in form -(pK')' + QK = ω² w_K K with p = r²e^{-2φ}:
  -(pK')' = -p K'' - p' K'.  But raw Eq.S has +r² K''.
  So we'd need p = -r²?  That's not what BB says.

Or perhaps BB's SL form has a sign-flipped source convention:
  (pK')' − QK + ω² w_K K = 0  → +pK'' + p'K' − QK + ω² w_K K = 0

Match: r² = p, w_K = r²·e^{2φ} (matching ω²r²e^{2φ} term).
Then Q = +(L−2)·e^{2φ}? Not φ-independent.

The only way to get φ-independent Q is to multiply by μ = e^{-2φ}.
Then ω² w_K = ω² · r² (NOT r²e^{2φ}).

Therefore: canonical doc's 'w_K = r²e^{2φ}' is a TYPO for w_K = r².
OR: BB is using a non-canonical SL form.

Let me re-check BB's Step 1 to see what they actually computed.
""")
