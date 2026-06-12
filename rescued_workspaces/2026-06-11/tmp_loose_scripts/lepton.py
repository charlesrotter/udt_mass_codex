import numpy as np
# Lepton targets: m_mu/m_e=206.768, m_tau/m_e=3477.23 ; Koide Q for leptons:
me,mm,mt=0.5109989,105.6584,1776.86
Q=(me+mm+mt)/(np.sqrt(me)+np.sqrt(mm)+np.sqrt(mt))**2
print("lepton Koide Q =",round(Q,5)," (~2/3=",round(2/3,5),")")
print("ratios mu/e=",round(mm/me,2)," tau/e=",round(mt/me,2))
# The spectrum (mass=E) gives all E in (0.5,1): max ratio < 2. Cannot give 207,3477.
# Could binding (m-E) help? m-E in (0,0.5). ratios of binding could be large IF one level
# sits extremely close to threshold. But within a channel they accumulate at E->m,
# i.e. m-E ->0, so the SMALLEST binding is unbounded ratios -- but that's WITHIN a channel
# (same kappa = same particle type), not across the 3 generations.
# Across the 3 GROUND states (the natural 'three leptons'): E1,E2,E3 ~ 0.5,0.86,0.94
# m-E = 0.5,0.14,0.06 -> ratios ~3.6, 8.5 -> nowhere near 207,3477; Koide won't be 2/3 either.
