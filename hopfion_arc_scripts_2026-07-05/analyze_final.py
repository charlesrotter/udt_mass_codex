"""Analyze a saved relaxed hopfion: energy-density ring radius, core width (FWHM),
radial profile / localization, and Q. argv: npzfile"""
import sys, math, numpy as np, torch, fs_hopfion as m
f=np.load(sys.argv[1]); N=int(f['N']);L=float(f['L']);xi=float(f['xi']);kappa=float(f['kappa'])
n=torch.tensor(f['n'],device=m.dev)
X,Y,Z,h=m.make_grid(N,L)
nn=n/n.norm(dim=0,keepdim=True)
dn=m.grads(nn,h)
def cross(a,b): return torch.stack([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],0)
e2=0.5*xi*sum((dn[i]*dn[i]).sum(0) for i in range(3))
e4=torch.zeros_like(e2)
for i in range(3):
    for j in range(3):
        if i==j:continue
        Fij=(nn*cross(dn[i],dn[j])).sum(0); e4=e4+0.25*kappa*Fij*Fij
ed=(e2+e4).cpu().numpy()
xg=np.linspace(-L,L,N)
# ring radius: max energy density, and its cylindrical radius; use z~0 slab
iz0=np.argmin(np.abs(xg))
slab=ed[:,:,iz0]
ii=np.unravel_index(np.argmax(slab),slab.shape)
xm,ym=xg[ii[0]],xg[ii[1]]; Rring=math.hypot(xm,ym)
# n_inf check at box corner
ninf=nn[:,0,0,0].cpu().numpy()
# core width: profile of ed along +x axis through the ring center at z=0
line=ed[:, ii[1] if abs(ym)>abs(xm) else N//2, iz0]  # crude
# better: radial profile in z=0 plane vs cyl radius
XX,YY=np.meshgrid(xg,xg,indexing='ij')
rcyl=np.hypot(XX,YY)
# azimuthal average of ed in z=0 plane
nb=80; redges=np.linspace(0,L,nb+1); rc=0.5*(redges[:-1]+redges[1:])
prof=np.array([slab[(rcyl>=redges[k])&(rcyl<redges[k+1])].mean() if np.any((rcyl>=redges[k])&(rcyl<redges[k+1])) else 0 for k in range(nb)])
pk=prof.max(); ipk=prof.argmax()
half=pk/2
# FWHM around the peak
lo=ipk
while lo>0 and prof[lo]>half: lo-=1
hi=ipk
while hi<nb-1 and prof[hi]>half: hi+=1
fwhm=rc[hi]-rc[lo]
Etot=(ed.sum()*h**3)
# fraction of energy within r<2*Rring (localization)
mask=(np.hypot(np.hypot(XX[:,:,None],YY[:,:,None]), (xg[None,None,:]))<=2*Rring)
frac=(ed[mask].sum())/(ed.sum())
Q,_,_=m.hopf_charge(nn,h,N,L)
print(f"file={sys.argv[1]} N={N} L={L} xi={xi} kappa={kappa} h={h:.4f}")
print(f"  E_total={Etot:.3f} Ehat=E/sqrt(xik)={Etot/math.sqrt(xi*kappa):.3f} (published FS Q=1: 275.0)")
print(f"  Q={Q:.4f}")
print(f"  ring radius (z=0 peak)={Rring:.4f}  in units sqrt(k/xi)={math.sqrt(kappa/xi):.3f}: R/scale={Rring/math.sqrt(kappa/xi):.4f}")
print(f"  ring peak cyl-radius (azim prof)={rc[ipk]:.4f}  core FWHM={fwhm:.4f}  FWHM/sqrt(k/xi)={fwhm/math.sqrt(kappa/xi):.4f}")
print(f"  n_inf(corner)={ninf}  (expect ~[0,0,-1])")
print(f"  energy fraction within r<2*Rring = {frac:.4f} (localization; ->1 means localized)")
print("  azimuthal energy-density profile (rc: value):")
for k in range(0,nb,4):
    print(f"    r={rc[k]:5.2f}  ed={prof[k]:.4e}")
