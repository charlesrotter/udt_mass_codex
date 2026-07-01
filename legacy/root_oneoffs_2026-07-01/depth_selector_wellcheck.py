import numpy as np
# Verify the verifier: does U(D)=c_grav(e^{2D}-1)+(1/2)A0^2*max(omega^2,0) develop a
# genuine INTERIOR minimum (with omega^2>0 there, not tachyonic) above a threshold R=A0^2/c_grav?
floor=2.0; Dstar=2.6; k=4.0
c_bind=floor/Dstar**k
def omega2(D): return floor - c_bind*np.asarray(D,float)**k
def U(D,cg,A0sq):
    return cg*(np.exp(2*np.asarray(D,float))-1) + 0.5*A0sq*np.maximum(omega2(D),0.0)
Dg=np.linspace(1e-3,Dstar-1e-3,8000)
cg=1.0
for A0sq in [50,100,136,150,300,1000]:
    Uv=U(Dg,cg,A0sq)
    imin=1+np.where((Uv[1:-1]<Uv[:-2])&(Uv[1:-1]<Uv[2:]))[0]
    if len(imin):
        Dm=Dg[imin[0]]; w2=omega2(Dm)
        print(f"R=A0^2/c_grav={A0sq/cg:7.1f}: INTERIOR MIN at D={Dm:.3f}, omega^2 there={w2:.3f} ({'STABLE' if w2>0 else 'TACHYON'}), depth={Uv[imin[0]]-Uv.min() if False else 0:.0f}")
    else:
        Dm=Dg[Uv.argmin()]
        print(f"R=A0^2/c_grav={A0sq/cg:7.1f}: NO interior min (min at D={Dm:.3f}, {'edge' if Dm<0.01 or Dm>Dstar-0.01 else 'interior'})")
# How many BOUND depth levels does the genuine well hold? (R=300, well clear of cap)
print("\n--- rung count in the genuine omega^2>0 well (R=300) ---")
A0sq=300.0
Dg2=np.linspace(1e-3,Dstar,2500+2)[1:-1]; h=Dg2[1]-Dg2[0]
Uv=U(Dg2,cg,A0sq)
imin=1+np.where((Uv[1:-1]<Uv[:-2])&(Uv[1:-1]<Uv[2:]))[0]
Dm=Dg2[imin[0]]; Umin=Uv[imin[0]]
# barrier tops: left edge value and the local max to the right of the min
right=Uv[imin[0]:]; 
lmax_idx=imin[0]+np.argmax(right[:np.argmin(np.abs(Dg2[imin[0]:]-Dstar))] if False else right)
# simpler: well is bounded by min(U(0+), U(Dstar))? left side rises toward D->0 (carrier barrier)
Uleft=Uv[0]; Uwall=U(Dstar-1e-4,cg,A0sq)
well_top=min(Uleft,Uwall)
for m_D in [1.0,4.0,16.0,64.0]:
    main=1.0/(m_D*h**2)+Uv; off=-1.0/(2*m_D*h**2)*np.ones(len(Dg2)-1)
    T=np.diag(main)+np.diag(off,1)+np.diag(off,-1)
    ev=np.linalg.eigvalsh(T)
    nb=np.sum((ev>Umin-1e-6)&(ev<well_top))
    print(f"  m_D={m_D:5.1f}: well[{Umin:.2f},{well_top:.2f}] bound levels={nb}  E0={ev[0]:.3f}")
print("  (if #bound tracks m_D => box-controlled even in the genuine well)")
