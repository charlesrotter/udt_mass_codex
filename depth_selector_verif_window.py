"""
depth_selector_verif_window.py
==============================
The TRUE interior double-well exists in a WINDOW of R=A0^2/c_grav (~136-230 for
floor=2,D*=2.6,k=4). Build it IN the window, quantize, and decide whether it RESCUES
the depth-selector:
  (1) double-well confirmed (Umax then Umin, both barriers >0, omega2>0 throughout)?
  (2) how many bound levels BELOW the left (interior) barrier?  (a multi-rung tower?)
  (3) ANTI-BOX: are those interior levels intrinsic to the well curvature, or do they
      track the cap/box?  Vary the OUTER box beyond D* with the well fixed.
  (4) mass ladder mass_n=e^{2Dn}-1 at the well turning points: exponential or saturating?
  (5) PROVENANCE of the back-reaction A^2(D)=2c_grav(e^{2D}-1)/omega2(D): native or smuggled?
"""
import numpy as np

floor,Dstar,k=2.0,2.6,4.0
cb=floor/Dstar**k
def w2(D): return floor-cb*np.asarray(D,float)**k
def Eg(D,c_grav): return c_grav*(np.exp(2*np.asarray(D,float))-1.0)
def U(D,c_grav,A0sq): return Eg(D,c_grav)+0.5*A0sq*np.maximum(w2(D),0.0)

# pick R=170 (mid-window): omega2@min ~1.06, Dmin~2.15, well clear of D*
c_grav,A0sq=1.0,170.0
D=np.linspace(1e-5,Dstar,800000); Uv=U(D,c_grav,A0sq)
# locate interior max then min
dU=np.gradient(Uv,D); s=np.sign(dU); cr=np.where(np.diff(s)!=0)[0]
print("="*78); print(f"TRUE double-well at R={A0sq/c_grav} (floor=2,D*=2.6,k=4)"); print("="*78)
Dcross=D[cr]
print("dU/dD sign changes at D =",np.array2string(Dcross,precision=3))
imax=cr[0]; imin=cr[1] if len(cr)>1 else len(D)-1
Dmax,Dmin=D[imax],D[imin]
print(f"local MAX @D={Dmax:.3f} (U={Uv[imax]:.3f}), local MIN @D={Dmin:.3f} (U={Uv[imin]:.3f})")
print(f"omega2 along well: @Dmax={w2(Dmax):.3f} @Dmin={w2(Dmin):.3f}  (both>0 => REAL, not tachyonic)")
print(f"interior barrier (Umax - Umin) = {Uv[imax]-Uv[imin]:.3f}")
print(f"right wall (U(D*) - Umin)       = {Uv[-1]-Uv[imin]:.3f}")
print(f"=> a genuine interior well bounded by a LEFT carrier barrier and a RIGHT exp wall, omega2>0.")

# (2)+(3) quantize; count levels under the interior barrier; anti-box by extending outer box
def levels(c_grav,A0sq,Dbox,m_D=1.0,hbar=1.0,N=4000):
    Dg=np.linspace(1e-4,Dbox,N+2)[1:-1]; h=Dg[1]-Dg[0]
    # carrier capped/frozen at 0 beyond D* (omega2=0 there); E_grav keeps rising
    Dc=np.minimum(Dg,Dstar)
    Up=Eg(Dg,c_grav)+0.5*A0sq*np.maximum(w2(Dc),0.0)
    main=hbar**2/(m_D*h**2)+Up; off=-hbar**2/(2*m_D*h**2)*np.ones(N-1)
    T=np.diag(main)+np.diag(off,1)+np.diag(off,-1)
    return np.linalg.eigvalsh(T)

barrier_top=Uv[imax]   # interior levels = those below the local max (trapped in the well)
print(f"\nInterior-trapped levels = those below the local-max barrier U={barrier_top:.3f}")
print("[ANTI-BOX] extend outer box Dbox beyond D*; do the trapped levels stay put?")
for Dbox in [Dstar,3.0,3.5,4.5]:
    e=levels(c_grav,A0sq,Dbox)
    trap=e[e<barrier_top]
    print(f"  Dbox={Dbox:4.1f}: lowest 5 = {np.array2string(e[:5],precision=3)}  #trapped(<{barrier_top:.0f})={len(trap)}")
print("  READ: stable lowest levels as Dbox grows => WELL-INTRINSIC (the well, not the box, sets them).")

# (4) mass ladder at the well's inner turning points
e=levels(c_grav,A0sq,Dstar)
Dscan=np.linspace(1e-4,Dstar,400000); Us=U(Dscan,c_grav,A0sq)
trap=e[e<barrier_top]
Dn=[]
for En in trap[:6]:
    below=Dscan[(Dscan>Dmax)&(Us<=En)]  # turning point on the well's left flank (D>Dmax side)
    Dn.append(below[0] if len(below) else np.nan)
Dn=np.array(Dn); mass=np.exp(2*Dn)-1
print("\n[mass ladder] over the INTERIOR-TRAPPED levels, D_n = inner turning point of the well")
print("  n     :",list(range(len(Dn))))
print("  D_n   :",np.array2string(Dn,precision=3))
print("  mass_n:",np.array2string(mass,precision=3))
with np.errstate(divide='ignore',invalid='ignore'):
    print("  ratio :",np.array2string(mass[1:]/mass[:-1],precision=3))
print(f"  cost(D*)=e^(2*{Dstar})-1={np.exp(2*Dstar)-1:.1f}  (any tower still bounded by the cap)")

# (5) PROVENANCE of the back-reaction constraint
print("\n[PROVENANCE] back-reaction A^2(D)=2 c_grav(e^{2D}-1)/omega2(D):")
print("  This comes from EQUATING E_grav(D)=E_field(A,D)=(1/2)A^2 omega2(D).")
print("  i.e. it ASSUMES the MS dilation cost of depth D equals the carrier's field energy.")
print("  Is that the native Hamiltonian constraint? The native constraint is G^t_t = kappa T^t_t,")
print("  m(r)=int rho_carrier. Setting m(D)=E_field is a MODEL of that integral with (i) the")
print("  carrier energy = (1/2)A^2 omega2 (a HARMONIC/quadratic energy, valid only at small A),")
print("  and (ii) ALL the enclosed mass attributed to the carrier (no other source). Both are")
print("  MODELING CHOICES, native-FLAVORED but NOT the pointwise coupled G=kT solve. Flag: the")
print("  (1/2)A^2 omega2 energy is the LINEARIZED (quadratic) carrier energy -- Principle 2 caution")
print("  at finite amplitude. The U(D) assembly inherits this.")
