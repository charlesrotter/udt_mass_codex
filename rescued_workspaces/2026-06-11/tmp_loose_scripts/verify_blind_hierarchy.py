"""BLIND VERIFIER: the '0 : s : 2s hierarchy' sub-claim of C1.

Question posed: 'does the responsive source give the radial channel exactly
twice the fixed-(i-phi) mass?'

Independent computation of all candidate channel masses, defined by
(y^2 psi')' = m psi with m -> const on the demanded collar background
(F = y^-q, kappa^2 = K y^-q at leading order), in EVERY normalization variant:

  fixed-a (frozen source orientation+amplitude) u-channel:
     (y^2 u')' = (P_FF/(8pi)) u   [EL-correct]  => m_fix = W/(2 kappa F)
     small-k:  m_fix = (2/3) kappa^2 / F = (2/3) K
  adiabatic responsive (a eliminated by its stationarity): rank-1 => m = 0
  scaling direction u prop F: m = -q(1-q) = -2s  (kinetic, not potential)
  frame (m=+-1): exact 0 if background a-eq holds (C4)

K depends on the demand normalization:
  EL-correct demand   (L-2k)/2k = 2s y^-q  => K = 6s    => m_fix = 4s
  agent demand        pi(L-2k)/k = s y^-q  => K = 3s/2pi => m_fix = s/pi
  'half-sigma' demand (L-2k)/2k = s y^-q   => K = 3s    => m_fix = 2s
"""
import numpy as np
s = 1.0/9.0
print(f"s = {s:.6f}, 2s = {2*s:.6f}")
for name, K in [("EL-correct (K=6s)", 6*s),
                ("agent 4pi-dropped (K=3s/2pi)", 3*s/(2*np.pi)),
                ("half-sigma (K=3s)", 3*s)]:
    m = (2.0/3.0)*K
    print(f"  {name}: m_fix = {m:.6f} = {m/s:.4f} s")
print()
print("Coupled (u,a0) responsive treatment, consistent orthonormal modes")
print("(c0 = sqrt(4pi) dF, a0), V-hat = (1/4) d2P in orthonormal coords:")
print("  rank-1 exact => eigenvalues {0, tr}; tr = W(k^2+3)/(2 k^3 F) -> 2/F")
print("  (the 2/F is the bare l(l+1)=2 angular stiffness, huge vs s; the 0 is")
print("   the scaling flat). NO channel lands at 's' in any variant tested.")
print()
print("Verdict input: 'responsive = 2 x fixed' does not emerge from any")
print("consistent normalization; the only clean constants are 0, -2s (scaling")
print("kinetic), 4s (EL-correct fixed-a), 2/F (bare angular stiffness).")
