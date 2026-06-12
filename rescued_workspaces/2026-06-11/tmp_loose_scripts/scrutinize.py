import numpy as np
from scipy.integrate import solve_ivp
mu2=np.pi/3; rstar=6.9875; phi0=-np.cos(np.pi/5)
me=0.51099895; C=4*np.pi**2*me*rstar
def rhs(r,y):
    phi,J=y; return [J*np.exp(2*phi)/r**2, r**2*mu2*phi]
sol=solve_ivp(rhs,[1e-6,rstar],[phi0,0.0],rtol=1e-11,atol=1e-13,max_step=0.001)
phiE=sol.y[0,-1]; JE=sol.y[1,-1]
em2=np.exp(-2*phiE); mMS=(rstar/2)*(1-em2)
print(f"JE={JE:.4f}  em2={em2:.4f}  mMS={mMS:.4f}")

# Candidate A: |JE|/em2
print("\nA) |JE|/em2 =", abs(JE)/em2, " target m_p/C=6.65621, err=",
      abs(abs(JE)/em2-6.65621)/6.65621*100,"%")
# Is this geometric? |JE|/em2 -- JE is flux, em2 is metric. 
# Note m_MS=(r*/2)(1-em2). And phi'=J e^{2phi}/r^2 => J = phi' r^2 e^{-2phi}.
# At r*: J(r*)=phi'(r*) r*^2 e^{-2phi}. So |JE|/em2 = |phi'(r*)| r*^2. Check:
phipE=JE*np.exp(2*phiE)/rstar**2
print("phi'(r*) =",phipE,"  phi'(r*)*r*^2 =",phipE*rstar**2," (=JE/em2? )",JE/em2)
print("  so |JE|/em2 = |phi'(r*)|*r*^2 =", abs(phipE)*rstar**2)

# Candidate B: (em2-1)*|JE|/2
print("\nB) (em2-1)*|JE|/2 =",(em2-1)*abs(JE)/2," target 1836.15, err=",
      abs((em2-1)*abs(JE)/2-1836.15267)/1836.15267*100,"%")
# (em2-1) relates to m_MS: m_MS=(r*/2)(1-em2) => (em2-1)=-2 m_MS/r*
print("  (em2-1) = -2 mMS/r* =", -2*mMS/rstar)
print("  so B = (-2mMS/r*)*|JE|/2 = -mMS*|JE|/r* =", -mMS*abs(JE)/rstar)

# Sensitivity test: how much does the 'hit' move if r* shifts 1%?
print("\n=== Sensitivity: vary r* by +/-1%, recompute candidate A and B ===")
for frac in [0.99,0.995,1.0,1.005,1.01]:
    rs=rstar*frac
    s=solve_ivp(rhs,[1e-6,rs],[phi0,0.0],rtol=1e-11,atol=1e-13,max_step=0.001)
    pe,je=s.y[0,-1],s.y[1,-1]; e2=np.exp(-2*pe)
    A=abs(je)/e2; B=(e2-1)*abs(je)/2
    print(f"  r*={rs:.4f} ({frac}): A={A:.4f} (t6.656), B={B:.3f} (t1836.15)")
