import numpy as np
import itertools
from fractions import Fraction as Fr

print("="*70)
print("PHASE-1 INDEPENDENT VERIFICATION (uncover-don't-invent)")
print("="*70)

# ---- 1. The bridge values & charge-as-multiplicity-ratio ----
j, l, kmax = Fr(1,2), 1, 3
twoj1, twol1 = 2*j+1, 2*l+1          # = 2, 3
B1 = Fr(1, 2*twol1**2)               # 1/(2*(2l+1)^2)
B3 = Fr(1, 2*twoj1**2)               # 1/(2*(2j+1)^2)
print(f"\n[1] Bridge values: B1=1/(2*(2l+1)^2)={B1}  B3=1/(2*(2j+1)^2)={B3}")
print(f"    B1/B3 = {B1/B3} = (2j+1)^2/(2l+1)^2 = {Fr(twoj1**2,twol1**2)}  -> match: {B1/B3==Fr(twoj1**2,twol1**2)}")
print(f"    sqrt(B1/B3) = (2j+1)/(2l+1) = {twoj1}/{twol1} = {float(twoj1)/float(twol1):.4f}  ('Q_u'=2/3)")
print(f"    alpha_s/alpha_EM = B3'/B1' ratio = (2l+1)^2/(2j+1)^2 = {Fr(twol1**2,twoj1**2)} = 9/4")
print(f"    => the NUMBER 2/3 IS a multiplicity ratio (skeleton). 'charge' is the LABEL.")

# NULL test on the charge identification: how many simple functions of {2,3} land near 2/3?
print("\n[1-NULL] Is landing on 2/3 from {2,3,5} generic? simple ratios a/b, sqrt, etc.:")
nums=[1,2,3,4,5,6,7,8,9]
hits=set()
for a in nums:
    for b in nums:
        for f,name in [(Fr(a,b),f"{a}/{b}"), ]:
            if abs(float(f)-2/3)<0.02: hits.add((name,float(f)))
print(f"    plain ratios within 2% of 0.667: {sorted(hits)}")
print(f"    -> 2/3 is the single simplest; but 'charge=sqrt(coupling ratio)' map is unforced (cr193 admits).")

# ---- 2. base masses as multiplicity squares ----
print(f"\n[2] base masses: m_u=(2j+1)^2 m_e={twoj1**2} m_e ; m_d=(2l+1)^2 m_e={twol1**2} m_e")
print(f"    FORM is skeleton-tied (multiplicity^2). Match to MS-bar (u~2.2,d~4.7 MeV) unfalsifiable (10-20% err).")

# ---- 3. PHASE-1d: color-singlet construction in 3(x)3(x)3 under SO(3), l=1 ----
print("\n[3] PHASE-1d: SO(3) singlet multiplicity in 3 x 3 x 3 (l=1 triplet)")
# Build l=1 angular momentum operators (3x3), basis m=+1,0,-1
# Standard spin-1 matrices
sq2=np.sqrt(2)
Jp=np.array([[0,sq2,0],[0,0,sq2],[0,0,0]])   # raising in m=+1,0,-1 ordering
Jm=Jp.T.conj()
Jz=np.diag([1,0,-1]).astype(complex)
Jx=(Jp+Jm)/2; Jy=(Jp-Jm)/(2j*0+2j); 
Jy=(Jp-Jm)/(2j) if False else (Jp-Jm)/(2*1j)
def kron3(A,B,C): return np.kron(np.kron(A,B),C)
I3=np.eye(3)
# total J on triple product
JX=kron3(Jx,I3,I3)+kron3(I3,Jx,I3)+kron3(I3,I3,Jx)
JY=kron3(Jy,I3,I3)+kron3(I3,Jy,I3)+kron3(I3,I3,Jy)
JZ=kron3(Jz,I3,I3)+kron3(I3,Jz,I3)+kron3(I3,I3,Jz)
J2=JX@JX+JY@JY+JZ@JZ
evals=np.linalg.eigvalsh(J2)
# singlet => J(J+1)=0
n_singlet=int(np.sum(np.abs(evals)<1e-9))
print(f"    dim(3x3x3)=27 ; eigenvalues of total J^2, count of J=0 (singlet): {n_singlet}")
# explicit: epsilon tensor
eps=np.zeros((3,3,3))
for p in itertools.permutations(range(3)):
    sign=np.linalg.det(np.array([[1 if i==p[k] else 0 for i in range(3)] for k in range(3)]))
    eps[p]=sign
vec=eps.reshape(27)/np.sqrt(6)
print(f"    Levi-Civita epsilon_abc: ||v||={np.linalg.norm(vec):.4f}, J^2 eigenvalue on it = {np.real(vec@J2@vec):.2e}")
print(f"    -> exactly {n_singlet} SO(3) singlet, and it IS the antisymmetric epsilon (baryon handle). WELL-DEFINED.")

# meson: 3 x 3bar contains one singlet (delta_ab)
print("\n[3b] meson 3 x 3bar singlet (delta_ab): also multiplicity 1 (standard).")
print("="*70)
print("SUMMARY: skeleton (blocks/su(3)/singlet/multiplicity-numbers) computes clean.")
print("         charge/mass *interpretation map* is the free label (ontology-ii).")
