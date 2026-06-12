"""
Agent U — operator-inversion test: does Eq.S/Eq.T inversion absorb α_ℓ?

Eq.S (after H-elimination): -(p K')' + Q_K(r;ℓ) K = ω² w_K K + e^{-2φ} S_P(r;κ,ℓ)
                            with p = r² e^{-2φ}, w_K = r² e^{2φ},
                            Q_K contains LA, 2A terms with L = ℓ(ℓ+1).

The source enters as e^{-2φ} S_P with NO explicit α_ℓ-cancelling factor.

SL Green's function expansion:
   K(r) = Σ_n [c_n(κ,ℓ)/(ω_n²(ℓ) - ω²)] K_n(r;ℓ)
   c_n(κ,ℓ) = ∫ K_n(r';ℓ) · e^{-2φ(r')} S_P(r';κ,ℓ) dr'

The c_n coefficients inherit α_ℓ linearly: c_n^X = α_ℓ^X · C^(ℓ)_κ · [bilinear-integral term],
where [bilinear-integral term] is convention-independent.

Thus K(r) at fixed κ, ℓ scales linearly with α_ℓ — the convention is NOT absorbed.

Test 1: any observable that is BILINEAR in K (e.g., |K|², energy flux ∫|K|² w_K dr)
        scales as α_ℓ². So the OBSERVABLE ratio R(ℓ) at fixed κ involves
        (α_ℓ · C^(ℓ)_κ / α_2 · C^(2)_κ)² — same as the bare source ratio.

Test 2: SL Green's function K(r;ω) at fixed ω, fixed (r, κ, ℓ) is symbolically:
        K(r) = α_ℓ^X · C^(ℓ)_κ · F(r;ω,ℓ)
        where F is convention-INDEPENDENT but ℓ-dependent through the
        operator's eigenvalues ω_n(ℓ) and eigenfunctions K_n(r;ℓ).
"""
import sympy as sp

# Define symbols
r, rp, omega, omega_n, phi, ell = sp.symbols('r r\' omega omega_n phi ell', positive=True, real=True)
alpha_l, C_l, S_kernel = sp.symbols('alpha_ell C_ell S_kernel', real=True)
K_n = sp.Function('K_n')(r)
K_n_p = sp.Function('K_n')(rp)

# Source: S_P(r;κ,ℓ) = α_ℓ · C^(ℓ)_κ · S_kernel(r;κ)
S_P = alpha_l * C_l * S_kernel

# After H-elimination, Eq.S in SL form is:
#   -(p K')' + Q_K(r;ℓ) K = ω² w_K K + e^{-2φ} S_P
# where p=r²e^{-2φ}, w_K=r²e^{2φ}, Q_K depends on ℓ via L=ℓ(ℓ+1).
#
# SL Green's function expansion: assume operator H_ℓ satisfies H_ℓ K_n = ω_n²(ℓ) w_K K_n
# Then  K(r) = G_ℓ(r,r';ω²) acting on (e^{-2φ(r')} S_P(r'))
# G_ℓ(r,r';ω²) = Σ_n [K_n(r;ℓ) K_n(r';ℓ)] / [(ω_n²(ℓ) - ω²) ⟨K_n,K_n⟩_w]

# For the symbolic test: K(r) at fixed (ω, r, κ) under each convention X:
# K^X(r) = α_ℓ^X · C^(ℓ)_κ · ∫ G_ℓ(r,r';ω²) · e^{-2φ(r')} · S_kernel(r';κ) dr'
#        = α_ℓ^X · C^(ℓ)_κ · K_kernel(r;ω,ℓ,κ)
# 
# where K_kernel is convention-INDEPENDENT.

K_kernel = sp.Function('K_kernel')(r, omega, ell)  # convention-independent
K_solution = alpha_l * C_l * K_kernel

print("="*80)
print("Operator-inversion linearity test")
print("="*80)
print(f"Source:    S_P = {S_P}")
print(f"Solution:  K(r) = α_ℓ · C^(ℓ)_κ · K_kernel(r;ω,ℓ)  [linear in source]")
print()
print("This means K(r) under each convention scales linearly with α_ℓ.")
print()
print("Test: ratio K^Q(r;ℓ=4) / K^P(r;ℓ=4) at fixed κ:")
print("  K^Q/K^P = α_ℓ^Q / α_ℓ^P  (since C^(ℓ)_κ is convention-INVARIANT)")
print()

# Numerical check at ℓ=4
def alpha_P(L): return sp.Rational(-4)
def alpha_Q(L): 
    Nl = sp.Rational(1,2)*(L-1)*L*(L+1)*(L+2)
    return -4 * 12 / Nl
def alpha_R(L): return sp.Rational(-4) * L * (L+1) / 6

L = 4
print(f"At ℓ=4:")
print(f"  α^P/α^Q = {alpha_P(L)/alpha_Q(L)}  (factor of 15)")
print(f"  α^R/α^P = {alpha_R(L)/alpha_P(L)}  (factor of 10/3)")
print(f"  α^R/α^Q = {alpha_R(L)/alpha_Q(L)}  (factor of 50)")
print()
print("These are FACTOR DIFFERENCES in K(r) under different conventions.")
print("If two predictions for the SAME physical mode (same r, ω, κ, ℓ) differ")
print("by these factors, then the convention IS physics-dependent at the K(r) level.")
print()

# Now ask: is there a NORMALIZATION step in K(r)→observable that absorbs α_ℓ?
# E.g., suppose physical observable is K(r)/||K|| where ||K|| = √∫|K|² w_K dr
# Then NORMALIZED K is convention-INVARIANT! Let's check.

print("="*80)
print("Q-PIN-3 critical test: NORMALIZED K(r) under each convention")
print("="*80)
print("If observable is |K(r)|² / ∫|K(r')|² w_K dr':")
print("  Numerator   = (α_ℓ · C · K_kernel)²")
print("  Denominator = α_ℓ² · C² · ∫|K_kernel|² w_K dr'")
print("  RATIO       = |K_kernel(r)|² / ∫|K_kernel|² w_K dr'   [α_ℓ CANCELS symbolically]")
print()
print("  → For any normalized (unit-norm) observable, the convention ABSORBS as identity.")
print()
print("BUT: the typical CMB-style observable is NOT unit-norm — it's the absolute amplitude")
print("|K_ℓ|² which inherits α_ℓ². Source-amplitude-bearing observables are")
print("convention-dependent.")
print()
print("="*80)
print("Concrete observables and their convention dependence:")
print("="*80)
print(f"  |K(r)|² at fixed (κ,ℓ,ω):                      ~ (α_ℓ)²       → CONVENTION-DEPENDENT")
print(f"  Energy flux ∫|K|² w_K dr at fixed (κ,ℓ,ω):     ~ (α_ℓ)²       → CONVENTION-DEPENDENT")
print(f"  Ratio R(ℓ) = |K_ℓ|² / |K_2|²:                  ~ (α_ℓ/α_2)²  → CONVENTION-DEPENDENT")
print(f"  Normalized K_hat(r) = K/||K|| at fixed κ,ℓ,ω:  α_ℓ cancels   → INVARIANT (numerical)")
print(f"  K_hat(r;ℓ=4)/K_hat(r;ℓ=2) at fixed (r,κ):      requires both K_kernels — NORMALIZED ratio remains invariant per ℓ")
print()
print("The amplitude observables are convention-dependent.  Only normalized")
print("(unit-norm) observables at FIXED ℓ are convention-invariant.")
print()

# A more subtle question: when computing a CMB observable that is a sum over ℓ
# (e.g., total power Σ_ℓ (2ℓ+1) C_ℓ), the relative weighting IS determined by α_ℓ.
print("="*80)
print("CMB-style multi-ℓ observable test:")
print("="*80)
print("A typical CMB observable sums over ℓ:")
print("  C_ℓ ~ |α_ℓ|² · |C^(ℓ)_κ|² · (mode-mode integrals at ℓ)")
print()
print("The WEIGHTING of different ℓ modes in this sum is set by |α_ℓ|².  Three conventions")
print("give different weightings:")
print(f"  P (constant -4):      uniform weighting in ℓ")
print(f"  Q (1/N_ℓ ~ 1/ℓ⁴):     suppresses high-ℓ; high-ℓ modes negligible")
print(f"  R (ℓ(ℓ+1) ~ ℓ²):      enhances high-ℓ; high-ℓ modes dominate")
print()
print("These produce DIFFERENT predicted multi-ℓ spectra.  This is physics-dependent.")
