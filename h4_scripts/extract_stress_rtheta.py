import torch, numpy as np, os
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'
FP='/home/udt-admin/udt_mass_codex/hopfion_arc_scripts_2026-07-05/prod_an256.npz'
d=np.load(FP); n=torch.tensor(d['n'],device=dev); N=int(d['N']); L=float(d['L']); h=float(d['h'])
xi=float(d['xi']); kap=float(d['kappa'])
x=torch.linspace(-L,L,N,device=dev)
def dc(f,ax): return (torch.roll(f,-1,ax)-torch.roll(f,1,ax))/(2*h)
n=n/n.norm(dim=0,keepdim=True)
dn=[dc(n,i+1) for i in range(3)]
e2d=0.5*xi*sum((dn[i]*dn[i]).sum(0) for i in range(3))
def cross(a,b): return torch.stack([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],0)
F={}
for i in range(3):
    for j in range(3):
        if i!=j: F[(i,j)]=(n*cross(dn[i],dn[j])).sum(0)
e4d=torch.zeros_like(e2d)
for i in range(3):
    for j in range(3):
        if i!=j: e4d=e4d+0.25*kap*F[(i,j)]*F[(i,j)]
ed=e2d+e4d
E=(ed.sum()*h**3).item(); E2=(e2d.sum()*h**3).item(); E4=(e4d.sum()*h**3).item()
print(f"E={E:.3f} E2={E2:.3f} E4={E4:.3f} E2/E4={E2/E4:.5f}")
sig=torch.zeros(3,3,N,N,N,device=dev)
for i in range(3):
    for j in range(3):
        t=xi*(dn[i]*dn[j]).sum(0); fk=torch.zeros_like(t)
        for k in range(3):
            if k==i or k==j: continue
            Fik=F.get((i,k),torch.zeros_like(t)); Fjk=F.get((j,k),torch.zeros_like(t))
            fk=fk+kap*Fik*Fjk
        sig[i,j]=t+fk-(ed if i==j else 0)
X,Y,Z=torch.meshgrid(x,x,x,indexing='ij')
rr=torch.sqrt(X*X+Y*Y+Z*Z)+1e-12; rho=torch.sqrt(X*X+Y*Y)+1e-12
er=torch.stack([X/rr,Y/rr,Z/rr],0)
eth=torch.stack([X*Z/(rr*rho),Y*Z/(rr*rho),-rho/rr],0)
eph=torch.stack([-Y/rho,X/rho,torch.zeros_like(X)],0)
def contract(u,v):
    s=torch.zeros(N,N,N,device=dev)
    for i in range(3):
        for j in range(3): s=s+u[i]*sig[i,j]*v[j]
    return s
Trr=contract(er,er); Tthth=contract(eth,eth); Tphph=contract(eph,eph)
# bin to (r,theta) grid, averaging over azimuth (m=0 axisymmetric projection)
nr=240; nth=45
rmax=L
rb=torch.clamp((rr/rmax*nr).long(),0,nr-1)
costh=(Z/rr).clamp(-1,1); theta=torch.acos(costh)
tb=torch.clamp((theta/np.pi*nth).long(),0,nth-1)
lin=rb*nth+tb
def binavg(fld):
    num=torch.zeros(nr*nth,device=dev); cnt=torch.zeros(nr*nth,device=dev)
    num.scatter_add_(0,lin.flatten(),fld.flatten()); cnt.scatter_add_(0,lin.flatten(),torch.ones_like(fld.flatten()))
    return (num/cnt.clamp(min=1)).reshape(nr,nth).cpu().numpy(), cnt.reshape(nr,nth).cpu().numpy()
Tthth_rt,cnt=binavg(Tthth); Tphph_rt,_=binavg(Tphph); Trr_rt,_=binavg(Trr)
rc=(np.arange(nr)+0.5)/nr*rmax; thc=(np.arange(nth)+0.5)/nth*np.pi
_OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'stress_rtheta_h3.npz')
np.savez(_OUT,
         rc=rc,thc=thc,Tthth=Tthth_rt,Tphph=Tphph_rt,Trr=Trr_rt,cnt=cnt,E=E,E2=E2,E4=E4,xi=xi,kap=kap)
print('saved ->',_OUT)
# compactness + sector integrals (4pi int r^2 <.> dr with shell-avg over theta)
def shellavg_theta(fld_rt):  # average over theta with sin weight
    w=np.sin(thc); return (fld_rt*w).sum(1)/w.sum()
tau=Tthth_rt+Tphph_rt; shear=Tthth_rt-Tphph_rt
tau0=shellavg_theta(tau); sh0=shellavg_theta(shear); Trr0=shellavg_theta(Trr_rt)
dr=rc[1]-rc[0]
def rint(f): return float(np.sum(f*rc**2)*dr*4*np.pi)
print("sector ints: tau=%.2f shear=%.2f Trr=%.2f  (N1: -90,+139,+90)"%(rint(tau0),rint(sh0),rint(Trr0)))
print("compactness |tau0| tail:")
for k in range(0,nr,20): print("  r=%.2f tau0=%.3e"%(rc[k],tau0[k]))
