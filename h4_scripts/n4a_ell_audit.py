import torch, numpy as np, math
torch.set_default_dtype(torch.float64)
dev='cuda' if torch.cuda.is_available() else 'cpu'
d=np.load('/home/udt-admin/udt_mass_codex/hopfion_arc_scripts_2026-07-05/prod_an256.npz')
n=torch.tensor(d['n'],device=dev); N=int(d['N']); L=float(d['L']); h=float(d['h'])
xi=float(d['xi']); kap=float(d['kappa'])
print(f"N={N} L={L} h={h} xi={xi} kap={kap}")
x=torch.linspace(-L,L,N,device=dev)
def dc(f,ax): return (torch.roll(f,-1,ax)-torch.roll(f,1,ax))/(2*h)
n=n/n.norm(dim=0,keepdim=True)
dn=[dc(n,i+1) for i in range(3)]
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
sig=torch.zeros(3,3,N,N,N,device=dev)
for i in range(3):
    for j in range(3):
        t=xi*(dn[i]*dn[j]).sum(0)
        fk=torch.zeros_like(t)
        for k in range(3):
            if k==i or k==j: continue
            Fik=F[(i,k)] if (i,k) in F else torch.zeros_like(t)
            Fjk=F[(j,k)] if (j,k) in F else torch.zeros_like(t)
            fk=fk+kap*Fik*Fjk
        sig[i,j]=t+fk-(ed if i==j else 0)
X,Y,Z=torch.meshgrid(x,x,x,indexing='ij')
rr=torch.sqrt(X*X+Y*Y+Z*Z)+1e-12
rho=torch.sqrt(X*X+Y*Y)+1e-12
er=torch.stack([X/rr,Y/rr,Z/rr],0)
eth=torch.stack([X*Z/(rr*rho),Y*Z/(rr*rho),-rho/rr],0)
eph=torch.stack([-Y/rho,X/rho,torch.zeros_like(X)],0)
def contract(u,v):
    s=torch.zeros(N,N,N,device=dev)
    for i in range(3):
        for j in range(3):
            s=s+u[i]*sig[i,j]*v[j]
    return s
Trr=contract(er,er); Tthth=contract(eth,eth); Tphph=contract(eph,eph)
tau=Tthth+Tphph       # transverse trace
shear=Tthth-Tphph     # transverse traceless (in orthonormal frame)
mu=(Z/rr)             # cos theta

# Legendre polynomials
def Pl(l,x):
    if l==0: return torch.ones_like(x)
    if l==2: return (3*x**2-1)/2
    if l==4: return (35*x**4-30*x**2+3)/8
    if l==6: return (231*x**6-315*x**4+105*x**2-5)/16

nb=96; redges=torch.linspace(0,L,nb+1,device=dev)
rc=0.5*(redges[1:]+redges[:-1]); rc_np=rc.cpu().numpy()
idx=torch.clamp((rr/L*nb).long(),0,nb-1)
dr=(rc_np[1]-rc_np[0])
def proj(fld,l):
    # coefficient c_l(r) = (2l+1)/2 * <fld * P_l> shell average (approx orthonormal on cos)
    w=Pl(l,mu)*(2*l+1)/2.0
    num=torch.zeros(nb,device=dev); cnt=torch.zeros(nb,device=dev)
    num.scatter_add_(0,idx.flatten(),(fld*w).flatten())
    cnt.scatter_add_(0,idx.flatten(),torch.ones_like(fld.flatten()))
    return (num/cnt.clamp(min=1)).cpu().numpy()

print("\n=== ell-content of the transverse SOURCE profiles (shell coeff c_l(r)) ===")
print("Note: shell-avg with P_l weight; c_l(r) is the Legendre coefficient of the angular profile at radius r.")
for name,fld in [('tau(trace)',tau),('shear',shear),('Trr',Trr)]:
    c0=proj(fld,0); c2=proj(fld,2); c4=proj(fld,4); c6=proj(fld,6)
    # radial power in each ell: integral of c_l(r)^2 * r^2 dr  (a measure of the mode's weight)
    def pw(c): return float(np.sum(c**2 * rc_np**2)*dr)
    p0,p2,p4,p6=pw(c0),pw(c2),pw(c4),pw(c6)
    tot=p0+p2+p4+p6+1e-30
    print(f"\n{name}: radial-power(c_l) l=0:{p0:.4e} l=2:{p2:.4e} l=4:{p4:.4e} l=6:{p6:.4e}")
    print(f"   fraction: l0={p0/tot:.3f} l2={p2/tot:.3f} l4={p4/tot:.3f} l6={p6/tot:.3f}")

# The MONOPOLE flux (delta q) at O(amp^2) ~ sum_ell <T_ell, Linv T_ell> (diagonal in ell since L has no ell(ell+1)).
# Proxy for the ell-sector contribution to the bilinear monopole: |c_ell|^2 radial power.
# Compare the ell=4 (and 6) contribution to ell=2 to see if truncating at ell=2 drops load-bearing monopole flux.
print("\n=== back-projection proxy: relative ell>=2 contributions to the O(amp^2) monopole ===")
print("(each ell contributes ~ integral c_ell(r)^2 * (radial Greens weight); here reported as raw |c_ell|^2 radial power)")
for name,fld in [('tau',tau),('shear',shear)]:
    c2=proj(fld,2); c4=proj(fld,4); c6=proj(fld,6)
    def pw(c): return float(np.sum(c**2 * rc_np**2)*dr)
    p2,p4,p6=pw(c2),pw(c4),pw(c6)
    print(f"{name}: l4/l2={p4/p2:.4f}  l6/l2={p6/p2:.4f}")

# also report where support ends (compactness)
tau0=proj(tau,0)
print("\ncompactness: |tau_l0(r)| tail:")
for k in range(0,nb,6):
    print(f"  r={rc_np[k]:5.2f}  tau_l0={tau0[k]: .4e}")
