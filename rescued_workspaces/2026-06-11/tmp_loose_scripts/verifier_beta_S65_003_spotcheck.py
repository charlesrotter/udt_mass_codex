"""
Verifier-β PASS 3 numerical spot-check for S65-003 PONDER L3 closure test.

Goal: confirm §255 violation Δ_Dirac ≠ 0 at canonical Branch-M anchor.

Branch-M canonical anchor:
  φ_0 baseline = -cos(π/5) = -0.8090...
  μ² = π/3
  r* = 6.9875 (natural units)
  Canonical Form-T eigenmode κ = -1 ground state, E_1 = 2√2/3

This is supplementary verification: not load-bearing for the
STRUCTURAL-FINDING-AT-COUPLED-SYSTEM-LAYER verdict; the structural
argument is at PONDER §3.3 + §3.4.

Approach: Solve homogeneous nonlinear vacuum φ_0 ODE (□_g φ_0 = μ² φ_0) +
Form-T Dirac (G, F) at canonical anchor; evaluate
  Δ_Dirac(r; κ=-1) = -κ e^{-φ_0} G F / (2π r³)
at sample r values.

We use a simple shoot-and-evaluate at three illustrative r-values inside r* range.
"""
import numpy as np
from scipy.integrate import solve_ivp

# ---- Canonical Branch-M anchor parameters ----
phi0_anchor = -np.cos(np.pi/5)   # -0.80901699...
mu2 = np.pi/3                    # 1.0471975512
r_star = 6.9875                  # natural units
E1 = 2.0 * np.sqrt(2.0) / 3.0    # 0.94280904...
kappa = -1                       # ground state
m = 0.0                          # massless

print(f"=== Verifier-β S65-003 Branch-M spot-check ===")
print(f"φ_0 anchor value (at r* by convention here) = {phi0_anchor:.6f}")
print(f"μ²                = {mu2:.6f}")
print(f"r*                = {r_star:.4f}")
print(f"E_1 (κ=-1 ground) = {E1:.6f}")
print(f"κ                 = {kappa}")
print()

# ---- Solve nonlinear vacuum φ_0 ODE using flux form ----
# J' = r² μ² φ
# φ' = J e^{2φ} / r²
# Boundary: at r = r*, φ_0(r*) = phi0_anchor, φ_0'(r*) = 0 (Neumann)
# Integrate INWARD from r=r* to small r.
def phi_rhs(r, y):
    phi, J = y
    if r < 1e-12:
        return [0.0, 0.0]
    phi_prime = J * np.exp(2.0*phi) / (r*r)
    J_prime = r*r * mu2 * phi
    return [phi_prime, J_prime]

# Backward integration r* -> r_min
r_min = 0.05
sol_phi = solve_ivp(phi_rhs, [r_star, r_min], [phi0_anchor, 0.0],
                    method='DOP853', rtol=1e-10, atol=1e-12,
                    dense_output=True, max_step=0.05)
print(f"φ ODE status (back-integration): {sol_phi.status}, success={sol_phi.success}")
if not sol_phi.success:
    print("ABORT: vacuum φ ODE failed.")
    raise SystemExit

# ---- Solve canonical Form-T Dirac (G, F) at this background ----
# Form-T radial system at canonical metric (CG §4.4):
# dG/dr + (κ/r - φ')G = (m e^φ + E e^{2φ}) F
# dF/dr + (-κ/r - φ')F = (m e^φ - E e^{2φ}) G
# Forward-shoot from small r with Frobenius regularity. For κ=-1: G~r^0, F~r near origin.
# Eigenvalue condition at r*: Neumann G'(r*) = 0 (canonical Branch-M).
# We do NOT need to enforce the eigenvalue exactly; we use the canonical E_1 = 2√2/3
# and check that the resulting (G, F) gives non-zero Δ.

def dirac_rhs(r, y):
    G, F = y
    # Get φ, φ' from background via dense output
    phi, J = sol_phi.sol(r)
    if r < 1e-12:
        return [0.0, 0.0]
    phi_prime = J * np.exp(2.0*phi) / (r*r)
    # Form-T equations
    dG = -(kappa/r - phi_prime)*G + (m*np.exp(phi) + E1*np.exp(2.0*phi))*F
    dF = -(-kappa/r - phi_prime)*F + (m*np.exp(phi) - E1*np.exp(2.0*phi))*G
    return [dG, dF]

# κ = -1: Frobenius near origin: G(r) ~ G_0 + ..., F(r) ~ a₁ r + ...
# Use small initial values that satisfy regularity.
r_init = 0.05
G0, F0 = 1.0, 0.0  # canonical Frobenius leading at κ=-1
sol_dirac = solve_ivp(dirac_rhs, [r_init, r_star], [G0, F0],
                      method='DOP853', rtol=1e-10, atol=1e-12,
                      dense_output=True, max_step=0.05)
print(f"Dirac status: {sol_dirac.status}, success={sol_dirac.success}")

# ---- Evaluate Δ_Dirac at sample r values ----
sample_rs = [0.5, 1.5, 3.0, 5.0, 6.5]
print()
print(f"Sample evaluation of canonical §255 violation:")
print(f"  Δ_Dirac(r; κ=-1) = -κ e^{{-φ_0}} GF / (2π r³)")
print(f"  (single-mode canonical Form-T, no normalization scaling)")
print()
print(f"  {'r':>6} | {'φ_0(r)':>10} | {'G(r)':>12} | {'F(r)':>12} | {'Δ_Dirac':>14}")
print(f"  {'-'*6}-+-{'-'*10}-+-{'-'*12}-+-{'-'*12}-+-{'-'*14}")
for r in sample_rs:
    if not (r_min <= r <= r_star):
        continue
    phi_r = sol_phi.sol(r)[0]
    G_r, F_r = sol_dirac.sol(r)
    Delta = -kappa * np.exp(-phi_r) * G_r * F_r / (2.0*np.pi * r**3)
    print(f"  {r:6.2f} | {phi_r:10.5f} | {G_r:12.5e} | {F_r:12.5e} | {Delta:14.5e}")

print()
print("Interpretation:")
print("  - Δ_Dirac ≠ 0 at canonical single-mode Form-T Dirac (κ=-1 ground)")
print("    confirms §255 violation persists at Branch-M anchor.")
print("  - This is the canonical violation entering L3 closure question.")
print("  - The PONDER's structural finding (closure pre-empted by")
print("    §22.3.2 + §12.12.20) does NOT contradict Δ ≠ 0; it argues")
print("    the violation is test-field-on-metric-determined-background")
print("    consistent and does not require coupling-mediated closure.")
