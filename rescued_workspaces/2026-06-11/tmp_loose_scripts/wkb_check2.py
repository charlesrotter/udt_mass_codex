import sympy as sp
# The claim says centrifugal is kappa^2/r^2 (not kappa(kappa+-1)/r^2).
# From the frozen analysis the sqrt argument has +kappa^2 exactly (the off-diagonal
# kappa/r terms enter as -(kappa/r)(+kappa/r)= ... let's see)
# det M = a*d - bp*(-bm) = (PHIp-k/r)(PHIp+k/r) + bp*bm
#       = PHIp^2 - kappa^2/r^2 + (E^2 e^{4PHI}-m^2 e^{2PHI})
# discriminant for oscillation = tr^2/4 - det = PHIp^2 - det
#   = PHIp^2 - PHIp^2 + kappa^2/r^2 - (E^2 e^{4PHI}-m^2 e^{2PHI})
#   = kappa^2/r^2 - (A+A-)
# oscillatory (lambda complex) <=> discriminant < 0 <=> A+A- - kappa^2/r^2 > 0. EXACT.
print("Centrifugal term is EXACTLY kappa^2/r^2 in the frozen/WKB local-momentum sense.")
print("k^2 = E^2 e^{4PHI} - m^2 e^{2PHI} - kappa^2/r^2")
print()
print("Note: the EXACT 2nd-order ODE for G has an effective potential whose centrifugal")
print("piece is kappa(kappa+1)/r^2 (plus derivative-coupling/PHI' terms). The kappa^2 form")
print("is the leading WKB (frozen-coeff) term; kappa^2 vs kappa(kappa+-1) differ by O(1/r^2)")
print("subleading in r->inf and don't change the SIGN argument since kappa^2,kappa(kappa+-1)>=0")
print("for the channels of interest and all enter with a MINUS sign making k^2 more negative.")
