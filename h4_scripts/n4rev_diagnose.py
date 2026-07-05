import numpy as np
S='/tmp/claude-1000/-home-udt-admin-udt-mass-codex/329d5fd9-3bad-41b4-8ec1-3f27625f5889/scratchpad/'
d=np.load(S+'stress_rtheta.npz')
rc=d['rc']; thc=d['thc']; Tthth=d['Tthth']; Tphph=d['Tphph']; nr=len(rc); nth=len(thc)
dr=rc[1]-rc[0]; dth=thc[1]-thc[0]

def green_response(T):
    out=np.zeros_like(T)
    for j in range(nth):
        Tj=T[:,j]; f1=rc**2*Tj
        I1=np.concatenate([[0],np.cumsum(0.5*(f1[1:]+f1[:-1])*dr)])[:nr]
        f2=rc*Tj; cum2=np.concatenate([[0],np.cumsum(0.5*(f2[1:]+f2[:-1])*dr)])[:nr]; I2=cum2[-1]-cum2
        out[:,j]=rc*I1 - rc**2*I2
    return out
abar=green_response(Tphph); bbar=green_response(Tthth)
# (1) shear growth: abar(r) at outer radii, fractional abar/r^2
print("=== SHEAR RESPONSE growth (theta=pi/2 equatorial, j=nth//2) ===")
j=nth//2
for k in range(0,nr,24):
    print("  r=%.2f  abar=%.3e  abar/r^2(frac)=%.3e"%(rc[k],abar[k,j],abar[k,j]/rc[k]**2))
# fit abar ~ C1*r + C2*r^2 in outer region r in [5,6]
msk=(rc>=5)&(rc<=5.9)
A=np.vstack([rc[msk],rc[msk]**2]).T
for lbl,fld in [('abar(Tphph)',abar),('bbar(Tthth)',bbar)]:
    coef,_,_,_=np.linalg.lstsq(A,fld[msk,j],rcond=None)
    print(f"  outer fit {lbl}: C1(r-mode)={coef[0]:.3e}  C2(r^2-mode)={coef[1]:.3e}  -> r-mode dominates? {abs(coef[0])>abs(coef[1])*5}")

# (2) Shat and running integral
def ddr(f):
    g=np.zeros_like(f); g[1:-1]=(f[2:]-f[:-2])/(2*dr); g[0]=(f[1]-f[0])/dr; g[-1]=(f[-1]-f[-2])/dr; return g
abar_p=np.vstack([ddr(abar[:,j]) for j in range(nth)]).T
bbar_p=np.vstack([ddr(bbar[:,j]) for j in range(nth)]).T
r=rc[:,None]; sinm=np.sin(thc)[None,:]
ell2=(-2*r**2*abar_p*bbar_p+2*r*(abar*abar_p+abar*bbar_p+bbar*abar_p+bbar*bbar_p)
      -3*abar**2-2*abar*bbar-3*bbar**2)*sinm/(4*r**4)
Shat=ell2.sum(1)*dth
runint=np.concatenate([[0],np.cumsum(0.5*(Shat[1:]+Shat[:-1])*dr)])[:nr]
print("\n=== running int_0^R Shat dr  (unscreened dq = -(1/(Zf w0))*this) ===")
for k in range(0,nr,24):
    print("  R=%.2f  int_0^R Shat=%.3f   r^2*Shat=%.2f"%(rc[k],runint[k],rc[k]**2*Shat[k]))
print("  => sign of int Shat:", '+' if runint[-1]>0 else '-', " magnitude", runint[-1])
print("  => leading unscreened dq = -(1/(Zf*w0))*intShat -> sign of dq:", '-' if runint[-1]>0 else '+',
      " ; dm=-dq sign:", '+' if runint[-1]>0 else '-')

# (3) interior dphi' check: solve screened monopole for a DEEP case (real roots) and show dphi' != 0 interior
Rout=60.0; M=6000; rf=np.linspace(rc[0],Rout,M); hf=rf[1]-rf[0]
Shat_f=np.interp(rf,rc,Shat,right=0.0)
from scipy.linalg import solve_banded
def solve_monopole(Zf,w0):
    Sig=-(1.0/w0)*Shat_f
    a=np.zeros(M);b=np.zeros(M);c=np.zeros(M);rhs=Sig.copy()
    for i in range(1,M-1):
        ri=rf[i]; b[i]=Zf*ri**2/hf**2*(-2)+8*w0
        a[i]=Zf*(ri**2/hf**2-ri/hf); c[i]=Zf*(ri**2/hf**2+ri/hf)
    b[0]=1;c[0]=-1;rhs[0]=0; b[-1]=1;rhs[-1]=0
    ab=np.zeros((3,M)); ab[0,1:]=c[:-1]; ab[1,:]=b; ab[2,:-1]=a[1:]
    return rf,solve_banded((1,1),ab,rhs)
print("\n=== interior dphi' check (Zf=1, deep phi0=2.0, w0=0.0183; and Zf=8 phi0=1.0) ===")
for Zf,phi0 in [(1.0,2.0),(8.0,1.0)]:
    w0=np.exp(-2*phi0); rf,phi=solve_monopole(Zf,w0); dphip=np.gradient(phi,rf)
    imax=np.argmax(np.abs(dphip[:int(M*6/Rout)]))
    print(f"  Zf={Zf} phi0={phi0}: max|dphi'| in interior(r<6) = {abs(dphip[imax]):.3e} at r={rf[imax]:.2f}  -> dphi'!=0 interior: {abs(dphip[imax])>1e-9}")
    # dq read-surface dependence
    for rr in [7,10,20,40]:
        i=np.argmin(np.abs(rf-rr)); print("     dq(r=%2d)=%.3e"%(rr,-rr*phi[i]))
