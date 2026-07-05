import numpy as np
S='/tmp/claude-1000/-home-udt-admin-udt-mass-codex/329d5fd9-3bad-41b4-8ec1-3f27625f5889/scratchpad/'
d=np.load(S+'stress_rtheta.npz')
rc=d['rc']; thc=d['thc']; Tthth=d['Tthth']; Tphph=d['Tphph']; nr=len(rc); nth=len(thc)
dr=rc[1]-rc[0]; dth=thc[1]-thc[0]; sin=np.sin(thc)

# ---- Step 1: shear response  Lbare[alpha]=-(r^4/w0)Tphph ; alpha=abar/w0 ----
# abar(r)=Green[-r^4 T](r) = r*Int_0^r r'^2 T dr'  - r^2*Int_r^inf r' T dr'   (T at each theta)
def green_response(T):  # T shape (nr,nth); returns abar(nr,nth) [w0-independent, =w0*alpha]
    out=np.zeros_like(T)
    for j in range(nth):
        Tj=T[:,j]
        f1=rc**2*Tj; I1=np.concatenate([[0],np.cumsum(0.5*(f1[1:]+f1[:-1])*dr)])  # Int_0^r r'^2 T
        f2=rc*Tj;    # Int_r^inf r' T  = total - Int_0^r
        cum2=np.concatenate([[0],np.cumsum(0.5*(f2[1:]+f2[:-1])*dr)]); tot2=cum2[-1]
        I2=tot2-cum2
        out[:,j]=rc*I1[:nr] - rc**2*I2[:nr]
    return out
abar=green_response(Tphph)   # =w0*alpha  (alpha=dh_thth)
bbar=green_response(Tthth)   # =w0*beta   (beta =dh_pspsi/sin^2)
# radial derivatives
def ddr(f):
    g=np.zeros_like(f); g[1:-1]=(f[2:]-f[:-2])/(2*dr); g[0]=(f[1]-f[0])/dr; g[-1]=(f[-1]-f[-2])/dr; return g
abar_p=np.vstack([ddr(abar[:,j]) for j in range(nth)]).T
bbar_p=np.vstack([ddr(bbar[:,j]) for j in range(nth)]).T
r=rc[:,None]
# ell2 (w0-independent form, built from abar,bbar) : ell2[a,b] with sin(theta) included
sinm=np.sin(thc)[None,:]
ell2_bar=(-2*r**2*abar_p*bbar_p + 2*r*(abar*abar_p+abar*bbar_p+bbar*abar_p+bbar*bbar_p)
          -3*abar**2 -2*abar*bbar -3*bbar**2)*sinm/(4*r**4)
Shat=ell2_bar.sum(1)*dth        # Sigma_hat(r)=int ell2[abar,bbar] dtheta  (w0-independent)
# Sigma(r; w0) = -(1/w0)*Shat
# fractional shear magnitude (w0-independent part): |abar|/r^2  -> eps = that /w0
fracshear_bar=np.max(np.abs(abar)/r**2)
print("max |abar|/r^2 (=w0*eps_max) = %.4f  -> eps_max = %.4f/w0"%(fracshear_bar,fracshear_bar))
print("Shat tail (r, Shat, r^2*Shat):")
for k in range(0,nr,24): print("  r=%.2f Shat=%.3e r^2Shat=%.3e"%(rc[k],Shat[k],rc[k]**2*Shat[k]))
print("int Shat dr =",np.sum(Shat)*dr, " (converged tail check via r^2 Shat ~ const?)")

# ---- Step 2: screened monopole solve  Zf(r^2 dphi')' + 8 w0 dphi = Sigma(r;w0) ----
# fine radial grid
Rout=60.0; M=6000; rf=np.linspace(rc[0], Rout, M); hf=rf[1]-rf[0]
Shat_f=np.interp(rf, rc, Shat, right=0.0)  # Shat on fine grid, 0 beyond source range
def solve_monopole(Zf, w0):
    Sig=-(1.0/w0)*Shat_f    # Sigma(r;w0)
    # operator Zf*(r^2 phi'' + 2 r phi') + 8 w0 phi = Sig
    a=np.zeros(M); b=np.zeros(M); c=np.zeros(M); rhs=Sig.copy()
    for i in range(1,M-1):
        ri=rf[i]
        b[i]=Zf*ri**2/hf**2*(-2) + 8*w0
        a[i]=Zf*(ri**2/hf**2 - ri/hf)      # coeff phi_{i-1}
        c[i]=Zf*(ri**2/hf**2 + ri/hf)      # coeff phi_{i+1}
    # BC: regularity at r0: dphi'(0)=0 -> phi[0]=phi[1]
    b[0]=1.0; c[0]=-1.0; rhs[0]=0.0
    # BC outer: phi=0
    b[-1]=1.0; rhs[-1]=0.0
    # Thomas solve (tridiagonal)
    from scipy.linalg import solve_banded
    ab=np.zeros((3,M))
    ab[0,1:]=c[:-1]; ab[1,:]=b; ab[2,:-1]=a[1:]
    phi=solve_banded((1,1),ab,rhs)
    return rf,phi
# read dq at several read-surfaces
def read_dq(rf,phi):
    out={}
    for rr in [6,8,10,15,20,30,50]:
        i=np.argmin(np.abs(rf-rr)); out[rr]=-rr*phi[i]
    # flux based: Q=Zf r^2 phi' ; dq_flux=-Q/Zf at read-surf
    return out

print("\n=== SWEEP dq(phi0), dm=-dq ===")
for Zf in [1.0,8.0]:
    phicrit=0.5*np.log(32/Zf)
    print(f"\n----- Z_phi={Zf}  critical depth phi0={phicrit:.3f} (w0=Zf/32={Zf/32:.4f}) -----")
    print("phi0   w0        eps_max   dq(r=10)   dq(r=20)  dq(r=50)  dm=-dq(r=20)  sign")
    for phi0 in np.linspace(0,3,31):
        w0=np.exp(-2*phi0); eps=fracshear_bar/w0
        rf,phi=solve_monopole(Zf,w0); dq=read_dq(rf,phi)
        dm=-dq[20]
        print("%.2f  %.4e  %7.3f  %9.3e %9.3e %9.3e  %10.3e  %s"%(
            phi0,w0,eps,dq[10],dq[20],dq[50],dm,'+' if dm>0 else ('-' if dm<0 else '0')))
