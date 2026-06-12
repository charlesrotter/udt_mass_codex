"""Additional checks: φ_C(r_CMB) closure, frame ψ-norm equivalence, anchor sensitivity arithmetic."""
import sympy as sp
from sympy import sqrt, pi, cos, Rational, S, simplify, log, exp, symbols, Function, diff, Symbol

print("="*70)
print("Round 2 supplementary checks")
print("="*70)

mu_g_sym = pi*sqrt(pi/3)/13
r_CMB_target = 9.164  # what canonical doc cites

# What exactly is r_CMB? From CG: r_CMB = 9.164 Gpc, μ_g r_CMB ≈ 2.266
# But let's check whether r_CMB is solved exactly so φ_C(r_CMB) = ln(1101)
# φ_C(r) = (3/2)μr − cos(π/5)(μr)² + (2/3)(μr)³
# Set u = μr; want (3/2)u − cos(π/5)u² + (2/3)u³ = ln(1101)
u = sp.Symbol('u', positive=True)
phi_u = sp.Rational(3,2)*u - sp.cos(pi/5)*u**2 + sp.Rational(2,3)*u**3
print("\n[A] Solving φ_C(u) = ln(1101) for u = μ_g·r_CMB:")
sol = sp.nsolve(phi_u - sp.log(1101), u, 2.27)
print(f"  Exact u_CMB = {sol}")
mu_g_num = float(mu_g_sym)
r_CMB_exact = float(sol)/mu_g_num
print(f"  μ_g = {mu_g_num:.10f}")
print(f"  r_CMB = u/μ_g = {r_CMB_exact:.10f} Gpc")
print(f"  Canonical doc cites r_CMB = 9.164 Gpc")
print(f"  Discrepancy: {(r_CMB_exact - 9.164)*1000:.3f} milli-Gpc, i.e., {(r_CMB_exact-9.164)/9.164*100:.4f}%")

# So the small residual in φ_C(9.164) − ln(1101) is because 9.164 is rounded.
# Re-evaluate η_K at the exact r_CMB
phi_C_prime_at_exact = sp.Rational(3,2)*mu_g_sym - 2*sp.cos(pi/5)*mu_g_sym**2 * sol/mu_g_sym + 2*mu_g_sym**3 * (sol/mu_g_sym)**2
phi_C_prime_at_exact_num = float(mu_g_sym * (sp.Rational(3,2) - 2*sp.cos(pi/5)*sol + 2*sol**2))
print(f"\n  φ_C'(r_CMB,exact) = {phi_C_prime_at_exact_num:.10f} Gpc⁻¹")
print(f"  η_K(r_CMB,exact) = 2/r_CMB,exact - 2·φ' = {2/r_CMB_exact - 2*phi_C_prime_at_exact_num:.10f} Gpc⁻¹")
print(f"  Compare to canonical −3.790375 Gpc⁻¹")

# Use canonical doc 9.164 -- that's what was used
phi_at_9164 = sp.Rational(3,2)*mu_g_sym*9.164 - sp.cos(pi/5)*(mu_g_sym*9.164)**2 + sp.Rational(2,3)*(mu_g_sym*9.164)**3
print(f"\n[B] φ_C at r=9.164 (rounded canonical) = {float(phi_at_9164):.6f}")
print(f"  vs ln(1101) = {float(sp.log(1101)):.6f}; deviation 0.003% inherits from r_CMB rounding to 4 sig figs.")

# Anchor sensitivity check: 0.09% / 10.24 = ?
print("\n[C] Anchor sensitivity arithmetic:")
print(f"  0.09 / 100 = {0.09/100}")
print(f"  0.0009 / 10.24 = {0.0009/10.24:.8e}")
print(f"  ≈ {0.0009/10.24:.3e}")
print(f"  Canonical doc cites < 8.8 × 10⁻⁵ = 8.8e-5 = {8.8e-5}")
print(f"  Computed: {0.0009/10.24:.3e}")
print(f"  Ratio: {(0.0009/10.24)/8.8e-5:.4f}")
print("  Round to 2 sig figs: 8.8e-5 — match.")

# Now check Q(ℓ) when ℓ=2 reproduces the canonical ω²r²A − LA + 2A coefficient.
# Eq.S coefficient on K: ω²r²A − LA + 2A = ω²r²A + (2-L)A = ω²r²A − (L-2)A
# So Q in SL form = (L-2)·(weight factor), and BB's Q(ℓ) = (ℓ-1)(ℓ+2) = L − 2 — yes!
# But this Q has dim [length]² implicit if w = r²e^{2φ} dimensional; since L−2 dimensionless, Q here = (L-2) per ℓ.
# Wait — we need to inspect SL form more carefully.

print("\n[D] Q(ℓ) in SL form -- dimension consistency:")
print("    SL form: -(p K')' + Q K = ω² w K + source")
print("    p = r²e^{-2φ}, w = r²e^{2φ}")
print("    Eq.S has coefficient on K:  (ω² r² e^{2φ} - L e^{2φ} + 2 e^{2φ})")
print("                               = ω² (r²e^{2φ}) + (2-L) e^{2φ}")
print("                               = ω² w + (2-L) e^{2φ}")
print("    Hmm — but BB claims Q = (ℓ-1)(ℓ+2) is φ-INDEPENDENT.")
print("    If the SL identification is pK''+... + Q K = ω² w K, expanding")
print("    p = r²e^{-2φ} → p K'' = r²e^{-2φ} K''")
print("    But Eq.S has r² K'' (no e^{-2φ}).")
print("    ⇒ To get -(pK')' giving r² K'' coefficient, need to multiply Eq.S by")
print("       r²e^{-2φ}/r² = e^{-2φ} (overall factor) or rearrange.")
print("    Let me carefully derive the SL form of Eq.S.")

# Given: r² K'' + 2r(1−rφ') K' + (ω²r²A − LA + 2A) K = source (with A = e^{2φ})
# Multiply by μ(r) so that μ·r² K'' + μ·2r(1−rφ') K' = (μ r² K')'
# Need: d/dr(μ r²) = μ·2r(1−rφ')   → μ' r² + 2μ r = 2μr − 2μ r²φ'
#                                  → μ' = -2μφ', → μ = e^{-2φ}
# So (μr² K')' = e^{-2φ}·r² K'' + (e^{-2φ}·2r·(1-rφ') ) K'
# (Verify: d/dr[e^{-2φ}r²] = -2φ' e^{-2φ} r² + 2r e^{-2φ} = 2r e^{-2φ}(1 − rφ') ✓)
# So multiplying Eq.S by e^{-2φ}:
# (e^{-2φ}r² K')' + e^{-2φ}·(ω²r²A − LA + 2A) K = e^{-2φ}·source
# = (p K')' + (ω² r² + (2-L)) K = e^{-2φ}·source     [since e^{-2φ}·A = 1]
# Rewrite: -(pK')' + (L-2) K = ω² r² K + RHS
#                    NOT  ω² w K — w = r² (only)
# But canonical doc says w = r²e^{2φ}. Contradiction?
# Let me recompute:

print("\n  Multiply Eq.S by μ = e^{-2φ}:")
print("    e^{-2φ} r² K'' + e^{-2φ}·2r(1-rφ')·K' + e^{-2φ}(ω²r²A − LA + 2A)·K = source·e^{-2φ}")
print("  First two terms = (e^{-2φ}r² K')' = (p K')' with p = r²e^{-2φ}.")
print("  Third term: e^{-2φ}·A = 1, so:")
print("    e^{-2φ}·ω²r²A = ω² r²  (so weight w = r², not r²e^{2φ})")
print("    e^{-2φ}·(LA − 2A) = (L − 2)·1 = L − 2")
print("  ⇒ -(p K')' + (L−2) K = ω² r² K + RHS  (with -(pK')' arrangement)")
print("\n  Hence Q(ℓ) = L − 2 = (ℓ-1)(ℓ+2) — φ-INDEPENDENT ✓ (matches BB)")
print("  But weight w_K should be r², NOT r²e^{2φ}!")
print()
print("  Canonical doc claim: 'w_K = r²e^{2φ}' (CG §23.5 second-from-last paragraph cite)")
print("  BB-frame derivation: w = r² (φ-independent)")
print()
print("  *** Possible discrepancy or convention issue ***")
print("  Need to check whether 'w_K = r²e^{2φ}' is BB's intent or canonical-doc framing.")
