import numpy as np, sys
sys.path.insert(0,'.')
from engine2 import build_channel
from driver import get_profile, assemble_and_solve

# Angular harmonic factors. Real harmonics in (th,ph).
def Y(l,m):
    import numpy as np
    if l==0: return lambda T,P: np.ones_like(T)
    if l==1:
        if m==0:  return lambda T,P: np.cos(T)
        if m==1:  return lambda T,P: np.sin(T)*np.cos(P)
        if m==-1: return lambda T,P: np.sin(T)*np.sin(P)
    if l==2:
        if m==0:  return lambda T,P: (3*np.cos(T)**2-1)
        if m==1:  return lambda T,P: np.sin(T)*np.cos(T)*np.cos(P)
        if m==-1: return lambda T,P: np.sin(T)*np.cos(T)*np.sin(P)
        if m==2:  return lambda T,P: np.sin(T)**2*np.cos(2*P)
        if m==-2: return lambda T,P: np.sin(T)**2*np.sin(2*P)
    raise ValueError

def run_channel(p,R,fang,gang,Nr=160,Nth=160,Nph=24,r_core=0.05,bc='dirichlet'):
    F,Fp,phi,sol=get_profile(p,R,r_core=r_core)
    rgrid=np.linspace(r_core+1e-3, r_core+R-1e-3, Nr)
    Pr,Qr,Rr,Wr,_=build_channel(F,Fp,phi,fang,gang,rgrid,Nth=Nth,Nph=Nph)
    ev,evec,idx=assemble_and_solve(Pr,Qr,Rr,Wr,rgrid,bc=bc)
    return ev,evec,idx,rgrid,(Pr,Qr,Rr,Wr)

if __name__=='__main__':
    p=0; R=18.0
    print("=== convergence check on l=0 breathing (f=1 on e1) ===")
    for Nph in (8,16,32):
        ev,*_=run_channel(p,R, Y(0,0), lambda T,P:0*T, Nph=Nph)
        print(f"  Nph={Nph}: lowest 4 omega^2 =", np.round(ev[:4],5))
    print("\n=== e1 (polar) with l=1 m=0 angular factor cos(theta) ===")
    ev,*_=run_channel(p,R, Y(1,0), lambda T,P:0*T)
    print("  lowest 6:", np.round(ev[:6],5))
    print("\n=== e2 (azimuthal) with l=1 m=0 ===")
    ev,*_=run_channel(p,R, lambda T,P:0*T, Y(1,0))
    print("  lowest 6:", np.round(ev[:6],5))
