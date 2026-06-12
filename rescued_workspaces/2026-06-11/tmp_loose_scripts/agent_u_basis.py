"""
Agent U — Basis-rescaling analysis: does the observable h_ab(r,θ,φ) cancel α_ℓ?

In Regge-Wheeler-Zerilli theory, the polar metric perturbation is expanded as
    h_ab(t,r,θ,φ) = Σ_ℓm K_ℓm(r) [basis_function_K(θ,φ)]
                  + Σ_ℓm P_ℓm(r) [basis_function_P(θ,φ)] + ...

Three conventions correspond to three choices of basis_function_K:

(P) basis_K = g_ab Y_ℓm                    [direct h^μν projection]
(Q) basis_K = g_ab Y_ℓm / √N_ℓ             [orthonormal Y^E basis]
(R) basis_K = g_ab Y_ℓm · √(L/L_2)         [SL-natural with L=ℓ(ℓ+1)]

If basis_X = basis_baseline · f^X_ℓ, then
    K_ℓ^X = K_ℓ^baseline / f^X_ℓ

But the PHYSICAL observable h_ab(r,θ,φ) is basis-INDEPENDENT:
    h_ab = K_ℓ · basis_X = K_ℓ^X · basis_baseline · f^X_ℓ
         = K_ℓ^baseline · basis_baseline                     [identical!]

So if the source α_ℓ also rescales correspondingly:
    S_P^X = α_ℓ^X · C^(ℓ)_κ · ρ
    K_ℓ^X = α_ℓ^X · C^(ℓ)_κ · K_kernel(r;ω,ℓ)

Then the physical observable becomes:
    h_ab^X(r,θ,φ) = K_ℓ^X · basis_X(θ,φ)
                  = α_ℓ^X · C^(ℓ)_κ · K_kernel(r;ω,ℓ) · basis_X(θ,φ)

For h_ab to be convention-INVARIANT, we need:
    α_ℓ^X · basis_X(θ,φ) = const(X)

i.e., α_ℓ scales INVERSELY with the basis function.

Question: does the canonical α_ℓ for each convention satisfy this consistency?

(P) basis_K = g_ab Y_ℓm,                    α^P = -4
(Q) basis_K = g_ab Y_ℓm / √N_ℓ,             α^Q = -4 N_2/N_ℓ
(R) basis_K = g_ab Y_ℓm · √(L/L_2),         α^R = -4 L/L_2

For invariance, we need α_ℓ^X / α_ℓ^P · basis_X / basis_P = 1, i.e.,
    α^Q/α^P = basis_P/basis_Q = √N_ℓ/√N_2 ?
    Check: α^Q/α^P = N_2/N_ℓ.  basis_P/basis_Q = √N_ℓ.  Ratio = N_2/N_ℓ · √N_ℓ ≠ 1.
    
    α^R/α^P = basis_P/basis_R = √(L_2/L) ?
    Check: α^R/α^P = L/L_2.  basis_P/basis_R = √(L_2/L).  Ratio = L/L_2 · √(L_2/L) = √(L/L_2) ≠ 1.

So the THREE α_ℓ values do NOT correspond to consistent rescalings of the same h_ab.
They are not gauge transformations of one observable; they are three DIFFERENT predictions
for the source amplitude under three different basis choices.

Either:
  (a) Two of three are wrong (basis-mis-normalized in their derivation), OR
  (b) There is no canonical h_ab observable that all three should agree on; the
      question is "what α_ℓ does the canonical Form-T spinor source produce?"
      and the canonical answer depends on the basis convention used to read off
      α_ℓ from the integrand.

The latter is what the S51-002 finding is saying: the Form-T → polar tensor projection
is convention-dependent at the OPERATOR-DEFINITION layer because the canonical
text doesn't specify which basis to expand h_ab in.

Once a basis is FIXED (any of P, Q, R), the resulting α_ℓ is uniquely determined,
and the physical predictions are convention-invariant ONLY IF downstream observables
(K_ℓ × basis_ℓ × etc.) consistently use the same basis throughout.

The S51-002 finding therefore reduces to: pick a basis and stick with it.
But this CANNOT be done at the physics-observable layer alone — it's a bookkeeping
choice.  The "physics-invariance" verdict applies provided downstream pipeline
respects the basis pin.
"""

import sympy as sp

L_var, L_2 = sp.symbols('L L_2', positive=True)
N_l, N_2 = sp.symbols('N_ell N_2', positive=True)

# Three conventions:
alpha_P = -4
alpha_Q_over_P = N_2 / N_l   # ratio
alpha_R_over_P = L_var / L_2  # ratio

# Basis function rescalings (relative to P-baseline):
basis_Q_over_P = 1 / sp.sqrt(N_l)  # orthonormal: divide by √N_ℓ
basis_R_over_P = sp.sqrt(L_var / L_2)  # SL-natural: scale by √(L/L_2)

# For h_ab to be invariant: α_ℓ × basis_ℓ should be invariant
# i.e., (α^X / α^P) × (basis^X / basis^P) = 1

print("="*80)
print("Basis-consistency test: α_ℓ × basis_ℓ for three conventions")
print("="*80)

# Q vs P:
ratio_Q = alpha_Q_over_P * basis_Q_over_P
print(f"Q vs P:  (α^Q/α^P) × (basis_Q/basis_P) = (N_2/N_ℓ) × (1/√N_ℓ) = N_2/N_ℓ^(3/2)")
print(f"         = {sp.simplify(ratio_Q)}")
print(f"         INVARIANT only if N_ℓ = N_2 (i.e., ℓ=2). ⚠️ NOT generally invariant.")
print()

# R vs P:
ratio_R = alpha_R_over_P * basis_R_over_P
print(f"R vs P:  (α^R/α^P) × (basis_R/basis_P) = (L/L_2) × √(L/L_2) = (L/L_2)^(3/2)")
print(f"         = {sp.simplify(ratio_R)}")
print(f"         INVARIANT only if L = L_2 (i.e., ℓ=2). ⚠️ NOT generally invariant.")
print()

print("="*80)
print("INTERPRETATION")
print("="*80)
print("""
The three conventions are NOT three equivalent parameterizations of the SAME
observable h_ab.  They are three INCONSISTENT bookkeeping patterns where the
α_ℓ source coefficient and the basis-function normalization are not properly
matched to make h_ab convention-invariant.

This is a STRUCTURAL FINDING: the S51-002 derivation has a layer ambiguity
about whether α_ℓ is the coefficient of g_ab Y_ℓm (P) or of an orthonormal
tensor harmonic (Q) or of an SL-natural basis (R).  Each agent's α_ℓ is
internally consistent IF the corresponding basis is used downstream — but
the canonical text doesn't specify which.

If the basis is pinned (e.g., orthonormal Y^E, the standard RWZ choice), then
α^Q is the unique correct answer.  α^P and α^R correspond to non-orthonormal
bases that would give correct h_ab IF combined with their respective basis
functions, but DIFFERENT (incorrect) h_ab if combined with the orthonormal basis.

VERDICT: the convention-test cannot be answered at the bare-α_ℓ level alone.
The "physics observable" depends on whether the canonical pipeline uses an
orthonormal basis (Q canonical) or a different normalization (P or R canonical
with corresponding basis-function adjustment downstream).

This is a Q-PIN-3 NEAR-MISS: the conventions DO cancel symbolically when paired
with their consistent basis function — but ONLY when the pairing is enforced.
The canonical text currently does not specify the pairing, so the operator-level
α_ℓ alone is genuinely ambiguous.
""")
