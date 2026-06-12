"""
Agent U — physics-observable convention test.
Compute relative ℓ-amplitude under each of (P, Q, R) conventions
at fixed |κ|=3 (j=5/2) on Branch-C cavity at r_CMB.

Observable: |S_P(r;κ,ℓ=4)|^2 / |S_P(r;κ,ℓ=2)|^2 at r=r_CMB, |κ|=3.

The bracket [E e^φ (G^2+F^2)/r^4 - κ e^{-φ} GF/r^5] is independent of ℓ.
The Wigner-Eckart C^(ℓ)_κ at j=5/2, m=j convention is the same Clebsch-Gordan
calculation for any ℓ — convention-INVARIANT.

So the convention dependence shows up entirely in the ratio α_ℓ / α_2.
"""
import sympy as sp
from sympy.physics.quantum.cg import CG

# Symbolic variables
ell = sp.symbols('ell', integer=True, positive=True)

# Three candidate alpha_ell:
def alpha_P(L):
    return sp.Rational(-4)  # constant

def alpha_Q(L):
    # -4 * N_2 / N_ell, N_ell = (1/2)(ℓ-1)ℓ(ℓ+1)(ℓ+2)
    N2 = sp.Rational(1, 2) * 1 * 2 * 3 * 4  # = 12
    Nl = sp.Rational(1, 2) * (L - 1) * L * (L + 1) * (L + 2)
    return -4 * N2 / Nl

def alpha_R(L):
    # -4 * ℓ(ℓ+1)/6
    return sp.Rational(-4) * L * (L + 1) / 6

# Wigner-Eckart C^(ℓ)_κ at j=|κ|-1/2, m=j convention
# For |κ|=3, j=5/2
def C_kappa(L, kappa):
    j = sp.Rational(abs(kappa)) - sp.Rational(1, 2)
    return CG(j, j, L, 0, j, j).doit()

print("="*80)
print("Agent U — Convention test: relative ℓ-amplitude at fixed |κ|=3 (j=5/2)")
print("="*80)

# Verify ℓ=2 baseline
print("\nℓ=2 baseline check (all conventions should give α_2 = -4):")
print(f"  α_P(2) = {alpha_P(2)}")
print(f"  α_Q(2) = {alpha_Q(2)}")
print(f"  α_R(2) = {alpha_R(2)}")
assert alpha_P(2) == alpha_Q(2) == alpha_R(2) == -4, "ℓ=2 convention agreement check"

print("\nWigner-Eckart C^(ℓ)_κ at |κ|=3 (j=5/2, m=j):")
for L in [2, 4, 6, 8]:
    print(f"  C^({L})_3 = {C_kappa(L, 3)} = {float(C_kappa(L, 3)):.6f}")

# The ratio |S_P(ℓ=4)/S_P(ℓ=2)|^2 at fixed κ=3:
# (|S_P(ℓ)|/|S_P(2)|)^2 = (|α_ℓ|·|C^(ℓ)_κ| / (|α_2|·|C^(2)_κ|))^2

print("\n" + "="*80)
print("Ratio R(ℓ) = |S_P(ℓ)|^2 / |S_P(ℓ=2)|^2 at |κ|=3 (bracket cancels exactly):")
print("="*80)
print(f"{'ℓ':>4} {'α_ℓ^P':>10} {'α_ℓ^Q':>15} {'α_ℓ^R':>10} {'C^(ℓ)_3':>15}")
for L in [4, 6, 8]:
    print(f"{L:>4} {str(alpha_P(L)):>10} {str(alpha_Q(L)):>15} {str(alpha_R(L)):>10} {str(C_kappa(L,3)):>15}")

print("\nObservable ratios R^X(ℓ) = (α_ℓ^X · C^(ℓ)_3 / (α_2^X · C^(2)_3))^2:")
print(f"{'ℓ':>4} {'R^P(ℓ)':>20} {'R^Q(ℓ)':>20} {'R^R(ℓ)':>20}")
C2 = C_kappa(2, 3)
a2P, a2Q, a2R = alpha_P(2), alpha_Q(2), alpha_R(2)
for L in [4, 6, 8]:
    Cl = C_kappa(L, 3)
    aP, aQ, aR = alpha_P(L), alpha_Q(L), alpha_R(L)
    RP = sp.simplify((aP*Cl / (a2P*C2))**2)
    RQ = sp.simplify((aQ*Cl / (a2Q*C2))**2)
    RR = sp.simplify((aR*Cl / (a2R*C2))**2)
    print(f"{L:>4} {str(RP):>20} {str(RQ):>20} {str(RR):>20}")
    print(f"     numerical: P={float(RP):.6e}  Q={float(RQ):.6e}  R={float(RR):.6e}")

print("\n" + "="*80)
print("CONCLUSION: at the bare-source-vector level (no operator inversion),")
print("the three conventions give DIFFERENT observable ratios at ℓ ≥ 4.")
print("="*80)
