import os,sys,math,numpy as np,torch
torch.set_default_dtype(torch.float64)
REPO="/home/udt-admin/udt_mass_codex"; sys.path.insert(0,REPO)
import cell_solver_f2d as F2D
def cell_grid(Nr):
    zeta,Dz=F2D._cheb(Nr); ccw=F2D._cc_weights(Nr); return torch.tensor(zeta),torch.tensor(Dz),torch.tensor(ccw)
def load(fn):
    d=torch.load(os.path.join(REPO,fn),map_location="cpu",weights_only=False)
    w=d["w"];Nr=d["Nr"];Nth=d["Nth"];Na=d["Na"];prm=d["prm"];i=0
    phi=w[i:i+Nr];i+=Nr; rho=w[i:i+Nr];i+=Nr; r_p=float(w[2*Nr+Nr*Nth+2*Na])
    return dict(phi=phi.clone(),rho=rho.clone(),r_p=r_p,Nr=Nr,prm=tuple(prm))
f=load("E2b_A1Z8_P2_W2_wall.pt"); Z,XI,K,N=f["prm"];XI=float(XI);N=int(N)
zeta,Dz,ccw=cell_grid(f["Nr"]); L=f["r_p"]; sc=2/L; phi=f["phi"];rho=f["rho"]
Wk=torch.exp(-2*phi);Wb=torch.exp(2*phi)
ceil=float((N**2/(rho.numpy()**2*np.exp(2*phi.numpy()))).min())
def parts(th,Om2):
    thp=sc*(Dz@th);s2=torch.sin(th)**2
    Ekin=(ccw*(XI/2)*rho**2*Wk*thp**2).sum()*(L/2)
    Ewind=(ccw*(XI/2)*rho**2*s2*(N**2/rho**2)).sum()*(L/2)
    Eom=(ccw*(XI/2)*rho**2*s2*(-Wb*Om2)).sum()*(L/2)
    return float(Ekin),float(Ewind),float(Eom)
def E(th,Om2):
    thp=sc*(Dz@th);s2=torch.sin(th)**2
    return (ccw*(XI/2)*rho**2*(Wk*thp**2+s2*(N**2/rho**2-Wb*Om2))).sum()*(L/2)
def relax(Om2,steps=30000,lr=3e-4):
    x=(zeta+1)/2; th0=math.pi*(1-x); thc=th0[0].item();ths=th0[-1].item()
    u=th0[1:-1].clone().requires_grad_(True);opt=torch.optim.Adam([u],lr=lr)
    for _ in range(steps):
        opt.zero_grad(); th=torch.cat([torch.tensor([thc]),u,torch.tensor([ths])])
        E(th,Om2).backward();opt.step()
    return torch.cat([torch.tensor([thc]),u.detach(),torch.tensor([ths])])
rr=(L*(zeta.numpy()+1)/2)
print(f"field2 branch B, ceil={ceil:.3e}, r_p={L:.1f}")
print("r/r_p grid:", np.array2string(rr/L,precision=2,max_line_width=200))
for Om2 in [0.0, 10*ceil, 1e3*ceil]:
    th=relax(Om2); Ek,Ew,Eo=parts(th,Om2)
    print(f"\nOm2={Om2:.2e} (x{Om2/ceil:.0e})  Etot={float(E(th,Om2)):.3e}")
    print(f"   Theta(r): "+np.array2string(th.numpy(),precision=2,max_line_width=200))
    print(f"   Ekin={Ek:.3e}  Ewind={Ew:.3e}  Eomega={Eo:.3e}   (Eomega unbounded-below in Om2? Eo/Om2={Eo/Om2 if Om2>0 else 0:.3e})")
# runaway demo: Eomega linear in Om2 at fixed spread profile
print("\nRUNAWAY CHECK: hold a fixed spread profile (linear trial), scale Om2 -> E linear to -inf?")
x=(zeta+1)/2; thlin=math.pi*(1-x)
for Om2 in [0.0,1e2*ceil,1e4*ceil,1e6*ceil]:
    print(f"   Om2={Om2:.2e}: E(linear-trial)={float(E(thlin,Om2)):.3e}")
