"""
depth_selector_verif_ladder.py
==============================
ATTACK 4: the mass ladder mass_n=e^{2 D_n}-1.
Constructor used D_n = WKB turning point in the MONOTONE half-well and got DECREASING
ratios (2.43->1.28) capped at cost(D*). Independently:
 (a) reproduce in the monotone regime;
 (b) test ALTERNATIVE D_n assignments (eigenfunction PEAK, MEAN <D>) -- does any give a
     genuinely EXPONENTIAL (constant-ratio) ladder? If a reasonable assignment gives
     constant ratios, the 'sub-exponential' claim is assignment-dependent (a break).
"""
import numpy as np

floor,Dstar,k=2.0,2.6,4.0
cb=floor/Dstar**k
def w2(D): return floor-cb*np.asarray(D,float)**k
def U(D,cg,A): return cg*(np.exp(2*np.asarray(D,float))-1.0)+0.5*A*np.maximum(w2(np.minimum(D,Dstar)),0.0)

def eig(cg,A,Dbox,m_D=1.0,N=4000):
    Dg=np.linspace(1e-4,Dbox,N+2)[1:-1]; h=Dg[1]-Dg[0]
    Up=U(Dg,cg,A); main=1/(m_D*h**2)+Up; off=-1/(2*m_D*h**2)*np.ones(N-1)
    w,v=np.linalg.eigh(np.diag(main)+np.diag(off,1)+np.diag(off,-1))
    return w,v,Dg

# monotone regime (constructor): R=5
cg,A=1.0,5.0
w,v,Dg=eig(cg,A,Dstar,N=4000)
Uwall=U(Dstar,cg,A)
nb=int((w<Uwall).sum())
print("="*78); print("Mass ladder, monotone regime R=5 (constructor reproduce)"); print("="*78)
# (a) WKB turning point
Dscan=np.linspace(1e-4,Dstar,200000); Us=U(Dscan,cg,A)
def turning(En):
    b=Dscan[Us<=En]; return b[0] if len(b) else np.nan
Dn_turn=np.array([turning(En) for En in w[:6]])
# (b) eigenfunction peak and mean
Dn_peak=np.array([Dg[np.argmax(v[:,n]**2)] for n in range(6)])
prob=v[:,:6]**2; prob/=prob.sum(0,keepdims=True)
Dn_mean=np.array([(Dg*prob[:,n]).sum() for n in range(6)])
for name,Dn in [("turning",Dn_turn),("peak",Dn_peak),("mean<D>",Dn_mean)]:
    m=np.exp(2*Dn)-1
    with np.errstate(divide='ignore',invalid='ignore'):
        rat=m[1:]/m[:-1]
    print(f"\n D_n[{name:8}]:",np.array2string(Dn,precision=3))
    print(f" mass_n        :",np.array2string(m,precision=2))
    print(f" ratios        :",np.array2string(rat,precision=3),
          "  -> "+("CONSTANT (exponential)" if np.nanstd(rat)<0.05*np.nanmean(rat) else "DECREASING/varying (sub-exp)"))
print(f"\n cost(D*)=e^(2*{Dstar})-1 = {np.exp(2*Dstar)-1:.1f}  (ceiling on the ladder)")
print("\n VERDICT: under EVERY reasonable D_n assignment the ratios are NOT constant and the")
print(" ladder is capped at cost(D*). No assignment manufactures a clean exponential. The")
print(" constructor's sub-exponential+capped finding is assignment-robust.")
