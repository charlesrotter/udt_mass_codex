import os; os.environ.setdefault("PYTORCH_NVML_BASED_CUDA_CHECK","0")
import numpy as np, sympy as sp, torch
torch.set_default_dtype(torch.float64)
# Compare G_{mn}=d_m n.d_n n between MY hedgehog nA and the committed torch 'dn' in matter_stress_t.
# committed dn (from spectral_catalog_solver.matter_stress_t):
#  dn[RR,0]=cT*sth*dr_Th ; dn[RR,2]=cT*cth*dr_Th ; dn[RR,3]=-sT*dr_Th
#  dn[TH,0]=cT*sth*dth_Th+sT*cth ; dn[TH,2]=cT*cth*dth_Th - sT*sth ; dn[TH,3]=-sT*dth_Th
#  dn[PS,1]=sT*sth
# That's d_mu of components (n^1,n^2? ) Let's just compute Gmn_committed = dn@dn^T and compare to mine.
# committed indices: rows m in {RR=1,TH=2,PS=3}, A in {0,1,2,3}. So Gmn_comm[m,n]=sum_A dn[m,A]dn[n,A].
r=1.3; th=0.8; Th=1.1; drTh=0.4; dthTh=-0.25
sth,cth=np.sin(th),np.cos(th); sT,cT=np.sin(Th),np.cos(Th)
dn=np.zeros((4,4))
dn[1,0]=cT*sth*drTh; dn[1,2]=cT*cth*drTh; dn[1,3]=-sT*drTh
dn[2,0]=cT*sth*dthTh+sT*cth; dn[2,2]=cT*cth*dthTh-sT*sth; dn[2,3]=-sT*dthTh
dn[3,1]=sT*sth
Gcomm=dn@dn.T
# MY nA: [cosTh, sinTh sinth cospsi, sinTh sinth sinpsi, sinTh costh]; d_mu over (t,r,theta,psi)
# evaluate G_{mn} for m,n in r,theta,psi at psi=0, Th=Th(r,theta)
rs,ths,pss,ThF=sp.symbols('rs ths pss ThF')
Thr,Tht=sp.symbols('Thr Tht')  # dTh/dr, dTh/dth
Thfun=sp.Function('Th')(rs,ths)
sTf,cTf=sp.sin(Thfun),sp.cos(Thfun)
nA=[cTf, sTf*sp.sin(ths)*sp.cos(pss), sTf*sp.sin(ths)*sp.sin(pss), sTf*sp.cos(ths)]
coords=[sp.symbols('t'),rs,ths,pss]
Gm=sp.zeros(4,4)
for m in range(4):
 for n in range(4):
  Gm[m,n]=sum(sp.diff(nA[A],coords[m])*sp.diff(nA[A],coords[n]) for A in range(4))
sub={sp.diff(Thfun,rs):Thr,sp.diff(Thfun,ths):Tht,Thfun:ThF,pss:0,ths:th,ThF:Th,Thr:drTh,Tht:dthTh}
Gmine=np.array([[float(Gm[m,n].subs(sub)) for n in range(4)] for m in range(4)])
print("G_{mn} committed (dn):")
print(np.round(Gcomm,5))
print("G_{mn} mine (nA hedgehog):")
print(np.round(Gmine,5))
print("max abs diff:", np.max(np.abs(Gcomm-Gmine)))
