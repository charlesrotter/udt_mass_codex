from numpy import pi
me=0.51099895; rstar=6.9875; C=4*pi**2*me*rstar
print("angular masses m/m_e = 4A pi^Q  (Q=pi-power, A=coeff):")
for n,Q,A in [("electron",0,0.25),("PION",1,21.0),("muon",3,5/3),("proton",5,1.5)]:
    print(f"  {n:>8}  Q={Q}  4A={4*A:7.3f}   m/m_e={4*A*pi**Q:9.2f}")
print()
print("Q (e,pi,mu,p) = 0,1,3,5")
print("lepton/proton rule: Q=2l+1 (mu l=1->3, p l=2->5; electron is the EXCEPTION pi^0)")
print("pion (CG13.10): Q=2j, j=1/2 -> pi^1 = SPIN rule, DIFFERENT from the orbital rule")
print()
print(f"decompose: m_pi=84pi m_e = (84pi/4pi^2)(C/r*) = (21/pi)(C/r*) = {21/pi:.4f} (C/r*)")
print("  -> the lone pi traces to the C-anchor's 4pi^2, shuffled with a radial 1/pi;")
print("     it does NOT reduce to a single pion-specific sphere integral.")
