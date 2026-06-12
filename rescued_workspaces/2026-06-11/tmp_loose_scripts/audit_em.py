"""Cross-check §11.2a EM-Zerilli SL form claim."""
import sympy as sp
from sympy import Symbol, Function, exp, simplify, expand

r = Symbol('r', positive=True)
phi = Function('phi')
Phi_E = Function('Phi_E')
omega2 = Symbol('omega2', real=True)
L = Symbol('L', positive=True)

# §11.2a master: Φ_E'' + [ω²e^{4φ} − Le^{2φ}/r²]Φ_E = 0
EM_eq = Phi_E(r).diff(r, 2) + (omega2*exp(4*phi(r)) - L*exp(2*phi(r))/r**2) * Phi_E(r)
print("EM master:", EM_eq)

# This is already in SL form -(pΦ')' + QΦ = ω² w Φ with p=1:
# -(pΦ')' = -p Φ'' - p' Φ' = -Φ''
# So writing as: -Φ'' + Q Φ = ω² w Φ
# i.e., Φ'' = (Q − ω² w) Φ → Φ'' + (ω² w − Q) Φ = 0
# Match with given: Φ_E'' + [ω²e^{4φ} − Le^{2φ}/r²]Φ_E = 0
# ω² w = ω² e^{4φ}  →  w = e^{4φ}
# Q = L e^{2φ}/r²

print("\n  EM-Zerilli SL form (p=1):")
print("    p   = 1")
print("    w   = e^{4φ}")
print("    Q   = L e^{2φ}/r²  (φ-DEPENDENT)")

print("\n  Canonical doc claim: 'CG §11.2a (EM even-parity Zerilli-form SL cross-check;")
print("                       same canonical weight w = r²e^{2φ})'")
print("  But §11.2a's natural SL has w = e^{4φ}, NOT r²e^{2φ}.")
print("  ")
print("  Alternative SL form: multiply by some μ(r) to get p≠1.")
print("  The 'canonical' EM-Zerilli SL form claimed in canonical doc")
print("  has w = r²e^{2φ}. Let's see if there's a multiplication that gives this.")

# Multiply EM eq by μ(r). Then μΦ'' + μ[ω²e^{4φ} − Le^{2φ}/r²]Φ = 0
# To put in -(pΦ')' + QΦ = ω² w Φ form (with -(pΦ')' = -pΦ'' - p'Φ'):
# Need μ Φ'' = -p Φ'' - p' Φ' (sign flip OK since we can flip whole eq)
# This requires p' = 0, so p constant. Or μΦ'' = pΦ'' + p'Φ' impossible without Φ' term.
# 
# But our EM eq has NO Φ' term! So we can't introduce one through multiplication.
# Hence p must be constant. p = -μ if we want μΦ'' = -pΦ''.
# Or: -(pΦ')' = (with p=-μ) = μΦ'' (since p' = 0).
# Then Q − ω² w = original coefficient × something.
# This is getting tangled. Let me just say: with p=1, Q = Le^{2φ}/r², w = e^{4φ}.
# Multiplying by r² gives: r²Φ'' + [ω²r²e^{4φ} − Le^{2φ}]Φ = 0.
# This isn't SL form because (r²Φ')' = r²Φ'' + 2rΦ' which isn't there.

# So the claim 'w = r²e^{2φ}' for §11.2a is INCORRECT for the form as stated.

print("\n  ⇒ §11.2a as stated has (p,w,Q) = (1, e^{4φ}, Le^{2φ}/r²), NOT (·, r²e^{2φ}, ·)")
print("  ⇒ Canonical doc's cross-reference 'same canonical weight w = r²e^{2φ}' is mismatched")
print("    UNLESS there's a different SL-frame for §11.2a being implicitly used.")
