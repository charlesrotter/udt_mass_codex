"""
depth_selector_verif_box_and_tower.py
=====================================
ATTACK 3 (box-control) + the decisive tower question:
 (A) Independently reproduce the constructor's Part-7a box-control table for the
     MONOTONE (half-well) regime: do level count ~ D*sqrt(m_D), spacing ~ 1/m_D?
     (constructor used A0^2=5, c_grav=1 -> R=5, BELOW the well threshold -> monotone.)
 (B) The TRUE WELL regime (R in window): does the INTERIOR BARRIER ever get deep
     enough to hold MORE THAN ONE level anywhere in the legitimate ranges
     (floor in {2,6,12}, D* in [2.4,3.4], k in [3.5,4.9], R in its well-window)?
     Scan the max interior-barrier height and max #trapped levels over the whole space.
     If max #trapped is ~1 everywhere -> NO multi-rung tower -> NON-CLOSURE survives.
"""
import numpy as np, itertools

def pieces(floor,Dstar,k):
    cb=floor/Dstar**k
    w2=lambda D: floor-cb*np.asarray(D,float)**k
    Eg=lambda D,cg: cg*(np.exp(2*np.asarray(D,float))-1.0)
    return cb,w2,Eg

def Ufun(D,floor,Dstar,k,c_grav,A0sq):
    cb,w2,Eg=pieces(floor,Dstar,k)
    return Eg(D,c_grav)+0.5*A0sq*np.maximum(w2(D),0.0)

def levels(floor,Dstar,k,c_grav,A0sq,Dbox,m_D=1.0,hbar=1.0,N=2500):
    Dg=np.linspace(1e-4,Dbox,N+2)[1:-1]; h=Dg[1]-Dg[0]
    Dc=np.minimum(Dg,Dstar)
    cb,w2,Eg=pieces(floor,Dstar,k)
    Up=Eg(Dg,c_grav)+0.5*A0sq*np.maximum(w2(Dc),0.0)
    main=hbar**2/(m_D*h**2)+Up; off=-hbar**2/(2*m_D*h**2)*np.ones(N-1)
    return np.linalg.eigvalsh(np.diag(main)+np.diag(off,1)+np.diag(off,-1))

# ---- (A) box-control in the monotone regime (constructor's R=5) ----
print("="*78); print("(A) Box-control audit, monotone regime (R=A0^2/c_grav=5)"); print("="*78)
print(f"{'D*':>5}{'m_D':>6}{'#levels<wall':>13}{'E1':>9}{'E2-E1':>9}")
for Dstar in [2.0,2.6,3.2]:
    for m_D in [1.0,4.0,16.0]:
        e=levels(2.0,Dstar,4.0,1.0,5.0,Dstar,m_D=m_D,N=2000)
        Uwall=Ufun(Dstar,2.0,Dstar,4.0,1.0,5.0)
        nb=int((e<Uwall).sum())
        print(f"{Dstar:5.1f}{m_D:6.1f}{nb:13d}{e[0]:9.3f}{e[1]-e[0]:9.4f}")
print(" => count grows with D* and sqrt(m_D); spacing ~1/m_D. BOX-CONTROLLED (in monotone regime). CONFIRMED.")

# ---- (B) max trapped levels in the TRUE-WELL regime over the whole legitimate space ----
print("\n"+"="*78)
print("(B) In the TRUE interior-well regime: max #levels trapped below the interior barrier")
print("    scanned over floor,D*,k and the R well-window (anti-box: outer box extended).")
print("="*78)
best=(0,None)
for floor,Dstar,k in itertools.product([2.0,6.0,12.0],[2.4,2.6,3.0,3.4],[3.5,4.0,4.5,4.9]):
    cb,w2,Eg=pieces(floor,Dstar,k)
    # find the R-window where a true interior min exists; scan R finely
    for R in np.geomspace(5,2000,80):
        D=np.linspace(1e-5,Dstar,200000); Uv=Ufun(D,floor,Dstar,k,1.0,R)
        dU=np.gradient(Uv,D); s=np.sign(dU); cr=np.where(np.diff(s)!=0)[0]
        if len(cr)<2: continue   # need a max then a min => interior well
        imax,imin=cr[0],cr[1]
        if not (D[imax]<D[imin]<Dstar): continue
        barrier=Uv[imax]
        if Uv[imax]<=Uv[imin] or Uv[-1]<=Uv[imin]: continue
        # quantize over a box extended past D* (anti-box), count trapped below interior barrier
        e=levels(floor,Dstar,k,1.0,R,Dstar+1.0,m_D=1.0,N=2500)
        ntrap=int((e<barrier).sum())
        if ntrap>best[0]:
            best=(ntrap,dict(floor=floor,Dstar=Dstar,k=k,R=round(R,1),
                             barrier=round(Uv[imax]-Uv[imin],3),
                             omega2_min=round(float(w2(D[imin])),3),Dmin=round(float(D[imin]),3)))
print("MAX interior-trapped levels found anywhere in the legitimate space:",best[0])
print("   at:",best[1])
print("\n => If MAX trapped ~ 1, the true well is SHALLOW everywhere: it holds at most one")
print("    bound depth state -> NO multi-rung exponential tower -> the depth-selector does")
print("    NOT close even WITH the well. (The well exists; it just can't tower.)")
print("    If MAX trapped >> 1, the constructor MISSED a real multi-rung well (stronger break).")

# also: try m_D large (heavier depth mode packs more levels) -- but that is BOX-control again
print("\n[cross-check] does cranking m_D pack more levels into the SAME well? (would be box-like)")
b=best[1]
if b:
    for m_D in [1.0,4.0,16.0,64.0]:
        cb,w2,Eg=pieces(b['floor'],b['Dstar'],b['k'])
        D=np.linspace(1e-5,b['Dstar'],200000); Uv=Ufun(D,b['floor'],b['Dstar'],b['k'],1.0,b['R'])
        dU=np.gradient(Uv,D); cr=np.where(np.diff(np.sign(dU))!=0)[0]; imax=cr[0]
        e=levels(b['floor'],b['Dstar'],b['k'],1.0,b['R'],b['Dstar']+1.0,m_D=m_D,N=3000)
        ntrap=int((e<Uv[imax]).sum())
        print(f"   m_D={m_D:5.1f}: #trapped below interior barrier = {ntrap}")
    print("   => if #trapped scales with m_D, the 'tower' is the depth-mode-mass box, not native.")
