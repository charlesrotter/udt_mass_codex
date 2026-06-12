import numpy as np, itertools
from scipy.integrate import solve_ivp
mu2=np.pi/3; rstar=6.9875; phi0=-np.cos(np.pi/5)
me=0.51099895; C=4*np.pi**2*me*rstar
def rhs(r,y):
    phi,J=y; return [J*np.exp(2*phi)/r**2, r**2*mu2*phi]
sol=solve_ivp(rhs,[1e-6,rstar],[phi0,0.0],rtol=1e-11,atol=1e-13,max_step=0.001)
phiE=sol.y[0,-1]; JE=sol.y[1,-1]; em2=np.exp(-2*phiE); mMS=(rstar/2)*(1-em2)

# Numerology baseline: how many "hits" within 0.3% do we get from random-magnitude
# primitives times the same factor set? Count density.
prim_vals=[abs(mMS),em2,np.exp(-phiE),0.7554,0.3777,rstar,abs(phiE),abs(JE),13/np.pi,em2-1]
factors=[1,np.pi,1/np.pi,2*np.pi,np.pi/2,4*np.pi**2,np.pi**2,2,.5,3,1/3,4,6,1/6]
dtargs=[938.272/C,1836.15267]
N=0;hit=0
for p in prim_vals:
  for a,b in itertools.product(prim_vals,prim_vals):
    for combo in [a*b,a/b if b else 0,a-b,a+b,p]:
      if combo<=0 or not np.isfinite(combo):continue
      for f in factors:
        v=combo*f;N+=1
        for t in dtargs:
          if abs(v-t)/t<0.003: hit+=1
print(f"Numerology baseline: {hit} hits within 0.3% out of {N} expressions = {100*hit/N:.3f}% hit rate")
print("=> a 0.2-0.3% 'hit' from this large search space is EXPECTED by chance, not significant.")
print()
# The only structurally clean candidate: A = |phi'(r*)| r*^2 = |JE|/em2
A=abs(JE)/em2
print(f"Cleanest candidate A=|phi'(r*)|*r*^2={A:.5f} vs m_p/C=6.65621, err={abs(A-6.65621)/6.65621*100:.3f}%")
print(f"  but d(ln A)/d(ln r*) ~ 8  => 0.21% closeness requires r* to 0.03% precision (r* is itself locked/fit)")
