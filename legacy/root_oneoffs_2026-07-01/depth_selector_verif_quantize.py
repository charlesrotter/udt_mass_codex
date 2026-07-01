"""
depth_selector_verif_quantize.py
================================
The dip EXISTS (verif_analytic). Now: does the well RESCUE the depth-selector?
Build U(D) at a supercritical ratio R=A0^2/c_grav, confirm the interior well, and
quantize the depth mode in it. Ask:
  (a) Is it a TRUE double-well (left barrier from carrier energy at D=0, right wall
      = exponential rise toward D*)? How many bound levels does it hold?
  (b) Are those levels BOX-controlled (track D*, m_D) or WELL-intrinsic (track the
      well curvature, R-independent of the cap)?  ANTI-BOX test: vary the cap D* with
      the well fixed -> do the SUB-well levels move?
  (c) mass ladder mass_n = e^{2 D_n}-1 at the turning points: exponential or saturating?

I re-implement the depth eigensolve from scratch (numpy eigvalsh), do NOT trust the
constructor's torch tridiagonal.
"""
import numpy as np

def make(c_grav, A0sq, floor, Dstar, k):
    c_bind = floor/Dstar**k
    Eg  = lambda D: c_grav*(np.exp(2*np.asarray(D,float))-1.0)
    w2  = lambda D: floor - c_bind*np.asarray(D,float)**k
    Uph = lambda D: Eg(D) + 0.5*A0sq*np.maximum(w2(D),0.0)
    return Eg,w2,Uph,c_bind

# supercritical: floor=2, D*=2.6, k=4 -> R_threshold ~136. Use R=400 (A0^2=400,c_grav=1).
floor,Dstar,k = 2.0,2.6,4.0
c_grav,A0sq = 1.0,400.0
Eg,w2,Uph,cb = make(c_grav,A0sq,floor,Dstar,k)

D=np.linspace(1e-5,Dstar,500000); Uv=Uph(D)
imin=np.argmin(Uv); Dmin=D[imin]
print("="*78); print("Supercritical well: floor=2,D*=2.6,k=4, A0^2/c_grav=400"); print("="*78)
print(f"U(0)={Uv[0]:.3f}  U_min={Uv[imin]:.3f}@D={Dmin:.3f}  U(D*)={Uv[-1]:.3f}  omega2(Dmin)={w2(Dmin):.3f}")
print(f"left barrier U(0)-Umin = {Uv[0]-Uv[imin]:.3f}   right barrier U(D*)-Umin = {Uv[-1]-Uv[imin]:.3f}")
true_well = (Uv[0]>Uv[imin]) and (Uv[-1]>Uv[imin])
print(f"TRUE interior double-well (both barriers>0)? {true_well}")

# ---- (a) quantize depth in [0,D*] hard walls (postulate A), count bound levels ----
def depth_levels(Uph,Dstar,m_D=1.0,hbar=1.0,N=3000):
    Dg=np.linspace(1e-4,Dstar,N+2)[1:-1]; h=Dg[1]-Dg[0]
    Up=Uph(Dg)
    main=hbar**2/(m_D*h**2)+Up
    off=-hbar**2/(2*m_D*h**2)*np.ones(N-1)
    T=np.diag(main)+np.diag(off,1)+np.diag(off,-1)
    e=np.linalg.eigvalsh(T)
    return e,Dg,Up

e,Dg,Up=depth_levels(Uph,Dstar,m_D=1.0)
Uwall=Uph(Dstar); Umin=Up.min()
bound=e[(e<Uwall)]
print(f"\nDepth eigenlevels (m_D=1): first 8 = {np.array2string(e[:8],precision=3)}")
print(f"U_min={Umin:.3f} U(D*)={Uwall:.3f}  #levels below right wall = {len(bound)}")
# levels BELOW the LEFT barrier U(0) are truly trapped in the interior well
trapped=e[e<Uv[0]]
print(f"#levels below the LEFT barrier U(0)={Uv[0]:.3f} (truly interior-trapped) = {len(trapped)}")

# ---- (b) ANTI-BOX test: vary cap D* >> well, keep well fixed; do interior levels move? ----
print("\n[ANTI-BOX] extend the box wall D*_box beyond the well's right side; do the")
print("           interior-trapped levels stay put (well-intrinsic) or move (box)?")
# Build the SAME physical U but extend the integration box to D*_box > Dstar by holding
# the carrier capped at 0 beyond Dstar (omega2 already 0 there); E_grav keeps rising, so
# beyond Dstar U = E_grav alone = a steep exp wall. The interior well is unchanged.
for Dbox in [Dstar, 3.0, 3.5, 4.0]:
    def Uext(D):
        D=np.asarray(D,float)
        return Eg(D)+0.5*A0sq*np.maximum(w2(np.minimum(D,Dstar)),0.0)  # carrier frozen at cap past D*
    eN,_,_=depth_levels(Uext,Dbox,m_D=1.0,N=4000)
    trap=eN[eN<Uv[0]]
    print(f"  D*_box={Dbox:4.1f}: lowest 4 = {np.array2string(eN[:4],precision=4)}  #below-left-barrier={len(trap)}")
print("  READ: if the lowest few are STABLE as D*_box grows, they are WELL-intrinsic (NOT box).")

# ---- (c) mass ladder at the turning points of the interior well ----
print("\n[mass ladder] mass_n = e^{2 D_n}-1, D_n = inner turning point U(D_n)=E_n in the well")
Dscan=np.linspace(1e-4,Dstar,200000); Us=Uph(Dscan)
Dn=[]
for En in e[:6]:
    # inner turning point: first crossing from the left wall up
    below=Dscan[Us<=En]
    Dn.append(below[0] if len(below) else np.nan)
Dn=np.array(Dn); mass=np.exp(2*Dn)-1
print("  n     :",list(range(len(Dn))))
print("  D_n   :",np.array2string(Dn,precision=3))
print("  mass_n:",np.array2string(mass,precision=3))
with np.errstate(divide='ignore',invalid='ignore'):
    print("  ratio :",np.array2string(mass[1:]/mass[:-1],precision=3))
print(f"  cap cost(D*)=e^{{2*{Dstar}}}-1 = {np.exp(2*Dstar)-1:.1f}  (ladder still capped at D*)")
