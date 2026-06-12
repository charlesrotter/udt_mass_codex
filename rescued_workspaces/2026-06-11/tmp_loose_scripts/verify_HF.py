import sympy as sp
# Genuine first-order energy shift dE from Rayleigh quotient (the physical Hellmann-Feynman):
# The script's A.iii gave: dE_density = -2E e^{2phi}(G^2+F^2)dphi - m e^{phi}(F^2-G^2)dphi
# i.e. the REAL eigenvalue response to dphi is weighted by (G^2+F^2) [density], NOT GF.
# So §18.3a's claim that dphi modifies the eigenvalue via a "2E e^{2phi} GF" coupling is
# NOT the actual eigenvalue shift. The actual eigenvalue shift coupling is (G^2+F^2)-weighted.
# §18.3a's GF term, per the dispatch, only arises as |magnitude| of two cancelling off-diagonal pieces.
print("Actual first-order energy shift (Rayleigh/HF) is (G^2+F^2)-weighted, NOT GF.")
print("So §18.3a's '2E e^2phi GF as eigenvalue coupling' does NOT match the true HF shift.")
print("The dispatch's reconciliation: GF term = |magnitude of 2 cancelling off-diag pieces|.")
