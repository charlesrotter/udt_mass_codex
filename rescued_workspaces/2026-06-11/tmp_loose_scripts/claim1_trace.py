import sympy as sp
# Trace check for Dirac.  On-shell, T^mu_mu = m psibar psi for a Dirac field (standard).
# Claim says psibar psi = e^{PHI}(G^2 - F^2).
# The Form-T radial system uses radial functions G,F. The Dirac bilinear scalar density
# psibar psi for a single radial mode is, up to the metric/measure factor, ~ (G^2 - F^2).
# The e^{PHI} factor is the local frame/measure factor (vierbein) e^{PHI}=e^{-phi}=sqrt(-g_tt... )
# Let's at least verify DIMENSIONAL/structural consistency of the SOURCE vs the trace.
#
# Source claim:  T^r_r - T^t_t = -2 sigma [ kappa(F^2-G^2)/r + PHI'(F^2+G^2) + m e^{PHI} G F ]
# Trace claim:   T^mu_mu = m e^{PHI}(G^2-F^2)
#
# Key STRUCTURAL test: the mass channel.  In the Dirac stress tensor the mass appears ONLY
# through the trace (kinetic part is traceless).  The mass term in (T^r_r - T^t_t) is
#   -2 sigma * m e^{PHI} G F.
# Is "G F" the right mass structure (vs G^2-F^2 in the trace)? These differ, which is the
# correct expectation: T^mu_mu picks the scalar bilinear (G^2-F^2)e^{PHI}; but T^r_r-T^t_t is
# a DIFFERENCE of diagonal components, which for Dirac mixes via the off-diagonal vierbein
# structure -> GF can legitimately appear.  Let's test the coefficient by a CONCRETE
# flat-space-limit cross-check instead (phi->0, PHI->0), where the radial Dirac is standard.
print("structural note: trace uses G^2-F^2, source mass term uses GF -- these are genuinely")
print("different bilinears; consistency must come from explicit vierbein, checked numerically next.")
