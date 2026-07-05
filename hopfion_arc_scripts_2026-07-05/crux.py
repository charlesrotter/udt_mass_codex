import os,sys,math,numpy as np,torch
torch.set_default_dtype(torch.float64)
REPO="/home/udt-admin/udt_mass_codex"; sys.path.insert(0,REPO)
import cell_solver_f2d as F2D
def cell_grid(Nr):
    zeta,Dz=F2D._cheb(Nr); ccw=F2D._cc_weights(Nr)
    return torch.tensor(zeta),torch.tensor(Dz),torch.tensor(ccw)
def load(fn):
    d=torch.load(os.path.join(REPO,fn),map_location="cpu",weights_only=False)
    w=d["w"];Nr=d["Nr"];Nth=d["Nth"];Na=d["Na"];prm=d["prm"];i=0
    phi=w[i:i+Nr];i+=Nr; rho=w[i:i+Nr];i+=Nr
    r_p=float(w[2*Nr+Nr*Nth+2*Na])
    return dict(phi=phi.clone(),rho=rho.clone(),r_p=r_p,Nr=Nr,prm=tuple(prm))
def make_E(f,branch,N,XI):
    zeta,Dz,ccw=cell_grid(f["Nr"]); L=f["r_p"]; sc=2.0/L; phi=f["phi"];rho=f["rho"]
    Wk=torch.exp(-2*phi) if branch=="B" else torch.ones_like(phi)
    Wb=torch.exp(2*phi) if branch=="B" else torch.ones_like(phi)
    def E(th,Om2):
        thp=sc*(Dz@th); s2=torch.sin(th)**2
        return (ccw*((XI/2)*rho**2*(Wk*thp**2+s2*(N**2/rho**2-Wb*Om2)))).sum()*(L/2)
    return E
def trial(Nr):
    zeta,_,_=cell_grid(Nr); x=(zeta+1)/2; return math.pi*(1-x)
def lam_at(f,branch,Om2,N,XI,th):
    E=make_E(f,branch,N,XI); thc=th[0].item();ths=th[-1].item();u0=th[1:-1].clone()
    def Ei(u): return E(torch.cat([torch.tensor([thc]),u,torch.tensor([ths])]),Om2)
    H=torch.func.hessian(Ei)(u0);H=0.5*(H+H.T); return float(torch.linalg.eigvalsh(H)[0])
def relax(f,branch,Om2,N,XI,steps=20000,lr=3e-4):
    E=make_E(f,branch,N,XI); th0=trial(f["Nr"]); thc=th0[0].item();ths=th0[-1].item()
    u=th0[1:-1].clone().requires_grad_(True); opt=torch.optim.Adam([u],lr=lr)
    for _ in range(steps):
        opt.zero_grad(); th=torch.cat([torch.tensor([thc]),u,torch.tensor([ths])])
        loss=E(th,Om2); loss.backward(); opt.step()
    th=torch.cat([torch.tensor([thc]),u.detach(),torch.tensor([ths])])
    g=torch.autograd.functional.jacobian(lambda uu:E(torch.cat([torch.tensor([thc]),uu,torch.tensor([ths])]),Om2),u.detach())
    return th, float(torch.linalg.norm(g))

# ---- FULL Derrick curve, field2, branch B, several Om2 ----
f2=load("E2b_A1Z8_P2_W2_wall.pt"); Z,XI,K,N=f2["prm"];XI=float(XI);N=int(N)
zeta,_,_=cell_grid(f2["Nr"]); rn=f2["r_p"]*(zeta.numpy()+1)/2
rf=np.linspace(0,f2["r_p"],600); phif=np.interp(rf,rn,f2["phi"].numpy()); rhof=np.interp(rf,rn,f2["rho"].numpy())
Wkf=np.exp(-2*phif);Wbf=np.exp(2*phif)
ceil2=float((N**2/(f2["rho"].numpy()**2*np.exp(2*f2["phi"].numpy()))).min())
lams=np.linspace(0.03,2.5,60)
print(f"FIELD2 branch B full Derrick E(lam). ceil={ceil2:.3e}")
for Om2 in [0.0, ceil2, 10*ceil2, 1e3*ceil2]:
    Es=[]
    for lam in lams:
        x=np.clip((rf/f2["r_p"])/lam,0,1); th=math.pi*(1-x); thp=np.gradient(th,rf)
        Es.append(np.trapz((XI/2)*rhof**2*(Wkf*thp**2+np.sin(th)**2*(N**2/rhof**2-Wbf*Om2)),rf))
    Es=np.array(Es); im=int(np.argmin(Es))
    print(f"  Om2={Om2:.2e}(x{Om2/ceil2:.0e}) min@lam={lams[im]:.3f} E={Es[im]:.3e} | E@lam=2.5(expand)={Es[-1]:.3e} | interior_min? {0<im<len(lams)-1 and Es[-1]>Es[im]}")

# ---- DECISIVE: relax Theta to TRUE stationary point at Om2 with interior Derrick min, test Jacobi ----
print("\nDECISIVE relax-then-Jacobi (field2, branch B): is the stationary config STABLE?")
for Om2 in [0.0, ceil2, 10*ceil2, 100*ceil2, 1e3*ceil2]:
    th,gnorm=relax(f2,"B",Om2,N,XI)
    lm=lam_at(f2,"B",Om2,N,XI,th)
    print(f"  Om2={Om2:.2e}(x{Om2/ceil2:.0e}) |gradE|={gnorm:.2e}  lam_min@relaxed={lm:+.3e}  Th_mid={float(th[len(th)//2]):.3f}  {'*** STABLE window!' if lm>=0 else 'saddle/unstable'}")
