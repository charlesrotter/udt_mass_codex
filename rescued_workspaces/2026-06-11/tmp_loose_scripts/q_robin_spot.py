"""Spot-check Robin BC pin for matter-sector Hilbert space report.

Per CG §23.5: $\eta_K^{(0)}(r_*) = 2/r_* - 2\phi'(r_*)$
Branch-C N=2 polynomial: $\phi_C(r) = (3/2)\mu_g r - \cos(\pi/5)(\mu_g r)^2 + (2/3)(\mu_g r)^3$
$\phi_C'(r) = \mu_g[3/2 - 2\cos(\pi/5)(\mu_g r) + 2(\mu_g r)^2]$

At $\mu_g = \pi\sqrt{\pi/3}/13$ Gpc^{-1} and $r_{CMB} = 9.164$ Gpc, expect:
  $\phi'(r_{CMB}) = 2.004310$ Gpc^{-1}
  $\eta_K^{(0)} = -3.790375$ Gpc^{-1}
"""
import numpy as np

mu_g = np.pi * np.sqrt(np.pi/3.0) / 13.0
r_CMB = 9.164  # Gpc
cos_pi5 = np.cos(np.pi/5.0)

x = mu_g * r_CMB
phi_prime = mu_g * (1.5 - 2.0*cos_pi5*x + 2.0*x**2)
eta_K0 = 2.0/r_CMB - 2.0*phi_prime

print(f"mu_g = {mu_g:.6f} Gpc^-1  (canonical: 0.247298)")
print(f"mu_g * r_CMB = {x:.6f}    (canonical: 2.266)")
print(f"cos(pi/5) = {cos_pi5:.6f}  (canonical: 0.809017)")
print(f"phi'(r_CMB) = {phi_prime:.6f} Gpc^-1  (canonical: 2.004310)")
print(f"eta_K0 = {eta_K0:.6f} Gpc^-1  (canonical: -3.790375)")

# Verify Wigner-Eckart Clebsch-Gordan for lepton sector
print()
print("Lepton sector |kappa|=1, j=1/2 selection rule check:")
print(f"  ceil((ell+1)/2) at ell=2: {int(np.ceil(3.0/2.0))}")
print(f"  |kappa|=1 < 2, so C^(2)_{{+/-1}} = 0 (zero support at ell=2)")

# Check anchor sensitivity tolerance
print()
print("D-FORMT-ANCHOR-SENSITIVITY tolerance:")
sens = 10.24  # |d ln E / d alpha| at Branch-M anchor
tol_PDG = 0.0009  # 0.09%
lambda_max = tol_PDG / sens
print(f"  Sensitivity coefficient: |d ln E/d alpha| = {sens} at Branch-M kappa=-1 anchor")
print(f"  PDG mass-mapping tolerance: {tol_PDG*100}%")
print(f"  Maximum operator perturbation: lambda^op < {lambda_max:.2e}")
print(f"  Canonical bound: 8.8e-5  (matches: {abs(lambda_max - 8.8e-5)/8.8e-5*100:.1f}% deviation)")
