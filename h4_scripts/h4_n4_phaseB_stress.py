import torch, numpy as np, math
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'
d=np.load('hopfion_arc_scripts_2026-07-05/prod_an256.npz')
n=torch.tensor(d['n'],device=dev); N=int(d['N']); L=float(d['L']); h=float(d['h'])
xi=float(d['xi']); kap=float(d['kappa'])
x=torch.linspace(-L,L,N,device=dev)
def dc(f,ax): return (torch.roll(f,-1,ax)-torch.roll(f,1,ax))/(2*h)
n=n/n.norm(dim=0,keepdim=True)
dn=[dc(n,i+1) for i in range(3)]   # dn[i] = d_i n  (3,N,N,N)
# energy density pieces
e2d=0.5*xi*sum((dn[i]*dn[i]).sum(0) for i in range(3))
def cross(a,b): return torch.stack([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],0)
F={}
for i in range(3):
    for j in range(3):
        if i==j: continue
        F[(i,j)]=(n*cross(dn[i],dn[j])).sum(0)
e4d=torch.zeros_like(e2d)
for i in range(3):
    for j in range(3):
        if i==j: continue
        e4d=e4d+0.25*kap*F[(i,j)]*F[(i,j)]
ed=e2d+e4d
E=(ed.sum()*h**3).item(); E2=(e2d.sum()*h**3).item(); E4=(e4d.sum()*h**3).item()
print(f"check E={E:.3f} E2={E2:.3f} E4={E4:.3f} E2/E4={E2/E4:.4f}")
# static stress tensor sigma_ij = xi dn_i.dn_j + kap sum_k F_ik F_jk - delta_ij ed
sig=torch.zeros(3,3,N,N,N,device=dev)
for i in range(3):
    for j in range(3):
        t=xi*(dn[i]*dn[j]).sum(0)
        fk=torch.zeros_like(t)
        for k in range(3):
            if k==i or k==j: continue
            # F_ik F_jk ; F symmetric? F_ik=-F_ki
            Fik=F[(i,k)] if (i,k) in F else torch.zeros_like(t)
            Fjk=F[(j,k)] if (j,k) in F else torch.zeros_like(t)
            fk=fk+kap*Fik*Fjk
        sig[i,j]=t+fk-(ed if i==j else 0)
# trace check (virial): int trace = -E2+E4 ~ 0
tr=(sig[0,0]+sig[1,1]+sig[2,2])
print("int trace(sigma) =", (tr.sum()*h**3).item(), " (expect -E2+E4 =",(-E2+E4),")")
# ---- project to spherical shells. build r,theta and radial/transverse components ----
X,Y,Z=torch.meshgrid(x,x,x,indexing='ij')
rr=torch.sqrt(X*X+Y*Y+Z*Z)+1e-12
rho=torch.sqrt(X*X+Y*Y)+1e-12
# unit vectors
er=torch.stack([X/rr,Y/rr,Z/rr],0)
eth=torch.stack([X*Z/(rr*rho),Y*Z/(rr*rho),-rho/rr],0)   # theta-hat
eph=torch.stack([-Y/rho,X/rho,torch.zeros_like(X)],0)     # phi-hat
def contract(u,v):
    s=torch.zeros(N,N,N,device=dev)
    for i in range(3):
        for j in range(3):
            s=s+u[i]*sig[i,j]*v[j]
    return s
Trr=contract(er,er); Tthth=contract(eth,eth); Tphph=contract(eph,eph); Trth=contract(er,eth)
# transverse (2d) stress in ORTHONORMAL frame: trace tau=Tthth+Tphph, traceless shear sh=Tthth-Tphph, and Tthph
Tthph=contract(eth,eph)
tau=Tthth+Tphph          # transverse trace (breathing source)
shear=Tthth-Tphph        # transverse traceless (shear source)
# ---- radial binning: shell-average (ell=0) of tau, shear, Trr, |T| ----
nb=64; redges=torch.linspace(0,L,nb+1,device=dev)
rc=0.5*(redges[1:]+redges[:-1])
idx=torch.clamp((rr/L*nb).long(),0,nb-1)
def shell_avg(fld):
    out=torch.zeros(nb,device=dev); cnt=torch.zeros(nb,device=dev)
    out.scatter_add_(0,idx.flatten(),fld.flatten()); cnt.scatter_add_(0,idx.flatten(),torch.ones_like(fld.flatten()))
    return (out/cnt.clamp(min=1)).cpu().numpy()
tau0=shell_avg(tau); sh0=shell_avg(shear); Trr0=shell_avg(Trr)
absT=shell_avg((tau.abs()+shear.abs()+Trr.abs()))
rc_np=rc.cpu().numpy()
# ell=2 projection of tau and shear: weight P2(cos th)=(3cos^2-1)/2, cos th=Z/rr
P2=(3*(Z/rr)**2-1)/2
def shell_proj(fld,w):
    num=torch.zeros(nb,device=dev);cnt=torch.zeros(nb,device=dev)
    num.scatter_add_(0,idx.flatten(),(fld*w).flatten()); cnt.scatter_add_(0,idx.flatten(),torch.ones_like(fld.flatten()))
    return (num/cnt.clamp(min=1)).cpu().numpy()
tau2=shell_proj(tau,P2); sh2=shell_proj(shear,P2)
print("\n r_c   <tau>(l0)   <shear>(l0)  <Trr>(l0)   tau(l2)    shear(l2)")
for k in range(0,nb,3):
    print(f"{rc_np[k]:5.2f}  {tau0[k]:10.4f}  {sh0[k]:10.4f}  {Trr0[k]:9.4f}  {tau2[k]:9.4f}  {sh2[k]:9.4f}")
# integrated measures of source strength (r^2 weight ~ shell volume)
r2=torch.tensor(rc_np**2)
import numpy as np
dr=(rc_np[1]-rc_np[0])
def rad_int(f): return float(np.sum(f*rc_np**2)*dr*4*np.pi)   # crude 4pi r^2 integral of shell-avg
print("\n4pi.int r^2 <tau> dr =",rad_int(tau0),"  <shear> =",rad_int(sh0),"  <Trr> =",rad_int(Trr0))
print("magnitude scale: E=",E," ; peak |tau|=",np.abs(tau0).max()," peak|shear|=",np.abs(sh0).max())
np.savez('/tmp/claude-1000/-home-udt-admin-udt-mass-codex/329d5fd9-3bad-41b4-8ec1-3f27625f5889/scratchpad/stress_profiles.npz',
         rc=rc_np,tau0=tau0,sh0=sh0,Trr0=Trr0,tau2=tau2,sh2=sh2)
