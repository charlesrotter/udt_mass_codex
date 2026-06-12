"""Vβ-5d: WKB validity at m != 0 canonical Branch-M.

Branch-M anchor: phi0 = -cos(pi/5) ≈ -0.809, mu^2 = pi/3, r* ≈ 6.9875.
For Branch-M canonical electron mode E_1 = 2 sqrt(2)/3 ≈ 0.9428 (m = m_e in scaled units).
phi(r) ranges from phi0 ≈ -0.809 at r=0 to phi(r*) ≈ 0 (per Frobenius regularity + scalar EOM).

k(r) = 2 (m e^phi + E e^{2 phi}).
At Branch-M anchor inner region: phi ≈ -0.809, so:
  e^phi ≈ 0.445, e^{2 phi} ≈ 0.198
  C = m * 0.445 + E * 0.198
At E = E_1 ≈ 0.943 (sub-barrier electron with m=1 in scaled units):
  C ≈ 0.445 + 0.943 * 0.198 ≈ 0.632
  k ≈ 1.26
  
Compare to phi'(r): phi'(0) = 0 by regularity; phi'(r) can be ~ 0.1-0.5 in mid-r.
Need k >> phi' for WKB validity.  At Branch-M inner region: k ~ 1.26, phi' ~ 0.1-0.2: k/phi' ~ 6-12.
WKB *marginal* at Branch-M canonical electron mode.

And k r >> |kappa|: r ~ 3-4, kappa = -1. k r ~ 4-5. |kappa| = 1.  Ratio ~ 4-5: WKB marginal.

The agent's F1 anchor uses phi0 = -cos(pi/5) (Branch-M anchor) AT m=0, with E = 13-48 (much higher than E_1).
At E = 13:
  C = 0 + 13 * 0.2 ≈ 2.6  (at inner phi = -0.8)
  k ≈ 5.2
  k/phi' ~ 25: WKB safely valid.
  
Conclusion: agent's m=0 F1 work probes a DIFFERENT physical setup than the canonical Branch-M electron mode.
The substrate at m=0 is mathematically valid; the *physical scope* of the bound is m=0 spectra, not the canonical Branch-M electron mode at m=m_e where WKB is marginal.
"""
import numpy as np
phi0 = -np.cos(np.pi/5)
mu_sq = np.pi/3
r_star = 6.9875
m_phys = 1.0  # canonical Branch-M anchor mass
E_1 = 2*np.sqrt(2)/3
print(f"Branch-M anchor: phi0 = {phi0:.4f}, mu^2 = {mu_sq:.4f}, r* = {r_star:.4f}")
print(f"E_1 (sub-barrier electron) = {E_1:.4f}, m_phys = {m_phys:.4f}")
print()
phi_inner = phi0
C_inner = m_phys * np.exp(phi_inner) + E_1 * np.exp(2*phi_inner)
k_inner = 2 * C_inner
print(f"Inner: C = {C_inner:.4f}, k = {k_inner:.4f}")
print(f"phi'(inner ~ 0.1): expected ~0.1-0.2 (scalar EOM, regular origin)")
print(f"k / phi' ~ {k_inner/0.15:.2f}: WKB marginal at canonical sub-barrier electron mode.")
print()
print("Agent's F1 at m=0, E = 13-48: well above sub-barrier; WKB safely valid.")
print()
print("Sub-barrier means E < m e^{-phi_min} so the (G,F) system is in the classically forbidden region.")
print(f"At Branch-M: E_1 = {E_1:.4f}, m e^{{-phi_min}} = m e^{{-phi0}} = e^{{-(-0.809)}} = {np.exp(0.809):.4f}")
print(f"E_1 / (m e^{{-phi_min}}) = {E_1 / np.exp(0.809):.4f} < 1 -- sub-barrier confirmed.")
print()
print("At sub-barrier: the rotation eigenvalues of M_VW have det -> 0 somewhere?")
print("k(r) = 2 (m e^phi + E e^{2 phi}). At m = 1, E = 0.943:")
r_test = np.linspace(0.1, r_star, 21)
phi_test = phi0 * (1 - r_test/r_star)**2  # toy profile, not actual
for r_, p_ in zip(r_test[:5], phi_test[:5]):
    k_ = 2*(m_phys*np.exp(p_) + E_1*np.exp(2*p_))
    print(f"  r={r_:.2f}, phi~{p_:.4f}, k={k_:.4f}")
print()
print("k stays positive and order unity at canonical Branch-M sub-barrier electron mode.")
print("WKB ansatz remains valid but with k r ~ |kappa| at small r (turning region).")
print()
print("Vβ-5d substantive: k(r) = 2C(r) does NOT vanish at sub-barrier --")
print("the bound formula extends formally, but WKB validity region (k >> phi', k r >> |kappa|) shrinks.")
print("The bound coverage at canonical Branch-M electron mode is restricted to the outer cavity")
print("(where k r >> 1) and degrades near the turning region.")
