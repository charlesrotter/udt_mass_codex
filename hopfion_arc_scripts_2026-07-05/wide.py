import os,sys,math,numpy as np,torch
torch.set_default_dtype(torch.float64)
REPO="/home/udt-admin/udt_mass_codex"; sys.path.insert(0,REPO)
import cell_solver_f2d as F2D

def cell_grid(Nr):
    zeta,Dz=F2D._cheb(Nr); ccw=F2D._cc_weights(Nr)
    return torch.tensor(zeta),torch.tensor(Dz),torch.tensor(ccw)
def load_cell(fname):
    d=torch.load(os.path.join(REPO,fname),map_location="cpu",weights_only=False)
    w=d["w"];Nr=d["Nr"];Nth=d["Nth"];Na=d["Na"];prm=d["prm"];i=0
    phi=w[i:i+Nr];i+=Nr; rho=w[i:i+Nr];i+=Nr; i+=Nr*Nth; i+=Na; i+=Na
    r_p=float(w[i])
    return dict(fname=fname,phi=phi.clone(),rho=rho.clone(),r_p=r_p,Nr=Nr,prm=tuple(prm))

# INDEPENDENT: build energy from scratch. E=INT (xi/2) rho^2 [Wk Th'^2 + sin^2Th (N^2/rho^2 - Wb Om2)] dr
def make_E(fld,branch,N,XI):
    zeta,Dz,ccw=cell_grid(fld["Nr"]); L=fld["r_p"]; sc=2.0/L
    phi=fld["phi"]; rho=fld["rho"]
    if branch=="B": Wk=torch.exp(-2*phi); Wb=torch.exp(2*phi)
    else: Wk=torch.ones_like(phi); Wb=torch.ones_like(phi)
    def E(theta,Om2):
        thp=sc*(Dz@theta); s2=torch.sin(theta)**2
        dens=(XI/2.0)*rho**2*(Wk*thp**2+s2*(N**2/rho**2-Wb*Om2))
        return (ccw*dens).sum()*(L/2.0)
    return E,Wk,Wb,rho
def trial(Nr,kind):
    zeta,_,_=cell_grid(Nr); x=(zeta+1.0)/2.0
    if kind=="linear": return math.pi*(1.0-x)
    if kind=="cos": return math.pi*torch.cos(math.pi*x/2.0)**2
    if kind=="tanh": return math.pi*0.5*(1-torch.tanh((x-0.5)*6))
def lammin(fld,branch,Om2,N,XI,kind,th0=None):
    E,_,_,_=make_E(fld,branch,N,XI); Nr=fld["Nr"]
    if th0 is None: th0=trial(Nr,kind)
    thc=th0[0].item(); ths=th0[-1].item(); u0=th0[1:-1].clone()
    def Ei(u):
        th=torch.cat([torch.tensor([thc]),u,torch.tensor([ths])]); return E(th,Om2)
    H=torch.func.hessian(Ei)(u0); H=0.5*(H+H.T)
    ev=torch.linalg.eigvalsh(H); return float(ev[0])
def relax(fld,branch,Om2,N,XI,kind,steps=4000,lr=1e-4):
    # gradient-descent Theta toward stationary point of E at this Om2 (Dirichlet ends)
    E,_,_,_=make_E(fld,branch,N,XI); Nr=fld["Nr"]; th0=trial(Nr,kind)
    thc=th0[0].item(); ths=th0[-1].item(); u=th0[1:-1].clone().requires_grad_(True)
    opt=torch.optim.Adam([u],lr=lr)
    for _ in range(steps):
        opt.zero_grad()
        th=torch.cat([torch.tensor([thc]),u,torch.tensor([ths])]); loss=E(th,Om2)
        loss.backward(); opt.step()
    th=torch.cat([torch.tensor([thc]),u.detach(),torch.tensor([ths])])
    return th

FIELDS=["E2b_A1Z1_P2_W4_wall.pt","E2b_A1Z8_P2_W2_wall.pt","E2b_A3Z1_P2_W2_wall.pt"]
print("WIDE Om2 SWEEP (far past B=0 'ceiling'): does lam_min EVER reach 0?")
for fn in FIELDS:
    f=load_cell(fn); Z,XI,KAP,N=f["prm"]; XI=float(XI); N=int(N)
    zeta,_,_=cell_grid(f["Nr"])
    for branch in ["B","A"]:
        phi=f["phi"]; 
        Wb=torch.exp(2*phi) if branch=="B" else torch.ones_like(phi)
        ceil=float((N**2/(f["rho"]**2*Wb)).min())
        # log-spaced Om2 from 0.1*ceil to 1e6*ceil
        oms=np.concatenate([[0.0],np.geomspace(0.1*ceil,1e6*ceil,24)])
        best=-1e99; bestom=0
        crossed=None
        for Om2 in oms:
            lm=lammin(f,branch,float(Om2),N,XI,"linear")
            if lm>best: best=lm; bestom=Om2
            if lm>=0 and crossed is None: crossed=Om2
        print(f"\n{fn} branch {branch}: ceil(B=0)={ceil:.3e}  N={N} XI={XI}")
        print(f"   linear-trial: lam_min(0)={lammin(f,branch,0.0,N,XI,'linear'):+.3e}"
              f"  MAX lam_min={best:+.3e} at Om2={bestom:.3e} (Om2/ceil={bestom/ceil:.1e})"
              f"  crosses0? {'YES @Om2='+f'{crossed:.2e}' if crossed else 'NO'}")
print("\n--- TRIAL-ARTIFACT TEST: relax Theta at Om2=0 then re-measure lam_min (field1,B) ---")
f=load_cell(FIELDS[0]); Z,XI,KAP,N=f["prm"]; XI=float(XI); N=int(N)
for kind in ["linear","cos","tanh"]:
    lm0=lammin(f,"B",0.0,N,XI,kind)
    th_relaxed=relax(f,"B",0.0,N,XI,kind)
    lm_rel=lammin(f,"B",0.0,N,XI,kind,th0=th_relaxed)
    # gradient norm at relaxed point
    print(f"  trial={kind}: lam_min(trial)={lm0:+.3e}  -> after relax lam_min={lm_rel:+.3e}"
          f"  Theta_relaxed[0,mid,end]=({float(th_relaxed[0]):.2f},{float(th_relaxed[len(th_relaxed)//2]):.2f},{float(th_relaxed[-1]):.2f})")
