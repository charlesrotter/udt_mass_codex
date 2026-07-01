"""
UDT spectrum, next step: Z3 tight-binding recast.
DERIVED (exact): three cells on a Z3 ring have a circulant sqrt-mass operator
  C = a I + b P + b* P^2,  eigenvalues  sqrt(m_k) = a + 2|b| cos(beta + 2 pi k/3).
  Koide Q = 2/3  <=>  |b|/a = 1/sqrt2,  for ANY flux beta.
  b -> 0 (decoupled cells)  ->  Q = 1/3  (= the single-cell null result).
Lepton fit: |b|/a = 0.70710 (=1/sqrt2 to 5 figs), beta = 0.2222 ~ 2/9 = 2 q^2.
Electron light = flux 2.3 deg from a band node (NOT exponential m~MPl e^-Gamma).

SYNTHESIS: ring = topological N=3 (cand a); hopping b = ensemble coupling
(cand b); flux beta = dynamic phase (cand c). One operator, three slots.

NEXT COMPUTATION (kill/confirm): from the existing single soliton, compute the
two-soliton interaction energy in the shared back-reacted phi vs separation and
relative orientation. Extract on-site a (isolated sqrt-mass) and hopping b
(phi-mediated coupling).
  CONFIRM: |b|/a -> 1/sqrt2 and arg(b) -> ~2/9.
  KILL:    b -> 0 (decouple, Q->1/3) or |b|/a far from 1/sqrt2.
1/sqrt2 is unfittable: the scale cancels from the ratio.
"""
import numpy as np
sqrt_m = lambda a,bb,be: np.array([a+2*bb*np.cos(be+2*np.pi*k/3) for k in range(3)])
Q = lambda sm:(sm**2).sum()/sm.sum()**2

print("Koide vs hopping ratio (flux-independent):")
for ratio in [0.0,0.5,1/np.sqrt(2),0.9]:
    print(f"  |b|/a={ratio:.4f}  ->  Q={Q(sqrt_m(1,ratio,0.3)):.4f}")
print(f"  Koide 2/3 at |b|/a = 1/sqrt2 = {1/np.sqrt(2):.5f}\n")

me,mmu,mtau=0.51099895,105.6583755,1776.86
sm=np.sqrt([me,mmu,mtau]); a=sm.mean()
r=np.sqrt(((sm/a-1)**2).sum()*2/3); bb=r*a/2; be=np.arccos((sm[2]/a-1)/r)
print(f"lepton ring:  a={a:.4f}  |b|={bb:.4f}  |b|/a={bb/a:.5f}  beta={be:.5f} (2/9={2/9:.5f})")
print(f"Koide check Q={Q(sm):.6f};  decoupled limit Q={Q(sqrt_m(1,0,0)):.4f}")
