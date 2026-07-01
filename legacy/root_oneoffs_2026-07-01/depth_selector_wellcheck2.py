import numpy as np
floor=2.0; Dstar=2.6; k=4.0; c_bind=floor/Dstar**k; cg=1.0
def omega2(D): return floor - c_bind*np.asarray(D,float)**k
def U(D,A0sq): return cg*(np.exp(2*np.asarray(D,float))-1)+0.5*A0sq*np.maximum(omega2(D),0.0)
# scan R to map the window where a genuine interior min (omega^2>0) exists
print("R window where a genuine omega^2>0 interior minimum exists:")
Dg=np.linspace(1e-3,Dstar-1e-3,12000)
Rwin=[]
for R in np.arange(120,400,5.0):
    Uv=U(Dg,R); imin=1+np.where((Uv[1:-1]<Uv[:-2])&(Uv[1:-1]<Uv[2:]))[0]
    if len(imin) and Dg[imin[0]]<Dstar-0.02 and omega2(Dg[imin[0]])>0:
        Rwin.append(R)
if Rwin: print(f"  genuine interior-well window: R in [{min(Rwin)}, {max(Rwin)}]")
else: print("  none")

# rung count in a genuine well (pick R=160, well clear of cap edge)
for R in [140,160,200]:
    Dg2=np.linspace(1e-3,Dstar,3000+2)[1:-1]; h=Dg2[1]-Dg2[0]
    Uv=U(Dg2,R)
    imin=1+np.where((Uv[1:-1]<Uv[:-2])&(Uv[1:-1]<Uv[2:]))[0]
    if not len(imin): print(f"R={R}: no interior min on this grid"); continue
    Dm=Dg2[imin[0]]; Umin=Uv[imin[0]]
    # local maximum to the LEFT of the min (the carrier barrier) bounds the well on the left
    leftseg=Uv[:imin[0]]
    lmax=leftseg.max() if len(leftseg) else Uv[0]
    Uwall=U(Dstar-1e-4,R)
    well_top=min(lmax,Uwall)
    print(f"\nR={R}: interior min D={Dm:.3f} (omega^2={omega2(Dm):.2f}), U_min={Umin:.2f}, well_top={well_top:.2f}, well_depth={well_top-Umin:.2f}")
    for m_D in [1.0,4.0,16.0,64.0]:
        main=1.0/(m_D*h**2)+Uv; off=-1.0/(2*m_D*h**2)*np.ones(len(Dg2)-1)
        T=np.diag(main)+np.diag(off,1)+np.diag(off,-1); ev=np.linalg.eigvalsh(T)
        nb=int(np.sum((ev>Umin-1e-6)&(ev<well_top)))
        print(f"   m_D={m_D:5.1f}: bound-in-well levels={nb}  E0={ev[0]:.3f} E1={ev[1]:.3f}")
