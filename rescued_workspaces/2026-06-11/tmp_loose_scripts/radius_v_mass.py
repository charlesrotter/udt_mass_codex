import numpy as np
me=0.51099895; rstar=6.9875; C=4*np.pi**2*me*rstar
# nat length unit: r* set so r_c(BH)=0.7554 nat. Corpus: 0.756 nat ~ 1.06 fm.
# => 1 nat = 1.06/0.756 fm = 1.4026 fm
fm_per_nat = 1.06/0.756
print("1 nat =",fm_per_nat,"fm")
# proton charge radius ~0.84 fm. r_c=0.7554 nat ->
print("r_c =",0.7554*fm_per_nat,"fm  (cf proton charge radius 0.84 fm)")
# A length unit in nat, to become a MASS, needs hbar*c/length:
hbarc=197.327 # MeV*fm
print("hbar c / r_c[fm] =",hbarc/(0.7554*fm_per_nat),"MeV  (a Compton-like mass for the horizon radius)")
# vs m_p=938.272
m_from_rc = hbarc/(0.7554*fm_per_nat)
print("  /m_p =",m_from_rc/938.272," => gives ~186 MeV, NOT proton mass")
# So the horizon radius -> a ~186 MeV scale (near pion!), not the proton.
print("  (near m_pi~140? or m_muon~106?)  186 MeV is between mu and pi")
